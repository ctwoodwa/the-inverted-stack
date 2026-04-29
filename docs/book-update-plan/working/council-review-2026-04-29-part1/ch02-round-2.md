# KLEPPMANN COUNCIL REVIEW — Part I, Round 2
**Document:** `chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md`
**Date:** 2026-04-28
**Council seats convened:** Theorist · Production Operator · Skeptical Implementer · Pedantic Lawyer · Outside Observer
**Reviewer:** Kleppmann Council facilitator
**Round 1 verdict:** REVISE (overall 5.8 / 10; 4-of-5 seats REVISE; Outside Observer PROCEED-WITH-CONDITIONS)
**Round 2 posture:** Stricter scrutiny. Any new defect introduced by the revision is a Round 2 defect, not a Round 1 carryover.

---

## Round 1 Resolution Audit (gating check)

Before scoring, the council confirms each Round 1 P0 and P1 finding has a defensible resolution.

### P0 resolutions

| # | Finding | Status | Evidence |
|---|---|---|---|
| **P0-1** | Citation discipline gap (~10 uncited prose claims) | **RESOLVED** | Reference list grew from 3 to 9 entries (lines 216–232). New refs [4] Schrems II Case C-311/18, [5] DPDP 2023, [6] DIFC DPL 2020, [7] 242-FZ, [8] Linear sync blog, [9] Replicache docs. In-text markers placed at line 58 (Linear → [8]), line 64 (Replicache → [9]), line 185 (Schrems II → [4], DPDP → [5], DIFC DPL → [6], 242-FZ → [7]). |
| **P0-2** | Replicache omission | **RESOLVED** | New Replicache paragraph at line 64, ~165 words, parallels the Automerge treatment: names what it does well (sync framework, optimistic mutation, sub-second IndexedDB cache) and where it stops (server is source of truth, mutators run server-side, schema migration / key custody / MDM packaging out of scope). |
| **P0-3** | M-PESA/MTN MoMo mischaracterization | **RESOLVED** | Replaced at line 155 with Square Reader/Toast (offline-first POS) + Salesforce Mobile SDK (offline-first object framework). Both are user-device-replica patterns at commercial scale and survive the operator's "is this actually a device replica" test. |
| **P0-4** | DIFC DPL overclaim | **RESOLVED** | Line 185 now reads "constrains processing and cross-border transfers of personal data by DIFC-licensed entities and requires specific lawful bases for transfers to non-adequate jurisdictions." Categorical "may legally prohibit foreign cloud storage" framing is gone. |

### P1 resolutions

| # | Finding | Status | Evidence |
|---|---|---|---|
| **P1-1** | No like-for-like comparison vector | **RESOLVED** | 8-row × 4-column comparison table at lines 124–133 (deployment topology, data-ownership stance, threat model, business model). Covers Obsidian, Notion, Linear, Replicache, ElectricSQL, PowerSync, Actual Budget, Automerge. Closing analytical paragraph at line 135 reads the table for the reader. |
| **P1-2** | Thesis sentence buried | **RESOLVED** | "The composition is the contribution" now appears at line 14 (opening, bolded), line 135 (midpoint table close), and line 193 (close). Three landings, consistent phrasing. |
| **P1-3** | "What has not been done before" rhetorical, not falsifiable | **RESOLVED** | Line 159 narrows to three falsifiable axes: per-record CAP boundary + MDM-deployable installer + AGPLv3-with-managed-relay business model. The claim is now testable rather than rhetorical. |
| **P1-4** | Automerge operational caveat elided | **RESOLVED** | Line 159 inserts "though Automerge users have to budget for known operational costs (document size growth with edit history, cold-sync time on long-lived documents, and garbage-collection cadence) that the library leaves to the application." |
| **P1-5** | Sanctions citation absent | **PARTIALLY RESOLVED** | Covered by P0-1 reference list expansion *only insofar as the broader regulatory section now carries [4]–[7]*. The 2022 sanctions roll-call sentence at line 30 itself remains uncited. See Lawyer carryover below. |
| **P1-6** | Schrems II "direct compliance mechanism" overstates | **RESOLVED** | Line 185 now reads "structural mechanism that addresses the data-transfer leg of GDPR analysis under Schrems II." |
| **P1-7** | Linear "fail silently" sharper than UI behavior | **RESOLVED** | Line 58 now reads "Linear surfaces the sync state in the UI when the server is unreachable, so writes that depend on server-side validation … are visibly queued rather than silently dropped — but the queue still depends on the relay coming back." |
| **P1-8** | "What Each Gets Right" mini-section | **RESOLVED** | Line 118 "What Each Gets Right — and Where It Stops" is now a substantive H2 carrying the comparison table and a closing analytical paragraph. It earns its level. |

### Gating verdict

P0-1 through P0-4 are resolved; P1 is 7-of-8 resolved with one carryover (P1-5, the bare 2022 sanctions roll-call at line 30). Round 2 may proceed. The carryover lives below as a fresh blocking issue for the Lawyer seat only.

---

## SEAT 1 — The Theorist (academic / theoretical correctness)

