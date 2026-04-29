# Prose-review report — #9 Chain-of-Custody for Multi-Party Transfers

**Iteration:** iter-0027
**Date:** 2026-04-28
**Stage advance:** technical-review → prose-review
**Verdict:** PASS

---

## Scope

Strict scope per dispatch:

- `chapters/part-3-reference-architecture/ch15-security-architecture.md` — §Chain-of-Custody for Multi-Party Transfers (H2 starting line 583, ending before §GDPR Article 17 and Crypto-Shredding at line 674). ~2,394 words.
- `chapters/appendices/appendix-b-threat-model-worksheets.md` — §Section 5 — Chain-of-Custody Worksheet (lines 237–300). ~548 words.

Out of scope (sealed): §Forward Secrecy (refs [14]–[19]); §Endpoint Compromise (refs [20]–[27]); §Supply Chain Security; refs [1]–[27] in the Ch15 reference list; the HTML annotation header at Ch15:585.

---

## 1. Edits applied — Ch15

### Edit 1 — Line 621 paragraph split (paragraph length cap)

**Before:** Single paragraph, 7 sentences (over 6-sentence cap).

**After:** Split at the sentence boundary between the TSA-introduction-with-EU-framing and the protocol-mechanics. The eIDAS Article 41 framing the technical-reviewer corrected at iter-0026 is preserved verbatim; only the paragraph break moves. The `<!-- design-decisions: §5 #9 + §8.2 -->` annotation moves with the second paragraph (it documents the protocol commitment, which is the second paragraph's subject).

**Categories addressed:** paragraph length (≤6 sentences); structural rhythm (TSA service definition vs. protocol mechanics now read as separate beats).

**Preservation honored:** eIDAS Article 41 / Article 42 sentence preserved verbatim per tech-review preservation flag; design-decisions annotation preserved verbatim.

### Edit 2 — Line 633 weak-verb / passive-victim phrasing

**Before:**
> As each event is appended to the export log, its hash incorporates into a running Merkle root. The root signs and exports alongside each event batch. ... Any omission or reordering breaks the Merkle chain and is detectable on the regulator's side without requiring any cooperation from the operator.

**After:**
> As each event lands in the export log, the export pipeline folds its hash into a running Merkle root. The pipeline signs the root and emits it alongside each event batch. ... Any omission or reordering breaks the Merkle chain, and the regulator detects the gap without requiring any cooperation from the operator.

**Categories addressed:**

- **Active voice / agency vocabulary** — "the export pipeline folds" replaces "incorporates into" (passive-victim, no agent). "The pipeline signs the root and emits it" replaces "The root signs and exports alongside" (the root cannot sign itself; the pipeline performs both acts).
- **Strong verbs** — `lands`, `folds`, `emits` over `is appended`, `incorporates into`, `exports alongside`.
- **Active voice on detection clause** — "the regulator detects the gap" replaces "is detectable on the regulator's side."

**Preservation honored:** The Crosby–Wallach [30] + RFC 9162 [31] citations sit on the prior sentence and remain untouched; technical content (Merkle-tree commitment, append-only construction, root chain consistency) is unchanged.

---

## 2. Edits applied — App B

### Edit 3 — Line 280 passive-victim phrasing

**Before:** "Record the TSA certificate fingerprint locally so a substituted endpoint is detectable."

**After:** "Record the TSA certificate fingerprint locally so the verifier detects a substituted endpoint."

**Categories addressed:** active voice (the verifier is the agent of detection); agency vocabulary ("is detectable" → "the verifier detects").

---

## 3. Edits considered but not applied

### Ch15:645 honesty-bound — TSA absence

**Sentence:** "Deployments without a TSA anchor have no defense against local-clock manipulation, and the compliance posture must declare this honestly."

**Decision:** Not touched. Tech-reviewer at iter-0026 explicitly flagged: "preserved verbatim. Prose-reviewer is on notice not to soften." This sentence is the explicit-honesty discipline naming protection that lapses rather than letting it fail silently. The phrasing is sharp, declarative, and earns its place. Honored.

### Ch15:621 eIDAS Article 41 / Article 42 sentence

**Sentence:** "...under EU deployments, a qualified trust service provider (QTSP) issuing qualified electronic time stamps to which eIDAS Article 41 [29] attaches the legal presumption of accuracy and integrity (the technical requirements for qualified time stamps live in Article 42)..."

**Decision:** Not touched. Tech-reviewer just corrected this at iter-0026 to fix a material factual issue (Article 41 governs legal effect; Article 42 holds the technical requirements). The phrasing is now technically precise and load-bearing. Prose-reviewer scope is structural (the surrounding paragraph break) — not the sentence's content. Honored.

### Ch15:621 design-decisions annotation

**Annotation:** `<!-- design-decisions: §5 #9 + §8.2 — two-signature transfer receipt + RFC 3161 TSA anchoring is the architectural commitment surfaced at design-decisions §5 entry #9 ("multi-party signed transfer receipts, evidence-class temporal attestation"); §8.2 explicitly defers the formalization of multi-party signed transfer receipts to this writing task. -->`

**Decision:** Preserved verbatim. The annotation is the resolution of the prior CLAIM marker and documents the design-decisions provenance for the construction. Moved with the second paragraph in the split (the protocol mechanics paragraph) since the annotation documents the architectural commitment that paragraph specifies. Honored.

### Ch15:585 HTML annotation header

**Decision:** Not touched. Out-of-scope per dispatch. Tech-reviewer noted `Sunfish.Kernel.Audit` is in canon and the annotation's "forward-looking from #48" framing is mismatched, but a separate cleanup task tracks this.

### Sub-pattern labels (§9a, §9b, §9c)

**Decision:** Preserved verbatim. House style for intra-section cross-references; do not renumber.

### App B §Section 5 worksheet/checklist register

**Decision:** Preserved as worksheet/checklist register. The tables, checklists, and numbered escalation steps are deliberately not prosified. Only one prose sentence in the section needed an active-voice fix (Edit 3 above).

### Ch15:623 AdES inline phrase

**Sentence:** "Regulated deployments — those that produce evidence in legal proceedings, satisfy eIDAS AdES (Advanced Electronic Signature) requirements for evidence preservation, or comply with sector-specific record-keeping standards — declare a qualified TSA in their compliance posture."

**Decision:** Not touched. Tech-reviewer flagged this as "non-blocking" optional tightening (AdES is technically Articles 26–34; preservation services are Article 34). Three considered rewrites:

1. Drop AdES expansion → loses the regulated-industry signal vocabulary.
2. Add Article numbers ("eIDAS qualified-preservation requirements (Articles 26–34)") → adds noise without sharpening for the practitioner audience.
3. Re-order ("eIDAS evidence-preservation requirements for advanced electronic signatures") → loses the AdES term, which is the load-bearing acronym in regulated procurement.

None sharpens the sentence. The current phrasing communicates the load-bearing trigger correctly (regulated-evidence-preservation requirements are the trigger for declaring a qualified TSA). Tightening this requires a structural rewrite outside prose-review scope. Skipped.

### Ch15:587 opening paragraph (6 sentences, at cap)

**Decision:** Not touched. The paragraph is at cap, not over. Sentences are tight, the dashcam scenario establishes the load-bearing problem in concrete terms (Part III specification voice with a concrete entry case), and the closing two-line punch ("A timestamp database can record both facts. It cannot defend them.") earns the length. No change.

### Line 587 narrative scenario in Part III

**Decision:** Preserved. Part III is specification voice, but a single concrete scenario at section opening grounds the abstraction without violating register. The transition into "The audit trails specified in §Key-Loss Recovery sub-pattern 48f and §Collaborator Revocation sub-pattern 45f rest on the same substrate this section specifies" snaps back to spec voice immediately. House pattern preserved across the chapter (cf. §Endpoint Compromise opening, §Forward Secrecy opening).

---

## 4. Standard checklist run

| Check | Result | Notes |
|---|---|---|
| Paragraph length cap (≤6 sentences) | 1 violation found and fixed | Line 621 was 7 sentences; split. |
| Active voice | 2 violations found and fixed | Line 633 (Merkle pipeline), App B line 280 (substituted endpoint). |
| Strong verbs / no weak verbs | Fixed alongside active-voice pass | `lands`, `folds`, `emits`, `detects`. |
| Academic scaffolding | None found | No "this section argues", "as we have seen". |
| There-is constructions | None found | Section is clean. |
| Hedging as default | None found | "must declare this honestly" is intentional honesty-bound, not hedge. |
| Synonym cycling | None found | TSA / QTSP are distinct technical terms; transferor/recipient are roles, not synonyms; Merkle commitment / root / chain / tree are technically distinct usages. |
| Anti-AI tells §1 (puffery) | None found | No "stands as", "pivotal", "indelible". |
| Anti-AI tells §3 (-ing tail-phrases) | None load-bearing-free | Line 633 "without requiring any cooperation from the operator" is load-bearing — names the structural property of the Merkle proof. Kept. |
| Anti-AI tells §8 (copula avoidance) | None | No "serves as a", "stands as a", "marks a", "boasts" misuse. |
| Anti-AI tells §16 (significance puffery) | None | |
| Anti-AI tells §17 (title case in headings) | H3/H4 sentence case ✓ | H2 title case is chapter-wide house style for Ch15 (cf. all peer H2s). Not flagged. |
| Anti-AI tells §27 (persuasive authority tropes) | None | Line 609 "is not stylistic" is the **good** version: declarative claim, not "what really matters." |
| Anti-AI tells §29 (fragmented headers) | None | Every H3 is followed by substantive first sentence, not a restatement of the heading. |
| Internal extension number leaks | None | Section uses named cross-references (`§Key-Loss Recovery sub-pattern 48f`, `§Collaborator Revocation sub-pattern 45f`, `§Endpoint Compromise`). No bare `(#9)`/`(#48)`/`(#45)`/`(#47)` parentheticals. Sub-pattern labels (§9a/§9b/§9c) are intra-section labels per house style — preserved. |
| Restatements | None | Section economical. |

---

## 5. Voice-register confirmation

**Ch15 (Part III specification voice):** confirmed on-voice.

- Opens with the dashcam scenario (one concrete grounding case before snapping to spec voice — house pattern).
- "What chain-of-custody is not" subsection establishes negative space crisply.
- Sub-patterns 9a/9b/9c each open with a one-sentence statement of what the sub-pattern is, then enumerate fields/mechanics, then close with a behavior or consequence.
- FAILED conditions and kill trigger are specification-grade — bullet enumeration with named failure modes.
- Implementation surfaces names four event contracts and explicitly marks them illustrative ("the concrete schema lands when `Sunfish.Kernel.Custody` reaches its first milestone").
- Closes with the cross-reference to App B §Section 5 — round-trip preserved.

**App B §Section 5 (worksheet/checklist register):** confirmed on-voice.

- Opening directs the reader to use the worksheet under specific deployment conditions, with cross-reference to Ch15.
- Seven fields: tables for structured data, prose-instruction blocks for procedural fields, checklists for binary requirements.
- Each field has a one-sentence guidance closer (e.g., "Record fingerprints from the published key hierarchy, not informal channels.")
- Escalation paths in numbered list with imperative directives.
- Closes with the round-trip statement back to `Sunfish.Kernel.Custody`.

**Cross-section round-trip:** the worksheet is deployment-time; per-transfer enforcement happens in `Sunfish.Kernel.Custody` (Ch15 spec). Both files reinforce the same canonical names: `CustodyTransferInitiated`, `CustodyTransferConfirmed`, `CustodyTransferDisputed`, `RegulatoryExportBatch`, `tsa-pending`, `transfer-initiated`, `transfer-completed`. No synonym cycling between files.

---

## 6. Preservation flags honored

| Flag | Source | Honored? |
|---|---|---|
| Ch15:645 honesty-bound (TSA-absence declaration) | Tech-review §9 | YES — sentence preserved verbatim. |
| Ch15:621 eIDAS Article 41 / Article 42 framing | Tech-review §3 | YES — content preserved verbatim; only paragraph break introduced. |
| Ch15:621 `<!-- design-decisions: §5 #9 + §8.2 -->` annotation | Tech-review §1 | YES — preserved verbatim; moved with second paragraph in split. |
| Sub-pattern labels §9a / §9b / §9c | Dispatch | YES — not renumbered or relabeled. |
| Ch15:585 HTML annotation header | Dispatch | YES — out-of-scope, untouched. |
| Refs [1]–[27] in Ch15 reference list | Dispatch | YES — untouched. |
| §Forward Secrecy and §Endpoint Compromise | Dispatch | YES — untouched. |
| App B §Section 5 worksheet register | Dispatch | YES — only one micro-edit (App B line 280 active-voice fix); register intact. |

---

## 7. Edit summary

| File | Edits | Categories |
|---|---|---|
| `chapters/part-3-reference-architecture/ch15-security-architecture.md` | 2 | Paragraph split (line 621); active voice + strong verbs (line 633). |
| `chapters/appendices/appendix-b-threat-model-worksheets.md` | 1 | Active voice (line 280). |

Total: 3 edits across 2 files. No technical content changed. No citations changed. No cross-references changed. No new vocabulary introduced.

---

## 8. Gate decision

**Prose-review → voice-check PASSES.**

Section advances to voice-check (Stage 6 — human only) with:

- 0 paragraph-length violations remaining (1 found, 1 fixed).
- 0 active-voice violations remaining (2 found, 2 fixed).
- 0 hedging violations.
- 0 academic-scaffolding hits.
- 0 anti-AI tell pattern hits.
- 0 internal extension-number leaks.
- 0 synonym cycling between Ch15 and App B.
- All preservation flags honored verbatim.
- Voice register confirmed on-voice for both Part III (specification) and Appendix B (worksheet/checklist).

Voice-check is the human-only stage where the author adds personal context, field anecdotes, and connective tissue. The section is structurally and stylistically clean for that pass.
