# Unified Technical Writing Style Guide
### Synthesized from Sinek, Luhn, Clear, Robbins, and King

***

## Overview

This guide consolidates the most transferable elements from five distinct communicator voices — Simon Sinek, Matthew Luhn, James Clear, Tony Robbins, and Stephen King — into a coherent, practical writing style for technical documentation, architecture decision records, specifications, API docs, and engineering blog posts. The synthesis strips out delivery-dependent tactics (Robbins' physiology, Sinek's dramatic pauses) and distills what works in *written* technical communication: purpose clarity, narrative structure, actionable precision, vocabulary designed to shift mental states from confusion to confidence, and the revision discipline that separates a draft from prose worth a reader's time.

***

## The Core Philosophy: Purpose Before Process

**Borrowed from: Sinek (primary), Clear (supporting)**

Every technical document should answer "Why does this exist?" before it answers "What does it do?" or "How does it work?" Readers — especially developers and architects — disengage when they cannot connect a system's mechanics to a meaningful outcome.

In practice, this means:
- Open every document, section, or README with a **one-to-two sentence statement of purpose** — not a list of features.
- Frame the problem being solved before describing the solution.
- Use the architecture of *Why → What → How* as the default section ordering for technical designs.

> **Example (Anti-pattern):** "The AllocationScheduler component accepts an `IEnumerable<AllocationEvent>` and renders a gantt-style timeline using SVG."
>
> **Example (Pattern):** "AllocationScheduler exists to make over-allocation visible at a glance — the thing that causes projects to fail silently. It accepts allocation events and renders them as a timeline, so team leads can see conflicts before they become delays."

***

## Voice Characteristics

### Clarity is a Structural Obligation, Not a Polish Step
**Borrowed from: Clear (primary)**

Clarity is not something added at the end. It is the design constraint. Every sentence either earns its place or is removed.

- **Write for the reader's cognitive load, not your completeness instinct.** If a concept requires three paragraphs of context before it becomes useful, restructure so context is delivered just-in-time.
- **Prefer active voice.** "The gateway routes requests to downstream services" beats "Requests are routed to downstream services by the gateway."
- **One idea per paragraph.** Each paragraph should have a single controlling assertion, followed by its support. Readers should be able to scan topic sentences and understand the document's spine.
- **Cut ruthlessly.** If removing a sentence does not change the reader's understanding, remove it.
- **Second draft = first draft minus ten percent.** Borrowed from Stephen King's *On Writing*. After every chapter, section, or document is "done," cut ten percent. Not the worst ten percent — *any* ten percent. The discipline of cutting forces the question every word should answer: does this earn its place? If you cannot find ten percent to cut, you have not finished revising.
- **Trust the reader.** Describe just enough to put the picture in the reader's head, then stop. Over-description is not generosity; it is distrust. The reader who is given the load-bearing details and the room to assemble them will stay engaged longer than the reader who is handed every conclusion.

### Certainty in Tone, Precision in Claim
**Borrowed from: Robbins (primary), Clear (supporting)**

Robbins' defining quality is that his voice conveys *conviction without shouting.* In writing, this translates to a tone that is definitive and direct — not hedging with "this might be one approach" when the evidence points clearly to a recommendation.

- **Make recommendations, not inventories.** Do not list five equally weighted options when the situation clearly favors one. State the recommendation first, then provide the alternatives for context.
- **Use strong, specific verbs.** "Configure," "isolate," "emit," "propagate" — not "set up," "deal with," "send," "handle."
- **Avoid uncertainty language as a default register.** "This could potentially result in performance degradation under certain conditions" becomes "This increases latency under high concurrency — benchmark above 500 RPS before deploying."
- **Cut adverbs aggressively.** Borrowed from King: an adverb is usually a sign that the verb underneath it is weak. "The build runs slowly" is weaker than "the build crawls." "The system fails intermittently" is weaker than "the system drops connections under load." When you reach for an adverb, replace the noun-verb pair instead. Adverbs that survive should be load-bearing — they should change the meaning of the sentence, not redundantly emphasize what the verb already implies.

