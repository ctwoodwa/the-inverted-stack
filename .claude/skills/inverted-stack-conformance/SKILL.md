---
name: inverted-stack-conformance
description: Score any repository claiming alignment with *The Inverted Stack: Local-First Nodes in a SaaS World* against the full 562-concept catalog (foundational + inverted-stack-specific). Use when a repo's contributors say it implements this book's architecture (Zone A/B/C, Flease quorum participation, the specific sync daemon protocol from Appendix A, the Bridge hybrid pattern, KEK/DEK envelope hierarchy, three-tier CRDT resolution model, etc.) and you need a structured per-chapter conformance report. Goes deeper than `local-first-properties` — that skill covers Kleppmann's seven properties using the foundational subset (538 entries); this skill covers the full book including book-specific architectural choices (Sunfish package layout patterns, the WIRE-* protocol message types, the THREAT-* worksheet structure). ICM-aware: writes findings into `icm/01_discovery/output/` if the target repo has Sunfish-style ICM, otherwise `.inverted-stack-conformance/` at repo root. Invoke when the user asks "how much of the book does this repo implement?", "score this repo against The Inverted Stack," "what chapters of the book is this repo missing?", or after cloning a repo that names the book as its reference architecture.
---

# Inverted Stack Conformance — Full-Spec Skill

## Why this skill exists

*The Inverted Stack* makes a specific architectural commitment — not just "be local-first" but a particular shape of local-first software (microkernel + plugins, three-tier CRDT resolution, KEK/DEK envelope keys, signed wire-protocol messages, MDM-attested handshakes, Zone-A/B/C deployment taxonomy, Flease quorum coordination). A repo claiming alignment with the book should be scoreable against THE BOOK — not just against the seven Kleppmann properties.

This skill is the deep complement to `local-first-properties`. Same ICM-aware output structure, but covers the full 562-concept catalog (both `foundational` and `inverted-stack-specific` scopes) and groups the report by **chapter epic** rather than by Kleppmann property.

## When to consult this skill

Use it when:

- A user asks "score this repo against *The Inverted Stack*" or names the book as the target spec.
- The repo's README, ADRs, or docs reference the book by title or use book-specific terminology (Zone A, Zone C, Bridge, Anchor, Flease, ICrdtEngine, three-tier CRDT, etc.).
- A user wants per-chapter coverage (e.g., "how complete is our Ch12 CRDT engine?").
- A user is migrating a generic local-first prototype toward Inverted Stack alignment and wants a roadmap.
- A user wants the deepest possible scorecard before publication, conformance claims, or procurement claims.

Skip it when:

- The repo doesn't claim Inverted Stack alignment (use `local-first-properties` for the generic 7-property check instead — it works on Loro/Yjs/Automerge repos that take different architectural paths).
- The user just wants a quick "is this local-first?" sniff test (use `local-first-properties` quick mode).

## The catalog

The bundled `references/concept-index.yaml` is a snapshot of the consolidated index from *The Inverted Stack* repo. Coverage:

| Part | Chapters | Concept count |
|---|---|---|
| Front matter | preface | 8 |
| Part I — Thesis | ch01-ch04 | 61 |
| Part II — Council | ch05-ch10 | 96 |
| Part III — Reference architecture | ch11-ch16 | 188 |
| Part IV — Playbooks | ch17-ch20 | 95 |
| Epilogue + Appendices | epilogue, appendix-{a-f} | 114 |
| **Total** | **28** | **562** |

