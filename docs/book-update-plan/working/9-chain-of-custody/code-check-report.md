# Code-check report — #9 Chain-of-Custody for Multi-Party Transfers

**Iteration:** iter-0024
**Date:** 2026-04-28
**Stage advance:** draft → code-check
**Verdict:** PASS-with-claim-markers

---

## Scope

Code-check pass on the two new sections delivered at iter-0023:

1. **Ch15 §Chain-of-Custody for Multi-Party Transfers** (`chapters/part-3-reference-architecture/ch15-security-architecture.md`, lines 583–670, ~2,394 words). Inserted between §Supply Chain Security and §GDPR Article 17 and Crypto-Shredding.
2. **App B §Section 5 — Chain-of-Custody Worksheet** (`chapters/appendices/appendix-b-threat-model-worksheets.md`, lines 237–300, ~548 words). Inserted after §Section 4 — Key Compromise Incident Response Template, before the appendix-wide closing italic block.

---

## 1. Sunfish package inventory

| Namespace | Sites (Ch15) | Sites (App B) | Sites total | Canon status |
|---|---|---|---|---|
| `Sunfish.Kernel.Custody` | 5 | 1 | 6 | **Forward-looking.** NOT in current canon; NOT in `build/code-check.py` `SUNFISH_PACKAGES` set. New namespace introduced by extension #9. |
| `Sunfish.Kernel.Audit` | 2 | 0 | 2 | **Forward-looking.** NOT in current canon (introduced by extension #48); same status as in #48 code-check. |

All references are package-name-only. No class names, no method signatures, no constructor parameters introduced. The four named items (`CustodyTransferInitiated`, `CustodyTransferConfirmed`, `CustodyTransferDisputed`, `RegulatoryExportBatch`) are event-record contract names, parallel to the event-contract naming convention established in §Key-Loss Recovery and §Collaborator Revocation; they are not class definitions, method signatures, or constructor signatures.

**Anticipatory state contracts** — string-literal lifecycle states (`transfer-initiated`, `transfer-completed`, `transfer-disputed`, `tsa-pending`) are documented as state-machine values, not as method or constant identifiers, and are consistent with the loop-plan's "state-machine documented in prose" pattern from #45 / #46 / #48.

**Action item carried into technical-review:** promote the `Sunfish.Kernel.Custody` anticipatory entry in `docs/reference-implementation/sunfish-package-roadmap.md` from `Future forward-looking namespaces` to a first-class roadmap entry with status `book-committed`, source extension #9. (Same lift pattern as `Sunfish.Foundation.Recovery` and `Sunfish.Kernel.Audit` from #48.)

## 2. Code blocks

- Fenced code blocks in Ch15 §Chain-of-Custody: **0**
- Fenced code blocks in App B §Section 5: **0**
- Inline backtick identifiers in prose (state-machine values + event-contract names): present, illustrative by context, not invented runnable APIs
- `// illustrative — not runnable` markers required: **0** (no code blocks)
- Invented-API audit: **0 invented APIs**. Event-contract names are explicitly framed as illustrative event records ("The list is illustrative; the concrete schema lands when `Sunfish.Kernel.Custody` reaches its first milestone." — Ch15 line 661).

## 3. CLAIM markers

| # | Location | Disposition |
|---|---|---|
| 1 | Ch15 line 621, end of §Sub-pattern 9b RFC 3161 paragraph | **Preserved.** Format: `<!-- CLAIM: source? — the two-signature receipt construction with TSA anchoring at this granularity is a new architectural commitment from design-decisions §5 #9; v13/v5 reference chain-of-custody only as a forward gap. -->`. Within loop-plan policy of ≤1 per extension. Queued for technical-review resolution. |

App B §Section 5 contains 0 CLAIM markers (by design — the appendix is a deployment worksheet, not architectural specification).

The two pre-existing CLAIM markers in Ch15 (line 461 from #46; line 527 from #47) are unchanged by #9; they remain queued for their respective technical-review passes.

## 4. Cross-reference resolution

| Reference site | Target | Resolves? | Note |
|---|---|---|---|
| Ch15 §Chain-of-Custody → §Key-Loss Recovery sub-pattern 48f (line 589) | Ch15 line 224 (`#### Recovery-event audit trail`) | **PASS** | Substrate-sharing back-reference |
| Ch15 §Chain-of-Custody → §Collaborator Revocation sub-pattern 45f (line 589) | Ch15 line 383 (`### Sub-pattern 45f — Revocation-event audit trail`) | **PASS** | Substrate-sharing back-reference |
| Ch15 §Chain-of-Custody → §Endpoint Compromise: What Stays Protected (line 613) | Ch15 line 494 | **PASS** | Receipt verifiability not dependent on custodian endpoint integrity |
| Ch15 §Chain-of-Custody → §Collaborator Revocation (line 643) | Ch15 line 302 | **PASS** | Per-party key isolation foundation for two-signature attack analysis |
| Ch15 §Chain-of-Custody → §GDPR Article 17 and Crypto-Shredding (line 670) | Ch15 line 674 | **PASS** | Erasure / append-only stream tension |
| Ch15 §Chain-of-Custody → App B §Section 5 (line 670, also line 625) | App B line 237 | **PASS** | Sideways operational worksheet |
| Ch15 line 228 (in §48f) → §Chain-of-Custody for Multi-Party Transfers | Ch15 line 583 | **PASS** | Forward-reference update from `(cross-reference #9)` confirmed via grep — 0 hits for `cross-reference #9` or `chain-of-custody mechanism (#9)` remain |
| Ch15 line 389 (in §45f) → §Chain-of-Custody for Multi-Party Transfers | Ch15 line 583 | **PASS** | Forward-reference update from `(#9)` confirmed via grep |
| App B §Section 5 → Ch15 §Chain-of-Custody (line 239) | Ch15 line 583 | **PASS** | Sideways architectural specification back-reference |
| App B §Section 5 → §Collaborator Revocation 45e (line 261) | Ch15 line 362 (`### Sub-pattern 45e — Data partition for dissolution and dispute`) | **PASS** | Departure-partition trigger reference |

All 10 cross-references resolve. The two retroactive-update sites (lines 228 and 389) are confirmed to point to the live section heading via direct grep verification — no stale `(#9)` markers remain in the chapter.

## 5. Citation resolution

In-text citation sites in the new section, each traced both directions:

| In-text site | Ref | Resolves to entry? | Source |
|---|---|---|---|
| Ch15 line 611 §9a | [12] | **PASS** | Yjs Internals (existing, used since #46/#47) |
| Ch15 line 611 §9a | [13] | **PASS** | Loro Common (existing) |
| Ch15 line 621 §9b | [10] | **PASS** | RFC 5280 X.509 (existing) — used for TSA certificate verification chain |
| Ch15 line 621 §9b | [28] | **PASS** | RFC 3161 Time-Stamp Protocol — new at iter-0023, line 779 |
| Ch15 line 621 §9b | [29] | **PASS** | eIDAS Reg. (EU) 910/2014 Art. 41 — new at iter-0023, line 781 |
| Ch15 line 633 §9c | [30] | **PASS** | Crosby & Wallach 2009 — new at iter-0023, line 783 |
| Ch15 line 633 §9c | [31] | **PASS** | RFC 9162 Certificate Transparency v2.0 — new at iter-0023, line 785 |

Reverse direction — every new entry [28]–[31] in the reference list has at least one in-text site:

- [28] cited at line 621
- [29] cited at line 621
- [30] cited at line 633
- [31] cited at line 633

No orphan refs; no broken numbers; no duplicate entries. Numbering jump from existing [27] (last entry from #47) to [28]–[31] is consistent with the user's iter-0023 instruction (next available number).

## 6. Sub-pattern coverage

| Sub-pattern | Section pointer | Coverage status |
|---|---|---|
| 9a — Multi-party signed transfer receipt | Ch15 line 603 (`### Sub-pattern 9a — Multi-party signed transfer receipt`) | **PASS** — receipt structure, two-signature requirement (transferor + recipient device-key signatures over content hash), CRDT version-vector binding via [12][13], `transfer-initiated` → `transfer-completed` → `transfer-disputed` state machine. |
| 9b — Evidence-class temporal attestation via RFC 3161 | Ch15 line 615 (`### Sub-pattern 9b — Evidence-class temporal attestation`) | **PASS** — local-timestamp insufficiency, RFC 3161 [28] TSA integration with TimeStampRequest/TimeStampResponse, eIDAS Art. 41 [29] qualified TSP basis, deployment-class TSA selection, offline `tsa-pending` semantics. |
| 9c — Regulatory-export streaming with verifiable completeness | Ch15 line 627 (`### Sub-pattern 9c — Regulatory-export streaming with verifiable completeness`) | **PASS** — append-only Merkle commitment over event stream [30], CT-v2 web-PKI precedent [31], signed Merkle root export per batch, real-time vs batch modes, distinction from bilateral 9a/9b (unilateral attestation to passive verifier), tension with Article 17 erasure. |

All three required sub-patterns covered to outline §A specification.

## 7. Mandatory artifacts

| Artifact | Status | Location |
|---|---|---|
| HTML annotation header (forward-looking namespace disclosure) | **PASS** | Ch15 line 585: `<!-- code-check annotations: Sunfish.Kernel.Custody (NEW namespace, not in canon — forward-looking); Sunfish.Kernel.Audit (forward-looking from #48). 0 class APIs / method signatures introduced. -->` — same shape as the #46/#47/#48 annotation headers; reviewer-visible; reader-invisible |
| FAILED conditions block | **PASS** | Ch15 lines 649–655 (`### FAILED conditions`); three named conditions with severity classification (architecture / architecture / compliance), each mapped to the sub-pattern it voids |
| Kill trigger | **PASS** | Ch15 line 657: kill trigger sentence preserved verbatim from outline §C — `transfer-completed` without verifiable second signature traceable to recipient's published key |
| App B §Section 5 — 7-field worksheet structure | **PASS** | App B lines 241–298. All seven fields present: (1) Parties — line 241; (2) Data class — line 251; (3) Transfer trigger — line 259; (4) Signing requirements — line 263; (5) Timestamping — line 270; (6) Verification — line 282; (7) Escalation paths — line 288. |
| App B preamble cross-reference back to Ch15 | **PASS** | App B line 239: "Architectural specification: Ch15 §Chain-of-Custody for Multi-Party Transfers." |
| App B closing pointer to `Sunfish.Kernel.Custody` and four event contracts | **PASS** | App B line 300 |

## 8. build/code-check.py output (raw)

```
$ python3 build/code-check.py ch15

Code check: ch15-security-architecture.md
  Code blocks: 1

  ERRORS (3):
    - Unresolved CLAIM marker: <!-- CLAIM: OTR 2004 [19] named forward secrecy explicitly; "post-compromise security" as a named property post-dates OTR (PCS terminology is generally attributed to Cohn-Gordon, Cremers, Garratt c. 2016). The phrase "these properties" therefore overcredits OTR for both. Defer to next-pass copy-edit (precision tightening, not architectural change). -->
    - Unresolved CLAIM marker: <!-- CLAIM: Ch14 §Sync Daemon Protocol does not currently describe attestation validation at the handshake; this section assumes it as a forward dependency. Confirm in Ch14 cross-reference and either back-add or flag as a gap to address with a parallel Ch14 update. -->
    - Unresolved CLAIM marker: <!-- CLAIM: source? — the two-signature receipt construction with TSA anchoring at this granularity is a new architectural commitment from design-decisions §5 #9; v13/v5 reference chain-of-custody only as a forward gap. -->

Exit code: 1
```

Note: the script's `Code blocks: 1` count refers to the single Mermaid `### Key Hierarchy` diagram fence elsewhere in Ch15 (line 56–71) and is unrelated to the new section, which contributes 0 code fences.

**Human-judgment override.**

The script's three CLAIM-marker errors are **expected and accepted** under the loop-plan §5 policy: each is a deliberately-preserved CLAIM marker queued for the technical-review stage (pre-existing markers from #46 line 461 and #47 line 527; new marker from #9 line 621). The loop-plan permits ≤1 CLAIM marker per extension at code-check stage; #9 lands at exactly 1, the existing markers from prior extensions remain pending their respective technical-reviews.

The script does **not** flag the two forward-looking namespaces (`Sunfish.Kernel.Custody`, `Sunfish.Kernel.Audit`) as unknown-package errors because the script's regex (`build/code-check.py` line 72) only checks identifiers wrapped in fenced code blocks; the new section uses inline backticks in prose, which the regex does not trigger on. The HTML annotation header at line 585 is the explicit human-readable disclosure — the same pattern accepted at the #46, #47, and #48 code-checks.

**Override note:** the three CLAIM-marker errors are not blocking for code-check stage advance. The script's exit-1 behavior is by-design strictness for the build pipeline; at the iterative-extension code-check stage, an unresolved CLAIM marker is a *queued item for technical-review*, not a blocker. Verdict reflects this: PASS-with-claim-markers.

## 9. Items queued for technical-review

The following items are accepted for code-check but require @technical-reviewer verification against authoritative sources and v13/v5 / design-decisions §5 #9:

1. **CLAIM marker resolution (Ch15 line 621).** Verify the two-signature transfer-receipt construction with RFC 3161 TSA anchoring against design-decisions §5 #9 and v13/v5. Either retire the marker (if v13/v5 contain a precedent the outline missed) or convert to a `<!-- design-decisions: §5 #9 -->` reference annotation. This is the single new CLAIM marker introduced by #9.

2. **RFC 3161 framing precision.** Verify the §9b description of TimeStampRequest / TimeStampResponse — request contains SHA-256 hash of receipt event; response contains the hash, TSA identity, and certified time bound by the TSA's signature — matches RFC 3161 [28] §2.4 (request format) and §2.4.2 (response format). Confirm the X.509 chain-of-trust verification framing under [10] is RFC 5280 §6.

3. **eIDAS Article 41 framing.** Verify the §9b claim that eIDAS Reg. (EU) 910/2014 Article 41 [29] defines the qualified electronic time stamp and that "qualified trust service provider" is the regulation's correct title for the entity. Confirm the AdES (Advanced Electronic Signature) reference is faithful to the regulation's terminology.

4. **Crosby–Wallach Merkle log construction.** Verify §9c's claim that [30] formalized the append-only Merkle-tree commitment over event streams for tamper-evident logging. Confirm Crosby & Wallach 2009 (USENIX Security pp. 317–334) is the construction referenced and that the §9c framing — running Merkle root, signed export per batch, regulator-side verification of root chain extension — matches their formulation.

5. **Certificate Transparency v2.0 web-PKI standardization.** Verify [31] (RFC 9162) standardizes the Merkle log construction Crosby–Wallach formalized, and that the §9c claim about web-PKI inheritance is correctly attributed.

6. **Yjs and Loro version-vector identification.** Verify §9a's reliance on [12] and [13] for CRDT vector-clock operation-version identification matches the existing book-wide framing of CRDT vector clocks (continued from #46 / #47 usage).

7. **Event contract naming convention alignment.** Confirm `CustodyTransferInitiated`, `CustodyTransferConfirmed`, `CustodyTransferDisputed`, `RegulatoryExportBatch` align with the existing event-contract naming convention in `Sunfish.Kernel.Audit` (#48) and `Sunfish.Kernel.Sync` namespaces (PascalCase event records, past-tense state-change naming for state-transition events; noun-phrase batch naming for stream events).

8. **Sunfish package roadmap promotion.** Promote the `Sunfish.Kernel.Custody` anticipatory entry in `docs/reference-implementation/sunfish-package-roadmap.md` from `Future forward-looking namespaces` to a first-class roadmap entry with status `book-committed`, source extension #9. (Same lift pattern applied to `Sunfish.Foundation.Recovery` and `Sunfish.Kernel.Audit` at #48 technical-review.)

9. **Concept-index extraction.** Generate updates to `docs/reference-implementation/_per-chapter/ch15-security-architecture.yaml` and `appendix-b-threat-model-worksheets.yaml` capturing the new concepts: transfer-receipt primitive, two-signature requirement, RFC 3161 TSA integration, eIDAS qualified TSP basis, Merkle-chain regulatory export, custody-dispute state machine, `tsa-pending` offline state, four `CustodyTransfer*` / `RegulatoryExportBatch` event contracts.

10. **Honesty bound on TSA absence.** Verify §9b's threat-model entry "Deployments without a TSA anchor have no defense against local-clock manipulation, and the compliance posture must declare this honestly." (line 645) is consistent with the book's broader honest-bounds discipline (#47f precedent) and that no softer phrasing should replace it.

11. **Article 17 / Merkle-chain tension framing.** Verify §Implementation surfaces (line 670) framing that Article 17 erasure against an event in a `RegulatoryExportBatch` is resolved through crypto-shredding (destroying the DEK while preserving the structural entry) without breaking the Merkle proof. Confirm the cross-reference to §GDPR Article 17 and Crypto-Shredding is consistent with that section's mechanism description.

## 10. Verdict

**PASS-with-claim-markers.**

- All Sunfish package references are accounted for: 2 forward-looking namespaces, both disclosed in the HTML annotation header per the established #46/#47/#48 pattern.
- 0 code fences, 0 invented APIs, 0 placeholder markers, 0 `<!-- TBD -->` markers.
- 1 new CLAIM marker preserved (within loop-plan ≤1-per-extension policy).
- All 10 cross-references resolve cleanly.
- All 4 new IEEE references [28]–[31] resolve in both directions; reused refs [10], [12], [13] resolve.
- All 3 sub-patterns (9a / 9b / 9c) covered to outline §A specification.
- All mandatory artifacts (HTML annotation / FAILED conditions / kill trigger / 7-field App B worksheet) present at correct locations.

## 11. Gate decision

Code-check → technical-review **PASSES**. Section advances to technical-review with **11 documented items** for the next reviewer (1 CLAIM-marker resolution + 10 verification / promotion / extraction tasks). The forward-looking namespace disclosure pattern is consistent with the precedent established at #46/#47/#48; the human-judgment override on `build/code-check.py`'s strict CLAIM-error exit is documented above.
