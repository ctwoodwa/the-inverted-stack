# Literary Board Review -- Extension 48 Key-Loss Recovery

**Date:** 2026-04-26
**Scope:** Two sections -- Ch15 Key-Loss Recovery (between Key Compromise Incident Response and Offline Node Revocation and Reconnection) and Ch20 Key-Loss Recovery UX (between The First-Run Experience and Accessibility as a Contract).
**Context:** These sections cleared the Kleppmann Council Round 2 with a PUBLISH verdict: 0 P0, 0 P1, 4 P2 stylistic items, all non-blocking. Three Round 1 BLOCK findings (all legal-defensibility issues from the Pedantic Lawyer) were conclusively resolved. The polish pass applied the four R2 P2 items, including the structural reorder that promotes the deployment-class table above the six mechanisms. This literary board review brings the complementary editorial and global-market lens: prose craft, argumentative coherence, global regulatory coverage, accessibility, and market fit across Dubai/India, East Asia/APAC, Europe, Africa, Latin America, and CIS/Eastern Europe.

---

## Critic 1 -- Eleanor Chase
**Role:** Executive Editor (Acquisitions)
**Score: 8.5/10 | Verdict: POLISH**

These two sections are among the strongest Part III and Part IV content in the book. Ch15 earns its insertion point: it sits between an attacker-driven scenario (compromise) and an operator-driven scenario (offline revocation), and key-loss as user-driven failure is categorically distinct from both. The Why this matters opening names the genuine cost before naming any mechanism. The phrase Users who lose their keys lose their data. That boundary is the architecture honest edge is a sentence worth the page count it occupies.

The deployment-class table now leading the section is the right editorial call. Decision before reasoning. A practitioner can read one row and know the recommendation before diving into six sub-sections of cryptographic construction. This is the book stated rhetorical contract and it holds here.

The six mechanisms are cleanly sequenced. Each sub-section has a discernible shape: construction, threat model, deployment fit. The prose does not repeat the architecture from Part I; it assumes the reader has read Ch15 earlier sections.

Two friction points. First, the cross-reference cluster in Why this matters (cross-reference 32, Volume 2 / cross-reference 18) appears before the mechanisms are established. Readers who have not read the volume 2 roadmap encounter a pointer that sends them nowhere current. A brief subordinate clause (described in a future volume) absorbs the pointer. Second, the What This Section Does Not Solve subsection has grown to contain both limitation enumerations and one mitigation (the quarterly heartbeat). The opening sentence says Five failure modes are outside the scope -- which then contradicts itself by describing the trustee-decay mitigation. Either rename the subsection to Limits and Mitigations or move the heartbeat paragraph to the trustee-decay mechanism text.

Ch20 Key-Loss Recovery UX is proportionate to its subject. The Trust three friends / Trust your bank or lawyer / Trust a piece of paper in a safe plain-language framing is pitch-perfect for non-technical adopters. The round-trip transcription verification mandate (Skipping it is not an option) has exactly the production-grade register Part IV requires.

**Defended claims:** The Why this matters opening earns its position; the deployment-class table structure is correct; the Skipping it is not an option mandate is right in register; the five named Implementation Surfaces contracts are a genuine addition to the specification.

**Action items:**
- Reframe the Volume 2 / cross-reference 18 pointers in Why this matters as a brief subordinate clause (described in a future volume) so readers on the current volume are not derailed.
- Either rename What This Section Does Not Solve to Limits and Mitigations or move the quarterly-heartbeat paragraph into the trustee-decay mechanism text so the subsection does what its heading promises.
- Add one sentence at the close of Ch20 Recovery Completion Confirmation explicitly connecting the recovery event back to the periodic readiness audit.

---

## Critic 2 -- Marcus Webb
**Role:** CTO / Target Practitioner
**Score: 8/10 | Verdict: POLISH**

Would I change architectural decisions based on this? Yes, on two specific points. First, the deployment-class table answers the question I carry into any mechanism-heavy specification: given my deployment class, what do I actually implement? Getting that table upfront is the correct engineering-book design. Second, the five named event contracts -- RecoveryClaimSubmitted, GracePeriodObserver, TrusteeAttestation, RecoveryDispute, RecoveryCompleted -- give me enough surface to start integration planning.

The mechanisms are appropriately concrete. The dealer protocol paragraph is specification-grade: GF(2^256), local dealer, OS CSRNG, shares wrapped under trustee public key, dealer state zeroed post-emission. I can hand this to a principal engineer and say implement this. The Argon2id parameters are explicit and cross-referenced to the existing key hierarchy.

