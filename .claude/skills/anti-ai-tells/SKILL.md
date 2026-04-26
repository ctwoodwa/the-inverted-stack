---
name: anti-ai-tells
description: Catalog of LLM-generated writing patterns that mark prose as AI-authored and the calibrated rewrites that remove them — significance puffery, copula avoidance, superficial -ing tail-phrases, AI vocabulary words, negative parallelisms, false ranges, persuasive authority tropes, signposting, fragmented headers, and ~10 more. Use whenever drafting, revising, or reviewing prose where a sentence "reads competent but flat," opens a paragraph with ceremony instead of substance, or reaches for vocabulary like "underscore," "delve," "tapestry," "crucial," "pivotal moment," or "stands as a testament." Voice-* agents, prose-reviewer, and style-enforcer should consult this skill alongside literary-devices when refining prose. Use even when the user does not name "AI tell" or "humanizer" — if the task is making prose sound less assembled and more authored, this skill applies. Calibrated for *The Inverted Stack*'s deliberate use of em-dashes (Lencioni/Gladwell registers), boldface (sparingly for emphasis), and hyphenated technical terms (local-first, two-act, end-to-end) — these are NOT tells in this book's voice.
---

# Anti-AI Tells — Reference for Removing LLM Signatures from Technical Prose

## Why this skill exists

A book chapter can pass the technical-reviewer, satisfy the style-enforcer, and still feel "off" to a reader who has spent a year skimming AI-generated prose. The reason is rarely a single bad sentence — it is the cumulative weight of patterns that statistical language models reach for by default: ceremonial openers, vague attributions, forced groups of three, copulas swapped for "serves as," hedged conclusions that read like a teacher reluctant to fail a student.

This skill catalogs those patterns with rewrites in this book's register so the prose-reviewer and style-enforcer can flag them by name and the voice agents can avoid them on the first pass.

