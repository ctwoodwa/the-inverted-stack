# Prose-Review Report — #45 Collaborator Revocation and Post-Departure Partition

**Stage:** prose-review (ICM stage 5).
**Run:** 2026-04-27.
**Reviewer:** prose-reviewer subagent.
**Scope:** new sections only.
- Ch15 §Collaborator Revocation and Post-Departure Partition (lines 302–399 after edits).
- Ch20 §Revocation UX (lines 318–352 after edits).

---

## Edit summary

**Total edits applied:** 14 (11 in Ch15, 3 in Ch20).
**Edit categories:**
- Active-voice conversions (passive → active): 7
- Intransitive-passive verb fixes ("publishes", "generate", "re-encrypts" used intransitively): 4
- Paragraph-length splits (>6 sentences): 3
- Logical correction (FAILED-conditions lead-in inverted truth direction): 1
- Awkward phrasing tightenings: 2

The §B.4 "departure moment" placeholder paragraph and its `<!-- voice-check: -->` HTML comment were preserved untouched per scope.

---

## Edits applied — Ch15

### Active-voice conversions

**Line 320 (sub-pattern 45a — three-purpose enumeration).**
Before: "It is observable by all peers that must stop accepting writes from the revoked party. It is the timestamp anchor for the data-at-risk window in sub-pattern 45f. It is the entry in the audit trail that proves when access ended."
After: "All peers observe it and stop accepting writes from the revoked party. It anchors the timestamp for the data-at-risk window in sub-pattern 45f. It records the audit-trail entry that proves when access ended."
Reason: First sentence used passive voice ("is observable by") with an obvious agent. Other two clauses retained as definitional copulas (deliberate parallelism for the three-purpose list), but converted from "is the X" to verb-led "anchors / records" to remove copula-avoidance pattern (anti-ai-tells §8) without losing parallel rhythm.

**Line 330 (sub-pattern 45b — procedure introduction).**
Before: "the new KEK is generated before the revoked collaborator is notified, and the revoked party is excluded from the new bundle set from the first publication."
After: "the administrator generates the new KEK before notifying the revoked collaborator, and excludes the revoked party from the new bundle set from the first publication."
Reason: Three passive constructions with obvious agent (administrator, named two clauses earlier). Active voice removes hedge.

**Line 334 (sub-pattern 45b — step 3).**
Before: "The revocation event from sub-pattern 45a and the new key bundle publish simultaneously as administrative events in the encrypted log."
After: "The administrator publishes the revocation event from sub-pattern 45a and the new key bundle simultaneously as administrative events in the encrypted log."
Reason: "publish" used intransitively (non-standard English; events do not publish themselves). Promoted explicit agent.

**Line 336 (sub-pattern 45b — step 5).**
Before: "The old KEK is discarded after all authorized members confirm receipt of the new bundle."
After: "`Sunfish.Kernel.Security` discards the old KEK after all authorized members confirm receipt of the new bundle."
Reason: Passive with obvious agent. Named the responsible namespace, consistent with line 340's existing summary that `Sunfish.Kernel.Security` "manages... the discard broadcast."

**Line 360 (sub-pattern 45d — closing sentence).**
Before: "The partition case where a revoked collaborator sends a write to an offline peer before that peer learns of the revocation is handled by the circuit breaker on reconnection: quarantine, not silent promotion."
After: "The circuit breaker on reconnection handles the partition case where a revoked collaborator sends a write to an offline peer before that peer learns of the revocation: quarantine, not silent promotion."
Reason: "is handled by" passive with named agent. Promoted subject.

**Line 371 (sub-pattern 45e — step 2).**
Before: "A partition event publishes to the encrypted log, signed by the authorizing party (administrator, legal trustee, or both parties together)."
After: "The authorizing party (administrator, legal trustee, or both parties together) publishes a partition event to the encrypted log under their signature."
Reason: Same intransitive-publish error as line 334. Promoted explicit agent.

**Line 373 (sub-pattern 45e — step 4).**
Before: "New KEKs generate for each successor entity. Each party's successor log re-encrypts under their new KEK."
After: "`Sunfish.Foundation.Recovery` generates a fresh KEK for each successor entity. Each party re-encrypts their successor log under that new KEK."
Reason: Both verbs ("generate", "re-encrypts") used intransitively without agents — keys do not generate themselves; logs do not re-encrypt themselves. Named the responsible namespace and the human actor.

