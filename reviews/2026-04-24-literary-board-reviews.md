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

---

## Ch01 Second-Pass Review (post failure mode expansion)
**Board score: 7.6/10 — POLISH**

*Context: Ch01 expanded from five to six failure modes. The Third-Party Veto added as a new section; The Dependency Chain named explicitly within The Outage section.*

| Critic | Score | Verdict |
|--------|-------|---------|
| Eleanor Chase (Acquisitions) | 8 | POLISH |
| Marcus Webb (CTO/Target Reader) | 8 | READ |
| Ingrid Halvorsen (Prose) | 7 | SERVICEABLE |
| Jerome Nakamura (Technology Analyst) | 7 | ADEQUATE |
| Dr. Amara Osei (Academic) | 7 | OVERSTATED |
| Meera Krishnamurthy (Dubai/India) | 8 | NEEDS REGIONAL CONTEXT |
| Prof. Raymond Hollis (Rhetoric) | 8 | COHESIVE |
| Sofia Reyes (Accessibility/LATAM) | 7 | PARTIALLY ACCESSIBLE |
| Yuki Tanaka (East Asia/APAC) | 6 | TRANSLATES WITH ADAPTATION |
| Dr. Imogen Barker (European) | 8 | ADEQUATELY SUBSTANTIATED |
| Amina Diallo (African Markets) | 7 | RELEVANT WITH EXPANSION |
| Aleksei Volkov (CIS/Eastern Europe) | 9 | NEEDS CIS CONTEXT |

### Priority Action Items

1. **STRUCTURAL — Third-Party Veto needs a category-shift transition.** The first five failure modes share a vendor-user adversarial structure. The sixth doesn't — external authority, neither party controls. Add one sentence before the section: "The first five failure modes originate inside the service relationship. The sixth does not." Without it, readers may process The Third-Party Veto as another vendor failure rather than a categorically different class.

2. **REGULATORY GEOGRAPHY — East Asian data sovereignty absent.** China PIPL (2021) — stricter than GDPR; Japan PIPA (revised 2022); South Korea PIPA. All absent from both the Third-Party Veto section and "Who Pays the Most." Federal Law 242-FZ should be named explicitly by citation in the Third-Party Veto, not gestured at. Flagged by Tanaka, Volkov, and Krishnamurthy independently.

3. **OVERCLAIMS — Two phrases need qualification.** "Correct merged result" → "deterministically merged result" (CRDTs guarantee convergence, not semantic correctness). "The constraint has been removed" → "the constraint is removable under the assembly described in this book." Both are defensible claims stated at a precision level they can't support.

4. **ACCESSIBILITY PLACEMENT — The AT paragraph is structurally orphaned.** Dropped two paragraphs before the close, it reads as a post-hoc addition. Elevate to a seventh failure mode within the taxonomy, or integrate into The Outage section as a specific consequence for AT users. Chase, Webb, Hollis, and Reyes all identified this independently.

5. **PROOF POINT SCALE — Linear and Actual Budget need scale context.** "Production-proven" requires evidence beyond naming. Add one sentence per product giving scale (user count, deployment context). Flagged by Webb, Nakamura, and Osei.

### Additional items (lower priority)

- Add a bridge sentence between The Third-Party Veto close and "Who Pays the Most" — register shifts from regulatory example to SME vulnerability argument without a transition
- "The Vendor That Disappears" needs a closing beat — the legal firm migration scenario exits without a landing line
- The regulatory survey sentence in "Who Pays the Most" lists eight jurisdictions in one sentence — restructure as two sentences or cut to three most significant with a note
- Break the semicolon chain in the Anthropic/DoD passage — three distinct outcomes deserve three sentences
- Add the Anthropic passage a date anchor ("as of February 2026, the situation was as follows") since the legal sequence may evolve before publication
- Add scale acknowledgment to the 2022 CIS terminations — "hundreds of thousands of organizations" is missing; the current description names the event without establishing its evidentiary weight

### Strengths to preserve

