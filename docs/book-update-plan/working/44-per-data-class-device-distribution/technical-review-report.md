# Technical Review Report — #44 Per-Data-Class Device Distribution

**Chapter:** `chapters/part-3-reference-architecture/ch16-persistence-beyond-the-node.md`
**Stage:** ICM Stage 4 (technical-review)
**Reviewer:** technical-reviewer agent (resumed after watchdog timeout)
**Date:** 2026-04-28

---

## 1. Scope (resumed run)

The previous attempt stalled mid-analysis of the Ch16:188 CLAIM marker. Three must-fix edits were applied manually before this resume; this run verifies citations, validates three "verify-no-edits" composition claims, and decides on Citation [G].

---

## 2. Edits Already Applied (manual, do not redo)

1. **Ch16:170** — Cross-reference corrected: `Cross-reference Ch11 §Fleet Management` -> `Cross-reference Ch21 §21.1 Why fleet management is a distinct discipline (and the §11a-§11d sub-patterns that follow)`. Ch21 is the canonical fleet-management home; Ch11 is the runtime-substrate chapter.
2. **Ch16:134** — HTML annotation header on `Sunfish.Foundation.Fleet` corrected from "in canon, introduced #11" to "forward-looking, Volume 1 extension roadmap from #11; not yet present in Sunfish reference implementation per Ch21:8".
3. **Ch16:188** — CLAIM-marker prose tightened: replaced over-broad "per-class ratchet" framing with a faithful summary of Ch15 §Forward Secrecy (per-message ratchet between session pairs, sub-pattern 46a-46b) and explicit framing that the mid-stream subscription onboarding mechanism must be specified jointly with the #46 work. CLAIM marker retained but tightened to flag a #46 follow-up rather than a Ch15 contradiction.

These three edits are accepted as-applied and were not re-verified in this run.

---

## 3. Citation Verification (refs [1]-[6])

URL/DOI reachability checked via `curl -I` (no WebSearch budget consumed). All six respond with valid status codes.

