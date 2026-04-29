# Draft — #9 Chain-of-Custody for Multi-Party Transfers

This file is the standalone draft for the code-checker. It contains the new Ch15 section and the new App B Section 5, in the form they appear in the chapter files.

---

## Ch15 insertion — between §Supply Chain Security and §GDPR Article 17 and Crypto-Shredding

```markdown
## Chain-of-Custody for Multi-Party Transfers

<!-- code-check annotations: Sunfish.Kernel.Custody (NEW namespace, not in canon — forward-looking); Sunfish.Kernel.Audit (forward-looking from #48). 0 class APIs / method signatures introduced. -->

A commercial driver finishes a shift, parks the rig, and uploads the day's dashcam footage. The next morning, an incident from that route arrives on the company's risk desk. The footage now has to travel: to the insurer, to opposing counsel, to a regulator, possibly to a court. At every handoff, a different party must be able to assert two facts — the file is the file the camera produced, and custody passed on a date no one can credibly dispute. A timestamp database can record both facts. It cannot defend them.

The audit trails specified in §Key-Loss Recovery sub-pattern 48f and §Collaborator Revocation sub-pattern 45f rest on the same substrate this section specifies. Both reference the multi-party signed-event mechanism without naming it. This section names it: chain-of-custody is a signed, append-only sequence in which each entry attests to a specific act by a specific party at a specific moment, with the signatures traceable to the deployment's key hierarchy. The distinction matters in court. A timestamp database says "this happened." A chain-of-custody record says "this party asserted this state, at this time, under this authority, and the signature resolves through the published key hierarchy." Only the second claim survives discovery, regulatory inspection, and adversarial challenge.

Three deployment scenarios make the mechanism load-bearing rather than decorative. Commercial-vehicle dashcam footage must survive the handoff chain from in-vehicle capture through insurer adjudication and possible litigation, with no gap a defense expert can exploit. Regulated-industry data transfers — clinical handoffs, audited financial exports, deposition-bound legal records — require both the dispatcher's and the recipient's signed attestation in the same record. LADOT-MDS-style mandated regulatory streams require continuous proof that the operator's exported telemetry is complete, not merely that each individual event is authentic. The architecture treats all three under one signed-receipt primitive; naming the scenarios sets the scope.

### What chain-of-custody is not

Chain-of-custody is not key-loss recovery. Recovery handles the case where a legitimate user loses custody of their own key; chain-of-custody handles the case where data moves from one authoritative party to another with each transition attested. The two share `Sunfish.Kernel.Audit` as substrate but their event schemas, authorization parties, and legal uses are distinct.

Chain-of-custody is not collaborator revocation. Revocation terminates a party's access authority; chain-of-custody attests to the transfer of data to a new custodian. A handoff followed by a revocation produces two distinct records in the same audit log.

Chain-of-custody is not supply-chain security. Supply-chain security addresses the integrity of the software distribution pipeline. Chain-of-custody addresses the integrity of the data-custody sequence at runtime.

State the distinctions once. The sub-patterns below assume them.

### Sub-pattern 9a — Multi-party signed transfer receipt

The transfer receipt is the unit of custody handoff. It binds a single transition: the transferor asserts that a specific data object, at a specific version, left their custody at a specific moment; the recipient asserts that the same data object arrived at their node at a specific moment, matches the transferor's assertion, and is now under their custody.

A receipt carries the data-object identifier (the CRDT document's stable ID, not a mutable name); the operation-vector identifying the specific version transferred (CRDT vector clock or equivalent); the transferor's node identifier and signature; the recipient's node identifier; a UTC transfer-initiation timestamp from the transferor; a UTC receipt-confirmation timestamp from the recipient; the transfer channel (relay, peer-to-peer, out-of-band import); and a custody scope declaring what authority the recipient now holds — read, write, re-transfer. The receipt is incomplete until both signatures land. A one-sided receipt is a `transfer-initiated` record, not a `transfer-completed` record.

The two-signature construction is not stylistic. Evidence-class custody records cannot admit ambiguity about whether the receiving party accepted the object in the state the transferor claims. The transferor cannot later assert the recipient never received the data; the recipient cannot later assert the data arrived in a state other than what the transferor recorded. Certified-mail receipts and bill-of-lading double-endorsement encode the same principle in physical logistics. The architecture renders it as a cryptographic primitive — two device-key signatures over the same content hash, separated in time, both required for the receipt to close.

The version vector matters because CRDT documents evolve. A dashcam frame captured at 14:07:31 and exported to a custody record at 14:07:35 must be identifiable as the specific state at those moments — not "the dashcam recording in general." The CRDT vector clock specifies the exact set of applied operations defining the transferred version, independent of any application-layer name [12][13].

`Sunfish.Kernel.Custody` manages transfer-receipt records. The transferor's node emits the receipt event on dispatch; the recipient's node confirms on delivery. Until the recipient's acknowledgment event arrives and validates against the transferor's original event, the receipt sits in `transfer-initiated` state. After confirmation, it advances to `transfer-completed`. Any mismatch between the transferor's asserted version and the recipient's confirmed version triggers a `transfer-disputed` event and halts the custody chain pending resolution. The receipt verifiability does not depend on either custodian's endpoint integrity — see §Endpoint Compromise: What Stays Protected. A compromised endpoint can refuse to sign or sign falsely, but it cannot forge the counterparty's signature.

### Sub-pattern 9b — Evidence-class temporal attestation

A transfer receipt establishes who handled what and when. Evidence-class temporal attestation strengthens the "when" so it survives adversarial challenge — the timestamp is anchored to an external, independently verifiable time source the architecture itself cannot retroactively alter.

A timestamp recorded by the originating node is only as trustworthy as the node's clock and software stack. An attacker with root access can backdate a timestamp by modifying the system clock before the event is recorded. Against a well-resourced adversary — a defendant in litigation, a counterparty in a regulatory proceeding — a self-attested timestamp is a timestamp the opposing party will challenge. The append-only log already prevents retroactive modification; DAG continuity breaks if the chain is tampered with. The remaining gap is anchor-to-external-time, which the log structure alone does not close.

The architecture integrates RFC 3161 trusted timestamping [28] for evidence-class transfers. The timestamp authority (TSA) is an external service — under EU deployments, a qualified trust service provider as defined in eIDAS Article 41 [29]; in other jurisdictions, an authority certified under the equivalent regulation. On transfer-receipt creation, the transferor's node submits a TimeStampRequest containing the SHA-256 hash of the receipt event to the TSA. The TSA returns a TimeStampResponse: a signed token containing the hash, the TSA identity, and the authority's certified time. The token persists alongside the receipt event in the audit log. Any node verifies the token's signature against the TSA's published certificate (per X.509 chain-of-trust [10]) and the hash against the receipt event. Backdating now requires compromising both the local log (blocked by DAG continuity) and the TSA (out of scope for a node-level attacker). <!-- CLAIM: source? — the two-signature receipt construction with TSA anchoring at this granularity is a new architectural commitment from design-decisions §5 #9; v13/v5 reference chain-of-custody only as a forward gap. -->

Not all deployments need external TSA anchoring. Consumer-tier deployments rely on the log's internal append-only semantics. Regulated deployments — those that produce evidence in legal proceedings, satisfy eIDAS AdES (Advanced Electronic Signature) requirements for evidence preservation, or comply with sector-specific record-keeping standards — declare a qualified TSA in their compliance posture. The deployment manifest records the TSA endpoint; `Sunfish.Kernel.Custody` invokes it on every evidence-class transfer event.

The architecture is local-first; a transfer that occurs while the node is offline cannot reach a TSA. The protocol queues the TimeStampRequest and submits it at the next relay-connected window. The receipt event records `tsa-pending` state until the token arrives. Nodes verifying the chain observe the pending flag and defer final evidence-class validation until the token is attached. An offline evidence-class transfer is not denied — its external timestamp anchor is deferred. The deployment's compliance posture documents the maximum acceptable pending duration before the gap escalates as a compliance event (see App B §Section 5).

### Sub-pattern 9c — Regulatory-export streaming with verifiable completeness

LADOT-MDS-style regulatory exports introduce a third variant. The mechanism is not a point-in-time bilateral receipt but a continuous signed stream emitted to a regulator with cryptographic proof that the stream is complete — no events were omitted, reordered, or modified between source and recipient.

A regulator receiving a data feed from a fleet operator must verify two things: that each individual event in the stream is authentic, and that the stream as a whole is complete. A tampered stream that omits unfavorable events while preserving the remainder is not detectable by verifying individual events in isolation. The stream must carry a running proof of completeness alongside its content.

The architecture addresses this with an append-only Merkle-tree commitment over the event stream, following the construction Crosby and Wallach formalized for tamper-evident logging [30] and standardized for the web PKI in Certificate Transparency [31]. As each event is appended to the export log, its hash incorporates into a running Merkle root. The root signs and exports alongside each event batch. The regulator verifies that the received stream matches the committed root and that the root chain is internally consistent — each new root extends the prior one by exactly the new events, with no gaps. Any omission or reordering breaks the Merkle chain and is detectable on the regulator's side without requiring any cooperation from the operator.

The stream operates in two modes. Real-time mode emits events and their Merkle proof to the regulatory endpoint at the cadence the regulator specifies. Batch mode exports a complete signed package at a scheduled interval. Both modes produce the same verifiable-completeness artifact; the difference is delivery cadence, not cryptographic content. Regulated deployments declare the mode in their compliance posture and communicate the choice to the receiving regulator.

Sub-patterns 9a and 9b cover bilateral handoffs — one party transferring to another, with both parties signing. Sub-pattern 9c covers unilateral continuous reporting — one party continuously attesting to a passive verifier. The distinction is authority. In 9a and 9b, the recipient acknowledges receipt and the receipt is a two-signature primitive. In 9c, the regulator validates the completeness proof but does not acknowledge individual events — the stream is unilateral by design, because regulatory recipients cannot be made co-authors of every record they ingest.

### Threat model for chain-of-custody

Chain-of-custody is itself an attack surface. Three failure modes define the threat model.

**Receipt forgery.** An attacker forges a transfer receipt to claim a data object was — or was not — transferred at a time that serves their interest. The two-signature construction in 9a prevents this. A receipt requires both the transferor's and recipient's valid signatures under their device keypairs. Forging the receipt requires compromising both device keypairs simultaneously. A single compromised endpoint can fabricate a one-sided `transfer-initiated` record but cannot complete the receipt without the other party's signature — see §Collaborator Revocation for the per-party key isolation that makes simultaneous compromise of two distinct parties a separate, much harder attack.

**Timestamp manipulation.** An attacker with control of the local node modifies the system clock before recording a transfer event, backdating it. Sub-pattern 9b's external TSA anchor detects this. The TSA token carries the TSA's certified time, independent of the node's clock. A backdated receipt produces a TSA token with a later certified time than the receipt's claimed dispatch time — the mismatch is detectable by any verifier. Evidence-class deployments must use the external TSA. Deployments without a TSA anchor have no defense against local-clock manipulation, and the compliance posture must declare this honestly.

**Stream omission.** An attacker omits events from a regulatory-export stream to conceal unfavorable activity. Sub-pattern 9c's Merkle-chain commitment prevents this. Any omission breaks the chain. The regulator detects the gap on receipt-side verification, without requiring cooperation from the operator who would be the party performing the omission.

### FAILED conditions

The chain-of-custody primitive fails when any of the conditions below holds. Any one of them voids the primitive's guarantees.

- **A transfer receipt is accepted as complete with only one signature.** Architecture failure. Sub-pattern 9a's two-signature requirement is the foundation of the bilateral attestation; a one-signature receipt cannot ground the legal claim of mutual acknowledgment.
- **A chain-of-custody event does not appear in the encrypted audit log.** Architecture failure. The audit substrate is the tamper-evident anchor; an event recorded outside the log is an event with no cryptographic continuity guarantee.
- **A regulatory-export stream is accepted as complete without a Merkle-chain verification step.** Compliance failure. Sub-pattern 9c's verifiable-completeness proof is the structural answer to stream omission; bypassing the verification step leaves the regulator with no defense against silent gaps.

The kill trigger for this primitive is a transfer receipt that closes as `transfer-completed` without a verifiable second signature traceable to the recipient's published key. A primitive that cannot guarantee the second signature has not been forged is not a chain-of-custody primitive — it is a logbook with extra ceremony.

### Implementation surfaces

Chain-of-custody is observable through four named event contracts. The list is illustrative; the concrete schema lands when `Sunfish.Kernel.Custody` reaches its first milestone.

- `CustodyTransferInitiated` — the transferor's node has signed and dispatched a transfer receipt; carries the data-object identifier, the version vector, the transferor signature, and the UTC dispatch timestamp.
- `CustodyTransferConfirmed` — the recipient's node has signed the acknowledgment; the receipt advances to `transfer-completed`; carries the recipient signature and the UTC confirmation timestamp.
- `CustodyTransferDisputed` — a mismatch between the transferor's asserted version and the recipient's confirmed version; the custody chain halts pending resolution; carries both signatures and the divergence description.
- `RegulatoryExportBatch` — a signed event-batch and Merkle proof emitted in streaming-export mode; carries the batch range (first and last event sequence numbers), the Merkle root, and the TSA token when evidence-class mode is active.

Nodes integrating custody-verification flows subscribe through `Sunfish.Kernel.Custody`. The audit-log validation layer enforces the two-signature requirement before the `CustodyTransferConfirmed` contract is emitted. Custody records compose with the recovery-event audit trail (§Key-Loss Recovery sub-pattern 48f) and the revocation-event audit trail (§Collaborator Revocation sub-pattern 45f) at the substrate layer; their record schemas remain distinct.

Article 17 erasure requests against an event in a `RegulatoryExportBatch` introduce a tension the streaming-export mode cannot resolve unilaterally — modifying the event would break the Merkle chain and invalidate every batch downstream of it. The architecture's answer is the same as for the compliance-tier CRDT log: crypto-shred the content (destroy the DEK) while preserving the structural entry, satisfying the content-erasure obligation without breaking the stream's completeness proof. See §GDPR Article 17 and Crypto-Shredding for the full mechanism. The deployment-time worksheet for custody operations sits at App B §Section 5.
```

