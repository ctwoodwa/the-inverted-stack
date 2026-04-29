# Prose-review report — #46 Forward Secrecy and Post-Compromise Security

**Iteration:** iter-0020 (prose-review)
**Date:** 2026-04-28
**Stage advance:** technical-review → prose-review
**Verdict:** PASS — light revision applied; ready for voice-check

---

## Scope

§Forward Secrecy and Post-Compromise Security in `chapters/part-3-reference-architecture/ch15-security-architecture.md` (lines 403-474, ~1,480 words).

Out of scope and not touched:
- §Endpoint Compromise (#47, immediately following)
- §Collaborator Revocation (preceding)
- Refs [14]–[19] in the reference list (unchanged content; not re-edited in this pass)
- The CLAIM marker at §46e line 461 (OTR/PCS attribution) — preserved verbatim per loop-plan §5

---

## Voice register confirmation

Part III specification voice — "what it is, how it works fully." Confirmed:

- Section opens with WHY the section exists (the question key hierarchy is silent on), not what it describes.
- Active voice predominates ("the symmetric ratchet advances on every message," "the relay forwards ciphertext," "the recipient unwraps the sealed identity").
- Specification framing throughout — names commitments and constructions, no tutorial "you should" framing.
- No re-introduction of local-node architecture.
- No academic scaffolding ("as we have seen," "this paper argues") — none found.
- Cross-references resolve to canonical section names; internal extension numbers (#47, #48) removed where they leaked into reader-facing prose.

---

## Edits applied

### 1. Synonym cycling — "long-lived envelope" → "long-lived session key"

**Line 415.** The phrase "captures a session key under the long-lived envelope" cycled terminology — "envelope" appears nowhere else in §46. The "long-lived" attribute belongs to the session key itself (the very property §46a removes). Rewrote to attach the modifier directly to the named concept.

```
- A relay observer who captures a session key under the long-lived envelope
+ A relay observer who captures a long-lived session key
  decrypts every event encrypted under that key.
```

### 2. Active voice — "a peer that is currently offline" → "a currently offline peer"

**Line 433.** Minor passive construction with redundant relative clause. Tightened to compact adjective form.

```
- a node coming online can begin a session with a peer that is currently offline.
+ a node coming online can begin a session with a currently offline peer.
```

### 3. Active voice — "that variant is deferred" → "this book defers that variant"

**Line 455.** Agentless passive where the agent (the architecture / the book itself) is well-defined. Reattributed.

```
- that variant is deferred to a future volume.
+ this book defers that variant to a future volume.
```

### 4. Internal-numbering leakage and "is one trigger" framing

**Line 443.** Two issues in one paragraph:

- `(cross-reference to #47, §Endpoint Compromise: What Stays Protected)` exposed the ICM-pipeline extension number `#47` alongside the canonical section name. Reader-facing prose should use the section name only; `#47` is internal authoring scaffolding.
- The closer sentence began "Collaborator revocation ... is one trigger," which read as if introducing a third trigger after the paragraph already named two (suspected compromise, scheduled cadence). Collaborator revocation is a sub-case of the suspected-compromise / policy-driven path. Recast as "behaves the same way" to make the sub-case relationship explicit.
- Also tightened a passive participle clause: "Peers receiving the new public key advance their own DH ratchet on receipt" → "Peers advance their own DH ratchet on receipt of the new public key" (active subject-verb-object).

```
- When endpoint-compromise detection fires (cross-reference to #47, §Endpoint Compromise: What Stays Protected),
+ When endpoint-compromise detection fires (cross-reference to §Endpoint Compromise: What Stays Protected),

- Peers receiving the new public key advance their own DH ratchet on receipt.
+ Peers advance their own DH ratchet on receipt of the new public key.

- Collaborator revocation (...) is one trigger: a revocation event forces a ratchet advance for every remaining session, ensuring the revoked party's last-known ratchet state cannot decrypt subsequent messages.
+ Collaborator revocation (...) behaves the same way: a revocation event forces a ratchet advance for every remaining session, so the revoked party's last-known ratchet state cannot decrypt subsequent messages.
```

The `ensuring [X]` superficial -ing tail-phrase (anti-ai-tells §3) became an explicit `so [X]` causal — keeping the consequence visible without the puffy participle.

### 5. Internal-numbering leakage — `#48`

**Line 464.** `Cross-reference to §Key-Loss Recovery for the interaction with #48 — recovery reconstitutes...` exposed extension number `#48` (forward dependency on the key-loss-recovery item) inside reader-facing prose. The §Key-Loss Recovery section name is already present; `#48` was redundant authoring scaffolding. Removed.

```
- Cross-reference to §Key-Loss Recovery for the interaction with #48 — recovery reconstitutes KEK custody...
+ Cross-reference to §Key-Loss Recovery for the recovery interaction: recovery reconstitutes KEK custody...
```

---

## Edits considered but not applied

### A. Paragraph at line 443 lands at 6 sentences

**Held.** After edit 4 above, the paragraph still has six sentences, but each carries distinct content (paragraph topic sentence + two-trigger setup + first-trigger mechanism + key publication + peer behavior + collaborator-revocation sub-case). Splitting would lose the parallel structure between "first trigger" and the sub-case. The 6-sentence cap is a flag, not a hard limit; this paragraph earns the length.

### B. Paragraph at line 464 lands at 6 sentences

**Held.** Same reasoning. The paragraph contains the section's testability anchor (sentence 1), two parallel conformance-test definitions (sentences 2–3), the test-suite location (4), the cryptographic-property qualifier (5), and the recovery-interaction cross-reference (6). Each sentence carries unique architectural content; collapsing or splitting would damage the spec voice.

### C. `is zeroed after use` (line 419)

**Held.** Passive construction, but `Sunfish.Kernel.Security` is named as the agent in the very next paragraph (line 421: "owns the HKDF derivation and the per-message zeroing"). The line-419 passive reads as a property claim, not actor suppression. Cryptographic specification convention.

### D. `is AES-256-GCM encrypted under a DEK that persists until explicitly rotated` (line 423)

**Held.** Passive but conventional. `explicitly rotated` carries the load-bearing modifier "explicit" (rotation is not implicit/automatic) — rewriting would lose that.

### E. `which happens naturally as they communicate` (line 431)

**Held.** "Naturally" reads as a soft hedge but is doing specific work — it distinguishes the progressive DH-ratchet advance through normal traffic from the operator-triggered path defined in §46c. Removing it would obscure the distinction.

### F. CLAIM marker on line 461

**Preserved verbatim.** Per loop-plan §5 and the technical-review report, the OTR/PCS attribution marker is queued for the next technical-review pass. Prose-review does not touch it.

### G. `The honest boundary:` idiom (line 423)

**Held.** Recurring book device used elsewhere in Ch15 and across Part III. On-voice.

### H. `The architectural commitment is the two properties — forward secrecy and post-compromise security — not the specific construction` (line 437)

**Held.** Strong em-dash apposition, on-voice. Em-dash use is explicitly preserved per the anti-ai-tells calibration (§Calibrations).

---

## Anti-AI-tells scan results

Scanned for the high-frequency patterns from `.claude/skills/anti-ai-tells/SKILL.md`:

| Pattern | Found | Disposition |
|---|---|---|
| §1 Significance / legacy puffery | "all inherited the discipline" (line 461) | Held — earned punch line, not vague legacy puffery; ties to a specific list (Signal, MLS, Noise). |
| §3 Superficial -ing tail-phrases | `ensuring the revoked party's last-known ratchet state cannot decrypt` (line 443) | **Fixed in edit 4** — replaced with explicit `so` causal. Other -ing tails (`allowing one party to initiate` line 433, `matching the KEK rotation cadence` line 445, `resetting the symmetric ratchet from a new entropy source` line 429) are load-bearing — each carries a specific architectural claim, not vague consequence. Held. |
| §7 AI-vocabulary cluster | None — no `delve, showcase, tapestry, interplay, intricate, vibrant, enduring, additionally` cluster. `crucial`/`key` not used as soft emphasis. | Clean. |
| §8 Copula avoidance | None — the section uses plain `is`/`are`/`has` throughout (e.g., "Forward secrecy is the property that..."). No `serves as a`, `stands as a`, `represents a`. | Clean. |
| §9 Negative parallelisms | None — no `not only X but also Y` or `it's not just X, it's Y` patterns. | Clean. |
| §16 Inline-header vertical lists | FAILED-conditions bullets (line 470–472) use `**Header.**` format. | Held — this is the chapter's recurring FAILED-conditions reference list, used for every primitive in Ch15. Genuine reference structure, not paragraph-prose disguised as bullets. |
| §17 Title case in headings | All H3 sub-pattern headings use sentence case (`Sub-pattern 46a — Per-message ephemeral key derivation`). | Clean. |
| §27 Persuasive authority tropes | None — no `the real question is`, `at its core`, `fundamentally`, `what really matters`. | Clean. |
| §28 Signposting | None — no `let's dive into`, `let's explore`, `here's what you need to know`. | Clean. |
| §29 Fragmented headers | Each H3 is followed by substantive prose, not a one-line restatement. | Clean. |

There-is constructions: scanned. None in the section.

---

## Paragraph-length audit

| Para starting | Sentences | Status |
|---|---|---|
| "Collaborator revocation closed..." (407) | 4 | OK |
| "Forward secrecy is the property..." (409) | 6 | At cap; clean parallel definitions. OK. |
| "This section adds the session-key..." (411) | 2 | OK |
| "The key hierarchy uses long-lived KEKs..." (415) | 4 | OK |
| "Per-message ephemeral key derivation..." (417) | 3 | OK |
| "The construction begins at session..." (419) | 4 | OK |
| "This is the symmetric input path..." (421) | 3 | OK |
| "The honest boundary:..." (423) | 4 | OK |
| "Per-message ephemeral keys prevent..." (427) | 2 | OK |
| "The Double Ratchet combines..." (429) | 3 | OK |
| "Forward secrecy comes from..." (431) | 4 | OK |
| "Session establishment uses..." (433) | 3 | OK |
| "The Noise framework..." (435) | 5 | OK |
| "`Sunfish.Kernel.Sync` extends..." (437) | 3 | OK |
| "Post-compromise security through..." (441) | 3 | OK |
| "Two triggers advance..." (443) | 6 | At cap after edit 4; each sentence carries distinct content. OK. |
| "The second trigger is scheduled..." (445) | 2 | OK |
| "`Sunfish.Kernel.Security` exposes..." (447) | 3 | OK |
| "The relay forwards ciphertext..." (451) | 4 | OK |
| "Sealed sender hides..." (453) | 4 | OK |
| "The construction creates..." (455) | 4 | OK |
| "Sealed sender is opt-in..." (457) | 4 | OK |
| "The preceding sub-patterns..." (461) | 3 (CLAIM marker preserved) | OK |
| "Naming the commitment..." (464) | 6 | At cap; each sentence is load-bearing. OK. |
| "The forward secrecy and post-compromise..." (468) | 2 | OK |
| FAILED-conditions bullets (470–472) | reference list | OK |
| "The kill trigger..." (474) | 2 | OK |

No paragraph exceeds the 6-sentence cap.

---

## CLAIM markers preserved

One CLAIM marker preserved verbatim at line 461 (end of §46e opening paragraph), per loop-plan §5 and the technical-review report:

```
<!-- CLAIM: OTR 2004 [19] named forward secrecy explicitly; "post-compromise
security" as a named property post-dates OTR (PCS terminology is generally
attributed to Cohn-Gordon, Cremers, Garratt c. 2016). The phrase "these
properties" therefore overcredits OTR for both. Defer to next-pass copy-edit
(precision tightening, not architectural change). -->
```

---

## Overall assessment

- **Tone:** on-voice. Section reads as Part III specification — what the protocol commits to and how each commitment manifests as a testable property. No tutorial intrusion, no academic scaffolding.
- **Estimated revision time:** light. Five surgical edits applied; no structural rewrites needed.
- **Top 3 priorities (resolved in this pass):**
  1. Internal extension-number leakage (`#47`, `#48`) into reader-facing prose — fixed.
  2. Synonym cycling on `long-lived envelope` — fixed by anchoring to `long-lived session key`.
  3. Sub-case framing in §46c second paragraph (`is one trigger` → `behaves the same way`) — fixed.

---

## Gate decision

**prose-review → voice-check: ADVANCE.**

Quality gate per loop-plan §5: paragraph-length cap satisfied (≤6 sentences); active voice predominates; no academic scaffolding; one CLAIM marker preserved (≤2 budget); Sunfish package references intact (`Sunfish.Kernel.Security`, `Sunfish.Kernel.Sync`); cross-references resolve; refs [14]–[19] untouched; §Endpoint Compromise and §Collaborator Revocation untouched.

The §Forward Secrecy and Post-Compromise Security section is ready for voice-check at iter-0021.
