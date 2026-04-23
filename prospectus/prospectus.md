# Book Prospectus

## *The Inverted Stack: Local-First Nodes in a SaaS World*

<!-- Target: ~3,000 words -->
<!-- icm/draft -->

**Author:** Chris Woodward
**Format:** Self-published practitioner book
**Target length:** ~83,500 words
**Reference implementation:** Sunfish (`github.com/ctwoodwa/Sunfish`)

---

## The Problem This Book Solves

Every SaaS application makes the same implicit bargain: we will give you real-time collaboration, multi-device access, and zero-maintenance operation, and in exchange you will accept that your data lives on our infrastructure, that your access ends when your subscription ends, and that your software stops working when our servers go down. Most users have accepted this bargain not because they prefer it but because they believed the desirable half was inseparable from the undesirable half. It is not.

This belief persists because no single resource has demonstrated, with full technical specificity, how to deliver the capabilities users want — collaboration, sync, offline operation — without the vendor dependencies they have been forced to accept. Local-first software research has established the theoretical foundation. Individual systems like Linear, Figma, and Actual Budget have demonstrated pieces of the implementation. But no production-grade blueprint exists for the full stack: a workstation node with its own application logic, CRDT-backed storage, sync daemon, and enterprise deployment story.

The gap is not in the component technologies. CRDTs are production-proven. Gossip protocols are production-proven. Envelope encryption is production-proven. The gap is in the composition: assembling these components into a coherent architecture that handles the hard cases — CRDT garbage collection, distributed lease coordination, schema migration across a mixed-version fleet, MDM deployment in a managed enterprise, key compromise incident response, data portability on device loss — and doing so with enough specificity to build from.

This book is that blueprint.

It addresses the failure modes that stop local-first systems from reaching production: the construction site that loses connectivity during a critical handoff, the legal firm whose vendor shuts down while documents are under active review, the field operations team whose SaaS subscription is terminated by an acquirer three months into a project. These are not edge cases. They are the conditions under which the hidden cost of the SaaS bargain becomes visible. The Inverted Stack is a complete architecture for software that does not impose that cost.

---

## The Thesis

The central argument is that the inversion is now technically achievable and commercially viable.

**Conventional SaaS:** Cloud database is primary → local device caches and renders.

**Local-Node Architecture:** Local node is primary → cloud relay is an optional sync peer.

Every workstation runs a self-contained application node: UI, business logic, sync daemon, and encrypted local database. When peers are reachable, nodes exchange CRDT state through a gossip protocol. When no peers are reachable, the node operates at full fidelity. There is no degraded mode because there is no dependency on any remote service for core function. The cloud, where deployed, acts as a coordination relay and backup peer — not an authority.

| Property | Conventional SaaS | Local-Node Architecture |
|---|---|---|
| Works offline | Degraded or none | Full fidelity |
| Data residency | Vendor infrastructure | User's own hardware |
| Vendor dependency | Existential | None after installation |
| Real-time collaboration | Yes (cloud-mediated) | Yes (peer-to-peer) |
| Multi-device sync | Yes (cloud-mediated) | Yes (gossip relay) |
| Enterprise data governance | Contractual | Structural |
| IT/MDM deployment | Varies | First-class requirement |
| Air-gap operation | Rarely | Native |
| Open-source viable | Rarely | Designed for it |

This is not the right architecture for every product. Systems whose value derives from aggregating data across all users — social feeds, financial exchanges, global search, real-time inventory — remain correctly centralized. The selection framework in Chapter 4 provides a structured decision process. For the large class of software where the primary value is the user's own data — project management, document editing, field operations, professional services, healthcare workflows — the local-node architecture is not a compromise. It is an upgrade.

The commercial model follows from the architecture. A permissive open-source core with no license server means no feature paywall to enforce. Revenue comes from a managed relay: operationally hardened, SLA-backed peer coordination infrastructure that teams subscribe to for guaranteed sync, NAT traversal, and professional support. Infrastructure cost analysis shows the service reaches cash-flow positive well before meaningful scale, with surplus funding core library maintenance.

---

## Original Contribution

The component technologies in this book are not new. CRDTs underpin Figma and Linear. Leaderless replication underlies Cassandra and DynamoDB. The desktop-shell-plus-local-server pattern is established by VS Code and 1Password. Declarative partial sync is proven by PowerSync and ElectricSQL. Silent background container services are normalized by Docker Desktop and Tailscale.

The contribution is the composition. None of those systems individually answers: how do you assemble these proven components into a coherent, deployable architecture that behaves like a cloud application, scales to enterprise governance requirements, and treats user data ownership as a structural guarantee rather than a contractual promise?

Specifically, this book provides things that do not currently exist in a single resource:

