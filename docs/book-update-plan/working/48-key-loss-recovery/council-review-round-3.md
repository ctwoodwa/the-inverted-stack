# Kleppmann Council Review — Round 3 — Extension #48 Key-Loss Recovery

**Date:** 2026-04-26
**Round:** 3 (regression-verification)
**Scope:** Same two sections re-read in their post-literary-board state — Ch15 §Key-Loss Recovery (now lines 117–272) and Ch20 §Key-Loss Recovery UX (now lines 178–244).

Round 2 returned PUBLISH with four minor P2 items. A parallel literary-board review then surfaced 5 P1 + 22 P2. A resolution pass applied 18 fixes (5 P1 + 13 P2). This Round 3 review verifies that none of the 18 fixes regressed a Round 1 or Round 2 finding, no resolved item has been silently undone, and no new council-relevant gap has appeared in the post-edit prose. Each council member confirms the fixes that touched their seat and certifies (or names) any regression.

The 18 changes break down across the two chapters as follows:
- **Ch15 structural reorder** — §Recommended Deployment Combinations now leads after §Why this matters, before §The six recovery mechanisms.
- **Ch15 §Recovery State-Machine Convergence rewrite** — two-layer framing (global log semantics + local node behavior); custodian-release events explicitly bound by the convergence rule.
- **Ch15 §Boundaries and Operator Mitigations rename** — formerly §What This Section Does Not Solve; now contains six failure modes (mandatory key-escrow added).
- **Ch15 trustee-residency paragraph expanded** — DPDP, PIPL, DIFC DPL, ADGM 2021, 242-FZ, POPIA §72, GDPR Chapter V transfer mechanism named explicitly.
- **Ch15 §Custodian-held backup key expanded** — cloud custodians and regulated institutional intermediaries (system integrators, trust banks, regulated escrow) added.
- **Ch15 §Multi-sig social recovery** — opening split into two paragraphs to reduce clause density.
- **Ch20 §Recovery Initiation UX** — fresh-device retrieval path specified (relay query against public signed metadata, no auth at discovery).
- **Ch20 §Recovery Completion Confirmation** — KEK delivery channel specified (recovered root seed unwraps KEK envelopes from encrypted log via existing distribution path); closing arc-return paragraph added.
- **Ch20 §Time-Locked Grace Period UX** — high-outage paragraph added (grace period as floor, in-person trustee channel).
- **Ch20 §Trustee Designation Flow** — ARIA live region contract added (`aria-live=polite` for increments, `assertive` for threshold-met/failed).

---

## Round 1 + Round 2 finding regression check

