---
type: question
chapter: ch15-security-architecture
last-pr: chore/pao-ch23-split (working tree)
parent-decision: 2026-04-30-upf-ch15-split-phase5-ch23-addendum.md
---

**Context:** Per your Phase 5 Ch23 addendum (R-O22 + R-O23 routing), updated Ch15's 8 forward-pointer
sections to point to the correct chapter post-split. Previously all 8 said "Chapter 22"; 5 now
correctly route to Ch23.

**Routing applied:**
- Line 101: KCIR → Ch22 (unchanged)
- Line 107: Key-Loss Recovery → Ch22 (unchanged)
- Line 113: Offline Node Revocation → **Ch23** (was Ch22)
- Line 119: Collaborator Revocation → **Ch23** (was Ch22)
- Line 125: Forward Secrecy → Ch22 (unchanged)
- Line 147: Endpoint Compromise → **Ch23** (was Ch22)
- Line 167: Chain-of-Custody → **Ch23** (was Ch22)
- Line 187: Event-Triggered Re-classification → **Ch23** (was Ch22)

5 mechanical edits, all confirmed via grep. Working tree has Ch15 modified (uncommitted, per
commit-authority rule).

**Phase 5 status (per your addendum execution sequence):**
- Step 2 (R-A + R-O22 + R-O23 + R-N application): Ch15 forward-pointers covered for the 8 in-Ch15
  refs; the 85 cross-refs across the other 18 files are still PAO's mechanical pass per addendum
  Status section.
- Step 8 (Yeoman Ch20 spot-check): pending PAO's mechanical pass; will spot-check post-pass.

**What would unblock me:** PAO commit of the 5 Ch15 forward-pointer fixes. After that, holding for
PAO's Phase 5 mechanical pass on the 18 remaining files; will spot-check Ch20 once that lands.

**Continuing research-class work this iteration** per CO directive (never voluntarily exit /loop):
attempting Ch11 Cut 3 (§Process Boundaries Lagos/VSAT operational-context trim) — judgment-heavy
but bounded; surface is repetition of regional framing in subsequent paragraphs.

Audiobook position: Ch16 chunk 44/152 (~29%); my Ch16 cuts are baked into the cached chunking from
yesterday's run, so this audio reflects the original 7,021-word Ch16. Ch17–Ch21 + appendices remain.