---

## App B insertion — new §Section 5, before the closing italic appendix-wide footer

```markdown
## Section 5 — Chain-of-Custody Worksheet

Use this worksheet when the deployment transfers sensitive data to a third party (insurer, regulator, auditor, legal counsel, successor entity), handles evidence-class data (dashcam footage, healthcare records, financial audit logs), or operates a mandated regulatory-export stream (MDS-style telemetry, financial reporting, healthcare event reporting). Fill it in before the first evidence-class transfer; revisit when regulatory scope changes. Architectural specification: Ch15 §Chain-of-Custody for Multi-Party Transfers.

### Field 1 — Parties

| Role | Identity | Device key fingerprint | Jurisdiction |
|---|---|---|---|
| Transferor (originating custodian) | | | |
| Recipient (receiving custodian) | | | |
| External authority (regulator, TSA, court) — if applicable | | | |

Record fingerprints from the published key hierarchy, not informal channels.

### Field 2 — Data class

| Data class | Evidence-class? | Retention floor | Crypto-shred eligible? |
|---|---|---|---|
| | Yes / No | | Yes / No |

Under-designation saves setup cost until the first legal dispute exposes the gap.

### Field 3 — Transfer trigger

Name the event that initiates transfer (scheduled regulatory export, insurer claim request, auditor engagement, departure partition under §Collaborator Revocation 45e, subpoena, warrant) and the authorization gate — who signs off before a `CustodyTransferInitiated` event emits.

### Field 4 — Signing requirements

- [ ] Both transferor and recipient device keys are in the published key hierarchy with valid attestation at transfer time.
- [ ] Transferor signing role grants `re-transfer` scope (onward custody) or excludes it (custody terminal at recipient).
- [ ] One-sided `transfer-initiated` records are flagged incomplete and excluded from any artifact represented as completed.
- [ ] Audit-log validation rejects `CustodyTransferConfirmed` events lacking both signatures.

### Field 5 — Timestamping

| Item | Decision |
|---|---|
| External TSA required? | Yes (evidence-class) / No (consumer-tier) |
| TSA provider and qualification basis | e.g., eIDAS qualified TSP (EU); equivalent per jurisdiction |
| TSA endpoint and certificate fingerprint | |
| Max `tsa-pending` duration before compliance escalation | |
| Offline policy | Queue and submit on next relay window / Block transfer until TSA reachable |

Record the TSA certificate fingerprint locally so a substituted endpoint is detectable.

### Field 6 — Verification

- [ ] Merkle-chain verification documented for streaming exports — root cadence, hash function (SHA-256 default), proof format.
- [ ] Receipt-verification documented for bilateral transfers — signature check, version-vector match, TSA-token validation.
- [ ] Attestation artifacts (TSA tokens, Merkle proofs, signed receipts) retained alongside the data they attest. Lost artifacts reduce the transfer to `transfer-initiated` retroactively.

### Field 7 — Escalation paths

On `CustodyTransferDisputed` (recipient version mismatches transferor assertion):

1. Halt further transfers of the affected object pending resolution.
2. Log the dispute event with both signed events.
3. Engage legal counsel before responding to any external party.
4. Diagnose divergence: transferor error, recipient error, network corruption, adversarial tampering. Each path differs.
5. Do not reconcile by modifying either local log. The disputed state is the legally relevant state.

On TSA outages exceeding the declared pending duration, escalate to the compliance officer. On Merkle-chain verification failures recipient-side, treat as a stream-omission incident before responding to the regulator.

The worksheet is deployment-time. Per-transfer enforcement happens in `Sunfish.Kernel.Custody` through the four event contracts named in Ch15 §Chain-of-Custody.
```