Three things I would fix before recommending this to principal engineers. First: the convergence rule for custodian-release events is acknowledged as a gap in R2-N1 but the confirming sentence has not been added to the prose. A custodian release is a single signed event; the dispute-halt rule should apply identically and the text should say so. Second: Ch20 Recovery Initiation UX says the application retrieves the recovery arrangement on a fresh device -- but how does a fresh device with no existing session retrieve the arrangement metadata? The retrieval path is unspecified. Third: Recovery Completion Confirmation says the new device receives the wrapped KEKs -- from whom? Relay, custodian, trustee, or local reconstruction from the recovered root seed? An implementer cannot build this without knowing the delivery channel.

The Ch20 UX descriptions are precisely calibrated. Three of your five trustees must agree before your data can be recovered. Pick five people you trust who do not all know each other operationalizes collusion diversity without requiring the user to understand Shamir.

**Defended claims:** The deployment-class table is a genuine architectural contribution; the dealer protocol paragraph is specification-complete; the biometric technical-review annotation is the correct treatment for platform-specific claims; the five event contracts provide an implementable integration surface.

**Action items:**
- Explicitly confirm in Recovery State-Machine Convergence that the dispute-halt rule binds custodian-release events identically to trustee-completion events (R2-N1 from council -- still not in body text).
- Add one sentence in Ch20 Recovery Initiation UX specifying how a fresh device with no existing session retrieves the recovery arrangement metadata.
- Add one sentence in Recovery Completion Confirmation specifying the KEK delivery channel after successful recovery.

---

## Critic 3 -- Ingrid Halvorsen
**Role:** Prose Editor
**Score: 8/10 | Verdict: FLOWING**

These sections read. That is not faint praise for specification prose. Most Part III writing grinds -- long sentences accumulating clauses in the name of precision, paragraphs that are lists wearing prose clothing. This section mostly avoids all of that.

The best prose is in the threat-model sub-sections. An adversary who can submit a recovery claim and also suppress the original holder notifications for fourteen days has a substantially harder problem than an adversary who can complete recovery in seconds -- that sentence moves. It names the attacker actual problem, not the defender abstract property.

Several sentences in the six-mechanism sub-sections run dense. The multi-sig social recovery opening packs the Shamir construction, the n-of-t threshold, two example thresholds, two citations, and the dealer protocol into four consecutive sentences. The paragraph cap is not breached, but the cognitive load in those early paragraphs is higher than the rest of the section.

The custodian liability paragraph (three postures labeled a/b/c) is specification-precise but reads as a legal contract excerpt. Four sentences precede the posture list; those four could compress to two without losing information.

The What This Section Does Not Solve fifth failure mode ends awkwardly: water damage, faded ink, transcription error at first-run, mouse damage in storage -- mouse damage in storage is a jarring specific after three more generic causes. Cut or replace with a parallel-weight cause.

The Ch20 prose is cleaner than Ch15, as Part IV should be. The Trust three friends triad has real rhetorical energy. The grace-period paragraph naming the shared-screen visibility concern (anyone who might see the message on a shared screen) is the kind of detail most UX writing ignores.

**Defended claims:** The threat-model paragraphs are the section best prose; the Trust three friends triad is rhetorically effective; the shared-screen observation is a genuine prose contribution; the paragraph-length cap holds throughout.

**Action items:**
- Reduce clause density in the multi-sig social recovery opening two paragraphs -- spread Shamir, threshold, and threshold-rationale concepts across more paragraph-opening sentences.
- Compress the custodian liability paragraph lead-in from four sentences to two; the posture labels carry more weight than the introduction gives them.
- Replace or cut mouse damage in storage in the fifth failure mode of What This Section Does Not Solve -- it breaks the parallel syntactic weight of the preceding causes.

---

## Critic 4 -- Jerome Nakamura
**Role:** Technology Analyst (Argument)
**Score: 8/10 | Verdict: COMPELLING**

The argument structure is sound. The section opens with the architecture honest edge -- Users who lose their keys lose their data. That boundary is the architecture honest edge -- which is the steelman-the-tradeoff move that converts advocacy into analysis. A skeptic reading Ch15 for the first time cannot accuse the author of hiding the cost.

The six mechanisms are correctly sequenced from individual to institutional. Multi-sig social (individuals, small partnerships) through custodian (enterprise, regulated) through the composable grace-period layer to the audit-trail substrate. The deployment-class table makes the sequencing rationale explicit.

