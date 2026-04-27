# Sunfish Package Roadmap — Forward-Looking Namespaces from Volume 1 Extensions

**Status:** Living document. Authoritative source for forward-looking Sunfish package commitments made by book extensions (Volume 1).
**Cadence:** Updated whenever a book extension introduces a new Sunfish namespace. Mirrors are maintained in the Sunfish reference implementation at `C:/Projects/Sunfish/docs/specifications/inverted-stack-package-roadmap.md`.
**Last updated:** 2026-04-27.

## Purpose

The book makes architectural commitments to Sunfish packages that the reference implementation has not yet shipped. Each Volume 1 extension that introduces a new Sunfish namespace is, in effect, a roadmap commitment: the implementation will land this package, and the architecture the book describes is the contract.

This document is the canonical list of every such forward-looking namespace, the source extension that committed to it, what the package owns architecturally, the minimal surface the book references, and the implementation status in the Sunfish reference repo.

It exists for two audiences:

1. **Book readers** evaluating whether a Sunfish-aligned implementation today honors the architecture described — they need to know which packages are shipped and which are roadmap commitments.
2. **Sunfish developers** picking up implementation work — they need a single list of pending packages, ordered by priority, with the architectural commitment already specified by the book.

## Cross-references

- Each package's source extension is in `docs/reference-implementation/design-decisions.md` §5 entry #NN.
- Each extension's working artifacts (outline, draft, code-check report, technical-review report) are in `docs/book-update-plan/working/<extension-id>/`.
- Each shipped package's canonical entry is in the user-memory `project_sunfish_packages.md` (which lists in-canon packages and known-wrong APIs).
- Each package's Sunfish-side ADR (where one exists) is at `C:/Projects/Sunfish/docs/adrs/`.

## Status definitions

| Status | Meaning |
|---|---|
| `book-committed` | The book references the namespace as part of an extension's specification. No corresponding package directory exists in Sunfish. |
| `adr-accepted` | The Sunfish repo has an accepted ADR specifying the implementation choices. Package may or may not be scaffolded. |
| `scaffolded` | A package directory exists in Sunfish (`packages/<name>/`) with at least a `.csproj` and minimal interface declarations. |
| `in-development` | Active implementation work on the package. Some surface is functional, the full book-referenced surface is not yet complete. |
| `shipped` | Full book-referenced surface available. Canonical entry added to `project_sunfish_packages.md`. |

## Package roadmap

### `Sunfish.Foundation.Recovery`

| Field | Value |
|---|---|
| **Source extension** | #48 key-loss recovery |
| **Status** | `adr-accepted` (per ADR 0046) — not yet scaffolded |
| **Sunfish dir** | `packages/foundation-recovery/` (planned; does not yet exist) |
| **Sunfish ADR** | `docs/adrs/0046-key-loss-recovery-scheme-phase-1.md` (accepted 2026-04-26) |
| **Book sections** | Ch15 §Key-Loss Recovery; Ch20 §Key-Loss Recovery UX |

**Architectural commitment:** Owns the recovery primitive. Implements the six sub-patterns (48a multi-sig social, 48b custodian-held, 48c paper-key, 48d biometric-derived, 48e timed grace period, 48f recovery-event audit trail) under a unified configuration. Reads the deployment-class manifest at startup and binds the appropriate threshold and grace-period values. Emits five named event contracts: `RecoveryClaimSubmitted`, `GracePeriodObserver`, `TrusteeAttestation`, `RecoveryDispute`, `RecoveryCompleted`. Enforces the convergence rule (halt-on-dispute) at the audit-log validation layer.

**Phase 1 scope per ADR 0046:** sub-patterns 48a + 48c + 48e + 48f (multi-sig social + paper-key + 7-day timed grace + signed audit trail). Sub-patterns 48b (institutional custodian) and 48d (biometric-derived) are explicitly deferred to post-MVP. The Phase 1 architecture must not preclude adding them later — the recovery surface is an extensible enum, not hard-coded to the four ship-now flows.

**Minimal book-referenced surface:**

