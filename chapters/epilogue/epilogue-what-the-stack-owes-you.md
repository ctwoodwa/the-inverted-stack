# Epilogue — What the Stack Owes You

<!-- icm/prose-review -->

<!-- Target: ~2,500 words -->
<!-- Source: v13 §20, v5 §9-10, Ch10 synthesis -->

---

Three things close this book. What the architecture owes you if you build with it. Where it falls short today. Where it goes from here.

---

## What the Stack Owes You

The seven non-negotiables from Chapter 10 were presented as design constraints. They are something else. They are obligations — promises the architecture makes to the person sitting in front of it. If the implementation walks them back, the architecture has not merely failed a technical requirement. It has broken faith.

**The stack owes you data minimization at the protocol layer.** Not a UI filter. Not a server-side policy document. A protocol enforcement that ensures data never crosses the network to a node that is not authorized to receive it. The send-tier filter runs before the byte leaves the originating node. No version of this obligation says "we filter it on the way in." The promise is that unauthorized nodes never see the data at all. Anything less is a UI that lies about what security it provides.

**The stack owes you a compliance check before a compromised node touches your data.** MDM (Mobile Device Management) attestation happens at capability negotiation — before the handshake completes, before the sync stream opens, before a single document operation is applied. A compromised device is identified and rejected at the perimeter of the trust relationship, not detected after the fact in an audit log. An audit log of a breach is not a security posture. It is a post-mortem.

**The stack owes you honest CRDT (Conflict-free Replicated Data Type) semantics.** Three-tier resolution — AP for documents, CP under lease for coordination records, append-only for financial ledger — is not marketing positioning. It is an acknowledgment that no single consistency model fits every data type. Pretending otherwise is a technical debt that compounds quietly until it fails catastrophically in production. The architecture names what it guarantees and where. You are owed that honesty.

**The stack owes you complete role revocation.** DEK (Data Encryption Key)/KEK (Key Encryption Key) envelope encryption with key rotation proportional to document count means that when a role is revoked, that role is gone. Not approximately gone. Not gone pending the next sync cycle. Gone in the mathematical sense: the former role-holder cannot decrypt documents for which their key has been rotated. The word "revoked" should mean something. If it does not, the access control model is cosmetic.

**The stack owes you a dual license from day one.** The CLA and license structure must exist before the community forms, not as an afterthought once adoption creates leverage. Retroactive license changes are not just a business decision. They are a betrayal of the implicit agreement that brought contributors to the project. The governance terms belong in place before the first external pull request lands. Not before the IPO.

**The stack owes you a non-technical disaster recovery path.** A non-technical user must be able to restore their complete data after a device failure without calling support. This is not a convenience feature. Data ownership is a meaningless claim if it requires technical sophistication to exercise. The backup UX, the restore UX, and the verification UX must be legible to someone who is not an engineer. If they are not, the architecture has privatized ownership in practice while claiming it publicly.

**The stack owes you a plain-file export that requires no vendor cooperation.** The user can leave. At any time, without negotiating with the platform, without a data export request that takes thirty days to process, without depending on the vendor still being in business. The files are on disk in a documented format. The encryption keys are in the user's control. "Data ownership" without this guarantee is not ownership. It is a lease with favorable terms that the landlord can change.

These are not aspirations. They are the conditions under which the word "local-first" is not false advertising.

---

## The Open Questions That Remain Genuinely Unsettled

This book does not resolve everything.

The envelope encryption model handles role revocation well. The incident-response story for KEK compromise — a stolen administrator workstation with broad role access, active sync sessions, documents distributed across many nodes — has a procedure, but that procedure has not been stress-tested at scale. What does recovery look like when the compromised key had access to ten thousand documents across three hundred nodes? The architecture has answers. Those answers have not been validated under production load.

The relay is designed to be data-minimal — a transit cache, not a data store. For most verticals, that design is sufficient. For legal and healthcare, it is not sufficient yet. A full threat model and isolation story for high-risk verticals, where even metadata about document existence can be regulated, has not been completed. The architecture points in the right direction. The last mile of that journey is unfinished.

