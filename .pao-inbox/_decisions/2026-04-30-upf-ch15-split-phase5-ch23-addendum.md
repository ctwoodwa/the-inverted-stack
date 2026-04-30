---
type: upf-phase-5-amendment
date: 2026-04-30
author: PAO
audience: Yeoman (Phase 5 executor), CO (visibility)
parent-decision: 2026-04-29-upf-ch15-split.md
parent-inventory: 2026-04-29-upf-ch15-split-phase5-xref-inventory.md
phase: 5 (amended)
status: amendment — supersedes Rule R-O routing in original inventory
---

# UPF Ch15 Split — Phase 5 Cross-Reference Inventory Addendum (Ch22/Ch23 routing)

## TL;DR

Original Phase 5 inventory (`2026-04-29-upf-ch15-split-phase5-xref-inventory.md`)
assumed all operational sections would land in Ch22. Phase 4 kill-trigger fired;
Ch22 split into Ch22 (Key Lifecycle Operations) + Ch23 (Endpoint, Collaborator,
and Custody Operations). **Rule R-O is now Rule R-O22 and Rule R-O23.**

## New routing rules

### Rule R-O22 — references that redirect to Ch22 (Key Lifecycle Operations)

Sections that landed in Ch22 (Key Lifecycle Operations) per the Phase 4 split:

| `§<section name>` cited | Redirects to |
|---|---|
| `§Key Compromise Incident Response` | Ch22 |
| `§Key-Loss Recovery` (incl. sub-patterns 48a–48f, "Boundaries and Operator Mitigations") | Ch22 |
| `§Forward Secrecy and Post-Compromise Security` (incl. sub-pattern 46e) | Ch22 |

### Rule R-O23 — references that redirect to Ch23 (Endpoint + Collaborator + Custody Operations)

Sections that landed in Ch23 per the Phase 4 split:

| `§<section name>` cited | Redirects to |
|---|---|
| `§Offline Node Revocation and Reconnection` | Ch23 |
| `§Collaborator Revocation and Post-Departure Partition` (incl. sub-patterns 45a–45f) | Ch23 |
| `§Endpoint Compromise: What Stays Protected` (incl. sub-patterns 47a, 47b) | Ch23 |
| `§Chain-of-Custody for Multi-Party Transfers` | Ch23 |
| `§Event-Triggered Re-classification` (incl. sub-patterns 10a–10d) | Ch23 |

### Rule R-A unchanged

References to architectural sections still stay at Ch15 (see original inventory).

### Rule R-G unchanged

Generic "Chapter 15" references (no `§` qualifier) still need context-driven
classification per the original inventory's Rule R-G table.

### Rule R-N unchanged

Numeric `§` references (e.g., `Ch15 §7`) still convert to named-section refs.

### Rule R-F amendment

Appendix F regulatory chapter ranges that referenced "Ch13–Ch15, Ch22"
under the original Phase 5 inventory now need triple-target consideration:
"Ch13–Ch15, Ch22, Ch23" for regulations that touch both lifecycle operations
and endpoint/custody operations. Per-framework triage:

- GDPR: architectural compliance (Ch15) + erasure operational (Ch22 KLR audit-trail; Ch23 not directly relevant) → **Ch13–Ch15, Ch22**
- HIPAA: architectural (Ch15) + endpoint compromise + chain-of-custody for clinical handoffs → **Ch13–Ch15, Ch23** (HIPAA Security Rule applies to endpoints; clinical-handoff custody)
- DPDP / LGPD / DIFC / POPIA: erasure + cross-border + endpoint controls → **Ch13–Ch15, Ch22, Ch23** (all three apply)
- Financial-services regs (RBI, 242-FZ): localization + audit-trail + endpoint controls → **Ch13–Ch15, Ch22, Ch23**

Phase 5 execution adds Ch22 and Ch23 as appropriate per regulation. Default conservative posture: include both Ch22 and Ch23 unless the framework demonstrably touches only key-lifecycle (rare) or only endpoint+collaborator+custody (also rare).

## Updated per-file disposition

The original inventory's per-file analysis stands; redirect targets refine:

**`ch20-ux-sync-conflict.md` (14 refs):**
- §Key-Loss Recovery refs (5) → Ch22 (was Ch22; unchanged)
- §Collaborator Revocation refs (3) → **Ch23** (was Ch22; updated)
- §Event-Triggered Re-classification refs (3) → **Ch23** (was Ch22; updated)
- KCIR ref + 2 architectural refs → Ch22 + Ch15 (unchanged)

**`appendix-b-threat-model-worksheets.md` (9 refs):**
- §Endpoint Compromise refs → **Ch23** (was Ch22)
- §Chain-of-Custody refs → **Ch23** (was Ch22)
- §Collaborator Revocation refs (the broadcast mechanism reused by remote wipe) → **Ch23**
- §In-Memory + §Threat Model refs → Ch15 (unchanged)
- KCIR refs → Ch22 (unchanged)

**`ch21-operating-a-fleet.md` (8 refs):**
- §Key Hierarchy + §Role Attestation refs → Ch15 (unchanged)
- §Collaborator Revocation refs → **Ch23** (was Ch22)
- §Offline Revocation refs → **Ch23** (was Ch22)

**`ch16-persistence-beyond-the-node.md` (8 refs):**
- §Event-Triggered Re-classification refs → **Ch23** (was Ch22)
- §GDPR Article 17 + §Crypto-Shredding refs → Ch15 (unchanged)

**`appendix-g-glossary.md` (12 refs):**
- HSM, TPM, Endpoint Compromise refs → **Ch23** (was Ch22)
- Other Specified-in entries → Ch15 (unchanged)

**`appendix-f-regulatory-coverage.md` (14 refs):**
- Per Rule R-F amendment above; per-framework triage required during execution.

## Phase 5 execution sequencing

The original inventory's 7-step execution sequence stands, with one substitution:

1. `grep -rn -E "(Ch\.? *15|Chapter 15|chapter 15)" chapters/` → confirm hit count.
2. **Apply Rule R-A + R-O22 + R-O23 + R-N** (R-O is now two rules).
3. Apply Rule R-G to generic refs on context-read basis.
4. Apply Rule R-F + R-S amendments.
5. `grep -E "Ch ?15 §[0-9]" chapters/` → verify zero numeric §refs.
6. `grep -E "Ch15 §<each O22-section name>" chapters/` AND `grep -E "Ch15 §<each O23-section name>" chapters/` — verify zero stale O-section refs to Ch15.
7. `make lint` → zero broken refs in build.
8. Spot-check Ch20 (heaviest cross-ref file) end-to-end.

Estimated execution time: still 2–3h mechanical + 1h spot-check. The split into R-O22 vs R-O23 doesn't materially change the execution shape; the redirect rule is a per-section lookup either way.

## Status

- Phase 5 inventory amended for Ch22/Ch23 routing: COMPLETE.
- Phase 5 execution: still pending (was pending Phase 3; Phase 3 + Ch23 split now complete; ready to execute).
- Recommended sequencing: execute Phase 5 redirects in a follow-up PR; PAO directs, applies via mechanical pass + Yeoman spot-check on Ch20.

---

**End of amendment.** Original inventory at `.pao-inbox/_decisions/2026-04-29-upf-ch15-split-phase5-xref-inventory.md` remains canonical for everything other than R-O routing.
