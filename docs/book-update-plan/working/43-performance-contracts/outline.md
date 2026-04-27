# 43 — Performance Contracts with Framework-Level Enforcement — Outline

**ICM stage:** outline → ready for draft.
**Target chapters:** Ch11 (node architecture, Part III) + Ch20 (UX, Part IV).
**Total word target:** 2,500 words (Ch11 ~1,500; Ch20 ~1,000).
**Source:** `docs/reference-implementation/design-decisions.md` §5 entry #43 (sub-patterns 43a–43e).
**Why this is second in the priority list:** the most common critique of local-first deployments is not correctness — it is speed. "Local-first feels slow" is the objection that kills adoption. P1 (no-spinners) without an explicit, measurable, framework-enforced contract is aspiration, not architecture. This extension converts P1 from a claim into a verifiable invariant.

---

## §A. New section in Ch11 — "Performance Contracts and Main-Thread Isolation"

**Insertion point:** after the existing `## Sunfish Package Map` section and before the chapter's reference list (`---` + `[1]` entries). The Package Map is the final substantive section of Ch11 — it surveys what the kernel owns. Performance contracts belong here because they constrain how the kernel implements those responsibilities, not how domain plugins use them. Inserting after the Package Map closes the specification register with the enforcement layer: here is what the stack is made of; here is what it must deliver at runtime.

**Word target:** 1,500 words.

**H2:** `## Performance Contracts and Main-Thread Isolation`

### A.1 Why performance is a specification concern, not an optimisation concern (≈200 words)

- P1 (no-spinners, immediate response) is the first and most visible of the Kleppmann local-first properties. Without a frame-budget commitment, P1 is indistinguishable from marketing copy.
- The practical adversary: a Yjs/yrs document that has accumulated 100,000 operations (a realistic document after months of collaborative editing) can take multiple seconds to merge on reconnect. Without main-thread isolation, that merge freezes the UI thread. The user's cursor stops. Keystrokes queue up. The application appears hung.
- The canonical comparison: Linear's engineering blog is explicit that the product is built around 60fps as a hard constraint, not a target [cite]. The same bar applies here. A local-first node that cannot hit 60fps during normal use has not cleared P1.
- Web Vitals INP (Interaction to Next Paint) sets the web-platform equivalent: interactions must produce a visual response within 200ms [cite]. The architecture must declare its budget in terms practitioners already know.
- The design-decisions §5 FAILED conditions for this primitive state the bar directly: any operation that crosses budget fails; any UI freeze longer than 16ms fails; any path that requires network for a core function fails.

### A.2 Sub-pattern 43a — Per-operation latency budget by operation class (≈300 words)

- Performance budgets are meaningless unless they differentiate by operation type. A budget that says "the application must be fast" is not testable.
- Three operation classes with named budgets:
  - **Local write:** the time from user input confirmation to the CRDT document reflecting the write locally. Budget: <16ms (one frame at 60fps). Local writes must feel instantaneous. They have no network dependency.
  - **Local read / query:** the time from a query submission to the first rendered result. Budget: <50ms for indexed queries; <200ms for projection rebuilds from the event log. "From the first rendered result" is the critical phrasing — partial results that arrive incrementally are acceptable; a blank screen is not.
  - **Sync merge:** the time from receiving a CRDT delta to the local document reflecting it and UI re-rendering. Budget: <200ms for ordinary deltas; progressive-degradation fallback for merges that exceed this budget (see §A.4). Sync merges have no user-facing urgency that a local write has — but they also must not freeze the UI.
- Deployment-class calibration is specified in §A.5 below. The budgets above are the baseline; specific deployment classes may tighten or relax them within defined ranges.
- The budget table:

| Operation class | Baseline budget | FAILED condition |
|---|---|---|
| Local write | <16ms | ≥16ms blocks UI thread |
| Local read (indexed) | <50ms | ≥50ms before first result |
| Projection rebuild | <200ms | ≥200ms before first result |
| Sync merge (ordinary) | <200ms | ≥200ms before progressive-degradation fires |
| Sync merge (large doc) | Progressive degradation | No fallback = freeze |

