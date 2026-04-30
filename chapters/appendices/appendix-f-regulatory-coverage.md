# Appendix F — Regulatory Coverage Map

<!-- icm/draft -->
<!-- Target: ~2,000 words -->

---

This appendix consolidates every regulatory framework the book references. Practitioners deploying local-first architecture across multiple jurisdictions need a single place to check what each regime requires, where that requirement creates a structural argument for on-device residency, and which chapters develop the argument. Entries are practitioner-focused: each describes the deployment relevance, not the statutory text. This appendix is not legal advice — production deployments require jurisdiction-specific counsel.

Frameworks are grouped by region. Each entry gives: framework name and citation; effective date; data-residency, consent, or access-rights properties that bear on local-first architecture; chapters where the compliance argument appears. The four load-bearing entries — GDPR, Schrems II, DIFC DPL 2020, and Russia's Federal Law 242-FZ — receive fuller treatment because the book's structural compliance arguments pivot on them. All other entries are intentionally terse.

---

## Europe

### GDPR (Regulation (EU) 2016/679)

**Effective:** 25 May 2018.

The foundational EU data-residency and individual-rights regime. Article 5(1)(c) (data minimization) and Article 5(1)(e) (storage limitation) create architectural pressure toward bounded local storage. Article 17 (right to erasure) is the book's most significant unresolved tension: CRDTs retain full operation history by design; DEK destruction (crypto-shredding, Chapter 15) is the proposed erasure mechanism, but CNIL in France and several German DPAs have not definitively resolved whether it constitutes lawful Article 17 compliance — the question is unsettled, not foreclosed. Article 30 (records of processing) and Article 33 (72-hour breach notification) operate at the node level. Article 44 restricts transfers to third countries lacking adequacy.

**Chapters:** Preface, Ch02–Ch07, Ch09–Ch11, Ch13–Ch15, Ch18–Ch19, Ch22–Ch23, Epilogue, Appendix A, Appendix B, Appendix D

### Schrems II (*Data Protection Commissioner v. Facebook Ireland Limited and Maximillian Schrems*, CJEU C-311/18, 16 July 2020)

**Effective:** 16 July 2020 (Privacy Shield invalidated simultaneously).

The strongest European compliance argument for local-first. The CJEU ruled that Privacy Shield was invalid and that SCCs alone are insufficient where the importing country's surveillance laws preclude effective protection. A local-first node that never exports personal data to a foreign cloud bypasses the transfer mechanism entirely — Schrems II does not apply when there is no cross-border transfer to evaluate. The architecture answers the ruling structurally, not contractually.

**Chapters:** Preface, Ch02–Ch06, Ch09–Ch11, Ch13–Ch15, Ch18–Ch19, Ch23, Epilogue, Appendix D

### UK GDPR

**Effective:** 1 January 2021 (retained from EU GDPR, UK Data Protection Act 2018). Substantively mirrors EU GDPR. Article 17 erasure, Article 30 records, and transfer restrictions carry over. The EU–UK adequacy decision is maintained but subject to periodic review.

**Chapters:** Ch02, Appendix A

### Standard Contractual Clauses (SCCs) + Binding Corporate Rules (BCRs)

SCCs (updated 2021, Commission Decision C(2021) 3972) are the primary EU transfer mechanism to non-adequate countries; post-Schrems II they require supplemental Transfer Impact Assessments. BCRs (Article 47) cover intragroup transfers. A local-first architecture that maintains data on-device within the EEA reduces but does not eliminate SCC exposure.

**Chapters:** Ch02, Ch10, Ch23

### National DPAs: CNIL (France), German Datenschutzbehörden

Neither authority has definitively resolved whether DEK destruction constitutes lawful Article 17 erasure. The EDPB's supplementary-measures guidance (Guidelines 05/2021) is the operative framework for evaluating whether technical measures qualify as lawful transfer safeguards.

**Chapters:** Ch02, Ch06, Ch10, Ch22, Epilogue

---

## Middle East / GCC

### DIFC Data Protection Law 2020 (DIFC Law No. 5 of 2020)

**Effective:** 1 July 2020.