| Origin | Finding | R3 status | Note |
|---|---|---|---|
| R1 P0-1 | Custodian liability postures | STILL RESOLVED | Three-posture paragraph at Ch15:182 intact. |
| R1 P0-2 | Social-recovery jurisdictional residency | STILL RESOLVED, EXPANDED | Ch15:170 — DPDP / PIPL / DIFC DPL now joined by ADGM 2021, 242-FZ, POPIA §72, and GDPR Chapter V transfer mechanism. The legal-defensibility argument is materially stronger than in R2. |
| R1 P0-3 | GDPR Article 17 / audit-trail tension | STILL RESOLVED | Ch15:220 — default-preserve-with-counsel-review posture intact. |
| R1 P1-1 | Shamir-dealer arithmetic & delivery | STILL RESOLVED | Ch15:161 dealer paragraph intact; technical-review HTML comment at Ch15:163 preserved (CSRNG uniformity verified per Osei P2-12). |
| R1 P1-2 | Recovery state-machine convergence | RESOLVED + IMPROVED | Convergence rule rewritten into two-layer global/local framing per Osei P1-3; custodian-release path now explicitly bound per Webb/R2-N1. |
| R1 P1-3 | Trustee silent-decay mitigation | STILL RESOLVED, BETTER PLACED | Ch15:252 — quarterly liveness ping discipline preserved. The §Boundaries and Operator Mitigations rename resolves the dual-register concern (heartbeat-as-mitigation now sits naturally inside a section that names both limits and mitigations). |
| R1 P1-4 | Custodian transient-failure | STILL RESOLVED | Ch15:184 — single-point-of-failure language intact. |
| R1 P1-5 | Paper-key transcription verification | STILL RESOLVED | Ch20:194 — round-trip + refuse-to-complete language intact. |
| R1 P1-6 | Implementation surfaces named contracts | STILL RESOLVED, IMPROVED | Ch15:266 — `GracePeriodObserver` now specifies tick-cadence as implementation-defined / UX-driven, with push-alongside-pull and recommended minimum poll interval (one minute). Closes R2-P2-3 carried forward. |
| R1 P1-7 | Deployment-class binding | STILL RESOLVED | Ch15:143 — first-run declaration, signed manifest, audit log entry intact. |
| R1 P1-8 | Ch20 first-run primary + secondary | STILL RESOLVED | Ch20:192 — primary + secondary fallback prompt intact. |
| R1 P2-1 | Bad-faith trustees | STILL RESOLVED | Ch15:254 — coordinated-coercion + hostile-inheritance case intact. |
| R1 P2-2 | Silence-as-signal grounding | STILL RESOLVED | Ch20:232 — grounding paragraph intact. |
| R1 P2-3 | Deployment-class table promotion | NOW RESOLVED | Ch15:133 — table now leads §Key-Loss Recovery after §Why this matters, before the six mechanisms. The R1/R2 carry-forward stylistic concern is now closed. |
| R2 P2-1 | Custodian-release bound by convergence rule | NOW RESOLVED | Ch15:224–226 — convergence rule prose explicitly names "single signed custodian-release event (sub-pattern 48b)" alongside "trustee-threshold attestation (sub-pattern 48a)". |
| R2 P2-2 | Trustee-side burden of liveness ping | NOW RESOLVED | Ch15:252 — "The trustee-side cost is one challenge per quarter per user they serve as trustee — manageable at typical trustee-network sizes, worth budgeting against when an individual ends up named as trustee for many users at once." |
| R2 P2-3 | `GracePeriodObserver` tick cadence | NOW RESOLVED | Ch15:267 — implementation-defined, UX-driven, push alongside pull, one-minute recommended minimum poll interval. |
| R2 P2-4 | Deployment-class table promotion | NOW RESOLVED | Same as R1 P2-3 above. |

**Resolution totals across all rounds:** 14 of 14 R1 findings resolved, 4 of 4 R2 P2 items resolved, 0 regressions detected.

The literary-board P1 items that map onto council seats (Webb P1-1 and P1-2 — fresh-device retrieval and KEK delivery; Osei P1-3 — convergence framing precision; Webb/R2-N1 carried — custodian-release bound by convergence; Barker P1-5 — GDPR Chapter V) are resolved in the post-edit prose. None of the literary-board P2 items that were applied (the 13 of 22 fixed) regressed a council finding.

---

## SEAT 1 — The Distributed Systems Theorist (cryptographic and protocol soundness)

**Round 3 score: 8.7 / 10** (Round 2: 8.4)
**Verdict: PROCEED**

### Verification of prior findings

- **R1 F1 (dealer arithmetic) intact.** Ch15:161 dealer paragraph unchanged in substance; technical-review HTML comment at Ch15:163 preserves the CSRNG-uniformity claim and now matches Osei's literary-board attestation.
- **R1 F2 (state-machine convergence) materially improved.** The new two-layer framing (Ch15:225–227) is theoretically tighter than the R2 version. The R2 prose said "no node accepts a completion event for a recovery claim against which a signed dispute event already exists in its log... the recovery is reset and re-initiation is required" — strict halt language. The R3 prose distinguishes:
  - **Global log semantics** — validation rejects completion when a signed dispute pre-exists.
  - **Local node behavior** — a node that applied a completion before seeing the dispute reverses the completion on dispute arrival.
  This is the eventually-consistent reversibility model the architecture actually implements. The window-between-completion-and-dispute is named ("a real architectural fact") and the operational mitigation (sizing the grace period to make the window negligible) is given. This is exactly the precision a careful theorist wants.
