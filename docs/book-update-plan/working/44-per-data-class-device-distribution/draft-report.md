# Draft report — #44 Per-Data-Class Device-Distribution

**Stage:** draft complete; ready for code-check.
**Target chapter:** Ch16 — Persistence Beyond the Node, Part III.
**Insertion:** between §Lazy Fetch and Storage Budgets and §Snapshot Format and Rehydration (Ch16 line 132).
**Working draft copy:** `docs/book-update-plan/working/44-per-data-class-device-distribution/draft.md`.

---

## Word count

| Measure | Count |
|---|---|
| Target | 1,500 |
| ±10% range | 1,350–1,650 |
| ±20% range | 1,200–1,800 |
| **Body words (excluding HTML comments + code blocks)** | **1,754** |
| Deviation from target | +17% (within ±20%, outside ±10%) |

**Rationale for +17% deviation:** Sub-pattern 44c (cross-class references / policy-blocked placeholder) is the principal novelty of the extension and the primary risk surface for reader confusion. The outline §I budgets it at 350 of 1500 words (23%); the draft holds it at ~410 words (23% of body) — proportional to the outline. The §Failure modes block (~360 words) absorbs the FAILED conditions, kill trigger, and the forward-secrecy CLAIM, all of which are required artifacts. Trimming further would either compress the policy-blocked-vs-fetchable distinction (the explicit ask in the prompt) or remove the failure-mode block (also a required artifact). The +17% sits within the prompt's ±20% allowance.

The draft was already trimmed twice from an initial 2,043 body words. Further compression risks losing the explicit OneDrive / iCloud / Dropbox vs. policy-blocked distinction the prompt names as the core novelty.

---

## Sub-pattern coverage

All five sub-patterns from outline §B are covered in the draft.

| Sub-pattern | Section | Coverage |
|---|---|---|
| **44a** Per-device data-class subscription manifest | `### The class-subscription manifest` | Manifest distinct from attestation; signed CBOR under Ed25519; carries device_id, issuer, class list, issued_at, expiry, signature; class → bucket resolution via optional `data_class` field; signed versions retained for audit; PowerSync [5] analogue with client-vs-server inversion noted. |
| **44b** Sync-daemon push filter | `### Sync-daemon push filter` | Filter applied at send tier alongside attestation filter; class-label-driven; silent drop with no error (mirrors field-level out-of-scope behavior); O(1) hash-set check; ElectricSQL [4] WAN-sync analogue. |
| **44c** Cross-class reference / policy-blocked placeholder | `### Cross-class references: the policy-blocked placeholder` | **Principal novelty.** Explicit contrast: lazy stub fetchable on demand vs. class-excluded placeholder NOT fetchable. OneDrive [2] / iCloud [3] / Dropbox [1] analogues shown to mislead — they signal latency, not denial. Placeholder structure (record_id, class_label, exclusion_reason=`class_not_subscribed`, no content). UI rendering contract; integrity guarantee (detectable, not silent). |
| **44d** MDM/policy-driven manifest update | `### MDM-driven manifest update and propagation` | Signed update via OTA channel; manifest version bump; sync-daemon load at next capability negotiation; eviction-on-tightening (stub conversion); composition with #10 escalation explicit; expansion respects bucket replication mode (eager vs. lazy); cross-ref Ch11 §Fleet Management. |
| **44e** Audit / observability | `### Audit and observability` | Per-device class inventory (signed; counts per class; manifest version per acquisition/eviction); fleet aggregation via `Sunfish.Foundation.Fleet`; discrepancy detection during offline-update window; `Sunfish.Kernel.Audit` for all change events; Bayou [6] precedent. |

---

## Citations added

**Note on numbering:** The prompt suggested [42]–[47]. Ch16 had no existing references list; per Appendix E (citations are renumbered at final assembly in reading order) and Part III chapter-local convention (Ch12 starts at [1], Ch13 at [1], Ch14 at [1], Ch15 at [1]–[36]), Ch16's first reference list begins at [1]. Final-assembly renumbering will produce a global numbering across the book.

| # | Source | Use |
|---|---|---|
| [1] | Dropbox Selective Sync overview (Help Center) | §44c — analogue, untyped void contrast |
| [2] | Microsoft OneDrive Files On-Demand (Microsoft Support) | §44c — placeholder-as-presence-indicator analogue, fetchable-on-demand contrast |
| [3] | Apple iCloud "Optimise Mac storage" (Apple Support) | §44c — eviction-stub / on-access materialisation analogue |
| [4] | ElectricSQL v0.10 shape filtering (electric-sql.com blog) | §44b — closest production analogue for per-device WAN push filter |
| [5] | PowerSync Sync Rules / bucket definitions (docs.powersync.com) | §44a — bucket-as-client-parameter-driven-selector analogue, client-vs-server inversion |
| [6] | Terry et al. (1995) "Managing update conflicts in Bayou" SOSP | §44e — earliest academic precedent for device-level partial-replication subscriptions |

