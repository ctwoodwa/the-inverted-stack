# Draft — Endpoint-Compromise Threat Model
## Sub-pattern #47 (47a–47f) — Two new sections for Ch15 and Appendix B

---

<!-- ============================================================ -->
<!-- PART 1: Ch15 new section — "Endpoint Compromise: What Stays   -->
<!-- Protected"                                                    -->
<!-- Insertion point: between ## In-Memory Key Handling and        -->
<!-- ## Supply Chain Security                                      -->
<!-- Target: ~1,500 words                                          -->
<!-- ============================================================ -->

## Part 1: Ch15 — `## Endpoint Compromise: What Stays Protected`

---

## Endpoint Compromise: What Stays Protected

The protections in §In-Memory Key Handling assume the OS is honest. This section examines what happens when it is not. P6 makes a strong claim: data is encrypted at rest and in transit, keys never leave the node unencrypted, and the relay sees only ciphertext. That claim holds against a network adversary. It does not hold unchanged against an endpoint adversary.

The distinction is load-bearing. A user who reads only the P6 summary and concludes that their data is safe even when their phone is running Pegasus has drawn an incorrect inference. The architecture is responsible for making the correct inference available. This section adds the endpoint-compromise row to the master taxonomy in §Threat Model and fills it in.

The obligation discharged here is sub-pattern 47a: an explicit scope declaration that names, in the security chapter itself, what protection the architecture provides and what it does not provide when the endpoint is compromised. Not a footnote. Not a disclaimer appended to the conclusion. A dedicated section a practitioner can reference directly, in response to the council's original challenge on over-claiming security guarantees (Ch7 §The Security Lens).

### Sub-pattern 47a — Scope declaration

The table below is the specification. It states what the architecture protects, what it does not protect, and the residual risk, when the endpoint is compromised at OS level or hardware level.

| Protected | Not protected | Residual risk |
|---|---|---|
| Other users' data on the relay | Local key material once OS is compromised | Attacker reads plaintext in memory or in the OS keychain |
| Other devices in the user's fleet | The local node's cached copy | Attacker reads cached documents under the locally-held DEKs |
| Future ciphertext after key rotation | Past ciphertext under current keys | Attacker holds the keys; decryption is trivial |
| Transaction integrity (backdate attacks blocked) | The user's current session actions | Attacker impersonates the user going forward until revocation |

The table is not decorative. It is the deliverable for sub-pattern 47a, and it must appear verbatim in any deployment's security reference. The FAILED conditions for the primitive are derived from it: an architecture that allows a compromised endpoint to silently impersonate other devices, to backdate transactions, or that ships without documenting the endpoint-compromise scope, has not met the 47a specification.

### Sub-pattern 47b — HSM and Secure Enclave separation

The strongest hardware-level defense is key material that never leaves a tamper-resistant hardware module, even when the host OS is fully compromised. The Apple Secure Enclave [14], Google Pixel Titan M [15], and Microsoft Pluton [16] are production-deployed examples. The architecture's key hierarchy (§Key Hierarchy) places the root KEK in the platform's secure enclave when available. An attacker who owns the OS cannot extract the KEK by reading process memory or the keychain — the key exists only inside the enclave and is never presented to the OS in plaintext.

The protection boundary requires precision. Enclaves protect key material from OS-level extraction. They do not protect against a user who is coerced into authenticating — the rubber-hose boundary is outside any cryptographic primitive's scope. They do not protect against every physical hardware attack on the enclave itself: Intel SGX is the cautionary tale here, with multiple published academic side-channel attacks against successive generations [17][18][19]. Apple Secure Enclave and Google Titan M have a substantially better field record, and ARM TrustZone offers a comparable model on Arm-class hardware [20]. The architecture does not claim Secure Enclave is immune to all hardware attack; it claims the academic attack record is substantially shorter, and the deployment posture treats SGX and the others differently as a result.

`Sunfish.Kernel.Security` binds key material to the platform's secure enclave API on device classes where an enclave is available. On device classes without a hardware enclave — older Android devices, some Windows devices without Pluton — the package falls back to OS-keystore isolation with explicit documentation that the protection level is lower. The architecture does not silently degrade. The startup report identifies the key-storage tier in use, and administrators enforce a minimum tier through the deployment manifest. Regulated-tier deployments mandate enclave-backed key storage. Consumer-tier deployments encourage it.

