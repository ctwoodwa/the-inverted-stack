# Technical-Review Report — #45 Collaborator Revocation and Post-Departure Partition

**Stage:** technical-review (ICM stage 4).
**Run:** 2026-04-27.
**Reviewer:** technical-reviewer subagent.
**Scope:** new sections only.
- Ch15 §Collaborator Revocation and Post-Departure Partition (lines 302–393).
- Ch20 §Revocation UX (lines 318–350).
- Citations [8]–[11] in Ch15 references list.

---

## Verdict per item

### Item 1 — CRDT operation-identifier collision after partition (sub-pattern 45e CLAIM marker)
**Verdict:** PASS-with-edit. Resolved.

**What the sources say.**
- Yjs INTERNALS.md (`github.com/yjs/yjs/blob/main/INTERNALS.md`): "Each client is assigned a unique *clientID* property on first insert. This is a random 53-bit integer." "Everything inserted in a Yjs document is given a unique ID, formed from a *ID(clientID, clock)* pair (also known as a Lamport Timestamp). The clock counts up from 0 with the first inserted character or item a client makes."
- Loro `loro-common/src/lib.rs`: `pub type PeerID = u64; pub type Counter = i32; pub struct ID { pub peer: PeerID, pub counter: Counter }` with the Rustdoc "Unique id for each peer. It's a random u64 by default" and "If it's the nth Op of a peer, the counter will be n."

**Architectural truth.** Both engines scope operation identifiers per `(peer, counter)` pair. The KEK sealing alone does not prevent identifier collision — it prevents the OTHER party from decrypting the successor log. What actually prevents collision is the architectural commitment that the two successor logs never re-merge (they are forks, not branches awaiting reconciliation). The "fresh node identifier scopes" point is the second line of defense if any cross-log integration ever occurs out-of-band. Both properties together make the partition collision-safe; the original draft's framing was technically correct but imprecisely attributed.

**Edit applied (Ch15 §45e, end of section, before §45f).** Replaced the `<!-- CLAIM -->` marker with a verification paragraph that:
1. Cites Yjs INTERNALS.md as new reference [12].
2. Cites Loro `loro-common/src/lib.rs` as new reference [13].
3. States the two properties (no re-merge by KEK separation; fresh node identifier scope per successor entity) and notes either alone closes the question.

The CLAIM marker is removed.

### Item 2 — OAuth 2.0 Token Revocation citation [8] (RFC 7009)
**Verdict:** PASS.

**What the source says.** RFC 7009 §1 (Introduction): "This specification defines an additional endpoint for OAuth authorization servers, which allows clients to notify the authorization server that an obtained token is no longer needed." §2.1 specifies the revocation request flow: "the authorization server first validates the client credentials... In the next step, the authorization server invalidates the token."

**Architectural mapping.** The chapter's framing in §45a — "The OAuth 2.0 Token Revocation specification [8] establishes the prior art; this architecture diverges from RFC 7009 in one structural respect — no central authorization server exists, so the event must propagate to peers rather than invalidate at a single endpoint" — is accurate. RFC 7009 is the canonical IETF specification for programmatic token invalidation, and the divergence (no central authorization server in a local-first system) is precisely stated.

No edit required.

### Item 3 — OCSP citation [9] (RFC 6960)
**Verdict:** PASS.

**What the source says.** RFC 6960 §1: "This document specifies a protocol useful in determining the current status of a digital certificate without requiring CRLs." §2 (Protocol Overview) and §4.2 (Response Syntax) establish that the relying party submits a request and receives a signed status response — meaning revocation status is consulted at relying-party query time, not communicated push-style at the moment the issuer signs the revocation.

**Architectural mapping.** The chapter's framing in §45d — "The OCSP and CRL precedents [9] [10] for X.509 certificate revocation establish the same trade-off — revocation takes effect when the relying party receives the status, not when the issuer signs it" — accurately characterizes OCSP's pull/relying-party-query semantics. The AP-not-CP analogy is well grounded.

No edit required.

### Item 4 — CRL citation [10] (RFC 5280)
**Verdict:** PASS.

**What the source says.** RFC 5280 §5 (CRL and CRL Extensions Profile) specifies the X.509 v2 CRL format. §5.1.2.1 (CRL `thisUpdate` field) and §5.1.2.2 (CRL `nextUpdate` field) establish that CRLs are periodically published artifacts; the gap between issuance and acquisition by relying parties is intrinsic to the protocol. RFC 5280 §3.3 (Revocation) explicitly states that CRLs are issued periodically and there is a window between revocation and the relying party learning of it.

**Architectural mapping.** The chapter's CRL precedent framing aligns with RFC 5280's eventual-consistency posture for revocation propagation. The bilateral grouping with OCSP [9] in the same sentence is appropriate — both are relying-party-query mechanisms for the same X.509 revocation use case.

No edit required.

### Item 5 — NIST SP 800-12 citation [11]
**Verdict:** PASS.

