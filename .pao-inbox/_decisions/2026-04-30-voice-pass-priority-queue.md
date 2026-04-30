---
type: pao-deliverable
date: 2026-04-30
author: PAO
audience: CO (when ready to do Stage 6 voice-pass)
status: queue ordered by cost-of-delay
purpose: orient CO across the 9 extensions awaiting voice-pass without requiring a full state.yaml read
---

# Voice-Pass Priority Queue

## TL;DR

9 extensions sit at `awaiting-voice-check` per `docs/book-update-plan/state.yaml`. All gate Phase 7 of the Ch15 split UPF + the manuscript's full assembly. **Voice-pass is human-only** (CLAUDE.md Stage 6); PAO cannot do it. This queue orders the 9 by cost-of-delay so CO can pick the highest-leverage one when they sit down.

Each extension's working artifacts (outline.md §F or §E "Voice-Check Focus") have the candidate anecdote framings, connective-tissue prompts, and Sinek-calibration notes. Working dirs:
`docs/book-update-plan/working/<extension-id>/`

## Cost-of-delay ranking

### Tier 1 — Voice-pass directly unblocks structural work (do first)

**#45 — Collaborator Revocation** (Ch23 §Collaborator Revocation; was Ch15 pre-split)
- **Why first:** Voice-pass on this section UNBLOCKS Phase 4 prune of Ch23 (~400 words deeper compression). That prune is the last gate on closing the UPF Ch15 split and bringing Ch23 to its target word count. Single highest-leverage voice-pass for the manuscript's overall trajectory.
- **What it needs:** Departure-moment anecdote (3 candidate framings: departing employee packing a desk; business partner reading access-ended message after court-mediated settlement; administrator processing access revocation for long-time colleague). Plus Ch23↔Ch20 connective tissue, light Sinek calibration.
- **Where:** `docs/book-update-plan/working/45-collaborator-revocation/outline.md` §F. HTML placeholder `<!-- voice-check: -->` already in Ch23 chapter at the departure-moment scene.

**#43 — Performance Contracts** (Ch11 §Performance Contracts + Ch20 §Performance Budgets)
- **Why second:** Affects two Part-III/IV chapters. After voice-pass, Ch11 §Performance Contracts becomes available for compression (~200 words available). Cross-chapter pairing visible to readers.
- **What it needs:** Anecdote opener (3 candidates: developer can't lag Linear; CRDT merge freezes UI / force-quit moment; Apple HIG 16ms framing). Plus Ch11↔Ch20 connective tissue. 2 non-blocking `<!-- CLAIM: -->` markers (Linear 60fps source URL, Apple HIG 16ms source URL).
- **Where:** `docs/book-update-plan/working/43-performance-contracts/outline.md` §F.

**#11 — Fleet Management** (Ch21, entire chapter)
- **Why third:** Whole Ch21 is post-voice-pass; readers' first impression of Part V depends on the anecdote landing.
- **What it needs:** Opening-hook anecdote (3 candidates listed in `working/11-fleet-management/draft.md` QC notes). Plus sharpening the provisioning-as-cultural-shift moment + light Sinek calibration + optional connective-tissue line at close of §21.6 fleet-failure narrative.
- **Where:** `docs/book-update-plan/working/11-fleet-management/outline.md` §F.

### Tier 2 — Voice-pass unblocks chapter compression (do as bandwidth allows)

**#44 — Per-Data-Class Device-Distribution** (Ch16 §Per-Data-Class Device-Distribution)
- **Why:** Voice-pass unlocks deeper Ch16 compression (~300 words). Ch16 currently at 218% target.
- **What it needs:** Anecdote opener for the heterogeneous-fleet framing (restaurant floor-tablet vs back-office-laptop scenario already drafted in chapter; needs author's opening anchor).
- **Where:** `docs/book-update-plan/working/44-per-data-class-device-distribution/`.

**#46 — Forward Secrecy** (Ch22 §Forward Secrecy and Post-Compromise Security)
- **Why:** Voice-pass unlocks Ch22 prune (~150 words).
- **What it needs:** Per outline §E, anecdote anchor for the property — "captured today exposes nothing about yesterday or tomorrow." Author's framing.
- **Where:** `docs/book-update-plan/working/46-forward-secrecy/outline.md` §E.

**#47 — Endpoint Compromise** (Ch23 §Endpoint Compromise)
- **Why:** Voice-pass unlocks Ch23 prune (~200 words).
- **What it needs:** Anecdote framing for the "what stays protected when the OS itself is hostile" claim. Author's framing.
- **Where:** `docs/book-update-plan/working/47-endpoint-compromise/outline.md` §F.

### Tier 3 — Voice-pass closes the extension; modest compression unlock

**#9 — Chain-of-Custody** (Ch23 §Chain-of-Custody for Multi-Party Transfers)
- **Why:** Closes #9; modest compression unlock (~100 words). The dashcam handoff scenario is already drafted; author voice-pass adds the framing.
- **Where:** `docs/book-update-plan/working/9-chain-of-custody/outline.md` §F.

**#10 — Data-Class Escalation** (Ch23 §Event-Triggered Re-classification)
- **Why:** Closes #10. Restaurant-collision claim → footage escalation scenario already drafted.
- **Where:** `docs/book-update-plan/working/10-data-class-escalation/`.

**#12 — Privacy-Preserving Aggregation** (Ch15 §Privacy-Preserving Aggregation at Relay)
- **Why:** Closes #12. This section stayed in Ch15 (architectural). Differential-privacy framing is already complete; author voice-pass is light.
- **Where:** `docs/book-update-plan/working/12-privacy-aggregation/`.

## Process per extension (CLAUDE.md Stage 6)

For each extension picked off the queue:

1. Read the working dir's outline.md §F (or §E for #46) for candidate anecdote framings.
2. Pick one (or write your own) — the anecdote belongs at the section opener and grounds the technical claim in lived experience.
3. Insert at the marked location in the chapter (or where the prose currently lacks the anchor).
4. Light Sinek calibration per `~/.claude/projects/-Users-christopherwood-.../memory/feedback_voice_sinek_calibration.md` — don't over-mechanize.
5. Add the connective-tissue line where the extension pairs cross-chapter (Ch11↔Ch20 for #43, Ch23↔Ch20 for #45, etc.).
6. Commit. Yeoman or PAO promotes the extension `awaiting-voice-check → approved` in state.yaml afterward.

Total estimated time per extension (CO active session): 30–60 min. The 9 extensions ≈ 5–8 hours of focused author work, parallelizable across sessions.

## What's queued post-voice-pass (PAO-side)

Per `2026-04-30-word-count-target-revision-proposal.md`:
- Phase 4 prune of Ch22 + Ch23 (~3,000 words) — runs after #45 + #46 + #47 voice-pass
- Author-judgment cuts on Ch12, Ch16, Ch19 (~700 words combined) — needs CO call separately
- Cross-chapter connective-tissue verification — runs after voice-pass insertions land

---

**Status: queue ordered; CO picks at next focused session. PAO continues in /loop, not blocking on this.**