The honest-limitation paragraph closing Threat Model -- Recovery as Attack Vector is the argument strongest moment: no recovery primitive defeats a sufficiently patient adversary with simultaneous control of every recovery channel. The architecture bounds the attack cost. It does not bound it to infinity. That sentence earns the trust of a skeptical enterprise architect.

Three argumentative gaps remain. First: the deployment-class table row entries do not explicitly point to the mechanism sub-sections they reference. A single bridging sentence after the table (The regulated combination composes mechanisms 48b and 48a; the consumer combination composes 48a and 48c) closes this. Second: Ch20 Recovery Initiation UX says the application retrieves the recovery arrangement on a fresh device -- but the retrieval path from a device with no prior session is unspecified. Third: Recovery Completion Confirmation says the new device receives the wrapped KEKs without naming the delivery source. Both are one-sentence fixes; both are more than editorial -- they are architectural claims the text must answer.

**Defended claims:** The honest-limitation close of Threat Model is the section strongest argumentative moment; the deployment-class table is correctly positioned as a decision tool; the tradeoff acknowledgment in Why this matters earns the trust of skeptical readers.

**Action items:**
- Add one bridging sentence after the deployment-class table connecting row entries to the specific mechanism sub-sections that follow.
- Add one sentence in Ch20 Recovery Initiation UX explaining how a fresh device retrieves the recovery arrangement metadata.
- Add one sentence in Recovery Completion Confirmation specifying the KEK delivery channel after successful recovery.

---

## Critic 5 -- Dr. Amara Osei
**Role:** Academic Reviewer
**Score: 8.5/10 | Verdict: SOUND**

For a practitioner book, the technical claims are well-anchored. The Shamir secret-sharing citation is correct (Shamir 1979, Communications of the ACM vol. 22 no. 11). The biometric template non-exportability claim for Apple Secure Enclave, Pixel Titan M, and Windows Pluton is marked with a technical review comment confirming verification against platform security documentation -- an honest epistemic flag that the claim depends on platform architecture, not the book own reasoning. The Argon2id parameters are cross-referenced to the Key Hierarchy section, which is the correct treatment for parameters appearing in multiple specification contexts.

The GF(2^256) field specification for the Shamir dealer is consistent with standard practice. The threshold guarantee holds.

Two precision concerns. First: Recovery State-Machine Convergence describes the convergence rule as strict halt-on-dispute and says nodes apply the completion locally and reverse it when the dispute event arrives during sync. This is an eventually consistent reversibility model, not a strictly atomic model. Between the local application of the completion and the arrival of the dispute event, there is a window where the new key is in effect locally. The section should distinguish strict (globally atomic) from eventually consistent with reversal to avoid overclaiming. This is a framing precision issue that technically careful readers will probe. Second: the biometric template non-exportability claim is accurate for the referenced platforms as currently documented, but these security architectures are updated with each hardware generation. As documented at the time of writing makes the claim scope transparent.

**Defended claims:** Argon2id parameter sourcing is precise and cross-referenced; the honest-limitation close correctly characterizes the architecture bound without overclaiming; the six-mechanism taxonomy is internally consistent; the Shamir citation is correctly placed and formatted.

**Action items:**
- Revise Recovery State-Machine Convergence framing to distinguish global log semantics (no conflicting completion accepted at validation) from local node behavior (completion applied locally, reversed on dispute arrival) -- the current strict halt language overclaims the consistency model.
- Add as documented at the time of writing to the biometric template non-exportability claim.
- Confirm via a technical review comment that the Shamir dealer GF(2^256) CSRNG output is uniformly distributed over the field.

---

## Critic 6 -- Meera Krishnamurthy
**Role:** Regional Market Specialist (Dubai / India)
**Score: 8.5/10 | Verdict: GLOBALLY POSITIONED**

This section is materially stronger than anything the board reviewed in April 2026. The social-recovery jurisdictional paragraph naming DPDP, PIPL, and DIFC DPL trustee-residency obligations with an Appendix F cross-reference is the critical addition. A DIFC-licensed financial entity architect reading this knows immediately that trustee residency is a compliance parameter, not a social choice.

The Ch20 backup-target jurisdiction paragraph is the section most practical contribution to India and UAE deployment contexts: per-jurisdiction specificity for 242-FZ, DPDP, and UAE DPL 2022, with explicit UX behavior (block selection of out-of-jurisdiction options with a plain-language explanation). This converts a compliance requirement into a concrete UX behavior.

