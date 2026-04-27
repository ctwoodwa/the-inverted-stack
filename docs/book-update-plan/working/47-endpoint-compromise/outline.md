# 47 — Endpoint-Compromise Threat Model — Outline

**ICM stage:** outline → ready for draft.
**Target chapters:** Ch15 (security architecture, Part III) + Appendix B (threat-model worksheets).
**Total word target:** 2,000 words (Ch15 ~1,500; App B ~500).
**Source:** `docs/reference-implementation/design-decisions.md` §5 entry #47 (sub-patterns 47a–47f).
**Why this is fifth in the priority list:** the existing P6 security architecture covers network, relay, and supply-chain threat surfaces. Endpoint compromise is the gap that practitioners notice first and that commercial malware exploits most aggressively. Without an honest statement of what protection lapses when the user's device is fully owned, the book over-claims. The architecture's credibility depends on stating this boundary clearly.

---

## §A. New section in Ch15 — "Endpoint Compromise: What Stays Protected"

**Insertion point:** between the existing `## In-Memory Key Handling` section and the existing `## Supply Chain Security` section. The narrative logic is deliberate: In-Memory Key Handling closes the exposition on what the architecture does to protect key material under normal operating conditions. Endpoint Compromise follows immediately to address what happens when those conditions fail — when the OS itself is adversarial. Supply Chain Security then examines the adjacent attack surface (the build pipeline), completing the adversarial-environment trilogy before the chapter moves into compliance and relay concerns. Inserting here groups the three "what if the perimeter is already inside the wire" sections together.

**Word target:** 1,500 words.

**H2:** `## Endpoint Compromise: What Stays Protected`

### A.1 Why the scope declaration matters (≈200 words)

- P6 (security) makes a strong claim: data is encrypted at rest and in transit, keys never leave the node unencrypted, and the relay sees only ciphertext. That claim holds against a network adversary. It does not hold unchanged against an endpoint adversary.
- The distinction is load-bearing. A user who reads only the P6 summary and concludes that their data is safe even when their phone is running Pegasus has drawn an incorrect inference. The architecture is responsible for making the correct inference available.
- Sub-pattern 47a (explicit scope declaration) is the obligation to name, in the security chapter itself, what protection the architecture provides and what it does not provide when the endpoint is compromised. Not a footnote. Not a disclaimer appended to the conclusion. A dedicated section that a practitioner can reference directly.
- Cross-reference to Ch15 §Threat Model (the master threat taxonomy at the chapter head) — this section adds the endpoint-compromise row to that taxonomy and fills it in.
- Cross-reference to Ch7 §The Security Lens for the council's original challenge on over-claiming security guarantees — this section is the resolution.

### A.2 Sub-pattern 47a — Explicit endpoint-compromise scope declaration (≈200 words)

- A table: what the architecture protects, what it does not protect, and the residual risk, when the endpoint is compromised (OS-level or hardware-level compromise).

| Protected | Not protected | Residual risk |
|---|---|---|
| Other users' data on the relay | Local key material once OS is compromised | Attacker reads plaintext in memory or keystore |
| Other devices in the user's fleet | The local node's cached copy | Attacker reads cached documents |
| Future ciphertext after key rotation | Past ciphertext under current keys | Attacker has the keys; decryption is trivial |
| Transaction integrity (backdate attacks) | The user's current session actions | Attacker impersonates the user going forward |

- The table is the specification. It must appear verbatim in the chapter. It is not decorative — it is the deliverable for sub-pattern 47a.
- The FAILED conditions for this sub-pattern: endpoint compromise can be silently used to impersonate other devices; compromised endpoint can backdate transactions; endpoint compromise scope is undocumented. An architecture that fails any of these conditions has not met the 47a specification.

### A.3 Sub-pattern 47b — HSM and Secure Enclave separation (≈300 words)