### A.3 Sub-pattern 43b — Main-thread isolation guarantee (≈300 words)

- The universal rule: no CPU-bound operation executes on the UI thread. This is not a performance optimisation; it is an architectural invariant enforced at the kernel level.
- The mechanism: `Sunfish.Kernel.Performance` routes all CRDT merges, projection rebuilds, and large-query executions to background threads (in a .NET/MAUI host) or web workers (in a browser-hosted node). The UI thread handles only rendering and user input.
- Why this requires framework-level enforcement rather than developer discipline: individual plugin authors cannot be trusted to offload every heavy operation. The kernel must enforce the isolation structurally — a plugin that attempts a blocking CRDT operation on the UI thread receives a diagnostic assertion failure in debug builds and a circuit-breaker timeout in production builds.
- Practical implication for `ICrdtEngine`: all merge operations on the `ICrdtEngine` abstraction are async by contract. A synchronous merge API is not permitted. `Sunfish.Kernel.Crdt` exposes no blocking merge surface.
- The Yjs/yrs case specifically: Yjs merges on large documents are O(n) in operation count. A 100,000-operation document merge can take 2–8 seconds on commodity hardware [cite Yjs complexity docs]. This does not violate the contract — it triggers the progressive-degradation fallback specified in §A.4. What it cannot do is block the main thread for 2–8 seconds.
- Cross-reference to `Sunfish.Kernel.Crdt` (Ch11 §Kernel Responsibilities) and Ch12 for CRDT engine architecture.

### A.4 Sub-pattern 43c — Progressive-degradation fallback (≈250 words)

- When a sync merge or projection rebuild genuinely needs more time than the budget allows, the architecture does not stall. It shows partial results immediately and completes in the background.
- The UX shape of progressive degradation: the affected record or view renders its last-known state with a freshness indicator. A subtle progress indicator — not a spinner that blocks interaction, but an ambient pulse on the affected element — signals that an update is arriving. When the merge completes, the view re-renders. No freeze. No blank screen.
- "Last-known state" is not a degraded experience. It is the local-first architecture's core value proposition rendered visible: the data the user needs is on their device. The merge resolving in the background is additive, not blocking.
- The Replicache documentation on local-first responsiveness uses the same framing: optimistic local state is always current; remote reconciliation is always incremental [cite Replicache].
- Implementation hook: `Sunfish.Kernel.Performance` exposes a `IProgressiveDegradation` contract. The kernel calls the degradation handler when a merge is scheduled to take longer than the budget; the handler notifies the UI layer and provides a cancellation path. Ch20 §Performance Budgets and Progressive Degradation specifies the UX side of this contract.
- Cross-reference to Ch20 §Performance Budgets and Progressive Degradation (the UX surface for this mechanism).

### A.5 Sub-pattern 43d — Measurable conformance test in CI (≈250 words)

- A performance contract that cannot be tested is not a contract. Sub-pattern 43d closes the loop: budget violations fail the build.
- The conformance test structure: `Sunfish.Kernel.Performance` ships a `PerformanceBudgetValidator` that, given a CRDT document and a set of operations, measures actual latency against the declared budgets and asserts that no operation class exceeds its threshold.
- The CI harness runs the validator against three representative document sizes: a small document (1,000 operations, fast path), a medium document (10,000 operations, typical production case), and a large document (100,000 operations, stress test that triggers progressive-degradation). Each size is benchmarked; the large-document test specifically verifies that the progressive-degradation handler fires within the budget window rather than blocking.
- The test must run on CI hardware that is representative of the deployment target. A test that passes on a developer laptop with 32GB RAM and an M3 chip but fails on the embedded ARM device in a field office is not a conformance test — it is a developer-experience test. The loop-plan kill trigger (conformance below 95% for 3 consecutive sprints) references this CI test as the measurement source.
- Reference `Sunfish.Kernel.Performance` by package name only — no method signatures (pre-1.0).

