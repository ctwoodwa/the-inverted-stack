# OpenWolf

@.wolf/OPENWOLF.md

This project uses OpenWolf for context management. Read and follow .wolf/OPENWOLF.md every session. Check .wolf/cerebrum.md before generating code. Check .wolf/anatomy.md before reading files.


# The Inverted Stack — Book Authoring Instructions

## What This Repo Is

*The Inverted Stack: Local-First Nodes in a SaaS World* — a ~83,500-word self-published
practitioner book. Chapters live under `chapters/`. The writing plan is
`inverted-stack-book-plan.md`. The approved structure is `book-structure.md`.

**Audience:** Software architects, technical founders, senior engineers, and IT decision-makers
evaluating local-first architecture. Readers are practitioners, not researchers. They know
distributed systems vocabulary but do not need proofs.

**Voice:** Governed by `docs/style/style-guide.md`.
Key constraints:
- **Purpose before process.** Every section opens with why it exists, not what it does.
- **Active voice. Strong verbs.** "The gateway routes requests" — not "requests are routed."
- **Agency vocabulary.** "The service fails when X" — not "this issue may be encountered."
- **No hedging as default register.** Replace "could potentially" with a specific claim.
- **No synonym cycling.** Name a concept once; use that name everywhere.
- **Narrative for persuasion.** Part I uses scenario-driven Story Spine structure (Luhn).
- **No academic scaffolding.** No "this paper argues", "as we have seen", "the author contends."
- **Lead with the punchline.** Decision before reasoning. Constraint before implementation detail.

**Diagrams:** Mermaid (fenced code blocks with `mermaid` language tag). Pandoc-compatible; renders natively on GitHub. Use for architecture diagrams, flow charts, and sequence diagrams. Do not use ASCII art or external image files for diagrams that can be expressed in Mermaid.

**Citations:** IEEE numeric style. In-text: [1], [2], [3] in order of first appearance. Full reference list compiled at final assembly. Follow all rules in `chapters/appendices/appendix-e-citation-style.md` exactly.

---

## Source Material

All source files live in `source/` at the repo root (gitignored — not committed to the public repo):

| Alias | File | Role |
|---|---|---|
| **v13** | `source/local_node_saas_v13.md` | Primary architecture paper — main source of truth |
| **v5** | `source/inverted-stack-v5.md` | Companion paper — .NET/MAUI/Loro specifics |
| **R1** | `source/kleppmann_council_review.md` | Round 1 adversarial review (6 blocks) |
| **R2** | `source/kleppmann_council_review2.md` | Round 2 review (all blocks cleared, 15 conditions) |

