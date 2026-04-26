# Chapter Overview — Inverted Stack Conformance Catalog

Compact navigation index. Use this to scope which chapters to load from `concept-index.yaml`.

**Total concepts:** 562 across 28 chapters
**Foundational:** 298 · **Inverted-stack-specific:** 264

## `preface` — Preface

- **Concept count:** 8
- **Scope:** foundational=3, inverted-stack-specific=5
- **Kleppmann properties touched:** P1, P3, P5, P7
- **ID prefixes:** `PREF`
- **Sample concepts:** The architectural thesis — local node as primary, vendor as optional; SaaS tenancy as a withdrawable dependency; Offline as daily operating condition, not edge case; Three-audience scope (architects, enterprise evaluators, founders/contributors); Council adversarial-review framing (two rounds, five lenses)

## `ch01-when-saas-fights-reality` — When SaaS Fights Reality

- **Concept count:** 11
- **Scope:** foundational=11, inverted-stack-specific=0
- **Kleppmann properties touched:** P1, P3, P4, P5, P6, P7
- **ID prefixes:** `THESIS`
- **Sample concepts:** The SaaS bundle as conjoined value-and-cost; Vendor outage as deadline-coincident failure; Vendor disappearance as routine product end-state; Capability degradation under offline conditions; Data inaccessibility despite nominal ownership

## `ch02-local-first-serious-stack` — Local-First: From Sync Toy to Serious Stack

- **Concept count:** 14
- **Scope:** foundational=9, inverted-stack-specific=5
- **Kleppmann properties touched:** P1, P2, P3, P4, P5, P6, P7
- **ID prefixes:** `LF, THESIS`
- **Sample concepts:** No spinners, no waiting; Work is not trapped on one device; The network is optional; Seamless collaboration; The long now

## `ch03-inverted-stack-one-diagram` — The Inverted Stack in One Diagram

- **Concept count:** 21
- **Scope:** foundational=9, inverted-stack-specific=12
- **Kleppmann properties touched:** P1, P3, P4, P5, P6, P7
- **ID prefixes:** `INV, ZONE`
- **Sample concepts:** Local node as primary; cloud relay as optional peer; Five-layer reference model; Presentation layer owns no state; Four-state node health indicator; Application logic writes locally without network awareness

## `ch04-choosing-your-architecture` — Choosing Your Architecture

- **Concept count:** 15
- **Scope:** foundational=11, inverted-stack-specific=4
- **Kleppmann properties touched:** P1, P2, P3, P4, P5, P6, P7
- **ID prefixes:** `DEC, FILT`
- **Sample concepts:** The One Question (user-owned vs aggregated value); Mixed-ownership architecture pattern; Filter 1 — Consistency requirements (hard stop); Filter 2 — Data ownership profile; Filter 3 — Connectivity and operational environment

## `ch05-enterprise-lens` — The Enterprise Lens

- **Concept count:** 15
- **Scope:** foundational=9, inverted-stack-specific=6
- **Kleppmann properties touched:** P1, P3, P5, P6, P7
- **ID prefixes:** `LENS`
- **Sample concepts:** MDM compliance attestation at capability negotiation; Platform-agnostic MDM integration with regional coverage; Build-time SBOM generation in CycloneDX format; Signed and notarized installer with trusted-publisher compatibility; CVE response service-level commitment

## `ch06-distributed-systems-lens` — The Distributed Systems Lens

- **Concept count:** 16
- **Scope:** foundational=8, inverted-stack-specific=8
- **Kleppmann properties touched:** P3, P4, P5, P6, P7
- **ID prefixes:** `LENS`
- **Sample concepts:** Convergence is not correctness; CRDT applicability boundary by record class; Monotonic CRDT growth as structural property; Three-tier GC policy by data class; Stale peer recovery via full-state snapshot transfer

## `ch07-security-lens` — The Security Lens

- **Concept count:** 17
- **Scope:** foundational=14, inverted-stack-specific=3
- **Kleppmann properties touched:** P3, P5, P6, P7
- **ID prefixes:** `LENS`
- **Sample concepts:** Send-tier subscription filtering; Distributed attack surface acknowledgment; DEK/KEK envelope encryption hierarchy; Key compromise response procedure; Historical data-at-risk window

## `ch08-product-economic-lens` — The Product & Economic Lens

- **Concept count:** 15
- **Scope:** foundational=8, inverted-stack-specific=7
- **Kleppmann properties touched:** P3, P5, P6, P7
- **ID prefixes:** `LENS`
- **Sample concepts:** OSS public-good positioning as commercial strategy; First-customer archetype with named acquisition channel; Named OSS-to-paid conversion trigger; Vertical-first market selection on documented downtime cost; Five-step customer development path

