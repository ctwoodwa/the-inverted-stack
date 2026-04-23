# Chapter 1 — When SaaS Fights Reality

<!-- icm/draft -->
<!-- Target: ~4,500 words -->
<!-- Source: v13 §3, v13 Executive Summary, v13 §14.1, v13 §20.4, v5 §1 -->

---

Marcus is the project manager on a $4.2 million commercial renovation. His general contractor's bid is due at 5 PM — the owner group has a board meeting at 6. The project management platform his firm runs on has been down since 11 AM. It's now 2 PM.

The data isn't gone. It's on servers in Virginia, or Oregon, or wherever the cloud region is. The labor breakdown, the subcontractor bids, the change order history, the payment schedule — all of it exists. It's just not accessible because the service is experiencing an outage affecting "less than 1% of users," which, from Marcus's perspective, means 100% of the users who matter right now.

His options: reconstruct what he can from the email trail. Export a stale PDF from before the platform went down. Ask his client to extend the deadline, which reflects poorly on his firm.

This is not a planning failure. He planned correctly. He had his data, his team used the software, everything was in order. The failure is structural: his data lives on infrastructure he doesn't control, and when that infrastructure goes offline, his capability goes with it.

---

## The Bundle Nobody Agreed To

The SaaS deal goes like this: give us your data, keep it on our servers, pay us every month, and in exchange you get real-time collaboration, multi-device access, and zero maintenance. Most users said yes without fully registering the second half. The first half was the product. The second half was the terms.

The three desirable properties are real. Real-time collaboration is transformative — two people editing the same document, watching changes appear, not emailing attachments back and forth. Multi-device access means your work is on your phone when you need it at the airport. Zero maintenance means IT doesn't manage a server; the vendor handles it. These are genuine improvements over what preceded them.

The three conditions on the other side of the bundle get less attention. Your data lives on vendor infrastructure, which means the vendor can see it, lose it, sell the company that holds it, or turn the service off. Pricing is at the vendor's discretion — the rate when you adopted the software is not a commitment, it's a starting point. Service continuity is contingent on the vendor's survival: if the company gets acquired, runs out of money, or decides to sunset the product, your software stops working when theirs does.

Users accepted these conditions because the three desirable properties appeared to *require* them. Real-time collaboration required a central server both parties could talk to. Multi-device sync required a cloud that acted as the authoritative copy. Zero maintenance required that the vendor control the infrastructure. The package looked indivisible because, with the technology of 2010, it largely was.

That's no longer true. The rest of this chapter is about what it costs before we reach that — and who pays the most.

---

## Five Ways SaaS Breaks in the Field

### The Outage That Takes Your Work With It

Cloud platforms publish availability metrics. Major SaaS providers report 99.9% uptime — roughly 8.7 hours of downtime per year. For a single user, those hours distribute across the year and rarely land at a bad moment. For a team of ten, at any given moment someone is more likely to be in the middle of something time-sensitive. Marcus's 8.7 hours found him on a bid deadline.

The outage that gets published is the one the vendor is willing to call an outage. The incidents that affect partial regions, specific features, or specific customer cohorts often appear as "degraded performance" rather than a declared incident. From the affected user's side, degraded performance means the site loads but submissions fail silently, changes save and then revert, or search returns stale results. This is harder to work around than a clean outage, because it's not obvious that the problem is the platform rather than the user's own actions.

What makes outage risk particularly asymmetric is that it falls hardest on the moments that matter most. High-stakes work — deadline submissions, live customer sessions, critical handoffs — tends to involve intensive platform use, which means it's more exposed to performance degradation under load. And the work that can least tolerate delay tends to be the work with external dependencies: bids due to clients, documents due to regulators, reports due to boards. These are not moments where "try again in an hour" is an option.

The construction PM example is not unusual for the industry. Construction project management is deadline-driven by definition. A subcontractor bid has a submission deadline that is not negotiable after the fact. A change order authorization has a response window tied to contract terms. A safety inspection log has a regulatory timestamp requirement. When any of these processes depends on cloud infrastructure being available exactly when needed, the infrastructure is a single point of failure in a workflow that cannot tolerate one.

