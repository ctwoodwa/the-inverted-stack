# Prose-Review Report — #48 Key-Loss Recovery

**Chapters reviewed:** Ch15 §Key-Loss Recovery; Ch20 §Key-Loss Recovery UX
**ICM stage:** icm/prose-review
**Date:** 2026-04-26
**Reviewer:** @prose-reviewer

---

## Fixes Applied

### Ch15 §Key-Loss Recovery

**1. Academic scaffolding — line 131**
- **Before:** "Those policies determine who is authorized to invoke recovery and under what conditions; this section describes the cryptographic constructions that implement the authorization."
- **After:** "Those policies determine who is authorized to invoke recovery and under what conditions; the six mechanisms below implement the authorization cryptographically."
- **Category:** academic scaffolding ("this section describes")

**2. Passive voice — line 175**
- **Before:** "The construction is simple: when a recovery claim is submitted, the system broadcasts the claim to the original holder's existing devices and to designated trustees."
- **After:** "The construction is simple: when the user submits a recovery claim, the system broadcasts it to the original holder's existing devices and to designated trustees."
- **Category:** active-voice conversion (agent: the user)

---

### Ch20 §Key-Loss Recovery UX

**3. Academic scaffolding — line 182–183**
- **Before:** "This section covers what the user sees: the flows that surface the policy at setup time, the experience of initiating recovery after loss, and the UX for the grace period that protects against fraudulent claims."
- **After:** "This section covers the flows that surface that policy at setup time, the experience of initiating recovery after loss, and the UX for the grace period that protects against fraudulent claims."
- **Category:** academic scaffolding ("This section covers what the user sees"). Note: the phrase "what the user sees" is not merely redundant — it duplicates the chapter's stated purpose. The rewrite removes the meta-commentary wrapper while preserving the enumeration.

**4. Passive participial — line 189**
- **Before:** "It is not an optional step presented to advanced users."
- **After:** "It is not an optional step reserved for advanced users."
- **Category:** passive participial → precise active participial. "Presented to" implies delivery by an unnamed agent; "reserved for" is a property of the step itself and requires no agent.

**5. Passive voice — line 204**
- **Before:** "An arrangement with fewer than the threshold confirmed is flagged: 'You need at least 3 confirmed trustees…'"
- **After:** "The application flags an arrangement with fewer than the threshold confirmed: 'You need at least 3 confirmed trustees…'"
- **Category:** active-voice conversion (agent: the application)

**6. Passive voice — line 218**
- **Before:** "The original holder's existing devices — every device associated with the account — receive a high-priority notification the moment a recovery claim is submitted: 'Someone is requesting recovery of your account.'"
- **After:** "The original holder's existing devices — every device associated with the account — receive a high-priority notification the moment the user submits a recovery claim: 'Someone is requesting recovery of your account.'"
- **Category:** active-voice conversion (agent: the user)

**7. Passive construction — line 222**
- **Before:** "A recovery claim sent only through email is defeatable by an adversary who controls the user's email account."
- **After:** "Routing recovery claims through a single channel is defeatable by an adversary who controls that channel."
- **Category:** active-voice conversion; additionally generalizes the single-channel claim (not email-specific) which is a precision improvement consistent with the preceding sentence's emphasis on multi-channel.

---

## Anti-AI Tells Calibration

**Em-dashes:** preserved throughout both sections. Ch15 uses em-dash apposition extensively (e.g., "The P7 ownership property — that users hold the keys to their own data — is not a defect-free guarantee"). All intentional rhythm devices. Not flagged.

**Boldface:** used for the bold-header pattern inside the six-mechanism subsections (e.g., `**Envelope encryption mechanics.**`, `**Trustee compromise.**`). This is the vocabulary-installation pattern the book uses deliberately. Not flagged.

**Hyphenated technical terms:** "multi-sig", "time-locked", "key-loss", "first-run", "local-first", "end-to-end" — all correctly hyphenated technical terms. Not flagged.

**Significance puffery scan:** No instances of "pivotal", "crucial", "tapestry", "delve", "stands as a testament", "evolving landscape" found in either new section.

**AI vocabulary cluster scan:** No cluster instances. "Crucial" does not appear in the new sections; neither does "showcase", "underscore", "foster", "garner". One instance of "additional" (line 179 of Ch15: "the holder has additional channels") — legitimate adjective, not AI puffery.

**Copula avoidance scan:** No "serves as", "stands as", "represents a", "marks a" constructions in the new sections.

**Persuasive authority tropes:** No "at its core", "the real question is", "what really matters", "fundamentally" found.

**Superficial -ing tails:** One candidate in Ch15 line 154: "The deployment cost reflects the custodian relationship: contract negotiation, enrollment, and annual audit." — not a trailing -ing clause; this is a legitimate colon-list construction. No trailing "-ing" clauses of the LLM-signature type found in either section.

**Signposting (Pattern 28):** None found.

