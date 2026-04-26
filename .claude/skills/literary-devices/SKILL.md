---
name: literary-devices
description: Curated reference of rhetorical and literary devices — anaphora, chiasmus, antimetabole, asyndeton, polysyndeton, tricolon, antithesis, metonymy, prolepsis, anadiplosis, and ~30 more — with definitions, the cognitive function each performs, and worked examples in The Inverted Stack's register. Use this whenever drafting, revising, or reviewing prose where rhythm, emphasis, cadence, persuasive force, or named devices matter — chapter drafts, prose-review passes, voice-agent rewrites, and any moment a paragraph "feels flat," "lands soft," or "needs to punch harder." Voice-* agents and the prose-reviewer should consult this skill before applying intentional rhetorical structure. Use even when the user does not name a device by name — if the task involves making prose more rhythmic, more memorable, or more persuasive, this skill applies.
---

# Literary Devices — Reference for Persuasive Technical Prose

## Why this skill exists

Most prose problems in this book are not vocabulary problems. They are *structural* problems at the sentence level: a claim is correct but unmemorable; a paragraph reasons but does not land; a section persuades the head but not the gut. Named rhetorical devices are the levers that turn correct-but-flat prose into prose a reader carries around for a week.

This skill gives you a working vocabulary of those levers, with examples already in the book's register so you can reach for the right one without translating.

## When to consult this skill

Reach for it when:

- A passage in any chapter "reads correctly but doesn't land" — the reasoning is sound but the rhythm is dead.
- A section needs to *open* with force (Part I, Council chapters, Epilogue).
- A counter-argument needs to be acknowledged without being conceded (any chapter that pushes against SaaS orthodoxy).
- Voice agents (sinek, godin, brown, gladwell, grant, lencioni) are reaching for a named device and want a consistent house example.
- Prose-review surfaces a paragraph that drags, repeats, or reasons in a flat monotone.
- A claim is true and important but the reader will forget it by the next page.

## When to skip this skill

Skip it when the work is:

- **Pure specification.** Part III voice is "what it is, how it works fully" — clarity beats cadence. A device that adds rhythm at the cost of precision is a regression.
- **API reference, error catalogs, code samples, tables.** These do not persuade; they enumerate.
- **Tight word-count drafting with no revision room.** Devices reward a second pass; if you have only one pass, write clean and move on.
- **Anything where a device would draw attention to itself instead of to the idea.** The reader should feel the sentence land — not catch the writer reaching for a tool.

## How devices fail (anti-patterns)

Devices fail in four predictable ways. Watch for these in your own drafts and in voice-agent output.

1. **Decoration over function.** A chiasmus that sounds clever but adds no new pivot, no new contrast — just symmetry for symmetry's sake. Cut it.
2. **Density.** Three devices in two sentences. The reader notices the writing instead of the idea. One device per paragraph is plenty; two is a ceiling.
3. **Mismatch.** A polysyndeton ("and... and... and") used to enumerate a *short, clean* list when an asyndeton would land harder. Reach for the device the *function* asks for, not the one the writer prefers.
4. **Stack accumulation.** Five anaphoras in a chapter teach the reader the trick. By the sixth, the trick is doing the work — not the argument. Spread devices across chapters; do not concentrate them.

A useful self-check: if you can remove the device and the sentence loses *only* its prettiness, the device was decoration. If removing it loses the contrast, the rhythm, the pivot, or the punchline, the device was earning its place.

## The eight devices that earn their keep most often

These are the eight devices that come up constantly in this book's register. Each entry shows: what it is, what it *does* to the reader, a worked example using actual book topics, and the failure mode to watch for.

For the full ~40-device catalog grouped by function, see `references/devices.md`.

---

### 1. Anaphora — repetition at the start of successive clauses

- **What it does:** Builds rhythm and accumulates weight. Each repetition raises the stakes of the next.
- **Book-register example:** *"The gateway routes. The gateway authenticates. The gateway never holds state."*
- **Stronger when:** the repeated phrase is short (one to three words) and the variable tail does the actual work.
- **Watch for:** four or more repetitions becomes a chant. Three is the natural ceiling for prose; four crosses into rhetoric.

---

### 2. Antimetabole — same words, inverted order

- **What it does:** Forces the reader to register a relationship as *reversible* — and the reversal usually carries the argument. The classic Kennedy ("ask not what your country can do for you") works because the reversal is the thesis.
- **Book-register example:** *"We stopped asking what the cloud could do for our data and started asking what our data could do without the cloud."*
- **Stronger when:** the inversion does real conceptual work — i.e. the second half is not just a mirror but a *pivot*.
- **Watch for:** writers reach for antimetabole because it sounds clever. If the reversed sentence is a slogan rather than a claim, cut it.

---

### 3. Tricolon — three parallel elements (especially with rising length: *crescens*)

- **What it does:** Three is the smallest number that makes a list feel *complete*. Two feels like contrast; four feels like enumeration; three feels like an argument.
- **Book-register example (plain):** *"Sync is observable, replayable, recoverable."*
- **Book-register example (crescens):** *"It runs offline, it survives a vendor outage, and it outlives the company that wrote it."*
- **Stronger when:** the third element is the heaviest — longest, most concrete, or most surprising.
- **Watch for:** false tricolons where the three items are actually two-plus-padding. If you can drop the middle item without losing meaning, it was padding.

