# Outline — Extension #10: Data-Class Escalation (Event-Triggered Re-classification)

**Loop-plan spec:** `docs/book-update-plan/loop-plan.md §4 — #10`
**State entry:** `docs/book-update-plan/state.yaml → 10-data-class-escalation`
**Word target:** 2,000 words total (per `state.yaml estimated-words: 2000` and `loop-plan.md §4`)
**Status:** outline stage

---

## §A — Overview and Motivation

### The problem

Data classification in most systems is a decision made at schema-definition time. A record
is labeled when it is created: a dashcam clip is "routine footage"; a patient note is
"clinical"; a field-worker log is "operational." The label persists until someone manually
changes it, if the system even permits changes at all.

That assumption fails at the worst possible moment. A dashcam clip shot during an unremarkable
delivery shift becomes evidence the moment the vehicle is involved in a collision. A patient
note accumulates a genetic test result that requalifies it as GDPR Article 9 special-category
data. An internal note is referenced in a court order and suddenly requires legal-hold
retention that the original "internal" label never anticipated.

The design-decisions.md catalog captures this explicitly for the commercial-fleet dashcam
scenario (§4.4, commercial-fleet-vehicle-telematics entry):

> "Routine dashcam is shared-private with rolling 30-day retention; on event, escalates
> to attested-with-chain-of-custody, retention extends, signing-tier upgrades for evidence
> handoff to insurer/court."

The same pattern appears across a wide range of regulated and unregulated contexts:
healthcare records that acquire PHI identifiers after initial creation; financial notes
that become SAR-obligated when a suspicious pattern is later confirmed; field-worker
observations that become incident reports. In each case, the data was not high-class when
created. It became high-class because something happened.

Flat schema-time classification cannot handle this. Nor can manual relabeling workflows
that rely on a human noticing and acting. The architecture needs a first-class mechanism
for event-triggered re-classification.

### Why this is architecturally hard

Three properties of the Inverted Stack make late-binding re-classification non-trivial:

1. **Offline copies already exist.** When a re-classification event fires, copies of the
   record may be held by devices that have been disconnected for hours or days. Those copies
   must eventually learn the new class and apply its access rules — but the sync mechanism
   cannot deliver the re-classification until the device reconnects.

2. **Audit trails are immutable.** The record's history — all operations that produced its
   current state — was created under the old classification. Re-classifying in-place without
   duplicating storage means those historical operations now belong to a higher-class record.
   The audit trail must remain intact and must remain visible to authorized roles while access
   from previously-authorized lower-class roles is cut off.

3. **Downstream references have class consequences.** If a low-class record references a
   high-class record — an ordinary meeting note that references a classified incident report —
   the reference itself creates an exposure. The architecture must handle lifted references
   without silently leaking class information.

These properties combine to make re-classification a distributed systems problem, not just a
data-management one. The mechanism must be correct under partial replication, tolerate
offline nodes, and preserve immutable history — simultaneously.

---

## §B — Sub-pattern Decomposition

### 10a — Event-triggered re-classification API (~300 words)

