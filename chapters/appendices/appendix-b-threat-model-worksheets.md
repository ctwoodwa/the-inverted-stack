# Appendix B — Threat Model Worksheets

<!-- icm/prose-review -->

<!-- Target: ~1,800 words -->
<!-- Source: v13 §11.1, Ch 15 -->

---

## Introduction

Build your deployment threat model with these four worksheets. Fill them in before your first production deployment, update them when the asset inventory changes, and execute the incident response template on any suspected key compromise. Chapter 15 describes the full security architecture — the DEK/KEK key hierarchy, the role attestation flow, the compelled-access resistance model, and the key compromise incident response procedure. Complete Chapter 19's compliance checklist before beginning this exercise; the checklist establishes the regulatory scope these worksheets operate within.

---

## Section 1 — Asset Inventory Template

Fill this table before starting the threat model exercise. Every row represents an asset that, if compromised, lost, or corrupted, would cause material harm to the team or to individual users.

| Asset | Classification | Location | Owner | Sensitivity |
|---|---|---|---|---|
| User CRDT documents | Team-confidential | Local SQLCipher DB (per node) | User | High |
| Role KEKs | Team-secret | OS keystore (per node) | Team admin | Critical |
| Data Encryption Keys (DEKs) | Team-secret | Alongside ciphertext in SQLCipher | System | Critical |
| Device keypairs (Ed25519) | Node-secret | OS keystore (per node) | System | Critical |
| Attestation bundles | Team-internal | Local node; relay for catch-up | System | High |
| Sync operation log | Team-confidential | Local SQLCipher DB (per node) | Team | High |
| Relay ciphertext cache | Encrypted | Relay (operator-managed) | Operator | Medium (ciphertext only) |
| MDM configuration | Internal | MDM system (Intune / Jamf / SOTI MobiControl / IBM MaaS360 / Ivanti Endpoint Manager); node-config.json on endpoint | IT admin | Medium |
| Audit log completeness record | Compliance-grade | Local SQLCipher DB; exported to regulatory package | Compliance officer | Critical (Japan PIPA / Korea ISMS-P / PIPL regulated deployments) |

**Customization guidance:** Add domain-specific rows. HIPAA-covered entities must treat patient identifiers as Critical. HIPAA, SOX, ITAR, GDPR (data minimization and purpose limitation), DPDP Act Section 8 (purpose specification), and comparable frameworks mandate minimum classification floors — set those before filling in the Sensitivity column. Before treating Node-secret or Team-secret rows as structurally isolated, document which OS keystore implementation protects each (Windows Credential Manager + TPM, macOS Keychain + Secure Enclave, Linux libsecret + kernel keyring, Android Keystore, iOS Data Protection). These implementations have meaningfully different security boundaries; a practitioner evaluating node-secret isolation must verify their platform's actual properties.

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

List every actor who interacts or could realistically interact with your system, including adversarial actors. For each actor, record the realistic motivation and the capability level you must plan for.

| Actor | Access level | Likely motivation | Capability level |
|---|---|---|---|
| External attacker (remote) | None initially | Data theft, ransomware | Low to High |
| External attacker (physical access) | Physical device access | Credential theft, storage extraction | Medium |
| Malicious insider (role access) | Team member with authorized role | Data exfiltration within role scope | Medium |
| Compromised relay operator | Transport layer (ciphertext) | Traffic analysis, availability attack | Limited (no plaintext) |
| Relay service termination by policy | Service withdrawal | Jurisdiction restriction, sanctions, commercial decision | Total relay unavailability; local node continues, peer-to-peer sync continues where reachable |
| Former team member | None after rotation for future access | Historical data retention, post-revocation exfiltration attempt | Low for future access (blocked by key rotation). Historical exposure scope is determined by the data-at-risk calculation in Section 4 — key rotation does not remediate prior exfiltration |
| Compromised IdP | Authentication layer | Issue fraudulent role attestations | High — bypasses the attestation trust anchor. Requires IdP-level detection and rotation of the IdP signing key |
| Supply chain attacker | Build pipeline | Backdoor via malicious package or binary | High if signing key compromised |
| Government authority / regulatory body | Statutory — legal compulsion | Data access under warrant, subpoena, or administrative order; device seizure; regulatory inspection | Statutory. Mitigation: end-to-end encryption with local key management (keys never transmitted to relay) means ciphertext-only exposure on compelled relay inspection. Device seizure exposes whatever is decryptable with device-present credentials. This is the Schrems II, PIPL, 242-FZ, DIFC, UAE DPL, RBI, POPIA, NDPR, and Japan PIPA regulatory-access threat model |

