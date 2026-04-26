# Appendix D — Testing the Inverted Stack

<!-- icm/prose-review -->

<!-- Target: ~2,200 words -->
<!-- Source: v13 §15 -->

---

The failure modes local-first architectures ship with are the ones that look unlikely until they happen. Silent CRDT divergence. WAL corruption after power loss. Lease split-brain after a half-open TCP timeout. Ciphertext leakage through an audit-log side channel. This appendix exists to make those failure modes impossible to miss before a customer finds them.

Five testing levels govern this architecture. Each carries mandatory pass conditions before first production release. Level 1 and Level 2 run on every pull request. Level 3 runs nightly. Level 4 runs weekly or before release. Level 5 runs in staging before each major release. Each scenario specifies setup conditions, the action to perform, and the expected outcome. If a scenario has no pass condition, it is not a test.

---

## Section 1: The Five-Level Testing Pyramid

### Level 1 — Property-Based Tests

CRDT operations have four mathematical properties that example-based tests cannot verify reliably:

- **Convergence** — all replicas eventually agree, regardless of operation order.
- **Idempotency** — applying the same operation twice produces the same result as applying it once.
- **Commutativity** — concurrent operations reach the same final state regardless of application order. For operation-based CRDTs, commutativity is sufficient for convergence; for state-based CRDTs (which include both Yjs and Loro), convergence is guaranteed instead by the merge function forming a join-semilattice — commutativity of the merge in the traditional sense is implied but stated differently. Shapiro et al. (2011) is the citable reference for the formal distinction; see Appendix C [8].
- **Monotonicity** — the CRDT state never shrinks; no operation silently removes information.

Property-based frameworks generate thousands of random operation sequences automatically and report the minimal failing case when a property is violated. Use FsCheck (.NET) or fast-check (JavaScript). Configure the framework to generate at least 10,000 random operation sequences per property per test run. This is an authorial recommendation calibrated against production experience. FsCheck's default of 100 is insufficient for CRDT coverage. 10,000 is where empirical bug-discovery returns flatten for most CRDT engines. Reduce the count only if profiling identifies it as a bottleneck, and verify that the reduction does not eliminate the sequences that catch real failures.

Do not skip Level 1. An example-based CRDT test suite that passes is not evidence that the CRDT is correct. It is evidence that the specific sequences you tested are correct.

### Level 2 — Integration Tests (Real Dependencies)

The sync handshake, capability negotiation, and delta streaming must run against a real daemon process. Mocking the sync daemon produces tests that pass when the real integration is broken. The mock encodes your assumptions about how the daemon behaves — and those assumptions are exactly what you need to test.

Use Testcontainers (.NET) to spin up a real local-node instance per test suite. Run the full five-step handshake: HELLO → CAPABILITY_NEG → ACK → DELTA_STREAM → GOSSIP_PING. Assert on the CRDT state after delta exchange, not on the wire messages. The state is what matters. The message sequence is how you get there.

Testcontainers requires Docker. Add Docker to your CI environment before adding Level 2 tests.

### Level 3 — Fault Injection in CI

Network partition, packet loss, and node crash must be exercised in CI, not only in staging. Staging runs fault injection infrequently. Production incidents originate in the gap between a possible fault and a tested one.

Use Testcontainers with toxiproxy (or an equivalent network proxy) to inject faults programmatically. Three scenarios are mandatory at this level:

- Node crashes mid-handshake. Assert that the peer recovers, retries, and reaches consistent state.
- Relay becomes unreachable during DELTA_STREAM. Assert that the sender queues deltas locally and retransmits on reconnect (the CRDT operation log provides this durability — see Chapter 14).
- GOSSIP_PING misses three consecutive intervals due to packet loss. Assert that the node enters a degraded-but-consistent state and recovers without manual intervention.

The pass condition for every fault injection test is not "the system does not crash." It is "the system recovers to a consistent CRDT state identical to what it would have been without the fault."

### Level 4 — Deterministic Simulation

