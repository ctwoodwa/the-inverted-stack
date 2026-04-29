---
type: editorial-review
chapter: ch16-persistence-beyond-the-node
date: 2026-04-29
author: PAO
audience: Yeoman (executor), CO (visibility)
status: review — proposed cuts; awaits Yeoman application after audiobook window
target-reduction: ambitious from 7,021 → 3,000 (target); realistic ~5,000 given extension #44 absorption
identified-cuts: ~600 words mechanical (deduplication with Ch12); ~600 more from editorial trim if author approves
voice-pass-locked: §Per-Data-Class Device-Distribution (1,910 words from extension #44)
---

# Ch16 (Persistence Beyond the Node) — Compression Review

## TL;DR

Current 7,021 words against 3,000 target (234%). PAO reads this as **a target-revision case more than a compression case** — extension #44 added a load-bearing 1,910-word section (§Per-Data-Class Device-Distribution) that fundamentally changed Ch16's scope. The original 3,000-word target predates that scope expansion.

**PAO recommends:**
1. **Apply mechanical compression (~600 words):** deduplication with Ch12's Five-Layer Storage Architecture and CRDT Growth & GC sections. Both topics are spec'd in Ch12; Ch16's versions duplicate.
2. **Author chooses on editorial trim (~600 more words):** Plain-File Export, Backup UX, Non-Technical Disaster Recovery sections are all substantive but trimmable.
3. **Revise the chapter target.** 5,000 words (167% of original) is the realistic landing zone after #44 absorption. Confirms the broader pattern (already flagged for CO) that original word-count targets need revision after the extension wave.

## Section-level word inventory

| § | Section | Words | Compression class | Proposed cut |
|---:|---|---:|---|---:|
| 1 | The Problem Single-Node Storage Cannot Solve | 91 | tight | 0 |
| 2 | Five-Layer Storage Architecture | 248 | **dedup with Ch12** | -200 |
| 3 | Declarative Sync Buckets | 390 | substantive | 0 |
| 4 | Lazy Fetch and Storage Budgets | 275 | substantive | 0 |
| 5 | **Per-Data-Class Device-Distribution** | **1,910** | **VOICE-PASS-LOCKED** (extension #44) | 0 (do not touch) |
| 6 | Snapshot Format and Rehydration | 398 | substantive | 0 |
| 7 | CRDT Growth and Garbage Collection | 355 | **dedup with Ch12** | -325 |
| 8 | Backup UX: Three-State Model | 660 | trim candidate | -150 (author optional) |
| 9 | Relay Architecture | 671 | partial dedup | -80 (jurisdictional endpoints → Appendix F) |
| 10 | Non-Technical Disaster Recovery | 641 | trim candidate | -150 (author optional) |
| 11 | Plain-File Export | 788 | trim candidate | -280 (author optional; move format examples to reference) |
| 12 | Layer 5 — Decentralized Archival (Phase 2) | 139 | tight | 0 |
| 13 | Summary | 210 | tight | 0 |
| 14 | References | 156 | tight | 0 |
| **Mechanical subtotal** | | | | **-605** |
| **Author-optional editorial trim** | | | | -580 |
| **Combined potential** | | | | **-1,185** |
| **After all cuts** | | | | ~5,836 (195%) |

Even with all proposed cuts, Ch16 lands at ~5,836 (195% of target). The original 3,000-word target is no longer reachable without removing extension #44's contribution — which is voice-pass-pending and locked.

## Mechanical cuts (PAO recommends auto-apply)

### Cut 1 — Five-Layer Storage Architecture deduplication (~200 words)

**Current state:** Ch16 §Five-Layer Storage Architecture (248 words) introduces the same five storage tiers Ch12 §The Five-Layer Storage Architecture (783 words) specifies in detail. The Ch16 version is a summary; Ch12 is the spec. **They restate the same five-tier model.**

**Proposed replacement (~50 words):**
> Persistence in the local-first architecture composes five tiers, specified in Chapter 12 §The Five-Layer Storage Architecture. This chapter focuses on what each tier owns operationally — bucket subscription, lazy fetch, snapshot rehydration, backup UX, relay metadata posture, and disaster recovery — assuming the reader has the five-tier model from Ch12.

**Net:** ~200 words removed. Ch12 is the canonical Five-Layer spec.

### Cut 2 — CRDT Growth and Garbage Collection deduplication (~325 words)

**Current state:** Ch16 §CRDT Growth and Garbage Collection (355 words) lists the same three mitigation strategies (library-level compaction, document sharding, periodic shallow snapshots) that Ch12 §CRDT Growth and Garbage Collection (1,887 words) specifies in detail with the three-tier GC policy. Pure duplication.

**Bonus:** The Ch16 version carries the **same nested-parenthetical duplicate** that Ch12 has at line 28:
> "...YDotNet (the .NET CRDT engine port of Yjs ([github.com/yjs/yjs](...)the JavaScript CRDT library) via Rust FFI (Foreign Function Interface)) (the .NET CRDT engine port of Yjs..."

Both chapters need the same fix.

**Proposed replacement (~30 words):**
> CRDT growth and the three-tier garbage collection policy are specified in Chapter 12 §CRDT Growth and Garbage Collection. The garbage collection tier assignment lives in the bucket's IStreamDefinition; Ch12 specifies the GC policy itself.

**Net:** ~325 words removed.

### Cut 3 — Relay Architecture jurisdictional endpoint enumeration (~80 words)

**Current text** (line 53): full enumeration of jurisdictional relay endpoints (`eu-relay.example.com` Frankfurt, `me-relay.example.com` DIFC, `in-relay.example.com` Mumbai, `ru-relay.example.com` Moscow, etc.) with regulatory citations (Schrems II, DIFC, RBI, 242-FZ).

**Proposed replacement:**
> The managed relay operates per jurisdiction; teams select the relay endpoint at onboarding to satisfy data-residency obligations (Appendix F maps jurisdictional endpoints to regulatory frameworks). Cross-jurisdiction deployments configure multiple endpoints with relay-to-relay interconnect over TLS 1.3, authenticated by operator-held relay keys.

**Net:** ~80 words removed. Appendix F is the regulatory canonical reference.

## Author-optional editorial trim

### Trim A — Plain-File Export (788 → ~510, save ~280)

The export-formats enumeration is detailed (4 formats × multi-paragraph descriptions). PAO read: this is well-pitched for a publishing-quality reference, but a leaner version could move format-specific examples to a sidebar table while keeping the architectural commitment ("export is first-class, not aspirational") intact.

### Trim B — Non-Technical Disaster Recovery (641 → ~490, save ~150)

The recovery walkthrough is narrative and includes step-by-step prose. Some of the narration repeats setup context that's already established. Trim to bullet form for the mechanical steps; keep narrative for the author-of-the-architecture commitment moments.

### Trim C — Backup UX: Three-State Model (660 → ~500, save ~160)

The three states (Protected / Attention / At Risk) are well-distinguished but the exposition has parallel structure that could compress. Keep all three states; tighten the per-state narrative.

## What PAO is NOT proposing

**§Per-Data-Class Device-Distribution (1,910 words) is voice-pass-locked.** Extension #44 is at `awaiting-voice-check` per state.yaml. This section has author-anecdote slots pending. PAO will not propose any cuts to it. After voice-pass completes, it may be appropriate to do a separate compression review on that section — defer.

## Why not pre-applied

Ch16 is in the audiobook render queue (last completed Ch08; Ch09–16 still pending). Modifying Ch16 prose during render risks unnecessary re-render cost or source-of-truth divergence. Application defers to Yeoman handoff window after audiobook completes.

## Recommended target revision

Original target: 3,000 words. After extension #44 (mandatory load-bearing addition): realistic target ~5,000 (167%). PAO recommends CO/XO ratify the revised target alongside the broader word-count target revision pending in the structure-doc word-count table (`Original target` vs `Current draft`).

If the architecture should preserve the ability to land at 3,000 words, that requires reverting #44's substantive contribution — not a compression call, a content call, and against the explicit decision to add #44 to the manuscript.

---

**End of review.** Awaiting Yeoman handoff window.
