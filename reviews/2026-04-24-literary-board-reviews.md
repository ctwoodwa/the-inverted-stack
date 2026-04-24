# Literary Board Review Session — 2026-04-24

## Ch01 Full Board Review
**Board score: 6.2/10 — POLISH**

| Critic | Score | Verdict |
|--------|-------|---------|
| Eleanor Chase (Acquisitions) | 8 | POLISH |
| Marcus Webb (CTO/Target Reader) | 7 | READ |
| Ingrid Halvorsen (Prose) | 8 | FLOWING |
| Jerome Nakamura (Technology Analyst) | 7 | ADEQUATE |
| Dr. Amara Osei (Academic) | 6 | OVERSTATED |
| Meera Krishnamurthy (Dubai/India) | 5 | WESTERN-CENTRIC |
| Prof. Raymond Hollis (Rhetoric) | 8 | COHESIVE |
| Sofia Reyes (Accessibility/LATAM) | 4 | PARTIALLY ACCESSIBLE |
| Yuki Tanaka (East Asia/APAC) | 5 | TRANSLATES WITH ADAPTATION |
| Dr. Imogen Barker (European) | 6 | LACKS EUROPEAN PRECISION |
| Amina Diallo (African Markets) | 4 | MISSES MAJOR MARKET |

### Priority Action Items

1. **Expand connectivity globally.** Add Sub-Saharan Africa (load-shedding — 6-12 hour daily power cuts in Lagos as operational baseline), rural India (4G/3G/2G gradient, hundreds of millions of enterprise workers), rural Brazil/LATAM, Southeast Asia. "Not everyone's internet is always on" understates the scale by an order of magnitude.

2. **Expand regulatory narrative.** Add to "Who Pays the Most": India DPDP Act 2023, UAE Data Protection Law 2022, Schrems II (EU court ruling constraining US cloud providers — the strongest EU legal argument for local-first data residency), Nigeria NDPC/NDPR, South Africa POPIA, Japan PIPA, Brazil LGPD.

3. **Untangle Figma CRDT claim.** Figma uses CRDTs as a sync optimization; data resides on Figma's servers — it is not a data-sovereignty architecture. Conflating CRDTs-as-sync with local-first-as-sovereignty undermines the argument. Replace with Linear (local SQLite replica) and Actual Budget, or qualify explicitly.

4. **Acknowledge tradeoffs in one sentence.** The chapter reads as advocacy without it. One sentence: operational complexity, deployment burden, and upgrade management replace vendor dependency. The book addresses each — the acknowledgment earns trust from skeptical readers.

5. **Add the accessibility advantage paragraph.** AT users (screen readers, switch access, voice control) experience SaaS connectivity failure as complete access failure. Local-first keeps the application responsive regardless of network state. Untapped argument, real, adds a constituency.

### Additional polish (lower priority)

- Replace "blueprint" (final paragraphs) with "reference architecture" or "implementation specification"
- Cut organizational statement: "The rest of this chapter is about what it costs before we reach that — and who pays the most"
- Convert "The Data You Can't Get Back" bulleted list to prose sentences
- Tighten the Quip passage to one sentence; use the space to land a structural claim about the custody model
- Rewrite chapter handoff ("Chapter 2 maps... Chapter 3 shows") as a forward pull, not navigation labels
- Add one sentence at scene open establishing Marcus is representative, not exceptional

### Strengths to preserve

- Marcus opening scenario and bookend close ("His data was never gone. It was inaccessible because the software's design placed it somewhere he couldn't reach.")
- "The Bundle Nobody Agreed To" framing — original, teachable, quotable
- "They weren't accepting a bargain so much as acknowledging a constraint. The constraint has been removed." — most rhetorically sophisticated sentence in the chapter
- "Who Pays the Most" section structure and stakes framing
- Three-part technology section (CRDTs, gossip, local service pattern) — commercial proof strategy is right for the audience
- Distinction between declared outages and degraded performance that reads as user error

---

## Hollis Full Manuscript Review
**Score: 7/10 — EPISODIC**

### Findings

**Structural strength:** Part I earns its premise cleanly. The arc (instance → principle → manifestations → stakes → constraint removal) is persuasively sequenced. Part III holds together as specification. The epilogue earns its place — "What the Stack Owes You" reframes requirements as obligations, which is the correct register for a closing argument.

**Critical seam — Ch10 verdict reveal:** Ch10 opens by announcing the council approved the architecture, which kills the dramatic tension before it begins. Restructure: reveal conditions first, pattern second, conclusion last.

**Critical seam — Part II to Part III transition:** The adversarial narrative stops abruptly and a reference manual begins. A 200-300 word bridge passage at the start of Ch11 or as a Part III preamble is needed. "You have watched the architecture fail and survive; now here is what it actually is."

**Voice fragmentation:** The authorial "I" from the preface disappears in Parts III and IV. Part IV needs a sentence or two connecting back to Ch1 or the council.

**Sunfish implementation-state references:** Wave numbers and "working now / still placeholder" lists in Ch17-20 will read as broken promises within 12 months. Either move to a separate project document or reframe as architectural intent.

### Action Items

1. Restructure Ch10 to not open with the verdict — conditions → pattern → conclusion
2. Write 200-300 word bridge at start of Ch11 (or Part III preamble) acknowledging the register shift
3. Restore authorial voice in Part IV — one or two sentences connecting back to Ch1 or the council
4. Audit Sunfish implementation-state references in Ch17-20 for reader durability

---

## Barker Ch11 Review
**Score: 7/10 — ADEQUATELY SUBSTANTIATED**

Ch11 is strong by US technical standards. Three gaps for European precision:

### Action Items

1. **Relay governance paragraph** (in Process Boundaries or peer discovery section): specify whether relay transit is mandatory or optional for cross-segment connectivity; what the relay observes vs routes; under what jurisdiction the managed relay operates. For EU enterprise buyers evaluating Schrems II, the relay is where the sovereignty argument could collapse.

2. **Flease quorum formula + asymmetric partition failure mode:** Current text describes the happy path. Add: the quorum formula (majority of reachable peers, or configurable threshold); what happens when an asymmetric partition means one node sees quorum and another does not and both attempt the same CP-class write before the partition heals.

3. **Schrems II callout paragraph:** The architecture is a textbook Schrems II compliance answer. Name it. Data minimisation invariant (subscription filtering at send, not receive), local key hierarchy, send-tier filtering — these map directly to GDPR Chapter V transfer mechanism requirements. The managed relay routes ciphertext only. A paragraph making this explicit converts a technical description into a European procurement argument.