**What the source says.** NIST SP 800-12 Rev. 1 contains the relevant prior art for the access-termination artifact claim:
- §line 524: "Employee sabotage--often instigated by knowledge or threat of termination--is a critical issue for organizations and their systems. In an effort to mitigate the potential damage caused by employee sabotage, the terminated employee's access to IT infrastructure should be immediately disabled, and the individual should be escorted off company premises." (insider-threat access termination)
- §1189: "Examples of access control security controls include: account management, separation of duties, least privilege, session lock, information flow enforcement, and session termination." (account management as access control)
- §1205: "An audit trail is a record of individuals who have accessed a system as well as what operations the user has performed during a given period." (audit trail definition)
- §1357: "Examples of personnel control include: personnel screening, personnel termination, personnel transfer, access agreements, and personnel sanctions." (personnel termination as security control)
- §1358: "Organizations: ...(ii) ensure that organizational information and systems are protected during and after personnel actions such as terminations and transfers..." (post-termination protection)

**Architectural mapping.** The chapter's grouping in §45f — "For regulated industries — HIPAA, SOX, PCI-DSS, NIST SP 800-12 [11] — it is the access-termination artifact those frameworks require" — is supportable. NIST SP 800-12 is a high-level handbook rather than a detailed control catalog (NIST SP 800-53 would be the prescriptive control source — AC-2 Account Management family), but SP 800-12 explicitly names personnel termination, access disabling, and audit trails as security controls. The citation supports the broad framing the chapter makes.

**Optional improvement (not a blocker):** A future revision could add NIST SP 800-53 AC-2 (Account Management) for the prescriptive control reference. SP 800-12 is acceptable as the introductory framing this section uses.

No edit required.

### Item 6 — v13/v5 sourcing audit
**Verdict:** PASS-with-edit. Resolved.

**What the sources say.**
- v5 §4.3 ("Key Rotation and Revocation"): explicitly specifies the rotation procedure on role-membership change. "When role membership changes (for example, a user is removed from a team), the system must revoke access promptly: 1. Generate a new KEK for the role. 2. For each document owned by that role, decrypt the existing wrapped DEK using the old KEK and re-encrypt it with the new KEK. 3. Discard the old KEK once all DEKs are re-wrapped." This IS sub-pattern 45b's procedure, sourced directly from v5.
- v5 §1 abstract: "**Secure**: end-to-end encrypted, with revocation and rotation that still work at scale."
- v13 line 408: "Key rotation: the administrator generates new role keys, re-wraps for current authorized members, and publishes new bundles. Nodes no longer authorized do not receive new bundles and cannot decrypt future records."
- v13 line 532 (test edge case): "Role key rotated, former member reconnects → cannot decrypt records written after rotation."

**Architectural truth.** The original self-disclosure ("It does not appear in v13 or v5") is incorrect. v5 §4.3 specifies the cryptographic rotation half of the revocation procedure; v13 §11.3 specifies the same procedure under "Role Attestation vs. Key Distribution." Sub-pattern 45b (post-revocation key rotation) is a refinement of existing v13/v5 material, not a new commitment. The five other sub-patterns (45a explicit revocation event, 45c cached-copy management, 45d revocation propagation, 45e bilateral data partition, 45f revocation-event audit trail) ARE new — none of them appear in v13 or v5.

**Edit applied (Ch15 §Why this matters, paragraph 3).** Replaced the blanket "It does not appear in v13 or v5" claim with a precise enumeration: 45b is a refinement of v5 §4.3 / v13 §11.3 procedure; 45a, 45c, 45d, 45e, 45f are the new architectural commitments surfaced by the universal-planning review.

---

## Consolidated CLAIM marker list

| Marker | Location | Status |
|---|---|---|
| `<!-- CLAIM: CRDT operation identifiers... — verify -->` | Ch15:375 | RESOLVED — replaced with verification paragraph + refs [12] [13] |
| `<!-- voice-check: human author adds connective-tissue scene here... -->` | Ch20:350 | INTENTIONAL — structural placeholder for human voice-check pass; not a defect (per outline §F and code-check report) |

No new CLAIM markers added.

## References added

Two new entries appended to Ch15's reference list:
- `[12]` Yjs INTERNALS.md (Jahns, 2024) — for `(clientID, clock)` Lamport-pair operation identifiers.
- `[13]` Loro `loro-common/src/lib.rs` (Loro Project, 2024) — for `ID = (PeerID, Counter)` operation identifier struct.

These citations support the verification paragraph that resolves the §45e CRDT identifier-collision claim.

## Summary

All six items queued by code-check have been verified. Items 2, 3, 4, 5 (RFC 7009, RFC 6960, RFC 5280, NIST SP 800-12) PASS as cited — each citation accurately supports the prior-art framing the chapter makes. Items 1 (CRDT operation-identifier collision) and 6 (v13/v5 sourcing audit) PASS-with-edit — both required prose adjustments and were corrected in place. The CRDT identifier claim is now grounded in Yjs INTERNALS.md and Loro `loro-common/src/lib.rs`, with the precise architectural mechanism (no re-merge by KEK separation; fresh node identifier scope per successor entity) named explicitly. The v13/v5 self-disclosure now distinguishes 45b (refinement of existing v5 §4.3 / v13 §11.3 procedure) from 45a/45c/45d/45e/45f (genuinely new commitments). One CLAIM marker resolved; one intentional `<!-- voice-check -->` placeholder remains as designed for the human voice-check pass. No FAIL items.

**Technical-review → prose-review gate:** PASSED. Advance to prose-review.
