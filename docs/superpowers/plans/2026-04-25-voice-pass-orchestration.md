# Voice-Pass Orchestration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Take *The Inverted Stack* manuscript through a full editorial + voice-pass cycle: clean dense source prose, audit and tune voice agents, run all 27 chapters through the two-pass orchestrator, and promote vetted outputs back to `main` — with full provenance and reproducibility.

**Architecture:** Five phases (0.0, 0, 0.5, 1, 2, 3, 4) executed sequentially with binary gates between each. Heavy editorial work in Phase 0; one methodology test in Phase 0.5 that may collapse Phase 1; code changes to `build/voice-pass.py` and a new `build/promote.py` in Phases 1 and 4; pilot validation in Phase 2 before the full Phase 3 run.

**Tech Stack:** Python 3.12, Claude Code CLI (Sonnet 4.6), pytest (added in this plan), Pandoc (existing), Make (existing), git, plain markdown chapters, YAML plan file (custom parser, no PyYAML dep).

**Spec:** `docs/superpowers/specs/2026-04-25-voice-pass-orchestration-design.md`
**Audit:** `docs/superpowers/specs/2026-04-25-voice-pass-orchestration-audit.md`
**Council review:** `docs/superpowers/specs/2026-04-25-voice-pass-orchestration-design.council-review.md`

---

## File Structure

### Files created in this plan

| Path | Responsibility |
|---|---|
| `agents/voice-sinek.md` | Source-of-truth mirror of user-scope agent, then tuned per Phase 1 |
| `agents/voice-gladwell.md` | Same |
| `agents/voice-brown.md` | Same |
| `agents/voice-grant.md` | Same |
| `agents/voice-godin.md` | Same |
| `agents/voice-lencioni.md` | Same |
| `chapters/appendices/appendix-f-regulatory-coverage.md` | New — full jurisdiction × framework × chapter table |
| `chapters/_part-2-preamble.md` *(optional, see D1)* | Council-disclosure note alternative location |
| `build/promote.py` | Phase 4 promotion script; hash verification, manifest writing, ICM marker update |
| `build/check_audit.py` | Reference-integrity script: every jurisdiction removed from inline prose appears in Appendix F |
| `build/check_stale.py` | Pre-Phase 4 mtime check: warn if any source is newer than its draft |
| `tests/__init__.py` | Pytest scaffolding |
| `tests/build/__init__.py` | Same |
| `tests/build/test_voice_pass.py` | Tests for parser changes, mode dispatch, logging |
| `tests/build/test_promote.py` | Tests for promotion script |
| `tests/build/test_check_audit.py` | Tests for audit verification |
| `tests/conftest.py` | Pytest fixtures (tmp repo, sample chapter) |
| `pytest.ini` | pytest config |
| `chapters/<part>/<ch>.manifest.json` × 27 | Created during Phase 4 — per-promoted-chapter audit sidecar |

### Files modified in this plan

| Path | Why |
|---|---|
| `build/voice-pass.py` | Read agents from `agents/` not `~/.claude/agents/`; parse polish/normalize mode; per-invocation logging; mode-aware prompt selection; stale-draft detection |
| `chapters/voice-plan.yaml` | Add third column (polish/normalize); skip Appendix F |
| `chapters/<part>/<ch>.md` × 24 | Phase 0a regulatory compression |
| `chapters/front-matter/preface.md` | Phase 0c composite-character disclosure paragraph |
| `chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md` | Phase 0c council-heading note (pending D1) |
| `agents/voice-*.md` × 6 | Phase 1 tuning (after mirror) |
| `.gitignore` | Add `_voice-drafts/_log/` if not covered by parent rule |
| `build/Makefile` | Add `promote-chapter`, `check-audit`, `check-stale` targets |
| `.wolf/cerebrum.md` | Knowledge capture entries (Phase 2 + post-mortem) |
| `.wolf/buglog.json` | Incident entries (Phase 3 + post-mortem) |
| `.wolf/memory.md` | Per-action log entries throughout |

---

## Pre-flight: Test Scaffolding

### Task 0: Set up pytest

**Files:**
- Create: `pytest.ini`
- Create: `tests/__init__.py`
- Create: `tests/build/__init__.py`
- Create: `tests/conftest.py`

- [ ] **Step 1: Install pytest**

Run: `python -m pip install pytest`
Expected: `Successfully installed pytest-X.X.X`

- [ ] **Step 2: Create pytest.ini**

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

- [ ] **Step 3: Create empty package init files**

```python
# tests/__init__.py
```

```python
# tests/build/__init__.py
```

- [ ] **Step 4: Create shared conftest with sample-chapter fixture**

```python
# tests/conftest.py
"""Shared pytest fixtures."""
from __future__ import annotations
import json
from pathlib import Path

import pytest

SAMPLE_CHAPTER = """\
# Sample Chapter

This is a paragraph of prose.

## Section

Another paragraph with some content.
"""


@pytest.fixture
def tmp_repo(tmp_path: Path) -> Path:
    """Create a minimal repo skeleton: chapters/, agents/, _voice-drafts/."""
    (tmp_path / "chapters" / "part-1").mkdir(parents=True)
    (tmp_path / "agents").mkdir()
    (tmp_path / "chapters" / "_voice-drafts" / "pass1").mkdir(parents=True)
    (tmp_path / "chapters" / "_voice-drafts" / "final").mkdir(parents=True)
    (tmp_path / "chapters" / "_voice-drafts" / "_log").mkdir(parents=True)
    return tmp_path


@pytest.fixture
def sample_chapter(tmp_repo: Path) -> Path:
    """Write a sample chapter into the tmp repo."""
    p = tmp_repo / "chapters" / "part-1" / "ch99-sample.md"
    p.write_text(SAMPLE_CHAPTER, encoding="utf-8")
    return p


@pytest.fixture
def sample_agent(tmp_repo: Path) -> Path:
    """Write a sample agent file."""
    p = tmp_repo / "agents" / "voice-sinek.md"
    p.write_text("---\nname: voice-sinek\nmodel: sonnet\n---\nAgent prompt body.\n", encoding="utf-8")
    return p
```

- [ ] **Step 5: Verify pytest discovers the directory**

Run: `python -m pytest --collect-only`
Expected: `collected 0 items` (no tests yet, no errors)

- [ ] **Step 6: Commit**

```bash
git add pytest.ini tests/
git commit -m "build: add pytest scaffolding for voice-pass plan"
```

---

## Phase 0.0: Timing Pilot (C13/B4)

The single highest-leverage early gate. Compress two chapters, time it, project, decide.

### Task 1: Compress Ch01 ¶73 (HIGH severity, 27 jurisdictions)

**Files:**
- Modify: `chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md`

- [ ] **Step 1: Note the start time**

Run: `date -u +%FT%TZ` and record in a scratch file (e.g., `.wolf/phase00-timing.txt`).

- [ ] **Step 2: Read the offending paragraph**

Open `chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md`, locate paragraph 73 ("The jurisdictional scope of this compliance argument..."). The paragraph is named in the spec audit at `docs/superpowers/specs/2026-04-25-voice-pass-orchestration-audit.md`.

- [ ] **Step 3: Identify chapter-anchor jurisdiction(s)**

Ch01 is the thesis/pain chapter for a global audience. Anchors: GDPR (Schrems II) for EU; DPDP (India) for the largest Tier-2/Tier-3 reader population; DIFC DPL 2020 for the regulated-finance vertical the chapter cites.

- [ ] **Step 4: Replace the enumeration with the canonical compressed form**

Old paragraph (excerpt):
```
The jurisdictional scope of this compliance argument is wider than US-centric discussions typically acknowledge. The EU's GDPR established that personal data of EU residents requires lawful basis... [27 jurisdictions enumerated]... The book's architecture is frequently a legal requirement before it is an architectural choice.
```

New paragraph:
```
The jurisdictional scope of this compliance argument is wider than US-centric discussions typically acknowledge. The EU's Schrems II ruling, India's Digital Personal Data Protection Act 2023, and the UAE's DIFC Data Protection Law 2020 are representative — each, in different language, makes data residency a compliance mechanism rather than a preference. The same pattern repeats across more than thirty national and regional frameworks; the full coverage table for this chapter is in Appendix F. In each of these jurisdictions, an architecture where data lives on the user's own hardware — not in a vendor's cloud region — is not merely preferred. In many configurations, it is the architecture that makes compliance tractable. The book's architecture is frequently a legal requirement before it is an architectural choice.
```

- [ ] **Step 5: Verify word count of the chapter is still in range**

Run: `python build/word-count.py ch01` (or `make word-count`)
Expected: ch01 word count within ±10% of its target.

- [ ] **Step 6: Note end time and compute elapsed minutes**

Append to `.wolf/phase00-timing.txt`:
```
ch01 ¶73 (HIGH): start=<T0> end=<T1> elapsed=<minutes>
```

- [ ] **Step 7: Commit**

```bash
git add chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md
git commit -m "edit(ch01): compress jurisdictional enumeration ¶73 (Phase 0.0 timing pilot)"
```

### Task 2: Compress one MED-severity paragraph

