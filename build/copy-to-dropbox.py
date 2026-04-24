"""Copy generated audiobook files to a destination folder (typically Dropbox).

Default destination is the author's local Dropbox; override via --dest or the
INVERTED_STACK_AUDIO_DEST environment variable. The script is skip-if-newer
by default — only copies files whose source mtime is newer than the
destination, so re-runs are cheap.

Usage:
    python build/copy-to-dropbox.py                     # MP3s + manifest
    python build/copy-to-dropbox.py --include-m4b       # also the .m4b
    python build/copy-to-dropbox.py --include-scripts   # also narration .txt
    python build/copy-to-dropbox.py --dest D:/elsewhere # override path
    python build/copy-to-dropbox.py --dry-run           # report only

Run after build/audiobook.py finishes — the script does not detect
in-flight renders. Files modified within the last 5 seconds are
considered unstable and skipped (use --no-stability-check to override).
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AUDIO_DIR = REPO / "build" / "output" / "audiobook"
EPUB_DIR = REPO / "build" / "output"

# Hardcoded fallback for this repo's primary author. Override via --dest
# or the INVERTED_STACK_AUDIO_DEST environment variable for other machines.
DEFAULT_DEST = Path(r"C:\Users\Chris\Dropbox\Personal-Chris\books\the-inverted-stack")

STABILITY_WINDOW_SEC = 5.0


def is_stable(path: Path, window: float = STABILITY_WINDOW_SEC) -> bool:
    """Return False if the file was modified within the last `window` seconds."""
    age = time.time() - path.stat().st_mtime
    return age >= window


def should_copy(src: Path, dst: Path) -> bool:
    """Skip-if-newer: copy only when source is newer or destination missing."""
    if not dst.exists():
        return True
    return src.stat().st_mtime > dst.stat().st_mtime + 1.0


def copy_one(src: Path, dst: Path, dry_run: bool, check_stability: bool) -> str:
    """Copy a single file; return a one-line status string."""
    if check_stability and not is_stable(src):
        return f"skip (in-flight, mtime <{STABILITY_WINDOW_SEC:.0f}s ago): {src.name}"
    if not should_copy(src, dst):
        return f"skip (up-to-date):     {src.name}"
    size_mb = src.stat().st_size / (1024 * 1024)
    if dry_run:
        return f"would copy ({size_mb:5.1f} MB): {src.name}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return f"copied   ({size_mb:5.1f} MB):  {src.name}"


def main() -> None:
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )
    ap.add_argument(
        "--dest",
        default=os.environ.get("INVERTED_STACK_AUDIO_DEST", str(DEFAULT_DEST)),
        help=f"destination folder. Default: {DEFAULT_DEST} "
             f"(or INVERTED_STACK_AUDIO_DEST env var)",
    )
    ap.add_argument("--include-scripts", action="store_true",
                    help="also copy the per-chapter narration .txt scripts")
    ap.add_argument("--include-m4b", action="store_true",
                    help="also copy any .m4b audiobook bundles in the source dir")
    ap.add_argument("--include-epub", action="store_true",
                    help="also copy the .epub from build/output/")
    ap.add_argument("--include-pdf", action="store_true",
                    help="also copy any .pdf from build/output/")
    ap.add_argument("--no-manifest", action="store_false", dest="manifest", default=True,
                    help="skip manifest.json (default: copy it)")
    ap.add_argument("--no-stability-check", action="store_false",
                    dest="stability", default=True,
                    help="copy files even if modified in the last "
                         f"{STABILITY_WINDOW_SEC:.0f}s (use only when you know "
                         "no render is in progress)")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would be copied without doing it")
    args = ap.parse_args()

    if not AUDIO_DIR.exists():
        print(f"Source folder missing: {AUDIO_DIR}", file=sys.stderr)
        sys.exit(2)

    dest = Path(args.dest)
    print(f"Source:      {AUDIO_DIR}")
    print(f"Destination: {dest}")
    if args.dry_run:
        print("(dry run - no files will be copied)")

    queue: list[tuple[Path, Path]] = []

    for mp3 in sorted(AUDIO_DIR.glob("*.mp3")):
        queue.append((mp3, dest / mp3.name))

    if args.manifest:
        manifest = AUDIO_DIR / "manifest.json"
        if manifest.exists():
            queue.append((manifest, dest / manifest.name))

    if args.include_m4b:
        for m4b in sorted(AUDIO_DIR.glob("*.m4b")):
            queue.append((m4b, dest / m4b.name))

    if args.include_scripts:
        scripts_src = AUDIO_DIR / "scripts"
        if scripts_src.exists():
            for txt in sorted(scripts_src.glob("*.txt")):
                queue.append((txt, dest / "scripts" / txt.name))

    if args.include_epub:
        for epub in sorted(EPUB_DIR.glob("*.epub")):
            queue.append((epub, dest / epub.name))

    if args.include_pdf:
        for pdf in sorted(EPUB_DIR.glob("*.pdf")):
            queue.append((pdf, dest / pdf.name))

    if not queue:
        print("Nothing to copy.")
        return

    copied = 0
    skipped = 0
    for src, dst in queue:
        result = copy_one(src, dst, args.dry_run, args.stability)
        print(f"  {result}")
        if result.startswith("copied") or result.startswith("would"):
            copied += 1
        else:
            skipped += 1

    verb = "would copy" if args.dry_run else "copied"
    print(f"\n{copied} {verb}, {skipped} skipped")


if __name__ == "__main__":
    main()
