# Prose Review Report — Extension #10 (Data-Class Escalation)

**Reviewer:** prose-reviewer agent
**Date:** 2026-04-28
**Scope:** Ch15 §Event-Triggered Re-classification + Ch20 §Data-Class Escalation UX
**Verdict:** PASS with light edits applied directly. No further revision needed.

---

## 1. Sections reviewed

- `chapters/part-3-reference-architecture/ch15-security-architecture.md` lines ~688–737 (§Event-Triggered Re-classification)
- `chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md` lines ~354–409 (§Data-Class Escalation UX)

Both sections came in dense and on-voice from the technical-review pass. The edits below are surgical: paragraph-cap fixes and one passive-voice activation. No structural rewriting.

## 2. Paragraph length (4 fixes applied)

- **Ch15:694 (opening scenario)** — was 8 sentences. Merged two retention/access/export sentences with semicolons; merged "None of that was true / All of it must be true" with semicolon. Now 6 sentences. Narrative pacing preserved.
- **Ch15:720 (sub-pattern 10d)** — was 7 sentences. Merged the "flagged for operator review" + "auto-lifting cascades" pair into one sentence with `because`. Now 6 sentences.
- **Ch20:358 (opening)** — was 7 sentences. Merged "The mechanism that makes that legibility possible is specified in Ch15..." + "This section does not re-state it." + "It covers what the user sees..." into one sentence using a colon. Trimmed throat-clearing while keeping the section-map. Now 5 sentences.
- **Ch20:388 (operator-triggered escalation)** — was 7 sentences. Folded "The trigger identifier is required, not optional." into the rejection sentence as agency-active prose ("The form rejects an escalation without a named cause"). Now 6 sentences.

All other paragraphs at-or-under cap. Paras at the cap (6 sentences) audited and judged on-voice — they carry single threaded arguments without restatement.

## 3. Active voice / agency vocabulary (1 fix applied)

- **Ch15:710** — "Roles ... find their next attempted read denied" → "Roles ... see their next attempted read denied". `find ... denied` reads as passive-victim phrasing; `see ... denied` keeps the subject experiencing the event but reads cleaner. Truly active ("the daemon denies the next read") would lose the role-centric framing the sentence wants.
- **Ch15:720** — "Those records are flagged for operator review through the audit trail" → "The audit trail flags those records for operator review". Passive made active with an explicit agent.
- **Ch20:388** — "An escalation without a named cause is rejected at the form level" → "The form rejects an escalation without a named cause". Passive made active.

Other passive constructions (Ch15:712 "is not erased", "are not retrieved"; Ch15:716 "was written under the prior class") preserved as architectural commitments where the agent is "the architecture" and naming it would add throat-clearing.

## 4. Academic scaffolding / hedging

None found. The sections lead with facts and consequences — no "this paper argues", "as we have seen", "it is worth noting", "may be encountered". Hedging language ("could potentially", "might be") absent. The single hedge ("may disclose the existence of the investigation") is genuine domain uncertainty about what a reference reveals — appropriate.

## 5. There-is / there-are constructions

None found in either section. Clean.

## 6. Synonym cycling

Audited the three near-synonyms flagged in the brief — re-classification / class change / escalation — and confirmed they carry distinct technical meanings:
- **re-classification** — the formal CRDT operation
- **escalation** — the upward case (the only valid case under max-register monotonicity)
- **class change** — informal/UX-facing language for the same event

The naming aligns with PRESERVATION FLAGS. Not cycling — terminologically layered. Document/record terminology consistent: "record" used throughout (no oscillation to "document" or "object" except in the chain-of-custody tuple example, where "object-id" is the wire-protocol field name).

## 7. Anti-AI tells audit

Scanned both sections against `.claude/skills/anti-ai-tells/SKILL.md`:

- §1 puffery — clean
- §3 superficial -ing tail-phrases ("highlighting X", "ensuring Y") — clean
- §7 AI vocabulary cluster — clean (one "intricate"-adjacent word per page max)
- §8 copula avoidance ("serves as a", "represents a", "boasts") — clean
- §9 negative parallelism ("not only X but also Y") — clean
- §17 title-case headings — clean (all sub-pattern and FAILED-condition headers in sentence case)
- §25 generic positive conclusions — clean (kill-trigger paragraphs end with specific architectural claims)
- §27 persuasive authority tropes ("the real question is", "fundamentally") — clean
- §29 fragmented headers — clean (every heading followed by substance, not restatement)

The §16 inline-header vertical-list pattern doesn't apply — FAILED-conditions blocks ARE genuine glossary lists, the format is correct.

## 8. Part-specific voice tests

**Part III (Ch15) — specification voice.** Sub-pattern 10a–10e read as specification: "is", "does", "applies", "rejects" — not "you should". The §Composition forward block lands its three composition claims (deletion, forward-secrecy, chain-of-custody) as definitive prose. PASS.

**Part IV (Ch20) — tutorial voice.** Second-person imperatives where appropriate ("Do not surface the prior class", "Bind it to the record's current class", "Provide the trigger event identifier"). References Ch15 §10b and §10d rather than re-deriving them. Target-experience-first opening ("Revocation removes a person... Re-classification changes what a record is. Both shift access without user action..."). PASS.

## 9. Preservation flags — verified intact

- **Max-register CRDT framing (Ch15 §10a)** — verbatim. `max(L₁, L₂, ..., Lₙ)`, the three semilattice properties, the `(record_id, lower_class) is rejected at every replica` clause. UNTOUCHED.
- **§Composition forward (Ch15:728)** — the definitive resolution of the CLAIM is preserved verbatim. "Envelope-only re-keying ... is sufficient for every class transition." "Receipt's claim is point-in-time, not perpetual." UNTOUCHED.
- **Principal-novelty contrast paragraph (Ch15:704)** — Microsoft Purview / AWS Macie / Google Cloud DLP framed as contrast. UNTOUCHED.
- **FAILED conditions blocks** — both four-bullet blocks with kill triggers. UNTOUCHED.
- **HTML annotation headers** at start of each section. UNTOUCHED.

## 10. Extension-number leakage check

Scanned for "#10", "#46", "#48", etc. in user-facing prose. Sub-pattern designators (10a–10e, 12a–12c, 45c, 46a–46b, 48f) are in-prose pattern names, not extension numbers — these match the existing Ch15 voice elsewhere. No extension-number leaks found.

## 11. Edits summary

| Location | Issue | Fix |
|---|---|---|
| Ch15:694 | 8-sentence paragraph | Merged with semicolons → 6 sentences |
| Ch15:710 | "find ... denied" reads passive | Changed to "see ... denied" |
| Ch15:720 | 7-sentence paragraph + passive "are flagged" | Merged sentences with `because`; activated passive |
| Ch20:358 | 7-sentence opening with throat-clearing | Merged section-map sentences with colon |
| Ch20:388 | 7-sentence paragraph + passive "is rejected" | Merged trigger-required + rejection sentences; activated passive |

Total: 5 surgical edits. No structural rewriting. No content removed. No PRESERVATION FLAG content touched.

## 12. Overall assessment

- **Tone:** on-voice for both Part III specification register (Ch15) and Part IV tutorial register (Ch20)
- **Estimated revision time:** light — completed in this pass
- **Top 3 priorities (resolved):**
  1. Paragraph-cap compliance (4 fixes)
  2. Passive-voice activation where agent is obvious (3 fixes)
  3. Confirm preservation flags untouched (verified)

Ready for voice-check (Stage 6, human only).
