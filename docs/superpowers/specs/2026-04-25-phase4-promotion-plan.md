# Phase 4 Promotion Plan

**Background run ID:** `b1eesq6j1` (Phase 3 full orchestration, ~3–4 hours wall clock)

After Phase 3 completes, every chapter (except those promoted early) will have a fresh draft at `chapters/_voice-drafts/final/<ch>.md` plus a Phase 3 log entry at `chapters/_voice-drafts/_log/<UTC>-<ch>-pass2.json` capturing full provenance. Phase 4 promotes each chapter's draft into the source location with a sidecar manifest.

---

## Phase 4 verification before per-chapter promote/reject

Before touching individual chapters, run the integrity checks:

```bash
# 1. Reference integrity — every jurisdiction inline appears in Appendix F
python build/check_audit.py
# Expected: PASS (or list of orphans to add to Appendix F)

# 2. Stale-draft check — no source edited after Phase 3 began
python build/check_stale.py
# Expected: OK (or list of stale chapters to re-run via voice-pass --only --force)

# 3. Word counts (Phase 0 closure deferred this — informational only)
python build/word-count.py
```

---

## Already promoted (early Phase 4)

| Chapter | Promotion commit | Manifest |
|---|---|---|
| ch01-when-saas-fights-reality | `5777433` | chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.manifest.json |