One gap remains for the GCC market. The DIFC Data Protection Law 2020 is named correctly, but the Abu Dhabi Global Market (ADGM) has its own framework -- the ADGM Data Protection Regulations 2021 -- applicable to entities licensed in ADGM. DIFC and ADGM are legally separate free zones; ADGM is Abu Dhabi financial free zone, DIFC is Dubai. A solution sold to ADGM-licensed entities needs the ADGM DPR named. One parenthetical alongside the DIFC DPL entry closes this.

The RBI data localization circular for Indian BFSI deployments is not named in the recovery sections. Recovery key storage and trustee residency are precisely the data flows RBI scrutinizes. A parenthetical in the Ch20 DPDP entry -- Indian BFSI deployments additionally consult the RBI data localization circular -- is proportionate.

**Defended claims:** The DPDP + PIPL + DIFC DPL trustee-residency paragraph is correctly placed and scoped; the Ch20 backup-target jurisdiction UX behavior is precisely specified; the deployment-class table regulated tier maps cleanly to Indian BFSI and GCC financial contexts.

**Action items:**
- Add ADGM Data Protection Regulations 2021 as a parenthetical alongside DIFC DPL 2020 in the trustee-residency paragraph.
- Add a parenthetical to the Ch20 Indian DPDP entry noting that BFSI deployments should additionally consult the RBI data localization circular for recovery-key storage decisions.

---

## Critic 7 -- Prof. Raymond Hollis
**Role:** Narrative Rhetorician
**Score: 8/10 | Verdict: COHESIVE**

These two sections function as a policy/UX pair and the pairing is structurally sound. Ch15 establishes the cryptographic constructions, threat model, deployment combinations, and implementation surfaces. Ch20 surfaces each as a UX flow the user walks through. The forward reference in Ch15 and the backward reference in Ch20 give the reader explicit navigational anchors. This is the correct rhetorical architecture for a policy/UX split across chapters.

The most rhetorically effective moment is the Why this matters opening. It names the cost before naming the capability. The list of five real-world failure modes (forgotten password, lost device, factory reset, hardware token stolen, death without succession) achieves emotional grounding without sentimentality.

The Ch20 silence-as-signal passage is the section most rhetorically difficult moment. The grounding paragraph (Without the silence-completes rule, a user who genuinely lost everything would have no recovery path at all) handles it correctly. The ordering in Ch20 is gate-before-rationale -- a deliberate exception to the book decision-before-reasoning contract. The narrative logic is stronger than the contract here: the reader needs to feel the strangeness of the gate before they are ready for the explanation. I would keep this ordering, but the author should make the choice consciously.

One narrative gap: the Ch20 section ends with an outward pointer to Ch15 as its closing move. The reader is pointed away before the section has acknowledged its own closure. A single closing sentence returning the reader to the Ch20 arc would complete the rhetorical structure.

**Defended claims:** The policy/UX pairing structure is the right architectural choice; the Why this matters opening achieves grounding without sentimentality; the forward/backward cross-reference pair is correctly implemented; the honest edge framing is the section best rhetorical contribution.

**Action items:**
- Add one closing sentence to Ch20 Recovery Completion Confirmation returning the reader to the chapter arc before the outward pointer to Ch15.
- Confirm consciously whether the gate-before-rationale ordering in the silence-as-signal passage is the intended exception to decision-before-reasoning.

---

## Critic 8 -- Sofia Reyes
**Role:** Accessibility Consultant (Latin America)
**Score: 8/10 | Verdict: INCLUSIVE**

The accessibility treatment here is materially better than what the board saw in April 2026. The adjacent Accessibility as a Contract section establishes the ARIA contract that the recovery flows depend on -- role=status with aria-live=polite for ambient changes, role=alert with aria-live=assertive for action-required states.

Within Key-Loss Recovery UX specifically: the trustee designation screen updates in real time (Trustee 1: confirmed. Trustee 2: confirmed. Trustees 3 through 5: pending) -- this is a dynamic state change that requires an ARIA live region announcement. The text does not specify which ARIA pattern applies. The count increment is neither ambient background noise nor an emergency alert. An explicit assignment from the adjacent taxonomy would close the ambiguity.

The grace-period progress display has the same ambiguity for assistive technology users. The user can check progress without refreshing implies a polling model for sighted users; for screen reader users, push announcements and pull updates have different behavioral implications.

The recovery flows use plain-language register throughout -- appropriate for users under stress. Someone is requesting recovery of your account. If this is not you, dispute this request now is direct.

