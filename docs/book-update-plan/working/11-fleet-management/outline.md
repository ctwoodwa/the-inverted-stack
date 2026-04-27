# 11 — Fleet Management — Outline

**ICM stage:** outline → ready for draft.
**Decision:** NEW Chapter 21 — "Operating a Fleet of Local-First Nodes" (see §A introduction for reasoning).
**Target:** Ch21 — new chapter in a new Part V ("Operational Concerns"), or inserted as the opening chapter of an operational coda following Part IV.
**Total word target:** 6,500 words.
**Source:** `docs/reference-implementation/design-decisions.md` §5 entry #11 (sub-patterns derived from primitive specification).
**Why this is fourth in the priority list:** fleet management is the "at scale" unlock. Extension #48 keeps individual users' data safe. Extension #43 keeps individual nodes fast. Extension #45 keeps departures clean. Extension #11 makes all of that operate across tens, hundreds, or thousands of nodes without individual attention per node. Sunfish at production scale requires it.

---

## §A Introduction — Chapter vs. Appendix Decision

### The decision: New Chapter 21.

**Reasoning:**

Fleet management at the scale this extension covers — provisioning, key rotation orchestration, OTA update coordination, and fleet observability — is operational prose, not reference material. It requires:

- **Narrative structure:** the chapter must argue *why* fleet-scale operations break the assumptions built into the single-node playbooks (Ch17–Ch20) and *what* changes when a node is headless, provisioned at flash time, and never touched again by a human after deployment.
- **Opinion:** the chapter takes a position. It argues that fleet management is not an afterthought — it is the moment the local-first architecture either holds its properties at scale or quietly abandons them. That argument requires a chapter's voice, not an appendix's list.
- **Scenarios:** the canonical fleet failure scenario — a key rotation that partially propagates across 500 nodes, leaving 47 in a detached state — is the kind of concrete adversarial scenario that drives Part II and Part IV. It belongs in the same register.
- **Continuity with Part IV:** Ch17–Ch20 each address a specific phase of the node lifecycle (build, migrate, ship, UX). Ch21 addresses the operational phase that comes after ship: sustain. It is the natural conclusion of the playbook arc.

**Why not an appendix:**

Existing appendices (A–F) are reference artifacts: a wire protocol specification, threat-model worksheets, a reading list, a test recipe collection, a citation guide, a regulatory coverage matrix. Each is consulted, not read. Fleet management cannot be consulted out of order; it is a coherent operational argument with dependencies on Ch15 (key rotation), Ch14 (sync daemon), Ch19 (enterprise deployment), and the new extensions #48 and #45. An appendix that needs to be read linearly and that takes a position is a chapter in disguise.

**Word count reasoning:** 5,000–8,000 words permitted by the loop-plan §4. This outline targets **6,500 words** — the midpoint, weighted toward specification depth. The four major sub-pattern families (provisioning, key rotation orchestration, OTA, observability) each warrant ~1,200 words. A framing section and a FAILED conditions section add ~700 words each. The §I subagent prompt will target 6,500 words with ±10% latitude.

**Structural placement:** Ch21 opens a Part V titled "Operational Concerns" rather than appending awkwardly to Part IV. Part V is a single-chapter part — a coda. This is a deliberate structural signal: Part I convinces, Part II stress-tests, Part III specifies, Part IV implements, Part V operates. The word "operates" is important: it separates the first-deployment concerns of Part IV from the ongoing-operations concerns of Ch21. If the loop later adds #47 (endpoint-compromise threat model operational posture) or other primitives with operational-phase concerns, Part V has room for them. If not, it remains a single-chapter coda — no structural damage.

**File path:** `chapters/part-5-operational-concerns/ch21-operating-a-fleet.md`

---

## §A. Chapter 21 — "Operating a Fleet of Local-First Nodes"

**H1:** `# Chapter 21 — Operating a Fleet of Local-First Nodes`

**Word target:** 6,500 words across all sections below.

---

### A.1 Why fleet management is a distinct discipline (≈700 words)

This section is the chapter's framing argument. It does not introduce the architecture (Ch21 assumes Part I is read). It argues that operating at fleet scale breaks every assumption that Ch17–Ch20 embed in their "single operator, visible node" model.

- The single-node model is explicit in Part IV: Ch17 has you building one node, wiring it, watching it sync. Ch19 has you deploying it to a managed endpoint where IT can see it. Ch20 has you designing UX that a human interacts with. Each of those chapters assumes a human is nearby.
- The fleet model removes that assumption. A fleet of local-first nodes is headless, distributed, possibly air-gapped, provisioned at manufacturing or flash time, and expected to self-manage its security posture between rare maintenance windows.
- The canonical fleet scenario for this book: a construction-industry deployment (the vertical introduced in Ch8 and carried through Part III) where each site office has a local node running on an edge device. Forty sites. Each site goes through a network-isolated phase during excavation. Key rotation needs to happen. An OTA update needs to push. Who is watching the dashboard when site 23's node silently falls behind the rotation epoch?
- This section names the four operational responsibilities that the existing architecture does not specify at fleet scale:
  1. **Provisioning** — how a new node is initialized with its identity, keys, and initial data without a human in the loop
  2. **Key rotation orchestration** — how a fleet-wide key rotation propagates to all nodes within a defined time window, tracks stragglers, and escalates when nodes fall behind
  3. **OTA update coordination** — how software updates are delivered to headless nodes in a verifiable, rollback-capable way
  4. **Fleet observability** — how an operator monitors the security posture, health, and sync state of dozens or hundreds of nodes without per-node SSH access
