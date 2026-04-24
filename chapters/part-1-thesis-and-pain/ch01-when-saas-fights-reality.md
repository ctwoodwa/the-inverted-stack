# Chapter 1 — When SaaS Fights Reality

<!-- icm/prose-review -->
<!-- Target: ~4,500 words -->
<!-- Source: v13 §3, v13 Executive Summary, v13 §14.1, v13 §20.4, v5 §1 -->

---

Marcus is the project manager on a $4.2 million commercial renovation. His general contractor's bid is due at 5 PM — the owner group has a board meeting at 6. The project management platform his firm runs on has been down since 11 AM. It's now 2 PM.

The data isn't gone. It's on servers in Virginia, or Oregon, or wherever the cloud region is. The labor breakdown, the subcontractor bids, the change order history, the payment schedule — all of it exists. It's just not accessible because the service is experiencing an outage affecting "less than 1% of users," which, from Marcus's perspective, means 100% of the users who matter right now.

His options: reconstruct what he can from the email trail. Export a stale PDF from before the platform went down. Ask his client to extend the deadline, which reflects poorly on his firm.

This is not a planning failure. He planned correctly. He had his data, his team used the software, everything was in order. The failure is structural: his data lives on infrastructure he doesn't control, and when that infrastructure goes offline, his capability goes with it.

This scenario repeats across industries that run on deadline-sensitive work — the attorney preparing a brief at 9 PM, the engineer updating safety documentation in the field, the physician accessing patient records before rounds. The infrastructure failure is identical; only the deadline changes.

---

## The Bundle Nobody Agreed To

The SaaS deal goes like this: give us your data, keep it on our servers, pay us every month, and in exchange you get real-time collaboration, multi-device access, and zero maintenance. Most users said yes without fully registering the second half. The first half was the product. The second half was the terms.

The three desirable properties are real. Real-time collaboration is transformative — two people editing the same document, watching changes appear, not emailing attachments back and forth. Multi-device access means your work is on your phone when you need it at the airport. Zero maintenance means IT doesn't manage a server; the vendor handles it. These are genuine improvements over what preceded them.

The three conditions on the other side of the bundle get less attention. Your data lives on vendor infrastructure, which means the vendor can see it, lose it, sell the company that holds it, or turn the service off. Pricing is at the vendor's discretion — the rate when you adopted the software is not a commitment, it's a starting point. Service continuity is contingent on the vendor's survival: if the company gets acquired, runs out of money, or decides to sunset the product, your software stops working when theirs does.

The acceptance was rational. Neither half of the bundle is fully visible at adoption time. The vendor's terms of service when a company signs up and the vendor's terms of service three acquisitions later are different documents. The pricing that wins a customer's business is designed to win it — not to represent what the platform costs after that customer has built their workflows, trained their staff, and transferred their data. The bundle reveals itself over time, after the switching costs have accumulated.

Users accepted these conditions because the three desirable properties appeared to *require* them. Real-time collaboration required a central server both parties could talk to. Multi-device sync required a cloud that acted as the authoritative copy. Zero maintenance required that the vendor control the infrastructure. The package looked indivisible because, with the technology of 2010, it largely was.

That is no longer true.

---

## Five Ways SaaS Breaks in the Field

### The Outage That Takes Your Work With It

Major SaaS providers report 99.9% uptime — roughly 8.7 hours of downtime per year. For a single user, those hours distribute across the year and rarely land at a bad moment. For a team of ten, at any given moment someone is more likely to be in the middle of something time-sensitive. Marcus's 8.7 hours found him on a bid deadline.

The outage that gets published is the one the vendor is willing to call an outage. The incidents that affect partial regions, specific features, or specific customer cohorts often appear as "degraded performance" rather than a declared incident. From the affected user's side, degraded performance means the site loads but submissions fail silently, changes save and then revert, or search returns stale results. This is harder to work around than a clean outage, because it's not obvious that the problem is the platform rather than the user's own actions.

