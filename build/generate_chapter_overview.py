"""Generate chapter-overview.md for the inverted-stack-conformance skill.

Reads the bundled references/concept-index.yaml snapshot and emits a compact
per-chapter overview that lets the agent scope its scan without loading the
full 617KB index into context.
"""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
import yaml

REPO = Path(__file__).resolve().parent.parent
INDEX_IN = REPO / ".claude" / "skills" / "inverted-stack-conformance" / "references" / "concept-index.yaml"
OVERVIEW_OUT = REPO / ".claude" / "skills" / "inverted-stack-conformance" / "references" / "chapter-overview.md"


def main() -> int:
    data = yaml.safe_load(INDEX_IN.read_text(encoding="utf-8"))
    metadata = data["metadata"]
    concepts = data["concepts"]

    by_chapter = defaultdict(list)
    for c in concepts:
        by_chapter[c["chapter"]].append(c)

    out = []
    out.append("# Chapter Overview — Inverted Stack Conformance Catalog")
    out.append("")
    out.append("Compact navigation index. Use this to scope which chapters to load from `concept-index.yaml`.")
    out.append("")
    out.append(f"**Total concepts:** {metadata['total-concepts']} across {metadata['total-chapters']} chapters")
    out.append(f"**Foundational:** {metadata['scope-coverage'].get('foundational', 0)} · "
               f"**Inverted-stack-specific:** {metadata['scope-coverage'].get('inverted-stack-specific', 0)}")
    out.append("")

    for ch_meta in metadata["chapters"]:
        stem = ch_meta["stem"]
        title = ch_meta.get("title", stem)
        count = ch_meta.get("concept-count", 0)
        if count == 0:
            continue

        ch_concepts = by_chapter.get(stem, [])
        scope_split = defaultdict(int)
        prop_set = set()
        prefixes = set()
        for c in ch_concepts:
            scope_split[c.get("scope", "unknown")] += 1
            for p in c.get("kleppmann-properties", []) or []:
                prop_set.add(p)
            local_id = c.get("id", "")
            prefix = local_id.split("-")[0] if "-" in local_id else local_id
            prefixes.add(prefix)

        out.append(f"## `{stem}` — {title}")
        out.append("")
        out.append(f"- **Concept count:** {count}")
        out.append(f"- **Scope:** foundational={scope_split.get('foundational', 0)}, "
                   f"inverted-stack-specific={scope_split.get('inverted-stack-specific', 0)}")
        out.append(f"- **Kleppmann properties touched:** {', '.join(sorted(prop_set)) if prop_set else '—'}")
        out.append(f"- **ID prefixes:** `{', '.join(sorted(prefixes))}`")

        # Show first 5 concept names as theme indicators
        sample = [c["name"] for c in ch_concepts[:5]]
        if sample:
            out.append(f"- **Sample concepts:** {'; '.join(sample[:5])}")
        out.append("")

    OVERVIEW_OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OVERVIEW_OUT.relative_to(REPO).as_posix()}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