**Line 385 (sub-pattern 45f — opening).**
Before: "Every revocation event, every key rotation triggered by revocation, every partition authorization, and every revocation dispute is recorded as a signed event in the encrypted audit log. `Sunfish.Kernel.Audit` manages revocation-event records."
After: "`Sunfish.Kernel.Audit` records every revocation event, every key rotation triggered by revocation, every partition authorization, and every revocation dispute as a signed entry in the encrypted audit log."
Reason: Combined a passive + a redundant restatement. The original two sentences both said the same thing twice ("is recorded" + "manages revocation-event records"). Single active sentence is cleaner.

**Line 389 (sub-pattern 45f — middle paragraph).**
Before: "it documents when the former employee's data access was terminated."
After: "it documents when the deployment terminated the former employee's data access."
Reason: Passive with implicit agent. Active form is more specific about who terminated.

### Paragraph-length splits

**Line 364 (sub-pattern 45e — opening paragraph, 7 sentences).**
Split between the regulated-entity scenario (sentence 6) and the "Each scenario is structurally novel..." synthesis (sentence 7). The split also better isolates the "no direct OAuth/OCSP/CRL prior-art analogue" framing that outline §E flagged as structurally novel and worth protecting — it now lives in its own paragraph rather than buried at the end of a long enumeration.

**Line 377 (sub-pattern 45e — CRDT verification paragraph, 8 sentences).**
Split between the engine-citation sentences (Yjs + Loro identifier shapes [12] [13]) and the two-properties argument that follows. The split makes the proof structure visible: paragraph 1 names the source material; paragraph 2 names the architectural mechanism. The technical-review report's verification paragraph now reads as two paragraphs of equal weight rather than one block.