- **R1 F3 (Article 17 / audit-trail) intact.** Ch15:220 default-preserve language unchanged.
- **R2 N1 (custodian-release path under convergence) resolved.** Ch15:224 names "trustee-threshold attestation (sub-pattern 48a) or a single signed custodian-release event (sub-pattern 48b)" and Ch15:226 explicitly states "the rule applies identically to trustee-threshold completions (sub-pattern 48a) and single-signed custodian-release events (sub-pattern 48b) — both are completion events under the same convergence policy". The single-signed asymmetry is named, so an implementer cannot mis-read the rule as trustee-threshold-only.

### New concerns introduced by the resolution pass

**None at the theorist seat.** The convergence-rule rewrite is a strict improvement: it removes the strict-atomic overclaim Osei flagged and simultaneously closes the R2-N1 custodian-path silence. The two-layer structure is exactly the partition-tolerance posture this architecture commits to elsewhere; no new theoretical gap is opened.

The Shamir dealer paragraph split into two paragraphs (per literary-board Halvorsen P2-7) reduces clause density but preserves all of: the field, the dealer location, the entropy source, the wrapping discipline, the post-emission zeroing. No theoretical content lost in the split.

### Defended claims (still tested, still accepted)

- Argon2id parameter cross-reference (Ch15:188) — unchanged.
- "Deliberate friction, not a network propagation delay" framing (Ch15:208) — unchanged.
- Threshold ladder in deployment-class table — unchanged from R2; now leads the section per the structural reorder.
- The new dealer paragraph extends rather than contradicts the Argon2id discipline.
- The "reverse on dispute arrival" sentence at Ch15:226 is the partition-tolerance commitment the architecture makes elsewhere; the local-reversal behavior at the sync layer matches the CRDT-engine-layer behavior described in Ch12.

---

## SEAT 2 — The Production Operator (what breaks at 3am)

**Round 3 score: 8.4 / 10** (Round 2: 8.2)
**Verdict: PROCEED**

### Verification of prior findings

- **R1 F1 (trustee silent decay) intact and better-placed.** The §Boundaries and Operator Mitigations rename resolves the dual-register concern raised in R2-N4. The heartbeat paragraph now reads naturally inside a section explicitly titled to contain both boundaries and mitigations, rather than awkwardly inside §What This Section Does Not Solve.
- **R1 F2 (custodian transient failure) intact.** Ch15:184 single-point-of-failure language unchanged.
- **R1 F3 (paper-key transcription verification) intact.** Ch20:194 round-trip language unchanged.
- **R2 N2 (trustee-side burden) resolved.** Ch15:252 — "The trustee-side cost is one challenge per quarter per user they serve as trustee — manageable at typical trustee-network sizes, worth budgeting against when an individual ends up named as trustee for many users at once." This is the operator-honest acknowledgment the prior review asked for. The "worth budgeting against when an individual ends up named as trustee for many users at once" half-sentence pre-empts the high-fan-out trustee case (one person named as trustee for fifty users would face fifty quarterly pings — explicitly flagged as an operational concern even though it is rare).
- **Custodian-held backup key expansion (Ch15:176)** — the addition of "regulated cloud custodians" and "regulated institutional intermediary" categories (system integrators, trust banks, regulated escrow) reflects what operators actually field-deploy in regulated APAC and EU markets. The phrase "the institutional category that fills the role varies by region and industry" is the right operator-honest framing.

### New concerns introduced by the resolution pass

**N1 (Round 3) — High-outage in-person trustee channel is prescribed but not operationalized.** Ch20:228 says "configure at least one trustee reachable through an in-person or offline channel so the original holder retains a non-digital dispute path." This is the right architectural guidance, but the operational mechanism for an in-person dispute is not specified. How does an in-person trustee file a signed dispute event into the audit log when they cannot reach the network themselves? The prose implies they would file the dispute through their own device's intermittent connectivity, but a deployment in a 2G-only region may have a trustee whose own connectivity is no better than the original holder's. **Severity: P2 (clarification, not gap).** A future operator-playbook section could elaborate; the recovery section itself does not need to solve every offline-trustee operational case.

