# Draft report — #9 Chain-of-Custody for Multi-Party Transfers

**Iteration:** iter-0023
**Stage:** outline → draft
**Status:** complete; ready for code-check

---

## Files modified

1. `chapters/part-3-reference-architecture/ch15-security-architecture.md`
   - Inserted new H2 `## Chain-of-Custody for Multi-Party Transfers` between §Supply Chain Security and §GDPR Article 17 and Crypto-Shredding (line 583).
   - Updated cross-reference at line 228 (formerly "the chain-of-custody mechanism (cross-reference #9)").
   - Updated cross-reference at line 389 (formerly "Cross-reference to the chain-of-custody mechanism (#9)").
   - Appended IEEE refs [28]–[31] to the references list.

2. `chapters/appendices/appendix-b-threat-model-worksheets.md`
   - Inserted new H2 `## Section 5 — Chain-of-Custody Worksheet` after §Section 4 — Key Compromise Incident Response Template (line 237), before the appendix-wide closing italic block.

3. `docs/book-update-plan/working/9-chain-of-custody/draft.md`
   - Standalone draft for the code-checker.

---

## Word counts

| Target | Actual | Variance |
|---|---|---|
| Ch15 §Chain-of-Custody — 2,500 words | **2,394 words** | -4.2% (within ±10%) |
| App B §Section 5 — 500 words | **548 words** | +9.6% (within ±10%) |
| Combined | **2,942 words** | +4.0% over the 2,500+500 = 3,000 nominal |

Both sections land within ±10% of their declared targets.

---

## Sub-pattern coverage

All three required sub-patterns covered:

| Sub-pattern | Section | Coverage |
|---|---|---|
| 9a — Multi-party signed transfer receipt with two-signature completion | Ch15 §Sub-pattern 9a | Receipt structure, two-signature requirement (transferor + recipient device-key signatures over content hash), CRDT version-vector binding, `transfer-initiated` → `transfer-completed` → `transfer-disputed` state machine. |
| 9b — Evidence-class temporal attestation via RFC 3161 trusted timestamping | Ch15 §Sub-pattern 9b | Local-timestamp insufficiency, RFC 3161 TSA integration with TimeStampRequest/TimeStampResponse, eIDAS Article 41 qualified TSP basis, deployment-class TSA selection, offline `tsa-pending` semantics. |
| 9c — Regulatory-export streaming with Merkle-chain verifiable completeness | Ch15 §Sub-pattern 9c | Append-only Merkle commitment over event stream, signed Merkle root export per batch, real-time vs batch modes, distinction from bilateral 9a/9b (unilateral attestation to passive verifier), tension with Article 17 erasure. |

---

## Citations added

Four IEEE refs appended to Ch15 reference list:

- `[28]` IETF RFC 3161 — Time-Stamp Protocol (TSP), Aug. 2001 — cited in §Sub-pattern 9b.
- `[29]` eIDAS Regulation (EU) 910/2014 Article 41 — qualified electronic time stamps — cited in §Sub-pattern 9b.
- `[30]` Crosby & Wallach 2009 — Efficient Data Structures for Tamper-Evident Logging — cited in §Sub-pattern 9c.
- `[31]` IETF RFC 9162 — Certificate Transparency Version 2.0 — cited in §Sub-pattern 9c.

Existing citations also referenced from the new section:

- `[10]` (RFC 5280, X.509 v3) — TSA certificate verification chain.
- `[12]` (Yjs Internals) and `[13]` (Loro Common) — CRDT operation-ID / vector-clock identification.

App B Section 5 cross-references Ch15; no new citations needed in App B.

**Note on outline §G citation numbering:** the outline anticipated [14]–[17] for these refs, but #46 has already claimed [14]–[19] and #47 has claimed [20]–[27]. The user's instruction confirmed the next available number is [28]. Refs land at [28]–[31] accordingly.

---

## Namespace declaration

**New forward-looking namespace introduced:** `Sunfish.Kernel.Custody`

The HTML annotation header at the top of the new Ch15 section declares:

```
<!-- code-check annotations: Sunfish.Kernel.Custody (NEW namespace, not in canon — forward-looking); Sunfish.Kernel.Audit (forward-looking from #48). 0 class APIs / method signatures introduced. -->
```

Per outline §G.4 reasoning:

1. Bilateral external-party co-authorship of receipts differs from single-node-signed audit records (`Sunfish.Kernel.Audit` is single-author).
2. RFC 3161 TSA integration belongs to a dedicated package — folding it into a general-purpose audit log creates a hybrid log with two distinct external dependencies.
3. The two packages compose without merging; existing `Sunfish.Kernel.Audit` references in #48 and #45 remain unchanged.

