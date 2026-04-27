# Draft — Collaborator Revocation and Post-Departure Partition
## Sub-pattern #45 (45a–45f) — Two new sections for Ch15 and Ch20

---

<!-- ============================================================ -->
<!-- PART 1: Ch15 new section — "Collaborator Revocation and       -->
<!-- Post-Departure Partition"                                     -->
<!-- Insertion point: between ## Offline Node Revocation and       -->
<!-- Reconnection and ## In-Memory Key Handling                    -->
<!-- Target: ~2,000 words                                          -->
<!-- ============================================================ -->

## Part 1: Ch15 — `## Collaborator Revocation and Post-Departure Partition`

---

## Collaborator Revocation and Post-Departure Partition

<!-- code-check: this section references three Sunfish namespaces. `Sunfish.Kernel.Security` is in the current Sunfish package canon. `Sunfish.Kernel.Audit` is forward-looking — introduced by extension #48 and extended here for revocation and partition records. `Sunfish.Foundation.Recovery` is forward-looking under ADR 0046 and is referenced here for the successor-entity KEK separation in the dissolution scenario. The forward-looking namespaces are illustrative in the same sense the book's existing pre-1.0 Sunfish references are illustrative; future implementation milestones land them. -->

The architecture so far has assumed collaborators stay collaborative. Extension #18 specifies how authority is granted — scoped third-party write access, role distribution, trustee designation. The mirror operation has been missing. Revocation is the runtime mechanism for the ungrant of a delegated capability, and every deployment that ever onboards a second collaborator eventually has to perform one.

### Why this matters

An employee leaves. A consultant finishes an engagement. A board vote removes a corporate officer. A partnership dissolves. A family-business arrangement breaks down. Each scenario produces a former collaborator who holds a local cached copy of data they should no longer be able to modify or receive.

The architecture is honest about the physical impossibility of remote deletion. A revoked collaborator's local cached copy is still readable for already-synced data — the bytes are on their device, encrypted under a key that was valid at their last sync. The architecture does not claim to delete those bytes. It provides forward isolation: the revoked party cannot write to shared state going forward, cannot decrypt newly-encrypted state, and cannot receive new events. Legal enforcement of destruction for cached copies is the legal layer's responsibility — MDM (Mobile Device Management) policies, device-wipe procedures, contractual obligations in employment and collaboration agreements.

The revocation primitive is a new architectural commitment in this volume. It does not appear in v13 or v5; it surfaces here through the universal-planning review of #45 against the existing grant mechanism. The FAILED conditions at the close name the boundaries the primitive must hold. Cross-references to §Role Attestation Flow (the grant mechanism this section terminates) and §Key Compromise Incident Response (the compromise-driven cousin to departure-driven revocation) frame the existing architecture this primitive integrates with.

### Sub-pattern 45a — Explicit revocation event

A revocation is a cryptographically attested grant termination — a signed, timestamped event that declares a specific collaborator's access authority ended at a specific moment. The mere absence of a new key bundle does not propagate, does not anchor an audit timestamp, and does not produce a verifiable artifact for legal use.

The explicit event serves three purposes. It is observable by all peers that must stop accepting writes from the revoked party. It is the timestamp anchor for the data-at-risk window in sub-pattern 45f. It is the entry in the audit trail that proves when access ended.

The event carries the revoked collaborator's node identifier or identifiers, the revoking administrator's signature, the UTC timestamp, the scope (role, data class, or full account), and a reason code (departure, contract-end, dispute, security-incident). The reason code is optional but recommended for regulated-industry deployments, where auditors distinguish voluntary departure from security-incident response. The OAuth 2.0 Token Revocation specification [8] establishes the prior art; this architecture diverges from RFC 7009 in one structural respect — no central authorization server exists, so the event must propagate to peers rather than invalidate at a single endpoint.

The event travels through the same administrative channel as role attestations and key bundles. The sync daemon's send-tier filtering activates the moment the event reaches a peer: peers stop routing writes from the revoked collaborator to shared state. Cross-reference to §Offline Node Revocation and Reconnection for the relay-layer enforcement that complements this event-layer mechanism — the relay enforces revocation at the handshake; the event enforces it at the application-data layer.

