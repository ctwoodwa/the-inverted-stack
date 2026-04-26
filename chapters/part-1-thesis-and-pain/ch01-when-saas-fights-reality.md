# Chapter 1 — When SaaS (Software as a Service) Fights Reality

<!-- icm/prose-review -->
<!-- Target: ~5,200 words -->
<!-- Source: v13 §3, v13 Executive Summary, v13 §14.1, v13 §20.4, v5 §1 -->

---

It is two o'clock in the afternoon and Marcus is staring at a browser tab that will not load. He is the project manager on a $4.2 million commercial renovation. His general contractor's bid is due at five. The owner group meets at six. The project management platform his firm runs on has been down since eleven that morning.

The data is not gone. It exists, somewhere — on servers in Virginia, or Oregon, or wherever the cloud region happens to be that day. The labor breakdown, the subcontractor bids, the change order history, the payment schedule — all of it sits intact on a hard drive Marcus will never touch, in a building he could not find on a map. It is simply not accessible. The vendor's status page calls it an outage "affecting less than 1% of users." On this bid, that one percent is everyone.

His options narrow as the clock runs. Reconstruct what he can from the email trail. Export a stale PDF from before the platform went down. Ask his client to extend the deadline — and explain to a board, two hours from now, why his firm wasn't ready.

This is not a planning failure. He planned correctly. He had his data. His team used the software. Everything was in order. The failure is structural: his data lives on infrastructure he doesn't control, and when that infrastructure goes offline, his capability goes with it.

The scenario repeats across industries that run on deadline-sensitive work — the attorney preparing a brief at nine in the evening, the engineer updating safety documentation in the field, the physician reaching for patient records before rounds. The infrastructure fails identically. Only the deadline changes.

---

## The Bundle Nobody Agreed To

The SaaS deal goes like this. Give us your data. Keep it on our servers. Pay us every month. In exchange you get real-time collaboration, multi-device access, and zero maintenance. Most users said yes without fully registering the second half. The first half was the product. The second half was the terms.

The three desirable properties are real. Real-time collaboration is transformative — two people editing the same document, watching each other's changes appear, never again emailing attachments back and forth. Multi-device access means your work is on your phone when you need it at the airport. Zero maintenance means IT does not nurse a server in a closet; the vendor handles it. These are genuine improvements over what came before them.

The three conditions on the other side of the bundle get less attention. Your data lives on vendor infrastructure, which means the vendor can see it, lose it, sell the company that holds it, or turn the service off. Pricing is at the vendor's discretion — the rate when you adopted the software is not a commitment. It is a starting point. Service continuity is contingent on the vendor's survival: if the company gets acquired, runs out of money, or decides to sunset the product, your software stops working when theirs does.

The acceptance was rational. Neither half of the bundle is fully visible at adoption time. The terms of service when a company signs up and the terms of service three acquisitions later are different documents. The pricing that wins a customer's business is designed to win it — not to represent what the platform costs after that customer has built their workflows, trained their staff, and transferred their data. The bundle reveals itself slowly, after the switching costs have accumulated.

Users accepted these conditions because the three desirable properties appeared to *require* them. Real-time collaboration required a central server both parties could talk to. Multi-device sync required a cloud that acted as the authoritative copy. Zero maintenance required that the vendor control the infrastructure. The package looked indivisible because, with the technology of 2010, it largely was.

That is no longer true.

---

## Six Ways SaaS Breaks in the Field

### The Outage That Takes Your Work With It

Major SaaS providers report 99.9% uptime — roughly 8.7 hours of downtime per year. For a single user, those hours scatter harmlessly across the calendar and rarely land at a bad moment. For a team of ten, at any given moment somebody is in the middle of something time-sensitive. Marcus's 8.7 hours found him on a bid deadline.

The outage that gets published is the one the vendor is willing to call an outage. The incidents that affect partial regions, specific features, or specific customer cohorts surface as "degraded performance" — a phrase that does most of its work by not being the word *outage*. From the affected user's side, degraded performance means the site loads but submissions fail silently, changes save and then revert, or search returns stale results. This is harder to work around than a clean outage, because it is not obvious that the problem is the platform rather than something the user did. With a clean outage you know to stop trying. With degraded performance you keep trying — and the failure looks like something you did.

What makes outage risk asymmetric is that it falls hardest on the moments that matter most. High-stakes work — deadline submissions, live customer sessions, critical handoffs — tends to involve intensive platform use, which means it is more exposed to performance degradation under load. And the work that can least tolerate delay tends to be the work with external dependencies: bids due to clients, documents due to regulators, reports due to boards. These are not moments where "try again in an hour" is an option.

