# Code-check report — 11 fleet management

**Stage:** code-check.
**Run:** 2026-04-27.
**Verdict:** PASS.

## Sunfish package references

| Namespace | Sites | Status |
|---|---|---|
| `Sunfish.Foundation.Fleet` | ~10+ (chapter-wide) | **NEW forward-looking.** Tracked in `docs/reference-implementation/sunfish-package-roadmap.md` (added this iteration). |
| `Sunfish.Kernel.Security` | multiple | **In canon.** |
| `Sunfish.Kernel.Sync` | 1+ | **In canon.** |
| `Sunfish.Foundation.LocalFirst` | 1 (comparison) | **In canon.** |
| `Sunfish.Foundation.Recovery` | 1 | **Forward-looking** (introduced by #48; tracked). |
| `Sunfish.Kernel.Audit` | 2 | **Forward-looking** (introduced by #48; tracked). |

HTML code-check annotation present at chapter start. All references are package-name only. Component / interface names appear only in code fences.

## Code snippets

Four fenced `csharp` code blocks in §21.2, §21.3, §21.4, §21.5 (provisioning, rotation, OTA, observability examples). All four marked `// illustrative — not runnable (Sunfish.Foundation.Fleet pre-1.0)`.

## Markers

| Type | Count | Notes |
|---|---|---|
| `<!-- TBD -->` | 0 | None. |
| `<!-- CLAIM: -->` | 0 | None. |
| `TBD` / `TODO` | 0 | None. |
| `<!-- voice-check: -->` | (see voice-check stage) | Outline §F notes opening hook anecdote candidates for human voice-pass. |

## Cross-reference resolution

- Chapter 19 §Code Signing and Notarization ✓
- Chapter 19 §Air-Gap Deployment ✓
- Chapter 19 §Admin Tooling for Revocation (referenced as "§Admin Tooling") ✓
- Chapter 11 §The UI Kernel (Four-Tier Layering) ✓
- Chapter 14 §Sync Daemon Protocol ✓
- Chapter 15 §Key Rotation and Revocation — **needs verification** (Ch15's §heading is "Key Compromise Incident Response" not "Key Rotation and Revocation"; the chapter draft references the latter framing. May need rewording.)
- Chapter 15 §Device and User Identity — **needs verification** (Ch15's actual sections are Threat Model, Four Defensive Layers, Key Hierarchy, Role Attestation Flow, etc. "§Device and User Identity" isn't a current section title. May need rewording.)
- Chapter 15 §Collaborator Revocation (extension #45) ✓ (just added)
- Chapter 17 §QR-Code Onboarding — **needs verification** (Ch17 may not have this exact section title)
- Extension #43 (performance contracts) ✓
- Extension #48 (recovery-event audit trail substrate) ✓

**Three cross-references flag for technical-review pass to verify section titles match Ch15 and Ch17 actual structure.** May require minor wording adjustment in the new chapter.

## Quality gate

Per loop-plan §5: code-check → technical-review.

- [x] All Sunfish package references validated; new `Sunfish.Foundation.Fleet` entry added to roadmap.
- [x] Code snippets marked illustrative.
- [x] No TBD markers.
- [x] Most cross-references resolve; 3 flagged for tech-review section-title verification.

Gate **passed**. Advance to technical-review.

## Items queued for technical-review

1. Verify Ch15 cross-references: "§Key Rotation and Revocation" and "§Device and User Identity" don't match current Ch15 H2 titles. Rewrite to point to actual Ch15 sections (likely §Key Compromise Incident Response and §Threat Model or §Layer 1 Encryption at Rest).
2. Verify Ch17 cross-reference: "§QR-Code Onboarding" — confirm this exact section exists in Ch17.
3. Reference [6] NIST SP 800-82 — included per outline §G but inline use is implicit (regulated-tier framing). Tech reviewer may pin to specific in-prose citation or mark for removal.
4. Verify all Apple/Google/Microsoft/AWS/Mender/Prometheus/HIPAA citations [1]-[11] for URL accuracy.
5. v13/v5 sourcing audit — fleet management is acknowledged as new architectural commitment; verify v13/v5 contain no fleet-management specification.
6. Confirm idempotent re-wrapping requirement in §21.3 — this is a kernel invariant the fleet layer relies on; the technical-review pass should note whether it's validated against the kernel's existing rotation implementation.

## Word count

Chapter body: ~6,579 words (target 6,500 ±10% = 5,850–7,150). Within band.

## Pending structural concerns

The chapter introduces a NEW Part V "Operational Concerns" that does not yet exist in the book's main structure files. Pending follow-up items (will be tracked in state.yaml; not blocking code-check):

1. `book-structure.md` — add Part V entry with Ch21 listing.
2. `ASSEMBLY.md` — deferred until #11 reaches `icm/approved`.
3. Part-divider file at `chapters/part-5-operational-concerns/README.md` (optional — match other parts' pattern if they have one).

These are document-structure tasks, not code-check concerns. Recommend handling them in the prose-review or post-prose-review stage when the chapter is closer to publication-ready.
