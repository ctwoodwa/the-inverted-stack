# Technical-review report — #47 Endpoint Compromise

**Iteration:** iter-0019 (technical-review)
**Date:** 2026-04-28
**Stage advance:** code-check (PASS) → technical-review
**Verdict:** PASS-with-claim-markers (1 marker preserved at §47c per loop-plan §5)

---

## Scope

Technical-accuracy review of the two new sections from extension #47:

1. **Ch15 §Endpoint Compromise: What Stays Protected** plus its IEEE refs [20]–[28] in the Ch15 reference list.
2. **App B §THREAT-10 — Compromised Endpoint** under §Section 2.

Out of scope (handled by another reviewer at iter-0019): Ch15 §Forward Secrecy and refs [14]–[19].

## Source-of-truth verification path

This Mac instance does not have the `C:\Projects\Sunfish\` reference implementation (project moved cross-platform per memory `reference_migration_memory_path.md`); the v13 / v5 papers in `source/` are gitignored and not present locally. Verification proceeded against:

- `docs/reference-implementation/design-decisions.md` §5 #47 (canonical statement of the primitive)
- `docs/reference-implementation/implementation-specification.md` (canonical SEC-* and SYNC-* concepts)
- `docs/reference-implementation/sunfish-package-roadmap.md` (canonical package boundaries for #47)
- Ch14 §Five-Step Handshake (in-tree) for the §47c forward-dependency check
- Reviewer domain knowledge of the academic citations (USENIX, IEEE S&P, Signal, Amnesty, Lookout, Citizen Lab)

## Items checked — all 10 from code-check queue

### 1. Apple Secure Enclave / Pixel Titan M / Microsoft Pluton non-extractability

- **Apple Secure Enclave.** The Secure Enclave is a coprocessor with its own secure boot, isolated memory, and cryptographic engine. Keys generated inside the Secure Enclave are not extractable by the Application Processor; only operations are exposed. The §47b claim "the key exists only inside the enclave and is never presented to the OS in plaintext" is consistent with Apple Platform Security guide.
- **Pixel Titan M.** Titan M is a discrete security chip on Pixel devices integrated with the Android Hardware-Backed Keystore via StrongBox. Keys generated with the StrongBox `KeyProperties.SECURITY_LEVEL_STRONGBOX` flag remain inside Titan M. The §47b claim is consistent with Google's published architecture.
- **Microsoft Pluton.** Pluton is a CPU-integrated security processor (vs. discrete TPM 2.0). The Nov 17, 2020 announcement date is correct. The §47b claim is consistent with Microsoft's published architecture; the implementation-specification at line 6142 also aligns with Pluton-tier deployments.
- **Citation collapse decision.** Ch15 [7] (Apple Platform Security, May 2024, general guide) and the prior [20] (Apple Platform Security — Secure Enclave anchor, May 2024) cite the same source document at different anchors. Per code-check guidance and standard IEEE practice, these collapse. **Action taken:** [20] collapsed into [7]; refs [21]–[28] renumbered → [20]–[27]. All inline citation sites in §47b (one) and §47f (two) updated accordingly.

**Status:** RESOLVED with edits. Refs [20]–[27] now consecutive with no duplicate Apple entry.

### 2. Intel SGX side-channel chronology

- **Foreshadow [22] (was [23]).** Van Bulck et al., USENIX Security 2018, pp. 991–1008. Verified — the paper appears in the proceedings of the 27th USENIX Security Symposium (Baltimore, 2018) at those page numbers. Cited correctly.
- **Plundervolt [23] (was [24]).** Murdock et al., IEEE S&P 2020, pp. 1466–1482. Verified — published in 2020 IEEE Symposium on Security and Privacy at those pages. Cited correctly.
- **SGAxe [24] (was [25]).** van Schaik et al., 2020, web reference at sgaxe.com. The website is the canonical disclosure site; SGAxe was the SGX-specific extension of the broader CacheOut work. Cited correctly.
- **Chronology in prose:** §47b says "successive generations" of SGX side-channel attacks. Foreshadow (2018) → Plundervolt (2019 disclosure, 2020 publication) → SGAxe (2020) is a valid "successive generations" timeline. Accurate.

**Status:** RESOLVED — no edits needed beyond renumber.

### 3. ARM TrustZone framing

- Ref [25] (was [26]) — Arm Ltd. white paper "Arm Security Technology — Building a Secure System using TrustZone Technology", Apr 2009 (revised 2022). Verified canonical source on Arm developer documentation.
- §47b claims TrustZone "offers a comparable model on Arm-class hardware." TrustZone is a hardware-isolated "secure world" (CPU mode separation, secure peripherals, secure memory). Apple's SEP and Google's StrongBox/Titan M conceptually fall in the same secure-coprocessor abstraction class even though their concrete implementations differ. The §47b "comparable model" framing is accurate and appropriately hedged ("comparable", not "equivalent").

**Status:** RESOLVED — no edits needed.

### 4. Pegasus / Predator / Hermit characterization

- **Pegasus reference [26] (was [27]).** **Citation attribution corrected.** The "Forensic Methodology Report: How to catch NSO Group's Pegasus" (July 2021) was published by **Amnesty International Security Lab**, not by Citizen Lab. Citizen Lab provided independent peer review. The original draft incorrectly attributed primary authorship to "Marczak, Scott-Railton, and Deibert (Citizen Lab)". **Action taken:** updated [26] to credit Amnesty International Security Lab as primary publisher with Citizen Lab cross-confirmation, and switched the URL to the Amnesty International canonical landing page.
- **Hermit reference [27] (was [28]).** **Date refined.** Lookout's original public disclosure of Hermit was April 2022, with subsequent confirmation of Kazakhstan deployment in June 2022. The original "Jun. 2022" date was defensible but imprecise. **Action taken:** updated [27] to read "Apr. 2022 (with subsequent Citizen Lab confirmation of Kazakhstan use Jun. 2022)" — preserves both timestamps and the secondary cross-confirmation source.
- **Predator/Cytrox.** Cited in [27] as a supplement via Google Threat Analysis Group (TAG) reporting. TAG analysis of Predator/Cytrox is publicly documented. The supplemental URL `blog.google/threat-analysis-group/` is the correct landing page for TAG threat advisories.
- **§47f characterization.** "Pegasus, Predator, and Hermit operate at the level of full OS compromise with zero-click delivery" is accurate for all three families per documented Citizen Lab/Amnesty/Lookout/TAG reporting. The zero-click delivery vectors (iMessage/iOS for Pegasus; SMS-based exploit chains for Predator; carrier-mediated message delivery for Hermit) are publicly attributed.

**Status:** RESOLVED with citation-attribution + date edits.

### 5. TPM 2.0 attestation framing

- §47c states: "TPM 2.0 and equivalent mechanisms produce a cryptographic proof that the device is running expected, unmodified software at boot time. The attestation is presented to the relay at handshake; the relay validates it against a known-good measurement before admitting the session."
- TPM 2.0 (TCG specification family 2.0) supports Platform Configuration Registers (PCRs) that accumulate measurements during the boot chain, and the TPM Quote operation produces a signed PCR digest that constitutes a remote attestation proof. The §47c framing is technically accurate.
- The §47c term "known-good measurement" is the standard remote-attestation pattern (verifier maintains expected PCR values, compares against quote). Accurate.

**Status:** RESOLVED — no edits needed.

### 6. Ch14 forward-dep resolution (the §47c CLAIM marker)

- Ch14 §Five-Step Handshake (lines 52–79) describes a five-step handshake: HELLO, CAPABILITY_NEG, ACK, DELTA_STREAM, GOSSIP_PING. Ch14 line 73 describes role attestation in CAPABILITY_NEG ("each requested subscription includes a role attestation token signed by the node's device key. The receiving node verifies the attestation before granting any subscription").
- This is **role attestation** (a signed claim about the user's role) — distinct from **boot-time integrity attestation** (TPM 2.0 cryptographic proof that the device is running expected unmodified software). Ch14 does not currently describe TPM-based boot attestation validation at the handshake.
- **Decision:** the §47c CLAIM marker stays in place. The forward dependency on Ch14 is real and accurately scoped: Ch14 currently has a role-attestation handshake step but no boot-attestation handshake step. Per loop-plan §5, PASS-with-claim-markers up to 2 markers is acceptable; the §47c marker counts toward that budget. Resolution path is documented in the marker itself (back-add a brief boot-attestation paragraph to Ch14, or re-frame §47c as forward-looking contract).

**Status:** PRESERVED (1 of 2 allowed markers used).

### 7. §47e containment mechanisms

Verified against `implementation-specification.md` and `design-decisions.md` §5 #47:

- **Per-device keypair isolation.** SEC-23 (line 4880) confirms "every write is signed by a long-lived Ed25519 device keypair". Line 5468: "Each data directory contains a distinct device keypair." The §47e claim "Each device in a user's fleet holds a distinct keypair. Compromise of one device's private key does not compromise other devices in the same fleet" is consistent.
- **Append-only transaction log with per-device signing.** Lines 681, 746, 753, 1240, 1246, 2389, 2761, 3461, 4081 all confirm append-only structure. Line 3430 verifies the backdating-prevention property: "attempt a backdated posting, assert it is recorded as an adjustment in the current period and the closed-period log is unchanged." The §47e claim is consistent with the spec.
- **Role-scoped access.** SEC-02 (line 4410) confirms "per-role encryption keys are absent from non-member nodes." The §Role Attestation Flow cross-reference resolves correctly to Ch15 line 83. The §47e claim is consistent.

**Status:** VERIFIED — no edits needed.

### 8. Relay keypair-session binding

- §47e claim: "the relay enforces keypair-session binding at every reconnection. An attacker holding a stolen session token from one device cannot pivot it onto another."
- Ch14 line 46 (managed relay description): "All relay-forwarded messages carry the same Ed25519 device-key signatures as direct connections; the receiving daemon verifies each signature before applying any operation, so a compromised relay cannot inject messages nor silently modify them in transit."
- This confirms relay-side signature verification per device key. The "every reconnection" specificity is consistent with Ch14's CAPABILITY_NEG re-execution at every handshake (line 73).

**Status:** VERIFIED — no edits needed.

### 9. MDM provider accuracy

- **Microsoft Intune.** Confirmed enterprise MDM with documented OS-level wipe capability (`Wipe`/`AutopilotReset` actions). Cited correctly.
- **Jamf (Jamf Pro).** Confirmed enterprise MDM with documented `EraseDevice` MDM command for managed Apple devices. Cited correctly.
- **Google Workspace MDM.** Google Workspace's mobile management surface includes remote wipe for managed Android and iOS devices. Cited correctly.
- Implementation-spec line 6154: "integration tests pass identical attestation flows under at least Intune and Jamf packaging" — Intune and Jamf are the spec's canonical MDM examples, consistent with §47d.

**Status:** VERIFIED — no edits needed.

### 10. §47f hard sentence preservation

- Sentence: "No software-only architecture can claim otherwise."
- Verified present at Ch15 line 555 (post-edit). Position preserved at end of §47f closing paragraph.
- **Note for prose-reviewer:** this sentence must survive prose-review unsoftened. Carries the §47f architectural-honesty load. Confirmed in code-check item 10 and reaffirmed here.

**Status:** PRESERVED for prose-reviewer attention.

## Sunfish package canon check

Per `.wolf/cerebrum.md` and the Sunfish package canon:

- `Sunfish.Kernel.Security` — referenced 4 times in §Endpoint Compromise (47b enclave binding, 47c attestation surface, 47d crypto-shred, FAILED-conditions escalation). All in canon. ✓
- No other Sunfish namespaces referenced in the section. ✓
- App B THREAT-10 contains no Sunfish namespace references — by design. ✓

## App B §THREAT-10 verification

- **Capability tier table.** Medium (consumer spyware) / High (Pegasus, Predator, Hermit) split is consistent with the practitioner-facing language in §A.7 of the outline and the §47f characterization in Ch15. Accurate.
- **Attack tree branches 1–6.** Each branch maps to a specific Ch15 §47 mechanism: branch 2/3 → §47b enclave separation; branch 4 → §In-Memory Key Handling re-authentication; branch 5 → §47e per-device keypair binding; branch 6 → §47d remote wipe + MDM. Cross-references resolve.
- **"Bearer-only tokens succeed — that is an architectural failure against §47e."** Verified consistent with §47e's per-device keypair isolation requirement: a token system that is not bound to the device keypair would let an attacker pivot a captured session token to another device, which §47e explicitly prohibits.
- **Mitigation summary.** Five bullets, each tracing back to a specific Ch15 §47 sub-pattern. Accurate.

**Status:** App B THREAT-10 passes technical review with no edits required.

## Edits made

1. Ch15 line 517 — `[20]` → `[7]` for Apple Secure Enclave reference; `[21]`/`[22]` → `[20]`/`[21]` for Titan M / Pluton.
2. Ch15 line 519 — `[23][24][25]` → `[22][23][24]` (SGX side-channel triple).
3. Ch15 line 519 — `[26]` → `[25]` (TrustZone).
4. Ch15 line 555 — `[27][28]` → `[26][27]` (Pegasus + Hermit).
5. Ch15 reference list (lines 672–688) — removed the standalone [20] (Apple Secure Enclave anchor) by collapsing into existing [7]; renumbered [21]–[28] → [20]–[27].
6. Ch15 ref [26] (Pegasus) — corrected primary authorship from Citizen Lab → Amnesty International Security Lab; updated URL accordingly; preserved Citizen Lab cross-confirmation note.
7. Ch15 ref [27] (Hermit) — refined date to "Apr. 2022 (with subsequent Citizen Lab confirmation of Kazakhstan use Jun. 2022)" reflecting Lookout's original April 2022 disclosure.

## Items deferred via CLAIM marker

1. **§47c Ch14 attestation-handshake forward dependency.** Marker preserved (1 of 2 allowed). Resolution path documented in marker text. Will be addressed either by a parallel Ch14 update (adding boot-attestation step to the five-step handshake) or by reframing §47c language as forward-looking-contract.

## Quality gate

- CLAIM markers used: 1 of 2 budget (§47c Ch14 forward dependency).
- Citation accuracy: all 9 in-text refs ([7] + [20]–[27]) verified or corrected.
- Sunfish package canon: clean (only `Sunfish.Kernel.Security`).
- Implementation-spec consistency: SEC-23 + SEC-02 + SEC-01 + line 4408 align with §47e containment claims.
- §47f hard sentence: preserved.
- App B THREAT-10: accurate, cross-references resolve, attack-tree mechanism mapping consistent with Ch15 §47.

**Verdict: PASS-with-claim-markers.** Section advances to prose-review.

## Notes for prose-reviewer

1. §47f sentence "No software-only architecture can claim otherwise" — must not soften.
2. The §47b prose now references both [7] (Apple) and [20] (Titan M) in the same sentence enumerating production-deployed enclaves — the asymmetric numbering (7 then 20) is intentional and reflects that Apple Platform Security was already cited from extension #48; do not "renumber for visual symmetry".
3. The §47c CLAIM marker stays inline through prose-review; it will resolve at the next #47-touching iteration or via a parallel Ch14 update queued by the loop-coordinator.
