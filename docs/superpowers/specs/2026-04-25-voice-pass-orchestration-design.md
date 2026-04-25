# Voice-pass Orchestration for the Entire Book — Design

**Status:** Amended after council review (fb88cf9 → A-grade target)
**Author:** Chris Wood (with Claude)
**Date:** 2026-04-25
**Scope:** Full manuscript — preface, ch01–ch20, epilogue, appendices A–F (F is new)
**Quality target:** Universal Planning Framework A-grade after Stage 1.5 hardening
**Council review:** `2026-04-25-voice-pass-orchestration-design.council-review.md` (B1–B5, C1–C18)
**Pinned tooling:** Claude Code CLI as installed at session start; model `claude-sonnet-4-6` for voice agents (per agent file `model:` field). Recorded in each phase commit message.

---

## 1. Context and Why

The Inverted Stack manuscript has been through technical review, prose review, and multiple literary-board cycles. A reader of the voice-passed Ch01 (`chapters/_voice-drafts/final/ch01-when-saas-fights-reality.md`) reported the prose reads as "too mechanical" and "an aggressive stream of details that becomes fatiguing." A specific paragraph (Ch01 ¶73) enumerates 27 jurisdictions in 285 words — a pattern that repeats in 24 chapters and that fights the reader and the audiobook listener equally hard.

The work has three intertwined problems, not one:

1. **Voice-sinek tunes too mechanical at chapter scale** — the agent was calibrated on a 3-paragraph example and applied unmodified to 5,000+ word chapters. The "restate 2–3 times" and "end on moral statement" rules compound across many sections into constant emphatic-declaration cadence with no narrative breath.
2. **Source prose itself is over-stuffed**, especially regulatory enumerations added during literary-board cycles to address regional-market reviewers.
3. **Voice-pass orchestration for the whole book has not been validated** — only Ch01 has been through both passes; the workflow, the tier choices, and the per-chapter voice mapping are untested at scale.

All three feed the same root failure: **information density that defeats narrative flow**. Audiobook makes it worse — the listener cannot skim.

**Why this plan now:** the manuscript is structurally complete and approaches publication. Voice-pass-driven editorial work is the last major editorial pass before promotion-to-publish. Doing it well makes the difference between a tight book and a fatiguing one.

---

## 2. Success Criteria

### End-state deliverables

A manuscript on `main` where:

1. **Regulatory enumerations live in references, not inline prose.** A new Appendix F — Regulatory Coverage Map holds the full table; chapters cite it with one canonical example per claim and a pointer.
2. **Composite-character device is named openly in two places** — an expansive Sinek-voice paragraph in the Preface, and a short factual note under the Council framing heading at the start of Part II.
3. **Voice-sinek is tuned for chapter-scale prose** — calibration test relaxed from per-section to per-chapter; scene-preservation rule added; audiobook-cadence rule added; register variation between scene/exposition allowed; Preface paragraph added as a second canonical example.
4. **All six voice agents have been audited and tuned where needed** for chapter-scale work.
5. **All chapters have been voice-passed** with appropriate guest voice (pass-1) and Sinek polish or normalize (pass-2), and promoted from `_voice-drafts/final/` into `chapters/<part>/<ch>.md` on `main`.
6. **Style guide updated with King's influence** (10% revision cut, adverb discipline, trust-the-reader). *(Done in this session.)*

### Binary FAILED conditions

The plan has failed if **any** of these are true after Phase 4:

| # | Condition | Detection |
|---|---|---|
| F1 | Fewer than 3 of 4 Phase 2 pilots PASS on first run after Phase 1 retune | Manual pilot review |
| F2 | Audiobook spot-check produces listener-fatigue verdict at 1.0× playback for any pilot chapter | `build/audiobook.py` then listen |
| F3 | Phase 3 orchestrator FAIL rate >25% on first run | Orchestrator output |
| F4 | Post-promotion `make draft-pdf`, `make epub`, or audiobook build fails | Build script exit code |
| F5 | Post-promotion `make word-count` shows any chapter outside ±10% of target | `make word-count` |
| F6 | Reference-integrity script reports any jurisdiction removed from inline prose without a corresponding Appendix F entry | Custom script |

### Out of scope

- Rewriting any chapter's argument
- Changing the table of contents
- Touching the Sunfish reference repo
- Retiring the literary-board cycle (it remains available as a post-completion option)
- Parallelizing the orchestrator (serial runs are acceptable for the planned timeline)

---

## 3. Assumptions and Validation