Availability statistics miss a compounding factor: the concentration of cloud hosting means that failures cascade across unrelated products simultaneously. An AWS us-east-1 availability zone failure affects every product hosted there — project management tools, document collaboration platforms, file storage services, communication tools — at the same moment. A single incident becomes an industry-wide incident for everyone whose vendor chose the same region. Users who experience a simultaneous failure across multiple tools they rely on don't find redundancy in having adopted multiple platforms; they find that all their fallback options went down at the same time.

### The Vendor That Disappears

In 2015, Sunrise Calendar had approximately 1.5 million users and was widely considered the best third-party calendar app for iOS. Microsoft acquired it in 2015 and shut it down in September 2016. Users received a few weeks' notice. The data was exportable — in a format that no other calendar app read natively, requiring manual remapping of categories and recurrence rules.

Sunrise wasn't exceptional. It was typical of how software products end.

The mechanism changes — acquisition, runway exhaustion, a strategic pivot, the founder taking a job somewhere larger — but the pattern is consistent. The product goes dark. Users who built their workflows around it are left with whatever they managed to export before the deadline.

Quip, the collaborative document tool acquired by Salesforce, was folded into the Salesforce platform and ultimately deprioritized. Groups that used it for internal documentation found their investment in the tool's specific organizational structure — the way Quip handled threaded comments, the sidebar navigation model, the direct link between documents and spreadsheets — essentially worthless on migration, because no competing tool was designed to import and replicate it.

The data export problem deserves specific attention. When a vendor announces shutdown, it typically offers an export function. What that export contains, what format it uses, and whether any other software can actually consume it are highly variable. For calendar data, iCal is reasonably standard. For project management data, vendors typically export a CSV of the task list — without the comments, without the attachment history, without the relationship structure that made the tool useful. For document collaboration, most platforms offer a PDF export, which preserves the appearance but none of the editability.

The legal firm whose vendor gets acquired faces this directly. They adopted the software, trained staff, integrated it with billing and document management workflows, and accumulated years of matter history. Now they evaluate whether to migrate to the acquirer's competing product under the acquirer's pricing, or start over with a third party, reconstructing what they can from a flat CSV and a folder of PDFs.

This risk has a name that undersells it. "Vendor shutdown" sounds like a rare catastrophe. It's routine. Thousands of SaaS products shut down every year. Most are small enough that their shutdowns don't make news. Their users find out through an email or a banner in the app. The shutdowns that do make news — Evernote's degraded state following years of ownership changes, Google Reader's abrupt termination in 2013 despite millions of active users, the steady stream of products acquired into enterprise platforms and starved of investment — are notable primarily because of the scale of the disruption, not because the pattern is unusual.

### The Connectivity That Wasn't There

Not everyone's internet is always on. This sounds obvious. It is consistently underweighted in the architecture of software sold to the industries where it most frequently fails.

Construction sites operate at the edge of mobile coverage. A superintendent in a concrete frame building can't get a signal three floors underground. Rural professional service firms — accounting firms in small towns, medical practices in counties with limited broadband, legal practices in areas where fiber hasn't reached — operate on connectivity that drops daily and fails entirely during weather events. Hospital clinical environments include zones where mobile devices are restricted near sensitive equipment. Air-gapped facilities — manufacturing, defense, government — cannot connect to any external network at all as a policy requirement.

For these users, offline capability is not a feature request. It is the baseline requirement.

The SaaS vendor's marketing page says "works on mobile," which is true when there's a signal. It doesn't say "works when there isn't one," because the centralized architecture makes that impossible without fundamental redesign. The application is a thin client rendering views from a remote database. Remove the remote database and the client has nothing to render.

Most SaaS platforms offer some form of "offline mode." What this means in practice is usually: a read-only cache of recently viewed data, with form submissions that queue locally and attempt to upload when connectivity returns — with uncertain success rates and no visibility into what actually synced. You can view the last-synced version of a document. You cannot create new records, cannot run reports, cannot access data you haven't recently viewed, and cannot have any confidence that what you submitted offline actually made it to the server.

The field operations manager who needs to log a safety inspection at 7 AM on a construction site before the crew starts work has a few options when the SaaS is unreachable: write it in a notebook and transcribe it later (with all the transcription errors that introduces), use the app's read-only offline mode and hope the form submission queues correctly, or skip the log and fill it in from memory when back in the office. All three options introduce risk. None of them should be necessary. The software should work on a construction site because that's where the work happens.

### The Data You Can't Get Back

Your vendor's terms of service say your data is yours. They're often technically correct — the vendor does not claim ownership of the content you create. What the terms of service don't address is *accessibility*.

