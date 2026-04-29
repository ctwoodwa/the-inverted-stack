# Prose-review report — #12 Privacy-Preserving Aggregation at Relay

**Iteration:** prose-review (post iter-0030 technical-review)
**Date:** 2026-04-28
**Stage advance:** technical-review (PASS, 0 CLAIM markers) → prose-review
**Verdict:** PASS

---

## Scope

Ch15 §Privacy-Preserving Aggregation at Relay (lines 710–767) plus two out-of-section
back-edits the technical-review pass folded in:

1. §Relay Trust Model close-out forward-pointer sentence (line 708).
2. §Security Properties Summary metadata-minimization table row (line 780).

Out of scope (sealed): §Forward Secrecy refs [14]–[19]; §Endpoint Compromise refs [20]–[27];
§Chain-of-Custody refs [28]–[31]; §Relay Trust Model body content; refs [1]–[31].

Refs [32]–[36] are in scope but were verified verbatim at technical-review and required no
prose pass.

---

## Edits applied

### Paragraph length (1 edit)

- **§12b k-anonymity-floor paragraph (line 740 pre-edit).** The pre-edit paragraph ran 7
  sentences, exceeding the 6-sentence cap. The technical-review pass inserted the k = 10
  qualification sentence ("k = 10 is a commonly applied minimum…depending on attribute
  sensitivity") into a tight 6-sentence paragraph and pushed it over cap. Split at the
  natural seam: sentences 1–4 stay together as the operational-mechanism paragraph (floor
  definition, suppression options, default policy); sentences 5–7 break out into a new
  parameter-value paragraph (k = 10 architecture floor, k = 50 regulated, l-diversity
  extension). Both halves now sit at 4 and 3 sentences respectively, preserving the
  k-floor-qualification preservation flag and the l-diversity discussion intact.

### Table-row register parallelism (1 edit)

- **§Security Properties Summary metadata-minimization row (line 780).** The new row used
  semicolons to chain three clauses in the Guarantee column and one semicolon plus an em-dash
  in the Mechanism column. Adjacent rows (Confidentiality, Integrity, Availability,
  Non-repudiation) all use period-separated sentences. Converted the new row's semicolons to
  periods so it parses at the same register as the four pre-existing rows. The em-dash is
  preserved (house style retains em-dashes; tech-reviewer's flag noted "may exceed budget"
  but the em-dash here delimits the relay-internal policy-component apposition cleanly).
  Row content is unchanged — only the punctuation register was tightened to match the table.

---

## Edits considered but not applied

### Preservation flags honored

1. **§12c Honest scoping paragraph (line 752).** The "engineering heuristic, not a formal
   solution to temporal differential privacy" disclaimer is preserved verbatim. All four
   honesty elements (heuristic disclaimer, named open research problem, "the architecture
   does not claim to solve it" disavowal, operational-value framing) remain intact. Tech-review
   retired the CLAIM marker on the basis of this prose; softening the framing here would
   reopen the marker. **No edit.**

2. **Paragraph 3 load-bearing scope clarification (line 720).** The "differential privacy
   here applies *only to metadata aggregates the relay computes as a side effect of routing*"
   distinction is preserved. The paragraph is dense (5 sentences, italics on the scope clause,
   two cross-references to §Forward Secrecy and §Endpoint Compromise) — that density is the
   point. Readers who skim this paragraph will misread the threat model; the paragraph's
   weight earns its placement. **No edit.**

3. **Recovery-event carve-out (line 742).** The named-carve-out structure ("with a named
   exception", "operator-policy decision, not a general suppression rule") is preserved. The
   cross-reference to §Key-Loss Recovery sub-pattern 48f stays as the primary scope anchor.
   The 5-sentence paragraph sits at cap; cadence is correct for the architectural-honesty
   register §12 carries throughout. **No edit.**

4. **k = 10 "practical floor for this architecture" qualification (line 740 post-split).**
   Preserved verbatim per tech-review item 3. The phrase "and the practical floor recommended
   for this architecture" qualifies the architecture's choice without falsely attributing a
   specific value to Sweeney 2002. The follow-up clause ("Sweeney's k-anonymity model [35]
   does not prescribe a specific value, and applied-privacy practice spans a k = 5 to k = 25
   range depending on attribute sensitivity") preserves the technical-truth disclaimer.
   **No edit.**

### Not-applied because already on-voice

1. **Line 720 passive "is not retained at single-node granularity."** Could be active ("the
   relay does not retain even the metadata it does see at single-node granularity") but the
   passive here parallels the prior clause "the relay sees only ciphertext under any
   compromise scenario" — the rhetorical pair is "the relay sees X / X is not retained Y"
   and rewording would break the parallel. Pre-existing prose, not new at this iteration.
   **Leave.**

2. **Line 730 passive "the noise is added once."** The clause "Central DP produces lower
   noise for equivalent guarantees because the noise is added once to the aggregate rather
   than once per contributor" is making a contrastive claim where the agent identity is
   incidental to the contrast. Activating ("the relay adds noise once") would shift weight
   onto the relay identity rather than the once-vs-per-contributor count which is the load
   the sentence carries. Pre-existing prose. **Leave.**

3. **Line 734 passive "are declared in the relay configuration manifest."** Mechanism, ε
   value, and aggregate-output schema as a coordinated subject reads more naturally than
   "The relay configuration manifest declares the mechanism, ε value, and aggregate-output
   schema" — the specification voice prefers the artifact-declared form. Pre-existing prose.
   **Leave.**

4. **Line 754 "The suspension event is encrypted to the operator role only" passive.**
   Adjectival passive (descriptive of the encryption boundary, not an active verb on a
   missing agent). Activating would force a new subject ("the relay encrypts the suspension
   event…") that breaks the parallel with the prior sentence "The suspension itself emits a
   signed event into `Sunfish.Kernel.Audit`". The pair "suspension itself emits / suspension
   event is encrypted" reads cleanly as event-attribute description. **Leave.**

5. **§12a "noise" / "Laplace mechanism" / "Gaussian mechanism" / "noise injector" / "central
   differential privacy."** Considered as synonym cycling. Decision: leave. Laplace mechanism
   and Gaussian mechanism are distinct named DP mechanisms — keeping their formal names is
   correct in spec voice. "noise" is the generic noun; "noise injector" names the
   relay-internal policy component; "central differential privacy" names the architectural
   choice. Each name owns a distinct concept; this is the spec's vocabulary, not synonym
   cycling.

6. **§12c "DP noise on these counts may mask the signal."** "may mask" hedge considered.
   Decision: leave. Genuine uncertainty — whether DP noise masks the forensic signal depends
   on the noise scale relative to signal magnitude, which the operator-tunable ε determines.
   The hedge is technically precise, not stylistic softening.

7. **§12c "Tension with §Endpoint Compromise" paragraph long em-dashed sentence.** Tech-review
   flagged this for em-dash budget. House style explicitly preserves em-dashes; the
   parenthetical "— visible to the operator and to auditors holding the operator-role key,
   not to the broader node fleet —" carries the visibility-scope clarification that was
   missing pre-edit. Anti-ai-tells §14 (em-dash) is explicitly NOT applied per house policy.
   **Leave.**

8. **§Sub-pattern 12a / 12b / 12c spec labels.** These are the spec's own intra-section
   sub-pattern labels (cf. §Forward Secrecy uses §46a/§46b labels; §Endpoint Compromise uses
   §47a–§47f; §Key-Loss Recovery uses §48a–§48f). Distinct from the editorial-process
   "#12" extension number (which does not appear in user-facing prose). The §-prefixed
   labels are the spec's vocabulary — preserve.

9. **H2 heading "Privacy-Preserving Aggregation at Relay" Title Case.** Anti-ai-tells §17
   would flag Title Case in headings — but Ch15's H2 convention throughout the chapter is
   Title Case (§Forward Secrecy and Post-Compromise Security, §Endpoint Compromise: What
   Stays Protected, §Security Properties Summary, §Relay Trust Model). Changing one H2 to
   sentence case would break the chapter's established convention. Chapter-level
   normalization is out of scope for this section pass.

10. **§Relay Trust Model close-out forward pointer (line 708).** Read for naturalness and
    active voice. Reads natural: "§Privacy-Preserving Aggregation at Relay specifies the
    differential-privacy and k-anonymity mechanisms…" — active verb (specifies), section as
    subject. Mirrors the cross-reference style used at the end of §Endpoint Compromise (line
    568 forward pointer). One sentence, well-formed, no edit needed.

---

## CLAIM markers preserved

- **0 CLAIM markers in scope.** Tech-review pass retired the §12c marker (line 750 pre-edit).
  No new markers introduced at this prose pass.

---

## Voice-register confirmation

Part III specification voice maintained throughout the section.

- No "you should" / "we recommend" / "consider X" instructions. Statements are "X does Y" /
  "the architecture does Y" / "the primitive's FAILED conditions are Y" / "the relay
  suppresses Z".
- Cross-references resolve to other Part III sections (§Relay Trust Model, §Forward Secrecy
  and Post-Compromise Security, §Endpoint Compromise: What Stays Protected, §Key-Loss
  Recovery sub-pattern 48f). All section names match canonical headings as they appear in
  the chapter.
- Citation refs [32]–[36] all in IEEE-numeric form as established by Appendix E; Dwork &
  Roth [32] cited twice (sequential composition at line 748, advanced composition at line
  752) — same source section §3.5 covers both theorems, so the parallel citation is
  deliberate and correct.
- Sub-pattern labels (§Sub-pattern 12a, §12b, §12c) used consistently in section-body cross
  references; matches the §Forward Secrecy, §Endpoint Compromise, §Key-Loss Recovery
  conventions.

---

## Table-row register check (§Security Properties Summary new row)

Post-edit, the metadata-minimization row parses parallel to the four pre-existing rows:

| Row | Guarantee column structure | Mechanism column structure |
|---|---|---|
| Confidentiality (pre-existing) | 3 sentences, period-separated | 1 sentence, semicolon-separated within |
| Integrity (pre-existing) | 2 sentences, period-separated | 1 sentence, semicolon-separated |
| Availability (pre-existing) | 3 sentences, period-separated | 1 sentence, period-separated |
| Non-repudiation (pre-existing) | 2 sentences, period-separated | 1 sentence |
| **Metadata minimization (new, post-edit)** | 3 sentences, period-separated | 2 sentences, period-separated, em-dash for apposition |

All five rows now use period-separated sentences in the Guarantee column. The new row's
em-dash is the only mid-cell em-dash in the table; it carries the "all relay-internal policy
components within `Sunfish.Kernel.Sync`" apposition that no other row needed (the new
guarantee names three relay-internal policy components, and the apposition collapses them
into a single namespace declaration). Acceptable per house em-dash policy.

---

## Anti-AI tells spot-check

- **§1 significance puffery:** zero matches. No "stands as a testament", "marks a pivotal
  moment", "the evolving landscape", "indelible mark".
- **§3 superficial -ing tail-phrases:** one borderline at line 754 ("preserving the audit
  trail across the suspension period") — substantive consequence (audit-trail continuity is
  load-bearing, not vague consequence-puff). Leave.
- **§7 AI vocabulary cluster:** zero matches. No delve / showcase / tapestry / interplay /
  intricate / pivotal / vibrant / enduring / underscores. The word "intelligence" appears in
  "operational intelligence" — domain term, not the AI-vocabulary "intelligence" of "data
  intelligence platform". OK.
- **§8 copula avoidance:** zero matches. The plain `is`/`are` definitional copulas at lines
  744 and 756 ("The k-floor evaluator is a relay-internal policy component within
  `Sunfish.Kernel.Sync`" / "The budget tracker is the third relay-internal policy component
  within `Sunfish.Kernel.Sync`") are simple definitional `is`, not the puffy
  "serves as a" / "represents a" / "boasts" pattern §8 targets.
- **§9 negative parallelisms:** zero matches.
- **§16 inline-header vertical lists:** none used in the new content. The FAILED conditions
  list is genuine reference content (calibrated correct format per house policy).
- **§17 title case in headings:** H2 Title Case follows the chapter's established convention
  (see voice-register confirmation note above); H3 sub-pattern labels use sentence case after
  the dash, which is consistent.
- **§25 generic positive conclusions:** the section closes on FAILED conditions and the kill
  trigger — specific, terminal, action-bound. No "the future looks bright" puffery.
- **§27 persuasive authority tropes:** zero matches. No "fundamentally", "the real question",
  "at its core", "the deeper issue".
- **§29 fragmented headers:** none. Each H3 ("Sub-pattern 12a/b/c") is followed immediately by
  substance, not by a one-line restatement.

---

## Internal extension-number leaks

Grepped for "#12", "#46", "#47", "#48" in user-facing prose of the §Privacy-Preserving
Aggregation section. **Zero matches.** Sub-pattern labels use the §-prefixed spec form
(§Sub-pattern 12a, §12b, §12c, §Key-Loss Recovery sub-pattern 48f) consistent with §Forward
Secrecy / §Endpoint Compromise / §Key-Loss Recovery conventions. Editorial extension numbers
do not leak into reader-facing prose.

---

## Word count after prose pass

- Body of §Privacy-Preserving Aggregation: 1,759 words → 1,759 words. The §12b paragraph
  split inserts a paragraph break (zero word delta) but no other content change.
- §Relay Trust Model close pointer: unchanged (44 words).
- §Security Properties Summary new row: 65 words → 65 words (semicolons → periods, no word
  delta).

Total prose-pass delta: **0 words.** Edits are punctuation-and-paragraphing; content is
untouched.

---

## Verdict

**PASS.**

- 0 paragraph-cap violations remain (§12b split resolved the only one introduced by the
  tech-review pass).
- 0 CLAIM markers added; pre-existing markers (none in scope) untouched.
- 0 internal extension-number leaks in reader-facing prose.
- 0 invented Sunfish APIs; all references in canon (verified at code-check and
  technical-review).
- All preservation flags honored: §12c Honest scoping paragraph, paragraph-3 scope
  clarification, recovery-event carve-out structure, k = 10 architecture qualification.
- Voice register: Part III specification voice maintained throughout.
- Table-row register: metadata-minimization row now parses parallel to the four pre-existing
  rows.
- §Relay Trust Model close-out forward pointer reads natural and active without further edit.

---

## Gate decision

**Prose-review → voice-check PASSES.**

Section advances to voice-check. The voice-check pass is the human-only step (per CLAUDE.md
Workflow Stage 6) where author adds personal context, field anecdote, and connective tissue.
Items voice-check may consider:

1. The section is densely technical (DP mechanisms, k-anonymity, privacy budget) — author
   may consider whether one operational anecdote (e.g., a fleet-health-dashboard story
   illustrating the k = 10 floor in action) would humanize §12b without breaking spec voice.
   Optional, not required.
2. The §12c "Tension with §Endpoint Compromise" paragraph carries an architectural-honesty
   moment (suspension visibility scope) — voice-check may consider whether the
   operator-only-encryption framing reads with enough urgency for readers who skim.
3. No prose-review concerns block the voice-check stage.

Pre-existing CLAIM markers at lines 461 (#46) and 527 (#47) are unchanged and remain queued
for their respective extension passes. They are not within #12's review scope.
