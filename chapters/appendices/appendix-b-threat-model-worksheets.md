# Appendix B — Threat Model Worksheets

<!-- icm/prose-review -->

<!-- Target: ~1,800 words -->
<!-- Source: v13 §11.1, Ch15, Ch22, Ch23 -->

---

## Introduction

Build your deployment threat model with these four worksheets. Fill them in before your first production deployment. Update them when the asset inventory changes. Run the incident response template the moment a key compromise is suspected — not the moment it is confirmed. Chapter 15 carries the security architecture: the DEK (Data Encryption Key)/KEK (Key Encryption Key) key hierarchy, the role attestation flow, and the compelled-access resistance model. Chapter 22 carries the key compromise incident response procedure. Complete Chapter 19's compliance checklist before you start this exercise. The checklist names the regulatory ground these worksheets stand on.

---

## Section 1 — Asset Inventory Template

Fill this table before you start the threat model exercise. Every row is an asset that, if compromised, lost, or corrupted, would cause material harm to the team or to a person who trusted you with their data.

| Asset | Classification | Location | Owner | Sensitivity |
|---|---|---|---|---|
| User CRDT (Conflict-free Replicated Data Type) documents | Team-confidential | Local SQLCipher DB (per node) | User | High |
| Role KEKs | Team-secret | OS keystore (per node) | Team admin | Critical |
| Data Encryption Keys (DEKs) | Team-secret | Alongside ciphertext in SQLCipher | System | Critical |
| Device keypairs (Ed25519) | Node-secret | OS keystore (per node) | System | Critical |
| Attestation bundles | Team-internal | Local node; relay for catch-up | System | High |
| Sync operation log | Team-confidential | Local SQLCipher DB (per node) | Team | High |
| Relay ciphertext cache | Encrypted | Relay (operator-managed) | Operator | Medium (ciphertext only) |
| MDM (Mobile Device Management) configuration | Internal | MDM system (Intune / Jamf / SOTI MobiControl / IBM MaaS360 / Ivanti Endpoint Manager); node-config.json on endpoint | IT admin | Medium |
| Audit log completeness record | Compliance-grade | Local SQLCipher DB; exported to regulatory package | Compliance officer | Critical (Japan PIPA (Personal Information Protection Act) / Korea ISMS-P (Information Security Management System – Personal) / PIPL (Personal Information Protection Law) regulated deployments) |

**Customization guidance:** Add domain-specific rows. HIPAA (Health Insurance Portability and Accountability Act)-covered entities must treat patient identifiers as Critical. HIPAA, SOX, ITAR (International Traffic in Arms Regulations), GDPR (General Data Protection Regulation) (data minimization and purpose limitation), DPDP (Digital Personal Data Protection) Act Section 8 (purpose specification), and comparable frameworks set minimum classification floors. Set those floors before you fill in the Sensitivity column. Before you treat any Node-secret or Team-secret row as structurally isolated, write down which OS keystore protects it: Windows Credential Manager with TPM (Trusted Platform Module), macOS Keychain with Secure Enclave, Linux libsecret with the kernel keyring, Android Keystore, iOS Data Protection. These keystores have meaningfully different security boundaries. A practitioner who is reasoning about node-secret isolation needs to verify their platform's actual properties, not the platform's marketing.

**Classification definitions for this template:**

| Label | Meaning |
|---|---|
| Node-secret | Known only to the node that generated it; never transmitted |
| Team-secret | Known to authorized team members; protected by KEK hierarchy |
| Team-confidential | Restricted to named team members with role-based access |
| Team-internal | Available to all current team members; not for external disclosure |
| Encrypted | Stored or transmitted in ciphertext; plaintext inaccessible without key material |

---

## Section 2 — Actor Taxonomy Template

List every actor who interacts with your system, or who could realistically interact with it, including adversarial actors. For each one, write down the realistic motivation. Then write down the capability level you must plan for — not the capability level you wish you only had to plan for.

