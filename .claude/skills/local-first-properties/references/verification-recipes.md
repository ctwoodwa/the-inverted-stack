# Verification Recipes for Local-First Property Conformance

This file gives the agent concrete recipes for the verification step of each foundational concept in `concept-index-by-property.yaml`. The catalog's `verification` field tells you WHAT to check; this file tells you HOW.

## General principles

1. **Static first, dynamic only when necessary.** Most checks can be answered by reading source code, configs, manifests, and test names — without running the target repo. Only suggest a runtime check when static evidence is genuinely insufficient.
2. **Look for the contract, not the implementation.** A repo can satisfy a concept with a different implementation than the book describes — what matters is whether the contract holds. If the catalog says "schema migrations must be idempotent and replay-safe" and the repo uses event-sourcing with deterministic projections, that satisfies the contract even if it doesn't have a `Migration` class.
3. **Evidence > absence of evidence.** If you can't find evidence in 60 seconds of grep, log it as `partial` ("evidence inconclusive — checked X, Y, Z; consider asking the maintainer") rather than `missing`. Save `missing` for cases where you affirmatively confirmed the absence.
4. **Cite the file and line.** Every `complete` and `partial` finding should include a file path (and line if helpful). This is how the user verifies your work and how re-runs detect regressions.

## Recipe by verification type

### Type 1: File or namespace presence

**Catalog says:** "Sunfish.Kernel.Sync namespace exists with at least one type"
or "/packages/foundation/ contains the kernel"

**Recipe:**
1. Glob for path patterns (e.g., `**/Sync/*.cs`, `**/foundation/**`).
2. For namespace checks: Grep for `namespace <name>` declarations or `package <name>` imports.
3. Confirm at least one type/class/function inside (not just an empty folder or a stub file).
4. Cite the file path(s) found.

**False positive watch:** A namespace can exist for one purpose (e.g., `MyApp.Sync` for HTTP polling) and not satisfy a local-first sync concept. Read the implementation to confirm semantics, not just the name.

### Type 2: Behavioral / semantic check

**Catalog says:** "Disconnect network; application performs all core operations identically"
or "Multi-peer convergence test demonstrates byte-identical state after partition heal"

**Recipe:**
1. Look for offline tests, partition tests, or network-disconnection scenarios in the test directory. Glob: `**/*offline*`, `**/*partition*`, `**/*disconnect*`, `**/*convergence*`.
2. Look for code that handles network errors as "queue locally and retry" vs. "show error to user." Grep for the patterns that distinguish these.
3. Look for documentation that describes offline behavior — README sections like "Offline mode," "Network requirements," etc.
4. If the repo has CI runs for these tests, look for a workflow file referencing them.

**Mark as `complete`** if a dedicated test exists AND it asserts the exact behavior the concept names.
**Mark as `partial`** if some offline handling exists but no test covers the specific scenario.
**Mark as `missing`** if there's no offline path at all (the app calls the network synchronously on every action).

### Type 3: Integration test presence

**Catalog says:** "Integration test under accelerators/anchor/tests covers multi-peer convergence"

**Recipe:**
1. Glob for test files in the canonical test location for the repo's stack.
2. Grep test names for the scenario name (e.g., `convergence`, `merge`, `concurrent_edit`, `sync_after_partition`).
3. Read the test setup — does it actually spin up multiple peers, or just call a function with mocked inputs?
4. Cite the test file + test name.

**False positive watch:** A test named `test_convergence` might only call `merge(a, b) == merge(b, a)` (a unit test of the merge function), not actually test two peers converging. Read the test body to be sure.

### Type 4: Configuration or contract presence

**Catalog says:** "Manifest declares per-record CRDT tier (AP / CP / ledger)"

**Recipe:**
1. Find the manifest, schema, or contract files (e.g., `*.json`, `*.yaml`, `*.toml` configs; or `interface ICrdtEngine` declarations).
2. Read for the specific field or contract the catalog names.
3. If the contract is implicit in code (no separate manifest), grep for the equivalent declaration.