Mixed-version nodes, epoch transitions while a node is offline, and Flease edge cases cannot be tested reliably with real time. Real-time tests are non-deterministic. A lease expiry that takes 30 seconds in production cannot be exercised in CI at real speed without making the test suite unusable. A simulation harness with a controllable clock and deterministic network scheduling makes these scenarios fast, repeatable, and exhaustive.

No off-the-shelf simulation harness implements this protocol. Teams implementing this architecture must build one. The minimum viable harness implements:

1. **Controllable virtual clock.** A global monotonic clock the test driver advances in discrete ticks; all timeouts, lease expiries, and retry intervals resolve against this clock rather than wall-time.
2. **Deterministic message scheduler.** A pluggable scheduler that orders messages across simulated nodes. The test driver controls delivery order; the scheduler can delay, reorder, or drop messages per-test.
3. **In-process node factory.** Boot N node instances inside the test process, each with an isolated SQLCipher store, wired to the deterministic scheduler rather than real sockets.
4. **Invariant assertions.** Hooks that verify CRDT convergence, ledger balance, lease exclusivity, and epoch monotonicity after any scheduler-driven sequence.

Expect one to three engineer-weeks of effort to build the MVP harness, depending on protocol familiarity. The investment buys failure modes that cannot be caught any other way — production-quality lease-expiry, epoch-transition, and mixed-version coverage. Design the harness against the Appendix A wire protocol specification before implementation. A harness built on an incomplete understanding of the handshake simulates the wrong system.

Three scenario families belong at Level 4: mixed-version node sync (one node at schema N, one at schema N-1), epoch transitions while a node is offline, and Flease edge cases such as a lease holder disconnecting mid-write. Each of these requires precise control over timing and message ordering.

### Level 5 — Chaos Testing in Staging

After Levels 1–4 pass, run chaos testing in a staging environment under production-representative load. Use Pumba (Docker container chaos) or Gremlin (commercial chaos-engineering platform) for process, network, and resource-level chaos. Toxiproxy continues to be useful for fine-grained network-fault injection at this layer as well. Randomly kill processes. Introduce latency spikes. Flip nodes offline. Corrupt network links. The goal is not to verify known properties. It is to discover failure modes that were not anticipated at Level 4.

Chaos testing requires a multi-node staging environment loaded at a traffic level that reflects median production usage. Chaos under idle conditions finds different failures than chaos under load.

Document every anomaly found during chaos testing, whether or not it causes a visible failure. Anomalies are leading indicators. A node that recovers but takes 47 seconds instead of the expected 3 seconds is not failing. It is about to fail under a slightly different condition.

---

## Section 2: CRDT Growth Tests

CRDT growth tests do not belong in the per-commit test suite. Run them weekly in CI and before every major release. They answer a different question from the pyramid: not "does the system behave correctly" but "does the system stay within resource bounds over time."

Run each growth test with simulated usage at the median activity level for your target vertical. Simulate usage at short, medium, and long time horizons — 30, 90, and 365 days are useful reference points. Measure CRDT document size in bytes at each interval.

**Pass conditions:**

- Document size at 365 days stays within the configured storage budget. The default budget is 10 GB per node. A system that exceeds this budget at 365 days will exceed it in production. Adjust either the budget or the compaction policy before release, not after.
- Library-level compaction fires when the configured threshold is reached and reduces document size measurably. If compaction fires but document size does not decrease, the compaction implementation is not working.
- Application-level document sharding keeps per-shard document size below the shallow snapshot threshold. If any shard exceeds the threshold, verify that shallow snapshot mode activates correctly and that the node does not attempt to load the full document into memory.

Growth tests that fail are not test failures in the normal sense. They are architecture signals. A document that grows without bound is not a test problem; it is a CRDT design problem that requires a change to the data model, the compaction policy, or the sharding strategy.

---

## Section 3: Mandatory Scenarios Before First Production Release

Every scenario below must pass before first production release. These are the minimum set, not representative samples.

Scenario tables carry Pass/Fail status and an Evidence column when used as procurement documentation (Japanese SIer acceptance tests, German BSI reviews, Korean ISMS-P certification). The Evidence column records the artefact produced by a passing run — log excerpt, serialized CRDT state, signed test report — that the release documentation package archives. Prose inline below each table names the scenario-specific evidence expected.