What makes outage risk particularly asymmetric is that it falls hardest on the moments that matter most. High-stakes work — deadline submissions, live customer sessions, critical handoffs — tends to involve intensive platform use, which means it's more exposed to performance degradation under load. And the work that can least tolerate delay tends to be the work with external dependencies: bids due to clients, documents due to regulators, reports due to boards. These are not moments where "try again in an hour" is an option.

The construction PM example is not unusual for the industry. Construction project management is deadline-driven by definition. A subcontractor bid has a submission deadline that is not negotiable after the fact. A change order authorization has a response window tied to contract terms. A safety inspection log has a regulatory timestamp requirement. When any of these processes depends on cloud infrastructure being available exactly when needed, the infrastructure is a single point of failure in a workflow that cannot tolerate one.

Availability statistics miss a compounding factor: the concentration of cloud hosting means that failures cascade across unrelated products simultaneously. An AWS us-east-1 availability zone failure affects every product hosted there — project management tools, document collaboration platforms, file storage services, communication tools — at the same moment. A single incident becomes an industry-wide incident for everyone whose vendor chose the same region. Users who experience a simultaneous failure across multiple tools they rely on don't find redundancy in having adopted multiple platforms; they find that all their fallback options went down at the same time.

### The Vendor That Disappears

In 2015, Sunrise Calendar had approximately 1.5 million users and was widely considered the best third-party calendar app for iOS. Microsoft acquired it in 2015 and shut it down in September 2016. Users received a few weeks' notice. The data was exportable — in a format that no other calendar app read natively, requiring manual remapping of categories and recurrence rules.

Sunrise wasn't exceptional. It was typical of how software products end.

The mechanism changes — acquisition, runway exhaustion, a strategic pivot, the founder taking a job somewhere larger — but the pattern is consistent. The product goes dark. Users who built their workflows around it are left with whatever they managed to export before the deadline.

Salesforce acquired Quip and deprioritized it; teams that had built workflows around its document structure found the investment worthless on migration because the structure was stored in a format only Quip controlled. That is not a product failure. It is the custody model working exactly as designed: the user's workflow lives on vendor infrastructure until it doesn't.

The data export problem deserves specific attention. When a vendor announces shutdown, it typically offers an export function. What that export contains, what format it uses, and whether any other software can actually consume it are highly variable. For calendar data, iCal is reasonably standard. For project management data, vendors typically export a CSV of the task list — without the comments, without the attachment history, without the relationship structure that made the tool useful. For document collaboration, most platforms offer a PDF export, which preserves the appearance but none of the editability.

The legal firm whose vendor gets acquired faces this directly. They adopted the software, trained staff, integrated it with billing and document management workflows, and accumulated years of matter history. Now they evaluate whether to migrate to the acquirer's competing product under the acquirer's pricing, or start over with a third party, reconstructing what they can from a flat CSV and a folder of PDFs.

This risk has a name that undersells it. "Vendor shutdown" sounds like a rare catastrophe. It's routine. Thousands of SaaS products shut down every year. Most are small enough that their shutdowns don't make news. Their users find out through an email or a banner in the app. The shutdowns that do make news — Evernote's degraded state following years of ownership changes, Google Reader's abrupt termination in 2013 despite millions of active users, the steady stream of products acquired into enterprise platforms and starved of investment — are notable primarily because of the scale of the disruption, not because the pattern is unusual.

### The Connectivity That Wasn't There

Not everyone's internet is always on — and this is consistently underweighted in the architecture of software sold to the industries where it most frequently fails.

Construction sites operate at the edge of mobile coverage. A superintendent in a concrete frame building can't get a signal three floors underground. Rural professional service firms — accounting firms in small towns, medical practices in counties with limited broadband, legal practices in areas where fiber hasn't reached — operate on connectivity that drops daily and fails entirely during weather events. Hospital clinical environments include zones where mobile devices are restricted near sensitive equipment. Air-gapped facilities — manufacturing, defense, government — cannot connect to any external network at all as a policy requirement.