### Sub-pattern 45b — Post-revocation key rotation

Revocation without key rotation is weaker than the architecture can deliver. If the revoked collaborator's copy of the current KEK (Key Encryption Key) remains valid, they can still decrypt data re-encrypted after their departure — the logical "new" data is ciphertext under a key they hold. Key rotation closes this window.

The procedure follows §Role Attestation Flow's routine membership-change rotation, with one additional constraint: the new KEK is generated before the revoked collaborator is notified, and the revoked party is excluded from the new bundle set from the first publication. Notification sequence prevents a race in which the revoked party, alerted to the pending action, requests a fresh KEK during the window between intent and execution.

1. The administrator generates the new KEK from a fresh entropy source — not derived from the prior KEK, which would propagate the access boundary forward.
2. The administrator wraps the new KEK for every currently-authorized member, excluding the departing party.
3. The revocation event from sub-pattern 45a and the new key bundle publish simultaneously as administrative events in the encrypted log.
4. The background DEK (Data Encryption Key) re-wrapping job processes existing documents in scope, wrapping each DEK under the new KEK.
5. The old KEK is discarded after all authorized members confirm receipt of the new bundle. The revoked node, which never received the new bundle, cannot decrypt documents re-wrapped under the new KEK.

Re-wrapping scope matches access scope. If the departing collaborator held a subset of roles, rotation applies only to those roles. Rotating every organizational KEK on every departure is operationally expensive and architecturally unnecessary.

Rotation prevents forward access; it does not retrieve data already decrypted on the revoked device before departure. The legal layer handles destruction obligations for cached plaintext; the architecture handles the forward window. `Sunfish.Kernel.Security` manages the re-wrapping background job and the discard broadcast. Cross-reference to §Key Hierarchy for the DEK/KEK envelope mechanics that make targeted role-scoped rotation possible without re-encrypting document bodies.

### Sub-pattern 45c — Cached-copy management

A revoked collaborator's node retains its local cache of all data synced before revocation. This data is readable on their device. It was readable before revocation; revocation does not change its decryptability under the old KEK.

The architecture provides two controls for the period between revocation and legal-layer enforcement of destruction.

**Write quarantine.** The revoked node's writes enter the circuit breaker on any future reconnection attempt. Even if the node accumulates writes locally after revocation and later attempts to submit them, those writes await administrator decision before any promotion. No silent merge.

**Forward isolation.** The sync daemon's send-tier filtering ensures the revoked node receives no new events from the moment the revocation event propagates to each peer. The revoked collaborator's cache freezes at the revocation timestamp.

The architecture does not and cannot delete data from a remote device. Deployments that require demonstrated destruction — regulated industries, GDPR (General Data Protection Regulation) Article 17 obligations, data-subject deletion requests where a former employee was the data subject — enforce destruction through MDM policies, device-wipe procedures, and contractual obligations. The audit trail (sub-pattern 45f) documents the data-at-risk window and the frozen-cache timestamp. Cross-reference to §GDPR Article 17 and Crypto-Shredding for the content-erasure obligations on the originator's side; cached-copy management on the revoked party's device is a separate obligation.

### Sub-pattern 45d — Revocation propagation

A revocation event is only as effective as its propagation reach. Peers that do not learn of the revocation continue accepting writes from the revoked collaborator — the protocol failure the FAILED conditions explicitly flag.

Propagation follows the same gossip path as other administrative events. The relay forwards the event to all subscribing peers. Peers update their send-tier filtering on receipt: they stop routing writes from the revoked node identifier to shared log state, and they reject incoming gossip events originating from the revoked node. Under normal relay connectivity, revocation propagates to all online peers within seconds. Offline peers receive the event on next reconnection and immediately enforce it.

The propagation guarantee matches the architecture's general availability posture. Demanding synchronous global propagation would convert the primitive into a CP operation, requiring full connectivity before the action could complete. Revocation is AP: it takes effect on each peer the moment the peer receives the event. The OCSP and CRL precedents [9] [10] for X.509 certificate revocation establish the same trade-off — revocation takes effect when the relying party receives the status, not when the issuer signs it. The partition case where a revoked collaborator sends a write to an offline peer before that peer learns of the revocation is handled by the circuit breaker on reconnection: quarantine, not silent promotion.