The most structurally decisive regime in this book's GCC arguments. The DIFC DPL uniquely *prohibits* foreign cloud storage for DIFC-licensed financial entities — not a constraint to satisfy contractually, but a categorical prohibition. A local-first node that never routes personal data through an offshore cloud satisfies this prohibition at the architectural level. Chapter 4 develops the argument; Chapter 14 addresses the compelled-access threat model in the DIFC context.

**Chapters:** Preface, Ch02–Ch06, Ch09–Ch11, Ch13–Ch15, Ch18–Ch19, Ch22–Ch23, Epilogue, Appendix D

### UAE Federal Data Protection Law 2022 (Federal Decree-Law No. 45 of 2021, effective 2 January 2022)

Establishes data processing principles, consent requirements, and erasure rights (Article 16) for UAE federal and private-sector processing outside DIFC/ADGM. Article 16 carries the same crypto-shredding tension as GDPR Article 17.

**Chapters:** Preface, Ch02–Ch05, Ch11, Ch13, Ch19, Ch22, Epilogue

### Saudi PDPL (Royal Decree M/19, 2021)

**Effective:** Phased from 2023; implementers should verify current enforcement with local counsel. Establishes data subject rights and cross-border transfer restrictions comparable to UAE DPL. Sensitive-data localization creates strong architectural pressure.

**Chapters:** Ch02, Ch04

---

## South Asia

### India DPDP Act 2023 (Digital Personal Data Protection Act, No. 22 of 2023)

**Effective:** Notified August 2023; implementing rules pending as of this writing. Section 12 establishes erasure rights parallel to GDPR Article 17. For BFSI deployments, the RBI circular (below) layers a hard localization mandate on top.

**Chapters:** Preface, Ch02–Ch06, Ch09, Ch11, Ch13–Ch15, Ch18–Ch19, Ch22–Ch23, Epilogue, Appendix A, Appendix D

### RBI Data Localization Circular (April 2018, DPSS.CO.OD No.2785)

**Effective:** October 2018 for payment system operators. Requires all payment-related data to be stored exclusively in India — a hard territorial mandate, not a design preference. Chapter 13 treats it as a Tier 3 architectural driver alongside 242-FZ and DIFC.

**Chapters:** Ch04–Ch06, Ch09, Ch11, Ch13–Ch14, Ch18, Ch23, Appendix D

### Bangladesh DPA

Dedicated legislation was in draft as of this writing. Implementers should verify current status with local counsel.

---

## East Asia / APAC

### China PIPL (Personal Information Protection Law, effective 1 November 2021) + MLPS 2.0 (effective 1 December 2019)

PIPL Article 47 establishes erasure rights parallel to GDPR Article 17. Cross-border transfer restrictions are among the strictest globally — personal data of Chinese residents must generally be stored within China. MLPS 2.0 adds a security classification and certification layer. Together they create one of the strongest architectural arguments for local-first in this roster.

**Chapters:** Ch02–Ch06, Ch08–Ch11, Ch13–Ch15, Ch18–Ch19, Ch22–Ch23, Epilogue, Appendix D

### Japan APPI / PIPA (revised 2022)

**Effective:** 1 April 2022 (revised). Article 34 (third-party restrictions), Article 36 (cross-border transfer consent). The 2022 revision strengthened transfer controls; Article 36 erasure-equivalent right carries the same CRDT/DEK-destruction tension.

**Chapters:** Preface, Ch02–Ch03, Ch05, Ch07–Ch11, Ch13–Ch15, Ch18–Ch19, Ch22–Ch23, Epilogue, Appendix A, Appendix D

### South Korea PIPA + ISMS-P

Strong erasure rights; ISMS-P is a procurement-required certification standard in Korean enterprise procurement. Chapter 8 treats it alongside SOC 2 and ISO 27001 as documentation the local-first vendor must produce.

**Chapters:** Preface, Ch02–Ch03, Ch05, Ch08–Ch11, Ch13–Ch14, Ch18–Ch19, Ch22–Ch23, Epilogue, Appendix A, Appendix D

### Taiwan PDPA / Singapore PDPA

Both establish cross-border transfer controls and data subject rights. Relevant for APAC regional deployments. Implementers should verify current amendments with local counsel.

**Chapters:** Ch02, Ch04

---

## Africa