The construction PM example is not unusual for the industry. Construction project management is deadline-driven by definition. A subcontractor bid has a submission deadline that is not negotiable after the fact. A change order authorization has a response window tied to contract terms. A safety inspection log has a regulatory timestamp requirement. When any of these processes depends on cloud infrastructure being available exactly when needed, the infrastructure becomes a single point of failure in a workflow that cannot tolerate one.

Availability statistics miss a compounding factor. The concentration of cloud hosting means failures cascade across unrelated products at the same instant. An AWS us-east-1 availability zone failure affects every product hosted there — project management tools, document collaboration platforms, file storage services, communication tools — at the same moment. A single incident becomes an industry-wide incident for everyone whose vendor chose the same region. Users who experience a simultaneous failure across multiple tools they rely on do not find redundancy in having adopted multiple platforms; they find that all their fallback options went down at the same time. This is the dependency chain. Not your vendor failing, but the infrastructure layer beneath your vendor — shared cloud regions, CDN providers, authentication services — none of which appear in your vendor's SLA (Service Level Agreement), and none of which you have any contract with.

Outages hit hardest the users who can least work around them. Assistive technology users — those who rely on screen readers, switch access devices, or voice control software — experience SaaS connectivity failure as complete access failure. The screen reader announces a failed load. Voice control has no form fields to target. The application stops responding. Degraded performance that a connected user circumvents by refreshing is inaccessible in a more absolute sense — the AT user cannot navigate what is not there. The architecture this book describes keeps the application responsive regardless of network state. For AT users, this is not a usability improvement. It is the difference between accessible and inaccessible software.

### The Vendor That Disappears

In 2015, Sunrise Calendar had approximately 1.5 million users and was widely considered the best third-party calendar app for iOS. Microsoft acquired it that year. Microsoft shut it down in September 2016. Users received a few weeks' notice. The data was exportable — in a format that no other calendar app read natively, requiring manual remapping of categories and recurrence rules.

Sunrise was not exceptional. It was typical of how software products end.

The mechanism changes — acquisition, runway exhaustion, a strategic pivot, the founder taking a job somewhere larger — but the pattern is consistent. The product goes dark. Users who built their workflows around it are left with whatever they managed to export before the deadline.

Salesforce acquired Quip and deprioritized it; teams that had built workflows around its document structure found the investment worthless on migration because the structure was stored in a format only Quip controlled. That is not a product failure. It is the custody model working exactly as designed: the user's workflow lives on vendor infrastructure until it doesn't.

The data export problem deserves specific attention. When a vendor announces shutdown, it typically offers an export function. What that export contains, what format it uses, and whether any other software can actually consume it are highly variable. For calendar data, iCal is reasonably standard. For project management data, vendors typically export a CSV of the task list — without the comments, without the attachment history, without the relationship structure that made the tool useful. For document collaboration, most platforms offer a PDF export, which preserves the appearance but none of the editability.

The legal firm whose vendor gets acquired faces this directly. They adopted the software, trained staff, integrated it with billing and document management workflows, and accumulated years of matter history. Now they evaluate whether to migrate to the acquirer's competing product under the acquirer's pricing, or start over with a third party, reconstructing what they can from a flat CSV and a folder of PDFs.

The risk has a name that undersells it. *Vendor shutdown* sounds like a rare catastrophe. It is routine. Thousands of SaaS products shut down every year. Most are small enough that their shutdowns do not make news; their users find out through an email or a banner in the app. The shutdowns that do make news — Evernote's degraded state following years of ownership changes, Google Reader's abrupt termination in 2013 despite millions of active users, the steady stream of products acquired into enterprise platforms and starved of investment — are notable primarily because of the scale of the disruption, not because the pattern is unusual.

### The Connectivity That Wasn't There

Not everyone's internet is always on — and this is consistently underweighted in the architecture of software sold to the industries where it most frequently fails.

Construction sites operate at the edge of mobile coverage. A superintendent in a concrete frame building cannot get a signal three floors underground. Rural professional service firms — accounting firms in small towns, medical practices in counties with limited broadband, legal practices in areas where fiber has not reached — operate on connectivity that drops daily and fails entirely during weather events. Hospital clinical environments include zones where mobile devices are restricted near sensitive equipment. Air-gapped facilities — manufacturing, defense, government — cannot connect to any external network at all as a policy requirement.

For these users, offline capability is not a feature request. It is the baseline requirement.

