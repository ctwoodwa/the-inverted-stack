# 9 — Chain-of-Custody for Multi-Party Transfers — Outline

**ICM stage:** outline → ready for draft.
**Target chapters:** Ch15 (security architecture, Part III) + Appendix B (threat-model worksheets).
**Total word target:** 2,500 words (Ch15 ~2,000; App B ~500).
**Source:** `docs/reference-implementation/design-decisions.md` §5 entry #9 (one-liner + §8.2 concept-addition note); cross-references in #48 outline §H and #45 draft §A.7 (`Sunfish.Kernel.Audit` substrate shared by both). Sub-patterns 9a–9c derived from the design-decisions framing ("multi-party signed transfer receipts, evidence-class temporal attestation") and the §8.2 note on `attested-with-chain-of-custody` as a distinct authenticity tier.
**Why this is seventh in the priority list:** chain-of-custody is a structural gap the book notes but never closes. Extensions #48 (key-loss recovery) and #45 (collaborator revocation) both cross-reference #9's multi-party signed-event substrate as the mechanism that underpins their own audit trails — meaning #9 is already invoked by two delivered extensions. Until #9 is written, those cross-references point at a void. Additionally, extension #47 established the THREAT-NN numbered format in Appendix B with THREAT-10, explicitly naming #9 as "notably THREAT-11 for chain-of-custody extension #9." This outline closes both gaps.

---

## §A. New section in Ch15 — "Chain-of-Custody for Multi-Party Transfers"

**Insertion point:** between the existing `## Supply Chain Security` section and the existing `## GDPR Article 17 and Crypto-Shredding` section. The narrative logic is deliberate. Supply Chain Security closes the build-pipeline adversarial-environment trilogy. GDPR Article 17 opens the compliance-layer considerations. Chain-of-custody sits at the seam: it is a cryptographic mechanism that serves both operational integrity (who handled this data, in what sequence, under what authority) and regulatory artifact (the signed record that satisfies evidence standards, regulatory-export mandates, and custody-chain requirements). Inserting between Supply Chain Security and GDPR Article 17 places chain-of-custody exactly where a reader moving from "how the architecture defends against adversaries" into "how the architecture satisfies compliance obligations" expects to find it.

**Word target:** 2,000 words.

**H2:** `## Chain-of-Custody for Multi-Party Transfers`

### A.1 Why this matters (≈200 words)

- The audit trail that §Key-Loss Recovery (sub-pattern 48f) and §Collaborator Revocation (sub-pattern 45f) both depend on is not merely a log. It is a chain-of-custody record: a signed, append-only sequence in which each entry attests to a specific act by a specific party at a specific moment. When those sections cross-reference "#9 (chain-of-custody)" they are pointing here — to the mechanism that makes the audit trail more than a timestamp database.
- The distinction matters in practice. A timestamp database says "this happened." A chain-of-custody record says "this party asserted this state, at this time, under this authority, and the signature is traceable to the key hierarchy." The second claim survives legal discovery, regulatory inspection, and adversarial challenge. The first does not.
- Three deployment scenarios make chain-of-custody load-bearing rather than decorative: (1) commercial-driver dashcam footage that must survive evidence handoff to insurer and court with an unbroken chain from in-vehicle capture through adjudication; (2) regulated-industry data transfers where the recipient's receipt and the transferor's dispatch must both appear in the compliance record; (3) LADOT-MDS-style mandated real-time signed exports to regulators where verifiable-completeness of the stream is itself a statutory requirement. The architecture does not address these scenarios differently — the same signed-transfer-receipt primitive covers all three — but naming them sets the scope.
- Cross-reference to Ch15 §Key-Loss Recovery sub-pattern 48f and §Collaborator Revocation sub-pattern 45f — those two sections share this substrate. The present section is the substrate specification.

### A.2 What chain-of-custody is not (≈150 words)

