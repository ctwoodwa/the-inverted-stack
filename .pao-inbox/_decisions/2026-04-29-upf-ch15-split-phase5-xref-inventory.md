---
type: upf-phase-5-prep
date: 2026-04-29
author: PAO
audience: Yeoman (Phase 5 executor), CO, XO
parent-decision: 2026-04-29-upf-ch15-split.md
parent-triage: 2026-04-29-upf-ch15-split-triage.md
phase: 5 of 7 (pre-staged before Phase 3 executes)
status: inventory complete; mechanical edits queued for Phase 5
---

# UPF Ch15 Split — Phase 5 Cross-Reference Inventory

## TL;DR

**85 cross-references to Ch15 across 18 files** (excluding `ch15-security-architecture.md` itself). After the split, an estimated **~50 redirects to Ch22**, **~30 stay at Ch15**, **~5 require sentence-level rewrite** (mixed references citing both A and O topics in one phrase).

This inventory pre-stages Phase 5 of the UPF so it executes mechanically once Phase 3 (relocate sections) lands. Phase 5's own gate (`make lint` passes; zero broken refs) is achievable in a single editorial pass with this map.

## Distribution by file

| File | Refs | Dominant target after split |
|---|---:|---|
| `chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md` | 14 | Mostly Ch22 (UX counterparts to operational sections) |
| `chapters/appendices/appendix-f-regulatory-coverage.md` | 14 | Both — chapter-range entries need split into "Ch13–Ch15, Ch22" or similar |
| `chapters/appendices/appendix-g-glossary.md` | 12 | Mixed — `Specified in: Chapter 15 §X` per-entry classification |
| `chapters/appendices/appendix-b-threat-model-worksheets.md` | 9 | Mixed — KH/RAF→Ch15; KCIR/Endpoint/Chain-of-Custody→Ch22 |
| `chapters/part-5-operational-concerns/ch21-operating-a-fleet.md` | 8 | Mixed — KH/RAF→Ch15; CR/OR→Ch22 |
| `chapters/part-3-reference-architecture/ch16-persistence-beyond-the-node.md` | 8 | Mostly Ch22 (Event-Triggered Re-classification cross-refs) |
| `chapters/part-4-implementation-playbooks/ch17-building-first-node.md` | 3 | Ch15 (architectural primitives) |
| `chapters/part-3-reference-architecture/ch12-crdt-engine-data-layer.md` | 3 | TBD — read at Phase 5 execution |
| `chapters/part-2-council-reads-the-paper/ch10-synthesis.md` | 3 | TBD |
| `chapters/part-1-thesis-and-pain/ch04-choosing-your-architecture.md` | 2 | Ch15 (compliance framework, relay legal posture) |
| `chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md` | 2 | Ch15 (compliance framework) |
| `ch19-shipping-to-enterprise.md`, `ch18-migrating-existing-saas.md`, `ch14-sync-daemon-protocol.md`, `ch13-schema-migration-evolution.md`, `ch11-node-architecture.md`, `ch06-distributed-systems-lens.md`, `appendix-a-sync-daemon-wire-protocol.md` | 1 each | TBD per-line |

## Redirect rules (mechanical)

After Phase 3 relocates sections, apply these rules to update cross-refs. Each rule is a sed-friendly redirect; readers grep `Ch15 §<section name>` and route to the right chapter.

### Rule R-A — references that stay at Ch15 (architecture)

Pattern → unchanged target:

| `§<section name>` cited | Stays at | Note |
|---|---|---|
| `§Threat Model` | Ch15 | |
| `§Four Defensive Layers` (and sub-Layer references like `§Layer 1: Encryption at Rest`) | Ch15 | |
| `§Key Hierarchy` | Ch15 | Most-cited section; mainly from glossary + Ch21 |
| `§Role Attestation Flow` | Ch15 | |
| `§In-Memory Key Handling` | Ch15 | |
| `§Supply Chain Security` | Ch15 | |
| `§GDPR Article 17 and Crypto-Shredding` | Ch15 | |
| `§Relay Trust Model` | Ch15 | |
| `§Privacy-Preserving Aggregation at Relay` | Ch15 | |
| `§Security Properties Summary` | Ch15 | |

### Rule R-O — references that redirect to Ch22 (operational)

Pattern → new target (must update chapter number throughout):