- The Marcus cold open. "100% of the users who matter right now" — do not touch.
- The dependency chain paragraph: "not your vendor failing, but the infrastructure layer beneath your vendor" — precise, original, actionable.
- The Third-Party Veto as a category. The category is the contribution; section needs strengthening, not replacement.
- The global connectivity paragraph — Nigeria, India, rural Brazil, rural Mexico, Southeast Asia named specifically and framed as the global baseline. Praised by five critics independently.
- The "Bundle Nobody Agreed To" structure — three desirable properties, three conditions, the rational acceptance argument.
- Schrems II present and correctly cited in two places.

---

## Ch03 Full Board Review
**Board score: 6.4/10 — REVISE**

*Context: "How This Changes Failure Modes" section rebuilt with three explicit categories: What the inversion resolves (six named resolutions mirroring Ch01), What you may not have noticed you were exposed to (The Security Breach), What the architecture introduces honestly (unchanged).*

| Critic | Score | Verdict |
|--------|-------|---------|
| Eleanor Chase (Acquisitions) | 8 | POLISH |
| Marcus Webb (CTO/Target Reader) | 8 | READ |
| Ingrid Halvorsen (Prose) | 7 | SERVICEABLE |
| Jerome Nakamura (Technology Analyst) | 8 | COMPELLING |
| Dr. Amara Osei (Academic) | 8 | SOUND |
| Meera Krishnamurthy (Dubai/India) | 5 | NEEDS REGIONAL CONTEXT |
| Prof. Raymond Hollis (Rhetoric) | 8 | COHESIVE |
| Sofia Reyes (Accessibility/LATAM) | 4 | PARTIALLY ACCESSIBLE |
| Yuki Tanaka (East Asia/APAC) | 5 | TRANSLATES WITH ADAPTATION |
| Dr. Imogen Barker (European) | 7 | ADEQUATELY SUBSTANTIATED |
| Amina Diallo (African Markets) | 3 | MISSES MAJOR MARKET |
| Aleksei Volkov (CIS/Eastern Europe) | 4 | LARGEST CASE STUDY ABSENT |

### Priority Action Items

1. **Name the 2022 SaaS service terminations in the Third-Party Veto resolution.** The resolution section says "Government or regulatory action targeting a vendor can interrupt service to every customer downstream." It does not name the 2022 terminations as the most documented recent example. Ch01 names them. Ch03 does not. This is the asymmetry. Flagged by Volkov, Krishnamurthy, Barker, Diallo.

2. **Expand regulatory naming beyond HIPAA/GDPR.** "Data sovereignty requirements" without names is empty. Add at minimum: Schrems II (strongest EU compliance argument — name it explicitly, not just "compliance framework"), DIFC Data Protection Law / UAE DPL 2022, POPIA / NDPR / Kenya DPA, Federal Law 242-FZ, Japan PIPA / China PIPL. A sidebar or list paragraph naming the key laws by jurisdiction resolves this without body rewrite.

3. **SunfishNodeHealthBar accessibility specification.** The HealthBar's four states are described with no mention of MAUI SemanticProperties or live region announcements for state transitions. WCAG 2.1 requires that state information be available through more than color. For a chapter that names the HealthBar and its states by name, this creates an obligation. Add two sentences: one naming SemanticProperties.Description as the AT mechanism, one naming live region announcement for state transitions. Detail in Part III.

4. **Cut four of the five layer-closing "when network is unavailable" refrains.** By Layer 5, this reads as authorial anxiety. Keep the Layer 1 instance as the governing statement; cut the rest. Flagged by Chase, Webb, and Halvorsen independently.

5. **Anchor Security Breach paragraph in the DEK/KEK key architecture.** "Relay holds ciphertext only" needs its technical basis stated: the relay receives only post-encryption deltas sealed under keys it does not hold — reference the DEK/KEK/Argon2id hierarchy from Layer 4. One sentence makes the claim falsifiable rather than asserted. Flagged by Webb and Barker.

### Additional items (lower priority)

