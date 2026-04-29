KLEPPMANN COUNCIL REVIEW — Round 2
Document: chapters/part-1-thesis-and-pain/ch04-choosing-your-architecture.md
Date: 2026-04-29
Council composition: chapter-calibrated (Theorist / Production Operator / Skeptical Implementer / Pedantic Lawyer / Outside Observer)
Word count: Round 1 ~3,420 → Round 2 ~5,075 (+42%, content-driven, R1-mandated)
=====================================

## Round-1-to-Round-2 Resolution Audit (run before scoring)

| ID | Class | Status | Evidence |
|---|---|---|---|
| P0-1 | Filter ordering & tiebreaker | RESOLVED | New paragraph at lines 28 names F1/F2/F4 as hard-stop-capable, asserts the precedence chain, and resolves the F2-vs-F4 contradiction explicitly ("F4 wins, even if F2 and F3 cleared"). |
| P0-2 | F5 operational capability gap | RESOLVED | New sub-section in Filter 5 (lines 148–158) names endpoint observability, MDM coordination, supply-chain signing/SBOM, on-call across unowned endpoints. Forward-pointer to Part IV (Ch17–20) and Ch21 present at line 158. |
| P0-3 | Worked example | RESOLVED | New "Construction-Industry SaaS Migration" walk-through at lines 228–242. ~280 words. Walks F1→F5 with a Zone C verdict and concrete Phase 1 / Phase 2 migration. Forward-pointer to Ch18. |
| P0-4 | Per-Zone compliance posture | RESOLVED | New 5-row × 3-Zone table at lines 218–224 (GDPR/Schrems II, HIPAA, DIFC/GCC, India DPDP/RBI, SOC 2). Followed by analytical paragraph at line 226 stating local-first shifts compliance burden, not skips it. |
| P0-5 | Zones-as-spectrum acknowledgment | RESOLVED | New paragraph at line 164 explicitly names the three Zones as "anchor points on a spectrum, not a strict partition" and acknowledges between-Zone projects and the Zone-C-toward-Zone-A migration trajectory. |
| P1-1 | F2 regulatory-custodian doing F1's job | RESOLVED | Parenthetical at line 60 redirects regulatory-custodian-mandated authoritative-copy to Filter 1 explicitly. |
| P1-2 | Zone A operational sketch | RESOLVED | New paragraph at line 198 names MDM-managed endpoint fleet + Anchor accelerator + relay topology + observability pipeline + relay-failure behavior. Cross-references Part III and Part IV/Ch21. |
| P1-3 | Filter 3 table column mixing | DEFERRED | Per user note — copyedit-stage. |
| P1-4 | Filter 4 table column mixing | DEFERRED | Per user note — copyedit-stage. |
| P1-5 | Small-team-fast-ship as Zone B | RESOLVED | Named explicitly in Zone B description at line 202, with the "two-person weekend prototype" worked example. |
| P1-6 | EU-US Data Privacy Framework | RESOLVED | Acknowledged at line 95 alongside Schrems II, with the appropriate "in active legal review" hedge. |
| P1-7 | HIPAA §164.308 administrative safeguards | RESOLVED | Named at line 68, paired with §164.312, with explicit acknowledgment that endpoints make administrative safeguards harder. |
| P1-8 | GDPR Art. 28 relay-as-processor | RESOLVED | New paragraph at line 212 names Article 28, the processor framing, and forward-points to Ch15. |
| P1-9 | Filter ordering justification | RESOLVED | Folded into P0-1 — same paragraph. |
| P1-10 | Part III/IV cross-references | RESOLVED | Folded into P1-2 (line 198) and P0-2 (line 158). |
| P2-1 to P2-5 | Stylistic / appendix-pointer / citation precision | OUT OF SCOPE | Voice-pass / copyedit. Not regression-checked here. |

**Regression check (new content introduced by the revision):**

