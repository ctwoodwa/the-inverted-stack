---
description: Run an iterative board-review / resolution cycle on one or more chapters until PUBLISH or an escape condition fires. Invoke as `/review-cycle ch01` or `/review-cycle ch01 ch03 --max-passes 3 --target 8.5`.
---

# Review Cycle — Adversarial Improvement Loop

Run a bounded loop that alternates literary-board review with targeted resolution edits, driving a chapter's score toward PUBLISH without running forever. The loop MUST stop on any escape condition below — the user approves continuation explicitly at each checkpoint.

## Arguments

```
/review-cycle <chapter-id> [<chapter-id>...] [--max-passes N] [--target S] [--quorum Q] [--plateau D] [--auto-apply]
```

- `<chapter-id>` — one or more: `ch01`, `ch03`, `ch11`, etc. Resolves to `chapters/**/<chapter-id>-*.md`
- `--max-passes N` (default **3**) — hard cap on review+resolve iterations per chapter
- `--target S` (default **8.5**) — target aggregate board score; stop when met
- `--quorum Q` (default **9**) — number of individual critics voting PUBLISH needed to exit
- `--plateau D` (default **0.3**) — stop if score delta between two consecutive passes < D
- `--auto-apply` (default **false**) — if set, apply fixes without confirmation after pass 1

## Escape Hatches (ALL active — the loop stops on the FIRST that fires)

1. **MAX_PASSES reached** — hard cap, no exceptions
2. **TARGET score reached** — aggregate ≥ `--target`
3. **PUBLISH quorum reached** — ≥ `--quorum` critics individually vote PUBLISH
4. **PLATEAU detected** — score delta between last two passes < `--plateau`
5. **SINGLE-CRITIC ITEMS ONLY** — if all remaining priority items are single-critic flags, diminishing returns reached; stop
6. **USER HALT** — at every checkpoint the user can type "stop"; the loop exits immediately
7. **WORD BUDGET BLOWN** — if chapter exceeds target by >15%, stop and flag for refactor pass
8. **ERROR DURING EDIT** — if any Edit call fails (old_string not unique, etc.), stop and surface to user

## The Loop

For each chapter, in sequence:

### Pass 0 — Initialization

- Read current chapter state. Record current word count.
- If there's a prior review for this chapter in `reviews/`, record the last score as `prior_score`. Otherwise `prior_score = null`.
- Set `pass = 1`.

### Pass N — Review

