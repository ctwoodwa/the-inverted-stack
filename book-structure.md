# BOOK-STRUCTURE

## Working Title

**Working title:** *The Inverted Stack: Local-First Nodes in a SaaS World*

---

## Reference Implementation

**Sunfish** (`github.com/ctwoodwa/Sunfish`) is the open-source reference implementation
developed alongside this book. It is in active early development; the architecture described
here is its specification. Two canonical accelerators exist:

- **Anchor** (`accelerators/anchor/`) — Zone A local-first desktop (.NET MAUI Blazor Hybrid,
  offline-by-default, SQLCipher, Ed25519 device keys)
- **Bridge** (`accelerators/bridge/`) — Zone C hybrid multi-tenant SaaS (.NET Aspire, Blazor
  Server, per-tenant data-plane isolation, hosted-node-as-SaaS)

Sunfish APIs are pre-1.0 and subject to change. The book references packages by name
(`Sunfish.Kernel.Sync`, `Sunfish.Foundation.LocalFirst`) rather than specific class APIs.

> **CRDT engine note:** This book specifies Loro as the aspirational primary CRDT engine for
> .NET (compact encoding, shallow snapshots, Rust-native performance). Sunfish's reference
> implementation uses YDotNet (Yjs .NET bindings) — the practical choice while Loro's C# bindings
> (`loro-cs`) remain community-maintained and minimal. The architecture is engine-agnostic via
> `ICrdtEngine`; the book addresses both paths and the evaluation criteria for choosing between them.

---

## Front Matter

### Foreword
*Placeholder — reserved for a voice from the local-first community (Ink & Switch contributor,
Automerge/Yjs maintainer, or practitioner with a recognizable name in the distributed systems
space). Written last.*

### Preface
- Why this book exists: the gap between local-first ideals and production-grade systems
- Who it's for: software architects, technical founders, senior engineers, IT decision-makers
- How to read it: Part I convinces, Part II stress-tests, Part III specifies, Part IV implements
- Note on Sunfish as the living reference implementation
- Note on the Kleppmann Council as structured adversarial evaluation

---

## Part I — The Thesis and the Pain
*~16,200 words. Establishes the problem, the solution shape, and when to use it.*

### Chapter 1 — When SaaS Fights Reality
*~5,200 words*
- The hidden costs of the SaaS bundle: vendor dependency, data custody, pricing risk
- Six concrete failure modes: outage and the dependency chain, vendor disappearance,
  connectivity gaps, data inaccessibility, price capture, and the third-party veto
  (government or regulatory authority restricts access regardless of vendor or customer preference)
- What actually breaks first when all state lives in someone else's cloud
- Why users have accepted this — and why that acceptance is eroding

### Chapter 2 — Local-First: From Sync Toy to Serious Stack
*~4,000 words*
- The seven local-first ideals (Kleppmann et al.) and why they matter
- A tour of existing implementations: what each does, exactly where it stops short
  (Obsidian: file-based, no structured data; Linear: lightweight SQLite replica, not a full node;
  Automerge demos: document-centric, no business logic; Actual Budget: closest commercial analogue)
- The missing step: a full node on the workstation — UI, business logic, sync daemon, storage —
  not just a smarter cache
- What "serious stack" requires that toy examples omit

### Chapter 3 — The Inverted Stack in One Diagram
*~3,500 words*
- The central inversion: local node as primary, cloud as relay/backup/discovery
- Visual: five-layer model (presentation, application logic, sync daemon, storage, relay)
- How this changes failure modes vs. classic SaaS — and which failure modes it creates
- The two canonical deployment shapes: Anchor (Zone A) and Bridge (Zone C) introduced
- A first look at the .NET MAUI/Blazor Hybrid + sync daemon stack

### Chapter 4 — Choosing Your Architecture
*~3,500 words*
- The core question: does value derive from the user's own data, or from aggregating across users?
- Five filters: consistency requirements, data ownership profile, connectivity environment,
  business model alignment, team capability and timeline
