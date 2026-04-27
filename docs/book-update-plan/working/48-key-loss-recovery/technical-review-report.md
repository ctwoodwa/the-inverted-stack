# Technical-Review Report — #48 Key-Loss Recovery
**Stage:** technical-review (ICM stage 4).
**Run:** iter-0004, 2026-04-26.
**Scope:** Ch15 §"Key-Loss Recovery" (~2,050 words) + Ch20 §"Key-Loss Recovery UX" (~1,040 words).
**Source materials consulted:** v13 §11, v5, design-decisions §5 #48, outline §D, code-check-report.md.

---

## Item 1 — CLAIM Marker: Biometric Template Non-Exportability

**Verdict: PASS-with-edit.**

The `<!-- CLAIM: ... -->` marker at Ch15 line 167 (biometric-derived secondary key subsection) asserted that Apple Secure Enclave, Pixel Titan M, and Windows Pluton never export the raw biometric template and only output derived keying material. Verification:

- **Apple Secure Enclave:** Confirmed against Apple Platform Security [7]. The Secure Enclave processes Touch ID and Face ID data and exposes only match results and derived cryptographic output to the application processor. Raw biometric templates are never accessible to software running outside the Secure Enclave. The architectural guarantee is explicitly documented.

- **Pixel Titan M:** Consistent with Google's published Titan M security architecture. Biometric matching executes within the Titan M's trusted execution environment; the output crossing the trust boundary is a cryptographic derived value, not the template. The claim holds.

- **Windows Pluton:** Accurate in substance, with a precision note. Windows Hello biometric templates reside in the Windows Hello container, which the TPM (or Pluton processor on Pluton-equipped devices) protects. Pluton is Microsoft's security processor replacement for the discrete TPM, and on Pluton-equipped hardware it fulfils the same biometric-protection role. Template extraction is not available through any documented Windows API. The prose says "the biometric template never leaves the enclave" which is accurate for all three implementations. Pluton-specific caution: not all Windows devices have Pluton (it ships on newer AMD/Intel/Qualcomm platforms from ~2022 onward); the prose is technically accurate for Pluton-equipped devices and for the Windows Hello/TPM architecture on older devices, but Pluton is the aspirational platform, not universal. This is not a factual error — it is a precision note appropriate for a practitioner audience — and the prose does not assert universality.

**Edit made:** The `<!-- CLAIM: ... -->` marker was replaced with a `<!-- technical-review: ... -->` comment documenting the verification result and its basis. The comment is reviewer-visible and reader-invisible. No prose change was required — the claim as written is accurate and the citation [7] is already present in the surrounding prose.

**File:line:** `chapters/part-3-reference-architecture/ch15-security-architecture.md`, line 167.

---

## Item 2 — Shamir Threshold Logic

**Verdict: PASS.**

Ch15 §"Multi-sig social recovery" (line 137) states: "A threshold of 3-of-5 tolerates the simultaneous unavailability of two trustees; a threshold of 2-of-3 is appropriate for smaller trust networks."

Verified against Shamir, "How to share a secret," *Communications of the ACM*, vol. 22, no. 11, pp. 612–613, Nov. 1979 [6]:

- Shamir's scheme with threshold *t* and *n* shares: any *t* shares reconstruct the secret; fewer than *t* shares reveal nothing. Therefore 3-of-5 tolerates n − t = 5 − 3 = 2 simultaneous absences. The claim "tolerates the simultaneous unavailability of two trustees" is arithmetically correct.
- "2-of-3 is appropriate for smaller trust networks" — a valid statement. With n=3 and t=2, only one trustee can be absent. The tradeoff (less fault tolerance, lower collusion risk) is implicit in the comparison and consistent with standard Shamir usage.

No edit required.

---

## Item 3 — Time-Lock Attack Model Honesty

**Verdict: PASS.**

The §"Timed recovery with grace period" subsection (lines 176–181) and the §"Threat Model" subsection (lines 191–205) were reviewed for honest framing.

The prose correctly distinguishes between "raising the cost" and "defeating" the attack:

- Line 177: "An adversary who can submit a recovery claim and also suppress the original holder's notifications for fourteen days has a substantially harder problem than an adversary who can complete recovery in seconds." — Honest. Claims raised cost, not impossibility.
- Lines 178–179: "The attacker who controls the recovery initiation path still must also control every notification channel simultaneously, for the duration of the grace period, without the holder noticing." — Accurate threat-model boundary.
- Lines 204–205 (Honest limitation): "no recovery primitive defeats a sufficiently patient adversary with simultaneous control of every recovery channel. The architecture bounds the attack cost. It does not bound it to infinity." — Explicit and honest.