- The strongest hardware-level defense: key material that never leaves a tamper-resistant hardware module, even when the host OS is fully compromised. The iPhone Secure Enclave, Google Pixel Titan M, and Windows Pluton are production-deployed examples of this model [cite].
- The architecture's key hierarchy (Ch15 §Key Hierarchy) places the root KEK in the platform's secure enclave when available. An attacker who owns the OS cannot extract the KEK by reading process memory or the keychain — the key exists only inside the enclave and is never presented to the OS in plaintext.
- The protection boundary: enclaves protect key material from OS-level extraction. They do not protect against a user who is coerced into authenticating (the "rubber-hose" boundary). They do not protect against a physical hardware attack on the enclave itself (documented for older SGX generations [cite] — Intel SGX is the cautionary tale here; Secure Enclave and Titan M have a substantially better record). ARM TrustZone offers a comparable model on Arm-class hardware [cite].
- `Sunfish.Kernel.Security` binds key material to the platform's secure enclave API on device classes where an enclave is available. On device classes without a hardware enclave (older Android devices, some Windows devices without Pluton), the package falls back to OS-keystore isolation with explicit documentation that the protection level is lower.
- Deployment guidance: regulated-tier deployments mandate enclave-backed key storage as a deployment requirement. Consumer-tier deployments encourage it. The architecture does not silently degrade — the `Sunfish.Kernel.Security` startup report identifies the key-storage tier in use. Administrators can enforce a minimum tier through the deployment manifest.
- Cross-reference to Ch15 §Key Hierarchy for the DEK/KEK envelope that the enclave protects.

### A.4 Sub-pattern 47c — Attested boot and integrity measurement (≈200 words)

- A compromised endpoint is most dangerous when the compromise is invisible — when the device continues to participate in the sync mesh without the relay or other peers detecting the anomaly. Attested boot addresses this.
- TPM (Trusted Platform Module) and equivalent mechanisms produce a cryptographic proof that the device is running expected, unmodified software at boot time. The attestation is presented to the relay at handshake; the relay validates it against a known-good measurement before admitting the session [cite].
- The architecture integrates attestation at the sync daemon's handshake layer (Ch14 §Sync Daemon Protocol). A device that fails attestation is denied relay admission; it falls back to local operation only. It does not silently contaminate the sync mesh.
- Honest limitation: attestation covers boot-time integrity. It does not cover runtime compromise — a device that boots cleanly and is then compromised in-session is not caught by attestation alone. The residual risk is in-session compromise between attestation events. For high-security deployments, the architecture requires re-attestation at every relay reconnection.
- `Sunfish.Kernel.Security` exposes the attestation surface; the relay-side enforcement is in the relay's handshake policy, not the node package.

### A.5 Sub-pattern 47d — Remote-wipe capability (≈200 words)

- When a device is confirmed lost or compromised, the operator needs to revoke that device's access and, where possible, crypto-shred the local copy of the data. Remote wipe is the operational procedure.
- The architecture's remote-wipe path: the administrator issues a revocation broadcast for the device's node identity (the same mechanism as Ch15 §Collaborator Revocation, applied to a device rather than a person). The broadcast carries a crypto-shred instruction: on receipt, the node overwrites its local key material and database encryption key with random bytes before exit.
- The honest limitation: remote wipe is only as reliable as the device's network reachability at the moment the broadcast fires. A device that is powered off, in airplane mode, or behind a network that blocks the relay cannot receive the wipe instruction until it reconnects. The architecture does not guarantee synchronous destruction — it guarantees destruction upon next reachable sync event, with audit trail confirmation.
- MDM (Mobile Device Management) integration: enterprise deployments that use MDM (Intune, Jamf, Google Workspace MDM) can issue an OS-level wipe order through MDM channels in parallel with the architecture's crypto-shred. The two mechanisms are complementary; MDM catches the "device never reconnects to the relay" case.
- `Sunfish.Kernel.Security` implements the local-side crypto-shred instruction; MDM integration is the deployment layer's responsibility.

### A.6 Sub-pattern 47e — Endpoint-compromise containment (≈200 words)