- The three outcome zones: Zone A (local-first node), Zone B (traditional SaaS/website), Zone C (hybrid)
- Anchor as the Zone A reference; Bridge as the Zone C reference
- The practical shortcut: three questions that produce a fast answer for most cases
- When *not* to use the inverted stack — and why the CAP theorem is not a negotiating position

---

## Part II — The Council Reads the Paper
*~20,000 words. Five domain experts stress-test the architecture across two rounds.
Each chapter has two acts: Round 1 objections and blocking issues, then what changed,
then Round 2 verdict. The architecture fails first inspection — and survives the second.*

### Chapter 5 — The Enterprise Lens
*~3,500 words | Council member: Dr. Marguerite Voss, Enterprise Infrastructure Architect*
- Her lens: will this pass a real procurement committee? Can IT actually manage it?
- Round 1: MDM integration, code signing, SBOM, incident response gap (BLOCKED)
- What changed: named Intune/Jamf policies, signed/notarized installer, incident response runbook,
  zero-downtime container update path, SBOM toolchain (Syft/Grype)
- Round 2: PROCEED WITH CONDITIONS — AGPLv3 copyleft implications, SBOM CI/CD timing,
  Podman WSL2 vs. Hyper-V, admin revocation tooling
- Takeaway: the non-negotiable constraints any serious local-first product must satisfy before
  IT will allow it on managed endpoints

### Chapter 6 — The Distributed Systems Lens
*~3,500 words | Council member: Prof. Dmitri Shevchenko, Distributed Systems Researcher*
- His lens: is the synchronization model theoretically sound? Does "CRDT handles it" mean
  the user sees correct data?
- Round 1: CRDT GC absent, Flease split-write window unaddressed (BLOCKED)
- What changed: three-tier GC policy, stale peer recovery protocol, Flease split-write proof,
  reconnection storm handling, CRDT operation validation
- Round 2: PROCEED WITH CONDITIONS — stale peer recovery when vector clock predates GC horizon,
  linearizable operation enumeration, CRDT store as durable partition buffer
- Takeaway: convergence at the data-structure level is not the same as correctness at the
  domain level — here is where the boundary lies

### Chapter 7 — The Security Lens
*~3,500 words | Council member: Nia Okonkwo, Application Security Practitioner*
- Her lens: what is the actual threat model? What does an attacker with physical access gain?
- Round 1: key compromise incident response absent (BLOCKED)
- What changed: key hierarchy diagram (root org → role KEKs → per-node wrapped keys → per-record),
  key compromise detection and re-keying procedure, offline node revocation reconnection flow
- Round 2: PROCEED WITH CONDITIONS — relay traffic analysis limitation, GDPR Article 17 and
  crypto-shredding, release signing key custody, Sigstore supply-chain spec
- Takeaway: distributing data to endpoints solves the central honeypot problem and creates
  a distributed one — here is how to manage it honestly

### Chapter 8 — The Product & Economic Lens
*~3,500 words | Council member: Jordan Kelsey, Product Manager / Startup Founder*
- His lens: will anyone buy this? What is the payback period? Can the relay sustain a team of five?
- Round 1: no first customer archetype, no OSS-to-paid conversion mechanism (BLOCKED)
- What changed: construction vertical selection, five-step customer development path,
  relay economics model (10/100/1,000 teams), competitive comparison table, dual-license strategy
- Round 2: PROCEED WITH CONDITIONS — customer acquisition channel, governance model,
  relay commoditization moat, dual-license CLA before the repo opens
- Takeaway: how to fund a product that doesn't own the primary database — and why the
  managed relay is the right unit of competitive analysis

### Chapter 9 — The Local-First Practitioner Lens
*~3,500 words | Council member: Tomás Ferreira, Local-First Community Practitioner*
- His lens: does this actually work for real users? Does the paper understand existing work
  or reinvent it poorly?