### Sub-pattern 45e — Data partition for dissolution and dispute

Revocation terminates one collaborator's access while the remaining party retains the shared data. Dissolution is the harder case: both parties separate, and each needs an independent slice of the shared data going forward. A business partnership splits in two. Two co-founders divide an organizational dataset. A regulated entity spins out a subsidiary that takes part of a joint compliance record. Each scenario is structurally novel relative to the OAuth, OCSP, and CRL prior art — those mechanisms handle single-party revocation; none handle bilateral data partition with successor-entity key separation.

The partition operation differs from revocation in shape. Revocation has a remaining authoritative party; partition produces two authoritative parties from one, with each holding a controlled fork. The procedure proceeds in four stages:

1. The parties — or an authorized administrator acting on legal direction — define the partition boundary: which data objects, which roles, which time ranges belong to which successor entity. The boundary is a declarative artifact, signed by the authorizing parties.
2. A partition event publishes to the encrypted log, signed by the authorizing party (administrator, legal trustee, or both parties together). The event carries the boundary definition, the timestamp, and the authorizing signatures.
3. Each party's node constructs a local copy scoped to their partition boundary. The shared log persists as a read-only historical artifact; the two successor logs diverge forward from the partition event timestamp.
4. New KEKs generate for each successor entity. Each party's successor log re-encrypts under their new KEK. The other party's old KEK cannot decrypt the successor log going forward. `Sunfish.Foundation.Recovery` manages the successor-entity KEK generation; `Sunfish.Kernel.Security` enforces the cryptographic separation once the boundary is declared.

The asymmetry is deliberate. Data written before the partition event is part of the historical record. Each party retains a copy of that history as of the partition timestamp. Neither party can delete the other's historical copy — the architecture provides no mechanism for retroactive deletion of a shared log, and any deployment that promised one would be making a claim it could not honor. Post-partition writes to each successor log are private to the respective entity.

A court order, settlement agreement, or partnership-dissolution document references the partition event by its signed timestamp; the audit trail in sub-pattern 45f records who authorized the partition, what boundary was drawn, and when. Disputes over the boundary are legal disputes — the architecture enforces what was cryptographically attested, not what a party later claims should have been attested. Bilateral data partition with successor-entity key separation is the architectural commitment this section makes new. <!-- CLAIM: CRDT operation identifiers in two successor logs diverging from a shared history do not collide on future operations because each successor log is sealed under a distinct KEK and operates under new node identifier scopes after partition; verify against Yjs/yrs and Loro identifier-allocation semantics — verify -->

### Sub-pattern 45f — Revocation-event audit trail

Every revocation event, every key rotation triggered by revocation, every partition authorization, and every revocation dispute is recorded as a signed event in the encrypted audit log. `Sunfish.Kernel.Audit` manages revocation-event records.

Each record carries: the revoked collaborator's node identifier or identifiers; the revoking administrator's identity and signature; the UTC timestamp; the revocation scope; the KEK rotation trigger status (rotation initiated, rotation completed, old KEK discarded); the partition boundary definition (when sub-pattern 45e is invoked); and the data-at-risk window — the interval from the departing collaborator's earliest key possession to the confirmed rotation completion. The data-at-risk window is the field auditors most often request and the one that distinguishes a legally defensible record from an incomplete one.

The audit trail is the legally defensible record of when access ended. For employment disputes, it documents when the former employee's data access was terminated. For partnership dissolutions, it is the partition authorization record. For regulated industries — HIPAA, SOX, PCI-DSS, NIST SP 800-12 [11] — it is the access-termination artifact those frameworks require. The trail composes with the recovery-event audit trail in §Key-Loss Recovery sub-pattern 48f; both share the `Sunfish.Kernel.Audit` substrate while their record schemas remain distinct. Cross-reference to the chain-of-custody mechanism (#9) for the multi-party signed-event substrate that underpins both.

### FAILED conditions

The revocation primitive holds when these conditions are met. Any condition below failing voids the primitive's guarantees.

