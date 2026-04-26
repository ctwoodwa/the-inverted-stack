# Design Decisions — Conformance Skills, ICM Variants, Catalog Extensions

**Status:** Decision brief, not implementation. Captures decisions from a multi-turn design discussion (April 2026) for execution in future sessions. Live design — superseded by code/skills/ICM artifacts as they are built.

**Audience:** Whoever (likely future-Claude) executes Path 1 polish or Step 3 in subsequent sessions, needing full design context without re-doing the discussion.

---

## 1. Decisions made (executive summary)

### 1.1 Architecture

| Layer | Where | What |
|---|---|---|
| Concept catalog | This repo | `docs/reference-implementation/concept-index.yaml` (562 concepts) — the single source of truth |
| Generic conformance skill | This repo | `.claude/skills/local-first-properties/` — Kleppmann 7-property check, foundational subset |
| Book-specific conformance skill | This repo | `.claude/skills/inverted-stack-conformance/` — full 562-concept catalog |
| ICM pipeline variants | Sunfish repo | `c:/Projects/Sunfish/icm/pipelines/` — Sunfish-specific glue |
| Conformance map | Sunfish repo | `c:/Projects/Sunfish/icm/_config/conformance-map.md` — concept→package mapping per app |
| Conformance decisions | Sunfish repo | `c:/Projects/Sunfish/icm/_config/conformance-decisions.yaml` — approved-gap / in-scope / deferred records |

### 1.2 Sunfish ICM rename + new variants

| Variant | Current/New | Question it answers |
|---|---|---|
| `sunfish-component-parity` | RENAME from `sunfish-gap-analysis` | "Do sibling components / adapters / APIs match their documented contract and each other?" |
| `sunfish-local-first-conformance` | NEW | "Does this accelerator app satisfy Kleppmann's seven properties under its supported deployment combos?" |
| `sunfish-inverted-stack-conformance` | NEW | "Does this accelerator app implement *The Inverted Stack*'s full architectural commitments?" |

Naming convention: short names; rely on per-variant README for scope clarification.

### 1.3 Catalog extensions for Path 1 polish (this repo)

To be added to `SCHEMA.md` and applied across `concept-index.yaml`:

1. **`security-axis: [confidentiality, authenticity]`** per concept — separates the orthogonal security properties so deployment-side data-class declarations can selectively relax/enforce
2. **`applies-to-roles: [full-node, ...]`** per concept (defaults to all roles) — makes role-aware scoring possible at catalog level rather than only at conformance-map level

### 1.4 Mapping freshness — Option C (hybrid)

Hand-maintain anchor namespaces in `conformance-map.md`; auto-validate file paths via grep. Drift caught when namespace moves (rare); map survives package reorganizations (common). Validator wired into `sunfish-{local-first,inverted-stack}-conformance` Stage 07 Review.

### 1.5 Conformance-decisions unified mechanism

`conformance-decisions.yaml` (per Sunfish repo, possibly per-app variants) records:

- `approved-gap` — intentionally not implemented (with rationale + reviewer + date + review-by); does NOT count against headline % score
- `in-scope` — actively planned (with target sprint + owner); counts as `partial` if not yet implemented
- `deferred` — not now, not approved-gap, just not on roadmap; counts as `missing` but flagged "deferred (no current owner)"

Re-runs read this file first; only flag concepts NOT in the decisions file as new gaps requiring triage.

### 1.6 Engine-substitution-table

`c:/Projects/Sunfish/icm/_config/engine-substitution-table.md` lists CRDT-engine-bound concepts and which alternates satisfy them. Example: `CRDT-12: ICrdtEngine adapter pattern` is YDotNet-specific in book; satisfied by Loro adapter implementing same interface contract.

---

## 2. Skills design (both)

### 2.1 Common behaviors

- **ICM-aware output destination.** If target repo has `icm/CONTEXT.md`, write report into `icm/01_discovery/output/<skill>-<date>.md`. Else create `.<skill>/` at repo root and write `report-<date>.md`.
- **Read-only on target source.** Skills only write the report; never modify scanned code.
- **Idempotent.** Re-runs produce fresh reports without modifying anything in the target repo.
- **Modes: quick / standard / deep.** Trade-off scan time vs. depth. Default `standard`.
- **Multi-app per-app + roll-up.** When target repo has multiple apps (e.g., Sunfish has Anchor + Bridge), score each app individually AND produce platform-level roll-up. Detect apps via convention (`apps/<name>/`); fall back to ask user.
- **Optional `.local-first-scope.yaml` in target repo.** Declares which apps + which deployment combos are claimed; skill respects scope and doesn't penalize out-of-scope concepts.
- **Delta tracking.** Diffs against previous report in same output dir; surfaces "↑ improved", "↓ regressed", "→ new gap" since last run.
- **Output retention.** Keep N most recent reports (default N=10); prune older. Override with `--all` to keep everything.
- **Blocked-on-user section.** Verification recipes that require dynamic checks (run integration tests, observe behavior) are flagged in a separate section so user knows what they need to verify themselves.
- **Stub detection.** A class/function existing as `// stub — not yet implemented` counts as `partial`, not `complete`. Verification recipes must distinguish.

### 2.2 Out-of-scope-for-current-book section

Cyber-physical / multi-stakeholder-economic / extreme-environment deployments will exceed the current catalog's scope. Reports include a section listing the architectural primitives the deployment requires that the book doesn't cover, pointing to `book-extension-candidates.md` (future-book-writing roadmap).

