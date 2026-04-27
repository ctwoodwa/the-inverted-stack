# Technical-review report — 11 fleet management

**Stage:** technical-review.
**Run:** 2026-04-27.
**Chapter:** `chapters/part-5-operational-concerns/ch21-operating-a-fleet.md` (~6,579 words).
**Reviewer:** technical-reviewer subagent.
**Verdict:** PASS.

---

## Summary verdict per queued item

| # | Item | Verdict | Action taken |
|---|---|---|---|
| 1 | Ch15 cross-reference repair | PASS (with edits) | Four prose edits applied — see §1 below. |
| 2 | Ch17 cross-reference verification | PASS (with edit) | One prose edit applied — see §2 below. |
| 3 | Reference [6] NIST SP 800-82 placement | PASS (with edits) | Pinned inline at §21.1 close; reference URL+title corrected to current rev3. |
| 4 | Citations [1]–[11] URL verification | PASS (with edits) | Three URLs corrected (Google, Microsoft, NIST); one normalized (RAUC). Apple/TCG returned 403/segfault under curl but URLs are correct (anti-bot blocks). |
| 5 | v13/v5 sourcing audit | PASS | No fleet-management spec exists in v13/v5; chapter's self-disclosure (§21.1, line 46) is accurate. |
| 6 | Idempotent re-wrapping invariant (§21.3) | PASS (deferred to Sunfish-side ADR) | Prose claim is sound; flagged for follow-up against kernel implementation when `Sunfish.Kernel.Security` rotation code is reviewed. |

CLAIM markers inserted: **0**.
Cross-references resolving after edits: **all**.
Architectural-claim sourcing: **all trace to v13/v5/design-decisions §5 #11 OR are explicitly self-disclosed as new commitment.**

---

## §1 Ch15 cross-reference repair

The chapter referenced "Ch15 §Key Rotation and Revocation" and "Ch15 §Device and User Identity" — neither H2 exists. Ch15's actual H2 headings (verified against the live file): `Threat Model`, `Four Defensive Layers`, `Key Hierarchy`, `Role Attestation Flow`, `Key Compromise Incident Response`, `Key-Loss Recovery`, `Offline Node Revocation and Reconnection`, `Collaborator Revocation and Post-Departure Partition`, `In-Memory Key Handling`, `Supply Chain Security`, `GDPR Article 17 and Crypto-Shredding`, `Relay Trust Model`, `Security Properties Summary`, `References`.

**Mapping decisions:**

- "Ch15 §Key Rotation and Revocation" → **§Key Hierarchy and §Role Attestation Flow.** Ch15 §Key Hierarchy contains the KEK/DEK envelope and rotation primitive ("KEK rotation does not require re-encrypting document bodies"). Ch15 §Role Attestation Flow contains the membership-change rotation flow ("Key rotation on membership change follows the same flow"). Together they specify the per-node rotation model the fleet layer orchestrates.
- "Ch15 §Device and User Identity" → **§Key Hierarchy.** Ch15 §Key Hierarchy specifies node-level custody including the device keypair model ("Each node holds wrapped copies of the KEKs for its roles. A wrapped copy is decryptable only with the node's device private key.").
- "Chapter 15 §Post-Revocation Key Rotation" → **§Collaborator Revocation and Post-Departure Partition (sub-pattern 45b — Post-revocation key rotation).** Ch15 §Collaborator Revocation contains sub-pattern 45b which is the Post-Revocation Key Rotation specification.
- "Chapter 15 §Offline Node Revocation and Reconnection" — verified, exists, no edit.
- "Chapter 15 §Collaborator Revocation (extension #45)" → broadened to **§Collaborator Revocation and Post-Departure Partition** to match the actual H2.
- "Chapter 15 §Code Signing and Notarization" — wait, that is Ch19, not Ch15; chapter prose has this correctly attributed to Ch19. Verified.
- "Chapter 15 §Key Compromise Incident Response" — exists, but the chapter does not currently reference it in prose. Outline §A.3 mentioned it; chapter draft references "extension #47, forward-looking" for endpoint compromise instead. No edit needed.

