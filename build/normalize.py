"""EBU R128 loudness normalization for the audiobook MP3s.

Normalizes the per-chapter MP3 files in build/output/audiobook/ to the
audiobook submission spec used by Audible, ACX, and the major podcast
distributors:

    Integrated loudness:  -16 LUFS
    True peak:            -1.5 dBTP
    Loudness range:       11 LU (max)

Uses ffmpeg's `loudnorm` filter via the static binary bundled with the
`imageio-ffmpeg` pip package — no system ffmpeg install required.

Two-pass mode (default) is the audiobook-grade path: ffmpeg first measures
the chapter, then re-encodes with the measured offsets applied. Single-pass
linear mode is faster (--single-pass) but slightly less accurate at the
boundaries of the LRA target.

Usage:
    python build/normalize.py                 # all chapters, two-pass, in-place
    python build/normalize.py --single-pass   # faster, less accurate
    python build/normalize.py --only ch05     # one chapter
    python build/normalize.py --suffix _norm  # write to ch05_norm.mp3 (don't overwrite)
    python build/normalize.py --dry-run       # report which files would be processed
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import imageio_ffmpeg

REPO = Path(__file__).resolve().parent.parent
AUDIO_DIR = REPO / "build" / "output" / "audiobook"

# Audible / ACX-aligned target. -16 LUFS is the platform-agnostic audiobook
# integrated loudness; podcasts typically run -16 LUFS as well.
TARGET_I = -16.0     # integrated loudness (LUFS)
TARGET_TP = -1.5     # true peak ceiling (dBTP)
TARGET_LRA = 11.0    # loudness range (LU)


def measure(ffmpeg: str, src: Path) -> dict:
    """First-pass loudnorm measurement. Returns the JSON measurement dict."""
    cmd = [
        ffmpeg, "-hide_banner", "-nostats", "-i", str(src),
        "-af",
        f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}:print_format=json",
        "-f", "null", "-",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    # ffmpeg writes the JSON block to stderr at the end of analysis
    out = proc.stderr
    match = re.search(r"\{[\s\S]*?\}", out)
    if not match:
        raise RuntimeError(f"loudnorm measurement produced no JSON for {src.name}")
    return json.loads(match.group(0))


def normalize_two_pass(ffmpeg: str, src: Path, dst: Path) -> None:
    """Two-pass loudnorm: measure, then re-encode with measured offsets."""
    m = measure(ffmpeg, src)
    flt = (
        f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}:"
        f"measured_I={m['input_i']}:"
        f"measured_TP={m['input_tp']}:"
        f"measured_LRA={m['input_lra']}:"
        f"measured_thresh={m['input_thresh']}:"
        f"offset={m['target_offset']}:"
        f"linear=true:print_format=summary"
    )
    cmd = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "warning",
        "-i", str(src),
        "-af", flt,
        # Preserve sample rate (Kokoro outputs 22.05 kHz; loudnorm internally
        # resamples to 192k, so we restore on output).
        "-ar", "44100",
        # Mono speech at 96 kbps = audiobook quality floor.
        "-c:a", "libmp3lame", "-b:a", "96k", "-ac", "1",
        str(dst),
    ]
    subprocess.run(cmd, check=True)


def normalize_single_pass(ffmpeg: str, src: Path, dst: Path) -> None:
    """Single-pass loudnorm. ~3x faster than two-pass; slightly less accurate
    at the edges of the LRA target. Acceptable for podcast-tier listening,
    not for Audible submission."""
    flt = f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}"
    cmd = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "warning",
        "-i", str(src),
        "-af", flt,
        "-ar", "44100",
        "-c:a", "libmp3lame", "-b:a", "96k", "-ac", "1",
        str(dst),
    ]
    subprocess.run(cmd, check=True)


def main() -> None:
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )
    ap.add_argument("--only", help="only process chapters whose name contains this substring")
    ap.add_argument("--suffix", default="",
                    help="output suffix before .mp3 (e.g. '_norm' writes ch05_norm.mp3). "
                         "Default: empty (overwrite source in place via temp file).")
    ap.add_argument("--single-pass", action="store_true",
                    help="single-pass mode (~3x faster, slightly less accurate)")
    ap.add_argument("--dry-run", action="store_true", help="list files that would be processed")
    ap.add_argument("--force", action="store_true",
                    help="re-normalize even if output is newer than source")
    args = ap.parse_args()

    if not AUDIO_DIR.exists():
        print(f"Source folder missing: {AUDIO_DIR}", file=sys.stderr)
        sys.exit(2)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"ffmpeg: {Path(ffmpeg).name}")
    print(f"target: I={TARGET_I} LUFS, TP={TARGET_TP} dBTP, LRA={TARGET_LRA} LU")
    print(f"mode:   {'single-pass (fast)' if args.single_pass else 'two-pass (accurate)'}")

    sources = sorted(AUDIO_DIR.glob("*.mp3"))
    if args.only:
        sources = [p for p in sources if args.only in p.name]
    if not sources:
        print("No matching MP3s found.")
        return

    normalize = normalize_single_pass if args.single_pass else normalize_two_pass

    t0 = time.time()
    for i, src in enumerate(sources, 1):
        if args.suffix:
            dst = src.with_name(src.stem + args.suffix + ".mp3")
        else:
            # In-place: write to temp, then atomically replace source.
            dst = src.with_name(src.stem + ".__norm_tmp__.mp3")

        if args.dry_run:
            print(f"  [{i:2d}/{len(sources)}] would normalize {src.name}")
            continue

        if not args.force and dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            print(f"  [{i:2d}/{len(sources)}] skip up-to-date: {src.name}")
            continue

        ti = time.time()
        try:
            normalize(ffmpeg, src, dst)
        except subprocess.CalledProcessError as e:
            print(f"  [{i:2d}/{len(sources)}] FAILED {src.name}: {e}", file=sys.stderr)
            if dst.exists():
                dst.unlink()
            continue

        if not args.suffix:
            shutil.move(str(dst), str(src))
            final = src
        else:
            final = dst

        elapsed = time.time() - ti
        size_mb = final.stat().st_size / 1024 / 1024
        print(f"  [{i:2d}/{len(sources)}] {final.name:<50} {size_mb:5.1f} MB  {elapsed:5.1f}s")

    print(f"\nTotal wall time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
