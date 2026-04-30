---
type: question
chapter: ch16, ch20, ch21, appendix-b
last-pr: chore/pao-phase5-amend-ch23 (working tree)
parent-decision: 2026-04-30-upf-ch15-split-phase5-ch23-addendum.md
---

**Context:** Phase 5 spot-check on PAO's mechanical pass (commit 910a7b8). Pass executed cleanly
on explicit `§<section name>` references but missed 6 concept-level stragglers across 4 files
where the citation describes an operational concept without using the section's literal name.

**Stragglers found:**

1. **Ch20 line 24** — "credential revocation under the Chapter 15 **rekeying flow**" → likely Ch22
   §Key Compromise Incident Response (rekeying = post-compromise key rotation, operational not
   architectural).

2. **Ch20 line 264** — "The **Ch15 deployment-class table** treats recovery as a composition" →
   Ch22 §Key-Loss Recovery (the deployment-class table moved with that section).

3. **Ch16 line 154** — "the substrate Ch15 specifies for **revocation and key-loss recovery**" →
   split to "Ch23 §Collaborator Revocation and Ch22 §Key-Loss Recovery" (both audit-trail
   substrates moved with their sections).

4. **Ch21 line 42** — "Key rotation orchestration extends **Chapter 15's per-node rotation**" →
   Ch22 §Key Compromise Incident Response (per-node rotation flow is operational; architectural
   §Key Hierarchy stays in Ch15 but the rotation flow itself moved).

5. **Appendix B line 6** — `<!-- Source: v13 §11.1, Ch 15 -->` → per Rule R-S amendment, should be
   `<!-- Source: v13 §11.1, Ch15, Ch22, Ch23 -->` (appendix references both architectural and
   operational material).

6. **Appendix B line 12** — "Chapter 15 carries the full security architecture: ... and the **key
   compromise incident response procedure**" → split to "Chapter 15 carries the security
   architecture: DEK/KEK key hierarchy, role attestation flow, compelled-access resistance model.
   Chapter 22 carries the key compromise incident response procedure."

**Confirmed correct (no action needed):**
- Ch20 line 157 ("founder attestation — root trust anchor described in Chapter 15") — Role
  Attestation Flow stays in Ch15.
- Ch20 line 308 ("Ch15 §Role Attestation Flow") — explicit ref, correct.
- Ch16 lines 236, 244, 254 — DEK/KEK hierarchy, security architecture cryptographic mechanism,
  Relay Trust Model — all stay in Ch15.
- Ch21 lines 48, 97, 105, 136 — explicit §Key Hierarchy + §Role Attestation Flow refs, correct.
- Appendix B lines 101, 113, 148 — explicit §In-Memory Key Handling + §Endpoint Compromise refs,
  correct.
- Appendix G lines 15, 27, 34, 66, 85 — explicit §Key Hierarchy refs, correct.

**Pattern observation:** the 6 stragglers all follow a pattern your mechanical pass couldn't catch
mechanically: a citation that describes the *concept* spec'd by a moved section without using the
section's literal name. Future passes might want a concept→section mapping in addition to the
§-name regex.

**What would unblock me:** Your call on whether the 6 stragglers ship as-is (acceptable copyedit
debt at this stage) or warrant a follow-up mechanical pass. None are reader-experience-blocking;
all are accuracy-of-cross-reference concerns. Ch15 forward-pointers from my prior beacon are the
mechanical companions to fixing #1, #2, #4 cleanly.

**Continuing to monitor /loop per CO never-exit directive.** No further chapter edits planned this
iteration; queue dry pending PAO direction or external signal (audiobook progression, Phase 4
Ch22+Ch23 prune review, voice-pass author input).