**A complete per-record CAP positioning framework.** Not "use CRDTs for everything." This book specifies, at the record-class level, which data belongs on the AP side of the CAP boundary — CRDT merge, full offline availability — and which belongs on the CP side — distributed lease coordination, blocking writes during partition. The criteria are operational, not theoretical.

**A production CRDT garbage collection policy.** Long-running local-first systems accumulate op log history without bound unless actively managed. This book specifies a three-tier GC policy with stale peer recovery protocols for nodes that reconnect after the GC horizon.

**A schema migration architecture for mixed-version fleets.** Nodes update independently. Teams run mixed versions simultaneously. The expand-contract pattern with bidirectional schema lenses, epoch coordination, and copy-transform migration jobs handles the "couch device" returning after three major versions.

**A key compromise incident response procedure.** The DEK/KEK envelope encryption hierarchy, detection mechanism, re-keying procedure, data-at-risk scope, and user-visible notification path are fully specified.

**A formal adversarial evaluation record.** Five domain experts reviewed this architecture across two rounds. Every blocking issue is documented alongside its resolution. Part II of the book is that record.

---

## Intended Audience

**Software architects and senior engineers** building or evaluating local-first systems will find a complete distributed systems specification precise enough to serve as an implementation guide. The technical sections assume distributed systems familiarity but not prior local-first experience.

**Enterprise evaluators, IT architects, and technical decision-makers** will find a governance-first design with named MDM policies, SBOM toolchain specifications, compliance framework mappings, and an incident response runbook written to satisfy enterprise procurement questions directly.

**Open-source contributors, technical founders, and product teams** will find a viable project model: a dual-license strategy, relay economics modeled at 10/100/1,000 teams, a first-customer archetype in the construction vertical, and a governance structure specific enough to build a business plan from.

The book does not require prior local-first experience. It requires the ability to read a distributed systems specification and care about whether production software survives contact with reality.

---

## Structure and Scope

**Part I — The Thesis and the Pain** (Chapters 1–4, ~15,000 words) establishes why the SaaS default is worth replacing and what replaces it. Chapter 1 documents concrete failure modes by domain. Chapter 2 surveys the existing local-first landscape and identifies what prior work omits. Chapter 3 introduces the architecture in one diagram. Chapter 4 provides the selection framework.

**Part II — The Council Reads the Paper** (Chapters 5–10, ~20,000 words) is the adversarial evaluation. Five domain experts reviewed the architecture across two rounds. Each chapter presents one council member's lens, the blocking issues from Round 1, what changed, and the Round 2 verdict. The architecture failed first inspection on six counts; the resolutions are substantive.

**Part III — The Reference Architecture** (Chapters 11–16, ~22,000 words) is the complete technical specification: node architecture, CRDT engine and data layer, schema migration, sync daemon protocol, security architecture, persistence and relay. Written as reference — return to individual chapters as you build.

**Part IV — Implementation Playbooks** (Chapters 17–20, ~14,000 words) provides minimal paths to working implementations: building a first node, migrating an existing SaaS, shipping to enterprise, designing UX for sync and conflict. References Part III for full specifications.

---

## The Kleppmann Council as Evaluation Method

Standard peer review asks: is this correct? The Kleppmann Council asks: does this actually work — for IT departments, for distributed systems researchers, for security practitioners, for paying customers, for real users?

Five reviewers examined the architecture from distinct professional lenses:

- **Dr. Marguerite Voss** (Enterprise Infrastructure Architect) — will this pass a real procurement committee?
- **Prof. Dmitri Shevchenko** (Distributed Systems Researcher) — is the synchronization model theoretically sound?
- **Nia Okonkwo** (Application Security Practitioner) — what does an attacker with physical access gain?
- **Jordan Kelsey** (Product Manager / Startup Founder) — will anyone pay for this?
- **Tomás Ferreira** (Local-First Community Practitioner) — does this actually work for real users?

Round 1 produced two BLOCK verdicts and four conditions across the other three reviewers. The six blocking issues were:

1. No CRDT garbage collection strategy — without one, long-running nodes accumulate unbounded op log history, causing performance degradation in any deployment running longer than twelve months.
2. An unaddressed Flease split-write window — if the lease holder becomes unreachable during a write and a new lease is elected, two nodes may simultaneously believe they hold write authority.
3. Absent key compromise incident response — for a system with symmetric role keys wrapped per-node, a compromised node key potentially exposes all data the node has ever been authorized to read. No detection mechanism, re-keying procedure, or data-at-risk scope was specified.
4. No first customer archetype — the commercial section named a demographic ("developer communities who value data sovereignty") rather than a customer with a job title, a problem, and an acquisition path.
5. No OSS-to-paid conversion mechanism — the specific moment or trigger that causes a free user to pay was undefined.
6. No data portability path — a paper arguing for data ownership that did not specify how a user exports their data in a durable, application-independent format contradicted its own thesis.

