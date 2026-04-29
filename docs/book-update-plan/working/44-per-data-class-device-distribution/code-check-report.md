# Code-check report — #44 Per-Data-Class Device-Distribution

**Iteration:** code-check on iter-0032 draft
**Date:** 2026-04-28
**Stage advance:** draft → code-check
**Verdict:** PASS-with-claim-markers (one cross-reference correction queued for technical-review)

---

## Scope

Code-check pass on the new section delivered at iter-0032:

1. **Ch16 §Per-Data-Class Device-Distribution** (`chapters/part-3-reference-architecture/ch16-persistence-beyond-the-node.md`, lines 132–190; ~1,754 body words). Inserted between the existing §Lazy Fetch and Storage Budgets section (ending line 128) and the existing §Snapshot Format and Rehydration section (line 194).
2. **New Ch16 §References list** (lines 397–409, six new IEEE refs [1]–[6]).

The section carries:
- 2 opening paragraphs (motivation, dual-failure framing)
- Five sub-pattern subsections: 44a (manifest, line 140), 44b (push filter, line 148), 44c (placeholder pattern, line 154), 44d (MDM update, line 164), 44e (audit/observability, line 172)
- §Failure modes block (line 178) carrying five named conditions and the kill trigger
- One CLAIM marker (line 188)

---

## 1. Sunfish package inventory