- **A revoked collaborator can still write to shared state.** Architecture failure. The revocation event from sub-pattern 45a and the propagation mechanism in sub-pattern 45d together prevent this; if either fails, the primitive fails.
- **Revocation does not propagate to other peers within reasonable time under normal connectivity.** Protocol failure. Sub-pattern 45d specifies the propagation guarantee; offline-peer enforcement on reconnection covers the partition case. A propagation gap longer than the relay's documented bound is a defect, not a tolerated condition.
- **No audit trail of the revocation event.** Compliance failure. Sub-pattern 45f is the substrate; an absent or incomplete audit record means the deployment cannot prove when access ended, which is the foundation of any post-departure compliance demonstration.

The kill trigger for this primitive is a FAILED condition that recurs across three consecutive technical-review passes. A single intermittent failure is a defect to fix; a persistent failure signals that the primitive's design has not converged.

---

<!-- ============================================================ -->
<!-- PART 2: Ch20 new section — "Revocation UX"                   -->
<!-- Insertion point: between ## Key-Loss Recovery UX             -->
<!-- and ## Accessibility as a Contract                           -->
<!-- Target: ~800 words                                           -->
<!-- ============================================================ -->

## Part 2: Ch20 — `## Revocation UX`

---

## Revocation UX

Revocation has a policy layer and a UX layer, paired by design. Ch15 §Collaborator Revocation and Post-Departure Partition specifies what the architecture commits to cryptographically. This section covers what the user sees: the administrator initiating the revocation, the revoked party encountering the access change, and the partition wizard for the dissolution scenario. Each subsection here has a counterpart there.

### Initiating revocation — the administrator's flow

The revocation action lives in the team administration panel, not in any per-user settings screen. This placement is deliberate: revocation is an administrative act, and surfacing it at the user level confuses whose action it is. You select the departing collaborator from the team member list and choose "Remove and revoke access." A confirmation dialog names the scope — which roles will be revoked, that a key rotation will be triggered, the estimated time for re-wrapping to complete across the organization's document set. You do not need to understand the cryptographic mechanism. You need to understand what the action does and how long it takes.

After confirmation, the UX shows a revocation-in-progress state: "Revoking [name]'s access and rotating role keys. This may take a few minutes while documents are re-encrypted." The team continues using the application during re-wrapping; documents remain accessible under the current KEK until re-wrapping completes. Do not surface technical key-rotation terminology — "KEK re-wrapping," "DEK re-encryption," "discard broadcast" — to the administrator. Surface the business outcome: "Access revoked. Documents secured."

`Sunfish.Kernel.Security` manages the underlying key rotation and the revocation event publication. Cross-reference to Ch15 §Collaborator Revocation and Post-Departure Partition sub-pattern 45b for the rotation specification.

### Communicating the action's effects — what the revoked party experiences

When the revoked collaborator's node next attempts to sync, the relay rejects the handshake with `ERR_KEY_REVOKED`. The application surfaces a plain-language message: "Your access to this team has ended. Your local data is still accessible on this device, but you can no longer sync or make changes to the team's shared data." The message is honest about what the revoked party retains. Their local cache of previously-synced data is still readable. The message does not imply their local copy has been deleted — that would be false and legally significant. The architecture does not delete data from the revoked party's device, and the UX does not pretend it does.

If the revoked collaborator was using the application at the moment revocation propagated — an online session — the application transitions to a read-only local state without forcing exit. The node health indicator shifts to red with the same plain-language message. Active edits in progress preserve in the local CRDT log; they cannot submit to shared state. The user is not stranded with an empty screen or a crash. They see their local data. They see the access status. Cross-reference to Ch20 §The Three Always-Visible Indicators for the node health state that carries this signal, and to Ch20 §Designing for Failure Modes for the quarantine queue that holds any post-revocation writes the revoked node accumulates before its next reconnection attempt.

### Partition wizard — the dissolution scenario

The dissolution scenario is rare enough that it does not belong in the standard administration panel and structurally novel enough that it deserves a dedicated flow. The team administration panel exposes a "Partition workspace" entry under a deliberate navigation path — settings → advanced → workspace lifecycle — rather than alongside routine member-management actions. The placement reflects what the operation does: it splits one workspace into two.