**Line 336 (Ch20 §Communicating the action's effects, 7 sentences).**
Split between the "They see the access status." line and the cross-reference to Three Always-Visible Indicators / Designing for Failure Modes. The cross-reference is structurally a different beat (forward pointer) and reads more cleanly as its own paragraph.

### Logical correction

**Line 393 (Ch15 FAILED conditions block lead-in).**
Before: "The revocation primitive holds when these conditions are met. Any condition below failing voids the primitive's guarantees."
After: "The revocation primitive fails when any of the conditions below holds. Any one of them voids the primitive's guarantees."
Reason: The original lead-in inverted the FAILED-conditions semantics — the bullets describe failure modes, so they are conditions to be **avoided**, not "met." Reading the original literally meant the primitive holds when its failure modes hold. Corrected to standard FAILED-conditions block phrasing matching extension #43's treatment.

### Tightenings

**Line 377 (sub-pattern 45e — closing of legal-layer paragraph).**
Before: "Bilateral data partition with successor-entity key separation is the architectural commitment this section makes new."
After: "Bilateral data partition with successor-entity key separation is this section's new architectural commitment."
Reason: "makes new" reads as awkward verbification. Possessive form is cleaner and equally precise.

**Line 381 (sub-pattern 45e — CRDT proof, second paragraph).**
Before: "operations from one log are never integrated into the other"; "the same physical device is later associated with both successor entities"
After: "operations from one log never integrate into the other"; "the same physical device later associates with both successor entities"
Reason: Two passives in one paragraph where the active reading is sharper. Minor but consistent with active-voice pass.

---

## Edits applied — Ch20

### Active-voice conversion

**Line 322 (Revocation UX — opening).**
Before: "Revocation has a policy layer and a UX layer, paired by design."
After: "Revocation pairs a policy layer with a UX layer by design."
Reason: "paired by design" is a passive participle phrase. Active form uses revocation as the subject and pairs as the verb.

### Paragraph-length split

**Line 336 (Communicating the action's effects — second paragraph).**
Documented above under Ch15 splits.

### Awkward intransitive-passive fix

**Line 336 (mid-paragraph).**
Before: "Active edits in progress preserve in the local CRDT log; they cannot submit to shared state."
After: "The local CRDT log retains active edits in progress; they do not reach shared state."
Reason: "preserve" used intransitively (edits do not preserve themselves) and "submit" used intransitively in the second clause (edits do not submit themselves). Promoted "the local CRDT log" as agent for the first clause; replaced the second clause with a state assertion that is grammatically clean.

---

## Anti-AI tells calibration

A targeted scan against `.claude/skills/anti-ai-tells/SKILL.md` patterns. Patterns 14 (em-dash), 15 (boldface), 26 (hyphenated terms) are explicitly NOT applied per house calibration.

| Pattern | Status in section | Notes |
|---|---|---|
| §1 Significance / legacy puffery | CLEAN | No "stands as testament", "pivotal moment", "evolving landscape" |
| §3 Superficial -ing tail-phrases | CLEAN | No trailing "highlighting…", "underscoring…", "ensuring…" |
| §5 Vague attributions | CLEAN | All claims attributed to specific RFCs (7009, 6960, 5280), specific NIST publications (SP 800-12), or named architectural commitments |
| §7 AI vocabulary cluster | CLEAN | No "delve", "showcase", "tapestry", "intricate", "vibrant", "enduring" cluster. "crucial" appears zero times in either section. |
| §8 Copula avoidance | RESOLVED | "It is observable" → "All peers observe it" (line 320); other "is the X" definitional copulas retained where parallelism justifies them; intransitive-passive verbs ("publish", "generate", "re-encrypt", "preserve", "submit") all promoted to active. |
| §9 Negative parallelisms | CLEAN | No "not only X but also Y" |
| §16 Inline-header vertical lists | DELIBERATE | Lines 348-350 use `**Write quarantine.**` and `**Forward isolation.**` as named architectural sub-controls within sub-pattern 45c — this is correct named-pattern usage (each phrase is a defined control name), not glossary-style decoration. Retained. |
| §17 Title case in headings | CONSISTENT | H2 "Collaborator Revocation and Post-Departure Partition" matches existing chapter convention ("Offline Node Revocation and Reconnection", "In-Memory Key Handling"); H3 sub-pattern headers use sentence-case ("Sub-pattern 45a — Explicit revocation event"). |
| §25 Generic positive conclusions | CLEAN | Sub-pattern 45f closes on a specific claim ("the access-termination artifact those frameworks require"); FAILED conditions block closes on a kill-trigger definition. No vague optimism. |
| §27 Persuasive authority tropes | CLEAN | No "the real question is", "at its core", "fundamentally", "what really matters" |
| §29 Fragmented headers | CLEAN | No heading is followed by a one-line restatement of itself; first paragraph after each H3 is substance. |

The "structurally novel relative to OAuth/OCSP/CRL prior art" framing in sub-pattern 45e is the legitimate kind of significance claim — it is precise (names the three specific prior-art mechanisms it diverges from), earned (the technical-review report verifies the divergence claim), and load-bearing for the architecture's novelty argument. It does **not** fall under §1 puffery and was preserved per outline §E.

---

## Paragraph length confirmation

After the three splits applied above, every paragraph in both sections is at or below the 6-sentence cap.

**Ch15 §Collaborator Revocation and Post-Departure Partition** — paragraph counts after edits:
- Why this matters: 1 + 5 + 4 + 5 = all under cap.
- Sub-pattern 45a: 2 + 3 + 3 + 2 = all under cap.
- Sub-pattern 45b: 3 + 2 + step list + 3 + 4 = all under cap.
- Sub-pattern 45c: 3 + 1 + 3 (write quarantine) + 2 (forward isolation) + 4 = all under cap.
- Sub-pattern 45d: 2 + 4 + 5 = all under cap.
- Sub-pattern 45e: 6 + 1 + step list + 5 + 4 + 3 + 5 = all under cap (was 7 and 8 before splits).
- Sub-pattern 45f: 1 + 2 + 5 = all under cap.
- FAILED conditions: 2 + 3 bullets + 2 = all under cap.

**Ch20 §Revocation UX** — paragraph counts after edits:
- Opening: 4 sentences.
- Initiating revocation: 6 + 4 + 2 = all at or under cap.
- Communicating the action's effects: 6 + 6 + 1 = all at or under cap (was 7 in second paragraph before split).
- Partition wizard: 3 + 5 + 5 = all under cap.
- The departure moment: 4 sentences (placeholder paragraph; not modified).

---

## Synonym-cycling check

The book's revocation vocabulary stays disciplined. Confirmed by reading every occurrence:

- "revocation" appears throughout — never replaced with "termination", "withdrawal", or "removal" (one exception: "grant termination" in line 318 as a definitional gloss for what revocation **is** cryptographically; the surrounding paragraphs continue to use "revocation"). One sentence in line 389 uses "terminated the former employee's data access" — this is the access-termination compliance term of art, matching NIST SP 800-12 and the §A.7 audit-trail framing. Acceptable in context.
- "partition" stays "partition" — never "split", "separation", "fork" (except where "fork" is used precisely once in the architectural sense at line 368: "with each holding a controlled fork", which is the standard CRDT-divergence term).
- "collaborator" stays "collaborator" / "revoked collaborator" — never "user", "member" (except where "member" is the role-bundle term in sub-pattern 45b, which is established v13 vocabulary).
- "audit trail" stays "audit trail" — never "log", "record" alone, or "history".

No synonym cycling detected.

---

## "There is" / "There are" check

Confirmed: zero "there is" / "there are" constructions in either section after edits. The architecture description uses promoted-subject phrasing throughout ("no central authorization server exists", "All peers observe it", "The local CRDT log retains").

---

## Part-specific voice tests

**Ch15 — Part III specification register.**
- No second-person address: PASS (every "you" verified absent).
- No hedging on revocation guarantees: PASS. The architecture's honest-boundary claims ("does not and cannot delete data from a remote device", line 352) are direct declarative statements rather than hedges.
- Positive declarative throughout: PASS.
- Specification voice ("it does X") not tutorial voice ("you should do X"): PASS.

**Ch20 — Part IV tutorial register.**
- Direct second-person on administrator flows: PASS ("You select the departing collaborator", "You do not need to understand the cryptographic mechanism", "The wizard walks you through three steps").
- Plain-language UI copy in quotes: PASS (every quoted message uses non-technical vocabulary).
- Explicit "do not" instructions: PASS ("Do not surface technical key-rotation terminology", "The message does not imply their local copy has been deleted").

---

## What was preserved untouched

- The "no direct OAuth/OCSP/CRL prior-art analogue" framing at line 366 (per outline §E request to protect specificity).
- The §B.4 "departure moment" paragraph at Ch20 line 350 and its `<!-- voice-check: -->` HTML comment at line 352.
- All citation numbers [8]–[13].
- All cross-references (§Role Attestation Flow, §Offline Node Revocation and Reconnection, §Key Compromise Incident Response, §Key Hierarchy, §Key-Loss Recovery sub-pattern 48f, §GDPR Article 17 and Crypto-Shredding, #9 chain-of-custody, #18 delegated capability).
- The FAILED conditions block's three-bullet structure and per-bullet labels (Architecture failure / Protocol failure / Compliance failure).
- The kill-trigger sentence structure that mirrors extension #43.
- The HTML code-check annotations at the top of each section.
- Title-case H2 headings (consistent with rest of chapter file conventions).

---

## Verdict

**Prose-review → voice-check gate:** **PASS**.

All scope items resolved:
1. Active voice — 7 explicit conversions; 4 intransitive-passive fixes.
2. Hedging — zero hedge words detected; no "could potentially", "might be", "tends to" in either section.
3. Academic scaffolding — zero "this section presents", "as we have seen" instances.
4. Paragraph length cap — every paragraph at or under 6 sentences after 3 splits.
5. Synonym cycling — confirmed clean across all key concepts.
6. "There is" / "There are" — zero occurrences.
7. Anti-AI tells calibration — em-dashes / boldface / hyphenated terms preserved per house style; copula-avoidance and intransitive-passive patterns scrubbed.
8. Sub-pattern 45e specificity — "no direct OAuth/OCSP/CRL prior-art analogue" framing preserved; the dissolution scenario's structural novelty is now isolated in its own paragraph after the line 364 split, making the claim more visible rather than less.
9. Departure-moment paragraph and `<!-- voice-check: -->` placeholder — untouched.

**Advance to voice-check (ICM stage 6 — human only).**
