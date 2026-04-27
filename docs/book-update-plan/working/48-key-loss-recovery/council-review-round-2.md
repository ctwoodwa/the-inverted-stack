# Kleppmann Council Review — Round 2 — Extension #48 Key-Loss Recovery

**Date:** 2026-04-26
**Round:** 2
**Scope:** Same two sections reviewed in Round 1 — Ch15 §Key-Loss Recovery (now spanning through §Implementation Surfaces, lines 117–261) and Ch20 §Key-Loss Recovery UX (lines 178–240) — re-read in their post-resolution-pass state.

Round 1 produced REVISE with 3 P0 (all from Pedantic Lawyer — BLOCK), 8 P1, and 3 P2 findings. Between rounds, eleven fixes were applied to the chapters: 3 of 3 P0, 8 of 8 P1, and 2 of 3 P2 (P2-3 structural reorder deferred). This review verifies each finding individually, then re-scores the council members and identifies any new concerns introduced by the resolution pass.

---

## Round 1 findings status

| ID | Round 1 finding | Status | Note |
|---|---|---|---|
| P0-1 | Custodian liability postures unspecified (Pedantic Lawyer F1) | RESOLVED | Ch15:157 — three postures (a/b/c) named, regulated-industry default explicitly identified as posture (b) at minimum, Appendix F cross-referenced, weakly-defensible warning on (a) preserved. ~115 words. |
| P0-2 | Social-recovery jurisdictional residency unaddressed (Pedantic Lawyer F2) | RESOLVED | Ch15:145 — DPDP / PIPL / DIFC DPL trustee-residency obligations stated, Appendix F cross-referenced, "cryptographic construction is sound everywhere; legal classification is not" closing line maintains spec voice. |
| P0-3 | GDPR Article 17 / audit-trail tension elided (Pedantic Lawyer F3 + Theorist F3) | RESOLVED | Ch15:195 — closing paragraph rewritten to default-preserve metadata, distinguishes content-stub crypto-shred from third-party metadata, names trustees' and custodians' evidentiary interest, "case-specific erasure follows counsel review" pointer added. |
| P1-1 | Shamir-dealer arithmetic & delivery protocol unstated (Theorist F1) | RESOLVED | Ch15:139 — GF(2^256), local dealer on user device, OS CSRNG seed, shares wrapped under trustee public key before transit, dealer state zeroed, in-memory recovery key zeroed. Specification-grade. |
| P1-2 | Recovery state-machine convergence undefined under partition (Theorist F2) | RESOLVED | New H3 §Recovery State-Machine Convergence at Ch15:197–201 — strict halt-on-dispute tiebreak, asymmetric-authority justification (cost of erroneously-completed > cost of halted-and-re-initiated), enforcement at audit-log validation layer named, reversal-on-late-dispute behaviour stated. |
| P1-3 | Trustee silent-decay mitigation absent (Production Operator F1) | RESOLVED | Ch15:243 — quarterly liveness ping per trustee, degraded-arrangement banner when active count falls below threshold + 1, 12-month cadence acknowledged as too coarse. Lands inside §What This Section Does Not Solve, which is a defensible placement (operator-honesty register). |
| P1-4 | Custodian transient-failure single-point-of-failure unstated (Production Operator F2) | RESOLVED | Ch15:159 — appended sentence names identity-dispute / outage / staffing-gap stalls, declares custodian-only is a single point of failure, prescribes secondary mechanism (paper-key, social) as operational mitigation. |
| P1-5 | Paper-key transcription verification missing from Ch20 (Production Operator F3) | RESOLVED | Ch20:194 — round-trip transcription verification mandated at setup time, application refuses to accept setup completion until typed phrase matches, "skipping it is not an option" register matches the production-critical framing. |
| P1-6 | Implementation surfaces unnamed (Skeptical Implementer F1) | RESOLVED | New H3 §Implementation Surfaces at Ch15:251–261 — five named contracts (`RecoveryClaimSubmitted`, `GracePeriodObserver`, `TrusteeAttestation`, `RecoveryDispute`, `RecoveryCompleted`), illustrative-marker preserved, audit-log subscription path stated. |
| P1-7 | Deployment-class binding mechanism unstated (Skeptical Implementer F2) | RESOLVED | Ch15:229 — declared at first-run, persists in signed configuration manifest, `Sunfish.Foundation.Recovery` reads class on initialization and binds threshold + grace period, manifest entry is itself a signed audit-log event. |
| P1-8 | Ch20 first-run prompt singular when Ch15 supports composition (Skeptical Implementer F3) | RESOLVED | Ch20:192 — primary + secondary fallback explicit, follow-up prompt example included ("Most users pair social recovery with a paper key in a safe"), both selections bound into signed configuration manifest. |
| P2-1 | Bad-faith trustees case unaddressed (Outside Observer F1) | RESOLVED | Ch15:245 — coordinated coercion in family/business dispute named, hostile inheritance claim added as second case, trustee-selection responsibility placed on user, grace-period limitation acknowledged for travelling/hospitalized users. |
| P2-2 | Silence-as-signal paragraph unsettling without grounding (Outside Observer F2) | RESOLVED | Ch20:230 — single grounding paragraph added: "without the silence-completes rule, a user who genuinely lost everything would have no recovery path at all", deployment-class table cross-referenced. |
| P2-3 | Deployment-class table structural promotion (Outside Observer F3) | NOT RESOLVED (deferred — explicitly noted in fix-pass description) | The author deferred this as P2-stylistic; consistent with Round 1 verdict guidance that the chapter could clear without it. Not blocking. |

