# Kleppmann Council Review — Round 1
**Document:** `chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md`
**Date:** 2026-04-29
**Stage at review:** `icm/prose-review` (per file header)
**Word target:** ~5,200 (anatomy reports ~9,970 tokens — chapter is roughly on-budget)

> Note on seat mapping. The user requested the five seats as Theorist / Production Operator / Skeptical Implementer / Pedantic Lawyer / Outside Observer. I am mapping these onto the standing Kleppmann Council membership as follows, since this is a Part I narrative chapter (not an architecture document) and the original seats' adversarial postures map cleanly:
>
> - **Theorist** → Prof. Dmitri Shevchenko (academic / theoretical correctness — for Ch01, theoretical correctness of the *failure-mode taxonomy* and of distributed-systems claims made in passing)
> - **Production Operator** → Dr. Marguerite Voss (ops + reliability lens — outage anatomy, SLA realism, IT custody framing)
> - **Skeptical Implementer** → Tomás Ferreira (engineer-shipping perspective — "does this match what I have actually seen ship?")
> - **Pedantic Lawyer** → Nia Okonkwo, repurposed (compliance / regulatory / IP — Schrems II, DPDP, sanctions, professional responsibility)
> - **Outside Observer** → Jordan Kelsey (audience accessibility / argumentative cohesion — does this land for a CISO? a working engineer? a non-specialist? does the argument carry?)
>
> Each seat is reviewed in their own voice, against their own dimensions, with their own verdict gate.

---

## SEAT 1 — Theorist (Prof. Dmitri Shevchenko)
*Lens: theoretical correctness of claims, failure-mode taxonomy soundness, honesty about distributed-systems primitives invoked in passing.*

### DIMENSION SCORES

| # | Dimension | Score | One-sentence rationale |
|---|---|---|---|
| D1 | Failure-mode taxonomy soundness (MECE) | 6 | Six modes are presented as an exhaustive set but they are not mutually exclusive (outage and connectivity overlap heavily, vendor-disappears and price-changes are two faces of the same custody problem) and they are not collectively exhaustive (data corruption / silent divergence is missing). |
| D2 | CRDT claim accuracy (lines 193) | 7 | The claim that "the merge algorithm guarantees convergence; whether the result reflects the users' semantic intent is a property of how the application models its domain" is correct and unusually honest for a Part I chapter, but it is buried in the closing section rather than landing as a load-bearing caveat. |
| D3 | Gossip-protocol claim accuracy (line 195) | 5 | "Cassandra and DynamoDB operate at planetary scale using these mechanisms. On a five-person team with five workstations, the same protocols work without any cloud relay at all" elides that Cassandra/DynamoDB operate gossip *plus* hinted-handoff *plus* read-repair *plus* tunable consistency — a five-workstation deployment without those companion mechanisms is not the "same protocols" working at small scale. |
| D4 | SLA arithmetic correctness (line 41) | 8 | "99.9% uptime — roughly 8.7 hours of downtime per year" is correct (8.76h); the "scatters harmlessly across the calendar" framing for individuals vs. teams is a sound framing of expected-value vs. tail-risk. |
| D5 | Honest-limits posture on architectural alternative | 6 | The chapter names "operational complexity, key management, schema migration across independent nodes, and upgrade coordination" as costs (line 199), but does so in a single sentence at the end; the cost paragraph is half a sentence and Part I should not let the reader exit Ch01 thinking the inverted stack is *only* upside. |
| D6 | Distinction between availability, durability, partition-tolerance | 5 | The chapter conflates availability ("the platform is down") with accessibility ("Marcus cannot reach his data") with portability ("the data is exportable but not usable") — these are three distinct properties and merging them into "your data is inaccessible" obscures what is actually being claimed. |
| D7 | Asymmetry claim ("falls hardest on moments that matter most," line 45) | 7 | Plausibly true and well-stated, but presented as a structural property when it is an empirical regularity; the chapter does not cite any incident postmortem or availability study to ground it. |
| D8 | Theoretical novelty acknowledgment | 6 | The chapter implies the failure-mode taxonomy is the book's contribution but does not flag that vendor-shutdown / lock-in / data-portability concerns have been catalogued before (Doctorow on enshittification, Kleppmann's *Local-First Software* essay, Ink & Switch's cataloguing). The framing reads as if this is new ground — it is not. |

**DOMAIN AVERAGE: 6.25 / 10**

### BLOCKING ISSUES