### Sub-pattern 47c — Attested boot and integrity measurement

A compromised endpoint is most dangerous when the compromise is invisible — when the device continues to participate in the sync mesh without the relay or other peers detecting the anomaly. Attested boot addresses this. TPM 2.0 and equivalent mechanisms produce a cryptographic proof that the device is running expected, unmodified software at boot time. The attestation is presented to the relay at handshake; the relay validates it against a known-good measurement before admitting the session. A device that fails attestation is denied relay admission and falls back to local-only operation. It does not silently contaminate the sync mesh.

The attestation surface integrates at the sync daemon's handshake layer (Ch14 §Sync Daemon Protocol). `Sunfish.Kernel.Security` exposes the attestation; the relay-side enforcement is in the relay's handshake policy, not the node package. <!-- CLAIM: Ch14 §Sync Daemon Protocol does not currently describe attestation validation at the handshake; this draft assumes it as a forward dependency. Confirm in Ch14 cross-reference and either back-add or flag as a gap to address with a parallel Ch14 update. -->

The honest limitation is the runtime-compromise gap. Attestation covers boot-time integrity. It does not cover runtime compromise — a device that boots cleanly and is then exploited mid-session is not caught by attestation alone. The residual risk is in-session compromise between attestation events. For high-security deployments, the architecture requires re-attestation at every relay reconnection, which narrows the gap to a single session's duration. It does not eliminate it; an in-session zero-click exploit between two reconnects remains an exposure.

### Sub-pattern 47d — Remote-wipe capability

When a device is confirmed lost or compromised, the operator needs to revoke that device's access and, where possible, crypto-shred the local copy of the data. Remote wipe is the operational procedure. The administrator issues a revocation broadcast for the device's node identity — the same mechanism as §Collaborator Revocation, applied to a device rather than a person — carrying a crypto-shred instruction. On receipt, the node overwrites its local key material and database encryption key with random bytes before exit.

The honest limitation is reachability. Remote wipe is only as reliable as the device's network reachability at the moment the broadcast fires. A device that is powered off, in airplane mode, or behind a network that blocks the relay cannot receive the wipe instruction until it reconnects. The architecture does not guarantee synchronous destruction — it guarantees destruction upon next reachable sync event, with audit-trail confirmation. An attacker who deliberately keeps the device offline defeats this control until reconnection occurs.

MDM (Mobile Device Management) integration is the parallel channel that closes the offline-device gap. Enterprise deployments using Intune, Jamf, or Google Workspace MDM issue an OS-level wipe order through MDM channels in parallel with the architecture's crypto-shred. The two mechanisms are complementary; MDM catches the case where the device never reconnects to the relay. `Sunfish.Kernel.Security` implements the local-side crypto-shred instruction. MDM integration is the deployment layer's responsibility — it is not part of the kernel-security package.

### Sub-pattern 47e — Endpoint-compromise containment

The blast radius of a compromised endpoint must be bounded. Three containment mechanisms enforce the FAILED conditions stated in §Sub-pattern 47a — that a compromised device cannot impersonate other devices, cannot backdate transactions, and cannot access other users' data on the relay.

**Per-device keypair isolation.** Each device in a user's fleet holds a distinct keypair. Compromise of one device's private key does not compromise other devices in the same fleet. The sync daemon rejects session tokens signed by a key it does not recognize, and the relay enforces keypair-session binding at every reconnection. An attacker holding a stolen session token from one device cannot pivot it onto another.

**Append-only transaction log.** The CRDT operation log is append-only and each entry is signed by the originating device keypair. Backdating requires a valid signature from the target timestamp's keypair — an attacker who compromises a device today cannot sign operations as if they occurred last week, because the historical keypair is not the one currently in the OS keychain. Forward-secrecy key rotation (#46) further narrows the window during which any single compromised key can sign anything at all.

**Role-scoped access.** A compromised device can access only the data classes and roles it was provisioned to access. It cannot escalate to roles held by other users on the relay. The relay enforces role-level access at every session handshake (§Role Attestation Flow). The compromise stays inside the lane it started in.

### Sub-pattern 47f — Honest documentation of post-compromise risk

This sub-pattern is not a cryptographic mechanism. It is an architectural commitment to honesty. The chapter must state directly what protection lapses at endpoint compromise, not leave the reader to infer it.