**Resolution totals:** 13 of 14 RESOLVED, 0 PARTIALLY, 1 deferred-by-design. The three P0 BLOCK items from the Pedantic Lawyer are all cleared.

---

## SEAT 1 — The Distributed Systems Theorist (cryptographic and protocol soundness)

**Round 2 score: 8.4 / 10** (Round 1: 6.8)
**Verdict: PROCEED**

### Verification of Round 1 findings against this seat

- **F1 resolved:** the new dealer paragraph at Ch15:139 specifies the field, the dealer location, the entropy source, the wrapping discipline, and the post-emission zeroing. The chapter now answers "who dealt and on what device" without ambiguity.
- **F2 resolved:** the new §Recovery State-Machine Convergence H3 specifies the tiebreak rule, justifies it (asymmetric-authority argument is defensible — preferring halt over silent completion is the conservative default for confidentiality-preserving systems), and locates enforcement at the audit-log validation layer rather than vaguely at "the system". The "applied locally and reversed when the dispute event arrives during sync" sentence closes the partition-tolerance question explicitly.
- **F3 resolved:** the closing paragraph of §Recovery-event audit trail at Ch15:195 abandons the contradictory "audit follows crypto-shredding rules" claim and replaces it with a defensible default-preserve posture. The technical claim and the legal claim are now consistent.

### New concerns introduced by the resolution pass

**N1 — Convergence rule applies cleanly to the social-recovery and grace-period mechanisms; the custodian-release path is silent on it.** The new §Recovery State-Machine Convergence reads as if all completions are trustee-attestation events, but a custodian release produces a single signed event, not a t-of-n threshold reconstruction. The dispute-halt rule presumably applies to custodian releases too, but the prose does not say so. A practitioner implementing the custodian variant may reasonably wonder whether the convergence rule binds the custodian's release event identically to a trustee-completion event. **Severity: P2 (clarification, not gap).**

### Defended claims (still tested, still accepted)

- The Argon2id parameter cross-reference at Ch15:163 (regulated-tier values for paper-key derivation) is unchanged and correct.
- The "deliberate friction, not a network propagation delay" framing at Ch15:183 is unchanged and remains theoretically sound.
- The threshold ladder in the deployment-class table is unchanged and remains a defensible mapping.
- The new dealer paragraph extends rather than contradicts the existing Argon2id discipline; the pre-existing key-derivation section at Ch15:75 is consistent with the new dealer specification.

---

## SEAT 2 — The Production Operator (what breaks at 3am)

**Round 2 score: 8.2 / 10** (Round 1: 6.5)
**Verdict: PROCEED**

### Verification of Round 1 findings against this seat

