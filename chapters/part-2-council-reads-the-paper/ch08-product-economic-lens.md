# Chapter 8 — The Product & Economic Lens

<!-- Target: ~3,500 words -->
<!-- Source: R1 Kelsey, R2 Kelsey, v13 17, v5 7 -->

---

## Who Is Jordan Kelsey

<!-- icm/prose-review -->

Jordan Kelsey has been on both sides of the pitch. His first company was a B2C privacy-first notes app — the kind of product where the slide deck led with your data stays yours and the demo wowed everyone who saw it. It ran out of runway eighteen months in. Not because the technology failed. Because privacy-first turned out to be a value proposition that users endorsed enthusiastically in surveys and declined to pay for at checkout. He knows what it feels like to watch conversion data tell you a story your product strategy refuses to believe.

His second company was developer tooling. It got acquired for 22 million dollars. That one worked because he had learned to answer a different set of questions first: who is in pain, what does the pain cost them, and what is the smallest intervention that makes it stop. He angel-invests now and advises early-stage teams. He has reviewed more than two hundred pitches that said we will monetize with services and support. He has watched most of them fail at the same place: a business model that is theoretically correct and operationally impossible.

When Kelsey read the Inverted Stack paper, he recognized the architecture immediately. Not the specific technical decisions — those were new to him — but the structural shape of the commercial bet. An open-source core, a managed service as the revenue vehicle, a privacy story as the differentiator. He had built that company. He knew which questions it had to answer before it could survive.

---

## Act 1: Round 1 — Two Missing Business Fundamentals

### What Scored Adequately

The paper's commercial section was not empty. The unit economics sketch was more specific than most early-stage pitches Kelsey encounters — two dollars infrastructure cost per team, ten to twenty dollar pricing target is a real number, not a gesture toward a number. He scored it 7/10 with a note that it needed a worked model, not just a ratio. The competitive positioning was implicit but present: against Obsidian (single-user, no collaboration), Notion (no offline, no data ownership), Nextcloud (IT-managed only, not developer-friendly). He gave that a 7/10 as well, with a request for a comparison table that made the contrast visible without requiring the reader to reconstruct it from prose.

The OSS public-good reframe was the genuinely strong insight in the commercial section. When locally installed software has no license server to protect proprietary features, treating open-source as a vulnerability is a losing strategy. Embracing it as the strategic choice — publishing the full capability and competing on relay quality and support rather than feature access — eliminates the license-cracking problem and positions the project as infrastructure rather than a product. That is a defensible position. Kelsey commended it specifically.

Commending the strategic framing while flagging the operational gap is exactly what an experienced commercial reviewer does. The framing was right. The execution path was absent.

### No First Customer Archetype

The paper described its target market as developer communities who value data sovereignty. Kelsey scored first customer archetype 4/10 — the lowest dimensional score in his round.

The reason is specific: a demographic is not a customer. Developer communities who value data sovereignty says nothing about who picks up the phone to buy, what budget line the purchase comes from, what other software they are already paying for, or why they would switch today rather than next quarter. It does not specify the company size, the job title, the decision-making process, or what problem they are solving with the money they would spend on a relay subscription.

Kelsey had tried to sell privacy-first software to enterprise buyers. He knew the pitch that fails: you care about privacy, we protect privacy, therefore you will pay. Enterprise buyers who care about privacy already have approved vendor lists, legal review processes, and compliance frameworks. A new tool requires a procurement conversation, a security review, and a champion willing to spend political capital to shepherd an unfamiliar product through those gates. The claim that the buyer values data sovereignty addresses none of that process.

The deeper problem was that the paper had no answer to the most important commercial question: who pays first, and why do they pay today? A first customer is not just a buyer profile. It is a specific scenario — a person with a specific job, a specific pain, a specific budget, and a specific reason not to wait. The paper had no scenario.

### No OSS-to-Paid Conversion Mechanism

The paper assumed that community adoption would drive relay conversion. Kelsey scored OSS-to-paid conversion 5/10.

The assumption is not wrong — the model works for some projects. Grafana runs it. GitLab runs it. Those projects succeeded because the conversion trigger was clearly defined and structurally built into the product: Grafana users who want enterprise authentication or hosted infrastructure hit a specific capability wall that the paid tier removes. The conversion event is known, predictable, and occurs at a natural scale threshold.

