---
type: question
chapter: ch22-security-operations (NEW) + ch15-security-architecture
last-pr: n/a — uncommitted; per 2026-04-29 commit-authority change PAO commits chapter work
parent-decision: 2026-04-29-upf-ch15-split.md (Phase 2)
---

**Context:** Phase 2 (Ch22 skeleton + voice-plan entry) is staged uncommitted in the working tree.
- `chapters/part-5-operational-concerns/ch22-security-operations.md` created — header block (icm/draft, target ~10,000w, source notes, code-check inheritance from Ch15), opening framing (architecture↔operations seam), 8 H2 stubs in Phase 1 triage order with per-section Phase-3-placeholder comments naming the source line + prune budget + prune surface for each, and a §References stub naming the citation split per Phase 1 triage footnotes.
- `chapters/voice-plan.yaml` updated — added `# Part V — operational concerns` block with `ch21-operating-a-fleet: sinek` (the existing Ch21 was missing from the file; opportunistic fix) and `ch22-security-operations: sinek` (matches Ch15's preset since the absorbed sections inherit Ch15's voice).
- Phase 2 gate per UPF: file exists ✓; manifest validates → no per-chapter manifest.json exists in this repo (Ch21 has none either; build/output/audiobook/manifest.json is a different artifact). voice-plan.yaml is the closest equivalent and is updated. If PAO wants a separate per-chapter manifest format for Ch22, please specify.

**What would unblock me:** PAO sign-off + commit of the staged work, then Phase 3 directive (move-ordering already specified in triage; ready to execute the 8 mechanical relocations as soon as PAO greenlights). Audiobook re-render is currently on Ch08 (chunk 60/102), so a window for Ch15 edits is open — Phase 3 won't conflict.
