# Prose-Review Report — #11 Fleet Management (Ch21)

**Chapter:** `chapters/part-5-operational-concerns/ch21-operating-a-fleet.md`
**Stage:** `icm/draft` → `icm/prose-review`
**Voice register:** Hybrid spec/tutorial leaning Ch19. Direct second-person for operational instructions; declarative for primitive definitions.
**Verdict:** PASS (with edits applied in place).

---

## Summary

The draft arrived in solid shape. Lexical AI-tells were already absent — zero hits across patterns 1, 4, 7, 8, 9, 12, 27, 28 (significance puffery, promotional vocabulary, AI vocabulary, copula avoidance, negative parallelisms, false ranges, persuasive authority tropes, signposting). The opening framing landed hard. The §21.6 fleet-failure narrative voice was already on-register.

The dominant issue was paragraph length. Eight paragraphs exceeded the 6-sentence cap, several at 7–10 sentences. Most over-long paragraphs covered two distinct topics that could split cleanly at a topic shift without rewrite. A small number of passive constructions and one minor weasel-phrase (`at any later moment`) were corrected. The narrative scene in §21.6 was preserved in voice — paragraph splits there honor topic shifts within the past-tense scene, not register changes.

Total edits: 14, across paragraph splits, passive-voice tightening, and one weasel-phrase trim.

---

## Findings

### PARAGRAPH LENGTH (8 flags — all fixed by splitting)

- **Para starting "A fleet of local-first nodes removes…"** (line 16) — 7 sentences. Split after the construction-deployment frame; the rhetorical "Sites go through excavation phases…" tetracolon now opens its own paragraph and lands harder.
- **Para starting "The shift from Chapter 17's…"** (line 24) — 7 sentences. Split after "It is a mental-model shift." so the two short rhetorical sentences ("Nodes are no longer people…") land as a stand-alone beat.
- **Para starting "The four dimensions are not arbitrary…"** (line 187) — 8 sentences. Split after the four dimensional-question lines so the concluding claim opens its own paragraph.
- **Para starting "Aggregation matters as much as per-node detail…"** (line 189) — 8 sentences. Split after "The aggregation surfaces the systemic signal…" so the citation/precedent attribution stands separately.
- **Para starting "For regulated-tier fleets…"** (line 191) — 7 sentences. Split after "an immutable record of the fleet's posture at the moment of the export." so the SOC 2 scoping discussion opens its own paragraph.
- **Para starting "Wednesday morning, the propagation deadline passed…"** (line 219) — 8 sentences. Narrative scene; split after the dashboard transition so the operator's reaction stands alone.
- **Para starting "Thirty days after the original rotation announcement…"** (line 223) — 7 sentences. Narrative scene; split after the audit-log entry so the field-technician resolution opens its own beat.
- **Para starting "What would have happened without fleet management…"** (line 227) — 10 sentences (the longest in the chapter). Narrative counter-factual; split twice — after "No audit trail." and after "The investigation would have taken days." — so the scene's three rhetorical movements (no-mechanism / discovery-by-helpdesk / ambiguous-compliance) each land separately.

### ACTIVE VOICE (3 flags — all fixed)

- **Line 38** (now in §21.1 "responsibilities" para): `**Provisioning** is the mechanism by which a new node is initialised with its identity, keys…` → `**Provisioning** initialises a new node with its identity, keys…`. Tighter, active, no information lost.
- **Line 40**: `Each responsibility is defined by the silent failure mode it eliminates.` → `Each responsibility names the silent failure mode it eliminates.` Active, and the verb (`names`) is more specific than the passive `defined`.
- **Line 181**: `A heartbeat that fails signature verification is discarded by the fleet registry and surfaces as an integrity-failure alert.` → `The fleet registry discards any heartbeat that fails signature verification and surfaces it as an integrity-failure alert.` Active subject; same content.

### WEAK PHRASING / WEASEL (2 flags — fixed)

- **Line 16**: `is a useful frame` → `is the frame for this chapter`. Removes soft-pedal modifier.
- **Line 62**: `the operator cannot tell — at any later moment — which keys came from where` → `the operator cannot tell, after the fact, which keys came from where`. `At any later moment` was redundant filler; the simpler `after the fact` is sharper.

### PART-SPECIFIC FLAGS (1 advisory — left as-is)

- §21.6 narrative voice: confirmed past-tense scene voice throughout. Splits applied above honor topic shifts within the scene; no register conversion to specification voice. The "What would have happened without fleet management" counter-factual remains a counter-factual paragraph, now split at its three natural rhetorical beats.

---

## Patterns checked, zero hits

- Significance / legacy puffery (anti-ai-tells §1) — clean.
- Copula avoidance (§8) — clean. The chapter uses `is`/`are`/`has` directly.
- Superficial -ing tail-phrases (§3) — clean.
- AI vocabulary cluster (§7) — clean.
- Persuasive authority tropes (§27) — clean.
- Signposting / chatty announcements (§28) — clean.
- Negative parallelisms (§9) — clean.
- Vague attributions (§5) — clean (every claim cites or names its source).
- Generic positive conclusions (§25) — clean. The chapter closes on a specific architectural claim ("Part IV teaches you to ship. Part V teaches you to sustain.") rather than vague optimism.
- Fragmented headers (§29) — clean. Every H2 opens directly into substance.
- Title case in headings (§17) — clean. Sentence case throughout.
- Inline-header vertical lists (§16) — used appropriately for the three provisioning models, three escalation levels, three rollout phases, four heartbeat dimensions, five dashboard states. Each is a genuine reference list, not prose disguised as bullets. Calibration says this format is correct here.
- "There is" / "There are" constructions — clean.
- Synonym cycling on "fleet" — clean. "Fleet" is used consistently; "deployment" appears only in compounds like "fleet deployment" or "deployment plan" where it carries a distinct meaning.
- Hedging on operational claims — clean. "Fleet management converts silent failures into observable events" lands as a definite claim everywhere it appears. Calibration values (`72 hours`, `30 days`, `5 minutes`, `1–5%`) are stated as defaults, not approximated.
- Re-introducing the architecture — clean. The chapter assumes Part I is read.
- FAILED conditions block — formatted correctly; left untouched per scope.
- Code fences and `// illustrative` markers — left untouched per scope.

---

## Overall assessment

- **Tone:** on-voice. Hybrid spec/tutorial register matches Ch19 closely. Direct second-person ("Configure the propagation window…", "Specify it once, specify it correctly…") for operational decisions; declarative for primitive definitions.
- **Estimated revision time:** light. Eight paragraph splits and three small phrasing tightens.
- **Top 3 edits applied:**
  1. Split four over-long paragraphs in the spec sections (§21.1, §21.5).
  2. Split three over-long paragraphs in the §21.6 narrative scene at topic shifts, preserving past-tense scene voice.
  3. Tightened three passive constructions and one weasel-phrase (`at any later moment` → `after the fact`).

**Gate verdict:** PASS. Chapter advances `icm/draft` → `icm/prose-review` complete.
