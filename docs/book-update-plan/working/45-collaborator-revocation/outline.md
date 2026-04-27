# 45 — Collaborator Revocation and Post-Departure Partition — Outline

**ICM stage:** outline → ready for draft.
**Target chapters:** Ch15 (security architecture, Part III) + Ch20 (UX, Part IV).
**Total word target:** 2,800 words (Ch15 ~2,000; Ch20 ~800).
**Source:** `docs/reference-implementation/design-decisions.md` §5 entry #45 (sub-patterns 45a–45f).
**Why this is third in the priority list:** the departing-employee scenario is universal. The current book assumes collaborators remain collaborative — #18 (delegated capability) handles granting access; nothing handles revoking it. Every enterprise deployment, every partnership dissolution, every family-business dispute eventually needs to answer: what happens after someone leaves?

---

## §A. New section in Ch15 — "Collaborator Revocation and Post-Departure Partition"

**Insertion point:** between the existing `## Offline Node Revocation and Reconnection` section and the existing `## In-Memory Key Handling` section. The narrative arc is deliberate: the offline revocation section handles the case where a node is offline when a revocation fires — a protocol-level concern. The new section handles the case where revocation is the intentional act, initiated by an administrator or party with authority — a policy-level concern. In-Memory Key Handling follows as the final procedural layer covering key lifecycle after any revocation completes. Inserting between offline revocation and in-memory handling keeps the revocation family grouped while separating the two conceptually distinct halves: what happens to an already-offline node (handled above) versus what happens when you deliberately remove someone (this new section).

**Word target:** 2,000 words.

**H2:** `## Collaborator Revocation and Post-Departure Partition`

### A.1 Why this matters (≈250 words)

- Extension #18 (delegated capability) handles the grant side of collaboration: scoped third-party write authority, trustee designation, role distribution. Revocation is the UNGRANT. The book currently has no primitive for it.
- Real-world departure scenarios that force the question: an employee leaves the company — amicably or otherwise; a consultant finishes an engagement; a partnership dissolves; a board vote removes a corporate officer; a family dispute breaks a shared-data arrangement; a contractor relationship ends with a dispute. Each of these produces a former collaborator who has a local cached copy of data they should no longer be able to modify or receive.
- The architecture is honest about the physical impossibility of remote deletion: a revoked collaborator's local cached copy is still readable for already-synced data. The architecture does not claim otherwise. What it provides is: the revoked party cannot write to shared state going forward, cannot decrypt newly-encrypted state, and cannot receive new events. Legal enforcement of destruction for the cached copies is the legal layer's responsibility.
- The FAILED conditions from design-decisions §5 #45 are the specification's honest boundary conditions: revoked collaborator can still write to shared state (architecture failure); revocation fails to propagate to other peers within reasonable time (protocol failure); no audit trail of the revocation event (compliance failure).
- Cross-reference to Ch15 §Role Attestation Flow (the mechanism this section terminates) and Ch15 §Key Compromise Incident Response (compromise-driven revocation as upstream cousin to departure-driven revocation).

### A.2 Sub-pattern 45a — Explicit revocation event (≈250 words)

- A revocation is a cryptographically attested grant termination. It is not the absence of a future grant; it is a signed, timestamped event that declares a specific collaborator's access authority ended at a specific moment.
- The explicit event serves three purposes that the mere absence of a new key bundle does not serve: (1) it is observable by all other peers who need to stop accepting writes from the revoked party; (2) it is the timestamp anchor for the data-at-risk window in post-departure partition; (3) it is the entry in the legally defensible audit trail that proves when access ended.
- Event structure: carries the revoked collaborator's node identifier(s), the revoking administrator's signature, the UTC timestamp, the scope of revocation (role, data class, or full account), and a revocation reason code (departure, contract-end, dispute, security-incident). The reason code is optional but recommended for regulated-industry deployments where auditors distinguish voluntary departure from security-incident response.
- The revocation event travels through the same administrative event channel as role attestations and key bundles — the same encrypted log that application data traverses. The sync daemon's send-tier filtering activates the moment the revocation event reaches a peer: peers stop routing writes from the revoked collaborator to shared state.
- Cross-reference to Ch15 §Offline Node Revocation and Reconnection for the relay-layer enforcement that complements this event-layer mechanism: the relay enforces revocation at the handshake layer; the revocation event enforces it at the application-data layer.

### A.3 Sub-pattern 45b — Post-revocation key rotation (≈350 words)