| `§<section name>` cited | Redirects to | Notes |
|---|---|---|
| `§Key Compromise Incident Response` | Ch22 | |
| `§Key-Loss Recovery` (incl. sub-patterns 48a–48f, "Boundaries and Operator Mitigations") | Ch22 | High-volume — Ch20 has ~5 refs to this section |
| `§Offline Node Revocation and Reconnection` | Ch22 | |
| `§Collaborator Revocation and Post-Departure Partition` (incl. sub-patterns 45a–45f) | Ch22 | High-volume — Ch20 has ~3 refs to this section |
| `§Forward Secrecy and Post-Compromise Security` | Ch22 | |
| `§Endpoint Compromise: What Stays Protected` (incl. sub-patterns 47a, 47b) | Ch22 | |
| `§Chain-of-Custody for Multi-Party Transfers` | Ch22 | |
| `§Event-Triggered Re-classification` (incl. sub-patterns 10a–10d) | Ch22 | High-volume — Ch16 + Ch20 both reference |

### Rule R-G — generic "Chapter 15" references (no §section)

Re-read each in context to determine architectural vs operational topic:

| File:line pattern | Topic | Disposition |
|---|---|---|
| `ch04:204` (data-processing agreement, relay-operator legal posture) | Architectural — Relay Trust Model | Ch15 |
| `ch04:208` (supplemental controls; Appendix F details) | Architectural — compliance framework | Ch15 |
| `ch03:186` (compliance framework for third-party-veto) | Architectural | Ch15 |
| `ch03:188` (compliance framework for cross-jurisdiction sync) | Architectural | Ch15 |
| `ch14:267` (security architecture underpinning device-key auth + role attestation) | Architectural | Ch15 |
| `ch20:line w/ "rekeying flow"` | Architectural — Key Hierarchy | Ch15 |
| `ch20:line w/ "founder attestation — root trust anchor"` | Architectural — Role Attestation Flow | Ch15 |
| `appendix-b:175` ("architectural response is specified in Chapter 15") | Mixed; rewrite to point to either Ch15 §Threat Model or Ch22 §Endpoint Compromise depending on which threat the worksheet row addresses | Both — context-driven |
| `appendix-b:154` ("Ch 15 for relay deployment options") | Architectural — Relay Trust Model | Ch15 |
| `appendix-a:210` ("compelled-access and device-theft threat model Chapter 15 specifies") | Architectural — Threat Model | Ch15 |

### Rule R-N — numeric §refs (fragile post-split)

`appendix-b:148` cites `Ch 15 §7 for the in-memory key handling policy`. **Numeric §refs break post-split.** Yeoman replaces with named-section refs:

| Old (fragile) | New (resilient) |
|---|---|
| `Ch 15 §7` | `Ch15 §In-Memory Key Handling` |

PAO recommends a final pass with `grep -E "Ch ?15 §[0-9]" chapters/` after Phase 5 to catch any remaining numeric §refs. None should exist post-Phase-5.

### Rule R-F — Appendix F regulatory chapter ranges

14 entries in `appendix-f-regulatory-coverage.md` list chapters touching each regulatory framework. After split, regulatory content distributes:

- **Ch15 keeps** the §GDPR Article 17 and Crypto-Shredding section (architectural compliance mapping)
- **Ch22 absorbs** the operational compliance touchpoints (Chain-of-Custody for multi-party transfers, Key-Loss Recovery audit-trail, Collaborator Revocation audit-trail)

For most regulations, **both Ch15 and Ch22 touch the framework**. Update rule:

| Old listing | New listing | Notes |
|---|---|---|
| `Ch13–Ch15` | `Ch13–Ch15, Ch22` | when framework triggers operational flows |
| `Ch15` | `Ch15` or `Ch22` | depends on framework — read each entry |
| `Ch15, Appendix B` | `Ch15, Ch22, Appendix B` | when worksheets cite both A and O sections |

The reverse-index table at line 242 (`| Ch15 | DPDP, LGPD Art. 18, ...`) splits across Ch15 (architectural) + Ch22 (operational). Most listed regulations have crypto-shredding architecture obligation (→Ch15) AND erasure/audit operational obligation (→Ch22) — both rows present.

### Rule R-S — `<!-- Source: ... -->` HTML comments

`appendix-b:6` has `<!-- Source: v13 §11.1, Ch 15 -->` — a source-tracking comment, not user-visible content. Update to `<!-- Source: v13 §11.1, Ch15, Ch22 -->` for the appendix that references both architectural and operational material.

## Per-file disposition summary

### High-volume files (≥8 refs)

