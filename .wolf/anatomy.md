# anatomy.md

> Auto-maintained by OpenWolf. Last scanned: 2026-04-23T23:28:33.692Z
> Files: 59 tracked | Anatomy hits: 0 | Misses: 0

## ./

- `.gitattributes` — Git attributes (~20 tok)
- `.gitignore` — Git ignore rules (~72 tok)
- `ASSEMBLY.md` — Assembly Manifest (~725 tok)
- `book-structure.md` — BOOK-STRUCTURE (~5995 tok)
- `CLAUDE.md` — OpenWolf (~2262 tok)
- `CONTRIBUTING.md` — Contributing (~361 tok)
- `inverted-stack-book-plan.md` — The Inverted Stack — Book Writing Implementation Plan (~22768 tok)
- `LICENSE` — Project license (~204 tok)
- `Makefile` — Make build targets (~35 tok)
- `README.md` — Project documentation (~554 tok)
- `write_ch12_final.py` — -*- coding: utf-8 -*- (~557 tok)
- `write_ch12_script.py` — -*- coding: utf-8 -*- (~71 tok)

## .claude/

- `settings.json` (~441 tok)

## .claude/agents/

- `chapter-drafter.md` — Before You Draft (~1073 tok)
- `council-reviewer.md` — The Five Council Members (~3349 tok)
- `prose-reviewer.md` — The Book's Voice (~1197 tok)
- `research-assistant.md` — Primary Sources (always check these first) (~1073 tok)
- `technical-reviewer.md` — Source Material Locations (~742 tok)

## .claude/rules/

- `openwolf.md` (~313 tok)

## .github/ISSUE_TEMPLATE/

- `chapter.md` — Chapter (~359 tok)

## chapters/appendices/

- `appendix-a-sync-daemon-wire-protocol.md` — Appendix A — Sync Daemon Wire Protocol (~2,192 words, icm/draft: message framing, 5-message handshake HELLO/CAPABILITY_NEG/ACK, DELTA_STREAM, GOSSIP_PING, 7 error codes with retry semantics, QR onboarding payload, backward compatibility policy) (~2800 tok)
- `appendix-b-threat-model-worksheets.md` — Appendix B — Threat Model Worksheets (~2,198 words, icm/draft: asset inventory, actor taxonomy, construction PM worked example, key compromise IR template with re-keying procedure and notification script) (~2800 tok)
- `appendix-c-further-reading.md` — Appendix C — Further Reading (~1,248 words, icm/draft: 12 annotated entries across 5 sections — local-first foundations, CRDT libraries, distributed systems, production analogues, schema evolution) (~1800 tok)
- `appendix-d-testing-the-inverted-stack.md` — Appendix D — Testing the Inverted Stack (~2,531 words, icm/draft: five-level pyramid, CRDT growth tests, mandatory pre-release scenarios for partition/reconnect, schema migration, Flease edge cases, security, ledger, CI configuration guidance) (~3200 tok)
- `appendix-e-citation-style.md` — Appendix E — Citation Style (~729 tok)

## chapters/epilogue/

- `epilogue-what-the-stack-owes-you.md` — Epilogue — What the Stack Owes You (~2,203 words, icm/draft: 7 obligations, open questions, drift anti-patterns, what comes next, closing paragraph) (~2500 tok)

## chapters/front-matter/

- `foreword-placeholder.md` — Foreword (~146 tok)
- `preface.md` — Preface (~1614 tok)

## chapters/part-1-thesis-and-pain/

- `ch01-when-saas-fights-reality.md` — Chapter 1 — When SaaS Fights Reality (~6652 tok)
- `ch02-local-first-serious-stack.md` — Chapter 2 — Local-First: From Sync Toy to Serious Stack (~6926 tok)
- `ch03-inverted-stack-one-diagram.md` — Chapter 3 — The Inverted Stack in One Diagram (~5447 tok)
- `ch04-choosing-your-architecture.md` — Chapter 4 — Choosing Your Architecture (~5711 tok)

## chapters/part-2-council-reads-the-paper/

