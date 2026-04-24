# Chapter 10 — Synthesis: What the Council Finally Agreed On

<!-- icm/prose-review -->

<!-- Target: ~2,500 words -->
<!-- Source: R1, R2 -->

The council approved the architecture. Round 1 ended with two hard blocks and a 6.8 average. Round 2 cleared every block, raised the average to 7.1, and issued fifteen conditions — none individually blocking, all resolvable during alpha implementation. The result is a green light with a specific list of things to get right.


---

## Round 1: The Architecture Fails

The council entered with different concerns but arrived at the same judgment: the architecture was not ready.

The aggregate Round 1 scorecard told one story on the surface — 6.8 average across five members, which sounds like a reasonable start. It concealed another story underneath. Two members issued hard blocks. When two of five reviewers block, the paper does not proceed. No averaging resolves that; averaging is for conditions, not blocks.

| Member | Domain Avg | Verdict |
|--------|-----------|---------|
| Dr. Voss — Enterprise Infrastructure | 7.1 | PROCEED WITH CONDITIONS |
| Prof. Shevchenko — Distributed Systems | 7.1 | **BLOCK** |
| Nia Okonkwo — Security | 7.3 | PROCEED WITH CONDITIONS |
| Jordan Kelsey — Product | 5.5 | **BLOCK** |
| Tomás Ferreira — Local-First | 7.0 | PROCEED WITH CONDITIONS |

Shevchenko's block was technical. Two separate correctness gaps, each serious enough on its own. The CRDT garbage collection strategy was absent. Without a GC policy, every node accumulates operation log history without bound — a performance cliff that hits any deployment running longer than about twelve months. The Flease split-write window was unaddressed. If the lease-holder becomes unreachable during a write and a new lease is elected, two nodes can briefly and simultaneously believe they hold write authority. That window is either safe because CRDT merge absorbs it, or it creates a data corruption scenario. The paper said nothing about which.

Kelsey's block was commercial. The first customer archetype was completely absent. Not vague — absent. A paper proposing a commercial architecture that cannot name who pays first, why they pay, and how to find them has not written the business case yet. The OSS-to-paid conversion mechanism had the same problem: the paper implied that teams would pay for the relay when they need it without specifying what causes that need to crystallize into a transaction.

Shevchenko's block and Kelsey's block were entirely separate failures. One could have been resolved without touching the other. The paper had two distinct things to fix, not one.

Okonkwo did not block, but her verdict came with a condition that functioned like a soft block: key compromise incident response was absent. She graded the dimension at 5/10 and conditioned her PROCEED on the issue being resolved before any security review sign-off. For a system where a compromised node key potentially exposes all data the node had ever been authorized to read, the absence of a detection mechanism, a re-keying procedure, and a user-visible notification was not an oversight — it was a gap in the threat model.

Ferreira's block — data portability — was the sharpest philosophical objection in either round. A paper that argues for data ownership as a core principle and then omits the export button contradicts itself in the most visible possible way. His words: "This is a philosophical and practical blocker."

The Round 1 commendations defined what the revision had to preserve: the three-tier CRDT resolution model (Shevchenko, Ferreira), subscription filtering at the send tier (Okonkwo, Shevchenko), the MDM compliance check at capability negotiation (Voss), the EAS attestation and key wrapping distinction (Okonkwo), and the OSS public-good reframe (Kelsey). These were not politeness — they marked the parts of the architecture that worked.

---

## Round 2: The Architecture Survives (with Conditions)

The revision cleared every block. The revision cleared every BLOCK verdict.

| Member | R1 Avg | R2 Avg | Delta | Verdict |
|--------|--------|--------|-------|---------|
| Dr. Voss | 7.1 | 7.2 | +0.1 | PROCEED WITH CONDITIONS |
| Prof. Shevchenko | 7.1 | 6.8 | -0.3 | PROCEED WITH CONDITIONS |
| Nia Okonkwo | 7.3 | 7.0 | -0.3 | PROCEED WITH CONDITIONS |
| Jordan Kelsey | 5.5 | 6.8 | +1.3 | PROCEED WITH CONDITIONS |
| Tomás Ferreira | 7.0 | 7.6 | +0.6 | PROCEED — NO CONDITIONS |
| **Overall** | **6.8** | **7.1** | **+0.3** | **PROCEED WITH CONDITIONS** |