The re-classification event is a metadata operation, not a data operation. The record's
content does not change. What changes is the record's class label, which is stored as a
signed metadata field on the record (alongside the record's own CRDT operations). When
a triggering event occurs — an incident flag, a legal-hold directive, the attachment of
a regulated PII field — the classification service writes a new class assertion signed
by the asserting authority (operator, compliance system, or designated user role).

The key design choice: re-classification is operation-based, not state-based. It is a
new operation appended to the record's operation log, carrying a monotonically increasing
class level, the trigger event ID, the signing authority, and a timestamp. The CRDT
invariant that applies: class level is a max-register — it can only increase, never decrease.
Once a record reaches Class 3, it cannot be re-classified to Class 2, only to Class 4 or
higher. This makes the operation idempotent and convergent: multiple nodes receiving the
same re-classification event in different orders will always converge to the same (highest)
class label.

**Target word budget:** ~300 words

### 10b — Backward propagation of policy across already-replicated copies (~350 words)

The revocation-broadcast mechanism from extension #45 (Collaborator Revocation) is the
structural analogue. Where #45 broadcasts "this collaborator's KEK share is revoked,"
#10 broadcasts "this record's class level has changed, and the new class's access policy
applies retroactively."

The broadcast mechanism uses the same gossip path as the sync daemon. The re-classification
operation propagates like any other operation. The difference from a normal edit is that
the receiving node must immediately re-evaluate access permissions for the record — not
wait until the next policy evaluation cycle.

Offline-node handling: a node that was offline when the re-classification event fired will
receive the re-classification operation on reconnect, as part of its normal anti-entropy
exchange. The node's sync daemon processes it before delivering any pending reads or writes
on that record. If the reconnecting node holds a previously lower-class copy with access
granted to roles that are no longer authorized at the new class, those sessions must be
invalidated. This invalidation is not retroactive — reads already delivered are not erased —
but forward access is cut off.

**Target word budget:** ~350 words

### 10c — Audit-trail handling under class change (~200 words)

The record's operation history was written under the old classification. The architecture's
position: the operations are preserved in full. Truncating or redacting CRDT history to
hide pre-reclassification state is explicitly out of scope — it would break convergence.
Instead, access to the historical operations is governed by the record's current class.
Roles that were authorized to read the record before re-classification are not authorized
to read its history after re-classification unless they also have access under the new class.

This creates a situation where a user who held read access at Class 1 loses that access
when the record escalates to Class 3. They retain any locally-held cached copy of the
record as of the last sync before the event, but cannot pull new deltas. This is analogous
to how #45 handles cached copies for revoked collaborators (§Sub-pattern 45c). The same
cached-copy management framework applies.

The audit trail itself — the fact that the record was re-classified, at what time, by
which authority, and for what trigger — is itself a high-class record at the new
classification level. It is produced by Sunfish.Kernel.Audit and is subject to the new
class's access controls.

**Target word budget:** ~200 words

### 10d — Cross-class references (~200 words)

A low-class record that contains a reference to a high-class record acquires an implicit
class obligation. The reference does not itself reveal the high-class record's contents,
but it proves that a relationship exists. Depending on the application domain, the
existence of the reference may itself be sensitive — in a legal-hold context, revealing
that a low-class note references an incident report may disclose the existence of the
investigation.

The architecture handles this via "class lifting." When a record is re-classified, the
system evaluates all records that hold references to it (reachable via the reference index
in Sunfish.Kernel.SchemaRegistry). Records holding inbound references are flagged for
manual operator review — not automatically re-classified, because auto-lifting could
cascade uncontrollably. The operator decides whether the referencing record's class should
be elevated. This decision is itself a re-classification operation (10a) and follows the
same propagation path (10b).

**Target word budget:** ~200 words

### 10e — Schema evolution interaction (~150 words)

Data class is a dimension of the schema: a record's schema version and its class level are
both metadata fields on the record. The question for the technical reviewer to confirm: does
re-classification constitute a schema migration in the Sunfish.Kernel.SchemaRegistry sense?

The outline position: no. Re-classification changes the record's class label but does not
change the shape of its payload. No lens is required; no upcasting logic fires. The class
label field is a fixed part of the record's envelope, not a versioned schema field.
However, the class change may trigger schema enforcement: some fields permitted at Class 1
(e.g., a human-readable description without anonymization) may be prohibited at Class 3
(e.g., the same description field must now be redacted or pseudonymized before being
delivered to read operations). This enforcement is applied at read time by the access-
control layer, not by the schema migration engine.

Flag this for technical review: confirm whether the Sunfish.Kernel.SchemaRegistry
enforcement layer or the Sunfish.Kernel.Security access-control layer is the right place
for per-class field-access rules.

**Target word budget:** ~150 words

---

## §C — Target Chapter Selection and Insertion Point

### Decision: two sections, two chapters

Per `loop-plan.md §4` and `state.yaml`, the confirmed targets are:

- **Ch15 §"Event-Triggered Re-classification"** (~1,000 words) — the policy and
  mechanism layer. This is where the CRDT operation design, backward propagation, audit-
  trail handling, and cross-class reference problem are specified. Ch15 is the security
  architecture reference chapter; data-class policy belongs there because it is a security
  decision (who can see what, and when does that change).

- **Ch20 §"Data-Class Escalation UX"** (~1,000 words) — the user-facing surface.
  Ch20 is the UX chapter for sync and conflict; data-class escalation has a UX consequence
  (a user's view of a record may change without the user having edited it, and the UX must
  communicate this honestly).

### Insertion points

**Ch15:** Insert between **§GDPR Article 17 and Crypto-Shredding** and **§Relay Trust
Model**. Rationale: the GDPR crypto-shredding section closes the "erase on higher-class
basis" case; data-class escalation is the upstream cause that triggers crypto-shredding
eligibility. Placing re-classification immediately before the relay trust model is correct
because the relay trust model specifies what the relay sees — and a re-classified record's
new access constraints directly affect relay behavior.

Current Ch15 heading order at that point:
```
## GDPR (General Data Protection Regulation) Article 17 and Crypto-Shredding (line 583)
## Relay Trust Model (line 597)
## Security Properties Summary (line 617)
## References (line 632)
```
New section inserts at line ~597, pushing Relay Trust Model and subsequent sections down.

**Ch20:** Insert between **§Revocation UX** and **§Accessibility as a Contract**. Rationale:
revocation and re-classification are both "a previously-granted permission changes without
user action" patterns. Grouping them is consistent with how revocation UX was placed
(between §Key-Loss Recovery UX and §Accessibility as a Contract in the prior iteration).
The user needs to understand both in proximity to understand the full scope of access
changes that can happen without user-initiated edits.

Current Ch20 heading order at that point:
```
## Revocation UX (line 318)
## Accessibility as a Contract (line 354)
```
New section inserts between lines 353 and 354.

---

## §D — Sunfish Package Decisions

### Recommended: extend Sunfish.Kernel.Security; do not introduce a new top-level package

**Rationale:**

Re-classification is a security decision — it changes who can access a record. The policy
enforcement, the access-control re-evaluation, and the KEK re-wrapping (if the new class
uses a different key envelope) all belong to Sunfish.Kernel.Security. This is consistent
with how #45 (collaborator revocation) was handled: no new namespace, extensions to
Sunfish.Kernel.Security.

The one function that extends beyond Sunfish.Kernel.Security is the reference-index lookup
for cross-class reference detection (sub-pattern 10d). That lookup queries the reference
index maintained by Sunfish.Kernel.SchemaRegistry. The call goes from
Sunfish.Kernel.Security → Sunfish.Kernel.SchemaRegistry (cross-package call in the same
tier), which is consistent with the existing dependency graph.

**Against Sunfish.Kernel.DataClass (new package):** A dedicated data-class package would
make sense if data-class policy was the primary orchestration surface. But the primary
orchestration is access control (Security) and the primary metadata is stored in the CRDT
envelope (Kernel.Crdt). A new package for a metadata field and one propagation operation
is over-segmentation at this scale.

**Package references to use in prose:**
- `Sunfish.Kernel.Security` — re-classification assertion, KEK re-wrapping on class change
- `Sunfish.Kernel.Audit` — re-classification event record (forward-looking, per #48 precedent)
- `Sunfish.Kernel.SchemaRegistry` — reference-index lookup for cross-class reference detection
- `Sunfish.Kernel.Sync` — propagation of the re-classification operation via gossip

All four packages are either in canon or marked as forward-looking in prior extensions.
No new package introduction required.

---

## §E — Citations Needed

The draft should include IEEE citations for the following. The technical-review stage will
verify URLs and publication metadata.

| Citation | Source | Relevance |
|---|---|---|
| NIST SP 800-60 Vol. 1 Rev. 1 | [https://csrc.nist.gov/pubs/sp/800/60/v1/r1/final](https://csrc.nist.gov/pubs/sp/800/60/v1/r1/final) | Data classification framework; high-watermark principle; re-classification triggers |
| NIST SP 800-60 Rev. 2 (IWD) | [https://csrc.nist.gov/pubs/sp/800/60/r2/iwd](https://csrc.nist.gov/pubs/sp/800/60/r2/iwd) | Updated classification guidance including re-classification review triggers |
| ISO/IEC 27001:2022 Annex A 5.12 | [https://www.isms.online/iso-27001/annex-a-2022/5-12-classification-of-information-2022/](https://www.isms.online/iso-27001/annex-a-2022/5-12-classification-of-information-2022/) | Classification of Information control; explicit requirement to review and update classification when value or sensitivity changes |
| GDPR Article 9 | [https://gdpr-info.eu/art-9-gdpr/](https://gdpr-info.eu/art-9-gdpr/) | Special-category data prohibition; inference-based classification trigger ("processing intends to make an inference linked to a special category...regardless of confidence level") |
| HIPAA PHI classification | Accountable HQ / Forcepoint policy references | Three-tier PHI classification; continuous monitoring requirement; re-classification on new identifier accumulation |

**Note on source-paper status:** The primary architecture paper (v13) and companion paper
(v5) are unavailable in this environment (gitignored). The design-decisions.md entry
(§4.4, commercial-fleet-vehicle-telematics) confirms the escalation pattern is part of
the architecture's acknowledged scope. Technical-review stage must locate the v13/v5 section
numbers that discuss data classification labels and confirm whether the max-register CRDT
invariant for class level is specified in the papers or is an extension introduced here.

---

## §F — FAILED Conditions and Kill Trigger

**FAILED conditions for this extension:**

- **FAILED:** Any implementation path that requires duplicating the record to achieve
  class separation — copying old-class record to an archive store and creating a new
  high-class record. In-place re-classification without storage duplication is the
  defining constraint.

- **FAILED:** Any re-classification mechanism that breaks CRDT convergence — for example,
  treating re-classification as a state mutation rather than an operation append, causing
  nodes that apply operations in different orders to disagree on the record's class label.

- **FAILED:** Any mechanism that silently strips access from an offline node's locally-held
  copy without informing the user on reconnect. The UX section must surface the access
  change explicitly.

- **FAILED:** Any mechanism that allows class-level to decrease — re-classification is
  irreversible (max-register). If the extension draft contradicts this in any sub-pattern,
  that is a kill-trigger-level error.

- **FAILED:** Any cross-class reference handling that auto-escalates referencing records
  without operator review, risking unbounded cascade.

**Kill trigger:** Set `kill-triggers.quality-regression = true` if the technical-review
stage identifies that in-place re-classification with audit-trail preservation requires
a fundamentally different CRDT mechanism than the operation-append approach described in
sub-pattern 10a. In that case, the section cannot be drafted without a confirmed design,
and the loop should pause for author decision.

---

## §G — Open Technical-Review Items

1. **Max-register CRDT invariant for class labels** — is this specified in v13/v5, or is
   it an extension? If it is an extension, the prose must acknowledge it as such.

2. **Offline-node invalidation on reconnect** — the mechanism described in 10b (invalidate
   forward access, not retroactive reads) needs v13/v5 sourcing or explicit acknowledgment
   as a new design decision.

3. **Schema enforcement at Class N** — 10e proposes that per-class field-access rules are
   enforced at read time by Sunfish.Kernel.Security, not by Sunfish.Kernel.SchemaRegistry.
   Technical reviewer should confirm this is the correct ownership boundary.

4. **Cross-class reference detection** — 10d proposes a reference index in
   Sunfish.Kernel.SchemaRegistry. Confirm whether this index exists or is forward-looking.

5. **Interaction with #17 crypto-shredding** — the cross-reference in §H points to GDPR
   Article 17 and Crypto-Shredding. Confirm that re-classification at Class N can serve as
   the trigger for a subsequent crypto-shredding event (i.e., if a record is re-classified
   into a higher class and later subject to a deletion request, the deletion uses the
   higher-class KEK for shredding). This is a chain: 10a → GDPR Art. 17 § crypto-shredding.

6. **Interaction with #46 forward secrecy** — re-classification may require re-encryption
   under the new class's KEK. If the old-class KEK was ephemeral (forward-secrecy ratchet),
   the new class must create a new KEK from the current ratchet state, not from the old
   KEK. Technical reviewer should confirm this composes without a re-encryption of the
   full record content (envelope-only re-keying should suffice).

---

## §H — Cross-Reference Plan

### Forward references

- **§GDPR Article 17 and Crypto-Shredding** (Ch15, existing section immediately before
  the new insertion point): re-classified records that accumulate data subject to right-
  to-erasure may require crypto-shredding at the higher class's KEK. The re-classification
  section should close with a forward pointer: "When an escalated record is later subject
  to a deletion request, §GDPR Article 17 and Crypto-Shredding applies at the new class
  level."

### Backward references

- **§Collaborator Revocation and Post-Departure Partition** (Ch15 §45a–45f): the
  revocation-broadcast mechanism is the structural analogue for backward propagation (10b).
  The new section should reference it: "The propagation mechanism is identical in structure
  to the revocation broadcast defined in §Collaborator Revocation."

- **§Schema Migration and Evolution** (Ch13): re-classification is not a schema migration
  in the Sunfish.Kernel.SchemaRegistry sense (10e), but readers coming from Ch13 may
  expect a connection. Ch13 does not need a new cross-reference, but the 10e sub-section
  should explicitly explain the non-overlap.

- **§AP/CP Visibility by Data Class** (Ch20, existing section at line 52): Ch20 already
  introduces the concept of data classes in the context of staleness thresholds and UX
  treatment. The new §Data-Class Escalation UX section should back-reference this table
  explicitly: "The data classes in the §AP/CP Visibility table are static assignments at
  deployment time. Re-classification changes which row of that table a record belongs to."

### Ch20 specific cross-reference

- **§Revocation UX** (Ch20, immediately before the new insertion point): both sections
  address "a permission changed without user action." The new section's opening paragraph
  should acknowledge the parallel and distinguish the trigger: revocation is about removing
  a collaborator, re-classification is about changing what the record is.

---

## §I — Word Budgets Per Sub-Section

**Total target: 2,000 words across Ch15 and Ch20.**

### Ch15 §"Event-Triggered Re-classification" (~1,000 words)

| Sub-section | H-level | Budget |
|---|---|---|
| Opening — the dashcam scenario (concrete) | H3 | ~150 words |
| Sub-pattern 10a — re-classification API and CRDT invariant | H3 | ~300 words |
| Sub-pattern 10b — backward propagation to offline nodes | H3 | ~250 words |
| Sub-pattern 10c — audit-trail handling under class change | H3 | ~150 words |
| Sub-pattern 10d — cross-class references | H3 | ~100 words |
| Sub-pattern 10e — schema evolution non-interaction | H3 | ~50 words |
| FAILED conditions | H3 | ~50 words |
| **Ch15 total** | | **~1,050 words** |

### Ch20 §"Data-Class Escalation UX" (~1,000 words)

| Sub-section | H-level | Budget |
|---|---|---|
| Opening — what the user sees when a record changes class | H3 | ~150 words |
| The visibility change: record-level indicator of class | H3 | ~200 words |
| The offline case: reconnect and discover changed access | H3 | ~250 words |
| Operator-triggered escalation flow (operator side) | H3 | ~200 words |
| The cross-class reference prompt (operator review flow) | H3 | ~150 words |
| **Ch20 total** | | **~950 words** |

**Combined: ~2,000 words.** Within the ±20% acceptable band at 1,600–2,400 words.

---

## §J — Notes on Novelty

In-place re-classification with audit-trail preservation has no direct prior-art analogue
in published local-first or distributed-systems literature known to this outline.

**What exists:**

- NIST SP 800-60 defines re-classification as a management decision requiring human review
  (not a protocol-level operation), with no mechanism specified for distributed systems.
- ISO/IEC 27001:2022 Annex A 5.12 requires periodic review and update of classification
  but does not specify a distributed convergence mechanism.
- Microsoft Purview / Azure Information Protection automate label assignment at scan time
  but treat re-classification as a centralized, online operation that cannot be applied to
  offline copies.
- AWS Macie and Google Cloud DLP operate similarly — centralized, online scan-and-label.
- CRDT literature addresses operation commutativity but does not address security metadata
  as a CRDT register with access-control side effects.

**What this section contributes:**

The max-register invariant applied to a security metadata field (class label) propagated
via the existing CRDT operation log, with access-control re-evaluation on delivery, is the
specific novelty. The claim is that re-classification can be made convergent and correct
under partial replication without duplicating storage or breaking immutable audit trails.

**Flag for technical review:** The max-register approach is presented here as the design
decision. If the technical reviewer finds a prior system that implements the same mechanism,
cite it. If not, the prose should acknowledge the gap explicitly: "No prior system known
to the authors handles this combination; the mechanism is proposed here as a necessary
extension of the architecture."

---

## §K — Chapter-Drafter Subagent Prompt (for draft stage)

Draft two new sections for insertion into the book:

**Section 1:** Ch15 §"Event-Triggered Re-classification" (~1,000 words)
Insert between Ch15 §GDPR Article 17 and Crypto-Shredding and §Relay Trust Model.
Voice: Part III specification. No second-person. Lead with the concrete dashcam scenario.
Cover sub-patterns 10a–10e and FAILED conditions per the outline.
Package references: Sunfish.Kernel.Security, Sunfish.Kernel.Audit, Sunfish.Kernel.SchemaRegistry,
Sunfish.Kernel.Sync — all by name only, no class APIs.
Citations: NIST SP 800-60 Rev. 1 [N], ISO/IEC 27001:2022 Annex A 5.12 [N], GDPR Article 9 [N].
Cross-references: §GDPR Article 17 (forward), §Collaborator Revocation (backward).

**Section 2:** Ch20 §"Data-Class Escalation UX" (~1,000 words)
Insert between Ch20 §Revocation UX and §Accessibility as a Contract.
Voice: Part IV tutorial. Direct second-person on wiring. Target-experience-first.
Cover: record-level class indicator, the offline reconnect experience, operator
escalation flow, cross-class reference review prompt.
Back-reference: Ch20 §AP/CP Visibility by Data Class table.
Cross-reference: Ch15 §Event-Triggered Re-classification (backward to policy layer).

Both sections: no academic scaffolding, no there-is constructions, active voice,
no paragraph >6 sentences, no CLAIM markers unless architectural claim cannot be
verified against v13/v5 (in which case insert <!-- CLAIM: source? --> inline).
Add IEEE citation placeholders as [N] for all citations; number sequentially from
the current highest IEEE reference number in Ch15 (currently [27] at Ch15 line 632+).
Add FAILED conditions block in Ch15 section as bold-labeled bulleted list.
HTML code-check annotation at the start of each new section disclosing which
Sunfish packages are referenced and their canon status.
