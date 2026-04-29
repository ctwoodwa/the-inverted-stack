# Code-check report — #46 Forward Secrecy and Post-Compromise Security

**Iteration:** iter-0017 (post-migration resume)
**Date:** 2026-04-27
**Stage advance:** draft → code-check
**Verdict:** PASS

---

## Scope

Code-check pass on the Ch15 §Forward Secrecy and Post-Compromise Security section (chapters/part-3-reference-architecture/ch15-security-architecture.md, lines 403-474, ~1,480 words). #46 introduced no new chapter; it inserted one new H2 section into Ch15 between §Collaborator Revocation and §In-Memory Key Handling.

## Sunfish package inventory

Two distinct Sunfish namespace references, both in current canon:

| Namespace | In canon? | Site count | Use |
|---|---|---|---|
| `Sunfish.Kernel.Security` | yes | 3 | HKDF-SHA256 derivation + per-message zeroing (§46a); rotation trigger interface (§46c); FS/PCS conformance test suite (§46e) |
| `Sunfish.Kernel.Sync` | yes | 4 | Ephemeral X25519 at session establishment (§46a); Double Ratchet session-layer extension (§46b); rotation execution (§46c); sealed-sender policy flag (§46d) |

**No new top-level namespace introduced.** Forward secrecy and post-compromise security extend the existing kernel session layer; they do not introduce a Foundation-tier package. The HTML code-check annotation at line 405 declares this explicitly. No update to `docs/reference-implementation/sunfish-package-roadmap.md` required.

## Code block / class API audit

- Code fences in section: 0
- Class names in prose: 0
- Method signatures in prose: 0
- Constructor parameters in prose: 0

The section is pure prose-level specification. The illustrative-code marker (`// illustrative — not runnable`) is therefore unused.

## Placeholder / marker audit

- `TBD` / `TODO` / `expand here` / `see paper for details`: 0
- `<!-- CLAIM: -->` markers: 0
- HTML code-check annotation block: 1 (line 405, accurate disclosure of namespace status)

## Cross-reference resolution

All cross-references resolve to existing sections within Ch15 except where a forward dependency on Ch14 was already documented during the #47 application:

| Reference | Target | Resolves? |
|---|---|---|
| §Threat Model | Ch15 line 10 | yes |
| §Key Compromise Incident Response | Ch15 line 99 | yes |
| Ch14 §Sync Daemon Protocol | external chapter | yes (cross-chapter) |
| §Relay Trust Model | Ch15 line 519 | yes |
| §Endpoint Compromise: What Stays Protected | Ch15 (inserted at iter-0016) | yes |
| §Collaborator Revocation and Post-Departure Partition | Ch15 line 302 | yes |
| §Key Hierarchy | Ch15 line 52 | yes |
| §Key-Loss Recovery | Ch15 line 117 | yes |

Six of seven Ch15-internal cross-references resolve cleanly. The one external cross-reference (Ch14 §Sync Daemon Protocol) resolves at the chapter-name level; the same forward dependency on Ch14 attestation-handshake validation is already documented in #47's CLAIM marker (Ch15 §47c). No additional CLAIM marker introduced for #46.

## Citation audit

In-text citations [14]–[19] correspond to the six new IEEE references appended to Ch15's reference list at iter-0014/0015:

| In-text site | Ref | Source |
|---|---|---|
| Line 427 §46b | [14] | Marlinspike & Perrin, "The Double Ratchet Algorithm," Signal Foundation, Nov. 2016 |
| Line 433 §46b | [15] | Marlinspike & Perrin, "The X3DH Key Agreement Protocol," Signal Foundation, Nov. 2016 |
| Line 435 §46b | [16] | T. Perrin, "The Noise Protocol Framework," rev. 34, Jul. 2018 |
| Line 435 §46b | [17] | Barnes et al., "MLS Protocol," IETF RFC 9420, Jul. 2023 |
| Line 435 §46b | [18] | WhatsApp Inc., "WhatsApp Encryption Overview," Sep. 2021 |
| Line 461 §46e | [19] | Borisov, Goldberg, Brewer, "OTR Communication," WPES 2004 |

All six in-text citations resolve to entries in the reference list. No duplicate citations; no broken numbers.

## FAILED conditions and kill trigger

§FAILED conditions block (lines 465-473) is present and accurate:
- Past messages decryptable from current key material → FS failure
- Current key compromise propagates to future messages without rotation → PCS failure
- No automatic key rotation exists → both fail

Kill trigger present (line 473): a FAILED condition recurring across three consecutive technical-review passes is the kill threshold.

## Items queued for technical-review

The following items are accepted for code-check but require @technical-reviewer verification against authoritative cryptographic sources:

1. **X25519 / Curve25519 ephemeral exchange framing** — verify standard usage and that "Diffie-Hellman function over Curve25519" parenthetical is accurate per RFC 7748.
2. **HKDF-SHA256 derivation chain framing** — verify the per-message-key chain construction described in §46a matches the standard ratchet construction (HKDF as PRF, salt rotation per step).
3. **Double Ratchet faithfulness** — verify §46b description of symmetric ratchet (per-message advance) and DH ratchet (advance on new public key from peer) matches the Marlinspike-Perrin Nov. 2016 spec [14].
4. **X3DH asynchronous-prekey framing** — verify §46b description of prekey-based async session establishment matches [15].
5. **Noise KK pattern fit** — verify the claim that Noise KK (both parties have known static keypairs) is the closer fit to the architecture's enrolled-device model, per [16].
6. **MLS / TreeKEM extension to group sessions** — verify [17] describes TreeKEM-based group ratcheting and that the §46b parenthetical "deployments with large role groups may adopt MLS in place of pairwise Double Ratchet" is accurate.
7. **OTR provenance** — verify [19] citation metadata (Borisov, Goldberg, Brewer, WPES 2004, pp. 77-84) and that the §46e claim "Off-The-Record Messaging established the precedent — naming these properties in the protocol spec itself" is supportable.
8. **WhatsApp at billion-user scale** — verify [18] describes Double Ratchet deployment at billion-user scale, not a different protocol.
9. **Conformance test framing** — verify that the §46e conformance test descriptions (recorded session state at time T cannot decrypt T-1; captured ratchet state at T after one DH advance cannot decrypt T+2) are correct cryptographic property statements.

## Quality gate

Code-check → technical-review **PASSES**. Section advances to technical-review with 9 documented items for the next reviewer.
