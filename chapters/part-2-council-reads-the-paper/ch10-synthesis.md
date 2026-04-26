# Chapter 10 — Synthesis: What the Council Finally Agreed On

<!-- icm/prose-review -->

<!-- Target: ~2,500 words -->
<!-- Source: R1, R2 -->

Five experts. Two rounds. Two blocks cleared, fifteen conditions attached, one unconditional PROCEED, and an architecture that entered Round 1 as a proposal and exited Round 2 as a structural commitment. Shevchenko blocked on CRDT (Conflict-free Replicated Data Type) garbage collection and Flease split-writes. Kelsey blocked on the missing commercial model. Okonkwo conditioned on key compromise response. Ferreira conditioned on the export path. Voss conditioned on MDM (Mobile Device Management) governance and SBOM (Software Bill of Materials). Every block cleared. Every condition produced a specific change in the architecture. The architecture that survived is not the architecture that was proposed. It is the architecture the council allowed to proceed. This is what the review found, where it pulled in opposing directions, and what the result became.


---

## Round 1: The Architecture Fails

The council entered with different concerns but arrived at the same judgment. The architecture was not ready.

The aggregate Round 1 scorecard told one story on the surface and concealed another underneath. The 6.8 average across five members sounds like a reasonable start. Two members issued hard blocks. When two of five reviewers block, the paper does not proceed. No averaging resolves that. Averaging is for conditions, not blocks.

| Member | Domain Avg | Verdict |
|--------|-----------|---------|
| Dr. Voss — Enterprise Infrastructure | 7.1 | PROCEED WITH CONDITIONS |
| Prof. Shevchenko — Distributed Systems | 7.1 | **BLOCK** |
| Nia Okonkwo — Security | 7.3 | PROCEED WITH CONDITIONS |
| Jordan Kelsey — Product | 5.5 | **BLOCK** |
| Tomás Ferreira — Local-First | 7.0 | PROCEED WITH CONDITIONS |

Shevchenko's block was technical. Two separate correctness gaps, each serious enough on its own. The CRDT garbage collection strategy was absent. Without a GC policy, every node accumulates operation log history without bound — a performance cliff that hits any deployment running longer than about twelve months. The Flease split-write window was unaddressed. If the lease-holder becomes unreachable during a write and a new lease is elected, two nodes can briefly and simultaneously believe they hold write authority. That window is either safe because CRDT merge absorbs it, or it creates a data corruption scenario. The paper said nothing about which.

Kelsey's block was commercial. The first customer archetype was completely absent. Not vague — absent. A paper proposing a commercial architecture that cannot name who pays first, why they pay, and how to find them has not written the business case yet. The OSS-to-paid conversion mechanism had the same problem. The paper implied that teams would pay for the relay when they need it without specifying what causes that need to crystallize into a transaction.

Shevchenko's block and Kelsey's block were entirely separate failures. Either could have been resolved without touching the other. The paper had two distinct things to fix, not one.

Okonkwo did not block. Her verdict carried a condition that functioned like a soft block. Key compromise incident response was absent. She graded the dimension at 5/10 and conditioned her PROCEED on the issue being resolved before any security review sign-off. For a system where a compromised node key potentially exposes all data the node had ever been authorized to read, the absence of a detection mechanism, a re-keying procedure, and a user-visible notification was not an oversight. It was a gap in the threat model.

Ferreira's block — data portability — was the sharpest philosophical objection in either round. A paper that argues for data ownership as a core principle and then omits the export button contradicts itself in the most visible possible way. His words: "This is a philosophical and practical blocker."

The Round 1 commendations marked what the revision had to preserve. Shevchenko and Ferreira commended the three-tier CRDT resolution model. Okonkwo and Shevchenko commended subscription filtering at the send tier. Voss commended the MDM compliance check at capability negotiation. Okonkwo commended the EAS attestation and key wrapping distinction. Kelsey commended the OSS public-good reframe. These were not politeness — they marked the parts of the architecture that worked.