### Partition and Reconnect

| Scenario | Setup | Action | Expected Outcome |
|---|---|---|---|
| 30-day offline divergence | Two nodes share team state; both are disconnected | Each node makes AP-class edits for 30 simulated days; reconnect both | All edits merge correctly; no data loss; both nodes reach identical CRDT state |
| Extended-offline baseline (routine) | One node operates offline for 90 simulated days with sporadic connectivity windows | Simulate 90 days of offline + daily 10-minute online windows with partial sync | Node remains operational throughout; sync resumes cleanly in each window; no operation loss; no divergence at end of period |
| CP quorum loss | Three-node team; all nodes online | Kill two nodes; attempt a CP write on the remaining node | Write is blocked; user sees a clear quorum-unavailable indicator; write is not silently dropped or applied |
| 1,000+ queued operations (standard + low-resource) | One node offline on standard dev hardware and on a constrained-resource variant (2 GB RAM, 16 GB storage — representative African/LatAm SME baseline) | Accumulate 1,000+ queued CRDT operations on the offline node | On reconnect, anti-entropy completes without timeout; all operations are applied; no operations are lost or duplicated; no OOM on constrained hardware |
| Abrupt power interruption during WAL write | Running node with an open transaction writing to the WAL | SIGKILL the process at a random byte offset during an open WAL write, repeated 100+ times across different offsets | WAL recovery completes on relaunch; all operations committed before the kill are present and consistent; no partial operation appears as committed; no corruption of previously committed records. Required scenario for deployments in markets with unreliable grid power (Nigeria, Pakistan, parts of SE Asia, Lagos-style load-shedding contexts) |
| Air-gapped operation | Node operates with no relay connectivity for 30+ simulated days | All operations routed through peer-to-peer sync only; relay endpoint is unreachable and MUST NOT be contacted | All local operations succeed; peer sync completes correctly on P2P path; on relay reconnect, sync resumes without data loss; evidence: relay-endpoint network log shows zero attempted connections during air-gap period |

The quorum-loss test is the most important scenario in this group. A system that silently drops CP writes under quorum loss will corrupt ledger state in production. The pass condition is not "the write fails." It is "the user sees a clear, actionable message and the write is preserved for retry when quorum is restored."

The extended-offline baseline and the power-interruption scenarios are not edge cases. For deployments in Sub-Saharan Africa, rural India, tier-3 LatAm cities, and parts of Southeast Asia, extended offline operation and unplanned shutdowns are the routine operating condition — not exceptions being stress-tested. Evidence from these tests is required for any deployment targeting those markets.

### Schema Migration

| Scenario | Setup | Action | Expected Outcome |
|---|---|---|---|
| N-1 to N sync | One node at schema version N; one node at schema version N-1 | Exchange CRDT deltas in both directions | Lenses translate correctly in both directions; no data loss; both nodes reach valid state for their respective schema version |
| Offline epoch transition | One node offline during an epoch transition | Return the offline node online after the transition completes | Node downloads the epoch snapshot and resumes sync; no manual intervention required; no data loss |
| Couch device | One node offline for 3+ major schema versions | Attempt to reconnect | Capability negotiation rejects the connection with ERR_VERSION_INCOMPATIBLE; the system directs the user to update before sync resumes; the system does not attempt a partial or lossy migration |

The couch-device scenario requires a clear policy decision before testing. What is the maximum schema gap the system will bridge automatically, and what gap triggers a forced update? Encode that policy in the capability negotiation layer and test the boundary explicitly.

### Flease Edge Cases

| Scenario | Setup | Action | Expected Outcome |
|---|---|---|---|
| Lease holder offline mid-write | Node A holds the CP lease; a write is in progress | Kill node A mid-write | The lease expires after the configured timeout (default: 30 seconds); node B acquires a new lease; node A's partial write is quarantined and flagged for review, not silently merged into team state |
| Partition during lease negotiation | Three-node team; all nodes online | Introduce a network partition during CAPABILITY_NEG lease request | Both partitions identify a no-quorum state independently; neither side acquires the lease; writes are blocked on both sides with a clear user message; no split-brain |

