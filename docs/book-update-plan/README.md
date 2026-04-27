# Book Update Loop — Index + Quick Start

This directory contains the loopable execution plan for incorporating 10 Volume-1-extension primitives (#9-#12, #43-#48) into the existing book chapters.

## Files

| File | Purpose |
|---|---|
| `README.md` | This file — index + quick-start |
| `loop-plan.md` | The comprehensive plan (12 sections; the loop reads this) |
| `state.yaml` | Operational state across iterations (loop reads + writes every iteration) |
| `working/` | Per-extension working files (outlines, draft notes, review reports) — created by the loop |
| `STOPPED.md` | Created by loop when a kill trigger fires; explains what happened |

## Quick start

### Launch a /loop session in this repo

In a new Claude Code terminal:

```bash
cd C:\Projects\the-inverted-stack
claude
```

Then paste the loop prompt from `loop-plan.md` §9 (full prompt is paste-ready there).

### Watch progress

From any terminal:

```bash
# See iteration history
cat docs/book-update-plan/state.yaml | grep -A 50 "^iterations:"

# See current state of all extensions
cat docs/book-update-plan/state.yaml | grep -A 5 "  status:"

# See recent commits from the loop
git log --oneline --grep="book-update-loop" --since="7 days ago"

# See word-count delta (rough)
make word-count   # if Makefile target exists
```

### Pause the loop

Edit `state.yaml`:

```yaml
kill-triggers:
  user-pause: true
```

The loop will stop on the next iteration and write a `STOPPED.md` explaining why.

### Resume the loop

Edit `state.yaml`:

```yaml
kill-triggers:
  user-pause: false
```

Then re-launch the /loop session (or it resumes if still scheduled).

### Voice-check stops

When an extension reaches `voice-check` stage, the loop stops on that extension and waits for human attention. This is the only stage Claude cannot do.

You'll see in state.yaml:

```yaml
extensions:
  48-key-loss-recovery:
    status: awaiting-voice-check
```

To complete voice-check:

1. Read the relevant chapter section (whichever was just drafted + reviewed)
2. Add personal anecdote, connective tissue, the "this is yours" tone
3. Commit with message format: `voice-check(book-update-loop): <extension-id> voice pass complete`
4. Manually update state.yaml: `current-stage: approved`
5. Loop will pick up the next extension on next iteration

## Estimates

- 10 extensions
- ~70 total iterations (most are 30-90 min; draft iterations 1-2 hours)
- ~50-150 hours of loop work
- ~10 hours of human voice-check time
- Calendar time: 2 weeks to 2 months depending on loop firing cadence

## Coordination with other work

This loop edits BOOK CHAPTERS in `chapters/`. It does NOT touch:
- `docs/` (specs, design decisions, MVP plan, etc.)
- `.claude/` (agents, skills, settings)
- `build/` (build scripts)
- `source/` (source papers — gitignored)

If you do manual chapter edits while the loop is running, pause it first (see "Pause the loop" above) to avoid commit conflicts.
