## Data-Class Escalation UX

<!-- code-check annotations: Sunfish.Kernel.Security (in-canon, surfaces the re-classification policy and the access-control re-evaluation); Sunfish.Kernel.Audit (in-canon per cerebrum 2026-04-28, supplies the escalation-event record the operator UI reads); Sunfish.Kernel.SchemaRegistry (in-canon, supplies the cross-class reference index the operator review surface queries); Sunfish.Kernel.Sync (in-canon, propagates the operation); Sunfish.UIAdapters.Blazor (in-canon, hosts the class-indicator component alongside SunfishFreshnessBadge). 0 new top-level namespaces. 0 class APIs / method signatures introduced. -->

Revocation removes a person from a workspace. Re-classification changes what a record is. Both shift access without user action, and both belong in the same UX neighbourhood — a user who has just learned to read the revocation message should find the escalation message immediately legible from the same vocabulary. The mechanism that makes that legibility possible is specified in Ch15 §Event-Triggered Re-classification. This section does not re-state it. It covers what the user sees: the escalated-record indicator on the affected card, the access-tightened message that lands when a previously-readable record refuses a read, the offline-reconnect experience, the operator-side escalation flow, and the cross-class reference review prompt that follows an escalation upstream.

The §AP/CP Visibility by Data Class table at the top of this chapter assigned each record a class at deployment time. Re-classification changes which row of that table a record belongs to. The freshness threshold, the staleness UI, and the read-access constraint move with it.

### The record-level escalation indicator

An escalated record gains a class-changed indicator on its card or row in the application's main UI. The indicator is a small badge — coloured to match the record's new class, paired with a text label — placed in the same slot the freshness badge occupies for AP/CP indication. Both badges are visible together; they communicate orthogonal facts and both matter. The text label reads "Class changed" with a tooltip that names the new class in plain language: "This record was re-classified as evidence on 12 March. Access has tightened." Do not surface the prior class in the default tooltip. A user with no prior context for the record does not need to learn its history; they need to know the current state.

The badge persists on the record for fourteen days after escalation, then fades into the standard class indicator. The fourteen-day persistence is a UX choice, not an architectural one — the audit record persists indefinitely. The visible badge serves the user's working memory: a permanent escalation badge becomes ambient noise within a quarter.

The class-indicator component lives in `Sunfish.UIAdapters.Blazor` alongside the freshness badge described in §AP/CP Visibility by Data Class. Bind it to the record's current class as exposed by `Sunfish.Kernel.Security`; the component reads the most recent escalation event from `Sunfish.Kernel.Audit` for the recent-change state and updates without additional application code. Do not hand-roll the computation. The escalation-event read path is the same surface the operator console reads, and a parallel implementation will drift.

### When a previously-readable record refuses a read

A user attempting to open a record they could read yesterday but cannot read today encounters the access-tightened message. The message is plain language: "This record was re-classified on 12 March and your role no longer has access. The previous version remains in your local cache and is read-only on this device." It names the date, names the reason category — re-classification, not "permission denied" or "unauthorised" — and tells the user what they retain. The architecture does not delete the locally-cached prior version, and the message does not pretend it does.

The message does not name the new class level or the asserting authority. A user without access at the new class does not gain that information by encountering the message; revealing it would leak class information through the failure path. Operator and compliance-system identifiers stay in the audit log, visible to the operator console, not to the user whose access just ended.

If the user holds a role with access at the new class, no message appears at all — the record opens normally. The escalation has tightened the access set; if the user is still inside it, nothing changes except the badge on the card.

### The offline-reconnect experience

A user offline when the escalation fired returns to the application and finds an access change they did not initiate. The reconnect handshake processes the re-classification operation before any reads complete (Ch15 §Event-Triggered Re-classification sub-pattern 10b). On the first attempt to open the affected record, the access-tightened message appears with a small addition: "This record was re-classified on 12 March, while you were offline, and your role no longer has access."

Do not surface the escalation as a separate notification on reconnect. A list of "things that changed while you were away" invites the user to investigate records they may have no current intention of opening, which surfaces escalation events to roles that no longer hold access at all. The message lands at the moment of attempted access, where the user has a concrete intention and the message has a concrete answer.

The user's local cache of the record at its prior class remains visible in offline-mode read views — the same copy the architecture commits not to erase. A small "(read-only — cached before re-classification)" suffix names the state honestly. A user who needs the current version contacts the workspace's administrator through the support path §UX for the Non-Technical Adopter specifies.

### Operator-triggered escalation — the administrator's flow

Operator escalation lives in the same administration panel that hosts revocation. Select the record — or a saved query identifying a set of records — choose "Re-classify," and pick the new class from a list filtered to classes equal to or higher than the record's current class. The UI does not display a downward option, because §10a's max-register invariant rejects them. Provide the trigger event identifier: an incident-flag from the dispatcher console, a legal-hold reference, a regulator-notice number. The trigger identifier is required, not optional. An escalation without a named cause is rejected at the form level; the audit trail's defensibility depends on the trigger field being load-bearing.

The confirmation dialog names the consequences in plain language: "This will tighten access to [N] records. Roles losing access: [list]. The escalation cannot be reversed; if needed, you can recreate the record at a lower class with a fresh identifier." After confirmation, `Sunfish.Kernel.Security` issues the operation, `Sunfish.Kernel.Sync` propagates it, and the audit log records the assertion. A progress indicator shows propagation status across the fleet; the operator does not have to wait for full propagation to dismiss the dialog, but the badge on each affected record updates as the operation lands.

Do not surface "max-register invariant" or "CRDT operation" to the operator. Surface the business outcome: "Access tightened. [N] records re-classified to [new class]."

### Cross-class reference review

After the escalation propagates, the reference index in `Sunfish.Kernel.SchemaRegistry` identifies records holding inbound references to the escalated record (Ch15 §Event-Triggered Re-classification sub-pattern 10d). Those candidates surface in the operator's review queue as a "References to recently-escalated records" panel — a list with the candidate record, its current class, the escalated record it references, and two actions: "Confirm class unchanged" and "Re-classify upward."

The review queue does not auto-resolve. An unreviewed candidate remains in the queue indefinitely, surfaced on the operator's next session and on the periodic compliance-review prompt. The commitment is not to resolve the question — the question is domain-specific — but to refuse to lose track of it. Auto-lifting cascades unbounded; auto-dismissing leaves an audit gap. The review queue is the human-in-the-loop surface that bounds both failure modes.

### FAILED conditions

The escalation UX fails when any of the conditions below holds. Any one degrades the trust the access-change message depends on.

- **The access-tightened message names the new class level or the asserting authority to a user without access at the new class.** UX failure. The failure path leaks class metadata the user has no clearance to learn.
- **An offline-reconnect handshake delivers a read from the prior-class cache as if it were live state.** UX failure. The "(read-only — cached before re-classification)" suffix is the only correct framing for that copy.
- **The operator escalation form accepts an escalation without a trigger event identifier.** Compliance failure. The audit trail's defensibility depends on every operation naming its cause.
- **The cross-class reference review queue auto-resolves an unreviewed candidate by either lifting or dismissing it.** UX failure. The queue is the bound on the cascade; auto-resolution at either edge defeats it.

The kill trigger for this UX is an access-tightened message that lists the new class level to a user without access at that class. A primitive that uses the failure path to disclose the metadata the access tightening exists to protect is not access tightening — it is a side channel.
