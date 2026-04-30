# Chapter 22 — Key Lifecycle Operations

<!-- icm/draft -->

<!-- Target: ~6,000 words (post-prune; UPF Ch15 split kill-trigger fired 2026-04-30; Ch22 split into Ch22 Key Lifecycle Ops + Ch23 Endpoint + Collaborator Ops). -->
<!-- Source: post-Ch15-split + post-Ch22-Ch23 split per UPF FAILED-condition. This chapter retains the lifecycle-of-keys operational flows (compromise response, loss recovery, forward secrecy ratcheting). Endpoint, collaborator, custody, and event-triggered class-escalation operations live in Chapter 23. -->

<!-- code-check: namespaces inherited from Ch15. Sunfish.Kernel.Security, Sunfish.Kernel.Sync, Sunfish.Kernel.Audit (forward-looking from #48), Sunfish.Foundation.Recovery (forward-looking from #48). Per-section code-check annotations carried with their sections. -->

---

Chapter 15 specifies the security architecture. This chapter specifies what to do when a key changes lifecycle state — compromised, lost, or stale enough that forward secrecy must engage. Each section is a self-contained operational flow.

Endpoint compromise, collaborator revocation, multi-party chain-of-custody, and event-triggered re-classification — operational flows that run when state changes *around* the keys rather than within their lifecycle — live in Chapter 23.

---

## Key Compromise Incident Response


Scheduled key rotation is a maintenance operation. Key compromise is an incident. The response procedure differs from routine rotation in one critical way: the new KEK must not derive from the compromised key.

**Detection triggers.** The system logs all key access events to the audit log. Detection arrives from three sources: a physical loss report from a user whose device was stolen or found in an untrusted state; anomalous access patterns in the audit log that suggest unauthorized key use; or an explicit administrator report of suspected credential exposure. The incident response procedure activates on any of these triggers.

**New KEK generation.** The administrator generates an entirely new KEK for the affected role from a fresh entropy source. Derivation from the compromised key would propagate the compromise forward. All other aspects of the distribution flow — wrapping with member public keys, publishing as signed administrative events — are identical to routine rotation.

**DEK re-wrapping.** The system re-wraps every DEK owned by the affected role using the new KEK. The background job processes DEK blobs only, leaving document bodies unchanged. During re-wrapping, documents remain accessible to nodes that hold the current KEK. The old KEK is not discarded until all DEKs in scope are re-wrapped and new bundles are delivered to all authorized nodes.

**Old KEK discard.** Once DEK re-wrapping completes and new bundles are delivered, the administrator triggers discard of the old KEK. `Sunfish.Kernel.Security` broadcasts a discard signal through the relay; each node zeros its in-memory copy of the old KEK and removes it from the OS keystore. A node that received the discard signal but has not yet received the new bundle cannot decrypt documents in that role — and that is the correct behavior. Partial access is not granted as a fallback.

**Revocation broadcast.** The relay receives a revocation event for the compromised key identifier. Subsequent connection attempts from any node presenting the revoked key are rejected at the handshake layer with a specific error code.

**User notification.** Affected users receive a notification specifying the data-at-risk window: the interval from the compromised key's creation date to the moment the revocation broadcast was confirmed. The notification is specific — "documents in the Finance role between January 3 and April 17 may have been accessed" — not a generic security alert.

---

## Key-Loss Recovery


<!-- code-check: package references in this section include `Sunfish.Foundation.Recovery` (forward-looking — Volume 1 extension roadmap, not yet present in the Sunfish reference implementation; illustrative in the same sense the book's other pre-1.0 Sunfish references are illustrative). The other two references, `Sunfish.Kernel.Security` and `Sunfish.Kernel.Audit`, are in the current Sunfish package canon (verified 2026-04-28: packages/kernel-audit/ exists). -->

My mother called me in the summer of 2023 from my Aunt Vickie's house. Uncle Charlie had died — twenty-three years a Michigan conservation officer, and in his off-hours a hobby photographer who had earned a modest income selling his work online. There was the funeral. There was an iPhone, locked. It had been part of Charlie's daily life and potentially the channel through which his photographs reached buyers. None of us knew exactly what was on it. My aunt was sitting next to my mother, the iPhone on the table between them, and the question my mother was calling to ask, because I work in software, was whether there was a way to recover an iPhone.

I knew the answer before she finished. The honest version is: not really. There is a court order. There is Apple's deceased-relative process. There is a queue, a verification cycle, a chance the data comes back and a chance it doesn't — a probability distribution, not a recovery primitive, and not what my aunt was asking for with the device sitting in front of her.

I told her what I knew. She said okay. We talked about other things. The well-meaning Genius Bar staff were eventually able to help, and the photographs are now in my aunt's possession — a probability that resolved favorably, on a timeline outside our control, through the discretion of strangers acting in good faith. The next family in the same posture has no architectural reason to expect the same.

The architecture of this chapter is built for people like Charlie who just use technology on a daily basis, and for those who survive them. It is also built for the moment he never got to have, and for the call I did not have a better answer to.

Incident response handles the case where an attacker compromises a key. Key-loss recovery handles the case where the legitimate user loses one. The two scenarios look superficially similar — both require generating new keys and distributing them — but they differ in one critical way: in the compromise case, the user is present and the attacker is the unknown party; in the loss case, the user is the unknown party and the system must verify them before granting access.

Recovery is one of the few subjects in this book that splits cleanly into a policy chapter and a UX chapter — the two are paired by design. This section specifies what the architecture commits to. Ch20 §Key-Loss Recovery UX specifies what the user sees when those commitments engage. Each sub-section here has a counterpart there; readers who skim one without the other miss the point of either.

### Why this matters

The P7 ownership property — that users hold the keys to their own data — is not a defect-free guarantee. It is an honest trade. Users who retain their keys retain full control. Users who lose their keys lose their data. That boundary is the architecture's honest edge.

Real-world key loss arrives through five distinct failure modes. A master password is forgotten; a device is lost or stolen with no cloud backup in place; an OS factory reset wipes the keystore without a prior export; a hardware security token is physically destroyed or stolen; or a user dies or becomes incapacitated without a succession arrangement. Each of these converts the architecture's confidentiality guarantee into permanent data loss unless a recovery primitive is in place before the event.

A recovery primitive introduces a new attack surface. Any path that allows a legitimate user to recover access is a path an adversary can attempt to exploit. The design space is narrow: the primitive must be at least as hard for an adversary to traverse as the original custody chain was to compromise, and it must impose enough friction that a patient attacker is deterred by cost rather than by any single gate. The six mechanisms below occupy different positions in that design space. No single mechanism is universally correct. Deployment class, threat model, and the user population's tolerance for recovery friction all determine the right combination.

Recovery is the runtime mechanism for two upstream policies: succession arrangements with executor delegation (described in a future volume) and delegated capability grants. Those policies determine who is authorized to invoke recovery and under what conditions; the six mechanisms described later in this section implement the authorization cryptographically.

### Recommended Deployment Combinations

Pick the deployment class first; the rest of the section describes the mechanisms it composes. Consumer deployments optimize for a successful recovery the user will actually complete when needed; excessive friction means users skip setup and have no recovery path. Regulated deployments optimize for auditability and resistance to coercive attacks; the longer grace period reflects both regulatory dispute requirements and the higher likelihood that a regulatory-tier adversary has greater patience and resources.

| Deployment class | Primary mechanism | Secondary mechanism | Grace period |
|---|---|---|---|
| Consumer | Multi-sig social (3-of-5) | Paper-key offline | 14 days |
| SMB | Custodian-held + 2-of-3 social | Paper-key in safe | 7 days |
| Regulated (HIPAA, PCI, financial) | Custodian-held under attestation | Multi-sig social with named officers | 30 days |

The deployment class is declared at first-run and persists in the team's signed configuration manifest. `Sunfish.Foundation.Recovery` reads the class on initialization and binds the corresponding threshold and grace-period values; the manifest entry is itself a signed event in the audit log, so a class change is an audited operation that any node can verify.

**Consumer.** Three-of-five social recovery tolerates losing contact with two trustees and is straightforward to explain: "Pick five people you trust. Any three of them together can help you get your data back." The paper-key secondary fallback covers the scenario where trustees are unavailable for an extended period — a family emergency, a natural disaster, a death without notice. The 14-day grace period is long enough to give the original holder time to notice and dispute, short enough not to strand a user who genuinely lost access and needs timely recovery. `Sunfish.Foundation.Recovery` defaults to this configuration for consumer profiles.

**SMB.** Small and medium businesses typically have a legal relationship with a lawyer or accountant who can serve as institutional custodian. Combining that relationship with 2-of-3 social recovery across named officers — the owner, the operations manager, a designated deputy — provides both institutional accountability and a personal recovery path. The paper-key in a physical safe protects against simultaneous loss of all digital channels. The shorter 7-day grace period reflects the business continuity pressure that enterprise deployments typically face; a 30-day pause on a production account is not acceptable in most SMB contexts.

**Regulated.** HIPAA-covered entities, PCI-DSS merchants, and financial services firms face audit requirements that demand a documented, verifiable recovery path. The custodian-held mechanism under an attestation policy produces the audit artifact; the 30-day grace period satisfies the dispute and review timelines that regulated industries typically require. Multi-sig social recovery with named officers — named in the attestation policy — provides a secondary path where the custodian relationship fails. Every recovery event appears in the audit log maintained by `Sunfish.Kernel.Audit`; the log is the compliance artifact.

The consumer combination composes sub-patterns 48a (multi-sig social) and 48c (paper-key); the SMB combination composes 48b (custodian) with 48a; the regulated combination composes 48b with 48a, layered under sub-pattern 48e (timed grace period) tuned to the audit window. The next subsection describes each sub-pattern in turn.

### The six recovery mechanisms

#### Multi-sig social recovery

Multi-sig social recovery — sub-pattern 48a — distributes the recovery authority across a set of trusted individuals the user designates before any loss occurs. The construction derives from Shamir secret sharing [6]: the user's root recovery key is split into *n* shares, each share held by a separate trustee, and any *t* of the *n* shares suffices to reconstruct the key. Each trustee holds a share, not the full key; no single trustee can unilaterally reconstruct the recovery key or access the user's data.

A threshold of 3-of-5 tolerates the simultaneous unavailability of two trustees; a threshold of 2-of-3 is appropriate for smaller trust networks. The Argent smart wallet specification [5] and Vitalik Buterin's 2021 case for social recovery wallets [4] establish the pattern's practical architecture.

The dealer protocol matters as much as the threshold. The user's device runs the Shamir dealer locally over GF(2^256), seeded by the OS CSRNG, and produces *n* shares from the recovery key. Each share is wrapped under the trustee's enrolled public key before it leaves the device — shares never traverse the network or the relay in plaintext. After the dealer emits all shares, the device zeros the dealer's working state and the in-memory copy of the recovery key. The protocol is local-first: no third party — including the relay — ever sees the unwrapped shares.

<!-- technical-review: CSRNG output is uniformly distributed over GF(2^256) under standard cryptographic assumptions for getrandom(2) on Linux, BCryptGenRandom on Windows, and SecRandomCopyBytes on macOS — the OS CSRNGs cited in §Key Hierarchy. -->


Trustee designation happens at first-run, not after loss. A user who has not designated trustees before losing their key has no social recovery path. The time-lock period — default seven days — opens a dispute window: if the original holder's devices or trustees receive the recovery claim and the original holder is actually present, they can dispute and halt the process. The time-lock is not a network artifact; it is deliberate friction.

The threat model is collusion. If *t* trustees coordinate — or are simultaneously compromised by the same adversary — the recovery key is reconstructable without the original holder. Geographic and social diversity in trustee selection reduces collusion risk. Multi-sig social recovery is the correct mechanism for individuals and small partnerships. It is not the correct mechanism for enterprise deployments where the trust network cannot be meaningfully diversified.

Social-recovery legal status varies by jurisdiction. Trustee residency may itself trigger data-residency obligations under the DPDP Act (India), PIPL (China), DIFC DPL 2020 (Dubai International Financial Centre) and the parallel ADGM Data Protection Regulations 2021 (Abu Dhabi Global Market), Russia's Federal Law 242-FZ, and POPIA Section 72 (South Africa) cross-border transfer requirements. Deployments subject to localization requirements name their trustees in-jurisdiction or document an exception in the team's compliance posture (see Appendix F). For EU-resident users with trustees outside the EU/EEA, the share transfer is itself a data transfer under GDPR Chapter V — deployments name a Chapter V transfer mechanism (Standard Contractual Clauses, an adequacy decision, or binding corporate rules) before designating an out-of-region trustee. The cryptographic construction is sound everywhere; the legal classification of the trustees' role is not.

The deployment cost is low: trustee designation is a setup flow in `Sunfish.Foundation.Recovery`. The ongoing cost is maintaining accurate trustee contact information as relationships change.

#### Custodian-held backup key

Sub-pattern 48b delegates recovery authority to an institutional custodian: a law firm, a bank's custody division, a regulated cloud-custodian operating under an audited security posture, or a regulated institutional intermediary serving in a trust capacity (a system integrator under contract, a trust bank, a regulated escrow service — the institutional category that fills the role varies by region and industry). The architecture wraps the user's or organization's root recovery key and transfers the wrapped copy to the custodian under an attestation policy that specifies the conditions for release.

Release requires multi-factor identity verification through the custodian's out-of-band channel — in-person identity documents, video call, notarized request, or whatever the custodian's policy mandates. The custodian does not hold the key in plaintext; they hold a wrapped copy that `Sunfish.Foundation.Recovery` unwraps on the user's device after the custodian releases it. The custodian's channel is the verification gate; the cryptographic unwrapping happens locally.

The threat model is custodian compromise or coercion. An adversary who compromises the custodian's systems, or who legally compels the custodian to release the wrapped key, gains the wrapped blob. The wrapping itself provides no defense against coercion once the release conditions are met. The mitigation is the custodian's own audited security posture, the legal liability allocation in the custody contract, and the out-of-band identity verification that an adversary must also defeat.

The custody contract allocates liability for release errors in one of three postures. Posture (a) is custodian-disclaims-all: the custodian carries no liability for releases that turn out to be unauthorized. This is the most common contract for low-fee consumer custodianship and is weakly defensible against the user's loss; informed users avoid it. Posture (b) is bounded-cap liability: the custodian is liable for release errors up to a contractual cap, typical of regulated financial-services and trust-company custody. Posture (c) is joint liability with the architecture vendor: rare, expensive, and reserved for high-value institutional deployments where the vendor and custodian both carry insurance against release error. Regulated-industry deployments — HIPAA, PCI-DSS, financial services — typically require posture (b) at minimum; deployments accepting posture (a) for cost reasons document the trade-off in the team's compliance posture (see Appendix F).

Custodian-held backup key is the correct mechanism for enterprise deployments, regulated industries, and succession arrangements where executor delegation requires institutional involvement (cross-reference #32). Relying on a single custodian is itself a single point of failure for recovery: when the custodian is operational but the verification flow stalls for a specific user — identity dispute, custodian-side outage, staffing gap — recovery halts indefinitely. A secondary mechanism (paper-key, social) is the operational mitigation. The deployment cost reflects the custodian relationship: contract negotiation, enrollment, and annual audit. The ongoing cost is custodian fee and key refresh on rotation cycles.

#### Paper-key fallback

Sub-pattern 48c generates a BIP-39-style mnemonic phrase at first-run, prints it, and relies on the user to store it offline in a physically secure location. The phrase derives the root recovery seed through Argon2id (see §Key Hierarchy for the regulated-tier parameters: memory cost 128 MiB, iteration count 4, parallelism 4). The physical security perimeter — safe, safety-deposit box, fireproof lockbox — is the user's responsibility and the architecture's honest boundary.

Paper-key fallback is the simplest recovery mechanism to understand and the most forgiving in terms of threat model: no trustee can be compromised, no custodian can be coerced, no online account can be phished. The threat model shifts entirely to physical access. An adversary who obtains the printed phrase obtains the recovery key. The architecture provides no defense against that physical compromise.

Paper keys defeat cold-boot and hibernation attacks during an offline key-recovery operation because the recovery process does not require a running device with key material in memory. They are best suited to low-frequency recovery scenarios, single-user accounts, and deployments where every online escrow path is itself a higher risk than physical paper — a security researcher, a journalist working under hostile conditions, an individual deploying in a jurisdiction where digital custody creates legal exposure. Paper-key fallback is not a substitute for a primary recovery mechanism in multi-user environments. It is a secondary fallback.

#### Biometric-derived secondary key

Sub-pattern 48d derives a recovery key from a biometric template held in the device's hardware secure enclave — Apple Secure Enclave, Pixel Titan M, or Windows Pluton, as documented at the time of writing. The biometric template never leaves the enclave; the enclave derives a keying material value only on a positive biometric match and passes that value to `Sunfish.Kernel.Security` for the recovery unwrap operation. The biometric itself is never extracted, transmitted, or stored outside the hardware boundary.

<!-- technical-review: template non-exportability verified. Apple Secure Enclave: documented in Apple Platform Security [7] — the Secure Enclave processes biometric data and outputs match results and derived keys; raw templates are never exposed to the application processor. Pixel Titan M: consistent with Google's Titan M security architecture documentation — biometric matching executes in the secure environment; derived keys, not templates, cross the trust boundary. Windows Pluton: Windows Hello biometric templates reside in the Windows Hello container backed by the TPM or Pluton processor; template extraction is not available through any documented software API. All three platforms conform to the architectural claim. -->

The threat model includes coerced biometric presentation — the user asleep or physically compelled — and, for some sensor implementations, template extraction through hardware attacks. Biometric-derived secondary keys are not the default recovery mechanism in regulated-tier deployments. They are an appropriate secondary factor when combined with another mechanism — the combination of biometric plus paper-key plus grace period means no single coerced action completes recovery alone.

Biometric recovery is opt-in at the deployment level. Consumer deployments may enable it as a convenience secondary factor. Regulated deployments should not rely on it as a primary mechanism given the coercion exposure.

#### Timed recovery with grace period

Sub-pattern 48e is a composable layer, not a standalone mechanism. Any of the mechanisms above can be combined with a time-locked grace period, and every production deployment should combine them. The construction is simple: when the user submits a recovery claim, the system broadcasts it to the original holder's existing devices and to designated trustees. The original holder has a configurable window — seven to thirty days, depending on deployment class — to dispute the claim. If the holder disputes, recovery halts. If the grace period elapses without dispute, recovery completes and the new key takes effect.

The grace period is deliberate friction, not a network propagation delay. An adversary who can submit a recovery claim and also suppress the original holder's notifications for fourteen days has a substantially harder problem than an adversary who can complete recovery in seconds. The attacker who controls the recovery initiation path still must also control every notification channel simultaneously, for the duration of the grace period, without the holder noticing.

The threat model for the grace period mechanism specifically is a long-game adversary with persistent access to all of the original holder's notification channels — email, SMS, in-app, push. That threat model is not common and not low-cost. The mitigation against it is multi-channel notification (not only email, not only SMS) and trustee co-signing on completion, so the holder has additional channels through which a dispute can be registered.

`Sunfish.Foundation.Recovery` emits recovery-claim events and manages the grace-period state machine. The grace period is not a client-side timer; it is an event in the signed audit log, which means it is tamper-evident and observable by any node that validates the log.

#### Recovery-event audit trail

Sub-pattern 48f is the logging substrate on which all other mechanisms depend. Every recovery initiation, trustee response, dispute, and completion is a signed event in the same encrypted log used for application data. `Sunfish.Kernel.Audit` manages recovery-event records. Each record carries the recovery mechanism type, the trustee identifiers (where applicable), the claimed identity, the grace-period boundaries, and the completion or dispute attestation.

The audit trail is the legal artifact when a recovery is later contested. It is the architectural defense against silent recovery: a recovery that completes without a corresponding event in the log cannot be legitimate, and any node verifying the log detects the gap. The trail composes with §Chain-of-Custody for Multi-Party Transfers — the same multi-party signed-event structure, applied to recovery operations rather than data transfers.

Recovery audit records are retained by default for the deployment's regulatory retention period. Crypto-shredding the data subject's content stub on an Article 17 erasure request is technically possible; whether the surrounding trustee, custodian, and timing metadata is also erasable is jurisdiction-specific and intersects third-party rights. Trustees and custodians named in a recovery record retain a legitimate evidentiary interest in their participation being preserved against contested claims. Default behavior is to preserve the metadata pending a written legal determination; case-specific erasure follows counsel review (see §GDPR Article 17 and Crypto-Shredding).

### Recovery State-Machine Convergence

Recovery is a concurrent state machine across multiple signing parties on a partitionable transport. The original holder's devices, designated trustees, and the custodian (where present) all sign events into the same encrypted log; events propagate through the relay or directly between peers as the network allows. During a partition, two events may be filed concurrently against the same recovery claim — a dispute from the original holder's existing device and a completion event, whether the completion is a trustee-threshold attestation (sub-pattern 48a) or a single signed custodian-release event (sub-pattern 48b). The convergence rule binds both completion paths identically.

The convergence rule has two distinct layers. **Global log semantics:** no node accepts a completion event for a recovery claim against which a signed dispute event already exists in its log; the completion is rejected at validation, the recovery state resets, and re-initiation is required. The rule applies identically to trustee-threshold completions (sub-pattern 48a) and single-signed custodian-release events (sub-pattern 48b) — both are completion events under the same convergence policy. **Local node behavior:** a node that applied a completion before seeing a not-yet-propagated dispute event reverses the completion on dispute arrival during sync. The new key is in effect locally for the partition window between completion application and dispute arrival; after reversal, the node returns to the pre-completion state and the recovery requires re-initiation. The window is a real architectural fact — security-sensitive deployments size the grace period to make this window negligible compared to the time required for the original holder to detect and dispute.

The rule is asymmetric by design. The original holder's authority to halt outweighs the trustees' or custodian's authority to complete, because the cost of an erroneously-completed recovery is permanent loss of the original holder's data control while the cost of a halted-and-re-initiated recovery is operational delay. `Sunfish.Foundation.Recovery` enforces this convergence at the audit-log validation layer; the local-reversal behavior is a sync-layer consequence of the partition tolerance the architecture commits to elsewhere.

### Threat Model — Recovery as Attack Vector

Recovery primitives are attack surfaces. The cardinal rule: the aggregate difficulty of traversing the recovery path must be at least as high as the aggregate difficulty of compromising the original custody chain. Recovery that is easier to invoke than the original access was to obtain breaks confidentiality by another route.

Four specific attack patterns define the threat model for recovery operations.

**Trustee compromise.** An adversary compromises one or more trustees to reconstruct the Shamir secret-sharing threshold. The t-of-n threshold means a single trustee compromise yields nothing; the adversary must compromise *t* trustees simultaneously or in a coordinated window shorter than the grace period. Grace-period notification to the original holder provides a dispute opportunity even if *t*-minus-one trustees are compromised. Recovery fails when *t* trustees are simultaneously compromised. The architecture cannot defend against this outcome; it can only require that *t* is chosen large enough that simultaneous compromise is costly.

**Custodian coercion.** An adversary coerces the institutional custodian through legal process, extortion, or infiltration. The custodian's release conditions are the gate; once those conditions are met, the architecture provides no further defense. The mitigation is custodian selection, contract structure, and out-of-band identity verification that the adversary must also satisfy.

**Forged loss claim.** An adversary submits a recovery claim without actually holding the account. The grace period and multi-channel notification give the original holder a dispute window. Trustee co-signing on completion requires the adversary to also compromise the trustees. Signed audit trail entries log the claim identity and allow post-hoc forensics.

**Coerced recovery.** An adversary physically coerces the user to complete the recovery flow themselves. No cryptographic mechanism defeats physical coercion. The architectural mitigation is to ensure that no single coerced action completes the recovery flow: biometric plus paper-key plus grace period means the adversary must coerce the user into initiating, coerce each trustee into signing, and suppress notifications for the full grace period. That combination raises the cost of coercion substantially. It does not eliminate it.

Honest limitation: no recovery primitive defeats a sufficiently patient adversary with simultaneous control of every recovery channel. The architecture bounds the attack cost. It does not bound it to infinity.

### Boundaries and Operator Mitigations

Six failure modes sit outside the cryptographic guarantees of the mechanisms above. The architecture acknowledges each, prescribes operator mitigations where they exist, and documents what remains the user's responsibility.

A user who skips recovery setup at first-run and then loses their key loses their data. The architecture presents the choice and documents the consequence. It cannot force the choice. `Sunfish.Foundation.Recovery` surfaces an explicit acknowledgment prompt for users who decline setup; the acknowledgment is logged. The log records that the user declined, not that the architecture failed.

A user who designates trustees who are themselves all compromised — or who designates trustees who predecease them or become unreachable — has no social recovery path from that posture. The architecture cannot grade trustee selection or predict trustee availability over time. Periodic recovery-readiness audits (described in Ch20 §Key-Loss Recovery UX) surface the risk; the user must act on the reminder. Silent decay is a real operational failure mode: a 12-month audit cadence is too coarse to catch a trustee who changed contact details ten months ago, so deployments raise the bar with a quarterly liveness ping per trustee. The trustee's app responds to a tiny challenge; when the active trustee count falls below threshold + 1, the application surfaces a degraded-arrangement banner. The trustee-side cost is one challenge per quarter per user they serve as trustee — manageable at typical trustee-network sizes, worth budgeting against when an individual ends up named as trustee for many users at once. This converts silent decay into an observed event without flooding either party with alerts.

A user whose designated trustees act in bad faith — coordinated coercion in a family or business dispute, or a hostile inheritance claim — has limited defense beyond the grace-period dispute window. Selection of trustees with no shared interest in the user's data is the user's responsibility; the architecture cannot grade trustee motivations. The grace period helps when the user is reachable through their notification channels and detects the unauthorized claim; it does not help a user who is travelling, hospitalized, or otherwise out of contact for the duration of the window.

A user whose complete recovery arrangement becomes invalid before loss occurs — paper key destroyed in the same disaster that destroyed the device, custodian out of business, all trustees deceased — has no recovery path. The architecture cannot prevent a pre-arrangement from decaying. The mitigation is the same periodic readiness audit. An arrangement that has not been verified in 12 months may no longer be valid. The audit is the check. Nothing in the architecture substitutes for that check.

A user whose paper key is illegible at recovery time — water damage, faded ink, transcription error at first-run, prolonged storage degradation — has no recovery from that mechanism alone. The architectural mitigation is round-trip transcription verification at setup time and a recommended secondary mechanism. Ch20 §Key-Loss Recovery UX describes the setup-time verification flow; the deployment-class table above describes the secondary-mechanism recommendation per class.

A jurisdiction with mandatory key-escrow requirements supersedes the user-held recovery model entirely. Where such requirements apply — they are not currently in force in most jurisdictions named in Appendix F, but several CIS and ECOWAS policy discussions are active — the deployment substitutes an escrow-compliant custodian arrangement for the recovery-key custody chain, with separate compliance review. The architecture cannot honor user-held recovery and government-mandated escrow simultaneously; the deployment chooses one and documents the choice in the team's compliance posture.

### Implementation Surfaces

The recovery primitive is observable through five named contracts that any conforming implementation surfaces in its event taxonomy. The list is illustrative — the concrete event schema lands when `Sunfish.Foundation.Recovery` reaches its first milestone; the contracts themselves are stable across implementations.

- `RecoveryClaimSubmitted` — the user or a delegate has submitted a recovery claim; carries the claim identity, the mechanism type, and the grace-period boundary.
- `GracePeriodObserver` — emits ticks during the grace period and the terminal expiry event; nodes subscribe to drive the UX progress display. Tick frequency is implementation-defined and UX-driven — subscribers pull at the cadence their progress display requires (typically once per minute for in-app banners, once per hour for OS push notifications). Push delivery of the terminal expiry event is supported alongside pull; the recommended minimum poll interval for the intermediate ticks is one minute, to avoid log-validation thrash.
- `TrusteeAttestation` — a designated trustee has signed their share or co-signed a completion; carries the trustee identifier and the attestation type.
- `RecoveryDispute` — the original holder's device or a co-signing trustee has filed a dispute; carries the dispute reason and triggers the convergence halt described above.
- `RecoveryCompleted` — the threshold is met, the grace period has elapsed without dispute, and the new key is live.

Nodes wishing to integrate recovery flows subscribe to the relevant contracts through `Sunfish.Kernel.Audit`. The audit-log validation layer enforces the convergence rules before any UX layer observes the events.

---

## Forward Secrecy and Post-Compromise Security


<!-- code-check: this section references two Sunfish namespaces — `Sunfish.Kernel.Security` and `Sunfish.Kernel.Sync` — both already in the current Sunfish package canon. No new top-level namespace is introduced; forward secrecy and post-compromise security extend the existing kernel session layer rather than adding a new Foundation tier. -->

Collaborator revocation closed the question of what happens at a session's end. Forward secrecy and post-compromise security govern what happens within a session that an attacker has partially observed. The key hierarchy and the four-layer defense model protect data at rest and constrain who may decrypt it. They are silent on a different question: when an adversary captures a session key today, what does that compromise expose about messages sent yesterday, and what does it expose about messages sent tomorrow.

Forward secrecy is the property that past communications stay confidential after a key compromise. Post-compromise security is the property that future communications recover confidentiality once the session advances past the captured state. Neither property is automatic. Each requires specific protocol design at the session layer. An architecture that names confidentiality without naming these two properties relies on the implementer or the transport substrate to supply them — a silent risk the conformance tests cannot detect. Sub-pattern 46e closes the gap by raising the commitment to a testable property of the protocol specification.

This section adds the session-key-compromise row to the §Threat Model taxonomy. §Key Compromise Incident Response governs the organizational response when a KEK is compromised; this section specifies what the protocol guarantees about messages before and after that response runs.

### Sub-pattern 46a — Per-message ephemeral key derivation

The key hierarchy uses long-lived KEKs to wrap per-document DEKs. That construction protects data at rest. It does not protect the transport of sync events between nodes, which travel through the relay as AES-256-GCM payloads. A relay observer who captures a long-lived session key decrypts every event encrypted under that key.

Per-message ephemeral key derivation closes that exposure. Each sync event carries a freshly derived message key. An attacker who recovers one message key decrypts exactly that message — not the prior message, not the next message. Compromise of today's message key does not expose yesterday's traffic, and rotation of the message key advances the chain past the compromised state.

The construction begins at session establishment. The two nodes perform an ephemeral X25519 (the Diffie-Hellman function over Curve25519) exchange and derive a shared secret. HKDF-SHA256 derives a per-message key chain from that secret. Each outbound message advances the chain by one step; the prior message key is zeroed after use. An attacker who recovers one chain state cannot reverse the chain — the ratchet is one-directional by construction.

This is the symmetric input path that sub-pattern 46b advances. `Sunfish.Kernel.Sync` owns the ephemeral exchange at session establishment. `Sunfish.Kernel.Security` owns the HKDF derivation and the per-message zeroing. The handshake boundary is the sync daemon protocol defined in Ch14 §Sync Daemon Protocol.

The honest boundary: per-message ephemeral derivation protects the transport. It does not protect the local database copy, which is AES-256-GCM encrypted under a DEK that persists until explicitly rotated. An attacker with both transport access and local-database access must compromise both layers. That is a harder problem. It is not an impossible one.

### Sub-pattern 46b — Sender and receiver ratchet (Double Ratchet)

Per-message ephemeral keys prevent retrospective decryption. The Double Ratchet pattern (Marlinspike and Perrin, Signal Foundation, 2016) [14] adds healing — the property that the session recovers confidentiality after a compromise without operator intervention.

The Double Ratchet combines two ratchets. The symmetric ratchet advances on every message: each outbound message derives its key from the ratchet state and advances that state forward. The Diffie-Hellman ratchet advances whenever a new DH public key from the other party arrives: the prior ratchet state combines with the new public key to produce a fresh shared secret, resetting the symmetric ratchet from a new entropy source the attacker who held the prior state cannot predict.

Forward secrecy comes from the symmetric ratchet's one-directionality. An attacker who recovers the ratchet state at time T decrypts messages from T forward but cannot reverse the ratchet to decrypt messages from before T. Post-compromise security comes from the Diffie-Hellman ratchet. Once both parties exchange a new ephemeral keypair — which happens naturally as they communicate — the session advances to a value the attacker who captured the old state cannot compute. The session heals automatically.

Session establishment uses an asynchronous key agreement protocol. The Signal X3DH (Extended Triple Diffie-Hellman) construction [15] establishes the initial shared secret from prekeys published in advance, allowing one party to initiate a session while the other party is offline. The Double Ratchet then runs over the X3DH output. The Inverted Stack adopts X3DH or an equivalent asynchronous key agreement so that a node coming online can begin a session with a currently offline peer.

The Noise framework [16] provides a composable substrate for handshake construction. The KK pattern (both parties have known static keypairs) is the closer fit to the Inverted Stack's enrolled-device model, where each node holds a registered device keypair. The architecture does not mandate one specific construction; it mandates that whatever construction is used satisfies the two properties named above. MLS (Messaging Layer Security, RFC 9420) [17] extends ratcheting to group messaging through a TreeKEM construction; deployments with large role groups may adopt MLS in place of pairwise Double Ratchet. The WhatsApp end-to-end encryption specification [18] documents the Double Ratchet at billion-user scale.

`Sunfish.Kernel.Sync` extends its session layer to implement the Double Ratchet, an MLS group session, or a Noise-pattern equivalent. The architectural commitment is the two properties — forward secrecy and post-compromise security — not the specific construction. Cross-reference to Ch14 §Sync Daemon Protocol for the handshake that carries the ratchet state; §Relay Trust Model for the relay's role as ciphertext forwarder that observes ratchet messages without decrypting them.

### Sub-pattern 46c — Automatic key rotation on suspected compromise or scheduled cadence

Post-compromise security through the DH ratchet is progressive. It heals as parties communicate. Automatic scheduled rotation is the complementary mechanism for deployments where parties stay offline for extended periods between exchanges and the ratchet does not advance through normal traffic.

Two triggers advance the ratchet state independently of message traffic. The first is suspected compromise. When endpoint-compromise detection fires (cross-reference to §Endpoint Compromise: What Stays Protected), the session forces an immediate DH ratchet step. The compromised party generates a new ephemeral X25519 keypair, publishes the new public component, and marks the previous session state as poisoned. Peers advance their own DH ratchet on receipt of the new public key. Collaborator revocation (cross-reference to §Collaborator Revocation and Post-Departure Partition) behaves the same way: a revocation event forces a ratchet advance for every remaining session, so the revoked party's last-known ratchet state cannot decrypt subsequent messages.

The second trigger is scheduled cadence. Even without a detected compromise, the session forces a DH ratchet step every 90 days, matching the KEK rotation cadence in §Key Hierarchy. Scheduled rotation closes the long-lived-session gap that arises when peers communicate frequently but never trigger a fresh DH exchange.

`Sunfish.Kernel.Security` exposes the rotation trigger interface. `Sunfish.Kernel.Sync` executes the new ephemeral exchange at the next feasible session event. The trigger is a no-op if the DH ratchet has already advanced within the rotation window through normal message traffic.

### Sub-pattern 46d — Sealed sender

The relay forwards ciphertext between nodes. Even without decrypting payload, the relay observes the communication graph: which node sends to which, at what rate, at what time. For most enterprise deployments, that metadata is not sensitive. For deployments in healthcare, legal services, or politically sensitive environments, knowing that Node A communicated with Node B at 11:47 PM on the day of a board vote is itself sensitive information.

Sealed sender hides the sender's identity from the relay. The sender encrypts the outer-envelope source identifier under the recipient's long-term public key before submitting the message. The relay sees the destination node identifier but not the source. The recipient unwraps the sealed identity after decrypting the message payload and verifies the sender's role attestation at that point.

The construction creates a validation asymmetry. Without seeing the sender, the relay cannot enforce sender-side authorization. The architecture resolves the asymmetry by moving authorization validation to the recipient: the recipient checks the sender's identity and attestation after unsealing. A relay that enforces authorization without seeing the sender requires zero-knowledge proof machinery; this book defers that variant to a future volume.

Sealed sender is opt-in. `Sunfish.Kernel.Sync` exposes a sealed-sender policy flag in the session configuration. Setting the flag switches the outer-envelope construction for metadata-sensitive deployments. Cross-reference to §Relay Trust Model for the full discussion of relay-observed metadata and its mitigations.

### Sub-pattern 46e — Protocol-level forward secrecy commitment

The preceding sub-patterns are implementation choices. Sub-pattern 46e is a declaration: the protocol specification names forward secrecy and post-compromise security as required properties, not as implementation details. Off-The-Record Messaging (Borisov, Goldberg, and Brewer, 2004) [19] established the precedent — naming these properties in the protocol spec itself, not in an implementation note — and Signal, MLS, and Noise all inherited the discipline. <!-- CLAIM: OTR 2004 [19] named forward secrecy explicitly; "post-compromise security" as a named property post-dates OTR (PCS terminology is generally attributed to Cohn-Gordon, Cremers, Garratt c. 2016). The phrase "these properties" therefore overcredits OTR for both. Defer to next-pass copy-edit (precision tightening, not architectural change). -->


Naming the commitment makes it testable. A conformance test for forward secrecy: given a recorded session state at time T, no key material derivable from that state decrypts a message sent at time T-1. A conformance test for post-compromise security: given a captured ratchet state at time T, after one DH ratchet advance, no key material derivable from the captured state decrypts a message sent at time T+2. These tests live in `Sunfish.Kernel.Security`'s test suite alongside the existing key-zeroing and memory-locking validations. They are cryptographic property assertions, not integration tests; any conforming implementation passes them. Cross-reference to §Key-Loss Recovery for the recovery interaction: recovery reconstitutes KEK custody but does not reconstitute ratchet state, so forward secrecy for the pre-recovery period is not retroactively recovered.

### FAILED conditions

The forward secrecy and post-compromise security primitive fails when any of the conditions below holds. Any one of them voids the primitive's guarantees.

- **Past messages are decryptable from current key material.** Forward secrecy failure. Occurs when per-message keys are not derived from an advancing ratchet, or when old ratchet states are not zeroed after use.
- **Current key compromise propagates to future messages without rotation.** Post-compromise security failure. Occurs when the DH ratchet never advances — either because the session implementation uses only a symmetric ratchet, or because DH advance is conditional on manual operator action.
- **No automatic key rotation exists.** Neither property is self-enforcing without a rotation mechanism. An implementation that names forward secrecy and post-compromise security in its protocol spec but offers no automatic trigger to advance the DH ratchet on suspected compromise or scheduled cadence has delivered a theoretical property without an operational one.

The kill trigger for this primitive is a FAILED condition that recurs across three consecutive technical-review passes. A single intermittent failure is a defect to fix; a persistent failure signals that the session-layer implementation has not converged on the architectural commitment.

---

## References

<!-- Phase 3 placeholder: Ch22's share of the Ch15 reference list (~470 words). Citations split per-section between Ch15 (architecture share) and Ch22 (operations share); Ch22 keeps cites referenced from O sections. Per UPF Phase 1 triage: Shamir [6] (key-loss recovery), Buterin [4] (social recovery), Argent [5] (multi-sig wallet patterns), Sigstore [2] (supply chain — though cross-referenced from Ch15), the SGX/TEE family [22]–[24] (endpoint compromise), Pegasus + Hermit [26]–[27] (endpoint compromise), TSP RFC 3161 [28] (chain-of-custody timestamp), and the DP family [32]–[36] if Privacy-Aggregation is reclassified to O in a later round (currently A per Phase 1 triage footnote ¹). Final assignment confirmed during Phase 5 cross-reference work. -->