- Cross-reference to Ch15 §Key Rotation and Revocation (the single-node rotation model this section extends to fleet scale), Ch19 §Admin Tooling (the enterprise-side panel this chapter operationalizes at fleet size), and extension #43 (performance contracts per node that fleet observability monitors).

**FAILED conditions block** (displayed as a named block, same format as extension #43 and #45):

**FAILED conditions:**
- Any node completes key rotation without the fleet operator knowing it succeeded or failed
- Any OTA update reaches less than the operator-configured minimum propagation threshold without escalation
- Any new node enters the fleet with a key bundle derived outside the fleet's provisioning ceremony
- Fleet observability shows health metrics that are more than the operator-configured staleness window out of date
- A stale node (behind the current key rotation epoch by more than one epoch) continues to receive new events from the relay without quarantine

---

### A.2 Sub-pattern 11a — Provisioning at flash time (≈1,200 words)

This sub-pattern covers the moment a new node joins the fleet — not as a human-initiated event (Ch17's QR-code onboarding) but as a manufacturing or deployment ceremony that initializes the node's identity and key bundle before it ever reaches the field.

- **The provisioning ceremony.** A fleet provisioning ceremony is a controlled, attested initialization event that produces a signed node identity bundle (device keypair, initial KEK bundle for its assigned fleet segment, initial sync configuration, enrollment receipt). The ceremony happens in a trusted environment — a factory, a CI/CD pipeline, a deployment staging area — not in the field.
- **Three provisioning models:**
  - *Pre-provisioned hardware:* the device leaves the factory with a node identity burned in at manufacturing time. The node's device keypair is generated by a hardware security module (HSM) during manufacturing and never leaves the device. The public key is registered with the fleet registry; the private key is sealed to the device's Secure Enclave or TPM. This is the highest-assurance model.
  - *Zero-touch deployment:* the device arrives factory-reset. When it first connects to a trusted network (or to a USB provisioning tool), it receives its node identity and initial key bundle via an authenticated provisioning protocol. The provisioning server verifies the device's hardware attestation before issuing the bundle. This model accommodates field replacement without requiring a human to carry the key material.
  - *Operator-mediated enrollment:* for smaller fleets or deployments without TPM/Secure-Enclave support, an operator manually completes a reduced provisioning ceremony — typically a QR-code or NFC exchange that transfers the initial key bundle under the operator's credential. The enrollment receipt is the audit artifact. This is the fallback, not the default.
- **The enrollment receipt.** Every provisioning event produces a signed enrollment receipt: the device's public key, the fleet segment assignment, the key bundle epoch at provisioning time, the provisioning operator's identity (for operator-mediated model), the HSM or platform attestation (for hardware models), and the timestamp. The receipt is stored in the fleet registry (operator-side) and in the node's own audit log. Cross-reference to extension #9 (chain-of-custody) — the enrollment receipt is a custody record: the device's identity is attested at a specific time under a specific key authority.
- **Fleet segmentation.** Large fleets may organize nodes into segments that have different key material, sync scope, and update channels. The provisioning ceremony assigns the node to a segment; the assignment is cryptographically bound to the node's identity bundle. Segment re-assignment requires a re-provisioning ceremony, not an in-band configuration change.
- `Sunfish.Foundation.Fleet` — owns the provisioning ceremony, the enrollment receipt schema, and the fleet registry client. Mark all references `// illustrative — not runnable`.
- Cross-reference to Ch15 §Device and User Identity (the single-node device keypair model this section extends), Ch17 §QR-Code Onboarding (the interactive enrollment this sub-pattern replaces for headless nodes), and Ch19 §Admin Tooling (the fleet registry the operator manages).

---

### A.3 Sub-pattern 11b — Fleet-scale key rotation orchestration (≈1,200 words)

This sub-pattern extends Ch15's single-node key rotation to the fleet context. The single-node rotation is a local operation — one node, one rotation event, immediate effect. Fleet rotation is a coordinated operation — N nodes, a rotation window, a propagation tracker, and an escalation path for nodes that fall behind.

- **The rotation epoch.** A fleet key rotation is announced as a rotation epoch event: a signed announcement that names the new KEK bundle, the epoch identifier, the propagation deadline (a timestamp after which nodes still on the old epoch are quarantined), and the fleet segment scope. The announcement travels through the relay to all nodes in the segment.
- **The propagation window.** Nodes have until the propagation deadline to confirm receipt of the new epoch. Confirmation is a signed acknowledgment event that the node emits to the fleet registry after successfully wrapping its local DEKs under the new KEK. The fleet registry tracks the propagation state per node.
- **Straggler handling.** A node that has not confirmed by the deadline is a straggler. Straggler handling has three levels:
  - *Warning:* the node is flagged in fleet observability with a staleness indicator. Operator is notified. No operational change yet.
  - *Read-only quarantine:* after a second configurable deadline, the straggler node is moved to read-only mode for new relay events. It continues to serve its local data but receives no new events from the relay under the new epoch. Cross-reference to Ch15 §Offline Node Revocation and Reconnection — the offline-revocation circuit breaker handles the reconnection logic; fleet quarantine extends that primitive to the rotation-epoch context.
  - *Decommission escalation:* after a third deadline (operator-configured; typically 30 days beyond the initial propagation window), the node is flagged for operator decommission. The fleet registry records the escalation event. The operator decides whether to attempt recovery (re-provisioning ceremony) or retire the node.
- **Re-keying background job.** The DEK re-wrapping job that Ch15 §Post-Revocation Key Rotation specifies for individual nodes runs on each node in the fleet independently, triggered by receipt of the new epoch announcement. `Sunfish.Foundation.Fleet` coordinates the epoch announcement; `Sunfish.Kernel.Security` runs the per-node re-wrapping job. The fleet layer monitors completion; the security layer performs the work.
- **Key rotation cadence.** Fleet key rotation cadence is deployment-class dependent. For a regulated-tier fleet (HIPAA, PCI, SOX), rotation runs quarterly at minimum. For a standard-tier fleet, annually or on security-incident trigger. For a fleet with a compromised node (extension #47 endpoint compromise), an out-of-band triggered rotation runs on the segment that included the compromised node. Cross-reference to extension #47 (endpoint compromise) and Ch15 §Key Compromise Incident Response.
- `Sunfish.Foundation.Fleet` — owns the epoch announcement, propagation tracker, straggler registry, and escalation events.
- Cross-reference to Ch15 §Key Rotation and Revocation (per-node rotation), Ch15 §Collaborator Revocation (the revocation circuit breaker the straggler path uses), and extension #48 §Recovery-event audit trail (the same `Sunfish.Kernel.Audit` substrate records fleet rotation events).

---

### A.4 Sub-pattern 11c — OTA update coordination (≈1,200 words)

Over-the-air (OTA) software updates to headless fleet nodes are one of the highest-risk operations in a local-first fleet deployment. Unlike a desktop update (the user is present; the installer is interactive), a fleet OTA is unattended, potentially across a patchy connectivity window, and cannot require a human to verify it completed.

- **The update bundle.** A fleet OTA update is a signed artifact: the new software version, a cryptographic hash, the signing key's certificate chain (rooted in the fleet operator's release signing key, per Ch19 §Code Signing), a delta patch or full installer, and the update metadata (target segment, minimum rollback version, compatibility matrix). The bundle is content-addressed — the node can verify the hash before applying.
- **The staged rollout model.** Fleet OTA does not push simultaneously to all nodes. A staged rollout:
  - *Canary stage:* 1–5% of nodes in the segment receive the update first. The fleet registry monitors canary nodes for error rates, sync stability, and performance-contract violations (extension #43) over a configurable soak window.
  - *Wave expansion:* if canary soak passes, the rollout expands to 25%, 50%, 100% in configurable waves with soak windows between them.
  - *Automatic rollback:* if any wave's error rate exceeds the operator-configured threshold during soak, the rollout halts. Nodes that received the update receive a rollback bundle. The rollback bundle is pre-signed at the same time as the update bundle — the operator cannot rollback without a pre-committed rollback artifact.
- **Verifiable update gating.** Before applying an update, the node verifies: (1) the bundle's hash matches the manifest; (2) the signing certificate chain terminates at the fleet's trusted root; (3) the update version is greater than the installed version (downgrade attacks are refused); (4) the node's current hardware/software environment meets the compatibility matrix. Any gate failure aborts the update and logs a signed failure event.
- **Air-gap and offline-safe delivery.** For nodes that are periodically offline or air-gapped, the update bundle is queued in the fleet relay's update cache. When the node reconnects, it fetches the pending bundle and applies it at next maintenance window. The fleet registry tracks pending-update nodes separately from straggler nodes; the distinction matters for compliance reporting (software version is an asset attribute; out-of-date nodes in a regulated fleet are an audit finding).
- `Sunfish.Foundation.Fleet` — owns the update bundle manifest, staging configuration, rollout tracker, and rollback bundle management.
- Cross-reference to Ch19 §Code Signing and Notarization (the signing infrastructure this sub-pattern extends to fleet OTA), Ch19 §Air-Gap Deployment (the internal update server this sub-pattern extends to fleet scale).

---

### A.5 Sub-pattern 11d — Fleet observability (≈1,200 words)

Fleet observability answers the question: what is the security posture and operational health of every node in the fleet, at any moment, without SSH access to individual nodes?

- **The observability contract.** Each node emits a signed health heartbeat to the fleet registry on a configurable interval (default: 5 minutes for connected nodes; on-reconnect for offline nodes). The heartbeat carries: the node's current key rotation epoch, the current software version, the sync daemon status (running, degraded, stopped), the CRDT engine's last operation timestamp, the node's disk utilization tier (normal, warning, critical), the performance-contract status (per extension #43 — budget-compliant, degraded, or violated), and any queued circuit-breaker events from Ch15.
- **The fleet dashboard dimensions.** Fleet observability surfaces four dimensions for every node:
  - *Security posture:* current key epoch vs. fleet epoch; whether the node is within the propagation window; any pending revocation events from extension #45.
  - *Software currency:* installed version vs. fleet target version; pending OTA update status; rollback eligibility.
  - *Sync health:* last successful gossip round; peer count; relay connectivity status; last CRDT operation received and emitted.
  - *Performance posture:* performance-contract compliance per extension #43; last budget-violation event and its timestamp.
- **Aggregation and alerting.** The fleet registry aggregates heartbeats into fleet-level summaries. Alerts fire on configurable thresholds: `>5% nodes straggling on key rotation`, `any node on a software version older than 3 releases`, `>10% nodes showing sync-health degradation simultaneously` (which may indicate a relay issue rather than per-node issues). Alerts are distinct from per-node escalations — fleet-level aggregation catches systemic issues that per-node monitoring misses.
- **The compliance export.** For regulated-tier fleets, the fleet registry exports a signed compliance snapshot on demand: every node's software version, key epoch, and last-health-event timestamp, in a format that satisfies SOC 2 audit evidence requirements and HIPAA risk-assessment documentation. The export is point-in-time, signed, and content-addressed — it is an immutable record of the fleet's posture at the moment the export was requested.
- **Offline node handling.** A node that has not emitted a heartbeat within the staleness window is flagged as offline rather than unhealthy — offline is an expected state in a local-first fleet. The fleet dashboard distinguishes: `Online (current)`, `Online (stale heartbeat)`, `Offline (last seen: N hours ago, posture unknown)`, `Quarantined (stale epoch)`, `Decommissioned`. The distinction matters: an offline node is not a security problem unless it is also behind on key rotation.
- `Sunfish.Foundation.Fleet` — owns the heartbeat protocol, the fleet registry, the dashboard aggregation layer, and the compliance export.
- Cross-reference to Ch11 §The UI Kernel (the `SunfishNodeHealthBar` per-node health indicator; fleet observability is the fleet-level equivalent), Ch14 §Sync Daemon Protocol (the gossip round status that fleet health tracks), and extension #43 §Performance Contracts (the performance posture dimension).

---

### A.6 The fleet failure scenario — narrative (≈700 words)

This section is the chapter's opinion piece — the part that makes Ch21 a chapter rather than a list of sub-patterns. It walks through the canonical fleet failure: a key rotation that partially propagates, leaving nodes in a split epoch, and what the fleet management primitives above do about it.

- The scenario: 200 nodes in the fleet. A key rotation is announced. 183 nodes confirm within 48 hours. 17 nodes are offline (sites in excavation-phase with no connectivity). The propagation deadline passes. Straggler quarantine activates on the 17 offline nodes.
- Eight days later: 14 of the 17 offline nodes come back online. They receive the epoch announcement, complete re-wrapping, confirm, and exit quarantine. Fleet observability marks them `Online (current)`. Three nodes remain offline. Fleet observability marks them `Offline (last seen: 8 days ago, straggler epoch)`.
- Thirty days after the original rotation announcement: the three stragglers have not reconnected. The fleet registry fires a decommission escalation event. The operator must decide: attempt re-provisioning ceremony (if the devices are reachable), or retire them from the fleet. The audit trail records the escalation and the operator's decision.
- What would have happened without fleet management: the 17 nodes would have continued receiving relay events under the old epoch until the relay's backward-compatibility window expired. At that point, they would have silently lost sync without any escalation, any operator notification, or any audit trail. The operator would have discovered the problem when a site-office user reported that their data was several weeks old.
- The argument: fleet management is the mechanism that converts an invisible, silent failure mode into a visible, tracked, escalated operational event. The architecture does not make fleet operations easy. It makes fleet failures observable.
- Cross-reference to Ch4 §Choosing Your Architecture (the deployment-class filter that identifies fleet-scale deployments as requiring this chapter), and to Part V's framing as the operational coda: Part IV teaches you to ship; Part V teaches you to sustain.

---

## §B. Not applicable.

This extension places all content in a single chapter (Ch21). There is no second insertion point. §B is unused.

---

## §C. Code-Check Requirements

The draft references the following Sunfish namespaces by name only (per CLAUDE.md Sunfish reference policy — pre-1.0; package names not class APIs):

### NEW namespace: `Sunfish.Foundation.Fleet`

**Recommendation:** `Sunfish.Foundation.Fleet` (not `Sunfish.Kernel.Fleet`).

**Reasoning:** The fleet management layer sits *above* the kernel. The kernel owns the per-node primitives: sync daemon lifecycle (`Sunfish.Kernel.Sync`), security envelope and key rotation (`Sunfish.Kernel.Security`), performance contracts (`Sunfish.Kernel.Performance`). The fleet layer *orchestrates* those per-node kernel primitives across a population of nodes — it is a coordination layer, not a low-level protocol layer. Foundation packages in the existing architecture are coordination-and-abstraction layers above the kernel (e.g., `Sunfish.Foundation.LocalFirst`, `Sunfish.Foundation.Recovery`). Fleet management matches that pattern.

**What `Sunfish.Foundation.Fleet` owns:** provisioning ceremony coordinator, enrollment receipt schema, fleet registry client, key-rotation epoch announcer and propagation tracker, straggler management and escalation, OTA update bundle manifest and staging configuration, node health heartbeat emitter (node-side), fleet-level aggregation and alerting (operator-side), compliance snapshot export.

**What it does NOT own:** per-node key rotation job (belongs to `Sunfish.Kernel.Security`), per-node sync daemon (belongs to `Sunfish.Kernel.Sync`), per-node performance contract enforcement (`Sunfish.Kernel.Performance`). Fleet management monitors and orchestrates; the kernel packages execute.

**Status:** `book-committed` — not yet scaffolded; no ADR yet. The code-check report for this extension must add the entry to `docs/reference-implementation/sunfish-package-roadmap.md`.

### Existing namespaces referenced in Ch21:

- `Sunfish.Kernel.Security` — in canon; key rotation job and revocation circuit breaker.
- `Sunfish.Kernel.Sync` — in canon; sync daemon status consumed by fleet observability heartbeat.
- `Sunfish.Kernel.Audit` — forward-looking (introduced by extension #48); fleet rotation events and compliance snapshots share this audit substrate. Mark `// illustrative — not runnable`.
- `Sunfish.Kernel.Performance` — forward-looking (introduced by extension #43); fleet observability includes performance-posture dimension per node. Mark `// illustrative — not runnable`.
- `Sunfish.Foundation.Recovery` — forward-looking (introduced by extension #48); re-provisioning ceremony path re-uses recovery patterns for node identity restoration. Mark `// illustrative — not runnable`.

All `Sunfish.Foundation.Fleet` references marked `// illustrative — not runnable`.

---

## §D. Technical-Review Focus

For the `@technical-reviewer` pass:

- **MDM and mobile device management literature.** The provisioning sub-pattern (11a) describes zero-touch deployment and hardware-attested provisioning. Verify the architecture's claims are consistent with Apple Business Manager, Google Zero-Touch Enrollment, and Microsoft Windows Autopilot documentation. The claim that "the public key is registered with the fleet registry; the private key is sealed to the device's Secure Enclave or TPM" needs to trace to hardware attestation documentation for each platform. Candidate citations: Apple Business Manager documentation; Google Zero-Touch Enrollment developer guide; Microsoft Intune Autopilot; TCG TPM 2.0 specification (for TPM-based key sealing).

- **OTA update systems for embedded and edge deployments.** The OTA sub-pattern (11c) describes staged rollouts, verifiable gating, and automatic rollback. Verify against documented OTA systems: RAUC (Robust Auto-Update Controller), SWUpdate, Mender.io, Balena. The staged-rollout model with canary + wave expansion is documented in these systems. The automatic rollback on error-rate threshold is an architectural claim the reviewer should trace to an existing reference or mark as new architectural commitment. Candidate citations: RAUC project documentation; Mender.io documentation; Balena documentation.

- **Key rotation at fleet scale.** The rotation-epoch model (11b) is a new architectural primitive — no direct analogue in v13/v5. The reviewer must confirm: (1) the epoch-announcement + propagation-window + straggler-quarantine model is internally consistent with Ch15's per-node rotation semantics; (2) the DEK re-wrapping background job (per `Sunfish.Kernel.Security`) is idempotent so that a node which receives the epoch announcement twice (due to network retry) does not double-wrap; (3) the "read-only quarantine" for straggler nodes is consistent with the offline-revocation circuit breaker described in Ch15 §Offline Node Revocation and Reconnection.

- **Fleet observability and telemetry.** The observability sub-pattern (11d) references signed health heartbeats. The reviewer should verify: (1) what the heartbeat's encryption model is — does the heartbeat travel outside the standard sync channel? (2) whether a fleet registry that aggregates heartbeats from all nodes is consistent with the data minimization invariant the architecture enforces elsewhere (Ch14 §Data Minimization Invariant). The fleet registry knows each node's software version, key epoch, and sync state — this is metadata, not content, but the reviewer should flag whether this is a new metadata trust boundary. Candidate citation: Prometheus exposition format (as a reference for structured telemetry); Grafana fleet observability patterns; AWS IoT Fleet Indexing documentation.

- **Compliance posture for fleet software.** The compliance export sub-pattern in §A.5 claims to satisfy SOC 2 audit evidence requirements and HIPAA risk-assessment documentation. The reviewer must verify these claims are scoped correctly: SOC 2 Type II requires evidence of controls operating over time, not a point-in-time snapshot. The compliance export is a point-in-time artifact — the section must acknowledge this limitation and note that a series of exports forms the time-series evidence. HIPAA §164.306(e) (maintenance standard) requires periodic review and modification of security measures, which a fleet compliance export supports but does not complete. Candidate citations: SOC 2 (AICPA Trust Services Criteria 2022); HIPAA Security Rule §164.306; NIST SP 800-82 (Guide to Industrial Control Systems Security — relevant for edge/embedded fleet context).

- **Trace every architectural claim** to v13/v5 source papers OR mark as new architectural commitment surfaced through universal-planning review (per design-decisions §5 #11). The fleet management primitive is entirely new; none of its sub-patterns appear in v13/v5. The chapter's opening section (§A.1) must acknowledge this explicitly: Ch21 extends the architecture defined in Part III into an operational domain the original papers did not address.

---

## §E. Prose-Review Focus

For the `@prose-reviewer` + `@style-enforcer` pass:

- **Part IV tutorial register, extended to operational voice.** Ch21 is a playbook chapter, not a specification chapter. It uses second-person address for configuration and operational decisions. "Configure your canary threshold before the first production rollout — not during it." Not "operators should consider configuring the canary threshold."
- **Active voice throughout.** "The fleet registry flags the straggler" — not "the straggler is flagged by the fleet registry." "The node verifies the bundle hash" — not "the bundle hash is verified by the node."
- **Lead with the operational consequence.** Each sub-pattern opens with what goes wrong in its absence, not what the mechanism does. "Without provisioning ceremonies, nodes carry keys generated outside the fleet's trust boundary" — that is the opening sentence of §A.2, not a list of benefits.
- **No hedging on quarantine and escalation timelines.** The propagation window, straggler deadlines, and rollback thresholds are named with specific defaults. "The default propagation window is 72 hours" — not "operators may wish to configure a propagation window of approximately 72 hours or thereabouts."
- **FAILED conditions block.** The FAILED conditions in §A.1 must appear as a named block in the chapter — not buried in prose. Same treatment as extension #43 and #45.
- **The fleet failure scenario (§A.6) is narrative, not specification.** Write it in the past tense, scenario voice. No bullet points. No table. It is a story about 200 nodes, a rotation, and 17 stragglers. The reader should feel the operational reality before the mechanism names appear.
- Paragraph length cap: 6 sentences.

---

## §F. Voice-Check Focus (HUMAN STAGE — not autonomous)

For the human voice-pass:

- **The fleet goes wrong anecdote.** The opening hook for Ch21 should be a concrete operational failure — the kind that happens in the field, not in a lab. Candidates:
  - The site-office manager who calls in to say their construction-management application hasn't updated in six weeks — and the IT team doesn't know why, because there's no fleet dashboard.
  - The security audit that flags 37 devices running software two major versions behind — with no way to push an update because the OTA system was never set up.
  - The moment a key rotation completes on 194 of 200 nodes, and no one knows which six are behind, or why, or whether they're still receiving any data at all.
- **The provisioning ceremony as a cultural shift.** The move from interactive onboarding (Ch17's QR-code flow) to provisioning ceremonies is a shift in the operator's mental model: nodes are not people; they are infrastructure. The voice-pass should acknowledge this shift explicitly — there is a moment when "operating a fleet" stops feeling like "managing a group of users" and starts feeling like "operating a distributed system." That moment is the chapter's emotional core.
- **The connective tissue from Ch19 to Ch21.** Ch19 teaches the operator to ship to enterprise. Ch21 teaches the operator to sustain at fleet scale. A sentence in Ch21's opening that acknowledges this arc — "Ch19 got you to production; this chapter keeps you there" — is the connective tissue the voice-pass should add or refine.
- **Calibrate Sinek register lightly** per `feedback_voice_sinek_calibration.md` memory — do not over-mechanize the prose with deliberate-pacing hammering. The fleet failure narrative in §A.6 is the primary vehicle for voice; let it carry the weight.

---

## §G. Citations

The draft adds a new reference list to Ch21 (IEEE numeric, beginning at [1] for the new chapter):

**[1] Apple Inc., "Apple Business Manager User Guide," Apple Inc., 2025.** [Online]. Available: https://support.apple.com/guide/apple-business-manager/welcome/web — for zero-touch enrollment and device provisioning.

**[2] Google LLC, "Zero-touch enrollment for IT admins," Google Workspace Admin Help, 2025.** [Online]. Available: https://support.google.com/a/answer/7514005 — for Android/ChromeOS fleet provisioning.

**[3] Microsoft Corporation, "Windows Autopilot overview," Microsoft Learn, 2025.** [Online]. Available: https://learn.microsoft.com/en-us/mem/autopilot/overview — for Windows zero-touch deployment.

**[4] Trusted Computing Group (TCG), "TPM 2.0 Library Specification," TCG, 2019.** [Online]. Available: https://trustedcomputinggroup.org/resource/tpm-library-specification/ — for TPM-based key sealing in hardware-attested provisioning.

**[5] RAUC Project, "RAUC — Robust Auto-Update Controller," rauc.io, 2024.** [Online]. Available: https://rauc.readthedocs.io — for staged OTA update architecture in embedded deployments.

**[6] National Institute of Standards and Technology (NIST), "Guide to Industrial Control Systems (ICS) Security," SP 800-82 Rev. 3, 2023.** [Online]. Available: https://csrc.nist.gov/publications/detail/sp/800-82/rev-3/final — for edge/embedded fleet security context.

**[7] American Institute of Certified Public Accountants (AICPA), "Trust Services Criteria," 2022 edition, AICPA, 2022.** — for SOC 2 audit evidence requirements referenced in compliance export discussion.

**Citations to verify and possibly add (technical reviewer action required):**

- Mender.io or Balena OTA documentation for staged-rollout and automatic-rollback claims in §A.4. Candidate: Mender.io, "Mender Documentation," mender.io/docs, 2025.
- Prometheus exposition format or equivalent telemetry-format reference for the signed heartbeat protocol in §A.5. Candidate: Prometheus Authors, "Exposition Formats," prometheus.io, 2024.
- HIPAA Security Rule §164.306 for the compliance export claims in §A.5. Candidate: U.S. Department of Health and Human Services, "HIPAA Security Rule," 45 CFR Part 164, 2003 (as amended 2013).

**Note on citation numbering:** Ch21 is a new chapter; its citation list starts at [1]. The technical reviewer must confirm the first-appearance order in the draft and assign final numbers accordingly.

---

## §H. Cross-References to Add

Inside Ch21:

- Ch21 → Ch15 §Key Rotation and Revocation (the per-node rotation model that fleet key rotation orchestrates at scale)
- Ch21 → Ch15 §Offline Node Revocation and Reconnection (the offline-node circuit breaker that the straggler-quarantine path re-uses)
- Ch21 → Ch17 §QR-Code Onboarding (the interactive enrollment ceremony that fleet provisioning replaces for headless nodes)
- Ch21 → Ch19 §Code Signing and Notarization (the signing infrastructure that fleet OTA's verifiable gating builds on)
- Ch21 → Ch19 §Admin Tooling (the enterprise admin panel that fleet observability extends)
- Ch21 → Ch19 §Air-Gap Deployment (the internal update server that fleet OTA update delivery uses for offline nodes)
- Ch21 → Ch11 §The UI Kernel (the `SunfishNodeHealthBar` per-node health indicator; fleet observability is the fleet-level analogue)
- Ch21 → Ch14 §Sync Daemon Protocol (gossip-round status consumed by fleet heartbeat)
- Ch21 → Ch4 §Choosing Your Architecture (the deployment-class filter; fleet management applies to headless fleet deployments)
- Ch21 → Extension #43 (performance contracts per node — fleet observability includes performance-posture dimension)
- Ch21 → Extension #45 §Collaborator Revocation (pending revocation events surfaced in fleet security-posture dimension)
- Ch21 → Extension #48 §Recovery-Event Audit Trail (the `Sunfish.Kernel.Audit` substrate that fleet rotation events share)
- Ch21 → Extension #9 (chain-of-custody, future — enrollment receipts as custody records)
- Ch21 → Extension #47 (endpoint-compromise, future — fleet-triggered rotation on compromised-segment detection)

---

## §I. Subagent Prompt for the Draft Stage

The next iteration (`outline → draft`) will invoke `@chapter-drafter` with this prompt:

> Draft a new chapter for *The Inverted Stack*: **Chapter 21 — Operating a Fleet of Local-First Nodes** (~6,500 words). This chapter opens a new Part V ("Operational Concerns") that follows Part IV.
>
> File path: `chapters/part-5-operational-concerns/ch21-operating-a-fleet.md`. Create the directory `chapters/part-5-operational-concerns/` if it does not exist.
>
> Source: outline at `docs/book-update-plan/working/11-fleet-management/outline.md`. Follow the section structure and word targets exactly.
>
> Voice: Part IV tutorial register — direct second-person address for operational decisions, explicit "do not" instructions for common mistakes, minimal path to working fleet management. This is a playbook chapter that a practitioner reads while setting up fleet operations, not while specifying an architecture. Assume the reader has read Part I through Part IV.
>
> Active voice throughout. No academic scaffolding. No re-introducing the architecture. No hedging on operational thresholds — name specific defaults (72-hour propagation window, 30-day decommission escalation, 5-minute heartbeat interval, 1–5% canary stage).
>
> Chapter structure (per outline):
> - §A.1 Why fleet management is a distinct discipline (~700 words) — framing argument; FAILED conditions block as a named bulleted list under bold **FAILED conditions** label
> - §A.2 Sub-pattern 11a Provisioning at flash time (~1,200 words) — three provisioning models; enrollment receipt; fleet segmentation
> - §A.3 Sub-pattern 11b Fleet-scale key rotation orchestration (~1,200 words) — rotation epoch; propagation window; straggler handling; three escalation levels
> - §A.4 Sub-pattern 11c OTA update coordination (~1,200 words) — update bundle; staged rollout (canary + waves); verifiable gating; air-gap delivery
> - §A.5 Sub-pattern 11d Fleet observability (~1,200 words) — heartbeat protocol; four dashboard dimensions; aggregation and alerting; compliance export; offline-node handling
> - §A.6 The fleet failure scenario (~700 words) — narrative, past tense, scenario voice; 200 nodes, a key rotation, 17 stragglers; what fleet management makes visible that would otherwise be silent
>
> Sunfish references: `Sunfish.Foundation.Fleet` is a NEW forward-looking namespace introduced by this extension — mark all references `// illustrative — not runnable`. `Sunfish.Kernel.Security`, `Sunfish.Kernel.Sync` are in canon; no illustrative marker needed. `Sunfish.Kernel.Audit`, `Sunfish.Kernel.Performance`, `Sunfish.Foundation.Recovery` are forward-looking namespaces introduced by extensions #48, #43, and #48 respectively; mark `// illustrative — not runnable`.
>
> Citations: IEEE numeric. Begin at [1] for Ch21's new reference list. Assign citation numbers in order of first appearance in the prose. At minimum include the seven sources listed in outline §G. The technical reviewer will verify and may add additional sources before finalizing.
>
> Cross-references: per outline §H — the draft must wire all of them. The most important pairs: Ch21 → Ch15 §Key Rotation (the per-node model being extended), Ch21 → Ch19 §Admin Tooling and §Code Signing (the enterprise deployment layer being scaled), Ch21 → extension #43 performance contracts (fleet observability dimension).
>
> FAILED conditions block: must appear in §A.1 as a named block — not buried in prose. Same format as extensions #43 and #45.
>
> The fleet failure scenario (§A.6) is narrative, not specification — write it in past tense, scenario voice, no bullet points. It is the chapter's argument, not a sub-pattern description.
>
> Chapter frontmatter: include `<!-- icm/draft -->`, word-count comment, and source references comment per existing chapter conventions.

---

## §J. Quality Gate for `outline → draft`

Per loop-plan §5: outline has all section headers + bullet points (✓ §A.1 through §A.6 above); word count target estimated (✓ 6,500 words); subagent prompt prepared (✓ §I above). Gate passes.

**Sub-pattern coverage map:**

| Sub-pattern | Designation | Section(s) |
|---|---|---|
| 11a Provisioning at flash time | §A.2 (Ch21 spec + tutorial) | One section |
| 11b Fleet-scale key rotation orchestration | §A.3 (Ch21 spec + tutorial) | One section |
| 11c OTA update coordination | §A.4 (Ch21 spec + tutorial) | One section |
| 11d Fleet observability | §A.5 (Ch21 spec + tutorial) | One section |

All four sub-patterns have designated subsections. Each is covered in both its specification dimension (what the mechanism does and why) and its tutorial dimension (how the operator configures and uses it). The fleet failure scenario (§A.6) is the synthetic section that makes the sub-patterns operational rather than theoretical.

**FAILED conditions from design-decisions §5 #11 reflected in outline:**

- FAILED: any node completes key rotation without operator visibility → §A.3 (propagation tracker) + §A.5 (observability dashboard)
- FAILED: OTA update reaches less than minimum propagation threshold without escalation → §A.4 (staged rollout + automatic rollback)
- FAILED: new node enters fleet with keys generated outside provisioning ceremony → §A.2 (provisioning ceremony; enrollment receipt)
- FAILED: fleet observability metrics are more than staleness window out of date → §A.5 (heartbeat protocol; offline-node handling)
- FAILED: straggler node continues receiving new events without quarantine → §A.3 (straggler quarantine escalation levels)

All five FAILED conditions are addressed. The kill trigger for this extension is the standard loop-plan quality-regression trigger (3 consecutive technical-review failures on the same gate).

**Sunfish namespace decision:** `Sunfish.Foundation.Fleet` recommended (not `Sunfish.Kernel.Fleet`). Reasoning: fleet management is a coordination-and-orchestration layer above the kernel, consistent with the Foundation tier's role in the existing package architecture. The code-check stage must add this namespace to `docs/reference-implementation/sunfish-package-roadmap.md` with status `book-committed` and the architectural commitment specified in §C above.

**Roadmap-doc update required at code-check stage:**

Add to `docs/reference-implementation/sunfish-package-roadmap.md` under `## Future forward-looking namespaces`:

- Advance the existing anticipatory entry `#11 fleet-management | NEW Sunfish.Foundation.Fleet` to a first-class entry with: source extension, status `book-committed`, architectural commitment (owns provisioning ceremony, fleet registry client, rotation epoch announcer, propagation tracker, OTA staging, heartbeat emitter, fleet aggregation, compliance export), open questions (whether Fleet depends on Kernel.Audit or extends it; whether the fleet registry is operator-side only or has a node-side agent).

---

**Estimated next-iteration duration (draft stage):** 90–120 minutes. Ch21 is the largest single draft in this extension set (6,500 words vs. 2,000–3,000 for sections-in-existing-chapters). Schedule next fire 2 hours after this one to allow context-cache cooldown and human-review window. The fleet failure scenario (§A.6) is the highest-risk section for voice quality — budget extra revision time there.
