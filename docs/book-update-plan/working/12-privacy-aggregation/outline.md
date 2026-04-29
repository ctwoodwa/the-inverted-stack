# 12 — Privacy-Preserving Aggregation at Relay — Outline

**ICM stage:** outline → ready for draft.
**Target chapter:** Ch15 (security architecture, Part III).
**Total word target:** 1,500 words.
**Source:** `docs/reference-implementation/design-decisions.md` §5 entry #12 (DP / k-anonymity at relay; smart-meter scenario). Composes with Ch15 §Relay Trust Model (already committed), §Forward Secrecy and Post-Compromise Security (#46), and §Endpoint Compromise (#47).

---

## §A. Overview and Motivation

The relay in this architecture is a ciphertext router: it cannot read payload content. What it can read is the *shape* of communication — which nodes connect, how often, how many operations they emit, and how those counts vary over time. §Relay Trust Model (already in Ch15) names this observation capability and prescribes a self-hosted relay for metadata-sensitive deployments. That prescription handles the *access* problem — a self-hosted relay eliminates third-party relay operators as metadata observers. It does not handle the *aggregation* problem: even the organization that hosts its own relay, or a multi-tenant managed-relay operator, may need to derive operational intelligence from the traffic it forwards — error rates, per-role sync latencies, fleet health counts — without creating a log that, if subpoenaed or breached, reveals individual behavior patterns with fine-grained precision.

Privacy-preserving aggregation is the mechanism that makes relay-side analytics safe to collect. The relay computes aggregate statistics — counts, rates, latency percentiles — with calibrated noise that satisfies a formal privacy guarantee. Any individual node's behavior becomes indistinguishable from its neighbors' in the reported aggregate. The organization retains operational intelligence; individual behavior is protected.

This section specifies three sub-patterns. They are ordered by the scope of the privacy question they answer and the cost of the mechanism they employ.

Sub-pattern **12a — Differential-privacy noise injection on relay-side aggregates.** The relay holds plaintext metadata even in an encrypted-payload architecture: operation counts, sync latency samples, error codes, connection durations. DP calibrates the noise added to these aggregates before they leave the relay tier. The result satisfies (ε, δ)-differential privacy: any two adjacent inputs — differing by one node's contribution — produce output distributions whose divergence is bounded by ε. The relay operator learns the aggregate pattern; no individual node's behavior is recoverable from the published statistic.

Sub-pattern **12b — k-anonymity floor for per-role aggregates.** Some relay-side queries partition statistics by role: "what is the error rate for Finance-role nodes?" If the Finance role has three members and one has a persistent error, the partition leaks that member's identity even with DP noise. The k-anonymity floor suppresses any per-partition aggregate computed over fewer than k nodes (recommended minimum k=10; regulated deployments k=50). Queries that fall below floor are either withheld, merged into a coarser partition, or returned with a suppression indicator. k-anonymity and DP compose: the floor gates which partitions DP noise is applied to.

Sub-pattern **12c — Privacy budget tracking across repeated queries.** DP composition is sequential and additive: running n queries over the same population consumes n × ε of total privacy budget. An operator who runs hourly sync-latency reports over a one-month window has run 720 queries. Without budget tracking, the composition theorem's guarantee degrades to near-nothing — the cumulative ε effectively collapses to no protection. Budget tracking makes the degradation visible and enforceable: the relay tracks each query's ε contribution, accumulates it over a configurable window (default: 30-day rolling), and gates new queries against the remaining budget. When the budget is exhausted, new queries are queued until the window rolls forward.

---

## §B. Sub-pattern Decomposition

### 12a — Differential-privacy noise injection (~600 words)

**What it covers.** DP noise calibrated to the Laplace mechanism (for pure ε-DP) or the Gaussian mechanism (for (ε, δ)-DP) applied to relay-side aggregate statistics: operation-count totals per time window, per-role sync latency distributions (reported as bucket counts, not raw samples), error-event counts per code per window, and connection-duration histograms. These are additive aggregates — the mechanisms defined by Dwork and Roth apply directly without requiring sensitivity analysis beyond simple counting queries.

**What it does not cover.** DP does not apply to the CRDT operation payload. The relay receives ciphertext; the architecture offers no DP mechanism for content because content never leaves encryption. DP applies exclusively to *metadata aggregates* that the relay computes as a side effect of routing. This distinction is the load-bearing one: readers who conflate "DP on data" with "DP on metadata" will misunderstand the threat model this section addresses.

