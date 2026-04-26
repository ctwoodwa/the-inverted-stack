# Sunfish Business MVP Plan

**Status:** Execution plan for a separate Claude Code session focused on business-application MVP. Not implementation; not yet validated against working code.

**Audience:** Future Claude session (and human reviewer) executing the build of Anchor + Bridge business modules.

**Source decisions:** This plan synthesizes lessons from production OSS reference implementations (Actual Budget, Frappe Books, GnuCash, Beancount/Fava) and applies the architectural primitives from `concept-index.yaml` (562 concepts) + `design-decisions.md` (48 architectural primitives across 5 volumes).

---

## §1. Vision and scope

### What we're building

**The Sunfish Business Suite** — an integrated local-first SMB (small/medium business) operations suite covering four interlocking modules:

- **Accounts** — double-entry accounting (chart of accounts, journal entries, bank reconciliation, P&L + balance sheet + cash flow, multi-currency, tax handling, invoicing)
- **Vendors** — vendor master, AP workflow (PO → receipt → bill → payment), vendor catalog, 1099/W-9 reporting
- **Inventory** — item master, multi-location stock, stock movements, cost methods (FIFO/LIFO/avg), serial/lot/batch tracking
- **Projects** — project hierarchy, time tracking, resource allocation, kanban + gantt + list views, file attachments, project-cost rollup to accounts

### What makes this different from existing OSS

| Existing OSS | Limitation we address |
|---|---|
| **QuickBooks / Xero** | Cloud-locked; vendor controls your data; subscription required; no offline |
| **Actual Budget** | Personal finance only; not SMB; no inventory/vendors/projects |
| **GnuCash** | Single-device; no real multi-device sync; no collab; no inventory/vendors/projects |
| **Frappe Books** | Cloud-based by default; not local-first by design |
| **ERPNext / Odoo** | Massive complexity; cloud-first; over-featured for SMB |
| **Specialized tools** (OpenProject, Snipe-IT, EspoCRM) | No integration; need to glue together; multiple cloud subscriptions |

**Sunfish Business Suite differentiators:**

1. **Integrated SMB suite** — accounts + vendors + inventory + projects in one app
2. **Local-first by design** — owner controls data; no vendor lock-in
3. **Multi-device collab without forcing cloud** — LAN sync between Anchor instances
4. **Optional cloud bridge for off-site access** — Bridge for mobile / remote workers / off-site backup
5. **Open formats / no lock-in** — plain-file export per module (CSV / JSON / Markdown / OFX)
6. **Privacy-first** — financial + customer data stays on user-controlled infrastructure
7. **Sanctions-resilient** — works in jurisdictions where US/EU SaaS is unavailable (per book Ch01 vendor-disappearance failure mode + Ch08 sanctions-grade availability)

### Target customer profile

- **Size**: 1-50 employees
- **Industries**: services (consulting, agencies, design, dev shops), retail (single + multi-location), trades (construction, contractors), professional services (law, accounting, healthcare), light manufacturing
- **Pain point**: tired of vendor lock-in, subscription creep, data residency concerns, "what happens to our books if QuickBooks deletes our account?"
- **Tech sophistication**: low to medium — owner is not a developer; needs UI as good as cloud SaaS competitors
- **Network reality**: usually has internet but not always; needs to keep working during outages; some have intermittent / metered connectivity

### MVP success criteria

The MVP is shippable when:

1. A real small business can run their entire operations on it for 90 consecutive days
2. The deployment passes `local-first-properties` skill scan with ≥80% conformance across P1-P7
3. The deployment passes `inverted-stack-conformance` skill scan with ≥60% across the full 562-concept catalog
4. Three reference deployments demonstrated: restaurant POS scenario, construction-company project scenario, small-consultancy scenario
5. End-to-end demo video showing offline operation, multi-device sync, conflict resolution, recovery from device loss
6. Conformance baseline reports committed to Sunfish's `icm/01_discovery/output/`

---

## §2. OSS lessons synthesis

### Actual Budget — local-first sync architecture validated

**What they prove:** The Anchor + Bridge architecture (client + optional sync server) works at production scale for personal finance. CRDTs for accounting data are mature. Open-source sync server with self-hostable option is viable.

**What we adopt:**
- Client + optional sync-server architecture (= Anchor + Bridge)
- CRDT-based concurrent editing of financial records
- Self-hosted vs. provider-hosted Bridge as user choice
- Open-source with paid-hosting business model viability

**What we extend beyond Actual Budget:**
- SMB scope (vs. personal finance only)
- Inventory + vendors + projects in addition to accounts
- Multi-tenant Bridge (vs. one-user-many-devices only)
- Per-resource ACL within tenant (vs. owner-only)

