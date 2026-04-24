# Chapter 5 — The Enterprise Lens

<!-- icm/draft -->
<!-- Target: ~3,500 words -->
<!-- Source: R1 Voss, R2 Voss, v13 §16 -->

---

Dr. Marguerite Voss spent twenty-two years watching innovative software die in procurement. Not because the technology was wrong. Because the people who built it had never sat through an IT security review.

She has her own shorthand for the pattern: a team builds something genuinely useful, a forward-thinking IT manager shepherds it to a procurement committee, and the first question from legal or InfoSec kills it on the spot. Not whether it works — everyone in the room can see it works. The question is where the data goes when an endpoint is compromised. Or what is the incident response procedure. Or, most often, does this run as root.

Three times, she has watched a promising rollout collapse not because of technical failure but because the architecture had no answer to questions any enterprise IT department would ask on day one. The software teams in those cases were not incompetent. They had simply never been required to think about their product from the perspective of a CISO responsible for ten thousand managed endpoints.

That is her lens. Not whether this is interesting, but whether it will survive a real procurement committee. Not whether the security story sounds plausible, but whether IT can actually operate this, audit it, and respond when something goes wrong.

She read the paper expecting to find another promising pitch that would fail the first security review. What she found was more complicated.

---

## Act 1: Round 1 — The Architecture Fails Procurement

### What Voss Scored Well

Voss does not issue scores generously. When a section earns an eight from her, it has earned it in the way that a document earns it: by being specific, testable, and tied to actual policy.

The MDM integration earned that score. The paper names Intune, Jamf, and SCCM — not as examples or as supported-if-the-customer-configures-it, but as the specific management platforms the installation is designed for. More importantly, the paper describes the MDM compliance check at a specific point in the protocol: capability negotiation. Before a node joins the sync mesh and touches data, it must present a valid compliance attestation from the MDM platform. A node that fails the compliance check — because a managed policy has been violated, because the device has been flagged, because the certificate has expired — is rejected at the gate, not after it has already received data.

That is architecturally correct. Most MDM-compatible software validates compliance once at installation and then assumes the device remains compliant. The inverted stack validates it continuously at the point of access. Voss commended this directly: a compromised non-compliant node is rejected before it touches data, not after.

The SBOM commitment also earned strong marks. The architecture commits to publishing a Software Bill of Materials with each release — the list of every software component in the product, their versions, and their provenance. This is now a requirement for many enterprise procurement conversations and a baseline expectation for any software sold into regulated industries. The signed and notarized installer language — Apple Developer ID on macOS, Authenticode signing with App Control for Business (WDAC) integration on Windows — is procurement-ready. An IT administrator reading that section can translate it directly into a policy: this software can be added to the trusted-publisher list, deployed silently via Intune, and installed without user elevation.

The governance documentation quality was solid. SBOM plus signed installer plus MDM integration is a coherent governance story. For most local-first pitches, which typically arrive to procurement with a GitHub link and a request to run as administrator, this was a meaningful departure from the standard.

### The Blocking Issue: No Incident Response Procedure

Voss scored incident response and forensic capability at a six. That score came with a blocking issue.

The paper describes a CRDT audit trail. Every write operation is recorded in a tamper-evident append-only log; the sync daemon can reconstruct the full history of any record from its operation log. For forensic purposes, this is genuinely useful. For an incident response procedure, it is not a substitute.

The specific problem Voss raised: when an endpoint is compromised in an enterprise environment, the incident response process is not look at the audit trail. It is a defined sequence of steps: who is notified first, what artifacts are collected and from where, how the chain of custody is established for those artifacts, what the communication protocol is between IT, legal, and affected users, and who files the formal incident report with what regulators if required.

An audit trail tells you what happened. An incident response procedure tells you what to do about it.

The paper had the first and not the second. A CISO cannot hand an audit trail to a procurement committee as a response to the question about incident response procedure. They need a document that specifies the triggering events — what constitutes a reportable incident for this system — the artifact collection sequence, the chain of custody requirements for those artifacts, and the escalation path.

Without that document, the architecture cannot pass a security review in any enterprise that takes its compliance obligations seriously. A financial institution, a healthcare organization, a federal contractor, a law firm handling client confidential data — all of these require incident response procedures as a condition of deploying new software. The CRDT audit trail is a forensic asset. It is not a procedure.

Container update governance also drew scrutiny. The paper describes container images delivered through a registry — a standard and appropriate update mechanism. What it does not describe is how those updates are applied to a running production stack without downtime. Enterprise IT departments need to know whether updates require a maintenance window, whether they are applied automatically or manually triggered, and what the rollback procedure is if an update introduces a regression. None of those questions had answers.