- Round 1: no data portability path — a paper about data ownership with no export button (BLOCKED)
- What changed: plain-file export path, full non-technical disaster recovery walkthrough,
  symmetric NAT / relay-down failure mode acknowledgment, community governance model
- Round 2: PROCEED — all seven Kleppmann ideals satisfied; no blocking conditions
- Takeaway: what actually works in practice for users, teams, and community contributors

### Chapter 10 — Synthesis: What the Council Finally Agreed On
*~2,500 words*
- The non-negotiable properties that emerged from both rounds: data minimization at the
  protocol layer, subscription filtering at send not receive, MDM compliance check at
  capability negotiation, three-tier CRDT resolution model, dual-license from day one
- The open questions the council did not fully resolve (relay commoditization moat,
  GDPR Article 17 in CRDT systems, long-term archival format stability)
- How the agreed properties shape the reference architecture in Part III
- Bridge into Part III: from evaluation to specification

---

## Part III — The Reference Architecture
*~22,000 words. The complete technical specification. Part II tells you what constraints
must be satisfied; Part III specifies how to satisfy them. Written as a reference —
return to individual chapters as you build.*

### Chapter 11 — Node Architecture
*~4,000 words*
- The microkernel monolith: stable kernel + domain plugins under strict contracts
- Kernel responsibilities: node lifecycle, sync daemon, CRDT engine abstraction, schema migration
  infrastructure, security primitives, partial sync engine, plugin registry
- Plugin contracts: `ILocalNodePlugin`, `IStreamDefinition`, `IProjectionBuilder`,
  `ISchemaVersion`, `IUiBlockManifest`
- The UI kernel: four-tier layering (Foundation tokens → Framework-Agnostic contracts →
  Blocks & Modules → Compat/Adapter layer); sync-state semantic tokens
- Process boundaries and IPC: Unix domain socket transport between shell and sync daemon
- Sunfish package map: `Sunfish.Kernel.*`, `Sunfish.Foundation.LocalFirst`, `Sunfish.UI.*`

### Chapter 12 — CRDT Engine and Data Layer
*~4,000 words*
- The three-layer CRDT architecture: data layer (maps, lists, text, counters),
  semantic layer (domain rules interpreting CRDT changes), view layer (projections and indexes)
- YDotNet (Yjs .NET) as the reference implementation; Loro evaluation criteria and
  when to prefer it; the `ICrdtEngine` abstraction that keeps the choice reversible
- Per-record CAP positioning: AP (CRDT merge) vs. CP (distributed lease); which record
  classes belong where and why
- The double-entry ledger as the canonical CP-class subsystem: posting engine,
  idempotency, CQRS read models, period closing and rollup snapshots
- CRDT growth and GC: library-level compaction, application-level document sharding,
  periodic shallow snapshots; the three-tier GC policy (aggressive / 90-day / no-GC)
- Five-layer storage architecture: local encrypted DB, CRDT/event log, BYOC backup,
  content-addressed distribution, decentralized archival

### Chapter 13 — Schema Migration and Evolution
*~3,500 words | NEW*
- Why schema migration is the hardest operational problem in a local-node architecture:
  nodes update independently, teams run mixed versions simultaneously
- The expand-contract (parallel change) pattern: expand phase, compatibility window,
  contract phase, epoch bump
- Event versioning and upcasters: additive changes, new event type variants, upcaster chains,
  the accumulation problem and mandatory stream compaction
- Bidirectional schema lenses: declarative transformation functions between schema versions,
  version graph traversal, field renames and structural reorganizations
- Schema epoch coordination: quorum-agreed epoch announcement, copy-transform background job,
  cutover and old-epoch retirement; the "couch device" returning after three major versions
- Stale peer recovery: what happens when a reconnecting peer's vector clock predates the GC horizon

### Chapter 14 — Sync Daemon Protocol
*~3,500 words*
- The sync daemon as a separate long-running process: why the separation matters,
  lifetime and restart behavior, Unix domain socket IPC
