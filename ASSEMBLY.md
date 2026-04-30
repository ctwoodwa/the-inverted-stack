# Assembly Manifest

*This file defines the final manuscript assembly order for `make draft-pdf` and `make epub`.*
*Update as chapters reach `icm/assembled`. Word counts via `python3 build/word-count.py`.*

## Status

Last refreshed: 2026-04-30 post-Ch15-split. Word counts from `build/word-count.py`. ICM stages reflect the loop's `state.yaml` (canonical) for extension-affected chapters and the last review pass (council / literary board) for the rest.

| Chapter | File | ICM Stage | Words | Target | QC-1 |
|---|---|---|---:|---:|---|
| Foreword | `chapters/front-matter/foreword-placeholder.md` | placeholder | 86 | — | pending contributor |
| Preface | `chapters/front-matter/preface.md` | icm/prose-review | 1,434 | ~1,000 | ✓ over (143%) |
| Ch 1 | `chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md` | icm/voice-passed (R1+R2 council, literary board) | 6,281 | ~4,500 | ✓ over (140%) |
| Ch 2 | `chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md` | icm/voice-passed (R1+R2 council, literary board) | 5,270 | ~4,000 | ✓ over (132%) |
| Ch 3 | `chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md` | icm/voice-passed (R1+R2 council, literary board) | 4,120 | ~3,000 | ✓ over (137%) |
| Ch 4 | `chapters/part-1-thesis-and-pain/ch04-choosing-your-architecture.md` | icm/voice-passed (R1+R2 council, literary board) | 4,909 | ~3,500 | ✓ over (140%) |
| Ch 5 | `chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md` | icm/voice-passed | 3,912 | ~3,500 | ✓ |
| Ch 6 | `chapters/part-2-council-reads-the-paper/ch06-distributed-systems-lens.md` | icm/voice-passed | 3,788 | ~3,500 | ✓ |
| Ch 7 | `chapters/part-2-council-reads-the-paper/ch07-security-lens.md` | icm/voice-passed | 4,198 | ~3,500 | ✓ |
| Ch 8 | `chapters/part-2-council-reads-the-paper/ch08-product-economic-lens.md` | icm/voice-passed | 4,116 | ~3,500 | ✓ |
| Ch 9 | `chapters/part-2-council-reads-the-paper/ch09-local-first-practitioner-lens.md` | icm/voice-passed | 4,572 | ~3,500 | ✓ |
| Ch 10 | `chapters/part-2-council-reads-the-paper/ch10-synthesis.md` | icm/voice-passed | 3,438 | ~2,500 | ✓ |
| Ch 11 | `chapters/part-3-reference-architecture/ch11-node-architecture.md` | icm/awaiting-voice-check (#43 §Performance Contracts) | 6,498 | ~4,000 | ⚠ over (162%); voice-pass-locked |
| Ch 12 | `chapters/part-3-reference-architecture/ch12-crdt-engine-data-layer.md` | icm/voice-passed (post-cuts) | 4,897 | ~4,000 | ✓ |
| Ch 13 | `chapters/part-3-reference-architecture/ch13-schema-migration-evolution.md` | icm/voice-passed | 3,857 | ~3,500 | ✓ |
| Ch 14 | `chapters/part-3-reference-architecture/ch14-sync-daemon-protocol.md` | icm/voice-passed | 3,809 | ~3,500 | ✓ |
| Ch 15 | `chapters/part-3-reference-architecture/ch15-security-architecture.md` | icm/voice-passed (post Ch15 split UPF) | 6,359 | ~5,500 (revised post-split) | ✓ |
| Ch 16 | `chapters/part-3-reference-architecture/ch16-persistence-beyond-the-node.md` | icm/awaiting-voice-check (#44 §Per-Data-Class Device-Distribution) | 6,135 | ~3,000 | ⚠ over (204%); voice-pass-locked |
| Ch 17 | `chapters/part-4-implementation-playbooks/ch17-building-first-node.md` | icm/voice-passed | 3,481 | ~4,000 | ⚠ under (87%); review pending |
| Ch 18 | `chapters/part-4-implementation-playbooks/ch18-migrating-existing-saas.md` | icm/voice-passed | 3,600 | ~3,500 | ✓ |
| Ch 19 | `chapters/part-4-implementation-playbooks/ch19-shipping-to-enterprise.md` | icm/voice-passed | 4,322 | ~3,500 | ✓ over (123%) |
| Ch 20 | `chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md` | icm/awaiting-voice-check (#43 §Performance Budgets, #45 §Revocation UX, #10 §Data-Class Escalation UX) | 9,120 | ~3,000 | ⚠ over (304%); multiple voice-pass-locked |
| Ch 21 | `chapters/part-5-operational-concerns/ch21-operating-a-fleet.md` | icm/awaiting-voice-check (#11) | 6,309 | ~6,500 | ✓ |
| Ch 22 | `chapters/part-5-operational-concerns/ch22-security-operations.md` | icm/awaiting-voice-check (post-split; #46 §Forward Secrecy + #48 §Key-Loss Recovery sections) | 7,194 | ~7,400 | ✓ |
| Ch 23 | `chapters/part-5-operational-concerns/ch23-endpoint-collaborator-ops.md` | icm/awaiting-voice-check (post-split; #45 §Collaborator Revocation, #47 §Endpoint Compromise, #9 §Chain-of-Custody, #10 §Event-Triggered) | 8,581 | ~9,000 | ✓ |
| Epilogue | `chapters/epilogue/epilogue-what-the-stack-owes-you.md` | icm/voice-passed | 3,070 | ~2,500 | ✓ |
| Appendix A | `chapters/appendices/appendix-a-sync-daemon-wire-protocol.md` | icm/voice-passed | 3,570 | ~2,000 | ✓ over (178%) |
| Appendix B | `chapters/appendices/appendix-b-threat-model-worksheets.md` | icm/voice-passed | 4,330 | ~2,000 | ✓ over (216%) |
| Appendix C | `chapters/appendices/appendix-c-further-reading.md` | icm/voice-passed | 3,293 | ~2,000 | ✓ over (165%) |
| Appendix D | `chapters/appendices/appendix-d-testing-the-inverted-stack.md` | icm/voice-passed | 3,667 | ~2,000 | ✓ over (183%) |
| Appendix E | `chapters/appendices/appendix-e-citation-style.md` | icm/approved | 962 | ~500 | ✓ over (192%) |
| Appendix F | `chapters/appendices/appendix-f-regulatory-coverage.md` | icm/voice-passed (added 2026-04 + Phase 5 R-F update) | 2,223 | ~2,000 | ✓ |
| Appendix G | `chapters/appendices/appendix-g-glossary.md` | icm/voice-passed (added 2026-04) | 3,349 | ~3,000 | ✓ |

**Running total (excluding foreword placeholder):** ~144,664 words
**Original target:** 85,000 words (predates Volume-1 extensions + Part V + Appendices F+G)
**Revised target proposal:** ~135,000 words (PAO recommendation, awaiting CO ratification — see `.pao-inbox/_decisions/2026-04-30-word-count-target-revision-proposal.md`)
**Vs revised target:** 144,664 / 135,000 = 107% — **7% over revised target**, achievable via post-voice-pass cuts.

## Voice-Pass Queue (gating event for assembly)

9 extensions sit at `awaiting-voice-check`. Per `.pao-inbox/_decisions/2026-04-30-voice-pass-priority-queue.md`:

**Tier 1 (unblocks structural work):** #45 Collaborator Revocation (Ch23), #43 Performance Contracts (Ch11+Ch20), #11 Fleet Management (Ch21).
**Tier 2 (unblocks chapter compression):** #44 Per-Data-Class Device-Distribution (Ch16), #46 Forward Secrecy (Ch22), #47 Endpoint Compromise (Ch23).
**Tier 3 (closes extension):** #9 Chain-of-Custody (Ch23), #10 Data-Class Escalation (Ch23), #12 Privacy-Aggregation (Ch15).

Each extension's working artifacts live at `docs/book-update-plan/working/<extension-id>/`.

## Ch15 Split (UPF executed 2026-04-29 / 2026-04-30)

The original Ch15 (22,274 words; 5.5× target) was split into three chapters per XO's UPF (`.pao-inbox/_decisions/2026-04-29-upf-ch15-split.md`):

- **Ch15 — Security Architecture** (architectural primitives, ~6,359 words)
- **Ch22 — Key Lifecycle Operations** (KCIR + Key-Loss Recovery + Forward Secrecy, ~7,194 words)
- **Ch23 — Endpoint, Collaborator, and Custody Operations** (Offline Revocation + Collaborator Revocation + Endpoint Compromise + Chain-of-Custody + Event-Triggered Re-classification, ~8,581 words)

Phase 4 prune deferred until #45 voice-pass unlocks Ch23 §Collaborator Revocation; expected to recover ~3k words.

## Next Steps

1. **`icm/voice-check`** (author, 9 extensions): Tier 1 first per priority queue. Highest leverage: #45 Collaborator Revocation (closes Ch15 split UPF).
2. **Phase 4 prune** (PAO directs, Yeoman executes): post-voice-pass cuts to Ch22+Ch23 (~-3k); cuts on Ch11+Ch20 §Performance Contracts/Budgets (~-400); cuts on Ch16 §Per-Data-Class (~-300).
3. **Foreword**: external contributor needed.
4. **Phase 7 reference-list split**: split Ch15's combined reference list into Ch15/Ch22/Ch23 per the Phase 5 inventory addendum (`.pao-inbox/_decisions/2026-04-30-upf-ch15-split-phase5-ch23-addendum.md`).
5. **Final assembly**: set all chapters to `icm/assembled` after voice-pass + Phase 4 prune; run `make draft-pdf`.

## Build

```bash
make draft-pdf   # Full PDF draft
make epub        # ePub for Leanpub preview
make word-count  # Per-chapter word count vs. targets
make lint        # Check broken cross-references
```

`build/Makefile` includes Ch21–23 + Appendix F+G in `draft-pdf` (added 2026-04-30 PR #26).
`build/lint.py` recognises Ch21–23 + Appendix F+G (added 2026-04-30 PR #23).
`build/audiobook.py` includes Ch22+Ch23 in `CHAPTER_FILES` (added 2026-04-30 PR #26).

Lint status: 0 errors, 2 warnings (Ch16 mid-stream forward-secrecy boundary architectural Q + Ch22 Cohn-Gordon 2016 PCS deferred citation; both legitimate deferred-work trackers).