Network policy compatibility scored a seven rather than the eight it could have earned. Relay traffic over port 443 is implied by the architecture — the relay is an HTTPS service — but the paper does not state it explicitly. More importantly, PAC file compatibility and behavior behind corporate proxies that perform TLS inspection are not addressed. Many enterprises route all outbound traffic through a proxy that terminates and re-establishes TLS connections. Software that does not respect proxy configuration fails invisibly in these environments. The paper needed to confirm that the sync daemon respects system proxy configuration and that relay connections route cleanly through PAC-file-configured proxies.

Compliance certification pathway was a six. SOC 2 Type II and ISO 27001 are not mentioned anywhere in the paper. For enterprise procurement, the absence of any mention of a compliance certification path — even a statement that the architecture is designed with SOC 2 controls in mind — is a gap that a security questionnaire will surface immediately.

### Round 1 Verdict: PROCEED — With One Hard Prerequisite

Voss scored a domain average of 7.1 out of 10 and issued PROCEED WITH CONDITIONS. Her formal verdict was not a block. But one item on her scorecard carried a weight that overrode the overall average in practical terms: without it, no enterprise security sign-off could follow.

The paper has no formal incident response procedure. For enterprise procurement, a CRDT audit trail is a forensic artifact, not a runbook. Before the architecture can be presented to a procurement committee in any enterprise environment with real compliance obligations, it must specify the triggering events that constitute a reportable incident for this system, the sequence of artifact collection steps, the chain of custody requirements for those artifacts, and the communication protocol — who notifies whom, in what order, within what timeframe.

This is not a theoretical gap. It is the specific question that kills procurement at the InfoSec review. Without it, the strongest governance story in the architecture is incomplete, because governance without incident response is not governance — it is a checklist that stops at the moment it matters most.

The three conditions Voss attached — explicit port 443 and TLS 1.3 with proxy compatibility, zero-downtime update path, and named SBOM toolchain — were lower-priority additions. They would not individually block the architecture. They were completeness items. The incident response gap was the one that had to be resolved before any security-phase review could proceed.

---

## What Changed Between Rounds

The revision addressed the blocking issue directly and without hedging.

The incident response runbook became a companion document to the architecture. It specifies four triggering events: suspected unauthorized access to a local node, detection of an unauthorized device in the sync mesh, a key compromise or suspected key exposure, and a data exfiltration event involving relay traffic. For each trigger, the runbook defines the artifact collection sequence — which logs to preserve, from which systems, in what order — and the chain of custody procedure for those artifacts. It specifies the escalation path: IT administrator notifies the CISO within one hour, legal counsel within four hours if personal data may be involved, and any applicable regulators within the timeframes mandated by the relevant compliance framework.

The SBOM toolchain was named. Syft generates the SBOM at build time from source — not assembled post-install, but produced from the dependency graph before the installer is built. Grype scans the SBOM against the NVD and OSS vulnerability databases as part of the CI pipeline. The CVE response SLA commits to critical vulnerabilities being addressed within fourteen days of disclosure, with a public advisory posted within forty-eight hours of the patch release.

Relay traffic was confirmed to route exclusively over port 443 with TLS 1.3. The sync daemon respects system proxy configuration including PAC files and authenticating proxies. In environments where corporate proxies perform TLS inspection, the relay connection can be added to the proxy bypass list using the standard format enterprise proxy configurations support.

The zero-downtime update path was specified: a rolling update with a health-check gate. The container orchestration layer applies the new image to one replica, runs the health check sequence, and only rotates the remaining replicas if the first reports healthy. If the update fails, the orchestration layer automatically rolls back to the previous image. The entire sequence completes without a maintenance window for typical updates.

The MDM compliance check at capability negotiation — already the strongest enterprise-governance feature in the architecture — was retained verbatim. Voss had commended it in Round 1 and it required no revision.

---

## Act 2: Round 2 — Conditional Passage

### The Security Audit Package

Round 2 opened with the question Voss applies to every enterprise software review: can this survive a CISO audit?

The answer had improved substantially. The SBOM in CycloneDX format satisfies the current NTIA minimum elements and CISA guidance — the specific format that federal agencies and large enterprise security teams request. Rootless Podman addresses the most common enterprise container objection: the architecture does not run its container runtime as root, which eliminates an entire class of privilege escalation concerns that InfoSec teams raise automatically when they see the word container. The network footprint is clean — no inbound ports on any external interface, relay traffic on port 443 only. That is a strong story for corporate firewall approval.

Voss scored the security audit story at an eight. Her remaining note was a process detail, not an architecture concern: the paper specifies what goes in the SBOM but not when and how it is generated. Security teams want to know that the SBOM is produced at build time from source code — meaning it reflects what was actually compiled into the binary — rather than assembled post-install from whatever packages happen to be present on the system. Build-time generation is the stronger claim. The paper should state it explicitly.