- Gossip anti-entropy: membership list, vector clocks, periodic delta exchange,
  tiered peer discovery (mDNS → mesh VPN → managed relay)
- Five-phase handshake: HELLO, CAPABILITY_NEG, ACK, DELTA_STREAM, GOSSIP_PING
- Data minimization invariant: subscription filtering at the send tier, not the application layer
- Distributed lease coordination (CP mode): Flease-model lease negotiation, quorum arithmetic,
  split-write safety, lease expiry and offline release
- CBOR wire format: message types, versioning scheme, backward-compatibility policy
- Reconnection storm handling: behavior when 50+ nodes reconnect simultaneously
- Sunfish relay configuration reference: `MaxConnectedNodes`, `AllowedTeamIds`,
  relay-only vs. attested hosted peer vs. no hosted peer trust levels

### Chapter 15 — Security Architecture
*~4,000 words*
- Threat model: distributed endpoints vs. central honeypot; insider threat; physical access;
  supply chain; relay compromise
- Device and user identity: Ed25519 device keypairs, OS-native keystore, OIDC/SAML IdP mapping
- DEK/KEK envelope encryption: per-document DEKs, per-role KEKs, key wrapping and distribution
- Key rotation and revocation: rotation work proportional to document count not size;
  re-keying procedure; offline node revocation window and reconnection behavior
- Four defensive layers: encryption at rest (SQLCipher), field-level encryption,
  stream-level data minimization, circuit breaker quarantine queue
- Key compromise incident response: detection, re-keying procedure, data-at-risk scope,
  user-visible notification, forward secrecy window
- Compliance framework mapping: SOC 2, HIPAA, GDPR Article 17 and crypto-shredding
- In-memory key material: locked memory pages, key zeroing on process exit, re-authentication intervals

### Chapter 16 — Persistence Beyond the Node
*~3,000 words | CONSOLIDATED: Storage/Backup + Relay/Federation*
- Local persistence: encrypted database format, durability guarantees, durability vs. performance tradeoffs
- BYOC backup patterns: object storage adapters, rclone integration, backup status UX
  (Protected / Attention / At Risk), the "last device destroyed" recovery walkthrough
- Long-term archival: snapshot formats, signed append-only logs, regulated-industry retention
- Relay architecture: relay responsibilities vs. non-responsibilities; what the relay stores
  (ciphertext only) vs. what it cannot access; multi-tenancy and tenant isolation
- Privacy posture: relay metadata and traffic analysis limitation; logging minimization;
  self-hosted relay as the high-sensitivity alternative
- Federation: peer discovery, NAT traversal tiers, symmetric NAT failure mode acknowledgment

---

## Part IV — Implementation Playbooks
*~14,000 words. Minimal paths to working implementations. References Part III for
specification; does not repeat it. Sunfish packages are the starting point, not the
finished product.*

### Chapter 17 — Building Your First Node
*~4,000 words*
- The Sunfish Anchor accelerator as your starting point: what it gives you, what is
  still placeholder, how to orient yourself in the codebase
- Minimal MAUI + sync daemon + IPC skeleton: `MauiProgram.cs` wiring,
  `AddSunfishEncryptedStore()`, `AddSunfishKernelRuntime()`, `AddSunfishKernelSecurity()`
- Wiring in a CRDT document and syncing between two devices: YDotNet document creation,
  gossip daemon bootstrap, mDNS peer discovery
- QR-code onboarding: the three-step flow (install, authenticate, sync), CBOR payload
  wire format, founder vs. joiner attestation bundles
- Local-first UX basics: `SunfishNodeHealthBar`, offline edit indicators, sync status tokens

### Chapter 18 — Migrating an Existing SaaS
*~3,500 words*
- The Sunfish Bridge accelerator as the Zone C reference: per-tenant data-plane isolation,
  hosted-node-as-SaaS, ciphertext-only relay
- Phased migration: read-only mirror → offline editing for non-conflicting domains →
  full local authority for new projects → gradual backfill of legacy records
