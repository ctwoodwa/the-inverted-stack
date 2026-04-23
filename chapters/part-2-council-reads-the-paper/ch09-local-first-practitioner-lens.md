# Chapter 9 — The Local-First Practitioner Lens

<!-- icm/draft -->
<!-- Target: ~3,500 words -->
<!-- Source: R1 Ferreira, R2 Ferreira, v13 §13 -->

---

## Who Is Tomás Ferreira

Tomás Ferreira has shipped code to the Automerge repository for three years. Before that, he built a production local-first application for a small legal firm — document collaboration, no server required — and watched the users try to restore their data from a broken laptop. The restore took four hours because the backup was a folder on Dropbox that had not synced correctly. He built a second application, this time with a proper backup strategy, and watched a different user delete their container accidentally and discover that no backup meant no data.

He is not idealistic about local-first software. He is familiar with where it breaks.

His lens on any local-first architecture proposal is not whether it upholds the principles — the principles are table stakes. His questions are operational: What happens when the user's only device dies? What happens when both peers are behind carrier-grade NAT and the relay is down? What happens when a user wants to leave and take their data somewhere else? He has sat across from non-technical users who encountered all three of these scenarios. He knows what their faces look like.

When Ferreira reviewed the architecture paper in Round 1, he brought that operational history with him. He commended the places the paper got right. He blocked it on the place the paper got exactly wrong.

---

## Act 1: Round 1 — The Data Portability Failure

### What Ferreira Commended

Ferreira does not commend things he does not mean. His Round 1 scorecard opened with a score of 9 out of 10 for CRDT library selection — Yjs for JavaScript environments and Loro for Rust-native performance are both correct choices, well-suited to their respective contexts, and the three-tier resolution model that governs when to apply CRDT merge versus user-arbitrated resolution is the most honest treatment of CRDT applicability he had encountered in any architecture proposal outside published academic literature.

The multi-device onboarding flow — install, scan a QR code, sync in the background — addressed the bootstrapping problem that breaks most naive local-first architectures. The usual failure mode is a chicken-and-egg: to join a workspace, the new device needs credentials, but credentials require an existing peer, and a peer requires the network to be available at exactly the right moment. The QR-based attestation bundle transfers everything the new node needs to authenticate and begin gossip in a single out-of-band step. That is the right design.

He also commended the container cold-start solution. One of the places local-first desktop applications fall apart is the delay between launch and ready for data. A Podman container starting from scratch on first open creates a pause that signals to users that something is wrong — that the software is not, in fact, running locally, but is somehow waiting for something remote. The architecture's answer — a persistent background service that keeps the container running, fronted by a health-check gate that holds the UI until the daemon is ready — is pragmatically correct. It hides the implementation reality without lying about it.

Alignment with the Kleppmann et al. local-first ideals [1] scored an 8 out of 10. The paper understood the ideals and implemented most of them faithfully. The Ink and Switch essays on Pushpin and Backchat were not cited, which left the paper vulnerable to community criticism — the local-first community notices when practitioners ignore prior art. But that is a condition, not a block.

Community governance scored a 5 out of 10. An MIT or Apache 2 license is stated; who controls the roadmap, who approves breaking changes, what the contribution model looks like — none of that is specified. The local-first community has watched too many promising projects fork or stall because governance was not designed before it was needed. That is a condition too.

Then Ferreira got to data portability.

### The Blocking Issue: No Export Path

The paper's thesis is data ownership. The paper's proof is the local node: because the data lives on the user's machine, in a local encrypted database, the user owns it in a structural sense. The vendor cannot take it away. The SaaS subscription cannot gate access to it. The architecture enforces the ownership as a design invariant, not a contractual promise.

Ferreira agreed with the thesis. He blocked on the execution.

If a user wants to leave the application — switch to a different tool, transfer their data to a new platform, or simply preserve their records in a format that will still be readable in twenty years — how do they do it? The paper specified the backup target: rclone with a user-controlled object storage account. But rclone backup preserves the internal data format. It does not export the data in a form any other application can read. It does not give the user a JSON file of their records, a CSV of their tabular data, or a folder of Markdown documents. It gives them a copy of the encrypted local database, readable only by the application that created it.

This is a philosophical contradiction that Ferreira named precisely: a paper arguing for data ownership that does not specify how a user exports their data in a durable, application-independent format does not actually deliver data ownership. It delivers data custody under slightly better conditions.

The difference matters. A user who wants to move from this architecture to a different tool needs access to their data in a form the new tool can ingest. An application-independent export format — JSON for structured records, CSV for tabular data, Markdown for documents — satisfies that requirement. An internal backup format does not.