- The new filter-ordering paragraph (line 28) introduces the claim that F1, F2, and F4 are the hard-stop-capable filters. This is consistent with the per-filter tables (F1 explicit "Stop"; F2 explicit Centralized verdicts in two rows; F4 explicit Centralized verdict for network-effects row). No internal contradiction. **No regression.**
- The HIPAA paragraph at line 68 was revised to fold §164.308 into the existing §164.312 sentence. The revised sentence is longer and dense; it remains readable. **No regression on the legal axis; mild prose-density flag for voice-pass.**
- The Zone A operational paragraph (line 198) introduces a "self-hosted or managed relay" claim. This is consistent with the existing Zone A definition at line 194 ("the relay is optional infrastructure"). **No regression.**
- The compliance-posture table (lines 218–224) introduces SOC 2 as a fifth regime, which was not in the R1 chapter at all. SOC 2 mapping is correctly drawn (vendor SOC 2 covers software supply chain, customer IT covers endpoints). **No regression; net addition.**
- The worked example (lines 228–242) introduces the "double-entry change-order ledger as per-project lease" claim. This is a new technical claim. It is consistent with v13's lease/Flease pattern, but the chapter does not cite it inline. **Mild — flagged below.**
- The Zone B paragraph (line 202) now includes the small-team-fast-ship case in a long sentence that joins multiple Zone B drivers. Reads cleanly. **No regression.**
- New parenthetical at line 60 (F2 regulatory-custodian → F1) creates a small forward-reference paradox: the reader is in F2 being told the row is actually F1, but F1 has already been read. The fix is correctly placed as an aside, not a re-decision. **No regression.**

---

## SEAT 1 — The Theorist

DIMENSION SCORES (Δ from Round 1):

  D1 Zone taxonomy completeness: 7 (+1) — The zones-as-spectrum paragraph at line 164 acknowledges the partition is approximate; this directly addresses the Round 1 concern that "three categories" was being asserted rather than defended. The taxonomy is now honest about being three anchor points. Pure-P2P-no-relay and federated-multi-relay still unnamed (P2-4 deferred), but the framing moved from "exhaustive" to "the positions most teams settle at," which is what the Theorist asked for.
  D2 Filter orthogonality: 7 (+2) — The filter-ordering paragraph at line 28 explicitly names F1/F2/F4 as hard-stop-capable and resolves F2-vs-F4 contradictions in F4's favor. The orthogonality concern is no longer that the filters secretly overlap; it is that the chapter now openly admits some overlap and resolves it by precedence. P1-1's parenthetical at line 60 closes the F2-doing-F1's-job loop. Filters are not formally orthogonal, but the precedence chain replaces orthogonality with a deterministic ordering, which is sufficient for a decision framework.
  D3 Edge-case handling: 7 (+2) — The mixed-ownership case is still routed through Zone C in the prose at line 66, and the worked example at lines 228–242 demonstrates the routing concretely. The flowchart still does not encode the mixed-ownership split, but the prose now backs it with a real walkthrough. The "borderline F2" case still produces a Zone label without a confidence interval, but the spectrum acknowledgment at line 164 frames that limitation honestly.
  D4 Definitional rigor: 8 (=) — CAP framing at line 41 unchanged and still correct; the worked example introduces "per-project lease" for the change-order ledger which is consistent with the broader lease pattern but uncited inline. Mild flag for the Theorist: a new technical claim should carry its source.
  D5 Tiebreaker logic: 8 (+5) — The largest improvement. The new paragraph at line 28 ends the "you are wrong" terminus by stating "F4 wins, even if F2 and F3 cleared." The decision framework now terminates in a Zone in every traversable path. The flowchart at lines 166–190 reflects this — every branch terminates at ZA, ZB, or ZC.
  D6 Citation discipline: 7 (=) — v13 §20.2–20.8 still cited in the chapter frontmatter; the worked example introduces v13 §20-class material (per-project lease for the ledger) without inline citation. Same level of discipline as Round 1, with one new uncited claim.
  D7 Theoretical honesty about what the framework cannot decide: 8 (+2) — The spectrum paragraph at line 164 is the largest improvement. The chapter now openly says "three positions most teams settle at, not as the only positions the architecture supports." This is the honesty the Round 1 review asked for.
  D8 Mutual exclusivity of zones: 7 (+3) — The spectrum framing at line 164 directly addresses the Round 1 finding that the chapter sold a spectrum as a partition. Mutual exclusivity is now explicitly disavowed. The Zones remain useful taxonomic anchors, which is the right outcome.

DOMAIN AVERAGE: 7.38 / 10  (Round 1: 5.5 / 10 — Δ +1.88)

