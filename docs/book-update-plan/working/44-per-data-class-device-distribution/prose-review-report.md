# Prose Review Report — #44 Per-Data-Class Device-Distribution

**Section:** Ch16 §Per-Data-Class Device-Distribution (lines 132–192)
**Reviewer:** prose-reviewer (iter-0034)
**Date:** 2026-04-28
**Verdict:** PASS — gate prose-review → voice-check

---

## 1. Scope Confirmed

Edits limited to §Per-Data-Class Device-Distribution and reference list entries [1]–[6]. No other Ch16 sections touched. CLAIM marker at L188 preserved verbatim. Cross-reference to Ch21 §21.1 at L172 preserved. HTML annotation at L134 preserved. Kill-trigger sentence at L192 preserved.

## 2. Edits Applied

| Line | Issue | Fix |
|---|---|---|
| L138 | Passive: "device class is set by IT policy" | "where IT policy sets device class independently of the user's role" |
| L142 | Passive: "still be configured to exclude" | "still exclude detailed customer-record classes through its manifest" + tightened follow-on clause |
| L152 | Passive cluster: "is dropped silently", "No error is emitted" | "The send tier drops records of an excluded class silently" / "The filter emits no error" |
| L156 | There-is construction: "Three options exist" | "Three responses are possible" |
| L162 | **Paragraph length cap violation (9 sentences)** | Split into two paragraphs at "The UI layer enforces..." Result: 5 + 3 sentences. Active-voice rewrite of the second half: "are detectable and labeled" → kept (pairs with "not silent" — load-bearing); "are explicitly marked" → "carry explicit marks" |
| L170 | Passive cluster: "are retained as", "is purged", "is logged", "when a record's class is escalated" | "the daemon retains identifiers and metadata as class-excluded placeholders and purges content" / "The daemon logs the eviction" / "when escalation moves a record into a class the device's manifest excludes" |

## 3. Edits Considered but NOT Applied (Preservation Flags Honored)

- **L158 policy-blocked-vs-fetchable boldface contrast** — preserved verbatim. The "fetchable on demand" / "is not" pair is the section's load-bearing novelty against OneDrive/iCloud/Dropbox.
- **L188 forward-secrecy CLAIM marker + body** — preserved verbatim. Hedged language ("may not be able to decrypt") is genuine pending-#46 uncertainty, not default-register hedging. Hedge stays.
- **L192 kill-trigger sentence** — preserved verbatim. Architectural escape hatch.
- **L172 Ch21 cross-reference** — preserved verbatim (recently fixed manually).
- **L134 HTML annotation block** — preserved verbatim.
- **L178 "The architecture's contribution is..."** — copula `is` carrying genuine claim-weight. Anti-AI-tells §8 calibration: flag only when `is`/`has` is dressed up as `serves as`/`represents`/`stands as`. Plain `is` here is correct.
- **L146 "PowerSync's bucket-definition model [5] influenced this shape"** — "influenced" is weak by itself but the sentence completes with a precise inversion ("with one inversion: PowerSync evaluates rules server-side per client parameter; the architecture evaluates the manifest client-side..."). The verb earns its place via the contrast that follows.

## 4. Paragraph-Length Audit (After Edits)

| Para opens with | Sentence count | Status |
|---|---|---|
| "Device fleets in production..." | 4 | OK |
| "The first failure is..." | 7 | At cap+1 — borderline. Each sentence carries a distinct claim (security failure → record-not-on-device principle → storage failure → bucket-model recap → orthogonal-axis claim → MDM distinction). Not flagged: density is intentional for the dual-failure framing. |
| "Each device carries..." | 4 | OK |
| "The manifest is a signed CBOR..." | 3 | OK |
| "A data class is..." | 5 | OK |
| "`Sunfish.Kernel.Sync` on the sending node..." | 3 | OK |
| "The send tier drops..." | 7 | At cap+1 — same density justification (filter behavior → schema declaration → reclassification cross-ref → O(1) cost → ElectricSQL contrast). Not flagged. |
| "A record in class A..." | 2 | OK |
| "The architecture chooses the third." | 4 | OK |
| "This is where consumer-software analogues mislead." | 5 | OK |
| "The class-excluded placeholder differs in kind." | 5 | OK (was 9 before split) |
| "The UI layer enforces..." | 3 | OK (new para from split) |
| "The class-subscription manifest changes by signed update." | 6 | At cap |
| "When a manifest tightens..." | 5 | OK |
| "When a manifest expands..." | 5 | OK |
| "An administrator who cannot verify..." | 3 | OK |
| "`Sunfish.Foundation.Fleet` aggregates..." | 6 | At cap |