### 2.3 Two skills, scope split

| Skill | Audience | Catalog scope | Output organization |
|---|---|---|---|
| `local-first-properties` | Any local-first repo (Loro/Yjs/Automerge/Sunfish/custom) | `foundational` only (538 entries) | Grouped by Kleppmann property P1-P7 |
| `inverted-stack-conformance` | Repos claiming Inverted Stack alignment | Full 562 concepts | Grouped by chapter epic; cross-cut by Kleppmann property |

---

## 3. App archetype taxonomy

### 3.1 Roles

Concept's `applies-to-roles:` tag selects which roles need to satisfy it. Default: all roles.

| Role | Description |
|---|---|
| `full-node` | Owns data, syncs as peer, has human user. Anchor, mobile, tablet. |
| `full-node-multi-user` | Like full-node but multi-user-on-one-device with per-shift identity rotation. Kiosk, vending machine consumer face. |
| `full-node-headless` | Full node behavior with no human user at the device. Server-side Anchor, weather station, smart meter, vehicle ECU, robot, vending operational backend. UX-* concepts mostly N/A; observability/fleet-mgmt concepts gain weight. |
| `relay` | Routes ciphertext, no data ownership. Bridge, LAN hub, edge gateway, federated relay. |
| `thin-client-read` | Consumes / displays node data, doesn't own it. Browser extension, read-only viewer, voice interface, TV viewer, web dashboard. |
| `thin-client-write` | Pushes data to a node, doesn't read or own. Sensor, scanner, form portal, webhook receiver. |
| `legacy-bridge` | Translates between Inverted Stack and external systems. POS-bridge, payment-processor connector, OPC-UA bridge, SCADA connector, blockchain payment rail. |
| `developer-tool` | For people building ON the platform. CLI, SDK, inspector, dev-tools. |

### 3.2 Apps in v1 conformance-map (Sunfish-side)

| App | Status | Role | Form |
|---|---|---|---|
| `anchor` | Today (Zone A) | full-node | desktop Win/Mac/Linux |
| `bridge` | Today (Zone C) | relay (+ admin console as thin-client-read via browser plug-in or separate install) | headless API + browser client |
| `mobile` | Placeholder | full-node | iOS / Android native |
| `kiosk` | Placeholder | full-node-multi-user | locked-down terminal |
| `lan-hub` | Placeholder | relay | self-hosted Pi/NAS for in-network sync |

Future apps register in conformance-map as built. Suggested archetypes worth scaffolding for:
- `tablet` (full-node, between mobile and desktop)
- `anchor-embedded` (full-node-headless, RPi-class for IoT/sensor scenarios)
- `browser-extension` (thin-client-read)
- `cli` (developer-tool)

---

## 4. Deployment scenarios (13 captured)

Each is a deployment combination of apps + a `data-classes:` block + Kleppmann property coverage. The conformance scorer interprets these to know what counts as in-scope for a given target.

### 4.1 In current book scope (information systems)

```yaml
- id: small-office-typical
  apps: [anchor × 5-10, lan-hub × 1, bridge × 1]
  notes: Standard small-office Inverted Stack deployment; LAN sync hub for in-house resilience + Bridge for off-site mobile/remote
  properties-satisfied: [P1, P2, P3, P4, P5, P6, P7]

- id: regulated-air-gap
  apps: [anchor × 5, lan-hub × 1]
  notes: Defense / classified / hospital-private; no internet egress
  properties-satisfied: [P1, P2, P3, P4, P5, P6, P7]

- id: solo-traveler
  apps: [anchor × 1, mobile × 1, bridge × 1]
  notes: One user, three devices, internet-routed sync
  properties-satisfied: [P1, P2, P3, P5, P6, P7]
  properties-degraded: [P4]   # solo user has no collab need

- id: kiosk-tenant
  apps: [kiosk × 4, bridge × 1]
  notes: Retail front-of-house; per-shift identity rotation; admin via Bridge
  properties-satisfied: [P1, P3, P5, P6, P7]
  properties-degraded: [P2, P4]

- id: restaurant-pos
  apps: [kiosk × 4, anchor × 1 (back-office), lan-hub × 1, bridge × 1, pos-bridge × 1]
  notes: Multi-station POS + LAN hub for in-house resilience + Bridge for off-site owner; payment processor as legacy-bridge
  properties-satisfied: [P1, P3, P4, P5, P6, P7]
  compliance-relevant: [PCI-DSS, local-tax-records, health-dept-records]

- id: farmers-market-vendor
  apps: [mobile × 1, bridge × 1, pos-bridge × 1]
  notes: Single vendor; offline all day; end-of-day sync
  properties-satisfied: [P1, P3, P5, P6, P7]
  properties-degraded: [P2, P4]

- id: farmers-market-multi-vendor
  apps: [mobile × N, lan-hub × 1, bridge × 1]
  notes: Market-organizer-supplied LAN hub; per-vendor tenant isolation on Bridge; aggregated organizer analytics
  properties-satisfied: [P1, P2, P3, P5, P6, P7]
  properties-degraded: [P4]

- id: vending-machine-route
  apps: [kiosk × N (10-1000), bridge × 1, pos-bridge × 1, thin-client-read × M (operations + service-techs)]
  notes: |
    Unattended kiosk fleet. Each machine = node owning inventory + sales + health.
    Multi-tenant data: operator owns sales/inventory; property owner sees aggregate
    revenue (commission); brand partner sees aggregate sell-through. Service techs
    pair via Bluetooth locally for low-bandwidth diagnostic + restock confirmation.
  properties-satisfied: [P1, P3, P5, P6, P7]
  properties-degraded: [P2, P4]
  data-classes:
    sales-transactions:
      confidentiality: shared-private (operator + property-owner-aggregate)
      authenticity: attested
      retention: 7yr-tax-mandate
    cash-vault-events:
      confidentiality: private (operator)
      authenticity: attested-with-chain-of-custody    # tamper-evident vault access
      retention: 7yr-anti-theft
    consumer-payment-data:
      confidentiality: legacy-bridge-handles    # PCI scope at processor
      authenticity: attested
  catalog-coverage-estimate: ~70-80%   # well within current book scope
```