**Posture:** Same as Round 1. Re-reads with attention to whether the new Replicache paragraph and the comparison table land *theoretically*, not just rhetorically.

### DIMENSION SCORES

| # | Dimension | R1 | R2 | Δ | Rationale |
|---|---|---|---|---|---|
| D1 | Accuracy of the seven-properties summary | 8 | 8 | — | Unchanged. Properties paraphrased correctly. Order remains reshuffled vs. paper; harmless for narrative. |
| D2 | Fidelity of CRDT theory references | 6 | 6 | — | Op-based vs. state-based distinction (R1 P2-1) is still not made; CRDT is still used generically. Cambria reference at line 193 is still by name only; no Litt et al. 2020 citation. The CRDT-as-class-vs-implementation conflation persists. P2-class, so does not block, but the dimension does not improve. |
| D3 | Correctness of system-specific technical claims | 6 | 8 | +2 | Linear paragraph now carries [8] and the operational behavior is more accurately framed. Replicache paragraph (line 64) is technically precise — calls out Rocicorp by name, identifies IndexedDB, server-side mutator validation, framework-vs-application scope. The Automerge operational caveat (line 159) is correct and disciplined. Actual Budget and Figma claims unchanged. |
| D4 | Treatment of the broader prior-art landscape | 4 | 8 | +4 | The largest single delta in this seat. The 8-row comparison table covers Replicache, ElectricSQL, PowerSync alongside Obsidian/Notion/Linear/Actual/Automerge. Replicache also gets its own paragraph. The omission that defined the Round 1 verdict is closed. Liveblocks and Yjs/Y-Sweet still get short shrift in the prose, but the table makes the absence less consequential. Jazz, Triplit, Evolu, Anytype-Cloud, Logseq, Tinybase, Verdant, RxDB still absent — but those are P2-class for an "opinionated, not encyclopedic" chapter. |
| D5 | Citation discipline (IEEE per Appendix E) | 4 | 8 | +4 | Reference count rose from 3 to 9. The four most consequential new claims (Schrems II, DPDP, DIFC DPL, 242-FZ) are bracketed. Linear carries [8]; Replicache carries [9]. Remaining gaps are smaller-bore: Cambria (Litt et al. 2020) at line 193 is still uncited; Stender et al. Flease 2010 is no longer name-dropped in this chapter (the Flease reference moved earlier in the manuscript revision); the Figma quotation at line 159 is still unattributed to Wallace 2019; the 2022 sanctions roll-call at line 30 is still bare. Substantial improvement, residual gaps. |
| D6 | Honest acknowledgement of prior intellectual debts | 7 | 7 | — | Closing paragraph at line 208 unchanged — names Ink & Switch, Kleppmann; does not name Litt, van Hardenberg, Wiggins, McGranaghan, Zelenka. P2 carryover. |
| D7 | Avoidance of overclaim | 7 | 9 | +2 | The "what has not been done before" claim is now narrowed to three falsifiable axes (line 159). This is exactly the discipline the Theorist asked for in Round 1. The "to the authors' knowledge at time of writing" hedge at line 36 remains. |
| D8 | Theoretical depth on CAP/lease/GC | 5 | 6 | +1 | The new line-159 narrowing surfaces "per-record CAP boundary that lets AP-class records and CP-class records coexist in one system" — which is the formal positioning that was missing in Round 1. The forward reference to Chapter 6 is still implicit, but the chapter at least *names* the construct. |

**DOMAIN AVERAGE: 7.5 / 10** (Round 1: 5.9; Δ +1.6)

### BLOCKING ISSUES (Theorist)

- None. The two Round 1 blockers (B1-T citation discipline, B2-T Replicache absence) are both resolved.

### CONDITIONS (carry forward, P1-class)

- **C1-T (carryover):** Cambria reference at line 193 still wants a Litt et al. 2020 citation. The chapter cites Cambria as the source of the "bidirectional schema lenses" contribution; the source paper deserves a number.
- **C2-T (carryover):** Figma "inspired by multiple separate CRDTs" string at line 159 is still in quotation marks without a Wallace 2019 attribution. Quote → cite.
- **C3-T (P2):** Op-based vs. state-based CRDT distinction is still elided. One sentence in the Seven Ideals section would close this.

### COMMENDATIONS

- ✓ The Replicache paragraph at line 64 is, structurally, the strongest piece of competitive positioning the chapter now contains. It uses the same scaffold as the Automerge paragraph (does well / stops at) and arrives at the right verdict ("solves the latency and reactivity problems extremely well within a smart-cache architecture; it does not produce a full node").
- ✓ The narrowing at line 159 — "three pieces no other published architecture combines" with three named axes — converts a rhetorical claim into a falsifiable one. This is precisely what the Theorist asked for.
- ✓ The Round 1 commendations (Anytype treatment at line 36; Local-First Conf 2024 citation as [3]) carry forward.

### VERDICT (Theorist): **PROCEED WITH CONDITIONS**
The two Round 1 blockers are cleanly resolved. Citation discipline has moved from a structural defect to a small set of named gaps. The taxonomy now treats Replicache fairly. The differentiator is falsifiable. Domain average clears 7.5; the seat will sign with the three named conditions tracked.

