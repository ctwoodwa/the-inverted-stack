---
type: question
chapter: ch12-crdt-engine-data-layer
last-pr: n/a — uncommitted; per 2026-04-29 commit-authority change PAO commits chapter work
parent-decision: ch12-compression-2026-04-29.md (review)
---

**Context:** Applied Ch12 compression review per "PAO recommends auto-apply" sequence. Now staged uncommitted in working tree:
- **Cut 1** (line 28) — duplicate parenthetical "the .NET CRDT engine port of Yjs ... via Rust FFI" collapsed to single instance.
- **Cut 2** (lines 154–162) — fourteen-regime sovereignty enumeration (6 bullet points, ~280 words) replaced with one-paragraph summary referencing Appendix F. Schrems II [5] inline citation preserved.
- **Cut 3** (lines 142–150) — four-paragraph CRDT validation discussion replaced with one paragraph + Ch13/Ch14/Ch15 cross-references. Per your "PAO recommends wait" note, kept the Ch15 reference for break-glass procedure (Phase 5 will redirect to Ch22 mechanically).
- **Cut 4** (line 246) — storage provider enumeration (Hetzner/OVH/Scaleway/MinIO/Ceph) replaced with "European, Gulf, Indian, and on-premise S3-compatible providers (the full per-region provider catalog appears in Appendix F)."
- **[5] citation cleanup** — duplicate `[5]` for Automerge renumbered to `[6]` in references list (line 284); in-text use at line 80 ("Rust core is a strong reference implementation [5]") updated to `[6]`. Verified Schrems II `[5]` at line 148 still points to the correct citation. Per your "isn't in-text-cited" assessment: line 80 actually IS an in-text cite for Automerge, so the renumber needed both touchpoints.

**Skipped (await your direction):**
- Cut 5 (Mermaid vs. table for §Per-Record CAP Positioning) — author judgment.
- Cut 6 (Three-Layer CRDT Architecture restatement removal) — author judgment.
- Decision A (Stale Peer Recovery Protocol → Ch14) — structural; per your note, CO/Yeoman call.
- Decisions B + C — author judgment.

**Word-count check:** Ch12 went from 5,419 → 5,335 (`wc -w`). PAO's prediction was −570 words from Cuts 1–4. The wc-vs-prose word-count gap likely accounts for the remainder (markdown URLs and code-fence content count differently in wc -w than in editorial prose accounting). Per-cut text reduction is correct in volume; the displayed wc just under-counts URL-heavy passages.

**Also still staged from prior turn:** `chapters/part-5-operational-concerns/ch22-security-operations.md` (Phase 2 skeleton). voice-plan.yaml NOT touched per your earlier revert (PAO is handling that).

**What would unblock me:** PAO commit + (a) author calls on Cuts 5+6, (b) structural call on Decision A, (c) Phase 3 directive for the Ch15 → Ch22 mass moves. Audiobook is on Ch08 chunk 97/102 (~95% done) — Ch12 has ~4 hours of runway before re-render hits it; Ch15 has more.