### Defended claims (still tested, still accepted)

- The deployment-class table grace-period progression (14/7/30 days) — unchanged.
- "No recovery setup at first-run = explicit acknowledgment" pattern (Ch20:188) — unchanged.
- Multi-channel notification at Ch20:226 — unchanged; now explicitly framed as an architectural floor that high-outage deployments treat as conservative rather than guaranteed.
- The §Boundaries and Operator Mitigations rename is a clean editorial improvement — the heading now matches the content's dual register (limits + mitigations) and the prose at Ch15:248 explicitly says "The architecture acknowledges each, prescribes operator mitigations where they exist, and documents what remains the user's responsibility."

---

## SEAT 3 — The Skeptical Implementer (is the prose implementable?)

**Round 3 score: 8.5 / 10** (Round 2: 8.0)
**Verdict: PROCEED**

### Verification of prior findings

- **R1 F1 (Implementation Surfaces) intact and improved.** Ch15:266 still names the five contracts; the `GracePeriodObserver` description now closes the R2-P2-3 cadence ambiguity:
  > "Tick frequency is implementation-defined and UX-driven — subscribers pull at the cadence their progress display requires (typically once per minute for in-app banners, once per hour for OS push notifications). Push delivery of the terminal expiry event is supported alongside pull; the recommended minimum poll interval for the intermediate ticks is one minute, to avoid log-validation thrash."
  An implementer can now build against this. Push-alongside-pull is named; the one-minute minimum poll interval prevents naive tight-loop polling that would thrash the log validator.
- **R1 F2 (deployment-class binding) intact.** Ch15:143 first-run + signed manifest language unchanged.
- **R1 F3 (Ch20 primary + secondary) intact.** Ch20:192 prompt unchanged.
- **R2 N3 (`GracePeriodObserver` tick cadence) resolved** — see above.
- **Webb literary-board P1-1 (fresh-device retrieval) resolved.** Ch20:214 — "The application queries the relay for signed recovery-arrangement metadata events under that identifier — these events carry the public envelope (mechanism type, trustee count, custodian identifier, declared deployment class) but no key material, and the relay returns them without authenticating the requester because the metadata reveals nothing usable to an adversary." This is a specification-grade answer to "how does the fresh device get the arrangement metadata" — the relay query, the event-shape, the no-auth-at-discovery posture, and the explicit security justification ("the metadata reveals nothing usable to an adversary") are all in the prose. The follow-up sentence at Ch20:214 — "Authentication of the requester happens further down the flow, through the chosen mechanism's release path" — closes the trust-boundary question.
- **Webb literary-board P1-2 (KEK delivery channel) resolved.** Ch20:236 — "the new device's recovered root seed unwraps the wrapped KEKs (Key Encryption Keys) for the user's roles directly from the encrypted log: the wrapped KEK envelopes are stored as administrative events in the same log used for application data (the existing distribution channel described in Ch15 §Role Attestation Flow), and the recovered root seed is the only key required to unwrap them locally. No additional delivery channel is required." This is exactly the kind of specification-grade answer a principal engineer wants — the delivery channel is the existing log-event distribution path (no new mechanism), the unwrapping is local, and the cross-reference points the implementer at the canonical Role Attestation Flow.

### New concerns introduced by the resolution pass

**None at the implementer seat.** The fresh-device retrieval and KEK delivery answers compose cleanly with the existing Role Attestation Flow and the convergence rule. The five-contract Implementation Surfaces list at Ch15:266 still lands cleanly — `RecoveryClaimSubmitted`, `GracePeriodObserver`, `TrusteeAttestation`, `RecoveryDispute`, `RecoveryCompleted` — and the `GracePeriodObserver` cadence specification removes the last R2-P2 implementation-detail concern.

### Defended claims (still tested, still accepted)