**Repo:** [github.com/actualbudget/actual-server](https://github.com/actualbudget/actual-server) — read for sync-server reference implementation patterns.

### Frappe Books — desktop accounting feature surface

**What they prove:** Electron + SQLite desktop accounting works for SMB. Double-entry + invoicing + inventory + POS is the right feature surface for the segment. Multi-currency + tax handling is solvable.

**What we adopt:**
- Desktop-first Electron-equivalent (Sunfish uses .NET MAUI per book Ch12; could also evaluate Tauri for cross-platform)
- SQLite as local store
- Double-entry semantic foundation
- Built-in invoice template builder
- Multi-currency from day one
- Tax handling per jurisdiction (state, GST/VAT)

**What we improve:**
- Multi-device sync (Frappe Books is single-device; we add CRDT sync between Anchor instances)
- Encrypted at rest (SQLCipher, per book Ch15)
- Optional Bridge relay (Frappe Books has no off-site sync option without cloud)
- Plain-file export (Frappe Books is SQLite-only)
- Plugin architecture (each module as plugin per book Ch11 NODE-* concepts)

**Repo:** [github.com/frappe/books](https://github.com/frappe/books) — read for SMB accounting feature surface + UI patterns.

### GnuCash — mature double-entry semantic foundation

**What they prove:** Double-entry accounting model has been stable for 25+ years. The 5-account-type taxonomy (asset, liability, equity, income, expense) is durable. Reconciliation workflow patterns are well-understood. Account hierarchy is the right organizing concept.

**What we adopt:**
- 5-account-type taxonomy
- Account hierarchy (parent + children)
- Transaction = source + destination accounts (matches book Ch12 ledger CRDT-23 concept)
- Reconciliation workflow against bank statements
- Multi-currency with currency-conversion dates
- Imported transaction matching

**What we improve:**
- Modern UI (GnuCash GTK is dated)
- Real multi-device support (GnuCash file format isn't sync-friendly)
- Plain-text export beyond GnuCash XML (CSV + Markdown + Beancount-compatible)
- Web-mobile companion (GnuCash desktop-only)

**Repo:** [github.com/Gnucash/gnucash](https://github.com/Gnucash/gnucash) — read for data model + transaction semantics.

### Beancount / Fava / Plain Text Accounting — long-now archival format

**What they prove:** Plain-text accounting in deterministic format outlives any specific software. Fava's web interface proves you can have rich reports against plain-text source. Plugin architecture allows extension without forking.

**What we adopt:**
- Beancount-compatible plain-text export (P5 long-now archival format — matches book Ch16 DUR-25 plain-file export)
- Account hierarchy with `:` separators (Beancount convention: `Assets:Bank:Checking`)
- Metadata on transactions (tags, links, document attachments)
- Plugin architecture for custom rules / imports / reports

**What we improve beyond Beancount:**
- GUI as primary interface (Beancount is CLI-first; we make plain-text export, not edit, as primary)
- Multi-device sync (Beancount files in Git is the current pattern; CRDTs are better)
- SMB feature surface (vendors / inventory / projects beyond accounting alone)

**Repo:** [github.com/beancount/beancount](https://github.com/beancount/beancount) — read for plain-text format spec; use as P5 export format.

### Other OSS to mine per module

#### Project / tasks / Gantt

- **Plane** ([github.com/makeplane/plane](https://github.com/makeplane/plane), AGPL-3.0) — modern Jira/Linear/ClickUp alternative; Gateway + Pilot microservices architecture; native MCP server + agent framework + @mention support; cycles, modules, work items, dashboards, estimates, REST API + webhooks; Docker-deployable in <10 min with 2 CPU + 4GB RAM. **Most relevant for Projects module**: modern UI patterns + MCP integration vector. **Note:** Plane is server-architected (not local-first); we adopt UI patterns + MCP server idea, not the architecture.
- **OpenProject** ([github.com/opf/openproject](https://github.com/opf/openproject)) — mature project mgmt feature surface; Gantt + Kanban + meetings + work-breakdown
- **Taiga** ([github.com/taigaio/taiga-back](https://github.com/taigaio/taiga-back)) — agile project mgmt; story-driven; well-designed sprint flow
- **Redmine** ([github.com/redmine/redmine](https://github.com/redmine/redmine)) — issue tracking + project mgmt; Ruby on Rails; very mature plugin ecosystem
- **Wekan** ([github.com/wekan/wekan](https://github.com/wekan/wekan)) — open-source kanban; Trello-style UX

#### Inventory / parts

- **InvenTree** ([github.com/inventree/InvenTree](https://github.com/inventree/InvenTree)) — Python/Django; **strong parts management** with hierarchical categorization; supplier-linked parts; **Bill of Materials (BOM)** with intelligent management; **Build management** (track builds consuming stock to make new parts — this is light manufacturing); REST API + Python binding library; plugin system. Particularly strong for hardware / electronics / light manufacturing SMBs. **Most relevant for Inventory module**: BOM + build mgmt patterns (post-MVP but architecture must not preclude); parts categorization + supplier-linked patterns.
- **ERPNext** ([github.com/frappe/erpnext](https://github.com/frappe/erpnext)) — full Frappe-stack ERP; modular; inventory + accounting + manufacturing tightly integrated
- **Odoo Inventory** (part of Odoo Community, see below) — barcode scanning, batch tracking, real-time valuation
- **Snipe-IT** ([github.com/snipe/snipe-it](https://github.com/snipe/snipe-it)) — IT asset management; checkout/checkin model; asset depreciation tracking. **Most relevant for asset-heavy SMBs** that need to track equipment.

#### Invoicing / billing

- **Invoice Ninja** ([github.com/invoiceninja/invoiceninja](https://github.com/invoiceninja/invoiceninja), Laravel + Flutter + React) — invoicing, billing, payment management; recurring billing; quote/proposal management; expense tracking; **built-in time tracking** (overlap with project mgmt — interesting integration model); source-available license (not pure OSS — note for licensing strategy). **Most relevant for Accounts module**: invoice template + recurring billing patterns.
- **Akaunting** ([github.com/akaunting/akaunting](https://github.com/akaunting/akaunting), Laravel + Vue) — online accounting for small business; **multi-company support from one admin panel** (relevant for SMBs with multiple legal entities); multi-currency + tax rules + client portals; **app marketplace concept** (similar to Sunfish plugin architecture per book Ch11). Limitation: free version is single-user. **Most relevant for Accounts module**: multi-company architecture + plugin marketplace patterns.

#### Full ERP (all domains)

- **ERPNext** — see above; comprehensive Frappe-based ERP
- **Odoo Community** ([odoo.com](https://www.odoo.com/)) — Python + PostgreSQL; **modular ERP architecture is the selling point**; CRM + Sales + Accounting + Inventory + Project + Manufacturing modules; OCA (Odoo Community Association) extends with additional modules; no per-user/per-app fee. **Most relevant for the overall MVP architecture**: validates modular ERP pattern that maps directly to Sunfish's kernel-plugin architecture (book Ch11). Specifically: Odoo Community accounting + inventory + project + CRM = exactly the MVP module set.
- **EspoCRM** ([github.com/espocrm/espocrm](https://github.com/espocrm/espocrm)) — vendor/customer relationship mgmt patterns; lighter-weight than Salesforce-class
- **Tryton** ([github.com/tryton/tryton](https://github.com/tryton/tryton)) — modular business application platform; module separation patterns

### Local-first project landscape (production references for the architecture, not the features)

The OSS surveyed above (§2 above) shows the FEATURE SURFACE for SMB business apps. This section surveys the LOCAL-FIRST PROJECT LANDSCAPE — what proves the architectural patterns we're building on. Less about "what features do we need" and more about "who has built local-first at production scale and what did they learn."

#### Production local-first apps (validate the user-facing patterns)

| Project | Domain | Sync model | Lesson for MVP |
|---|---|---|---|
| **Logseq** ([github.com/logseq/logseq](https://github.com/logseq/logseq), AGPL) | Knowledge graph / note-taking | Syncthing OR Git OR self-hosted | **Sync via existing tools is viable** — users can BYO sync (Syncthing, Git remote, NAS); doesn't have to mean "use our cloud." Outliner-first UX style. Markdown files on disk = perfect P5 long-now |
| **Obsidian** ([obsidian.md](https://obsidian.md/), proprietary client / open file format) | Knowledge graph / note-taking | Optional paid sync OR free P2P (Syncthing, iCloud Drive, etc.) | **Plugin ecosystem is the moat** — 1000+ community plugins keep users locked-in to Obsidian *because* of community value, not because of vendor lock-in. Plain markdown files mean users can leave anytime. Sunfish should plan for plugins from day one (book Ch11 already does) |
| **Anytype** ([anytype.io](https://anytype.io/), AGPL) | Knowledge management with structured objects | True P2P + optional self-hosted sync nodes | **P2P-first is feasible at scale** — proves CRDT-based multi-device sync without central server is production-ready. Object-based model (vs. file-based) for richer relations |
| **Joplin** ([joplinapp.org](https://joplinapp.org/), MIT) | Note-taking with sync | Dropbox / OneDrive / Joplin Cloud / WebDAV / S3 | **Sync via off-the-shelf services** — uses general-purpose cloud storage as transport instead of building bespoke relay. Optional E2EE on top. Useful pattern for users who already pay for Dropbox |
| **Standard Notes** ([standardnotes.com](https://standardnotes.com/), AGPL) | Encrypted notes | E2EE with sync server (self-hostable) | **Zero-knowledge sync at scale works** — proves the Bridge pattern (relay holds only ciphertext, can never decrypt) is viable for production users. Validates Sunfish's relay model |
| **Reflect** ([reflect.app](https://reflect.app/), proprietary) | Notes with backlinks | E2EE iCloud Drive sync | **Apple-ecosystem local-first** — uses iCloud as the sync layer; data lives on user devices. Useful pattern for Anchor's macOS/iOS variant |
| **Heynote** ([heynote.com](https://heynote.com/), MIT) | Scratchpad / quick notes | Local file with optional cloud sync | **Minimal local-first works** — proves you don't need full CRDT machinery for many use cases; sometimes just "save to a local file with smart conflict resolution" is enough |
| **Actual Budget** (already covered in §2) | Personal finance | Optional self-hosted sync server | Validates the Anchor + Bridge architecture for financial data at production scale |

**Key lesson cluster:** local-first apps that have achieved real adoption (Logseq, Obsidian, Anytype, Joplin) all share three patterns: (1) plain-file or open-format storage so users CAN leave; (2) sync as a feature, not the value proposition (the value is the app, not the cloud); (3) plugin/extension ecosystem to lock users in via community value rather than vendor capture. Sunfish should adopt all three.

#### Local-first sync engines (validate the technical infrastructure)

These are the building blocks Sunfish would compete with OR build on. Important distinction (per Aaron Boodman, Replicache): server-authority engines vs. decentralized engines.

| Engine | License | Architecture pattern | Lesson for MVP |
|---|---|---|---|
| **Replicache** ([replicache.dev](https://replicache.dev/), source-available) | Source-available + commercial | Server-authority sync framework; client-side datastore | Mature production-grade sync framework; pattern for client-side mutator + server-side validation. Authority pattern is server-side (vs. CRDT decentralized) |
| **PowerSync** ([powersync.com](https://www.powersync.com/), Apache 2.0 client / commercial cloud) | Apache 2.0 client / commercial server | Server-authority; SQLite client + Postgres backend; bidirectional sync via persistent upload queue | **Strong fit for "I have a Postgres backend, want to add local-first to my app"** — relevant for SMBs migrating from cloud-only to local-first |
| **ElectricSQL** ([electric-sql.com](https://electric-sql.com/), Apache 2.0) | Apache 2.0 | "Durable Sync" layer for Postgres; replication streams push to clients; strong schema consistency | Different sync philosophy than Sunfish's CRDT approach — Postgres-anchored. Useful comparison for "why CRDTs over replication-based sync" decision rationale |
| **InstantDB** ([instantdb.com](https://instantdb.com/), MIT client / commercial cloud) | MIT client / commercial cloud | Server-authority; "spiritual successor to Firebase for relational era"; offline + permissions out of box | Validates relational + real-time + offline triad. Sunfish's Bridge could expose similar query primitives over the local CRDT data |
| **Triplit** ([triplit.dev](https://triplit.dev/), now community OSS) | OSS (was commercial; folded Jan 2026) | Server-authority; full-stack local-first DB | **Cautionary tale**: commercial local-first sync engine couldn't sustain as company; folded to community OSS in early 2026. **Implication**: Sunfish's open-source-from-day-one position is more durable than commercial-from-day-one. The Bridge's value-as-managed-service rather than value-as-product is a defensible business model |
| **Jazz** ([jazz.tools](https://jazz.tools/), MIT) | MIT | CRDT-based with collaborative state primitives | Newer entrant; CRDT-decentralized; useful comparison for "what does a modern Yjs alternative look like" |
| **Automerge** ([automerge.org](https://automerge.org/), MIT) | MIT | Decentralized CRDT engine | One of the canonical CRDT engines; rust-based with JS bindings; competing pattern to Yjs/YDotNet |
| **Yjs** ([github.com/yjs/yjs](https://github.com/yjs/yjs), MIT) | MIT | Decentralized CRDT engine | Most-deployed CRDT engine in production (powers Notion AI, Linear, etc.); Y-Sweet by Jamsocket adds managed sync. **YDotNet is .NET port — Sunfish's current choice per book Ch12** |
| **Loro** ([loro.dev](https://loro.dev/), MIT) | MIT | Modern Rust CRDT engine | **Sunfish's stated future target** per book Ch12; faster than Yjs for large documents; pluggable into Sunfish's `ICrdtEngine` adapter |

**Key lesson cluster:** the sync-engine landscape divides cleanly into **server-authority** (Replicache, Zero, PowerSync, ElectricSQL, InstantDB, Convex, Triplit, Firebase) and **decentralized** (Yjs, Automerge, Loro). Sunfish chose decentralized (CRDT-based) per book Ch12 because it cleanly satisfies P3 (network optional) and P7 (ownership) — server-authority engines fundamentally require the server to be reachable for write authorization. Sunfish's Bridge is server-authority FOR ROUTING (relay) but data ownership stays decentralized at the peer level. This is a meaningful architectural choice worth documenting.

**Triplit-as-cautionary-tale** is important: a VC-backed local-first sync company with a strong team folded its commercial business in early 2026 and re-released as community OSS. The local-first space is full of similar attempts. Sunfish's positioning — open-source-from-day-one with Bridge-as-managed-service business model — is structurally more durable than competing as a closed-source local-first sync engine.

#### Local-first research projects (validate emerging patterns)

These are research lab projects, not production apps, but they prove patterns the book directly references:

| Project | Lab | What it proves | Book reference |
|---|---|---|---|
| **Patchwork** ([inkandswitch.com/patchwork](https://www.inkandswitch.com/patchwork/notebook/01/)) | Ink & Switch | Universal version control for collaborative documents; malleable substrate for in-the-moment toolmaking | Validates richer-than-Git version control on top of CRDTs; relevant for project documentation in Module 4 |
| **PushPin** ([github.com/inkandswitch/pushpin](https://github.com/inkandswitch/pushpin)) | Ink & Switch | Mixed-media canvas (Miro/Milanote-style) on Automerge; presence avatars; collab without server | Most fully-realized Automerge-based app; validates rich UI on CRDT substrate |
| **Cambria** ([inkandswitch.com/cambria](https://www.inkandswitch.com/cambria/)) | Ink & Switch | Schema evolution via bidirectional translation lenses for cross-version collaboration | **Directly referenced in book Ch13 (SCH-12)**. Sunfish's schema migration uses this pattern. Cambria is the canonical implementation |
| **Hypermerge** | Ink & Switch | Peer-to-peer Automerge document store with hypercore | Validates fully-decentralized CRDT distribution without any server; predecessor to today's Y-Sweet patterns |
| **Local-First Conf 2026** ([localfirstconf.com](https://localfirstconf.com/)) | Community | Annual gathering of local-first builders | Worth attending or watching talks; community for surfacing new patterns |

#### Local-first-adjacent commercial validators

Not local-first by strict definition, but validate that "feels like local" + "works offline" + "real-time collaborative" is a winning product strategy:

| Product | What they validate |
|---|---|
| **Linear** ([linear.app](https://linear.app/)) | "Local-feeling" speed at cloud scale (CRDT under the hood); proves users will pay premium for sub-frame responsiveness |
| **Notion** | Offline mode for an otherwise-cloud-native tool; users do expect offline when traveling |
| **Figma** | Real-time multi-user collab on rich documents (CRDT-based; Y-Sweet uses similar tech); proves multi-cursor + presence is table-stakes for collab tools |
| **Zed** ([zed.dev](https://zed.dev/), GPL) | Collaborative text editor with sub-frame latency; native MCP support; integrates with Linear and Figma via MCP. Validates **MCP-native local-first apps as a category** |

**Key lesson cluster:** even commercial cloud-first products (Linear, Notion, Figma) have moved toward CRDT-backed sync because users expect local-first responsiveness AND multi-user collaboration. The competitive bar Sunfish must clear is "as fast as Linear, as collaborative as Figma, but with user-controlled data." Zed's pattern of "MCP-native + collaborative + fast" is the strongest contemporary archetype.

### Synthesis: which OSS contributes what to MVP

| Module | Primary references | Specific patterns to adopt |
|---|---|---|
| **Accounts** | GnuCash + Beancount + Akaunting + Invoice Ninja + Odoo Community | Double-entry semantics (GnuCash); plain-text export (Beancount); multi-company (Akaunting); recurring billing + invoice templates (Invoice Ninja); modular accounting (Odoo) |
| **Vendors** | Frappe Books + ERPNext + EspoCRM + Odoo Community | Vendor master + PO workflow (ERPNext); contact mgmt (EspoCRM); three-way match (Odoo Community); 1099/W-9 (Frappe Books US-specific) |
| **Inventory** | InvenTree + Frappe Books + Odoo Inventory + Snipe-IT | Parts categorization + supplier-linked (InvenTree); BOM (InvenTree, post-MVP); barcode scanning (Odoo Inventory); asset depreciation (Snipe-IT, post-MVP) |
| **Projects** | Plane + OpenProject + Taiga + Wekan + Invoice Ninja | Modern UI + MCP integration (Plane); Gantt + work breakdown (OpenProject); agile/sprint flow (Taiga); kanban (Wekan); time tracking + project billing (Invoice Ninja) |
| **Architecture** | Actual Budget + Odoo Community + Frappe Books | Sync server pattern (Actual Budget); modular kernel+plugin (Odoo Community); SQLite + Electron-equivalent (Frappe Books) |

---

## §3. Architecture decisions

### Notable architecture insights from OSS research

Two patterns from the broader OSS landscape are worth surfacing because they suggest non-obvious architectural directions:

**1. Plane's native MCP server** — Plane ships with a Model Context Protocol (MCP) server built in, allowing AI agents to interact with project management primitives natively (`@mention` agents in tasks, agent-driven task creation, full agent-run lifecycle tracking). This is the SAME MCP we use in Claude Code. **Implication for Sunfish**: each module (accounts / vendors / inventory / projects) should ship with a native MCP server exposing its primitives. This makes Sunfish AI-agent-friendly from day one — agents can query inventory, post journal entries, update project status — without bolting on AI features later. Local-first MCP is interesting because the AI agent runs against the user's local Anchor with the user's keys, not against a vendor's cloud.

**2. Odoo Community's modular architecture** — Odoo's modules are independently installable + upgradable + removable, with a published API contract between modules. This maps directly to Sunfish's kernel + plugin architecture (book Ch11 NODE-* concepts). **Implication for Sunfish**: each MVP module (accounts / vendors / inventory / projects) ships as a separate Sunfish plugin, with the kernel orchestrating them. Users can install only the modules they need. Third parties can write additional modules using the same plugin contract. This is also how the OCA (Odoo Community Association) extends Odoo's surface — community-contributed modules outside the core team.

These two patterns together suggest a mature plugin-plus-MCP architecture where each plugin is independently AI-agent-accessible. This is a meaningful differentiator from cloud SaaS competitors who typically bolt MCP on at the API layer (and require their cloud to mediate).

### Tech stack (rationale + alternatives)

| Layer | Choice | Rationale | Alternative considered |
|---|---|---|---|
| **Anchor app shell** | .NET MAUI | Per book Ch12 reference (.NET ecosystem); cross-platform Win/Mac/Linux; integrates with Sunfish package layout | Tauri (Rust + web UI) — more web-native but doesn't match book's .NET orientation |
| **Anchor local store** | SQLite + SQLCipher | Per book Ch15 encrypted-at-rest; matches Frappe Books, Actual Budget, GnuCash patterns; mature; battle-tested | LiteDB / RocksDB / DuckDB — less mature for application data |
| **CRDT engine** | YDotNet (today) → Loro (target) | Per book Ch12 CRDT-10 engine adapter; existing in Sunfish reference | Automerge (different language); custom implementation (too risky) |
| **Bridge service** | ASP.NET Core 9+ | Consistent with .NET ecosystem; battle-tested; native to Sunfish package layout | Node.js (mismatched stack); Go (ditto) |
| **Bridge storage** | PostgreSQL + Redis | Standard for ASP.NET multi-tenant; well-understood scale-out patterns | SQLite-only (won't scale to multi-tenant); MongoDB (overkill) |
| **Wire protocol** | Per Appendix A (CBOR over Noise_XX over UDS / TCP) | Already specified in book; reuse | gRPC (added complexity; Noise gives security primitives directly) |
| **UI components** | Sunfish.UiBlocks | Per other concurrent session's work | Build per-app — wasteful |
| **i18n / l10n** | Per other concurrent session's framework | Per concurrent session | Build per-module — wasteful |
| **Plain-text export** | Beancount-compatible for accounts; CSV for inventory; Markdown for project docs; JSON for raw data | Per book Ch16 DUR-25 plain-file export + #37 long-horizon format | Custom XML — won't outlive software |
| **MCP server per module** | Native MCP server in each plugin exposing module primitives | Per Plane's pattern; makes each module AI-agent-accessible without bolting on AI later; runs locally against user keys | Bolt-on AI integration at API layer — cedes control to vendor |

### Architectural primitives applied

This MVP exercises virtually every primitive in the current book + most v1.1 extensions:

| Primitive | Applied where |
|---|---|
| #1 CRDT data plane | All record types (journal entries, items, vendors, projects, tasks) |
| #2 Sync protocol | Anchor↔Anchor (LAN) + Anchor↔Bridge (off-site) |
| #3 Key custody | Per-user identity keys; per-tenant data keys; per-record DEK |
| #4 Zero-knowledge relay | Bridge holds only ciphertext; cannot read business data |
| #5 Multi-tenant isolation | Bridge supports multiple SMBs; strict per-tenant data boundaries |
| #6 Schema evolution | Module schemas evolve over years; per book Ch13 |
| #7 Plain-file export | Per module: Beancount for accounts; CSV for inventory; Markdown for projects |
| #8 Threat-model worksheets | Per module + per actor (SMB owner, employee, departing employee, regulator, attacker) |
| #11 Fleet management | Multi-device per business (owner laptop + manager tablet + warehouse phone + mobile sales) |
| #34 Compliance posture | Per-deployment manifest declaring tax/regulatory obligations (state-by-state in US; GST/VAT internationally) |
| #43 Performance contracts | All read/write operations <16ms; reports <500ms; sync <30s after reconnect |
| #44 Per-data-class device-distribution | Owner laptop holds full data; warehouse phone holds inventory-only; mobile sales holds CRM-only |
| #45 Collaborator revocation | Departing employee removal; owner can revoke per-resource access |
| #46 Forward secrecy | Sync sessions use ephemeral keys; past sync stays safe after current key compromise |
| #47 Endpoint-compromise threat model | Honest documentation of what stays protected if owner's laptop is stolen with active session |
| #48 Key-loss recovery | Multi-sig social recovery for owner; institutional custodian for accountant-of-record |

---

## §4. Module 1 — Accounts

### Feature scope

Drawing from GnuCash (double-entry foundation) + Beancount (plain-text export format) + Frappe Books (SMB UI patterns) + Akaunting (multi-company) + Invoice Ninja (recurring billing + invoice templates) + Odoo Community (modular accounting):

**Chart of accounts**
- 5-type hierarchy (Asset / Liability / Equity / Income / Expense)
- Standard SMB template + per-business customization
- Account = (id, name, type, parent, currency, opening-balance)
- Hierarchical naming convention (Beancount-style: `Assets:Bank:Checking`)

**Journal entries / transactions**
- Double-entry: every transaction has debits = credits across N≥2 accounts
- Transaction = (date, description, splits[], tags[], linked-document-uri)
- Multi-currency with conversion rates at transaction date
- Recurring transactions (rent, payroll, subscriptions)
- Per book Ch12 CRDT-23: ledger is the canonical CP-class CRDT example

**Reconciliation**
- Import bank statements (OFX, QFX, CSV)
- Match imported transactions against journal entries
- Mark reconciled (supports rolled-up monthly close)
- Bank balance vs. book balance reports

**Reports**
- P&L (Income Statement) — current period, prior period, YoY
- Balance Sheet — current + comparative
- Cash Flow Statement — direct + indirect methods
- AR Aging (Customer Aging) — outstanding receivables by age bucket
- AP Aging (Vendor Aging) — outstanding payables by age bucket
- Trial Balance — all accounts current
- General Ledger — full transaction history per account

**Invoicing**
- Sales invoices → AR
- Customer master (id, name, contact, payment terms, default tax)
- Invoice line items (item-or-description, qty, unit-price, tax)
- PDF generation via template builder (Frappe Books pattern)
- Email + print + save-to-disk
- Payment recording (matches against AR)

**Tax handling**
- Per-jurisdiction tax rates (US state-by-state sales tax; GST/VAT/HST internationally)
- Tax-on-tax handling
- Tax periods + filing reports

### Local-first compliance per Kleppmann property

| Property | How |
|---|---|
| **P1 No spinners** | All journal-entry writes commit to local SQLite in <16ms; report computation runs in background worker; main thread never blocks |
| **P2 Multi-device** | Owner's laptop + accountant's laptop sync via LAN or Bridge; per-data-class policy: full data on accountant + owner devices; mobile sales sees only customer-facing AR balances |
| **P3 Network optional** | All accounting workflows complete offline (record sale, generate invoice, mark payment); sync queues delta; reconciliation can proceed against locally-cached bank import |
| **P4 Collaboration** | Owner + bookkeeper + accountant edit concurrently; CRDT merges per-account journal entries; period-close uses Flease quorum to prevent backdating after close |
| **P5 Long now** | Beancount-compatible export of all journal data; account templates and chart of accounts in plain text; tax rate tables exported with effective-date metadata |
| **P6 Security** | All data encrypted at SQLCipher rest; sync via zero-knowledge Bridge (Bridge sees only ciphertext); per-user identity via Ed25519; tax-sensitive data classified `private` |
| **P7 Ownership** | Owner can export full chart of accounts + journal in Beancount text at any time; can revoke accountant's access; can crypto-shred customer PII per GDPR right-to-erasure |

### CRDT semantics per record type

- **Account** (in chart): LWW-Map (last-write-wins for name/type/parent/etc.) — schema-stable
- **Journal entry**: append-only log with Flease-protected period-close lease — once closed, entries within period are immutable
- **Customer / vendor master**: LWW-Map with delete-tombstones
- **Item master** (shared with inventory): LWW-Map
- **Tax rate table**: append-only with effective-date version

### Specific failed-conditions to test

- Period-close with Flease lease prevents backdated journal entry → CONCEPT FAILS if backdated entry succeeds
- Bank-import deduplication prevents same bank statement being applied twice → CONCEPT FAILS if duplicate entry survives
- Multi-currency report computes correct conversion → CONCEPT FAILS if conversion uses wrong rate or rounding error >0.01
- Reconciliation marker survives sync between devices → CONCEPT FAILS if reconciled status diverges across peers

---

## §5. Module 2 — Vendors

### Feature scope

Drawing from Frappe Books (SMB AP workflow) + ERPNext (full P2P cycle) + EspoCRM (contact management) + Odoo Community (vendor module + three-way match):

**Vendor master**
- Vendor = (id, name, contacts[], addresses[], payment-terms, default-currency, tax-treatment, 1099-W9-status)
- Vendor catalog (vendor-supplied items + agreed prices + lead times)
- Vendor performance metrics (on-time delivery %, price stability, dispute rate)

**Purchase order workflow**
- PO = (vendor-id, requestor, line-items[], expected-delivery, terms, status)
- Status lifecycle: draft → approved → sent → partial-received → received → closed
- Approval workflow (configurable thresholds; small POs auto-approve; large POs require manager approval)
- Receipt against PO (record actual quantities / dates / damage notes)
- Three-way match: PO ↔ receipt ↔ vendor bill

**Vendor bills (AP)**
- Bill = (vendor-id, bill-number, date, due-date, line-items[] — link to PO line if applicable, total, status)
- Status lifecycle: draft → entered → approved → scheduled → paid
- Payment scheduling (per due date + cash-flow optimization)
- 1099 / W-9 data accumulation per vendor

**Reports**
- Vendor list with status + balance
- AP Aging (also in accounts module — same data, different view)
- PO outstanding (placed but not yet received)
- 1099 prep report (US-specific)
- Vendor performance scorecard

### Local-first compliance per Kleppmann property

| Property | How |
|---|---|
| **P1** | PO entry / approval / status change all <16ms locally |
| **P2** | Buyer + receiver + AP clerk sync vendors + POs; mobile receiver records receipts on phone |
| **P3** | Receiving in warehouse with no signal — receipt goes into local CRDT; syncs when signal returns |
| **P4** | Buyer creates PO; receiver records partial receipt; AP enters bill; all converge on PO #N record |
| **P5** | Vendor master + PO history exportable as CSV + JSON |
| **P6** | Vendor banking info (for ACH payments) classified `private` — encrypted at rest with separate KEK |
| **P7** | Owner can export entire vendor master + AP history; can revoke AP clerk's access; can crypto-shred former vendor's PII per data retention policy |

### CRDT semantics

- **Vendor master**: LWW-Map with delete-tombstones
- **Purchase order**: structured CRDT with per-line-item LWW-Map; Flease-protected close (once closed, no edits)
- **Bill / AP entry**: links to PO (immutable reference); itself is LWW-Map until paid

### Specific failed-conditions to test

- Approval threshold enforced regardless of which device approves → FAILS if device with stale settings allows over-threshold approval
- Three-way match catches discrepancy between PO + receipt + bill → FAILS if mismatch goes undetected
- Closed PO cannot be edited → FAILS if late edit succeeds
- Vendor banking info encrypted with separate key → FAILS if found in plaintext anywhere

---

## §6. Module 3 — Inventory

### Feature scope

Drawing from InvenTree (parts categorization + supplier-linked + BOM patterns) + Frappe Books (SMB inventory UI) + Odoo Inventory (barcode + batch tracking + real-time valuation) + Snipe-IT (asset checkout/checkin patterns):

**Item master**
- Item = (sku, name, description, unit-of-measure, default-cost, default-price, tax-class, item-class)
- Categories / hierarchy
- Variants (size / color / configuration)
- Linked vendor catalog entries (which vendors supply this item at what price)

**Stock levels**
- Per-location stock (warehouse, store, vehicle)
- Real-time current quantity + cost
- Reserved (allocated to open sales orders)
- Available = Current − Reserved
- Reorder point + economic order quantity per item per location

**Stock movements**
- Movement types: receipt (from PO), issue (to sale), transfer (between locations), adjustment (audit / damage / write-off)
- Each movement = (date, item-id, location-id, qty, cost, reference-doc, reason)
- Append-only log; stock-level views are projections

**Cost methods**
- FIFO, LIFO, weighted-average per item
- Per-period cost roll-up (monthly close affects COGS)
- Inventory valuation report

**Serial / lot / batch tracking**
- Serial-tracked items: each unit has serial number; movements tied to specific serial
- Lot-tracked items: bulk lots with lot-number; can recall by lot
- Batch-tracked items: batches with expiration date; FIFO-by-expiration

**Reports**
- Stock levels (current quantity per item per location)
- Stock movements (chronological by item or location)
- Inventory valuation (per cost method)
- Reorder report (items below reorder point)
- Slow-moving inventory (no movement in N days)
- Aging report (for batch-tracked items with expirations)

### Local-first compliance per Kleppmann property

| Property | How |
|---|---|
| **P1** | Stock-level lookups <16ms (projections cached); movement entry <16ms |
| **P2** | Warehouse-floor tablets + back-office laptop + mobile-sales devices sync; per-data-class policy: warehouse holds full inventory; sales sees only available-for-sale view |
| **P3** | Receiving + transfers + adjustments work offline; batch updates sync when signal returns |
| **P4** | Multiple receivers + multiple sales reps move stock concurrently; CRDT converges (per-location quantity is grow-only counter for receipts + grow-only counter for issues + adjustments append-only) |
| **P5** | Item master + movement history exportable as CSV; stock-level snapshots exportable as JSON |
| **P6** | Item costs (proprietary purchasing data) classified `shared-private`; not visible to all employees |
| **P7** | Owner can export full inventory + history; can revoke employee access; can crypto-shred per-customer purchase histories per privacy policy |

### CRDT semantics

- **Item master**: LWW-Map with delete-tombstones
- **Stock movement**: append-only log; per-location quantity is computed projection
- **Stock-level projection**: derived; eventually consistent across peers
- **Cost calculation**: deterministic function over movement log given cost method

### Specific failed-conditions to test

- Stock cannot go negative without explicit allow-negative flag → FAILS if negative qty allowed silently
- Concurrent issues from two devices for same lot don't double-issue → FAILS if same units leave twice
- Cost calculation deterministic across devices → FAILS if devices disagree on COGS
- Serial number uniqueness enforced per item → FAILS if same serial on two units

---

## §7. Module 4 — Projects

### Feature scope

Drawing from Plane (modern UI + MCP server integration vector) + OpenProject (Gantt + work breakdown) + Taiga (agile/sprint flow) + Wekan (kanban) + Redmine (issue tracking) + Invoice Ninja (time tracking → project billing):

**Project hierarchy**
- Project = (id, name, client-id, status, start, end, budget, billing-method)
- Phase = (project-id, name, order, % allocated)
- Task = (phase-id, name, description, assignee, status, est-hours, actual-hours, due, dependencies[])
- Subtask = task with parent-task-id

**Time tracking**
- Time entry = (user-id, task-id, date, hours, billable, notes)
- Per-user time sheets (weekly view)
- Timer / stopwatch UX (start / pause / stop)
- Batch entry from notes / calendar

**Resource allocation**
- Per-user availability calendar
- Per-user skills / hourly rate
- Allocation conflicts (over-allocated user warning)

**Views**
- List view (filter / sort / group)
- Kanban board (drag tasks across status columns)
- Gantt chart (timeline with dependencies)
- Calendar view (deadlines + milestones)

**File attachments**
- Per-task documents (specs, deliverables, references)
- Storage budget per project (per book DUR-08 storage budget enforcement)
- Eager (default) vs. lazy (storage-constrained device) sync

**Issue tracking**
- Issue = lightweight task type for bugs / change requests
- Workflow: open → in-progress → resolved → verified → closed

**Project-cost rollup**
- Time entries × user hourly rate = labor cost
- Material costs (linked to inventory issues)
- Vendor costs (linked to PO/bills tagged with project)
- Project P&L report → integrates with accounts module

**Client billing**
- Time-and-materials billing: generate invoice from billable time + costs
- Fixed-fee billing: invoice on milestone completion
- Retainer billing: invoice monthly with time-tracked drawdown

### Local-first compliance per Kleppmann property

| Property | How |
|---|---|
| **P1** | Task drag-drop on kanban <16ms; gantt-view rendering <100ms; time-entry save <16ms |
| **P2** | Project manager's laptop + team members' phones + tablet on-site all sync; per-data-class policy: PM sees full data; field crew sees their assigned tasks only |
| **P3** | Field worker logs hours on phone with no signal; tasks update on-site without server roundtrip |
| **P4** | Multiple team members concurrently edit task status / add comments / log time — CRDT converges |
| **P5** | Project plan + tasks exportable as Markdown; time entries as CSV; gantt as JSON |
| **P6** | Client confidential project data classified per project; per-project ACL (#46) — not all employees see all projects |
| **P7** | Owner can export entire project history; can revoke departed employee access; can crypto-shred completed-and-billed project data per data retention policy |

### CRDT semantics

- **Project / phase / task**: tree CRDT (parent-child) + per-node LWW-Map for fields
- **Task assignment**: LWW (last assignment wins)
- **Task comments**: append-only log
- **Time entries**: append-only log; deletion is a tombstone (audit trail)
- **Status transitions**: state machine with per-task lock to prevent concurrent transitions of same task

### Specific failed-conditions to test

- Time entry on closed project rejected → FAILS if late entry succeeds
- Concurrent status transitions of same task converge to one state → FAILS if state diverges
- Storage budget enforced per project → FAILS if attachments exceed budget without warning
- Field worker sees only their assigned tasks → FAILS if worker can browse other workers' assignments

---

## §8. Anchor vs. Bridge feature split

| Capability | Anchor (desktop full-node) | Bridge (relay + admin console) |
|---|---|---|
| **Local data store** | ✓ SQLCipher SQLite (full data) | Per-tenant SQLite shards (CIPHERTEXT only — relay can't decrypt) |
| **CRDT engine** | ✓ YDotNet (full operations) | Read-only CRDT for sync routing; cannot mutate without device key |
| **Sync daemon** | ✓ Initiates + receives sync | ✓ Receives + relays; no local mutation |
| **All four modules** (accounts/vendors/inventory/projects) | ✓ Full UI + features | None — Bridge has no business logic; only sync |
| **Reports + analytics** | ✓ All reports compute locally | None — analytics only computable on Anchor with decryption keys |
| **Plain-text export** | ✓ All formats | None — Bridge cannot decrypt |
| **Tenant management UI** | None | ✓ Admin console for managing multiple tenants (one tenant = one SMB) |
| **Per-tenant billing** | None | ✓ Bridge tracks usage per tenant; bills tenant for relay service |
| **Audit log of relay activity** | ✓ Local audit log for owner | ✓ Tenant-visible audit log of relay-side operations (who connected, sync volume, no content) |
| **Backup orchestration** | ✓ Local backup to user-chosen location | Optional: Bridge holds encrypted backup blobs (if tenant opts in) |
| **Key recovery custodian** | None — Anchor IS the keyholder | Optional: Bridge can serve as custodian-of-last-resort with escrow protocol |
| **MDM / fleet management** | Per-device | ✓ Per-tenant fleet view; rotate keys across N Anchor instances |

### Deployment patterns

**Anchor-only (single user, single device)**
- Solo proprietor with one laptop
- All data local; backup to external drive
- No multi-device; no off-site access

**Anchor-plus-Anchor LAN (small team, on-prem)**
- 2-10 Anchor instances on same office LAN
- LAN sync via mDNS discovery
- Optional small Anchor-on-NAS as 24/7 sync hub
- No off-site access without Bridge

**Anchor-plus-Bridge (small team, off-site access)**
- 2-50 Anchor instances + 1 Bridge tenant
- Bridge = managed cloud OR self-hosted
- Off-site / mobile access via Bridge
- Standard SMB deployment

**Anchor-plus-Bridge-multi-tenant (Bridge as service)**
- Multiple SMBs share one Bridge deployment
- Each SMB = one tenant with strict isolation
- Bridge operator sells relay-as-service to many SMBs
- Standard "managed local-first" business model

---

## §9. Local-first compliance matrix

Cross-cuts §4-§7 modules with §1 properties — this is the conformance scorecard target for the MVP:

| | Accounts | Vendors | Inventory | Projects |
|---|---|---|---|---|
| **P1 No spinners** | All entry < 16ms; reports background | All entry < 16ms; PO state changes < 16ms | Stock lookup < 16ms; cached projections | Drag-drop < 16ms; gantt < 100ms |
| **P2 Multi-device** | Accountant + owner + bookkeeper sync | Buyer + receiver + AP clerk sync | Warehouse + store + sales-mobile sync | PM + team + field-crew sync |
| **P3 Network optional** | Full offline | Receive in warehouse offline | Movements offline; sync later | Field time-entry offline |
| **P4 Collaboration** | Multi-user concurrent (CRDT) | PO + receipt + bill across roles | Concurrent receipts / issues converge | Concurrent kanban + comments converge |
| **P5 Long now** | Beancount export | CSV + JSON export | CSV + JSON export | Markdown + CSV + JSON export |
| **P6 Security** | Encrypted at rest; tax-sensitive `private` | Vendor banking `private` (separate KEK) | Item costs `shared-private` | Per-project ACL; client data per-classification |
| **P7 Ownership** | Owner exports + revokes + crypto-shreds PII | Owner exports + revokes + crypto-shreds vendor PII | Owner exports + revokes + crypto-shreds purchase history | Owner exports + revokes + crypto-shreds project data per retention |

**Conformance baseline target:** ≥80% per cell after 12-month build.

---

## §10. Phased roadmap

### Phase 1 (Months 1-2): Foundation

- Anchor app shell (.NET MAUI Win/Mac/Linux)
- Bridge service shell (ASP.NET Core multi-tenant)
- User identity (Ed25519 device keys + per-tenant data keys)
- Sync protocol (basic CRDT delta exchange per Appendix A wire format)
- Backup/restore + multi-sig social recovery (#48 key-loss recovery)
- ICM pipeline variant: build `sunfish-inverted-stack-conformance` per design-decisions.md §7
- First baseline conformance scan against this skeleton

**Deliverable:** Anchor opens, syncs with another Anchor over LAN, syncs with Bridge over WAN, key recovery flow works end-to-end.

### Phase 2 (Months 3-4): Accounts module

- Chart of accounts (CoA template + custom)
- Journal entries (double-entry per book Ch12 ledger model)
- Bank import (OFX + CSV)
- Reconciliation
- Basic reports (P&L, balance sheet, cash flow)
- Invoicing (template builder + PDF generation)
- Multi-currency
- US sales tax handling (state-level)

**Deliverable:** Real bookkeeper can run their books for a small business for 30 consecutive days; conformance scan ≥70% across P1-P7 for accounts module.

### Phase 3 (Months 5-6): Vendors module

- Vendor master
- PO → receipt → bill three-way-match workflow
- Approval thresholds
- AP scheduling + payment recording
- 1099 / W-9 prep (US)
- Vendor performance scorecard
- Integration with accounts (AP)

**Deliverable:** SMB can manage full P2P (procure-to-pay) cycle; conformance ≥75% across vendors.

### Phase 4 (Months 7-8): Inventory module

- Item master (with variants)
- Multi-location stock
- Stock movements (receipts / issues / transfers / adjustments)
- Cost methods (FIFO + weighted-avg)
- Reorder reports
- Serial / lot / batch tracking (serial first; lot+batch in next phase)
- Integration with accounts (COGS, asset valuation) + vendors (PO receipts)

**Deliverable:** Light manufacturer or retail SMB can run inventory; conformance ≥80% across inventory.

### Phase 5 (Months 9-10): Projects module

- Project + phase + task hierarchy
- Time tracking (with timer)
- Kanban + list + gantt views
- File attachments
- Issue tracking
- Resource allocation
- Project-cost rollup to accounts
- Client billing (T&M + fixed-fee + retainer)

**Deliverable:** Consultancy or agency can run client projects; conformance ≥80% across projects.

### Phase 6 (Months 11-12): Polish + demo + GA

- Cross-module dashboards
- Search across all modules
- Per-resource ACL refinement (per primitive #46)
- Full conformance scan against both skills (target ≥80% across all modules)
- Three demo deployment scenarios fully built:
  - **Restaurant POS** (kiosks + back-office Anchor + Bridge for off-site owner)
  - **Construction company** (project-heavy + vendors for materials + accounts for billing)
  - **Small consultancy** (project-heavy + accounts for invoicing)
- Documentation + screencast videos
- Public release announcement

**Deliverable:** Public 1.0 release; baseline conformance reports committed to Sunfish ICM; demo videos published.

---

## §11. Conformance test targets

For each module, specific conformance tests to add to Sunfish CI:

### Accounts conformance tests

```yaml
test-id: ACCT-CONF-01
maps-to: ch12-crdt-engine-data-layer:CRDT-23 (Double-entry ledger as canonical CP subsystem)
test: Concurrent journal entries from 2 devices on same period converge to consistent ledger
property-served: P4
expected-outcome: After sync, both devices show same balance per account; total debits = total credits

test-id: ACCT-CONF-02
maps-to: ch15:KEY-04 (Argon2id key derivation)
test: SQLCipher key derived with Argon2id parameters per book
expected-outcome: Memory ≥ 64 MiB, iterations ≥ 3, parallelism ≥ 1; key distinct from password

test-id: ACCT-CONF-03
maps-to: ch16:DUR-25 (Plain-file export)
test: Full ledger exports to Beancount text format; round-trips through Beancount CLI without loss
expected-outcome: Beancount imports the export; all transactions present; account hierarchy intact

test-id: ACCT-CONF-04
maps-to: P1 + #43 performance contracts
test: Journal entry write commits to local SQLite in <16ms p95
expected-outcome: 1000 sequential writes; p95 <16ms; p99 <50ms

test-id: ACCT-CONF-05
maps-to: P3 + #44 per-data-class device-distribution
test: Full bookkeeping workflow completes with network disabled
expected-outcome: 30-minute offline session; 200 transactions entered; reconciliation marked; no errors; sync queues delta for later
```

### Vendors / Inventory / Projects conformance tests

(Similar structure — see template above. Subagent can generate per-module specifics during build.)

### Cross-module conformance tests

```yaml
test-id: XMOD-CONF-01
maps-to: P4 collaboration + #46 per-resource ACL
test: 5 concurrent users editing different modules simultaneously
expected-outcome: All edits converge; permissions enforced (sales user cannot see vendor banking)

test-id: XMOD-CONF-02
maps-to: P7 + #48 key-loss recovery
test: Simulate owner laptop loss; multi-sig social recovery via 3-of-5 trustees restores access
expected-outcome: Within 7-day grace window, recovered; original holder can dispute; after grace, keys re-issued

test-id: XMOD-CONF-03
maps-to: P5 + #37 long-horizon format stability
test: Export everything; advance simulated clock by 25 years; re-import using version 1.0 format spec
expected-outcome: All data round-trips; version-spec frozen at v1.0 still readable
```

---

## §12. Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| .NET MAUI cross-platform stability issues | Medium | High | Track .NET MAUI roadmap; have Tauri fallback evaluated by end of Phase 1 |
| YDotNet performance on large CRDT histories | Medium | High | Per book Ch12 GC strategy; benchmark at 10k / 100k op corpus during Phase 1; switch to Loro early if YDotNet doesn't scale |
| Tax handling complexity (50 US states + international) | High | Medium | Phase 2 ships US-state-level only; international (GST/VAT) in Phase 4 or post-1.0; partner with tax-rate-data provider |
| Multi-currency edge cases (lost cents, conversion timing) | Medium | Medium | Use decimal math (not float); store rates with effective-from-date; comprehensive currency test suite |
| Conformance scan finds <60% baseline | Medium | High | Iterate per phase; close highest-leverage gaps first; some primitives (e.g., long-now governance #40-#42) won't apply to MVP |
| Concurrent Claude sessions step on each other | High | Medium | Strict ICM coordination via icm/00_intake/; each session works in distinct package directory; merge via Sunfish's existing review process |
| Scope creep: "we need feature X" mid-phase | High | Medium | Treat all new requests as post-1.0 unless they unblock current phase; add to backlog |
| Bridge multi-tenant scaling | Low | High | Single-tenant Bridge first (Phase 1); multi-tenant in Phase 6; deferred until needed |

---

## §13. Out of scope for MVP

Explicit non-goals for the 12-month MVP — all flagged for post-1.0:

- **Mobile native apps** (iOS / Android) — read-only mobile-web-PWA against Bridge in 1.x; native in 2.0
- **Manufacturing module** (BOM, work orders, MRP) — too complex for MVP; hooks for v2.0
- **CRM module** (sales pipeline, opportunity tracking) — basic customer master in accounts module; full CRM in 2.0
- **HR / Payroll** — high regulatory complexity; integrate with external payroll providers in 1.x
- **Banking integration via Plaid / Yodlee** — manual OFX import in MVP; live connections in 1.x
- **AI features** (auto-categorization, natural-language reports) — possibly in 1.x via Sunfish.AI plugin
- **Multi-language UI** — handled by other concurrent session; MVP ships English-only initially
- **Full WCAG 2.2 AAA** — handled by other concurrent session; MVP targets AA
- **DePIN / cryptoeconomic features** — book Volume 3 territory; not in scope
- **Long-now governance features** (#40-#42) — book Volume 5B territory; not in scope
- **Cyber-physical / IoT features** — book Volume 2 territory; not in scope
- **Spacecraft / DTN** — book Volume 4 territory; obviously not in scope

---

## §14. Coordination with other Sunfish sessions

| Concurrent session | Coordination point | Coordination mechanism |
|---|---|---|
| **Components** (Sunfish.UiBlocks) | MVP modules use components; new components requested via icm/00_intake/ | ICM ticket per new component need; component session implements; MVP session integrates |
| **Multi-language** (i18n / l10n) | All MVP user-facing strings flow through i18n framework | Strings extracted via existing framework; MVP session adds keys; i18n session adds locale data |
| **Disabled-user** (a11y / WCAG) | All MVP UI uses a11y-compliant components; keyboard nav + screen reader tested per module | Component session handles a11y at component level; MVP session uses components correctly |

The MVP plan does NOT specify implementations for these dimensions — it integrates with whatever the concurrent sessions produce. When a coordination need arises (e.g., MVP needs a "currency-amount-input" component that doesn't exist), MVP session files an icm/00_intake/ ticket; component session decides whether to build, when, and how.

---

## §15. Updating this plan

This is **live planning**, expected to evolve. Update when:

- Module scope shifts based on implementation experience
- New OSS lesson surfaces from build (e.g., "we hit problem X; existing tool Y solves it as Z")
- Conformance test fails and reveals a missing primitive
- Phase ordering needs adjustment based on actual velocity
- Risk register entry materializes (mitigation activates)

Treat as canonical execution spec until 1.0 ships; thereafter the codebase becomes canonical and this plan tracks 2.0 roadmap.

---

## Appendix A — Quick reference: relevant book chapters

For the MVP build, these chapters are most directly relevant:

- **Ch11 Node Architecture** — kernel + plugin pattern; module-as-plugin for accounts/vendors/inventory/projects
- **Ch12 CRDT Engine + Data Layer** — three-tier resolution; ledger as CP-class CRDT (CRDT-23 directly applies to accounts)
- **Ch13 Schema Migration** — module schemas evolve over years; expand-contract pattern
- **Ch14 Sync Daemon Protocol** — Anchor↔Anchor LAN sync + Anchor↔Bridge WAN sync
- **Ch15 Security Architecture** — KEK/DEK envelope; per-tenant + per-user key custody; encryption-at-rest via SQLCipher
- **Ch16 Persistence Beyond the Node** — backup + recovery; plain-file export per module
- **Ch17 Building First Node** — start-here playbook; MVP follows this
- **Ch18 Migrating Existing SaaS** — for users coming from QuickBooks/Xero into Sunfish; Phase 6 documentation
- **Ch19 Shipping to Enterprise** — when an SMB grows mid-market; signing + MDM; out-of-MVP scope but architecture should not preclude
- **Ch20 UX Sync Conflict** — conflict resolution UI patterns; sync-state visualization; backup-state UX

For the conformance work:

- **Appendix A** — sync daemon wire protocol (Phase 1 implements this)
- **Appendix B** — threat-model worksheets (per-module worksheets in Phase 1)
- **Appendix D** — testing the inverted stack (per-phase test patterns)
- **Appendix F** — regulatory coverage (US sales tax, GDPR, etc. — per-deployment compliance manifest)
