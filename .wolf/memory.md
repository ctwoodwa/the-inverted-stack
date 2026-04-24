# Memory

> Chronological action log. Hooks and AI append to this file automatically.
> Old sessions are consolidated by the daemon weekly.
| 20:19 | Drafted Chapter 13 Schema Migration and Evolution | chapters/part-3-reference-architecture/ch13-schema-migration-evolution.md | 4144 words, committed to main | ~8000 |
| session | Resolved 40 technical-review markers in ch17 | chapters/part-4-implementation-playbooks/ch17-building-first-node.md | All CLAIM/SUNFISH-API/PACKAGE markers removed; ICM advanced to icm/technical-review | ~6000 |
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