### 4.2 Out of current book scope — IoT / sensor

```yaml
- id: single-weather-station
  apps: [anchor-embedded × 1 (RPi), bridge × 1, thin-client-read × 1+]
  notes: Solar-powered station, continuous sensor ingestion, weeks-of-disconnection-tolerant
  properties-satisfied: [P1, P3, P5, P6, P7]
  properties-degraded: [P2, P4]
  stress-points: [CRDT growth, power-loss resilience, embedded-key provisioning, storage budget]

- id: weather-station-network
  apps: [anchor-embedded × N (5-50), lan-hub × 1, bridge × 1, thin-client-read × M]
  notes: Distributed sensor mesh; LoRa/cellular; mixed-privacy data classes (sensor public, health shared, calibration private)
  properties-satisfied: [P1, P3, P4, P5, P6, P7]
  properties-degraded: [P2]
```

### 4.3 Out of current book scope — multi-stakeholder economic

```yaml
- id: utility-smart-meter
  apps: [anchor-embedded × N (1k-100k), bridge × 1-K, thin-client-read × 1+ per home, legacy-bridge × 1 (SCADA)]
  notes: |
    Per-house meter node owned by homeowner; utility holds SCOPED write authority
    for demand response (AC cycling, water-heater delay, EV-charging schedule).
    Real-time grid-frequency data + monthly billing aggregate + appliance control
    commands all distinct data classes.
  catalog-coverage-estimate: ~50-60%
  out-of-scope-for-book: cyber-physical-AND-multi-stakeholder
  new-primitives-needed:
    - Delegated capability tokens (utility's scoped write authority)
    - Real-time CP-class command channel (sub-second AC cycling)
    - Privacy-preserving aggregation (DP for billing buckets)
    - Tariff-anchored consent contract (regulator-supervised opt-in)

- id: depin-storage-node
  apps: [anchor-embedded × N (10s of thousands), relay × M (decentralized DHT), thin-client-read, legacy-bridge × 1 (blockchain)]
  notes: |
    Filecoin / Storj / Arweave / Sia / Helium / WeatherXM class. Permissionless
    participation; cryptoeconomic security (stake-and-slash); on-chain reward
    distribution; decentralized governance.
  catalog-coverage-estimate: ~30-40%
  out-of-scope-for-book: multi-stakeholder-economic
  new-primitives-needed:
    - Cryptoeconomic security (stake/slash, sybil resistance)
    - Hardware attestation (TPM/SGX instead of MDM)
    - Proof-of-resource protocols (storage/bandwidth/coverage challenges)
    - On-chain payment integration (smart contract interaction)
    - Decentralized governance (DAO-style protocol upgrades)
    - Cross-jurisdictional operator base (multi-country tokenization)
```

### 4.4 Out of current book scope — cyber-physical

```yaml
- id: commercial-fleet-vehicle-telematics
  apps: [anchor-embedded × N (10-1000) per truck, lan-hub × 1 (depot), bridge × 1, thin-client-read × M, legacy-bridge × 1 (insurer evidence portal)]
  notes: |
    Vehicle-mounted RPi-class telematics. GPS + dashcam + vehicle telemetry.
    Critical: data-class ESCALATION on incident trigger — routine dashcam is
    shared-private with rolling 30-day retention; on event, escalates to
    attested-with-chain-of-custody, retention extends, signing-tier upgrades
    for evidence handoff to insurer/court.
  catalog-coverage-estimate: ~50-60%
  out-of-scope-for-book: cyber-physical (chain-of-custody + escalation gaps)

- id: passenger-vehicle-local-first
  apps: [anchor-embedded × 1 (vehicle ECU cluster, ASIL-D), thin-client-read × 1+, bridge × 0-1 (federated learning), legacy-bridge × varies]
  notes: |
    Local-first inversion of Tesla model. Driving decisions local + formally
    verified; OTA updates from chosen sources not vendor-locked; fleet learning
    via opt-in federated learning + DP. 15-25 year hardware lifetime.
  catalog-coverage-estimate: ~25-35%
  new-primitives-needed:
    - Safety-critical real-time control (ISO 26262 ASIL-D)
    - Multi-decade hardware stewardship
    - V2X peer-to-peer mesh (sub-100ms)
    - Family/fleet multi-driver profiles with strict privacy
    - Federated learning / differential privacy
    - Physical tampering threat model

- id: consumer-robot-vacuum-or-mower
  apps: [anchor-embedded × 1, lan-hub × 1, thin-client-read × 1+]
  notes: Roomba / Mammotion class. Privacy-sensitive home interior map owned locally.
  catalog-coverage-estimate: ~50-60%

- id: humanoid-robot-home-or-workplace
  apps: [anchor-embedded × 1 (dual-mod safety), lan-hub × 1, bridge × 0-1 (federated learning)]
  notes: Tesla Optimus / Figure / 1X / Boston Dynamics class. ~100x privacy concern of consumer robot.
  catalog-coverage-estimate: ~20-30%
  new-primitives-needed:
    - Safety envelope enforcement (ISO 13482)
    - Physical-action provenance (audit trail of actuator commands)
    - Multi-party liability chain-of-custody
    - Model update as data (federated ML weights as CRDT)
    - Human-robot trust calibration UX

- id: industrial-robot-factory-floor
  apps: [anchor-embedded × N (1-100/cell), lan-hub × 1, legacy-bridge × 1 (OPC-UA), thin-client-read × M]
  notes: Fanuc / ABB / KUKA / UR. Already typically air-gapped. Process-IP local.
  catalog-coverage-estimate: ~45-55%
```

