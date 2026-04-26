# Book Extension Candidates — Architectural Primitives Beyond the Current Volume

**Status:** Writing roadmap, not implementation. Captures architectural primitives surfaced during the Path B design discussion (April 2026) that are NOT in the current book's 562-concept catalog but warrant inclusion in future writing — either Volume 1 extensions (this book, future editions) or new volumes (Volumes 2-5).

**Audience:** Future-author for chapter planning; conformance-skill consumers who need to know what's covered today vs. what's roadmapped; reviewers evaluating the book's architectural completeness.

**Source:** Decisions documented in `design-decisions.md` §5 (architectural primitives 9-48). The current book covers primitives 1-8 (Volume 1 core); this document tracks 9-48 as the writing roadmap.

---

## How to read this roadmap

Each entry maps a primitive identifier (matching `design-decisions.md` §5) to its target volume + suggested chapter slot + rough writing-effort estimate.

**Volume planning:**
- **Volume 1 extensions** = additions to the CURRENT book in a future edition. Things the book SHOULD address but doesn't yet.
- **Volume 2 — Cyber-physical systems** = potential new book covering local-first for automotive, robotics, smart-home actuators, medical devices, industrial control.
- **Volume 3 — Multi-stakeholder economic systems** = potential new book covering DePIN, smart meters, voting, governance, ownership transfer, redaction, compliance.
- **Volume 4 — Extreme environment systems** = potential new book covering spacecraft, drones, submarines, aviation.
- **Volume 5 — Long-now systems** = potential new book covering deep-time archives, multi-generational governance, mythic-depth artifacts. Splits into 5A (technical substrate) and 5B (governance and cognition).

**Effort estimates:**
- **S (small)** = ~1 chapter section, ~1-2k words
- **M (medium)** = ~1 full chapter, ~3-5k words
- **L (large)** = ~2-3 chapters or a new appendix, ~8-15k words
- **XL (extra-large)** = new book volume, ~50-80k words

---

## Volume 1 extensions (additions to current book in future editions)

These primitives apply to the book's current scope (information-systems local-first) but were missed in the original writing. Adding them to a future edition would close real gaps without expanding scope.

| # | Primitive | Suggested chapter slot | Effort |
|---|---|---|---|
| 9 | Chain-of-custody (multi-party signed transfer receipts, evidence-class temporal attestation) | New Ch15 section OR new Appendix G | M |
| 10 | Data-class escalation (event-triggered re-classification with retention/signing/custody upgrade) | New Ch20 section OR Ch15 extension | S-M |
| 11 | Fleet management (provisioning at flash time, fleet-scale key rotation, OTA updates, fleet observability) | New Ch19 section OR new chapter | M |
| 12 | Privacy-preserving aggregation (DP / k-anonymity at relay-side aggregation) | New Ch15 section OR new Appendix | M |
| 43 | Performance contracts with framework-level enforcement | New Ch11 section OR new Ch20 section | M |
| 44 | Per-data-class device-distribution policy | New Ch12 section OR new Ch16 section | S-M |
| 45 | Collaborator revocation and post-departure data partition | New Ch15 section + new Ch20 UX section | M |
| 46 | Forward secrecy + post-compromise security | New Ch15 section OR new Appendix B section | S-M |
| 47 | Endpoint-compromise threat model | New Ch15 section + Appendix B threat-actor entry | M |
| 48 | Key-loss recovery | New Ch15 section + new Ch20 UX section | M |

**Volume 1 extension total: 10 primitives.** A second-edition or "expanded" edition could plausibly add a new Part V (Operational and post-deployment concerns) covering all 10 in ~30-50k additional words.

---

## Volume 2 — Cyber-physical systems (potential new book)

These primitives apply when local-first software CONTROLS PHYSICAL ACTUATORS. Bug consequences move from data loss / disclosure to property damage / injury / death — qualitative jump from information-systems local-first.