### Emotional Authenticity and Relatable Struggle
**Borrowed from: Luhn (primary), Sinek (supporting)**

Technical writing is still writing for humans. The most effective documentation acknowledges that implementation is hard, that the reader may be confused, and that the author has been there. This is not softness — it is strategic connection.

- **Name the difficulty.** If a concept is genuinely hard, say so: "This part is counterintuitive until you see it in practice." This signals competence, not weakness.
- **Use first-person plural sparingly but intentionally.** "We ran into this problem when..." grounds abstract solutions in real experience.
- **Write the failure state, not just the success path.** Documentation that only shows the happy path fails users when they inevitably diverge from it.

### Systems Thinking Over Feature Lists
**Borrowed from: Clear (primary), Sinek (supporting)**

Clear's emphasis on *systems over goals* maps directly to how good architecture is documented. A feature list describes what a system *is*. A systems view describes what a system *does over time* and *why that matters.*

- **Document invariants and constraints, not just capabilities.** What must always be true? What can never happen? These are more valuable than a list of supported methods.
- **Show compounding effects.** When a design decision accumulates benefit over time (e.g., consistent event naming makes log querying 10x faster six months in), make that explicit.
- **Use "If X, then Y" framing** to connect architectural decisions to downstream consequences.

***

## Narrative Structure

**Borrowed from: Luhn (primary), Sinek (supporting)**

Luhn's "Story Spine" — *Once upon a time / Every day / Until one day / Because of that / Until finally / Ever since then* — is a surprisingly effective template for architecture decision records (ADRs), technical blog posts, and postmortems.

### The Technical Story Spine

| Story Element | Technical Equivalent | Example |
|---|---|---|
| *Once upon a time...* | Current state / context | "Our API gateway was a single YARP instance routing all tenant traffic." |
| *Every day...* | The recurring pattern or constraint | "This worked until any single tenant's traffic spike degraded response times for all others." |
| *Until one day...* | The inflection point / incident | "A load test revealed 400ms P99 latency at 1,200 concurrent users." |
| *Because of that...* | What changed and why | "We introduced per-tenant rate limiting at the gateway layer." |
| *Until finally...* | The resolution | "P99 dropped to 80ms and tenant isolation became a hard guarantee." |
| *Ever since then...* | The lasting principle | "All new tenants are onboarded with explicit rate limit profiles." |

This structure should govern: **postmortems, ADRs, design rationale sections, and engineering blog posts**. It is not required for reference documentation (API references, configuration schemas), where structured lists and tables are more appropriate.

***

## Rhetorical Techniques Adapted for Technical Writing

**Borrowed from: Sinek (primary), Robbins (supporting)**

### Lead with the Punchline
Sinek's "Why first" principle aligns with the *inverted pyramid* structure common in journalism: most important information first, supporting detail after. In technical writing, this means:

- Function signatures and return values before parameter tables.
- The decision before the reasoning.
- The constraint before the implementation detail.

### Contrast to Create Clarity
Sinek's use of sharp contrasts (Apple vs. competitors, Wright Brothers vs. Langley) is one of the most transferable rhetorical devices. In technical writing, a bad example illuminates a good one faster than any amount of description.

- **Show the before and after.** For every pattern, show the anti-pattern alongside it.
- **Use comparison tables** when two architectures, libraries, or approaches are being evaluated. Never describe both in prose if a table would do.

### Repetition of Key Terms (Controlled)
Both Sinek and Clear use repeatable frameworks — "The Golden Circle," "The 4 Laws of Behavior Change" — because named frameworks stick. In technical writing, consistent naming of core concepts reduces cognitive load and builds a shared vocabulary across a codebase or team.

- **Name the pattern, then use that name consistently.** If it's a "Boundary Service," call it that everywhere — in code, docs, and conversation.
- **Do not synonym-cycle.** Calling the same thing "the gateway," "the proxy," "the router," and "the middleware" in the same document is not stylistic variation — it is confusion.