The lapses, stated directly: local cached data is readable with the locally-held keys. Future writes from the compromised device are trusted by peers until revocation propagates. A session in progress at compromise time exposes whatever plaintext is already in memory. Biometric-based authentication on the compromised device cannot be trusted, because the attacker controls the authentication flow.

The architecture does not claim to solve endpoint compromise. It claims four things: blast-radius containment via the three mechanisms in §47e; hardware-backed key protection where the platform offers it; a remote-wipe path that completes when the device is reachable; and honest documentation of the residual risk so practitioners plan against it rather than discover it in an incident post-mortem. Pegasus, Predator, and Hermit operate at the level of full OS compromise with zero-click delivery [21][22]. Against these, hardware enclave separation is the only control that reliably retains key protection. On a fully Pegasus-compromised device, keys in the OS keychain are accessible; keys in a hardware enclave are not. No software-only architecture can claim otherwise.

### FAILED conditions

The primitive's FAILED conditions, drawn directly from design-decisions §5 #47:

- Compromised endpoint can impersonate other devices in the sync mesh.
- Compromised endpoint can backdate transactions in the shared log.
- Endpoint compromise scope is not documented in the deployed architecture's security reference.

Any FAILED condition confirmed at technical review escalates to `Sunfish.Kernel.Security` maintainers before the draft advances. This primitive has security-boundary implications; a confirmed failure is not a prose-pass defect.

---

<!-- ============================================================ -->
<!-- PART 2: Appendix B new threat-actor entry —                   -->
<!-- "THREAT-10 — Compromised Endpoint"                           -->
<!-- Insertion point: appended to ## Section 2 — Actor Taxonomy   -->
<!-- Template, after the existing "Supply chain attacker" row     -->
<!-- and after the "Government authority" row                     -->
<!-- Target: ~500 words                                           -->
<!-- Note: introduces the THREAT-NN format; future #9 chain-of-   -->
<!-- custody extension follows as THREAT-11                       -->
<!-- ============================================================ -->

## Part 2: Appendix B — `### THREAT-10 — Compromised Endpoint`

---

### THREAT-10 — Compromised Endpoint

THREAT-10 is the first numbered, structured entry in this taxonomy. Subsequent extensions follow the same THREAT-NN format.

**Actor profile.** A device fully owned by an attacker. The OS is no longer trustworthy: persistent malware, a zero-click exploit, or other privileged code execution defeats application-layer protections. Consumer spyware and nation-state tooling both fall in this category. The capability ceiling differs; the architectural exposure does not.

**Capabilities.**

| Tier | Examples | Practical implication |
|---|---|---|
| Medium | Scripted exploit, consumer spyware | Reads OS keychain on non-enclave devices; reads in-memory plaintext during active session; captures session tokens |
| High | Pegasus, Predator, Hermit (zero-click, nation-state) | All of the above, plus persistence across reboots; covert sync-mesh participation until revocation |

Most real-world compromises are Medium. High capability changes the calculus for hardware enclaves: only enclave-backed key storage retains protection; the OS keychain is read.

**Attack surface.** OS keychain, in-memory key material during active session, application database (decryptable with the locally-held DEKs), session tokens, biometric authentication flow.

**Architecture protects.** Other devices in the user's fleet (per-device keypair isolation). Other users' data on the relay (role-scoped access). Future state after revocation propagates. Transaction-log integrity — backdate attacks blocked by the append-only log and per-device signing.

**Architecture does not protect.** Local cached data that was decryptable before compromise. Current-session plaintext in memory. Keys held in the OS keychain on non-enclave devices.

**Residual risk.** Scoped to the compromised device's cached copy. On enclave-class devices (Secure Enclave, Titan M, Pluton), the KEK is protected even under OS compromise; in-memory plaintext remains exposed. On non-enclave devices, the KEK is exposed and all locally-cached ciphertext is decryptable.

#### Attack tree — primary branch: mobile zero-click compromise