- **B1 (Theorist):** The "six failure modes" are presented to the reader as a taxonomy but are not MECE. *Outage* (mode 1) and *connectivity* (mode 3) overlap so heavily that the same incident — Marcus on a job site with no cell signal *and* a cloud platform that requires it — is simultaneously both modes. *Vendor disappears* (mode 2) and *price changes* (mode 5) are two manifestations of the same vendor-custody problem, not two independent failure modes. And the taxonomy is missing at least one common mode: **silent data corruption / divergence** — the case where the SaaS does not go down, does not get acquired, does not raise prices, but quietly mangles your data (Salesforce duplicate-record problem, Notion sync bugs that lose blocks, Airtable formula recomputation losing edits). A Part I chapter that promises a taxonomy of "six ways SaaS breaks in the field" must either (a) be MECE, or (b) explicitly acknowledge it is enumerating *categories of pain* rather than asserting an orthogonal taxonomy.

### CONDITIONS

- **C1:** Add an explicit data-corruption / silent-divergence failure mode, OR rewrite the section header to "Six pains of the SaaS bundle" / "Six ways SaaS lets users down" so the chapter is not making a taxonomic claim it cannot defend.
- **C2:** Tighten the Cassandra/DynamoDB analogy (line 195). State plainly that planetary-scale gossip relies on companion mechanisms, and that the small-deployment claim is "the same *family* of protocols," not "the same protocols."
- **C3:** Pull the cost-acknowledgment sentence (line 199) into its own short paragraph. Part I owes the reader an honest signal that the architecture has costs *before* it sends them into Part II.

### COMMENDATIONS

- The CRDT correctness vs. semantic-intent caveat at line 193 is genuinely well-stated and rare for a popular-press technical chapter.
- The "what gets called an outage vs. degraded performance" framing at line 43 is a real observation about the operational sociology of SLAs, not just a complaint.

### VERDICT: **REVISE**

Domain average is below the 8.0 PROCEED threshold and there is one blocking taxonomic issue. The chapter's argumentative core — that SaaS has structural failure modes that custody architecture addresses — survives the review, but the "six failure modes" framing is doing more work than the modes can support. Either rewrite as "common pains" (low-cost fix) or add the missing data-corruption mode and disambiguate the overlap (higher-cost fix).

---

## SEAT 2 — Production Operator (Dr. Marguerite Voss)
*Lens: ops + reliability — outage anatomy, IT custody framing, real procurement signal, MDM realism in passing.*

### DIMENSION SCORES

| # | Dimension | Score | One-sentence rationale |
|---|---|---|---|
| D1 | Outage anatomy realism (lines 41–51) | 9 | The "degraded performance" vs. "outage" distinction at line 43 is exactly how it lands in the SOC, and the AT-user paragraph (line 51) is the kind of operational truth most architecture books skip. |
| D2 | Cloud-region cascade framing (line 49) | 8 | "AWS us-east-1 availability zone failure affects every product hosted there" is correct in spirit; tightening would name a real incident (June 2023 us-east-1, December 2021 us-east-1) and give the reader a date to anchor on. |
| D3 | Vendor-shutdown realism (lines 55–67) | 8 | Sunrise (2015→2016), Quip (Salesforce deprioritization), Evernote, Google Reader (2013) are the right reference incidents and the export-format paragraph (line 63) is operationally accurate. |
| D4 | Connectivity-edge realism (lines 71–85) | 9 | Construction concrete frame, rural broadband, hospital RF restrictions, manufacturing/defense air-gap, M-PESA/MTN MoMo, India 4G/3G/2G gradient — this is the strongest section in the chapter operationally and reads as written by someone who has actually worked in those environments (or talked to people who have). |
| D5 | IT-helpdesk implication | 5 | The chapter does not address what local-first means for the helpdesk: who supports the local node when it breaks, what the support model looks like for "the user deleted the container," what change-management looks like for a node update. Part I is allowed to defer this to Parts III/IV — but a one-sentence flag would protect against the CISO closing the book at line 200. |
| D6 | Compliance pathway honesty | 7 | Schrems II, Russia 242-FZ, India DPDP are correctly named and the pointer to Appendix F is appropriate; Sunrise's iCal-but-unmappable detail (line 55) is exactly the right level of forensic specificity. |
| D7 | Workaround anatomy (lines 137–145) | 9 | *The Pitt* episode used as a case is a strong choice — it carries operational weight, the felt-tip / carbon-paper / triplicate detail lands, and the "domain expertise outlasts the software" / "but the digital affordances did not survive" two-observation structure (line 141) is exactly the kind of distinction the operator audience cares about. |
| D8 | Honest-limits on the alternative | 6 | The chapter says "the architecture has real costs" (line 199) but does not enumerate the operator-relevant costs: who patches the local node, who handles the SBOM, what the incident-response model looks like when a node is compromised. Part I should not own those answers but should *flag* that they are real questions. |

