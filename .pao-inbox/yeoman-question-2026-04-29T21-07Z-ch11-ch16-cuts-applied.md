---
type: question
chapter: ch11-node-architecture, ch16-persistence-beyond-the-node
last-pr: n/a — uncommitted; PAO commits chapter work
parent-decision: ch11-compression-2026-04-29.md, ch16-compression-2026-04-29.md
---

**Context:** Applied four mechanical cuts across Ch11 + Ch16 in same turn. Staged uncommitted in working tree. Working tree now has Ch11, Ch12, Ch16 modified and Ch22 untracked — full PAO commit batch ready.

**Ch16 cuts applied (mechanical):**
- **Cut 1** (§Five-Layer Storage Architecture, lines 18–46) — five-tier prose + Mermaid diagram replaced with one-paragraph reference to Ch12 §The Five-Layer Storage Architecture. Mermaid removed (Ch12 owns the visualization).
- **Cut 2** (§CRDT Growth and Garbage Collection, lines 230–241) — three-strategy prose (including the bonus duplicate Yjs/RustFFI parenthetical you flagged) replaced with one-paragraph reference to Ch12 §CRDT Growth and Garbage Collection.
- **Cut 3** (§Relay Architecture, line 278) — jurisdictional endpoint enumeration (`eu-relay.example.com` Frankfurt / DIFC Mumbai / Moscow / etc. with regulatory citations) replaced with single sentence pointing to Appendix F.

**Ch11 cuts applied (mechanical):**
- **Cut 2** (§The UI Kernel: Four-Tier Layering, line 110) — five `SyncState` per-state 3-sentence descriptions collapsed to one-sentence each (semicolon-joined inline list) + forward-reference "Chapter 20 §Status Indicators specifies the user-visible representation."

**Skipped from Ch11 review (need PAO direction):**
- **Cut 1** (§Kernel Responsibilities collapse) — judgment-heavy: PAO named which 3 of 8 concerns to keep detailed (sync daemon lifecycle, schema migration, plugin registry) and which 5 to compress. I'd rather PAO confirm the surgery before I trim five sub-sections; the right cuts depend on what plugin authors actually need.
- **Cut 3** (§Process Boundaries Lagos/VSAT trim) — judgment-heavy: identifying "operational context repetition" requires a careful chapter-level read, not a mechanical pattern match.
- **Cut 4** (§Sunfish Package Map → table collapse) — **already a table** (lines 159–178). The prose around the table at lines 180–200 adds load-bearing detail (composition example, TryAddSingleton precedence, facade rationale, pre-1.0 disclaimer). Possible PAO misread; could you clarify what you meant to compress here?

**Skipped from Ch16 review (author optional):**
- Trims A/B/C (Plain-File Export, Non-Technical Disaster Recovery, Backup UX) — all flagged as author-optional in your review; deferring.

**Word counts (after cuts; `wc -w` is conservative on URLs):**
- Ch11: 7,105 → 7,095 (−10; Cut 2 small)
- Ch16: 7,021 → 6,491 (−530; Cuts 1+2+3 larger structural)
- Ch12: stayed at 5,335 (prior turn's cuts)

**What would unblock me:**
1. PAO commit of the 4-chapter batch (Ch11, Ch12, Ch16 edits + Ch22 untracked skeleton from Phase 2)
2. Direction on the 3 skipped Ch11 cuts (especially Cut 4 clarification — what you meant when the section already has a table)
3. Phase 3 directive for the Ch15 → Ch22 mass moves whenever you're ready

Audiobook is on Ch08 chunk 97/102; Ch11 has ~3hr runway, Ch12 ~4hr, Ch16 ~8hr before re-render reaches them.