| # | Primitive | Suggested chapter | Effort |
|---|---|---|---|
| 13 | Safety-critical real-time control (ISO 26262 / 13482 / IEC 61508) | Ch1 of V2 | L |
| 14 | Multi-decade hardware stewardship (15-50 year vehicle / aviation / spacecraft lifetimes) | Ch2 of V2 | L |
| 15 | Federated learning / model weights as CRDT data | Ch3 of V2 | L |
| 16 | Physical adversarial threat model (tampering, side-channels, V2X spoofing) | Ch4 of V2 | M |
| 17 | Human-machine trust calibration UX (handoff protocols) | Ch5 of V2 | M |
| 29 | Geofence enforcement as architectural primitive | Ch6 of V2 (or part of #13) | M |
| 30 | Human-in-the-loop override authority | Ch7 of V2 (paired with #17) | M |

**Volume 2 total: 7 primitives.** Plausible 8-12 chapter book covering automotive, robotics, smart-home actuators, medical devices, industrial control. ~70-90k words. **Effort: XL.**

---

## Volume 3 — Multi-stakeholder economic systems (potential new book)

These primitives apply when MULTIPLE INDEPENDENT PARTIES (with potentially divergent incentives) share a system. Trust, governance, ownership, and legal-compliance dimensions become first-class architectural concerns.

| # | Primitive | Suggested chapter | Effort |
|---|---|---|---|
| 18 | Delegated capability tokens | Ch1 of V3 | M |
| 19 | Cryptoeconomic security (stake/slash, sybil resistance) | Ch2 of V3 | L |
| 20 | Decentralized governance (DAO-style protocol upgrades) | Ch3 of V3 | L |
| 21 | Tokenization regulatory layer (Howey, MiCA, tax) | Ch4 of V3 | M |
| 22 | Hardware attestation primitives (TPM/SGX/Secure-Enclave) | Ch5 of V3 | M |
| 28 | Ephemeral identity / use-right tokens | Ch6 of V3 | S-M |
| 31 | Whole-system ownership transfer with persistent constraints | Ch7 of V3 | M |
| 32 | Succession arrangements with executor delegation | Ch8 of V3 | L |
| 33 | Compelled-access boundary (cryptographic vs. legal enforcement) | Ch9 of V3 | M |
| 34 | Compliance posture as architectural artifact | Ch10 of V3 | M |
| 35 | Legitimate-but-non-owner access | Ch11 of V3 | M |
| 36 | Redaction primitives (selective disclosure) | Ch12 of V3 | L |

**Volume 3 total: 12 primitives.** Plausible 12-15 chapter book covering DePIN, smart meters, voting systems, governance, ownership transfer, redaction, compliance. ~80-100k words. **Effort: XL.** This is likely the highest-leverage future volume — covers the most pressing real-world architectural patterns the current book doesn't address.

---

## Volume 4 — Extreme environment systems (potential new book)

These primitives apply when systems operate under extreme constraints (planet-scale latency, extreme dynamics, hostile-physical environments). Specialized but architecturally distinct.

| # | Primitive | Suggested chapter | Effort |
|---|---|---|---|
| 23 | Delay-tolerant networking (DTN / Bundle Protocol) | Ch1 of V4 | M |
| 24 | Highly-dynamic peer mesh (sub-second peer enter/exit) | Ch2 of V4 | M |
| 25 | Anonymity-preserving authenticity (voting, ZK proofs) | Ch3 of V4 | L |
| 26 | Mission-critical autonomy authority | Ch4 of V4 | M |
| 27 | Update-gating with multi-stakeholder approval | Ch5 of V4 | M |

**Volume 4 total: 5 primitives.** Plausible 6-8 chapter book covering spacecraft, LEO constellations, drones, submarines, aviation, voting systems. ~50-70k words. **Effort: L-XL.** Could also be packaged as 2-3 long appendices to V1 or V3 rather than standalone book.

---

## Volume 5 — Long-now systems (potential new book; splits 5A + 5B)

The 10,000-year timespan problem. Splits cleanly into TWO sub-clusters that work together but address orthogonal failure modes.

### Volume 5A — Technical substrate (data + custody + semantics survive)

| # | Primitive | Suggested chapter | Effort |
|---|---|---|---|
| 37 | Long-horizon format + media stability | Ch1 of V5 | L |
| 38 | Multi-generational custody and governance | Ch2 of V5 | L |
| 39 | Deep-time semantics | Ch3 of V5 | L |

### Volume 5B — Governance and cognition (decisions consider the long horizon)

| # | Primitive | Suggested chapter | Effort |
|---|---|---|---|
| 40 | Long-horizon decision governance | Ch4 of V5 | L |
| 41 | Mythic-depth artifacts and narrative continuity | Ch5 of V5 | M-L |
| 42 | Optionality preservation across generations | Ch6 of V5 | M-L |

**Volume 5 total: 6 primitives across 2 sub-clusters.** Plausible 8-10 chapter book at the intersection of architecture, governance theory, and Long Now Foundation framing. ~60-80k words. **Effort: XL.** Highly speculative / aspirational — would be more philosophy + architecture than implementation guide.

---

## Cross-cutting application domains (not primitives, but writing audiences)

Several primitives apply across multiple domains that warrant their own chapter-length treatment OR appendix coverage:

- **Civic-governance** — applies to #20, #31, #32, #33, #34, #35, #36, #38, #40
- **Medical-systems** — applies to #31, #34, #36
- **Estate-planning** — applies to #32, #38
- **Financial-systems** — applies to #21, #22, #34
- **Journalist-source-protection** — applies to #25, #33, #36
- **Dissident-protection** — applies to #25, #33, #36, #38
- **Research-ethics** — applies to #36, #41
- **Civic-archives** — applies to #37, #38, #39, #40
- **Cultural-heritage** — applies to #38, #39, #41
- **Scientific-data** — applies to #37, #38, #39
- **Family-genealogy** — applies to #37, #38
- **Indigenous-knowledge-preservation** — applies to #38, #39, #41
- **Climate-policy** — applies to #40, #42
- **Sovereign-finance** — applies to #40, #42

A future book or appendix series could organize content by application domain rather than by primitive, providing depth-first coverage of each domain's specific architectural needs.

---

## Total writing investment estimate

If all roadmap items were fully written:

- **Volume 1 second edition** (10 extensions added to current book): ~30-50k additional words
- **Volume 2** (cyber-physical): ~70-90k words
- **Volume 3** (multi-stakeholder economic): ~80-100k words (highest leverage)
- **Volume 4** (extreme environment): ~50-70k words
- **Volume 5** (long-now): ~60-80k words

**Grand total writing investment: ~290-390k additional words across 4-5 books.** This represents roughly 4-5 years of focused writing at the pace of *The Inverted Stack* (which took ~83k words and ~18 months including review cycles).

---

## Prioritization signals

Based on real-world deployment scenarios captured in `design-decisions.md` §4:

**Highest-priority Volume 1 extensions** (close gaps in existing scope):
1. **#48 Key-loss recovery** — most common P7 failure mode in real deployments; affects every consumer scenario
2. **#43 Performance contracts** — most common reason "local-first feels slow" critique lands
3. **#45 Collaborator revocation** — most common P4+P7 gap when departing-employee / divorce scenarios surface
4. **#11 Fleet management** — required for any organization deploying Sunfish at scale

**Highest-priority new volume to write**:
- **Volume 3 (multi-stakeholder economic)** — covers the most pressing real-world architectural patterns (DePIN, smart meters, voting, governance, ownership transfer, redaction, compliance). 12 primitives, broadest applicability.

**Aspirational / lowest urgency**:
- **Volume 5 (long-now systems)** — important but speculative; existing Ch16 + epilogue + Appendix C cover the philosophy adequately for current audience. Volume 5 would be a separate intellectual project rather than an immediate practitioner need.

---

## Document maintenance

This roadmap is **live planning**, expected to evolve as:

- New deployment scenarios surface new primitives (add to relevant Volume)
- Writing happens (mark items as "in V1 §X.Y" or "shipped in V2 Ch3" as appropriate)
- Prioritization shifts based on user feedback or implementation experience

Treat as the canonical writing roadmap until the next book volume is published; thereafter the published book becomes canonical and this document tracks the next-volume roadmap.