---

## References to add to Ch15 reference list (at end, after [27])

```markdown
[28] Internet Engineering Task Force (IETF), "Internet X.509 Public Key Infrastructure Time-Stamp Protocol (TSP)," RFC 3161, Aug. 2001. [Online]. Available: https://www.rfc-editor.org/rfc/rfc3161

[29] European Parliament and Council, "Regulation (EU) No 910/2014 on electronic identification and trust services for electronic transactions in the internal market (eIDAS)," Official Journal of the European Union, Jul. 2014, Art. 41. [Online]. Available: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32014R0910

[30] S. A. Crosby and D. S. Wallach, "Efficient Data Structures for Tamper-Evident Logging," in *Proc. 18th USENIX Security Symposium*, Montreal, Aug. 2009, pp. 317–334. [Online]. Available: https://www.usenix.org/legacy/event/sec09/tech/full_papers/crosby.pdf

[31] Internet Engineering Task Force (IETF), "Certificate Transparency Version 2.0," RFC 9162, Dec. 2021. [Online]. Available: https://www.rfc-editor.org/rfc/rfc9162
```

---

## Cross-reference updates required in Ch15

Two existing phrases must update at draft-stage commit:

1. Line 228 — "the chain-of-custody mechanism (cross-reference #9)" → "§Chain-of-Custody for Multi-Party Transfers"
2. Line 389 — "Cross-reference to the chain-of-custody mechanism (#9) for the multi-party signed-event substrate that underpins both." → "Cross-reference to §Chain-of-Custody for Multi-Party Transfers for the multi-party signed-event substrate that underpins both."