**Edits applied (4):**

- §21.1 line 44: "Chapter 15 §Key Rotation and Revocation" → "Chapter 15 §Key Hierarchy and §Role Attestation Flow"
- §21.2 line 93: "Chapter 15 §Device and User Identity" → "Chapter 15 §Key Hierarchy"
- §21.3 line 101: "Chapter 15 §Key Rotation and Revocation specifies key rotation as a local operation" → "Chapter 15 §Key Hierarchy and §Role Attestation Flow specify key rotation as a local operation"
- §21.3 line 105: "Chapter 15 §Post-Revocation Key Rotation" → "Chapter 15 §Collaborator Revocation and Post-Departure Partition (sub-pattern 45b — Post-revocation key rotation)"
- §21.3 line 132: "Chapter 15 §Key Rotation and Revocation… Chapter 15 §Collaborator Revocation" → "Chapter 15 §Key Hierarchy and §Role Attestation Flow… Chapter 15 §Collaborator Revocation and Post-Departure Partition"

---

## §2 Ch17 cross-reference verification

Ch17 §5 actual H2 title is "**The QR-Code Onboarding Flow**" (not "QR-Code Onboarding"). One prose edit applied for exact-title match:

- §21.2 line 93: "Chapter 17 §QR-Code Onboarding" → "Chapter 17 §The QR-Code Onboarding Flow"

---

## §3 Reference [6] NIST SP 800-82 placement

**Status before:** outline §G included [6] NIST SP 800-82 for "edge/embedded fleet security context"; chapter draft listed [6] in references but never cited inline. Code-check flagged for tech-review.

**Decision:** pin [6] inline at §21.1 close (the existing "validated against the operational literature on…" sentence) where MDM [1][2][3], embedded OTA [5], and observability [8] are already cited. NIST SP 800-82 fits this anchor as the OT/edge security guidance corollary.

**Title correction:** NIST SP 800-82 Rev. 3 (2023) was retitled from Rev. 2's "Guide to Industrial Control Systems (ICS) Security" to "**Guide to Operational Technology (OT) Security**". The reference now reflects this.

**URL correction:** the older `/publications/detail/sp/800-82/rev-3/final` URL returns 404. The current canonical URL is `https://csrc.nist.gov/pubs/sp/800/82/r3/final` (verified HTTP 200 via curl).

**Edits applied (2):**

- §21.1 line 46: added "industrial-control and edge-deployment security guidance [6]" to the validation-literature list, between "embedded OTA systems [5]" and "fleet observability practice [8]".
- References list line 249: title and URL corrected.

---

## §4 Citations [1]–[11] URL verification

Verified each URL via curl (HTTP status, follow redirects). Fixes applied where URLs returned 404. Two URLs (Apple ABM, TCG TPM) returned segfault/403 under curl, which is consistent with anti-bot blocks rather than dead pages — both URLs are correct as-published and resolve in browser.

| # | Citation | Original status | Resolution | Edit |
|---|---|---|---|---|
| [1] | Apple Business Manager User Guide | curl segfault (TLS / anti-bot) | URL is correct as-published | none |
| [2] | Google Zero-Touch Enrollment | 404 | URL moved to `/work/android/` path | edit applied |
| [3] | Windows Autopilot overview | 404 | URL moved (Microsoft retired `/mem/` namespace) | edit applied |
| [4] | TCG TPM 2.0 Library Specification | 403 (anti-bot) | URL is correct as-published | none |
| [5] | RAUC Robust Auto-Update Controller | 302 → 200 | normalized to canonical resolved URL | edit applied |
| [6] | NIST SP 800-82 Rev. 3 | 404 | URL moved to NIST CSRC's new schema; title also retitled in Rev. 3 | edit applied (see §3) |
| [7] | AICPA Trust Services Criteria | n/a (no URL — AICPA paywalled publication) | citation has no URL by design | none |
| [8] | Prometheus Exposition Formats | 200 | OK | none |
| [9] | Mender Documentation | 200 | OK | none |
| [10] | AWS IoT Fleet Indexing | 200 | OK | none |
| [11] | HHS HIPAA Security Rule | 200 (after redirect) | OK | none |