**Customization guidance:** Add actors specific to your vertical. Healthcare deployments should add "unauthorized staff member with workstation access" and "patient with provider relationship." Legal deployments should add "opposing counsel seeking discovery advantage." Government and defense deployments should add nation-state actors and insider threat programs as distinct entries with appropriate capability levels. Deployments in regulated markets (DIFC, RBI-supervised BFSI, PIPL-scoped, POPIA-scoped, GDPR-scoped) should extend the statutory-access actor with jurisdiction-specific inspection rights and document the regulatory basis in the capability notes.

**Capability level definitions:**

| Level | Meaning |
|---|---|
| Low | Script kiddie; uses published exploits; no novel capability |
| Medium | Competent attacker; adapts existing tools; targeted but not sophisticated |
| High | Sophisticated attacker; zero-day capability; nation-state or well-funded criminal |
| Limited | Access is structurally constrained (e.g., ciphertext only — no key material) |

---

## Section 3 — Worked Example: Construction PM Vertical

**Scenario:** A five-person construction project management team running the inverted stack. Primary workflows are RFI tracking, punch lists, and change orders. Nodes run on Windows 11 laptops. The team works from job sites with intermittent connectivity. The relay is operator-managed (cloud-hosted). No self-hosted relay.

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

This is the highest-probability threat for this vertical. Construction project managers carry laptops to job sites. Vehicles are broken into. Work through each branch:

1. **Attacker steals project manager's laptop from vehicle.** Physical access is achieved.
2. **Disk encryption check.** If BitLocker is not enforced via MDM policy, the attacker can read the filesystem directly. Mitigation: enforce BitLocker via MDM policy (Intune Device Compliance policy); confirm the compliance check is enforced before the node is permitted to join the sync mesh.
3. **Disk encryption is active.** Attacker reads the SQLCipher database file. Without the SQLCipher passphrase, the database is ciphertext. Attack fails at this branch.
4. **Device is powered on at time of theft.** Cold-boot attack window applies. See Ch 15 §7 for the in-memory key handling policy. A realistic cold-boot attack requires specialized laboratory conditions — DRAM module removal within seconds of power loss, chilled-memory preservation (liquid nitrogen or coolant spray to slow decay), and forensic imaging equipment. Unencrypted hibernation files and suspend-to-disk images expand this window and must be disabled via MDM. Treat as residual risk outside high-security environments; in government, defense, or intelligence deployment contexts, consult Ch 15 for the re-authentication interval guidance and enforce shorter intervals.
5. **Attacker targets OS keychain.** The role KEK and device keypair are stored in the Windows Credential Manager. Accessing them requires the device PIN or biometric. An attacker without the credential cannot extract key material from a locked device. Mitigation: enforce 6-digit minimum PIN via MDM. Disable USB boot and BIOS settings changes.
6. **Attacker copies SQLCipher DB offline.** Without the KEK and the SQLCipher passphrase, the ciphertext is unreadable. Attack fails.

**Residual risk: communication pattern analysis.** The relay operator cannot read document content — all sync payloads are encrypted before leaving the node. However, the operator can observe which nodes are active and when. In a five-person team, heavy sync activity between the project manager node and the estimator node in the 72 hours before a bid deadline reveals that an active bid is in preparation. The content is protected; the fact of activity is not.

**Mitigation for residual risk:** Deploy a self-hosted relay for projects with high competitive sensitivity. Self-hosted relay moves the traffic analysis capability from an external operator to internal IT, which is inside your trust boundary. See Ch 15 for relay deployment options.

**Supply chain branch (not laptop-theft-specific, but every worksheet must include it):** A compromised build pipeline can ship a backdoored binary that exfiltrates keys or plaintext from inside the trust boundary. Practitioners MUST add a supply chain branch to their own attack tree: source repository integrity (signed commits, protected branches), build reproducibility (deterministic builds, SBOM verification), binary signing (hardware-backed signing keys, code-signing certificate protection), and distribution channel integrity (package manifest signatures verified on install). A supply chain compromise can defeat every node-level control in this appendix; it must be modeled explicitly.

