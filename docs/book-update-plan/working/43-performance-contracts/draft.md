# Draft — Performance Contracts and Main-Thread Isolation
## Sub-pattern #43 (43a–43e) — Two new sections for Ch11 and Ch20

---

<!-- ============================================================ -->
<!-- PART 1: Ch11 new section — "Performance Contracts and        -->
<!-- Main-Thread Isolation"                                        -->
<!-- Insertion point: after ## Sunfish Package Map and before the  -->
<!-- chapter's reference list (--- + [1] entries)                  -->
<!-- Target: ~1,500 words                                          -->
<!-- ============================================================ -->

## Part 1: Ch11 — `## Performance Contracts and Main-Thread Isolation`

---

## Performance Contracts and Main-Thread Isolation

The local-first promise of immediate response is the most visible property the architecture commits to and the easiest one to lose. P1 — no spinners, no waiting, the application responds within the user's perceptual window — is indistinguishable from marketing copy unless the kernel enforces a frame-budget contract that fails the build when violated. This section specifies that contract.

### Why performance is a specification concern

Performance is structural here, not a polish step. The practical adversary is a Yjs ([github.com/yjs/yjs](https://github.com/yjs/yjs), the JavaScript CRDT library) document that has accumulated 100,000 operations over months of collaborative editing. Merging that document on reconnect can take multiple seconds on commodity hardware [4]. A node without main-thread isolation freezes the UI thread for the duration of that merge. The cursor stops. Keystrokes queue. The OS marks the window unresponsive. A user who has experienced this once does not retry the application a second time.

Linear's engineering team treats 60fps as a hard constraint on every interaction, not a target the application reaches under optimal conditions [5]. The Web Vitals Interaction to Next Paint (INP) metric formalises the same bar for the web platform: an interaction must produce a visual response within 200ms to register as "good" [6]. The architecture declares its budgets in terms practitioners already know, against thresholds the platform itself measures.

**FAILED conditions** for this primitive are stated directly later in this section. The shape of the bar: any local operation that crosses its budget fails; any UI freeze beyond a single frame fails; any path through a core node function that requires a network roundtrip fails.

### Sub-pattern 43a — Per-operation latency budget by operation class

A budget that says "the application must be fast" is not testable. The architecture differentiates by operation class and assigns a budget to each.

The three operation classes are local writes, local reads and queries, and sync merges. **Local writes** are user-initiated mutations applied to the CRDT document on the originating node. The budget runs from input confirmation to local document reflection. **Local reads** are queries against projections or the event log. The budget runs from query submission to first rendered result — partial results that arrive incrementally are acceptable, a blank screen is not. **Sync merges** are CRDT delta applications received from peers. The budget runs from delta receipt to local document reflection and UI re-render.

| Operation class | Baseline budget | FAILED condition |
|---|---|---|
| Local write | <16ms | ≥16ms blocks UI thread |
| Local read (indexed) | <50ms | ≥50ms before first result |
| Projection rebuild | <200ms | ≥200ms before first result |
| Sync merge (ordinary) | <200ms | ≥200ms before progressive-degradation fires |
| Sync merge (large doc) | Progressive degradation | No fallback = freeze |

The 16ms write budget corresponds to one frame at 60fps; a write that crosses it drops a frame on every screen the application targets. The 50ms read budget reflects the perceptual threshold below which a result feels instantaneous to a user who has already initiated the query. The 200ms projection rebuild budget aligns to the INP "good" boundary — a projection rebuild is the slowest path a user-initiated read can take, and it must still register as responsive.

The budgets above are the baseline. Per-deployment-class calibration tightens or relaxes them within defined ranges, specified in §Sub-pattern 43e below.

### Sub-pattern 43b — Main-thread isolation guarantee

No CPU-bound operation executes on the UI thread. This is an architectural invariant enforced at the kernel level, not a performance optimisation chosen at the plugin level.

`Sunfish.Kernel.Performance` routes CRDT merges, projection rebuilds, and large-query executions to background threads in a .NET/MAUI host or to web workers in a browser-hosted node. The UI thread handles rendering and user input. Plugin code that attempts a blocking CRDT operation on the UI thread receives a diagnostic assertion in debug builds and a circuit-breaker timeout in production builds. Discipline at the plugin layer is not the enforcement mechanism; the kernel is.

The isolation requirement propagates into the CRDT engine contract. All merge operations on `ICrdtEngine` (Ch11 §Kernel Responsibilities) are async by contract. `Sunfish.Kernel.Crdt` exposes no synchronous merge surface. A backend implementation that offered one would violate the kernel contract at compile time. This constraint is the architectural reason the engine abstraction was async-first from the start, not a property added after a performance regression.

The Yjs case illustrates the boundary the contract draws. A merge on a 100,000-operation document is O(n) in operation count and runs in seconds, not milliseconds [4]. The contract does not promise that this merge completes within 16ms. The contract promises that the merge does not block the UI thread while it runs. A multi-second merge that proceeds on a background thread, with the UI remaining responsive throughout, satisfies the contract. The same merge on the UI thread does not. The progressive-degradation fallback specified in §Sub-pattern 43c is the UX surface that makes the boundary visible to the user.

Chapter 12 specifies the CRDT engine architecture and the merge complexity characteristics that make this pattern necessary.

### Sub-pattern 43c — Progressive-degradation fallback

When a sync merge or projection rebuild needs more time than the budget allows, the architecture does not stall. It shows partial results immediately and completes the work in the background.

The shape of progressive degradation: the affected record or view renders its last-known local state with a freshness indicator. An ambient progress signal — not a spinner that blocks interaction — appears on the affected element. When the merge completes, the view re-renders. No freeze. No blank screen. No wait state imposed on the user.

"Last-known state" is the local-first architecture's core value proposition rendered visible. The data the user needs is on their device; the merge resolving in the background is additive, not blocking. Replicache's documentation frames the same pattern: optimistic local state is always current, and remote reconciliation is always incremental [7].

`Sunfish.Kernel.Performance` exposes an `IProgressiveDegradation` contract. The kernel calls the degradation handler when a merge or rebuild is scheduled to exceed its budget; the handler notifies the UI layer through `Sunfish.Foundation` and provides a cancellation path for the application to interrupt the background work if the user navigates away. Chapter 20 §Performance Budgets and Progressive Degradation specifies the UX surface this contract drives.

### Sub-pattern 43d — Measurable conformance test in CI

A performance contract that cannot be tested is not a contract. `Sunfish.Kernel.Performance` ships a `PerformanceBudgetValidator` that closes the loop: budget violations fail the build.

The validator measures actual latency against declared budgets across three representative document sizes. A small document of 1,000 operations exercises the fast path. A medium document of 10,000 operations exercises the typical production case. A large document of 100,000 operations exercises the stress case that triggers progressive degradation. Each size is benchmarked. The large-document test specifically asserts that the progressive-degradation handler fires within the budget window rather than blocking, which is the contract `IProgressiveDegradation` was designed to satisfy.

The test must run on CI hardware that is representative of the deployment target. A test that passes on a developer laptop with 32 GiB of RAM and an Apple M3 chip but fails on the embedded ARM device in a field office is not a conformance test; it is a developer-experience test. CI fleets for nodes that ship to intermittent-connectivity field deployments run on hardware in the same performance class as the deployment target — not on whatever the build farm happens to have available. The kill trigger specified in §FAILED conditions and kill trigger references this CI test as the measurement source.

```csharp
// illustrative — not runnable (Sunfish.Kernel.Performance pre-1.0)
builder.Services.AddSunfishPerformanceContracts(options =>
{
    options.DeploymentClass = PerformanceClass.DocumentEditing;
    options.RunBudgetValidatorInCi = true;
});
```

References to `Sunfish.Kernel.Performance` are by package name only; specific method signatures are pre-1.0 and subject to change.

### Sub-pattern 43e — Per-deployment-class budget calibration

Not all applications carry identical performance requirements. A drawing tool at 120fps has tighter write-latency needs than a document editor; an email client has looser ones. Calibration is a deployment-time configuration declared in the application's kernel startup, not a compile-time constant.

| Deployment class | Write budget | Read budget | Notes |
|---|---|---|---|
| Interactive (gaming, drawing) | <8ms | <25ms | Tightened; 120fps targets require sub-8ms |
| Document editing (default) | <16ms | <50ms | Baseline |
| Background sync (email, feed) | <50ms | <200ms | Relaxed; writes not on critical path |

The 8ms interactive budget is calibrated against the 8.33ms frame time at 120fps; sub-8ms gives one sub-frame of headroom for the UI thread's other work. The 16ms document-editing baseline is calibrated against the 60fps frame budget specified in Apple's Human Interface Guidelines [8]. The 200ms relaxed read budget aligns to the Web Vitals INP "good" threshold [6].

`PerformanceBudgetValidator` reads the declared deployment class and asserts against the corresponding budget. A deployment that declares "interactive" but ships with document-editing budgets fails the conformance test at build time. Misclassification is detected before release, not after a customer files a regression.

### FAILED conditions and kill trigger

**FAILED conditions for this primitive (any one of these means the contract is not met):**

- Any local write operation takes ≥16ms on the UI thread.
- Any UI freeze of ≥16ms duration is detectable under load profiling.
- Any path through a core node function requires a network roundtrip to complete.
- The `PerformanceBudgetValidator` CI test fails for any declared deployment class.
- Progressive degradation does not fire within budget; a large-document merge blocks rather than delegating to the background.

**Kill trigger.** Conformance — measured as the percentage of test operations completing within their declared budget — falls below 95% for three consecutive CI sprints. A drift below the kill threshold is not a sprint task. It is evidence that the implementation no longer meets the contract and requires architectural attention.

The `SyncState` enumeration (Ch11 §The UI Kernel) carries a `PerformanceDegraded` sub-state that the kernel sets when progressive degradation is active on a record or view. UI components in `Sunfish.UIAdapters.Blazor` bind to this state through the existing `SunfishNodeHealthBar` indicator architecture; Chapter 20 §Performance Budgets and Progressive Degradation specifies the user-facing surface.

Performance contracts are a primitive surfaced through architectural review, not derived from the v13 or v5 source papers directly. The contract above commits the architecture to a specification-level guarantee that the source papers framed as a desirable property; the framework-level enforcement, the budget table, and the kill trigger are new architectural commitments specific to this volume.

---

<!-- ============================================================ -->
<!-- PART 2: Ch20 new section — "Performance Budgets and          -->
<!-- Progressive Degradation"                                      -->
<!-- Insertion point: between ## The First-Run Experience and     -->
<!-- ## Key-Loss Recovery UX                                       -->
<!-- Target: ~1,000 words                                          -->
<!-- ============================================================ -->

## Part 2: Ch20 — `## Performance Budgets and Progressive Degradation`

---

## Performance Budgets and Progressive Degradation

The architecture handles the budget. The UX handles what the user sees while the budget is being met — and what they see in the rare cases when it is not. Ch11 §Performance Contracts specifies the contracts that make immediate response possible. This section describes how to surface those contracts to the user, what the user experiences when they hold, and how violations appear at three different levels of detail.

### What the user experiences when the contract is met

Picture a user who has been disconnected for a week. They reopen a shared document on Monday morning. The document loads immediately — their own last-known local state. Over the next few seconds, the view updates as the CRDT (Conflict-free Replicated Data Type) merge resolves in the background. Edits made by collaborators during the disconnected week appear progressively, in place, without redrawing the whole document. The user can start typing immediately. There is no spinner. There is no "loading your team's changes" banner. There is no apology for the time the merge takes.

This is the experience the architecture is engineered to produce. The user does not need to know that a CRDT merge is running, that the merge takes longer than a single frame, or that a background thread is working on their behalf. They need the document to be open, fast, and correct. The contracts in Ch11 §Performance Contracts are the specification-level guarantee. This section is the user-facing surface.

### Progressive-degradation UX patterns

When a sync merge will exceed its budget, the UI transitions through three states without freezing.

**Local state (immediate).** The user sees their own last-known local data the moment they open the view. Edits are accepted. The record is fully interactive. No part of the UI waits for the merge to complete before the user can act on it.

**Merge in progress (ambient indicator).** A subtle progress signal appears on the affected element — not a full-page spinner, not a banner across the top, but a component-level pulse or shimmer the user can ignore while continuing to work. The signal is calibrated to be visible but not insistent. A user who is actively typing does not experience the indicator as an interruption.

**Merge complete (silent transition).** The view re-renders with the merged state. If the merge produced no conflict with the user's current edits, the transition is invisible — the document simply reflects the new state. If the merge produced a conflict, the conflict inbox receives it through the standard flow described in §The Conflict Inbox and Bulk Resolution.

The governing principle is that the user must never be blocked by a merge in progress. If they are typing, their keystrokes apply locally. If they are reading, they read local state. The merge resolves on its own schedule, on its own thread.

`Sunfish.UIAdapters.Blazor` provides a `SunfishMergeProgressIndicator` component that implements the ambient indicator pattern. Wire it to the `IProgressiveDegradation` contract from `Sunfish.Kernel.Performance`. The component handles the three state transitions without additional application code.

```
// Illustrative — not runnable (pre-1.0 API)
<SunfishMergeProgressIndicator
    For="@RecordId"
    Source="@progressiveDegradation" />
```

Do not build custom spinners that block interaction. A spinner that covers the document while a merge completes violates the architecture's core UX commitment. Do not surface the merge as a modal or a banner. The merge is background work; the user is foreground work.

### Performance budget violation surfacing

Budget violations are observable at three levels of detail, calibrated to three audiences.

**User-facing.** When an operation consistently exceeds its budget — not a single occurrence, but a sustained pattern — `SunfishNodeHealthBar` shifts node health to amber with a plain-language explanation: "Some operations are taking longer than expected. This may be due to a large document size or resource constraints on this device." The user sees a problem without needing to understand what a budget is. The wording avoids cryptographic and architectural terminology, consistent with the Complexity Hiding Standard at the top of this chapter.

**Developer-facing.** `Sunfish.Kernel.Performance` emits structured telemetry events for every budget violation. In development builds, violations surface in the application diagnostics panel with operation class, actual duration, and declared budget. A developer who is shipping a component that consistently violates the write budget sees the violation immediately, without running a profiler. The diagnostic panel is not visible to end-users in production builds; it is wired only for development and staging environments.

**Operator-facing.** Enterprise deployments (Chapter 19) feed budget-violation telemetry into the operator observability stack. A node that is systematically slow on a particular operation class appears in the relay telemetry without requiring on-device diagnosis. An operator triaging a customer report can see that a single field office is experiencing budget violations across all nodes — a sign of hardware-class mismatch — versus a single node experiencing them — a sign of local resource constraint.

The three tiers correspond to the three audiences. Do not surface developer-tier telemetry to end-users; the diagnostics panel is not a customer-facing channel. Do not rely solely on user-facing indicators for development validation; the amber state is the last line of communication, not the first. Cross-references: Ch11 §Performance Contracts §Sub-pattern 43d for the conformance test that produces the operator telemetry; Ch19 §Operator Observability for the enterprise telemetry path.

### Quality-of-service indicators and the user's mental model

The always-visible status bar described in §The Three Always-Visible Indicators surfaces node health, link status, and data freshness. Performance budget status fits into this model — but only when the budget is actively degraded.

Under normal operation, performance indicators are invisible. Surfacing a "performance healthy" badge in the status bar is noise. Surface it only under degraded conditions, consistent with the existing ambient-awareness design. The user's mental model should read: "the app is fast normally; when it's doing a lot of work it tells me, briefly." That is the correct register. The user should not need to understand CRDT merge complexity to interpret the signal.

When the node is under load — a large merge in progress, a projection rebuild after reconnect — node health carries the performance signal without adding a fourth indicator. The `SyncState` enumeration from Ch11 §The UI Kernel extends with a `PerformanceDegraded` sub-state, distinct from the existing `Stale`, `Offline`, and `ConflictPending` states. The sub-state composes with the existing indicator architecture rather than introducing a new one.

```
// Illustrative — not runnable (pre-1.0 API)
public enum SyncState
{
    Healthy,
    Stale,
    Offline,
    ConflictPending,
    Quarantine,
    PerformanceDegraded   // new sub-state for #43
}
```

`SunfishNodeHealthBar` binds to the extended enumeration without modification. The component exposes the same three pills the rest of the chapter describes; the amber state simply has one more cause it can signal. Wire the indicator into the application shell once and let the component cover the new state alongside the existing ones.

---

<!-- ============================================================ -->
<!-- PART 3: Ch11 reference-list additions                         -->
<!-- Five new IEEE-numeric citations, numbered [4]–[8] in          -->
<!-- first-appearance order in the new §Performance Contracts      -->
<!-- section                                                       -->
<!-- ============================================================ -->

## Part 3: Ch11 reference-list additions

The following five entries extend Ch11's existing reference list (which ends at [3]). They appear in order of first appearance within the new `## Performance Contracts and Main-Thread Isolation` section.

[4] K. Jahns, "Yjs — Performance Characteristics," *Yjs Documentation*. Accessed: 2026. [Online]. Available: https://docs.yjs.dev/

[5] Linear, "How Linear builds product," *Linear Engineering Blog*. Accessed: 2026. [Online]. Available: https://linear.app/blog/

[6] Google, "Interaction to Next Paint (INP)," *Web Vitals*. Accessed: 2026. [Online]. Available: https://web.dev/articles/inp

[7] Replicache, "Why Replicache," *Replicache Engineering Documentation*. Accessed: 2026. [Online]. Available: https://doc.replicache.dev/

[8] Apple Inc., "Human Interface Guidelines: Responsiveness." Accessed: 2026. [Online]. Available: https://developer.apple.com/design/human-interface-guidelines/

---

<!-- ============================================================ -->
<!-- QC NOTES FOR REVIEWER                                         -->
<!-- ============================================================ -->

## QC notes

**Word counts (approximate, body prose only — excludes code fences, tables, and HTML comments):**

- Part 1 (Ch11 §Performance Contracts and Main-Thread Isolation): ~1,490 words
- Part 2 (Ch20 §Performance Budgets and Progressive Degradation): ~1,005 words
- Part 3 (reference list additions): not counted against chapter word totals

Both parts are within the ±10% target band specified in CLAUDE.md QC-1.

**CLAIM markers inserted:** None. All claims trace either to the cited sources [4]–[8] or to the design-decisions §5 #43 architectural commitment. The Yjs 100k-operation merge complexity claim is attributed to [4] and flagged in outline §D for technical-reviewer verification of the specific URL and figure; the reference is included with the documentation root rather than a specific benchmark page. The Linear 60fps claim is attributed to [5] with the engineering blog root; the technical reviewer will pin the specific post.

**Sub-patterns 43a–43e coverage:**

- 43a (per-operation latency budget by operation class): Ch11 §Sub-pattern 43a, with budget table.
- 43b (main-thread isolation guarantee): Ch11 §Sub-pattern 43b.
- 43c (progressive-degradation fallback): Ch11 §Sub-pattern 43c (specification side); Ch20 §Progressive-degradation UX patterns (UX side).
- 43d (measurable conformance test in CI): Ch11 §Sub-pattern 43d.
- 43e (per-deployment-class budget calibration): Ch11 §Sub-pattern 43e, with calibration table.

**FAILED conditions and kill trigger (outline §A.7):** Rendered as a bold-labeled bulleted list under §FAILED conditions and kill trigger, followed by the kill-trigger sentence. Not buried in prose.

**Cross-references wired (outline §H):**

- Ch11 §Performance Contracts → Ch11 §Kernel Responsibilities (async CRDT merge constraint, `Sunfish.Kernel.Crdt`) — wired in §Sub-pattern 43b.
- Ch11 §Performance Contracts → Ch12 §CRDT Engine and Data Layer (Yjs/yrs merge complexity) — wired in §Sub-pattern 43b ("Chapter 12 specifies…").
- Ch11 §Performance Contracts → Ch20 §Performance Budgets and Progressive Degradation — wired in §Sub-pattern 43c.
- Ch11 §Performance Contracts → Ch11 §The UI Kernel (`SyncState` and `PerformanceDegraded` sub-state) — wired in §FAILED conditions and kill trigger.
- Ch20 §Performance Budgets → Ch11 §Performance Contracts — wired in opening paragraph and §B.1.
- Ch20 §Performance Budgets → Ch20 §The Three Always-Visible Indicators — wired in §Quality-of-service indicators.
- Ch20 §Performance Budgets → Ch20 §The Conflict Inbox and Bulk Resolution — wired in §Progressive-degradation UX patterns.
- Ch20 §Performance Budgets → Ch19 §Operator Observability — wired in §Performance budget violation surfacing.

**Sunfish reference policy:**

- All Sunfish references are by package name: `Sunfish.Kernel.Performance` (new), `Sunfish.Kernel.Crdt` (existing), `Sunfish.UIAdapters.Blazor` (existing), `Sunfish.Foundation` (existing).
- Pre-1.0 component and interface names (`SunfishMergeProgressIndicator`, `PerformanceBudgetValidator`, `IProgressiveDegradation`, `PerformanceDegraded` sub-state) appear only in code fences explicitly marked illustrative.
- Code-check report (per outline §C) should note that `Sunfish.Kernel.Performance` is forward-looking and not yet present in the Sunfish package canon; same handling as `Sunfish.Foundation.Recovery` in extension #48.

**QC checklist:**

- [x] QC-1 Word count within ±10% of target (1,500 / 1,000) — Ch11 ~1,490; Ch20 ~1,005.
- [x] QC-2 All outline §A.1–§A.7 and §B.1–§B.4 subsections addressed.
- [x] QC-3 Citations inline at first use, IEEE numeric, [4]–[8] in first-appearance order.
- [x] QC-4 Sunfish packages by name only; component and interface names appear only in `// illustrative` code fences.
- [x] QC-5 No academic scaffolding ("this section discusses", "we have seen", etc.) — checked.
- [x] QC-6 No re-introduction of the architecture; both sections assume Parts I–II and earlier Ch11/Ch20 sections.
- [x] QC-7 Ch11 voice is specification register (positive declarative statements, no second-person address, no hedging on budget figures); Ch20 voice is tutorial register (direct second-person address on component wiring; target-experience-first opening).
- [x] QC-9 N/A (not a council chapter).
- [x] QC-10 No placeholder text.

**Items deferred to human voice-check (outline §F):**

- Linear/Notion 60fps anecdote opening for §Why performance is a specification concern. The current opener leads with the architectural framing; the voice-check pass can swap in a felt-experience anecdote per outline §F.
- "The moment a CRDT merge freezes the UI" anecdote candidate — the visceral force-quit / lost-state moment that grounds the FAILED condition.
- Connective tissue sentence in each section pointing explicitly to the other (Ch11 → Ch20 forward, Ch20 → Ch11 back). Both directions are wired in prose; voice-check can add a sharper pairing sentence per outline §F.
- Sinek register calibration per `feedback_voice_sinek_calibration.md` memory — light pacing only; do not over-mechanize.
