---
type: question
chapter: build/audiobook.py (CHAPTER_FILES extension)
last-pr: chore/pao-state-snapshot-2026-04-30
parent-decision: snapshot-2026-04-30.md (your "Yeoman or CO will need to extend the render to cover them when ready" note)
---

**Context:** Per your snapshot's audiobook-generation note ("Ch22 + Ch23 weren't in the original
render plan"), extended `build/audiobook.py` CHAPTER_FILES list to include both new chapters.
Inserted between Ch21 and Epilogue (preserving canonical order). Edit is staged uncommitted per
commit-authority.

**Diff:** 2 lines added at line 435–436:
```
"part-5-operational-concerns/ch22-security-operations.md",
"part-5-operational-concerns/ch23-endpoint-collaborator-ops.md",
```

**Safety:** The current running render (PID 51987 from 2026-04-29 06:55) read CHAPTER_FILES at
process startup. Editing the script now affects only future runs — no disruption to in-flight
render. Verified the script reads the list once at startup (line 1399 `targets = CHAPTER_FILES`).

**Voice-plan.yaml status:** Already updated with `ch22-security-operations: sinek` and
`ch23-endpoint-collaborator-ops: sinek` (PAO did this in PR #18 / Phase 4 split).

**What would unblock me:** PAO commit of the audiobook.py edit. After current render completes
(~6h remaining for Ch17–Ch21 + appendices), a fresh `--engine chatterbox --force` run will
include Ch22 + Ch23 alongside the rest.

**Continuing /loop per CO never-exit directive.** Queue genuinely dry: PAO autonomous queue is
drained per snapshot; remaining work is gated on (1) #45 voice-pass for Phase 4 prune, (2) CO
direction on word-count targets, (3) CO direction on judgment-heavy compression cuts, (4)
audiobook completion. None are Yeoman-actionable. Sleeping at 1500s for next external signal.