- The HTML annotation marking `Sunfish.Foundation.Recovery` and `Sunfish.Kernel.Audit` as forward-looking is preserved at Ch15:119 and Ch20:180.
- The active-voice register and concrete UI copy in Ch20 are preserved through both the fresh-device retrieval description and the KEK delivery confirmation.
- No new code blocks; the `// illustrative — not runnable` annotation remains correctly applied where it appears.

---

## SEAT 4 — The Pedantic Lawyer (legal and regulatory exposure)

**Round 3 score: 9.0 / 10** (Round 2: 8.6)
**Verdict: PROCEED**

### Verification of prior findings

- **R1 F1 (custodian liability) intact.** Ch15:182 three-posture paragraph unchanged in substance.
- **R1 F2 (social-recovery jurisdictional residency) intact and materially expanded.** The R2 prose named DPDP, PIPL, and DIFC DPL. The R3 prose at Ch15:170 names DPDP, PIPL, DIFC DPL, ADGM Data Protection Regulations 2021, Federal Law 242-FZ, and POPIA Section 72 explicitly — and adds GDPR Chapter V transfer mechanism for EU-resident users with non-EU trustees, with named compliance instruments (Standard Contractual Clauses, adequacy decision, binding corporate rules). This is a strict improvement over R2 in legal coverage.
- **R1 F3 (GDPR Article 17 / audit-trail) intact.** Ch15:220 default-preserve language unchanged.
- **Mandatory key-escrow boundary added (Ch15:260) — addresses Volkov literary-board P2-22.** The §Boundaries and Operator Mitigations subsection now explicitly names the case where mandatory key-escrow requirements supersede the user-held recovery model, with the honest qualifier "they are not currently in force in most jurisdictions named in Appendix F, but several CIS and ECOWAS policy discussions are active". The closing sentence — "The architecture cannot honor user-held recovery and government-mandated escrow simultaneously; the deployment chooses one and documents the choice in the team's compliance posture" — is exactly the kind of structural acknowledgment a careful counsel wants to see, and it does not retreat into hedge language.

### New concerns introduced by the resolution pass

**None at the lawyer seat.** The expansion of the trustee-residency paragraph is the largest delta and it lands cleanly. The naming of ADGM 2021 alongside DIFC DPL closes the GCC gap Krishnamurthy flagged. The naming of POPIA §72 alongside the African regimes closes the Diallo gap. The naming of 242-FZ explicitly (rather than via "and similar regimes") closes the Volkov gap. The GDPR Chapter V sentence closes the Barker gap. None of these expansions weaken the existing argument; each strengthens it.

The mandatory key-escrow boundary is correctly placed in §Boundaries and Operator Mitigations — it is the structural acknowledgment that the architecture cannot serve two masters, presented in the same operator-honest register as the other five failure modes. A careful counsel reviewing the chapter for HIPAA / PCI / financial-services deployments now has explicit pointer text for every regulated-jurisdiction concern the chapter targets.

### Defended claims (still tested, still accepted)

- The honest-limitation register of §Boundaries and Operator Mitigations continues to read as good-faith counsel guidance.
- Cross-reference to #32 (succession arrangements) — preserved.
- Ch20 grace-period plain-language disclosure — preserved.
- The "Five failure modes" → "Six failure modes" header update at Ch15:248 correctly reflects the expanded count after mandatory key-escrow was added; no silent overclaim.

---

## SEAT 5 — The Outside Observer (honesty and accessibility to a non-specialist)

**Round 3 score: 8.5 / 10** (Round 2: 8.0)
**Verdict: PROCEED**

### Verification of prior findings

