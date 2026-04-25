# Cerebrum

> OpenWolf's learning memory. Updated automatically as the AI learns from interactions.
> Do not edit manually unless correcting an error.
> Last updated: 2026-04-23

## User Preferences

<!-- How the user likes things done. Code style, tools, patterns, communication. -->

## Key Learnings

- **Project:** the-inverted-stack
- **Description:** A practitioner book for software architects, technical founders, and senior engineers
- **Sunfish package split — schema migration:** `Sunfish.Kernel.Runtime` owns `ISchemaVersion` (upcaster registration only). `Sunfish.Kernel.SchemaRegistry` owns `ISchemaLens`, `LensGraph`, epoch coordinator, copy-transform migrator, and compaction scheduler. These are separate packages; do not attribute the lens engine to Kernel.Runtime.
- **Sunfish.Kernel.SchemaRegistry DI method:** `AddSunfishKernelSchemaRegistry()` (confirmed in ch11 code example).
- **Lens registration API:** `LensGraph.AddLens()` in `Sunfish.Kernel.SchemaRegistry` — not via `ISchemaVersion`.
- **ICrdtEngine real API:** `CreateDocument(string documentId)` and `OpenDocument(string documentId, ReadOnlyMemory<byte> snapshot)` — both synchronous.
- **IPostingEngine real API:** `PostAsync(Transaction tx, CancellationToken ct)` where `Transaction` = `{TransactionId, IdempotencyKey, Postings, CreatedAt}`.
- **loro-cs state:** Very bare bones (v1.10.3), snapshot/delta/vector-clock surface not exposed, multi-week binding effort needed. YDotNet is the default; Loro is aspirational.
- **SyncState component:** Lives in `Sunfish.UIAdapters.Blazor.Components.LocalFirst.SyncState`, not `Sunfish.Foundation`.
- **TFMs:** `net11.0-windows10.0.19041.0` and `net11.0-maccatalyst`.
- **DI registration for CRDT engine:** `AddSunfishCrdtEngine()`.
- **Sunfish.Foundation.LocalFirst IS a valid package** — `packages/foundation-localfirst/` exists in the Sunfish repo; `AddSunfishLocalFirst()` is a real method (takes no parameters). `LocalFirstMode` enum does NOT exist. Earlier session notes incorrectly marked this package as invalid.
- **AddSunfishKernelSync() and AddSunfishKernelSecurity()** take no parameters — do not invent options lambdas. GossipDaemonOptions uses `RoundIntervalSeconds` (int), not `GossipInterval` (TimeSpan). `AntiEntropyEnabled` does not exist.
- **Package names: Sunfish.UICore and Sunfish.UIAdapters.Blazor** are correct per repo PackageId values. Not `Sunfish.UI.Core` or `Sunfish.UI.Adapters.Blazor`.
- **SyncState enum valid values:** `Healthy`, `Stale`, `Offline`, `ConflictPending`, `Quarantine`. Do NOT use Linked, Searching, Fresh, Unknown, Degraded, or Error — none exist.
- **ILocalNodePlugin real members:** `Id` (string), `Version` (string), `Dependencies` (IReadOnlyCollection<string>), lifecycle method `OnLoadAsync(IPluginContext context, CancellationToken ct)`. Not PluginId, DependsOn, or Register(ILocalNodeBuilder).
- **IStreamDefinition real members:** `EventTypes`, `BucketContributions` — NOT DocumentTypes, StreamId as StreamId type, or BucketPolicy.
- **IProjectionBuilder real member:** `RebuildAsync(CancellationToken ct)` — NOT Build(IProjectionRegistry).
- **AddSunfishPlugin<T>()** does NOT exist in Sunfish repo.
- **GenerateFounderBundleAsync real signature:** `GenerateFounderBundleAsync(string teamName, CancellationToken ct)` — no teamId parameter.
- **IssueJoinerAttestationAsync real signature:** `IssueJoinerAttestationAsync(byte[] teamId, byte[] joinerPublicKey, ReadOnlyMemory<byte> founderPrivateKey, ...)` — NOT GenerateJoinerBundleAsync.
- **AttestationBundle:** No version field inside the CBOR payload — flat array of 7-field attestation records.
- **WriteState enum:** Does NOT exist. Do not reference WriteState.Pending, WriteState.Confirmed, or WriteState.Failed.
- **MDM node-config.json schema:** Known fields: schemaVersion, teamId, relayEndpoint, allowedBuckets, dataDirectory, logLevel, updateServerUrl, enterpriseAttestationIssuerPublicKey. `storageEncryption` field does NOT exist.