- **F1 resolved:** the new heartbeat / quarterly-liveness paragraph at Ch15:243 turns silent decay into an observed event. The threshold + 1 banner discipline is exactly what an operator would specify; it avoids the "binary alive/dead" model that misses gradual decay. Placing this inside §What This Section Does Not Solve is unusual for a *mitigation* paragraph (it reads as both "what the architecture does about decay" and "what it cannot fully prevent") but the prose handles the dual register cleanly.
- **F2 resolved:** the appended sentence at Ch15:159 names the transient-failure modes the original review enumerated (identity dispute, custodian-side outage, staffing gap) and prescribes the operator-honest mitigation (secondary mechanism). The "single point of failure" language matches the operator register established elsewhere in the chapter.
- **F3 resolved:** Ch20:194 mandates round-trip transcription verification with refuse-to-complete-setup discipline. "Skipping it is not an option" is exactly the production-grade phrasing — softer language would have been a lesser fix.

### New concerns introduced by the resolution pass

**N2 — Heartbeat-ping cadence is asserted (quarterly) but the trustee-side cost is unstated.** The trustee's app must respond to a tiny challenge once per quarter per user they serve as trustee. A trustee serving five users encounters the prompt twenty times per year. This is not an operator-blocking issue — quarterly is conservative — but a brief sentence acknowledging the trustee-side burden would close the loop. **Severity: P2.**

### Defended claims (still tested, still accepted)

- The deployment-class grace-period progression (14/7/30 days) is unchanged.
- The "no recovery setup at first-run = explicit acknowledgment" pattern (Ch20:188) is preserved and now strengthened by the round-trip verification flow.
- Multi-channel notification (Ch20:226) is preserved.

---

## SEAT 3 — The Skeptical Implementer (is the prose implementable?)

**Round 2 score: 8.0 / 10** (Round 1: 6.2)
**Verdict: PROCEED**

### Verification of Round 1 findings against this seat

- **F1 resolved:** the new §Implementation Surfaces H3 lists five named event contracts. Each contract carries a one-line description of what it carries and when it fires. The "audit-log validation layer enforces the convergence rules before any UX layer observes the events" sentence connects the implementation surface to the convergence rule from the new Theorist-F2 fix. An implementer can now hold both H3 sections in their head and produce a coherent integration plan.
- **F2 resolved:** Ch15:229 specifies declaration-at-first-run, persistence in the signed configuration manifest, initialization-time read by `Sunfish.Foundation.Recovery`, and the auditability of class changes. The configuration-binding gap is closed.
- **F3 resolved:** Ch20:192 surfaces primary + secondary mechanism selection at the first-run prompt, matching the Ch15 deployment-class composition. The example pairing (social + paper-key in safe) makes the abstract composition concrete.

### New concerns introduced by the resolution pass

**N3 — `GracePeriodObserver` is described as emitting "ticks during the grace period and the terminal expiry event".** Tick frequency is unspecified. An implementer needs to know whether ticks are once-per-second, once-per-minute, once-per-hour, or event-driven (only on UX subscription). This is a small gap — likely intended to be a UX-driven implementation choice — but for a contract-level description, the indeterminacy is uncharacteristic of the chapter's overall register. **Severity: P2.**

### Defended claims (still tested, still accepted)

- The HTML annotation marking `Sunfish.Foundation.Recovery` and `Sunfish.Kernel.Audit` as forward-looking is preserved at both Ch15:119 and Ch20:180; the implementation-surfaces fix does not contradict the pre-1.0 disclaimer.
- The active-voice register and concrete UI copy in Ch20 are preserved through the rewritten first-run prompt.
- No new code blocks were introduced; the existing `// illustrative — not runnable` annotation is unchanged.

---

## SEAT 4 — The Pedantic Lawyer (legal and regulatory exposure)

**Round 2 score: 8.6 / 10** (Round 1: 5.9)
**Verdict: PROCEED**

### Verification of Round 1 findings against this seat