| # | Assumption | Validated by | Impact if wrong |
|---|---|---|---|
| A1 | Voice-sinek's mechanical feel comes from the calibration-test rules (restate 2–3×, end on moral) | Phase 2 Ch01 pilot — diff against current `_voice-drafts/final/ch01` | Hypothesis is wrong; root cause is elsewhere (probably the rule that demands ≥2 short ≤8-word sentences). Iterate Phase 1 with a different rule loosening |
| A2 | Loosening Sinek won't lose voice fidelity | Phase 2 pilot reading — does it still sound like Sinek? | If too loose, tighten specific rules in Phase 1 retune. Two-knob problem (mechanical ↔ voiceless); finding the middle is the work |
| A3 | Guest voice agents have analogous chapter-scale risks | Phase 1 audit + Phase 2 separate reading of pass-1 outputs | If a guest voice doesn't have the problem, leave it alone — per-agent decisions, not one-size-fits-all |
| A4 | Polish vs. normalize tier is a useful distinction | Phase 2 Ch01 (polish) vs. Ch11 (normalize) read against each other | If output is indistinguishable, collapse to one mode and simplify the orchestrator |
| A5 | Regulatory enumerations can be compressed without losing literary-board-required coverage | Phase 0 manual review against original board feedback | If a board-required jurisdiction can't be compressed, keep it inline as a documented exception |
| A6 | The reader who flagged Ch01 represents the broader audience | External — get a second reader on the Ch01 pilot output if possible | If the second reader disagrees, the plan still helps (tighter book regardless) but urgency drops |
| A7 | Voice-pass actually improves the book vs. just changing it | Phase 2 — if the four pilots don't read better than their sources, the whole effort is in question | F1 fires; fall back to Alternative A (Phase 0 only) |
| A8 | "24 chapters affected by enumeration density" is correct | Phase 0a — when sweeping, confirm or adjust the count | Scope estimate adjusts; recipe stays the same |
| A9 | We are operating without prior art on AI-assisted prose voice-tuning iteration counts (C18). The "two retune rounds" cap in §7 is a judgement call, not an empirically supported number | External — none found at spec-writing time; if discovered later, fold into §3 | Cap may be too tight or too loose; revise based on Phase 2 evidence |
| A10 | **Determinism stance** (C5): voice-pass is non-deterministic. Each chapter is voice-passed exactly **once per agent revision**. Re-running is a deliberate retune cycle, not a refresh. The canonical artefact is the *promoted* one; intermediate drafts are advisory. If a re-run looks better than the promoted version, the next *agent revision* incorporates the lesson — we do not swap promoted output for re-run output without re-promoting through Phase 4 | Phase 4 manifest verification | If violated, manuscript drifts silently across re-runs |

### Confidence Level per phase

| Phase | Confidence | Reasoning |
|---|---|---|
| 0 — Source cleanup | **High** | Pure editorial work; tool support via `make word-count` and grep; reversible |
| 1 — Agent tuning | **Medium** | Two-knob problem; probably solvable, possibly needs iteration |
| 2 — Pilot | **Medium** | Pilot is the validation step; outcome unknown by design |
| 3 — Full orchestration | **High if Phase 2 PASSes**, otherwise plan in retune | Orchestrator is proven (Ch01 ran successfully); scaling is mechanical |
| 4 — Promotion | **High** | Per-chapter promote/reject decision is fully under user control |

---

## 4. Phases

Five phases, each with a binary PASS/FAIL gate before the next starts. Each phase boundary is a git commit.

### Phase 0 — Source cleanup (editorial; no orchestration)

Operates directly on `chapters/<part>/<ch>.md` files on `main`. Five workstreams. **The first is a timing pilot** — do not sweep all 24 chapters before measuring real per-chapter effort.

#### 0.0. Timing pilot (C13/B4)

Pick **two** chapters from the audit — one HIGH-severity (e.g., Ch01 ¶73) and one MED-severity. Run the compression recipe on both. **Record actual hours spent.** Project total Phase 0 effort:

- If projection is within the original 24–48h estimate: continue Phase 0 sweep.
- If projection is 50–100h: pause and decide. Continue (accept calendar) or invoke **Alternative A** (Phase 0 only — no voice-pass).
- If projection is >100h: invoke Alternative B (professional copyeditor) or Alternative A.

This gate fires **before** the full Phase 0 sweep. Two-chapter sample beats one-chapter assumption.

#### 0a. Regulatory enumeration audit and compression

The audit has already been run; results are in `docs/superpowers/specs/2026-04-25-voice-pass-orchestration-audit.md` — 24 affected chapters, with per-paragraph severity tier (HIGH/MED/TABLE) and word counts.

For each **HIGH-severity** paragraph (≥10 jurisdictions in dense prose), apply the compression recipe:

1. Identify the **chapter-anchor jurisdiction** — the one most relevant to the chapter's argument (e.g., GDPR/Schrems II for an EU compliance paragraph; DIFC for a UAE financial-services paragraph). If literary-board feedback specifically requested a jurisdiction for that chapter, that one is the anchor.
2. Identify any **specifically-board-flagged jurisdictions** for that chapter that aren't the anchor — these stay inline as a short series of two or three.
3. Lift all other jurisdictions to **Appendix F — Regulatory Coverage Map**, indexed by chapter and topic.
4. Replace the inline enumeration with: anchor + short series + reference pointer. Pattern:
   > "The EU's Schrems II ruling, India's DPDP Act, and the UAE's DIFC DPL 2020 are representative; the full regulatory-coverage table for this chapter is in Appendix F."
5. Verify the paragraph still reads as one argument, not two — if compression breaks the argument, split into two paragraphs.

For **MED-severity** paragraphs (4–9 jurisdictions): same recipe, less aggressive — keep up to four inline if they're a short series; lift the rest.

For **TABLE-tier** paragraphs (mostly appendix-b): leave as-is unless the table has fewer than 5 rows of data, in which case consider prose.