He also flagged the non-technical disaster recovery path as a condition rather than a second block. The architecture specified rclone backup to user-controlled object storage, which is correct. But the paper never walked through what a non-technical user actually does when their laptop dies and they need to restore. Step one: buy a new laptop. Step two: install the application. Step three: what? The architecture knew the answer but never wrote it down.

The symmetric NAT scenario was a third condition: when two peers are both behind carrier-grade NAT and the relay is unavailable, direct communication is impossible. The paper's peer discovery section described mDNS for LAN discovery and relay for WAN — but it did not acknowledge that carrier-grade NAT can defeat both if the relay is down. The failure mode exists. The paper did not document it.

### The BLOCK Verdict

Ferreira's domain average for Round 1 was 7.0 out of 10 — the scoring rubric would normally warrant a PROCEED WITH CONDITIONS. He issued PROCEED WITH CONDITIONS in his formal verdict, but with one item classified as a philosophical and practical blocker: the absent export path.

His verdict rationale was direct. The paper cannot argue for data ownership and omit the export button. Until the architecture specifies how a user retrieves their data in a form that does not require the original application to read it, the ownership claim is hollow. The underlying architecture is better than most. The specific gap is the most important one.

The paper returned to the author with the data portability issue as a blocking item alongside the five blocks raised by the other four council members. The revision would need to resolve all six before any member would begin a second review.

---

## What Changed Between Rounds

Four months passed between the Round 1 verdict and the Round 2 submission. The author addressed all six blocking issues in the paper's second version. Ferreira's three Round 1 conditions and his single blocking issue all received direct treatment.

The export path is now specified. One command produces a directory with three artifacts: a JSON file containing all user records in application-independent structure, a set of CSV files for every tabular data type, and a folder of Markdown documents for long-form content. No vendor cooperation required. No active subscription required. No internet connection needed. The command runs against the local node, reads from the local encrypted database, and writes to a path the user specifies. Any application that can ingest JSON or CSV can ingest the output.

The non-technical disaster recovery walkthrough now exists step by step. The scenario is a laptop destroyed beyond recovery — hardware failure, theft, fire. Step one: acquire a new laptop. Step two: install the application, which installs the container runtime and stack silently. Step three: when prompted, the user enters a recovery code generated during initial setup, or scans a QR code from a team member's device. Step four: the application prompts for the BYOC backup target — the Backblaze bucket, the S3 path, the rclone destination configured during original setup. Step five: full restore runs in the background. The user can work immediately on data their role includes in eager sync buckets; remaining records populate as the background sync completes. No technical knowledge required at any step. The recovery code or team-member QR scan substitutes for the original device's attestation bundle.

The symmetric NAT failure mode is now documented honestly. When both peers are behind carrier-grade NAT and the relay is down, direct peer-to-peer communication is impossible. The paper does not paper over this. It names the condition: carrier-grade NAT plus relay outage produces local-only mode for both parties. The relay is the resolution — when the relay is up, it handles NAT traversal. For organizations where relay availability is itself a concern, self-hosting a relay instance on a cloud VM with a public IP provides a fallback that eliminates the symmetric NAT problem by giving both peers a fixed reachable endpoint.

Community governance now has a three-stage model: the author serves as BDFL for version 1, making unilateral architectural decisions with a published rationale for each breaking change. A contributor council of five elected members takes over for version 2, with a defined voting process for protocol changes. A foundation structure for version 3, modeled on established open-source infrastructure projects, provides independent governance once the community has grown enough to sustain it.

---

## Act 2: Round 2 — An Unconditional Pass

### Seven Ideals Compliance: The Full Checklist

Ferreira opened his Round 2 review by applying the Kleppmann et al. checklist [1] directly. He had done this in Round 1 and found gaps. In Round 2, he did it again and found none.

The seven local-first ideals, checked against the revised architecture:

**No spinners, no waiting.** The local node holds the authoritative data copy. The UI reads from local storage. There are no round-trips to a remote server for reads. Instant. Checked.

**Your work is not trapped on one device.** CRDT sync across peers ensures that data written on one device propagates to all authorized peers. The gossip daemon handles the distribution. Checked.

**The network is optional.** The architecture is explicitly offline-first. The node operates at full fidelity without network connectivity. Degraded UX modes apply only to CP-class data requiring freshness guarantees. Checked.

**Seamless collaboration with your colleagues.** CRDT merge handles concurrent edits without coordination. The conflict inbox and bulk resolution UX surfaces the edge cases that require human judgment. Checked.