- Phase-transition success criteria: what validates readiness to advance; how to pause
  at Phase 2 indefinitely for a risk-averse change advisory board
- Data mapping: translating relational schemas to CRDT document structures; coexistence
  with the legacy backend during transition
- Running pilots without destabilizing the existing product

### Chapter 19 — Shipping to Enterprise
*~3,500 words*
- Build and packaging pipelines: MSIX installer (Windows), .pkg/.dmg (macOS),
  multi-target MAUI builds
- Code signing and notarization: Apple Developer ID, `notarytool`, stapling;
  Authenticode signing, App Control for Business (WDAC) trusted-publisher rules
- MDM deployment: Intune/Jamf profiles, silent installation, pre-seeded configuration,
  SBOM generation in CI (Syft for generation, Grype for vulnerability scanning),
  CVE response SLA
- Podman substrate choice: WSL2 vs. Hyper-V — implications for corporate images and
  virtualization product conflicts; recommended defaults
- Admin tooling: revocation workflow interface (console UI or CLI sketch), zero-downtime
  container update path, deprovisioning runbook
- Air-gap deployment: internal update server, internal relay, SBOM distribution channel

### Chapter 20 — Designing UX for Sync and Conflict
*~3,000 words*
- The complexity hiding standard: a non-technical user should be unable to determine
  whether the application is local-first or cloud-first
- Status indicators: node health, link status, data freshness — non-intrusive under
  normal conditions, informative under degraded ones
- AP/CP visibility by data class: staleness thresholds, amber indicators, freshness badges,
  "as of [timestamp]" labels
- Optimistic UI: writes applied locally, synced asynchronously, visual confirmation states
- Conflict inbox and bulk resolution: grouping by record type, "prefer mine / prefer remote /
  merge by rule", "resolve all similar", audit log of all decisions
- Designing for failure: offline mode, partial connectivity, degraded states, the circuit
  breaker quarantine queue surfaced to the user
- First-run experience: zero-state onboarding for a brand-new user with no prior data

---

## Epilogue — What the Stack Owes You
*~2,500 words*
- What the council agreed the architecture must never compromise
- The open questions that remain genuinely unsettled: relay commoditization moat,
  GDPR Article 17 in CRDT systems, formal verification of domain-level invariants,
  long-term archival format stability
- The implementation drift risk: how "just a quick server-side check" gradually
  re-centralizes a local-first system — and how to prevent it
- What comes next: Sunfish milestones, community governance, invitation to contribute
- The stack's obligation: if it asks users to trust a new infrastructure model,
  it owes them data portability, disaster recovery, and honest failure modes

---

## Appendices

### Appendix A — Sync Daemon Wire Protocol
- Formal CBOR message formats for all five protocol phases
- Example request/response sequences with field-level annotations
- Error codes, retry semantics, and backward-compatibility policy

### Appendix B — Threat Model Worksheets
- Asset inventory template, actor taxonomy, attack tree structure
- Filled example for the construction PM vertical
- Key compromise incident response template

### Appendix C — Further Reading
- Local-first literature: Kleppmann et al., Ink & Switch essays (Pushpin, Backchat),
  CRDTech community references
- CRDT libraries: Yjs, Loro, Automerge — comparison and selection criteria
- Production analogues: Figma, Linear, Obsidian, Actual Budget, PowerSync, ElectricSQL
- Distributed systems foundations: DDIA, Flease paper, Cambria lenses

### Appendix D — Testing the Inverted Stack
- The five-level testing pyramid: property-based, integration, fault injection,
  deterministic simulation, chaos testing
- Mandatory scenarios before first production release: partition and reconnect,
  schema migration, Flease edge cases, security invariants, ledger correctness
- CRDT growth tests: stress scenarios for high-churn documents
- Test strategy for the sync protocol: network partition simulation, clock skew injection,
  concurrent edit generation, GC boundary conditions, Byzantine operation injection