**Reference implementation:** `C:\Projects\Sunfish\`
- `accelerators/anchor/` — Zone A local-first desktop
- `accelerators/bridge/` — Zone C hybrid SaaS

---

## ICM Pipeline

Every chapter moves through these stages. The current stage is tracked as a GitHub label.

| Stage | Label | Description |
|---|---|---|
| 1 | `icm/outline` | Outline drafted and reviewed against book-structure.md |
| 2 | `icm/draft` | First draft written; word count within ±10% of target |
| 3 | `icm/code-check` | Code snippets validated against Sunfish packages |
| 4 | `icm/technical-review` | Technical accuracy audit against v13 + v5 |
| 5 | `icm/prose-review` | Readability and style pass |
| 6 | `icm/voice-check` | Human synthesis: personal anecdotes, consistent voice |
| 7 | `icm/approved` | Chapter approved for final assembly |
| 8 | `icm/assembled` | Included in `ASSEMBLY.md` final manifest |

**Branching convention:** `draft/ch01`, `draft/ch05`, etc. Open a PR against `main` when
a chapter reaches `icm/technical-review`. Merge at `icm/approved`.

---

## Specialized Agents

Four subagents are defined in `.claude/agents/` (also installed at user scope `~/.claude/agents/`).
Invoke them by name or @-mention:

| Agent | When to use | Invoke as |
|---|---|---|
| `chapter-drafter` | Write a first draft from an outline (Stage 2) | `@chapter-drafter draft ch01` |
| `technical-reviewer` | Verify claims against v13/v5, flag invented APIs (Stage 4) | `@technical-reviewer review ch12` |
| `prose-reviewer` | Active voice, no scaffolding, paragraph length (Stage 5) | `@prose-reviewer review ch05` |
| `research-assistant` | Find citations, source claims, brainstorm outlines (any stage) | `@research-assistant find sources for [claim]` |

## Chapter Templates

Templates in `templates/` match the voice requirements for each part:

| Template | For | Apply with |
|---|---|---|
| `chapter-standard.md` | Part I (Ch 1–4) and epilogue | `make template type=standard ch=ch01` |
| `chapter-council.md` | Part II (Ch 5–10) — two-act structure | `make template type=council ch=ch05` |
| `chapter-reference.md` | Part III (Ch 11–16) — specification voice | `make template type=reference ch=ch11` |
| `chapter-playbook.md` | Part IV (Ch 17–20) — tutorial voice | `make template type=playbook ch=ch17` |

---

## Writing Workflow

### Outline (Stage 1)
Read the chapter entry in `book-structure.md`. Expand each bullet into a 2–4 sentence
summary. Identify the one claim the chapter must land. Post the outline as a comment on
the chapter's GitHub issue before drafting.

### Draft (Stage 2)
Write prose against the outline. Check word count: `make word-count`. Commit at the end
of each writing session — never leave an uncommitted draft.

### Code Check (Stage 3)
Every code snippet must compile or be explicitly marked `// illustrative — not runnable`.
Validate Sunfish package names against `C:\Projects\Sunfish\` (no invented APIs).
Run: `make code-check CHAPTER=ch01`

### Technical Review (Stage 4)
Read the chapter as a hostile reviewer. Check every claim against v13 + v5. Mark any
assertion that goes beyond the papers with `<!-- CLAIM: source? -->`. Resolve all markers
before moving to Stage 5.

### Prose Review (Stage 5)
Read aloud. Cut every sentence that restates the previous sentence. Cut every word that
does not earn its place. Target: no paragraph longer than 6 sentences.

### Voice Check (Stage 6 — human only)
Claude cannot do this step. The author adds personal context, field anecdotes, and the
connective tissue that makes the book a book rather than a report. This is the step that
makes it yours.

---

## Quality Checklist

Apply before every chapter PR merge. All items must pass.

```
[ ] QC-1  Word count within ±10% of target
[ ] QC-2  Every topic in book-structure.md for this chapter is addressed
[ ] QC-3  Source sections cited inline (v13 §X, v5 §Y, R1/R2 where applicable)
[ ] QC-4  Sunfish packages referenced by name only (Sunfish.Kernel.Sync) — no class APIs
[ ] QC-5  No academic scaffolding ("this paper argues", "as we have seen")
[ ] QC-6  No re-introducing the architecture (body chapters assume Part I is read)
[ ] QC-7  Part III voice: specification (what it is, how it works fully)
          Part IV voice: tutorial (minimal path, references Part III, does not repeat it)
[ ] QC-8  Ch 2 only: one paragraph per prior work, ends with what this book adds
[ ] QC-9  Council chapters: two-act structure (R1 failure → what changed → R2 verdict)
[ ] QC-10 No placeholder text ("TBD", "expand here", "see paper for details")
```

---

## Writing Discipline Rules

1. **Part III is specification; Part IV is tutorial.** Part IV references Part III — does not
   rewrite it.
2. **Ch 2 is opinionated, not encyclopedic.** One paragraph per existing approach, ends with
   a crisp statement of what this book adds.
3. **Council chapters have two acts.** Round 1 → narrative gap → Round 2.
4. **Sunfish references by package name, not class API.** Pre-1.0; APIs evolve.
5. **No re-introducing the architecture.** Each chapter assumes the reader has read Part I.

---

## Sunfish Reference Policy

- Reference packages by name: `Sunfish.Kernel.Sync`, `Sunfish.Foundation.LocalFirst`
- Do not reference specific class names, method signatures, or constructor parameters
- Pre-1.0 disclaimer applies to all Sunfish references
- If a Sunfish API is needed for an example, mark it `// illustrative` and note it in the
  chapter's GitHub issue for validation when Sunfish reaches the relevant milestone