### Nigeria NDPR (2019) / Nigeria Data Protection Act 2023 (NDPA)

The NDPA (Act No. 40 of 2023) re-enacted and strengthened NDPR, establishing a dedicated Data Protection Commission. Erasure rights parallel GDPR Article 17. Sectoral regulators in BFSI and telecom compound NDPA requirements with additional localization obligations.

**Chapters:** Preface, Ch02–Ch03, Ch05, Ch07–Ch11, Ch13, Ch15, Ch18–Ch19, Ch22–Ch23, Epilogue, Appendix A, Appendix D

### South Africa POPIA (Protection of Personal Information Act 4 of 2013, effective 1 July 2021)

Section 24 (right to correction and deletion). Section 72 prohibits cross-border transfers to countries lacking adequate protection — the same structural argument as GDPR for on-device residency.

**Chapters:** Preface, Ch02–Ch03, Ch05, Ch07–Ch11, Ch13, Ch15, Ch18–Ch19, Ch22–Ch23, Epilogue, Appendix A, Appendix D

### Kenya Data Protection Act 2019 (Act No. 24 of 2019)

**Effective:** November 2019. Section 40 (erasure rights). The ODPC has issued binding financial-sector guidance.

**Chapters:** Ch05, Ch07–Ch09, Ch11, Ch13, Ch15, Ch18–Ch19, Ch22, Appendix D

### Ghana DPA (Act 843 of 2012) / ECOWAS Supplementary Act (A/SA.1/01/10, 2010)

Ghana's DPA is one of Africa's earliest; the ECOWAS Act provides a common floor for 15 member states. Implementers should verify current enforcement with local counsel.

**Chapters:** Ch02

---

## Americas

### Brazil LGPD (Lei 13.709/2018, effective September 2020)

Article 18 establishes erasure rights parallel to GDPR Article 17. The ANPD has not yet settled whether crypto-shredding constitutes lawful erasure.

**Chapters:** Ch02–Ch03, Ch05, Ch07, Ch09–Ch11, Ch13–Ch15, Ch18, Ch22, Epilogue

### Mexico LFPDPPP (2010) — ARCO Rights

Cancellation right (the ARCO "C") parallels GDPR Article 17. Data localization requirements are sector-specific.

**Chapters:** Ch02, Ch07, Ch09, Ch11, Ch15, Ch22

### Colombia Ley 1581 (2012) / Argentina Ley 25.326 (2000) / Canada PIPEDA

Each establishes data subject rights including deletion. Argentina has EU adequacy status. Canada's PIPEDA is pending replacement by Bill C-27/CPPA as of this writing.

**Chapters:** Ch02

### United States — Sector-Specific Frameworks

No omnibus federal privacy law. The book addresses:

- **HIPAA** (1996): PHI handling and breach notification. Technical safeguards align well with on-device encryption. Ch02, Ch05, Ch08, Ch18.
- **FERPA / GLBA**: Student records and financial NPI, respectively. Referenced for completeness. Ch02.
- **ITAR / EAR**: Defense-related and dual-use technology export controls. Sovereign-deployment context. Ch02.
- **FedRAMP**: Federal cloud-service authorization. Enterprise procurement context. Ch02, Ch19.
- **SOC 2 / ISO 27001 / CMMC**: Procurement-threshold attestations, not regulatory obligations. Ch05, Ch08, Ch19.
- **CCPA / CPRA** (California, 2018/2020): Consumer data rights for California residents. Ch02.

---

## CIS / Eastern Europe

### Russia Federal Law 242-FZ (2015)

**Effective:** 1 September 2015 — enacted two years before GDPR and the earliest major national localization mandate. 242-FZ amended Federal Law 152-FZ to require that personal data of Russian citizens be initially collected and stored on servers physically located in Russia. The book repeatedly emphasizes this chronology: Russia established the doctrinal pattern of hard localization mandates before Europe's rights-based framework took effect. A local-first node within Russia satisfies 242-FZ at the architectural level — the same structural answer as Schrems II, but with a harder territorial requirement. Roskomnadzor enforcement has intensified since 2022.

**Chapters:** Ch02–Ch06, Ch09, Ch11, Ch13–Ch15, Ch18–Ch19, Ch23, Epilogue