For these users, offline capability is not a feature request. It is the baseline requirement.

The SaaS vendor's marketing page says "works on mobile," which is true when there's a signal. It doesn't say "works when there isn't one," because the centralized architecture makes that impossible without fundamental redesign. The application is a thin client rendering views from a remote database. Remove the remote database and the client has nothing to render.

Most SaaS platforms offer some form of "offline mode." What this means in practice is usually: a read-only cache of recently viewed data, with form submissions that queue locally and attempt to upload when connectivity returns — with uncertain success rates and no visibility into what actually synced. You can view the last-synced version of a document. You cannot create new records, cannot run reports, cannot access data you haven't recently viewed, and cannot have any confidence that what you submitted offline actually made it to the server.

The field operations manager who needs to log a safety inspection at 7 AM on a construction site before the crew starts work has a few options when the SaaS is unreachable: write it in a notebook and transcribe it later (with all the transcription errors that introduces), use the app's read-only offline mode and hope the form submission queues correctly, or skip the log and fill it in from memory when back in the office. All three options introduce risk. None of them should be necessary. The software should work on a construction site because that's where the work happens.

The scale of this mismatch extends beyond any single vertical. Reliable internet access is not universal, even in developed economies. Hospital clinical environments restrict wireless devices near sensitive equipment. Manufacturing and warehouse floors often have RF environments hostile to Wi-Fi. Agricultural operations span hundreds of acres — the field where something needs to be logged is rarely next to the fiber drop. Emergency response personnel work in exactly the places infrastructure fails first. For all of these workers, SaaS software's connectivity assumption is not an occasional inconvenience. It is a systematic design error applied to environments the designers never worked in.

Intermittent connectivity is not a US edge case — it is the global operational baseline. In Nigeria and South Africa, scheduled load-shedding cuts power for six to twelve hours daily; when electricity goes, routers and base stations go with it, and connectivity fails regardless of coverage quality. Hundreds of millions of enterprise workers in those economies plan their workdays around outage schedules, not around the assumption that the network is always available. In India, the 4G/3G/2G coverage gradient means that enterprise field operations — agricultural services, construction, financial services, healthcare — routinely run on intermittent connectivity across large portions of Tier 2 and Tier 3 cities and rural areas. Rural Brazil, rural Mexico, and most of Southeast Asia present comparable patterns at comparable scale. A SaaS platform that cannot function without a persistent connection does not have a niche offline problem. It has an architecture that excludes the majority of the world's enterprise users from full functionality.

### The Data You Can't Get Back

Your vendor's terms of service say your data is yours. They're often technically correct — the vendor does not claim ownership of the content you create. What the terms of service don't address is *accessibility*.

Data that you own but cannot retrieve is data you don't have.

Four mechanisms make data inaccessible while it technically "belongs" to you.

Export rate limits are the first. Many platforms allow data export but rate-limit the export API to prevent bulk data extraction. A legal firm with ten years of matter history attempting a bulk export may find that retrieving their own data at the permitted rate takes weeks. During that window, they remain dependent on the vendor's infrastructure to operate — which is, not coincidentally, exactly the position the vendor prefers them to be in.

Proprietary formats are the second. The export is available but in a format only the vendor's tools read well. Attachments export without their metadata. Comment threads export as flat text without threading structure. Custom fields export as raw column headers without the semantic context that made them useful. The data is present; the information it represented is partially lost.

Feature-gated access is the third. Some platforms require paid subscriptions to access export features, or limit export to higher pricing tiers. Users on free or lower tiers discover that their data is portable only as long as they keep paying — which means it isn't portable at all.