### 4.5 Out of current book scope — shared / supervised cyber-physical

```yaml
- id: shared-micromobility
  apps: [anchor-embedded × N (1k-50k/city), bridge × K (per-city), thin-client-write × ephemeral-per-rider, thin-client-read × ops, legacy-bridge × city-MDS, legacy-bridge × payment, legacy-bridge × insurance]
  notes: |
    Lime / Bird / Spin / Tier class. Scooter is a node — owns location,
    battery, lock state, ride-session log. Rider rents for minutes-to-hours
    then identity dissolves. Geofence enforcement local + verifiable.
    Per-city Bridge tenants handle multi-jurisdictional variation. Mandated
    real-time MDS export to city with verifiable-completeness contract.
  catalog-coverage-estimate: ~45-55%
  new-primitives-needed:
    - Ephemeral identity / use-right tokens (15-min-to-hour scoped grants; identity dissolves after session)
    - Geofence enforcement as architectural primitive (local-first geo-bounded behavior, works offline)
    - Mandated real-time regulatory export (signed streaming compliance data with verifiable-completeness)

- id: last-mile-delivery-robot-supervised
  apps: [anchor-embedded × N (10s-1000s), bridge × 1, thin-client-write × M (supervisors), thin-client-read × consumer+restaurant, legacy-bridge × restaurant-pos+stripe]
  notes: |
    Starship / Kiwibot / Coco (sidewalk); Nuro (street); Wing / Zipline
    (aerial). 90% autonomous; human supervisor takes over on hard cases.
    Each supervisor oversees 5-20 robots; handoff requires sub-200ms latency.
    Multi-handoff cargo chain-of-custody: restaurant → robot → consumer.
    Public-space operation creates accountability when robot encounters
    pedestrians, vehicles, or property.
  catalog-coverage-estimate: ~25-35%
  new-primitives-needed:
    - Human-in-the-loop override authority (autonomous control + low-latency manual override; supervisor identity attested per session)
    - Latency-critical remote supervisor session (sub-200ms video + telemetry + control transfer)
    - Multi-party cargo chain-of-custody (restaurant → robot → consumer 3-party signed handoff)
    - Public-space behavior accountability (incident data immutable for after-the-fact liability)
```

### 4.6 Out of current book scope — controlled ownership transfer

```yaml
- id: office-of-authority-transition
  apps: [anchor-embedded × 1 (tamper-evident-rugged-portable), thin-client-write × 2-4 (outgoing+incoming officer creds), thin-client-read × M (witnesses), legacy-bridge × varies (command-authority-chain)]
  notes: |
    Nuclear football / presidential authentication / Fed chair transition /
    central bank governor handover. System bound to OFFICE, not holder.
    At constitutionally-defined transfer instant, outgoing officer's
    cryptographic capability revokes; incoming officer's activates.
    Multi-party attestation (Chief Justice, military aide, Joint Chiefs).
    Constraints persist: only office-holder can exercise authority.
  catalog-coverage-estimate: ~15-20%
  out-of-scope-for-book-volume: civic-governance-systems
  new-primitives-needed: [#31 whole-system ownership transfer, constitutional constraint enforcement, continuous physical custody during transition]

- id: medical-custody-transfer
  apps: [anchor-embedded × 1 (instrumented container), thin-client-write × 5-8 (procurement+courier+recipient), bridge × 1 (UNOS), legacy-bridge × 1 (hospital EHR)]
  notes: |
    Organ transplant container / blood products / vaccine cold chain /
    biological samples. Container is a node owning temperature history +
    custody chain + viability window. Ownership of CONTENTS transfers
    through multi-stakeholder chain: donor → procurement → courier →
    recipient hospital → recipient. Each handoff multi-party signed.
    Constraints persist: cold chain, viability window, UNOS allocation
    rules. Container refuses release if constraints violated.
  catalog-coverage-estimate: ~30-40%
  out-of-scope-for-book-volume: medical-systems
  new-primitives-needed: [#31 whole-system ownership transfer, viability-window constraint enforcement, tiered custody-vs-ownership distinction]

- id: corporate-asset-acquisition
  apps: [anchor-embedded × N (acquired systems), thin-client-write × legal+tech-counsel, legacy-bridge × regulatory-filings]
  notes: |
    Company A acquires Company B; ALL Company B systems atomically transfer
    ownership at deal-close. Today: weeks of integration. Node-based
    cryptographic transfer: instant at deal-close attestation. All systems'
    credentials reissue atomically; old revokes; new ownership recorded
    immutably. Constraints persist: regulatory commitments, customer
    license terms, employment contracts, IP licenses.
  catalog-coverage-estimate: ~20-30%
  out-of-scope-for-book-volume: civic-governance-AND-multi-stakeholder
  new-primitives-needed: [#31 whole-system ownership transfer, atomic multi-system co-transfer, contract-surviving constraints]
```