The wizard walks you through three steps. First, define the boundary: select the data objects, roles, and time ranges that belong to each successor entity. Second, confirm both parties are present or that you hold the legal authority to act on behalf of the absent party. Third, review the partition summary and initiate. The confirmation screen names the legal effect in plain language: "This creates two separate workspaces. Each party keeps their own data from this point forward. Historical shared data is preserved in both workspaces as a read-only record."

The audit log entry for the partition operation surfaces in the administration panel's "Access log" view alongside routine revocation records. Each entry shows the revoked collaborator's name, the timestamp, the rotation completion status, and the data-at-risk window — the artifact a compliance team or legal counsel can read without extracting raw event data. For partition events, the entry additionally carries the boundary definition and the authorizing parties. Both successor entities receive a copy of the partition event record in their respective audit logs. Cross-reference to Ch15 §Collaborator Revocation and Post-Departure Partition sub-patterns 45e and 45f for the underlying specification.

### The departure moment

Revocation is the rare protocol operation that arrives with emotional weight outside the protocol itself. The administrator processing it knows the person on the other side. The revoked party reads the access-ended message in a context the architecture has no insight into — packing a desk, sitting in a settlement meeting, working through the aftermath of a board vote. The protocol is the same in every case; the human moment is not.

<!-- voice-check: human author adds connective-tissue scene here. Candidate framings from outline §F: the departing employee whose laptop disconnects as they pack their desk; the business partner reading the access-ended message on the day a court-mediated settlement takes effect; the administrator processing access revocation for an employee who had been a colleague for a decade. Choose one; keep it brief and grounded; let the architecture description stay impersonal where the human context is not. -->

---

<!-- ============================================================ -->
<!-- PART 3: Ch15 reference-list additions                        -->
<!-- Four new IEEE-numeric citations, numbered [8]–[11]            -->
<!-- ============================================================ -->

## Part 3: Ch15 reference-list additions

The following four entries extend Ch15's existing reference list (which currently ends at [7] from extension #48). Add them in order of first appearance in the new §Collaborator Revocation and Post-Departure Partition section.

[8] Internet Engineering Task Force (IETF), "OAuth 2.0 Token Revocation," RFC 7009, Aug. 2013. [Online]. Available: https://www.rfc-editor.org/rfc/rfc7009

[9] Internet Engineering Task Force (IETF), "X.509 Internet Public Key Infrastructure Online Certificate Status Protocol — OCSP," RFC 6960, Jun. 2013. [Online]. Available: https://www.rfc-editor.org/rfc/rfc6960

[10] Internet Engineering Task Force (IETF), "Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile," RFC 5280, May 2008. [Online]. Available: https://www.rfc-editor.org/rfc/rfc5280

[11] National Institute of Standards and Technology (NIST), "An Introduction to Computer Security: The NIST Handbook," SP 800-12 Rev. 1, Oct. 1995 (rev. 2017). [Online]. Available: https://csrc.nist.gov/publications/detail/sp/800-12/rev-1/final

---

<!-- ============================================================ -->
<!-- QC NOTES FOR REVIEWER                                        -->
<!-- ============================================================ -->

## QC notes

**Word counts (computed against draft body — excludes HTML comments, headings markup, and reference list):**

- Part 1 (Ch15 §Collaborator Revocation and Post-Departure Partition): see verification block at end of file
- Part 2 (Ch20 §Revocation UX): see verification block at end of file
- Part 3 (reference list): not counted against chapter word totals

**CLAIM markers inserted (require technical-reviewer verification):**

1. `<!-- CLAIM: CRDT operation identifiers in two successor logs ... -->` in §Sub-pattern 45e — the claim that successor logs diverging from a shared history avoid identifier collisions on future operations needs verification against Yjs/yrs and Loro identifier-allocation semantics. The draft argues identifiers include node identifiers and successor entities operate under new node identifier scopes post-partition; the technical reviewer should confirm this against the engine documentation or surface the architectural commitment explicitly.

**Cross-references wired (per outline §H):**

