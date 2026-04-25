"""Embed cover art as an ID3v2 APIC frame in every chapter MP3.

Audiobook players (Apple Books, Plex, Smart Audiobook Player, BookFusion)
read the APIC frame to display per-track cover art. Without it, individual
chapter MP3s show generic file icons rather than the book cover.

Source: assets/cover-square.jpg (1400×1400 — Apple Books / Audible
audiobook standard). The source can be overridden via --cover.

Uses ffmpeg via imageio_ffmpeg — copies the audio stream (no re-encode)
and adds the cover as an attached_pic stream. This preserves the loudness
normalization done by build/normalize.py and adds ~50–100 KB per chapter.

Usage:
    python build/embed-cover.py                 # all chapters, default cover
    python build/embed-cover.py --only ch05     # one chapter
    python build/embed-cover.py --cover other.jpg
    python build/embed-cover.py --dry-run
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

import imageio_ffmpeg

REPO = Path(__file__).resolve().parent.parent
AUDIO_DIR = REPO / "build" / "output" / "audiobook"
CHAPTERS_DIR = REPO / "chapters"
MANIFEST = AUDIO_DIR / "manifest.json"
DEFAULT_COVER = REPO / "assets" / "cover-square.jpg"

BOOK_TITLE = "The Inverted Stack: Local-First Nodes in a SaaS World"
BOOK_AUTHOR = "Christopher Wood"
BOOK_DATE = "2026"
BOOK_GENRE = "Audiobook"


def chapter_title_from_md(md_path: Path) -> str:
    """Pull the first H1 out of the chapter markdown as the chapter title."""
    for line in md_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return md_path.stem


def build_chapter_title_map() -> dict[str, str]:
    """MP3 stem -> chapter title from the markdown source. Reads the audiobook
    manifest if present (preserves original chapter ordering and titles);
    falls back to scanning chapters/ when manifest is missing."""
    titles: dict[str, str] = {}
    if MANIFEST.exists():
        import json
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        for c in manifest.get("chapters", []):
            mp3_stem = Path(c["output"]).stem
            md_path = REPO / c["source"]
            if md_path.exists():
                titles[mp3_stem] = chapter_title_from_md(md_path)
    return titles


def has_attached_pic(ffmpeg: str, mp3: Path) -> bool:
    """Return True if the MP3 already carries an attached_pic stream."""
    proc = subprocess.run(
        [ffmpeg, "-i", str(mp3)],
        capture_output=True, text=True,
    )
    return "attached pic" in proc.stderr.lower()


def embed(ffmpeg: str, src: Path, cover: Path, chapter_title: str,
          track_n: int | None = None, total_tracks: int | None = None) -> None:
    """Embed cover + full ID3v2 metadata into src in place via temp + rename.

    Writes:
      - APIC (attached_pic) cover image
      - title  (chapter title)
      - artist (book author)
      - album_artist (book author)
      - album  (book title)
      - genre  (Audiobook)
      - date   (book year)
      - track  (NN/TOTAL) when provided
    """
    tmp = src.with_name(src.stem + ".__cover_tmp__.mp3")
    cmd = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "warning",
        "-i", str(src),
        "-i", str(cover),
        "-map", "0:a",
        "-map", "1",
        "-c", "copy",
        "-id3v2_version", "3",
        "-write_id3v1", "1",
        "-disposition:v:0", "attached_pic",
        "-metadata:s:v:0", "title=Cover",
        "-metadata:s:v:0", "comment=Cover (front)",
        "-metadata", f"title={chapter_title}",
        "-metadata", f"artist={BOOK_AUTHOR}",
        "-metadata", f"album_artist={BOOK_AUTHOR}",
        "-metadata", f"album={BOOK_TITLE}",
        "-metadata", f"genre={BOOK_GENRE}",
        "-metadata", f"date={BOOK_DATE}",
    ]
    if track_n and total_tracks:
        cmd += ["-metadata", f"track={track_n}/{total_tracks}"]
    cmd.append(str(tmp))
    try:
        subprocess.run(cmd, check=True)
        shutil.move(str(tmp), str(src))
    except subprocess.CalledProcessError:
        if tmp.exists():
            tmp.unlink()
        raise


def main() -> None:
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )
    ap.add_argument("--cover", type=Path, default=DEFAULT_COVER,
                    help=f"cover image (jpg/png), default {DEFAULT_COVER.relative_to(REPO).as_posix()}")
    ap.add_argument("--only", help="only chapters whose name contains this substring")
    ap.add_argument("--force", action="store_true",
                    help="re-embed even if an attached_pic stream already exists")
    ap.add_argument("--dry-run", action="store_true", help="report only")
    args = ap.parse_args()

    if not args.cover.exists():
        print(f"Cover not found: {args.cover}", file=sys.stderr)
        sys.exit(2)
    if not AUDIO_DIR.exists():
        print(f"Source folder missing: {AUDIO_DIR}", file=sys.stderr)
        sys.exit(2)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"ffmpeg: {Path(ffmpeg).name}")
    print(f"cover:  {args.cover.relative_to(REPO).as_posix()}")

    sources = sorted(AUDIO_DIR.glob("*.mp3"))
    # Skip helper files (QA fixture, etc.)
    sources = [s for s in sources if not s.name.startswith("_")]
    if args.only:
        sources = [s for s in sources if args.only in s.name]
    if not sources:
        print("No matching MP3s.")
        return

    t0 = time.time()
    embedded = 0
    skipped = 0
    for i, src in enumerate(sources, 1):
        if args.dry_run:
            tag = "(has cover)" if has_attached_pic(ffmpeg, src) else "(needs cover)"
            print(f"  [{i:2d}/{len(sources)}] {src.name}  {tag}")
            continue

        if not args.force and has_attached_pic(ffmpeg, src):
            print(f"  [{i:2d}/{len(sources)}] skip (already has cover): {src.name}")
            skipped += 1
            continue

        ti = time.time()
        try:
            embed(ffmpeg, src, args.cover)
        except subprocess.CalledProcessError as e:
            print(f"  [{i:2d}/{len(sources)}] FAILED {src.name}: {e}", file=sys.stderr)
            continue
        size_mb = src.stat().st_size / 1024 / 1024
        print(f"  [{i:2d}/{len(sources)}] {src.name:<50} {size_mb:5.1f} MB  {time.time()-ti:4.1f}s")
        embedded += 1

    if not args.dry_run:
        print(f"\n{embedded} embedded, {skipped} skipped, {time.time()-t0:.1f}s total")


if __name__ == "__main__":
    main()
