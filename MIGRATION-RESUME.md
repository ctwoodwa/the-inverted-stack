# Migration Resume — Book Update Loop Session State

**Generated:** 2026-04-27 by the autonomous /loop session.
**Last commit before migration:** `5a02dd1` (this commit will likely follow).
**Reason for this file:** session migration from Windows to macOS; survives even if `~/.claude/` session transcripts fail to load.

If the session transcript loaded cleanly on the new machine and Claude already has full conversation context, you can ignore this file. If the transcript did not load (or you started a fresh session), paste the **First-prompt template** below to bootstrap context. The state itself is captured authoritatively in `docs/book-update-plan/state.yaml`; this file is a human-readable summary on top of that.

---

## Loop state at migration

The book extension loop has 10 extensions. Status as of this commit:

| Extension | Stage | Status | Next autonomous step |
|---|---|---|---|
| #48 key-loss-recovery | approved | published-ready (assembly mechanical) | mark assembled when ASSEMBLY.md runs next |
| #43 performance-contracts | voice-check | **awaiting human voice-pass** | human adds anecdote + connective tissue + Sinek calibration |
| #45 collaborator-revocation | voice-check | **awaiting human voice-pass** | same |
| #11 fleet-management | voice-check | **awaiting human voice-pass** | same |
| #46 forward-secrecy | draft (applied) | code-check is next | dispatch code-check verification |
| #47 endpoint-compromise | draft (staged, NOT applied) | apply pending | renumber refs [14]–[22] → [20]–[28], then apply Ch15 + App B inserts |
| #9 chain-of-custody | outline | draft is next | dispatch chapter-drafter |
| #12 privacy-aggregation | not-started | outline is next | dispatch research-assistant for outline |
| #10 data-class-escalation | not-started | outline is next | same |
| #44 per-data-class-device-distribution | not-started | outline is next | same |

## Voice-check tasks queued for the human (3 sections)

When you resume, three new sections await your voice-pass. Each has working artifacts in `docs/book-update-plan/working/<extension-id>/`:

### #43 — Ch11 §Performance Contracts + Ch20 §Performance Budgets

- **Anecdote opener** for §Why performance is a specification concern. Outline §F suggests: the moment a CRDT merge freezes the UI (force-quit / lost-state visceral); or a Linear/Notion 60fps adoption observation. Three candidate framings in `working/43-performance-contracts/outline.md` §F.
- **Ch11 ↔ Ch20 connective tissue** — pairing sentence in each direction.
- **Light Sinek calibration** per `~/.claude/projects/.../memory/feedback_voice_sinek_calibration.md`.
- **2 open `<!-- CLAIM: -->` markers** at Linear 60fps and Apple HIG 16ms — non-blocking; queued for future technical-review when better source URLs surface, not for voice-check.

### #45 — Ch15 §Collaborator Revocation + Ch20 §Revocation UX

- **Departure-moment anecdote** for Ch20 §The departure moment (a deliberate `<!-- voice-check: -->` HTML placeholder is in the chapter; replace it). Three candidate framings: departing employee packing a desk; business partner reading the access-ended message after a court-mediated settlement; administrator processing access revocation for a long-time colleague.
- **Connective tissue** Ch15 ↔ Ch20.
- **Light Sinek calibration**.

### #11 — Ch21 §Operating a Fleet of Local-First Nodes (NEW chapter)

- **Opening hook anecdote** — three candidates listed in the chapter-drafter QC notes (`working/11-fleet-management/draft.md` QC section).
- **Sharpening the provisioning-as-cultural-shift moment**.
- **Light Sinek calibration**.
- **Optional connective-tissue line** at close of §21.6 fleet-failure narrative.

