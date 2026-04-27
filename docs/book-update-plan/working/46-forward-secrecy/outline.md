# 46 — Forward Secrecy and Post-Compromise Security — Outline

**ICM stage:** outline → ready for draft.
**Target chapter:** Ch15 (security architecture, Part III) — single-section extension.
**Total word target:** 1,500 words.
**Source:** `docs/reference-implementation/design-decisions.md` §5 entry #46 (sub-patterns 46a–46e).
**Why this is sixth in the priority list:** the existing P6 security architecture specifies encryption at rest, key hierarchy, and role-scoped access. Forward secrecy and post-compromise security are properties of the *session layer* — they govern what an attacker learns from a key compromise that happens before or after the session. The architecture currently assumes these properties but does not name or specify them. An implementation that omits them still passes the existing conformance checks; this section closes that gap. Signal protocol, MLS, and the Noise framework have normalized these properties across the industry; not specifying them creates a silent conformance hole.

---

## §A. New section in Ch15 — "Forward Secrecy and Post-Compromise Security"

**Insertion point:** between the existing `## Collaborator Revocation and Post-Departure Partition` section and the existing `## In-Memory Key Handling` section. The narrative logic: Collaborator Revocation closes the treatment of access control over time — who can participate, when participation ends, what happens to the shared record. Forward Secrecy opens the treatment of what protection the protocol provides *within* a session and what survives a session-key compromise. In-Memory Key Handling then addresses the in-process residence of those keys, completing the session-security trilogy before the chapter moves into supply chain concerns. Grouping these three sections together keeps the "what if keys are exposed" argument continuous and avoids scattering it across the chapter.

**Word target:** 1,500 words.

**H2:** `## Forward Secrecy and Post-Compromise Security`

---

### A.1 Why naming these properties matters (≈200 words)

- The four-layer defense model (Ch15 §Four Defensive Layers) and the key hierarchy (Ch15 §Key Hierarchy) address encryption at rest and role-scoped access. They are silent on *what happens to past and future messages when a session key is compromised today*.
- Forward secrecy is the property that past communications remain confidential after a key compromise. Post-compromise security is the property that future communications recover confidentiality after rotation following a compromise. Neither property is automatic — both require specific protocol design.
- Signal protocol established these as engineering defaults in 2013. MLS (RFC 9420, 2023) extended them to group messaging. The Noise framework provides a composable substrate for transport-layer variants. An architecture that skips this specification is implicitly relying on the transport layer or the implementer to supply these properties — a silent risk.
- Sub-pattern 46e (protocol-level forward secrecy commitment) closes that risk by making the commitment explicit and testable.
- Cross-reference to Ch15 §Threat Model — this section adds the "session-key compromise" row to the master threat taxonomy and fills in what each property guarantees and what it does not.
- Cross-reference to Ch15 §Key Compromise Incident Response — that section handles the organizational response when a KEK is compromised; this section specifies what the protocol guarantees about messages *before* and *after* that response completes.

---

### A.2 Sub-pattern 46a — Per-message ephemeral key derivation (≈250 words)

- The architecture's existing key hierarchy uses long-lived KEKs to wrap per-document DEKs. That construction protects data at rest. It does not provide forward secrecy for the *transport* of sync events between nodes, which travel through the relay as AES-256-GCM payloads.
- Per-message ephemeral key derivation means each sync event carries a freshly derived message key. When a message key is recovered by an attacker, it decrypts exactly that message and no others. Compromise of today's message key does not expose yesterday's messages or tomorrow's.
- Construction: each sync connection establishes a shared Diffie-Hellman (DH) secret through an ephemeral X25519 exchange. From that shared secret, HKDF-SHA256 derives a per-message key chain. Each message advances the chain; the prior message key is zeroed after use. An attacker who recovers one message key cannot reverse the chain to earlier keys.
- This is the ratchet input path — the symmetric state that sub-pattern 46b advances on every message.
- `Sunfish.Kernel.Sync` owns the ephemeral key exchange at sync session establishment. `Sunfish.Kernel.Security` owns the HKDF derivation and per-message key zeroing. The two packages interact at the session handshake boundary already defined in Ch14 §Sync Daemon Protocol.
- The honest boundary: per-message ephemeral derivation protects the transport layer. It does not protect the local database copy — that copy is AES-256-GCM encrypted under a DEK that persists until explicitly rotated. An attacker with both transport access and local database access needs to compromise both layers. That is a harder problem. It is not an impossible one.
- Cross-reference to Ch15 §Key Hierarchy for the DEK/KEK layer that persists locally; Ch14 §Sync Daemon Protocol for the session handshake this derivation operates within.