## Do-Not-Repeat

<!-- Mistakes made and corrected. Each entry prevents the same mistake recurring. -->
<!-- Format: [YYYY-MM-DD] Description of what went wrong and what to do instead. -->
- [2026-04-24] Do NOT attribute `ISchemaLens` or `LensGraph` to `Sunfish.Kernel.Runtime`. They live in `Sunfish.Kernel.SchemaRegistry`. Runtime owns upcasters (`ISchemaVersion`) only.
- [2026-04-24] Do NOT invent ICrdtEngine methods like `OpenOrCreateAsync()`. Real API: `CreateDocument()` and `OpenDocument()` (both sync).
- [2026-04-24] Do NOT describe loro-cs as "actively maintained with small version lag" — it's very bare bones, multi-week effort to complete bindings.
- [2026-04-24] Do NOT use SyncState.Linked, .Searching, .Fresh, .Unknown, .Degraded, or .Error — valid values are only Healthy, Stale, Offline, ConflictPending, Quarantine.
- [2026-04-24] Do NOT invent plugin API members (PluginId, DependsOn, Register). Use Id, Dependencies, OnLoadAsync.
- [2026-04-24] Do NOT use WriteState enum (Pending/Confirmed/Failed) — does not exist in Sunfish repo.
- [2026-04-24] Do NOT invent MDM config key `storageEncryption: required` — not in node-config.json schema.
- [2026-04-24] Do NOT reference OnboardingState enum — use AnchorSessionService.IsOnboarded (bool) instead.
- [2026-04-24] Do NOT claim AddSunfishKernelRuntime() wires sync daemon, mDNS, gossip, or ICrdtEngine — it only registers INodeHost and IPluginRegistry.
- [2026-04-24] Do NOT claim AddSunfishKernelSecurity() loads/generates keypair or registers onboarding state machine — cryptographic services only.
- [2026-04-24] Do NOT describe Sunfish's CRDT as "working CRDT merge." Current StubCrdtEngine uses total-order replay, not CRDT semantics; real engine (YDotNet) validated in spike 2026-04-22 but not yet integrated into kernel-crdt. Stub file self-marks "DO NOT SHIP TO PRODUCTION."
- [2026-04-24] Do NOT claim GossipDaemon applies deltas back into ICrdtDocument — code comment confirms apply-back "still lands in Wave 2.6." Two nodes can exchange state vectors today, but concurrent edits don't converge without manual intervention.
- [2026-04-24] Do NOT claim full `dotnet build` passes on Sunfish repo — test projects (kernel-lease/tests, local-node-host/tests, blocks-forms/tests) have interface mismatches. Only apps/local-node-host builds cleanly as of 2026-04-24.
- [2026-04-24] Do NOT claim OnboardAsync persists attestation or applies snapshot in Wave 3.x — both are deferred to Wave 4.
- [2026-04-24] SunfishNodeHealthBar lives in Sunfish.UIAdapters.Blazor, NOT Sunfish.Foundation.LocalFirst.
- [2026-04-24] Razor illustrative marker syntax: use @* illustrative — not runnable (pre-1.0 API) *@ not HTML comment syntax inside fenced razor blocks.

## Decision Log

<!-- Significant technical decisions with rationale. Why X was chosen over Y. -->

## Decision Log — 2026-04-25 — Phase 0.0 timing pilot

