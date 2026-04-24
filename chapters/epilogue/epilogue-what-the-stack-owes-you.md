# Epilogue — What the Stack Owes You

<!-- icm/prose-review -->

<!-- Target: ~2,500 words -->
<!-- Source: v13 §20, v5 §9-10, Ch10 synthesis -->

---

Three things close this book: what the architecture owes you if you build with it, where it falls short today, and where it goes from here.

---

## What the Stack Owes You

The seven non-negotiables from Chapter 10 were presented as design constraints. They are something else. They are obligations — promises the architecture makes to the person sitting in front of it. If the implementation walks them back, the architecture has not merely failed a technical requirement. It has broken faith.

**The stack owes you data minimization at the protocol layer.** Not a UI filter. Not a server-side policy document. A protocol enforcement that ensures data never crosses the network to a node that is not authorized to receive it. The send-tier filter runs before the byte leaves the originating node. No version of this obligation says "we filter it on the way in." The promise is that unauthorized nodes never see the data at all. Anything less is a UI that lies about what security it provides.

**The stack owes you a compliance check before a compromised node touches your data.** MDM attestation happens at capability negotiation — before the handshake completes, before the sync stream opens, before a single document operation is applied. A compromised device is identified and rejected at the perimeter of the trust relationship, not detected after the fact in an audit log. An audit log of a breach is not a security posture. It is a post-mortem.

**The stack owes you honest CRDT semantics.** Three-tier resolution — AP for documents, CP under lease for coordination records, append-only for financial ledger — is not a marketing positioning. It is an acknowledgment that no single consistency model fits every data type, and that pretending otherwise is a technical debt that compounds until it fails catastrophically in production. The architecture names what it guarantees and where. You are owed that honesty.

**The stack owes you complete role revocation.** DEK/KEK envelope encryption with key rotation proportional to document count means that when a role is revoked, that role is gone. Not approximately gone. Not gone pending the next sync cycle. Gone in the mathematical sense: the former role-holder cannot decrypt documents for which their key has been rotated. The word "revoked" should mean something. If it does not, the access control model is cosmetic.

**The stack owes you a dual license from day one.** The CLA and license structure must exist before the community forms, not as an afterthought once adoption creates leverage. Retroactive license changes are not just a business decision. They are a betrayal of the implicit agreement that brought contributors to the project. The governance terms belong in place before the first external pull request lands, not before the IPO.

**The stack owes you a non-technical disaster recovery path.** A non-technical user must be able to restore their complete data after a device failure without calling support. This is not a convenience feature. Data ownership is a meaningless claim if it requires technical sophistication to exercise. The backup UX, the restore UX, and the verification UX must be legible to someone who is not an engineer. If they are not, the architecture has privatized ownership in practice while claiming it publicly.

**The stack owes you a plain-file export that requires no vendor cooperation.** The user can leave. At any time, without negotiating with the platform, without a data export request that takes thirty days to process, without depending on the vendor still being in business. The files are on disk in a documented format. The encryption keys are in the user's control. "Data ownership" without this guarantee is not ownership. It is a lease with favorable terms that the landlord can change.

These are not aspirations. They are the conditions under which the word "local-first" is not false advertising.

---

## The Open Questions That Remain Genuinely Unsettled

This book does not resolve everything.

The envelope encryption model handles role revocation well. The incident-response story for KEK compromise — a stolen administrator workstation with broad role access, active sync sessions, documents distributed across many nodes — has a procedure, but that procedure has not been stress-tested at scale. What does recovery look like when the compromised key had access to ten thousand documents across three hundred nodes? The architecture has answers; those answers have not been validated under production load.

The relay is designed to be data-minimal — a transit cache, not a data store. For most verticals, that design is sufficient. For legal and healthcare, it is not sufficient yet. A full threat model and isolation story for high-risk verticals, where even metadata about document existence can be regulated, has not been completed. The architecture points in the right direction. The last mile of that journey is unfinished.

