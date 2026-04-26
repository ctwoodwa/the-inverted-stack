---
name: local-first-properties
description: Score any local-first repository against Kleppmann's seven local-first properties (P1-P7) using a curated catalog of foundational concepts derived from *The Inverted Stack: Local-First Nodes in a SaaS World*. Use whenever a repo claims to be "local-first," "offline-first," or "user-data-owned" and you need a structured discovery report with per-property gaps, evidence, and remediation tasks. Works on any repo regardless of CRDT engine choice (Loro, Yjs, Automerge, custom) — the catalog is filtered to ENGINE-AGNOSTIC concepts. ICM-aware: writes findings into `icm/01_discovery/output/` if the repo has Sunfish-style ICM, otherwise `.local-first-conformance/` at repo root. Invoke when the user asks "is this repo local-first?", "score this repo against Kleppmann's seven properties," "what local-first gaps does X have?", or after cloning a repo that claims local-first behavior.
---

# Local-First Properties — Conformance Skill

## Why this skill exists

"Local-first" is a label that everyone reaches for and nobody scores against. Martin Kleppmann's 2019 Ink & Switch paper named seven properties as the minimum bar; anything calling itself local-first should be able to demonstrate every one. This skill turns that bar into a structured, repeatable discovery exercise: read the repo, score each property, identify gaps, and emit a report a team can act on.

The catalog is derived from `concept-index-by-property.yaml` (538 foundational entries grouped by P1-P7). Foundational means: any local-first impl needs them, regardless of CRDT engine, framework, or language. Inverted-Stack-specific concepts are intentionally excluded — for those, use the sister `inverted-stack-conformance` skill.

## When to consult this skill

Use it when:

- A user asks "is this repo local-first?", "score this against Kleppmann's seven properties," or "what local-first gaps does X have?"
- A user runs the skill against a repo they're evaluating for adoption, fork, or contribution.
- A user wants a baseline conformance report before starting a sprint of local-first improvements.
- A user re-runs the skill after closing gaps to measure delta.

Skip it when:

- The repo doesn't claim local-first or offline-first behavior — the property bar doesn't apply.
- The user wants a deep, book-specific scorecard with the Inverted Stack's specific architectural choices (Zone A/B/C, Flease, sync daemon protocol from Appendix A, etc.) — use `inverted-stack-conformance` instead, which has 562 concepts vs. this skill's foundational subset.

## The seven properties

The catalog groups every foundational concept under at least one property:

- **P1 — No spinners.** Reads and writes hit local storage; the user never waits on a network call for core operations.
- **P2 — Your work is not trapped on one device.** Multi-device sync without a single device being authoritative.
- **P3 — The network is optional.** Disconnected operation matches connected operation for core function.
- **P4 — Seamless collaboration with colleagues.** Concurrent multi-user edits converge correctly.
- **P5 — The Long Now.** Data outlives the vendor, the subscription, the company strategy shift.
- **P6 — Security and privacy by default.** Encrypted at rest and in transit; the relay sees ciphertext only.
- **P7 — You retain ultimate ownership and control.** Export, recovery, and operation under user-controlled infrastructure.

Concept distribution (foundational only): P1=36, P2=9, P3=89, P4=78, P5=108, P6=103, P7=115. Concepts can serve multiple properties.

## How to invoke

When the user asks for a scan, follow this procedure exactly. Do not skip steps; do not adapt for "speed" — the report's value comes from following the procedure.

### 1. Detect the target repo

The skill operates on a target repo path. Default to the current working directory if none given. Confirm the path with the user before scanning:

> "I'll score `<path>` against the seven local-first properties. The catalog has 538 foundational concepts grouped by P1-P7. Expect 30-45 minutes for a deep scan, 10-15 for a quick pass. Quick or deep?"

### 2. Detect the output destination

Run a single check:

```bash
test -d <repo>/icm && test -f <repo>/icm/CONTEXT.md && echo "ICM-style"
```

