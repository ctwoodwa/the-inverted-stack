# Appendix B — Threat Model Worksheets

<!-- icm/draft -->

<!-- Target: ~1,800 words -->
<!-- Source: v13 §11.1, Ch 15 -->

---

## Introduction

This appendix provides ready-to-use worksheets for building a deployment-specific threat model for an inverted-stack system. Chapter 15 describes the full security architecture — the four defensive layers, the DEK/KEK key hierarchy, the role attestation flow, and the key compromise incident response procedure. These worksheets operationalize that architecture. Fill them in before your first production deployment, update them when the asset inventory changes, and use the incident response template whenever a key compromise is detected or suspected.

---

## Section 1 — Asset Inventory Template

Fill this table before starting the threat model exercise. Every row represents an asset that, if compromised, lost, or corrupted, would cause material harm to the team or to individual users. Add rows for domain-specific assets. Adjust sensitivity ratings based on regulatory requirements (HIPAA, SOX, ITAR, and similar frameworks impose mandatory minimum classifications).

| Asset | Classification | Location | Owner | Sensitivity |
|---|---|---|---|---|
| User CRDT documents | Team-confidential | Local SQLCipher DB (per node) | User | High |
| Role KEKs | Team-secret | OS keystore (per node) | Team admin | Critical |
| Data Encryption Keys (DEKs) | Team-secret | Alongside ciphertext in SQLCipher | System | Critical |
| Device keypairs (Ed25519) | Node-secret | OS keystore (per node) | System | Critical |
| Attestation bundles | Team-internal | Local node; relay for catch-up | System | High |
| Sync operation log | Team-confidential | Local SQLCipher DB (per node) | Team | High |
| Relay ciphertext cache | Encrypted | Relay (operator-managed) | Operator | Medium (ciphertext only) |
| MDM configuration | Internal | MDM system; node-config.json on endpoint | IT admin | Medium |

**Customization guidance:** Add domain-specific rows. Adjust sensitivity ratings to match regulatory requirements — HIPAA-covered entities must treat patient identifiers as Critical.

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

List every actor who might interact with your system, including adversarial interactions. Include actors who currently have no access — they represent the baseline threat that the encryption boundary must hold against. For each actor, record the realistic motivation and the capability level you must plan for.

| Actor | Access level | Likely motivation | Capability level |
|---|---|---|---|
| External attacker (remote) | None initially | Data theft, ransomware | Low to High |
| External attacker (physical access) | Physical device access | Credential theft, storage extraction | Medium |
| Malicious insider (role access) | Team member with authorized role | Data exfiltration within role scope | Medium |
| Compromised relay operator | Transport layer (ciphertext) | Traffic analysis, availability attack | Limited (no plaintext) |
| Former team member (post-revocation) | None after rotation | Verify revocation completeness | Low (blocked by key rotation) |
| Supply chain attacker | Build pipeline | Backdoor via malicious package or binary | High if signing key compromised |

**Customization guidance:** Add actors specific to your vertical. Healthcare deployments should add "unauthorized staff member with workstation access" and "patient with provider relationship." Legal deployments should add "opposing counsel seeking discovery advantage." Government and defense deployments should add nation-state actors and insider threat programs as distinct entries with appropriate capability levels.

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
2. **Disk encryption check.** If BitLocker is not enforced via MDM policy, the attacker can read the filesystem directly. Mitigation: enforce BitLocker via MDM; verify that node-config.json specifies `storageEncryption: required`.
3. **Disk encryption is active.** Attacker reads the SQLCipher database file. Without the SQLCipher passphrase, the database is ciphertext. Attack fails at this branch.
4. **Device is powered on at time of theft.** Cold-boot attack window applies. See Ch 15 §7 for the in-memory key handling policy. The sync daemon zeroes key material after each operation; the window is seconds, not minutes. Realistic cold-boot attack requires lab conditions; treat as residual risk, not primary threat.
5. **Attacker targets OS keychain.** The role KEK and device keypair are stored in the Windows Credential Manager. Accessing them requires the device PIN or biometric. An attacker without the credential cannot extract key material from a locked device. Mitigation: enforce 6-digit minimum PIN via MDM. Disable USB boot and BIOS settings changes.
6. **Attacker copies SQLCipher DB offline.** Without the KEK and the SQLCipher passphrase, the ciphertext is unreadable. Attack fails.