All six citations from the outline §E are present; none were dropped.

---

## Namespace declaration

Per outline §D, **no new top-level namespace.** Four in-canon packages extended:

- `Sunfish.Kernel.Buckets` — extended for class-subscription manifest storage and class → bucket resolution. (Already in canon at Ch16:128.)
- `Sunfish.Kernel.Sync` — extended for class-aware push filter on outbound deltas. (In canon, Ch14.)
- `Sunfish.Kernel.Audit` — used for manifest-change, eviction, and backfill events. (In canon per cerebrum 2026-04-28, `packages/kernel-audit/`.)
- `Sunfish.Foundation.Fleet` — used for per-device class-inventory aggregation. (In canon, from extension #11.)

Code-check open question retained from outline §D: confirm whether the manifest belongs directly in `Sunfish.Kernel.Buckets` or in a sub-namespace `Sunfish.Kernel.Buckets.Subscription`. Default to direct extension; flag for code-check stage. Annotation header carries this note.

---

## Cross-references

| Direction | Target | Use |
|---|---|---|
| Backward | Ch16 §Declarative Sync Buckets | Bucket model is the layer this extension extends; class-level filtering is second axis over role-level filtering. |
| Backward | Ch16 §Lazy Fetch and Storage Budgets | Stub model; eviction-on-tightening reuses stub conversion; placeholder differs from stub by being non-fetchable. |
| Backward | Ch14 §Five-Step Handshake | Manifest travels with device identity during handshake. |
| Backward | Ch14 §Data Minimization at the Stream Level | Push filter sits at same tier; the two filters compose. |
| Backward | Ch15 §Collaborator Revocation | Subscription change is a revocation-shaped event. |
| Backward | Ch15 §Forward Secrecy | Mid-stream subscription onboarding boundary; CLAIM marker for #46 verification. |
| Forward | Ch15 §Event-Triggered Re-classification | Composition with extension #10 — escalation produces class-change event; manifest filter reacts via eviction protocol. |
| Forward | Ch11 §Fleet Management | Administrative workflow for manifest update authorization, approval, rollout. |

Note on Ch14 section names: the outline referenced Ch14 §Capability Negotiation and §Subscription Enforcement; the actual Ch14 sections are §Five-Step Handshake and §Data Minimization at the Stream Level. The draft uses the actual section names.

---

## FAILED conditions block

Implemented as the `### Failure modes` subsection. All five outline-§F conditions present, plus the kill trigger:

- **Manifest conflated with attestation** (F-1)
- **Placeholder treated as error state** (F-3)
- **Manifest expansion treated as eager backfill** (F-4)
- **Eviction-on-tightening skipped** (new — composition correctness with #10)
- **Forward-secrecy boundary at mid-stream subscription** (with CLAIM marker)
- **Kill trigger** (manifest/bucket-schema coexistence — escalate if breaking change required)

F-2 (push filter mechanics duplicated in Ch16) is satisfied by construction: the draft cross-references Ch14 §Data Minimization at the Stream Level for the enforcement substrate rather than re-specifying it. F-5 (no new namespace invented) is satisfied by the namespace declaration above.

---

## Kill trigger sentence

> "If technical review determines that the class-subscription manifest cannot coexist with the existing bucket YAML schema without a breaking change to the `required_attestation` field's role-driven semantics, escalate before continuing."

Rationale: the manifest's device-policy axis and the attestation's user-role axis must compose in a single bucket evaluation. If they cannot, the extension scope changes (per outline §F).

---

## Novelty notes

**Principal novelty: policy-blocked vs. fetchable placeholders.** The draft makes this distinction at three levels:

1. The **bold sentence** in §44c: "A lazy-evicted stub is fetchable on demand. A class-excluded placeholder is not."
2. The **prior-art contrast** explicitly walks through OneDrive [2], iCloud [3], and Dropbox [1] to show why each is a different shape — OneDrive/iCloud signal latency; Dropbox creates an untyped void; the architecture's placeholder is a typed policy boundary.
3. The **structure-level distinction**: the placeholder carries an explicit `exclusion_reason` of `class_not_subscribed`, not a missing-content indicator. Applications render it as a restricted-reference indicator, not a "not found" error.

**Secondary novelty: MDM-signed manifest as fleet artifact.** The Bayou [6] precedent established device-level subscription declarations academically; the architecture's contribution is binding the subscription to MDM authority signing and to a per-device audit inventory aggregated at fleet level via `Sunfish.Foundation.Fleet`.

**Composition with #10 (escalation):** the eviction protocol from outline §J is condensed into the §MDM-driven manifest update subsection — when escalation produces a class-change record and the device's manifest excludes the new class, the daemon evaluates against the manifest and schedules eviction. The two extensions compose at the manifest interface; #10 produces the event, #44 reacts. Cross-reference is forward to Ch15 §Event-Triggered Re-classification (where #10 lives).

---

## Tension flags for technical review

1. **Forward-secrecy mid-stream subscription** (outline §G item 4). The draft carries a single CLAIM marker on this point. The text states the boundary as designed (newly-subscribed devices cannot decrypt historical class operations under per-class FS) but flags that #46's draft does not yet specify whether a key-state handoff is provided or whether the undecryptable-history boundary is accepted as a feature. Tech-reviewer should resolve against the current #46 spec.

2. **Bucket YAML schema extension** (outline §G item 1). The draft assumes an optional `data_class` label can be added to existing bucket entries without breaking the `required_attestation` semantics. Tech-reviewer to confirm that the addition is a non-breaking extension.

3. **CAPABILITY_NEG payload** (outline §G item 2). The draft places manifest exchange in the five-step handshake (Ch14 §Five-Step Handshake). Tech-reviewer to confirm the handshake's existing payload slot accommodates the manifest, or identify the correct extension point.

4. **Eviction vs. deletion** (outline §G item 3). The draft commits to eviction-to-stub (via class-excluded placeholder) rather than full deletion when a manifest tightens. Tech-reviewer to confirm consistency with the existing eviction behavior in `Sunfish.Kernel.Buckets`.

5. **Sub-pattern verification against source paper** (outline §G item 5). Source `local_node_saas_v13.md` is gitignored and was not consulted directly; sub-pattern decomposition derives from outline + loop-plan. Tech-reviewer to verify against v13 once accessible.

---

## CLAIM markers

One CLAIM marker inserted, in the §Forward-secrecy boundary failure mode:

> `<!-- CLAIM: the per-class forward-secrecy ratchet's handling of mid-stream subscription onboarding is not architecturally resolved in the current draft of #46 — verify whether a key-state handoff to newly-subscribing devices is specified or whether mid-stream subscriptions accept an undecryptable-history boundary as a feature. -->`

This is the loop-plan policy maximum (1 CLAIM per draft). Resolves against #46 once that extension's tech-review completes.

---

## Deviations from outline

1. **Word budget +17%** (outline §I targets 1,500; draft is 1,754). Rationale above. Within ±20% allowance per prompt.

2. **Citations renumbered to [1]–[6]** instead of prompt's [42]–[47]. Ch16 had no pre-existing reference list; Part III chapter-local numbering convention applies. Final-assembly renumbering pass per Appendix E will produce the global numbering.

3. **Ch14 cross-reference target names corrected.** Outline used "§Capability Negotiation" and "§Subscription Enforcement" — actual Ch14 section names are "§Five-Step Handshake" and "§Data Minimization at the Stream Level." Draft uses the actual names.

4. **Ch15 §Event-Triggered Re-classification cross-reference is forward-looking** — that section does not yet exist in Ch15 (extension #10 drafts it in parallel into Ch15+Ch20). Draft references it as if present; will resolve when #10 lands. No `<!-- forward: -->` HTML marker added because the cross-reference reads naturally either way.

5. **§Audit subsection condenses two outline bullets into one paragraph** (per-device inventory + fleet aggregation merged into a single paragraph) to hit the trimmed word budget without losing content.

6. **Failure modes block uses explicit bold-labeled bullets** as specified by the outline §F template; the kill trigger appears as the final bold-labeled item rather than as a separate H4.

---

## QC checklist self-assessment

- [x] QC-1 Word count within ±20% (1,754 vs. 1,500 target; ±10% missed by ~7 percentage points; documented above)
- [x] QC-2 Every topic in outline §A–§J addressed
- [x] QC-3 Sources cited inline ([1]–[6] with reference list added to Ch16)
- [x] QC-4 Sunfish packages referenced by name only — no class APIs invented
- [x] QC-5 No academic scaffolding ("this section explores", "as we have seen") — checked
- [x] QC-6 No re-introducing the architecture; opens directly with the failure scenario
- [x] QC-7 Part III specification voice maintained (no second-person, no hedging, no there-is constructions)
- [x] QC-9 Not applicable (council chapter rule)
- [x] QC-10 No placeholder text (one CLAIM marker is policy-permitted, not a placeholder)

---

## Files changed

| File | Change |
|---|---|
| `chapters/part-3-reference-architecture/ch16-persistence-beyond-the-node.md` | Inserted §Per-Data-Class Device-Distribution between §Lazy Fetch and §Snapshot Format; added §References list at end ([1]–[6]). |
| `docs/book-update-plan/working/44-per-data-class-device-distribution/draft.md` | New file — working draft copy. |
| `docs/book-update-plan/working/44-per-data-class-device-distribution/draft-report.md` | This file. |

No conflict with extension #10, which writes to ch15 + ch20.