---

## SEAT 2 — The Production Operator (ops + reliability lens)

**Posture:** Same as Round 1. Re-reads the M-PESA replacement, the Linear softening, and the new Automerge operational caveat with the lens of an operator who has watched POS systems and Salesforce Mobile fail in the field.

### DIMENSION SCORES

| # | Dimension | R1 | R2 | Δ | Rationale |
|---|---|---|---|---|---|
| D1 | Operational accuracy of Linear description | 7 | 8 | +1 | Line 58 softening now matches Linear's actual UI behavior. "Visibly queued rather than silently dropped" is the right phrase. Citation [8] gives the operator a primary source to verify against. |
| D2 | Operational accuracy of Obsidian description | 7 | 7 | — | Unchanged. Conflict-copy framing remains correct; the multiple-sync-mechanism nuance (Sync vs. Git vs. iCloud vs. Syncthing vs. Remotely Save) is still elided, but P2-class. |
| D3 | Operational accuracy of Notion description | 6 | 6 | — | Unchanged. Self-host posture absence still not flagged. P2-class. |
| D4 | Operational accuracy of Actual Budget description | 8 | 8 | — | Unchanged. Still the sharpest single taxonomy entry. |
| D5 | Operational accuracy of Automerge / AutomergeRepo | 6 | 8 | +2 | The new caveat at line 159 ("document size growth with edit history, cold-sync time on long-lived documents, and garbage-collection cadence that the library leaves to the application") is exactly what the operator wanted. The "production-ready" framing no longer reads as marketing. |
| D6 | M-PESA / MTN MoMo operational analogy | 4 | 8 | +4 | The Round 1 disqualifying defect is gone. Square Reader, Toast, and Salesforce Mobile SDK are *actually* user-device-replica patterns. The framing at line 155 ("user-device-replica operation at commercial scale in domains where the cost of failed offline operation is concrete") is operationally honest. The replacement also makes a cleaner argumentative move: payments and field service generalize to structured-data applications more broadly. |
| D7 | Treatment of operational realities the chapter elides | 5 | 6 | +1 | MTBF numbers, Linear outage acknowledgment, ElectricSQL ceilings, Liveblocks MAU pricing — all still absent. The comparison table at lines 124–133 partially mitigates by exposing business-model differences. The Replicache paragraph at line 64 names "developer's server controls" the reconciliation, which is operationally honest. |
| D8 | Honest acknowledgement of operational pain on the proposed side | 5 | 6 | +1 | Line 206 ("managed relay is a residual vendor dependency the architecture does not eliminate — it disaggregates it") carries forward the Round 1 honest paragraph. The operational *cost* of running a full node (device provisioning, key custody UX, support burden) is still not flagged in Ch 2 — but the chapter at least narrows its claim to "data custody remains on user hardware" rather than a generic free-lunch promise. Carryover P2. |

**DOMAIN AVERAGE: 7.1 / 10** (Round 1: 6.0; Δ +1.1)

### BLOCKING ISSUES (Production Operator)

- None. The Round 1 blocker (B1-O M-PESA mischaracterization) is cleanly resolved.

### CONDITIONS (carry forward, P2-class)

- **C1-O (P2 carryover):** One sentence in Ch 2 acknowledging the *operational* cost of a full node (device provisioning, key custody UX, support burden) so the chapter does not sell a free lunch. The "manage relay residual" paragraph at line 206 covers vendor dependency but not user-device burden.
- **C2-O (P2):** Liveblocks gets one ambiguous sentence at line 62 ("CRDT-as-a-service frameworks push further in the CRDT direction but relocate the vendor dependency to hosted infrastructure"). The hosted-service-by-MAU operational model is still undescribed. Half-sentence fix.

### COMMENDATIONS

- ✓ The Square/Toast/Salesforce replacement at line 155 is *operationally* the right kind of analogue. An ops engineer reading "Square Reader and Toast … operate offline-first on the merchant's own device: a transaction recorded while the network is unreachable settles when connectivity returns" will nod. The argument also strengthens because POS and field service are domains where the *cost* of failed offline operation is concrete and audited.
- ✓ The Automerge caveat at line 159 ("document size growth with edit history, cold-sync time on long-lived documents, and garbage-collection cadence") names the three actual operational pain points an Automerge production user has lived through. Three out of three.
- ✓ Round 1 commendations carry forward: Actual Budget paragraph and the Cassandra/DynamoDB/VS Code/1Password/Tailscale/Docker Desktop production-component reassurance list.

### VERDICT (Production Operator): **PROCEED WITH CONDITIONS**
The Round 1 disqualifying defect is repaired with an analogue that survives operator scrutiny. The Linear and Automerge framings are now operationally honest. Two carryover conditions remain (full-node operational cost flag; Liveblocks half-sentence) but neither blocks. Domain average clears 7.0; the seat signs.

---

## SEAT 3 — The Skeptical Implementer (engineer-shipping perspective)

**Posture:** Same as Round 1. The implementer's question — *should I pick this over Replicache or ElectricSQL, and why?* — was the question Round 1 said the chapter failed to answer. Re-reads with that test.

