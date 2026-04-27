# Code-check report — 45 collaborator revocation

**Stage:** code-check (ICM stage 3).
**Run:** 2026-04-27.
**Verdict:** PASS.

## Sunfish package references

| Namespace | Status |
|---|---|
| `Sunfish.Kernel.Security` | **In canon.** Cited multiple times for revocation broadcast, KEK rotation, post-partition cryptographic separation. |
| `Sunfish.Foundation.Recovery` | **Forward-looking.** Already tracked in `docs/reference-implementation/sunfish-package-roadmap.md` (introduced by #48 ADR 0046). Extended here for successor-entity KEK separation in sub-pattern 45e. |
| `Sunfish.Kernel.Audit` | **Forward-looking.** Already tracked in roadmap (introduced by #48). Extended here for revocation-event records in sub-pattern 45f. |

**No new top-level Sunfish namespace introduced by #45** — the extension is purely additive on existing canon + #48's forward-looking namespaces. The roadmap doc requires no update for #45.

HTML code-check annotations present at start of each new H2 section (Ch15:304 and Ch20:320). All references are package-name only. No class APIs in prose.

## Code snippets

No fenced code blocks introduced by #45. Nothing to mark illustrative.

## Markers

| Type | Count | Notes |
|---|---|---|
| `<!-- TBD -->` | 0 | None. |
| `<!-- CLAIM: -->` | 1 | Sub-pattern 45e: CRDT operation-identifier collision question across Yjs/yrs and Loro after partition. Queued for technical-review. |
| `<!-- voice-check: -->` | 1 | Ch20 §The departure moment: deliberate placeholder for human author to add the connective-tissue scene during voice-check. Not a defect — an intentional structural marker. |
| `TBD` / `TODO` | 0 | None. |

## Cross-reference resolution

All cross-references resolve cleanly:

- Ch15 §Role Attestation Flow ✓ (Ch15:83 area)
- Ch15 §Key Compromise Incident Response ✓
- Ch15 §Key Hierarchy ✓
- Ch15 §GDPR Article 17 and Crypto-Shredding ✓
- Ch15 §Offline Node Revocation and Reconnection ✓ (immediately precedes new section)
- Ch15 §Key-Loss Recovery sub-pattern 48f ✓ (cross-extension reference to #48)
- Ch20 §The Three Always-Visible Indicators ✓ (Ch20:20)
- Ch20 §Designing for Failure Modes ✓ (Ch20:137)
- Primitives #18, #9, #48 — design-decisions §5 references

## Quality gate

Per loop-plan §5: code-check → technical-review.

- [x] All Sunfish package references validated.
- [x] No code snippets present; nothing to mark illustrative.
- [x] No `<!-- TBD -->` markers.
- [x] All cross-reference targets resolve.

Gate **passed**. Advance to technical-review.

## Items queued for technical-review

1. **CRDT operation-identifier collision after partition (sub-pattern 45e CLAIM marker).** Verify against Yjs/yrs and Loro identifier-allocation semantics that two successor logs diverging from a shared history do not collide on future operations because each successor log is sealed under a distinct KEK and operates under new node identifier scopes after partition. This is the structurally-novel part of #45 — no direct prior-art analogue.
2. **OAuth 2.0 Token Revocation citation [8].** Verify RFC 7009 is the right citation for the revocation-event prior-art framing; confirm the architecture's divergence from RFC 7009 (no central authorization server) is stated accurately.
3. **OCSP and CRL precedent citations [9] [10].** Verify RFC 6960 OCSP and RFC 5280 CRL are the right precedents for the AP-not-CP propagation framing.
4. **NIST SP 800-12 citation [11].** Verify the access-termination artifact requirement is stated in NIST SP 800-12 or a closer NIST publication.
5. **v13/v5 sourcing audit.** The closing paragraph of §Why this matters self-discloses the revocation primitive as new architectural commitment ("It does not appear in v13 or v5..."). Verify this self-disclosure is accurate.
6. **Word-count overshoot.** Total new prose is ~4,100 words vs. baseline 2,800 target (overshoot ~46%). 45e's novelty depth justifies extra content but prose-review may want to trim repetition.

Word counts (approximate, body prose only):
- Ch15 §Collaborator Revocation and Post-Departure Partition: ~3,100 words (baseline 2,000; +55%)
- Ch20 §Revocation UX: ~1,000 words (baseline 800; +25%)
- Total: ~4,100 words (baseline 2,800; +46%)

The overshoot is concentrated in 45e (~600 words for a sub-pattern targeted at ~400). Acceptable given novelty; prose-review pass may trim.
