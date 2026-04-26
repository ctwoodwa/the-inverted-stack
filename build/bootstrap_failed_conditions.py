"""Bootstrap failed-conditions field across all 562 concepts.

Heuristic: for each `must-implement` item, derive a "this is not enforced"
failed-condition. Plus add a verification-not-passing failed-condition where
verification field exists.

Output is bootstrap-quality — each concept gets failed-conditions that are
mechanical negations of must-implement. A subagent enhancement pass can later
refine to add more nuanced failed-conditions (e.g., partial-implementation
detection, edge cases, common pitfall patterns).

Reads:  docs/reference-implementation/_per-chapter/*.yaml
Writes: same files, in place, with failed-conditions added per concept.

Skip rule: concepts with `must-implement: []` (purely conceptual / philosophical
entries) get `failed-conditions: []` — there's nothing to fail against.

Verb-flip patterns:
  "Application reads/writes hit local storage as primary"
    → "Application reads/writes do not hit local storage as primary"
  "Component X exposes Y interface"
    → "Component X does not expose Y interface"
  "Migration scripts are idempotent and replay-safe"
    → "Migration scripts are not idempotent or not replay-safe"
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
PER_CHAPTER_DIR = REPO / "docs" / "reference-implementation" / "_per-chapter"


def negate_must_implement(item) -> str:
    """Heuristically derive a failed-condition from a must-implement item.

    Strategy: insert "fails to" / "does not" / "is not" near the verb to
    convert imperative-positive to declarative-negative. Defensively handles
    both string entries and dict entries (some chapters used structured
    must-implement with sub-fields).
    """
    if isinstance(item, dict):
        # Common structured patterns: {requirement: ..., rationale: ...}
        # Use the requirement / description / what / item field
        for key in ("requirement", "description", "what", "item", "name", "summary"):
            if key in item and isinstance(item[key], str):
                item = item[key]
                break
        else:
            # Fallback: stringify the dict
            item = str(item)
    if not isinstance(item, str):
        item = str(item)
    s = item.strip()
    if not s:
        return ""

    # Common verb patterns
    patterns = [
        # "X is/are Y" → "X is/are not Y"
        (r"\b(is|are|has|have)\b(?! not\b)", r"\1 not"),
        # "X must Y" → "X does not Y"
        (r"\b(must)\b", "does not"),
        # "X should Y" → "X does not Y"
        (r"\b(should)\b", "does not"),
        # "X can Y" → "X cannot Y"
        (r"\b(can)\b(?! not\b)", "cannot"),
        # "X exposes/provides/supports/implements/exists/maintains/derives"
        # → "X does not expose/provide/..."
        (r"\b(exposes|provides|supports|implements|exists|maintains|derives|"
         r"validates|verifies|enforces|requires|signs|encrypts|stores|preserves|"
         r"propagates|emits|carries|tracks|surfaces|publishes|prevents|allows|"
         r"applies|persists|generates|accepts|rejects|guarantees|ensures|"
         r"records|reports|audits|attests|rotates|revokes|grants|retains|"
         r"declares|imports|exports|migrates|converges|completes|handles|"
         r"executes|operates|tolerates|recovers|detects|responds|monitors|"
         r"replays|caches|aggregates|negotiates|coordinates|isolates|escalates|"
         r"includes|covers|spans|maps|matches|forwards|routes|deduplicates|"
         r"buffers|batches|fragments|reassembles|preserves)\b",
         r"does not \1"),
    ]

    out = s
    for pat, repl in patterns:
        # Apply only the first matching pattern to avoid double-negation
        new = re.sub(pat, repl, out, count=1, flags=re.IGNORECASE)
        if new != out:
            # Fix up "does not exposes" → "does not expose" (third-person → bare verb)
            new = re.sub(r"does not (\w+?)s\b", r"does not \1", new)
            new = re.sub(r"does not (\w+?)es\b", lambda m: f"does not {m.group(1)}",
                         new)
            return new.strip()

    # Fallback: prepend "fails to satisfy: "
    return f"Fails to satisfy: {s}"


def derive_failed_conditions(concept: dict) -> list[str]:
    """Bootstrap failed-conditions list from must-implement + verification."""
    must = concept.get("must-implement", []) or []
    verification = concept.get("verification")

    # Purely conceptual (no must-implement) → no failed-conditions
    if not must:
        return []

    out: list[str] = []
    for item in must:
        negated = negate_must_implement(item)
        if negated and negated not in out:
            out.append(negated)

    # Add a verification-not-passing condition if verification exists
    if verification:
        verification_failed = (
            f"Verification check does not pass: {verification[:120]}"
            + ("..." if len(verification) > 120 else "")
        )
        if verification_failed not in out:
            out.append(verification_failed)

    return out


def process_chapter(path: Path) -> tuple[int, int, int]:
    """Apply failed-conditions to one chapter file. Returns (concepts,
    concepts-with-failed-conditions, purely-conceptual)."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    concepts = data.get("concepts", []) or []

    with_conditions = 0
    purely_conceptual = 0
    for c in concepts:
        conditions = derive_failed_conditions(c)
        if conditions:
            c["failed-conditions"] = conditions
            with_conditions += 1
        else:
            # Purely conceptual entries get explicit empty list
            c["failed-conditions"] = []
            purely_conceptual += 1

    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )
    return len(concepts), with_conditions, purely_conceptual


def main() -> int:
    files = sorted(PER_CHAPTER_DIR.glob("*.yaml"))
    if not files:
        print(f"ERROR: no per-chapter files found in {PER_CHAPTER_DIR}",
              file=sys.stderr)
        return 2

    total_concepts = 0
    total_with = 0
    total_conceptual = 0
    print(f"Bootstrapping failed-conditions across {len(files)} chapter files...")
    print()
    for path in files:
        n, w, c = process_chapter(path)
        total_concepts += n
        total_with += w
        total_conceptual += c
        print(f"  {path.stem:50s}  {n:3d} concepts | "
              f"with-conditions: {w:3d} | purely-conceptual: {c:3d}")

    print()
    print(f"Total: {total_concepts} concepts; "
          f"{total_with} have failed-conditions; "
          f"{total_conceptual} are purely conceptual ([])")
    print()
    print("These are BOOTSTRAP-QUALITY failed-conditions (mechanical negation of")
    print("must-implement). Subagent enhancement pass can refine to add more")
    print("nuanced failure modes (partial-impl detection, edge cases, common")
    print("pitfall patterns). Track as follow-up in book-extension-candidates.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
