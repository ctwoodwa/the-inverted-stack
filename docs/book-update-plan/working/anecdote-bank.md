# Anecdote Bank

A working file for personal anecdotes that don't yet have a chapter home but are too good to lose. Each entry includes the raw fact, candidate placements, and a register sketch.

---

## A1 — The recovery-token washers

**Raw fact (from the author):** A SaaS platform used hardware recovery tokens. The author stamped the recovery seed phrase onto metal washers — physical, fire-resistant, durable, multiple copies — going beyond the platform's recommended paper-key approach. The washers still exist. The SaaS platform does not.

**Why it matters:**

This is the book's whole thesis in one personal artifact. The author did everything right — physical durability, redundant copies, defense against fire, water, time, and theft. The recovery layer was bulletproof. What broke was the layer above it: the vendor itself disappeared. With SaaS, even a perfectly engineered recovery cannot survive the platform's exit. With local-first, the same recovery setup outlives the vendor because the data and the keys live on infrastructure the user controls.

The anecdote is rare in being *self-implicating without being a failure story* — the author was thoughtful, durable, and ahead of the curve. The platform failed them.

**Candidate placements:**

1. **Ch15 §Paper-key fallback** — currently makes the abstract argument about durable physical storage. The washers are the concrete realization of that argument and a reminder that paper is not the only durable medium. ~150-word sidebar or paragraph addition.

2. **Ch01 §When SaaS Fights Reality** — Part I's scenario-driven opening. The washers anecdote could anchor a Charles-Conn-equivalent scene where the failure mode is *vendor disappearance* rather than user error. Strongest placement for the book's thesis arc.

3. **Epilogue § What the Stack Owes You** — a closing-image candidate. The washers are still on someone's desk; the platform is dust. That image lands the book's argument.

4. **Ch04 §Choosing Your Architecture** — the deployment-decision chapter. The washers as evidence that the architecture choice (SaaS vs. local-first) constrains what recovery setups can survive.

**Register sketch (Brown, first-person, ~150 words):**

> I once stamped a recovery seed phrase onto a set of metal washers. Stainless steel. Punch-and-letter, the slow way, sitting at a kitchen table with a small hammer. Three of them. I left one in a fireproof box, one in a safe-deposit drawer, one in a friend's apartment three states over. Paper would burn. Paper would water-damage. Metal would not. I was proud of myself, in the small private way of a person who has watched too many people lose seed phrases to ordinary household failures.
>
> I still have the washers. The SaaS platform that issued the recovery token is gone — the company sold, the product wound down, the login servers retired three years after the engagement letter. The washers sit in their three locations, durable and useless. I had built a recovery for the half of the system I controlled. The other half was never mine.

**Register sketch (Lencioni, third-person, ~150 words):**

The washers had been Marcus's idea. Stainless steel, a quarter-inch thick, the seed phrase punched character by character with a hammer and a letter set. Three of them. One in a fireproof box at home, one in a safe-deposit drawer, one in his sister's place out of state. He had read the platform's recommendation — *write it down on paper, store it somewhere safe* — and he had thought: paper burns. He spent a Saturday morning at the kitchen table with the punch set.

Three years later the platform was sold. The login servers were retired the following quarter. The washers were still on his desk. He had built a recovery setup that would survive a house fire, a flood, and most of the next century. It would not survive the company.

**Last updated:** 2026-04-27. Captured before the washers story could evaporate during the #48 voice-pass.
