# 48 — Key-loss Recovery — Outline

**ICM stage:** outline → ready for draft.
**Target chapters:** Ch15 (security architecture, Part III) + Ch20 (UX, Part IV).
**Total word target:** 3000 words (Ch15 ~2000; Ch20 ~1000).
**Source:** `docs/reference-implementation/design-decisions.md` §5 entry #48 (sub-patterns 48a–48f).
**Why this comes first in the priority list:** most common P7 failure mode in real-world local-first deployments. Without it, the P7 ownership promise breaks at the first forgotten password, the first lost device, the first death without succession arrangement.

---

## §A. New section in Ch15 — "Key-Loss Recovery"

**Insertion point:** between the existing `## Key Compromise Incident Response` section and the existing `## Offline Node Revocation and Reconnection` section. The flow is: scheduled rotation → compromise response → user-driven key loss → offline-revocation handshake. Key-loss recovery sits naturally between attacker-driven and operator-driven scenarios.

**Word target:** 2000 words.

**H2:** `## Key-Loss Recovery`

### A.1 Why this matters (≈250 words)

- The P7 ownership property assumes the user retains the keys that decrypt their data. Lose the key, lose the data — that is the architecture's honest boundary, not a defect.
- Real-world failure modes: forgotten master password; lost device with no backup; sudden death or incapacity without succession arrangement; loss of the OS keystore through factory reset; loss of a hardware key through theft or destruction.
- Without a recovery primitive, a single lapse converts the architecture's confidentiality guarantee into permanent data loss.
- A correct recovery primitive cannot lower the bar to entry — recovery that an attacker can also invoke breaks confidentiality. The design space is the narrow corridor where a legitimate user can recover and an adversary cannot.
- Cross-reference to #32 (succession arrangements with executor delegation) and #18 (delegated capability) — recovery is the runtime mechanism; succession and delegation are the upstream policies.

### A.2 The six recovery mechanisms (≈900 words — ~150 each)

Each subsection presents one mechanism with: who it serves, the cryptographic construction in plain language, the threat model (recovery-as-attack-vector), and the deployment cost.

#### A.2.1 Multi-sig social recovery (sub-pattern 48a)

- Construction: 3-of-5 (or 2-of-3) trustees, time-locked. Argent wallet pattern; Vitalik Buterin's 2021 case for social recovery wallets [cite].
- Trustee designation occurs at first-run (not after loss); each trustee holds a fragment of an unwrapping key derived via Shamir secret sharing.
- Threshold construction prevents any single trustee from unilateral access; time-lock period (default 7 days) gives original holder window to dispute.
- Threat model: collusion of *t* trustees defeats the scheme; mitigation is geographic and social diversity in trustee selection.
- Best fit: individuals; small partnerships; not enterprise.

#### A.2.2 Custodian-held backup key (sub-pattern 48b)

- Construction: institutional custodian (lawyer, bank, regulated cloud-custodian) holds a wrapped recovery key under attestation policy.
- Release requires multi-factor identity verification by the custodian — out-of-band channel.
- Threat model: custodian compromise or coercion; mitigation is custodian's own audited security posture; legal liability allocation through contract.
- Best fit: enterprise, regulated industries, estate planning.
- Cross-reference to #32 (executor delegation for succession).

#### A.2.3 Paper-key fallback (sub-pattern 48c)

- Construction: BIP-39-style mnemonic phrase printed at first-run, stored offline (safe, safety-deposit box).
- The printed phrase derives the root seed via Argon2id under the deployment's high-security parameters (memory cost 128 MiB, iterations 4 — same parameters Ch15 §Key Hierarchy specifies for the regulated tier).
- Threat model: physical access to the printed phrase. The architecture is honest: paper keys defeat hibernation/cold-boot attacks but have a physical-security perimeter the user is responsible for.
- Best fit: low-frequency recovery, single-user accounts, deployments where digital escrow is itself a higher risk than physical paper.

#### A.2.4 Biometric-derived secondary key (sub-pattern 48d)

- Construction: a recovery key derived from a biometric template held in the platform's secure enclave (Apple Secure Enclave, Pixel Titan M, Windows Pluton).
- The biometric never leaves the enclave; what leaves is a derived key only on positive match.
- Threat model: coerced biometric (sleeping user, forced presentation), template extraction (rare but documented for some sensors). Mitigation is deployment-specific opt-in only — biometric recovery is not the default in regulated tiers.
- Best fit: consumer; secondary-factor with another mechanism, not standalone.