---

### 4. Antithesis — two contrasting ideas in parallel grammatical form

- **What it does:** Makes a contrast *unmissable* by forcing the reader's eye to compare across matched grammar. The architecture of the sentence does the persuasive work.
- **Book-register example:** *"Cloud-first treats the device as a viewport. Local-first treats the device as the truth."*
- **Stronger when:** the two halves match in syllable count or rhythm, not just in grammar.
- **Watch for:** false contrasts where the two halves are not actually opposed. A reader who tries to flip the framing should fail.

---

### 5. Asyndeton vs. Polysyndeton — omitted vs. repeated conjunctions

These are a pair. Use them deliberately, and never reflexively.

- **Asyndeton** (*"we came, we saw, we conquered"*) accelerates. The list moves fast; the absence of "and" creates urgency.
  - **Book-register example:** *"Local-first is fast, sovereign, durable, offline-capable."*
  - **Use when:** you want the reader to feel the items *piling up* without pause.

- **Polysyndeton** (*"and X and Y and Z"*) decelerates and weights every item. The repeated conjunction makes each addition feel like one more burden, one more cost, one more thing the reader must hold.
  - **Book-register example:** *"The vendor owns the schema and the API and the compute and the bill and, eventually, the customer."*
  - **Use when:** the *accumulation* is the argument — the point is that the list keeps going.

- **Watch for:** mixing them in adjacent sentences. The contrast loses force when both are deployed in the same paragraph.

---

### 6. Prolepsis — anticipating and answering an objection

- **What it does:** Pre-empts the reader's pushback, which both disarms it and signals that the writer has thought further than the reader. Particularly powerful in Council chapters and any section that pushes against SaaS orthodoxy.
- **Book-register example:** *"You might think this is a step backwards into client-server. It is not. Client-server placed the authority in the server; local-first places it in the device, and reconciles upward only when convenient."*
- **Structure:** *"You might think X. It is not. \[reframe\]."* The middle sentence — the flat denial — is the engine.
- **Watch for:** straw-man prolepsis, where the anticipated objection is one no real reader holds. If the objection is too easy to refute, the reader feels manipulated.

---

### 7. Metonymy — substitute an associated thing for the thing itself

- **What it does:** Compresses an entire system into a single concrete noun. *"The cloud"* is metonymy for an entire commercial arrangement; *"the bill"* is metonymy for the long-term cost of vendor lock-in.
- **Book-register example:** *"When the bill comes due, your sovereignty comes due with it."*
- **Stronger when:** the substituted noun is more concrete than the abstraction it replaces. *"The bill"* is more concrete than *"the recurring SaaS expense profile."*
- **Watch for:** opaque metonymy that requires the reader to guess what stands for what. The substitution should be immediate, not a puzzle.

---

### 8. Anadiplosis — last word of one clause becomes the first word of the next

- **What it does:** Builds a chain of cause-and-effect by making the linkage *visible*. The repeated word is the hinge that the reader cannot help but notice.
- **Book-register example:** *"The cloud holds your data. Your data holds your livelihood. Your livelihood holds the leverage."*
- **Stronger when:** the chain has three or more links (two links read as accidental repetition; three reads as deliberate structure).
- **Watch for:** chains where the repeated word changes meaning between clauses. That can be deliberate (the shift is the point), but if it happens by accident the sentence reads as muddled.

---

## How voice agents should use this skill

Voice agents (`voice-sinek`, `voice-godin`, `voice-grant`, `voice-brown`, `voice-gladwell`, `voice-lencioni`) frequently reach for named rhetorical structures while rewriting passages. Without a shared catalog, each agent invents its own examples — which fragments the house style across the book.

**The contract is:**

1. Before deploying a named device in a rewrite, the agent consults this skill — at minimum the eight devices above, ideally `references/devices.md` for the function-grouped catalog.
2. The agent uses the device whose *function* matches the work the passage needs to do (not the device the agent personally favors).
3. Worked examples in this skill are the house register. An agent's rewrite should be in the *same register* — declarative, agency-vocabulary, lead-with-punchline, no academic scaffolding.
4. If the agent finds itself reaching for a device this skill does not cover, it adds a candidate to `references/devices.md` (with a book-register example) so the next session has it.

The prose-reviewer agent uses this skill from the other direction: when reviewing a chapter, it consults the catalog to *name* devices the writer reached for unconsciously — confirming whether each one is functioning or merely decorating.

## Loading guidance

`SKILL.md` (this file) is the entry point — read it whenever the skill triggers.

`references/devices.md` is the full catalog, ~40 devices grouped by function. Load it when:

- You need a device not covered in the eight above.
- You want to see the full set of options for a given function (e.g. "what other repetition devices exist beyond anaphora?").
- You are doing a chapter-scale review and need to scan for *any* device the writer might have used.

Do not load `references/devices.md` for every prose touch — the eight above cover ~80% of cases.

## A discipline note

A device that is *named* is not automatically a device that is *working*. The test is always the same: remove it, read the sentence, and ask what was lost. If only the cleverness was lost, cut it. If the contrast, the rhythm, the pivot, or the punchline was lost, keep it.

Devices serve the argument. The argument never serves devices.