The SaaS vendor's marketing page says "works on mobile," which is true when there is a signal. It does not say "works when there isn't one," because the centralized architecture makes that impossible without fundamental redesign. The application is a thin client rendering views from a remote database. Remove the remote database and the client has nothing to render.

Most SaaS platforms offer some form of "offline mode." What this means in practice is usually a read-only cache of recently viewed data, with form submissions that queue locally and attempt to upload when connectivity returns — with uncertain success rates and no visibility into what actually synced. You can view the last-synced version of a document. You cannot create new records, cannot run reports, cannot access data you have not recently viewed, and cannot have any confidence that what you submitted offline actually made it to the server.

The field operations manager who needs to log a safety inspection at seven in the morning on a construction site, before the crew starts work, has a few options when the SaaS is unreachable. Write it in a notebook and transcribe it later, with all the transcription errors that introduces. Use the app's read-only offline mode and hope the form submission queues correctly. Or skip the log and fill it in from memory when back in the office. All three options introduce risk. None of them should be necessary. The software should work on a construction site because that is where the work happens.

The mismatch extends beyond any single vertical. Reliable internet access is not universal, even in developed economies. Hospital clinical environments restrict wireless devices near sensitive equipment. Manufacturing and warehouse floors often have RF environments hostile to Wi-Fi. Agricultural operations span hundreds of acres — the field where something needs to be logged is rarely next to the fiber drop. Emergency response personnel work in exactly the places infrastructure fails first. For all of these workers, SaaS software's connectivity assumption is not an occasional inconvenience. It is a systematic design error applied to environments the designers never worked in.

Intermittent connectivity is not a US edge case. It is the global operational baseline. In Nigeria and South Africa, scheduled load-shedding cuts power for six to twelve hours daily; when electricity goes, routers and base stations go with it, and connectivity fails regardless of coverage quality. Hundreds of millions of enterprise workers in those economies plan their workdays around outage schedules, not around the assumption that the network is always available. In India, the 4G/3G/2G coverage gradient means that enterprise field operations — agricultural services, construction, financial services, healthcare — routinely run on intermittent connectivity across large portions of Tier 2 and Tier 3 cities and rural areas. Rural Brazil, rural Mexico, and most of Southeast Asia present comparable patterns at comparable scale. A SaaS platform that cannot function without a persistent connection does not have a niche offline problem. It has an architecture that excludes the majority of the world's enterprise users from full functionality.

### The Data You Can't Get Back

Your vendor's terms of service say your data is yours. They are often technically correct — the vendor does not claim ownership of the content you create. What the terms of service do not address is *accessibility*.

Data that you own but cannot retrieve is data you do not have.

Four mechanisms make data inaccessible while it technically "belongs" to you.

Export rate limits are the first. Many platforms allow data export but rate-limit the export API (Application Programming Interface) to prevent bulk extraction. A legal firm with ten years of matter history attempting a bulk export may find that retrieving its own data at the permitted rate takes weeks. During that window, the firm remains dependent on the vendor's infrastructure to operate — which is, not coincidentally, exactly the position the vendor prefers it to be in.

Proprietary formats are the second. The export is available, but in a format only the vendor's tools read well. Attachments export without their metadata. Comment threads export as flat text without threading structure. Custom fields export as raw column headers without the semantic context that made them useful. The data is present; the information it represented is partially lost.

Feature-gated access is the third. Some platforms require paid subscriptions to access export features, or limit export to higher pricing tiers. Users on free or lower tiers discover that their data is portable only as long as they keep paying — which means it is not portable at all.

Account closure timing is the fourth. When a user cancels a subscription, access typically ends when the billing period ends. A user who cancels on the first of the month with a billing cycle that ends on the fifteenth has fifteen days to export before the account closes. Miss that window — because you changed jobs, because the cancellation notice did not clearly state the deadline — and the data may be gone.

None of these are edge cases. They are the routine operational parameters of vendor-managed data. Users encounter them not as occasional anomalies but as the standard cost of cloud data custody.

### The Price That Changes After You've Committed

Switching costs in SaaS are high because users build workflows around software. Training, integrations, historical data, learned patterns — these represent real investments. Vendors know this. Pricing structures often reflect it.

Pricing is competitive during the acquisition phase, when vendors are winning customers and competing on features and price. After adoption, when the switching cost is real and rising, pricing pressure relaxes. A company that adopted a project management platform at $8 per seat per month, built an organization-wide workflow on it over two years, and now faces a renewal at $18 per seat per month confronts a real calculation: pay the new rate, or absorb the migration cost. The migration cost is often large enough that the price increase wins.

