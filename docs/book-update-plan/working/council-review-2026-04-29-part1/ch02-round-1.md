# KLEPPMANN COUNCIL REVIEW — Part I, Round 1
**Document:** `chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md`
**Date:** 2026-04-29
**Council seats convened (per request):** Theorist · Production Operator · Skeptical Implementer · Pedantic Lawyer · Outside Observer
**Reviewer:** Kleppmann Council facilitator
**Word count target:** ~4,000 (chapter currently ~3,950 measured)

---

## Pre-review notes

The chapter's brief, per `book-structure.md` and CLAUDE.md QC-8, is *opinionated, not encyclopedic — one paragraph per existing approach, ends with a crisp statement of what this book adds*. It must position against prior art (Kleppmann et al., Ink & Switch, Replicache, ElectricSQL, PowerSync, etc.) without becoming a literature review.

Citations as written: only **three** numbered references appear ([1] Kleppmann 2019, [2] DDIA 2017, [3] Kleppmann 2024 talk). Multiple specific systems and claims (Anytype, Linear, Actual Budget, Obsidian, Figma, M-PESA, MTN MoMo, Schrems II, Adobe/Autodesk/Microsoft/Figma sanctions exits, Cassandra, DynamoDB, Cambria, AutomergeRepo, Pushpin/Backchat/Trellis, libsodium/age/Argon2id) are referenced in prose without a bracketed citation. This is the single most consequential pattern in the chapter and surfaces in nearly every seat below.

---

## SEAT 1 — The Theorist (academic / theoretical correctness)

**Posture:** Has read Kleppmann et al. 2019 (Onward!) cover-to-cover, the Shapiro et al. CRDT survey, the Ink & Switch Cambria paper, the Yjs and Automerge papers, the original Flease paper (Stender, Berlin, Reinefeld 2010), and watched the Local-First Conf 2024 talks. Will detect any place a primary-source claim is paraphrased without citation, or where a system's actual semantics are misrepresented.

### DIMENSION SCORES