| Actor | Access level | Likely motivation | Capability level |
|---|---|---|---|
| External attacker (remote) | None initially | Data theft, ransomware | Low to High |
| External attacker (physical access) | Physical device access | Credential theft, storage extraction | Medium |
| Malicious insider (role access) | Team member with authorized role | Data exfiltration within role scope | Medium |
| Compromised relay operator | Transport layer (ciphertext) | Traffic analysis, availability attack | Limited (no plaintext) |
| Relay service termination by policy | Service withdrawal | Jurisdiction restriction, sanctions, commercial decision | Total relay unavailability; local node continues, peer-to-peer sync continues where reachable |
| Former team member | None after rotation for future access | Historical data retention, post-revocation exfiltration attempt | Low for future access (blocked by key rotation). Historical exposure scope is determined by the data-at-risk calculation in Section 4 — key rotation does not remediate prior exfiltration |
| Compromised IdP (Identity Provider) | Authentication layer | Issue fraudulent role attestations | High — bypasses the attestation trust anchor. Requires IdP-level detection and rotation of the IdP signing key |
| Supply chain attacker | Build pipeline | Backdoor via malicious package or binary | High if signing key compromised |
| Government authority / regulatory body | Statutory — legal compulsion | Data access under warrant, subpoena, or administrative order; device seizure; regulatory inspection | Statutory. Mitigation: end-to-end encryption with local key management (keys never transmitted to relay) means ciphertext-only exposure on compelled relay inspection. Device seizure exposes whatever is decryptable with device-present credentials. This is the Schrems II, PIPL, 242-FZ, DIFC (Dubai International Financial Centre), UAE DPL (Data Protection Law), RBI (Reserve Bank of India), POPIA (Protection of Personal Information Act), NDPR (Nigeria Data Protection Regulation), and Japan PIPA regulatory-access threat model |

**Customization guidance:** Add the actors specific to your vertical. Healthcare deployments add "unauthorized staff member with workstation access" and "patient with provider relationship." Legal deployments add "opposing counsel seeking discovery advantage." Government and defense deployments add nation-state actors and insider threat programs as distinct entries with capability levels that match. Deployments in regulated markets — DIFC, RBI-supervised BFSI (Banking, Financial Services, and Insurance), PIPL-scoped, POPIA-scoped, GDPR-scoped — extend the statutory-access actor with jurisdiction-specific inspection rights. Document the regulatory basis in the capability notes so a future reader knows the law you were planning against.

**Capability level definitions:**

| Level | Meaning |
|---|---|
| Low | Script kiddie; uses published exploits; no novel capability |
| Medium | Competent attacker; adapts existing tools; targeted but not sophisticated |
| High | Sophisticated attacker; zero-day capability; nation-state or well-funded criminal |
| Limited | Access is structurally constrained (e.g., ciphertext only — no key material) |

### THREAT-10 — Compromised Endpoint

Subsequent threat entries follow the same THREAT-NN format used here.

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

Cross-references: Ch23 §Endpoint Compromise (full specification); Ch15 §In-Memory Key Handling (re-authentication interval); Ch23 §Collaborator Revocation (the broadcast mechanism reused by remote wipe).

---

## Section 3 — Worked Example: Construction PM Vertical

**Scenario:** A five-person construction project management team is running the inverted stack. The primary workflows are RFI tracking, punch lists, and change orders. Nodes run on Windows 11 laptops. The team works from job sites with intermittent connectivity. The relay is operator-managed and cloud-hosted. There is no self-hosted relay.

### Vertical-Specific Asset Additions

Add these rows to the standard asset inventory table:

| Asset | Classification | Location | Owner | Sensitivity |
|---|---|---|---|---|
| Bid documents | Confidential | Local SQLCipher DB | Project manager | Critical |
| Subcontractor contracts | Confidential | Local SQLCipher DB | Principal | Critical |
| Change order log | Compliance-grade | CRDT compliance tier (immutable) | System | Critical |
| Project schedule | Team-internal | Local SQLCipher DB | Project manager | High |
| Punch list items | Team-internal | Local SQLCipher DB | Field supervisor | Medium |