BLOCKING ISSUES:
  None. B1 (Round 1) RESOLVED via P0-1.

CONDITIONS:
  C1 (carry forward, downgraded to P2): Inline-cite the per-project lease claim in the worked example (line 232) — v13 §X or Ch15 forward-pointer. New material introduces a technical claim without source.
  C2 (carry forward, downgraded to P2): The flowchart still does not encode the mixed-ownership split between primary and secondary records. The prose routes it through Zone C; the flowchart could mirror that routing with one Q-node split or one annotation. Optional.

COMMENDATIONS:
  ✓ The filter-ordering paragraph at line 28 is the most theoretically load-bearing addition between Round 1 and Round 2. It converts the funnel from a vibes-based ordering into a precedence chain with explicit dominance ("F4 wins, even if F2 and F3 cleared"). This is exactly the formal property a decision framework needs.
  ✓ The spectrum acknowledgment at line 164 ("anchor points on a spectrum, not a strict partition") is the right register — it preserves the taxonomy's utility while disclaiming the partition claim.
  ✓ The worked example at lines 228–242 closes the Round 1 gap on "framework demonstrates its own application" with a real per-filter walk that lands at Zone C with a concrete migration sequence.

VERDICT: PROCEED WITH CONDITIONS
The Theorist's Round 1 concerns — non-orthogonal filters with no tiebreaker, partition-as-spectrum, no demonstration of the framework on a real case — are all directly addressed. The chapter is now a defensible decision framework, not a sketch of one. Two minor carries forward (C1 and C2) are downgrades to P2; neither blocks Round 2 PROCEED-WITH-CONDITIONS.

---

## SEAT 2 — The Production Operator