### 4.6.1 Out of current book scope — succession arrangements (extends §4.6 ownership transfer)

```yaml
- id: small-business-succession-named-beneficiary
  apps: [anchor × 1 (existing business deployment), thin-client-write × varies (owner + beneficiary + executor + civic-attestor), legacy-bridge × 1 (probate court / death cert authority)]
  notes: |
    Restaurant owner / sole proprietor pre-arranges succession: designates
    beneficiary; designates lawyer as executor with TRANSFER-AUTHORITY-ONLY
    (executor can authorize transfer but cannot use the restaurant). On
    owner death, multi-party attestation triggers #31 ownership transfer:
    death certificate (civic legacy-bridge) + executor signature +
    beneficiary acceptance replaces the impossible outgoing-owner signature.
    Constraints persist (PCI, supplier contracts, health-dept, employees).
  catalog-coverage-estimate: ~20-30%
  new-primitives-needed: [#32 succession arrangements, #32a meta-capability delegation (executor has authority OVER transfer without USE of system), civic-attestor pattern]

- id: trust-managed-asset-succession
  apps: [anchor × N (trust-administered systems), thin-client-write × varies (settlor + trustee + beneficiaries + co-trustees), legacy-bridge × 1 (trust admin + tax authority)]
  notes: |
    Sophisticated estate planning. Owner places systems in trust; trustee
    (person / bank trust dept / institution) controls disposition per terms.
    Co-trustees (multi-sig), spendthrift provisions, pour-over from will,
    incentive provisions. On qualifying events (settlor death, milestone),
    trust executes ownership transfer per terms.
  catalog-coverage-estimate: ~25-35%
  new-primitives-needed: [#32 succession, #32d programmatic trust conditions (machine-verifiable transfer terms), multi-sig trustees with weighted votes]

- id: multi-sig-social-recovery
  apps: [anchor × 1 (personal/business system), thin-client-write × 5+ (pre-designated guardians)]
  notes: |
    Crypto-native pattern (Argent, Safe wallets, Vitalik's social-recovery
    proposal). Owner pre-designates N guardians and threshold M (e.g., 3
    of 5). On loss of access OR death, M guardians collectively authorize
    key reset / ownership transfer. No single guardian acts alone. Time-
    locks delay recovery for owner contestation. Particularly relevant for
    digital-native businesses, DePIN nodes, NFT collections, individuals
    without formal estate plans.
  catalog-coverage-estimate: ~30-40%
  new-primitives-needed: [#32 succession, #32c threshold-sig social recovery (M-of-N guardian authorization), #32e time-locked recovery delay (defense against collusion)]
```

### 4.7 Out of current book scope — extreme environment

```yaml
- id: deep-space-probe
  apps: [anchor-embedded × 1 (rad-hard, redundant), legacy-bridge × 1 (DSN), thin-client-read × ops-team]
  notes: Mars rover / Voyager class. Planet-scale latency; spacecraft autonomy authority; safing modes.
  catalog-coverage-estimate: ~25-30%
  new-primitives-needed:
    - Delay-tolerant networking (DTN / RFC 4838)
    - Asynchronous command authorization
    - Spacecraft autonomy authority + safe-mode protocols
    - Radiation-tolerant computation (ECC, TMR)
    - Mission-critical update gating (multi-stakeholder approval)

- id: leo-constellation-starlink-class
  apps: [anchor-embedded × N (1k-50k), relay × M (gateways), bridge × K]
  notes: Inter-satellite laser links; highly dynamic peer mesh (handoff every few seconds)
  catalog-coverage-estimate: ~40-50%

- id: crewed-vehicle-iss-or-mars-transit
  apps: [anchor-embedded × M, thin-client-read × crew, legacy-bridge × 1 (ground)]
  notes: Crew autonomy increases with distance; per-subsystem isolation (life support / propulsion / nav / science)
  catalog-coverage-estimate: ~30-35%
```

### 4.8 Other genuinely-new scenarios surfaced (briefly)

| Scenario | New primitive |
|---|---|
| **Submarine / deep-water research vehicle** | Acoustic comm protocols; total mission-critical isolation while submerged |
| **Voting systems** | Anonymity-preserving authenticity (anonymized + attested-as-eligible — needs zero-knowledge proofs) |
| **Drone swarms** | Highly-dynamic peer mesh at low altitude; jamming resistance; GPS-denied operation |
| **Aviation (commercial + GA)** | Multi-decade airworthiness certification + multi-jurisdictional regulation per flight |
| **Microgrids / prosumer energy markets** | Real-time economic operations between prosumers (overlap with smart-meter + DePIN) |
| **Pipeline / SCADA over long distances** | Continuous safety-critical operation across vast geographic areas with intermittent links |
| **Pacemakers / implanted medical devices** | Multi-decade implant lifetime; safety-critical with NO software-update path possible after implantation |

---

## 5. The 16 architectural primitives identified

Across all deployment scenarios, ~16 distinct architectural primitives surfaced. The book currently covers the first 8 cleanly; the rest are flagged for future book volumes.

### Volume 1 — information systems (current book)