For Latin American deployments specifically: in rural Brazil (Northeast, Para, Amazonas), rural Mexico (Oaxaca, Chiapas), and rural Colombia, the grace-period dispute notification may not reach the original holder if their only connectivity is 2G or intermittent. The multi-channel notification section correctly acknowledges an undisputed claim in a channel the user does not monitor is the architecture honest limitation -- but a user in these environments may have no reliable second digital channel. One sentence directing low-connectivity deployments to configure at least one trustee reachable through an in-person channel would close this.

**Defended claims:** The plain-language register is appropriate for users under stress; the multi-channel notification framing is the correct architectural response to single-channel attack vectors; the transcription verification mandate is the right accessibility and usability constraint.

**Action items:**
- Specify the ARIA live region contract for the trustee designation real-time update screen (aria-live=polite for count increments, aria-live=assertive for threshold-met/failed states), consistent with the Accessibility as a Contract taxonomy.
- Add one sentence in Time-Locked Grace Period UX directing low-connectivity deployments to configure at least one trustee reachable through an in-person or offline channel.

---

## Critic 9 -- Yuki Tanaka
**Role:** East Asian / APAC Editorial
**Score: 8/10 | Verdict: TRANSLATES WITH ADAPTATION**

The social-recovery jurisdictional paragraph names DPDP, PIPL, and DIFC DPL trustee-residency obligations. PIPL is present, which is a material improvement over earlier chapters. The Appendix F cross-reference carries the weight for APPI and PIPA.

For the East Asian enterprise market, the custodian-held backup key mechanism is the most relevant. Japanese enterprises will recognize the custodian relationship as analogous to existing trusted intermediary structures (trust banks, legal escrow, regulated custody). The SMB description (a lawyer or accountant) maps less cleanly to Japanese enterprise culture, where the equivalent relationship is more likely with a system integrator (NTT Data, Fujitsu, NEC) acting in a trust role. A brief parenthetical acknowledging that regulated cloud custodians and institutional intermediaries -- not only law firms and banks -- can fulfill the custodian role would make the mechanism legible to Japanese and Korean enterprise readers.

The Recovery State-Machine Convergence section satisfies the Japanese engineering culture expectation of formal-enough specification: the convergence rule is named, the asymmetric-authority justification is given, the enforcement layer is identified. Japanese technical readers in regulated financial services contexts will probe the applied locally and reversed on late dispute arrival behavior that Dr. Osei also flags. This is a precision gap the revision pass should address.

The Chinese regulatory context is adequately handled through PIPL in the trustee-residency paragraph. MLPS 2.0 categorization implications for recovery event logging are appropriately a Ch19 concern.

The Ch20 UX flows will translate structurally. The Trust three friends plain-language framing requires cultural localization for Japanese-language editions -- trustee relationships carry different cultural weight -- but the UX structure is sound.

**Defended claims:** The PIPL trustee-residency paragraph is correctly placed and scoped; the Recovery State-Machine Convergence section is specification-complete enough for Japanese engineering culture; the five named event contracts provide an adequate integration starting point.

**Action items:**
- Add a brief parenthetical in Custodian-held backup key acknowledging that regulated cloud custodians and institutional intermediaries can serve the custodian role, not only law firms and banks.
- Flag for translation notes: the Trust three friends plain-language framing requires cultural localization for Japanese-language editions.

---

## Critic 10 -- Dr. Imogen Barker
**Role:** European Editorial
**Score: 8.5/10 | Verdict: RIGOROUS**

The legal treatment in these sections is materially tighter than anything from the April 2026 session. The three Round 1 BLOCK findings are conclusively resolved. The GDPR Article 17 treatment is now defensible: crypto-shredding is correctly described; the audit-trail tension is correctly named; the metadata-residue limitation is acknowledged; the Section 17(3)(b) exemption argument is correctly flagged as jurisdiction-dependent and requiring legal review.

Schrems II is present and correctly cited in Ch15 Relay Trust Model. The recovery sections do not need to re-cite it because the key custody model (keys never leave originating nodes) is already the Schrems II answer, and the relay trust model cross-reference carries the argument.

One European precision gap: the trustee-residency paragraph names DPDP Act, PIPL, DIFC DPL, and similar regimes but the most directly relevant regime for European deployments is GDPR Chapter V (transfer mechanism requirements). A trustee resident outside the EU/EEA is a data transfer recipient under GDPR if the recovery key fragment constitutes personal data -- which a share derived from the user root recovery key may. The closing line (The cryptographic construction is sound everywhere; the legal classification of the trustees role is not) is exactly correct. But the GDPR Chapter V transfer mechanism question for EU-resident users with non-EU trustees is not named. One sentence makes the European compliance posture explicit.

