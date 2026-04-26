"""First-use rule checker.

Per the style guide: every acronym/initialism and every named product
must be defined on its first use within each chapter. This script
scans chapter sources, finds the first occurrence of each known term,
and reports any first occurrence that lacks a defining context.

Usage:
    python build/check_first_use.py             # full report
    python build/check_first_use.py --counts    # just per-chapter violation counts
    python build/check_first_use.py --term GDPR # only report violations for one term

Definition patterns recognized as acceptable:
    - Spell-out before abbreviation:
        "The General Data Protection Regulation (GDPR)"
        "Conflict-free Replicated Data Types (CRDTs)"
    - Abbreviation explained inline:
        "GDPR (General Data Protection Regulation)"
    - Markdown link or domain reference (for products):
        "[Linear](https://linear.app)" or "Linear (linear.app)"
        "Linear ([linear.app](...))"
    - Definitional phrase:
        "Linear, the issue tracker"
        "Linear — the issue tracker"

Exit code: 0 if zero violations, 1 if any violations found.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHAPTERS = REPO / "chapters"

# Acronyms and initialisms with their canonical spell-outs.
# A first use is "defined" if the spell-out appears within ~80 chars before
# the abbreviation, or the abbreviation appears within ~80 chars after the
# spell-out, or the abbreviation appears in parentheses immediately after
# the spell-out.
ACRONYMS: dict[str, list[str]] = {
    # Regulatory / compliance
    "GDPR": ["General Data Protection Regulation"],
    "DPDP": ["Digital Personal Data Protection"],
    "POPIA": ["Protection of Personal Information Act"],
    "NDPR": ["Nigeria Data Protection Regulation"],
    "NDPA": ["Nigeria Data Protection Act"],
    "LGPD": ["Lei Geral de Proteção de Dados"],
    "DIFC": ["Dubai International Financial Centre"],
    "DPL": ["Data Protection Law"],
    "DPA": ["Data Protection Act", "Data Protection Authority"],
    "PIPL": ["Personal Information Protection Law"],
    "PIPA": ["Personal Information Protection Act"],
    "APPI": ["Act on the Protection of Personal Information"],
    "LFPDPPP": ["Ley Federal de Protección de Datos Personales en Posesión de los Particulares"],
    "EDPB": ["European Data Protection Board"],
    "CNIL": ["Commission nationale de l'informatique et des libertés"],
    "BSI": ["Bundesamt für Sicherheit in der Informationstechnik"],
    "RBI": ["Reserve Bank of India"],
    "BFSI": ["Banking, Financial Services, and Insurance"],
    "ISMS-P": ["Information Security Management System – Personal"],
    "MLPS": ["Multi-Level Protection Scheme"],
    "HIPAA": ["Health Insurance Portability and Accountability Act"],
    "FERPA": ["Family Educational Rights and Privacy Act"],
    "GLBA": ["Gramm-Leach-Bliley Act"],
    "CCPA": ["California Consumer Privacy Act"],
    "CPRA": ["California Privacy Rights Act"],
    "PIPEDA": ["Personal Information Protection and Electronic Documents Act"],
    "ITAR": ["International Traffic in Arms Regulations"],
    "FedRAMP": ["Federal Risk and Authorization Management Program"],
    "CMMC": ["Cybersecurity Maturity Model Certification"],
    "ECOWAS": ["Economic Community of West African States"],
    "PDPA": ["Personal Data Protection Act"],
    "PDPL": ["Personal Data Protection Law"],
    "BAA": ["Business Associate Agreement"],
    # Geographic
    "GCC": ["Gulf Cooperation Council"],
    "CIS": ["Commonwealth of Independent States"],
    "APAC": ["Asia-Pacific"],
    "LATAM": ["Latin America"],
    "EEA": ["European Economic Area"],
    # Technical
    "CRDT": ["Conflict-free Replicated Data Type"],
    "CRDTs": ["Conflict-free Replicated Data Types"],
    "MDM": ["Mobile Device Management"],
    "SBOM": ["Software Bill of Materials"],
    "RBAC": ["Role-Based Access Control"],
    "DEK": ["Data Encryption Key"],
    "KEK": ["Key Encryption Key"],
    "HKDF": ["HMAC-based Key Derivation Function"],
    "HSM": ["Hardware Security Module"],
    "MFA": ["Multi-Factor Authentication"],
    "SSO": ["Single Sign-On"],
    "IdP": ["Identity Provider"],
    "CMK": ["Customer-Managed Key"],
    "BYOC": ["Bring Your Own Cloud"],
    "TPM": ["Trusted Platform Module"],
    "CBOR": ["Concise Binary Object Representation"],
    "DAG": ["Directed Acyclic Graph"],
    "RFC": ["Request for Comments"],
    "IETF": ["Internet Engineering Task Force"],
    "API": ["Application Programming Interface"],
    "TLS": ["Transport Layer Security"],
    "TCP": ["Transmission Control Protocol"],
    "WAL": ["Write-Ahead Log"],
    "ADR": ["Architecture Decision Record"],
    "FFI": ["Foreign Function Interface"],
    "SLA": ["Service Level Agreement"],
    "SLO": ["Service Level Objective"],
    # Roles / org
    "CISO": ["Chief Information Security Officer"],
    "CTO": ["Chief Technology Officer"],
    "ISV": ["Independent Software Vendor"],
    "SIer": ["Systems Integrator"],
    "SaaS": ["Software as a Service"],
    "UI": ["User Interface"],
    "UX": ["User Experience"],
    "IT": ["Information Technology"],
    "ICP": ["Internet Content Provider"],
    "OS": ["Operating System"],
    "ARCO": ["Access, Rectification, Cancellation, and Opposition"],
    "SCC": ["Standard Contractual Clauses"],
    "SCCs": ["Standard Contractual Clauses"],
    "BCR": ["Binding Corporate Rules"],
    "BCRs": ["Binding Corporate Rules"],
    "MAUI": [".NET Multi-platform App UI"],
    "ICM": ["Inverted Stack Chapter Methodology"],
}

# Products with brief identifiers to look for as evidence of definition.
# A first use is "defined" if any identifier substring appears within ~120
# chars of the first occurrence.
PRODUCTS: dict[str, list[str]] = {
    "Linear": ["linear.app", "issue tracker", "the issue", "sync engine"],
    "Figma": ["figma.com", "design tool", "design platform", "collaborative design"],
    "Sunfish": ["github.com/ctwoodwa/Sunfish", "reference implementation"],
    "YDotNet": [".NET", "Yjs", "Rust", "FFI"],
    "Loro": ["github.com/loro-dev", "loro-cs", "Rust core", "CRDT library"],
    "Yjs": ["github.com/yjs", "JavaScript", "K. Jahns"],
    "Automerge": ["github.com/automerge", "JSON-like"],
    "Pandoc": ["pandoc", "document converter", "LaTeX"],
    "Kokoro": ["TTS", "text-to-speech", "speech synthesis"],
    "Intune": ["Microsoft", "MDM", "Mobile Device Management"],
    "Jamf": ["Apple", "macOS", "MDM"],
    "MaaS360": ["IBM", "MDM"],
    "Ivanti": ["MDM", "Mobile Device Management"],
    "MinIO": ["S3", "object storage", "self-hosted"],
    "Sigstore": ["signing", "supply-chain", "attestation"],
    "Aspire": [".NET", "orchestration"],
    "Anchor": ["Zone A", "local-first desktop", "MAUI"],
    "Bridge": ["Zone C", "hybrid SaaS", "multi-tenant"],
}

# Pre-flight: quick sanity check that ACRONYMS spell-outs and PRODUCTS
# identifiers do not contain regex metacharacters that would break the
# substring match. (None do as written; this is a guardrail.)


def strip_non_prose(text: str) -> str:
    """Remove fenced code, inline code, HTML comments, and IEEE-style
    references at the end of a file (the [N] reference list itself is
    authoritative; we want to check prose, not the references)."""
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    # Strip the trailing References section, if present
    text = re.split(r"\n##\s+References\s*\n", text, maxsplit=1, flags=re.IGNORECASE)[0]
    return text


def find_first_occurrence(prose: str, term: str) -> int | None:
    """Return the character index of the first standalone occurrence of
    `term` in prose, or None if absent. Uses word-boundary regex so
    'API' does not match 'rapid' or 'OAPI'."""
    pattern = r"\b" + re.escape(term) + r"\b"
    m = re.search(pattern, prose)
    return m.start() if m else None


def is_defined_at(prose: str, idx: int, term: str, evidence: list[str], window: int = 120) -> bool:
    """Check whether `prose[idx:idx+len(term)]` appears in a context that
    defines it. The defining evidence (spell-out, identifier, link) must
    appear within `window` chars before or after the term."""
    start = max(0, idx - window)
    end = min(len(prose), idx + len(term) + window)
    context = prose[start:end]
    for ev in evidence:
        if ev.lower() in context.lower():
            return True
    return False


def chapter_key(filename: str) -> str:
    m = re.search(r"(ch\d+|appendix-[a-z]|preface|epilogue|foreword)", filename)
    return m.group(1) if m else filename


def scan_chapter(path: Path) -> list[tuple[str, int]]:
    """Return list of (term, char_idx) for each undefined first occurrence
    in the chapter at `path`."""
    text = path.read_text(encoding="utf-8")
    prose = strip_non_prose(text)
    violations: list[tuple[str, int]] = []
    for term, spell_outs in ACRONYMS.items():
        idx = find_first_occurrence(prose, term)
        if idx is None:
            continue
        if not is_defined_at(prose, idx, term, spell_outs):
            violations.append((term, idx))
    for product, identifiers in PRODUCTS.items():
        idx = find_first_occurrence(prose, product)
        if idx is None:
            continue
        if not is_defined_at(prose, idx, product, identifiers):
            violations.append((product, idx))
    return violations


def context_snippet(path: Path, char_idx: int, span: int = 40) -> str:
    """Return a short snippet of prose around char_idx for diagnostic display."""
    text = path.read_text(encoding="utf-8")
    prose = strip_non_prose(text)
    start = max(0, char_idx - span)
    end = min(len(prose), char_idx + span)
    snippet = prose[start:end].replace("\n", " ")
    return f"...{snippet}..."


SKIP_CHAPTERS = {
    "appendix-e-citation-style.md",      # citation-format examples reference acronyms
    "appendix-f-regulatory-coverage.md",  # regulatory reference table
    "foreword-placeholder.md",            # not real content
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counts", action="store_true", help="just per-chapter violation counts")
    ap.add_argument("--term", help="filter to one specific term")
    args = ap.parse_args()

    all_violations: dict[str, list[tuple[str, int]]] = {}
    for path in sorted(CHAPTERS.glob("**/*.md")):
        if "_voice-drafts" in path.parts:
            continue
        if path.name in SKIP_CHAPTERS:
            continue
        if path.name.endswith(".manifest.json"):
            continue
        violations = scan_chapter(path)
        if args.term:
            violations = [v for v in violations if v[0].lower() == args.term.lower()]
        if violations:
            all_violations[str(path.relative_to(REPO))] = violations

    if args.counts:
        total = sum(len(v) for v in all_violations.values())
        for path, vs in sorted(all_violations.items()):
            print(f"  {len(vs):>3}  {path}")
        print(f"  ---  ---")
        print(f"  {total:>3}  TOTAL")
        return 0 if total == 0 else 1

    total = 0
    for path, violations in sorted(all_violations.items()):
        print(f"\n{path}:")
        for term, idx in violations:
            ctx = context_snippet(Path(REPO / path), idx)
            print(f"  {term:<10}  {ctx}")
            total += 1

    print(f"\nTOTAL: {total} undefined first-use occurrences across {len(all_violations)} files.")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