### Russia Federal Law 152-FZ (2006, as amended) / Federal Law 188-FZ (2015)

152-FZ is the parent omnibus personal data statute; 242-FZ is the localization amendment that drives the book's argument. 188-FZ governs state procurement preference for domestic software.

**Chapters:** Ch02, Ch14

### Импортозамещение (Import Substitution Policy)

Russian state policy mandating preference for domestically-produced software in government and state-adjacent procurement. Not a data protection law — a market-access requirement. State-sector enterprises face formal procurement barriers against Western SaaS products that do not apply to locally-deployed on-device software. A local-first node built on domestically-licensed components can qualify for state procurement in ways that a cloud-resident SaaS cannot. Import substitution thereafter.

**Chapters:** Ch02, Ch05, Ch09, Ch19

### Kazakhstan Law on Personal Data / Belarus Law on Information

Both establish data localization obligations for citizens' personal data. Implementers should verify current scope with local counsel.

**Chapters:** Ch02

---

## Cross-Cutting Frameworks

### ISO/IEC 27701, SOC 2, ISMS-P (Korea), ENS (Spain)

Certification and attestation standards, not laws. The book treats them as procurement thresholds — evidence artifacts the local-first vendor produces to satisfy enterprise procurement. Chapter 8 and Chapter 19 develop the compliance-packaging argument.

---

## Per-Chapter Index

Reverse index showing frameworks each compressed chapter originally cited inline. Used by reviewers and the reference-integrity script (`build/check_audit.py`). Chapters not yet through HIGH-tier compression (Ch01, Ch16, Ch20, and MED-tier paragraphs in Ch07 and Ch10) are omitted — their inline citations remain in the chapter text and will be added here during the MED-tier pass. Appendix B ¶56 and Ch12 ¶61 (retained as structured lists) are included for completeness.