### A.6 Sub-pattern 43e — Per-deployment-class budget calibration (≈200 words)

**Decision note:** 43e is placed as a separate H3 sub-subsection rather than embedded in §A.2 because the calibration table is substantive enough to stand on its own and because the draft author needs clear guidance that calibration is a deployment-time configuration, not a compile-time constant.

- Not all applications have identical performance requirements. A gaming application at 60fps has different write-latency needs than a document-editing application; a document-editing application has different needs than an email client.
- The three deployment classes and their budget adjustments:

| Deployment class | Write budget | Read budget | Notes |
|---|---|---|---|
| Interactive (gaming, drawing) | <8ms | <25ms | Tightened; 120fps targets require sub-8ms |
| Document editing (default) | <16ms | <50ms | Baseline |
| Background sync (email, feed) | <50ms | <200ms | Relaxed; writes not on critical path |

- Calibration is declared in the application's kernel startup configuration and checked by the `PerformanceBudgetValidator` in CI. A deployment that declares "interactive" but ships with document-editing budgets fails the conformance test.
- Apple HIG specifies 16ms as the maximum frame duration for smooth 60fps rendering [cite Apple HIG]. Web Vitals INP specifies 200ms as the boundary between "good" and "needs improvement" for interaction responsiveness [cite Web Vitals]. The architecture aligns to both.

### A.7 FAILED conditions and kill trigger (≈200 words)

This sub-section makes the design-decisions §5 FAILED conditions explicit in the specification text — not buried in a YAML schema, but visible to the reader.

**FAILED conditions for this primitive (any one of these means the contract is not met):**
- Any local write operation takes ≥16ms on the UI thread.
- Any UI freeze ≥16ms duration is detectable under load profiling.
- Any path through a core node function requires a network roundtrip to complete.
- The `PerformanceBudgetValidator` CI test fails for any declared deployment class.
- Progressive degradation does not fire within budget; a large-document merge blocks rather than delegating.

**Kill trigger:** conformance falls below 95% (measured as the percentage of test operations completing within their budget) for 3 consecutive CI sprints. At that point the implementation is not meeting the contract and requires architectural attention — not a sprint task.

---

## §B. New section in Ch20 — "Performance Budgets and Progressive Degradation"

**Insertion point:** between the existing `## The First-Run Experience` section and the existing `## Key-Loss Recovery UX` section. The First-Run Experience is where users form their initial performance expectations; Performance Budgets is where those expectations become visible UX policy. Key-Loss Recovery follows as a separate trust-surface concern. This ordering also keeps the Ch20 arc coherent: onboarding (first-run) → ongoing operation quality (performance) → edge-case recovery (key-loss) → accessibility as a contract.

**Word target:** 1,000 words.

**H2:** `## Performance Budgets and Progressive Degradation`

### B.1 What the user experiences when the contract is met (≈150 words)

- The correct opening for this section in the tutorial register: describe the target experience before the mechanisms that produce it.
- A user opening a document after a week of disconnected collaborative editing sees the document load immediately — their last-known local state. Over the next few seconds, the view updates as the CRDT merge resolves in the background. Edits by collaborators appear progressively. No waiting. No spinners. The user can start typing immediately.
- This is the experience the architecture is engineered to produce. The Ch11 §Performance Contracts specification defines the contracts that make it possible. This section describes how to surface those contracts to the user and what the user sees when they are violated.

### B.2 Progressive-degradation UX patterns (≈300 words)