#### A.2.5 Timed recovery with grace period (sub-pattern 48e)

- Construction: a recovery claim is broadcast to the user's existing devices and to designated trustees (where present). The original holder has 7–30 days to dispute. If undisputed, the recovery completes and the new key takes effect.
- The grace period is not an artifact of network propagation — it is a deliberate friction layer. An attacker who can also wait 30 days and suppress the original holder's notifications has a much harder problem than an attacker who can complete recovery in minutes.
- Threat model: long-game adversary with persistent access to the original user's notification channels (email, SMS); mitigation is multi-channel notification and trustee co-signing on completion.
- Best fit: every deployment that uses any of the prior mechanisms — the grace period is composable, not exclusive.

#### A.2.6 Recovery-event audit trail (sub-pattern 48f)

- Construction: every recovery initiation, dispute, and completion is recorded as a signed event in the same encrypted log used for application data. Records carry the trustee identifiers (where applicable), the claimed identity, the grace-period start and end, and the completion attestation.
- The audit trail is the legal artifact when a recovery is later contested. It is also the architectural defense against silent recovery — a recovery cannot complete without a corresponding event in the log, and any node verifying the log can detect a tampered or missing record.
- Cross-reference to #9 (chain-of-custody) — the same multi-party signed-event mechanism, applied to recovery rather than data transfer.

### A.3 Threat model — recovery as attack vector (≈300 words)

- The cardinal rule: recovery that defeats the legitimate user's threat model defeats confidentiality. The recovery primitive must be at least as hard for an attacker to invoke as the original key custody was to compromise.
- Specific failure modes the architecture defends against:
  - **Trustee compromise.** Mitigated by t-of-n threshold + grace period; defeated only by *t* simultaneous compromises.
  - **Custodian coercion.** Mitigated by attestation policy and out-of-band identity verification; ultimately bounded by custodian's own integrity.
  - **Forged loss claim.** Mitigated by grace period, multi-channel notification to the original holder, and signed audit trail.
  - **Coerced recovery (rubber-hose attack).** Architectural mitigation is limited; deployment guidance is to combine biometric + paper-key + grace period so no single coerced action completes recovery.
- Honest limitation: no recovery primitive defeats a sufficiently patient adversary with control of every recovery channel simultaneously. The architecture bounds the attack cost; it does not eliminate it.

### A.4 Recommended deployment combinations (≈350 words)

A three-row table — one row per deployment class — documenting the recommended combination of mechanisms.

| Deployment class | Primary mechanism | Secondary | Grace period |
|---|---|---|---|
| Consumer | Multi-sig social (3-of-5) | Paper-key offline | 14 days |
| SMB | Custodian-held + 2-of-3 social | Paper-key in safe | 7 days |
| Regulated (HIPAA, PCI, financial) | Custodian-held under attestation | Multi-sig social with named officers | 30 days |

Discussion: each row's tradeoff (recovery friction vs. attack resistance); the regulatory tier's longer grace period reflects audit and dispute requirements; consumer tier optimizes for a smooth recovery the user will not abandon when needed.

### A.5 What this section does not solve (≈200 words)

- A user who refuses to set up any recovery mechanism at first-run and then loses their keys still loses their data. The architecture surfaces the choice; it cannot force the choice.
- A user who designates trustees who are themselves compromised has no recovery from that posture. The architecture cannot grade trustee selection.
- A user whose pre-arrangement is invalid by the time recovery is needed (trustees deceased, custodian out of business, paper-key destroyed in same disaster as the device) has no recovery from that posture either. The architecture surfaces this risk through periodic recovery-readiness audits — described in Ch20 — but the user must act on them.

---

## §B. New section in Ch20 — "Key-Loss Recovery UX"

**Insertion point:** between the existing `## The First-Run Experience` section and the existing `## Accessibility as a Contract` section. First-run is where recovery setup begins; accessibility considerations apply to recovery flows specifically. Inserting between them keeps the chronology of the user's journey visible.

**Word target:** 1000 words.

**H2:** `## Key-Loss Recovery UX`

### B.1 First-run prompt: setting up recovery (≈250 words)

