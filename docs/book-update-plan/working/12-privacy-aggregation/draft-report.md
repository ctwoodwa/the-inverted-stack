# Draft report — #12 Privacy-Preserving Aggregation at Relay

**Iteration:** iter-0027
**Stage:** draft → ready for code-check
**Target:** Ch15 §Privacy-Preserving Aggregation at Relay (inserted between §Relay Trust Model and §Security Properties Summary)
**Outline:** `docs/book-update-plan/working/12-privacy-aggregation/outline.md` (~700 words structural spec)
**Standalone draft:** `docs/book-update-plan/working/12-privacy-aggregation/draft.md`

---

## Word count

- **Total file (incl. HTML comments and CLAIM marker):** 1,716 words
- **Body prose (comments stripped):** 1,674 words
- **Target:** 1,500 words
- **±10% acceptable range:** 1,350 – 1,650
- **±20% extended-acceptable range:** 1,200 – 1,800

**Status:** 1,674 body words is **24 words over the ±10% upper bound** (1,650) but well within the ±20% extended-acceptable range (1,200–1,800).

**Rationale for 24-word overrun:**
The section carries four required artifacts beyond the three sub-pattern bodies: (1) the early load-bearing scope clarification (DP applies to metadata aggregates, not data), (2) two cross-reference paragraphs to §Forward Secrecy and §Endpoint Compromise establishing orthogonal composition, (3) the §12b recovery-event carve-out paragraph (a named architectural exception, not a generic rule), (4) the FAILED conditions block plus kill trigger sentence. Three trim passes brought the draft from 1,854 → 1,777 → 1,745 → 1,716. Further trimming would compress either the central-vs-local DP decision (the load-bearing architectural contribution this book makes) or the carve-out rationale, neither of which can be cut without losing required content. The 1.5% overrun on ±10% is documented and accepted under the ±20% policy.

---

## Sub-pattern coverage

| Sub-pattern | Required content | Coverage in draft |
|---|---|---|
| **12a** central-DP-at-relay | DP noise mechanism (Laplace/Gaussian), ε settings (1.0 standard / 0.1 regulated), central-vs-local DP choice presented as architectural decision (not derived from prior literature), trust-model trade-off, package placement | Full. "Central DP at the relay tier — an architectural decision" subhead presents the choice with explicit reasoning ("the Inverted Stack chooses central DP"). RAPPOR [33] and Apple [34] cited as local-DP precedents the architecture chose against. |
| **12b** k-anonymity floor | k-floor mechanism (Sweeney), suppression options, k=10/k=50 deployment classes, l-diversity extension, recovery-event carve-out | Full. Carve-out is a dedicated boldface paragraph naming §Key-Loss Recovery sub-pattern 48f and tying audit-rights to deployment manifest. |
| **12c** rolling-window budget | Sequential composition arithmetic, Σε allocation, BudgetWarning event, queue-on-exhaustion, **honest scoping disclaimer** (not formal temporal-DP), advanced-composition knob, incident-response suspension tension with #47 | Full. "Honest scoping" boldface paragraph explicitly states the heuristic-vs-formal-DP gap. Incident-response tension cross-references §Endpoint Compromise. |

---

## Citations added (Ch15 reference list)

Added in order to References section after [31]:

- **[32]** Dwork and Roth — *The Algorithmic Foundations of Differential Privacy* (2014). Used in §12a (Laplace mechanism) and §12c (sequential composition §3.5; advanced composition).
- **[33]** Erlingsson, Pihur, Korolova — RAPPOR (CCS 2014). Used in §12a as local-DP precedent.
- **[34]** Apple — Learning with Privacy at Scale (2017). Used in §12a as second local-DP precedent.
- **[35]** Sweeney — k-Anonymity (2002). Used in §12b for the floor definition.
- **[36]** Machanavajjhala et al. — l-Diversity (2007). Used in §12b for the extension model.

All five formatted to match existing Ch15 IEEE numeric style.

---

## Load-bearing clarification placement

Required by task brief: DP applies *only to metadata aggregates the relay computes as a side effect of routing*, not to payload content (which is ciphertext and DP-inaccessible). Conflating "DP on data" with "DP on relay-side metadata" misreads the threat model.

**Placement:** Paragraph 3 of the section opening — directly after the gap-statement paragraph and before the sub-pattern list. This satisfies the "first 1-2 paragraphs" placement requirement. The clarification sits as the third paragraph because the first two paragraphs frame the gap (§Relay Trust Model handled access, not aggregation; DP closes the aggregation gap). The clarification then constrains the scope before the reader encounters any sub-pattern detail.