Ferreira's unconditional PROCEED is the most meaningful single verdict in Round 2. He is the council member with the strictest local-first standards — a practitioner who has shipped production local-first applications and watched the failure modes that theory misses. He checked the revised architecture against all seven Kleppmann ideals and found every one satisfied. A practitioner with the hardest standards gave the cleanest pass.

Kelsey's +1.3 delta is the largest movement in either direction. Round 1 was the lowest score from any member — 5.5, reflecting a commercial section that was not yet written. Round 2 addressed the construction vertical selection, the five-step customer development path, and the relay economics model. The commercial section went from the architecture's weakest section to a credible business model in a single revision.

Shevchenko's -0.3 delta is the one number that requires explanation. His score dropped. This did not signal a failure — it signaled the opposite. He entered Round 2 with his two blocking issues resolved and raised new technical concerns he had not seen before: stale peer recovery protocol, CRDT operation validation, sync daemon buffer behavior during prolonged partition. These are real gaps, but they are implementation-depth concerns, not correctness failures. Shevchenko's score dropped because he took the architecture more seriously in Round 2, not less.

The council's consensus statement captures what happened between rounds: "The new concerns raised in Round 2 are second-order — they arise from the paper being taken seriously as an implementation guide rather than a conceptual proposal."

---

## The Seven Non-Negotiables

Five reviewers across two rounds produced hundreds of individual observations. Most were specific to one member's domain. Seven properties were different — they appeared across multiple members, survived both rounds, and were treated as mandatory without negotiation. Part III is built against these seven constraints.

**1. Data minimization at the protocol layer.** Subscription filtering happens at the send tier, not in the application layer and not at the receive tier. A node receives only the data its role authorizes, and that constraint is enforced before the data leaves the sending node. Okonkwo called this "a genuine architectural achievement, not a compliance checkbox." Shevchenko commended it as the correct security invariant, noting that most implementations get it backwards. An application-layer filter catches the same data at the wrong point — after it has already been transmitted.

**2. MDM compliance check at capability negotiation.** Before a node exchanges any data, it must pass an MDM compliance check. A node that fails the check does not proceed to the capability negotiation phase. Voss's commendation was precise: a compromised non-compliant node is rejected before it touches data. Enterprise deployments cannot rely on reactive detection; the compliance gate must be proactive and early. This constraint belongs in the sync daemon handshake protocol, not in an application policy layer.

**3. Three-tier CRDT resolution model.** The architecture does not apply CRDT merge uniformly across all data types. Documents and collaborative content sit in the AP tier — CRDT merge handles conflicts automatically. Operations that require a single writer — sequential ID generation, inventory quantity, appointment slots, financial transaction totals — sit in the CP tier under distributed lease coordination. Financial ledger entries sit outside the CRDT entirely; they are append-only, posted by the domain ledger engine, and not subject to merge. Shevchenko commended this as "the most technically honest treatment of CRDT applicability seen in a local-first architecture proposal." The three-tier model works because it stops claiming CRDT solves problems it does not solve.

**4. DEK/KEK envelope encryption with rotation proportional to document count.** Each document holds a data encryption key (DEK). Each role holds a key encryption key (KEK) that wraps the DEKs for documents that role can access. When a role is revoked, the KEK rotates, and DEKs for affected documents are re-wrapped under the new KEK. An attacker who compromises a role KEK gains access to documents that key could decrypt — not documents outside that role's scope, and not forward access after rotation. Okonkwo's key hierarchy requirement — root org key to role KEKs to per-node wrapped keys to per-record DEKs — codifies exactly this structure.

**5. Dual-license structure from day one.** AGPLv3 governs the open-source repository. A commercial license is available for organizations that cannot accept AGPLv3's network use clause. Kelsey's condition was the sharper one: the CLA and dual-license structure must be in place before the repository opens, because retrofitting a license change after the community has formed requires contributor license agreements from every prior contributor. The time to establish the structure is at founding.

**6. Non-technical disaster recovery path.** A non-technical user must be able to recover their complete data after total device failure without calling support. The architecture claims data ownership, and data ownership is meaningless if only a developer can perform the restore. The non-technical disaster recovery walkthrough is not a UX nicety — it is the proof of the ownership claim.

**7. Plain-file export with no vendor cooperation required.** Users can export all their data to a standard file format — plain files, CSV, JSON — without contacting the vendor, without the vendor's cooperation, and without any special tooling beyond a standard file manager. A user who can export their data can leave. A user who cannot is not in control, regardless of what the marketing copy says.

These seven properties function as architectural invariants.

---

## The Open Questions