Feature paywalls move in one direction. Features available on a given tier at adoption are not guaranteed to remain there. The roadmap description from three years ago that listed a capability as "included on Professional" may not match the current pricing page. Users who built workflows on features they understood to be included sometimes discover those features now require the next tier up.

The per-seat model creates structural pressure as teams grow. A ten-person team's annual SaaS bill is manageable. A fifty-person team's bill at the same per-seat rate is five times larger, and by the time a company has reached fifty people using a platform, the switching cost has compounded accordingly. Teams that grow into enterprise sizes often find that per-seat pricing which was attractive at ten seats has become a significant budget line that IT attempts to renegotiate — often without success, because leverage has shifted.

Mid-contract price changes are less common but not rare. Platform economics shift, investor pressure changes, the competitive landscape evolves. Users who committed workflows and data to a platform signed a contract of sorts — and then discovered the other party's interpretation of that contract differed from their own.

The lock-in compounds when teams use multiple SaaS products that integrate with each other. A project management platform connected to a communication tool, a file storage service, a time tracker, and a billing system creates a dependency web where each integration raises the switching cost of every other platform. When one vendor raises prices, the team is not evaluating that product in isolation — they are evaluating the cost of unwinding a set of integrations built over years. Integration ecosystems serve the vendor's retention objectives as reliably as they serve the user's productivity. The web of dependencies is not a side effect of the SaaS model. From the vendor's perspective, it is a feature of it.

### The Third-Party Veto

The first five failure modes originate inside the service relationship. The vendor fails, decides, or prices. Both the vendor and the customer are subject to the same disruption, and in most cases neither party wanted it.

The sixth does not. An external authority — a government, a regulator, a court — restricts access regardless of what either party wants. The vendor has not failed. The customer has not been negligent. A third party with authority over one or both sides of the relationship has acted, and the service relationship cannot continue.