**DOMAIN AVERAGE: 7.6 / 10**

### BLOCKING ISSUES

- **None.** No falsifiable correctness gap at the operator-lens level.

### CONDITIONS

- **C4:** Anchor the "us-east-1" cascade claim (line 49) to a real, dated incident. The reader who lived through December 2021 will trust the chapter more if it names the incident; the reader who did not gets a citation to look up.
- **C5:** Add one sentence in the closing section flagging that the inverted stack creates *new* operator-relevant questions (helpdesk model, patch cadence, key custody), with an explicit pointer to Parts III–IV. This is honest-limits hygiene; right now Part I lets the reader exit thinking the alternative is operationally free.
- **C6:** Consider naming one or two specific availability-statistic studies for line 41 ("Major SaaS providers report 99.9% uptime"). The number is correct but the source is unattributed; a CISO reader will want a citation to bring to procurement.

### COMMENDATIONS

- The AT-user paragraph at line 51 is the strongest single operational observation in the chapter.
- *The Pitt* / EHR-downtime case (lines 137–145) is excellent — it is a recent, specific, culturally resonant anchor that makes the abstract argument concrete without being maudlin.
- The "drawer of paper backup forms" framing at line 145 lands as a true claim about resilience design, not as a rhetorical flourish.

### VERDICT: **PROCEED WITH CONDITIONS**

Domain average 7.6 is below the strict 8.0 PROCEED bar but well above the 6.0 condition floor, with no blocking issues. The operator lens is the strongest of the five for this chapter; the conditions are about anchoring claims, not about repairing them.

---

## SEAT 3 — Skeptical Implementer (Tomás Ferreira)
*Lens: engineer-shipping perspective — does this match what I have actually seen ship? Does it cite the actual existing local-first work? Does it overclaim what CRDTs / gossip / containers actually deliver in practice?*

### DIMENSION SCORES

