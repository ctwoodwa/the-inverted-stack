# Memory

> Chronological action log. Hooks and AI append to this file automatically.
> Old sessions are consolidated by the daemon weekly.
| 2026-04-24 | Appendix D pass-1 resolution (6.3 POLISH → 5 priority items) | chapters/appendices/appendix-d-testing-the-inverted-stack.md | Opening stakes hook added; 4 CRDT properties as bulleted list + state-based vs op-based commutativity qualifier + Shapiro citation; 10,000-sequence rationale stated; Level 4 MVP harness design spec (4 components + 1-3 engineer-week estimate); Level 5 chaos tooling named (Pumba/Gremlin/toxiproxy); NEW scenarios added — Extended-offline-baseline 90 days, Abrupt-power-interruption WAL SIGKILL, Air-gapped 30-day, Historical-document-re-keying, Data-boundary-relay-disabled (Schrems II/DIFC/RBI/NDPR/PIPL/242-FZ), Relay-operator-cannot-decrypt (state-actor threat model), Attestation-validation-and-revocation, Audit-trail-completeness (Japan PIPA/Korea ISMS-P/PIPL/SOX/HIPAA); Low-resource-variant (2 GB RAM / 16 GB storage); Regulatory citations parenthetical per security scenario; Section 4 restructured as CI tier table (Tier/Levels/Trigger/Time budget/Severity/Purpose); Test artefact capture requirements (test report/evidence/harness config/SBOM); Accessibility announcement testing (WCAG 2.1 AA / EU EAA 2025 / Section 508 / UK Equality Act); 3,663 words | ~6000 |
| 2026-04-24 | Appendix C pass-1 resolution (4.3 REVISE → 5 priority items) | chapters/appendices/appendix-c-further-reading.md | Expanded from 12 entries / 5 sections to 38 entries / 9 sections. New Section 4 Cryptography (Noise RFC 34, SQLCipher, libsodium, Argon2id RFC 9106, Ed25519 RFC 8032); new Section 5 Regulatory primary sources (GDPR, Schrems II C-311/18, DPDP 2023, PIPL, Japan PIPA, Korea PIPA + ISMS-P, UAE DPL + DIFC DPL, POPIA + NDPA, LGPD, 242-FZ); new Section 8 Vendor Dependency Case Studies (2022 CIS terminations composite); new Section 9 Reference Implementation (Sunfish repo + ADR pointers). Section 3 expanded with Raft (Ongaro-Ousterhout USENIX ATC 2014), Brewer CAP PODC 2000, Gilbert-Lynch SIGACT 2002, Saito-Shapiro ACM CS 2005, Lamport CACM 1978. Section 6 production analogues: Linear URL anchored to "Scaling Linear sync engine" post, M-PESA, FarmerLine, Nubank, CouchDB/PouchDB added. CRDT platform note (Android/Kotlin + .NET alongside JS). Cambria annotation tightened (practitioner-action leading). 3,288 words | ~6000 |
| 2026-04-24 | Appendix B pass-1 resolution (5.9 REVISE → 5 priority items) | chapters/appendices/appendix-b-threat-model-worksheets.md | Regulatory disclaimer expanded (7 regions, ~30 frameworks inc. GDPR/Schrems II/UAE DPL/DIFC/DPDP/PIPL/Japan PIPA/Korea PIPA/POPIA/NDPR/242-FZ/LGPD); breach notification deadline table split from 90-day retention (GDPR 72h, PIPL 3d, Korea 24h, etc.); Statutory-compulsion actor added (compelled-access threat model with jurisdiction list); Relay-termination-by-policy actor; Compromised IdP actor; "Former team member" capability corrected (key rotation limits future access only); KEK-unavailable Step 1a branch added; OS keystore evaluation prompt (Windows+TPM/macOS Secure Enclave/Linux libsecret/Android/iOS); MDM expanded (Intune/Jamf/SOTI/MaaS360/Ivanti); Audit log completeness record asset (Japan/Korea); Supply chain attack branch; Power interruption + lawful access detection items; user notification template active-voice; Ch15+Ch19 workflow positioning; cold-boot attack grounded; 3,153 words | ~5500 |
| 2026-04-24 | Appendix A pass-1 resolution (6.46 REVISE → 5 priority items) | chapters/appendices/appendix-a-sync-daemon-wire-protocol.md | Positioning statement + Noise_XX transport layer + 4 MiB rationale; state machine Mermaid diagram (CONNECTING→NOISE→CBOR→STREAMING→ERROR/CLOSED); ACK negotiated_version field; Deterministic CBOR (RFC 8949 §4.2) required for signed fields; vector_clock key encoding clarified (64-char hex tstr); op_type/payload mismatch detection; protocol_version uint vs semver reconciled; Ed25519 RFC 8032 + FIPS 186-5 + GOST R 34.10-2012 constraint; bearer-credential security properties + replay protection via Noise; personal-data note (9 jurisdictions); YDotNet snapshot format reference; §A.8 Conformance (16 REQ-A-NNN); §A.9 Test Vectors stub; 3,951 words | ~6000 |
| 2026-04-24 | Epilogue pass-1 resolution (6.1 REVISE → 5 priority items) | chapters/epilogue/epilogue-what-the-stack-owes-you.md | Preface-promise loop closed (4 commitments named as delivered), "What Comes Next" replaced with Week 1/Month 1/First enterprise pitch reader-action sequence, regulatory geography expanded (GDPR/Schrems II/DPDP/UAE DPL/PIPL/Japan PIPA/Korea PIPA/POPIA/NDPR/242-FZ/LGPD in Article 17 paragraph), 2022 CIS terminations added as evidentiary anchor, GDPR Article 17 crypto-shredding qualified (CNIL/German DPAs pending), drift irreversibility softened to empirical pattern; "dependency for agency" moved closer to final beat; 3,014 words | ~5000 |
| 2026-04-24 | Preface pass-1 resolution (5.6 REVISE → 5 priority items) | chapters/front-matter/preface.md | "Why I Wrote This" expanded with personal texture + concrete Round 1 redesign example + 15 conditions framing; regulatory signal broadened (GDPR/Schrems II/UAE DPL/DIFC DPL/DPDP/POPIA/NDPR/Japan PIPA/Korea PIPA); offline reframed as baseline for Sub-Saharan Africa/rural India/LatAm/SE Asia; three closing notes consolidated to one "Note on the Reference Implementation"; Kleppmann Council methodology note removed; new closing paragraph names four deliverables; 2022 CIS terminations added to opening; 1,217 words | ~5000 |
| 2026-04-24 | Ch20 final polish — 5 priority items from pass-1 board review (5.9 REVISE) | chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md | Accessibility section added (ARIA contracts, IUiBlockManifest, ISunfishIconProvider), Ch15 revocation UX message, SunfishOptimisticButton/SunfishConflictList/SunfishFreshnessBadge named, Non-Technical Trust Gap reframed as "UX for the Non-Technical Adopter", full-offline reframed for rural deployments, Unexpected Shutdown failure mode added, regulated-market backup target validation (242-FZ, DPDP, DPL 2022); 3,966 words | ~5000 |
| 20:19 | Drafted Chapter 13 Schema Migration and Evolution | chapters/part-3-reference-architecture/ch13-schema-migration-evolution.md | 4144 words, committed to main | ~8000 |
| 06:58 | Applied 8 literary board priority edits to Ch01 | chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | all 8 edits applied, 4702 words (within ±10% of 4500 target), committed | ~4500 |
| 09:45 | Applied Barker editorial review to Ch11: relay governance paragraph, Flease quorum formula + partition failure mode, Schrems II callout + citation [2] | chapters/part-3-reference-architecture/ch11-node-architecture.md | ~230 words added, committed to main | ~3500 |
| prose-review | Style enforcement pass on Part II (Ch05–Ch10) — fixed there-is openers, passive voice, weak verbs, throat-clearing, restatement duplicates; fixed one Edit-induced duplication in ch07 | ch05–ch10 enterprise/distributed/security/product/practitioner/synthesis | ~45 targeted edits across 6 files | ~12000 |
| session | Resolved 40 technical-review markers in ch17 | chapters/part-4-implementation-playbooks/ch17-building-first-node.md | All CLAIM/SUNFISH-API/PACKAGE markers removed; ICM advanced to icm/technical-review | ~6000 |
| 2026-04-24 | Prose review appendix-b + appendix-d | chapters/appendices/appendix-b*.md, appendix-d*.md | 20+ edits applied; both advanced to icm/prose-review; committed c84c2cc | ~4000 |
| 2026-04-24 | Authorial voice fix Ch17 — 2-sentence Marcus callback opens Section 1 | chapters/part-4-implementation-playbooks/ch17-building-first-node.md | committed 06fe3cf | ~800 |
| 2026-04-24 | Fixed citation errors appendix-c | chapters/appendices/appendix-c-further-reading.md | Flexible Paxos authors corrected; fabricated co-author removed; YDotNet/Loro language fixed; ICM to icm/technical-review | ~3000 |
| 2026-04-24 | Prose review ch17, appendix-c, preface | ch17 + appendix-c + preface | Three prose review agents launched; awaiting completion | ~2000 |
| 2026-04-24 | Style-guide compliance pass on preface + Ch01–Ch04 | preface.md, ch01–ch04 | 6 targeted edits: 1 ch01, 2 ch02, 1 ch03, 2 ch04; no changes to preface | ~6000 |
| 2026-04-24 | Style-enforcer pass on Ch17–Ch20 | ch17, ch18, ch19, ch20 | 12 targeted edits across 4 files: passive voice, scaffolding, weak verbs, throat-clearing | ~8000 |
| 2026-04-24 | Style enforcer prose pass: preface + Ch01–Ch04 | preface.md, ch01–ch04 | 3 style edits (ch01: contraction, passive voice); encoding repair on ch03 (43 double-encoded UTF-8 sequences fixed) | ~9000 |
| 2026-04-24 | Style enforcement pass: epilogue + 5 appendices | epilogue, appendix-a through appendix-e | 3 edits total: 2 in epilogue (there-is + weak value-of construction), 1 in appendix-c (there-is); all other files clean | ~5000 |
| 2026-04-24 | Style-guide compliance pass on Ch17–Ch20, Epilogue, Appendices A–D | 9 files | 9 edits total: ch17(2), ch18(3), ch19(0), ch20(2), epilogue(2), appendix-a(0), appendix-b(0), appendix-c(0), appendix-d(0) | ~7000 |
| 2026-04-24 | Style-guide compliance pass on Ch05–Ch10 (Part 2) | ch05–ch10 | 9 targeted edits: 6 ch05, 1 ch06, 1 ch07, 0 ch08, 0 ch09, 1 ch10; there-is openers, passive voice, restatements | ~8000 |
| 2026-04-24 | Style-guide compliance pass on Part III Ch11–Ch16 | ch11–ch16 (part-3-reference-architecture) | 7 targeted edits across 5 files; ch11 and ch12 needed no changes | ~9000 |
| 23:45 | Drafted Appendix D — Testing the Inverted Stack | chapters/appendices/appendix-d-testing-the-inverted-stack.md | 2531 words, committed 2ba0d8c | ~5500 |
| 23:45 | Wrote Appendix C — Further Reading | chapters/appendices/appendix-c-further-reading.md | 1248 words, 12 annotated entries, 5 sections, committed 18548fd | ~3500 |
| 23:45 | Drafted Chapter 19 Shipping to Enterprise | chapters/part-4-implementation-playbooks/ch19-shipping-to-enterprise.md | 3229 words, committed ad3e030 | ~6500 |
| 2026-04-23 | Drafted Chapter 18 — Migrating an Existing SaaS | chapters/part-4-implementation-playbooks/ch18-migrating-existing-saas.md | 3139 words, committed 70b60ac | ~6000 |
| 23:45 | Drafted Chapter 17 Building Your First Node | chapters/part-4-implementation-playbooks/ch17-building-first-node.md | 3532 words, committed 9ecb667 | ~9000 |
| 23:35 | Drafted Chapter 15 Security Architecture | chapters/part-3-reference-architecture/ch15-security-architecture.md | 3656 words, committed e539be1 | ~7500 |
| 23:45 | Drafted Chapter 14 Sync Daemon Protocol | chapters/part-3-reference-architecture/ch14-sync-daemon-protocol.md | 3474 words, committed 8bdf2f5 | ~7000 |
| 01:08 | drafted Chapter 16 — Persistence Beyond the Node | chapters/part-3-reference-architecture/ch16-persistence-beyond-the-node.md | committed 445429b, 3,278 words | ~7000 |
| 21:34 | draft: Chapter 20 — UX, Sync, and Conflict | chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md | 3167 words committed at 7e0a9b6 | ~3800 tok |
| 21:39 | drafted epilogue | chapters/epilogue/epilogue-what-the-stack-owes-you.md | committed ca5caed, 2203 words | ~2500 |
| 21:43 | wrote Appendix A — Sync Daemon Wire Protocol | chapters/appendices/appendix-a-sync-daemon-wire-protocol.md | committed 6517d17, 2192 words | ~2800 |
| 21:44 | Drafted Appendix B — Threat Model Worksheets | chapters/appendices/appendix-b-threat-model-worksheets.md | 2198 words, committed 95eb981 to main | ~3500 |

