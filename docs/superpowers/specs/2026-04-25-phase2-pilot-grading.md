# Phase 2 Pilot Grading

**Background run ID:** `bzduwnh42` — 4 pilots serial, ~40 min wall-clock.

**Order of execution:** Ch04 → Ch05 → Ch11 → Ch01 (Ch01 last so the chapter with original reader feedback gets the freshest read).

**Files to read per pilot:**
- Pass 1 (guest voice only): `chapters/_voice-drafts/pass1/<chapter>.md` (skipped for Ch11 — sinek-direct, no pass-1)
- Pass 2 (after Sinek polish): `chapters/_voice-drafts/final/<chapter>.md`

**Baseline for comparison (Ch01 only):** `chapters/_voice-drafts/_archive/<ts>-pre-phase2/final/ch01-when-saas-fights-reality.md` — the pre-tune output that received "too mechanical, fatiguing" feedback.

---

## Phase 2 Gate (per spec)

| # | Condition | Status |
|---|---|---|
| G1 | ≥3 of 4 pilots PASS by author review | TBD |
| G2 | Audiobook listener-test PASS on ≥1 pilot | TBD |
| G3 | External-reader binding PASS on ≥1 pilot | TBD |

If G1, G2, G3 all PASS → proceed to Phase 3. If any FAIL → return to Task 16/17 retune; second failure escalates to Phase 1 rethink (per kill criteria).

---

## Pilot 1 — Ch04: Choosing Your Architecture

**Pipeline:** godin → sinek
**Map of what each pass should do:**
- Godin should give it manifesto-ish punch (radical brevity, tension-release, direct address)
- Sinek should normalize the cadence without flattening the punch

### Grade

- **Pass 1 (godin):** [ PASS / FAIL ]
  - Notes:
- **Pass 2 (sinek over godin):** [ PASS / FAIL ]
  - Notes:
- **Did Sinek preserve Godin's brevity?** [ YES / NO ]
- **Did Sinek over-compress (audiobook-cadence rule firing too aggressively)?** [ NO / YES ]

---

## Pilot 2 — Ch05: The Enterprise Lens

**Pipeline:** lencioni → sinek
**Map of what each pass should do:**
- Lencioni should foreground the fable structure (named characters: Voss; dialogue; pyramid reveal)
- Sinek should preserve scenes (tuning rule: preserve narrative scenes); normalize between-scene exposition

### Grade

- **Pass 1 (lencioni):** [ PASS / FAIL ]
  - Notes:
- **Pass 2 (sinek over lencioni):** [ PASS / FAIL ]
  - Notes:
- **Did Sinek preserve scene-level prose without flattening Voss's interiority?** [ YES / NO ]
- **Does the Council heading note (Phase 0c, top of Ch05) still survive correctly?** [ YES / NO ]

---

## Pilot 3 — Ch11: Node Architecture

**Pipeline:** sinek-direct (only pass-2 effectively)
**Map of what should happen:**
- Pure house-voice test on a spec chapter
- Voice-pass should produce specification-register prose: Why → How → What, no enumeration drift, audiobook-cadence safe

### Grade

- **Pass 2 (sinek direct):** [ PASS / FAIL ]
  - Notes:
- **Did the spec content stay technically accurate (no Sunfish package drift)?** [ YES / NO ]
- **Did the audiobook-cadence rule prevent Schrems II / DIFC enumeration recurrence?** [ YES / NO ]

---

## Pilot 4 — Ch01: When SaaS Fights Reality (the bellwether)

**Pipeline:** gladwell → sinek
**Map of what each pass should do:**
- Gladwell should give the Marcus opener scene-first, zoom-out structure (already proven in Phase 0.5 as "looks good")
- Sinek should NOT make it mechanical the way it did pre-tune

### Grade against the pre-tune baseline

Diff command for visual side-by-side:
```bash
diff -u chapters/_voice-drafts/_archive/<ts>-pre-phase2/final/ch01-when-saas-fights-reality.md \
        chapters/_voice-drafts/final/ch01-when-saas-fights-reality.md | less
```

- **Pass 1 (gladwell):** [ PASS / FAIL ]
  - Notes:
- **Pass 2 (sinek-tuned over gladwell):** [ PASS / FAIL ]
  - Notes:
- **Diff against pre-tune baseline:** [ NEW IS BETTER / NEW IS SAME / NEW IS WORSE ]
  - Notes (specific passages where it improved or regressed):
- **Did the original "mechanical, fatiguing" complaint survive the tune?** [ NO (fixed) / PARTIAL / YES (still mechanical) ]

---

## Audiobook listener test (G2)

Pick ONE pilot to generate audiobook for and listen at 1.0× playback. Recommended: Ch01 (the bellwether).

```bash
python build/audiobook.py --chapter ch01 --source chapters/_voice-drafts/final/ch01-when-saas-fights-reality.md
# or whatever the audiobook entry signature is
```

- **Listener verdict:** [ PASS (no fatigue) / FAIL (fatigue at: ___) ]
- **Specific timestamps where prose tripped the listener:**

---

## External-reader binding gate (G3)

Send Ch01 pass-2 to one non-author reader. Their PASS/FAIL is binding (per spec C17).

- **Reader name / handle:**
- **Sent date:**
- **Returned verdict:** [ PASS / FAIL ]
- **Reader's notes:**

---

## Decision

After grading all 4 pilots + audiobook + external reader:

- **G1 (3 of 4 pilots PASS):** [ ✅ / ❌ ]
- **G2 (audiobook PASS):** [ ✅ / ❌ ]
- **G3 (external reader PASS):** [ ✅ / ❌ ]

**Phase 2 verdict:** [ PASS — proceed to Phase 3 / FAIL — return to Phase 1 retune / KILL — invoke Alternative A ]

**If proceeding to Phase 3, also decide:**

- **Mode dispatch needed?** Per spec A4, if polish and normalize would produce indistinguishable output, collapse to single mode and skip Tasks 25–26.
  - [ Single-mode is fine — skip Tasks 25–26 ]
  - [ Need both modes — implement mode dispatch in Phase 3 ]

---

## Knowledge capture (post-grading)

Before moving to Phase 3, append to `.wolf/cerebrum.md` `## Key Learnings`:

- Which agent rule actually delivered the improvement vs. pre-tune?
- Which guest agent needed the most tuning (or least)?
- Did any tune backfire (e.g., audiobook-cadence over-applied)?
- Was the polish/normalize tier necessary, or did single-mode suffice?