The mid-write quarantine behavior is critical. A partial write that is silently merged produces silent data corruption — the hardest class of production defect to detect and repair. The pass condition is not "the partial write is discarded." It is "the partial write is quarantined and visible, so the operator can decide what to do with it."

### Security

Scenarios below produce evidence directly usable in the major regulatory regimes — GDPR/Schrems II, DIFC, RBI, India's DPDP, and the broader Appendix F coverage matrix. The parenthetical regulatory citations name the most common audit contexts where each scenario's evidence is requested.

| Scenario | Setup | Action | Expected Outcome |
|---|---|---|---|
| Storage extraction without credentials (HIPAA §164.312(a)(2)(iv); GDPR Art 32; DPDP Section 8; POPIA §19; LGPD Art 46) | A running node with a SQLCipher-encrypted database | Copy the SQLCipher file to a separate machine; attempt to open it without the encryption key | SQLCipher renders the file unreadable; plaintext access to document content requires the encryption key |
| Key rotation blocks former member (GDPR Art 5(1)(e); NDPR §2.2; Korea PIPA §21) | A team with a role key; one member's access is revoked | Rotate the role KEK; the former member's node attempts to reconnect and request documents written after rotation | The node receives ERR_KEY_REVOKED; it cannot decrypt any document written after the key rotation; re-adding the member requires explicit operator action |
| Historical document re-keying (GDPR Art 32; HIPAA §164.308(a)(5)) | A team with documents encrypted under KEK version K; KEK is rotated to K+1 | Re-wrap all existing DEKs under K+1; verify every document is accessible under K+1 and no document is accessible under K | No document remains accessible under the old KEK; all documents remain accessible under the new KEK; re-keying completes within the configured time budget |
| Data-boundary negative test — relay disabled (Schrems II [C-311/18]; DIFC DPL Art 25; RBI PSD localization circular; NDPR §2.11; PIPL Arts 38–43; 242-FZ) | A running node with relay explicitly disabled in configuration | Perform 100+ AP and CP operations over 60 simulated minutes; monitor all network egress from the node | Zero packets egress to any relay endpoint; all operations complete via P2P or local-only paths; evidence: full network packet capture with relay-destination filter showing zero matches. This scenario is the compliance evidence for every jurisdiction requiring data sovereignty |
| Relay-operator cannot decrypt (PIPL state-actor threat model; 242-FZ; DIFC surveillance-jurisdiction review) | A relay operator with full administrative access to relay infrastructure | Capture every byte transiting the relay during a 60-minute session of AP and CP operations | Relay operator cannot decrypt any document content from captured ciphertext without the team's DEK/KEK material; evidence: captured packet contents are verified ciphertext with no decryption path given relay-side-only keys. Verifies the end-to-end encryption claim under the infrastructure-layer adversary threat model |
| Attestation validation and revocation | A node presents an attestation bundle during CAPABILITY_NEG; the bundle's issuer has subsequently been revoked | Attempt full handshake | Relay validates Ed25519 signature against issuer key, consults revocation list, returns ERR_KEY_REVOKED; no streams or buckets are granted; evidence: relay log entry with timestamp, issuer key fingerprint, and revocation-list hit |
| Audit trail completeness (Japan PIPA Art 23; Korea ISMS-P control 2.6.1; PIPL Art 51; SOX §404; HIPAA §164.308(a)(1)(ii)(D)) | A node with audit logging enabled | Execute a specified operation sequence (create/update/delete against ten documents, with two key rotations and one revocation) | Audit log contains every operation in strict monotonic sequence; no gaps between sequence numbers; tamper-evidence check (Merkle root or equivalent) verifies log integrity; evidence: exported audit log with verified integrity hash |

### Ledger