- The blast radius of an endpoint compromise must be bounded. The FAILED conditions for this primitive state the boundary explicitly: a compromised endpoint cannot impersonate other devices; cannot backdate transactions; cannot access other users' data.
- Three containment mechanisms enforce this:
  - **Per-device keypair isolation.** Each device holds a distinct keypair. Compromise of one device's private key does not compromise other devices in the user's fleet. The sync daemon rejects session tokens signed by a key it does not recognize.
  - **Append-only transaction log.** The CRDT operation log is append-only and each entry is signed by the originating device keypair. Backdating requires a valid signature from the target timestamp's keypair — an attacker who compromises the device today cannot sign operations as if they occurred last week.
  - **Role-scoped access.** A compromised device can access only the data classes and roles it was provisioned to access. It cannot escalate to roles held by other users on the relay. The relay enforces role-level access at every session handshake.
- Cross-reference to Ch15 §Role Attestation Flow for the role-scoping mechanism; Ch14 §Sync Daemon Protocol for the session authentication that enforces device-keypair isolation.

### A.7 Sub-pattern 47f — Honest documentation of post-compromise risk (≈200 words)

- This sub-pattern is not a cryptographic mechanism. It is an architectural commitment to honesty — the chapter must state directly what protection lapses at endpoint compromise, not leave the reader to infer it.
- The lapses, stated directly:
  - Local cached data is readable with the locally-held keys.
  - Future writes from the compromised device are trusted by peers until revocation propagates.
  - A session in progress at compromise time exposes whatever plaintext is in memory to the attacker.
  - Biometric-based authentication on the compromised device cannot be trusted — the attacker controls the authentication flow.
- The architecture does not claim to solve endpoint compromise. It claims to: (1) limit blast radius via containment; (2) provide hardware-backed key protection where available; (3) provide a remote-wipe path; and (4) document the residual risk honestly so practitioners plan against it rather than discover it in an incident post-mortem.
- Contrast to journalist-targeted mobile malware. Pegasus, Predator, and Hermit operate at the level of full OS compromise with zero-click delivery [cite]. Against these, hardware enclave separation is the only control that reliably retains key protection. The architecture is honest: on a fully-Pegasus-compromised device, keys in the OS keychain are accessible; keys in a hardware enclave are not. No software-only architecture can claim otherwise.

### A.8 FAILED conditions and kill trigger (≈100 words)

Drawn directly from design-decisions §5 #47. Specified here for the technical-review stage:

**FAILED conditions:**
- Compromised endpoint can impersonate other devices in the sync mesh.
- Compromised endpoint can backdate transactions in the shared log.
- Endpoint compromise scope is not documented in the deployed architecture's security reference.

**Kill trigger:**
- Any FAILED condition confirmed in technical review triggers escalation to `Sunfish.Kernel.Security` maintainers before the draft advances to prose-review. This primitive has security-boundary implications; a confirmed failure is not a prose-pass defect.

---

## §B. New threat-actor entry in Appendix B — "THREAT-10 Compromised Endpoint"