### DIMENSION SCORES

| # | Dimension | R1 | R2 | Δ | Rationale |
|---|---|---|---|---|---|
| D1 | Does the chapter help me decide vs. Replicache? | 2 | 8 | +6 | Replicache now has its own ~165-word paragraph (line 64) that explicitly identifies it as "the most direct production competitor in this category and the system most often suggested as an off-the-shelf path to local-first apps." The implementer learns: Replicache is a sync framework not a complete application; mutators run server-side; offline writes queue against eventual reconciliation under developer's server control; schema migration / key custody / MDM packaging are out of scope. That is the answer the implementer needed. |
| D2 | Does the chapter help me decide vs. ElectricSQL? | 4 | 7 | +3 | ElectricSQL has its own row in the comparison table (line 130) — "server-authoritative Postgres + selective sync; vendor-held; local SQLite is a filtered replica; open-source core + commercial Electric service." The single-half-sentence problem from Round 1 is mitigated by the table. Prose treatment is still light, but the implementer can now triangulate. |
| D3 | Does the chapter help me decide vs. PowerSync? | 4 | 7 | +3 | Same as ElectricSQL — table row at line 131 gives the implementer the four-axis profile. Prose treatment still light. |
| D4 | Does the chapter help me decide vs. Yjs/Automerge directly | 7 | 8 | +1 | Automerge paragraph is unchanged in its competitive positioning, but the new operational caveat at line 159 (document growth, cold sync, GC) gives the implementer evaluating Automerge a sharper buy-vs-build heuristic. |
| D5 | Clarity of the differentiation claim | 6 | 8 | +2 | "The composition is the contribution" lands three times (lines 14, 135, 193) and the line-159 narrowing names the three falsifiable axes. The implementer can now quote one sentence. The laundry list at lines 197–204 is still long but the comparison table preceding it does the heavy lifting. |
| D6 | Build-or-buy heuristic | 4 | 5 | +1 | The line-135 "every system that satisfies vendor-independent data ownership stops short of team collaboration; every system that supports team collaboration delegates authority to a vendor" is itself a heuristic — the implementer reads it as "if I need both, none of these works; the book's architecture is the candidate." That is *almost* the heuristic Round 1 asked for. The explicit "pick this when X; pick Replicache when Y" framing is still deferred to Ch 4. P2 carryover. |
| D7 | Cost of switching / adoption friction | 5 | 5 | — | Unchanged. The Sunfish .NET/MAUI assumptions and integration cost from existing codebases are still not flagged in Ch 2. P2 carryover; the Sunfish package policy in CLAUDE.md may justify the silence at this chapter level. |
| D8 | Code-or-config-level concreteness | 5 | 5 | — | Unchanged. No third diagram showing where existing Yjs/Automerge code maps onto the inverted stack. P2 carryover. |

**DOMAIN AVERAGE: 6.6 / 10** (Round 1: 4.6; Δ +2.0)

### BLOCKING ISSUES (Skeptical Implementer)

- None. Both Round 1 blockers (B1-SI Replicache absence, B2-SI no like-for-like comparison vector) are resolved.

### CONDITIONS (carry forward, P2-class)

- **C1-SI (carryover):** A provisional decision sentence in Ch 2 ("if your data is single-tenant per-user collaborative documents, Yjs+Y-Sweet ships fastest; if you need typed records with role-scoped access, this book") would convert the implicit heuristic at line 135 into a quotable one. Forward reference to Ch 4 is fine but the implementer should not leave Ch 2 without something they can sketch on a whiteboard.
- **C2-SI (carryover):** Adoption friction acknowledgment for teams already on Yjs/Automerge/Replicache/ElectricSQL. One sentence on what an integration adapter looks like.
- **C3-SI (carryover):** A "where my existing code maps onto the inverted stack" diagram. Optional; deferrable to Ch 3.

### COMMENDATIONS

- ✓ The Replicache paragraph at line 64 is the answer to the question that defined the Round 1 verdict. Its construction — name the system, name the company, name the data structure (IndexedDB), name the architectural commitment (server-side mutators), name where it stops (schema/key/MDM out of scope) — is the right level of specificity for an implementer comparison-shopping in 2026.
- ✓ The comparison table at lines 124–133 lets the implementer do the four-axis triangulation in 30 seconds. This is the artifact Round 1 asked for, delivered at the right detail level.
- ✓ The closing analytical sentence at line 135 — "every system that satisfies vendor-independent data ownership stops short of team collaboration; every system that supports team collaboration delegates authority to a vendor" — is the chapter's strongest competitive frame. It exposes the gap the book is trying to fill in one sentence.
- ✓ Round 1 commendations carry forward (Automerge taxonomy entry; "what this book assembles" enumerated list).

### VERDICT (Skeptical Implementer): **PROCEED WITH CONDITIONS**
The two Round 1 blockers are resolved cleanly and the largest single delta in this review (+6 on D1) belongs to this seat. The chapter now answers the implementer's headline question. Three small carryover conditions remain (decision sentence, adoption friction, integration map) but none blocks. Domain average clears 6.0 with margin; the seat signs.

