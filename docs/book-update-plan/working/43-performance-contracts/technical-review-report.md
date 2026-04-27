# Technical-Review Report — #43 Performance Contracts

**Stage:** technical-review (ICM stage 4).
**Run:** iter-0013, 2026-04-27.
**Verdict:** PASS-with-edit (gate passes with two CLAIM markers left for follow-up).
**Scope:** Two new sections drafted in iter-0011 and code-checked in iter-0012:
- `chapters/part-3-reference-architecture/ch11-node-architecture.md` §"Performance Contracts and Main-Thread Isolation"
- `chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md` §"Performance Budgets and Progressive Degradation"

---

## Per-item verdicts (the seven items queued by code-check)

### 1. Yjs 100k-operation merge complexity claim ([4]) — PASS-with-edit

**What the chapter says:** "Merging that document on reconnect can take multiple seconds on commodity hardware [4]." (Ch11:212) and "A merge on a 100,000-operation document is O(n) in operation count and runs in seconds, not milliseconds [4]." (Ch11:244)

**What the source actually says:** The canonical public benchmark for Yjs merge cost is the `dmonad/crdt-benchmarks` repository (maintained by Kevin Jahns, the author of Yjs). Benchmark B4 ("real-world editing dataset") replays 259,778 operations and reports 5,714 ms for Yjs on an Intel i5-8400 at 2.80 GHz × 6 (the README's documented benchmark hardware). 5,714 ms is "multiple seconds" by any reasonable reading; it also exceeds the chapter's chosen 100,000-operation reference (which is below the benchmark's 259k-op load and therefore plausibly faster, but still in the seconds range).

**Edit applied:** Citation [4] repointed from `https://docs.yjs.dev/` (the docs root, which does not contain the benchmark) to `https://github.com/dmonad/crdt-benchmarks#b4-real-world-editing-dataset` (the canonical benchmark, with the specific anchor for B4). Reference list entry updated to:
> [4] K. Jahns, "CRDT benchmarks: B4 — Real-world editing dataset," *dmonad/crdt-benchmarks*, GitHub. Accessed: 2026. [Online]. Available: https://github.com/dmonad/crdt-benchmarks#b4-real-world-editing-dataset

**Prose unchanged.** The claim "multiple seconds on commodity hardware" is faithful to the B4 result on the benchmark's documented hardware.

**File:line:** ch11-node-architecture.md:315 (reference list).

### 2. Linear 60fps engineering blog claim ([5]) — PASS-with-edit (CLAIM marker added)

**What the chapter says:** "Linear's engineering team treats 60fps as a hard constraint on every interaction, not a target the application reaches under optimal conditions [5]." (Ch11:214)

**What the source actually says:** The phrase "60fps as a hard constraint on every interaction" is widely attributed to Linear in industry discussion but could not be pinned to a verbatim public Linear blog post or talk transcript within the iteration budget. Linear's blog and `/about` and `/method` pages use the language of "fast," "speed," and "craft" but do not explicitly state "60fps" as a quotable engineering claim. The closest publicly indexable engineering content is the "Scaling the Linear Sync Engine" talk page (https://linear.app/blog/scaling-the-linear-sync-engine), which discusses sync architecture but not the 60fps figure verbatim.

**Edits applied:**
1. Prose softened from a direct attribution ("treats 60fps as a hard constraint") to a paraphrase ("treats interaction latency as a first-class product constraint"), preserving the rhetorical role of Linear-as-aspirational-bar without making a specific 60fps claim that cannot be sourced.
2. Citation [5] repointed from `https://linear.app/blog/` (root) to the specific "Scaling the Linear Sync Engine" talk URL.
3. `<!-- CLAIM: source? -->` marker inserted noting the verbatim 60fps phrase could not be pinned and inviting the next reviewer to either find a verbatim source or soften the paraphrase further.

**File:line:** ch11-node-architecture.md:214 (prose), ch11-node-architecture.md:317 (reference list).

### 3. Web Vitals INP threshold ([6]) — PASS

**What the chapter says:** "an interaction must produce a visual response within 200ms to register as 'good' [6]" (Ch11:214) and "The 200ms relaxed read budget aligns to the Web Vitals INP 'good' threshold [6]." (Ch11:287)

**What the source says:** https://web.dev/articles/inp — verbatim quote from the page: "An INP below or at **200 milliseconds** means a page has **good responsiveness**. An INP above **200 milliseconds** and below or at **500 milliseconds** means a page's responsiveness **needs improvement**. An INP above **500 milliseconds** means a page has **poor responsiveness**." Threshold matches the chapter exactly. INP did replace FID in March 2024 and the thresholds have not been revised since.

**No edit needed.** Citation URL already points to the correct deep-link page. Verdict: PASS.

### 4. Apple HIG 16ms frame-budget claim ([8]) — PASS-with-edit (CLAIM marker added)

**What the chapter says:** "The 16ms document-editing baseline is calibrated against the 60fps frame budget specified in Apple's Human Interface Guidelines [8]." (Ch11:287)

**What the source says:** The current Apple Human Interface Guidelines (https://developer.apple.com/design/human-interface-guidelines/) is a JavaScript-rendered SPA. Static-HTML scrapes return the SPA shell only; the underlying JSON content endpoints used by the SPA returned no body content for "16ms" or "60fps" within the iteration budget. The 16ms / 60fps figure is industry-standard (1000ms / 60fps = 16.67ms) and Apple does target 60fps for smooth animation on non-ProMotion displays, but a verbatim quote from the current HIG could not be pinned to a deep-link section.

**Edits applied:**
1. Prose softened from "the 60fps frame budget specified in Apple's Human Interface Guidelines" to "the 60fps frame budget that Apple's Human Interface Guidelines treat as the responsiveness target for smooth animation and scrolling," reducing the specificity of what Apple HIG is asserted to "specify."
2. The math is now stated explicitly in the prose: "(1000ms / 120fps)" appears alongside the 8.33ms figure to make the derivation visible.
3. `<!-- CLAIM: source? -->` marker inserted noting that Apple HIG does not publicly state "16ms" as an explicit budget; the figure is derived from a 60fps target. Reviewer to either pin a deep-link section once Apple republishes a static-HTML version or substitute a citation to a WWDC session that quotes the figure directly.

**File:line:** ch11-node-architecture.md:287 (prose).

### 5. Replicache "optimistic local state always current" framing ([7]) — PASS-with-edit

**What the chapter says:** "Replicache's documentation frames the same pattern: optimistic local state is always current, and remote reconciliation is always incremental [7]." (Ch11:254)

**What the source says:** The Replicache documentation root and the "How it works" page (https://doc.replicache.dev/concepts/how-it-works) explicitly establish the pattern: "When a user takes an action in your app, the app invokes a mutator. The mutator modifies the local Replicache, and your subscriptions fire... [mutations are] synchronized to the server in batches, where they are run using the server-side mutators, updating the canonical datastore. When data changes on the server, the server pokes... and reveals it to your app." The Replicache docs frame this as: "[Replicache takes] the server round-trip off the application's critical path, and instead [syncs] data continuously in the background." The chapter's paraphrase "optimistic local state is always current; remote reconciliation is always incremental" is a faithful summary of this framing.

**Edit applied:** Citation [7] repointed from `https://doc.replicache.dev/` (root) to `https://doc.replicache.dev/concepts/how-it-works` (the deep-link page where the framing originates). Reference list entry updated to:
> [7] Replicache, "How Replicache Works," *Replicache Documentation*. Accessed: 2026. [Online]. Available: https://doc.replicache.dev/concepts/how-it-works

**Prose unchanged.** Paraphrase is faithful.

**File:line:** ch11-node-architecture.md:321 (reference list).

### 6. Per-deployment-class budget table math (§Sub-pattern 43e) — PASS-with-edit

**What the chapter said (before edit):** "The 8ms interactive budget is calibrated against the 8.33ms frame time at 120fps; sub-8ms gives one sub-frame of headroom for the UI thread's other work." (Ch11:287)

**Math verification:** 1000ms / 120fps = 8.333... ms per frame. ✓ Mathematically correct.

**Issue with prose phrasing:** "one sub-frame of headroom" is ambiguous. Sub-8ms gives roughly 0.33ms headroom, which is a small margin under the frame deadline — not "one sub-frame" in any meaningful sense. The phrasing implies a larger budget than actually exists.

**Edit applied:** Prose tightened to "(1000ms / 120fps); sub-8ms keeps the work below the frame deadline with a small margin for the UI thread's other work." The math is now stated explicitly inline so the reader can verify; "sub-frame" replaced with "small margin" (accurate) and "below the frame deadline" (specific).

**File:line:** ch11-node-architecture.md:287 (prose).

### 7. v13/v5 sourcing audit — PASS

**What the chapter says (closing paragraph):** "Performance contracts are a primitive surfaced through architectural review, not derived from the v13 or v5 source papers directly. The contract above commits the architecture to a specification-level guarantee that the source papers framed as a desirable property; the framework-level enforcement, the budget table, and the kill trigger are new architectural commitments specific to this volume." (Ch11:305)

**What v13 and v5 actually say about performance:** Comprehensive grep of both source papers for the terms `performance`, `frame`, `60fps`, `120fps`, `16ms`, `200ms`, `latency`, `budget`, `spinner`, `isolation`, `degradation`, `main thread`, `web worker`, `background thread`, `INP` returns:

- **v13 (`source/local_node_saas_v13.md`):** Uses "performance" in three contexts only — "performance optimization" (snapshots), "performance characteristics" (CRDT library evaluation), and "performance at scale" (CQRS read models). No latency budget, no main-thread isolation, no progressive-degradation specification. Uses "budget" only in `storage budget` (Section 10.3 — disk-quota budget, unrelated to time budget). Uses "frame" only in `framework` and `framework-agnostic`. No 60fps, no 16ms, no 200ms, no INP reference.
- **v5 (`source/inverted-stack-v5.md`):** References "Loro... has shown strong performance characteristics" once. References "Latency and resilience issues" as an SaaS criticism. No latency budget, no main-thread isolation, no progressive-degradation specification.

**Verdict:** The closing-paragraph self-disclosure is **accurate**. Performance contracts are not specified at the level the chapter commits to in v13 or v5. The architectural commitment in this chapter — per-operation latency budgets by class, framework-enforced main-thread isolation, progressive-degradation fallback, deployment-class calibration table, CI conformance test, kill trigger — is genuinely new in this volume.

**No edit needed.** Verdict: PASS.

---

## Consolidated CLAIM markers

Two `<!-- CLAIM: source? -->` markers were added by this technical-review pass; both are accompanied by detailed inline notes for the next reviewer:

| File | Line | Claim | Status |
|---|---|---|---|
| ch11-node-architecture.md | ~214 | Linear 60fps verbatim attribution | OPEN — verbatim source not found in iteration budget; prose softened to paraphrase |
| ch11-node-architecture.md | ~287 | Apple HIG 16ms verbatim attribution | OPEN — HIG is JS-rendered SPA, not statically indexable in iteration budget; prose softened |

Both markers are deliberate carry-forwards. The substantive technical content (the 60fps and 16ms figures themselves) is industry-standard and not in dispute; what the markers flag is that the **citation as written attributes the figure to a specific source whose published wording could not be confirmed within the iteration budget**. The next technical-review iteration can either (a) find the verbatim wording and remove the marker, or (b) accept the softened paraphrase as the final form and remove the marker on those grounds.

No CLAIM markers were removed by this pass (none were present in the draft when it entered technical-review — code-check noted that the draft's two flagged claims, items 1 and 2, were attributed via citation rather than marker).

---

## Reference list adjustments

Five edits to Ch11's reference list (all URL pins, all sub-item-1, sub-item-2, sub-item-5 adjustments documented above):

| Citation | Before | After |
|---|---|---|
| [4] Yjs | https://docs.yjs.dev/ (root) | https://github.com/dmonad/crdt-benchmarks#b4-real-world-editing-dataset (deep-link to canonical benchmark) |
| [5] Linear | https://linear.app/blog/ (root) | https://linear.app/blog/scaling-the-linear-sync-engine (specific talk page) |
| [7] Replicache | https://doc.replicache.dev/ (root) | https://doc.replicache.dev/concepts/how-it-works (deep-link to source of paraphrase) |
| [6] Web Vitals | https://web.dev/articles/inp | (unchanged — already pinned correctly) |
| [8] Apple HIG | https://developer.apple.com/design/human-interface-guidelines/ | (unchanged — HIG is SPA-rendered; deep-link unavailable in iteration budget; CLAIM marker covers the gap) |

---

## Gate decision

The technical-review → prose-review gate **passes** under the loop-plan §5 rule "All `<!-- CLAIM: source? -->` markers either resolved (URL pinned, prose adjusted) or explicitly left for follow-up with note in Output A." The two remaining markers are explicitly documented above, with detailed notes on what the next reviewer must do, and the prose has been softened so that even if the markers are never resolved, the chapter does not make a claim that overstates what the cited source publicly says.

**Verdict:** PASS-with-edit. Gate passes. Advance to prose-review.

---

## Files modified by this iteration

- `chapters/part-3-reference-architecture/ch11-node-architecture.md` — five edits (three prose tightenings, two CLAIM markers, four citation URL pins)
- `docs/book-update-plan/working/43-performance-contracts/technical-review-report.md` — this file (new)

No edits to Ch20 in this iteration. The Ch20 new section's only verifiable technical claims are cross-references to Ch11 §Performance Contracts (already verified by code-check) and to Ch19 §The Operational Runbook Minimum (cross-reference fix already applied in iter-0012). No source-paper claims in the Ch20 new section require independent verification.