- `IRecoveryArrangement` — declared at first-run, persists in the team's signed configuration manifest; binds primary mechanism, secondary mechanism, deployment class, grace-period window
- `IShamirDealer` — local Shamir secret-sharing dealer (sub-pattern 48a); GF(2^256) field; OS CSRNG seed; share-wrapping under trustee public key before transit; dealer-state zeroing post-emission
- `ICustodianRelease` — out-of-band custodian release (sub-pattern 48b); local unwrap; never holds plaintext key
- `IPaperKeyDerivation` — BIP-39 mnemonic derivation through Argon2id at regulated-tier parameters (sub-pattern 48c); round-trip transcription verification at setup
- `IRecoveryAuditTrail` — signed event sequence (sub-pattern 48f); composes with chain-of-custody mechanism (#9, future)

**Open questions for the Sunfish implementation:**

- Whether the recovery audit trail uses `Sunfish.Kernel.Audit` (forward-looking, see below) or extends `Sunfish.Kernel.Ledger` / `Sunfish.Kernel.EventBus`. Decision deferred to package scaffold time.
- Whether `Sunfish.Foundation.Recovery` depends on `Sunfish.Foundation.LocalFirst` for the configuration manifest persistence or has its own.

### `Sunfish.Kernel.Audit`

| Field | Value |
|---|---|
| **Source extension** | #48 key-loss recovery |
| **Status** | `book-committed` — not yet scaffolded; potential overlap with existing packages flagged |
| **Sunfish dir** | `packages/kernel-audit/` (planned; does not yet exist) |
| **Sunfish ADR** | None yet. Referenced obliquely in ADR 0046. |
| **Book sections** | Ch15 §Key-Loss Recovery (§Recovery-event audit trail); Ch15 §Implementation Surfaces |

**Architectural commitment:** Owns recovery-event audit records and the multi-party signed-event substrate that recovery, chain-of-custody (#9 future), and other compliance-tier mechanisms compose against. Distinct from the application-data audit log because recovery records carry third-party metadata (trustee identifiers, custodian identifiers) that has different retention and erasure semantics than ordinary application data.

**Minimal book-referenced surface:**

- Recovery-event records: claim submission, trustee attestation, dispute, completion — all signed, all in the same encrypted log used for application data, but with a distinct retention class
- Default-preserve metadata posture for Article 17 erasure requests; case-specific erasure requires legal review (per Ch15 §Recovery-event audit trail closing paragraph)

**Open questions for the Sunfish implementation:**

- **Whether this is a distinct package or a subsystem of `Sunfish.Kernel.Ledger` or `Sunfish.Kernel.EventBus`.** The book treats it as a separate namespace because the retention semantics are different from the standard ledger. The implementation may choose to inline this into `kernel-ledger` with a "audit" record type rather than spinning up a new package. Either is architecturally sound; the choice belongs to whoever scaffolds it.
- Whether `Sunfish.Kernel.Audit` is the right place for the convergence-rule validator the book specifies in Ch15 §Recovery State-Machine Convergence, or whether that lives in `Sunfish.Foundation.Recovery`.

**Recommendation:** when scaffolding `Sunfish.Foundation.Recovery`, decide whether to also scaffold a separate `kernel-audit` package or to extend `kernel-ledger`. Open an ADR for that decision.

### `Sunfish.Kernel.Performance`

| Field | Value |
|---|---|
| **Source extension** | #43 performance contracts with framework-level enforcement |
| **Status** | `book-committed` — not yet scaffolded; no ADR yet |
| **Sunfish dir** | `packages/kernel-performance/` (planned; does not yet exist) |
| **Sunfish ADR** | None yet. Recommend opening one as part of the next implementation phase. |
| **Book sections** | Ch11 §Performance Contracts and Main-Thread Isolation; Ch20 §Performance Budgets and Progressive Degradation |

**Architectural commitment:** Owns the performance contract enforcement layer. Routes CPU-bound operations (CRDT merges, projection rebuilds, large-query executions) to background threads or web workers. Enforces per-operation latency budgets at the kernel level. Provides progressive-degradation hooks for operations that genuinely need more time than their budget allows. Ships a CI conformance test that fails the build on budget violations.

**Minimal book-referenced surface:**

- `PerformanceClass` — enumeration of deployment classes (`Interactive`, `DocumentEditing`, `BackgroundSync`); declared at startup
- `IProgressiveDegradation` — hook called when a merge or rebuild is scheduled to exceed its budget; provides cancellation path and notifies UI layer through `Sunfish.Foundation`
- `PerformanceBudgetValidator` — CI test that measures actual latency across three representative document sizes (1k, 10k, 100k operations) and asserts against declared budgets per deployment class
- `PerformanceDegraded` — new sub-state on `SyncState` (Ch11 §The UI Kernel); existing `SunfishNodeHealthBar` binds to it through the same indicator architecture

**Constraint propagated to existing packages:**

- `Sunfish.Kernel.Crdt` — `ICrdtEngine` merge operations are async by contract. No synchronous merge surface permitted. (This constraint is consistent with the existing async-first design per ADR 0028.)

**Phase 1 scope (recommended):** sub-patterns 43a (per-operation budget) + 43b (main-thread isolation guarantee) + 43c (progressive-degradation fallback) + 43d (CI conformance test) + 43e (per-deployment-class calibration). All five sub-patterns need to ship together for the contract to hold; partial implementation does not satisfy the FAILED-conditions block.

**Kill trigger:** conformance below 95% (test operations completing within budget) for three consecutive CI sprints. This is an architectural-attention escalation, not a sprint task.

**Open questions for the Sunfish implementation:**

- Whether `Sunfish.Kernel.Performance` is a kernel package or a foundation package. The book treats it as kernel-tier because it constrains the kernel itself.
- Whether the `PerformanceBudgetValidator` is in the package or in `tests/` infrastructure that consumes the package. The book leans toward "ships with the package" so the contract and the validator are co-located.

## Future forward-looking namespaces (priority order from `docs/book-update-plan/loop-plan.md` §1)

These namespaces will be added to this roadmap as their source extensions advance through the ICM pipeline. The list below is anticipatory; it captures expected commitments, not yet-made commitments.

| Extension | Likely namespace | Owns |
|---|---|---|
| #45 collaborator-revocation | extends `Sunfish.Foundation.Recovery` + `Sunfish.Kernel.Security` | revocation events; post-departure data partition; cached-copy management |
| #11 fleet-management | NEW `Sunfish.Foundation.Fleet` (or `Sunfish.Kernel.Fleet`) | provisioning, key rotation, OTA, observability for headless-fleet deployments |
| #47 endpoint-compromise | extends `Sunfish.Kernel.Security` | HSM/secure-enclave separation; attested boot; remote-wipe; endpoint-compromise containment |
| #46 forward-secrecy | extends `Sunfish.Kernel.Security` + `Sunfish.Kernel.Sync` | per-message ephemeral keys; double-ratchet; sealed sender |
| #9 chain-of-custody | NEW `Sunfish.Kernel.Custody` (or extends `Sunfish.Kernel.Audit`) | multi-party signed transfer receipts |
| #12 privacy-aggregation | NEW relay-side privacy module | DP, k-anonymity, l-diversity at relay |
| #10 data-class-escalation | extends `Sunfish.Foundation.Catalog` + `Sunfish.Kernel.Runtime` | event-triggered re-classification |
| #44 per-data-class-device-distribution | extends `Sunfish.Kernel.Buckets` + `Sunfish.Kernel.Sync` | per-data-class device-eligibility declarations |

These will become first-class entries in this document as the corresponding extensions reach `code-check` stage and the namespace commitments solidify in chapter prose.

## Update procedure

When a Volume 1 extension introduces a new Sunfish namespace:

1. The extension's `code-check` stage flags the namespace as forward-looking and adds an HTML comment in the chapter file identifying it.
2. The extension's `code-check-report.md` lists the namespace under "Forward-looking namespace handling."
3. **This document gets a new entry** with status `book-committed`, the source extension, the architectural commitment, the minimal surface, and any open questions for the Sunfish implementation.
4. The Sunfish-side mirror at `C:/Projects/Sunfish/docs/specifications/inverted-stack-package-roadmap.md` is updated in the same commit cycle.
5. When Sunfish opens an ADR for the namespace, the ADR ID is recorded here; status advances to `adr-accepted`.
6. When the package directory is created in Sunfish, status advances to `scaffolded`.
7. When the full book-referenced surface ships, status advances to `shipped`, the canonical entry is added to `project_sunfish_packages.md`, and the HTML annotation in the chapter is removed.

## Maintenance

This document is the authoritative roadmap. The Sunfish-side mirror references this document as the source of truth and tracks Sunfish-specific implementation status (ADR ID, package directory existence, build-target hookup, etc.).

If the book and the implementation drift on a namespace's commitment, **the book is authoritative for the architectural commitment** (what the package must own and the minimal surface it must expose). The Sunfish-side mirror is authoritative for **implementation status** (where in the lifecycle the package is). Conflicts are resolved by ADR.
