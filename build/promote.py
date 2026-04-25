"""Phase 4 promotion script.

Promotes a voice-passed draft from chapters/_voice-drafts/final/<ch>.md
into chapters/<part>/<ch>.md after verifying the draft's SHA-256 matches
the recorded log entry from Phase 3. Writes a sidecar manifest alongside
the source as the permanent audit trail.

Council findings addressed:
- C3: per-promotion sidecar manifest with full provenance
- C11: hash verification before promotion (catches tampering, partial writes,
       or accidental edits between pass and promotion)

Usage:
    python build/promote.py --chapter ch01-when-saas-fights-reality
    python build/promote.py --all                 # promote every available draft
    python build/promote.py --reject ch15 --reason "voice-passed worse than source"
    python build/promote.py --chapter ch01 --accept-manual-edit  # bypass hash check
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHAPTERS = REPO / "chapters"
DRAFTS_FINAL = CHAPTERS / "_voice-drafts" / "final"
LOG_DIR = CHAPTERS / "_voice-drafts" / "_log"
REJECTION_LOG = CHAPTERS / "_voice-drafts" / "_rejections.jsonl"


class HashMismatchError(Exception):
    """Raised when the draft's SHA-256 does not match the log entry."""


def compute_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_source(chapter_stem: str) -> Path | None:
    """Locate a chapter's source file under chapters/, excluding _voice-drafts/."""
    for p in CHAPTERS.glob(f"**/{chapter_stem}.md"):
        if "_voice-drafts" in p.parts:
            continue
        return p
    return None


def latest_log_for(chapter_stem: str, pass_num: int, log_dir: Path) -> dict | None:
    """Return the most recent log entry for the given chapter and pass number,
    or None if no log entry exists. Picks the lexically last filename, which
    works because timestamps are encoded ISO-style at the start of the name."""
    candidates = sorted(log_dir.glob(f"*-{chapter_stem}-pass{pass_num}.json"))
    if not candidates:
        return None
    return json.loads(candidates[-1].read_text(encoding="utf-8"))


def promote_chapter(
    source: Path, draft: Path, log_dir: Path,
    promoter: str, promoted_at_iso: str,
    accept_manual_edit: bool = False,
) -> Path:
    """Promote a draft to source. Returns the manifest path.

    Raises HashMismatchError if draft's SHA does not match the log entry,
    unless accept_manual_edit=True. Raises FileNotFoundError if no log
    entry exists for the chapter (no audit trail = no promotion).
    """
    chapter_stem = source.stem
    log = latest_log_for(chapter_stem, 2, log_dir)
    if log is None:
        log = latest_log_for(chapter_stem, 1, log_dir)
    if log is None:
        raise FileNotFoundError(
            f"no log entry for {chapter_stem}; promotion requires Phase 3 audit trail"
        )

    draft_sha = compute_sha256(draft)
    if not accept_manual_edit and log["output_sha256"] != draft_sha:
        raise HashMismatchError(
            f"draft SHA {draft_sha} != log SHA {log['output_sha256']} for {chapter_stem}; "
            f"either re-run pass with --force, or pass --accept-manual-edit if the diff is intentional"
        )

    # Copy draft over source (the actual promotion)
    shutil.copyfile(draft, source)
    promoted_sha = compute_sha256(source)

    manifest = {
        **log,
        "promoted_sha256": promoted_sha,
        "promoted_at_iso": promoted_at_iso,
        "promoter": promoter,
        "manual_edit": bool(accept_manual_edit),
    }
    manifest_path = source.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path


def log_rejection(chapter_stem: str, reason: str, rejected_at_iso: str, rejecter: str) -> None:
    """Append a REJECT decision to chapters/_voice-drafts/_rejections.jsonl."""
    REJECTION_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "chapter": chapter_stem,
        "decision": "REJECT",
        "reason": reason,
        "rejected_at_iso": rejected_at_iso,
        "rejecter": rejecter,
    }
    with REJECTION_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def _git_user() -> str:
    """Best-effort git user identity for the manifest. Returns 'unknown' on failure."""
    try:
        name = subprocess.check_output(
            ["git", "config", "user.name"], text=True, stderr=subprocess.DEVNULL
        ).strip()
        email = subprocess.check_output(
            ["git", "config", "user.email"], text=True, stderr=subprocess.DEVNULL
        ).strip()
        return f"{name} <{email}>" if name and email else "unknown"
    except Exception:
        return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )
    ap.add_argument("--chapter", help="single chapter stem to promote")
    ap.add_argument("--all", action="store_true", help="promote every available draft")
    ap.add_argument("--reject", help="record a REJECT decision (requires --reason)")
    ap.add_argument("--reason", help="reason for reject (required with --reject)")
    ap.add_argument(
        "--accept-manual-edit", action="store_true",
        help="accept hash mismatch (the draft was manually edited post-pass; record the override in the manifest)",
    )
    args = ap.parse_args()

    if args.reject:
        if not args.reason:
            print("ERROR: --reject requires --reason", file=sys.stderr)
            return 2
        rejected_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        log_rejection(args.reject, args.reason, rejected_at, _git_user())
        print(f"REJECT {args.reject}: {args.reason}")
        return 0

    if not (args.chapter or args.all):
        ap.print_help()
        return 2

    promoter = _git_user()
    promoted_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    chapters: list[str] = []
    if args.chapter:
        chapters = [args.chapter]
    else:
        chapters = sorted(d.stem for d in DRAFTS_FINAL.glob("*.md"))

    failures: list[str] = []
    for ch in chapters:
        source = find_source(ch)
        if source is None:
            print(f"SKIP {ch}: no source under chapters/")
            continue
        draft = DRAFTS_FINAL / f"{ch}.md"
        if not draft.exists():
            print(f"SKIP {ch}: no draft at {draft.relative_to(REPO).as_posix()}")
            continue
        try:
            manifest_path = promote_chapter(
                source=source, draft=draft, log_dir=LOG_DIR,
                promoter=promoter, promoted_at_iso=promoted_at,
                accept_manual_edit=args.accept_manual_edit,
            )
            print(f"OK   {ch} -> {source.relative_to(REPO).as_posix()} (manifest: {manifest_path.name})")
        except HashMismatchError as e:
            print(f"FAIL {ch}: {e}", file=sys.stderr)
            failures.append(ch)
        except FileNotFoundError as e:
            print(f"FAIL {ch}: {e}", file=sys.stderr)
            failures.append(ch)
        except Exception as e:
            print(f"FAIL {ch}: {type(e).__name__}: {e}", file=sys.stderr)
            failures.append(ch)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