---

### A.3 Sub-pattern 46b — Sender and receiver ratchet (Double Ratchet) (≈300 words)

- Per-message ephemeral keys prevent retrospective decryption. The Double Ratchet pattern (Marlinspike and Perrin, Signal Protocol, 2016 [N]) adds *healing* — the ability for the session to recover confidentiality after a key compromise.
- The Double Ratchet combines two ratchets. The symmetric ratchet advances on every message: each outbound message derives its key from the ratchet state and advances that state forward. The Diffie-Hellman ratchet advances whenever a new DH public key from the other party arrives: the two ratchet states combine to produce a fresh shared secret, resetting the symmetric ratchet from a new entropy source that the attacker who held the previous state cannot predict.
- Forward secrecy comes from the symmetric ratchet's one-directionality — an attacker who recovers the ratchet state at time T can decrypt messages from T onward but cannot reverse the ratchet to decrypt messages from before T.
- Post-compromise security comes from the DH ratchet — once both parties have exchanged a new ephemeral key pair (which happens naturally as they communicate), the session state advances to a value the attacker who captured the old state cannot compute. The session heals automatically without requiring a deliberate re-keying procedure.
- The Signal Protocol specification (Marlinspike and Perrin, 2016) [N] describes this construction formally. The WhatsApp end-to-end encryption specification [N] applies it at scale. ProtonMail's symmetric ratchet [N] is a simpler variant without the DH step; it provides forward secrecy but not post-compromise security — the distinction matters for the threat model.
- The Noise framework [N] provides a composable substrate from which the Inverted Stack's session handshake can be constructed. NK (no identity, known responder) and KK (both parties known) patterns from Noise are relevant to sync sessions where nodes have enrolled device keypairs. The architecture does not mandate a specific Noise pattern variant; it mandates that whatever handshake is used satisfies sub-patterns 46a and 46b.
- `Sunfish.Kernel.Sync` extends its session layer to implement the Double Ratchet or a Noise-pattern equivalent. The exact variant is an implementation decision — the architectural commitment is the two properties (forward secrecy + post-compromise security), not the specific construction.
- Cross-reference to Ch14 §Sync Daemon Protocol for the session handshake that carries the ratchet state; Ch15 §Relay Trust Model for the relay's role as a ciphertext forwarder that observes ratchet messages without being able to decrypt them.

---

### A.4 Sub-pattern 46c — Automatic key rotation on suspected compromise or scheduled cadence (≈200 words)

- Post-compromise security through the DH ratchet is progressive — it heals as parties communicate. Automatic scheduled key rotation is the complementary mechanism for deployments where parties may be offline for extended periods between exchanges.
- Two triggers advance the ratchet state independently of normal message traffic:
  1. **Suspected compromise.** When #47 endpoint-compromise detection fires, or when sub-pattern 47b (HSM/secure-enclave separation) signals that key material may have been exposed, the session forces an immediate DH ratchet step. The compromised party generates a new ephemeral X25519 keypair, publishes the new public component, and marks the previous session state as poisoned. Peers receiving the new public key advance their own DH ratchet immediately.
  2. **Scheduled cadence.** Even without a detected compromise, the session forces a DH ratchet step on a configurable schedule — default every 90 days, matching the KEK rotation schedule from Ch15 §Key Hierarchy. Scheduled rotation closes the "long-lived session with no DH ratchet advance" gap that arises in deployments where users communicate frequently but peers stay online without reconnecting.
- `Sunfish.Kernel.Security` exposes the rotation trigger interface. `Sunfish.Kernel.Sync` executes the new ephemeral exchange at the next feasible session event. The trigger is a no-op if the DH ratchet has already advanced within the rotation window through normal message traffic.
- Cross-reference to Ch15 §Key Compromise Incident Response for the KEK rotation that runs in parallel; Ch15 §Endpoint Compromise: What Stays Protected for the #47 triggers that initiate a forced rotation.

---

### A.5 Sub-pattern 46d — Sealed sender (≈200 words)