The CRDT event log is not a stable archival format. The architecture assumes a CRDT-backed document store that is alive and queryable. What happens in twenty years when the software is gone and the data needs to be recovered? Snapshots in more stable formats — signed append-only logs, standardized export schemas — have not been specified. This is not a theoretical concern. It is the obligation from the previous section made concrete across a longer time horizon.

CRDTs (Conflict-free Replicated Data Types) give structural convergence. They do not give domain invariants. The inventory-cannot-go-negative constraint, the appointment-time-must-not-double-book constraint, the ledger-must-balance constraint — these require additional modeling beyond what the CRDT engine provides. The architecture acknowledges this. It does not yet have a standardized approach to formal verification of those invariants. This is real work that remains to be done, and the people best positioned to do it are the ones who understand both the domain and the mathematics.

The right-to-erasure question is partially addressed by crypto-shredding. Destroy the DEK, and the content is unrecoverable. Whether the operation metadata in the CRDT log — the fact that a document existed, was created by a particular user, was modified at a particular time — constitutes personal data under the applicable regime depends on a legal analysis this book cannot perform. The technical mechanism addresses erasure at the content layer; whether this satisfies the erasure statute in your jurisdiction requires jurisdiction-specific legal counsel. CNIL (Commission nationale de l'informatique et des libertés) in France and several German DPAs have not definitively resolved whether DEK destruction constitutes lawful erasure under GDPR (General Data Protection Regulation) Article 17, and the same unsettled question applies under every parallel right-to-deletion regime — India's DPDP (Digital Personal Data Protection) Act 2023 Section 12 and the UAE Data Protection Law 2022 Article 16 are representative; the full coverage matrix is in Appendix F. The CRDT-log erasure question is universal, not European. Every jurisdiction that has codified a right to deletion faces the same open question, and the answer must come from a lawyer with both data-protection and CRDT expertise — an intersection that is rare in every market the architecture would serve.

The analytics problem has no answer here. How do you run product analytics on local-first data without shipping it all to a server? How do you understand aggregate user behavior without centralizing the events that generate it? The architecture has no answer for this. If your product depends on traditional product analytics, you will feel this gap before the end of Phase 1.

The mobile platform question is unresolved. iOS and Android impose constraints on background processing, keystore behavior, and filesystem access that the local-node architecture has not yet solved for. A sync daemon that needs to run continuously encounters App Store restrictions on background execution. A local encrypted database that must survive across app launches faces platform-specific keystore semantics that differ materially from the desktop model. The architecture is designed desktop-first. The path to mobile as a first-class deployment target requires platform-specific engineering that has not been done, and the tradeoffs — battery, background execution limits, user-facing permission prompts — have not been specified. A field operations crew whose primary computing surface is an iPhone does not yet have a complete answer here.

Every architecture has a horizon. Honesty about the horizon means you know where the map ends before you need it.

---

## The Implementation Drift Risk

The most common way local-first architectures fail in practice is not a technical failure. No CRDT bug, no protocol flaw, no security vulnerability takes down more local-first projects than a single phrase: "just a quick server-side check."

It starts with a feature flag. The product team wants to gate a new feature for a beta cohort. The local-first position is clear; the PM points out that the feature will ship in three weeks. The server-side gate goes in. Then analytics — just session counts, nothing identifying, the server barely even sees it. Then A/B testing, because the analytics vendor already has the integration. Then compliance logging, because legal needs an audit trail and the SIEM is already connected to the server. Then permission checks at write time, because someone is not sure the role attestation handles a new edge case and the server check is faster to ship.

At the end of this sequence, the server is load-bearing again. The local node has become a cache with an expensive offline UI. No single decision caused this. Every decision was locally reasonable.

The anti-patterns are specific enough to name. Server-side feature gates after Phase 2 must be replaced with `Sunfish.Foundation.FeatureManagement` evaluated locally — the capability is there, and the decision to use it must be made before the first sprint in which someone asks for a feature flag. Telemetry that requires shipping event data to a server cannot be bolted on after the architecture is established; it must be decided before the first product analytics request, because once the pattern exists it becomes the default. Compliance logging routed to a central server breaks the data sovereignty claim at the exact moment the enterprise customer is likely to audit it. Using the relay as a data store rather than a relay cache turns a transit layer into a dependency, and the relay will eventually exhibit the same failure modes as any database. Server-side permission checks at write time are not a fallback — the permission check belongs in the role attestation at capability negotiation, where it was designed to live.

None of these drift patterns requires a bad actor. They require ordinary engineering teams under ordinary schedule pressure making ordinary pragmatic decisions. The antidote is not a technology choice. It is a set of architectural decisions made before the pressure arrives, recorded in ADRs that future engineers can read, so that when the analytics request lands, a written answer already exists — one that predates the request and does not require relitigating the architecture.

Once established, the pattern has historically not reversed without rearchitecting: server-side paths accumulate dependencies that become load-bearing before anyone notices. The ADR (Architecture Decision Record) recommendation here is organizational as well as technical — the drift-prevention decisions must name an owner (an architecture review board, a principal engineer, or explicit CTO (Chief Technology Officer) sign-off on any deviation), because ADRs without an enforcement role do not survive velocity pressure.

---

## What You Do Next

The remainder of this epilogue addresses the reader directly — what to do with this book closed in front of you, on three time horizons.

**Week 1: Read the sync daemon protocol in Appendix A.** Every architectural decision downstream hinges on the handshake, the capability negotiation message format, the stream subscription filtering, and the lease coordination protocol. Draft your first ADR using the Chapter 17 template: *ADR-001: Why we are building local-first*. Name the failure mode your organization faces — procurement lock-in, regulatory pressure, connectivity baseline, or a 2022-style termination risk — and the specific obligations from "What the Stack Owes You" that you commit to delivering. If the drift-risk section's anti-patterns describe your current roadmap, ADR-001 is the place to draw the line before the pressure arrives.

**Month 1: Stand up the Phase 1 kernel proof-of-concept.** Use Chapter 17 as your reference — a single-node Anchor (the Zone A local-first desktop accelerator) deployment with the CRDT engine, the sync daemon skeleton, and the role attestation flow. Validate against a concrete scenario from your domain: a field operation, a two-laptop disconnected editing session, a device restore from backup. The proof-of-concept is not the product. It is the evidence you will use to defend the architectural choice in the first procurement conversation.

**First enterprise pitch: run the compliance checklist before you schedule the call.** Chapter 19 provides the MDM policy, SBOM (Software Bill of Materials) manifest, code-signing attestation, and compliance framework mapping a procurement committee will ask for. The jurisdictions this book addresses — anchored by GDPR/Schrems II, India's DPDP Act, and the UAE's DIFC (Dubai International Financial Centre) DPL (Data Protection Law), with the full coverage matrix in Appendix F — are named with their compliance obligations because enterprise buyers will ask which of them you have considered. Have the answer before the question lands. For readers operating in relationship-led procurement markets — GCC (Gulf Cooperation Council) government, traditional Indian BFSI (Banking, Financial Services, and Insurance), Japanese SIer (Systems Integrator) channels — the first conversation is not with the technical buyer; it is with the local partner or SIer who will carry the architecture through the purchasing committee. The specification completeness of Part III is what enables that intermediary to represent the architecture without the author in the room.

**For the reader committed to Azure, AWS, or GCP today:** Sunfish (the open-source reference implementation, [github.com/ctwoodwa/Sunfish](https://github.com/ctwoodwa/Sunfish)) Bridge (the Zone C hybrid SaaS accelerator) (the Zone C hybrid SaaS (Software as a Service) accelerator) is the on-ramp. Chapter 18's four-phase migration — cloud-authoritative, dual-authority, local-authoritative with cloud backup, pure local-first — lets an organization move incrementally rather than cutting over. The trade-off is documented honestly. The timeline is weeks to months per phase for a typical organization, not days.

**For the reader whose organization lost access to SaaS (Software as a Service) tools in 2022:** you have already paid the cost this book warns against. You are the architecture's most natural early adopter. The migration path in Chapter 18 is calibrated to your case — you do not have the luxury of drift, and the specification completeness of Part III is the substrate for the import-substitution procurement mandate (импортозамещение) that your buyers face.

**For the contributor:** three categories matter. The sync daemon protocol specification, relay hardening for high-risk verticals (legal, healthcare, public sector), and formal merge invariant modeling for domain-level constraints are the areas where the core team most needs expertise it does not have. If you have distributed-systems protocol experience, healthcare or legal compliance knowledge, or formal verification methods, the contribution that matters is specification work, not feature work. And one contribution that often goes overlooked: deployment experience. Every organization that runs a node in production and writes down what failed — the MDM edge case, the mDNS multicast issue, the enterprise security team's question the architecture document did not answer — contributes more durable value than a new feature. Runbooks, post-mortems, and annotated deployment guides are primary source material for the next engineer who attempts the same path. A practitioner book without practitioners who write back is a monologue.

---

## The Closing

The preface made four commitments. They are worth revisiting now that the book has been read.

*A production-calibrated specification cleared by five adversarial reviews under fifteen documented conditions.* Delivered. Part II names the conditions; the open questions above name the honest subset that remains unsettled.

*A credibility framework — named objections and named responses — for defending the architectural choice.* Delivered. Parts II, III, and IV together provide the vocabulary for a procurement conversation, a security review, or a compliance audit.

*A commercial model that does not depend on community adoption as economic substrate.* Delivered. Chapter 8 models relay economics at 10, 100, and 1,000 teams; Chapter 10 closes the commercial case with an acquisition channel rather than a hopeful community.

*A compliance posture across the major data-residency regimes — Schrems II, DPDP, DIFC DPL, and the broader Appendix F coverage matrix.* Delivered with a specific deferral: every jurisdiction with a codified right to deletion carries the CRDT-log open question named above. The mechanism is specified. The jurisdictional ruling is pending — in some cases indefinitely.

The evidentiary anchor is the 2022 CIS (Commonwealth of Independent States) terminations. Adobe, Autodesk, Microsoft, and Figma ([figma.com](https://www.figma.com/), the design tool) suspended or restricted service across Russia and Belarus; organizations across the region lost access to data they had paid to host on vendor infrastructure. You have read what vendor dependency costs in the language of architecture throughout this book. In 2022, you saw it in the language of procurement, in real time, at continental scale. That event is the reason the architectural choice matters. Everything this book specifies is the answer to the question it forced every enterprise IT leader in the region to answer in a weekend.

The enabling technologies are mature. The components are individually production-validated. The remaining work is engineering: assembling what is known into a coherent, deployable system with the UX polish that makes distributed complexity invisible to the people who should never have to think about it.

What this architecture asks of the people who build with it is different from what a managed SaaS asks. A SaaS vendor asks you to trust that they will keep the data safe, keep the service available, and not change the terms. The inverted stack asks you to take responsibility for the data — to run the backup, to manage the keys, to issue the attestations, to maintain the runbooks. That is a larger surface of responsibility. It is also a surface you actually control. For the use cases this book describes — field operations, regulated industries, disconnected worksites, organizations in connectivity-constrained markets, organizations under data-localization mandates — the infrastructure model matches the environment. The architecture is not fighting the deployment context. It is designed for it.

The stack knows what it owes. You now know how to demand it — in an RFP, in a procurement review, in a security audit, in a migration plan, in an ADR. The difference the architecture offers is not a trade of convenience for security. It is a trade of dependency for agency.

Take it.

---

*End of The Inverted Stack: Local-First Nodes in a SaaS World*