**Where literary-board feedback lives:** check `.wolf/memory.md` entries dated 2026-04-24 for the literary-board pass-1 resolution work, where regional-market reviewers' specific jurisdiction asks were itemized per chapter. Those are the asks that survive inline.

#### 0b. Create Appendix F — Regulatory Coverage Map

Single appendix that holds the full jurisdiction × framework × applies-to-which-chapter table. Built once from the existing inline enumerations so nothing is lost.

#### 0c. Composite-character disclosures

Two insertions:

- **Preface** — the Sinek-voice paragraph: *"We invented the people. We did not invent the objections. Five composite characters — each a faithful stand-in for a domain that had every reason to dismantle this architecture — read the paper twice. What broke, broke for real reasons. What changed, changed because the reasons were good."*
- **Top of Ch05** (or new Part II preamble file — implementer chooses) — the short factual note: *"A note on the council: The five members are composite characters — fictional practitioners constructed to embody real domains and real objections. The objections are real. The names are not."*

#### 0d. Style guide update — DONE

Already completed in design session: King's influence added to `docs/style/style-guide.md` (10% cut, adverb discipline, trust the reader). Phase 1 voice agents will reference this.

#### Gate

- All 24 affected chapters compressed
- Appendix F exists; reference-integrity script reports zero orphans
- Both disclosures present
- `make word-count` shows every chapter still within ±10% of target
- Phase 0 commit message records actual hours spent vs. projected (per C13)

### Phase 0.5 — Methodology check (NEW; C16/B5)

**This is the load-bearing methodology test the council flagged.** It fires after Phase 0 has cleaned up Ch01 (so the comparison is against cleaned source, not stale source). Cost: ~1 hour.

#### Procedure

1. Re-run Gladwell pass-1 only on the cleaned Ch01: `python build/voice-pass.py --only ch01 --pass 1 --force`. Output lands in `_voice-drafts/pass1/ch01-when-saas-fights-reality.md`.
2. Read three versions in sequence:
   - The cleaned source `chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md`
   - The new pass-1 `_voice-drafts/pass1/ch01-when-saas-fights-reality.md` (Gladwell only, no Sinek)
   - The current pass-2 `_voice-drafts/final/ch01-when-saas-fights-reality.md` (the existing Gladwell→Sinek output that was flagged as mechanical)
3. Decide: which reads best? Specifically — does pass-1 (raw Gladwell, no Sinek polish) read better than pass-2?

#### Decision matrix

| Pass-1 (Gladwell-only) reads… | Decision | Phase 1 scope |
|---|---|---|
| Better than current pass-2 | **Drop pass-2 for guest-voiced chapters.** The mechanical feel was Sinek over-rewriting. Voice-plan.yaml updated so guest-voice chapters end at pass-1 | Phase 1 collapses: only tune Sinek for chapters mapped to sinek-direct (16 chapters); guest agents need only the Phase 1 audit (no tuning) |
| About the same | **Light Sinek tune only.** The polish/normalize tier may not be needed | Phase 1 reduced: relax Sinek calibration without adding new modes |
| Worse than pass-2 (or worse than source) | **Original plan stands.** Tune all six agents; introduce polish/normalize tiers | Phase 1 unchanged |

#### Gate

- Decision recorded in `.wolf/cerebrum.md` `## Key Learnings` with reasoning
- Phase 1 scope confirmed before any agent file edits

### Phase 1 — Voice-agent tuning

**Pre-step (C2/B1) — mirror agent files into the manuscript repo.** Before any tuning, copy `~/.claude/agents/voice-*.md` to `agents/voice-*.md` in this repo. Update `build/voice-pass.py` so the prompt references `agents/voice-{voice}.md` instead of `~/.claude/agents/voice-{voice}.md`. The user-scope copy becomes a convenience mirror; the in-repo copy is the source of truth. From this point forward, all agent edits are made in `agents/` and committed alongside the chapters that result.

**Pre-step (C10) — agent-prompt restriction.** Voice agents must not reference any file under `source/` (the gitignored confidential papers). Add an explicit prohibition to each agent file's "What you do not do" section: *"You do not read, reference, or quote files under `source/`. Chapter content is the only authorised input."*

Then for voice-sinek specifically:

- Calibration test #2 (restate 2–3 times) reframed from per-section to **per-chapter** scope.
- New rule: **scene preservation** — when source paragraph is a narrative scene (named person, time, place), do not apply restatement-loop or moral-statement-ending techniques.
- New rule: **audiobook cadence** — no inline enumerations longer than three items; lift longer lists to a sentence break or to a referenced footnote.
- New rule: **register variation** — explicitly call out that scene, exposition, and argument should sound different; permission to leave well-written passages alone.
- New rule: **10% cut** — after rewriting, make a pass that cuts 10%. Borrowed from style-guide update in Phase 0d.
- Add a second canonical example: the Preface composite-character paragraph, demonstrating Sinek voice at chapter-opening register.

For each guest agent (gladwell, brown, grant, godin, lencioni): apply the same chapter-scale audit. The fixes are likely lighter than Sinek's. Per-agent decisions, not one-size-fits-all. **If Phase 0.5 returned "drop pass-2 for guest-voiced chapters," the audit becomes informational only — guest agents are not edited.**

