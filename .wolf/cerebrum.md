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

## Do-Not-Repeat

<!-- Mistakes made and corrected. Each entry prevents the same mistake recurring. -->
<!-- Format: [YYYY-MM-DD] Description of what went wrong and what to do instead. -->
- [2026-04-24] Do NOT attribute `ISchemaLens` or `LensGraph` to `Sunfish.Kernel.Runtime`. They live in `Sunfish.Kernel.SchemaRegistry`. Runtime owns upcasters (`ISchemaVersion`) only.
- [2026-04-24] Do NOT invent ICrdtEngine methods like `OpenOrCreateAsync()`. Real API: `CreateDocument()` and `OpenDocument()` (both sync).
- [2026-04-24] Do NOT describe loro-cs as "actively maintained with small version lag" — it's very bare bones, multi-week effort to complete bindings.

## Decision Log

<!-- Significant technical decisions with rationale. Why X was chosen over Y. -->
