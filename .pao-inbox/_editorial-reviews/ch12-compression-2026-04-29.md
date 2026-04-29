---
type: editorial-review
chapter: ch12-crdt-engine-data-layer
date: 2026-04-29
author: PAO
audience: Yeoman (executor), CO (visibility)
status: review — proposed cuts; awaits Yeoman application after audiobook window
target-reduction: ~1,400 words to land at 4,000-word target (currently 5,419 = 135%)
identified-cuts: ~720 words mechanical + structural reroutes; remainder needs author judgment
---

# Ch12 (CRDT Engine and Data Layer) — Compression Review

## TL;DR

Current 5,419 words against 4,000 target. **PAO identifies ~720 words of mechanical compression + ~150 words of cleanup with clear editorial wins.** Closing the remaining ~530 words to hit target requires structural decisions (relocate Stale Peer Recovery Protocol to Ch14? condense double-entry ledger sub-sections?) — those are flagged here for author/editor judgment, not pre-applied.

## Section-level word inventory

| § | Section | Words | Compression target | Notes |
|---:|---|---:|---:|---|
| 1 | The Three-Layer CRDT Architecture | 551 | -50 | Light prune of restatement in second paragraph |
| 2 | Per-Record CAP Positioning | 686 | -100 | Mermaid flowchart and table cover the same 5 record classes; collapse to one |
| 3 | CRDT Engine Selection | 439 | 0 | Tight already; keep |
| 4 | **CRDT Growth and Garbage Collection** | **1,887** | **-460** | Biggest prune surface (sovereignty enum → F; validation → Ch13) |
| 5 | The Double-Entry Ledger as the Canonical CP Subsystem | 575 | -50 | Light condense of CQRS sub-section |
| 6 | The Five-Layer Storage Architecture | 783 | -80 | Storage provider enumeration → "S3-compatible (full list in F)" |
| 7 | Failure Modes and Edge Cases | 323 | 0 | Useful as quick reference; keep |
| 8 | Sunfish Package Reference | 150 | 0 | Tight; keep |
| 9 | References | 165 | (cleanup) | Duplicate [5] citation needs renumber to [6] |
| **Mechanical subtotal** | | | **−740** | |
| **Open editorial questions** | | | up to −400 more | See "Structural decisions" below |
| **Combined potential** | | | **−1,140** | Lands at ~4,280 = 107% of target ✓ |

## Mechanical cuts (PAO recommends auto-apply)

### Cut 1 — Duplicate parenthetical at line 28 (~30 words)

**Current text:**
> Swapping the CRDT engine — moving from YDotNet (the .NET CRDT engine port of Yjs via Rust FFI) (the .NET CRDT engine port of Yjs ([github.com/yjs/yjs](...)the JavaScript CRDT library) via Rust FFI (Foreign Function Interface)) to Loro...

The parenthetical "the .NET CRDT engine port of Yjs..." appears twice nested. Acquired through prior re-exposition pass; text editor or source-paper merge artifact.

