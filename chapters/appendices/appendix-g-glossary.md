# Appendix G — Glossary

<!-- icm/draft -->
<!-- Target: ~2,500 words -->

This glossary defines the specialized vocabulary the book uses across multiple chapters. Terms are alphabetical. Each entry gives the full expansion (where applicable), a brief definition, and a chapter pointer to the section that develops the concept in full when that section exists.

The glossary is the canonical first-use reference for the book's specialized vocabulary. Chapters may use a term without inline expansion when the term is established here. Industry-universal acronyms (UI, UX, IT, OS) are not glossed; the book assumes practitioner familiarity.

---

## A

**AES-256-GCM (Advanced Encryption Standard, 256-bit, Galois/Counter Mode)**
A NIST-standard authenticated encryption algorithm. The local-node architecture uses AES-256-GCM for envelope encryption — each document gets a random 256-bit Data Encryption Key (DEK), the DEK encrypts the document body with a fresh 96-bit nonce per encryption event and a 128-bit authentication tag. See also: DEK, KEK. Specified in: Chapter 15 §Key Hierarchy.

**Anchor (Sunfish accelerator)**
The reference implementation of the Zone A pattern — a .NET MAUI Blazor Hybrid local-first desktop application. Source: `Sunfish/accelerators/anchor/`. The Anchor accelerator is the right shape for offline-by-default professional or enterprise software where each user runs a complete local node. Pre-1.0; in active development. See also: Bridge, Zone A. Specified in: Chapter 17.

**Anti-entropy**
A class of distributed-systems protocols that converge replicas by exchanging only the differences (deltas) between them, rather than retransmitting full state. The local-node architecture's sync daemon uses gossip-based anti-entropy: every 30 seconds, the daemon exchanges a delta with two random peers. See also: gossip protocol, vector clock. Specified in: Chapter 14 §Sync Daemon Protocol.

**AP-class (Availability-Partition class records)**
Records whose correctness tolerates eventual consistency under network partitions. AP-class records use CRDT merge semantics — multiple peers can write concurrently; the system converges deterministically. Most user-owned records (notes, project files, work logs, comments) are AP-class. See also: CAP theorem, CP-class. Specified in: Chapter 12 §AP/CP Boundary.

**Argon2id**
A memory-hard password-based key derivation function, winner of the 2015 Password Hashing Competition. The local-node architecture uses Argon2id (128 MiB memory, 4 iterations, 4 lanes) to derive paper-key recovery secrets from a user's transcribed passphrase. Specified in: Chapter 15 §Key Hierarchy.

---

## B

**BAA (Business Associate Agreement)**
A HIPAA-required contract between a covered entity (a healthcare provider) and a business associate (a vendor handling protected health information) that specifies the business associate's obligations under HIPAA. A vendor shipping local-node software for HIPAA workloads needs a BAA covering the storage architecture and the audit-trail surfaces. See also: HIPAA. Specified in: Chapter 4 §Per-Zone Compliance Posture; Chapter 15.

**Bridge (Sunfish accelerator)**
The reference implementation of the Zone C pattern — a .NET Aspire multi-tenant hosted SaaS where each tenant gets a dedicated local-node host process. Source: `Sunfish/accelerators/bridge/`. The Bridge accelerator is the right shape for organizations that want hosted-service deployment simplicity alongside local-first data sovereignty guarantees. Pre-1.0; in active development. See also: Anchor, Zone C. Specified in: Chapter 18.

---

## C

**CAP theorem**
The result that no distributed system can simultaneously guarantee consistency, availability, and partition tolerance (Brewer 2000; formal proof Gilbert & Lynch 2002). The local-node architecture treats CAP as a per-record-class decision, not a system-wide one — AP-class records favor availability; CP-class records favor consistency. See also: AP-class, CP-class. Specified in: Chapter 3 §The Per-Record CAP Boundary.

**CBOR (Concise Binary Object Representation)**
A binary serialization format defined in RFC 8949, designed for compactness and processing efficiency on resource-constrained devices. The sync daemon uses CBOR as the wire format for delta exchange between peers. Specified in: Chapter 14 §Wire Protocol; Appendix A.

**CCPA (California Consumer Privacy Act)**
The 2018 California state law (effective 2020, amended by CPRA effective 2023) governing personal information collected from California residents. CCPA's data-portability and right-to-delete provisions are addressed structurally by the local-node architecture's user-controlled storage. Specified in: Appendix F.