The Implementation Surfaces disclaimer that the concrete event schema lands when Sunfish.Foundation.Recovery reaches its first milestone is an honest forward-looking marker. European buyers evaluating pre-1.0 software will read this correctly.

**Defended claims:** The GDPR Article 17 treatment is defensible as written; the Schrems II argument is present and correctly cross-referenced; the custodian liability posture enumeration is complete; the metadata-residue limitation is correctly acknowledged as jurisdiction-specific.

**Action items:**
- Add one sentence to the trustee-residency paragraph naming GDPR Chapter V transfer mechanism requirements for EU-resident users whose trustees reside outside the EU/EEA.
- Confirm the Article 17(3)(b) exemption argument applies under the German BDSG national implementation -- BDSG has specific exemption interpretations that diverge from the GDPR floor.

---

## Critic 11 -- Amina Diallo
**Role:** African Technology Markets
**Score: 7.5/10 | Verdict: RELEVANT WITH EXPANSION**

This section is more globally aware than earlier chapters in the book. The consumer-tier deployment class -- designed for simplicity at the expense of institutional structure -- maps cleanly to African consumer and SMB deployments where no lawyer-custodian relationship exists as a default. The paper-key fallback section explicitly acknowledges deployments where digital escrow is itself a higher risk than physical paper including an individual deploying in a jurisdiction where digital custody creates legal exposure -- a sentence that describes large swaths of the African deployment landscape without naming them.

The adjacent Designing for Failure Modes section correctly frames offline as the operational baseline with an explicit Sub-Saharan Africa reference. The recovery sections should hold the same standard -- and they mostly do, with one real gap.

The grace-period mechanism assumes notification-channel delivery is reliable over the full grace-period window. In Nigeria, where load-shedding is routine and network outages follow power outages, a 14-day grace period may pass during which the original holder devices are offline, email unreachable, and SMS unavailable. The silence is the signal architecture is correct in principle. But the text should acknowledge that in high-outage environments, the effective notification window may be shorter than the nominal grace period.

The Nigerian (NDPR), South African (POPIA), and Kenyan (DPA) regimes appear via and similar regimes in the trustee-residency paragraph. POPIA Section 72 cross-border transfer requirements for trustee key fragments are more precise than the generic cluster implies. For South African financial services deployments, one named reference would be proportionate.

**Defended claims:** The consumer-tier deployment class correctly maps to African SMB and consumer contexts; the paper-key fallback digital-escrow-as-higher-risk acknowledgment covers the African context correctly; the adjacent Designing for Failure Modes section correctly frames offline as the operational baseline.

**Action items:**
- Add one sentence in Time-Locked Grace Period UX acknowledging that in high-outage environments, notification-channel delivery cannot be assumed over the full grace period; deployments in these environments should treat the grace period as a floor, not a guaranteed delivery window.
- Add POPIA Section 72 as a named cross-border transfer reference for South African deployments alongside the and similar regimes trustee-residency cluster, or in the Appendix F South Africa entry.

---

## Critic 12 -- Aleksei Volkov
**Role:** CIS / Eastern European Technology Independence
**Score: 8.5/10 | Verdict: GLOBALLY COMPLETE**

The 2022 SaaS service terminations are named in Ch15 Relay Trust Model (The 2022 demonstration) and the architectural argument is correctly stated: Organizations replacing Western SaaS under import substitution mandates find the architecture directly aligned with their adoption driver. The recovery section does not repeat this, which is correct.

For CIS readers, the recovery mechanisms interact directly with data-sovereignty and import-substitution concerns. The paper-key fallback -- which defeats cold-boot and hibernation attacks during an offline key-recovery operation -- is directly relevant to deployments where the threat model includes state-level infrastructure access: a key that never touches a networked system cannot be compelled from a cloud provider. The custodian local-unwrap model (The custodian does not hold the key in plaintext; they hold a wrapped copy that Sunfish.Foundation.Recovery unwraps on the user device after the custodian releases it) is the correct architectural response to compelled-access threat models.

Federal Law 242-FZ is currently carried by and similar regimes in the trustee-residency paragraph. DPDP, PIPL, and DIFC DPL are named explicitly. Naming 242-FZ explicitly alongside them would give CIS readers the same treatment other jurisdictions receive.

One additional gap: What This Section Does Not Solve does not acknowledge that in jurisdictions with mandatory key-escrow requirements -- not currently in force in Russia but present in some ECOWAS states and under active consideration in several CIS policy discussions -- the architecture recovery mechanisms may conflict with or be superseded by government-mandated escrow. One sentence closes this without overstating the current regulatory situation.

