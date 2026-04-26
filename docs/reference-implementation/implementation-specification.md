# Implementation Specification — The Inverted Stack

**Generated** from `concept-index.yaml` schema v1.0.
  **Total concepts:** 562 across 28 chapters.
  **Foundational:** 298 (any local-first repo).
  **Inverted-Stack-specific:** 264 (this book's specific architecture).

## How to read this spec

This document is the human-readable view of `concept-index.yaml`. Each *concept* is a discrete architectural commitment the book makes. Concepts group into *chapter epics*, which group into *parts* matching the book structure.

Each concept entry shows:
- **Canonical reference**: `<chapter-stem>:<local-id>` — the stable ID downstream skills and scorecards use.
- **Definition**: one sentence stating what the concept IS.
- **Kleppmann tag**: which of the seven properties (P1–P7) the concept serves. `—` if it serves no Kleppmann property directly (e.g., a build-tooling or business-model concept).
- **Scope tag**: `foundational` (applies to any local-first repo) or `inverted-stack-specific` (requires this book's architectural choices).
- **Failure modes**: named failure modes the concept addresses, where applicable.
- **Must implement**: imperative requirements an implementation must satisfy to claim coverage. Empty for purely philosophical concepts.
- **Verification**: the specific check (file/namespace presence, behavioral test, integration scenario).

## Two consumer audiences

1. **Generic local-first repos** (Loro-, Yjs-, Automerge-, custom-engine implementations) score themselves against the `foundational`-scoped concepts grouped by Kleppmann property — see `concept-index-by-property.yaml` and the future `local-first-properties` Claude skill.
2. **Inverted Stack-aligned repos** (Sunfish's Anchor and Bridge today; future implementations of this book's architecture) score themselves against the FULL concept index — see the future `inverted-stack-conformance` Claude skill.

**Sunfish-specific glue** (mapping concept IDs to Sunfish package paths, ICM pipeline variants for conformance review) lives in `C:\Projects\Sunfish\icm\` — not in this repo.

## Kleppmann property glossary

- **P1** — No spinners — fast, work happens locally
- **P2** — Your work is not trapped on one device
- **P3** — The network is optional
- **P4** — Seamless collaboration with colleagues
- **P5** — The Long Now — data outlives vendor and subscription
- **P6** — Security and privacy by default
- **P7** — You retain ultimate ownership and control

## Property coverage summary

| Property | Concept count |
|---|---|
| P1: No spinners — fast, work happens locally | 61 |
| P2: Your work is not trapped on one device | 22 |
| P3: The network is optional | 158 |
| P4: Seamless collaboration with colleagues | 138 |
| P5: The Long Now — data outlives vendor and subscription | 181 |
| P6: Security and privacy by default | 199 |
| P7: You retain ultimate ownership and control | 216 |

Note: a single concept can serve multiple properties. The sum exceeds the total concept count.

## Scope coverage summary

| Scope | Concept count |
|---|---|
| `foundational` | 298 |
| `inverted-stack-specific` | 264 |

## Synthesis relationships

Several chapters synthesize or reference concepts from other chapters. Downstream consumers (skills, scorecards) should be aware of these relationships when computing coverage:

- **ch10-synthesis** ← ch05-enterprise-lens, ch06-distributed-systems-lens, ch07-security-lens, ch08-product-economic-lens, ch09-local-first-practitioner-lens
  - Ch10 LENS-* concepts are the survivors of cross-lens review; Ch05-Ch09 LENS-{E,D,S,P,LF}-* concepts are the per-lens sources. Downstream consumers may treat Ch10 entries as canonical and per-lens entries as supporting derivations.
- **ch14-sync-daemon-protocol** ← appendix-a-sync-daemon-wire-protocol
  - Ch14 SYNC-* concepts describe the daemon at the protocol/architecture level; Appendix A WIRE-* concepts specify the byte-level wire format. Both are normative — Ch14 owns semantics, Appendix A owns format.
- **ch15-security-architecture** ← appendix-b-threat-model-worksheets
  - Ch15 KEY-*/SEC-* concepts define security primitives and architecture; Appendix B THREAT-*/SEC-*/MITIG-* concepts define threat-model worksheet methodology + named actors + per-actor mitigations. Complementary — Ch15 owns mechanism, Appendix B owns runbook.
- **appendix-d-testing-the-inverted-stack** ← ch12-crdt-engine-data-layer, ch13-schema-migration-evolution, ch14-sync-daemon-protocol, ch15-security-architecture
  - Appendix D TEST-* concepts operationalize Part III architectural concepts as test patterns. Each TEST-* references one or more body-chapter concepts.
- **epilogue-what-the-stack-owes-you** ← ch11-node-architecture, ch12-crdt-engine-data-layer, ch14-sync-daemon-protocol, ch15-security-architecture, ch16-persistence-beyond-the-node
  - Epilogue EPI-* concepts are obligation contracts — each names what a Part III chapter must deliver to qualify as local-first under this book's definition.

## Cross-chapter ID collisions

The following local IDs appear in more than one chapter. The canonical reference `chapter:id` disambiguates them.

| Local ID | Chapters |
|---|---|
| `COMP-01` | appendix-b-threat-model-worksheets, appendix-f-regulatory-coverage |
| `COMP-02` | appendix-b-threat-model-worksheets, appendix-f-regulatory-coverage |
| `SEC-01` | ch15-security-architecture, appendix-b-threat-model-worksheets |
| `SEC-02` | ch15-security-architecture, appendix-b-threat-model-worksheets |
| `SEC-03` | ch15-security-architecture, appendix-b-threat-model-worksheets |
| `SEC-04` | ch15-security-architecture, appendix-b-threat-model-worksheets |
| `SEC-05` | ch15-security-architecture, appendix-b-threat-model-worksheets |
| `SEC-06` | ch15-security-architecture, appendix-b-threat-model-worksheets |
| `SEC-07` | ch15-security-architecture, appendix-b-threat-model-worksheets |
| `SEC-08` | ch15-security-architecture, appendix-b-threat-model-worksheets |
| `SEC-09` | ch15-security-architecture, appendix-b-threat-model-worksheets |
| `SEC-10` | ch15-security-architecture, appendix-b-threat-model-worksheets |
| `SEC-11` | ch15-security-architecture, appendix-b-threat-model-worksheets |
| `SEC-12` | ch15-security-architecture, appendix-b-threat-model-worksheets |
| `THESIS-01` | ch01-when-saas-fights-reality, ch02-local-first-serious-stack |
| `THESIS-02` | ch01-when-saas-fights-reality, ch02-local-first-serious-stack |
| `THESIS-03` | ch01-when-saas-fights-reality, ch02-local-first-serious-stack |
| `THESIS-04` | ch01-when-saas-fights-reality, ch02-local-first-serious-stack |
| `THESIS-05` | ch01-when-saas-fights-reality, ch02-local-first-serious-stack |
| `THESIS-06` | ch01-when-saas-fights-reality, ch02-local-first-serious-stack |
| `THESIS-07` | ch01-when-saas-fights-reality, ch02-local-first-serious-stack |

---

# The catalog

## Part 0 — Front matter

### Epic: Preface (preface)

**Source-paper refs:** v13 preface, v5 §1

**Concept count:** 8

#### `preface:PREF-01` — The architectural thesis — local node as primary, vendor as optional

The book's central thesis is the inversion of the SaaS dependency relationship: the local node is the primary data plane and the vendor relay is an optional accelerator, so the application survives vendor withdrawal.

**Kleppmann:** `P3, P5, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, vendor-acquisition, vendor-outage`

**Must implement:**

- Application reads and writes hit local storage as the primary data plane
- No application function depends on cloud reachability for core operation
- Vendor relay services are optional accelerators, not required dependencies
- Application continues to function when the vendor service is unreachable, withdrawn, or sanctioned

**Verification:** Disconnect the application from all vendor services (network block of vendor domains); application performs all core read, write, and local collaboration operations identically to the connected state.

> This is the book's defining concept; every later concept either implements it or stress-tests it.

#### `preface:PREF-02` — SaaS tenancy as a withdrawable dependency

SaaS tenancy is an external dependency that can be withdrawn unilaterally by the vendor, evidenced by the 2022 Adobe/Autodesk/Microsoft/Figma suspensions across Russia and the CIS that locked organizations out of their own data on infrastructure they had paid for.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, vendor-acquisition, vendor-outage`

*Conceptual / philosophical — no direct implementation requirement.*

> Canonical real-world evidence cited throughout the book for the vendor-withdrawal failure mode.

#### `preface:PREF-03` — Offline as daily operating condition, not edge case

Intermittent or absent connectivity is the baseline operating condition for enterprise users across Sub-Saharan Africa, rural India, tier-3 Latin American cities, and much of Southeast Asia, so offline-first is a primary requirement rather than a degraded mode.

**Kleppmann:** `P1, P3` · **Scope:** `foundational` · **Failure modes:** `vendor-outage`

**Must implement:**

- Application has no degraded mode when offline; offline behavior matches online behavior for core operations
- Application is usable on intermittent connectivity without user-visible spinners on local actions

**Verification:** Run the application on a connection that drops for hours at a time; user can complete every core workflow during the disconnected windows with no behavioral difference from connected operation.

#### `preface:PREF-04` — Three-audience scope (architects, enterprise evaluators, founders/contributors)

The book is scoped for three audiences — software architects and senior engineers (Parts III/IV technical specification), enterprise IT and decision-makers (Chapters 5, 7, 15, 19 governance and compliance), and open-source contributors, technical founders, and product teams (Chapters 8, 10, 16 commercial viability) — and a reference implementation must serve all three audience needs simultaneously.

**Scope:** `inverted-stack-specific`

*Conceptual / philosophical — no direct implementation requirement.*

> Book-meta concept; informs which audience constraints downstream chapters address.

#### `preface:PREF-05` — Council adversarial-review framing (two rounds, five lenses)

The architecture in this book has been stress-tested through two rounds of adversarial review by five domain experts (enterprise IT, distributed systems research, security, product management, local-first practitioner), with Round 1 producing two BLOCK verdicts that forced a partial rewrite and Round 2 clearing all five lenses under fifteen documented conditions named in the epilogue.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Reference implementation documents the fifteen conditions under which Round 2 cleared the architecture
- Each council lens has at least one corresponding test or design artifact demonstrating the objection has been answered

**Verification:** Repository contains a council-conditions document enumerating the fifteen Round 2 conditions, each cross-referenced to the chapter, code, or test that satisfies it.

> Structures Part II of the book and the conformance contract for any reference implementation.

#### `preface:PREF-06` — Sunfish reference-implementation policy (packages not class APIs)

The book references the Sunfish reference implementation by package name (e.g., Sunfish.Kernel.Sync, Sunfish.Foundation.LocalFirst) rather than by class, method, or constructor signature, because package contracts are stable while pre-1.0 method signatures are not.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Documentation references Sunfish (or any reference implementation) by package or namespace, not by class API
- Package boundaries are stable across pre-1.0 releases even when class internals change

**Verification:** Search the manuscript for class-name or method-signature references to Sunfish packages; references must be at package or namespace granularity only.

#### `preface:PREF-07` — Engine-agnostic CRDT architecture via ICrdtEngine

The CRDT engine is pluggable through a single ICrdtEngine adapter, with YDotNet as the current implementation and Loro as the aspirational target, so the engine choice is reversible by design.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-acquisition`

**Must implement:**

- A single adapter interface (e.g., ICrdtEngine) abstracts the CRDT engine from the rest of the system
- At least one engine implementation is wired through the adapter; swapping engines requires no changes outside the adapter implementation
- Documentation names both the current engine and at least one alternate target to demonstrate engine-agnosticism is real, not aspirational

**Verification:** Replace the YDotNet adapter implementation with a stub or alternate engine; the rest of the system compiles and core CRDT operations route through the adapter without source changes outside the adapter package.

#### `preface:PREF-08` — AI-collaboration disclosure (production transparency)

The book discloses that Claude and Claude Code were collaborators in research, drafting, technical review, editing, the Kleppmann Council reviews, the literary-board review cycle, and the audiobook production pipeline, with the author retaining full responsibility for architectural arguments, conclusions, and remaining errors.

**Scope:** `inverted-stack-specific`

*Conceptual / philosophical — no direct implementation requirement.*

> Production-transparency concept; not architectural but cited as a framing precedent for the Council disclosure in Part II.


---

## Part I — Thesis and pain

### Epic: When SaaS Fights Reality (ch01-when-saas-fights-reality)

**Source-paper refs:** v13 §3, v13 Executive Summary, v13 §14.1, v13 §20.4, v5 §1

**Concept count:** 11

#### `ch01-when-saas-fights-reality:THESIS-01` — The SaaS bundle as conjoined value-and-cost

SaaS packages three desirable properties (real-time collaboration, multi-device access, zero maintenance) inseparably with three undesirable conditions (data on vendor infrastructure, vendor-discretion pricing, vendor-contingent service continuity), accepted as a single take-it-or-leave-it deal because the technology of the time made the conditions appear structurally required to deliver the properties.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, vendor-acquisition, vendor-outage`

*Conceptual / philosophical — no direct implementation requirement.*

> The bundle frame is the organizing thesis Ch01 establishes; the rest of the book argues the bundle is now separable.

#### `ch01-when-saas-fights-reality:THESIS-02` — Vendor outage as deadline-coincident failure

A failure mode in which the SaaS provider's infrastructure becomes unavailable (full outage or undisclosed degraded performance) and renders user data inaccessible at the moment of greatest operational need, with cascading exposure when many vendors share the same underlying cloud region.

**Kleppmann:** `P1, P3` · **Scope:** `foundational` · **Failure modes:** `vendor-outage`

**Must implement:**

- Application reads and writes complete locally without dependency on vendor reachability
- Application surfaces no functional difference between connected and disconnected operation for core workflows
- Application does not silently queue submissions whose persistence cannot be confirmed

**Verification:** Disconnect network from the device; application performs all core read, write, search, and submission operations identically to the connected case.

#### `ch01-when-saas-fights-reality:THESIS-03` — Vendor disappearance as routine product end-state

A failure mode in which the SaaS provider is acquired, sunset, pivoted, or runs out of runway, terminating service on a vendor-controlled timeline and leaving users with whatever export the vendor chooses to provide in whatever format the vendor chooses to emit.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `vendor-acquisition`

**Must implement:**

- User data is stored in a format the user can read without the vendor's tools
- Application continues to function on user-controlled hardware after vendor termination
- Schema, attachments, comment threads, and relationship structure remain coherent without vendor-side reconstruction

**Verification:** Remove all vendor-side services; application launches, reads historical data, and continues normal operation against the local store.

#### `ch01-when-saas-fights-reality:THESIS-04` — Capability degradation under offline conditions

A failure mode in which a SaaS application reduces to a read-only cache, queued submissions of uncertain success, or total inoperability when network connectivity is intermittent, weak, restricted, or absent — disproportionately affecting field, rural, clinical, industrial, air-gapped, and majority-world users whose baseline operating environment is non-continuous connectivity.

**Kleppmann:** `P1, P3` · **Scope:** `foundational` · **Failure modes:** `vendor-outage`

**Must implement:**

- All core operations including create, update, search, and report execute against local storage with no functional difference from the connected case
- Submission persistence is locally durable and acknowledged at write time
- No feature is gated on persistent connectivity

**Verification:** Place device in airplane mode for the duration of a complete representative workflow; confirm every action completes locally and converges on later reconnect with no user intervention.

#### `ch01-when-saas-fights-reality:THESIS-05` — Data inaccessibility despite nominal ownership

A failure mode in which user data is contractually owned by the user but operationally inaccessible due to export rate limits, proprietary formats that strip semantic structure, feature-gated export behind paid tiers, or short post-cancellation retrieval windows.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, vendor-acquisition`

**Must implement:**

- User data is stored locally in a documented, schema-described format
- Bulk export of all user data completes in bounded time without rate limiting
- Export preserves attachments with metadata, comment threading, and custom-field semantics
- No retrieval depends on an active subscription or vendor billing state

**Verification:** Run a documented export procedure on a representative dataset; confirm the export round-trips into a third-party tool with attachments, threading, and field semantics intact.

#### `ch01-when-saas-fights-reality:THESIS-06` — Post-adoption pricing capture

A failure mode in which switching costs accumulated through training, integrations, historical data, and learned workflows allow vendors to raise prices, move features behind higher tiers, or change contractual terms after the customer has lost realistic exit leverage, with per-seat pricing and integration ecosystems compounding the lock-in as teams grow.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `vendor-acquisition`

**Must implement:**

- Architecture removes the structural switching cost by keeping data, schema, and workflow on user infrastructure
- No core capability is gated on a vendor subscription tier
- Integration with other tools occurs through user-controlled interfaces, not vendor-locked connectors

**Verification:** Cancel any optional vendor relay or sync service; confirm the application retains all core functionality on the local node alone.

#### `ch01-when-saas-fights-reality:THESIS-07` — Third-party veto over vendor-custodied data

A failure mode in which an external authority — sanctions regime, data residency regulator, court order, or national security designation — compels the vendor to suspend service or compels the customer to cease use, ending the relationship regardless of either party's preferences because data custody at the vendor concentrates the exposure surface there.

**Kleppmann:** `P5, P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, vendor-acquisition`

**Must implement:**

- Authoritative state for user data resides on hardware the user controls
- Application functions independently of any vendor-side service for core workflows
- Any optional relay holds ciphertext only and is replaceable by a user-controlled relay without data migration

**Verification:** Specification documents the data custody boundary; deployment guide demonstrates substituting a user-controlled relay for a vendor relay with no application-level changes.

> Distinct from the first five failure modes in originating outside the vendor-customer relationship; addressed in Appendix F regulatory coverage.

#### `ch01-when-saas-fights-reality:THESIS-08` — Architectural reversal of data custody

The thesis-level architectural inversion that moves authoritative state from vendor infrastructure to user infrastructure, demoting the vendor's role from primary data plane to optional relay peer, made feasible by three independently matured technology shifts (production CRDTs, edge gossip protocols, the local service pattern).

**Kleppmann:** `P3, P5, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, vendor-acquisition, vendor-outage`

**Must implement:**

- Authoritative copy of user data lives on the user's device or user-controlled infrastructure
- Vendor or shared services participate, when present, as peers or relays rather than as authoritative state holders
- The architecture composes production-proven CRDT, gossip, and local-service-pattern components rather than introducing novel primitives

**Verification:** Architecture documents identify the device-resident authoritative store; sync protocol documents identify any cloud component as relay or peer rather than primary; component inventory cites mature open implementations for each substrate.

#### `ch01-when-saas-fights-reality:THESIS-09` — No-degraded-mode commitment

An architectural commitment that the application exposes no reduced-capability operating mode under offline, partitioned, or vendor-unreachable conditions — every core capability behaves identically whether the network is present or absent.

**Kleppmann:** `P1, P3` · **Scope:** `foundational` · **Failure modes:** `vendor-outage`

**Must implement:**

- No feature presents an offline-only read-only state
- No submission path queues with uncertain persistence semantics
- Search, reporting, create, update, and delete operate against local storage with the same latency and correctness profile online and offline
- The application surfaces no banner, modal, or capability gate that distinguishes connected from disconnected state for core workflows

**Verification:** Behavioral test runs the full core workflow with the network disabled and asserts byte-identical outcomes (modulo timestamps) to the connected baseline; UI inspection confirms no degraded-mode indicator appears.

> Specifically named for accessibility-technology users for whom degraded mode is functionally equivalent to inaccessibility.

#### `ch01-when-saas-fights-reality:THESIS-10` — Asymmetric exposure of small-and-medium organizations

The observation that the SaaS bundle's undesirable conditions fall hardest on small and medium professional service firms because they sign standard terms without negotiated SLA, escrow, or portability clauses, while bearing direct professional, regulatory, and client-relationship consequences from any of the six failure modes.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection`

**Must implement:**

- The architecture provides default protections (data custody, portability, durability) without requiring per-customer contractual negotiation
- Compliance posture for regulated professions (legal, medical, construction, finance) is met by default deployment, not by enterprise add-ons

**Verification:** Default deployment of the architecture passes a representative SMB compliance checklist (HIPAA, professional responsibility, jurisdictional residency) without enterprise-tier features enabled.

#### `ch01-when-saas-fights-reality:THESIS-11` — Paper-fallback as evidence of mediation rather than value

The observation that organizations under SaaS outage continue operating via analog fallbacks (paper charts, whiteboards, fax, manual reconciliation) demonstrates that the SaaS layer was largely mediating work that continued to happen, while the digital affordances (search, cross-history pattern detection, analytic queries) were the genuine value lost — value that a local-first node preserves through the outage.

**Kleppmann:** `P1, P3, P4` · **Scope:** `foundational` · **Failure modes:** `vendor-outage`

**Must implement:**

- Local node retains full digital affordances (search, reporting, cross-record analytics) during vendor or network unavailability
- Reconciliation overhead after a connectivity gap reduces from days of post-incident transcription to automatic convergence on reconnect
- Paper backup remains an available last resort but ceases to be the only operating mode

**Verification:** Field test simulates vendor unavailability for a representative workday; node retains search, reporting, and analytic queries against local data; on reconnect, no manual transcription or back-fill is required.


### Epic: Local-First: From Sync Toy to Serious Stack (ch02-local-first-serious-stack)

**Source-paper refs:** v13 §2.1-§2.4, v13 §19, v5 §1-§3

**Concept count:** 14

#### `ch02-local-first-serious-stack:LF-01` — No spinners, no waiting

The software responds instantly because it reads from local state rather than from a network request, with no perceptible round-trip latency for any user-visible operation.

**Kleppmann:** `P1` · **Scope:** `foundational` · **Failure modes:** `vendor-outage`

**Must implement:**

- Application reads resolve from local storage without a network call
- User-visible operations show no loading spinners during normal use
- Latency does not depend on network round-trip time for any core operation

**Verification:** Disconnect network; instrument all user-visible reads and writes; confirm zero network calls and sub-frame latency for every core operation.

#### `ch02-local-first-serious-stack:LF-02` — Work is not trapped on one device

User data is structurally accessible across all the user's devices and to designated collaborators without depending on a vendor account or subscription to remain accessible.

**Kleppmann:** `P2` · **Scope:** `foundational` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- Data syncs across the user's own devices without vendor account dependency
- Data syncs to designated collaborators without subscription gating
- Loss of vendor service does not strand data on a single device

**Verification:** Cancel the vendor subscription or simulate vendor disappearance; confirm data remains accessible and syncable across devices the user controls.

#### `ch02-local-first-serious-stack:LF-03` — The network is optional

The full application works without any network connection indefinitely and syncs when a connection becomes available, with the local node holding an authoritative copy of all data it is allowed to act on.

**Kleppmann:** `P3` · **Scope:** `foundational` · **Failure modes:** `partition, peer-discovery-failure, vendor-outage`

**Must implement:**

- Every core operation works identically with the network disconnected
- The local node holds an authoritative copy of data it can act on, not a stale cache
- No operation queues waiting for a server before completing locally
- Sync resumes automatically when connectivity returns

**Verification:** Disconnect network indefinitely; perform all core operations; confirm identical behavior to online mode and successful convergence after reconnection.

#### `ch02-local-first-serious-stack:LF-04` — Seamless collaboration

Multiple people can edit the same data simultaneously without explicit locking, checkout workflows, or a designated human conflict resolver, with convergence guaranteed by merge semantics rather than by a coordinating server.

**Kleppmann:** `P4` · **Scope:** `foundational` · **Failure modes:** `clock-skew, partition`

**Must implement:**

- Concurrent edits from multiple peers converge to a defined merged state
- No central server is required to adjudicate concurrent writes
- No explicit lock or checkout workflow gates concurrent editing
- CRDT or equivalent merge semantics provide deterministic convergence

**Verification:** Multi-peer concurrent-edit test under partition; confirm byte-identical state on all peers after partition heal without server adjudication.

#### `ch02-local-first-serious-stack:LF-05` — The long now

User data outlives the vendor, the subscription, the company's strategic priorities, and the political conditions under which the service operates, by virtue of being stored in an open format on user-controlled hardware.

**Kleppmann:** `P5` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, vendor-acquisition, vendor-outage`

**Must implement:**

- Data is stored in an open, documented format readable by tools other than the originating application
- Data lives on hardware the user physically controls
- Continued access does not depend on vendor existence, subscription status, or jurisdictional service availability
- Sync formats are open or interoperable, not proprietary lock-in

**Verification:** Confirm data file format has a public specification readable by at least one independent tool; confirm continued read/write access works after simulated vendor shutdown and after simulated jurisdictional service withdrawal.

#### `ch02-local-first-serious-stack:LF-06` — Security and privacy by default

Data is encrypted end-to-end at rest and in transit by default, with key control held by the user rather than the vendor, raising the cost of compromise from one breach exposing all users to one breach exposing one user.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, key-compromise, key-loss`

**Must implement:**

- Data at rest is encrypted under keys the user controls
- Data in transit is end-to-end encrypted between authorized peers
- Vendor or relay infrastructure cannot decrypt user data
- Compromise of one node yields one user's data, not all users' data

**Verification:** Confirm relay or vendor infrastructure handles ciphertext only; confirm key material does not leave user-controlled hardware; threat-model worksheet demonstrates one-node-compromise containment.

#### `ch02-local-first-serious-stack:LF-07` — You retain ultimate ownership and control

The user structurally — not contractually — decides where data lives, who can access it, and when to delete it, because the bits live on hardware the user controls in a format the user can read under encryption the user can manage.

**Kleppmann:** `P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, vendor-acquisition`

**Must implement:**

- Data resides on hardware physically controlled by the user
- Data format is readable by the user without vendor cooperation
- Encryption keys are managed by the user, not held in escrow by the vendor
- Ownership is structural (architectural) rather than promised by contract

**Verification:** Confirm user can copy, back up, and read data files independently of the vendor application; confirm key material is held only on user-controlled hardware.

#### `ch02-local-first-serious-stack:THESIS-01` — Seven properties as a minimum bar, not a wishlist

The seven Kleppmann properties function as a calibrated filter that fails any system satisfying only a subset, not as a menu from which an implementer may select.

**Kleppmann:** `P1, P2, P3, P4, P5, P6, P7` · **Scope:** `foundational`

**Must implement:**

- Conformance evaluation treats the seven properties as a conjunctive set
- Partial satisfaction (e.g., five-of-seven) is recorded as non-conformance, not as success
- Gradient scoring is permitted alongside but does not replace the binary minimum-bar reading

**Verification:** Conformance scorecard reports per-property pass/fail in addition to any gradient score; overall conformance requires all seven to pass.

#### `ch02-local-first-serious-stack:THESIS-02` — Full node versus smart cache

A full node runs presentation, application logic, sync daemon, storage, and security primitives locally with the cloud serving as another peer for relay and backup, whereas a smart cache holds a recent copy of server-authoritative state and defers to the server for write authority and business logic.

**Kleppmann:** `P1, P3, P4, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition, vendor-outage`

**Must implement:**

- Local node holds authoritative state for data the user is allowed to act on
- Business logic and automations execute locally, not on a server
- Cloud components serve relay and backup roles, never source-of-truth roles
- All five layers (UI, business logic, sync, storage, security) run on the user's device

**Verification:** Disconnect from any vendor-operated infrastructure; confirm new records can be created, business automations fire, and concurrent edits converge against local state alone.

#### `ch02-local-first-serious-stack:THESIS-03` — Composition as the contribution

This book's contribution is the integration of existing proven primitives (CRDT libraries, gossip anti-entropy, desktop-shell-plus-local-server, declarative partial sync, container background services, bidirectional schema lenses) into a coherent enterprise-deployable system, not the invention of new primitives.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Architecture reuses audited, production-validated primitives rather than inventing equivalents
- Each component has at least one cited production analogue
- Integration concerns (consistent invariants across components) are treated as the primary engineering work

**Verification:** For every primitive in the architecture, a production analogue is named in the chapter or appendix; integration ADRs document how invariants compose across primitive boundaries.

#### `ch02-local-first-serious-stack:THESIS-04` — No-novel-cryptography discipline

Property 6 is feasible only when audited cryptographic primitives (libsodium, age, Argon2id reference) are used opaquely and a DEK/KEK hierarchy composes them against a specification reviewed by a cryptographic engineer, never when novel cryptography is invented.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- All cryptographic primitives come from audited reference libraries
- No new cipher, KDF, or protocol construction is invented in-house
- Key hierarchy composition is reviewed by a credentialed cryptographic engineer before deployment

**Verification:** SBOM lists cryptographic dependencies; design review record names the cryptographic engineer who approved the key hierarchy; no in-house cipher implementations are present in the codebase.

#### `ch02-local-first-serious-stack:THESIS-05` — Adopt-don't-invent wire format discipline

Property 5 (the long now) is preserved by adopting an existing portable CRDT format (Yjs or Automerge) rather than inventing a proprietary wire format, because invented formats repeat the Anytype Any-Block portability failure.

**Kleppmann:** `P5` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-acquisition`

**Must implement:**

- The CRDT wire format is a documented, third-party-readable specification (Yjs, Automerge, or equivalent)
- No proprietary or single-vendor wire format is introduced for portable data
- At least one independent tool can parse the wire format

**Verification:** Wire format documentation cites the upstream specification; an independent reference implementation parses sample documents; ADR records the adopt-don't-invent decision.

#### `ch02-local-first-serious-stack:THESIS-06` — Disaggregated managed relay

A managed relay is a residual vendor dependency that holds ciphertext only and can be self-hosted without protocol changes, distinguishing it structurally from a SaaS vendor that holds decryptable data.

**Kleppmann:** `P5, P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- The managed relay handles ciphertext exclusively
- The relay protocol is documented and supports user self-hosting without modification
- Data custody (the keys) remains on user hardware, never on relay infrastructure
- Relay failure does not destroy user data, only impairs propagation

**Verification:** Wire-protocol specification confirms ciphertext-only relay payloads; deploy a self-hosted relay using the public protocol and confirm interoperability with the managed relay; threat model documents relay as untrusted.

#### `ch02-local-first-serious-stack:THESIS-07` — Per-record CAP positioning

The architecture treats CRDT-merge records and lease-coordinated records as first-class distinct classes with a defined boundary and handoff between them, rather than forcing all data into a single consistency model.

**Kleppmann:** `P3, P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Each record type is classified as AP (CRDT-merged) or CP (lease-coordinated) at schema definition time
- The boundary between AP and CP records is explicit and documented
- A defined handoff protocol governs interactions that cross the boundary

**Verification:** Schema declarations carry an AP/CP tag for each record type; integration tests exercise the handoff protocol between AP and CP records.


### Epic: The Inverted Stack in One Diagram (ch03-inverted-stack-one-diagram)

**Source-paper refs:** v13 §5, v5 §2, v5 §2.1, v5 §2.2

**Concept count:** 21

#### `ch03-inverted-stack-one-diagram:INV-01` — Local node as primary; cloud relay as optional peer

The architectural inversion replaces SaaS's cloud-primary / device-cache topology with a topology where the local node holds the authoritative copy and any cloud relay participates only as an optional sync peer.

**Kleppmann:** `P1, P3, P5, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, partition, vendor-outage`

**Must implement:**

- Application reads and writes hit the local store as the primary data path
- No code path requires cloud connectivity for core function
- Cloud relay participation is optional and removable without changing application behavior
- The node has no degraded mode when no peers are reachable

**Verification:** Disconnect all network interfaces; the application performs every core operation identically and the relay role can be unplugged without rebuilding the application.

#### `ch03-inverted-stack-one-diagram:INV-02` — Five-layer reference model

The inverted stack decomposes into five layers — Presentation, Application Logic, Sync Daemon, Storage, and Relay/Discovery — each with a single owner, a single boundary, and an explicit answer to the network-unavailable question.

**Kleppmann:** `P3` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Each layer has one owner and a documented boundary
- Each layer has a defined behavior when no peer is reachable
- Layers are addressable independently and replaceable without rewriting adjacent layers

**Verification:** Architecture documentation enumerates five layers, each with owner, boundary, and offline-behavior statements; the reference implementation contains a separate component per layer.

#### `ch03-inverted-stack-one-diagram:INV-03` — Presentation layer owns no state

The presentation layer renders directly from the local store, owns no independent state, caches nothing on its own, and makes no data decisions.

**Kleppmann:** `P1, P3` · **Scope:** `inverted-stack-specific`

**Must implement:**

- UI components read from the local store and do not maintain a parallel cache
- The same component surface renders against a local desktop node and a hosted tenant node without modification
- UI behavior is unchanged when no peers are reachable, except for the sync-status indicator

**Verification:** UI integration test renders the same component tree against an Anchor instance and a Bridge instance and asserts identical output for the same store state.

#### `ch03-inverted-stack-one-diagram:INV-04` — Four-state node health indicator

The presentation layer surfaces sync state as four named states — sync-healthy, stale, offline, and conflict-pending — each communicated through more than color and announced to assistive technology on transition.

**Kleppmann:** `P1, P3` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition, peer-discovery-failure`

**Must implement:**

- Health indicator exposes sync-healthy, stale, offline, and conflict-pending states
- Each state has a non-color cue and a programmatic accessibility description
- State transitions trigger an assistive-technology live-region announcement

**Verification:** Component test confirms accessibility-tree exposure of each state name and live-region announcement on transition; visual test confirms a non-color cue per state.

#### `ch03-inverted-stack-one-diagram:INV-05` — Application logic writes locally without network awareness

Domain command handlers translate user intent into CRDT operations against the local store and contain no network-aware code paths, except for explicit consultation of the lease coordinator for CP-class records.

**Kleppmann:** `P1, P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition, vendor-outage`

**Must implement:**

- Command handlers commit to the local store before acknowledgement
- The application logic layer contains no implicit network calls in its validation or invariant code
- CP-class writes explicitly call the lease coordinator and surface a clear constraint when quorum is unreachable

**Verification:** Static analysis confirms application-logic modules import no network client; unit tests pass with the sync daemon socket disabled for AP-class operations.

#### `ch03-inverted-stack-one-diagram:INV-06` — Per-record-class CAP positioning

CAP trade-offs are made per record class rather than per application — documents and notes are AP via CRDT merge, identity facts are AP with deferred merge, reservations and slots are CP via distributed lease, and financial transactions are CP under lease plus ledger ordering.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `clock-skew, partition`

**Must implement:**

- Each record class declares its CAP position in the schema
- AP-class records use CRDT merge with deterministic semantics
- CP-class records require lease acquisition before commit
- Audit-bound records commit through an append-only ledger with strict ordering

**Verification:** Schema definition enumerates CAP class per record type; integration test demonstrates AP-class writes succeed under partition while CP-class writes block until quorum returns.

#### `ch03-inverted-stack-one-diagram:INV-07` — Sync daemon as separate long-running process

The sync daemon runs as a separate OS-managed long-running process that survives application restarts and communicates with the application shell over a Unix-domain socket.

**Kleppmann:** `P3, P4` · **Scope:** `inverted-stack-specific`

**Must implement:**

- The daemon registers with the OS service manager and starts at login independently of the application window
- The daemon continues collecting peer deltas while the application is closed or crashed
- Application-to-daemon communication uses a local IPC socket, not in-process calls

**Verification:** Process listing confirms the daemon runs independently of the app; restart test confirms deltas received during app downtime are present when the app reconnects.

#### `ch03-inverted-stack-one-diagram:INV-08` — Three-tier peer discovery hierarchy

Peer discovery follows a fixed hierarchy — mDNS on the local network, mesh-VPN (WireGuard-based) for NAT traversal across networks, and the managed relay as the final fallback.

**Kleppmann:** `P3, P4, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `peer-discovery-failure`

**Must implement:**

- Daemon attempts mDNS discovery on the local network first
- Daemon falls back to mesh-VPN peer discovery across networks
- Daemon uses the managed relay only when neither prior tier yields peers
- Each tier is independently configurable and removable

**Verification:** Daemon trace shows the three-tier order on cold start; LAN-only test confirms two devices on the same Wi-Fi sync with no relay traffic.

#### `ch03-inverted-stack-one-diagram:INV-09` — Gossip anti-entropy with vector clocks

The daemon converges peer state through periodic gossip — every 30 seconds it selects two random peers, exchanges deltas based on vector-clock divergence, and streams missing CRDT operations using CBOR encoding.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Daemon selects gossip partners on a periodic schedule with random peer selection
- Vector clocks track per-peer operation visibility
- Delta payloads use CBOR wire encoding
- Gossip operates correctly with no central coordinator

**Verification:** Wire trace confirms CBOR-encoded delta exchange on the configured interval; multi-peer convergence test demonstrates byte-identical state across peers after gossip rounds.

#### `ch03-inverted-stack-one-diagram:INV-10` — Write buffering with durable local commit before peer delivery

When no peers are reachable, the daemon accepts writes from the application logic layer and buffers them to the durable local event log before acknowledgement, then drains the buffer when any peer becomes reachable.

**Kleppmann:** `P3, P5` · **Scope:** `foundational` · **Failure modes:** `partition, vendor-outage`

**Must implement:**

- Buffered writes commit to the local event log before the daemon acknowledges them
- A power interruption between buffering and peer delivery does not lose buffered data
- The daemon resumes buffer drainage automatically when a peer becomes reachable
- The application is not required to track whether a write was buffered or delivered

**Verification:** Durability test interrupts power after buffering and before delivery, then asserts the write replays from the event log on restart and reaches peers when reconnected.

#### `ch03-inverted-stack-one-diagram:INV-11` — Storage layer with CRDT store, event log, and read-model projections

The storage layer holds three coexisting structures — a typed CRDT document store, an append-only event log as the ground truth, and rebuildable read-model projections — all backed by SQLite encrypted with SQLCipher and a key derived via Argon2id and held in the OS keystore.

**Kleppmann:** `P5, P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise, key-loss`

**Must implement:**

- All AP-class data is stored as typed CRDT documents (map, list, text)
- The event log is append-only and never modifies past entries
- Read-model projections are rebuildable from the event log
- The database is encrypted with SQLCipher using an Argon2id-derived key stored in the OS-native keystore

**Verification:** Storage layer exposes the three structures as separate APIs; recovery test rebuilds projections from the event log; key-extraction test confirms physical storage extraction without credentials yields ciphertext only.

#### `ch03-inverted-stack-one-diagram:INV-12` — Engine-agnostic CRDT abstraction

The CRDT engine is consumed through an abstraction (`ICrdtEngine`) so that the choice between YDotNet (current) and Loro (aspirational target) is reversible without changes to the application layer.

**Kleppmann:** `P5, P7` · **Scope:** `foundational`

**Must implement:**

- Application code consumes only the engine abstraction, not engine-specific types
- Adding a new engine implementation requires no changes to application logic
- Merge semantics are commutative, associative, and idempotent across all engines behind the abstraction

**Verification:** Test suite runs the same convergence scenarios against multiple engine implementations and asserts byte-identical merged state.

#### `ch03-inverted-stack-one-diagram:INV-13` — Relay as ciphertext-only optional peer

The relay is an optional component that receives, fans out, and rendezvous-routes encrypted CRDT deltas without ever holding decryption keys, decrypted content, or authoritative data.

**Kleppmann:** `P3, P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection, vendor-acquisition`

**Must implement:**

- The relay holds no keys for any payload it routes
- The relay stores no plaintext from any peer
- The relay protocol is open and the relay is self-hostable
- Removing the relay leaves LAN and mesh-VPN sync unaffected

**Verification:** Relay process inspection confirms no key material is present; protocol fuzz test confirms the relay rejects any request that requires plaintext access; replacing the managed relay with a self-hosted relay requires no node configuration change.

#### `ch03-inverted-stack-one-diagram:INV-14` — Two relay trust levels — relay-only and attested hosted peer

The relay operates at one of two declared trust levels — relay-only ciphertext routing as the default, or attested hosted peer that participates in CP-class quorum via an explicit administrator-issued role attestation.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise, vendor-acquisition`

**Must implement:**

- Default relay deployment is relay-only and cannot decrypt payloads
- Attested hosted peer mode requires an explicit role attestation issued by an administrator
- Trust level is visible to all peers participating in the topology

**Verification:** Configuration audit confirms default relay deployment lacks any role attestation; integration test confirms an unattested relay is excluded from quorum decisions.

#### `ch03-inverted-stack-one-diagram:INV-15` — Mirror-inversion of Ch01 failure modes

The inversion specifically resolves each of Ch01's six named SaaS failure modes — The Outage and The Dependency Chain, The Vendor, The Connectivity, The Data, The Price, and The Third-Party Veto — by removing the vendor's data custody as the load-bearing dependency.

**Kleppmann:** `P3, P5, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, partition, vendor-acquisition, vendor-outage`

**Must implement:**

- Local authoritative state survives any upstream cloud-region outage
- Vendor business changes do not interrupt access to user data
- Connectivity enables sync but is not a prerequisite for function
- User data is exportable in a standard format without vendor participation
- Switching costs are bounded by relay replacement, not full data extraction
- Disaggregation of data custody from service custody limits third-party veto exposure

**Verification:** Failure-mode regression tests for each named mode confirm continued local function and data accessibility; export test produces a standard-format archive without vendor API calls.

#### `ch03-inverted-stack-one-diagram:INV-16` — The Security Breach as hidden-exposure reveal

SaaS exposes users to a structurally invisible failure mode — vendor-side breach of decryptable copies — that the inverted architecture neutralizes by ensuring the relay only ever holds ciphertext sealed under per-document DEKs wrapped by role KEKs whose keys never leave the originating node.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, key-compromise`

**Must implement:**

- Per-document data encryption keys (DEKs) are generated and held only on originating nodes
- DEKs are wrapped by role-scoped key encryption keys (KEKs) at the source node
- No relay or hosted infrastructure component receives any DEK or KEK material
- A complete breach of relay infrastructure exposes no decryptable content

**Verification:** Threat-model audit demonstrates no key material crosses the node boundary; relay breach simulation produces only ciphertext payloads with no path to plaintext.

#### `ch03-inverted-stack-one-diagram:INV-17` — Honest new failure modes introduced by the architecture

The inversion introduces three categorically new operational concerns — endpoint-compromise expansion of the attack surface, schema migration across independently-updating nodes, and CRDT garbage-collection debt across long-lived peers — each of which the architecture addresses but does not eliminate.

**Kleppmann:** `P5, P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise, partition, schema-skew`

**Must implement:**

- Endpoint defense uses layered controls (encryption at rest, field-level encryption, sync-layer minimization, circuit-breaker quarantine)
- Schema evolution uses additive expand-contract changes, bidirectional lenses, and quorum-coordinated schema epochs for breaking changes
- CRDT history is bounded by a tiered GC policy with a stale-peer recovery protocol

**Verification:** Threat model documents endpoint compromise scenarios and the four-layer defense mapping; migration test runs five concurrent schema versions to convergence; GC test reintegrates a peer offline for longer than the active retention window.

#### `ch03-inverted-stack-one-diagram:ZONE-01` — Anchor as Zone A — offline-by-default local-first deployment shape

Anchor is the Zone A canonical shape — a .NET MAUI Blazor Hybrid native application running on Windows and macOS desktops with data in a local SQLCipher SQLite database, an Ed25519 device-identity keypair generated at first run, and opt-in sync.

**Kleppmann:** `P1, P3, P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection, vendor-outage`

**Must implement:**

- Application runs and is fully functional with sync disabled from first launch
- Device identity is a long-lived Ed25519 keypair generated locally and held in the OS keystore
- Local SQLite/SQLCipher database is the authoritative store for the device
- Enabling sync is an explicit user action, not a precondition for function

**Verification:** Fresh install with networking disabled completes setup and supports all core workflows; keystore inspection confirms a per-device Ed25519 keypair was generated locally.

#### `ch03-inverted-stack-one-diagram:ZONE-02` — Bridge as Zone C — hybrid multi-tenant SaaS deployment shape

Bridge is the Zone C canonical shape — a .NET Aspire / Blazor Server hosted application that runs a dedicated local-node host process and dedicated SQLCipher database per tenant, defaulting to ciphertext-only relay participation in the tenant's gossip scope.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection, key-compromise`

**Must implement:**

- Each tenant gets a dedicated local-node host process with its own SQLCipher database
- Per-tenant data planes are isolated and not shared across tenants
- The hosted node defaults to ciphertext-only participation in the tenant gossip scope
- Tenant-issued role attestation is required before the hosted node participates in CP-class quorum

**Verification:** Multi-tenant deployment audit confirms one host process and one database per tenant; default deployment lacks any role attestation; integration test confirms cross-tenant data is unreachable.

#### `ch03-inverted-stack-one-diagram:ZONE-03` — One architecture, two deployment shapes

Anchor and Bridge use the same Sunfish component surface, sync protocol, CAP positioning model, and storage architecture; they differ only in where the authoritative data location lives.

**Kleppmann:** `P3, P4, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Both shapes consume the same `Sunfish.Kernel.Sync` and `Sunfish.Foundation.LocalFirst` packages (pre-1.0)
- Sync wire protocol is identical across shapes
- Choosing between shapes is a deployment-time decision, not a code-fork decision

**Verification:** Reference implementation builds both shapes from the same kernel packages; protocol conformance tests pass identically against an Anchor peer and a Bridge tenant peer.

#### `ch03-inverted-stack-one-diagram:INV-18` — Three developer-habit shifts under the inversion

Building under the inversion shifts three habits — writes succeed on local durability rather than remote acknowledgement, business logic owns its correctness independently of the network, and failure modes are explicit rather than papered over.

**Kleppmann:** `P1, P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition, vendor-outage`

**Must implement:**

- Command handlers acknowledge on local-store commit, not on remote server response
- Every state mutation is expressed as a CRDT operation, not a current-state assignment
- Validation, invariants, and state machine transitions execute against local data with no implicit network shortcut
- Sync conflicts surface to a conflict inbox rather than via silent overwrite

**Verification:** Code review confirms no command handler awaits a remote response before acknowledgement; static analysis confirms no validator imports a network client; UI inventory confirms a conflict-inbox surface exists.


### Epic: Choosing Your Architecture (ch04-choosing-your-architecture)

**Source-paper refs:** v13 §20.2, v13 §20.3, v13 §20.4, v13 §20.5, v13 §20.6, v13 §20.7, v13 §20.8

**Concept count:** 15

#### `ch04-choosing-your-architecture:DEC-01` — The One Question (user-owned vs aggregated value)

The architecture-determining question is whether the primary value of the software comes from the user's own data or from data aggregated across many users.

**Kleppmann:** `P5, P7` · **Scope:** `foundational`

**Must implement:**

- Architecture decision record states the answer to the One Question for the product's primary records
- Aggregated-value features are scoped to a separate service layer when present alongside user-owned primary records
- Local-node architecture is selected only when primary value is user-owned

**Verification:** Architecture decision record names the primary records, identifies their natural owner, and cites the One Question answer as the basis for selecting Zone A, B, or C.

#### `ch04-choosing-your-architecture:DEC-02` — Mixed-ownership architecture pattern

A product whose primary records are user-owned but which also exposes aggregated surfaces routes the primary records through the local-node data plane and treats aggregated surfaces as optional read models on a separate service layer.

**Kleppmann:** `P3, P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-outage`

**Must implement:**

- Primary user-owned records live on the local-node data plane
- Aggregated surfaces (org dashboards, cross-team reports, benchmarking) are served by a separate service that treats local nodes as the source of truth
- Aggregated read models are not authoritative; loss of the aggregation service does not impair access to primary records

**Verification:** System diagram shows aggregated surfaces as downstream consumers of node-sourced data; integration test confirms primary records remain readable and writable after the aggregation service is stopped.

#### `ch04-choosing-your-architecture:FILT-01` — Filter 1 — Consistency requirements (hard stop)

A disqualifying check that rejects local-first architecture when the domain requires atomic cross-user transactions, intolerance for stale data, or millisecond-identical truth across all peers.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Architecture review explicitly evaluates whether primary records require atomic cross-user consistency as a moment-to-moment invariant
- Domains requiring globally consistent state at settlement (payments processors, exchanges, real-time inventory) are routed to centralized architecture
- CP-class subsystems (e.g., the double-entry ledger) are scoped as deliberately specified components, not as the product's core loop

**Verification:** Architecture decision record answers all four Filter 1 questions in writing; any "yes" to atomic cross-user transactions, dangerous stale data, or millisecond-identical truth requirements documents the centralized routing for that subsystem.

#### `ch04-choosing-your-architecture:FILT-02` — Filter 2 — Data ownership profile

A check that classifies the natural owner of the primary records by who creates them, who uses them, and who suffers loss when access is severed — distinguishing user-owned, vendor-aggregated, and regulator-custodied profiles.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, vendor-acquisition`

**Must implement:**

- Architecture decision record names the natural owner of each primary record type
- Vendor-aggregated-as-product use cases are routed to centralized storage
- Regulatory-custodian regimes (HIPAA BAA scope, FINRA 4511 / SEC 17a-4 WORM, ITAR) are identified before architecture selection and route specific retention flows to the required custodian
- Mixed-ownership products use Zone C with user-owned primary records and aggregated surfaces on a separate service

**Verification:** Architecture decision record cites the data-ownership profile per primary record type; regulator-custodian flows reference the specific regulation (HIPAA, FINRA, ITAR, etc.) and the custodial mechanism used.

#### `ch04-choosing-your-architecture:FILT-03` — Filter 3 — Connectivity and operational environment

A check that names the actual deployment environment and routes to local-first when users operate in field, air-gapped, regulated-residency, clinical, or chronically intermittent-connectivity conditions.

**Kleppmann:** `P1, P3` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, vendor-outage`

**Must implement:**

- Architecture decision record names the physical deployment environment of the primary user, not the cloud provider's SLA
- Field, air-gapped, MDM-governed, residency-regulated, and chronically-intermittent environments route to local-first as mandatory or strongly preferred
- The product treats absence of network as a normal operating mode, not a degraded one — input is accepted and writes are queued without network access
- Always-online browser-only zero-install scenarios are the only category routed to traditional SaaS at this filter

**Verification:** Architecture decision record names the actual environments; behavioral test confirms the application accepts input and persists writes with no network present, distinguished from a degraded-but-online state.

#### `ch04-choosing-your-architecture:FILT-04` — Filter 4 — Business model alignment

A check that rejects local-first when revenue depends on controlling user access to their own data, and confirms it when revenue derives from service quality, managed relay, support, tooling, or dual-licensed open-core offerings.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- Architecture decision record states the revenue model and confirms it does not require gating user access to user-owned data
- Revenue paths that depend on data-custody lock-in are explicitly disqualified
- Managed relay is specified as replaceable infrastructure, not a data custodian — relay failure degrades sync but never local operation or data access
- Dual-licensing patterns (open-source core plus commercial managed offering) are recognized as the strongest alignment for this architecture

**Verification:** Business model document names the revenue path; relay-failure test confirms local operation and data access continue unaffected; user data export is supported without vendor mediation.

#### `ch04-choosing-your-architecture:FILT-05` — Filter 5 — Team capability and timeline

A check that governs when and how to adopt local-first by honestly assessing whether the team has CRDT, distributed-state, multi-version schema, and key-management skills, and whether the timeline accommodates the required investment.

**Scope:** `foundational` · **Failure modes:** `key-compromise, key-loss, schema-skew`

**Must implement:**

- Team capability assessment names CRDT debugging, distributed state management, multi-version schema migration, and key management as the four required skills
- Timeline budgets 3–6 months for CRDT and sync work and 1–3 months for key management before naming a production date
- Sub-3-month timelines route to Zone C (start with traditional SaaS, architect for local-node migration from day one)
- Existing hosted products with established users route to Zone C incremental migration, not Zone A greenfield rebuild
- Greenfield projects with adequate timeline and capability route to Zone A

**Verification:** Project plan documents the four-skill capability assessment, the CRDT/sync and key-management budgets, and the resulting Zone selection; production date is not set before the key-management budget elapses.

#### `ch04-choosing-your-architecture:DEC-03` — Zone A — Local-first node outcome

The outcome when all five filters clear and the team has timeline and capability to build the full local-first node from the start, where every user runs a complete local node and the relay is optional infrastructure.

**Kleppmann:** `P1, P2, P3, P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- Every user runs a complete local node holding authoritative state
- The relay is optional infrastructure for peer discovery and backup, not a runtime dependency
- The application operates at full fidelity with no server reachable
- Domain fit is single-tenant or team-scoped productivity, professional or enterprise users, software whose value exists before any other user joins

**Verification:** Integration test confirms the application provides full functionality with no relay reachable; reference implementation is the Anchor accelerator under Sunfish.

#### `ch04-choosing-your-architecture:DEC-04` — Zone B — Centralized SaaS outcome (when local-first is wrong)

The outcome when Filter 1 or Filter 2 returns a hard "centralized only" verdict, applying to multi-tenant aggregation as core value, anonymous public access, millisecond global consistency requirements, and pure content delivery.

**Scope:** `foundational`

**Must implement:**

- Architecture decision record cites the specific Filter 1 or Filter 2 result that routed the product to centralized
- Local-first is not retrofitted onto a domain whose primary value is aggregated state or whose core loop requires CP-class consistency
- The architecture serves the domain — building financial trading infrastructure on a local-node architecture is recognized as wrong for the domain

**Verification:** Architecture decision record names which filter forced Zone B and identifies the aggregated value or consistency invariant that justifies centralization.

#### `ch04-choosing-your-architecture:DEC-05` — Zone C — Hybrid outcome

The outcome when filters pass for user-scoped primary records but fail for specific coordination features, or when Filter 5 indicates a timeline incompatible with full Zone A investment, where the local node handles user-owned data and a cloud relay handles sync, cross-organization collaboration, payments, and compliance reporting.

**Kleppmann:** `P3, P4, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-outage`

**Must implement:**

- The local node holds all user-owned data and performs all day-to-day compute
- The cloud relay handles sync, cross-organization collaboration, payment-class transactions, and compliance reporting
- A traditional web layer handles public-facing surfaces when present
- Hybrids are designed with an explicit trajectory toward Zone A; server-side logic is not allowed to accumulate indefinitely

**Verification:** Architecture decision record documents which features run on the relay versus the node; reference implementation is the Bridge accelerator under Sunfish; periodic review confirms server-side logic has not re-centralized authoritative state.

#### `ch04-choosing-your-architecture:DEC-06` — The Practical Shortcut (three-question prefilter)

A three-question prefilter — primary-record ownership, sustained-offline requirement, vendor-outlive requirement — that determines whether a full five-filter evaluation is worth the time for a project in early discovery.

**Kleppmann:** `P3, P5, P7` · **Scope:** `foundational` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- Discovery-stage projects answer the three shortcut questions before committing to a full filter evaluation
- All-yes answers route to Zone A (Anchor) for greenfield or Zone C (Bridge) for migration
- A "no" answer maps to a specific filter for full evaluation (Q1 → Filter 2, Q2 → Zone C tolerance, Q3 → Filter 4)
- The shortcut is not a substitute for the full five filters in a production architectural decision

**Verification:** Discovery-stage architecture note records the three shortcut answers and either cites the resulting Zone or names the filter requiring full evaluation.

#### `ch04-choosing-your-architecture:DEC-07` — Vendor-outlive requirement

The requirement that the product keep working regardless of whether the vendor survives, is acquired, changes pricing, or is directed to stop serving a given jurisdiction — making vendor-independent authoritative data custody a structural, not contractual, property.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- Authoritative data lives on infrastructure under the user's or customer's control
- The application functions without vendor server availability
- Data export is not gated by vendor permission or active subscription
- Recovery from vendor disappearance does not require vendor cooperation

**Verification:** Behavioral test simulates vendor service permanently unavailable; the application continues to function on local data and a documented procedure exists for replacing vendor-provided relay infrastructure without data migration.

#### `ch04-choosing-your-architecture:DEC-08` — Degraded-vs-absent network distinction

An operational distinction that treats an application loading stale data and queueing writes as degraded (still working) and an application showing a spinner and refusing input as broken — establishing absence-tolerance, not graceful-degradation, as the local-first acceptance criterion.

**Kleppmann:** `P1, P3` · **Scope:** `foundational` · **Failure modes:** `vendor-outage`

**Must implement:**

- The application accepts user input with no network present
- Writes are persisted locally and queued for sync without blocking the UI
- Reads return locally available data without spinners on network absence
- Failure to reach the network never produces a refused-input state

**Verification:** Behavioral test disables all network interfaces and exercises the application's primary write and read paths; no spinner appears on network absence and no input is refused.

#### `ch04-choosing-your-architecture:DEC-09` — Four required local-first engineering skills

The four engineering skills that separate local-node development from standard web application development — CRDT debugging, distributed state management, multi-version schema migration, and key management.

**Kleppmann:** `P4, P5, P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise, key-loss, partition, schema-skew`

**Must implement:**

- Team has practitioners who can reason about CRDT type semantics and merge order under uncertainty
- Team manages authoritative local state under concurrent local edits, incoming sync deltas, and schema migrations with explicit design
- Team applies the expand-contract pattern for schema migrations across a distribution of in-field versions
- Team designs and implements key rotation, revocation, and recovery procedures before first production deployment

**Verification:** Capability matrix documents named owners for each of the four skills; key compromise recovery procedure exists in writing before the first production deployment date is set.

#### `ch04-choosing-your-architecture:DEC-10` — Replaceable-relay invariant

The structural property that the managed relay is replaceable infrastructure rather than a data custodian, such that relay failure degrades sync and cross-organization collaboration but never affects local operation or data access.

**Kleppmann:** `P3, P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- Relay failure does not affect local operation or data access on any node
- A team can replace its relay provider without data migration
- The relay holds no authoritative state that is not also held on at least one node
- Cross-organization collaboration is the only function that requires a reachable relay

**Verification:** Behavioral test stops the relay and confirms full local operation continues; relay-replacement procedure swaps providers without migrating authoritative data.


---

## Part II — Council perspectives

### Epic: The Enterprise Lens (ch05-enterprise-lens)

**Source-paper refs:** v13 §16, R1 Voss, R2 Voss

**Concept count:** 15

#### `ch05-enterprise-lens:LENS-E-01` — MDM compliance attestation at capability negotiation

Before a node joins the sync mesh and exchanges data, it must present a valid compliance attestation from the organization's Mobile Device Management platform during capability negotiation, with non-compliant nodes rejected at the gate rather than after data exchange.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Sync daemon handshake includes an MDM compliance attestation phase before capability exchange completes
- A node failing the compliance attestation is rejected before any data frame is transmitted
- Compliance is validated continuously at the point of access, not only at installation time
- Attestation freshness is enforced; expired attestations cause rejection

**Verification:** Sync daemon protocol specification defines a pre-capability MDM compliance phase; behavioral test confirms a node with revoked or expired MDM attestation is rejected at handshake before receiving any record payload.

#### `ch05-enterprise-lens:LENS-E-02` — Platform-agnostic MDM integration with regional coverage

The MDM compliance attestation protocol is platform-agnostic at the architecture level and ships with documented integration patterns for at least the dominant Western and non-Western enterprise MDM platforms used in target markets.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Compliance attestation protocol defines a platform-neutral interface, not a vendor-specific binding
- Documented integration patterns exist for Intune, Jamf, and SCCM
- Documented integration patterns exist for SOTI MobiControl, IBM MaaS360, and Ivanti Endpoint Manager
- At least six MDM platforms are named with concrete integration guidance

**Verification:** Architecture documentation enumerates the supported MDM platforms with per-platform integration guides; protocol specification shows the attestation interface accepts attestations from any conforming MDM source.

#### `ch05-enterprise-lens:LENS-E-03` — Build-time SBOM generation in CycloneDX format

A Software Bill of Materials is generated at build time from source by the CI pipeline in CycloneDX format, scanned against vulnerability databases before release, and published with each release artifact.

**Kleppmann:** `P5, P6` · **Scope:** `foundational`

**Must implement:**

- SBOM is produced at build time from the dependency graph, not assembled post-install
- SBOM is published in CycloneDX format that satisfies NTIA minimum elements and CISA guidance
- CI pipeline scans the SBOM against NVD and OSS vulnerability databases before release
- SBOM is published alongside each release artifact

**Verification:** CI pipeline configuration shows Syft (or equivalent) producing CycloneDX SBOM at build, Grype (or equivalent) scanning before release; release artifact directory contains the SBOM file for the corresponding binary.

#### `ch05-enterprise-lens:LENS-E-04` — Signed and notarized installer with trusted-publisher compatibility

Installers are code-signed and notarized using each platform's enterprise-grade signing path so that the software can be added to organizational trusted-publisher lists and deployed via MDM without disabling endpoint security policies.

**Kleppmann:** `P6` · **Scope:** `foundational`

**Must implement:**

- macOS installer is signed with an Apple Developer ID and notarized
- Windows installer is Authenticode-signed and compatible with App Control for Business (WDAC) trusted-publisher policies
- Installer supports silent installation without user elevation in MDM-managed deployments
- No installation step requires disabling platform security policies

**Verification:** Release artifact passes platform notarization checks; deployment dry run via Intune or equivalent silently installs the software on a managed endpoint with default security policies enabled.

#### `ch05-enterprise-lens:LENS-E-05` — CVE response service-level commitment

The project commits to a public service-level agreement on vulnerability response, with critical CVEs addressed within fourteen days of disclosure and a public advisory posted within forty-eight hours of patch release.

**Kleppmann:** `P6` · **Scope:** `foundational`

**Must implement:**

- Critical CVEs are addressed by a patch release within fourteen days of disclosure
- A public security advisory is posted within forty-eight hours of patch availability
- SLA terms are published in the project's security policy
- SBOM-driven scanning surfaces affected dependencies in time to meet the SLA

**Verification:** Project security policy publishes the CVE response SLA; historical advisories show patch-to-disclosure intervals within the committed window.

#### `ch05-enterprise-lens:LENS-E-06` — Defined incident response runbook

A formal incident response runbook accompanies the architecture, specifying triggering events, artifact collection sequence, chain of custody requirements, escalation path, and jurisdiction-specific regulatory notification windows, distinct from and complementary to the CRDT audit trail.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Runbook enumerates the triggering events (suspected unauthorized node access, unauthorized device in sync mesh, key compromise, relay-traffic exfiltration)
- Runbook specifies which artifacts are collected from which systems in what order
- Runbook defines chain-of-custody procedures for collected artifacts
- Runbook defines escalation timing (CISO within one hour, legal within four hours when personal data is implicated)
- Runbook enumerates per-jurisdiction regulatory notification windows (GDPR Article 33 72 hours, HIPAA 60 days, DPDP, PIPA, PIPL, NDPR, POPIA, LGPD, 242-FZ) with cross-reference to Appendix F

**Verification:** Companion runbook document exists alongside architecture spec; runbook contains each enumerated section; tabletop exercise executes the runbook end-to-end against a simulated incident.

#### `ch05-enterprise-lens:LENS-E-07` — CRDT audit trail as forensic asset distinct from procedure

The tamper-evident append-only CRDT operation log is positioned and documented as a forensic asset that supports incident response, not as a substitute for a defined incident response procedure.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Every write operation is recorded in a tamper-evident append-only operation log
- Sync daemon can reconstruct full record history from the operation log
- Documentation distinguishes the audit trail (forensic asset) from the runbook (procedure)
- Audit-trail outputs are referenced as inputs to runbook artifact collection steps

**Verification:** Architecture documentation explicitly separates audit-trail capability from incident response procedure; runbook references audit-trail extraction as a defined collection step.

#### `ch05-enterprise-lens:LENS-E-08` — Zero-downtime rolling update with health-gated rollback

Container updates apply via a rolling update that promotes a new image to one replica, runs a defined health-check sequence, and only rotates remaining replicas on success, with automatic rollback to the prior image on health-check failure.

**Kleppmann:** `P1, P3` · **Scope:** `foundational`

**Must implement:**

- Container orchestration applies updates incrementally to one replica before the rest
- A defined health-check sequence runs against the updated replica before further rotation
- Failed health checks trigger automatic rollback to the previous image
- Typical updates complete without a maintenance window

**Verification:** Deployment manifests define the rolling-update strategy and health-check sequence; failure-injection test confirms automatic rollback when the health check fails on the updated replica.

#### `ch05-enterprise-lens:LENS-E-09` — Enterprise network footprint and proxy compatibility

The node exposes no inbound ports on external interfaces, routes all relay traffic exclusively over port 443 with TLS 1.3, and respects system proxy configuration including PAC files, authenticating proxies, and TLS-inspecting corporate proxies via documented bypass-list format.

**Kleppmann:** `P3, P6` · **Scope:** `foundational` · **Failure modes:** `peer-discovery-failure`

**Must implement:**

- No inbound ports are opened on any external interface
- All relay traffic uses port 443 with TLS 1.3
- Sync daemon honors system proxy configuration including PAC files
- Sync daemon authenticates against authenticating corporate proxies
- Documentation specifies the bypass-list entry format for environments performing TLS inspection

**Verification:** Network audit on a managed endpoint confirms zero inbound listeners and port-443-only outbound; proxy compatibility test passes the daemon through a PAC-configured authenticating proxy and through a TLS-inspecting proxy with a documented bypass entry.

#### `ch05-enterprise-lens:LENS-E-10` — Documented Podman substrate choice for Windows

For Windows deployments, the architecture documents the choice between WSL2 and Hyper-V as the Podman substrate with recommended defaults and known compatibility constraints with existing virtualization products.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Documentation names WSL2 as the recommended default substrate for most deployments
- Documentation names Hyper-V as the recommended substrate for organizations already standardized on it
- Documentation flags WSL2 incompatibility with Group Policy environments that disable the Linux subsystem
- Documentation flags Hyper-V conflict with VMware Workstation Pro and similar products
- Deployment guide directs IT administrators to verify virtualization-product compatibility before rollout

**Verification:** Windows deployment guide contains the substrate selection section with both options, recommended defaults, and the named compatibility caveats.

#### `ch05-enterprise-lens:LENS-E-11` — Administrative tooling for capability revocation

An IT administrator interface — Admin Console, CLI, or REST endpoint — exists for triggering capability revocation, monitoring propagation across the sync mesh, and confirming completion when a user is deprovisioned.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- A concrete admin interface (console, CLI, or API) triggers capability revocation by user account
- The interface surfaces propagation progress across active peers
- The interface confirms completion when all active peers acknowledge the rotation
- Revocation completes within one capability negotiation cycle for online peers
- Admin Console is delivered before first enterprise deployment (pre-GA gating requirement)

**Verification:** Admin tooling specification documents the revocation workflow with screens or CLI invocations; integration test confirms revocation propagates and is acknowledged across a multi-peer mesh within one capability cycle.

#### `ch05-enterprise-lens:LENS-E-12` — Four-phase reversible migration model

Organizations transition from hosted tools to the local node through a four-phase model — shadow mode, partial offline editing, new-project authority, full historical migration — where each phase is independently reversible and admits indefinite pause.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- Phase one runs the local node in shadow mode with no authoritative writes
- Phase two enables offline editing for non-conflicting data domains while the hosted platform remains active for the rest
- Phase three grants the local node full authority for new projects while legacy records remain hosted
- Phase four migrates historical records via bulk import that preserves record history
- Each phase is independently reversible; rollback to the prior phase is supported
- Each phase transition has documented success criteria and rough timing heuristics for change advisory board review

**Verification:** Migration playbook documents each phase with entry, exit, and rollback procedures plus rough timing heuristics (e.g., four to eight weeks shadow-mode with sync error rate below 0.1 percent before phase two).

#### `ch05-enterprise-lens:LENS-E-13` — Dual-license structure with CLA for enterprise customization

The codebase ships under AGPLv3 with a parallel commercial license available for enterprise customers whose legal policy prohibits AGPLv3 in production, supported by a Contributor License Agreement that preserves the right to issue the commercial license.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-acquisition`

**Must implement:**

- Repository publishes AGPLv3 license at first public commit
- Parallel commercial license terms are published or available on request from first public commit
- Contributor License Agreement is required from every contributor from first public commit
- Commercial license is established before the first enterprise procurement conversation

**Verification:** Repository contains LICENSE (AGPLv3), a documented commercial license path, and a CLA process; sales documentation references the commercial license option.

#### `ch05-enterprise-lens:LENS-E-14` — Power-interruption durability as baseline property

Local writes commit to durable storage before acknowledgment so that abrupt power loss does not corrupt the local data store, and the sync daemon recovers cleanly from cold restart after unexpected shutdown.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `key-loss`

**Must implement:**

- Local writes are durably committed before the application receives an acknowledgment
- The local data store survives abrupt power loss without corruption
- The sync daemon survives cold restart after unexpected shutdown
- Durability is treated as a baseline property rather than an edge-case mitigation, including for grid-unstable deployment environments

**Verification:** Crash-injection test cuts power mid-write across many trials; on restart the data store opens cleanly with no corruption and the sync daemon resumes operation.

#### `ch05-enterprise-lens:LENS-E-15` — Structural data residency by jurisdiction

Local-first data custody satisfies data-residency requirements across major regulatory regimes (GDPR/Schrems II, India DPDP, UAE DIFC DPL 2020, Russian import-substitution, and the full Appendix F matrix) as a structural property of the deployment rather than as a configuration option.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, vendor-outage`

**Must implement:**

- User data resides on user-controlled infrastructure by default of the architecture
- Compliance with named regulatory regimes does not require special configuration toggles
- Architecture operates without dependency on Western cloud services so that import-substitution-style regimes are satisfied
- Per-jurisdiction coverage is enumerated in Appendix F

**Verification:** Compliance documentation maps each named regime to the architectural property that satisfies it; deployment audit confirms no Western cloud dependency exists in the default node configuration.


### Epic: The Distributed Systems Lens (ch06-distributed-systems-lens)

**Source-paper refs:** v13 §2, v13 §6, v13 §9, R1, R2

**Concept count:** 16

#### `ch06-distributed-systems-lens:LENS-D-01` — Convergence is not correctness

CRDT convergence guarantees that all peers reach the same state but does not guarantee that the converged state satisfies application-level correctness or domain invariants.

**Kleppmann:** `P3, P4` · **Scope:** `foundational`

**Must implement:**

- Architecture documents distinguish CRDT convergence guarantees from application correctness guarantees
- Domain invariants are validated at a layer above raw CRDT merge
- Specification names which guarantees are structural and which require application enforcement

**Verification:** Specification document explicitly separates convergence (data-structure property) from correctness (application property) and identifies the validation boundary.

#### `ch06-distributed-systems-lens:LENS-D-02` — CRDT applicability boundary by record class

CRDT merge semantics are appropriate for AP-class records where concurrent writes can be deterministically reconciled but are insufficient for CP-class records where concurrent writes produce double-bookings, oversold inventory, or duplicate sequential IDs.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Each record class is classified as AP (CRDT-merge safe) or CP (requires linearizable write coordination)
- CP-class records do not rely on CRDT merge for correctness
- AP-class records use CRDT merge as the primary reconciliation mechanism

**Verification:** Schema definitions tag each record type with its CAP class; classification is enforceable at code-review time and at runtime by the sync daemon.

#### `ch06-distributed-systems-lens:LENS-D-03` — Monotonic CRDT growth as structural property

An operation-based CRDT must retain enough operation history to deterministically merge concurrent changes from peers that have not yet seen each other's operations, causing internal state to grow monotonically with edits regardless of visible content size.

**Kleppmann:** `P3, P5` · **Scope:** `foundational`

**Must implement:**

- CRDT engine retains causal history sufficient for deterministic merge with any peer up to a defined retention horizon
- Retention behavior is documented as a structural property, not a bug
- Storage growth is bounded by an explicit GC policy rather than treated as an implementation detail

**Verification:** CRDT engine documentation states the retention guarantee in operation-history terms; storage growth observable in long-running test deployment matches the stated retention policy.

#### `ch06-distributed-systems-lens:LENS-D-04` — Three-tier GC policy by data class

Operation-history garbage collection is differentiated by data class — aggressive GC for ephemeral data, a 90-day retention window for business records, and no GC at all for compliance records.

**Kleppmann:** `P3, P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Each record type is assigned to one of three GC tiers (ephemeral, business, compliance)
- Ephemeral tier uses aggressive library-level GC and assumes no durability requirement
- Business tier guarantees at least 90 days of operation history before compaction
- Compliance tier retains full operation history indefinitely
- When a record could belong to multiple tiers, the higher tier is assigned

**Verification:** Schema definitions tag every record type with a GC tier; integration test confirms business-tier records are not compacted before the 90-day horizon and compliance-tier records are never compacted.

#### `ch06-distributed-systems-lens:LENS-D-05` — Stale peer recovery via full-state snapshot transfer

When a reconnecting peer's vector clock predates the current GC horizon, the sync daemon detects the incompatibility at CAPABILITY_NEG, abandons incremental sync, and initiates a full-state snapshot transfer that becomes the peer's new gossip baseline.

**Kleppmann:** `P3, P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition, schema-skew`

**Must implement:**

- Sync daemon CAPABILITY_NEG phase compares the reconnecting peer's vector clock against the local GC horizon
- When the vector clock predates the horizon, incremental sync is abandoned and snapshot transfer begins
- Receiving peer adopts the snapshot as a new baseline and resumes normal gossip anti-entropy from that point
- Behavior is deterministic and surfaces an explicit code path rather than a silent merge failure

**Verification:** Sync daemon protocol specifies the vector-clock-vs-horizon check at CAPABILITY_NEG; integration test simulates a peer offline past the GC horizon and confirms snapshot transfer rather than silent failure.

#### `ch06-distributed-systems-lens:LENS-D-06` — Stale peer recovery gap when no online peer holds required history

When a peer reconnects past the GC horizon and no currently online peer can serve a complete incremental stream from that peer's last vector clock, business-tier records may have an unrecoverable gap while compliance-tier records remain fully recoverable.

**Kleppmann:** `P3, P5` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Specification names exact behavior when no online peer can serve a complete incremental stream from the reconnecting peer's vector clock
- Specification states which data classes are affected by the recovery gap and which are not
- Compliance-tier no-GC policy guarantees compliance records are always recoverable in this scenario

**Verification:** Specification document includes a named edge-case section enumerating affected data classes; behavioral test confirms compliance-tier records survive the scenario while business-tier gaps are surfaced explicitly.

#### `ch06-distributed-systems-lens:LENS-D-07` — Flease lease protocol for CP-class records

Flease provides leader-free distributed mutual exclusion via message-passing quorum, used to serialize linearizable writes for CP-class records such as sequential IDs, global unique constraints, and financial transaction totals.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `clock-skew, partition`

**Must implement:**

- CP-class write paths acquire a Flease lease before performing the linearizable operation
- Lease grant requires acknowledgment from a quorum of reachable peers
- No dedicated leader process is required for lease coordination

**Verification:** Architecture decision record names Flease as the chosen lease protocol; sync daemon implementation includes a lease-acquisition path gated on quorum acknowledgment for tagged CP-class operations.

#### `ch06-distributed-systems-lens:LENS-D-08` — Two-node Flease quorum with managed relay as participant

A managed relay serves as a Flease quorum participant for two-person teams, providing CP-class write guarantees without requiring a third physical node and resolving the threshold problem that affects small-team consensus.

**Kleppmann:** `P3, P4, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Managed relay implements the Flease quorum participant role for teams below the natural quorum threshold
- Two-node teams achieve CP-class write guarantees using node-plus-relay quorum
- Relay participation is architecturally bounded and does not extend to payload visibility

**Verification:** Sync daemon protocol specification documents the relay-as-quorum-participant role; integration test demonstrates a two-node team performing CP-class writes through node + relay quorum and failing safely when the relay is partitioned.

#### `ch06-distributed-systems-lens:LENS-D-09` — Flease split-write fence for unmergeable CP records

For CP-class records where two concurrent writes cannot be merged at all (sequential IDs, unique constraints), a new lease holder must receive acknowledgment from all reachable peers that the previous lease has expired and no in-flight write is pending before accepting the first new write.

**Kleppmann:** `P3, P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- New lease holder issues a fence message confirming expiry of the previous lease before accepting writes
- Fence requires acknowledgment from all reachable peers, not only quorum
- Behavior is honest about the crash-failure model and does not claim Byzantine safety

**Verification:** Sync daemon protocol specification documents the lease-fence handshake; behavioral test confirms a new lease holder rejects writes until fence acknowledgments from all reachable peers are received.

#### `ch06-distributed-systems-lens:LENS-D-10` — Post-merge invariant validation for AP-backed CP constraints

For records where a CP constraint is a domain invariant layered on top of an AP data structure, CRDT merge resolves concurrent writes into a deterministic state and the domain invariant is enforced as a post-merge validation step rather than via lease coordination.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Records of this hybrid class use CRDT merge as the structural reconciliation mechanism
- Domain invariants are evaluated against the merged state, not per-write
- Validation failures surface through the conflict-inbox path rather than data corruption

**Verification:** Schema definition identifies hybrid AP-with-domain-invariant record types; semantic-layer code includes post-merge validation hooks for these types; behavioral test confirms invariant violations after concurrent merges are surfaced rather than silently committed.

#### `ch06-distributed-systems-lens:LENS-D-11` — Enumerate linearizable operations before development

Implementers must identify every operation in their domain model that requires CP-class linearizable semantics before committing to an implementation strategy, treating the architecture's named examples as illustrative rather than exhaustive.

**Kleppmann:** `P3, P4` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Project bootstrap process includes a linearizable-operation inventory step before schema design
- Each domain operation is explicitly classified as AP-mergeable or CP-linearizable
- Inventory captures non-obvious cases (inventory quantities, appointment slots, resource allocations)

**Verification:** Project template includes a linearizable-operation inventory artifact; chapter checklists or playbooks reference the inventory step before any record-type implementation begins.

#### `ch06-distributed-systems-lens:LENS-D-12` — CRDT store as durable outbound buffer

The local CRDT store itself serves as the durable outbound operation buffer during partition, so operations are persisted across process restarts and re-read by the sync daemon on reconnection rather than queued in a separate in-memory buffer.

**Kleppmann:** `P3, P5` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Sync daemon does not maintain a separate in-memory-only outbound queue for unsent operations
- Outbound operations are persisted to the CRDT store and re-read on reconnect
- Buffer capacity is bounded only by local disk capacity, not in-memory queue size

**Verification:** Sync daemon implementation reads pending outbound operations from the CRDT store on startup; integration test confirms operations survive process restart during partition and are transmitted on reconnect.

#### `ch06-distributed-systems-lens:LENS-D-13` — Schema-validation gate at CRDT store entry

Before an operation is applied locally and queued for gossip, the sync daemon validates it against the current schema definition for the operation's record type, quarantining structurally valid but semantically incorrect operations rather than letting them propagate.

**Kleppmann:** `P3, P4, P6` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Sync daemon validates every incoming operation against the current schema definition before insertion
- Operations failing validation are routed to the quarantine queue rather than applied
- Validation occurs prior to gossip propagation so corrupt operations do not spread

**Verification:** Sync daemon code path shows schema validation between deserialization and CRDT store apply; behavioral test injects a structurally valid but schema-violating operation and confirms it is quarantined rather than applied or propagated.

#### `ch06-distributed-systems-lens:LENS-D-14` — Break-glass recovery for corrupt operation sequences

When a buggy client version produces structurally valid but semantically incorrect operations that have already replicated to peers, recovery requires documented tooling and human judgment rather than a clean rollback because CRDT convergence makes the corruption durable.

**Kleppmann:** `P3, P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Documented break-glass procedure exists for remediating propagated corrupt operation sequences
- Recovery tooling supports compensating operations rather than retroactive deletion
- Procedure is documented before it is needed under production pressure

**Verification:** Operations runbook includes a break-glass section for corrupt-sequence remediation; tooling for issuing compensating operations exists and is tested independently of any specific incident.

#### `ch06-distributed-systems-lens:LENS-D-15` — Required test categories for sync protocol correctness

Sync protocol verification requires a defined set of test categories — network partition simulation, clock skew injection, concurrent edit generation, GC boundary conditions, Byzantine operation injection, and long-partition reconnect scenarios.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `clock-skew, partition, schema-skew`

**Must implement:**

- Test suite includes named coverage for each of the six categories
- Each category is exercisable as an isolated test fixture, not only as part of an end-to-end run
- CI gating treats absence of any category as a coverage failure for the sync protocol

**Verification:** Test directory includes labeled fixtures for partition, clock-skew, concurrent-edit, GC-boundary, Byzantine-injection, and long-partition-reconnect scenarios; CI configuration enforces presence of each.

#### `ch06-distributed-systems-lens:LENS-D-16` — Reconnection storm bandwidth governance

When many nodes reconnect simultaneously after a relay outage, a resource governor throttles per-tick bandwidth consumption so each gossip cycle processes a bounded number of exchanges rather than exhausting network or relay capacity.

**Kleppmann:** `P3, P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Sync daemon includes a resource governor that bounds per-tick gossip exchanges
- Governor parameters are explicit configuration, not implicit constants
- Behavior under simultaneous reconnect is documented rather than assumed

**Verification:** Sync daemon configuration exposes per-tick exchange limits; load test simulates simultaneous reconnect of many peers and confirms bounded bandwidth consumption per gossip cycle.


### Epic: The Security Lens (ch07-security-lens)

**Source-paper refs:** v13 §11, v5 §4, R1 Okonkwo, R2 Okonkwo

**Concept count:** 17

#### `ch07-security-lens:LENS-S-01` — Send-tier subscription filtering

Subscription filtering is enforced at the sync daemon's send tier so that a node lacking the required role attestation never receives the operations, eliminating any reliance on the application or UI to discard data it should not have.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Sync daemon evaluates subscription scope before transmitting any operation
- Application layer never receives operations the role is not authorized for
- UI components and API handlers contain no visibility-filtering logic for role-scoped data

**Verification:** Black-box test in which a node without a role attestation observes zero matching operations on the wire and zero matching rows in local storage

#### `ch07-security-lens:LENS-S-02` — Distributed attack surface acknowledgment

Distributing data to endpoints does not eliminate the honeypot problem; it relocates the honeypot to the weakest endpoint in a heterogeneous fleet whose security posture sets the effective bound for any data that endpoint holds.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Threat model documents endpoint compromise as an expected event
- Architecture bounds blast radius by role scope rather than denying endpoint exposure

**Verification:** Threat-model document enumerates endpoint compromise as in-scope and states that the weakest endpoint sets the data-at-risk bound for that endpoint's roles

#### `ch07-security-lens:LENS-S-03` — DEK/KEK envelope encryption hierarchy

A four-level hierarchy in which the root organization key wraps role KEKs, role KEKs are wrapped per authorized node with each node's public key, role KEKs wrap per-record DEKs, and DEKs encrypt ciphertext using a symmetric cipher.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise, key-loss`

**Must implement:**

- Each document is encrypted by a per-record DEK
- Each role holds a KEK that wraps the DEKs for documents in that role
- Role KEKs are wrapped per authorized node using that node's public key
- Root organization key wraps role KEKs and is held outside any per-node keystore

**Verification:** Key hierarchy diagram and code path demonstrate that decrypting any document requires unwrapping in the documented order from node key to role KEK to DEK to plaintext

#### `ch07-security-lens:LENS-S-04` — Key compromise response procedure

A specified sequence triggered by detection of KEK compromise that generates a fresh KEK not derived from the compromised key, re-wraps every DEK owned by the affected role, discards old KEK copies, broadcasts revocation through the relay, and notifies affected users with the data-at-risk window.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- System exposes detection triggers including physical-loss reports, anomalous access patterns, and explicit administrator reports
- Re-keying generates a fresh KEK independent of any compromised key material
- All DEKs owned by the affected role are re-wrapped with the new KEK
- Old KEK and all node-level wrapped copies are discarded
- Revocation is broadcast through the relay
- Affected users receive notification stating the data-at-risk window from KEK creation to revocation

**Verification:** Compromise drill executes the documented procedure end-to-end and produces revocation broadcast, re-wrapped DEKs, discarded prior key material, and a user-visible notification within a measurable interval

#### `ch07-security-lens:LENS-S-05` — Historical data-at-risk window

A compromised KEK exposes every document that KEK ever protected from the moment of key creation to the moment of revocation, so the data-at-risk window is bounded by KEK age rather than by detection latency.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Each KEK records its creation timestamp
- Incident response computes data-at-risk window from KEK creation to revocation
- User notification states the computed window explicitly

**Verification:** Incident drill produces a user notification containing a concrete data-at-risk window derived from KEK metadata

#### `ch07-security-lens:LENS-S-06` — Offline node revocation reconnection

When an offline node reconnects, the sync daemon presents its current attestation bundle to the relay, which checks the revocation log and rejects the handshake with a specific revocation error code if any key in the bundle has been revoked.

**Kleppmann:** `P3, P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Sync handshake transmits the node's current attestation bundle
- Relay consults the revocation log before accepting a handshake
- Relay returns a distinct revocation error code rather than a generic connection failure
- Node initiates re-authentication against the IdP and re-attestation flow before resuming sync
- User sees a message stating that access credentials have been updated and re-authentication is required

**Verification:** Offline-reconnect test against a node whose key has been revoked produces the documented error code, blocks sync, and surfaces the re-authentication prompt

#### `ch07-security-lens:LENS-S-07` — In-memory key material protection

Key material in process memory is protected by locked memory pages that prevent OS swap-out and is zeroed on process exit, treated as implementation constraints on the security kernel rather than as recommendations.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Memory pages holding key material are locked against OS swap
- Application zeros key material on process exit
- Constraint is enforced inside the Sunfish.Kernel.Security package

**Verification:** Process inspection confirms that pages containing key material are mlock-equivalent and that exit handlers overwrite key buffers

#### `ch07-security-lens:LENS-S-08` — Re-authentication interval

A configurable interval at which the application re-requests credentials from the OS keychain, narrowing the window in which an attacker with live-system access can extract decryption keys from running process memory.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Application supports a configurable re-authentication interval
- Default interval for high-security deployments is four hours
- Interval expiry forces credential re-prompt before further plaintext access

**Verification:** Configuration test confirms that after the interval expires the application requires fresh credentials before any further decryption operation

#### `ch07-security-lens:LENS-S-09` — Supply chain signing custody and transparency

Release artifact integrity rests on three layered controls: documented custody for the release signing key, reproducible builds that allow independent verification of binary against source, and a publicly auditable transparency log such as Sigstore that records every signing event.

**Kleppmann:** `P6, P7` · **Scope:** `foundational`

**Must implement:**

- Release signing key custody is documented, including storage and compromise procedure
- Build process is reproducible such that an independent party can rebuild the published binary from published source
- Signing events are recorded in a transparency log
- Clients reject any release whose signing event is absent from the transparency log

**Verification:** Independent rebuild matches the published artifact byte-for-byte and the signature appears in the public transparency log

#### `ch07-security-lens:LENS-S-10` — Ciphertext-only relay

The relay is treated as untrusted transport that handles only end-to-end encrypted payloads, so a relay operator who reads everything on the wire obtains operation identifiers and timestamps but no plaintext content.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- All payloads are encrypted at the originating node before entering the relay
- Relay code paths have no access to any DEK or KEK
- Relay validates and forwards ciphertext only

**Verification:** Inspection of relay process memory and storage finds no key material capable of decrypting any routed payload

#### `ch07-security-lens:LENS-S-11` — Relay traffic-analysis disclosure

A ciphertext-only relay still observes the communication graph, timing, and volume between nodes, and the architecture must disclose this metadata exposure rather than leave it for security teams to discover at deployment.

**Kleppmann:** `P6, P7` · **Scope:** `foundational`

**Must implement:**

- Documentation enumerates the metadata fields visible to the relay operator
- Self-hosted relay deployment is supported as the mitigation for metadata-sensitive contexts

**Verification:** Relay documentation lists each observable metadata channel and identifies the deployment topology that removes each

#### `ch07-security-lens:LENS-S-12` — Compelled-access threat model

A jurisdictional threat in which infrastructure operators are subject to mandatory government access requirements, addressed structurally because the relay holds only ciphertext and the keys never leave the originating device, so the operator cannot produce decryptable content under compulsion.

**Kleppmann:** `P6, P7` · **Scope:** `foundational`

**Must implement:**

- Keys are generated and held only on the originating device
- Relay holds only ciphertext at all times
- Threat model document names compelled access as a distinct named threat
- Self-hosted relay path is offered when metadata residency is also a compelled-access concern

**Verification:** Threat-model worksheet for compelled access lists the relay operator as unable to produce plaintext and references the supporting key custody and ciphertext-only properties

#### `ch07-security-lens:LENS-S-13` — Crypto-shredding for right-to-erasure

A pattern that satisfies right-to-erasure obligations against an immutable CRDT log by destroying the DEK that protects the targeted operation's content, leaving the operation entry in the log structurally intact while rendering its ciphertext permanently unreadable.

**Kleppmann:** `P5, P6, P7` · **Scope:** `foundational`

**Must implement:**

- Each erasable operation's content is encrypted under a DEK that can be uniquely identified and destroyed
- Erasure procedure destroys the DEK across all replicas and key stores
- Operation entry remains in the log with metadata intact and ciphertext as an unrecoverable stub
- Documentation names the operation-metadata residue as a known limitation

**Verification:** Erasure drill destroys the targeted DEK, confirms ciphertext is no longer decryptable on any replica, and produces a documentation artifact stating the metadata residue

#### `ch07-security-lens:LENS-S-14` — Credential recovery paths

A required set of artifact-based recovery options — recovery-key file, administrator-held wrapped KEK escrow, MDM re-enrollment plus relay-assisted re-sync — from which every deployment must select and test at least one before production, with the no-artifact case explicitly disclosed as permanent loss.

**Kleppmann:** `P5, P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-loss`

**Must implement:**

- System supports a recovery-key file generated at account setup
- System supports administrator-held wrapped KEK escrow under a defined procedure
- System supports MDM re-enrollment combined with relay-assisted re-sync
- Onboarding discloses that declining all recovery paths makes permanent loss possible
- Deployment checklist requires selection and test of at least one recovery path before production

**Verification:** Recovery drill executes each enabled path end-to-end and restores access; onboarding flow surfaces the no-artifact disclosure

#### `ch07-security-lens:LENS-S-15` — Defense-in-depth four-layer model

A non-optional composition of four enforcement layers — encryption at rest, field-level envelope encryption, stream-level send-tier data minimization, and circuit-breaker quarantine of offline writes — each built from independently audited primitives and specified before use.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Local databases are encrypted at rest with a vetted engine and Argon2id-derived keys stored in OS-native keystores
- Per-record DEKs and per-role KEKs implement field-level envelope encryption
- Subscription filtering at the sync daemon's send tier enforces stream-level data minimization
- Offline writes enter a quarantine queue on reconnection and are validated against current policy before merging

**Verification:** Architecture conformance test confirms presence and engagement of each of the four layers and that primitives in use are from the approved list

#### `ch07-security-lens:LENS-S-16` — Quarantine of reconnected offline writes

A circuit-breaker mechanism in which writes accumulated by a long-offline node enter a quarantine queue on reconnection and are validated against current team policy before being promoted into the merged state, preventing a compromised offline node from injecting malicious writes at reconnection.

**Kleppmann:** `P3, P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise, replay`

**Must implement:**

- Sync daemon detects long-offline reconnection and routes queued writes into quarantine
- Quarantine validation evaluates writes against current role attestations and policy state
- Promotion into the merged state is blocked until validation succeeds

**Verification:** Reconnect test from a node with stale attestations confirms that queued writes remain in quarantine and are rejected if current policy disallows them

#### `ch07-security-lens:LENS-S-17` — Root key custody via HSM or multi-party ceremony

The root organization key is custodied either inside a Hardware Security Module or under a documented multi-party key ceremony, with a domestic equivalent permitted in jurisdictions where Western HSM hardware is not approved.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Root organization key never resides in any per-node keystore
- Custody uses an HSM or a documented multi-party ceremony
- Deployment under import-substitution constraints uses a domestic HSM or documented multi-party ceremony equivalent

**Verification:** Custody documentation names the HSM model or the multi-party procedure and the on-call holders, and an audit confirms the root key is not present in any node-level store


### Epic: The Product & Economic Lens (ch08-product-economic-lens)

**Source-paper refs:** v13 §17, v5 §7, R1, R2

**Concept count:** 15

#### `ch08-product-economic-lens:LENS-P-01` — OSS public-good positioning as commercial strategy

Because locally installed software cannot enforce a license server for proprietary features, the commercial model treats the open-source release as the strategic asset and competes on relay quality and support depth rather than feature gating.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-acquisition`

**Must implement:**

- Full application capability is published under an open-source license rather than gated behind a paid tier
- Revenue mechanisms target managed-relay quality, support depth, and compliance amortization rather than feature access
- Project positioning is documented as infrastructure rather than as a product with locked features

**Verification:** Repository at first public release contains the full application source under an open-source license; pricing page describes the commercial offer in terms of relay, support, and compliance — not feature unlock.

#### `ch08-product-economic-lens:LENS-P-02` — First-customer archetype with named acquisition channel

A specified first customer is recorded as a tuple of job title, company size, problem, and acquisition channel — not as a demographic descriptor — so the customer development plan has an executable first step.

**Scope:** `foundational`

**Must implement:**

- Commercial plan names the first customer's job title, company size, and named pain
- Commercial plan names at least one specific acquisition channel (industry association, trade publication, or warm-introduction partner)
- Generic descriptors (e.g., "developers who care about X") are rejected as insufficient

**Verification:** Go-to-market document contains the four required fields (title, size, problem, channel) for the first customer archetype; reviewer can identify the next ten outreach targets without further interpretation.

#### `ch08-product-economic-lens:LENS-P-03` — Named OSS-to-paid conversion trigger

The commercial model names a specific user-observable event — not a need — that converts a free user into a paying customer, and the product is built so that event predictably occurs.

**Scope:** `foundational`

**Must implement:**

- The conversion trigger is named as a discrete event (e.g., "second device or second team member needs to sync and both are behind NAT")
- Product UX surfaces the paid path at the moment the trigger fires rather than through periodic upsell
- Conversion-rate measurement instruments the trigger event, not generic activity metrics

**Verification:** Product analytics define the conversion event as a measurable funnel step; the paid offer is presented in-product at the moment the trigger fires.

#### `ch08-product-economic-lens:LENS-P-04` — Vertical-first market selection on documented downtime cost

The initial target vertical is selected on three specific properties — documented connectivity failures, customer-owned legally significant data, and a measurable downtime cost — rather than on founder affinity or addressable market size.

**Kleppmann:** `P3, P5` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-outage`

**Must implement:**

- Vertical selection memo names documented connectivity-failure conditions for the target buyer
- Vertical selection memo names the legally significant data the buyer owns
- Vertical selection memo names the per-incident downtime cost in monetary terms
- Construction project management is the named launch vertical for this book's reference implementation

**Verification:** Go-to-market document records the three named selection properties for the chosen vertical; the construction-PM choice cites RFI tracking and punch lists as the candidate workflows.

#### `ch08-product-economic-lens:LENS-P-05` — Five-step customer development path

A repeatable customer development sequence — identify ten target operators through industry channels, conduct discovery interviews on a single cost-of-failure question, locate the workflow with measurable repeated cost, build directly to that scenario, then measure ninety-day relay activation on one live team.

**Scope:** `foundational`

**Must implement:**

- Step 1 names the industry-association or publication channel for identifying ten initial interview targets
- Step 2 conducts discovery interviews scoped to the question "when did software failure cost you money?"
- Step 3 selects a single workflow with measurable repeated cost
- Step 4 builds product narrowly to that workflow rather than to generic features
- Step 5 measures relay activation at ninety days on one live team and uses that data to deepen-or-pivot

**Verification:** Customer development plan in repository or product wiki contains all five named steps with owners and dates; the ninety-day activation review is on the calendar before step 4 begins.

#### `ch08-product-economic-lens:LENS-P-06` — Relay unit economics at three scale tiers

The commercial model is validated against a worked unit-economics model at 100, 1,000, and 10,000 paying teams, with per-team infrastructure cost held under two dollars per month and per-team pricing in the fifteen-to-twenty-five-dollar range, yielding gross margin above ninety percent at the 1,000-team tier.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Unit-economics model documents revenue, infrastructure cost, and gross margin at each of the three named tiers
- Per-team infrastructure cost stays under two dollars per month at 1,000 teams
- Per-team pricing falls within the documented fifteen-to-twenty-five-dollar range or names the deviation explicitly
- Gross margin at the 1,000-team tier is at least ninety percent

**Verification:** Financial model spreadsheet contains rows for each tier with revenue, infrastructure, and margin columns; relay capacity test demonstrates approximately 500 concurrent team connections on a single commodity instance.

#### `ch08-product-economic-lens:LENS-P-07` — Tier-by-tier staffing model

A staffing plan is recorded at each of the 100, 1,000, and 10,000-team tiers showing which roles each tier's revenue can fund, with external capital named explicitly as the bridge for any tier where revenue cannot fund the team required to reach the next tier.

**Scope:** `foundational`

**Must implement:**

- Staffing plan names headcount and roles at 100, 1,000, and 10,000 teams
- Each tier's plan demonstrates that revenue at that tier funds the team required to reach the next tier, or names external capital as the bridge
- The plan distinguishes Bay Area salaries from distributed-team rates as a sensitivity input

**Verification:** Operating plan contains a staffing table by tier; investor or board review confirms the bridge financing is named for any non-self-funding tier.

#### `ch08-product-economic-lens:LENS-P-08` — Dual-license structure established at repository founding

The codebase ships under AGPLv3 by default with a parallel commercial license available for organizations that cannot accept the AGPL network use clause, and the dual-license structure plus contributor license agreement is in place before the public repository opens to external contribution.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-acquisition`

**Must implement:**

- Repository publishes AGPLv3 license at first public commit
- Parallel commercial license terms are documented and obtainable without bespoke negotiation
- Contributor License Agreement is required from every external contributor before merge
- Dual-license structure is not retrofitted after community formation
- Managed-relay subscription includes the commercial license as a bundled line item

**Verification:** Repository at first public release contains LICENSE (AGPLv3), a documented commercial license path, and a CLA enforcement step in CI; release notes show no retroactive CLA collection in git history.

#### `ch08-product-economic-lens:LENS-P-09` — Project-entity copyright assignment via CLA

The contributor license agreement assigns copyright in contributed code to the project entity, preserving the entity's authority to offer the commercial license exception over the entire codebase including community contributions.

**Kleppmann:** `P5` · **Scope:** `foundational`

**Must implement:**

- The CLA grants the project entity rights sufficient to relicense the contribution under the commercial exception
- CLA collection is automated in the pull-request workflow and blocks merge without a recorded signature
- The project entity is a named legal entity capable of holding copyright assignment

**Verification:** CLA text in repository assigns inbound rights to a named project entity; CI configuration enforces a CLA-check status before any merge.

#### `ch08-product-economic-lens:LENS-P-10` — Relay defensibility through three named moats

Because the relay protocol is published and the relay binary is open-source, the managed-relay business is defended by three explicit moats — product-integrated onboarding, full-stack support depth, and amortized regulatory and compliance certification — that operate at non-infrastructure margins where commodity providers cannot compete.

**Kleppmann:** `P5, P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- Relay onboarding completes in seconds from within the application without exposing infrastructure choices to the user
- Support team is staffed to resolve cross-layer incidents (application, sync protocol, CRDT semantics, deployment) in one escalation
- Compliance program amortizes the named certifications (SOC 2 Type II, ISO 27001, HIPAA BAA, Schrems II, DIFC, India DPDP, plus the regimes named in Appendix F)
- Architecture documents that the relay is replaceable infrastructure (not a data custodian) so a buyer can self-host on relationship end without data migration

**Verification:** Onboarding test confirms a relay is configured in seconds without exposing infrastructure UI; support runbook covers cross-layer escalation paths; compliance register lists the named certifications with renewal dates; self-host migration path is documented.

#### `ch08-product-economic-lens:LENS-P-11` — Self-serve and enterprise tier separation

The pricing structure separates a self-serve tier priced at the per-team SaaS rate from an enterprise tier with negotiated pricing, contractual terms, and security-review cadence, with a documented headcount or revenue threshold marking the boundary.

**Scope:** `foundational`

**Must implement:**

- Pricing page distinguishes self-serve and enterprise tiers
- A documented headcount or revenue threshold marks the boundary between tiers
- Enterprise tier supports negotiated pricing, master-services-agreement terms, and a security-review cadence
- Self-serve customers do not consume sales-engineering or legal-review effort beyond the documented self-serve flow

**Verification:** Pricing documentation lists both tiers with the boundary criterion; an enterprise master services agreement template exists; self-serve flow requires no sales touch through purchase.

#### `ch08-product-economic-lens:LENS-P-12` — Documented project governance model

A governance model — BDFL, contributor council, or lightweight stewardship — is documented publicly before the first external pull request so the first significant disagreement has a defined resolution path rather than producing a community crisis.

**Kleppmann:** `P5` · **Scope:** `foundational`

**Must implement:**

- Repository contains a GOVERNANCE document at first public release
- The document names who approves pull requests and who decides protocol changes
- The document names the decision-making structure for unresolved disagreements
- Governance is documented before the first external contribution is accepted

**Verification:** GOVERNANCE document is present in repository at first public commit; document names PR-approval authority, protocol-change authority, and dispute-resolution path.

#### `ch08-product-economic-lens:LENS-P-13` — Region-specific go-to-market channel matrix

The commercial plan names a distinct acquisition channel per major region — product-led for US and European small teams, relationship-led with system integrators for GCC and India BFSI, agritech and fintech network distribution for Sub-Saharan Africa and Latin America, and import-substitution channels for CIS — rather than assuming a single global motion.

**Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection`

**Must implement:**

- Go-to-market plan names the dominant channel per named region
- The plan identifies system-integrator or association partners by name in relationship-led regions
- The plan names regulator-facing assets (RBI compliance documentation, Schrems II equivalence, DIFC equivalence) required as procurement enablers per region
- Product-led-growth assumptions are not extrapolated to relationship-led regions

**Verification:** Regional go-to-market document contains per-region channel and partner entries for the named regions; procurement-enablement assets are tracked per region.

#### `ch08-product-economic-lens:LENS-P-14` — Vendor-continuity risk as commercial purchasing argument

The architecture's structural ability to keep operating after vendor commercial relationship is severed — empirically anchored by the 2022 Western SaaS withdrawal from Russia and CIS markets — is positioned in procurement materials as a structural commercial claim that cloud-dependent competitors cannot make without re-architecture.

**Kleppmann:** `P3, P5, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, vendor-acquisition, vendor-outage`

**Must implement:**

- Procurement and sales materials name vendor-continuity-on-suspension as a structural property of the architecture
- The 2022 SaaS withdrawal is cited as the empirical anchor rather than as a hypothetical
- The claim is supported by demonstrable continued operation after disconnection in a tabletop or sandbox test
- Cloud-dependent competitors' inability to construct the same claim is articulated explicitly

**Verification:** Sales collateral contains the vendor-continuity claim with the 2022 anchor citation; tabletop exercise demonstrates continued local operation after simulated vendor severance.

#### `ch08-product-economic-lens:LENS-P-15` — Business-model precedence over repository opening

Because some commercial-model elements (CLA, dual-license, governance) are expensive or impossible to introduce after a community forms, the business model is specified before the repository goes public and repository-opening day is treated as a commercial event rather than only an engineering one.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-acquisition`

**Must implement:**

- Dual-license structure, CLA enforcement, and governance document are present at first public commit
- First-customer archetype, conversion trigger, vertical selection, and unit-economics tiers are documented before the repository accepts external contributions
- Repository-opening date is gated on commercial-model completion, not only on engineering readiness

**Verification:** Pre-launch checklist names the dual-license, CLA, governance, first-customer archetype, conversion trigger, vertical, and unit-economics artifacts as gating items for repository public release; first public commit contains all named artifacts.


### Epic: The Local-First Practitioner Lens (ch09-local-first-practitioner-lens)

**Source-paper refs:** v13 §13, R1 Ferreira, R2 Ferreira

**Concept count:** 16

#### `ch09-local-first-practitioner-lens:LENS-LF-01` — Plain-file application-independent export path

A user-owned local-first application must provide a single command that produces user data in durable application-independent formats — JSON for structured records, CSV for tabular data, Markdown for long-form documents — readable by any other competent software without vendor cooperation, active subscription, or network connectivity.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- Application exposes a single export command that runs entirely against the local node
- Export emits JSON for structured records, CSV for tabular data, and Markdown for long-form documents
- Export operates with no vendor cooperation, no active subscription check, and no network connectivity required
- Export output is byte-for-byte readable by software that has never seen the producing application

**Verification:** Disconnect the network, cancel the subscription if applicable, run the export command, then ingest the resulting JSON/CSV/Markdown into a different application and confirm semantic equivalence to the source records.

> Distinguished from rclone-style backup, which preserves only the internal database format and therefore delivers custody rather than ownership.

#### `ch09-local-first-practitioner-lens:LENS-LF-02` — Non-technical disaster recovery walkthrough

Recovery from total device loss is a documented step-by-step path that a non-technical user can complete unaided in under thirty minutes, ending with a working node that resumes from BYOC backup without exposing any technical surface such as bucket URLs or rclone paths.

**Kleppmann:** `P2, P5, P7` · **Scope:** `foundational` · **Failure modes:** `key-loss, vendor-outage`

**Must implement:**

- Recovery flow is specified as a sequenced user-facing walkthrough — buy device, install application, enter recovery code or scan team-member QR, confirm BYOC target, restore runs in background
- Recovery substitutes a recovery code or peer-attestation QR for the lost device's original attestation bundle
- Eager-sync buckets populate first so the user resumes role-relevant work immediately while remaining records hydrate in the background
- No step in the recovery flow requires the user to type a bucket URL, an rclone destination, or any other technical identifier

**Verification:** A non-technical tester completes end-to-end restore from a destroyed device to a working node in under thirty minutes without consulting documentation beyond in-application prompts.

#### `ch09-local-first-practitioner-lens:LENS-LF-03` — Symmetric NAT plus relay outage as documented failure mode

When both peers sit behind carrier-grade NAT and the managed relay is unavailable, direct peer-to-peer communication is impossible and the architecture documents this as a named local-only failure mode with a self-hosted-relay fallback rather than concealing it.

**Kleppmann:** `P3, P7` · **Scope:** `foundational` · **Failure modes:** `partition, peer-discovery-failure`

**Must implement:**

- Peer-discovery documentation names symmetric NAT plus relay outage as a known failure mode that produces local-only operation for both parties
- Self-hosting a relay on a host with a public IP is documented as the supported fallback that eliminates the symmetric NAT problem
- The application surfaces a clear sync-status indication when both LAN and relay paths are unreachable

**Verification:** Architecture documentation contains a section naming the symmetric NAT plus relay outage failure mode and the self-hosted-relay remediation; integration test exercises the local-only mode and confirms reads/writes succeed against local storage.

#### `ch09-local-first-practitioner-lens:LENS-LF-04` — Engine-agnostic CRDT abstraction for ecosystem reversibility

The application layer interacts with the CRDT engine through a stable abstraction such as ICrdtEngine that prevents lock-in to any specific CRDT ecosystem — Yjs, Automerge, or Loro — so the engine can be replaced without rewriting the application as the field continues to evolve.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `vendor-acquisition`

**Must implement:**

- A single interface mediates all CRDT operations consumed by the application layer
- At least one engine implementation is replaceable without changes to application code
- The abstraction surfaces map, list, text, and counter operations independent of engine-native types

**Verification:** Source tree contains an ICrdtEngine-equivalent interface; a second engine adapter (test stub or alternate implementation) exists and the application test suite passes against both.

#### `ch09-local-first-practitioner-lens:LENS-LF-05` — Peer-attestation QR onboarding bundle

A new device joins an existing workspace by scanning a QR-encoded attestation bundle from an existing peer that transfers credentials, workspace identity, and gossip-bootstrap parameters in a single out-of-band step, eliminating the credentials-require-peer chicken-and-egg failure mode of naive multi-device onboarding.

**Kleppmann:** `P2, P4, P7` · **Scope:** `foundational` · **Failure modes:** `peer-discovery-failure`

**Must implement:**

- Existing peer generates a QR-encoded bundle containing the credentials and workspace metadata required to authenticate and begin gossip
- New device authenticates and begins peer gossip using only the scanned bundle plus a network path to at least one peer
- Bundle exchange occurs out-of-band, requiring no third-party credential server

**Verification:** Pair a new device to a workspace by scanning a peer-generated QR; confirm the new device authenticates and begins receiving CRDT updates without contacting a centralized credential service.

#### `ch09-local-first-practitioner-lens:LENS-LF-06` — Container cold-start hidden behind health-gated UI

Local-first desktop applications shipped as containerized stacks must hide cold-start latency behind a persistent background service plus a health-check gate that holds the UI until the daemon is ready, eliminating the launch-pause that signals to users that the software is waiting on something remote.

**Kleppmann:** `P1` · **Scope:** `inverted-stack-specific`

**Must implement:**

- A persistent background service keeps the local container runtime warm across application launches
- The application UI does not present an interactive surface until a health check confirms the local daemon is ready
- The health gate hides implementation latency without misrepresenting the application as remote-dependent

**Verification:** Cold-launch the application from a fresh boot and confirm the UI either appears with the daemon ready or presents a deterministic loading state until readiness, with no point at which the user can interact with stale or partial data.

#### `ch09-local-first-practitioner-lens:LENS-LF-07` — Three-state backup status with dismissible at-risk banner

Backup health surfaces to the user through three escalating states — Protected (subtle), Attention (amber badge), At Risk (persistent non-blocking banner dismissible only with explicit acknowledgment) — so users do not think about working backups but cannot accidentally ignore failing ones.

**Kleppmann:** `P5, P7` · **Scope:** `foundational`

**Must implement:**

- Backup status UI exposes exactly the three named states with distinct visual treatments
- Protected state is unobtrusive and requires no user attention
- At Risk banner is persistent, non-blocking, and dismissible only via an explicit acknowledgment that records user intent

**Verification:** Force each of the three backup states in a test build and confirm the visual treatment matches specification; confirm the At Risk dismissal records an acknowledgment event in the local log.

#### `ch09-local-first-practitioner-lens:LENS-LF-08` — Recovery UX parity with backup status design

The restore experience receives the same non-technical design attention as backup status — a guided reconnection to the BYOC target, a restore-progress indicator that mirrors the three-state backup model in restore context, and zero exposure of bucket URLs or rclone paths at the moment the user is most stressed about lost work.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `key-loss`

**Must implement:**

- Restore flow guides the user through reconnecting to the configured BYOC target with the same UX register used during initial backup configuration
- Restore progress surfaces as a background-sync indicator using the three-state visual model adapted to restore semantics
- No technical identifier (bucket URL, rclone path, credential string) is exposed in the restore flow

**Verification:** A non-technical tester completes restore using only in-application prompts; UI inspection confirms no bucket URL or rclone path appears anywhere in the restore flow.

#### `ch09-local-first-practitioner-lens:LENS-LF-09` — Zero-state first-run experience as product specification

The first thirty seconds after install for a brand-new solo user with no prior data and no existing peers is specified as a product requirement that walks the user from blank state to first project, first backup configuration, and first invite — closing the most common 30-day abandonment path for local-first applications.

**Kleppmann:** `P1, P2, P4` · **Scope:** `foundational`

**Must implement:**

- The application specifies the zero-state screen explicitly — what the user sees, the first action surfaced, and the path to first project
- The first-run flow guides the user to configure a backup target before significant data is created
- The first-run flow surfaces the invite path so the workspace is not silently single-user by default

**Verification:** Install the application on a fresh device with no prior workspace; confirm the user reaches a first project, a configured backup target, and an invite surface within the first session without consulting external documentation.

#### `ch09-local-first-practitioner-lens:LENS-LF-10` — Conflict-inbox grouping with auto-resolve and resolve-all-similar

When two offline nodes reconnect, surfaced conflicts are grouped by record type and cause, auto-resolved where predefined rules clearly apply, and offer a resolve-all-similar action for the remainder — converting the undifferentiated conflict list that breaks most collaborative local-first applications into a manageable inbox.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Conflict UI groups conflicts by record type and by underlying cause rather than presenting a flat list
- Conflicts matching predefined deterministic resolution rules are auto-resolved and surfaced as informational rather than blocking
- A resolve-all-similar action exists that applies a single user decision across all conflicts in a group

**Verification:** Generate a synthetic conflict set covering at least three record types and two cause classes after a partition heal; confirm the UI groups by type and cause, auto-resolves rule-matching conflicts, and exposes resolve-all-similar.

#### `ch09-local-first-practitioner-lens:LENS-LF-11` — Three-tier sync status indicator with degradation escalation

Sync state surfaces to the user through three persistent but unobtrusive status-bar indicators that escalate from silent to informative to persistent-banner as connectivity and sync health degrade, giving the user accurate situational awareness without alarm fatigue.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition, peer-discovery-failure`

**Must implement:**

- The status bar exposes a sync-state indicator with three distinct levels matching the silent / informative / persistent-banner pattern
- Indicator escalation is driven by observable sync-health signals, not arbitrary timers
- The persistent-banner level appears only when sync degradation crosses a documented threshold

**Verification:** Simulate healthy, degraded, and failed sync conditions in a test build and confirm the indicator transitions through the three levels at the documented thresholds.

#### `ch09-local-first-practitioner-lens:LENS-LF-12` — Default-deny telemetry with named privacy model

Product analytics in a local-first architecture must be specified before the first analytics request arrives — opt-in telemetry disabled by default, aggregate-through-relay privacy-preserving statistics as the only permitted centralized collection — and the chosen model is documented in an ADR mapped to GDPR Article 25 privacy-by-design so the line stays durable under future product pressure.

**Kleppmann:** `P6, P7` · **Scope:** `foundational`

**Must implement:**

- Telemetry is opt-in and disabled by default at first install
- Centralized analytics collection is restricted to aggregate-through-relay privacy-preserving statistics or none at all
- An ADR documents the chosen telemetry model with explicit mapping to GDPR Article 25 privacy-by-design

**Verification:** Confirm a fresh install reports no telemetry; confirm an ADR exists naming the telemetry model with the GDPR Article 25 mapping; confirm centralized collection paths in the codebase emit only aggregate metadata.

#### `ch09-local-first-practitioner-lens:LENS-LF-13` — Implementation drift prohibition on server-side feature gating

A local-first architecture explicitly prohibits server-side feature flag checks, server-side A/B tests, and server-coordinated business logic that would re-introduce the network as a runtime dependency, naming this as the primary drift path that erodes local-first commitments one reasonable-sounding decision at a time.

**Kleppmann:** `P1, P3, P7` · **Scope:** `foundational` · **Failure modes:** `vendor-outage`

**Must implement:**

- Feature flag evaluation runs entirely against the local node with no network call as a precondition for feature visibility
- A/B assignment is computed locally from a deterministic seed, not retrieved from a server-side experiment service
- Business logic gating is rejected at code review when it requires a server round-trip

**Verification:** Disconnect the network, launch the application, and confirm all features behave identically to a connected launch; code review checklist includes a server-side-feature-gate prohibition.

#### `ch09-local-first-practitioner-lens:LENS-LF-14` — Intermittent connectivity as architectural baseline

The architecture treats intermittent connectivity as the operational baseline for hundreds of millions of enterprise workers across Sub-Saharan Africa, South and Southeast Asia, and rural Latin America — not as a carrier-grade NAT edge case — so all sync, conflict, and recovery flows are designed for sessions that span many disconnected intervals.

**Kleppmann:** `P3, P4, P7` · **Scope:** `foundational` · **Failure modes:** `partition, peer-discovery-failure`

**Must implement:**

- Sync daemon is designed for long-running sessions across repeated disconnections without manual reconnect actions
- Subscription scoping at the sync daemon limits per-reconnect catch-up cost to role-relevant data
- Conflict surfaces remain usable after multi-day partitions, not just brief outages

**Verification:** Run a multi-day partition simulation across the test fleet; confirm reconnect catch-up completes without manual intervention and the conflict inbox remains within the documented usability envelope.

#### `ch09-local-first-practitioner-lens:LENS-LF-15` — Sanctions-grade availability as design anchor

The architecture is anchored against the empirical case of the 2022 sanctions-driven SaaS suspensions across Russia and CIS markets — hundreds of thousands of organizations losing vendor access on days of notice — establishing that surviving vendor suspension is not a theoretical improvement but a property the architecture has already had to provide.

**Kleppmann:** `P3, P5, P7` · **Scope:** `foundational` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- Core read and write paths function with all vendor-controlled endpoints unreachable
- Self-hosted relay deployment is documented and supported as a first-class option
- License terms permit continued use under vendor-jurisdiction sanctions enforcement

**Verification:** Block all vendor-controlled domains at the network layer and confirm the application performs all core operations identically; confirm a self-hosted relay deployment guide exists in the public documentation.

#### `ch09-local-first-practitioner-lens:LENS-LF-16` — Shared-device role-scoped recovery

Recovery must support shared-device deployments — a single tablet rotated across a team of field workers — by targeting the role and the workspace rather than the device and its sole user, with BYOC backup configured against role-scoped workspace targets so any team member can restore from any device.

**Kleppmann:** `P2, P4, P7` · **Scope:** `foundational` · **Failure modes:** `key-loss`

**Must implement:**

- BYOC backup targets are scoped to workspace and role, not bound to a specific device serial
- Recovery flow accepts a role credential plus workspace identifier as sufficient inputs to restore role-relevant data
- Multiple users may rotate through the same physical device without each restore wiping the prior user's role state from backup

**Verification:** Provision a workspace with three role-scoped users, restore each onto a single shared device in succession, and confirm each user reaches role-relevant data without loss to the others' backup state.


### Epic: Synthesis: What the Council Finally Agreed On (ch10-synthesis)

**Source-paper refs:** R1, R2

**Concept count:** 17

#### `ch10-synthesis:LENS-01` — Block-vs-condition verdict semantics

Council review distinguishes BLOCK verdicts (correctness or commercial gaps that prevent proceeding regardless of average score) from CONDITION verdicts (specific changes required before sign-off but compatible with proceeding).

**Scope:** `inverted-stack-specific`

**Must implement:**

- Architecture review process records each reviewer's verdict as one of BLOCK, PROCEED WITH CONDITIONS, or PROCEED
- A single BLOCK halts progression regardless of aggregate scores
- Conditions are tracked as named, addressable items that map to specific architecture changes

**Verification:** Review-cycle artifact lists per-reviewer verdicts and conditions; any BLOCK present prevents the artifact from advancing to specification stage.

#### `ch10-synthesis:LENS-02` — Send-tier subscription filtering as data minimization invariant

Subscription filtering enforces role-scoped data minimization at the sending node before transmission, not at the receiver or in the application layer.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, key-compromise`

**Must implement:**

- Sync daemon evaluates subscription filters before any payload leaves the sending node
- Receiver-side filtering is not the primary enforcement point
- Application-layer filters do not substitute for protocol-layer filtering

**Verification:** Sync daemon trace shows that data outside a peer's subscription scope is never serialized for that peer; integration test asserts a peer with a restricted role never receives out-of-scope ciphertext on the wire.

#### `ch10-synthesis:LENS-03` — MDM compliance gate at capability negotiation

A node must pass an MDM compliance check during the sync daemon handshake before any data exchange or capability negotiation completes.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Sync daemon handshake includes a compliance attestation phase before capability exchange
- A node that fails the compliance check is rejected before subscription filters or data exchange occur
- Compliance gating lives in the daemon protocol, not in an application policy layer

**Verification:** Sync daemon protocol specification defines a pre-capability compliance phase; behavioral test confirms a non-compliant node is rejected at handshake before any data frame is transmitted.

#### `ch10-synthesis:LENS-04` — Three-tier CRDT applicability model

Data is partitioned into three tiers — AP CRDT-merged content, CP single-writer operations under lease coordination, and append-only ledger entries outside the CRDT — based on whether automatic merge is semantically valid.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Documents and collaborative content use CRDT merge in an AP tier
- Operations requiring single-writer semantics (sequential IDs, inventory, slots, financial totals) use distributed lease coordination in a CP tier
- Ledger entries are append-only, posted by a domain ledger engine, and not subject to CRDT merge

**Verification:** Architecture documents the tier classification per data type; tier-violating writes (e.g., concurrent CRDT merge of a CP-tier counter) are rejected by the data layer.

#### `ch10-synthesis:LENS-05` — DEK/KEK envelope encryption with role-scoped rotation

Each document holds a Data Encryption Key wrapped by role-scoped Key Encryption Keys, organized as a four-level hierarchy (root org key to role KEKs to per-node wrapped keys to per-record DEKs) such that role revocation rotates the affected KEK and re-wraps in-scope DEKs.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise, key-loss`

**Must implement:**

- Each document is encrypted under a per-document DEK
- Role KEKs wrap DEKs only for documents the role is authorized to access
- Role revocation triggers KEK rotation and re-wrapping of in-scope DEKs
- Compromise of a role KEK does not yield access to documents outside that role's scope
- {'The key hierarchy is exactly': 'root org key, role KEKs, per-node wrapped keys, per-record DEKs'}

**Verification:** Security architecture chapter specifies the four-level hierarchy; revocation test confirms that after rotation the old KEK no longer decrypts in-scope documents and never decrypted out-of-scope documents.

#### `ch10-synthesis:LENS-06` — Dual-license structure established at founding

The codebase ships under AGPLv3 with a parallel commercial license available for organizations that cannot accept the AGPLv3 network use clause, and the dual-license structure plus contributor license agreement is in place before the public repository opens.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-acquisition`

**Must implement:**

- Repository publishes AGPLv3 license at first public commit
- Parallel commercial license terms are published or available on request from first public commit
- Contributor License Agreement is required from every contributor from first public commit
- License structure is not retrofitted after community formation

**Verification:** Repository at first public release contains LICENSE (AGPLv3), a documented commercial license path, and a CLA process; git history shows the license files present at the initial commit.

#### `ch10-synthesis:LENS-07` — Non-technical disaster recovery path

A non-technical user can recover their complete data after total device failure without contacting support and without developer-only tooling.

**Kleppmann:** `P2, P5, P7` · **Scope:** `foundational` · **Failure modes:** `key-loss`

**Must implement:**

- Recovery flow is documented as a UX walkthrough usable by a non-developer
- Recovery requires only artifacts a non-technical user can manage (recovery phrase, backup file, or equivalent)
- Recovery does not depend on vendor support intervention

**Verification:** Documented walkthrough exists; usability test with a non-technical participant completes restore on a fresh device without developer assistance.

#### `ch10-synthesis:LENS-08` — Plain-file export without vendor cooperation

A user can export all of their data to standard plain-file formats (CSV, JSON, plain files) using only a standard file manager, with no vendor service call and no special tooling.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- Export produces standard formats (CSV, JSON, plain files) accessible via a standard file manager
- Export executes without any network call to a vendor service
- Export covers all user-owned records held by the node
- Export discloses categories where regulatory custody overrides user export rights

**Verification:** Disconnect node from network; trigger export; verify produced files open in standard tools and contain the user's full record set; verify any withheld categories are listed with the regulatory basis.

#### `ch10-synthesis:LENS-09` — Pre-GA blocker classification of cross-lens conflicts

When security and commercial timelines conflict over readiness, both requirements are classified as pre-GA blockers rather than allowing one lens to defer to a post-GA roadmap.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Key-compromise incident response is executable by a non-cryptographer IT administrator before first external release
- Dual-license structure and first-customer acquisition path are in place before first external release
- Neither security nor commercial item ships independently of the other

**Verification:** Release-readiness checklist names both items as gating conditions for GA; release artifact records both as satisfied.

#### `ch10-synthesis:LENS-10` — Documented-gap shipping discipline

Where correctness rigor and unit-economics pressure conflict, the protocol ships with known rough edges named explicitly in the public specification rather than being silently deferred or perfected before release.

**Scope:** `inverted-stack-specific` · **Failure modes:** `partition, schema-skew`

**Must implement:**

- Public specification names known protocol gaps (e.g., stale peer recovery, buffer behavior under prolonged partition) at release time
- Each named gap has an owner and a tracked remediation path
- Gaps are not silently elided from the specification to ease shipping

**Verification:** Public spec contains a named "Known Gaps" section enumerating each documented limitation with remediation status.

#### `ch10-synthesis:LENS-11` — Intermittent connectivity as baseline operating condition

The architecture treats intermittent connectivity as the default operating environment for the target user population, not as an edge case the system gracefully degrades into.

**Kleppmann:** `P1, P3` · **Scope:** `foundational` · **Failure modes:** `partition, peer-discovery-failure, vendor-outage`

**Must implement:**

- Core operations complete identically online and offline
- No feature is gated on continuous connectivity for its primary path
- Degraded modes are not used to mask online-required behavior

**Verification:** Disconnect network for an extended period; full feature set executes against the local node with no functional regression versus the online state.

#### `ch10-synthesis:LENS-12` — Sanctions-grade availability as design anchor

The architecture treats the documented 2022 Western SaaS withdrawal from Russia and CIS markets as the empirical anchor against which availability, encryption, and ownership invariants are validated, not as a hypothetical threat model.

**Kleppmann:** `P3, P5, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, vendor-acquisition, vendor-outage`

**Must implement:**

- Ciphertext is held locally so that loss of relay access does not expose plaintext
- The three-tier CRDT model and plain-file export preserve operational continuity independent of vendor availability
- The dual-license structure prevents vendor removal of the software itself, not only the service

**Verification:** Tabletop exercise simulating sudden vendor withdrawal demonstrates continued local operation, retained data, and standalone software availability.

#### `ch10-synthesis:LENS-13` — Crypto-shredding as erasure-rights resolution with documented limits

Erasure rights against CRDT full-history retention are resolved by destroying the per-document DEK, rendering the data cryptographically inaccessible, and the architecture documents that cryptographic inaccessibility is not the same as physical erasure under every regulatory regime.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-loss`

**Must implement:**

- Erasure request triggers destruction of the per-document DEK
- Architecture documents which jurisdictions accept crypto-shredding as fulfilling erasure rights and which do not
- The crypto-shredding limitation is named in the public compliance specification rather than implied

**Verification:** Compliance documentation maps each named jurisdiction (GDPR, LGPD, POPIA, NDPR, DPDP, PIPA, PIPL, etc.) to its treatment of crypto-shredding; behavioral test confirms DEK destruction on erasure request.

#### `ch10-synthesis:LENS-14` — Per-deployment relay residency as regulatory contract

The managed relay's legal residency is a per-deployment choice driven by the buyer's jurisdictional regime (Schrems II for EU, 242-FZ for Russia, DIFC 2020 for UAE financial firms, PIPL for China), and a self-hosted relay path exists for deployments where managed residency cannot satisfy the regime.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection, vendor-outage`

**Must implement:**

- Managed relay offers jurisdictionally-resident deployment options matched to named regulatory regimes
- Self-hosted relay path is available and documented for high-sensitivity deployments
- Relay metadata residency is treated as in-scope for jurisdictional review, not only payload residency

**Verification:** Deployment documentation lists supported relay residency options per jurisdiction; self-hosted relay package is published with operator documentation.

#### `ch10-synthesis:LENS-15` — Local key custody as architectural answer to compelled disclosure

Encryption keys never leave the user-controlled device, so a relay or cloud operator served with a compelled-disclosure order cannot produce decryptable content because no decryptable content is in their custody.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Private key material remains on the user's device and is never uploaded to relay or vendor infrastructure
- Relay processes only ciphertext payloads
- Architecture states explicitly that relay operator compliance with disclosure orders cannot yield plaintext

**Verification:** Audit of relay storage and logs confirms no key material is present; cryptographic protocol specification documents that relay never receives a private key.

#### `ch10-synthesis:LENS-16` — Domain-invariant validation as deployment responsibility

Structural validity of a CRDT operation does not imply semantic correctness, and each deployment is responsible for specifying and enforcing its own domain-level merge invariants on top of the architecture's structural validation layer.

**Kleppmann:** `P4` · **Scope:** `foundational` · **Failure modes:** `partition, schema-skew`

**Must implement:**

- Architecture provides an operation validation layer at insertion that enforces structural validity
- Each deployment defines and enforces domain-specific semantic invariants
- A semantically invalid but structurally valid operation does not silently propagate convergence-breaking corruption across peers

**Verification:** Validation layer rejects an operation that violates a registered domain invariant; multi-peer test demonstrates that domain-invariant violation at one peer does not propagate as accepted state to other peers.

#### `ch10-synthesis:LENS-17` — Default-no analytics with deliberate model selection

Local-first architecture has no server-side analytics endpoint by default, and the analytics model (opt-in telemetry only, aggregate via relay metadata, or none) must be selected and specified before implementation teams face delivery pressure to add one.

**Kleppmann:** `P6, P7` · **Scope:** `foundational`

**Must implement:**

- No server-side analytics endpoint is added by default
- The analytics model is named in the architecture specification before alpha implementation
- Any opt-in telemetry is opt-in by user action, not opt-out

**Verification:** Architecture document names the chosen analytics model and the rationale; sync daemon and node kernel contain no implicit telemetry channel.


---

## Part III — Reference architecture (the specification)

### Epic: Node Architecture (ch11-node-architecture)

**Source-paper refs:** v13 §5, v5 §3

**Concept count:** 31

#### `ch11-node-architecture:NODE-01` — Microkernel monolith pattern

A small stable kernel owns infrastructure concerns while domain plugins implementing well-defined extension-point contracts run in-process within the same monolith.

**Kleppmann:** `P1, P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Kernel exposes a fixed set of infrastructure contracts that plugins consume but do not implement
- All plugins execute in-process with the kernel with no per-plugin processes or inter-plugin RPC
- Domain plugins are versioned and deployed independently of the kernel

**Verification:** Sunfish.Kernel.Runtime package exists exposing INodeHost and IPluginRegistry; plugin-to-kernel calls occur via in-process method dispatch with no serialization layer.

#### `ch11-node-architecture:NODE-02` — Kernel-plugin boundary by change cadence

Concerns are assigned to the kernel when changes require coordinated updates across all plugins, and to plugins when they encode independently-evolving domain knowledge.

**Kleppmann:** `P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Kernel responsibilities cover node lifecycle, sync daemon, CRDT engine abstraction, schema migration, security primitives, partial sync engine, and plugin registry
- Plugin responsibilities cover aggregates, commands, events, projections, and UI blocks
- No domain-specific knowledge is hard-coded inside the kernel

**Verification:** Static analysis of kernel namespaces shows no references to specific domain types (scheduling, ledger, billing, etc.); kernel package set matches the eight named infrastructure concerns.

#### `ch11-node-architecture:NODE-03` — Topological plugin load with version contracts

The plugin registry loads plugins in topological dependency order, deterministic by plugin ID at equal depth, and rejects cycles or missing dependencies before any load phase executes.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Plugin registry computes load order from declared dependencies and rejects cycles at load time
- Missing dependencies are rejected before any plugin OnLoad executes
- At equal dependency depth, plugins load in deterministic ID-sorted order
- Unload reverses the topological load order
- Plugin identifiers follow reverse-DNS convention

**Verification:** IPluginRegistry implementation rejects a test fixture containing a dependency cycle; integration test confirms reverse-order unload.

#### `ch11-node-architecture:NODE-04` — One-shot plugin load surface

The plugin registry rejects a second load call until the prior loaded set has been fully unloaded, preventing partial state from a failed swap from contaminating the running plugin set.

**Scope:** `inverted-stack-specific`

**Must implement:**

- IPluginRegistry rejects concurrent or overlapping load operations
- A failed load batch leaves the registry in a clean unloaded state, not a partial state

**Verification:** Behavioral test attempts a second load before unload completes and observes rejection.

#### `ch11-node-architecture:NODE-05` — Five-state node lifecycle with terminal Faulted

INodeHost transitions through Stopped, Starting, Running, Stopping, and Faulted states, with Faulted as a terminal state that does not auto-restart on unrecoverable error.

**Kleppmann:** `P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- INodeHost exposes the five enumerated lifecycle states
- Faulted state is terminal and blocks automated restart
- Plugin loads sequence in topological order on start; unloads in reverse on stop

**Verification:** INodeHost type defines exactly the five named states; integration test forces a Faulted transition and confirms no auto-restart occurs.

> Faulted is terminal because automatic restart can mask data integrity problems requiring operator diagnosis.

#### `ch11-node-architecture:NODE-06` — Three-tier peer discovery

Peer discovery operates across mDNS for LAN-local zero-configuration discovery, a WireGuard mesh VPN for cross-segment intra-organization discovery, and a managed relay for cross-organization or relay-assisted connectivity.

**Kleppmann:** `P3, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `peer-discovery-failure`

**Must implement:**

- Sync layer attempts mDNS discovery first with no infrastructure dependency
- WireGuard mesh discovery is supported as a second tier
- Managed relay is used only when direct paths are unavailable
- Same-LAN nodes sync without contacting the relay

**Verification:** Behavioral test on isolated LAN demonstrates peer discovery and sync with no relay reachable.

#### `ch11-node-architecture:NODE-07` — ICrdtEngine abstraction

Sunfish.Kernel.Crdt exposes ICrdtEngine as the single contract for creating and opening CRDT documents, allowing engine swaps without changes to kernel or plugin code.

**Kleppmann:** `P4` · **Scope:** `foundational`

**Must implement:**

- ICrdtEngine interface exists in Sunfish.Kernel.Crdt with engine name and version metadata
- All CRDT-using code depends on ICrdtEngine, not on a specific backend type
- At least one production-grade backend (YDotNet) and one test backend (StubCrdtEngine) implement the contract
- Test-only backends are clearly marked not for production

**Verification:** Sunfish.Kernel.Crdt namespace exposes ICrdtEngine; backend implementations satisfy the interface; StubCrdtEngine carries explicit DO NOT SHIP marker.

> Overlaps with Ch12 CRDT engine and data layer specification.

#### `ch11-node-architecture:NODE-08` — Schema registry with upcaster chain

Sunfish.Kernel.SchemaRegistry maintains event schema versions and pure-function upcasters, coordinates schema epochs across peers, and enables nodes at different plugin versions to interoperate.

**Kleppmann:** `P4, P5` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Schema registry stores upcasters keyed by source and target version
- Upcasters are pure functions with no I/O or side effects
- Inbound events from peers at older versions are lifted through the chain to current version
- Schema epochs are coordinated across the peer set
- Stream compaction removes superseded event versions

**Verification:** ISchemaVersion contract surface present; integration test sends an N-1 schema event and observes correct upcasting through the chain.

> Overlaps with Ch13 schema migration.

#### `ch11-node-architecture:NODE-09` — Capability-gated bucket subscription

Sunfish.Kernel.Buckets evaluates sync-bucket eligibility against attestation bundles received during peer handshake, refusing non-attested peers before any bucket data is transferred.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Buckets are declaratively named subsets of the team dataset, each gated on a required role attestation
- Attestation evaluation occurs during handshake, before data transfer
- Non-attested peers are refused subscriptions, not merely filtered after delivery

**Verification:** Integration test confirms a peer lacking the required attestation receives zero events from the protected bucket on the wire.

#### `ch11-node-architecture:NODE-10` — Send-side subscription filtering invariant

Bucket eligibility filtering occurs at the send tier before events leave the originating daemon, never at the receive tier where the data has already traveled.

**Kleppmann:** `P6, P7` · **Scope:** `foundational`

**Must implement:**

- Originating daemon evaluates each outbound event against the receiving peer's attestation bundle and skips disallowed events
- No code path delivers a protected event to a peer and then filters at the receiver

**Verification:** Wire-trace test on a protected bucket confirms zero packets containing protected events leave the originator toward an unauthorized peer.

> Council review identified as a non-negotiable.

#### `ch11-node-architecture:NODE-11` — Flease distributed lease coordinator for CP records

Sunfish.Kernel.Lease implements a Flease-inspired distributed lease coordinator that requires strict-majority quorum acknowledgment before a CP-class record write proceeds.

**Kleppmann:** `P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- CP-class writes acquire a lease granted by strict majority of the configured peer set
- Lease tokens are epoch-stamped to detect partition-time conflicts
- On partition heal, the lower-epoch lease is superseded and its pending write surfaces as a lease conflict, never as silent overwrite
- A node unable to reach quorum blocks the CP-class write and surfaces a staleness indicator instead of proceeding

**Verification:** Multi-node partition test: induce asymmetric partition, attempt concurrent CP writes, confirm exactly one succeeds and the other surfaces a lease conflict on heal.

> Overlaps with Ch14 sync daemon partition recovery protocol.

#### `ch11-node-architecture:NODE-12` — Three-tier CRDT resolution model

The kernel routes writes to one of three coordinators based on tier classification: ICrdtEngine for AP-class records with deterministic merge, Flease coordinator for CP-class records requiring linearizable writes, and an append-only ledger engine for records not subject to merge.

**Kleppmann:** `P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Each ILocalNodePlugin declares record-type tier assignments in its manifest
- Tier classification is validated at plugin load time
- Plugins cannot mutate tier classification at runtime
- Kernel routes each write to the coordinator matching the declared tier

**Verification:** Plugin manifest schema enforces tier declaration; load-time test rejects manifests missing tier classifications; behavioral test confirms a CP-declared record never bypasses the lease coordinator.

#### `ch11-node-architecture:NODE-13` — Append-only durable event log

Sunfish.Kernel.EventBus exposes IEventBus for in-process publication and IEventLog for durable append-only persistence, with the event log as the authoritative record from which projections are rebuilt.

**Kleppmann:** `P5` · **Scope:** `foundational`

**Must implement:**

- IEventLog persists events durably in append-only fashion
- Read-model projections are derived from the event log and may be discarded and rebuilt
- Both file-backed (production) and in-memory (test) implementations ship with the package

**Verification:** Sunfish.Kernel.EventBus exposes both IEventBus and IEventLog; durability test confirms event survival across process restart.

> Overlaps with Ch16 durability.

#### `ch11-node-architecture:NODE-14` — ILocalNodePlugin contract

Every domain plugin implements ILocalNodePlugin and registers stream definitions, projections, schema versions, and UI block manifests via the IPluginContext surface during the load phase.

**Scope:** `inverted-stack-specific`

**Must implement:**

- ILocalNodePlugin exposes Id, Version, Dependencies, OnLoadAsync, OnUnloadAsync
- IPluginContext exposes registration methods for streams, projections, schema versions, and UI blocks
- IPluginContext.Services exposes the host DI container for resolving kernel-registered services

**Verification:** Sunfish.Kernel.Runtime exposes ILocalNodePlugin and IPluginContext; reference plugin demonstrates registration of all four extension-point types.

#### `ch11-node-architecture:NODE-15` — IStreamDefinition contract

IStreamDefinition declares a CRDT stream contributed by a plugin, carrying a stable stream identifier, schema version, emitted event type names, and the sync-bucket IDs the stream contributes to.

**Kleppmann:** `P4` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Each stream definition declares stable stream ID, schema version, event type names, and bucket contributions
- Empty bucket contributions render the stream local-only with no peer propagation

**Verification:** IStreamDefinition interface present; reference stream with empty bucket list demonstrates no gossip-layer propagation.

#### `ch11-node-architecture:NODE-16` — IProjectionBuilder contract with idempotent rebuild

IProjectionBuilder registers a derived read-model projection that reads from a source stream, holds no authoritative state, and exposes an idempotent rebuild safe to call repeatedly during schema migration and CRDT compaction.

**Scope:** `foundational`

**Must implement:**

- Each projection declares stable projection ID and source stream ID
- Projections hold no authoritative state and may be discarded by the kernel
- Rebuild method is idempotent and safe under repeated invocation

**Verification:** Test invokes projection rebuild twice consecutively and observes byte-identical resulting state.

#### `ch11-node-architecture:NODE-17` — ISchemaVersion contract with pure upcasters

ISchemaVersion declares the event types a plugin produces and provides a pure-function upcaster that lifts older event payloads to the current in-memory shape.

**Kleppmann:** `P5` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Each ISchemaVersion declares event type, current canonical version, and accepted older versions
- Upcasters are pure functions with no side effects and no I/O
- Kernel chains upcasters incrementally from inbound version to current

**Verification:** Test passes an N-2 event payload through the upcaster chain and observes deterministic lift to current shape.

#### `ch11-node-architecture:NODE-18` — IUiBlockManifest with attestation-gated visibility

IUiBlockManifest registers a UI block with stable identifier, display name, category, source stream IDs, and required role attestations, suppressing the block when the current user lacks the attestations required for its underlying streams.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Each manifest declares block ID, display name, category, source stream IDs, and required role attestations
- Kernel UI layer suppresses blocks whose required attestations the current user lacks
- Suppressed blocks do not appear in the block picker
- {'Manifest declares accessibility metadata': 'roles exposed, live-region policy, keyboard shortcut surface'}

**Verification:** Behavioral test loads a manifest requiring attestation A; user without A observes the block absent from both rendered surface and block picker.

#### `ch11-node-architecture:NODE-19` — SyncState alignment invariant

Every infrastructure state visible to the data layer has a corresponding component-level visual state in the UI layer, structurally enforced through the SyncState enumeration with values Healthy, Stale, Offline, ConflictPending, and Quarantine.

**Kleppmann:** `P1, P4` · **Scope:** `inverted-stack-specific`

**Must implement:**

- SyncState enumeration exposes exactly the five named values
- No UI tier introduces a UI state that does not correspond to a SyncState value
- UI cannot present data as current when the kernel reports Stale, ConflictPending, or Quarantine
- Resolvable conflicts are not hidden from users with authority to act on them

**Verification:** Static check confirms only the five SyncState values; behavioral test forces ConflictPending in the kernel and observes UI surface reflects it within one render cycle.

#### `ch11-node-architecture:NODE-20` — Four-tier UI layering

The UI kernel is organized as Foundation (design tokens and base contracts), Framework-Agnostic Contracts (renderer and provider interfaces), Adapters and Blocks (Blazor and React implementations plus domain blocks), and Compatibility Layer (third-party-API-shape wrappers).

**Scope:** `inverted-stack-specific`

**Must implement:**

- Sunfish.Foundation owns design tokens and base type hierarchy
- Sunfish.UICore owns ISunfishRenderer, ISunfishCssProvider, ISunfishIconProvider, SunfishWidgetDescriptor without UI-framework dependencies
- Sunfish.UIAdapters.Blazor and @sunfish/ui-adapters-react implement Tier 2 contracts
- Sunfish.Compat.* packages provide source-shape parity with third-party libraries via Tier 2 contracts

**Verification:** Sunfish.UICore package has no Blazor or React dependencies; assembly inspection confirms the four layered packages exist with the correct dependency direction.

#### `ch11-node-architecture:NODE-21` — Accessibility as Tier 1 contract

Accessibility is enforced at the foundation tier rather than as a Tier 3 polish, requiring sync-state components to communicate state through more than color and to pair every icon with a text equivalent.

**Scope:** `foundational`

**Must implement:**

- Sync-state components expose role="status", aria-live="polite", and text labels alongside iconography
- ISunfishIconProvider implementations pair every icon with a text equivalent
- IUiBlockManifest declares accessibility metadata per block

**Verification:** Accessibility audit on reference blocks confirms WCAG-compatible role/aria attributes and text-with-icon pairing.

> Local-first architecture preserves AT user data access during connectivity loss; full AT treatment in Ch20.

#### `ch11-node-architecture:NODE-22` — Sync daemon as separate long-running process

The sync daemon runs as a separate long-running process from the host (MAUI or Blazor shell) so that in-flight gossip rounds, peer connections, peer membership, and the CRDT document store survive host restarts and process cycling.

**Kleppmann:** `P3, P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Sync daemon is deployed as an OS-level process distinct from the application host
- Daemon owns the connection pool, peer membership list, and CRDT document store
- Daemon survives host process termination and restart
- Buffered writes reach the durable event log before acknowledgment

**Verification:** Behavioral test kills the host process mid-round and confirms daemon continues gossip; restart of host reconnects to the running daemon without state loss.

> Overlaps with Ch14 sync daemon specification.

#### `ch11-node-architecture:NODE-23` — Circuit-breaker quarantine queue

A queue inside Sunfish.Kernel.Sync buffers inbound and outbound operations through interruptions and holds unverified writes pending re-attestation on the next clean daemon start.

**Kleppmann:** `P3, P5` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Inbound and outbound operations are buffered through host or network interruption
- Unverified writes are held pending re-attestation rather than applied speculatively
- Buffered state survives abrupt power loss and resumes on clean daemon start

**Verification:** Simulated power-loss test confirms buffered ops resume after restart with no double-apply.

#### `ch11-node-architecture:NODE-24` — Length-prefixed CBOR IPC channel

The host-to-daemon channel uses Unix domain sockets on POSIX and named pipes on Windows, framed as CBOR payloads preceded by a 4-byte big-endian length prefix with frames capped at 16 MiB.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific`

**Must implement:**

- POSIX implementation uses UnixDomainSocketEndPoint with file-permission confinement
- Windows implementation uses named pipes with OS-level access controls
- Every message is a CBOR payload prefixed by a 4-byte big-endian length
- Frames exceeding 16 MiB are rejected; chunking is done at the application layer
- All IPC messages use CBOR per RFC 8949 with canonical mode for signed messages

**Verification:** Wire-format test inspects an IPC frame and confirms the prefix-then-CBOR layout; oversize-frame test confirms rejection.

#### `ch11-node-architecture:NODE-25` — Authenticated five-phase IPC handshake

The daemon enforces a five-phase handshake (HELLO, CAPABILITY_NEG, ACK, DELTA_STREAM, GOSSIP_PING) against every connecting host process, with HELLO carrying an Ed25519 signature over a canonical CBOR array and a +/-30-second replay-protection window.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `replay`

**Must implement:**

- Daemon enforces the five named handshake phases on every connection
- HELLO message is signed Ed25519 over canonical CBOR array of [node_id, schema_version, public_key, sent_at]
- Daemon verifies HELLO signature against claimed public key and rejects mismatches
- Daemon rejects HELLO whose sent_at falls outside +/-30 seconds
- Same attestation verification applies to local IPC as to peer-to-peer; no bypass path exists

**Verification:** Replay test resends a captured HELLO outside the 30-second window and observes rejection; tampered-signature test observes rejection.

#### `ch11-node-architecture:NODE-26` — Push-based daemon-to-host change notifications

After capability negotiation, the daemon pushes change notifications to the host as CRDT deltas arrive from peers and the host does not poll, while command traffic flows host-to-daemon as user-intent operations the daemon translates into CRDT mutations.

**Kleppmann:** `P1, P4` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Host receives change notifications via push, not polling
- Host sends create/update/delete commands describing user intent
- Daemon translates commands into CRDT mutations compatible with concurrent edits
- Daemon validates commands against the CRDT document store before applying and gossiping

**Verification:** Behavioral test confirms zero polling traffic on idle channel; command-to-mutation translation test demonstrates conflict-free composition with concurrent peer edits.

#### `ch11-node-architecture:NODE-27` — Ciphertext-only managed relay

The managed relay observes and routes ciphertext only, holds no decryption keys, and is required only when nodes on different networks lack a direct IP path.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection, vendor-outage`

**Must implement:**

- Relay never holds decryption keys
- Relay never gains access to plaintext payload content
- Same-LAN nodes sync without relay involvement
- Cross-network nodes queue CRDT deltas during relay outage and catch up automatically on recovery

**Verification:** Inspect relay process: confirm no key material is provisioned; wire-trace at relay confirms only ciphertext frames pass through.

#### `ch11-node-architecture:NODE-28` — Strict layered package dependency direction

Sunfish package dependencies flow strictly from upper layers (plugins) through kernel to foundation, with no lower-layer package importing from a higher layer.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Foundation packages have no Sunfish dependencies
- Kernel packages depend only on foundation
- Plugins depend on kernel and foundation, never the reverse
- UI layers respect Foundation -> UICore -> Adapters/Compat layering

**Verification:** Static dependency analysis across the Sunfish package set confirms acyclic dependency graph in the documented direction.

#### `ch11-node-architecture:NODE-29` — Sunfish.Kernel facade via type forwarding

The Sunfish.Kernel package re-exports the seven kernel primitives via assembly type forwarding so a consuming package takes a single dependency rather than listing individual Foundation sub-packages, while the live stateful services remain in Sunfish.Kernel.Runtime and other runtime packages.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Sunfish.Kernel facade re-exports entity store, version store, audit log, permission evaluator, blob store, schema registry, and event bus types
- Live stateful services are owned by Sunfish.Kernel.Runtime and runtime packages, not the facade

**Verification:** Assembly inspection of Sunfish.Kernel confirms type-forwarded references; runtime packages own concrete service implementations.

#### `ch11-node-architecture:NODE-30` — TryAddSingleton DI override convention

Each AddSunfish* DI extension uses TryAddSingleton internally so a preceding registration (test double, stub backend, custom transport) takes precedence without modifying the extension method.

**Scope:** `inverted-stack-specific`

**Must implement:**

- All AddSunfish* extensions register via TryAddSingleton
- Preceding registrations are honored without modification of kernel extension methods
- Test fixtures can inject stubs by registering before the production extension

**Verification:** Source review of AddSunfish* extensions confirms TryAddSingleton; integration test registers a stub before AddSunfishCrdtEngine() and observes the stub is used.

#### `ch11-node-architecture:NODE-31` — Local-first encrypted store foundation

Sunfish.Foundation.LocalFirst provides the local encrypted store (SQLCipher-backed), the IOfflineStore contract, and the circuit-breaker quarantine queue as foundational primitives every node depends on.

**Kleppmann:** `P3, P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise, key-loss`

**Must implement:**

- Local store is encrypted at rest (SQLCipher or equivalent)
- IOfflineStore contract is implemented as the primary storage surface
- Quarantine queue is part of foundation, not kernel runtime

**Verification:** Sunfish.Foundation.LocalFirst package exists with encrypted store and IOfflineStore; storage file inspection confirms encryption-at-rest.

> Overlaps with Ch15 security and Ch16 durability.


### Epic: CRDT Engine and Data Layer (ch12-crdt-engine-data-layer)

**Source-paper refs:** v13 §2.2, v13 §2.4, v13 §9, v13 §12, v5 §3.1, ADR 0028

**Concept count:** 32

#### `ch12-crdt-engine-data-layer:CRDT-01` — Three-layer CRDT architecture (data, semantic, view)

The data layer's CRDT foundation is decomposed into three layers — data (raw CRDT types), semantic (domain interpretation/invariants), and view (projections for query) — where each layer extends rather than overrides the guarantees beneath it.

**Kleppmann:** `P4, P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Raw CRDT type primitives are isolated from domain logic
- Semantic layer interprets CRDT changes as domain events and enforces domain invariants
- View layer holds no authoritative state and is rebuildable from data plus semantic layers

**Verification:** Architecture review confirms separate modules/namespaces for CRDT primitives, domain interpretation, and projections, with no domain types referenced from the data layer.

#### `ch12-crdt-engine-data-layer:CRDT-02` — CRDT merge mathematical properties (commutativity, associativity, idempotency)

A CRDT merge function must satisfy commutativity, associativity, and idempotency so that any two peers applying the same set of operations in any order — including duplicate application — converge to identical state.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Merge function is commutative across operation order
- Merge function is associative across operation grouping
- Applying an operation twice produces the same state as applying it once

**Verification:** Property-based test applies randomized operation sequences in different orders and with duplicates, asserting byte-identical convergent state.

#### `ch12-crdt-engine-data-layer:CRDT-03` — CRDT data layer primitives (map, list, text, counter)

The data layer exposes four raw CRDT types — map (concurrent key insertions), list (insertion-order-preserving), text (human-legible character-merge), and counter (additive across peers) — none of which carry domain semantics.

**Kleppmann:** `P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Map type merges concurrent key insertions deterministically
- List type preserves insertion order across peers under concurrent inserts
- Text type resolves concurrent character insertions into a human-legible result
- Counter type accumulates per-peer increments and converges to the correct sum

**Verification:** Per-type convergence tests under concurrent edits assert deterministic output across peers for each primitive.

#### `ch12-crdt-engine-data-layer:CRDT-04` — Semantic layer enforces domain invariants

The semantic layer interprets CRDT data-layer changes as domain events and enforces invariants that CRDT merge cannot enforce structurally — for example, turning a concurrent posting-amount mutation into a compensating ledger entry rather than a silent corruption.

**Kleppmann:** `P4, P7` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Domain validation runs on every CRDT change interpreted as a domain event
- Invalid state transitions surface to a domain-defined resolution path (compensation, conflict inbox, etc.)
- Semantic layer has authority that the data layer does not

**Verification:** Test injects a CRDT-merged state that violates a domain invariant; assertion confirms semantic layer flags or compensates rather than accepting silently.

#### `ch12-crdt-engine-data-layer:CRDT-05` — View layer as derived projections

The view layer projects current CRDT state into indexes and read models (balance tables, task boards, aging reports) that hold no authoritative state and must be idempotently rebuildable from the data and semantic layers at any time.

**Kleppmann:** `P1, P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Projections are registered through a builder interface (e.g. IProjectionBuilder)
- View rebuild is idempotent and may be triggered without notice
- View layer holds no state that cannot be rebuilt from data + semantic layers

**Verification:** Delete projection store, trigger rebuild, assert resulting projections are byte-identical to pre-deletion state.

#### `ch12-crdt-engine-data-layer:CRDT-06` — Per-record CAP positioning

CAP is not a global setting — each record class is explicitly assigned to AP (CRDT merge, divergence tolerated) or CP (distributed lease, no divergence) based on whether merge convergence is acceptable for that record's domain semantics.

**Kleppmann:** `P3, P4, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Each record class declares AP or CP positioning at definition time
- CP-class designation routes writes through lease coordination before reaching the CRDT store
- Designation lives in the plugin's stream definition, not in the data layer

**Verification:** Inspect stream definitions for explicit AP/CP designation; verify CP writes traverse the lease coordinator before the CRDT document store.

#### `ch12-crdt-engine-data-layer:CRDT-07` — AP records — CRDT merge with tolerated divergence

AP records (documents, notes, task descriptions, team membership) tolerate concurrent offline divergence because deterministic CRDT merge produces a result the user can review, and the domain consequence of temporary inconsistency is acceptable.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- AP-classified records accept offline writes without coordination
- Reconnect triggers deterministic CRDT merge with no user prompt for the common path
- Identity-fact AP records (membership, permissions) re-verify role attestation on reconnect

**Verification:** Two-peer offline divergence test for an AP stream confirms reconnect produces deterministic merged state with no manual intervention.

#### `ch12-crdt-engine-data-layer:CRDT-08` — CP records — distributed lease serialization

CP records (resource reservations, financial transactions, audit/governance records) prohibit divergence because concurrent writes produce conflicting domain state unrecoverable by merge — they require lease acquisition before any write proceeds.

**Kleppmann:** `P4, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- CP-classified writes require lease acquisition prior to commit
- Conflicting CP writes surface as user-visible conflicts rather than silent merges
- Audit/governance CP records append to an append-only event log

**Verification:** Two-peer offline test for a CP reservation stream confirms only one node's reservation commits and the other surfaces a lease-conflict requiring user resolution.

#### `ch12-crdt-engine-data-layer:CRDT-09` — Circuit breaker quarantine queue for offline CP writes

CP-class writes attempted while a node is offline are held in a circuit-breaker quarantine queue and, on reconnect, the breaker attempts to acquire each required lease in submission order before promoting the write to the shared event log.

**Kleppmann:** `P3, P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Offline CP writes are not silently dropped or applied locally as committed
- Quarantine queue preserves submission order
- Reconnect logic attempts lease acquisition per queued write and surfaces conflicts on failure

**Verification:** Submit CP writes while offline, reconnect, assert each enters the lease acquisition path and that conflicting writes surface to the conflict inbox.

#### `ch12-crdt-engine-data-layer:CRDT-10` — ICrdtEngine adapter abstraction

ICrdtEngine in Sunfish.Kernel.Crdt is the engine-agnostic abstraction exposing only the surface the sync protocol and migration infrastructure need (create/open documents, produce/apply deltas, snapshot/restore, advance version vector), so that no kernel package, plugin, or sync daemon depends on a specific engine implementation.

**Kleppmann:** `P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Abstraction exposes document create/open, delta produce/apply, snapshot produce/restore, and version-vector advance
- No plugin or sync daemon code references a concrete engine type
- Engine name and version string are reported through the abstraction for diagnostics and capability negotiation

**Verification:** Static analysis confirms zero references to YDotNet (or any concrete engine) outside the engine adapter package; engine-name string appears in CAPABILITY_NEG advertisements.

#### `ch12-crdt-engine-data-layer:CRDT-11` — Engine swap reversibility via event log as source of truth

Swapping the CRDT engine (e.g., YDotNet to Loro) does not require a schema epoch bump because the event log stores domain events rather than CRDT wire format, allowing the live CRDT working surface to be rebuilt from the engine-independent log under the new engine.

**Kleppmann:** `P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Event log encodes domain events, not CRDT wire-format payloads
- Engine swap procedure rebuilds CRDT documents from the event log
- Schema epoch is not bumped solely for engine substitution

**Verification:** Test rebuilds CRDT working state from event log under a stub engine, confirming the log replay produces equivalent semantic state independent of original engine.

#### `ch12-crdt-engine-data-layer:CRDT-12` — Engine selection criteria (YDotNet default, Loro aspirational, Automerge excluded)

YDotNet is the default production backend for its mature .NET bindings to yrs; Loro is the aspirational primary for its first-class compaction and shallow snapshot model; Automerge is excluded only because no .NET binding currently covers the required sync surface.

**Kleppmann:** `P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- YDotNet backend is shipped and validated
- Loro backend is targeted as the binding surface matures
- Engine selection rationale is documented in an ADR

**Verification:** ADR exists naming chosen engine and its trade-offs; backend implementations exist behind the ICrdtEngine abstraction.

#### `ch12-crdt-engine-data-layer:CRDT-13` — Monotonic CRDT growth requires bounded mitigation

CRDT documents grow monotonically because tombstones, historical operations, and version-vector metadata accumulate as the document is used — this is a structural property of coordinator-free deterministic merge, not a flaw, and growth must be bounded rather than eliminated.

**Kleppmann:** `P5` · **Scope:** `foundational`

**Must implement:**

- Architecture acknowledges monotonic growth as a property and applies bounding strategies
- At least one of library compaction, sharding, or shallow snapshots is applied per document type

**Verification:** Long-running soak test on a high-churn document confirms growth is bounded by the configured GC policy rather than unbounded.

#### `ch12-crdt-engine-data-layer:CRDT-14` — Library-level compaction

Library-level compaction is the engine's built-in pruning of tombstones and superseded operations, treated as a primary engine evaluation criterion because emergent-GC engines (YDotNet) require all-peer acknowledgment before pruning while shallow-snapshot engines (Loro) avoid that dependency.

**Kleppmann:** `P5` · **Scope:** `foundational`

**Must implement:**

- Compaction strategy is specified per chosen engine
- For acknowledgment-dependent engines, AckVector tracking gates pruning

**Verification:** Engine compaction runs in an integration test and confirms operations older than the acknowledgment watermark are pruned without breaking convergence.

#### `ch12-crdt-engine-data-layer:CRDT-15` — Application-level document sharding

Document sharding splits a large logical document into sub-documents under named map keys (e.g., per-week log entries under a project map) so that archiving a key garbage-collects the sub-document independently, with the semantic layer declaring shard keys and the data layer executing transparently.

**Kleppmann:** `P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Plugin declares which domains use sharded sub-documents and the sharding key
- Data layer executes sharding transparently to application code
- Archiving a sub-document key triggers independent GC of that shard

**Verification:** High-churn domain test creates many shard keys, archives older ones, and confirms older shards are GC'd independently while newer shards remain intact.

#### `ch12-crdt-engine-data-layer:CRDT-16` — Periodic shallow snapshots

A shallow snapshot captures current visible state plus a version vector encoding which operations are included, discards operations older than the snapshot boundary, and becomes the new base for subsequent deltas — opt-in per document type, with full-state transfer required for peers whose vector predates the boundary.

**Kleppmann:** `P5` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Shallow snapshots are opt-in via stream definition
- Snapshot boundary is recorded as a version vector
- Peers whose vector predates the boundary fall through to full-state snapshot transfer

**Verification:** Trigger shallow snapshot on opt-in stream; reconnect a stale peer and assert full-state transfer activates rather than incremental delta.

#### `ch12-crdt-engine-data-layer:CRDT-17` — Three-tier GC policy (ephemeral, standard, compliance)

Each document type is assigned to one of three GC tiers — ephemeral (aggressive GC, no durability), standard (90/180-day retention with peer-acknowledgment gating), or compliance (no GC, indefinite retention) — based on durability requirements and acknowledgment characteristics.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Each stream definition assigns a GC tier
- Ephemeral tier discards operations on a short schedule with no peer-ack requirement
- Standard tier gates GC on AckVector confirming all active peers received operations
- Compliance tier never triggers GC

**Verification:** Inspect stream definitions for explicit tier assignment; soak tests for each tier confirm correct retention and pruning behavior.

#### `ch12-crdt-engine-data-layer:CRDT-18` — AckVector and active peer set semantics

AckVector is a compact per-document per-peer acknowledgment watermark persisted alongside the Layer 2 event log, and the "active peer set" is the set of peers that authenticated a CAPABILITY_NEG handshake within a configurable peer-staleness window (30 days default) — GC proceeds only after all active peers have acknowledged.

**Kleppmann:** `P5` · **Scope:** `foundational` · **Failure modes:** `partition, peer-discovery-failure`

**Must implement:**

- AckVector tracks each peer's highest-indexed acknowledged operation per document
- Active peer set membership respects a configurable staleness window
- GC waits for all active peers to acknowledge before pruning standard-tier operations
- Administrators may drop staleness-exceeding peers from the active set

**Verification:** Multi-peer simulation confirms GC blocks until all active peers ack; dropping a stale peer unblocks GC; returning peer enters stale-peer recovery.

#### `ch12-crdt-engine-data-layer:CRDT-19` — Stale peer recovery via full-state snapshot transfer

When a reconnecting peer's vector clock predates the local compaction watermark, incremental sync is impossible, so the sync daemon abandons delta exchange and initiates full-state snapshot transfer with source-selection preference, concurrency limits, idempotent resume on interruption, and per-tier behavior.

**Kleppmann:** `P3, P5` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition, peer-discovery-failure`

**Must implement:**

- CAPABILITY_NEG compares peer vector against compaction watermark and routes to snapshot transfer when stale
- Snapshot source preference favors most recent successful sync partner
- Snapshot transfer resumes from byte offset on interruption and verifies integrity hash before commit
- Snapshot is applied atomically (full replace or no change)
- Per-tier behavior — compliance tier never needs transfer; ephemeral tier rebuilds from next broadcast

**Verification:** Force a peer's clock to predate the GC horizon; reconnect and assert full-state transfer activates with correct source selection, resume on disconnect, and atomic application.

#### `ch12-crdt-engine-data-layer:CRDT-20` — Schema-on-write CRDT operation validation at store entry

Every CRDT operation — locally produced or peer-received — passes through schema-level validation before insertion into the local CRDT store, gating insertion by record-type check, field constraints, and minimum-supported schema version, with failures quarantined rather than applied.

**Kleppmann:** `P4, P6` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Validation runs on every operation prior to CRDT store insertion
- Operations whose schema version is below the node's minimum-supported version are rejected
- Field constraints (required fields, types, enum ranges) are checked
- Failed operations enter the quarantine queue and surface in the conflict inbox

**Verification:** Inject a malformed operation via the sync path and assert it is quarantined and surfaced to the conflict inbox without modifying CRDT state.

#### `ch12-crdt-engine-data-layer:CRDT-21` — Schema version negotiation at CAPABILITY_NEG

Each peer declares its minimum-supported schema version per stream at the CAPABILITY_NEG handshake, the pair converges on the highest mutually-supported version, and operations outside the negotiated compatibility window are rejected with a diagnostic pointing to the upcast path.

**Kleppmann:** `P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `schema-skew`

**Must implement:**

- Handshake exchanges per-stream min-supported schema version
- Pair converges on highest mutually supported schema version
- Out-of-window operations are rejected with a diagnostic referencing the required upcast

**Verification:** Two peers with disparate schema versions complete handshake; assert negotiated version equals the highest common version and out-of-window ops produce diagnostics.

#### `ch12-crdt-engine-data-layer:CRDT-22` — Compliance tier required by data sovereignty regimes

The no-GC compliance tier is a mandatory (not preferred) classification for record types subject to fourteen named data sovereignty regimes across six geographic regions, ensuring growth is bounded only by business volume — the activity the records exist to document.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection`

**Must implement:**

- Stream definitions for regulated record types assign the compliance tier explicitly
- GDPR Article 17 erasure interaction is handled via crypto-shredding at the DEK level (cross-ref Ch15)
- Tier assignment is a domain decision recorded in the plugin

**Verification:** Audit confirms regulated streams (e.g. financial postings, audit records) are assigned compliance tier and never have operations pruned.

#### `ch12-crdt-engine-data-layer:CRDT-23` — Double-entry ledger as canonical CP subsystem

The double-entry ledger is the correct model for value records — not a CRDT workaround — because its append-only, immutable, strictly-ordered, balanced-postings structure aligns directly with what CP positioning requires for audit integrity.

**Kleppmann:** `P5, P7` · **Scope:** `foundational`

**Must implement:**

- Every transaction produces at least two postings whose amounts sum to zero
- Postings are immutable once committed; corrections occur via compensating entries
- Immutability is enforced structurally by the append-only event log

**Verification:** Attempt to mutate a committed posting and confirm the operation is rejected; verify ledger integrity check confirms balanced postings per transaction.

#### `ch12-crdt-engine-data-layer:CRDT-24` — Posting engine with idempotency keys

Sunfish.Kernel.Ledger's posting engine converts domain events into ledger entries under distributed lease coordination, and uses idempotency keys carried on domain events so that processing the same event multiple times produces at most one set of postings.

**Kleppmann:** `P4, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Posting writes acquire a quorum-granted lease via Sunfish.Kernel.Lease before commit
- Each domain event carries an idempotency key
- Duplicate processing of the same idempotency key is a no-op returning the original result

**Verification:** Submit the same idempotency-keyed event twice; assert the ledger contains exactly one posting set and the second call returns identical results.

#### `ch12-crdt-engine-data-layer:CRDT-25` — CQRS write/read split for ledger

The ledger applies CQRS — the immutable posting event stream is the write side, while balance tables, statements, aging reports, and period summaries are derived read-side projections that hold no data unrebuildable by replaying the event stream.

**Kleppmann:** `P5` · **Scope:** `foundational`

**Must implement:**

- Write path appends to the event stream only
- Projections derive from the event stream and are rebuildable from it
- Business rule aggregates read from the event stream or current lease-protected CP state, never from lagging projections

**Verification:** Delete projection store, replay event log, and confirm rebuilt projections match original; assert no business rule reads from projection-only state.

#### `ch12-crdt-engine-data-layer:CRDT-26` — Period close and rollup snapshots

At period close, the projection engine computes account balances, P&L, and cash flow as rollup snapshots committed as closing events to the append-only log, and any subsequent postings affecting a closed period are directed to adjustment accounts in the next open period — the closed-period log is never rewritten.

**Kleppmann:** `P5, P7` · **Scope:** `foundational`

**Must implement:**

- Period close emits rollup snapshot events to the append-only log
- Postings affecting a closed period route to adjustment accounts in the next open period
- Closed-period event log is immutable and never rewritten

**Verification:** Close a period, attempt a backdated posting, assert it is recorded as an adjustment in the current period and the closed-period log is unchanged.

#### `ch12-crdt-engine-data-layer:CRDT-27` — Five-layer storage architecture

The storage architecture places five concerns in five distinct layers — Layer 1 local encrypted database, Layer 2 CRDT and event log, Layer 3 user-controlled cloud backup (always present), Layer 4 content-addressed distribution (opt-in), Layer 5 decentralized archival (opt-in enterprise) — each with independent durability semantics.

**Kleppmann:** `P3, P5, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Layers 1, 2, and 3 are always present in a production node
- Each layer has independent durability semantics and failure modes
- Layers 4 and 5 are opt-in and do not affect operation when absent

**Verification:** Architecture review confirms five-layer separation; failure injection in any layer demonstrates independent failure modes.

#### `ch12-crdt-engine-data-layer:CRDT-28` — Layer 1 — local encrypted database (SQLCipher)

Layer 1 is the primary operational store — Sunfish.Foundation.LocalFirst's SQLCipher-backed IOfflineStore — applying AES-256 page-level encryption with the key derived from the device's OS-native keystore via Sunfish.Kernel.Security, never stored in plaintext alongside the database.

**Kleppmann:** `P1, P3, P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise, key-loss`

**Must implement:**

- All reads and writes hit Layer 1 first
- Encryption key is derived from OS-native keystore, never persisted plaintext alongside the database
- Reads are synchronous from the application perspective with no network round-trip
- Layer 1 corruption triggers rebuild from Layer 2 event log

**Verification:** Inspect database file confirms encryption-at-rest; key material is absent from filesystem; corruption test rebuilds from Layer 2.

#### `ch12-crdt-engine-data-layer:CRDT-29` — Layer 2 — append-only event log as source of truth

Layer 2 is the append-only CRDT and event log — the source of truth — to which every CRDT operation, domain event, and ledger posting is durably written (fsync on POSIX, FlushFileBuffers on Windows) before the application receives confirmation, with the only mutating operation being compaction under the three-tier GC policy.

**Kleppmann:** `P3, P5` · **Scope:** `foundational`

**Must implement:**

- Every operation is durably persisted (fsync/FlushFileBuffers) before application acknowledgment
- Write path is append-only with no in-place mutation operation
- Compaction replaces ranges with snapshots representing equivalent state, never silent deletion
- Layer 2 truncation without Layer 3 backup is acknowledged as the one irrecoverable failure mode

**Verification:** Power-loss simulation confirms acknowledged writes survive recovery; static analysis confirms no in-place mutation API on the log; compaction test confirms snapshot equivalence.

#### `ch12-crdt-engine-data-layer:CRDT-30` — Layer 3 — user-controlled cloud backup

Layer 3 streams the event log to object storage under the user's own credentials and chosen jurisdiction, with the provider adapter supporting any S3-compatible endpoint (sovereign clouds, EU-resident providers, on-premise MinIO/Ceph) so the user controls credentials, bucket, residency, and retention.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection, vendor-outage`

**Must implement:**

- Backup adapter accepts any S3-compatible endpoint
- User supplies and retains backup credentials
- User selects jurisdictional residency and retention policy
- Disaster recovery proceeds via new device install + backup credentials + restore from object storage

**Verification:** Configure backup against multiple S3 endpoints (AWS, Hetzner, MinIO); destroy local node; restore from backup credentials only and confirm full state recovery.

#### `ch12-crdt-engine-data-layer:CRDT-31` — Layer 4 — content-addressed binary distribution (opt-in)

Layer 4 synchronizes binary assets across nodes using content-hash addressing as the storage key, providing integrity verification and deduplication as structural properties — opt-in because text-and-structured-data nodes do not need the infrastructure overhead.

**Kleppmann:** `P4, P5` · **Scope:** `foundational`

**Must implement:**

- Asset storage key is the content hash
- Two nodes with the same asset confirm identity by hash without redundant transfer
- Layer is opt-in via deployment configuration

**Verification:** Two nodes independently receive the same binary; hash comparison confirms identity and no redundant transfer occurs.

#### `ch12-crdt-engine-data-layer:CRDT-32` — Layer 5 — decentralized archival with proof-of-storage (opt-in enterprise)

Layer 5 commits signed archive segments from the event log to a decentralized storage network that issues cryptographic proofs of storage and integrity, satisfying regulated-industry audit requirements where self-attesting archives would not pass scrutiny — opt-in and never an operational dependency.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Archive segments are cryptographically signed before commit
- Proofs of storage are retrievable for audit
- Local Layers 1 and 2 remain valid and operational regardless of Layer 5 availability

**Verification:** Submit segment to Layer 5; retrieve proof; verify proof cryptographically; disconnect Layer 5 and confirm node operates normally.


### Epic: Schema Migration and Evolution (ch13-schema-migration-evolution)

**Source-paper refs:** v13 §7, v13 §8, v13 §15, v13 §19, v5 §3

**Concept count:** 25

#### `ch13-schema-migration-evolution:SCH-01` — Multi-version schema skew across nodes

A team's nodes simultaneously run multiple schema versions because no central authority can force coordinated upgrade and the sync daemon cannot know a peer's schema version until handshake.

**Kleppmann:** `P3, P4, P5` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- System tolerates concurrent operation across at least three live schema versions
- No write path assumes a single global schema version is in effect
- Application correctness does not depend on coordinated upgrade windows

**Verification:** Multi-peer test runs three nodes at v1, v2, v3 simultaneously and verifies bidirectional sync produces convergent state for shared record types.

#### `ch13-schema-migration-evolution:SCH-02` — Expand-contract migration pattern

A schema modification divided into an expand phase (additive, dual-write, both old and new fields present) and a contract phase (removal of old field) separated by a compatibility window.

**Kleppmann:** `P3, P4, P5` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Every breaking schema modification decomposes into an expand phase followed by a contract phase
- Expand phase remains active for at least one full major version release cycle
- Contract phase is initiated only by explicit operational act, never by timer

**Verification:** Migration runbook in source control documents the expand-contract decomposition for each schema change; CI rejects schema changes lacking a registered expand and contract step.

#### `ch13-schema-migration-evolution:SCH-03` — Dual-write during expand phase

During the expand phase, every write path produces records carrying both the old and the new field, so that nodes on either schema version can interpret the record without information loss.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- All write paths producing a migrated record type write both old and new fields atomically
- New-schema reads prefer the new field and fall back to the old field when absent
- A code-review invariant prohibits write paths that emit only the new field during expand phase

**Verification:** Static analysis or grep-based check enumerates all write sites for the record type and confirms each writes both fields; integration test produces a record on a v2 node and reads it correctly on a v1 peer.

#### `ch13-schema-migration-evolution:SCH-04` — Unknown-field tolerance in CRDT maps

CRDT map types preserve unknown keys received from peers running newer schemas, storing them rather than rejecting the operation.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- CRDT map deserialization preserves unknown keys rather than dropping them
- Unknown keys are retained on disk and re-emitted to peers on subsequent sync
- Domain logic ignores unknown keys without failing

**Verification:** Test sends a CRDT map operation containing a field absent from the local schema; node stores the field and re-emits it on subsequent sync to a third peer that recognizes it.

#### `ch13-schema-migration-evolution:SCH-05` — Compatibility window minimum duration

The expand phase must remain active long enough that all realistically deployed nodes have had the opportunity to upgrade, governed by the slowest-connecting node in the deployment.

**Kleppmann:** `P3, P5` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Kernel tracks the oldest schema version observed per peer per sync session
- Epoch coordinator consults peer-version tracking before initiating contract phase
- Compatibility window duration is configurable per deployment intermittency profile

**Verification:** Kernel exposes a per-peer oldest-schema-version metric queryable by the epoch coordinator; coordinator refuses to advance epoch if any acknowledged peer is below threshold.

#### `ch13-schema-migration-evolution:SCH-06` — Schema version registry

A kernel-level registry of declared schema versions, each carrying its upcasting logic and registered through a versioning interface.

**Kleppmann:** `P5` · **Scope:** `inverted-stack-specific` · **Failure modes:** `schema-skew`

**Must implement:**

- Kernel exposes an interface for registering schema versions and their upcasters
- Plugins declare each schema version they have ever published to the registry
- Startup fails if a registered schema version omits required upcaster wiring

**Verification:** Sunfish.Kernel.Runtime exposes an ISchemaVersion interface; startup test confirms a plugin missing an upcaster between two registered versions causes a fatal startup error.

> ISchemaVersion lives in Sunfish.Kernel.Runtime per the package reference table.

#### `ch13-schema-migration-evolution:SCH-07` — Event upcaster as pure read-path transform

A pure function that transforms an event of an older type into the equivalent current-version event, applied on read by the semantic layer before domain logic sees the event.

**Kleppmann:** `P5` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Upcasters are pure functions with no side effects
- Semantic layer applies upcasters on read before delivering events to domain logic
- The original event in the log is never modified by upcasting

**Verification:** Upcaster registry test feeds a stored V1 event to the read path and confirms domain logic receives a V2-shaped event while the on-disk V1 event is unchanged.

#### `ch13-schema-migration-evolution:SCH-08` — Additive change classes that skip upcasters

Two classes of schema change require no upcaster — adding a new optional field to an existing event type, and adding a new event variant — because absence is a defined default and unknown variants are quarantined.

**Kleppmann:** `P3, P4, P5` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Optional field absence is treated as the field's declared default
- New event variants unknown to a node are quarantined into the circuit breaker queue rather than dropped
- Quarantined events are re-evaluated after upgrade

**Verification:** Test introduces a new optional field and a new event variant, sends both to an old node, and confirms the optional field is defaulted and the new variant lands in the circuit breaker queue.

#### `ch13-schema-migration-evolution:SCH-09` — New event type for non-additive change

Non-additive changes such as field renames must introduce a new event type alongside the unmodified original, registered with an upcaster that promotes the old type to the new on read.

**Kleppmann:** `P5` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Renames and structural reshuffles produce a new event type, never modify an existing one
- The prior event type remains readable from the log indefinitely until compaction retires it
- An upcaster bridges every retained prior version to the current shape

**Verification:** Audit test enumerates registered event types and confirms no event type's schema definition has been mutated since its first commit; SHA of each event type's definition is pinned.

#### `ch13-schema-migration-evolution:SCH-10` — Upcaster chain accumulation problem

Each new schema version adds an upcaster to the chain, producing maintenance and read-path complexity that grows linearly with version history unless explicitly bounded.

**Kleppmann:** `P1, P5` · **Scope:** `foundational`

**Must implement:**

- System tracks total upcaster chain depth per event type
- Maintenance documentation captures each upcaster's transformation
- Compaction is triggered before chain depth degrades read latency

**Verification:** Telemetry exposes per-event-type upcaster chain depth; alert fires when depth exceeds configured threshold.

#### `ch13-schema-migration-evolution:SCH-11` — Mandatory stream compaction

A background copy-transform job that replays the original event stream, applies all current upcasters in sequence, and writes a new compacted stream where every event is in current-version shape.

**Kleppmann:** `P1, P5` · **Scope:** `foundational`

**Must implement:**

- Compaction runs as a low-priority background process that does not block sync
- Compaction is checkpointed so an interrupted run resumes rather than restarts
- Original stream is archived rather than deleted after compacted stream is verified
- Retired upcasters are removed from the active read path after compaction verification

**Verification:** Test interrupts a compaction job mid-run and confirms restart resumes from the last checkpoint with byte-identical output to an uninterrupted run.

#### `ch13-schema-migration-evolution:SCH-12` — Bidirectional schema lens

A pair of forward and backward transformation functions between two schema versions, where forward and backward must be mutual inverses up to information loss.

**Kleppmann:** `P3, P4, P5` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Each lens registers both forward and backward functions
- Bidirectionality is verified at startup against a canonical property-based test fixture
- A lens whose round-trip is not identity halts node startup with a diagnostic naming the failing edge

**Verification:** Sunfish.Kernel.SchemaRegistry startup runs round-trip tests for each registered lens; injecting a lens with a non-identity round-trip causes startup to fail with the failing edge name in the diagnostic.

> Architecture follows Ink and Switch Cambria reference design.

#### `ch13-schema-migration-evolution:SCH-13` — Lens application on transmission and receipt

The sync daemon applies the backward lens before transmitting a delta to an older-schema peer and the forward lens on receipt of a delta from an older-schema peer, so neither node stores data in the wrong version shape.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Outbound deltas to older-schema peers pass through the backward lens
- Inbound deltas from older-schema peers pass through the forward lens
- Local storage always reflects the local node's own schema version

**Verification:** Sync test between a v1 and v2 node confirms each node's local store contains records in its own schema version after bidirectional sync.

#### `ch13-schema-migration-evolution:SCH-14` — Lens version graph and shortest-path composition

Lenses form a directed graph between schema versions; non-adjacent translations are produced by composing lenses along the shortest path through the graph.

**Kleppmann:** `P1, P3, P4` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Lens registry maintains a graph of version-to-version edges
- Sync daemon computes shortest path between peer and local schema versions
- Composed lens chains are cached per peer schema version

**Verification:** Lens engine exposes a query returning the composition path between any two registered versions; cache hit-rate metric is observable.

#### `ch13-schema-migration-evolution:SCH-15` — Missing lens edge suspends sync

When the lens version graph contains no path between a peer's schema version and the local schema version for a given record type, synchronization for that record type is suspended until a lens is installed or the peer upgrades.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Sync daemon checks for a lens path during HELLO handshake per record type
- Absence of a path suspends only the affected record types, not the entire sync session
- Suspension produces a diagnostic identifying the missing edge

**Verification:** Test removes a lens edge between v2 and v3, connects a v1 and v3 peer, and confirms only the affected record types are suspended while unaffected types continue to sync.

#### `ch13-schema-migration-evolution:SCH-16` — Schema epoch with minimum supported version

A versioned, gossiped administrative boundary that carries a minimum supported peer version, below which the sync daemon refuses to synchronize the record types governed by the epoch.

**Kleppmann:** `P4, P5` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Epoch announcements propagate through the gossip network as administrative events
- Sync daemon enforces minimum supported version for governed record types
- Below-minimum peers receive an explicit version-gate error rather than partial data

**Verification:** Test announces epoch E+1 with minimum version v3; v2 peer attempting to sync a governed record type receives a version-gate error and does not receive partial data; non-governed types continue to sync.

#### `ch13-schema-migration-evolution:SCH-17` — Epoch coordinator role

A statically assigned but transferable team role responsible for announcing epochs, accumulating peer acknowledgments, and committing the epoch when quorum is reached.

**Kleppmann:** `P4, P6, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Coordinator role is statically assigned at team setup, defaulting to the administrator node
- Role transfer requires either current-coordinator authorization or quorum of authenticated team members
- Coordinator monitors epoch acknowledgment progress and commits only on quorum

**Verification:** Test confirms an unauthenticated node cannot assume coordinator role; role transfer event is signed and verifiable.

#### `ch13-schema-migration-evolution:SCH-18` — Epoch quorum acknowledgment

An epoch becomes active only when a strict majority of the currently reachable peer set has acknowledged the announcement, matching the CP-class lease quorum from Chapter 12.

**Kleppmann:** `P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Coordinator counts acknowledgments from currently reachable peers
- Strict majority threshold is required before epoch activation
- Offline peers receive the epoch event on reconnect and acknowledge then

**Verification:** Test with 5-node team confirms epoch activation requires 3 acknowledgments and not just announcement broadcast; activation is denied below threshold.

#### `ch13-schema-migration-evolution:SCH-19` — Couch device snapshot recovery

A node returning after an absence so long that the lens graph no longer spans its version recovers by discarding its local event log for affected record types and downloading a current-version snapshot from a reachable peer.

**Kleppmann:** `P3, P5` · **Scope:** `foundational` · **Failure modes:** `partition, schema-skew`

**Must implement:**

- Sync handshake detects when peer vector clock predates the GC horizon
- Daemon reports a snapshot-required condition rather than attempting incremental sync
- Snapshot delivery supports byte-offset resume across interrupted connections
- Peer's pre-absence local edits to governed types are quarantined for human review

**Verification:** Test simulates a peer offline across two epoch boundaries; on reconnect, daemon reports snapshot-required, snapshot resumes after connection interruption, and offline edits to governed types appear in the circuit breaker queue.

#### `ch13-schema-migration-evolution:SCH-20` — Copy-transform background migration

An idempotent, checkpointed background job that reads the existing event log for governed record types, applies all registered lenses and upcasters in sequence, and writes the result to a new epoch stream while sync continues uninterrupted.

**Kleppmann:** `P1, P5` · **Scope:** `foundational`

**Must implement:**

- Job is idempotent and resumes from the last checkpointed position after interruption
- Job does not block synchronization
- New operations written during the job land directly in the new epoch stream
- Old epoch stream is preserved in read-only mode until retention window expires

**Verification:** Test interrupts the copy-transform job, restarts it, and confirms the resulting new-epoch stream is byte-identical to an uninterrupted run; concurrent writes during the job land in the new stream.

#### `ch13-schema-migration-evolution:SCH-21` — Eight-step migration runbook with reversibility gate

A sequenced operational procedure of eight steps from epoch announcement through copy-transform completion, where every step before the contract phase commit is fully reversible.

**Kleppmann:** `P5` · **Scope:** `foundational`

**Must implement:**

- Each step is observable and produces an audit record
- Steps 1 through 6 are reversible without forward-only side effects
- Step 7 commit is gated on quorum acknowledgment
- Rolling back after step 7 requires issuing a new epoch, not a true revert

**Verification:** Runbook test simulates abort at each step 1-6 and confirms full state restoration; abort at step 7 requires forward-recovery via new epoch.

#### `ch13-schema-migration-evolution:SCH-22` — Non-migratable change classes

Three classes of change cannot be expressed as a bidirectional lens and require introducing a new document type rather than migrating the existing one — field removal with no semantic equivalent, CRDT type change, and field split with no deterministic inverse merge.

**Kleppmann:** `P5` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Schema-change linter rejects field removals lacking a backward lens with no information loss
- CRDT type changes are rejected at registration; replacement requires a new field
- Field splits with non-deterministic inverse are rejected as migrations and treated as new document types

**Verification:** Schema linter test attempts each of the three forbidden change classes against an existing schema and confirms each is rejected with an explanation pointing to the new-document-type alternative.

#### `ch13-schema-migration-evolution:SCH-23` — HELLO handshake schema version negotiation

The sync daemon's HELLO handshake exchanges schema versions per record type so each side can determine whether a lens path exists before transmitting any operations.

**Kleppmann:** `P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `schema-skew`

**Must implement:**

- HELLO handshake includes per-record-type schema version
- Daemon resolves lens paths before any delta exchange begins
- Capability mismatch produces a structured suspension report rather than a connection failure

**Verification:** Wire-protocol test confirms HELLO frame carries per-record-type schema version fields; handshake test with mismatched versions produces a structured suspension report.

> Wire-format details belong to Ch14 / Appendix A; this concept is the schema-side contract.

#### `ch13-schema-migration-evolution:SCH-24` — Local-only archival of retired epoch streams

Retired epoch streams remain on the node operator's storage and are not replicated to the managed relay by default, so archival retention does not trigger a cross-border data transfer event.

**Kleppmann:** `P5, P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection`

**Must implement:**

- Retired epoch streams default to local-only retention
- Replication of archived streams to relay requires explicit opt-in
- Retention window for archived streams is configurable per jurisdiction

**Verification:** Configuration audit confirms archived streams are not enumerated in default replication targets; opt-in requires a signed administrative event.

#### `ch13-schema-migration-evolution:SCH-25` — Crypto-shred deletion bridge to right-to-erasure

The tension between immutable archival history and storage-limitation or erasure-rights regulation is resolved by deleting the per-record DEK rather than rewriting the archive, rendering the historical record cryptographically unreadable.

**Kleppmann:** `P5, P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-loss`

**Must implement:**

- Archived streams are encrypted with per-record or per-document DEKs
- Erasure operation deletes the DEK, leaving ciphertext unreadable
- Audit log records the DEK-deletion event without revealing plaintext

**Verification:** Erasure test confirms post-deletion the archived ciphertext remains on disk but is unrecoverable without the DEK; audit log records the operation.

> Implementation detail of the deletion path lives in Ch15.


### Epic: Sync Daemon Protocol (ch14-sync-daemon-protocol)

**Source-paper refs:** v13 §6, v5 §3.4, v5 §3.5

**Concept count:** 35

#### `ch14-sync-daemon-protocol:SYNC-01` — Sync daemon as separate OS process

The sync daemon runs as a distinct OS-level process from the application, decoupling network and replication lifecycle from application lifecycle.

**Kleppmann:** `P1, P3, P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition, vendor-outage`

**Must implement:**

- Daemon runs in a process distinct from the application process
- Daemon survives application restart, update, and crash
- Daemon continues accepting inbound deltas while application is down
- Daemon reconnects to peers independent of application UI startup

**Verification:** Kill the application process while peers are streaming; confirm daemon process retains peer connections and queues inbound deltas for next application startup.

#### `ch14-sync-daemon-protocol:SYNC-02` — IPC over Unix domain socket / named pipe

The application communicates with the daemon over a Unix domain socket on Linux/macOS and a named pipe on Windows, with file-permission/ACL controls scoping access to the same user.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Daemon exposes a local IPC endpoint (UDS or named pipe)
- Socket path enforces user-level filesystem permissions or explicit ACL grants
- No network port is exposed for application-to-daemon communication

**Verification:** Inspect socket path permissions; confirm only same-user processes (or explicit ACL grantees) can connect.

#### `ch14-sync-daemon-protocol:SYNC-03` — Device-key authentication on the IPC channel

All messages on the daemon's IPC channel are authenticated with a device key, so processes that can reach the socket cannot inject operations without a valid key.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Daemon rejects IPC sessions that do not present a valid device key
- Authentication occurs before any command-channel operation is processed

**Verification:** Connect a process without a device key to the socket and confirm the daemon refuses session establishment.

#### `ch14-sync-daemon-protocol:SYNC-04` — Daemon ownership of four responsibilities

The daemon owns the local CRDT document store, peer/relay connections, per-peer capability and subscription enforcement, and background tasks (compaction, archival), and the application never touches the document store directly.

**Kleppmann:** `P3, P4, P5, P6` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Document store is accessed only via the daemon
- Peer connection lifecycle is managed by the daemon, not the application
- Capability/subscription rules are enforced inside the daemon
- Background maintenance (compaction, archival) runs in the daemon

**Verification:** Inspect the application binary; confirm no code paths read or mutate the document store outside the daemon command channel.

#### `ch14-sync-daemon-protocol:SYNC-05` — Three-tier peer discovery

The daemon discovers peers concurrently across three mechanisms — mDNS for LAN, mesh VPN for cross-network, and managed relay for restricted networks — with no tier acting as a fallback that disables another.

**Kleppmann:** `P3, P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `peer-discovery-failure`

**Must implement:**

- Daemon runs all three discovery mechanisms concurrently when configured
- Tiers are not mutually exclusive; a peer reachable on multiple paths is recorded for all
- Daemon selects the lowest-latency reachable path per peer

**Verification:** With a peer reachable via mDNS and mesh VPN, observe the daemon selecting mDNS as primary while keeping VPN as hot standby.

#### `ch14-sync-daemon-protocol:SYNC-06` — mDNS LAN discovery

On a local network segment, the daemon announces node ID, schema version, and IPC endpoint via multicast DNS, removing peers from the candidate list after three missed heartbeat intervals.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `peer-discovery-failure`

**Must implement:**

- Daemon emits mDNS announcements containing node ID and schema version
- Daemon removes a peer from the candidate list after three missed heartbeats
- Discovery requires no central coordinator on the LAN

**Verification:** Two daemons on the same LAN segment discover each other within one mDNS announcement interval with zero configuration.

#### `ch14-sync-daemon-protocol:SYNC-07` — Mesh VPN cross-network discovery

Peers on different networks connect through a WireGuard-based mesh VPN that handles NAT traversal and provides in-transit encryption independent of protocol-layer authentication.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition, peer-discovery-failure`

**Must implement:**

- Daemon supports a WireGuard-based mesh VPN transport
- No port forwarding is required at either endpoint
- VPN peers are treated identically to LAN peers above the transport layer

**Verification:** Two daemons behind separate NATs establish a session through the mesh VPN with no per-endpoint port forwarding.

#### `ch14-sync-daemon-protocol:SYNC-08` — Managed relay for restricted networks

For deployments where direct peer-to-peer connectivity is not viable, the daemon connects through a managed relay that forwards delta streams without decrypting them and cannot inject or modify operations.

**Kleppmann:** `P3, P4, P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition, peer-discovery-failure`

**Must implement:**

- Relay forwards delta frames opaquely without decrypting payloads
- Receiving daemon verifies Ed25519 signatures on every relay-forwarded message
- Relay cannot read content or inject operations

**Verification:** Run a relay with logging instrumented; confirm no plaintext payload visibility and that mutated frames are rejected by the receiving daemon's signature check.

#### `ch14-sync-daemon-protocol:SYNC-09` — Lowest-latency path selection with hot standby

The daemon selects the lowest-latency reachable path to each known peer and dynamically updates path selection as network conditions change, retaining alternate paths as hot standby.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Daemon measures per-path latency to each known peer
- Daemon promotes an alternate path when the primary degrades
- Path selection updates without re-handshake

**Verification:** Sever the primary path between two peers; observe the daemon promoting the standby within one gossip interval without a fresh CAPABILITY_NEG.

#### `ch14-sync-daemon-protocol:SYNC-10` — Five-step handshake (HELLO, CAPABILITY_NEG, ACK, DELTA_STREAM, GOSSIP_PING)

Every peer connection follows a fixed five-step sequence — HELLO, CAPABILITY_NEG, ACK, DELTA_STREAM, GOSSIP_PING — that establishes identity, negotiates capabilities, and confirms subscription grants before any CRDT operations flow.

**Kleppmann:** `P4, P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `replay, schema-skew`

**Must implement:**

- No DELTA_STREAM frames flow before ACK is received
- Both peers exchange HELLO simultaneously at session start
- GOSSIP_PING runs on a 30-second cadence after the session is live

**Verification:** Capture wire trace of a fresh session; confirm the five message types appear in the specified order and no operations precede ACK.

#### `ch14-sync-daemon-protocol:SYNC-11` — HELLO message and schema-version negotiation

HELLO carries node ID, current schema epoch, public key, signed timestamp, and supported protocol versions; the session proceeds on the highest mutually supported version, and incompatible epochs result in SCHEMA_VERSION_INCOMPATIBLE and session close.

**Kleppmann:** `P4, P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `schema-skew`

**Must implement:**

- HELLO carries node_id, schema_version, public_key, sent_at, signature, supported_versions
- Session uses the highest version in the intersection of both peers' supported lists
- Incompatible schema epoch closes the session with SCHEMA_VERSION_INCOMPATIBLE; no partial or read-only mode
- Application surfaces a schema-update notification when the daemon closes a session on version grounds

**Verification:** Connect two daemons with non-overlapping supported_versions; confirm SCHEMA_VERSION_INCOMPATIBLE is sent and the session closes.

#### `ch14-sync-daemon-protocol:SYNC-12` — CAPABILITY_NEG with role-attestation tokens

The requesting node declares CRDT streams, CP leases, and bucket subscriptions, with each requested subscription accompanied by a role attestation signed by the node's device key that the receiving node verifies before granting.

**Kleppmann:** `P4, P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Each requested subscription carries a device-key-signed role attestation
- Receiving daemon verifies attestation signature and validity before grant
- Streams without valid attestations are excluded from grants

**Verification:** Submit a CAPABILITY_NEG with an expired attestation; confirm the corresponding subscription is rejected with EXPIRED_ATTESTATION.

#### `ch14-sync-daemon-protocol:SYNC-13` — ACK with granted_subscriptions and typed rejections

The accepting node responds with granted_subscriptions[] and a rejected[] list using typed reason codes (MISSING_ATTESTATION, EXPIRED_ATTESTATION, INVALID_SIGNATURE), and silently omits streams the requester has no attestation for to prevent stream enumeration.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- ACK enumerates only granted subscriptions and explicitly rejected ones
- Rejection codes are limited to the specified taxonomy
- Streams the requester is unaware of are absent from both arrays

**Verification:** Request a stream the receiver does not publish to the requester; confirm it appears in neither granted nor rejected arrays.

#### `ch14-sync-daemon-protocol:SYNC-14` — DELTA_STREAM continuous CRDT operation flow

After ACK, both nodes emit a continuous append-only stream of compact binary CRDT deltas computed from the difference between sender state and receiver vector clock, with out-of-scope operations dropped at the send tier.

**Kleppmann:** `P3, P4` · **Scope:** `foundational`

**Must implement:**

- Deltas are computed per receiver vector clock
- Out-of-scope operations are dropped at the sender, not filtered at the receiver
- Receiver applies operations and advances its vector clock

**Verification:** Observe wire trace; confirm deltas contain only operations the receiver has not seen and only for granted subscriptions.

#### `ch14-sync-daemon-protocol:SYNC-15` — GOSSIP_PING for membership and clock summary

Every 30 seconds each node emits GOSSIP_PING carrying its current vector clock summary and known-peer membership list, enabling drift detection, peer discovery via transitive knowledge, and network healing without a central directory.

**Kleppmann:** `P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `clock-skew, peer-discovery-failure`

**Must implement:**

- Daemon emits GOSSIP_PING on a 30-second cadence (configurable)
- GOSSIP_PING carries vector clock summary and membership entries
- Receiving node merges new peers and updated addresses into local membership list

**Verification:** Three-node test where C learns of B's new address only via A's GOSSIP_PING transitively forwarding it.

#### `ch14-sync-daemon-protocol:SYNC-16` — CBOR canonical wire encoding with length prefix

All wire messages use CBOR (RFC 8949) canonical encoding, length-prefixed with a 4-byte big-endian frame length, with individual frames capped at 16 MiB and unknown fields ignored for forward compatibility.

**Scope:** `inverted-stack-specific`

**Must implement:**

- All frames use CBOR canonical encoding
- 4-byte big-endian length precedes each CBOR payload
- Frames exceeding 16 MiB are rejected
- Unknown fields are ignored on decode

**Verification:** Send a frame with an unknown field; confirm receiver accepts the frame and processes the known fields.

#### `ch14-sync-daemon-protocol:SYNC-17` — Replay-window-bounded signed HELLO

HELLO is signed with the sender's Ed25519 key over (node_id, schema_version, public_key, sent_at) and accepted only within a ±30-second replay window of receiver clock.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `replay`

**Must implement:**

- HELLO signature is Ed25519 over the specified canonical tuple
- Receiver rejects HELLO with sent_at outside ±30-second window
- Receiver verifies signature against the embedded public_key

**Verification:** Replay a captured HELLO 60 seconds later; confirm receiver rejects it on replay-window grounds.

#### `ch14-sync-daemon-protocol:SYNC-18` — Membership list with tier-aware addressing

Each node maintains a membership list recording peer node ID, last-known address per discovery tier, current reachability state (active/suspected/failed), and last-received vector clock per peer.

**Kleppmann:** `P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `peer-discovery-failure`

**Must implement:**

- Membership entry stores per-tier last-known address
- Entry tracks reachability state in {active, suspected, failed}
- Entry tracks last-received vector clock from peer

**Verification:** Inspect daemon membership store; confirm presence of all four fields per peer.

#### `ch14-sync-daemon-protocol:SYNC-19` — Random-peer-selection gossip anti-entropy

Every 30 seconds each node selects two peers at random from its active membership list and initiates a symmetric delta exchange, ensuring O(log N) propagation and preventing load concentration on high-degree nodes.

**Kleppmann:** `P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Daemon selects k random peers (default k=2) per gossip tick
- Exchange is symmetric — each side sends operations the other lacks
- 30-second default interval is configurable per deployment

**Verification:** Run a 10-node simulation; confirm convergence in O(log N) rounds and even per-node send/receive distribution.

#### `ch14-sync-daemon-protocol:SYNC-20` — Vector-clock-driven delta computation

Each CRDT operation carries a vector clock entry identifying the originating node and logical time, and deltas include all operations causally ahead of the remote peer's last known clock.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `clock-skew, partition`

**Must implement:**

- Operations carry per-node vector clock entries
- Receiver advances its vector clock on operation apply
- Delta computation includes only operations causally ahead of remote clock

**Verification:** Two-peer convergence test under partition heal; confirm byte-identical state after exchange.

#### `ch14-sync-daemon-protocol:SYNC-21` — Send-tier subscription scope enforcement

The sync daemon enforces subscription scope at the stream level before operations leave the node, ensuring unauthorized data never reaches the receiving device — application-layer filtering is not a substitute.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection, key-compromise`

**Must implement:**

- Subscription eligibility is checked on the sender prior to transmission
- Out-of-scope operations are not transmitted and not logged
- Receiver never receives operations for unauthorized streams or fields

**Verification:** Capture wire trace from sender; confirm operations for out-of-scope streams/fields never appear on the wire.

#### `ch14-sync-daemon-protocol:SYNC-22` — Field-level scope stripping within streams

Stream definitions specify the minimum field set required per role, and the daemon strips operations for out-of-scope fields when constructing outbound deltas even within streams the receiver is authorized to receive.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Stream definitions encode per-role minimum field sets
- Daemon strips out-of-scope-field operations at delta construction
- Field-level exclusions are invisible to the receiver

**Verification:** Two-role test where Role A receives a stream with field set {x, y} and Role B receives the same stream with {x}; confirm Role B's wire trace contains no operations for field y.

#### `ch14-sync-daemon-protocol:SYNC-23` — Re-eligibility check on reconnect

When a node reconnects after offline, the daemon re-runs eligibility checks during the handshake before replaying buffered deltas, and excludes streams whose attestations expired during the offline period.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Buffered deltas are not replayed before fresh CAPABILITY_NEG completes
- Expired-attestation streams are excluded from new session grants
- Buffered deltas for excluded streams are dropped, not delivered

**Verification:** Expire a node's attestation while offline; reconnect and confirm no buffered deltas for that stream are delivered post-handshake.

#### `ch14-sync-daemon-protocol:SYNC-24` — Distributed quorum lease for CP-class records

Before a node writes to a CP-class record it must acquire a distributed lease requiring acknowledgement by ceil(N/2)+1 of the active membership, with a default 30-second lease duration.

**Kleppmann:** `P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Daemon requests a lease for every CP-class write
- Default quorum is ceil(N/2)+1 of active membership
- Default lease duration is 30 seconds

**Verification:** Attempt a CP-class write with N=3 and only 1 peer reachable; confirm the write blocks rather than proceeding.

#### `ch14-sync-daemon-protocol:SYNC-25` — No-fallback semantics for blocked CP writes

When quorum is unreachable, the daemon blocks the CP-class write rather than degrading to a best-effort write, surfacing a definitive failure signal to the application UI.

**Kleppmann:** `P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Daemon never silently queues a CP-class write when quorum is unreachable
- Application receives an explicit failure signal for blocked writes
- UI reflects blocked-write status with a definitive indicator

**Verification:** Force a partition; attempt a CP-class write; confirm explicit failure signal reaches the application within the configured timeout.

#### `ch14-sync-daemon-protocol:SYNC-26` — Lease expiry via missed renewal pings

Leases expire automatically at the configured duration; a node that goes offline without explicit release loses the lease, and other nodes detect expiry through absence of a renewal GOSSIP_PING.

**Kleppmann:** `P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Leases expire on a wall-clock timer at the configured duration
- Daemon does not require explicit release for expiry
- Other nodes infer expiry from missing renewal GOSSIP_PINGs

**Verification:** Acquire a lease, kill the holding daemon mid-write; confirm a different node acquires the lease after expiry without manual intervention.

#### `ch14-sync-daemon-protocol:SYNC-27` — Early lease-conflict surfacing in CAPABILITY_NEG

CAPABILITY_NEG carries the cp_leases[] field so peer handshakes immediately surface lease conflicts on shared records rather than deferring detection until the write attempt.

**Kleppmann:** `P4` · **Scope:** `inverted-stack-specific`

**Must implement:**

- CAPABILITY_NEG includes cp_leases[] for all leases the node currently holds
- Daemon detects conflicts at handshake time and signals them to the application

**Verification:** Two nodes hold conflicting lease intentions; confirm the conflict is reported during handshake, not at first write attempt.

#### `ch14-sync-daemon-protocol:SYNC-28` — Exponential backoff with jitter on reconnect

When a previously unavailable network path becomes reachable, the daemon waits a random interval drawn from an exponential distribution bounded at 60 seconds before initiating handshake, ensuring simultaneously disconnected nodes do not reconnect simultaneously.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Backoff formula is min(base * 2^attempt, max_seconds) + uniform_jitter(0, jitter_range)
- Maximum backoff is 60 seconds (relay-enforced)
- A node offline beyond a full gossip cycle uses maximum backoff on first reconnect

**Verification:** Simulate 100 nodes reconnecting after a partition heal; confirm reconnection events are spread across the 60-second window.

#### `ch14-sync-daemon-protocol:SYNC-29` — Relay-enforced per-node delta rate limiting

The managed relay enforces a per-node rate limit on delta submissions with a bounded queue that drops the oldest queued submission on overflow, signalling flow control via the next handshake ACK.

**Kleppmann:** `P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Relay queues rather than rejects nodes exceeding the rate limit
- Queue is bounded; oldest entry is dropped on overflow
- Flow-control indication is delivered in the next ACK frame
- Receiving node increases backoff interval after flow-control signal

**Verification:** Submit deltas faster than the rate limit through the relay; confirm queue behavior and ACK-borne flow-control signal.

#### `ch14-sync-daemon-protocol:SYNC-30` — Three-to-five interval failure detection

A peer that misses three consecutive GOSSIP_PINGs transitions from active to suspected, and after five total missed intervals transitions from suspected to failed and is removed from the active membership list.

**Kleppmann:** `P4` · **Scope:** `foundational` · **Failure modes:** `partition, peer-discovery-failure`

**Must implement:**

- Three missed GOSSIP_PINGs triggers active-to-suspected transition
- Five total missed intervals triggers suspected-to-failed transition
- Failed peers are removed from active membership list
- Suspected peers continue to receive GOSSIP_PINGs

**Verification:** Block GOSSIP_PINGs to one peer; observe state transitions at the 3rd and 5th missed intervals.

#### `ch14-sync-daemon-protocol:SYNC-31` — Suspected-peer recovery without re-handshake

A suspected peer that responds to a GOSSIP_PING transitions immediately back to active and resumes delta exchange on the existing session without requiring a fresh handshake.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Suspected-to-active transition occurs on first GOSSIP_PING response
- Existing session is preserved across suspected interval
- No fresh CAPABILITY_NEG is required for recovery

**Verification:** Drive a peer to suspected state, then resume responses; confirm session continues without re-handshake and accumulated deltas exchange.

#### `ch14-sync-daemon-protocol:SYNC-32` — Address-change reconnect on same node ID

A new peer presenting the same node ID as a previously failed peer is treated as a reconnect, triggering a fresh handshake including full CAPABILITY_NEG and resetting the failure counter.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `peer-discovery-failure`

**Must implement:**

- Daemon recognizes returning node IDs and resets failure counter
- Address change triggers fresh CAPABILITY_NEG, not stale-session reuse
- Membership list updates to the new address

**Verification:** Have a node move from Wi-Fi to cellular, presenting the same node ID at a new address; confirm fresh handshake completes and old address is replaced.

#### `ch14-sync-daemon-protocol:SYNC-33` — Transitive address propagation via gossip

Stale addresses are cleaned through explicit removal at failed-state and through address updates carried in incoming GOSSIP_PING messages, allowing transitive learning of new addresses without direct contact.

**Kleppmann:** `P4` · **Scope:** `foundational` · **Failure modes:** `peer-discovery-failure`

**Must implement:**

- Address updates in GOSSIP_PING overwrite older entries for the same node ID
- Failed-state removal clears stale entries from active list
- Node C learns Node B's new address via Node A's gossip

**Verification:** Three-node test where A learns of B's new address from C without A having pinged B directly at the new address.

#### `ch14-sync-daemon-protocol:SYNC-34` — Sunfish.Kernel.Sync as protocol entry point

The sync daemon's full protocol lifecycle — discovery, handshake, delta computation, gossip, lease coordination, reconnection backoff — is exposed to the application via the Sunfish.Kernel.Sync package, with stream definitions registered there declaring the field-level access rules the daemon enforces.

**Kleppmann:** `P3, P4, P6, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Sunfish.Kernel.Sync namespace exists and exposes the daemon command channel
- Stream definitions registered through the package drive daemon enforcement
- Application has no code path that re-implements any part of the sync protocol

**Verification:** Inspect application code; confirm all sync operations go through Sunfish.Kernel.Sync and stream definitions are the sole source of access rules.

#### `ch14-sync-daemon-protocol:SYNC-35` — Uniform protocol guarantees across all transport tiers

The protocol invariants — source-side subscription scope, quorum-required CP writes, handshake-before-data-flow, rate-controlled reconnection — hold uniformly across mDNS, mesh VPN, and managed relay, with no trusted-network mode that relaxes rules for LAN peers.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- No code path bypasses scope enforcement on LAN peers
- No code path bypasses quorum requirement on LAN peers
- No code path bypasses handshake on LAN peers
- All transport tiers apply identical protocol rules

**Verification:** Audit transport-tier branches in daemon code; confirm no per-tier conditional that disables an invariant.


### Epic: Security Architecture (ch15-security-architecture)

**Source-paper refs:** v13 §11, v5 §4

**Concept count:** 36

#### `ch15-security-architecture:SEC-01` — Distributed honeypot threat model

Distributing data to endpoints does not eliminate the honeypot problem but spreads it across many smaller perimeters whose weakest device sets the attacker's minimum viable entry cost.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Architecture documents that endpoint compromise is an expected event, not an exception
- System bounds blast radius rather than denying endpoint exposure

**Verification:** Threat model document explicitly enumerates endpoint compromise as in-scope and states the bounded blast radius as a design property

#### `ch15-security-architecture:SEC-02` — Three blast-radius bounding properties

Each node holds only data its role subscriptions permit, per-role keys are absent from non-member nodes, and key compromise does not expose historical data encrypted under previously rotated keys.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Node storage contains only data for roles the node holds
- Per-role encryption keys are absent from non-member nodes
- Rotated keys remain absent from compromised nodes after rotation

**Verification:** Compromise simulation test confirms that seizing one node's full disk and memory exposes only data for that node's current role keys

#### `ch15-security-architecture:SEC-03` — Zero-knowledge relay

The relay is treated as an untrusted intermediary that routes ciphertext only and never holds decryption keys, so a relay operator cannot read payload plaintext.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Encryption is applied at the originating node before payload enters the relay
- Relay code paths have no access to decryption keys
- Relay receives, validates subscription, and forwards ciphertext only

**Verification:** Relay process memory and storage contain no key material capable of decrypting any payload it routes

#### `ch15-security-architecture:SEC-04` — Relay metadata visibility

The relay observes the communication graph — which node identifiers communicate with which, when, in what volume, and with what burst pattern — even though it cannot read payload content.

**Kleppmann:** `P6` · **Scope:** `foundational`

**Must implement:**

- Documentation enumerates exactly which metadata fields the relay observes
- Self-hosted relay deployment path exists for metadata-sensitive deployments

**Verification:** Relay observability documentation lists every metadata channel and identifies which deployment topology eliminates each

#### `ch15-security-architecture:SEC-05` — Defense in depth — four independent layers

Security applies four independent layers — encryption at rest, field-level encryption, stream-level data minimization, and circuit breaker quarantine — where defeating one layer yields no advantage on the next.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Each layer is implemented in a separately auditable module
- No layer's correctness depends on another layer being uncompromised

**Verification:** Static analysis confirms no shared trust assumption between the four layer implementations

#### `ch15-security-architecture:SEC-06` — SQLCipher encryption at rest with OS keystore root

Local databases use SQLCipher with the database key derived via HKDF-SHA256 from a 256-bit root seed stored in the OS-native keystore (Keychain, DPAPI, or Linux Secret Service).

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Local database files are encrypted using SQLCipher
- Root seed is 256 bits from a CSRNG and stored only in the OS keystore
- Database key is derived via HKDF-SHA256 from the root seed
- Database key is loaded on demand and zeroed after the session closes
- Database key is never written to disk

**Verification:** Disk forensic capture of the database file without OS keystore access yields no plaintext; process memory inspection after database close finds no residual key bytes

#### `ch15-security-architecture:SEC-07` — Field-level encryption with per-role keys

Records in high-sensitivity buckets carry per-field encryption under per-role symmetric keys distinct from the database key, so opening the database does not grant access to fields the node lacks the role for.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Fields in high-sensitivity buckets are encrypted with per-role keys
- The field-level key is distinct from the database key
- Decryption fails closed when the role key is absent

**Verification:** Test demonstrates a node with database access but without a role key cannot read field-encrypted records for that role

#### `ch15-security-architecture:SEC-08` — Send-tier subscription filtering invariant

The sync daemon enforces subscription filtering before any event leaves the originating node, so non-subscribed nodes never receive events regardless of relay state or administrator misconfiguration.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Sync daemon filters events at the originating node before transmission
- No code path bypasses send-tier filtering for any event class

**Verification:** Wire-protocol test confirms that events outside a peer's declared subscription set are never observed entering the relay from the originating node

#### `ch15-security-architecture:SEC-09` — Circuit breaker quarantine for offline writes

Writes from a reconnecting node that conflict with current authorization policy are held in quarantine pending administrator review rather than discarded or auto-applied.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Reconnecting nodes' writes are validated against current team state
- Conflicting writes enter a quarantine queue
- Administrator promotes or rejects each quarantined write with logged reason
- Audit trail records what was offered, who reviewed, and what decision was made

**Verification:** Quarantine review test produces an audit record containing offered write, reviewer identity, decision, and reason

#### `ch15-security-architecture:KEY-01` — Four-tier key hierarchy

Keys are organized in four independently rotatable tiers — root organization key, role KEKs, node-level wrapped KEK copies, and per-document DEKs.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Each tier has a distinct key type with its own rotation procedure
- Rotation of any tier does not require rotating other tiers

**Verification:** Rotation procedure for each tier exists and is independently exercisable in isolation tests

#### `ch15-security-architecture:KEY-02` — KEK/DEK envelope encryption

Each document is encrypted under a freshly generated 256-bit DEK using AES-256-GCM, and the DEK is itself wrapped under the role's current KEK so KEK rotation re-wraps DEKs without re-encrypting document bodies.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- DEK is 256 bits from the OS CSRNG, generated fresh per document
- Document body encrypted with AES-256-GCM, 96-bit random nonce per encryption, 128-bit tag
- DEK wrapped with current role KEK using AES-256-GCM with fresh 96-bit nonce
- Wrapped DEK stored alongside ciphertext
- KEK never touches document body
- DEK does not persist in unwrapped form beyond the active decryption operation

**Verification:** Encryption library test confirms nonces are randomly generated per encryption event and never reused under the same key

#### `ch15-security-architecture:KEY-03` — Argon2id parameters for credential-derived keys

When user credentials derive an OS keystore password, Argon2id runs with memory cost 64 MiB, iteration count 3, parallelism 4 for standard deployments and 128 MiB / 4 / 4 for the high-security tier.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Argon2id is the credential KDF
- Standard tier uses memory 64 MiB, iterations 3, parallelism 4
- High-security tier uses memory 128 MiB, iterations 4, parallelism 4
- Configuration names the chosen tier explicitly

**Verification:** Configuration file inspection confirms Argon2id parameters match the standard or high-security tier values exactly

#### `ch15-security-architecture:KEY-04` — Node-level wrapped KEK custody

Each node holds wrapped copies of its role KEKs that are decryptable only with the node's device private key, so revocation by withholding new bundles renders existing wrapped copies useless after rotation.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- KEK copies on a node are wrapped under that node's device public key
- Device private key is the sole unwrap path for that node's KEK copies
- Revoked nodes are excluded from new bundle distribution

**Verification:** Test confirms a captured wrapped KEK blob cannot be unwrapped without the originating device's private key

#### `ch15-security-architecture:KEY-05` — Role attestations distinct from role keys

Role attestations prove role membership for subscription decisions while role keys enable decryption, with key possession verified separately before field-encrypted content is delivered.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Sync daemon uses signed attestations for subscription decisions
- Field-encrypted content delivery requires separate proof of key possession
- A node holding neither attestation nor key receives no events

**Verification:** Test confirms a node presenting an attestation but lacking the role key cannot decrypt delivered field-encrypted content

#### `ch15-security-architecture:KEY-06` — Administrator-signed key bundle distribution

Per-role KEKs are wrapped per-member with the member's device public key and published as administrator-signed administrative events in the CRDT log, with nodes verifying the signature before accepting any bundle.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Per-role KEK is generated from a fresh entropy source, not derived from any organizational root
- KEK is wrapped per member using the member's device public key
- Wrapped bundles are published as administrative events in the CRDT log
- Administrative events are signed by the administrator key
- Receiving nodes verify the signature before accepting the bundle

**Verification:** Test confirms an unsigned or invalidly signed bundle is rejected and never written to the OS keystore

#### `ch15-security-architecture:KEY-07` — KEK rotation without document re-encryption

KEK rotation re-wraps DEKs under the new KEK without touching document ciphertext, so rotation work is proportional to document count rather than cumulative document size.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Rotation procedure re-wraps DEKs under new KEK
- Document bodies are not re-encrypted on KEK rotation

**Verification:** Rotation benchmark confirms work scales with document count, not cumulative document byte size

#### `ch15-security-architecture:KEY-08` — Key compromise incident response procedure

On compromise, the administrator generates a new KEK from fresh entropy (never derived from the compromised key), re-wraps all affected DEKs, distributes new bundles, then triggers discard of the old KEK and a revocation broadcast.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- New KEK is generated from fresh entropy, never derived from the compromised key
- All DEKs in scope are re-wrapped under the new KEK before old KEK discard
- Old KEK discard signal zeros in-memory copies and removes keystore entries on every node
- Revocation event is published for the compromised key identifier
- Affected users receive a notification specifying the data-at-risk window

**Verification:** Incident-response runbook is exercised end-to-end and produces an audit log showing each step in order

#### `ch15-security-architecture:KEY-09` — Detection triggers for key compromise

Compromise detection arrives from physical loss reports, anomalous access patterns in the audit log, or explicit administrator reports of suspected credential exposure.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- All key access events are logged to the audit log
- Anomaly detection runs over the audit log
- User-facing reporting flow exists for physical loss
- Administrator-initiated incident-response trigger exists

**Verification:** Each of the three trigger types produces an incident-response activation in test

#### `ch15-security-architecture:KEY-10` — Handshake-layer revocation enforcement

The relay enforces key revocation at the connection handshake by rejecting any node presenting a revoked key identifier with the specific error code ERR_KEY_REVOKED rather than a generic failure.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise, key-loss`

**Must implement:**

- Relay maintains a revocation log indexed by key identifier
- Handshake checks each presented key identifier against the revocation log
- Revoked-key handshakes return ERR_KEY_REVOKED
- Client distinguishes ERR_KEY_REVOKED from network and certificate errors

**Verification:** Reconnection test with a revoked key receives ERR_KEY_REVOKED specifically

#### `ch15-security-architecture:KEY-11` — Re-attestation via IdP after revocation

A revocation-rejected node cannot resume sync until the user re-authenticates through the IdP, after which the administrator's device issues new wrapped KEK copies for the user's current roles.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Revocation rejection blocks sync until re-authentication
- Re-authentication establishes fresh role attestations against current team state
- Administrator device detects reconnected node and issues new KEK bundles

**Verification:** End-to-end test exercises revocation, IdP re-authentication, KEK redelivery, and sync resumption

#### `ch15-security-architecture:KEY-12` — Offline compromise window

A node offline during a KEK discard broadcast continues to use the compromised KEK until reconnection, bounded by configurable rotation schedule (default 90 days) and relay-enforced revocation on reconnect.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise, partition`

**Must implement:**

- KEK rotation schedule is configurable per role
- Default rotation interval is 90 days or any role-membership change
- Documentation explicitly names the residual exposure between discard broadcast and offline node reconnect

**Verification:** Configuration documents the rotation schedule and the exposure window is named in security documentation

#### `ch15-security-architecture:SEC-10` — Locked memory pages for key material

Key material is allocated in pages marked non-swappable using mlock on POSIX or VirtualLock on Windows so the OS cannot page key bytes to disk under memory pressure.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Key allocations call the platform memory-locking API
- Locked-page allocator is the only allocation path for key material

**Verification:** Source review confirms every key allocation uses the locked-page allocator

#### `ch15-security-architecture:SEC-11` — Compiler-resistant zeroing on exit

Key material is zeroed before process exit using a function the compiler cannot optimize away, including under abnormal exit via registered signal handlers.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Zeroing function is dead-store-elimination resistant
- Exit handlers zero key material on normal exit
- Signal handlers zero key material on abnormal exit
- Platform-provided secure zeroing is used where available

**Verification:** Process memory inspection after exit (including SIGTERM and SIGABRT) finds no residual key bytes

#### `ch15-security-architecture:SEC-12` — Re-authentication interval

A configurable re-authentication interval (default four hours, sixty minutes for highly regulated deployments) evicts in-memory key material and prompts re-authentication to bound cold-boot and memory-forensics exposure.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Re-authentication interval is enforced in the kernel
- Default interval is four hours
- Interval is configurable per deployment sensitivity tier
- Hardware-backed authentication (FIDO2 or smart card) removes the interval-based tradeoff

**Verification:** Session test confirms key material is evicted after the configured interval and re-authentication is required to resume key-using operations

#### `ch15-security-architecture:SEC-13` — Content-addressed update verification

Each update package is identified by a content identifier (CID) computed from package contents and distributed via a signed release manifest separate from the CDN, with the client verifying the computed CID before installation.

**Kleppmann:** `P6, P7` · **Scope:** `foundational`

**Must implement:**

- Each update package has a CID computed from its contents
- CID is distributed in a signed release manifest separate from the CDN
- Client computes the CID of the downloaded package and compares against the manifest
- CID mismatch aborts installation

**Verification:** Tampered-binary test produces a CID mismatch and aborts installation

#### `ch15-security-architecture:SEC-14` — Hardware-custodied release signing key

The release signing key is held in a hardware security module under multi-party authorization, with signing operations requiring quorum approval and the key never present in CI/CD environments.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Release signing key is HSM-resident
- Signing requires multi-party quorum
- CI/CD environments have no access to the signing key

**Verification:** Audit confirms HSM custody, quorum policy, and absence of the key from CI/CD secret stores

#### `ch15-security-architecture:SEC-15` — Sigstore transparency log enforcement

All signing events are logged to Rekor, and clients reject any signed package whose signing event is absent from the transparency log beyond a short propagation hold period.

**Kleppmann:** `P6` · **Scope:** `foundational`

**Must implement:**

- All package signing events are submitted to Rekor
- Client verifies presence of the signing event in Rekor before accepting the package
- A short hold period is permitted for recent signing events

**Verification:** Test with a signed-but-unlogged package is rejected by the client

#### `ch15-security-architecture:SEC-16` — Reproducible builds

Independent parties can reproduce the published binary from published source and verify the computed CID matches, providing an independent verification path beyond the signing key.

**Kleppmann:** `P6` · **Scope:** `foundational`

**Must implement:**

- Build is bit-for-bit reproducible from published source
- Build documentation enables third-party reproduction

**Verification:** An independent party reproduces the binary and confirms CID equality with the published manifest

#### `ch15-security-architecture:SEC-17` — Crypto-shredding for GDPR Article 17

Erasure requests destroy the DEK for the targeted record, leaving the operation entry in the immutable log while making its ciphertext permanently unreadable.

**Kleppmann:** `P6, P7` · **Scope:** `foundational`

**Must implement:**

- Erasure operation zeros the targeted DEK from all node keystores
- Operation stub remains in the log with a marker indicating destroyed DEK
- Erasure event is logged with data subject identifier, targeted operation identifier, and timestamp
- No copy of the destroyed DEK is retained anywhere in the system

**Verification:** After crypto-shredding, the targeted record's ciphertext is recoverable but no key path exists to decrypt it

#### `ch15-security-architecture:SEC-18` — Residual metadata limitation

Operation identifier, timestamp, and DAG position are not erasable without breaking log structure and constitute residual metadata whose Article 17 sufficiency is jurisdiction-dependent.

**Kleppmann:** `P6` · **Scope:** `foundational`

**Must implement:**

- Documentation enumerates exactly what metadata residue remains after crypto-shredding
- Legal review is required before relying on crypto-shredding for an Article 17 response

**Verification:** Compliance documentation explicitly names the residual metadata fields and the legal-review prerequisite

#### `ch15-security-architecture:SEC-19` — Compelled-access structural defense

The relay cannot produce decryptable content under legal compulsion because it does not possess decryptable content, providing a structural answer to compelled-access threat models that customer-managed-key cloud patterns cannot match.

**Kleppmann:** `P6, P7` · **Scope:** `foundational`

**Must implement:**

- Relay holds no decryption keys for any payload it routes
- Decryption keys never leave originating nodes

**Verification:** Legal-process simulation confirms relay can only produce ciphertext and metadata, never plaintext

#### `ch15-security-architecture:SEC-20` — Self-hosted relay for metadata-sensitive deployments

Deployments where the communication graph itself is sensitive replace the third-party relay with a self-hosted relay running the same codebase under the organization's operational custody.

**Kleppmann:** `P6, P7` · **Scope:** `foundational`

**Must implement:**

- Relay binary is deployable on customer-controlled infrastructure
- Self-hosted relay is the same codebase as the managed relay
- Connection logs on a self-hosted relay are subject to the operator's retention policy

**Verification:** Self-hosted deployment guide exists and the relay binary runs identically against the standard wire protocol

#### `ch15-security-architecture:SEC-21` — Break-glass corrupt-sequence quarantine

When a CRDT sequence arrives in a structurally invalid state (signature mismatch, unknown reference, or unresolved schema-version violation), the sync daemon quarantines the full sequence and requires explicit administrator action to dispose of it.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Structurally invalid sequences are fully quarantined, never partially applied
- Administrator console exposes a quarantine viewer
- Disposition is one of reject, promote-after-correction, or request-resend
- Audit log captures sequence, administrator determination, and disposition

**Verification:** Test injecting a signature-mismatch sequence produces full quarantine and an audit record on disposition

#### `ch15-security-architecture:SEC-22` — Traffic-analysis limitation

The architecture does not implement constant-rate padding between nodes, so deployments with traffic-analysis adversaries must apply application-layer obfuscation or route through a mixnet outside the kernel scope.

**Kleppmann:** `P6` · **Scope:** `foundational`

**Must implement:**

- Documentation explicitly names absence of constant-rate padding
- Documentation names mixnet or application-layer obfuscation as the operator-deployment mitigation

**Verification:** Security documentation lists traffic-analysis as a named limitation with a documented mitigation path

#### `ch15-security-architecture:SEC-23` — Long-lived Ed25519 device keypairs for non-repudiation

Every write is signed by a long-lived Ed25519 device keypair stored in a hardware-backed OS keystore where available, so a node cannot deny authorship of an operation it signed.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Each device holds a long-lived Ed25519 keypair
- Private key is stored in a hardware-backed OS keystore where available
- Every write carries a signature attributable to a device key

**Verification:** Audit log entry for any write resolves to a device public key whose signature validates the operation bytes

#### `ch15-security-architecture:SEC-24` — Administrator device as trust anchor

The administrator device is the system's trust anchor whose compromise enables fraudulent key distribution, and its protection is an organizational responsibility outside the scope of the security kernel.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Documentation names the administrator device as the trust anchor
- Hardware-backed key storage is required for administrator operations in elevated threat models
- Administrator operations are restricted to managed devices with HSMs in regulated deployments

**Verification:** Security documentation explicitly identifies the administrator device as the trust anchor and names its required hardware posture


### Epic: Persistence Beyond the Node (ch16-persistence-beyond-the-node)

**Source-paper refs:** v13 §2.4, v13 §8, v13 §9, v13 §10, v5 §3.5

**Concept count:** 29

#### `ch16-persistence-beyond-the-node:DUR-01` — Node as authority over data it holds

Local-first does not mean data lives only on one machine; it means the node is the authority over the data it holds, and persistence beyond the node is composed from explicit additional tiers.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- Architecture documents how data survives device loss without ceding authority to a vendor
- No persistence tier introduces a central server that can override the node's local authority

**Verification:** Architecture document specifies persistence tiers and names the authority for each tier as the node, not a vendor service.

#### `ch16-persistence-beyond-the-node:DUR-02` — Five-layer storage architecture

Persistence is composed of five specialized tiers — local encrypted database, CRDT and event log, user-controlled cloud backup, content-addressed distribution (opt-in), and decentralized archival (opt-in) — rather than a single database system.

**Kleppmann:** `P3, P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-outage`

**Must implement:**

- Implementation distinguishes the five tiers as separately addressable subsystems
- Tiers 1-3 are mandatory; Tiers 4-5 are opt-in and absence does not constitute degradation
- Each tier resolves a distinct named failure mode

**Verification:** Architecture document enumerates the five tiers with named subsystems for each; an implementation that omits Tiers 4-5 is documented as a standard configuration.

#### `ch16-persistence-beyond-the-node:DUR-03` — Event log as source of truth

An append-only log of all CRDT operations and domain events is the system's source of truth for sync and audit; the local database is a derived projection of the log.

**Kleppmann:** `P5, P7` · **Scope:** `foundational`

**Must implement:**

- Append-only event log is persisted distinctly from the queryable local database
- Local database can be rebuilt deterministically from the event log
- Event log survives database deletion or corruption

**Verification:** Deleting the local database file and replaying the event log reproduces equivalent application state.

#### `ch16-persistence-beyond-the-node:DUR-04` — Declarative sync buckets

A bucket is a named, declaratively specified subset of the team dataset whose membership is tied to role attestations and enforced by the sync daemon at capability negotiation, not by application-layer filtering after data arrives.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection`

**Must implement:**

- Buckets are declared in a static configuration (e.g., YAML) with name, record types, filter, replication mode, and required attestation
- Sync daemon evaluates bucket eligibility against verified peer attestations before sending any data
- Non-eligible peers never receive bucket events at the protocol layer

**Verification:** A peer presenting only `team_member` attestation receives only buckets whose `required_attestation` matches; financial buckets are never forwarded to it on the wire.

#### `ch16-persistence-beyond-the-node:DUR-05` — Eager versus lazy bucket replication

Each bucket declares a replication mode — eager buckets sync immediately on connect; lazy buckets use demand-driven fetch and represent records locally as stubs.

**Kleppmann:** `P1, P2` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Sync daemon supports both `eager` and `lazy` replication modes per bucket
- Lazy bucket records materialize as stubs locally until fetched
- Eager bucket records replicate fully on capability negotiation

**Verification:** A bucket configured `replication: lazy` produces stub records on subscribing peers; opening a record triggers a content fetch.

#### `ch16-persistence-beyond-the-node:DUR-06` — Stub records with content hash

A stub is a local representation of a lazy or evicted record containing identifier, display metadata, and content hash but no payload, sufficient to render navigation, search, and lists without fetching content.

**Kleppmann:** `P1, P3` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Stub structure includes record identifier, navigation metadata (title, type, author, last-modified), and content hash
- Application can render lists, navigation, and search over stubs without fetching content
- Stub-to-full transitions verify the content hash before writing to local database

**Verification:** Disconnect network; navigation and search over lazy buckets render using stub metadata only.

#### `ch16-persistence-beyond-the-node:DUR-07` — Configurable local storage budget with LRU eviction

Nodes enforce a configurable local storage budget (default 10 GB); when approaching the ceiling, the sync daemon evicts least-recently-used records from lazy buckets back to stubs without deleting them.

**Kleppmann:** `P2` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Local storage budget is configurable at the workspace level
- Eviction policy converts full lazy records back to stubs preserving identifier, metadata, and content hash
- Eager bucket records are not evicted by the budget mechanism

**Verification:** Set storage budget below current footprint; eviction reduces local storage and converts evicted records to stubs that remain accessible on demand.

#### `ch16-persistence-beyond-the-node:DUR-08` — Mandatory content hash verification on fetch

Every fetched record must have its content hash verified against the stub's stored hash before being written to the local database; mismatched fetches are rejected and re-requested from an alternate peer.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Sync daemon computes hash of fetched content and compares against stub hash before commit
- Hash mismatch triggers rejection and re-request from a different peer
- No code path writes fetched content to local database without hash verification

**Verification:** Inject a corrupted content payload from a peer; the receiving node rejects the fetch and re-requests from an alternate peer.

#### `ch16-persistence-beyond-the-node:DUR-09` — Snapshot as performance optimization over event log

A snapshot captures the current state of an aggregate at a point in time indexed to the last event it incorporates; snapshots are deletable and regenerable without affecting correctness because the event log remains the source of truth.

**Kleppmann:** `P1, P5` · **Scope:** `foundational`

**Must implement:**

- Snapshot record includes aggregate_id, epoch_id, schema_version, last_event_seq, payload, and creation timestamp
- Snapshots are stored separately from the event log
- Deleting all snapshots and rehydrating from the log produces equivalent application state

**Verification:** Delete the snapshot store; aggregate rehydration replays from the beginning of the event log and reproduces identical state.

#### `ch16-persistence-beyond-the-node:DUR-10` — Epoch- and schema-scoped snapshot rehydration

Rehydration loads the most recent snapshot, verifies its epoch and schema version match current values, replays subsequent events with upcasters applied for older schema versions, and discards snapshots that do not match.

**Kleppmann:** `P5` · **Scope:** `inverted-stack-specific` · **Failure modes:** `schema-skew`

**Must implement:**

- Rehydration verifies snapshot epoch_id and schema_version against current values before use
- Mismatched snapshots are discarded and rehydration falls back to event-log replay
- Schema upcasters are applied during replay for events from older schema versions

**Verification:** Force a snapshot's schema_version to a stale value; rehydration discards it and replays from the log without producing incorrect state.

#### `ch16-persistence-beyond-the-node:DUR-11` — Snapshot scheduling policy

New snapshots are written after rehydration, after a configurable per-document-type operation-count threshold (default 5,000 operations), and on explicit request at application shutdown.

**Kleppmann:** `P1` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Implementation triggers snapshot write after rehydration completes
- Per-document-type operation-count threshold is configurable and triggers snapshot writes
- Explicit snapshot creation is exposed as an API for shutdown hooks

**Verification:** Apply 5,001 operations to an aggregate of a type with default threshold; a new snapshot is written within bounded time.

#### `ch16-persistence-beyond-the-node:DUR-12` — CRDT garbage collection strategies

CRDT documents grow monotonically under naive storage; the architecture mitigates this with three named strategies — library-level compaction, application-level document sharding, and periodic shallow snapshots — with full-history retention as the conservative default.

**Kleppmann:** `P5` · **Scope:** `foundational`

**Must implement:**

- Architecture names the three mitigation strategies and their tradeoffs
- Default policy retains full history relying on library-level compaction
- Application-level sharding and shallow snapshots are opt-in per document type via the schema

**Verification:** Document schema configuration accepts opt-in flags for sharding and shallow-snapshot policies; defaults retain full history.

#### `ch16-persistence-beyond-the-node:DUR-13` — Shallow-snapshot mergeability tradeoff

A shallow snapshot captures current document state without history required to merge with older versions; nodes that discard history below the shallow snapshot cannot merge with peers retaining that older history.

**Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Schema declares opt-in for shallow snapshots per document type
- System surfaces the mergeability tradeoff at configuration time
- Shallow snapshot is reserved for high-write-rate document types (logs, sensor feeds) by policy

**Verification:** Schema documentation for shallow-snapshot-enabled types names the lost-mergeability constraint explicitly.

#### `ch16-persistence-beyond-the-node:DUR-14` — Three-state backup UX

Backup status is exposed to the user as one of three states — Protected, Attention, At Risk — each mapping to a single user action (none, back up now, acknowledge), with no exposure of internal replication factors or vector clocks.

**Kleppmann:** `P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- System surfaces backup state as exactly the three named states
- Attention state offers a single dismissible "Back up now" prompt
- At Risk state displays a persistent warning that returns each session until backup completes; acknowledgement records awareness but does not clear risk

**Verification:** Force backup lag past the policy window; UI transitions to Attention and offers "Back up now"; force lag past the escalation threshold; UI transitions to At Risk with a non-dismissible warning.

#### `ch16-persistence-beyond-the-node:DUR-15` — Backup state as typed contract, not prescribed UI

The backup state machine is exposed as a typed state by the foundation package; the host application provides the presentation, so the package contract is the state model rather than any specific UI.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Foundation package exposes backup state as a typed enum or equivalent
- No UI rendering is prescribed by the package
- Application can substitute its own presentation while preserving the three-state semantics

**Verification:** `Sunfish.Foundation` exposes a backup state type; no UI components ship in the package.

#### `ch16-persistence-beyond-the-node:DUR-16` — BYOC user-controlled backup destination

The Tier 3 backup adapter accepts any S3-API-compatible endpoint configured by the operator (hyperscaler, EU-resident, sovereign-cloud, on-premise MinIO/Ceph), not a vendor-bound destination.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection, vendor-acquisition, vendor-outage`

**Must implement:**

- Backup adapter is provider-agnostic and configured per deployment
- Adapter accepts any S3-API-compatible endpoint including self-hosted object storage
- No code path requires a specific cloud vendor for backup to function

**Verification:** Configure backup destination to a self-hosted MinIO instance; full backup-and-restore cycle completes without invoking any vendor-specific API.

#### `ch16-persistence-beyond-the-node:DUR-17` — Backup encryption under user key hierarchy

Backup objects contain a full encrypted snapshot of the node's CRDT event log encrypted under a key derived via HKDF-SHA256 from the same DEK/KEK hierarchy that protects the local database; the storage provider cannot read the backup.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise, vendor-acquisition`

**Must implement:**

- Backup encryption key is derived from the same root seed as the local database key
- Backup payload is the encrypted serialized event log, not a raw database file
- Storage provider has no path to plaintext backup contents

**Verification:** Inspect backup objects in storage; payload is opaque ciphertext that cannot be decrypted without the user's key material.

> Cross-references Ch15 key hierarchy.

#### `ch16-persistence-beyond-the-node:DUR-18` — Ciphertext-only relay invariant

The relay routes encrypted CRDT operation frames between authenticated peers without holding decryption keys; it sees peer identities, workspace identifiers, and frame envelopes but no plaintext payload.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise, vendor-acquisition`

**Must implement:**

- Relay code path holds no decryption keys for forwarded payloads
- All frames the relay forwards are end-to-end encrypted under keys that never leave originating devices
- A compromised relay exposes only metadata (who, when, volume), not content

**Verification:** Static analysis of relay binary confirms no key material is accepted or stored; integration test confirms forwarded frames are opaque ciphertext to the relay process.

#### `ch16-persistence-beyond-the-node:DUR-19` — Self-hostable relay binary

The relay is distributed as a single binary (native executable and OCI container image) deployable on operator-controlled infrastructure with a small resource profile (512 MiB RAM, 2 vCPU, 10 GiB disk for fifty-person teams), implementing the same protocol as the managed relay.

**Kleppmann:** `P3, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection, vendor-outage`

**Must implement:**

- Relay ships as both native binary and OCI container image
- Self-hosted and managed relays are protocol-indistinguishable to nodes
- Node `relayEndpoint` configuration redirects to operator-controlled relays without code changes

**Verification:** Deploy self-hosted relay; nodes configured to it complete sync identically to nodes connected to the managed relay.

#### `ch16-persistence-beyond-the-node:DUR-20` — Open relay protocol prevents vendor lock-in

The relay protocol is specified in Chapter 14 with sufficient precision for third-party implementation; there is no proprietary wire format or vendor-specific handshake extension, so any compliant relay is indistinguishable from the first-party relay.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- Relay protocol specification is published under the same license as the kernel
- Specification includes wire format, handshake, and routing semantics with no proprietary extensions
- A third-party relay implementation can interoperate with first-party nodes without vendor cooperation

**Verification:** A third-party relay implementation built from the published specification interoperates with first-party nodes in convergence tests.

#### `ch16-persistence-beyond-the-node:DUR-21` — Relay compelled-access immunity

A subpoena or compulsion order to the relay operator yields connection logs and message envelopes only — never payload plaintext — because the relay structurally does not possess decryptable content.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Relay operator has no technical capability to produce plaintext payloads under legal compulsion
- Compelled-access posture is documented as a structural property, not a policy promise

**Verification:** Architecture document and threat model state the compelled-access invariant; implementation review confirms no key escrow path exists at the relay layer.

#### `ch16-persistence-beyond-the-node:DUR-22` — Peer-assisted device recovery via QR attestation transfer

A new device recovers by authenticating against the IdP and receiving a one-time QR-encoded key exchange from an existing team member's device that transfers the role attestation bundle and an initial CRDT snapshot of authorized eager-bucket records.

**Kleppmann:** `P2, P5` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-loss`

**Must implement:**

- New-device flow detects empty local CRDT state on first launch
- Existing-member device generates a one-time QR-encoded key exchange for attestation transfer
- Transferred attestation bundle is signed by the team's identity authority and cannot be forged by the new device
- Scope of transferred data is bounded by the existing member's own attestation set

**Verification:** Provision a new device; an existing member's QR scan brings the new device to working state with eager-bucket access in minutes, without contacting a central server beyond the IdP.

#### `ch16-persistence-beyond-the-node:DUR-23` — Backup-only recovery without peer assistance

When no team member is available for QR exchange, a new device authenticates against the IdP, retrieves the most recent backup snapshot from user-controlled object storage, applies it locally, and re-synchronizes with peers to incorporate post-backup changes.

**Kleppmann:** `P2, P5` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-loss`

**Must implement:**

- System supports recovery from Tier 3 backup without requiring a peer-assisted handoff
- Recovery flow re-synchronizes with peers after backup application to capture changes since backup
- Recovery produces the same end-state as peer-assisted recovery (full local authority, peer-synced)

**Verification:** Disable peer-assisted path; recovery from backup alone restores the node to working state synchronized with peers.

#### `ch16-persistence-beyond-the-node:DUR-24` — Offline recovery bundle

Each node optionally generates at onboarding a one-time-use cryptographic blob containing a wrapped recovery key and minimum bootstrap attestation, stored out-of-band by the user, that restores the node from backup without IdP availability and expires on use or on a configurable wall-clock timeout (default 12 months).

**Kleppmann:** `P3, P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-loss, vendor-outage`

**Must implement:**

- Node generation flow produces an optional offline recovery bundle at onboarding
- Bundle restores read-write local state from backup with no network connectivity
- Bundle is single-use; on use the recovered node re-attests against the IdP and rotates to a fresh bundle
- Bundle has a configurable wall-clock expiry (default 12 months)

**Verification:** Provision a node, capture its offline recovery bundle, then disconnect network and restore to a new device; the new device reaches read-write state without contacting the IdP.

> Touches Ch15 key recovery; this concept is the persistence-layer mechanism, distinct from key-hierarchy concepts owned by Ch15.

#### `ch16-persistence-beyond-the-node:DUR-25` — Plain-file export as architectural requirement

All user data must be exportable as standard formats (SQLite, JSON, CSV, original-format binaries, Markdown) without running the application, as a first-class architectural feature rather than a compliance afterthought.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- Export pipeline runs from local data without network connectivity
- Export emits relational data as SQLite, structured records as JSON, tabular data as CSV, binary assets in original format, and long-form text as Markdown
- Export pipeline is exposed by `Sunfish.Foundation` as a background task with a destination-path contract
- No host-application UI is prescribed by the export pipeline

**Verification:** Run export with network disconnected; resulting directory opens in third-party tools (SQLite client, text editor, spreadsheet) without application software.

#### `ch16-persistence-beyond-the-node:DUR-26` — Export determinism and completeness guarantees

The export process emits no telemetry, requires no network, produces deterministic output (identical state yields identical export), and includes every record the local node holds — full records as content, stubs as metadata-plus-hash.

**Kleppmann:** `P5, P7` · **Scope:** `foundational`

**Must implement:**

- Export emits zero network requests during execution
- Identical local state produces byte-identical export directory contents (modulo timestamps in UTC ISO 8601 filenames)
- Stubs are exported as metadata plus content hash with content field absent and a documented note
- No record present in the local database is omitted from export

**Verification:** Run export twice over identical state; diff confirms identical contents. Capture network traffic during export; confirm zero outbound requests.

#### `ch16-persistence-beyond-the-node:DUR-27` — Versioned export manifest

A machine-readable `manifest.json` at the export root records format version, export timestamp, node identifier, included document types, and the count of stubs versus full records, enabling future readers to determine compatibility before parsing data files.

**Kleppmann:** `P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Every export directory contains a `manifest.json` at root and a plain-language `README.txt`
- Manifest records format version, timestamp, node identifier, included document types, and stub-vs-full counts
- Export format version is versioned independently of the application version

**Verification:** Inspect any export directory; `manifest.json` parses with the documented schema and reports a format version.

#### `ch16-persistence-beyond-the-node:DUR-28` — Markdown as long-now format

Markdown is included as an export format for long-form document content because it is simultaneously human-readable in any text editor, machine-parseable by any competent library, and version-control friendly without specialized tooling.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `vendor-outage`

**Must implement:**

- Long-form document content (notes, descriptions, inline text) is exported as Markdown
- Markdown export does not require application-specific tooling to read or parse

**Verification:** Open any Markdown export file in a plain text editor; content is human-readable without rendering.

#### `ch16-persistence-beyond-the-node:DUR-29` — Layer 5 decentralized archival as deferred extension point

Layer 5 is an optional enterprise tier providing cryptographic proof-of-storage for regulated long-term retention; the operational mechanism (Filecoin, Arweave, Merkle-challenge) is deferred to v2.0 and current deployments satisfy retention obligations through Tier 3 BYOC backup with retention policies.

**Kleppmann:** `P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Architecture documents Layer 5 as a Phase 2 extension point with no 1.0 specification
- 1.0 deployments satisfy retention obligations via Tier 3 BYOC with long-term retention policies
- Layer 5 absence is documented as expected, not as a gap

**Verification:** Specification document marks Layer 5 as deferred to v2.0 and references Tier 3 retention as the 1.0 satisfier.


---

## Part IV — Implementation playbooks

### Epic: Building Your First Node (ch17-building-first-node)

**Source-paper refs:** v13 §5, v13 §13, v13 §18

**Concept count:** 23

#### `ch17-building-first-node:BUILD-01` — Minimum-viable node deliverable checklist

A first-node implementation is complete only when every item on a fixed eight-point checklist (build runs, keypair generated, founder bundle generated, joiner bundle verified, NodeHealth Healthy, document persists across restart, two-instance LAN discovery, status bar visible) passes.

**Kleppmann:** `P1, P2, P3, P4` · **Scope:** `inverted-stack-specific`

**Must implement:**

- First launch builds and runs without error on the chosen target framework
- First launch generates and persists a device keypair
- Founder bundle generates and base64-encodes
- Joiner bundle decodes and verifies a founder signature
- NodeHealth transitions to Healthy after OnboardAsync completes
- A CRDT document creates, updates, and persists across application restart
- Two instances on the same LAN discover each other via mDNS
- The status bar surfaces all three operational indicators

**Verification:** Run the eight-item checklist on a freshly-cloned build; every item passes before the chapter is considered complete.

#### `ch17-building-first-node:BUILD-02` — Accelerator-shell-vs-domain-code split

The reference accelerator delivers the security and sync infrastructure as wired primitives while the application domain (report catalog, document views, sync UI, packaging, auto-update) is left to the implementer to build on top.

**Kleppmann:** `P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Reference shell wires kernel, encrypted store, security, and sync without requiring domain code
- Reference shell ships no opinionated domain model
- Domain features are added as plugins on top of the shell, not by modifying the shell

**Verification:** Inspect a freshly-cloned accelerator — kernel security and sync are functional, no business-domain types are present in the shell project.

#### `ch17-building-first-node:BUILD-03` — Three-call kernel composition root

The local-first kernel is wired in the application composition root with three ordered DI calls — encrypted store first, runtime second, security third — because each layer depends on the layer registered before it.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Composition root registers the encrypted store before the kernel runtime
- Composition root registers the kernel runtime before the security layer
- Each subsystem (sync, CRDT engine, schema registry, local-first store) is registered by its own extension method called explicitly in the composition root
- Registration uses TryAdd-style semantics so test harnesses can swap any subsystem by registering ahead of the default

**Verification:** Composition root contains the three named registrations in the prescribed order; reordering causes a deterministic startup failure in the test suite.

#### `ch17-building-first-node:BUILD-04` — Deterministic kernel startup sequence

After DI registration, the node startup sequence runs in a fixed order — open encrypted database, initialize runtime (sync daemon, mDNS, CRDT engine), load or generate device keypair, evaluate onboarding state, render shell — and the UI shell branch is determined by the persisted onboarding state.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Encrypted database opens before the runtime initializes
- Device keypair is loaded or generated before the UI shell renders
- Onboarding state is evaluated before the UI shell selects a route
- UI shell renders the onboarding surface when not onboarded and the workspace when onboarded

**Verification:** Trace startup logs of a fresh install and an onboarded install; ordering and shell-branch selection match the documented sequence.

#### `ch17-building-first-node:BUILD-05` — Onboarding-gated workspace access

The kernel refuses to render or operate the main workspace until a valid attestation has been applied, so the UI cannot present application surface that the security layer has not authorized.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Workspace routes are unreachable while the session reports not-onboarded
- The kernel — not the UI — is the authority that gates workspace access
- UI shell selection reflects the kernel-reported onboarding state

**Verification:** Attempt to navigate to a workspace route on a not-onboarded node; navigation is refused at the kernel layer rather than only at the route guard.

#### `ch17-building-first-node:BUILD-06` — First-document development loop

The canonical first-feature loop is to obtain the CRDT engine from DI, create a document by ID, apply a typed update, and subscribe to update events that distinguish local from remote origin.

**Kleppmann:** `P1, P3, P4` · **Scope:** `foundational`

**Must implement:**

- CRDT engine is obtained via the application's DI container
- Document creation and open are addressable by stable string ID
- Local updates are applied through a typed update API
- Update subscription distinguishes local-origin from remote-origin events

**Verification:** A worked example in the accelerator's tests creates a document, applies an update, and asserts the subscriber receives the change with the correct origin tag.

#### `ch17-building-first-node:BUILD-07` — Engine-owned persistence (no explicit save)

The CRDT engine persists every applied update automatically into the encrypted store, so application code never issues a save call and a reopened document returns with all prior updates intact.

**Kleppmann:** `P1, P3, P5` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Application code contains no explicit document save or flush call
- Document state survives application restart with byte-identical replay
- Persistence latency is bounded such that a crash after Apply returns does not lose the update

**Verification:** Apply an update, kill the process before any user-initiated save, restart, and confirm the update is present.

#### `ch17-building-first-node:BUILD-08` — Zero-config two-instance LAN sync

Two instances of the node started on the same LAN discover each other via mDNS within seconds and complete a peer handshake without any configured IP address, port, or peer list.

**Kleppmann:** `P3, P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `peer-discovery-failure`

**Must implement:**

- Second instance is started with only a distinct data directory, no peer configuration
- mDNS service record is advertised on runtime start
- Link status transitions from offline to healthy when the peer handshake completes
- Once linked, an update applied on one instance is delivered to the other via gossip anti-entropy

**Verification:** Run two instances with separate data directories on one LAN; confirm link status reaches healthy and a one-side update is observable on the other side without explicit peer configuration.

#### `ch17-building-first-node:BUILD-09` — Per-instance data directory isolation for multi-run

Multiple instances on a single machine require explicit per-instance data directory paths so that each instance owns a distinct encrypted store and a distinct mDNS service record.

**Scope:** `inverted-stack-specific` · **Failure modes:** `peer-discovery-failure`

**Must implement:**

- Runtime accepts a per-launch data directory override flag
- Two instances launched with the same data directory are detected and the second refuses to start
- Each data directory contains a distinct device keypair

**Verification:** Launch two instances with the same data directory and observe a deterministic startup refusal; launch them with distinct directories and observe both running concurrently.

#### `ch17-building-first-node:BUILD-10` — Implementation-status disclosure obligation

When a documented subsystem ships ahead of its specification, the chapter and the running build must explicitly disclose the gap — naming the stub component, what guarantees do not yet hold, and which roadmap milestone closes the gap.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Stub or placeholder components carry a runtime marker identifying them as not-production-ready
- Documentation names the production target and the roadmap milestone that completes it
- Tutorial text states which guarantees are exercised today and which are specification-ahead-of-implementation

**Verification:** Inventory of accelerator components labels each as production, beta, or stub; documentation cross-references the corresponding specification chapter and roadmap entry.

#### `ch17-building-first-node:BUILD-11` — Length-prefixed dual-section onboarding payload

Every onboarding payload is a length-prefixed binary envelope containing exactly two sections — a CBOR-encoded attestation bundle and a raw CRDT snapshot — each preceded by a little-endian uint32 byte length.

**Kleppmann:** `P2, P4` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Payload begins with a 4-byte little-endian uint32 specifying CBOR bundle length
- CBOR-encoded attestation bundle follows, containing attestation records for team members
- A second 4-byte little-endian uint32 specifies snapshot length
- Raw snapshot bytes follow
- Decoder reads sections by length prefix without any inline delimiters

**Verification:** Round-trip encode and decode an onboarding payload; assert the byte layout matches the four-field specification exactly.

#### `ch17-building-first-node:BUILD-12` — Founder bundle as self-signed trust root

A founder bundle is self-signed (issuer and subject are the same device key) and embeds the founder's Ed25519 public key, establishing the trust root for the team without any external certificate authority.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `vendor-acquisition`

**Must implement:**

- Founder generation produces a bundle where issuer equals subject
- The bundle embeds the founder device's Ed25519 public key as IssuerPublicKey
- Joiner verification checks signature against the embedded public key
- No external CA or third-party issuer is consulted

**Verification:** Generate a founder bundle and inspect it — issuer equals subject, IssuerPublicKey is present, verification succeeds against the embedded key alone.

#### `ch17-building-first-node:BUILD-13` — Founder-issued joiner attestation with embedded subject key

A joiner bundle is signed by the founder's Ed25519 private key, embeds the joining device's public key as the subject, and is verified against the founder's public key at decode time before any state is mutated.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise, replay`

**Must implement:**

- Joiner bundle issuance requires the founder's Ed25519 private key
- The joining device's public key is embedded as SubjectPublicKey
- Decoder verifies the signature before invoking onboarding state changes
- A failed signature verification aborts onboarding and surfaces a typed exception

**Verification:** Tamper one byte of a joiner bundle; decode aborts with a signature-mismatch typed exception and the node remains not-onboarded.

#### `ch17-building-first-node:BUILD-14` — Side-channel-agnostic bundle transport

Onboarding payload transport is independent of the bundle's security guarantees because trust derives from signature verification rather than channel confidentiality, so paste, QR scan, and deep link are interchangeable transports.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Reference transport is paste (base64 string into a UI field)
- Camera-based QR scanning and deep-link activation are supported alternatives
- Security guarantees do not change with transport choice
- An intercepted bundle without the founder private key cannot be used to onboard a fraudulent device

**Verification:** Repeat the onboarding flow with paste, QR scan, and deep link transports; the cryptographic verification path is identical in all three cases.

#### `ch17-building-first-node:BUILD-15` — Typed onboarding decode errors surfaced to UI

The onboarding decoder throws a distinct typed exception per failure mode (malformed length prefix, CBOR parse error, signature mismatch) so the UI can render a specific actionable error rather than a generic failure message.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Decoder distinguishes length-prefix errors, CBOR parse errors, and signature errors as separate exception types
- UI catches each type and renders a per-type user-facing message
- No code path collapses these into a generic "invalid bundle" error

**Verification:** Inject one of each failure into the decoder; assert each surfaces a distinct typed exception and a distinct UI message.

#### `ch17-building-first-node:BUILD-16` — Always-visible three-indicator status bar

A local-first node renders a permanently-visible status bar with three indicators — Node Health, Link Status, and Data Freshness — so the user can always perceive how the node's behavior depends on its current network and sync state.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition, peer-discovery-failure`

**Must implement:**

- Status bar is rendered on every screen, never hidden behind a settings panel
- Status bar shows Node Health, Link Status, and Data Freshness as three distinct indicators
- Each indicator has named states with documented meanings
- Indicators are distinguishable to users with vision impairment (label-or-icon contract)

**Verification:** Walk every UI route in the application; the status bar is present on each one with all three indicators rendered.

#### `ch17-building-first-node:BUILD-17` — Configurable data-freshness threshold as product decision

The staleness threshold that flips Data Freshness from healthy to stale is a configurable product decision (default five minutes) chosen per application context — short for high-frequency collaborative writing, long for intermittent-connectivity field deployments — and fixed before the first user-facing release.

**Kleppmann:** `P3` · **Scope:** `foundational`

**Must implement:**

- Staleness threshold is configurable per deployment
- A default value is shipped (five minutes is the reference default)
- Threshold is fixed before initial release and changes after release require explicit user-facing communication

**Verification:** Configuration surface exposes the threshold; an integration test asserts the indicator transitions to stale at the configured boundary.

#### `ch17-building-first-node:BUILD-18` — Three-state optimistic write button

Every write surface in a local-first application reflects three local-write states — pending (in-flight to local store), confirmed (durable on local device), failed (local-store error only) — without conflating sync delay with write failure.

**Kleppmann:** `P1, P3` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- UI distinguishes pending, confirmed, and failed states for every write surface
- Confirmed state fires on local-store completion, not on peer acknowledgment
- Failed state appears only on local-store errors, never on sync delays
- Sync-delay signal is carried by the Data Freshness indicator, not by the write button

**Verification:** Disconnect network and submit a write; the button reaches confirmed and the Data Freshness indicator transitions to stale, but the write does not enter the failed state.

#### `ch17-building-first-node:BUILD-19` — Plugin contract as platform stability boundary

Domain features attach to the node only through the plugin extension-point contract, which is the stability boundary between the platform and the application; pre-1.0 kernel services beneath the contract may change without notice.

**Kleppmann:** `P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- All domain features are implemented as plugins, not as direct kernel-service consumers
- Application code does not call kernel services that are not part of the plugin extension-point surface
- The plugin contract is versioned independently of internal kernel APIs

**Verification:** Static analysis confirms application code references only the documented extension-point types; references to internal kernel services from application code raise a build warning.

#### `ch17-building-first-node:BUILD-20` — Five-extension-point plugin surface

The complete plugin surface for a domain feature consists of exactly five extension points — ILocalNodePlugin (lifecycle), IStreamDefinition (CRDT streams and sync buckets), IProjectionBuilder (read-model projections), ISchemaVersion (schema versions and upcasters), and IUiBlockManifest (UI blocks).

**Kleppmann:** `P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Plugin lifecycle is implemented via ILocalNodePlugin
- CRDT streams and sync bucket contributions are declared via IStreamDefinition
- Read-model projections register via IProjectionBuilder with idempotent rebuild
- Schema versions and upcasters declare via ISchemaVersion
- Plugin-specific Blazor or UI components register via IUiBlockManifest

**Verification:** A plugin that uses all five extension points loads cleanly; omitting one of the five does not break the others (each is independently optional except ILocalNodePlugin).

#### `ch17-building-first-node:BUILD-21` — Reverse-DNS plugin identifier with semver version

Each plugin declares a reverse-DNS-style Id (used by the dependency resolver) and a semantic-version Version (logged at load time for diagnostics) so that startup logs uniquely identify the running plugin build.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Plugin Id follows reverse-DNS convention
- Plugin Version follows semantic versioning
- Both are logged at load time
- Dependencies of one plugin reference other plugins by reverse-DNS Id

**Verification:** Inspect a node's startup logs; every loaded plugin is identified by reverse-DNS Id and a semver string.

#### `ch17-building-first-node:BUILD-22` — Single-team-per-install v1 scope decision

The first-shipped node supports exactly one team per installation by design, with the multi-team workspace-switcher model deferred to v2 because the v2 migration path is additive (per-team HKDF subkeys, per-workspace state isolation) rather than a rewrite.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- First-version installation supports a single team
- Persistence layout is structured so that adding per-team isolation does not require migrating existing single-team data
- Documentation states the v2 migration is additive

**Verification:** Install the node; only one team can be onboarded; attempting a second team-onboard returns a deterministic refusal with a v2 forward-reference message.

#### `ch17-building-first-node:BUILD-23` — Recursive declare-project-add-extend feature loop

The development loop for every new domain feature is the same five-step cycle — declare the IStreamDefinition, build the IProjectionBuilder, add the UI surface, run two instances on LAN to validate sync, then implement the next feature as another ILocalNodePlugin returning to step one.

**Kleppmann:** `P1, P3, P4, P5` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Each new feature begins with an IStreamDefinition declaration
- Each new feature builds at least one IProjectionBuilder for its read model
- Each new feature is integration-tested by running two instances on LAN
- Subsequent features are added as additional ILocalNodePlugin implementations, not by modifying earlier plugins

**Verification:** A second domain feature is added by following the loop without modifying any file owned by the first feature; both features sync correctly when two instances are run on LAN.


### Epic: Migrating an Existing SaaS (ch18-migrating-existing-saas)

**Source-paper refs:** v5 §8

**Concept count:** 24

#### `ch18-migrating-existing-saas:MIG-01` — Reversible four-phase migration model

A SaaS-to-local-first migration runs in four sequential phases where every gate below the final phase is reversible without data loss, replacing rewrite-everything cutover with phase-bounded engineering investment.

**Kleppmann:** `P5, P7` · **Scope:** `foundational`

**Must implement:**

- Migration plan declares four named phases with explicit entry and exit criteria
- Phases 1 through 3 are demonstrably reversible by reverting configuration alone, no data migration required
- Phase 4 is bounded to one workspace at a time and never run fleet-wide
- Each phase delivers user-visible value independently so the team may pause indefinitely between phases

**Verification:** Migration runbook exists naming the four phases with per-phase rollback procedure; rollback procedures for Phases 1 through 3 are exercised in a staging environment without invoking a data migration job.

#### `ch18-migrating-existing-saas:MIG-02` — Five migration triggers

A team justifies migrating a hosted SaaS to local-first only when at least one of five named business triggers applies — compliance mandate, data-residency objection in enterprise sales, vendor reliability or termination event, churn driven by data sovereignty, or procurement review blocking adoption.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, vendor-acquisition, vendor-outage`

**Must implement:**

- Migration proposal cites at least one of the five named triggers with concrete evidence from customer or regulator interactions
- Aesthetic, fashion, or curiosity-driven justifications are explicitly rejected as insufficient

**Verification:** Migration kickoff document names the triggering condition with linked customer or regulatory evidence, reviewed by a non-engineering stakeholder before engineering investment begins.

#### `ch18-migrating-existing-saas:MIG-03` — Five-filter eligibility framework applied per record class

Migration eligibility is determined by running each record class through five filters covering ownership, staleness tolerance, conflict resolvability, offline value, and compliance posture, with the result selecting Zone B, Zone C, or no migration at all.

**Kleppmann:** `P3, P5, P6, P7` · **Scope:** `foundational`

**Must implement:**

- Every record class in the existing schema is classified against all five filters
- Filter results are recorded per record class, not aggregated to a product-level verdict
- Records failing Filter 1 or Filter 2 are routed to Zone B and excluded from local-first migration scope
- Records passing all five filters are eligible for AP-class CRDT treatment

**Verification:** A filter-result table exists with one row per record class and five filter columns, archived in the migration plan.

#### `ch18-migrating-existing-saas:MIG-04` — AP-class versus CP-class record separation

Records are classified as AP-class — user-owned, eventually consistent, suitable for CRDT replication — or CP-class — server-coordinated, requiring linearizable writes — and the two classes never share a backing table.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Each table or aggregate is labeled AP-class or CP-class in the schema documentation
- AP-class data resides on CRDT documents on local nodes
- CP-class data resides on the server-authoritative store with lease coordination
- No table mixes AP-class and CP-class fields, regardless of join convenience
- Table names encode the classification (e.g., ProjectBody for AP, ProjectBillingRecord for CP)

**Verification:** Schema audit script enumerates tables and asserts each is labeled AP or CP; CI rejects schema changes that introduce mixed-class tables.

#### `ch18-migrating-existing-saas:MIG-05` — Three-plane Bridge separation

The Zone C hybrid architecture separates concerns into three logical planes — a shared control plane for signup and billing, a per-tenant data plane holding workspace data, and a shared stateless relay tier transporting encrypted deltas — with no team data permitted in the control or relay tiers.

**Kleppmann:** `P5, P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection`

**Must implement:**

- Control plane holds only tenant registry records of shape {tenant_id, plan, billing, support_contacts, team_public_key}
- Data plane runs one local-node-host process and one SQLCipher database per tenant at a per-tenant path
- Each tenant receives a dedicated subdomain
- Relay tier persists no tenant content and operates as a horizontally scaled message bus only
- Any content record discovered in the control plane triggers a stop-and-investigate response

**Verification:** Bridge audit tooling enumerates control-plane tables and confirms only the registry shape; relay process inspection shows no persistent storage attached for content.

#### `ch18-migrating-existing-saas:MIG-06` — Hosted-node peer as ciphertext-only participant

The server-side hosted-node peer participates in sync as a ciphertext-only peer that holds encrypted deltas for catch-up-on-reconnect but cannot decrypt without a team-issued role attestation.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise, vendor-outage`

**Must implement:**

- Hosted-node peer holds no decryption keys for tenant data by default
- Decryption capability requires explicit team-issued role attestation
- Catch-up-on-reconnect proceeds against ciphertext deltas
- Bridge audit tooling verifies the ciphertext-only invariant before each release

**Verification:** Bridge audit job inspects the hosted-node process key store and confirms absence of plaintext keys for any tenant; integration test attempts decryption without attestation and observes failure.

#### `ch18-migrating-existing-saas:MIG-07` — Three Bridge tenant trust levels

Bridge supports three tenant trust levels — relay-only as the default with no operator plaintext access, attested hosted peer as opt-in for backup verification and admin-assisted recovery, and self-hosted nodes that use Bridge only for the control plane.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Default tenant configuration is relay-only with no operator plaintext capability
- Attested hosted peer mode requires explicit tenant-admin role attestation issuance
- Self-hosted-node tenants may consume only the control plane
- Trust level is selectable per tenant at provisioning time

**Verification:** Tenant provisioning workflow exposes the three trust levels as named options; per-tenant audit query returns the active trust level.

#### `ch18-migrating-existing-saas:MIG-08` — Per-tenant data isolation as first decision

Migration begins by separating a shared-schema multi-tenant database into per-tenant data planes, wired through a single tenant-context interface that becomes the migration seam between the prior projection and a CRDT-backed projection.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection`

**Must implement:**

- Every database query routes through ITenantContext from Sunfish.Foundation
- Per-tenant database paths are isolated, not separated by filter columns alone
- The decision is made and executed before any local-first work begins
- Backup and index jobs are tenant-scoped

**Verification:** Static analysis confirms no query bypasses ITenantContext; schema inspection shows per-tenant database paths rather than a shared schema with tenant-ID columns.

#### `ch18-migrating-existing-saas:MIG-09` — Append-only event tables as migration seam

Domain state is stored as append-only event rows for mutable aggregates rather than last-write-wins field mutations, providing a mechanical replay path from server events to equivalent CRDT operations.

**Kleppmann:** `P5` · **Scope:** `foundational`

**Must implement:**

- Mutable aggregates are stored as append-only event tables not nullable-column tables
- Each event row carries enough information to replay as a CRDT operation
- New mutable field columns are rejected in code review on the migration path

**Verification:** Schema review identifies aggregate tables and confirms append-only event-row structure; replay job transforms event rows into CRDT operations and asserts projection equivalence.

#### `ch18-migrating-existing-saas:MIG-10` — Block-contract UI wiring

UI components consume block contracts whose data shape is identical whether backed by a server-side projection or a CRDT-backed local document, so the storage layer can swap underneath without UI rewrites.

**Kleppmann:** `P1` · **Scope:** `inverted-stack-specific`

**Must implement:**

- UI components depend on Sunfish.Blocks.* contracts not on ORM models or DTOs
- Block contract shape is identical across Postgres-backed and CRDT-backed implementations
- No migration phase requires a UI rewrite to change the backing store

**Verification:** Component-level dependency scan confirms UI imports reference block contracts only; integration test swaps the backing store for a single block and observes no UI code change.

#### `ch18-migrating-existing-saas:MIG-11` — Business logic out of stored procedures

Validation, computation, and workflow logic moves from database stored procedures to application-layer domain services so it can replicate to local nodes that execute in the application process.

**Kleppmann:** `P3` · **Scope:** `foundational`

**Must implement:**

- Stored procedures contain only set-based data operations
- Validation, computation, and workflow logic resides in application-layer domain services
- The audit and extraction occur during pre-migration decision work, not during Phase 3 provisioning

**Verification:** Audit script enumerates stored procedures and classifies each as set-operation-only or violation; violations are zero before Phase 3 begins.

#### `ch18-migrating-existing-saas:MIG-12` — Phase 1 shadow mode with feature-flag rollback

A local node is deployed alongside the existing SaaS, mirroring data read-only and serving UI reads while writes still flow through the server API, with a standard feature flag providing instant deployment-free rollback.

**Kleppmann:** `P1` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Local node populates from the existing read model and serves UI reads
- All writes continue through the server API unchanged in this phase
- A feature flag (convention LocalFirst.ShadowMode) gates the read switch and is consulted by Sunfish.Foundation.LocalFirst at startup
- Flag evaluates through the team's existing flag provider (IFeatureManager or equivalent), not a Sunfish-proprietary system
- Rollback is achieved by flipping the flag with no deployment required

**Verification:** Production toggle of the flag from on to off restores server-API reads within one configuration-refresh interval and without redeploying the application.

#### `ch18-migrating-existing-saas:MIG-13` — Phase 1 read-latency and consistency success criteria

Phase 1 is judged successful only when P95 read latency drops by at least 20% with no write-consistency regression and the local replica stays within the declared AP staleness window.

**Kleppmann:** `P1` · **Scope:** `foundational`

**Must implement:**

- P95 read latency is measured before and after Phase 1 deployment
- Write-consistency tests run unchanged against the server-API write path during Phase 1
- Replica staleness is monitored against a declared baseline (30 seconds for typical task-management domains)
- Failure on any criterion blocks the Phase 1 to Phase 2 transition

**Verification:** Phase 1 exit report includes the three measurements with pre- and post-deployment values; CAB sign-off references the report.

#### `ch18-migrating-existing-saas:MIG-14` — Phase 2 local writes for AP-class only

Phase 2 routes AP-class block writes through the CRDT engine for instant local feedback while CP-class records — billing, subscription limits, role membership, audit logs — remain server-authoritative.

**Kleppmann:** `P1, P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- AP-class writes apply locally without a server round-trip
- CRDT merge resolves concurrent edits on AP-class records without data loss
- CP-class write paths are unmodified and pass existing integration tests unchanged
- Server transitions to a relay role for AP-class deltas, propagating but not owning them
- The eligibility test for AP classification is whether two-user concurrent edits with merge yield an acceptable result

**Verification:** Convergence test against AP-class aggregates demonstrates byte-identical state after concurrent edits; CP-class regression suite passes unchanged.

#### `ch18-migrating-existing-saas:MIG-15` — Phase 2 reversibility via CRDT log preservation

Phase 2 is reversible per domain by disabling CRDT writes, returning authority to the server API while preserving the CRDT event log so local authority can be re-enabled later by replay.

**Kleppmann:** `P5, P7` · **Scope:** `foundational`

**Must implement:**

- CRDT writes can be disabled per domain via configuration
- The CRDT event log is preserved on rollback, not deleted
- A re-enable path exists that replays the preserved log
- Pausing indefinitely at Phase 2 is treated as a respectable terminal state

**Verification:** Per-domain rollback procedure is exercised on a staging tenant; re-enable replay produces the expected projection without loss.

#### `ch18-migrating-existing-saas:MIG-16` — Phase 3 full local authority for new workspaces

Newly provisioned workspaces start with the full local-node stack — gossip sync daemon, per-workspace SQLCipher database, device keypair issuance, role attestations — while existing workspaces remain at Phase 2 until opting into Phase 4.

**Kleppmann:** `P1, P2, P3, P4, P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition, vendor-outage`

**Must implement:**

- New-workspace provisioning provisions Sunfish.Kernel.Sync and Sunfish.Kernel.Security
- Device keypairs are issued at first launch
- Role attestations govern hosted-node peer access
- Gossip anti-entropy converges within the configured interval (30-second default) under the test topology
- New workspaces operate at full fidelity without server connectivity
- Phase 3 workspaces and Phase 2 workspaces coexist on the same infrastructure

**Verification:** New-workspace integration test runs offline end-to-end and confirms full feature fidelity; topology test measures convergence within the configured gossip interval.

#### `ch18-migrating-existing-saas:MIG-17` — BYOC backup mandatory at Phase 3 provisioning

New workspaces configure Bring-Your-Own-Cloud backup at provisioning time because the hosted-node peer is a relay cache that evicts and does not guarantee retention.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-loss`

**Must implement:**

- Workspace provisioning workflow makes BYOC backup the default the team must override, not an option the team must remember
- Provisioning records the configured backup destination
- The hosted-node peer is documented as cache-not-backup in tenant onboarding

**Verification:** Provisioning UI test confirms BYOC configuration is required by default; tenant audit query returns the backup destination per workspace.

#### `ch18-migrating-existing-saas:MIG-18` — Phase 4 copy-transform-validate with projection diff

Phase 4 migrates an existing workspace by reading its server-side domain events, transforming each into a CRDT operation, projecting both stores, and asserting projection equivalence under a declared comparison contract before switching the write path.

**Kleppmann:** `P5` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Migration job reads domain events from the existing event store
- Each event is transformed into an equivalent CRDT operation by a per-aggregate transformer
- Postgres projection and CRDT projection are compared under a declared equivalence contract covering field equality, collection membership, and type coercions
- The diff fails fast on first divergence with a logged diff object
- The write path switch occurs only after a clean diff
- Diff failures hold the workspace at Phase 2 pending transformer correction
- The migration job is idempotent and may be rerun until the diff is empty

**Verification:** A pilot workspace migration produces a clean projection diff and the diff report is archived; chaos test injects a transformer bug and confirms fail-fast hold at Phase 2.

#### `ch18-migrating-existing-saas:MIG-19` — Phase 4 per-workspace one-way door with 30-day stabilization

Phase 4 is opt-in per workspace, runs incrementally one workspace at a time, holds each migrated workspace for 30 days on Phase 3 before treating the migration as stable, and is not reversible without re-running the copy-transform in reverse.

**Kleppmann:** `P5, P7` · **Scope:** `foundational`

**Must implement:**

- Phase 4 is never run fleet-wide in a single batch
- A pilot workspace runs first and is observed for 30 days before any expansion
- The Postgres write path stays disabled for the 30-day stabilization without rollback requests
- Re-migration from Phase 4 back to Phase 2 is documented as expensive and error-prone, requiring inverse copy-transform
- The CRDT event log becomes the system of record after the 30-day window

**Verification:** Migration runbook documents the per-workspace cadence and the 30-day hold; rollout dashboard tracks per-workspace days-since-cutover.

#### `ch18-migrating-existing-saas:MIG-20` — Phase transition gates with hard stops

Each phase transition is governed by an explicit gate question with a named hard-stop condition — CP-class write regression blocks Phase 1 to 2, merge data loss blocks Phase 2 to 3, projection-diff failure blocks fleet rollout from Phase 3 to 4.

**Kleppmann:** `P5` · **Scope:** `foundational`

**Must implement:**

- A change-advisory-board decision is required at each transition, not a calendar event
- Each transition documents the gate question and the named hard stop
- Hard-stop conditions block the transition unconditionally when triggered

**Verification:** CAB record exists per transition with the gate question, evidence, and decision; hard-stop simulation in staging confirms the transition is blocked.

#### `ch18-migrating-existing-saas:MIG-21` — Failure mode — server-side feature gates re-centralizing the architecture

A drift pattern in which feature flag evaluation, analytics, A/B testing, or rate limiting routes AP-class decisions through server calls, gradually re-centralizing the architecture under the appearance of harmless individual additions.

**Kleppmann:** `P3, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Feature flags evaluate locally against node role attestations from Phase 1 onward
- No AP-class decision routes through a server call
- Sunfish.Foundation.FeatureManagement (or equivalent local evaluator) is wired before any server-evaluated flag patterns are introduced
- Code review rejects new server-call patterns on AP-class write paths

**Verification:** Static analysis enumerates server-call sites on AP-class write paths and asserts the count is zero; periodic architecture audit confirms feature-flag evaluation remains local.

#### `ch18-migrating-existing-saas:MIG-22` — Failure mode — relay mistaken for backup

An operational failure mode in which teams skip BYOC backup configuration on the assumption that the hosted-node peer holds their data durably, then discover during a device-loss incident that the relay is a cache that evicts rather than a guaranteed-retention store.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-loss, vendor-outage`

**Must implement:**

- The relay tier is documented as cache-not-backup in operator and tenant materials
- BYOC backup configuration is non-optional and default-on at workspace provisioning
- Recovery drills exercise the BYOC restore path, not the relay catch-up path

**Verification:** Tenant onboarding documents declare the relay-as-cache contract; recovery drill is run and restores from the BYOC destination.

#### `ch18-migrating-existing-saas:MIG-23` — Per-phase Sunfish package availability matrix

Each Sunfish package becomes appropriate at a specific migration phase and reaching for a package before its phase is an architectural anti-pattern, with Sunfish.Foundation.FeatureManagement wired first and kernel packages introduced only as their phase arrives.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Sunfish.Foundation, UICore, UIAdapters.Blazor, and Blocks are available from Phase 1
- Sunfish.Foundation.LocalFirst progresses from shadow-read-only (Phase 1) to shadow-plus-local-writes (Phase 2) to full (Phases 3 and 4)
- Sunfish.Kernel.Crdt is introduced only at Phase 2 and only for AP domains
- Sunfish.Kernel.Sync and Sunfish.Kernel.Security are introduced only at Phase 3
- Sunfish.Foundation.FeatureManagement is wired in Phase 1 before any flag-evaluation pattern emerges

**Verification:** Build inspection per phase confirms package set matches the matrix; CI rule rejects pull requests that introduce kernel packages before their declared phase.

#### `ch18-migrating-existing-saas:MIG-24` — Greenfield Zone C bypasses migration path

A greenfield product whose five-filter framework returns Zone C clones the Bridge accelerator directly rather than running the migration phases, because the control plane, relay tier, per-tenant data plane, and ciphertext-only hosted peer ship pre-separated.

**Kleppmann:** `P5, P6, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Greenfield Zone C teams clone accelerators/bridge/ as the starting point
- The migration phases are not run when no production data and no existing tenants exist
- Greenfield work is scoped as product configuration not architecture construction

**Verification:** Greenfield project bootstrap script clones the Bridge accelerator and the resulting plane separation matches the Bridge audit baseline.


### Epic: Shipping to Enterprise (ch19-shipping-to-enterprise)

**Source-paper refs:** v13 §16, v5 §5

**Concept count:** 23

#### `ch19-shipping-to-enterprise:ENT-01` — Dual-license structure with commercial exception

The open-source core ships under AGPLv3 by default with a parallel commercial license offered to organizations that cannot accept the network-use clause.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `vendor-acquisition`

**Must implement:**

- Repository contains a LICENSES/ directory holding both the AGPLv3 text and a commercial license template
- The commercial license grants internal-modification rights, warranty, and a security-patch SLA
- Dual-license offer is discoverable from the repository without a sales conversation

**Verification:** Repository inspection finds both license texts under LICENSES/ and a top-level NOTICE or README pointer to the commercial exception

#### `ch19-shipping-to-enterprise:ENT-02` — Contributor License Agreement precondition

An inbound-equals-outbound CLA is in place before any external contribution is accepted, preserving the legal authority to offer the commercial license exception.

**Kleppmann:** `P5, P7` · **Scope:** `foundational`

**Must implement:**

- A CLA is signed by every external contributor before merging any contributed code
- The CLA grants inbound rights sufficient to relicense under the commercial exception
- CI blocks pull requests from contributors lacking a recorded CLA signature

**Verification:** Repository CI configuration enforces a CLA-check status before merge; a signed CLA record exists for every author in git history

#### `ch19-shipping-to-enterprise:ENT-03` — Managed-endpoint packaging contract

The product ships as a signed MSIX/MSI on Windows and a signed and notarized .pkg or .dmg on macOS, with no archive-and-script delivery path offered to enterprise customers.

**Scope:** `inverted-stack-specific`

**Must implement:**

- CI produces a signed MSI or MSIX for Windows on every release
- CI produces a signed and notarized .pkg or .dmg for macOS on every release
- Installers register the sync daemon as a Windows Service and a launchd LaunchDaemon respectively
- Installers run silently with no user prompts

**Verification:** Release artifacts include both Windows and macOS installers; silent install completes without UI on a clean managed-endpoint test image

#### `ch19-shipping-to-enterprise:ENT-04` — System-context daemon registration

The sync daemon is installed at system scope — Windows Service or /Library/LaunchDaemons launch agent — so it starts before user login and runs under MDM supervision rather than as a user-context process.

**Kleppmann:** `P3` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Windows installer declares the sync daemon via a service-install element
- macOS installer places the launch plist under /Library/LaunchDaemons rather than ~/Library/LaunchAgents
- The daemon process survives user logoff and restarts on failure under OS supervision

**Verification:** Post-install inspection on each platform confirms the daemon is registered at system scope and is restarted by the OS service manager after a forced kill

#### `ch19-shipping-to-enterprise:ENT-05` — macOS Developer ID signing and Apple notarization

Every shipped macOS binary is signed with a Developer ID certificate under the hardened runtime and submitted to Apple notarization, with the notarization ticket stapled into the distributable package.

**Scope:** `foundational`

**Must implement:**

- codesign is invoked with --options runtime on every binary in the bundle
- Both the foreground app and the sync daemon are independently signed
- notarytool submission completes successfully before release
- The notarization ticket is stapled into the .pkg or .dmg before publication

**Verification:** spctl --assess --type execute on the published artifact returns accepted with notarized status on a clean macOS endpoint

#### `ch19-shipping-to-enterprise:ENT-06` — Windows Authenticode signing for App Control

Every Windows executable and DLL is Authenticode-signed with an organization-owned certificate chained to a trusted commercial CA so that App Control for Business publisher-trust rules cover the product.

**Scope:** `foundational`

**Must implement:**

- signtool signs every .exe and .dll with sha256 digest and an RFC 3161 timestamp
- The signing certificate chains to a recognized commercial CA (not self-signed)
- signtool verify /pa succeeds against every signed binary
- The deployment guide instructs customers to configure App Control rules by trusted publisher rather than per-file hash

**Verification:** signtool verify /pa /v on any shipped binary returns success with a chain to a trusted commercial root

#### `ch19-shipping-to-enterprise:ENT-07` — MDM-platform-agnostic attestation core

Sunfish.Kernel.Security verifies the enterprise attestation issuer public key from node-config.json regardless of which MDM platform deployed the configuration, so adding a new MDM is a packaging-and-detection-rule exercise rather than a kernel change.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Attestation verification consumes only the issuer public key from node-config.json
- No code path branches on which MDM platform deployed the configuration
- Adding a new MDM platform requires only a packaging recipe and a detection rule

**Verification:** Code review confirms no MDM-platform identifier influences attestation verification; integration tests pass identical attestation flows under at least Intune and Jamf packaging

#### `ch19-shipping-to-enterprise:ENT-08` — Six-MDM coverage matrix

The product ships deployment recipes for Intune, Jamf, SOTI MobiControl, IBM MaaS360, Ivanti Endpoint Manager, and SCCM so that GCC, Indian BFSI, APAC, and African enterprise fleets can deploy via their existing MDM platform.

**Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection`

**Must implement:**

- Documentation provides a deployment recipe for each of the six named MDM platforms
- Each recipe includes a service-registration detection rule and a pre-seeded config deployment path
- Each recipe is validated on a representative test fleet before publication

**Verification:** docs/ contains a per-MDM deployment runbook for each of the six platforms and each recipe references the same node-config.json schema

#### `ch19-shipping-to-enterprise:ENT-09` — Pre-seeded node-config.json schema

A versioned JSON configuration schema delivered to a platform-specific path before first run that supplies team identity, relay endpoint, allowed buckets, data directory, log level, internal update server URL, and the enterprise attestation issuer public key.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `schema-skew`

**Must implement:**

- node-config.json declares schemaVersion and is validated against the published schema at startup
- All required fields (teamId, relayEndpoint, allowedBuckets, dataDirectory, enterpriseAttestationIssuerPublicKey) must be present
- The host refuses to start on schema validation failure rather than falling back to defaults
- Per-platform paths follow the documented Windows/Linux/macOS conventions

**Verification:** Starting the host with a malformed or incomplete node-config.json produces a logged validation error and a non-zero exit; integration test asserts no default-fallback behavior

#### `ch19-shipping-to-enterprise:ENT-10` — Compliance check at every capability negotiation

MDM compliance is re-evaluated at every capability-negotiation handshake rather than once at install, so revocation of MDM compliance propagates to data access within minutes of the next handshake boundary.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Relay queries MDM compliance status on every capability-negotiation handshake
- Non-compliant nodes receive ERR_ATTESTATION_REQUIRED and have sync suspended
- Active sessions do not retain access past the next handshake after compliance loss

**Verification:** Integration test marks a node non-compliant mid-session and asserts the next handshake returns ERR_ATTESTATION_REQUIRED within the documented propagation window

#### `ch19-shipping-to-enterprise:ENT-11` — Build-time CycloneDX SBOM generation

A CycloneDX-format SBOM is generated from source at build time as a required CI gate and published alongside every release artifact at a predictable URL.

**Scope:** `foundational`

**Must implement:**

- CI generates a CycloneDX JSON SBOM from source on every release build
- SBOM generation is a required gate that blocks the release pipeline on failure
- The SBOM is published to a predictable URL alongside the release artifact
- The SBOM is signed and a SHA-256 digest is published next to it

**Verification:** Release pipeline log shows SBOM generation as a required gate; the published mirror serves the SBOM and its SHA-256 at the documented URL

#### `ch19-shipping-to-enterprise:ENT-12` — CVE scan as release gate

A vulnerability scan runs the generated SBOM against a known-CVE database during CI and fails the release on any high or critical finding without a documented suppression entry.

**Scope:** `foundational`

**Must implement:**

- CI runs grype (or equivalent) against the build-time SBOM
- The scanner is configured to fail the build on high or critical CVEs
- Suppression entries require a documented justification and an expiry date
- Suppression entries are reviewed before each release

**Verification:** Release pipeline configuration shows --fail-on high (or equivalent) wired in; suppression file contains expiry dates and justifications for every entry

#### `ch19-shipping-to-enterprise:ENT-13` — Published CVE response SLA

A written, severity-tiered CVE response commitment specifying advisory and patch timelines is published before procurement asks and demonstrably met in practice.

**Kleppmann:** `P6` · **Scope:** `foundational`

**Must implement:**

- Security policy document states timelines per severity tier (Critical, High, Medium, Low)
- Critical (CVSS >= 9.0) commits to public advisory within 48 hours and patch within 14 days
- High (CVSS 7.0-8.9) commits to a patch within 30 days
- The SLA is published before procurement engagement, not on request

**Verification:** A SECURITY.md or equivalent document contains the severity-tiered SLA table; release records show actual response times meeting the published commitments

#### `ch19-shipping-to-enterprise:ENT-14` — Pre-rehearsed critical-CVE patch drill

The full critical-patch release sequence — fix, rebuild, regenerate SBOM, rescan, sign and notarize, mirror, and canary push — is rehearsed end-to-end during the first sprint after general availability and the elapsed time measured against the published SLA.

**Scope:** `foundational`

**Must implement:**

- A dry-fire patch release is executed against a test artifact within the first GA sprint
- Elapsed time per pipeline step is recorded
- Steps exceeding their share of the SLA budget are tightened before the next drill

**Verification:** Engineering records contain a dated dry-fire patch report with per-step elapsed times and remediation actions for any step exceeding budget

#### `ch19-shipping-to-enterprise:ENT-15` — Named admin revocation command with audit trail

Revoking a user is a single named CLI command that rotates the affected role's KEK, re-wraps DEKs excluding the revoked user, broadcasts a signed revocation through the relay, and writes a revocation record to the audit log.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- A documented CLI command (sunfish admin revoke --user --team) executes revocation atomically
- Execution generates a new KEK for the affected role
- All DEKs are re-wrapped under the new KEK excluding the revoked user
- A signed revocation message is broadcast through the relay
- A revocation record with timestamp and operator identity is written to the audit log
- The relay returns ERR_KEY_REVOKED on the revoked node's next handshake

**Verification:** Running the revocation command against a test team produces a new KEK, an audit log entry with operator identity, and ERR_KEY_REVOKED on the revoked node's next handshake

#### `ch19-shipping-to-enterprise:ENT-16` — Air-gap-strict deployment posture

The same binary supports a strict air-gap posture configured by pointing updateServerUrl and relayEndpoint at internal infrastructure, omitting telemetry, and applying egress firewall rules — without a separate build artifact.

**Kleppmann:** `P3, P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-outage`

**Must implement:**

- The release binary runs unchanged in connected, proxied, and air-gap-strict postures
- node-config.json switches posture by configuration alone
- No build flag or separate artifact is required for air-gap operation
- Documentation lists exactly which destinations are safe to block and which are not

**Verification:** A binary identical to the public release runs in an isolated test network with internal mirror and internal relay only; no outbound public-internet connections are observed

#### `ch19-shipping-to-enterprise:ENT-17` — Internal update server REST contract

The internal update server exposes a minimal REST surface for latest-version metadata, versioned artifact downloads, and per-release SBOM with SHA-256 digest, allowing offline mirrors to satisfy the same client expectations as the public update feed.

**Kleppmann:** `P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- GET /releases/latest.json returns version, publish timestamp, artifact URLs, per-artifact SHA-256, and SBOM URL plus SHA-256
- GET /releases/{version}/artifacts/{name} returns the named artifact bytes
- GET /releases/{version}/Sunfish.cdx.json returns the SBOM
- GET /releases/{version}/Sunfish.cdx.sha256 returns the SBOM digest
- Nodes verify SHA-256 of every artifact before installing
- Nodes archive the SBOM alongside the artifact for audit

**Verification:** Conformance test pulls latest.json, downloads the artifact, validates the SHA-256 match, fetches and digest-verifies the SBOM, and rejects any artifact whose digest fails to match

#### `ch19-shipping-to-enterprise:ENT-18` — OCSP and CRL connectivity preservation

Air-gap egress policy must preserve a path to OCSP and CRL responders — internal mirror, certificate pinning with long-lived certs, or open egress to public responders — because blocking revocation checking breaks TLS chain validation across the entire node, not just update checks.

**Kleppmann:** `P6` · **Scope:** `foundational`

**Must implement:**

- Air-gap deployment guidance names OCSP/CRL preservation as non-negotiable
- At least one of internal OCSP responder, certificate pinning with long-lived cert, or whitelisted public OCSP egress is configured
- The deployment runbook lists OCSP/CRL responders explicitly under "do not block"

**Verification:** Air-gap deployment validation includes a TLS handshake to the relay endpoint succeeding without OCSP soft-fail; deployment runbook lists OCSP/CRL on the do-not-block list

#### `ch19-shipping-to-enterprise:ENT-19` — Jurisdictional self-hosted Bridge relay

For compliance-mandated markets the self-hosted Bridge relay runs on infrastructure within the required jurisdiction — on-premise, sovereign cloud, or domestic data center — making the relay-sovereignty guarantee legally defensible rather than a marketing claim.

**Kleppmann:** `P5, P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection, vendor-outage`

**Must implement:**

- Bridge relay deploys as a single statically-compiled binary or OCI container image
- Relay listens on TLS 1.3 only and authenticates connections against Ed25519 public keys from enterpriseAttestationIssuerPublicKey
- Relay forwards CRDT operation frames without access to payload content
- Production deployments run at least two-node HA, with three-node automatic failover for enterprise SLA tiers
- Deployment infrastructure is sited within the required regulatory jurisdiction

**Verification:** Deployed relay rejects non-TLS-1.3 connections, accepts only attested Ed25519 identities, has no payload-decryption code paths, and is hosted within the regulator-approved jurisdiction (verifiable from cloud-provider region or on-premise inventory)

#### `ch19-shipping-to-enterprise:ENT-20` — Power-interruption-resilient endpoint specification

For deployments in load-shedding or unstable-grid environments the hardware specification names a UPS with at least 30-minute runtime and SSDs with power-loss-protection capacitors as a baseline, not an optional upgrade.

**Kleppmann:** `P3, P5` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Endpoint hardware specification names UPS with >=30-minute runtime for affected regions
- Local SQLCipher database resides on an SSD with power-loss-protection capacitors
- Sync daemon resumes cleanly from cold restart by replaying the append-only event log
- MDM compliance re-attests on first successful handshake after power loss

**Verification:** Abrupt-power-loss test drops AC mid-write and confirms event-log durability, clean restart, gossip resumption, and successful MDM re-attestation on next handshake

#### `ch19-shipping-to-enterprise:ENT-21` — Compliance documentation pipeline

A repeatable workflow that exports the audit log, SBOM, Grype CVE report, MDM compliance manifest, and Bridge relay jurisdictional configuration and assembles them into the format each compliance regime accepts (SOC 2 Type II, GDPR Article 30, EU CRA, regimes in Appendix F).

**Kleppmann:** `P5, P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection`

**Must implement:**

- sunfish admin audit-export emits a date-bounded CSV-and-JSON bundle mapping to SOC 2 Trust Services Criteria
- A quarterly GDPR Article 30 rollup is assembled from bucket definitions, node-config.json, SBOM, and MDM manifest
- SBOMs are signed and attested under SLSA Level 3 to satisfy EU CRA SBOM obligations
- Each Appendix F regime has a documented mapping from the common evidence substrate to its required document format

**Verification:** Documentation pipeline produces a SOC 2 evidence bundle, a GDPR Article 30 record, and an EU CRA SBOM attestation from a single test deployment without manual data re-entry

#### `ch19-shipping-to-enterprise:ENT-22` — Three-runbook minimum for enterprise GA

Enterprise general availability requires three published runbooks — node onboarding, node deprovisioning, and incident response for node or key compromise — each with named commands, expected outputs, and audit-log verification steps.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Node onboarding runbook covers IdP confirmation, attestation issuance, pre-seeded config, MDM deployment, and audit-log verification
- Node deprovisioning runbook covers admin revocation, MDM wipe, and audit-log archival
- Incident response runbook covers immediate revocation on suspicion, forensic-hold coordination, and key-material rotation
- Each runbook includes the named command, expected output, and an audit-log verification step

**Verification:** docs/runbooks/ contains all three named runbooks with command-output-verification triplets and expected-duration targets

#### `ch19-shipping-to-enterprise:ENT-23` — Staged canary update rollout

Production updates roll out in three stages — five-to-ten-percent canary, fifty percent, one hundred percent — with twenty-four-hour holds at each stage and a defined rollback by republishing the previous artifact through the same MDM policy on health-check failure.

**Scope:** `foundational`

**Must implement:**

- Update rollouts target a 5-10% canary deployment ring first
- Each stage holds at least 24 hours before promotion
- Health-check criteria include sync-daemon running, no ERR_ events in relay logs, and no MDM compliance failures
- Rollback republishes the previous artifact via the same MDM policy
- The internal update server continues serving the previous version until rollback completes
- Failed rollouts produce an incident report before any retry

**Verification:** A staged-rollout dry-run on a test fleet executes all three stages with documented holds and a successful canary-failure rollback within the published health-check criteria


### Epic: UX, Sync, and Conflict (ch20-ux-sync-conflict)

**Source-paper refs:** v13 §13, v13 §14, v5 §6

**Concept count:** 25

#### `ch20-ux-sync-conflict:UX-01` — Complexity Hiding Standard

A non-technical user must not be able to determine from normal use whether the application is local-first or cloud-first; the only visible difference is that the local-first app keeps working when the internet does not.

**Kleppmann:** `P1, P3` · **Scope:** `foundational`

**Must implement:**

- User-facing strings expose no distributed-systems vocabulary (no "gossip", "relay-only", "peer sync")
- No "offline mode" banner or modal differentiates online from offline operation
- Application chrome remains constant across connectivity states except for ambient indicators

**Verification:** A non-technical reviewer using the app under normal connectivity and full offline cannot identify which state they are in from chrome alone.

#### `ch20-ux-sync-conflict:UX-02` — Plain-language register for all user-visible state

Every string a user reads must pass a plain-language test — a practitioner with no knowledge of distributed systems understands it without training.

**Kleppmann:** `P1` · **Scope:** `foundational`

**Must implement:**

- String catalog excludes infrastructure terminology in any user-visible surface
- Status messages name user actions and consequences, not protocol states
- Translation review enforces the plain-language register in every active locale

**Verification:** String audit confirms no occurrences of forbidden terms (gossip, relay, quorum, epoch, attestation, CRDT) in any user-facing locale file.

#### `ch20-ux-sync-conflict:UX-03` — Three always-visible status indicators

The application status bar displays three indicators at all times — node health, link status, and data freshness — non-intrusive under normal conditions and expanding to plain-language labels under degraded conditions.

**Kleppmann:** `P1, P3` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Status bar persists across all application screens
- Three indicators (node health, link status, data freshness) are present and ambient under normal conditions
- Degraded states surface a short plain-language label and amber/red emphasis

**Verification:** Application shell includes a status bar implementing the three indicators; a screenshot under normal connectivity shows ambient icons with no labels.

#### `ch20-ux-sync-conflict:UX-04` — Node health indicator semantics

The node health indicator signals whether the local node is operating normally (green = engine and sync daemon running and last self-check passed; amber = degraded; red = node cannot accept writes and requires user action).

**Kleppmann:** `P1, P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Indicator reflects engine, sync-daemon, and self-check state
- Amber state covers disk-near-capacity, sync-daemon restart, and schema-migration-in-progress
- Red state surfaces a plain-language prompt for required user action (e.g., re-sign-in after credential revocation) without naming protocol terms

**Verification:** Forcing each underlying condition (low disk, daemon restart, migration, credential revocation) drives the indicator to the documented state and surface text.

#### `ch20-ux-sync-conflict:UX-05` — Link status indicator semantics with no red state

The link status indicator signals connectivity to the team using green (peer reachable, gossip flowing), amber (relay-only), and grey (fully offline) — and never red, because connectivity failure is not an error condition for a local-first node.

**Kleppmann:** `P3` · **Scope:** `foundational` · **Failure modes:** `partition, peer-discovery-failure`

**Must implement:**

- Indicator distinguishes peer-reachable, relay-only, and offline states
- No red state is ever presented for connectivity loss
- Offline state is rendered as ambient grey, not as a warning

**Verification:** Disconnecting the network drives the indicator to grey without surfacing any error or warning chrome.

#### `ch20-ux-sync-conflict:UX-06` — Data freshness indicator with hidden-by-default policy

The data freshness indicator is invisible while every active data class is within its staleness threshold and only surfaces when a threshold is close to expiring or has expired.

**Kleppmann:** `P1, P3` · **Scope:** `foundational` · **Failure modes:** `clock-skew`

**Must implement:**

- Indicator computes staleness against the configured threshold for each active data class
- Indicator is hidden under normal conditions and only renders amber or red when thresholds approach or exceed their limit
- Threshold configuration is sourced from the AP/CP classification declared in sync configuration

**Verification:** With all data classes within threshold the indicator does not render; advancing system clock past a threshold causes the indicator to appear in the documented state.

#### `ch20-ux-sync-conflict:UX-07` — AP/CP visibility per data class

Each data class declares its own staleness threshold and UX treatment derived from its AP/CP classification, with tighter thresholds and stricter blocking for data whose stale use causes immediate concrete harm.

**Kleppmann:** `P1, P3, P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `clock-skew, partition`

**Must implement:**

- Each data class declares a staleness threshold and UX treatment in configuration
- CP-class actions are blocked while freshness cannot be confirmed; AP-class edits apply locally and propagate
- Per-record freshness is computed against the class threshold without per-application code

**Verification:** Configuration manifest enumerates data classes with thresholds and treatments; behavioral test confirms a CP-class write is blocked while a matching AP-class write succeeds offline.

#### `ch20-ux-sync-conflict:UX-08` — Per-record freshness badge bound to AP/CP classification

A freshness badge component renders the per-record indicator for any data class, computing staleness against the configured threshold and handling clock-skew, daylight-saving, and suspend/resume edge cases without per-application code.

**Kleppmann:** `P1, P3` · **Scope:** `inverted-stack-specific` · **Failure modes:** `clock-skew`

**Must implement:**

- Component binds to the AP/CP classification configured in the sync layer
- Component handles suspend/resume and clock adjustments without losing accuracy
- Per-application code does not implement freshness timers

**Verification:** Suspending the host machine across a threshold boundary, then resuming, drives the badge to the correct post-resume state without the application invoking a timer reset.

#### `ch20-ux-sync-conflict:UX-09` — Three-state optimistic write lifecycle

An AP-class write moves through three explicit visual states — pending (applied locally, not yet seen by any peer), confirmed (received by at least one peer), and failed (circuit breaker rejected on reconnect) — with the failed state opening the conflict inbox.

**Kleppmann:** `P1, P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Writes apply locally on user confirmation and surface a pending visual state immediately
- Confirmation state is reached when at least one peer has acknowledged the write
- Failed state is distinct from pending and offers a "Review" affordance into the conflict inbox

**Verification:** A write performed offline shows pending; reconnecting with no conflict transitions it to confirmed; reconnecting with an unresolvable conflict transitions it to failed and opens the conflict inbox via the Review affordance.

#### `ch20-ux-sync-conflict:UX-10` — Pending and failed states never collapse

A failed write must never remain in the pending visual state, because a user who sees a persistent spinner waits while a user who sees a failure indicator acts.

**Kleppmann:** `P1, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Pending state has a deterministic upper bound after which the UI resolves to confirmed or failed
- Circuit-breaker rejection surfaces as a failed state on the affected record
- The pending visual state never persists past the documented timeout without a state transition

**Verification:** Forcing a circuit-breaker rejection at reconnect resolves the pending visual state to failed within the documented bound, never indefinitely spinning.

#### `ch20-ux-sync-conflict:UX-11` — Conflict inbox as single resolution surface

All conflict resolution occurs in a dedicated panel — not a modal, not an interstitial — accessible from the status bar and any failed-write indicator.

**Kleppmann:** `P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Application exposes one canonical conflict inbox surface, not multiple per-feature dialogs
- Inbox is reachable from both the status bar and any failed-write indicator
- Conflict resolution UX never blocks unrelated work via modal dialogs

**Verification:** Two independent conflict-producing edits route both items to the same inbox panel reachable from the status bar.

#### `ch20-ux-sync-conflict:UX-12` — Conflict grouping by record type and field

The conflict inbox groups conflicts by record type and field so a non-technical user sees structured items like "Status conflict on task: Design Review" rather than a raw CRDT diff.

**Kleppmann:** `P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Conflicts are grouped by record type and conflicting field
- Group labels use the user-facing entity name and field label, not internal identifiers
- Raw CRDT diffs are not surfaced in the default view

**Verification:** Producing N conflicts on the same record-type/field shows a single grouped item containing N entries with a human-readable label.

#### `ch20-ux-sync-conflict:UX-13` — Configurable resolution rules constrained by data model

Per-conflict-group resolution offers prefer-mine, prefer-remote, or a configurable merge rule chosen from rules declared per record type — end users cannot select arbitrary merge strategies the data model does not support.

**Kleppmann:** `P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Merge rules are declared per record type in application configuration
- Resolution UI presents only declared rules for the affected type
- Component rejects attempts to apply undeclared rules

**Verification:** Configuration declares a numeric "keep higher value" rule; resolution UI for a numeric field offers it and rejects an attempt to apply a non-declared rule.

#### `ch20-ux-sync-conflict:UX-14` — Resolve-all-similar bulk action

A bulk affordance applies a chosen rule to every conflict of the same shape in a single operation, with outliers retained for individual review.

**Kleppmann:** `P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Bulk action applies the selected rule to all conflicts matching the active group's shape
- Outliers that do not match the rule remain in the inbox for individual handling
- The bulk action is reachable from the inbox without leaving the surface

**Verification:** Producing 40 same-shape conflicts and applying "resolve all similar" with one rule resolves them in one user-visible operation, leaving any outliers visible.

#### `ch20-ux-sync-conflict:UX-15` — Auditable conflict-resolution event log

Every conflict resolution writes an event log entry recording the conflict shape, the rule applied, the resolving user, and the timestamp; no resolution may pass through the system without a corresponding entry.

**Kleppmann:** `P4, P6` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Each resolution emits a structured log entry with shape, rule, user, and timestamp
- Log entries are persisted alongside the underlying CRDT events
- Resolution paths that bypass logging are rejected at component boundary

**Verification:** Performing a resolution and inspecting the event log shows a matching entry; attempting to invoke a non-logging resolution path fails at the component boundary.

#### `ch20-ux-sync-conflict:UX-16` — Three distinct connectivity-failure UX modes

Full offline, partial connectivity (relay-only), and the quarantine queue are surfaced as three distinct UX modes, not collapsed into a single "offline" treatment.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition, peer-discovery-failure`

**Must implement:**

- Full offline runs at full fidelity with no degraded banner and no implied apology
- Relay-only mode surfaces specific explanations for actions requiring direct peer connectivity
- Quarantine queue surfaces a one-sentence count and a single review action on reconnect

**Verification:** Each of the three states presents the documented surface in isolation; collapsing any two into a shared treatment fails the test.

#### `ch20-ux-sync-conflict:UX-17` — Quarantine queue surfaced before sync completes

When the node reconnects with offline writes pending validation, the quarantine count is surfaced as a one-sentence courtesy with a single review action before sync completes — not as a modal blocker, and not after the fact.

**Kleppmann:** `P3, P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Reconnect surfaces the pending-validation count before sync completion
- The surface is a non-blocking notification with a single review action
- Dismissal allows sync to complete and routes any conflicts to the inbox

**Verification:** Producing N offline writes and reconnecting surfaces a count-of-N notification with a Review action; dismissing it completes sync silently and any resulting conflicts appear in the inbox.

#### `ch20-ux-sync-conflict:UX-18` — Invisible recovery from unexpected shutdown

After a power-loss or OS-kill termination the node validates the last write-ahead checkpoint, replays pending writes from the CRDT log, and surfaces a single short status only when replay takes more than two seconds — never a crash dialog.

**Kleppmann:** `P1, P3, P5` · **Scope:** `foundational`

**Must implement:**

- Relaunch validates the WAL checkpoint and replays the CRDT log automatically
- Workspace opens as soon as replay completes
- Replay surface appears only when recovery exceeds two seconds; no crash dialog is presented

**Verification:** Killing the node mid-write and relaunching opens the workspace at the prior state; injecting a long-replay condition surfaces the documented status string and no crash dialog.

#### `ch20-ux-sync-conflict:UX-19` — First-run two-choice gate

A new user sees exactly two options on first run — Start a new team and Join an existing team — with no onboarding tour, no feature callouts, and no auxiliary links.

**Kleppmann:** `P2, P4` · **Scope:** `inverted-stack-specific`

**Must implement:**

- First-run screen presents exactly the two named options
- No tour, callout, or auxiliary action is presented before the choice
- The chosen path determines all subsequent first-run flow

**Verification:** Fresh-install launch renders only the two-option chooser; instrumentation confirms no other actionable elements are present.

#### `ch20-ux-sync-conflict:UX-20` — Mandatory BYOC backup configuration before workspace opens

Choosing "Start a new team" prompts for the first BYOC backup configuration before the application opens, framed in plain language with concrete target choices (local folder, OneDrive, Dropbox) — not as a later step.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-loss`

**Must implement:**

- New-team flow blocks workspace open until a backup target is configured
- Backup target prompt offers concrete named options, not a generic file picker
- The prompt uses plain language that avoids "BYOC" and similar terminology

**Verification:** Selecting "Start a new team" presents the backup-target prompt before the workspace renders; the workspace cannot be reached without configuring a target.

#### `ch20-ux-sync-conflict:UX-21` — Jurisdictional backup-target labelling and gating

Each backup target is labelled with its jurisdiction in plain language, and out-of-jurisdiction options are blocked with a short explanation when the team's declared jurisdiction requires in-country storage.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection`

**Must implement:**

- Each backup option displays its jurisdiction (e.g., "OneDrive (Microsoft, United States)")
- Out-of-jurisdiction targets are blocked when team policy requires in-country storage
- Block surfaces a short plain-language explanation referencing the team policy

**Verification:** Configuring a team with an in-country requirement renders only in-country targets as selectable; attempting an out-of-jurisdiction target is blocked with the documented explanation.

#### `ch20-ux-sync-conflict:UX-22` — QR-based peer-assisted onboarding

Choosing "Join an existing team" runs the three-step onboarding flow — scan a QR code on an existing team member's device (or paste the bundle), transfer the role attestation, then sync eager buckets in the background — and shows a sync progress indicator until enough data has landed for a meaningful state.

**Kleppmann:** `P2, P4, P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `peer-discovery-failure`

**Must implement:**

- Join flow accepts QR scan and a paste-bundle fallback
- Role attestation transfer occurs before any data download
- Initial eager-bucket sync displays a progress surface and gates workspace open until a meaningful state is reached

**Verification:** Scanning a valid QR transfers the attestation and begins eager-bucket sync; the workspace opens only after the documented progress state is reached.

#### `ch20-ux-sync-conflict:UX-23` — Accessibility as a Tier-1 contract

Every UX surface in the application carries an accessibility contract — semantic ARIA roles, keyboard reachability, declared component metadata, and plain-language assistive-technology text — enforced as rigorously as the write path.

**Kleppmann:** `P1, P4` · **Scope:** `foundational`

**Must implement:**

- Status surfaces use role="status" with aria-live="polite" for ambient changes and role="alert" with aria-live="assertive" for required-action states
- Colour is never the sole signal; every indicator pairs colour with localised text
- Interactive elements support tab order, Enter and Space activation, and Escape-to-dismiss where dismissal is allowed
- Focus after conflict resolution returns to the next pending group, not to the page header

**Verification:** Automated accessibility audit on every shipped UI block confirms ARIA roles, keyboard reachability, and colour-plus-text pairing; a screen-reader walkthrough of the conflict inbox resolves a conflict without pointer input and lands focus on the next pending group.

#### `ch20-ux-sync-conflict:UX-24` — Component-manifest accessibility enforcement

Each UI block declares its ARIA roles, announced state transitions, and keyboard contract via a component manifest, and the platform refuses to register a custom replacement that declares a weaker contract than the component it replaces.

**Kleppmann:** `P4` · **Scope:** `inverted-stack-specific`

**Must implement:**

- UI block manifest declares ARIA role, announced transitions, and keyboard contract
- Platform validates the manifest at registration time
- Custom replacement components must declare an equal-or-stronger contract or fail registration

**Verification:** Registering a custom component whose manifest weakens any declared contract relative to the replaced component fails at registration with a documented error.

#### `ch20-ux-sync-conflict:UX-25` — Plain-language parity across visual and assistive channels

Text surfaced to assistive technology must use the same plain-language register as the visible text, with no fallback to technical terminology in ARIA labels.

**Kleppmann:** `P4` · **Scope:** `foundational`

**Must implement:**

- ARIA labels and live-region announcements use the same plain-language strings as visible text
- String catalog enforces parity between visible and assistive surfaces per locale
- Reviews reject components whose assistive surface drops to technical terminology

**Verification:** Locale audit confirms each visible string has a matching assistive string in the same register; a screen-reader pass on the freshness, optimistic-write, and conflict surfaces hears the same plain-language register as the sighted view.


---

## Part V — Epilogue and appendices

### Epic: What the Stack Owes You (epilogue-what-the-stack-owes-you)

**Source-paper refs:** v13 §20, v5 §9, v5 §10

**Concept count:** 15

#### `epilogue-what-the-stack-owes-you:EPI-01` — Protocol-layer data minimization

Data minimization is a send-tier protocol enforcement that prevents bytes from leaving the originating node toward an unauthorized peer, not a UI filter or server-side policy applied after data arrives.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection`

**Must implement:**

- Sync daemon evaluates authorization against peer attestations before serializing payload
- Unauthorized peers never receive document bytes on the wire
- No filter is applied only at receive time

**Verification:** Wire capture from an unauthorized peer's perspective shows zero protected bytes after capability negotiation completes.

#### `epilogue-what-the-stack-owes-you:EPI-02` — MDM attestation at capability negotiation

Mobile Device Management attestation is verified during capability negotiation before the sync stream opens, so that a non-compliant device is rejected at the perimeter rather than detected post-hoc in an audit log.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Capability negotiation includes an MDM attestation challenge
- Handshake fails closed when attestation is missing or invalid
- No document operation is applied from a peer that has not satisfied attestation

**Verification:** A peer presenting an invalid or absent MDM attestation cannot complete handshake; sync stream is never opened.

#### `epilogue-what-the-stack-owes-you:EPI-03` — Honest three-tier CRDT consistency

The architecture commits to a three-tier resolution model — AP for documents, CP under lease for coordination records, append-only for financial ledger — and names the consistency guarantee per data type rather than presenting a single uniform model.

**Kleppmann:** `P4, P5` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Each data type is assigned an explicit consistency tier
- Document store uses AP CRDT semantics
- Coordination records use CP semantics under a lease protocol
- Financial records use append-only ledger semantics

**Verification:** Architecture document maps every persisted data type to one of the three tiers; the CRDT engine adapter for each tier matches the documented semantics.

#### `epilogue-what-the-stack-owes-you:EPI-04` — Cryptographic role revocation

Role revocation is implemented through DEK/KEK envelope encryption with key rotation proportional to document count, so that a revoked role cannot decrypt documents whose keys have been rotated.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Each protected document is encrypted with a per-document DEK wrapped by a role KEK
- Role revocation triggers DEK rotation for documents the revoked role had access to
- The former role-holder's KEK cannot unwrap rotated DEKs

**Verification:** Revocation procedure is executed, then the revoked principal's key material is presented against rotated documents and fails to decrypt.

#### `epilogue-what-the-stack-owes-you:EPI-05` — Dual license and CLA before community formation

The dual license structure and Contributor License Agreement must exist before the first external pull request, so that governance terms cannot be retroactively changed against contributors who joined under different terms.

**Kleppmann:** `P5` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-acquisition`

**Must implement:**

- Repository has a published dual license at first public commit
- CLA process is in place before merging external contributions
- License change requires contributor consent under documented governance

**Verification:** Repository contains LICENSE, CLA, and governance documents whose commit dates precede the first external pull request merge.

#### `epilogue-what-the-stack-owes-you:EPI-06` — Non-technical disaster recovery

A non-technical user must be able to restore complete data after a device failure without contacting support, using a backup, restore, and verification UX legible to someone who is not an engineer.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `key-loss`

**Must implement:**

- Backup UX surfaces backup state and recency without technical vocabulary
- Restore UX guides recovery from a fresh device end-to-end
- Verification UX confirms restored data integrity to a non-technical user

**Verification:** A non-technical tester completes device-loss recovery scenario without engineering assistance and confirms data integrity.

#### `epilogue-what-the-stack-owes-you:EPI-07` — Plain-file export without vendor cooperation

User data is available on local disk in a documented file format under user-controlled keys, allowing the user to leave the platform at any time without negotiating with the vendor or depending on its continued operation.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- Export format is publicly documented
- Export proceeds entirely from local disk and local key material
- No vendor service is required to produce or interpret an export

**Verification:** Disconnect network and revoke vendor accounts; user produces a complete export and a third-party tool reads it using only the public format spec and the user's keys.

#### `epilogue-what-the-stack-owes-you:EPI-08` — KEK-compromise incident response at scale

The procedure for responding to compromise of a broadly-scoped Key Encryption Key across thousands of documents and hundreds of nodes is specified in principle but has not been validated under production load.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Incident response runbook for KEK compromise exists
- Runbook covers fan-out re-keying across all affected nodes and documents
- Stress-test plan is identified as outstanding work

**Verification:** Runbook document exists naming the steps; an explicit open item records that production-scale validation has not been completed.

> Acknowledged as unfinished work; included so conformance scoring can mark partial coverage rather than overstating completeness.

#### `epilogue-what-the-stack-owes-you:EPI-09` — Relay isolation for high-risk verticals

The relay is designed as a data-minimal transit cache, but a complete threat model and isolation architecture for verticals where metadata about document existence is itself regulated (legal, healthcare) is not yet specified.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection`

**Must implement:**

- Relay deployment documents what metadata is observable at the relay
- High-risk vertical deployments specify additional metadata-isolation controls
- Outstanding work for legal and healthcare isolation is named in the architecture backlog

**Verification:** Threat model document for the relay enumerates observable metadata; deployment guide for high-risk verticals either specifies isolation controls or marks them as open.

#### `epilogue-what-the-stack-owes-you:EPI-10` — Long-now archival format beyond CRDT log

Because the CRDT event log is not a stable archival format, long-horizon durability requires snapshots in standardized formats (signed append-only logs, documented export schemas) that the architecture has not yet specified.

**Kleppmann:** `P5` · **Scope:** `foundational`

**Must implement:**

- Architecture identifies a stable archival snapshot format separate from the live CRDT log
- Periodic snapshot generation is specified
- Snapshot format is consumable without a running CRDT engine

**Verification:** Snapshot specification document exists; a snapshot can be opened and read by a tool that has no CRDT engine in its dependency tree.

#### `epilogue-what-the-stack-owes-you:EPI-11` — Domain invariant enforcement above CRDT convergence

CRDTs deliver structural convergence but not domain invariants such as inventory-cannot-go-negative, no-double-booking, or ledger-balance, which require additional modeling beyond the CRDT engine and have no standardized formal verification approach in this architecture.

**Kleppmann:** `P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Semantic layer enforces named domain invariants on top of CRDT merge
- Each enforced invariant is documented with the data type and the enforcement mechanism
- Invariants whose enforcement is not yet specified are listed as open items

**Verification:** Semantic-layer document enumerates enforced invariants and their mechanisms; merge tests demonstrate violation rejection for each enforced invariant.

#### `epilogue-what-the-stack-owes-you:EPI-12` — Crypto-shredding as right-to-erasure mechanism

Right-to-erasure is implemented technically by destroying the per-document DEK so that ciphertext becomes unrecoverable; whether residual CRDT-log operation metadata constitutes personal data under a given jurisdiction's deletion statute is an unsettled legal question, not a technical one.

**Kleppmann:** `P6, P7` · **Scope:** `foundational`

**Must implement:**

- DEK destruction procedure renders document content unrecoverable
- Residual CRDT operation metadata is documented as the surface a legal review must evaluate
- Per-jurisdiction legal posture is captured in the compliance appendix

**Verification:** Destroying a document's DEK is shown to render its ciphertext unrecoverable; compliance documentation names the jurisdictions in scope and the open legal question for each.

#### `epilogue-what-the-stack-owes-you:EPI-13` — Mobile platform constraints unresolved

iOS and Android impose background-execution, keystore, and filesystem constraints that the desktop-first local-node architecture has not yet solved, so mobile is not yet a first-class deployment target with a fully specified tradeoff envelope.

**Kleppmann:** `P2, P3` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Mobile deployment guide identifies background-execution, keystore, and filesystem constraints
- Tradeoffs in battery, background limits, and permission prompts are documented
- Architecture backlog names mobile-first work as outstanding

**Verification:** Mobile platform notes exist enumerating the constraints and the architectural choices that remain open.

#### `epilogue-what-the-stack-owes-you:EPI-14` — Implementation drift via server-side convenience paths

The dominant failure mode for local-first architectures in practice is the gradual accumulation of locally-reasonable server-side paths — feature gates, analytics, A/B testing, compliance logging, write-time permission checks — that re-establish the server as load-bearing and reduce the local node to a cache.

**Kleppmann:** `P3, P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-outage`

**Must implement:**

- Architecture names each drift anti-pattern with the local-first equivalent that replaces it
- Feature flags evaluate locally via a Sunfish.Foundation.FeatureManagement-equivalent capability
- Telemetry, compliance logging, and permission checks are designed before the first request that would centralize them

**Verification:** ADR set documents each named anti-pattern with the local replacement; sample drift requests are matched to the ADR that already answers them.

#### `epilogue-what-the-stack-owes-you:EPI-15` — ADRs with named enforcement owner

Architecture Decision Records that prevent drift must name an enforcement owner — a review board, principal engineer, or CTO sign-off path — because ADRs without an owner do not survive velocity pressure.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Every drift-prevention ADR names an accountable role for deviation approval
- Deviation requests follow a documented review path
- ADR template requires the enforcement owner field

**Verification:** ADR template includes an enforcement owner field; existing drift-prevention ADRs have that field populated with a named role.


### Epic: Sync Daemon Wire Protocol (appendix-a-sync-daemon-wire-protocol)

**Source-paper refs:** v13 §6.2

**Concept count:** 36

#### `appendix-a-sync-daemon-wire-protocol:WIRE-01` — Unix domain socket transport

The sync daemon exposes its wire protocol over Unix domain sockets on Linux, macOS, and Windows 10 / Server 2019 and later, with a configurable socket path.

**Kleppmann:** `P3, P6` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Daemon listens on a Unix domain socket whose path is configurable
- Default socket path is /var/run/sunfish-sync.sock on Linux/macOS and \\.\pipe\sunfish-sync on Windows
- Daemon supports Linux, macOS, and Windows 10 / Server 2019 and later

**Verification:** Inspect daemon configuration for socket path; confirm a connection can be opened to the configured socket on each supported OS.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-02` — Mandatory Noise_XX tunnel

Every connection must complete a Noise Protocol Framework Noise_XX handshake using Ed25519 static keys, ChaCha20-Poly1305, and BLAKE2s before any CBOR message defined in this protocol is exchanged.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise, replay`

**Must implement:**

- Daemon and relay run a Noise_XX handshake on every new connection
- Static keys use Ed25519; AEAD is ChaCha20-Poly1305; hash is BLAKE2s
- No CBOR message is sent or accepted before Noise handshake completion
- All CBOR framing operates inside the Noise transport layer

**Verification:** Packet capture on the socket shows Noise_XX handshake messages preceding any CBOR body; reject test sending a HELLO before Noise completion is closed without response.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-03` — CBOR length-prefixed framing

Every wire message is a 4-byte little-endian uint32 length prefix followed by exactly that many bytes of CBOR-encoded message body.

**Scope:** `foundational`

**Must implement:**

- Sender writes a 4-byte little-endian uint32 length prefix before each CBOR body
- Receiver reads the length prefix and then the full length bytes before decoding
- Receiver treats partial body reads as a protocol error

**Verification:** Wire-vector test (appendix-a §A.9) round-trips byte-for-byte through the framer.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-04` — Four-MiB body cap

The maximum allowed CBOR body size is 4,194,304 bytes (4 MiB), enforced as a relay memory-allocation invariant by closing any connection whose length prefix exceeds the cap without sending an error.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Receiver rejects any length prefix greater than 4,194,304
- Receiver closes the connection on oversize prefix without emitting an error message
- Relay pre-allocates receive buffers sized to this bound

**Verification:** Send a length prefix of 4 MiB + 1 and confirm the connection closes silently with no error CBOR on the wire.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-05` — Deterministic CBOR for signed fields

Any CBOR encoding of fields that appear in signed contexts must use Deterministic Encoding per RFC 8949 §4.2 — definite-length arrays and maps, lexicographically sorted map keys, shortest-form integers, and shortest exact floating-point representation.

**Kleppmann:** `P6` · **Scope:** `foundational`

**Must implement:**

- Signed CBOR uses definite-length arrays and maps only
- Map keys are sorted by lexicographic byte order
- Integers and floats use shortest exact encoding

**Verification:** Encode an attestation bundle twice on different implementations and compare byte-for-byte equality of the signed input.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-06` — Unknown-field tolerance

Receivers must ignore unknown fields in any CBOR map so that optional fields can be added in minor protocol revisions without breaking older implementations.

**Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Decoder does not error on unrecognised map keys
- Unknown fields are dropped silently and do not affect message validity

**Verification:** Inject an extra unknown key into a HELLO body; confirm the receiver processes the message normally.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-07` — Connection state machine

A connection traverses the states CONNECTING, NOISE_HANDSHAKING, CBOR_HANDSHAKING, STREAMING, ERROR, and CLOSED, with defined transitions between them.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Daemon and relay model the connection as the six named states
- Transitions follow the diagram in §A.3 (e.g. STREAMING reachable only after HELLO/CAPABILITY_NEG/ACK)
- ERROR transitions to CLOSED only after an error message is sent

**Verification:** State-machine test exercises each documented transition and rejects invalid transitions.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-08` — Back-to-back HELLO and CAPABILITY_NEG

The connecting node sends HELLO immediately followed by CAPABILITY_NEG without waiting for a response, allowing the relay to construct attestation, lease, and bucket authorisation in one transaction and saving a round trip.

**Kleppmann:** `P1` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Connecting node emits CAPABILITY_NEG without awaiting a response to HELLO
- Relay buffers HELLO and processes both messages together
- Relay indexes pending-handshake state by node_id from HELLO before CAPABILITY_NEG arrives

**Verification:** Trace shows CAPABILITY_NEG sent immediately after HELLO with no intervening server message.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-09` — HELLO message

HELLO is the first CBOR message of every connection and carries node_id (Ed25519 32-byte public key), schema_version (semver string), supported_versions (semver array), and protocol_version (uint major version).

**Scope:** `inverted-stack-specific`

**Must implement:**

- Connecting node sends HELLO as its first CBOR message
- HELLO includes node_id, schema_version, supported_versions, and protocol_version
- node_id is exactly 32 bytes and equals the node's Ed25519 public key

**Verification:** Wire-vector 1 in §A.9 decodes to the documented field set with correct CBOR types.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-10` — Stable node_id identity

The node_id Ed25519 public key is the stable identity of a node across reconnections and must not be rotated without re-onboarding through the attestation flow.

**Kleppmann:** `P2, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-loss`

**Must implement:**

- Daemon persists node_id across restarts and reconnections
- Daemon does not generate a new node_id without re-running onboarding
- Relay uses node_id as the lookup key for attestation and lease state

**Verification:** Restart the daemon and confirm node_id is unchanged in the next HELLO.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-11` — CAPABILITY_NEG message

CAPABILITY_NEG follows HELLO and requests CRDT stream subscriptions, optional CP-class lease record types, sync bucket subscriptions, and carries the AttestationBundle proving the node's role.

**Kleppmann:** `P4` · **Scope:** `inverted-stack-specific`

**Must implement:**

- CAPABILITY_NEG carries crdt_streams, bucket_subscriptions, and attestation_bundle
- cp_leases is omitted when the node has no CP-class record requirements
- Stream identifiers are stable across reconnections

**Verification:** Decode a CAPABILITY_NEG vector and confirm field presence and types match §A.3.2.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-12` — Stream and bucket attestation gating

The relay validates each requested CRDT stream identifier and bucket subscription against the role claims in the attestation bundle before granting access.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Relay parses attestation_bundle role_claims before granting any stream
- Relay refuses streams or buckets not authorised by role_claims
- Granted set is a subset of requested set

**Verification:** Submit CAPABILITY_NEG with a stream not authorised by the bundle; confirm the stream is absent from granted_streams in ACK.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-13` — CP-class lease acquisition before ACK

For every record type listed in cp_leases the relay acquires and holds a Flease-protocol distributed lease on behalf of the node before returning ACK; types not listed default to AP-class with no lease.

**Kleppmann:** `P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Relay acquires Flease leases for each cp_leases entry prior to ACK
- Relay treats record types omitted from cp_leases as AP-class
- Lease is held for the lifetime of the session

**Verification:** Integration test: connecting with cp_leases set blocks ACK until lease acquisition completes.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-14` — ACK message

ACK is the relay's single closing message of the handshake, carrying negotiated_version, granted_streams, granted_buckets, and an optional human-readable denied_reason; receipt of ACK transitions the connection to STREAMING.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Relay sends ACK only after validating both HELLO and CAPABILITY_NEG
- ACK carries negotiated_version, granted_streams, granted_buckets
- denied_reason is included when any requested resource is refused

**Verification:** Wire-vector test for ACK decodes the expected fields; STREAMING transition occurs on ACK receipt.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-15` — Wire-version negotiation rule

negotiated_version is the highest wire protocol version supported by both peers (intersection of node supported_versions and relay capabilities), and the connecting node must use that version for all subsequent messages.

**Scope:** `inverted-stack-specific` · **Failure modes:** `schema-skew`

**Must implement:**

- Relay selects the highest mutually supported version present in supported_versions
- Connecting node uses negotiated_version for every subsequent message
- Node logs a downgrade when negotiated_version differs from its preferred protocol_version

**Verification:** Connect with supported_versions = ["1.0.0","1.1.0"] against a relay capped at 1.0.0; confirm negotiated_version = 1 and downgrade is logged.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-16` — Empty grant is not an error

granted_streams and granted_buckets may be empty arrays when the attestation bundle authorises none of the requested resources; the connection remains valid and the node should surface the empty grant to the operator.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Receiver does not treat empty grant arrays as a protocol error
- Daemon surfaces empty-grant condition to the operator log
- Daemon does not silently continue without alerting

**Verification:** Test attestation that authorises no requested streams produces ACK with empty arrays and operator-visible warning.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-17` — DELTA_STREAM message

DELTA_STREAM carries a single CRDT operation tagged with stream_id, op_type (insert/delete/update), vector_clock, opaque CRDT payload bytes, and an optional epoch_id for CP-class records, fanned out by the relay to every node subscribed to that stream.

**Kleppmann:** `P3, P4` · **Scope:** `inverted-stack-specific`

**Must implement:**

- DELTA_STREAM includes stream_id, op_type, vector_clock, payload
- epoch_id is set on every CP-class operation
- Relay fans out received DELTA_STREAM to every subscriber of stream_id
- stream_id matches an entry in granted_streams

**Verification:** Multi-peer test: a DELTA_STREAM published by one node arrives unchanged at every subscribed peer.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-18` — Vector-clock node-key encoding

Vector clocks are CBOR maps whose keys are the 64-character lowercase hexadecimal encoding of a node's 32-byte Ed25519 public key (tstr) and whose values are uint sequence numbers.

**Scope:** `foundational` · **Failure modes:** `clock-skew`

**Must implement:**

- Vector-clock keys use lowercase hex encoding of the Ed25519 public key
- Vector-clock values are CBOR uint sequence numbers
- Encoder emits exactly 64 hex characters per key

**Verification:** Decode a DELTA_STREAM vector and verify keys are 64 lowercase hex characters and values parse as uint.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-19` — op_type as advisory routing metadata

op_type is advisory metadata used by the receiving application layer to route a delta to the correct merge handler; the CRDT engine applies payload regardless of op_type, so applications routing on op_type must validate against post-apply state.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Sender sets op_type to one of "insert", "delete", "update" accurately
- Receiver does not reject a message solely on op_type/payload mismatch
- Applications routing on op_type validate against engine state if correctness depends on the distinction

**Verification:** Code review confirms application routing layer validates engine post-apply state when correctness depends on op_type.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-20` — Epoch verification before CP-class apply

For any CP-class operation the receiver must verify that its local epoch matches the message's epoch_id before applying the payload, producing ERR_EPOCH_MISMATCH on disagreement.

**Kleppmann:** `P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Receiver checks local epoch against epoch_id for every CP-class operation
- Receiver emits ERR_EPOCH_MISMATCH on mismatch and does not apply the payload
- Non-CP operations skip the epoch check

**Verification:** Inject a DELTA_STREAM with stale epoch_id; receiver returns ERR_EPOCH_MISMATCH and CRDT state is unchanged.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-21` — No relay reordering or buffering

The relay does not reorder or buffer DELTA_STREAM messages; operations are delivered in network order and the CRDT engine guarantees convergent merge regardless of arrival order.

**Kleppmann:** `P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Relay forwards DELTA_STREAM in receive order without buffering
- CRDT engine produces convergent merge under arbitrary delivery order

**Verification:** Relay test: ordered injected stream emerges in the same order at subscribers; multi-peer convergence test demonstrates byte-identical state under reordered deliveries.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-22` — GOSSIP_PING membership protocol

Each node sends a GOSSIP_PING to all connected peers every 30 seconds carrying sender_id, a partial membership_excerpt of known peers, and the sender's vector_clock summary; the relay forwards the message unchanged.

**Kleppmann:** `P3, P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition, peer-discovery-failure`

**Must implement:**

- Daemon emits GOSSIP_PING on a 30-second interval to every connected peer
- GOSSIP_PING carries sender_id, membership_excerpt, sender_vector_clock
- Relay forwards GOSSIP_PING without generating its own

**Verification:** Trace shows GOSSIP_PING from each node every 30 s with correctly populated membership_excerpt entries.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-23` — Membership excerpt entry shape

Each membership_excerpt entry is a CBOR map with node_id (32-byte Ed25519 public key), last_seen (Unix-seconds uint), and vector_clock_summary (map of hex node-key to uint sequence number).

**Scope:** `inverted-stack-specific`

**Must implement:**

- Each entry contains node_id, last_seen, vector_clock_summary
- last_seen is Unix-seconds uint
- vector_clock_summary uses the same hex-key encoding as DELTA_STREAM vector clocks

**Verification:** Decode a GOSSIP_PING vector and confirm each entry has the three fields with documented types.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-24` — Ninety-second suspected-partition threshold

A receiver that observes a peer's last_seen older than 90 seconds (three times the 30-second ping interval) should mark that peer suspected-partitioned and escalate to the application layer.

**Kleppmann:** `P3` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- Receiver tracks last_seen per peer from incoming GOSSIP_PING entries
- Receiver flags peers with last_seen age greater than 90 s as suspected-partitioned
- Daemon escalates suspected-partition events to the application layer

**Verification:** Halt a peer's GOSSIP_PING; after 90 s the receiver raises a suspected-partition signal.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-25` — Long-absence reconnect treated as new node

A node returning after long absence is treated as a new connection — prior session state is discarded, CAPABILITY_NEG reacquires leases and subscriptions, and catch-up proceeds via DELTA_STREAM replay rather than session resume.

**Kleppmann:** `P3` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition, peer-discovery-failure`

**Must implement:**

- Relay discards prior session state on reconnect
- Returning node re-runs full handshake including CAPABILITY_NEG
- Catch-up uses DELTA_STREAM replay; no session-resume primitive is used

**Verification:** Disconnect a node for hours; on reconnect verify a fresh handshake and DELTA_STREAM replay rather than a resume.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-26` — Error message envelope

All error messages share a CBOR map with type (the error code string) and reason (a human-readable description) and may be sent at any point in the connection lifecycle including during the handshake.

**Scope:** `foundational`

**Must implement:**

- Error messages carry the documented type and reason fields
- Errors are valid in any state, including handshake
- Receiver applies the documented retry semantics for each error code

**Verification:** Inject each error code mid-stream and mid-handshake; confirm decoder recognises the envelope and triggers correct retry behaviour.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-27` — Error retry semantics catalogue

Each defined error code carries a normative retry policy — exponential backoff with jitter for ERR_RATE_LIMIT_EXCEEDED and ERR_THROTTLE, no-retry for ERR_VERSION_INCOMPATIBLE and ERR_BUCKET_NOT_AUTHORIZED, IdP re-authentication for ERR_ATTESTATION_REQUIRED and ERR_KEY_REVOKED, and epoch snapshot fetch for ERR_EPOCH_MISMATCH.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise, key-loss, partition, schema-skew`

**Must implement:**

- ERR_RATE_LIMIT_EXCEEDED retries with exponential backoff (initial 1 s, max 60 s) and uniform jitter in [0, interval/2]
- ERR_THROTTLE applies the same backoff as ERR_RATE_LIMIT_EXCEEDED
- ERR_VERSION_INCOMPATIBLE and ERR_BUCKET_NOT_AUTHORIZED do not auto-retry
- ERR_ATTESTATION_REQUIRED triggers fresh IdP attestation acquisition
- ERR_KEY_REVOKED requires a new key bundle from the org admin and permanently invalidates the old node_id
- ERR_EPOCH_MISMATCH triggers epoch snapshot fetch from a peer before retry

**Verification:** Failure-injection harness exercises each error code and confirms the retry handler matches the documented policy.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-28` — QR onboarding payload layout

The QR onboarding payload is a flat byte sequence of bundle_length (uint32 LE), attestation_bundle CBOR bytes, snapshot_length (uint32 LE), and raw snapshot bytes, suitable for QR, NFC, or secure paste transfer.

**Kleppmann:** `P2, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Onboarding encoder emits the four-section layout in the documented order
- Both length fields are 4-byte little-endian uint32
- Decoder reads exactly bundle_length and snapshot_length bytes for the respective sections

**Verification:** Round-trip an onboarding payload through QR encoding and confirm byte-identical decode.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-29` — AttestationBundle structure and signature

An AttestationBundle is a CBOR map carrying issuer_public_key, subject_public_key, role_claims, an Ed25519 (RFC 8032) signature over the deterministic CBOR concatenation of those fields, and an issued_at Unix-seconds timestamp.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Bundle includes issuer_public_key, subject_public_key, role_claims, signature, issued_at
- Signature is computed over issuer_public_key ‖ subject_public_key ‖ role_claims_cbor (deterministic CBOR)
- Verifier validates the signature with Ed25519 against issuer_public_key

**Verification:** Wire-vector 2 in §A.9 produces a verifiable founder self-signed bundle; mutated payloads fail verification.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-30` — Founder vs joiner bundle semantics

Founder bundles are self-signed (issuer_public_key equals subject_public_key) and carry an implicit grant of every role claim accepted only at initial node creation; joiner bundles are signed by the founder or any admin-role holder and verified by the relay during CAPABILITY_NEG.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Relay accepts founder (self-signed) bundles only during initial node creation
- Joiner bundles are issued by founder or any admin-role holder
- Relay verifies issuer signature against issuer_public_key during CAPABILITY_NEG

**Verification:** Re-presenting a founder bundle to an established relay is rejected; a joiner bundle from a non-admin issuer is rejected.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-31` — Relay-side attestation revocation

Attestation bundles have no expiry field; revocation is enforced at the relay by a revocation list keyed on issuer_public_key ‖ subject_public_key, and any revoked bundle produces ERR_KEY_REVOKED regardless of issued_at.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Relay maintains a revocation list keyed on issuer_public_key ‖ subject_public_key
- Revoked bundle attempts produce ERR_KEY_REVOKED on every reconnect
- Bundles have no time-based expiry; only revocation invalidates them

**Verification:** Add a bundle to the revocation list; subsequent CAPABILITY_NEG with that bundle returns ERR_KEY_REVOKED.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-32` — Snapshot hydration with replay fallback

The onboarding snapshot is opaque CRDT-engine serialised state passed directly to the engine's hydration API, and on hydration failure the node must discard the snapshot and request full state transfer via DELTA_STREAM replay from a peer.

**Kleppmann:** `P3` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- New node passes snapshot bytes verbatim to the engine hydration API
- Hydration failure triggers snapshot discard
- Recovery proceeds via DELTA_STREAM replay from a peer

**Verification:** Corrupt the snapshot section; confirm the daemon discards the bundle and initiates DELTA_STREAM replay.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-33` — Two-version rolling-upgrade overlap

HELLO carries both a uint major protocol_version and a supported_versions semver array; the relay must negotiate down to the highest mutually supported version listed in supported_versions rather than rejecting the connection, enabling two-version overlap during rolling upgrades.

**Scope:** `inverted-stack-specific` · **Failure modes:** `schema-skew`

**Must implement:**

- HELLO populates supported_versions with all versions the node can speak
- Relay attempts down-negotiation before returning ERR_VERSION_INCOMPATIBLE
- Negotiated version is the highest version in the intersection of node and relay support

**Verification:** Mixed-version test: nodes with overlapping supported_versions sets connect successfully at the intersection's maximum.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-34` — Minor-version field-stability guarantees

Within the same major protocol_version, message type strings are stable, required fields are not removed, and only optional fields may be added; receivers must apply the unknown-field-ignore rule.

**Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Implementations do not rename type strings within a major version
- Required fields persist across minor versions
- Optional fields can be added; receivers ignore unknown ones

**Verification:** Spec test confirms message type strings and required-field sets match the appendix tables for each released minor version.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-35` — Ed25519 algorithm fixed for signatures

The protocol fixes Ed25519 (RFC 8032) for node identity and attestation signatures with no algorithm agility in the current version; deployments under national algorithm mandates such as GOST R 34.10-2012 must negotiate algorithm selection at a layer above this wire protocol.

**Kleppmann:** `P6` · **Scope:** `inverted-stack-specific`

**Must implement:**

- All node_id keys and attestation signatures use Ed25519
- Implementation does not attempt algorithm negotiation in the wire layer
- Alternative-algorithm deployments handle selection above the wire protocol

**Verification:** Cryptographic test confirms all signatures verify under Ed25519 and no other algorithm appears in conformant traffic.

#### `appendix-a-sync-daemon-wire-protocol:WIRE-36` — Conformance test-vector equivalence

A conformant implementation must produce byte-for-byte equivalent output to the published reference test vectors covering HELLO, CAPABILITY_NEG, ACK, DELTA_STREAM (insert/update/delete), GOSSIP_PING, attestation-bundle signature inputs, and each error code.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Encoder produces byte-identical CBOR to each published vector under deterministic encoding
- Decoder accepts and round-trips each vector without modification
- Test suite is wired into CI to detect drift

**Verification:** Run accelerators/anchor/tests/wire-vectors/ harness; all vectors pass byte-for-byte equivalence.


### Epic: Threat Model Worksheets (appendix-b-threat-model-worksheets)

**Source-paper refs:** v13 §11.1

**Concept count:** 25

#### `appendix-b-threat-model-worksheets:SEC-01` — Asset inventory worksheet

A maintained table enumerating every asset whose compromise, loss, or corruption would cause material harm, classified by sensitivity, location, and owner.

**Kleppmann:** `P6, P7` · **Scope:** `foundational`

**Must implement:**

- Maintain an asset inventory listing CRDT documents, KEKs, DEKs, device keypairs, attestation bundles, sync logs, relay caches, MDM config, and audit logs
- Assign each asset a classification label (Node-secret, Team-secret, Team-confidential, Team-internal, Encrypted)
- Record location, owner, and sensitivity for each asset
- Update the inventory whenever the asset set changes

**Verification:** Repository contains an asset inventory document covering all canonical asset categories with classification, location, owner, and sensitivity columns populated.

#### `appendix-b-threat-model-worksheets:SEC-02` — Asset classification taxonomy

A five-label classification scheme distinguishing Node-secret, Team-secret, Team-confidential, Team-internal, and Encrypted assets by who may know them and how they are protected.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific`

**Must implement:**

- Define the five classification labels with explicit semantics
- Apply exactly one classification label per asset row
- Keep Node-secrets non-transmitted by design
- Protect Team-secrets via the KEK hierarchy

**Verification:** Asset inventory uses only the defined labels; threat-model docs include classification definitions matching the appendix taxonomy.

#### `appendix-b-threat-model-worksheets:SEC-03` — Keystore-binding documentation

A requirement to record which OS keystore protects each Node-secret or Team-secret, naming the platform-specific protection mechanism rather than relying on generic claims of isolation.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Record the OS keystore (Windows Credential Manager + TPM, macOS Keychain + Secure Enclave, Linux libsecret + kernel keyring, Android Keystore, iOS Data Protection) backing each secret
- Verify actual platform security properties rather than relying on vendor marketing

**Verification:** Threat-model document names the keystore protecting each per-platform deployment of secret material.

#### `appendix-b-threat-model-worksheets:SEC-04` — Actor taxonomy worksheet

A maintained table enumerating every actor (benign or adversarial) who could realistically interact with the system, with access level, motivation, and capability level recorded for each.

**Kleppmann:** `P6, P7` · **Scope:** `foundational`

**Must implement:**

- List every actor that interacts or could interact with the system, including adversarial ones
- Record access level, likely motivation, and capability level per actor
- Plan for the actual capability level encountered, not the desired one

**Verification:** Threat-model document contains an actor table with access, motivation, and capability columns populated for each named actor.

#### `appendix-b-threat-model-worksheets:THREAT-01` — External remote attacker

An adversary with no initial access who attempts data theft or ransomware against the deployment from outside the trust boundary.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Treat external remote attackers as an in-scope actor with low-to-high capability range
- Apply network-edge controls and end-to-end encryption to limit remote-attacker reach

**Verification:** Actor taxonomy includes a remote external attacker entry; perimeter and transport controls are documented.

#### `appendix-b-threat-model-worksheets:THREAT-02` — External attacker with physical access

An adversary who obtains physical possession of a node device and attempts credential theft or storage extraction.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Enforce full-disk encryption on every node
- Require device PIN or biometric to unlock keystore-protected material
- Disable hibernation and suspend-to-disk to constrain cold-boot exposure

**Verification:** MDM policy enforces disk encryption, PIN/biometric, and hibernation disable on all enrolled nodes.

#### `appendix-b-threat-model-worksheets:THREAT-03` — Malicious insider with role access

An authorized team member who attempts data exfiltration within the scope of their assigned role.

**Kleppmann:** `P6` · **Scope:** `foundational`

**Must implement:**

- Scope role-based access to the minimum data needed
- Audit role-scoped operations to a tamper-evident log

**Verification:** Role definitions and audit log coverage are documented; role scope is enforced by KEK hierarchy.

#### `appendix-b-threat-model-worksheets:THREAT-04` — Compromised relay operator

A relay operator whose transport-layer position grants ciphertext visibility and traffic-analysis capability but no plaintext access because keys never leave nodes.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise`

**Must implement:**

- Encrypt every sync payload end-to-end before it leaves the node
- Never transmit key material to the relay
- Document relay capability as Limited (ciphertext only)

**Verification:** Wire-protocol implementation encrypts payloads at the node; key-distribution path bypasses the relay.

#### `appendix-b-threat-model-worksheets:THREAT-05` — Relay service termination

The threat that a relay operator withdraws service due to jurisdiction restriction, sanctions, or commercial decision, producing total relay unavailability.

**Kleppmann:** `P3, P5` · **Scope:** `foundational` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- Continue local-node operation when the relay is unreachable
- Continue peer-to-peer sync where peers are reachable without the relay
- Document a relay-replacement path

**Verification:** Disconnect the relay; nodes continue local operation and reachable peer-to-peer sync without degradation.

#### `appendix-b-threat-model-worksheets:THREAT-06` — Former team member

A previously authorized member whose future access is blocked by key rotation but whose historical-data exposure remains scoped by the data-at-risk calculation.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Rotate KEKs on departure to block future access
- Compute and document the historical exposure scope per the data-at-risk calculation
- Distinguish remediated future access from unremediated prior exfiltration in incident records

**Verification:** Offboarding runbook triggers KEK rotation and logs a data-at-risk computation for the affected role.

#### `appendix-b-threat-model-worksheets:THREAT-07` — Compromised IdP

An identity provider whose signing key is under adversary control, allowing fraudulent role attestations that bypass the attestation trust anchor.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Detect IdP compromise and rotate the IdP signing key
- Re-issue role attestations after IdP signing-key rotation

**Verification:** IdP-compromise runbook exists naming detection signals and the signing-key rotation procedure.

#### `appendix-b-threat-model-worksheets:THREAT-08` — Supply chain attacker

An adversary who compromises the build pipeline to ship a backdoored binary capable of exfiltrating keys or plaintext from inside the trust boundary.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Sign commits and protect source branches
- Produce reproducible builds with SBOM verification
- Sign binaries with hardware-backed code-signing keys
- Verify package manifest signatures on install

**Verification:** Build pipeline produces signed reproducible artifacts; SBOM and signature verification are gating steps in distribution.

#### `appendix-b-threat-model-worksheets:THREAT-09` — Government authority and regulatory body

A statutory actor with legal compulsion power (warrant, subpoena, administrative order, inspection notice, device seizure) whose architectural mitigation is end-to-end encryption with local key management so that compelled relay inspection yields ciphertext only.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, key-compromise`

**Must implement:**

- Hold all key material at the node so the relay can yield only ciphertext under compelled inspection
- Document the regulatory basis (Schrems II, PIPL, 242-FZ, DIFC, UAE DPL, RBI, POPIA, NDPR, PIPA) for each market the team operates in
- Treat device-present credentials as the boundary of device-seizure exposure

**Verification:** Architecture proves keys never reach the relay; legal-response runbook lists applicable jurisdictional authorities and the architectural response.

#### `appendix-b-threat-model-worksheets:SEC-05` — Capability-level taxonomy

A four-level scale (Low, Medium, High, Limited) rating an actor's technical sophistication and structural access constraints, used to size mitigations.

**Scope:** `foundational`

**Must implement:**

- Assign each actor exactly one of Low, Medium, High, or Limited
- Use Limited only when access is structurally constrained (e.g., ciphertext-only)

**Verification:** Actor taxonomy entries each carry one of the four defined capability levels.

#### `appendix-b-threat-model-worksheets:SEC-06` — Per-vertical worksheet customization

A requirement that each deployment add asset rows and actor rows specific to its vertical (healthcare, legal, government, defense, regulated finance) before the worksheet is treated as complete.

**Kleppmann:** `P6` · **Scope:** `foundational`

**Must implement:**

- Extend the asset inventory with vertical-specific assets before first deployment
- Extend the actor taxonomy with vertical-specific adversaries before first deployment
- Document jurisdiction-specific inspection rights for regulated markets

**Verification:** Per-deployment threat model includes vertical-specific additions beyond the template baseline.

#### `appendix-b-threat-model-worksheets:SEC-07` — Attack tree per worksheet

A branch-by-branch decomposition of a primary threat scenario, naming each control checkpoint and its mitigation, and identifying the residual risk where controls do not fully cover the branch.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Walk the highest-probability threat scenario branch by branch
- Name the mitigation that defeats each branch
- Identify and label residual risk that mitigations do not cover

**Verification:** Threat-model document contains at least one named attack tree with explicit mitigations and a residual-risk note.

#### `appendix-b-threat-model-worksheets:MITIG-01` — MDM-enforced device hardening

An MDM-enforced configuration baseline requiring full-disk encryption, minimum 6-digit PIN, disabled USB boot, locked BIOS settings, and disabled hibernation/suspend-to-disk on every node before it joins the sync mesh.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Enforce full-disk encryption (e.g., BitLocker on Windows) via MDM compliance policy
- Require minimum 6-digit PIN through MDM
- Disable USB boot and lock BIOS settings changes
- Disable hibernation files and suspend-to-disk images via MDM
- Block sync-mesh enrollment until MDM compliance is confirmed

**Verification:** MDM policy file enforces all five controls; nodes failing compliance cannot complete sync-mesh handshake.

#### `appendix-b-threat-model-worksheets:MITIG-02` — Self-hosted relay for traffic-analysis sensitivity

Deployment of a relay inside the team's own trust boundary so that traffic-pattern observation moves from an external operator to internal IT.

**Kleppmann:** `P3, P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `vendor-outage`

**Must implement:**

- Provide a deployable self-hosted relay artifact
- Document the operational requirements for internal-IT relay hosting

**Verification:** Relay distribution includes a self-hosted deployment package and operations guide.

#### `appendix-b-threat-model-worksheets:SEC-08` — Key-compromise detection checklist

A standing list of triggers (theft, anomalous audit-log access, credential leak, threat-intel hit, IdP failures, offboarding, abnormal sync-state inconsistency, lawful access demand) that initiate the re-keying procedure on suspicion rather than on confirmation.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Initiate re-keying on suspicion, not on confirmation
- Cover all eight named trigger categories in the detection checklist
- Distinguish infrastructure-failure WAL replay from sync-state inconsistency that signals a security event
- Engage legal counsel before responding to lawful access demands

**Verification:** Incident-response runbook contains a detection checklist with the eight named triggers and an explicit suspicion-not-confirmation directive.

#### `appendix-b-threat-model-worksheets:SEC-09` — Re-keying procedure

An ordered seven-step procedure (with a 1a recovery branch) that generates a fresh KEK, re-wraps DEKs, discards the old KEK, broadcasts revocation, forces re-authentication, notifies users, and re-issues wrapped KEK copies, each step having a named owner and completion condition.

**Kleppmann:** `P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-compromise, key-loss`

**Must implement:**

- Generate a new KEK from cryptographically random material, never derived from the compromised KEK
- Check old-KEK availability before attempting re-wrap; document unrecoverable scope when the old KEK is gone
- Re-wrap every recoverable DEK in scope under the new KEK
- Discard old KEK copies and verify with keystore audit
- Broadcast revocation through the relay so reconnecting nodes receive ERR_KEY_REVOKED
- Notify all affected role members with KEK creation date, revocation date, and accessible-data scope
- Re-issue wrapped KEK copies to current authorized members through the standard distribution path

**Verification:** Incident-response runbook lists the seven steps with owners and completion conditions; relay protocol implements the ERR_KEY_REVOKED handshake response.

#### `appendix-b-threat-model-worksheets:SEC-10` — Unrecoverable-KEK contingency (Step 1a)

The branch of the re-keying procedure executed when the old KEK cannot be retrieved, in which DEKs wrapped under the lost KEK are declared permanently inaccessible, the loss scope is documented, revocation is still broadcast, and the team chooses between BYOC backup reconstruction or accepted loss.

**Kleppmann:** `P5, P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `key-loss`

**Must implement:**

- Detect old-KEK unavailability before attempting Step 2
- Document the scope of unrecoverable data in the incident log
- Skip directly to revocation broadcast to prevent further compromise
- Surface the reconstruct-from-BYOC-backup vs accept-loss decision to the team

**Verification:** Runbook explicitly handles the unrecoverable-KEK branch with a documented decision point and incident-log entry requirement.

#### `appendix-b-threat-model-worksheets:SEC-11` — Data-at-risk scope calculation

A bounded calculation of compromise exposure defined by the compromised KEK's keystore creation date as start, the relay-confirmed revocation date as end, and the documents the KEK protected within that window as scope, with documents outside that role or created after revocation explicitly excluded.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Use the keystore creation timestamp as the start date, not employee recollection
- Use the relay-confirmed revocation timestamp as the end date
- Enumerate all documents the compromised KEK protected within the window
- Exclude documents in unaffected roles and documents created after the revocation date

**Verification:** Incident-response output contains a data-at-risk calculation with documented start, end, scope, and exclusions.

#### `appendix-b-threat-model-worksheets:SEC-12` — User notification template and 90-day retention floor

A standardized affected-user notification recording recipient, channel, and timestamp, retained for a minimum of 90 days as an audit-log retention floor distinct from regulatory breach-notification deadlines.

**Kleppmann:** `P6` · **Scope:** `foundational` · **Failure modes:** `key-compromise`

**Must implement:**

- Send the templated notification to every member of the affected role
- Log timestamp, channel, and recipient for each notification
- Retain notification records for at least 90 days

**Verification:** Audit log contains notification records with the three required fields and a retention policy of at least 90 days.

#### `appendix-b-threat-model-worksheets:COMP-01` — Jurisdictional breach notification SLA matrix

A matrix mapping each operating jurisdiction to its supervisor-notification window and data-subject-notification window, against which the incident-response SLA is set to the shortest applicable window.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, key-compromise`

**Must implement:**

- Verify and record the supervisor-notification window for each jurisdiction the team operates in
- Verify and record the data-subject-notification window for each jurisdiction
- Set the incident-response SLA against the shortest applicable window
- Treat the GDPR 72-hour window as the shortest common denominator unless a stricter window applies

**Verification:** Compliance documentation contains a jurisdiction matrix and an incident SLA equal to the shortest listed window.

#### `appendix-b-threat-model-worksheets:COMP-02` — Pre-deployment regulatory validation

A pre-production requirement to validate, for every market the team operates in, the breach notification window, retention floor, regulatory inspection rights, and cross-border data transfer rules under the applicable regional frameworks.

**Kleppmann:** `P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection`

**Must implement:**

- Identify the applicable regulatory frameworks for each operating market
- Validate breach notification window, retention floor, inspection rights, and cross-border transfer rules per market
- Complete validation before first production deployment

**Verification:** Pre-deployment compliance checklist documents the four validations per operating market.


### Epic: Further Reading (appendix-c-further-reading)

**Concept count:** 8

#### `appendix-c-further-reading:READ-01` — Kleppmann seven local-first ideals

The seven aspirational properties — fast local performance (P1), multi-device access (P2), network-optional operation (P3), seamless collaboration (P4), longevity beyond vendor lifespan (P5), security and privacy by default (P6), and ultimate user ownership (P7) — that together define local-first software per Kleppmann et al. (Onward! 2019).

**Kleppmann:** `P1, P2, P3, P4, P5, P6, P7` · **Scope:** `foundational`

**Must implement:**

- System satisfies all seven Kleppmann properties P1-P7 measurably
- Each property has a verification test in the conformance suite
- Trade-offs against any property are documented in an ADR

**Verification:** Conformance scorecard maps every architectural choice to one or more of P1-P7; no property is left unaddressed.

> This is the canonical reference the entire book and conformance scorecard are organized around.

#### `appendix-c-further-reading:READ-02` — CRDT convergent vs commutative distinction

The Shapiro et al. 2011 distinction between state-based (convergent) CRDTs that ship full state and operation-based (commutative) CRDTs that ship operation logs, which determines what is carried across the sync wire.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- CRDT engine selection documents whether it is state-based, op-based, or delta-based
- Wire protocol matches the engine's replication model
- Merge semantics are deterministic and provably convergent

**Verification:** ADR exists naming the chosen CRDT type family (CvRDT, CmRDT, or delta-CRDT) with citation to Shapiro 2011.

#### `appendix-c-further-reading:READ-03` — Flexible Paxos quorum intersection

The Howard, Malkhi, and Spiegelman 2016 result that read and write quorums in a consensus protocol need only intersect, not be identical, which underpins the relaxed quorum assumptions in distributed lease protocols such as Flease.

**Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Any CP-mode quorum protocol documents its read and write quorum sizes
- Quorum intersection property is provably maintained under reconfiguration

**Verification:** ADR for any consensus or lease protocol cites Flexible Paxos and states quorum sizes.

#### `appendix-c-further-reading:READ-04` — CAP theorem as architectural constraint

The Brewer (2000) conjecture and Gilbert-Lynch (2002) proof that a distributed system cannot simultaneously guarantee consistency, availability, and partition tolerance, which forces every zone in the architecture to be classified as either AP or CP.

**Kleppmann:** `P3` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Every architectural zone is classified as AP or CP in writing
- The classification is justified against partition behavior
- User-facing degradation under partition matches the stated classification

**Verification:** Each zone's ADR states AP or CP and describes observable behavior under network partition.

#### `appendix-c-further-reading:READ-05` — Optimistic replication semantics

The Saito and Shapiro 2005 framing of replication that allows tentative local commits, eventual convergence, and application-level conflict resolution — the academic vocabulary for what the book operationally calls local-first.

**Kleppmann:** `P1, P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Local writes commit tentatively without coordination
- Convergence is eventual across all reachable peers
- Conflict resolution is specified per data type

**Verification:** Behavioral test confirms a local write commits and is visible to the local reader before any peer acknowledges it.

#### `appendix-c-further-reading:READ-06` — Lamport logical time

Lamport's 1978 construction of logical clocks and the happens-before relation, which is the basis for the vector clocks the Appendix A wire protocol uses to order events across peers without relying on wall-clock time.

**Kleppmann:** `P4` · **Scope:** `foundational` · **Failure modes:** `clock-skew, partition`

**Must implement:**

- Sync wire protocol carries logical time (vector clock or equivalent), not wall-clock time
- Causal ordering of events is preserved across peers
- Clock skew between peers does not affect correctness

**Verification:** Wire protocol specification names its logical-time scheme; partition test confirms causal order is preserved after heal.

#### `appendix-c-further-reading:READ-07` — Cambria lens-based schema evolution

The Ink and Switch Cambria abstraction (2021) of bidirectional lenses that translate documents between schema versions N and N+1 without data loss, which is the conceptual foundation for the Chapter 13 schema migration approach.

**Kleppmann:** `P2, P5` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Schema migrations are expressed as bidirectional lenses, not destructive ALTER operations
- Each lens is reversible to preserve backward compatibility across heterogeneous fleets
- Old-version peers continue to read new-version documents through lens application

**Verification:** Schema migration tests demonstrate round-trip lens application preserves data on a fleet running mixed schema versions.

#### `appendix-c-further-reading:READ-08` — Vendor dependency risk as empirical case

The composite 2022 record of Western SaaS providers suspending, restricting, or terminating service across Russia, Belarus, and adjacent CIS markets, treated by the book as the empirical case study justifying the local-first thesis against vendor dependency.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `vendor-acquisition, vendor-outage`

**Must implement:**

- Architecture has no single vendor whose unilateral action can revoke customer access to their own data
- Core operations continue when any one external vendor terminates service
- Data export from any vendor-managed component is possible at any time without vendor cooperation

**Verification:** Tabletop exercise confirms that simulated termination of any single vendor does not block customer access to their own data.


### Epic: Testing the Inverted Stack (appendix-d-testing-the-inverted-stack)

**Source-paper refs:** v13 §15

**Concept count:** 14

#### `appendix-d-testing-the-inverted-stack:TEST-01` — Five-level testing pyramid

A tiered test architecture in which CRDT property tests, real-dependency integration tests, fault injection, deterministic simulation, and chaos testing each run at a defined cadence with mandatory pass conditions before first production release.

**Kleppmann:** `P3, P4, P5, P6` · **Scope:** `foundational` · **Failure modes:** `clock-skew, key-compromise, key-loss, partition, peer-discovery-failure, replay, schema-skew`

**Must implement:**

- Levels 1 and 2 execute on every pull request
- Level 3 fault injection executes nightly
- Level 4 deterministic simulation executes weekly or per release candidate
- Level 5 chaos executes in staging before each major release
- Each scenario specifies setup, action, and a pass/fail condition

**Verification:** CI configuration shows distinct jobs for each level with the prescribed triggers and time budgets, and every scenario in the suite carries an explicit pass condition.

#### `appendix-d-testing-the-inverted-stack:TEST-02` — Property-based CRDT tests for convergence, idempotency, commutativity, and monotonicity

A Level 1 test class in which a property-based framework generates thousands of random operation sequences to verify that CRDT merge satisfies convergence, idempotency, commutativity (or join-semilattice merge for state-based CRDTs), and monotonicity.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition`

**Must implement:**

- Use FsCheck (.NET) or fast-check (JavaScript) or equivalent property-based framework
- Generate at least 10,000 random operation sequences per property per test run
- Assert convergence, idempotency, commutativity, and monotonicity as separate properties
- Report the minimal failing sequence on violation

**Verification:** Test suite output shows at least 10,000 generated cases per CRDT property, with shrinking enabled and named property assertions distinct from example-based tests.

#### `appendix-d-testing-the-inverted-stack:TEST-03` — Real-daemon integration tests via Testcontainers

A Level 2 test class that exercises the full sync handshake (HELLO, CAPABILITY_NEG, ACK, DELTA_STREAM, GOSSIP_PING) against a real local-node process spun up via Testcontainers, asserting on resulting CRDT state rather than wire messages.

**Kleppmann:** `P3, P4` · **Scope:** `inverted-stack-specific` · **Failure modes:** `peer-discovery-failure`

**Must implement:**

- Spin up a real local-node instance per test suite using Testcontainers
- Execute the full five-step handshake end to end
- Assert on post-exchange CRDT state, not on wire message sequences
- Forbid mocking the sync daemon for integration coverage

**Verification:** Integration test fixtures launch a containerized node, complete the handshake, and assertions reference CRDT state hashes; CI environment provides Docker.

#### `appendix-d-testing-the-inverted-stack:TEST-04` — Fault injection for partition, packet loss, and crash

A Level 3 test class that uses a network proxy such as toxiproxy with Testcontainers to inject node crashes mid-handshake, relay unreachability during DELTA_STREAM, and consecutive GOSSIP_PING losses, then asserts the system recovers to a CRDT state identical to the no-fault outcome.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `partition, peer-discovery-failure`

**Must implement:**

- Inject a node crash mid-handshake and assert peer recovery to consistent state
- Make the relay unreachable during DELTA_STREAM and assert sender queues and retransmits on reconnect
- Drop three consecutive GOSSIP_PING intervals and assert degraded-but-consistent recovery without manual intervention
- Pass condition for every scenario is byte-identical recovered state, not absence of crash

**Verification:** Nightly CI job runs each fault scenario through toxiproxy and asserts post-recovery CRDT hash equals the no-fault baseline.

#### `appendix-d-testing-the-inverted-stack:TEST-05` — Deterministic simulation harness with virtual clock and message scheduler

A Level 4 in-process test harness that boots N node instances under a controllable virtual clock and a deterministic message scheduler, enabling exhaustive coverage of mixed-version sync, offline epoch transitions, and Flease edge cases that real-time tests cannot reach reliably.

**Kleppmann:** `P3, P4, P5` · **Scope:** `inverted-stack-specific` · **Failure modes:** `clock-skew, partition, schema-skew`

**Must implement:**

- Provide a global monotonic virtual clock advanced in discrete ticks by the test driver
- Provide a pluggable scheduler that can delay, reorder, or drop messages per test
- Boot N node instances in-process, each with an isolated SQLCipher store, wired to the scheduler instead of real sockets
- Provide invariant assertion hooks for CRDT convergence, ledger balance, lease exclusivity, and epoch monotonicity
- Design the harness against the Appendix A wire protocol specification before implementation

**Verification:** Repository contains a simulation harness whose tests resolve all timeouts against the virtual clock and pass deterministically on repeated runs with the same seed.

#### `appendix-d-testing-the-inverted-stack:TEST-06` — Chaos testing in staging under representative load

A Level 5 test class that runs Pumba, Gremlin, or equivalent chaos tooling against a multi-node staging environment loaded at median-production traffic, with the explicit goal of discovering unanticipated failure modes rather than verifying known properties.

**Kleppmann:** `P3, P4` · **Scope:** `foundational` · **Failure modes:** `clock-skew, partition, peer-discovery-failure`

**Must implement:**

- Operate a permanent multi-node staging environment representative of production
- Apply process kill, latency injection, node-offline flips, and link-corruption chaos
- Sustain median-production load throughout chaos runs
- Document every observed anomaly, whether or not it manifests as a visible failure

**Verification:** Pre-major-release pipeline executes a 24–48 hour chaos run with logged anomalies and recovery times, archived against the release tag.

#### `appendix-d-testing-the-inverted-stack:TEST-07` — CRDT growth tests for bounded resource use

A weekly and pre-release test class that simulates median-vertical usage at 30, 90, and 365 day horizons and measures CRDT document size to verify the system stays within its configured storage budget, that compaction reduces size when fired, and that per-shard size stays below the shallow snapshot threshold.

**Kleppmann:** `P1, P5` · **Scope:** `foundational`

**Must implement:**

- Simulate median-activity usage at 30, 90, and 365 day horizons
- Assert 365-day document size stays within the configured storage budget (default 10 GB per node)
- Assert library-level compaction measurably reduces size when its threshold is reached
- Assert per-shard size stays below the shallow snapshot threshold and shallow mode activates correctly when crossed

**Verification:** Weekly CI job runs the growth simulation and emits per-horizon size metrics that the build gate compares to budget thresholds.

#### `appendix-d-testing-the-inverted-stack:TEST-08` — Mandatory partition and reconnect scenarios

A required scenario set covering 30-day offline divergence with merge, 90-day extended-offline baseline with intermittent windows, CP quorum loss, 1,000+ queued operations on standard and constrained hardware, abrupt power interruption during WAL write, and 30-day air-gapped operation, each with explicit pass conditions before first production release.

**Kleppmann:** `P3, P4, P5, P7` · **Scope:** `foundational` · **Failure modes:** `partition, peer-discovery-failure`

**Must implement:**

- Two nodes diverge offline for 30 simulated days then merge with no data loss to identical CRDT state
- Sustain 90 simulated days of offline operation with daily 10-minute sync windows and no operation loss
- Block CP writes under quorum loss with a clear unavailable indicator and no silent drop
- Apply 1,000+ queued operations on reconnect without timeout, OOM, or duplication, on both standard and 2 GB RAM / 16 GB storage hardware
- SIGKILL during WAL write at random byte offsets 100+ times with full recovery and no partial-as-committed records
- Operate air-gapped for 30 simulated days with zero relay egress packets recorded in the network log

**Verification:** Test report archives per-scenario pass/fail with CRDT state dumps, network captures showing zero relay traffic during air-gap, and recovery logs after each WAL kill.

#### `appendix-d-testing-the-inverted-stack:TEST-09` — Schema migration scenarios across version skew

A required scenario set covering N-to-N-1 bidirectional sync via lenses, offline epoch transition recovery without manual intervention, and the couch-device case where a node lagging 3+ major versions is rejected at capability negotiation rather than migrated lossily.

**Kleppmann:** `P5, P7` · **Scope:** `foundational` · **Failure modes:** `schema-skew`

**Must implement:**

- Exchange CRDT deltas between schema N and schema N-1 nodes with bidirectional lens translation and no data loss
- Allow an offline node to download the post-transition epoch snapshot and resume sync without operator intervention
- Reject capability negotiation with ERR_VERSION_INCOMPATIBLE when the schema gap exceeds the configured maximum
- Encode the maximum auto-bridged schema gap as an explicit policy and test the boundary

**Verification:** Test suite includes mixed-version pairs, an offline-during-epoch fixture, and an over-gap connection attempt asserting the precise error code and update prompt.

#### `appendix-d-testing-the-inverted-stack:TEST-10` — Flease edge case scenarios

A required scenario set covering CP lease holder crash mid-write (partial write quarantined and visible, lease re-acquired by a peer after timeout) and partition during lease negotiation (both sides identify no-quorum and block writes with no split-brain).

**Kleppmann:** `P4, P6` · **Scope:** `inverted-stack-specific` · **Failure modes:** `partition`

**Must implement:**

- On lease holder crash mid-write, expire the lease after the configured timeout (default 30 seconds) and let a peer acquire a new lease
- Quarantine partial writes from a crashed lease holder and surface them for operator review rather than silently merging
- Under partition during CAPABILITY_NEG lease request, have both partitions independently report no-quorum and block writes with no split-brain

**Verification:** Test injects each scenario and asserts the partial write appears in a quarantine queue, lease ownership transfers cleanly, and no two partitions claim the lease concurrently.

#### `appendix-d-testing-the-inverted-stack:TEST-11` — Security scenarios for encryption, key rotation, and audit

A required scenario set producing regulator-grade evidence covering SQLCipher unreadability without keys, post-rotation key revocation, historical document re-keying under a new KEK, data-boundary negative tests with relay disabled, relay-operator inability to decrypt, attestation revocation, and tamper-evident audit trail completeness.

**Kleppmann:** `P5, P6, P7` · **Scope:** `foundational` · **Failure modes:** `key-compromise, key-loss, replay`

**Must implement:**

- Verify a copied SQLCipher file is unreadable without the encryption key
- Verify a revoked member receives ERR_KEY_REVOKED and cannot decrypt documents written after rotation
- Re-wrap all DEKs from KEK version K to K+1 with no document accessible under the old KEK and all accessible under the new
- Capture full network egress while relay is disabled and assert zero relay-destination packets
- Capture all relay-transiting bytes and verify ciphertext cannot be decrypted with relay-side keys alone
- Reject attestation bundles whose issuer appears on the revocation list with ERR_KEY_REVOKED and a logged audit entry
- Verify the audit log holds every operation in strict monotonic sequence with a passing tamper-evidence integrity check

**Verification:** Per-scenario evidence column captures packet captures, audit log exports with verified Merkle root, relay log entries with issuer fingerprint, and ciphertext samples — archived per release.

#### `appendix-d-testing-the-inverted-stack:TEST-12` — Ledger invariant scenarios under failure and duplication

A required scenario set asserting that the sum-to-zero ledger invariant holds across the complete account set after a posting-node crash and retry, and that idempotency keys prevent duplicate postings when an identical domain event is submitted twice.

**Kleppmann:** `P4` · **Scope:** `foundational` · **Failure modes:** `partition, replay`

**Must implement:**

- Verify exactly one posting set exists after a mid-transaction crash and retry, with no duplicate postings
- Verify sum-to-zero across the full related-account set, not only directly involved accounts
- Verify idempotency keys cause a duplicate domain event to produce exactly one set of postings

**Verification:** Test sums the ledger across all related accounts after each scenario and asserts a single posting set keyed by the idempotency token.

#### `appendix-d-testing-the-inverted-stack:TEST-13` — Tiered CI configuration with archived test artefacts

A four-tier CI configuration (per-PR, nightly, weekly/RC, pre-major-release) that gates merges on L1+L2, runs L3 nightly, executes L4 simulation weekly or per RC, and runs L5 chaos before major releases, with archived test report, scenario evidence, harness configuration, and SBOM per release.

**Kleppmann:** `P5, P6` · **Scope:** `foundational`

**Must implement:**

- Gate every PR merge on L1 (<5 min) and L2 (<15 min) tests
- Run L3 nightly within a 2-hour budget with P1 incident on failure
- Run L4 simulation weekly and on RC tags, blocking the RC on failure
- Run L5 chaos for 24–48 hours before major release on a permanently maintained representative staging environment
- Capture and archive per-release test report, scenario evidence, harness configuration, and SBOM tied to the release version and code SHA

**Verification:** CI definitions show four named tiers with the prescribed triggers, time budgets, and artefact-upload steps producing an archive linked to each release tag.

#### `appendix-d-testing-the-inverted-stack:TEST-14` — Accessibility test for sync-state announcements

A test scenario asserting that sync-state transitions (sync-healthy, stale, offline, conflict-pending, revocation) are exposed through the platform accessibility tree (aria-live on web, UIAccessibilityTraits on iOS, AccessibilityNodeInfo on Android) and announced on change.

**Kleppmann:** `P4` · **Scope:** `foundational`

**Must implement:**

- Expose every sync-state value through the platform accessibility tree on each supported platform
- Fire a state-change announcement on every sync-state transition
- Forbid communicating sync state through colour or icon alone

**Verification:** UI test triggers each sync-state transition and asserts the platform accessibility API receives the corresponding announcement on web, iOS, and Android targets.


### Epic: Citation Style (appendix-e-citation-style)

**Concept count:** 1

#### `appendix-e-citation-style:DOC-01` — Compliance citations verified against primary sources

Every legal decision, statute, and regulation cited in support of a compliance claim must be checked against the primary source (case docket, official journal, enacting body) before publication.

**Scope:** `inverted-stack-specific`

**Must implement:**

- Reference implementation documentation cites compliance claims with verifiable primary-source references (case number, regulation number with publication date, statute act number)
- Each cited legal/regulatory source resolves to an authoritative URL or print citation, not a secondary summary
- A citation-audit step in the documentation build verifies every legal/regulatory reference resolves before release

**Verification:** Documentation build includes a citation-audit step that checks every legal-decision, statute, and regulation reference resolves to a primary source; build fails on broken or secondary-only references.

> Architectural relevance is indirect — supports the credibility of compliance claims that the reference implementation must back up (see Appendix F and Ch15/Ch19). All other appendix content (in-text bracket format, reference-list templates) is editorial and not extracted.


### Epic: Regulatory Coverage Map (appendix-f-regulatory-coverage)

**Concept count:** 15

#### `appendix-f-regulatory-coverage:COMP-01` — GDPR Article 17 right-to-erasure via crypto-shredding

An EU-mandated individual right to erasure that local-first architectures answer by destroying the per-record DEK so encrypted CRDT history becomes unrecoverable, with the lawfulness of crypto-shred-as-erasure remaining unsettled across CNIL and German DPAs.

**Kleppmann:** `P5, P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, key-loss`

**Must implement:**

- Per-record or per-tenant DEKs are independently destroyable
- Operator documentation describes the crypto-shred procedure as the Article 17 mechanism
- Residual CRDT metadata (operation IDs, timestamps, DAG position) is enumerated for jurisdictional review
- Legal review precedes any production reliance on crypto-shred for Article 17 responses

**Verification:** After erasure, the targeted record's ciphertext remains but no DEK path exists to decrypt it; an ADR documents the chosen erasure mechanism and its jurisdictional caveats

#### `appendix-f-regulatory-coverage:COMP-02` — GDPR Article 30 records-of-processing at the node level

A GDPR requirement that processing activities be logged in a controller-accessible record, satisfied in local-first architectures by per-node processing logs rather than centralized SaaS audit trails.

**Kleppmann:** `P5, P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection`

**Must implement:**

- Each node maintains a processing record covering purpose, categories of data, and retention
- Records are exportable for controller and DPA inspection
- The 72-hour Article 33 breach-notification window is the shortest assumed deadline absent stricter local rules

**Verification:** A node export produces an Article-30-compliant processing record without requiring vendor cooperation

#### `appendix-f-regulatory-coverage:COMP-03` — Schrems II structural answer via no cross-border transfer

The CJEU C-311/18 ruling invalidating Privacy Shield and constraining SCCs is bypassed structurally when a local-first node never exports personal data to a foreign cloud, removing the transfer mechanism the ruling evaluates.

**Kleppmann:** `P3, P5, P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection`

**Must implement:**

- Personal data of EEA subjects never leaves EEA-resident nodes during normal operation
- Sync relays for EEA tenants terminate within EEA jurisdiction
- The deployment topology is documented sufficient to assert no cross-border transfer occurs

**Verification:** A traffic-flow diagram and a deployment audit show no PII egress from EEA-resident nodes to non-adequate jurisdictions

#### `appendix-f-regulatory-coverage:COMP-04` — DIFC DPL 2020 categorical foreign-cloud prohibition

A DIFC-jurisdiction rule prohibiting DIFC-licensed financial entities from routing personal data through offshore cloud infrastructure, satisfied at the architectural level by a local-first node that never traverses an offshore cloud.

**Kleppmann:** `P3, P5, P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection`

**Must implement:**

- DIFC-tenant nodes route personal data only through infrastructure inside the permitted jurisdiction
- Sync paths and relay endpoints for DIFC tenants are independently auditable
- The deployment topology documents which components are inside DIFC and which are not

**Verification:** A network-egress test for a DIFC tenant shows no personal data leaving permitted infrastructure under any operational condition including degraded sync

#### `appendix-f-regulatory-coverage:COMP-05` — UAE Federal DPL 2022 Article 16 erasure right

A UAE federal data protection rule establishing an Article 16 erasure right for processing outside DIFC and ADGM, carrying the same crypto-shredding sufficiency tension as GDPR Article 17.

**Kleppmann:** `P5, P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, key-loss`

**Must implement:**

- Erasure mechanism for UAE federal-jurisdiction tenants is the same crypto-shred path as GDPR Article 17
- Documentation distinguishes UAE federal tenancy from DIFC-licensed tenancy

**Verification:** A UAE federal tenant erasure request produces the same crypto-shred audit artifacts as a GDPR Article 17 request

#### `appendix-f-regulatory-coverage:COMP-06` — India DPDP Act 2023 Section 12 erasure rights

India's omnibus data protection statute establishes a Section 12 erasure right parallel to GDPR Article 17, with implementing rules pending and BFSI deployments layered with the RBI localization circular.

**Kleppmann:** `P5, P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, key-loss`

**Must implement:**

- DPDP-jurisdiction tenants receive the same crypto-shred erasure path as GDPR Article 17
- BFSI tenancy is segregated from non-BFSI to allow stricter residency enforcement

**Verification:** A DPDP Section 12 erasure request produces a documented crypto-shred audit trail for the targeted record

#### `appendix-f-regulatory-coverage:COMP-07` — RBI 2018 hard payment-data localization

A Reserve Bank of India circular requiring all payment-related data of Indian payment-system operators to be stored exclusively within India, treated as a Tier 3 architectural driver rather than a design preference.

**Kleppmann:** `P3, P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection`

**Must implement:**

- Payment-related personal data for RBI-scoped tenants is stored only on India-resident nodes
- Sync relays carrying RBI-scoped data terminate within India
- The deployment topology distinguishes payment data from non-payment data scope

**Verification:** An infrastructure inventory shows every node and relay handling RBI-scoped data resides within India

#### `appendix-f-regulatory-coverage:COMP-08` — Russia Federal Law 242-FZ initial-collection localization

The 2015 amendment to Federal Law 152-FZ requiring personal data of Russian citizens to be initially collected and stored on servers physically located in Russia, predating GDPR and establishing the doctrinal pattern of hard territorial mandates that local-first satisfies architecturally.

**Kleppmann:** `P3, P5, P6, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection`

**Must implement:**

- Initial collection of Russian-citizen personal data targets Russia-resident nodes
- Subsequent processing nodes outside Russia receive only data already domiciled inside Russia
- The deployment topology identifies which nodes are inside the Russian Federation

**Verification:** A data-flow trace for a Russian-citizen record shows initial write to a Russia-resident node before any cross-border replication

#### `appendix-f-regulatory-coverage:COMP-09` — China PIPL plus MLPS 2.0 strict cross-border restriction

PIPL Article 47 erasure rights combined with MLPS 2.0 security classification create one of the strictest cross-border transfer regimes globally, generally requiring personal data of Chinese residents to remain inside China.

**Kleppmann:** `P3, P5, P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, key-loss`

**Must implement:**

- Chinese-resident-tenant nodes are domiciled within mainland China
- Cross-border egress of PIPL-scoped personal data is gated by documented legal basis
- Erasure mechanism for PIPL-scoped tenants is the same crypto-shred path as GDPR Article 17
- MLPS 2.0 classification level is recorded for each China-resident deployment

**Verification:** A China-tenant deployment audit confirms node residency, MLPS classification, and absence of unauthorized cross-border egress

#### `appendix-f-regulatory-coverage:COMP-10` — Japan APPI Article 36 cross-border consent and erasure

The 2022-revised Japanese APPI introduces Article 36 cross-border transfer consent and an erasure-equivalent right that inherits the same CRDT-history-versus-DEK-destruction tension as GDPR Article 17.

**Kleppmann:** `P5, P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, key-loss`

**Must implement:**

- Cross-border transfer of APPI-scoped data records consent provenance per data subject
- Erasure mechanism for APPI-scoped tenants is the same crypto-shred path as GDPR Article 17

**Verification:** A Japan-tenant erasure request produces a crypto-shred audit trail and any cross-border transfer carries an attached consent record

#### `appendix-f-regulatory-coverage:COMP-11` — South Korea PIPA plus ISMS-P procurement certification

South Korea's PIPA establishes erasure rights and ISMS-P functions as a procurement-required certification that the local-first vendor must produce alongside SOC 2 and ISO 27001 documentation.

**Kleppmann:** `P5, P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection`

**Must implement:**

- Korean-tenant erasure path matches the GDPR Article 17 crypto-shred mechanism
- ISMS-P artifacts are produced as part of the compliance-packaging deliverable for Korean enterprise procurement

**Verification:** An ISMS-P artifact exists in the procurement-evidence bundle and an erasure dry-run produces a PIPA-suitable audit trail

#### `appendix-f-regulatory-coverage:COMP-12` — Africa parallel mandates (NDPA, POPIA, Kenya DPA)

A coherent set of African data-protection statutes (Nigeria NDPA 2023, South Africa POPIA Sections 24 and 72, Kenya DPA 2019 Section 40) establishing erasure rights and cross-border transfer prohibitions to non-adequate countries that mirror the GDPR structural argument for on-device residency.

**Kleppmann:** `P5, P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection`

**Must implement:**

- Erasure path for African-jurisdiction tenants matches the GDPR Article 17 crypto-shred mechanism
- Cross-border transfers from POPIA-scoped tenants verify destination adequacy under Section 72
- Sectoral BFSI and telecom localization obligations are identified per tenant

**Verification:** A POPIA Section 72 transfer review and a per-tenant sectoral-obligation register exist and are kept current

#### `appendix-f-regulatory-coverage:COMP-13` — LATAM erasure-rights cluster (LGPD, LFPDPPP ARCO)

A Latin American cluster of statutes (Brazil LGPD Article 18, Mexico LFPDPPP ARCO cancellation right, Colombia Ley 1581, Argentina Ley 25.326) establishing erasure rights parallel to GDPR Article 17 with the ANPD's stance on crypto-shredding still unsettled.

**Kleppmann:** `P5, P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, key-loss`

**Must implement:**

- Erasure path for LATAM-jurisdiction tenants matches the GDPR Article 17 crypto-shred mechanism
- LGPD-tenant documentation flags ANPD's open position on crypto-shred sufficiency

**Verification:** An LGPD Article 18 erasure dry-run produces a crypto-shred audit trail and an open-question note for ANPD review

#### `appendix-f-regulatory-coverage:COMP-14` — US sector-specific frameworks (HIPAA, FedRAMP, ITAR)

The absence of a US omnibus privacy law leaves sector-specific regimes — HIPAA for PHI, FedRAMP for federal cloud authorization, ITAR/EAR for export-controlled technology, CCPA/CPRA for California consumer rights — each addressed by on-device encryption and sovereign deployment patterns.

**Kleppmann:** `P5, P6, P7` · **Scope:** `foundational` · **Failure modes:** `data-residency-objection, key-compromise`

**Must implement:**

- HIPAA-scoped PHI is encrypted at rest using the same per-record DEK pattern as GDPR-scoped data
- ITAR-scoped or EAR-scoped deployments restrict node residency to authorized jurisdictions and personnel
- FedRAMP-relevant deployments produce the procurement-evidence bundle required for federal authorization
- California-resident-tenant nodes honor CCPA and CPRA consumer-rights requests through the same erasure path

**Verification:** A US-tenant deployment registers each applicable sectoral framework and produces the corresponding evidence artifacts on demand

#### `appendix-f-regulatory-coverage:COMP-15` — Russian import-substitution market-access requirement

A Russian state procurement policy mandating preference for domestically-produced software, treated not as a data protection law but as a market-access requirement that a locally-deployed on-device build on domestically-licensed components can satisfy where cloud-resident SaaS cannot.

**Kleppmann:** `P5, P7` · **Scope:** `inverted-stack-specific` · **Failure modes:** `data-residency-objection, vendor-acquisition`

**Must implement:**

- State-sector Russian deployments use components on the domestic licensing register
- Build provenance for state-sector deployments is documented to support procurement audits
- The deployment topology distinguishes state-sector tenants from commercial tenants

**Verification:** A state-sector procurement audit confirms domestic component licensing and locally-deployed build provenance for the tenant's nodes


---