- The relay forwards ciphertext between nodes. Even without decrypting payloads, the relay observes communication topology: which node is sending to which, at what rate, at what time of day. For most enterprise deployments that metadata is not sensitive. For deployments in healthcare, legal services, or politically sensitive environments, knowing that Node A communicated with Node B at 11:47 PM on the day of a board vote is itself sensitive information.
- Sealed sender hides the sender's identity from the relay. The sender encrypts their outer-envelope identity (the source node identifier) using the recipient's long-term public key before submitting the message to the relay. The relay sees the destination but not the source. The recipient unwraps the sealed sender identity after decrypting the message payload.
- The Signal Protocol's sealed-sender construction [N] implements this at scale. The Noise NK handshake pattern provides the necessary one-sided identity hiding at the transport layer.
- Sealed sender creates a validation asymmetry: without knowing the sender, the relay cannot validate that the sender is authorized. The architecture resolves this by moving authorization validation to the recipient node — the recipient checks the sender's identity and role attestation after unsealing. A relay that enforces authorization without seeing the sender identity requires a more complex zero-knowledge proof; that variant is deferred to a future volume.
- The current architecture implements sealed sender as an opt-in capability for metadata-sensitive deployments. It is not the default. `Sunfish.Kernel.Sync` exposes a sealed-sender policy flag in the session configuration; setting it switches the outer-envelope construction.
- Cross-reference to Ch15 §Relay Trust Model for the full discussion of what the relay observes and how to mitigate metadata exposure for sensitive deployments.

---

### A.6 Sub-pattern 46e — Protocol-level forward secrecy commitment (≈150 words)

- The preceding sub-patterns are implementation choices. Sub-pattern 46e is a declaration: the protocol specification states explicitly that forward secrecy and post-compromise security are required properties, not implementation details.
- Making the commitment explicit makes it testable. A conformance test for forward secrecy: given a recorded session state at time T, confirm that a message sent at time T-1 cannot be decrypted using any key material derivable from that state. A conformance test for post-compromise security: given a captured ratchet state at time T, after one DH ratchet advance, confirm that a message sent at time T+2 cannot be decrypted using any key material derivable from the captured state.
- These tests belong in `Sunfish.Kernel.Security`'s test suite alongside the existing key-zeroing and memory-locking validations. They are not integration tests — they are cryptographic property assertions that any conforming implementation must pass.
- The FAILED conditions at the close of this section name the three conditions that mean the primitive has not been met.

---

### A.7 FAILED conditions (≈100 words)

The forward secrecy and post-compromise security primitive fails when any of the conditions below holds. Any one of them voids the primitive's guarantees.