This became condition C1 in Round 2: specify SBOM generation timing in the CI/CD pipeline, confirming build-time generation from source.

### MDM Deployment Specifics

The MSIX packaging for Windows with Intune deployment earned a solid score. MSIX is the correct format for enterprise Windows deployment: it supports silent installation, automatic updates, and Group Policy configuration. The Intune deployment path — package upload, deployment ring configuration, compliance policy attachment — follows the standard enterprise software deployment workflow that IT administrators already understand.

The gap Voss identified: the paper does not specify whether Podman for Windows runs on the WSL2 substrate or on Hyper-V, and the choice has real implications for corporate managed environments.

WSL2 requires the Windows Subsystem for Linux feature, which some organizations disable in Group Policy because it introduces a Linux kernel execution environment they cannot fully audit. Hyper-V is the native Windows virtualization substrate and is typically already enabled in enterprise environments — but it conflicts with VMware Workstation Pro, which many enterprise developers have installed for testing. Neither choice is universally correct. The paper needs a two-sentence acknowledgment: WSL2 is the recommended default for most deployments, Hyper-V for organizations already running it as their primary virtualization substrate, with a note that IT administrators should verify compatibility with any existing virtualization products before deployment.

Condition C2: document Podman Windows substrate options with recommended defaults. This is the kind of environmental detail that saves an IT administrator from a failed deployment and a confused support ticket.

### The Deprovisioning Gap

When a developer leaves an organization, IT needs to revoke their access. The architecture handles this cryptographically: the capability rotation cycle removes the departing user role attestation, the relay propagates the revocation to active peers, and the next capability negotiation cycle confirms the revocation across the mesh.

What the paper does not describe is how an IT administrator actually triggers this process.

The cryptographic description is correct. The administrative interface is absent. An IT administrator sitting at a helpdesk console needs to know: do they open a web dashboard, run a CLI command, or call a REST endpoint? And when they take that action, what do they see — a confirmation that the revocation has been queued, a status indicator showing propagation progress, an alert when all active peers have acknowledged?

Voss scored deprovisioning at a seven and attached condition C3: add an admin tooling sketch for the revocation workflow. Not a full implementation specification — even a sketch is sufficient at this stage. IT admin opens the Admin Console, selects the user account, clicks Revoke Access, and the relay broadcasts a key rotation to all active peers within one capability cycle — that is an action. That level of specificity transforms a cryptographic guarantee into an operational procedure.

This gap is common in security-conscious architecture documents. The cryptographic properties are well-specified; the administrative interface is assumed to exist. For enterprise procurement, the administrative interface is not an implementation detail. It is part of the product.

### The Migration Path

The four-phase migration model for organizations transitioning from hosted tools earned the strongest commendation Voss issued in either round.

Phase one runs the local node in shadow mode alongside the existing hosted platform: the node receives data but does not become the authoritative source. IT can validate data volumes, query patterns, and sync behavior without committing to the switch. Phase two enables offline editing for non-conflicting data domains — tasks and documents that have no dependencies on cloud-only features — while the hosted platform remains active for everything else. Phase three gives the local node full authority for new projects while legacy records remain on the hosted platform. Phase four completes the migration of historical records through a bulk-import process that preserves record history.

Each phase is independently reversible. An organization can pause at phase two indefinitely if their change advisory board needs more evidence before approving the next step. They can roll back to phase one if phase two introduces unexpected issues. The architecture does not require commitment to the full migration path to deliver value.

Voss scored this at an eight and described the four-phase reversible model as exactly the right framing for enterprise risk management — an enterprise architect can present this to a change advisory board with confidence. Her single condition: add phase-transition success criteria and rough timing estimates. What data does an organization collect during phase one to determine they are ready for phase two? Even rough heuristics — four to eight weeks of shadow-mode operation with less than 0.1 percent sync error rate — provide the operational credibility that makes this section usable in a change advisory board presentation.

### The License Question

The procurement story — AGPLv3 plus a managed relay subscription — is structurally clean. There is no per-seat licensing negotiation, no enterprise edition with gated features, no contract renewal conversation tied to user count. IT departments understand SaaS subscriptions. They have procurement workflows for them. The open-source core removes the vendor lock-in objection that derails many procurement conversations before they start.

But the AGPLv3 copyleft clause creates a specific problem for enterprise customers who customize the software.

The AGPL network use clause requires that any organization that modifies the software and uses it to provide a service over a network must publish their modifications under the same license. Most enterprise software deployments involve customization — at minimum, UI modifications to match brand guidelines, workflow adjustments to fit organizational processes, integrations with internal systems. An organization that makes these modifications is arguably required to publish them under AGPLv3. Corporate legal teams at large enterprises frequently have categorical policies against deploying AGPLv3 software in production environments for exactly this reason.

