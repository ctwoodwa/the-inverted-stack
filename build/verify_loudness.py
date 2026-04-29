"""Verify normalized chapter MP3s land within their target loudness spec.

ACX (Audible) rejects roughly 30% of indie audiobook submissions for
loudness or peak issues. This script re-measures each MP3 in
build/output/audiobook/ with ffmpeg's loudnorm filter (measurement-only
mode) and reports pass/fail against the chosen target preset.

Run this AFTER `python build/normalize.py [--target acx]`. Two-pass
linear normalization should land each chapter within ±0.5 LU of the
integrated-loudness target, but on long files the linear-mode estimate
can drift and produce sub-spec output that submission gatekeepers
catch. Verification with the same loudnorm measurement is the cheapest
way to catch this before submission.

Tolerances applied (matching ACX's published acceptance window):

    Integrated loudness:  target ± 1.0 LU
    True peak:            <= target + 0.0 dB  (must NOT exceed the ceiling)
    Loudness range:       <= target + 1.0 LU  (max LRA tolerance)

Targets are kept in lockstep with build/normalize.py — the same preset
table drives both scripts so a chapter normalized as `acx` is verified
against `acx`.

Optional noise-floor check (--check-noise) measures the ffmpeg silence
detector's quietest 0.5-second window. ACX requires <= -60 dBFS noise
floor; this is a heuristic — true ACX checking uses a long-form silence
analysis. Useful as a smoke test, not authoritative.

Usage:
    python build/verify_loudness.py                  # all chapters, podcast spec
    python build/verify_loudness.py --target acx     # all chapters, ACX spec
    python build/verify_loudness.py --only ch05      # one chapter
    python build/verify_loudness.py --target acx --check-noise

Exits with code 0 if every checked chapter passes, 1 if any fails, 2 on
infrastructure errors (missing folder, no MP3s, ffmpeg failure).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg

REPO = Path(__file__).resolve().parent.parent
AUDIO_DIR = REPO / "build" / "output" / "audiobook"

# Mirror normalize.TARGETS so the two scripts stay in lockstep. Prefer
# importing if both live in the same package; for now the duplication is
# trivial and avoids a sys.path dance for direct script invocation.
TARGETS: dict[str, dict] = {
    "podcast": {
        "I": -16.0,
        "TP": -1.5,
        "LRA": 11.0,
        "description": "Apple Books / Leanpub / generic podcast",
    },
    "acx": {
        "I": -19.0,
        "TP": -3.0,
        "LRA": 11.0,
        "description": "Audible / ACX submission spec",
    },
}

# Pass/fail tolerances. ACX is strict on TP (must not exceed) and looser
# on integrated loudness (within ±2 LU is technically acceptable, but ±1
# is conventional for indie submissions to avoid borderline rejects).
TOL_I = 1.0       # integrated loudness, ± LU
TOL_LRA = 1.0     # loudness range, only fails if exceeds target + this
NOISE_FLOOR_DB = -60.0  # ACX hard requirement; checked when --check-noise


def measure(ffmpeg: str, src: Path, target: dict) -> dict:
    """Re-run loudnorm in measurement mode against the given target.

    Returns the JSON measurement dict ffmpeg emits to stderr at the end
    of analysis. Same call shape as normalize.measure() so the readings
    here line up with what normalize.py used during the pass.
    """
    cmd = [
        ffmpeg, "-hide_banner", "-nostats", "-i", str(src),
        "-af",
        f"loudnorm=I={target['I']}:TP={target['TP']}:LRA={target['LRA']}:print_format=json",
        "-f", "null", "-",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    out = proc.stderr
    match = re.search(r"\{[\s\S]*?\}", out)
    if not match:
        raise RuntimeError(f"loudnorm measurement produced no JSON for {src.name}")
    return json.loads(match.group(0))


def check_noise_floor(ffmpeg: str, src: Path, threshold_db: float) -> tuple[bool, float | None]:
    """Heuristic noise-floor check via ffmpeg silencedetect.

    Looks for any 0.5-second window quieter than `threshold_db`. If even
    one such window exists, the floor at that point is at least as
    quiet as the threshold — return (True, measured_db). If silencedetect
    finds NO silent windows, the noise floor is louder than the target
    and we return (False, None). This is not a true integrated noise
    floor measurement; it is a fast smoke test.
    """
    cmd = [
        ffmpeg, "-hide_banner", "-nostats", "-i", str(src),
        "-af", f"silencedetect=noise={threshold_db}dB:duration=0.5",
        "-f", "null", "-",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    stderr = proc.stderr
    # silencedetect logs `[silencedetect ...] silence_start: T` and
    # `silence_end: T | silence_duration: D`. Any match means at least
    # one window quieter than threshold_db was found.
    match = re.search(r"silence_start:\s*([\d.]+)", stderr)
    if match:
        return True, float(threshold_db)
    return False, None


def verify_one(ffmpeg: str, src: Path, target: dict, target_name: str,
               check_noise: bool) -> tuple[bool, list[str]]:
    """Verify a single MP3 against the target spec. Returns (passed, reasons)."""
    failures: list[str] = []
    try:
        m = measure(ffmpeg, src, target)
    except subprocess.CalledProcessError as e:
        return False, [f"ffmpeg measurement failed: {e}"]
    except RuntimeError as e:
        return False, [str(e)]

    # input_i / input_tp / input_lra are the measured values for the file.
    # Earlier ffmpeg builds report these as numeric strings.
    measured_i = float(m.get("input_i", "0"))
    measured_tp = float(m.get("input_tp", "0"))
    measured_lra = float(m.get("input_lra", "0"))
    measured_thresh = float(m.get("input_thresh", "0"))

    if abs(measured_i - target["I"]) > TOL_I:
        failures.append(
            f"integrated loudness {measured_i:+.2f} LUFS out of target "
            f"{target['I']:+.1f} ± {TOL_I} LU"
        )
    if measured_tp > target["TP"]:
        failures.append(
            f"true peak {measured_tp:+.2f} dBTP exceeds ceiling {target['TP']:+.1f} dBTP"
        )
    if measured_lra > target["LRA"] + TOL_LRA:
        failures.append(
            f"loudness range {measured_lra:.2f} LU exceeds max "
            f"{target['LRA']:.1f} + {TOL_LRA:.1f} LU"
        )

    if check_noise:
        ok, _ = check_noise_floor(ffmpeg, src, NOISE_FLOOR_DB)
        if not ok:
            failures.append(
                f"no silence window quieter than {NOISE_FLOOR_DB} dBFS detected — "
                f"noise floor likely exceeds ACX requirement (heuristic only; "
                f"submit a true silence-floor measurement before final ACX upload)"
            )

    measurement_summary = (
        f"I={measured_i:+.2f} LUFS  TP={measured_tp:+.2f} dBTP  "
        f"LRA={measured_lra:.2f} LU  thresh={measured_thresh:.2f}"
    )

    if failures:
        return False, [measurement_summary] + failures
    return True, [measurement_summary]


def main() -> None:
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )
    ap.add_argument("--target", choices=list(TARGETS.keys()), default="podcast",
                    help="distribution target preset (default: podcast)")
    ap.add_argument("--only", help="only verify chapters whose name contains this substring")
    ap.add_argument("--check-noise", action="store_true",
                    help="add heuristic noise-floor check (silencedetect under -60 dBFS)")
    ap.add_argument("--quiet", action="store_true",
                    help="only print failing chapters (suppress passing-chapter output)")
    args = ap.parse_args()

    if not AUDIO_DIR.exists():
        print(f"Source folder missing: {AUDIO_DIR}", file=sys.stderr)
        sys.exit(2)

    target = TARGETS[args.target]
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    sources = sorted(AUDIO_DIR.glob("*.mp3"))
    # Skip sample renders by default — they're short and not part of the
    # distribution-master verification flow.
    sources = [p for p in sources if "_sample" not in p.stem]
    if args.only:
        sources = [p for p in sources if args.only in p.name]
    if not sources:
        print("No matching MP3s found.", file=sys.stderr)
        sys.exit(2)

    print(f"verify-loudness — {args.target} ({target['description']})")
    print(f"  target:   I={target['I']:+.1f} LUFS  TP={target['TP']:+.1f} dBTP  "
          f"LRA={target['LRA']:.1f} LU max")
    print(f"  tolerances: I=±{TOL_I:.1f} LU,  TP=hard ceiling,  LRA=+{TOL_LRA:.1f} LU max")
    if args.check_noise:
        print(f"  noise floor heuristic: any window quieter than {NOISE_FLOOR_DB:.1f} dBFS")
    print()

    pass_count = 0
    fail_count = 0
    for i, src in enumerate(sources, 1):
        passed, reasons = verify_one(ffmpeg, src, target, args.target, args.check_noise)
        prefix = "PASS" if passed else "FAIL"
        if passed:
            pass_count += 1
            if not args.quiet:
                print(f"  [{i:2d}/{len(sources)}] {prefix} {src.name}")
                print(f"             {reasons[0]}")
        else:
            fail_count += 1
            print(f"  [{i:2d}/{len(sources)}] {prefix} {src.name}", file=sys.stderr)
            for r in reasons:
                print(f"             {r}", file=sys.stderr)

    print()
    print(f"Verified {len(sources)} chapter(s):  {pass_count} pass,  {fail_count} fail")
    if fail_count:
        print(f"\n{fail_count} chapter(s) out of {args.target} spec. Re-run "
              f"`python build/normalize.py --target {args.target} --force --only <name>` "
              f"on each failing chapter, then verify again.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
