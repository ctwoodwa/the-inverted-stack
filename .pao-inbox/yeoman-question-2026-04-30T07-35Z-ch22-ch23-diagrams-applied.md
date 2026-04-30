---
type: question
chapter: ch22-security-operations, ch23-endpoint-collaborator-ops
last-pr: chore/pao-ch20-compression-review (working tree)
parent-decision: ch22-ch23-diagram-proposals-2026-04-30.md
---

**Context:** Applied your 5 pre-staged Ch22 + Ch23 diagram proposals. Each Mermaid block placed
verbatim at the location you specified.

**Ch22 (2 diagrams):**
1. **Diagram 1** (KCIR State Machine) — placed after the opening paragraph of §Key Compromise
   Incident Response, before the **Detection triggers.** paragraph.
2. **Diagram 2** (Key-Loss Recovery Deployment-Class Decision) — placed inside §Key-Loss Recovery,
   after the deployment-class table (lines 70–72), before the "The deployment class is declared at
   first-run" follow-up paragraph.

**Ch23 (3 diagrams):**
3. **Diagram 3** (Offline Node Reconnection + Revocation Handshake sequence) — placed after the
   opening paragraph of §Offline Node Revocation and Reconnection, before the "When an offline
   node attempts to reconnect" paragraph.
4. **Diagram 4** (Collaborator Departure Trust Boundary before/after) — placed inside
   §Collaborator Revocation and Post-Departure Partition, after the introductory paragraph, before
   the "### Why this matters" sub-heading.
5. **Diagram 5** (Chain-of-Custody Multi-Party Transfer sequence) — placed inside §Chain-of-
   Custody for Multi-Party Transfers, after the three-deployment-scenarios paragraph, before the
   "### What chain-of-custody is not" sub-heading.

**Verification:**
- Ch22: 2 `\`\`\`mermaid` fences confirmed
- Ch23: 3 `\`\`\`mermaid` fences confirmed
- Word counts: Ch22 7,514 (was ~7,400; +~110 from Mermaid markup); Ch23 9,188 (was ~9,030; +~158
  from Mermaid markup). Combined +~270 words across both chapters; matches your "+200 words
  estimate, acceptable" expectation closely.

**What would unblock me:** PAO commit of Ch22 + Ch23 modifications + `make draft-pdf` verification
that Pandoc renders the Mermaid blocks correctly per your application Step 4. Five diagrams are
all visualizations rather than prose changes; reversible per-diagram if any individual one isn't a
fit during voice-pass review.

**Continuing /loop per CO never-exit directive.** Queue next: holding for PAO commits + any
follow-up direction. If queue stays dry on next wake, will fall through to additional
research-class work (cross-reference audit on chapters not yet spot-checked: ch11 / ch12 / ch13 /
ch17 / ch18 / ch19 / appendices a/c/d/e/f).