The catalog is adapted from blader/humanizer (MIT, based on Wikipedia's WikiProject AI Cleanup "Signs of AI writing" guide) and **calibrated** to *The Inverted Stack*'s house style — three of the source patterns are explicitly *not* applied here because the book uses them deliberately (see "Calibrations" below).

## When to consult this skill

Reach for it when:

- Drafting any chapter — voice agents and chapter-drafter should scan for patterns 1, 3, 7, 8, 9, 12, 27 *during* writing rather than discovering them in review.
- Reviewing prose — prose-reviewer should grep for the lexical tells (vocabulary lists in patterns 1, 4, 7, 8, 27, 28) on every chapter.
- Editing — style-enforcer should fix patterns 8 (copula avoidance), 17 (title case), 29 (fragmented headers), and the lexical patterns mechanically.
- Any sentence that reads "puffed up" without saying more.
- Any paragraph that announces what it is about to do instead of doing it.
- Any heading followed by a one-line restatement of itself.

## When to skip this skill

Skip it when the work is:

- **Code blocks, tables, configuration schemas, citation reference lists.** These do not persuade; they enumerate. AI-pattern grep on these will produce false positives.
- **Direct quotes from outside sources.** A quoted passage can contain any pattern the source contained. Do not edit attributed quotes to remove tells.
- **Specification voice clauses where copula avoidance is structural.** "The kernel exposes" is not "stands as" — `expose` is the verb of record. Only flag verbs from the explicit copula-avoidance list.

## Calibrations — patterns NOT applied in this book

Three patterns from the upstream catalog are deliberately *excluded* because the book's voice uses them on purpose:

- **Em-dash use is INTENTIONAL.** The Lencioni and Gladwell voice agents lean on em-dash apposition for rhythm. The voice-pass tuning explicitly preserves em-dashes. Do not flag em-dash density as a tell. (Audiobook narration converts em-dash to comma for prosody — that is a TTS-only transform, not a style fix.)
- **Boldface emphasis is ALLOWED sparingly.** The book uses `**bold**` for vocabulary installations ("**The SaaS bundle:** ...") and key-term first-use anchors. Flag bold only when it is mechanical (every bullet starts with bold; bold used for emphasis on plain prose words like "**important**" or "**critical**").
- **Hyphenated technical terms are CORRECT.** `local-first`, `local-node`, `two-act`, `end-to-end`, `Zone-A`/`Zone-C`, `cross-tenant`, `client-side` are technical terminology with stable meaning. The "hyphenated word pair overuse" pattern (#26 in the upstream) does not apply.

---

## Lexical Quick-Grep

The fastest review pass is a grep across all chapters for the high-frequency tell vocabulary. Hits are not automatic violations — review the surrounding sentence. But every hit is a candidate for review.

```bash
# Significance / legacy puffery (Pattern 1)
grep -nE "stands? (as|for) a? ?testament|pivotal moment|evolving landscape|setting the stage|indelible mark|broader (trend|movement)|deeply rooted|enduring legacy|underscores its (importance|significance)" chapters/

# AI vocabulary words (Pattern 7) — high false-positive rate; review each
grep -niE "\b(delve|showcase|tapestry|interplay|intricate|underscores?|garner|foster|enduring|crucial|pivotal|vibrant)\b" chapters/

# Copula avoidance (Pattern 8)
grep -nE "\b(serves? as|stands? as|marks? a|represents? a|boasts?|features?(?! a (configuration|design|module|component))) " chapters/

# Persuasive authority tropes (Pattern 27)
grep -niE "the real question is|at its core|in reality|fundamentally(,| )|what really matters|the heart of the matter|the deeper issue" chapters/

# Signposting (Pattern 28)
grep -niE "let's (dive|explore|break this down|unpack|walk through)|here's what you need to know|without further ado|now let's look at" chapters/

# Collaborative artifacts (Pattern 20) — should be zero in published chapters
grep -niE "i hope this helps|certainly!|of course!|you're absolutely right|let me know if|here is an? overview" chapters/
```

The voice-pass logging in `build/voice-pass.py` could optionally surface counts per chapter as part of its run report.

---

## The Catalog

### 1. Significance / Legacy / Broader-Trend Puffery

**The tell:** A sentence that puffs up a fact's importance by gesturing at "broader" trends, "evolving landscapes," or "pivotal moments" — language that adds emotional weight without adding information.

**Lexical markers:** *stands as a testament, serves as a reminder, marking a pivotal moment, the evolving landscape, contributing to the broader, setting the stage for, an indelible mark, deeply rooted in, an enduring legacy, underscores its importance, reflects a broader, key turning point, focal point*

**Why this matters in this book:** *The Inverted Stack* makes specific claims about specific systems. Puffery dilutes the claims. A sentence that says "marking a pivotal moment in the evolution of distributed storage" tells the reader less than "this was the first system to ship CRDTs at consumer scale."

**Before:**
> The 2019 Ink & Switch paper marked a pivotal moment in the evolution of distributed software, contributing to a broader movement toward user-controlled data and setting the stage for the local-first architectures that would follow.

**After:**
> The 2019 Ink & Switch paper named seven properties for local-first software. Every architecture in this book traces back to that list.

### 2. Notability / Coverage Stuffing

**The tell:** A list of media outlets or follower counts substituting for the substance of what was said.

**Lexical markers:** *coverage in [list of outlets], an active social media presence, written by a leading expert, widely cited, frequently referenced*

**Less common in this book** — but appears in author bios, related-work sections, and "further reading" appendices. When it appears, replace the list with the actual claim being attributed.

**Before:**
> Kleppmann's work has been covered in Communications of the ACM, the Morning Paper, and major distributed-systems blogs.

**After:**
> Kleppmann's 2019 paper *"Local-first software"* defined the seven properties this book treats as a minimum bar.

### 3. Superficial -ing Tail-Phrases

**The tell:** A `-ing` participle clause tacked onto the end of a sentence to add the appearance of consequence or insight without specifying any.

**Lexical markers (sentence tails):** *highlighting…, underscoring…, emphasizing…, ensuring…, reflecting…, symbolizing…, contributing to…, fostering…, cultivating…, encompassing…, showcasing…, leveraging…*

**Why this matters in this book:** Specification chapters in Part III rely on declarative clauses. A trailing `-ing` clause turns a precise statement into a soft-edged one. Tutorial chapters in Part IV give imperative steps; trailing `-ing` clauses make steps feel optional or vague.

**Before:**
> The kernel signs every payload before transmission, ensuring tamper-evidence and underscoring the importance of cryptographic integrity at the data plane.

**After:**
> The kernel signs every payload before transmission. The recipient rejects any payload whose signature does not validate against the sender's identity key.

### 4. Promotional / Travel-Brochure Language

**The tell:** Vocabulary lifted from marketing copy used to describe technical or factual content.

**Lexical markers:** *boasts, vibrant, rich (figurative), profound, in the heart of, nestled, breathtaking, must-visit, renowned, groundbreaking (figurative), seamless, intuitive, powerful*

**Less common in this book** — but watch for "**seamless**, **intuitive**, **powerful**" triplets in Part IV tutorial chapters and product-comparison passages. Replace with specific properties.

**Before:**
> The framework boasts a vibrant ecosystem of plugins and offers a seamless, intuitive developer experience.

**After:**
> The framework has 240+ third-party plugins. Setup is `npm install` plus one config file.

### 5. Vague Attributions / Weasel Words

**The tell:** An opinion attributed to "industry observers," "experts," "some critics," or "several sources" — any authority phrase that names no actual source.

**Lexical markers:** *industry reports/observers/analysts, experts argue/believe/agree, some critics, several sources, many commentators, it is widely believed*

**Why this matters in this book:** Council chapters in Part II depend on attributing positions to *named* council members. Specification chapters in Part III state architectural facts directly. There is no role for unnamed expert opinion. Either name the source (with a citation) or state the claim without attribution.

**Before:**
> Industry observers have noted that local-first architectures struggle with multi-tenant scenarios. Some experts argue that this limits adoption.

**After:**
> Multi-tenant local-first deployments require a coordinator for cross-tenant operations (admin overrides, billing aggregation, audit views). Chapter 18 covers the Bridge accelerator pattern that solves this.

### 6. Outline "Challenges and Future Prospects" Sections

**The tell:** A section that ends with a formulaic "challenges remain" paragraph followed by a "but the future is bright" paragraph — vague difficulty followed by vague optimism, no specific actions named.

**Why this matters in this book:** The epilogue and several Part IV "Shipping" chapters could fall into this pattern. The book's voice instead says: *here is what is unsolved; here is what to do about it; here is who is doing it.*

**Before:**
> Despite its promise, local-first architecture faces several challenges, including ecosystem maturity, developer education, and tooling gaps. Despite these challenges, the future of local-first software looks bright as the community continues to grow.

**After:**
> Three problems remain unsolved as of 2026: schema evolution under arbitrary client-version skew (Chapter 13), end-user-managed key recovery without a custodian (Chapter 15), and discoverability of peers across NAT without a relay (Chapter 14). The Inverted Stack project is tracking each in its public roadmap.

### 7. AI Vocabulary Words

**The tell:** A vocabulary cluster that appears at much higher frequency in post-2023 text than in pre-2023 books and journals. These words are not wrong individually, but they appear together with statistical regularity.

**High-frequency markers:** *actually, additionally, align with, crucial, delve, emphasizing, enduring, enhance, foster, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun), pivotal, showcase, tapestry, testament, underscore (verb), valuable, vibrant*

**Calibration for this book:**
- `crucial` and `key` are commonly *correct* in technical writing ("the key invariant is"). Flag only when used as soft emphasis.
- `landscape` is fine in literal/technical compounds ("the data-residency landscape") but a tell as abstract puffery ("the evolving software landscape").
- `showcase` and `delve` are almost always tells — replace with `demonstrate`, `examine`, `look at`.
- `additionally` at sentence start is almost always cuttable — the next sentence either follows from the previous or it doesn't; "additionally" adds nothing.

**Before:**
> Additionally, this chapter delves into the intricate interplay between the sync daemon and the relay, showcasing how their key roles foster a vibrant, enduring architecture.

**After:**
> The sync daemon and relay communicate over a wire protocol defined in Appendix A. This section traces a single message from emit to commit on a remote peer.

### 8. Copula Avoidance ("serves as," "stands as," "represents")

**The tell:** Replacing simple `is`/`are`/`has` with elaborate verb constructions that add no information.

**Lexical markers:** *serves as a, stands as a, marks a, represents a, embodies a, constitutes a, boasts, features (when "has" would do), offers (when "has" or "provides" would do)*

**Why this matters in this book:** Specification voice (Part III) is built on direct copulas. "The kernel **is** the trust boundary." "The relay **has** no persistent state." Copula avoidance dilutes the specification. This is one of the highest-yield single-rule fixes for AI-flavored prose.

**Calibration:** Some verbs in the marker list are legitimate when they carry their literal meaning. *"The relay serves authenticated traffic only"* is fine — `serve` means to handle. `"This chapter represents the bridge between Part I and Part II"` is the puffy use — replace with `is`.

**Before:**
> The Anchor accelerator serves as the reference implementation for Zone A. It boasts an embedded SQLite store, features a CRDT engine adapter layer, and stands as a testbed for the architecture.

**After:**
> The Anchor accelerator is the reference implementation for Zone A. It uses embedded SQLite, has a CRDT engine adapter layer, and is the testbed for the architecture.

### 9. Negative Parallelisms and Tailing Negations

**The tell:** "Not only X, but also Y" or "It's not just X, it's Y" used as a default rhetorical structure rather than for genuine contrast. Also: short tail-fragments like "no guessing" or "no wasted motion" tacked onto the end of a sentence as if they were full clauses.

**Lexical markers:** *not only…but also, it's not just…it's, this isn't merely…it's, this is not X, it is Y*

**Calibration:** A *real* not-only-but-also is fine when both halves carry weight. The tell is when "but also" introduces something the writer would have included anyway. If you can drop "not only" and "but also" without losing meaning, drop them.

**Before:**
> The local node is not only a database, it is a complete runtime environment.

**After:**
> The local node is a complete runtime environment, not just a database. (Or: simply state the broader claim.)

### 10. Rule of Three Overuse

**The tell:** Every list contains exactly three items. Every claim is reinforced with three examples. Three-item lists feel rhetorically complete to LLMs because they almost always are — which is why ubiquitous threes start to read mechanical.

**Calibration:** Three-item lists are often *correct*. The tell is when *every* list in a paragraph is exactly three. Vary cadence: some twos, some fours, occasional ones. Tricolons used for *intentional rhetorical force* (see literary-devices) are fine and welcome.

**Before:**
> The architecture is built on three principles: data ownership, offline operation, and cryptographic integrity. Three components implement these: the kernel, the relay, and the daemon. Three failure modes matter most: network partition, key loss, and schema skew.

**After:**
> The architecture has two load-bearing principles: the user owns the data, and the data is encrypted at rest with a key the user controls. Four components implement them — the kernel, the daemon, the relay, and the recovery custodian. (Then list failure modes naturally, without forcing the count.)

### 12. False Ranges ("from X to Y")

**The tell:** A "from X to Y" construction where X and Y are not on a meaningful scale — they are just two examples of a category.

**Before:**
> The book covers everything from CRDTs to compliance, from key management to UX patterns.

**After:**
> The book covers four areas in roughly equal depth: CRDTs and conflict semantics; key management and recovery; compliance and data residency; UX patterns for sync and conflict.

### 16. Inline-Header Vertical Lists

**The tell:** A bulleted list where every item starts with a bolded header followed by a colon followed by a one-sentence description. The format is not wrong — it is just so default-LLM that it signals provenance.

**Calibration:** This format is *appropriate* when items are genuinely parallel definitions (a glossary, a table-of-contents preview, a configuration reference). The tell is when it appears for prose that should flow as paragraphs — when the bolded headers add no scanning value because the reader will read every item anyway.

**Before:**
> - **User Experience:** The UX has been improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**After:**
> The 1.4 release improved the conflict-resolution UI, cut sync latency by 40% through batched delta encoding, and added end-to-end encryption for the cross-device sync channel.

### 17. Title Case in Headings

**The tell:** Headings written in Title Case (every Major Word Capitalized) where the book's house style is sentence case.

**House rule:** Sentence case for all H2/H3/H4 headings. H1 chapter titles follow their own pattern (`Chapter N — Title`). Section headings get sentence case.

**Before:**
> ## The Inverted Stack In One Diagram
> ### Choosing Your Architecture For Local-First

**After:**
> ## The inverted stack in one diagram
> ### Choosing your architecture for local-first

### 20. Collaborative Communication Artifacts

**The tell:** Phrases left over from chatbot conversation pasted as content.

**Lexical markers:** *I hope this helps, Of course!, Certainly!, You're absolutely right, Would you like…, Let me know if, Here is an overview, Here's a summary*

**Should be zero in published chapters.** The grep query above is the canonical check.

### 21. Knowledge-Cutoff Disclaimers

**The tell:** A sentence that hedges a factual claim by gesturing at the limits of "available information."

**Lexical markers:** *as of [date], up to my last training update, while specific details are limited, based on available information, while comprehensive data is not available*

**Why this matters in this book:** When a fact is unknown or unstable, *say so directly* — name the uncertainty and what would resolve it. Do not hedge with "available information" language that reads as model-self-disclosure.

**Before:**
> While specific details about Sunfish's production deployments are limited, it appears to be in active use by several teams as of 2026.

**After:**
> Sunfish is open source ([github.com/ctwoodwa/Sunfish](https://github.com/ctwoodwa/Sunfish)) and pre-1.0 as of 2026; production deployments are not publicly tracked.

### 25. Generic Positive Conclusions

**The tell:** A closing paragraph or sentence that offers vague optimism — "looks bright," "exciting times ahead," "a major step in the right direction" — without naming what specifically improves or what action follows.

**Why this matters in this book:** The epilogue and chapter conclusions in Part IV must close on a *specific* claim or action — what the reader does next, what shipped, what is now possible. Generic optimism reads as filler and weakens the book's overall posture of operational seriousness.

**Before:**
> The future of local-first software looks bright. Exciting developments are on the horizon as the community continues to grow.

**After:**
> The next eighteen months will tell whether local-first reaches the inflection point of CRDT engines becoming a commodity dependency. Three projects to watch: Sunfish, Loro, and Yjs's 2.0 line. (Then end.)

### 27. Persuasive Authority Tropes

**The tell:** Phrases that *signal* the writer is about to deliver a deep insight, when the sentence that follows just restates an ordinary point with extra ceremony.

**Lexical markers:** *the real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter, when you get down to it*

**Why this matters in this book:** This is one of the highest-density tells in technical-flavored AI prose. The book's voice already leads with the punchline (style-guide §"Lead with the Punchline") — these tropes are the opposite of leading with the punchline. They are the writer clearing throat before saying the punchline.

**Before:**
> The real question is whether teams will adopt local-first architectures. At its core, what really matters is whether the developer experience can match the SaaS baseline.

**After:**
> Adoption depends on developer experience matching the SaaS baseline. Until tooling closes that gap, local-first remains a deliberate choice rather than a default.

### 28. Signposting and Announcements

**The tell:** Sentences that announce what the writing is about to do — "Let's dive into," "Here's what you need to know," "Now let's look at," "Without further ado" — instead of doing it.

**Lexical markers:** *let's dive in, let's explore, let's break this down, let's unpack, let's walk through, here's what you need to know, here's the thing, now let's look at, without further ado*

**Why this matters in this book:** The style-guide already prohibits throat-clearing ("In this chapter, we will…"). Pattern 28 covers the *casual* version of the same offense — the chatty signpost that AI models reach for to soften transitions. In the book's register, the new section's first sentence *is* the transition.

**Before:**
> Let's dive into how the sync daemon handles peer discovery. Here's what you need to know.

**After:**
> Peer discovery in the sync daemon runs in two modes: bootstrap (find any peer to start) and steady-state (maintain the working set of known peers).

### 29. Fragmented Headers (heading + one-line restatement)

**The tell:** A heading followed by a one-line paragraph that restates the heading before the real content begins.

**Why this matters in this book:** Adds nothing; reads as filler; breaks the rhythm of opening directly into substance. The first paragraph after a heading should be the *first piece of substance* on that section's topic.

**Before:**
> ## Failure modes
> Failure modes matter.
> When the relay is unreachable, the daemon queues writes locally. The queue is bounded at 10,000 entries by default…

**After:**
> ## Failure modes
> When the relay is unreachable, the daemon queues writes locally. The queue is bounded at 10,000 entries by default…

---

## Process for the Reviewer

When a chapter arrives at icm/prose-review:

1. **Run the lexical greps above.** Expect zero hits for patterns 20, 21 in published chapters; expect a small number for patterns 1, 7, 8, 27, 28 — review each.
2. **Scan the structural patterns by eye.** Patterns 3 (-ing tails), 6 (challenges-and-prospects), 10 (rule-of-three), 12 (false ranges), 16 (inline-header bullets), 17 (title case), 25 (generic conclusions), 29 (fragmented headers) cannot be reliably grep'd.
3. **For every flag, decide between fix and leave.** A pattern hit is a *candidate*, not a verdict. The calibration notes above explain when each pattern is actually correct.
4. **Apply fixes via style-enforcer for mechanical patterns** (8, 17, 29) and leave structural patterns (3, 6, 10, 12, 25) for the author or voice agent to revise with intent.

## Process for the Drafter / Voice Agent

When drafting a new chapter or revising one:

1. **Avoid patterns 1, 7, 8, 27 by default.** These are habit-forming — once you avoid them on the first pass, the prose-reviewer pass becomes much shorter.
2. **Reach for patterns from `literary-devices/` instead.** Where you would otherwise reach for "stands as a testament," reach for tricolon, antithesis, or anaphora — devices with intentional rhetorical force that are not AI defaults.
3. **Close sections on a specific claim or action.** This kills pattern 25 before it appears.
4. **Check the heading directly above each opening paragraph.** If the paragraph would be redundant with the heading, cut it. This kills pattern 29.

---

## Acknowledgment

The catalog is adapted from [blader/humanizer](https://github.com/blader/humanizer) v2.5.1 (MIT), which is in turn based on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) maintained by WikiProject AI Cleanup. The patterns documented there come from observations of thousands of instances of AI-generated text on Wikipedia. The calibrations, the book-specific examples, and the lexical greps are this project's contribution.
