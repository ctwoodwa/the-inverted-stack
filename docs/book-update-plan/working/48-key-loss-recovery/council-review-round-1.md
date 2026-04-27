# Kleppmann Council Review — Round 1 — Extension #48 Key-Loss Recovery

**Date:** 2026-04-26
**Round:** 1
**Scope (narrow):** Two new sections added by extension #48 only.
- Ch15 §"Key-Loss Recovery" — `chapters/part-3-reference-architecture/ch15-security-architecture.md`, lines 117–231 (~2,050 words; specification register; six recovery mechanisms 48a–48f, threat model, deployment-class table, honest-boundary section).
- Ch20 §"Key-Loss Recovery UX" — `chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md`, lines 178–234 (~1,040 words; tutorial register; five UX flows).

The rest of Ch15 and Ch20 passed prior ICM cycles and is out of scope for this review. The council interrogates only what is new.

Convention: file references use `Ch15:NNN` and `Ch20:NNN` for line numbers in the chapter files as quoted in the line-numbered reads of those files. The full chapter files have been the basis of review.

---

## SEAT 1 — The Distributed Systems Theorist (Voss-equivalent — cryptographic and protocol soundness)

**Score: 6.8 / 10**
**Verdict: PROCEED WITH CONDITIONS**

### Top 3 findings

**F1 — Shamir secret-sharing arithmetic is asserted, not specified (Ch15:137).**
The text reads "the user's root recovery key is split into *n* shares, each share held by a separate trustee, and any *t* of the *n* shares suffices to reconstruct the key." The arithmetic is right. What is missing is the field over which the polynomial lives, the order of the share encoding, and — most importantly — the protocol by which shares are *generated and delivered* to trustees. The book describes the *result* of the Shamir construction but never discloses the dealer model. Who dealt? Where? On what device? Trustee delivery is also silent — does the user generate shares locally and email them in plaintext (catastrophic) or is each share encrypted under the trustee's public key before transit (correct)?
**Fix:** add a one-paragraph specification under §Multi-sig social recovery declaring (a) shares are generated on the user's device using a CSPRNG-seeded Shamir dealer over GF(2^256); (b) each share is wrapped under the trustee's enrolled public key before leaving the device; (c) the dealer's working state is zeroed after share emission. This is a bookkeeping fix, not a redesign.

**F2 — The grace-period state machine has no defined behaviour under split-brain or trustee-dispute concurrency (Ch15:181, Ch15:200–203).**
Line 181 states "the grace period is not a client-side timer; it is an event in the signed audit log, which means it is tamper-evident and observable by any node that validates the log." Good. But what happens when the user's existing device files a dispute *and* a trustee files a recovery completion in overlapping time-windows during a network partition? Both are signed events. Both target the same recovery claim. Which event wins, by what tiebreak rule, and how is that rule justified? The chapter currently treats recovery as a single linear state machine when in practice it is concurrent across multiple signing parties on a partitionable transport. This is exactly the kind of "CRDT handles it" elision the council exists to surface.
**Fix:** add a "Recovery state-machine convergence" paragraph specifying tiebreak (e.g., "any signed dispute event in the log halts recovery — completion events filed concurrently are rejected on convergence; the recovery is reset and re-initiation is required") and stating the partition-tolerance posture explicitly. Cross-reference Ch12 conflict resolution if relevant.

**F3 — Crypto-shredding interaction with recovery audit trail is asserted but not proven sound (Ch15:189).**
The closing sentence of §Recovery-event audit trail says "Recovery audit events follow the same retention and crypto-shredding rules as application data... the records' content is erasable by DEK destruction if a data subject requests erasure." This is an unprovable claim as written. Recovery events contain trustee identifiers, custodian identifiers, and grace-period boundaries — these are personal data referring to *third parties*, not just the data subject. A GDPR Article 17 erasure request from the data subject does not extend to the trustees' identity records, and an erasure of the recovery DEK destroys evidence that may be required to defend the trustees in a contested recovery dispute. The architectural claim ("crypto-shred works here too") is in tension with the legal evidentiary claim ("audit trail is the legal artifact"). One of those two has to bend.
**Fix:** rewrite the closing sentence to acknowledge the tension. Suggested: "Recovery audit retention is jurisdiction-dependent and intersects third-party rights. Crypto-shredding the data subject's content stub is technically possible; legal review determines whether trustee/custodian identifiers in the same record are also erasable, since those refer to third parties whose evidentiary interest may attach." This matches the honest tone already established in §GDPR Article 17.