**Defended claims:** The Relay Trust Model 2022 demonstration paragraph is present and correctly scoped; the import substitution framing is correctly attributed; the paper-key offline-only model is the correct answer to compelled-access threat models; the custodian local-unwrap model is correctly positioned as the CIS-deployment-relevant cryptographic property.

**Action items:**
- Name 242-FZ explicitly in the trustee-residency paragraph rather than carrying it via and similar regimes.
- Add one sentence in What This Section Does Not Solve acknowledging that mandatory key-escrow requirements, where they apply, supersede user-held recovery and require separate compliance review.

---

## Consolidated Action Items

### P0 -- Must fix before publication

None.

---

### P1 -- Should fix to lift publication quality

| # | Raised by | Chapter | Issue |
|---|---|---|---|
| P1-1 | Webb, Nakamura | Ch20 | The fresh-device recovery arrangement retrieval path is unspecified: how does a device with no existing session retrieve the arrangement metadata (mechanism type, trustee count, custodian identifier)? One sentence closes this gap. |
| P1-2 | Webb, Nakamura | Ch20 | The KEK delivery path after recovery completion is unspecified: the new device receives the wrapped KEKs -- from whom? Relay, custodian, trustee, or local reconstruction from recovered root seed? One sentence specifies the delivery channel. |
| P1-3 | Osei | Ch15 | Recovery State-Machine Convergence overclaims with strict halt-on-dispute when the actual model is eventually consistent reversal on late dispute arrival -- revise framing to distinguish global log semantics from local node behavior. |
| P1-4 | Webb, Nakamura (R2-N1 carried) | Ch15 | Explicitly confirm in body text that the dispute-halt convergence rule binds custodian-release events identically to trustee-completion events -- the council flagged this in R2-N1 and it remains absent from prose. |
| P1-5 | Barker | Ch15 | GDPR Chapter V transfer mechanism requirements for EU-resident users whose trustees reside outside the EU/EEA are not named in the trustee-residency paragraph -- one sentence names the most immediate European compliance implication. |

---

### P2 -- Nice-to-have / polish

| # | Raised by | Chapter | Issue |
|---|---|---|---|
| P2-1 | Chase | Ch15 | What This Section Does Not Solve opening sentence contradicts the heartbeat mitigation paragraph -- rename to Limits and Mitigations or relocate the heartbeat paragraph to the trustee-decay mechanism text. |
| P2-2 | Chase | Ch15 | Volume 2 / cross-reference 18 pointers in Why this matters send readers to non-existent current destinations -- add a brief subordinate clause (described in a future volume). |
| P2-3 | Chase, Hollis | Ch20 | Add one closing sentence to Recovery Completion Confirmation returning the reader to the Ch20 arc before the outward pointer to Ch15. |
| P2-4 | Nakamura | Ch15 | Add one bridging sentence after the deployment-class table connecting row entries to the specific mechanism sub-sections that follow. |
| P2-5 | Halvorsen | Ch15 | Compress the custodian liability paragraph lead-in from four sentences to two. |
| P2-6 | Halvorsen | Ch15 | Replace or cut mouse damage in storage in the fifth failure mode -- it breaks the parallel syntactic weight of the preceding causes. |
| P2-7 | Halvorsen | Ch15 | Reduce clause density in the multi-sig social recovery opening two paragraphs. |
| P2-8 | Hollis | Ch20 | Confirm consciously whether the gate-before-rationale ordering in the silence-as-signal passage is the intended exception to decision-before-reasoning. |
| P2-9 | Webb | Ch15 | GracePeriodObserver: clarify whether push events are supported alongside pull, and what the recommended minimum poll interval is to avoid log-validation thrash. |
| P2-10 | Webb | Ch20 | Add one sentence addressing backwards compatibility of the signed configuration manifest for users who configured recovery under an earlier single-mechanism model. |
| P2-11 | Osei | Ch15 | Add as documented at the time of writing to the biometric template non-exportability claim. |
| P2-12 | Osei | Ch15 | Confirm via technical review comment that the Shamir dealer GF(2^256) CSRNG output is uniformly distributed over the field. |
| P2-13 | Krishnamurthy | Ch15 | Add ADGM Data Protection Regulations 2021 parenthetical alongside DIFC DPL 2020 in the trustee-residency paragraph. |
| P2-14 | Krishnamurthy | Ch20 | Add a parenthetical to the Indian DPDP entry noting that BFSI deployments should additionally consult the RBI data localization circular for recovery-key storage decisions. |
| P2-15 | Tanaka | Ch15 | Add a brief parenthetical in Custodian-held backup key acknowledging that regulated cloud custodians and institutional intermediaries can serve the custodian role, not only law firms and banks. |
| P2-16 | Barker | Ch15 | Confirm the Article 17(3)(b) exemption argument applies under the German BDSG national implementation. |
| P2-17 | Reyes | Ch20 | Specify the ARIA live region contract for the trustee designation real-time update screen (aria-live=polite for count increments, aria-live=assertive for threshold-met/failed states). |
| P2-18 | Reyes, Diallo | Ch20 | Add one sentence in Time-Locked Grace Period UX directing low-connectivity deployments to configure at least one trustee reachable through an in-person or offline channel. |
| P2-19 | Diallo | Ch15 | Add POPIA Section 72 as a named cross-border transfer reference for South African deployments alongside the and similar regimes cluster, or in Appendix F. |
| P2-20 | Diallo | Ch15 | Add one sentence acknowledging that in high-outage environments, notification-channel delivery cannot be assumed over the full grace period -- treat the grace period as a floor, not a guaranteed delivery window. |
| P2-21 | Volkov | Ch15 | Name 242-FZ explicitly in the trustee-residency paragraph rather than carrying it via and similar regimes. |
| P2-22 | Volkov | Ch15 | Add one sentence in What This Section Does Not Solve acknowledging that mandatory key-escrow requirements, where they apply, supersede user-held recovery and require separate compliance review. |

