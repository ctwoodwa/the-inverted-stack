# Chapter 22 — Security Operations

<!-- icm/draft -->

<!-- Target: ~10,000 words (per UPF Ch15 split, post Phase 4 prune; FAILED-condition kill trigger at >12,000 words → split into Ch22 (Key Lifecycle Ops) + Ch23 (Endpoint + Collaborator Ops)) -->
<!-- Source: post-Ch15-split. Sections relocate from chapters/part-3-reference-architecture/ch15-security-architecture.md per Phase 3 of UPF 2026-04-29-upf-ch15-split.md. Section ordering preserves Ch15's original narrative arc as recommended by UPF Phase 1 triage. -->

<!-- code-check: this chapter inherits the Sunfish package surface used by the Ch15 sections it absorbs. Current-canon: `Sunfish.Kernel.Security`, `Sunfish.Kernel.Sync`, `Sunfish.Kernel.Audit` (forward-looking from #48), `Sunfish.Foundation.Recovery` (forward-looking from #48), `Sunfish.Kernel.Custody` (forward-looking from #9). Per-section code-check annotations migrate with each section in Phase 3. No NEW namespaces introduced by the split itself. -->

---

Chapter 15 specifies the security architecture. This chapter specifies what to do when that architecture is exercised — when a key is lost, when a collaborator departs, when an endpoint is compromised, when a record's classification escalates under an event trigger, when a multi-party transfer needs a verifiable custody chain. The split between architecture and operations follows the same arc Part V applies to fleet management: Part III specifies the system; Part V specifies how to operate it under stress.

Each section below is a self-contained operational flow. Readers landing on a single section from a search hit or runbook reference do not need to read the chapter top-to-bottom. The cryptographic primitives each section relies on are specified in Chapter 15 (Security Architecture); cross-references point back to the relevant Ch15 section for readers who arrive without that context.

The operational seams are deliberate. Key Compromise Incident Response handles the case where an attacker captures key material. Key-Loss Recovery handles the case where the legitimate user loses access to it. Offline Node Revocation and Collaborator Revocation handle access-removal at two scales (single device vs. ongoing collaborator). Forward Secrecy and Endpoint Compromise govern what data remains protected during and after a session is partially observed. Chain-of-Custody and Event-Triggered Re-classification govern how custody and classification of records change as they move between parties or escalate in sensitivity. Each section names its FAILED conditions explicitly — the boundary at which the operational flow ceases to deliver its security guarantee.

---

## Key Compromise Incident Response

<!-- Phase 3 placeholder: content moves from chapters/part-3-reference-architecture/ch15-security-architecture.md §Key Compromise Incident Response (current line 99). No prune budget per Phase 1 triage (382 words → 382). -->

---

## Key-Loss Recovery

<!-- Phase 3 placeholder: content moves from chapters/part-3-reference-architecture/ch15-security-architecture.md §Key-Loss Recovery (current line 117). Phase 1 prune budget: -1,400 words (4,845 → 3,445). Prune surface: 3-class table + 6-mechanism per-section dense exposition; consumer/SMB/regulated framing tightens; each mechanism's threat-model paragraph compresses ~30%. -->

---

## Offline Node Revocation and Reconnection

<!-- Phase 3 placeholder: content moves from chapters/part-3-reference-architecture/ch15-security-architecture.md §Offline Node Revocation and Reconnection (current line 286). Phase 1 prune budget: -50 words (419 → 369). Already tight. -->

---

## Collaborator Revocation and Post-Departure Partition

<!-- Phase 3 placeholder: content moves from chapters/part-3-reference-architecture/ch15-security-architecture.md §Collaborator Revocation and Post-Departure Partition (current line 302). Phase 1 prune budget: -400 words (2,462 → 2,062). Prune surface: voice-pass for #45 tightens departure-moment narrative naturally (~250 words); ~150 more from post-departure partition repetition. NOTE: voice-pass-pending HTML placeholder (`<!-- voice-check: -->`) for #45 departure-moment scene relocates with this section; voice-plan.yaml entry updates to point at Ch22. -->

---

## Forward Secrecy and Post-Compromise Security

<!-- Phase 3 placeholder: content moves from chapters/part-3-reference-architecture/ch15-security-architecture.md §Forward Secrecy and Post-Compromise Security (current line 403). Phase 1 prune budget: -150 words (1,884 → 1,734). Triage classified O on the basis that 80% of content is response framing ("when an adversary captures a session key today…"); the property *forward secrecy* is specified architecturally upstream in Ch15 §Key Hierarchy. Cross-reference to Ch15 §Key Hierarchy required at section opening. -->

---

## Endpoint Compromise: What Stays Protected

<!-- Phase 3 placeholder: content moves from chapters/part-3-reference-architecture/ch15-security-architecture.md §Endpoint Compromise: What Stays Protected (current line 494). Phase 1 prune budget: -200 words (1,723 → 1,523). Prune surface: redundancy with §Threat Model relay-observation framing collapses; sub-pattern 47a scope declaration retained verbatim. Citations [20]–[28] (renumbered from #47 draft's [14]–[22]) move with the section. -->

---

## Chain-of-Custody for Multi-Party Transfers

<!-- Phase 3 placeholder: content moves from chapters/part-3-reference-architecture/ch15-security-architecture.md §Chain-of-Custody for Multi-Party Transfers (current line 583). Phase 1 prune budget: -700 words (2,499 → 1,799). Prune surface: worked examples for dashcam, clinical handoffs, LADOT-MDS relocate to Appendix B with reference back per UPF Stage 0; protocol specification stays. -->

---

## Event-Triggered Re-classification

<!-- Phase 3 placeholder: content moves from chapters/part-3-reference-architecture/ch15-security-architecture.md §Event-Triggered Re-classification (current line 690). Phase 1 prune budget: -250 words (1,526 → 1,276). Prune surface: opening dashcam framing repeats §Chain-of-Custody opening — collapse to single shared scenario. -->

---

## References

<!-- Phase 3 placeholder: Ch22's share of the Ch15 reference list (~470 words). Citations split per-section between Ch15 (architecture share) and Ch22 (operations share); Ch22 keeps cites referenced from O sections. Per UPF Phase 1 triage: Shamir [6] (key-loss recovery), Buterin [4] (social recovery), Argent [5] (multi-sig wallet patterns), Sigstore [2] (supply chain — though cross-referenced from Ch15), the SGX/TEE family [22]–[24] (endpoint compromise), Pegasus + Hermit [26]–[27] (endpoint compromise), TSP RFC 3161 [28] (chain-of-custody timestamp), and the DP family [32]–[36] if Privacy-Aggregation is reclassified to O in a later round (currently A per Phase 1 triage footnote ¹). Final assignment confirmed during Phase 5 cross-reference work. -->
