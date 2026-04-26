"""Remediate first-use rule violations across all chapter sources.

For each chapter, find the first occurrence of each known acronym/product
that appears without a definition in its surrounding context, and inject
a parenthetical definition immediately after.

Mechanical, conservative, idempotent:
- Skips chapters with no violations
- Skips terms whose first occurrence is already defined (spell-out within
  ~120 chars, parenthetical, link, or "the X (TERM)" pattern)
- Skips ambiguous acronyms (multiple possible spell-outs — DPA is a notable
  example: 'Data Protection Act' vs 'Data Protection Authority')
- Skips occurrences inside code blocks, fenced code, HTML comments, or
  IEEE bracketed citation markers
- Skips the canonical examples appendix (appendix-e — citation style
  examples reference acronyms without prose definition by design)
- Uses abbreviation-first format: "GDPR (General Data Protection Regulation)"
  rather than full-form-first ("the General Data Protection Regulation (GDPR)")
  for mechanical simplicity. Author may refine high-traffic acronyms manually.

Usage:
    python build/remediate_first_use.py             # dry-run, list proposed changes
    python build/remediate_first_use.py --apply     # write changes to files
    python build/remediate_first_use.py --apply --only ch01  # one chapter
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHAPTERS = REPO / "chapters"

# Acronyms with a SINGLE canonical spell-out — eligible for auto-remediation.
# Ambiguous acronyms (DPA = Act vs Authority) are intentionally omitted; they
# need human judgement per occurrence.
ACRONYM_SPELLOUTS: dict[str, str] = {
    # Regulatory
    "GDPR": "General Data Protection Regulation",
    "DPDP": "Digital Personal Data Protection",
    "POPIA": "Protection of Personal Information Act",
    "NDPR": "Nigeria Data Protection Regulation",
    "NDPA": "Nigeria Data Protection Act",
    "LGPD": "Lei Geral de Proteção de Dados",
    "DIFC": "Dubai International Financial Centre",
    "DPL": "Data Protection Law",
    "PIPL": "Personal Information Protection Law",
    "PIPA": "Personal Information Protection Act",
    "APPI": "Act on the Protection of Personal Information",
    "LFPDPPP": "Ley Federal de Protección de Datos Personales en Posesión de los Particulares",
    "EDPB": "European Data Protection Board",
    "CNIL": "Commission nationale de l'informatique et des libertés",
    "BSI": "Bundesamt für Sicherheit in der Informationstechnik",
    "RBI": "Reserve Bank of India",
    "BFSI": "Banking, Financial Services, and Insurance",
    "ISMS-P": "Information Security Management System – Personal",
    "MLPS": "Multi-Level Protection Scheme",
    "HIPAA": "Health Insurance Portability and Accountability Act",
    "FERPA": "Family Educational Rights and Privacy Act",
    "GLBA": "Gramm-Leach-Bliley Act",
    "CCPA": "California Consumer Privacy Act",
    "CPRA": "California Privacy Rights Act",
    "PIPEDA": "Personal Information Protection and Electronic Documents Act",
    "ITAR": "International Traffic in Arms Regulations",
    "FedRAMP": "Federal Risk and Authorization Management Program",
    "CMMC": "Cybersecurity Maturity Model Certification",
    "ECOWAS": "Economic Community of West African States",
    "BAA": "Business Associate Agreement",
    # Geographic
    "GCC": "Gulf Cooperation Council",
    "CIS": "Commonwealth of Independent States",
    "APAC": "Asia-Pacific",
    "LATAM": "Latin America",
    "EEA": "European Economic Area",
    # Technical
    "CRDT": "Conflict-free Replicated Data Type",
    "CRDTs": "Conflict-free Replicated Data Types",
    "MDM": "Mobile Device Management",
    "SBOM": "Software Bill of Materials",
    "RBAC": "Role-Based Access Control",
    "DEK": "Data Encryption Key",
    "KEK": "Key Encryption Key",
    "HKDF": "HMAC-based Key Derivation Function",
    "HSM": "Hardware Security Module",
    "MFA": "Multi-Factor Authentication",
    "SSO": "Single Sign-On",
    "IdP": "Identity Provider",
    "CMK": "Customer-Managed Key",
    "BYOC": "Bring Your Own Cloud",
    "TPM": "Trusted Platform Module",
    "CBOR": "Concise Binary Object Representation",
    "DAG": "Directed Acyclic Graph",
    "RFC": "Request for Comments",
    "IETF": "Internet Engineering Task Force",
    "API": "Application Programming Interface",
    "TLS": "Transport Layer Security",
    "TCP": "Transmission Control Protocol",
    "WAL": "Write-Ahead Log",
    "ADR": "Architecture Decision Record",
    "FFI": "Foreign Function Interface",
    "SLA": "Service Level Agreement",
    "SLO": "Service Level Objective",
    # Roles / org
    "CISO": "Chief Information Security Officer",
    "CTO": "Chief Technology Officer",
    "ISV": "Independent Software Vendor",
    "SIer": "Systems Integrator",
    "SaaS": "Software as a Service",
    "ARCO": "Access, Rectification, Cancellation, and Opposition",
    "MAUI": ".NET Multi-platform App UI",
    "ICM": "Inverted Stack Chapter Methodology",
}

# Products with brief identifiers + link
PRODUCT_DEFINITIONS: dict[str, str] = {
    "Linear": "[linear.app](https://linear.app/), the issue tracker",
    "Figma": "[figma.com](https://www.figma.com/), the design tool",
    "Sunfish": "the open-source reference implementation, [github.com/ctwoodwa/Sunfish](https://github.com/ctwoodwa/Sunfish)",
    "YDotNet": "the .NET CRDT engine port of Yjs via Rust FFI",
    "Loro": "[github.com/loro-dev/loro](https://github.com/loro-dev/loro), a Rust-core CRDT library",
    "Yjs": "[github.com/yjs/yjs](https://github.com/yjs/yjs), the JavaScript CRDT library",
    "Automerge": "[github.com/automerge/automerge](https://github.com/automerge/automerge), a JSON-like CRDT library",
    "Pandoc": "the universal document converter",
    "Kokoro": "the local TTS engine",
    "MinIO": "self-hosted S3-compatible object storage",
    "Anchor": "the Zone A local-first desktop accelerator",
    "Bridge": "the Zone C hybrid SaaS accelerator",
    "Sigstore": "[sigstore.dev](https://www.sigstore.dev/), the supply-chain signing toolkit",
}

# Skip these chapters entirely (canonical examples + the appendix-f data table)
SKIP_CHAPTERS = {
    "appendix-e-citation-style.md",      # citation-format examples
    "appendix-f-regulatory-coverage.md",  # regulatory data table
    "foreword-placeholder.md",            # not real content
}


def strip_non_prose_for_search(text: str) -> str:
    """Mask code/comments/citations so first-occurrence search ignores them.

    Returns the text with non-prose regions replaced by spaces of equal length
    so character indices remain valid for the original text.
    """
    def mask(match: re.Match) -> str:
        return " " * (match.end() - match.start())

    text = re.sub(r"```.*?```", mask, text, flags=re.DOTALL)
    text = re.sub(r"`[^`]+`", mask, text)
    text = re.sub(r"<!--.*?-->", mask, text, flags=re.DOTALL)
    text = re.sub(r"\[\d+(?:[,\-]\d+)*\]", mask, text)  # citation markers
    return text


def is_already_defined(text: str, idx: int, term: str, evidence: str, window: int = 120) -> bool:
    """Check whether the term at `idx` is already defined within `window` chars."""
    start = max(0, idx - window)
    end = min(len(text), idx + len(term) + window)
    context = text[start:end].lower()
    return evidence.lower() in context


def remediate_chapter(path: Path, dry_run: bool) -> tuple[int, list[str]]:
    """Apply first-use remediations to one chapter file.

    Returns (changes_made, summary_lines).
    """
    text = path.read_text(encoding="utf-8")
    masked = strip_non_prose_for_search(text)
    changes_made = 0
    summary: list[str] = []

    # Process acronyms: each gets one inline parenthetical definition at first
    # un-defined occurrence. Sort longest first so e.g. "CRDTs" is fixed before
    # "CRDT" within the same pass, avoiding double-fix.
    for term in sorted(ACRONYM_SPELLOUTS.keys(), key=len, reverse=True):
        spellout = ACRONYM_SPELLOUTS[term]
        pattern = re.compile(r"\b" + re.escape(term) + r"\b")
        m = pattern.search(masked)
        if not m:
            continue
        if is_already_defined(text, m.start(), term, spellout):
            continue
        replacement = f"{term} ({spellout})"
        text = text[:m.start()] + replacement + text[m.end():]
        masked = strip_non_prose_for_search(text)
        changes_made += 1
        summary.append(f"  +acronym  {term} -> {term} ({spellout})")

    # Process products: similar pattern, with link/identifier
    for term in sorted(PRODUCT_DEFINITIONS.keys(), key=len, reverse=True):
        identifier = PRODUCT_DEFINITIONS[term]
        pattern = re.compile(r"\b" + re.escape(term) + r"\b")
        m = pattern.search(masked)
        if not m:
            continue
        if is_already_defined(text, m.start(), term, identifier.split(",")[0]):
            continue
        replacement = f"{term} ({identifier})"
        text = text[:m.start()] + replacement + text[m.end():]
        masked = strip_non_prose_for_search(text)
        changes_made += 1
        summary.append(f"  +product  {term} -> {term} ({identifier[:60]}...)")

    if changes_made and not dry_run:
        path.write_text(text, encoding="utf-8")

    return changes_made, summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry-run)")
    ap.add_argument("--only", help="filter chapters by substring (e.g. 'ch01')")
    args = ap.parse_args()

    targets = sorted(CHAPTERS.glob("**/*.md"))
    targets = [p for p in targets if "_voice-drafts" not in p.parts and not p.name.endswith(".manifest.json")]
    targets = [p for p in targets if p.name not in SKIP_CHAPTERS]
    if args.only:
        targets = [p for p in targets if args.only in p.name]

    total_changes = 0
    chapters_touched = 0
    for path in targets:
        rel = path.relative_to(REPO).as_posix()
        changes, summary = remediate_chapter(path, dry_run=not args.apply)
        if changes:
            chapters_touched += 1
            total_changes += changes
            print(f"\n{rel}:  {changes} change(s)")
            for line in summary:
                print(line)

    print()
    print("=" * 60)
    if args.apply:
        print(f"Applied {total_changes} change(s) across {chapters_touched} chapter(s).")
    else:
        print(f"DRY-RUN: would apply {total_changes} change(s) across {chapters_touched} chapter(s).")
        print("Re-run with --apply to write.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