Account closure timing is the fourth. When a user cancels a subscription, access typically ends when the billing period ends. A user who cancels on the first of the month with a billing cycle that ends on the fifteenth has fifteen days to export before the account closes. Miss that window — because you changed jobs, because the cancellation notice didn't clearly state the deadline — and the data may be gone.

None of these are edge cases. They are the routine operational parameters of vendor-managed data. Users encounter them not as occasional anomalies but as the standard cost of cloud data custody.

### The Price That Changes After You've Committed

Switching costs in SaaS are high because users build workflows around software. Training, integrations, historical data, learned patterns — these represent real investments. Vendors know this. Pricing structures often reflect it.

Pricing is competitive during the acquisition phase, when vendors are winning customers and competing on features and price. After adoption, when the switching cost is real and rising, pricing pressure relaxes. A company that adopted a project management platform at $8 per seat per month, built an organization-wide workflow on it over two years, and now faces a renewal at $18 per seat per month confronts a real calculation: pay the new rate, or absorb the migration cost. The migration cost is often large enough that the price increase wins.

Feature paywalls move in one direction. Features available on a given tier at adoption are not guaranteed to remain there. The roadmap description from three years ago that listed a capability as "included on Professional" may not match the current pricing page. Users who built workflows on features they understood to be included sometimes discover those features now require the next tier up.

The per-seat model creates structural pressure as teams grow. A ten-person team's annual SaaS bill is manageable. A fifty-person team's bill at the same per-seat rate is five times larger, and by the time a company has reached fifty people using a platform, the switching cost has compounded accordingly. Teams that grow into enterprise sizes often find that per-seat pricing which was attractive at ten seats has become a significant budget line that IT attempts to renegotiate — often without success, because leverage has shifted.

Mid-contract price changes are less common but not rare. Platform economics shift, investor pressure changes, the competitive landscape evolves. Users who committed workflows and data to a platform signed a contract of sorts — and then discovered the other party's interpretation of that contract differed from their own.

The lock-in compounds when teams use multiple SaaS products that integrate with each other. A project management platform connected to a communication tool, a file storage service, a time tracker, and a billing system creates a dependency web where each integration raises the switching cost of every other platform. When one vendor raises prices, the team isn't evaluating that product in isolation — they're evaluating the cost of unwinding a set of integrations built over years. Integration ecosystems serve the vendor's retention objectives as reliably as they serve the user's productivity. The web of dependencies isn't a side effect of the SaaS model — it's a feature of it, from the vendor's perspective.

---

## Who Pays the Most

The organizations most exposed to all five failure modes share a characteristic: they have the least structural leverage to address any of them.

A large enterprise with a skilled procurement and IT organization can negotiate. Data portability clauses, SLAs with financial penalties, escrow provisions for source code and data — these are available to buyers with enough revenue to make the vendor's legal team engage seriously. When the vendor gets acquired, the enterprise has attorneys who can enforce contract terms or negotiate exit conditions.

Small and medium-sized professional service firms don't have this leverage. The legal practice with eight attorneys signs up through a website. The medical group with four physicians clicks through a terms of service that nobody reads. The construction firm with two project managers pays by credit card. Their vendor contract is the standard terms of service, unmodified. They have no SLA. They have no escrow. They have no explicit data portability requirement. If the vendor changes pricing, those users have no mechanism to object. If the vendor shuts down, they have whatever the shutdown announcement says they have.

These are also the organizations where software failures have direct professional consequences rather than just operational inconvenience. The construction PM missing a bid deadline loses the bid — and damages the relationship with the client. The legal practice unable to access case files has a professional responsibility exposure. The medical practice that can't retrieve patient records has regulatory risk. The stakes of availability are not abstract.

And these organizations are the primary addressable market for the products most likely to carry the SaaS risks described above. The large enterprise with the IT team and the procurement counsel is using enterprise-licensed software with negotiated protections. The eight-attorney law firm is using the same product tier as the freelancer, under the same standard terms, with the same structural exposure to every failure mode described in this chapter.

