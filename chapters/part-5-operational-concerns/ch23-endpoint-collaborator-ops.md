# Chapter 23 — Endpoint, Collaborator, and Custody Operations

<!-- icm/draft -->

<!-- Target: ~7,000 words (post-prune; UPF Ch15 split kill-trigger fired 2026-04-30; Ch22 split into Ch22 Key Lifecycle Ops + Ch23 Endpoint + Collaborator + Custody Ops). -->
<!-- Source: post-Ch15-split + post-Ch22-Ch23 split per UPF FAILED-condition. This chapter absorbs five operational flows whose triggers are external state changes rather than key-lifecycle events: an offline node returning to a network where its credentials were revoked while it was disconnected, a collaborator's role being withdrawn, an endpoint operating system going hostile, a multi-party data transfer that requires verifiable custody, and a record's classification escalating in response to an external event. -->

<!-- code-check: namespaces inherited from Ch15. Sunfish.Kernel.Security, Sunfish.Kernel.Sync, Sunfish.Kernel.Audit, Sunfish.Kernel.Custody (forward-looking from #9), Sunfish.Foundation.Catalog (forward-looking from #10). Per-section code-check annotations carried with their sections. -->

---

Chapter 15 specifies the security architecture; Chapter 22 specifies the key-lifecycle operational flows. This chapter specifies the operational flows whose triggers come from outside the key lifecycle: a node returning from offline, a person leaving the team, a hostile OS, a data handoff to a third party, a regulatory event escalating a record's class.

Each section is a self-contained operational flow. Cross-references point back to Chapter 15 (architectural primitives) and Chapter 22 (key-lifecycle operations) where readers need that context.

---

## Offline Node Revocation and Reconnection


A node that is offline when a revocation event occurs does not receive that event until reconnection. The relay enforces revocation at the handshake layer, not through an out-of-band push.

When an offline node attempts to reconnect, the sync daemon presents the node's current attestation bundle to the relay. The relay checks each key identifier in the bundle against the revocation log. If any key has been revoked, the relay rejects the handshake with error code `ERR_KEY_REVOKED` — not a generic connection failure. The specific error code allows the node's client to distinguish between a network problem, an expired certificate, and a deliberate revocation.

The node cannot resume sync until the user re-authenticates through the IdP (Identity Provider). Re-authentication establishes fresh role attestations against current team state. After successful re-authentication, the administrator's device detects the reconnected node and issues new wrapped KEK copies for the roles the user currently holds. Once the new key bundle arrives and is stored in the OS keystore, sync resumes.

The user-visible message on revocation rejection is: "Your access credentials have been updated. Sign in again to continue syncing." The message avoids technical terminology and does not indicate whether the revocation was triggered by a compromise, a role change, or an administrative rotation.

A node whose revocation predates its last offline period may have accumulated writes in its local CRDT store during that period. Those writes enter the circuit breaker quarantine on reconnection and await administrator review before promotion. The combination of relay-level revocation rejection and circuit breaker quarantine ensures that a revoked node cannot inject writes into the live system without explicit administrator decision.

**Offline compromise window.** A node that is offline during a KEK discard broadcast continues to use the old — potentially compromised — KEK until reconnection. The architecture bounds this exposure in two ways. First, role-scoped KEKs rotate on a configurable schedule (default: every 90 days, or on any role-membership change), so an old KEK outside rotation has an intrinsic validity horizon. Second, the relay enforces revocation on reconnect — a node presenting an attestation against a revoked KEK receives `ERR_KEY_REVOKED` and cannot resume sync until re-attested. Documents encrypted with the compromised KEK between the discard broadcast and the offline node's reconnect remain readable by any holder of the old KEK during that window. The mitigation is time-bounded key validity enforced at the relay, with high-sensitivity deployments shortening the rotation schedule to reduce exposure. This is the honest boundary of the compromise-response procedure. The architecture cannot retroactively un-read data.

---

## Collaborator Revocation and Post-Departure Partition


<!-- code-check: this section references three Sunfish namespaces. `Sunfish.Kernel.Security` and `Sunfish.Kernel.Audit` are in the current Sunfish package canon (verified 2026-04-28: packages/kernel-audit/ exists). `Sunfish.Foundation.Recovery` is forward-looking under ADR 0046 — referenced here for the successor-entity KEK separation in the dissolution scenario; illustrative in the same sense the book's existing pre-1.0 Sunfish references are illustrative. -->

The architecture so far has assumed collaborators stay collaborative. Extension #18 specifies how authority is granted — scoped third-party write access, role distribution, trustee designation. The mirror operation has been missing. Revocation is the runtime mechanism for the ungrant of a delegated capability, and every deployment that ever onboards a second collaborator eventually has to perform one.

### Why this matters

An employee leaves. A consultant finishes an engagement. A board vote removes a corporate officer. A partnership dissolves. A family-business arrangement breaks down. Each scenario produces a former collaborator who holds a local cached copy of data they should no longer be able to modify or receive.

The architecture is honest about the physical impossibility of remote deletion. A revoked collaborator's local cached copy is still readable for already-synced data — the bytes are on their device, encrypted under a key that was valid at their last sync. The architecture does not claim to delete those bytes. It provides forward isolation: the revoked party cannot write to shared state going forward, cannot decrypt newly-encrypted state, and cannot receive new events. Legal enforcement of destruction for cached copies is the legal layer's responsibility — MDM (Mobile Device Management) policies, device-wipe procedures, contractual obligations in employment and collaboration agreements.

The revocation primitive extends a partial precedent. The companion architecture paper specifies key rotation on role-membership change as a single procedure: generate a new KEK, re-wrap DEKs for the remaining members, discard the old KEK. That procedure covers the cryptographic mechanics of sub-pattern 45b. The other five sub-patterns in this section — the explicit revocation event (45a), cached-copy management (45c), revocation propagation across peers (45d), bilateral data partition for dissolution (45e), and the revocation-event audit trail (45f) — are new architectural commitments in this volume, surfaced through the universal-planning review of #45 against the existing grant mechanism. The FAILED conditions at the close name the boundaries the primitive must hold. Cross-references to §Role Attestation Flow (the grant mechanism this section terminates) and §Key Compromise Incident Response (the compromise-driven cousin to departure-driven revocation) frame the existing architecture this primitive integrates with.

### Sub-pattern 45a — Explicit revocation event

A revocation is a cryptographically attested grant termination — a signed, timestamped event that declares a specific collaborator's access authority ended at a specific moment. The mere absence of a new key bundle does not propagate, does not anchor an audit timestamp, and does not produce a verifiable artifact for legal use.

The explicit event serves three purposes. All peers observe it and stop accepting writes from the revoked party. It anchors the timestamp for the data-at-risk window in sub-pattern 45f. It records the audit-trail entry that proves when access ended.

The event carries the revoked collaborator's node identifier or identifiers, the revoking administrator's signature, the UTC timestamp, the scope (role, data class, or full account), and a reason code (departure, contract-end, dispute, security-incident). The reason code is optional but recommended for regulated-industry deployments, where auditors distinguish voluntary departure from security-incident response. The OAuth 2.0 Token Revocation specification [8] establishes the prior art; this architecture diverges from RFC 7009 in one structural respect — no central authorization server exists, so the event must propagate to peers rather than invalidate at a single endpoint.

The event travels through the same administrative channel as role attestations and key bundles. The sync daemon's send-tier filtering activates the moment the event reaches a peer: peers stop routing writes from the revoked collaborator to shared state. Cross-reference to §Offline Node Revocation and Reconnection for the relay-layer enforcement that complements this event-layer mechanism — the relay enforces revocation at the handshake; the event enforces it at the application-data layer.

### Sub-pattern 45b — Post-revocation key rotation

Revocation without key rotation is weaker than the architecture can deliver. If the revoked collaborator's copy of the current KEK (Key Encryption Key) remains valid, they can still decrypt data re-encrypted after their departure — the logical "new" data is ciphertext under a key they hold. Key rotation closes this window.

The procedure follows §Role Attestation Flow's routine membership-change rotation, with one additional constraint: the administrator generates the new KEK before notifying the revoked collaborator, and excludes the revoked party from the new bundle set from the first publication. Notification sequence prevents a race in which the revoked party, alerted to the pending action, requests a fresh KEK during the window between intent and execution. The five-step sequence:

1. The administrator generates the new KEK from a fresh entropy source — not derived from the prior KEK, which would propagate the access boundary forward.
2. The administrator wraps the new KEK for every currently-authorized member, excluding the departing party.
3. The administrator publishes the revocation event from sub-pattern 45a and the new key bundle simultaneously as administrative events in the encrypted log.
4. The background DEK (Data Encryption Key) re-wrapping job processes existing documents in scope, wrapping each document's DEK under the new KEK.
5. `Sunfish.Kernel.Security` discards the old KEK after all authorized members confirm receipt of the new bundle. The revoked node, which never received the new bundle, cannot decrypt documents re-wrapped under the new KEK.

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

The propagation guarantee matches the architecture's general availability posture. Demanding synchronous global propagation would convert the primitive into a CP operation, requiring full connectivity before the action could complete. Revocation is AP: it takes effect on each peer the moment the peer receives the event. The OCSP and CRL precedents [9] [10] for X.509 certificate revocation establish the same trade-off — revocation takes effect when the relying party receives the status, not when the issuer signs it. The circuit breaker on reconnection handles the partition case where a revoked collaborator sends a write to an offline peer before that peer learns of the revocation: quarantine, not silent promotion.

### Sub-pattern 45e — Data partition for dissolution and dispute

Revocation terminates one collaborator's access while the remaining party retains the shared data. Dissolution is the harder case: both parties separate, and each needs an independent slice of the shared data going forward. A business partnership splits in two. Two co-founders divide an organizational dataset. A married couple with shared finances begins running separate accounts. A regulated entity spins out a subsidiary that takes part of a joint compliance record.

Each scenario is structurally novel relative to the OAuth, OCSP, and CRL prior art — those mechanisms handle single-party revocation; none handle bilateral data partition with successor-entity key separation.

The partition operation differs from revocation in shape. Revocation has a remaining authoritative party; partition produces two authoritative parties from one, with each holding a controlled fork. The partition procedure proceeds in four stages:

1. The parties — or an authorized administrator acting on legal direction — define the partition boundary: which data objects, which roles, which time ranges belong to which successor entity. The boundary is a declarative artifact, signed by the authorizing parties.
2. The authorizing party (administrator, legal trustee, or both parties together) publishes a partition event to the encrypted log under their signature. The event carries the boundary definition, the timestamp, and the authorizing signatures.
3. Each party's node constructs a local copy scoped to their partition boundary. The shared log persists as a read-only historical artifact; the two successor logs diverge forward from the partition event timestamp.
4. `Sunfish.Foundation.Recovery` generates a fresh KEK for each successor entity. Each party re-encrypts their successor log under that new KEK. The other party's old KEK cannot decrypt the successor log going forward. `Sunfish.Kernel.Security` enforces the cryptographic separation once the boundary is declared.

The asymmetry is deliberate. Data written before the partition event is part of the historical record. Each party retains a copy of that history as of the partition timestamp. Neither party can delete the other's historical copy — the architecture provides no mechanism for retroactive deletion of a shared log, and any deployment that promised one would be making a claim it could not honor. Post-partition writes to each successor log are private to the respective entity.

The legal layer references the architectural artifact. A court order, settlement agreement, or partnership-dissolution document names the partition event by its signed timestamp; the audit trail in sub-pattern 45f records who authorized the partition, what boundary was drawn, and when. Disputes over the boundary itself are legal disputes — the architecture enforces what was cryptographically attested, not what a party later claims should have been attested. Bilateral data partition with successor-entity key separation is this section's new architectural commitment.

CRDT operation-identifier semantics in both engines the architecture targets confirm the partition is safe. Yjs assigns every operation an `(clientID, clock)` pair where `clientID` is a random 53-bit integer chosen on first insert and `clock` is a per-client monotonic counter [12]. Loro uses the same shape: `ID = (PeerID, Counter)` where `PeerID` is a random `u64` and `Counter` is a per-peer monotonic `i32` [13].

Two properties of the partition prevent identifier collision between the successor logs. First, the architectural commitment is that the two successor logs never re-merge — they are forks, not branches awaiting reconciliation, and operations from one log never integrate into the other. The KEK separation enforces this at the cryptographic layer (the other party's KEK cannot decrypt the successor log going forward). Second, the partition protocol assigns a fresh node identifier scope to each successor entity, so even if the same physical device later associates with both successor entities through some out-of-band path, its operations in each log carry distinct `clientID`/`PeerID` values. Either property alone closes the collision question; the two together make it structural.

### Sub-pattern 45f — Revocation-event audit trail

`Sunfish.Kernel.Audit` records every revocation event, every key rotation triggered by revocation, every partition authorization, and every revocation dispute as a signed entry in the encrypted audit log.

Each record carries: the revoked collaborator's node identifier or identifiers; the revoking administrator's identity and signature; the UTC timestamp; the revocation scope; the KEK rotation trigger status (rotation initiated, rotation completed, old KEK discarded); the partition boundary definition (when sub-pattern 45e is invoked); and the data-at-risk window — the interval from the departing collaborator's earliest key possession to the confirmed rotation completion. The data-at-risk window is the field auditors most often request and the one that distinguishes a legally defensible record from an incomplete one.

The audit trail is the legally defensible record of when access ended. For employment disputes, it documents when the deployment terminated the former employee's data access. For partnership dissolutions, it is the partition authorization record. For regulated industries — HIPAA, SOX, PCI-DSS, NIST SP 800-12 [11] — it is the access-termination artifact those frameworks require. The trail composes with the recovery-event audit trail in §Key-Loss Recovery sub-pattern 48f; both share the `Sunfish.Kernel.Audit` substrate while their record schemas remain distinct. Cross-reference to §Chain-of-Custody for Multi-Party Transfers for the multi-party signed-event substrate that underpins both.

### FAILED conditions

The revocation primitive fails when any of the conditions below holds. Any one of them voids the primitive's guarantees.

- **A revoked collaborator can still write to shared state.** Architecture failure. The revocation event from sub-pattern 45a and the propagation mechanism in sub-pattern 45d together prevent this; if either fails, the primitive fails.
- **Revocation does not propagate to other peers within reasonable time under normal connectivity.** Protocol failure. Sub-pattern 45d specifies the propagation guarantee; offline-peer enforcement on reconnection covers the partition case. A propagation gap longer than the relay's documented bound is a defect, not a tolerated condition.
- **No audit trail of the revocation event.** Compliance failure. Sub-pattern 45f is the substrate; an absent or incomplete audit record means the deployment cannot prove when access ended, which is the foundation of any post-departure compliance demonstration.

The kill trigger for this primitive is a FAILED condition that recurs across three consecutive technical-review passes. A single intermittent failure is a defect to fix; a persistent failure signals that the primitive's design has not converged.`) for #45 departure-moment scene relocates with this section; voice-plan.yaml entry updates to point at Ch22. -->

---

## Endpoint Compromise: What Stays Protected


The protections in §In-Memory Key Handling assume the OS is honest. This section examines what happens when it is not. P6 makes a strong claim: data is encrypted at rest and in transit, keys never leave the node unencrypted, and the relay sees only ciphertext. That claim holds against a network adversary. It does not hold unchanged against an endpoint adversary.

The distinction is load-bearing. A user who reads only the P6 summary and concludes that their data is safe even when their phone is running Pegasus has drawn an incorrect inference. The architecture is responsible for making the correct inference available. This section adds the endpoint-compromise row to the master taxonomy in §Threat Model and fills it in.

Sub-pattern 47a is the explicit scope declaration: the security chapter itself names what protection the architecture provides and what it does not provide when the endpoint is compromised. Not a footnote. Not a disclaimer appended to the conclusion. A dedicated section a practitioner can reference directly, in response to the council's original challenge on over-claiming security guarantees (Ch7 §The Security Lens).

### Sub-pattern 47a — Scope declaration

The table below is the specification. It states what the architecture protects, what it does not protect, and the residual risk when the endpoint is compromised at OS level or hardware level.

| Protected | Not protected | Residual risk |
|---|---|---|
| Other users' data on the relay | Local key material once OS is compromised | Attacker reads plaintext in memory or in the OS keychain |
| Other devices in the user's fleet | The local node's cached copy | Attacker reads cached documents under the locally-held DEKs |
| Future ciphertext after key rotation | Past ciphertext under current keys | Attacker holds the keys; decryption is trivial |
| Transaction integrity (backdate attacks blocked) | The user's current session actions | Attacker impersonates the user going forward until revocation |

The table is not decorative. It is the deliverable for sub-pattern 47a, and it must appear verbatim in any deployment's security reference. The FAILED conditions for the primitive are derived from it: an architecture that allows a compromised endpoint to silently impersonate other devices, to backdate transactions, or that ships without documenting the endpoint-compromise scope, has not met the 47a specification.

### Sub-pattern 47b — HSM and Secure Enclave separation

The strongest hardware-level defense is key material that never leaves a tamper-resistant hardware module, even when the host OS is fully compromised. The Apple Secure Enclave [7], Google Pixel Titan M [20], and Microsoft Pluton [21] are production-deployed examples. The architecture's key hierarchy (§Key Hierarchy) places the root KEK in the platform's secure enclave when available. An attacker who owns the OS cannot extract the KEK by reading process memory or the keychain — the key exists only inside the enclave and is never presented to the OS in plaintext.

The protection boundary requires precision. Enclaves protect key material from OS-level extraction. They do not protect against a user who is coerced into authenticating — the rubber-hose boundary is outside any cryptographic primitive's scope. They do not protect against every physical hardware attack on the enclave itself: Intel SGX is the cautionary tale here, with multiple published academic side-channel attacks against successive generations [22][23][24]. Apple Secure Enclave and Google Titan M have a substantially better field record, and ARM TrustZone offers a comparable model on Arm-class hardware [25]. The architecture does not claim Secure Enclave is immune to all hardware attack; it claims the academic attack record is substantially shorter, and the deployment posture treats SGX and the others differently as a result.

`Sunfish.Kernel.Security` binds key material to the platform's secure enclave API on device classes where an enclave is available. On device classes without a hardware enclave — older Android devices, some Windows devices without Pluton — the package falls back to OS-keystore isolation with explicit documentation that the protection level is lower. The architecture does not silently degrade. The startup report identifies the key-storage tier in use, and administrators enforce a minimum tier through the deployment manifest. Regulated-tier deployments mandate enclave-backed key storage. Consumer-tier deployments encourage it.

### Sub-pattern 47c — Attested boot and integrity measurement

A compromised endpoint is most dangerous when the compromise is invisible — when the device continues to participate in the sync mesh without the relay or other peers detecting the anomaly. Attested boot addresses this. TPM 2.0 and equivalent mechanisms produce a cryptographic proof that the device is running expected, unmodified software at boot time. The node presents the attestation to the relay at handshake; the relay validates it against a known-good measurement before admitting the session. The relay denies admission to a device that fails attestation, and the device falls back to local-only operation. It does not silently contaminate the sync mesh.

The attestation surface integrates at the sync daemon's handshake layer (Ch14 §Sync Daemon Protocol). `Sunfish.Kernel.Security` exposes the attestation; the relay-side enforcement is in the relay's handshake policy, not the node package. <!-- CLAIM: Ch14 §Sync Daemon Protocol does not currently describe attestation validation at the handshake; this section assumes it as a forward dependency. Confirm in Ch14 cross-reference and either back-add or flag as a gap to address with a parallel Ch14 update. -->

The honest limitation is the runtime-compromise gap. Attestation covers boot-time integrity. It does not cover runtime compromise — a device that boots cleanly and is then exploited mid-session is not caught by attestation alone. The residual risk is in-session compromise between attestation events. For high-security deployments, the architecture requires re-attestation at every relay reconnection, which narrows the gap to a single session's duration. It does not eliminate it; an in-session zero-click exploit between two reconnects remains an exposure.

### Sub-pattern 47d — Remote-wipe capability

When a device is confirmed lost or compromised, the operator needs to revoke that device's access and, where possible, crypto-shred the local copy of the data. Remote wipe is the operational procedure. The administrator issues a revocation broadcast for the device's node identity — the same mechanism as §Collaborator Revocation, applied to a device rather than a person — carrying a crypto-shred instruction. On receipt, the node overwrites its local key material and database encryption key with random bytes before exit.

The honest limitation is reachability. Remote wipe is only as reliable as the device's network reachability at the moment the broadcast fires. A device that is powered off, in airplane mode, or behind a network that blocks the relay cannot receive the wipe instruction until it reconnects. The architecture does not guarantee synchronous destruction — it guarantees destruction upon next reachable sync event, with audit-trail confirmation. An attacker who deliberately keeps the device offline defeats this control until reconnection occurs.

MDM (Mobile Device Management) integration is the parallel channel that closes the offline-device gap. Enterprise deployments using Intune, Jamf, or Google Workspace MDM issue an OS-level wipe order through MDM channels in parallel with the architecture's crypto-shred. The two mechanisms are complementary; MDM catches the case where the device never reconnects to the relay. `Sunfish.Kernel.Security` implements the local-side crypto-shred instruction. MDM integration is the deployment layer's responsibility — it is not part of the kernel-security package.

### Sub-pattern 47e — Endpoint-compromise containment

The blast radius of a compromised endpoint must be bounded. Three containment mechanisms enforce the FAILED conditions stated in §Sub-pattern 47a — that a compromised device cannot impersonate other devices, cannot backdate transactions, and cannot access other users' data on the relay.

**Per-device keypair isolation.** Each device in a user's fleet holds a distinct keypair. Compromise of one device's private key does not compromise other devices in the same fleet. The sync daemon rejects session tokens signed by a key it does not recognize, and the relay enforces keypair-session binding at every reconnection. An attacker holding a stolen session token from one device cannot pivot it onto another.

**Append-only transaction log.** The CRDT operation log is append-only and each entry is signed by the originating device keypair. Backdating requires a valid signature from the target timestamp's keypair — an attacker who compromises a device today cannot sign operations as if they occurred last week, because the historical keypair is not the one currently in the OS keychain. Forward-secrecy key rotation (§Forward Secrecy and Post-Compromise Security) further narrows the window during which any single compromised key can sign anything at all.

**Role-scoped access.** A compromised device can access only the data classes and roles it was provisioned to access. It cannot escalate to roles held by other users on the relay. The relay enforces role-level access at every session handshake (§Role Attestation Flow). The compromise stays inside the lane it started in.

### Sub-pattern 47f — Honest documentation of post-compromise risk

This sub-pattern is not a cryptographic mechanism. It is an architectural commitment to honesty. The chapter must state directly what protection lapses at endpoint compromise, not leave the reader to infer it.

The lapses, stated directly: local cached data is readable with the locally-held keys. Peers trust future writes from the compromised device until revocation propagates. A session in progress at compromise time exposes whatever plaintext is already in memory. Biometric authentication on the compromised device cannot be trusted, because the attacker controls the authentication flow.

The architecture does not claim to solve endpoint compromise. It claims four things: blast-radius containment via the three mechanisms in §47e; hardware-backed key protection where the platform offers it; a remote-wipe path that completes when the device is reachable; and honest documentation of the residual risk so practitioners plan against it rather than discover it in an incident post-mortem. Pegasus, Predator, and Hermit operate at the level of full OS compromise with zero-click delivery [26][27]. Against these, hardware enclave separation is the only control that reliably retains key protection. On a fully Pegasus-compromised device, keys in the OS keychain are accessible; keys in a hardware enclave are not. No software-only architecture can claim otherwise.

### FAILED conditions

The primitive's FAILED conditions:

- Compromised endpoint can impersonate other devices in the sync mesh.
- Compromised endpoint can backdate transactions in the shared log.
- Endpoint compromise scope is not documented in the deployed architecture's security reference.

Any FAILED condition confirmed at technical review escalates to `Sunfish.Kernel.Security` maintainers before the draft advances. This primitive has security-boundary implications; a confirmed failure is not a prose-pass defect.

---

## Chain-of-Custody for Multi-Party Transfers


<!-- code-check annotations: Sunfish.Kernel.Custody (NEW namespace, not in canon — forward-looking); Sunfish.Kernel.Audit (in-canon per cerebrum 2026-04-28, packages/kernel-audit/ exists). 0 class APIs / method signatures introduced. -->

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

The architecture integrates RFC 3161 trusted timestamping [28] for evidence-class transfers. The timestamp authority (TSA) is an external service — under EU deployments, a qualified trust service provider (QTSP) issuing qualified electronic time stamps to which eIDAS Article 41 [29] attaches the legal presumption of accuracy and integrity (the technical requirements for qualified time stamps live in Article 42); in other jurisdictions, an authority certified under the equivalent regulation.

On transfer-receipt creation, the transferor's node submits a TimeStampRequest containing a hash of the receipt event (SHA-256 by default) to the TSA. The TSA returns a TimeStampResponse: a signed time-stamp token whose `TSTInfo` structure binds the message imprint, the TSA identity, and the authority's certified time. The token persists alongside the receipt event in the audit log. Any node verifies the token's signature against the TSA's published certificate (per X.509 chain-of-trust [10]) and the message imprint against the receipt event. Backdating now requires compromising both the local log (blocked by DAG continuity) and the TSA (out of scope for a node-level attacker). <!-- design-decisions: §5 #9 + §8.2 — two-signature transfer receipt + RFC 3161 TSA anchoring is the architectural commitment surfaced at design-decisions §5 entry #9 ("multi-party signed transfer receipts, evidence-class temporal attestation"); §8.2 explicitly defers the formalization of multi-party signed transfer receipts to this writing task. -->

Not all deployments need external TSA anchoring. Consumer-tier deployments rely on the log's internal append-only semantics. Regulated deployments — those that produce evidence in legal proceedings, satisfy eIDAS AdES (Advanced Electronic Signature) requirements for evidence preservation, or comply with sector-specific record-keeping standards — declare a qualified TSA in their compliance posture. The deployment manifest records the TSA endpoint; `Sunfish.Kernel.Custody` invokes it on every evidence-class transfer event.

The architecture is local-first; a transfer that occurs while the node is offline cannot reach a TSA. The protocol queues the TimeStampRequest and submits it at the next relay-connected window. The receipt event records `tsa-pending` state until the token arrives. Nodes verifying the chain observe the pending flag and defer final evidence-class validation until the token is attached. An offline evidence-class transfer is not denied — its external timestamp anchor is deferred. The deployment's compliance posture documents the maximum acceptable pending duration before the gap escalates as a compliance event (see App B §Section 5).

### Sub-pattern 9c — Regulatory-export streaming with verifiable completeness

LADOT-MDS-style regulatory exports introduce a third variant. The mechanism is not a point-in-time bilateral receipt but a continuous signed stream emitted to a regulator with cryptographic proof that the stream is complete — no events were omitted, reordered, or modified between source and recipient.

A regulator receiving a data feed from a fleet operator must verify two things: that each individual event in the stream is authentic, and that the stream as a whole is complete. A tampered stream that omits unfavorable events while preserving the remainder is not detectable by verifying individual events in isolation. The stream must carry a running proof of completeness alongside its content.

The architecture addresses this with an append-only Merkle-tree commitment over the event stream, following the construction Crosby and Wallach formalized for tamper-evident logging [30] and standardized for the web PKI in Certificate Transparency [31]. As each event lands in the export log, the export pipeline folds its hash into a running Merkle root. The pipeline signs the root and emits it alongside each event batch. The regulator verifies that the received stream matches the committed root and that the root chain is internally consistent — each new root extends the prior one by exactly the new events, with no gaps. Any omission or reordering breaks the Merkle chain, and the regulator detects the gap without requiring any cooperation from the operator.

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

---

## Event-Triggered Re-classification


<!-- code-check annotations: Sunfish.Kernel.Security (in-canon, extends existing); Sunfish.Kernel.Audit (in-canon per cerebrum 2026-04-28); Sunfish.Kernel.SchemaRegistry (in-canon); Sunfish.Kernel.Sync (in-canon, propagates re-classification operation via gossip). 0 new top-level namespaces. 0 class APIs / method signatures introduced. -->

A commercial driver finishes a delivery shift. The dashcam footage from that route lands in the fleet's local-first store under the routine `operational` class — 30-day rolling retention, dispatcher-role envelope, no signed-export pipeline. Three days later, an insurer phones: a vehicle from that route was named in a third-party collision claim. The footage is now evidence. Its retention must extend, its access must tighten, and its export must carry the chain-of-custody primitive specified in §Chain-of-Custody for Multi-Party Transfers. None of that was true when the record was written; all of it must be true now — and replicas already sit on the driver's tablet, the dispatch desktop, and a back-office relay cache that may be offline until tomorrow morning. Schema-time classification cannot handle this. The architecture treats data-class escalation as a first-class operation on the CRDT log, governed by a CRDT-native invariant and propagated through the same gossip path that carries every other operation.

### Sub-pattern 10a — Re-classification operation and the max-register CRDT invariant

Re-classification is an operation, not a state mutation. The classification service does not overwrite a `class` field. It appends a new operation carrying four fields: the record identifier, the new class level, the trigger event identifier, and the signature of the asserting authority — operator, compliance system, or designated user role. The record's content does not change. Its envelope acquires a new assertion.

The CRDT invariant governing class level is the **max-register**. The class label of a record at any node is `max(L₁, L₂, ..., Lₙ)` taken over every re-classification operation that has reached the node. Max is associative, commutative, and idempotent — the three properties a strict semilattice requires for monotonic convergence. Two nodes that receive the same operations in different orders converge to the same label; a replayed operation does not change the resulting class. The mechanism aligns with the high-watermark principle NIST SP 800-60 prescribes for aggregated systems [37][38] and the periodic-review obligation ISO/IEC 27001:2022 Annex A 5.12 places on classified information [39].

The invariant has a sharp edge. **An operation `(record_id, lower_class)` is rejected at every replica.** Re-classification is monotonic upward; a record at Class 3 cannot be returned to Class 2 by any authority. A downward move would re-grant access already cut off; if a deployment determines an escalation was issued in error, the corrective path is deletion-and-recreation at the lower class with a fresh record identifier. The trigger event identifier is the load-bearing field for accountability — every operation names its cause (an incident-flag, a legal-hold directive, a regulator notice, an inferred-special-category trigger fired when a content scanner detects a GDPR Article 9 attribute [40]) and resolves to a record in `Sunfish.Kernel.Audit`.

**Principal novelty.** Microsoft Purview sensitivity labels [41], AWS Macie, and Google Cloud DLP perform classification and re-classification as centralized, online operations against a canonical store. None applies a max-register CRDT invariant to a security metadata field with access-control re-evaluation as a delivery-side effect. Those systems are the appropriate point of contrast, not the model. The contribution is convergent re-classification under partial replication without duplicating storage and without breaking the immutable audit trail.

### Sub-pattern 10b — Backward propagation across replicated copies

A re-classification operation propagates through the gossip path the sync daemon uses for every operation in `Sunfish.Kernel.Sync`. The mechanism is structurally identical to the revocation broadcast specified in §Collaborator Revocation and Post-Departure Partition. Where revocation broadcasts "this collaborator's KEK share is revoked," re-classification broadcasts "this record's class level has changed, and the new class's access policy applies retroactively." Transport identical; asserted fact different.

What distinguishes re-classification from an ordinary edit is the receiving node's behavior on delivery. The sync daemon hands the operation to `Sunfish.Kernel.Security` for immediate access-control re-evaluation — not on the next refresh cycle, not at the next session handshake, but inline before any pending read or write on the affected record reaches the application layer. Roles that held access at the prior class but lack access at the new class see their next attempted read denied with a `class-escalated` reason code.

Offline-node handling is the case the architecture has to get right. A node offline when the escalation fired holds a previously-lower-class copy. On reconnect, it receives the operation as part of its anti-entropy exchange, and the sync daemon processes the re-classification before delivering any pending reads or writes the application queued during the offline window. The local cached copy is not erased — the architecture does not delete data from offline replicas, the same commitment §Collaborator Revocation makes for revoked collaborators. Forward access at the prior class is cut off; previously-delivered reads are not retrieved. The UX consequence of this forward-only invalidation is specified in Ch20 §Data-Class Escalation UX.

### Sub-pattern 10c — Audit-trail handling under class change

The record's operation history was written under the prior class. Truncating it to hide pre-escalation state is out of scope — it would break the CRDT's append-only invariant. The historical operations remain in the log; the access policy that governs their retrieval changes. A role authorized at Class 1 was authorized to read history at Class 1; after escalation to Class 3, that role is not authorized to read the history unless it also holds access at Class 3. Cached copies a node held before escalation remain locally readable on that node — see §Collaborator Revocation sub-pattern 45c for the cached-copy framework — but no further history can be pulled from peers under the prior credential. The escalation event itself produces a record in `Sunfish.Kernel.Audit` carrying the record identifier, prior and new class levels, trigger identifier, asserting authority, and UTC timestamp; the audit record's own class is the **new** class.

### Sub-pattern 10d — Cross-class references and operator review

A low-class record holding a reference to a high-class record carries an implicit class obligation. The reference does not reveal content, but it proves a relationship exists — in a legal-hold context, a routine note referencing an incident report's identifier may disclose the existence of the investigation. When a record escalates, `Sunfish.Kernel.Security` queries the reference index maintained by `Sunfish.Kernel.SchemaRegistry` for every record holding an inbound reference to the escalated identifier. The audit trail flags those records for operator review; they are **not** auto-escalated, because auto-lifting would cascade unbounded. The operator either confirms referencing records remain at their original class or issues a separate re-classification operation, which propagates through 10b as a first-class escalation. The review surface is specified in Ch20 §Data-Class Escalation UX.

### Sub-pattern 10e — Schema-evolution non-interaction

Class level is a metadata field on the record's envelope, not a schema field on its payload. Re-classification does not change payload shape, does not require a lens, and does not advance the schema version; the migration engine is not invoked. Per-class field-access rules — fields permitted at Class 1 that must be redacted at Class 3 — are enforced at read time by `Sunfish.Kernel.Security`, not by the schema migration engine. Schema migration mutates payload shape; access enforcement filters payload content for delivery.

### Composition forward

A record escalated under §10a that later becomes subject to a deletion request follows §GDPR Article 17 and Crypto-Shredding at the new class level — the DEK destroyed is the new class's DEK. Composition with §Forward Secrecy and Post-Compromise Security is clean. The forward-secrecy ratchet (sub-pattern 46a–46b) operates per-session-pair on sync-event transport; re-classification is an event on the record's envelope, and the two layers do not interact. Envelope-only re-keying — re-wrapping the existing DEK under the new class's KEK — is sufficient for every class transition. The DEK itself does not change; the ratchet does not advance on a re-classification operation any differently than on any other operation; full content re-encryption is not required. Composition with §Chain-of-Custody for Multi-Party Transfers is equally clean. A transfer receipt binds a specific `(object-id, version-vector, transferor-signature, recipient-signature)` tuple at a specific moment. Subsequent escalation does not retroactively modify any field of the prior receipt — it produces a successor event in the audit log. The receipt's class field names the class at time of transfer and remains accurate as a historical fact; it is not made stale by escalation, because the receipt's claim is point-in-time, not perpetual.

### FAILED conditions

- **A re-classification operation lowers a record's class level.** Architecture failure. Max-register monotonicity is the foundation of convergence and access-control correctness.
- **An offline node delivers reads from a cached prior-class copy after receiving the re-classification operation on reconnect.** Architecture failure. Forward access at the prior class must be cut off inline at delivery.
- **A cross-class reference cascade auto-escalates referencing records without operator review.** Architecture failure. The §10d gate exists precisely to bound the propagation surface.
- **The escalation event is not recorded in `Sunfish.Kernel.Audit` at the new class level.** Compliance failure.

The kill trigger for this primitive is a re-classification operation that converges to a lower class than its highest received argument at any replica. A primitive that does not preserve max-register monotonicity is not data-class re-classification — it is mutable-state pretending to converge.

---

## References

<!-- Phase 3 placeholder: Ch22's share of the Ch15 reference list (~470 words). Citations split per-section between Ch15 (architecture share) and Ch22 (operations share); Ch22 keeps cites referenced from O sections. Per UPF Phase 1 triage: Shamir [6] (key-loss recovery), Buterin [4] (social recovery), Argent [5] (multi-sig wallet patterns), Sigstore [2] (supply chain — though cross-referenced from Ch15), the SGX/TEE family [22]–[24] (endpoint compromise), Pegasus + Hermit [26]–[27] (endpoint compromise), TSP RFC 3161 [28] (chain-of-custody timestamp), and the DP family [32]–[36] if Privacy-Aggregation is reclassified to O in a later round (currently A per Phase 1 triage footnote ¹). Final assignment confirmed during Phase 5 cross-reference work. -->