### Define Acronyms and Products on First Use

Every acronym, initialism, or named product gets defined on its first use **per chapter**. Readers may enter at any chapter; an undefined term costs them comprehension immediately.

**Acronyms and initialisms** — spell out the full form on first use, with the abbreviation in parentheses:

- "The General Data Protection Regulation (GDPR)" — not bare "GDPR"
- "Conflict-free Replicated Data Types (CRDTs)" — not bare "CRDTs"
- "Mobile Device Management (MDM)" — not bare "MDM"

Subsequent uses within the same chapter use the abbreviation alone.

**Products, projects, and named tools** — establish a brief identifier on first use: what it is, and where to find it (link or short description):

- "Linear ([linear.app](https://linear.app/), the issue tracker)"
- "Figma ([figma.com](https://www.figma.com/), the design tool)"
- "Sunfish (the open-source reference implementation, [github.com/ctwoodwa/Sunfish](https://github.com/ctwoodwa/Sunfish))"

After first introduction, use the bare name within the chapter.

**The rule is per-chapter, not per-book.** A reader who jumps to Chapter 14 should not have to flip back to Chapter 2 for a definition. The cost of one repeated spell-out across chapters is much smaller than the cost of one undefined acronym at a chapter boundary.

**Headings exempt.** Acronyms in section headings or table column headers do not count as first use; spell them out at the first prose occurrence in the section instead.

### Transformational Vocabulary
Robbins' emphasis on vocabulary that shifts mental states maps to a subtle but powerful writing choice: **replace passive/victim vocabulary with agency vocabulary** in technical writing.

| Passive / Ambiguous | Agency-Oriented |
|---|---|
| "This issue was encountered" | "The service fails when..." |
| "It may be necessary to..." | "Restart the container when..." |
| "There are some considerations" | "Three constraints govern this decision" |
| "This could be improved" | "Replace X with Y to reduce latency by ~40%" |

***

## Structural Patterns by Document Type

### Architecture Decision Records (ADRs)
1. **Status** (Proposed / Accepted / Deprecated)
2. **Context** — Why now? What forced this decision? *(Sinek: Why first)*
3. **Decision** — State it in one sentence. *(Clear: Lead with the conclusion)*
4. **Consequences** — Both positive and negative. *(Luhn: Honest about difficulty)*
5. **Alternatives Considered** — Brief; table format preferred. *(Robbins: Contrasting options)*

### Technical Specifications
1. **Purpose** — One paragraph: the problem this solves and who it helps.
2. **Constraints** — What must always be true; what is explicitly out of scope.
3. **Design** — Narrative + diagrams. Use the Story Spine for non-trivial designs.
4. **Interface Contract** — Precise. Tables, typed signatures, example payloads.
5. **Failure Modes** — What breaks and why. Never omit this section.
6. **Migration / Rollout** — Sequenced steps with checkpoints.

### README / Developer Onboarding
1. **One-line purpose** — What problem does this solve?
2. **Quick Start** — Working example in under 5 steps.
3. **Mental Model** — How does this fit into the larger system? *(Sinek: Why)*
4. **Configuration Reference** — Tables, not paragraphs.
5. **Troubleshooting** — Most common failure states and their fixes.

***

## Tone Calibration

The synthesized voice sits at the intersection of:

- **Warm but direct** — Not cold and bureaucratic, not conversational to the point of imprecision.
- **Confident but honest about tradeoffs** — Recommendations are made clearly; limitations are not buried.
- **Purpose-anchored** — Every section connects back to why the reader is here.
- **Human but not performative** — Acknowledge difficulty; do not perform humility or enthusiasm.

### What This Voice Is NOT
- **Not academic.** No passive voice as a default, no hedging as professionalism.
- **Not motivational.** Emotion serves comprehension, not inspiration for its own sake.
- **Not terse to the point of coldness.** Brevity without context is just incomplete.
- **Not verbose as thoroughness.** Length is not a proxy for quality.

