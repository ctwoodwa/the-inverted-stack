# Technical-review report — #12 Privacy-Preserving Aggregation at Relay

**Iteration:** iter-0030
**Date:** 2026-04-28
**Stage advance:** code-check → technical-review
**Verdict:** PASS (0 CLAIM markers remaining; section advances to prose-review)

---

## Scope

Technical-review pass on the Ch15 §Privacy-Preserving Aggregation at Relay section
(`chapters/part-3-reference-architecture/ch15-security-architecture.md`, original lines 710–764).
Code-check at iter-0029 returned PASS-with-claim-markers with one preserved CLAIM marker at §12c
(line 750) and 11 queued items. This pass addresses all 11 items.

Out-of-scope (sealed): §Forward Secrecy [14]–[19], §Endpoint Compromise [20]–[27],
§Chain-of-Custody [28]–[31], §Relay Trust Model body content (the close-out forward pointer
back-edit IS in-scope per item 6a).

---

## Items resolved with edits

### Item 1 — CLAIM marker at §12c (line 750), retired

**Disposition: RESOLVED. Marker retired.**

The drafted prose at line 750 reads:

> **Honest scoping.** The rolling-window budget is a practical engineering heuristic, not a
> formal solution to temporal differential privacy. Time-series DP composition under temporal
> correlation is an open research problem; the architecture does not claim to solve it. The
> tracker's value is operational: it forces the operator to confront the cumulative budget
> cost at deployment time rather than discover it after the formal guarantee has silently
> collapsed.

This framing fully honors the outline §J commitment: "the section should state that the
rolling-window approach is a reasonable operational heuristic, not a formal temporal-DP
solution... acknowledge the gap rather than claiming a solution the architecture does not
deliver." All four honesty elements are present:

1. Explicit "engineering heuristic, not a formal solution" disclaimer.
2. Named open research problem (temporal correlation).
3. Explicit "the architecture does not claim to solve it" disavowal.
4. Operational-value framing distinct from formal-guarantee framing.

The CLAIM marker has been removed. The honesty-bound prose itself is preserved verbatim
(only the HTML comment marker was stripped).

### Item 3 — k = 10 "practical floor" qualified

**Disposition: RESOLVED with edit.**

The drafter softened "de facto minimum" to "practical floor" but did not qualify the claim
against primary-source scope. Sweeney 2002 [35] does not prescribe a specific k value; HIPAA
Safe Harbor expert-determination practice operates on attribute-specific thresholds in a
broader range (commonly k = 5 to k = 25 by attribute sensitivity). The §12b prose has been
revised to:

> k = 10 is a commonly applied minimum in operational-telemetry deployments and the practical
> floor recommended for this architecture; Sweeney's k-anonymity model [35] does not prescribe
> a specific value, and applied-privacy practice spans a k = 5 to k = 25 range depending on
> attribute sensitivity.

This makes the architecture's choice explicit ("recommended for this architecture") without
falsely attributing the floor to a primary source.

### Item 5 — Suspension audit-event visibility scope specified

**Disposition: RESOLVED with edit.**

The §12c "Tension with §Endpoint Compromise" paragraph emitted the suspension event into
`Sunfish.Kernel.Audit` without specifying visibility scope. Drafter flagged this as
unspecified. The correct scope is operator-only, because broadcasting suspension to all nodes
would itself leak the fact of an unconfirmed incident before the operator has scoped it. The
edit appended:

> The suspension event is encrypted to the operator role only — visible to the operator and
> to auditors holding the operator-role key, not to the broader node fleet — so the
> existence of the suspension does not itself leak the fact of an unconfirmed incident
> before the operator has scoped it.

This aligns with the §Endpoint Compromise procedure (operator-controlled response) and the
§Key-Loss Recovery 48f audit-event visibility model (encrypted application-data log; visible
to the role that holds the audit-role key).

### Item 6a — Forward pointer at §Relay Trust Model close

**Disposition: RESOLVED with edit.**

§Relay Trust Model previously closed with the "Traffic analysis resistance" paragraph
(limitation statement). One sentence was added at the close pointing forward to the new
section:

> For operators who legitimately derive aggregate statistics from relay traffic — error
> rates, sync latencies, fleet health counts — §Privacy-Preserving Aggregation at Relay
> specifies the differential-privacy and k-anonymity mechanisms that satisfy the same
> metadata-protection intent as a self-hosted relay while still enabling operational
> intelligence.