The authority can act on the vendor. In 2022, Western SaaS providers — Adobe, Autodesk, Microsoft, Figma ([figma.com](https://www.figma.com/), the design tool), and dozens of others — suspended service across Russia and CIS (Commonwealth of Independent States) markets under sanctions enforcement; hundreds of thousands of organizations in those markets, which had built workflows on Western SaaS over more than a decade, found their operations interrupted not because their vendors failed them but because their vendors were directed to stop serving them. Software that had been licensed, trained on, and integrated into operational workflows became inaccessible with days of notice, not months. In February 2026, the US Defense Secretary designated Anthropic's AI services a national security supply-chain risk. Federal agencies with active Anthropic deployments — deployments they found valuable and wished to continue — received direction under executive order to cease using them. Anthropic contested the designation legally, and a California court subsequently enjoined portions of the order for civilian agencies. The Department of Defense exclusion stood. Both Anthropic and its federal customers wanted to continue the relationship. Neither controlled the outcome. The analytically significant detail in both cases: the restriction came from a party with authority over the vendor, independent of both the vendor's and the customer's preferences.

The authority can act on the customer. Russia's Federal Law 242-FZ — among the first general-purpose data localization laws globally, predating GDPR (General Data Protection Regulation) by two years — has required since 2015 that personal data of Russian citizens be stored on servers located within Russia; organizations using Western SaaS found themselves structurally non-compliant not because their vendor did anything but because the SaaS architecture cannot provide on-premises data residency by design. The European Court of Justice's 2020 Schrems II ruling constrained EU organizations from transferring personal data to US cloud providers without adequate supplemental safeguards — the vendor continued operating; the customer's legal ability to continue using it was constrained. India's DPDP (Digital Personal Data Protection) Act 2023 is now creating comparable obligations for Indian organizations using US-hosted services for Indian residents' personal data. In each case, the customer becomes non-compliant regardless of the vendor's preferences or actions.

The structural property that makes this failure mode distinct: data custody determines exposure. Data in vendor infrastructure can be reached by a government action targeted at the vendor. Data on hardware the user controls requires action targeted specifically at the user. The architecture either concentrates that exposure surface at the vendor or distributes it.

---

## Who Pays the Most

These six failure modes do not hit every organization equally. The organizations most exposed share a characteristic: they have the least structural leverage to address any of them.

A large enterprise with a skilled procurement and IT organization can negotiate. Data portability clauses, SLAs with financial penalties, escrow provisions for source code and data — these are available to buyers with enough revenue to make the vendor's legal team engage seriously. When the vendor gets acquired, the enterprise has attorneys who can enforce contract terms or negotiate exit conditions.

Small and medium-sized professional service firms do not have this leverage. The legal practice with eight attorneys signs up through a website. The medical group with four physicians clicks through a terms of service that nobody reads. The construction firm with two project managers pays by credit card. Their vendor contract is the standard terms of service, unmodified. They have no SLA. They have no escrow. They have no explicit data portability requirement. If the vendor changes pricing, those users have no mechanism to object. If the vendor shuts down, they have whatever the shutdown announcement says they have.

These are also the organizations where software failures have direct professional consequences rather than just operational inconvenience. The construction PM missing a bid deadline loses the bid — and damages the relationship with the client. The legal practice unable to access case files has a professional responsibility exposure. The medical practice that cannot retrieve patient records has regulatory risk. The stakes of availability are not abstract.

And these organizations are the primary addressable market for the products most likely to carry the SaaS risks described above. The large enterprise with the IT team and the procurement counsel is using enterprise-licensed software with negotiated protections. The eight-attorney law firm is using the same product tier as the freelancer, under the same standard terms, with the same structural exposure to every failure mode described in this chapter.

This is not a coincidence. The SaaS bundle packages its desirable and undesirable properties together in a way that affects smaller buyers more severely, because smaller buyers have less ability to negotiate the undesirable half away.

The regulatory dimension compounds this asymmetry. A legal practice storing confidential client communications in a vendor's cloud carries a professional duty to understand where that data lives and who can access it. A medical practice has HIPAA (Health Insurance Portability and Accountability Act) obligations. A construction firm with government contracts may have data residency requirements tied to those contracts. For large enterprises, these obligations get negotiated into vendor agreements with audit rights and data processing addenda. For the eight-attorney firm, the compliance answer is the vendor's standard privacy policy — a document written to protect the vendor, not the client.

The jurisdictional scope of this compliance argument is wider than US-centric discussions typically acknowledge. The EU's Schrems II ruling, India's Digital Personal Data Protection Act 2023, and the UAE's DIFC (Dubai International Financial Centre) Data Protection Law 2020 are representative — each, in different language, makes data residency a compliance mechanism rather than a preference. The same pattern repeats across more than thirty national and regional frameworks; the full coverage table for this chapter is in Appendix F. In each of these jurisdictions, an architecture where data lives on the user's own hardware — not in a vendor's cloud region — is not merely preferred. In many configurations, it is the architecture that makes compliance tractable. The book's architecture is frequently a legal requirement before it is an architectural choice.

---

## Why Users Have Accepted This

Until recently, they did not have a choice.

Real-time collaboration requires that all parties see consistent state when they make concurrent changes. In 2008, the most practical way to guarantee this was a central server both parties could read from and write to simultaneously. Every other approach — emailing files, shared drives, version control — introduced either merge conflicts requiring manual resolution or coordination overhead requiring explicit locking. Real-time collaboration solved both problems by making divergence impossible: one copy, everyone editing the same one.

Multi-device sync requires an authoritative copy that all devices agree on. When the cloud holds the authoritative copy, sync is the cloud pushing updates to each device. Without a cloud authority, devices have to figure out among themselves which version is current — and the consumer-grade protocols for resolving concurrent edits across devices reliably, at scale, without requiring user intervention, did not exist. Merging concurrent edits deterministically, without a server to adjudicate conflicts, was an unsolved problem for end-user software.

Zero maintenance requires that someone else manage the infrastructure. The alternative is the user managing it, which requires IT capability that most small organizations do not have and do not want to develop. The comparison to self-hosted software circa 2005 is instructive: a self-hosted email server, a self-hosted project tracker, a self-hosted document collaboration platform — all theoretically possible, all practically demanding enough that most organizations paid someone else to handle it.

The dependencies looked structural because they were structural. The technology for delivering these properties without vendor infrastructure either did not exist or was not mature enough to deploy without specialized expertise. CRDTs (Conflict-free Replicated Data Types) were academic research with a handful of experimental implementations. Gossip protocols ran inside distributed databases; nobody was building them into end-user applications. Container runtimes existed for server workloads; the packaged, embeddable, consumer-invisible form that makes Docker Desktop run silently on your laptop had not been built.

Users accepted the SaaS bundle not because they preferred the conditions on the second half but because the technology of the time made those conditions appear to be the cost of the first half. They were not accepting a bargain so much as acknowledging a constraint.

The constraint is removable — by the architecture this book describes.

The evidence is commercial, not theoretical. The earliest and most consequential proof is African mobile money. M-PESA has processed financial transactions for hundreds of millions of users across East Africa since 2007; MTN MoMo operates at comparable scale across dozens of African markets. Both are built on offline-tolerant transaction patterns — store-and-forward reconciliation, intermittent-network authorization, operational continuity through connectivity gaps — because the networks they run on require it. Local-first architecture is not a new idea awaiting adoption; it has operated at population scale for nearly two decades in the markets that most benefit from it. In the professional software space, Actual Budget — commercially deployed to a substantial and growing user base — delivers full personal finance capability on local storage; its sync service is optional. Linear ([linear.app](https://linear.app/), the issue tracker) — commercially deployed across thousands of engineering teams worldwide — runs its sync engine on a local SQLite replica; the cloud is already demoted to a relay peer. These products demonstrate that the desirable half of the SaaS bundle — collaboration, sync, responsive UI — does not require vendor data custody to function. Users who have worked with software built on these foundations have a reference point. They know what it feels like when software keeps running after the internet goes out. The acceptance erodes when the alternative is observable, not theoretical.

---

## The Dependency That Looks Inevitable

Three specific technology shifts made the structural necessity of the SaaS bundle removable.

**CRDTs in production.** Conflict-free replicated data types provide an algorithm for merging concurrent edits without a central coordinator. Two users edit the same document offline, reconnect, and see a deterministically merged result — no data loss, no manual conflict resolution, no authority required to adjudicate. The merge algorithm guarantees convergence; whether the result reflects the users' semantic intent is a property of how the application models its domain. This is not theoretical. It is the mechanism Linear uses for simultaneous task edits, the mechanism behind Automerge ([github.com/automerge/automerge](https://github.com/automerge/automerge), a JSON-like CRDT (Conflict-free Replicated Data Type) library) and Yjs ([github.com/yjs/yjs](https://github.com/yjs/yjs), the JavaScript CRDT library) and the growing family of production CRDT (Conflict-free Replicated Data Type) libraries, and the basis for Actual Budget's fully local data model. Figma uses CRDTs for multiplayer cursor coordination, but Figma's data resides on Figma's servers — it is not a data-sovereignty architecture. The data-sovereignty proof points are Linear (local SQLite replica, sync to cloud) and Actual Budget (fully local SQLite, cloud sync optional): both keep authoritative state on the device. The central server that served as the authority for "what's the current version of this document" is replaceable by a mathematically guaranteed merge that does not require an authority.

**Gossip protocols at the edge.** Leaderless replication — gossip algorithms, anti-entropy sync, vector clocks — allows nodes to synchronize state without a master. Every peer can accept writes; every peer eventually converges to the same state. Cassandra and DynamoDB operate at planetary scale using these mechanisms. On a five-person team with five workstations, the same protocols work without any cloud relay at all: when the machines are on the same network, they sync directly. When they are not, they sync through any reachable relay, including a user-controlled one.

**The local service pattern.** Container runtimes, and specifically the background-service model that tools like Docker Desktop and Tailscale established, made it normal for complex multi-service software to run silently on a user's machine without requiring the user to manage it. The pattern of a native UI shell connecting to a locally running application server is not novel — VS Code does it with language servers, 1Password does it with its desktop helper, Tailscale does it with its mesh daemon. The user experience is indistinguishable from a cloud application. The infrastructure is local.

These three shifts happened independently, solving problems that had nothing to do with the SaaS bundle. CRDTs were a distributed systems research problem. Gossip protocols were a database scaling problem. Container runtimes were a server deployment problem. The consequence — that the technical necessity of the SaaS bundle is now removable — followed from solutions to those other problems. The architecture has real costs: operational complexity, key management, schema migration across independent nodes, and upgrade coordination replace vendor dependency. The rest of this book addresses each of those costs directly.

Marcus's scenario — deadline-critical work held hostage by infrastructure he does not control — is the failure mode this architecture addresses first. His data was never gone. It was inaccessible because the software's design placed it somewhere he could not reach. The rest of this book specifies a design where that distinction does not exist.

What remains is the reference architecture: how to assemble these proven components into a coherent, deployable architecture that behaves like a cloud application, passes enterprise security review, and treats user data ownership as a structural guarantee rather than a contractual one.

The building blocks are production-proven. What remains is the specific assembly that produces a node — not a smarter cache, not a thicker client, but a first-class local peer. Chapter 2 identifies exactly what that requires and where the existing work stops short. Chapter 3 draws the node.