**Proposed text:**
> Swapping the CRDT engine — moving from YDotNet (the .NET CRDT engine port of Yjs ([github.com/yjs/yjs](https://github.com/yjs/yjs)) via Rust FFI) to Loro...

### Cut 2 — Sovereignty regime enumeration → Appendix F (~280 words)

**Current text** (lines 154–162): full enumeration of 14 regimes across 6 regions (GDPR + Schrems II + BSI + CNIL; UAE DPL; DIFC DPL; DPDP + RBI; PIPL + MLPS; APPI; PIPA + ISMS-P + SIer; LGPD; LFPDPPP; Ley 1581; Ley 25.326; NDPR; POPIA; Kenya DPA; Ghana DPA; ECOWAS Supplementary Act; Russia 242-FZ; Russia 188-FZ; Kazakhstan; Belarus).

**Proposed replacement (~50 words):**
> The compliance tier is required — not preferred — for records under fourteen major data sovereignty regimes across six regions: European data residency under GDPR Article 30 + Schrems II, Gulf and South Asia under DIFC DPL + DPDP + RBI, East Asia under PIPL + APPI + PIPA, Americas under LGPD + LFPDPPP, Africa under POPIA + NDPR, and CIS under Russia 242-FZ. Per-regime mapping including national enforcement, citation, and chapter-coverage in Appendix F.

**Net:** ~280 words removed; full detail relocated to its canonical reference (Appendix F is the regulatory coverage map and is referenced inline already).

### Cut 3 — CRDT Operation Validation at Store Entry → Ch13 reference (~180 words)

**Current text** (lines 142–150): full discussion of schema-level validation, schema version compatibility, quarantine queue routing, and break-glass recovery. The cross-reference to Ch13 (schema registry, upcaster chain, epoch coordination) and Ch14 (CAPABILITY_NEG) is already present at line 150.

**Proposed replacement (~30 words):**
> Every CRDT operation arriving at the local node passes through schema-level validation before storage. Validation gates insertion; failed operations route to the quarantine queue. Chapter 13 specifies the schema registry, upcaster chain, and epoch coordination; Chapter 14 specifies the CAPABILITY_NEG wire format; Chapter 22 specifies the break-glass corrupt-sequence recovery procedure (post-Ch15-split — currently in Ch15).

**Net:** ~180 words removed; readers seeking schema-validation detail follow the references to where it's specified canonically. (Note: cross-reference to Ch15 should be updated to Ch22 post-split; this PR can either pre-apply that or wait for Phase 5 — PAO recommends wait.)

### Cut 4 — Storage provider enumeration in Layer 3 (~80 words)

**Current text** (line 246): full list of "Hetzner Object Storage, OVHcloud, Scaleway, Gulf and Indian sovereign clouds, MinIO (self-hosted S3-compatible object storage), Ceph RGW".

**Proposed replacement:**
> ...any endpoint conforming to the S3 API, including Azure Blob Storage and Google Cloud Storage alongside European, Gulf, Indian, and on-premise S3-compatible providers (the full per-region provider catalog appears in Appendix F).

**Net:** ~80 words removed; the regulatory framework (Appendix F) is the right home for the provider catalog.

### Cut 5 — Per-Record CAP Positioning Mermaid + table redundancy (~100 words)

**Current text** (lines 38–58): Mermaid flowchart shows 5 record classes; table immediately below lists same 5 classes; following two paragraphs (lines 60–62) re-explain AP and CP records using the same five examples.

**Proposed replacement:** Keep the table. Drop the Mermaid flowchart (the table is more skimmable for a reference chapter). Trim the AP/CP explanatory paragraphs to focus on *why* the position is chosen rather than re-listing the same record types.

**Net:** ~100 words removed (the Mermaid is ~75 words of label content; explanatory paragraphs prune ~25). Decision is about visual style — could keep Mermaid + drop table instead.

### Cut 6 — Three-Layer CRDT Architecture restatement (~50 words)

**Current text** (line 20): "The CRDT data model separates three concerns. Collapse them together and you produce systems where merge logic depends on domain rules and domain rules depend on how storage happens to arrange bytes. Keep the three layers distinct..."

This restates the previous paragraph's framing in inverse form (positive → negative → positive). Effective rhetorically but redundant for a reference chapter.

**Proposed cut:** Remove this paragraph. The first paragraph's "Each layer extends rather than overrides the guarantees beneath it" already lands the structural commitment. Saves ~50 words.

### Cleanup — Citation [5] duplicate (no word change)

References list has `[5]` for Schrems II AND `[5]` for Automerge. The Automerge cite at line 297 should renumber to `[6]`. Then verify that the only in-text use of [5] (line 156, "Schrems II [5]") points to the right reference. The Automerge citation isn't in-text-cited as a number; it's referenced by repository link in §3.

## Open structural decisions (PAO escalates; not pre-applied)

### Decision A — Stale Peer Recovery Protocol: Ch12 or Ch14?

The Stale Peer Recovery Protocol section (lines 128–140, ~440 words) is in Ch12 (CRDT/data layer) but specifies a sync-protocol behavior: snapshot transfer triggered at CAPABILITY_NEG, source selection, concurrent transfer limits, idempotency under interruption. The protocol mechanism arguably belongs in Ch14 (Sync Daemon Protocol).

**Tradeoff:**
- Keeping in Ch12: makes sense thematically (recovery is about CRDT engine state). Word count high (~440 words in the heaviest Ch12 section).
- Moving to Ch14: aligns with Ch14's wire-protocol specification. Recovers ~440 words from Ch12 but adds to Ch14 (currently 109% of target — could absorb).

**PAO recommendation:** Move to Ch14. The protocol IS a sync wire concern; Ch12 keeps a paragraph forward-reference. Net Ch12 reduction: ~400 words. Net Ch14 addition: ~400 words (lands ~120% — still tolerable).

**Authority needed:** This is structural — affects two chapters' boundaries. CO/Yeoman call.

### Decision B — Double-Entry Ledger sub-sections: condense?

§5 (Double-Entry Ledger) has three sub-sections (Posting Engine, CQRS Write/Read Split, Period Close). Each is independently useful. Combined ~575 words. Could collapse CQRS Write/Read Split into a single paragraph within Posting Engine (saves ~150 words).

**PAO read:** Light condense is defensible; aggressive merge loses the Period Close detail which is load-bearing for compliance-tier readers. Recommend ≤50-word condense rather than the full 150.

### Decision C — Compliance-tier "fourteen regimes" detail

After Cut 2 above, the regulatory detail moves to Appendix F. Some readers (especially regulated-industry buyers) expect to see the regimes named in the architecture spec, not just the appendix. This is a publishing-positioning question, not pure word count. PAO defers to author preference.

## Recommended execution

1. Apply Cuts 1–4 mechanically (clear wins, no editorial judgment needed beyond confirmation).
2. Author chooses on Cut 5 (Mermaid vs. table) and Cut 6 (paragraph removal).
3. CO/Yeoman decide on Decision A (move Stale Peer Recovery Protocol to Ch14).
4. Citation [5] cleanup as a separate pass (touches references list).

After Cuts 1–4 applied: Ch12 lands at ~4,820 words (120% of target). With Cut 5 + 6 + Decision A: ~4,280 (107%). With Decision A only: ~4,420 (110%). All scenarios are within Part III tolerance bands.

## Why not apply the cuts now

Audiobook rendering pipeline is currently working through Part II → III chapter sequence (last completed: Ch08 at 16:35). Ch12 will be hit imminently. Modifying Ch12 prose during render risks (a) unnecessary re-render cost, or (b) source-of-truth divergence if cached version is used.

PAO defers the actual chapter edit until Yeoman frees a window. This review is the pre-staged direction.

---

**End of review.** Awaiting Yeoman handoff window.