The CRDT event log is not a stable archival format. The architecture assumes a CRDT-backed document store that is alive and queryable. What happens in twenty years when the software is gone and the data needs to be recovered? Snapshots in more stable formats — signed append-only logs, standardized export schemas — have not been specified. This is not a theoretical concern. It is the obligation from the previous section made concrete across a longer time horizon.

CRDTs give structural convergence. They do not give domain invariants. The inventory-cannot-go-negative constraint, the appointment-time-must-not-double-book constraint, the ledger-must-balance constraint — these require additional modeling beyond what the CRDT engine provides. The architecture acknowledges this; it does not yet have a standardized approach to formal verification of those invariants. This is real work that remains to be done, and the people best positioned to do it are the ones who understand both the domain and the mathematics.

GDPR Article 17 — the right to erasure — is partially addressed by crypto-shredding. Destroy the DEK, and the content is unrecoverable. Whether the operation metadata in the CRDT log — the fact that a document existed, was created by a particular user, was modified at a particular time — constitutes personal data under Article 17 depends on a legal analysis this book cannot perform. The technical mechanism is sound. The legal question requires a lawyer with CRDT expertise, and that intersection is rare.

The analytics problem has no answer here. How do you run product analytics on local-first data without shipping it all to a server? How do you understand aggregate user behavior without centralizing the events that generate it? The architecture has no answer for this. If your product depends on traditional product analytics, you will feel this gap before the end of Phase 1.

The mobile platform question is unresolved. iOS and Android impose constraints on background processing, keystore behavior, and filesystem access that the local-node architecture has not yet solved for. A sync daemon that needs to run continuously encounters App Store restrictions on background execution. A local encrypted database that must survive across app launches faces platform-specific keystore semantics that differ materially from the desktop model. The architecture is designed desktop-first. The path to mobile as a first-class deployment target requires platform-specific engineering that has not been done, and the tradeoffs — battery, background execution limits, user-facing permission prompts — have not been specified. A field operations crew whose primary computing surface is an iPhone does not yet have a complete answer here.

Every architecture has a horizon. The value of honesty about the horizon is that you know where the map ends before you need it.

---

## The Implementation Drift Risk

The most common way local-first architectures fail in practice is not a technical failure. No CRDT bug, no protocol flaw, no security vulnerability takes down more local-first projects than a single phrase: "just a quick server-side check."

It starts with a feature flag. The product team wants to gate a new feature for a beta cohort. The local-first position is clear; the PM points out that the feature will ship in three weeks. The server-side gate goes in. Then analytics — just session counts, nothing identifying, the server barely even sees it. Then A/B testing, because the analytics vendor already has the integration. Then compliance logging, because legal needs an audit trail and the SIEM is already connected to the server. Then permission checks at write time, because someone is not sure the role attestation handles a new edge case and the server check is faster to ship.

At the end of this sequence, the server is load-bearing again. The local node has become a cache with an expensive offline UI. No single decision caused this. Every decision was locally reasonable.

The anti-patterns are specific enough to name. Server-side feature gates after Phase 2 must be replaced with `Sunfish.Foundation.FeatureManagement` evaluated locally — the capability is there, and the decision to use it must be made before the first sprint in which someone asks for a feature flag. Telemetry that requires shipping event data to a server cannot be bolted on after the architecture is established; it must be decided before the first product analytics request, because once the pattern exists it becomes the default. Compliance logging routed to a central server breaks the data sovereignty claim at the exact moment the enterprise customer is likely to audit it. Using the relay as a data store rather than a relay cache turns a transit layer into a dependency, and the relay will eventually exhibit the same failure modes as any database. Server-side permission checks at write time are not a fallback — the permission check belongs in the role attestation at capability negotiation, where it was designed to live.

None of these drift patterns requires a bad actor. They require ordinary engineering teams under ordinary schedule pressure making ordinary pragmatic decisions. The antidote is not a technology choice. It is a set of architectural decisions made before the pressure arrives, recorded in ADRs that future engineers can read, so that when the analytics request lands there is a written answer that predates the request and does not require relitigating the architecture.