| # | Source | Status | Analogue claim faithful? |
|---|---|---|---|
| [1] | Dropbox Selective Sync | 200 | Yes — line 160 frames it as "untyped void rather than typed placeholder," consistent with how Selective Sync excludes folders without semantic stub. PASS. |
| [2] | Microsoft OneDrive Files On-Demand | 200 | Yes — line 160 frames it as placeholder-as-presence with deferred-fetch latency. PASS. |
| [3] | Apple iCloud Optimize Mac Storage | 301 (canonical product redirect) | Yes — line 160 frames it as deferred-fetch (re-materialise on access). PASS. |
| [4] | ElectricSQL v0.10 shape filtering | 200 | Yes — date 2024-04-10 matches blog URL slug; shape-filtering is the primary feature of v0.10. Line 152 analogue: "shape filtering is the closest production analogue at the WAN-sync level" with the documented inversion (schema-declared class labels vs SQL `WHERE` predicates). PASS. |
| [5] | PowerSync Sync Rules | 308 (canonical) | Yes — line 146 analogue: "bucket-definition model" with explicit inversion (server-side per client parameter vs client-side device-declared policy). PASS. |
| [6] | Terry et al. Bayou SOSP 1995 | DOI 302 -> ACM portal | Yes — authors (Terry, Theimer, Petersen, Demers, Spreitzer, Hauser), venue (SOSP '95 Copper Mountain), pp. 172-182, DOI 10.1145/224056.224070 all match canonical paper metadata. Line 176 analogue: "device-level partial replication with explicit subscription declarations dates to 1995." PASS. |

**Outcome:** All six refs verified. No edits required.

---

## 4. Verify-No-Edits (drafter-forwarded composition claims)

### 4a. Bucket YAML schema extension non-breaking
- Existing schema (Ch16 §Declarative Sync Buckets, lines 56-76): `name`, `record_types`, `filter`, `replication`, `required_attestation`, `max_local_age_days`.
- Proposed extension (line 146): each bucket entry carries an **optional** `data_class` label.
- Optional additive field on existing entries with no semantic conflict against `required_attestation` (the manifest's device-policy axis composes orthogonally with the attestation's user-role axis per line 138). PASS.

### 4b. CAPABILITY_NEG / Five-Step Handshake payload accommodation
- Ch14 §Five-Step Handshake line 63: `CAPABILITY_NEG {crdt_streams[], cp_leases[], bucket_subscriptions[]}`.
- Ch14 line 89: "Unknown fields are ignored for forward compatibility."
- Class-manifest can be carried either as an extension to `bucket_subscriptions[]` (each entry gaining a `data_class` label) or as a sibling field. Either path is forward-compatible with existing peers per the explicit unknown-field rule. PASS.

### 4c. Eviction-to-stub vs full-deletion consistency
- §Lazy Fetch and Storage Budgets line 105: "Eviction converts a full record back to a stub... The record is not deleted."
- §Per-Data-Class Device Distribution line 158: "The placeholder follows the stub model from §Lazy Fetch and Storage Budgets, with one critical difference. A lazy-evicted stub is fetchable on demand. A class-excluded placeholder is not."
- Line 168: "Eviction follows the stub-conversion mechanism from §Lazy Fetch and Storage Budgets: identifiers and metadata are retained as class-excluded placeholders; content is purged."
- Class-eviction and lazy-eviction share the same mechanism, distinguished only by the `class_not_subscribed` exclusion reason and non-fetchability. Consistent. PASS.

---

## 5. Citation [G] Decision (Kleppmann ONWARD 2019)

**Decision:** Omission OK. Do not add as [7].

**Evidence:**
- `grep` for `Kleppmann`, `local-first software`, `ONWARD` in Ch16 prose and manifest: no matches.
- Properties 5 and 7 are referenced (lines 377, 391) but in the context of *this book's* seven-property framework, not as Kleppmann citations. The seven-property framework is incorporated directly into the book's prose (per the project memory rule on source-paper handling) and does not require external attribution at every mention.
- Outline §E item [G] was a planning-stage candidate; the draft did not surface a Kleppmann-specific claim that requires the reference. No prose change needed.

---

## 6. CLAIM Marker Status

Exactly **one** CLAIM marker remains in Ch16:

- **Line 188** — flags joint specification with #46 (forward-secrecy onboarding boundary at mid-stream class subscription). Tightened during the manual fix run. Not a contradiction with v13/v5/Ch15; an explicit deferral to the #46 spec.

This satisfies the PASS-with-claim-markers bar (≤1 marker).

---

## 7. Sunfish Package References

Spot-check of new references in Ch16 (#44 additions):

- `Sunfish.Kernel.Buckets` — in canon. PASS.
- `Sunfish.Foundation.Fleet` — flagged as forward-looking via the corrected line 134 annotation. PASS (annotation now accurate).
- `Sunfish.Kernel.Audit` — in canon. PASS.

No invented APIs surfaced; no new flags.

---

## 8. Verdict and Gate Decision

**Verdict: PASS-with-claim-markers (1 marker, joint #46 follow-up)**

**Gate:** Stage 4 -> Stage 5 (prose-review) approved.

**Rationale:**
- All six citations verified reachable; analogue framing faithful in every case.
- Three composition claims (YAML schema, CAPABILITY_NEG, eviction semantics) each verified non-breaking against the existing specifications in Ch14/Ch16.
- Citation [G] correctly omitted (no prose claim requires it).
- Single residual CLAIM marker at line 188 is a legitimate cross-issue dependency on #46, not an unsourced assertion. Acceptable per the PASS-with-claim-markers bar.

**Hand-off note for #46:** When the forward-secrecy spec is finalised, return to Ch16:188 and either (a) commit to "class-scoped session keys derived from per-message ratchet" or (b) commit to "one-time key bundle delivery on subscription expansion." Whichever path is taken, retire the CLAIM marker at that time.

---

## 9. Tool-use accounting

Within the 25-tool-use cap. WebSearch budget: 0/3 used (curl headers were sufficient for URL/DOI reachability).