---

## Section 4 — Key Compromise Incident Response Template

Use this template when a KEK compromise is detected or suspected. Triggers include stolen device, reported credential leak, and anomalous access patterns in the audit log. Do not wait for confirmation before starting the re-keying procedure — a suspected compromise is sufficient to begin.

### Detection Checklist

Run through this list whenever an employee reports a security event:

- [ ] Physical loss or theft reported by employee
- [ ] Anomalous access pattern flagged in audit log (off-hours access, unusual volume, unfamiliar source IP)
- [ ] Employee reports credentials as potentially compromised
- [ ] Security team identifies device in threat intelligence feed
- [ ] IdP reports failed authentication attempts against the affected account
- [ ] Employee is terminated or resigns (proactive revocation, not reactive)
- [ ] Unplanned device shutdown during sync operation in a region with unreliable grid power (Lagos, Karachi, parts of SE Asia). Distinguish from a security event: a node that resumes cleanly from WAL replay is an infrastructure failure; a node that cannot complete WAL replay, or that shows sync-daemon state inconsistent with the local database, should be treated as a potential security event until the sync mesh confirms consistency.
- [ ] Government authority or regulatory body presents a lawful access demand (subpoena, warrant, administrative order, inspection notice). Engage legal counsel before any response. The architectural response is specified in Chapter 15; the incident response below still applies to any credentials exposed during compliance with such orders.

Any checked item triggers the re-keying procedure below. Multiple checked items indicate elevated severity — consider notifying affected users immediately rather than waiting until the procedure is complete.

### Re-Keying Procedure

Execute these steps in order. Do not skip steps. Each step has a named owner and a completion condition.