**No class APIs or method signatures introduced.** The four named event contracts (`CustodyTransferInitiated`, `CustodyTransferConfirmed`, `CustodyTransferDisputed`, `RegulatoryExportBatch`) are event-record names, not class or method definitions; they parallel the existing event-contract naming convention in §Key-Loss Recovery and §Collaborator Revocation.

**Action item for code-check stage:** the sunfish-package-roadmap.md anticipatory entry for #9 needs promotion from `Future forward-looking namespaces` to a first-class roadmap entry with status `book-committed`, namespace `Sunfish.Kernel.Custody`, source extension #9.

---

## Cross-references

All cross-references from outline §H wired:

| From | To | Direction |
|---|---|---|
| Ch15 §Chain-of-Custody | Ch15 §Key-Loss Recovery sub-pattern 48f | Backward — substrate sharing |
| Ch15 §Chain-of-Custody | Ch15 §Collaborator Revocation sub-pattern 45f | Backward — substrate sharing |
| Ch15 §Chain-of-Custody | Ch15 §Endpoint Compromise: What Stays Protected | Backward — receipt verifiability not dependent on custodian endpoint integrity |
| Ch15 §Chain-of-Custody | Ch15 §Collaborator Revocation | Backward — per-party key isolation foundation for the two-signature attack analysis |
| Ch15 §Chain-of-Custody | Ch15 §GDPR Article 17 and Crypto-Shredding | Forward — erasure / append-only stream tension |
| Ch15 §Chain-of-Custody | App B §Section 5 | Sideways — operational worksheet |
| App B §Section 5 | Ch15 §Chain-of-Custody | Sideways — architectural specification |

**Retroactive updates applied:**

- Line 228 (in §Recovery-event audit trail): `the chain-of-custody mechanism (cross-reference #9)` → `§Chain-of-Custody for Multi-Party Transfers`
- Line 389 (in §Sub-pattern 45f Revocation-event audit trail): `the chain-of-custody mechanism (#9)` → `§Chain-of-Custody for Multi-Party Transfers`

Both former forward-references-to-a-gap are now live cross-references to the delivered section. Confirmed via post-edit grep: `chain-of-custody mechanism \(#9\)|cross-reference #9` returns 0 hits in the chapter.

---

## FAILED conditions

A standalone `### FAILED conditions` subsection sits in the new Ch15 section (line 649). The three conditions:

1. A transfer receipt is accepted as complete with only one signature (architecture failure, voids 9a).
2. A chain-of-custody event does not appear in the encrypted audit log (architecture failure, voids substrate guarantee).
3. A regulatory-export stream is accepted as complete without a Merkle-chain verification step (compliance failure, voids 9c).

Each condition includes its severity classification and which sub-pattern it voids. The block follows the same pattern as #45's and #46's existing FAILED-conditions subsections.

---

## Kill trigger

A single sentence specifying the architecture-invalidating condition appears at the end of the FAILED conditions block:

> The kill trigger for this primitive is a transfer receipt that closes as `transfer-completed` without a verifiable second signature traceable to the recipient's published key. A primitive that cannot guarantee the second signature has not been forged is not a chain-of-custody primitive — it is a logbook with extra ceremony.

---

## CLAIM markers

**One CLAIM marker inserted** (within the loop-plan policy of ≤1 per extension):

Location: §Sub-pattern 9b — Evidence-class temporal attestation, end of the RFC 3161 paragraph.

Marker text:

```
<!-- CLAIM: source? — the two-signature receipt construction with TSA anchoring at this granularity is a new architectural commitment from design-decisions §5 #9; v13/v5 reference chain-of-custody only as a forward gap. -->
```

Rationale: per outline §D, the two-signature transfer-receipt construction is not derived from v13 or v5 — it is a new architectural commitment surfaced through the chain-of-custody gap analysis. The technical-review pass should confirm the construction against design-decisions §5 #9 and either retire the marker (if v13/v5 contain a precedent the outline missed) or convert it to a `<!-- design-decisions: ... -->` reference annotation.

---

## Voice / register compliance