| Scenario | Setup | Action | Expected Outcome |
|---|---|---|---|
| Sum-to-zero invariant under failure | A posting transaction is in progress | Kill the posting node mid-transaction; retry the transaction | On recovery, exactly one posting set exists; the sum-to-zero invariant holds across all accounts; no duplicate postings are created by the retry |
| Duplicate domain events | A domain event is submitted to the posting engine | Submit the identical domain event a second time | Exactly one set of postings is produced; the idempotency key prevents the second submission from creating duplicate postings |

The sum-to-zero test must verify the invariant across the complete account set, not just the accounts directly involved in the failed transaction. A posting failure that satisfies sum-to-zero locally but violates it across related accounts is a ledger corruption that an account-scoped check will miss.

---

## Section 4: CI Configuration Guidance

Sections 1–3 tell you what to test. This section tells you when to run it and what output to capture. Configure CI in four tiers that reflect the cost and speed of each testing level.

| Tier | Levels | Trigger | Time budget | Failure severity | Purpose |
|---|---|---|---|---|---|
| Per-PR gate | L1 + L2 | Every pull request | L1 <5 min, L2 <15 min | Blocks merge | Fast regression guard |
| Nightly | L3 | Scheduled nightly build | <2 hours total | P1 incident on failure | Fault-injection regression coverage without PR drag |
| Weekly / release candidate | L4 | Scheduled weekly + RC tag | <1 hour (simulation runs are fast once harness exists) | Blocks RC | Deterministic exhaustive coverage of edge cases |
| Pre-major-release | L5 | Before major release | 24–48 hours under representative load | Blocks release | Discovery of unanticipated failure modes |

**Tier notes.** Per-PR tests must stay fast enough to gate merges. Nightly runs catch regressions the day after they land — acceptable trade-off. Running only in staging is not. Level 4 simulation harness requires setup investment, but once it exists, simulation runs are fast — controllable clocks make 30-day scenarios run in seconds. Level 5 chaos requires a production-representative staging environment maintained permanently, not a temporary one spun up per release. The setup and validation cost of a temporary environment consumes the time the chaos run is supposed to save.

**Test artefact capture (required for procurement documentation).** For Level 3, Level 4, and Level 5 runs, the following artefacts must be captured, archived, and linked to the release version:

1. **Test report** — serialized pass/fail status per scenario, with timestamp, test-harness version, and code SHA.
2. **Scenario evidence** — the per-scenario Evidence column output (CRDT state dump, audit log excerpt, network packet capture, relay log fragment) referenced in Section 3 tables.
3. **Harness configuration** — the full configuration of the test environment (toxiproxy rules, chaos parameters, clock-skew settings) so results are reproducible.
4. **SBOM alignment** — the software bill of materials for the artefact tested, tied to the same release version; required for EU Cyber Resilience Act compliance (effective 2027) and for FedRAMP evidence.

These artefacts are the evidence a BSI C5 audit, a Japanese SIer acceptance review, a Korean ISMS-P certification, or a DIFC regulatory inspection will request. Capture them once per RC. Do not reconstruct them under audit pressure.

**Infrastructure notes.** Testcontainers requires Docker in CI; verify Docker availability before adding Level 2 or Level 3 tests. The simulation harness at Level 4 is custom infrastructure — design against the Appendix A protocol specification before implementation begins. A harness built on an incomplete understanding of the handshake simulates the wrong system. Cryptographic test vectors must include Ed25519 (RFC 8032) compliance at minimum; for CIS deployments subject to GOST R 34.10-2012, verify algorithm compliance is testable above the wire layer (Appendix A §A.6 notes algorithm agility is not supported at the wire-protocol layer in this version).

**Accessibility testing.** Sync-state announcements (sync-healthy, stale, offline, conflict-pending, revocation) must be exposed through the platform accessibility tree (`aria-live` on web, `UIAccessibilityTraits` on iOS, `AccessibilityNodeInfo` on Android). Add a scenario that asserts state-change announcements are fired on transition. A UI that communicates state only through color or icon is not accessible and will fail assistive-technology audit on any jurisdiction that mandates WCAG 2.1 AA (EU EAA 2025, US Section 508, UK Equality Act 2010 guidance).

The failure modes these tests exercise will occur in production. The question is whether they surface in CI or in a customer's environment.