The Inverted Stack paper had no equivalent specification. When does a free user become a paid user? The implication was when they need the relay — but need is not a trigger. Need is a property of the user's situation. A trigger is an event: the second team member tries to sync and cannot reach the first node because both are behind NAT. The relay solves that problem immediately. That event is the conversion trigger. The paper never named it.

Without a specified trigger, the conversion model is a hope. The team builds and ships, the OSS community grows, and at some undefined point some undefined fraction converts to paid relay. Kelsey had watched this play out at multiple portfolio companies. Without a named trigger, the converted fraction is always smaller than projected — "when they need it" never becomes a transaction without a defined trigger.

The funding and sustainability analysis scored 5/10 as well. At 100 teams paying fifteen dollars per month, that is fifteen hundred dollars per month — not a salary. The paper needed a model that showed when relay revenue covers at least one full-time engineer, and what team count achieves break-even at different price points.

### The BLOCK Verdict

Kelsey issued two blocks.

**B1 — No first customer archetype.** Developer communities who value data sovereignty is a demographic, not a customer. The paper must identify who pays first, why they pay, and how they are found. Title, company size, problem, acquisition path — all four required.

**B2 — No OSS-to-paid conversion mechanism.** The specific moment or event that causes a team to pay for the managed relay must be named. A hypothesis about community conversion is not a mechanism.

His overall domain average was 5.5/10 — the lowest Round 1 score across the council. The architecture was sound. The business case did not exist yet.

---

## What Changed Between Rounds

The author did not respond with a generic business model section. The revision made a vertical bet.

Construction project management was selected as the initial target market — and the choice was argued on specifics, not sentiment. Construction sites have documented connectivity failures; job sites in dense urban areas or remote locations lose cellular coverage routinely. Construction firms own their project data — RFI logs, punch lists, change orders, inspection records — and that data is legally significant. A subcontractor dispute resolved incorrectly because the digital record was unavailable during a service outage is not an abstract risk; it is a contract dispute. Construction project management software has a clear, measurable downtime cost: a delayed bid or a missed change order window can cost a firm a project worth multiples of a year's software spend.

The five-step customer development path was the concrete resolution to B1.

First: identify ten construction project managers through industry association channels — Associated General Contractors (AGC), Associated Builders and Contractors (ABC), or trade publications including Engineering News-Record and Constructor. Second: conduct discovery interviews focused on one question — when did software failure cost you money? Third: find the specific workflow where connectivity failure or platform outage has measurable, repeated cost. The author identified RFI tracking and punch lists as candidate workflows.

Fourth: build directly to that scenario — no generic feature development, one vertical, one workflow, one failure mode. Fifth: get one team live, measure relay activation at ninety days, and use that data to decide whether to deepen the vertical or pivot.

The relay economics were modeled across three scale tiers. A single relay instance on commodity infrastructure handles approximately 500 concurrent team connections. At a per-team infrastructure cost under two dollars per month and a pricing target of fifteen to twenty-five dollars per team per month, gross margin at scale exceeds 90 percent. The model showed the revenue at each tier and the headcount it could support.

The OSS-to-paid conversion trigger was specified precisely: the relay becomes necessary the moment a second device or a second team member needs to sync and both are behind NAT. A single user on a local network can run entirely without the relay. The moment the team grows to include a remote collaborator — or the user switches between an office workstation and a laptop on a job site — NAT traversal is required. The relay solves that problem. That event is the conversion trigger.

---

## Act 2: Round 2 — Getting to Viable

### The Customer Acquisition Channel

Kelsey scored the first customer path 8/10 in Round 2, up from 4. He acknowledged the vertical selection as well-reasoned and the five-step path as the right framework. His remaining gap was specific: the paper identified who but not where.

Cold outreach to construction project managers is notoriously difficult. They are not on LinkedIn the way software buyers are. They do not attend SaaS conferences. They are skeptical of software vendors by professional habit — the construction industry has been oversold on project management software that failed to account for job site realities, and project managers remember it. A customer development plan built on cold email or inbound content marketing is not a plan; it is a list of tactics with no conversion rate behind them.