This is not a coincidence. The SaaS bundle packages its desirable and undesirable properties together in a way that affects smaller buyers more severely, because smaller buyers have less ability to negotiate the undesirable half away.

The regulatory dimension compounds this asymmetry. A legal practice storing confidential client communications in a vendor's cloud carries a professional duty to understand where that data lives and who can access it. A medical practice has HIPAA obligations. A construction firm with government contracts may have data residency requirements tied to those contracts. For large enterprises, these obligations get negotiated into vendor agreements with audit rights and data processing addenda. For the eight-attorney firm, the compliance answer is the vendor's standard privacy policy — a document written to protect the vendor, not the client.

The jurisdictional scope of this compliance argument is wider than US-centric discussions typically acknowledge. The EU's GDPR established that personal data of EU residents requires lawful basis for processing and affirmative data subject rights. The 2020 Schrems II ruling by the EU Court of Justice invalidated the Privacy Shield framework and constrained transfers of EU personal data to US cloud providers without adequate supplemental safeguards — a ruling that made local-first data residency a direct compliance mechanism, not merely an architectural preference. India's Digital Personal Data Protection Act 2023 (DPDP) imposes consent and localization requirements on personal data of Indian residents. The UAE Data Protection Law 2022 requires explicit consent for cross-border data transfers. Brazil's LGPD, South Africa's Protection of Personal Information Act (POPIA, 2021), Nigeria's NDPR enforced by the NDPC, and Japan's PIPA each impose data residency, consent, and access-rights obligations that constrain where personal data may be processed and stored. In each of these jurisdictions, an architecture where data lives on the user's own hardware — not in a vendor's cloud region — is not merely preferred. In many configurations, it is the architecture that makes compliance tractable. The book's architecture is frequently a legal requirement before it is an architectural choice.

---

## Why Users Have Accepted This

Until recently, they didn't have a choice.

Real-time collaboration requires that all parties see consistent state when they make concurrent changes. In 2008, the most practical way to guarantee this was a central server both parties could read from and write to simultaneously. Every other approach — emailing files, shared drives, version control — introduced either merge conflicts requiring manual resolution or coordination overhead requiring explicit locking. Real-time collaboration solved both problems by making divergence impossible: one copy, everyone editing the same one.

Multi-device sync requires an authoritative copy that all devices agree on. When the cloud holds the authoritative copy, sync is the cloud pushing updates to each device. Without a cloud authority, devices have to figure out among themselves which version is current — and the consumer-grade protocols for resolving concurrent edits across devices reliably, at scale, without requiring user intervention, didn't exist. Merging concurrent edits deterministically, without a server to adjudicate conflicts, was an unsolved problem for end-user software.

Zero maintenance requires that someone else manage the infrastructure. The alternative is the user managing it, which requires IT capability that most small organizations don't have and don't want to develop. The comparison to self-hosted software circa 2005 is instructive: a self-hosted email server, a self-hosted project tracker, a self-hosted document collaboration platform — all theoretically possible, all practically demanding enough that most organizations paid someone else to handle it.

The dependencies looked structural because they were structural. The technology for delivering these properties without vendor infrastructure either didn't exist or wasn't mature enough to deploy without specialized expertise. CRDTs were academic research with a handful of experimental implementations. Gossip protocols ran inside distributed databases; nobody was building them into end-user applications. Container runtimes existed for server workloads; the packaged, embeddable, consumer-invisible form that makes Docker Desktop run silently on your laptop hadn't been built.

Users accepted the SaaS bundle not because they preferred the conditions on the second half but because the technology of the time made those conditions appear to be the cost of the first half. They weren't accepting a bargain so much as acknowledging a constraint.

The constraint has been removed.

