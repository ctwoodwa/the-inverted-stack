# Draft Report — Extension #10: Data-Class Escalation (Event-Triggered Re-classification)

**Stage:** icm/draft (Stage 2)
**Branch context:** GitButler workspace (parent loop)
**Drafter:** chapter-drafter subagent
**Date:** 2026-04-28

---

## Files written

- `chapters/part-3-reference-architecture/ch15-security-architecture.md` — new H2 section `## Event-Triggered Re-classification` inserted between `## GDPR Article 17 and Crypto-Shredding` and `## Relay Trust Model` (now at line 690). Five new IEEE references appended to the Ch15 reference list ([37]–[41]).
- `chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md` — new H2 section `## Data-Class Escalation UX` inserted between `## Revocation UX` and `## Accessibility as a Contract` (now at line 354).
- `docs/book-update-plan/working/10-data-class-escalation/draft-ch15.md` — working copy
- `docs/book-update-plan/working/10-data-class-escalation/draft-ch20.md` — working copy

## Word count per file

Word counts exclude HTML comments and code-check annotation headers.

| File | Target | Actual | Δ vs target |
|---|---|---|---|
| `draft-ch15.md` (Ch15 §Event-Triggered Re-classification) | ~1,000 | 1,408 | +41% |
| `draft-ch20.md` (Ch20 §Data-Class Escalation UX) | ~1,000 | 1,392 | +39% |
| **Combined** | **~2,000** | **2,800** | **+40%** |

### Word-count overage rationale (mandatory per loop-plan §4)

The combined ~2,800 word count is materially over the user-prompt's 2,000-word target (40% over, beyond the ±20% rationale-acceptable band). The drafter's judgment on the overage:

1. **Five sub-patterns plus opening plus FAILED block plus kill trigger × 2 sections is structurally larger than 2,000 words at this chapter's voice register.** Peer sections in Ch15 — §Chain-of-Custody for Multi-Party Transfers (~3,000+ words covering 3 sub-patterns), §Privacy-Preserving Aggregation at Relay (~2,800+ words covering 3 sub-patterns) — show that the chapter's specification voice consistently runs ~700–1,000 words per sub-pattern when threat model, mechanism, and FAILED conditions are all required. Ch15 §Event-Triggered Re-classification carries 5 sub-patterns and lands at ~280 words per sub-pattern, which is at the **tighter** end of this chapter's per-sub-pattern density, not the looser end.
2. **Ch20's UX register is denser than typical Part IV content because each UX surface (badge, refused-read message, offline-reconnect, operator flow, cross-class review) has both a plain-language user-facing string requirement and a wiring requirement.** The user prompt's "minimal path" guidance for Part IV is honoured at the per-sub-section level (no API surface area, references back to Ch15 for mechanism), but the surface count is fixed by the underlying mechanism's user-visible touchpoints.
3. **Trim path attempted; further trimming threatens specification completeness.** Three iterations brought Ch15 from 2,040 → 1,650 → 1,425 → 1,408 and Ch20 from 1,240 → 1,392 (Ch20 grew on the second pass when the FAILED block + kill trigger were added per the user prompt's required-artifacts list). Further compression would either drop a sub-pattern, drop the principal-novelty contrast paragraph, or strip the FAILED block to two bullets, all of which violate explicit user-prompt requirements.
4. **Recommendation to technical-review and prose-review:** accept the overage. If a hard 2,000-word ceiling is required, the trim candidates in priority order are (a) merge §10c and §10e into §10b (saves ~150 words but reduces audit-trail and schema-evolution clarity); (b) compress the Ch20 cross-class review section (saves ~80 words at the cost of the human-in-the-loop framing); (c) drop the §Composition forward sub-section in Ch15 and inline the GDPR/forward-secrecy pointers into 10a (saves ~150 words and forfeits the surfaced tension flag the user prompt asked for).

## Sub-patterns covered (with file)

All five sub-patterns from the outline are covered. Distribution:

| Sub-pattern | Ch15 (spec) | Ch20 (UX) |
|---|---|---|
| 10a — max-register class-label op (PRINCIPAL NOVELTY) | yes — full spec, max-register CRDT semantics, Microsoft Purview / AWS Macie / Google Cloud DLP contrast paragraph | mentioned indirectly via the operator flow — UI does not display a downward option, because §10a's max-register invariant rejects them |
| 10b — backward propagation across replicated copies | yes — full spec, identical to revocation broadcast in §Collaborator Revocation, gossip via `Sunfish.Kernel.Sync` | yes — offline-reconnect experience subsection cross-references §10b |
| 10c — audit-trail handling | yes — full spec, history operations preserved, access policy follows current class, audit record's class is the new class | not duplicated — Ch20 references the audit log as the source for the operator review queue but does not re-explain the audit-trail handling |
| 10d — cross-class references | yes — full spec, reference index in `Sunfish.Kernel.SchemaRegistry`, operator review (no auto-escalation) | yes — cross-class reference review subsection (UX surface for the operator review queue) |
| 10e — schema-evolution non-interaction | yes — full spec, ownership boundary between `Sunfish.Kernel.SchemaRegistry` migration and `Sunfish.Kernel.Security` access enforcement | not duplicated — Ch20 does not surface schema-evolution since it does not affect UX |

## Citations added

Five new IEEE references appended to the Ch15 reference list (now at [1]–[41]; previously [1]–[36]). Ch20 shares these references by number per outline §E.

| Cite | Source | Used in |
|---|---|---|
| [37] | NIST SP 800-60 Vol. 1 Rev. 1 — high-watermark principle | Ch15 §10a (max-register alignment with high-watermark) |
| [38] | NIST SP 800-60 Rev. 2 IWD — updated classification guidance | Ch15 §10a (paired with [37]) |
| [39] | ISO/IEC 27001:2022 Annex A 5.12 — classification review requirement | Ch15 §10a (periodic-review obligation) |
| [40] | GDPR Article 9 — special-category trigger | Ch15 §10a (inferred-special-category trigger example) |
| [41] | Microsoft Purview sensitivity labels | Ch15 §10a Principal-novelty paragraph (centralized-online contrast) |

All five citations land in Ch15 §10a (consolidated under the foundational sub-pattern). Ch20 inherits the references by number and does not introduce new ones.

## Namespace declaration

Per outline §D, no new top-level Sunfish package is introduced. The HTML code-check annotation header at the start of each new section declares all referenced namespaces with canon status:

**Ch15 §Event-Triggered Re-classification:**
- `Sunfish.Kernel.Security` — in-canon, extends existing
- `Sunfish.Kernel.Audit` — in-canon (per cerebrum 2026-04-28; `packages/kernel-audit/` exists)
- `Sunfish.Kernel.SchemaRegistry` — in-canon
- `Sunfish.Kernel.Sync` — in-canon

**Ch20 §Data-Class Escalation UX:** same four kernel packages plus
- `Sunfish.UIAdapters.Blazor` — in-canon (hosts the class-indicator component alongside `SunfishFreshnessBadge`; the new component is referenced by location, not by class name, to avoid invented APIs)

Zero class APIs / method signatures introduced in either section. The class-indicator component in Ch20 is referenced by package location and the existing peer component (`SunfishFreshnessBadge`) is mentioned as the wiring analogue — no new class name is invented.

## Cross-references

### Ch15 backward references (existing → new)
- §GDPR Article 17 and Crypto-Shredding — §Composition forward references this for the deletion-of-escalated-records flow
- §Collaborator Revocation and Post-Departure Partition — §10b references this for the structural broadcast analogue; §10c references sub-pattern 45c for the cached-copy framework
- §Chain-of-Custody for Multi-Party Transfers — opening references this primitive for the dashcam-evidence export path; CLAIM marker flags chain-of-custody event-vs-state composition as unresolved
- §Forward Secrecy and Post-Compromise Security — §Composition forward references this for envelope re-keying

### Ch15 forward references (new → existing)
- Ch20 §Data-Class Escalation UX — §10b references this for forward-only invalidation UX consequence; §10d references this for operator review surface

### Ch20 backward references (new → existing)
- §Revocation UX — opening paragraph names the parallel and distinguishes the trigger
- §AP/CP Visibility by Data Class — second paragraph back-references the table per outline §H
- Ch15 §Event-Triggered Re-classification — opening states "the mechanism that makes that legibility possible is specified in Ch15 §Event-Triggered Re-classification. This section does not re-state it." Single cross-reference, no re-explanation, per Part III/Part IV pattern
- §UX for the Non-Technical Adopter — offline-reconnect subsection references the support path

### Ch20 forward references
- §Accessibility as a Contract — implicit (immediately follows the new section; no explicit cross-ref)

## FAILED conditions

Both new sections include a FAILED conditions block per the user-prompt required-artifacts list.

**Ch15 §Event-Triggered Re-classification — 4 FAILED conditions:**
1. Re-classification operation lowers a record's class level (Architecture failure)
2. Offline node delivers reads from cached prior-class copy after reconnect re-classification delivery (Architecture failure)
3. Cross-class reference cascade auto-escalates without operator review (Architecture failure)
4. Escalation event not recorded in `Sunfish.Kernel.Audit` at the new class level (Compliance failure)

**Ch20 §Data-Class Escalation UX — 4 FAILED conditions:**
1. Access-tightened message names the new class level or asserting authority to a user without access at the new class (UX failure — failure-path metadata leak)
2. Offline-reconnect handshake delivers a read from prior-class cache as if it were live state (UX failure)
3. Operator escalation form accepts an escalation without a trigger event identifier (Compliance failure)
4. Cross-class reference review queue auto-resolves an unreviewed candidate (UX failure)

## Kill triggers

**Ch15 kill trigger:** "A re-classification operation that converges to a lower class than its highest received argument at any replica. A primitive that does not preserve max-register monotonicity is not data-class re-classification — it is mutable-state pretending to converge."

**Ch20 kill trigger:** "An access-tightened message that lists the new class level to a user without access at that class. A primitive that uses the failure path to disclose the metadata the access tightening exists to protect is not access tightening — it is a side channel."

## Novelty / honesty notes

The Principal-novelty paragraph in Ch15 §10a names Microsoft Purview, AWS Macie, and Google Cloud DLP as the centralized-online contrast and explicitly states that none applies a max-register CRDT invariant to a security metadata field with access-control re-evaluation as a delivery-side effect. The contribution is positioned as "convergent re-classification under partial replication without duplicating storage and without breaking the immutable audit trail" — verifiable claim, framed as architecture contribution rather than overstated novelty.

NIST SP 800-60's high-watermark principle is cited as conceptual alignment, not as a prior implementation of the same mechanism. ISO/IEC 27001:2022 Annex A 5.12 is cited as the periodic-review compliance obligation the architecture satisfies, not as a mechanism specification. GDPR Article 9 is cited as a trigger source, not as a mechanism. Microsoft Purview is cited specifically as the contrast (centralized, online, against a canonical store).

## Tension flags for tech-review

One CLAIM marker inserted (within the loop-plan ≤1 budget) at Ch15 §Composition forward, line 39 of draft-ch15.md:

> `<!-- CLAIM: re-classification re-encryption under forward-secrecy ratchet — confirm envelope-only re-keying is sufficient for all class transitions; same question for §Chain-of-Custody chain-of-custody receipts under in-flight escalation. Flag for technical-review. -->`

Two compositional tensions surfaced in this single CLAIM marker:

1. **Composition with #46 forward secrecy:** A re-classification that moves a record into a class with a different KEK envelope requires re-wrapping the DEK under the new class's KEK. If the prior KEK was ephemeral under a forward-secrecy ratchet, the new envelope must derive from current ratchet state, not from the prior KEK. The drafter's working answer is that envelope-only re-keying suffices — the record's content does not need re-encryption — but the boundary conditions under aggressive ratchet rotation deserve explicit specification at technical-review.

2. **Composition with #9 chain-of-custody:** Does an in-flight custody receipt remain valid when the underlying record escalates? The receipt covers the *event* of transfer at a specific class assertion; if the class changes mid-transfer, does the receipt invalidate? The drafter's hypothesis is that the receipt covers the version-vector-identified state of the record at the moment of transfer (per §Chain-of-Custody sub-pattern 9a), and a subsequent escalation produces a separate event in the same audit log without invalidating the prior receipt — but this needs technical-reviewer confirmation against the §Chain-of-Custody specification.

**Composition with #45 collaborator revocation** is resolved cleanly in the prose: same broadcast mechanism, different trigger, same gossip path in `Sunfish.Kernel.Sync`. No CLAIM marker needed; the prose names this directly in §10b.

## Deviations from outline

1. **Per-sub-section word budgets exceeded uniformly.** The outline §I budget table sums to ~1,050 words for Ch15 and ~950 for Ch20. Actual counts are 1,408 and 1,392 — each running ~30–50% above the per-section budget. Same rationale as the combined-overage rationale above: full coverage of 5 sub-patterns + principal novelty + FAILED + kill trigger requires more words than the outline budget anticipated for this chapter's voice register.
2. **Composition forward as a standalone H3 in Ch15** (not in outline). The outline placed forward-secrecy/chain-of-custody composition in §G open-technical-review items. The drafter elevated this to in-prose surfacing per the user-prompt's "TENSIONS to surface" requirement, with the CLAIM marker flagging the unresolved compositional questions for technical-review.
3. **The `Sunfish.UIAdapters.Blazor` package reference in Ch20** does not name a specific component class (`SunfishClassBadge` was an early invented name; removed in revision). The component is referenced by package location and by analogy to the existing in-canon `SunfishFreshnessBadge`. This is consistent with the QC-4 / Sunfish reference policy (no invented class APIs).
4. **Ch20 FAILED block + kill trigger added** despite being a Part IV (tutorial voice) section. The user-prompt required-artifacts list mandates both in BOTH new sections; the Ch20 block uses UX-flavoured failure framings (failure-path metadata leak, audit gap) rather than mechanism failures.

## QC checklist self-assessment

| Item | Status | Note |
|---|---|---|
| QC-1 Word count ±10% | FAIL | +40% combined; rationale documented above |
| QC-2 All outline topics addressed | PASS | All 5 sub-patterns + composition + FAILED + kill trigger |
| QC-3 Source sections cited inline | PARTIAL | IEEE [37]–[41] cited inline; v13/v5 sourcing for max-register invariant is the technical-review item per outline §G item 1 (max-register CRDT for class labels — confirm v13/v5 sourcing or acknowledge as extension; current prose acknowledges this implicitly via the Principal-novelty paragraph) |
| QC-4 Sunfish packages by name only | PASS | No class APIs / method signatures introduced |
| QC-5 No academic scaffolding | PASS | Ledger-checked: no "this section explores", "as we have seen", "the author argues" |
| QC-6 No re-introducing the architecture | PASS | Both sections assume Part I and prior chapters |
| QC-7 Part III spec / Part IV tutorial voice | PASS | Ch15 = specification; Ch20 = tutorial with single back-ref to Ch15 §Event-Triggered Re-classification |
| QC-9 Council two-act (N/A — not council chapter) | N/A | |
| QC-10 No placeholder text | PASS | No TBD / expand here / see paper for details |

Recommended next stage: `icm/code-check` to validate Sunfish package canon status and the absence of invented class APIs, followed by `icm/technical-review` to address the CLAIM marker and outline §G items 1 (max-register invariant v13/v5 sourcing) and 6 (forward-secrecy composition).
