KLEPPMANN COUNCIL REVIEW — Stage 1.5 Adversarial Hardening
Document: `docs/superpowers/specs/2026-04-25-voice-pass-orchestration-design.md`
Date: 2026-04-25
=====================================

> Note: this spec is an editorial-orchestration plan, not an architecture
> document. The five seats below score the *plan* against their domains —
> not the manuscript content — and translate their adversarial postures
> into concerns about plan completeness, failure mode coverage, and
> hidden assumptions. The voting rules and scoring scale are unchanged.

---

## SEAT 1 — Dr. Marguerite Voss (Plan-as-infrastructure)

DIMENSION SCORES
  D1 Tooling/dependency governance: 5 — "Claude CLI on PATH" is treated as an environmental constant; no version pin, no model-version pin, no behaviour-when-Anthropic-changes-Sonnet.
  D2 Deployment/promotion governance: 7 — Phase 4 has a per-chapter PROMOTE/REJECT gate, but no audit log of *which prompt + agent revision* produced each promoted artefact.
  D3 Supply-chain / SBOM analogue: 4 — agent files live in `~/.claude/agents/` (user-scope, outside the repo). Phase 1 commits "agent files updated and committed" but the spec never says *to which repo*. The artefact that produced the manuscript is not under the manuscript's version control.
  D4 Incident response: 6 — kill criteria exist per phase, but no rollback drill; the F4 "build fails" trigger lacks a step-by-step recovery, only "fix regression source."
  D5 Network/runtime policy: 6 — serial run is fine, but no statement on what happens if Claude rate-limits mid-run, returns truncated output, or refuses (safety filter on a security chapter, e.g. ch07/ch15).
  D6 Compliance/process pathway: 7 — ICM pipeline is referenced, but the spec does not say which ICM stage a voice-passed chapter sits at *before* promotion (still `icm/voice-check`? regressed from `icm/approved`?).
  D7 Author-as-helpdesk burden: 6 — 14 hours for promote/reject decisions is plausible only if diffs are small; spec doesn't budget the case where Sinek meaningfully restructures and the diff is 80% red.
  D8 Plan documentation quality: 8 — well-structured, traceable, UPF-compliant.

DOMAIN AVERAGE: 6.1 / 10

BLOCKING ISSUES
  B1: Agent files (`~/.claude/agents/voice-*.md`) are user-scope and not in this repo. Phase 1 says "previous versions preserved in git history" but does not specify *which* git history. If a future session's agent files drift, no one can reproduce the run. Provenance gap.

CONDITIONS
  C1: Pin Claude CLI version and model name in the spec; record them in each phase commit message.
  C2: Copy or symlink agent files into the manuscript repo (e.g. `agents/voice-*.md`) so the manuscript's git history *is* the agent history. Treat user-scope as a convenience mirror, not the source of truth.
  C3: For each promoted chapter, write a sidecar file (`chapters/_voice-drafts/manifest.json`) recording: source SHA, agent SHA, CLI version, model name, prompt mode, timestamp.
  C4: Add a kill criterion for "Claude safety filter refuses ch07 or ch15" — these chapters discuss attacker behaviour and key compromise; refusal is a realistic failure.

COMMENDATIONS
  ✓ §6 Rollback Strategy is per-phase and concrete.
  ✓ §8 Resume Protocol uses primitives (`--only`, `--force`) the orchestrator already supports.

VERDICT: PROCEED WITH CONDITIONS
The plan is well-structured but has a real provenance gap: the agent files that *produce* the manuscript are not versioned alongside the manuscript. C2 and C3 are the load-bearing fixes. Without them, "git revert per chapter" rolls back the prose but not the prompt that produced it — meaning a re-run is not actually reproducible.

---

## SEAT 2 — Prof. Dmitri Shevchenko (Plan-as-distributed-system)