This converts the §Relay Trust Model close from a pure-limitation statement into a
forward-pointer that names the analytics-not-surveillance solution.

### Item 6b — Metadata-minimization row in §Security Properties Summary

**Disposition: RESOLVED with edit.**

The §Security Properties Summary table previously listed four properties (Confidentiality,
Integrity, Availability, Non-repudiation). One row added:

> | **Metadata minimization** | Relay-side aggregate statistics satisfy (ε, δ)-differential
> privacy with a k-anonymity floor; per-partition aggregates below floor are suppressed;
> cumulative ε is gated against a rolling-window budget so individual-node behavior is not
> recoverable from published telemetry. | Central differential privacy at the relay tier,
> k-anonymity floor evaluator, and rolling-window budget tracker — all relay-internal policy
> components within `Sunfish.Kernel.Sync`; suspension-event audit trail in
> `Sunfish.Kernel.Audit`. |

The summary now incorporates the new guarantee without requiring a retroactive edit pass.

### Item 8 — Apple [34] citation precision

**Disposition: RESOLVED with edit.**

The reference was tightened from corporate author + generic venue to:

> [34] Apple Inc. Differential Privacy Team, "Learning with Privacy at Scale," *Apple Machine
> Learning Journal*, vol. 1, no. 8, Dec. 2017.

The Differential Privacy Team author attribution and the *Apple Machine Learning Journal*
volume/issue/date metadata match the document's published metadata. URL is unchanged.

### Item 11 — `BudgetWarning` event-contract naming

**Disposition: RESOLVED with edit.**

`BudgetWarning` was renamed to `BudgetWarningRaised` to align with the PascalCase past-tense
event-contract convention established in §Key-Loss Recovery (`RecoveryClaimSubmitted`,
`RecoveryCompleted`) and §Chain-of-Custody (`CustodyTransferInitiated`,
`CustodyTransferConfirmed`). `Raised` matches the threshold-crossing semantic
(an alarm is *raised*, not "warned").

---

## Items verified without edits

### Item 2 — Smart-meter worked example

**Disposition: GENERIC FRAMING SUFFICES. No edit.**

Outline §G item 7 flagged the smart-meter scenario as possibly a clearer worked example than
generic relay sync telemetry. After review: the generic framing (operation counts, sync
latencies, error codes, connection-duration histograms) covers all three sub-patterns
end-to-end and stays grounded in the architecture's actual deployment context (relay
forwarding CRDT operations between nodes). A smart-meter worked example would shift focus to
an industrial scenario the architecture does not otherwise discuss; this would buy
illustrative concreteness at the cost of architectural relevance. The arxiv 2311.04544
reference cited in outline §E is acknowledged in §J's novelty discussion as the practitioner
literature pointing at the temporal-correlation gap, which is sufficient. **No worked example
added.**

### Item 4 — DP / forward-secrecy orthogonality

**Disposition: VERIFIED. No edit.**

§Forward Secrecy specifies per-message ephemeral keys derived via X25519 + HKDF-SHA256, with
ratchet state owned by `Sunfish.Kernel.Sync` (session establishment) and `Sunfish.Kernel.
Security` (HKDF derivation + per-message zeroing). Ratchet keys never leave endpoints and
are zeroed after use.

The DP noise injector at the relay operates exclusively on observed plaintext metadata
(packet headers, session timings, connection-graph edges, error codes). It has no view into
ratchet state, no key-material-derived inputs, and no shared budget or accounting with the
forward-secrecy ratchet. The two mechanisms compose orthogonally — neither shares state with
the other, neither weakens the other, neither alone closes the other's gap.

The §12a orthogonality statement is technically accurate as drafted.

### Item 7 — Dwork & Roth §3.5 sequential vs advanced composition

**Disposition: VERIFIED. No edit.**