- **R1 F1 (bad-faith trustees) intact.** Ch15:254 coordinated-coercion + hostile-inheritance case intact.
- **R1 F2 (silence-as-signal grounding) intact and improved by closing arc-return.** Ch20:232 grounding paragraph unchanged; Ch20:244 now adds a closing-arc paragraph that returns the reader to the chapter's ownership story before the outward pointer. The closing sentence — "the next section returns to a different surface that the same ownership story depends on — accessibility — because every recovery flow in this section also has to land for a user navigating with a screen reader, a keyboard, or a high-contrast display" — is exactly the kind of section-arc-return Hollis flagged.
- **R1 F3 (deployment-class table position) NOW RESOLVED.** The structural reorder promotes the deployment-class table above the six-mechanism descriptions. A non-specialist reader now encounters the recommendation before the cryptography. This is the "lead with the punchline / decision before reasoning" voice principle the book commits to, and the chapter now holds it. The bridging sentence at Ch15:151 — "The consumer combination composes sub-patterns 48a (multi-sig social) and 48c (paper-key); the SMB combination composes 48b (custodian) with 48a; the regulated combination composes 48b with 48a, layered under sub-pattern 48e (timed grace period) tuned to the audit window" — closes Nakamura's bridging-sentence concern as a bonus.
- **R2 N4 (dual-register subsection) resolved.** The §Boundaries and Operator Mitigations rename does the work R2-N4 flagged: the section is now named to contain both boundaries and mitigations, so the heartbeat paragraph reads naturally inside it rather than as a register-clash.

### New concerns introduced by the resolution pass

**N2 (Round 3) — The argument flow now requires the lay reader to absorb the deployment-class table before any mechanism is defined.** This is the intended improvement (decision-before-reasoning), but it does mean the lay reader meets technical terms — "Multi-sig social (3-of-5)", "Custodian-held under attestation", "Multi-sig social with named officers" — before any of those mechanisms is explained. The prose handles this well: the per-class paragraphs at Ch15:145–149 use plain-language framing ("Pick five people you trust. Any three of them together can help you get your data back.") that lets a reader without prior context absorb the table. But a strict non-specialist on first read will still encounter the cryptographic terminology before the explanation. This is not a regression — it is the trade-off the structural reorder explicitly makes — and the prose at Ch15:135 ("Pick the deployment class first; the rest of the section describes the mechanisms it composes") signposts the trade-off honestly. **Severity: P2-borderline (acknowledgment, not action item).**

### Defended claims (still tested, still accepted)

- The Ch20 grace-period UI copy — preserved.
- "Trust three friends / Trust your bank or lawyer / Trust a piece of paper in a safe" framing at Ch20:190 — preserved.
- 12-month recovery-readiness audit cadence reasoning at Ch20:242 — preserved.
- The Ch20 closing arc-return at Ch20:244 turns what was an outward-pointer-only ending into a section-closure-then-pointer pattern. The rhetorical structure now matches the rest of the book.

---

## Cross-cutting verifications

- **Spec voice in Ch15.** All 18 fixes hold the specification register. The Boundaries-and-Operator-Mitigations rename, the convergence-rule rewrite, the trustee-residency expansion, the custodian-category expansion, and the table-leads structural reorder all hold spec voice without slipping into tutorial register.
- **Tutorial voice in Ch20.** All Ch20 additions (fresh-device retrieval, KEK delivery channel, high-outage paragraph, ARIA live region, closing arc-return) hold tutorial register. The fresh-device retrieval description sits naturally in the user's first-person flow ("The user is on a fresh device. Their original device is gone..."); the KEK delivery description is a single paragraph that an implementer reads as specification but a reader reads as plain reassurance ("Recovery complete. Your data is being decrypted on this device.").
- **Paragraph-length cap (≤6 sentences).** Spot-checked the longest of the 18 changes. The convergence-rule paragraph at Ch15:225 is 5 sentences; the trustee-residency expansion at Ch15:170 is 5 sentences; the high-outage paragraph at Ch20:228 is 2 sentences; the ARIA live region addition at Ch20:208 is 1 added sentence inside an existing paragraph; the KEK delivery paragraph at Ch20:236 is 4 sentences; the closing arc-return at Ch20:244 is 1 sentence. All within cap.
- **HTML annotations preserved.** Ch15:119 and Ch20:180 forward-looking-namespace HTML comments intact. Ch15:163 CSRNG-uniformity technical-review HTML comment intact. Ch15:198 Apple Secure Enclave / Pixel Titan M / Windows Pluton technical-review HTML comment intact.
- **Cross-references intact.** #32 (succession), #18 (delegated capability grants), #9 (chain of custody), Appendix F (regulatory matrix), Ch12 (CRDT conflict resolution), Ch15 §Role Attestation Flow (newly cross-referenced from Ch20 KEK delivery), Ch20 §Key-Loss Recovery UX ↔ Ch15 §Key-Loss Recovery, and the new Ch20 §Time-Locked Grace Period UX → Ch15 §Boundaries and Operator Mitigations cross-reference at Ch20:242 all resolve.
- **Header-count consistency.** §Boundaries and Operator Mitigations opens with "Six failure modes" at Ch15:248 — verified against actual count: skip-setup, designate-then-decay-or-bad-faith-trustees, decayed-arrangement, illegible-paper-key, mandatory-key-escrow. **Wait — I count five there**, plus the bad-faith-trustees case at Ch15:254. So six is correct. (The bad-faith-trustees paragraph is a distinct failure mode, separate from designate-then-decay.) Header count matches body count.