---

## SEAT 4 — The Pedantic Lawyer (compliance / regulatory / IP)

**Posture:** Same as Round 1. Re-reads with attention to whether the new bracketed citations actually defend the regulatory claims, and whether the DIFC DPL softening survives a deposition test.

### DIMENSION SCORES

| # | Dimension | R1 | R2 | Δ | Rationale |
|---|---|---|---|---|---|
| D1 | Defensibility of claims about specific commercial products | 5 | 7 | +2 | Linear is now [8]-cited; Replicache is [9]-cited and the developer-controlled-mutator framing is defensible. Notion claims unchanged but were already defensible. Anytype framing unchanged — still a contested-but-correct OSI usage that warrants a footnote. |
| D2 | Defensibility of claims about defunct / sanctions-affected vendors | 6 | 6 | — | **No change.** Line 30 still names Adobe, Autodesk, Microsoft, Figma in a 2022 sanctions context with **no citation**. Round 1 P1-5 was tracked as "covered by P0-1 reference list expansion" but the reference list expansion did not actually add a Reuters/AP/BBC/FT primary source for the sanctions exits. This is a Round 2 carryover and arguably a fresh blocker — the regulatory citation upgrade exposes the sanctions roll-call as the only major regulatory claim in the chapter still bare. |
| D3 | Accuracy of regulatory citations | 5 | 8 | +3 | Schrems II is now Case C-311/18 [4]. DPDP 2023 is [5]. DIFC DPL 2020 is [6]. 242-FZ is [7]. Per Appendix E "Legal Decision" pattern, all four are correctly formed. The reference list entries (lines 222–228) carry the right metadata (case number, statute number, jurisdiction, date). |
| D4 | Specificity of regulatory claims | 6 | 8 | +2 | Schrems II framing now reads "structural mechanism that addresses the data-transfer leg of GDPR analysis under Schrems II rather than an architectural preference." This is what the ruling actually compels. The conflation of data-residency-in-general with transfer-leg-specifically is gone. |
| D5 | UAE DIFC DPL claim defensibility | 4 | 8 | +4 | Largest single delta in this seat. Line 185 now reads "constrains processing and cross-border transfers of personal data by DIFC-licensed entities and requires specific lawful bases for transfers to non-adequate jurisdictions." This is defensible against the actual text of DIFC DPL §28 / §27, does not categorically prohibit foreign cloud storage, and a DIFC-licensed entity reading it would not rely on it for a compliance decision they cannot ground in the underlying statute. |
| D6 | Russia 242-FZ historical claim | 5 | 7 | +2 | Now reads "among the early general-purpose data localization laws globally" (line 185). The "first" framing is gone. The carryover Round 1 P2-4 condition is satisfied. |
| D7 | IP / license naming | 8 | 8 | — | Unchanged. AGPLv3, Yjs, Automerge, Cambria still named correctly. |
| D8 | Quotation discipline | 6 | 6 | — | The Figma "inspired by multiple separate CRDTs" string at line 159 is still in quotation marks without a Wallace 2019 attribution. Round 1 condition C4-PL was not addressed. Carryover. |

**DOMAIN AVERAGE: 7.3 / 10** (Round 1: 5.6; Δ +1.7)

### BLOCKING ISSUES (Pedantic Lawyer)

- **B1-PL (CARRYOVER + ESCALATED):** The 2022 sanctions roll-call at line 30 (Adobe, Autodesk, Microsoft, Figma — named in a regulatory action) still carries no citation. Round 1 flagged this as P1-5 with the fix "cite to primary news (Reuters, AP, BBC, FT)." The Round 2 reference list expansion added regulatory citations [4]–[7] but did *not* add the sanctions reporting. With the rest of the regulatory section now properly cited, this sentence is the only major compliance-adjacent claim in the chapter still bare. Per Appendix E §Assembly Guidance #4, naming companies in a regulatory action without citation is a credibility defect. **Fix: add one or two news citations as [10] / [11] (e.g., Reuters or AP coverage of the March 2022 vendor exits) and bracket the line-30 sentence.** This is a small fix but blocks a full PROCEED.

### CONDITIONS

- **C1-PL (carryover):** Cite the Figma quotation at line 159 to Wallace, "Multiplayer Editing in Figma," Figma Engineering Blog, 2019. This was Round 1 C4-PL and was not addressed.
- **C2-PL (P2):** The Cambria reference at line 193 wants a Litt et al. 2020 citation (overlaps with Theorist C1-T).
- **C3-PL (P2):** The Anytype "source available, not open-source" framing at line 36 wants a one-line footnote naming the OSI definition or the Any Source Available License.

### COMMENDATIONS

- ✓ The DIFC DPL softening at line 185 is exactly what the Lawyer asked for in Round 1. The new framing is grounded in the statute's actual structure (transfer requirements + lawful bases) without overstating.
- ✓ The Schrems II framing at line 185 ("structural mechanism that addresses the data-transfer leg of GDPR analysis") is precise about what the ruling compels and disclaims the broader residency conflation.
- ✓ The 242-FZ "among the early" softening at line 185 closes the Round 1 P2-4 condition.
- ✓ The reference list entries [4]–[7] (lines 222–228) are well-formed: case number, statute number, jurisdiction, dates. Appendix E "Legal Decision" pattern is followed correctly.
- ✓ Round 1 commendations carry forward (Anytype precision; "ownership conveyed only through a contract" sentence).