- `ch05-enterprise-lens.md` — Chapter 5 — The Enterprise Lens (~6266 tok)
- `ch06-distributed-systems-lens.md` — Chapter 6 — The Distributed Systems Lens (~5666 tok)
- `ch07-security-lens.md` — Chapter 7 — The Security Lens (~5461 tok)
- `ch08-product-economic-lens.md` — Who Is Jordan Kelsey (~5635 tok)
- `ch09-local-first-practitioner-lens.md` — Chapter 9 — The Local-First Practitioner Lens (~5971 tok)
- `ch10-synthesis.md` — Chapter 10 — Synthesis: What the Council Finally Agreed On (~4252 tok)

## chapters/part-3-reference-architecture/

- `ch11-node-architecture.md` — Chapter 11 — Node Architecture (~7353 tok)
- `ch12-crdt-engine-data-layer.md` — Chapter 12 — CRDT Engine and Data Layer (~7842 tok)
- `ch13-schema-migration-evolution.md` — Chapter 13 — Schema Migration and Evolution (~6500 tok) — icm/draft: expand-contract, lenses, epochs, runbook, failure modes
- `ch14-sync-daemon-protocol.md` — Chapter 14 — Sync Daemon Protocol (~7000 tok) — icm/draft: process isolation, 3-tier discovery, 5-step handshake, gossip anti-entropy, data minimization, Flease/lease coordination, reconnection storms, stale peer recovery
- `ch15-security-architecture.md` — Chapter 15 — Security Architecture (~5000 tok) — icm/draft: threat model, 4 defensive layers, DEK/KEK key hierarchy, role attestation flow, key compromise IR, offline revocation, in-memory key handling, supply chain, crypto-shredding, relay trust model
- `ch16-persistence-beyond-the-node.md` — Chapter 16 — Persistence Beyond the Node (~7000 tok) — icm/draft: five-layer storage, declarative sync buckets, lazy fetch/LRU eviction, snapshot rehydration, CRDT GC policy, three-state backup UX, disaster recovery, plain-file export

## chapters/part-4-implementation-playbooks/

- `ch17-building-first-node.md` — Chapter 17 — Building Your First Node (~3500 words) — icm/technical-review: Anchor clone/build, kernel wiring, CRDT document + two-device sync, QR onboarding wire format, SunfishNodeHealthBar UX, plugin registration
- `ch18-migrating-existing-saas.md` — Chapter 18 — Migrating an Existing SaaS (~3,500 words) — icm/draft: zone determination, Bridge Zone-C reference, 5 architectural decisions, 4 migration phases (shadow/local-writes/full-authority/backfill), phase gates, 5 failure modes, package availability table
- `ch19-shipping-to-enterprise.md` — Chapter 19 — Shipping to Enterprise (~3,229 words) — icm/draft: dual-license/CLA, MSIX/MSI+PKG packaging, code signing (macOS notarytool + Windows Authenticode/WDAC), MDM pre-seeded node-config.json schema, MDM compliance at capability negotiation, SBOM CycloneDX/Syft/Grype, CVE SLA, revocation CLI, air-gap three-posture config, three required runbooks
- `ch20-ux-sync-conflict.md` — Chapter 20 — UX, Sync, and Conflict (~3167 words) — icm/draft: complexity hiding standard, 3 status indicators, AP/CP table, optimistic write states, conflict inbox bulk resolution, 3 failure modes, first-run experience, non-technical trust gap

## docs/icm/

- `pipeline.md` — Book ICM Pipeline (~1346 tok)

## docs/style/

- `style-guide.md` — Unified Technical Writing Style Guide (~3038 tok)

## prospectus/

- `prospectus.md` — Book Prospectus (~4256 tok)

## source/

- `inverted-stack-v5.md` — The Inverted Stack v5.0 (~4757 tok)
- `kleppmann_council_review.md` — The Kleppmann Council — Charter, Personas & Scoring Templates (~7812 tok)
- `kleppmann_council_review2.md` — Kleppmann Council — Round 2 Review (~8735 tok)
- `local_node_saas_v13.md` — Inverting the SaaS Paradigm: A Local-Node Architecture for Collaborative Software (~13147 tok)

## templates/

- `chapter-council.md` — Chapter N — The [Domain] Lens (~484 tok)
- `chapter-playbook.md` — Chapter N — [Task] Your [Noun] (~414 tok)
- `chapter-reference.md` — Chapter N — Component Name (~409 tok)
- `chapter-standard.md` — Chapter N — Title (~187 tok)