DIMENSION SCORES (Δ from Round 1):

  D1 Zone A operational story: 8 (+4) — The new paragraph at line 198 names the four operational components (MDM-managed endpoint fleet, Anchor accelerator, self-hosted or managed relay, fleet observability pipeline) and what happens at relay failure. This is the relay-failure paragraph from F4 that R1 commended, now extended to Zone A. Cross-references to Part III and Part IV/Ch21 give the reader where to go for depth. Operational Operator's Round 1 ask was met directly.
  D2 Zone C operational story: 7 (+2) — The Zone C definition at lines 206–212 is unchanged, but the relay-as-processor paragraph at line 212 adds the GDPR Article 28 framing which is operationally relevant (the relay operator's contractual obligations affect on-call escalation paths). Plus the compliance-posture table at line 222 specifies what each Zone enables, which is operationally usable.
  D3 Zone B operational story: 8 (=) — Unchanged from Round 1; still appropriate brevity for a 25-year-prior architecture.
  D4 Failure mode coverage per Zone: 6 (+3) — The Zone A relay-failure behavior is now named at line 198 ("when the relay fails, day-to-day work continues on the local plane; sync catches up when the relay returns"). The "last device dies" failure mode is still not named in this chapter, which is acceptable because Ch04 is a decision framework and that failure mode belongs in Ch15-16 or Ch17-20. The Round 1 score weight came from the Zone A operational sketch; that has been added.
  D5 Capacity planning / cost-of-operation per Zone: 5 (+1) — Still not addressed. The compliance-posture table at line 226 acknowledges that Zone A shifts cost to the customer's IT, which is the right framing for one form of operational cost-shifting, but per-seat infrastructure cost numbers are not present. This is acceptable for a decision framework chapter; it would be unacceptable for a Part IV ops chapter.
  D6 Migration / rollback story between Zones: 7 (+1) — The worked example demonstrates a Zone B → Zone C migration in concrete Phase 1 / Phase 2 terms with a 90-day + 6-month timeline. This is a real operational artifact. Zone-A-to-Zone-B rollback still unaddressed; acceptable.
  D7 Observability / debuggability per Zone: 7 (+4) — The new F5 operational sub-section at line 150 names "fleet telemetry exported from each node to a metric and log aggregator the operator runs" — this directly addresses the Round 1 concern that the chapter was silent on Zone A observability. Plus the Zone A operational picture at line 198 names the observability pipeline as a first-class component.
  D8 Operational maturity required to choose each Zone: 8 (+3) — F5 now has an "engineering capability is necessary but not sufficient" hinge at line 148, then names four operational disciplines (endpoint observability, MDM coordination, supply-chain signing/SBOM, on-call across unowned endpoints) at lines 150–156. The Round 1 finding that F5 covered engineering but not operational capability is fully addressed. The closing line at 158 ("a team that treats operational capability as something to figure out post-launch ships software that fails customer 1") is operationally honest.

DOMAIN AVERAGE: 7.0 / 10  (Round 1: 4.75 / 10 — Δ +2.25)

BLOCKING ISSUES:
  None. B2 (Round 1) RESOLVED via P0-2.

CONDITIONS:
  C3 (new, P1): The "supply-chain signing and SBOM discipline" paragraph at line 154 says "Skipping this in early releases is fine; skipping it before enterprise procurement review is not." This is correct, but a Production Operator would prefer an explicit named milestone — e.g., "before customer 1's procurement review" or "before the first non-design-partner customer" — because "early releases" is vague enough that a team will mis-time it. One-sentence tightening, not a structural fix.
  C4 (carry forward, P2): Per-seat operational cost is still unmodeled. Acceptable for a decision framework but flagged for the Production Operator's interest. Belongs in Ch17 or Ch21, not here.

COMMENDATIONS:
  ✓ The operational-capability sub-section at lines 148–158 is the model fix. It does not duplicate Part IV; it names what Part IV will cover and forward-points. This is the right division of labor between a Part I decision framework and a Part IV playbook.
  ✓ The Zone A operational picture at line 198 mirrors the F4 relay-failure paragraph that the Round 1 review commended — exactly as the Round 1 condition C6 asked. The chapter is internally consistent in its operational register.
  ✓ The closing line at 158 — "ships software that fails customer 1" — is the kind of operationally specific failure-mode statement that signals the chapter understands what shipping enterprise software actually feels like.

VERDICT: PROCEED WITH CONDITIONS
The Operations Operator's Round 1 REVISE is fully resolved. The chapter now equips a team to evaluate not just whether they can build Zone A but whether they can run it. The two carry-forwards (C3 milestone naming, C4 cost-modeling) are P2 and belong in voice-pass or downstream chapters.

---

## SEAT 3 — The Skeptical Implementer

DIMENSION SCORES (Δ from Round 1):

  D1 Decision actionability: 8 (+1) — The worked example at lines 228–242 ends in a concrete Phase 1 / Phase 2 plan with a 90-day + 6-month timeline. A reader can map their own product onto the example's shape. The Anchor/Bridge accelerator pointer at the closing section is unchanged and still strong.
  D2 Use-case ruling-OUT honesty: 9 (+1) — The Round 1 commendation for "Building financial trading infrastructure on a local-node architecture is not principled — it is wrong for the domain" is preserved at line 204. The Round 1 miss — small-team-fast-ship Zone B — is now named explicitly at line 202 with the "two-person weekend prototype" example. Ruling-OUT honesty is now complete.
  D3 Apples-to-apples table discipline: 6 (=) — P1-3 (Filter 3 mixed columns) and P1-4 (Filter 4 mixed columns) are deferred to copyedit. Score unchanged. The deferral is acknowledged and acceptable for Round 2; this is a copyedit-stage concern.
  D4 Decisiveness: 8 (+1) — The new precedence-chain paragraph at line 28 is decisive in exactly the way the Round 1 review asked for. The mixed-ownership case still produces "Zone C usually" rather than a hard rule, but the worked example demonstrates the routing.
  D5 Self-test usability: 7 (+1) — The worked example provides a model run that calibrates the reader's interpretation. "Atomic across multiple users simultaneously" is still a precision-demanding phrase, but the worked example's F1 walk ("a two-hour eventual-consistency window during reconnection is acceptable") shows what the right answer looks like in practice.
  D6 Worked-example pull-through: 9 (+5) — The largest improvement. The construction-industry SaaS example at lines 228–242 is the Round 1 condition C8 fully delivered. It walks all five filters with a Zone verdict and a concrete migration plan. ~280 words is the right length — long enough to be useful, short enough not to crowd the framework.
  D7 In-between team ergonomics: 6 (+1) — The spectrum acknowledgment at line 164 helps the in-between team see that they are not anomalous. The shortcut at line 248 still produces "Zone A or Zone C" for the common pass case; the worked example demonstrates the Zone-C-from-existing-product path concretely.
  D8 Reading economy: 6 (-1) — The chapter grew from ~3,420 to ~5,075 words (+42%). The growth is content-driven and Round-1-mandated, and the user note explicitly tells the council not to flag it as P0. Noting it as a -1 score because reading economy is a real Skeptical Implementer concern; the chapter is denser, even if the density earns its keep. Voice-pass should look at whether the operational-capability sub-section in F5 can lose 50–100 words without losing substance.

DOMAIN AVERAGE: 7.38 / 10  (Round 1: 6.25 / 10 — Δ +1.13)

BLOCKING ISSUES:
  None. B3 (Round 1) RESOLVED via P0-3.

CONDITIONS:
  C5 (new, P2): Reading economy. The chapter is now ~5,075 words; some of the F5 operational-capability sub-section could compress without losing the four named disciplines. Voice-pass concern.
  C6 (carry forward, copyedit-stage): P1-3 and P1-4 column-mixing deferred. Should be addressed before publication.

COMMENDATIONS:
  ✓ The worked example at lines 228–242 is the highest-leverage addition between Round 1 and Round 2 from the Skeptical Implementer's lens. It converts the five-filter framework from theory into a runnable procedure with a sample output.
  ✓ The Zone B small-team-fast-ship case at line 202 closes the Round 1 finding that the chapter under-named the case where the architecture is overkill. This is honest framework discipline.
  ✓ The opening question at line 12 and the honest-limit at line 204 are preserved unchanged. The chapter's strongest single sentences are intact.

VERDICT: PROCEED WITH CONDITIONS
The Skeptical Implementer's Round 1 REVISE is resolved. The worked example, the small-team-fast-ship naming, and the precedence chain together make this a chapter a reader can execute against their own product. The deferred column-mixing concerns are real but copyedit-stage.

---

## SEAT 4 — The Pedantic Lawyer

DIMENSION SCORES (Δ from Round 1):

  D1 Accuracy of named regulations: 8 (+1) — All Round 1 named regulations preserved correctly. EU-US DPF (2023) added at line 95 with the appropriate "in active legal review and may not survive the next round of court challenges" hedge — this is the right level of caution for a 2026 publication. SOC 2 added in the compliance table at line 224 and correctly scoped to vendor-vs-customer responsibility.
  D2 Scope precision: 7 (+2) — HIPAA paragraph at line 68 now names §164.308 administrative safeguards alongside §164.312 technical safeguards, with the explicit acknowledgment that endpoints make administrative safeguards harder. This was the Round 1 ask. DIFC clause still appropriately hedged with "may." The chapter still does not cite the specific DIFC DPL article number (P2-5 deferred); acceptable for now.
  D3 Currency: 7 (+1) — EU-US DPF (2023) acknowledged. The chapter's hedge that the DPF "is itself in active legal review and may not survive the next round of court challenges" is the right disposition for a 2026 publication. India DPDP enforcement variance still not addressed; acceptable scope.
  D4 Per-Zone compliance posture specification: 8 (+4) — The compliance-posture table at lines 218–224 is the load-bearing fix the Round 1 review asked for. Five regimes × three Zones = fifteen cells, each one sentence. The framework now lets a general counsel build a compliance memo from the chapter directly. The analytical paragraph at line 226 ("Local-first does not skip compliance; it shifts where compliance burden sits") is the right framing — it inverts the common assumption that local-first is compliance-friendlier without being defensive about the cases where it shifts burden to the customer.
  D5 IP / licensing implications by Zone: 4 (+1) — The Zone C definition's GDPR Article 28 paragraph at line 212 names the relay-operator-as-processor question, which is a partial IP-class question (it's a data-processing-agreement framing, which has IP-adjacent terms). Employee-leaves-with-data still unnamed; acceptable.
  D6 Audit trail / evidentiary posture per Zone: 6 (+2) — HIPAA cell in the compliance table specifies that §164.312 technical safeguards are met by encryption-at-rest + role-scoped keys, which implies audit trail. The compliance table's structure — what each Zone enables structurally vs. what depends on operator policy — gives an auditor a reading frame. Per-Zone audit trail is not specified explicitly; it is implied by the table.
  D7 Cross-border transfer treatment: 7 (+1) — The Article 28 paragraph at line 212 names the relay-operator-in-different-jurisdiction question for the first time. The compliance table's GDPR row also names "Relay holds ciphertext only" (Zone A) and the Article 28 requirement (Zone C) — this is the cross-border-transfer treatment the Round 1 review asked for, packaged in the table.
  D8 Citation discipline for legal claims: 7 (=) — Same level as Round 1. Appendix F still pointed to without section numbers (P2-3 deferred). Acceptable.