These are not editorial quibbles. Items 1 and 2 are correctness gaps that would cause production failures. Items 3 through 6 would cause the architecture to fail enterprise security review, fail commercial diligence, and fail the trust of the local-first community simultaneously.

Round 2 cleared all six blocks. The architecture advanced to PROCEED WITH CONDITIONS — fifteen conditions across four reviewers, none individually blocking, all addressable without halting implementation. Tomás Ferreira, the local-first community practitioner, issued an unconditional PROCEED — the first version of the architecture he reviewed without reservation.

Part II of this book is a detailed account of both rounds: what each council member found, what changed between rounds, and the principle each chapter's resolution demonstrates. The adversarial evaluation process is how an architecture earns the right to claim production-readiness rather than merely asserting it.

---

## Why Self-Publishing

Self-publishing allows the book and the reference implementation to evolve together. Sunfish is pre-1.0. Its package names are stable; its class APIs are not. A traditionally published book with an 18-month production timeline would arrive out of date.

Self-publishing also allows Part I to be released first — readable and useful independently — while the more technically demanding Parts III and IV are completed. Practitioners making architecture decisions now do not have to wait for the full manuscript.

*Designing Data-Intensive Applications* is published by O'Reilly, which is appropriate for a book that covers multiple systems at breadth. This book covers one architecture in depth. Depth books age faster, iterate more, and serve their readers better as living documents.

---

## The Reference Implementation

**Sunfish** (`github.com/ctwoodwa/Sunfish`) is the open-source reference implementation developed alongside this book. Two canonical accelerators exist:

- **Anchor** (`accelerators/anchor/`) — Zone A local-first desktop (.NET MAUI Blazor Hybrid, offline-by-default, SQLCipher, Ed25519 device keys)
- **Bridge** (`accelerators/bridge/`) — Zone C hybrid multi-tenant SaaS (.NET Aspire, Blazor Server, per-tenant data-plane isolation, ciphertext-only relay)

Sunfish is pre-1.0. This book references it by package name (`Sunfish.Kernel.Sync`, `Sunfish.Foundation.LocalFirst`) rather than specific class APIs. The current CRDT engine is YDotNet (Yjs .NET); the architecture specifies Loro as the aspirational primary pending maturity of the `loro-cs` bindings. The `ICrdtEngine` abstraction makes the choice reversible.

---

## Comparable Works

**Designing Data-Intensive Applications** (Kleppmann, O'Reilly, 2017) is the closest intellectual ancestor. DDIA establishes the distributed systems vocabulary this book assumes — replication, consensus, transactions, consistency models — and provides the deepest available treatment of the individual components. It does not attempt to specify how to compose those components into a single deployable product. This book picks up where DDIA leaves off: not how these systems work individually, but how to assemble them into a locally-hosted application that behaves like cloud software, deploys into enterprise environments, and treats data ownership as a structural guarantee.

**The Local-First Software essay** (Kleppmann et al., Ink & Switch, 2019) establishes the seven ideals this architecture is designed to satisfy and makes the foundational argument for why they matter. It does not provide an implementation architecture. The essay is approximately 8,000 words; this book is approximately 83,500 words that answer the question the essay raises.

**Building Microservices** (Newman, O'Reilly) and **Software Architecture: The Hard Parts** (Ford et al., O'Reilly) address distributed system decomposition with the cloud as the assumed deployment target. This book inverts that assumption — the workstation is the server, the cloud is a peer — which changes most of the architectural decisions.

**Actual Budget** is the closest production commercial analogue to what this book specifies: a full-capability financial application that runs locally, requires no server for core function, and offers an optional sync service. It validates both the local-first model and a revenue path that does not depend on per-seat pricing. It does not publish its architecture.

No current book addresses local-first architecture at the implementation depth this one does — with full coverage of CRDT GC policy, schema migration for mixed-version fleets, enterprise MDM deployment, security key hierarchy, and commercial viability in a single resource.

---

## Word Count and Timeline

| Section | Target |
|---|---|
| Front Matter | ~2,000 |
| Part I (Ch 1–4) | ~15,000 |
| Part II (Ch 5–10) | ~20,000 |
| Part III (Ch 11–16) | ~22,000 |
| Part IV (Ch 17–20) | ~14,000 |
| Epilogue | ~2,500 |
| Appendices A–D | ~8,000 |
| **Total** | **~83,500** |

Release plan: Part I published first as early access. Parts II, III, and IV follow in sequence. Sunfish and the book are updated in parallel.