- **Sub-pattern 43c UX side.** When a sync merge will take longer than the budget allows, the UI transitions through three states without freezing:
  1. **Local state (immediate).** The user sees their own last-known local data. Edits are accepted. The record or view is fully interactive.
  2. **Merge in progress (ambient indicator).** A subtle progress signal appears on the affected element — not a full-page spinner, not a banner, but a component-level pulse or shimmer. The user can ignore it and keep working.
  3. **Merge complete (silent transition).** The view re-renders with the merged state. If the merge produced no conflict with the user's current edits, the transition is invisible. If it produced a conflict, the conflict inbox receives it per the standard flow (§The Conflict Inbox and Bulk Resolution).
- The governing principle: the user must never be blocked by a merge in progress. If they are typing, their keystrokes apply locally. If they are reading, they read local state. The merge resolves on its own schedule.
- `Sunfish.UIAdapters.Blazor` provides a `SunfishMergeProgressIndicator` component that implements the ambient indicator pattern. Wire it to the `IProgressiveDegradation` contract from `Sunfish.Kernel.Performance`; it handles state transitions without additional application code.
- Do not build custom spinners that block interaction. A spinner that covers the document while a merge completes violates the architecture's core UX commitment.

### B.3 Performance budget violation surfacing (≈300 words)

- Budget violations are observable by the user, by the developer, and by the operator — at different levels of detail.
- **User-facing:** when an operation consistently exceeds its budget (not a one-off; a sustained pattern), the `SunfishNodeHealthBar` shifts node health to amber with a plain-language explanation: "Some operations are taking longer than expected. This may be due to a large document size or resource constraints on this device." The user sees a problem without needing to understand what a budget is.
- **Developer-facing:** `Sunfish.Kernel.Performance` emits structured telemetry events for every budget violation. In development builds, violations surface in the application diagnostics panel with operation class, actual duration, and declared budget. A developer who is shipping a component that consistently violates the write budget sees it immediately — without needing to run a profiler.
- **Operator-facing:** in enterprise deployments (Ch19), budget violation telemetry feeds into the operator observability stack. A node that is systematically slow on a particular operation class is identifiable from the relay telemetry without requiring on-device diagnosis.
- The three tiers of observability correspond to the three audiences. Do not surface developer-tier telemetry to end-users. Do not rely only on user-facing indicators for development validation.
- Cross-reference to `Sunfish.Kernel.Performance` (Ch11 §Performance Contracts, §A.5) and Ch19 §Operator Observability for the enterprise telemetry path.

### B.4 Quality-of-service indicators and the user's mental model (≈250 words)

- The always-visible status bar (§The Three Always-Visible Indicators) already surfaces node health, link status, and data freshness. Performance budget status fits into this model as a fourth axis — but only when actively degraded.
- Under normal operation, performance indicators are invisible. Surfacing a "performance healthy" indicator in the status bar is noise. Surface it only under degraded conditions, consistent with the existing ambient-awareness design.
- When the node is under load — a large merge in progress, a projection rebuild after reconnect — the node health indicator can carry the performance signal without adding a fourth indicator. Amending the node health state to include a `PerformanceDegraded` sub-state (distinct from the existing `Stale`, `Offline`, and `ConflictPending` states from Ch11 §The UI Kernel) maintains the existing indicator architecture while extending it.
- The user's mental model: "the app is fast normally; when it's doing a lot of work it tells me." This is the correct register. The user should not need to understand CRDT merge complexity to interpret the signal.
- Note to the draft author: confirm with Ch11 §The UI Kernel whether a `PerformanceDegraded` sub-state on `SyncState` is the right hook or whether a separate observable on `SunfishNodeHealthBar` is cleaner. Either is architecturally sound; the draft should pick one and mark it `// illustrative — not runnable` per the Sunfish reference policy.

---

## §C. Code-Check Requirements

The draft references the following Sunfish namespaces by name only (per CLAUDE.md Sunfish reference policy — pre-1.0; package names not class APIs):

