---
type: upf-phase-1-triage
date: 2026-04-29
author: PAO
audience: XO (UPF author), Yeoman (Phase 3 executor), CO (visibility)
parent-decision: 2026-04-29-upf-ch15-split.md
phase: 1 of 7
gate: zero M-classified sections (or, if M's exist, Phase 1.5 rewrite plan added)
---

# UPF Ch15 Split — Phase 1 Triage

## Verdict

**Zero M (mixed) sections after read-through.** UPF Stage 0's claim of clean seams holds. Phase 1.5 (rewrite straddling sections) does not fire. Phase 2 (Ch22 skeleton) is unblocked.

Two sections required closer reads to confirm classification (§9 Forward Secrecy, §17 Privacy-Aggregation). Both resolved cleanly — see footnotes below.

## Per-section classification + prune estimates

Section sizes from `awk` over current `chapters/part-3-reference-architecture/ch15-security-architecture.md` (22,165 words across 19 top-level sections including References).

### Architecture (A) — stays in Ch15

| § | Section | Current words | Prune estimate | Post-prune | Rationale for A |
|---:|---|---:|---:|---:|---|
| 1 | Threat Model | 312 | 0 | 312 | Architectural framing; bounds the rest of the chapter. |
| 2 | Four Defensive Layers | 502 | 0 | 502 | Architectural primitives in 4 independent layers. |
| 3 | Key Hierarchy | 459 | 0 | 459 | Static key-tier structure (org → role → node → record). |
| 4 | Role Attestation Flow | 310 | 0 | 310 | Architectural distribution protocol; the *flow* describes how the protocol operates, not what to do during an event. |
| 10 | In-Memory Key Handling | 285 | 0 | 285 | Architectural primitive (locked memory, zeroing, re-auth intervals). |
| 12 | Supply Chain Security | 312 | 0 | 312 | Architectural posture (CIDs, signing, Sigstore transparency log). |
| 14 | GDPR Article 17 and Crypto-Shredding | 412 | -50 | 362 | Architectural compliance framework mapping; jurisdiction enumeration prunes lightly. |
| 16 | Relay Trust Model | 813 | -150 | 663 | Architectural trust model; some overlap with §Threat Model on relay observability prunes. |
| 17 | Privacy-Preserving Aggregation at Relay | 1,784 | -400 | 1,384 | Architectural extension of §Relay Trust Model — defines the differential-privacy *property* the relay implements, scoped to side-effect metadata aggregates only. Opening framing repeats §Relay Trust Model context; that's the prunable surface. ¹ |
| 18 | Security Properties Summary | 317 | 0 | 317 | Recap of the architectural commitments above; serves as Ch15's closer. |
| — | References (Ch15 share) | ~450 | 0 | ~450 | Citations split per-section between Ch15 and Ch22; Ch15 keeps cites referenced from A sections. |
| **Subtotal** | | **5,956** | **−600** | **~5,356** | Within UPF target of ≤5,500 ✓ |

### Operational (O) — moves to Ch22

| § | Section | Current words | Prune estimate | Post-prune | Rationale for O |
|---:|---|---:|---:|---:|---|
| 5 | Key Compromise Incident Response | 382 | 0 | 382 | Pure operational flow; named "incident response." |
| 6 | Key-Loss Recovery | 4,845 | -1,400 | 3,445 | Operational recovery flows (3 deployment classes, 6 mechanisms, audit trail). The 3-class table + 6-mechanism per-section dense exposition is the prune surface; consumer/SMB/regulated framing tightens; each mechanism's threat-model paragraph can compress ~30%. |
| 7 | Offline Node Revocation and Reconnection | 419 | -50 | 369 | Procedural reconnection flow with user-visible message wording; tight already. |
| 8 | Collaborator Revocation and Post-Departure Partition | 2,462 | -400 | 2,062 | Departure-scenario operational flow; voice-pass for #45 tightens departure-moment narrative naturally (~250 words); ~150 more from post-departure partition repetition. |
| 9 | Forward Secrecy and Post-Compromise Security | 1,884 | -150 | 1,734 | Operational flow for what happens within a compromised session before/after key rotation; opens with "Each requires specific protocol design at the session layer" — protocol response, not standalone property. ² |
| 11 | Endpoint Compromise: What Stays Protected | 1,723 | -200 | 1,523 | Event-response framing ("when X happens"); sub-pattern 47a scope declaration. Some redundancy with §Threat Model relay-observation framing that can prune. |
| 13 | Chain-of-Custody for Multi-Party Transfers | 2,499 | -700 | 1,799 | Operational protocol with worked examples for dashcam, clinical handoffs, LADOT-MDS. UPF Stage 0 noted worked examples could move to Appendix B with reference back; that's the prune surface. |
| 15 | Event-Triggered Re-classification | 1,526 | -250 | 1,276 | Operational flow for class escalation triggered by external events (collision, claim, regulatory hold); opening dashcam framing repeats §Chain-of-Custody opening — collapse to single shared scenario. |
| — | References (Ch22 share) | ~470 | 0 | ~470 | Citations split per-section between Ch15 and Ch22; Ch22 keeps cites referenced from O sections (Shamir [6], Buterin [4], Argent [5], Sigstore [2], etc.). |
| **Subtotal** | | **16,210** | **−3,150** | **~13,060** | **⚠ Above UPF target of ≤12,000 by ~1,000 words.** Triggers FAILED-condition watch — see Risk section below. |

### Total post-prune

- **Ch15 (slimmed):** ~5,356 words ✓
- **Ch22 (Security Operations):** ~13,060 words ⚠ (1,060 over UPF target of 12,000)
- **Combined:** ~18,416 words (recovers ~3,750 words from current 22,165)

## Risk: Ch22 above the FAILED threshold

UPF FAILED-condition: "Ch22 lands above 12,000 words after prune → split into Ch22 (Key Lifecycle Operations: KCIR + Key-Loss Recovery + Forward Secrecy) + Ch23 (Endpoint + Collaborator Operations: Offline Revocation + Collaborator Revocation + Endpoint Compromise)."

PAO's read: my prune estimates are intentionally conservative. Aggressive pruning of §Key-Loss Recovery (currently estimated -1,400; could realistically reach -1,800 if the per-mechanism deployment-cost paragraphs collapse to a single comparison table) and §Chain-of-Custody (estimated -700; could reach -1,000 if all worked examples relocate to Appendix B) would land Ch22 at ~12,260 — close enough to the 12,000 threshold that an editorial round of close prose-prune over Phase 4 likely closes the gap without triggering Ch23 split.

**Recommendation:** **Do not pre-trigger the Ch22+Ch23 split.** Proceed to Phase 2 (skeleton) and Phase 3 (relocate) on the assumption Ch22 holds together as a single chapter; budget Phase 4 prune for the aggressive scenario; surface the kill-trigger only if Phase 4 actually overshoots. Splitting into Ch23 doubles the cross-reference work in Phase 5 and creates a 6-or-7-chapter Part V that loses the "Operational Concerns" framing's coherence.

If CO or XO want a more conservative posture, the alternate plan is to plan Ch22+Ch23 split *now* (parallel-author from Phase 2) and cleanly split the operational sections along Key Lifecycle vs. Endpoint+Collaborator lines from the start. PAO defers to whichever risk posture preferred.

## Footnotes

¹ **§17 Privacy-Aggregation classification.** This section sits structurally next to §Relay Trust Model (§16) and extends it. Opening paragraph reframes the architectural problem ("§Relay Trust Model named the self-hosted relay as the mitigation… It does not handle the *aggregation* problem"). The bulk specifies a property the relay must implement (differential privacy on metadata aggregates only) and the protocol scope. This is architectural specification, not event-response — classified A. The two readers of this section are (a) someone asking "what does the relay see, and what does it commit to not retaining?" — Ch15 question; (b) someone implementing the relay — Ch15+Ch22 question. Pairing with §Relay Trust Model in Ch15 serves both.

² **§9 Forward Secrecy classification.** The property *forward secrecy* is architectural; the post-compromise *recovery* it specifies is operational. Reading the section: 80% of the content is response framing ("when an adversary captures a session key today… within a session that an attacker has partially observed… the response runs"). Opening explicitly bridges from §Collaborator Revocation: "Collaborator revocation closed the question of what happens at a session's end. Forward secrecy and post-compromise security govern what happens within a session that an attacker has partially observed." The framing positions this as the next operational scenario, not a standalone architectural property. Classified O per UPF's read; PAO concurs.

## Status

- Phase 1 gate: PASS. Zero M-classified sections.
- Phase 2 (Yeoman creates `chapters/part-5-operational-concerns/ch22-security-operations.md` skeleton + manifest): unblocked.
- Phase 3 ordering recommendation (PAO directs): move sections in this order to keep cross-references resolvable: §5 Key Compromise IR → §6 Key-Loss Recovery → §7 Offline Revocation → §8 Collaborator Revocation → §9 Forward Secrecy → §11 Endpoint Compromise → §13 Chain-of-Custody → §15 Event-Triggered. (Roughly the order they currently appear in Ch15; preserves the narrative arc the chapter already established.)
- Phase 4 prune budget: -3,750 words across both chapters; FAILED-condition watch on Ch22 ≤12,000.
- Phase 5 cross-reference inventory: pending Phase 3 execution.

PAO ready to direct Phase 2 the moment Yeoman frees a window from audiobook generation.
