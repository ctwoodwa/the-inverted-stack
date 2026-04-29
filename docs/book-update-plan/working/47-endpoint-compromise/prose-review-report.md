# Prose-review report — #47 Endpoint Compromise

**Iteration:** iter-0022 (prose-review)
**Date:** 2026-04-28
**Stage advance:** technical-review (PASS-with-claim-markers) → prose-review
**Verdict:** PASS

---

## Scope

Two new sections from extension #47:

1. **Ch15 §Endpoint Compromise: What Stays Protected** — H2 starting line 494, ending before §Supply Chain Security (line 569). ~1,691 words.
2. **App B §THREAT-10 — Compromised Endpoint** — H3 inside §Section 2, lines 73–113. ~554 words.

Out of scope (preserved untouched): Ch15 §Forward Secrecy and refs [14]–[19] (prose-reviewed at iter-0021); Ch15 §Collaborator Revocation; Ch15 §Supply Chain Security; Ch15 refs [1]–[19]; Ch15 refs [20]–[27] (untouched per instructions); the §47c CLAIM marker (out of scope, preserved as-is).

## Edits applied — Ch15 §Endpoint Compromise

### Academic scaffolding (1 edit)

- **Line 500.** Removed passive abstract opener "The obligation discharged here is sub-pattern 47a:". Replaced with active opener "Sub-pattern 47a is the explicit scope declaration:". The reformulation puts agency on the named primitive rather than a passive nominalization ("obligation discharged"). The list of "Not a footnote. Not a disclaimer. A dedicated section..." closer is preserved.

### Active voice (3 edits)

- **Line 525.** "The attestation is presented to the relay at handshake" → "The node presents the attestation to the relay at handshake". Active. Agent is the node.
- **Line 525.** "A device that fails attestation is denied relay admission and falls back to local-only operation" → "The relay denies admission to a device that fails attestation, and the device falls back to local-only operation." Active; relay is the agent of denial.
- **Line 553.** "Future writes from the compromised device are trusted by peers until revocation propagates" → "Peers trust future writes from the compromised device until revocation propagates." Active; peers are the agent.

### Punctuation tightening (1 edit)

- **Line 504.** Removed weakly-attached comma in "the residual risk, when the endpoint is compromised" → "the residual risk when the endpoint is compromised" — the temporal clause is restrictive, not parenthetical.

### Synonym tightening (1 edit)

- **Line 553.** "Biometric-based authentication" → "Biometric authentication". The "-based" suffix added no information; the noun-on-noun form is shorter and used elsewhere in the security chapter.

### Internal extension-number leak (1 edit)