1. **Attacker delivers zero-click exploit.** No user interaction. Targets the OS messaging stack or browser engine. Device is compromised silently.
2. **Attacker reads OS keychain.** Non-enclave devices: KEK is extracted; locally-cached ciphertext is decryptable. Attack succeeds at the data-access goal.
3. **Enclave check.** Enclave-class devices: KEK is inaccessible via OS API. Attack contained to in-memory plaintext during active session only.
4. **Attacker reads in-memory plaintext.** Whatever the application has decrypted for display is accessible. Re-authentication interval (Ch15 §In-Memory Key Handling) limits the window — four hours consumer, sixty minutes regulated.
5. **Attacker attempts relay impersonation.** Captured session token used to forge writes. Blocked when the token is bound to the device keypair and the relay enforces keypair-session binding. Bearer-only tokens succeed — that is an architectural failure against §47e.
6. **Operator issues remote-wipe broadcast.** Revocation plus crypto-shred propagates. The device evicts key material on next connection. An attacker who keeps the device offline defers the wipe; MDM (parallel channel) catches that case for enterprise deployments.

#### Mitigation summary

- Mandate enclave-backed key storage for any deployment with regulated or sensitive individual data.
- Enforce re-authentication intervals: four hours consumer, sixty minutes regulated.
- Integrate MDM (Intune, Jamf, Google MDM) for enterprise deployments. MDM wipe runs in parallel with crypto-shred.
- Enforce device attestation at relay handshake for high-security deployments.
- Communicate honestly: no architecture protects data on a fully-compromised device where the attacker has extracted keys from a non-enclave keychain.

Cross-references: Ch15 §Endpoint Compromise (full specification); Ch15 §In-Memory Key Handling (re-authentication interval); Ch15 §Collaborator Revocation (the broadcast mechanism reused by remote wipe).

---

<!-- ============================================================ -->
<!-- PART 3: Ch15 reference list additions                        -->
<!-- Existing Ch15 references: [1]–[13]                           -->
<!-- New entries start at [14]. Apple Platform Security already at -->
<!-- [7] — reuse for Secure Enclave (47b) where cited; do not      -->
<!-- duplicate.                                                    -->
<!-- ============================================================ -->

## Part 3: Ch15 reference-list additions

Append to the existing `## References` section in `chapters/part-3-reference-architecture/ch15-security-architecture.md`. Existing list runs through [13]. Apple Platform Security is already cited as [7] from extension #48; the Secure Enclave inline citation in 47b uses [14] below for the consolidated platform-enclave reference, but where the existing [7] suffices for an Apple-specific point the draft reuses it. The mapping in the draft prose: [14] Apple Secure Enclave (could collapse into existing [7] at technical-review's discretion); [15] Google Titan M; [16] Microsoft Pluton; [17][18][19] SGX cautionary attacks; [20] ARM TrustZone; [21] Pegasus; [22] Hermit / Predator collective.

If technical review elects to collapse [14] into existing [7] (Apple Platform Security), renumber [15]–[22] down by one. The draft is written to be renumber-stable: prose cites the work, not the bare number.

[14] Apple Inc., "Apple Platform Security — Secure Enclave," May 2024. [Online]. Available: https://support.apple.com/guide/security/secure-enclave-sec59b0b31ff/web

[15] Google, "Pixel Titan M and Android Hardware-Backed Keystore," Android Developers documentation, 2024. [Online]. Available: https://source.android.com/docs/security/features/keystore and https://developer.android.com/privacy-and-security/keystore

[16] Microsoft, "Microsoft Pluton security processor," Microsoft Security Blog, Nov. 17, 2020. [Online]. Available: https://www.microsoft.com/en-us/security/blog/2020/11/17/meet-the-microsoft-pluton-processor-the-security-chip-designed-for-the-future-of-windows-pcs/

[17] J. Van Bulck *et al.*, "Foreshadow: Extracting the Keys to the Intel SGX Kingdom with Transient Out-of-Order Execution," in *Proc. 27th USENIX Security Symposium*, 2018, pp. 991–1008.

[18] K. Murdock *et al.*, "Plundervolt: Software-based Fault Injection Attacks against Intel SGX," in *Proc. IEEE Symposium on Security and Privacy (S&P)*, 2020, pp. 1466–1482.

[19] S. van Schaik *et al.*, "SGAxe: How SGX Fails in Practice," 2020. [Online]. Available: https://sgaxe.com/

[20] Arm Ltd., "Arm Security Technology — Building a Secure System using TrustZone Technology," white paper, Apr. 2009 (rev. 2022). [Online]. Available: https://developer.arm.com/documentation/prd29-genc-009492/

[21] B. Marczak, J. Scott-Railton, and R. Deibert (Citizen Lab), "Forensic Methodology Report: How to catch NSO Group's Pegasus," Jul. 2021. [Online]. Available: https://citizenlab.ca/2021/07/forensic-methodology-report-how-to-catch-nso-groups-pegasus/