The acquisition channel must be specified before the customer development path has an execution path. Three options exist. AGC and ABC chapter events are the highest-trust entry point: a presentation or workshop on construction technology at a chapter meeting puts the product in front of decision-makers who already trust the organizing body. Trade publications — ENR, Constructor — reach the same audience in written form; a contributed article on job site connectivity as a project risk is a credible vehicle for this product. A warm introduction through a construction technology consulting firm with established relationships with general contractors and subcontractors is the fastest path to the first three conversations.

The condition stands: specify the channel before ten design partner interviews becomes a task with no execution path.

### Unit Economics at Scale

Kelsey scored unit economics 8/10 in Round 2, up from 7. The worked model passed his threshold for credibility.

At 1,000 teams paying twenty dollars per team per month: revenue of twenty thousand dollars per month (240,000 dollars ARR), infrastructure cost of approximately two thousand dollars per month, gross margin of approximately 90 percent. Ninety percent gross margin is exceptional SaaS unit economics. The relay-as-infrastructure model produces it because the marginal cost of serving an additional team approaches zero once relay capacity exists. This is not unusual for infrastructure-layer products; it is one of the reasons the model is worth pursuing.

The gap Kelsey raised was headcount. 240,000 dollars ARR supports two to three full-time engineers at Bay Area salaries, or four to five at distributed team rates. But getting to 1,000 teams requires customer success capacity, relay operations, and active development. The paper needed a staffing model at each scale tier — not a precise forecast, but a sanity check that revenue at each stage can fund the team required to reach the next stage. Without it, the 1,000-team scenario looks viable in isolation but may not be reachable from the 100-team stage without external capital.

### The Dual-License Imperative

The AGPLv3 license choice created a condition that Kelsey flagged as high priority: the dual-license structure must be specified before the repository opens, not after the community forms.

The AGPL network use clause requires that organizations deploying the software make their modifications available under the same license. For users who do not modify the software, this is irrelevant. For enterprise customers who want to customize the application — even internal workflow modifications to the UI or report formats — the clause can trigger a compliance review that produces a categorical rejection. Some corporate legal teams maintain AGPL blocklist policies that do not involve case-by-case analysis; the license name triggers the rejection automatically.

The standard resolution is a dual-license structure: AGPLv3 for open-source users and self-hosters who accept the copyleft terms, plus a commercial license for organizations that cannot accept AGPL and are willing to pay for the exception. This is the model used by Metabase, Grafana Enterprise, and multiple other OSS-commercial projects. The commercial license tier needs a price point, a definition of which organizations require it, and a clear relationship to the managed relay subscription.

The timing condition is non-negotiable. Introducing a dual-license structure after a community has formed requires contributor license agreements (CLAs) from every contributor who has merged code. Retroactive CLA collection fails for two reasons: contributors become unreachable, and reachable contributors sometimes refuse on principle. The CLA and dual-license structure must be in place at the repository's founding, before the first external contributor opens a pull request. After that moment, the option is either expensive or foreclosed.

The specific structure the paper must document: all contributors sign a CLA assigning copyright to the project entity. The default license is AGPLv3. A commercial license is available for organizations that cannot accept AGPLv3, at a price determined by deployment scale. The relay subscription and the commercial license are separate line items; managed relay customers receive the commercial license included.

### Year-Two Failure Modes

Kelsey scored year-two failure modes 5/10 — the lowest Round 2 dimensional score. The paper's open problems section named technical risks accurately but left commercial risks unaddressed.

Three failure modes threaten a relay-funded OSS project in its second year.

**Relay commoditization.** Once the relay protocol is published and the relay server is open-source, a cloud provider can offer managed relay at infrastructure cost with no margin. The managed relay as specified has approximately 90 percent gross margin at scale — which makes it an attractive target for a provider that wants to commoditize the layer. The protocol itself cannot be the moat because it is published. The defensible position is support quality and product-integrated onboarding: a relay that is trivial to configure from within the application, with a support team that understands the full stack, competes on a dimension that infrastructure providers cannot easily match. The paper needs to articulate this moat explicitly, because without it the relay commoditization scenario ends the commercial model.

