# Book ICM Pipeline

*Integrated Change Management for technical authoring. Adapted from the Sunfish ICM model.*

---

## Philosophy

A chapter is not done when you stop writing it. It is done when it has cleared the full
pipeline: outline validated, draft written, code checked, technical accuracy confirmed,
prose reviewed, voice synthesized by the author.

Each stage is a gate — not a rubber stamp. Advancing past a gate means the work at that
stage is complete, not that it will be fixed later.

---

## Pipeline Stages

### Stage 1 — `icm/outline`

**Entry:** Chapter issue created with scope defined
**Work:** Expand book-structure.md bullets into 2–4 sentence summaries per section.
Identify the single claim the chapter must land.
**Gate:** Outline posted as a comment on the GitHub issue; it matches the book-structure.md
scope; the central claim is explicit.
**Output:** Outline comment on the chapter issue

---

### Stage 2 — `icm/draft`

**Entry:** Outline approved (Stage 1 gate passed)
**Work:** Write prose against the outline. Commit at the end of each writing session.
**Gate:** Word count within ±10% of target; all outline sections have prose; QC-1 through
QC-6 pass; no `<!-- TODO -->` markers remain.
**Output:** Chapter file committed on `draft/<chapter>` branch

---

### Stage 3 — `icm/code-check`

**Entry:** Draft committed (Stage 2 gate passed)
**Work:** Every code snippet validated: compiles or marked `// illustrative`.
Sunfish package names verified against `C:\Projects\Sunfish\`.
Run `make code-check ch=<chapter>`.
**Gate:** No unvalidated code snippets; no invented APIs; package names match.
**Output:** Passing `make code-check` output; any illustrative snippets annotated

---

### Stage 4 — `icm/technical-review`

**Entry:** Code check passed (Stage 3 gate passed)
**Work:** Read the chapter as a hostile reviewer. Verify every claim against v13 + v5.
Mark any assertion that goes beyond the papers: `<!-- CLAIM: source? -->`.
Resolve all markers.
**Gate:** Zero unresolved `<!-- CLAIM -->` markers; QC-3 passes (source citations present);
no claims contradict v13/v5.
**Output:** Chapter file with resolved review comments

---

### Stage 5 — `icm/prose-review`

**Entry:** Technical review complete (Stage 4 gate passed)
**Work:** Read aloud. Cut restatements. Cut words that do not earn their place.
No paragraph longer than 6 sentences.
**Gate:** QC-5 passes (no academic scaffolding); readability confirmed; no paragraph > 6 sentences.
**Output:** Revised chapter file committed

---

### Stage 6 — `icm/voice-check`

**Entry:** Prose review complete (Stage 5 gate passed)
**Work:** Author only. Add personal anecdotes, field stories, connective tissue.
Ensure the chapter sounds like the same author as Chapter 1.
**Gate:** Author has read the chapter start-to-finish and approved the voice.
This is the only stage Claude cannot complete.
**Output:** Final chapter file; PR ready for merge

---

### Stage 7 — `icm/approved`

**Entry:** Voice check passed (Stage 6 gate passed)
**Work:** Open PR from `draft/<chapter>` against `main`. Full QC checklist (QC-1 through
QC-10) passes. Merge.
**Gate:** All 10 QC items pass; PR merged.
**Output:** Chapter merged to `main`

---

### Stage 8 — `icm/assembled`

**Entry:** Chapter merged to `main` (Stage 7 gate passed)
**Work:** Chapter added to `ASSEMBLY.md` manifest in correct order. Running word count
updated. Build verified: `make draft-pdf` completes without errors.
**Gate:** Chapter appears in draft PDF output; no assembly errors.
**Output:** Updated `ASSEMBLY.md` committed; draft PDF builds clean

---

## Part Milestones

| Milestone | Chapters | Criteria |
|---|---|---|
| `part-i-complete` | Ch 1–4 | All four chapters at `icm/assembled` |
| `part-ii-complete` | Ch 5–10 | All six chapters at `icm/assembled` |
| `part-iii-complete` | Ch 11–16 | All six chapters at `icm/assembled` |
| `part-iv-complete` | Ch 17–20 | All four chapters at `icm/assembled` |
| `manuscript-complete` | All | All 20 chapters + front matter + epilogue + appendices assembled |
| `v1.0` | All | Final proofreading pass complete; ePub and PDF published |

---

## Dependency Order

Part II council chapters reference claims from Part I. Part III is the specification
that Part IV references. Write in this order:

```
Part I (Ch 1 → 4) in sequence
  ↓
Part II (Ch 5–10) — parallelizable after Part I complete
  ↓
Part III (Ch 11–16) — parallelizable; Ch 13 (schema migration) depends on Ch 12 (CRDT)
  ↓
Part IV (Ch 17–20) — parallelizable after Part III complete
  ↓
Epilogue → Appendices → Front Matter (Preface written last, Foreword placeholder)
```

---

## Quick Reference: Labels

Create these labels in the GitHub repo:

| Label | Color | Meaning |
|---|---|---|
| `icm/outline` | #e4e669 | Chapter in outline stage |
| `icm/draft` | #f9d0c4 | Chapter in first draft |
| `icm/code-check` | #ffa500 | Code snippets being validated |
| `icm/technical-review` | #d4c5f9 | Technical accuracy review |
| `icm/prose-review` | #c2e0c6 | Prose and style review |
| `icm/voice-check` | #0075ca | Author voice synthesis |
| `icm/approved` | #0e8a16 | Approved, ready to assemble |
| `icm/assembled` | #006b75 | In final manuscript |
| `part-i` | #bfd4f2 | Part I chapter |
| `part-ii` | #bfd4f2 | Part II chapter |
| `part-iii` | #bfd4f2 | Part III chapter |
| `part-iv` | #bfd4f2 | Part IV chapter |
