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
- [2026-04-24] Do NOT claim OnboardAsync persists attestation or applies snapshot in Wave 3.x — both are deferred to Wave 4.
- [2026-04-24] SunfishNodeHealthBar lives in Sunfish.UIAdapters.Blazor, NOT Sunfish.Foundation.LocalFirst.
- [2026-04-24] Razor illustrative marker syntax: use @* illustrative — not runnable (pre-1.0 API) *@ not HTML comment syntax inside fenced razor blocks.

## Decision Log

<!-- Significant technical decisions with rationale. Why X was chosen over Y. -->