Scope split: **298 foundational** (any local-first repo) + **264 inverted-stack-specific** (this book's architectural choices).

The chapter-level overview is in `references/chapter-overview.md` for quick navigation without loading the full 617KB YAML up front.

## How to invoke

### 1. Confirm scope and depth with the user

Before scanning, ask:

> "I'll score `<repo path>` against *The Inverted Stack*'s full 562-concept catalog organized by chapter epic. Three depth options:
> - **Quick** (~20 min): sample 30% of concepts per chapter, flag obvious gaps
> - **Standard** (~60 min): score every concept once, no deep behavioral verification
> - **Deep** (~2 hours): score every concept including behavioral checks where applicable
>
> Also, do you want all 28 chapters scored, or filter to specific parts? (Common filter: just Part III — the spec — for an architecture audit.)"

### 2. Detect output destination

```bash
test -d <repo>/icm && test -f <repo>/icm/CONTEXT.md && echo "ICM-style"
```

- **If ICM-style**: write to `<repo>/icm/01_discovery/output/inverted-stack-conformance-<YYYY-MM-DD>.md`. This integrates with Sunfish-style ICM workflow — the report is a Stage 01 Discovery output, ready to advance into Stage 02 Architecture (remediation design) and onward through the pipeline.
- **Otherwise**: create `<repo>/.inverted-stack-conformance/` and write `report-<YYYY-MM-DD>.md` there.

State the destination before writing.

### 3. Load the catalog efficiently

The full `concept-index.yaml` is large (~617KB). Don't load it all at once — load the metadata header first, then load chapter-by-chapter as you score:

```python
import yaml
with open('references/concept-index.yaml') as f:
    data = yaml.safe_load(f)
metadata = data['metadata']      # summary stats, chapter list, glossary
concepts = data['concepts']       # the full 562-entry list
```

Then group concepts by chapter:

```python
from collections import defaultdict
by_chapter = defaultdict(list)
for c in concepts:
    by_chapter[c['chapter']].append(c)
```

Process one chapter at a time. After each chapter, write its findings to the report incrementally rather than holding all 562 findings in memory.

For really tight context budgets, use `references/chapter-overview.md` to navigate — it lists each chapter's concept count and key themes without the full per-concept data.

### 4. Score per chapter

For each chapter (or each chapter in the user's filter):

1. Read the chapter's concepts from the catalog.
2. For each concept: read `must-implement` requirements and `verification` field, scan the target repo for evidence using Read/Grep/Glob, classify the finding.
3. Tally: `<complete count> / <total>` per chapter.

**Classification rubric (Standard mode default):**

| Status | Criteria |
|---|---|
| `complete` | Evidence found AND it implements the requirement(s) substantively |
| `partial` | Evidence found but incomplete |
| `missing` | No evidence found |
| `not_applicable` | Concept does not apply (justify in notes — e.g., "this repo is Zone A only, Bridge concepts in MIG-* are out of scope") |

**Evidence sources by concept type:**

- **Architecture concepts** (NODE-*, CRDT-*, etc.) → look for namespace/class/package presence
- **Protocol concepts** (SYNC-*, WIRE-*) → look for wire-format implementations and tests
- **Security concepts** (SEC-*, KEY-*) → look for key-derivation code, encryption boundaries, attestation flows
- **UX concepts** (UX-*) → look for UI components, sync-state indicators, conflict-resolution surfaces
- **Test concepts** (TEST-*) → look for the named test patterns in test directories
- **Compliance concepts** (COMP-*) → look for documented compliance procedures, ADRs, regulatory metadata
- **Build/deploy concepts** (BUILD-*, ENT-*) → look for CI/CD configs, signing infrastructure, release processes
- **Lens concepts** (LENS-*) → look for the named requirements in code AND in ADRs/docs
- **Thesis concepts** (THESIS-*, INV-*, PREF-*) → mostly philosophical; score `not_applicable` unless they have explicit must-implement requirements

See `references/verification-recipes.md` (or the sister `local-first-properties/references/verification-recipes.md`) for verification recipes by type.

### 5. Emit the report

Use this exact structure:

```markdown
# Inverted Stack Conformance Report

**Repo:** `<repo path>`
**Scan date:** YYYY-MM-DD
**Catalog:** inverted-stack-conformance skill, full 562-concept index
**Mode:** quick | standard | deep
**Chapter filter:** all | <list>

## Summary

### Overall coverage

| Scope | Score |
|---|---|
| Foundational (298 concepts) | XXX/298 (XX%) |
| Inverted-Stack-specific (264 concepts) | XXX/264 (XX%) |
| **Total** | **XXX/562 (XX%)** |

### Coverage by part

| Part | Concepts | Score |
|---|---|---|
| Front matter | 8 | X/8 (X%) |
| Part I — Thesis | 61 | X/61 (X%) |
| Part II — Council | 96 | X/96 (X%) |
| Part III — Reference architecture | 188 | X/188 (X%) |
| Part IV — Playbooks | 95 | X/95 (X%) |
| Epilogue + Appendices | 114 | X/114 (X%) |

### Coverage by Kleppmann property

(Cross-cut from chapter view — for parity with local-first-properties scorecards)

| Property | Score |
|---|---|
| P1 No spinners | X/61 (X%) |
| P2 Multi-device | X/22 (X%) |
| P3 Network optional | X/158 (X%) |
| P4 Collaboration | X/138 (X%) |
| P5 Long now | X/181 (X%) |
| P6 Security | X/199 (X%) |
| P7 Ownership | X/216 (X%) |

**Headline:** [one sentence — e.g., "Strong on Part III spec (Ch11-14 at 80%+); weak on Part IV playbooks (Ch17-19 at <40%) reflecting that this is a library, not a packaged product."]

## Top remediation priorities (ranked by leverage × gap size)

Ranking heuristic: prioritize concepts that are (1) referenced by `must-implement` of multiple other concepts, (2) currently `missing`, (3) in chapters where overall score is below 50%.

1. `<chapter:id>` — <name>: <one-line remediation>
2. ...

## Per-chapter findings

### Epic: Preface (preface) — X/8 complete

[Same per-concept structure as local-first-properties report, with status icon, ref, name, evidence, suggested remediation.]

### Epic: When SaaS Fights Reality (ch01-when-saas-fights-reality) — X/11 complete

...

[... all 28 chapters in book order ...]

## Synthesis cross-references

This catalog has known synthesis relationships. When scoring, note:

- **ch10-synthesis ← ch05-ch09 LENS**: a Ch10 LENS-* concept being `complete` implies its Ch05-Ch09 source LENS-{E,D,S,P,LF}-* concepts are also covered. Conversely, gaps at the per-lens level may not roll up to Ch10 if Ch10 already absorbed the requirement.
- **ch14 ← appendix-a (wire format)**: Ch14 SYNC-* concepts and Appendix A WIRE-* concepts are paired (semantics + format). A complete WIRE-* without a corresponding SYNC-* implementation is a documentation-only gap; the inverse is rare.
- **ch15 ← appendix-b (threat model)**: Ch15 KEY-*/SEC-* primitives + App B THREAT-*/MITIG-* worksheets are complementary. App B can be `complete` (worksheets exist) even if some Ch15 mechanisms are partial.
- **appendix-d → ch12-ch15 (tests)**: TEST-* concepts operationalize Part III concepts. A TEST-* being `complete` is evidence FOR the corresponding Part III concept; it doesn't substitute.
- **epilogue → Part III (obligations)**: EPI-* concepts are obligation contracts pointing at Part III mechanisms. Score them by checking the Part III referent.

## Not-applicable concepts (with justification)

- `<chapter:id>` — <name>: <why not applicable to this repo>

## Re-run guidance

To re-score after closing gaps: invoke `inverted-stack-conformance` again on the same repo. Idempotent — does not modify the target repo.

To compare deltas: diff this report against the previous one. The chapter-by-chapter structure makes per-epic deltas easy to read.

To advance to remediation (Sunfish-style ICM repos): the report is now in `icm/01_discovery/output/`. Open a Stage 02 Architecture work item using the report's "Top remediation priorities" as the input.
```

### 6. Surface the report

Tell the user:
- The path to the report
- The headline summary
- The top 3 remediation priorities
- The lowest-coverage chapter (often the most useful to discuss first)
- An offer to deep-dive into any chapter

## Specific behaviors

### Filtering by chapter

If the user filters (e.g., "just Part III"), produce a complete report scoped to those chapters AND a smaller header:

```markdown
**Chapter filter:** Part III only (ch11-ch16)
**Concepts in scope:** 188
**Concepts excluded:** 374 (front matter, Part I, Part II, Part IV, epilogue, appendices)
```

The summary tables show only the in-scope counts. Per-chapter findings only cover in-scope chapters.

### Filtering by scope

If the user wants only `foundational` or only `inverted-stack-specific`:

- `foundational` filter → effectively the same as running `local-first-properties` but with chapter grouping. Recommend the user invoke `local-first-properties` instead unless they specifically want chapter-grouped output.
- `inverted-stack-specific` filter → useful for "what book-specific architecture is in this repo?" — focuses on the architectural choices that distinguish Inverted Stack from generic local-first.

### Sunfish-specific scoring (if target repo is Sunfish itself)

If the target repo is `c:/Projects/Sunfish` (or appears to be — check for `Sunfish.*` package names), there's an additional resource: `c:/Projects/Sunfish/icm/_config/conformance-map.md` (built in a separate session) maps each book concept to the Sunfish package(s) where it should live. If that file exists, USE IT — it tells you exactly where to look for evidence of each concept, vastly speeding up scoring.

If the file doesn't exist yet, fall back to general grep/glob across the Sunfish package layout: `packages/foundation/`, `packages/kernel/`, `packages/sync/`, `apps/anchor/`, `apps/bridge/`, `tooling/`.

## Calibration notes

**Inverted-Stack-specific concepts have stricter evidence requirements.** A concept like `ch11:NODE-22 — Daemon as separate process with length-prefixed CBOR over UDS` requires the SPECIFIC implementation choice (CBOR + UDS), not just any IPC mechanism. If the repo uses gRPC over TCP, that's `not_applicable` (different architectural choice) — note this clearly and don't penalize.

**Foundational concepts can be implemented many ways.** A concept like `ch12:CRDT-02 — Algebraic CRDT properties hold` is satisfied by Loro, Yjs, Automerge, or any custom impl that demonstrates commutativity/associativity/idempotency under property tests.

**Pre-1.0 repos won't have Part IV coverage.** Part IV is the playbooks for shipping to enterprise. A pre-1.0 reference implementation (like Sunfish today) will legitimately have low Part IV scores — the playbooks document what they would do at GA, not what they've already shipped.

**Council chapters (Part II) are constraints, not contracts.** A `partial` or `missing` LENS-* finding usually means "the constraint isn't surfaced in the design" rather than "the code doesn't satisfy it." Often, the architecture satisfies the constraint by accident — verify by reading the code, then suggest the constraint be made explicit in an ADR.

## Refreshing the catalog

The bundled `references/concept-index.yaml` is a snapshot from `the-inverted-stack` repo. To refresh:

1. `git pull` `the-inverted-stack`
2. Run `python build/consolidate_concept_index.py` in that repo
3. Copy `docs/reference-implementation/concept-index.yaml` over this skill's `references/concept-index.yaml`
4. Refresh `references/chapter-overview.md` from the metadata header

Pin the snapshot to a known book commit if reproducibility across teams matters.

## What this skill does NOT do

- Does not modify the target repo's source code
- Does not run the target repo or its tests
- Does not score against frameworks other than this book (use other tools for general code review)
- Does not attempt to fix gaps automatically
- Does not produce binary "compliant / not compliant" — coverage is a percentage, and the rubric (complete/partial/missing/n_a) preserves nuance

## Acknowledgments

Catalog source: *The Inverted Stack: Local-First Nodes in a SaaS World* by Christopher Wood, full `concept-index.yaml`. Companion to the `local-first-properties` skill (which scopes to the foundational subset for engine-agnostic scoring).