---

## Round 2: The Architecture Survives (with Conditions)

The revision cleared every BLOCK verdict.

| Member | R1 Avg | R2 Avg | Delta | Verdict |
|--------|--------|--------|-------|---------|
| Dr. Voss | 7.1 | 7.2 | +0.1 | PROCEED WITH CONDITIONS |
| Prof. Shevchenko | 7.1 | 6.8 | -0.3 | PROCEED WITH CONDITIONS |
| Nia Okonkwo | 7.3 | 7.0 | -0.3 | PROCEED WITH CONDITIONS |
| Jordan Kelsey | 5.5 | 6.8 | +1.3 | PROCEED WITH CONDITIONS |
| Tomás Ferreira | 7.0 | 7.6 | +0.6 | PROCEED — NO CONDITIONS |
| **Overall** | **6.8** | **7.1** | **+0.3** | **PROCEED WITH CONDITIONS** |

Ferreira's unconditional PROCEED is the most meaningful single verdict in Round 2. He is the council member with the strictest local-first standards — a practitioner who has shipped production local-first applications and watched the failure modes that theory misses. He checked the revised architecture against all seven Kleppmann ideals and found every one satisfied. A practitioner with the hardest standards gave the cleanest pass.

Kelsey's +1.3 delta is the largest movement in either direction. His Round 1 score was the lowest from any member — 5.5, reflecting a commercial section that was not yet written. Round 2 addressed the construction vertical selection, the five-step customer development path, and the relay economics model. The commercial section moved from the architecture's weakest section to a credible business model in a single revision.

Shevchenko's -0.3 delta is the one number that requires explanation. His score dropped. That did not signal a failure. It signaled the opposite. He entered Round 2 with his two blocking issues resolved and raised new technical concerns he had not seen before: stale peer recovery protocol, CRDT operation validation, sync daemon buffer behavior during prolonged partition. These are real gaps, but they are implementation-depth concerns, not correctness failures. Shevchenko's score dropped because he took the architecture more seriously in Round 2, not less.

The council's consensus statement captures what happened between rounds: "The new concerns raised in Round 2 are second-order — they arise from the paper being taken seriously as an implementation guide rather than a conceptual proposal."

The consensus was not frictionless. The clearest tension surfaced between Okonkwo and Kelsey. Okonkwo's insistence that the key-compromise incident-response procedure be executable by a non-cryptographer IT administrator before first external release conflicted directly with Kelsey's commercial-timeline pressure to ship the dual-license structure and first-customer acquisition path on a revenue-bearing cadence. The architecture resolved this by classifying both as pre-GA blockers rather than post-GA roadmap items. Neither ships without the other. A second tension ran between Ferreira's plain-file export — the Property 7 proof of ownership — and Voss's enterprise data-governance requirements, where some data categories are under regulatory custody that constrains free export. The resolution: export must exist for user-owned records and must disclose the categories where regulatory custody overrides user export rights. Shevchenko and Kelsey produced the quietest friction. Shevchenko's correctness rigor required formal documentation of stale peer recovery before implementation. Kelsey's unit economics required shipping with known rough edges to reach revenue. The resolution was to ship the protocol with documented known gaps rather than perfecting it first, but to name the gaps in the public specification. Every resolution was made. None of them were free.

---

## The Seven Non-Negotiables

Five reviewers across two rounds produced hundreds of individual observations. Most were specific to one member's domain. Seven properties were different. They appeared across multiple members, survived both rounds, and were treated as mandatory without negotiation. Part III is built against these seven constraints.

**1. Data minimization at the protocol layer.** Subscription filtering happens at the send tier. Not in the application layer. Not at the receive tier. A node receives only the data its role authorizes, and that constraint is enforced before the data leaves the sending node. Okonkwo called this "a genuine architectural achievement, not a compliance checkbox." Shevchenko commended it as the correct security invariant, noting that most implementations get it backwards. An application-layer filter intercepts the same data at the wrong point — after it has already been transmitted.