**Files:**
- Modify: one of the MED-tier paragraphs from the audit (recommended: `chapters/part-3-reference-architecture/ch16-persistence-beyond-the-node.md` ¶67, 9 jurisdictions in 319 words)

- [ ] **Step 1: Note start time** as in Task 1.

- [ ] **Step 2: Read the audit entry** for the chosen paragraph.

- [ ] **Step 3: Apply the MED-recipe** — keep up to 4 jurisdictions inline as a short series; lift the rest to a forthcoming Appendix F entry (which will be created in Task 5).

- [ ] **Step 4: Verify word count.**

- [ ] **Step 5: Note end time.**

- [ ] **Step 6: Commit** with prefix `edit(chXX): compress jurisdictional enumeration (Phase 0.0)`.

### Task 3: Project Phase 0 total and decide

- [ ] **Step 1: Compute average minutes per paragraph from the two pilots**

From `.wolf/phase00-timing.txt`, compute `avg_minutes = (ch01_minutes + chXX_minutes) / 2`.

- [ ] **Step 2: Multiply by total paragraph count from the audit**

Run: `grep -c "^- \*\*HIGH\*\*\|^- \*\*MED\*\*" docs/superpowers/specs/2026-04-25-voice-pass-orchestration-audit.md`
Expected: a single number — total HIGH+MED paragraphs.

Project total = `total_paragraphs * avg_minutes / 60` hours.

- [ ] **Step 3: Decide**

| Projection | Action |
|---|---|
| ≤48h | Continue to Task 4 (full sweep) |
| 48–100h | Pause; decide continue vs. Alternative A vs. Alternative B |
| >100h | Invoke Alternative A or B; this plan stops at this task |

- [ ] **Step 4: Record decision in `.wolf/cerebrum.md`**

Append a `## Key Learnings` entry: "Phase 0.0 timing: avg X min/para, projected total Yh, decision Z."

- [ ] **Step 5: Commit**

```bash
git add .wolf/cerebrum.md .wolf/phase00-timing.txt
git commit -m "plan(phase-0.0): timing pilot complete; projection Xh, decision Y"
```

---

## Phase 0: Source Cleanup

If Task 3 says "continue," this phase sweeps the remaining HIGH and MED paragraphs across all 24 affected chapters.

### Task 4: Bulk compress all remaining HIGH-severity paragraphs

**Files:** Each chapter listed as HIGH in the audit.

- [ ] **Step 1: Open the audit and list HIGH paragraphs**

Run: `grep "^- \*\*HIGH\*\*" docs/superpowers/specs/2026-04-25-voice-pass-orchestration-audit.md`

- [ ] **Step 2: For each remaining HIGH paragraph (Ch01 ¶73 already done), apply the recipe from Task 1**

For each:
1. Read the paragraph in context.
2. Identify the chapter-anchor jurisdiction(s) — the one most relevant to the chapter's argument; check `.wolf/memory.md` 2026-04-24 entries for any literary-board-flagged jurisdictions for that chapter.
3. Replace enumeration with: anchor + short series of 2–3 + reference pointer to Appendix F.
4. Re-read the paragraph; verify it still reads as one argument.
5. `make word-count` to confirm chapter is within ±10%.

- [ ] **Step 3: Commit per chapter**

```bash
git add chapters/<part>/<ch>.md
git commit -m "edit(chXX): compress jurisdictional enumeration (Phase 0a HIGH)"
```

(One commit per chapter — small commits aid Phase 4 review.)

### Task 5: Bulk compress all remaining MED-severity paragraphs

Same procedure as Task 4, but use the lighter MED recipe (keep up to 4 inline as a short series).

- [ ] **Step 1: List MED paragraphs**

Run: `grep "^- \*\*MED\*\*" docs/superpowers/specs/2026-04-25-voice-pass-orchestration-audit.md`

- [ ] **Step 2: For each MED paragraph, apply the lighter recipe**

Same five sub-steps as Task 4 Step 2, but inline allowance is 4 jurisdictions instead of 2–3.

- [ ] **Step 3: Commit per chapter** as in Task 4.

### Task 6: Create Appendix F — Regulatory Coverage Map

**Files:**
- Create: `chapters/appendices/appendix-f-regulatory-coverage.md`

- [ ] **Step 1: Draft the appendix structure**

Use this template (write the full file):

```markdown
# Appendix F — Regulatory Coverage Map

<!-- icm/draft -->
<!-- Target: ~2,000 words -->

This appendix consolidates the regulatory frameworks referenced throughout the book. Inline chapters cite a representative anchor for each compliance argument; this appendix provides the full coverage matrix for readers, evaluators, and counsel.

The frameworks are grouped by region. Within each region, the entries follow a consistent shape: framework name and citation; year of effective date; data-residency, consent, and access-rights properties relevant to the local-first architecture; and the chapter(s) where the framework's coverage applies.

## Europe

### GDPR (Regulation (EU) 2016/679)

[Description of GDPR's relevance to local-first architecture; Article 17 erasure; Article 30 records of processing; Article 44 transfer restrictions.]

**Chapters:** 1, 2, 3, 4, 7, 9, 11, 12, 15, 18

### Schrems II (CJEU C-311/18, 2020)

[Description: invalidates Privacy Shield; constrains EU→US transfers without supplemental safeguards.]

**Chapters:** 1, 2, 3, 4, 7, 9, 11, 12, 15, 18

[... continue for: SCCs status, EUI Data Act, ePrivacy Directive ...]

## Middle East

### UAE Federal Data Protection Law 2022
### DIFC Data Protection Law 2020 (DIFC Law No. 5 of 2020)
### Saudi PDPL (Royal Decree M/19, 2021)

## Asia-Pacific

### India DPDP Act 2023
### China PIPL (2021)
### Japan APPI (act 57 of 2003, amended 2022)
### South Korea PIPA (act 10465, 2011, amended)
### Singapore PDPA (act 26 of 2012)

## Africa

### South Africa POPIA (act 4 of 2013, effective 2021)
### Nigeria NDPR + NDPA 2023
### Kenya Data Protection Act 2019

## Americas

### Brazil LGPD (Lei 13.709/2018)
### Mexico LFPDPPP (2010)
### Colombia Ley 1581 (2012)
### Argentina Ley 25.326 (2000)
### California CCPA + CPRA (2018, 2020)
### US sector-specific (HIPAA, FERPA, GLBA)

## CIS / Eastern Europe

### Russia Federal Law 242-FZ (2014)

## Cross-Cutting Frameworks

### Standard Contractual Clauses (EU) — adequacy status
### Binding Corporate Rules
### ISO/IEC 27701, SOC 2, ISMS-P (Korea), ENS (Spain) — administrative controls

## Per-Chapter Index

A reverse index showing which frameworks each chapter cites. Used by reviewers and the reference-integrity script.

| Chapter | Frameworks cited |
|---|---|
| Ch01 | GDPR, Schrems II, DPDP, DIFC DPL, ... |
| Ch02 | ... |
| ... | ... |

---

**Note:** This appendix is not legal advice. Readers building production deployments must engage qualified counsel for jurisdiction-specific compliance review.
```

Fill in the bracketed sections by reading the original enumerations from each chapter's git history (pre-Phase 0a).

- [ ] **Step 2: Verify word count**

