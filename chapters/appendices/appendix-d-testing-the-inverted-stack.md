# Appendix D — Testing the Inverted Stack

<!-- Target: ~2,200 words -->
<!-- Source: v13 §15 -->

---

Local-first systems fail in ways that conventional server-side software does not. A network partition, a vector clock divergence, a schema version mismatch between two nodes, or a Flease expiry mid-write are not edge cases — they are normal operating conditions that the system must handle correctly every time. A test suite that does not exercise these conditions is not a test suite; it is a confidence illusion.

This appendix specifies five testing levels and the mandatory scenarios that must pass before first production release. Level 1 and Level 2 run on every pull request. Level 3 runs nightly. Level 4 runs weekly or before release. Level 5 runs in staging before each major release. Every scenario below includes explicit setup conditions, the action to perform, and the expected outcome. If a scenario has no pass condition, it is not a test.

---

## Section 1: The Five-Level Testing Pyramid

### Level 1 — Property-Based Tests

CRDT operations have four mathematical properties that example-based tests cannot verify reliably. Convergence: all replicas eventually agree, regardless of operation order. Idempotency: applying the same operation twice produces the same result as applying it once. Commutativity: concurrent operations reach the same final state regardless of the order in which they are applied. Monotonicity: the CRDT state never shrinks — information is never silently discarded.

Testing these properties with hand-written examples is insufficient. Any example you construct tests one particular operation sequence. The sequences that break convergence are the ones you did not think to write. Property-based frameworks generate thousands of random operation sequences automatically and report the minimal failing case when a property is violated.

For .NET: use FsCheck. For JavaScript: use fast-check. Configure each framework to generate at least 10,000 random operation sequences per property per test run. Do not reduce this count to speed up CI — property violations are rare, and reducing the search space is how they survive to production.

Do not skip Level 1. An example-based CRDT test suite that passes is not evidence that the CRDT is correct. It is evidence that the specific sequences you tested are correct.

### Level 2 — Integration Tests (Real Dependencies)

The sync handshake, capability negotiation, and delta streaming must run against a real daemon process. Mocking the sync daemon produces tests that pass when the real integration is broken. The mock encodes your assumptions about how the daemon behaves — and those assumptions are exactly what you need to test.

Use Testcontainers (.NET) to spin up a real local-node instance per test suite. Run the full five-step handshake: HELLO → CAPABILITY_NEG → ACK → DELTA_STREAM → GOSSIP_PING. Assert on the CRDT state after delta exchange, not on the wire messages. The state is what matters; the message sequence is how you get there.

Testcontainers requires Docker. Add Docker to your CI environment before adding Level 2 tests. The setup cost is hours; the failure modes it catches are production incidents.

### Level 3 — Fault Injection in CI

Network partition, packet loss, and node crash must be exercised in CI, not only in staging. Fault injection in staging runs infrequently, and the gap between a fault being possible and a fault being tested is where production incidents originate.

Use Testcontainers with toxiproxy (or an equivalent network proxy) to inject faults programmatically. Three scenarios are mandatory at this level:

- Node crashes mid-handshake. Assert that the peer recovers, retries, and reaches consistent state.
- Relay becomes unreachable during DELTA_STREAM. Assert that the sender queues deltas locally and retransmits on reconnect.
- GOSSIP_PING misses three consecutive intervals due to packet loss. Assert that the node enters a degraded-but-consistent state and recovers without manual intervention.

The pass condition for every fault injection test is not "the system does not crash." It is "the system recovers to a consistent state." Crashing and restarting is not recovery. Recovery means the CRDT state is identical to what it would have been without the fault.

### Level 4 — Deterministic Simulation

Mixed-version nodes, epoch transitions while a node is offline, and Flease edge cases cannot be tested reliably with real time. Real-time tests are non-deterministic: a lease expiry that takes 30 seconds in production cannot be exercised in CI at real speed without making the test suite unusable. A simulation harness with a controllable clock and deterministic network scheduling makes these scenarios fast, repeatable, and exhaustive.

The simulation harness is not provided out of the box. Teams implementing this architecture must build it. The investment is significant — typically two to four weeks for an engineer who understands the protocol. It is justified: every production incident in a distributed system that a simulation harness would have caught represents a proportionally larger cost in incident response, customer impact, and repair time.