**Residual risk: communication pattern analysis.** The relay operator cannot read document content — all sync payloads are encrypted before leaving the node. However, the operator can observe which nodes are active and when. In a five-person team, heavy sync activity between the project manager node and the estimator node in the 72 hours before a bid deadline reveals that an active bid is in preparation. The content is protected; the fact of activity is not.

**Mitigation for residual risk:** Deploy a self-hosted relay for projects with high competitive sensitivity. Self-hosted relay moves the traffic analysis capability from an external operator to internal IT, which is inside your trust boundary. See Ch 15 for relay deployment options.

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

Any checked item triggers the re-keying procedure below. Multiple checked items indicate elevated severity — consider notifying affected users immediately rather than waiting until the procedure is complete.

### Re-Keying Procedure

Execute these steps in order. Do not skip steps. Each step has a named owner and a completion condition.

| Step | Action | Owner | Completion condition |
|---|---|---|---|
| 1 | Generate new KEK for each affected role using cryptographically random key material. Do not derive from the compromised KEK. | Administrator | New KEK material exists in keystore; derivation from old KEK is not used |
| 2 | For each document in the affected role's scope: decrypt the existing wrapped DEK using the old KEK, re-encrypt (wrap) with the new KEK, store alongside ciphertext. | Administrator | All DEKs in scope are re-wrapped; no document references the old KEK |
| 3 | Discard the old KEK and all node-level copies. Verify deletion with OS keystore audit. | Administrator | Keystore audit confirms old KEK is absent from all managed nodes |
| 4 | Broadcast revocation through the relay. All active nodes receive `ERR_KEY_REVOKED` on next handshake. | Administrator | Revocation broadcast confirmed; relay acknowledges |
| 5 | Any node holding the revoked key that attempts to reconnect receives `ERR_KEY_REVOKED` and must re-authenticate with IdP. | System (automatic) | Monitor relay logs for unexpected successful handshakes post-revocation |
| 6 | Notify all team members in the affected role. Include the KEK creation date, the revocation date, and the scope of potentially accessible data. | Administrator | All affected users notified; notification logged with timestamp |
| 7 | Issue new wrapped KEK copies to all current authorized members of the affected role via the standard key distribution path. | Administrator | All authorized members can sync; no member has access to old KEK |

### Data-at-Risk Scope Calculation

- **Start date:** Date the compromised KEK was created. Check the keystore creation timestamp — do not rely on employee recollection.
- **End date:** Date the revocation broadcast was confirmed at the relay.
- **Scope:** All documents in roles protected by the compromised KEK during the window between start date and end date.
- **Excluded from scope:** Documents in roles not protected by the compromised KEK. Documents created after the revocation date (these use the new KEK).

### User Notification Template

Send this message to every team member in the affected role. Adjust the bracketed fields:

> Your access credentials for [team name] have been updated following a security event.
>
> Documents in [role name] from [start date] to [end date] may have been accessible to an unauthorized party. All documents created after [end date] are protected under new credentials.
>
> Please sign in again to continue syncing. Your data remains intact — this step updates your access credentials only.
>
> Contact [IT contact name] at [IT contact email or phone] if you have questions or concerns.

**Logging requirement:** Record the timestamp of each notification, the channel used (email, SMS, in-app), and the recipient. Retain this record for a minimum of 90 days. Regulated industries may require longer retention — check applicable requirements before setting the retention period.

---

*These worksheets are deployment tools, not compliance documentation. They do not substitute for a qualified security assessment in regulated environments. For HIPAA, ITAR, FedRAMP, or SOC 2 contexts, engage a qualified assessor who can evaluate the full deployment against applicable control frameworks.*