The outline §D asked: "is 30 days actually defeasible by a patient adversary with control of all notification channels?" The answer is yes, and the prose says so directly. The architecture does not claim total defense; it claims bounded cost increase. This framing is verified as accurate and not over-claiming.

No edit required.

---

## Item 4 — Argon2id Parameters

**Verdict: PASS.**

Ch15 §"Paper-key fallback" (line 157) states: "The phrase derives the root recovery seed through Argon2id (see §Key Hierarchy for the regulated-tier parameters: memory cost 128 MiB, iteration count 4, parallelism 4)."

Ch15 §Key Hierarchy (line 75) states: "Regulated-industry deployments configure the high-security tier: memory cost 128 MiB, iteration count 4, parallelism 4."

The two values match exactly. The paper-key fallback correctly cites and links to the regulated-tier parameters in §Key Hierarchy.

Cross-check: the standard tier in §Key Hierarchy is "memory cost 64 MiB, iteration count 3, parallelism 4." The paper-key fallback correctly uses the regulated tier (128 MiB / 4 / 4), not the standard tier, which is consistent with the design intent that paper keys are a fallback for deployments where the higher security cost is justified.

No edit required.

---

## Item 5 — Citation Metadata

**Verdict: PASS with one annotation.**

All four new IEEE citations verified:

**[4] Buterin 2021**
`V. Buterin, "Why we need wide adoption of social recovery wallets," *vitalik.ca*, Jan. 2021. [Online]. Available: https://vitalik.ca/general/2021/01/11/recovery.html`