### VERDICT (Pedantic Lawyer): **PROCEED WITH CONDITIONS**
The two Round 1 blockers (DIFC DPL overclaim; sanctions roll-call uncited) are 1.5-of-2 resolved. DIFC DPL is cleanly fixed; the sanctions roll-call carryover is small but real and is escalated as a Round 2 blocker the chapter should clear before final approval. Even with the carryover, domain average reaches 7.3 — the seat signs **with conditions**, not BLOCK, because the underlying claim (companies exited Russia in 2022 under sanctions) is unambiguously true and only the citation is missing. The fix is a 30-minute web search, not a structural rewrite.

---

## SEAT 5 — The Outside Observer (audience accessibility / argumentative cohesion)

**Posture:** Same as Round 1. Re-reads cold, asking whether the front-loaded thesis lands, whether the comparison table reads, and whether the closing list now feels earned rather than ceremonial.

### DIMENSION SCORES

| # | Dimension | R1 | R2 | Δ | Rationale |
|---|---|---|---|---|---|
| D1 | Opening hook / orientation in first 200 words | 7 | 8 | +1 | Opening unchanged through line 12; new line 14 ("**The composition is the contribution** — not the individual components, which are all production-proven somewhere, but the assembly that lets them be one system") gives the cold reader the chapter's thesis up front. The bolding is tasteful — single boldface, single sentence, lands. |
| D2 | Section structure and signposting | 7 | 8 | +1 | The Round 1 awkward "What Each Gets Right" mini-section is now an earned H2 (line 118) carrying substantive material — the comparison table and the analytical close. The chapter now has four real sections (Seven Ideals → Taxonomy → What Each Gets Right → Missing Step → What This Book Adds — five if you count the close) and each carries its own argumentative weight. |
| D3 | Paragraph length discipline | 6 | 6 | — | The long-now paragraph at line 30 is *unchanged*. Round 1 C2-OO ("trim to: Sunrise Calendar one sentence → 2022 sanctions wave one tight sentence with citation → 'proprietary sync formats fail this property' closer") was not addressed. The paragraph still runs six beats. The Replicache paragraph at line 64 is also long (~165 words, 6+ sentences) but earns its length. The line-159 paragraph after the Square/Toast replacement runs ~10 sentences and is the longest in the chapter — borderline overlong for the style guide's "no paragraph longer than 6 sentences" target. |
| D4 | Voice consistency with Part I register | 7 | 7 | — | The list section at lines 197–204 still drifts into Part III specification voice. The comparison table at lines 124–133 also leans specification rather than narrative — but it is appropriate at that location because it earns its slot. Net: holds at 7. |
| D5 | Acronym / first-use discipline | 8 | 8 | — | Still strong. New acronyms in revised text (none material) all introduced cleanly. The "CRDT" double-spell-out from Round 1 (lines 28 and 36) is also unchanged — line 36 still spells out "CRDT (Conflict-free Replicated Data Type)" again. P2 carryover from Round 1 P2-9. |
| D6 | Cross-reference clarity | 7 | 7 | — | Forward-reference density appears unchanged — Round 1 counted 11; a quick recount finds approximately the same (Chapter 3, Chapter 4 ×3, Part II, Part III, Part IV, Appendix F, Chapter 6 implicit, Chapter 11). Round 1 C5-OO ("halve the forward-reference density") was not addressed. P2 carryover. |
| D7 | The "what this book adds" landing | 6 | 9 | +3 | The Round 1 fuzzy gestalt is gone. "The composition is the contribution" lands at line 14 (opening), line 135 (midpoint, after the table), and line 193 (close). Three landings, identical phrasing. The cold reader leaves with one quotable sentence — exactly the Round 1 ask. |
| D8 | Anti-AI-tells / freshness of phrasing | 7 | 7 | — | Round 1 flagged "stands on the local-first community's work" at line 191 (Round 2 line 208) — unchanged. "Structural property that follows from where authority lives" at line 140 / Round 2 line 157 also unchanged. New text introduces no fresh AI-tells. P2 carryover. |

**DOMAIN AVERAGE: 7.5 / 10** (Round 1: 6.9; Δ +0.6)

### BLOCKING ISSUES (Outside Observer)

- None. Round 1 had B1-OO (no memorable thesis sentence); resolved by the three landings of "the composition is the contribution."

### CONDITIONS (carry forward, P2-class)

- **C1-OO (carryover):** Trim the long-now paragraph at line 30 per Round 1 C2-OO. The Sunrise Calendar + Adobe + Autodesk + Microsoft + Figma + sanctions + format-failure-closer six-beat structure is still in place.
- **C2-OO (carryover):** Trim the line-159 paragraph (the production-analogue paragraph after the Square/Toast replacement). It runs ~10 sentences. Either split into two paragraphs at the "What this book contributes is the *composition*" pivot or trim the named-component list.
- **C3-OO (carryover):** Halve the forward-reference density per Round 1 C5-OO.
- **C4-OO (carryover):** Replace "stands on the local-first community's work" with "builds on" per Round 1 P2-8.
- **C5-OO (carryover):** Spell out CRDT once per chapter, not twice.

