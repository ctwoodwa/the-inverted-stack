---
type: editorial-review
chapter: ch19-shipping-to-enterprise
date: 2026-04-30
author: PAO
audience: Yeoman (executor), CO (visibility)
status: review — light compression candidate; recommend ship-as-is or modest prune
target-reduction: 5,019 → 3,500 (target = 143% currently); modest compression yields ~400-500 words
---

# Ch19 (Shipping to Enterprise) — Compression Review

## TL;DR

Ch19 is at 143% of target — the **closest to target of any remaining compressible chapter**. Voice-passed, no extension pending. PAO read: ship-as-is is defensible (Part IV tutorial chapters tolerate +30-50% bloat for completeness; this is exactly that). A light editorial prune would recover ~400-500 words; that's the upper bound. No structural surgery needed.

## Section inventory

| § | Section | Words | Class | Cut estimate |
|---:|---|---:|---|---:|
| 1 | The Procurement Conversation | 311 | tight | 0 |
| 2 | Build and Packaging | 274 | tight | 0 |
| 3 | Code Signing and Notarization | 390 | tight | -50 |
| 4 | MDM Deployment | 944 | mild redundancy across Intune + Jamf | -150 |
| 5 | SBOM Generation and CVE Response | 476 | tight | 0 |
| 6 | Admin Tooling for Revocation | 297 | tight | 0 |
| 7 | **Air-Gap Deployment** | **1,233** | longest section; detailed scenarios | -200 |
| 8 | The Operational Runbook Minimum | 831 | three runbooks; could collapse to bullet form | -100 |
| 9 | Putting It Together | 133 | summary | 0 |
| **Total** | | **5,019** | | **-500** |

**After cuts:** ~4,520 words (129% of target). Within Part IV tolerance.

## Cut proposals

### Cut 1 — §Air-Gap Deployment (-200 words)

§Air-Gap Deployment is the chapter's longest section at 1,233 words. The opening 3-posture comparison table (connected / proxied / air-gap strict) is well-pitched. The mid-section detailed deployment instructions across the three postures contain some procedural redundancy — internal update server setup repeats across the proxied and air-gap-strict scenarios. Collapse to "internal update server (same setup for proxied and air-gap-strict modes; differences only at the endpoint reachability boundary)."

### Cut 2 — §MDM Deployment (-150 words)

The Intune and Jamf sub-sections describe similar pre-configuration steps (signing key trust anchors, MSI/PKG silent-install flags, post-install verification) using parallel structure. A consolidated "MDM-agnostic deployment steps" subsection followed by Intune-specific and Jamf-specific deltas would tighten the prose without losing detail.

### Cut 3 — §The Operational Runbook Minimum (-100 words)

The three runbooks (node deprovisioning, key compromise IR, schema-epoch update) get full prose treatment. Convert each runbook to a bullet-form checklist with 5-7 steps; keep narrative for the 1-2 most critical decision points only. Saves prose churn; readers prefer checklist format for runbooks anyway.

### Cut 4 — §Code Signing (-50 words)

Light tightening of the macOS notarization step descriptions; the technical content stays.

## What PAO is NOT proposing

- **§The Procurement Conversation, §Build and Packaging, §SBOM, §Admin Tooling for Revocation, §Putting It Together** — all tight; cuts would weaken the chapter.
- **No structural reorganization.** The chapter's narrative arc (procurement → packaging → signing → MDM → SBOM → admin tooling → air-gap → runbooks → checklist) is well-pitched for the enterprise IT reader who is the chapter's audience.

## Recommended outcome

**Ship-as-is is defensible.** 143% of target is within Part IV's tolerance band for tutorial chapters. If author wants to recover 500 words for the broader compression budget, Cuts 1–4 yield that without harming reader experience.

PAO does not recommend pre-applying these cuts via mechanical pass; they involve editorial judgment about how dense the procedural detail should be. Yeoman + CO call.

---

**End of review.** Awaiting Yeoman handoff window or author decision to ship-as-is.
