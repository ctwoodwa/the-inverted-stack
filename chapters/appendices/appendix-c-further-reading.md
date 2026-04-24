# Appendix C — Further Reading

<!-- icm/prose-review -->

<!-- Target: ~1,000 words -->

---

Entries are organized by topic. Each annotation names what a practitioner gets from the source, not just what the source is.

---

## Section 1: Local-First Foundations

[1] M. Kleppmann, A. Wiggins, P. van Hardenberg, and M. McGranaghan, "Local-first software: You own your data, in spite of the cloud," in *Proc. ACM SIGPLAN Int. Symp. New Ideas, New Paradigms, and Reflections on Programming and Software (Onward! '19)*, Athens, Greece, Oct. 2019, pp. 154–178.

The paper that named the paradigm. Required reading before this book. Kleppmann et al. define the seven ideals of local-first software — offline capability, longevity, privacy, multi-device, collaboration, author ownership, and synchronization without vendor lock-in. The seven ideals are deliberately aspirational: the paper is a manifesto, not an engineering manual.

[2] Ink & Switch, "Local-first research project essays," Ink & Switch. [Online]. Available: https://www.inkandswitch.com/

Ink & Switch publishes detailed post-mortems of real local-first projects — Pushpin (a spatial canvas), Backchat (a messaging system), and others. These are the most honest accounts of what breaks in practice when building local-first software: the UX challenges of conflict resolution, the cognitive model users need, and the persistent gap between theory and production. Read the project essays before designing your UX layer.

---

## Section 2: CRDT Libraries

[3] K. Jahns, "Yjs: A CRDT for building collaborative applications," GitHub. [Online]. Available: https://github.com/yjs/yjs

Yjs is the most mature, most widely deployed CRDT library available. Its documentation covers every integration point, its ecosystem (y-websocket, y-indexeddb, y-monaco) is broad, and multiple production teams have benchmarked its performance at scale. If you are building on JavaScript or can use a webview approach, Yjs is the default choice. The Sunfish reference implementation currently uses YDotNet — the Yjs .NET port via Rust FFI — as the working engine; Loro (ADR 0028) is the aspirational primary target once loro-cs matures.

[4] Yjs Contributors, "y-crdt / yrs: The Rust port of the Yjs CRDT library," GitHub. [Online]. Available: https://github.com/y-crdt/y-crdt

The Rust port of Yjs, also called yrs, and the foundation for YDotNet — the .NET bindings currently used in the Sunfish reference implementation. The yrs codebase is the right place to understand how Yjs encoding and garbage collection work at the byte level. Evaluate the yrs release cadence against your project timeline before binding your project to it: the Rust port and JavaScript original do not always stay in sync across minor versions.

[5] Loro Contributors, "Loro: A CRDT library with rich text support," GitHub. [Online]. Available: https://github.com/loro-dev/loro

Loro is the aspirational primary CRDT engine for Sunfish (see ADR 0028 in the reference implementation). It offers a Rust core with efficient binary encoding, shallow snapshot support, and strong performance on high-churn documents. Its C# bindings (loro-cs) are community-maintained and minimal as of this writing; evaluate API coverage and maintenance status before adopting loro-cs in a production system. The loro-dev/loro repository is the right place to track progress on the .NET story.

[6] Automerge Contributors, "Automerge: A JSON-like data structure which can be modified concurrently," GitHub. [Online]. Available: https://github.com/automerge/automerge

Automerge is an excellent design reference with a clean, well-documented API and a substantial body of supporting research. The Automerge WASM build and JavaScript SDK are production-grade. As of this writing, Automerge has no first-class .NET binding. If your target platform is JavaScript or TypeScript, evaluate Automerge alongside Yjs.

---

## Section 3: Distributed Systems Foundations

[7] M. Kleppmann, *Designing Data-Intensive Applications*, 1st ed. Sebastopol, CA: O'Reilly Media, 2017.

The closest intellectual ancestor to this book. Chapters 5 (replication), 8 (distributed system troubles), and 9 (consistency and consensus) are required reading before designing a local-first architecture. Kleppmann explains why strong consistency is expensive and what you give up when you weaken it — the precise trade-off that motivates the AP/CP split in Chapter 12.

[8] M. Shapiro, N. Preguiça, C. Baquero, and M. Zawirski, "A comprehensive study of convergent and commutative replicated data types," INRIA, Tech. Rep. RR-7506, Jan. 2011.

The foundational CRDT theory paper. Dense and mathematical; not required for practitioners who are assembling existing CRDT libraries. Essential for anyone implementing a new CRDT type or contributing to the CRDT engine layer directly. Read it before writing any custom merge logic. The convergent vs. commutative distinction matters when deciding whether to carry full state or operation logs across the sync wire.

[9] H. Howard, D. Malkhi, and A. Spiegelman, "Flexible Paxos: Quorum intersection revisited," *arXiv:1608.06696*, Aug. 2016.

The theoretical basis for understanding quorum flexibility in distributed consensus. Flexible Paxos demonstrates that read and write quorums need only intersect, not be identical — context useful for understanding the quorum assumptions that underpin distributed lease protocols such as Flease.

---

## Section 4: Production Analogues

[10] Linear, "Scaling the Linear sync engine," Linear Engineering Blog. [Online]. Available: https://linear.app/blog

Linear's architecture is the closest public analogue to the AP-first data model in this book. Their client-replica approach — sync everything to the client, render from local state, treat the server as a replication peer rather than the authority — validates the core design at commercial scale. Linear's blog posts on their sync engine are the most useful production account available of how this model performs under real collaborative load.

[11] Actual Budget Contributors, "Actual: A local-first personal finance app," GitHub. [Online]. Available: https://github.com/actualbudget/actual

The closest commercial analogue to Zone A (pure local-first node). Actual stores all financial data locally, syncs peer-to-peer, and supports a self-hosted server for optional backup. Its architecture makes the trade-offs explicit: no server-side features, no analytics, no SaaS onboarding funnel, no per-seat billing. Study the Actual architecture before finalizing your Zone A monetization model.

---

## Section 5: Schema Evolution

[12] Ink & Switch, "Cambria: Translate your data with lenses," Ink & Switch, 2021. [Online]. Available: https://www.inkandswitch.com/cambria/

The Cambria paper introduces bidirectional schema lenses for CRDTs — the conceptual foundation for the schema migration approach in Chapter 13. A lens describes how to translate a document from schema version N to version N+1 and back, which is the property you need to maintain backward compatibility across a heterogeneous fleet of nodes running different software versions. The Cambria library is available for JavaScript. No .NET port exists; treat the paper as the specification for the lens abstraction and implement lens types for your document schemas.
