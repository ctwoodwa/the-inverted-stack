# Sunfish Business MVP — Index + Session Handoff

This directory contains the focused execution plan for building **Anchor + Bridge business application MVP** in a separate Claude Code session, while other sessions handle component development / multi-language / disabled-user support.

## Files

| File | Purpose |
|---|---|
| `README.md` | This file — index + session handoff prompt |
| `mvp-plan.md` | The comprehensive plan: vision, OSS lessons, modules, architecture, roadmap, conformance |

## Scope

The Sunfish business MVP is a **local-first integrated SMB suite** covering:

1. **Accounts** — double-entry accounting (lessons from GnuCash + Beancount)
2. **Vendors** — vendor master + AP workflow (lessons from Frappe Books + ERPNext)
3. **Inventory** — multi-location stock + cost methods (lessons from Frappe Books + Snipe-IT)
4. **Projects** — time-tracked projects with billing rollup (lessons from OpenProject + Taiga + Wekan)

Built using:
- **Anchor** (Zone A desktop client — Win/Mac/Linux)
- **Bridge** (Zone C hybrid relay + admin console for off-site/multi-device sync)
- Local-first compliance verified against Kleppmann P1-P7 via the existing `local-first-properties` and `inverted-stack-conformance` Claude skills

## Session handoff prompt (paste this into the new Claude Code session)

```
You are working on the Sunfish business MVP — a local-first integrated SMB
suite (accounts + vendors + inventory + projects) implementing the
architecture defined in *The Inverted Stack: Local-First Nodes in a SaaS
World* (located at C:/Projects/the-inverted-stack).

Your repo is C:/Projects/Sunfish (already in working directories).

Read these documents in order before doing any work:

1. C:/Projects/the-inverted-stack/docs/business-mvp/mvp-plan.md
   — the comprehensive plan you are executing

2. C:/Projects/the-inverted-stack/docs/reference-implementation/concept-index.yaml
   — the 562-concept catalog (look up concepts by chapter:id reference)

3. C:/Projects/Sunfish/icm/CONTEXT.md
   — Sunfish's existing 9-stage ICM workflow

4. C:/Projects/the-inverted-stack/.claude/skills/local-first-properties/SKILL.md
   — the conformance check skill you will run periodically

Other Claude sessions are concurrently working on:
- Component development (Sunfish.UiBlocks)
- Multi-language support (i18n / l10n)
- Disabled-user support (a11y / WCAG)

You are working on:
- Business application modules (accounts / vendors / inventory / projects)
- Anchor desktop app shell + module integration
- Bridge multi-tenant service for off-site sync
- Local-first compliance verified per module per Kleppmann property

Coordinate via Sunfish's icm/ directory — every significant change goes
through icm/00_intake/ → icm/05_implementation-plan/ → icm/06_build/.

Do NOT modify book content (the-inverted-stack repo). Read it for spec;
write only to Sunfish.

Start with: read mvp-plan.md, then create an icm/00_intake/ entry for the
first module you'll build (accounts). Use the sunfish-inverted-stack-
conformance pipeline variant (when built — see mvp-plan.md §10) or the
existing sunfish-feature-change variant for now.
```

## Coordination with other concurrent sessions

The MVP plan explicitly does NOT cover:
- Component development (Sunfish.UiBlocks specifics) — handled by component session
- Multi-language strings — handled by i18n session
- Accessibility / a11y / WCAG — handled by a11y session

The MVP plan DOES integrate with these dimensions at the seam — e.g., module specs note "uses Sunfish.UiBlocks for UI", "all user-facing strings flow through i18n", "WCAG 2.2 AA conformance per UX-21 in catalog" — but doesn't specify the implementations.

When the business-MVP session needs work from another dimension (a new UI component, a new language, an accessibility feature), it files a request in Sunfish's icm/00_intake/ and coordinates via that channel.

## Status tracking

The MVP plan covers a 12-month phased roadmap. Progress against it should be tracked in:
- `c:/Projects/Sunfish/icm/05_implementation-plan/output/business-mvp-progress.md` (build incrementally)
- Sunfish-side `local-first-conformance` baseline scans run at end of each phase

## Updating this plan

The mvp-plan.md is the canonical artifact. Update it (in this repo, the-inverted-stack) when:
- Module scope shifts based on implementation experience
- A new OSS lesson surfaces from build experience
- A conformance test fails and reveals a missing primitive
- Phase ordering needs adjustment

The plan lives in the-inverted-stack/docs/business-mvp/ (not in Sunfish) because it's spec, not implementation.