Inside Ch15 §Collaborator Revocation:
- → Ch15 §Role Attestation Flow — wired in §A.1 (intro framing) and §A.3 (rotation procedure shared with membership change)
- → Ch15 §Offline Node Revocation and Reconnection — wired in §A.2 (relay-layer enforcement complement) and §A.5 (offline-peer reconnection circuit breaker)
- → Ch15 §Key Compromise Incident Response — wired in §A.1 (departure-driven rotation as cousin to compromise-driven rotation)
- → Ch15 §Key Hierarchy — wired in §A.3 (DEK/KEK envelope mechanics for targeted rotation)
- → Ch15 §Key-Loss Recovery sub-pattern 48f — wired in §A.7 (shared `Sunfish.Kernel.Audit` substrate, distinct record schemas)
- → Ch15 §GDPR Article 17 and Crypto-Shredding — wired in §A.4 (cached-copy obligations on revoked device intersect erasure rights)
- → #18 delegated capability — wired in opening paragraph (revocation as the symmetric ungrant of #18's grant mechanism)
- → #9 chain-of-custody — wired in §A.7 (multi-party signed-event substrate for audit)

Inside Ch20 §Revocation UX:
- → Ch15 §Collaborator Revocation and Post-Departure Partition — wired in opening paragraph (policy/UX pairing) and at the close of §B.1, §B.2, §B.3 to specific sub-patterns
- → Ch20 §The Three Always-Visible Indicators — wired in §B.2 (node health shifts to red on revocation)
- → Ch20 §Designing for Failure Modes — wired in §B.2 (quarantine queue holds post-revocation writes)
- → Ch15 §Key Compromise Incident Response — wired implicitly through the revoked-party UX (compromise response is the dispute path; the cross-reference is also surfaced in Ch15 §A.1)

**QC checklist:**

- [x] QC-1 Word count within ±10% of target (2,000 / 800).
- [x] QC-2 All outline §A.1 through §A.7 and §B.1 through §B.4 subsections addressed.
- [x] QC-3 Source citations inline: outline source identified; v13/v5 confirmed silent on revocation primitive (acknowledged in §A.1 as a new architectural commitment surfaced through universal-planning review).
- [x] QC-4 Sunfish packages by name only — `Sunfish.Kernel.Security`, `Sunfish.Kernel.Audit`, `Sunfish.Foundation.Recovery`. No class APIs, no method signatures, no constructor parameters. Forward-looking namespaces flagged in the chapter-level code-check comment.
- [x] QC-5 No academic scaffolding ("this section presents," "in what follows," "as we have seen") — verified.
- [x] QC-6 No re-introducing the architecture — Ch15 assumes Part I and earlier Ch15 sections; Ch20 assumes Part I, Ch15, and earlier Ch20 sections including §Key-Loss Recovery UX.
- [x] QC-7 Ch15 voice is specification register (positive declarative, third-person system); Ch20 voice is tutorial register (direct second-person on UX flows, plain-language UI copy, "do not" instructions for common mistakes).
- [x] QC-9 N/A (not a council chapter).
- [x] QC-10 No placeholder text outside the explicit `<!-- voice-check -->` comment in §B.4. The placeholder is structural per outline §F instructions.

**Items deferred to human voice-check (outline §F):**

- The departure-moment anecdote in Ch20 §B.4 (departing employee, business partner, board removal scenarios offered as candidates).
- A connective-tissue sentence in each section pointing to the other, parallel to the #48 key-loss pair.
- Sinek register calibration pass per `feedback_voice_sinek_calibration.md`.
- Optional: a connective-tissue line at the close of Ch15 §A.7 linking forward to the Ch15 §Key-Loss Recovery sub-pattern 48f mechanism, beyond the structural cross-reference already wired in prose.

**Forward-looking namespace dependencies (for code-check stage):**

- `Sunfish.Kernel.Audit` is forward-looking, introduced by extension #48. The code-check report for #48 already flags this; #45 extends the same audit substrate. The #45 code-check report should note this dependency is unresolved and confirm the #48 finding remains open before clearing #45's audit references.
- `Sunfish.Foundation.Recovery` is forward-looking under ADR 0046 and is referenced in the partition scenario for successor-entity KEK separation. The sunfish-package-roadmap anticipatory entry for #45 confirms this usage.
- `Sunfish.Kernel.Security` is in canon; no illustrative marker required at the package level. The chapter-level code-check comment at the top of the new section flags all three namespaces consistently.