- Revocation without key rotation provides weaker guarantees than the architecture can deliver. If the revoked collaborator's copy of the current KEK remains valid, they can still decrypt data that was written under that KEK and re-encrypted after their departure — the logical "new" data is still ciphertext they can decrypt. Key rotation closes this window.
- The rotation procedure is the same as the routine role-membership-change rotation described in Ch15 §Role Attestation Flow — but with one additional constraint: the new KEK is generated before the revoked collaborator is notified, and the revoked collaborator is excluded from the new bundle set. Notification sequence matters.
  - Step 1: Administrator generates the new KEK from a fresh entropy source.
  - Step 2: Administrator wraps the new KEK for every currently-authorized member excluding the departing party.
  - Step 3: The revocation event (45a) and the new key bundle are published simultaneously as administrative events in the log.
  - Step 4: The background DEK re-wrapping job processes existing documents, wrapping DEKs under the new KEK.
  - Step 5: The old KEK is discarded after all authorized members have confirmed receipt of the new bundle. The revoked node, which never received the new bundle, cannot decrypt documents re-wrapped under the new KEK.
- The re-wrapping scope matters. If the departing collaborator had access only to a subset of roles, rotation applies only to those roles. Rotating all organizational KEKs on every departure is operationally expensive and architecturally unnecessary — the access scope is bounded by role, and rotation is scoped to match.
- Key rotation does not remove data from the revoked collaborator's local cache that was already decrypted before departure. Rotation prevents forward access to newly-written or newly-re-encrypted state. The honest architectural boundary: past ciphertext that was decryptable before departure remains decryptable because the old KEK is in the collaborator's cache. The legal layer handles destruction obligations; the architecture handles the forward window.
- `Sunfish.Kernel.Security` manages the re-wrapping background job and the discard broadcast. Cross-reference to Ch15 §Key Hierarchy for the DEK/KEK envelope mechanics that make rotation work.

### A.4 Sub-pattern 45c — Cached-copy management (≈200 words)

- A revoked collaborator's node retains its local cache of all data synced before revocation. The architecture is explicit: this data is readable on their device. It was readable before revocation; revocation does not change its decryptability with the old KEK.
- The architecture provides two controls for the period between revocation and legal-layer enforcement of destruction:
  - **Write quarantine:** the revoked node's writes are quarantined at the circuit breaker on any future reconnection attempt. Even if the node tries to submit locally-accumulated writes after revocation, those writes enter the quarantine queue and await administrator decision before any promotion.
  - **Forward isolation:** the sync daemon's send-tier filtering ensures the revoked node receives no new events from the moment the revocation event propagates to each peer. The revoked collaborator's cache is frozen at the revocation timestamp — it does not grow.
- The architecture does not and cannot delete data from a remote device. Deployments that require demonstrated destruction — regulated industries, GDPR Article 17 obligations, data subject deletion requests where a former employee was the data subject — enforce destruction through MDM (Mobile Device Management) policies, device wipe procedures, and contractual obligations in employment and collaboration agreements. The architecture supports this with the audit trail (45f) that documents the data-at-risk window and the frozen-cache timestamp.
- Cross-reference to Ch15 §GDPR Article 17 and Crypto-Shredding for content-erasure obligations on the originator's side; cached-copy management on the revoked party's device is a separate obligation.

### A.5 Sub-pattern 45d — Revocation propagation (≈200 words)

- A revocation event is only as effective as its propagation reach. Other peers who do not learn of the revocation continue accepting writes from the revoked collaborator — a protocol failure that the FAILED conditions explicitly flag.
- Propagation follows the same gossip path as other administrative events. The relay receives the revocation event and forwards it to all subscribing peers. Peers update their send-tier filtering immediately upon receipt: they stop routing writes from the revoked node identifier to shared log state, and they reject incoming gossip events originating from the revoked node.
- Propagation latency matters. Under normal relay connectivity, revocation propagates to all online peers within seconds. Offline peers receive the revocation event on next reconnection and immediately enforce it.
- The propagation guarantee matches the architecture's general availability posture: the relay guarantees delivery to all currently-online subscribers; offline subscribers receive the event when they next connect. This is the correct posture. Demanding synchronous global propagation before revocation takes effect would convert the revocation primitive into a CP operation, requiring the system to be fully connected before the action can complete. Revocation is AP: it takes effect on each peer the moment the peer receives the event.
- The partition case: if a peer is offline when revocation fires and the revoked collaborator sends a write to that offline peer before it learns of the revocation, the circuit breaker on the offline peer's reconnection handles the write — quarantine, not silent promotion.

### A.6 Sub-pattern 45e — Data partition for dissolution/dispute (≈400 words)

This sub-pattern addresses the hardest case: not a departure where one party leaves and the other retains the shared data, but a dissolution where both parties are separating and each needs their own slice of the shared data going forward. A business partnership splits in two. A married couple with shared finances separates. Two co-founders each take a portion of a shared organizational dataset.