DIMENSION SCORES
  D1 "Library" (agent) selection rationale: 7 — six voices are listed; rationale per voice is in `voice-plan.yaml` comments.
  D2 Convergence/idempotence: 4 — voice-pass is non-deterministic. The plan does not specify what happens if running pass-2 twice on the same input produces *different* outputs both within tolerance — which is the live release wins?
  D3 Conflict-resolution depth: 5 — Phase 4 "REJECT and keep source" is the conflict resolution between machine output and human judgement, but the spec doesn't say what happens to the *next* run's pass-1 input if pass-2 was rejected.
  D4 Protocol completeness: 6 — `--only` and `--force` are present; missing: a `--from-pass1` to re-run only pass-2 after a Sinek retune, which is exactly the Phase 1→2 iteration loop.
  D5 Lease/sequencing correctness: 8 — phase boundaries are git commits, gates are binary; no concurrent-writer hazard.
  D6 GC strategy for intermediate state: 5 — `_voice-drafts/{pass1,final}/` accumulates across runs; spec is silent on when to clean up. After three Phase 1 retunes, pass1/ contains stale outputs that look authoritative.
  D7 Causal ordering: 6 — Phase 0 (source edits) precedes Phase 2 (pilots), good. But if Phase 0 lands a fix to ch11 *after* Phase 3 has already drafted ch11, the orchestrator silently uses the new source — and the user doesn't know unless they inspect timestamps.
  D8 Adversarial scenario coverage: 5 — covers Claude auth break, agent corruption, network outage. Missing: silent agent regression (the agent runs but produces subtly worse output), partial-write (CLI exits 0 but output is truncated), and the "drift" scenario where successive re-runs slowly transform a chapter beyond recognition.

DOMAIN AVERAGE: 5.8 / 10

BLOCKING ISSUES
  B2: Non-determinism is unaddressed. Two pass-2 runs of the same input produce different prose. The spec treats voice-pass as if it were a pure function. It is not. The plan needs an explicit "the canonical artefact is the *promoted* one; intermediate drafts are advisory" statement, plus a rule for tie-breaking when a re-run looks better than the promoted version.

CONDITIONS
  C5: Specify a determinism stance: each chapter is voice-passed exactly once per Phase-1 agent revision; re-running is a deliberate retune cycle, not a refresh.
  C6: Add a `--from-pass1` switch (or document that `--pass 2 --force --only` is the supported pattern). The Phase 1→2 retune loop *will* hit this; if it isn't supported, users will manually delete files and lose pass-1 cache.
  C7: Add a GC step at each phase boundary: archive `_voice-drafts/` to a timestamped subdirectory before Phase 1 retune. Otherwise stale pass-1 outputs poison the next pilot.
  C8: Add a Phase 0 → Phase 3 ordering check: any source edit after Phase 3 starts forces a re-run of that chapter.

COMMENDATIONS
  ✓ Binary gates per phase are correctly specified (PASS/FAIL only — no soft "looks good enough" language).
  ✓ §3 A4 explicitly proposes collapsing polish/normalize if they are indistinguishable — the plan is willing to simplify itself.

VERDICT: PROCEED WITH CONDITIONS
The plan treats voice-pass as deterministic. It is not. C5–C7 close the gap. The drift risk (silent regression across re-runs) is the one Phase 3 will hit hardest.

---

## SEAT 3 — Nia Okonkwo (Plan-as-threat-surface)