The clarification paragraph explicitly:
1. States DP applies to metadata aggregates only.
2. Names the cryptographic-inaccessibility reason (relay receives ciphertext).
3. Calls out the misread risk by name ("Readers who conflate ... misread the threat model").
4. Composes with §Forward Secrecy and Post-Compromise Security (#46) — orthogonal composition stated.
5. Composes with §Endpoint Compromise: What Stays Protected (#47) — relay sees ciphertext under any compromise; even visible metadata is not single-node-granular.

---

## Namespace declaration

**HTML annotation header at section start:**
```
<!-- code-check annotations: Sunfish.Kernel.Sync (in-canon, extends existing). 0 new top-level namespaces. 0 class APIs / method signatures introduced. -->
```

`Sunfish.Kernel.Sync` is already in canon and is the natural home for relay-internal policy components (the relay's routing and session logic lives here per outline §D). The three policy components — noise injector, k-floor evaluator, budget tracker — are referenced by role only ("a relay-internal policy component"), never by class or method signature. `Sunfish.Kernel.Audit` is referenced once for the incident-response suspension event (already in canon from #48). No `Sunfish.Foundation.Privacy` or `Sunfish.Kernel.Privacy` namespace is introduced or implied.

---

## Cross-references (all backward, Part III convention)

| Target | Where used | Purpose |
|---|---|---|
| **§Relay Trust Model** | Opening paragraph 1 | Immediate predecessor; same threat locus, different attack vector (operator analytics vs. third-party). |
| **§Forward Secrecy and Post-Compromise Security** | Load-bearing scope paragraph (paragraph 3) | Orthogonal composition: forward secrecy hides content, DP hides aggregates. Neither weakens the other; neither alone closes the other's gap. |
| **§Endpoint Compromise: What Stays Protected** | Load-bearing scope paragraph (paragraph 3) and §12c incident-response tension | Relay sees only ciphertext under compromise; the metadata it does see is not single-node-granular. §12c tension paragraph names the incident-response suspension mode that integrates with the §Endpoint Compromise procedure. |
| **§Key-Loss Recovery sub-pattern 48f** | §12b recovery-event carve-out paragraph | Names the recovery-event metric defined by 48f as the unusually sensitive statistic that triggers the named carve-out. |

No forward references inserted into prior sections (the §Relay Trust Model close-out forward pointer suggested in outline §H was held back for prose-review pass; the new section's opening directly extends §Relay Trust Model's argument, so the forward pointer is implicit through adjacency).

---

## FAILED conditions and kill trigger

**FAILED block** (matches the §Forward Secrecy and §Chain-of-Custody styles already in Ch15):

1. DP-labeled aggregate published over a sub-floor cohort — architecture failure (privacy theater).
2. Cumulative ε exceeds Σε without the budget gate halting — architecture failure (formal guarantee surrendered).
3. Recovery-event partition statistics published without explicit operator audit rights — carve-out failure.

**Kill trigger** (single sentence per task brief):
> "The kill trigger for this primitive is a published DP-labeled statistic computed over a cohort below the k-anonymity floor. A primitive that labels noise-dominated output as differential privacy is not privacy preservation — it is a confidence trick performed on the operator and on the people whose behavior the data describes."

The kill trigger names the cohort-below-floor scenario as the architectural-invalidation condition. Below the k floor, Laplace noise dominates signal; publishing a DP-labeled number under those conditions is mislabeled output, which falsifies the entire privacy claim chain.

---

## Novelty / honesty notes

**Novelty (claimed in prose):** The central-DP-at-relay decision is presented as an architectural contribution this book makes — explicitly stated as a choice ("The Inverted Stack chooses central DP") with reasoning grounded in §Relay Trust Model's self-hosted-relay prescription. Most local-first architecture literature treats the relay as a routing component without analytics; choosing central over local DP at the relay tier and reasoning from the trusted-curator-by-organizational-identity argument is a design decision the book is contributing, not citing. RAPPOR [33] and Apple [34] are cited as the local-DP precedents the architecture is choosing *against*, not as the source the architecture derives from.

**Honesty boundaries (named in prose):**
1. **Rolling-window budget is not formal temporal-DP** — §12c "Honest scoping" paragraph explicitly states the heuristic nature: "Time-series DP composition under temporal correlation is an open research problem; the architecture does not claim to solve it." This protects against future technical-reviewer pushback that the rolling-window approach overclaims a formal guarantee.
2. **Central DP requires trusted curator** — §12a "trade-off is honest" paragraph names the trust requirement and the managed-relay-without-audit-rights case where central DP is not credible. The architecture exposes the central/local/hybrid choice as deployment-time configuration with no default that can be unearned.
3. **Carve-out is operator-policy, not general rule** — §12b carve-out paragraph explicitly notes "This is an operator-policy decision, not a general suppression rule," preventing readers from generalizing the recovery-event suppression to all sensitive metrics.

---

## CLAIM markers inserted

**One CLAIM marker** (within loop-plan policy of ≤1):

```
<!-- CLAIM: rolling-window budget gating is presented as engineering heuristic, not formal temporal-DP — verify framing matches honest-architecture commitment in outline §J -->
```

**Location:** §12c "Honest scoping" paragraph, immediately after the "practical engineering heuristic, not a formal solution to temporal differential privacy" sentence.

**What it flags for technical-reviewer:** Verify that the prose framing of the rolling-window budget — explicitly disclaimed as a heuristic — is consistent with the honest-architecture commitment laid out in outline §J. Outline §J is explicit that this section should *not* claim a formal temporal-DP solution. The marker exists so the technical reviewer confirms the prose lands the disclaimer with the right register and does not retreat from the honesty commitment under prose-tightening pressure in later passes.

---

## Deviations from outline

**1. Word budget allocation.** The outline §I budgeted 200/600/350/350 across opening / 12a / 12b / 12c. Actual rough allocation (body words, post-trim):
- Opening + load-bearing clarification + section-roadmap: ~400 words (200 over budget — the load-bearing scope paragraph required full development to satisfy the "first 1-2 paragraphs" placement requirement and to compose with #46 + #47 in a single dense paragraph).
- §12a: ~530 words (70 under budget).
- §12b: ~310 words (40 under budget).
- §12c: ~340 words (10 under budget).
- FAILED + kill trigger: ~170 words (not separately budgeted; counts against the section total).

**Net effect:** The opening took more space than budgeted because the load-bearing scope clarification + cross-references to two sibling sections + sub-pattern roadmap had to fit in the first ~400 words. Sub-patterns 12a–12c absorbed the offset.

**2. No worked smart-meter scenario.** Outline §G item 7 noted the smart-meter scenario as design-decisions reference but flagged it as possibly unnecessary if generic relay sync telemetry suffices. The draft uses generic relay sync telemetry (operation counts, sync latencies, error rates, connection durations) and does not introduce a worked smart-meter example. Rationale: the three sub-patterns are fully illustrated by the relay sync telemetry context; introducing a smart-meter scenario would require a new domain framing that the section does not have the word budget to support. Flag for technical-reviewer to confirm this scoping is acceptable.

**3. No explicit sensitivity-analysis table.** Outline §G item 1 noted that DP applies to additive aggregates and asked the technical-reviewer to verify scope. The draft names the relevant aggregates (operation counts, latency bucket counts, error counts, connection-duration histograms) and states sensitivity = 1 explicitly. No tabular breakdown was added; the inline statement satisfies the spec requirement.

**4. l-diversity coverage.** §12b mentions l-diversity (Machanavajjhala et al. [36]) as a one-sentence extension note rather than a sub-pattern. Outline §G item 4 flagged this as adequate.

**5. No forward-pointer back-edits.** Outline §H suggested adding a forward pointer at the close of §Relay Trust Model (one sentence) to point readers from §Relay Trust Model into the new §Privacy-Preserving Aggregation at Relay section. This back-edit was deferred to prose-review pass to avoid scope-creep on the draft stage. The new section's opening directly extends §Relay Trust Model's argument, so the forward pointer is currently implicit through section adjacency.

**6. No Security Properties Summary table row.** Outline §H suggested adding a "Metadata minimization" row to the §Security Properties Summary table. This back-edit was also deferred to prose-review pass. The summary table currently retains its original four rows.

---

## QC items believed to pass

- **QC-1** Word count within ±20% (1,716 with comments / 1,674 body — over ±10% by 24 words; rationale documented).
- **QC-2** All required sub-patterns covered (12a/12b/12c).
- **QC-3** Source sections cited inline (Dwork & Roth [32], RAPPOR [33], Apple [34], Sweeney [35], Machanavajjhala [36]).
- **QC-4** Sunfish packages referenced by name only (`Sunfish.Kernel.Sync`, `Sunfish.Kernel.Audit`); no class APIs or method signatures.
- **QC-5** No academic scaffolding ("this section explores", "as we have seen", etc.).
- **QC-6** No re-introduction of the architecture; assumes Part I + earlier Ch15 sections.
- **QC-7** Part III specification voice (what it is, how it works fully); no tutorial drift.
- **QC-9** Not applicable (Ch15 is Part III, not Part II council chapter).
- **QC-10** No placeholder text.

---

## Flags for technical-reviewer

1. **CLAIM marker** at §12c honest-scoping paragraph — verify rolling-window budget framing matches outline §J honesty commitment.
2. **No smart-meter worked example** — confirm generic relay sync telemetry is sufficient illustration for all three sub-patterns (outline §G item 7).
3. **k=10 minimum cohort claim** — outline §G item 4 asked for primary source verification. The draft text says "k = 10 is the practical floor" without claiming "de facto minimum." Confirm this softer phrasing is acceptable, or request a specific NIST/healthcare-privacy primary source.
4. **DP-forward-secrecy orthogonality claim** — verify no interaction exists through the relay's processing pipeline (e.g., does the noise injector observe key-material metadata that forward secrecy should protect?). Outline §G item 5.
5. **Incident-response suspension audit-event visibility** — outline §G item 6 asked whether the suspension event in `Sunfish.Kernel.Audit` is encrypted to the operator role only, or visible to all nodes. The draft does not specify the audit-event visibility scope; flag for follow-up.
6. **Two deferred back-edits** — forward pointer at §Relay Trust Model close (outline §H) and "Metadata minimization" row in §Security Properties Summary table (outline §H). Confirm these can be folded in at prose-review or whether they need a separate back-edit pass.

---

*Draft complete. Ready for `code-check` stage.*
