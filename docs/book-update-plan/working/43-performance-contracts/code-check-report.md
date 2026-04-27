# Code-check report — 43 performance contracts

**Stage:** code-check (ICM stage 3).
**Run:** iter-0012, 2026-04-27.
**Verdict:** PASS.

---

## Scope

Two new sections were drafted and inserted in iter-0011:

- `chapters/part-3-reference-architecture/ch11-node-architecture.md` §"Performance Contracts and Main-Thread Isolation" (~1,490 words, between §Sunfish Package Map and the reference list)
- `chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md` §"Performance Budgets and Progressive Degradation" (~1,005 words, between §The First-Run Experience and §Key-Loss Recovery UX)

Code-check verifies: Sunfish package references against the canonical Sunfish package list, no class APIs / method signatures appear in prose, all code snippets marked illustrative, no `<!-- TBD -->` / placeholder markers remain, all cross-reference targets resolve.

---

## Sunfish package references in the new sections

| Namespace | Sites in new sections | Canon status |
|---|---|---|
| `Sunfish.Kernel.Performance` | 6 (Ch11: 5; Ch20: 1) | **Forward-looking.** NEW for this extension. Tracked in `docs/reference-implementation/sunfish-package-roadmap.md`. |
| `Sunfish.Kernel.Crdt` | 1 (Ch11) | **In canon.** `ICrdtEngine` ownership. |
| `Sunfish.UIAdapters.Blazor` | 2 (Ch11: 1; Ch20: 1) | **In canon.** Hosts `SunfishMergeProgressIndicator` (NEW pre-1.0 component). |
| `Sunfish.Foundation` | 1 (Ch11) | **In canon.** UI-layer notification path. |

All references are package-name only. No class APIs in prose. No method signatures in prose.

## Pre-1.0 component / interface names introduced

| Name | Owner namespace | Appears in |
|---|---|---|
| `IProgressiveDegradation` | `Sunfish.Kernel.Performance` (forward-looking) | Ch11 §Sub-pattern 43c; Ch20 §Progressive-degradation UX patterns |
| `PerformanceBudgetValidator` | `Sunfish.Kernel.Performance` (forward-looking) | Ch11 §Sub-pattern 43d; Ch11 §Sub-pattern 43e |
| `PerformanceClass` | `Sunfish.Kernel.Performance` (forward-looking) | Ch11 §Sub-pattern 43d (in code fence) |
| `SunfishMergeProgressIndicator` | `Sunfish.UIAdapters.Blazor` (in canon; new component) | Ch20 §Progressive-degradation UX patterns |
| `PerformanceDegraded` | `Sunfish.Foundation.SyncState` enum sub-state (existing enum, new value) | Ch11 §FAILED conditions; Ch20 §Quality-of-service indicators |

All five names appear in code fences explicitly marked illustrative. No use in prose claims a method signature beyond what the book specifies as the architectural commitment.

## Forward-looking namespace handling

Per the outline §C requirement and the loop-plan §5 quality gate, the forward-looking namespace `Sunfish.Kernel.Performance` is annotated:

- **Ch11 §Performance Contracts:** HTML-comment annotation at section start (after the H2) listing the forward-looking namespace, the new pre-1.0 component/interface names, and the in-canon namespaces also referenced.
- **Ch20 §Performance Budgets and Progressive Degradation:** identical HTML-comment annotation pattern.

Same handling as `Sunfish.Foundation.Recovery` and `Sunfish.Kernel.Audit` in extension #48. The annotations are reviewer-visible (HTML comments) and reader-invisible (no prose intrusion).

The namespace is also tracked in the new authoritative roadmap document: `docs/reference-implementation/sunfish-package-roadmap.md` (added in commit `b8f302c`). Sunfish-side mirror at `C:/Projects/Sunfish/docs/specifications/inverted-stack-package-roadmap.md` (placement managed separately by the book maintainer outside this loop).

## Code snippets

Two fenced code blocks present in the new sections, both marked illustrative:

| Location | Content | Marker |
|---|---|---|
| Ch11 §Sub-pattern 43d | C# `AddSunfishPerformanceContracts` DI extension example | `// illustrative — not runnable (Sunfish.Kernel.Performance pre-1.0)` |
| Ch20 §Progressive-degradation UX patterns | Razor `<SunfishMergeProgressIndicator>` wiring | `// Illustrative — not runnable (pre-1.0 API)` |
| Ch20 §Quality-of-service indicators | C# `SyncState` enum extension showing `PerformanceDegraded` | `// Illustrative — not runnable (pre-1.0 API)` |

Three code fences total (one in Ch11, two in Ch20). All three carry the illustrative marker per the Sunfish reference policy.

## Markers and placeholders

| Marker type | Result |
|---|---|
| `<!-- TBD -->` | None found. |
| `TODO` | None found. |
| `expand here` | None found. |
| `placeholder` | None found. |
| `<!-- CLAIM: -->` | None inserted by draft. Two claims (Yjs 100k-merge complexity, Linear 60fps engineering blog) are attributed via citation [4] and [5] respectively, with the technical-review stage flagged to pin the specific URLs. This is a deliberate choice — citation-attributed claims rather than CLAIM markers in prose. |