Three scenario families belong at Level 4: mixed-version node sync (one node at schema N, one at schema N-1), epoch transitions while a node is offline, and Flease edge cases such as a lease holder disconnecting mid-write. Each of these requires precise control over timing and message ordering that real-time tests cannot provide.

### Level 5 — Chaos Testing in Staging

After Levels 1–4 pass, run chaos testing in a staging environment under production-representative load. Randomly kill processes, introduce latency spikes, flip nodes offline, and corrupt network links. The goal is not to verify known properties — it is to discover failure modes that were not anticipated at Level 4.

Chaos testing requires a multi-node staging environment. It cannot run meaningfully against a single-node setup. The staging environment must be loaded at a traffic level that reflects median production usage, not idle or synthetic load. Chaos under idle conditions finds different failures than chaos under load.

Document every anomaly found during chaos testing, whether or not it causes a visible failure. Anomalies are leading indicators. A node that recovers but takes 47 seconds instead of the expected 3 seconds is not failing — it is about to fail under a slightly different condition.

---

## Section 2: CRDT Growth Tests

CRDT growth tests do not belong in the per-commit test suite. Run them weekly in CI and before every major release. They answer a different question from the pyramid: not "does the system behave correctly" but "does the system stay within resource bounds over time."

Run each growth test with simulated usage at the median activity level for your target vertical. Simulate 30, 90, and 365 days of usage. Measure CRDT document size in bytes at each interval.

**Pass conditions:**

- Document size at 365 days stays within the configured storage budget. The default budget is 10 GB per node. A system that exceeds this budget at 365 days will exceed it in production. Adjust either the budget or the compaction policy before release, not after.
- Library-level compaction fires when the compaction trigger threshold is reached and reduces document size measurably. If compaction fires but document size does not decrease, the compaction implementation is not working.
- Application-level document sharding keeps per-shard document size below the shallow snapshot threshold. If any shard exceeds the threshold, verify that shallow snapshot mode activates correctly and that the node does not attempt to load the full document into memory.

Growth tests that fail are not test failures in the normal sense — they are architecture signals. A document that grows without bound is not a test problem; it is a CRDT design problem that requires a change to the data model, the compaction policy, or the sharding strategy.

---

## Section 3: Mandatory Scenarios Before First Production Release

Every scenario in this section must pass before the system ships. These are not representative samples — they are the minimum set. A system that passes all scenarios below is not guaranteed to be correct, but a system that fails any of them is guaranteed to have production incidents that were preventable.

### Partition and Reconnect

| Scenario | Setup | Action | Expected Outcome |
|---|---|---|---|
| 30-day offline divergence | Two nodes share team state; both are disconnected | Each node makes AP-class edits for 30 simulated days; reconnect both | All edits merge correctly; no data loss; both nodes reach identical CRDT state |
| CP quorum loss | Three-node team; all nodes online | Kill two nodes; attempt a CP write on the remaining node | Write is blocked; user sees a clear quorum-unavailable indicator; write is not silently dropped or applied |
| 1,000+ queued operations | One node offline | Accumulate 1,000+ queued CRDT operations on the offline node | On reconnect, anti-entropy completes without timeout; all operations are applied; no operations are lost or duplicated |

The quorum-loss test is the most important scenario in this group. A system that silently drops CP writes under quorum loss will corrupt ledger state in production. The pass condition is not "the write fails" — it is "the user sees a clear, actionable message and the write is preserved for retry when quorum is restored."

### Schema Migration

| Scenario | Setup | Action | Expected Outcome |
|---|---|---|---|
| N-1 to N sync | One node at schema version N; one node at schema version N-1 | Exchange CRDT deltas in both directions | Lenses translate correctly in both directions; no data loss; both nodes reach valid state for their respective schema version |
| Offline epoch transition | One node offline during an epoch transition | Return the offline node online after the transition completes | Node downloads the epoch snapshot and resumes sync; no manual intervention required; no data loss |
| Couch device | One node offline for 3+ major schema versions | Attempt to reconnect | Capability negotiation rejects the connection with ERR_VERSION_INCOMPATIBLE; the user is directed to update before sync resumes; the system does not attempt a partial or lossy migration |

The couch-device scenario requires a clear policy decision before testing: what is the maximum schema gap the system will bridge automatically, and what gap triggers a forced update? Encode that policy in the capability negotiation layer and test the boundary explicitly.