Data that you own but cannot retrieve is data you don't have.

The mechanisms by which data becomes inaccessible while technically "belonging" to you are well-documented:

**Export rate limits.** Many platforms allow data export but rate-limit the export API to prevent bulk data extraction. A legal firm with ten years of matter history attempting a bulk export may find that retrieving their own data at the permitted rate takes weeks. During that window, they remain dependent on the vendor's infrastructure to operate — which is, not coincidentally, exactly the position the vendor prefers them to be in.

**Proprietary formats.** The export is available but in a format only the vendor's tools read well. Attachments export without their metadata. Comment threads export as flat text without threading structure. Custom fields export as raw column headers without the semantic context that made them useful. The data is present; the information it represented is partially lost.

**Feature-gated access.** Some platforms require paid subscriptions to access export features, or limit export to higher pricing tiers. Users on free or lower tiers discover that their data is portable only as long as they keep paying — which means it isn't portable at all.

**Account closure timing.** When a user cancels a subscription, access typically ends when the billing period ends. A user who cancels on the first of the month with a billing cycle that ends on the fifteenth has fifteen days to export before the account closes. Miss that window — because you changed jobs, because the cancellation notice didn't clearly state the deadline — and the data may be gone.

None of these are edge cases. They are the routine operational parameters of vendor-managed data. Users encounter them not as occasional anomalies but as the standard cost of cloud data custody.

### The Price That Changes After You've Committed

Switching costs in SaaS are high because users build workflows around software. Training, integrations, historical data, learned patterns — these represent real investments. Vendors know this. Pricing structures often reflect it.

The pattern is predictable. Pricing is competitive during the acquisition phase, when vendors are winning customers and competing on features and price. After adoption, when the switching cost is real and rising, pricing pressure relaxes. A company that adopted a project management platform at $8 per seat per month, built an organization-wide workflow on it over two years, and now faces a renewal at $18 per seat per month confronts a real calculation: pay the new rate, or absorb the migration cost. The migration cost is often large enough that the price increase wins.

Feature paywalls move in one direction. Features available on a given tier at adoption are not guaranteed to remain there. The roadmap description from three years ago that listed a capability as "included on Professional" may not match the current pricing page. Users who built workflows on features they understood to be included sometimes discover those features now require the next tier up.

The per-seat model creates structural pressure as teams grow. A ten-person team's annual SaaS bill is manageable. A fifty-person team's bill at the same per-seat rate is five times larger, and by the time a company has reached fifty people using a platform, the switching cost has compounded accordingly. Teams that grow into enterprise sizes often find that per-seat pricing which was attractive at ten seats has become a significant budget line that IT attempts to renegotiate — often without success, because leverage has shifted.

Mid-contract price changes are less common but not rare. Platform economics shift, investor pressure changes, the competitive landscape evolves. Users who committed workflows and data to a platform signed a contract of sorts — and then discovered the other party's interpretation of that contract differed from their own.

---

## Who Pays the Most

The organizations most exposed to all five failure modes share a characteristic: they have the least structural leverage to address any of them.

A large enterprise with a skilled procurement and IT organization can negotiate. Data portability clauses, SLAs with financial penalties, escrow provisions for source code and data — these are available to buyers with enough revenue to make the vendor's legal team engage seriously. When the vendor gets acquired, the enterprise has attorneys who can enforce contract terms or negotiate exit conditions.

Small and medium-sized professional service firms don't have this leverage. The legal practice with eight attorneys signs up through a website. The medical group with four physicians clicks through a terms of service that nobody reads. The construction firm with two project managers pays by credit card. Their vendor contract is the standard terms of service, unmodified. They have no SLA. They have no escrow. They have no explicit data portability requirement. If the vendor changes pricing, those users have no mechanism to object. If the vendor shuts down, they have whatever the shutdown announcement says they have.

These are also the organizations where software failures have direct professional consequences rather than just operational inconvenience. The construction PM missing a bid deadline loses the bid — and potentially the relationship with the client. The legal practice unable to access case files has a professional responsibility exposure. The medical practice that can't retrieve patient records has regulatory risk. The stakes of availability are not abstract.

And these organizations are the primary addressable market for the products most likely to carry the SaaS risks described above. The large enterprise with the IT team and the procurement counsel is using enterprise-licensed software with negotiated protections. The eight-attorney law firm is using the same product tier as the freelancer, under the same standard terms, with the same structural exposure to every failure mode described in this chapter.