## Cross-reference integrity

Cross-references introduced by iter-0011, verified against current chapter state:

| From | To | Status |
|---|---|---|
| Ch11 §Performance Contracts | Ch11 §Kernel Responsibilities | ✓ exists at Ch11:43 |
| Ch11 §Performance Contracts | Ch12 (CRDT engine architecture) | ✓ chapter exists |
| Ch11 §Performance Contracts | Ch20 §Performance Budgets and Progressive Degradation | ✓ exists (just added in iter-0011) |
| Ch11 §Performance Contracts | Ch11 §The UI Kernel: Four-Tier Layering | ✓ exists at Ch11:106 |
| Ch20 §Performance Budgets | Ch11 §Performance Contracts | ✓ exists (just added in iter-0011) |
| Ch20 §Performance Budgets | Ch20 §The Three Always-Visible Indicators | ✓ exists at Ch20:20 |
| Ch20 §Performance Budgets | Ch20 §The Conflict Inbox and Bulk Resolution | ✓ exists at Ch20:108 |
| Ch20 §Performance Budgets | Ch19 §Operator Observability | **broken — fixed in this iteration** |

**Cross-reference fix applied this iteration:**

The original draft cross-referenced "Ch19 §Operator Observability" — a section that does not exist. Ch19's H2 sections are: Procurement Conversation, Build and Packaging, Code Signing and Notarization, MDM Deployment, SBOM Generation and CVE Response, Admin Tooling for Revocation, Air-Gap Deployment, The Operational Runbook Minimum, Putting It Together. The closest match for "the enterprise telemetry path that consumes operator-facing budget violation telemetry" is §The Operational Runbook Minimum (line 382) — operational concerns naturally land in the runbook section.

Edit applied at Ch20 §Performance budget violation surfacing closing sentence:

  Was: "Ch19 §Operator Observability for the enterprise telemetry path."
  Now: "Ch19 §The Operational Runbook Minimum for the enterprise telemetry path that consumes it."

This is a minor cross-reference fix, not a substantive edit. The architectural commitment (operator-facing budget telemetry feeds the enterprise observability stack) is unchanged; only the named target section now resolves.

## Quality gate — code-check → technical-review

Per loop-plan §5:

- [x] All Sunfish package references validated — three classified, one annotated as forward-looking and tracked in the roadmap, three verified in canon.
- [x] Code snippets marked illustrative — three code fences, all marked `// illustrative — not runnable` or `// Illustrative — not runnable`.
- [x] No `<!-- TBD -->` markers — verified.
- [x] All cross-reference targets resolve (one broken reference fixed this iteration; six others verified).

Gate **passed**. Advance to technical-review.

---

## Findings logged for technical-review (next stage)

The technical-review stage handles substantive accuracy. The following items are queued for that pass:

1. **Yjs 100k-operation merge complexity claim ([4]).** Citation currently points to the Yjs documentation root. Technical reviewer pins the specific page or benchmark that documents the multi-second merge characteristic. If the documented figure differs from "multiple seconds on commodity hardware," the prose adjusts.
2. **Linear 60fps engineering blog claim ([5]).** Citation currently points to the Linear engineering blog root. Technical reviewer pins the specific post that articulates the 60fps-as-hard-constraint commitment. If no such post is publicly indexable, the technical reviewer either finds an alternative public source for the claim or rewords the prose.
3. **Web Vitals INP threshold ([6]).** Verify ≤200ms = "good" is current per Web Vitals documentation. INP replaced FID in March 2024; confirm thresholds have not been revised since.
4. **Apple HIG 16ms frame-budget claim ([8]).** Verify Apple's Human Interface Guidelines explicitly state 16ms or that 16ms is derivable from the documented 60fps target. The current citation is the HIG root; technical reviewer pins the specific section.
5. **Replicache "optimistic local state always current" framing ([7]).** Verify the paraphrase is faithful to Replicache's documentation framing. The current citation is the Replicache documentation root.
6. **Per-deployment-class budget table math (§Sub-pattern 43e):** verify the 8ms interactive budget reasoning (one sub-frame of headroom at 120fps, where one frame is 8.33ms). Confirm the math is stated accurately.
7. **Trace every architectural claim to v13/v5 source papers OR mark as new architectural commitment.** Performance contracts are explicitly NEW (acknowledged in the closing paragraph of the new section: "Performance contracts are a primitive surfaced through architectural review, not derived from the v13 or v5 source papers directly. The contract above commits the architecture to a specification-level guarantee that the source papers framed as a desirable property; the framework-level enforcement, the budget table, and the kill trigger are new architectural commitments specific to this volume."). Technical reviewer confirms this self-disclosure is accurate and that no other architectural claims silently assume v13/v5 backing.