Run: `python build/word-count.py appendix-f` (or update the word-count script's chapter list).

- [ ] **Step 3: Commit**

```bash
git add chapters/appendices/appendix-f-regulatory-coverage.md
git commit -m "draft(appendix-f): regulatory coverage map (consolidates jurisdictions lifted in Phase 0a)"
```

### Task 7: Build the reference-integrity script

**Files:**
- Create: `build/check_audit.py`
- Create: `tests/build/test_check_audit.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/build/test_check_audit.py
"""Tests for the reference-integrity audit checker."""
from __future__ import annotations
from pathlib import Path

import pytest

from build.check_audit import find_jurisdictions_in_chapter, find_jurisdictions_in_appendix_f


def test_finds_jurisdictions_in_chapter(tmp_path: Path):
    ch = tmp_path / "ch01.md"
    ch.write_text("The EU's GDPR and India's DPDP Act apply.", encoding="utf-8")
    found = find_jurisdictions_in_chapter(ch)
    assert "GDPR" in found
    assert "DPDP" in found


def test_finds_jurisdictions_in_appendix_f(tmp_path: Path):
    apx = tmp_path / "appendix-f.md"
    apx.write_text("# Appendix F\n\n### GDPR\n### DPDP Act 2023\n", encoding="utf-8")
    found = find_jurisdictions_in_appendix_f(apx)
    assert "GDPR" in found
    assert "DPDP" in found
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/build/test_check_audit.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'build.check_audit'`

- [ ] **Step 3: Write minimal implementation**

```python
# build/check_audit.py
"""Reference-integrity check: every jurisdiction in inline prose appears in Appendix F.

Usage:
    python build/check_audit.py
Exits 0 on PASS, 1 on FAIL with diagnostic.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHAPTERS = REPO / "chapters"
APPENDIX_F = CHAPTERS / "appendices" / "appendix-f-regulatory-coverage.md"

JURISDICTION_PATTERNS = [
    r"GDPR", r"Schrems(?: II)?", r"DPDP(?: Act)?", r"DIFC(?: DPL)?", r"LGPD",
    r"POPIA", r"NDPR", r"NDPA", r"\bPIPA\b", r"PIPL", r"APPI",
    r"242-FZ", r"LFPDPPP", r"Ley 1581", r"Ley 25\.326", r"CCPA", r"CPRA",
    r"HIPAA", r"FERPA", r"GLBA", r"PDPA",
]
PATTERN = re.compile("|".join(JURISDICTION_PATTERNS))


def find_jurisdictions_in_chapter(path: Path) -> set[str]:
    """Return distinct jurisdiction tokens found in a chapter file."""
    return set(PATTERN.findall(path.read_text(encoding="utf-8")))


def find_jurisdictions_in_appendix_f(path: Path) -> set[str]:
    """Return distinct jurisdiction tokens declared in Appendix F."""
    return set(PATTERN.findall(path.read_text(encoding="utf-8")))


def main() -> int:
    if not APPENDIX_F.exists():
        print(f"ERROR: {APPENDIX_F} does not exist; create it before running this check.", file=sys.stderr)
        return 1
    declared = find_jurisdictions_in_appendix_f(APPENDIX_F)
    failures: list[str] = []
    for ch in sorted(CHAPTERS.glob("**/*.md")):
        if "_voice-drafts" in ch.parts or ch == APPENDIX_F:
            continue
        used = find_jurisdictions_in_chapter(ch)
        orphans = used - declared
        if orphans:
            failures.append(f"{ch.relative_to(REPO).as_posix()}: {sorted(orphans)}")
    if failures:
        print("FAIL — jurisdictions in chapters not declared in Appendix F:")
        for f in failures:
            print(f"  {f}")
        return 1
    print(f"PASS — every jurisdiction in chapters appears in Appendix F.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/build/test_check_audit.py -v`
Expected: 2 passed.

- [ ] **Step 5: Run the script against the real repo**

Run: `python build/check_audit.py`
Expected: PASS (assuming Phase 0a + 0b are complete). If FAIL, the listed orphans need to be added to Appendix F.

- [ ] **Step 6: Add a Make target**

Add to `build/Makefile`:
```makefile
.PHONY: check-audit
check-audit:
	python build/check_audit.py
```

- [ ] **Step 7: Commit**

```bash
git add build/check_audit.py tests/build/test_check_audit.py build/Makefile
git commit -m "build: reference-integrity script for Phase 0a → Appendix F"
```

### Task 8: Insert composite-character disclosure paragraph in Preface

**Files:**
- Modify: `chapters/front-matter/preface.md`

- [ ] **Step 1: Read the current Preface and find the right insertion point**

The disclosure should appear in or just after the section that introduces the council device (likely under a "Method" or "How this book is structured" heading). If no such section exists, insert before "Why I Wrote This."

- [ ] **Step 2: Insert the Sinek-voice paragraph**

```markdown
We invented the people. We did not invent the objections. Five composite characters — each a faithful stand-in for a domain that had every reason to dismantle this architecture — read the paper twice. What broke, broke for real reasons. What changed, changed because the reasons were good.
```

- [ ] **Step 3: Verify word count**

Run: `make word-count` and confirm preface still within ±10% of target.

- [ ] **Step 4: Commit**

```bash
git add chapters/front-matter/preface.md
git commit -m "edit(preface): composite-character disclosure paragraph (Phase 0c)"
```

### Task 9: Insert council-heading note at top of Ch05

**Files:**
- Modify: `chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md`

- [ ] **Step 1: Insert the note immediately after the Part II / Ch05 heading**

After the chapter's title heading, before the body, insert:

```markdown
> **A note on the council:** The five members are composite characters — fictional practitioners constructed to embody real domains and real objections. The objections are real. The names are not.
```

- [ ] **Step 2: Verify word count**

- [ ] **Step 3: Commit**

```bash
git add chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md
git commit -m "edit(ch05): council-heading composite-character note (Phase 0c)"
```

### Task 10: Run full Phase 0 verification suite

- [ ] **Step 1: Run word-count**

Run: `make word-count`
Expected: every chapter listed within ±10% of target.

- [ ] **Step 2: Run cross-reference lint**

Run: `make lint`
Expected: no broken cross-references.

- [ ] **Step 3: Run reference-integrity check**

Run: `make check-audit`
Expected: PASS.

- [ ] **Step 4: Re-read each compressed chapter (manual)**

For each chapter listed in the audit, open the file and verify the compressed paragraph reads as one argument and accuracy is preserved.

- [ ] **Step 5: Commit Phase 0 closure marker**

```bash
git commit --allow-empty -m "phase(0): source cleanup complete; ready for Phase 0.5 methodology check"
```

---

## Phase 0.5: Methodology Check (C16/B5)

The single most consequential one-hour test in the plan. May rescope Phase 1 dramatically.

### Task 11: Re-run Gladwell pass-1 on cleaned Ch01

**Files:**
- Output: `chapters/_voice-drafts/pass1/ch01-when-saas-fights-reality.md`

- [ ] **Step 1: Confirm Phase 0 commit landed for Ch01**

Run: `git log --oneline chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md | head -3`
Expected: a recent `edit(ch01): compress jurisdictional enumeration` commit.

- [ ] **Step 2: Re-run pass-1 with --force**

Run: `python build/voice-pass.py --only ch01 --pass 1 --force`
Expected: `OK ch01-when-saas-fights-reality -> voice-gladwell` with elapsed time.

- [ ] **Step 3: Verify the output exists and is fresh**

Run: `ls -la chapters/_voice-drafts/pass1/ch01-when-saas-fights-reality.md`
Expected: file exists with recent mtime.

### Task 12: Read three Ch01 versions and decide

- [ ] **Step 1: Read the cleaned source**

Open `chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md`.

- [ ] **Step 2: Read the new pass-1 (Gladwell only)**

Open `chapters/_voice-drafts/pass1/ch01-when-saas-fights-reality.md`.

- [ ] **Step 3: Read the existing pass-2 (Gladwell→Sinek)**

Open `chapters/_voice-drafts/final/ch01-when-saas-fights-reality.md`.

- [ ] **Step 4: Decide using the spec's decision matrix**

| Pass-1 reads… | Decision | Phase 1 scope |
|---|---|---|
| Better than current pass-2 | Drop pass-2 for guest-voiced chapters | Tune Sinek only for sinek-direct chapters; guest agents get audit only |
| About the same | Light Sinek tune only | No polish/normalize tier |
| Worse than pass-2 (or worse than source) | Original plan stands | Tune all six agents; introduce polish/normalize tiers |

- [ ] **Step 5: Record decision in `.wolf/cerebrum.md`**

Append `## Key Learnings`:
```
Phase 0.5 methodology check (2026-MM-DD): Ch01 pass-1 vs pass-2 vs cleaned source
Decision: <Drop pass-2 | Light Sinek | Original plan>
Reasoning: <2-3 sentences on what was different about pass-1 vs pass-2>
Phase 1 scope: <updated scope>
```

- [ ] **Step 6: Commit decision**

```bash
git add .wolf/cerebrum.md
git commit -m "phase(0.5): methodology check complete; Phase 1 scope = <decision>"
```

The Phase 1 task list below assumes "Original plan stands." If a different decision was made, skip the Phase 1 tasks marked **[full-tune-only]** and adjust as noted.

---

## Phase 1: Voice-Agent Tuning + Code Provenance

### Task 13: Mirror agent files into the manuscript repo (B1/C2)

**Files:**
- Create: `agents/voice-{sinek,gladwell,brown,grant,godin,lencioni}.md`

- [ ] **Step 1: Copy each agent file**

```bash
mkdir -p agents
cp ~/.claude/agents/voice-sinek.md agents/
cp ~/.claude/agents/voice-gladwell.md agents/
cp ~/.claude/agents/voice-brown.md agents/
cp ~/.claude/agents/voice-grant.md agents/
cp ~/.claude/agents/voice-godin.md agents/
cp ~/.claude/agents/voice-lencioni.md agents/
```

- [ ] **Step 2: Verify all six are present**

Run: `ls agents/voice-*.md | wc -l`
Expected: `6`

- [ ] **Step 3: Commit baseline**

```bash
git add agents/
git commit -m "agents: mirror six voice agents into repo (Phase 1 pre-step; council B1/C2)"
```

### Task 14: Update voice-pass.py to read agents from in-repo path (B1/C2)

**Files:**
- Modify: `build/voice-pass.py`
- Create: `tests/build/test_voice_pass.py`

- [ ] **Step 1: Write a failing test for the agent-path resolution**

```python
# tests/build/test_voice_pass.py
"""Tests for build/voice-pass.py changes."""
from __future__ import annotations
import sys
from pathlib import Path

import pytest

# Make build/ importable
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# Import the module-under-test by file path because of the hyphen in the filename
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "voice_pass",
    Path(__file__).resolve().parents[2] / "build" / "voice-pass.py",
)
voice_pass = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(voice_pass)


def test_build_prompt_references_in_repo_agent_path():
    """The prompt should point to agents/voice-X.md (in repo), not ~/.claude/agents/."""
    src = Path("chapters/part-1/ch01.md")
    dst = Path("chapters/_voice-drafts/final/ch01.md")
    prompt = voice_pass.build_prompt("sinek", src, dst)
    assert "agents/voice-sinek.md" in prompt
    assert "~/.claude/agents/voice-sinek.md" not in prompt
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/build/test_voice_pass.py::test_build_prompt_references_in_repo_agent_path -v`
Expected: FAIL — current `build_prompt` references `~/.claude/agents/voice-{voice}.md`.

- [ ] **Step 3: Update build_prompt in build/voice-pass.py**

Open `build/voice-pass.py`. Find the `build_prompt` function (~line 92). Change:
```python
return f"""Operate as the voice-{voice} agent (defined in ~/.claude/agents/voice-{voice}.md).
```
to:
```python
return f"""Operate as the voice-{voice} agent (defined in agents/voice-{voice}.md).
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/build/test_voice_pass.py::test_build_prompt_references_in_repo_agent_path -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add build/voice-pass.py tests/build/test_voice_pass.py
git commit -m "build(voice-pass): read agents from in-repo agents/ path (B1/C2)"
```

### Task 15: Add source-paper prohibition rule to each agent (C10)

**Files:**
- Modify: `agents/voice-sinek.md`, `agents/voice-gladwell.md`, `agents/voice-brown.md`, `agents/voice-grant.md`, `agents/voice-godin.md`, `agents/voice-lencioni.md`

- [ ] **Step 1: For each agent file, locate the "What you do not do" section**

Each agent has a `## What you do not do` section. The exact heading wording may vary slightly per agent.

- [ ] **Step 2: Append the prohibition bullet**

Add this bullet to the existing list in each file:

```markdown
- You do not read, reference, or quote files under `source/`. The chapter content provided in this prompt is the only authorised input.
```

- [ ] **Step 3: Verify with grep**

Run: `grep -L "You do not read, reference, or quote files under" agents/voice-*.md`
Expected: empty output (every agent file has the line).

- [ ] **Step 4: Commit**

```bash
git add agents/
git commit -m "agents: forbid source/ paper access (council C10)"
```

### Task 16: Tune voice-sinek for chapter-scale prose (B5/C16 — full-tune-only)

**Files:**
- Modify: `agents/voice-sinek.md`

> Skip this task if Phase 0.5 returned "drop pass-2" — Sinek is unchanged in that branch.

- [ ] **Step 1: Reframe calibration test #2 from per-section to per-chapter**

Open `agents/voice-sinek.md`. Find the calibration test section. Change:
```
2. Is the core claim restated 2–3 times across the passage, each at a different angle?
```
to:
```
2. Is the chapter's core claim — not each section's claim — restated 2–3 times across the chapter, each at a different angle? Section-level repetition compounds at chapter scale into fatiguing emphasis. Restate the chapter's thesis, not each section's.
```

- [ ] **Step 2: Add the scene-preservation rule**

Insert into the "Sentence-level rules" section:
```markdown
- **Preserve narrative scenes.** When the source paragraph is a narrative scene (named person, time, place, sensory detail), do not apply restatement-loop or moral-statement-ending techniques to it. Scenes earn their place by carrying the reader; they do not need rhetorical reinforcement. Sharpen the prose; preserve the scene's pace.
```

- [ ] **Step 3: Add the audiobook-cadence rule**

Insert into "Sentence-level rules":
```markdown
- **Audiobook cadence.** No inline enumeration longer than three items. Lists of four or more must be either lifted to a sentence break (one item per sentence) or replaced with a representative anchor + a pointer to a referenced source. The audiobook listener cannot skim; long enumerations become an unbroken stream of names.
```

- [ ] **Step 4: Add the register-variation rule**

Insert into "Sentence-level rules":
```markdown
- **Register variation.** Scene, exposition, and argument should sound different. Do not flatten all three to a single declarative cadence. When a passage in the source is already well-written for its register, leave it alone — your job is to add craft on top of the author's, not to overwrite it.
```

- [ ] **Step 5: Add the 10% cut rule**

Insert into "Sentence-level rules" (or as a new rule near the calibration test):
```markdown
- **10% cut.** After rewriting, make a final pass that cuts 10% of the rewrite. Borrowed from Stephen King: the discipline of cutting forces every word to earn its place. Reference: `docs/style/style-guide.md`.
```

- [ ] **Step 6: Add a chapter-opening canonical example**

Insert after the existing CRDT example (### Example):

```markdown
### Example — chapter-opening register

This is the Sinek voice operating at *chapter* scale rather than at illustration scale.

**Source (preface fragment):**
> The Kleppmann Council read the paper twice. They are five composite characters — invented people — who each represent a real domain that had every reason to dismantle this architecture.

**Sinek-voice (chapter-opening register):**
> We invented the people. We did not invent the objections. Five composite characters — each a faithful stand-in for a domain that had every reason to dismantle this architecture — read the paper twice. What broke, broke for real reasons. What changed, changed because the reasons were good.

Notice: scene-led ("we invented... we did not invent"), parallel construction, no inline enumeration of jurisdictions or domains. The closing line gives the reader a stance, not a summary.
```

- [ ] **Step 7: Verify the agent file still parses (frontmatter intact)**

Run: `python -c "
from pathlib import Path
text = Path('agents/voice-sinek.md').read_text(encoding='utf-8')
assert text.startswith('---'), 'frontmatter missing'
end = text.find('---', 3)
assert end > 0, 'frontmatter not closed'
print('OK')
"`
Expected: `OK`

- [ ] **Step 8: Commit**

```bash
git add agents/voice-sinek.md
git commit -m "agents(sinek): chapter-scale calibration; scene preservation, audiobook cadence, register variation, 10% cut"
```

### Task 17: Audit guest agents (gladwell, brown, grant, godin, lencioni)

**Files:**
- Review (read-only): `agents/voice-{gladwell,brown,grant,godin,lencioni}.md`
- Modify only as needed.

- [ ] **Step 1: For each guest agent, read the file**

For each of the five guest agents, ask: "If these rules are applied to a 5,000-word chapter instead of a 300-word example, do they compound into a mechanical pattern?"

- [ ] **Step 2: Where needed, apply analogous tunes**

Apply the relevant subset of the Sinek tunes (chapter-scale calibration, audiobook cadence, register variation) to any guest agent whose existing rules show the same chapter-scale risk. Skip rules that are already chapter-scale-aware (gladwell's information rationing, lencioni's leadership-fable structure are likely fine as-is).

- [ ] **Step 3: For each modified guest agent, commit separately**

```bash
git add agents/voice-<name>.md
git commit -m "agents(<name>): chapter-scale audit findings"
```

- [ ] **Step 4: For agents not modified, log the decision in `.wolf/cerebrum.md`**

Append `## Key Learnings`:
```
Phase 1 guest-agent audit:
- gladwell: <changes / no change + why>
- brown: <...>
- grant: <...>
- godin: <...>
- lencioni: <...>
```

- [ ] **Step 5: Commit cerebrum**

```bash
git add .wolf/cerebrum.md
git commit -m "phase(1): guest-agent audit findings recorded"
```

### Task 18: Add per-invocation logging to voice-pass.py (C9/B3)

**Files:**
- Modify: `build/voice-pass.py`
- Modify: `tests/build/test_voice_pass.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/build/test_voice_pass.py`:

```python
def test_log_invocation_writes_json_with_required_fields(tmp_repo):
    """Per-invocation log file contains all required fields."""
    log_dir = tmp_repo / "chapters" / "_voice-drafts" / "_log"
    src = tmp_repo / "chapters" / "part-1" / "ch99-sample.md"
    src.write_text("source content", encoding="utf-8")
    dst = tmp_repo / "chapters" / "_voice-drafts" / "final" / "ch99-sample.md"
    dst.write_text("output content", encoding="utf-8")
    agent = tmp_repo / "agents" / "voice-sinek.md"
    agent.parent.mkdir(exist_ok=True, parents=True)
    agent.write_text("agent content", encoding="utf-8")

    log_path = voice_pass.log_invocation(
        log_dir=log_dir,
        chapter="ch99-sample",
        pass_num=2,
        source=src,
        output=dst,
        agent_path=agent,
        cli_version="claude 1.0.0",
        model="claude-sonnet-4-6",
        mode="polish",
        exit_code=0,
        duration_s=12.5,
        start_iso="2026-04-25T10:00:00Z",
        end_iso="2026-04-25T10:00:12Z",
    )
    import json
    data = json.loads(log_path.read_text(encoding="utf-8"))
    for key in ("chapter", "pass_num", "input_sha256", "output_sha256",
                "agent_path", "agent_sha256", "claude_cli_version", "model",
                "prompt_mode", "exit_code", "duration_s",
                "wall_clock_start_iso", "wall_clock_end_iso"):
        assert key in data, f"missing {key}"
    assert data["chapter"] == "ch99-sample"
    assert data["pass_num"] == 2
    assert data["prompt_mode"] == "polish"
    assert len(data["input_sha256"]) == 64
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/build/test_voice_pass.py::test_log_invocation_writes_json_with_required_fields -v`
Expected: FAIL — `log_invocation` does not exist.

- [ ] **Step 3: Add log_invocation to build/voice-pass.py**

Add this function (above `run_voice_pass`):

```python
import hashlib
import json


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def log_invocation(
    log_dir: Path,
    chapter: str,
    pass_num: int,
    source: Path,
    output: Path,
    agent_path: Path,
    cli_version: str,
    model: str,
    mode: str,
    exit_code: int,
    duration_s: float,
    start_iso: str,
    end_iso: str,
) -> Path:
    """Write a per-invocation log file in chapters/_voice-drafts/_log/.

    Returns the path of the written log file."""
    log_dir.mkdir(parents=True, exist_ok=True)
    safe_start = start_iso.replace(":", "").replace("-", "")
    log_path = log_dir / f"{safe_start}-{chapter}-pass{pass_num}.json"
    payload = {
        "chapter": chapter,
        "pass_num": pass_num,
        "input_sha256": _sha256(source),
        "output_sha256": _sha256(output) if output.exists() else None,
        "agent_path": agent_path.relative_to(REPO).as_posix() if agent_path.is_absolute() else str(agent_path),
        "agent_sha256": _sha256(agent_path),
        "claude_cli_version": cli_version,
        "model": model,
        "prompt_mode": mode,
        "exit_code": exit_code,
        "duration_s": duration_s,
        "wall_clock_start_iso": start_iso,
        "wall_clock_end_iso": end_iso,
    }
    log_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return log_path


def _claude_cli_version(claude_path: str) -> str:
    """Best-effort capture of claude --version. Returns 'unknown' on failure."""
    try:
        result = subprocess.run([claude_path, "--version"], capture_output=True, text=True, timeout=10)
        return result.stdout.strip() or "unknown"
    except Exception:
        return "unknown"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/build/test_voice_pass.py::test_log_invocation_writes_json_with_required_fields -v`
Expected: PASS.

- [ ] **Step 5: Wire logging into run_voice_pass**

Update `run_voice_pass` to call `log_invocation` after each invocation completes. Pass `pass_num` (1 or 2) and `mode` (currently always "normalize"; will be polish/normalize after Task 19).

```python
def run_voice_pass(
    claude: str, voice: str, source: Path, output: Path,
    pass_num: int, mode: str = "normalize",
    timeout_s: int = 900, force: bool = False,
) -> tuple[bool, str]:
    """... existing docstring ..."""
    output.parent.mkdir(parents=True, exist_ok=True)
    if force and output.exists():
        output.unlink()
    prompt = build_prompt(voice, source, output)
    start_dt = datetime.now(timezone.utc)
    start_time = time.time()
    cli_version = _claude_cli_version(claude)
    agent_path = REPO / "agents" / f"voice-{voice}.md"
    try:
        proc = subprocess.run(
            [claude, "-p", prompt],
            capture_output=True, text=True, cwd=REPO, timeout=timeout_s,
        )
        exit_code = proc.returncode
    except subprocess.TimeoutExpired:
        exit_code = -1
        proc = None
    end_dt = datetime.now(timezone.utc)
    duration = time.time() - start_time

    # Write the log regardless of success
    log_invocation(
        log_dir=DRAFTS / "_log",
        chapter=source.stem,
        pass_num=pass_num,
        source=source,
        output=output,
        agent_path=agent_path,
        cli_version=cli_version,
        model="claude-sonnet-4-6",
        mode=mode,
        exit_code=exit_code,
        duration_s=duration,
        start_iso=start_dt.isoformat().replace("+00:00", "Z"),
        end_iso=end_dt.isoformat().replace("+00:00", "Z"),
    )

    if proc is None:
        if output.exists() and output.stat().st_mtime > start_time:
            return True, f"timeout-but-output-written ({output.stat().st_size} bytes)"
        return False, f"timeout after {timeout_s}s, no fresh output"
    if proc.returncode != 0:
        return False, f"claude exited {proc.returncode}: {proc.stderr.strip()[:240]}"
    if not output.exists() or output.stat().st_size == 0:
        return False, f"agent did not write {output.relative_to(REPO).as_posix()}"
    if output.stat().st_mtime < start_time:
        return False, f"output is stale (not touched during this run)"
    last_line = (proc.stdout.strip().splitlines() or [""])[-1]
    return True, last_line[:160]
```

Add `from datetime import datetime, timezone` to the top imports.

Update the two call sites (in `main()`) to pass `pass_num=1` for pass 1 and `pass_num=2` for pass 2.

- [ ] **Step 6: Run all voice_pass tests**

Run: `python -m pytest tests/build/test_voice_pass.py -v`
Expected: all pass.

- [ ] **Step 7: Commit**

```bash
git add build/voice-pass.py tests/build/test_voice_pass.py
git commit -m "build(voice-pass): per-invocation logging with SHAs and CLI metadata (council B3/C9)"
```

### Task 19: Archive `_voice-drafts/` before Phase 2 begins (C7)

- [ ] **Step 1: Create timestamped archive subdirectory**

```bash
ts=$(date -u +%Y-%m-%d-%H%M)
mkdir -p chapters/_voice-drafts/_archive/${ts}-pre-phase2
mv chapters/_voice-drafts/pass1 chapters/_voice-drafts/_archive/${ts}-pre-phase2/
mv chapters/_voice-drafts/final chapters/_voice-drafts/_archive/${ts}-pre-phase2/
mkdir chapters/_voice-drafts/pass1 chapters/_voice-drafts/final
```

- [ ] **Step 2: Verify the archive**

Run: `ls chapters/_voice-drafts/_archive/`
Expected: directory containing the prior pass1 and final.

- [ ] **Step 3: Note in memory.md**

Append a one-line entry: `archived _voice-drafts before Phase 2`.

- [ ] **Step 4: Phase 1 closure commit**

```bash
git commit --allow-empty -m "phase(1): voice-agent tuning + provenance plumbing complete"
```

---

## Phase 2: Pilot

### Task 20: Run pilot voice-pass on Ch01 (gladwell → sinek)

- [ ] **Step 1: Confirm Phase 1 changes are committed**

Run: `git log --oneline -5`
Expected: recent Phase 1 commits visible.

- [ ] **Step 2: Run both passes for Ch01**

Run: `python build/voice-pass.py --only ch01 --force`
Expected: `OK` for pass 1 (gladwell) and pass 2 (sinek).

- [ ] **Step 3: Verify outputs and log entries**

```bash
ls -la chapters/_voice-drafts/pass1/ch01-when-saas-fights-reality.md
ls -la chapters/_voice-drafts/final/ch01-when-saas-fights-reality.md
ls -la chapters/_voice-drafts/_log/*-ch01-when-saas-fights-reality-*.json
```

Expected: both drafts and at least 2 log entries (one per pass).

### Task 21: Run pilot for Ch11 (sinek-direct), Ch05 (lencioni→sinek), Ch04 (godin→sinek)

- [ ] **Step 1: Run each pilot**

```bash
python build/voice-pass.py --only ch11 --force
python build/voice-pass.py --only ch05 --force
python build/voice-pass.py --only ch04 --force
```

- [ ] **Step 2: Verify all log entries**

Run: `ls chapters/_voice-drafts/_log/`
Expected: log files for ch01, ch04, ch05, ch11 across the relevant passes.

### Task 22: Read each pilot's both passes and grade

- [ ] **Step 1: For each of the four pilots (Ch01, Ch04, Ch05, Ch11), read pass-1 output (skip Ch11 since it's sinek-direct, no pass-1)**

Open each `chapters/_voice-drafts/pass1/<ch>.md` and read end to end.

- [ ] **Step 2: For each, read pass-2 output**

Open each `chapters/_voice-drafts/final/<ch>.md`.

- [ ] **Step 3: Grade PASS/FAIL with notes**

Create `.wolf/phase2-pilot-grades.md`:
```markdown
# Phase 2 Pilot Grades

## Ch01 (gladwell → sinek-polish)
- Pass-1: PASS / FAIL — <notes>
- Pass-2: PASS / FAIL — <notes>

## Ch04 (godin → sinek-polish)
...
## Ch05 (lencioni → sinek-polish)
...
## Ch11 (sinek-normalize direct)
- Pass-2: PASS / FAIL — <notes>
```

- [ ] **Step 4: External-reader gate (C17)**

Send the Ch01 pass-2 (or pass-1 if Phase 0.5 dropped pass-2) to one non-author reader. Their PASS/FAIL is binding. Record their verdict in `phase2-pilot-grades.md`.

### Task 23: Generate audiobook for one pilot and listen

- [ ] **Step 1: Generate the audiobook MP3 for Ch01**

Run: `python build/audiobook.py --chapter ch01 --source chapters/_voice-drafts/final/ch01-when-saas-fights-reality.md`
Expected: MP3 written to `build/output/audio/ch01-*.mp3`.

- [ ] **Step 2: Listen at 1.0× playback**

Listen end-to-end. Note any passage where cadence fatigues or enumeration breaks the listen.

- [ ] **Step 3: Record verdict in `.wolf/phase2-pilot-grades.md`**

Add a `## Audiobook listener test` section with PASS/FAIL and notes.

### Task 24: Phase 2 gate — decide continue or retune

- [ ] **Step 1: Apply gate**

Plan continues to Phase 3 only if:
- ≥3 of 4 pilots PASS
- External-reader PASS on the binding pilot
- Audiobook listener-test PASS

If any fails: identify the agent rule responsible, return to Task 16/17, and re-pilot. After two retune rounds without all pilots passing, invoke the §7 kill criterion (fall back to Alternative A).

- [ ] **Step 2: Commit Phase 2 closure**

```bash
git add .wolf/phase2-pilot-grades.md
git commit -m "phase(2): pilot complete; <pass/retune>"
```

---

## Phase 3: Full Orchestration Run

### Task 25: Add polish/normalize mode parser to voice-pass.py (full-tune-only)

> Skip this entire task if Phase 0.5 collapsed Phase 1 — no mode dispatch needed.

**Files:**
- Modify: `build/voice-pass.py`
- Modify: `tests/build/test_voice_pass.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/build/test_voice_pass.py`:

```python
def test_load_plan_with_mode_column(tmp_path, monkeypatch):
    """voice-plan.yaml entries support an optional third column for mode."""
    plan_text = """\
ch01-foo:    gladwell    polish
ch11-bar:    sinek       normalize
ch99-baz:    grant
"""
    plan_file = tmp_path / "plan.yaml"
    plan_file.write_text(plan_text, encoding="utf-8")
    monkeypatch.setattr(voice_pass, "PLAN", plan_file)
    plan = voice_pass.load_plan()
    assert plan["ch01-foo"] == ("gladwell", "polish")
    assert plan["ch11-bar"] == ("sinek", "normalize")
    assert plan["ch99-baz"] == ("grant", "normalize")  # default mode


def test_load_plan_rejects_unknown_mode(tmp_path, monkeypatch, capsys):
    plan_text = "ch01-foo:    gladwell    bogus\n"
    plan_file = tmp_path / "plan.yaml"
    plan_file.write_text(plan_text, encoding="utf-8")
    monkeypatch.setattr(voice_pass, "PLAN", plan_file)
    plan = voice_pass.load_plan()
    assert "ch01-foo" not in plan  # bogus mode → entry skipped
    err = capsys.readouterr().err
    assert "bogus" in err
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/build/test_voice_pass.py -v -k "mode"`
Expected: 2 FAIL.

- [ ] **Step 3: Update load_plan in build/voice-pass.py**

Replace the existing `load_plan` with:

```python
VALID_MODES = {"polish", "normalize"}


def load_plan() -> dict[str, tuple[str, str]]:
    """Parse voice-plan.yaml as 'chapter: voice [mode]'.

    Returns a map of chapter → (voice, mode). Mode defaults to 'normalize'.
    """
    plan: dict[str, tuple[str, str]] = {}
    for line in PLAN.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.split("#", 1)[0].strip()
        if not value:
            continue
        parts = value.split()
        voice = parts[0]
        mode = parts[1] if len(parts) > 1 else "normalize"
        if voice not in VALID_VOICES:
            print(f"WARN: unknown voice '{voice}' for {key.strip()}", file=sys.stderr)
            continue
        if mode not in VALID_MODES:
            print(f"WARN: unknown mode '{mode}' for {key.strip()}", file=sys.stderr)
            continue
        plan[key.strip()] = (voice, mode)
    return plan
```

- [ ] **Step 4: Update all callers**

In `main()`, `plan_summary()`, and the iteration loops, treat `plan[ch]` as a tuple `(voice, mode)` rather than a string. Update `plan_summary` to count voices only (not modes).

- [ ] **Step 5: Update voice-plan.yaml with mode column**

Open `chapters/voice-plan.yaml`. For each guest-voice entry, append `polish`. For each sinek entry, append `normalize`. Example:

```yaml
ch01-when-saas-fights-reality:    gladwell    polish
ch02-local-first-serious-stack:   grant       polish
ch03-inverted-stack-one-diagram:  sinek       normalize
ch04-choosing-your-architecture:  godin       polish
ch05-enterprise-lens:             lencioni    polish
ch06-distributed-systems-lens:    lencioni    polish
ch07-security-lens:               lencioni    polish
ch08-product-economic-lens:       grant       polish
ch09-local-first-practitioner-lens: brown     polish
ch10-synthesis:                   sinek       normalize
ch11-node-architecture:           sinek       normalize
ch12-crdt-engine-data-layer:      grant       polish
ch13-schema-migration-evolution:  sinek       normalize
ch14-sync-daemon-protocol:        sinek       normalize
ch15-security-architecture:       sinek       normalize
ch16-persistence-beyond-the-node: sinek       normalize
ch17-building-first-node:         godin       polish
ch18-migrating-existing-saas:     lencioni    polish
ch19-shipping-to-enterprise:      sinek       normalize
ch20-ux-sync-conflict:            brown       polish
preface:                          sinek       normalize
epilogue-what-the-stack-owes-you: sinek       normalize
appendix-a-sync-daemon-wire-protocol: sinek   normalize
appendix-b-threat-model-worksheets: sinek     normalize
appendix-c-further-reading:       sinek       normalize
appendix-d-testing-the-inverted-stack: sinek  normalize
appendix-e-citation-style:        sinek       normalize
```

(Note: Appendix F is intentionally omitted from the plan per spec §4.3.)

- [ ] **Step 6: Run tests**

Run: `python -m pytest tests/build/test_voice_pass.py -v`
Expected: all pass.

- [ ] **Step 7: Commit**

```bash
git add build/voice-pass.py chapters/voice-plan.yaml tests/build/test_voice_pass.py
git commit -m "build(voice-pass): polish/normalize mode column in voice-plan.yaml"
```

### Task 26: Add mode-aware prompt selection (full-tune-only)

**Files:**
- Modify: `build/voice-pass.py`
- Modify: `tests/build/test_voice_pass.py`

- [ ] **Step 1: Write failing test**

Append to `tests/build/test_voice_pass.py`:

```python
def test_build_prompt_polish_differs_from_normalize():
    src = Path("chapters/part-1/ch01.md")
    dst = Path("chapters/_voice-drafts/final/ch01.md")
    polish = voice_pass.build_prompt("sinek", src, dst, mode="polish")
    normalize = voice_pass.build_prompt("sinek", src, dst, mode="normalize")
    assert polish != normalize
    assert "polish" in polish.lower() or "preserve" in polish.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/build/test_voice_pass.py::test_build_prompt_polish_differs_from_normalize -v`
Expected: FAIL — `build_prompt` does not accept `mode`.

- [ ] **Step 3: Add mode parameter to build_prompt**

Update the signature and append a mode-specific instruction block:

```python
def build_prompt(voice: str, source_path: Path, output_path: Path, mode: str = "normalize") -> str:
    rel_src = source_path.relative_to(REPO).as_posix() if source_path.is_absolute() else source_path.as_posix()
    rel_dst = output_path.relative_to(REPO).as_posix() if output_path.is_absolute() else output_path.as_posix()
    base = f"""Operate as the voice-{voice} agent (defined in agents/voice-{voice}.md).

TASK
1. Read the chapter markdown at {rel_src}
2. Rewrite it in your voice following ALL instructions in your agent file.
3. Apply your calibration self-check before producing the rewrite.
4. Write the rewritten markdown to {rel_dst} (create parent directories if needed).

[... existing PRESERVATION RULES, REWRITE TARGETS, DISCIPLINE RULES sections unchanged ...]
"""
    if mode == "polish":
        mode_block = """
MODE: POLISH
You are running in POLISH mode. The source has already been rewritten by a guest voice.
Your job is to lightly normalize cadence and cut hedging — not to overwrite the guest voice.
Specifically:
- Do NOT apply restatement-loop or moral-statement-ending techniques to scenes.
- Do NOT replace the guest voice's prose patterns with your own.
- DO cut adverbs, hedges, and redundancy. DO apply the 10% cut.
- DO enforce the audiobook-cadence rule (no inline enumerations longer than 3 items).
"""
    else:
        mode_block = """
MODE: NORMALIZE
You are running in NORMALIZE mode. The source is the original chapter (not guest-voiced).
Apply your full voice instructions — Why→How→What sequencing, repetition loops at chapter scale, scene preservation.
"""
    return base + mode_block + """
OUTPUT TO STDOUT:
After successfully writing the file, output a single line of the form:
DONE: <output-path> (<word-count> words)
Output nothing else.
"""
```

(Replace the entire `build_prompt` function. The existing PRESERVATION RULES / REWRITE TARGETS / DISCIPLINE RULES blocks must be preserved verbatim — copy them from the current implementation.)

- [ ] **Step 4: Wire mode through to run_voice_pass and main()**

In `main()`, when iterating the plan, pass the mode from the plan tuple to `build_prompt` (via `run_voice_pass`).

- [ ] **Step 5: Run tests**

Run: `python -m pytest tests/build/test_voice_pass.py -v`
Expected: all pass.

- [ ] **Step 6: Commit**

```bash
git add build/voice-pass.py tests/build/test_voice_pass.py
git commit -m "build(voice-pass): mode-aware prompt selection (polish vs normalize)"
```

### Task 27: Add stale-draft check (C8)

**Files:**
- Create: `build/check_stale.py`
- Create: `tests/build/test_check_stale.py`

- [ ] **Step 1: Write failing test**

```python
# tests/build/test_check_stale.py
"""Tests for the stale-draft check."""
from __future__ import annotations
import os
import time
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "check_stale",
    Path(__file__).resolve().parents[2] / "build" / "check_stale.py",
)
check_stale = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_stale)


def test_detects_stale_when_source_newer_than_draft(tmp_path):
    src = tmp_path / "chapters" / "part-1" / "ch01.md"
    src.parent.mkdir(parents=True)
    src.write_text("source", encoding="utf-8")

    draft = tmp_path / "chapters" / "_voice-drafts" / "final" / "ch01.md"
    draft.parent.mkdir(parents=True)
    draft.write_text("draft", encoding="utf-8")
    # Make draft older than source
    old = time.time() - 3600
    os.utime(draft, (old, old))

    stale = check_stale.find_stale_drafts(tmp_path / "chapters")
    assert "ch01" in stale


def test_no_stale_when_draft_newer(tmp_path):
    src = tmp_path / "chapters" / "part-1" / "ch01.md"
    src.parent.mkdir(parents=True)
    src.write_text("source", encoding="utf-8")
    old = time.time() - 3600
    os.utime(src, (old, old))

    draft = tmp_path / "chapters" / "_voice-drafts" / "final" / "ch01.md"
    draft.parent.mkdir(parents=True)
    draft.write_text("draft", encoding="utf-8")

    stale = check_stale.find_stale_drafts(tmp_path / "chapters")
    assert "ch01" not in stale
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/build/test_check_stale.py -v`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement build/check_stale.py**

```python
# build/check_stale.py
"""Pre-Phase-4 stale-draft detector.

If any chapter source under chapters/<part>/ has mtime newer than its
corresponding _voice-drafts/final/<ch>.md, the draft is stale and
voice-pass needs to re-run.

Usage:
    python build/check_stale.py
Exits 0 if all drafts are fresh, 1 if any are stale.
"""
from __future__ import annotations
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHAPTERS = REPO / "chapters"


def find_stale_drafts(chapters_root: Path) -> list[str]:
    """Return the stems of chapter drafts that are stale relative to source."""
    final_dir = chapters_root / "_voice-drafts" / "final"
    if not final_dir.exists():
        return []
    stale: list[str] = []
    for source in chapters_root.glob("**/*.md"):
        if "_voice-drafts" in source.parts:
            continue
        draft = final_dir / source.name
        if not draft.exists():
            continue
        if source.stat().st_mtime > draft.stat().st_mtime:
            stale.append(source.stem)
    return stale


def main() -> int:
    stale = find_stale_drafts(CHAPTERS)
    if stale:
        print("STALE drafts (source edited after voice-pass):")
        for s in stale:
            print(f"  {s}")
        return 1
    print("OK — all drafts are at-or-newer than their source.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/build/test_check_stale.py -v`
Expected: 2 passed.

- [ ] **Step 5: Add Make target**

Append to `build/Makefile`:
```makefile
.PHONY: check-stale
check-stale:
	python build/check_stale.py
```

- [ ] **Step 6: Commit**

```bash
git add build/check_stale.py tests/build/test_check_stale.py build/Makefile
git commit -m "build: stale-draft check for source-edited-after-Phase-3 (C8)"
```

### Task 28: Run the full Phase 3 orchestration

- [ ] **Step 1: Verify pre-conditions**

```bash
make check-audit
make check-stale
git status
```

Expected: check-audit PASS; check-stale OK; working tree clean.

- [ ] **Step 2: Capture run-start metadata in commit-staging**

```bash
claude --version > /tmp/voice-pass-cli-version.txt
date -u +%FT%TZ > /tmp/voice-pass-start.txt
```

- [ ] **Step 3: Run the orchestrator**

Run: `python build/voice-pass.py --force`
Expected: serial run across all 27 chapters; per-chapter OK/FAIL line.

- [ ] **Step 4: Capture failures**

If any chapter shows FAIL, list them. For each FAIL:
- Read the corresponding log entry in `_voice-drafts/_log/`.
- For ch07 / ch15 specifically, check for safety-filter refusal (the §7 special case).
- Re-run individually: `python build/voice-pass.py --only <ch> --force`.

- [ ] **Step 5: Verify no FAILs outstanding**

After re-runs, expect zero FAILs across all 27 chapters.

- [ ] **Step 6: Phase 3 closure commit**

```bash
git commit --allow-empty -m "phase(3): full voice-pass run complete; CLI=$(cat /tmp/voice-pass-cli-version.txt)"
```

---

## Phase 4: Promotion

### Task 29: Build the promotion script

**Files:**
- Create: `build/promote.py`
- Create: `tests/build/test_promote.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/build/test_promote.py
"""Tests for the Phase 4 promotion script."""
from __future__ import annotations
import json
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "promote",
    Path(__file__).resolve().parents[2] / "build" / "promote.py",
)
promote = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(promote)


def test_compute_sha256(tmp_path):
    p = tmp_path / "f.txt"
    p.write_text("hello\n", encoding="utf-8")
    assert promote.compute_sha256(p) == promote.compute_sha256(p)
    p2 = tmp_path / "g.txt"
    p2.write_text("hello\n", encoding="utf-8")
    assert promote.compute_sha256(p) == promote.compute_sha256(p2)


def test_promote_copies_draft_and_writes_manifest(tmp_repo):
    # Set up: a source, a draft, and a matching log entry
    source = tmp_repo / "chapters" / "part-1" / "ch01-foo.md"
    source.write_text("source v1", encoding="utf-8")
    draft = tmp_repo / "chapters" / "_voice-drafts" / "final" / "ch01-foo.md"
    draft.write_text("voice-passed v1", encoding="utf-8")
    log_dir = tmp_repo / "chapters" / "_voice-drafts" / "_log"
    log_entry = {
        "chapter": "ch01-foo",
        "pass_num": 2,
        "input_sha256": promote.compute_sha256(source),
        "output_sha256": promote.compute_sha256(draft),
        "agent_path": "agents/voice-sinek.md",
        "agent_sha256": "0" * 64,
        "claude_cli_version": "claude 1.0.0",
        "model": "claude-sonnet-4-6",
        "prompt_mode": "normalize",
        "exit_code": 0,
        "duration_s": 1.0,
        "wall_clock_start_iso": "2026-04-25T10:00:00Z",
        "wall_clock_end_iso": "2026-04-25T10:00:01Z",
    }
    (log_dir / "20260425T100000Z-ch01-foo-pass2.json").write_text(
        json.dumps(log_entry), encoding="utf-8"
    )
    promoted_at = "2026-04-25T11:00:00Z"
    promote.promote_chapter(
        source=source, draft=draft, log_dir=log_dir,
        promoter="Test User <t@example.com>",
        promoted_at_iso=promoted_at,
    )
    # Source now has the draft content
    assert source.read_text(encoding="utf-8") == "voice-passed v1"
    # Manifest exists alongside source
    manifest_path = source.with_suffix(".manifest.json")
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["promoted_at_iso"] == promoted_at
    assert manifest["promoter"] == "Test User <t@example.com>"
    assert manifest["promoted_sha256"] == promote.compute_sha256(source)


def test_promote_fails_on_hash_mismatch(tmp_repo):
    source = tmp_repo / "chapters" / "part-1" / "ch01-foo.md"
    source.write_text("source v1", encoding="utf-8")
    draft = tmp_repo / "chapters" / "_voice-drafts" / "final" / "ch01-foo.md"
    draft.write_text("voice-passed v1", encoding="utf-8")
    log_dir = tmp_repo / "chapters" / "_voice-drafts" / "_log"
    # Log entry with WRONG output sha
    log_entry = {
        "chapter": "ch01-foo", "pass_num": 2,
        "input_sha256": promote.compute_sha256(source),
        "output_sha256": "f" * 64,  # mismatch
        "agent_path": "agents/voice-sinek.md", "agent_sha256": "0" * 64,
        "claude_cli_version": "claude 1.0.0", "model": "claude-sonnet-4-6",
        "prompt_mode": "normalize", "exit_code": 0, "duration_s": 1.0,
        "wall_clock_start_iso": "2026-04-25T10:00:00Z",
        "wall_clock_end_iso": "2026-04-25T10:00:01Z",
    }
    (log_dir / "20260425T100000Z-ch01-foo-pass2.json").write_text(
        json.dumps(log_entry), encoding="utf-8"
    )
    with pytest.raises(promote.HashMismatchError):
        promote.promote_chapter(
            source=source, draft=draft, log_dir=log_dir,
            promoter="t", promoted_at_iso="2026-04-25T11:00:00Z",
        )
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/build/test_promote.py -v`
Expected: 3 FAIL (module not found).

- [ ] **Step 3: Implement build/promote.py**

```python
"""Phase 4 promotion script.

Promotes a voice-passed draft from chapters/_voice-drafts/final/<ch>.md
into chapters/<part>/<ch>.md, after verifying the draft's SHA-256 matches
the recorded log entry. Writes a sidecar manifest alongside the source.

Usage:
    python build/promote.py --chapter ch01-when-saas-fights-reality
    python build/promote.py --all                 # promote every chapter
    python build/promote.py --reject ch15 --reason "voice-passed worse than source"
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHAPTERS = REPO / "chapters"
DRAFTS_FINAL = CHAPTERS / "_voice-drafts" / "final"
LOG_DIR = CHAPTERS / "_voice-drafts" / "_log"


class HashMismatchError(Exception):
    pass


def compute_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_source(chapter_stem: str) -> Path | None:
    for p in CHAPTERS.glob(f"**/{chapter_stem}.md"):
        if "_voice-drafts" in p.parts:
            continue
        return p
    return None


def latest_log_for(chapter_stem: str, pass_num: int, log_dir: Path) -> dict | None:
    """Return the most recent log entry for the given chapter and pass."""
    candidates = sorted(log_dir.glob(f"*-{chapter_stem}-pass{pass_num}.json"))
    if not candidates:
        return None
    return json.loads(candidates[-1].read_text(encoding="utf-8"))


def promote_chapter(
    source: Path, draft: Path, log_dir: Path,
    promoter: str, promoted_at_iso: str,
    accept_manual_edit: bool = False,
) -> Path:
    """Promote a draft to source. Returns the manifest path.

    Raises HashMismatchError if draft's SHA does not match the log entry,
    unless accept_manual_edit=True.
    """
    chapter_stem = source.stem
    log = latest_log_for(chapter_stem, 2, log_dir)
    if log is None:
        log = latest_log_for(chapter_stem, 1, log_dir)
    if log is None:
        raise FileNotFoundError(f"no log entry for {chapter_stem}")

    draft_sha = compute_sha256(draft)
    if not accept_manual_edit and log["output_sha256"] != draft_sha:
        raise HashMismatchError(
            f"draft SHA {draft_sha} != log SHA {log['output_sha256']} for {chapter_stem}"
        )

    # Copy draft over source
    shutil.copyfile(draft, source)
    promoted_sha = compute_sha256(source)

    manifest = {
        **log,
        "promoted_sha256": promoted_sha,
        "promoted_at_iso": promoted_at_iso,
        "promoter": promoter,
        "manual_edit": accept_manual_edit,
    }
    manifest_path = source.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path


def _git_user() -> str:
    try:
        name = subprocess.check_output(["git", "config", "user.name"], text=True).strip()
        email = subprocess.check_output(["git", "config", "user.email"], text=True).strip()
        return f"{name} <{email}>"
    except Exception:
        return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", help="single chapter stem to promote")
    ap.add_argument("--all", action="store_true", help="promote every available draft")
    ap.add_argument("--reject", help="record a REJECT decision with --reason")
    ap.add_argument("--reason", help="reason for reject")
    ap.add_argument("--accept-manual-edit", action="store_true",
                    help="accept hash mismatch (manual edit was made post-pass)")
    args = ap.parse_args()

    if args.reject:
        # Just record the rejection in cerebrum/memory; no source change.
        if not args.reason:
            print("ERROR: --reject requires --reason", file=sys.stderr)
            return 2
        print(f"REJECT {args.reject}: {args.reason}")
        # Append to a rejection log (caller commits manually)
        return 0

    if not (args.chapter or args.all):
        ap.print_help()
        return 2

    promoter = _git_user()
    promoted_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    chapters = []
    if args.chapter:
        chapters = [args.chapter]
    else:
        chapters = [d.stem for d in DRAFTS_FINAL.glob("*.md")]

    failures: list[str] = []
    for ch in chapters:
        source = find_source(ch)
        if source is None:
            print(f"SKIP {ch}: no source under chapters/")
            continue
        draft = DRAFTS_FINAL / f"{ch}.md"
        if not draft.exists():
            print(f"SKIP {ch}: no draft at {draft.relative_to(REPO)}")
            continue
        try:
            manifest_path = promote_chapter(
                source=source, draft=draft, log_dir=LOG_DIR,
                promoter=promoter, promoted_at_iso=promoted_at,
                accept_manual_edit=args.accept_manual_edit,
            )
            print(f"OK   {ch} -> {source.relative_to(REPO)} (manifest: {manifest_path.name})")
        except HashMismatchError as e:
            print(f"FAIL {ch}: {e}", file=sys.stderr)
            failures.append(ch)
        except Exception as e:
            print(f"FAIL {ch}: {type(e).__name__}: {e}", file=sys.stderr)
            failures.append(ch)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/build/test_promote.py -v`
Expected: 3 passed.

- [ ] **Step 5: Add Make target**

Append to `build/Makefile`:
```makefile
.PHONY: promote-chapter promote-all
promote-chapter:
	python build/promote.py --chapter $(ch)
promote-all:
	python build/promote.py --all
```

- [ ] **Step 6: Commit**

```bash
git add build/promote.py tests/build/test_promote.py build/Makefile
git commit -m "build: Phase 4 promotion script with sidecar manifest + hash verification (C3/C11)"
```

### Task 30: Per-chapter promote/reject decision and execution

For each of the 27 chapters in `_voice-drafts/final/`:

- [ ] **Step 1: Diff draft against source**

Run: `git diff --no-index chapters/<part>/<ch>.md chapters/_voice-drafts/final/<ch>.md`

- [ ] **Step 2: Decide PROMOTE or REJECT**

Read the diff. Decide. Record in `.wolf/phase4-decisions.md`:
```markdown
| Chapter | Decision | Reason |
|---|---|---|
| ch01 | PROMOTE | voice tune landed; cadence improved |
| ch15 | REJECT | hallucinated a key derivation step; keep source |
```

- [ ] **Step 3: Execute PROMOTE**

For each PROMOTE:
```bash
make promote-chapter ch=ch01-when-saas-fights-reality
git add chapters/<part>/ch01-when-saas-fights-reality.md chapters/<part>/ch01-when-saas-fights-reality.manifest.json
git commit -m "promote(ch01): voice-pass output replaces source (Phase 4)"
```

- [ ] **Step 4: Execute REJECT**

For each REJECT:
```bash
python build/promote.py --reject ch15 --reason "<reason>"
```

(No file changes; the decision is recorded in `.wolf/phase4-decisions.md` and committed below.)

- [ ] **Step 5: Update ICM markers**

For each PROMOTED chapter, edit the chapter's HTML comment ICM marker to advance from `icm/prose-review` (or wherever) to `icm/voice-check`. Commit per chapter or in one batch.

### Task 31: Phase 4 verification suite

- [ ] **Step 1: Run all build targets**

```bash
make word-count
make draft-pdf
make epub
python build/audiobook.py --all  # (or whatever the audiobook entrypoint is)
```

Expected: all succeed; no chapter outside ±10% target; PDF + EPUB build clean; audiobook MP3s produced for every chapter.

- [ ] **Step 2: Verify F1–F6 conditions**

Walk through `docs/superpowers/specs/2026-04-25-voice-pass-orchestration-design.md` §2 FAILED conditions. Mark each PASS or FAIL.

- [ ] **Step 3: Record decisions**

```bash
git add .wolf/phase4-decisions.md
git commit -m "phase(4): promotion complete; F1-F6 evaluated"
```

---

## Post-completion

### Task 32: Knowledge capture and post-mortem

- [ ] **Step 1: Append lessons to `.wolf/cerebrum.md`**

`## Key Learnings` section:
```markdown
- Voice-pass orchestration completed YYYY-MM-DD. Promote ratio: X/27 promoted, Y rejected.
- Phase 0.5 decision was <X>; reasoning <Y>.
- The Sinek rule that actually caused the mechanical feel was <X> (validates/refutes A1).
- Guest-agent audit results: <summary>.
- Polish vs. normalize tier <was useful / collapsed>.
```

- [ ] **Step 2: Append incidents to `.wolf/buglog.json`**

For any orchestrator failure mode encountered (CLI auth break, safety filter refusal, etc.), append a bug entry per the `.wolf/OPENWOLF.md` schema.

- [ ] **Step 3: Append session log to `.wolf/memory.md`**

One-line entry summarizing the multi-session work.

- [ ] **Step 4: Commit**

```bash
git add .wolf/
git commit -m "post-mortem: voice-pass orchestration complete; learnings captured"
```

### Task 33: Decide post-completion exit (per spec §13)

- [ ] **Step 1: Apply the spec's decision rule**

If ≥3 chapters required REJECT in Phase 4 → recycle through `literary-board` agent.
Else → decide between professional copyedit pass and ship based on calendar pressure.

- [ ] **Step 2: Record decision**

Append to `.wolf/cerebrum.md` `## Decision Log` and commit.

---

## Self-Review Checklist (run before declaring plan done)

The plan author already ran a self-review pass. The implementer should run the same check before the first task:

1. **Spec coverage:** every spec section maps to at least one task above. Phase 0.0 → Tasks 1–3. Phase 0 → 4–10. Phase 0.5 → 11–12. Phase 1 → 13–19. Phase 2 → 20–24. Phase 3 → 25–28. Phase 4 → 29–31. Post-completion → 32–33.
2. **Placeholder scan:** no TBD/TODO/"implement later." Recipes are concrete.
3. **Type consistency:** `load_plan()` returns `dict[str, tuple[str, str]]` after Task 25; all callers updated. `build_prompt()` accepts `mode` after Task 26. `compute_sha256()` and `HashMismatchError` are defined in `build/promote.py`.
4. **No dangling references:** every function called in tests is defined in the same task that creates it.

If the implementer finds a gap on first read, fix it inline and continue.
