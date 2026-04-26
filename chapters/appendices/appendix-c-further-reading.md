# Appendix C — Further Reading

<!-- icm/prose-review -->

<!-- Target: ~2,500 words (revised from 1,000 after pass-1 board review) -->

---

Entries are organized by topic. Each annotation names what a practitioner gets from the source — not what the source is, but what reading it gives you. This is a curated practitioner list, not an exhaustive literature review. Categories deliberately omitted include general programming texts and language-specific framework references; practitioners will reach for those through their normal channels.

---

## Section 1: Local-First Foundations

[1] M. Kleppmann, A. Wiggins, P. van Hardenberg, and M. McGranaghan, "Local-first software: You own your data, in spite of the cloud," in *Proc. ACM SIGPLAN Int. Symp. New Ideas, New Paradigms, and Reflections on Programming and Software (Onward! '19)*, Athens, Greece, Oct. 2019, pp. 154–178, doi: 10.1145/3359591.3359737. [Online]. Available: https://www.inkandswitch.com/essay/local-first/

The paper that named the paradigm. Required reading before this book. Kleppmann and his coauthors define the seven ideals of local-first software — offline capability, longevity, privacy, multi-device, collaboration, author ownership, and synchronization without vendor lock-in. The ideals are deliberately aspirational. The paper is a manifesto, not an engineering manual.

[2] Ink & Switch, "Local-first research project essays," Ink & Switch. [Online]. Available: https://www.inkandswitch.com/

Ink & Switch publishes detailed post-mortems of real local-first projects — Pushpin (a spatial canvas), Backchat (a messaging system), and others. These are the most honest accounts of what breaks in practice when building local-first software: the UX challenges of conflict resolution, the cognitive model users need, and the persistent gap between theory and production. Read the project essays before you design your UX layer.

---

## Section 2: CRDT Libraries

[3] K. Jahns, "Yjs ([github.com/yjs/yjs](https://github.com/yjs/yjs), the JavaScript CRDT library): A CRDT for building collaborative applications," GitHub. [Online]. Available: https://github.com/yjs/yjs

Yjs is the most mature, most widely deployed CRDT library available. Its documentation covers every integration point. Its ecosystem — y-websocket, y-indexeddb, y-monaco — is broad. Multiple production teams have benchmarked its performance at scale. If you are building on JavaScript, or if you can adopt a webview approach, Yjs is the default choice. The Sunfish (the open-source reference implementation, [github.com/ctwoodwa/Sunfish](https://github.com/ctwoodwa/Sunfish)) reference implementation currently uses YDotNet (the .NET CRDT engine port of Yjs via Rust FFI) — the Yjs .NET port via Rust FFI (Foreign Function Interface) — as the working engine. Loro ([github.com/loro-dev/loro](https://github.com/loro-dev/loro), a Rust-core CRDT library) (ADR (Architecture Decision Record) 0028) is the aspirational primary target once loro-cs matures.

[4] Yjs Contributors, "y-crdt / yrs: The Rust port of the Yjs CRDT library," GitHub. [Online]. Available: https://github.com/y-crdt/y-crdt

The Rust port of Yjs — also called yrs — and the foundation for YDotNet, the .NET bindings the Sunfish reference implementation currently uses. The yrs codebase is the right place to understand how Yjs encoding and garbage collection work at the byte level. Evaluate the yrs release cadence against your project timeline before you bind to it. The Rust port and the JavaScript original do not always stay in sync across minor versions.

[5] Loro Contributors, "Loro: A CRDT library with rich text support," GitHub. [Online]. Available: https://github.com/loro-dev/loro

Loro is the aspirational primary CRDT engine for Sunfish (see ADR 0028 in the reference implementation). It offers a Rust core with efficient binary encoding, shallow snapshot support, and strong performance on high-churn documents. Its C# bindings (loro-cs) are community-maintained and minimal as of this writing. Evaluate API (Application Programming Interface) coverage and maintenance status before you adopt loro-cs in a production system. The loro-dev/loro repository is the right place to track progress on the .NET story.

[6] Automerge ([github.com/automerge/automerge](https://github.com/automerge/automerge), a JSON-like CRDT library) Contributors, "Automerge: A JSON-like data structure which can be modified concurrently," GitHub. [Online]. Available: https://github.com/automerge/automerge

Automerge is an excellent design reference. It has a clean, well-documented API and a substantial body of supporting research behind it. The Automerge WASM build and JavaScript SDK are production-grade. As of this writing, Automerge has no first-class .NET binding. If your target platform is JavaScript or TypeScript, evaluate Automerge alongside Yjs.

**Platform note.** Enterprise field-operations software in the GCC (Gulf Cooperation Council), South Asia, and Africa is predominantly Android (Java/Kotlin) and .NET (C# MAUI (.NET Multi-platform App UI), WPF) rather than JavaScript. For Android-first deployments, evaluate `automerge-kotlin` (the community port) alongside YDotNet running through Xamarin.Android bindings. For .NET-first deployments, YDotNet via the yrs FFI is the current production path. The JavaScript defaults implicit in the Yjs and Automerge annotations above require translation for these platforms.

---

## Section 3: Distributed Systems Foundations

[7] M. Kleppmann, *Designing Data-Intensive Applications*, 1st ed. Sebastopol, CA: O'Reilly Media, 2017.

The closest intellectual ancestor to this book. Chapters 5 (replication), 8 (distributed system troubles), and 9 (consistency and consensus) are required reading before you design a local-first architecture. Kleppmann explains why strong consistency is expensive and what you give up when you weaken it. That trade-off — what you give up, why it is worth it — is what motivates the AP/CP split in Chapter 12.

[8] M. Shapiro, N. Preguiça, C. Baquero, and M. Zawirski, "A comprehensive study of convergent and commutative replicated data types," INRIA, Tech. Rep. RR-7506, Jan. 2011.

The foundational CRDT theory paper. Dense and mathematical. Not required for practitioners assembling existing CRDT libraries. Essential for anyone implementing a new CRDT type or contributing to the CRDT engine layer directly. Read it before you write any custom merge logic. The convergent vs. commutative distinction matters when you decide whether to carry full state or operation logs across the sync wire.

[9] H. Howard, D. Malkhi, and A. Spiegelman, "Flexible Paxos: Quorum intersection revisited," *arXiv:1608.06696*, Aug. 2016.

The theoretical basis for understanding quorum flexibility in distributed consensus. Flexible Paxos demonstrates that read and write quorums need only intersect — they do not need to be identical. Useful context for the quorum assumptions that underpin distributed lease protocols such as Flease.

[10] D. Ongaro and J. Ousterhout, "In Search of an Understandable Consensus Algorithm," in *Proc. USENIX Annual Technical Conference (USENIX ATC '14)*, Philadelphia, PA, Jun. 2014, pp. 305–319.

The Raft paper. More widely implemented and more widely taught than Paxos variants. The consensus algorithm most practitioners encounter in production — etcd, Consul, CockroachDB, and TiKV all build on it. Read this alongside Flexible Paxos [9]. Raft gives you the understandable baseline. Flexible Paxos gives you the quorum flexibility to reason about weakened consistency models.

[11] E. Brewer, "Towards robust distributed systems," in *Proc. 19th Annual ACM SIGACT-SIGOPS Symposium on Principles of Distributed Computing (PODC 2000)*, Portland, OR, Jul. 2000, keynote.

The CAP conjecture as originally stated. The keynote slides are the canonical reference. Brewer's later 2012 retrospective ("CAP twelve years later") is also worth reading for the clarifications it makes. The book's AP/CP classification throughout Parts II and III rests on the framing this keynote introduced.

[12] S. Gilbert and N. Lynch, "Brewer's conjecture and the feasibility of consistent, available, partition-tolerant web services," *ACM SIGACT News*, vol. 33, no. 2, pp. 51–59, Jun. 2002.

The proof that formalizes Brewer's conjecture as the CAP theorem. Important for anyone who needs to defend AP/CP classification decisions against a rigorous reviewer. The theorem is a real constraint, not a design aesthetic.

[13] Y. Saito and M. Shapiro, "Optimistic replication," *ACM Computing Surveys*, vol. 37, no. 1, pp. 42–81, Mar. 2005.

The canonical survey of optimistic replication — the distributed-systems framing most closely aligned with what "local-first" operationally means. Read this before arguing AP semantics to an academic reviewer. The survey establishes the vocabulary — tentative commits, eventual convergence, conflict resolution — that the CRDT literature later built on.

[14] L. Lamport, "Time, clocks, and the ordering of events in a distributed system," *Communications of the ACM*, vol. 21, no. 7, pp. 558–565, Jul. 1978.

The foundational paper on logical time in distributed systems. The vector clock construction the Appendix A wire protocol uses originates here. Required reading for anyone who has to explain why logical time is not a detail. It is a correctness property.

---

## Section 4: Cryptography and Security

[15] T. Perrin, "The Noise Protocol Framework," Revision 34, Jul. 2018. [Online]. Available: https://noiseprotocol.org/noise.html

The specification for the Noise Protocol Framework, which the sync daemon (Appendix A) uses for transport-layer security. Section 7 of the specification defines the handshake patterns. Noise_XX is the relevant pattern for the protocol. Read this before you implement the daemon — the handshake choices interact with key rotation and re-keying in ways the sync daemon chapter specifies at a high level.

[16] Zetetic LLC, "SQLCipher Documentation," Zetetic. [Online]. Available: https://www.zetetic.net/sqlcipher/documentation/

SQLCipher is the encryption-at-rest layer for the local document store. The documentation covers key derivation (PBKDF2-HMAC-SHA512, 256,000 iterations by default), page-level encryption, and integrity verification. Read the "SQLCipher Design" section before evaluating at-rest security claims. The key derivation parameters are the first thing a security reviewer will audit.

[17] F. Denis et al., "libsodium Documentation," libsodium. [Online]. Available: https://doc.libsodium.org/

The cryptographic primitives library that Sunfish — and most comparable architectures — uses for Ed25519 signatures, ChaCha20-Poly1305 authenticated encryption, and Argon2id key derivation. libsodium's API documentation is the authoritative reference for algorithm parameters and side-channel-safe usage patterns. The "Usage" section is the practitioner's first read. The "Security considerations" section is where audit-driven questions get answered.

[18] A. Biryukov, D. Dinu, and D. Khovratovich, "Argon2: The memory-hard function for password hashing and other applications," in *Proc. IEEE European Symposium on Security and Privacy (EuroS&P)*, Saarbrücken, Germany, Mar. 2016, pp. 292–302. (Also IETF (Internet Engineering Task Force) RFC (Request for Comments) 9106, Sep. 2021.)

Argon2id is the key derivation function for the SQLCipher passphrase-to-key mapping and for the founder bootstrap in Chapter 17. The paper establishes the memory-hardness properties. RFC 9106 is the normative specification for parameter selection. Use the RFC 9106 parameters unless you have a specific reason otherwise.

[19] S. Josefsson and I. Liusvaara, "Edwards-Curve Digital Signature Algorithm (EdDSA)," IETF RFC 8032, Jan. 2017.

The normative specification for Ed25519, the signature algorithm the sync daemon uses for node identity and attestation. Appendix A requires Ed25519 compliance with RFC 8032. Deployments subject to FIPS 186-5 (2023) or GOST R 34.10-2012 need to verify algorithm approval separately.

---

## Section 5: Regulatory Primary Sources

This section provides primary source references for the regulatory frameworks the book cites throughout its compliance arguments. For jurisdiction-specific application of each law to local-first architecture, engage qualified legal counsel. These references establish the regulatory text, not the compliance posture.

[20] Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data (General Data Protection Regulation), *Official Journal of the European Union*, L 119/1, May 2016.

GDPR. Articles 5 (data minimization, purpose limitation, storage limitation), 17 (right to erasure), 25 (data protection by design and by default), 32 (security of processing), and 33–34 (breach notification) are the articles most directly engaged by local-first architecture decisions.

[21] Court of Justice of the European Union, "Case C-311/18 — Data Protection Commissioner v. Facebook Ireland Ltd and Maximillian Schrems," Judgment, Jul. 16, 2020.

Schrems II. The ruling that invalidated Privacy Shield and imposed strict supplementary measures on standard contractual clauses for EU-to-US data transfers. Local-first architecture is the most architecturally direct response: if personal data never leaves EU infrastructure, the cross-border transfer restriction never triggers. Read paragraphs 168–202 of the judgment for the reasoning on standard contractual clauses. That section is the one practitioners cite in compliance documentation.

[22] Government of India, The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023), Aug. 11, 2023.

DPDP. Sections 8 (purpose specification) and 12 (right to erasure) are the direct analogues of GDPR Articles 5 and 17 for Indian operations. Section 16 covers cross-border transfer and is structurally similar to Schrems II reasoning. RBI (Reserve Bank of India)'s April 6, 2018 circular on Storage of Payment System Data establishes stricter localization requirements for BFSI (Banking, Financial Services, and Insurance) data. Consult it alongside DPDP for financial-services deployments.

[23] Standing Committee of the National People's Congress, People's Republic of China, "Personal Information Protection Law," effective Nov. 1, 2021.

PIPL. Articles 38–43 establish cross-border transfer restrictions stricter than GDPR. For data on Chinese citizens, local-first architecture is often the only compliant path. Article 47 establishes the right to deletion. Article 57 requires breach notification to the Cyberspace Administration of China within three working days.

[24] Personal Information Protection Commission, Japan, "Act on the Protection of Personal Information (APPI / PIPA (Personal Information Protection Act))," Act No. 57 of 2003, revised 2022.

Japan PIPA. The 2022 revision tightened cross-border transfer rules and expanded breach notification obligations. Article 36 establishes the right to request cessation of processing — the same CRDT-log erasure implications discussed in the epilogue.

[25] Personal Information Protection Commission, Republic of Korea, "Personal Information Protection Act," Act No. 10465, 2011, most recently revised 2023.

Korea PIPA. The ISMS-P (Information Security Management System – Personal) (Information Security and Personal Information Management System) certification program is the procurement gate for Korean public sector and major enterprise deployments. Local-first architecture simplifies ISMS-P compliance in ways the certification body has documented publicly.

[26] United Arab Emirates, "Federal Decree-Law No. 45 of 2021 on the Protection of Personal Data," published Sep. 2021, effective Jan. 2, 2022. Dubai International Financial Centre, "DIFC Data Protection Law No. 5 of 2020," effective Jul. 1, 2020.

UAE DPL 2022 and DIFC DPL 2020. Practitioners deploying in Dubai financial services should start with the DIFC DPL — the older and more mature of the two. Practitioners deploying in mainland UAE follow the federal DPL. Both require clarity on whether personal data crosses a free-zone boundary or the UAE border.

[27] Republic of South Africa, "Protection of Personal Information Act, 2013 (Act No. 4 of 2013)," effective Jul. 1, 2021. Federal Republic of Nigeria, "Nigeria Data Protection Act, 2023" (re-enacting NDPR (Nigeria Data Protection Regulation) 2019).

POPIA (Protection of Personal Information Act) (South Africa) and NDPA (Nigeria Data Protection Act) (Nigeria). Both establish breach notification obligations and restrict cross-border transfer without adequate protection findings. POPIA Section 72 covers cross-border transfer. NDPA Section 41 covers lawful transfers. Local-first architecture provides a defensible answer to both — the data never crosses the border.

[28] Presidency of the Federative Republic of Brazil, "Lei No. 13.709, de 14 de agosto de 2018 (LGPD (Lei Geral de Proteção de Dados))," published Aug. 15, 2018, effective Sep. 18, 2020.

LGPD. Article 18 establishes the right to deletion. Article 48 requires breach notification to the ANPD (Brazilian Data Protection Authority). The structure is close to GDPR. The analogous right-to-erasure challenges for CRDT operation logs apply identically.

[29] Federation Council of the Federal Assembly of the Russian Federation, "Federal Law No. 242-FZ," Jul. 21, 2014, effective Sep. 1, 2015.

Federal Law 242-FZ. Establishes the requirement that personal data of Russian citizens be stored on servers physically located in Russia. Predates GDPR by two years. Served as the template for subsequent CIS (Commonwealth of Independent States) data localization laws — Kazakhstan, Belarus. Enforcement is real. Roskomnadzor blocked LinkedIn in 2016 for non-compliance.

---

## Section 6: Production Analogues

[30] T. Palmer, "Scaling the Linear ([linear.app](https://linear.app/), the issue tracker) sync engine to 100M+ records," Linear Engineering Blog, 2023. [Online]. Available: https://linear.app/blog/scaling-the-linear-sync-engine

Linear's architecture is the closest public analogue to the AP-first data model in this book. Their client-replica approach — sync everything to the client, render from local state, treat the server as a replication peer rather than the authority — validates the core design at commercial scale. The linked post covers write-order semantics, transaction boundaries, and partial sync for large workspaces. It is the most detailed production account of the model currently available in English. For additional posts, search the Linear blog for "sync engine."

[31] Actual Budget Contributors, "Actual: A local-first personal finance app," GitHub. [Online]. Available: https://github.com/actualbudget/actual

The closest commercial analogue to Zone A — the pure local-first node. Actual stores all financial data locally, syncs peer-to-peer, and supports a self-hosted server for optional backup. Its architecture makes the trade-offs explicit. No server-side features. No analytics. No SaaS (Software as a Service) onboarding funnel. No per-seat billing. Study the Actual architecture before you finalize your Zone A monetization model.

[32] Safaricom PLC and collaborators, "M-PESA System Architecture Documentation," Safaricom and GSMA Mobile Money programme resources; see also "M-PESA: The mobile payments revolution," Deutsche Gesellschaft für Internationale Zusammenarbeit (GIZ) case study, 2021.

M-PESA is the world's largest deployed offline-first financial system by transaction volume. Hundreds of millions of users. Multi-country deployment across East Africa. Two decades of production operation under intermittent connectivity. The store-and-forward architecture, delayed settlement semantics, and SIM-card-anchored identity predate "local-first" as a term — but they instantiate most of its principles. Read the GSMA Mobile Money architecture documentation before you assert that local-first cannot scale to hundreds of millions.

[33] FarmerLine, "Offline-first agricultural advisory: FarmerLine technical case study," FarmerLine Ltd., 2022. [Online]. Available via the GSMA AgriTech Programme.

FarmerLine serves millions of smallholder farmers across Ghana, Nigeria, and neighboring markets. Offline-capable advisory content. Voice-based interfaces in twenty-plus local languages. The store-and-forward voice content delivery and the multi-week offline operation intervals are the specific deployment contexts the book describes as baseline for rural Sub-Saharan African enterprise.

[34] Nubank, "How Nubank builds for offline-first mobile experiences," Nubank Engineering Blog. [Online]. Available: https://building.nubank.com.br/

The largest LATAM (Latin America) digital bank, serving over 100 million customers across Brazil, Mexico, and Colombia. Nubank's engineering blog documents offline-first mobile architecture patterns that serve rural customers with intermittent connectivity — the LATAM field-operations scenario the book's Chapter 1 vignette describes. Search the blog for "offline" or "eventual consistency" to find relevant posts.

[35] Apache Software Foundation, "Apache CouchDB Documentation," and PouchDB Contributors, "PouchDB: The Database That Syncs," [Online]. Available: https://docs.couchdb.org/ and https://pouchdb.com/

CouchDB and PouchDB are the longest-running production-grade offline-first database ecosystem. Deployment case studies span regulated healthcare (Medic Mobile's SMS-based health worker platform), education, and field operations. The replication protocol documentation is required reading for anyone evaluating bucket-based sync at scale. CouchDB's replication semantics predate CRDTs (Conflict-free Replicated Data Types) and resolve conflicts through multi-version concurrency control with application-level resolution. The architectural choice is different from CRDTs. The comparison illuminates the CRDT decision.

---

## Section 7: Schema Evolution

[36] Ink & Switch, "Cambria: Translate your data with lenses," Ink & Switch, 2021. [Online]. Available: https://www.inkandswitch.com/cambria/

Cambria lets you translate a document from schema version N to version N+1 and back without losing data — the exact capability you need to maintain backward compatibility across a heterogeneous fleet of nodes running different software versions. A lens is the conceptual foundation for the schema migration approach in Chapter 13. The Cambria library is available for JavaScript. No .NET port exists. Treat the paper as the specification for the lens abstraction and implement lens types for your document schemas.

---

## Section 8: Vendor Dependency Risk Case Studies

[37] "Western software companies' responses to the Russia-Ukraine conflict: 2022 service terminations, restrictions, and suspensions," composite of primary sources including Adobe press release (March 2022), Autodesk support communication (March 2022), Microsoft commercial activity announcement (March 2022), Figma ([figma.com](https://www.figma.com/), the design tool) platform notice (September 2022), and industry reporting in *The Verge*, *Reuters*, and *Interfax*.

The largest documented demonstration of vendor dependency risk in enterprise software history. Over a period of months in 2022, major Western SaaS providers suspended, restricted, or terminated service across Russia, Belarus, and adjacent CIS markets. Organizations that depended on vendor-hosted tooling for their operations lost access to their own data, to design systems, and to business-critical workflows. The event is the empirical case study for this book's thesis. For practitioners arguing the vendor dependency case in procurement review, cite the composite reality of the 2022 terminations rather than any single source. The documented breadth — not any individual incident — is the evidence.

---

## Section 9: Reference Implementation

[38] C. Wood et al., "Sunfish: The reference implementation for *The Inverted Stack*," GitHub. [Online]. Available: https://github.com/ctwoodwa/Sunfish

The open-source reference implementation developed alongside this book. Two canonical accelerators — **Anchor (the Zone A local-first desktop accelerator)** (Zone A local-first desktop, .NET MAUI Blazor Hybrid) and **Bridge (the Zone C hybrid SaaS accelerator)** (Zone C hybrid multi-tenant SaaS, .NET Aspire + Blazor Server). The repository's `docs/adr/` directory contains Architecture Decision Records. Start with ADR 0001 (architectural goals). Then ADR 0028 (CRDT engine selection, cross-referenced from Sections 2 and 5 above). The `accelerators/` directory contains the reference implementations organized by zone. Sunfish is pre-1.0. Package contracts are stable; method signatures are not. When Sunfish reaches 1.0, a companion release of this book will update implementation-specific references. For deployment knowledge — runbooks, post-mortems, annotated field experience — contribute to the repository's `docs/deployment-experience/` directory per the epilogue's contribution guidance.
