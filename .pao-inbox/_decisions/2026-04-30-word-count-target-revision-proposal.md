---
type: pao-recommendation
date: 2026-04-30
author: PAO
audience: CO (decision)
status: proposal — awaits CO ratification
re: word-count target revision (manuscript at 139k vs 85k original target = +64%)
---

# Word-Count Target Revision — PAO Recommendation

## TL;DR

The original 85,000-word target predates the **9 Volume-1 extensions** + **Part V**
(Ch21/22/23) + **Appendices F+G** that have landed since the structure doc was written.
A realistic revised target is **~135,000 words** (~10% above current after the queued
post-voice-pass compression). Three candidate target levels surveyed below; PAO recommends
(B) at ~135k as the publishing target.

## Current state vs original target

```
85,000 — original target (book-structure.md, predates extensions + Part V + F+G)
113,000 — revised theoretical (original + Part V scope + F+G additions; not adjusted for
          extension absorption into existing chapters)
134,000 — projected after queued compression (current 139k − ~5k from voice-pass-unlocked
          Phase 4 prune + author-judgment cuts on Ch11/Ch12/Ch16)
139,337 — current draft (build/word-count.py)
```

## Candidate target levels

### Option A — Stretch compression target: ~120k (29% over original)

**Reach.** Requires ~19k of cuts beyond what's currently queued. Sources:
- Aggressive prune across Part II council chapters (currently 23.9k vs 20k target = ~4k available)
- Aggressive prune across Part IV playbooks (currently 20.5k vs 14k target = ~6k available)
- Aggressive prune across Appendices A–E (currently 18k vs 8k target = ~10k available)
- Zero touch on extension-introduced sections (voice-pass-locked content)

**Editorial cost:** High. Would compromise the practitioner-detail level that's the book's
positioning. Council chapters at ~3,500 words each are at their narrative-arc minimum;
deeper cuts would weaken the two-act structure. Appendices A–D were drafted to reference
specification-level depth; Appendix B is threat-model worksheets where length is feature.

**Reader experience cost:** Medium-high. The book targets architects + senior engineers
who *expect* completeness; aggressive compression to hit publishing-norm targets sacrifices
the differentiator.

**PAO recommends:** Not this option, unless CO has external publishing constraints (page
budget, $/page printing economics) that make 120k a hard ceiling.

### Option B — Realistic publishing target: ~135k (59% over original) **PAO recommends**

**Reach.** ~4k of additional cuts beyond what's currently queued. Achievable via:
- Post-voice-pass deep prune on §Collaborator Revocation (Ch23, extension #45)
- Post-voice-pass cuts on §Performance Contracts (Ch11, extension #43)
- Post-voice-pass cuts on §Per-Data-Class Device-Distribution (Ch16, extension #44)
- Author judgment on Cuts 5–6 (Ch12) + Trims A/B/C (Ch16) + Cut 4 (Ch19) — not pre-applied

**Editorial cost:** Low-medium. Compression happens in the chapters that absorbed extension
content; the original-spec sections (Part I, council chapters, Appendices A–E) ship as-is.

**Reader experience cost:** Low. Lands the manuscript in the 130-150k band that's normal for
comprehensive practitioner books in this category (DDIA ~200k, Clean Architecture ~75k,
Phoenix Project ~120k). Defensible as "longer than originally planned but coherent."

**PAO recommends this option.**

### Option C — Accept current (~134k after queued compression; ~57% over original)

**Reach.** Zero additional editorial work. Voice-pass + queued compression cuts land here.

**Editorial cost:** Zero.

**Reader experience cost:** Low. The +5k between (B) and (C) is not reader-visible. The
difference is whether CO wants PAO to direct the author-judgment cuts (Cuts 5–6 + Trims +
Cut 4) or ship them as-is.

**PAO would accept this.**

## Per-section breakdown vs proposed (B) target

| Section | Current | Proposed (B) | Trim |
|---|---:|---:|---:|
| Front matter | 1,520 | 1,500 | -20 |
| Part I (Ch 1–4) | 20,785 | 19,500 | -1,285 (light prune across all 4) |
| Part II (Ch 5–10) | 23,924 | 22,000 | -1,924 (modest tightening) |
| Part III (Ch 11–16) | 31,961 | 28,500 | -3,461 (Ch11 + Ch16 deep prune post-voice-pass) |
| Part IV (Ch 17–20) | 20,523 | 19,500 | -1,023 (Ch20 modest after voice-pass; rest as-is) |
| Part V (Ch 21–23) | 22,724 | 21,000 | -1,724 (Phase 4 prune lands here) |
| Epilogue | 3,070 | 3,000 | -70 |
| Appendices A–G | 21,330 | 20,000 | -1,330 (light prune Appendix B + C + D) |
| **Total** | **~145,837** | **~135,000** | **-10,837** |

`build/word-count.py` reports 139,337; the ~6,500 delta is appendices F+G (~5,500) + voice-drafts
directories the script doesn't include. Real total per `wc -w` is closer to 145k.

## What blocks the trajectory toward (B)

1. **Voice-pass on 9 extensions** is the gating event. Until #43, #45, #44 voice-pass:
   - Ch11 §Performance Contracts (~2,100 words) — locked from compression
   - Ch16 §Per-Data-Class Device-Distribution (~1,910) — locked
   - Ch20 §Performance Budgets, §Revocation UX, §Data-Class Escalation UX (~4,000 combined) — locked
   - Ch23 §Collaborator Revocation (~2,500) — locked, blocks Phase 4 prune
2. **Yeoman's Phase 4 prune execution window** — waits for audiobook completion + voice-pass.
3. **Author judgment on the deferred Cuts 5–6 / Trims / Cut 4** — small impact (~600 words).

## Decision asked

CO ratify one of:
- (A) ~120k stretch target — requires aggressive editorial cost
- **(B) ~135k publishing target — PAO recommends; matches practitioner-book norms**
- (C) Accept ~134k current trajectory — defer formal target revision

If (B): no immediate execution change. The trajectory above lands there as voice-pass
unblocks the queued cuts. PAO updates `book-structure.md` word-count table to reflect
revised target.

If (A): PAO produces an aggressive-prune review for Part II council chapters + Appendices
A–D (the unprotected surfaces). Substantial editorial work; needs author input on
which detail to retain.

If (C): no action needed.

---

**Status: pending CO decision. PAO continues in /loop; not blocking on this.**
