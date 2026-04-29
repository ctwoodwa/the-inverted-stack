# Code-check report — #47 Endpoint Compromise

**Iteration:** iter-0018 (post-migration resume)
**Date:** 2026-04-27
**Stage advance:** draft (applied) → code-check
**Verdict:** PASS

---

## Scope

Code-check pass on the two new sections:

1. **Ch15 §Endpoint Compromise: What Stays Protected** (chapters/part-3-reference-architecture/ch15-security-architecture.md, ~1,691 words) inserted at iter-0016 between §In-Memory Key Handling and §Supply Chain Security.
2. **App B §THREAT-10 — Compromised Endpoint** (chapters/appendices/appendix-b-threat-model-worksheets.md, ~554 words) inserted at iter-0016 inside §Section 2 — Actor Taxonomy Template after the capability-level definitions table.

## Sunfish package inventory

One Sunfish namespace reference, in current canon:

| Namespace | In canon? | Site count | Use |
|---|---|---|---|
| `Sunfish.Kernel.Security` | yes | 4 | Secure-enclave binding (§47b); attestation exposure (§47c); local-side crypto-shred instruction (§47d); FAILED-condition escalation contract |

**No new top-level namespace introduced.** The HTML code-check annotation prepended at the start of the Ch15 section declares this explicitly. No update to `docs/reference-implementation/sunfish-package-roadmap.md` required for #47.

App B §THREAT-10 contains no Sunfish namespace references — by design (the appendix is the threat-model worksheet template, not the architectural specification).

## Code block / class API audit

- Code fences in Ch15 section: 0
- Code fences in App B THREAT-10: 0
- Class names in prose: 0
- Method signatures in prose: 0

The sections are pure prose-level specification + a structured threat-actor template. The illustrative-code marker (`// illustrative — not runnable`) is therefore unused.

## Placeholder / marker audit

- `TBD` / `TODO` / `expand here` / `see paper for details`: 0
- `<!-- CLAIM: -->` markers in Ch15: 1 (preserved at §47c — Ch14 §Sync Daemon Protocol does not currently describe attestation validation at the handshake; flagged for technical-review resolution)
- `<!-- CLAIM: -->` markers in App B: 0
- HTML code-check annotation block in Ch15: 1 (line preceding §Endpoint Compromise heading, accurate disclosure of namespace status + forward dependency on Ch14)

## Cross-reference resolution