- **If ICM-style** (Sunfish-style 9-stage pipeline): write the report to `<repo>/icm/01_discovery/output/local-first-conformance-<YYYY-MM-DD>.md`. Discovery is the right ICM stage for this kind of finding (per `icm/CONTEXT.md`'s `sunfish-gap-analysis` variant — Stage 01 is heavyweight for gap scoping).
- **Otherwise**: create `<repo>/.local-first-conformance/` and write `report-<YYYY-MM-DD>.md` there.

State the destination to the user before writing.

### 3. Load the catalog

Read `references/concept-index-by-property.yaml` from this skill's folder. The structure is:

```yaml
metadata:
  view: Foundational concepts grouped by Kleppmann property (P1-P7)
  scope-filter: foundational only
  concepts-per-property: {P1: 36, P2: 9, ...}

properties:
  P1:
    - ref: ch01-when-saas-fights-reality:THESIS-02
      name: <concept name>
      definition: <one sentence>
      must-implement: [<imperative requirement>, ...]
      verification: <how to check>
  P2: [...]
  ...
```

Each entry's `ref` is the canonical concept reference (`<chapter-stem>:<local-id>`); use it verbatim in the report so users can look concepts up in the source book.

### 4. Score each property

For each property P1 through P7 in order:

1. Read every concept in that property's bucket.
2. For each concept:
   - Read the `must-implement` requirements.
   - Read the `verification` field — this is the SPECIFIC check to run.
   - Use Read/Grep/Glob to look for evidence in the target repo. Common verification types and how to check them:
     - **File or namespace presence** — Glob for path patterns; Grep for namespace declarations or class/function definitions.
     - **Behavioral check** — Read relevant source files; reason about whether the behavior is implemented.
     - **Integration test presence** — Glob for test files; Grep for test names that suggest the scenario is covered.
     - **Configuration or contract** — Read config files, manifest files, or interface definitions.
   - Classify as `complete | partial | missing | not_applicable` per the rubric below.
3. Tally: `<complete count> / <total>` per property.

**Classification rubric (Standard mode — recommended default):**

| Status | Criteria |
|---|---|
| `complete` | Evidence found AND it implements the requirement(s) substantively (not just a stub) |
| `partial` | Evidence found but incomplete (e.g., interface exists but no implementation; tests assert success path only; only one of two required must-implement items is satisfied) |
| `missing` | No evidence found |
| `not_applicable` | The concept does not apply to this repo's architecture (justify in the notes — e.g., "this repo is server-only, P2 multi-device sync is out of scope") |

For each `partial` or `missing` finding, capture:
- The concept ref + name
- What evidence is missing
- A one-line remediation suggestion (where to add the missing piece, what file or namespace)

### 5. Emit the report

The report follows this structure exactly:

```markdown
# Local-First Conformance Report

**Repo:** `<repo path>`
**Scan date:** YYYY-MM-DD
**Catalog:** local-first-properties skill (foundational subset, P1-P7), 538 concepts
**Mode:** quick | deep

## Summary

| Property | Definition | Score |
|---|---|---|
| P1 | No spinners | 24/36 (67%) |
| P2 | Multi-device | 4/9 (44%) |
| P3 | Network optional | 71/89 (80%) |
| P4 | Collaboration | 52/78 (67%) |
| P5 | Long now | 88/108 (81%) |
| P6 | Security | 64/103 (62%) |
| P7 | Ownership | 91/115 (79%) |
| **Total** | — | **394/538 (73%)** |

**Headline:** [one sentence — e.g., "Strong on P5/P7, weak on P2/P6 — multi-device sync and key custody are the largest gaps."]

## Top remediation priorities (ranked by gap size + property weight)

1. **<concept ref>** — <one-line remediation>
2. ...

## Per-property findings

### P1 — No spinners (24/36 complete, 8 partial, 4 missing)

**Complete:**
- `<chapter:id>` — <name>: <evidence>
- ...

**Partial:**
- `<chapter:id>` — <name>: <what's there + what's missing>. Suggested remediation: <one line>.
- ...

**Missing:**
- `<chapter:id>` — <name>: no evidence found. Suggested remediation: <one line>.
- ...

### P2 — Multi-device
[same structure]

[... P3-P7 ...]

## Not-applicable concepts (with justification)

- `<chapter:id>` — <name>: <why not applicable>

## Re-run guidance

To re-score after closing gaps: invoke `local-first-properties` again on the same repo. The skill is idempotent — it will produce a fresh report without modifying the target repo.

To compare deltas: diff the new report against this one (`diff -u report-<old>.md report-<new>.md` or eyeball the per-property scores).
```

Stick to this structure. Downstream tools (and humans skimming the file) rely on the table format and section headers being consistent across runs.

### 6. Surface the report

After writing, tell the user:
- The path to the report
- The headline summary (one sentence)
- The top 3 remediation priorities
- An offer to deep-dive into any property they want to discuss

Do NOT modify the target repo beyond writing the report (and creating `.local-first-conformance/` if needed). This skill is read-only on source code.

## Modes: Quick vs. Deep

Two depth settings the user can choose at invocation:

- **Quick (10-15 min)** — for an initial sniff test. For each property, sample 30-50% of concepts (prefer the highest-leverage ones — those that appear in must-implement of multiple other concepts). Mark unsampled concepts as `unscanned` rather than `missing`. Useful for "is it even worth running deep?"
- **Deep (30-45 min)** — score every concept. Default for any conformance claim or sprint planning.

The mode goes in the report header so re-runs can be compared like-for-like.

## Calibration notes

**The catalog reflects this book's opinions, not Kleppmann's paper alone.** The seven properties are Kleppmann's; the *concepts that serve them* are derived from *The Inverted Stack*'s foundational subset. A repo that takes a fundamentally different architectural approach to a property (e.g., uses CmRDTs instead of state-based CRDTs for P4 collaboration) may legitimately fail concepts that are framed around the book's choices. When that happens, mark `not_applicable` with a clear justification — don't penalize architectural divergence.

**P2 is under-represented in the catalog (only 9 concepts).** This reflects the book's emphasis (multi-device is largely a consequence of P3/P4 working correctly, not a separate architectural axis) rather than the property being unimportant. A multi-device-heavy repo should probably score P2 leniently and look at P3/P4 results for actual multi-device readiness.

**Foundational ≠ universal.** Some "foundational" concepts in the catalog (like specific schema-evolution patterns) reflect *the book's* understanding of what every local-first system needs. A repo that solves the problem differently isn't wrong — but it should be able to articulate how it solves it before claiming `not_applicable`.

## Refreshing the catalog

The bundled `references/concept-index-by-property.yaml` is a **snapshot** from `the-inverted-stack` repo at the date this skill was committed. To refresh after the book is updated:

1. Clone or `git pull` `the-inverted-stack` to a local directory.
2. Run `python build/consolidate_concept_index.py` in that repo to regenerate the canonical YAMLs.
3. Copy `docs/reference-implementation/concept-index-by-property.yaml` over this skill's `references/concept-index-by-property.yaml`.
4. Update the snapshot date in this skill's frontmatter description if the property counts changed.

The skill catalog is versioned with the book; pin the snapshot to a known book commit if you need reproducibility across teams.

## What this skill does NOT do

- **Does not modify the target repo's source code.** The report is the output; remediation is the user's call.
- **Does not run the target repo or its tests.** All checks are static (file/namespace/behavior reading). For dynamic verification (run a multi-peer integration test, observe convergence), the user runs the test themselves.
- **Does not score against Inverted-Stack-specific architectural choices.** Use the `inverted-stack-conformance` skill for that.
- **Does not rate one CRDT engine choice over another.** Engine choice is `not_applicable` to the seven properties — what matters is whether the chosen engine satisfies the per-CRDT-type requirements.
- **Does not attempt to fix gaps automatically.** Findings are surfaced; remediation is a separate planning step (which in Sunfish-style ICM repos flows through stages 02_architecture → 06_build).

## Acknowledgments

Catalog source: *The Inverted Stack: Local-First Nodes in a SaaS World* by Christopher Wood, foundational subset of `concept-index-by-property.yaml`. The seven properties are Martin Kleppmann et al., "Local-first software: You own your data, in spite of the cloud" (Ink & Switch, 2019).
