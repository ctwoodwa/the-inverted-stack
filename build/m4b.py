"""Build a single .m4b audiobook file from the per-chapter MP3s.

Reads build/output/audiobook/manifest.json in chapter order, concatenates the
MP3s, transcodes to AAC-in-MP4 (.m4b), and embeds chapter markers + book-level
metadata (title, author, genre=Audiobook). Uses the static ffmpeg bundled with
the `imageio-ffmpeg` pip package — no system ffmpeg install required.

Usage:
    python build/m4b.py                  # default 96 kbps AAC mono (audiobook quality floor)
    python build/m4b.py --bitrate 128k   # higher quality, ~33% larger file
    python build/m4b.py --bitrate 64k    # podcast tier
    python build/m4b.py --out custom.m4b
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg

REPO = Path(__file__).resolve().parent.parent
AUDIO_DIR = REPO / "build" / "output" / "audiobook"
MANIFEST = AUDIO_DIR / "manifest.json"
DEFAULT_OUT = AUDIO_DIR / "the-inverted-stack.m4b"

BOOK_TITLE = "The Inverted Stack: Local-First Nodes in a SaaS World"
BOOK_AUTHOR = "Chris Woodward"
BOOK_DATE = "2026"
BOOK_DESCRIPTION = (
    "A practitioner's guide to local-first architecture for software "
    "architects, technical founders, and senior engineers."
)


def chapter_title_from_md(md_path: Path) -> str:
    """Pull the first H1 out of the chapter markdown as the chapter title."""
    for line in md_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return md_path.stem


def mp3_duration_ms(path: Path) -> int:
    """Compute duration of a 128 kbps CBR MP3 by byte count, skipping ID3v2."""
    data = path.read_bytes()
    audio_start = 0
    if data[:3] == b"ID3":
        size = (data[6] << 21) | (data[7] << 14) | (data[8] << 7) | data[9]
        audio_start = 10 + size
    audio_bytes = len(data) - audio_start
    # 128 kbps = 16000 bytes/sec => ms = bytes * 1000 / 16000 = bytes / 16
    return round(audio_bytes * 1000 / 16000)


def escape_metadata(value: str) -> str:
    """Escape ffmetadata special chars per ffmpeg docs."""
    return (
        value.replace("\\", "\\\\")
        .replace("=", r"\=")
        .replace(";", r"\;")
        .replace("#", r"\#")
        .replace("\n", " ")
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT,
                    help=f"output .m4b path (default: {DEFAULT_OUT.name})")
    ap.add_argument("--bitrate", default="96k",
                    help="AAC bitrate (default: 96k — audiobook quality floor; "
                         "Audible accepts 64-320k, but 96k is the threshold below "
                         "which speech artifacts become audible on critical listening)")
    ap.add_argument("--keep-temp", action="store_true",
                    help="keep intermediate concat-list.txt and ffmetadata.txt")
    args = ap.parse_args()

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    chapters = manifest["chapters"]
    if not chapters:
        print("Manifest has no chapters. Run build/audiobook.py first.", file=sys.stderr)
        sys.exit(1)

    list_file = AUDIO_DIR / "concat-list.txt"
    metadata_file = AUDIO_DIR / "ffmetadata.txt"

    entries = []
    cursor_ms = 0
    for c in chapters:
        mp3_path = REPO / c["output"]
        md_path = REPO / c["source"]
        if not mp3_path.exists():
            print(f"Missing MP3: {mp3_path}", file=sys.stderr)
            sys.exit(2)
        title = chapter_title_from_md(md_path)
        dur_ms = mp3_duration_ms(mp3_path)
        entries.append({"path": mp3_path, "title": title, "start_ms": cursor_ms,
                        "end_ms": cursor_ms + dur_ms})
        cursor_ms += dur_ms

    # concat demuxer input list — forward slashes required on Windows
    with list_file.open("w", encoding="utf-8") as f:
        for e in entries:
            p = str(e["path"]).replace("\\", "/")
            f.write(f"file '{p}'\n")

    # ffmetadata file — book-level tags + per-chapter markers
    with metadata_file.open("w", encoding="utf-8") as f:
        f.write(";FFMETADATA1\n")
        f.write(f"title={escape_metadata(BOOK_TITLE)}\n")
        f.write(f"artist={escape_metadata(BOOK_AUTHOR)}\n")
        f.write(f"album_artist={escape_metadata(BOOK_AUTHOR)}\n")
        f.write(f"album={escape_metadata(BOOK_TITLE)}\n")
        f.write(f"date={BOOK_DATE}\n")
        f.write("genre=Audiobook\n")
        f.write(f"comment={escape_metadata(BOOK_DESCRIPTION)}\n")
        for e in entries:
            f.write("\n[CHAPTER]\n")
            f.write("TIMEBASE=1/1000\n")
            f.write(f"START={e['start_ms']}\n")
            f.write(f"END={e['end_ms']}\n")
            f.write(f"title={escape_metadata(e['title'])}\n")

    cmd = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "warning",
        "-f", "concat", "-safe", "0", "-i", str(list_file),
        "-i", str(metadata_file),
        "-map_metadata", "1",
        "-map", "0:a",
        "-c:a", "aac", "-b:a", args.bitrate, "-ac", "1",
        "-movflags", "+faststart",
        str(args.out),
    ]
    print(f"Concatenating {len(entries)} chapters -> {args.out.relative_to(REPO).as_posix()}")
    print(f"  total duration: {cursor_ms/1000/3600:.2f} hours")
    print(f"  ffmpeg: {Path(ffmpeg).name}")
    subprocess.run(cmd, check=True)

    if not args.keep_temp:
        list_file.unlink(missing_ok=True)
        metadata_file.unlink(missing_ok=True)

    out_size_mb = args.out.stat().st_size / 1024 / 1024
    print(f"\nM4B written: {args.out.relative_to(REPO).as_posix()}")
    print(f"  size: {out_size_mb:.1f} MB")
    print(f"  chapters: {len(entries)}")
    print(f"  first chapter: {entries[0]['title']!r}")
    print(f"  last chapter: {entries[-1]['title']!r}")


if __name__ == "__main__":
    main()
