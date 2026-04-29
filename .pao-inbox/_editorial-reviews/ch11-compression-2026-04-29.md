---
type: editorial-review
chapter: ch11-node-architecture
date: 2026-04-29
author: PAO
audience: Yeoman (executor), CO (visibility)
status: review — proposed cuts; awaits Yeoman application after audiobook window
target-reduction: 7,105 → 4,000 (target = 178% currently)
identified-cuts: ~650 words editorial; voice-pass-locked section excludes ~2,100 words from cut surface
voice-pass-locked: §Performance Contracts and Main-Thread Isolation (2,105 words from extension #43)
---

# Ch11 (Node Architecture) — Compression Review

## TL;DR

Current 7,105 words against 4,000 target (178%). **§Performance Contracts and Main-Thread Isolation (2,105 words) is voice-pass-locked from extension #43** — PAO will not touch it until #43 voice-pass completes.

Compressing the non-#43 sections (5,000 words) to a realistic ~4,350 yields Ch11 at ~6,455 (161% of target). The "in-tolerance" landing zone for Ch11 likely sits around 5,500–6,000 (138–150%) given the extension absorption — same target-revision pattern as Ch16.

## Section inventory

| § | Section | Words | Notes |
|---:|---|---:|---|
| 1 | The Microkernel Monolith | 407 | Tight; keep |
| 2 | Kernel Responsibilities | 1,193 | Compression candidate (~200) |
| 3 | Plugin Contracts | 565 | Tight; keep |
| 4 | The UI Kernel: Four-Tier Layering | 827 | Compression candidate (~100; Ch20 may already cover SyncState detail) |
| 5 | Process Boundaries and IPC | 1,153 | Compression candidate (~150; Lagos/VSAT framing) |
| 6 | Sunfish Package Map | 648 | Compression candidate (~200; collapse to matrix table) |
| 7 | **Performance Contracts and Main-Thread Isolation** | **2,105** | **VOICE-PASS-LOCKED (extension #43)** |
| **Total compressible** | | | **~650 words** |

## Mechanical / editorial cuts (PAO recommends auto-apply)

### Cut 1 — §Kernel Responsibilities collapse (~200 words)

**Current:** Eight infrastructure concerns each get a 1–2 paragraph description with parallel structure ("X manages Y. The Y has these states: A, B, C..."). Useful for first-time readers; redundant after the third item.

**Proposal:** Keep the eight concerns as a numbered list with one-sentence summary each. Move the per-concern detail (state machines, timing constraints, operational guarantees) to subsections only where the detail is load-bearing for plugin authors. The §Sunfish Package Map already lists which package owns each concern; that mapping shouldn't repeat at the prose level.

**Net:** ~200 words removed. Detail preserved for the 2–3 most load-bearing concerns (sync daemon lifecycle, schema migration, plugin registry); other 5 concerns get a one-sentence summary plus a forward-reference to the relevant chapter (Ch12 for CRDT engine, Ch13 for schema migration, Ch14 for sync daemon).

### Cut 2 — §The UI Kernel: Four-Tier Layering — SyncState detail (~100 words)

**Current:** The five `SyncState` values (Healthy, Stale, Offline, ConflictPending, Quarantine) get 3-sentence descriptions each. Ch20 §Status Indicators covers the user-visible side of these states; Ch11's role is the architectural commitment.

**Proposal:** Reduce per-state descriptions to one sentence each: "`Healthy` means sync within freshness threshold; `Stale` beyond threshold but data still trusted for reads; `Offline` no transport; `ConflictPending` requires user resolution before sync proceeds; `Quarantine` flagged for operator review." Forward-reference: "Ch20 §Status Indicators specifies the user-visible representation."

**Net:** ~100 words removed. Aligns with the discipline that Part III specifies and Part IV/V handles UX.

### Cut 3 — §Process Boundaries and IPC — operational-reality framing (~150 words)

**Current:** Opening paragraph has a vivid Lagos/VSAT/rural-India/load-shedding framing that establishes why the daemon-as-separate-process is load-bearing. Subsequent paragraphs re-establish the same operational context for individual sub-features.

**Proposal:** Keep the opening Lagos/VSAT framing (establishes the "this is not nice-to-have" commitment). Trim subsequent re-establishments of operational context where the same regional examples surface again. The reader has the framing; later paragraphs can cite "the operational realities introduced above" rather than re-listing them.

**Net:** ~150 words removed. Persuasive force preserved at the chapter open; reduced repetition at section level.

### Cut 4 — §Sunfish Package Map — prose-to-table collapse (~200 words)

**Current:** Package-by-package narrative descriptions (Foundation, Foundation.LocalFirst, Kernel.Crdt, Kernel.Lease, Kernel.Sync, Kernel.Security, etc.) with paragraph-level detail for each.

**Proposal:** Collapse to a matrix table (Package | Layer | Primary responsibility | Cross-reference) — denser format. The narrative for each package mostly restates what the chapter has already established in §Kernel Responsibilities or §Plugin Contracts. The map's value is the mapping itself, not the re-narration.

**Net:** ~200 words removed. The mapping table is more reference-friendly anyway.

## What PAO is NOT proposing

**§Performance Contracts and Main-Thread Isolation (2,105 words) is voice-pass-locked.** Extension #43 is at `awaiting-voice-check` per state.yaml. Working artifacts in `docs/book-update-plan/working/43-performance-contracts/` include candidate anecdote framings the author chooses among (the moment a CRDT merge freezes the UI; Linear/Notion 60fps observation). PAO does not propose any cuts to this section until voice-pass completes.

After #43 voice-pass lands, a separate compression review on §Performance Contracts may be worthwhile — that section has the same shape as the chapters that benefited from prune (~15-20% trim achievable on dense exposition), but it must wait for the author's anecdote insertion to anchor the prose first.

## Recommended outcome

After Cuts 1–4 applied: Ch11 lands at ~6,455 (161% of original 4,000 target).

Real target after #43 absorption: ~5,500–6,000 (138–150%) — same pattern as Ch16. PAO recommends bundling Ch11's target revision with the broader word-count table revision pending in `book-structure.md`.

If CO wants Ch11 closer to 4,500 (113%), that requires either reverting #43's content or aggressively pruning §Performance Contracts after voice-pass — content/voice calls, not pure compression.

## Why not pre-applied

Ch11 is in audiobook render queue (currently rendering Ch08; Ch11 still ahead). Modifying chapter prose during render risks unnecessary re-render. Application defers to Yeoman handoff window.

---

**End of review.** Awaiting Yeoman handoff window.