The standard resolution is dual licensing: the default license is AGPLv3, and a commercial license is available for organizations that cannot accept copyleft terms. Metabase, Grafana, and dozens of other commercial open-source products use this structure. The commercial license grants permission to deploy and modify the software without the copyleft obligation, in exchange for the license fee.

Voss scored the procurement dimension at a six — the lowest score in her Round 2 review — and attached condition C5: address AGPLv3 copyleft implications for enterprise customization and specify a dual-license structure. This is not a fatal flaw in the architecture. It is a commercial and legal structure question that must be resolved before the first enterprise contract is signed.

### Round 2 Verdict: PROCEED WITH CONDITIONS

Voss Round 2 domain average was 7.2 — a marginal improvement over Round 1 7.1, with the blocking issue resolved and scores redistributed across the stronger governance narrative.

Her verdict: PROCEED WITH CONDITIONS.

The five conditions she attached are all addressable without architectural revision:

**C1:** Specify SBOM generation timing in the CI/CD pipeline — confirm build-time generation from source rather than post-install assembly.

**C2:** Document Podman Windows substrate options (WSL2 vs. Hyper-V) with recommended defaults and compatibility notes for environments with existing virtualization products.

**C3:** Add an admin tooling sketch for the revocation workflow — at minimum, a description of the interface an IT administrator uses to trigger and monitor access revocation.

**C4:** Add phase-transition success criteria and rough timing estimates to the migration section — what data validates readiness to move from each phase to the next.

**C5:** Address AGPLv3 copyleft implications for enterprise customization; specify or commit to specify a dual-license structure before the first enterprise sales conversation.

None of these conditions require changes to the sync protocol, the CRDT data model, the security architecture, or the deployment model. They are governance documentation, operational tooling descriptions, and commercial licensing decisions. The architecture itself cleared the review. The conditions govern how it is packaged, licensed, and operated.

---

## The Non-Negotiable Enterprise Checklist

The review across two rounds produced something more durable than a verdict: a clear picture of the constraints that any local-first architecture must satisfy before an enterprise IT department will allow it on managed endpoints.

These are not negotiating positions. They are the baseline. An architecture that does not meet them will not reach the procurement committee — it will be rejected at the IT security pre-screening that happens before the formal review.

**MDM-compatible installation.** Silent deployment via Intune on Windows and Jamf on macOS. No user interaction required. Configuration pre-seeded via MDM profile. If IT cannot deploy and configure the software without touching each endpoint individually, they cannot manage a fleet of them.

**Signed and notarized binaries.** Apple Developer ID with notarization on macOS. Authenticode signing with trusted-publisher compatibility for App Control for Business (WDAC) on Windows. Unsigned software cannot be deployed on managed endpoints without disabling security policies that exist for good reasons. Requiring that exception is a non-starter.

**SBOM at build time.** Generated from source at build time, not assembled post-install. Published in CycloneDX format. Scanned against vulnerability databases as part of the CI pipeline. Critical CVEs addressed within fourteen days of disclosure. Without a current SBOM, the software cannot pass a supply-chain security review, and supply-chain security reviews are now standard practice in enterprise procurement.

**Defined incident response procedure.** A formal runbook specifying triggering events, artifact collection sequence, chain of custody requirements, and communication protocol. The CRDT audit trail is a forensic asset — it is not the procedure. The procedure is what IT does with the audit trail when something goes wrong, and who they call first.

**Administrative tooling for deprovisioning.** A concrete interface — console, CLI, or API — that an IT administrator uses to revoke access, monitor revocation propagation, and confirm completion. Cryptographic correctness without an administrative interface is not an enterprise feature.

**Clear licensing terms for enterprise customization.** An AGPLv3 copyleft clause creates legal uncertainty for enterprise customers who customize the software. The resolution — dual licensing with a commercial option for organizations that cannot accept copyleft — must be decided before the first enterprise procurement conversation.

The architecture this book describes satisfies all of these requirements. The council review process documented in the chapters that follow is the evidence. But the checklist has value independent of this particular architecture: it applies to any local-first system that intends to be deployed on managed enterprise endpoints, sold to organizations with real compliance obligations, and operated by IT departments that did not build the software and cannot be assumed to understand its internals.

An architecture that makes IT job easier — that reduces rather than increases the surface area IT must understand, audit, and respond to — earns a different kind of conversation than one that asks IT to make exceptions. The conditions attached in Round 2 specify what completing that work requires. The architecture cleared the review. The checklist is how it stays cleared.