| # | Dimension | Score | One-sentence rationale |
|---|---|---|---|
| D1 | Linear / Actual Budget characterization (lines 185, 193) | 8 | "Linear runs its sync engine on a local SQLite replica; the cloud is already demoted to a relay peer" is approximately right and the Actual Budget characterization is fair; Linear is not, however, fully data-sovereign — saying "the cloud is already demoted to a relay peer" overshoots Linear's actual architecture. |
| D2 | Figma disambiguation (line 193) | 9 | Calling out that Figma uses CRDTs for cursors but is NOT a data-sovereignty architecture is exactly the disambiguation the local-first community has been begging mainstream coverage to make for five years; this is a real win. |
| D3 | Automerge / Yjs reference handling (line 193) | 7 | Both libraries are correctly named and linked, but the chapter does not name Loro (the book's own aspirational target per CLAUDE.md) or any of the recent CRDT work that has actually changed the ergonomics (Yjs binary protocol, Automerge 2's Rust core); a reader who knows the space will notice. |
| D4 | M-PESA / MTN MoMo as local-first proof point (line 185) | 6 | This is a legitimate analogy but it is a stretch — M-PESA is store-and-forward against a central authority (the operator's switch), not peer-to-peer with eventual convergence. Calling it "local-first architecture has operated at population scale for nearly two decades" is true *if* you adopt a generous definition of local-first, false on the strict Kleppmann-essay definition. |
| D5 | Linear-as-proof-point honesty | 5 | Linear is the load-bearing example for "the desirable half of the SaaS bundle does not require vendor data custody to function" (line 185), but Linear *does* require vendor data custody — Linear's data is on Linear's servers. Linear's *engine* is local; its *custody* is not. The chapter conflates engine-locality with custody-locality, which is exactly the conflation Ch02 is supposed to argue against. |
| D6 | Container-runtime claim (line 197) | 8 | The "VS Code language servers, 1Password helper, Tailscale daemon" parallel is the right one and lands well; this is the section a working engineer will read and think "yes, this is already shipping." |
| D7 | Sync-conflict / merge-correctness honesty | 6 | The chapter says CRDTs deliver "deterministically merged result — no data loss, no manual conflict resolution" (line 193), and then in the next clause partially walks it back ("whether the result reflects the users' semantic intent is a property of how the application models its domain"). The walk-back is correct but the headline is overclaim — "no manual conflict resolution" is exactly what every shipping local-first app eventually has to expose to the user (see Automerge's own docs on this). |
| D8 | Prior-art acknowledgment | 7 | The chapter cites Kleppmann's *Local-First Software* essay implicitly through framing but does not name it; Ink & Switch is unmentioned; Couch/PouchDB unmentioned; Replicache unmentioned. This is a Part I chapter so encyclopedic citation is not required, but a single forward-pointer to "Chapter 2 reviews the prior art" would help a reader who knows the space. |

**DOMAIN AVERAGE: 7.0 / 10**

### BLOCKING ISSUES

- **B2 (Skeptical Implementer):** The chapter uses Linear and Actual Budget as commercial proof points that "the desirable half of the SaaS bundle — collaboration, sync, responsive UI — does not require vendor data custody to function" (line 185). Actual Budget supports this claim. Linear does not — Linear's data lives on Linear's servers and Linear is exactly the SaaS-with-local-engine pattern that the rest of the book argues is *insufficient*. Using Linear as the load-bearing proof point for data-sovereignty in Ch01, when Ch02–Ch04 will turn around and argue that engine-locality without custody-locality is precisely the gap, undermines the chapter's argumentative spine. Either (a) demote Linear from "proof point for data sovereignty" to "proof point that sync engines can run locally even inside a SaaS architecture" and lean harder on Actual Budget, or (b) replace Linear with a stronger custody-local example (Anytype, Logseq, Obsidian Sync).

### CONDITIONS

- **C7:** Soften the CRDT "no manual conflict resolution" claim at line 193. Every shipping local-first app exposes some merge UX eventually; a reader who has built one will close the book at this sentence. The fix is one clause: "...no data loss, and conflict resolution that the application can either auto-merge or surface to the user as a structured choice."
- **C8:** Either name Loro (Sunfish's aspirational target) alongside Automerge / Yjs, or note explicitly that the CRDT library landscape is broader than these two; the omission of Loro from a book whose reference implementation targets it is jarring.
- **C9:** Tighten the M-PESA framing — call it "store-and-forward transaction patterns at population scale" rather than "local-first architecture," because the strict-definition reader will catch the stretch.

### COMMENDATIONS

- The Figma disambiguation at line 193 is the single best paragraph in the chapter for the local-first practitioner audience.
- The container-runtime / VS-Code-language-server analogy at line 197 lands cleanly with the working-engineer audience.
- The closing acknowledgment that the alternative has costs (line 199) is in the right place even if too brief.

### VERDICT: **REVISE**

Domain average 7.0 is in conditions territory, but B2 (the Linear-as-data-sovereignty conflation) is a falsifiable correctness gap that undermines the chapter's argumentative foundation. The fix is small in word-count but load-bearing. Without it, the chapter sets up an argument that Ch02–Ch04 are then forced to walk back.

---

## SEAT 4 — Pedantic Lawyer (Nia Okonkwo, repurposed for compliance/regulatory/IP lens)
*Lens: legal precision in regulatory citations, professional-responsibility framing, claim-vs-evidence discipline on legal arguments.*

### DIMENSION SCORES

| # | Dimension | Score | One-sentence rationale |
|---|---|---|---|
| D1 | Schrems II characterization (line 127) | 9 | "constrained EU organizations from transferring personal data to US cloud providers without adequate supplemental safeguards" is correctly framed — it does not overclaim that Schrems II banned transfers, which is the most common mischaracterization. |
| D2 | Russia 242-FZ characterization (line 127) | 8 | Correct that 242-FZ predates GDPR ("by two years" — the law took effect in September 2015, GDPR adopted April 2016 effective May 2018, so "two years" is approximately right but loose). The "first general-purpose data localization law" claim is contestable (South Korea's PIPA 2011 has localization-adjacent provisions); recommend either citing or softening. |
| D3 | India DPDP characterization (line 127) | 8 | "now creating comparable obligations for Indian organizations using US-hosted services for Indian residents' personal data" is fair; would be tightened by noting that DPDP's data-localization mechanism is the "blacklist" (notified countries) model, distinct from Russia's flat localization or GDPR's adequacy regime. |
| D4 | Sanctions-enforcement claim (line 125) | 7 | Correct that Adobe / Autodesk / Microsoft / Figma suspended Russia/CIS service in 2022, but the claim "hundreds of thousands of organizations" needs a citation — the number is plausible but the chapter does not source it, and a CISO reading this will want one. |
| D5 | Anthropic / DoD designation claim (line 125) | 4 | This is a fictional event ("In February 2026, the US Defense Secretary designated Anthropic's AI services a national security supply-chain risk"). It may be a deliberate near-future hypothetical, but the chapter presents it without any signal that it is hypothetical, alongside historical events (2022 sanctions, Schrems II 2020) that are real. A reader will not distinguish. **This is a legal-claim integrity issue, not a stylistic one.** Either flag it as hypothetical, source it if it is real, or replace it with a real analogous incident (the TikTok divestiture order, the Kaspersky federal-systems ban under Trump-1, the Huawei restrictions). |
| D6 | Professional-responsibility framing (lines 157–163) | 9 | "A legal practice storing confidential client communications in a vendor's cloud carries a professional duty to understand where that data lives and who can access it" is correctly framed; HIPAA naming for medical practice is correct; the "vendor's standard privacy policy — a document written to protect the vendor, not the client" framing is sharp and accurate. |
| D7 | Jurisdictional scope honesty (line 165) | 8 | Naming UAE DIFC alongside Schrems II and India DPDP, with the explicit forward-pointer to Appendix F, is correctly calibrated; a Part I chapter should not enumerate 30+ frameworks but should signal that it knows the scope is global. |
| D8 | Custody-vs-exposure framing (line 129) | 9 | "Data in vendor infrastructure can be reached by a government action targeted at the vendor. Data on hardware the user controls requires action targeted specifically at the user." This is the cleanest statement of the legal-exposure asymmetry I have seen in a popular-press technical book; it is the right framing and it is correctly hedged. |

**DOMAIN AVERAGE: 7.75 / 10**

### BLOCKING ISSUES

- **B3 (Pedantic Lawyer):** Line 125 contains what appears to be a fabricated or speculative legal incident ("In February 2026, the US Defense Secretary designated Anthropic's AI services a national security supply-chain risk... a California court subsequently enjoined portions of the order for civilian agencies. The Department of Defense exclusion stood."). Today's date (2026-04-29) is two months after the claimed event. If this is real, it must be cited. If it is a near-future hypothetical for illustrative purposes, it must be flagged as such (e.g., "Imagine: in late 2026..." or "A near-future scenario already on the horizon: ..."). Presenting it inline alongside the verifiable 2022 sanctions case will erode reader trust in every other regulatory claim in the chapter the moment one reader fact-checks it. **This is a falsifiable correctness gap.** A Part I chapter for a book that wants to land with CISOs cannot fabricate a federal-action incident — even a small one, even for narrative power.

### CONDITIONS

- **C10:** Cite or soften the "hundreds of thousands of organizations" figure for the 2022 Russia/CIS SaaS suspension at line 125 ("hundreds of thousands" is plausible — Adobe Russia alone reportedly served ~500K seats — but a footnote or hedge is owed).
- **C11:** Tighten the "first general-purpose data localization law globally" claim for Russia 242-FZ at line 127. South Korea's PIPA (2011) and Indonesia's Reg 82/2012 both have localization-adjacent provisions; "among the first general-purpose data localization laws" (already in the prose) is fine, but "predating GDPR by two years" should be checked against actual effective dates.
- **C12:** Consider a one-sentence note on jurisdictional reach of US discovery (FBI subpoena, CLOUD Act) — the "data on vendor infrastructure can be reached by a government action targeted at the vendor" framing at line 129 is correct, but a CISO reader will want the specific US-side mechanism named, not just the structural property.

### COMMENDATIONS

- The Schrems II framing at line 127 avoids the most common mischaracterization in industry coverage.
- The "vendor's standard privacy policy — a document written to protect the vendor, not the client" line at line 163 is the kind of sentence that gets quoted.
- The custody-vs-exposure framing at line 129 is the chapter's single strongest legal claim.

### VERDICT: **BLOCK**

Domain average 7.75 would otherwise be a clean PROCEED-WITH-CONDITIONS, but B3 (the apparently fabricated Anthropic / DoD federal-action incident) is a hard block. A book that wants to be cited by procurement counsel cannot present unsourced near-future hypotheticals as fait accompli alongside real 2020/2022 events. Resolve B3 — by citing the event if real, flagging it as hypothetical if speculative, or replacing it with a verifiable analogue — and this verdict converts immediately to PROCEED WITH CONDITIONS.

---

## SEAT 5 — Outside Observer (Jordan Kelsey, repurposed for audience accessibility / argumentative cohesion)
*Lens: does the bid scene carry argumentative weight or read as illustration? Does the chapter land for a CISO without prior context? For a working engineer without condescension? Does the argument hold from line 1 to line 206?*

### DIMENSION SCORES

| # | Dimension | Score | One-sentence rationale |
|---|---|---|---|
| D1 | Marcus opener — argumentative weight | 8 | The bid scene works because it sets up four specific structural claims the chapter then delivers (data on infrastructure not controlled / failure is structural / repeats across industries / not a planning failure); it carries weight, not just color. |
| D2 | Does it land for a CISO without prior context | 9 | Yes — the "vendor cloud → vendor custody → regulatory exposure → Schrems II / Russia 242-FZ / India DPDP" arc is exactly the arc a CISO has been arguing internally and seeing this in book form is validating; Appendix F pointer at the right moment. |
| D3 | Does it land for a working engineer without condescension | 7 | Mostly yes — the CRDT / gossip / container-runtime trio (lines 193–197) is appropriately compressed for a reader who already knows what these are. The risk is the opposite condescension: a reader who does NOT know these terms is given a one-paragraph definition each and may feel the chapter is talking past them. |
| D4 | Does the chapter assume the architectural answer too early | 6 | This is a Part I chapter and the architectural answer (CRDT + gossip + container runtime) lands in section "The Dependency That Looks Inevitable" (lines 191–199), which is *inside* Ch01. The book's plan says Part I sets up the problem and the answer comes in Parts II–IV. Compressing the answer into Ch01's last 200 lines is a structural choice, not necessarily wrong, but it pre-empts what Ch02 ("From Sync Toy to Serious Stack") and Ch03 ("The Inverted Stack in One Diagram") were supposed to deliver. |
| D5 | Honest-limits posture | 6 | Single sentence at line 199 ("operational complexity, key management, schema migration across independent nodes, and upgrade coordination replace vendor dependency"). A reader exits the chapter with a strong sense of what SaaS does badly and a weak sense of what the alternative does badly. This is the single biggest cohesion gap. |
| D6 | Section-to-section flow | 8 | "The Bundle" → "Six Ways" → "The Work That Doesn't Stop" → "Who Pays the Most" → "Why Users Have Accepted This" → "The Dependency That Looks Inevitable" is a strong arc; the *Pitt* section is the standout because it pivots from "what breaks" to "what survives," which the chapter then closes on. |
| D7 | Voice consistency with style guide | 8 | Active voice throughout; agency vocabulary; named patterns; minimal hedging; the M-PESA / Linear / Actual Budget commercial proof points are well-placed. The chapter does occasionally drift into definitional throat-clearing ("CRDTs (Conflict-free Replicated Data Type) library) and Yjs (the JavaScript CRDT library)" at line 193 has a typo — close paren without open paren — and reads as defensive over-definition). |
| D8 | Closing momentum into Ch02 | 8 | "What remains is the specific assembly that produces a node — not a smarter cache, not a thicker client, but a first-class local peer. Chapter 2 identifies exactly what that requires and where the existing work stops short. Chapter 3 draws the node." — this is a strong handoff and exactly the kind of forward-pointer the style guide rewards. |

**DOMAIN AVERAGE: 7.5 / 10**

### BLOCKING ISSUES

- **None at the cohesion level.** The chapter argues cleanly enough that no blocking-rewrite is required for cohesion alone. (B1, B2, B3 from prior seats are real but they are scope-of-claim issues, not cohesion failures.)

### CONDITIONS

- **C13:** Resolve the structural question of whether Ch01 should land the architectural answer or only set up the problem. The current chapter does both — opens with problem-setup and closes with a compressed version of the architectural answer. If the book-plan says Part I sets up the problem and Parts II–IV deliver the answer, then the "Three specific technology shifts made the structural necessity of the SaaS bundle removable" section (lines 191–199) is doing Ch02's work. Either (a) keep the compression as a *teaser* and explicitly defer to Ch02 / Ch03, or (b) accept that Ch01 is doing more than problem-setup and revise Ch02 to start from a higher-altitude position.
- **C14:** Expand the honest-limits paragraph at line 199 to two or three sentences. A reader who exits Ch01 with no sense that the alternative has real costs will read the rest of the book defensively, looking for the catch. Naming the catch up front is structural honesty and it is also better persuasion.
- **C15:** Fix the close-paren / open-paren imbalance at line 193 and check the chapter for the broader pattern of redundant first-use definitions ("CRDTs (Conflict-free Replicated Data Type)... CRDT (Conflict-free Replicated Data Type) libraries" — defining CRDT twice in two sentences is the anti-pattern the style guide warns against).
- **C16:** The "Marcus" name appears in lines 9–18 and then disappears until line 201. Bringing him back once in the body — perhaps at the M-PESA / construction site framing at lines 71–85, or at the "Who Pays the Most" section at line 155 — would make the chapter feel like one sustained argument rather than a sequence of sections that share an opening anecdote. This is a craft note, not a cohesion failure.

### COMMENDATIONS

- The Marcus opener earns its place — it sets up four specific structural claims the chapter then delivers, rather than just providing color.
- *The Pitt* episode case (lines 137–145) is the chapter's structural keystone — it pivots from "what breaks" to "what survives," and that pivot is what makes the closing argument land.
- The "drawer of paper backup forms remains in the supply closet... the drawer becomes a true backup rather than the only operating mode" line at line 145 is the chapter's quotable sentence and it is doing real argumentative work.
- The Ch02 / Ch03 forward-pointer at line 205 is a textbook example of how the style guide says forward-pointers should land.

### VERDICT: **PROCEED WITH CONDITIONS**

Domain average 7.5, no blocking issues at the cohesion lens. The chapter holds together as one sustained argument and lands its keystone (the *Pitt* section). The conditions are about scope-of-Ch01 vs. scope-of-Ch02 and about honest-limits posture — important, but not blocking.

---

## COUNCIL TALLY

| Member | Domain Avg | Verdict | Blocking issues |
|---|---|---|---|
| Theorist (Shevchenko) | 6.25 | REVISE | B1: failure-mode taxonomy not MECE; missing data-corruption mode |
| Production Operator (Voss) | 7.6 | PROCEED WITH CONDITIONS | None |
| Skeptical Implementer (Ferreira) | 7.0 | REVISE | B2: Linear used as data-sovereignty proof point but is not data-sovereign |
| Pedantic Lawyer (Okonkwo) | 7.75 | **BLOCK** | B3: apparently fabricated Anthropic/DoD federal-action incident at line 125 |
| Outside Observer (Kelsey) | 7.5 | PROCEED WITH CONDITIONS | None |
| **Overall** | **7.22** | **BLOCK (any-member rule)** | 3 blocking issues across 3 seats |

---

## CONSOLIDATED CROSS-CUTTING FINDINGS — RANKED P0 / P1 / P2

### P0 — Must resolve before next round (blocking)

| # | Raised by | Location | Issue | Suggested fix |
|---|---|---|---|---|
| **P0-1** | Pedantic Lawyer (B3) | Line 125 | The Anthropic / DoD designation incident appears to be either fabricated or a near-future hypothetical presented as fait accompli. Today's date is 2026-04-29; the claimed event is February 2026. If real, it requires a citation; if hypothetical, it requires explicit framing. Presenting unsourced legal-action claims alongside verifiable ones (Schrems II, 2022 sanctions) erodes trust in the entire compliance argument. | Either cite the incident with a primary source (DoD memo, court docket number), flag it explicitly as a hypothetical ("Imagine a near-future incident: ..."), or replace it with a verifiable analogue (TikTok divestiture order, Kaspersky federal ban, Huawei restrictions). |
| **P0-2** | Theorist (B1) | Lines 37–129 | The "six failure modes" are framed as a taxonomy but are not MECE: outage and connectivity overlap; vendor-disappears and price-changes are two faces of vendor custody; **silent data corruption / divergence is missing entirely** despite being one of the most common SaaS pain points (Notion sync bug history, Salesforce duplicate records, Airtable formula recomputation). | Add a seventh failure mode for silent data corruption / divergence, OR rewrite the section header as "Six pains of the SaaS bundle" / "Six common ways SaaS breaks" so the chapter is not making a taxonomic claim it cannot defend. The first option is preferred — Part I that names seven concrete pain modes is stronger than one that names six and leaves the silent-corruption case to Ch07. |
| **P0-3** | Skeptical Implementer (B2) | Lines 185, 193 | Linear is used as the load-bearing commercial proof point that "the desirable half of the SaaS bundle... does not require vendor data custody to function" (line 185) and as the data-sovereignty exemplar at line 193. Linear's data lives on Linear's servers. Linear is exactly the engine-local-but-custody-vendor pattern that Ch02–Ch04 will turn around and argue is *insufficient*. Using it as the Ch01 proof point undermines the chapter's argumentative spine. | Demote Linear to "proof point that sync engines run locally even inside SaaS architectures," lean harder on Actual Budget for the data-sovereignty claim, and consider adding Anytype / Logseq / Obsidian Sync as a third custody-local example. |

### P1 — Should resolve in this round

| # | Raised by | Location | Issue | Suggested fix |
|---|---|---|---|---|
| **P1-1** | Outside Observer (C13) | Lines 191–199 | Ch01 lands a compressed version of the architectural answer (CRDT + gossip + container-runtime) which the book-plan says should belong to Ch02–Ch03. Either Ch01 is doing too much or Ch02 needs to start from a higher-altitude position. | Decide the structural question and either compress lines 191–199 into a teaser ("Three specific technology shifts have made this architecture practical — Chapter 2 develops them in full") or accept that Ch01 covers more ground and rebrief Ch02. |
| **P1-2** | Outside Observer + Operator + Theorist (C3, C5, C14) | Line 199 | Single-sentence honest-limits paragraph. A reader exits Ch01 with strong understanding of what SaaS does badly and almost no sense of what the alternative does badly. Three seats independently flagged this. | Expand to a full paragraph naming the operator-relevant costs (helpdesk model, SBOM, patch cadence, key custody, schema migration), with explicit forward-pointer to Parts III–IV where each cost is addressed. |
| **P1-3** | Skeptical Implementer (C7) | Line 193 | "no data loss, no manual conflict resolution, no authority required" overclaims CRDT capability. Every shipping local-first app exposes some merge UX eventually. A reader who has built one closes the book at this sentence. | One-clause fix: "...no data loss, and conflict resolution that the application can either auto-merge or surface to the user as a structured choice." |
| **P1-4** | Pedantic Lawyer (C10) | Line 125 | "Hundreds of thousands of organizations" lacks a citation. Plausible but unsourced. | Cite or hedge ("seats" is the more defensible unit; Adobe Russia alone is reportedly ~500K seats). |
| **P1-5** | Theorist (C2) | Line 195 | Cassandra/DynamoDB analogy elides companion mechanisms (hinted-handoff, read-repair, tunable consistency). | Soften: "the same family of protocols" rather than "the same protocols." |

### P2 — Address opportunistically

| # | Raised by | Location | Issue | Suggested fix |
|---|---|---|---|---|
| **P2-1** | Operator (C4) | Line 49 | Cloud-region cascade claim unanchored. | Name a real incident (December 2021 us-east-1, June 2023 us-east-1). |
| **P2-2** | Operator (C6) | Line 41 | "Major SaaS providers report 99.9% uptime" unattributed. | Cite a study or industry report. |
| **P2-3** | Pedantic Lawyer (C11) | Line 127 | Russia 242-FZ "predating GDPR by two years" is loose on effective dates. | Tighten or hedge ("among the first" already softens this — reconcile). |
| **P2-4** | Pedantic Lawyer (C12) | Line 129 | US discovery / CLOUD Act mechanism unnamed. | One-sentence addition naming the specific US-side mechanism. |
| **P2-5** | Skeptical Implementer (C8) | Line 193 | Loro absent from CRDT library list despite being Sunfish's aspirational target. | Name Loro or note "CRDT library landscape is broader than these two." |
| **P2-6** | Skeptical Implementer (C9) | Line 185 | M-PESA framed as "local-first architecture" — strict-definition stretch. | Reframe as "store-and-forward transaction patterns at population scale." |
| **P2-7** | Theorist (D6) | Throughout | Availability vs. accessibility vs. portability are conflated. | Name the three properties once (could be a footnote or a short side-bar). |
| **P2-8** | Outside Observer (C15) | Line 193 | Paren imbalance and redundant CRDT first-use definition. | Copyedit; check first-use rule across the section. |
| **P2-9** | Outside Observer (C16) | Throughout | Marcus opens at line 9, returns at line 201. Sustained-argument feel would benefit from one mid-chapter callback. | Bring Marcus back once in the "Who Pays the Most" or "Workaround" sections. |
| **P2-10** | Theorist (D8) | General | Prior-art (Doctorow on enshittification, Kleppmann's *Local-First Software* essay, Ink & Switch) not named. | One-line forward-pointer: "Chapter 2 surveys the prior art." |

---

## ROUND-LEVEL VERDICT: **BLOCK**

**Trigger:** any-member BLOCK rule. Pedantic Lawyer (Okonkwo) issues BLOCK on B3 (apparently fabricated Anthropic / DoD incident). Theorist (Shevchenko) and Skeptical Implementer (Ferreira) issue REVISE on B1 and B2 respectively. Two seats clear conditionally (Voss, Kelsey).

**What this means in practice:** the chapter is structurally sound — the Marcus opener works, the *Pitt* episode is the structural keystone, the regulatory framing is sharper than most popular-press technical books, and the closing handoff to Ch02/Ch03 is textbook. The blocks are *specific, falsifiable, and small in word-count to fix.* B3 is a citation-or-flag-or-replace decision. B1 is a section-header-or-add-a-mode decision. B2 is a paragraph-rewrite decision. The chapter is one focused revision pass away from PROCEED-WITH-CONDITIONS.

**Recommended next step:** resolve P0-1 (Anthropic incident) first because it is the highest-trust risk; resolve P0-2 (taxonomy) and P0-3 (Linear conflation) in the same pass; address the five P1 items in the same pass; defer P2 to a copyedit cycle. Then resubmit for Round 2 — the council will check that B1/B2/B3 are resolved before re-scoring.

---
*End of Round 1 review.*
