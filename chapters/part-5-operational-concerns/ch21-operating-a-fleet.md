# Chapter 21 — Operating a Fleet of Local-First Nodes

<!-- icm/draft -->

<!-- Target: ~6,500 words -->
<!-- Source: outline at docs/book-update-plan/working/11-fleet-management/outline.md; design-decisions §5 #11 -->

<!-- code-check: this chapter introduces ONE new top-level Sunfish namespace, `Sunfish.Foundation.Fleet`, that is part of the Volume 1 extension roadmap and not yet present in the Sunfish reference implementation. Tracked in docs/reference-implementation/sunfish-package-roadmap.md. All other namespace references — `Sunfish.Kernel.Security`, `Sunfish.Kernel.Sync`, `Sunfish.Foundation.LocalFirst`, `Sunfish.Foundation.Recovery` (forward-looking from #48), `Sunfish.Kernel.Audit` (forward-looking from #48) — are either in the current Sunfish package canon or already tracked as forward-looking by extension #48. Code fences referencing `Sunfish.Foundation.Fleet` are marked `// illustrative — not runnable`. -->

---

Chapter 19 got you to production. This chapter keeps you there.

Part IV walks the operator through the lifecycle of a single node — building it, migrating into it, shipping it past enterprise IT, and designing the surface a human interacts with. Each chapter in that part embeds an assumption: a person is nearby. The user installs the application. The administrator runs the deprovisioning command. The IT technician investigates the failed install. The architect inspects the local data directory. Every chapter in Part IV makes operational sense because someone with hands and eyes and a keyboard is close to the node when something goes wrong.

A fleet of local-first nodes removes that assumption. The construction-industry deployment introduced in Chapter 8 is a useful frame: forty site offices, each with a headless edge device running a Sunfish (the open-source reference implementation, [github.com/ctwoodwa/Sunfish](https://github.com/ctwoodwa/Sunfish)) node, deployed through manufacturing or a flash-time provisioning ceremony, and never touched by a human after the device leaves the staging area. Sites go through excavation phases with no connectivity. Keys must rotate. Software must update. A device fails on a Tuesday in a trailer two thousand kilometres from anyone who could SSH into it. Who is watching the dashboard when site 23's node silently falls behind the rotation epoch?

Fleet management is the answer to that question. It is not a polish step on top of the single-node playbooks. It is a different operational discipline. A fleet of local-first nodes is a distributed system in the strict sense — many nodes, intermittent connectivity, no human at any individual node — and the architecture either holds its security and correctness properties at fleet scale or quietly abandons them between rare maintenance windows.

The chapter takes a position. The four sub-patterns specified below — provisioning at flash time, fleet-scale key rotation orchestration, OTA (Over-the-Air) update coordination, and fleet observability — are not optional features. They are the difference between a local-first architecture that scales and a local-first architecture that survives one quarter at production scale before silent failure modes accumulate into an unrecoverable state. Each sub-pattern is the runtime mechanism that converts a category of silent failure — a node that fell behind, a node that never got the patch, a node that drifted out of compliance, a node that nobody knew existed — into an observable operational event the operator can act on.

That conversion is the operational claim of this chapter. Fleet management does not prevent failures at fleet scale. It cannot. Failures happen — sites lose connectivity, hardware dies, key rotations propagate unevenly, OTA updates surface incompatibilities under load. What fleet management prevents is the *invisible* failure: the node that has been broken for six weeks while the operator believed everything was fine. Every primitive specified in this chapter exists to surface a specific class of silent failure as a tracked, escalatable event with an audit trail.

The shift from Chapter 17's interactive QR-code onboarding to fleet provisioning ceremonies, and from Chapter 19's enterprise admin panel to the fleet observability dashboard, is more than a scale change. It is a mental-model shift. Nodes are no longer people you manage. They are infrastructure you operate. That shift has implications for how you design the runbooks, who you trust to execute the procedures, and what you measure to know the system is healthy. Acknowledging the shift explicitly is the first step. Engineering for it is the rest of this chapter.

A new namespace surfaces alongside this chapter: `Sunfish.Foundation.Fleet`. It sits above the kernel, orchestrating the per-node primitives that `Sunfish.Kernel.Security` and `Sunfish.Kernel.Sync` already own. The fleet layer monitors and coordinates; the kernel executes. Fleet management is not a low-level protocol layer; it is a coordination-and-abstraction layer in the same architectural tier as `Sunfish.Foundation.LocalFirst` and `Sunfish.Foundation.Recovery`. All references to `Sunfish.Foundation.Fleet` in this chapter are forward-looking and marked `// illustrative — not runnable`.

The five FAILED conditions named at the close of Section 21.1 are the boundary conditions for this primitive. Any one of them voids the architectural claim that fleet management converts silent failures into observable events. The conformance test is whether each named failure, in a deployed fleet, surfaces as a specific operational artifact — an alert, a dashboard state, an audit-log record — within the operator-configured staleness window.

---

## 21.1 Why fleet management is a distinct discipline

Without fleet management, a local-first deployment at fifty nodes or more runs on hope. The operator hopes the key rotation propagated. The operator hopes the OTA update reached every device. The operator hopes none of the offline sites have drifted out of compliance. Hope is not an operational discipline. The transition from hope to a tracked operational posture is what this chapter specifies.

The single-node playbooks in Part IV embed the human-at-the-node assumption in their structure. Chapter 17 walks you through building a node and watching it sync — the verb *watching* presupposes a screen with a person in front of it. Chapter 19 deploys to managed endpoints where IT can see the daemon running in Event Viewer. Chapter 20 designs UX for a user who interacts with the application through a mouse and keyboard. None of those chapters generalises to a deployment of forty headless devices in field offices that nobody visits between maintenance windows. The single-node model breaks at the moment the operator-to-node ratio crosses one.

Fleet management names four operational responsibilities the existing architecture does not specify at fleet scale. **Provisioning** is the mechanism by which a new node is initialised with its identity, keys, and initial configuration without a human in the loop — replacing Chapter 17's interactive onboarding with a manufacturing or flash-time ceremony. **Key rotation orchestration** extends Chapter 15's per-node rotation to the fleet context, with a propagation window, a straggler tracker, and an escalation path for nodes that fall behind. **OTA update coordination** delivers verified, rollback-capable software updates to headless devices over patchy connectivity. **Fleet observability** answers, at any moment, the question: what is the security posture and operational health of every node in the fleet?

Each responsibility is defined by the silent failure mode it eliminates. Without provisioning ceremonies, nodes carry keys generated outside the fleet's trust boundary — and the operator cannot tell which keys are which. Without key rotation orchestration, a partial propagation across two hundred nodes leaves the operator unable to identify which thirteen are behind. Without OTA coordination, a critical security patch reaches some unknown subset of the fleet and leaves the rest exposed. Without fleet observability, an offline node is indistinguishable from a compromised node — both manifest as silence on the relay.

The architectural claim is specific. Fleet management is the mechanism that converts these four classes of silent failure into observable, tracked, escalatable operational events. The architecture does not make fleet operations easy. It makes fleet failures *visible*. Visibility is the prerequisite for every other operational discipline — incident response, compliance evidence, capacity planning, customer support — and it is the property that single-node tooling cannot deliver at fleet scale.

Cross-references for the integration this chapter makes with the existing architecture: Chapter 15 §Key Rotation and Revocation specifies the per-node rotation model that Section 21.3 orchestrates at fleet scale; Chapter 19 §Admin Tooling specifies the enterprise admin panel that Section 21.5 extends to fleet size; Chapter 11 §The UI Kernel specifies the `SunfishNodeHealthBar` that the fleet dashboard generalises to a fleet-level health view. Forward-looking integrations: the per-node performance contracts in extension #43 surface as the performance-posture dimension in fleet observability; the recovery-event audit trail substrate in extension #48 carries fleet rotation events through the same `Sunfish.Kernel.Audit` log.

Fleet management is not a derivation from the v13 or v5 source papers. It is a new architectural commitment surfaced through the universal-planning review of design-decisions §5 #11. The papers establish the local-first node architecture; this chapter extends that architecture into the operational domain the papers did not address. Where the per-node primitives in Part III have a direct lineage to the source material, the fleet primitives in this chapter are first-class additions to the architecture — committed in this volume and validated against the operational literature on Mobile Device Management (MDM) [1] [2] [3], embedded OTA systems [5], and fleet observability practice [8].

**FAILED conditions:**

- **Any node completes key rotation without the fleet operator knowing it succeeded or failed.** The propagation tracker in Section 21.3 is the substrate; if confirmation events do not reach the fleet registry, the primitive has failed.
- **Any OTA update reaches less than the operator-configured minimum propagation threshold without escalation.** The staged rollout and rollback mechanisms in Section 21.4 must surface a stalled rollout as an alert, not as a quiet partial success.
- **Any new node enters the fleet with a key bundle derived outside the fleet's provisioning ceremony.** The enrollment receipt in Section 21.2 is the audit artifact; an unprovisioned node operating in the fleet is a trust-boundary violation.
- **Fleet observability shows health metrics that are more than the operator-configured staleness window out of date.** The heartbeat protocol in Section 21.5 is the substrate; stale metrics misrepresent the fleet's state and make every other operational decision unreliable.
- **A stale node — behind the current key rotation epoch by more than one epoch — continues to receive new events from the relay without quarantine.** The straggler quarantine path in Section 21.3 is the enforcement; a node that participates in sync under an obsolete epoch is the definition of a silent compliance failure.

The kill trigger for this primitive is a FAILED condition that recurs across three consecutive technical-review passes against the same gate. A single intermittent failure is a defect. A persistent failure across reviews signals that the primitive's design has not converged.

---

## 21.2 Sub-pattern 11a — Provisioning at flash time

Without provisioning ceremonies, nodes carry keys generated outside the fleet's trust boundary, and the operator cannot tell — at any later moment — which keys came from where. The fleet's security posture starts at the moment of node creation. If you cannot attest to the conditions under which a node was initialised, you cannot make any other security claim about that node downstream.

A fleet provisioning ceremony is a controlled, attested initialisation event that produces a signed node identity bundle: the device keypair, the initial KEK (Key Encryption Key) bundle for the node's assigned fleet segment, the initial sync configuration, and the enrollment receipt. The ceremony executes in a trusted environment — a manufacturing line, a CI/CD pipeline, a deployment staging area — never in the field. The trust boundary of the fleet starts inside the ceremony and propagates outward through the enrollment receipts the ceremony emits.

Choose one of three provisioning models. The choice determines the ceremony's mechanics, the device hardware requirement, and the fallback path for field replacement.

**Pre-provisioned hardware.** The device leaves the factory with a node identity burned in at manufacturing time. The device keypair is generated by a Hardware Security Module (HSM) during manufacturing and never leaves the device. The public key registers with the fleet registry; the private key seals to the device's Secure Enclave or Trusted Platform Module (TPM) [4]. This is the highest-assurance model. It is appropriate for regulated-tier fleets — healthcare devices under HIPAA, financial-services edge devices, regulated-industry telematics. It is also the most expensive model. Manufacturing-line integration with an HSM and a fleet-registry service costs real engineering effort that smaller deployments cannot amortise.

**Zero-touch deployment.** The device arrives factory-reset. When it first connects to a trusted network — or to a USB provisioning tool an operator carries to the deployment site — it receives its node identity and initial key bundle through an authenticated provisioning protocol. The provisioning server verifies the device's hardware attestation [1] [2] [3] before issuing the bundle. This model accommodates field replacement: a failed device is swapped for a stock unit, the unit goes through zero-touch on first connection, and the fleet registry records the replacement event with a chain-of-custody link to the original device. This is the default model for most production fleets. The provisioning protocol borrows directly from Apple Business Manager [1], Google Zero-Touch Enrollment [2], and Windows Autopilot [3] — three documented systems with extensive deployment experience.

**Operator-mediated enrollment.** For smaller fleets or deployments without TPM or Secure-Enclave support, an operator manually completes a reduced provisioning ceremony — typically a QR-code or NFC exchange that transfers the initial key bundle under the operator's credential. The enrollment receipt is the audit artifact: it carries the operator's identity, the timestamp, and the attestation that the operator vouches for the device's initial state. This is the fallback, not the default. Use it when hardware constraints or fleet size make zero-touch infeasible, and never in regulated-tier deployments where the audit trail must trace to hardware attestation rather than operator credential.

```csharp
// illustrative — not runnable (Sunfish.Foundation.Fleet pre-1.0)
builder.Services.AddSunfishFleetProvisioning(options =>
{
    options.Model = ProvisioningModel.ZeroTouch;
    options.FleetRegistryEndpoint = "https://fleet.internal.corp/registry";
    options.SegmentAssignment = "construction.region.west";
    options.EnrollmentReceiptStore = EnrollmentReceiptStore.FleetRegistryAndLocal;
});
```

Every provisioning event produces a signed enrollment receipt. The receipt carries the device's public key, the fleet segment assignment, the key bundle epoch at provisioning time, the provisioning operator's identity (in the operator-mediated model), the HSM or platform attestation (in the hardware models), and the UTC timestamp. The receipt stores in two places: the fleet registry on the operator side, and the node's own audit log on the device side. The dual storage is deliberate. A receipt held only by the fleet registry can be questioned by an auditor — "how do you know the device received this?" — and a receipt held only by the device can be questioned by the operator — "how do you know this device is supposed to be here?" The matched pair answers both questions.

The enrollment receipt is also a chain-of-custody record in the sense extension #9 develops more fully. The device's identity is attested at a specific time, under a specific key authority, by a specific operator or hardware path. Subsequent operations on the device — key rotations, software updates, role changes — extend the chain. The provisioning receipt is the genesis record. Without it, the chain has no anchor.

Large fleets may organise nodes into segments. A segment is a sub-population of the fleet that shares key material, sync scope, and update channels. The forty-site construction deployment from the chapter introduction divides naturally into regional segments — west, central, east — each with its own KEK bundle and its own update schedule, so that an outage or a security incident in one region does not cascade across the others. Segmentation is also the unit of compliance: a regulated-tier segment can run under stricter key-rotation cadence and tighter OTA gating than a standard-tier segment, without forcing the regulated tier's overhead onto the rest of the fleet.

The provisioning ceremony assigns the node to a segment. The assignment is cryptographically bound to the node's identity bundle: the segment KEK is wrapped under the device's public key at provisioning time, and the node cannot decrypt KEKs from other segments. Segment re-assignment requires a re-provisioning ceremony — not an in-band configuration change. This is intentional. An operator who could re-segment a node by editing a config file could also exfiltrate cross-segment data by a sequence of re-segmentations. Re-provisioning closes that path: a re-segmented node has a new identity bundle, a new enrollment receipt, and an audit trail that records the re-segmentation event explicitly.

`Sunfish.Foundation.Fleet` owns the provisioning ceremony, the enrollment receipt schema, and the fleet registry client. It coordinates with `Sunfish.Kernel.Security` for the cryptographic primitives — keypair generation, KEK wrapping, signature operations — and with `Sunfish.Foundation.Recovery` for the re-provisioning path that re-uses key-recovery patterns when a device is replaced or re-segmented. Cross-reference to Chapter 15 §Device and User Identity for the single-node device keypair model that fleet provisioning extends, to Chapter 17 §QR-Code Onboarding for the interactive enrollment ceremony that operator-mediated enrollment replaces in headless deployments, and to Chapter 19 §Admin Tooling for the fleet registry the operator manages.

The provisioning model is a procurement-time decision, not a runtime decision. Specify it in your fleet's deployment plan before the first device is ordered. Adding HSM-based provisioning to a fleet that was originally provisioned through operator-mediated enrollment is a re-provisioning of the entire fleet — an expensive operation. Specify it once, specify it correctly, and document the choice in the fleet's compliance manifest.

---

## 21.3 Sub-pattern 11b — Fleet-scale key rotation orchestration

Chapter 15 §Key Rotation and Revocation specifies key rotation as a local operation: one node, one rotation event, immediate effect. At fleet scale, that model breaks. A rotation is no longer a single event — it is a coordinated operation across hundreds of nodes, with a propagation window, a tracker for which nodes have confirmed, and an escalation path for nodes that fall behind. The single-node model is correct. It is also insufficient.

A fleet key rotation announces as a *rotation epoch* event. The announcement is a signed message that names the new KEK bundle, the epoch identifier, the propagation deadline, and the fleet segment scope. The announcement travels through the relay to all nodes in the segment over the standard sync channel. The default propagation window is 72 hours. Configure tighter windows for regulated-tier segments — 24 hours for healthcare or financial-services segments where compliance requires faster compromise containment — and looser windows for connectivity-constrained segments where 72 hours is insufficient to reach all field nodes. Configure the window before the first rotation, not during one.

Each node receives the announcement, generates the new KEK derivation locally, and runs the per-node DEK (Data Encryption Key) re-wrapping job specified in Chapter 15 §Post-Revocation Key Rotation. The re-wrapping completes when every DEK in the local document set has been re-wrapped under the new KEK. The node then emits a *confirmation event* — a signed acknowledgment that travels back to the fleet registry and records the node's transition to the new epoch. Confirmation is the propagation tracker's primary signal. A node that has emitted a confirmation event is current; a node that has not is either offline, in progress, or stalled.

Re-wrapping must be idempotent. A node that receives the epoch announcement twice — through a relay retry, a network partition heal, or a duplicated message — must not double-wrap its DEKs. Idempotence is a `Sunfish.Kernel.Security` invariant, not a fleet-layer concern, and the technical-review pass for this chapter must confirm the kernel's re-wrapping job preserves it. The fleet layer's job is to track confirmations, not to suppress duplicate announcements.

A node that has not confirmed by the propagation deadline is a *straggler*. Straggler handling escalates through three named levels.

**Warning.** The node flags in fleet observability with a staleness indicator. The operator sees the node listed in the dashboard as "Pending epoch [N], last seen [T]". The operator receives a notification through the configured alert channel. No operational change occurs to the node itself. The node continues to operate under its existing epoch and continues to receive new events from the relay. The warning level is the soft signal — the operator's window to investigate before automatic enforcement triggers.

**Read-only quarantine.** After a second configurable deadline — typically 24 hours after the initial propagation deadline for regulated-tier segments, 7 days for standard-tier — the straggler node moves to read-only mode. The relay stops forwarding new events under the new epoch to the node. The node continues to serve its local data to the local user, but it receives no new updates from peers and cannot publish new events that would be accepted under the new epoch. This is the offline-revocation circuit breaker from Chapter 15 §Offline Node Revocation and Reconnection extended to the rotation-epoch context. The fleet-layer mechanism is the same circuit-breaker primitive, applied to a different trigger condition.

**Decommission escalation.** After a third deadline — typically 30 days beyond the initial propagation window, configurable per segment — the fleet registry fires a decommission escalation event. The event records in the audit trail. The operator receives an explicit notification. The operator then decides: attempt a re-provisioning ceremony if the device is reachable, or retire the node from the fleet. The architecture does not make the decision for the operator. It surfaces the choice with a defined timeline and a complete record of what has happened to the node since the rotation announcement.

The 30-day default is deliberate. It is long enough to accommodate seasonal connectivity gaps — construction sites in winter, agricultural deployments in dormant seasons — while short enough that a genuinely abandoned node does not accumulate indefinitely as a fleet liability. Tighter values are appropriate for regulated-tier deployments; looser values for fleets with documented multi-month offline phases. Whatever value you choose, document it in the segment configuration and in the compliance manifest. An auditor who reads "30-day decommission escalation" should be able to find the configured value in the fleet registry, not infer it from the architecture documentation.

Fleet key rotation cadence is deployment-class dependent. For a regulated-tier fleet — HIPAA, PCI-DSS, SOX [7] — rotation runs quarterly at minimum. For a standard-tier fleet, annually or on security-incident trigger. For a fleet that includes a node flagged under the endpoint-compromise primitive (extension #47, forward-looking), an out-of-band rotation triggers on the segment that included the compromised node, with the decommission escalation timeline compressed to the regulated-tier value regardless of the segment's normal classification.

```csharp
// illustrative — not runnable (Sunfish.Foundation.Fleet pre-1.0)
builder.Services.AddSunfishFleetKeyRotation(options =>
{
    options.PropagationWindow = TimeSpan.FromHours(72);
    options.QuarantineDeadline = TimeSpan.FromDays(7);
    options.DecommissionEscalation = TimeSpan.FromDays(30);
    options.Cadence = RotationCadence.Quarterly;  // regulated-tier
});
```

`Sunfish.Foundation.Fleet` owns the epoch announcement, the propagation tracker, the straggler registry, and the escalation events. `Sunfish.Kernel.Security` owns the per-node re-wrapping job. The separation is deliberate: the fleet layer monitors and orchestrates; the kernel layer executes. Cross-reference to Chapter 15 §Key Rotation and Revocation for the per-node rotation specification, Chapter 15 §Collaborator Revocation (extension #45) for the revocation circuit breaker the straggler quarantine path re-uses, and extension #48's recovery-event audit trail for the `Sunfish.Kernel.Audit` substrate that records fleet rotation events alongside per-node recovery events.

The most common failure mode is not the rotation itself — the cryptographic operations are reliable when implemented correctly. The most common failure mode is the operator who configured a 72-hour window for a fleet with weekly connectivity at half its sites. The propagation deadline expires, two-thirds of the fleet enters quarantine, and the operator scrambles to extend the deadline retroactively — which the architecture does not support, because retroactive extension would create epoch ambiguity in the audit log. Configure the propagation window against your fleet's *worst-case* connectivity profile, not its average. The window is not a target. It is a contract.

---

## 21.4 Sub-pattern 11c — OTA update coordination

OTA software updates to headless fleet nodes are one of the highest-risk operations in a local-first fleet deployment. A desktop update is interactive: the user is present, the installer is visible, the failure path is a dialog box the user can read. A fleet OTA is unattended, runs across patchy connectivity, and cannot require a human to verify it completed. A bug in the update logic affects every node in the rollout, simultaneously, with no human at any of them to catch the failure before it propagates.

The mitigation is structural: a fleet OTA is a *staged*, *verified*, and *rollback-capable* operation, never a simultaneous push. The staging gives you intervention windows. The verification refuses bad bundles. The rollback recovers from bad bundles that pass verification but fail in production. Each property is non-negotiable; the absence of any of the three converts a routine update into a fleet-wide incident.

The update bundle is a signed artifact. It carries the new software version, a cryptographic hash, the signing key's certificate chain (rooted in the fleet operator's release-signing key per Chapter 19 §Code Signing and Notarization), the delta patch or full installer, and the update metadata: target segment, minimum rollback version, compatibility matrix. The bundle is content-addressed. The node verifies the hash before applying. RAUC [5] and Mender [9] both implement the same content-addressed signed-bundle pattern; the architecture borrows directly from their proven approaches.

Fleet OTA does not push simultaneously to all nodes. The staged rollout proceeds in three phases.

**Canary stage.** One to five percent of nodes in the segment receive the update first. The fleet registry monitors canary nodes for error rates, sync stability, and performance-contract violations (extension #43) over a configurable soak window. The default canary soak is 24 hours for standard-tier segments, 72 hours for regulated-tier segments where compliance requires longer observation before broader deployment. The soak window is the operator's primary signal: if the canary nodes show degraded telemetry — elevated error rates, sync failures, performance regressions — the rollout halts before it reaches the rest of the segment. Canary selection is not random in the strict sense. The fleet registry selects canary nodes for diversity: a mix of hardware platforms, geographic regions, and connectivity profiles, so that the canary stage exercises the failure modes the broader rollout would encounter.

**Wave expansion.** If the canary soak passes, the rollout expands in configurable waves. The default wave schedule: 25%, 50%, 100%, with a 24-hour soak window between waves. The fleet registry continues to monitor the same telemetry — error rates, sync stability, performance posture — and halts the rollout if any wave's telemetry degrades. Wave sizes and soak windows are operator-configurable per segment. A regulated-tier segment may run 10%, 25%, 50%, 100% with 48-hour holds; a standard-tier segment may compress to two waves with 12-hour holds. The architecture does not prescribe the schedule. It enforces the staging.

**Automatic rollback.** If any wave's error rate exceeds the operator-configured threshold during soak, the rollout halts and rollback initiates. Nodes that received the update receive a rollback bundle. The rollback bundle is *pre-signed at the same time as the update bundle* — the operator cannot rollback without a pre-committed rollback artifact. This constraint is deliberate. An ad-hoc rollback that signs at incident time depends on the incident-response infrastructure being available; pre-signing the rollback at release time means the rollback path works even if the release-signing infrastructure is unavailable during the incident. Rollback nodes verify the rollback bundle's signature and version constraint exactly as they verified the original update bundle. A rollback that lacks proper signing or that targets an incompatible version is refused. The fleet registry records the rollback event in the audit trail, including the trigger metric, the threshold, and the affected node set.

Before applying any update, every node verifies four gates. **First**, the bundle's hash matches the manifest. **Second**, the signing certificate chain terminates at the fleet's trusted root. **Third**, the update version is greater than the installed version — downgrade attacks are refused, even if the downgrade bundle is signed correctly, because a properly signed older bundle could re-introduce a known vulnerability. The rollback bundle is the only exception; it carries an explicit rollback flag that the verification logic recognises as a downgrade authorisation. **Fourth**, the node's current hardware and software environment meets the compatibility matrix declared in the bundle metadata. Any gate failure aborts the update and logs a signed failure event the fleet registry aggregates.

```csharp
// illustrative — not runnable (Sunfish.Foundation.Fleet pre-1.0)
builder.Services.AddSunfishFleetOtaUpdates(options =>
{
    options.CanaryPercentage = 5;
    options.CanarySoakWindow = TimeSpan.FromHours(24);
    options.Waves = new[] { 25, 50, 100 };
    options.WaveSoakWindow = TimeSpan.FromHours(24);
    options.RollbackErrorRateThreshold = 0.02;  // 2% error rate triggers rollback
    options.RequirePreSignedRollback = true;
});
```

For nodes that are periodically offline or air-gapped, the update bundle queues in the fleet relay's update cache. When the node reconnects, it fetches the pending bundle and applies it at the next maintenance window. The fleet registry tracks pending-update nodes separately from straggler nodes; the distinction matters for compliance reporting. Software version is an asset attribute. Out-of-date nodes in a regulated fleet are an audit finding regardless of whether the operator considers them "stragglers" or "pending updates" — but the operator's response differs. A straggler is a node that should have updated and did not. A pending-update node is a node that has not yet had the opportunity to update. The dashboard surfaces the distinction; the audit-log entry preserves it.

`Sunfish.Foundation.Fleet` owns the update bundle manifest, the staging configuration, the rollout tracker, and the rollback bundle management. The signing pipeline that produces the bundle and the rollback artifact is part of `Sunfish.Kernel.Security` and reuses the release-signing infrastructure described in Chapter 19 §Code Signing and Notarization. Cross-reference also to Chapter 19 §Air-Gap Deployment for the internal update server pattern that this sub-pattern extends from per-deployment to per-fleet scale.

The most expensive failure mode in fleet OTA is the bundle that passes the four verification gates but fails in production load. Hash verification cannot detect a logic bug. Signature verification cannot detect a memory leak that surfaces only after eight hours of production traffic. The four gates ensure the bundle is what the operator intended; the staged rollout and the automatic rollback ensure that an unintended consequence of that bundle does not propagate to the entire fleet before the operator notices. The four gates are necessary. They are not sufficient. The staging is what makes the operation safe.

---

## 21.5 Sub-pattern 11d — Fleet observability

Fleet observability answers a single question. *What is the security posture and operational health of every node in the fleet, at any moment, without SSH access to individual nodes?* If you cannot answer that question in under thirty seconds for any node in your fleet, fleet observability has failed regardless of what dashboards exist. The answer must be current, signed, and complete.

Each node emits a signed health heartbeat to the fleet registry on a configurable interval. The default is five minutes for connected nodes; on-reconnect for nodes returning from offline. The heartbeat carries the node's current key rotation epoch, the current software version, the sync daemon status (Running, Degraded, Stopped), the CRDT (Conflict-free Replicated Data Type) engine's last operation timestamp, the disk utilisation tier (Normal, Warning, Critical), the performance-contract status per extension #43 (Compliant, Degraded, Violated), and any queued circuit-breaker events from Chapter 15. The heartbeat travels through the same encrypted channel as the standard sync traffic and signs with the node's device key. A heartbeat that fails signature verification is discarded by the fleet registry and surfaces as an integrity-failure alert.

The heartbeat contract has a privacy implication the technical-review pass must confirm. The fleet registry knows each node's software version, key epoch, and sync state. This is metadata, not content — the registry cannot read the node's data — but it is a new metadata trust boundary that did not exist in the per-node architecture. Document the boundary explicitly in the fleet's compliance manifest. The Bridge relay's data-minimisation invariant (Chapter 14 §Data Minimisation Invariant) applies to data; the fleet registry's metadata accumulation requires its own minimisation policy. Default policy: heartbeats expire from the registry after 30 days; aggregated fleet-level summaries persist indefinitely. The technical-review pass must confirm this policy is consistent with the deployment's compliance regime.

The fleet dashboard surfaces four dimensions for every node. **Security posture** shows the current key epoch versus the fleet epoch, whether the node is within the propagation window, and any pending revocation events from extension #45. **Software currency** shows the installed version versus the fleet's target version, pending OTA update status, and rollback eligibility. **Sync health** shows the last successful gossip round, peer count, relay connectivity status, and the last CRDT operation received and emitted. **Performance posture** shows performance-contract compliance from extension #43 and the last budget-violation event with its timestamp.

The four dimensions are not arbitrary. Each maps to a class of operational decision the operator needs to make. Security posture answers *can this node be trusted right now?*. Software currency answers *is this node patched against the latest known issues?*. Sync health answers *is this node still part of the working fleet?*. Performance posture answers *is this node delivering the user experience the architecture committed to?*. Together, the four dimensions are the complete operational picture. A dashboard that omits any of them produces an incomplete answer.

Aggregation matters as much as per-node detail. The fleet registry aggregates heartbeats into fleet-level summaries. Alerts fire on configurable thresholds: more than 5% of nodes straggling on key rotation, any node on a software version older than three releases, more than 10% of nodes showing sync-health degradation simultaneously (which usually indicates a relay issue rather than per-node issues). Fleet-level alerts are distinct from per-node escalations. A single offline node is operational noise. Ten percent of the fleet going offline simultaneously is a relay incident. The aggregation surfaces the systemic signal that per-node monitoring misses. The Prometheus exposition format [8] is the model the heartbeat protocol borrows from for its structured-telemetry shape; AWS IoT Fleet Indexing [10] documents the same pattern for fleet-scale aggregation.

For regulated-tier fleets, the fleet registry exports a signed compliance snapshot on demand. The snapshot carries every node's software version, key epoch, last-health-event timestamp, and segment assignment, in a format that satisfies SOC 2 audit-evidence requirements [7] and HIPAA risk-assessment documentation [11]. The export is point-in-time, signed, and content-addressed — an immutable record of the fleet's posture at the moment of the export. Note the SOC 2 scope correctly: SOC 2 Type II requires evidence of controls operating *over time*, not a single point-in-time snapshot. The compliance export is a point-in-time artifact; a *series* of exports forms the time-series evidence that SOC 2 Type II requires. State this in your compliance documentation. Auditors who read "the system supports SOC 2" without seeing the time-series caveat will infer something the architecture does not deliver.

```csharp
// illustrative — not runnable (Sunfish.Foundation.Fleet pre-1.0)
builder.Services.AddSunfishFleetObservability(options =>
{
    options.HeartbeatInterval = TimeSpan.FromMinutes(5);
    options.StalenessWindow = TimeSpan.FromMinutes(15);
    options.ComplianceExportFormat = ComplianceExportFormat.SignedJson;
    options.AlertThresholds.KeyRotationStraggling = 0.05;     // 5%
    options.AlertThresholds.SyncHealthDegraded = 0.10;        // 10%
});
```

A node that has not emitted a heartbeat within the staleness window flags as offline rather than unhealthy. *Offline is an expected state in a local-first fleet.* The fleet dashboard distinguishes five states: **Online (current)** — heartbeat received within the window, current epoch, current software version. **Online (stale heartbeat)** — heartbeat overdue but node still reachable, possibly degraded. **Offline (last seen N hours ago, posture unknown)** — node has not reported within the staleness window; last known posture displayed for context. **Quarantined (stale epoch)** — node is in read-only quarantine pending key rotation completion. **Decommissioned** — node has exceeded the decommission escalation deadline; operator action required.

The five states matter. An offline node is not a security problem unless it is also behind on key rotation. A quarantined node is a known operational state with a defined recovery path. A decommissioned node is a fleet liability that the operator has been notified about. Conflating these states — showing them all as "unhealthy" or "needs attention" — turns the dashboard into noise the operator stops checking. The dashboard's job is to present the operational state in language that maps to the operator's decision tree, not in language that reflects the architecture's internal categories.

`Sunfish.Foundation.Fleet` owns the heartbeat protocol, the fleet registry, the dashboard aggregation layer, and the compliance export. Cross-reference to Chapter 11 §The UI Kernel for the `SunfishNodeHealthBar` per-node health indicator that fleet observability generalises to a fleet-level analogue, Chapter 14 §Sync Daemon Protocol for the gossip-round status that fleet health tracks, and extension #43 for the performance-posture dimension.

---

## 21.6 The fleet failure scenario

The deployment was 200 nodes. A regulated-tier construction-management fleet across a mid-sized contractor's project portfolio. Quarterly key rotation was the cadence specified in the segment's compliance manifest. The propagation window was 72 hours — the regulated-tier default. The operator scheduled the rotation for a Monday morning, expecting most sites to be online and the propagation window to clear by Thursday.

By Monday evening, 183 nodes had confirmed receipt of the new epoch and successfully completed re-wrapping. Seventeen nodes had not. Fifteen of those were sites in active excavation phases — buried in dirt, no connectivity, expected to come back online within a week. Two were sites the operator had not realised were offline. The propagation window remained open. The fleet dashboard listed all seventeen nodes as "Pending epoch [N+1], last seen [varies]" — a routine status, not an alert.

Wednesday morning, the propagation deadline passed. The fifteen excavation-phase nodes were still offline. The two unknown-offline nodes had also not appeared. Straggler quarantine activated automatically. The relay stopped forwarding new events under the new epoch to the seventeen straggler nodes. The fleet dashboard transitioned them to "Quarantined (stale epoch)". The operator received a notification. The notification was not an emergency — it was the expected outcome of a routine rotation against a fleet with known offline sites. The operator acknowledged the notification and continued working.

Eight days later, fourteen of the seventeen offline nodes came back online. They received the epoch announcement on reconnection, completed re-wrapping locally, emitted confirmation events, and exited quarantine. The fleet dashboard transitioned them to "Online (current)". Three nodes remained offline — one excavation site that had run later than scheduled, and the two nodes the operator had not initially identified as offline. The dashboard now showed them as "Offline (last seen 8 days ago, straggler epoch)" — a status that escalated their visual prominence and added them to the operator's daily review.

Thirty days after the original rotation announcement, the three stragglers had not reconnected. The fleet registry fired a decommission escalation event. The operator received an explicit notification: three nodes in the west-region segment had exceeded the decommission deadline and required action. The audit log recorded the escalation, the timestamps, and the segment context. The operator dispatched a field technician to the excavation site, found the node had been damaged during equipment movement, and re-provisioned a replacement device through the zero-touch flow. The two unknown-offline nodes turned out to be a discontinued site the contractor had forgotten to retire and a node in a trailer that had been disconnected from power for a month. The operator retired both from the fleet through the explicit decommission flow, recording the reason in the audit trail.

The rotation was a success. Three nodes were lost — recovered, retired, replaced — and the remaining 197 nodes operated under the new epoch with a complete audit trail of what had happened to each.

What would have happened without fleet management. The seventeen offline nodes would have continued to receive relay events under the old epoch until the relay's backward-compatibility window expired — perhaps six weeks, perhaps six months, depending on the operator's retention policy. At that point, those nodes would have silently lost sync. No quarantine. No decommission escalation. No audit trail. The operator would have discovered the problem only when a site-office user called the helpdesk to report that their construction-management application had not updated in several weeks. The investigation would have taken days. The compliance posture would have been ambiguous: were the nodes offline by choice, by failure, by compromise? The audit log would not have been able to distinguish.

Fleet management does not make the rotation easier. It makes the rotation's failure modes *visible*. The seventeen straggler nodes, the three persistent stragglers, the equipment-damaged site, the disconnected trailer, the discontinued site — every one of them surfaced as a tracked operational event with a defined response path. The architecture did not prevent the failures. It converted each failure from a silent state into an observable, escalatable, auditable event the operator could act on within a defined timeline.

That is the chapter's claim. It is not that fleet management makes operations easy. It is that fleet management makes operations *honest*. An operator who runs a fleet with the primitives in this chapter knows what is happening to every node, knows when something goes wrong, and has the audit trail to prove what was known when. An operator who runs a fleet without these primitives knows what they hope is true, and discovers the truth at a delay measured in weeks or months. The difference is the architecture's commitment to making fleet operations observable rather than merely possible.

Cross-reference to Chapter 4 §Choosing Your Architecture for the deployment-class filter that identifies fleet-scale headless deployments as requiring this chapter, and to the Part V framing as the operational coda. Part IV teaches you to ship. Part V teaches you to sustain.

---

## References

[1] Apple Inc., "Apple Business Manager User Guide," Apple Inc., 2025. [Online]. Available: https://support.apple.com/guide/apple-business-manager/welcome/web

[2] Google LLC, "Zero-touch enrollment for IT admins," *Google Workspace Admin Help*, 2025. [Online]. Available: https://support.google.com/a/answer/7514005

[3] Microsoft Corporation, "Windows Autopilot overview," *Microsoft Learn*, 2025. [Online]. Available: https://learn.microsoft.com/en-us/mem/autopilot/overview

[4] Trusted Computing Group, "TPM 2.0 Library Specification," TCG, 2019. [Online]. Available: https://trustedcomputinggroup.org/resource/tpm-library-specification/

[5] RAUC Project, "RAUC — Robust Auto-Update Controller," 2024. [Online]. Available: https://rauc.readthedocs.io

[6] National Institute of Standards and Technology, "Guide to Industrial Control Systems (ICS) Security," SP 800-82 Rev. 3, 2023. [Online]. Available: https://csrc.nist.gov/publications/detail/sp/800-82/rev-3/final

[7] American Institute of Certified Public Accountants, "Trust Services Criteria," 2022 edition, AICPA, 2022.

[8] Prometheus Authors, "Exposition Formats," *Prometheus Documentation*, 2024. [Online]. Available: https://prometheus.io/docs/instrumenting/exposition_formats/

[9] Northern.tech AS, "Mender Documentation," *mender.io*, 2025. [Online]. Available: https://docs.mender.io/

[10] Amazon Web Services, "AWS IoT Device Management — Fleet Indexing," *AWS Documentation*, 2025. [Online]. Available: https://docs.aws.amazon.com/iot/latest/developerguide/iot-indexing.html

[11] U.S. Department of Health and Human Services, "HIPAA Security Rule," 45 CFR Part 164, 2003 (as amended 2013). [Online]. Available: https://www.hhs.gov/hipaa/for-professionals/security/