### Vertical-Specific Actor Additions

| Actor | Motivation | Realistic attack |
|---|---|---|
| Competitor | Access to bid pricing | Physical access to project manager's laptop at a job site |
| Disgruntled subcontractor | Evidence deletion | Insider with partial role access; attempt to modify change order log |
| Relay operator | Traffic analysis | Observe which teams are active during a bid period |

### Attack Tree — Primary Branch: Laptop Theft at Job Site

This is the highest-probability threat for this vertical. Project managers carry laptops to job sites. Vehicles get broken into. Walk through the branches one at a time:

1. **Attacker steals project manager's laptop from vehicle.** Physical access is achieved.
2. **Disk encryption check.** If BitLocker is not enforced through MDM policy, the attacker reads the filesystem directly. Mitigation: enforce BitLocker through MDM policy (Intune Device Compliance policy). Confirm the compliance check is enforced before the node is permitted to join the sync mesh.
3. **Disk encryption is active.** The attacker reads the SQLCipher database file. Without the SQLCipher passphrase, the database is ciphertext. The attack fails at this branch.
4. **Device is powered on at time of theft.** The cold-boot attack window applies. See Ch15 §In-Memory Key Handling for the policy. A realistic cold-boot attack requires laboratory conditions: DRAM module removal within seconds of power loss, chilled-memory preservation (liquid nitrogen or coolant spray to slow decay), and forensic imaging equipment. Unencrypted hibernation files and suspend-to-disk images expand the window. Disable both via MDM. Treat this as residual risk outside high-security environments. In government, defense, or intelligence contexts, consult Ch15 §In-Memory Key Handling for the re-authentication interval guidance and enforce shorter intervals.
5. **Attacker targets OS keychain.** The role KEK and the device keypair sit in the Windows Credential Manager. To get to them you need the device PIN or the biometric. An attacker without the credential cannot extract key material from a locked device. Mitigation: enforce a 6-digit minimum PIN through MDM. Disable USB boot. Lock down BIOS settings changes.
6. **Attacker copies SQLCipher DB offline.** Without the KEK and the SQLCipher passphrase, the ciphertext is unreadable. The attack fails.

**Residual risk: communication pattern analysis.** The relay operator cannot read document content — every sync payload is encrypted before it leaves the node. The operator can still observe which nodes are active and when. In a five-person team, heavy sync activity between the project manager node and the estimator node in the 72 hours before a bid deadline tells the operator that an active bid is in preparation. The content is protected. The fact of activity is not.

**Mitigation for residual risk:** Deploy a self-hosted relay for projects with high competitive sensitivity. A self-hosted relay moves the traffic analysis capability from an external operator to internal IT, which is inside your trust boundary. See Ch 15 for relay deployment options.

**Supply chain branch (not laptop-theft-specific, but every worksheet must include it):** A compromised build pipeline can ship a backdoored binary that exfiltrates keys or plaintext from inside the trust boundary. Practitioners MUST add a supply chain branch to their own attack tree. Source repository integrity: signed commits, protected branches. Build reproducibility: deterministic builds, SBOM (Software Bill of Materials) verification. Binary signing: hardware-backed signing keys, code-signing certificate protection. Distribution channel integrity: package manifest signatures verified on install. A supply chain compromise can defeat every node-level control in this appendix. Model it explicitly.

---

## Section 4 — Key Compromise Incident Response Template

Use this template when a KEK compromise is detected or suspected. The triggers are familiar: a stolen device, a reported credential leak, an anomalous access pattern in the audit log. Do not wait for confirmation before you start the re-keying procedure. A suspected compromise is enough to begin.

### Detection Checklist

Run through this list whenever an employee reports a security event:

- [ ] Physical loss or theft reported by employee
- [ ] Anomalous access pattern flagged in audit log (off-hours access, unusual volume, unfamiliar source IP)
- [ ] Employee reports credentials as potentially compromised
- [ ] Security team identifies device in threat intelligence feed
- [ ] IdP reports failed authentication attempts against the affected account
- [ ] Employee is terminated or resigns (proactive revocation, not reactive)
- [ ] Unplanned device shutdown during sync operation in a region with unreliable grid power (Lagos, Karachi, parts of SE Asia). Distinguish this from a security event. A node that resumes cleanly from WAL (Write-Ahead Log) replay is an infrastructure failure. A node that cannot complete WAL replay, or that shows sync-daemon state inconsistent with the local database, is a potential security event until the sync mesh confirms consistency.
- [ ] Government authority or regulatory body presents a lawful access demand (subpoena, warrant, administrative order, inspection notice). Engage legal counsel before any response. The architectural response is specified in Chapter 15. The incident response below still applies to any credentials exposed during compliance with such orders.

Any checked item triggers the re-keying procedure below. Multiple checked items mean elevated severity — consider notifying affected users immediately rather than waiting until the procedure is complete.

### Re-Keying Procedure

Execute these steps in order. Do not skip steps. Each step has a named owner and a completion condition.