- **Line 559.** "The primitive's FAILED conditions, drawn directly from design-decisions §5 #47:" → "The primitive's FAILED conditions:". Removed `#47` editorial-process leak (same fix pattern as #46 prose-review). The `design-decisions §5` provenance is correctly captured in the HTML code-check comment at line 492; user-facing prose does not need it.

## Edits applied — App B §THREAT-10

### Editorial-process leak (1 edit)

- **Line 75.** "THREAT-10 is the first numbered, structured entry in this taxonomy. Subsequent extensions follow the same THREAT-NN format." → "Subsequent threat entries follow the same THREAT-NN format used here." Two changes: (a) removed self-conscious "first numbered, structured entry in this taxonomy" — readers do not need to know the entry's position in the editorial backlog; (b) replaced "Subsequent extensions" (book-update-loop terminology) with "Subsequent threat entries" (reader-facing terminology). Preserves the format-convention statement which is genuinely useful for setting reader expectations on subsequent THREAT-NN entries.

## Edits considered but not applied

### Preservation flags honored

1. **§47f hard sentence — "No software-only architecture can claim otherwise."** (Ch15 line 555). Preserved verbatim. This sentence carries the §47f architectural-honesty load per tech-review item 10. No softening, no hedging-clause additions, no rewording. The full closing paragraph (6 sentences) was kept at the 6-sentence cap to retain the rhythm leading into the hard close.
2. **§47c CLAIM marker** (Ch15 line 527). Preserved as-is. Out of scope for prose-review per loop-plan §5; will resolve at the next #47-touching iteration or via parallel Ch14 update.
3. **Asymmetric reference numbering [7] / [20] / [21]** (Ch15 line 517). Preserved. The [7] (Apple) is shared with extension #48 — IEEE-correct re-use, not a renumbering bug. Tech-review item 1 documents the rationale.

### Not-applied because already on-voice

1. **Repeated "The honest limitation is X" opener** (lines 529 and 535). Considered as synonym/template cycling. Decision: leave. The two instances frame parallel honest-limitation statements (runtime-compromise gap; reachability gap) and the parallelism is rhetorically intentional — the sub-pattern's voice is precisely about naming limits aloud. Tightening one to break the parallel would weaken the §47f honesty thesis.
2. **"as a result" tail-clause** (line 519). Anti-AI tells §3 candidate. Decision: leave. The phrase is doing real causal work between two clauses about deployment posture differing for SGX vs. Secure Enclave; it is not a vague consequence-puff. Rewriting to "and the deployment posture reflects that gap" would lengthen the sentence without sharpening it.
3. **"Compromise of one device's private key does not compromise other devices"** (line 543). Repetition of "compromise" considered. Decision: leave. The repetition is a deliberate rhetorical play (technical noun → technical verb) that doubles the FAILED-condition statement. Spec voice tolerates it.
4. **Sub-pattern label cross-references** ("§47a", "§47e" inside the section body). Decision: leave. These are intra-section cross-references using the spec's own sub-pattern labels — consistent with §Forward Secrecy's "§Sub-pattern 46a" pattern, which was preserved at iter-0021 prose-review. Different from the `#47` editorial-process leak fixed at line 559.
5. **App B inline-header bullet list at line 105 (mitigation summary).** Five bullets each starting with a strong verb (Mandate, Enforce, Integrate, Enforce, Communicate). Anti-ai-tells §16 calibrated this format as correct for genuine reference/checklist content. Worksheet voice — leave as-is.
6. **App B numbered attack-tree** (lines 98–103). Each entry has a bold lead followed by terse explanation. Same calibration: this is the canonical attack-tree worksheet format. Leave.

## CLAIM markers preserved

- **§47c Ch14 attestation forward-dependency** (Ch15 line 527). 1 of 2 budget per loop-plan §5. Marker text untouched.

## Voice-register confirmation

- **Ch15 §Endpoint Compromise.** Part III specification voice maintained throughout. No "you should" instructions; statements are "X does Y" / "the architecture does Y" / "the primitive's FAILED conditions are Y". Cross-references resolve to other Part III sections (§In-Memory Key Handling, §Threat Model, §Key Hierarchy, §Collaborator Revocation, §Forward Secrecy, §Role Attestation Flow) and one Part II section (Ch7 §The Security Lens, for the council-challenge callback). All section names match canonical headings.
- **App B §THREAT-10.** Worksheet/checklist register maintained. Terse elliptical sentences ("Captured session token used to forge writes."), bold-led entries (Actor profile / Capabilities / Attack surface / etc.), numbered attack-tree branches. Did not prosify; did not over-tighten. The denser register is correct for an appendix worksheet template — distinct from chapter prose.

## Anti-AI tells grep results

- Significance puffery (§1): zero matches.
- Copula avoidance (§8): zero matches.
- AI vocabulary cluster (§7): zero matches (no delve / showcase / tapestry / interplay / intricate / pivotal / vibrant / enduring / underscores in either section).
- Persuasive authority tropes (§27): zero matches.
- There-is constructions: zero matches.
- Hedging defaults (could potentially / might be / under certain conditions): zero matches.

## Paragraph-length audit

All paragraphs in both sections are at or under the 6-sentence cap. Three Ch15 paragraphs (lines 519, 525, 555) sit exactly at the cap. The line 555 paragraph closes on the §47f hard sentence — its length is structural and cannot be shortened without breaking the load-bearing close.

## Quality gate

- Active voice: 3 passive-voice fixes applied. Section now active throughout.
- Academic scaffolding: 1 fix at the §47a sub-pattern opener.
- Internal extension-number leaks: 1 fix at line 559 + 1 fix at App B line 75. None remaining in user-facing prose.
- Synonym cycling: 1 minor tightening (biometric-based → biometric).
- §47f hard sentence: preserved.
- CLAIM markers: 1 of 2 budget preserved.
- Reference numbering [7] / [20] / [21] asymmetry: preserved (IEEE-correct).
- Voice register: Ch15 = Part III specification; App B = worksheet/checklist. Both confirmed.

**Verdict: PASS.** Section advances to voice-check (Stage 6).

## Notes for voice-check / iter-0023

1. Ch15 §Endpoint Compromise uses two parallel "The honest limitation is X" openers (lines 529, 535). The voice agent should preserve this parallelism — it is the rhetorical engine of §47f's honesty thesis.
2. The §47f closing paragraph (line 555) is rhythmically tuned to land on "No software-only architecture can claim otherwise." The voice agent must not break the lead-in chain (Pegasus/Predator/Hermit citation → "Against these..." → "On a fully Pegasus-compromised device..." → hard close).
3. App B THREAT-10 worksheet voice is intentionally denser than chapter prose. The voice agent should not prosify the elliptical entries (e.g., "Captured session token used to forge writes.") — the appendix register requires that terseness.
4. Sub-pattern label cross-references (§47a, §47e) are house-style internal references and consistent with §Forward Secrecy's §46a/§46b/etc. usage. Not an editorial-process leak.