- **F1 BLOCK resolved:** the new ~115-word liability paragraph at Ch15:157 names all three postures (custodian-disclaims-all, bounded-cap, joint-liability), identifies the regulated-industry default (posture b at minimum), explicitly warns that posture (a) is "weakly defensible against the user's loss" — language the Round 1 review specifically requested — and points the reader to Appendix F. This is exactly the practitioner-orienting paragraph the prior review demanded; the chapter no longer fails a careful counsel's first read on the custodian section.
- **F2 BLOCK resolved:** Ch15:145 names DPDP, PIPL, and DIFC DPL trustee-residency obligations and points to Appendix F. The closing line ("The cryptographic construction is sound everywhere; the legal classification of the trustees' role is not") reads as exactly the kind of honest separation a regulated buyer wants to see — the architecture admits the limit of its own jurisdiction-scope.
- **F3 BLOCK resolved:** Ch15:195 establishes default-preserve as the posture, distinguishes the data subject's content stub (crypto-shreddable) from the surrounding third-party metadata (jurisdiction-specific, requires legal review), and names the trustees' and custodians' evidentiary interest. This now reads as defensible counsel guidance rather than a crypto-claim that overreaches into legal territory.

### New concerns introduced by the resolution pass

None. The three legal-exposure paragraphs are well-calibrated to the book's existing regulatory voice. The cross-references to Appendix F are consistent with how the rest of the chapter handles jurisdictional matters. The §What This Section Does Not Solve update from "Three failure modes" to "Five failure modes" reflects the genuine expansion of the boundary section and avoids the silent-overclaim problem.

### Defended claims (still tested, still accepted)

- The honest-limitation register of §What This Section Does Not Solve continues to read as good-faith counsel guidance.
- The cross-reference to #32 (succession arrangements with executor delegation) is preserved.
- The Ch20 grace-period plain-language disclosure ("If this is not you, contact your trustees immediately") is preserved.

---

## SEAT 5 — The Outside Observer (honesty and accessibility to a non-specialist)

**Round 2 score: 8.0 / 10** (Round 1: 7.4)
**Verdict: PROCEED**

### Verification of Round 1 findings against this seat

- **F1 resolved:** the new bad-faith-trustees paragraph at Ch15:245 covers the case the Round 1 review specifically named — coordinated coercion in family/business disputes — and adds hostile-inheritance as a parallel case. The "trustee selection is the user's responsibility" framing avoids the architecture overclaiming its ability to grade trustee motivations. The acknowledgment that the grace period does not help travelling/hospitalized users is the operator-honest qualifier the Round 1 reviewer asked for.
- **F2 resolved:** Ch20:230 adds the grounding paragraph that converts the unsettling silence-as-signal moment into a comprehensible design choice. "Without the silence-completes rule, a user who genuinely lost everything would have no recovery path at all" is the right register: it gives the non-specialist reader the design rationale without retreating into cryptographic terminology.
- **F3 NOT RESOLVED (deferred):** the deployment-class table remains positioned after the six-mechanism descriptions. The Round 1 review tagged this as P2-stylistic; the deferral is consistent with that tagging. A non-specialist reader still wades through the cryptography before reaching the recommendation. This is a real friction point for the lay reader but does not rise to a publication-stop concern.

### New concerns introduced by the resolution pass

**N4 — The §What This Section Does Not Solve subsection has grown from three failure modes to five and now also contains a *mitigation* (the heartbeat / quarterly liveness paragraph for P1-3).** The section is now doing two jobs: enumerating limitations *and* prescribing one of the chapter's mitigations. The dual register is handled cleanly enough at the prose level — the heartbeat paragraph reads naturally inside the trustee-decay mode — but a non-specialist reader scanning for "what does this architecture cannot do" may find the mixed register slightly confusing. This is a borderline-P2 stylistic note; not an action item for this round.

### Defended claims (still tested, still accepted)

- The Ch20 grace-period UI copy is preserved.
- The "Trust three friends / Trust your bank or lawyer / Trust a piece of paper in a safe" framing at Ch20:190 is preserved and now extended naturally into the primary + secondary composition prompt.
- The 12-month recovery-readiness audit cadence reasoning is preserved at Ch20:240.

---

## Cross-cutting verifications (asked for explicitly in the brief)