| Namespace | Sites in #44 | Canon status | Verification |
|---|---|---|---|
| `Sunfish.Kernel.Buckets` | 3 (lines 134 [annotation], 146 [body], 168 [body — implicit via `Sunfish.Kernel.Audit` adjacency, see §1 note]) | **In canon.** | `packages/kernel-buckets/` exists in Sunfish repo (verified by directory listing). Already present in Ch11:168 as the partial-sync engine package owning `IBucketRegistry`/YAML bucket definitions/`IBucketFilterEvaluator`/lazy-fetch stubs; also present at Ch16:128 ("storage budget, eviction policy, and minimum stub retention period are configurable via `Sunfish.Kernel.Buckets`"). The HTML annotation header at line 134 declares it `(in canon, Ch16:128, extended for class-subscription manifest)` — correct. |
| `Sunfish.Kernel.Sync` | 2 (lines 134 [annotation], 150 [body — section opens with `\`Sunfish.Kernel.Sync\` on the sending node applies the receiver's manifest as a push filter`]) | **In canon.** | `packages/kernel-sync/` exists in Sunfish repo (verified by directory listing); already in current Sunfish package canon and present in `build/code-check.py` SUNFISH_PACKAGES allow-list. The HTML annotation header at line 134 declares it `(in canon, Ch14, extended for class-aware push filter)` — correct. |
| `Sunfish.Kernel.Audit` | 3 (lines 134 [annotation], 168 [body], 176 [body]) | **In canon** (per cerebrum 2026-04-28 update at L39 — `packages/kernel-audit/` verified to exist on disk). | The HTML annotation header at line 134 declares it `(in canon per cerebrum 2026-04-28, packages/kernel-audit/)` — correct designation; the 2026-04-28 cerebrum update established that earlier extension headers at Ch15 lines 119/304/585 (#48/#45/#9) had erroneously called it forward-looking. **#44 correctly designates Audit as in-canon — improvement over the precedent in those earlier headers.** |
| `Sunfish.Foundation.Fleet` | 2 (lines 134 [annotation], 176 [body]) | **In canon** by extension #11's introduction in Ch21, but **the Sunfish reference implementation does not yet contain a `packages/foundation-fleet/` directory** (verified by directory listing of `packages/`). Per Ch21's own annotation header at line 8, this namespace "is part of the Volume 1 extension roadmap and not yet present in the Sunfish reference implementation. Tracked in docs/reference-implementation/sunfish-package-roadmap.md." | **Annotation header at line 134 inconsistent with Ch21's declared status.** #44 says "in canon, introduced #11"; Ch21 says "Volume 1 extension roadmap, not yet present in reference implementation." The two annotations are not aligned. **See §11 item 6 (queued correction).** |

**Summary of namespace status as authored in #44's HTML annotation header (line 134):**

> `<!-- code-check: namespaces referenced — Sunfish.Kernel.Buckets (in canon, Ch16:128, extended for class-subscription manifest), Sunfish.Kernel.Sync (in canon, Ch14, extended for class-aware push filter), Sunfish.Kernel.Audit (in canon per cerebrum 2026-04-28, packages/kernel-audit/), Sunfish.Foundation.Fleet (in canon, introduced #11). No new top-level namespace. Default to direct extension of Sunfish.Kernel.Buckets for the manifest; consider sub-namespace Sunfish.Kernel.Buckets.Subscription only if the manifest's surface area pulls in unrelated dependencies — confirm at code-check stage. APIs illustrative pending v1.0. -->`

All four namespaces are declared. Three (Buckets, Sync, Audit) are correctly designated as in-canon and verified by directory listing. The fourth (Foundation.Fleet) is designated in-canon but conflicts with Ch21's own forward-looking declaration — flagged below.

**No new top-level namespaces introduced** (commitment from outline §D / draft-report §"Namespace declaration" honored). All four namespaces named are extensions of existing or roadmap-tracked packages.

**Class APIs / method signatures:** zero introduced. All references to package internals — class-subscription manifest, push filter, eviction protocol, fleet inventory — are framed as roles or contracts, not as class names with method signatures. The `data_class` YAML field (lines 146, 152) is a schema field, not a class member; the `class_not_subscribed` exclusion-reason value (line 162) is a record-payload string constant; the `financial_role` and `financial` class-name examples (lines 142, 162, 180) are illustrative class identifiers, not invented APIs.

## 2. Code blocks

- Fenced code blocks in §Per-Data-Class Device-Distribution: **0**
- Inline backtick identifiers in prose: present (e.g., `Sunfish.Kernel.Sync`, `Sunfish.Kernel.Buckets`, `Sunfish.Kernel.Audit`, `Sunfish.Foundation.Fleet`, `data_class`, `class_not_subscribed`, `financial_role`, `required_attestation`, `WHERE`); illustrative by context — none represent invented runnable APIs.
- `// illustrative — not runnable` markers required: **0** (no code blocks).
- Invented-API audit: **0 invented APIs.** All inline identifiers refer to YAML schema fields, payload constants, role names, or canonical SQL keywords.

## 3. CLAIM markers

| # | Location | Disposition |
|---|---|---|
| 1 | Ch16 line 188, §Failure modes block, "Forward-secrecy boundary at mid-stream subscription" paragraph | **Preserved.** Format: `<!-- CLAIM: the per-class forward-secrecy ratchet's handling of mid-stream subscription onboarding is not architecturally resolved in the current draft of #46 — verify whether a key-state handoff to newly-subscribing devices is specified or whether mid-stream subscriptions accept an undecryptable-history boundary as a feature. -->`. Within loop-plan policy of ≤1 CLAIM marker per draft. Queued for technical-review resolution against the current state of #46 (which has completed technical-review at iter-0028 — see `docs/book-update-plan/working/46-forward-secrecy/technical-review-report.md`). The marker pre-supposes a per-class FS ratchet; the technical-reviewer should confirm against #46's actual scope (per-message vs. per-class FS) before either retiring the marker or revising the §Failure modes paragraph. |

The two pre-existing CLAIM markers in Ch15 (lines 461 from #46 and 527 from #47) are unchanged by #44 — they remain queued for their own respective technical-review passes and are unrelated to this section.

## 4. Cross-reference resolution

**Note on the parallel-draft dependency callout in the prompt brief:** The prompt instructed code-check to flag the forward cross-reference to "Ch15 §Event-Triggered Re-classification" as a parallel-draft dependency that may not yet resolve because #10 is being drafted in parallel. **Status update:** #10 has in fact landed in Ch15 — `## Event-Triggered Re-classification` is present at Ch15:690, with sub-patterns 10a–10e at lines 696–722. The forward reference resolves cleanly; no parallel-draft dependency remains. (This is a positive race outcome — both extensions completed and integrated cleanly.)

| Reference site | Target | Resolves? | Note |
|---|---|---|---|
| Ch16:138 → §Declarative Sync Buckets (Ch16) | Ch16:48 (`## Declarative Sync Buckets`) | **PASS** | Bucket model is the layer #44 extends; the §44a manifest section frames the class-subscription manifest as a higher-level abstraction over the bucket entries this section already specifies. |
| Ch16:144 → Ch14 §Five-Step Handshake | Ch14:52 (`## Five-Step Handshake`) | **PASS** | Drafter correctly used the actual Ch14 section name (the outline had named "§Capability Negotiation" — the draft-report §"Cross-references" notes the correction). The handshake message-field reference at Ch14:87 (`### Wire Format — Message Field Reference`) is the implicit payload-extension point for the manifest; technical-review should confirm a payload slot exists or specify the correct extension point (drafter flag 3, see §11 item 3). |
| Ch16:150 → Ch14 §Data Minimization at the Stream Level | Ch14:141 (`## Data Minimization at the Stream Level`) | **PASS** | Drafter correctly used the actual Ch14 section name (the outline had named "§Subscription Enforcement"). The Ch14 §Data Minimization section is the substrate the class-subscription filter composes with at the same protocol tier. |
| Ch16:152 → Ch15 §Event-Triggered Re-classification | Ch15:690 (`## Event-Triggered Re-classification`) | **PASS** | **No longer a parallel-draft dependency.** #10's drafted Ch15 section landed before #44's code-check; the forward reference resolves cleanly. The §44b body cites this section for the runtime-reclassification path that composes with the manifest filter through the §44d eviction protocol. |
| Ch16:158 → §Lazy Fetch and Storage Budgets (Ch16) | Ch16:93 (`## Lazy Fetch and Storage Budgets`) | **PASS** | The class-excluded placeholder reuses the stub-conversion mechanism from §Lazy Fetch and Storage Budgets but adds the policy-blocked-vs-fetchable distinction the §44c sub-pattern foregrounds. |
| Ch16:166 → Ch15 §Collaborator Revocation | Ch15:302 (`## Collaborator Revocation and Post-Departure Partition`) | **PASS-with-naming-note** | The actual Ch15 section is "Collaborator Revocation and Post-Departure Partition" (full H2 at Ch15:302). The §44d body uses the abbreviated name "§Collaborator Revocation". This abbreviation pattern matches existing book usage — Ch11 §The UI Kernel similarly abbreviates "Chapter 11 §The UI Kernel: Four-Tier Layering". Acceptable; no correction required. |
| Ch16:168 → Ch15 §Event-Triggered Re-classification (re-cite) | Ch15:690 | **PASS** | Second cite in §44d for the eviction-on-escalation composition; resolves to the same target as the first cite. |
| Ch16:170 → Ch11 §Fleet Management | **NOT FOUND in Ch11.** Actual fleet-management content lives in **Ch21 (Operating a Fleet, part-5)**. Ch21 H2 sections include 21.1 "Why fleet management is a distinct discipline" (line 36), 21.3 "Fleet-scale key rotation orchestration" (line 103), 21.5 "Fleet observability" (line 187), and 21.6 "The fleet failure scenario" (line 229). | **FAIL — cross-reference target wrong chapter.** | The draft says "Cross-reference Ch11 §Fleet Management for the administrative workflow that governs manifest update authorization, approval, and rollout." The administrative workflow for fleet-scale enrollment, key-rotation orchestration, OTA update orchestration, and fleet observability is in Ch21, not Ch11. Ch11 (Node Architecture) covers the kernel/UI/IPC structure of a single node; Ch11 references `Sunfish.Kernel.Buckets` and `SunfishNodeHealthBar` but does not own the fleet-management workflow. **The outline §H also incorrectly named "Ch21 §Fleet Management" — the outline §D and draft-report §"Cross-references" both intended Ch11 but Ch21 is the correct target.** Recommend correction at technical-review: change `Ch11 §Fleet Management` to `Ch21 §Operating a Fleet` (or to a specific Ch21 sub-section — most likely `Ch21 §21.4 — OTA Update Orchestration` if such exists, or 21.1 / 21.5 / 21.6 depending on which administrative facet is meant). See §11 item 7 (queued for technical-review). |

**Cross-reference summary:** 7 of 8 references resolve cleanly; **1 fails** (Ch11 §Fleet Management → does not exist in Ch11; correct target is Ch21). The prompt's note about the parallel-draft dependency for #10 / Ch15 §Event-Triggered Re-classification was overtaken by events — that reference resolves cleanly.

The cross-reference name corrections from the draft-report (Ch14 §Five-Step Handshake replacing the outline's §Capability Negotiation; Ch14 §Data Minimization at the Stream Level replacing the outline's §Subscription Enforcement) are correctly applied in the draft and verified against actual Ch14 headings. **One additional correction is needed:** Ch11 → Ch21 for §Fleet Management.

## 5. Citation resolution

**Numbering convention used:** Ch16-local [1]–[6]. The drafter chose this against the prompt's suggestion of [42]–[47]. **See §8 for the citation-numbering convention check against Appendix E.**

In-text citation sites in the new section, traced both directions:

| In-text site | Ref | Resolves to entry? | Source |
|---|---|---|---|
| Ch16:146 §44a (PowerSync bucket-definition model) | [5] | **PASS** | PowerSync — "Sync Rules — Bucket Definitions" (PowerSync Documentation, 2024) — Ch16:407 |
| Ch16:152 §44b (ElectricSQL shape filtering) | [4] | **PASS** | ElectricSQL — "ElectricSQL v0.10 released — shape-based partial replication" (electric-sql.com Blog, Apr. 10, 2024) — Ch16:405 |
| Ch16:160 §44c (OneDrive Files On-Demand) | [2] | **PASS** | Microsoft — "Save disk space with OneDrive Files On-Demand for Windows" (Microsoft Support, 2024) — Ch16:401 |
| Ch16:160 §44c (iCloud Optimize Mac Storage) | [3] | **PASS** | Apple Inc. — "Optimise Mac storage in iCloud" (Apple Support, 2024) — Ch16:403 |
| Ch16:160 §44c (Dropbox Selective Sync) | [1] | **PASS** | Dropbox — "Selective Sync overview" (Dropbox Help Center, 2024) — Ch16:399 |
| Ch16:176 §44e (Bayou subscription model) | [6] | **PASS** | D. B. Terry et al. — "Managing update conflicts in Bayou" (SOSP '95) — Ch16:409 |

Reverse direction — every entry [1]–[6] in the Ch16 reference list has at least one in-text site:

- [1] cited at line 160
- [2] cited at line 160
- [3] cited at line 160
- [4] cited at line 152
- [5] cited at line 146
- [6] cited at line 176

**No orphan refs; no broken numbers; no duplicate entries.** All six citations from outline §E are present (the outline labelled them [A]–[G] with [G] being Kleppmann et al. 2019 as a possible inclusion, but [G] was not adopted in the final draft — that omission is consistent with the draft-report §"Citations added" table). IEEE numeric style preserved per Appendix E.

The citation order in the body does not match the numbering: the first numbered ref encountered in the body is [5] at line 146, then [4] at line 152, then [1]/[2]/[3] at line 160, then [6] at line 176. **Per Appendix E §"Assembly Guidance"**: at final-manuscript assembly, the manuscript will be walked in reading order and renumbered from [1] to [N] in first-appearance order. The current Ch16-local numbering is sub-optimal for first-appearance ordering ([1] should be PowerSync, [2] should be ElectricSQL, etc., based on body order). However, per the same Appendix E section, the canonical numbering happens at final assembly, not at chapter-local stage. **No correction required at code-check; final-assembly renumbering will normalise the order.** Documented as informational.

## 6. Sub-pattern coverage

| Sub-pattern | Section pointer | Coverage status |
|---|---|---|
| 44a — Per-device data-class subscription manifest | Ch16:140 (`### The class-subscription manifest`) | **PASS** — Manifest distinct from attestation (line 142); signed CBOR under Ed25519 (line 144); carries device_id, issuer (MDM authority key or self-signed), accepted-class list, issued_at, expiry, signature (line 144); class → bucket resolution via optional `data_class` field (line 146); signed versions retained in audit log (line 146); PowerSync [5] analogue with client-vs-server inversion noted (line 146); travels with device identity during five-step handshake (line 144). |
| 44b — Sync-daemon push filter | Ch16:148 (`### Sync-daemon push filter`) | **PASS** — Filter applied at send tier alongside attestation filter (line 150); class-label-driven filter (line 152); silent drop with no error mirrors field-level out-of-scope behaviour (line 152); reclassification at runtime is Ch15 §Event-Triggered Re-classification's domain (line 152); O(1) hash-set check (line 152); ElectricSQL [4] WAN-sync analogue with schema-class-vs-SQL-WHERE distinction (line 152). |
| 44c — Cross-class reference handling: the policy-blocked placeholder | Ch16:154 (`### Cross-class references: the policy-blocked placeholder`) | **PASS — principal novelty.** Three options framing (line 156); explicit boldface fetchable-vs-not-fetchable distinction (line 158: "**A lazy-evicted stub is fetchable on demand. A class-excluded placeholder is not.**"); OneDrive [2] / iCloud [3] / Dropbox [1] analogues each shown to mislead in distinct ways — OneDrive/iCloud signal latency, Dropbox creates an untyped void (line 160); placeholder structure carries record_id, class_label, exclusion_reason `class_not_subscribed`, no content (line 162); UI rendering contract enforced at application layer (line 162); integrity guarantee — detectable, not silent (line 162). |
| 44d — MDM/policy-driven manifest update | Ch16:164 (`### MDM-driven manifest update and propagation`) | **PASS** — Signed update via OTA (line 166); manifest version bump and audit log entry on receipt (line 166); revocation-shaped event with cross-ref to Ch15 §Collaborator Revocation (line 166); eviction-on-tightening with stub-conversion via `Sunfish.Kernel.Audit` (line 168); composition with #10 escalation explicit at the manifest interface (line 168); expansion respects bucket replication mode (eager vs. lazy, line 170); cross-ref to Ch11 §Fleet Management (**Ch11 incorrect — see §4 above**, but the cross-reference *intent* and *placement* are correct). |
| 44e — Audit and observability | Ch16:172 (`### Audit and observability`) | **PASS** — Per-device class inventory (signed; counts of full records and placeholders per class; manifest version per acquisition/eviction; line 174); fleet aggregation via `Sunfish.Foundation.Fleet` (line 176); discrepancy detection during offline-update window (line 176); `Sunfish.Kernel.Audit` for all change events (line 176); Bayou [6] precedent with the architecture's contribution called out (policy-blocked placeholder semantics + MDM-signed manifest as fleet artifact) (line 176). |

All five sub-patterns from outline §B are covered. Drafter's coverage table in `draft-report.md` matches independently-verified prose.

## 7. Mandatory artifacts

| Artifact | Status | Location |
|---|---|---|
| HTML annotation header (in-canon namespace disclosure) | **PASS-with-fleet-correction-flag** | Ch16:134 — declares all four namespaces (Buckets, Sync, Audit, Foundation.Fleet) in a single comment block; declares zero new top-level namespaces; flags the Buckets-direct vs. Buckets.Subscription sub-namespace question for code-check resolution. **Issue:** Foundation.Fleet's "in canon, introduced #11" designation conflicts with Ch21's own annotation header at line 8 which calls it "Volume 1 extension roadmap, not yet present in the Sunfish reference implementation." See §11 item 6 for the queued correction. |
| FAILED conditions block | **PASS** | Ch16:178 (`### Failure modes`) — five named conditions present: (a) Manifest conflated with attestation (line 180); (b) Placeholder treated as error state (line 182); (c) Manifest expansion treated as eager backfill (line 184); (d) Eviction-on-tightening skipped (line 186); (e) Forward-secrecy boundary at mid-stream subscription (line 188 — carries the CLAIM marker). All five outline §F conditions covered (F-1, F-3, F-4 directly; F-2 and F-5 satisfied by construction — F-2 via cross-reference rather than re-specification, F-5 via no new namespace introduced). |
| Kill trigger sentence | **PASS** | Ch16:190 — `**Kill trigger.** If technical review determines that the class-subscription manifest cannot coexist with the existing bucket YAML schema without a breaking change to the \`required_attestation\` field's role-driven semantics, escalate before continuing. The manifest's device-policy axis and the attestation's user-role axis must compose in a single bucket evaluation; if they cannot, the extension's scope changes and the present specification requires redesign.` Confirmed at end of §Failure modes block per outline §F. |
| Sub-namespace open question (Buckets-direct vs Buckets.Subscription) | **PASS** | Embedded in the HTML annotation header at line 134: "Default to direct extension of Sunfish.Kernel.Buckets for the manifest; consider sub-namespace Sunfish.Kernel.Buckets.Subscription only if the manifest's surface area pulls in unrelated dependencies — confirm at code-check stage." This is the open question from outline §D and draft-report §"Namespace declaration." **Code-check disposition: defer to technical-review** — the manifest's surface-area implications cannot be evaluated without consulting the v13 / v5 source papers (gitignored on this workstation). Queued as §11 item 8. |

## 8. Citation-numbering convention check (Ch16-local vs global, per Appendix E)

The drafter chose **Ch16-local [1]–[6]** numbering against the prompt's original suggestion of [42]–[47]. The draft-report §"Citations added" justifies this with two arguments:

1. Ch16 had no pre-existing reference list; the global [42]–[47] would imply continuity from a non-existent prior numbering.
2. Part III chapter-local convention applies (Ch12 starts at [1], Ch13 starts at [1], Ch14 starts at [1]; Ch15 is the exception, running [1]–[36] because it has been the cumulative anchor for #46/#47/#45/#48/#9/#12).

**Verification against Appendix E (`chapters/appendices/appendix-e-citation-style.md`):**

Appendix E §"Assembly Guidance" specifies (lines 124–128):

> 1. Walk the manuscript in reading order and renumber every citation from [1] to [N] in first-appearance order.
> 2. Compile the numbered Reference List in the back matter, entries matching the renumbered in-text citations.
> 3. Verify every in-text bracket resolves to a Reference List entry, and every Reference List entry is cited at least once.

This rule confirms that **chapter-local numbering during draft is acceptable** because the canonical numbering is performed at final-manuscript assembly. Appendix E does not specify that mid-draft numbering must match the eventual global order. The drafter's choice is consistent with:

- **Ch12** (`chapters/part-3-reference-architecture/ch12-crdt-engine-data-layer.md`) — restarts at [1].
- **Ch13** (`chapters/part-3-reference-architecture/ch13-schema-migration-evolution.md`) — restarts at [1].
- **Ch14** (`chapters/part-3-reference-architecture/ch14-sync-daemon-protocol.md`) — restarts at [1] (per `## References` heading at Ch14:271; not opened in this code-check, declared by drafter).

Ch15 is the exception, running [1]–[36] because it has accumulated reference entries cumulatively across multiple security-architecture extensions (#46/#47/#45/#48/#9/#12). That accumulation pattern reflects Ch15's role as the cumulative security-architecture anchor — not a deviation from the chapter-local convention but a chapter-internal continuation of an already-running list.

**Code-check disposition: ACCEPT Ch16-local [1]–[6].** This is consistent with Part III chapter-local convention and consistent with Appendix E §"Assembly Guidance" — final-assembly renumbering will produce the global numbering. No correction required at code-check stage.

## 9. build/code-check.py output (raw)

```
$ python3 build/code-check.py ch16

Code check: ch16-persistence-beyond-the-node.md
  Code blocks: 7

  ERRORS (1):
    - Unresolved CLAIM marker: <!-- CLAIM: the per-class forward-secrecy ratchet's handling of mid-stream subscription onboarding is not architecturally resolved in the current draft of #46 — verify whether a key-state handoff to newly-subscribing devices is specified or whether mid-stream subscriptions accept an undecryptable-history boundary as a feature. -->

Exit code: 1
```

The script counts 7 code blocks in Ch16, all of which are **outside** the new section (Mermaid diagrams in §Lazy Fetch lazy-fetch sequence at Ch16:97–124, §Backup UX state diagram at Ch16:252–260, §Non-Technical Disaster Recovery sequence diagram at Ch16:304–320; JSON snapshot example at Ch16:200–209; export directory tree at Ch16:354–367). The new section contributes **0** code blocks. The script's regex `r"```[\w]*\n(.*?)```"` does not flag the inline backticks in #44 prose because those are not fenced code blocks.

**Human-judgment override.**

The single CLAIM-marker error reported by the script is **expected and accepted** under loop-plan §5 policy — the marker is the deliberately-preserved CLAIM marker queued for technical-review against the current state of #46. The script's exit-1 behaviour is by-design strictness for the build pipeline (intended to block final-manuscript assembly with an unresolved CLAIM); at the iterative-extension code-check stage, an unresolved CLAIM marker is a *queued item for technical-review*, not a stage-advance blocker. Verdict reflects this: PASS-with-claim-markers.

The script does **not** flag the four namespaces in #44's HTML annotation header because the script's package check regex only matches identifiers within fenced code blocks (line 69: `re.findall(r"Sunfish\.\w+(?:\.\w+)*", block)` is scoped to `block` from the code-blocks loop). Inline backticks in prose are not matched by this check. Three of the four namespaces (Buckets, Audit, Foundation.Fleet) are also not in the script's `SUNFISH_PACKAGES` allow-list (lines 15–33), but because the namespaces appear only in inline backticks in prose, the script does not generate package errors for them. The HTML annotation header at line 134 is the explicit human-readable disclosure — same pattern accepted at #46/#47/#48/#9/#12 code-checks.

**Override note:** the single CLAIM-marker error is not blocking for code-check stage advance. Same pattern accepted at all prior extension code-checks.

## 10. Word count check

- **Target:** 1,500 words
- **±10% acceptable range:** 1,350 – 1,650
- **±20% extended-acceptable range:** 1,200 – 1,800
- **Standalone draft (incl. HTML comment + CLAIM marker):** 1,868 words *(measured: `wc -w docs/book-update-plan/working/44-per-data-class-device-distribution/draft.md` returns 1,868)*
- **Body prose in inserted section, HTML comments stripped:** **1,754 words** *(measured: `awk 'NR>=132 && NR<=190' chapters/part-3-reference-architecture/ch16-persistence-beyond-the-node.md | sed 's/<!--[^>]*-->//g' | wc -w` returns 1,754)*

**Status:** 1,754 body words is **104 words over the ±10% upper bound (1,650)**, **46 words under the ±20% upper bound (1,800)**. The overrun is **6.3% above the ±10% bound**, **2.6% below the ±20% bound**.

**Rationale (drafter-supplied, code-check-confirmed):** §44c carries the principal novelty of the extension (the policy-blocked-vs-fetchable distinction) and consumed ~410 body words against an outline §I budget of 350 words — proportional to its 23%-of-target-budget allocation in the outline. The §Failure modes block (~360 words) absorbs the FAILED conditions, kill trigger, and the forward-secrecy CLAIM, which are required artifacts. The drafter ran two trim passes from an initial 2,043 body words to 1,754. Further compression would compress either the OneDrive / iCloud / Dropbox three-way analogue contrast in §44c (the explicit ask in the prompt) or the §Failure modes block (also a required artifact). **Acceptable per loop-plan §QC-1 ±20% policy** — 104-word overrun documented, no QC-1 violation at the ±20% bound.

The prompt brief explicitly noted "drafter reports 1,754 body words (+17% vs 1,500 target, within ±20% extended-acceptable). Confirm acceptable per loop-plan §QC-1." **Confirmed acceptable.**

## 11. Items queued for technical-review

The following items are accepted for code-check but require @technical-reviewer verification against authoritative sources, v13/v5, and design-decisions §5 #44. Items 1–5 are pulled forward from the drafter's flag list (`draft-report.md` §"Tension flags for technical review"); items 6–10 are added by code-check.

1. **CLAIM marker resolution (Ch16:188).** Verify the per-class forward-secrecy ratchet's handling of mid-stream subscription onboarding against the current state of extension #46 (technical-review completed at iter-0028 — see `docs/book-update-plan/working/46-forward-secrecy/technical-review-report.md`). Either resolve the marker by retiring it (if #46 specifies a key-state handoff or accepts the undecryptable-history boundary as a feature) or revise the §Failure modes paragraph to align with #46's actual scope. Drafter forward flag (1).

2. **Bucket YAML schema extension** (drafter forward flag 2; outline §G item 1). Confirm that adding an optional `data_class` label to existing bucket entries is a non-breaking extension to the bucket YAML schema and does not interact with the `required_attestation` field's role-driven semantics. The kill trigger explicitly names the breaking-change scenario as escalation-required.

3. **CAPABILITY_NEG (five-step handshake) payload extension** (drafter forward flag 3; outline §G item 2). Confirm the existing five-step handshake (Ch14 §Five-Step Handshake) has a payload slot accommodating the class-subscription manifest, or identify the correct extension point. Outline §G item 2 suggested the existing `mdm_compliance` attestation slot as a likely candidate; verify against Ch14:87 §Wire Format — Message Field Reference.

4. **Eviction vs. deletion on manifest tightening** (drafter forward flag 4; outline §G item 3). Confirm eviction-to-stub (via class-excluded placeholder) is consistent with the existing eviction behaviour in `Sunfish.Kernel.Buckets`. The §44d body asserts stub conversion identical to the lazy-fetch eviction model; technical-review should confirm against the kernel-buckets package's actual eviction implementation if accessible.

5. **Sub-pattern verification against source paper** (drafter forward flag 5; outline §G item 5). Source `local_node_saas_v13.md` is gitignored on this workstation and was not consulted directly during draft or code-check. The sub-pattern decomposition derives from the outline + loop-plan. Technical-reviewer to verify sub-patterns 44a–44e against the primary source paper once accessible.

6. **`Sunfish.Foundation.Fleet` annotation header inconsistency.** [Code-check addition.] The HTML annotation header at Ch16:134 declares `Sunfish.Foundation.Fleet (in canon, introduced #11)`. However, Ch21's own annotation header at Ch21:8 declares Foundation.Fleet "part of the Volume 1 extension roadmap and not yet present in the Sunfish reference implementation. Tracked in docs/reference-implementation/sunfish-package-roadmap.md." The two annotations are not aligned. **Verification by directory listing confirmed `packages/foundation-fleet/` does not exist in the Sunfish repo** (other Foundation packages such as `foundation-localfirst/` and `foundation-recovery/` were not part of the listing scope but the absence of foundation-fleet/ is notable). Technical-review should align Ch16:134 with Ch21:8 — either by changing #44's designation to "(forward-looking, introduced as Volume 1 roadmap by #11)" or by updating Ch21's header if a status change has occurred. Recommend matching Ch21's existing forward-looking declaration to maintain consistency until the reference implementation lands the package. Same precedent as the canon-correction sweep noted in cerebrum L39 (Audit was previously called forward-looking incorrectly; it is now in-canon and the inconsistency was addressed by updating extension headers — Foundation.Fleet's status is the inverse: declared in-canon but actually forward-looking).

7. **Ch11 §Fleet Management cross-reference target wrong.** [Code-check addition; major.] Ch16:170 says "Cross-reference Ch11 §Fleet Management for the administrative workflow that governs manifest update authorization, approval, and rollout." **Ch11 has no §Fleet Management section**; the fleet-management content lives in **Ch21 — Operating a Fleet**. This is a discoverable error: the outline §H also incorrectly named "Ch21 §Fleet Management" (the outline named Ch21 for the OTA channel and Ch11 for the administrative workflow — both of those resolve to Ch21 in fact). Recommend correction: change `Ch11 §Fleet Management` to `Ch21 §Operating a Fleet`, or to a more specific Ch21 sub-section (`Ch21 §21.4 — OTA Update Orchestration` if a future H2 exists, or to `Ch21 §21.5 — Fleet Observability` if the administrative-workflow context is the dashboard view). Technical-review to determine the optimal Ch21 sub-section. **Acceptable defer-to-technical-review per the task prompt**: "Defer all substantive changes to technical-review." This is substantive (changes the chapter target and section name) so the code-check does not edit the chapter file.

8. **Sub-namespace decision: Buckets-direct vs Buckets.Subscription.** [Code-check addition.] The HTML annotation header at Ch16:134 defers this decision to code-check ("consider sub-namespace Sunfish.Kernel.Buckets.Subscription only if the manifest's surface area pulls in unrelated dependencies"). Code-check defers to technical-review because the manifest's surface-area implications cannot be evaluated without v13 / v5 source-paper access. Technical-review should confirm one of: (a) direct extension of `Sunfish.Kernel.Buckets` (current draft assumption); (b) sub-namespace `Sunfish.Kernel.Buckets.Subscription`; (c) a third option not yet identified. The annotation header should be updated to record the resolved decision once made.

9. **Citation [G] (Kleppmann et al. 2019) deliberately omitted.** [Code-check addition.] Outline §E listed seven candidate citations [A]–[G]; the draft adopted six ([1]–[6] mapping to outline [A]–[F]). [G] (Kleppmann et al. 2019, "Local-First Software") was not adopted — the draft-report's citations table at §"Citations added" lists six entries with no acknowledgment of the omission. The omission is editorially defensible (Kleppmann is already cited prolifically across the book; #44's specific contribution is clearer without re-anchoring to the foundational Kleppmann citation in this section). **No correction required at code-check** — flagged for technical-review acknowledgment to confirm the omission is intentional.

10. **Concept-index extraction.** [Code-check addition.] Generate updates to `docs/reference-implementation/_per-chapter/ch16-persistence-beyond-the-node.yaml` capturing the new concepts: per-data-class device-distribution policy, class-subscription manifest, signed CBOR manifest under Ed25519, manifest-as-restriction-layer-over-attestation, `data_class` YAML label, class → bucket resolution, sync-daemon class-aware push filter, three-options framing for cross-class references (refuse / silent-null / explicit-placeholder), policy-blocked placeholder, `class_not_subscribed` exclusion reason, fetchable-vs-not-fetchable distinction, MDM-driven manifest update via OTA, eviction-on-tightening with stub conversion, eager-vs-lazy bucket replication mode in expansion, per-device class inventory, fleet-level inventory aggregation via `Sunfish.Foundation.Fleet`, discrepancy detection during offline-update window, manifest-change/eviction/backfill audit events in `Sunfish.Kernel.Audit`, MDM-signed manifest as fleet artifact, Bayou subscription model precedent.

11. **Sunfish-package-roadmap.md cross-reference.** [Code-check addition; minor.] Ch21:8 and Ch20:252 cross-reference `docs/reference-implementation/sunfish-package-roadmap.md`. The annotation header at Ch16:134 does not include the parallel cross-reference — it could improve traceability if the Foundation.Fleet annotation cross-referenced the roadmap document. **Resolve at the same time as item 6** (Foundation.Fleet annotation correction).

## 12. Verdict

**PASS-with-claim-markers.**

- All four Sunfish package references are accounted for in the HTML annotation header at line 134.
- Three (Buckets, Sync, Audit) verified as in-canon by directory listing of `Sunfish/packages/`.
- Foundation.Fleet's annotation says "in canon, introduced #11" but conflicts with Ch21:8's "Volume 1 extension roadmap, not yet in reference implementation" — flagged for technical-review correction (item 6); not a code-check blocker because the cross-reference precedent for forward-looking namespaces is established.
- 0 new top-level namespaces introduced (commitment from outline §D honored).
- 0 code fences in new section, 0 invented APIs, 0 placeholder markers, 0 `<!-- TBD -->` markers (verified by grep; no matches in Ch16).
- 1 new CLAIM marker preserved at line 188 (within loop-plan ≤1-per-extension policy).
- 7 of 8 cross-references resolve cleanly; **1 cross-reference target wrong** (Ch11 §Fleet Management → does not exist; correct target is Ch21 §Operating a Fleet) — flagged for technical-review correction (item 7).
- All 6 new IEEE references [1]–[6] resolve in both directions; Ch16-local numbering accepted per Appendix E §"Assembly Guidance" final-assembly renumbering rule.
- All 5 sub-patterns (44a / 44b / 44c / 44d / 44e) covered to outline §B specification.
- All mandatory artifacts present (HTML annotation header / FAILED conditions / kill trigger / sub-namespace open-question note).
- Word count: 1,754 body words = 6.3% over ±10% bound, 2.6% below ±20% upper bound. Documented and accepted.
- Parallel-draft dependency (Ch15 §Event-Triggered Re-classification) resolved positively — #10 has landed in Ch15.

**Two substantive items deferred to technical-review:** Foundation.Fleet annotation header consistency (item 6); Ch11 → Ch21 §Fleet Management cross-reference correction (item 7). Both are documented in §11 with recommended fixes; neither edits the chapter file at code-check per the prompt's "Defer all substantive changes to technical-review" directive.

## 13. Gate decision

Code-check → technical-review **PASSES**. Section advances to technical-review with **11 documented items** for the next reviewer (1 CLAIM-marker resolution + 4 drafter-forwarded flags + 6 code-check additions). The HTML annotation header at line 134 represents an improvement over the precedent established at #46/#47/#48/#9 — those declared `Sunfish.Kernel.Audit` forward-looking incorrectly; #44 declares Audit as in-canon (correct per cerebrum 2026-04-28) and ties the designation to the Sunfish-repo path. The Foundation.Fleet inconsistency is the inverse of the Audit precedent (in-canon designation where forward-looking is more accurate) and is queued for parallel correction. The human-judgment override on `build/code-check.py`'s strict CLAIM-error exit is documented in §9 and consistent with all prior extension code-checks (#46/#47/#48/#9/#12).
