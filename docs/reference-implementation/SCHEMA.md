# Concept-Index Schema (v1.0)

This document defines the YAML schema for `concept-index.yaml` and the per-chapter extraction files under `_per-chapter/`. Subagents extracting concepts from book chapters MUST follow this schema exactly so the consolidator can merge cleanly.

## Per-chapter file structure

Each `_per-chapter/<chapter-stem>.yaml` contains:

```yaml
chapter: ch12                                    # Chapter stem (matches markdown filename)
chapter-title: CRDT Engine and Data Layer       # Human-readable title (drop "Chapter N — " prefix)
source-paper-refs: [v13 §6.2, v5 §3.1]          # Cross-references to source papers if cited inline
extraction-date: 2026-04-26
extracted-by: subagent

concepts:
  - id: <CHAPTER-PREFIX>-<NN>                    # Per-chapter local ID; consolidator assigns global IDs
    name: <short, capitalized phrase>
    source: ch12 §"Section heading text"        # Chapter + section heading where defined
    source-paper: v13 §6.2                       # Or null if book-original
    definition: <one sentence, ends with period>
    must-implement:                              # Empty list [] if conceptual/philosophical only
      - <imperative requirement, present tense>
      - <another requirement>
    verification: <how to check implementation>  # Or null if conceptual
    kleppmann-properties: [P1, P3]               # Subset of P1-P7 this serves; [] if none directly
    scope: foundational                          # foundational | inverted-stack-specific
    failure-modes: [partition, key-loss]         # Named failure modes if relevant; [] otherwise
    tags: [crdt, semantic-layer]                 # Free tags for grouping/filtering
    notes: <optional clarification>              # Or omit field
```

## Field guide

### `id`
Per-chapter local identifier — `<PREFIX>-<NN>` where prefix is short and consistent within the chapter.

Recommended prefixes by topic:
- `THESIS-*` — Part I thesis/motivation concepts
- `LENS-*` — Part II council perspective constraints
- `NODE-*` — node architecture (Ch 11)
- `CRDT-*` — CRDT engine, semantic layer (Ch 12)
- `SCH-*` — schema, migration (Ch 13)
- `SYNC-*` — sync daemon, wire protocol (Ch 14, App A)
- `KEY-*` / `SEC-*` — security, keys, threat model (Ch 15, App B)
- `DUR-*` — durability, persistence (Ch 16)
- `BUILD-*` — building first node (Ch 17)
- `MIG-*` — SaaS migration (Ch 18)
- `ENT-*` — enterprise shipping (Ch 19)
- `UX-*` — UX patterns (Ch 20)
- `EPI-*` — epilogue
- `TEST-*` — testing (App D)
- `COMP-*` — compliance, regulatory (App F or per-chapter)

The consolidator MAY rename to canonical global IDs during merge; per-chapter prefixes are a starting point.

### `name`
Short capitalized phrase. Should be unique within the chapter. Examples:
- `Local node as primary data plane`
- `Two-node Flease quorum with managed relay`
- `Schema migration via additive evolution`

NOT good (too vague): `Architecture`, `Sync`, `Security`.

### `source`
Where in this chapter the concept is defined. Use the H2/H3 heading text. If the concept spans multiple sections, list the primary one.

### `source-paper`
Cross-reference to the source papers (`v13` = `local_node_saas_v13.md`, `v5` = `inverted-stack-v5.md`) using their section numbering. Use `null` if the concept is book-original (introduced first in this book, no paper precedent).

### `definition`
ONE sentence that says what the concept IS. Ends with a period. No examples, no rationale — just the definition. The reader should be able to understand what the concept refers to from this line alone.

### `must-implement`
List of imperative requirements an implementation must satisfy to claim coverage of this concept. Each entry is a present-tense statement.

Examples:
```yaml
must-implement:
  - Application reads/writes hit local storage as primary
  - No fallback path that requires cloud connectivity for core function
  - Application has no degraded mode when offline
```

If the concept is purely philosophical/motivational (no direct implementation requirement), use `must-implement: []`.

### `verification`
How to check that an implementation satisfies the requirements. Should describe a *specific test*:
- File or namespace presence: `Sunfish.Kernel.Sync namespace exists with at least one type`
- Behavioral check: `Disconnect network; application performs all core operations identically`
- Integration test: `Multi-peer convergence test under accelerators/anchor/tests demonstrates byte-identical state after partition heal`
- Doc/spec check: `ADR exists naming the chosen consensus protocol and its quorum semantics`

Use `null` if the concept is conceptual and no verification applies.

### `kleppmann-properties`
List the subset of P1-P7 this concept SERVES. Use the property identifiers consistently:

