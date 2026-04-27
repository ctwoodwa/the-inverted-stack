# Voice-pass connective-tissue candidates — Ch15 ↔ Ch20

Per outline §F voice-check task #2: "Add the connective tissue between Ch15 §Key-Loss Recovery and Ch20 §Key-Loss Recovery UX — a sentence in each pointing to the other so the reader recognizes the policy/UX pairing."

The existing prose already has cross-references in both directions, but they read as routine pointers. The voice-pass connective tissue should land more deliberately — naming the *policy/UX pairing* as a deliberate architectural split, so the reader carries that frame into both sections.

Three candidates per direction. Pick one, edit, or use as a creative prompt to write your own.

---

## Direction 1 — Ch15 → Ch20

**Insertion point:** end of the opening paragraph at line 119 of Ch15, immediately after "in the loss case, the user is the unknown party and the system must verify them before granting access."

### Candidate 1A — Direct policy/UX naming

> This section specifies the policy layer — the cryptographic constructions, the threat model, the deployment combinations, and the convergence rules under which a recovery completes or halts. Ch20 §Key-Loss Recovery UX is the paired surface that turns each policy decision here into a flow the user walks through. Read both as a unit. The cryptography in this chapter has no architectural meaning unless the UX in the next one makes it operable.

*Three sentences. Calibrated to the spec-voice register of the rest of Ch15. Names the pairing explicitly without breaking voice. Suitable if you want the reader to hold the split as a deliberate architectural choice from the first paragraph.*

### Candidate 1B — Quieter, single sentence

> The policy decisions that follow — the six mechanisms, the threat model, the deployment-class table, the convergence rule — each correspond to a user-visible flow specified in Ch20 §Key-Loss Recovery UX, which is the paired surface for everything in this section.

*One sentence. Lighter touch — slips into the existing rhythm without a full pause. Suitable if you want the linkage acknowledged but not foregrounded.*

### Candidate 1C — Reader-aware (acknowledges the split is unusual)

> Recovery is one of the few subjects in this book that splits cleanly into a policy chapter and a UX chapter — the two are paired by design. This section specifies what the architecture commits to. Ch20 §Key-Loss Recovery UX specifies what the user sees when those commitments engage. Each sub-section here has a counterpart there; readers who skim one without the other miss the point of either.

*Four sentences. The most foregrounded version — flags the policy/UX split as deliberate so the reader knows to read both. Suitable if you want to teach the reader how to navigate the rest of Part III/IV pairings (e.g., #43 will follow the same pattern, as will subsequent extensions).*

---

## Direction 2 — Ch20 → Ch15

**Insertion point:** the existing opening paragraph at line 180 of Ch20 already mentions Ch15. The voice-pass either replaces or extends that paragraph. Current text:

> Key-loss recovery has a policy layer and a UX layer. Ch15 §Key-Loss Recovery specifies the six mechanisms, the threat model, and the recommended deployment combinations. This section covers the flows that surface that policy at setup time, the experience of initiating recovery after loss, and the UX for the grace period that protects against fraudulent claims.

### Candidate 2A — Strengthen the existing paragraph

Replace the existing two-sentence opening with:

> Key-loss recovery splits across a policy chapter and a UX chapter, paired by design. Ch15 §Key-Loss Recovery specifies the cryptographic constructions, the deployment combinations, and the convergence rules — the layer the architecture commits to. This section is the layer the user sees: setup-time flows, recovery initiation after loss, the grace-period experience, and the completion confirmation that closes the loop. Each subsection here has a counterpart there; the two are read together or not at all.

*Four sentences. Mirrors the structure of Ch15's Candidate 1C — if you pick one, pair it with the matching candidate in the other direction for symmetry. Most foregrounded version.*

### Candidate 2B — Light addition to existing opening

Keep the existing two-sentence opening, then add one new sentence:

> Key-loss recovery has a policy layer and a UX layer. Ch15 §Key-Loss Recovery specifies the six mechanisms, the threat model, and the recommended deployment combinations. **This pairing is deliberate: every cryptographic construction in Ch15 has a corresponding flow specified here, and reading either alone misses what the architecture is actually doing.** This section covers the flows that surface that policy at setup time, the experience of initiating recovery after loss, and the UX for the grace period that protects against fraudulent claims.

*One inserted sentence (bold above). Suitable if you want minimal disruption to the existing opener but still want the pairing claim made explicitly.*

### Candidate 2C — Quietest version

Append one sentence to the existing opening paragraph (no replacement):

> ... This section covers the flows that surface that policy at setup time, the experience of initiating recovery after loss, and the UX for the grace period that protects against fraudulent claims. **Each flow below is paired with a specific Ch15 sub-section; cross-references in the prose name the partner section at each pivot.**

*One appended sentence. Lightest touch — doesn't reshape the opener; just adds a note that the cross-references are deliberate.*

---

## Recommended pairings

If you want the pairing foregrounded as a deliberate architectural choice (recommended for the book's voice principle "name the structure before the substance"):

- **1C + 2A** — both four-sentence treatments, mirror each other across the pair.

If you want a lighter touch:

- **1B + 2B** — single inserted sentence in each direction, low disruption.

If you want minimum prose change:

- **1A + 2C** — three-sentence Ch15 + one-sentence-append Ch20.

Pick by the register that fits how prominent you want the pairing to feel. The book pairs Ch11/Ch20 (architecture/UX) and Ch15/Ch20 (security/UX) explicitly elsewhere — this voice-pass either reinforces that pattern or simply notes it.

---

## Notes on placement

- Ch15 candidates 1A/1B/1C all insert at end of the opening paragraph (after "system must verify them before granting access"). The opening's existing four-sentence rhythm has room for one more sentence; the three-sentence and four-sentence variants would make the paragraph longer than the others in the section, but still under the 6-sentence cap.
- Ch20 candidate 2A replaces the existing first paragraph entirely; 2B and 2C extend it.
- All candidates preserve the existing cross-reference link to Ch15 §Key-Loss Recovery (it was already there).