## `ch09-local-first-practitioner-lens` — The Local-First Practitioner Lens

- **Concept count:** 16
- **Scope:** foundational=15, inverted-stack-specific=1
- **Kleppmann properties touched:** P1, P2, P3, P4, P5, P6, P7
- **ID prefixes:** `LENS`
- **Sample concepts:** Plain-file application-independent export path; Non-technical disaster recovery walkthrough; Symmetric NAT plus relay outage as documented failure mode; Engine-agnostic CRDT abstraction for ecosystem reversibility; Peer-attestation QR onboarding bundle

## `ch10-synthesis` — Synthesis: What the Council Finally Agreed On

- **Concept count:** 17
- **Scope:** foundational=11, inverted-stack-specific=6
- **Kleppmann properties touched:** P1, P2, P3, P4, P5, P6, P7
- **ID prefixes:** `LENS`
- **Sample concepts:** Block-vs-condition verdict semantics; Send-tier subscription filtering as data minimization invariant; MDM compliance gate at capability negotiation; Three-tier CRDT applicability model; DEK/KEK envelope encryption with role-scoped rotation

## `ch11-node-architecture` — Node Architecture

- **Concept count:** 31
- **Scope:** foundational=8, inverted-stack-specific=23
- **Kleppmann properties touched:** P1, P3, P4, P5, P6, P7
- **ID prefixes:** `NODE`
- **Sample concepts:** Microkernel monolith pattern; Kernel-plugin boundary by change cadence; Topological plugin load with version contracts; One-shot plugin load surface; Five-state node lifecycle with terminal Faulted

## `ch12-crdt-engine-data-layer` — CRDT Engine and Data Layer

- **Concept count:** 32
- **Scope:** foundational=14, inverted-stack-specific=18
- **Kleppmann properties touched:** P1, P3, P4, P5, P6, P7
- **ID prefixes:** `CRDT`
- **Sample concepts:** Three-layer CRDT architecture (data, semantic, view); CRDT merge mathematical properties (commutativity, associativity, idempotency); CRDT data layer primitives (map, list, text, counter); Semantic layer enforces domain invariants; View layer as derived projections

## `ch13-schema-migration-evolution` — Schema Migration and Evolution

- **Concept count:** 25
- **Scope:** foundational=22, inverted-stack-specific=3
- **Kleppmann properties touched:** P1, P3, P4, P5, P6, P7
- **ID prefixes:** `SCH`
- **Sample concepts:** Multi-version schema skew across nodes; Expand-contract migration pattern; Dual-write during expand phase; Unknown-field tolerance in CRDT maps; Compatibility window minimum duration

## `ch14-sync-daemon-protocol` — Sync Daemon Protocol

- **Concept count:** 35
- **Scope:** foundational=11, inverted-stack-specific=24
- **Kleppmann properties touched:** P1, P3, P4, P5, P6, P7
- **ID prefixes:** `SYNC`
- **Sample concepts:** Sync daemon as separate OS process; IPC over Unix domain socket / named pipe; Device-key authentication on the IPC channel; Daemon ownership of four responsibilities; Three-tier peer discovery

## `ch15-security-architecture` — Security Architecture

- **Concept count:** 36
- **Scope:** foundational=17, inverted-stack-specific=19
- **Kleppmann properties touched:** P6, P7
- **ID prefixes:** `KEY, SEC`
- **Sample concepts:** Distributed honeypot threat model; Three blast-radius bounding properties; Zero-knowledge relay; Relay metadata visibility; Defense in depth — four independent layers

## `ch16-persistence-beyond-the-node` — Persistence Beyond the Node

- **Concept count:** 29
- **Scope:** foundational=11, inverted-stack-specific=18
- **Kleppmann properties touched:** P1, P2, P3, P5, P6, P7
- **ID prefixes:** `DUR`
- **Sample concepts:** Node as authority over data it holds; Five-layer storage architecture; Event log as source of truth; Declarative sync buckets; Eager versus lazy bucket replication

## `ch17-building-first-node` — Building Your First Node

- **Concept count:** 23
- **Scope:** foundational=8, inverted-stack-specific=15
- **Kleppmann properties touched:** P1, P2, P3, P4, P5, P6, P7
- **ID prefixes:** `BUILD`
- **Sample concepts:** Minimum-viable node deliverable checklist; Accelerator-shell-vs-domain-code split; Three-call kernel composition root; Deterministic kernel startup sequence; Onboarding-gated workspace access

## `ch18-migrating-existing-saas` — Migrating an Existing SaaS