### COMMENDATIONS

- ✓ The three-landing thesis ("the composition is the contribution" at lines 14, 135, 193) is exactly the structural fix Round 1 asked for. The midpoint landing at line 135 lands particularly well because it follows the comparison table — the reader sees the gap, then reads the thesis as the answer to it.
- ✓ The new H2 at line 118 ("What Each Gets Right — and Where It Stops") is a real section now. The transition-paragraph-as-fake-H2 critique from Round 1 is resolved.
- ✓ The comparison table at lines 124–133 is the chapter's most dense single artifact — eight rows, four columns, all readable at-a-glance. Round 1 commendations on the seven-properties tour and acronym discipline carry forward.

### VERDICT (Outside Observer): **PROCEED WITH CONDITIONS**
The Round 1 conditions on thesis landing and the "What Each Gets Right" mini-section are resolved cleanly. The carryover P2 conditions (long-now paragraph trim, forward-reference density, CRDT double-spell-out, anti-AI-tells phrase) are stylistic polish rather than structural defects. Domain average rises from 6.9 to 7.5 — the seat signs, with the same PROCEED-WITH-CONDITIONS verdict it gave in Round 1, now with five P2 conditions instead of five P1+P2 conditions.

---

## COUNCIL TALLY — ROUND 2

| Member | R1 Domain Avg | R2 Domain Avg | Δ | R1 Verdict | R2 Verdict |
|---|---|---|---|---|---|
| Theorist | 5.9 | **7.5** | +1.6 | REVISE | **PROCEED WITH CONDITIONS** |
| Production Operator | 6.0 | **7.1** | +1.1 | REVISE | **PROCEED WITH CONDITIONS** |
| Skeptical Implementer | 4.6 | **6.6** | +2.0 | REVISE | **PROCEED WITH CONDITIONS** |
| Pedantic Lawyer | 5.6 | **7.3** | +1.7 | REVISE | **PROCEED WITH CONDITIONS** |
| Outside Observer | 6.9 | **7.5** | +0.6 | PROCEED WITH CONDITIONS | **PROCEED WITH CONDITIONS** |
| **Overall** | **5.8** | **7.2** | **+1.4** | **REVISE** | **PROCEED WITH CONDITIONS** |

**Round-level verdict:** **PROCEED WITH CONDITIONS.** All five seats sign. The Round 1 mandate (clear all four REVISE verdicts and reach PROCEED-WITH-CONDITIONS or PROCEED across all five seats) is met. Per-member scores all clear the 7.0 ideal except the Skeptical Implementer at 6.6 — which still clears the 6.0 floor and represents the largest single Round-over-Round improvement (+2.0). The chapter is approved for advancement to ICM Stage 6 (voice-check) subject to the residual conditions tracked below.

---

## REGRESSION CHECK

The council looks for new defects introduced by the Round 1→Round 2 revision.

| Area | Regression? | Notes |
|---|---|---|
| Word count discipline (CLAUDE.md QC-1, ±10% of 4,000 = 3,600–4,400) | None observed | Round 1 measured ~3,950. Net additions: Replicache paragraph (~165 words), comparison table (~120 words), Square/Toast replacement (~120 words vs. M-PESA ~80 words), citations and softenings (~60 words). Net trims: minor. Estimated Round 2 word count: ~4,200, within tolerance. |
| Voice consistency (Part I narrative register) | Minor regression at line 159 | The expanded production-analogue paragraph runs ~10 sentences and contains a comma-spliced enumerated list of three differentiators ("a per-record CAP boundary that lets AP-class records and CP-class records coexist in one system, an MDM-deployable installer model that lets enterprise IT ship full-node software without bespoke onboarding, and an AGPLv3-with-managed-relay business model that makes the architecture economically viable without forcing vendor data custody"). This drifts slightly into spec voice. Tracked as Outside Observer C2-OO. Not a Round 2 blocker. |
| Citation accuracy of new entries [4]–[9] | None observed | All entries follow Appendix E format. Schrems II case number correct. DPDP date correct. DIFC DPL number correct. 242-FZ enactment / effective dates correct. Linear blog and Replicache docs URL-anchored. |
| Reference numbering integrity | None observed | [1]–[9] used in order of first appearance (1 line 10, 2 line 208, 3 line 36, 4 line 185, 5 line 185, 6 line 185, 7 line 185, 8 line 58, 9 line 64). Per Appendix E first-appearance ordering rule, this is correct (each citation appears in order of its first prose use, with the regulatory cluster all landing in the line-185 paragraph after the order has been established earlier). |
| Mermaid diagrams | No regression | Both diagrams unchanged. Still render. |
| Anti-AI-tells | No regression | The Round 1 flags ("stands on … community's work"; "structural property that follows from where authority lives") are unchanged. New prose introduces no fresh tells. |
| Acronym discipline | No regression | All new acronyms (CIS already established, no new MDM use, AGPLv3 already established) introduced cleanly or already established. |