**CISO (Chief Information Security Officer)**
The executive role responsible for an organization's information security program. Procurement decisions for software handling sensitive data typically require CISO sign-off. The book's threat model and compliance framing are calibrated to survive CISO-led security review. Specified in: Chapter 5 (Voss's perspective); Chapter 19 §Procurement.

**CP-class (Consistency-Partition class records)**
Records whose correctness requires distributed coordination — typically because concurrent writes from different peers would create observable contradictions (double-bookings, double-spends, single-writer invariants). CP-class records use Flease lease coordination to acquire a temporary write authority before mutating. See also: AP-class, CAP theorem, Flease. Specified in: Chapter 12 §AP/CP Boundary; Chapter 14 §Lease Coordination.

**CRDT (Conflict-free Replicated Data Type)**
A class of data structures whose merge function is commutative, associative, and idempotent — meaning any two diverged copies can be merged in any order and arrive at the same result, without a coordinator. The local-node architecture uses CRDTs for all AP-class records. Foundational reference: Shapiro et al. 2011. See also: Yjs, Loro, Automerge, YDotNet. Specified in: Chapter 12.

---

## D

**DEK (Data Encryption Key)**
A symmetric encryption key generated per document or per record, used to encrypt the body content. The DEK never persists in unwrapped form beyond the active decryption operation — at rest it is wrapped under the role-scoped Key Encryption Key (KEK). See also: KEK, AES-256-GCM, envelope encryption. Specified in: Chapter 15 §Key Hierarchy.

**DIFC DPL (Dubai International Financial Centre Data Protection Law, 2020)**
The data protection law governing entities licensed to operate in the Dubai International Financial Centre free zone. DIFC DPL constrains processing and cross-border transfers of personal data and requires specific lawful bases for transfers to non-adequate jurisdictions. See also: GDPR, DPDP. Specified in: Appendix F.

**DPDP (Digital Personal Data Protection Act, India 2023)**
India's first comprehensive personal data protection law, enacted August 2023. DPDP creates obligations comparable to GDPR for organizations handling Indian residents' personal data, with notable differences in lawful bases and cross-border transfer rules. See also: GDPR, RBI circular. Specified in: Appendix F.

**DPL (Data Protection Law)**
A generic term used in the book to refer to jurisdictional data protection statutes. The book's regulatory coverage matrix (Appendix F) catalogs ~40+ DPLs across seven regions.

---

## E

**ElectricSQL**
A commercial sync framework (Postgres + selective replica sync to local SQLite) that provides server-authoritative real-time sync with offline support. Discussed as prior art in Chapter 2 §What Exists Today. The architecture in this book takes a different position: local-node-authoritative rather than server-authoritative.

**Envelope encryption**
A two-tier key hierarchy where each document is encrypted with a unique Data Encryption Key (DEK), and the DEK itself is encrypted ("wrapped") under a longer-lived Key Encryption Key (KEK). Envelope encryption enables key rotation without re-encrypting bulk data — only the DEK gets re-wrapped under the new KEK. See also: DEK, KEK, AES-256-GCM. Specified in: Chapter 15 §Key Hierarchy.

---

## F

**FINRA (Financial Industry Regulatory Authority)**
The US self-regulatory organization governing broker-dealers. FINRA Rule 4511 and SEC Rule 17a-4 specify third-party WORM (write-once-read-many) storage for broker-dealer records — a centralized-custody requirement that may require routing specific retention flows to a centralized custodian even when day-to-day operations run local-first. See also: SOX, SEC. Specified in: Chapter 4 §Filter 2.

**Flease (Fast Lease)**
A distributed lease-acquisition protocol that provides bounded-failure mutex guarantees across a configured peer set without requiring a centralized coordinator. The local-node architecture uses Flease for CP-class record coordination — when a node needs to write a CP-class record, it acquires a Flease lease first; the safety guarantee is that two competing leases cannot both reach majority quorum on the same configured peer set. Reference: Stender et al. 2010. See also: CP-class. Specified in: Chapter 14 §Lease Coordination.

---

## G

**GDPR (General Data Protection Regulation)**
The EU's 2016 regulation (effective 2018) governing personal data processing for EU residents, including data-processing agreements (Article 28), cross-border transfer mechanisms (Chapter V), and data subject rights including erasure (Article 17). The local-node architecture addresses several GDPR obligations structurally — data residency, processor relationships with relay operators, and the right-to-erasure via crypto-shredding. See also: Schrems II, EU-US Data Privacy Framework. Specified in: Chapter 15; Appendix F.

**Gossip protocol**
A class of decentralized communication protocols where peers periodically exchange information with random other peers, achieving eventual convergence without a coordinator. The sync daemon uses gossip for peer discovery and anti-entropy delta exchange. Reference: Demers et al. 1987 (Epidemic Algorithms). See also: anti-entropy. Specified in: Chapter 14.

---

## H

**HIPAA (Health Insurance Portability and Accountability Act)**
The 1996 US law (with the 2003 Privacy Rule and 2005 Security Rule) governing protected health information. The Security Rule's technical safeguards (45 CFR §164.312) cover access control, audit logging, integrity, and transmission security — addressed in the local-node architecture by encryption-at-rest and role-scoped key management. The administrative safeguards (45 CFR §164.308) cover workforce training, access management, and contingency planning — these are operator-policy concerns that endpoints make harder, not easier, because each endpoint is its own access boundary. See also: BAA. Specified in: Chapter 4 §Filter 2; Chapter 15.

**HKDF (HMAC-based Key Derivation Function)**
A NIST-standard key derivation function (RFC 5869) that produces multiple distinct keys from a single high-entropy input. The local-node architecture uses HKDF-SHA256 to derive per-purpose keys from the OS-keystore root seed. Specified in: Chapter 15 §Key Hierarchy.

**HSM (Hardware Security Module)**
A dedicated hardware device that performs cryptographic operations and stores keys in tamper-resistant memory. The local-node architecture uses platform-provided hardware-backed keystores (Apple Secure Enclave, Pixel Titan M, Windows Pluton) where available; dedicated HSMs are a deployment option for high-sensitivity operator infrastructure. See also: TPM, Secure Enclave. Specified in: Chapter 23 §Endpoint Compromise.

---

## I

**IaaS (Infrastructure as a Service)**
A cloud-computing service model where the vendor provides computing infrastructure (servers, storage, networking) and the customer manages everything above the operating system. Used in the book primarily as a contrast point against the SaaS model — IaaS leaves data custody to the customer, while SaaS centralizes data custody at the vendor. See also: SaaS, PaaS.

---

## K

**KEK (Key Encryption Key)**
A longer-lived symmetric key used to wrap (encrypt) Data Encryption Keys (DEKs). KEKs are scoped per-role in the local-node architecture — a node holding a role's KEK can decrypt that role's DEKs. Key rotation is performed at the KEK layer; the rotated KEK re-wraps existing DEKs without requiring re-encryption of bulk data. See also: DEK, envelope encryption. Specified in: Chapter 15 §Key Hierarchy.

---

## L

**Local-first software**
Software that satisfies the seven properties from Kleppmann, Wiggins, van Hardenberg, and McGranaghan (2019): no spinners, work is not trapped on one device, the network is optional, seamless collaboration, the long now, security and privacy by default, and you retain ownership and control. The architecture in this book is one realization of the seven properties at production scale. See also: the seven ideals (Chapter 2). Specified in: Chapter 2.

**Loro**
A Rust-core CRDT library ([github.com/loro-dev/loro](https://github.com/loro-dev/loro)) that the Sunfish reference implementation targets as the aspirational engine when C# bindings mature. Currently, Sunfish ships YDotNet (the .NET port of Yjs); Loro is the longer-term target. See also: CRDT, YDotNet, Yjs. Specified in: Chapter 12.

---

## M

**MAUI (.NET Multi-platform App UI)**
Microsoft's cross-platform UI framework for building native desktop and mobile applications from a single .NET codebase. The Anchor accelerator uses MAUI Blazor Hybrid — a native MAUI shell embedding a Blazor WebView — to ship the same component surface as the Bridge accelerator's browser shell. Specified in: Chapter 11; Chapter 17.

**mDNS (Multicast DNS)**
A zero-configuration networking protocol (RFC 6762) that resolves hostnames on local networks without a DNS server. The sync daemon uses mDNS for peer discovery on the same LAN. Note: enterprise Wi-Fi configurations frequently filter mDNS multicast traffic; the next discovery tier (mesh VPN, then managed relay) handles those environments. Specified in: Chapter 14 §Peer Discovery.

**MDM (Mobile Device Management)**
Software that enterprises use to provision, configure, monitor, and secure managed endpoints — typically including app distribution, configuration profiles, certificate management, and remote wipe. The local-node architecture is designed to be MDM-deployable without bespoke onboarding; the installer model and configuration profiles are documented in Chapter 17 and Chapter 19.

---

## N

**NIST (National Institute of Standards and Technology)**
The US federal agency that publishes cryptographic standards (FIPS publications, Special Publications). The book references NIST SP 800-60 (security categorization), SP 800-12 (security overview), and the FIPS-197 (AES) and FIPS-198 (HMAC) standards as the basis for several architectural choices. Specified throughout Part III.

---

## O

**OAuth (Open Authorization)**
The IETF standard (current version OAuth 2.0, RFC 6749) for delegated authorization. The book references OAuth in the context of enterprise SSO integrations and federated identity for Bridge-pattern deployments. Specified in: Chapter 19 §SSO Integration.

---

## P

**PaaS (Platform as a Service)**
A cloud-computing service model between IaaS and SaaS — the vendor provides a managed application runtime, development tools, and middleware while the customer provides the application code and data. Used in the book primarily as a contrast point. See also: SaaS, IaaS.

**PDPA (Personal Data Protection Act)**
The shared name for personal-data-protection statutes across several Asian jurisdictions, including Singapore (PDPA 2012), Thailand (PDPA 2019), Malaysia (PDPA 2010), and Taiwan (PDPA). Each PDPA has different scope and enforcement; the book treats them as a regional cluster. Specified in: Appendix F.

**PIPL (Personal Information Protection Law, China 2021)**
China's comprehensive personal information protection law, effective November 2021. PIPL creates obligations comparable to GDPR for organizations handling Chinese residents' personal information, with significant differences in lawful bases, cross-border transfer requirements (security assessment + standard contract + certification), and the role of the Cyberspace Administration of China. Specified in: Appendix F.

**POPIA (Protection of Personal Information Act, South Africa 2013)**
South Africa's comprehensive personal data protection law (effective 2021). POPIA creates obligations comparable to GDPR for South African data subjects. Specified in: Appendix F.

**PowerSync**
A commercial sync framework for offline-first SQLite applications, with per-user sync rules. Discussed as prior art in Chapter 2 §What Exists Today. The architecture in this book takes a different position on data ownership — the local node holds authoritative state, not a derived view.

---

## R

**RBI (Reserve Bank of India)**
India's central bank and primary financial regulator. The 2018 RBI circular on payment data localization requires that all payment-system data be stored on servers physically located in India — addressed structurally by local-node deployments where authoritative data lives on user-controlled hardware in-jurisdiction. Specified in: Appendix F.

**Relay (managed relay)**
The optional infrastructure that helps local nodes find each other across NAT boundaries and serves as a fan-out point when direct LAN sync is not viable. The relay holds ciphertext only; it cannot read the payloads it routes. The relay is *architecturally* optional but *operationally* mandatory for the modal team across symmetric NATs. Self-hosted relays are supported with no protocol changes. See also: gossip protocol, mDNS. Specified in: Chapter 3 §Layer 5; Chapter 14 §Relay Trust Model.

**Replicache**
A commercial sync framework (from Rocicorp) that provides local-first reactivity through optimistic mutation against a server-authoritative backend. Discussed as prior art in Chapter 2 §What Exists Today. The architecture in this book takes the next step: the local node is the authoritative source, not a reactive cache.

**RFC (Request for Comments)**
The Internet Engineering Task Force's standard publication format. The book references several RFCs (5869 HKDF, 6762 mDNS, 6749 OAuth 2.0, 7009 OAuth Token Revocation, 8949 CBOR, 9420 MLS, others). Specified throughout Part III.

---

## S

**SaaS (Software as a Service)**
A cloud-computing service model where the vendor hosts the application and the customer accesses it over the network, typically with data stored on vendor infrastructure. The book's central argument is that the historical reasons for the SaaS bundle (technical necessity of centralized state, sync complexity, multi-device access) are now removable, and that local-node architectures provide a path that preserves the SaaS user experience without vendor data custody. See also: IaaS, PaaS, Bridge (Zone C).

**SBOM (Software Bill of Materials)**
A formal record of the components, libraries, and modules used to build a piece of software. SBOM publication is an enterprise procurement requirement in regulated industries and is increasingly required by US federal procurement (Executive Order 14028). The local-node architecture's release pipeline produces SBOMs for every published artifact. Specified in: Chapter 19 §Supply Chain.

**Schrems II**
The 2020 ruling of the EU Court of Justice (Case C-311/18) that invalidated the EU-US Privacy Shield framework and constrained EU personal data transfers to US cloud providers without supplemental safeguards. Schrems II created a structural argument for local-first data residency: data on user-controlled hardware in-jurisdiction does not raise the cross-border transfer question that Schrems II governs. See also: GDPR, EU-US Data Privacy Framework. Specified in: Chapter 4 §Filter 3; Appendix F.

**SOC 2 (Service Organization Control 2)**
An AICPA auditing framework for service organizations covering five Trust Services Criteria (security, availability, processing integrity, confidentiality, privacy). SOC 2 attestation is a common enterprise procurement requirement. The vendor's SOC 2 covers software-supply-chain controls; the customer's IT covers endpoint operation in a Zone A deployment. Specified in: Chapter 4 §Per-Zone Compliance Posture.

**SOX (Sarbanes-Oxley Act, 2002)**
The US law governing financial reporting controls for publicly traded companies. SOX §404 requires management to attest to the effectiveness of internal controls over financial reporting, including IT general controls. The book treats SOX-relevant audit-trail records as CP-class with append-only retention. Specified in: Chapter 13 §Audit Trail.

**SQLCipher**
An open-source SQLite extension that provides transparent AES-256 encryption at the database file level. The local-node architecture uses SQLCipher for all local data storage; the database key derives from the OS-keystore-stored root seed via HKDF. See also: HKDF. Specified in: Chapter 15 §Layer 1: Encryption at Rest.

**Sunfish**
The open-source reference implementation of the architecture this book describes. Source: [github.com/ctwoodwa/Sunfish](https://github.com/ctwoodwa/Sunfish). Sunfish ships the Anchor accelerator (Zone A), the Bridge accelerator (Zone C), and the kernel + foundation packages they share. Pre-1.0; in active development. Package references throughout the book follow the convention of naming packages without specifying class APIs.

---

## T

**Tailscale**
A mesh VPN service built on WireGuard that handles NAT traversal and provides stable peer-to-peer hostnames. The local-node architecture's mesh-VPN peer-discovery tier uses WireGuard; Tailscale is one production implementation. Specified in: Chapter 14.

**TPM (Trusted Platform Module)**
A hardware cryptographic module specified by ISO/IEC 11889. Modern endpoints use TPM 2.0 (or platform-equivalent — Apple Secure Enclave on macOS/iOS, Pixel Titan M on Pixel, Windows Pluton on recent Windows). The local-node architecture uses TPM-backed keystore storage where available for the device-identity keypair and the root seed. See also: HSM. Specified in: Chapter 23 §Endpoint Compromise.

---

## V

**Vector clock**
A distributed-systems primitive that tracks causal dependencies between events on different peers without requiring synchronized clocks. Each peer maintains a counter; an event includes the issuing peer's counter, and recipients update their local view of that peer's counter. The sync daemon uses per-document vector clocks (one entry per peer that has produced operations on that document) to identify which operations each peer has seen. Reference: Lamport 1978; Mattern 1989. Specified in: Chapter 14 §Anti-Entropy.

---

## W

**WireGuard**
An open-source VPN protocol designed for simplicity and high performance, included in the Linux kernel since 5.6. The local-node architecture's mesh VPN tier (Layer 5 of the discovery hierarchy) uses WireGuard to handle NAT traversal between peers on different networks. See also: Tailscale. Specified in: Chapter 14.

---

## Y

**YDotNet**
The .NET port of Yjs ([github.com/yjs/yjs](https://github.com/yjs/yjs)) via Rust FFI (Foreign Function Interface), used as the current CRDT engine in the Sunfish reference implementation. Sunfish's `ICrdtEngine` abstraction keeps the choice of CRDT library reversible — Loro is the aspirational target when C# bindings mature. See also: CRDT, Yjs, Loro. Specified in: Chapter 12.

**Yjs**
A JavaScript CRDT library ([github.com/yjs/yjs](https://github.com/yjs/yjs)) widely deployed in production collaborative applications. Yjs implements the document-tree-as-CRDT pattern; the local-node architecture builds on Yjs's merge semantics via the YDotNet .NET port. See also: CRDT, YDotNet. Specified in: Chapter 12.

---

## Z

**Zone A (Local-First Node)**
The book's name for the deployment shape where every user runs a complete local node and the relay is optional infrastructure. Realized by the Anchor accelerator. See also: Anchor, Zone B, Zone C. Specified in: Chapter 4.

**Zone B (Traditional SaaS)**
The book's name for the centralized-server deployment shape, used as a contrast point and as the correct answer for some workloads (atomic cross-user transactions, multi-tenant aggregation as core value, small-team-fast-ship greenfield). See also: SaaS, Zone A, Zone C. Specified in: Chapter 4.

**Zone C (Hybrid)**
The book's name for the deployment shape where the local node handles user-owned data and a hosted relay handles sync, cross-organization collaboration, and public-facing surfaces. Realized by the Bridge accelerator. The most frequent outcome for enterprise software teams adopting local-first incrementally. See also: Bridge, Zone A, Zone B. Specified in: Chapter 4.

---

*End of Appendix G.*