The council cleared the architecture for alpha implementation. Five questions remain genuinely open — not because the council avoided them, but because they represent constraints the implementation must navigate without a clean answer.

**GDPR Article 17 and CRDT systems.** The Right to Erasure requires personal data be deleted on request. A CRDT operation log that retains every mutation for correctness creates a structural tension: deleting an operation may break the DAG that establishes document history. The crypto-shredding pattern offers a partial resolution — delete the DEK for the affected document, rendering the data cryptographically inaccessible. But cryptographically inaccessible is not the same as erased, and whether regulators treat DEK deletion as fulfilling Article 17 is a question of interpretation. Okonkwo flagged this as high priority. The architecture must document the limitation honestly and specify the crypto-shredding path for implementations that choose it.

**Relay commoditization moat.** The managed relay is the primary revenue source. The relay protocol is open-source. A cloud provider can offer a managed relay at infrastructure cost with no margin. What makes the vendor's relay defensible? Kelsey named this the most likely year-two failure mode. The answer — support quality, product-integrated onboarding, reliability SLAs — is not yet articulated in the architecture document. The moat is operational, not technical, and operational moats require a different kind of specification.

**Formal validation of domain-level merge invariants.** When a CRDT operation arrives at a node — structurally valid, correctly signed, from a legitimate peer — but semantically incorrect because the client had a software bug, the CRDT merges it faithfully and propagates the corruption to all peers. This is an inherent property of any convergent system: structural validity does not imply semantic correctness. The architecture specifies operation validation at insertion, but formal criteria require domain-specific specification. Part III defines the validation layer; each deployment defines its own domain invariants.

**KEK compromise incident response under realistic enterprise conditions.** The procedure exists in the revised architecture. The open question is not whether it is specified — it is whether it is executable: an IT administrator who is not a cryptographer, a node offline for an unknown duration, a role KEK in use for months. The procedure needs operational testing. Alpha implementation is the right time to find the gaps.

**Analytics and telemetry without re-centralizing.** Ferreira's observation about implementation drift is the most likely long-term architectural risk. In a local-first architecture, a server-side analytics endpoint is not available by default. Teams that add one, for valid product development reasons, begin re-centralizing the architecture in exactly the way the original local-first ideals warn against. [1] The architecture must specify an analytics model before implementation teams face the pressure: opt-in telemetry only, aggregate statistics through relay metadata, or no analytics at all. Not choosing is also a choice — made under pressure, not deliberation.

These five questions are not architectural flaws. They are known constraints the implementation must navigate. Part III specifies each component with these constraints in view.

---

## How the Council Verdict Shapes Part III

The council's PROCEED with fifteen conditions is not a finished design. It is a green light to build, with a specific list of things to get right.

Part III is structured against the seven non-negotiables. Chapter 11 specifies the node kernel, including the plugin contract that enforces the three-tier CRDT model. Chapter 12 specifies the CRDT engine and data layer, including the GC policy, the stale peer recovery protocol, and the operation validation layer Shevchenko conditioned in Round 2. Chapter 13 specifies schema migration — the hardest operational problem that underlies the stale peer recovery condition directly. Chapter 14 specifies the sync daemon protocol, including the five-phase handshake, the data minimization invariant at the send tier, and the distributed lease coordination governing CP-class operations. Chapter 15 specifies the security architecture, including the full DEK/KEK hierarchy, the key compromise incident response procedure, and the compliance framework mapping Okonkwo conditioned. Chapter 16 specifies persistence beyond the node, including the relay architecture, the BYOC backup model, and the plain-file export path Ferreira required.

The fifteen conditions are distributed across Part III and Part IV, addressed where they are architecturally relevant. The stale peer recovery protocol belongs in Chapter 12, alongside the GC policy that creates the condition under which it is needed. The admin tooling sketch belongs in Chapter 19, alongside the MDM deployment guidance. The GDPR Article 17 crypto-shredding treatment belongs in Chapter 15, alongside the compliance framework mapping.

The council reviewed an architecture document. Part III is the architecture.

---

*Part III begins with the node — its kernel, its plugin contracts, and the process boundaries that make the rest of the architecture possible.*

---

## References

[1] M. Kleppmann, A. Wiggins, P. van Hardenberg, and M. McGranaghan, "Local-first software: you own your data, in spite of the cloud," in *Proc. ACM SIGPLAN Int. Symp. New Ideas, New Paradigms, and Reflections on Programming and Software (Onward!)*, Oct. 2019, pp. 154–178.