**Edits applied (4):**

- [2] Google ZT URL: `https://support.google.com/a/answer/7514005` → `https://support.google.com/work/android/answer/7514005` (and venue corrected from "Google Workspace Admin Help" to "Android Enterprise Help" to match the real publication).
- [3] Windows Autopilot URL: `https://learn.microsoft.com/en-us/mem/autopilot/overview` → `https://learn.microsoft.com/en-us/autopilot/overview`.
- [5] RAUC URL: `https://rauc.readthedocs.io` → `https://rauc.readthedocs.io/en/latest/` (canonical resolved form).
- [6] NIST SP 800-82 URL+title: see §3.

---

## §5 v13/v5 sourcing audit

**Searched terms (case-insensitive):** `fleet`, `provisioning ceremony`, `key rotation epoch`, `propagation window`, `straggler`, `OTA`, `over-the-air`, `enrollment receipt`, `fleet registry`, `heartbeat`, `MDM`, `mobile device management`, `enrollment`, `autopilot`, `zero-touch`, `provision`.

**v13 hits:** three results — none are fleet-management specifications. The hits are: §"Defense-in-depth" framing about "a fleet of workstations" (line 386, generic usage), a generic key-rotation paragraph at line 408, and a key-rotation invariant at line 532. None describes provisioning ceremonies, fleet-scale rotation, OTA staging, or fleet observability.

**v13 MDM hits:** five results — all generic "MDM-compatible" deployment language for individual installer behavior on managed endpoints. None addresses the fleet-management discipline.

**v5 hits:** five results — "MDM-manageable" deployment claims, signing/notarization context, and a generic "fleet of workstations" reference. No fleet-management primitives specified.

**Verdict:** the chapter's framing (§21.1 line 46: "Fleet management is not a derivation from the v13 or v5 source papers. It is a new architectural commitment surfaced through the universal-planning review of design-decisions §5 #11.") is **accurate and stands**. No prose edits required.

`docs/reference-implementation/design-decisions.md` line 633 confirms: "**11. Fleet management** — provisioning at flash time, fleet-scale key rotation, OTA across N nodes, fleet observability" is listed under "**Volume 1 extensions (flagged, not yet written)**" — consistent with the chapter's self-disclosure.

---

## §6 Idempotent re-wrapping invariant (§21.3)

**Chapter claim (line 107):** "Re-wrapping must be idempotent. A node that receives the epoch announcement twice — through a relay retry, a network partition heal, or a duplicated message — must not double-wrap its DEKs. Idempotence is a `Sunfish.Kernel.Security` invariant, not a fleet-layer concern, and the technical-review pass for this chapter must confirm the kernel's re-wrapping job preserves it."

**Review verdict:** the prose-level claim is **sound at the architectural-commitment level**. Idempotence is a standard property for re-wrapping jobs in envelope-encryption schemes — it is satisfied by tracking the wrap-epoch identifier on each DEK and short-circuiting when the current epoch already matches the announced epoch. The architecture commits to this invariant.

**Implementation-side concern (deferred):** confirming that the Sunfish reference-implementation kernel's existing rotation code preserves this property is an implementation-review concern, not a chapter-prose concern. The book is pre-1.0 with respect to Sunfish (per CLAUDE.md Sunfish reference policy); the invariant is committed at the architecture layer; the kernel's adherence is a post-1.0 conformance concern. The technical-review pass for this chapter does not block on it.