1. **CRDT data plane** — convergent merge semantics, per-record-type primitives
2. **Sync protocol** — delta exchange, vector clocks, peer discovery, gossip, lease coordination
3. **Key custody** — KEK/DEK envelope, SQLCipher, key rotation, key recovery
4. **Zero-knowledge relay** — relay sees ciphertext only; never decrypts
5. **Multi-tenant isolation** — tenant boundaries on Bridge; per-tenant keys
6. **Schema evolution** — additive changes, lenses, version negotiation, epochs
7. **Plain-file export (P5)** — long-now data portability
8. **Threat-model worksheets** — named actors, named mitigations

### Volume 1 extensions (flagged, not yet written)

9. **Chain-of-custody** — multi-party signed transfer receipts, evidence-class temporal attestation
10. **Data-class escalation** — event-triggered re-classification with retention/signing/custody upgrade
11. **Fleet management** — provisioning at flash time, fleet-scale key rotation, OTA across N nodes, fleet observability
12. **Privacy-preserving aggregation** — DP / k-anonymity at relay-side aggregation

### Volume 2 — cyber-physical systems (potential)

13. **Safety-critical real-time control** — ISO 26262 / 13482 / IEC 61508; formal verification; verified-safe update gating
14. **Multi-decade hardware stewardship** — 15-50 year vehicle / aviation / spacecraft lifetimes; community-software-maintenance models
15. **Federated learning** — ML model weights as CRDT data; privacy-preserving training
16. **Physical adversarial threat model** — tampering, side-channels, V2X spoofing
17. **Human-machine trust calibration UX** — handoff protocols; when does the human take over?

### Volume 3 — multi-stakeholder economic systems (potential)

18. **Delegated capability tokens** — scoped third-party write authority (utility on home node; manufacturer warranty on appliance)
19. **Cryptoeconomic security** — stake/slash, sybil resistance, proof-of-resource protocols
20. **Decentralized governance** — DAO-style protocol upgrades; replaces vendor-led release model
21. **Tokenization regulatory layer** — Howey, MiCA, tax treatment of rewards
22. **Hardware attestation primitives** — TPM/SGX/Secure-Enclave instead of MDM

### Volume 4 — extreme environment systems (potential)

23. **Delay-tolerant networking** — DTN / Bundle Protocol; sync at hours/days timescale
24. **Highly-dynamic peer mesh** — sub-second peer enter/exit; orbital handoff; drone swarm coordination
25. **Anonymity-preserving authenticity** — voting; anonymous reporting; ZK-proof-of-eligibility
26. **Mission-critical autonomy authority** — when can the device act without operator approval (spacecraft, submarine, robot in extremis)?
27. **Update-gating with multi-stakeholder approval** — months of testing before deployment; spacecraft, aviation, medical implant

### Cross-volume additions (surfaced from shared / supervised cyber-physical)