The evidence is commercial, not theoretical. Actual Budget delivers full personal finance capability on local storage; its sync service is optional. Linear's sync engine runs on a local SQLite replica; the cloud is already demoted to a relay peer. These products demonstrate that the desirable half of the SaaS bundle — collaboration, sync, responsive UI — doesn't require vendor data custody to function. Users who have worked with software built on these foundations have a reference point: they know what it feels like when software keeps running after the internet goes out. The acceptance erodes when the alternative is observable, not theoretical.

---

## The Dependency That Looks Inevitable

Three specific technology shifts made the structural necessity of the SaaS bundle removable.

**CRDTs in production.** Conflict-free replicated data types provide an algorithm for merging concurrent edits without a central coordinator. Two users edit the same document offline, reconnect, and see a correct merged result — no data loss, no manual conflict resolution, no authority required to adjudicate. This is not theoretical: it's the mechanism Linear uses for simultaneous task edits, the mechanism behind Automerge and Yjs and the growing family of production CRDT libraries, and the basis for Actual Budget's fully local data model. Figma uses CRDTs for multiplayer cursor coordination, but Figma's data resides on Figma's servers — it is not a data-sovereignty architecture. The data-sovereignty proof points are Linear (local SQLite replica, sync to cloud) and Actual Budget (fully local SQLite, cloud sync optional): both keep authoritative state on the device. The central server that served as the authority for "what's the current version of this document" is replaceable by a mathematically guaranteed merge that doesn't require an authority.

**Gossip protocols at the edge.** Leaderless replication — gossip algorithms, anti-entropy sync, vector clocks — allows nodes to synchronize state without a master. Every peer can accept writes; every peer eventually converges to the same state. Cassandra and DynamoDB operate at planetary scale using these mechanisms. On a five-person team with five workstations, the same protocols work without any cloud relay at all: when the machines are on the same network, they sync directly. When they're not, they sync through any reachable relay, including a user-controlled one.

**The local service pattern.** Container runtimes, and specifically the background-service model that tools like Docker Desktop and Tailscale established, made it normal for complex multi-service software to run silently on a user's machine without requiring the user to manage it. The pattern of a native UI shell connecting to a locally running application server is not novel — VS Code does it with language servers, 1Password does it with its desktop helper, Tailscale does it with its mesh daemon. The user experience is indistinguishable from a cloud application. The infrastructure is local.

These three shifts happened independently, solving problems that had nothing to do with the SaaS bundle. CRDTs were a distributed systems research problem. Gossip protocols were a database scaling problem. Container runtimes were a server deployment problem. The consequence — that the technical necessity of the SaaS bundle is now removable — followed from solutions to those other problems. The architecture has real costs: operational complexity, key management, schema migration across independent nodes, and upgrade coordination replace vendor dependency. The rest of this book addresses each of those costs directly.

Marcus's scenario — deadline-critical work held hostage by infrastructure he doesn't control — is the failure mode this architecture addresses first. His data was never gone. It was inaccessible because the software's design placed it somewhere he couldn't reach. The rest of this book specifies a design where that distinction doesn't exist.

There is an advantage to this architecture that rarely appears in technical comparisons: it is accessible. Assistive technology users — screen readers, switch access devices, voice control software — depend on applications that remain responsive. When a SaaS application is in a connectivity failure state, the AT user does not experience degraded performance; they experience complete access failure: the screen reader announces a failed load, voice control has no form fields to target, the application has stopped responding. A local-first architecture, where application state lives on the device, keeps the application responsive regardless of network state. This is an accessibility property the SaaS model cannot structurally offer.

What remains is the reference architecture: how to assemble these proven components into a coherent, deployable architecture that behaves like a cloud application, passes enterprise security review, and treats user data ownership as a structural guarantee rather than a contractual one.

The building blocks are production-proven. What remains is the specific assembly that produces a node — not a smarter cache, not a thicker client, but a first-class local peer. Chapter 2 identifies exactly what that requires and where the existing work stops short. Chapter 3 draws the node.