The Dwork & Roth monograph §3.5 covers both basic sequential composition (Theorem 3.16:
k applications of ε-DP yield kε-DP, additive) and advanced composition (Theorem 3.20,
attributed to Dwork-Rothblum-Vadhan FOCS 2010, giving roughly √(2k ln(1/δ'))·ε + kε(e^ε - 1)
bounds — the sqrt-N savings under (ε, δ)-DP composition).

The drafted §12c distinguishes them correctly:

- **Sequential** at line 746: "Sequential composition is additive — n queries at ε per query
  consume nε of cumulative budget (Dwork and Roth [32], §3.5)." Correct attribution to the
  basic theorem.
- **Advanced** at line 750 (revised): "Deployments requiring tighter bounds adopt advanced
  composition accounting (Dwork and Roth [32], §3.5) — the relay exposes simple-versus-
  advanced composition as a configuration knob." Correct attribution; §3.5 covers both, so
  the citation is precise.

The two citations to the same chapter section are deliberate (both theorems live there) and
the prose distinguishes them by function. Framing is correct.

### Item 9 — `Sunfish.Kernel.Audit` canon-correction sweep

**Disposition: NOT A #12 BLOCKER. Documented as queued.**

Per cerebrum 2026-04-28 (line 39), `Sunfish.Kernel.Audit` is in canon (`packages/kernel-audit/`
exists in the Sunfish repo). Earlier extensions (#48 line 119, #45 line 304, #47 by
extension, #9 line 585) declared `Sunfish.Kernel.Audit` "forward-looking" in their HTML
annotation headers — that designation is incorrect. #12's HTML annotation header at line 712
correctly does NOT declare Audit as forward-looking (it only mentions `Sunfish.Kernel.Sync`;
Audit appears in body prose at line 752 only).

The pre-existing erroneous "forward-looking" annotation headers at Ch15 lines 119, 304, 585
are queued for the canon-correction sweep (separate task #25 per loop tracker). **Not a #12
blocker.** This technical-review pass does not modify those headers.

### Item 10 — Concept-index extraction

**Disposition: DEFERRED to next concept-index iteration. Documented here.**

The following terms should be added to
`docs/reference-implementation/_per-chapter/ch15-security-architecture.yaml` at the next
concept-index iteration:

- ε-differential privacy (ε-DP)
- (ε, δ)-differential privacy
- Laplace mechanism (λ = 1/ε for sensitivity-1 counting queries)
- Gaussian mechanism (for (ε, δ)-DP)
- central differential privacy at the relay tier
- local differential privacy (RAPPOR / Apple comparison)
- privacy budget (Σε)
- rolling-window privacy budget tracker
- sequential composition (Dwork-Roth Theorem 3.16)
- advanced composition (Dwork-Rothblum-Vadhan; Dwork-Roth Theorem 3.20)
- k-anonymity floor
- l-diversity extension
- recovery-event partition carve-out
- below-cohort-minimum suppression indicator
- BudgetWarningRaised event contract
- incident-response DP suspension mode
- trusted curator (organizational-identity satisfaction)

The yaml is not edited in this pass; the list is captured for the next concept-index sweep.

---

## Sunfish package verification

| Reference | Sites | Canon status | Verification |
|---|---|---|---|
| `Sunfish.Kernel.Sync` | 4 sites in section body + 1 in HTML annotation header + 1 in new Security Properties Summary row | **In canon** | Confirmed against cerebrum.md Sunfish-package canon |
| `Sunfish.Kernel.Audit` | 1 site in §12c body + 1 in new Security Properties Summary row | **In canon** (verified 2026-04-28 by @technical-reviewer at iter-0026) | Confirmed against cerebrum.md line 39 |

No invented APIs. No class names, method signatures, or constructor parameters. All
illustrative components referenced by role only (noise injector, k-floor evaluator, budget
tracker). Event-contract names (`BudgetWarningRaised`) align with established §Key-Loss
Recovery and §Chain-of-Custody PascalCase past-tense conventions.

**0 new top-level namespaces introduced.** Commitment from outline §D honored.

---

## Citations [32]–[36] verification

| Ref | Title | Year | Venue | Verified |
|---|---|---|---|---|
| [32] Dwork & Roth | The Algorithmic Foundations of Differential Privacy | 2014 | Foundations and Trends in TCS, vol. 9, nos. 3-4 | Title, year, venue match. §3.5 contains both basic (Theorem 3.16) and advanced (Theorem 3.20) composition |
| [33] Erlingsson, Pihur, Korolova | RAPPOR: Randomized Aggregatable Privacy-Preserving Ordinal Response | 2014 | ACM CCS 2014, Scottsdale, AZ | Title, authors, venue, year match |
| [34] Apple DP Team | Learning with Privacy at Scale | 2017 | Apple Machine Learning Journal, vol. 1, no. 8 | Citation tightened in this pass (corporate author refined to include "Differential Privacy Team"; venue tightened to journal vol/issue/date) |
| [35] Sweeney | k-Anonymity: A Model for Protecting Privacy | 2002 | IJUFKS 10(5), 557-570 | Title, year, venue match. Note: Sweeney does NOT prescribe a specific k value; this is correctly reflected in the revised §12b prose |
| [36] Machanavajjhala et al. | l-Diversity: Privacy Beyond k-Anonymity | 2007 | ACM TKDD 1(1) | Title, authors, venue match |

All five citations resolve in both directions (every in-text site has an entry; every entry
has at least one in-text site).

---

## Word count after edits

The technical-review pass added approximately:

- Item 3 (k-floor qualification): +35 words
- Item 5 (suspension visibility): +50 words
- Item 6a (Relay Trust Model forward pointer): +44 words
- Item 6b (Security Properties Summary row): +52 words

Total added: ~181 words. Items 6a and 6b land outside the §Privacy-Preserving Aggregation
section proper (one in §Relay Trust Model, one in §Security Properties Summary). Within the
§Privacy-Preserving Aggregation section itself: ~85 words added (items 3 and 5).

Body prose for §Privacy-Preserving Aggregation: previously 1,674 words; now approximately
1,759 words. Still within ±20% extended-acceptable range (1,200–1,800). At the upper edge of
the extended range; further additions would force a trim pass. **Acceptable per loop-plan
§QC-1.**

---

## Anti-AI tells / style spot-check

This is technical-review scope, not prose-review scope, but two flags noted for prose-review
to address:

- The new metadata-minimization summary row uses long em-dash phrasings that may exceed the
  stylistic budget for the table; prose-reviewer should evaluate whether the row body parses
  cleanly at table-cell width.
- Item 5's suspension-visibility addition uses a long em-dash phrase ("visible to the
  operator and to auditors holding the operator-role key, not to the broader node fleet").
  Acceptable architecturally; prose-reviewer should check it against the style guide's
  em-dash budget.

These are noted for the prose-review pass; they are not technical-review defects.

---

## Verdict

**PASS.**

- 1 pre-existing CLAIM marker (line 750) **resolved and retired** with no edit to the
  load-bearing honesty-bound prose. The marker was a process artifact; the prose itself
  satisfies outline §J's commitment fully.
- 0 new CLAIM markers introduced.
- 0 invented Sunfish APIs. All package references in canon.
- 0 placeholder text, 0 TBD markers, 0 broken cross-references.
- Citations [32]–[36] verified against primary-source metadata; one citation tightened ([34]).
- All 11 code-check items addressed: 7 resolved with edits, 3 verified without edits, 1
  deferred (concept-index yaml — separate task).
- Two outline-§H back-edits folded in (Relay Trust Model forward pointer; Security
  Properties Summary row).

**0 CLAIM markers remaining in the §Privacy-Preserving Aggregation section.** Verdict bar
(≤1 marker) achieved with margin.

---

## Gate decision

**Technical-review → prose-review PASSES.**

Section advances to prose-review. Items for prose-reviewer attention:

1. Em-dash budget check on the new Security Properties Summary metadata-minimization row.
2. Em-dash budget check on the §12c suspension-visibility addition.
3. General readability pass on §12b after the k-floor qualification edit (one new sentence
   inserted into a tight paragraph; verify cadence).
4. General readability pass on §Relay Trust Model close (one forward-pointer sentence
   appended to a previously-closed section).

The technical-review pass does NOT modify the §Forward Secrecy [14]–[19], §Endpoint
Compromise [20]–[27], or §Chain-of-Custody [28]–[31] sections — they remain sealed per the
review scope. The §Relay Trust Model close-out forward pointer (one sentence) and the
§Security Properties Summary metadata-minimization row (one row) are the only out-of-section
edits, both explicitly in scope per the queued items 6a and 6b.

Pre-existing CLAIM markers at lines 461 (#46) and 527 (#47) are unchanged and remain queued
for their respective extension passes. They are not within #12's review scope.