- **Spec voice in Ch15.** The new dealer paragraph, convergence H3, liability paragraph, jurisdictional paragraph, audit-trail rewrite, and Implementation Surfaces H3 all hold the specification register established in the rest of Ch15. No tutorial-voice slippage was introduced.
- **Tutorial voice in Ch20.** The rewritten first-run prompt and the new grounding paragraph after the silence-as-signal text both hold the tutorial register. The grounding paragraph at Ch20:230 was the highest-risk insertion (it sits adjacent to the philosophically necessary "silence is the signal" passage); the prose handles the register transition cleanly.
- **Paragraph-length cap (≤6 sentences).** Spot-checked the longest of the new paragraphs. The liability paragraph at Ch15:157 has 6 sentences; the heartbeat paragraph at Ch15:243 has 5; the audit-trail rewrite at Ch15:195 has 4; the convergence paragraph at Ch15:201 has 5. All within cap.
- **HTML annotation preserved.** The forward-looking-namespace HTML comments at Ch15:119 and Ch20:180 are intact; the Apple Secure Enclave technical-review HTML comment at Ch15:173 is intact. No annotation lost in the resolution pass.
- **Cross-references intact.** #32 (succession), #18 (delegated capability grants), #9 (chain of custody), Appendix F (regulatory matrix), Ch12 (CRDT conflict resolution), Ch20 §Key-Loss Recovery UX (from Ch15) and Ch15 §Key-Loss Recovery (from Ch20) all resolve correctly. The "Five failure modes" header update at Ch15:239 correctly reflects the actual count after the fix-pass additions.

---

## Round 2 consolidated action items

### P0 — must-fix before publication

| # | Raised by | Issue |
|---|---|---|
| — | — | None. |

### P1 — should-fix to lift chapter quality

| # | Raised by | Issue |
|---|---|---|
| — | — | None. |

### P2 — nice-to-have / stylistic

| # | Raised by | Issue |
|---|---|---|
| R2-P2-1 | Theorist (N1) | Add half-sentence to §Recovery State-Machine Convergence clarifying that the dispute-halt rule binds custodian-release events identically to trustee-completion events. |
| R2-P2-2 | Production Operator (N2) | Add half-sentence to the heartbeat paragraph acknowledging the trustee-side burden (one challenge per quarter per user served). |
| R2-P2-3 | Skeptical Implementer (N3) | Specify or scope the `GracePeriodObserver` tick cadence (e.g., "tick frequency is implementation-defined; UX subscribes for progress display"). |
| R2-P2-4 | Round 1 carried forward | Promote the deployment-class table above the six-mechanism descriptions (lead-with-the-punchline). Original P2-3, deferred from Round 1. |

---

## Overall Round 2 verdict

**PUBLISH.**

All five council members vote PROCEED. Domain averages: Theorist 8.4, Production Operator 8.2, Skeptical Implementer 8.0, Pedantic Lawyer 8.6, Outside Observer 8.0. No P0 issues. No P1 issues. Four P2 stylistic / clarification items, all minor and non-blocking. The three Round 1 BLOCK findings — all from the Pedantic Lawyer, all in the legal-defensibility space — are conclusively cleared. The eight P1 conditions are conclusively cleared. Of the three P2 items, two are cleared and one (P2-3 structural promotion) is consciously deferred; the deferral was acknowledged in the resolution-pass description and is consistent with the Round 1 verdict guidance that the chapter could clear without it.

The resolution pass introduced four small new concerns (N1 through N4 plus the carried-forward P2-3) — none rise to the level requiring another full council round. They are appropriate inputs to a copyedit pass, not a third adversarial review.

The chapter clears the council in this round.

---

**Round 2 totals:** 0 P0 / 0 P1 / 4 P2 (3 new + 1 carried). Five council members reviewed; five PROCEED, zero PROCEED-WITH-CONDITIONS, zero BLOCK.

**Most important remaining finding:** none rises to action-item-must-fix. If forced to identify a single highest-leverage polish, it is R2-P2-4 (promote the deployment-class table) — the lay reader still wades through cryptography before reaching the deployment recommendation, and the book's stated "decision before reasoning" voice principle would be better served by inversion. This is a structural copyedit, not a council-blocking concern.