---

## Round 3 consolidated action items

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
| R3-P2-1 | Production Operator (N1) | The high-outage in-person trustee channel is named at Ch20:228 but the operational mechanism for an in-person dispute (how a trustee files a signed dispute event when they cannot reach the network) is unspecified. A future operator-playbook section could elaborate; not section-blocking. |
| R3-P2-2 | Outside Observer (N2 — borderline) | The structural reorder requires the lay reader to encounter the deployment-class table before any mechanism is explained. Trade-off explicitly signposted at Ch15:135; trade-off is the intended editorial choice. No action item. |

---

## Overall Round 3 verdict

**PUBLISH.**

All five council members vote PROCEED. Domain averages: Theorist 8.7, Production Operator 8.4, Skeptical Implementer 8.5, Pedantic Lawyer 9.0, Outside Observer 8.5. Council average: **8.62 / 10** (Round 2 average: 8.24). Every score has improved over Round 2; no score has regressed.

**Zero regressions detected.** All 14 R1 findings remain resolved. All 4 R2 P2 items are now resolved (3 by direct prose addition, 1 by the structural reorder previously deferred). All 5 literary-board P1 items that mapped onto council seats (Webb fresh-device retrieval, Webb KEK delivery, Osei convergence framing precision, Webb-carried R2-N1 custodian-release, Barker GDPR Chapter V) are resolved in the post-edit prose. The 13 P2 fixes from the literary-board pass that were applied did not introduce any council-blocking concern.

The two new Round 3 items (R3-P2-1 in-person trustee operational mechanism, R3-P2-2 lay-reader deployment-table-first trade-off) are P2-stylistic / acknowledgment-only — neither rises to a publication-stop concern.

**Three R2 N-numbered concerns conclusively cleared by the post-edit prose:**
- R2-N1 (custodian-release path under convergence) — explicitly bound at Ch15:224 and Ch15:226.
- R2-N2 (trustee-side liveness-ping burden) — acknowledged at Ch15:252.
- R2-N3 (`GracePeriodObserver` tick cadence) — specified at Ch15:267.

**One R2 N-numbered concern resolved by the §Boundaries and Operator Mitigations rename:**
- R2-N4 (dual-register subsection) — the rename converts the subsection's mixed register from a register-clash into the section's named purpose.

The chapter clears the council in this round. **This is the final council pass for #48 before voice-check.**

---

**Round 3 totals:** 0 P0 / 0 P1 / 2 P2 (both stylistic / acknowledgment-only). Five council members reviewed; five PROCEED, zero PROCEED-WITH-CONDITIONS, zero BLOCK. Zero regressions across all three rounds.

**Most important Round 3 outcome:** the structural reorder (deployment-class table now leads the section) plus the convergence-rule two-layer rewrite together raise the chapter's ceiling materially. The Theorist and Pedantic Lawyer seats both gained ~0.3 points on the strength of these two changes alone. The chapter is now publication-ready for the regulated audience the deployment-class table targets, and the editorial register holds across all 18 post-R2 edits.