| Reference | Target | Resolves? |
|---|---|---|
| Ch7 §The Security Lens | chapters/part-2-council-reads-the-paper/ch07-security-lens.md | yes (chapter title; informal §-style cross-reference acceptable per book convention) |
| Ch15 §Threat Model | Ch15 line 10 | yes |
| Ch15 §Key Hierarchy | Ch15 line 52 | yes |
| Ch15 §Forward Secrecy and Post-Compromise Security | Ch15 line 403 (§47e cross-ref to #46) | yes |
| Ch15 §Role Attestation Flow | Ch15 line 83 | yes |
| Ch15 §Collaborator Revocation and Post-Departure Partition | Ch15 line 302 | yes |
| Ch15 §In-Memory Key Handling | Ch15 line 477 | yes |
| Ch15 §Endpoint Compromise (App B back-ref) | Ch15 (this section) | yes |
| Ch14 §Sync Daemon Protocol | Ch14 line 52 (§Five-Step Handshake) | partial — chapter exists; specific claim about attestation validation flagged via CLAIM marker for technical-review |

Eight of nine cross-references resolve cleanly. The one outstanding item is the documented forward dependency on Ch14 attestation-handshake validation, which is correctly held under a CLAIM marker pending technical-review resolution. This is the expected and accepted shape for a forward-looking integration point.

## Citation audit

In-text citations [20]–[28] correspond to the nine new IEEE references appended to Ch15's reference list at iter-0016:

| In-text site | Ref | Source |
|---|---|---|
| §47b | [20] | Apple, "Apple Platform Security — Secure Enclave," May 2024 |
| §47b | [21] | Google, "Pixel Titan M and Android Hardware-Backed Keystore," 2024 |
| §47b | [22] | Microsoft, "Microsoft Pluton security processor," Nov. 2020 |
| §47b | [23] | Van Bulck et al., "Foreshadow," USENIX Security 2018 |
| §47b | [24] | Murdock et al., "Plundervolt," IEEE S&P 2020 |
| §47b | [25] | van Schaik et al., "SGAxe," 2020 |
| §47b | [26] | Arm Ltd., "Arm TrustZone Technology," 2009 (rev. 2022) |
| §47f | [27] | Marczak et al. (Citizen Lab), "How to catch NSO Group's Pegasus," Jul. 2021 |
| §47f | [28] | Lookout Threat Intelligence, "Hermit Spyware in Kazakhstan," Jun. 2022 |

All 9 in-text citations resolve to entries in the Ch15 reference list. No duplicate citations; no broken numbers.

**Note for technical-review.** Ch15 reference [7] (Apple Platform Security, May 2024 — added at iter-0004 as part of #48 key-loss-recovery's biometric-template verification) and Ch15 reference [20] (Apple Platform Security — Secure Enclave, May 2024 — added at iter-0016) cite the same Apple source document but anchor to different sections of it. The draft self-disclosed this as a candidate for collapse during technical-review. Either keep [20] separate (current state) or collapse [20] → [7] and renumber [21]–[28] → [20]–[27]. Code-check defers the decision to technical-review.

## App B §THREAT-10 specific checks

- THREAT-NN format establishment: confirmed. THREAT-10 is the first numbered, structured taxonomy entry in App B; the §Customization guidance and capability-level definitions tables are positioned before THREAT-10, preserving the structure of Section 2. Subsequent extensions (#9 → THREAT-11) follow the established format.
- Attack-tree primary branch (mobile zero-click compromise): six numbered steps, structurally complete.
- Mitigation summary: five bullets, references Ch15 §Endpoint Compromise + §In-Memory Key Handling + §Collaborator Revocation cross-chapter (within Ch15).

## FAILED conditions

§FAILED conditions block (Ch15 §Endpoint Compromise) is present and accurate:
- Compromised endpoint impersonates other devices in sync mesh
- Compromised endpoint backdates transactions in shared log
- Endpoint-compromise scope not documented in deployed architecture's security reference

Each FAILED condition maps directly to one of the §47e containment mechanisms or the §47a scope-declaration commitment. The escalation path is named: confirmed FAILED conditions escalate to `Sunfish.Kernel.Security` maintainers before draft advances.

## Items queued for technical-review

The following items are accepted for code-check but require @technical-reviewer verification:

1. **Apple Secure Enclave / Pixel Titan M / Pluton non-extractability** — verify [20], [21], [22] correctly attribute non-extractability properties; consider collapse of [20] into existing [7] (both cite Apple Platform Security May 2024) per the draft's self-flagged note.
2. **Intel SGX side-channel chronology** — verify Foreshadow [23] (USENIX Security 2018, pp. 991-1008), Plundervolt [24] (IEEE S&P 2020, pp. 1466-1482), SGAxe [25] (2020) citation metadata; verify the §47b claim that Apple Secure Enclave + Google Titan M have a "substantially shorter" academic attack record than SGX.
3. **ARM TrustZone framing** — verify [26] supports the §47b claim that TrustZone offers a comparable enclave model on Arm-class hardware.
4. **Pegasus / Predator / Hermit zero-click capability** — verify [27] (Citizen Lab Pegasus methodology) and [28] (Lookout Hermit + Google TAG Predator) support the §47f characterization of nation-state spyware as full-OS zero-click compromise.
5. **TPM 2.0 attestation framing** — verify §47c description of TPM 2.0 producing cryptographic boot-time integrity proof matches TCG specification.
6. **Ch14 attestation forward dependency** — resolve the §47c CLAIM marker. Either: (a) back-add an attestation-validation paragraph to Ch14 §Five-Step Handshake (currently the attestation step is implicit at line 52), or (b) replace the §47c claim with a forward-looking statement that attestation handshake is part of extension #47's contract on the sync daemon.
7. **§47e containment mechanisms** — verify per-device keypair isolation, append-only transaction log with per-device signing, and role-scoped access match the v13 / design-decisions §5 #47 specification.
8. **Relay keypair-session binding** — verify the §47e claim that the relay enforces keypair-session binding at every reconnection matches the relay protocol spec.
9. **MDM provider list** — verify Intune, Jamf, Google Workspace MDM are accurate examples of enterprise MDM channels supporting OS-level wipe orders.
10. **§47f hard sentence preservation** — flag for prose-reviewer + style-enforcer: "No software-only architecture can claim otherwise" must survive prose-review unsoftened. This is a deliberate hard claim per the drafter's QC self-assessment.

## Quality gate

Code-check → technical-review **PASSES** with 1 documented CLAIM marker preserved (§47c Ch14 forward dependency) per loop-plan §5. Section advances to technical-review with 10 documented items for the next reviewer.
