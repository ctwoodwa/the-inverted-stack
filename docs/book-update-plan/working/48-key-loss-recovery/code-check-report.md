# Code-check report — 48 key-loss recovery

**Stage:** code-check (ICM stage 3).
**Run:** iter-0003, 2026-04-26.
**Verdict:** PASS.

---

## Scope

Two new sections were drafted and inserted in iter-0002:

- `chapters/part-3-reference-architecture/ch15-security-architecture.md` §"Key-Loss Recovery" (~2,050 words)
- `chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md` §"Key-Loss Recovery UX" (~1,040 words)

Code-check verifies: Sunfish package references against the canonical Sunfish package list, no class APIs / method signatures appear in prose, no code snippets need `// illustrative` markers, no `<!-- TBD -->` / placeholder markers remain.

---

## Sunfish package references in the new sections

| Namespace | Sites | Canon status |
|---|---|---|
| `Sunfish.Foundation.Recovery` | 7 (Ch15: 5; Ch20: 2) | **Forward-looking.** Not in current canon. Volume 1 extension roadmap. |
| `Sunfish.Kernel.Security` | 2 (Ch15: 1; Ch20: 1) | **Valid.** In `project_sunfish_packages.md` canon. |
| `Sunfish.Kernel.Audit` | 2 (Ch15: 1; Ch20: 1) | **Forward-looking.** Not in current canon. Volume 1 extension roadmap. |

All references are package-name-only. No class names. No method signatures. No constructor parameters.

## Forward-looking namespace handling

Per the outline §C requirement ("Reference Sunfish.Foundation.Recovery.* namespaces by name only; mark as illustrative") and the loop-plan §5 quality gate ("All Sunfish package references validated as real; code snippets marked illustrative"), the two forward-looking namespaces were annotated:

- Ch15 §Key-Loss Recovery: HTML-comment annotation at section start naming the two forward-looking namespaces and the one canon namespace.
- Ch20 §Key-Loss Recovery UX: identical HTML-comment annotation at section start.

The annotations are reviewer-visible (HTML comments) and reader-invisible (no prose intrusion). They satisfy the "mark as illustrative" requirement for forward-looking package references in prose. When Sunfish ships the recovery and audit subsystems, the annotations can be removed and the canon updated; the annotations themselves are pre-1.0 footnotes, not permanent architectural commentary.

## Code snippets

No fenced code blocks present in either new section. No `// illustrative` markers required. The existing Mermaid diagram in Ch15 (§Key Hierarchy, lines 56–71) is unchanged and outside the new section.

## Markers and placeholders

| Marker type | Result |
|---|---|
| `<!-- TBD -->` | None found. |
| `TODO` | None found. |
| `expand here` | None found. |
| `placeholder` | None found. |
| `<!-- CLAIM: -->` | One present in Ch15 §"Biometric-derived secondary key" — biometric-template non-exportability claim across Apple Secure Enclave / Pixel Titan M / Windows Pluton. **Intentional**; flagged for technical-review (next stage), not code-check. |

## Cross-reference integrity

Cross-references introduced by iter-0002:

- Ch15 §Key-Loss Recovery → Ch15 §Key Hierarchy (Argon2id parameters) — target exists; verified at line 75 of Ch15.
- Ch15 §Key-Loss Recovery → Ch15 §Key Compromise Incident Response — target exists; verified at line 99 of Ch15.
- Ch15 §Key-Loss Recovery → Ch15 §GDPR Article 17 and Crypto-Shredding — target exists; verified.
- Ch15 §Key-Loss Recovery → primitives #32, #18, #9 — these are entries in `docs/reference-implementation/design-decisions.md` §5; cross-references are appropriate for forward-looking sub-pattern references in book prose.
- Ch20 §Key-Loss Recovery UX → Ch15 §Key-Loss Recovery — newly-added section in same commit; cross-reference target exists.
- Ch20 §Key-Loss Recovery UX → Ch20 §The First-Run Experience — target exists at line 151 of Ch20.
- Ch20 §Key-Loss Recovery UX → Ch15 §Key Hierarchy — target exists; verified.

## Quality gate — code-check → technical-review

Per loop-plan §5:

- [x] All Sunfish package references validated — three classified, two annotated as forward-looking, one verified in canon.
- [x] Code snippets marked illustrative — no code snippets present; nothing to mark.
- [x] No `<!-- TBD -->` markers — verified.

Gate **passed**. Advance to technical-review.

---

## Findings logged for technical-review (next stage)

The technical-review stage handles substantive accuracy. The following items are queued for that pass:

1. The `<!-- CLAIM: ... -->` marker in Ch15 §Biometric-derived secondary key — verify Apple Secure Enclave, Pixel Titan M, and Windows Pluton biometric-template non-exportability against vendor documentation [7].
2. Verify Shamir threshold logic statements (3-of-5 vs. 2-of-3 tradeoff) against secret-sharing literature [6].
3. Verify Argon2id parameter values in §Paper-key fallback match the regulated-tier values stated in Ch15 §Key Hierarchy (memory cost 128 MiB, iteration count 4, parallelism 4).
4. Verify the four new IEEE citations [4]–[7] for date, venue, and URL stability.
5. Check that the threat-model claims (trustee compromise, custodian coercion, forged loss claim, coerced recovery) are honestly bounded and do not over-claim defense.