- CRDT engine: YDotNet is the current Sunfish implementation; Loro is the aspirational target.
  The architecture is engine-agnostic via `ICrdtEngine`. Mention both where relevant.

## Org chart + coordination

Naval-org: **CO** (Chris, BDFL) → **XO** (research session in `/Users/christopherwood/Projects/Sunfish`) → {**COB** (sunfish-PM, code), **PAO** (book editor/publisher, this repo) → **Yeoman** (technical writer, this repo)}.

**Yeoman** drafts and revises chapters; runs the audiobook pipeline. Reports to PAO.

**PAO** is the book editor + publisher: enforces clarity / structure / voice; reviews chapters; rewrites weak sections; recommends reorganizations; manages Yeoman's daily editorial work. Cross-repo funnel for Sunfish-architecture questions. Reports to XO. Doesn't draft prose; doesn't make Sunfish-architecture calls.

## Two-tier inbox protocol

### Tier 1 — book-internal (Yeoman ↔ PAO): `.pao-inbox/`

Filesystem inbox at `.pao-inbox/` in the book repo root. Yeoman writes `yeoman-question-*.md` when blocked on style / pacing / structural calls; PAO scans and resolves inline. Archived beacons go to `.pao-inbox/_archive/`. State snapshots (PAO's authoritative read of book status) go to `.pao-inbox/_state-snapshots/`. **Snapshots and beacons MUST be committed + pushed to the book repo** — leaving them in the working tree alone defeats persistence across session restarts.

**File naming:** `yeoman-{question|resumed}-YYYY-MM-DDTHH-MMZ-{slug}.md`. **Body:** 3-line YAML frontmatter (`type`, `chapter`, `last-pr`) + ≤2 lines context + ≤2 lines "what would unblock me." Tight; signal, not narrative.

### Tier 2 — cross-repo escalation (PAO → XO): Sunfish's `research-inbox/`

When chapter progress is gated on a Sunfish-side question (ADR status, workstream timing, foundational-paper alignment) PAO can't resolve from the book + Sunfish docs alone, **PAO writes** `pao-question-*.md` to Sunfish's `icm/_state/research-inbox/`. PAO is the cross-repo funnel for the book side. **Yeoman does NOT write directly to Sunfish** unless PAO is offline AND the question is critical (PAO-bypass fallback; flag in body).

**Cross-repo write recipe (PAO):**

```bash
cd /Users/christopherwood/Projects/Sunfish
git fetch origin main
git worktree add /tmp/sunfish-pao-beacon-wt origin/main -b chore/pao-beacon-<slug>
# author /tmp/sunfish-pao-beacon-wt/icm/_state/research-inbox/pao-question-<ts>-<slug>.md
cd /tmp/sunfish-pao-beacon-wt
git add icm/_state/research-inbox/ && git -c commit.gpgsign=false commit -m "chore(inbox): pao question — <slug>"
git push -u origin HEAD && gh pr create --title "chore(inbox): pao question — <slug>" --body "<context>"
gh pr merge --auto --squash
cd - && git worktree remove /tmp/sunfish-pao-beacon-wt
```

When XO answers (hand-off / ledger update / ADR amendment in Sunfish), the beacon gets `git mv`-ed to `_archive/` in the resolving PR.

Canonical protocol spec: Sunfish `CLAUDE.md` § "Live signaling to XO — `research-inbox/`".

---

## Build Targets

```bash
make draft-pdf           # Full manuscript draft PDF via Pandoc
make chapter-pdf ch=ch01 # Single chapter PDF
make word-count          # Word count per chapter vs. targets
make code-check ch=ch01  # Validate code snippets in one chapter
make epub                # ePub for Leanpub preview
make lint                # Check for broken cross-references
```

---

## Repo Conventions

- Branch naming: `draft/ch01`, `draft/prospectus`, `draft/appendix-a`
- Commit message prefix: `draft:`, `outline:`, `review:`, `fix:`, `build:`
- Do not commit source papers (`local_node_saas_v13.md` etc.) — they live in `source/` which is gitignored
- Chapter files are committed even when incomplete — no dark drafts