- The first-run experience presents recovery setup as a required step, not an optional one. Skipping it is permitted but requires an explicit acknowledgment that data loss is the consequence.
- The choice screen shows the three primary mechanisms (social, custodian, paper) with tradeoff text — "trust three friends" vs. "trust your bank" vs. "trust a piece of paper in a safe."
- The chosen mechanism's setup flow is inline; the user does not leave the application.
- Cross-reference to Ch20 §The First-Run Experience for the broader onboarding pattern.

### B.2 Trustee designation flow (≈200 words)

- For multi-sig social recovery: a step-by-step flow that walks the user through naming trustees, sending them an out-of-band invitation, and confirming each trustee has accepted.
- The UX surfaces threshold semantics: "3 of 5 must agree before your data can be recovered. Pick 5 people you trust who don't all know each other."
- Trustee acceptance is itself an event in the user's log; the user sees confirmation in real time as each trustee completes acceptance.

### B.3 Recovery initiation UX (≈200 words)

- The user has lost their key and is on a fresh device. The recovery flow begins with identity claim — the user proves they are the rightful holder through whatever channels the original setup designated.
- The grace-period timer is shown immediately: "Your recovery will complete in 14 days unless your existing device disputes."
- The user sees the recovery progress in clear text: trustees who have signed, trustees still pending, the dispute window remaining.

### B.4 Time-locked grace period UX (≈200 words)

- The original holder's existing devices receive a high-priority notification: "Someone is requesting recovery of your account. If this is not you, dispute now."
- Multi-channel: in-app banner, OS push notification, email, SMS where the user opted in.
- The dispute action is one tap. A confirmed dispute halts the recovery; the audit trail records the dispute.
- If the original holder has lost all notification channels (the genuine recovery case), the silence is itself the signal — the grace period elapses and recovery completes.

### B.5 Recovery completion confirmation (≈150 words)

- On grace-period expiry without dispute, the recovery completes. The new device receives the wrapped KEKs for the user's roles; sync resumes; the audit trail records completion.
- The user sees a final screen: "Recovery complete. Your data is being decrypted on this device. Documents will appear as they decrypt — large libraries may take several minutes."
- A periodic recovery-readiness audit reminds users every 12 months: "Verify your trustees are still reachable. Verify your paper-key is still in the safe." The reminder is calibrated; it is not so frequent that users dismiss it.

---

## §C. Code-check requirements

The draft references the following Sunfish namespaces by name only (per CLAUDE.md Sunfish reference policy — pre-1.0; package names not class APIs):

- `Sunfish.Foundation.Recovery` — recovery primitive interfaces (illustrative)
- `Sunfish.Kernel.Security` — already cited in Ch15; recovery hooks live here
- `Sunfish.Kernel.Audit` — recovery-event audit trail entries

All references marked `// illustrative — not runnable` per the Sunfish reference policy.

## §D. Technical-review focus

For the @technical-reviewer pass:

- Verify multi-sig threshold logic (3-of-5 vs. 2-of-3 tradeoff) against Shamir secret-sharing literature.
- Verify the time-lock attack model — is 30 days actually defeasible by a patient adversary with control of all notification channels? Cite the bound honestly.
- Verify Argon2id parameters cited match Ch15 §Key Hierarchy regulated-tier values exactly (memory cost 128 MiB, iteration count 4, parallelism 4).
- Verify Vitalik Buterin 2021 social-recovery citation date and venue.
- Verify Apple Secure Enclave / Pixel Titan M / Windows Pluton claims about biometric template containment.
- Trace every architectural claim back to v13 / v5 source papers OR mark as new architectural commitment surfaced through universal-planning review (per design-decisions §5 #48).

## §E. Prose-review focus

For the @prose-reviewer + @style-enforcer pass:

- Active voice throughout. "The trustee signs the recovery event" — not "the recovery event is signed by the trustee."
- No hedging on recovery guarantees. Replace "recovery may potentially fail if trustees are compromised" with the specific claim — "recovery fails when *t* trustees are simultaneously compromised."
- Honest about limitations. Section §A.5 ("What this section does not solve") is intentionally direct; do not soften it during prose review.
- No academic scaffolding. No "this section presents" or "in what follows."
- No restating Part I architecture — Ch15 already assumes the reader has read Part I.
- Paragraph length cap: 6 sentences.

## §F. Voice-check focus (HUMAN STAGE — not autonomous)

For the human voice-pass:

- Add a personal anecdote about key loss. Candidates: lost crypto-wallet seed; forgotten password manager master-password; family member death without password handoff; lost hardware token. The anecdote sets emotional ground for the reader before the cryptographic construction lands.
- Add the connective tissue between Ch15 §Key-Loss Recovery and Ch20 §Key-Loss Recovery UX — a sentence in each pointing to the other so the reader recognizes the policy/UX pairing.
- Calibrate Sinek register lightly per `feedback_voice_sinek_calibration.md` memory — do not over-mechanize the prose with deliberate-pacing hammering.

## §G. Citations

The draft adds these to Ch15's reference list (IEEE numeric, in order of first appearance after existing [1]–[3]):

- Vitalik Buterin, "Why we need wide adoption of social recovery wallets," *vitalik.ca*, Jan. 2021. [Online]. Available: https://vitalik.ca/general/2021/01/11/recovery.html
- Argent, "Argent Smart Wallet Specification," *github.com/argentlabs*, 2020. [Online]. Available: https://github.com/argentlabs/argent-contracts/blob/develop/specifications/specifications.pdf
- A. Shamir, "How to share a secret," *Communications of the ACM*, vol. 22, no. 11, pp. 612–613, Nov. 1979.
- Apple Inc., "Apple Platform Security," May 2024. [Online]. Available: https://support.apple.com/guide/security/welcome/web — for Secure Enclave architecture.

Ch20 cross-references the Ch15 source list — no new citations.

## §H. Cross-references to add

Inside the new sections:

- Ch15 §Key-Loss Recovery → Ch15 §Key Hierarchy (DEK/KEK envelope explained)
- Ch15 §Key-Loss Recovery → Ch15 §Key Compromise Incident Response (rotation as upstream mechanism)
- Ch15 §Key-Loss Recovery → #32 (succession; future Volume 2)
- Ch15 §Key-Loss Recovery → #18 (delegated capability; existing in catalog)
- Ch15 §Key-Loss Recovery → #9 (chain-of-custody; sibling Volume 1 extension; same audit-trail mechanism)
- Ch20 §Key-Loss Recovery UX → Ch15 §Key-Loss Recovery (the policy this UX surfaces)
- Ch20 §Key-Loss Recovery UX → Ch20 §The First-Run Experience (the broader onboarding pattern)
- Ch20 §Key-Loss Recovery UX → Ch20 §Designing for Failure Modes (key loss is one such failure mode)

## §I. Subagent prompt for the draft stage

The next iteration (`outline → draft`) will invoke `@chapter-drafter` with this prompt:

> Draft two new sections for *The Inverted Stack*: (1) `## Key-Loss Recovery` for Ch15 (~2000 words, inserted between the existing `## Key Compromise Incident Response` and `## Offline Node Revocation and Reconnection` sections); and (2) `## Key-Loss Recovery UX` for Ch20 (~1000 words, inserted between the existing `## The First-Run Experience` and `## Accessibility as a Contract` sections).
>
> Source: outline at `docs/book-update-plan/working/48-key-loss-recovery/outline.md`. Follow the section structure and word targets exactly. Voice: Part III specification register for Ch15; Part IV tutorial register for Ch20. Active voice throughout. No hedging. No academic scaffolding. No re-introducing the architecture (Ch15 assumes Part I + earlier Ch15 sections; Ch20 assumes Part I and Ch15).
>
> Sunfish references: package names only (`Sunfish.Foundation.Recovery`, `Sunfish.Kernel.Security`, `Sunfish.Kernel.Audit`) — no class APIs, no method signatures. Mark code snippets `// illustrative — not runnable` if any are needed.
>
> Citations: IEEE numeric. Add the four sources listed in outline §G to Ch15's reference list (continue the existing `[1]`, `[2]`, `[3]` numbering). Ch20 cross-references Ch15 — no new citations needed in Ch20.
>
> Cross-references: per outline §H — the draft must wire all of them.
>
> Insertion mechanics: write the new H2 sections directly into the existing chapter files at the specified insertion points. Preserve existing H2 anchor structure and H1 frontmatter. Update Ch15's reference list with the four new entries.

## §J. Quality gate for `outline → draft`

Per loop-plan §5: outline has all section headers + bullet points (✓ §A and §B above); word count target estimated (✓ 2000 + 1000 = 3000); subagent prompt prepared (✓ §I above). Gate passes.

---

**Estimated next-iteration duration (draft stage):** 60–90 minutes. Largest single iteration in this extension. Schedule next fire 1–2 hours after this one to allow context-cache cooldown and human-review window.