**2. MDM compliance check at capability negotiation.** Before a node exchanges any data, it must pass an MDM compliance check. A node that fails the check does not proceed to the capability negotiation phase. Voss's commendation was precise: a compromised non-compliant node is rejected before it touches data. Enterprise deployments cannot rely on reactive detection. The compliance gate must be proactive and early. This constraint belongs in the sync daemon handshake protocol, not in an application policy layer.

**3. Three-tier CRDT resolution model.** The architecture does not apply CRDT merge uniformly across all data types. Documents and collaborative content sit in the AP tier, where CRDT merge handles conflicts automatically. Operations that require a single writer — sequential ID generation, inventory quantity, appointment slots, financial transaction totals — sit in the CP tier under distributed lease coordination. Financial ledger entries sit outside the CRDT entirely. They are append-only, posted by the domain ledger engine, and not subject to merge. Shevchenko commended this as "the most technically honest treatment of CRDT applicability seen in a local-first architecture proposal." The three-tier model works because it stops claiming CRDT solves problems it does not solve.

**4. DEK (Data Encryption Key)/KEK (Key Encryption Key) envelope encryption with rotation proportional to document count.** Each document holds a data encryption key (DEK). Each role holds a key encryption key (KEK) that wraps the DEKs for documents that role can access. When a role is revoked, the KEK rotates, and DEKs for affected documents are re-wrapped under the new KEK. An attacker who compromises a role KEK gains access to documents that key could decrypt. Not documents outside that role's scope. Not forward access after rotation. Okonkwo's key hierarchy requirement — root org key to role KEKs to per-node wrapped keys to per-record DEKs — codifies exactly this structure.

**5. Dual-license structure from day one.** AGPLv3 governs the open-source repository. A commercial license is available for organizations that cannot accept AGPLv3's network use clause. Kelsey's condition was the sharper one. The CLA and dual-license structure must be in place before the repository opens. Retrofitting a license change after the community has formed requires contributor license agreements from every prior contributor. The structure must be established at founding.

**6. Non-technical disaster recovery path.** A non-technical user must be able to recover their complete data after total device failure without calling support. Data ownership is meaningless if only a developer can perform the restore. The non-technical disaster recovery walkthrough is not a UX nicety. It is the proof of the ownership claim.

**7. Plain-file export with no vendor cooperation required.** Users can export all their data to a standard file format — plain files, CSV, JSON — without contacting the vendor, without the vendor's cooperation, and without any special tooling beyond a standard file manager. A user who can export their data can leave. A user who cannot is not in control, regardless of what the marketing copy says.

These seven properties function as architectural invariants. They operate in a deployment context where intermittent connectivity is the baseline operating condition for hundreds of millions of enterprise workers. GCC (Gulf Cooperation Council) field operations, rural Indian BFSI (Banking, Financial Services, and Insurance), Sub-Saharan African field deployments, rural Latin American secondary cities — these are not edge cases the architecture gracefully handles. The non-negotiables are the structural answer to that deployment reality, not optional resilience layers for a cloud-stable-by-default product.

The council's verdict rests on one empirical anchor the architecture can point to without hedging. In 2022, Adobe, Autodesk, Microsoft, Figma ([figma.com](https://www.figma.com/), the design tool), and dozens of other Western SaaS (Software as a Service) vendors suspended service across Russia and CIS (Commonwealth of Independent States) markets under sanctions enforcement. Hundreds of thousands of organizations that had built operational workflows over more than a decade lost access with days of notice. Every non-negotiable above is a constraint that would have changed the outcome for affected organizations. Data minimization and DEK/KEK encryption kept ciphertext locally even where relay access was severed. The three-tier CRDT model and plain-file export preserved operational continuity independent of vendor availability. The dual-license structure meant the software itself was not removable from the customer even when the vendor's service was. The council did not build these seven properties against a hypothetical threat. They built them against a documented failure the industry had already produced.