**Local vs. central DP.** This architecture applies *central* DP at the relay tier, not local DP at the node tier. Each node reports raw sync events to the relay for delivery; the relay applies DP noise when it reports aggregated statistics to the operator dashboard or external monitoring system. Central DP produces lower noise for equivalent privacy guarantees because the noise is added once to the aggregate, not once per contributor. The trade-off is trust: the relay must be trusted to apply the noise faithfully. For self-hosted relays (the architecture's prescription for sensitive deployments), this trust is under organizational control. For managed-relay deployments, the relay operator's auditing posture determines whether central DP is credible; organizations without audit rights over the managed relay should consider local DP at the node tier as a defense-in-depth layer.

**Sensitivity and noise calibration.** The sensitivity of a count query is 1 (one node can change the count by at most 1). Laplace noise scale λ = sensitivity / ε = 1 / ε. For ε = 1.0 (a common operational baseline), λ = 1. For ε = 0.1 (strong protection), λ = 10 — ten times more noise, ten times more degraded utility. Regulated deployments choose ε based on the regulatory sensitivity of the counted attribute: connection frequency for a healthcare-team node is more sensitive than sync latency for a logistics-team node.

**Relationship to forward secrecy (#46).** Forward secrecy hides session-key content from a relay that records ciphertext. DP hides aggregate metadata patterns from a relay that records connection graphs. The two compose orthogonally: #46 protects payload confidentiality over time; #12a protects behavioral metadata in the aggregate. Implementing both is not redundant; neither alone closes the other's gap.

**Target word budget: ~600 words.**

### 12b — k-anonymity floor for per-role aggregates (~350 words)

**What it covers.** A suppression policy applied to any per-partition aggregate where the contributing-node count is below k. Suppression options: withhold the query result entirely (safest), merge the partition into a parent partition (e.g., merge "Finance-EMEA" into "Finance"), or return a synthetic "below minimum cohort size" indicator. The policy is declared in the relay configuration manifest; `Sunfish.Kernel.Sync` enforces it at the query evaluation layer.

**Practical floor values.** k=10 is the de facto minimum in applied privacy literature for operational telemetry. For deployments where a role may have 3-5 members (common in early-stage enterprise deployments), k=10 means many per-role statistics are permanently suppressed — the floor may need to be set at k=3 with augmented DP noise to compensate for the weaker anonymity bound. Regulated deployments (HIPAA, GDPR Article 25 data minimization) use k=50 as a reasonable high-water mark consistent with healthcare privacy research norms.

**Interaction with #48 (key-loss recovery).** Recovery-event counts are among the most sensitive relay-side statistics: a per-user recovery event is a unique event that may expose a compromised device before the user has detected the compromise. The k-anonymity floor applies to recovery-event counts with special handling — even if the cohort exceeds k, the relay suppresses the recovery-event partition unless the operator has explicit audit rights. This is a named carve-out, not a general rule.

**Target word budget: ~350 words.**

### 12c — Privacy budget tracking across repeated queries (~350 words)

**What it covers.** A sequential composition budget maintained per query type and per observation window. Each query consumes an ε allocation from the window's total budget (operator-configured; default Σε = 10.0 over 30 days for standard operational telemetry). When cumulative ε for a query type within the window reaches 80% of its allocation, the relay surfaces a budget-warning event. At 100%, new queries of that type are queued until the window advances.

**Why sequential composition matters for sync telemetry.** Sync telemetry is inherently time-series: the operator runs the same latency-histogram query every hour. The basic sequential composition theorem (Dwork and Roth §3.5) states that k applications of ε-DP mechanisms yield kε-DP total. An operator running hourly latency histograms with ε = 0.1 per query accumulates ε = 72 over 30 days — well into the range where the DP guarantee is practically meaningless. Budget tracking makes this degradation explicit and enforceable rather than implicit.

**Advanced composition.** For deployments that run many distinct query types, the advanced composition theorem (Dwork, Rothblum, and Vadhan) gives tighter budget bounds than simple sequential addition. The relay can expose a budget-configuration knob that selects between simple and advanced composition accounting; the default is simple (more conservative, no additional computational overhead).

**Integration with #47 (endpoint compromise).** An endpoint-compromise incident triggers a burst of unusual relay events: rapid reconnection attempts, anomalous operation counts, atypical latency profiles. DP noise on these counts may mask the forensic signal the operator needs to detect and scope the incident. The recommended approach is a named incident-response mode that temporarily suspends DP aggregation for the affected node's metrics — recording raw events into a separate operator-controlled audit log — and resumes DP after the incident is closed. The temporary suspension is itself a signed event in `Sunfish.Kernel.Audit`, maintaining the audit trail for the suspension period.

**Target word budget: ~350 words.**

---

## §C. Insertion Point in Ch15

**Insert after:** `## Relay Trust Model`
**Insert before:** `## Security Properties Summary`

**Rationale.** §Relay Trust Model (already committed) closes its discussion by naming traffic-analysis resistance as a known gap: "The current architecture does not implement constant-rate padding between nodes. Organizations whose threat model includes traffic analysis by a well-resourced adversary replace the relay with application-layer obfuscation or route it behind a mixnet. The architecture documents the limitation; the mitigation is an operator deployment choice outside the scope of `Sunfish.Kernel.Security`."

Privacy-preserving aggregation is the complement to that statement. Traffic analysis resistance addresses passive real-time observation of the relay traffic stream. DP aggregation addresses the relay operator's own derived analytics — the statistics the operator legitimately computes and retains. The two threats are distinct; they share the same relay tier as their observation point. §Privacy-Preserving Aggregation at Relay placed immediately after §Relay Trust Model follows the same "you've learned what the relay can observe; here's the mitigation" narrative arc that makes the Relay Trust Model section navigable.

Placing it before §Security Properties Summary ensures the summary table can incorporate the new guarantee row without requiring a retroactive edit. The summary should gain one row: `Metadata minimization | Relay-side aggregates satisfy (ε, δ)-differential privacy with k-anonymity floor; raw operation metadata is never retained longer than the budget window | DP noise injection + k-floor suppression + rolling budget gate in Sunfish.Kernel.Sync`.

**Neighboring section relationships:**

- **Before (#46 §Forward Secrecy):** Not adjacent. §Forward Secrecy is earlier in Ch15. Reference it within §12a to establish orthogonality.
- **Before (§Relay Trust Model):** Immediate predecessor. §12a's "central vs. local DP" discussion explicitly extends §Relay Trust Model's "self-hosted relay as metadata mitigation" argument — same threat actor, different attack vector.
- **After (§Security Properties Summary):** Immediate successor. The summary gains a metadata-minimization property row citing the DP + k-floor mechanism.

---

## §D. Sunfish Package Decisions

**Primary package: `Sunfish.Kernel.Sync`** (already in canon).

Rationale: the relay's routing and session logic lives in `Sunfish.Kernel.Sync`. DP noise injection on routing-derived aggregates, the k-anonymity floor enforcement, and the budget gate are all relay-tier operations — they occur in the sync layer, not the security key-management layer. Extending `Sunfish.Kernel.Sync` keeps the metadata-privacy machinery co-located with the metadata it operates on.

No new top-level Sunfish namespace is introduced. The implementation surfaces (noise injector, k-floor evaluator, budget tracker) are described by name only as components within `Sunfish.Kernel.Sync`. They carry the standard pre-1.0 illustrative marker.

**Secondary reference: `Sunfish.Kernel.Audit`** (forward-looking from #48; in canon for this book).

The incident-response suspension mode (§12c) emits a signed event into `Sunfish.Kernel.Audit` when DP is temporarily suspended for a compromised node's metrics. The reference is read-only from this section's perspective — the audit substrate is already specified by #48 and #47; this section adds an event type to the taxonomy it defines.

**No new package needed.** The privacy-aggregation functionality does not warrant a Foundation-tier package (that tier is for user-facing orchestration, not relay-internal policy enforcement). Do not introduce `Sunfish.Foundation.Privacy` or `Sunfish.Kernel.Privacy` — the naming would over-promise a scope this section does not deliver. Mark any illustrative component names within `Sunfish.Kernel.Sync` as forward-looking per the pre-1.0 policy.

---

## §E. Citations Needed

Extension #9 (chain-of-custody) precedes #12 in the pipeline and will consume approximately 4 citations ([28]–[31], continuing from [27] already in Ch15). Extension #12 therefore targets **[32]–[36]** as its citation range. The exact starting number will be confirmed when #9's draft lands; adjust numbers accordingly.

All five citations below are required for the section's technical claims. None can be derived from v13/v5 source papers (which contain no DP-specific content).

**[32] Dwork, C. and Roth, A.** — *The Algorithmic Foundations of Differential Privacy*, Foundations and Trends in Theoretical Computer Science, vol. 9, no. 3-4, pp. 211–487, 2014. Available: https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf

Use for: §12a formal definition of (ε, δ)-differential privacy; Laplace and Gaussian mechanism; §12c sequential composition theorem reference (this monograph is the standard citation for both).

**[33] Erlingsson, Ú., Pihur, V., and Korolova, A.** — "RAPPOR: Randomized Aggregatable Privacy-Preserving Ordinal Response," in *Proc. ACM Conference on Computer and Communications Security (CCS)*, Scottsdale, Nov. 2014. Available: https://dl.acm.org/doi/10.1145/2660267.2660348

Use for: §12a discussion of local vs. central DP — RAPPOR is the canonical local-DP telemetry deployment (Google's Chrome browser); naming it establishes that the architecture chose *central* DP at the relay (not local DP at each node) deliberately, and why.

**[34] Apple Inc.** — "Learning with Privacy at Scale," Apple Machine Learning Research, 2017. Available: https://docs-assets.developer.apple.com/ml-research/papers/learning-with-privacy-at-scale.pdf

Use for: §12a as a second real-world central-DP deployment example alongside RAPPOR. Apple's deployment illustrates the ε budget choices, utility tradeoffs, and the practical scale at which central DP produces useful aggregates — the same parameters that govern the relay-side deployment in this architecture.

**[35] Sweeney, L.** — "k-Anonymity: A Model for Protecting Privacy," *International Journal on Uncertainty, Fuzziness and Knowledge-Based Systems*, vol. 10, no. 5, pp. 557–570, 2002. Available: https://dl.acm.org/doi/10.1142/S0218488502001648

Use for: §12b k-anonymity floor definition, suppression policy, and the "k=10 minimum cohort" practical guidance.

**[36] Machanavajjhala, A., Kifer, D., Gehrke, J., and Venkitasubramaniam, M.** — "l-Diversity: Privacy Beyond k-Anonymity," *ACM Transactions on Knowledge Discovery from Data*, vol. 1, no. 1, Mar. 2007. Available: https://dl.acm.org/doi/10.1145/1217299.1217302

Use for: §12b — name l-diversity as the extension to k-anonymity that handles the case where a per-role partition has k members but a single sensitive-attribute value dominates (e.g., all Finance-role nodes show the same error code). Flag as a note for regulated deployments that require l-diversity alongside k-anonymity.

**Citation not needed (CHARM):** No "CHARM Encrypted Aggregation" paper was found in literature search that is relevant to this section's scope. Homomorphic encryption approaches for smart-grid aggregation exist but the architecture does not propose homomorphic encryption at the relay; the section uses DP noise injection, which is computationally cheaper and sufficient for count/rate aggregates. Do not cite a homomorphic encryption source that misrepresents the mechanism choice.

**Citation note — advanced composition:** the advanced composition theorem is cited through Dwork and Roth [32] (the monograph covers it in §3.5). No additional citation is required for advanced composition unless the technical-reviewer determines the monograph reference is insufficient for the specific claim.

---

## §F. FAILED Conditions and Kill Trigger

**FAILED condition — cohort-too-small:** The k-anonymity floor gate FAILS when every per-role partition in the deployment contains fewer than k nodes. In this case, the floor suppresses all per-role statistics permanently, rendering the aggregation layer useless for operational intelligence. The deployment must either raise k (reducing protection) or accept that per-role statistics are unavailable until the team grows. No automatic fallback exists; the operator configures the policy explicitly.

**FAILED condition — budget exhaustion:** The DP budget gate FAILS when the rolling budget window is configured too small for the query frequency. An operator who configures Σε = 1.0 over 30 days and runs hourly queries (720 per window) exhausts the budget in the first hour. Subsequent queries are permanently queued for the remainder of the window. The correct mitigation is to configure budget and query frequency together at deployment time; the relay surfaces a budget-sizing recommendation based on declared query frequency.

**Kill trigger:** The privacy-aggregation primitive fails entirely — and must be disabled to prevent false confidence — when DP noise is applied to aggregates over cohorts of fewer than 10 nodes regardless of ε. Below this threshold, the Laplace noise required to achieve meaningful DP exceeds the signal magnitude for most operational statistics. Publishing a DP-annotated number that is 90% noise is not privacy protection; it is theater. The relay must gate DP output with the k-anonymity floor, refuse to report DP-labeled statistics for sub-threshold cohorts, and surface a deployment-configuration warning to the operator.

---

## §G. Open Technical-Review Items

The `@technical-reviewer` pass must address these before the section advances from technical-review to prose-review:

1. **DP applies to additive aggregates: verify scope.** The section claims DP applies to operation counts, latency bucket counts, and error-event counts. Verify that these are all pure counting queries with sensitivity = 1. If any aggregate (e.g., per-session latency reported as a raw value rather than a bucket count) has sensitivity > 1, the Laplace noise formula changes. Flag any aggregate that requires sensitivity analysis beyond the simple counting case.

2. **Central vs. local DP — self-hosted relay trust claim.** The section asserts that central DP at the relay is credible for self-hosted deployments because the trust is under organizational control. Verify this framing against the Dwork/Roth definition: central DP assumes a trusted curator. For a self-hosted relay operated by the same organization whose nodes generate the statistics, "trusted curator" is satisfied by organizational identity — but the technical reviewer should confirm this is not a subtle trust-model inflation.

3. **Sequential composition ε accumulation formula.** §12c states that n applications of ε-DP yield nε total. Verify this against Dwork and Roth §3.5 (basic composition theorem). Confirm that the "advanced composition" variant claimed to give tighter bounds is the Dwork, Rothblum, Vadhan result (not a different theorem). If a cleaner primary citation exists for the advanced composition result separately from the monograph, add it.

4. **k=10 minimum cohort claim.** The outline cites k=10 as "the de facto minimum in applied privacy literature for operational telemetry." The technical-reviewer should locate a primary source for this specific value (a NIST guidance document, a published healthcare privacy standard, or a peer-reviewed operational-telemetry paper). If no primary source exists for k=10 specifically, the text must say "a commonly applied minimum" rather than "the de facto minimum."

5. **DP-forward-secrecy orthogonality claim.** §12a states that DP on metadata and forward secrecy on content "compose orthogonally." Verify: orthogonality here means the guarantees are independent — implementing one does not weaken the other. This is architecturally straightforward (different attack vectors, different mechanisms) but the technical reviewer should confirm no interaction exists through the relay's processing pipeline (e.g., does the relay's DP noise injector need to observe any key-material metadata that forward secrecy should protect?).

6. **DP-incident-response tension in §12c.** The section proposes temporarily suspending DP aggregation for a compromised node's metrics during incident response. Verify this is architecturally sound: the suspension emits a signed event in `Sunfish.Kernel.Audit`. Confirm that the audit event's existence does not itself leak the fact of the incident to the broader team before the operator has confirmed it — i.e., is the audit event encrypted to the operator role only, or is it visible to all nodes? Cross-reference to §Endpoint Compromise (#47) for the incident-response procedure that this suspension mode would integrate with.

7. **Smart-meter scenario fit.** The design-decisions note on #12 explicitly names the smart-meter scenario. The section as outlined does not use it as a worked example — it uses generic relay-side sync telemetry. The technical reviewer should confirm whether the smart-meter scenario is a better worked example than relay sync telemetry, or whether relay sync telemetry is sufficient to illustrate all three sub-patterns and the smart-meter reference belongs only in a footnote or cross-reference.

---

## §H. Cross-Reference Plan

**Backward references (from the new section to existing Ch15 sections):**

- **§Threat Model** — the opening paragraph of §Privacy-Preserving Aggregation at Relay names the relay's observation capability (which nodes connect, at what volume) as the threat this section mitigates. This is the explicit observation capability named in §Threat Model: "The relay can, however, observe the shape of the conversation: which nodes connect to which, at what times, at what volume." Cross-reference to §Threat Model anchors the new section in the existing threat framing.
- **§Relay Trust Model** — immediate predecessor. §12a's "central vs. local DP" argument explicitly extends §Relay Trust Model's "self-hosted relay eliminates third-party relay operators as metadata observers" prescription. Cross-reference establishes that DP aggregation is the second layer of the relay-metadata mitigation strategy.
- **§Forward Secrecy and Post-Compromise Security (#46)** — §12a establishes orthogonality. One cross-reference sentence: "§Forward Secrecy and Post-Compromise Security addresses payload content over time; the present section addresses behavioral metadata in aggregate — the two compose independently."
- **§Endpoint Compromise (#47)** — §12c names the incident-response suspension mode. One cross-reference sentence pointing to §Endpoint Compromise for the incident-response procedure the suspension integrates with.
- **§Key-Loss Recovery (#48)** — §12b names recovery-event counts as a special carve-out from the k-anonymity floor's general rule. One cross-reference to the recovery-event audit trail sub-pattern 48f.

**Forward references (from existing sections to the new section):**

- **§Relay Trust Model** should gain one sentence at its close: "For operators who legitimately derive aggregate statistics from relay traffic — error rates, sync latencies, fleet health counts — §Privacy-Preserving Aggregation at Relay specifies the DP and k-anonymity mechanisms that satisfy the same privacy intent as self-hosting while enabling operational intelligence." This converts §Relay Trust Model's close from a limitation statement ("traffic analysis by a well-resourced adversary") into a forward pointer that names the solution for the analytics-not-surveillance use case.
- **§Security Properties Summary** gains one row in the guarantee table (see §C above).

---

## §I. Estimated Word Budgets

| Sub-section | Content | Budget |
|---|---|---|
| Opening (§ motivation) | Why relay aggregation creates a gap not covered by §Relay Trust Model; three sub-patterns named | 200 words |
| Sub-pattern 12a | DP mechanism definition, Laplace vs. Gaussian, sensitivity for count queries, central vs. local DP choice, ε values for standard and regulated deployments, orthogonality with #46 | 600 words |
| Sub-pattern 12b | k-anonymity floor, suppression policy, k values per deployment class, l-diversity extension note, recovery-event carve-out | 350 words |
| Sub-pattern 12c | Sequential composition budget, formula, budget window, advanced composition option, incident-response suspension mode | 350 words |
| **Total** | | **~1,500 words** |

The sub-pattern budgets sum precisely to target. The 200-word opening replaces any need for a separate "Why this matters" H3 — the section is short enough that a standalone motivation paragraph within the opening prose suffices.

---

## §J. Notes on Novelty

**Sub-pattern 12a** has strong prior art: Dwork/Roth is the foundational reference; Apple and Google have deployed central and local DP respectively at scale. The application to relay-side sync metadata is a direct and uncontroversial application of established mechanisms. No novelty claim needed; the technical value is the *scoping clarity* — making explicit that DP applies to metadata aggregates, not to CRDT operation content (which is encrypted and DP-inaccessible).

**Sub-pattern 12b** (k-anonymity floor on per-role relay aggregates) is a straightforward application of Sweeney's model to relay partitioning. The k-anonymity floor applied specifically to CRDT role partitions — where roles are the natural quasi-identifier — may not have direct published precedent, but the mechanism is orthodox. The recovery-event carve-out (suppressing recovery-event counts even above the k floor) is a deployment policy, not a new mechanism. No novelty claim needed; flag as an architectural decision with the rationale documented.

**Sub-pattern 12c** (rolling privacy budget gate for time-series relay telemetry) is where this section makes its most distinctive contribution. Time-series DP composition — the same population observed repeatedly — is an active research area (temporal correlation in DP is a known hard problem). The outline's framing (rolling window budget with configurable Σε per window) is a practical engineering approach that makes the composition cost explicit without solving the temporal-correlation problem. This is honest: the section should state that the rolling-window approach is a reasonable operational heuristic, not a formal temporal-DP solution. The recent smart-meter DP literature (arxiv 2311.04544, 2023) confirms that practitioners deploying LDP on time-series data face exactly this challenge. The section should acknowledge the gap rather than claiming a solution the architecture does not deliver.

**The central/local DP choice is architecturally novel for local-first systems.** Most local-first architecture literature treats the relay as purely a routing component with no analytics role. The explicit decision to apply central DP at the relay tier — and the reasoning for choosing central over local DP given a trusted self-hosted relay — is a design decision that the book is contributing, not citing. Mark the central/local DP choice as an architectural decision in the section's prose; do not imply it is derived from prior literature.

---

*Outline complete. Ready for `draft` stage: invoke `@chapter-drafter` with §A–§C as the structural specification, §D for package decisions, §E for citation list, §G for known open questions (pre-answer where possible in the draft, flag the rest for technical-review).*