**Enterprise direct sales cost.** The fifteen to twenty-five dollar per team per month price point is incompatible with a traditional enterprise sales motion. An account executive plus solutions engineer plus legal review cycle for a deal worth three hundred dollars per year is not economically viable. But some enterprise customers — particularly in regulated industries or large general contractor firms — will require a procurement conversation, a security review, and contractual terms before deployment. The paper needs a tier structure: self-serve for teams below a headcount threshold, an enterprise tier with negotiated pricing and contractual terms for organizations above it. Without this, the product either turns away enterprise deals or absorbs enterprise sales cost against a price point that cannot support it.

**Contributor governance vacuum.** An AGPLv3 project that depends on community contributions needs a governance model before it needs a commercial model. Who approves pull requests? Who decides protocol changes? What happens when a large contributor — a company that has built significant internal tooling on top of the protocol — disagrees with a roadmap decision? Absent governance does not prevent early contributions; it creates a crisis when the first significant disagreement occurs. Foundation-backed open-source projects define governance structures at founding precisely to avoid this crisis. A BDFL model, a contributor council, or a lightweight stewardship structure are all viable; the choice matters less than making it publicly before the community depends on it.

### Round 2 Verdict: PROCEED WITH CONDITIONS

Kelsey's Round 2 average was 6.8/10, up from 5.5. All blocking issues were cleared. He issued five conditions.

**C1 (High):** Specify the customer acquisition channel for construction PM outreach. AGC/ABC chapter events, ENR/Constructor publications, or a warm introduction path through a construction technology consulting firm are the viable options. The channel must be named before the customer development path is executable.

**C2 (High):** Specify the dual-license strategy and CLA requirement at repository founding. The structure — AGPLv3 default, commercial license available, CLA required from all contributors — must be documented before the first external pull request.

**C3 (Medium):** Add a governance model section. Who approves PRs, who decides protocol changes, what is the decision-making structure for the project? The section need not be long. It needs to exist.

**C4 (Medium):** Address relay commoditization directly. Articulate what makes the managed relay defensible against infrastructure provider competition. Support quality and product-integrated onboarding are the answer; the paper needs to say so explicitly.

**C5 (Low):** Add a market sizing sentence for the construction vertical. How many construction project managers exist? What fraction use project management software? One sentence of market sizing makes the commercial section significantly more compelling to any investor who reads it.

His commendation was specific: the construction vertical selection and the five-step customer development path represented a genuine strategic advance. The distinction between a theoretical monetization model and a concrete commercial strategy is exactly the gap those additions closed.

---

## The Principle: Open Source Needs a Business Model Before the Repo Opens

Kelsey's two-round arc distills to a single operational principle: the business model must be specified before the repository goes public.

Founders from engineering backgrounds resist this sequence — the instinct is to build first, prove the technology, then figure out commercialization. That sequence works when the commercial model is straightforward: a clear product, a clear buyer. It fails when the commercial model depends on community dynamics that are set in motion the moment the repository goes live.

The dual-license structure requires a CLA from every contributor. If the CLA is not in place at founding, retroactive collection is expensive and sometimes impossible. The governance model shapes who feels ownership of the project and who feels like a contributor to someone else's commercial venture. The first-customer vertical determines what the early codebase optimizes for — and early codebase decisions compound. A project that optimizes for construction project management in year one looks different from one that optimized for general developer tooling, and changing direction requires changing the community's expectations, not just the code.

The managed relay as a revenue model has genuine structural advantages: exceptional gross margins, a natural conversion trigger at the point of multi-device or multi-user sync, and a defensible position built on support and integration quality rather than proprietary protocols. The architecture is designed for this model. The economics work. The construction vertical is a credible entry point with a documentable pain point, a reachable buyer, and a measurable success metric.

What the relay model cannot survive is launching with undefined conversion triggers, no specified license strategy, and no acquisition channel. Those are not gaps that get filled by building a better sync daemon. They are decisions that must be made before the first line of code is committed to a public repository.

The managed relay is the right unit of competitive analysis. Its defensibility rests on support quality and product-integrated onboarding — not on the protocol, which is open. Get the dual-license structure and the CLA in place before the first external contributor opens a pull request. Pick the acquisition channel before the first customer development interview. The architecture earns a PROCEED. The business earns it conditionally — and the conditions have deadlines that the technology calendar does not set.