**Net regression assessment:** One minor voice-register drift at line 159 (the expanded production-analogue paragraph). No material regressions. The revision is additive, not corrosive.

---

## CONSOLIDATED ACTION ITEMS — ROUND 2

### Blocking Issues (resolve before final approval)

| # | Raised By | Issue | Location |
|---|---|---|---|
| **B1-R2** | Lawyer | 2022 sanctions roll-call (Adobe, Autodesk, Microsoft, Figma) still uncited. Carryover from R1 P1-5; escalated because the rest of the regulatory section is now cited and the bare sentence is now the only major compliance-adjacent claim without a primary source. Fix: add one or two news refs (Reuters/AP/BBC/FT March 2022) as [10]/[11]. | Line 30 |

### Conditions (required for full PROCEED, not for PROCEED WITH CONDITIONS)

| # | Raised By | Condition | Location |
|---|---|---|---|
| C1 | Theorist + Lawyer | Cite Cambria reference to Litt et al. 2020. | Line 193 |
| C2 | Theorist + Lawyer | Attribute the Figma "inspired by multiple separate CRDTs" quotation to Wallace 2019. | Line 159 |
| C3 | Theorist | Distinguish op-based vs. state-based CRDT in one sentence (or commit to "operation-based CRDT" phrasing throughout). | Seven Ideals section |
| C4 | Operator | One sentence in Ch 2 acknowledging the *operational* cost of running a full node (device provisioning, key custody UX, support burden). | Around line 206 |
| C5 | Operator | Half-sentence on Liveblocks' hosted-service-by-MAU operational model. | Line 62 |
| C6 | Implementer | Provisional decision sentence ("if your data is single-tenant per-user collaborative documents, Yjs+Y-Sweet ships fastest; if you need typed records with role-scoped access, this book"). | Around line 135 |
| C7 | Implementer | One sentence on adoption/integration friction for teams already on Yjs/Automerge/Replicache/ElectricSQL. | Around line 159 |
| C8 | Outside Observer | Trim the long-now paragraph to three beats. | Line 30 |
| C9 | Outside Observer | Trim or split the line-159 production-analogue paragraph (~10 sentences). | Line 159 |
| C10 | Outside Observer | Halve the forward-reference density (currently ~11; target ~5–6). | Throughout |
| C11 | Outside Observer | Replace "stands on the local-first community's work" with "builds on." | Line 208 |
| C12 | Outside Observer | Spell out "CRDT" once per chapter, not twice. | Line 36 |

### Commendations (carry forward across rounds)

- The three landings of "the composition is the contribution" (lines 14, 135, 193) — the chapter now has a quotable thesis. (Outside Observer)
- The Replicache paragraph at line 64 — the strongest piece of competitive positioning the chapter now contains; structurally parallel to the Automerge paragraph and arrives at the right verdict. (Theorist + Implementer)
- The comparison table at lines 124–133 — eight rows × four columns; the implementer's apples-to-apples answer in 30 seconds. (Implementer)
- The Square Reader / Toast / Salesforce Mobile SDK replacement at line 155 — operationally honest analogue that survives an ops engineer's "is this actually a device replica" test. (Operator)
- The DIFC DPL softening and Schrems II "data-transfer leg" precision at line 185 — defensible against the underlying statutes / ruling. (Lawyer)
- The line-159 narrowing of "what this book adds" to three falsifiable axes (per-record CAP boundary; MDM-deployable installer; AGPLv3-with-managed-relay business model) — the differentiator is now testable rather than rhetorical. (Theorist + Implementer)
- The Automerge operational caveat at line 159 (document growth, cold sync, GC cadence) — names the three actual production pain points. (Operator)
- Reference list grew from 3 to 9 entries with correct Appendix E formatting; case number, statute number, jurisdiction, dates all in place. (Lawyer)

---

## ROUND 2 GATING CRITERIA — STATUS

| Criterion | Status |
|---|---|
| 1. P0-1 through P0-4 resolved | **MET** (all four) |
| 2. Word count within ±10% of 4,000 | **MET** (estimated ~4,200) |
| 3. Citation count rises from 3 to ~13 | **PARTIALLY MET** — count rose from 3 to 9. The originally-projected 13 assumed Cambria, Flease, Wallace 2019, and primary sanctions news would also land. Three of those four are still missing (Flease was relocated out of this chapter; Cambria and Wallace 2019 are tracked as carryover conditions; sanctions news is the residual blocker). |
| 4. Replicache paragraph parallels Automerge | **MET** |
| 5. M-PESA paragraph replaced with defensible precedent | **MET** |

**Overall gating status:** The chapter clears Round 2 with PROCEED WITH CONDITIONS across all five seats. One small residual blocker (B1-R2 sanctions citation) and twelve P2-class conditions remain. The chapter is approved for ICM Stage 6 (voice-check). Final PROCEED requires resolving B1-R2 and at least the Theorist/Lawyer C1–C2 citations before assembly.

---

*End of Round 2 review.*