**Fragmented header (Pattern 29):** Borderline instance at Ch15 §Threat Model — Recovery as Attack Vector, line 195: "Four specific attack patterns define the threat model for recovery operations." — This sentence follows the H3 heading and partially restates it. However, it also adds the count ("four") and the narrowed scope ("for recovery operations"), which carries information the heading does not. Judgment call: left in place. The sentence that follows ("Recovery primitives are attack surfaces…") opens with substantive content; the count sentence is a short bridge, not a full restatement.

**Collaborative artifacts:** Zero instances.

---

## Paragraph Length Cap

All paragraphs in both new sections were counted. None exceeds 6 sentences.

The longest paragraphs:
- Ch15 §Multi-sig social recovery opening paragraph: 5 sentences (line 137–139 block).
- Ch15 §Timed recovery with grace period opening paragraph: 6 sentences (line 175–176 block). At the cap; not over.
- Ch15 §Trustee compromise (threat model): 5 sentences.

No splits required.

---

## §A.5 ("What This Section Does Not Solve") — Honesty Verification

Per outline §E, this subsection is intentionally direct and must not be softened.

Review confirms:
- "A user who skips recovery setup at first-run and then loses their key loses their data." — direct.
- "The architecture presents the choice and documents the consequence. It cannot force the choice." — direct.
- "The architecture cannot grade trustee selection or predict trustee availability over time." — direct.
- "The architecture cannot prevent a pre-arrangement from decaying." — direct.
- "The book cannot substitute for the check." — direct.

No softening applied. This subsection is correct as written.

---

## Synonym Cycling Check

| Concept | Names used | Status |
|---|---|---|
| trustee | "trustee" throughout | Consistent |
| grace period | "grace period" throughout (never "waiting period", "dispute window" as a synonym) | Consistent |
| recovery key | "root recovery key" / "recovery key" / "wrapped recovery key" — these are structurally distinct (the unwrapped key, the wrapped copy, the full path); the distinction is intentional | Not cycling |
| the mechanisms | "mechanisms" and "sub-patterns" used — these are genuinely different referents (mechanism = functional concept; sub-pattern = catalog ID) | Not cycling |
| audit trail | "audit trail", "audit log", "signed audit log" — slight variation; "audit trail" and "audit log" are used interchangeably once in Ch15 | Borderline. Both forms appear within the same subsection (§Recovery-event audit trail). Recommend standardizing to "audit trail" throughout to match the subsection title and the §A.5 usage — but this is a light flag, not a blocking issue. |

---

## Part-Specific Checks

### Ch15 (Part III — specification register)

- Third-person throughout. No "you" in the new section. Correct.
- Direct address used only in the table discussion paragraphs ("Three-of-five social recovery tolerates…") — these are in-register for specification prose describing deployment recommendations.
- "The system does X" framing maintained throughout.
- No "you should" constructions found.

### Ch20 (Part IV — tutorial register)

- "You" used appropriately and consistently in imperative/tutorial positions.
- Action-oriented sentences throughout.
- Concrete UI copy in quoted form: "I understand that without recovery setup, I cannot recover my data if I lose access to this device." — correct format.
- Cross-references to Ch15 present and correctly placed.
- No re-explanation of Part I concepts found.

---

## Re-introduction Check

Both sections assume Part I and earlier Ch15 is read. No re-explanation of what a local node is, what the CRDT engine does, or what the relay is. The P7 property is named and briefly glossed ("users hold the keys to their own data") — this is the first appearance of P7 in this specific section context and earns its brief gloss. Not a re-introduction.

---

## QC Checklist (CLAUDE.md QC-1 through QC-10)

| Check | Status | Notes |
|---|---|---|
| QC-1 Word count within ±10% | Pass | Ch15 section ~2,050 words (target 2,000); Ch20 section ~1,040 words (target 1,000) |
| QC-2 Topics in book-structure.md addressed | Pass | Six mechanisms, threat model, deployment combinations, §A.5 limitations — all present |
| QC-3 Source sections cited inline | Pass | Citations [4]–[7] present; cross-references to companion sections present |
| QC-4 Sunfish packages by name only | Pass | `Sunfish.Foundation.Recovery`, `Sunfish.Kernel.Security`, `Sunfish.Kernel.Audit` — no class APIs or method signatures |
| QC-5 No academic scaffolding | Pass (after edits) | Two instances fixed |
| QC-6 No re-introducing the architecture | Pass | No Part I re-explanation |
| QC-7 Part III spec voice / Part IV tutorial voice | Pass | Ch15: third-person specification; Ch20: second-person tutorial with concrete UI copy |
| QC-8 Ch 2 only | N/A | Not Ch2 |
| QC-9 Council chapters two-act structure | N/A | Not a council chapter |
| QC-10 No placeholder text | Pass | No "TBD", "expand here", "see paper for details" |

---

## Verdict

**Gate: PASS**

Seven edits applied across two files: 2 in Ch15, 5 in Ch20. Categories: academic scaffolding (2), active-voice conversion (4), passive participial (1). No paragraph splits required; no synonym-cycling fixes required beyond the light audit-trail note above. Anti-AI tells calibrated correctly — em-dashes, boldface, and hyphenated technical terms preserved; no LLM-signature vocabulary found in either new section. §A.5 honesty preserved. Both sections are ready for the voice-check gate.