---

## The Open Questions

The council cleared the architecture for alpha implementation. Six questions remain genuinely open. Not because the council avoided them. Because they represent constraints the implementation must navigate without a clean answer.

**Multi-jurisdiction data sovereignty and CRDT systems.** The Right to Erasure under GDPR (General Data Protection Regulation) Article 17 — and parallel erasure rights across the regimes named in Appendix F (LGPD (Lei Geral de Proteção de Dados), POPIA (Protection of Personal Information Act), NDPR (Nigeria Data Protection Regulation), DPDP (Digital Personal Data Protection), PIPA (Personal Information Protection Act), PIPL (Personal Information Protection Law), and others) — creates a structural tension with CRDT full-history retention. Deleting an operation may break the DAG (Directed Acyclic Graph) that establishes document history. The crypto-shredding pattern offers a uniform resolution: destroy the DEK for the affected document, rendering the data cryptographically inaccessible. But cryptographically inaccessible is not the same as erased. Whether regulators in each jurisdiction treat DEK destruction as fulfilling the erasure right is an interpretation question. Schrems II (CJEU, 2020) adds a parallel constraint on cross-border transfers of EU personal data to US cloud providers; the architecture's answer — local retention with no relay-exposed payload — is the structural response, not a contractual safeguard. Russia's Federal Law 242-FZ, the UAE's DIFC (Dubai International Financial Centre) DPL (Data Protection Law) 2020, and China's PIPL impose localization requirements that make Tier 3 compliance retention the architecturally required path, not a preference. Okonkwo flagged this as high priority. Chapter 15 specifies the compliance framework mapping across every named jurisdiction; the architecture must document the crypto-shredding limitation honestly. EDPB (European Data Protection Board) guidance on pseudonymization and on rendering personal data inaccessible already exists and does not fully resolve the erasure-equivalence question. The architecture engages with that regulatory discourse rather than treating it as a blank slate.

**Relay geographic architecture.** The managed relay routes ciphertext only. The metadata it observes — which nodes communicate with which, at what times, at what volume — is itself subject to jurisdictional data-residency scrutiny. For EU buyers under Schrems II, DIFC-licensed firms under DIFC 2020, Russian organizations under 242-FZ, or Chinese organizations under PIPL, the question of where the relay operator's infrastructure is legally located determines whether the architecture satisfies regulatory transfer constraints. The self-hosted relay path answers this for high-sensitivity deployments. The managed relay requires jurisdictional deployment choices: EU-resident for Schrems II, Russia-resident for 242-FZ, and so on. This is one of the most consequential implementation decisions in the architecture and is currently unspecified. Chapter 16 addresses the relay architecture; relay geographic residency becomes a per-deployment choice with regulatory consequences. A distinct threat model operates in parallel: state-mandated data access on cloud-hosted infrastructure. Local key management, where keys never leave the user's device, addresses this threat model architecturally — the relay cannot produce decryptable content because the relay does not possess decryptable content. This is a deployment consideration relevant across multiple jurisdictions, not a political judgment about any specific government.

**Relay commoditization moat.** The managed relay is the primary revenue source. The relay protocol is open-source. A cloud provider can offer a managed relay at infrastructure cost with no margin. What makes the vendor's relay defensible? Kelsey named this the most likely year-two failure mode. The answer — support quality, product-integrated onboarding, reliability SLAs — is not yet articulated in the architecture document. The moat is operational, not technical. Operational moats require a different kind of specification.

**Formal validation of domain-level merge invariants.** When a CRDT operation arrives at a node — structurally valid, correctly signed, from a legitimate peer — but semantically incorrect because the client had a software bug, the CRDT merges it faithfully and propagates the corruption to all peers. This is an inherent property of any convergent system. Structural validity does not imply semantic correctness. The architecture specifies operation validation at insertion, but formal criteria require domain-specific specification. Part III defines the validation layer. Each deployment defines its own domain invariants.

