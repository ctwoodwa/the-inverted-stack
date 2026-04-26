"""Generate the human-readable implementation-specification.md from the
consolidated concept-index.yaml.

Structure:
  Part 0: Front matter (preface)
  Part I: Thesis (ch01-ch04) — Epic per chapter
  Part II: Council perspectives (ch05-ch10) — Epic per chapter
  Part III: Reference architecture (ch11-ch16) — Epic per chapter (THE SPEC)
  Part IV: Implementation playbooks (ch17-ch20) — Epic per chapter
  Part V: Epilogue + Appendices

Each chapter epic contains:
  - Header: chapter title, source paper refs, concept count
  - One section per concept: name, definition, must-implement bullets,
    verification, kleppmann-properties tag, scope tag, failure-modes tag

Each concept entry uses the canonical reference `chapter:id` (e.g.
`ch15-security-architecture:SEC-01`) so downstream skills and scorecards can
link back unambiguously.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
INDEX_IN = REPO / "docs" / "reference-implementation" / "concept-index.yaml"
SPEC_OUT = REPO / "docs" / "reference-implementation" / "implementation-specification.md"

PARTS = [
    ("Part 0 — Front matter", ["preface"]),
    ("Part I — Thesis and pain", [
        "ch01-when-saas-fights-reality",
        "ch02-local-first-serious-stack",
        "ch03-inverted-stack-one-diagram",
        "ch04-choosing-your-architecture",
    ]),
    ("Part II — Council perspectives", [
        "ch05-enterprise-lens",
        "ch06-distributed-systems-lens",
        "ch07-security-lens",
        "ch08-product-economic-lens",
        "ch09-local-first-practitioner-lens",
        "ch10-synthesis",
    ]),
    ("Part III — Reference architecture (the specification)", [
        "ch11-node-architecture",
        "ch12-crdt-engine-data-layer",
        "ch13-schema-migration-evolution",
        "ch14-sync-daemon-protocol",
        "ch15-security-architecture",
        "ch16-persistence-beyond-the-node",
    ]),
    ("Part IV — Implementation playbooks", [
        "ch17-building-first-node",
        "ch18-migrating-existing-saas",
        "ch19-shipping-to-enterprise",
        "ch20-ux-sync-conflict",
    ]),
    ("Part V — Epilogue and appendices", [
        "epilogue-what-the-stack-owes-you",
        "appendix-a-sync-daemon-wire-protocol",
        "appendix-b-threat-model-worksheets",
        "appendix-c-further-reading",
        "appendix-d-testing-the-inverted-stack",
        "appendix-e-citation-style",
        "appendix-f-regulatory-coverage",
    ]),
]


def fmt_property_tag(props: list[str]) -> str:
    if not props:
        return "—"
    return ", ".join(sorted(props))


def fmt_failure_modes(modes: list[str]) -> str:
    if not modes:
        return ""
    return f"**Failure modes addressed:** {', '.join(sorted(modes))}\n\n"


def render_concept(c: dict) -> str:
    ref = f"{c['chapter']}:{c['id']}"
    name = c["name"]
    definition = c["definition"]
    must = c.get("must-implement", []) or []
    verification = c.get("verification")
    props = c.get("kleppmann-properties", []) or []
    scope = c.get("scope", "unknown")
    failure_modes = c.get("failure-modes", []) or []
    notes = c.get("notes")

    out = []
    out.append(f"#### `{ref}` — {name}")
    out.append("")
    out.append(definition)
    out.append("")

    badges = []
    if props:
        badges.append(f"**Kleppmann:** `{fmt_property_tag(props)}`")
    badges.append(f"**Scope:** `{scope}`")
    if failure_modes:
        badges.append(f"**Failure modes:** `{', '.join(sorted(failure_modes))}`")
    out.append(" · ".join(badges))
    out.append("")

    if must:
        out.append("**Must implement:**")
        out.append("")
        for item in must:
            out.append(f"- {item}")
        out.append("")
    else:
        out.append("*Conceptual / philosophical — no direct implementation requirement.*")
        out.append("")

    if verification:
        out.append(f"**Verification:** {verification}")
        out.append("")

    if notes:
        out.append(f"> {notes}")
        out.append("")

    return "\n".join(out)


def render_chapter(stem: str, concepts_by_chapter: dict[str, list[dict]],
                   chapters_meta: dict[str, dict]) -> str:
    meta = chapters_meta.get(stem, {})
    title = meta.get("title", stem)
    paper_refs = meta.get("source-paper-refs", []) or []
    concepts = concepts_by_chapter.get(stem, [])

    out = []
    out.append(f"### Epic: {title} ({stem})")
    out.append("")
    if paper_refs:
        out.append(f"**Source-paper refs:** {', '.join(paper_refs)}")
        out.append("")
    out.append(f"**Concept count:** {len(concepts)}")
    out.append("")

    if not concepts:
        out.append("*No concepts extracted from this chapter.*")
        out.append("")
        return "\n".join(out)

    for c in concepts:
        out.append(render_concept(c))

    return "\n".join(out)


def main() -> int:
    data = yaml.safe_load(INDEX_IN.read_text(encoding="utf-8"))
    metadata = data["metadata"]
    concepts = data["concepts"]

    # Group concepts by chapter
    by_chapter: dict[str, list[dict]] = defaultdict(list)
    for c in concepts:
        by_chapter[c["chapter"]].append(c)

    chapters_meta = {ch["stem"]: ch for ch in metadata["chapters"]}

    out = []
    out.append("# Implementation Specification — The Inverted Stack")
    out.append("")
    out.append(f"**Generated** from `concept-index.yaml` schema v{metadata['schema-version']}.")
    out.append(f"  **Total concepts:** {metadata['total-concepts']} across {metadata['total-chapters']} chapters.")
    out.append(f"  **Foundational:** {metadata['scope-coverage'].get('foundational', 0)} (any local-first repo).")
    out.append(f"  **Inverted-Stack-specific:** {metadata['scope-coverage'].get('inverted-stack-specific', 0)} (this book's specific architecture).")
    out.append("")
    out.append("## How to read this spec")
    out.append("")
    out.append("This document is the human-readable view of `concept-index.yaml`. Each *concept* is a discrete architectural commitment the book makes. Concepts group into *chapter epics*, which group into *parts* matching the book structure.")
    out.append("")
    out.append("Each concept entry shows:")
    out.append("- **Canonical reference**: `<chapter-stem>:<local-id>` — the stable ID downstream skills and scorecards use.")
    out.append("- **Definition**: one sentence stating what the concept IS.")
    out.append("- **Kleppmann tag**: which of the seven properties (P1–P7) the concept serves. `—` if it serves no Kleppmann property directly (e.g., a build-tooling or business-model concept).")
    out.append("- **Scope tag**: `foundational` (applies to any local-first repo) or `inverted-stack-specific` (requires this book's architectural choices).")
    out.append("- **Failure modes**: named failure modes the concept addresses, where applicable.")
    out.append("- **Must implement**: imperative requirements an implementation must satisfy to claim coverage. Empty for purely philosophical concepts.")
    out.append("- **Verification**: the specific check (file/namespace presence, behavioral test, integration scenario).")
    out.append("")
    out.append("## Two consumer audiences")
    out.append("")
    out.append("1. **Generic local-first repos** (Loro-, Yjs-, Automerge-, custom-engine implementations) score themselves against the `foundational`-scoped concepts grouped by Kleppmann property — see `concept-index-by-property.yaml` and the future `local-first-properties` Claude skill.")
    out.append("2. **Inverted Stack-aligned repos** (Sunfish's Anchor and Bridge today; future implementations of this book's architecture) score themselves against the FULL concept index — see the future `inverted-stack-conformance` Claude skill.")
    out.append("")
    out.append("**Sunfish-specific glue** (mapping concept IDs to Sunfish package paths, ICM pipeline variants for conformance review) lives in `C:\\Projects\\Sunfish\\icm\\` — not in this repo.")
    out.append("")
    out.append("## Kleppmann property glossary")
    out.append("")
    for p, desc in metadata["kleppmann-property-glossary"].items():
        out.append(f"- **{p}** — {desc}")
    out.append("")
    out.append("## Property coverage summary")
    out.append("")
    out.append("| Property | Concept count |")
    out.append("|---|---|")
    for prop_label, count in metadata["property-coverage"].items():
        out.append(f"| {prop_label} | {count} |")
    out.append("")
    out.append("Note: a single concept can serve multiple properties. The sum exceeds the total concept count.")
    out.append("")
    out.append("## Scope coverage summary")
    out.append("")
    out.append("| Scope | Concept count |")
    out.append("|---|---|")
    for scope, count in metadata["scope-coverage"].items():
        out.append(f"| `{scope}` | {count} |")
    out.append("")
    out.append("## Synthesis relationships")
    out.append("")
    out.append("Several chapters synthesize or reference concepts from other chapters. Downstream consumers (skills, scorecards) should be aware of these relationships when computing coverage:")
    out.append("")
    for rel in metadata.get("synthesis-relationships", []) or []:
        out.append(f"- **{rel['synthesizer']}** ← {', '.join(rel['sources'])}")
        out.append(f"  - {rel['note']}")
    out.append("")
    out.append("## Cross-chapter ID collisions")
    out.append("")
    collisions = metadata.get("cross-chapter-id-collisions") or {}
    if collisions:
        out.append(f"The following local IDs appear in more than one chapter. The canonical reference `chapter:id` disambiguates them.")
        out.append("")
        out.append("| Local ID | Chapters |")
        out.append("|---|---|")
        for cid, chs in sorted(collisions.items()):
            out.append(f"| `{cid}` | {', '.join(chs)} |")
        out.append("")
    else:
        out.append("None.")
        out.append("")

    out.append("---")
    out.append("")
    out.append("# The catalog")
    out.append("")

    for part_title, part_chapters in PARTS:
        out.append(f"## {part_title}")
        out.append("")
        for stem in part_chapters:
            out.append(render_chapter(stem, by_chapter, chapters_meta))
            out.append("")
        out.append("---")
        out.append("")

    SPEC_OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {SPEC_OUT.relative_to(REPO).as_posix()} "
          f"({sum(len(by_chapter[c]) for c in by_chapter)} concept entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
