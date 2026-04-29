# Code-Check Report — Extension #10 (Data-Class Escalation)

**Stage:** ICM Stage 3 (code-check)
**Sections under review:**
- Ch15 §Event-Triggered Re-classification (lines 690–737)
- Ch20 §Data-Class Escalation UX (lines 354–409)

**Method note:** Per loop owner instruction, `python3 build/code-check.py` was not run; the loop accepts human-judgment override on every #-extension code-check. Verification done by direct read of the new section ranges plus targeted grep against the cerebrum package canon.

---

## 1. HTML Annotation Headers — CONFIRMED

Both sections open with the required `<!-- code-check annotations: ... -->` block.

**Ch15 (line 692):** Lists `Sunfish.Kernel.Security`, `Sunfish.Kernel.Audit`, `Sunfish.Kernel.SchemaRegistry`, `Sunfish.Kernel.Sync`. Declares "0 new top-level namespaces. 0 class APIs / method signatures introduced."

**Ch20 (line 356):** Lists the same four kernel packages plus `Sunfish.UIAdapters.Blazor` (badge component host). Declares "0 new top-level namespaces. 0 class APIs / method signatures introduced."

Both annotations align with cerebrum canon (`Sunfish.Kernel.Audit` + `Sunfish.Kernel.SchemaRegistry` confirmed in-canon as of 2026-04-28).

## 2. Sunfish Package Site Inventory

**Ch15 §Event-Triggered Re-classification (in-text references):**
- `Sunfish.Kernel.Audit` — line 702 (trigger-event resolution); line 716 (escalation event record)
- `Sunfish.Kernel.Sync` — line 708 (gossip-path propagation)
- `Sunfish.Kernel.Security` — line 710 (immediate access-control re-eval); line 720 (queries reference index); line 724 (read-time field-access enforcement)
- `Sunfish.Kernel.SchemaRegistry` — line 720 (reference index)

All four are in-canon. **No invented namespaces. No class APIs, method signatures, or constructor parameters surfaced.** Behaviours are described at the package boundary ("hands the operation to," "queries the reference index," "issues the operation").