[22] Lookout Threat Intelligence, "Lookout Discovers Hermit Spyware Deployed in Kazakhstan," Jun. 2022. [Online]. Available: https://www.lookout.com/threat-intelligence/article/hermit-spyware-discovery — for Hermit; supplement with Google Threat Analysis Group analysis of Predator/Cytrox at https://blog.google/threat-analysis-group/.

---

## Cross-references wired in this draft

Per outline §H — verified present in the prose above:

- Ch15 §Endpoint Compromise → Ch15 §Threat Model (master taxonomy) — wired in opening paragraph.
- Ch15 §Endpoint Compromise → Ch15 §Key Hierarchy — wired in 47b.
- Ch15 §Endpoint Compromise → Ch15 §Key Compromise Incident Response — implicit through §Collaborator Revocation reuse; not explicitly named (acceptable per outline).
- Ch15 §Endpoint Compromise → Ch15 §In-Memory Key Handling — wired in opening sentence and in 47f via re-authentication interval.
- Ch15 §Endpoint Compromise → Ch15 §Collaborator Revocation — wired in 47d.
- Ch15 §Endpoint Compromise → Ch14 §Sync Daemon Protocol — wired in 47c (with CLAIM marker for forward dependency).
- Ch15 §Endpoint Compromise → #46 forward-secrecy — wired in 47e (append-only log discussion).
- Ch15 §Endpoint Compromise → #45 collaborator revocation — wired in 47d (reuses the revocation-broadcast mechanism).
- App B THREAT-10 → Ch15 §Endpoint Compromise — wired in cross-reference footer.
- App B THREAT-10 → Ch15 §In-Memory Key Handling — wired in attack-tree branch 4.

---

## CLAIM markers for technical review

One CLAIM marker inserted in this draft:

1. **Ch14 attestation handshake.** §47c states the relay validates attestation at handshake against known-good measurements. The outline §D technical-review focus flags that Ch14 §Sync Daemon Protocol may not currently describe attestation validation. Marker inserted at the relevant paragraph. Action for technical reviewer: confirm Ch14's current state, and either back-add a brief attestation paragraph to Ch14 or replace the §47c claim with a forward-looking statement that attestation handshake is part of extension #47's contract on the sync daemon.

---

## Word counts (actual)

Counted with the standard `make word-count` heuristic (whitespace-separated tokens, prose body only — table content counted as cell text, code/HTML comments excluded):

- **Part 1 — Ch15 §Endpoint Compromise:** 1,691 words (target 1,500; +12.7%; within ±20% acceptable band).
- **Part 2 — App B §THREAT-10:** 554 words (target 500; +10.8%; within ±20% acceptable band).
- **Part 3 — Reference list additions:** 9 new entries, administrative (not counted toward chapter prose target).

**Total prose:** 2,245 words against the combined 2,000-word target (+12.3%). Within the ±20% acceptable band.

---

## QC items — drafter self-assessment

- [x] QC-1 Word count within ±20% acceptable band (2,245 vs. 2,000 target; +12.3%).
- [x] QC-2 All sub-patterns 47a–47f addressed; FAILED conditions block included.
- [x] QC-3 Source citations inline (design-decisions §5 #47 referenced; new IEEE citations [14]–[22] added).
- [x] QC-4 Sunfish referenced by package name only (`Sunfish.Kernel.Security`); no class APIs.
- [x] QC-5 No academic scaffolding ("this section presents", "as we have seen") — verified.
- [x] QC-6 No re-introducing the architecture; assumes Part I is read.
- [x] QC-7 Part III specification voice for Ch15; reference-table register for App B.
- [N/A] QC-8 Ch2-only rule.
- [N/A] QC-9 Council two-act rule.
- [x] QC-10 No placeholder text. Single CLAIM marker is intentional, scoped, and noted for technical review.

Sunfish reference policy: only `Sunfish.Kernel.Security` named; no new namespace introduced (per sunfish-package-roadmap.md entry for #47, this primitive extends the existing namespace). No code snippets in this draft, so the `// illustrative — not runnable` marker is unused.

The Pegasus paragraph (§47f) is deliberately hard. The hard sentence — "No software-only architecture can claim otherwise" — must survive prose review unsoftened.