| Step | Action | Owner | Completion condition |
|---|---|---|---|
| 1 | Generate new KEK for each affected role using cryptographically random key material. Do not derive from the compromised KEK. | Administrator | New KEK material exists in keystore; derivation from old KEK is not used |
| 1a | **Check old KEK availability before Step 2.** If the old KEK cannot be retrieved (device seized, device destroyed, keystore wiped, hardware failure of the KEK-holder's primary node), Step 2 cannot execute — the DEKs wrapped under the old KEK are permanently inaccessible without the KEK. Document the scope of unrecoverable data in the incident log. Proceed directly to Step 4 to broadcast revocation and prevent further compromise. Affected documents must be treated as lost; the team must decide whether to reconstruct them from BYOC backup (Chapter 16) or accept the loss. | Administrator | Recovery status documented in incident log; team has decided on reconstruction-from-backup or accepted-loss path |
| 2 | For each document in the affected role's scope (where the old KEK is available): decrypt the existing wrapped DEK using the old KEK, re-encrypt (wrap) with the new KEK, store alongside ciphertext. | Administrator | All recoverable DEKs in scope are re-wrapped; no document references the old KEK |
| 3 | Discard the old KEK and all node-level copies. Verify deletion with OS keystore audit. | Administrator | Keystore audit confirms old KEK is absent from all managed nodes |
| 4 | Broadcast revocation through the relay. All active nodes receive `ERR_KEY_REVOKED` on next handshake. | Administrator | Revocation broadcast confirmed; relay acknowledges |
| 5 | Any node holding the revoked key that attempts to reconnect receives `ERR_KEY_REVOKED` and must re-authenticate with IdP. | System (automatic) | Monitor relay logs for unexpected successful handshakes post-revocation |
| 6 | Notify all team members in the affected role. Include the KEK creation date, the revocation date, and the scope of potentially accessible data. | Administrator | All affected users notified; notification logged with timestamp |
| 7 | Issue new wrapped KEK copies to all current authorized members of the affected role via the standard key distribution path. | Administrator | All authorized members can sync; no member has access to old KEK |

### Data-at-Risk Scope Calculation

- **Start date:** Date the compromised KEK was created. Check the keystore creation timestamp — do not rely on employee recollection.
- **End date:** Date the revocation broadcast was confirmed at the relay.
- **Scope:** All documents that the compromised KEK protected between the start date and the end date.
- **Excluded from scope:** Documents in roles not protected by the compromised KEK. Documents created after the revocation date (these use the new KEK).

### User Notification Template

Send this message to every team member in the affected role. Adjust the bracketed fields:

> A security event affected [role name] credentials on [date]. We have issued new credentials and revoked the previous ones.
>
> Documents in [role name] between [start date] and [end date] may have been accessible to an unauthorized party. All documents created after [end date] are protected under the new credentials.
>
> Sign in again to continue syncing. Your data is intact; this step updates your access credentials only.
>
> Contact [IT contact name] at [IT contact email or phone] with questions.

**Logging requirement — retention floor:** Record the timestamp of each notification, the channel used (email, SMS, in-app), and the recipient. Retain this record for a minimum of 90 days. This is an audit-log retention floor, not a breach notification deadline.

**Breach notification deadlines — separate and faster.** Retention and notification are distinct obligations. The deadlines below are notification-to-regulator (and in some cases notification-to-affected-data-subjects) windows, which run from the moment the organization becomes aware of the breach. Verify the jurisdiction-specific window before setting an incident response SLA:

| Jurisdiction | Notification to supervisor | Notification to data subjects |
|---|---|---|
| EU (GDPR Article 33–34) | 72 hours | "without undue delay" when high-risk |
| UK (UK GDPR) | 72 hours | as GDPR |
| Brazil (LGPD) | "reasonable time" per ANPD guidance | as required by risk |
| China (PIPL Article 57) | Within 3 working days to CAC | "without undue delay" |
| Japan (PIPA Article 26) | "promptly" to PPC | "promptly" |
| South Korea (PIPA) | Within 24 hours for large breaches | "without delay" |
| India (DPDP Act Section 8) | As prescribed by Data Protection Board | As prescribed |
| UAE (DPL 2022) | 72 hours for high-risk | As directed |
| Russia (242-FZ + 152-FZ) | Within 24 hours initial, 72 hours supplementary | As required |
| Nigeria (NDPR) | Within 72 hours | "expeditiously" |
| South Africa (POPIA) | "as soon as reasonably possible" to the Regulator | "as soon as reasonably possible" |
| USA (HIPAA) | 60 days from discovery for reportable breaches | 60 days |
| USA (state laws — CCPA, etc.) | Varies | Varies |

Verify the jurisdictional obligations for every market the team operates in before the first incident occurs. The retention floor above is an audit control; the table above is the incident SLA.

---

*These worksheets are deployment tools, not compliance documentation. They do not substitute for a qualified security assessment in regulated environments. Engage a qualified assessor who can evaluate the full deployment against the applicable control frameworks before relying on the outputs of this appendix for regulatory representation.*

*Applicable regulatory frameworks by region (non-exhaustive):*

- *North America: HIPAA, ITAR, FedRAMP, SOC 2, CMMC, CCPA, PIPEDA*
- *European Economic Area / UK: GDPR (Article 33 — 72-hour supervisor notification; Article 34 — affected-party notification when high-risk), UK GDPR, Schrems II (case C-311/18 — data-transfer compliance driver), BSI TR-02102 and BSI C5 (Germany)*
- *GCC: UAE Federal Data Protection Law 2022, DIFC Data Protection Law 2020, Saudi Arabia Personal Data Protection Law*
- *South Asia: India Digital Personal Data Protection Act 2023 (DPDP), RBI data localization circular (BFSI), Bangladesh DPA*
- *East Asia / APAC: China PIPL (2021), Japan PIPA (revised 2022), South Korea PIPA + ISMS-P certification, Taiwan PDPA, Singapore PDPA*
- *Africa: Nigeria NDPR (2019, re-enacted 2023), South Africa POPIA (2021), Kenya Data Protection Act 2019, Ghana DPA 2012, ECOWAS Supplementary Act on Personal Data Protection*
- *Latin America: Brazil LGPD, Mexico LFPDPPP, Colombia Ley 1581, Argentina Ley 25.326*
- *CIS: Federal Law 242-FZ (Russia, data localization), Federal Law 152-FZ (Russia, personal data), Kazakhstan Law on Personal Data, Belarus Law on Information, import substitution procurement mandates (импортозамещение) for public-sector and critical-infrastructure deployments*

*For each jurisdiction the team operates in, validate the breach notification window, the retention floor, the regulatory inspection rights, and the cross-border data transfer rules before the first production deployment. The 72-hour GDPR window is the shortest common denominator; plan incident response against the shortest applicable window, not the longest.*