**Mark as `complete`** if the contract is explicit and used.
**Mark as `partial`** if the contract exists but is unused or only one example uses it.

### Type 5: Documentation / ADR presence

**Catalog says:** "ADR exists naming the chosen consensus protocol and its quorum semantics"

**Recipe:**
1. Glob for ADR locations: `docs/adr/`, `docs/decisions/`, `architecture/decisions/`, `**/ADR-*`.
2. Grep ADR titles for the topic (e.g., `consensus`, `quorum`, `flease`, `paxos`, `raft`).
3. Read the ADR — does it actually decide and justify, or is it a stub?

**Mark as `complete`** if a real ADR with reasoning exists.
**Mark as `partial`** if there's a stub or a code comment but no full ADR.
**Mark as `missing`** if the decision was made implicitly with no documentation.

### Type 6: Behavioral check via running tests

**Catalog says:** "CRDT properties (commutativity, associativity, idempotency) hold for all CRDT types under property-based test"

**Recipe:**
1. Look for property-based test frameworks in the repo's deps: `fast-check` (JS/TS), `FsCheck` (.NET), `hypothesis` (Python), `proptest` (Rust), `Quickcheck` (Haskell), etc.
2. Look for property tests that name the algebraic properties.
3. **Do not run the tests yourself** — note that the property tests exist and the user should run them as part of CI verification.

### Type 7: Negative check ("the relay sees only ciphertext")

**Catalog says:** "Relay never decrypts payload; relay logs contain no plaintext key material"

**Recipe:**
1. Read the relay's source (if open) or its API contract (if hosted).
2. Look for any code path that calls `decrypt(payload)` on the relay side. There should be NONE.
3. Grep for log statements that emit payload contents — these should not exist on the relay.
4. Check if the relay's data model stores only ciphertext (look at the storage schema, not the in-memory types).

**Mark as `complete`** if you can affirmatively show the relay has no decryption path AND no plaintext logging.
**Mark as `partial`** if the design intent is right but the implementation has gaps (e.g., debug logs that include payloads under a flag).
**Mark as `missing`** if the relay can decrypt or log plaintext.

## When to ask the user vs. mark as gap

If a concept is genuinely ambiguous and reading more code won't resolve it, ask ONE focused question:

> "Concept `<chapter:id>` requires <X>. I see <evidence Y> but it's unclear whether <specific question>. Do you want me to mark this `partial` and continue, or pause for you to point me at the right file?"

Don't ask a question for every ambiguous concept — that turns the report into an interview. Mark genuinely-ambiguous ones as `partial` with a clear note about what evidence is missing, and only escalate the 2-3 most material ones.

## Output line format

Each finding in the report uses this exact format:

```
- `<chapter:id>` — <name>: <status icon> <evidence summary>
```

Status icons: `✓` complete · `~` partial · `✗` missing · `—` not applicable

Example:
```
- `ch12-crdt-engine-data-layer:CRDT-02` — CRDT algebraic properties: ✓ FsCheck property tests at `tests/Sunfish.Tests/Crdt/AlgebraicProperties.cs:23-78` cover commutativity, associativity, idempotency for Map, List, Text, Counter
- `ch12-crdt-engine-data-layer:CRDT-13` — Monotonic CRDT growth: ~ Growth observed in `Sunfish.Kernel.CrdtStore.cs:Apply()`, but no test asserts unbounded growth is bounded by GC. Suggested remediation: add a fuzzing test that runs N=10,000 ops and asserts `store.size < O(N * log N)` after periodic GC.
- `ch15-security-architecture:KEY-04` — Argon2id parameters: ✗ no Argon2id usage found; SQLCipher key is derived via PBKDF2 in `Sunfish.Foundation.LocalFirst.KeyDerivation.cs:31`. Suggested remediation: switch to Argon2id with named parameters per the catalog (memory ≥ 64 MiB, iterations ≥ 3, parallelism ≥ 1) — this is a known weakness for offline brute-force.
```

Consistent format makes diff-based re-run analysis trivial.