- **Past messages are decryptable from current key material.** Forward secrecy failure. Occurs when per-message keys are not derived from an advancing ratchet, or when old ratchet states are not zeroed after use.
- **Current key compromise propagates to future messages without rotation.** Post-compromise security failure. Occurs when the DH ratchet never advances — either because the session implementation uses only a symmetric ratchet (as in ProtonMail's variant) or because DH ratchet advance is conditional on manual operator action.
- **No automatic key rotation exists.** Neither property is self-enforcing without a rotation mechanism. An implementation that provides forward secrecy and post-compromise security in the protocol definition but offers no automatic trigger to advance the DH ratchet on suspected compromise or scheduled cadence has delivered a theoretical property without an operational one.

The kill trigger for this primitive is a FAILED condition that persists across three consecutive technical-review passes. A single intermittent failure is a defect to fix; a persistent failure signals that the session-layer implementation has not converged on the architectural commitment.

---

## §B. Code-check requirements

The draft references the following Sunfish namespaces by name only (per CLAUDE.md Sunfish reference policy — pre-1.0; package names not class APIs):

- `Sunfish.Kernel.Security` — HKDF derivation, per-message key zeroing, rotation trigger interface; existing in-canon package extended by this section
- `Sunfish.Kernel.Sync` — ephemeral key exchange at session establishment, Double Ratchet / Noise-pattern session layer, sealed-sender policy flag; existing in-canon package extended by this section

No new top-level namespace is introduced. Forward secrecy and post-compromise security extend existing kernel packages rather than requiring a new Foundation-tier coordination layer. This is consistent with the sunfish-package-roadmap.md entry for #46: "extends `Sunfish.Kernel.Security` + `Sunfish.Kernel.Sync`."

All references marked `// illustrative — not runnable` per the Sunfish reference policy.

---

## §C. Technical-review focus

For the `@technical-reviewer` pass:

- Verify the Double Ratchet algorithm description (sub-pattern 46b) against the Marlinspike and Perrin specification — confirm that the symmetric-ratchet / DH-ratchet terminology is accurate and that the post-compromise security claim is correctly attributed to the DH ratchet step, not the symmetric step.
- Verify that the Noise NK and KK pattern references (sub-pattern 46b) are accurate for the sync session topology — NK is correct for the case where the initiator is unauthenticated; KK is correct when both parties have enrolled keypairs. The Inverted Stack's enrolled-device model implies KK is the closer fit; flag if the draft conflates them.
- Verify sealed sender's authorization-validation asymmetry claim (sub-pattern 46d) — confirm that moving validation to the recipient node is the standard Signal Protocol resolution, not an architectural invention.
- Verify the HKDF-SHA256 derivation path (sub-pattern 46a) is consistent with Ch15 §Key Hierarchy, which also uses HKDF-SHA256 for subordinate key derivation.
- Trace every architectural claim back to v13 / v5 source papers OR mark as new architectural commitment surfaced through universal-planning review (per design-decisions §5 #46).
- Verify ProtonMail symmetric ratchet claim — confirm that ProtonMail uses a symmetric ratchet only (not DH-ratchet) and that the "forward secrecy but not post-compromise security" distinction is accurate.

---

## §D. Prose-review focus

For the `@prose-reviewer` + `@style-enforcer` pass:

- Active voice throughout. "Each message advances the chain" — not "the chain is advanced by each message."
- No hedging on property guarantees. State what each property provides and what it does not. "Forward secrecy means past messages are safe; it does not mean the local database copy is safe" — not "forward secrecy may provide protection for historical messages under certain conditions."
- Maintain the Part III specification register — this is the reference architecture chapter; every claim must be precise enough to implement against.
- No academic scaffolding. No "this section demonstrates" or "as we have seen."
- No restating Part I architecture. Ch15 assumes the reader has read Part I and the earlier Ch15 sections.
- Paragraph length cap: 6 sentences.
- Technical term introductions: X25519, HKDF, Double Ratchet, and Noise are specialist terms — introduce each once with its full expansion (e.g., "X25519, the Diffie-Hellman function over Curve 25519") and use the short form thereafter. Do not over-explain; the audience is practitioners.

---

## §E. Voice-check focus (HUMAN STAGE — not autonomous)

For the human voice-pass:

- This section is technically dense. A brief framing observation from the author's own experience — a moment of recognizing that a system's "encrypted" claim did not mean historical messages were safe — would anchor the reader before the cryptographic construction lands.
- The sealed-sender section (46d) has a natural rhetorical opening: the metadata-is-the-message observation. Signal's sealed sender emerged from exactly this recognition. The author may have a real-world encounter with this — a situation where who communicated with whom was more sensitive than what was said.
- Calibrate Sinek register lightly per `feedback_voice_sinek_calibration.md` — the specification register dominates in Part III; personal voice is seasoning, not scaffolding.

---

## §F. Citations

The draft adds these to Ch15's reference list (IEEE numeric, continuing from the existing [13] — next reference is [14]):

- M. Marlinspike and T. Perrin, "The Double Ratchet Algorithm," Signal Foundation, Nov. 2016. [Online]. Available: https://signal.org/docs/specifications/doubleratchet/
- Open Whisper Systems (M. Marlinspike), "The X3DH Key Agreement Protocol," Signal Foundation, Nov. 2016. [Online]. Available: https://signal.org/docs/specifications/x3dh/
- T. Perrin, "The Noise Protocol Framework," 2018. [Online]. Available: https://noiseprotocol.org/noise.html
- Internet Engineering Task Force (IETF), "The Messaging Layer Security (MLS) Protocol," RFC 9420, Jul. 2023. [Online]. Available: https://www.rfc-editor.org/rfc/rfc9420
- WhatsApp Inc., "WhatsApp Encryption Overview," 2021. [Online]. Available: https://www.whatsapp.com/security/WhatsApp-Security-Whitepaper.pdf
- N. Borisov, I. Goldberg, and E. Brewer, "Off-the-Record Communication, or, Why Not To Use PGP," in *Proc. ACM Workshop on Privacy in the Electronic Society (WPES)*, Oct. 2004, pp. 77–84.

Citation numbers assigned in order of first appearance in the draft; [14]–[19] are provisional placeholders until the draft allocates them sequentially.

---

## §G. Cross-references to add

Inside the new section:

- Ch15 §Forward Secrecy and Post-Compromise Security → Ch15 §Threat Model (adds the session-key-compromise row)
- Ch15 §Forward Secrecy and Post-Compromise Security → Ch15 §Key Compromise Incident Response (KEK rotation that runs in parallel with ratchet advance)
- Ch15 §Forward Secrecy and Post-Compromise Security → Ch15 §Key Hierarchy (DEK/KEK layer this section complements)
- Ch15 §Forward Secrecy and Post-Compromise Security → Ch15 §Relay Trust Model (relay as ciphertext forwarder; sealed-sender metadata mitigation)
- Ch15 §Forward Secrecy and Post-Compromise Security → Ch14 §Sync Daemon Protocol (session handshake that carries ratchet state and ephemeral keys)
- Ch15 §Forward Secrecy and Post-Compromise Security → Ch15 §Endpoint Compromise: What Stays Protected (#47 triggers that force a ratchet step under 46c)
- Ch15 §Forward Secrecy and Post-Compromise Security → Ch15 §Collaborator Revocation and Post-Departure Partition (#45 revocation as one trigger for forced ratchet advance)
- Ch15 §Forward Secrecy and Post-Compromise Security → Ch15 §Key-Loss Recovery (#48 — interaction: recovery reconstitutes KEK custody but does not reconstitute ratchet state; forward secrecy for the pre-recovery period is not retroactively recovered)

Reverse cross-references to add in existing sections:

- Ch15 §Key Compromise Incident Response → add a forward pointer to §Forward Secrecy and Post-Compromise Security for the session-layer complement to the KEK incident procedure.
- Ch15 §Relay Trust Model → add a forward pointer to §Forward Secrecy and Post-Compromise Security §46d (sealed sender) as the mechanism for metadata-sensitive relay deployments.

---

## §H. Subagent prompt for the draft stage

The next iteration (`outline → draft`) will invoke `@chapter-drafter` with this prompt:

> Draft one new section for *The Inverted Stack*: `## Forward Secrecy and Post-Compromise Security` for Ch15 (~1,500 words), inserted between the existing `## Collaborator Revocation and Post-Departure Partition` section and the existing `## In-Memory Key Handling` section.
>
> Source: outline at `docs/book-update-plan/working/46-forward-secrecy/outline.md`. Follow the section structure and word targets exactly. Voice: Part III specification register — precise enough to implement against, no hedging. Active voice throughout. No academic scaffolding. No re-introducing the architecture (Ch15 assumes Part I + earlier Ch15 sections).
>
> Sub-patterns to cover in order: 46a per-message ephemeral key derivation, 46b Double Ratchet sender/receiver ratchet, 46c automatic key rotation (compromise-triggered + scheduled), 46d sealed sender, 46e protocol-level forward secrecy commitment. Close with the FAILED conditions block.
>
> Sunfish references: package names only (`Sunfish.Kernel.Security`, `Sunfish.Kernel.Sync`) — no class APIs, no method signatures. No new top-level namespace. Mark any code snippets `// illustrative — not runnable`.
>
> Citations: IEEE numeric. Add the six sources listed in outline §F to Ch15's reference list (continuing from existing [13]; next is [14]). Assign numbers sequentially in order of first appearance in the draft.
>
> Cross-references: per outline §G — the draft must wire all listed cross-references and add the two reverse pointers in existing sections.
>
> Insertion mechanics: write the new H2 section directly into the existing chapter file at the specified insertion point. Preserve existing H2 anchor structure and H1 frontmatter. Update Ch15's reference list with the six new entries.

---

## §I. Quality gate for `outline → draft`

Per loop-plan §5: outline has all section headers + bullet points (✓ §A above, subsections A.1–A.7); word count target estimated (✓ 1,500 words); subagent prompt prepared (✓ §H above). Gate passes.

---

**Estimated next-iteration duration (draft stage):** 45–60 minutes. Single-section extension; shorter than the 48 and 45 drafts. Schedule next fire 1 hour after this one to allow context-cache cooldown and human-review window.