**KEK compromise incident response under realistic enterprise conditions.** The procedure exists in the revised architecture. The open question is not whether it is specified. It is whether it is executable. An IT administrator who is not a cryptographer. A node offline for an unknown duration. A role KEK in use for months. The procedure needs operational testing. Alpha implementation is the right time to find the gaps.

**Analytics and telemetry without re-centralizing.** Ferreira's observation about implementation drift is the most likely long-term architectural risk. In a local-first architecture, a server-side analytics endpoint is not available by default. Teams that add one, for valid product development reasons, begin re-centralizing the architecture in exactly the way the original local-first ideals warn against [1]. The architecture must specify an analytics model before implementation teams face the pressure: opt-in telemetry only, aggregate statistics through relay metadata, or no analytics at all. Not choosing is also a choice. Made under pressure, not deliberation.

These six questions are not architectural flaws. They are known constraints the implementation must navigate. Part III specifies each component with these constraints in view.

---

## How the Council Verdict Shapes Part III

The council's PROCEED with fifteen conditions is not a finished design. It is a green light to build, with a specific list of things to get right.

Part III is structured against the seven non-negotiables. Chapter 11 specifies the node kernel, including the plugin contract that enforces the three-tier CRDT model. Chapter 12 specifies the CRDT engine and data layer, including the GC policy, the stale peer recovery protocol, and the operation validation layer Shevchenko conditioned in Round 2. Chapter 13 specifies schema migration — the hardest operational problem that underlies the stale peer recovery condition directly. Chapter 14 specifies the sync daemon protocol, including the five-phase handshake, the data minimization invariant at the send tier, and the distributed lease coordination governing CP-class operations. Chapter 15 specifies the security architecture, including the full DEK/KEK hierarchy, the key compromise incident response procedure, and the compliance framework mapping Okonkwo conditioned. Chapter 16 specifies persistence beyond the node, including the relay architecture, the BYOC (Bring Your Own Cloud) backup model, and the plain-file export path Ferreira required.

The fifteen conditions are distributed across Part III and Part IV, addressed where they are architecturally relevant. The stale peer recovery protocol belongs in Chapter 12, alongside the GC policy that creates the condition under which it is needed. The admin tooling sketch belongs in Chapter 19, alongside the MDM deployment guidance. The GDPR Article 17 crypto-shredding treatment belongs in Chapter 15, alongside the compliance framework mapping.

The council reviewed an architecture document. Part III is the architecture. The two are different objects.

Chapters 5 through 10 were a procedure. A proposal submitted, reviewed, blocked, revised, and approved under conditions. The reader witnessed a process. The architecture had to be argued for, defended, and refined against objection. It arrived at its current form through that process. The Flease lease coordination, the send-tier subscription filter, the DEK/KEK rotation policy are not arbitrary choices. They are specific answers to specific blocks.

Part III is not a continuation of that process. It is its output.

The voice shifts here by design. Part II's register is narrative: events happened, reviewers reacted, positions changed. Part III's register is specification: the component does this, the invariant holds for this reason, the failure mode presents as this. A specification that performs uncertainty undermines the thing it is specifying. Part III is written with the confidence of an architecture that has already survived adversarial review. Because it has.

Read Part III knowing that every mechanism was earned before it was specified. The seven non-negotiables are the spinal cord. Each specification chapter is organized against at least one of them.

---

*Part III begins with the node — its kernel, its plugin contracts, and the process boundaries that make the rest of the architecture possible.*

---

## References

[1] M. Kleppmann, A. Wiggins, P. van Hardenberg, and M. McGranaghan, "Local-first software: You own your data, in spite of the cloud," in *Proc. ACM SIGPLAN Int. Symp. New Ideas, New Paradigms, and Reflections on Programming and Software (Onward! '19)*, Athens, Greece, Oct. 2019, pp. 154–178, doi: 10.1145/3359591.3359737. [Online]. Available: https://www.inkandswitch.com/essay/local-first/