**Ch20 §Data-Class Escalation UX (in-text references):**
- `Sunfish.UIAdapters.Blazor` — line 368 (hosts class-indicator component "alongside the freshness badge")
- `Sunfish.Kernel.Security` — line 368 (record's current class); line 390 (issues the operation)
- `Sunfish.Kernel.Audit` — line 368 (recent escalation event read)
- `Sunfish.Kernel.SchemaRegistry` — line 396 (reference index for cross-class review)
- `Sunfish.Kernel.Sync` — line 390 (propagates the operation)

All five are in-canon. **`SunfishClassBadge` is NOT introduced as a named class.** The component is referenced by analogy ("the same slot the freshness badge occupies," "alongside the freshness badge") and by package home (`Sunfish.UIAdapters.Blazor`). No method signatures, no constructor parameters, no XAML/Razor markup. The cerebrum rule "package name, not class API" is honoured.

## 3. Sub-Pattern Coverage (10a–10e) — CONFIRMED with Pointers

| Sub-pattern | Ch15 anchor | Ch20 cross-ref |
|---|---|---|
| 10a — Re-classification op + max-register CRDT invariant | line 696 | line 388 ("§10a's max-register invariant rejects [downward options]") |
| 10b — Backward propagation across replicated copies | line 706 | line 380 (offline-reconnect handshake cites "sub-pattern 10b") |
| 10c — Audit-trail handling under class change | line 714 | implicit at line 374 (operator/compliance ids stay in audit log) |
| 10d — Cross-class references and operator review | line 718 | line 396 (cites "sub-pattern 10d") + entire §Cross-class reference review |
| 10e — Schema-evolution non-interaction | line 722 | not surfaced to user (correctly — UX has no payload-shape implication) |

Every sub-pattern has an in-Ch15 home. 10a, 10b, and 10d carry explicit cross-references from Ch20. 10c surfaces in Ch20 only as a side observation (audit-log access scope), which is correct — the audit-trail invariant is a Part III specification concern, not a Part IV user surface. 10e is correctly absent from Ch20 (no UX consequence when payload shape is unchanged).

## 4. CLAIM Marker Audit — 1 marker, correctly placed

**Location:** Ch15 line 728, inside §Composition forward.

**Text:** "CLAIM: re-classification re-encryption under forward-secrecy ratchet — confirm envelope-only re-keying is sufficient for all class transitions; same question for §Chain-of-Custody chain-of-custody receipts under in-flight escalation. Flag for technical-review."

This is the right marker for the right place. The composition with §Forward Secrecy is genuinely under-specified in the new draft (envelope-only re-keying is asserted as "common case" with boundary conditions explicitly deferred). Marker is well-formed and correctly defers to technical-review (Stage 4), not code-check.

**No CLAIM markers in Ch20.** Correct — Ch20 specifies user-visible behaviour grounded in Ch15's architectural commitments and adds no new architectural claims.

## 5. FAILED Conditions + Kill Trigger — CONFIRMED

**Ch15 (lines 730–737):** Four FAILED conditions present:
1. Re-classification operation lowers a record's class level
2. Offline node delivers reads from prior-class cache after receiving operation
3. Cross-class reference cascade auto-escalates without operator review
4. Escalation event not recorded in `Sunfish.Kernel.Audit` at the new class level

Kill trigger present (line 737): "a re-classification operation that converges to a lower class than its highest received argument at any replica."

**Ch20 (lines 400–409):** Four FAILED conditions present:
1. Access-tightened message names new class level or asserting authority to a user without access
2. Offline-reconnect delivers prior-class cache as live state
3. Operator escalation form accepts an escalation without trigger event identifier
4. Cross-class reference review queue auto-resolves an unreviewed candidate

Kill trigger present (line 409): "an access-tightened message that lists the new class level to a user without access at that class."

Both blocks follow the architecture-failure / compliance-failure / UX-failure framing the precedent extensions established. Kill triggers are sharp and falsifiable.

## 6. References [37]–[41] — Bidirectional Resolution CONFIRMED

In-text uses (Ch15):
- Line 700: `[37][38]` (NIST SP 800-60 high-watermark principle)
- Line 700: `[39]` (ISO/IEC 27001:2022 Annex A 5.12)
- Line 702: `[40]` (GDPR Article 9 special categories)
- Line 704: `[41]` (Microsoft Purview sensitivity labels)

Reference list entries (lines 913–921):
- [37] NIST SP 800-60 Vol. 1 Rev. 1
- [38] NIST SP 800-60 Rev. 2 IWD
- [39] ISO/IEC 27001:2022 Annex A 5.12
- [40] GDPR Article 9
- [41] Microsoft Purview sensitivity labels

All five citations resolve in both directions. No orphan refs, no orphan in-text markers in the new section.

## 7. Word Count Overage — Recommend ACCEPT

Loop owner reports Ch15 §Event-Triggered Re-classification at +41% over the section budget, Ch20 §Data-Class Escalation UX at +39% over, combined +40%.

**Precedent:** Extension #45 (Collaborator Revocation) accepted at +55%, Extension #48 accepted at +115% — both with the "review-driven, not bloat" framing where the council/literary-board cycle drove length to absorb specific reviewer demands rather than authorial expansion.

**Judgment for #10:** The Ch15 section carries five sub-patterns, a max-register invariant proof sketch, a principal-novelty positioning paragraph against Purview/Macie/DLP, a composition-forward note with a flagged CLAIM, four FAILED conditions, and a kill trigger. The Ch20 section carries five UX surfaces (badge, refusal message, offline reconnect, operator flow, reference review), four FAILED conditions, and a kill trigger. There is no daylight between section content and section budget that would survive a cut without losing a load-bearing element. **+40% is review-driven, not bloat.**

**Recommendation: ACCEPT word-count overage.** Frame in the integration commit as consistent with #45 and #48 precedent.

## 8. Verdict + Gate Decision

**Verdict: PASS.**

- HTML annotation headers present and accurate at start of both sections
- Sunfish package sites all in-canon; zero invented namespaces; zero class APIs / method signatures
- 10a–10e all covered in Ch15 with file+line pointers; Ch20 cross-refs to 10b and 10d; 10e correctly absent from UX layer
- 1 CLAIM marker in Ch15 §Composition forward, well-formed, correctly deferred to technical-review
- 4 FAILED conditions + kill trigger in each section, sharp and falsifiable
- Refs [37]–[41] resolve in both directions
- Word count +40% combined; ACCEPT under #45/#48 precedent

**Gate decision:** Advance both sections to ICM Stage 4 (technical-review). The §Composition forward CLAIM marker is the only deferred item and the right reviewer for it is Stage 4, not Stage 3.

**Items not verified within tool budget:**
- Did not re-read full chapter files; relied on targeted reads of the two new section ranges plus reference-list grep. If the loop owner needs a sweep for ripple effects elsewhere in Ch15/Ch20, that is a separate pass.
- Did not run `python3 build/code-check.py` (per instruction).