- Add bridge sentence between opening inversion and five-layer walkthrough framing the layer detail as proof-of-concept, not interruption: "The inversion is one sentence. The five-layer model is why that sentence is implementable."
- Add explicit rhetorical purpose sentence to the Anchor/Bridge section explaining why two deployment shapes appear in the architectural chapter rather than Ch04
- Reconcile the chapter title with its content — promises "one diagram," delivers five sections; candidate retitles: "The Inverted Stack: Architecture and Failure Modes" or "How the Stack Inverts"
- Add at least one African fintech precedent (M-PESA, MTN MoMo) as proof of the architecture's real-world deployment at scale before this book
- Add Japan PIPA, China PIPL to the Third-Party Veto resolution section
- Name Nigeria NDPR, Kenya DPA, POPIA in the Data resolution section
- Acknowledge that SIer-mediated procurement (Japan, Korea) and relationship-led procurement (India BFSI, GCC) differ from the product-led model embedded in the book's GTM assumptions

### Strengths to preserve

- The three-tier failure mode structure (resolves / hidden exposure / introduces honestly) — the chapter's structural achievement. Do not flatten.
- "This is the inversion. Everything else is implementation." — Do not move or edit.
- The Security Breach paragraph — best paragraph in the chapter. "Invisible until it has already happened; you cannot evaluate a vendor's internal security posture from outside it" is exactly right.
- The CAP positioning table — correctly reasoned, every row defensible, "Why" column earns its place. Keep every row.
- "The relay's failure is not the application's failure." — Keep as written.
- "Part II is six rounds of adversarial review by people who were looking for exactly these problems." — Clean transition. Do not revise.
- "What Changes for the Developer" section's three declarative subheadings — good paragraph architecture throughout.

---

## Ch01 Third-Pass Review (post priority board fixes)
**Board score: 8.3/10 — POLISH**

*Context: Priority fixes applied: 242-FZ qualifier added; China PIPL and South Korea PIPA added to regulatory survey; "correct merged result" → "deterministically merged result" + convergence clarification; "The constraint has been removed" → "The constraint is removable — by the architecture this book describes"; AT paragraph moved from orphaned closing position into The Outage section as its conclusion; orphaned AT paragraph removed from closing section; scale context added for Linear and Actual Budget.*

| Critic | Score | Verdict |
|--------|-------|---------|
| Eleanor Chase (Acquisitions) | 9 | POLISH |
| Marcus Webb (CTO/Target Reader) | 8 | READ |
| Ingrid Halvorsen (Prose) | 8 | FLOWING |
| Jerome Nakamura (Technology Analyst) | 8 | COMPELLING |
| Dr. Amara Osei (Academic) | 8 | SOUND |
| Meera Krishnamurthy (Dubai/India) | 9 | GLOBALLY POSITIONED |
| Prof. Raymond Hollis (Rhetoric) | 9 | COHESIVE |
| Sofia Reyes (Accessibility/LATAM) | 8 | INCLUSIVE |
| Yuki Tanaka (East Asia/APAC) | 8 | TRANSLATES WITH ADAPTATION |
| Dr. Imogen Barker (European) | 9 | RIGOROUS |
| Amina Diallo (African Markets) | 8 | RELEVANT WITH EXPANSION |
| Aleksei Volkov (CIS/Eastern Europe) | 8 | NEEDS CIS CONTEXT |

### Priority Action Items

1. **SCALE THE 2022 CIS TERMINATIONS.** "Adobe, Autodesk, Microsoft, Figma, and dozens of others" names the event but not its evidentiary weight. "Hundreds of thousands of organizations" — or a verified figure — converts the example from illustrative to structural evidence. Flagged by Volkov (all three passes), Webb (Passes 2 and 3), Nakamura (Pass 3). Highest-priority remaining fix.

2. **RESTRUCTURE ANTHROPIC/DOD SEMICOLON CHAIN.** Four distinct events share one sentence. Break into three: executive order; Anthropic's legal challenge and civilian injunction; DoD exclusion. Add date anchor ("In February 2026..."). Flagged by Chase, Halvorsen, Hollis.