Phase 4 needs to verify the early promotion is still consistent (source SHA matches manifest's `promoted_sha256`).

---

## 26 chapters to promote

Per `chapters/voice-plan.yaml`, the remaining 26 chapters and their voice mappings. Phase 4 promote/reject decision per chapter.

| # | Chapter | Voice | Decision | Notes |
|---|---|---|---|---|
| 1 | preface | sinek | [ ] PROMOTE / REJECT | |
| 2 | ch02-local-first-serious-stack | grant | [ ] PROMOTE / REJECT | |
| 3 | ch03-inverted-stack-one-diagram | sinek | [ ] PROMOTE / REJECT | |
| 4 | ch04-choosing-your-architecture | godin | [ ] PROMOTE / REJECT | Phase 2 pilot |
| 5 | ch05-enterprise-lens | lencioni | [ ] PROMOTE / REJECT | Phase 2 pilot; council heading note added |
| 6 | ch06-distributed-systems-lens | lencioni | [ ] PROMOTE / REJECT | |
| 7 | ch07-security-lens | lencioni | [ ] PROMOTE / REJECT | Watch for Claude safety-filter refusal |
| 8 | ch08-product-economic-lens | grant | [ ] PROMOTE / REJECT | |
| 9 | ch09-local-first-practitioner-lens | brown | [ ] PROMOTE / REJECT | |
| 10 | ch10-synthesis | sinek | [ ] PROMOTE / REJECT | |
| 11 | ch11-node-architecture | sinek | [ ] PROMOTE / REJECT | Phase 2 pilot |
| 12 | ch12-crdt-engine-data-layer | grant | [ ] PROMOTE / REJECT | |
| 13 | ch13-schema-migration-evolution | sinek | [ ] PROMOTE / REJECT | |
| 14 | ch14-sync-daemon-protocol | sinek | [ ] PROMOTE / REJECT | |
| 15 | ch15-security-architecture | sinek | [ ] PROMOTE / REJECT | Watch for Claude safety-filter refusal |
| 16 | ch16-persistence-beyond-the-node | sinek | [ ] PROMOTE / REJECT | |
| 17 | ch17-building-first-node | godin | [ ] PROMOTE / REJECT | |
| 18 | ch18-migrating-existing-saas | lencioni | [ ] PROMOTE / REJECT | |
| 19 | ch19-shipping-to-enterprise | sinek | [ ] PROMOTE / REJECT | |
| 20 | ch20-ux-sync-conflict | brown | [ ] PROMOTE / REJECT | |
| 21 | epilogue-what-the-stack-owes-you | sinek | [ ] PROMOTE / REJECT | |
| 22 | appendix-a-sync-daemon-wire-protocol | sinek | [ ] PROMOTE / REJECT | |
| 23 | appendix-b-threat-model-worksheets | sinek | [ ] PROMOTE / REJECT | |
| 24 | appendix-c-further-reading | sinek | [ ] PROMOTE / REJECT | |
| 25 | appendix-d-testing-the-inverted-stack | sinek | [ ] PROMOTE / REJECT | |
| 26 | appendix-e-citation-style | sinek | [ ] PROMOTE / REJECT | |

(appendix-f-regulatory-coverage is intentionally omitted — pure tabular reference content)

---

## Per-chapter workflow

For each chapter:

1. **Diff the draft against the source:**
   ```bash
   diff -u chapters/<part>/<ch>.md chapters/_voice-drafts/final/<ch>.md | less
   ```

2. **Decide PROMOTE or REJECT.**

3. **PROMOTE:**
   ```bash
   python build/promote.py --chapter <ch>
   git add chapters/<part>/<ch>.md chapters/<part>/<ch>.manifest.json
   git commit -m "promote(<ch>): voice-pass output replaces source (Phase 4)"
   ```

4. **REJECT:**
   ```bash
   python build/promote.py --reject <ch> --reason "<reason>"
   ```
   (Source unchanged; rejection logged to `chapters/_voice-drafts/_rejections.jsonl`.)

5. **Update ICM marker** in the chapter's HTML comment:
   - Promoted: `<!-- icm/voice-check -->` → `<!-- icm/approved -->` (or `voice-check` if you want a final read pass)
   - Rejected: leave at current marker

---

## Batch promotion (if all 26 are PROMOTE)

If you want to promote all in one shot (after eyeballing diffs):

```bash
python build/promote.py --all
```

Promotes every chapter with a draft. Refuses on hash mismatch. Writes manifests. You then commit the entire batch:

```bash
git add chapters/
git commit -m "promote: bulk Phase 4 promotion of 26 chapters with voice-pass output + manifests"
```

---

## Post-promotion verification (F1–F6)

Per spec §2 binary FAILED conditions:

| # | Condition | Check |
|---|---|---|
| F1 | ≥3 of 4 Phase 2 pilots PASSed | (already evaluated) |
| F2 | Audiobook spot-check no fatigue | Generate audiobook for one promoted chapter; listen at 1.0× |
| F3 | Phase 3 orchestrator FAIL rate ≤25% | Count FAILs in Phase 3 background output (`b1eesq6j1`) |
| F4 | `make draft-pdf`, `make epub`, audiobook build all run clean | `python build/audiobook.py --all` ; Pandoc is invoked from Make |
| F5 | `make word-count` shows every chapter ±10% | Pre-existing condition; may stay deferred to professional copyedit |
| F6 | Reference-integrity script reports no orphans | `python build/check_audit.py` |

---

## Audiobook regeneration after promotion

The audio fixes landed in Phase 1.5-equivalent work (df60de5, 98298ee, a209773):
- Em-dash → comma (no dot-marker pauses)
- `$N magnitude` → "N magnitude dollar(s)" with attributive/predicative heuristic
- `[N]` citation markers stripped
- Bare URLs stripped
- 50+ initialisms spelled letter-by-letter

After Phase 4 promotion, regenerate audiobook for all chapters:

```bash
python build/audiobook.py --force --all
```

(Or per-chapter for spot-checks.) Then listen-test ≥1 chapter at 1.0× to validate F2.

---

## Post-Phase-4 exit decisions (per spec §13)

After all 26 promote/reject decisions:

- **If ≥3 chapters required REJECT** — recycle through the literary-board agent for those chapters
- **Else** — decide between professional copyedit pass (~$2-4k) and ship-as-is
- **First-use rule remediation** (567 violations from `check_first_use.py`) is queued for post-voice-pass cleanup; do it before the copyedit pass

---

## Knowledge capture

After Phase 4 closure, append to `.wolf/cerebrum.md` `## Key Learnings`:

- Promote-vs-reject ratio per chapter type (Part I narrative, Part II council, Part III spec, Part IV playbook, appendix)
- Which voice mappings produced the highest-quality output
- Whether single-mode vs polish/normalize tier proved necessary (Phase 2 evidence pointed to single-mode sufficient)
- Which agent rules earned their place vs. were over-engineered
- Total cost (token spend across Phase 3) — confirms or revises §9 budget estimate
