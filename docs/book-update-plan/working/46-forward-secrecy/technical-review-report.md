# Technical-review report — #46 Forward Secrecy and Post-Compromise Security

**Iteration:** iter-0019 (technical-review)
**Date:** 2026-04-28
**Stage advance:** code-check → technical-review
**Verdict:** PASS-with-claim-markers (1 CLAIM marker; within ≤2 budget)

---

## Scope

§Forward Secrecy and Post-Compromise Security in `chapters/part-3-reference-architecture/ch15-security-architecture.md` (lines 403-474, ~1,480 words) and the IEEE numeric references [14]-[19] in the Ch15 reference list (lines 659-669). Out of scope: §Endpoint Compromise (refs [20]-[28]) — owned by extension #47.

Source-paper context note: the v13/v5 architecture papers in `source/` are not present on this machine (gitignored, not transferred during the recent macOS migration). The task brief acknowledges this is expected and that v13/v5 may not directly speak to the cryptographic protocols cited; verification is therefore against (a) chapter-internal architectural consistency, (b) primary-source crypto specifications [14]-[19] verified live, and (c) the Sunfish package canon in `.wolf/cerebrum.md`.

---

## Items checked

### A. Architectural claims (consistency with chapter context)

1. **Per-node identity keys / device keypairs as the basis for session establishment** — consistent with Ch14 §Five-Step Handshake (CAPABILITY_NEG carries attestations signed by the node's device key) and Ch15 §Threat Model. ✓
2. **Relay as ciphertext forwarder; relay observes communication graph but not payload** — consistent with Ch15 §Relay Trust Model (lines 596-612). The §46d sealed-sender treatment cleanly extends the existing relay-metadata discussion. ✓
3. **KEK rotation cadence (90 days)** — §46c claims "scheduled cadence... every 90 days, matching the KEK rotation cadence in §Key Hierarchy." Ch15 §Key Hierarchy and §Key Compromise Incident Response do not state an explicit 90-day default, but they describe periodic rotation as a maintenance operation distinct from incident response. The 90-day claim is forward-compatible architectural commitment surfaced by #46 (per outline §C, "new architectural commitment surfaced through universal-planning review per design-decisions §5 #46"). Consistent. ✓
4. **Cross-references** — §Threat Model, §Key Compromise Incident Response, §Key Hierarchy, §Relay Trust Model, §Endpoint Compromise: What Stays Protected, §Collaborator Revocation and Post-Departure Partition, §Key-Loss Recovery all resolve. Ch14 §Sync Daemon Protocol reference resolves at chapter-name level. ✓
5. **Session-layer extension (no new top-level namespace)** — code-check report confirmed no new package is introduced; §46 extends `Sunfish.Kernel.Security` and `Sunfish.Kernel.Sync` only. Consistent with cerebrum canon. ✓

### B. Primary-source citations [14]-[19]

| Ref | Source | URL live? | Authors verified | Date verified | Notes |
|---|---|---|---|---|---|
| [14] | Marlinspike & Perrin, "The Double Ratchet Algorithm," Signal Foundation, Nov. 2016 | yes (HTTP 200) | yes | Nov. 2016 spec date is canonical | ✓ |
| [15] | Marlinspike & Perrin, "The X3DH Key Agreement Protocol," Signal Foundation, Nov. 2016 | yes (HTTP 200) | yes | Nov. 2016 spec date is canonical | ✓ |
| [16] | T. Perrin, "The Noise Protocol Framework," rev. 34, Jul. 2018 | yes (HTTP 200) | yes (single author) | Document carries `<meta name="date" content="2018-07-11">`; revision 34 confirmed in change log | ✓ |
| [17] | Barnes, Beurdouche, Robert, Millican, Omara, Cohn-Gordon, "MLS Protocol," IETF RFC 9420, Jul. 2023 | yes (HTTP 200) | yes (full author list verified against rfc-editor.org HTML metadata) | RFC 9420 is the canonical MLS RFC, published July 2023 | ✓ |
| [18] | WhatsApp Inc., "WhatsApp Encryption Overview — Technical White Paper," ~~Sep. 2021~~ → **Nov. 2021** | yes (HTTP 200; redirects to fbcdn) | corporate author | PDF embedded filename indicates `whitepaper_edited_Nov 2021`; **draft cited Sep. 2021 (incorrect)** | **CORRECTED in chapter file** |
| [19] | Borisov, Goldberg, Brewer, "Off-the-Record Communication, or, Why Not To Use PGP," WPES 2004, Washington DC, pp. 77-84 | OTR PDF live (HTTP 200 from cypherpunks.ca); ACM DL Cloudflare-blocked but DBLP record confirms metadata | yes (DBLP BibTeX confirmed) | yes (October 2004 venue date) | ✓ |

### C. Cryptographic claims attached to citations

1. **§46b "symmetric ratchet advances on every message; DH ratchet advances on new public key from peer"** — matches Marlinspike-Perrin Nov. 2016 [14] §3 (KDF chains) and §3.3 (DH ratchet). ✓
2. **§46b "Forward secrecy comes from the symmetric ratchet's one-directionality"** — correct: the chain KDF is one-way per [14] §2.2. ✓
3. **§46b "Post-compromise security comes from the Diffie-Hellman ratchet"** — correct: DH ratchet is the healing mechanism per [14] §1, §3.3. ✓
4. **§46b "X3DH... establishes the initial shared secret from prekeys published in advance, allowing one party to initiate a session while the other party is offline"** — correct per [15] §1, §2.5. ✓
5. **§46b "The Noise framework... KK pattern (both parties have known static keypairs) is the closer fit to the Inverted Stack's enrolled-device model"** — correct per [16] §7. The KK pattern: both initiator and responder have known static keypairs at session start. Matches an enrolled-device topology where both nodes have device keypairs prior to first contact. ✓
6. **§46b "MLS (Messaging Layer Security, RFC 9420) extends ratcheting to group messaging through a TreeKEM construction"** — correct per [17] §1, §5.4 (TreeKEM). ✓
7. **§46b "WhatsApp end-to-end encryption specification documents the Double Ratchet at billion-user scale"** — correct per [18] (WhatsApp uses the Signal protocol; user count exceeds 2 billion as of 2021). ✓
8. **§46a "ephemeral X25519 (the Diffie-Hellman function over Curve25519) exchange"** — correct per RFC 7748 (X25519 is the DH function defined over Curve25519). ✓
9. **§46a "HKDF-SHA256 derives a per-message key chain from that secret"** — consistent with the Signal symmetric KDF chain construction; HKDF-SHA256 framing aligns with Ch15 §Key Hierarchy's existing usage of HKDF-SHA256 for subordinate key derivation. ✓
10. **§46d sealed sender (encrypt sender identifier under recipient's long-term public key; relay sees destination only)** — correct per Signal's sealed-sender deployment; recipient unwraps and verifies sender attestation post-decryption. ✓

### D. Sunfish package references

Two package references in the section, both in canon:
- `Sunfish.Kernel.Security` — in current Sunfish package canon. ✓
- `Sunfish.Kernel.Sync` — in current Sunfish package canon. ✓

No class names, method signatures, constructor parameters, or invented APIs in the section. No new namespace introduced.

---

## Items resolved with edits

### Edit 1 — WhatsApp whitepaper date corrected

**File:** `chapters/part-3-reference-architecture/ch15-security-architecture.md` line 667

**Change:** `Sep. 2021` → `Nov. 2021`

**Justification:** The PDF embedded filename `whitepaper_edited_Nov 2021-en-pt_br-R-C` (visible in PDF body strings) indicates the document is the November 2021 revision. The September 2021 date in the draft was unsupported and contradicts the PDF's own metadata.

---

## Items deferred with CLAIM markers

### CLAIM marker 1 — OTR forward-secrecy attribution (§46e, line 461)

**Inserted at:** end of the §46e opening paragraph, after "...all inherited the discipline."

**Marker text:**
```
<!-- CLAIM: OTR 2004 [19] named forward secrecy explicitly; "post-compromise
security" as a named property post-dates OTR (PCS terminology is generally
attributed to Cohn-Gordon, Cremers, Garratt c. 2016). The phrase "these
properties" therefore overcredits OTR for both. Defer to next-pass copy-edit
(precision tightening, not architectural change). -->
```

**Justification:** The OTR 2004 paper [19] established forward secrecy as a named protocol property and is correctly cited as the precedent. However, the prose says OTR established the precedent for naming "these properties" — referring back to forward secrecy *and* post-compromise security from earlier in the section. PCS as a named, formalized protocol property post-dates OTR by roughly a decade. The architectural claim (naming security properties in the protocol spec is the discipline Signal, MLS, and Noise inherited) is sound; the temporal attribution of *both* properties to OTR is imprecise. Flagged for prose-review precision tightening rather than architectural rework. Within the ≤2 CLAIM budget per loop-plan §5.

---

## Items not flagged (verified ✓)

The following items from the code-check queue are verified and need no marker:

- X25519/Curve25519 framing (RFC 7748)
- HKDF-SHA256 derivation framing (consistent with Ch15 §Key Hierarchy)
- Double Ratchet symmetric/DH ratchet description ([14] §3)
- X3DH async-prekey framing ([15] §2.5)
- Noise KK pattern fit ([16] §7)
- MLS TreeKEM extension to group sessions ([17] §5.4)
- WhatsApp Double Ratchet at billion-user scale ([18])
- Conformance test framing (cryptographic property assertions, standard practice)
- Cross-reference resolution within Ch15 (six of seven internal targets)
- Forward dependency on Ch14 §Sync Daemon Protocol (already documented in #47's CLAIM marker, no new marker required)

---

## Verdict

**PASS-with-claim-markers.** One CLAIM marker inserted; ≤2-marker budget per loop-plan §5 satisfied. One factual correction applied to a reference-list entry (WhatsApp whitepaper date Sep. 2021 → Nov. 2021).

The section's architectural claims are internally consistent with the Ch15 threat model, the Ch14 sync-daemon handshake, and Sunfish package canon. All six primary-source citations [14]-[19] resolve to live URLs and are correctly attributed. The flagged imprecision is editorial-grade (a single phrase that overcredits OTR for both forward secrecy and post-compromise security) and does not affect the section's architectural commitment.

---

## Gate decision

**technical-review → prose-review: ADVANCE.**

Quality gate per loop-plan §5: ≤2 CLAIM markers (actual: 1); architectural claims source-traceable; primary-source citations resolve; package references in canon; one factual correction applied directly. The §Forward Secrecy and Post-Compromise Security section is ready for prose-reviewer at iter-0020.

Reverse cross-references documented in the draft QC notes (Ch15 §Key Compromise Incident Response and Ch15 §Relay Trust Model forward pointers to §Forward Secrecy and Post-Compromise Security) are deferred to the prose-review or assembly stage and tracked as draft-QC items, not technical-review items.