**The long now.** The compliance CRDT tier with no garbage collection preserves the complete operation history. Records in this tier cannot be lost to compaction. Long-term archival formats are addressed. Checked.

**Security and privacy by default.** Subscription scoping at the sync daemon layer enforces data minimization at the protocol layer — nodes receive only the data their role authorizes. End-to-end encryption means the relay handles ciphertext only. Checked.

**You retain ultimate ownership and control.** BYOC backup to user-controlled object storage. AGPLv3 license. Self-hostable relay. Plain-file export. The ownership is structural, not contractual, and the export path now makes it operationally real. Checked.

This is the first version of the paper where Ferreira could work through the checklist without pausing. All seven ideals satisfied, without reservation. Score: 10 out of 10.

### The Zero-State First-Run Problem

With the blocking issue cleared and the checklist passed, Ferreira turned to what the revision had not addressed.

The UX section of the second paper substantially improved on Round 1. The sync status indicator design is correct — three persistent but unobtrusive indicators in the status bar, escalating from silent to informative to persistent-banner as conditions degrade. The conflict resolution UX addresses the most common usability failure in collaborative local-first applications: the overwhelming, undifferentiated list of conflicts that most systems present when two offline nodes reconnect. Grouping by record type and cause, auto-resolving the cases where predefined rules clearly apply, and offering resolve-all-similar for everything else brings the conflict inbox from anxiety-inducing to manageable.

The gap Ferreira identified as the primary 30-day abandonment risk is the zero-state first-run experience: what a brand-new user sees after installation, with no prior data and no existing peers.

The paper describes multi-device pairing — what happens when a user adds a second device to an existing workspace. It describes team onboarding — what happens when a user joins an existing team. What it does not describe is what a single user, installing the application for the first time, with no prior data and no colleague to scan a QR code from, actually sees.

This is where most users leave. Not when the sync breaks. Not when a conflict surfaces. At the beginning, when the screen is empty and the application has no obvious first action. A brand-new user who installs the application, opens it, and sees a blank state without clear guidance for the first thirty seconds is a user who closes it. Not because the architecture failed — because the first-run experience gave them no foothold. Ferreira has watched this happen with promising local-first software repeatedly. The architecture is sound; the opening screen is a dead end.

The paper should specify the zero-state experience explicitly: what the user sees, what action they take, how the application walks them from empty state to first project, first backup configuration, first invite. This is a product question, not an architecture question. But local-first architectures that do not answer it fail before the architecture gets a chance to prove itself.

### Backup and Recovery UX

The backup status model in the revised paper is correct. Three states — Protected, Attention, At Risk — with escalating visual treatment: subtle for Protected (users do not need to think about a working backup), amber badge for Attention (something needs configuration), persistent non-blocking banner for At Risk (data is in danger, but the user retains the ability to dismiss with acknowledgment). The dismissal with explicit acknowledgment respects user agency without hiding the problem.

Ferreira's remaining gap: the paper describes the backup status display. It does not describe the recovery experience with comparable care.

If a user's only device is destroyed and they initiate a restore from backup, what do they see? Does the application walk them through reconnecting to their backup target the same way it walked them through configuring it? Does the restore progress surface as a background sync indicator, using the same three-state model flipped into a restore context? Or does the user face a technical interface — a rclone path, a bucket URL — at exactly the moment when they are already stressed about lost work?

The architecture's backup infrastructure is solid. The recovery UX needs the same design attention. Your backup is protected earns user trust only if the restore works without calling support. The paper should describe the restore flow step by step, with the same non-technical framing used for the disaster recovery walkthrough added in the revision.

### Production Analogues

The architecture's analogues table in the revised paper cites Figma, Linear, Obsidian, and PowerSync. These are correct references — they demonstrate that each subsystem of the inverted stack has production validation somewhere. But they do not address the most relevant question for this chapter: has anyone shipped a complete local-first commercial application and made money doing it?

The answer is yes. Ferreira named it: Actual Budget.

Actual is a personal finance application. No server required. Data lives on the user's device. Syncing is optional and user-controlled. It charges a one-time purchase price, with an optional sync service subscription for users who want it. No per-seat pricing. No subscription required to access core features. The data is the user's by design, not by contract.

Actual validates two things simultaneously. First, the local-first model works at the product level — real users adopt it, pay for it, and use it daily. Second, the revenue model works without server-side data custody — one-time purchase plus optional convenience subscription produces enough revenue to sustain development. The closest commercial analogue to the inverted stack's business model is not a SaaS company. It is a desktop software company that added sync as a feature, not as a dependency.