| Step | Action | Owner | Completion condition |
|---|---|---|---|
| 1 | Generate new KEK for each affected role using cryptographically random key material. Do not derive from the compromised KEK. | Administrator | New KEK material exists in keystore; derivation from old KEK is not used |
| 1a | **Check old KEK availability before Step 2.** If the old KEK cannot be retrieved (device seized, device destroyed, keystore wiped, hardware failure of the KEK-holder's primary node), Step 2 cannot execute. The DEKs wrapped under the old KEK are permanently inaccessible without the KEK. Document the scope of unrecoverable data in the incident log. Proceed directly to Step 4 to broadcast revocation and prevent further compromise. Affected documents must be treated as lost. The team decides whether to reconstruct them from BYOC (Bring Your Own Cloud) backup (Chapter 16) or accept the loss. | Administrator | Recovery status documented in incident log; team has decided on reconstruction-from-backup or accepted-loss path |
| 2 | For each document in the affected role's scope (where the old KEK is available): decrypt the existing wrapped DEK using the old KEK, re-encrypt (wrap) with the new KEK, store alongside ciphertext. | Administrator | All recoverable DEKs in scope are re-wrapped; no document references the old KEK |
| 3 | Discard the old KEK and all node-level copies. Verify deletion with OS keystore audit. | Administrator | Keystore audit confirms old KEK is absent from all managed nodes |
| 4 | Broadcast revocation through the relay. All active nodes receive `ERR_KEY_REVOKED` on next handshake. | Administrator | Revocation broadcast confirmed; relay acknowledges |
| 5 | Any node holding the revoked key that attempts to reconnect receives `ERR_KEY_REVOKED` and must re-authenticate with IdP. | System (automatic) | Monitor relay logs for unexpected successful handshakes post-revocation |
| 6 | Notify all team members in the affected role. Include the KEK creation date, the revocation date, and the scope of potentially accessible data. | Administrator | All affected users notified; notification logged with timestamp |
| 7 | Issue new wrapped KEK copies to all current authorized members of the affected role through the standard key distribution path. | Administrator | All authorized members can sync; no member has access to old KEK |

### Data-at-Risk Scope Calculation

- **Start date:** The date the compromised KEK was created. Check the keystore creation timestamp. Do not rely on employee recollection.
- **End date:** The date the revocation broadcast was confirmed at the relay.
- **Scope:** Every document the compromised KEK protected between the start date and the end date.
- **Excluded from scope:** Documents in roles not protected by the compromised KEK. Documents created after the revocation date — those are protected under the new KEK.

### User Notification Template

Send this message to every team member in the affected role. Adjust the bracketed fields:

> A security event affected [role name] credentials on [date]. We have issued new credentials and revoked the previous ones.
>
> Documents in [role name] between [start date] and [end date] may have been accessible to an unauthorized party. All documents created after [end date] are protected under the new credentials.
>
> Sign in again to continue syncing. Your data is intact; this step updates your access credentials only.
>
> Contact [IT contact name] at [IT contact email or phone] with questions.

**Logging requirement — retention floor:** Record the timestamp of each notification, the channel used (email, SMS, in-app), and the recipient. Retain this record for a minimum of 90 days. This is an audit-log retention floor. It is not a breach notification deadline.

**Breach notification deadlines — separate and faster.** Retention and notification are distinct obligations. The deadlines below are notification-to-regulator windows — and in some jurisdictions, notification-to-affected-data-subjects windows — that run from the moment the organization becomes aware of the breach. Verify the jurisdiction-specific window before you set an incident response SLA (Service Level Agreement):

| Jurisdiction | Notification to supervisor | Notification to data subjects |
|---|---|---|
| EU (GDPR Article 33–34) | 72 hours | "without undue delay" when high-risk |
| UK (UK GDPR) | 72 hours | as GDPR |
| Brazil (LGPD (Lei Geral de Proteção de Dados)) | "reasonable time" per ANPD guidance | as required by risk |
| China (PIPL Article 57) | Within 3 working days to CAC | "without undue delay" |
| Japan (PIPA Article 26) | "promptly" to PPC | "promptly" |
| South Korea (PIPA) | Within 24 hours for large breaches | "without delay" |
| India (DPDP Act Section 8) | As prescribed by Data Protection Board | As prescribed |
| UAE (DPL 2022) | 72 hours for high-risk | As directed |
| Russia (242-FZ + 152-FZ) | Within 24 hours initial, 72 hours supplementary | As required |
| Nigeria (NDPR) | Within 72 hours | "expeditiously" |
| South Africa (POPIA) | "as soon as reasonably possible" to the Regulator | "as soon as reasonably possible" |
| USA (HIPAA) | 60 days from discovery for reportable breaches | 60 days |
| USA (state laws — CCPA (California Consumer Privacy Act), etc.) | Varies | Varies |

Verify the jurisdictional obligations for every market the team operates in before the first incident occurs. The retention floor above is an audit control. The table above is the incident SLA.

---

## Section 5 — Chain-of-Custody Worksheet

Use this worksheet when the deployment transfers sensitive data to a third party (insurer, regulator, auditor, legal counsel, successor entity), handles evidence-class data (dashcam footage, healthcare records, financial audit logs), or operates a mandated regulatory-export stream (MDS-style telemetry, financial reporting, healthcare event reporting). Fill it in before the first evidence-class transfer; revisit when regulatory scope changes. Architectural specification: Ch23 §Chain-of-Custody for Multi-Party Transfers.

### Field 1 — Parties

| Role | Identity | Device key fingerprint | Jurisdiction |
|---|---|---|---|
| Transferor (originating custodian) | | | |
| Recipient (receiving custodian) | | | |
| External authority (regulator, TSA, court) — if applicable | | | |

Record fingerprints from the published key hierarchy, not informal channels.

### Field 2 — Data class

| Data class | Evidence-class? | Retention floor | Crypto-shred eligible? |
|---|---|---|---|
| | Yes / No | | Yes / No |

Under-designation saves setup cost until the first legal dispute exposes the gap.

### Field 3 — Transfer trigger

Name the event that initiates transfer (scheduled regulatory export, insurer claim request, auditor engagement, departure partition under Ch23 §Collaborator Revocation sub-pattern 45e, subpoena, warrant) and the authorization gate — who signs off before a `CustodyTransferInitiated` event emits.

### Field 4 — Signing requirements

- [ ] Both transferor and recipient device keys are in the published key hierarchy with valid attestation at transfer time.
- [ ] Transferor signing role grants `re-transfer` scope (onward custody) or excludes it (custody terminal at recipient).
- [ ] One-sided `transfer-initiated` records are flagged incomplete and excluded from any artifact represented as completed.
- [ ] Audit-log validation rejects `CustodyTransferConfirmed` events lacking both signatures.

### Field 5 — Timestamping

| Item | Decision |
|---|---|
| External TSA required? | Yes (evidence-class) / No (consumer-tier) |
| TSA provider and qualification basis | e.g., eIDAS qualified TSP (EU); equivalent per jurisdiction |
| TSA endpoint and certificate fingerprint | |
| Max `tsa-pending` duration before compliance escalation | |
| Offline policy | Queue and submit on next relay window / Block transfer until TSA reachable |

Record the TSA certificate fingerprint locally so the verifier detects a substituted endpoint.

### Field 6 — Verification

- [ ] Merkle-chain verification documented for streaming exports — root cadence, hash function (SHA-256 default), proof format.
- [ ] Receipt-verification documented for bilateral transfers — signature check, version-vector match, TSA-token validation.
- [ ] Attestation artifacts (TSA tokens, Merkle proofs, signed receipts) retained alongside the data they attest. Lost artifacts reduce the transfer to `transfer-initiated` retroactively.

### Field 7 — Escalation paths

On `CustodyTransferDisputed` (recipient version mismatches transferor assertion):

1. Halt further transfers of the affected object pending resolution.
2. Log the dispute event with both signed events.
3. Engage legal counsel before responding to any external party.
4. Diagnose divergence: transferor error, recipient error, network corruption, adversarial tampering. Each path differs.
5. Do not reconcile by modifying either local log. The disputed state is the legally relevant state.

On TSA outages exceeding the declared pending duration, escalate to the compliance officer. On Merkle-chain verification failures recipient-side, treat as a stream-omission incident before responding to the regulator.

The worksheet is deployment-time. Per-transfer enforcement happens in `Sunfish.Kernel.Custody` through the four event contracts named in Ch23 §Chain-of-Custody.

---

*These worksheets are deployment tools, not compliance documentation. They do not substitute for a qualified security assessment in regulated environments. Engage a qualified assessor who can evaluate the full deployment against the applicable control frameworks before you rely on the outputs of this appendix for regulatory representation.*

*Applicable regulatory frameworks by region (non-exhaustive):*

- *North America: HIPAA, ITAR, FedRAMP (Federal Risk and Authorization Management Program), SOC 2, CMMC (Cybersecurity Maturity Model Certification), CCPA, PIPEDA (Personal Information Protection and Electronic Documents Act)*
- *European Economic Area / UK: GDPR (Article 33 — 72-hour supervisor notification; Article 34 — affected-party notification when high-risk), UK GDPR, Schrems II (case C-311/18 — data-transfer compliance driver), BSI (Bundesamt für Sicherheit in der Informationstechnik) TR-02102 and BSI C5 (Germany)*
- *GCC (Gulf Cooperation Council): UAE Federal Data Protection Law 2022, DIFC Data Protection Law 2020, Saudi Arabia Personal Data Protection Law*
- *South Asia: India Digital Personal Data Protection Act 2023 (DPDP), RBI data localization circular (BFSI), Bangladesh DPA*
- *East Asia / APAC (Asia-Pacific): China PIPL (2021), Japan PIPA (revised 2022), South Korea PIPA + ISMS-P certification, Taiwan PDPA, Singapore PDPA*
- *Africa: Nigeria NDPR (2019, re-enacted 2023), South Africa POPIA (2021), Kenya Data Protection Act 2019, Ghana DPA 2012, ECOWAS (Economic Community of West African States) Supplementary Act on Personal Data Protection*
- *Latin America: Brazil LGPD, Mexico LFPDPPP (Ley Federal de Protección de Datos Personales en Posesión de los Particulares), Colombia Ley 1581, Argentina Ley 25.326*
- *CIS (Commonwealth of Independent States): Federal Law 242-FZ (Russia, data localization), Federal Law 152-FZ (Russia, personal data), Kazakhstan Law on Personal Data, Belarus Law on Information, import substitution procurement mandates (импортозамещение) for public-sector and critical-infrastructure deployments*

*For each jurisdiction the team operates in, validate the breach notification window, the retention floor, the regulatory inspection rights, and the cross-border data transfer rules before the first production deployment. The 72-hour GDPR window is the shortest common denominator. Plan incident response against the shortest applicable window, not the longest.*