This is not a coincidence. The SaaS bundle packages its desirable and undesirable properties together in a way that affects smaller buyers more severely, because smaller buyers have less ability to negotiate the undesirable half away.

---

## Why Users Have Accepted This

Until recently, they didn't have a choice.

Real-time collaboration requires that all parties see consistent state when they make concurrent changes. In 2008, the most practical way to guarantee this was a central server both parties could read from and write to simultaneously. Every other approach — emailing files, shared drives, version control — introduced either merge conflicts requiring manual resolution or coordination overhead requiring explicit locking. Real-time collaboration solved both problems by making divergence impossible: one copy, everyone editing the same one.

Multi-device sync requires an authoritative copy that all devices agree on. When the cloud holds the authoritative copy, sync is the cloud pushing updates to each device. Without a cloud authority, devices have to figure out among themselves which version is current — and the consumer-grade protocols for resolving concurrent edits across devices reliably, at scale, without requiring user intervention, didn't exist.

Zero maintenance requires that someone else manage the infrastructure. The alternative is the user managing it, which requires IT capability that most small organizations don't have and don't want to develop. The comparison to self-hosted software circa 2005 is instructive: a self-hosted email server, a self-hosted project tracker, a self-hosted document collaboration platform — all theoretically possible, all practically demanding enough that most organizations paid someone else to handle it.

The dependencies looked structural because they were structural. The technology for delivering these properties without vendor infrastructure either didn't exist or wasn't mature enough to deploy without specialized expertise. CRDTs were academic research with a handful of experimental implementations. Gossip protocols ran inside distributed databases; nobody was building them into end-user applications. Container runtimes existed for server workloads; the packaged, embeddable, consumer-invisible form that makes Docker Desktop run silently on your laptop hadn't been built.

Users accepted the SaaS bundle not because they preferred the conditions on the second half but because the technology of the time made those conditions appear to be the cost of the first half. They weren't accepting a bargain so much as acknowledging a constraint.

The constraint has been removed.

---

## The Dependency That Looks Inevitable

Three specific technology shifts made the structural necessity of the SaaS bundle removable.

**CRDTs in production.** Conflict-free replicated data types provide an algorithm for merging concurrent edits without a central coordinator. Two users edit the same document offline, reconnect, and see a correct merged result — no data loss, no manual conflict resolution, no authority required to adjudicate. This is not theoretical: it's the mechanism Linear uses for simultaneous task edits, the mechanism Figma uses for concurrent design work, the mechanism behind Automerge and Yjs and the growing family of production CRDT libraries. The central server that served as the authority for "what's the current version of this document" is replaceable by a mathematically guaranteed merge that doesn't require an authority.

**Gossip protocols at the edge.** Leaderless replication — gossip algorithms, anti-entropy sync, vector clocks — allows nodes to synchronize state without a master. Every peer can accept writes; every peer eventually converges to the same state. Cassandra and DynamoDB operate at planetary scale using these mechanisms. On a five-person team with five workstations, the same protocols work without any cloud relay at all: when the machines are on the same network, they sync directly. When they're not, they sync through any reachable relay, including a user-controlled one.

**The local service pattern.** Container runtimes, and specifically the background-service model that tools like Docker Desktop and Tailscale established, made it normal for complex multi-service software to run silently on a user's machine without requiring the user to manage it. The pattern of a native UI shell connecting to a locally running application server is not novel — VS Code does it with language servers, 1Password does it with its desktop helper, Tailscale does it with its mesh daemon. The user experience is indistinguishable from a cloud application. The infrastructure is local.

These three shifts happened independently, solving problems that had nothing to do with the SaaS bundle. CRDTs were a distributed systems research problem. Gossip protocols were a database scaling problem. Container runtimes were a server deployment problem. The consequence — that the technical necessity of the SaaS bundle is now removable — followed from solutions to those other problems.

What remains is the blueprint: how to assemble these proven components into a coherent, deployable architecture that behaves like a cloud application, passes enterprise security review, and treats user data ownership as a structural guarantee rather than a contractual one.

Chapter 2 maps what the local-first community has already built with these tools, where those efforts stop short of a complete answer, and why the gap requires a full node rather than a smarter cache. Chapter 3 shows what the full node looks like.
