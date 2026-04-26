"""Apply v1.1 schema fields (security-axis, applies-to-roles) to per-chapter
concept YAMLs via heuristics.

Reads:  docs/reference-implementation/_per-chapter/*.yaml
Writes: same files, in place, with security-axis and applies-to-roles added.

Heuristic rules:

security-axis:
  - KEY-* prefix → [confidentiality, authenticity] (keys both encrypt + sign)
  - Concept name contains "encrypt" / "encryption" / "ciphertext" / "decrypt"
    → [confidentiality]
  - Concept name contains "signature" / "sign" / "attest" / "auth" / "verify"
    → [authenticity]
  - Concept name contains "handshake" / "noise" / "tls" / "envelope"
    → [confidentiality, authenticity]
  - Concept name contains "key" (but not via KEY- prefix, e.g., "key rotation"
    in a security context) → [confidentiality, authenticity]
  - Concept name contains "relay" with "ciphertext" or "zero-knowledge"
    → [confidentiality]
  - Otherwise → [] (not security-related; will be omitted)

applies-to-roles:
  - UX-* prefix → [full-node, full-node-multi-user]
    (UX concepts don't apply to headless / relay / thin-client / legacy-bridge)
  - Concept name contains "ui" / "user-facing" / "display" / "interface"
    → [full-node, full-node-multi-user]
  - Otherwise → [] (means "all roles", per schema convention)

failed-conditions: NOT applied here — too nuanced for heuristics; dispatched
to subagents in a separate pass.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
PER_CHAPTER_DIR = REPO / "docs" / "reference-implementation" / "_per-chapter"


def derive_security_axis(concept: dict) -> list[str]:
    """Heuristic security-axis assignment based on prefix + name keywords."""
    cid = concept.get("id", "").upper()
    name = concept.get("name", "").lower()
    definition = concept.get("definition", "").lower()

    # KEY-* prefix → both axes (keys serve both encryption and signing)
    if cid.startswith("KEY-"):
        return ["confidentiality", "authenticity"]

    text = f"{name} {definition}"

    # Confidentiality keywords
    confidentiality_kw = ["encrypt", "ciphertext", "decrypt", "zero-knowledge",
                          "private (key|content)", "envelope encryption",
                          "sqlcipher", "at-rest"]
    has_confidentiality = any(kw in text for kw in confidentiality_kw)

    # Authenticity keywords
    authenticity_kw = ["signature", "signed", "signing", "attest", "ed25519",
                       "verify", "non-repudiation", "tamper-evident",
                       "tamper-evidence", "replay", "sequence number",
                       "monotonic"]
    has_authenticity = any(kw in text for kw in authenticity_kw)

    # Both (handshake/Noise/TLS-style)
    both_kw = ["handshake", "noise_xx", "noise xx", "tls", "mtls",
               "session establishment", "key exchange"]
    if any(kw in text for kw in both_kw):
        return ["confidentiality", "authenticity"]

    axes = []
    if has_confidentiality:
        axes.append("confidentiality")
    if has_authenticity:
        axes.append("authenticity")
    return axes


def derive_applies_to_roles(concept: dict) -> list[str]:
    """Heuristic applies-to-roles assignment based on prefix + name keywords."""
    cid = concept.get("id", "").upper()
    name = concept.get("name", "").lower()
    definition = concept.get("definition", "").lower()

    text = f"{name} {definition}"

    # UX-* prefix → only full-node + full-node-multi-user (no headless / relay /
    # thin-client / legacy-bridge — no human at device)
    if cid.startswith("UX-"):
        return ["full-node", "full-node-multi-user"]

    # UI-related concepts in non-UX chapters
    ui_kw = ["user interface", "ui block", "ui tier", "user-facing display",
             "human readable", "screen reader", "accessibility", "wcag",
             "first-run", "onboarding ui", "conflict ui"]
    if any(kw in text for kw in ui_kw):
        return ["full-node", "full-node-multi-user"]

    # Default: empty list = applies to all roles (schema convention)
    return []


def process_chapter(path: Path) -> tuple[int, int, int]:
    """Apply v1.1 tags to one chapter file. Returns (concepts, security-tagged,
    role-tagged) counts."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    concepts = data.get("concepts", []) or []

    security_tagged = 0
    role_tagged = 0
    for c in concepts:
        axis = derive_security_axis(c)
        roles = derive_applies_to_roles(c)
        if axis:
            c["security-axis"] = axis
            security_tagged += 1
        if roles:
            c["applies-to-roles"] = roles
            role_tagged += 1

    # Re-serialize
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )
    return len(concepts), security_tagged, role_tagged


def main() -> int:
    files = sorted(PER_CHAPTER_DIR.glob("*.yaml"))
    if not files:
        print(f"ERROR: no per-chapter files found in {PER_CHAPTER_DIR}",
              file=sys.stderr)
        return 2

    total_concepts = 0
    total_security = 0
    total_roles = 0
    print(f"Tagging v1.1 fields across {len(files)} chapter files...")
    print()
    for path in files:
        n, s, r = process_chapter(path)
        total_concepts += n
        total_security += s
        total_roles += r
        if s or r:
            print(f"  {path.stem:50s}  {n:3d} concepts | "
                  f"security-axis: {s:2d} | applies-to-roles: {r:2d}")

    print()
    print(f"Total: {total_concepts} concepts; "
          f"{total_security} tagged with security-axis; "
          f"{total_roles} tagged with applies-to-roles")
    print()
    print("Note: failed-conditions NOT applied here — dispatched to subagents.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
