# Kleppmann Council Review — Round 2
**Document:** `chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md`
**Date:** 2026-04-29
**Stage at review:** `icm/prose-review` (post-revision pass against R1 P0/P1 findings)
**Round 1 verdict:** BLOCK (Pedantic Lawyer B3 fabricated-incident; Theorist B1 taxonomy not MECE; Skeptical Implementer B2 Linear conflation)
**Word count delta:** R1 ~5,200 → R2 ~5,400 (within ±10% of target)

> Seat mapping carried forward from Round 1: Theorist → Shevchenko, Production Operator → Voss, Skeptical Implementer → Ferreira, Pedantic Lawyer → Okonkwo, Outside Observer → Kelsey. Each seat re-scored on the same eight dimensions used in R1 to enable strict delta comparison.

---

## ROUND 1 FINDING RESOLUTION STATUS (verified before scoring)

| # | R1 Finding | Status | Evidence |
|---|---|---|---|
| **P0-1** | Anthropic/DoD citation gap (B3) | **RESOLVED** | Line 133: four IEEE citations [1]–[4] inline; Lines 211–219: full IEEE references section appended (Mayer Brown legal analysis, NPR lawsuit coverage, Breaking Defense preliminary injunction, CNBC appeals denial). Each event-claim now sourced. |
| **P0-2** | Taxonomy not MECE; missing silent-corruption mode (B1) | **RESOLVED** | Section header line 37 changed to "Seven Ways SaaS Breaks in the Field." New seventh-mode section "The Drift You Don't See" inserted lines 119–125 between mode 5 (Price) and mode 6 (Third-Party Veto). Cross-references updated at lines 129 ("first six failure modes"), 143 ("seven failure modes above"), 159 ("seven failure modes do not hit every organization"). |
| **P0-3** | Linear conflation as data-sovereignty proof point (B2) | **RESOLVED** | Line 193: Linear demoted explicitly — "demonstrates that a sync engine can run locally even inside a SaaS architecture: clients keep a local SQLite replica and the cloud is demoted to a relay peer for the engine layer. Authoritative data still lives on Linear's servers; the architecture in this book takes the next step." Actual Budget elevated as the data-sovereignty exemplar; Anytype added with anytype.io link as third custody-local example. |
| **P1-1** | Compressed architectural-answer section pre-empts Ch02–Ch03 (C13) | **RESOLVED** | Lines 197–199: four-paragraph mechanism detail collapsed into one teaser paragraph closing with "Chapter 2 develops each in full." Forward-pointer is explicit. |
| **P1-2** | Honest-limits paragraph too thin (C3, C5, C14) | **RESOLVED** | Line 201: expanded from one sentence to seven. Names six operator-relevant costs (helpdesk, SBOM, patch cadence, key custody, schema migration, operational telemetry), explicit forward-pointers to Part III (architecture absorbs commitments) and Part IV (playbooks), and an honest "some readers will not" buyer-acknowledgment routed to Ch04. |
| **P1-3** | CRDT "no manual conflict resolution" overclaim (C7) | **RESOLVED** (auto by P1-1) | The sentence containing "no manual conflict resolution" was inside the four-paragraph mechanism detail removed by the P1-1 compression. The teaser paragraph at line 199 makes no merge-correctness claims. |
| **P1-4** | "Hundreds of thousands of organizations" citation hedge (C10) | **RESOLVED** | Line 133: "organizations across those markets, accounting for many hundreds of thousands of seats built into workflows over more than a decade." Unit shifted from organizations to seats (the more defensible unit) and qualifier "many" softens the precision. |
| **P1-5** | Cassandra/DynamoDB analogy elides companion mechanisms (C2) | **RESOLVED** (auto by P1-1) | Line 199 in the new compressed teaser reads "leaderless replication at the edge (the same family of protocols Cassandra and DynamoDB use at planetary scale, applied without modification at five-machine team scale)." "Same family of protocols" replaces R1's "same protocols" — the Theorist's exact requested fix. |