### Defended claims (tested, accepted)

- The decision to not derive new KEKs from compromised keys (Ch15:106) is repeated correctly in the recovery context (forward-secrecy intent preserved).
- The Argon2id parameter cross-reference (Ch15:157) matches the regulated-tier values from §Key Hierarchy (verified by technical-review item 4).
- The non-derivation framing of the time-locked grace period as "deliberate friction, not a network propagation delay" (Ch15:177) is theoretically sound and honestly framed.
- The recommended deployment-class threshold ladder (3-of-5 / 2-of-3 / regulated-tier custodian-primary) is a defensible mapping of n, t, and grace-period to user-population threat model.

---

## SEAT 2 — The Production Operator (Marguerite Voss-equivalent — what breaks at 3am)

**Score: 6.5 / 10**
**Verdict: PROCEED WITH CONDITIONS**

### Top 3 findings

**F1 — Trustee-acceptance state never reconciles against trustee unreachability (Ch20:203–204).**
The Ch20 designation flow reads "Trustee 1: confirmed. Trustee 2: confirmed. Trustees 3–5: pending." The application "flags an arrangement with fewer than the threshold confirmed." This is fine for the moment of designation. The unanswered operational question is what happens 14 months later when a trustee changes their email and the user has not noticed. The Ch20 §Recovery Completion paragraph mentions a "12-month recovery-readiness audit reminder" (Ch20:234), but the Ch15 deployment-class table prescribes 3-of-5 for consumers — so the consumer can lose two trustees silently and remain at threshold, but lose three silently and be cryptographically locked out at the moment of greatest stress. A 12-month audit cadence is too coarse to catch this; the math says a trustee unreachable for 11 months is undetected until month 12, and an unreachable trustee at recovery time is indistinguishable from a malicious holdout.
**Fix:** add to Ch15 deployment-class discussion (or create a new paragraph in §A.5) a heartbeat mechanism — quarterly liveness ping per trustee (the trustee's app responds to a tiny challenge), with a degraded-arrangement banner when the *active* trustee count falls below threshold + 1. This raises the implementation bar but turns silent decay into an observed event, which is the operator's whole job.

**F2 — Custodian-held backup has no defined failure behaviour for custodian outage (Ch15:147–152).**
The custodian section says release "requires multi-factor identity verification through the custodian's out-of-band channel — in-person identity documents, video call, notarized request, or whatever the custodian's policy mandates." What happens when the custodian's website is down on the day the user needs recovery? When the custodian's notary is unreachable for two weeks? When the custodian was acquired three months ago and the new owner has not yet stood up the verification flow? The Ch15 honest-boundary paragraph mentions "custodian out of business" (Ch15:230) as one of the unsolvable scenarios — fine — but the *transient* failure modes (slow custodian, custodian under audit, custodian's verification flow failing for one specific user) are exactly what production operators see, and the chapter has nothing to say about them. The grace-period mechanism does not save this case because the custodian is not a trustee.
**Fix:** add a sentence to §Custodian-held backup key naming the operational failure mode explicitly: "When the custodian is operational but the verification flow for a specific user fails — identity dispute, custodian-side outage, or staffing — the recovery stalls indefinitely. A secondary recovery mechanism (paper-key, social) is the operational mitigation; relying on a single custodian is a single point of failure for recovery." This is the operator-honest version of the deployment-class recommendation already implicit in the table.

**F3 — Paper-key UX has no defensive treatment for the most common production failure: the user lost the paper or it is illegible (Ch20 entirely silent).**
Ch15:159 states honestly "An adversary who obtains the printed phrase obtains the recovery key. The architecture provides no defense against that physical compromise." Good. But the *operator* failure mode is the user's paper key being water-damaged after a flood, eaten by a mouse in storage, faded after eight years in a hot attic, or — most commonly — written down with a transcription error at first-run that the user does not detect until recovery. Ch20 §Key-Loss Recovery UX has no first-run UX for verifying the paper-key transcription. A serious deployment would print the phrase, ask the user to re-enter it, and refuse to accept setup completion until round-trip succeeds. Ch20 currently does not require this.
**Fix:** add a one-paragraph subsection to Ch20 §First-Run Prompt (or §Trustee Designation Flow's paper-key analog) requiring round-trip transcription verification at setup time. "Print the phrase, ask the user to type it back, refuse setup completion until they match. Mention this is the only opportunity the application has to detect a transcription error before it costs the user their data." Forty additional words; production-critical.

### Defended claims (tested, accepted)

- The deployment-class table (Ch15:213–215) — the 14/7/30-day grace period progression is defensible as a real operational ladder, not a theoretical curve.
- The "no recovery setup at first-run = explicit acknowledgment" pattern (Ch20:188) reflects real operator practice; SaaS services that buried this in settings have produced known data-loss incidents.
- The multi-channel notification requirement for the grace period (Ch20:222) is operationally correct — single-channel routing is a production failure pattern from real incident reports.
- The framing of full-offline as the *normal* operating state for some deployments (Ch20 elsewhere; Ch20 §Key-Loss Recovery UX inherits this voice) is consistent and operator-honest.

---

## SEAT 3 — The Skeptical Implementer (Shevchenko-equivalent — is the prose implementable?)

**Score: 6.2 / 10**
**Verdict: PROCEED WITH CONDITIONS**

### Top 3 findings

**F1 — `Sunfish.Foundation.Recovery` and `Sunfish.Kernel.Audit` are forward-looking namespaces with no concrete observable contract (Ch15:119, Ch20:180).**
Both chapter files now carry HTML comments acknowledging that these two namespaces "are part of the Volume 1 extension roadmap and not yet present in the Sunfish reference implementation." That is honest. The implementer's question, however, is: if I were to build this *today* against Sunfish.Kernel.Security alone, what is the integration contract? The chapter prescribes events ("recovery-claim events", "grace-period state machine", "recovery-event audit trail") without naming the event schema, the persistence layer, or the cross-package invariants. A reader trying to implement #48 against the current Sunfish package canon will get to "the system broadcasts the recovery claim" (Ch15:175) and discover there is no documented broadcast surface, no documented grace-period observer, and no documented audit-event taxonomy.
**Fix:** add a short "Implementation surfaces" paragraph at the end of Ch15 §Key-Loss Recovery — not an API spec, but a list of the *named contracts* the chapter implies. Three to five bullets: recovery-claim event type, grace-period observer, trustee-attestation event type, completion event type, dispute event type. Mark the section "// illustrative — see Sunfish package canon at Foundation milestone" per existing pre-1.0 convention. This costs 60 words; it removes the implementer's complaint that the section is unimplementable.

**F2 — Deployment-class recommendations are not distinguishable in code (Ch15:213–215).**
The table says "Consumer: 3-of-5 social, 14-day grace; SMB: custodian + 2-of-3, 7-day grace; Regulated: custodian + multi-sig with named officers, 30-day grace." How does the application *know* which class it is in? The chapter never says. There is no described configuration mechanism, no profile descriptor, no schema entry. A deployment that mis-self-identifies (consumer claiming regulated profile, or vice versa) silently uses the wrong threshold and grace period. For a section whose entire normative force is "pick the right combination", the absence of a configuration-binding statement is a hole.
**Fix:** add a single sentence after the table: "Deployment class is declared at first-run and persists in the team's signed configuration manifest. `Sunfish.Foundation.Recovery` reads the class on initialization and binds the corresponding threshold and grace-period values; the manifest entry is a signed event in the audit log so a class change is itself an audited operation." Twenty words; closes the configuration gap.

**F3 — Ch20 references "the recovery arrangement" as a singular thing, but Ch15 supports composition (paper-key + social + biometric) (Ch20:210).**
Ch20:210 reads "The application retrieves the recovery arrangement — mechanism type, trustee count, custodian identifier — and displays it without displaying any key material." Singular "mechanism type". But Ch15:174 establishes that the grace-period mechanism is *composable* with all the others, and the deployment-class table prescribes primary + secondary mechanisms simultaneously. Implementing Ch20 against this Ch15 yields ambiguity: does the user pick one mechanism at setup (Ch20's flow), or does the user configure a primary + secondary combination (Ch15's deployment-class recommendation)?
**Fix:** rewrite the Ch20 first-run prompt to surface primary and secondary mechanisms. "Pick a primary recovery mechanism. We recommend a secondary fallback in case the primary is unavailable when you need it." The existing UI copy in §Recovery Completion already nods at this ("Your recovery arrangement is still active. You may want to update your trustees if anything has changed.") — the setup flow needs to match.

### Defended claims (tested, accepted)

- The decision to keep both `Sunfish.Foundation.Recovery` and `Sunfish.Kernel.Audit` as named-but-forward-looking namespaces is consistent with the book's existing pre-1.0 Sunfish reference policy and the HTML annotation makes the constraint visible.
- The active-voice register and concrete UI copy in Ch20 (the verbatim user strings inside quotes) make the section directly implementable as UX copy.
- The "// illustrative — not runnable" annotation on code blocks is correctly applied where used; no invented APIs surface in code that would mislead implementers.

---

## SEAT 4 — The Pedantic Lawyer (Okonkwo-equivalent — legal and regulatory exposure)

**Score: 5.9 / 10**
**Verdict: BLOCK**

### Top 3 findings

**F1 — BLOCKING. Custodian liability allocation is assumed, not specified (Ch15:147–153).**
The §Custodian-held backup key text reads "The mitigation is the custodian's own audited security posture, the legal liability allocation in the custody contract, and the out-of-band identity verification that an adversary must also defeat." This sentence presupposes that a custody contract exists and allocates liability — but the architecture as written gives no opinion on what that contract must contain. A real-world deployment will have one of three liability postures: (a) the custodian disclaims all liability for release errors (the most common contract; weakly defensible against the user's loss); (b) the custodian carries bounded liability up to a contractual cap (typical financial-services posture); (c) the custodian is jointly liable with the architecture vendor (rare; expensive). The book is the place where a practitioner gets oriented to the question. By asserting the "legal liability allocation" exists without naming the three postures or the regulated-industry default expectation, the chapter is silently implying that this is solved when it is not. For a chapter targeting HIPAA, PCI, and financial deployments, this is a publication-stop concern.
**Fix:** add a 100-word paragraph to §Custodian-held backup key explicitly naming the three liability postures and stating which is the default expectation in regulated industries (typically (b)). Cross-reference Appendix F's regulatory matrix where the relevant frameworks appear. This is not a legal-counsel substitute; it is a "point the practitioner at the right question" gloss the rest of the chapter already does well for cryptographic concerns.

**F2 — BLOCKING. Buterin-style social recovery has unclear legal standing in several jurisdictions named in Appendix F (Ch15:137).**
The Argent / Buterin social-recovery construction is sound cryptography. Its *legal* standing as a custody arrangement is jurisdiction-dependent in a way the chapter does not surface. In several jurisdictions referenced elsewhere in the book — India under DPDP Act, China under PIPL, the UAE under DIFC DPL — handing fragments of the user's data-decryption key to friends without a formal regulated relationship may be construed as an unlicensed deposit-taking activity, an unauthorized financial-services arrangement, or a breach of the data-residency principle (if a trustee resides in a jurisdiction the team's policy prohibits). The chapter recommends 3-of-5 social recovery for consumer deployments without flagging that the trustees' geographic distribution may itself be a compliance event. Given the book's elsewhere-rigorous regulatory voice (cross-jurisdictional references in Ch15 Relay Trust Model, Appendix F), the silence on social-recovery legal status is a non-trivial gap.
**Fix:** add a sentence to §Multi-sig social recovery: "Social-recovery legal status varies by jurisdiction. Trustee residency may itself trigger data-residency obligations under DPDP, PIPL, DIFC DPL, and similar regimes; deployments subject to localization requirements name their trustees in-jurisdiction or document an exception in the team's compliance posture (see Appendix F)." This is consistent with the book's existing voice and closes the legal-defensibility gap.

**F3 — BLOCKING. GDPR Article 17 / recovery-audit-trail interaction is acknowledged but the practical answer is missing (Ch15:189; Theorist F3 above).**
The Theorist (Seat 1) flagged the technical inconsistency. The legal version is sharper: a data subject who later disputes a recovery completion has a legitimate interest in the audit trail being preserved. The trustees and custodian named in that audit trail have a legitimate interest in the record being preserved as evidence of their good-faith participation. A blanket "audit follows crypto-shredding rules" statement creates legal exposure for *all three parties* — the data subject (who may want erasure), the trustees (who may want their participation record preserved), and the architecture vendor (whose product produced the contradiction). The chapter would currently fail a careful counsel's review for a HIPAA, PCI, or financial-services deployment. Hold-as-default and case-specific erasure-on-request, with legal-counsel sign-off, is the only defensible posture; the chapter does not say so.
**Fix:** rewrite the closing paragraph of §Recovery-event audit trail to state: "Recovery audit records are retained by default for the deployment's regulatory retention period. Crypto-shredding the data subject's content stub on Article 17 request is technically possible; whether the surrounding trustee/custodian/timing metadata is also erasable is jurisdiction-specific and requires legal review. Default behavior is to preserve the metadata pending a written legal determination." This matches the existing GDPR §17 voice and removes the contradiction.

### Defended claims (tested, accepted)

- The honest-limitation paragraph (Ch15:204–205) does what it claims: it limits the architecture's claims rather than overclaiming, which a careful counsel reads as good-faith.
- The cross-reference to #32 (succession arrangements with executor delegation) is the right pointer for the estate-planning legal question; the chapter does not pretend to solve succession in this section.
- The Ch20 grace-period explanation ("If this is not you, contact your trustees immediately") is a defensibly user-comprehensible disclosure, which matters under jurisdictions that require the user to be informed in plain language.
- The "What This Section Does Not Solve" subsection (Ch15:223–231) is exactly the document a counsel wants to point to when scoping liability — the architecture's own admission of its boundaries is itself a legal artifact.

---

## SEAT 5 — The Outside Observer (Kelsey/Ferreira-equivalent — honesty and accessibility to a non-specialist)

**Score: 7.4 / 10**
**Verdict: PROCEED**

### Top 3 findings

**F1 — §A.5 boundary section is excellent in tone but understates the most painful real-world case (Ch15:223–231).**
The three failure modes named (skip setup; designate-then-decay; pre-arrangement-decay) are correct and honestly stated. The case missing — and the one a non-specialist reader will recognize from real headlines — is the *user who designates trustees who turn out to be malicious*. Not "compromised" as in the threat-model section (a separate concern), but actively bad-faith trustees. A user asks five family members to be trustees; three of them collude during a divorce or inheritance dispute and complete recovery against the user's living wishes. The grace period helps if the user is online and notified; if the user is travelling, hospitalized, or simply not checking that channel, the trustees-acting-in-bad-faith case is the case the boundary section should name. As written, the user is implicitly assumed to be a passive cryptographic principal whose only failure modes are skip/decay. Real users have hostile family members.
**Fix:** add a fourth bullet to §A.5: "A user whose designated trustees act in bad faith — coordinated coercion in a family or business dispute — has limited defense beyond the grace-period dispute window. Selection of trustees with no shared interest in the user's data is the user's responsibility; the architecture cannot grade trustee motivations." This is consistent with the existing voice and makes §A.5 cover the case a non-specialist reader actually fears.

**F2 — Ch20 grace-period explanation is good, but the silence-as-signal paragraph is jarring on first read (Ch20:224).**
The paragraph "If the original holder has genuinely lost all notification channels — no running devices, no email access, no SMS — the silence is the signal. The grace period elapses, and recovery completes." is correct, philosophically necessary, and *unsettling* to a non-specialist reader because it reads as "if you really lose everything, your account quietly transfers to whoever asked." The non-specialist reaction is "wait, what?" — the architecture is doing the right thing, but the prose places the reader in the panic state without giving them an exit. A single grounding sentence reframes the silence as the design choice it is: this is the only way to recover when you have truly lost everything, and the alternative would be to give up the recovery altogether.
**Fix:** add one sentence after the paragraph: "This is the architecture's deliberate choice — without it, a user who genuinely lost everything would have no recovery path at all. The trade-off is open and acknowledged; the grace period exists precisely to make the silence detectable while there is still time." Twenty-five words; converts the unsettling moment into a comprehensible design choice.

**F3 — The six mechanisms are presented in order of complexity, not in the order a non-specialist reader would actually choose them (Ch15:135–189).**
The order — multi-sig social → custodian → paper-key → biometric → grace-period → audit trail — is logically defensible but reads as an essay-by-cryptographer, not a decision-helper. A non-specialist reader making a real choice would benefit from the deployment-class table appearing *before* the mechanism descriptions, not after. The current structure forces the reader through the cryptography first and then offers the recommendation; the inverse — recommendation first, then cryptography — matches the book's elsewhere-stated "decision before reasoning" voice principle (CLAUDE.md style guide: "Lead with the punchline. Decision before reasoning. Constraint before implementation detail.").
**Fix:** consider promoting the deployment-class recommendations table (Ch15:213–215) above the six-mechanism descriptions, with a forward-pointing line: "Three deployment classes use the mechanisms below in different combinations. The remainder of this section describes each mechanism; the table at the end summarizes which combinations apply to each class." This is a structural edit, larger than the others; flag P2 not P0.

### Defended claims (tested, accepted)

- The Ch20 grace-period UI copy ("Your recovery will complete in 14 days unless your existing device or account disputes this request. If this is not you, contact your trustees immediately.") is plain-language correct and emotionally calibrated for the moment of greatest user stress.
- The "Trust three friends / Trust your bank or lawyer / Trust a piece of paper in a safe" framing (Ch20:190) is exactly the right register for a non-specialist first-run; the cryptographic mechanisms are correctly hidden beneath the metaphor.
- The §A.5 honest-boundary section's voice ("the user must act on the reminder", Ch15:229) is correct in placing responsibility on the user rather than overclaiming architectural automation.
- The 12-month recovery-readiness audit cadence with explicit reasoning ("not so frequent that users dismiss it", Ch20:234) is a thoughtful UX detail that an outside observer will read as evidence of careful design.

---

## CONSOLIDATED ACTION ITEMS

### P0 — must-fix before publication (any council member voted BLOCK)

| # | Raised by | Action | Cost |
|---|---|---|---|
| P0-1 | Pedantic Lawyer F1 | Add a paragraph to Ch15 §Custodian-held backup key naming the three liability postures (disclaims, bounded cap, joint liability) and the regulated-industry default. Cross-reference Appendix F. | ~100 words |
| P0-2 | Pedantic Lawyer F2 | Add a sentence to Ch15 §Multi-sig social recovery flagging that trustee residency may trigger data-residency obligations under DPDP / PIPL / DIFC DPL; deployments subject to localization name in-jurisdiction trustees or document an exception. | ~40 words |
| P0-3 | Pedantic Lawyer F3 + Theorist F3 | Rewrite the closing paragraph of Ch15 §Recovery-event audit trail to state the default-preserve posture for trustee/custodian metadata under Article 17, with case-specific legal review for erasure of metadata referring to third parties. | ~60 words |

### P1 — should-fix to lift chapter quality

| # | Raised by | Action | Cost |
|---|---|---|---|
| P1-1 | Theorist F1 | Add a Shamir-dealer specification paragraph to Ch15 §Multi-sig social recovery: GF(2^256) field, dealer is on user device, shares wrapped under trustee public key before transit, dealer state zeroed. | ~70 words |
| P1-2 | Theorist F2 | Add a "Recovery state-machine convergence" paragraph defining tiebreak (signed dispute event halts recovery; concurrent completion events rejected on convergence) and partition-tolerance posture. | ~80 words |
| P1-3 | Production Operator F1 | Add a heartbeat-mechanism paragraph in Ch15 §A.5 (or as new operator note): quarterly liveness ping per trustee with degraded-arrangement banner when active count falls below threshold + 1. | ~80 words |
| P1-4 | Production Operator F2 | Add a sentence to Ch15 §Custodian-held backup key naming custodian-transient-failure as a case requiring secondary recovery; relying on one custodian is a single point of failure for recovery. | ~30 words |
| P1-5 | Production Operator F3 | Add a paragraph to Ch20 §Trustee Designation Flow (or new analog section) requiring round-trip transcription verification at paper-key setup time. | ~40 words |
| P1-6 | Skeptical Implementer F1 | Add an "Implementation surfaces" paragraph at the end of Ch15 §Key-Loss Recovery listing the named event types: recovery-claim, grace-period observer, trustee-attestation, completion, dispute. Mark `// illustrative`. | ~60 words |
| P1-7 | Skeptical Implementer F2 | Add a sentence to Ch15 after the deployment-class table specifying that deployment class is declared at first-run, persists in the team's signed configuration manifest, and binds threshold + grace period. | ~30 words |
| P1-8 | Skeptical Implementer F3 | Rewrite the Ch20 first-run choice screen prompt to surface primary + secondary mechanism selection, matching Ch15's deployment-class composition. | ~30 words |

### P2 — nice-to-have / stylistic

| # | Raised by | Action |
|---|---|---|
| P2-1 | Outside Observer F1 | Add a fourth bullet to Ch15 §A.5 covering the bad-faith-trustees case (family/business dispute coordination). |
| P2-2 | Outside Observer F2 | Add one grounding sentence after the silence-as-signal paragraph in Ch20 §Time-Locked Grace Period. |
| P2-3 | Outside Observer F3 | Consider promoting the deployment-class table above the six-mechanism descriptions in Ch15 §Key-Loss Recovery (structural; lead-with-the-punchline). |

---

## OVERALL ROUND-1 VERDICT

**REVISE.**

Three council members vote PROCEED WITH CONDITIONS, one votes PROCEED outright (Outside Observer), and one votes BLOCK (Pedantic Lawyer). Three P0 issues raised, all by the Pedantic Lawyer, all in the legal-defensibility space — none of them require a structural rewrite, but each is a publication-stop for a chapter targeting HIPAA / PCI / financial-services audiences. Eight P1 conditions and three P2 stylistic notes round out the action list.

The **single most important finding** is **P0-1** (custodian liability allocation): the chapter currently asserts that liability is allocated by contract without naming what the three postures look like, and a regulated-industry buyer reading this section will close the book at that point. Of the three P0 items, this one is the highest-leverage — it is the one that turns the chapter from "honest-but-incomplete" to "publication-ready for the regulated audience the deployment-class table targets."

Verdict path forward: address the three P0 items in a focused revision pass (~200 words total across two locations), then the chapter clears the council. The eight P1 items can land in a second polish pass without blocking publication of the section, but should not be silently dropped — each closes a specific reviewer concern that will resurface in real-world implementation reviews.

**Round-1 totals:** 3 P0 / 8 P1 / 3 P2 action items. Five council members reviewed; one BLOCK, three PROCEED WITH CONDITIONS, one PROCEED.