### Flease Edge Cases

| Scenario | Setup | Action | Expected Outcome |
|---|---|---|---|
| Lease holder offline mid-write | Node A holds the CP lease; a write is in progress | Kill node A mid-write | The lease expires after the configured timeout (default: 30 seconds); node B acquires a new lease; node A's partial write is quarantined and flagged for review, not silently merged into team state |
| Partition during lease negotiation | Three-node team; all nodes online | Introduce a network partition during CAPABILITY_NEG lease request | Both partitions identify a no-quorum state independently; neither side acquires the lease; writes are blocked on both sides with a clear user message; no split-brain |

The mid-write quarantine behavior is critical. A partial write that is silently merged produces silent data corruption — the hardest class of production defect to detect and repair. The pass condition is not "the partial write is discarded" — it is "the partial write is quarantined and visible, so the operator can decide what to do with it."

### Security

| Scenario | Setup | Action | Expected Outcome |
|---|---|---|---|
| Storage extraction without credentials | A running node with a SQLCipher-encrypted database | Copy the SQLCipher file to a separate machine; attempt to open it without the encryption key | The file is unreadable; SQLCipher encryption prevents plaintext access to any document content |
| Key rotation blocks former member | A team with a role key; one member's access is revoked | Rotate the role KEK; the former member's node attempts to reconnect and request documents written after rotation | The node receives ERR_KEY_REVOKED; it cannot decrypt any document written after the key rotation; re-adding the member requires explicit operator action |

### Ledger

| Scenario | Setup | Action | Expected Outcome |
|---|---|---|---|
| Sum-to-zero invariant under failure | A posting transaction is in progress | Kill the posting node mid-transaction; retry the transaction | On recovery, exactly one posting set exists; the sum-to-zero invariant holds across all accounts; no duplicate postings are created by the retry |
| Duplicate domain events | A domain event is submitted to the posting engine | Submit the identical domain event a second time | Exactly one set of postings is produced; the idempotency key prevents the second submission from creating duplicate postings |

The sum-to-zero test must verify the invariant across the complete account set, not just the accounts directly involved in the failed transaction. A posting failure that satisfies sum-to-zero locally but violates it across related accounts is a ledger corruption that an account-scoped check will miss.

---

## Section 4: CI Configuration Guidance

A team starting with this architecture should configure CI in four tiers that reflect the cost and speed of each testing level.

**Per pull request:** Run Level 1 (property-based) and Level 2 (integration with real dependencies). These tests are fast enough to gate merges. Level 1 tests should complete in under 5 minutes. Level 2 tests, including Testcontainers startup, should complete in under 15 minutes. If either suite exceeds these targets, profile and optimize before adding more tests.

**Nightly:** Run Level 3 (fault injection). Fault injection tests are too slow for PR gates — a single partition-and-recover scenario can take minutes at real time. Running nightly is too infrequent to catch regressions the day they are introduced, but it is far better than running only in staging. When a nightly fault injection run fails, treat it as a P1 until resolved.

**Weekly or pre-release:** Run Level 4 (deterministic simulation). The simulation harness requires setup investment. Once it exists, simulation runs are fast — controllable clocks make 30-day scenarios run in seconds. The weekly cadence is a minimum; run simulation before every release candidate.

**Pre-major-release in staging:** Run Level 5 (chaos testing). Chaos requires a production-representative staging environment. The staging environment is the most expensive testing infrastructure in this stack. Maintain it as a permanent environment, not a temporary one spun up per release — the setup and validation cost of a temporary environment consumes the time the chaos run is supposed to save.

**Infrastructure notes:** Testcontainers requires Docker in CI. Verify Docker availability before adding Level 2 or Level 3 tests to an existing CI pipeline — discovering this dependency after the tests are written wastes time. The simulation harness at Level 4 is not a commodity tool; it is custom infrastructure that the team must design and build. The design should be reviewed against the protocol specification in Appendix A before implementation begins. A simulation harness built on an incomplete understanding of the handshake will simulate the wrong system.

The total CI investment for a team implementing all five levels is significant. It is not optional. The failure modes that these tests exercise are the failure modes that will occur in production. The question is not whether to test them — it is whether to find them in CI or in a customer's production environment.
