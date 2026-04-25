# build/check_audit.py
"""Reference-integrity check: every jurisdiction in inline prose appears in Appendix F.

Usage:
    python build/check_audit.py
Exits 0 on PASS, 1 on FAIL with diagnostic.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHAPTERS = REPO / "chapters"
APPENDIX_F = CHAPTERS / "appendices" / "appendix-f-regulatory-coverage.md"

JURISDICTION_PATTERNS = [
    r"GDPR", r"Schrems", r"DPDP", r"DIFC", r"LGPD",
    r"POPIA", r"NDPR", r"NDPA", r"\bPIPA\b", r"PIPL", r"APPI",
    r"242-FZ", r"LFPDPPP", r"Ley 1581", r"Ley 25\.326", r"CCPA", r"CPRA",
    r"HIPAA", r"FERPA", r"GLBA", r"PDPA",
]
PATTERN = re.compile("|".join(JURISDICTION_PATTERNS))


def find_jurisdictions_in_chapter(path: Path) -> set[str]:
    """Return distinct jurisdiction tokens found in a chapter file."""
    return set(PATTERN.findall(path.read_text(encoding="utf-8")))


def find_jurisdictions_in_appendix_f(path: Path) -> set[str]:
    """Return distinct jurisdiction tokens declared in Appendix F."""
    return set(PATTERN.findall(path.read_text(encoding="utf-8")))


def main() -> int:
    if not APPENDIX_F.exists():
        print(f"ERROR: {APPENDIX_F} does not exist; create it before running this check.", file=sys.stderr)
        return 1
    declared = find_jurisdictions_in_appendix_f(APPENDIX_F)
    failures: list[str] = []
    for ch in sorted(CHAPTERS.glob("**/*.md")):
        if "_voice-drafts" in ch.parts or ch == APPENDIX_F:
            continue
        used = find_jurisdictions_in_chapter(ch)
        orphans = used - declared
        if orphans:
            failures.append(f"{ch.relative_to(REPO).as_posix()}: {sorted(orphans)}")
    if failures:
        print("FAIL — jurisdictions in chapters not declared in Appendix F:")
        for f in failures:
            print(f"  {f}")
        return 1
    print(f"PASS — every jurisdiction in chapters appears in Appendix F.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