- Dispatch the `literary-board` agent on the chapter with full context:
  - Previous scores and trajectory
  - The specific fixes applied since the last pass (if any) — pass them verbatim so critics know what to verify
  - Open items explicitly deferred (so critics don't re-raise them as fresh findings)
  - Instruction to report: aggregate score, per-critic scores, individual PUBLISH votes, priority action items ordered by consensus weight, and an explicit PUBLISH-readiness recommendation
- Record the result. Append to `reviews/<date>-literary-board-reviews.md`.

### Pass N — Escape Check

Evaluate every escape hatch in order:
1. Aggregate score ≥ target? → STOP with verdict PUBLISH-READY
2. PUBLISH-voting critics ≥ quorum? → STOP with verdict PUBLISH-READY
3. `pass >= max_passes`? → STOP with verdict CAP-REACHED (surface remaining items)
4. `prior_score != null` and `current_score - prior_score < plateau`? → STOP with verdict PLATEAU
5. All priority items are single-critic flags? → STOP with verdict DIMINISHING-RETURNS
6. Word count > target × 1.15? → STOP with verdict WORD-BUDGET-BLOWN

If none fire: continue to Resolution.

### Pass N — Resolution

- Extract priority items from the board output. **Only items flagged by 2+ critics this pass are in-scope for automatic resolution**; single-critic items go into a deferred list.
- Present the in-scope items to the user with the proposed edit for each.
- If `--auto-apply` is set AND `pass == 1`: apply without confirmation.
- Otherwise: user confirms go/no-go per item or as a batch.
- Apply approved edits with the Edit tool. If any edit fails, stop and surface.
- Commit with a descriptive message:
  ```
  polish: resolve pass-N board priorities for <chapter-id>

  Items addressed (with flagging critics):
  - ...
  - ...
  ```
- Record the deferred (single-critic) items in the cycle log but do NOT address them.
- Increment `pass`. Return to Review.

### Final

- Print the trajectory: `pass_1_score → pass_2_score → ... → final_score`
- Print the exit verdict and which escape hatch fired
- Print the deferred (single-critic) items for human judgment
- Update `.wolf/memory.md` with the cycle summary

## What the Loop DOES NOT DO

- It does NOT rewrite the chapter structurally. Structural reordering (e.g., Hollis's "move What Changes for the Developer") requires an explicit user instruction; the loop only applies sentence-level or paragraph-level edits.
- It does NOT run without user presence. The user must be available at every checkpoint. This is not an autonomous background job.
- It does NOT chase unanimity. A chapter at 8.5+ with 9+ PUBLISH votes is done. Twelve-of-twelve is a failure mode, not a goal — it indicates the book is being written by committee.
- It does NOT address items deferred by earlier policy decisions (SIer/procurement framing for later chapters, etc.) unless the user explicitly re-opens them.
- It does NOT loop across multiple chapters in parallel. Chapters are sequential to avoid context pollution and to let the user adjust targets mid-run.

## When to Use This Command

**USE when:**
- A chapter is at POLISH (7.5–8.5) and needs one or two targeted passes to reach PUBLISH
- You have budget for 1–3 board reviews and want a structured way to consume it
- The user wants to stay in the loop but doesn't want to hand-hold every fix

**DO NOT USE when:**
- A chapter is at REVISE (below 7) — structural issues need a human pass first
- A chapter is freshly drafted and hasn't had a single board review yet — run a single review, triage with the user, then consider the cycle
- The remaining items are predominantly structural (section reordering, chapter retitles, narrative arc changes)
- The chapter is at REWORK — the loop will not fix a broken thesis

## Dry-Run Mode

If the user invokes with `--dry-run`, run the review but DO NOT apply any edits. Report what would have been applied. Useful for budget estimation or sanity-checking the loop's reasoning.

## Cost Awareness

Each full board review is ~40k tokens. A three-pass cycle on two chapters is roughly 240k tokens. Surface this estimate before the first pass so the user can calibrate.

## Interaction Pattern

```
> /review-cycle ch01 ch03 --max-passes 2 --target 8.7

Estimated cost: 4 board reviews × ~40k tokens = ~160k tokens.
Proceed? (y/n/adjust)

> y

═══ ch01 — pass 1 ═══
[dispatch literary-board...]
Aggregate: 8.6 | PUBLISH votes: 7 | Trajectory: 6.2 → 7.6 → 8.3 → 8.6

Escape check: target=8.7 not met, quorum=9 not met, pass<max, no plateau (+0.3 = plateau edge).
Priority items (≥2 critics):
  1. 242-FZ "first major" → "among the first general-purpose" (5 critics)
  2. Transitional sentence Third-Party Veto → Who Pays the Most (3 critics)
  3. SCC-adequacy-contested sentence for Schrems II (2 critics — Barker, Osei)

Apply all three? (y/n/select)

> y

[Edit × 3]
[git commit]

═══ ch01 — pass 2 ═══
...
```

## Logging

The cycle appends to `.wolf/memory.md`:

```
| HH:MM | review-cycle ch01 pass 1 | ch01 | 8.6/10 POLISH (+0.3) | ~42k |
| HH:MM | review-cycle ch01 pass 1 resolution | ch01 | 3 items applied | ~2k |
| HH:MM | review-cycle ch01 pass 2 | ch01 | 8.9/10 PUBLISH-READY | ~41k |
| HH:MM | review-cycle ch01 EXIT: TARGET REACHED | ch01 | 8.9/10 (target 8.7) | — |
```