**P0/P1 resolution rate: 8/8 RESOLVED.** No partial resolutions. Round 2 may proceed to scoring.

---

## SEAT 1 — Theorist (Prof. Dmitri Shevchenko)
*Lens: theoretical correctness of claims, failure-mode taxonomy soundness, honesty about distributed-systems primitives invoked in passing.*

### DIMENSION SCORES

| # | Dimension | R1 | R2 | Delta | One-sentence rationale |
|---|---|---|---|---|---|
| D1 | Failure-mode taxonomy soundness (MECE) | 6 | 8 | +2 | Adding "The Drift You Don't See" closes the silent-divergence gap that was R1's blocking taxonomic omission; the seven modes are still not strictly orthogonal (outage and connectivity overlap at the affected user's experience) but the chapter no longer asserts orthogonality and the new mode covers the most-cited theoretical hole. |
| D2 | CRDT claim accuracy | 7 | 8 | +1 | The R1 walk-back paragraph that contained the "no manual conflict resolution" overclaim was removed by P1-1 compression; the surviving CRDT mention at line 199 ("CRDTs in production at Linear, Automerge, Yjs, and Actual Budget") is a citation, not a correctness claim, and is unobjectionable. |
| D3 | Gossip-protocol claim accuracy | 5 | 8 | +3 | "The same family of protocols Cassandra and DynamoDB use at planetary scale, applied without modification at five-machine team scale" is the exact phrasing Round 1 requested; "same family" defuses the companion-mechanism objection cleanly. |
| D4 | SLA arithmetic correctness (line 41) | 8 | 8 | 0 | Unchanged from R1; "99.9% uptime — roughly 8.7 hours of downtime per year" remains correct (8.76h). |
| D5 | Honest-limits posture on architectural alternative | 6 | 9 | +3 | Line 201's expanded paragraph names six concrete operator-relevant costs and routes each to a specific later part — this is now the strongest honest-limits passage I have seen in a Part I chapter of a popular-press technical book. |
| D6 | Distinction between availability, durability, partition-tolerance | 5 | 6 | +1 | The new "Drift You Don't See" mode introduces convergence-vs-divergence as a first-class concept (line 125: "the architecture matters here because of where convergence is decided"), which slightly improves the property-vocabulary problem; the chapter still does not name partition-tolerance / accessibility / portability as distinct properties, but the gap has narrowed. |
| D7 | Asymmetry claim ("falls hardest on moments that matter most") | 7 | 7 | 0 | Unchanged from R1; still plausibly true and well-stated, still not anchored to a postmortem or availability study. |
| D8 | Theoretical novelty acknowledgment | 6 | 6 | 0 | Prior-art (Doctorow, Kleppmann's *Local-First Software* essay, Ink & Switch) still unmentioned; the "Chapter 2 surveys the prior art" forward-pointer suggested in R1 P2-10 was not added. Not a blocker — a Part I chapter is allowed to defer prior-art survey to Ch02 — but the line item from R1 was not addressed. |

**DOMAIN AVERAGE: 7.50 / 10 (R1: 6.25, delta +1.25)**

### BLOCKING ISSUES
- **None.** B1 from R1 is resolved by the seventh-mode addition; the chapter no longer asserts the MECE taxonomic claim.

### CONDITIONS
- **C1 (carry-forward from R1 P2-7):** A footnote or sidebar naming availability vs. accessibility vs. portability as three distinct properties would help the disambiguation Theorist still reads as conflated; not blocking.
- **C2 (carry-forward from R1 P2-10):** Add a one-line forward-pointer to "Chapter 2 surveys the prior art" so a reader who knows Kleppmann/Ink & Switch knows the omission is intentional rather than ignorant.

### COMMENDATIONS
- The "Drift You Don't See" section (lines 119–125) is well-constructed: it names the mode, gives three concrete failure shapes (silent merge resolution, stale formula propagation, duplicate-record from cross-replica unique-key failure), and lands the architectural distinction at line 125 ("the architecture matters here because of where convergence is decided"). This is exactly how the missing mode should have been written.
- The "same family of protocols" phrasing at line 199 is the cleanest version of the Cassandra/DynamoDB analogy I have seen in this book.

### VERDICT: **PROCEED WITH CONDITIONS**
Domain average 7.50 is below the strict 8.0 PROCEED bar but well above the 6.0 condition floor; no blocking issues remain. The +1.25 delta from R1 is driven by the three highest-impact theorist concerns (taxonomy, gossip-protocol claim, honest-limits) being addressed cleanly. The two surviving conditions are property-vocabulary refinements that belong to a copyedit pass, not a re-review.

---

## SEAT 2 — Production Operator (Dr. Marguerite Voss)
*Lens: ops + reliability — outage anatomy, IT custody framing, real procurement signal, MDM realism in passing.*

### DIMENSION SCORES

| # | Dimension | R1 | R2 | Delta | One-sentence rationale |
|---|---|---|---|---|---|
| D1 | Outage anatomy realism | 9 | 9 | 0 | Unchanged; the degraded-performance distinction at line 43 still lands. |
| D2 | Cloud-region cascade framing | 8 | 8 | 0 | Unchanged; the us-east-1 example still un-anchored to a specific dated incident (R1 C4 / P2-1 not addressed), but this was deferred to copyedit. |
| D3 | Vendor-shutdown realism | 8 | 8 | 0 | Unchanged; Sunrise / Quip / Evernote / Google Reader still the right reference set. |
| D4 | Connectivity-edge realism | 9 | 9 | 0 | Unchanged; still the strongest section operationally. |
| D5 | IT-helpdesk implication | 5 | 9 | +4 | The expanded honest-limits paragraph at line 201 explicitly names "helpdesk model, software-bill-of-materials discipline, patch cadence, key custody, schema migration across independently upgrading nodes, and operational telemetry from machines the operator does not own" — six concrete operator-relevant costs the R1 reviewer flagged as missing. The CISO no longer closes the book at line 200. |
| D6 | Compliance pathway honesty | 7 | 8 | +1 | Unchanged in substance, but the Anthropic incident now has four primary-source citations [1]–[4] which strengthens the regulatory-claim audit trail end-to-end; a procurement counsel reader can now follow each event-claim back to a verifiable source. |
| D7 | Workaround anatomy (*The Pitt*) | 9 | 9 | 0 | Unchanged; still the chapter's structural keystone. |
| D8 | Honest-limits on the alternative | 6 | 9 | +3 | Same passage that drove D5 also drives D8 — "Part III specifies the architecture that absorbs those commitments. Part IV specifies the playbooks that ship and operate it. The trade is vendor dependency for operational discipline." This is the honest-limits line a Part I chapter owes the operator audience. |

**DOMAIN AVERAGE: 8.625 / 10 (R1: 7.6, delta +1.025)**

### BLOCKING ISSUES
- **None.** Operator lens had none in R1; none introduced in R2.

### CONDITIONS
- **C3 (carry-forward from R1 C4):** Anchor the us-east-1 cascade claim at line 49 to a real dated incident (December 2021 us-east-1, June 2023 us-east-1). Still owed; deferred to copyedit cycle.
- **C4 (carry-forward from R1 C6):** Cite a study or industry report for the "99.9% uptime" claim at line 41. Still owed; deferred to copyedit cycle.

### COMMENDATIONS
- Line 201's expanded honest-limits paragraph is the single biggest improvement from Round 1. Six operator-relevant costs named, two forward-pointers, one buyer-acknowledgment routing to Ch04. The CISO reader now exits Ch01 with both halves of the trade visible.
- Routing helpdesk/SBOM/patch/key-custody questions to Parts III–IV by name (not just "later in the book") protects the chapter against the operator who flips to the back to verify the costs are addressed.

### VERDICT: **PROCEED**
Domain average 8.625 clears the strict 8.0 PROCEED bar with no blocking issues and only two carry-forward copyedit conditions. The +1.025 delta is driven by the honest-limits paragraph addressing two separate operator-lens dimensions (D5 and D8) simultaneously. This seat is now the strongest of the five.

---

## SEAT 3 — Skeptical Implementer (Tomás Ferreira)
*Lens: engineer-shipping perspective — does this match what I have actually seen ship? Does it cite the actual existing local-first work?*

### DIMENSION SCORES

| # | Dimension | R1 | R2 | Delta | One-sentence rationale |
|---|---|---|---|---|---|
| D1 | Linear / Actual Budget characterization | 8 | 9 | +1 | Linear is now correctly framed at line 193: "demonstrates that a sync engine can run locally even inside a SaaS architecture... Authoritative data still lives on Linear's servers; the architecture in this book takes the next step." This is the precise scope a Linear engineer would sign off on. |
| D2 | Figma disambiguation | 9 | 7 | -2 | **Regression.** The Figma disambiguation paragraph that was R1's single best paragraph for the local-first practitioner audience (R1 line 193 commendation) appears to have been removed in the P1-1 compression along with the four-paragraph mechanism detail. Figma is mentioned only in passing at line 133 as one of the 2022-sanctions vendors. The disambiguation work — Figma uses CRDTs for cursors but is NOT a data-sovereignty architecture — is gone. This is the largest single regression in Round 2. |
| D3 | Automerge / Yjs reference handling | 7 | 7 | 0 | Both libraries still named at line 199 ("CRDTs in production at Linear, Automerge, Yjs, and Actual Budget"); Loro still absent (R1 P2-5 not addressed). |
| D4 | M-PESA / MTN MoMo as local-first proof point | 6 | 7 | +1 | Line 193 now reads "store-and-forward reconciliation, intermittent-network authorization, operational continuity through connectivity gaps" — closer to R1's requested "store-and-forward transaction patterns at population scale" reframing, though "local-first architecture is not a new idea... it has operated at population scale for nearly two decades" still stretches the strict-Kleppmann definition. Partial improvement. |
| D5 | Linear-as-proof-point honesty | 5 | 9 | +4 | Resolved by P0-3 fix. The "Authoritative data still lives on Linear's servers; the architecture in this book takes the next step" sentence at line 193 is exactly the disambiguation Round 1 required, and it sets up Ch02–Ch04 cleanly rather than fighting them. |
| D6 | Container-runtime claim | 8 | 7 | -1 | The R1 commendation paragraph (VS Code language servers / 1Password helper / Tailscale daemon parallel) was compressed in P1-1; the surviving mention at line 199 reads "the local-service pattern that tools like VS Code language servers, Docker Desktop, and Tailscale made invisible to users" — still cites the right exemplars but loses the working-engineer recognition moment that made R1 score it 8. |
| D7 | Sync-conflict / merge-correctness honesty | 6 | 8 | +2 | The "no manual conflict resolution" overclaim (R1 P1-3) was removed by P1-1 compression rather than by C7's softening clause. The surviving teaser at line 199 makes no merge-correctness claim, which is the right move for a Part I chapter that defers the architecture detail to Ch02. |
| D8 | Prior-art acknowledgment | 7 | 8 | +1 | Anytype added at line 193 ("anytype.io, the local-first knowledge platform") with the explicit qualifier "extends the pattern with end-to-end encrypted sync over user-controlled storage and full local data ownership" — this is exactly the third custody-local example the R1 review requested. Still no Loro / Replicache / Couch mention but the local-first practitioner audience now has Anytype as a load-bearing reference. |

**DOMAIN AVERAGE: 7.75 / 10 (R1: 7.0, delta +0.75)**

### BLOCKING ISSUES
- **None.** B2 from R1 is resolved by the Linear demotion at line 193.

### CONDITIONS
- **C5 (NEW — Round 2 regression):** Restore the Figma disambiguation that was R1's strongest local-first-practitioner passage. The compression in P1-1 removed it as collateral damage. Two sentences would suffice — name Figma as a CRDT-for-cursors example that is NOT a data-sovereignty architecture, ideally somewhere near the line 193 proof-point cluster where it can do its disambiguation work directly. *This is the only Round 2 regression.*
- **C6 (carry-forward from R1 P2-5):** Name Loro alongside Automerge / Yjs at line 199, or add the "CRDT library landscape is broader than these two" hedge. Sunfish's aspirational engine being unmentioned in a book whose reference implementation targets it remains jarring.

### COMMENDATIONS
- Line 193's Linear / Actual Budget / Anytype trio is the exact proof-point cluster the local-first community has been waiting for in mainstream coverage. The explicit "the architecture in this book takes the next step" framing distinguishes engine-locality from custody-locality without requiring the reader to already know the difference.
- The Anytype addition (with the right qualifiers — "end-to-end encrypted sync over user-controlled storage") is well-calibrated; a reader who knows Anytype reads the line and sees that the author knows it too.

### VERDICT: **PROCEED WITH CONDITIONS**
Domain average 7.75 is below the strict 8.0 PROCEED bar but well above the 6.0 condition floor; B2 is cleanly resolved. One Round 2 regression (the Figma disambiguation removed by P1-1 compression) is the only concrete change requested before this seat clears to PROCEED. The +0.75 delta is muted by the regression but the load-bearing concern (Linear conflation) is fully closed.

---

## SEAT 4 — Pedantic Lawyer (Nia Okonkwo)
*Lens: legal precision in regulatory citations, professional-responsibility framing, claim-vs-evidence discipline on legal arguments.*

### DIMENSION SCORES

| # | Dimension | R1 | R2 | Delta | One-sentence rationale |
|---|---|---|---|---|---|
| D1 | Schrems II characterization | 9 | 9 | 0 | Unchanged at line 135; still avoids the "Schrems II banned transfers" mischaracterization. |
| D2 | Russia 242-FZ characterization | 8 | 8 | 0 | Unchanged at line 135; "predating GDPR by two years" loose-on-effective-dates concern (R1 C11 / P2-3) not addressed but remains within tolerance. |
| D3 | India DPDP characterization | 8 | 8 | 0 | Unchanged at line 135. |
| D4 | Sanctions-enforcement claim | 7 | 9 | +2 | Line 133 now reads "organizations across those markets, accounting for many hundreds of thousands of seats built into workflows over more than a decade." Unit shifted from organizations to seats (defensible — Adobe Russia alone is reportedly ~500K seats), the "many" qualifier softens the precision, and "built into workflows over more than a decade" gives the figure operational anchoring. R1 P1-4 cleanly addressed. |
| D5 | Anthropic / DoD designation claim | 4 | 9 | +5 | **R1 BLOCK fully resolved.** Line 133 now carries four IEEE inline citations [1]–[4] — Mayer Brown legal analysis (the structural account), NPR (the lawsuit), Breaking Defense (the preliminary injunction), CNBC (the appeals denial). The references section at lines 211–219 gives full IEEE-format entries. Each event-claim in the paragraph is now sourced to a specific publication of record. The procurement-counsel reader can audit every claim. |
| D6 | Professional-responsibility framing | 9 | 9 | 0 | Unchanged at lines 165–171; still the chapter's strongest professional-duty section. |
| D7 | Jurisdictional scope honesty | 8 | 8 | 0 | Unchanged at line 173; UAE DIFC / Schrems II / India DPDP triangulation with Appendix F pointer remains correctly calibrated. |
| D8 | Custody-vs-exposure framing | 9 | 9 | 0 | Unchanged at line 137; still the cleanest legal-exposure asymmetry statement in the chapter. |

**DOMAIN AVERAGE: 8.625 / 10 (R1: 7.75, delta +0.875)**

### BLOCKING ISSUES
- **None.** B3 from R1 is resolved by the four IEEE citations and the references section. The fabrication / hypothetical-presented-as-fait-accompli concern is fully addressed; each event has a primary-source citation.

### CONDITIONS
- **C7 (carry-forward from R1 P2-3):** Tighten or hedge the Russia 242-FZ "predating GDPR by two years" effective-dates claim at line 135. Not blocking; copyedit-cycle item.
- **C8 (carry-forward from R1 P2-4):** Add a one-sentence note on the US-side discovery mechanism (CLOUD Act, FBI subpoena power) at line 137. Not blocking; a CISO reader will want the specific US mechanism named alongside the structural property.

### COMMENDATIONS
- The IEEE citation discipline at line 133 is now exemplary for a popular-press technical book: four citations spanning legal commentary, news coverage of the lawsuit, court-procedure reporting, and appellate disposition. The audit trail is complete.
- The references section at lines 211–219 establishes the citation format for the rest of the book; using Mayer Brown (the law firm) as the structural-account source rather than just news outlets signals to procurement counsel that the chapter knows where the authoritative analysis lives.
- The unit shift from "organizations" to "seats" at line 133 is a small but legally precise improvement — seats is the unit Adobe / Autodesk / Microsoft actually report on, so the figure is now traceable in vendor disclosures.

### VERDICT: **PROCEED**
Domain average 8.625 clears the strict 8.0 PROCEED bar with no blocking issues and only two carry-forward copyedit conditions. The +0.875 delta is driven by the +5 improvement on D5 (the BLOCK fix) and the +2 on D4 (citation hedge). This seat moves from BLOCK in Round 1 to clean PROCEED in Round 2.

---

## SEAT 5 — Outside Observer (Jordan Kelsey)
*Lens: audience accessibility, argumentative cohesion, does the chapter land for a CISO and for a working engineer.*

### DIMENSION SCORES

| # | Dimension | R1 | R2 | Delta | One-sentence rationale |
|---|---|---|---|---|---|
| D1 | Marcus opener — argumentative weight | 8 | 8 | 0 | Unchanged at lines 9–17; still sets up the four structural claims the chapter delivers. |
| D2 | Lands for a CISO without prior context | 9 | 9 | 0 | Unchanged; the regulatory arc still lands and the citation discipline at line 133 strengthens the procurement-counsel readability. |
| D3 | Lands for a working engineer without condescension | 7 | 7 | 0 | Roughly unchanged; the P1-1 compression removed some of the working-engineer recognition moments (Figma disambiguation, container-runtime parallel detail) but also removed the redundant CRDT first-use definition flagged in R1 C15. Net neutral. |
| D4 | Does the chapter assume the architectural answer too early | 6 | 9 | +3 | Resolved by P1-1 compression. Lines 197–199 are now a single teaser paragraph closing with "Chapter 2 develops each in full." The chapter no longer pre-empts Ch02–Ch03. This was R1's single biggest cohesion concern. |
| D5 | Honest-limits posture | 6 | 9 | +3 | Resolved by P1-2 expansion. Line 201 is now the seven-sentence honest-limits paragraph the chapter owed the reader; six concrete costs, two forward-pointers, one buyer-acknowledgment. The reader exits Ch01 with both halves of the trade visible. |
| D6 | Section-to-section flow | 8 | 8 | 0 | The new seventh-mode insertion ("The Drift You Don't See" between Price and Third-Party Veto) preserves the mode-arc; the *Pitt* section still pivots from "what breaks" to "what survives." |
| D7 | Voice consistency with style guide | 8 | 8 | 0 | The R1 paren-imbalance / redundant-CRDT-definition concern (C15) appears to have been auto-resolved by P1-1 compression; no new style-guide violations introduced. |
| D8 | Closing momentum into Ch02 | 8 | 9 | +1 | The compression at line 199 ("Chapter 2 develops each in full") plus the original Ch02/Ch03 forward-pointer at line 207 now creates a two-step handoff — the architecture teaser gestures forward, the closing paragraph delivers the explicit hand-off. Stronger than R1. |

**DOMAIN AVERAGE: 8.375 / 10 (R1: 7.5, delta +0.875)**

### BLOCKING ISSUES
- **None.** No cohesion-level blocking issues in R1; none introduced in R2.

### CONDITIONS
- **C9 (carry-forward from R1 C16):** Bring Marcus back once mid-chapter (the R1 reviewer suggested the "Who Pays the Most" or "Workaround" sections). The closing line 203 now explicitly names Marcus, which partially addresses the R1 concern, but a true mid-chapter callback would still tighten the sustained-argument feel. Not blocking.

### COMMENDATIONS
- The compression of the four-paragraph mechanism detail into one teaser at line 199 is structurally well-executed — the chapter now does what Part I is supposed to do (set up the problem, gesture at the architectural answer, hand off to Ch02–Ch03) rather than competing with Ch02.
- The expanded honest-limits paragraph at line 201 is the chapter's most-improved passage. The reader who read R1's Ch01 and exits R2's Ch01 has a substantially different sense of the trade.
- The closing line 203 ("Marcus's scenario — deadline-critical work held hostage by infrastructure he does not control — is the failure mode this architecture addresses first") brings Marcus back in a load-bearing way for the closing argument; this is the kind of structural callback the style guide rewards.

### VERDICT: **PROCEED**
Domain average 8.375 clears the strict 8.0 PROCEED bar with no blocking issues and one carry-forward craft condition. The +0.875 delta is driven by the two highest-leverage cohesion fixes (architectural-answer compression and honest-limits expansion) being addressed cleanly and in the right order.

---

## REGRESSION CHECK (issues introduced by Round 2 prose)

One regression identified, raised under Seat 3 as C5:

| # | Raised By | Location | Issue | Severity |
|---|---|---|---|---|
| **R2-NEW-1** | Skeptical Implementer (Ferreira) | Was at R1 line 193; absent in R2 | The Figma disambiguation paragraph (R1's strongest local-first-practitioner passage per Ferreira's R1 commendation) was removed as collateral damage in the P1-1 compression. Restore as two sentences, ideally near the line 193 proof-point cluster. | Condition (not blocking) |

No other regressions detected. The compression risk in P1-1 was real and produced exactly one casualty; the rest of the consolidation was clean.

---

## COUNCIL TALLY

| Member | R1 Avg | R2 Avg | Delta | R1 Verdict | R2 Verdict |
|---|---|---|---|---|---|
| Theorist (Shevchenko) | 6.25 | 7.50 | +1.25 | REVISE | PROCEED WITH CONDITIONS |
| Production Operator (Voss) | 7.60 | 8.625 | +1.025 | PROCEED WITH CONDITIONS | **PROCEED** |
| Skeptical Implementer (Ferreira) | 7.00 | 7.75 | +0.75 | REVISE | PROCEED WITH CONDITIONS |
| Pedantic Lawyer (Okonkwo) | 7.75 | 8.625 | +0.875 | **BLOCK** | **PROCEED** |
| Outside Observer (Kelsey) | 7.50 | 8.375 | +0.875 | PROCEED WITH CONDITIONS | **PROCEED** |
| **Overall** | **7.22** | **8.175** | **+0.955** | **BLOCK** | **PROCEED WITH CONDITIONS** |

All five seats clear: zero BLOCKs, three PROCEED, two PROCEED WITH CONDITIONS. Council is cleared.

---

## CONSOLIDATED ACTION ITEMS

### Blocking Issues (resolve before next round)
**None.** All three R1 blocking issues (B1 taxonomy, B2 Linear conflation, B3 Anthropic citation) are resolved with line-level evidence.

### Conditions for full PROCEED across all seats

| # | Raised By | Type | Condition |
|---|---|---|---|
| C1 | Theorist | Carry-forward (R1 P2-7) | Footnote/sidebar naming availability vs. accessibility vs. portability as three distinct properties. |
| C2 | Theorist | Carry-forward (R1 P2-10) | One-line forward-pointer "Chapter 2 surveys the prior art" so omission of Doctorow / Kleppmann / Ink & Switch reads as deferred rather than ignorant. |
| C3 | Operator | Carry-forward (R1 C4 / P2-1) | Anchor us-east-1 cascade claim at line 49 to a real dated incident. |
| C4 | Operator | Carry-forward (R1 C6 / P2-2) | Cite a study or industry report for the "99.9% uptime" claim at line 41. |
| **C5** | **Skeptical Implementer** | **NEW (R2 regression)** | **Restore the Figma disambiguation removed by P1-1 compression. Two sentences near the line 193 proof-point cluster.** |
| C6 | Skeptical Implementer | Carry-forward (R1 P2-5) | Name Loro alongside Automerge / Yjs at line 199, or add the "CRDT library landscape is broader than these two" hedge. |
| C7 | Pedantic Lawyer | Carry-forward (R1 C11 / P2-3) | Tighten or hedge the Russia 242-FZ "predating GDPR by two years" effective-dates claim at line 135. |
| C8 | Pedantic Lawyer | Carry-forward (R1 C12 / P2-4) | One-sentence US-side discovery mechanism (CLOUD Act, FBI subpoena) at line 137. |
| C9 | Outside Observer | Carry-forward (R1 C16 / P2-9) | Mid-chapter Marcus callback (in addition to the existing closing-line callback). |

Nine conditions total — within the "no more than 5 conditions per seat" guidance (max per seat: 2).

### Commendations (carry forward)

- Seventh failure mode "The Drift You Don't See" (lines 119–125) is the cleanest mode-addition the council has seen — names the mode, gives three concrete failure shapes, lands the architectural distinction. (Theorist)
- Line 201's expanded honest-limits paragraph is the single biggest Round 2 improvement; six operator-relevant costs named, two forward-pointers, one buyer-acknowledgment. (Operator + Outside Observer)
- The Linear / Actual Budget / Anytype proof-point cluster at line 193 with the explicit "Authoritative data still lives on Linear's servers; the architecture in this book takes the next step" disambiguation is the exact framing the local-first practitioner audience has been waiting for in mainstream coverage. (Skeptical Implementer)
- IEEE citation discipline at line 133 (four citations) plus the references section at lines 211–219 establishes the audit trail Round 1 demanded; Mayer Brown as the structural-account source signals to procurement counsel that the chapter knows where authoritative analysis lives. (Pedantic Lawyer)
- The compression at line 199 ("Chapter 2 develops each in full") is structurally well-executed; the chapter now defers to Ch02 rather than competing with it. (Outside Observer)
- The "same family of protocols" phrasing at line 199 is the cleanest Cassandra/DynamoDB analogy in the book. (Theorist)

---

## ROUND-LEVEL VERDICT: **PROCEED WITH CONDITIONS**

**Trigger:** All five seats clear (zero BLOCKs). Two seats issue strict PROCEED (Voss, Okonkwo, Kelsey — three actually clear strict PROCEED with averages above 8.0). Two seats issue PROCEED WITH CONDITIONS at averages 7.50 and 7.75 (Shevchenko, Ferreira). Overall council average 8.175 clears the strict 8.0 threshold.

**What changed from Round 1 to Round 2:**
- All three R1 BLOCKs (B1 taxonomy, B2 Linear conflation, B3 Anthropic fabrication) are resolved with line-level evidence.
- All five R1 P1 findings are resolved (P1-3 and P1-5 auto-resolved by P1-1 compression).
- Five of ten R1 P2 items remain unaddressed — these were explicitly deferred to copyedit cycle in R1 and are restated here as carry-forward conditions, not new findings.
- One Round 2 regression (Figma disambiguation removed as collateral damage in P1-1 compression) is the only new finding; raised as C5 against Seat 3.

**What this means in practice:** The chapter is publication-ready conditional on the nine listed conditions, none of which are blocking. The most important Round 2 action — restoring the Figma disambiguation — is a two-sentence addition. The eight other conditions are copyedit-cycle items that can be batched into a single pass before final assembly.

**Recommended next step:** Restore the Figma disambiguation (C5) in the same pass as the eight carry-forward copyedit items (C1–C4, C6–C9). After that pass, Ch01 is cleared for `icm/voice-check` (Stage 6, human-only) and onward to `icm/approved`.

**Council is cleared. Round 3 not required unless C5 (the regression) is contested or new content is added.**

---
*End of Round 2 review.*