- **Concept count:** 24
- **Scope:** foundational=12, inverted-stack-specific=12
- **Kleppmann properties touched:** P1, P2, P3, P4, P5, P6, P7
- **ID prefixes:** `MIG`
- **Sample concepts:** Reversible four-phase migration model; Five migration triggers; Five-filter eligibility framework applied per record class; AP-class versus CP-class record separation; Three-plane Bridge separation

## `ch19-shipping-to-enterprise` — Shipping to Enterprise

- **Concept count:** 23
- **Scope:** foundational=11, inverted-stack-specific=12
- **Kleppmann properties touched:** P3, P5, P6, P7
- **ID prefixes:** `ENT`
- **Sample concepts:** Dual-license structure with commercial exception; Contributor License Agreement precondition; Managed-endpoint packaging contract; System-context daemon registration; macOS Developer ID signing and Apple notarization

## `ch20-ux-sync-conflict` — UX, Sync, and Conflict

- **Concept count:** 25
- **Scope:** foundational=13, inverted-stack-specific=12
- **Kleppmann properties touched:** P1, P2, P3, P4, P5, P6, P7
- **ID prefixes:** `UX`
- **Sample concepts:** Complexity Hiding Standard; Plain-language register for all user-visible state; Three always-visible status indicators; Node health indicator semantics; Link status indicator semantics with no red state

## `epilogue-what-the-stack-owes-you` — What the Stack Owes You

- **Concept count:** 15
- **Scope:** foundational=7, inverted-stack-specific=8
- **Kleppmann properties touched:** P2, P3, P4, P5, P6, P7
- **ID prefixes:** `EPI`
- **Sample concepts:** Protocol-layer data minimization; MDM attestation at capability negotiation; Honest three-tier CRDT consistency; Cryptographic role revocation; Dual license and CLA before community formation

## `appendix-a-sync-daemon-wire-protocol` — Sync Daemon Wire Protocol

- **Concept count:** 36
- **Scope:** foundational=7, inverted-stack-specific=29
- **Kleppmann properties touched:** P1, P2, P3, P4, P6, P7
- **ID prefixes:** `WIRE`
- **Sample concepts:** Unix domain socket transport; Mandatory Noise_XX tunnel; CBOR length-prefixed framing; Four-MiB body cap; Deterministic CBOR for signed fields

## `appendix-b-threat-model-worksheets` — Threat Model Worksheets

- **Concept count:** 25
- **Scope:** foundational=20, inverted-stack-specific=5
- **Kleppmann properties touched:** P3, P5, P6, P7
- **ID prefixes:** `COMP, MITIG, SEC, THREAT`
- **Sample concepts:** Asset inventory worksheet; Asset classification taxonomy; Keystore-binding documentation; Actor taxonomy worksheet; External remote attacker

## `appendix-c-further-reading` — Further Reading

- **Concept count:** 8
- **Scope:** foundational=8, inverted-stack-specific=0
- **Kleppmann properties touched:** P1, P2, P3, P4, P5, P6, P7
- **ID prefixes:** `READ`
- **Sample concepts:** Kleppmann seven local-first ideals; CRDT convergent vs commutative distinction; Flexible Paxos quorum intersection; CAP theorem as architectural constraint; Optimistic replication semantics

## `appendix-d-testing-the-inverted-stack` — Testing the Inverted Stack

- **Concept count:** 14
- **Scope:** foundational=11, inverted-stack-specific=3
- **Kleppmann properties touched:** P1, P3, P4, P5, P6, P7
- **ID prefixes:** `TEST`
- **Sample concepts:** Five-level testing pyramid; Property-based CRDT tests for convergence, idempotency, commutativity, and monotonicity; Real-daemon integration tests via Testcontainers; Fault injection for partition, packet loss, and crash; Deterministic simulation harness with virtual clock and message scheduler

## `appendix-e-citation-style` — Citation Style

- **Concept count:** 1
- **Scope:** foundational=0, inverted-stack-specific=1
- **Kleppmann properties touched:** —
- **ID prefixes:** `DOC`
- **Sample concepts:** Compliance citations verified against primary sources

## `appendix-f-regulatory-coverage` — Regulatory Coverage Map

- **Concept count:** 15
- **Scope:** foundational=10, inverted-stack-specific=5
- **Kleppmann properties touched:** P3, P5, P6, P7
- **ID prefixes:** `COMP`
- **Sample concepts:** GDPR Article 17 right-to-erasure via crypto-shredding; GDPR Article 30 records-of-processing at the node level; Schrems II structural answer via no cross-border transfer; DIFC DPL 2020 categorical foreign-cloud prohibition; UAE Federal DPL 2022 Article 16 erasure right