Two paragraphs (L138, L152) sit at 7 sentences. Both are dense-by-design specification paragraphs where each sentence introduces a distinct claim. Splitting either would force an artificial heading or a one-sentence orphan. Holding at 7 and flagging here for voice-check awareness rather than forcing a split.

## 5. Synonym-Cycling Check

Single canonical name per concept maintained:
- **manifest** (never "subscription document", "class list", "policy file")
- **class-subscription manifest** when full disambiguation needed
- **placeholder** for the class-excluded marker; **stub** reserved for §Lazy Fetch lazy-evicted records (the contrast is load-bearing at L158)
- **bucket** for §Declarative Sync Buckets unit
- **data class** / **class** for the data-class abstraction
- **attestation** never blurred with **manifest**

No cycling found. The stub-vs-placeholder distinction is preserved as a deliberate two-name contrast, not synonym-cycling.

## 6. Anti-AI-Tells Audit

Patterns checked from `.claude/skills/anti-ai-tells/SKILL.md`:

- §1 significance puffery — none.
- §3 trailing -ing tail-phrases — L160 "leaving applications with broken paths and no semantic signal" — concrete consequences specified, not hand-wave. Not flagged.
- §7 AI vocabulary cluster — no clusters.
- §8 copula avoidance — none. All `is`/`are` used plainly.
- §9 negative parallelisms — L160 "deferred latency, not policy denial" and L162 "not a missing-data error, not a broken link, but a policy-gated boundary" — both carry genuine contrast (the policy-blocked-vs-fetchable distinction). Not flagged.
- §17 title-case headings — all H3s are sentence case ("The class-subscription manifest", "Sync-daemon push filter", "Cross-class references: the policy-blocked placeholder", "MDM-driven manifest update and propagation", "Audit and observability", "Failure modes"). Confirmed.
- §25 generic positive conclusions — section ends on the kill trigger, not optimism.
- §27 persuasive authority tropes — none.
- §29 fragmented headers — every H3 is followed by a substantive opening sentence, not a restatement.

## 7. Voice-Register Confirmation (Part III specification)

Section reads as specification:
- "The send tier drops records of an excluded class silently" — what it does, not what you should do.
- "When a manifest tightens, the sync daemon evicts every record..." — declarative spec.
- "Filter evaluation is O(1) per operation — a hash-set membership check" — concrete cost claim.
- Failure modes named declaratively ("Manifest conflated with attestation") — specification of error conditions, not advice.
- No "you should", no "consider", no tutorial-voice slips.
- No re-introduction of the architecture or local-first concepts.

Confirmed Part III voice.

## 8. Extension-Number Leak Check

Searched for `#44`, `#10`, `#46`, `#48` in user-facing prose: none in body. The CLAIM marker at L188 contains `#46` inside an HTML comment — not user-facing. The L134 HTML annotation contains `#11` — not user-facing. The references list [1]–[6] uses IEEE numerics, not extension numbers.

Confirmed: no leaks.

## 9. Active-Voice Audit (Spot Check After Edits)

Remaining passive constructions kept where the agent is unknown, irrelevant, or where the construction names a state rather than an action:

- L142 "tamper-evident and attributable" — adjective phrase, not passive verb.
- L144 "The manifest travels with the device identity" — active.
- L146 "Every manifest change produces a new signed version retained in the audit log" — "retained" reads as past-participle adjective; rewriting would force "that the audit log retains" which is heavier without clarity gain. Holding.
- L162 "fully verifies all class-A-internal references" — active.
- L176 "Each device maintains" — active. "where each class was acquired or evicted" — passive but listing inventory fields, where the field names are themselves passive labels. Holding.

## 10. Reference List

Entries [1]–[6] not edited. IEEE format compliant. URLs and access dates intact. No prose changes needed.

## 11. Word-Count Impact

Edits are net-neutral to slightly negative (~10–20 words removed via active-voice tightening, +0 from paragraph split). Section remains within tech-review's reported ~1,754 body words ±2%.

## 12. Gate Decision

**PASS — proceed to voice-check (Stage 6).**

Top 3 priorities for voice-check:
1. The two 7-sentence paragraphs (L138 first-failure / L152 push-filter) — confirm density is acceptable for spec voice or split with a connective sentence.
2. L162 paragraph split — confirm the "The UI layer enforces..." opener flows from the rendering example before it without a beat-skip.
3. The "Three responses are possible" rewrite at L156 — confirm reads as crisp setup rather than soft enumeration.

Tone: on-voice. Estimated voice-check time: light.