- **Register:** Part III specification voice. Active throughout. No hedging. No academic scaffolding ("this section presents", "as we have seen", "it should be noted").
- **Paragraphs:** All paragraphs ≤ 6 sentences (sub-pattern 9a's largest paragraph is 5 sentences; threat-model bullets are 4–5 sentences each).
- **No re-introducing the architecture:** the new section assumes Part I and earlier Ch15 sections are read. Key hierarchy, admin event channel, CRDT log structure, and `Sunfish.Kernel.Audit` are referenced without re-describing.
- **Lead with concrete:** the section opens with a commercial-driver dashcam scenario, not with "Chain-of-custody is..." abstract definition. The legal-distinction punchline ("only the second claim survives discovery") lands in the second paragraph. Voice-check stage may add or expand the dashcam anecdote per outline §F.
- **Em-dashes / boldface / hyphenated technical terms:** preserved per book convention (anti-AI-tells calibration §1).
- **No invented APIs:** no class names, no method signatures. Only namespace name `Sunfish.Kernel.Custody` and event-record names (`CustodyTransferInitiated` etc.).

---

## Deviations from outline

**Citation numbering:** outline §G specified [14]–[17]. Actual: [28]–[31]. Reason: #46 and #47 already claimed [14]–[27]; per user instruction, next available was [28]. No content change — same four citations, same primary sources, same in-text positions.

**Word counts:** outline §A targeted ~2,000 words for Ch15; user instruction targeted ~2,500 (state.yaml estimate). Actual landed at 2,394 — within ±10% of the user-instructed 2,500 target. The tighter outline targets per sub-section (200/150/450/450/350/200/150) were treated as guidance; actual sub-section lengths were calibrated to the active-voice rewrite cadence rather than mechanical word allocation.

**App B word target:** outline §B targeted ~500 words; user instruction also ~500. Actual: 548 (+9.6%). Within ±10%; the seven-field structure with table headers and checklist items inflates the word count modestly above the outline's compressed estimate.

**App B field structure:** the outline §B.1–B.4 structure proposed four sub-sections (purpose, transfer-class inventory, deployment checklist, incident response). The user's required field structure (1) parties, (2) data class, (3) transfer trigger, (4) signing requirements, (5) timestamping, (6) verification, (7) escalation paths is finer-grained and field-oriented. Actual delivery follows the user's required field structure. The transfer-class inventory table from outline §B.2 was absorbed into Field 2 (Data class); the deployment checklist from outline §B.3 was distributed across Fields 4–6; the incident response from outline §B.4 became Field 7. All checklist substance is preserved; the navigation is field-oriented rather than process-oriented.

---

## QC checklist self-assessment

- [x] **QC-1** Word count within ±10% of target — Ch15 -4.2%, App B +9.6%.
- [x] **QC-2** Every topic in the outline is addressed — sub-patterns 9a/9b/9c, threat model, FAILED conditions, kill trigger, implementation surfaces, App B worksheet.
- [x] **QC-3** Source sections cited inline — refs [10], [12], [13], [28], [29], [30], [31] used in body.
- [x] **QC-4** Sunfish packages referenced by name only — no class APIs, no method signatures. Event-record names parallel existing chapter convention.
- [x] **QC-5** No academic scaffolding — verified via grep for "this section", "as we have seen", "we present", "it should be noted" — 0 hits in new section.
- [x] **QC-6** No re-introducing the architecture — substrate references (key hierarchy, audit log, DAG continuity) cite earlier sections without re-describing.
- [x] **QC-7** Part III specification voice held; tutorial detours absent.
- [x] **QC-9 (n/a)** Council two-act structure not applicable (Part III chapter).
- [x] **QC-10** No placeholder text — verified via grep for "TBD", "expand here", "see paper for details" — 0 hits.

---

## Handoff to code-check stage

The next iteration (`draft → code-check`) should validate:

1. Sunfish package canon update — promote `Sunfish.Kernel.Custody` anticipatory entry to first-class status in sunfish-package-roadmap.md (book-committed; source extension #9).
2. Event-contract naming — confirm `CustodyTransferInitiated` / `CustodyTransferConfirmed` / `CustodyTransferDisputed` / `RegulatoryExportBatch` align with the existing event-contract naming convention in `Sunfish.Kernel.Audit` (#48) and `Sunfish.Kernel.Sync` namespaces.
3. CLAIM marker resolution — technical-reviewer confirms two-signature + TSA construction against design-decisions §5 #9 and v13/v5; retires the marker or converts to a design-decisions reference annotation.
4. Concept-index extraction — generate `docs/reference-implementation/_per-chapter/ch15-security-architecture.yaml` and `appendix-b-threat-model-worksheets.yaml` updates capturing the new concepts (transfer-receipt, two-signature primitive, RFC 3161 TSA integration, Merkle-chain regulatory export, custody dispute state machine).