DOMAIN AVERAGE: 6.75 / 10  (Round 1: 5.25 / 10 — Δ +1.50)

BLOCKING ISSUES:
  None. B4 (Round 1) RESOLVED via P0-4.

CONDITIONS:
  C7 (carry forward, P2): Cite specific DIFC DPL article number when the appendix is finalized. P2-5 deferred to copyedit / appendix-finalization stage.
  C8 (carry forward, P2): Appendix F section numbers in inline references. P2-3 deferred.
  C9 (new, P2): The HIPAA paragraph at line 68 is now one of the densest sentences in the chapter (about 90 words). Voice-pass should consider splitting the sentence at "endpoints make administrative safeguards harder, not easier" into a second sentence for readability without losing legal precision.

COMMENDATIONS:
  ✓ The compliance-posture table at lines 218–224 is the largest legal improvement between Round 1 and Round 2. It is a real artifact a general counsel can use. The five regimes chosen are the five most-asked-about in 2026 enterprise procurement.
  ✓ The "Local-first does not skip compliance; it shifts where compliance burden sits" framing at line 226 is the rare honest sentence about local-first compliance. Most marketing materials claim local-first solves compliance; this chapter accurately states it relocates compliance, and names which side gets the burden under each Zone.
  ✓ The EU-US DPF acknowledgment at line 95 with the active-legal-review hedge is exactly the right disposition. Most chapters published in 2026 either ignore the DPF or treat it as resolved; the chapter holds the right level of legal caution.