**Decision: skip Task 2 (MED-tier pilot); proceed to Phase 0 sweep without timing data.**

**Reasoning:** Author has stated the project has no deadline and will take as long as it takes. Real timing data is therefore not load-bearing for the continue/abort decision. Use a conservative estimate as a sanity check rather than a budget.

**Conservative estimate for Phase 0** (assuming Claude does the compression with author review):
- 12 HIGH-severity paragraphs × ~5 min Claude generation + ~5 min author review = 2 hours
- ~30 MED-severity paragraphs × ~3 min generation + ~3 min review = 3 hours
- Appendix F creation (Task 6) = ~4 hours (substantive compilation work)
- Disclosures + verification + commit hygiene = ~2 hours
- **Conservative total: ~11 hours.** Well within the original 24-48h budget; no need to invoke Alternative A or B.

**Decision: CONTINUE with Phase 0 sweep.** Plan Task 3 (the projection gate) is satisfied: projection ≤48h, continue.

## Decision Log — 2026-04-25 — Phase 0.5 result

**Decision: ORIGINAL PLAN stands.** Phase 0.5 methodology test produced a fresh Gladwell pass-1 on cleaned Ch01 (`chapters/_voice-drafts/pass1/ch01-when-saas-fights-reality.md`, 5,447 words). Author's verdict: "the ch01 reality check looks good" — confirming pass-1 did not regress after Phase 0a; pass-2 (Sinek polish over Gladwell) is still needed for the book's house voice.

**Phase 1 scope unchanged:** tune all six voice agents (sinek + 5 guests). Polish/normalize tier system as planned.

## GitButler state — 2026-04-25

GitButler was set up earlier in the session and torn down via `but teardown`
after a workspace-conflict error during `but setup` retry. Current state:

- `.git/gitbutler` directory still exists (residual)
- `gitbutler/target` and `gitbutler/workspace` branches still exist locally
  with leftover commits (b244d05, adef29e, db4a0a1)
- Working in plain git mode on `main`; no GitButler hooks active
- All work since teardown has been clean linear commits on `main`

**Implication for future sessions:** the user's global GitButler detection
(`test -d .git/gitbutler`) will return "GitButler-managed" and trigger the
`use-gitbutler.md` workflow. But `but` commands will fail until either:
(a) the leftover gitbutler/* branches are cleaned and `but setup` re-run,
or (b) the .git/gitbutler directory is removed to make the repo look like
plain git again.

User has not asked for cleanup — leaving as-is. If a future session
hits `but` errors, surface this state immediately rather than retrying.

## Phase 1 → Phase 2 transition — 2026-04-25

Phase 1 closed at commit `af4e113`. Six voice agents tuned per the
ORIGINAL PLAN (Phase 0.5 decision):
- voice-sinek: chapter-scale calibration, scene preservation, audiobook
  cadence, register variation, 10% cut, preserve definitions, second
  canonical example (chapter-opening register)
- voice-gladwell, voice-brown: universal tunes (audiobook + preserve
  definitions) + 10% cut
- voice-grant: universal tunes + 10% cut + citation-enumeration guard
  (Grant-specific compounding pattern)
- voice-godin: universal tunes only (existing brevity rule already
  prevents Sinek-style compounding)
- voice-lencioni: universal tunes + preserve-narrative-scenes (fable
  agent needs scene preservation more than others) + scene-safe 10% cut

Per-invocation logging (B3/C9) added to voice-pass.py: every voice-pass
run now writes a JSON audit entry to chapters/_voice-drafts/_log/.

Phase 2 dispatched as background process bzduwnh42 — 4 pilots serial
(Ch04, Ch05, Ch11, Ch01), ~40 min wall-clock. Grading template at
docs/superpowers/specs/2026-04-25-phase2-pilot-grading.md.

In parallel: promote.py (Phase 4 prep) dispatched as subagent — TDD
work, ~20 min, non-overlapping with pilot run.