Explicitly citing Actual Budget closes the implicit objection that no one has made this model work commercially. Someone has. The paper should say so.

### Implementation Drift Risk

Ferreira's final Round 2 observation is the one that will matter most in year two of production: the implementation drift problem.

The Kleppmann et al. paper [1] warns about this directly. Local-first architecture erodes under pressure. The erosion does not happen all at once — it happens one reasonable-sounding decision at a time. A team adds a server-side feature flag check. Then a server-side A/B test. Then product analytics to understand which features users use. Then a server-side model for something the local CRDT cannot handle efficiently. Each decision is defensible in isolation. Collectively, they re-centralize the architecture until the local node is a thick client again and the server is load-bearing.

The paper addresses this for business logic — it explicitly prohibits feature gating via server-side checks. What it does not address is the analytics and observability layer.

Modern product teams expect product analytics. They need to understand where users drop off, which features get used, what errors occur. In a local-first architecture, these signals cannot be collected server-side because there is no server-side session. The options are: opt-in telemetry that users explicitly enable; aggregate statistics piped through the relay, privacy-preserving and metadata-only; or no analytics at all.

The paper needs to specify which model it adopts and why. Not because the choice is architecturally complex — it is not — but because leaving it unspecified guarantees that the first product manager who wants a funnel report will add a server-side analytics endpoint as a quick addition. That quick addition is the first stone on the re-centralization path. Name the telemetry model now, before the first product analytics request arrives, and hold the line explicitly.

### Round 2 Verdict: PROCEED

Ferreira issued PROCEED in Round 2. No conditions required. No blocking issues.

His four observations — the zero-state first-run gap, the recovery UX, the Actual Budget omission, and the telemetry model — came with specific recommendations, not conditions. He filed them as non-blocking guidance, not as gates on implementation.

This matters for two reasons. Practically: it means the architecture can proceed to alpha implementation without resolving these items first. They are refinements, not failures. Structurally: Ferreira is the first council member, across both rounds, to issue an unconditional PROCEED. The enterprise architect issued PROCEED WITH CONDITIONS. The distributed systems researcher issued PROCEED WITH CONDITIONS. The security practitioner issued PROCEED WITH CONDITIONS. The product manager issued PROCEED WITH CONDITIONS. Ferreira, the practitioner who knows where the bodies are buried, looked at the revised architecture and found nothing that blocked it.

That verdict is not a formality. It is the hardest one to earn.

---

## The Principle: Data Ownership Requires the Export Button

Ferreira's Round 1 block reduced to a single principle: you cannot claim to give users ownership of their data if you do not give them a way to take it somewhere else.

The local node solves the access problem. Data on the user's machine is accessible when vendor servers are down. Data in the user's encrypted local database cannot be held hostage by a subscription paywall. The architecture eliminates the dependency on vendor infrastructure for the thing users care about most: getting to their own work.

But access is not portability. A user who wants to move to a different application, or preserve their data in a format that does not require this specific software to read, needs more than local storage. They need an export. JSON, CSV, Markdown — durable, application-independent formats that any competent software can ingest.

The export button is not a nice-to-have. It is the proof of the claim. An architecture that argues for data ownership and does not ship the export button is making a claim about values it has not actually implemented.

The same logic extends to disaster recovery. Your data is backed up is not sufficient. Your data can be restored by a non-technical user in under thirty minutes after a complete device failure is the claim that actually serves users. The architecture must describe the recovery path with the same care it describes the backup configuration — because a backup that cannot be restored is not a backup. It is a simulation of safety.

And the symmetric NAT failure mode is a concrete example of the honesty standard that separates production local-first software from demos. Every architecture has connectivity scenarios it cannot handle. The question is whether it names them or hides them. Carrier-grade NAT plus relay outage produces a failure mode where two peers cannot communicate. The right answer is not to claim the relay is so reliable this scenario never occurs. The right answer is to document the failure mode, name the conditions that produce it, and describe the fallback: a self-hosted relay on a machine with a public IP removes the symmetric NAT problem entirely, at the cost of the infrastructure burden the managed relay was designed to eliminate.

Honesty about failure modes is what distinguishes production local-first software from a persuasive demo. Ferreira has shipped production local-first software. He recognized the difference. He PROCEED'd when he saw it.

---

## References

[1] M. Kleppmann, A. Wiggins, P. van Hardenberg, and M. McGranaghan, "Local-first software: you own your data, in spite of the cloud," in *Proc. ACM SIGPLAN Int. Symp. New Ideas, New Paradigms, and Reflections on Programming and Software (Onward!)*, 2019, pp. 154-178.