- Chain-of-custody is not the same as key-loss recovery. Recovery handles the case where the legitimate user loses custody of their own key; chain-of-custody handles the case where data moves from one authoritative party to another, with each transition attested. The two primitives share `Sunfish.Kernel.Audit` as substrate — both emit signed events into the same encrypted log — but their event schemas, their authorization parties, and their legal uses are distinct.
- Chain-of-custody is not the same as collaborator revocation. Revocation terminates a party's access authority; chain-of-custody attests to the transfer of data to a new custodian. A handoff followed by a revocation produces both a chain-of-custody transfer receipt and a revocation event — two distinct records in the same audit log.
- Chain-of-custody is not supply-chain security. Supply-chain security addresses the integrity of the software distribution pipeline. Chain-of-custody addresses the integrity of the data-custody sequence at runtime.
- These distinctions matter for the reader who arrives at this section having just read those three adjacent sections. State them once; do not repeat them in every sub-pattern.

### A.3 Sub-pattern 9a — Multi-party signed transfer receipt (≈450 words)

The transfer receipt is the fundamental unit of a chain-of-custody record. It attests to a single custody handoff: a transferor asserts that a specific data object, at a specific version, left their custody at a specific moment; the recipient asserts that the same data object arrived at their node at a specific moment, matches the transferor's assertion, and is now under their custody.

