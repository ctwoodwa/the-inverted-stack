# Reference Implementation Specification

This directory contains the machine-readable concept index extracted from *The Inverted Stack* and the human-readable implementation specification derived from it. Together they let any local-first repository — Sunfish's Anchor and Bridge accelerators today; other implementations tomorrow — measure conformance to the book.

## Files

| File | Audience | Purpose |
|---|---|---|
| `SCHEMA.md` | Subagent extractors; consolidator | Defines the YAML schema for `concept-index.yaml` and per-chapter files |
| `concept-index.yaml` | Skills, scorecards, conformance pipelines | Canonical concept catalog (~150-300 entries), tagged with Kleppmann properties + scope |
| `implementation-specification.md` | Authors verifying coverage; implementers building from the book | Human-readable epic/story/task hierarchy organized by chapter |
| `_per-chapter/<chapter-stem>.yaml` | Workflow artifact | Per-chapter extractions before consolidation; gitignored after merge |

## Two consumer audiences

The `concept-index.yaml` is designed to feed two distinct downstream workflows:

### 1. Generic local-first verification (any repo)

A `local-first-properties` Claude skill (built in a follow-up session under `.claude/skills/`) groups the index by `kleppmann-properties` and runs verification checks against any repo claiming to be local-first. It uses ONLY entries with `scope: foundational` so the check is portable across CRDT engine choices (Loro, Yjs, Automerge, custom).

### 2. Inverted Stack-specific conformance (any repo claiming to follow this book)

A `inverted-stack-conformance` Claude skill uses the FULL index (both `foundational` and `inverted-stack-specific` scopes) to verify a repo implements this book's architectural choices — Zone A/B/C, Flease quorum participation, the specific sync daemon protocol from Appendix A, the Bridge hybrid pattern, etc.

### Sunfish-specific glue (lives in the Sunfish repo)

`C:\Projects\Sunfish\icm\pipelines\sunfish-local-first-conformance/` and `sunfish-inverted-stack-conformance/` are pipeline variants that wrap both skills, scope them to the Sunfish package layout, and integrate findings into Sunfish's existing 9-stage ICM workflow. The Sunfish-side `icm/_config/conformance-map.md` maps concept IDs to the Sunfish packages where they should live.

## Build process

1. **Extraction** (parallel subagents) — One subagent per chapter, outputs `_per-chapter/<chapter-stem>.yaml` following `SCHEMA.md`.
2. **Consolidation** — Merge per-chapter files into `concept-index.yaml` with stable global IDs, dedupe overlapping concepts (e.g., a CRDT garbage collection concept might appear in both ch12 and ch16).
3. **Specification authoring** — Write `implementation-specification.md` as the human-readable hierarchy, every task linking back to its concept-index ID.

The per-chapter files under `_per-chapter/` are workflow artifacts. Once `concept-index.yaml` is consolidated, the per-chapter files can be regenerated from chapters anytime; they are tracked in git for diff visibility but consolidation is the canonical view.