VERDICT: PROCEED WITH CONDITIONS
The Pedantic Lawyer's Round 1 REVISE is resolved. The chapter is no longer a regulatory citation list; it is now a regulatory framework a counsel can use to shape Zone choice. The remaining conditions (DIFC article number, Appendix F section numbers, HIPAA sentence density) are P2 and belong in copyedit / appendix-finalization passes.

---

## SEAT 5 — The Outside Observer

DIMENSION SCORES (Δ from Round 1):

  D1 Opening-question force: 9 (=) — The opening at line 12 is unchanged. Still the strongest single sentence in the chapter.
  D2 Argumentative cohesion: 8 (+1) — The new precedence-chain paragraph at line 28 directly addresses the Round 1 finding that the filter order was unjustified. The chapter now reads with explicit dominance reasoning rather than implicit ordering. The cohesion is materially improved.
  D3 Reader-paralysis risk: 6 (+1) — The chapter is denser than Round 1 (+42% words). The compliance-posture table and the worked example both add real reader value but also add reading load. The shortcut at line 248 still helps. Net: paralysis risk reduced because the worked example shows the framework producing a verdict, but raised because the chapter is now ~5,075 words.
  D4 Voice consistency with Part I: 8 (=) — Active voice preserved. Strong verbs preserved. No academic scaffolding introduced by the new content. The new operational sub-section in F5 reads in the same register as the rest of the chapter. The compliance table is appropriately terse.
  D5 Anti-AI-tells discipline: 7 (=) — Same level as Round 1. New material does not introduce "delve," "tapestry," "underscore," or other tells. The HIPAA sentence at line 68 is dense but not AI-stylistic; it is dense in the lawyer-careful register, which is appropriate.
  D6 Literary-device deployment: 6 (=) — Anaphora at lines 22–24 preserved. The four-item list at line 14 still breaks triadic cadence (P2-1 deferred). The worked example uses italicized filter labels (*Filter 1 (Consistency).*) as a structural device, which works as a list marker without becoming a cadence break.
  D7 Transitions and flow: 7 (=) — The new sections (operational sub-section in F5, compliance table, worked example) are each preceded by a clear hinge sentence. The transition from compliance table to worked example at line 228 is smooth ("A 60-person construction-industry software company..."). The transition from worked example to The Practical Shortcut at line 246 is the abrupt one — the worked example ends on Ch18 forward-pointer, then the next section opens with "If the five filters feel like too much evaluation..." This works but is the seam most visible to a careful reader.
  D8 Closing momentum: 8 (=) — "What You Have Earned" closing preserved. Bridge to Part II preserved. Both still effective.