- The partition operation is structurally different from revocation. Revocation terminates one collaborator's access and leaves the data intact for the remaining party. Partition creates two independent datasets from a shared one, with each party holding a controlled fork.
- The partition procedure:
  1. The parties — or an authorized administrator — define the partition boundary: which data objects, which roles, which time ranges belong to which successor entity.
  2. A partition event is published to the log, signed by the authorizing party (administrator, legal trustee, or both parties together). The partition event carries the boundary definition and the timestamp.
  3. Each party's node constructs a local copy scoped to their partition boundary. The shared log continues to exist as a read-only historical artifact; the two successor logs diverge forward from the partition event.
  4. New KEKs are generated for each successor entity. Each party's successor log is re-encrypted under their new KEK. The other party's old KEK cannot decrypt the successor log going forward.
- The key asymmetry: data written to the shared log before the partition event is part of the historical record. Each party retains a copy of that history as of the partition timestamp. Neither party can delete the other's historical copy — the architecture provides no mechanism for retroactive deletion of a shared log. Post-partition writes to each successor log are private to the respective entity.
- Legal context: the partition event is the architectural artifact that a court order or settlement agreement references. The audit trail (45f) records who authorized the partition, what boundary was drawn, and when. Disputes over the partition boundary are legal disputes; the architecture enforces the boundary that was cryptographically attested, not the boundary that one party claims should have been attested.
- This sub-pattern is the most complex in the revocation family and the one with the greatest divergence from standard OAuth/OCSP/certificate-revocation analogues. Existing certificate revocation (OCSP, CRL) handles single-party revocation; it does not handle bilateral data partition with successor-entity key separation. This architecture handles both.
- `Sunfish.Kernel.Security` manages the partition event and the successor-entity KEK generation. The data-boundary definition is an application-layer responsibility; `Sunfish.Kernel.Security` enforces the cryptographic separation once the boundary is declared.

### A.7 Sub-pattern 45f — Revocation-event audit trail (≈200 words)

