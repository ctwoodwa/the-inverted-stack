"""Consolidate per-chapter YAML extractions into the master concept-index.yaml.

Reads:
- docs/reference-implementation/_per-chapter/*.yaml

Writes:
- docs/reference-implementation/concept-index.yaml  (chapter-ordered master)
- docs/reference-implementation/concept-index-by-property.yaml  (P1-P7 grouped)

Each concept in the master file gets:
- All original fields from the per-chapter extraction
- An added `chapter` field naming the source chapter stem
- Its `id` field preserved (per-chapter local ID, e.g. "SEC-01")

The canonical reference for a concept across the book is `chapter:id` (e.g.
`ch15-security-architecture:SEC-01`). Local IDs are unique within a chapter
by construction; the chapter prefix disambiguates the rare cross-chapter
collisions (THESIS-* used by both ch01 and ch02; SEC-* used by both ch15 and
appendix-b; COMP-* used by both appendix-b and appendix-f).
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
PER_CHAPTER_DIR = REPO / "docs" / "reference-implementation" / "_per-chapter"
MASTER_OUT = REPO / "docs" / "reference-implementation" / "concept-index.yaml"
PROPERTY_OUT = REPO / "docs" / "reference-implementation" / "concept-index-by-property.yaml"

# Canonical chapter ordering (matches book-structure.md / Pandoc EPUB build)
CHAPTER_ORDER = [
    "preface",
    "ch01-when-saas-fights-reality",
    "ch02-local-first-serious-stack",
    "ch03-inverted-stack-one-diagram",
    "ch04-choosing-your-architecture",
    "ch05-enterprise-lens",
    "ch06-distributed-systems-lens",
    "ch07-security-lens",
    "ch08-product-economic-lens",
    "ch09-local-first-practitioner-lens",
    "ch10-synthesis",
    "ch11-node-architecture",
    "ch12-crdt-engine-data-layer",
    "ch13-schema-migration-evolution",
    "ch14-sync-daemon-protocol",
    "ch15-security-architecture",
    "ch16-persistence-beyond-the-node",
    "ch17-building-first-node",
    "ch18-migrating-existing-saas",
    "ch19-shipping-to-enterprise",
    "ch20-ux-sync-conflict",
    "epilogue-what-the-stack-owes-you",
    "appendix-a-sync-daemon-wire-protocol",
    "appendix-b-threat-model-worksheets",
    "appendix-c-further-reading",
    "appendix-d-testing-the-inverted-stack",
    "appendix-e-citation-style",
    "appendix-f-regulatory-coverage",
]

KLEPPMANN_PROPERTIES = {
    "P1": "No spinners — fast, work happens locally",
    "P2": "Your work is not trapped on one device",
    "P3": "The network is optional",
    "P4": "Seamless collaboration with colleagues",
    "P5": "The Long Now — data outlives vendor and subscription",
    "P6": "Security and privacy by default",
    "P7": "You retain ultimate ownership and control",
}


def load_chapter(stem: str) -> dict | None:
    path = PER_CHAPTER_DIR / f"{stem}.yaml"
    if not path.exists():
        print(f"WARN: missing per-chapter file: {path}", file=sys.stderr)
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    all_concepts: list[dict] = []
    chapters_meta: list[dict] = []

    # Track id collisions across chapters
    id_to_chapters: dict[str, list[str]] = defaultdict(list)

    for stem in CHAPTER_ORDER:
        data = load_chapter(stem)
        if not data:
            continue
        chapter_concepts = data.get("concepts", []) or []
        chapters_meta.append({
            "stem": stem,
            "title": data.get("chapter-title"),
            "source-paper-refs": data.get("source-paper-refs", []),
            "concept-count": len(chapter_concepts),
        })
        for c in chapter_concepts:
            # Preserve original fields, add chapter
            entry = {"chapter": stem, **c}
            all_concepts.append(entry)
            id_to_chapters[c["id"]].append(stem)

    # Report collisions (kept distinct via chapter prefix)
    collisions = {cid: chs for cid, chs in id_to_chapters.items() if len(chs) > 1}
    if collisions:
        print("Cross-chapter local-ID collisions (resolved via `chapter:id` reference):",
              file=sys.stderr)
        for cid, chs in sorted(collisions.items()):
            print(f"  {cid}: appears in {chs}", file=sys.stderr)

    # Compute summary stats
    by_scope: dict[str, int] = defaultdict(int)
    by_property: dict[str, int] = defaultdict(int)
    by_chapter: dict[str, int] = defaultdict(int)
    for c in all_concepts:
        by_scope[c.get("scope", "unknown")] += 1
        for prop in c.get("kleppmann-properties", []) or []:
            by_property[prop] += 1
        by_chapter[c["chapter"]] += 1

    metadata = {
        "schema-version": "1.0",
        "generated-from": "docs/reference-implementation/_per-chapter/",
        "total-concepts": len(all_concepts),
        "total-chapters": len(chapters_meta),
        "scope-coverage": dict(sorted(by_scope.items())),
        "property-coverage": {
            f"{p}: {KLEPPMANN_PROPERTIES[p]}": by_property[p]
            for p in sorted(KLEPPMANN_PROPERTIES.keys())
        },
        "concepts-per-chapter": {
            ch: by_chapter[ch] for ch in CHAPTER_ORDER if ch in by_chapter
        },
        "cross-chapter-id-collisions": {
            cid: chs for cid, chs in sorted(collisions.items())
        } if collisions else None,
        "synthesis-relationships": [
            {
                "synthesizer": "ch10-synthesis",
                "sources": [
                    "ch05-enterprise-lens",
                    "ch06-distributed-systems-lens",
                    "ch07-security-lens",
                    "ch08-product-economic-lens",
                    "ch09-local-first-practitioner-lens",
                ],
                "note": "Ch10 LENS-* concepts are the survivors of cross-lens review; Ch05-Ch09 LENS-{E,D,S,P,LF}-* concepts are the per-lens sources. Downstream consumers may treat Ch10 entries as canonical and per-lens entries as supporting derivations.",
            },
            {
                "synthesizer": "ch14-sync-daemon-protocol",
                "sources": ["appendix-a-sync-daemon-wire-protocol"],
                "note": "Ch14 SYNC-* concepts describe the daemon at the protocol/architecture level; Appendix A WIRE-* concepts specify the byte-level wire format. Both are normative — Ch14 owns semantics, Appendix A owns format.",
            },
            {
                "synthesizer": "ch15-security-architecture",
                "sources": ["appendix-b-threat-model-worksheets"],
                "note": "Ch15 KEY-*/SEC-* concepts define security primitives and architecture; Appendix B THREAT-*/SEC-*/MITIG-* concepts define threat-model worksheet methodology + named actors + per-actor mitigations. Complementary — Ch15 owns mechanism, Appendix B owns runbook.",
            },
            {
                "synthesizer": "appendix-d-testing-the-inverted-stack",
                "sources": [
                    "ch12-crdt-engine-data-layer",
                    "ch13-schema-migration-evolution",
                    "ch14-sync-daemon-protocol",
                    "ch15-security-architecture",
                ],
                "note": "Appendix D TEST-* concepts operationalize Part III architectural concepts as test patterns. Each TEST-* references one or more body-chapter concepts.",
            },
            {
                "synthesizer": "epilogue-what-the-stack-owes-you",
                "sources": [
                    "ch11-node-architecture",
                    "ch12-crdt-engine-data-layer",
                    "ch14-sync-daemon-protocol",
                    "ch15-security-architecture",
                    "ch16-persistence-beyond-the-node",
                ],
                "note": "Epilogue EPI-* concepts are obligation contracts — each names what a Part III chapter must deliver to qualify as local-first under this book's definition.",
            },
        ],
        "chapters": chapters_meta,
        "kleppmann-property-glossary": {
            p: KLEPPMANN_PROPERTIES[p] for p in sorted(KLEPPMANN_PROPERTIES.keys())
        },
    }

    master = {
        "metadata": metadata,
        "concepts": all_concepts,
    }

    MASTER_OUT.write_text(
        yaml.safe_dump(master, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )
    print(f"Wrote {MASTER_OUT.relative_to(REPO).as_posix()} "
          f"({len(all_concepts)} concepts across {len(chapters_meta)} chapters)")

    # Property-grouped view: only foundational concepts, grouped by P1-P7
    foundational_by_property: dict[str, list[dict]] = defaultdict(list)
    for c in all_concepts:
        if c.get("scope") != "foundational":
            continue
        props = c.get("kleppmann-properties", []) or []
        if not props:
            continue
        for prop in props:
            # Lightweight reference for the property-view
            foundational_by_property[prop].append({
                "ref": f"{c['chapter']}:{c['id']}",
                "name": c["name"],
                "scope": c["scope"],
                "definition": c["definition"],
                "must-implement": c.get("must-implement", []),
                "verification": c.get("verification"),
            })

    property_view = {
        "metadata": {
            "schema-version": "1.0",
            "view": "Foundational concepts grouped by Kleppmann property (P1-P7)",
            "purpose": "Feeds the local-first-properties Claude skill (any local-first repo can be scored against P1-P7 from this subset)",
            "scope-filter": "foundational only — inverted-stack-specific concepts excluded so this view is portable to non-Inverted-Stack local-first implementations",
            "concepts-per-property": {
                p: len(foundational_by_property.get(p, []))
                for p in sorted(KLEPPMANN_PROPERTIES.keys())
            },
        },
        "kleppmann-property-glossary": {
            p: KLEPPMANN_PROPERTIES[p] for p in sorted(KLEPPMANN_PROPERTIES.keys())
        },
        "properties": {
            p: foundational_by_property.get(p, [])
            for p in sorted(KLEPPMANN_PROPERTIES.keys())
        },
    }

    PROPERTY_OUT.write_text(
        yaml.safe_dump(property_view, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )
    foundational_count = sum(len(v) for v in foundational_by_property.values())
    print(f"Wrote {PROPERTY_OUT.relative_to(REPO).as_posix()} "
          f"({foundational_count} foundational property-mapped entries; "
          f"P1-P7 distribution: {dict((p, len(foundational_by_property[p])) for p in sorted(KLEPPMANN_PROPERTIES.keys()))})")

    print()
    print("=== Summary ===")
    print(f"Total concepts: {len(all_concepts)}")
    print(f"Scope: foundational={by_scope['foundational']}, inverted-stack-specific={by_scope['inverted-stack-specific']}")
    print(f"Property coverage:")
    for p in sorted(KLEPPMANN_PROPERTIES.keys()):
        print(f"  {p}: {by_property[p]:3d} concepts")
    print(f"Cross-chapter ID collisions: {len(collisions)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
