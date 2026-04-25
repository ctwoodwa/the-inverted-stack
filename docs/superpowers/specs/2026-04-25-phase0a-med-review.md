# Phase 0a MED-Tier Review and Decisions

**Result: 3 compressions applied, 9 paragraphs skipped with documented reasoning.**

The audit's MED tag (4–9 jurisdictions per paragraph) is a coarse filter. On closer reading, most MED paragraphs use named jurisdictions substantively — as anchor cases for a structural argument, not as fatiguing enumerations. Only paragraphs where a list of 5+ jurisdictions appears as a tail-of-sentence enumeration warrant Phase 0a's anchor-+-pointer recipe.

## Compressions applied (3)

| File | ¶ | What changed |
|---|---|---|
| `appendix-a-sync-daemon-wire-protocol.md` | ¶8 | Added "see Appendix F" pointer to the parenthetical jurisdiction list (kept all 4 inline) |
| `ch07-security-lens.md` | ¶99 | Last bullet: compressed "GDPR, LGPD, POPIA, NDPR, Kenya DPA, DPDP, PIPA" to GDPR + DPDP + LGPD + Appendix F pointer |
| `ch16-persistence-beyond-the-node.md` | ¶67 | Regulatory citations attached to provider examples compressed; provider names (Hetzner, OVHcloud, Scaleway, IDCFrontier, NTT, Sakura, Aliyun, MinIO, Ceph) preserved as actionable operator info |

## Skipped (9) — with documented reasoning

| File | ¶ | Reason for skip |
|---|---|---|
| `appendix-b-threat-model-worksheets.md` | ¶17 | Instructional content (customization guidance); jurisdictions used as illustrative examples for the *reader's* deployment, not as enumeration |
| `front-matter/preface.md` | ¶22 | Audit false positive — paragraph is just `---` separator; jurisdiction tokens were matched in surrounding context |
| `ch01-when-saas-fights-reality.md` | ¶41 | Countries (Nigeria, South Africa, India, rural Brazil/Mexico/SE Asia) are the *subject* of the connectivity discussion, not regulatory enumeration |
| `ch01-when-saas-fights-reality.md` | ¶62 | 3 anchor cases (242-FZ, Schrems II, DPDP) used substantively — each illustrates a distinct customer-side compliance failure mode |
| `ch07-security-lens.md` | ¶53 | 5 regimes used as anchor cases in compelled-access argument; the regional pivot ("Schrems II for European, 242-FZ for Russian, DIFC for DIFC firms, DPDP for Indian BFSI, PIPL for China") is the structural argument |
| `ch10-synthesis.md` | ¶40 | 4 jurisdictions used as case examples for relay-geographic-architecture decision; substantive use, not enumeration |
| `ch16-persistence-beyond-the-node.md` | ¶72 | 4 concrete operational endpoints (Frankfurt/DIFC/Mumbai/Moscow) used as deployment examples — at the spec threshold and concrete |
| `ch16-persistence-beyond-the-node.md` | ¶76 | 4–5 anchor cases for compelled-access threat model (CIS, EU post-Schrems II, GCC, China) — illustrative regional coverage |
| `ch20-ux-sync-conflict.md` | ¶57 | 3 anchor cases (242-FZ, DPDP, UAE DPL 2022) for regulated-markets backup target — at threshold |

## Method

The recipe distinguishes:
- **Compress** — when 5+ jurisdictions appear as a *terminal-clause enumeration* (tail-of-sentence list) that doesn't carry argument weight per item
- **Skip** — when 4–5 jurisdictions appear as *anchor cases* in a structural argument where each named regime is doing distinct work

## Verification after Phase 0a MED

- `python build/check_audit.py`: **PASS** — every jurisdiction in chapters appears in Appendix F
- 3 commits: `6f18466`, `081d2f3`, `163eea5`

## Phase 0a complete

HIGH (24) + MED (3) = 27 paragraphs compressed across Phase 0a. 9 MED paragraphs skipped with documented reasoning above. Phase 0 remaining: Task 10 (closure verification).