| 22:15 | Technical review of ch05-ch10 (Part II council chapters) | chapters/part-2-council-reads-the-paper/*.md | 3 CLAIM markers inserted (ch05 Voss verdict, ch07 Okonkwo verdict, ch09 five-blocks claim); all other technical claims verified against R1/R2/v13/v5 | ~18000 |

| 22:16 | Technical review of Ch01-Ch04 (Part I) — 4 CLAIM flags inserted across ch02 and ch03 | chapters/part-1-thesis-and-pain/ | FAIL (4 flags) | ~12000 || 22:26 | technical-review: ch17/ch18/ch19/ch20/epilogue/appendices — 11 flags inserted | chapters/part-4-implementation-playbooks/*.md, chapters/appendices/appendix-a*.md, chapters/appendices/appendix-c*.md | 6 TFM/package/API flags in ch17; 4 API flags in ch18; 3 flags in ch19; 1 transport flag in appendix-a; 1 citation flag in appendix-c | ~18000 |
| 03:39 | prose review wave 3 committed | ch01/02/05/07/15/20 | 6 files, 53 lines cut | ~3000 |
| 03:47 | technical-review ch12: applied 6 flag markers (IStreamDefinition CP claim, Yjs superlative, loro-cs state, ICrdtEngine.OpenOrCreateAsync invented API, IPostingEngine.PostAsync/Posting invented signatures, three-tier GC tier naming) | chapters/part-3-reference-architecture/ch12-crdt-engine-data-layer.md | FAIL — 6 flags inserted | ~8000 |
| 03:52 | technical review ch11-node-architecture.md | chapters/part-3-reference-architecture/ch11-node-architecture.md | 2 CLAIM flags inserted: DACL claim (unverifiable), SyncState package assignment (factual error) | ~8000 tok |

| 2026-04-24 | Session: QC-1 word count fixes (ch12/ch13/ch17), ch13 technical accuracy (lens package attribution), ch14 technical review in progress | ch12, ch13, ch17, ch11, appendix-c | committed 5045373, 5c19915 | ~25000 |
| 04:13 | technical-reviewer: reviewed ch14-sync-daemon-protocol.md against v13 §6, Sunfish kernel-sync | chapters/part-3-reference-architecture/ch14-sync-daemon-protocol.md | 5 flags inserted (2 error-code/behavior, 1 ACK silent-omission, 2 package not found); FAIL | ~4500 |
| 04:22 | technical-review ch15 | chapters/part-3-reference-architecture/ch15-security-architecture.md | FAIL — 2 CLAIM flags + 1 SUNFISH-API flag inserted; Argon2id vs HKDF-SHA256 discrepancy and relay tooling not in Sunfish.Kernel.Security | ~8500 |
| 04:23 | Technical review of ch16-persistence-beyond-the-node.md | chapters/part-3-reference-architecture/ch16-persistence-beyond-the-node.md | 6 CLAIM/PACKAGE flags inserted; FAIL verdict | ~9000 |
| 04:31 | technical-review ch18 | chapters/part-4-implementation-playbooks/ch18-migrating-existing-saas.md | 8 comment markers inserted (4 CLAIM, 1 SUNFISH-API, 1 NOTE, 2 PACKAGE-NAME); FAIL verdict | ~18000 |
| 04:xx | Technical review of Ch19 Shipping to Enterprise | chapters/part-4-implementation-playbooks/ch19-shipping-to-enterprise.md | 6 CLAIM markers inserted; FAIL verdict | ~8000 |
| 2026-04-24 | Technical accuracy review + fixes: ch11-ch16 Part III | chapters/part-3-reference-architecture/*.md | ch11(icm/prose-review), ch12(icm/prose-review), ch13(icm/prose-review), ch14(icm/prose-review), ch15(icm/prose-review), ch16(icm/prose-review) — fixed lens package attribution, YDotNet package, SQLCipher key derivation, ACK denied array, Sunfish.Foundation.LocalFirst refs | ~25000 |
| 2026-04-24 | Technical review + fixes: ch18 Migrating Existing SaaS | chapters/part-4-implementation-playbooks/ch18-migrating-existing-saas.md | Fixed 3 code blocks with invented method signatures; added // illustrative markers; icm/prose-review | ~8000 |
| 2026-04-24 | QC-1 word count fixes: ch12, ch13, ch17, appendix-a, appendix-c | multiple | All chapters now within ±10% of target | ~5000 |
| 2026-04-24 | ICM marker applied to all 30+ chapters | multiple | Part II: icm/prose-review; Part III: icm/prose-review (after review); Part IV: icm/draft or icm/prose-review | ~2000 |
| 04:41 | prose-review pass on ch15, ch16, ch18 | ch15-security-architecture.md, ch16-persistence-beyond-the-node.md, ch18-migrating-existing-saas.md | 4 edits to ch15 (Layer3 restatement, 'temporarily unable', relay verb, citation renumber), 5 edits to ch16 (throat-clearing, 'acknowledges', hedged phrasing, re-intro removal, summary flag), 5 edits to ch18 ('needs'->'requires', academic framing, metric flag, Part IV re-explain flag, greenfield dupe flag) | ~12000 tok |
| 04:47 | technical-reviewer: reviewed appendix-b-threat-model-worksheets.md against v13 �11, v5 �4, Sunfish repo | chapters/appendices/appendix-b-threat-model-worksheets.md | 2 flags inserted (storageEncryption invented field, cold-boot zeroing claim unsourced) | ~4500 |
| 04:49 | prose-review Ch19 + Ch20 | ch19-shipping-to-enterprise.md, ch20-ux-sync-conflict.md | 5 edits Ch19, 7 edits Ch20; both MINOR grade | ~6500 tok |
| 04:49 | prose-review: applied 8 epilogue + 3 appendix-a inline edits (throat-clearing, author intrusion, restatements, agency) | epilogue-what-the-stack-owes-you.md, appendix-a-sync-daemon-wire-protocol.md | 11 edits applied, all verified | ~4200 |
| 04:51 | Technical review of appendix-d-testing-the-inverted-stack.md — 6 CLAIM markers inserted, 0 SUNFISH-API flags, 0 PACKAGE flags | chapters/appendices/appendix-d-testing-the-inverted-stack.md | FAIL (6 flags) | ~18000 |
| 05:01 | Prose review fixes: Part I ch01-ch04, Part II ch05-ch10, ch19-ch20, epilogue, appendix-a/b/d. Technical review fixes: appendix-b (2 claims), appendix-d (6 editorial → qualified). Committed. | multiple | applied and committed | ~12000 |
| 05:01 | ch17 technical review: 40 flags (11 CLAIM, 28 SUNFISH-API, 1 PACKAGE). Fix agent launched (abb88b00b8f809ac9). Prose review agents for appendix-b/d and technical review for appendix-c also launched. | ch17, appendix-b, appendix-c, appendix-d | in progress | ~3000 |
| 05:12 | technical-review: appendix-c-further-reading.md — flagged 19 CLAIM markers across 12 entries; [9] author list is hard factual error (wrong Flexible Paxos authors); [3]/[4] contradict ADR 0028 on Yjs-vs-Loro primary | chapters/appendices/appendix-c-further-reading.md | CLAIM markers written inline | ~6000 |
| 05:21 | prose-review: appendix-c-further-reading.md — 8 fixes applied, ICM advanced to icm/prose-review | chapters/appendices/appendix-c-further-reading.md | complete | ~1800 tok |
| 09:15 | Prose review pass on preface.md — 7 fixes applied, ICM advanced to prose-review | chapters/front-matter/preface.md | done | ~2800 tok |
| 05:25 | Prose review pass on ch17 — 8 fixes applied (passive voice, paragraph splits, restatements, synonym cycling, There-constructions, re-introduction, weak verbs) | chapters/part-4-implementation-playbooks/ch17-building-first-node.md | ICM advanced to prose-review | ~3500 tok |
| 2026-04-24 | QC-1 word count expansions: ch16, ch17, ch19, epilogue | ch16 (2949→3556), ch17 (3520→3910), ch19 (3148→3481), epilogue (2219→2488) | all four now PASS QC-1; corrected fabricated plugin lifecycle claims (OnUnloadAsync, no faulted-continue, no version validation) | ~12000 |
| 2026-04-24 | Automated pipeline complete | All 27 chapters at icm/prose-review; 27/28 pass QC-1 (preface 926/1300 is human-only); running total ~81,900 words vs ~83,500 target | Pipeline blocked on icm/voice-check (human stage); preface expansion and foreword still needed | ~5000 |
| 06:16 | prose-review style pass: Part III Ch11–Ch16, fixed there-is openers, hedges, weak verbs, passive, restatements | ch11-node-architecture.md ch12-crdt-engine-data-layer.md ch13-schema-migration-evolution.md ch14-sync-daemon-protocol.md ch15-security-architecture.md ch16-persistence-beyond-the-node.md | ~30 targeted edits applied | ~12000 |
| 06:44 | Expanded literary-board to 11 global critics: Reyes (LATAM/accessibility), Tanaka (APAC/Japan), Barker (Europe/Germany), Diallo (Africa) | .claude/agents/literary-board.md | committed 3bdfd33 | ~8000 |
| 07:07 | Applied Hollis findings: Ch10 verdict-reveal fix + bridge passage, Ch17 voice restoration | ch10-synthesis.md, ch17-building-first-node.md | committed 754defa + 06fe3cf | ~6000 |
| 07:32 | Applied remaining Hollis findings: Ch17/Ch12 implementation-state cleanup, Ch01 final polish (Marcus representativeness, Quip, closing handoff) | ch17, ch12, ch01 | committed 2142073 + 139e856 | ~5000 |
| 08:10 | Edited .claude/agents/literary-board.md | inline fix | ~196 |
| 08:10 | Edited .claude/agents/literary-board.md | inline fix | ~59 |
| 08:15 | Edited .claude/agents/literary-board.md | modified substitution() | ~1300 |
| 08:16 | Edited .claude/agents/literary-board.md | 2→2 lines | ~54 |
| 08:16 | Edited .claude/agents/literary-board.md | 5→5 lines | ~98 |
| 08:16 | Edited .claude/agents/literary-board.md | expanded (+10 lines) | ~189 |
| 08:16 | Edited .claude/agents/literary-board.md | 3→4 lines | ~88 |
| 08:17 | Session end: 7 writes across 1 files (literary-board.md) | 1 reads | ~10289 tok |
| 08:21 | Session end: 7 writes across 1 files (literary-board.md) | 1 reads | ~10289 tok |
| 08:24 | Session end: 7 writes across 1 files (literary-board.md) | 1 reads | ~10289 tok |

## Session: 2026-04-24 08:29

| Time | Action | File(s) | Outcome | ~Tokens |
|------|--------|---------|---------|--------|
| 09:09 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | inline fix | ~8 |
| 09:09 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | inline fix | ~10 |
| 09:09 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | inline fix | ~124 |
| 09:09 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | expanded (+12 lines) | ~920 |
| 09:10 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | inline fix | ~39 |
| 09:10 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | inline fix | ~8 |
| 09:10 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | expanded (+14 lines) | ~1563 |
| 09:11 | Edited book-structure.md | 2→2 lines | ~32 |
| 09:11 | Edited book-structure.md | 7→8 lines | ~147 |
| 09:11 | Edited book-structure.md | 2→2 lines | ~18 |
| 09:11 | Edited book-structure.md | inline fix | ~13 |
| 09:11 | Edited book-structure.md | inline fix | ~8 |
| 09:12 | Created ../../Users/Chris/.claude/projects/C--Projects-the-inverted-stack/memory/project_failure_mode_taxonomy.md | — | ~449 |
| 09:12 | Edited ../../Users/Chris/.claude/projects/C--Projects-the-inverted-stack/memory/MEMORY.md | 1→2 lines | ~98 |
| 09:12 | Session end: 14 writes across 5 files (ch01-when-saas-fights-reality.md, ch03-inverted-stack-one-diagram.md, book-structure.md, project_failure_mode_taxonomy.md, MEMORY.md) | 4 reads | ~3683 tok |

## Session: 2026-04-24 09:15

| Time | Action | File(s) | Outcome | ~Tokens |
|------|--------|---------|---------|--------|
| 09:24 | Edited reviews/2026-04-24-literary-board-reviews.md | expanded (+106 lines) | ~2689 |
| 09:24 | Session end: 1 writes across 1 files (2026-04-24-literary-board-reviews.md) | 5 reads | ~17282 tok |
| 09:32 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | 3→3 lines | ~148 |

## Session: 2026-04-24 09:34

| Time | Action | File(s) | Outcome | ~Tokens |
|------|--------|---------|---------|--------|
| 09:35 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | inline fix | ~57 |
| 09:35 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | inline fix | ~101 |
| 09:36 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | inline fix | ~89 |
| 09:36 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | inline fix | ~19 |
| 09:36 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | 3→5 lines | ~274 |
| 09:36 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | removed 3 lines | ~12 |
| 09:36 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | inline fix | ~104 |
| 09:36 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | inline fix | ~207 |
| 09:36 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | 3→5 lines | ~297 |
| 09:37 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | 3→5 lines | ~175 |
| 09:37 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | removed 3 lines | ~7 |
| 09:37 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | removed 3 lines | ~6 |
| 09:37 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | removed 3 lines | ~9 |
| 09:37 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | inline fix | ~15 |
| 09:37 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | inline fix | ~81 |
| 09:43 | Edited reviews/2026-04-24-literary-board-reviews.md | expanded (+118 lines) | ~2698 |
| 09:52 | Applied 15 priority board fixes to Ch01 and Ch03 (7+8 edits) | ch01, ch03 | committed c23dbe4 | ~800 |
| 09:52 | Third-pass board review Ch01: 8.3/10 POLISH (was 7.6) — 5 priority items remain | ch01, reviews | complete | ~43k |
| 09:52 | Second-pass board review Ch03: 7.8/10 POLISH (was 6.4) — 5 priority items remain | ch03, reviews | complete | ~39k |
| 09:44 | Session end: 16 writes across 3 files (ch01-when-saas-fights-reality.md, ch03-inverted-stack-one-diagram.md, 2026-04-24-literary-board-reviews.md) | 4 reads | ~23322 tok |
| 10:00 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | "s AI services a national " → "s AI services a national " | ~364 |
| 10:00 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | inline fix | ~325 |
| 10:01 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | "s LGPD, South Africa" → "s LGPD, Mexico" | ~134 |
| 10:01 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | inline fix | ~93 |
| 10:01 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | inline fix | ~136 |
| 10:01 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | 3→3 lines | ~107 |
| 10:01 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | inline fix | ~63 |
| 10:02 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | "s 2020 Schrems II ruling " → "s 2020 Schrems II ruling " | ~327 |
| 10:02 | Applied top-5 board priority fixes to Ch01 and Ch03 | ch01, ch03 | committed 4522839 | ~900 |
| 10:02 | Ch01 now 5,459 words (~5,200 target); Ch03 now 3,732 words (~3,500 target) | both | within relaxed budget | ~10 |
| 10:03 | Session end: 24 writes across 3 files (ch01-when-saas-fights-reality.md, ch03-inverted-stack-one-diagram.md, 2026-04-24-literary-board-reviews.md) | 4 reads | ~24980 tok |
| 10:11 | Created .claude/commands/review-cycle.md | — | ~2019 |
| 10:12 | Edited reviews/2026-04-24-literary-board-reviews.md | modified as() | ~1768 |
| 10:30 | Fourth-pass Ch01 board review: 8.6/10 POLISH, 7/12 PUBLISH votes | ch01 | trajectory 6.2→7.6→8.3→8.6 | ~39k |
| 10:30 | Third-pass Ch03 board review: 8.1/10 POLISH, 1/12 clean PUBLISH + 4 borderline | ch03 | trajectory 6.4→7.8→8.1 | ~41k |
| 10:34 | Created /review-cycle slash command with 8 escape hatches | .claude/commands/review-cycle.md | created | ~1500 |
| 10:13 | Session end: 26 writes across 4 files (ch01-when-saas-fights-reality.md, ch03-inverted-stack-one-diagram.md, 2026-04-24-literary-board-reviews.md, review-cycle.md) | 4 reads | ~31960 tok |
| 10:19 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | inline fix | ~40 |
| 10:19 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | inline fix | ~49 |
| 10:19 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | inline fix | ~132 |
| 10:19 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | inline fix | ~70 |
| 10:19 | Edited chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | inline fix | ~146 |
| 10:20 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | inline fix | ~16 |
| 10:20 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | inline fix | ~356 |
| 10:20 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | modified peer() | ~147 |
| 10:20 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | inline fix | ~129 |
| 10:20 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | inline fix | ~99 |
| 10:20 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | inline fix | ~74 |
| 10:21 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | inline fix | ~50 |
| 10:21 | Edited chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md | inline fix | ~135 |
| 10:25 | Edited reviews/2026-04-24-literary-board-reviews.md | modified Deferred() | ~814 |
| 10:45 | /review-cycle Ch01 pass 4 resolution: 5 items applied | ch01 | committed 72de62d | ~1k |
| 10:45 | /review-cycle Ch03 pass 3 resolution: 8 items applied (structural deferred) | ch03 | committed 72de62d | ~2k |
| 10:48 | Ch01 pass 5 verification: 8.9/10 PUBLISH-READY (12/12 unanimous) | ch01 | EXIT: TARGET + QUORUM | ~35k |
| 10:48 | Ch03 pass 4 verification: 8.8/10 PUBLISH-READY (12/12 unanimous) | ch03 | EXIT: TARGET + QUORUM | ~35k |
| 10:50 | /review-cycle run complete: both chapters advanced to icm/approved | ch01, ch03, reviews | recorded | ~2k |
| 10:25 | Session end: 40 writes across 4 files (ch01-when-saas-fights-reality.md, ch03-inverted-stack-one-diagram.md, 2026-04-24-literary-board-reviews.md, review-cycle.md) | 4 reads | ~34750 tok |
| 10:38 | Edited reviews/2026-04-24-literary-board-reviews.md | expanded (+60 lines) | ~1257 |
| 11:15 | Rules reloaded — cerebrum + anatomy + openwolf re-read | .wolf/* | refreshed | ~500 |
| 11:15 | /review-cycle Ch02 pass 1 initial: 6.2/10 REVISE — user-triage checkpoint | ch02 | DO-NOT-USE advisory triggered (below 7) | ~43k |
| 10:38 | Session end: 41 writes across 4 files (ch01-when-saas-fights-reality.md, ch03-inverted-stack-one-diagram.md, 2026-04-24-literary-board-reviews.md, review-cycle.md) | 7 reads | ~42112 tok |
| 10:44 | Session end: 41 writes across 4 files (ch01-when-saas-fights-reality.md, ch03-inverted-stack-one-diagram.md, 2026-04-24-literary-board-reviews.md, review-cycle.md) | 8 reads | ~42112 tok |
| 10:50 | Edited chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md | inline fix | ~177 |
| 10:50 | Edited chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md | inline fix | ~264 |
| 10:51 | Edited chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md | "s servers throughout. Con" → "s servers throughout; con" | ~196 |
| 10:51 | Edited chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md | reduced (-10 lines) | ~205 |
| 10:51 | Edited chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md | 1→3 lines | ~263 |
| 10:52 | Edited chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md | 3→5 lines | ~651 |
| 10:52 | Edited chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md | 1→3 lines | ~179 |
| 10:52 | Edited chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md | inline fix | ~63 |
| 10:58 | Edited reviews/2026-04-24-literary-board-reviews.md | expanded (+58 lines) | ~940 |
| 11:30 | Pre-flight Figma CRDT verification via research-assistant | v13 line 643 flagged as erroneous upstream | ~20k |
| 11:32 | Ch02 pass 1 resolution: 7 edits applied per UPF Option-C+ plan | ch02 | committed 99915f3 | ~900 |
| 11:38 | Ch02 pass 2 verification: 8.0/10 POLISH (delta +1.8 from 6.2) | ch02 | all kill criteria passed | ~38k |
| 11:38 | Board voted to terminate cycle; 5 light-polish items remain for user decision | ch02 | user-triage checkpoint | ~2k |
| 10:58 | Session end: 50 writes across 5 files (ch01-when-saas-fights-reality.md, ch03-inverted-stack-one-diagram.md, 2026-04-24-literary-board-reviews.md, review-cycle.md, ch02-local-first-serious-stack.md) | 8 reads | ~52366 tok |
| 11:02 | Edited chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md | inline fix | ~379 |
| 11:02 | Edited chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md | 3→5 lines | ~179 |
| 11:03 | Edited chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md | 3→1 lines | ~160 |
| 11:03 | Edited chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md | inline fix | ~142 |
| 11:03 | Edited chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md | inline fix | ~63 |
| 11:45 | Ch02 final polish: 5 board-recommended items applied | ch02 | committed; cycle exit | ~1k |
| 11:45 | /review-cycle Ch02 COMPLETE: 6.2 REVISE -> 8.0 POLISH -> final polish | ch02 | icm/approved candidate | ~100 |
| 11:04 | Session end: 55 writes across 5 files (ch01-when-saas-fights-reality.md, ch03-inverted-stack-one-diagram.md, 2026-04-24-literary-board-reviews.md, review-cycle.md, ch02-local-first-serious-stack.md) | 8 reads | ~53354 tok |
| 11:10 | Session end: 55 writes across 5 files (ch01-when-saas-fights-reality.md, ch03-inverted-stack-one-diagram.md, 2026-04-24-literary-board-reviews.md, review-cycle.md, ch02-local-first-serious-stack.md) | 8 reads | ~53354 tok |
| 11:18 | Edited chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md | inline fix | ~262 |
| 11:18 | Edited chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md | 1→3 lines | ~86 |
| 12:05 | Research: no production app satisfies all 7 Kleppmann properties; Anytype closest at 5.5/7 | research findings | strengthened hedge | ~32k |
| 12:07 | Ch02 polish: Anytype near-miss analysis + Kleppmann 2024 gradient citation [3] | ch02 | committed 57478af | ~500 |
| 11:19 | Session end: 57 writes across 5 files (ch01-when-saas-fights-reality.md, ch03-inverted-stack-one-diagram.md, 2026-04-24-literary-board-reviews.md, review-cycle.md, ch02-local-first-serious-stack.md) | 8 reads | ~53726 tok |
| 11:23 | Session end: 57 writes across 5 files (ch01-when-saas-fights-reality.md, ch03-inverted-stack-one-diagram.md, 2026-04-24-literary-board-reviews.md, review-cycle.md, ch02-local-first-serious-stack.md) | 8 reads | ~53726 tok |
| 11:31 | Edited chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md | 1→3 lines | ~236 |
| 11:42 | Edited chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md | 1→3 lines | ~360 |
| 11:43 | Created ../Sunfish/docs/ENGINEERING-PRINCIPLES.md | — | ~1915 |
| 12:30 | Research: Sunfish reality check vs Kleppmann 7 — 4/7 IMPLEMENTED, 1 PARTIAL, 1 BLOCKED, 1 SPECIFIED | Sunfish repo audit | 8-10 weeks to all-seven | ~30k |
| 12:32 | Cerebrum updates: Sunfish CRDT is stub; GossipDaemon delta-apply-back pending; full dotnet build fails | .wolf/cerebrum.md | +4 Do-Not-Repeat entries | ~500 |
| 12:38 | Ch02 polish: three feasibility disciplines added (integration, crypto, open-format) | ch02 | 4,617 words (17 over 4,600 threshold, accepted) | ~400 |
| 12:42 | Created Sunfish/docs/ENGINEERING-PRINCIPLES.md — three principles codified as enforceable rules | Sunfish repo | file created, not committed (CLAUDE.md rule) | ~2k |
| 11:44 | Session end: 60 writes across 6 files (ch01-when-saas-fights-reality.md, ch03-inverted-stack-one-diagram.md, 2026-04-24-literary-board-reviews.md, review-cycle.md, ch02-local-first-serious-stack.md) | 26 reads | ~56416 tok |
| 12:01 | Created ../Sunfish/docs/build-first-agent-prompt.md | — | ~4016 |
| 12:55 | Created Sunfish/docs/build-first-agent-prompt.md — self-contained LLM prompt for 8-10 week sprint | Sunfish repo | file created, not committed | ~2.5k |
| 12:01 | Session end: 61 writes across 7 files (ch01-when-saas-fights-reality.md, ch03-inverted-stack-one-diagram.md, 2026-04-24-literary-board-reviews.md, review-cycle.md, ch02-local-first-serious-stack.md) | 26 reads | ~60719 tok |
| 12:12 | Edited chapters/part-1-thesis-and-pain/ch04-choosing-your-architecture.md | inline fix | ~35 |
| 12:13 | Edited chapters/part-1-thesis-and-pain/ch04-choosing-your-architecture.md | 1→3 lines | ~518 |
| 12:13 | Edited chapters/part-1-thesis-and-pain/ch04-choosing-your-architecture.md | inline fix | ~148 |
| 12:13 | Edited chapters/part-1-thesis-and-pain/ch04-choosing-your-architecture.md | reduced (-8 lines) | ~263 |
| 12:14 | Edited chapters/part-1-thesis-and-pain/ch04-choosing-your-architecture.md | inline fix | ~40 |
| 12:14 | Edited chapters/part-1-thesis-and-pain/ch04-choosing-your-architecture.md | 3→3 lines | ~191 |
| 12:20 | Edited chapters/part-1-thesis-and-pain/ch04-choosing-your-architecture.md | inline fix | ~119 |
| 12:20 | Edited chapters/part-1-thesis-and-pain/ch04-choosing-your-architecture.md | 3→5 lines | ~187 |
| 12:20 | Edited chapters/part-1-thesis-and-pain/ch04-choosing-your-architecture.md | inline fix | ~216 |
| 12:21 | Edited chapters/part-1-thesis-and-pain/ch04-choosing-your-architecture.md | 1→3 lines | ~200 |
| 12:22 | Edited reviews/2026-04-24-literary-board-reviews.md | modified cannot() | ~1128 |
| 13:15 | Ch04 pass 1 board review: 6.3 REVISE (editorial-vs-regional split) | ch04 | pattern matches Ch01/02/03 | ~33k |
| 13:20 | Ch04 pass 1 resolution: 4 of 5 items applied (structural deferred) | ch04 | committed aee8eca | ~700 |
| 13:27 | Ch04 pass 2 verification: 7.92 POLISH (delta +1.62) | ch04 | board voted terminate | ~35k |
| 13:32 | Ch04 final polish: 4 of 5 remaining items applied | ch04 | committed 29fb90b; Part I cycle complete | ~600 |
| 12:31 | Edited chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md | 3→5 lines | ~265 |
| 12:31 | Edited chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md | 1→3 lines | ~231 |
| 12:31 | Edited chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md | inline fix | ~151 |
| 12:32 | Edited chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md | 5→5 lines | ~420 |
| 12:32 | Edited chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md | 1→3 lines | ~88 |
| 12:32 | Edited chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md | inline fix | ~140 |
| 12:32 | Edited chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md | inline fix | ~118 |
| 12:33 | Edited chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md | 1→3 lines | ~222 |
| 12:33 | Edited chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md | 3→1 lines | ~81 |
| 12:38 | Edited chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md | "s DPDP Rules, Nigeria" → "s DPDP Rules, Japan" | ~150 |
| 12:38 | Edited chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md | 5→3 lines | ~188 |
| 12:38 | Edited chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md | inline fix | ~85 |
| 12:39 | Edited chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md | inline fix | ~95 |
| 12:39 | Edited chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md | 1→3 lines | ~327 |
| 12:46 | Edited chapters/part-2-council-reads-the-paper/ch06-distributed-systems-lens.md | expanded (+13 lines) | ~484 |
| 12:46 | Edited chapters/part-2-council-reads-the-paper/ch06-distributed-systems-lens.md | 1→3 lines | ~219 |
| 12:46 | Edited chapters/part-2-council-reads-the-paper/ch06-distributed-systems-lens.md | 1→3 lines | ~395 |
| 12:47 | Edited chapters/part-2-council-reads-the-paper/ch06-distributed-systems-lens.md | 4→6 lines | ~119 |
| 12:47 | Edited chapters/part-2-council-reads-the-paper/ch06-distributed-systems-lens.md | 4→6 lines | ~143 |
| 12:51 | Edited chapters/part-2-council-reads-the-paper/ch06-distributed-systems-lens.md | inline fix | ~71 |
| 12:51 | Edited chapters/part-2-council-reads-the-paper/ch06-distributed-systems-lens.md | "s NDPR, South Africa" → "s LGPD, Mexico" | ~74 |
| 12:59 | Edited chapters/part-2-council-reads-the-paper/ch07-security-lens.md | 1→3 lines | ~434 |
| 13:00 | Edited chapters/part-2-council-reads-the-paper/ch07-security-lens.md | expanded (+10 lines) | ~431 |
| 13:00 | Edited chapters/part-2-council-reads-the-paper/ch07-security-lens.md | 1→3 lines | ~257 |
| 13:00 | Edited chapters/part-2-council-reads-the-paper/ch07-security-lens.md | modified C5() | ~147 |
| 13:00 | Edited chapters/part-2-council-reads-the-paper/ch07-security-lens.md | inline fix | ~121 |
| 13:01 | Edited chapters/part-2-council-reads-the-paper/ch07-security-lens.md | expanded (+14 lines) | ~590 |
| 13:06 | Edited chapters/part-2-council-reads-the-paper/ch07-security-lens.md | inline fix | ~38 |
| 13:06 | Edited chapters/part-2-council-reads-the-paper/ch07-security-lens.md | inline fix | ~152 |
| 13:06 | Edited chapters/part-2-council-reads-the-paper/ch07-security-lens.md | 1→2 lines | ~199 |
| 13:12 | Literary board review pass 1 — Ch08 Product-Economic Lens | chapters/part-2-council-reads-the-paper/ch08-product-economic-lens.md | Board score 5.92/10 REVISE; 5 priority items; regional gap is primary finding | ~9000 |
| 13:13 | Edited chapters/part-2-council-reads-the-paper/ch08-product-economic-lens.md | inline fix | ~209 |
| 13:14 | Edited chapters/part-2-council-reads-the-paper/ch08-product-economic-lens.md | inline fix | ~446 |
| 13:14 | Edited chapters/part-2-council-reads-the-paper/ch08-product-economic-lens.md | 1→3 lines | ~396 |
| 13:14 | Edited chapters/part-2-council-reads-the-paper/ch08-product-economic-lens.md | modified if() | ~947 |
| 13:20 | Edited chapters/part-2-council-reads-the-paper/ch08-product-economic-lens.md | removed 7 lines | ~40 |
| 13:20 | Edited chapters/part-2-council-reads-the-paper/ch08-product-economic-lens.md | inline fix | ~92 |
| 13:20 | Edited chapters/part-2-council-reads-the-paper/ch08-product-economic-lens.md | inline fix | ~108 |
| 13:20 | Edited chapters/part-2-council-reads-the-paper/ch08-product-economic-lens.md | inline fix | ~168 |
| 13:20 | Edited chapters/part-2-council-reads-the-paper/ch08-product-economic-lens.md | 1→3 lines | ~379 |
| 13:27 | Edited chapters/part-2-council-reads-the-paper/ch09-local-first-practitioner-lens.md | inline fix | ~144 |
| 13:28 | Edited chapters/part-2-council-reads-the-paper/ch09-local-first-practitioner-lens.md | reduced (-6 lines) | ~696 |
| 13:29 | Edited chapters/part-2-council-reads-the-paper/ch09-local-first-practitioner-lens.md | expanded (+25 lines) | ~1103 |
| 13:34 | Edited chapters/part-2-council-reads-the-paper/ch09-local-first-practitioner-lens.md | 3→3 lines | ~650 |
| 13:35 | Edited chapters/part-2-council-reads-the-paper/ch09-local-first-practitioner-lens.md | inline fix | ~198 |
| 13:41 | Edited chapters/part-2-council-reads-the-paper/ch10-synthesis.md | inline fix | ~206 |
| 13:42 | Edited chapters/part-2-council-reads-the-paper/ch10-synthesis.md | 1→3 lines | ~435 |
| 13:42 | Edited chapters/part-2-council-reads-the-paper/ch10-synthesis.md | 1→3 lines | ~635 |
| 13:42 | Edited chapters/part-2-council-reads-the-paper/ch10-synthesis.md | modified as() | ~292 |
| 13:42 | Edited chapters/part-2-council-reads-the-paper/ch10-synthesis.md | inline fix | ~52 |
| 13:47 | Edited chapters/part-2-council-reads-the-paper/ch10-synthesis.md | inline fix | ~63 |
| 13:47 | Edited chapters/part-2-council-reads-the-paper/ch10-synthesis.md | inline fix | ~121 |
| 13:47 | Edited chapters/part-2-council-reads-the-paper/ch10-synthesis.md | inline fix | ~185 |
| 13:47 | Edited chapters/part-2-council-reads-the-paper/ch10-synthesis.md | inline fix | ~145 |
| 13:48 | Session end: 125 writes across 14 files (ch01-when-saas-fights-reality.md, ch03-inverted-stack-one-diagram.md, 2026-04-24-literary-board-reviews.md, review-cycle.md, ch02-local-first-serious-stack.md) | 36 reads | ~131149 tok |

## Session: 2026-04-24 14:55

| Time | Action | File(s) | Outcome | ~Tokens |
|------|--------|---------|---------|--------|
| 15:03 | Edited chapters/part-3-reference-architecture/ch11-node-architecture.md | inline fix | ~258 |
| 15:03 | Edited chapters/part-3-reference-architecture/ch11-node-architecture.md | inline fix | ~60 |
| 15:03 | Edited chapters/part-3-reference-architecture/ch11-node-architecture.md | 1→3 lines | ~392 |
| 15:04 | Edited chapters/part-3-reference-architecture/ch11-node-architecture.md | 1→3 lines | ~593 |
| 15:04 | Edited chapters/part-3-reference-architecture/ch11-node-architecture.md | 3→1 lines | ~110 |
| 15:04 | Edited chapters/part-3-reference-architecture/ch11-node-architecture.md | 1→3 lines | ~392 |
| 15:05 | Edited chapters/part-3-reference-architecture/ch11-node-architecture.md | 1→3 lines | ~354 |
| 15:10 | Edited chapters/part-3-reference-architecture/ch11-node-architecture.md | "s relay-is-ciphertext-onl" → "s relay-is-ciphertext-onl" | ~540 |
| 15:10 | Edited chapters/part-3-reference-architecture/ch11-node-architecture.md | inline fix | ~293 |
| 15:10 | Edited chapters/part-3-reference-architecture/ch11-node-architecture.md | inline fix | ~260 |
| 15:10 | Edited chapters/part-3-reference-architecture/ch11-node-architecture.md | 1→3 lines | ~102 |
| 15:17 | Edited chapters/part-3-reference-architecture/ch12-crdt-engine-data-layer.md | expanded (+24 lines) | ~1410 |
| 15:17 | Edited chapters/part-3-reference-architecture/ch12-crdt-engine-data-layer.md | 1→3 lines | ~506 |
| 15:18 | Edited chapters/part-3-reference-architecture/ch12-crdt-engine-data-layer.md | inline fix | ~300 |
| 15:18 | Edited chapters/part-3-reference-architecture/ch12-crdt-engine-data-layer.md | inline fix | ~67 |

## Session: 2026-04-24 15:19

| Time | Action | File(s) | Outcome | ~Tokens |
|------|--------|---------|---------|--------|
| 15:23 | Edited chapters/part-3-reference-architecture/ch12-crdt-engine-data-layer.md | expanded (+9 lines) | ~594 |
| 15:24 | Edited chapters/part-3-reference-architecture/ch12-crdt-engine-data-layer.md | 1→3 lines | ~96 |
| 15:24 | Edited chapters/part-3-reference-architecture/ch12-crdt-engine-data-layer.md | inline fix | ~335 |
| 15:24 | Edited chapters/part-3-reference-architecture/ch12-crdt-engine-data-layer.md | modified must() | ~155 |
| 15:24 | Edited chapters/part-3-reference-architecture/ch12-crdt-engine-data-layer.md | inline fix | ~194 |
| 15:24 | Edited build/Makefile | expanded (+9 lines) | ~215 |
| 15:26 | Edited build/Makefile | 3→2 lines | ~12 |
| 15:26 | Built EPUB 3 from 27 chapters + updated Makefile to --to epub3 --split-level=1 | build/Makefile, build/output/the-inverted-stack.epub | 288 KB EPUB 3 | ~1500 |
| 15:26 | Session end: 7 writes across 2 files (ch12-crdt-engine-data-layer.md, Makefile) | 6 reads | ~20892 tok |
| 15:29 | Edited chapters/part-3-reference-architecture/ch13-schema-migration-evolution.md | inline fix | ~239 |
| 15:30 | Edited chapters/part-3-reference-architecture/ch13-schema-migration-evolution.md | inline fix | ~248 |
| 15:30 | Edited chapters/part-3-reference-architecture/ch13-schema-migration-evolution.md | 1→3 lines | ~522 |
| 15:31 | Session end: 10 writes across 3 files (ch12-crdt-engine-data-layer.md, Makefile, ch13-schema-migration-evolution.md) | 6 reads | ~21972 tok |
| 15:32 | Created build/audiobook.py | — | ~3230 |
| 15:34 | Session end: 11 writes across 4 files (ch12-crdt-engine-data-layer.md, Makefile, ch13-schema-migration-evolution.md, audiobook.py) | 9 reads | ~45930 tok |
| 15:36 | Edited chapters/part-3-reference-architecture/ch14-sync-daemon-protocol.md | expanded (+23 lines) | ~692 |
| 15:36 | Edited chapters/part-3-reference-architecture/ch14-sync-daemon-protocol.md | inline fix | ~271 |
| 15:37 | Edited chapters/part-3-reference-architecture/ch14-sync-daemon-protocol.md | 1→3 lines | ~535 |
| 15:39 | Session end: 14 writes across 5 files (ch12-crdt-engine-data-layer.md, Makefile, ch13-schema-migration-evolution.md, audiobook.py, ch14-sync-daemon-protocol.md) | 10 reads | ~47534 tok |
| 15:43 | Edited chapters/part-3-reference-architecture/ch15-security-architecture.md | modified required() | ~391 |
| 15:43 | Edited chapters/part-3-reference-architecture/ch15-security-architecture.md | inline fix | ~151 |
| 15:43 | Edited chapters/part-3-reference-architecture/ch15-security-architecture.md | expanded (+6 lines) | ~1034 |
| 15:44 | Edited chapters/part-3-reference-architecture/ch15-security-architecture.md | "s integrity guarantees an" → "s DPDP Act erasure right," | ~234 |
| 15:44 | Edited chapters/part-3-reference-architecture/ch15-security-architecture.md | 1→3 lines | ~389 |
| 15:51 | Edited chapters/part-3-reference-architecture/ch16-persistence-beyond-the-node.md | expanded (+20 lines) | ~1832 |
| 15:51 | Edited chapters/part-3-reference-architecture/ch16-persistence-beyond-the-node.md | 1→3 lines | ~446 |
| 15:52 | Edited chapters/part-3-reference-architecture/ch16-persistence-beyond-the-node.md | expanded (+8 lines) | ~693 |
| 15:52 | Session end: 22 writes across 7 files (ch12-crdt-engine-data-layer.md, Makefile, ch13-schema-migration-evolution.md, audiobook.py, ch14-sync-daemon-protocol.md) | 13 reads | ~89153 tok |
| 15:52 | Edited chapters/part-3-reference-architecture/ch16-persistence-beyond-the-node.md | 6→5 lines | ~374 |
| 15:53 | Session end: 23 writes across 7 files (ch12-crdt-engine-data-layer.md, Makefile, ch13-schema-migration-evolution.md, audiobook.py, ch14-sync-daemon-protocol.md) | 13 reads | ~89553 tok |
| 15:55 | Session end: 23 writes across 7 files (ch12-crdt-engine-data-layer.md, Makefile, ch13-schema-migration-evolution.md, audiobook.py, ch14-sync-daemon-protocol.md) | 13 reads | ~89553 tok |
| 16:00 | Edited build/audiobook.py | expanded (+17 lines) | ~203 |
| 16:00 | Edited build/audiobook.py | modified _heading_sub() | ~215 |
| 16:00 | Edited build/audiobook.py | modified _ensure_period() | ~283 |
| 16:00 | Edited build/audiobook.py | modified synth_chunk() | ~488 |
| 16:00 | Edited build/audiobook.py | modified enumerate() | ~222 |
| 16:01 | Edited build/audiobook.py | modified exists() | ~409 |
| 16:01 | Edited build/audiobook.py | modified len() | ~257 |
| 16:02 | Session end: 30 writes across 7 files (ch12-crdt-engine-data-layer.md, Makefile, ch13-schema-migration-evolution.md, audiobook.py, ch14-sync-daemon-protocol.md) | 13 reads | ~91630 tok |
| 16:02 | Session end: 30 writes across 7 files (ch12-crdt-engine-data-layer.md, Makefile, ch13-schema-migration-evolution.md, audiobook.py, ch14-sync-daemon-protocol.md) | 13 reads | ~91630 tok |
| 16:12 | Edited chapters/part-4-implementation-playbooks/ch17-building-first-node.md | expanded (+6 lines) | ~575 |
| 16:12 | Edited chapters/part-4-implementation-playbooks/ch17-building-first-node.md | inline fix | ~24 |
| 16:12 | Edited chapters/part-4-implementation-playbooks/ch17-building-first-node.md | inline fix | ~187 |
| 16:13 | Edited chapters/part-4-implementation-playbooks/ch17-building-first-node.md | 10→11 lines | ~123 |
| 16:13 | Edited chapters/part-4-implementation-playbooks/ch17-building-first-node.md | 1→5 lines | ~326 |
| 16:13 | Edited chapters/part-4-implementation-playbooks/ch17-building-first-node.md | GenerateJoinerBundleAsync() → IssueJoinerAttestationAsync() | ~67 |
| 16:14 | Edited chapters/part-4-implementation-playbooks/ch17-building-first-node.md | modified if() | ~311 |
| 16:14 | Edited chapters/part-4-implementation-playbooks/ch17-building-first-node.md | modified OnLoadAsync() | ~717 |
| 16:17 | Edited build/audiobook.py | expanded (+23 lines) | ~374 |
| 16:17 | Edited build/audiobook.py | expanded (+7 lines) | ~209 |
| 16:18 | Edited build/audiobook.py | modified items() | ~486 |
| 16:18 | Edited build/audiobook.py | modified exists() | ~172 |
| 16:18 | Edited build/audiobook.py | 2→2 lines | ~33 |
| 16:18 | Session end: 43 writes across 8 files (ch12-crdt-engine-data-layer.md, Makefile, ch13-schema-migration-evolution.md, audiobook.py, ch14-sync-daemon-protocol.md) | 16 reads | ~109267 tok |
| 16:19 | Session end: 43 writes across 8 files (ch12-crdt-engine-data-layer.md, Makefile, ch13-schema-migration-evolution.md, audiobook.py, ch14-sync-daemon-protocol.md) | 16 reads | ~109267 tok |
| 16:19 | Session end: 43 writes across 8 files (ch12-crdt-engine-data-layer.md, Makefile, ch13-schema-migration-evolution.md, audiobook.py, ch14-sync-daemon-protocol.md) | 16 reads | ~109267 tok |
| 16:22 | Edited chapters/part-4-implementation-playbooks/ch18-migrating-existing-saas.md | expanded (+24 lines) | ~1112 |
| 16:23 | Edited chapters/part-4-implementation-playbooks/ch18-migrating-existing-saas.md | AddSunfishFeatureManagement() → AddFeatureManagement() | ~469 |
| 16:23 | Edited chapters/part-4-implementation-playbooks/ch18-migrating-existing-saas.md | expanded (+21 lines) | ~354 |
| 16:24 | Edited build/audiobook.py | expanded (+17 lines) | ~415 |
| 16:24 | Edited build/audiobook.py | 2→5 lines | ~115 |
| 16:24 | Edited build/audiobook.py | modified resolve_preset() | ~182 |
| 16:24 | Edited build/audiobook.py | modified exists() | ~157 |
| 16:24 | Edited build/audiobook.py | 2→6 lines | ~92 |
| 16:25 | Session end: 51 writes across 9 files (ch12-crdt-engine-data-layer.md, Makefile, ch13-schema-migration-evolution.md, audiobook.py, ch14-sync-daemon-protocol.md) | 18 reads | ~125422 tok |
| 16:29 | Edited chapters/part-4-implementation-playbooks/ch19-shipping-to-enterprise.md | 12→12 lines | ~531 |
| 16:30 | Edited chapters/part-4-implementation-playbooks/ch19-shipping-to-enterprise.md | expanded (+14 lines) | ~506 |
| 16:31 | Edited chapters/part-4-implementation-playbooks/ch19-shipping-to-enterprise.md | expanded (+26 lines) | ~1775 |
| 16:31 | Edited chapters/part-4-implementation-playbooks/ch19-shipping-to-enterprise.md | expanded (+23 lines) | ~663 |
| 16:36 | Session end: 55 writes across 10 files (ch12-crdt-engine-data-layer.md, Makefile, ch13-schema-migration-evolution.md, audiobook.py, ch14-sync-daemon-protocol.md) | 19 reads | ~137391 tok |
| 16:39 | Created build/m4b.py | — | ~1622 |
| 16:39 | Edited build/Makefile | expanded (+8 lines) | ~31 |
| 16:39 | Session end: 57 writes across 11 files (ch12-crdt-engine-data-layer.md, Makefile, ch13-schema-migration-evolution.md, audiobook.py, ch14-sync-daemon-protocol.md) | 19 reads | ~139046 tok |

## Session: 2026-04-24 16:40

| Time | Action | File(s) | Outcome | ~Tokens |
|------|--------|---------|---------|--------|

## Session: 2026-04-24 16:41

| Time | Action | File(s) | Outcome | ~Tokens |
|------|--------|---------|---------|--------|

## Session: 2026-04-24 16:42

| Time | Action | File(s) | Outcome | ~Tokens |
|------|--------|---------|---------|--------|
| 16:42 | Edited chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md | 2→6 lines | ~142 |
| 16:42 | Edited chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md | expanded (+6 lines) | ~152 |

## Session: 2026-04-24 16:42

| Time | Action | File(s) | Outcome | ~Tokens |
|------|--------|---------|---------|--------|

## Session: 2026-04-24 16:42

| Time | Action | File(s) | Outcome | ~Tokens |
|------|--------|---------|---------|--------|
| 16:42 | Edited chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md | expanded (+6 lines) | ~208 |
| 16:42 | Edited chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md | expanded (+7 lines) | ~244 |
| 16:43 | Edited chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md | 6→11 lines | ~250 |
| 16:43 | Edited chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md | expanded (+11 lines) | ~310 |
| 16:43 | Edited chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md | expanded (+11 lines) | ~369 |
| 16:44 | Edited chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md | expanded (+43 lines) | ~932 |
| 16:44 | Edited chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md | 15→18 lines | ~278 |
| 16:45 | Session end: 7 writes across 1 files (ch20-ux-sync-conflict.md) | 0 reads | ~2777 tok |
| 16:55 | Edited chapters/front-matter/preface.md | 3→3 lines | ~397 |
| 16:55 | Edited chapters/front-matter/preface.md | 7→9 lines | ~461 |
| 16:56 | Edited chapters/front-matter/preface.md | inline fix | ~211 |
| 16:56 | Edited chapters/front-matter/preface.md | YDotNet() → name() | ~551 |
| 17:02 | Edited chapters/epilogue/epilogue-what-the-stack-owes-you.md | inline fix | ~340 |
| 17:02 | Edited chapters/epilogue/epilogue-what-the-stack-owes-you.md | inline fix | ~124 |
| 17:03 | Edited chapters/epilogue/epilogue-what-the-stack-owes-you.md | 13→15 lines | ~1123 |
| 17:04 | Edited chapters/epilogue/epilogue-what-the-stack-owes-you.md | expanded (+12 lines) | ~884 |
| 17:10 | Edited chapters/appendices/appendix-a-sync-daemon-wire-protocol.md | 5→9 lines | ~499 |
| 17:10 | Edited chapters/appendices/appendix-a-sync-daemon-wire-protocol.md | expanded (+16 lines) | ~723 |
| 17:11 | Edited chapters/appendices/appendix-a-sync-daemon-wire-protocol.md | 19→17 lines | ~358 |
| 17:11 | Edited chapters/appendices/appendix-a-sync-daemon-wire-protocol.md | 3→3 lines | ~43 |
| 17:11 | Edited chapters/appendices/appendix-a-sync-daemon-wire-protocol.md | inline fix | ~125 |
| 17:11 | Edited chapters/appendices/appendix-a-sync-daemon-wire-protocol.md | 8→11 lines | ~347 |
| 17:11 | Edited chapters/appendices/appendix-a-sync-daemon-wire-protocol.md | 2→2 lines | ~153 |
| 17:11 | Edited chapters/appendices/appendix-a-sync-daemon-wire-protocol.md | inline fix | ~186 |
| 17:12 | Edited chapters/appendices/appendix-a-sync-daemon-wire-protocol.md | 10→10 lines | ~261 |
| 17:12 | Edited chapters/appendices/appendix-a-sync-daemon-wire-protocol.md | inline fix | ~199 |
| 17:12 | Edited chapters/appendices/appendix-a-sync-daemon-wire-protocol.md | inline fix | ~94 |
| 17:12 | Edited chapters/appendices/appendix-a-sync-daemon-wire-protocol.md | modified layer() | ~915 |
| 17:13 | Edited chapters/appendices/appendix-a-sync-daemon-wire-protocol.md | modified increments() | ~1597 |
| 17:18 | Edited chapters/appendices/appendix-b-threat-model-worksheets.md | 3→3 lines | ~163 |
| 17:18 | Edited chapters/appendices/appendix-b-threat-model-worksheets.md | 3→4 lines | ~308 |
| 17:18 | Edited chapters/appendices/appendix-b-threat-model-worksheets.md | 10→13 lines | ~689 |
| 17:18 | Edited chapters/appendices/appendix-b-threat-model-worksheets.md | inline fix | ~182 |
| 17:19 | Edited chapters/appendices/appendix-b-threat-model-worksheets.md | modified branch() | ~262 |
| 17:19 | Edited chapters/appendices/appendix-b-threat-model-worksheets.md | 6→8 lines | ~326 |
| 17:19 | Edited chapters/appendices/appendix-b-threat-model-worksheets.md | modified scope() | ~332 |
| 17:19 | Edited chapters/appendices/appendix-b-threat-model-worksheets.md | expanded (+20 lines) | ~637 |
| 17:20 | Edited chapters/appendices/appendix-b-threat-model-worksheets.md | modified region() | ~538 |
| 17:27 | Created chapters/appendices/appendix-c-further-reading.md | — | ~6372 |
| 17:32 | Edited chapters/appendices/appendix-d-testing-the-inverted-stack.md | 1→3 lines | ~209 |
| 17:32 | Edited chapters/appendices/appendix-d-testing-the-inverted-stack.md | modified forming() | ~416 |
| 17:33 | Edited chapters/appendices/appendix-d-testing-the-inverted-stack.md | expanded (+7 lines) | ~440 |
| 17:33 | Edited chapters/appendices/appendix-d-testing-the-inverted-stack.md | inline fix | ~146 |
| 17:33 | Edited chapters/appendices/appendix-d-testing-the-inverted-stack.md | expanded (+7 lines) | ~921 |
| 17:34 | Edited chapters/appendices/appendix-d-testing-the-inverted-stack.md | expanded (+7 lines) | ~997 |
| 17:34 | Edited chapters/appendices/appendix-d-testing-the-inverted-stack.md | expanded (+12 lines) | ~1055 |
