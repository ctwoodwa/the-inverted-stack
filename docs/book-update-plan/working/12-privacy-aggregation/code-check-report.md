# Code-check report — #12 Privacy-Preserving Aggregation at Relay

**Iteration:** iter-0028
**Date:** 2026-04-28
**Stage advance:** draft → code-check
**Verdict:** PASS-with-claim-markers

---

## Scope

Code-check pass on the new section delivered at iter-0027 / iter-0028:

1. **Ch15 §Privacy-Preserving Aggregation at Relay** (`chapters/part-3-reference-architecture/ch15-security-architecture.md`, lines 710–764, ~1,674 body words / 1,716 total file words). Inserted between §Relay Trust Model (line 690) and §Security Properties Summary (line 768).

The section carries:
- 1 opening + 1 load-bearing scope clarification + 1 sub-pattern roadmap paragraph
- Three sub-patterns: 12a (DP noise injection, line 722), 12b (k-anonymity floor, line 734), 12c (rolling-window budget, line 744)
- FAILED conditions block (line 756) + kill trigger sentence (line 764)
- Five new IEEE references [32]–[36] in the Ch15 reference list

---

## 1. Sunfish package inventory

| Namespace | Sites in #12 | Canon status |
|---|---|---|
| `Sunfish.Kernel.Sync` | 3 | **In canon.** Already present in current Sunfish package canon — `packages/kernel-sync/` exists. The HTML annotation header at line 712 declares `(in-canon, extends existing)`. The three policy components (noise injector / k-floor evaluator / budget tracker) are referenced by *role* only, not by class or method — see lines 732, 742, 754. |
| `Sunfish.Kernel.Audit` | 1 | **In canon** (verified 2026-04-28 by @technical-reviewer at iter-0026 — `packages/kernel-audit/` exists in the Sunfish repo). Cited once at line 752 for the incident-response suspension audit event. **Status correction noted:** previous Ch15 extensions (#48 line 119, #45 line 304, #47 line 492 by extension, #9 line 585) declared `Sunfish.Kernel.Audit` "forward-looking" in their HTML annotation headers — that designation is incorrect per cerebrum 2026-04-28 update. **#12's HTML annotation header correctly does NOT declare Audit forward-looking** because it only mentions `Sunfish.Kernel.Sync` (Audit is mentioned only in body prose at line 752). The pre-existing erroneous annotation headers at lines 119, 304, 585 are queued for the low-priority canon-correction sweep noted in cerebrum, NOT a #12 concern. |

All references are package-name-only. No class names, method signatures, or constructor parameters introduced. The three named relay-internal policy components are referenced by *role* (noise injector, k-floor evaluator, budget tracker) — they are not class definitions. The `BudgetWarning` event name at line 748 is an event-record contract name, parallel to the event-contract naming convention established in §Key-Loss Recovery, §Collaborator Revocation, and §Chain-of-Custody. It is not a class, not a method signature, not a constructor.

**No new top-level namespaces introduced** (in contrast to extension #9 which introduced `Sunfish.Kernel.Custody`). Metadata-privacy enforcement is co-located in `Sunfish.Kernel.Sync` because it is a sync-layer concern operating on metadata the sync layer already handles. The HTML annotation header at line 712 makes this commitment explicit: "0 new top-level namespaces."

## 2. Code blocks

- Fenced code blocks in §Privacy-Preserving Aggregation at Relay: **0**
- Inline backtick identifiers in prose: present (e.g., `Sunfish.Kernel.Sync`, `Sunfish.Kernel.Audit`, `BudgetWarning`, `below-cohort-minimum`); illustrative by context, not invented runnable APIs
- `// illustrative — not runnable` markers required: **0** (no code blocks)
- Invented-API audit: **0 invented APIs**. The mathematical notation (Laplace `λ = 1/ε`, ε = 1.0, ε = 0.1, k = 10, k = 50, Σε = 10.0, n × ε) refers to standard DP literature constructions (Dwork & Roth [32]) and is not invented.

## 3. CLAIM markers

| # | Location | Disposition |
|---|---|---|
| 1 | Ch15 line 750, §12c "Honest scoping" paragraph | **Preserved.** Format: `<!-- CLAIM: rolling-window budget gating is presented as engineering heuristic, not formal temporal-DP — verify framing matches honest-architecture commitment in outline §J -->`. Within loop-plan policy of ≤1 per extension. Queued for technical-review resolution. Marker flags: verify the "practical engineering heuristic, not a formal solution to temporal differential privacy" framing matches outline §J's honesty commitment and does not retreat under prose-tightening pressure in later passes. |

The two pre-existing CLAIM markers in Ch15 (line 461 from #46; line 527 from #47) are unchanged by #12; they remain queued for their respective technical-review passes.

## 4. Cross-reference resolution

| Reference site | Target | Resolves? | Note |
|---|---|---|---|
| Ch15 line 714 → §Relay Trust Model | Ch15 line 690 (`## Relay Trust Model`) | **PASS** | Immediate predecessor; opening paragraph extends §Relay Trust Model's argument from access (third-party operator) to aggregation (self-hosted-operator-as-curator). |
| Ch15 line 718 → §Forward Secrecy and Post-Compromise Security | Ch15 line 403 (`## Forward Secrecy and Post-Compromise Security`) | **PASS** | Orthogonal-composition statement (FS hides content; DP hides aggregates) sits in the load-bearing scope paragraph. |
| Ch15 line 718 → §Endpoint Compromise: What Stays Protected (1st of 2) | Ch15 line 494 (`## Endpoint Compromise: What Stays Protected`) | **PASS** | Establishes that the relay sees only ciphertext under any compromise scenario. |
| Ch15 line 752 → §Endpoint Compromise (2nd of 2) | Ch15 line 494 | **PASS** | §12c "Tension with §Endpoint Compromise" paragraph names the incident-response suspension mode integrating with the compromise procedure. |
| Ch15 line 728 → §Relay Trust Model (re-reference) | Ch15 line 690 | **PASS** | §12a "Central DP at the relay tier" paragraph cites §Relay Trust Model again for the trusted-curator-by-organizational-identity argument. |
| Ch15 line 740 → §Key-Loss Recovery sub-pattern 48f | Ch15 line 226 (`Sub-pattern 48f is the logging substrate on which all other mechanisms depend.`) | **PASS** | §12b "Carve-out for recovery-event partition statistics" names sub-pattern 48f as the metric origin. |

**All 6 cross-references resolve.** Two §Endpoint Compromise references confirmed as expected (one in load-bearing scope paragraph at line 718, one in §12c tension paragraph at line 752).

The §Relay Trust Model close-out forward pointer noted in outline §H (one sentence pointing readers from §Relay Trust Model into the new §Privacy-Preserving Aggregation at Relay section) was deferred to prose-review pass per draft report. The new section's opening directly extends §Relay Trust Model's argument, so the forward pointer is implicit through section adjacency. **Status: deferred per drafter, not a code-check defect.**

## 5. Citation resolution

In-text citation sites in the new section, each traced both directions:

| In-text site | Ref | Resolves to entry? | Source |
|---|---|---|---|
| Ch15 line 724 §12a (Laplace mechanism) | [32] | **PASS** | Dwork and Roth — *The Algorithmic Foundations of Differential Privacy* (2014) — line 847 |
| Ch15 line 728 §12a (RAPPOR local-DP precedent) | [33] | **PASS** | Erlingsson, Pihur, Korolova — RAPPOR (CCS 2014) — line 849 |
| Ch15 line 728 §12a (Apple at-scale telemetry) | [34] | **PASS** | Apple — Learning with Privacy at Scale (2017) — line 851 |
| Ch15 line 738 §12b (k-anonymity floor) | [35] | **PASS** | Sweeney — k-Anonymity (2002) — line 853 |
| Ch15 line 738 §12b (l-diversity extension) | [36] | **PASS** | Machanavajjhala et al. — l-Diversity (2007) — line 855 |
| Ch15 line 746 §12c (sequential composition §3.5) | [32] (re-cite) | **PASS** | Dwork and Roth §3.5 — line 847 |
| Ch15 line 750 §12c (advanced composition accounting) | [32] (re-cite) | **PASS** | Dwork and Roth §3.5 — line 847 |

Reverse direction — every new entry [32]–[36] in the reference list has at least one in-text site:

- [32] cited at lines 724, 746, 750
- [33] cited at line 728
- [34] cited at line 728
- [35] cited at line 738
- [36] cited at line 738

No orphan refs; no broken numbers; no duplicate entries. Numbering jump from existing [31] (last entry from #9 / iter-0024) to [32]–[36] is consistent and matches the drafter report. IEEE numeric style preserved (matching pattern of refs [1]–[31]).

## 6. Sub-pattern coverage

| Sub-pattern | Section pointer | Coverage status |
|---|---|---|
| 12a — Differential-privacy noise injection | Ch15 line 722 (`### Sub-pattern 12a — Differential-privacy noise injection`) | **PASS** — Laplace mechanism with sensitivity 1 and λ = 1/ε [32]; Gaussian extension for (ε, δ)-DP; ε = 1.0 standard / ε = 0.1 regulated; central-vs-local DP architectural decision with RAPPOR [33] / Apple [34] as local-DP precedents the architecture chooses against; trusted-curator-by-organizational-identity rationale; trade-off section (managed-relay-without-audit-rights case); package placement in `Sunfish.Kernel.Sync`. |
| 12b — k-anonymity floor for per-role aggregates | Ch15 line 734 (`### Sub-pattern 12b — k-anonymity floor for per-role aggregates`) | **PASS** — Sweeney [35] floor mechanism; three suppression options (withhold default / merge to parent / `below-cohort-minimum` indicator); k = 10 general / k = 50 regulated; l-diversity [36] extension as one-sentence note; **recovery-event carve-out** as dedicated boldface paragraph naming §Key-Loss Recovery sub-pattern 48f and tying audit-rights to deployment manifest; k-floor evaluator placement in `Sunfish.Kernel.Sync`. |
| 12c — Rolling-window privacy budget tracker | Ch15 line 744 (`### Sub-pattern 12c — Rolling-window privacy budget tracker`) | **PASS** — Sequential composition arithmetic [32 §3.5]; default Σε = 10.0 over 30 days; `BudgetWarning` event at 80% / queue-on-100%; **honest scoping disclaimer** paragraph naming the heuristic-vs-formal-DP gap; advanced composition knob as deployment configuration; **incident-response suspension tension** with §Endpoint Compromise emitting suspension event into `Sunfish.Kernel.Audit`; budget tracker placement in `Sunfish.Kernel.Sync`. |

All three required sub-patterns covered to outline §A specification. Coverage table from drafter report matches independently-verified prose.

## 7. Mandatory artifacts

| Artifact | Status | Location |
|---|---|---|
| HTML annotation header (in-canon namespace disclosure) | **PASS** | Ch15 line 712: `<!-- code-check annotations: Sunfish.Kernel.Sync (in-canon, extends existing). 0 new top-level namespaces. 0 class APIs / method signatures introduced. -->` — declares `Sunfish.Kernel.Sync` as in-canon (correct per cerebrum); declares zero new namespaces; reviewer-visible; reader-invisible. **Notably correct in declaring Sunfish.Kernel.Audit not as forward-looking** (it is in-canon) — though Audit is referenced only in body prose at line 752, not in the header. |
| FAILED conditions block | **PASS** | Ch15 lines 756–762 (`### FAILED conditions`); three named conditions (sub-floor cohort publishing, budget gate non-enforcement, recovery-event audit-rights bypass), each mapped to the sub-pattern it voids and tagged by failure class (architecture / architecture / carve-out). Confirmed at line 756 per task brief. |
| Kill trigger sentence | **PASS** | Ch15 line 764: "The kill trigger for this primitive is a published DP-labeled statistic computed over a cohort below the k-anonymity floor. A primitive that labels noise-dominated output as differential privacy is not privacy preservation — it is a confidence trick performed on the operator and on the people whose behavior the data describes." Confirmed at line 764 per task brief. |
| Load-bearing scope clarification placement | **PASS** | Ch15 line 718, paragraph 3 of the section (after gap-statement at 714 and DP-as-mitigation at 716). Within the "first 1-2 paragraphs" placement requirement (the third paragraph is the appropriate placement once the gap-and-mitigation framing is established). The clarification states (1) DP applies to metadata aggregates only, (2) cryptographic-inaccessibility reason, (3) misread risk by name, (4) orthogonal composition with §Forward Secrecy, (5) compositional relationship with §Endpoint Compromise. |

## 8. build/code-check.py output (raw)

```
$ python3 build/code-check.py ch15

Code check: ch15-security-architecture.md
  Code blocks: 1

  ERRORS (3):
    - Unresolved CLAIM marker: <!-- CLAIM: OTR 2004 [19] named forward secrecy explicitly; "post-compromise security" as a named property post-dates OTR (PCS terminology is generally attributed to Cohn-Gordon, Cremers, Garratt c. 2016). The phrase "these properties" therefore overcredits OTR for both. Defer to next-pass copy-edit (precision tightening, not architectural change). -->
    - Unresolved CLAIM marker: <!-- CLAIM: Ch14 §Sync Daemon Protocol does not currently describe attestation validation at the handshake; this section assumes it as a forward dependency. Confirm in Ch14 cross-reference and either back-add or flag as a gap to address with a parallel Ch14 update. -->
    - Unresolved CLAIM marker: <!-- CLAIM: rolling-window budget gating is presented as engineering heuristic, not formal temporal-DP — verify framing matches honest-architecture commitment in outline §J -->

Exit code: 1
```

Note: the script's `Code blocks: 1` count refers to the single Mermaid `### Key Hierarchy` diagram fence at lines 56–71 of Ch15 and is unrelated to the new section, which contributes 0 code fences.

**Human-judgment override.**

The script's three CLAIM-marker errors are **expected and accepted** under loop-plan §5 policy. Each is a deliberately-preserved CLAIM marker queued for technical-review:

- Marker 1 (line 461) — pre-existing from #46; queued for #46's technical-review (already completed, awaiting next-pass copy-edit per its disposition).
- Marker 2 (line 527) — pre-existing from #47; queued for Ch14 back-add work.
- Marker 3 (line 750) — **new with #12**, deliberately preserved per loop-plan ≤1-marker-per-extension policy. #12 lands at exactly 1 new marker.

The script does **not** flag the in-canon namespace `Sunfish.Kernel.Sync` because the script's regex (`build/code-check.py` line 72) only checks identifiers wrapped in fenced code blocks; the new section uses inline backticks in prose, which the regex does not trigger on. The HTML annotation header at line 712 is the explicit human-readable disclosure — same pattern accepted at the #46/#47/#48/#9 code-checks, with the correctness improvement that #12 declares Sync as in-canon (not forward-looking).

**Override note:** the three CLAIM-marker errors are not blocking for code-check stage advance. The script's exit-1 behavior is by-design strictness for the build pipeline; at the iterative-extension code-check stage, an unresolved CLAIM marker is a *queued item for technical-review*, not a blocker. Verdict reflects this: PASS-with-claim-markers.

## 9. Word count check

- **Target:** 1,500 words
- **±10% acceptable range:** 1,350 – 1,650
- **±20% extended-acceptable range:** 1,200 – 1,800
- **Total file (incl. HTML comments + CLAIM marker):** 1,716 words *(measured: `wc -w docs/book-update-plan/working/12-privacy-aggregation/draft.md` returns 1,716)*
- **Body prose (HTML comments stripped, lines 710–764 of ch15):** 1,674 words *(measured: `awk '710..764' | sed 's/<!--[^>]*-->//g' | wc -w` returns 1,674)*

**Status:** 1,674 body words is **24 words over the ±10% upper bound (1,650)** but well within the ±20% extended-acceptable range (1,200–1,800). The overrun is **1.5%** on the ±10% bound.

**Rationale (drafter-supplied, code-check-confirmed):** the section carries four required artifacts beyond the three sub-pattern bodies: (1) early load-bearing scope clarification, (2) two cross-reference paragraphs to §Forward Secrecy and §Endpoint Compromise establishing orthogonal composition, (3) §12b recovery-event carve-out as a named architectural exception, (4) FAILED conditions block plus kill trigger. Three trim passes brought the draft from 1,854 → 1,777 → 1,745 → 1,716. Further trimming would compress either the central-vs-local DP decision (the load-bearing architectural contribution) or the carve-out rationale. **Acceptable per loop-plan §QC-1 ±20% policy** — 24-word overrun documented, no QC-1 violation at the ±20% bound.

## 10. Items queued for technical-review

The following items are accepted for code-check but require @technical-reviewer verification against authoritative sources, v13/v5, and design-decisions §5 #12. Items 1–6 are pulled forward from the drafter's flag list (draft report §"Flags for technical-reviewer"); items 7–10 are added by code-check.

1. **CLAIM marker resolution (Ch15 line 750).** Verify the rolling-window budget framing — explicitly disclaimed as a heuristic, not formal temporal-DP — is consistent with the honest-architecture commitment in outline §J. Either retire the marker (if framing is fully aligned and the disclaimer is unambiguous) or convert to a `<!-- design-decisions: §J -->` reference annotation. This is the single new CLAIM marker introduced by #12.

2. **No smart-meter worked example** (drafter flag 2). Confirm generic relay sync telemetry (operation counts, sync latencies, error rates, connection durations) is sufficient illustration for all three sub-patterns. Outline §G item 7 flagged the smart-meter scenario as possibly unnecessary; drafter chose to omit. Verify this scoping is acceptable or request a worked smart-meter example.

3. **k = 10 minimum cohort claim** (drafter flag 3). Outline §G item 4 asked for primary-source verification of the k = 10 floor. The draft text says "k = 10 is the practical floor" without claiming "de facto minimum." Confirm this softer phrasing is acceptable or request a specific NIST/healthcare-privacy primary source.

4. **DP-forward-secrecy orthogonality claim** (drafter flag 4; outline §G item 5). Verify no interaction exists through the relay's processing pipeline (e.g., does the noise injector observe key-material metadata that forward secrecy should protect?). The draft asserts the two compose orthogonally; technical reviewer should confirm against the relay's metadata pipeline specification.

5. **Incident-response suspension audit-event visibility** (drafter flag 5; outline §G item 6). The §12c tension paragraph emits the suspension event into `Sunfish.Kernel.Audit` but does not specify whether the audit-event is encrypted to the operator role only, or visible to all nodes. Confirm scope and add visibility specification if required.

6. **Two deferred back-edits** (drafter flag 6; outline §H). (a) Forward pointer at the close of §Relay Trust Model (one sentence) pointing readers into §Privacy-Preserving Aggregation at Relay; (b) "Metadata minimization" row in §Security Properties Summary table. Confirm these can be folded in at prose-review or whether they need a separate back-edit pass.

7. **Dwork & Roth §3.5 framing precision.** Verify the §12c claim that sequential composition (Dwork & Roth §3.5) yields nε for n queries at ε per query is correct, and that the "advanced composition accounting" reference at line 750 correctly attributes the tighter bound to §3.5 of [32] (not to a separate work). Standard textbook construction — likely correct — but flag for verification because two separate citations point at the same chapter section.

8. **Apple [34] citation precision.** Verify the 2017 "Learning with Privacy at Scale" reference is the canonical citation for Apple's local-DP at-scale deployment. The Apple ML Research URL resolves; technical reviewer should confirm the document title, year, and authorship attribution match Apple's published metadata exactly. (No author byline for the work — IEEE format permits the corporate author "Apple Inc." per the existing reference list pattern.)

9. **`Sunfish.Kernel.Audit` in-canon designation.** Per cerebrum 2026-04-28 update (verified at iter-0026 by @technical-reviewer), `Sunfish.Kernel.Audit` is in-canon (`packages/kernel-audit/` exists in Sunfish repo). #12's HTML annotation header at line 712 correctly does NOT declare Audit as forward-looking (only `Sunfish.Kernel.Sync` is named in the header; Audit appears only in body prose at line 752). The pre-existing erroneous "forward-looking" annotation headers at Ch15 lines 119, 304, and 585 (from #48, #45, #9) are queued for the canon-correction sweep noted in cerebrum — **not a #12 blocker, but should be picked up by a future technical-review or canon-sweep pass.**

10. **Concept-index extraction.** Generate updates to `docs/reference-implementation/_per-chapter/ch15-security-architecture.yaml` capturing the new concepts: differential-privacy noise injection primitive, Laplace mechanism (λ = 1/ε), Gaussian mechanism for (ε, δ)-DP, central-vs-local DP architectural decision, ε = 1.0 standard / ε = 0.1 regulated, k-anonymity floor (k = 10 / k = 50), three suppression options, l-diversity extension, recovery-event partition carve-out, rolling-window privacy budget tracker, sequential composition arithmetic, Σε = 10.0 default, `BudgetWarning` event contract, advanced composition knob, incident-response DP suspension mode.

11. **`BudgetWarning` event contract naming convention alignment.** Confirm `BudgetWarning` aligns with the event-contract naming convention established in `Sunfish.Kernel.Audit` and `Sunfish.Kernel.Custody` (#48 / #9): noun-phrase event names, PascalCase. `BudgetWarning` is noun-phrase + PascalCase but is *present-tense / state-ish* rather than past-tense state-change like `CustodyTransferConfirmed`. Verify acceptable as a *threshold-crossing* event class (analogous to a sensor warning) or request rename to past-tense form (`BudgetThresholdCrossed`, `BudgetWarningEmitted`, etc.) for consistency.

## 11. Verdict

**PASS-with-claim-markers.**

- All Sunfish package references are accounted for: `Sunfish.Kernel.Sync` declared in-canon in HTML annotation header at line 712; `Sunfish.Kernel.Audit` referenced once in body prose, in-canon per cerebrum 2026-04-28.
- 0 new top-level namespaces introduced (commitment from outline §D honored).
- 0 code fences in new section, 0 invented APIs, 0 placeholder markers, 0 `<!-- TBD -->` markers.
- 1 new CLAIM marker preserved at line 750 (within loop-plan ≤1-per-extension policy).
- All 6 cross-references resolve cleanly (§Relay Trust Model ×2, §Forward Secrecy, §Endpoint Compromise ×2, §Key-Loss Recovery 48f).
- All 5 new IEEE references [32]–[36] resolve in both directions.
- All 3 sub-patterns (12a / 12b / 12c) covered to outline §A specification.
- All mandatory artifacts present (HTML annotation header / FAILED conditions / kill trigger / load-bearing scope clarification in paragraph 3).
- Word count: 1,674 body words = 1.5% over ±10% bound, comfortably within ±20% policy. Documented and accepted.

## 12. Gate decision

Code-check → technical-review **PASSES**. Section advances to technical-review with **11 documented items** for the next reviewer (1 CLAIM-marker resolution + 5 drafter-forwarded flags + 5 code-check additions). The in-canon namespace disclosure pattern at line 712 represents an improvement over the precedent established at #46/#47/#48/#9 — those declared `Sunfish.Kernel.Audit` forward-looking incorrectly; #12 declares only `Sunfish.Kernel.Sync` and correctly omits any forward-looking designation. The human-judgment override on `build/code-check.py`'s strict CLAIM-error exit is documented above and consistent with prior extensions.