**Phase boundary archive (C7).** Before committing Phase 1 agent edits, archive `_voice-drafts/` to a timestamped subdirectory: `_voice-drafts/_archive/YYYY-MM-DD-HHmm-pre-phase1/`. Stale pass-1 outputs from earlier sessions otherwise poison the next pilot.

#### Gate

- All six agent files mirrored to `agents/` and committed in this repo
- Tuning edits committed; previous versions preserved in git history
- Source-prohibition rule present in all six agent files
- `python build/voice-pass.py --plan-only` parses cleanly against the new in-repo agent path
- Each agent reads cleanly to a human reviewer
- `_voice-drafts/` archived to timestamped subdir

### Phase 2 — Re-pilot on four archetypes

Run voice-pass against four deliberately-chosen pilots covering all four pipeline types:

- **Ch01** (gladwell → sinek-polish) — narrative-heavy; baseline to diff against current `_voice-drafts/final/ch01`
- **Ch11** (sinek-normalize direct) — spec chapter; pure house-voice test
- **Ch05** (lencioni → sinek-polish) — council fable; heaviest test of polish tier
- **Ch04** or **Ch17** (godin → sinek-polish) — decision-framework / manifesto register; least-validated voice

For each pilot, read **two** outputs:

- Pass-1 output (`_voice-drafts/pass1/<ch>.md`) — does the **guest voice** work on its own merits?
- Pass-2 output (`_voice-drafts/final/<ch>.md`) — did **Sinek** preserve what the guest voice did, or flatten it?

If a pilot reveals the wrong voice mapping, fix `voice-plan.yaml` rather than fight an agent.

Generate audiobook MP3 for ≥1 pilot chapter and listen at 1.0× — validates the audiobook-cadence rule.

**Retune loop pattern (C6).** When Phase 1 retune is needed mid-Phase 2, the supported re-run pattern is:
```
python build/voice-pass.py --only ch01 --pass 2 --force
```
This re-runs only pass-2 (Sinek) over the existing pass-1 cache. Pass-1 (the guest voice work) is preserved unless the guest agent itself was retuned, in which case use `--force` without `--pass 2` to redo both.

**External-reader gate (C17/A6).** At least one pilot — recommended: Ch01 — is reviewed by a non-author reader. Their PASS/FAIL is **binding**, not advisory. Author-fatigue can produce false-PASS verdicts after enough re-readings; the external read is the truth-gate.

#### Gate

- All four pilots PASS by user review
- ≥1 pilot PASSes by external reader (binding)
- Audiobook spot-check passes (no fatigue verdict)
- Specific notes captured per pilot for any FAIL
- `_voice-drafts/` archived to timestamped subdir before Phase 3 begins

### Phase 3 — Full orchestration run

**Code changes required first** (these belong inside Phase 3, not deferred):