DOMAIN AVERAGE: 7.38 / 10  (Round 1: 7.13 / 10 — Δ +0.25)

BLOCKING ISSUES:
  None.

CONDITIONS:
  C10 (carry forward, P2): Four-item list at line 14 still breaks triadic cadence. Voice-pass.
  C11 (new, P2): The worked-example-to-Practical-Shortcut transition at line 246 could use one bridging sentence. "The worked example shows the full filter walk; for projects in early discovery, three questions cover the common case." Optional.
  C12 (new, P2): Reading economy at +42% words. The compliance-posture table earns its space; the operational-capability sub-section in F5 may have 50–100 compressible words. Voice-pass.

COMMENDATIONS:
  ✓ The chapter's argumentative arc — opening question → five filters → three zones → worked example → shortcut → close — is now structurally complete. Round 1 had the spine; Round 2 has the demonstrating example, which is what an Outside Observer needs to feel the framework lands.
  ✓ The compliance-posture table is the right kind of artifact for a Part I chapter — concrete, scannable, and useful without requiring the reader to leave the page.
  ✓ The "Local-first does not skip compliance; it shifts where compliance burden sits" sentence at line 226 is the new strongest single sentence in the chapter (Round 1's strongest was the opening question, which is preserved). It is honest in a way that most marketing materials are not.

VERDICT: PROCEED WITH CONDITIONS
The Outside Observer's Round 1 PROCEED-WITH-CONDITIONS converts to a stronger PROCEED-WITH-CONDITIONS in Round 2. The chapter reads as a more complete decision tool than in Round 1 without losing the opening force. Reading economy is the only modest concern; voice-pass can address.

---

## COUNCIL TALLY

| Member | Round 1 Avg | Round 2 Avg | Δ | Round 1 Verdict | Round 2 Verdict |
|--------|-----------|-----------|---|---|---|
| Theorist | 5.5 | 7.38 | +1.88 | PROCEED WITH CONDITIONS | PROCEED WITH CONDITIONS |
| Production Operator | 4.75 | 7.0 | +2.25 | REVISE | PROCEED WITH CONDITIONS |
| Skeptical Implementer | 6.25 | 7.38 | +1.13 | REVISE | PROCEED WITH CONDITIONS |
| Pedantic Lawyer | 5.25 | 6.75 | +1.50 | REVISE | PROCEED WITH CONDITIONS |
| Outside Observer | 7.13 | 7.38 | +0.25 | PROCEED WITH CONDITIONS | PROCEED WITH CONDITIONS |
| **Overall** | **5.78** | **7.18** | **+1.40** | **REVISE** | **PROCEED WITH CONDITIONS** |

Council verdict gates applied:
- 5 of 5 members at PROCEED WITH CONDITIONS.
- 0 REVISE verdicts.
- 0 BLOCK verdicts.
- 0 blocking issues raised at any per-member level.
- Domain average 7.18 clears the 6.0 PROCEED-WITH-CONDITIONS threshold by +1.18.
- Per-member minimum is 6.75 (Pedantic Lawyer); all members ≥ user's expected ≥7.0 except the Lawyer who lands at 6.75 — a +1.50 improvement and acceptable for a chapter where the legal axis is partially deferred to Appendix F and Ch15.
- **Council status: PROCEED WITH CONDITIONS.** All three Round 1 REVISE verdicts cleared.

---

## CONSOLIDATED ROUND 2 ACTION ITEMS

### Blocking Issues (resolve before next round)
None. All five Round 1 P0 issues resolved.

### Conditions (P1 — material to chapter quality)
| # | Raised By | Condition |
|---|-----------|-----------|
| C3 | Production Operator | Tighten the supply-chain signing milestone language at line 154: replace "early releases" with a named milestone (e.g., "before the first non-design-partner customer's procurement review"). |

### Conditions (P2 — voice-pass / copyedit / appendix-finalization)
| # | Raised By | Condition |
|---|-----------|-----------|
| C1 | Theorist | Inline-cite the per-project lease claim in the worked example at line 232. |
| C2 | Theorist | Optionally add a flowchart annotation or Q-node split for the mixed-ownership case routed to Zone C. |
| C4 | Production Operator | Per-seat operational cost model — defer to Ch17 / Ch21. |
| C5 | Skeptical Implementer | Reading economy: compress F5 operational-capability sub-section by 50–100 words. |
| C6 | Skeptical Implementer | P1-3 / P1-4 column-mixing in Filter 3 and Filter 4 tables — copyedit-stage. |
| C7 | Pedantic Lawyer | Cite specific DIFC DPL article number when Appendix F is finalized. |
| C8 | Pedantic Lawyer | Inline references to Appendix F should give section numbers. |
| C9 | Pedantic Lawyer | Split the dense HIPAA sentence at line 68 into two sentences for readability. |
| C10 | Outside Observer | Four-item list at line 14 — cut to triadic cadence. |
| C11 | Outside Observer | Add a bridging sentence between the worked example (line 242) and The Practical Shortcut (line 246). |
| C12 | Outside Observer | Reading economy: voice-pass the F5 operational-capability sub-section for compression. |

### Commendations (carry forward)
- Filter-ordering precedence chain at line 28 (Theorist) — converts the funnel from vibes-ordering into a deterministic decision procedure.
- Spectrum acknowledgment at line 164 (Theorist, Outside Observer) — preserves taxonomy utility while disclaiming partition claim.
- F5 operational-capability sub-section at lines 148–158 (Production Operator) — names what Part IV will cover and forward-points cleanly.
- Zone A operational picture at line 198 (Production Operator) — mirrors the F4 relay-failure paragraph, internally consistent.
- "Ships software that fails customer 1" closing line at 158 (Production Operator) — operationally specific failure-mode framing.
- Worked example at lines 228–242 (Skeptical Implementer) — converts framework from theory to runnable procedure with sample output.
- Zone B small-team-fast-ship case at line 202 (Skeptical Implementer) — honest framework discipline; rules out the over-engineered case.
- Compliance-posture table at lines 218–224 (Pedantic Lawyer) — fifteen cells of regulatory framing a general counsel can use directly.
- "Local-first does not skip compliance; it shifts where compliance burden sits" at line 226 (Pedantic Lawyer, Outside Observer) — the new strongest single sentence in the chapter.
- EU-US DPF hedge at line 95 (Pedantic Lawyer) — appropriately cautious for a 2026 publication on a framework in active legal review.
- Opening question at line 12 (Outside Observer) — preserved unchanged.
- Honest-limit at line 204 (Skeptical Implementer) — preserved unchanged.
- "What You Have Earned" closing register (Outside Observer) — preserved unchanged.

---

## ROUND 2 VERDICT: PROCEED WITH CONDITIONS

All five Round 1 P0 blocking issues resolved. All three Round 1 REVISE verdicts cleared. Council average rose from 5.78 to 7.18 (+1.40). Per-member improvements range from +0.25 (Outside Observer, who was already strongest in Round 1) to +2.25 (Production Operator, who had the largest gap to close).

The chapter now functions as a complete decision framework: it presents the question, the filters with explicit precedence, the three zones with the spectrum disclaimer, a compliance-posture table that lets a general counsel use the framework, an operational-capability sub-section that lets an SRE evaluate readiness, a worked example that demonstrates the framework producing a Zone verdict, and a shortcut for early-discovery cases. The closing momentum — Anchor and Bridge as next-Monday actions, Part II as the next read — is preserved.

The remaining conditions are predominantly P2 (voice-pass / copyedit / appendix-finalization). The single P1 carry-forward (C3 — milestone naming for supply-chain signing) is one sentence. None of these block PROCEED WITH CONDITIONS, and none requires another council review round — they can be folded into the prose-review pass and verified by the prose-reviewer agent.

**Recommendation:** Promote the chapter to `icm/voice-check` (Stage 6). Address C3 in the next prose-review iteration. Address P2 conditions during voice-pass and copyedit. Appendix F section-numbering conditions (C7, C8) can be addressed when Appendix F is finalized; flag in the chapter's GitHub issue.

**No Round 3 council review required.** The chapter is council-cleared.
