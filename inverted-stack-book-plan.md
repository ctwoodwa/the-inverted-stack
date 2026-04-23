# The Inverted Stack — Book Writing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task.
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Write all chapters and supporting files for *The Inverted Stack: Local-First Nodes
in a SaaS World*, a self-published practitioner book, organized as manageable markdown files
ready for final assembly.

**Architecture:** 20 chapters + preface + epilogue + 4 appendices, written in dependency
order (Part I → Part II → Part III → Part IV), with Part II council chapters parallelizable
and Part III reference chapters largely parallelizable. Each deliverable is a standalone
markdown file under `inverted-stack-book/`.

**Source material (all in `C:\Users\Chris\Dropbox\ideas\local-first\`):**
- `local_node_saas_v13.md` — primary architecture paper (referred to as **v13**)
- `inverted-stack-v5.md` — companion paper with .NET specifics (referred to as **v5**)
- `kleppmann_council_review.md` — Round 1 adversarial review (referred to as **R1**)
- `kleppmann_council_review2.md` — Round 2 review (referred to as **R2**)
- `book-structure.md` — approved structure with word count targets and writing rules

**Reference implementation:** `C:\Projects\Sunfish\`

---

## Quality Checklist (apply to every chapter before marking complete)

Run this checklist before each commit step. A chapter is not done until all items pass.

```
[ ] QC-1  Word count within ±10% of target
[ ] QC-2  Every topic listed in book-structure.md for this chapter is addressed
[ ] QC-3  Source sections cited inline where claims come directly from papers
[ ] QC-4  Sunfish packages referenced by name (Sunfish.Kernel.Sync) not class API
[ ] QC-5  No academic scaffolding ("this paper argues", "as we have seen", "the author contends")
[ ] QC-6  No re-introducing the architecture (body chapters assume Part I is read)
[ ] QC-7  Part III chapters: specification voice (what it is, how it works fully)
          Part IV chapters: tutorial voice (minimal path, references Part III)
[ ] QC-8  Ch 2 only: opinionated not encyclopedic — one paragraph per prior work,
          ends with crisp statement of what this book adds
[ ] QC-9  Council chapters only: two-act structure (Round 1 failure → what changed → Round 2 verdict)
[ ] QC-10 No placeholder text ("TBD", "expand here", "see paper for details")
```

---

## Phase 0 — Scaffold

### Task 0: Create folder structure and ASSEMBLY.md

**Files to create:**
```
C:\Users\Chris\Dropbox\ideas\local-first\inverted-stack-book\
  ASSEMBLY.md
  front-matter\
    foreword-placeholder.md
    preface.md
  part-1-thesis-and-pain\
    ch01-when-saas-fights-reality.md
    ch02-local-first-serious-stack.md
    ch03-inverted-stack-one-diagram.md
    ch04-choosing-your-architecture.md
  part-2-council-reads-the-paper\
    ch05-enterprise-lens.md
    ch06-distributed-systems-lens.md
    ch07-security-lens.md
    ch08-product-economic-lens.md
    ch09-local-first-practitioner-lens.md
    ch10-synthesis.md
  part-3-reference-architecture\
    ch11-node-architecture.md
    ch12-crdt-engine-data-layer.md
    ch13-schema-migration-evolution.md
    ch14-sync-daemon-protocol.md
    ch15-security-architecture.md
    ch16-persistence-beyond-the-node.md
  part-4-implementation-playbooks\
    ch17-building-first-node.md
    ch18-migrating-existing-saas.md
    ch19-shipping-to-enterprise.md
    ch20-ux-sync-conflict.md
  epilogue\
    epilogue-what-the-stack-owes-you.md
  appendices\
    appendix-a-sync-daemon-wire-protocol.md
    appendix-b-threat-model-worksheets.md
    appendix-c-further-reading.md
    appendix-d-testing-the-inverted-stack.md
```

- [ ] **Step 1: Create all directories and stub files**

  Create each directory and a stub `.md` file containing only the chapter title as an H1.
  Example stub content for `ch01-when-saas-fights-reality.md`:
  ```markdown
  # Chapter 1 — When SaaS Fights Reality
  <!-- stub -->
  ```

- [ ] **Step 2: Write ASSEMBLY.md**

  Create `ASSEMBLY.md` with the following content:

  ```markdown
  # Assembly Instructions — The Inverted Stack

  ## Pandoc (recommended for ePub/PDF)

  ```bash
  pandoc \
    front-matter/foreword-placeholder.md \
    front-matter/preface.md \
    part-1-thesis-and-pain/ch01-when-saas-fights-reality.md \
    part-1-thesis-and-pain/ch02-local-first-serious-stack.md \
    part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md \
    part-1-thesis-and-pain/ch04-choosing-your-architecture.md \
    part-2-council-reads-the-paper/ch05-enterprise-lens.md \
    part-2-council-reads-the-paper/ch06-distributed-systems-lens.md \
    part-2-council-reads-the-paper/ch07-security-lens.md \
    part-2-council-reads-the-paper/ch08-product-economic-lens.md \
    part-2-council-reads-the-paper/ch09-local-first-practitioner-lens.md \
    part-2-council-reads-the-paper/ch10-synthesis.md \
    part-3-reference-architecture/ch11-node-architecture.md \
    part-3-reference-architecture/ch12-crdt-engine-data-layer.md \
    part-3-reference-architecture/ch13-schema-migration-evolution.md \
    part-3-reference-architecture/ch14-sync-daemon-protocol.md \
    part-3-reference-architecture/ch15-security-architecture.md \
    part-3-reference-architecture/ch16-persistence-beyond-the-node.md \
    part-4-implementation-playbooks/ch17-building-first-node.md \
    part-4-implementation-playbooks/ch18-migrating-existing-saas.md \
    part-4-implementation-playbooks/ch19-shipping-to-enterprise.md \
    part-4-implementation-playbooks/ch20-ux-sync-conflict.md \
    epilogue/epilogue-what-the-stack-owes-you.md \
    appendices/appendix-a-sync-daemon-wire-protocol.md \
    appendices/appendix-b-threat-model-worksheets.md \
    appendices/appendix-c-further-reading.md \
    appendices/appendix-d-testing-the-inverted-stack.md \
    -o inverted-stack-complete.epub \
    --toc --toc-depth=2 \
    --metadata title="The Inverted Stack: Local-First Nodes in a SaaS World"
  ```

  ## Leanpub
  Leanpub reads from a `manuscript/` folder with a `Book.txt` index file.
  Point `Book.txt` at the files above in assembly order.

  ## Word count check
  ```bash
  wc -w **/*.md
  ```
  Target: 80,000–86,000 words total.
  ```

- [ ] **Step 3: Save all files**

---

## Phase 1 — Prospectus and Front Matter

### Task 1: Prospectus

**File:** `C:\Users\Chris\Dropbox\ideas\local-first\inverted-stack-book\prospectus.md`
**Target:** 2,500–3,500 words
**Sources:** Both papers (abstracts + executive summaries), book-structure.md

- [ ] **Step 1: Write the prospectus outline**

  Create these sections as headers with bullet-point notes before writing prose:
  ```
  ## The Problem This Book Solves
  ## The Thesis
  ## Original Contribution
  ## Intended Audience
  ## Structure and Scope
  ## The Kleppmann Council as Evaluation Method
  ## Why Self-Publishing
  ## The Reference Implementation (Sunfish)
  ## Comparable Works
  ## Word Count and Timeline
  ```

- [ ] **Step 2: Write "The Problem This Book Solves" (~400 words)**

  Draw from: v13.md Abstract and Executive Summary; v5.md §1 Problem Statement.

  Cover: The SaaS bundle (what users want vs. what they're forced to accept). The dependency
  that appeared inseparable but isn't. The specific conditions under which it breaks
  (vendor shutdown, connectivity loss, data sovereignty requirements).

- [ ] **Step 3: Write "The Thesis" (~300 words)**

  State it directly: local-node architecture with CRDT-based synchronization delivers
  collaboration-equivalent functionality to centralized SaaS while structurally guaranteeing
  data sovereignty. The cloud becomes a peer, not an authority.

  Include the comparison table from v13.md Executive Summary (Conventional SaaS vs.
  Local-Node Architecture across 9 properties).

- [ ] **Step 4: Write "Original Contribution" (~300 words)**

  This book's contribution is the composition: assembling individually production-validated
  components (CRDTs, leaderless replication, gossip protocols, event sourcing, envelope
  encryption) into a coherent, deployable architecture with a formal evaluation record.

  Name what each source paper contributes and what the book adds beyond them.

- [ ] **Step 5: Write remaining sections (~1,500 words combined)**

  - **Intended Audience:** The three audiences from v13.md Preface. Primary: software
    architects, technical founders, senior engineers. Secondary: IT decision-makers.
  - **Structure and Scope:** Brief tour of all four parts and what each delivers.
  - **The Kleppmann Council:** Five adversarial reviewers, two rounds, all blocks cleared.
    Name each council member and their lens. Explain why this is a more rigorous evaluation
    than a standard peer review.
  - **Why Self-Publishing:** Control over structure, release cadence, and updates. The book
    and the reference implementation evolve together.
  - **The Reference Implementation:** Sunfish: what it is, Anchor (Zone A) and Bridge
    (Zone C), pre-1.0 status, how to find it.
  - **Comparable Works:** Kleppmann's DDIA (closest intellectual ancestor — same depth,
    different domain). What this book covers that DDIA doesn't.
  - **Word Count and Timeline:** ~83,500 words. Self-paced release — Part I first,
    then parts released incrementally.

- [ ] **Step 6: Quality check**
  ```
  [ ] Prospectus makes a clear claim about what is novel
  [ ] Council evaluation is presented as a genuine peer-review mechanism
  [ ] Sunfish pre-1.0 status is disclosed
  [ ] No academic hedging language
  [ ] Readable by a technical founder who has never heard of CRDTs
  ```

- [ ] **Step 7: Save**

---

### Task 2: Foreword Placeholder + Preface

**Files:**
- `front-matter/foreword-placeholder.md`
- `front-matter/preface.md`
**Targets:** Foreword placeholder: 200 words. Preface: 1,200–1,500 words.

- [ ] **Step 1: Write foreword-placeholder.md**

  ```markdown
  # Foreword

  *This page is reserved for a foreword from a recognized voice in the local-first
  community — an Automerge/Yjs maintainer, an Ink & Switch contributor, or a practitioner
  who has shipped a production local-first system.*

  *If you would like to contribute a foreword, contact [author contact].*

  ---
  <!-- PLACEHOLDER: Replace this file before final publication -->
  ```

- [ ] **Step 2: Write preface outline and prose (~1,300 words)**

  Sections:
  - **Why I wrote this** — the gap between local-first ideals and production-grade systems;
    the experience of designing an architecture that passes adversarial review
  - **Who this book is for** — three audiences (architects/engineers, enterprise
    evaluators/IT, OSS contributors/founders); how to read it by audience
  - **How to read this book** — Part I convinces, Part II stress-tests, Part III specifies,
    Part IV implements; Parts III and IV are reference sections you return to
  - **A note on Sunfish** — the open-source reference implementation
    (`github.com/ctwoodwa/Sunfish`); Anchor (Zone A) and Bridge (Zone C); pre-1.0;
    Sunfish references in this book are by package name, not class API
  - **A note on the CRDT engine** — the book specifies Loro as aspirational primary for
    compact encoding and shallow snapshots; the Sunfish reference implementation uses
    YDotNet (Yjs .NET) while loro-cs matures; the `ICrdtEngine` abstraction keeps the
    choice reversible
  - **A note on the Kleppmann Council** — five domain experts, two rounds of adversarial
    review; how to use Part II

- [ ] **Step 3: Quality check**
  ```
  [ ] Preface is personal, not academic — first-person, direct
  [ ] Foreword placeholder makes it easy for a contributor to know what's expected
  [ ] CRDT engine discrepancy disclosed clearly and without apology
  [ ] Sunfish pre-1.0 disclaimer present
  ```

- [ ] **Step 4: Save both files**

---

## Phase 2 — Part I: The Thesis and the Pain

*Dependencies: Prospectus complete. Chapters can be written Ch1 → Ch2 → Ch3 → Ch4 in order;
each builds on the previous.*

---

### Task 3: Chapter 1 — When SaaS Fights Reality

**File:** `part-1-thesis-and-pain/ch01-when-saas-fights-reality.md`
**Target:** 4,000–5,000 words
**Sources:** v13.md §3 (Reframing the SaaS Contract), v13.md Executive Summary,
v5.md §1 (Problem Statement)

- [ ] **Step 1: Write chapter outline**

  ```
  ## The Bundle Nobody Agreed To
  ## Five Ways SaaS Breaks in the Field
    ### 1. The Outage That Takes Your Work With It
    ### 2. The Vendor That Disappears
    ### 3. The Connectivity That Wasn't There
    ### 4. The Data You Can't Get Back
    ### 5. The Price That Changes After You've Committed
  ## Who Pays the Most
  ## Why Users Have Accepted This
  ## The Dependency That Looks Inevitable
  ```

- [ ] **Step 2: Write "The Bundle Nobody Agreed To" (~600 words)**

  The SaaS contract bundles three desirable properties (collaboration, multi-device access,
  zero-maintenance) with three that users would reject if offered separately (vendor data
  custody, vendor-controlled pricing, service continuity contingent on vendor survival).

  Draw from: v13.md §3 and Executive Summary. Make it concrete immediately — open with a
  specific scenario, not an abstract claim.

- [ ] **Step 3: Write "Five Ways SaaS Breaks in the Field" (~2,000 words)**

  Each subsection: one concrete failure mode, one real-world domain example, the specific
  harm, and why the conventional architecture makes it structurally unavoidable.

  - **Outage:** Project management tool down during a bid deadline. Construction PM example
    from v5.md §7 (construction vertical). The team has the data — it's on the server —
    but can't reach it.
  - **Vendor disappears:** Pull examples from well-known SaaS shutdowns (Sunrise calendar,
    Quip, others). The data export problem.
  - **Connectivity:** Field work, rural offices, legal depositions, hospital floors, air-gapped
    facilities. v13.md §20.4 (Filter 3: Connectivity). Not an edge case — a standard condition
    for entire industries.
  - **Data retrieval:** Rate-limited exports, proprietary formats, data that "belongs" to
    the user but requires vendor cooperation to access. v13.md §3.
  - **Pricing:** Mid-contract price changes, per-seat escalation, feature paywalls added
    post-adoption. The lock-in that makes switching expensive enough to be effectively permanent.

- [ ] **Step 4: Write "Who Pays the Most" + "Why Users Have Accepted This" (~900 words)**

  Who pays most: SMBs and professionals with minimal IT (legal, medical, construction,
  consultancies) — the organizations least equipped to negotiate enterprise data agreements.
  v13.md §14.1.

  Why accepted: The desirable properties appeared inseparable from the centralized
  infrastructure. CRDTs didn't exist at scale. Leaderless replication wasn't desktop-viable.
  Container runtimes weren't consumer-installable. The dependency looked structural because
  it *was* structural — until recently. v13.md §4 (hardware viability).

- [ ] **Step 5: Write "The Dependency That Looks Inevitable" (~500 words)**

  Closing section: the dependency isn't structural anymore. Name the enabling technologies
  briefly (CRDTs in production, gossip protocols at scale, desktop container runtimes).
  Don't describe the architecture yet — that's Ch 3. Set up the question Ch 2 answers.

- [ ] **Step 6: Quality check against QC-1 through QC-10**

- [ ] **Step 7: Save**

---

### Task 4: Chapter 2 — Local-First: From Sync Toy to Serious Stack

**File:** `part-1-thesis-and-pain/ch02-local-first-serious-stack.md`
**Target:** 3,500–4,500 words
**Sources:** v13.md §2.1, v5.md §1 (extending local-first)
**Writing discipline:** QC-8 applies — opinionated not encyclopedic

- [ ] **Step 1: Write chapter outline**

  ```
  ## The Seven Ideals
  ## What Exists Today: A Taxonomy of Local-First Attempts
    ### The Document Sync Apps (Obsidian, Notion)
    ### The Lightweight Replica Apps (Linear, Liveblocks)
    ### The Local-First Finance App (Actual Budget)
    ### The Research Prototypes (Automerge, Ink & Switch essays)
  ## What Each Gets Right — and Where It Stops
  ## The Missing Step: Full Node, Not Smart Cache
  ## What This Book Adds
  ```

- [ ] **Step 2: Write "The Seven Ideals" (~600 words)**

  Cover Kleppmann et al.'s seven local-first ideals from R2 Tomás Ferreira's prompt response
  (the checklist against v2). For each: name it, one sentence on what it means in practice,
  one sentence on why most apps fail it.

  1. No spinners, no waiting
  2. Work is not trapped on one device
  3. Network is optional
  4. Seamless collaboration
  5. The long now (data outlives the vendor)
  6. Security and privacy by default
  7. You retain ultimate ownership and control

- [ ] **Step 3: Write "What Exists Today" (~1,400 words — ~350 words per entry)**

  For each existing approach: what it does, exactly where it stops short, why that gap matters.
  Be specific and direct. Do not soften criticism.

  - **Obsidian:** Plain markdown files locally, sync via proprietary service. No CRDT —
    conflicts produce duplicate files. No structured data model. Single-user in practice.
    Gap: can't handle team workflows with structured, relational data.
  - **Linear:** Local SQLite replica, server sync, proprietary protocol. Fast reads, good UX.
    Gap: not a full node — no background jobs, no offline writes to server-owned records,
    no peer-to-peer sync if Linear's servers are down.
  - **Actual Budget:** Full local-first financial app, no server required, file export.
    Closest commercial analogue to what this book describes. Gap: single-user, no team
    collaboration, no real-time multi-device sync without their optional sync service
    (which reintroduces a central server).
  - **Automerge / Ink & Switch research:** Correct theory, excellent reference implementations.
    Gap: document-centric, assumes a sync backend exists, no production deployment story,
    no enterprise governance model.

- [ ] **Step 4: Write "The Missing Step" + "What This Book Adds" (~1,000 words)**

  The missing step: running the *entire* stack locally — UI, business logic, sync daemon,
  storage — not just a smarter cache. The distinction from v5.md §1's core question:
  "What if a user's workstation ran a full node of the system — including state, business
  logic, and sync — such that 'the cloud' is merely another peer, not the source of truth?"

  What this book adds: the composition. Not inventing new primitives — assembling proven ones
  (CRDTs from Figma, gossip from Cassandra, desktop containers from Docker Desktop, declarative
  sync from PowerSync) into a coherent architecture with a governance model, a security
  model, and a business model. The production-analogues table from v13.md §19.

- [ ] **Step 5: Quality check (QC-1 through QC-10, note QC-8)**

- [ ] **Step 6: Save**

---

### Task 5: Chapter 3 — The Inverted Stack in One Diagram

**File:** `part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md`
**Target:** 2,500–3,500 words
**Sources:** v13.md §5 (Kernel Architecture), v5.md §2 (Architectural Overview),
Sunfish `accelerators/anchor/README.md`, `accelerators/bridge/README.md`

- [ ] **Step 1: Write chapter outline**

  ```
  ## The Inversion in One Sentence
  ## The Five Layers
    ### Layer 1: Presentation
    ### Layer 2: Application Logic
    ### Layer 3: Sync Daemon
    ### Layer 4: Storage
    ### Layer 5: Relay and Discovery
  ## How This Changes Failure Modes
  ## The Two Canonical Shapes: Anchor and Bridge
  ## What Changes for the Developer
  ```

- [ ] **Step 2: Write the inversion + five layers (~1,200 words)**

  Open with the core inversion stated as sharply as possible:

  > Conventional SaaS: Cloud database is primary → local device caches and renders.
  > Local-Node Architecture: Local node is primary → cloud relay is an optional sync peer.

  From v13.md Executive Summary comparison table and v5.md §2.1.

  For each layer, describe: what runs there, what it owns, what it does not own, and what
  happens to it when the network is unavailable. Use the v5.md §2.2 layered model as the
  skeleton; enrich with v13.md §5's kernel/plugin split.

- [ ] **Step 3: Write "How This Changes Failure Modes" (~700 words)**

  The conventional failure modes disappear (vendor outage = no data access, connectivity
  loss = degraded mode). The new failure modes appear (endpoint compromise expands attack
  surface, schema migration complexity increases, GC debt accumulates).

  Draw from: v13.md §11.1 (threat model framing), v13.md §7 (schema migration motivation).
  Be honest about both — this section earns credibility for the rest of the book.

- [ ] **Step 4: Write "The Two Canonical Shapes" (~600 words)**

  Introduce Anchor and Bridge as named, real implementations.

  - **Anchor** (Zone A): `.NET MAUI Blazor Hybrid`, offline-by-default, local SQLCipher,
    Ed25519 device keys. The desktop node in its pure form.
    From: `accelerators/anchor/README.md` — role in architecture section, Zone A framing.
  - **Bridge** (Zone C): `.NET Aspire`, Blazor Server, per-tenant data-plane isolation,
    hosted-node-as-SaaS. The hybrid shape where the vendor runs a peer, not the authority.
    From: `accelerators/bridge/README.md` — Zone C hybrid architecture section.

  Both use the same Sunfish component surface. Both implement the same sync protocol.
  The difference is where the authoritative data lives.

- [ ] **Step 5: Write "What Changes for the Developer" (~400 words)**

  Closing orientation: this book's job is to specify the full architecture so you can
  build either shape. Part II (the council) establishes the constraints it must satisfy.
  Part III (reference architecture) specifies each component. Part IV (playbooks) shows
  you how to build.

- [ ] **Step 6: Quality check (QC-1 through QC-10)**

- [ ] **Step 7: Save**

---

### Task 6: Chapter 4 — Choosing Your Architecture

**File:** `part-1-thesis-and-pain/ch04-choosing-your-architecture.md`
**Target:** 3,000–4,000 words
**Sources:** v13.md §20 (Architecture Selection Framework — entire section)

- [ ] **Step 1: Write chapter outline**

  ```
  ## The One Question That Decides Everything
  ## Filter 1: Consistency Requirements (Hard Stop)
  ## Filter 2: Data Ownership Profile
  ## Filter 3: Connectivity and Operational Environment
  ## Filter 4: Business Model Alignment
  ## Filter 5: Team Capability and Timeline
  ## The Three Outcome Zones
  ## The Practical Shortcut
  ## Anchor Is Your Zone A. Bridge Is Your Zone C.
  ```

- [ ] **Step 2: Write the chapter (~3,200 words)**

  This chapter is almost entirely drawn from v13.md §20. Translate directly but with
  practitioner prose, not specification voice.

  - **The one question:** Does primary value derive from the user's own data, or from
    aggregating across users? This is not rhetorical — answer it for your product before
    reading further.

  - **Filters 1–5:** Use the tables from v13.md §20.2–20.5 directly, but precede each
    table with a short paragraph explaining what the filter is testing and why it matters.
    Filter 1 gets the most emphasis: the CAP theorem is not a negotiating position.
    If a transaction must be atomic across multiple users simultaneously — stop. This is
    not the architecture for that.

  - **Three outcome zones:** Zone A (local-first node), Zone B (traditional SaaS/website),
    Zone C (hybrid). Anchor = Zone A, Bridge = Zone C, named explicitly.

  - **Practical shortcut:** The three questions from v13.md §20.8. If all three are true,
    Zone A/C is the default.

  - **Closing:** This is the last chapter before the architecture is stress-tested in
    Part II. If you ran the filters and the architecture applies to your problem, the
    council's job — starting in the next chapter — is to find every way it fails.

- [ ] **Step 3: Quality check (QC-1 through QC-10)**

- [ ] **Step 4: Save**

---

## Phase 3 — Part II: The Council Reads the Paper

*Dependencies: Ch 3 must be complete (council chapters reference the architecture overview).
Ch 5 through Ch 9 can be written in parallel — each covers one council member independently.
Ch 10 (Synthesis) depends on Ch 5–9 being complete.*

*Two-act structure for Ch 5–9 (QC-9):*
*Act 1: The council member's lens + Round 1 objections + what blocked or conditioned the verdict.*
*Interlude: What changed between rounds.*
*Act 2: Round 2 prompts + revised scores + verdict + the takeaway principle.*

---

### Task 7: Chapter 5 — The Enterprise Lens

**File:** `part-2-council-reads-the-paper/ch05-enterprise-lens.md`
**Target:** 3,000–4,000 words
**Sources:** R1 Dr. Voss section, R2 Member 1 Dr. Voss section,
v13.md §16 (IT Governance), v5.md §5 (Deployment in Managed Environments)

- [ ] **Step 1: Write Act 1 (~1,200 words)**

  Open with Dr. Voss's persona from R1: 22 years in enterprise IT governance, personal scar
  tissue from three failed rollouts blocked by MDM policy. Her core lens: will this pass a
  real procurement committee?

  Her Round 1 dimension scores with rationale (draw from R1 verbatim where possible):
  - MDM integration: named Intune/Jamf but hand-wavy on specific policies
  - Incident response: CRDT audit trail ≠ IR runbook (this was the BLOCK)
  - SBOM: committed but no toolchain named
  - Container updates: zero-downtime path unspecified

  The blocking issue: no formal incident response procedure. "CRDT audit trail exists" is
  not a substitute for a defined IR runbook. BLOCK verdict with rationale.

- [ ] **Step 2: Write interlude — what changed (~500 words)**

  What the architecture added between rounds to satisfy Voss's concerns:
  - Incident response runbook: triggering events, artifact collection, chain of custody,
    communication protocol
  - Named SBOM toolchain: Syft for generation, Grype for vulnerability scanning, CVE response SLA
  - Relay traffic over port 443 / TLS 1.3 only, with PAC file and corporate proxy compatibility
  - Zero-downtime container update path specified (rolling update with health-check gate)
  - MDM compliance check at capability negotiation — the architectural detail Voss commended

- [ ] **Step 3: Write Act 2 (~1,000 words)**

  Round 2 prompt responses (from R2 Voss section):
  - Security audit framing: SBOM in CycloneDX, rootless Podman, three-port network footprint
  - MDM deployment: MSIX + Intune path; Podman WSL2 vs. Hyper-V substrate question
  - Deprovisioning: admin tooling gap — cryptographic description vs. actual admin interface
  - Migration: four-phase reversible model earns commendation
  - Procurement: AGPLv3 copyleft enterprise customization concern

  Round 2 verdict: PROCEED WITH CONDITIONS. Conditions: SBOM CI/CD timing, Podman
  substrate documentation, admin tooling sketch, phase-transition success criteria,
  AGPLv3 dual-license strategy.

  **Takeaway principle:** The non-negotiable enterprise constraints are MDM-compatible
  installation, signed/notarized binaries, SBOM, and a defined incident response process.
  An architecture without these will not pass procurement regardless of its technical merit.

- [ ] **Step 4: Quality check (QC-1 through QC-10, note QC-9)**

- [ ] **Step 5: Save**

---

### Task 8: Chapter 6 — The Distributed Systems Lens

**File:** `part-2-council-reads-the-paper/ch06-distributed-systems-lens.md`
**Target:** 3,000–4,000 words
**Sources:** R1 Prof. Shevchenko section, R2 Member 2 Shevchenko section,
v13.md §2 (Theoretical Foundations), v13.md §6 (Sync Architecture), v13.md §9 (CRDT GC)

- [ ] **Step 1: Write Act 1 (~1,200 words)**

  Shevchenko's persona: associate professor, 14 papers on CRDT correctness, personally
  debugged five production CRDT deployments that diverged "in ways the theory said were
  impossible." Zero tolerance for optimism about network partitions.

  Two BLOCK issues from R1:
  1. CRDT GC strategy absent — long-running nodes accumulate unbounded op log history.
     Without checkpoint interval or retention window, this causes production failures
     after 12 months.
  2. Flease split-write window — if the lease holder goes offline mid-write and a new
     lease is elected, two nodes may simultaneously believe they hold write authority.
     Must prove this is safe or specify a fence.

  Explain each technically: why unbounded op log growth fails, what a split-write window
  means for data integrity.

- [ ] **Step 2: Write interlude — what changed (~500 words)**

  Resolutions between rounds:
  - Three-tier GC policy: Yjs aggressive GC for ephemeral data, Loro 90-day retention
    for business records, no-GC for compliance records
  - Flease split-write proof: CP-class records use CRDT merge semantics for the
    write window — the CRDT handles the race, the lease prevents double-booking
  - Stale peer recovery protocol added: when reconnecting peer's vector clock predates
    GC horizon, full-state snapshot transfer replaces incremental stream
  - Reconnection storm handling: gossip anti-entropy throttled per-tick by resource governor

- [ ] **Step 3: Write Act 2 (~1,000 words)**

  Round 2 prompts (from R2 Shevchenko section):
  - Correctness under partition: Flease treatment now correct; relay-as-Flease-participant
    for two-person teams is architecturally elegant
  - GC safety: stale peer gap — if a peer has been offline 95 days and GC horizon is 90,
    it requests operations the originating node has already GC'd. Fix: stale peer recovery.
  - Prolonged partition: sync daemon outbound buffer must shed to durable local storage.
    CRDT store serves this role — but the paper must make this explicit.
  - Byzantine failure: buggy CRDT operation (valid structure, corrupt semantics) propagates
    faithfully to all peers. Need operation validation and corrupt-sequence recovery.

  PROCEED WITH CONDITIONS verdict. Conditions: stale peer recovery (high priority),
  linearizable operation enumeration guidance, CRDT store as partition buffer.

  **Takeaway principle:** Convergence at the data-structure level is not the same as
  correctness at the domain level. The CRDT handles structural merge; the application
  must separately validate domain invariants. The Flease lease governs coordination, not
  merge semantics.

- [ ] **Step 4: Quality check (QC-1 through QC-10, note QC-9)**

- [ ] **Step 5: Save**

---

### Task 9: Chapter 7 — The Security Lens

**File:** `part-2-council-reads-the-paper/ch07-security-lens.md`
**Target:** 3,000–4,000 words
**Sources:** R1 Nia Okonkwo section, R2 Member 3 Okonkwo section,
v13.md §11 (Security Architecture), v5.md §4 (Security and Identity)

- [ ] **Step 1: Write Act 1 (~1,200 words)**

  Okonkwo's persona: principal security engineer, former red team, OSCP + CISSP, has
  exploited three "local-first" demos in under 20 minutes by attacking the sync layer.
  Core conviction: distributed security architectures fail not in the cryptography but
  in key management, trust establishment, and revocation pathways.

  Round 1 scores: data minimization at protocol layer earns 9/10 (the highest single score
  in the round) — subscription filtering at send tier is the correct control placement.
  Key hierarchy described but not diagrammed.

  The BLOCK: key compromise incident response absent. A node key compromise potentially
  exposes all data the node has ever been authorized to read. Must specify: detection
  mechanism, re-keying procedure, data-at-risk scope, user-visible notification.

- [ ] **Step 2: Write interlude — what changed (~500 words)**

  Resolutions:
  - Key hierarchy diagram added: root org key → role KEKs → per-node wrapped keys →
    per-record DEK → ciphertext
  - Key compromise procedure: detection (anomalous access patterns, physical loss
    report), re-keying (new role KEK generated, all DEKs re-wrapped, old KEK discarded),
    data-at-risk scope (records readable by compromised node since last rotation),
    user notification
  - Offline node revocation reconnection: exact steps — node presents attestation,
    daemon checks revocation log, if revoked: new key bundle required before sync resumes
  - In-memory key material: locked memory pages, key zeroing on process exit

- [ ] **Step 3: Write Act 2 (~1,000 words)**

  Round 2 prompts (from R2 Okonkwo section):
  - Attack tree: supply chain gap — who signs the release CID? Need release signing key
    custody, reproducible build requirement, Sigstore supply-chain transparency.
  - Compromised relay: relay sees metadata not payload (correct) — but traffic analysis
    is still sensitive for high-security deployments. Self-hosted relay is the mitigation.
  - Physical access: cold boot / memory scraping window when app is running. Re-auth
    interval recommendation (every 4 hours) is a hardening note, not a flaw.
  - Compliance: GDPR Article 17 Right to Erasure in a no-GC CRDT system. Crypto-shredding
    pattern: destroying the DEK renders the ciphertext permanently unreadable without
    breaking the operation DAG. Document the pattern; disclose the limitation.

  PROCEED WITH CONDITIONS. Conditions: Sigstore supply chain (high), GDPR Article 17
  crypto-shredding (high), relay traffic analysis acknowledgment, re-attestation
  default interval.

  **Takeaway principle:** Distributing data to endpoints solves the central honeypot problem
  and creates a distributed one. Defense-in-depth — four layers from encryption at rest
  through stream-level filtering — is not optional. The data minimization invariant
  (subscription filtering at send, not receive) is the architectural achievement that
  makes the security story credible.

- [ ] **Step 4: Quality check (QC-1 through QC-10, note QC-9)**

- [ ] **Step 5: Save**

---

### Task 10: Chapter 8 — The Product & Economic Lens

**File:** `part-2-council-reads-the-paper/ch08-product-economic-lens.md`
**Target:** 3,000–4,000 words
**Sources:** R1 Jordan Kelsey section, R2 Member 4 Kelsey section,
v13.md §17 (OSS Strategy and Sustainability), v5.md §7 (Economic Model)

- [ ] **Step 1: Write Act 1 (~1,200 words)**

  Kelsey's persona: two-time founder, first company failed (B2C SaaS, runway), second
  acquired ($22M developer tooling). Has personally tried to sell "privacy-first" and
  "open-source" software to enterprise buyers. Knows exactly why those pitches fail.

  Round 1 scores: unit economics 7/10 ("$2 infrastructure cost" is more specific than
  most but needs a worked model). Go-to-market 5/10. First customer archetype 4/10 —
  completely absent.

  Two BLOCKs:
  1. No first customer archetype. "Developer communities who value data sovereignty"
     is a demographic, not a customer. Who pays first, why, and how are they found?
  2. No OSS-to-paid conversion mechanism. The specific moment that causes a team to
     pay for the relay must be specified.

- [ ] **Step 2: Write interlude — what changed (~500 words)**

  Resolutions:
  - Construction vertical selected: job-site connectivity failures, data ownership anxiety,
    software downtime cost measured in bid outcomes. RFI tracking and punch lists as
    candidate workflows.
  - Five-step customer development path: identify 10 construction PMs via AGC/ABC
    associations or ENR/Constructor publications, conduct discovery interviews, identify
    the moment software failure costs money, build to that scenario, get one team live.
  - Relay economics model: infrastructure cost <$2/team/month, pricing target $15–25/team/month,
    ~90% gross margin at scale.
  - OSS-to-paid conversion mechanism: the relay becomes load-bearing the moment a second
    device or second team member needs to sync. That is the conversion trigger.

- [ ] **Step 3: Write Act 2 (~1,000 words)**

  Round 2 prompts (from R2 Kelsey section):
  - First customer path: construction PMs identified but no acquisition channel.
    AGC/ABC, ENR/Constructor, or construction tech consulting warm intro are the paths.
  - Unit economics at 1,000 teams: $20K/month revenue, $2K infrastructure, 90% gross
    margin — supports 2–3 FTE at Bay Area salaries. Headcount model needed.
  - AGPLv3 exit strategy: dual-license structure must be specified before the repo opens.
    CLA from all contributors. AGPL for open-source users, commercial license for
    organizations that can't accept AGPL.
  - Year-2 failure modes: relay commoditization (AWS offers a managed relay at infra cost),
    enterprise direct sales cost vs. $15–25 price point, contributor governance vacuum.

  PROCEED WITH CONDITIONS. Conditions: customer acquisition channel (high), dual-license
  CLA (high), governance model, relay commoditization moat articulation.

  **Takeaway principle:** The managed relay is the right unit of competitive analysis, but
  its defensibility rests on support quality and product-integrated onboarding — not the
  protocol itself, which is open. Get the dual-license structure and CLA in place before
  the first external contributor opens a PR.

- [ ] **Step 4: Quality check (QC-1 through QC-10, note QC-9)**

- [ ] **Step 5: Save**

---

### Task 11: Chapter 9 — The Local-First Practitioner Lens

**File:** `part-2-council-reads-the-paper/ch09-local-first-practitioner-lens.md`
**Target:** 3,000–4,000 words
**Sources:** R1 Tomás Ferreira section, R2 Member 5 Ferreira section,
v13.md §13 (UX Design Philosophy), v13.md §14 (Non-Technical Trust Gap),
v5.md §6 (UX and Conflict Handling)

- [ ] **Step 1: Write Act 1 (~1,200 words)**

  Ferreira's persona: core contributor to Automerge, built three local-first production
  apps. Has watched promising local-first projects fail at the "last device" backup problem,
  the NAT traversal problem, and the "the user deleted the container" problem.

  Round 1 scores: CRDT library selection 9/10 (Yjs and Loro appropriate, but Automerge
  omission unexplained). Alignment with local-first literature 8/10. Community governance 5/10.

  The BLOCK: no data portability path. A paper arguing for data ownership that does not
  specify how a user exports their data in a durable, application-independent format
  contradicts its own thesis. "Export to plain files" is not mentioned anywhere.

- [ ] **Step 2: Write interlude — what changed (~500 words)**

  Resolutions:
  - Plain-file export path added: JSON export of all user records, CSV export for tabular
    data, markdown export for documents. One command, no vendor cooperation required.
  - Non-technical disaster recovery walkthrough: laptop dies → buy new laptop → install
    app → authenticate with recovery code or team-member QR scan → point at BYOC backup
    target → full restore in background. Step-by-step, no technical knowledge required.
  - Symmetric NAT failure mode: when both peers are behind carrier-grade NAT and relay
    is down, direct communication is impossible. Documented honestly. Relay is the
    resolution; self-hosted relay on a cloud VM with public IP is the fallback.
  - Community governance model added: BDFL for v1, contributor council for v2, foundation
    for v3; roadmap decisions require documented consensus.

- [ ] **Step 3: Write Act 2 (~1,000 words)**

  Round 2 prompts (from R2 Ferreira section):
  - Seven ideals compliance: R2 is the first version to satisfy all seven without
    reservation. The checklist from R2, verbatim.
  - 30-day abandonment risk: zero-state first-run experience not described. What does a
    brand-new user see after installation? This is where most users abandon the product.
  - Backup/recovery UX: three-state model (Protected/Attention/At Risk) is correct;
    the restore experience needs the same UX care as the backup configuration flow.
  - Production analogues: Actual Budget as the closest commercial analogue — validates
    both the local-first model and a non-subscription revenue path.
  - Implementation drift risk: local-first architectures re-centralize under pressure via
    server-side analytics, A/B testing, feature gates. Specify the telemetry model now
    (opt-in, aggregate-only via relay, or none) before the first product analytics request.

  PROCEED — no blocking conditions. The first council member to issue an unconditional
  PROCEED in Round 2.

  **Takeaway principle:** The architecture earns the right to claim data ownership only
  when it ships the export button, documents the disaster recovery path, and honestly
  names the connectivity scenarios where it cannot help. Local-first is not a feature flag
  on top of a centralized system — it requires that every failure mode is visible and
  survivable by a non-technical user.

- [ ] **Step 4: Quality check (QC-1 through QC-10, note QC-9)**

- [ ] **Step 5: Save**

---

### Task 12: Chapter 10 — Synthesis: What the Council Finally Agreed On

**File:** `part-2-council-reads-the-paper/ch10-synthesis.md`
**Target:** 2,000–3,000 words
**Sources:** R1 Council Tally, R2 Aggregate Scorecard, R2 Council Consensus Statement,
both reviews' Commendations sections
**Dependency:** Ch 5–9 must be complete before writing this chapter

- [ ] **Step 1: Write chapter outline**

  ```
  ## Round 1: The Architecture Fails
  ## Round 2: The Architecture Survives (with Conditions)
  ## The Non-Negotiables: Seven Properties No Implementation Can Skip
  ## The Open Questions: What the Council Did Not Resolve
  ## How the Agreed Properties Shape Part III
  ```

- [ ] **Step 2: Write "Round 1 fails / Round 2 survives" (~500 words)**

  The scorecard tables from R1 and R2. What changed between rounds. The overall trajectory:
  from 6.8 average with 2 BLOCKs to 7.1 average with 0 BLOCKs. This is not a comfortable
  pass — it is a conditional one. Fifteen conditions remain.

- [ ] **Step 3: Write "The Non-Negotiables" (~800 words)**

  Seven properties that all five council members, across both rounds, treated as
  mandatory — the commendations that survived both reviews:
  1. Data minimization at the protocol layer (subscription filtering at send, not receive)
  2. MDM compliance check at capability negotiation phase
  3. Three-tier CRDT resolution model (AP for documents, CP for transactions, no CRDT
     for financial ledger)
  4. DEK/KEK envelope encryption with rotation work proportional to document count
  5. Dual-license structure (AGPL + commercial) with CLA before repo opens
  6. Non-technical disaster recovery path (step-by-step, no technical knowledge required)
  7. Plain-file export with no vendor cooperation required

- [ ] **Step 4: Write "The Open Questions" + bridge to Part III (~700 words)**

  The questions the council raised that the architecture acknowledges but does not
  fully resolve (from R2 conditions and v5.md §9 Open Questions):
  - GDPR Article 17 Right to Erasure in a CRDT system
  - Relay commoditization moat — what makes the managed relay defensible at scale
  - Formal verification of domain-level merge invariants
  - KEK compromise incident response under realistic enterprise conditions
  - Analytics and telemetry model without re-centralizing

  Bridge to Part III: these are the constraints the reference architecture must satisfy.
  Part III specifies how.

- [ ] **Step 5: Quality check (QC-1 through QC-10)**

- [ ] **Step 6: Save**

---

## Phase 4 — Part III: The Reference Architecture

*Dependencies: Ch 10 complete. Ch 11 must precede Ch 12 (data layer builds on node arch).
Ch 13 (schema migration) should follow Ch 12. Ch 12, 14, 15, 16 can largely be written
in parallel after Ch 11.*

---

### Task 13: Chapter 11 — Node Architecture

**File:** `part-3-reference-architecture/ch11-node-architecture.md`
**Target:** 3,500–4,500 words
**Sources:** v13.md §5 (full section), v5.md §2.2 (Layered Model), v5.md §3.4 (Sync Daemon IPC),
Sunfish `CLAUDE.md` (package architecture section)

- [ ] **Step 1: Write chapter outline**

  ```
  ## The Microkernel Monolith
  ## Kernel Responsibilities
  ## Plugin Contracts
  ## The UI Kernel: Four-Tier Layering
  ## Process Boundaries and IPC
  ## Sunfish Package Map
  ```

- [ ] **Step 2: Write "The Microkernel Monolith" + Kernel Responsibilities (~1,200 words)**

  The Linux modular kernel applied to application software: stable core with well-defined
  extension points, all running in-process to avoid IPC overhead. From v13.md §5.1.

  Kernel responsibilities (stable, versioned slowly): node lifecycle, sync daemon protocol,
  CRDT engine abstraction, schema migration infrastructure, security primitives, partial
  sync engine, plugin registry.

  The three practical benefits of the kernel/plugin split: independent evolution of domain
  plugins, tenant-specific bundles, safe third-party extensibility against a stable contract.

- [ ] **Step 3: Write "Plugin Contracts" (~600 words)**

  Five extension point interfaces from v13.md §5.3:
  - `ILocalNodePlugin` — registration, lifecycle, dependency declaration
  - `IStreamDefinition` — CRDT streams, event types, sync bucket contributions
  - `IProjectionBuilder` — read-model projections rebuilt from event log
  - `ISchemaVersion` — supported schema versions and upcasters
  - `IUiBlockManifest` — block and module registration with UI kernel

  How compatibility adapters work: they implement the same interfaces as their target and
  route through an alternative provider. The kernel cannot distinguish a first-party plugin
  from a compat adapter.

- [ ] **Step 4: Write "The UI Kernel" (~800 words)**

  Four-tier layering from v13.md §5.2:
  1. Foundation — design tokens (sync-healthy, stale, offline, conflict-pending, quarantine),
     typography, spacing, icons
  2. Framework-Agnostic Component Layer — status indicators, optimistic-write buttons,
     conflict list component, freshness badge
  3. Blocks and Modules — domain plugin UI; each block exposes its data contract and
     handles offline/stale/conflict states
  4. Compat/Adapter Layer — alternative rendering engines or external auth providers

  The alignment invariant: every kernel state visible to the data layer has a corresponding
  token and component in the UI layer. In Sunfish terms: `SunfishNodeHealthBar` is the
  live implementation of this principle.

- [ ] **Step 5: Write "Process Boundaries and IPC" + "Sunfish Package Map" (~900 words)**

  IPC: Unix domain socket between the application shell and the sync daemon. From v5.md §3.4.
  Why a separate process: the daemon survives application restarts and updates; peer sessions
  remain established while the application layer churns. `System.Net.Sockets.UnixDomainSocketEndPoint`
  in .NET 5+ — cross-platform on Windows 10/Server 2019+, Linux, macOS.

  Sunfish package map (from Sunfish `CLAUDE.md` package architecture):
  ```
  Sunfish.Foundation              → design tokens, utilities, core contracts
  Sunfish.UI.Core                 → framework-agnostic component contracts
  Sunfish.UI.Adapters.Blazor      → Blazor implementation
  Sunfish.Kernel.Crdt             → CRDT engine abstraction (ICrdtEngine, ICrdtDocument)
  Sunfish.Kernel.Sync             → gossip daemon, peer discovery, delta streaming
  Sunfish.Kernel.Security         → DEK/KEK, attestation, key lifecycle
  Sunfish.Kernel.Ledger           → double-entry posting engine, CQRS projections
  Sunfish.Kernel.Runtime          → node lifecycle, plugin registry, service composition
  Sunfish.Foundation.LocalFirst   → local store, backup adapter, circuit breaker
  Sunfish.Blocks.*                → domain plugin building blocks
  ```

- [ ] **Step 6: Quality check (QC-1 through QC-10, QC-7 applies)**

- [ ] **Step 7: Save**

---

### Task 14: Chapter 12 — CRDT Engine and Data Layer

**File:** `part-3-reference-architecture/ch12-crdt-engine-data-layer.md`
**Target:** 3,500–4,500 words
**Sources:** v13.md §2.2–2.5, v13.md §9, v13.md §12, v5.md §3.1–3.3,
Sunfish `docs/adrs/0028-crdt-engine-selection.md`

- [ ] **Step 1: Write chapter outline**

  ```
  ## The Three-Layer CRDT Architecture
  ## Per-Record CAP Positioning
  ## CRDT Engine Selection: YDotNet, Loro, and the ICrdtEngine Abstraction
  ## CRDT Growth and Garbage Collection
  ## The Double-Entry Ledger as the Canonical CP Subsystem
  ## The Five-Layer Storage Architecture
  ```

- [ ] **Step 2: Write "Three-Layer Architecture" + "Per-Record CAP" (~900 words)**

  Three layers from v5.md §3.1: data layer (maps, lists, text, counters), semantic layer
  (domain rules interpreting CRDT changes), view layer (projections and indexes). The
  separation keeps merge logic data-structure-centric while allowing application-level
  constraint enforcement.

  Per-record CAP positioning table from v13.md §2.2: documents/notes/tasks → AP (CRDT);
  team membership/permissions → AP with deferred merge; resource reservations/scheduled slots
  → CP (distributed lease); financial transactions → CP + ledger; audit records → CP + append-only.

- [ ] **Step 3: Write "CRDT Engine Selection" (~900 words)**

  The evaluation from Sunfish ADR 0028:
  - Yjs/YDotNet: most mature, widely deployed, excellent documentation, good .NET support.
    Con: emergent GC approach (not compaction-first).
  - Loro: designed with compaction as a primary concern, shallow snapshots, compact encoding.
    Con: newer, less battle-tested, .NET bindings (loro-cs) are active but bare-bones.
  - Automerge: excellent design reference, no first-class .NET binding.
  - Native .NET: full control, enormous correctness maintenance burden.

  ADR 0028 decision: Loro as the aspirational primary (compaction story, compact encoding,
  shallow snapshots match paper §9 mitigations exactly). YDotNet as the fallback while
  loro-cs matures. The `ICrdtEngine` abstraction keeps the choice reversible — an engine
  swap does not ripple through application code and does not require a schema epoch bump.

  loro-cs status: `github.com/sensslen/loro-cs` — actively maintained, cross-platform
  NuGet, v1.10.3 released December 2025, ~4 months behind loro-core v1.11.x, "bare bones"
  API coverage by maintainer's own assessment. Evaluate against your required API surface
  before committing; contribute missing bindings if the gap is small.

- [ ] **Step 4: Write "CRDT Growth and GC" (~700 words)**

  The growth problem from v13.md §9: tombstones and historical operations accumulate.
  Long-lived, high-churn documents grow large even when visible content is modest.

  Three-tier GC policy from R2 Shevchenko (the resolution that cleared the BLOCK):
  - Yjs with aggressive GC: safe for ephemeral data (cursors, presence) where durability
    is not required
  - Loro 90-day retention: safe if and only if every peer has acknowledged all operations
    older than 90 days before compaction — stale peer recovery protocol activates if not
  - No-GC compliance tier: safe by construction; document growth bounded by business volume

  Application-level sharding: large logical documents split into sub-documents under map
  keys. Archiving a section = key deletion; CRDT engine GCs that section independently.

- [ ] **Step 5: Write "The Ledger" + "Five-Layer Storage" (~900 words)**

  Ledger from v13.md §12: double-entry as a first-class CP subsystem. Every financial
  change is an immutable posting event. Sum of all postings per transaction = zero.
  Posting engine converts domain events under distributed lease; idempotency keys prevent
  duplicate postings. CQRS split: immutable posting stream (write side) vs. materialized
  projections for balance queries (read side). Period closing as ledger-specific snapshots.

  Five-layer storage architecture from v13.md §2.4: local encrypted database → CRDT +
  event log → BYOC backup → content-addressed distribution (optional) → decentralized
  archival (optional, enterprise). Tiers 4–5 are opt-in; core system runs on 1–3.

- [ ] **Step 6: Quality check (QC-1 through QC-10, QC-7 applies)**

- [ ] **Step 7: Save**

---

### Task 15: Chapter 13 — Schema Migration and Evolution

**File:** `part-3-reference-architecture/ch13-schema-migration-evolution.md`
**Target:** 3,000–4,000 words
**Sources:** v13.md §7 (full section), v13.md §8 (Snapshots and Rehydration)

- [ ] **Step 1: Write chapter outline**

  ```
  ## Why Schema Migration Is the Hardest Problem
  ## The Expand-Contract Pattern
  ## Event Versioning and Upcasters
  ## Bidirectional Schema Lenses
  ## Epoch Coordination and Copy-Transform Migration
  ## Stale Peer Recovery
  ## Snapshots: Performance Optimization, Not Source of Truth
  ```

- [ ] **Step 2: Write all sections (~3,200 words)**

  Draw entirely from v13.md §7 and §8. Translate specification language to practitioner
  prose with concrete examples for each pattern.

  - **Why it's hardest:** Nodes update independently. Teams run mixed versions simultaneously.
    A team of five may run versions spread across three releases. The schema must work for
    all of them — simultaneously, with no coordinator.

  - **Expand-contract:** New fields additive and optional in expand phase; dual-write to
    old and new fields; older nodes ignore unknown fields; newer nodes prefer new fields.
    Contract phase only after all active peers pass the compatibility window. Schema epoch
    bump gates sync connections from nodes below minimum epoch.

  - **Upcasters:** Immutable events; additive changes in-place; non-additive changes
    introduce new event types (`RecordUpdatedV2`) leaving old types intact. Upcaster chains
    accumulate and become brittle — mandatory stream compaction retires them.

  - **Bidirectional lenses:** Declarative transformation functions between schema versions.
    Version graph; migrations traverse shortest path. Handles field renames, type changes,
    structural reorganizations. From v13.md §7.3 (cites Ink & Switch Cambria).

  - **Epoch coordination:** Quorum-agreed announcement, copy-transform background job,
    cutover, old epoch marked read-only. The "couch device" returning after three major
    versions: capability negotiation rejects with clear error, user directed to update.

  - **Stale peer recovery (from R2 Shevchenko):** When reconnecting peer's vector clock
    predates the GC horizon, incremental sync is impossible. Trigger full-state snapshot
    transfer. The reconnecting node downloads the current epoch snapshot and resumes.

  - **Snapshots:** Format (aggregate_id, epoch_id, schema_version, last_event_seq, payload).
    Rehydration sequence: load snapshot → verify epoch + schema → replay events after
    last_event_seq → apply upcasters. Snapshots are performance optimization only; delete
    and regenerate without correctness impact.

- [ ] **Step 3: Quality check (QC-1 through QC-10, QC-7 applies)**

- [ ] **Step 4: Save**

---

### Task 16: Chapter 14 — Sync Daemon Protocol

**File:** `part-3-reference-architecture/ch14-sync-daemon-protocol.md`
**Target:** 3,000–4,000 words
**Sources:** v13.md §6 (full section), v5.md §3.4 (Sync Daemon IPC),
Sunfish `docs/specifications/sync-daemon-protocol.md`,
Sunfish `accelerators/bridge/README.md` (relay configuration reference)

- [ ] **Step 1: Write chapter outline**

  ```
  ## The Daemon as a Separate Process
  ## Gossip Anti-Entropy
  ## The Five-Phase Handshake
  ## Data Minimization Invariant
  ## Distributed Lease Coordination (CP Mode)
  ## Wire Format and Protocol Versioning
  ## Reconnection Storm and Partition Behavior
  ## Relay Configuration
  ```

- [ ] **Step 2: Write all sections (~3,200 words)**

  Draw from v13.md §6 for architecture and from Sunfish sync-daemon-protocol.md for
  wire-level specifics.

  - **Daemon as separate process:** Survives app restarts, updates, crashes. Unix domain
    socket IPC. From v5.md §3.4. All IPC messages authenticated using device keys.

  - **Gossip anti-entropy:** Membership list + vector clocks. Periodic delta exchange
    (default 30s, two random peers). Three-tier peer discovery: mDNS (LAN, zero-config)
    → WireGuard mesh VPN (cross-network, automatic NAT traversal) → managed relay (fallback).

  - **Five-phase handshake from v13.md §6.2:**
    ```
    1. HELLO           {node_id, schema_version, supported_versions[]}
    2. CAPABILITY_NEG  {crdt_streams[], cp_leases[], bucket_subscriptions[]}
    3. ACK             {granted_subscriptions[]}
    4. DELTA_STREAM    (continuous)
    5. GOSSIP_PING     (every 30s)
    ```
    MDM compliance check occurs during CAPABILITY_NEG — non-compliant nodes rejected
    before they touch data (Voss commendation from R1/R2).

  - **Data minimization invariant:** Subscription filtering at send tier. Non-subscribed
    nodes never receive events. Eligibility determined by role attestation during
    capability negotiation. Receiving data and hiding it in the UI is not a security control.

  - **Distributed lease coordination:** Lease required before CP-class write. Granted when
    quorum of peers acknowledge. Default: 30s duration, ceil(N/2)+1 quorum. Lease holder
    offline → lease expires → new election. Split-write safety: CRDT merge handles the
    write window for CP-class records that overlap with the lease transfer.

  - **Wire format:** CBOR encoding. Message types, versioning scheme, backward-compatibility
    policy. Reference Sunfish sync-daemon-protocol.md for field-level specification.

  - **Reconnection storm:** 50+ nodes reconnecting simultaneously after relay outage.
    Resource governor caps concurrent gossip rounds per tick. Anti-entropy throttled to
    keep small laptops within memory bounds.

  - **Relay configuration (from Bridge README):** `MaxConnectedNodes` (default 500),
    `AllowedTeamIds`, `ListenEndpoint`. Three trust levels: relay-only (ciphertext only,
    maximum privacy), attested hosted peer (operator has team attestation), no hosted peer
    (self-hosted only).

- [ ] **Step 3: Quality check (QC-1 through QC-10, QC-7 applies)**

- [ ] **Step 4: Save**

---

### Task 17: Chapter 15 — Security Architecture

**File:** `part-3-reference-architecture/ch15-security-architecture.md`
**Target:** 3,500–4,500 words
**Sources:** v13.md §11 (full section), v5.md §4 (full section),
Sunfish `accelerators/anchor/README.md` (authentication model section)

- [ ] **Step 1: Write chapter outline**

  ```
  ## Threat Model
  ## Device and User Identity
  ## DEK/KEK Envelope Encryption
  ## Key Rotation and Revocation
  ## The Four Defensive Layers
  ## Key Compromise Incident Response
  ## Compliance Framework Mapping
  ## In-Memory Key Material Hardening
  ```

- [ ] **Step 2: Write all sections (~3,800 words)**

  - **Threat model from v13.md §11.1:** Distributing data to endpoints does not eliminate
    the honeypot — it distributes it. A cloud database is a single high-value target.
    A fleet of workstations is a larger attack surface with heterogeneous posture.
    Defense-in-depth required. Insider threat acknowledged. Physical access threat named.

  - **Identity from v5.md §4.1:** Device identity = long-lived Ed25519 keypair, OS-native
    keystore. User identity = OIDC/SAML IdP or local auth. Peers authenticate using device
    keys. Users authorized via role assignments in CRDT state. Anchor's Ed25519 keypair
    issued at onboarding (from Anchor README authentication section); HKDF subkeys per-team
    defeat cross-team operator correlation.

  - **DEK/KEK from v5.md §4.2:** Per-document DEK (random, AES-GCM). Per-role KEK.
    DEK wrapped with current KEK, stored alongside ciphertext. Standard KMS-backed pattern.
    Key hierarchy diagram: root org key → role KEKs → per-node wrapped keys → per-record DEK → ciphertext.

  - **Key rotation from v5.md §4.3:** New KEK generated; all DEKs re-wrapped with new KEK;
    old KEK discarded. Rotation work proportional to document count, not size. Background
    job operates on metadata and small DEK blobs; document bodies untouched.

  - **Four defensive layers from v13.md §11.2:** At-rest encryption (SQLCipher, Argon2id
    key derivation); field-level encryption (per-role symmetric keys, wrapped with member
    public keys, distributed as administrative events); stream-level data minimization
    (daemon enforces subscription filtering before data leaves node); circuit breaker +
    quarantine (offline writes held pending validation on reconnect).

  - **Key compromise IR (R1 Okonkwo's BLOCK, now resolved):** Detection (anomalous access
    patterns in audit log, physical loss report by user); re-keying procedure (new role KEK,
    all DEKs re-wrapped, old KEK securely deleted); data-at-risk scope (all records readable
    by compromised node since last rotation); user notification (in-app alert + email if
    configured); forward secrecy window (records created before compromise are protected
    by prior DEKs if old KEK was already rotated).

  - **Compliance mapping (from R2 Okonkwo):** SOC 2 Type II (encryption at rest + in transit,
    audit log, access control — achievable; gap: anomalous access pattern monitoring).
    HIPAA (application-layer achievable; relay metadata = BAA consideration; self-hosted
    relay for maximum privacy). GDPR Article 17 (crypto-shredding: destroying the DEK renders
    ciphertext permanently unreadable; document this explicitly; acknowledge that truly
    immutable compliance records conflict with Art. 17 by design).

  - **In-memory hardening (from R2 Okonkwo):** Locked memory pages for key material.
    Key zeroing on process exit. Re-authentication interval (24-hour recommended default)
    limits cold boot attack window.

- [ ] **Step 3: Quality check (QC-1 through QC-10, QC-7 applies)**

- [ ] **Step 4: Save**

---

### Task 18: Chapter 16 — Persistence Beyond the Node

**File:** `part-3-reference-architecture/ch16-persistence-beyond-the-node.md`
**Target:** 2,500–3,500 words
**Sources:** v13.md §2.4 (Five-Layer Storage), v13.md §10 (Partial and Selective Sync),
Sunfish `docs/federation/operator-guide.md`,
Sunfish `docs/specifications/air-gap-deployment.md`,
Sunfish `docs/zone-b-migration-path.md` §4 (Phase 3 relay wiring)

- [ ] **Step 1: Write chapter outline**

  ```
  ## Local Persistence: What the Node Owns
  ## BYOC Backup: The "Last Device Destroyed" Recovery Path
  ## Backup Status UX
  ## Declarative Sync Buckets
  ## Relay Architecture
  ## Privacy Posture and Traffic Analysis
  ## Federation and Long-Term Archival
  ```

- [ ] **Step 2: Write all sections (~2,800 words)**

  - **Local persistence:** SQLCipher encrypted database. Durability guarantees (writes
    fsync'd before acknowledgment for CP records; AP records acknowledged optimistically,
    persisted asynchronously). Storage budget enforcement (default 10GB; lazy-bucket LRU
    eviction; stubs retained after eviction).

  - **BYOC backup:** Object storage adapter (rclone-compatible). User-controlled disaster
    recovery. The "last device destroyed" walkthrough: install app on new device →
    authenticate (recovery code or team-member QR scan) → point at BYOC backup target →
    full CRDT state restores automatically in background. No vendor cooperation required.

  - **Backup status UX:** Three-state model: Protected (recent backup confirmed),
    Attention (backup overdue, warn), At Risk (no backup configured or backup failed,
    persistent non-blocking banner). "I understand the risk" dismissal. Source: R2 Ferreira.

  - **Declarative sync buckets from v13.md §10.2:** Named, YAML-specified subsets of
    team dataset. Bucket eligibility by role attestation. `replication: eager` vs. `lazy`.
    `max_local_age_days` for archival buckets. Lazy stubs: fetch on access, content hash
    verification. Reference the YAML example from v13.md §10.2 verbatim.

  - **Relay architecture from Bridge README:** What the relay owns (DELTA_STREAM fan-out,
    GOSSIP_PING routing, team-id-scoped multiplexing). What it does not own (persistence,
    application state, decryption capability). Stateless — catch-up traffic persisted by
    hosted-node peer, not relay. Three tenant trust levels.

  - **Privacy posture:** Relay sees metadata (which nodes communicate, when, at what volume)
    not payload. For legal, healthcare, defense: metadata is sensitive. Self-hosted relay
    on operator-controlled infrastructure is the mitigation. Acknowledge limitation honestly.
    Source: R2 Okonkwo prompt 2.

  - **Federation and archival:** Phase D federation patterns from Sunfish operator guide
    (briefly — one paragraph each): multi-jurisdiction entity sync, air-gapped sneakernet
    replication. Long-term archival formats (signed append-only logs, snapshot formats).
    Decentralized archival tier for regulated industries (optional, enterprise).

- [ ] **Step 3: Quality check (QC-1 through QC-10, QC-7 applies)**

- [ ] **Step 4: Save**

---

## Phase 5 — Part IV: Implementation Playbooks

*Dependencies: Part III substantially complete (Ch 11–16). Chapters in Part IV reference
Part III for specification — they do not rewrite it. QC-7 applies: tutorial voice, not
specification voice. Ch 17 should precede Ch 18; Ch 19 and Ch 20 can be written in parallel.*

---

### Task 19: Chapter 17 — Building Your First Node

**File:** `part-4-implementation-playbooks/ch17-building-first-node.md`
**Target:** 3,500–4,500 words
**Sources:** v13.md §18 Phase 1–2 (Implementation Roadmap),
Sunfish `accelerators/anchor/README.md` (full)

- [ ] **Step 1: Write chapter outline**

  ```
  ## Start with Sunfish Anchor
  ## What Anchor Gives You Today
  ## Wiring the Kernel Stack
  ## Your First CRDT Document and Two-Device Sync
  ## The QR-Code Onboarding Flow
  ## Local-First UX Basics
  ## What to Build Next
  ```

- [ ] **Step 2: Write all sections (~3,800 words)**

  - **Start with Anchor:** Clone `accelerators/anchor/`. It builds and launches.
    The shell is a placeholder — that's intentional. It gives you the wiring without
    the domain-specific cruft. `dotnet build Sunfish.Anchor.csproj -f net10.0-windows10.0.19041.0`.

  - **What Anchor gives you today (from Anchor README deliverable checklist):**
    LocalFirst store wiring (Wave 3.3 landed), kernel security + runtime wired in
    `MauiProgram.cs`, device-bound Ed25519 keypair at onboarding, founder/joiner
    attestation flow, three-step onboarding surface in `Components/Pages/Onboarding.razor`.
    What's still placeholder: bundle selection UI, report catalog, sync toggle, platform
    packaging, auto-update.

  - **Wiring the kernel stack:** The three `MauiProgram.cs` calls that wire the local-first
    kernel: `AddSunfishEncryptedStore()`, `AddSunfishKernelRuntime()`,
    `AddSunfishKernelSecurity()`. What each registers. The startup sequence:
    kernel runtime initializes → local SQLCipher DB opens → device keypair loaded from
    OS keystore → onboarding state checked → UI shell renders.

  - **First CRDT document:** Create a `LoroDoc` (or `YDotNet.YDoc` depending on engine),
    register it with `ICrdtEngine`, subscribe to updates via `IStreamDefinition`.
    Two-device sync: run two Anchor instances on the same LAN — mDNS discovers the peer,
    gossip daemon establishes session, CRDT delta streams flow automatically.

  - **QR-code onboarding flow (from Anchor README §Onboarding flow):**
    Three steps: install → authenticate (paste base64 bundle or QR decode) → sync.
    CBOR wire format (4-byte length prefix + AttestationBundle + snapshot bytes).
    Founder bundle: self-signed Ed25519. Joiner bundle: signed by founder's key.
    `QrOnboardingService.GenerateFounderBundleAsync` and `DecodePayloadAsync`.

  - **Local-first UX basics:** Wire `SunfishNodeHealthBar` to the kernel's sync state.
    Three indicators: node health, link status, data freshness. These are live in Anchor
    via the three-indicator status bar from paper §13.2. Add an optimistic-write button
    that reflects pending/confirmed/failed states using the `ICrdtEngine` write result.

  - **What to build next:** Register your first domain plugin (implement `ILocalNodePlugin`,
    `IStreamDefinition`, `IProjectionBuilder`). Reference Ch 11 for the full plugin contract.
    Add your first domain-specific block (implement `IUiBlockManifest`). Reference Ch 12
    for CRDT document modeling decisions.

- [ ] **Step 3: Quality check (QC-1 through QC-10, QC-7 applies)**

- [ ] **Step 4: Save**

---

### Task 20: Chapter 18 — Migrating an Existing SaaS

**File:** `part-4-implementation-playbooks/ch18-migrating-existing-saas.md`
**Target:** 3,000–4,000 words
**Sources:** v5.md §8 (Migration from Hosted SaaS),
Sunfish `docs/zone-b-migration-path.md` (full),
Sunfish `accelerators/bridge/README.md`

- [ ] **Step 1: Write chapter outline**

  ```
  ## Is Your Product Zone B, Zone C, or Somewhere Between?
  ## The Bridge Accelerator as Your Zone C Reference
  ## The Four Migration Phases
  ## Phase Transition Success Criteria
  ## Architectural Decisions That Determine Migration Cost
  ## Common Failure Modes
  ```

- [ ] **Step 2: Write all sections (~3,200 words)**

  Draw from `docs/zone-b-migration-path.md` (written specifically for this book). This
  chapter is the prose adaptation of that technical guide for a practitioner audience.

  - **Zone determination:** Run the four-filter framework from Ch 4. If all user-owned data
    passes filters but some coordination features don't, you are in Zone C. If everything
    fails Filter 1, you are in Zone B — use Sunfish's component surface but don't add
    the local-node kernel (see migration guide).

  - **Bridge as Zone C reference:** `accelerators/bridge/` demonstrates Zone C at a working
    level. Per-tenant data-plane isolation, hosted-node-as-SaaS, ciphertext-only relay.
    The control plane (signup, billing, tenant registry) stays in Postgres. The data plane
    (CRDT documents, event log, sync) moves to per-tenant local-node-host processes.

  - **Four migration phases** (from zone-b-migration-path.md §4 and v5.md §8):
    1. Shadow mode — local node mirrors data read-only; writes still flow through server
    2. Local writes for non-conflicting domains — AP-class data routes through CRDT engine
    3. Full local authority for new projects — server becomes a relay peer
    4. Gradual backfill of legacy records — copy-transform Postgres events to CRDT log

    For each phase: what it involves, success criteria, reversibility.

  - **Phase transition criteria (from R2 Voss commendation):** Present the framing that
    earned praise in Round 2 — "We can pause at Phase 2 indefinitely" is the framing for
    a change advisory board. Each phase is independently reversible.

  - **Architectural decisions that determine migration cost** (from zone-b-migration-path.md §3):
    Per-tenant storage isolation from day one; event-sourced mutable state; AP/CP data
    separation visible in the schema; build against block contracts not custom components;
    no stored procedures.

  - **Common failure modes (from zone-b-migration-path.md §5):** Server-side feature gates
    re-centralizing the architecture; shared Postgres schema blocking per-tenant isolation;
    relay mistaken for a backup; Phase 1 without a feature flag.

- [ ] **Step 3: Quality check (QC-1 through QC-10, QC-7 applies)**

- [ ] **Step 4: Save**

---

### Task 21: Chapter 19 — Shipping to Enterprise

**File:** `part-4-implementation-playbooks/ch19-shipping-to-enterprise.md`
**Target:** 3,000–4,000 words
**Sources:** v13.md §16 (IT Governance), v5.md §5 (Deployment in Managed Environments),
Sunfish `docs/specifications/mdm-config-schema.md`,
Sunfish `docs/specifications/air-gap-deployment.md`

- [ ] **Step 1: Write chapter outline**

  ```
  ## The Procurement Conversation
  ## Build and Packaging Pipeline
  ## Code Signing and Notarization
  ## MDM Deployment
  ## SBOM Generation and CVE Response
  ## Admin Tooling for Revocation
  ## Air-Gap Deployment
  ## The Operational Runbook Minimum
  ```

- [ ] **Step 2: Write all sections (~3,200 words)**

  - **Procurement conversation:** AGPLv3 + managed relay subscription = no per-seat license,
    one predictable line item. Open-source core removes vendor lock-in objection. But: some
    corporate legal teams have categorical AGPLv3 policies (network use clause triggers on
    internal modifications). Dual-license commercial exception resolves this — specify it
    before the first enterprise conversation. From R2 Voss prompt 5 and R2 Kelsey prompt 3.

  - **Build and packaging:** Windows MSIX installer (provisions MAUI host + sync daemon as
    Windows Service). macOS signed + notarized `.pkg`/`.dmg` (installs `.app` bundle +
    background launch agent). Multi-target MAUI build (`net10.0-windows`, `net10.0-maccatalyst`,
    `net10.0-ios`, `net10.0-android`). From v5.md §5.1 and Anchor README.

  - **Code signing and notarization:** macOS: Developer ID certificate, `notarytool`,
    stapling. Both foreground MAUI app and background sync daemon covered. Windows:
    Authenticode signing, App Control for Business (WDAC) trusted-publisher rules —
    not per-hash rules. From v5.md §5.2–5.3.

  - **MDM deployment:** Intune/Jamf profiles, silent installation, pre-seeded configuration
    via MDM profile. From v13.md §16.1. MDM compliance check at capability negotiation
    (not just at install time — a node that falls out of compliance mid-session is rejected
    before it touches data). Reference Sunfish `mdm-config-schema.md` for configuration keys.

  - **SBOM:** CycloneDX format satisfies NTIA minimum elements and CISA guidance. Syft for
    generation, Grype for vulnerability scanning. Generated at build time from source
    (not assembled post-install). CVE response SLA: critical within 24h, high within 7 days.
    From R1 Voss conditions and R2 Voss prompt 1.

  - **Admin revocation tooling (from R2 Voss prompt 3):** IT administrator needs a concrete
    interface — not "the system propagates revocation" but "open Admin Console, select user,
    click Revoke Access, relay broadcasts key rotation to all active peers." Sketch the
    admin CLI command or console action. `sunfish admin revoke --user <user-id> --team <team-id>`.

  - **Air-gap deployment:** Internal update server, internal relay, SBOM distribution channel.
    Reference Sunfish `air-gap-deployment.md`. Configuration pre-seeded via MDM profile with
    internal relay endpoint, internal update feed URL, and proxy settings.

  - **Operational runbook minimum:** Three required runbooks before enterprise GA:
    1. Node deprovisioning (user leaves organization)
    2. Incident response (node compromise, key compromise)
    3. Container update rollout (zero-downtime path, rollback procedure)

- [ ] **Step 3: Quality check (QC-1 through QC-10, QC-7 applies)**

- [ ] **Step 4: Save**

---

### Task 22: Chapter 20 — Designing UX for Sync and Conflict

**File:** `part-4-implementation-playbooks/ch20-ux-sync-conflict.md`
**Target:** 2,500–3,500 words
**Sources:** v13.md §13 (UX Design Philosophy), v13.md §14 (Non-Technical Trust Gap),
v5.md §6 (UX and Conflict Handling)

- [ ] **Step 1: Write chapter outline**

  ```
  ## The Complexity Hiding Standard
  ## The Three Always-Visible Indicators
  ## AP/CP Visibility by Data Class
  ## Optimistic UI and Confirmed States
  ## The Conflict Inbox and Bulk Resolution
  ## Designing for Failure Modes
  ## The First-Run Experience
  ## The Non-Technical Trust Gap
  ```

- [ ] **Step 2: Write all sections (~2,800 words)**

  - **Complexity hiding standard from v13.md §13.1:** A non-technical user should be
    unable to determine, from normal use, whether the application is local-first or
    cloud-first. The only visible difference should be that it works offline.

  - **Three indicators from v13.md §13.2:** Node health (is the local node running and
    healthy), link status (is any peer reachable), data freshness (how stale is the
    data I'm viewing). Always visible in status bar. Non-intrusive under normal conditions.
    In Sunfish: `SunfishNodeHealthBar` implements all three live.

  - **AP/CP visibility table from v13.md §13.2:** Resource availability (5-min threshold,
    amber indicator + booking blocked offline), financial balances (15-min, "as of [timestamp]"
    + writes require online), scheduled appointments (10-min, calendar freshness badge),
    team membership (24-hour, surfaced only at role-dependent action).

  - **Optimistic UI:** Writes applied locally, synced asynchronously. Button states:
    pending (submitted to local CRDT, not yet gossiped), confirmed (received by at least
    one peer), failed (rejected by circuit breaker on reconnect). Use `ICrdtEngine` write
    result to drive button state.

  - **Conflict inbox and bulk resolution from v13.md §13.3 and v5.md §6.2:** Conflicts
    grouped by record type and field. "Prefer mine / prefer remote / merge by rule X."
    "Resolve all similar" applies chosen rule to all conflicts of the same shape.
    All decisions logged as events for audit. No undifferentiated conflict list.

  - **Designing for failure modes:** Offline mode (full fidelity, no degraded banner unless
    CP data is stale). Partial connectivity (relay reachable but peers offline — gossip
    via relay only, peer-to-peer unavailable). Quarantine queue surfaced: "3 edits made
    offline are pending validation" with inline review before sync.

  - **First-run experience (from R2 Ferreira prompt 2):** Zero-state new user after installation.
    Show: install → open → pick "Start a new team" or "Join an existing team". New team:
    creates founder attestation, prompts for first BYOC backup configuration before showing
    the app. Join: QR scan or paste bundle, shows sync progress. Do not show an empty app
    with no guidance.

  - **Non-technical trust gap from v13.md §14:** The framing: "Your data lives on your
    computers, in your office. It keeps working when the internet is out. If we disappear,
    your software keeps running." The four elements from v13.md §14.3: champion, comparison,
    fallback story, support path. These are UX problems, not just marketing problems.

- [ ] **Step 3: Quality check (QC-1 through QC-10, QC-7 applies)**

- [ ] **Step 4: Save**

---

## Phase 6 — Epilogue and Appendices

*Dependencies: All chapters complete. Epilogue draws from everything; write it last.*

---

### Task 23: Epilogue — What the Stack Owes You

**File:** `epilogue/epilogue-what-the-stack-owes-you.md`
**Target:** 2,000–3,000 words
**Sources:** v5.md §9 (Open Questions), v5.md §10 (Conclusion),
v13.md Conclusion, R2 Council Consensus Statement

- [ ] **Step 1: Write epilogue (~2,500 words)**

  Five sections:

  1. **What the council agreed the architecture must never compromise** — the seven
     non-negotiables from Ch 10's synthesis, stated as obligations. Not what the architecture
     can do — what it owes its users. Frame each as a promise, not a feature.

  2. **The open questions that remain genuinely unsettled** — from v5.md §9:
     KEK compromise incident response at scale, relay multi-tenancy threat model for
     high-risk verticals, long-term archival formats, formal verification of domain-level
     merge invariants. Plus R2 additions: GDPR Art. 17 in CRDT systems, analytics model
     without re-centralization. Be honest: this book doesn't resolve these. It names them.

  3. **The implementation drift risk** — the most common way local-first architectures
     fail in practice: "just a quick server-side check" that gradually re-centralizes
     the system. The telemetry model must be decided before the first product analytics
     request. Enumerate the drift anti-patterns from R2 Ferreira prompt 5 and
     zone-b-migration-path.md §5.

  4. **What comes next** — Sunfish milestones, community governance model, invitation
     to contribute. The two accelerators (Anchor, Bridge) and what remains unbuilt.
     The sync daemon sub-document as the first critical deliverable (from v13.md Conclusion).

  5. **The obligation** — closing. If this architecture asks users to trust a new
     infrastructure model, it owes them: data portability (the export button exists),
     disaster recovery (the non-technical recovery path is documented and tested),
     and honest failure modes (symmetric NAT is acknowledged, GC limits are stated,
     GDPR tension is disclosed). These aren't features. They are the cost of making
     the claim that the user owns their data.

- [ ] **Step 2: Quality check**
  ```
  [ ] Does not re-introduce the architecture (trust the reader has read the book)
  [ ] Open questions are specific and falsifiable, not vague
  [ ] The obligation section is direct and personal, not corporate
  [ ] Leaves the reader with a specific next action (clone Sunfish, read a paper, contribute)
  ```

- [ ] **Step 3: Save**

---

### Task 24: Appendix A — Sync Daemon Wire Protocol

**File:** `appendices/appendix-a-sync-daemon-wire-protocol.md`
**Target:** 1,500–2,500 words
**Sources:** Sunfish `docs/specifications/sync-daemon-protocol.md`,
v13.md §6.2 (handshake sequence), Sunfish `accelerators/anchor/README.md` (QR payload format)

- [ ] **Step 1: Write the appendix**

  - Formal CBOR message type definitions for all five handshake phases
  - Field-level annotations (data type, required/optional, versioning notes)
  - Example HELLO / CAPABILITY_NEG / ACK exchange with concrete field values
  - DELTA_STREAM message format (op_type, stream_id, vector_clock, payload)
  - GOSSIP_PING format (membership list excerpt, vector clock summary)
  - Error codes with retry semantics (RATE_LIMIT_EXCEEDED, VERSION_INCOMPATIBLE,
    ATTESTATION_REQUIRED, EPOCH_MISMATCH)
  - Backward-compatibility policy: which fields are versioned, which are stable
  - QR onboarding payload wire format (from Anchor README):
    4-byte length prefix + CBOR AttestationBundle + 4-byte snapshot length + snapshot bytes

- [ ] **Step 2: Quality check**
  ```
  [ ] Every message type named in Ch 14 appears here with a formal definition
  [ ] Error codes are specific enough to guide implementation
  [ ] CBOR types are named (uint, tstr, bstr, map, array) not left as "bytes"
  ```

- [ ] **Step 3: Save**

---

### Task 25: Appendix B — Threat Model Worksheets

**File:** `appendices/appendix-b-threat-model-worksheets.md`
**Target:** 1,500–2,000 words
**Sources:** v13.md §11.1 (Threat Model), R1 Okonkwo standard prompts,
R2 Okonkwo attack tree prompt

- [ ] **Step 1: Write the appendix**

  Section 1: **Asset inventory template**
  ```
  | Asset | Classification | Location | Owner | Sensitivity |
  |---|---|---|---|---|
  | User CRDT documents | Team-confidential | Local SQLCipher DB | User | High |
  | Role KEKs | Team-secret | OS keystore | Admin | Critical |
  | ... | | | | |
  ```

  Section 2: **Actor taxonomy template**
  ```
  | Actor | Access level | Likely motivation | Capability |
  |---|---|---|---|
  | External attacker | Physical access to endpoint | Data theft | Low-High |
  | Malicious insider | Team member with role access | Data exfiltration | Medium |
  | Compromised relay | Transport layer | Traffic analysis | Limited |
  | ... | | | |
  ```

  Section 3: **Worked example — construction PM vertical**
  Fill the asset inventory, actor taxonomy, and attack tree for a five-person construction
  project management team. Primary assets: bid documents, subcontractor contracts, project
  schedules. Primary actors: disgruntled subcontractor with stolen device, competitor.
  Primary attacks: physical access to stolen laptop, relay traffic analysis to determine
  which teams are active on a bid.

  Section 4: **Key compromise incident response template**
  From Ch 15 — four sections: detection checklist, re-keying procedure steps,
  data-at-risk scope calculation, user notification script.

- [ ] **Step 2: Quality check**
  ```
  [ ] Templates are usable without additional explanation
  [ ] Worked example is specific enough to be adapted, not just illustrative
  [ ] IR template is actionable — each step has a verb and an owner
  ```

- [ ] **Step 3: Save**

---

### Task 26: Appendix C — Further Reading

**File:** `appendices/appendix-c-further-reading.md`
**Target:** 800–1,200 words

- [ ] **Step 1: Write the appendix**

  Organized sections with annotations (not just a flat list):

  **Local-First Literature**
  - Kleppmann et al., "Local-First Software: You Own Your Data, in Spite of the Cloud" (2019) — the foundational paper; start here
  - Ink & Switch essays: Pushpin, Backchat — production local-first experience reports
  - CRDTech community references — active practitioner discussion

  **CRDT Libraries**
  - Yjs (`github.com/yjs/yjs`) — most mature, excellent docs, wide deployment
  - yrs / y-crdt (`github.com/y-crdt/y-crdt`) — Rust port, basis for .NET bindings
  - Loro (`github.com/loro-dev/loro`) — compact encoding, shallow snapshots, ADR 0028 selection
  - loro-cs (`github.com/sensslen/loro-cs`) — C# bindings for Loro; evaluate API coverage before committing
  - Automerge — excellent design reference; no first-class .NET binding as of writing

  **Distributed Systems Foundations**
  - Kleppmann, *Designing Data-Intensive Applications* — the closest intellectual ancestor to this book; read chs 5, 8, 9 first
  - Flease paper (Meijer, Reuter) — failure-aware lease management without dedicated coordinators
  - Shapiro et al., "A Comprehensive Study of Convergent and Commutative Replicated Data Types" — CRDT theory

  **Production Analogues**
  - Linear blog posts on sync architecture — the lightweight SQLite replica model
  - Figma blog posts on multiplayer — CRDT in production at scale
  - PowerSync / ElectricSQL documentation — declarative partial sync in practice
  - Actual Budget — the closest commercial analogue to Zone A local-first

  **Schema Evolution**
  - Ink & Switch, Cambria — bidirectional schema lenses for CRDTs
  - DXOS ECHO documentation — decentralized schema migration in production

- [ ] **Step 2: Quality check**
  ```
  [ ] Every cited work in the main text appears here with context
  [ ] Annotations explain why to read each reference, not just what it is
  [ ] loro-cs status note included (API coverage evaluation required)
  ```

- [ ] **Step 3: Save**

---

### Task 27: Appendix D — Testing the Inverted Stack

**File:** `appendices/appendix-d-testing-the-inverted-stack.md`
**Target:** 2,000–2,500 words
**Sources:** v13.md §15 (Testing Strategy — full section)

- [ ] **Step 1: Write the appendix**

  Draw entirely from v13.md §15. Translate into practitioner prose.

  Section 1: **The Five-Level Testing Pyramid**
  Table from v13.md §15.1 with expanded rationale for each level:
  1. Property-based: CRDT convergence, idempotency, commutativity, monotonicity —
     these are mathematical properties; test them with a property-based framework
     (FsCheck for .NET, fast-check for JS)
  2. Integration tests with real dependencies: sync handshake, data path — no mocks
     for the sync daemon
  3. Fault injection in CI: partition, packet loss, node crash — use Testcontainers
     with network partition simulation
  4. Deterministic simulation: mixed-version nodes, epoch transitions, lease edge cases —
     the hardest tier; use simulation harness with controllable clocks
  5. Chaos testing in staging: unknown failure modes under production-representative load

  Section 2: **Mandatory Scenarios Before First Production Release**
  All scenarios from v13.md §15.2, grouped by category:

  *Partition and reconnect:*
  - Two nodes offline for 30 days → merge without data loss
  - Three-node team loses CP quorum → write blocked, surfaced to user, not silently dropped
  - Node returns with 1000+ queued ops → anti-entropy completes without timeout

  *Schema migration:*
  - Node on schema N-1 syncs with N → lenses translate both directions
  - Epoch transition while node offline → snapshot download + resume
  - "Couch device" (offline for 3+ major versions) → capability negotiation rejects with error

  *Flease edge cases:*
  - Lease holder goes offline mid-write → expiry, new lease, prior write quarantined
  - Partition during lease negotiation → both sides identify no-quorum correctly

  *Security:*
  - Storage extracted without credentials → encryption prevents plaintext
  - Role key rotated, former member reconnects → cannot decrypt records after rotation

  *Ledger:*
  - Sum-to-zero invariant holds under retries and failures
  - Duplicate domain events produce exactly one posting set

  Section 3: **CRDT Growth Tests**
  Stress tests: programmatic edit load on high-churn documents. Verify library-level
  compaction + application sharding keep document size bounded. Measure op log size
  at 30 days, 90 days, 1 year of simulated usage.

- [ ] **Step 2: Quality check**
  ```
  [ ] Every mandatory scenario has a concrete pass/fail criterion
  [ ] Testing pyramid maps to real .NET tooling (FsCheck, Testcontainers, xUnit)
  [ ] CRDT growth test includes a numeric bound (not just "bounded")
  ```

- [ ] **Step 3: Save**

---

## Phase 7 — Final Assembly Check

### Task 28: Word count audit and final review

- [ ] **Step 1: Count words per file**

  ```bash
  # From inverted-stack-book/ directory
  wc -w **/*.md
  ```

  Expected totals per section:
  ```
  Prospectus:               2,500–3,500
  Front matter:             1,400–1,700
  Part I (Ch 1–4):         13,000–17,000
  Part II (Ch 5–10):       18,000–23,000
  Part III (Ch 11–16):     19,000–24,000
  Part IV (Ch 17–20):      12,000–16,000
  Epilogue:                 2,000–3,000
  Appendices A–D:           6,000–9,000
  TOTAL TARGET:            74,000–97,000
  ```

- [ ] **Step 2: Run full quality checklist across all 27 files**

  For each chapter file, verify QC-1 through QC-10. Any file failing three or more
  checks returns to its task for revision before assembly.

- [ ] **Step 3: Verify all cross-references resolve**

  Search for every "see Ch X", "Part III", "Appendix A" reference in all files.
  Confirm the referenced content exists and the reference is accurate.

  ```bash
  grep -r "see Ch\|Part III\|Part IV\|Appendix" . --include="*.md"
  ```

- [ ] **Step 4: Verify no stub files remain**

  ```bash
  grep -r "<!-- stub -->" . --include="*.md"
  ```

  Expected output: no matches. Any remaining stubs = incomplete task.

- [ ] **Step 5: Run assembly**

  Follow `ASSEMBLY.md` instructions. Verify the assembled output renders without
  broken markdown (missing closing fences, unbalanced headers, orphaned footnotes).

---

## Execution Order Summary

| Phase | Tasks | Can Parallelize |
|---|---|---|
| Phase 0 | Task 0 (scaffold) | — |
| Phase 1 | Task 1 (prospectus), Task 2 (front matter) | After Task 0 |
| Phase 2 | Tasks 3–6 (Ch 1–4) | Sequential: Ch1→Ch2→Ch3→Ch4 |
| Phase 3 | Tasks 7–11 (Ch 5–9) then Task 12 (Ch 10) | Ch 5–9 parallel; Ch 10 after all five |
| Phase 4 | Task 13 (Ch 11) then Tasks 14–18 (Ch 12–16) | Ch 11 first; Ch 12–16 largely parallel |
| Phase 5 | Task 19–20 sequential, Tasks 21–22 parallel | Ch 17→Ch 18 sequential; Ch 19 + Ch 20 parallel |
| Phase 6 | Task 23 (epilogue) last; Tasks 24–27 (appendices) parallel | Epilogue last; appendices alongside Phase 5 |
| Phase 7 | Task 28 (audit) | After everything |