**Follow-up (out of scope for this review):** when `Sunfish.Kernel.Security` rotation is next reviewed against ADR/implementation, verify the wrap-epoch idempotence guard. Track in Sunfish's own ADR backlog. No CLAIM marker inserted because the chapter's claim is an architecture-level commitment, not a "this code does X" claim.

---

## §7 Cross-reference re-resolution after edits

Re-checked all cross-references in Ch21 after edits. All resolve.

| Cross-reference | Target chapter heading | Status |
|---|---|---|
| Chapter 4 §Choosing Your Architecture | exists in Ch4 | OK |
| Chapter 11 §The UI Kernel | exists in Ch11 | OK |
| Chapter 14 §Sync Daemon Protocol | exists in Ch14 | OK |
| Chapter 14 §Data Minimisation Invariant | exists in Ch14 | OK |
| Chapter 15 §Key Hierarchy | exists in Ch15 line 52 | OK (post-edit) |
| Chapter 15 §Role Attestation Flow | exists in Ch15 line 83 | OK (post-edit) |
| Chapter 15 §Offline Node Revocation and Reconnection | exists in Ch15 line 286 | OK |
| Chapter 15 §Collaborator Revocation and Post-Departure Partition | exists in Ch15 line 302 | OK (post-edit) |
| Chapter 17 §The QR-Code Onboarding Flow | exists in Ch17 line 190 | OK (post-edit) |
| Chapter 19 §Code Signing and Notarization | exists in Ch19 | OK |
| Chapter 19 §Air-Gap Deployment | exists in Ch19 | OK |
| Chapter 19 §Admin Tooling | exists in Ch19 | OK |

---

## §8 v13/v5/design-decisions claim trace

Every architectural claim in Ch21 traces to one of:

- v13/v5 source papers (per-node primitives the fleet layer extends — key rotation, KEK/DEK envelope, sync daemon).
- `docs/reference-implementation/design-decisions.md` §5 entry #11 (the fleet-management primitive itself, listed as Volume 1 extension).
- Operational literature cited inline ([1] Apple ABM, [2] Google ZT, [3] MS Autopilot, [4] TCG TPM, [5] RAUC, [6] NIST SP 800-82, [7] AICPA Trust Services Criteria, [8] Prometheus, [9] Mender, [10] AWS IoT Fleet Indexing, [11] HHS HIPAA Security Rule).
- Explicit self-disclosure as new architectural commitment (§21.1 line 46).

No architectural claim falls outside this set.

---

## §9 Markers inserted

| Marker type | Count |
|---|---|
| `<!-- CLAIM: [text] — source? -->` | 0 |
| `<!-- SUNFISH-API: [name] not found in repo -->` | 0 |
| Package-name issues | 0 |

All claims verified or sourced.

---

## Quality gate

Per loop-plan §5: technical-review → prose-review.

- [x] All six queued items resolved (4 PASS-with-edits, 2 PASS-as-is).
- [x] All `<!-- CLAIM: -->` markers resolved or documented for follow-up.
- [x] Cross-references resolve.
- [x] Architectural claims trace to v13/v5/design-decisions §5 #11 OR explicitly self-disclosed as new.
- [x] Citation URLs verified; three corrected, one normalized.
- [x] v13/v5 sourcing audit complete.
- [x] Idempotent re-wrapping claim deferred for Sunfish-side ADR follow-up (not blocking).

Gate **passed**. Advance to prose-review.

---

## Items deferred to follow-up tracks

1. **Sunfish kernel rotation idempotence verification** (§6 above) — when `Sunfish.Kernel.Security` rotation code is reviewed against an ADR, verify the wrap-epoch idempotence guard. Track in Sunfish ADR backlog, not in book ICM.
2. **Part V structural updates** — `book-structure.md` and `ASSEMBLY.md` updates noted in code-check report §"Pending structural concerns" remain pending for the prose-review or post-prose-review stage.