The URL path encodes the date (2021/01/11), confirming January 2021 publication. Venue is vitalik.ca (Vitalik Buterin's personal blog). The IEEE citation renders this correctly as an online source. VERIFIED.

**[5] Argent 2020**
`Argent, "Argent Smart Wallet Specification," *github.com/argentlabs*, 2020. [Online]. Available: https://github.com/argentlabs/argent-contracts/blob/develop/specifications/specifications.pdf`

The year 2020 is the approximate initial publication year of the Argent v1 specification. The URL points to the `develop` branch, which means the linked content can change as the repository evolves. This is a known limitation of GitHub blob URLs pointing to mutable branches. For IEEE citation stability, the URL should ideally point to a commit-SHA or a tagged release. However, since the Argent specification is used to document the pattern's practical architecture rather than a specific version, this is acceptable given the book's practitioner audience. The design-decisions §5 #48 lists "Argent wallet social recovery" without a specific year. No factual error; annotation: URL points to mutable branch.

**[6] Shamir 1979**
`A. Shamir, "How to share a secret," *Communications of the ACM*, vol. 22, no. 11, pp. 612–613, Nov. 1979.`

This is the canonical citation for the original Shamir secret-sharing paper. Journal, volume, number, and pages are correct per the published record. VERIFIED.

**[7] Apple Platform Security 2024**
`Apple Inc., "Apple Platform Security," May 2024. [Online]. Available: https://support.apple.com/guide/security/welcome/web`

Apple Platform Security is a living document with a date stamp on each revision. "May 2024" is a valid point-in-time citation for a web source. The URL is Apple's stable canonical entry point for the guide. VERIFIED.

No edits required. Annotation on [5] noted above — not a factual error, does not require a chapter edit.

---

## Item 6 — Architectural Claims Trace to v13/v5 or Design-Decisions §5 #48

**Verdict: PASS.**

Review of all architectural claims in both new sections against v13 §11, v5, and design-decisions §5 #48:

**Claims sourced in v13 §11:**
- Four defensive layers (encryption at rest, field-level encryption, stream-level data minimization, circuit breaker) — v13 §11.2. The key-loss recovery section cross-references these without re-introducing them. ✓
- P7 ownership property framing — v13 §4 (properties), referenced as established context. ✓
- Argon2id for key derivation — v13 §11.2 Layer 1 mentions Argon2id (without specific parameters; parameters are Ch15 §Key Hierarchy's own spec). ✓
- KEK/DEK envelope structure — v13 §11.2 Layer 2. ✓
- Audit trail as signed log — v13 §11.2 Layer 4 (quarantine reviewed and logged). ✓

**Claims sourced in design-decisions §5 #48:**
All six sub-patterns are explicitly listed in #48 with their cryptographic constructions:
- 48a multi-sig social recovery (Shamir threshold, time-lock) ✓
- 48b custodian-held backup key (institutional, attestation policy) ✓
- 48c paper-key fallback (BIP-39 mnemonic, Argon2id derivation) ✓
- 48d biometric-derived secondary key (secure enclave, derived key output) ✓
- 48e timed recovery with grace period (7–30 days, composable) ✓
- 48f recovery-event audit trail (signed log entries, legal artifact) ✓

**Claims that are new commitments, not in v13/v5:**
- Specific grace period defaults (7 days for SMB, 14 days for consumer, 30 days for regulated) — not in v13/v5. These are consistent with design-decisions §5 #48 ("7-30 days" range) and the deployment-class table in the outline (§A.4). Authorized as new commitment. ✓
- BIP-39 as the specific mnemonic standard — not in v13/v5. Design-decisions #48c cites "classic crypto-wallet pattern" without naming BIP-39 specifically. BIP-39 is the de facto standard for seed-phrase mnemonics; the claim is accurate. The outline §A.2.3 explicitly mentions "BIP-39-style mnemonic phrase." Authorized. ✓
- Deployment-class table (consumer/SMB/regulated) — not in v13/v5. Outline §A.4 specifies this table as a new commitment for this section. Authorized. ✓

**Claims not found in v13, v5, or design-decisions §5 #48:**
None identified. All claims are sourced or explicitly authorized as new commitments by the outline.

No new `<!-- CLAIM: source? -->` markers were added.

---

## Item 7 — Threat-Model Honesty

**Verdict: PASS.**

The §"Threat Model — Recovery as Attack Vector" subsection (Ch15, lines 191–205) lists four attack patterns. Each was reviewed for over-claiming:

**Trustee compromise:** "Recovery fails when *t* trustees are simultaneously compromised. The architecture cannot defend against this outcome; it can only require that *t* is chosen large enough that simultaneous compromise is costly." — Explicit bound. Does not claim to defeat it. PASS.

**Custodian coercion:** "The custodian's release conditions are the gate; once those conditions are met, the architecture provides no further defense." — Explicit bound. PASS.

**Forged loss claim:** "Grace period and multi-channel notification give the original holder a dispute window. Trustee co-signing on completion requires the adversary to also compromise the trustees." — States what the mitigation does, not that it is absolute. PASS.

**Coerced recovery:** "No cryptographic mechanism defeats physical coercion. The architectural mitigation is to ensure that no single coerced action completes the recovery flow... That combination raises the cost of coercion substantially. It does not eliminate it." — Explicit. PASS.

**Honest limitation paragraph (lines 204–205):** "no recovery primitive defeats a sufficiently patient adversary with simultaneous control of every recovery channel. The architecture bounds the attack cost. It does not bound it to infinity." — Correct, direct, and honest.

No edit required.

---

## Summary: CLAIM Markers

| Status | Location | Action |
|---|---|---|
| Resolved (removed) | Ch15 line 167 — biometric template non-exportability | CLAIM marker replaced with `<!-- technical-review: verified -->` comment |
| None added | Both new sections | No new unverifiable claims identified |

Zero `<!-- CLAIM: source? -->` markers remain open in either new section.

---

## Consolidated Findings

| Item | Verdict | Edit made |
|---|---|---|
| 1. Biometric CLAIM marker | PASS-with-edit | Marker resolved; verification comment inserted at Ch15 line 167 |
| 2. Shamir threshold logic | PASS | None |
| 3. Time-lock attack model | PASS | None |
| 4. Argon2id parameters | PASS | None |
| 5. Citation metadata [4]–[7] | PASS | None (annotation on [5] URL stability, no error) |
| 6. Claims trace to sources | PASS | None |
| 7. Threat-model honesty | PASS | None |

---

## Gate Determination

**Technical-review → prose-review gate: PASSED.**

All `<!-- CLAIM: source? -->` markers are resolved. All technical claims trace to v13 §11, design-decisions §5 #48, or are explicitly authorized as new commitments per the outline. No invented Sunfish APIs identified (forward-looking namespaces `Sunfish.Foundation.Recovery` and `Sunfish.Kernel.Audit` are annotated as such in both chapter files per the code-check stage). Threat model is honestly bounded throughout. Citation metadata is accurate. Shamir arithmetic is correct.

The two new sections are ready to advance to `icm/prose-review`.
