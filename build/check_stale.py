"""Pre-Phase-4 stale-draft detector.

If any chapter source under chapters/<part>/ has mtime newer than its
corresponding chapters/_voice-drafts/final/<ch>.md, the draft is stale
and voice-pass needs to re-run for that chapter (council finding C8).

Sources without a corresponding draft are NOT stale — they simply have
not been voice-passed yet (e.g., a new chapter, or a chapter the user
chose to skip).

Usage:
    python build/check_stale.py
Exits 0 if all drafts are at-or-newer than their source, 1 if any are stale.
"""
from __future__ import annotations
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHAPTERS = REPO / "chapters"


def find_stale_drafts(chapters_root: Path) -> list[str]:
    """Return the stems of chapter drafts that are stale relative to source.

    A draft is stale when its source file's mtime is greater than the draft's
    mtime — meaning the source was edited after the draft was generated.
    """
    final_dir = chapters_root / "_voice-drafts" / "final"
    if not final_dir.exists():
        return []
    stale: list[str] = []
    for source in chapters_root.glob("**/*.md"):
        if "_voice-drafts" in source.parts:
            continue
        draft = final_dir / source.name
        if not draft.exists():
            continue  # No draft = not stale, just not voice-passed yet
        if source.stat().st_mtime > draft.stat().st_mtime:
            stale.append(source.stem)
    return stale


def main() -> int:
    stale = find_stale_drafts(CHAPTERS)
    if stale:
        print("STALE drafts (source edited after voice-pass):")
        for s in stale:
            print(f"  {s}")
        print()
        print("Re-run voice-pass for each stale chapter:")
        for s in stale:
            print(f"  python build/voice-pass.py --only {s} --force")
        return 1
    print("OK — all drafts are at-or-newer than their source.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