When all three voice-pass tasks complete, each extension flips `awaiting-voice-check → approved → assembled`, and the loop autonomously continues with the remaining extensions (#46, #47, #9, #12, #10, #44).

## What this session accomplished (high level)

- **#48** completed the full pipeline: 3-round Kleppmann Council adversarial review (R1 REVISE 5.9 BLOCK → R2 PUBLISH 8.24 → R3 PUBLISH 8.62), 12-critic Literary Board (POLISH 8.17), 30+ substantive edits applied, Uncle-Charlie-iPhone anecdote inserted, Ch15↔Ch20 connective tissue, Sinek calibration declared no-op. **Approved.**
- **#43, #45, #11** each cleared outline → draft → code-check → technical-review → prose-review (all PASS). Now waiting on human voice-pass.
- **#46** drafted and applied to Ch15 (between §Collaborator Revocation and §In-Memory Key Handling). 6 new IEEE refs [14]–[19] added.
- **#47** drafted but not yet applied — citation numbering conflict ([14]–[22] needs to renumber to [20]–[28] because #46 already claims [14]–[19]).
- **#9** outline pre-staged with NEW namespace decision: `Sunfish.Kernel.Custody`.
- **3 outlines pre-staged in parallel** as background research-assistant dispatches: #11 (became active), #47 (became active), #9 (still at outline).
- **Sunfish package roadmap** created at `docs/reference-implementation/sunfish-package-roadmap.md` with mirror at `C:/Projects/Sunfish/docs/specifications/inverted-stack-package-roadmap.md` (Sunfish-side uncommitted at migration time).
- **Effort + model selection memory** written to `~/.claude/projects/.../memory/` (`feedback_effort_mapping.md`, `reference_model_selection.md`). Subagent `.md` frontmatter bumped 11 agents to opus per the Tier 1 routing policy.

## Key documents to know about

| Document | Purpose |
|---|---|
| `docs/book-update-plan/state.yaml` | **Authoritative loop state.** Per-extension status, current-stage, history, quality gates, kill triggers. |
| `docs/book-update-plan/loop-plan.md` | The master plan governing the loop's protocol. |
| `docs/book-update-plan/working/<extension-id>/` | Per-extension artifacts: outline.md, draft.md, code-check-report.md, technical-review-report.md, prose-review-report.md, council-review-round-{1,2,3}.md (where applicable), literary-board-review.md (where applicable), voice-pass-anecdote-candidates*.md (#48 only). |
| `docs/reference-implementation/sunfish-package-roadmap.md` | Authoritative roadmap of forward-looking Sunfish namespaces introduced by Volume 1 extensions. Sunfish-side mirror at `~/Projects/Sunfish/docs/specifications/inverted-stack-package-roadmap.md`. |
| `docs/reference-implementation/design-decisions.md` §5 | Source primitive specifications for all extensions. |
| `~/.claude/projects/.../memory/MEMORY.md` | Index of session-persistent memory entries. |
| `~/.claude/projects/.../memory/feedback_effort_mapping.md` | The /effort tier policy (xhigh default; max for correctness-critical only; medium/low for execution). |
| `~/.claude/projects/.../memory/reference_model_selection.md` | When to use Opus 4.7 vs Sonnet 4.6 vs Haiku 4.5; per-subagent routing. |
| `CLAUDE.md` | Project-wide voice + workflow instructions. |
| `.claude/agents/*.md` | Project-scope subagent definitions (model: frontmatter sets routing). |

## First-prompt template (paste this on the new machine if the session transcript is unavailable)

> I'm resuming a long-running book-update loop session that was migrated from Windows to macOS. Read `MIGRATION-RESUME.md` at the repo root for full context, then read `docs/book-update-plan/state.yaml` for authoritative loop state and `docs/book-update-plan/loop-plan.md` for the loop protocol. Three things to know up front:
>
> 1. **Path translation:** all references in CLAUDE.md, memory files, working artifacts, and the chapter prose to `C:/Projects/the-inverted-stack/...` map to `~/Projects/the-inverted-stack/...`, and `C:/Projects/Sunfish/...` maps to `~/Projects/Sunfish/...`. Don't rewrite anything; just translate as you read.
> 2. **Effort policy:** per the memory entry `feedback_effort_mapping.md`, default is `/effort xhigh` for coding/agentic/multi-file work; `max` only for correctness-critical debugging or complex evaluation; `medium`/`low` for pre-decided execution. Most subagent dispatches are at opus per the agent `.md` frontmatter — that routing is automatic.
> 3. **Three extensions are blocked on my voice-pass** (#43, #45, #11). I plan to handle voice-pass interactively. The autonomous queue is: apply #47 with citation renumber [14]–[22] → [20]–[28], advance #46 + #47 through code-check / tech-review / prose-review to voice-check, then draft #9, then pre-stage outlines for #12, #10, #44.
>
> What's the most useful next step right now? My focus today is [voice-pass on one of #43/#45/#11 / continuing the autonomous queue / something else].

## Path translation cheatsheet

| Windows path | macOS path |
|---|---|
| `C:/Projects/the-inverted-stack/` | `~/Projects/the-inverted-stack/` |
| `C:/Projects/Sunfish/` | `~/Projects/Sunfish/` |
| `C:/Users/Chris/.claude/projects/C--Projects-the-inverted-stack/` | `~/.claude/projects/-Users-<whoami>-Projects-the-inverted-stack/` |
| `C:/Users/Chris/.claude/agents/` | `~/.claude/agents/` |

These appear hardcoded in many of the per-extension working artifacts and in some memory entries. The chapter prose itself is path-agnostic.

## Sunfish-side reminder

The Sunfish repo at `~/Projects/Sunfish/` (after migration) had an uncommitted `docs/specifications/inverted-stack-package-roadmap.md` on branch `docs/anchor-cross-os-strategy-adr-0048` (GitButler-managed). At time of writing, the user said they'd handle the Sunfish side independently. If the migration loses that file, the book-side authoritative copy at `docs/reference-implementation/sunfish-package-roadmap.md` can regenerate it.

If Sunfish uses GitButler virtual branches: install GitButler on macOS, run `but setup` in the cloned Sunfish repo, and reattach to the workspace.

## Quick verification commands

After migration, run these to confirm the migration succeeded:

```bash
cd ~/Projects/the-inverted-stack

# Repo state:
git log --oneline -3                         # most recent should be the commit that added this file
ls docs/book-update-plan/working/            # should list 7 working dirs (43, 45, 46, 47, 48, 9, 11)
grep -c "^  [0-9]" docs/book-update-plan/state.yaml  # should be 10 (extension count)

# Memory:
ME=$(whoami)
ls ~/.claude/projects/-Users-${ME}-Projects-the-inverted-stack/memory/
# Should list: MEMORY.md, feedback_effort_mapping.md, reference_model_selection.md,
#              feedback_source_papers.md, project_sunfish_packages.md,
#              project_failure_mode_taxonomy.md, feedback_voice_sinek_calibration.md,
#              reference_gitbutler_workflow.md, reference_literary_devices_skill.md,
#              reference_anti_ai_tells_skill.md, reference_conformance_skills.md,
#              feedback_effort_mapping.md, reference_model_selection.md
ls ~/.claude/agents/ | wc -l                 # should be 13 user-scope agents

# Voice-pass artifacts (for #48, the example to mirror for #43/#45/#11 patterns):
ls docs/book-update-plan/working/48-key-loss-recovery/
# Should include: voice-pass-anecdote-candidates.md, voice-pass-anecdote-candidates-brown.md,
#                connective-tissue-candidates.md, anecdote-bank.md
```

If any of these fail, the migration is incomplete. The most likely culprit is the project-dir rename on the Mac side — Claude Code keys on `~/.claude/projects/<project-encoded-path>/` and the Windows-encoded directory name will not match the Mac path.

---

**To delete this file once you're settled:** it's safe to remove after a few clean turns of the resumed session. The information lives in state.yaml + memory + git history; this file is a transition aid only.