28. **Ephemeral identity / use-right tokens** (Volume 3 multi-stakeholder economic) — short-lived, narrow-scope grants distinct from long-lived delegated capability. Sources: shared scooters (rental session), valet mode, courier handoff tokens, rental car sessions, time-bounded device access.
29. **Geofence enforcement as architectural primitive** (Volume 2 cyber-physical) — local-first geo-bounded behavior with verifiable enforcement that works offline. Sources: shared micromobility (slowdown / no-park zones), drone airspace restrictions, robot operating boundaries, asset-tracking with auto-disable on theft.
30. **Human-in-the-loop override authority** (Volume 2 cyber-physical) — combines autonomous safety-critical control with low-latency manual override; supervisor identity attested per session; handoff timing recorded for liability. Sources: last-mile delivery robots, semi-autonomous vehicles (lane-keeping vs. driver), industrial robots with operator-stop, surgical robots.
31. **Whole-system ownership transfer with persistent constraints** (Volume 3 multi-stakeholder economic, with civic-governance + medical-systems as cross-cutting application domains) — atomic transfer of entire system+data unit to new owner with cryptographic key reissuance and constraints that bind regardless of owner identity. Distinct from chain-of-custody (#9 — owner unchanged), delegated capability (#18 — owner unchanged + scoped grant), and ephemeral identity (#28 — owner unchanged + short-lived grant). Defining elements: atomic transfer event, old-owner key wipe, new-owner re-keying, multi-party attestation, constraint persistence (laws/contracts/biological-physical-limits bind regardless of owner), immutable transfer log, time-stamped activation, optional reversibility. Sources: nuclear football / presidential transition / Federal Reserve chair handover; organ transplant container / blood products / vaccine cold chain; vehicle title / real estate / land title transfer; digital estate inheritance; domain name / NFT / repository ownership; corporate acquisition / asset transfer; pawnshop / pledge; insurance subrogation; conservatorship; container shipping (TEU) handoffs.

32. **Succession arrangements with executor delegation** (Volume 3 multi-stakeholder economic, with civic-governance + estate-planning as cross-cutting application domains) — pre-arranged rules for ownership transfer when the owner CANNOT personally attest (death, incapacity, disappearance, force majeure, long-term absence). Builds ON #31 by providing the authorization path when the owner is absent. KEY ARCHITECTURAL INSIGHT: capability OVER the system (use, run, see data) is distinct from capability OVER the system's ownership (decide who gets it). Local-first architecture should explicitly separate these. Sub-patterns: 32a meta-capability delegation (executor/lawyer/trustee gets transfer-authority WITHOUT use authority), 32b event-triggered activation (death certificate / incapacity finding / milestone / time-lock as trigger), 32c threshold-sig social recovery (M-of-N guardians collectively authorize; no single guardian acts alone), 32d programmatic trust conditions (machine-verifiable terms — age, marriage, performance, tax-status), 32e time-locked recovery delay (owner contestation window before succession completes), 32f reversibility-while-living (settlor/testator can amend until trigger event, then irrevocable). Sources: small-business succession (restaurant owner dies, beneficiary inherits); estate planning (wills, trusts, POAs); conservatorship and guardianship; multi-sig social recovery (crypto wallets); corporate succession plans; partnership buyout agreements; franchise transfer rights; sports team / music catalog inheritance; digital estate planning. Edge cases: disputed succession (multiple claimants), intestate cases (no pre-arrangement; civic-default), owner-thought-dead-returns, cross-jurisdictional probate, tax-timing.

> **Note on regulatory streaming export:** the LADOT-MDS-style "mandated real-time signed export to a regulator with verifiable-completeness" pattern surfaced from the shared-scooter scenario is treated as a variant of chain-of-custody (#9) rather than a separate primitive — the architectural mechanism (signed streaming with append-only verifiable log) is the same.

---

## 6. Path 1 polish — concrete tasks for executor

These should be done in this repo before Step 3:

### 6.1 Schema updates

Add to `docs/reference-implementation/SCHEMA.md`:

```yaml
# New fields per concept entry:
security-axis: [confidentiality, authenticity]    # subset; both common; [] for non-security concepts
applies-to-roles: [full-node, full-node-headless]  # subset; defaults to all roles when omitted; explicit list when concept doesn't apply universally
```

### 6.2 Catalog tagging pass

Estimated 80-100 of the 562 concepts need explicit `security-axis` (the SEC-*, KEY-*, WIRE-*, some CRDT-* and SYNC-* entries). Default rules:

- Encryption-at-rest concepts → `security-axis: [confidentiality]`
- Signing / Ed25519 / replay-window concepts → `security-axis: [authenticity]`
- Handshake concepts that both encrypt session AND sign messages → `security-axis: [confidentiality, authenticity]`
- Non-security concepts → omit field (or `security-axis: []`)

For `applies-to-roles`: most concepts apply to all roles (defaults); explicit exclusions:

- UX-* concepts → `applies-to-roles: [full-node, full-node-multi-user]` (NOT headless / relay / thin-client / legacy-bridge)
- Fleet-management concepts (when added in Volume 1 extensions) → `applies-to-roles: [full-node-headless]`
- Relay-specific concepts (DUR-18, SEC-03, WIRE-21) → `applies-to-roles: [relay]`

### 6.3 Re-run consolidator + skill snapshot refresh

After tagging:

```bash
python build/consolidate_concept_index.py
python build/generate_chapter_overview.py
cp docs/reference-implementation/concept-index.yaml .claude/skills/inverted-stack-conformance/references/
cp docs/reference-implementation/concept-index-by-property.yaml .claude/skills/local-first-properties/references/
```

### 6.4 SKILL.md updates

Both SKILL.md files need a section on consuming the new fields:

- Section explaining how `security-axis` interacts with deployment-side `data-classes` declarations
- Section explaining how `applies-to-roles` filters concepts per app role
- Updated procedure step in "Score per chapter / property" to apply these filters before classifying

### 6.5 New file: book-extension-candidates.md

Create `docs/reference-implementation/book-extension-candidates.md` capturing the 19 primitives flagged for Volumes 1-extensions, 2, 3, 4 (items 9-27 in §5 above). This becomes the writing roadmap.

### 6.6 Commit + push

Single commit covering all six items above. Suggested message:

> `docs(reference-implementation): Path 1 polish — two-axis security + applies-to-roles + book-extension roadmap`

---

## 7. Step 3 — concrete tasks for Sunfish-repo executor

These run in `c:/Projects/Sunfish/`:

### 7.1 Rename existing variant

```bash
cd c:/Projects/Sunfish
git mv icm/pipelines/sunfish-gap-analysis icm/pipelines/sunfish-component-parity
# Update references in icm/_config/routing.md
# Update README inside the variant to clarify scope
```

### 7.2 Build two new variants

For each of `sunfish-local-first-conformance` and `sunfish-inverted-stack-conformance`:

- `pipelines/<variant>/README.md` — describe the variant's question and audience (use Sunfish's existing README format)
- `pipelines/<variant>/routing.md` — Stage 01 Discovery heavyweight (gap scoping); Stage 02 Architecture for "approved gap vs. roadmap item" decisions; otherwise standard 9-stage flow
- `pipelines/<variant>/deliverables.md` — what each stage produces; Stage 01 produces conformance report from the corresponding Claude skill

### 7.3 Build conformance-map.md

`icm/_config/conformance-map.md` with the schema from §3.2:

- `apps:` block for `anchor`, `bridge` (today); `mobile`, `kiosk`, `lan-hub` (placeholders)
- `deployments:` block for the in-scope scenarios from §4.1 + §4.2 (information systems + IoT)
- Per-concept role mapping (which app implements / which apps consume)
- Reference the engine-substitution-table for CRDT-engine alternatives

### 7.4 Build conformance-decisions.yaml

`icm/_config/conformance-decisions.yaml` with the structure from §1.5. Initial pass: scan baseline conformance reports, classify each gap as approved-gap / in-scope / deferred, record rationale.

### 7.5 Build engine-substitution-table.md

`icm/_config/engine-substitution-table.md` with CRDT-engine-bound concepts and Loro/Yjs/Automerge alternates (Sunfish today is YDotNet → Loro target per book Ch12).

### 7.6 Build validator

`tooling/conformance-map-validator/` (per Option C):

- Reads `conformance-map.md`
- Asserts every declared namespace exists in actual package layout (grep)
- Flags drift; integrates with `sunfish-{local-first,inverted-stack}-conformance` Stage 07 Review

### 7.7 Run baseline scans

```bash
# In a Claude Code session at c:/Projects/Sunfish/:
# Invoke local-first-properties skill (from this repo if shared, or installed to ~/.claude/skills/)
# Invoke inverted-stack-conformance skill
# Both write into icm/01_discovery/output/
```

Commit baseline reports as the first Stage 01 Discovery output. These become input to the first remediation sprint.

---

## 8. Open questions for executors

### 8.1 Scope of `applies-to-roles` defaults

When a concept has no explicit `applies-to-roles`, defaulting to "all roles" is permissive but may cause false-positive `missing` flags on roles where the concept doesn't truly apply. Alternative: default to a narrow set (just `full-node`) and require explicit additions. Trade-off: permissive default → more false positives; narrow default → more concept-tagging work.

**Recommendation:** permissive default (all roles). Tag explicit narrowing only where confidently determined. Tighten over time based on real conformance-run feedback.

### 8.2 Chain-of-custody concept addition

The commercial-driver scenario surfaced `attested-with-chain-of-custody` as an authenticity tier. The catalog has audit-log concepts but doesn't formalize multi-party signed transfer receipts. Two paths:

- Add to catalog now under `KEY-*` or new `CUST-*` prefix (small catalog change)
- Defer to future writing task (covered in Volume 1 extensions item 9)

**Recommendation:** defer to writing task. Document workaround in conformance scorer until Volume 1 extension lands.

### 8.3 Per-app conformance map vs. shared

For Sunfish today: one `conformance-map.md` covering both Anchor and Bridge, with per-app columns/sections. For larger ecosystems: per-app maps loaded by a shared deployment matrix.

**Recommendation:** start with one shared map. Split per-app only when one map exceeds 1000 lines or when teams need independent ownership.

### 8.4 Out-of-scope deployment reporting

For deployments that exceed catalog coverage (cyber-physical, multi-stakeholder economic, extreme environment), the report includes an `out-of-scope-primitives-required` section pointing to `book-extension-candidates.md`. Should this section also produce a "minimum viable extensions" recommendation (which Volume 1 extensions would unblock the most coverage)?

**Recommendation:** yes, in skill v1.1 — defer to second iteration of skills work after baseline experience.

### 8.5 CI integration

Sunfish is solo / pre-1.0; CI conformance-gating is not needed today. Note for future: when Sunfish reaches GA, consider adding a CI step that fails the build if conformance regresses below a per-app threshold (e.g., Anchor must stay above 80%).

**Recommendation:** noted for future; no action.

---

## 9. Decision-discussion provenance

This brief consolidates decisions from a multi-turn design discussion. Source turns include:

- Initial framing of conformance-map idea (response to "is there an LLM summary for the concepts in the book that can be used for gap analysis on the sunfish repo")
- Two-audience clarification (generic local-first vs. Inverted Stack-aligned)
- ICM integration discovery (Sunfish's existing 9-stage pipeline + `sunfish-gap-analysis` variant)
- Edge-case stress test (12 edge cases identified across skill behavior + ICM workflow)
- Refinement: app-vs-platform distinction; deployment matrix as first-class artifact
- Application-archetype brainstorm (Anchor + Bridge today; mobile + kiosk + lan-hub near-term; thin clients, legacy bridges, dev tools mid-term)
- POS deployment scenarios (restaurant + farmers market)
- IoT scenarios (weather station, commercial driver) → surfaced two-axis security model
- Smart meter + DePIN → surfaced delegated capability + cryptoeconomic security primitives
- Automotive + robotics → surfaced cyber-physical primitive cluster (Volume 2 territory)
- Spacecraft → surfaced DTN + asynchronous command authority (Volume 4 territory)
- Vending machines → confirmed fits existing kiosk + POS + headless-fleet hybrid
- Shared scooters + last-mile delivery robots → surfaced ephemeral-identity + geofence-enforcement + human-in-the-loop override (cross-volume additions, primitives #28-30)
- Office-of-authority transition + medical custody transfer + corporate acquisition → surfaced whole-system ownership transfer with persistent constraints (#31)
- Restaurant succession + trust-managed assets + multi-sig social recovery → surfaced succession arrangements with executor delegation (#32) + the key insight that capability OVER ownership is architecturally distinct from capability OVER use

The architecture has converged: 32 primitives across 4 volumes (with civic-governance + medical-systems + estate-planning as cross-cutting application domains); new scenarios either fit existing archetypes with calibration OR add to the cross-volume primitive list when genuinely novel. Time to execute.

---

## 10. Document maintenance

This document is **live design**, expected to evolve. Update when:

- A new architectural primitive is identified that doesn't fit any of the 27 in §5
- A new role is added to the taxonomy in §3.1
- A new app is added to the conformance-map in §3.2
- A scope decision changes (e.g., chain-of-custody moves from Volume 1 extension to in-catalog)
- An open question in §8 is resolved

Treat as the canonical design reference until artifacts are built; thereafter the artifacts become canonical and this document becomes historical context.