- Add a third column to `chapters/voice-plan.yaml`: per-chapter pass-2 mode (`polish` or `normalize`). Current parser splits on `:` only — needs extension to parse `chapter: voice mode` or `chapter: voice` (mode defaults to `normalize` if absent for backward compat). **Skipped if Phase 0.5 returned "drop pass-2 for guest-voiced chapters."**
- Update `build/voice-pass.py` to read the mode and select the matching prompt variant for pass-2 (`build_prompt_polish` vs. existing `build_prompt`).
- Update `build/voice-pass.py` to read agent files from `agents/` in this repo, not `~/.claude/agents/` (per Phase 1 pre-step C2).
- Add `VALID_MODES = {"polish", "normalize"}` and warn on unknown modes.
- **Add per-invocation logging (C9/B3).** After each pass, write `_voice-drafts/_log/<UTC-timestamp>-<chapter>-pass<N>.json` containing: `input_sha256`, `output_sha256`, `agent_path`, `agent_sha256`, `claude_cli_version` (`claude --version`), `model_name`, `prompt_mode`, `exit_code`, `duration_seconds`, `wall_clock_start_iso`, `wall_clock_end_iso`. The log directory is gitignored along with the rest of `_voice-drafts/`; the per-promotion sidecar (Phase 4) lifts the relevant log entries into the repo.
- Decide whether Appendix F gets voice-passed at all — recommendation: **skip** (it's a coverage table, not prose). Add `appendix-f` to `voice-plan.yaml` with a `skip` voice marker or omit entirely.

Then run `python build/voice-pass.py --force` over the remaining ~23 chapters (27 total in plan minus 4 pilots already done). Review per-chapter OK/FAIL line; re-run any FAIL individually with `--only`.

**Source-edit ordering rule (C8).** Any edit to a chapter source under `chapters/<part>/` after Phase 3 has begun forces a re-run of voice-pass for that chapter. Detect via mtime comparison: if `chapters/<part>/<ch>.md` has mtime newer than `_voice-drafts/final/<ch>.md`, treat the draft as stale. Add an orchestrator check that warns on stale drafts before Phase 4.

#### Gate

- Every chapter has a fresh file in `_voice-drafts/final/`
- No FAIL lines outstanding after retries
- Spot-check N≥6 chapters across all four pipeline types

### Phase 4 — Promotion to `main`

Diff each `_voice-drafts/final/<ch>.md` against `chapters/<part>/<ch>.md`. For each chapter, decide PROMOTE or REJECT (keep source, log why). A small script or Make target automates the file copy + ICM marker update.

After promotion: run `make word-count`, `make draft-pdf`, `make epub`, and audiobook build to confirm no regressions.

**Sidecar manifest per promoted chapter (C3/B1).** For each PROMOTE, write `chapters/<part>/<ch>.manifest.json` containing the relevant Phase 3 log entry: `input_sha256` (the source at time of voice-pass), `output_sha256` (the voice-passed draft, which must match the bytes being promoted), `agent_path`, `agent_sha256`, `claude_cli_version`, `model_name`, `prompt_mode`, `wall_clock_start_iso`, `promoted_at_iso`, `promoter` (git user). Manifests are checked into the repo. They are the audit trail.

**Hash verification (C11).** Promotion script computes SHA-256 of `_voice-drafts/final/<ch>.md` and compares to the recorded `output_sha256` in the Phase 3 log. Mismatch halts that chapter's promotion — indicates the draft was modified post-pass (manual edit, partial overwrite, etc.). Recovery: re-run pass-2 with `--force --only`, or accept the manual edit by recomputing the hash and updating the log entry with `manual_edit: true`.

#### Gate

- All PROMOTE chapters merged on `main`, each with a sidecar manifest
- All hash verifications PASSed (or manual-edit-acknowledged)
- ICM markers advanced to `icm/voice-check`
- Build artifacts regenerate clean
- F1–F6 conditions all evaluated to PASS

**Note on counts:** "All 27 chapters" means everything in `voice-plan.yaml` after the parser update. Appendix F (the new coverage map) is excluded from voice-pass per Phase 3 decision above.

---

## 5. Verification

### Per-phase verification matrix

| Phase | Automated | Manual |
|---|---|---|
| 0.0 | Per-chapter timing recorded in Phase 0 commit | User decides continue / Alternative A / Alternative B based on projection |
| 0 | `make word-count` (±10% per chapter); `make lint` (cross-refs); reference-integrity script | User reads each compressed chapter for substantive completeness; reads Preface + Council disclosure in context; reads Appendix F end-to-end |
| 0.5 | Pass-1 re-run produces fresh `_voice-drafts/pass1/ch01.md` | User reads three Ch01 versions and decides Phase 1 scope per the decision matrix; decision recorded in `.wolf/cerebrum.md` |
| 1 | Frontmatter syntax check on each `agents/voice-*.md` file; `python build/voice-pass.py --plan-only` parses against in-repo agent path; source-prohibition rule grep-verifiable in each agent file | User reads diff for each tuned agent; confirms new rules don't contradict existing ones |
| 2 | Per-pilot orchestrator OK; both pass-1 and pass-2 files exist; word count ±10%; per-invocation log entries written | User reads pass-1 and pass-2 for each pilot; PASS/FAIL with notes; audiobook listen on ≥1 pilot; **external reader binding PASS on ≥1 pilot** |
| 3 | Per-chapter OK; word count check on every draft; all 27 chapters have fresh `_voice-drafts/final/` file; per-invocation log written; stale-draft warning shows zero chapters | Spot check N≥6 chapters across pipeline types |
| 4 | After promotion: `make word-count`, `make draft-pdf`, `make epub`, audiobook build; per-promotion sidecar manifest exists; SHA-256 hash verification PASS for every promoted chapter | Per-chapter PROMOTE/REJECT decision; ICM markers updated; uncertain chapters routed back through literary-board |

### Audiobook listener test

Generate audiobook MP3 for ≥1 pilot chapter and listen at 1.0× playback. Cadence is the rule most likely to fail silently — prose can read fine on the page and still fatigue when read aloud.

---

## 6. Rollback Strategy

| Phase | Reversibility | Mechanism |
|---|---|---|
| 0 — Source cleanup | Fully reversible | `git revert` Phase 0 commits |
| 1 — Agent tuning | Fully reversible | Agent files committed before edits; restore from git history |
| 2 — Pilots | No cleanup needed | Drafts in gitignored `_voice-drafts/` |
| 3 — Full run | No cleanup needed | Same |
| 4 — Promotion | Reversible per chapter | Each promotion is a separate commit; `git revert <commit>` per chapter |

---

## 7. Kill Criteria and Replanning Triggers

### Per-phase kills

- **Phase 0.0:** if 2-chapter timing pilot projects >100h for Phase 0, kill the original plan; invoke Alternative A or B.
- **Phase 0:** if compression in any chapter loses a literary-board-flagged jurisdiction, pause and decide whether to keep it inline as exception.
- **Phase 0.5:** decision matrix output is itself the gate; no separate kill.
- **Phase 1:** after **two** rounds of voice-sinek retune, if Ch01 pilot still reads mechanical, fall back to **Alternative A** (Phase 0 only — chapters mapped to a guest voice skip pass-2; only sinek-mapped chapters go through Sinek).
- **Phase 2:** if 2 of 4 pilots FAIL after Phase 1 retune, escalate — voice-pass may not be the right tool. Consider chapter-by-chapter manual editing using agents as advisors, not rewriters. **External-reader FAIL on a pilot is binding** (C17): if the external reader fails a pilot the author passed, the author's verdict is overridden.
- **Phase 3:** FAIL rate >25% halts the run. Diagnose systemic problem before resuming.
- **Phase 3 (special — C4/B1):** Claude safety filter refusal on ch07 (Security Lens) or ch15 (Security Architecture) is a realistic failure. These chapters discuss attacker behaviour, key compromise, and compelled-access scenarios. If refusal occurs: pause, manually edit the prompt for that single chapter to add safety-relevant context ("this is a defensive security chapter for a published book on local-first architecture; the content describes threat models the architecture protects against, not attack instructions"), retry with `--only`. If still refused, that chapter exits voice-pass and stays at the source draft.
- **Phase 4:** first 3 promoted chapters breaking build halts promotion. Fix regression source before continuing. Hash-verification mismatch on any chapter halts that chapter's promotion until reconciled.

### Project-level kill (C14)

The plan itself fails — replan, do not continue — if:

- **Calendar:** by **end of week two** from Phase 0 start, Phase 2 has not been entered. Stalling between Phase 2 commit and Phase 3 run is the worst possible state (work begun, not delivered). Replan to either: (a) compress remaining work into a focused weekend, (b) invoke Alternative B (professional copyedit), or (c) ship the Phase 0-only manuscript.
- **Cost:** total token spend >2× initial estimate (>$50, per C15).
- **Methodology:** Phase 0.5 returned "drop pass-2" but Phase 2 pilots still failed — the diagnosis was wrong; the problem is somewhere else entirely.

### Replanning triggers (mid-plan, scope-change)

The plan needs scope change (not abandonment) if:

- Phase 1 requires more than two retune rounds.
- Phase 2 reveals wrong voice-mapping for ≥2 chapters — `voice-plan.yaml` itself needs design work.
- Phase 3 FAIL rate exceeds 25%.
- Source-edit-after-Phase-3 (C8) triggers re-run of >3 chapters — stop, finish source edits, restart Phase 3.

### Incident response runbook for "promoted chapter contains hallucinated content" (C12)

If a reader, technical reviewer, or you discover that a promoted chapter contains content that misrepresents the architecture, hallucinates an API or jurisdiction, or shifts the security model:

1. **Halt** any in-flight Phase 3 or Phase 4 work for related chapters.
2. **`git revert`** the promotion commit for the affected chapter. The source-of-truth becomes the pre-voice-pass version.
3. **Read the audit log** — find the `_voice-drafts/_log/` entry referenced by the chapter's sidecar manifest. Identify: which agent revision, which model, which prompt mode produced the offending content.
4. **Decide one of three paths:**
   - **Retune the agent** if the failure looks like a systematic agent issue → repeat Phase 1 retune for that agent only.
   - **Run through literary-board agent** if the failure is content-substantive (a claim that should never have survived review) → re-cycle through `literary-board`.
   - **Manual edit + skip voice-pass** for that chapter if the failure is one-off → edit the source directly, mark in voice-plan.yaml as `skip` voice.
5. **Append the incident to `.wolf/buglog.json`** with full diagnostic chain.

---

## 8. Resume Protocol

The orchestrator already supports both knobs needed for resume:

- `--only <substring>` — retry a single chapter
- `--force` — overwrite an existing draft

Pass-1 outputs persist in `_voice-drafts/pass1/`, so if Sinek's tune changes mid-run, only pass-2 needs re-run for affected chapters.

Each phase boundary is a git commit. Resume from any phase boundary.

### Tool fallback

| Failure | Recovery |
|---|---|
| Claude CLI auth breaks | Reauth, resume with `--only` filter on un-processed chapters |
| Specific agent file missing/corrupt | Restore from git history; re-run with `--only` |
| Orchestrator script regression | `git checkout` prior version of `build/voice-pass.py`; re-run |
| Network outage mid-run | Single chapters that died re-run individually with `--force` |

---

## 9. Budget and Resources

### Time

- **Phase 0:** 1–2 hours per affected chapter for careful compression × 24 chapters = 24–48 hours of editorial work. Largest single time sink. Plus Appendix F creation (~4 hours) and disclosure inserts (~1 hour).
- **Phase 1:** 4–8 hours of agent tuning + review.
- **Phase 2:** ~1 hour per pilot for review × 4 pilots = 4 hours, plus audiobook listen (~1 hour for one chapter).
- **Phase 3:** 5–13 hours wall clock if serial; ~1 hour user time for review.
- **Phase 4:** 30 min per chapter for promote/reject decision × 27 chapters = ~14 hours.

**Total estimate:** 60–100 hours of focused work, calendar-spread across weeks.

### Tokens / cost

- 27 chapters × up to 2 passes = up to 54 Claude headless invocations per run.
- 12 guest-voice pass-1 + 27 pass-2 = 39 expected per run (or fewer if Phase 0.5 drops pass-2 for guest chapters).
- Each pass reads + writes 5,000–9,000 tokens of chapter; ~$0.30–0.50 per pass on Sonnet.
- **Per-run estimate: $15–25.**
- **Total budget across expected retunes (C15):** at most 2 Phase 3 runs (initial + one retune). Budget ceiling: **$30–50**. Matches the §7 stop-loss.

### Stop-loss

If cumulative token spend across all Phase 3 runs exceeds $50, pause and reassess. The retune budget is two runs; a third run requires explicit decision and a new budget.

### Tooling pin (C1)

Recorded once in spec frontmatter and re-recorded in each Phase 3 commit message:

```
Claude Code CLI: `claude --version` output captured at run-start
Model: claude-sonnet-4-6 (per agents/voice-*.md model: field)
```

If model version drifts mid-plan (Anthropic publishes a new Sonnet), pause and decide whether to re-pilot or pin to the prior version via the agent file's `model:` field.

---

## 10. Reference Library

**Source-paper prohibition (C10):** Voice agents must not read or reference any file under `source/`. The `source/` directory holds gitignored confidential papers (v13, v5, R1, R2). They are inputs to chapter-drafting, not to voice-pass. A voice agent that opens `source/local_node_saas_v13.md` during a pass leaks confidential content to the model provider via the rewrite prompt. Each voice agent file's "What you do not do" section enforces this prohibition.

| Resource | Path | Purpose |
|---|---|---|
| Voice agents (source of truth) | `agents/voice-{sinek,gladwell,brown,grant,godin,lencioni}.md` | The agents being tuned — mirrored into this repo per Phase 1 pre-step |
| Voice agents (user-scope mirror) | `~/.claude/agents/voice-*.md` | Convenience copy for direct `@voice-X` invocation; not the source of truth |
| Plan file | `chapters/voice-plan.yaml` | Chapter→voice mapping; gets a third column for polish/normalize mode |
| Orchestrator | `build/voice-pass.py` | Headless dispatch script |
| Drafts area | `chapters/_voice-drafts/{pass1,final}/` | Gitignored; voice-pass output lands here |
| Style guide | `docs/style/style-guide.md` | Updated in this session with King; agents reference it |
| Source paper | `source/local_node_saas_v13.md` | For technical accuracy when reviewing voice-passed chapters |
| Build targets | `build/Makefile` | `make word-count`, `make draft-pdf`, `make epub`, `make code-check` |
| Audiobook builder | `build/audiobook.py` | TTS pipeline; cadence verification |
| Existing Ch01 baseline | `chapters/_voice-drafts/final/ch01-when-saas-fights-reality.md` | Diff target for Phase 2 Ch01 pilot — proves whether tune helped |
| Council reviewer (for spec hardening) | `.claude/agents/council-reviewer` (or `literary-board`) | Adversarial review of this spec or chapters |

---

## 11. Knowledge Capture Protocol

Findings are routed into the OpenWolf system as follows.

After Phase 2 — append to `.wolf/cerebrum.md` `## Key Learnings`:

- What voice-sinek rule actually caused the mechanical feel (validates or refutes assumption A1).
- Which guest agents needed tuning vs. which were already chapter-scale-ready.
- Which polish/normalize tier assignments worked and which didn't.

After Phase 3 — append to `.wolf/buglog.json`:

- Any orchestrator failure modes encountered and their fixes.
- Any agent prompt regressions discovered.

After Phase 4 — append to `.wolf/memory.md`:

- Promote/reject ratio per chapter type (Part I narrative vs. Part III spec vs. Part IV playbook etc.).
- Any chapters requiring literary-board re-cycle.

---

## 12. Provenance and Reproducibility (NEW — addresses B1, B3)

The single largest unowned risk the council found: **the agent that voiced the book is not in the book's git history.** This section consolidates the artefacts required to make every voiced chapter reproducible from its commit.

### Artefacts and where they live

| Artefact | Repo path | Created by |
|---|---|---|
| Agent files (source of truth) | `agents/voice-*.md` | Phase 1 pre-step; mirrored from `~/.claude/agents/` |
| Per-invocation log | `_voice-drafts/_log/<UTC>-<chapter>-pass<N>.json` | `build/voice-pass.py` (gitignored — ephemeral) |
| Per-promotion sidecar manifest | `chapters/<part>/<ch>.manifest.json` | Phase 4 promotion script (committed — permanent) |
| Phase commit messages | git history | Each phase's commit; includes CLI version + model name |

### Manifest schema (the audit trail)

```json
{
  "chapter": "ch01-when-saas-fights-reality",
  "input_sha256": "<sha of chapters/<part>/<ch>.md at time of pass>",
  "output_sha256": "<sha of _voice-drafts/final/<ch>.md immediately after pass>",
  "promoted_sha256": "<sha of chapters/<part>/<ch>.md after promotion (must equal output_sha256)>",
  "agent_path": "agents/voice-sinek.md",
  "agent_sha256": "<sha of agent file at time of pass>",
  "claude_cli_version": "<output of claude --version>",
  "model_name": "claude-sonnet-4-6",
  "prompt_mode": "polish",
  "wall_clock_start_iso": "2026-05-02T14:23:11Z",
  "promoted_at_iso": "2026-05-02T15:08:42Z",
  "promoter": "Chris Wood <ctwoodwa@gmail.com>",
  "manual_edit": false
}
```

### Reproducibility procedure

To reproduce any promoted chapter from its manifest:

1. `git checkout` the commit that contains the manifest.
2. Read `chapters/<part>/<ch>.manifest.json`.
3. Restore the agent file from `agent_sha256` (`git show <sha>:agents/voice-X.md`).
4. Restore the source from `input_sha256`.
5. Install Claude Code CLI at the version recorded.
6. Run `python build/voice-pass.py --only <chapter> --force --pass <N>`.
7. Compare the resulting `output_sha256` to the manifest. Voice-pass is non-deterministic (per A10), so byte-exact reproduction is **not** the goal — the goal is forensic reconstruction of "what we ran." If the new output differs substantively, that is itself a finding (model drift).

### Enforcement

- Promotion script (Phase 4) **refuses to promote** without a valid log entry pointing to the matching `output_sha256`.
- Pre-commit hook on `chapters/<part>/<ch>.md` warns (does not block) if the file changes without a corresponding manifest update.

## 13. Post-Completion Plan

After Phase 4 promotion succeeds, the manuscript exits to one of three states:

- **Re-cycle through literary board** for any chapter where Phase 4 promote-vs-reject was uncertain. Use the existing `literary-board` agent.
- **Professional copyedit pass** as a final polish (Alternative B from Stage 0 — kept as post-completion option).
- **Ship.** No further structural review needed.

**Decision rule:** if ≥3 chapters required REJECT-and-keep-source in Phase 4, recycle through literary board first. Otherwise, decide between copyedit pass and ship based on calendar pressure.

---

## 14. Stage 0 — Alternatives Considered

| Alternative | Decision | Rationale |
|---|---|---|
| **A. Phase 0 only — no voice-pass** | **Held as escape hatch** | Skips voice-consistency work and the 6 agents already built; doesn't address part-by-part voice register. But Phase 0 has standalone value — if Phases 1–3 derail (kill criterion fires), Phase 0 alone may fix the original reader complaint about density |
| **B. Hire human copyeditor ($2–4k)** | **Held as post-completion option** | Copyeditors smooth; they don't voice. Book wants different registers in different parts — that's voice work. But a professional pass after voice-pass may be needed for final polish |
| **C. Do nothing — accept current draft** | **Rejected** | User identified the problem; audiobook makes it worse |
| **D. Voice-pass without source cleanup** | **Rejected** | Voice agents will not reliably compress 26-jurisdiction enumerations without dropping or hallucinating jurisdictions |

---

## 15. Open Decisions for Implementation

These are choices the implementation can resolve cold; flagging them so the writing-plans skill can sequence them properly:

- **D1.** Composite-character disclosure location: top of Ch05 vs. new Part II preamble file. Recommended: top of Ch05, no new file.
- **D2.** Appendix F format: single big table vs. per-chapter sub-tables. Recommended: per-chapter sub-tables for findability.
- **D3.** Voice-mapping changes from pilot findings: handled in Phase 2 if needed, not pre-committed.
- **D4.** Pilot 4 chapter: Ch04 vs. Ch17. Recommended: Ch04 (shorter feedback loop).
- **D5.** Phase 4 promotion: per-chapter manual decision vs. auto-promote-with-flagged-review. Recommended: manual for first pass; revisit if it becomes a bottleneck.

---

## Appendix — Universal Planning Framework checklist

| Section | Status |
|---|---|
| 5 CORE: Context & Why | ✅ §1 |
| 5 CORE: Success Criteria | ✅ §2 with binary FAILED conditions F1–F6 |
| 5 CORE: Assumptions & Validation | ✅ §3 with Confidence Levels (A1–A10) |
| 5 CORE: Phases | ✅ §4 with binary gates (Phase 0.0, 0, 0.5, 1, 2, 3, 4) |
| 5 CORE: Verification | ✅ §5 with audiobook listener test + external-reader gate |
| Stage 0: Discovery | ✅ §14 |
| Rollback Strategy | ✅ §6 |
| Risk / Kill Criteria | ✅ §7 with project-level kill, IR runbook |
| Resume Protocol + Tool Fallback | ✅ §8 |
| Budget & Resources | ✅ §9 with retune budget + tooling pin |
| Reference Library | ✅ §10 with source-paper prohibition |
| Knowledge Capture | ✅ §11 |
| Provenance & Reproducibility | ✅ §12 (added per council B1, B3) |
| Post-Completion Plan | ✅ §13 |
| Stage 1.5 Adversarial Hardening | ✅ council-review.md companion file; B1–B5/C1–C18 folded into spec |

### Council conditions resolution map

| Council ID | Resolved in |
|---|---|
| B1 / C1 / C2 / C3 | §12 Provenance; spec frontmatter; Phase 1 pre-step; Phase 4 sidecar |
| B2 / C5 / C6 / C7 / C8 | §3 A10; Phase 2 retune pattern; phase-boundary archive; Phase 3 ordering rule |
| B3 / C9 / C11 | Phase 3 logging; Phase 4 hash verification; §12 manifest schema |
| B4 / C13 / C14 / C15 | Phase 0.0 timing pilot; §7 project-level calendar kill; §9 retune budget |
| B5 / C16 / C17 / C18 | Phase 0.5 methodology check; §3 A9 prior-art note; Phase 2 external-reader gate |
| C4 | §7 Phase 3 Claude safety-filter kill |
| C10 | §10 source-paper prohibition + Phase 1 pre-step agent file rule |
| C12 | §7 Incident response runbook |