- Every revocation event, key rotation triggered by revocation, partition authorization, and revocation dispute is recorded as a signed event in the encrypted audit log. `Sunfish.Kernel.Audit` manages revocation-event records.
- Each record carries: the revoked collaborator's node identifier(s); the revoking administrator's identity and signature; the UTC timestamp; the revocation scope; the KEK rotation trigger status (rotation initiated, rotation completed, old KEK discarded); the partition boundary (if 45e is invoked); and the data-at-risk window (the interval from the compromised or departing collaborator's earliest key possession to the confirmed rotation completion).
- The audit trail is the legally defensible record of when access ended. For employment disputes, it is the evidence of when the former employee's data access was terminated. For partnership dissolutions, it is the partition authorization record. For regulated industries, it is the access-termination artifact that HIPAA, SOX, PCI-DSS, and similar frameworks require.
- The audit trail for revocation events composes with the same multi-party signed-event substrate as the key-loss recovery audit trail (Ch15 §Key-Loss Recovery — sub-pattern 48f). The two mechanisms share the `Sunfish.Kernel.Audit` substrate; their record schemas are distinct.
- The FAILED condition this sub-pattern guards against: a revocation event without a corresponding audit trail entry. If the audit trail is absent or incomplete, the deployment cannot prove when access ended — the foundation of any post-departure compliance demonstration.

---

## §B. New section in Ch20 — "Revocation UX"

**Insertion point:** between the existing `## Key-Loss Recovery UX` section and the existing `## Accessibility as a Contract` section. Key-Loss Recovery UX and Revocation UX are both in the "policy has a UX surface" family — each is the user-facing half of a Ch15 specification section. Keeping them adjacent is deliberate; the reader who has just worked through key-loss recovery flows brings the right mental model to revocation flows. Accessibility as a Contract follows as the transversal concern that applies to all of the flows above.

**Word target:** 800 words.

**H2:** `## Revocation UX`

### B.1 Initiating revocation — the administrator's flow (≈200 words)

This subsection is the UX surface for sub-patterns 45a (revocation event) and 45b (key rotation). It is written from the administrator's perspective — the person performing the revocation — rather than the revoked party's perspective.

- The revocation action appears in the team administration panel, not in any per-user settings. This is intentional: revocation is an administrative act, and surfacing it at the user level creates confusion about whose action it is.
- The administrator selects the departing collaborator from the team member list and chooses "Remove and revoke access." A confirmation dialog names the scope: which roles will be revoked, that a key rotation will be triggered, and the estimated time for re-wrapping to complete across the organization's document set. The administrator does not need to understand the cryptographic mechanism; they need to understand what the action does and how long it takes.
- After confirmation, the UX shows a revocation-in-progress state: "Revoking [name]'s access and rotating role keys. This may take a few minutes while documents are re-encrypted." The team can continue using the application during re-wrapping; documents remain accessible under the current KEK until re-wrapping completes.
- Do not surface the technical key-rotation terminology ("KEK re-wrapping," "DEK re-encryption") to the administrator. Surface the business outcome: "access revoked, documents secured."
- Cross-reference to Ch15 §Collaborator Revocation and Post-Departure Partition §Sub-pattern 45b for the key-rotation specification.

### B.2 Communicating the action's effects — what the revoked party experiences (≈200 words)

This subsection covers sub-pattern 45c (cached-copy management) from the revoked party's perspective — what they see if they open the application after revocation.

- When the revoked collaborator's node next attempts to sync, the relay rejects the handshake with `ERR_KEY_REVOKED`. The application surfaces a plain-language message: "Your access to this team has ended. Your local data is still accessible on this device, but you can no longer sync or make changes to the team's shared data."
- The message is honest about what the revoked party retains: their local cache of previously-synced data is still readable. The message does not imply their local copy has been deleted — that would be false and legally significant. The architecture does not delete data from the revoked party's device.
- If the revoked collaborator was using the application at the moment revocation propagated — an online session — the application transitions to a read-only local state without a forced exit. The node health indicator shifts to red with the same plain-language message. Active edits in progress are preserved in the local CRDT log; they cannot be submitted to shared state. The user is not stranded with an empty screen or a crash. They see their local data. They see the access status.
- For a departure scenario where the revocation is expected (the employee initiated their own departure), the message is matter-of-fact. For a scenario where it is unexpected (a dispute-triggered revocation), the message's tone may feel abrupt. The architecture cannot calibrate the message to the emotional context; it can only be factually accurate.

### B.3 Surfacing the audit trail — what the administrator can verify (≈200 words)

This subsection covers sub-pattern 45f (audit trail) from the administrator's UX perspective, and sub-pattern 45e (data partition) for the administrator who needs to manage a dissolution scenario.

- The team administration panel includes an "Access log" or "Security events" view. Revocation events appear here with: timestamp, the revoked collaborator's name, the scope of revocation, the key-rotation completion status, and the data-at-risk window. The administrator can verify when revocation was confirmed and provide this record to legal or compliance teams.
- The access log is not a developer artifact. It is a compliance artifact surfaced in the team administration panel with the same plain-language register as the rest of the UX. "Access revoked: [name]. Date: [timestamp]. Role keys rotated: complete. Documents affected: [count]." The count of affected documents lets the administrator communicate the scope to legal counsel without needing to extract data from a raw event log.
- For the data-partition scenario (45e), the administration panel exposes a "Partition workspace" flow — a guided wizard that walks the administrator through defining the boundary, confirming both parties, and initiating the partition operation. The wizard is explicitly for dissolution scenarios and is not surfaced in the standard administration panel; it requires a deliberate navigation path to access. The partition flow's confirmation screen names the legal effect: "This creates two separate workspaces. Each party keeps their own data from this point forward. Historical shared data is preserved in both."
- The audit log for partition events carries additional fields: the boundary definition, the authorizing parties, and the partition timestamp. Both successor entities receive a copy of the partition event record in their respective audit logs.
- Cross-reference to Ch15 §Collaborator Revocation and Post-Departure Partition §Sub-pattern 45f for the event records this UX surfaces.

### B.4 The departure moment — framing for the voice-check pass (≈200 words, placeholder)

This subsection is a structural placeholder to signal to the human voice-check author that the departure scenario carries emotional weight beyond the protocol description. The draft author should write this as a brief, factual transition — one to two sentences that acknowledge the human reality of revocation without editorializing. The voice-check author (human only) adds the anecdote or framing that makes the section feel authored rather than assembled.

- Candidate framing approaches (for the human voice-check pass to choose among):
  - The departing employee who realizes their work laptop no longer connects to the company system as they are packing their desk.
  - The business partner who receives the access-ended message on the day a court-mediated settlement takes effect.
  - The administrator who processes an access revocation for an employee who had been a colleague for a decade.
- None of these are crisis narratives — they are ordinary professional departures that happen every week in organizations that use shared data systems. The architecture handles them the same way it handles a key compromise: with a signed event, a key rotation, and an audit trail. The human context is different; the protocol is the same.
- Do not add the anecdote in the draft stage. Mark this section with a <!-- voice-check: add departure anecdote here --> comment.

---

## §C. Code-Check Requirements

The draft references the following Sunfish namespaces by name only (per CLAUDE.md Sunfish reference policy — pre-1.0; package names not class APIs):

- `Sunfish.Kernel.Security` — in canon; owns the revocation broadcast, KEK re-wrapping background job, and old-KEK discard signal. The revocation-event publication and propagation mechanism lives here.
- `Sunfish.Kernel.Audit` — forward-looking (book-committed, not yet scaffolded; source extension #48, extended by #45); owns the revocation-event audit record, the partition authorization record, and the data-at-risk window calculation. Mark all references `// illustrative — not runnable`.
- `Sunfish.Foundation.Recovery` — forward-looking (adr-accepted, per ADR 0046; not yet scaffolded); referenced in the partition scenario (45e) for the successor-entity KEK separation. The sunfish-package-roadmap anticipatory entry for #45 confirms this extension uses `Sunfish.Foundation.Recovery` for the partition key management path, alongside `Sunfish.Kernel.Security`. Mark all references `// illustrative — not runnable`.

All three namespaces should be introduced in Ch15 at first use of their architectural role; Ch20 cross-references Ch15 rather than re-introducing them.

**Note for the code-check stage:** `Sunfish.Kernel.Audit` was introduced in extension #48; the code-check report for #48 already flags it as forward-looking. Extension #45 extends the same audit substrate for revocation and partition records. The code-check report for #45 should note this dependency and confirm that the #48 code-check finding is still unresolved before marking #45's audit references clean.

---

## §D. Technical-Review Focus

For the `@technical-reviewer` pass:

- **Insider-threat literature:** the departing-employee scenario maps directly to the insider-threat threat model. Verify that the revocation primitive's FAILED conditions — specifically "revoked collaborator can still write to shared state" — align with the documented failure modes in CERT's insider-threat studies and NIST SP 800-12 access management guidance. The claim that other peers "stop accepting writes from the revoked collaborator" needs a traceable source for the propagation mechanism, or an explicit acknowledgment that it is a new architectural commitment.
- **OAuth token revocation:** OAuth 2.0 Token Revocation (RFC 7009) is the canonical prior art for programmatic access revocation. Verify that the architecture's revocation-event model is consistent with RFC 7009's intent (invalidation at the authorization server level) while acknowledging the difference: in a local-first system, there is no central authorization server, so the revocation event must propagate to peers. Cite RFC 7009 and note the structural divergence.
- **OCSP / CRL certificate revocation:** OCSP (Online Certificate Status Protocol, RFC 6960) and CRL (Certificate Revocation List, RFC 5280) are the X.509 precedents for revocation propagation. The key insight from CRL is the gap between issuance and propagation — a revoked certificate remains trusted by relying parties who have not yet received the CRL. Verify that the architecture's revocation propagation model is honest about the equivalent gap (revocation takes effect on each peer when the peer receives the event, not when the administrator signs it). Cite RFC 6960 and RFC 5280.
- **AWS IAM credential rotation:** AWS IAM's access key rotation and immediate invalidation procedures are the enterprise deployment analogue. Verify the claim in §A.3 that "the new KEK is generated before the revoked collaborator is notified" is consistent with AWS IAM's documented security practice for emergency access termination (IAM policies, access key deactivation, and the recommended offboarding sequence). The architectural claim is that notification sequence prevents a race condition; this should be traceable to a source or marked as new architectural commitment.
- **Google Workspace account suspension:** Google Workspace's admin console suspension flow is the product-level analogue for the §B.1 administrator UX. The book claims that revocation takes effect without requiring the application to force-quit the revoked user's active session. Verify whether Google Workspace's suspension procedure has the same property (suspension is asynchronous; the active session may continue briefly), which would validate the architecture's "transition to read-only local state without a forced exit" claim.
- **Bilateral data partition:** no standard OAuth/OCSP/CRL analogue covers the bilateral data partition described in §A.6 (sub-pattern 45e). The technical reviewer should confirm that this sub-pattern is genuinely novel relative to existing literature, or surface a prior-art reference (divorce-mediation software, joint-account closure protocols, shared-infrastructure separation procedures in corporate spin-offs). If novel, the section must acknowledge it explicitly rather than implying sourcing from existing revocation literature.
- **CRDT semantics for partition:** verify that splitting a shared CRDT log into two successor logs is well-defined under the CRDT model used by the architecture (Yjs/yrs or Loro). The claim that "the two successor logs diverge forward from the partition event" needs a clear statement of how CRDT operation identifiers are handled — specifically, whether operations from the shared history retain their identifiers in both successor logs, and whether future operations by one party could accidentally produce identifier collisions with the other's. Trace to Yjs/yrs documentation or mark as new architectural commitment.
- **Trace every architectural claim** to v13/v5 source papers OR mark as new architectural commitment surfaced through universal-planning review (per design-decisions §5 #45). The revocation primitive is a new extension; none of its sub-patterns appear in v13/v5. The section should acknowledge this explicitly in its opening.

---

## §E. Prose-Review Focus

For the `@prose-reviewer` + `@style-enforcer` pass:

- Active voice throughout. "The administrator revokes access" — not "access is revoked." "The relay rejects the handshake" — not "the handshake is rejected by the relay."
- Specification register for Ch15. Positive declarative statements throughout. "The revocation event carries the revoked collaborator's node identifier" — not "the revocation event should carry" or "could include."
- Tutorial register for Ch20. Direct second-person address for UX instructions. "Do not surface the technical key-rotation terminology" — not "the developer should avoid surfacing."
- The data-partition sub-section (§A.6) is the most complex and the most legally freighted. Keep the architecture description separate from the legal context. The architecture paragraph states what the system does; the legal-context paragraph names the human situations it serves. Do not blend them.
- The cached-copy management section (§A.4) carries the book's most honest architectural limitation in this extension: the architecture cannot delete data from a remote device. Write this limitation as a direct declarative statement, not as a hedge. "The architecture does not and cannot delete data from a remote device" — not "it should be noted that deletion may not be possible."
- No hedging on the propagation timing claim. "Revocation propagates to all online peers within seconds under normal relay connectivity" — not "revocation typically propagates relatively quickly." Specify the bound honestly and name the exception (offline peers receive the event on reconnection).
- Paragraph length cap: 6 sentences.
- The FAILED conditions must appear explicitly in Ch15 as a named block — not buried in prose. Same treatment as extension #43's FAILED conditions block.

---

## §F. Voice-Check Focus (HUMAN STAGE — not autonomous)

For the human voice-pass:

- **The departing employee anecdote.** The most grounded opening for this section is a brief story from the administrator's perspective: processing an access revocation for a competent, trusted employee who is leaving for a better opportunity. The action is necessary, the relationship ends on good terms, and the protocol is exactly as impersonal as it needs to be. The architecture handles the access change; the human relationship is the author's domain. This framing avoids turning the section into a threat narrative (the malicious departing employee) while anchoring it in the reality that access revocation is a normal, regular operation.
- **The family-business or partnership dispute anecdote.** Candidate for the §B.4 placeholder: a partnership dissolves over a disagreement — not a dramatic breakdown, but the kind of ordinary professional separation where two people who started something together decide to take different paths. The data partition sub-section (45e) addresses this directly. The author may have a version of this story — a business that pivoted, a project that forked, a collaboration that reached its natural end. The departure anecdote need not be adversarial to be effective.
- **Board removal of corporate access.** A third candidate: a board vote that terminates an officer's access to financial systems. The revocation-event audit trail (45f) is the artifact that demonstrates the access ended at the board meeting, not before or after. This anecdote frames the compliance value of the audit trail concretely, and it is a scenario that the enterprise customer (Ch19) will recognize immediately.
- **The connective tissue between Ch15 §Collaborator Revocation and Ch20 §Revocation UX.** A sentence in each section pointing to the other, as with the #48 key-loss pair. Ch15 points forward to Ch20 for the administrator and revoked-party UX surfaces; Ch20 points back to Ch15 for the specification of what the revocation event commits to cryptographically.
- Calibrate Sinek register lightly per `feedback_voice_sinek_calibration.md` memory — do not over-mechanize the prose with deliberate-pacing hammering.

---

## §G. Citations

The draft adds these to Ch15's reference list (IEEE numeric, continuing after the existing [7]):

**[8] Internet Engineering Task Force (IETF), "OAuth 2.0 Token Revocation," RFC 7009, Aug. 2013.** [Online]. Available: https://www.rfc-editor.org/rfc/rfc7009

**[9] Internet Engineering Task Force (IETF), "X.509 Internet Public Key Infrastructure Online Certificate Status Protocol — OCSP," RFC 6960, Jun. 2013.** [Online]. Available: https://www.rfc-editor.org/rfc/rfc6960

**[10] Internet Engineering Task Force (IETF), "Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile," RFC 5280, May 2008.** [Online]. Available: https://www.rfc-editor.org/rfc/rfc5280

**[11] National Institute of Standards and Technology (NIST), "An Introduction to Computer Security: The NIST Handbook," SP 800-12, Oct. 1995 (rev. 2017).** [Online]. Available: https://csrc.nist.gov/publications/detail/sp/800-12/rev-1/final — for access control and account management principles.

**Note on citation numbering:** Ch15 currently has seven references ([1]–[7]). The new citations for extension #45 begin at [8] and continue sequentially. The technical reviewer must confirm the first-appearance order in the draft and assign final numbers accordingly. Ch20 cross-references Ch15's citation list. No new citations are needed in Ch20 unless a Ch20-specific source surfaces during drafting.

**Citations to verify and possibly add (technical reviewer action required):**

- A CERT insider-threat study or NIST SP 800-53 access management control (AC-2 Account Management) for the insider-threat motivation in §A.1. Candidate: CERT Coordination Center, "Common Sense Guide to Mitigating Insider Threats," 6th ed., Software Engineering Institute, 2019.
- AWS IAM documentation for the notification-sequence claim in §A.3. Candidate: AWS, "Security best practices in IAM," AWS Documentation, 2024. Available: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
- Google Workspace admin documentation for the session-continuation claim in §B.2. Candidate: Google, "Suspend or restore a user," Google Workspace Admin Help, 2024. Available: https://support.google.com/a/answer/33312

---

## §H. Cross-References to Add

Inside the new sections:

- Ch15 §Collaborator Revocation → Ch15 §Role Attestation Flow (the grant mechanism this section terminates; key rotation procedure is identical to the membership-change rotation described there)
- Ch15 §Collaborator Revocation → Ch15 §Offline Node Revocation and Reconnection (relay-layer enforcement that complements the application-layer revocation event; the offline-node circuit-breaker quarantine handles writes accumulated before the revoked node reconnects)
- Ch15 §Collaborator Revocation → Ch15 §Key Compromise Incident Response (the compromise-triggered rotation is the upstream cousin to the departure-triggered rotation; same procedure, different trigger)
- Ch15 §Collaborator Revocation → Ch15 §Key Hierarchy (DEK/KEK envelope mechanics that make targeted role-scoped rotation possible without re-encrypting all document bodies)
- Ch15 §Collaborator Revocation → Ch15 §Key-Loss Recovery §Recovery-event audit trail (sub-pattern 48f and sub-pattern 45f share the `Sunfish.Kernel.Audit` substrate; readers who worked through 48f will recognize the mechanism)
- Ch15 §Collaborator Revocation → Ch15 §GDPR Article 17 and Crypto-Shredding (cached-copy obligations on the revoked party's device intersect erasure rights; deployment must address both separately)
- Ch15 §Collaborator Revocation → #18 delegated capability (the GRANT side of the collaboration this section unwinds; the two are paired — grant and revocation are symmetric operations at the policy level)
- Ch20 §Revocation UX → Ch15 §Collaborator Revocation and Post-Departure Partition (the cryptographic specification that this UX surfaces)
- Ch20 §Revocation UX → Ch20 §The Three Always-Visible Indicators (node health shifts to red on revocation; the existing indicator handles this without a new component)
- Ch20 §Revocation UX → Ch20 §Designing for Failure Modes (the quarantine-queue failure mode, already described in that section, is the mechanism that handles writes from a revoked collaborator who is reconnecting)
- Ch20 §Revocation UX → Ch15 §Key Compromise Incident Response (the dispute-halt path for revocation claims triggered by unauthorized attempts maps to the compromise response procedure)

---

## §I. Subagent Prompt for the Draft Stage

The next iteration (`outline → draft`) will invoke `@chapter-drafter` with this prompt:

> Draft two new sections for *The Inverted Stack*: (1) `## Collaborator Revocation and Post-Departure Partition` for Ch15 (~2,000 words, inserted between the existing `## Offline Node Revocation and Reconnection` section and the existing `## In-Memory Key Handling` section); and (2) `## Revocation UX` for Ch20 (~800 words, inserted between the existing `## Key-Loss Recovery UX` section and the existing `## Accessibility as a Contract` section).
>
> Source: outline at `docs/book-update-plan/working/45-collaborator-revocation/outline.md`. Follow the section structure and word targets exactly.
>
> Voice: Part III specification register for Ch15 — positive declarative statements, no hedging, no second-person address. Part IV tutorial register for Ch20 — direct second-person address on configuration and UX decisions; explicit "do not" instructions for common mistakes (do not surface KEK terminology to administrators; do not force-quit the revoked user's session; do not use a modal for the access-ended message).
>
> Active voice throughout. No hedging on revocation guarantees. No academic scaffolding. No re-introducing the architecture (Ch15 assumes Part I + earlier Ch15 sections; Ch20 assumes Part I, Ch15, and earlier Ch20 sections including §Key-Loss Recovery UX).
>
> Sub-patterns: 45a through 45f must each appear as a named subsection in Ch15 (§A.2 through §A.7 in the outline). Sub-patterns 45a, 45c, and 45f additionally surface in Ch20 (§B.1, §B.2, and §B.3 respectively); write both specification side and UX side for those three.
>
> FAILED conditions (from outline §A.1, sourced from design-decisions §5 #45) must appear explicitly in Ch15 as a named FAILED conditions block — not buried in prose. Format as a short bulleted list under a bold **FAILED conditions** label, same treatment as extension #43.
>
> The §B.4 placeholder in the Ch20 outline is a structural note for the human voice-check pass. In the draft, write one to two bridging sentences and add an HTML comment: `<!-- voice-check: add departure anecdote here -->`. Do not add the anecdote itself.
>
> Sunfish references: package names only (`Sunfish.Kernel.Security`, `Sunfish.Kernel.Audit`, `Sunfish.Foundation.Recovery`) — no class APIs, no method signatures. `Sunfish.Kernel.Audit` and `Sunfish.Foundation.Recovery` are forward-looking namespaces introduced by extensions #48 and #45 respectively; mark all references to them `// illustrative — not runnable`. `Sunfish.Kernel.Security` is in canon; no illustrative marker needed unless a specific new interface is named.
>
> Citations: IEEE numeric. Add the four sources listed in outline §G to Ch15's reference list, continuing after the existing [7]. First-appearance order in the draft determines the numbering. Ch20 cross-references Ch15 — no new citations in Ch20.
>
> Cross-references: per outline §H — the draft must wire all of them. The Ch15→Ch20 and Ch20→Ch15 cross-references are the most important pair; they make the policy/UX pairing visible. The Ch15→#18 cross-reference is the second most important; it frames revocation as the symmetric counterpart to the existing delegated-capability mechanism.
>
> Insertion mechanics: write the new H2 sections directly into the existing chapter files at the specified insertion points. Preserve existing H2 anchor structure and H1 frontmatter. Update Ch15's reference list with the four new entries. Do not modify any existing sections.

---

## §J. Quality Gate for `outline → draft`

Per loop-plan §5: outline has all section headers + bullet points (✓ §A.1 through §A.7 above; ✓ §B.1 through §B.4 above); word count target estimated (✓ 2,000 + 800 = 2,800); subagent prompt prepared (✓ §I above). Gate passes.

**Sub-pattern coverage map:**

| Sub-pattern | Designation | Section(s) |
|---|---|---|
| 45a Explicit revocation event | §A.2 (Ch15 spec) + §B.1 (Ch20 UX — administrator initiates) | Two sections |
| 45b Post-revocation key rotation | §A.3 (Ch15 spec) + §B.1 (Ch20 UX — administrator sees progress) | Two sections |
| 45c Cached-copy management | §A.4 (Ch15 spec) + §B.2 (Ch20 UX — revoked party sees) | Two sections |
| 45d Revocation propagation | §A.5 (Ch15 spec only — no direct UX surface) | One section |
| 45e Data partition for dissolution/dispute | §A.6 (Ch15 spec) + §B.3 (Ch20 UX — partition wizard) | Two sections |
| 45f Revocation-event audit trail | §A.7 (Ch15 spec) + §B.3 (Ch20 UX — access log) | Two sections |

All six sub-patterns have designated subsections. Four of the six (45a, 45b, 45c, 45e, 45f) have both a Ch15 specification side and a Ch20 UX side. Sub-pattern 45d (revocation propagation) is a protocol-layer concern with no direct user-facing UX and appears only in Ch15.

**FAILED conditions and kill triggers from design-decisions §5 #45 reflected in outline:**

- FAILED: revoked collaborator can still write to shared state → §A.2 and §A.5 (revocation event + propagation prevent this)
- FAILED: revocation doesn't propagate to other peers within reasonable time → §A.5 (propagation sub-pattern); §D technical-review focus on OCSP CRL gap analogue
- FAILED: no audit trail of revocation event → §A.7 (audit trail sub-pattern); §B.3 (access-log UX surface)

All three FAILED conditions are addressed. No kill trigger is surfaced as a separate sub-section because the revocation primitive does not carry a conformance-percentage kill trigger of the type used in #43 (performance contracts). The revocation FAILED conditions are binary: either the event propagates and the audit trail exists, or they do not. The kill trigger for this extension is a FAILED condition that recurs across 3 consecutive technical-review passes — the standard loop-plan quality-regression trigger.

---

**Estimated next-iteration duration (draft stage):** 60–90 minutes. Comparable to #48 in structural complexity. The data-partition sub-section (§A.6) is the most novel material and will require the most careful drafting; budget for it to run long before cutting. Schedule next fire 1–2 hours after this one to allow context-cache cooldown and human-review window.