- `P1` — No spinners (fast, work happens locally)
- `P2` — Your work is not trapped on one device (multi-device)
- `P3` — The network is optional (offline-first)
- `P4` — Seamless collaboration with colleagues
- `P5` — The Long Now (data outlives vendor/subscription)
- `P6` — Security and privacy by default
- `P7` — You retain ultimate ownership and control

A concept can serve multiple properties; use `[]` if it serves none directly (e.g., a build-tooling concept).

### `scope`
- `foundational` — applies to ANY local-first system (CRDT merge semantics, key management, conflict resolution UX). The `local-first-properties` skill (generic, 7-property check for any local-first repo) considers ONLY foundational concepts.
- `inverted-stack-specific` — applies specifically to this book's architecture (Zone A/B/C, Sunfish-style package layout, the specific sync daemon protocol from Appendix A, the Bridge hybrid pattern). The `inverted-stack-conformance` skill (book-specific) considers ALL concepts.

Decision rule: if a Loro-based or Yjs-based or Automerge-based system could implement the concept without inheriting Inverted Stack opinions, it's `foundational`. If it requires this book's specific architectural choices, it's `inverted-stack-specific`.

### `failure-modes`
Named failure modes the concept addresses or surfaces. Common modes referenced across chapters:
- `vendor-outage` — vendor service unreachable
- `vendor-acquisition` — vendor change of ownership / terms shift
- `data-residency-objection` — regulator/customer requires data on user-controlled infra
- `partition` — network partition between nodes
- `key-loss` — user loses key material
- `key-compromise` — adversary obtains key material
- `schema-skew` — peers running incompatible schema versions
- `clock-skew` — peer clocks disagree
- `peer-discovery-failure` — node cannot find peers across NAT
- `replay` — adversary replays old messages

Use `[]` if no failure mode is directly addressed.

### `tags`
Free tags for grouping/filtering. Examples: `architecture`, `philosophy`, `crdt`, `semantic-layer`, `wire-protocol`, `migration`, `compliance`, `ux`. No fixed vocabulary; use tags useful for downstream queries.

### `notes`
Optional. Use sparingly — for clarifications that don't fit elsewhere. Omit the field if you don't need it.

## Per-chapter extraction guidance

**High-yield chapters** (specification, playbooks, contracts) — expect 15-30 concepts each:
- Part III: ch11, ch12, ch13, ch14, ch15, ch16
- Part IV: ch17, ch18, ch19, ch20
- Appendix A (wire protocol), B (threat model)

**Medium-yield chapters** — expect 5-15 concepts each:
- Part II: ch05-ch10 (council perspectives surface constraints)
- Appendix D (testing)
- Epilogue

**Low-yield chapters** — expect 3-10 concepts each:
- Front matter: preface
- Part I: ch01, ch02, ch03, ch04 (mostly motivational, but failure modes and the inversion + 5-filter framework ARE concepts)
- Appendix C (further reading), E (citation style)

**Always include**, even from low-yield chapters:
- Named failure modes (Ch01's six failure modes are foundational concepts)
- Named frameworks (Ch04's five-filter framework, the One Question)
- Named patterns (Ch04's "the inversion in one sentence" is a defining concept)

**Do NOT include**:
- Marketing/persuasion language
- Author opinions without a definable concept attached
- Citations or reference list entries
- Code snippets unless they define a contract
- Chapter summaries

## What good extraction looks like

A subagent extracting Ch12 should produce ~20-30 concepts covering:
- The CRDT engine adapter pattern (`ICrdtEngine`)
- The data layer / semantic layer split
- Per-CRDT-type semantics (map, list, text, counter)
- The semantic layer's role in invariant enforcement
- Garbage collection of CRDT history
- Tombstones
- Merge determinism
- Schema-on-write vs schema-on-merge
- Engine-agnostic architecture (YDotNet vs Loro)
- ...and all the other named architectural decisions in that chapter

A bad extraction produces 3 vague concepts: "CRDT engine exists," "data layer is described," "semantic layer is described."

## Validation checklist

Before saving the per-chapter YAML, verify:
- [ ] Every concept has all required fields (id, name, source, definition, must-implement, kleppmann-properties, scope)
- [ ] `definition` is one complete sentence ending with a period
- [ ] `must-implement` items are imperative ("Component X validates Y") not declarative ("Component X exists")
- [ ] `kleppmann-properties` only contains values from P1-P7
- [ ] `scope` is exactly `foundational` or `inverted-stack-specific`
- [ ] No duplicate concept IDs within the file
- [ ] YAML parses cleanly (`python -c "import yaml; yaml.safe_load(open('<file>'))"`)