3. **ADD BRIDGE SENTENCE BETWEEN THIRD-PARTY VETO AND "WHO PAYS THE MOST."** Register shifts from geopolitical restriction to SME leverage without a hinge. Flagged by Chase, Nakamura, Hollis across two passes.

4. **RESTRUCTURE REGULATORY SURVEY INTO ARGUMENT.** Twelve jurisdictions in continuous prose is a catalog. Name the claim first, anchor with two or three examples, close with structural consequence. Flagged by Halvorsen, Hollis, Reyes, Barker.

5. **ADD M-PESA / MTN MOMO AS OFFLINE-FIRST PRECEDENTS.** African fintech deployed offline-first architecture at continental scale fifteen years before this book. Their absence makes the commercial proof section US/European-only. One sentence in "Why Users Have Accepted This" or the technology section. Flagged by Diallo in all three passes.

### Additional items (lower priority)

- Add DIFC-specific data residency constraints alongside UAE DPL 2022 (Krishnamurthy)
- Add Colombia and Argentina data protection laws alongside LGPD (Reyes)
- Qualify "first major data localization law globally" — consider "among the first general-purpose" to cover potential pre-2015 sectoral laws (Osei, Barker)
- Add Relay self-hostability sentence for European procurement readers (Barker)
- Add one sentence noting SCCs remain legally contested under Schrems II (Barker)
- Add import substitution acknowledgment as demand driver in CIS markets (Volkov)
- Verify 242-FZ "first global" claim; verify Actual Budget architecture currency (Osei)
- Confirm AT paragraph mechanism: "because data is local, the application has a data source regardless of network state" (Reyes)

### Strengths to preserve

- Marcus cold open and bookend close. "100% of the users who matter right now" / "His data was never gone. It was inaccessible because the software's design placed it somewhere he couldn't reach." Unanimous — do not touch.
- "The Bundle Nobody Agreed To" three/three parallel structure. "The bundle reveals itself over time, after the switching costs have accumulated." Preserve exactly.
- "The constraint is removable — by the architecture this book describes." Correctly hedged; keep exactly.
- Global connectivity paragraph — "does not have a niche offline problem... excludes the majority of the world's enterprise users from full functionality." Unanimous praise — do not touch.
- AT paragraph as placed in The Outage section — correctly positioned, correctly scoped.
- "Deterministically merged result" + convergence/semantic intent clarifying sentence. Carry forward to every subsequent chapter that discusses CRDTs.
- The Third-Party Veto transition: "The first five failure modes originate inside the service relationship. The sixth does not." Structurally essential.
- "In each of these jurisdictions... it is the architecture that makes compliance tractable." Best sentence added in this revision cycle. Do not dilute.

---

## Ch03 Second-Pass Review (post priority board fixes)
**Board score: 7.8/10 — POLISH**

*Context: Priority fixes applied: Third-Party Veto resolution leads with 2022 CIS terminations; regulatory naming paragraph added after six resolutions; HealthBar accessibility spec added (SemanticProperties + live region + Ch20 forward ref); Layer 2, 3, 4 closing refrains cut; Layer 5 trimmed to "The relay's failure is not the application's failure."; Security Breach anchored in DEK/KEK/Argon2id hierarchy.*

| Critic | Score | Verdict |
|--------|-------|---------|
| Eleanor Chase (Acquisitions) | 8 | POLISH |
| Marcus Webb (CTO/Target Reader) | 8 | READ |
| Ingrid Halvorsen (Prose) | 8 | FLOWING |
| Jerome Nakamura (Technology Analyst) | 7 | COMPELLING |
| Dr. Amara Osei (Academic) | 7 | SOUND |
| Meera Krishnamurthy (Dubai/India) | 8 | GLOBALLY POSITIONED |
| Prof. Raymond Hollis (Rhetoric) | 7 | COHESIVE |
| Sofia Reyes (Accessibility/LATAM) | 8 | INCLUSIVE |
| Yuki Tanaka (East Asia/APAC) | 7 | TRANSLATES WITH ADAPTATION |
| Dr. Imogen Barker (European) | 8 | RIGOROUS |
| Amina Diallo (African Markets) | 7 | RELEVANT WITH EXPANSION |
| Aleksei Volkov (CIS/Eastern Europe) | 9 | GLOBALLY COMPLETE |

