# Literary & Rhetorical Devices — Full Catalog

> Reference companion to `../SKILL.md`. ~40 devices grouped by the *function* they perform — not by alphabet, not by Greek-vs-Latin name. Group by what you need the sentence to *do*, then pick the device that does it.
>
> Each entry follows the same shape:
> - **What it is** — one-line definition
> - **What it does** — the cognitive or emotional function on the reader
> - **Book-register example** — using actual Inverted Stack subject matter
> - **Watch for** — the predictable failure mode

## Table of contents

- [A. Repetition & rhythm](#a-repetition--rhythm)
- [B. Contrast & inversion](#b-contrast--inversion)
- [C. Substitution & figure](#c-substitution--figure)
- [D. Emphasis & framing](#d-emphasis--framing)
- [E. Argumentative structure](#e-argumentative-structure)
- [F. Sound & texture](#f-sound--texture)
- [G. Narrative & dramatic](#g-narrative--dramatic)

---

## A. Repetition & rhythm

Use these when a passage has the right *content* but the wrong *cadence* — the reasoning is sound but the prose monotones.

### 1. Anaphora — repetition at the start of successive clauses

- **What it does:** Builds rhythm. Each repetition raises the stakes of the next.
- **Example:** *"The gateway routes. The gateway authenticates. The gateway never holds state."*
- **Watch for:** four or more repetitions becomes a chant; three is the prose ceiling.

### 2. Epistrophe — repetition at the end of successive clauses

- **What it does:** Plants the same closing weight three times. Where anaphora *opens* with rhythm, epistrophe *lands* with it. Particularly effective for naming a single failure that recurs across causes.
- **Example:** *"When the network fails, your app fails. When the vendor fails, your app fails. When the bill comes due, your app fails."*
- **Watch for:** the final word must carry weight on its own — if it is a flat verb ("happens," "occurs"), the trick deflates.

### 3. Symploce — anaphora and epistrophe combined

- **What it does:** Locks the variable middle between two repeated anchors. Reads as inevitability — the framing is the same; only the contents change.
- **Example:** *"In Zone A, you own the data. In Zone B, you negotiate the data. In Zone C, you rent the data."*
- **Watch for:** symploce is heavy. Use once per chapter, not once per section.

### 4. Anadiplosis — last word of one clause becomes the first of the next

- **What it does:** Makes a causal chain visible. The repeated word is the hinge.
- **Example:** *"The cloud holds your data. Your data holds your livelihood. Your livelihood holds the leverage."*
- **Watch for:** two links reads as accidental; aim for three or four for deliberate structure.

### 5. Polysyndeton — repeated conjunctions

- **What it does:** Decelerates. Weights every item. Makes the list feel like accumulation, not enumeration. The point is that the list keeps going.
- **Example:** *"The vendor owns the schema and the API and the compute and the bill and, eventually, the customer."*
- **Watch for:** if the items are short and clean, asyndeton lands harder. Use polysyndeton when the *length* of the list is itself the argument.

### 6. Asyndeton — omitted conjunctions

- **What it does:** Accelerates. Compresses. The absence of "and" creates urgency. Caesar's *veni, vidi, vici* is the canonical case.
- **Example:** *"Local-first is fast, sovereign, durable, offline-capable."*
- **Watch for:** lists of two or longer-than-five lose the effect. Three or four items is the sweet spot.

### 7. Tricolon (and tricolon crescens) — three parallel elements

- **What it does:** Three is the smallest count that makes a list feel *complete*. Crescens (rising length) lets the third element carry the most weight.
- **Plain example:** *"Sync is observable, replayable, recoverable."*
- **Crescens example:** *"It runs offline, it survives a vendor outage, and it outlives the company that wrote it."*
- **Watch for:** false tricolons where one item is padding. If you can drop the middle without losing meaning, the structure was decorative.

### 8. Isocolon (parallelism) — equal grammatical structure across clauses

- **What it does:** Forces the reader to compare across matched grammar. The architecture of the sentence does persuasive work.
- **Example:** *"What the cloud gives, the cloud meters. What the cloud meters, the cloud bills."*
- **Watch for:** strict isocolon (matched syllable counts) becomes singsong. Loose parallelism — matched grammar, varied length — usually reads better in technical prose.

---

## B. Contrast & inversion

Use these when the passage needs to do the work of *comparing* two ideas — and the comparison is the argument.

### 9. Antithesis — two contrasting ideas in parallel form

- **What it does:** Makes a contrast unmissable. The matched grammar forces the reader's eye across the pivot.
- **Example:** *"Cloud-first treats the device as a viewport. Local-first treats the device as the truth."*
- **Watch for:** false contrasts. If a reader could flip the framing without changing the substance, the contrast was cosmetic.

### 10. Chiasmus — inverted parallel *structure* (A B / B A meaning)

- **What it does:** Marks a relationship as *reversible*. Used when the inversion itself is the insight.
- **Example:** *"What the network gives, the network can take away."*
- **Watch for:** chiasmus is often confused with antimetabole (which uses the *same words*). Both are valid; chiasmus is the broader category.

### 11. Antimetabole — inverted parallel structure with the *same words*

- **What it does:** Compresses a thesis into a memorable reversal. The reader registers the relationship as not-just-symmetric but *bidirectional*.
- **Example:** *"We stopped asking what the cloud could do for our data and started asking what our data could do without the cloud."*
- **Watch for:** sloganeering. If the reversed sentence is a slogan rather than a claim, cut it.

### 12. Paradox — apparent contradiction that resolves into truth

- **What it does:** Stops the reader. The contradiction forces a second reading, and the second reading is where the insight lands.
- **Example:** *"The most reliable network is the one you do not depend on."*
- **Watch for:** paradoxes that do not resolve are just confusion. The second reading must clarify, not deepen the puzzle.

### 13. Oxymoron — compressed paradox in two adjacent words

- **What it does:** Smaller-scale paradox. Names a tension in a single phrase that the reader has felt but not yet articulated.
- **Example:** *"Vendor-managed sovereignty"* — the contradiction is the point.
- **Watch for:** decorative oxymorons that do not name a real tension. *"Cruel kindness"* is decoration; *"vendor-managed sovereignty"* is a diagnostic.

---

## C. Substitution & figure

Use these when an abstraction needs to be made concrete, or when one concrete thing needs to stand in for a system of relationships.

### 14. Metaphor — implicit comparison

- **What it does:** Maps the reader's existing intuitions onto a new domain. A good metaphor is a shortcut to a mental model.
- **Example:** *"The SaaS contract is a leasehold on your own operations."*
- **Watch for:** mixed metaphors where the second image undercuts the first. Pick one image per paragraph and ride it.

### 15. Simile — explicit comparison ("like," "as")

- **What it does:** Same as metaphor but signals the comparison openly. Useful when the comparison would otherwise read as a literal claim.
- **Example:** *"Sync without conflict resolution is like version control without merging — it works until two people care about the same thing."*
- **Watch for:** weak similes that compare X to Y without illuminating either. The simile must teach the reader something about the first term.

### 16. Metonymy — substitute an associated thing for the thing itself

- **What it does:** Compresses an entire system into a single concrete noun. *"The cloud"*, *"the bill"*, *"the dashboard"* — each stands in for an entire commercial or technical arrangement.
- **Example:** *"When the bill comes due, your sovereignty comes due with it."*
- **Watch for:** opaque metonymy that the reader must decode. The substitute must be immediately recognizable.

### 17. Synecdoche — part for whole, or whole for part

- **What it does:** Specialized metonymy. *"All hands on deck"* uses *hands* for sailors. In technical prose, often a single component stands in for the whole system.
- **Example:** *"The OAuth token is now the company's identity perimeter."*
- **Watch for:** synecdoche works when the part is *load-bearing*. If the part is incidental, the figure misleads.

### 18. Personification — non-human gets human agency

- **What it does:** Grants intent to systems. The reader's pattern-matching for human agency is faster than their pattern-matching for distributed systems behavior — personification borrows that speed.
- **Example:** *"The replica refuses to forget. Even after the user deletes the row, the replica remembers it as a tombstone until the GC sweep collects it."*
- **Watch for:** over-personifying technical systems can sneak in causal claims that are not literally true. Use it as figure, not as argument.

### 19. Analogy — extended comparison across multiple dimensions

- **What it does:** Like metaphor but worked out across multiple matched points. Useful when the new domain is complex enough that a single image is insufficient.
- **Example:** *"Local-first is to SaaS what owner-occupied is to leasehold: same address, same square footage, completely different power relationship — and the difference shows up at the moment you want to renovate."*
- **Watch for:** analogies break down if pushed too far. Stop at the point of maximum illumination; do not chase the analogy into edge cases.

---

## D. Emphasis & framing

Use these when the passage needs to *modulate* the reader's emotional register — up, down, or sideways.

### 20. Hyperbole — deliberate exaggeration

- **What it does:** Marks emotional weight. The reader knows it is exaggeration; the exaggeration signals "this matters more than the literal claim would convey."
- **Example:** *"A SaaS outage at the wrong moment can cost a company a decade of customer trust."*
- **Watch for:** technical readers are allergic to hyperbole used as argument. Use it for color, never as load-bearing claim.

### 21. Litotes — understatement via double negative

- **What it does:** Conveys conviction via restraint. *"The result is not unimpressive"* says *impressive* but signals *the writer is not given to easy praise*.
- **Example:** *"The cost of running your own sync infrastructure is not negligible."*
- **Watch for:** litotes can read as evasive in technical prose. Use sparingly and only when the restraint itself is the point.

### 22. Meiosis — understatement (positive form, no double negative)

- **What it does:** Deliberately under-describes a thing the reader knows is important. The gap between description and reality is the argument.
- **Example:** *"The migration is a small lift" — said about a six-month, eight-engineer rewrite.*
- **Watch for:** in earnest technical prose, meiosis can come across as flippant. Reserve it for contrast against the reader's actual expectation.

### 23. Apophasis (paralipsis, praeteritio) — mention by claiming not to mention

- **What it does:** *"I will not dwell on the fact that..."* The writer raises the point precisely by disclaiming it. Reader registers the content and the writer's restraint at once.
- **Example:** *"We will set aside, for now, the question of what happens to the customer's data on the day the vendor's funding round fails to close."*
- **Watch for:** overused, this reads as smug. Once per chapter at most.

### 24. Hypophora — asking and answering your own question

- **What it does:** Makes the reader's likely question explicit, then answers it before the reader can object. Useful at section breaks.
- **Example:** *"What does sovereignty cost? It costs an engineering month and saves a vendor decade."*
- **Watch for:** the question must be one a real reader would actually ask. Manufactured questions read as filler.

### 25. Erotema (rhetorical question) — question expecting no answer

- **What it does:** The question carries the assertion. *"Who would design it this way?"* — the reader supplies *no one*.
- **Example:** *"Who decides which row of your database lives where? In Zone C, the vendor decides — quietly, in a region you may not have approved."*
- **Watch for:** rhetorical questions can read as cheap rhetoric. Pair with concrete subject matter; never use as transition filler.

### 26. Aporia — feigned doubt or inability

- **What it does:** Models the reader's own uncertainty, then resolves it. Disarming.
- **Example:** *"It is hard to say at exactly which point a SaaS dependency becomes a liability — but it is easy to say what the day after looks like."*
- **Watch for:** false aporia (writer pretending to doubt something they have already concluded) reads as manipulative.

### 27. Climax (auxesis) — ascending order of importance

- **What it does:** Orders a list so each item is heavier than the last. The reader's attention compounds; the final item lands hardest.
- **Example:** *"You lose the dashboard. You lose the integrations. You lose the data. You lose the customers who relied on the data."*
- **Watch for:** if the items are not actually in ascending order, the structure backfires — the reader feels the descent.

---

## E. Argumentative structure

Use these when the passage is *making a case* and needs the structural moves that disarm objection or sharpen definition.

### 28. Prolepsis (procatalepsis) — anticipating an objection

- **What it does:** Pre-empts the reader's pushback. Disarms by demonstrating that the writer has thought one step further than the reader.
- **Example:** *"You might think this is a step backwards into client-server. It is not. Client-server placed authority in the server; local-first places it in the device, and reconciles upward only when convenient."*
- **Watch for:** straw-man prolepsis. The objection must be one a real reader holds.

### 29. Concession — granting the opponent's point before pivoting

- **What it does:** *"Yes, X is true — and that is precisely why Y."* Models intellectual honesty and uses the granted point as a launchpad.
- **Example:** *"Cloud SaaS is operationally simpler — and that simplicity is exactly the price the customer is paying without seeing the line item."*
- **Watch for:** concessions that do not pivot. A grant without a turn just hands the point away.

### 30. Distinctio — explicit definition before argument

- **What it does:** Names the senses of a term so the argument that follows cannot be deflected by ambiguity. Useful for words like *sovereignty*, *local-first*, *durability* that carry vendor-shaped baggage.
- **Example:** *"By 'local-first' we mean a system where the device holds the authoritative copy and the network is an optimization, not a precondition. We do not mean a system that caches aggressively while still requiring the network for writes."*
- **Watch for:** definitions that are too narrow to do work, or too broad to exclude anything. The definition should let some real systems in and keep others out.

### 31. Enumeratio — listing parts to make an abstract concrete

- **What it does:** Forces the reader to picture the *components* of an abstraction.
- **Example:** *"'Vendor lock-in' is a phrase. The actual mechanisms are: schema gravity, API surface area, custom field types, integration partners, billing dependencies, and the institutional knowledge of the people who configured it."*
- **Watch for:** enumerations longer than seven items lose force. If the list is genuinely longer, partition it into sub-lists.

### 32. Definition by negation — what something is *not*

- **What it does:** Brackets the concept by walking the reader through nearby ideas and rejecting them. The remainder is the definition.
- **Example:** *"Local-first is not offline-only. It is not peer-to-peer. It is not a return to the desktop era. It is the architecture in which the device holds the authoritative copy and the network is an optimization."*
- **Watch for:** negations that exclude no real reader's misconception. Each *not* must rule out a misreading the reader actually has.

---

## F. Sound & texture

Use these sparingly. In technical prose, sound effects that draw attention to themselves *cost* — the reader notices the writing and stops following the argument. Use only when the sound serves the sense.

### 33. Alliteration — repeated initial consonant

- **What it does:** Marks a phrase as worth remembering. *"Sovereign, secure, self-hosted"* is a tricolon with alliteration; the alliteration is what makes it slogan-like.
- **Example:** *"Durable, decentralized, deletable on demand."*
- **Watch for:** alliteration that traps you into bad word choices. If the alliteration drives the noun, the noun is doing the wrong work.

### 34. Assonance — repeated vowel sounds

- **What it does:** Subtler than alliteration. Smooths a phrase into a single rhythmic unit. Rarely deployed deliberately in technical prose; usually works by ear during revision.
- **Example:** *"The sync runs in the background, bound to no clock."* (the *un*/*ow* repetition)
- **Watch for:** assonance is almost always a revision-pass effect, not a drafting effect. If you are reaching for it deliberately, you are probably overworking.

### 35. Consonance — repeated consonant sounds in any position

- **What it does:** Like assonance, a texture-level effect. Adds weight by ear without the reader noticing why.
- **Example:** *"The schema scatters across services."* (*s*-*sh*-*sc*)
- **Watch for:** same caution as assonance — usually a revision artifact, not a drafting tool.

---

## G. Narrative & dramatic

Use these in Part I (scenario-driven Story Spine), Council chapters (two-act structure), Epilogue, and any passage where *story* is the persuasive engine.

### 36. In medias res — start in the middle of action

- **What it does:** Drops the reader into a scene already in motion, then loops back to context. Bypasses the slow ramp of "let me set the stage."
- **Example:** *"At 03:47 UTC the dashboard stopped reporting. The on-call engineer had been awake for nineteen hours. The vendor's status page showed all systems operational."*
- **Watch for:** in medias res buys engagement at the cost of comprehension. The loop-back must come within a paragraph or two.

### 37. Story Spine (Luhn) — *Once upon a time / Every day / Until one day / Because of that / Until finally / Ever since then*

- **What it does:** The skeleton of every narrative that holds attention. Maps cleanly onto an architectural decision record (ADR), a postmortem, or a Council chapter.
- **Mapping for technical prose:** *Setup / Steady state / Rupture / Consequence chain / Resolution / New steady state.*
- **Watch for:** technical readers will skip a story that does not signal its destination. Plant the *until-one-day* moment by the end of the second paragraph.

### 38. Foreshadowing — planting a later reveal

- **What it does:** A detail introduced early gains weight when its significance is revealed later. Used in Council chapters where a Round-1 failure is later mirrored in a Round-2 fix.
- **Example:** Mentioning a constraint early in plain prose ("the device will be offline for ten days") and then cashing it in three sections later when the sync algorithm has to handle exactly that case.
- **Watch for:** foreshadowing that is too obvious turns into telegraphing. The detail should read as ordinary on first encounter.

### 39. Bathos — anticlimactic descent for emphasis or comic relief

- **What it does:** The tonal drop after a climb makes the point land harder, often by exposing it as ordinary. Used carefully, it deflates pretension.
- **Example:** *"You can frame this as a paradigm shift, a re-decentralization, a return to first principles. Or you can frame it as: the database lives on the device now."*
- **Watch for:** bathos used too often becomes the writer's tic. Once per chapter, at the most.

### 40. Apostrophe — direct address to an absent entity, abstraction, or the reader

- **What it does:** Breaks the fourth wall. Pulls the reader from observer into participant.
- **Example:** *"Reader: if you are evaluating a SaaS contract this quarter, the clause you want is the one about data export under termination — and the one you want to delete is the one that grants the vendor a perpetual license."*
- **Watch for:** apostrophe used as filler ("dear reader, let us now consider...") reads as Victorian. Direct address only when the reader genuinely has a decision to make.

---

## How to extend this catalog

If a voice agent or a prose-review pass surfaces a device this catalog does not cover:

1. Add an entry in the appropriate section (use the four-line template: *what it is / what it does / book-register example / watch for*).
2. Match the register of the existing examples — declarative, agency-vocabulary, lead-with-punchline, no academic scaffolding.
3. The example should use actual book subject matter (CRDTs, sovereignty, vendor lock-in, sync, zones, local-first), not generic placeholders.
4. Keep the entry short. The catalog is a working reference, not an essay.