***

## Quick Reference: Per-Author Contributions

| Voice Contributor | Core Contribution to This Style |
|---|---|
| **Simon Sinek** | Purpose-first structure (Why → What → How); contrast-based clarity; human-centric framing |
| **Matthew Luhn** | Narrative arc (Story Spine); emotional authenticity; documenting failure states |
| **James Clear** | Radical clarity; systems thinking; named frameworks; active verb discipline |
| **Tony Robbins** | Certainty of tone; agency vocabulary; recommendation-first delivery; contrast as a persuasion tool |
| **Stephen King** | Adverb discipline; the 10% revision cut; trust the reader to assemble the picture from load-bearing details |

***

## Summary Principles

1. **Start with Why.** Every document opens with purpose, not mechanics.
2. **Name the problem before naming the solution.** Context earns attention.
3. **Lead with the conclusion.** Bury nothing important.
4. **Name your patterns and use them consistently.** Shared vocabulary is shared understanding.
5. **Show the anti-pattern.** A bad example is worth a thousand words of description.
6. **Document the failure path.** It is not optional.
7. **Use agency vocabulary.** The system does things; things do not happen to the system.
8. **Cut what doesn't earn its place.** Clarity is a structural obligation. Second draft = first draft minus ten percent.
9. **Trust the reader.** Describe just enough to put the picture in their head; then stop.
10. **Adverbs are usually a tell that the verb is weak.** Replace the noun-verb pair.

***

## Anti-AI Tells — Patterns to Avoid

Modern LLM-generated prose has a recognizable signature: ceremonial openers, copulas swapped for "serves as," vague attributions to "industry observers," forced groups of three, and trailing `-ing` clauses that puff the appearance of consequence without specifying any. These patterns pass technical review and pass active-voice review and *still* mark a chapter as model-authored to readers who have spent a year skimming AI prose.

Seventeen patterns are catalogued in `.claude/skills/anti-ai-tells/SKILL.md` with calibrated rewrites in this book's register and lexical greps for the prose-reviewer to run. Voice agents and the chapter-drafter should consult the skill *during drafting* (not just review) so the patterns do not appear on the first pass. The highest-yield single rules:

- **Restore copulas.** "X **is** Y" beats "X **serves as** a Y" / "X **stands as** a Y" / "X **represents** a Y" / "X **boasts** Y." Strip the elaborate verb when no information is lost.
- **Strip significance puffery.** "Marks a pivotal moment in the evolution of," "stands as a testament to," "the evolving landscape of," "contributing to a broader movement" — these add emotional weight without information. Cut.
- **Strip persuasive authority tropes.** "The real question is," "at its core," "fundamentally," "what really matters" — the book leads with the punchline. These tropes are throat-clearing before the punchline.
- **Watch the AI vocabulary cluster.** *delve, showcase, tapestry, interplay, intricate, pivotal, vibrant, enduring, additionally* — individual words are fine; clusters are a tell.
- **Drop trailing `-ing` clauses that add the appearance of consequence.** "…, highlighting X" / "…, underscoring Y" / "…, fostering Z" — usually replaceable with a second sentence that *names* the consequence.
- **Sentence case for H2/H3/H4.** Title Case in section headings is a tell. Proper nouns and acronyms keep their capitalization.

**Three patterns from the upstream catalog are explicitly NOT applied here** because the book uses them deliberately:

- **Em-dash use is intentional.** Lencioni and Gladwell registers depend on em-dash apposition for rhythm.
- **Boldface emphasis is allowed sparingly** — for vocabulary installations and key-term first-use anchors. Mechanical bullet-bolding is still flagged.
- **Hyphenated technical terms are correct** — `local-first`, `local-node`, `two-act`, `end-to-end` are stable terminology, not tells.

See the skill for the full catalog, calibration notes, and the lexical greps the prose-reviewer runs on every chapter.