| Chapter | Frameworks cited |
|---|---|
| Preface | GDPR, Schrems II, UAE DPL, DIFC DPL, DPDP, Japan APPI/PIPA, South Korea PIPA, POPIA, NDPR |
| Ch02 | GDPR, UK GDPR, Schrems II, CNIL, BSI, UAE DPL, DIFC DPL, Saudi PDPL, DPDP, RBI, Bangladesh DPA, PIPL, MLPS 2.0, Japan APPI/PIPA, South Korea PIPA+ISMS-P, Taiwan PDPA, Singapore PDPA, NDPR, POPIA, Kenya DPA, Ghana DPA, ECOWAS Act, LGPD, LFPDPPP, Ley 1581, Ley 25.326, PIPEDA, HIPAA, FERPA, GLBA, ITAR, FedRAMP, CMMC, CCPA/CPRA, Russia 242-FZ, 152-FZ, Kazakhstan, Belarus, SCCs |
| Ch03 | GDPR, Schrems II, PIPL, DPDP, Russia 242-FZ, UAE DPL, DIFC DPL, Japan APPI/PIPA, South Korea PIPA, LGPD, POPIA, NDPR |
| Ch04 | GDPR, Schrems II, DIFC DPL, UAE DPL, Saudi PDPL, DPDP, RBI, Taiwan PDPA, Singapore PDPA, PIPL, Japan APPI/PIPA, South Korea PIPA, LGPD, LFPDPPP, Ley 1581, Ley 25.326, POPIA, NDPR, Kenya DPA, Russia 242-FZ |
| Ch05 | GDPR Art. 33, HIPAA, DPDP, Japan APPI/PIPA, PIPL, NDPR, POPIA, LGPD, Russia 242-FZ, Schrems II, DIFC DPL, UAE DPL, RBI, Kenya DPA, LFPDPPP, SOC 2, ISMS-P |
| Ch06 | GDPR, Schrems II, EDPB, CNIL, DPDP, RBI, PIPL, DIFC DPL, UAE DPL, Japan APPI/PIPA, South Korea PIPA, LGPD, POPIA, NDPR, Russia 242-FZ |
| Ch07 | GDPR Art. 17, DPDP, LGPD, POPIA, NDPR, Kenya DPA, LFPDPPP, Japan APPI, South Korea PIPA |
| Ch08 | GDPR, Schrems II, SOC 2, ISO 27001, HIPAA, DIFC DPL, DPDP, PIPL, Japan APPI/PIPA, South Korea ISMS-P, NDPR, POPIA, Kenya DPA, Russia 242-FZ |
| Ch09 | GDPR, Schrems II, DPDP, RBI, DIFC DPL, Russia 242-FZ, 188-FZ/import substitution, PIPL, Japan APPI/PIPA, South Korea PIPA, LGPD, LFPDPPP, POPIA, NDPR, Kenya DPA |
| Ch10 | GDPR Art. 17, LGPD Art. 18, POPIA Sec. 24, NDPR, Kenya DPA, DPDP, Japan APPI/PIPA, South Korea PIPA, PIPL, EDPB, Schrems II, DIFC DPL, Russia 242-FZ, SCCs |
| Ch11 | GDPR, Schrems II, DIFC DPL, Russia 242-FZ, PIPL, Japan APPI/PIPA, DPDP, RBI, LGPD, LFPDPPP, POPIA, NDPR, Kenya DPA |
| Appendix B | GDPR, Schrems II, PIPL, MLPS 2.0, Russia 242-FZ, DIFC DPL, DPDP, RBI, Japan APPI/PIPA, South Korea PIPA+ISMS-P, LGPD, POPIA, NDPR (inline list retained) |
| Ch12 | GDPR, Schrems II, PIPL, Russia 242-FZ, DIFC DPL, DPDP, RBI, Japan APPI/PIPA, South Korea PIPA, POPIA, NDPR (inline list retained) |
| Ch13 | GDPR, UK GDPR, Schrems II, DIFC DPL, UAE DPL, DPDP, RBI, PIPL, Japan APPI/PIPA, South Korea PIPA, LGPD, Russia 242-FZ |
| Ch14 | GDPR Art. 5(1)(c)/(1)(e), Schrems II, DPDP, RBI, DIFC DPL, PIPL, Japan APPI/PIPA, South Korea PIPA, UAE DPL, LGPD, POPIA, NDPR, LFPDPPP, Russia 152-FZ/242-FZ |
| Ch15 | DIFC DPL, Schrems II, Russia 242-FZ (architectural compliance: foreign-cloud prohibition, transfer architecture, localization) |
| Ch22 | GDPR Art. 17, DPDP Sec. 12, UAE DPL Art. 16, LGPD Art. 18, LFPDPPP, POPIA Sec. 24, NDPR, Kenya DPA, Japan APPI Art. 36, South Korea PIPA, PIPL Art. 47, EDPB, CNIL (crypto-shredding via DEK destruction = key-lifecycle operation) |
| Ch23 | GDPR Art. 33, Schrems II, DIFC DPL, UAE DPL, DPDP, RBI, PIPL, Japan APPI/PIPA, South Korea PIPA+ISMS-P, NDPR, POPIA Sec. 72, LGPD, Russia 242-FZ, SCCs (endpoint controls, breach notification, multi-party transfer custody, sectoral localization) |
| Appendix D | GDPR, Schrems II, DIFC DPL, RBI, DPDP, PIPL, MLPS 2.0, Japan APPI/PIPA, South Korea PIPA+ISMS-P, LGPD, POPIA, NDPR |
| Ch18 | GDPR Art. 30, Schrems II, DIFC DPL, UAE DPL, DPDP, RBI, PIPL, Japan APPI, South Korea PIPA, LGPD, LFPDPPP, NDPR, POPIA, Kenya DPA, Russia 242-FZ |
| Ch19 | DIFC DPL, RBI, Schrems II, Russia 242-FZ, 188-FZ/import substitution, NDPR, POPIA, PIPL, Japan APPI, South Korea PIPA, LGPD, Kenya DPA, DPDP, FedRAMP, SOC 2, CMMC |
| Epilogue | GDPR Art. 17, Schrems II, DPDP Sec. 12, UAE DPL Art. 16, LGPD Art. 18, PIPL Art. 47, Japan APPI Art. 36, South Korea PIPA, POPIA, NDPR, Russia 242-FZ |

---

**This appendix is not legal advice. Readers building production deployments must engage qualified counsel for jurisdiction-specific compliance review.**
