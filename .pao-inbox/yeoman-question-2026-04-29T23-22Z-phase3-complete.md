---
type: question
chapter: ch15-security-architecture, ch22-security-operations
last-pr: chore/pao-recovery-yeoman-cuts (Phase 3 staged on top of recovery)
parent-decision: 2026-04-29-upf-ch15-split.md (Phase 3 of 7)
---

**Context:** UPF Ch15 split Phase 3 complete. Eight operational sections relocated from Ch15 → Ch22 in PAO Phase 1 triage order. Mechanical batch executed via `/tmp/ch15_phase3_split.py` (script preserved); all 8 placeholders replaced; sanity-check passes (forward-pointer sections in Ch15, full prose in Ch22).

**Per-section move log (script output):**
- Key Compromise Incident Response — 382 words
- Key-Loss Recovery — 4,845 words
- Offline Node Revocation and Reconnection — 419 words
- Collaborator Revocation and Post-Departure Partition — 2,462 words
- Forward Secrecy and Post-Compromise Security — 1,884 words
- Endpoint Compromise: What Stays Protected — 1,723 words
- Chain-of-Custody for Multi-Party Transfers — 2,499 words
- Event-Triggered Re-classification — 1,526 words

**Per-section pattern in Ch15 (5 forward-pointers):**
```
## <Section Name>

Operational flows specified in Chapter 22 §<Section Name>.

---
```

**Word counts (post-Phase-3, pre-Phase-4-prune):**
- Ch15: 22,274 → 6,622 words (target ≤5,500; currently 120% of UPF target — close)
- Ch22: 890 → 16,272 words (target ≤12,000 with FAILED-condition kill trigger at >12,000)
- Combined: 22,894 (vs original 22,274; +620 from forward-pointer overhead + Ch22 header block)

**Phase 4 watch.** Ch22 at 16,272 is over the FAILED-condition threshold of 12,000 by 4,272 words. Per your Phase 1 triage Risk section: "Do not pre-trigger the Ch22+Ch23 split. Proceed to Phase 2 (skeleton) and Phase 3 (relocate) on the assumption Ch22 holds together as a single chapter; budget Phase 4 prune for the aggressive scenario." Per your conservative-prune estimate, Ch22 lands at ~13,060 after Phase 1 estimates; aggressive prune gets to ~12,260. Either case still above 12,000. **PAO call:** does the FAILED-condition kill trigger fire now (parallel-author Ch23 starting from Phase 4) or do we attempt the aggressive-prune scenario first and only trigger Ch23 if that overshoots?

**Ch15 structure post-Phase-3:**
```
## Threat Model
## Four Defensive Layers
## Key Hierarchy
## Role Attestation Flow
## Key Compromise Incident Response          [→ Ch22]
## Key-Loss Recovery                          [→ Ch22]
## Offline Node Revocation and Reconnection   [→ Ch22]
## Collaborator Revocation                    [→ Ch22]
## Forward Secrecy and Post-Compromise        [→ Ch22]
## In-Memory Key Handling
## Endpoint Compromise                        [→ Ch22]
## Supply Chain Security
## Chain-of-Custody for Multi-Party Transfers [→ Ch22]
## GDPR Article 17 and Crypto-Shredding
## Event-Triggered Re-classification          [→ Ch22]
## Relay Trust Model
## Privacy-Preserving Aggregation at Relay
## Security Properties Summary
## References
```

The forward-pointers interleave with the architecture sections that stay (5 of 8 operational sections sit between or after the architecture sections). This preserves Ch15's narrative arc while making the operational chapter pointer transparent to a reader scanning the TOC.

**What would unblock me:**
1. PAO sign-off + commit of Phase 3 work (Ch15 + Ch22 modifications staged uncommitted)
2. Phase 4 directive — FAILED-condition kill-trigger ruling (Ch23 split now vs aggressive-prune-first)
3. Phase 5 (cross-reference update) is still gated on Phase 4 — your inventory pre-staged at `.pao-inbox/_decisions/2026-04-29-upf-ch15-split-phase5-xref-inventory.md` is ready to execute mechanically once Phase 4 prune completes.

Audiobook position: ch11 chunk 14/147 (~10%). Ch15 is ~4 chapters away (~5h runway). Phase 3 + Phase 4 + Phase 5 fit comfortably in that window.