| # | Dimension | Score | Rationale |
|---|---|---|---|
| D1 | Accuracy of the seven-properties summary | 8 | Properties are paraphrased correctly; the "no spinners," "long now," "ownership" reductions track Kleppmann et al. faithfully and the gradient acknowledgment from the 2024 talk is a nice touch. Order is reshuffled vs. the paper, which is fine for narrative but worth a footnote. |
| D2 | Fidelity of CRDT theory references | 6 | Conflates "CRDT" as a class with the Automerge/Yjs *implementations* of operation-based CRDTs without naming the distinction (op-based vs. state-based, the Shapiro et al. taxonomy). The Cambria reference is name-only — no citation, no description of what bidirectional lenses *do*. |
| D3 | Correctness of system-specific technical claims | 6 | Linear: "each Linear client maintains a local SQLite replica" is correct (per Linear's 2023 engineering blog) but uncited. Figma: the "inspired by multiple separate CRDTs" quote is real (Wallace 2019 Figma blog) but not attributed. Actual Budget: "uses CRDT merge semantics in production" overstates — Actual uses a custom CRDT for the budget data structure, not a general one; worth narrowing. |
| D4 | Treatment of the broader prior-art landscape | 4 | **Replicache, ElectricSQL, PowerSync, Liveblocks, Y-Sweet, Jazz, Triplit, Evolu, Anytype, Logseq, Tinybase, Verdant, RxDB** — the user's prompt explicitly named several of these. Only PowerSync and ElectricSQL are mentioned, and only in a single sentence about "declarative partial sync" near the end. Liveblocks gets one sentence. Replicache (Rocicorp), arguably the most direct production competitor, appears nowhere. |
| D5 | Citation discipline (IEEE per Appendix E) | 4 | The Local-First Conf 2024 talk at line 36 is correctly cited as [3]. But Anytype (line 36), Linear's sync engine (lines 58, 142), Figma's per-property merge (line 142), Adobe/Autodesk/Microsoft/Figma 2022 sanctions (line 30), M-PESA history (line 138), Cambria (line 176), the Stender et al. Flease paper (line 174 implicit), Cassandra/DynamoDB leaderless replication (line 142), and the Pushpin/Backchat/Trellis essays (line 78) all carry concrete factual claims with **no bracketed reference**. Per Appendix E §1 every assertion attributable to a primary source needs a number. |
| D6 | Honest acknowledgement of prior intellectual debts | 7 | The closing paragraph (line 191) acknowledges the seven ideals as "the benchmark," names the Ink & Switch essays, and credits Kleppmann's DDIA. Good faith is on display. The acknowledgment would be stronger if it named individuals (Geoffrey Litt, Peter van Hardenberg, Adam Wiggins, Mark McGranaghan, Brooklyn Zelenka) rather than only the institutional brand. |
| D7 | Avoidance of overclaim ("first," "novel," "no one else") | 7 | The chapter is mostly disciplined: "What this book assembles" is framed as composition, not invention. Two flags: line 36 "no production app satisfies all seven" is a strong empirical claim made *to the authors' knowledge at time of writing* — that hedge is good. Line 142 "What has not been done before is assembling them into a coherent, enterprise-deployable system" is the riskier claim — it ignores Anytype-Cloud-as-self-hosted, Jazz, Y-Sweet, and arguably Replicache's enterprise customers; the claim should narrow to a specific axis (e.g., "with a per-record CAP-class boundary and an MDM-deployable installer pathway"). |
| D8 | Theoretical depth where the chapter touches CAP, lease, GC | 5 | "CRDTs handle concurrent merge" — true but the chapter never says *under what consistency model* (strong eventual consistency / SEC), and the boundary between CRDT-class records and lease-class records is asserted (line 181) without forward reference to the formal CAP positioning that Chapter 6 supplies. A reader stopping at Ch 2 leaves with the impression CRDTs are universally applicable. |

**DOMAIN AVERAGE: 5.9 / 10**

### BLOCKING ISSUES (Theorist)

- **B1-T:** Citation discipline gap. At least eight prose claims attribute behavior to specific commercial or research systems without a bracketed IEEE reference. Per Appendix E and CLAUDE.md QC-3, this fails the chapter's own house style. (See line refs in D5.)
- **B2-T:** Replicache is the elephant in the room. Replicache (Rocicorp) is the most direct commercial implementation of a sync engine sitting between "smart cache" and "full node," with documented CRDT-adjacent semantics (mutators with rollback) and enterprise customers. A chapter positioning *against* prior art that omits Replicache reads as either uninformed or evasive.

### CONDITIONS

- **C1-T:** Add bracketed references for every system-specific claim — minimum: Linear engineering blog (already in Appendix E examples as [10]), Figma multiplayer blog (Wallace 2019), Anytype docs/whitepaper, Cambria paper (Litt et al. 2020), Stender et al. Flease 2010, the Adobe/Autodesk/Microsoft sanctions reporting (Reuters or AP, March 2022).
- **C2-T:** One-paragraph treatment of Replicache, ElectricSQL, and PowerSync in the taxonomy section — at minimum a four-system "lightweight replica" cluster (Linear, Replicache, ElectricSQL, PowerSync) where the chapter currently has Linear alone.
- **C3-T:** Distinguish op-based vs. state-based CRDTs in one sentence, OR drop the un-qualified "CRDT" generic and consistently say "operation-based CRDT (Automerge/Yjs lineage)."
- **C4-T:** Narrow the line-142 "what has not been done before" claim to its actual axis (per-record CAP boundary + MDM-deployable installer + AGPLv3-with-managed-relay business model), so the differentiator is falsifiable rather than rhetorical.

### COMMENDATIONS

- ✓ The Anytype treatment at line 36 is unusually fair: names the five properties it does satisfy, names the two it does not, and identifies the Any-Block format as the specific portability defect rather than vaguely calling Anytype "proprietary."
- ✓ Citing the Kleppmann 2024 Local-First Conf talk for the "gradient" acknowledgment is exactly the kind of primary-source discipline this seat rewards. It also forecloses the "but Kleppmann himself walked it back" objection.

### VERDICT (Theorist): **REVISE**
The chapter has the right shape and broadly faithful summaries, but the citation gap is structural — it is not a polish issue. A theory reviewer cannot certify "fair to prior art" when half the prior-art-specific claims have no bracketed reference. Replicache's absence is the single most credibility-damaging omission because it is the system most readers will mentally compare against.

---

## SEAT 2 — The Production Operator (ops + reliability lens)

**Posture:** Has run Linear, Notion, Obsidian, Actual Budget, Figma, and a homegrown ElectricSQL prototype in production environments. Knows what each system actually does on a flaky network at 2 a.m., not what its marketing page claims. Has a healthy distrust of "demos work, production breaks."

### DIMENSION SCORES

| # | Dimension | Score | Rationale |
|---|---|---|---|
| D1 | Operational accuracy of Linear description | 7 | "Local SQLite replica," "writes go to local first," "feels instant" — all match the Linear engineering blog [Palmer 2023]. The claim "fail silently or queue for an uncertain duration" (line 58) is sharper than I'd write — Linear surfaces sync state in the UI; the failure mode is more "the user keeps clicking and nothing visibly happens" than "silent failure." |
| D2 | Operational accuracy of Obsidian description | 7 | Conflict-copy behavior is correctly described (line 48). Worth noting that Obsidian Sync is *one* of several sync mechanisms (Git, iCloud, Syncthing, Remotely Save), each with different failure modes; the chapter implicitly treats Obsidian Sync as the canonical one without naming it. |
| D3 | Operational accuracy of Notion description | 6 | "Architecturally a web application with a rich offline cache" (line 52) is fair. The export claim — "ZIP archive of markdown files and CSVs" — is correct as of Notion's current export, but the chapter does not mention that Notion has a documented public API and a (paid) self-host posture is *not* available, which is the actual lock-in. |
| D4 | Operational accuracy of Actual Budget description | 8 | The "single-user by design" framing is exactly right. The hosted relay description matches Actual Server's actual architecture. The "Adapting it to multi-user team workflows would require... at which point it would no longer be Actual Budget" is the sharpest sentence in the chapter (line 72) — practitioners will nod. |
| D5 | Operational accuracy of Automerge / AutomergeRepo description | 6 | "Automerge is a library that operates on documents" is correct. The claim that AutomergeRepo provides "a working sync transport" is strictly true but underdescribes — production Automerge deployments hit known issues with **document size growth, history compaction (the GC story), and cold-sync time for large histories**. The chapter mentions this only obliquely ("CRDT GC policy" in the contributions list at line 182) without acknowledging Automerge's specific operational pain points. |
| D6 | M-PESA / MTN MoMo operational analogy | 4 | The M-PESA/MoMo paragraph (line 138) is the single weakest operational claim in the chapter. M-PESA does *not* run as a "full node on the user's device" in the local-first sense — it runs as a SIM Toolkit application with USSD/STK signaling; the offline-tolerance is provided by **agent-network reconciliation and a centralized Safaricom-operated platform**, not by user-device replicas. Calling this a "design constraint that produced M-PESA" and then claiming the book "generalizes that pattern to structured-data applications" is, charitably, a category error. The right analogue is probably Cassandra/DynamoDB (already cited) or a banking CBS like FIS Profile that does maintain branch-local replicas; M-PESA does not validate the architecture's claim. |
| D7 | Treatment of operational realities the chapter elides | 5 | Things a production operator wants and does not get: (a) MTBF-style numbers for any of the cited systems; (b) acknowledgment that ElectricSQL was a research-flavored project that has shipped commercial product but with documented partial-sync performance ceilings; (c) Liveblocks' actual operational profile (it is a hosted service charging by MAU, not a CRDT-as-a-library); (d) what happens to a Linear team when Linear has a 4-hour outage (which has happened — it's worth one sentence). |
| D8 | Honest acknowledgement of where the proposed architecture will hurt operationally | 5 | The "managed relay is a residual vendor dependency" paragraph (line 189) is honest. But the chapter never names the operational costs of running a full local node: device provisioning, key custody UX, the "couch device" recovery path (it's mentioned as a goal, not a cost), the support burden of every user being a partial sysadmin. These come later in the book — Ch 2 should at least *flag* them so readers don't feel sold. |

**DOMAIN AVERAGE: 6.0 / 10**

### BLOCKING ISSUES (Production Operator)

- **B1-O:** The M-PESA / MTN MoMo "operational precedent at continental scale" paragraph (line 138) misrepresents how those systems actually work. They are *not* user-device-replica architectures; they are agent-network store-and-forward over centralized cores. This is the kind of claim a production reader from sub-Saharan Africa or a fintech ops engineer will catch in five seconds, and it damages the credibility of every other operational claim in the chapter.

### CONDITIONS

- **C1-O:** Replace the M-PESA paragraph with a more defensible operational precedent. Candidates: (a) banking core branch replication (FIS, Temenos), (b) point-of-sale store-and-forward (Square's offline mode, Toast offline mode), (c) Salesforce Mobile SDK's offline-first mode for field agents, (d) the original SyncML / ActiveSync push-email model. Pick one that *actually* runs application logic on the user device and reconciles centrally.
- **C2-O:** Add one sentence on Automerge's known operational pain points (document size growth, cold-sync time, GC) so the "production-ready" framing on line 142 doesn't read as marketing.
- **C3-O:** One sentence (in Chapter 2, not deferred) acknowledging the operational *cost* of a full node: device provisioning, key custody, support burden. Otherwise the chapter sells a free lunch.
- **C4-O:** Soften "fail silently" (line 58) to match Linear's actual behavior — its sync state is visible in the UI even when the network is degraded.

### COMMENDATIONS

- ✓ The Actual Budget paragraph (lines 64–74) is operationally exact: single-user by design, hosted relay role correctly described as relay-and-backup-not-authority, and the honest "would no longer be Actual Budget" admission about why team sync isn't a feature add.
- ✓ Naming the cluster of proven components (Cassandra/DynamoDB, VS Code language servers, 1Password local agent, Tailscale, Docker Desktop) on line 142 is the right operational reassurance — the architecture is not asking the reader to bet on unproven primitives.

### VERDICT (Production Operator): **REVISE**
Three of four taxonomy entries are operationally fair. The M-PESA framing is the disqualifying defect — it's not a stylistic preference, it's a factual mischaracterization at the exact moment the chapter is trying to claim continental-scale precedent. Fix that, soften the Linear "silently" word, and the operator will sign.

---

## SEAT 3 — The Skeptical Implementer (engineer-shipping perspective)

**Posture:** Is six weeks into evaluating sync engines for a real product. Has read Replicache's docs end-to-end, has a half-finished ElectricSQL spike on their laptop, and has an Automerge prototype in a side branch. The question they want this chapter to answer: *should I pick this book's approach over Replicache or ElectricSQL — and why?*

### DIMENSION SCORES

| # | Dimension | Score | Rationale |
|---|---|---|---|
| D1 | Does the chapter help me decide vs. Replicache? | 2 | Replicache is not mentioned. At all. This is the most-asked competitive question for any team building local-first today, and the chapter is silent. |
| D2 | Does the chapter help me decide vs. ElectricSQL? | 4 | ElectricSQL appears in one half-sentence ("declarative partial sync is solved: PowerSync and ElectricSQL implement it," line 142). The chapter borrows ElectricSQL's category and gives nothing back — no comparison, no positioning. |
| D3 | Does the chapter help me decide vs. PowerSync? | 4 | Same as ElectricSQL — one half-sentence as a "solved" prior art, no positioning. |
| D4 | Does the chapter help me decide vs. Yjs/Automerge directly | 7 | Yes — the Automerge section (lines 76–84) makes the right argument: Automerge is a library, not a deployable product, and the application-level concerns (deployment, governance, schema, key management) are outside its scope. An implementer evaluating Automerge will recognize this. |
| D5 | Clarity of the differentiation claim | 6 | "The composition is the contribution" (line 193) is *almost* a strong claim. It is undermined by the laundry list at lines 180–187, which reads as a feature comparison rather than a sharp differentiator. The implementer wants one sentence: "Pick this when X; pick Replicache when Y; pick ElectricSQL when Z." |
| D6 | Does the chapter give me a build-or-buy heuristic? | 4 | Chapter 4 is forward-referenced for the decision framework, which is correct sequencing. But Ch 2 should leave the implementer with at least a *provisional* heuristic — e.g., "if your data is single-tenant per-user collaborative documents, Yjs+Y-Sweet is faster to ship; if you need typed records with role-scoped access, this book." |
| D7 | Cost of switching / adoption friction acknowledgment | 5 | The "Three disciplines" paragraph (line 174) names integration, cryptography choice, and wire-format choice as the kill-criteria for a roll-your-own attempt. This is genuinely useful to the implementer evaluating *building from scratch*. It does not address the equal-importance question of evaluating *adopting Sunfish* — what does the integration cost look like? what are the .NET/MAUI assumptions baked in? |
| D8 | Code-or-config-level concreteness | 5 | The chapter is appropriately abstract for Part I. The implementer would still benefit from naming *one* concrete artifact (e.g., "Sunfish.Kernel.Sync exposes the same delta-protocol surface that Yjs's `awareness` API does, so a Yjs migration costs roughly one adapter") that lets them mentally project the integration. The Mermaid diagrams help; a third diagram showing "where my existing Yjs/Automerge code maps onto the inverted stack" would close the gap. |

**DOMAIN AVERAGE: 4.6 / 10**

### BLOCKING ISSUES (Skeptical Implementer)

- **B1-SI:** Replicache absence. Any engineer comparison-shopping local-first sync engines in 2026 has Replicache (Rocicorp) on the list. Mentioning Linear, Liveblocks, Automerge, ElectricSQL, and PowerSync — but not Replicache — is the kind of omission that makes an implementer wonder if the author is unaware of the competitive landscape. This is a blocker because the chapter's *purpose* is to answer "why this and not the alternatives."
- **B2-SI:** No like-for-like comparison vector. Each system is described in its own terms (Obsidian by data model, Linear by replica strategy, Actual Budget by user-cardinality, Automerge by library scope) so the reader cannot do an apples-to-apples comparison. A small comparison table — or at minimum a consistent four-vector frame (deployment topology, data-ownership stance, threat model, business model) applied to each system — would let the implementer make a real decision.

### CONDITIONS

- **C1-SI:** Add Replicache. One paragraph minimum, in the lightweight-replica cluster.
- **C2-SI:** Add a comparison table at the end of the taxonomy section, scored on a consistent set of vectors. The user's prompt explicitly called for "like-for-like" treatment.
- **C3-SI:** Promote one provisional decision sentence into Ch 2 (forward-pointing to Ch 4 is fine) so the implementer leaves with a heuristic, not just a promise of one.
- **C4-SI:** Add an "evaluation criteria" half-paragraph describing what an integration-from-existing-Yjs/Automerge/Replicache codebase costs.

### COMMENDATIONS

- ✓ The Automerge taxonomy entry (lines 76–84) is the strongest single piece of competitive positioning in the chapter — the implementer reading it understands exactly what Automerge gives them and what it does not.
- ✓ "What this book assembles from those proven components" (line 178) followed by an enumerated list is the right shape for an implementer's eyes — list of concrete commitments, not aspirations.

### VERDICT (Skeptical Implementer): **REVISE**
The chapter is pitched at the wrong audience-pose. It treats prior art as *intellectual ancestors* (which it acknowledges generously) rather than as *competitors the reader is choosing between* (which the implementer needs). The Automerge treatment shows the chapter *can* do this — extend the same discipline to Replicache, ElectricSQL, PowerSync, and add a like-for-like vector and the implementer will have what they need.

---

## SEAT 4 — The Pedantic Lawyer (compliance / regulatory / IP)

**Posture:** Reads every claim about a third-party system as a potential defamation, false-comparison-advertising, or IP-misuse exposure. Reads every regulatory claim as something a regulator's lawyer will quote back at a deposition. Knows the difference between a court ruling, a regulation, and a guidance document.

### DIMENSION SCORES

| # | Dimension | Score | Rationale |
|---|---|---|---|
| D1 | Defensibility of claims about specific commercial products | 5 | "Notion's data lives in Notion's proprietary format" (line 52) — defensible. "Linear's sync protocol is proprietary... no peer-to-peer mode" (line 58) — defensible if cited; uncited it's an assertion. "Anytype... 'source available,' not open-source" (line 36) — this is a contested characterization (Anytype's license is the Any Source Available License, and the term "open-source" is OSI-defined; Anytype's website does call itself "open source" in some pages). The chapter's framing is technically correct under OSI usage but a Lawyer would want a footnote. |
| D2 | Defensibility of claims about defunct / sanctions-affected vendors | 6 | The Sunrise Calendar reference (line 30) is uncontroversial. The "Adobe... Autodesk... Microsoft... Figma... Dozens of other Western SaaS providers" 2022 sanctions exit (line 30) is a *real* event but **uncited** — and it implicates named companies in a regulatory action. A Lawyer wants either a Reuters/AP/FT citation or a softer framing. |
| D3 | Accuracy of regulatory citations | 5 | Schrems II is correctly named (line 168) but not cited as Case C-311/18 per Appendix E §"Legal Decision." India DPDP 2023, UAE DIFC DPL 2020, Russia 242-FZ are all named without a bracketed reference. The chapter says "see Appendix F" but Appendix E §Consistency Rules requires the in-text bracket on first appearance, not just an appendix pointer. |
| D4 | Specificity of regulatory claims | 6 | "Schrems II... constrains transfers... without supplemental safeguards — making local-first residency a direct compliance mechanism" (line 168) is **almost** right but is a load-bearing legal interpretation. Schrems II requires supplemental measures *or* an alternative legal basis (SCCs with TIA, BCRs, derogations). Calling local-first a "direct compliance mechanism" elides that the cloud transfer is the trigger; running a local node still generates EU personal data and does not ipso facto satisfy GDPR — controllerships, lawful bases, DSAR rights all still apply. |
| D5 | UAE DIFC DPL claim defensibility | 4 | "may legally prohibit foreign cloud storage for DIFC-licensed financial entities" (line 168) — the parenthetical "may" hedges, which is good. But the underlying statement is contested. DIFC DPL §28 covers cross-border transfers and requires adequate-jurisdiction or appropriate-safeguards or derogations; it does *not* categorically prohibit foreign cloud storage. DFSA financial-services rulebooks add overlay obligations but again do not categorically prohibit. A Lawyer would strike this sentence or rewrite it to cite the specific DIFC DPL §28 / DFSA GEN provisions. |
| D6 | Russia 242-FZ historical claim | 5 | "Among the first general-purpose data localization laws globally, predating GDPR by two years" (line 168). 242-FZ was enacted in 2014, effective Sep 2015. GDPR was adopted April 2016, effective May 2018. So 242-FZ predates GDPR's *adoption* by ~2 years and its *enforcement* by ~3 years. The "first general-purpose" framing is debatable — Vietnam (Decree 72, 2013), South Korea (PIPA, 2011), and others have prior data-localization features. A Lawyer would soften to "among the early general-purpose data localization laws." |
| D7 | IP / license naming | 8 | AGPLv3 is named correctly (line 186). Yjs and Automerge are named with their repository URLs per house style. The Cambria reference is by name only (line 176). No defamatory IP framings. The "dual-license CLA for enterprise customers" mention is the kind of thing the Lawyer wants more detail on — but at Ch 2 abstraction level, naming it is sufficient. |
| D8 | Quotation discipline | 6 | The Figma "inspired by multiple separate CRDTs" string (line 142) is in quotation marks — but the source is not cited. If quoted, attribute. |

**DOMAIN AVERAGE: 5.6 / 10**

### BLOCKING ISSUES (Pedantic Lawyer)

- **B1-PL:** The DIFC DPL "may legally prohibit foreign cloud storage" sentence (line 168) is too strong even with its "may" hedge. Either narrow it to a specific DFSA rulebook citation or remove. As written, a DIFC-licensed entity reading this could rely on it for a compliance decision and the book's claim is not defensible at that level of specificity.
- **B2-PL:** The 2022 sanctions-exit roll-call (line 30) names four real companies in a regulatory action and is uncited. Under the book's own Appendix E §Assembly Guidance #4, "a misspelled case name or a wrong regulation number, in a book making a compliance argument, is a credibility defect." The same standard applies to naming companies in a sanctions context.

### CONDITIONS

- **C1-PL:** Add IEEE-format bracketed citations to: Schrems II (Case C-311/18 per Appendix E example), India DPDP 2023 (Act No. 22 of 2023), UAE DIFC DPL 2020, Russia 242-FZ. Appendix F as a footnote pointer is fine but does not substitute for first-appearance bracketing.
- **C2-PL:** Cite the 2022 sanctions exits to a primary news source (Reuters, AP, BBC, FT) per company. Three references, one per company family, suffices.
- **C3-PL:** Soften "direct compliance mechanism" (line 168) to "a structural mechanism that addresses the data-transfer leg of GDPR analysis under Schrems II." Schrems II is about transfers, not about data residency in general.
- **C4-PL:** Cite the Figma quotation (line 142) to its source (Wallace, "Multiplayer Editing in Figma," Figma Engineering Blog, 2019).
- **C5-PL:** Soften the Russia 242-FZ "first general-purpose" claim to "among the early."

### COMMENDATIONS

- ✓ The "may legally prohibit" hedge on the DIFC line, while still too strong, *attempts* lawyer-grade caution and is the correct register.
- ✓ The Anytype "source available, not open-source" distinction (line 36) is precise OSI-correct usage — most popular-press writers get this wrong.
- ✓ "Ownership conveyed only through a contract is ownership that can be revoked when the contract changes" (line 34) is a single sentence that captures the legal-vs-architectural distinction the rest of the book turns on. Strong.

### VERDICT (Pedantic Lawyer): **REVISE**
The chapter's regulatory framing is directionally right and the hedging is mostly intentional, but two specific claims (DIFC DPL prohibition, 2022 sanctions roll-call) are exposed without citations and one (Schrems II "direct compliance mechanism") slightly overstates what the ruling actually compels. Citation discipline per Appendix E is the cure.

---

## SEAT 5 — The Outside Observer (audience accessibility / argumentative cohesion)

**Posture:** Has read Chapter 1 and is reading Chapter 2 cold. Is a senior engineer or technical founder, not a CRDT researcher. Wants to come away with: (a) what local-first is, (b) why existing attempts fall short, (c) what this book uniquely promises. Will measure the chapter on whether it delivers those three landings without a re-read.

### DIMENSION SCORES

| # | Dimension | Score | Rationale |
|---|---|---|---|
| D1 | Opening hook / orientation in first 200 words | 7 | "In 2019, researchers at Ink & Switch posed a hypothesis they called local-first software" is a clean opening. The pivot at line 14 ("The word 'serious'... is not a claim about complexity. It is a claim about scope") is a strong rhetorical move. The reader knows where they are. |
| D2 | Section structure and signposting | 7 | Three top-level sections (Seven Ideals → Taxonomy → Missing Step → What This Book Adds) — wait, four. The "What Each Gets Right" section (line 116) is a transition paragraph dressed as an H2 and breaks the rhythm. Either fold it into the end of Taxonomy or promote it to a real third section with substance. |
| D3 | Paragraph length discipline | 6 | Several paragraphs run long. The "long now" property paragraph (line 30) is the most overstuffed — Sunrise Calendar + Adobe + Autodesk + Microsoft + Figma + sanctions + sentence-on-proprietary-formats — that's six beats in one paragraph. Style guide target is "no paragraph longer than 6 sentences"; a few here exceed it. |
| D4 | Voice consistency with Part I register | 7 | The Sinek "purpose before process" register holds for most of the chapter. The "What This Book Adds" section drifts into list-heavy specification voice (lines 180–187) which belongs in Part III, not Part I. The reader pulled along by narrative hits a spec sheet. |
| D5 | Acronym / first-use discipline (per style guide) | 8 | API, CRDT, CIS, SaaS, MDM, BSI, CNIL, DPDP, DIFC, DPL, GDPR, GCC, APAC, HIPAA, SOC 2, SBOM, AGPLv3, DEK, KEK — all spelled out on first use within the chapter. Good. The one nit: "CRDT" is spelled out twice (line 28 and line 36) — the style guide says spell out *once* per chapter. |
| D6 | Cross-reference clarity | 7 | "Chapter 3, Chapter 4," "Part II," "Part III," "Part IV," "Appendix F" — all named. The forward references work. The risk is the cumulative weight: the chapter forwards-points so often that an outside reader may feel the *real* answers are always one chapter away. Trim by half. |
| D7 | The "what this book adds" landing | 6 | The contribution claim arrives twice: at line 174 ("Three disciplines separate working implementations from prototypes") and again at line 193 ("The composition is the contribution"). They say similar things in different vocabularies. The outside observer is left with a fuzzy gestalt rather than a one-sentence claim they can quote. The chapter needs a single, memorable, repeatable line. |
| D8 | Anti-AI-tells / freshness of phrasing | 7 | A few patterns from the anti-ai-tells skill flicker: "stands on the local-first community's work" (line 191) is borderline pattern-1 puffery; "structural property that follows from where authority lives" (line 140) is the kind of abstract gesture pattern-1 flags. Most of the chapter is fresh. The closing paragraph is ceremonial and could be cut to one sentence. |

**DOMAIN AVERAGE: 6.9 / 10**

### BLOCKING ISSUES (Outside Observer)

- **B1-OO:** The chapter has no single, memorable, quotable thesis sentence. "The composition is the contribution" is the closest, but it lands at the very end after the reader has already absorbed the laundry list. Pull it forward — make it the chapter's thesis statement, repeat it once midway, and close on it. Right now the differentiator dissolves into specifications.

### CONDITIONS

- **C1-OO:** Resolve the "What Each Gets Right" mini-section (line 116). Either fold the single paragraph into the end of the Taxonomy section, or expand it into a substantive synthesis that earns its H2.
- **C2-OO:** Trim the long-now paragraph (line 30). Cut to: Sunrise Calendar (one sentence) → 2022 sanctions wave (one tight sentence with citation) → "proprietary sync formats fail this property" closer. Currently five companies and a parenthetical jurisdiction definition — too much.
- **C3-OO:** Pull "the composition is the contribution" (line 193) into the chapter's first 500 words as a thesis statement, then repeat it once near the midpoint. The reader should leave with one memorable phrase.
- **C4-OO:** Cut the chapter's closing paragraph (line 193) by half. "The next chapter shows..." is fine; "Chapter 4 provides the decision framework..." can go (Ch 4 will introduce itself).
- **C5-OO:** Halve the forward-reference density. Currently I count 11 forward pointers in a 4,000-word chapter; 5 is enough.

### COMMENDATIONS

- ✓ Line 14 ("The word 'serious'... is not a claim about complexity. It is a claim about scope.") is the chapter's best rhetorical move and earns its place.
- ✓ The seven-properties tour (lines 22–34) reads cleanly and gives the cold reader the framework they need before the taxonomy hits.
- ✓ Acronym discipline is the strongest in any chapter I've reviewed in this book — eighteen acronyms, all spelled out on first use within the chapter, none orphaned.

### VERDICT (Outside Observer): **PROCEED WITH CONDITIONS**
The chapter is readable, well-paced for the first two-thirds, and orients a cold reader effectively. It loses energy in the "What This Book Adds" closing section because the contribution claim is buried under a feature list. Front-load the thesis, cut the closing list to a quoted commitment paragraph, and the chapter will carry its weight.

---

## COUNCIL TALLY

| Member | Domain Avg | Verdict |
|---|---|---|
| Theorist | 5.9 / 10 | REVISE |
| Production Operator | 6.0 / 10 | REVISE |
| Skeptical Implementer | 4.6 / 10 | REVISE |
| Pedantic Lawyer | 5.6 / 10 | REVISE |
| Outside Observer | 6.9 / 10 | PROCEED WITH CONDITIONS |
| **Overall** | **5.8 / 10** | **REVISE — does not clear Round 1** |

**Round-level verdict:** **REVISE.** Four of five seats issue REVISE; the overall domain average sits below the 6.0 threshold required for PROCEED WITH CONDITIONS. The chapter has good bones and a fundamentally honest argumentative shape, but the citation gap (raised by Theorist + Lawyer + Operator), the Replicache omission (Theorist + Implementer), the M-PESA mischaracterization (Operator), and the un-landed thesis (Observer) are not stylistic preferences. They are correctness, completeness, and competitive-positioning gaps. Round 2 should be initiated only after the P0 items below are resolved.

---

## CONSOLIDATED CROSS-CUTTING FINDINGS

Findings are ranked **P0 (must fix to clear Round 2)**, **P1 (must fix for full PROCEED)**, **P2 (improvement, not gating)**.

### P0 — Blocking across multiple seats

| # | Raised by | Finding | Location | Fix |
|---|---|---|---|---|
| P0-1 | Theorist, Lawyer, Operator | Citation discipline gap. ~10 prose claims attribute behavior or events to specific systems / regulations / news events without an IEEE bracketed reference. Violates Appendix E and CLAUDE.md QC-3. | Lines 30, 36, 52, 58, 78, 138, 142, 168, 176, 191 | Add bracketed [N] citations per Appendix E. New refs: Linear blog (already example [10]), Figma blog (Wallace 2019), Anytype docs, Cambria paper (Litt et al. 2020), Stender Flease 2010, 2022 sanctions reporting (Reuters/AP), Schrems II (Case C-311/18), DPDP 2023, DIFC DPL 2020, 242-FZ. |
| P0-2 | Theorist, Skeptical Implementer | Replicache omission. The most direct production competitor in the local-first sync-engine space is not mentioned. The chapter's purpose — positioning vs. prior art — fails on this axis. | Section "What Exists Today" (lines 40–112) | Add a Replicache paragraph to the Lightweight Replica cluster. One paragraph, ~150 words, treating Replicache the way the chapter treats Linear. |
| P0-3 | Production Operator | M-PESA / MTN MoMo "operational precedent" misrepresents how those systems actually work. They are agent-network store-and-forward over centralized cores, not user-device replicas. Damages credibility of every operational claim that follows. | Line 138 | Replace with a defensible analogue: banking-core branch replication, Square/Toast offline POS mode, or Salesforce Mobile SDK offline-first for field agents. |
| P0-4 | Pedantic Lawyer | DIFC DPL "may legally prohibit foreign cloud storage" is too strong even hedged. A DIFC-licensed entity could rely on the claim and the book's framing is not defensible at that specificity. | Line 168 | Either cite specific DIFC DPL §28 / DFSA rulebook provisions or remove the categorical framing. |

### P1 — Required for full PROCEED

| # | Raised by | Finding | Location | Fix |
|---|---|---|---|---|
| P1-1 | Skeptical Implementer | No like-for-like comparison vector across the taxonomy. Each system is described in its own terms; the implementer cannot make an apples-to-apples comparison. | Lines 40–112 | Add a four-vector comparison table at the end of the Taxonomy section: deployment topology, data-ownership stance, threat model, business model. Apply to Obsidian, Notion, Linear, Replicache, ElectricSQL, PowerSync, Actual Budget, Automerge. |
| P1-2 | Outside Observer | Thesis sentence ("the composition is the contribution") buried in closing. Reader leaves without a memorable, quotable claim. | Lines 14, 122, 193 | Pull "the composition is the contribution" forward. State at line ~14, repeat at midpoint, close on it. |
| P1-3 | Theorist | Line-142 "what has not been done before" is rhetorical, not falsifiable. | Line 142 | Narrow to a specific axis: per-record CAP boundary + MDM-deployable installer + AGPLv3-with-managed-relay business model. |
| P1-4 | Production Operator | Automerge's known operational pain (document size growth, cold-sync time, GC) is elided behind "production-ready" framing. | Line 142 | One sentence acknowledging the operational caveats. |
| P1-5 | Pedantic Lawyer | 2022 sanctions roll-call names four companies in a regulatory action with zero citation. | Line 30 | Cite to primary news (Reuters, AP, BBC, FT). |
| P1-6 | Pedantic Lawyer | Schrems II "direct compliance mechanism" overstates what the ruling compels. Schrems II is about transfers, not residency. | Line 168 | Soften to "structural mechanism that addresses the data-transfer leg of GDPR analysis under Schrems II." |
| P1-7 | Production Operator | Linear "fail silently" is sharper than Linear's actual UI behavior. | Line 58 | Soften to acknowledge Linear surfaces sync state in the UI. |
| P1-8 | Outside Observer | "What Each Gets Right" mini-section (line 116) is a single transition paragraph dressed as an H2. | Line 116 | Fold into end of Taxonomy or expand to an earned H2. |

### P2 — Improvements, not gating

| # | Raised by | Finding | Location | Fix |
|---|---|---|---|---|
| P2-1 | Theorist | "CRDT" used generically; op-based vs. state-based distinction never made. | Throughout | One sentence in the Seven Ideals section, OR consistently say "operation-based CRDT (Automerge/Yjs lineage)." |
| P2-2 | Outside Observer | Long-now paragraph (line 30) overstuffed with five companies + sanctions + format-failure closer. | Line 30 | Trim to three beats. |
| P2-3 | Outside Observer | Forward-reference density is high (11 in 4,000 words). | Throughout | Halve to 5–6. |
| P2-4 | Pedantic Lawyer | Russia 242-FZ "first general-purpose" is debatable. | Line 168 | Soften to "among the early." |
| P2-5 | Production Operator | Liveblocks gets one sentence, undescribed as a hosted-service-by-MAU. | Line 62 | Half-paragraph or cut. |
| P2-6 | Skeptical Implementer | No build-or-buy heuristic offered before deferring to Ch 4. | Line 172 onward | One provisional sentence: "If your data is single-tenant per-user collaborative documents, Yjs+Y-Sweet ships fastest; if you need typed records with role-scoped access, this book." |
| P2-7 | Theorist | Acknowledgment of intellectual debts names institutions (Ink & Switch) but not individuals (Geoffrey Litt, Peter van Hardenberg, etc.). | Line 191 | Name individuals where the chapter relies on specific work. |
| P2-8 | Outside Observer | "stands on the local-first community's work" — borderline anti-ai-tells pattern 1. | Line 191 | Replace with "builds on" or restructure. |
| P2-9 | Theorist | "CRDT" spelled out twice (lines 28 and 36). | Lines 28, 36 | Spell out once per chapter. |
| P2-10 | Outside Observer | Closing paragraph is ceremonial. | Line 193 | Cut by half. |

---

## ROUND 2 GATING CRITERIA

Before initiating Round 2, the following must be true:

1. P0-1 through P0-4 are resolved.
2. The chapter still measures within ±10% of 4,000 words after edits (CLAUDE.md QC-1). The new Replicache paragraph and the comparison table will add ~250 words; trims from P1-2, P1-8, P2-2, P2-3, P2-10 should net a small positive.
3. A `git diff` against this draft shows the citation count rising from 3 to ~13 numbered references.
4. The Replicache paragraph treats Replicache the way the Automerge paragraph treats Automerge — fair, specific about what it does well, specific about where it stops.
5. The M-PESA paragraph is replaced with a defensible operational precedent.

When those five conditions hold, re-convene the council for Round 2 review.

---

*End of Round 1 review.*