---

## Overall Board Verdict

| Critic | Score | Verdict |
|---|---|---|
| 1. Eleanor Chase (Acquisitions) | 8.5 | POLISH |
| 2. Marcus Webb (Target Practitioner) | 8.0 | POLISH |
| 3. Ingrid Halvorsen (Prose) | 8.0 | FLOWING |
| 4. Jerome Nakamura (Argument) | 8.0 | COMPELLING |
| 5. Dr. Amara Osei (Academic) | 8.5 | SOUND |
| 6. Meera Krishnamurthy (Dubai/India) | 8.5 | GLOBALLY POSITIONED |
| 7. Prof. Raymond Hollis (Rhetorician) | 8.0 | COHESIVE |
| 8. Sofia Reyes (Accessibility/LATAM) | 8.0 | INCLUSIVE |
| 9. Yuki Tanaka (East Asia/APAC) | 8.0 | TRANSLATES WITH ADAPTATION |
| 10. Dr. Imogen Barker (European) | 8.5 | RIGOROUS |
| 11. Amina Diallo (African Markets) | 7.5 | RELEVANT WITH EXPANSION |
| 12. Aleksei Volkov (CIS/Eastern Europe) | 8.5 | GLOBALLY COMPLETE |

**Board score: 8.17/10**
**Board verdict: POLISH**

No critic voted REVISE or REWORK. No P0 items. Five P1 items address implementer-facing gaps that are each one-sentence fixes. The 22 P2 items are polish, precision, and global-market completions appropriate for a copyedit pass.

### Strengths to preserve

- Users who lose their keys lose their data. That boundary is the architecture honest edge. -- the section best sentence and its correct rhetorical foundation. Do not revise.
- The deployment-class table leading the section (structural reorder correctly applied). Decision before reasoning -- holds the book rhetorical contract.
- The Shamir dealer protocol paragraph: GF(2^256), local dealer, OS CSRNG, shares wrapped under trustee public keys before transit, post-emission zeroing. Specification-complete. Do not dilute.
- No recovery primitive defeats a sufficiently patient adversary with simultaneous control of every recovery channel. The architecture bounds the attack cost. It does not bound it to infinity. -- the honest-limitation close of Threat Model. The section strongest argumentative moment.
- The DPDP + PIPL + DIFC DPL trustee-residency paragraph -- correctly placed, correctly scoped, earned by three rounds of review.
- Trust three friends / Trust your bank or lawyer / Trust a piece of paper in a safe -- Ch20 first-run plain-language framing. Pitch-perfect register for non-technical users.
- The round-trip transcription verification mandate in Ch20: the application refuses to accept setup completion until the typed phrase matches the displayed one. Skipping it is not an option. Production-grade register correctly held.
- The silence-as-signal grounding paragraph in Ch20: Without the silence-completes rule, a user who genuinely lost everything would have no recovery path at all. Converts the section most philosophically difficult moment into a comprehensible design rationale.
- The Implementation Surfaces five named event contracts -- a genuine specification contribution.
- The Recovery State-Machine Convergence asymmetric-authority justification -- well-reasoned, enforcement layer correctly identified.
