# 44 — Per-Data-Class Device-Distribution Policy — Outline

**ICM stage:** outline → ready for draft.
**Target chapter:** Ch16 — Persistence Beyond the Node (Part III, reference specification voice).
**Total word target:** 1,500 words.
**Source:** `docs/book-update-plan/loop-plan.md` §4 entry #44; `docs/book-update-plan/state.yaml` entry `44-per-data-class-device-distribution`; Ch16 existing §Declarative Sync Buckets and §Lazy Fetch and Storage Budgets; Ch14 §Capability Negotiation and §Subscription Enforcement; design-decisions §5 sub-patterns 44a–44e.
**Why tenth in priority list:** Smallest scope in the set. The problem is real but the mechanism (subscription manifest + push filter) is the most analogous to the existing bucket model. Bulk of the novelty is in 44c (broken-reference handling) and 44e (eviction-on-escalation, composed with extension #10).

---

## §A. New section in Ch16 — "Per-Data-Class Device-Distribution"

### Overview and motivation

Device fleets in real deployments are heterogeneous by design. A restaurant's floor tablet handled by servers holds customer orders and table assignments. The same restaurant's back-office laptop held by the owner holds payroll, vendor invoices, and cost-of-goods data. Uniform replication — every device holds every data class — fails this fleet in two ways simultaneously: the floor tablet holds payroll records that a server has no operational need for, and the storage budget on a constrained Android tablet is consumed by data classes it will never display.

The first failure is a security surface problem. A restaurant server whose tablet is left on a table for thirty seconds cannot execute a payroll lookup — the application access controls prevent it. But if the payroll records are present in the local encrypted database, the risk surface is a decryption key exposure, a debugger attach, or a future application bug, not a network request to a remote server. A record that is not on a device cannot be leaked from that device.

The second failure is a storage budget problem. The bucket model in §Declarative Sync Buckets already handles subscription filtering at the bucket granularity — a device with only `team_member` attestation receives `team_core` and not `financial_records`. That bucket-level filtering is role-driven: what attestations the device's user holds. Per-data-class device-distribution adds a second, independent axis: not just what the user is authorized to see, but what classes this physical device's operational role requires it to hold at all. The distinction matters in MDM-managed fleets where the device class is set by IT policy independently of the user's role.

**Insertion point:** Between the existing `## Lazy Fetch and Storage Budgets` section and the existing `## Snapshot Format and Rehydration` section. Narrative logic: Lazy Fetch and Storage Budgets establishes the eviction and stub model. Per-data-class device-distribution extends that model with a policy-driven subscription layer above it. Snapshot Format and Rehydration begins the correctness-and-recovery narrative, which depends on knowing which classes a device holds. Inserting here groups the "what does this device hold and why" concerns together before the "how do we preserve and recover it" concerns begin.

**H2:** `## Per-Data-Class Device-Distribution`

---

## §B. Sub-pattern decomposition

### 44a — Per-device data-class subscription manifest (≈300 words)

Each device carries a signed manifest that declares the data classes it accepts. The manifest is distinct from role attestations: role attestations are user-bound claims issued by the identity authority that authorize access to specific buckets; the class-subscription manifest is device-bound policy set by the MDM operator (or the user in consumer deployments) that declares which classes the device's operational role requires. A device can hold a `financial_role` attestation and still be configured by the MDM administrator to exclude detailed customer-record classes from the device — the manifest is a restriction layer over the attestation-granted set, not an expansion of it.

The manifest is a signed CBOR document. Signature is under the device's own Ed25519 keypair, making it tamper-evident and attributable. The manifest travels with the device identity during the CAPABILITY_NEG handshake (Ch14 §Capability Negotiation). The sync daemon on the sending peer reads the receiving device's manifest before constructing any outbound delta, and drops operations that touch record classes the manifest excludes.

**Bullet-point coverage:**
- Manifest structure: device_id, issuer (MDM authority or self-signed for consumer), class_subscriptions[] (list of accepted data-class identifiers), issued_at, expires_at, signature.
- Data classes as a higher-level abstraction over buckets: a data class maps to one or more bucket entries from the §Declarative Sync Buckets YAML. The manifest operates at the class level; the sync daemon resolves class → bucket membership internally.
- Consumer deployments: user sets class subscriptions via application preferences; manifest is self-signed; no MDM authority required. This preserves the architecture's non-MDM-dependent operation for individuals and small teams.
- The manifest is append-only in the audit log; every change produces a new signed version, preserving history for compliance purposes.

### 44b — Sync-daemon push filter (≈250 words)

The sync daemon on the sending node applies the receiver's manifest as a push filter before constructing outbound deltas. The filter is applied at the stream level, before any bytes leave the node.

**Bullet-point coverage:**
- Filter position: applied at the same tier as the subscription-scope filter in Ch14 §Subscription Enforcement — after attestation verification and before delta construction. The two filters compose: attestation filter removes streams for which the receiver lacks role authorization; class-subscription filter removes record-class operations within otherwise-authorized streams.
- A record that belongs to a class the receiving device has excluded is dropped silently at the send tier. The receiving node's daemon never sees the operation. No error is emitted. This mirrors the existing behavior for field-level out-of-scope operations described in Ch14 §Subscription Enforcement.
- The filter operates on the data-class label attached to each record at write time. Data classes are declared in the document schema and are immutable once assigned (mutability is extension #10's domain). A record without a class label is treated as belonging to the default class, which all devices accept.
- Performance note: the filter evaluation is O(1) per operation — a hash-set membership check against the receiving device's accepted classes. No per-record network round-trip. No relay involvement.

### 44c — Cross-class reference handling: the placeholder pattern (≈350 words)

This sub-pattern is the most technically novel element of the extension and warrants the largest word budget.

When a record in class A holds a reference to a record in class B, and the receiving device subscribes to class A but not class B, the A-record arrives on the device with a reference that cannot be resolved locally. Three options exist: refuse to deliver the A-record, deliver it with a broken reference that silently returns null, or deliver it with an explicit placeholder that signals "this reference points to a class you do not hold."

The architecture chooses the third option. The placeholder pattern follows the stub model established in §Lazy Fetch and Storage Budgets, with one critical difference: a lazy-evicted stub is fetchable on demand. A class-excluded placeholder is not fetchable — the device's manifest excludes the referenced class, and the sync daemon will not retrieve it regardless of demand. The placeholder must convey that distinction to the application.

**Bullet-point coverage:**
- Placeholder structure: record_id, class_label (of the referenced record), exclusion_reason (`class_not_subscribed`), content absent. The application renders the placeholder as a "restricted reference" indicator — not a missing-data error, not a broken link, but a policy-gated boundary the user can see and understand.
- Prior-art analogues: OneDrive Files On-Demand (cloud-only placeholder, fetchable on demand) and iCloud Optimize Mac Storage (eviction stub, fetch-on-demand via materialisation) both use the stub-as-presence-indicator pattern — the user sees the file exists without holding its content. The distinction in the local-first architecture is that the fetch is policy-blocked, not just deferred. The placeholder signals finality, not latency.
- Application responsibility: the application layer is responsible for rendering the placeholder in a way that does not silently mislead the user. A task record that references a payroll record (class: financial) on a device that excludes financial records must not render the payroll reference as "no data found." It renders as "restricted — not available on this device." This is an explicit application-layer contract, not an architectural invariant the sync daemon enforces.
- Reference integrity guarantee: the architecture does not guarantee that all cross-class references are resolvable on all devices. It guarantees that unresolvable references are detectable and labeled. A device that holds class A fully can verify all class-A-internal references. References to excluded classes are explicitly marked. This is the honest version of partial-replica reference integrity, consistent with the architecture's commitment to honest failure modes rather than silent degradation.

### 44d — MDM/policy-driven manifest update and propagation (≈200 words)

The class-subscription manifest can be updated by the MDM authority at any time. An IT administrator who decides that tablet-class devices should stop receiving order-history records (class: `order_history`) can push a manifest update that removes that class from those devices' subscriptions.

**Bullet-point coverage:**
- Manifest update delivery: the MDM authority signs a new manifest version and delivers it through the same OTA update channel used for node configuration (Ch21 §OTA Update Coordination for the fleet management context). The device's sync daemon loads the new manifest and applies it on the next capability negotiation cycle.
- Eviction on manifest tightening: when a device's manifest removes a class it previously held, the sync daemon evicts all records of that class from the local database. Eviction follows the same stub conversion used in §Lazy Fetch and Storage Budgets: identifiers and metadata are retained as class-excluded placeholders; content is purged. The eviction is logged to the audit record with the manifest version that triggered it.
- Expansion does not trigger backfill automatically: when a manifest adds a new class, the sync daemon requests the new class's records during the next capability negotiation. Backfill is eager for classes marked `replication: eager` in the bucket definition; lazy for `replication: lazy` classes.
- Cross-reference to Ch21 §Fleet Management for the administrative workflow that governs manifest update authorization, approval, and rollout.

### 44e — Audit and observability: what does this device actually hold? (≈200 words)

An administrator who cannot verify what a device holds cannot reason about the fleet's data exposure surface. The audit layer closes this gap.

**Bullet-point coverage:**
- Per-device class inventory: each device maintains a signed class-inventory record listing the classes it currently holds, the count of full records and stubs per class, and the manifest version under which each class was acquired or evicted. The inventory is updated on every sync session and on every manifest change.
- Fleet-level visibility: `Sunfish.Foundation.Fleet` (introduced by extension #11) aggregates per-device class inventories into a fleet-level view. An administrator sees, per device: subscribed classes, actual held counts, last-manifest version, and last-sync timestamp.
- Discrepancy detection: if a device's actual held classes diverge from its current manifest (possible during an offline manifest update that has not yet triggered eviction), the fleet dashboard flags the discrepancy. The device resolves it at next sync.
- Audit log entries: every manifest change, every eviction, and every class backfill produces a signed entry in `Sunfish.Kernel.Audit`. The entries are attributable (which authority issued the manifest that triggered the change), timestamped, and append-only.

---

## §C. Target chapter selection and insertion point

**Target chapter: Ch16 — Persistence Beyond the Node.** Rationale:

1. The extension is a persistence and storage-boundary concern. It governs which records persist to which devices. Ch16 already owns the bucket model, the storage budget, and the lazy-fetch mechanism that this extension extends.
2. The existing Ch16 §Declarative Sync Buckets already establishes bucket-level role filtering. Per-data-class device-distribution is the natural second tier of that filtering — one level higher in abstraction (class over bucket), one axis orthogonal to role (device policy vs. user attestation).
3. Ch14 (Sync Daemon Protocol) owns the push filter mechanism. The push filter for class subscriptions is analogous to the existing Ch14 §Subscription Enforcement field-level filter. The outline treats the class-subscription filter as a Ch14-backed mechanism and cross-references Ch14 rather than re-specifying the filter mechanics in Ch16. This respects the chapter boundary: Ch16 specifies what policy the device declares; Ch14 specifies how the daemon enforces it.

**Why not Ch15 (Security Architecture)?** The primary motivation is storage efficiency and operational correctness, not a security primitive. The security benefit (reduced risk surface) is a consequence of the policy, not its mechanism. The existing Ch15 §Data Minimization already covers the principle. This section specifies the mechanism that implements it for device fleets.

**Why not Ch14 (Sync Daemon Protocol)?** The push filter addition would fit mechanically in Ch14, but the subscription manifest is declared and managed at the persistence layer (Ch16), not the protocol layer (Ch14). Ch14 consumes the manifest; Ch16 defines it. Placing the section in Ch16 keeps the manifest's definition and its operational context (storage budgets, eviction, audit) co-located.

**Insertion point:** Between `## Lazy Fetch and Storage Budgets` and `## Snapshot Format and Rehydration`.

---

## §D. Sunfish package decisions

**No new top-level namespace.** The extension extends three packages already in use:

- `Sunfish.Kernel.Buckets` — already owns the bucket model, storage budget, and eviction policy. Extend to include class-subscription manifest storage and class → bucket resolution. This is the natural home for the manifest because the manifest is an input to the bucket subscription computation.
- `Sunfish.Kernel.Sync` — already owns the push filter and subscription enforcement (Ch14). Extend the outbound delta construction to apply the class-subscription filter after the attestation filter. The filter is a read-only operation against the receiving device's manifest; no new data model required.
- `Sunfish.Kernel.Audit` — already forward-looking from extensions #48 and #45. The manifest-change, eviction, and backfill events follow the same signed-event substrate as the existing audit entries.
- `Sunfish.Foundation.Fleet` — introduced by extension #11. The per-device class-inventory aggregation belongs here, as it is a fleet-level concern that consumes per-device kernel audit data.

**Forward-looking note for code-check stage:** `Sunfish.Kernel.Buckets` is referenced in the existing Ch16 text as an in-canon package (line 128: "configurable via `Sunfish.Kernel.Buckets`"). Confirm at code-check that extending it for class-subscription manifest storage is architecturally appropriate, or whether a sub-namespace `Sunfish.Kernel.Buckets.Subscription` is warranted. Mark illustrative in the draft section header comment; resolve at code-check.

---

## §E. Citations needed

**Selective-sync prior art:**

- [A] Dropbox Selective Sync — Dropbox Help (help.dropbox.com/sync/selective-sync-conflict). Cross-class reference analogue: when a file is excluded by selective sync and another synced file contains a path reference to it, Dropbox does not resolve the reference — the path simply points to a missing local file. The "selective sync conflict" folder pattern is the closest consumer-facing equivalent to the placeholder pattern, though Dropbox creates a folder stub rather than a typed placeholder record. Use for: §44c prior-art analogy with explicit note on where the architecture improves on it (typed exclusion reason vs. silent missing-file).

- [B] Microsoft OneDrive Files On-Demand. "Files On-Demand is the long-awaited replacement for Windows 8.1-era OneDrive placeholders... Instead of downloading every file, the OS creates lightweight reparse points that act as pointers to the cloud." (Petri IT Knowledgebase / Windows Central, referenced in web search results above.) Use for: §44c analogue — the placeholder-as-presence-indicator pattern. The key distinction to note: OneDrive placeholders are fetchable on demand; the architecture's class-excluded placeholders are policy-blocked.

- [C] Apple iCloud Optimize Mac Storage / materialisation. "macOS replaces local files with stubs and fetches on-demand... the process now known as materialisation." (Apple Support, search results above.) Use for: §44c second prior-art analogue — deferred fetch triggered on access. Same distinction applies: iCloud materialises on demand; the architecture distinguishes deferred-fetch stubs (lazy records) from policy-excluded placeholders.

- [D] ElectricSQL Shape Filtering (v0.10, 2024). "A Shape is the fundamental unit of synchronization in ElectricSQL representing a subset of a PostgreSQL table... shape filtering... will only sync the specified data." (electric-sql.com/blog/2024/04/10/electricsql-v0.10-released.) Use for: §44b push-filter prior art — ElectricSQL's shape-filtering is the closest production analogue to a per-device class-subscription filter in a local-first sync system. Distinction: ElectricSQL operates on row-level query predicates (SQL WHERE clauses); the architecture operates on data-class labels attached at the schema level.

- [E] PowerSync Sync Rules / bucket definitions (powersync.com). "PowerSync provides full bidirectional sync... Sync Rules consist of bucket definitions that define individual buckets... which clients then sync based on their parameters." Use for: §44a manifest-as-bucket-selector analogue. PowerSync's bucket definitions are server-side rules evaluated per client parameter; the architecture's class-subscription manifest is client-side policy that the server (sync daemon on the sending peer) applies. This positions the architecture's design as client-driven rather than server-driven — a key local-first property distinction.

**Academic / industry references on partial replication and class-aware distribution:**

- [F] Terry, D.B., et al. (1995). "Managing Update Conflicts in Bayou, a Weakly Connected Replicated Storage System." SOSP 1995. The Bayou system introduced per-device subscriptions to named data sets ("write streams") with explicit subscription management, which is the earliest well-cited precedent for device-level partial replication. The class-subscription manifest in this extension is structurally analogous to a Bayou subscription declaration. Verify URL at technical-review stage (ACM DL).

- [G] Kleppmann, M., et al. (2019). "Local-First Software: You Own Your Data, in Spite of the Cloud." Proceedings of the ACM ONWARD! 2019. Property 2 (real-time collaboration), Property 4 (offline), and Property 7 (user ownership) collectively establish the motivation for intentional locality. The data-class device-distribution policy is the architecture's mechanism for making Property 7 precise at the device level.

**Note to technical reviewer:** The class-subscription manifest pattern has no single canonical citation. It is closest to Bayou's subscription model [F] at the academic level and to ElectricSQL/PowerSync at the industry level. If a more precise citation for "device-declared data-class subscription in a local-first system" surfaces during technical review, insert it. Otherwise, cite [D] and [F] and note the gap explicitly.

---

## §F. FAILED conditions and kill trigger

**FAILED conditions — the section has failed if any of the following are true after draft:**

- **F-1 Manifest conflated with attestation.** The draft uses "manifest" and "attestation" interchangeably or fails to make explicit that the manifest is device-bound operator policy and the attestation is user-bound identity claim. The two are orthogonal axes; conflating them breaks the security model.
- **F-2 Push filter placed in wrong chapter.** The draft describes the push filter mechanics in full in Ch16, duplicating Ch14 §Subscription Enforcement. Ch16 should declare the policy (the manifest); Ch14 should be cross-referenced for the enforcement mechanism.
- **F-3 Placeholder-as-error.** The draft presents the class-excluded placeholder as an error state or as equivalent to a missing record. The placeholder is a policy boundary, not a data integrity failure. The distinction must be explicit.
- **F-4 Manifest expansion triggers automatic backfill without qualification.** The draft says "when the manifest adds a class, backfill begins" without specifying that eager-bucket backfill is immediate and lazy-bucket backfill is demand-driven. The §Declarative Sync Buckets distinction applies.
- **F-5 New top-level namespace invented.** The draft introduces a package outside `Sunfish.Kernel.Buckets`, `Sunfish.Kernel.Sync`, `Sunfish.Kernel.Audit`, and `Sunfish.Foundation.Fleet` for the manifest model. No new top-level namespace is warranted; extend existing packages.

**Kill trigger:** If technical-review determines that the class-subscription manifest conflicts with the existing bucket model in a way that requires redesigning the bucket YAML schema (rather than extending it), escalate to the author before continuing. The existing `required_attestation` field in the bucket definition is user-role-driven; the class-subscription manifest is device-policy-driven. If these cannot coexist in the existing schema, the extension scope changes.

---

## §G. Open technical-review items

1. **Manifest and bucket resolution:** confirm that the class → bucket resolution (a class maps to one or more buckets) is computable from the existing bucket YAML without requiring a new top-level schema element. Candidate: add an optional `data_class` field to each bucket entry. Classes are then resolved as the union of bucket entries that share the same `data_class` label. Verify this does not require a breaking change to the bucket YAML.

2. **Manifest at CAPABILITY_NEG:** confirm that the CAPABILITY_NEG message in Ch14 already has a payload slot for extended device metadata, or identify the correct extension point. The outline assumes the manifest travels with the handshake; verify against Ch14's CAPABILITY_NEG message structure (the existing `mdm_compliance` attestation slot is the likely candidate — the class-subscription manifest is an MDM-issued document when MDM is in use).

3. **Eviction vs. deletion on manifest tightening:** confirm that eviction-to-stub (identifier + metadata retained, content purged) is the correct behavior when a class is removed from the manifest, rather than full record deletion. The stub model preserves navigability; full deletion would break existing lazy-fetch cross-references within the application. The outline assumes eviction; verify this is consistent with the existing eviction behavior in `Sunfish.Kernel.Buckets`.

4. **Composition with extension #46 (forward secrecy):** a device that has never held class C does not hold the class-C key material. If forward secrecy is implemented per-class (class-C operations encrypted under a class-C ephemeral key chain), a device added to a class-C subscription mid-stream cannot decrypt historical class-C operations. The draft should note this boundary and cross-reference #46 §Forward Secrecy for the key-rotation handshake that delivers current-state class-C key material to a newly subscribing device. Technical reviewer to confirm whether the #46 forward-secrecy mechanism already handles this or whether an extension is needed.

5. **Reference to design-decisions §5 sub-patterns:** the source papers (`source/local_node_saas_v13.md`) are inaccessible on this machine (gitignored). The sub-pattern decomposition in this outline is derived from the design-decisions framing in `loop-plan.md` §4 entry #44. Technical reviewer to verify sub-patterns 44a–44e against the primary source paper once accessible.

---

## §H. Cross-reference plan

**Forward references:**

- Forward to **Ch21 §Fleet Management** (#11): the per-device class-subscription manifest is a fleet-admin artifact when MDM is in use. The manifest update workflow (44d) depends on the OTA update channel and manifest-distribution infrastructure specified in Ch21.
- Forward to **Ch19 §Shipping to Enterprise**: enterprise procurement discussions about data residency and device-class policy belong in Ch19; Ch16 §44 is the mechanism, not the sales argument. A one-sentence forward reference connecting the mechanism to the enterprise discussion is sufficient.

**Backward references:**

- Backward to **Ch16 §Declarative Sync Buckets** (same chapter, preceding section): the class-subscription manifest is a second-order filter over the bucket model. The section must open by establishing the relationship to the bucket layer, not re-explaining buckets.
- Backward to **Ch15 §Collaborator Revocation** (#45): when a collaborator is revoked, their device's manifest is effectively replaced with an empty subscription. The revocation event and the manifest update are two distinct events in the audit log, but they are causally linked. The cross-reference here is from Ch16 §44d (manifest update propagation) pointing back to Ch15 §45 for the revocation primitive.
- Backward to **Ch15 §Data Minimization** (existing section): the class-subscription manifest is the device-fleet instantiation of the data minimization principle already established in Ch15. A single sentence acknowledging the relationship keeps the two from appearing to contradict each other.
- Backward to **Ch14 §Subscription Enforcement**: the push filter in §44b is applied by the sync daemon using the mechanism Ch14 already specifies. The Ch16 section declares policy; Ch14 enforces it. The cross-reference must make this delegation explicit.

**Composition with extension #10 (§J below):** the cross-reference from §44 to #10 is forward (the escalation event that triggers class-change is specified in Ch20 §Data-Class Escalation UX and Ch15 §Event-Triggered Re-Classification). The present outline specifies the eviction protocol that those future sections depend on. Mark the cross-reference as `<!-- forward: #10 §eviction protocol — resolve when #10 is drafted -->` in the draft.

---

## §I. Estimated word budgets per sub-section

| Sub-section | H3 heading | Target words |
|---|---|---|
| §A (Overview and motivation) | `## Per-Data-Class Device-Distribution` + opening paragraphs | 200 |
| 44a | Per-device data-class subscription manifest | 300 |
| 44b | Sync-daemon push filter | 250 |
| 44c | Cross-class reference handling: the placeholder pattern | 350 |
| 44d | MDM/policy-driven manifest update and propagation | 200 |
| 44e | Audit and observability | 200 |
| **Total** | | **1,500** |

The distribution weights §44c (broken-reference handling) as the largest single sub-section because it is the most technically novel element and the one most likely to generate reader confusion. §44a and §44d are bounded because they extend existing constructs (the bucket model, the OTA update channel) with minimal new mechanism. §44e is bounded because the audit substrate is already specified by extensions #48 and #45; this section reuses it rather than re-specifying it.

---

## §J. Composition with extension #10 (data-class escalation): the eviction protocol

Extension #10 (data-class escalation) addresses a record whose class changes at runtime — a dashcam video promoted from `routine` to `incident` when a safety event is detected. Extension #44 addresses which devices hold which classes.

The composition scenario: a record currently residing on Device D (which subscribes to class A) is escalated by extension #10 to class B. Device D's manifest does not include class B. The record must be evicted from Device D.

**Eviction protocol sketch (to be expanded in the #10 draft):**

1. The escalation event (specified by #10) writes a class-change record to the CRDT document: `{record_id, old_class: A, new_class: B, escalation_trigger: <event_id>, signed_by: <authority>}`.
2. The class-change record propagates to all peers via the normal sync mechanism.
3. When Device D's sync daemon receives the class-change record for a record it holds, it evaluates the new class against the device's current manifest.
4. If class B is not in the manifest, the daemon schedules eviction: convert the full record to a class-excluded placeholder, log the eviction to `Sunfish.Kernel.Audit` with the class-change event as the causal reference, and drop the record from any outbound deltas for Device D going forward.
5. The eviction is irreversible unless the manifest is updated to include class B (§44d). There is no "undo escalation" path.

**Boundary note for the #10 draft:** the eviction mechanics described here (steps 3–5) are triggered by the #10 escalation event but executed by the #44 manifest-evaluation logic. The #10 draft should cross-reference #44 for the eviction protocol rather than re-specifying it. The two extensions compose at the interface: #10 produces the class-change event; #44 reacts to it.

**Security implication:** eviction-on-escalation closes the gap where a record's class changes after it has already been distributed to a device that should not hold the new class. Without this composition, extension #10 alone would guarantee that future operations for the escalated record are not sent to Device D, but the already-distributed copy would remain on the device indefinitely. The eviction protocol is what makes the two extensions a complete solution rather than two partial ones.

---

## §K. Chapter-drafter subagent prompt (for draft stage)

```
Draft a new section for Ch16 — Persistence Beyond the Node titled
"## Per-Data-Class Device-Distribution" (~1,500 words).

Insert between the existing ## Lazy Fetch and Storage Budgets section
and the existing ## Snapshot Format and Rehydration section.

Follow the specification in docs/book-update-plan/working/44-per-data-class-device-distribution/outline.md
exactly: sub-patterns 44a–44e, word budgets per §I, cross-references per §H,
placeholder pattern per §44c, eviction-on-escalation sketch per §J.

Voice: Part III specification voice. No second-person. No hedging.
"The daemon drops" not "the daemon would drop." No academic scaffolding.

Sunfish packages: Sunfish.Kernel.Buckets (extend, in-canon),
Sunfish.Kernel.Sync (extend, in-canon), Sunfish.Kernel.Audit
(forward-looking from #48/#45), Sunfish.Foundation.Fleet (from #11).
No new top-level namespace. Mark the draft section header with an HTML
comment: <!-- code-check: Sunfish.Kernel.Buckets extension for
class-subscription manifest — confirm at code-check; illustrative pending
API confirmation -->

Add a FAILED conditions block at the end of the section (bold-labeled
bullet list) matching §F of the outline.

Do NOT modify any other sections of Ch16.
```