### Priority Action Items

1. **WRITE THE BRIDGE SENTENCE between the inversion thesis and the five-layer walkthrough.** Three critics (Chase, Halvorsen, Hollis) independently identified this as the chapter's structural gap. "Why am I about to read a five-layer specification?" Answer: the thesis requires a proof of implementability; the five layers are that proof.

2. **ADD AFRICAN FINTECH PRECEDENT (M-PESA, MTN MoMo) as operational proof of the connectivity argument.** One sentence in the Connectivity resolution or Layer 3 section transforms the offline-first argument from theoretical to proven at continental scale. Flagged by Diallo across both passes.

3. **REFRAME "FIELD DEPLOYMENTS" AS GLOBAL BASELINE.** "Intermittent, sometimes slow connections that field deployments encounter" is US-centric framing. Replace with language acknowledging intermittent connectivity as the baseline condition for hundreds of millions of enterprise workers. Flagged by Krishnamurthy, Reyes, Tanaka, Diallo.

4. **CONFIRM WRITE-BUFFER SURVIVES POWER INTERRUPTION.** The daemon buffers writes to durable local storage; the chapter says it survives app restarts but does not confirm power interruption. One sentence closes this for African enterprise contexts. (Diallo)

5. **ADD REGULATORY ATLAS COMPLETIONS.** LGPD and LFPDPPP for Latin America (Reyes); South Korea PIPA (Tanaka); BSI/CNIL for European enforcement context (Barker). Two to three sentences total.

### Additional items (lower priority)

- Add import substitution (импортозамещение) acknowledgment as adoption driver (Volkov)
- Delete "without flinching" from CRDT GC paragraph (Halvorsen)
- Cut parenthetical list from CP-class prose sentence in Layer 2 — duplicates the table that follows (Halvorsen)
- Add bridge sentence from Third-Party Veto to regulatory atlas acknowledging geography isn't the risk — structural dependency is (Nakamura)
- Add one honest sentence acknowledging Bridge deployment complexity (per-tenant host processes, isolation) beyond "one system, two shapes" (Nakamura)
- Add one sentence on relay self-hostability and protocol openness for European procurement due diligence (Barker)
- Add key-management compelled-access threat model sentence to Security Breach paragraph (Volkov)
- Audit "What Changes for the Developer" — may collapse into Anchor/Bridge final paragraph (Chase, Hollis)
- Source or justify "90-day retention" GC parameter (Webb)
- Source Flease 30-second default vs. Sunfish implementation default (Osei)
- Add formal correctness annotation for Flease (mutual exclusion with bounded lease expiry) for Japanese/German technical readers (Tanaka, Osei)

### Strengths to preserve

- The diptych structure (Ch01 six failure modes ↔ Ch03 six named resolutions). Do not flatten.
- "This is the inversion. Everything else is implementation." Do not move or edit.
- The Security Breach paragraph — "Invisible until it has already happened" plus DEK/KEK specification. The best paragraph in the chapter. Chase, Osei, Barker all noted improvement.
- "The relay's failure is not the application's failure." Nine words. Perfect.
- The CAP-per-record-class table. Multiple critics cited this as the most actionable single element.
- The three-tier peer discovery hierarchy (mDNS → WireGuard → relay). Unchallenged by any critic.
- The event log as ground truth, projections as optimization. Unchallenged.
- "The software works." Layer 1 offline close. Keep.
- "Part II is six rounds of adversarial review by people who were looking for exactly these problems." Clean transition. Do not revise.
- Third-Party Veto resolution leading with 2022 CIS terminations — editorially restrained, analytically precise. Do not elaborate further.
- HealthBar accessibility spec (SemanticProperties.Description + live region + Ch20 forward ref). Correctly placed and scoped. Reyes noted this as the right treatment for Chapter 3.