**`ch20-ux-sync-conflict.md` (14 refs).** Three operational pairings dominate: §Key-Loss Recovery (5 refs → all Ch22), §Collaborator Revocation (3 refs → all Ch22), §Event-Triggered Re-classification (3 refs → all Ch22). Plus 3 architectural refs (rekeying flow, founder attestation root trust anchor, Key Compromise Incident Response — last one is O so Ch22). Single mechanical redirect pass.

**`appendix-f-regulatory-coverage.md` (14 refs).** All 13 chapter-range entries plus 1 reverse-index row need the dual-target redistribution per Rule R-F. Per-regulation triage: GDPR (Ch15+Ch22 both — architectural compliance + erasure operational), HIPAA (Ch15 dominant), DPDP/LGPD/DIFC/POPIA/etc. (Ch15+Ch22 — same dual structure). Single mechanical pass with attention to which framework drives which sections.

**`appendix-g-glossary.md` (12 refs).** All `Specified in: Chapter 15 §<topic>` glossary footers. Mechanical per-line redirect using R-A or R-O. Specific entries:
- AES-256-GCM, Argon2, DEK, envelope encryption, HKDF, KEK, SQLCipher (7 entries) → §Key Hierarchy / §Layer 1 → Ch15
- HSM, TPM (2 entries) → §Endpoint Compromise → Ch22
- BAA, GDPR, HIPAA (3 entries) → mixed; Ch15 architecture + Ch22 operational

**`appendix-b-threat-model-worksheets.md` (9 refs).** Mix of architectural (Threat Model, In-Memory, Relay Trust, Key Hierarchy) and operational (Endpoint Compromise, Chain-of-Custody, Collaborator Revocation, Key Compromise IR). One numeric §ref (`§7`) needs Rule R-N treatment. Some sentence-level rewrites where a single sentence cites multiple sections of mixed type.

**`ch21-operating-a-fleet.md` (8 refs).** Five Ch15-target (Key Hierarchy + Role Attestation Flow — architectural), three Ch22-target (Collaborator Revocation, Offline Revocation — operational). Single pass.

**`ch16-persistence-beyond-the-node.md` (8 refs).** Most likely Event-Triggered Re-classification (operational — Ch22). Verify per line at execution.

### Lower-volume files (1–3 refs each)

Read each in Phase 5 execution; classifications above (Rule R-G) cover most patterns. Files with single refs are quick.

## Execution sequence (Phase 5 itself)

1. **Run `grep -rn -E "(Ch\.? *15|Chapter 15|chapter 15)" chapters/`** to confirm 85 hits remain (or fewer if Phase 3 already touched some).
2. **Apply R-A + R-O + R-N rules in a single pass** per file. Use the table above as the redirect map.
3. **Apply R-G rule** to generic references on a context-read basis.
4. **Apply R-F + R-S** to Appendix F and the source comment in Appendix B.
5. **Run `grep -E "Ch ?15 §[0-9]" chapters/`** to verify zero numeric §refs remain.
6. **Run `make lint`** — zero broken cross-references.
7. **Spot-check Ch20**, the heaviest cross-ref file, end-to-end for narrative coherence post-redirects.

Estimated execution time: 2–3 hours of mechanical editing + 1 hour spot-check. Most files are single-pass; Ch20 + Appendix F + Appendix G are the largest surfaces.

## Risk flags surfaced during inventory

1. **Numeric §refs (`§7`)** are fragile and PAO recommends a single-pass cleanup at Phase 5 to convert them all to named-section refs, regardless of split target. The split provides the trigger; future-proofing benefits regardless.
2. **Appendix F dual-coverage redistribution** is the highest-cognitive-load piece — each regulation's chapter range needs a per-framework decision. Likely benefits from a Yeoman+PAO pair-review pass rather than a pure mechanical sed.
3. **Sub-pattern numbering survives the split** (45b, 47a, 48a–f, 10a–d). The sub-patterns move with their parent sections; refs like `Ch15 §Collaborator Revocation sub-pattern 45b` become `Ch22 §Collaborator Revocation sub-pattern 45b`. Sub-pattern numbers do not renumber.
4. **`make lint` may not catch every break.** It detects broken cross-references against the chapter file structure. It will not catch a stale `Ch15 §X` that points to a now-Ch22 section if the section name still exists somewhere — gives a false PASS. PAO recommends a separate `grep -rn "Ch15 §<each O section name>"` post-Phase-5 to verify zero hits.

## Status

- Phase 5 inventory: COMPLETE.
- Phase 5 execution: BLOCKED on Phase 3 (Yeoman relocates sections) which is BLOCKED on audiobook pipeline window.
- Once Phase 3 lands, Phase 5 executes mechanically per this inventory.

---

**End of inventory.**