Once established, the pattern is not reversible without rearchitecting: server-side paths accumulate dependencies that become load-bearing before anyone notices.

---

## What Comes Next

The sync daemon protocol sub-document is the first and most critical deliverable. It defines the peer handshake, the capability negotiation message format, the stream subscription filtering, and the lease coordination protocol. Every Phase 1 kernel item is blocked without it. Once the sync daemon contract exists as a specification — not an implementation, a specification — the remainder of the implementation follows a clear and validated path.

Sunfish Anchor, the Zone A local-first desktop reference, is running. Waves 3.3 and 3.4 delivered the core kernel wiring — CRDT engine integration, the sync daemon skeleton, the basic role attestation flow. Five items remain deferred from the Wave 3 scope: the Flease lease coordinator integration, gossip anti-entropy for stale peer recovery, the MDM compliance attestation in capability negotiation, the three-tier backup UX, and the plain-file export pipeline. These are not speculative. They are scheduled.

Sunfish Bridge, the Zone C hybrid SaaS reference, is the on-ramp for organizations that cannot cut over to pure local-first in a single step. Three deployment variants — cloud-authoritative with local cache, dual-authority with sync reconciliation, and local-authoritative with cloud backup — cover the migration path documented in Chapter 18. Wave 5 work includes the browser shell, which is the component that makes the hybrid architecture visible to end users who will never install a native app.

Community governance must be decided before the repository opens to external contributors, not after. The BDFL model — a single project lead with veto authority — provides fast decisions and coherent direction at the cost of bus factor and perceived legitimacy for enterprise adopters. A contributor council model — a small committee with defined roles and decision processes — provides legitimacy at the cost of speed and the coordination overhead of committee governance. The decision must be made before the first external pull request, because the governance model shapes contributor expectations in ways that are very difficult to revise once set.

The three highest-value areas for community contribution are the sync daemon protocol specification, the relay hardening work for high-risk verticals, and the formal merge invariant modeling for domain-level constraints. These are also the three areas where the architecture most needs people who bring expertise the core team does not have — distributed systems protocol experience, healthcare and legal compliance knowledge, and formal verification methods. If you have read this book and you have one of those backgrounds, the contribution that matters is not another feature. It is the specification work that unlocks the implementation.

One contribution that often goes overlooked: deployment experience. Every organization that runs a local-first node in production and writes down what failed — what the MDM edge case was, what the mDNS multicast issue turned out to be, what the enterprise security team asked that the architecture document did not answer — adds more durable value to the community than a new feature. The feature ships and gets superseded. The deployment experience accumulates. Runbooks, post-mortems, and annotated deployment guides are primary source material for the next engineer who attempts the same path. A practitioner book without practitioners who write back is a monologue.

---

## The Closing

The enabling technologies are mature. The components are individually production-validated. The remaining work is engineering: assembling what is known into a coherent, deployable system with the UX polish that makes distributed complexity invisible to the people who should never have to think about it.

What this architecture asks of the people who build with it is different from what a managed SaaS asks. A SaaS vendor asks you to trust that they will keep the data safe, keep the service available, and not change the terms. The inverted stack asks you to take responsibility for the data — to run the backup, to manage the keys, to issue the attestations, to maintain the runbooks. That is a larger surface of responsibility. It is also a surface you actually control. The difference is not a trade of convenience for security. It is a trade of dependency for agency. Whether that trade is worth making depends on what you are building and who you are building it for.

For the use cases this book describes — field operations, regulated industries, disconnected worksites, organizations with strong data sovereignty requirements — the trade is straightforward. The infrastructure model matches the environment. The architecture is not fighting the deployment context; it is designed for it.

It is tractable, with known unknowns and a clear path through them. The stack knows what it owes. Now it has to deliver.

---

*End of The Inverted Stack: Local-First Nodes in a SaaS World*