- `Sunfish.Kernel.Performance` — performance contract interfaces, budget validator, progressive-degradation hook (new package in this extension; mark all references `// illustrative — not runnable`)
- `Sunfish.Kernel.Crdt` — already cited in Ch11; the constraint that merge APIs are async by contract belongs here
- `Sunfish.UIAdapters.Blazor` — already cited in Ch11 and Ch20; `SunfishMergeProgressIndicator` is a new component in this extension; mark `// illustrative — not runnable`
- `Sunfish.Foundation` — referenced via `SyncState` enum; existing citation; the `PerformanceDegraded` sub-state is a new enum value; mark `// illustrative`

All new component and interface names in this extension are pre-1.0 additions. Every reference follows the "package name only, no method signatures, mark illustrative" rule.

**Note for the code-check stage:** `Sunfish.Kernel.Performance` does not appear in the current Sunfish package canon. Before the draft advances to `code-check`, validate whether this package name has been added to the Sunfish reference implementation or whether a different canonical name is in use. If not yet present, all references remain illustrative and the code-check report should note the gap as a forward-looking reference (same handling as `Sunfish.Foundation.Recovery` in extension #48).

---

## §D. Technical-Review Focus

For the `@technical-reviewer` pass:

- **Apple HIG 16ms frame budget:** verify the claim traces to current Apple HIG documentation (not just a common-knowledge assertion). The correct citation is Apple's Human Interface Guidelines, "Responsiveness" section. Verify the specific 16ms figure is stated there or derivable from the documented 60fps target.
- **Web Vitals INP:** verify the 200ms "good" threshold is current. INP replaced FID in the Core Web Vitals set in March 2024; confirm the thresholds: ≤200ms good, 200–500ms needs improvement, >500ms poor [cite Web Vitals INP spec]. Confirm this is the right metric (INP, not FCP or LCP) for the interaction-responsiveness claim.
- **Yjs 100k-operation merge complexity:** the claim that "Yjs merges on large documents can take 2–8 seconds on commodity hardware" needs a specific citation. Check the Yjs GitHub issues, Yjs documentation, or benchmarks (e.g., the `yjs-benchmarks` repository or Kevin Jahns' documented performance characteristics). The claim is plausible but needs a traceable source, not a design-decisions assertion.
- **Replicache documentation on local-first responsiveness:** trace the progressive-degradation framing to Replicache's documentation or engineering blog. Confirm the "optimistic local state is always current; remote reconciliation is always incremental" framing is theirs or is a reasonable paraphrase attributable to them.
- **Linear 60fps claim:** trace to a specific Linear engineering blog post, not just "Linear is known for 60fps." The design-decisions §5 entry lists "Linear's 60fps obsession" as a source. The technical reviewer must find the specific post and confirm the claim is stated there in a quotable form.
- **The per-deployment-class budget table (§A.6):** verify the 8ms "interactive" class budget is consistent with 120fps screen requirements (8.33ms frame time at 120fps; <8ms budget gives one sub-frame of headroom). Confirm the math is stated correctly.
- **Trace every architectural claim** to v13/v5 source papers OR mark as new architectural commitment surfaced through universal-planning review (per design-decisions §5 #43). Performance contracts are a new primitive not covered in v13/v5; the section should acknowledge this explicitly rather than implied sourcing.

---

## §E. Prose-Review Focus

For the `@prose-reviewer` + `@style-enforcer` pass:

- Active voice throughout. "The kernel routes CRDT merges to a background thread" — not "CRDT merges are routed to a background thread by the kernel."
- Specification register for Ch11. Every claim is a positive statement of what the architecture does, not a suggestion. "The merge API is async by contract" — not "the merge API should be async."
- Tutorial register for Ch20. Direct second-person address where appropriate: "Wire `SunfishMergeProgressIndicator` to the `IProgressiveDegradation` contract" — not "the developer should wire."
- No hedging on the budget figures. "The write budget is 16ms" — not "the write budget is typically around 16ms."
- No academic scaffolding. No "this section discusses" or "we have seen that." Lead with the punchline: the FAILED condition table at §A.2 is itself the punchline of that subsection — put the table early, not late.
- Paragraph length cap: 6 sentences.
- The FAILED conditions table in §A.7 is intentionally direct. Do not soften it during prose review. The same instruction applies here as in the #48 outline: the honest limitation statement is not a weakness; it is the specification being honest about its own boundary.

---

## §F. Voice-Check Focus (HUMAN STAGE — not autonomous)

For the human voice-pass:

- **The Linear/Notion 60fps anecdote.** The most potent opening for this section is a brief story: a developer opens Linear and notices they can't make it lag. They then open a competing tool and feel the difference immediately. The anecdote grounds the technical contract in a physical, felt experience before the architecture is described. The author should write a version of this story from their own product experience.
- **"The moment a CRDT merge freezes the UI."** Candidate anecdote: the author (or a known product) experiences the "hung application" moment that this primitive is designed to prevent — cursor stops responding, OS marks the window unresponsive, the user force-quits and loses the unsaved state. The anecdote makes the FAILED condition visceral rather than abstract.
- **The connective tissue between Ch11 §Performance Contracts and Ch20 §Performance Budgets.** A single sentence in each section pointing to the other: Ch11 points forward to Ch20 for the UX surface; Ch20 points back to Ch11 for the specification. The author adds this during voice-check to make the policy/UX pairing explicit.
- Calibrate Sinek register lightly per `feedback_voice_sinek_calibration.md` memory — do not over-mechanize the prose with deliberate-pacing hammering.

---

## §G. Citations

The draft adds these to Ch11's reference list (IEEE numeric, continuing after the existing `[1]`, `[2]`, `[3]`):

**[N] Apple Inc., Human Interface Guidelines: "Responsiveness."** Accessed 2026. [Online]. Available: https://developer.apple.com/design/human-interface-guidelines/

**[N] Google, "Interaction to Next Paint (INP)," Web Vitals.** Accessed 2026. [Online]. Available: https://web.dev/articles/inp

**[N] K. Jahns, "Yjs Documentation — Performance Characteristics."** (or the equivalent canonical Yjs source for the 100k-operation merge benchmark claim — the exact URL must be verified by the technical reviewer before citation.)

**[N] Replicache, "Why Replicache," Engineering Documentation.** Accessed 2026. [Online]. Available: https://doc.replicache.dev/

**[N] Linear, "How Linear builds product" (or equivalent engineering blog post citing 60fps commitment).** Accessed 2026. [Online]. Available: https://linear.app/blog/ (exact post to be verified by technical reviewer.)

**Note on citation numbering:** Ch11 currently has three numbered references ([1] CBOR RFC 8949; [2] Schrems II; [3] Flease). The new citations for extension #43 begin at [4] and continue sequentially. The technical reviewer must confirm the first-appearance order in the draft and assign final numbers accordingly.

Ch20 cross-references Ch11's citation list. No new citations are needed in Ch20 unless a Ch20-specific source surfaces during drafting.

---

## §H. Cross-References to Add

Inside the new sections:

- Ch11 §Performance Contracts → Ch11 §Kernel Responsibilities (async CRDT merge constraint references `Sunfish.Kernel.Crdt`)
- Ch11 §Performance Contracts → Ch12 §CRDT Engine and Data Layer (Yjs/yrs merge complexity documented there)
- Ch11 §Performance Contracts → Ch20 §Performance Budgets and Progressive Degradation (the UX surface for the progressive-degradation mechanism)
- Ch11 §Performance Contracts → Ch11 §The UI Kernel (the `SyncState` enumeration and `PerformanceDegraded` sub-state addition)
- Ch20 §Performance Budgets → Ch11 §Performance Contracts (the specification these UX patterns surface)
- Ch20 §Performance Budgets → Ch20 §The Three Always-Visible Indicators (the existing status bar this section extends)
- Ch20 §Performance Budgets → Ch20 §The Conflict Inbox (merge completion that produces a conflict routes there)
- Ch20 §Performance Budgets → Ch19 §Operator Observability (budget violation telemetry for enterprise deployments)

---

## §I. Subagent Prompt for the Draft Stage

The next iteration (`outline → draft`) will invoke `@chapter-drafter` with this prompt:

> Draft two new sections for *The Inverted Stack*: (1) `## Performance Contracts and Main-Thread Isolation` for Ch11 (~1,500 words, inserted after the existing `## Sunfish Package Map` section and before the reference list); and (2) `## Performance Budgets and Progressive Degradation` for Ch20 (~1,000 words, inserted between the existing `## The First-Run Experience` section and the existing `## Key-Loss Recovery UX` section).
>
> Source: outline at `docs/book-update-plan/working/43-performance-contracts/outline.md`. Follow the section structure and word targets exactly.
>
> Voice: Part III specification register for Ch11 (positive declarative statements, no hedging, no second-person address). Part IV tutorial register for Ch20 (direct second-person address on component wiring steps; clear target-experience description before the mechanism; explicit "do not" instructions for common mistakes).
>
> Active voice throughout. No hedging on budget figures. No academic scaffolding. No re-introducing the architecture (Ch11 assumes Parts I–II and earlier Ch11 sections; Ch20 assumes Part I, Ch11, and earlier Ch20 sections).
>
> Sub-patterns: 43a through 43e must each appear as a named subsection in Ch11 (§A.2 through §A.6 in the outline). 43c appears in both Ch11 (specification) and Ch20 (UX surface); write both sides.
>
> FAILED conditions (from outline §A.7) must appear explicitly as a FAILED conditions block in Ch11 — not buried in prose. Format as a short bulleted list under a bold **FAILED conditions** label before the kill trigger sentence.
>
> Sunfish references: package names only (`Sunfish.Kernel.Performance`, `Sunfish.Kernel.Crdt`, `Sunfish.UIAdapters.Blazor`, `Sunfish.Foundation`) — no class APIs, no method signatures. Component names (`SunfishMergeProgressIndicator`, `PerformanceBudgetValidator`) are new in this extension; mark all code snippets `// illustrative — not runnable`.
>
> Citations: IEEE numeric. Add the five sources listed in outline §G to Ch11's reference list, continuing after the existing [3]. First-appearance order in the draft determines the numbering. Ch20 cross-references Ch11 — no new citations in Ch20.
>
> Cross-references: per outline §H — the draft must wire all of them. The Ch11→Ch20 and Ch20→Ch11 cross-references are the most important pair; they make the policy/UX pairing visible.
>
> Insertion mechanics: write the new H2 sections directly into the existing chapter files at the specified insertion points. Preserve existing H2 anchor structure and H1 frontmatter. Update Ch11's reference list with the new entries.

---

## §J. Quality Gate for `outline → draft`

Per loop-plan §5: outline has all section headers + bullet points (✓ §A.1 through §A.7 above; ✓ §B.1 through §B.4 above); word count target estimated (✓ 1,500 + 1,000 = 2,500); subagent prompt prepared (✓ §I above). Gate passes.

The five sub-patterns (43a–43e) each have a designated subsection: 43a in §A.2, 43b in §A.3, 43c in §A.4, 43d in §A.5, 43e in §A.6. All five are in Ch11. 43c additionally surfaces in Ch20 §B.2 as the progressive-degradation UX. Requirement satisfied.

The FAILED conditions and kill trigger from design-decisions §5 #43 are reflected in §A.7 of this outline. Requirement satisfied.

---

**Estimated next-iteration duration (draft stage):** 45–75 minutes. Shorter than the #48 draft stage because the performance contracts material is more precisely scoped (no six-mechanism taxonomy; no threat-model section of comparable depth). Schedule next fire 1 hour after this one to allow context-cache cooldown and human-review window.