DIMENSION SCORES
  D1 Threat model: 4 — the spec has none. What does an attacker who modifies a voice agent file gain? (Answer: arbitrary control of the manuscript's voice, deniable because outputs are gitignored intermediates.)
  D2 Key/credential lifecycle: 6 — Claude CLI auth is the only credential; assumed present, not enforced.
  D3 Data minimisation: 7 — only chapter prose is sent to Claude; no PII, no source code. But the source paper (`source/local_node_saas_v13.md`) is referenced and is *gitignored confidential*; if any voice agent reads it during pass execution, that's leakage to a third-party model provider. Spec doesn't forbid it.
  D4 Tamper evidence: 5 — gitignored intermediates have no hashing, no signing. A malicious or buggy run can silently alter a draft and the user has no detection.
  D5 Physical access: 6 — laptop compromise gets the manuscript draft (already on the laptop) and the user's Claude API token (already on the laptop). New surface: agent files in user-scope are global and survive repo deletion.
  D6 Transport: 7 — TLS to Anthropic is assumed; not the spec's job to harden.
  D7 Audit trail: 4 — what was sent, what came back, when, with which agent version? Nothing is logged. The orchestrator's stdout is the only record and isn't captured.
  D8 IR for prompt compromise: 3 — if a tuned agent produces ideologically subtly-shifted prose for one chapter, the response procedure is undefined.

DOMAIN AVERAGE: 5.3 / 10

BLOCKING ISSUES
  B3: No audit trail. The orchestrator dispatches Claude in headless mode. There is no log of inputs, outputs, agent versions, or timestamps beyond the resulting markdown file. If the user reads ch15 a month after promotion and finds a sentence that misrepresents the security model, there is no forensic path back to *what produced that sentence*.

CONDITIONS
  C9: Log every voice-pass invocation: `_voice-drafts/_log/<timestamp>-<chapter>-<pass>.json` with input SHA, output SHA, agent SHA, CLI version, model, exit code, duration. This belongs in `build/voice-pass.py`, not the spec, but the spec must require it.
  C10: Forbid voice agents from referencing `source/` papers in their prompts. State this explicitly in §10 Reference Library.
  C11: Add hash verification: after pass-2 completes, write `<chapter>.sha256` next to the output. Promotion compares the hash; mismatch halts promotion.
  C12: Add an IR runbook entry: "If a promoted chapter is later found to contain hallucinated content, the recovery is: (a) `git revert` the promotion commit, (b) inspect the audit log for that chapter's run, (c) decide whether to retune the agent or run the chapter through the literary-board agent."

COMMENDATIONS
  ✓ Out-of-scope §2 explicitly says no Sunfish-repo touching — preserves a security boundary.
  ✓ Phase 4 manual gate is the right design — no auto-promotion of model output.

VERDICT: PROCEED WITH CONDITIONS
The plan has no audit trail. For an editorial pipeline this is an inconvenience; for a *security-chapter* editorial pipeline (ch07, ch15) it is a real risk that the manuscript silently shifts under the model's hand. C9–C11 are required.

---

## SEAT 4 — Jordan Kelsey (Plan-as-economics)

DIMENSION SCORES
  D1 Unit economics: 6 — $15–25 token cost is plausible at face value but assumes one full Phase 3 run; the plan implicitly budgets for retunes (§7) and does not multiply: 2 retunes × $25 = $75, breaching the $50 stop-loss before the user notices.
  D2 Time economics: 5 — 60–100 hours total. Phase 0 alone is 24–48 hours of *focused editorial work*; the plan does not say how that fits into a calendar with Sunfish work, day job, etc. "Calendar-spread across weeks" is hand-waving.
  D3 First-customer-of-this-plan: 8 — author is the customer, problem is concrete, urgency is real (audiobook ships).
  D4 Differentiation vs. alternatives: 8 — §13 is honest about A/B/C/D and why each is held or rejected.
  D5 Churn risk (project abandonment): 5 — no checkpoint at which the author would say "this isn't working, ship the current draft instead." Kill criteria fire *within phases*; nothing fires at the project level.
  D6 Expansion / leverage: 6 — knowledge capture into cerebrum is good, but the agent-tuning work is bespoke to this book; the spec doesn't ask whether the tuned agents become a reusable asset.
  D7 OSS/community: n/a (single-author project).
  D8 Sustainability horizon: 5 — implicitly assumes the author's attention budget for several weeks; competing demands are not modelled. If Sunfish demands two weeks, this plan stalls between Phase 2 and Phase 3 — which is exactly the worst place to stall (pilots committed, full run not done).

DOMAIN AVERAGE: 6.1 / 10

BLOCKING ISSUES
  B4: Phase 0 effort estimate (24–48 hours of editorial work) is the largest single line item and is the *least* tested. The Ch01 enumeration paragraph took some non-trivial time to compress well; multiplying by 24 chapters at 1–2 hours each assumes a learning curve that hasn't been measured. If Phase 0 actually takes 4 hours/chapter, the total swings to 96 hours for Phase 0 alone — and the whole plan blows past 100 hours.

CONDITIONS
  C13: Run Phase 0 on **two** chapters first (not one) and time it. Project the total. Decide before sweeping all 24 whether to invoke Alternative A (skip voice-pass) or invest the days.
  C14: Add a project-level kill criterion: "If by end-of-week-two we are not through Phase 2, the plan is replanned, not continued." Calendar discipline.
  C15: Budget retune cycles into the cost estimate: $15–25 *per Phase 3 run*, expecting at most 2 runs = $30–50. Match the $50 stop-loss to the budgeted ceiling, not to a single run.

COMMENDATIONS
  ✓ §9 Stop-loss at >$50 is concrete.
  ✓ §13 Alternative A retained as escape hatch — the plan does not over-commit to its own approach.

VERDICT: PROCEED WITH CONDITIONS
The economic model is plausible at the bottom and underbuilt at the top. Phase 0 timing is the load-bearing assumption and it has not been measured. C13 is the cheap, high-value check before committing to the full sweep.

---

## SEAT 5 — Tomás Ferreira (Plan-as-craft)

DIMENSION SCORES
  D1 Methodological grounding: 6 — "tune the agent + re-pilot" is a reasonable loop but the plan never asks whether agent-driven voice-pass is itself the right tool. The reader's complaint ("mechanical, fatiguing") is a *prose* complaint; agent re-tuning is one of several responses, not the obviously-correct one.
  D2 "Last device" / disaster recovery: 7 — Phase 4 per-chapter revert is fine; full plan revert is a `git reset` to a phase-boundary commit. Adequate.
  D3 Voice-mapping reliability: 5 — `voice-plan.yaml` was set once; D3 in §14 admits mapping changes are "not pre-committed" and will be made under pilot pressure. Three of six voices (gladwell, brown, godin) have *one* chapter of pilot evidence each. The spec assumes the mapping is mostly right — a strong assumption.
  D4 Onboarding (next-session resume): 7 — Resume Protocol is good; Reference Library is good. A fresh agent could mostly execute this cold.
  D5 Selection/community health of voice agents: 5 — the agents are author-internal, no external review. Sinek is canonical example #1 (3 paragraphs); now we'd add the Preface paragraph as #2. Two examples is thin for a 5,000-word target.
  D6 Portability: 8 — chapters stay as plain markdown; the plan does not lock the manuscript into the orchestrator.
  D7 Governance: 6 — single author. Decisions clear. But the "user reviews each pilot, PASS/FAIL" gate is exactly the place where author-fatigue produces false-PASS verdicts.
  D8 Prior art: 4 — the spec does not cite any prior art on AI-assisted prose voice-tuning. "Tune-then-re-pilot" is presented as native to this project. There is a body of work on prompt iteration loops (cited or not) that should at least inform whether two retune rounds is the right cap.

DOMAIN AVERAGE: 6.0 / 10

BLOCKING ISSUES
  B5: The methodology itself is unexamined. "The Sinek agent felt mechanical → tune the Sinek agent" is one diagnosis. Equally plausible: the *two-pass* pipeline (guest voice → Sinek normalize) is the source of mechanical compounding, and the fix is to *drop pass-2* for chapters where the guest voice already produces house-quality prose. The plan never asks this. Phase 1's premise (tune all six agents) commits to the existing pipeline shape before testing whether the shape is correct.

CONDITIONS
  C16: Add a Phase 0.5 — *methodology check*. Take Ch01 pass-1 (gladwell only, no Sinek polish). Does it read better than the current `_voice-drafts/final/ch01`? If yes, the answer is *less* Sinek, not *retuned* Sinek — and Phase 1's scope shrinks dramatically.
  C17: Add an external-reader gate: at least one pilot reviewed by a non-author reader (per A6 already), and the verdict is *binding*, not advisory.
  C18: Cite at least one prior-art reference for AI-assisted prose voice-tuning iteration counts. If none exists, say so explicitly — "we are operating without prior art" is honest and material.

COMMENDATIONS
  ✓ Audiobook listener test (§5) is exactly right — the failure mode is sound, not page.
  ✓ §3 A1/A2 frame the problem as a "two-knob" tradeoff (mechanical ↔ voiceless), which is the correct mental model.
  ✓ Composite-character disclosure (§0c) addresses an honest-craft issue the plan didn't have to address.

VERDICT: PROCEED WITH CONDITIONS
The plan does the second-best thing (retune the agent) without testing the best thing (drop pass-2 for chapters where it isn't earning its keep). C16 is a one-hour check that could halve the rest of the plan.

---

## COUNCIL TALLY

| Member | Domain Avg | Verdict |
|---|---|---|
| Voss (Infrastructure) | 6.1 | PROCEED WITH CONDITIONS |
| Shevchenko (Distributed Systems) | 5.8 | PROCEED WITH CONDITIONS *(below 6.0 — borderline)* |
| Okonkwo (Security) | 5.3 | PROCEED WITH CONDITIONS *(below 6.0 — see B3)* |
| Kelsey (Product/Economic) | 6.1 | PROCEED WITH CONDITIONS |
| Ferreira (Local-First Practitioner) | 6.0 | PROCEED WITH CONDITIONS |
| **Overall** | **5.9** | **CONDITIONAL — five blocking issues to clear** |

By the strict scoring rule (avg ≥ 6.0, no blocks), Shevchenko and Okonkwo would BLOCK on average alone. Both are seated at PROCEED WITH CONDITIONS because the conditions are concrete and the plan is recoverable, not structurally broken — but the council does not clear until B1–B5 are resolved.

---

## CONSOLIDATED ACTION ITEMS

### Blocking issues (resolve before next round)
| # | Raised by | Issue |
|---|---|---|
| B1 | Voss | Agent files are user-scope, not in this repo — manuscript provenance is not reproducible. |
| B2 | Shevchenko | Voice-pass is non-deterministic; the plan treats it as a pure function. No tie-breaking, no drift detection. |
| B3 | Okonkwo | No audit trail. No record of what input + agent version + model produced any given output. |
| B4 | Kelsey | Phase 0 timing (24–48h) is the largest line item and untested; one bad chapter doubles the estimate. |
| B5 | Ferreira | Methodology is unchallenged. The plan retunes Sinek without first testing whether *less* Sinek (drop pass-2 selectively) is the right answer. |

### Conditions (required for full PROCEED)
| # | Raised by | Condition |
|---|---|---|
| C1 | Voss | Pin Claude CLI version + model name; record per phase commit. |
| C2 | Voss | Mirror agent files into the manuscript repo as the source of truth. |
| C3 | Voss | Per-promotion sidecar manifest (source SHA, agent SHA, CLI, model, mode, timestamp). |
| C4 | Voss | Add kill criterion for Claude safety-filter refusal on ch07/ch15. |
| C5 | Shevchenko | Specify determinism stance: voice-pass once per agent revision; re-runs are deliberate. |
| C6 | Shevchenko | Document the `--pass 2 --force --only` retune pattern (or add `--from-pass1`). |
| C7 | Shevchenko | Archive `_voice-drafts/` to timestamped subdir at each phase boundary. |
| C8 | Shevchenko | Source-edit-after-Phase-3 forces re-run of that chapter. |
| C9 | Okonkwo | Per-invocation log file (input SHA, output SHA, agent SHA, CLI, model, exit, duration). |
| C10 | Okonkwo | Forbid voice agents from referencing `source/` papers; state in §10. |
| C11 | Okonkwo | Hash output post-pass-2; promotion verifies the hash. |
| C12 | Okonkwo | IR runbook entry for "promoted chapter contains hallucinated content." |
| C13 | Kelsey | Run Phase 0 on **two** chapters first; project total before sweeping. |
| C14 | Kelsey | Project-level calendar kill: not through Phase 2 by end of week 2 → replan. |
| C15 | Kelsey | Budget retunes: $30–50 ceiling = up-to-2 Phase 3 runs, matched to stop-loss. |
| C16 | Ferreira | Add Phase 0.5 — drop-pass-2 methodology check on Ch01 before committing to retune. |
| C17 | Ferreira | External-reader gate: at least one non-author reviewer of one pilot, binding. |
| C18 | Ferreira | Cite prior art on AI prose voice-tuning iteration counts, or state none exists. |

(18 conditions exceeds the per-member cap of 5 only when aggregated; each member stays within their cap.)

### Commendations (carry forward)
- §6 Rollback Strategy is per-phase and concrete (Voss).
- §8 Resume Protocol uses primitives the orchestrator already supports (Voss).
- Binary phase gates avoid soft-language failure (Shevchenko).
- §3 A4 willingness to collapse polish/normalize if indistinguishable — plan can simplify itself (Shevchenko).
- Out-of-scope statement protects the Sunfish security boundary (Okonkwo).
- Manual Phase 4 gate — no auto-promotion of model output (Okonkwo).
- $50 stop-loss is concrete (Kelsey).
- §13 keeps Alternative A as escape hatch — plan does not over-commit to itself (Kelsey).
- Audiobook listener test as the truth-gate for cadence (Ferreira).
- Two-knob framing of the mechanical/voiceless tradeoff (Ferreira).
- Composite-character disclosure §0c — honest-craft issue the plan chose to address (Ferreira).

---

## Council notes — gaps the spec did NOT name

The spec lists the gaps it knows about. The council was asked to find ones it didn't. Three deserve a final flag:

1. **Provenance** (B1, B3, C2/C3/C9/C11). The agent that voiced the book is not in the book's git history. The promoted chapter is, but the prompt that produced it isn't. This is the single largest unowned risk.
2. **Methodology** (B5, C16). The plan iterates *within* the current pipeline shape (two-pass, six agents). It never asks whether the shape is right. One hour of testing "drop pass-2" could collapse Phase 1 to a fraction of its current scope.
3. **Calendar** (B4, C13/C14). The plan budgets effort but not attention. A book project that stalls between Phase 2 commit and Phase 3 run sits in the worst possible state — promised work begun, not delivered. A project-level calendar kill is the discipline this plan needs.

The spec is good. With B1–B5 resolved, it would clear A-grade.