### Appendix E — Citation Style
- IEEE numeric citation style: in-text bracketed numbers [1], [2]; reference list ordered by
  first appearance
- Common reference formats: book, edited chapter, journal article, conference paper,
  web/online source
- Consistency rules for multi-source citations and capitalization

---

## Word Count Targets

| Section | Target |
|---|---|
| Front Matter (Preface + Foreword) | ~2,000 |
| Part I — Thesis and Pain (Ch 1–4) | ~16,200 |
| Part II — The Council (Ch 5–10) | ~20,000 |
| Part III — Reference Architecture (Ch 11–16) | ~22,000 |
| Part IV — Implementation Playbooks (Ch 17–20) | ~14,000 |
| Epilogue | ~2,500 |
| Appendices A–D | ~8,000 |
| **Total** | **~84,700** |

---

## File Structure

```
C:\Projects\the-inverted-stack\
├── source\                        ← gitignored — raw source papers
│   ├── local_node_saas_v13.md
│   ├── inverted-stack-v5.md
│   ├── kleppmann_council_review.md
│   └── kleppmann_council_review2.md
├── prospectus\
│   └── prospectus.md
├── ASSEMBLY.md
├── chapters\
│   ├── front-matter\
│   │   ├── foreword-placeholder.md
│   │   └── preface.md
│   ├── part-1-thesis-and-pain\
│   │   ├── ch01-when-saas-fights-reality.md
│   │   ├── ch02-local-first-serious-stack.md
│   │   ├── ch03-inverted-stack-one-diagram.md
│   │   └── ch04-choosing-your-architecture.md
│   ├── part-2-council-reads-the-paper\
│   │   ├── ch05-enterprise-lens.md
│   │   ├── ch06-distributed-systems-lens.md
│   │   ├── ch07-security-lens.md
│   │   ├── ch08-product-economic-lens.md
│   │   ├── ch09-local-first-practitioner-lens.md
│   │   └── ch10-synthesis.md
│   ├── part-3-reference-architecture\
│   │   ├── ch11-node-architecture.md
│   │   ├── ch12-crdt-engine-data-layer.md
│   │   ├── ch13-schema-migration-evolution.md
│   │   ├── ch14-sync-daemon-protocol.md
│   │   ├── ch15-security-architecture.md
│   │   └── ch16-persistence-beyond-the-node.md
│   ├── part-4-implementation-playbooks\
│   │   ├── ch17-building-first-node.md
│   │   ├── ch18-migrating-existing-saas.md
│   │   ├── ch19-shipping-to-enterprise.md
│   │   └── ch20-ux-sync-conflict.md
│   ├── epilogue\
│   │   └── epilogue-what-the-stack-owes-you.md
│   └── appendices\
│       ├── appendix-a-sync-daemon-wire-protocol.md
│       ├── appendix-b-threat-model-worksheets.md
│       ├── appendix-c-further-reading.md
│       ├── appendix-d-testing-the-inverted-stack.md
│       └── appendix-e-citation-style.md
```

---

## Writing Discipline Rules

1. **Part III is specification; Part IV is tutorial.** Part III tells you what each component
   is and how it works in full. Part IV shows the minimal path to a working implementation.
   Part IV references Part III — it does not rewrite it in tutorial voice.

2. **Ch 2 is opinionated, not encyclopedic.** One paragraph per existing approach; for each:
   what it does, exactly where it stops short. Ends with a crisp statement of what this book adds.

3. **Council chapters have two acts.** Round 1: objections, blocking issues, what failed.
   The narrative gap between rounds. Round 2: what changed, verdict, takeaway principle.

4. **Sunfish references by package name, not class API.** Pre-1.0; APIs evolve. Architectural
   patterns and package names are stable enough to cite. Specific method signatures are not.

5. **No re-introducing the architecture.** Each chapter assumes the reader has read Part I.
   No "as we established earlier, the local node is primary." Trust the structure.
