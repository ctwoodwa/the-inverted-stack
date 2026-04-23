---
name: Chapter
about: Track writing progress for a chapter
title: "[Ch XX] Chapter Title"
labels: icm/outline
assignees: ctwoodwa
---

## Chapter

**File:** `chapters/<part>/<filename>.md`
**Target word count:** <!-- from book-structure.md -->
**Part milestone:** <!-- part-i / part-ii / part-iii / part-iv -->

## ICM Pipeline

- [ ] `icm/outline` — Outline posted as comment below
- [ ] `icm/draft` — First draft committed; word count within ±10%
- [ ] `icm/code-check` — `make code-check ch=<chapter>` passes
- [ ] `icm/technical-review` — All `<!-- CLAIM -->` markers resolved
- [ ] `icm/prose-review` — Read-aloud pass; no paragraph > 6 sentences
- [ ] `icm/voice-check` — Author voice synthesis complete
- [ ] `icm/approved` — Full QC checklist (QC-1 through QC-10) passes; PR merged
- [ ] `icm/assembled` — Added to ASSEMBLY.md; draft PDF builds clean

## Quality Checklist

```
[ ] QC-1  Word count within ±10% of target
[ ] QC-2  Every topic in book-structure.md addressed
[ ] QC-3  Source sections cited (v13 §X, v5 §Y, R1/R2)
[ ] QC-4  Sunfish packages by name only — no class APIs
[ ] QC-5  No academic scaffolding
[ ] QC-6  No re-introducing the architecture
[ ] QC-7  Correct voice for part (spec vs. tutorial)
[ ] QC-8  Ch 2 only: one paragraph per prior work
[ ] QC-9  Council chapters only: two-act structure
[ ] QC-10 No placeholder text
```

## Notes

<!-- Dependencies, open questions, or reviewer callouts -->
