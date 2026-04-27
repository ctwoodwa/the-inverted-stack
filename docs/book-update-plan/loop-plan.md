# Book Update Loop Plan

**Status:** Loopable execution plan for incorporating 10 Volume-1-extension primitives (#9-#12, #43-#48 from `design-decisions.md` §5) into the existing 27 chapters of *The Inverted Stack*.

**Designed for:** Autonomous /loop Claude Code session that self-paces through ICM pipeline stages.

**Prerequisites:** Reader has access to:
- This repo (`C:/Projects/the-inverted-stack`) at the root
- The book chapters (`chapters/`)
- The voice / chapter / technical / prose review subagents (`.claude/agents/`)
- The skills catalog (`.claude/skills/`)
- The `state.yaml` file in this directory (for cross-iteration state)

---

## §1. Mission

Update the current book (Volume 1) to incorporate the 10 architectural primitives surfaced during the design discussion that the existing chapters SHOULD address but currently don't. These are gaps in the book's CURRENT scope, not future-volume aspirations.

The 10 Volume-1-extension primitives (per `design-decisions.md` §5):

| # | Name | Primary target chapter | Edit type |
|---|---|---|---|
| 9 | Chain-of-custody (multi-party signed transfer receipts) | Ch15 §new + App B §new actor | New section + threat-model entry |
| 10 | Data-class escalation (event-triggered re-classification) | Ch20 §new + Ch15 §new | New sections in two chapters |
| 11 | Fleet management (provisioning, key rotation, OTA, observability) | NEW Ch21 OR new App G | New chapter or substantial appendix |
| 12 | Privacy-preserving aggregation (DP / k-anonymity at relay) | Ch15 §new | New section |
| 43 | Performance contracts with framework-level enforcement | Ch11 §new + Ch20 §new | New section in two chapters |
| 44 | Per-data-class device-distribution policy | Ch16 §new | New section |
| 45 | Collaborator revocation and post-departure data partition | Ch15 §new + Ch20 §new | New section in two chapters |
| 46 | Forward secrecy + post-compromise security | Ch15 §new | New section |
| 47 | Endpoint-compromise threat model | Ch15 §new + App B §new actor | New section + threat-model entry |
| 48 | Key-loss recovery | Ch15 §new + Ch20 §new | New section in two chapters |

Estimated total writing: 30-50k additional words (per `book-extension-candidates.md` Volume 1 estimate). Roughly equivalent to a Part V (Operational concerns) added to the existing four parts.

---

## §2. Loop iteration protocol

### What ONE iteration does

Each iteration of the loop:

1. **Reads state** from `docs/book-update-plan/state.yaml` (which extension is in flight, what stage)
2. **Picks next action** based on state:
   - If no extension in flight → start the next one in `priority-order`
   - If one in flight → advance it to the next ICM stage
3. **Executes that action** using the appropriate subagent or direct edit
4. **Updates state** with new stage + commit SHA
5. **Commits** the work (book chapter edit + state file update in one commit)
6. **Reports** what was done in 2-3 sentences
7. **Stops** — the loop fires the next iteration on schedule

### Bounded scope per iteration

ONE iteration advances ONE extension by ONE ICM stage. No more.

ICM stages per extension:

| Stage | Action | Subagent | Output |
|---|---|---|---|
| `outline` | Read existing chapter + design-decisions §5 entry → write outline of new section | none (direct work) | Outline added to extension's working file in `docs/book-update-plan/working/<extension-id>/outline.md` |
| `draft` | Outline → first draft of new section | `@chapter-drafter` (or `@technical-book-writer` for spec chapters) | Draft inserted into target chapter file at appropriate location |
| `code-check` | Validate any code snippets compile / Sunfish package references are real | none (script-driven) | Code-check report; fix any invalid references |
| `technical-review` | Read draft as hostile reviewer; check claims against v13/v5 source papers | `@technical-reviewer` | Technical review report; address findings before advancing |
| `prose-review` | Active voice, no hedging, no academic scaffolding | `@prose-reviewer` then `@style-enforcer` | Style fixes applied in place |
| `voice-check` | **HUMAN ONLY** — author adds personal anecdotes, connective tissue | Loop stops here; surfaces for human | State marked `awaiting-voice-check`; loop pauses on this extension |
| `approved` | After human voice-check, mark approved | none | State marked `approved` |
| `assembled` | Already in main; included in next ASSEMBLY.md run | none | State marked `assembled` |

The loop autonomously executes stages 1-5 (`outline` through `prose-review`). It STOPS at stage 6 (`voice-check`) and waits for human attention. Stage 7 (`approved`) and stage 8 (`assembled`) are mechanical and resume autonomously.

### Iteration time budget

- Most iterations: 30-90 min
- `draft` stage iterations: up to 2 hours (longest)
- `code-check` and state-update iterations: 5-15 min

If an iteration exceeds 3 hours, the loop should checkpoint partial progress and stop. Hard cap.

---

## §3. State file format

`docs/book-update-plan/state.yaml`:

```yaml
schema-version: "1.0"
last-iteration: 2026-04-26T14:00:00Z
last-iteration-id: "iter-0042"
last-commit: "<sha>"

# Priority order — loop processes these in order; can be re-ordered between
# iterations if priorities shift
priority-order:
  - 48-key-loss-recovery       # Most common P7 failure mode; highest user value
  - 43-performance-contracts   # Most common P1 critique; bar to clear
  - 45-collaborator-revocation # Departing-employee scenario; common
  - 11-fleet-management        # Required for Sunfish at scale
  - 47-endpoint-compromise     # Honest threat model for Volume 1
  - 46-forward-secrecy         # Currently assumed; should be explicit
  - 9-chain-of-custody         # Multi-party signed transfer
  - 12-privacy-aggregation     # DP at relay
  - 10-data-class-escalation   # Event-triggered re-classification
  - 44-per-data-class-device-distribution  # Smaller scope; can be quick

# Current state per extension
extensions:
  48-key-loss-recovery:
    status: in-progress
    current-stage: draft
    target-chapter: ch15-security-architecture
    target-sections: [Ch15 §"Key recovery", Ch20 §"Recovery UX"]
    estimated-words: 3000
    started: 2026-04-26T08:00:00Z
    history:
      - {stage: outline, completed: 2026-04-26T08:30:00Z, commit: "abc123"}
      - {stage: draft, in-progress-since: 2026-04-26T09:00:00Z}

  43-performance-contracts:
    status: not-started
    target-chapter: ch11-node-architecture
    target-sections: [Ch11 §"Performance contracts", Ch20 §"Performance UX"]
    estimated-words: 2500

  # ... 8 more extensions

# Iterations history (last 10)
iterations:
  - id: iter-0042
    timestamp: 2026-04-26T14:00:00Z
    extension: 48-key-loss-recovery
    stage-from: outline
    stage-to: draft
    duration-min: 65
    commit: "abc123"
    notes: "Drafted Ch15 new section §Key recovery. 1800 words. Used @chapter-drafter."
  - id: iter-0041
    # ...

# Quality gates passed per extension (true if last passing review)
quality-gates:
  48-key-loss-recovery:
    code-check: null    # not yet reached
    technical-review: null
    prose-review: null
    voice-check: null
    approved: false

# Kill triggers — set to true to stop the loop on next iteration
kill-triggers:
  user-pause: false      # User can flip to true to pause loop
  budget-exceeded: false # Set if total iterations exceed budget
  quality-regression: false  # Set if 3 consecutive iterations fail review
  stuck-on-stage: null   # Extension-id if stuck >5 iterations on same stage
```

The loop reads this file at the start of every iteration and writes it at the end.

---

## §4. Per-extension specification

Detailed spec per extension to guide drafting. Loop reads the relevant entry when starting work on an extension.

### 48 — Key-loss recovery (HIGH priority)

**Why first:** Most common P7 failure mode in real-world local-first deployments. Affects every consumer scenario. Without this, P7 promise breaks at first password forgotten / device lost / death without succession.

**Target chapter:** Ch15 (security-architecture) primary; Ch20 (UX) for recovery flows.

**Target chapter sections (NEW):**
- Ch15 § "Key-loss recovery" (~2000 words)
- Ch20 § "Recovery UX" (~1000 words)

**Outline:**

Ch15 new section:
- Why this matters (P7 doesn't deliver if keys lost)
- Six recovery mechanisms (per design-decisions.md §5 sub-patterns 48a-48f):
  - 48a Multi-sig social recovery for individuals (3-of-5 trustees, time-locked)
  - 48b Custodian-held backup key (institutional with attestation)
  - 48c Paper-key fallback (printed recovery phrase, offline storage)
  - 48d Biometric-derived secondary key
  - 48e Timed recovery with grace period
  - 48f Recovery-event audit trail
- Threat model (recovery-as-attack-vector — defending against adversary using recovery to take over)
- Recommended deployment combinations per use case (consumer, SMB, regulated)
- Cross-references to #32 (succession) and #18 (delegated capability)

Ch20 new section:
- First-run UX prompt for setting up recovery
- Trustee designation flow (for multi-sig social recovery)
- Recovery initiation UX (when user actually loses keys)
- Time-locked grace period UX (notifications to original holder)
- Recovery completion confirmation

**Code-check requirements:** Reference Sunfish.Foundation.Recovery.* namespaces by name only; mark as illustrative.

**Technical-review focus:** Verify multi-sig social recovery threshold logic (3-of-5 vs 2-of-3 tradeoffs) is correct; verify time-lock attack model.

**Prose-review focus:** Active voice; no hedging on recovery guarantees; honest about limitations (recovery requires pre-arrangement; lost keys without pre-arrangement = lost data).

**Voice-check (human):** Add a personal anecdote about key loss (lost crypto-wallet seed, forgotten password recovery, family member death without password handoff) — relatable + sets emotional context.

**Word count target:** 3000 words across both sections.

---

### 43 — Performance contracts (HIGH priority)

**Why second:** Most common reason "local-first feels slow" critique lands. Performance bar Sunfish must clear vs. Linear/Notion/Figma is real and measurable.

**Target chapter:** Ch11 (node architecture) primary; Ch20 (UX) for measurement and progressive degradation.

**Target chapter sections (NEW):**
- Ch11 § "Performance contracts and main-thread isolation" (~1500 words)
- Ch20 § "Performance budgets and progressive degradation" (~1000 words)

**Outline:**

Ch11 new section:
- Why this matters (P1 without budgets is just aspiration)
- Universal "no operation blocks the UI thread" rule
- Per-operation latency budgets (writes <16ms, reads <Yms, sync <Zms) — different per deployment class
- Main-thread isolation guarantee (heavy work to background thread / web worker)
- Measurable conformance test in CI
- Real-world stress: CRDT merge on 100k-op documents takes seconds; cannot freeze UI
- Per-deployment-class calibration (gaming budget != document editing budget != email budget)
- Reference Sunfish.Kernel.Performance.* abstractions

Ch20 new section:
- Progressive-degradation UX (when operation needs time, show partial results, completion indicator, cancellable)
- Performance budget violation surfacing (telemetry, dashboards, dev tooling)
- User-visible quality-of-service indicators (sync state UX touches this)

**Word count target:** 2500 words across both sections.

---

### 45 — Collaborator revocation (HIGH priority)

**Why third:** Departing-employee scenario is universal. Current book assumes collaborators stay collaborative.

**Target chapter:** Ch15 + Ch20

**Target chapter sections (NEW):**
- Ch15 § "Collaborator revocation and post-departure partition" (~2000 words)
- Ch20 § "Revocation UX" (~800 words)

**Outline:** Per design-decisions.md §5 sub-patterns 45a-45f.

**Word count target:** 2800 words.

---

### 11 — Fleet management

**Target chapter:** New Ch21 OR new Appendix G.

**Decision deferred to first outline iteration:** Loop must decide based on word count + topic cohesion whether this is a chapter or an appendix.

**Outline candidates:** Ch21 "Operational concerns" combining fleet mgmt + chain-of-custody (#9) + privacy aggregation (#12) + performance contracts (#43) operational angles. OR keep separate as App G "Fleet management" only.

**Word count target:** 5000-8000 words (largest extension).

---

### 47 — Endpoint-compromise threat model

**Target chapter:** Ch15 + App B (new threat-actor entry)

**Target chapter sections (NEW):**
- Ch15 § "Endpoint compromise: what stays protected" (~1500 words)
- App B new actor "THREAT-10 Compromised endpoint" (~500 words)

**Outline:** Per design-decisions.md §5 sub-patterns 47a-47f.

**Word count target:** 2000 words.

---

### 46 — Forward secrecy + post-compromise security

**Target chapter:** Ch15

**Target chapter sections (NEW):**
- Ch15 § "Forward secrecy and post-compromise security" (~1500 words)

**Outline:** Per design-decisions.md §5 sub-patterns 46a-46e. Reference Signal protocol family explicitly.

**Word count target:** 1500 words.

---

### 9 — Chain-of-custody

**Target chapter:** Ch15 + App B

**Target chapter sections (NEW):**
- Ch15 § "Chain-of-custody for multi-party transfers" (~2000 words)
- App B template "Chain-of-custody worksheet" (~500 words)

**Outline:** Per design-decisions.md §5 sub-patterns 9a-9c (covered in primitive #9 entry).

**Word count target:** 2500 words.

---

### 12 — Privacy-preserving aggregation

**Target chapter:** Ch15 + possibly new App G

**Target chapter sections (NEW):**
- Ch15 § "Privacy-preserving aggregation at relay" (~1500 words)

**Outline:** DP, k-anonymity, l-diversity at relay-side aggregation. Reference smart-meter scenario explicitly.

**Word count target:** 1500 words.

---

### 10 — Data-class escalation

**Target chapter:** Ch20 + Ch15

**Target chapter sections (NEW):**
- Ch20 § "Data-class escalation UX" (~1000 words)
- Ch15 § "Event-triggered re-classification" (~1000 words)

**Outline:** Reference commercial-driver dashcam scenario — routine vs. incident-class footage.

**Word count target:** 2000 words.

---

### 44 — Per-data-class device-distribution policy

**Target chapter:** Ch16 (persistence)

**Target chapter sections (NEW):**
- Ch16 § "Per-data-class device-distribution" (~1500 words)

**Outline:** Per design-decisions.md §5 sub-patterns 44a-44e. Treat intentional locality as first-class.

**Word count target:** 1500 words.

---

## §5. Quality gates

Before advancing an extension to next stage, the loop verifies the gate criteria:

| Stage | Gate criteria |
|---|---|
| `outline → draft` | Outline has all section headers + bullet points; word count target estimated; subagent prompt prepared |
| `draft → code-check` | Draft committed to chapter file; word count within ±20% of target; all section headers present |
| `code-check → technical-review` | All Sunfish package references validated as real; code snippets marked illustrative or compile; no `<!-- TBD -->` markers |
| `technical-review → prose-review` | @technical-reviewer issued report; all `<!-- CLAIM: source? -->` markers resolved; technical claims trace to v13/v5 |
| `prose-review → voice-check` | @prose-reviewer + @style-enforcer passes applied; no academic scaffolding; no there-is constructions; active voice; QC checklist passes |
| `voice-check → approved` | **HUMAN ONLY** — anecdote added; connective tissue present; reads as authored not assembled; loop stops here |
| `approved → assembled` | Marked approved in state; will be picked up by next ASSEMBLY.md run |

If a gate fails, the loop:
1. Records failure in state.yaml `quality-gates`
2. Goes back to the previous stage
3. Records this in iterations history
4. If 3 consecutive failures on same gate → set `kill-triggers.quality-regression = true` and stop

---

## §6. Kill triggers

The loop checks these at the start of every iteration. If ANY are true, the loop stops cleanly (commits state file, exits):

| Trigger | When it fires |
|---|---|
| `user-pause` | User manually sets to true to pause loop |
| `budget-exceeded` | Total iterations exceed 100 (safety cap; ~300 hours of work) |
| `quality-regression` | 3 consecutive iterations fail same gate |
| `stuck-on-stage` | One extension stays on same stage for >5 iterations |
| `git-conflict` | Loop's commit conflicts with concurrent edits (rare; signal to manual reconciliation) |
| `subagent-failure` | Critical subagent (chapter-drafter, technical-reviewer, prose-reviewer) fails twice in same iteration |

When a kill trigger fires, the loop writes a `STOPPED.md` file in this directory with:
- Trigger that fired
- Last successful iteration
- Recommended human action

---

## §7. Success criteria

The loop is COMPLETE when:

- All 10 extensions are at stage `assembled`
- Total word count added to book: 25-50k (within 80-120% of estimate)
- All chapters affected pass QC checklist (per CLAUDE.md project instructions)
- ASSEMBLY.md updated and full draft PDF builds successfully
- Conformance scan against `inverted-stack-conformance` skill shows the new primitives are now in the catalog (re-extraction picks them up)

Partial completion is acceptable — the loop can stop at any time and resume later. No "all-or-nothing" requirement.

---

## §8. Coordination with other sessions

This loop session edits BOOK CHAPTERS in `chapters/`. To avoid conflicts:

- The loop does NOT modify `docs/`, `.claude/`, `build/`, or `source/`
- The loop does NOT modify other concurrent work (this repo is single-user; risk is low)
- If the loop's commit conflicts with concurrent edits in same chapter, kill trigger fires
- Loop commits go to `main` directly (per project conventions); no PR required

If you want to manually edit a chapter while the loop is running:
1. Set `kill-triggers.user-pause = true` in `state.yaml`
2. Wait for current iteration to complete (it will see the trigger and stop)
3. Make your edits + commit
4. Set `kill-triggers.user-pause = false`
5. Loop resumes on next scheduled fire

---

## §9. The loop prompt (paste-ready)

Open a new Claude Code session in this repo (`C:/Projects/the-inverted-stack`) and paste:

```
/loop You are executing the Book Update Loop Plan at
docs/book-update-plan/loop-plan.md.

Read these files in order:
1. docs/book-update-plan/loop-plan.md (this plan; full content)
2. docs/book-update-plan/state.yaml (current state; create if missing using the
   schema in §3 of the plan)
3. CLAUDE.md (project instructions for the book; voice, ICM workflow, QC)

Then execute ONE iteration per the protocol in §2:

1. Check kill-triggers in state.yaml; if any are true, stop with a message
   explaining which trigger fired
2. Determine the next action:
   - If no extension is in-progress, start the next one in priority-order
     (move it to status: in-progress, current-stage: outline)
   - Otherwise, advance the in-progress extension to the next ICM stage
3. Execute that stage per the per-extension spec in §4 of the plan, using the
   appropriate subagent (per the stage table in §2)
4. Verify the quality gate per §5 BEFORE advancing the state
5. Update state.yaml with the new stage + commit SHA + iteration history entry
6. Commit the work (chapter edit + state file in single commit). Commit message
   format: "draft(book-update-loop): iter-NNNN — <extension-id> <stage-from> →
   <stage-to>"
7. Report in 2-3 sentences what was done and what's next
8. Stop (the next iteration fires on the loop's schedule)

Hard rules:
- ONE iteration advances ONE extension by ONE stage. Do not chain multiple
  stages in one iteration.
- ONE iteration time budget: 3 hours hard cap. If approaching, checkpoint
  partial progress and stop.
- If you are at stage voice-check, the loop STOPS — voice-check is human-only
  per the plan. Set status: awaiting-voice-check and stop with a message asking
  the user to do the voice pass.
- If a subagent invocation fails, retry once. If it fails again, set
  kill-triggers.subagent-failure = true and stop.
- ALL changes must respect CLAUDE.md project conventions (voice, IEEE
  citations, QC checklist, ICM stage labels via PR comments or commit messages).

Self-pacing: choose your next firing delay based on what you just did.
- After draft stage (longest): allow 1-2 hours before next fire (let context
  cache cool; allow user review)
- After review/style stages: 30 min before next fire
- After state-only updates: 5 min before next fire
- After hitting voice-check or kill trigger: do not schedule next fire
```

---

## §10. Initial state file

When the loop first runs, it should create `docs/book-update-plan/state.yaml` with the schema in §3, populated with the priority-order from §1 and `status: not-started` for all 10 extensions.

The loop's first iteration will:
1. Create state.yaml
2. Pick `48-key-loss-recovery` (first in priority-order)
3. Set its status to `in-progress`, current-stage to `outline`
4. Execute the outline action (read Ch15 + design-decisions §5 entry #48 + write outline file)
5. Commit + update state + report + stop

---

## §11. Estimated total work

- 10 extensions × ~6 ICM stages each (skipping voice-check) = ~60 autonomous iterations
- Plus ~10 voice-check stops requiring human attention (one per extension)
- Plus ~10 final approved-state iterations (mechanical)

Total: ~70 iterations, weighted by stage:
- Most iterations: 30-90 min
- Draft iterations (10 of them, one per extension): 1-2 hours
- Total wall-clock: ~50-150 hours of loop work
- Total calendar time: depends on loop firing cadence; if firing every 1-2 hours, ~2-3 weeks of running; if firing every 4-6 hours, ~1-2 months

Plus ~10 hours of human voice-check time spread across the project.

---

## §12. Plan maintenance

This plan is **live**. Update when:

- Priority order shifts based on user feedback or implementation experience
- An extension turns out to need a different chapter target than initially specified
- A new sub-pattern surfaces during drafting that warrants its own outline entry
- A kill trigger fires and the resolution requires plan changes

The state.yaml is OPERATIONAL state; the loop-plan.md is DECISIONS state. State.yaml is updated every iteration; loop-plan.md is updated only when decisions change.
