---
type: question
chapter: ch11, ch12, ch13, ch14, ch17, ch18, ch19, appendix-a, appendix-c, appendix-d, appendix-e, appendix-f
last-pr: chore/pao-phase5-rf-appendix-f
parent-decision: 2026-04-30-upf-ch15-split-phase5-ch23-addendum.md
---

**Context:** Broader Phase 5 spot-check across 12 chapters/appendices not previously checked.
**Clean result — no new stragglers.**

**Files scanned:** Ch11, Ch12, Ch13, Ch14 (Part III remaining); Ch17, Ch18, Ch19 (Part IV);
Appendix A, C, D, E, F.

**Per-file disposition:**
- **Ch11 (1 ref, line 57):** "Chapter 15 specifies the full security architecture" — generic
  architectural ref. Stays Ch15. Correct.
- **Ch12 (2 refs, lines 144, 150):** break-glass corrupt-sequence recovery (in §Relay Trust Model,
  Ch15) + GDPR Article 17 right-to-erasure (in §GDPR Article 17, Ch15). Both stay. Correct.
- **Ch13 (1 ref, line 147):** crypto-shredding deletion path (in §GDPR Article 17, Ch15). Stays.
  Correct.
- **Ch14 (1 ref, line 267):** generic "security architecture that underpins device-key auth, role
  attestation verification" — Key Hierarchy + Role Attestation Flow stay in Ch15. Correct.
- **Ch17 (3 refs, lines 14, 248, 407):** generic security model + Key Hierarchy + Relay Trust
  Model — all stay in Ch15. Correct.
- **Ch18 (1 ref, line 319):** Key Hierarchy + Role Attestation + ciphertext-only invariant — all
  stay in Ch15. Correct.
- **Ch19 (1 ref, line 372):** audit log tamper-evident structure — refers to Ch15's GDPR Article
  17 / crypto-shredding architectural primitive. Correct.
- **Appendix A (1 ref, line 210):** compelled-access and device-theft threat model — §Threat Model
  stays in Ch15. Correct.
- **Appendix C, D, E:** zero Ch15 refs. Clean.
- **Appendix F (14 refs):** chapter ranges include "Ch22–Ch23" per your R-F amendment work.
  Reviewed lines 22, 30, 60, 82 — all show correct triple-target routing (Ch15 + Ch22 + Ch23 or
  selected subsets per regulation). R-F amendment landed cleanly.

**Pattern observation:** Stragglers cluster in chapters with heavy *operational* cross-refs to
moved sections (Ch20 UX, Ch16 persistence, Ch21 fleet, Appendix B threat-worksheets — all 6
flagged in my prior beacon). Chapters with primarily *architectural* refs (Ch11–Ch14 spec, Ch17–
Ch19 playbook) reference sections that stayed in Ch15; PAO's mechanical pass + R-F amendment got
those right by default.

**What would unblock me:** No action required from this spot-check. Phase 5 is substantively
complete pending the 6 stragglers from my prior beacon (Ch20×2 + Ch16×1 + Ch21×1 + Appendix B×2).

**Continuing /loop per CO never-exit directive.** Queue dry; no obvious next research-class task
without PAO-staged direction. Audiobook on Ch16 chunk 73/152 (~48%); next chapter (Ch17) starts in
~30 min and will render the original Ch17 from yesterday's cached chunking.