- **Structure of a transfer receipt.** A receipt carries: the data-object identifier (the CRDT document's stable ID, not a mutable name); the operation-vector that identifies the specific version being transferred (CRDT vector clock or equivalent); the transferor's node identifier and signature; the recipient's node identifier; a UTC transfer-initiation timestamp from the transferor; a UTC receipt-confirmation timestamp from the recipient; the transfer channel (relay, peer-to-peer, out-of-band import); and a custody scope (what authority the recipient is being granted — read, write, re-transfer). The receipt is not complete until both the transferor's signature and the recipient's acknowledgment are present. A one-sided receipt — transferor signs, recipient does not acknowledge — is a transfer-initiated record, not a transfer-completed record. The distinction matters when establishing exactly when custody passed.
- **Why both signatures are required.** A transfer that the recipient did not acknowledge is a transfer that failed. Evidence-class custody records cannot admit ambiguity about whether the receiving party accepted the object in the state the transferor claims. Both signatures close the loop: the transferor cannot later claim the recipient never received the data, and the recipient cannot later claim the data arrived in a state other than what the transferor asserts. The two-signature construction is the same principle that governs certified-mail receipts and bill-of-lading double-endorsement in physical logistics — the architecture translates it into a cryptographic primitive.
- **Versioning the transfer object.** The receipt identifies the transferred object at a specific version because CRDT documents evolve. A dashcam video frame captured at 14:07:31 and exported to a custody record at 14:07:35 must be identifiable as the specific state at those timestamps, not "the dashcam video in general." The CRDT vector clock satisfies this: it specifies the exact set of applied operations that define the transferred version, independent of any application-layer naming convention.
- `Sunfish.Kernel.Audit` manages transfer-receipt records. The receipt event is emitted by the transferor's node on dispatch and confirmed by the recipient's node on delivery. Until the recipient's acknowledgment event arrives and is validated against the transferor's original event, the receipt is in `transfer-initiated` state. After confirmation, it moves to `transfer-completed`. Any mismatch between the transferor's asserted version and the recipient's confirmed version triggers a `transfer-disputed` event and halts the custody chain pending resolution.
- Cross-reference to Ch15 §Key-Loss Recovery sub-pattern 48f and §Collaborator Revocation sub-pattern 45f — those sections reference the "multi-party signed-event substrate" that this sub-pattern specifies. The `Sunfish.Kernel.Audit` events emitted by the recovery and revocation primitives follow the same two-party signature construction as the transfer receipt.

### A.4 Sub-pattern 9b — Evidence-class temporal attestation (≈450 words)

A transfer receipt establishes who handled what and when. Evidence-class temporal attestation strengthens that record so the "when" survives adversarial challenge — the claim is not merely that the local node recorded a timestamp, but that the timestamp is anchored to an external, independently verifiable time source in a way that the architecture itself cannot retroactively alter.

- **Why local timestamps are insufficient for evidence class.** A timestamp recorded by the originating node is only as trustworthy as the node's clock and the node's software stack. An attacker with root access to the node can backdate a timestamp by modifying the system clock before the event is recorded. Against a well-resourced adversary — a defendant in litigation, a counterparty in a regulatory proceeding — a timestamp that is self-attested is a timestamp that an opposing party can challenge. The architecture's append-only log already prevents retroactive modification (DAG continuity — any tamper breaks the chain). The remaining gap is anchor-to-external-time, which the log structure alone does not close.
- **Trusted timestamping via RFC 3161.** The architecture integrates RFC 3161 trusted timestamping [cite] for evidence-class transfers. The timestamp authority (TSA) is an external service — a qualified trust service provider under eIDAS (EU) [cite] for EU deployments, or an equivalent authorized by the applicable jurisdiction. On transfer-receipt creation, the transferor's node submits a TimeStampRequest containing a hash of the receipt event to the TSA. The TSA returns a TimeStampResponse: a signed token containing the hash, the TSA identity, and the authority's certified time. The token is stored alongside the receipt event. Any node can verify the token's signature against the TSA's published certificate, and the hash against the receipt event. Backdating requires compromising both the local log (blocked by DAG continuity) and the TSA (not in scope for a node-level attacker).
- **Deployment-class selection of TSA.** Not all deployments require external TSA anchoring. Consumer deployments can rely on the log's internal append-only semantics. Regulated-industry deployments — those that need to produce evidence in legal proceedings, satisfy eIDAS AdES (Advanced Electronic Signature) requirements for evidence preservation, or comply with sector-specific record-keeping standards — specify a qualified TSA in their compliance posture. The deployment manifest records the TSA endpoint; `Sunfish.Kernel.Audit` calls it on every evidence-class transfer event.
- **Offline operation.** The architecture is local-first; a transfer that occurs while the node is offline cannot reach a TSA. The protocol queues the TimeStampRequest and submits it at the next available relay-connected window. The receipt event records the `tsa-pending` state until the token arrives; nodes verifying the chain observe the pending flag and defer final evidence-class validation until the token is attached. This is honest: an offline evidence-class transfer is not denied; its external timestamp anchor is deferred.
- Cross-reference to App B §Chain-of-Custody Worksheet for the deployment checklist that documents TSA selection and evidence-class designation.

### A.5 Sub-pattern 9c — Regulatory-export streaming with verifiable completeness (≈350 words)

The LADOT-MDS pattern named in the design-decisions note on chain-of-custody represents a third variant: not a point-in-time transfer receipt but a continuous signed stream exported to a regulator with cryptographic proof that the stream is complete (no events were omitted, reordered, or modified).

- **The streaming custody problem.** A regulator who receives a data stream from a fleet operator needs to verify not only that the individual events in the stream are authentic but that the stream as a whole is complete. A tampered stream that omits unfavorable events but preserves the remainder is not detectable by verifying individual events in isolation. The stream must carry a running proof of completeness.
- **Append-only Merkle construction.** The architecture addresses this with a Merkle-tree commitment over the event stream. As each event is appended to the log, its hash is incorporated into a running Merkle root. The root is signed and exported alongside each event batch; the regulator can verify that the received stream matches the committed root, and that the root chain is internally consistent (each root extends the prior one by exactly the new events, with no gaps). Any omission or reordering breaks the Merkle chain and is detectable [cite — transparency-log prior art: Crosby and Wallach, 2009].
- **Real-time vs. batch.** The streaming export can operate in two modes: real-time, in which the node emits events and their Merkle proof to the regulatory endpoint at the cadence the regulator specifies; and batch, in which the node exports a complete signed package at a scheduled interval. Both modes produce the same verifiable-completeness artifact; the difference is delivery cadence, not cryptographic content. Regulated deployments declare the mode in their compliance posture.
- **Distinction from chain-of-custody transfer receipt.** Sub-patterns 9a and 9b cover bilateral custody handoffs — one party transferring to another. Sub-pattern 9c covers unilateral continuous reporting — one party continuously attesting to an external authority. The distinction is authority: in 9a/9b, the recipient acknowledges receipt; in 9c, the regulator is a passive verifier who does not acknowledge individual events, only validates the completeness proof.
- Cross-reference to §GDPR Article 17 and Crypto-Shredding for the tension between an append-only regulatory-export stream and an erasure request that would require modifying or removing an event from that stream. The architecture's answer is the same as for the compliance-tier CRDT log: crypto-shredding the content (destroying the DEK) while preserving the structural entry satisfies the content-erasure obligation without breaking the Merkle chain.

### A.6 Threat model for chain-of-custody (≈200 words)

Chain-of-custody is itself an attack surface. Three specific failure modes define the threat model.

**Receipt forgery.** An attacker forges a transfer receipt to claim that a data object was transferred — or not transferred — at a time that serves their interest. The two-signature construction (sub-pattern 9a) prevents this: a receipt requires both the transferor's and recipient's valid signatures under their device keypairs. Forging the receipt requires compromising both device keypairs simultaneously. A single compromised endpoint can fabricate a one-sided `transfer-initiated` record but cannot complete the receipt without the other party's signature.

**Timestamp manipulation.** An attacker with control of the local node modifies the system clock before recording a transfer event, backdating it. Sub-pattern 9b's external TSA anchor detects this: the TSA token carries the TSA's certified time, which is independent of the node's clock. A backdated receipt has a TSA token with a later timestamp than the receipt claims — the mismatch is detectable by any verifier. Evidence-class deployments must use the external TSA; deployments without a TSA anchor have no defense against local-clock manipulation.

**Stream omission.** An attacker omits events from a regulatory-export stream to conceal unfavorable activity. Sub-pattern 9c's Merkle-chain commitment prevents this: any omission breaks the chain. The regulator detects the gap.

**FAILED conditions:** A transfer receipt that is accepted as complete with only one signature; a chain-of-custody event that does not appear in the encrypted audit log; a regulatory-export stream that is accepted as complete without a Merkle-chain verification step. Any one of these conditions voids the primitive's guarantees.

### A.7 Implementation surfaces (≈150 words)

Chain-of-custody is observable through four named event contracts. The list is illustrative — the concrete schema lands when `Sunfish.Kernel.Custody` reaches its first milestone (see §C for the namespace decision).

- `CustodyTransferInitiated` — the transferor's node has signed and dispatched a transfer receipt; carries the data-object identifier, the version vector, the transferor signature, and the UTC dispatch timestamp.
- `CustodyTransferConfirmed` — the recipient's node has signed the acknowledgment; receipt moves to `transfer-completed`; carries the recipient signature and the UTC confirmation timestamp.
- `CustodyTransferDisputed` — a mismatch between the transferor's asserted version and the recipient's confirmed version; custody chain halts pending resolution; carries both signatures and the divergence description.
- `RegulatoryExportBatch` — a signed event-batch and Merkle-proof emitted in streaming-export mode; carries the batch range (first and last event sequence numbers), the Merkle root, and the TSA token (if evidence-class mode is active).

Nodes wishing to integrate custody-verification flows subscribe to the relevant contracts through `Sunfish.Kernel.Custody` (or `Sunfish.Kernel.Audit` — see §C). The audit-log validation layer enforces the two-signature requirement before the `CustodyTransferConfirmed` contract is emitted.

---

## §B. New template in Appendix B — "Chain-of-Custody Worksheet"

**Insertion point:** as a new `## Section 5` appended after the existing `## Section 4 — Key Compromise Incident Response Template`. The existing appendix has four sections: asset inventory, actor taxonomy, worked example, and key compromise template. Extension #47 adds THREAT-10 to Section 2 (actor taxonomy). Extension #9 adds a new Section 5 — a standalone worksheet rather than a second actor-taxonomy entry — because chain-of-custody is not primarily an adversarial-actor concern. It is a process-and-compliance concern: which transfers require receipts, which require evidence-class timestamps, which require regulatory-export streaming.

**Decision on THREAT-11 vs. worksheet:** chain-of-custody does not introduce a new adversarial actor in the way that endpoint compromise does. The threat model for chain-of-custody (receipt forgery, timestamp manipulation, stream omission) is already covered in Ch15 §Chain-of-Custody for Multi-Party Transfers §Threat model section. Adding a THREAT-11 actor entry would duplicate that material. A worksheet template is the correct Appendix B artifact — it gives the practitioner a deployment-time checklist rather than another actor entry. The THREAT-NN series continues with the next extension that introduces a genuinely new adversarial actor.

**Word target:** 500 words.

**H2:** `## Section 5 — Chain-of-Custody Worksheet`

### B.1 Purpose and when to use this worksheet (≈100 words)

- Use this worksheet when any of the following applies to the deployment: the team transfers sensitive data to a third party (insurer, regulator, auditor, legal counsel, successor-entity); the deployment involves evidence-class data (dashcam footage, healthcare records, financial audit logs, compliance-tier CRDT logs); the deployment is subject to a mandated real-time regulatory-export requirement (MDS-style, financial transaction reporting, healthcare event reporting).
- This worksheet is a deployment-time checklist, not a per-transfer checklist. Fill it in before the first evidence-class transfer. Revisit whenever the deployment's regulatory scope changes.
- Cross-reference to Ch15 §Chain-of-Custody for Multi-Party Transfers for the architecture specification this worksheet applies.

### B.2 Transfer-class inventory (≈150 words)

Fill this table before any evidence-class data transfer.

| Transfer type | Data classes involved | Evidence class required? | External TSA required? | Regulatory-export mode | Receipt retention period |
|---|---|---|---|---|---|
| Internal role handoff (within org) | Varies by role | No (internal) | No | Not applicable | Per org policy |
| Departure partition (45e) | All roles under partition | Recommended | Recommended | Not applicable | Per statutory minimum |
| Third-party disclosure (insurer, auditor) | As specified in disclosure scope | Yes | Yes (regulated deployment) | Batch or real-time per agreement | Per disclosure contract + statutory |
| Regulatory streaming export | All events in scope | Yes | Yes (qualified TSA per jurisdiction) | Real-time or batch per regulator | Per regulatory requirement |

**Customization guidance:** add rows for every transfer class the deployment will perform. Mark the evidence-class column honestly — under-designating transfers as non-evidence-class saves setup cost until the first legal dispute reveals the gap. Identify the TSA vendor and the qualified trust service provider basis (eIDAS QSeal for EU, equivalent for other jurisdictions) in the deployment's compliance posture before any evidence-class transfer.

### B.3 Deployment checklist (≈150 words)

Run through this checklist before the first evidence-class transfer. All items must be confirmed.

- [ ] `Sunfish.Kernel.Custody` (or `Sunfish.Kernel.Audit`) namespace is configured with a valid TSA endpoint for evidence-class deployments.
- [ ] Deployment manifest declares the TSA provider and the jurisdiction basis for its qualification.
- [ ] Transfer-receipt retention policy is documented: which receipts are retained, for how long, under which regulatory retention floor.
- [ ] Regulatory-export mode (real-time or batch) is declared in the compliance posture and communicated to the receiving regulator.
- [ ] Evidence-class data classes are identified in the asset inventory (Appendix B §Section 1) and tagged in the deployment's data classification.
- [ ] Merkle-chain verification procedure is documented for the regulator or auditor who will validate the export stream.
- [ ] Offline-operation policy is documented: how long may a TSA-pending receipt remain unanchored before the deployment flags the gap as a compliance event?

### B.4 Incident response for custody-chain disputes (≈100 words)

When a `CustodyTransferDisputed` event fires — the recipient's confirmed version does not match the transferor's asserted version — execute this response:

1. Halt further transfers of the affected data object pending resolution.
2. Log the dispute event with both the transferor's and recipient's signed events for the audit record.
3. Engage legal counsel before responding to any external party (regulator, opposing party in litigation) about the disputed transfer.
4. Determine the source of divergence: transferor error, recipient error, network corruption, or adversarial tampering. Each requires a different resolution path.
5. Do not attempt to reconcile the version mismatch by modifying either party's local log. The disputed state is the legally relevant state.

---

## §C. Namespace Decision — `Sunfish.Kernel.Custody` vs. extends `Sunfish.Kernel.Audit`

The sunfish-package-roadmap.md anticipatory entry for #9 records the open question as: "NEW `Sunfish.Kernel.Custody` (or extends `Sunfish.Kernel.Audit`)." This outline decides.

**Decision: NEW `Sunfish.Kernel.Custody`.**

**Reasoning:**

1. **Distinct retention and legal semantics.** `Sunfish.Kernel.Audit` already carries a deferred decision about whether to remain a distinct package or become a subsystem of `Sunfish.Kernel.Ledger` (per the roadmap's open question for #48). Adding chain-of-custody events to `Sunfish.Kernel.Audit` before that decision is resolved compounds the architectural ambiguity. A separate `Sunfish.Kernel.Custody` namespace forces the decision on each mechanism's retention semantics independently.

2. **External-party participation.** Chain-of-custody transfer receipts require both the transferor's and recipient's signatures — making an external party (the recipient) a co-author of the audit record. Recovery-event and revocation-event records in `Sunfish.Kernel.Audit` are single-node-signed with multi-party acknowledgment layered on top; transfer receipts are inherently bilateral from the first write. The substrate's trust model differs enough to warrant a distinct namespace.

3. **TSA integration.** Sub-pattern 9b's RFC 3161 integration is specific to chain-of-custody events. Folding TSA-anchored events into a general-purpose audit log creates a hybrid log with two distinct external dependencies (the audit substrate and the TSA endpoint). A dedicated `Sunfish.Kernel.Custody` package owns the TSA integration cleanly.

4. **Composability with `Sunfish.Kernel.Audit`.** The two packages compose without merging: `Sunfish.Kernel.Audit` continues to own recovery-event and revocation-event records; `Sunfish.Kernel.Custody` owns transfer-receipt and regulatory-export records. Both emit into the same encrypted log substrate; their record schemas and retention policies remain distinct. Extensions #48 and #45 retain their `Sunfish.Kernel.Audit` references unchanged.

**Consequence for references in prior extensions:** the cross-reference in Ch15 §Key-Loss Recovery sub-pattern 48f reads "the chain-of-custody mechanism (#9)" without naming a namespace. That reference is accurate regardless of whether #9's namespace is `Sunfish.Kernel.Audit` or `Sunfish.Kernel.Custody` — the cross-reference is to the mechanism, not the package. No retroactive edits to #48 or #45 are required.

**Sunfish-package-roadmap update required at code-check stage:** the anticipatory entry for #9 advances from `Future forward-looking namespaces` to a first-class roadmap entry with status `book-committed`, namespace `Sunfish.Kernel.Custody`, source extension #9, and the architectural commitment described in §A.7 above.

---

## §D. Technical-Review Focus

For the `@technical-reviewer` pass:

- **RFC 3161 trusted timestamping.** Verify the TimeStampRequest/TimeStampResponse construction is accurate. The book should cite RFC 3161 directly [cite: IETF RFC 3161, Aug. 2001] and note that eIDAS Article 41 gives qualified electronic time stamps evidential value under EU law.
- **Merkle-tree streaming completeness.** Verify the Crosby and Wallach (2009) cite is accurate for append-only Merkle-log completeness proofs. The Certificate Transparency (RFC 9162) prior art is equally relevant for readers who know the web PKI context; both should be cited.
- **Two-signature receipt construction.** Verify no existing source paper (v13, v5) addresses this explicitly — if the two-signature construction is a new architectural commitment (surfaced through the chain-of-custody gap, not derived from v13/v5), mark it `<!-- CLAIM: new architectural commitment per design-decisions §5 #9 — not in v13/v5 source papers -->` for the technical-review pass to confirm.
- **LADOT-MDS note.** The design-decisions §5 note explicitly treats LADOT-MDS-style regulatory streaming as a variant of chain-of-custody. Verify the architectural fit: MDS uses a GBFS/GTFS-RT-compatible feed format with signed payloads. The Merkle-chain sub-pattern 9c is consistent with this but the book should not claim MDS-specific compliance without verifying the feed format's actual signing requirements.
- **Cross-references to #48 and #45.** Verify the phrase "multi-party signed-event substrate" in #45 draft §A.7 and #48 outline §H accurately describes what sub-pattern 9a specifies. If the existing prose in those delivered sections over-specifies the substrate in a way inconsistent with 9a's construction, flag for minor reconciliation in those sections.

---

## §E. Prose-Review Focus

For the `@prose-reviewer` + `@style-enforcer` pass:

- Active voice throughout. "The transferor signs the receipt" — not "the receipt is signed by the transferor."
- No hedging on the two-signature requirement. Replace "both signatures should ideally be present" with the specific claim: "a receipt without both signatures is a transfer-initiated record, not a transfer-completed record."
- Paragraph length cap: 6 sentences. Sub-patterns 9a and 9b are dense; they will require aggressive trimming to meet this constraint.
- No academic scaffolding. No "this section presents" or "as described above."
- No re-introducing the architecture. Ch15 already established the key hierarchy, the admin event channel, the CRDT log structure, and `Sunfish.Kernel.Audit`. This section may reference those without re-describing them.
- The §A.2 "what chain-of-custody is not" block distinguishes the three adjacent sections (key-loss recovery, collaborator revocation, supply-chain security). Write it directly — a reader who has read those three sections should need only one sentence per distinction, not a paragraph.

---

## §F. Voice-Check Focus (HUMAN STAGE — not autonomous)

For the human voice-pass:

- **Anecdote candidate — evidence handoff.** The dashcam footage scenario has a human core: a commercial driver whose vehicle is involved in an incident, and whose ability to prove what happened depends entirely on whether the footage that left their dash-mounted recorder arrived at the insurer with an unbroken chain of custody. This is a relatable professional reality for anyone who has dealt with insurance claims on video evidence. A two-sentence grounding of this scenario before the technical construction lands would give the section a human entry point.
- **Anecdote candidate — regulatory export failure.** The inverse of the dashcam scenario: a fleet operator who receives a regulatory inquiry and cannot prove their data stream was complete. The gap is not that the data was modified — it is that there is no proof it was not modified. That distinction (absence of proof vs. proof of absence) is the practical difference sub-pattern 9c closes.
- Do not add the anecdote in the draft stage. Mark with `<!-- voice-check: add custody handoff anecdote here -->`.
- Calibrate Sinek register lightly per `feedback_voice_sinek_calibration.md` memory — narrative scenes should earn their place, not perform purpose-before-process mechanically.

---

## §G. Citations

The draft adds these to Ch15's reference list (IEEE numeric, continuing from existing [13]):

- [14] Internet Engineering Task Force (IETF), "Internet X.509 Public Key Infrastructure Time-Stamp Protocol (TSP)," RFC 3161, Aug. 2001. [Online]. Available: https://www.rfc-editor.org/rfc/rfc3161 — for sub-pattern 9b (trusted timestamping).
- [15] European Parliament and Council, "Regulation (EU) No 910/2014 on electronic identification and trust services (eIDAS)," Official Journal of the European Union, Jul. 2014, Art. 41. [Online]. Available: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32014R0910 — for eIDAS qualified time-stamp evidential value.
- [16] S. Crosby and D. Wallach, "Efficient Data Structures for Tamper-Evident Logging," in *Proc. 18th USENIX Security Symposium*, Montreal, 2009. [Online]. Available: https://www.usenix.org/legacy/event/sec09/tech/full_papers/crosby.pdf — for Merkle-log completeness prior art.
- [17] Internet Engineering Task Force (IETF), "Certificate Transparency Version 2.0," RFC 9162, Dec. 2021. [Online]. Available: https://www.rfc-editor.org/rfc/rfc9162 — for Certificate Transparency as Merkle-log prior art (web PKI context readers may prefer this reference to Crosby/Wallach).

Appendix B cross-references Ch15's source list — no new citations needed in App B.

---

## §H. Cross-References to Add

Inside the new Ch15 section:

- Ch15 §Chain-of-Custody → Ch15 §Key-Loss Recovery sub-pattern 48f (shares `Sunfish.Kernel.Audit` substrate; #9 is the substrate specification for #48's cross-reference)
- Ch15 §Chain-of-Custody → Ch15 §Collaborator Revocation sub-pattern 45f (same substrate; #9 is the substrate specification for #45's cross-reference)
- Ch15 §Chain-of-Custody → Ch15 §Supply Chain Security (adjacent section; distinguish build-pipeline from runtime data-custody chain)
- Ch15 §Chain-of-Custody → Ch15 §GDPR Article 17 and Crypto-Shredding (downstream section; the streaming-export / erasure tension)
- Ch15 §Chain-of-Custody → App B §Section 5 (the worksheet that operationalizes this section)
- App B §Section 5 → Ch15 §Chain-of-Custody (the specification this worksheet applies)

**Retroactive note for #48 and #45 cross-references:** the phrase "cross-reference to #9 (chain-of-custody)" that appears in Ch15 §Key-Loss Recovery sub-pattern 48f and in Ch15 §Collaborator Revocation sub-pattern 45f should be updated at the draft stage of #9 to read "cross-reference to §Chain-of-Custody for Multi-Party Transfers" (using the section anchor rather than the extension number). This converts a forward-reference-to-a-gap into a live cross-reference to a delivered section. The draft-stage commit should perform this update in the same file edit that inserts the new section.

---

## §I. Subagent Prompt for the Draft Stage

The next iteration (`outline → draft`) will invoke `@chapter-drafter` with this prompt:

> Draft two additions to *The Inverted Stack*: (1) a new section `## Chain-of-Custody for Multi-Party Transfers` for Ch15 (~2,000 words, inserted between the existing `## Supply Chain Security` section and the existing `## GDPR Article 17 and Crypto-Shredding` section); and (2) a new `## Section 5 — Chain-of-Custody Worksheet` for Appendix B (~500 words, appended after the existing `## Section 4 — Key Compromise Incident Response Template`).
>
> Source: outline at `docs/book-update-plan/working/9-chain-of-custody/outline.md`. Follow the section structure and word targets exactly. Voice: Part III specification register for Ch15; practical deployment-tool register for App B (match the register of existing App B sections, not the specification register). Active voice throughout. No hedging. No academic scaffolding. No re-introducing the architecture.
>
> Sunfish references: package names only — `Sunfish.Kernel.Custody` is the new forward-looking namespace for this extension (see outline §C for the namespace decision and reasoning); `Sunfish.Kernel.Audit` is referenced for substrate sharing with #48 and #45 only. No class APIs, no method signatures. Mark all `Sunfish.Kernel.Custody` references `// illustrative — not runnable`.
>
> Citations: IEEE numeric. Add the four sources listed in outline §G as [14]–[17] to Ch15's reference list. App B cross-references Ch15 — no new citations needed in App B.
>
> Cross-references: per outline §H — wire all of them. Additionally, in the same edit, update the two existing cross-reference phrases "cross-reference to #9 (chain-of-custody)" in Ch15 §Key-Loss Recovery sub-pattern 48f and in Ch15 §Collaborator Revocation sub-pattern 45f to read "cross-reference to §Chain-of-Custody for Multi-Party Transfers".
>
> Insertion mechanics: write the new H2 section directly into `chapters/part-3-reference-architecture/ch15-security-architecture.md` at the specified insertion point; write the new H2 section directly into `chapters/appendices/appendix-b-threat-model-worksheets.md` at the specified insertion point. Preserve existing H2 anchor structure and H1 frontmatter. Update Ch15's reference list with [14]–[17].

---

## §J. Quality Gate for `outline → draft`

Per loop-plan §5: outline has all section headers + bullet points (✓ §A and §B above); word count target estimated (✓ 2,000 + 500 = 2,500); subagent prompt prepared (✓ §I above). Gate passes.

The following additional quality-gate item is specific to #9: the namespace decision in §C is documented with reasoning, not deferred to the draft stage. The code-check stage will confirm that `Sunfish.Kernel.Custody` appears in the chapter file's namespace inventory and that the sunfish-package-roadmap.md anticipatory entry has been promoted to a first-class entry. The code-check report must note this update as a required action.

---

**Estimated next-iteration duration (draft stage):** 60–90 minutes. Two files receive edits (Ch15 + App B) and two existing cross-references require retroactive update. Schedule next fire 1–2 hours after this one to allow context-cache cooldown and human-review window.
