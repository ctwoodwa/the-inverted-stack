"""Pre-Phase-4 stale-draft detector.

If any chapter source under chapters/<part>/ has mtime newer than its
corresponding chapters/_voice-drafts/final/<ch>.md, the draft is stale
and voice-pass needs to re-run for that chapter (council finding C8).

Sources without a corresponding draft are NOT stale — they simply have
not been voice-passed yet (e.g., a new chapter, or a chapter the user
chose to skip).

Promoted chapters are NOT stale either: a Phase 4 promotion overwrites
the source with the draft content (updating mtime), but content-wise
they are equivalent. We detect this via the sidecar manifest at
`<source>.manifest.json` — its presence means the chapter is post-promotion
and the mtime inversion is expected.

Usage:
    python build/check_stale.py
Exits 0 if all drafts are at-or-newer than their source (or manifested), 1 otherwise.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHAPTERS = REPO / "chapters"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_stale_drafts(chapters_root: Path) -> list[str]:
    """Return the stems of chapter drafts that are stale relative to source.

    A draft is stale when its source file's mtime is greater than the draft's
    mtime — meaning the source was edited after the draft was generated.

    Exception: if a sidecar manifest exists at <source>.manifest.json AND
    the source SHA matches the manifest's promoted_sha256, the chapter has
    been formally promoted (Phase 4) and the mtime inversion is expected.
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
        if source.stat().st_mtime <= draft.stat().st_mtime:
            continue  # Draft is fresh (or contemporaneous)
        # Source is newer than draft — check whether the chapter was promoted.
        manifest = source.with_suffix(".manifest.json")
        if manifest.exists():
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
                if data.get("promoted_sha256") == _sha256(source):
                    continue  # Promoted; mtime inversion is expected.
            except (OSError, json.JSONDecodeError):
                pass  # Manifest unreadable — fall through to stale.
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