**Insertion point:** as a new named section appended to `## Section 2 — Actor Taxonomy Template`, immediately after the existing final table row for "Supply chain attacker." The section introduces a named, numbered threat-actor entry format (THREAT-10) that extends the existing actor taxonomy with a structured block for the endpoint-compromise actor. This is the first instance of the numbered THREAT-NN format in the appendix; it establishes the format for future additions (notably THREAT-11 for chain-of-custody extension #9).

**Word target:** 500 words.

**H3:** `### THREAT-10 — Compromised Endpoint`

#### B.1 Actor entry block (≈200 words)

A structured block following the pattern of the existing actor-taxonomy rows, expanded to named fields:

- **Actor name:** Compromised endpoint (device fully owned by attacker).
- **Motivation:** Access to the user's local cached data; impersonation of the user; access to other users' data via the compromised device's credentials.
- **Capability level:** Medium (scripted exploit, consumer spyware) to High (zero-click nation-state malware — Pegasus, Predator, Hermit class). Most real-world endpoint compromises are Medium. Nation-state-class is High and changes the protection calculus for hardware enclaves.
- **Attack surface:** OS keychain, in-memory key material, application database, session tokens, biometric authentication flow.
- **What the architecture protects:** Other devices in the user's fleet; other users' data on the relay; future state after revocation propagates; transaction log integrity (backdate attacks blocked by append-only + device-keypair signing).
- **What the architecture does not protect:** Local cached data that was decryptable before compromise; current session plaintext in memory; keys in OS keychain (non-enclave devices).
- **Residual risk:** Local data exposure scoped to the compromised device's cached copy. On hardware-enclave devices, KEK is protected even under OS compromise. On non-enclave devices, KEK is exposed.

#### B.2 Attack tree — primary branch: mobile device zero-click compromise (≈200 words)

A short attack tree following the Construction PM pattern established in Section 3 of Appendix B:

1. **Attacker delivers zero-click exploit.** No user interaction required. Targets OS messaging stack or browser engine. Device is compromised silently.
2. **Attacker reads OS keychain.** On non-enclave devices: KEK is extracted. All locally-cached ciphertext decryptable. Attack succeeds at data-access goal.
3. **Enclave check.** On enclave-class devices (Secure Enclave, Titan M, Pluton): KEK is inaccessible via OS API. Attacker cannot extract key material. Attack is contained to in-memory plaintext during active session only.
4. **Attacker reads in-memory plaintext.** Whatever the application has decrypted for display is accessible. The re-authentication interval (Ch15 §In-Memory Key Handling) limits the window: key material evicted after four hours narrows exposure.
5. **Attacker attempts relay impersonation.** Uses captured session token to forge writes. Blocked if the token is bound to the device keypair and the relay enforces keypair-session binding. Succeeds if the session token is bearer-only with no keypair binding — an architectural failure.
6. **Operator issues remote-wipe broadcast.** Once the compromise is detected, revocation + crypto-shred instruction propagates. Device evicts key material on next relay connection. If the device is offline (attacker has it offline deliberately), wipe is deferred.

#### B.3 Mitigation summary for practitioners (≈100 words)

- Mandate enclave-backed key storage for any deployment with regulated data or sensitive individual data.
- Enforce re-authentication intervals (four hours consumer; sixty minutes regulated) to limit in-memory exposure.
- Integrate MDM for enterprise deployments; MDM wipe runs in parallel with architecture's crypto-shred.
- Enforce device attestation at relay handshake for high-security deployments.
- Communicate honestly to users: no architecture protects data on a fully-compromised device where the attacker has extracted keys from a non-enclave keychain.

---

## §C. Code-check requirements

Extension #47 extends `Sunfish.Kernel.Security` — no new namespace. Per the sunfish-package-roadmap.md `Future forward-looking namespaces` table entry for #47: "extends `Sunfish.Kernel.Security`."

References the following Sunfish namespaces by name only (per CLAUDE.md Sunfish reference policy — pre-1.0; package names not class APIs):

- `Sunfish.Kernel.Security` — HSM/enclave binding; remote-wipe crypto-shred; device-keypair isolation; attested boot surface.

All references marked `// illustrative — not runnable` per the Sunfish reference policy.

No new namespace is introduced; the code-check report will confirm `Sunfish.Kernel.Security` appears in the Ch15 namespace inventory and is a valid in-canon package.

---

## §D. Technical-review focus

For the @technical-reviewer pass:

- **Apple Secure Enclave:** verify the claim that the KEK never leaves the enclave as plaintext. Source: Apple Platform Security guide [cite]. Cross-check against Ch15 §Key-Loss Recovery biometric-derived key (48d) which references the same enclave — verify the two sections are consistent in how they characterize the enclave's protection model.
- **Google Pixel Titan M:** verify the analogous claim for Android hardware-backed keystore. Source: Google Android security bulletin + Titan chip technical documentation [cite].
- **Windows Pluton:** verify that Pluton, not TPM 2.0 alone, is the relevant control for Windows 11 devices. Pluton integrates directly with the CPU; TPM 2.0 has a bus-sniffing attack surface that Pluton eliminates [cite — Microsoft Pluton announcement + security whitepaper]. Note: not all Windows 11 devices ship with Pluton; the technical review must flag this and ensure the draft acknowledges the TPM 2.0 fallback position.
- **Intel SGX cautionary tale:** SGX has been the subject of multiple academic side-channel attacks (Foreshadow/L1TF [cite], Plundervolt [cite], SGAxe [cite]). The draft must reference these as the reason SGX is cited cautionary — to contrast with Secure Enclave and Titan M's comparatively better record. Do not claim Secure Enclave is immune to all hardware attacks; claim the academic attack record is substantially shorter.
- **ARM TrustZone:** verify TrustZone is the correct reference for Arm-class hardware security. Source: ARM security technology overview [cite].
- **Pegasus, Predator, Hermit:** verify characterizations against published reports. Pegasus: Citizen Lab and Amnesty International forensic reports (2021 [cite]). Predator: Cytrox/Intellexa technical analysis [cite]. Hermit: Google Project Zero + Lookout analysis [cite]. Verify the claim that zero-click delivery to OS messaging or browser stack accurately characterizes these tools' delivery mechanism.
- **TPM attested boot:** verify the claim that the relay validates attestation at handshake against known-good measurements. Ensure this does not conflict with Ch14 §Sync Daemon Protocol's handshake description — if Ch14 does not currently describe attestation validation, flag it as a gap to address with a cross-reference note rather than a silent inconsistency.
- **Citation [7] from extension #48 (Windows Pluton):** the loop-plan notes that Windows Pluton was already cited as [7] in Ch15 from the #48 key-loss-recovery extension. Verify the existing citation number at the time this draft lands and use the same reference rather than adding a duplicate. If [7] covers Apple Platform Security, the Pluton-specific reference may be distinct — confirm before citing.
- **Remote-wipe honest limitation:** verify the claim that MDM wipe (Intune, Jamf, Google MDM) runs in parallel with the architecture's crypto-shred as complementary mechanisms. The technical review must confirm MDM integration is not claimed as part of `Sunfish.Kernel.Security` — it is explicitly the deployment layer's responsibility.

---

## §E. Prose-review focus

For the @prose-reviewer + @style-enforcer pass:

- **Active voice throughout.** "The enclave protects the KEK" — not "the KEK is protected by the enclave." "The relay rejects the session" — not "the session is rejected."
- **Honest about post-compromise risk.** The Pegasus paragraph (§A.7) must not be softened. "No software-only architecture can claim otherwise" is a hard sentence; it must stay hard.
- **No hedging on scope declarations.** The §A.2 table states what is and is not protected. It does not add "generally," "typically," or "in most cases." The scope is the scope.
- **No academic scaffolding.** No "this section presents," "as we have seen," "the author contends."
- **No re-introducing the architecture.** Ch15 assumes Part I is read. The reader knows what a node is, what the relay is, what the DEK/KEK hierarchy is.
- **Paragraph length cap:** 6 sentences.
- **Register check:** Part III specification voice. Not tutorial (that is Part IV). Sentences state what the architecture does; they do not walk the reader through steps.

---

## §F. Voice-check focus (HUMAN STAGE — not autonomous)

For the human voice-pass:

- **Anecdote candidates.** The Pegasus-class threat may feel abstract unless grounded. Anecdote options:
  - A journalist or activist who discovered their device was compromised after the fact — the architecture's honest statement of what a hardware enclave provides versus what it cannot.
  - A work phone lost in a rideshare (common scenario) — illustrates the difference between "they have my data" (non-enclave, bad) and "they have my device but the enclave kept the keys" (hardware-backed, better outcome).
  - A practitioner discovering MDM had not been enforced when a device was lost — illustrates the "remote wipe only works if the device connects" gap.
- **Connective tissue.** The Endpoint Compromise section sits between In-Memory Key Handling and Supply Chain Security. The voice-pass should add one sentence at the close of In-Memory Key Handling that foreshadows the next topic: the controls just described assume the OS is honest; the next section examines what happens when it is not.
- **THREAT-10 in App B:** the attack-tree style (App B Section 3 construction PM pattern) is already established. Voice-pass should confirm the tone matches — practical, numbered, not academic.

---

## §G. Citations

The draft adds these to Ch15's reference list (IEEE numeric, in order of first appearance after existing entries). Exact reference numbers depend on the state of Ch15's reference list when the draft lands — the draft inserts after the last current entry.

Note: Windows Pluton may already be cited as [7] from extension #48 (per loop-plan §D technical-review note). Technical review must confirm; if so, reuse the existing entry number rather than adding a duplicate.

New citations to add:

1. Apple Inc., "Apple Platform Security," May 2024. [Online]. Available: https://support.apple.com/guide/security/welcome/web — for Secure Enclave architecture (47b).

2. Google, "Android Security Bulletin," 2024. [Online]. Available: https://source.android.com/docs/security/bulletin — for Titan M attestation (47b). Supplement with: Google, "Android Keystore system," Android Developers documentation. Available: https://developer.android.com/privacy-and-security/keystore.

3. Microsoft, "Microsoft Pluton security processor," Microsoft Security Blog. Available: https://www.microsoft.com/en-us/security/blog/2020/11/17/meet-the-microsoft-pluton-processor-the-security-chip-designed-for-the-future-of-windows-pcs/ — for Pluton vs. TPM 2.0 bus-sniffing distinction (47b, 47c). [Verify against existing Ch15 citation from #48; may be same entry.]

4. J. Van Bulck et al., "Foreshadow: Extracting the Keys to the Intel SGX Kingdom with Transient Out-of-Order Execution," in *Proc. 27th USENIX Security Symposium*, 2018, pp. 991–1008. — SGX cautionary tale (47b).

5. M. Murdock et al., "Plundervolt: Software-based Fault Injection Attacks against Intel SGX," in *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2020, pp. 1466–1482. — SGX voltage fault (47b).

6. P. Chen et al., "SGAxe: How SGX Fails in Practice," in *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2020. — SGX side channel (47b).

7. Arm Ltd., "Arm Security Technology — Building a Secure System using TrustZone Technology," white paper, Apr. 2009 (updated 2022). [Online]. Available: https://developer.arm.com/documentation/prd29-genc-009492/ — for ARM TrustZone (47b).

8. R. Deibert et al. (Citizen Lab), "Pegasus Project Technical Analysis," Jul. 2021. [Online]. Available: https://citizenlab.ca/2021/07/forensic-methodology-report-how-to-catch-nso-groups-pegasus/ — Pegasus forensic report (47f).

9. Lookout and Google Project Zero (referenced collectively), "Hermit: Enterprise-Grade Android Spyware," 2022. Available: https://blog.lookout.com/lookout-discovers-hermit — Hermit analysis (47f).

App B does not add new citations — it cross-references Ch15's entries.

---

## §H. Cross-references

Inside the new sections:

- Ch15 §Endpoint Compromise → Ch15 §Threat Model (master taxonomy; endpoint-compromise row added here)
- Ch15 §Endpoint Compromise → Ch15 §Key Hierarchy (DEK/KEK envelope; the hierarchy that the enclave protects)
- Ch15 §Endpoint Compromise → Ch15 §Key Compromise Incident Response (compromise response procedure)
- Ch15 §Endpoint Compromise → Ch15 §In-Memory Key Handling (re-authentication interval cited in 47d and 47f)
- Ch15 §Endpoint Compromise → Ch15 §Collaborator Revocation (remote-wipe reuses revocation broadcast mechanism)
- Ch15 §Endpoint Compromise → Ch14 §Sync Daemon Protocol (attested boot at handshake layer)
- Ch15 §Endpoint Compromise → #46 forward-secrecy (post-compromise key rotation closes the forward-access window — forward-secrecy extension is the complement)
- Ch15 §Endpoint Compromise → #45 collaborator revocation (remote-wipe uses the same revocation-broadcast path)
- App B THREAT-10 → Ch15 §Endpoint Compromise (the full specification; App B entry cross-references it)
- App B THREAT-10 → Ch15 §In-Memory Key Handling (re-authentication interval cited in attack tree branch 4)

---

## §I. Subagent prompt for the draft stage

The next iteration (`outline → draft`) will invoke `@chapter-drafter` (Part III specification register) with this prompt:

> Draft two new sections for *The Inverted Stack*: (1) `## Endpoint Compromise: What Stays Protected` for Ch15 (~1,500 words, inserted between the existing `## In-Memory Key Handling` and `## Supply Chain Security` sections); and (2) `### THREAT-10 — Compromised Endpoint` for Appendix B (~500 words, appended to `## Section 2 — Actor Taxonomy Template` after the final existing table row).
>
> Source: outline at `docs/book-update-plan/working/47-endpoint-compromise/outline.md`. Follow the section structure and word targets exactly. Voice: Part III specification register for Ch15 (state what the architecture does; do not walk through steps). App B entry matches the practical, numbered, non-academic tone of Section 3's construction PM attack tree.
>
> Sub-patterns to cover: 47a explicit scope declaration (with the four-row protected/not-protected table), 47b HSM/Secure Enclave separation (Apple Secure Enclave, Pixel Titan M, Windows Pluton; Intel SGX as cautionary tale), 47c attested boot and integrity measurement (TPM; relay handshake validation), 47d remote-wipe capability (honest about offline-device limitation; MDM as complementary layer), 47e endpoint-compromise containment (three mechanisms: per-device keypair isolation, append-only log, role-scoped access), 47f honest documentation of post-compromise risk (Pegasus/Predator/Hermit class; the one sentence about no software-only architecture standing against OS-level key extraction must not be softened). FAILED conditions from §A.8 must appear verbatim in a designated block.
>
> Sunfish references: `Sunfish.Kernel.Security` only — no new namespace (per sunfish-package-roadmap.md entry for #47). No class APIs, no method signatures. Mark any code snippets `// illustrative — not runnable`.
>
> Citations: IEEE numeric. Add the new entries listed in outline §G to Ch15's reference list (continue existing numbering; verify whether Windows Pluton is already cited from extension #48 before adding a duplicate). App B cross-references Ch15 — no new citations in App B.
>
> Cross-references: per outline §H — all must be wired in the draft.
>
> Insertion mechanics: write the Ch15 H2 section directly into `chapters/part-3-reference-architecture/ch15-security-architecture.md` between `## In-Memory Key Handling` and `## Supply Chain Security`. Write the App B H3 section directly into `chapters/appendices/appendix-b-threat-model-worksheets.md` as a new H3 under `## Section 2 — Actor Taxonomy Template`. Preserve all existing H2 anchor structure and H1 frontmatter. Update Ch15's reference list with the new entries.

---

## §J. Quality gate for `outline → draft`

Per loop-plan §5: outline has all section headers and bullet points (sub-patterns 47a–47f each have a designated subsection in §A; App B entry is fully structured in §B); word count target estimated (1,500 Ch15 + 500 App B = 2,000 total — within ±10% of loop-plan §4 #47 target of 2,000 words); subagent prompt prepared (§I above). Gate passes.

---

**Estimated next-iteration duration (draft stage):** 45–70 minutes. The draft is shorter than #48 (key-loss) and #45 (revocation) because the Ch15 section is 1,500 words rather than 2,000 and the App B entry is a structured block rather than a full new section. Schedule next fire 1 hour after this one.
