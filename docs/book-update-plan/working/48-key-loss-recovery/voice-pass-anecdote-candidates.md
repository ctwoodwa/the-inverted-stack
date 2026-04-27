# Voice-Pass Anecdote Candidates — Ch15 §Key-Loss Recovery

These are three candidate scene openings (~200 words each) for the human author to choose from
when adding the personal-anecdote layer to Ch15 §Key-Loss Recovery.

**How to use this file:**
Pick one candidate, edit it for accuracy to your own life or to a story you want to tell,
and insert it between the `## Key-Loss Recovery` heading (Ch15, line 117) and the existing
opening sentence "Incident response handles the case where an attacker compromises a key."
Or use the candidates as a creative prompt to write your own from scratch.

The scenes are written in pure Lencioni register: named characters, dialogue, tension
through behavior, no authorial announcement of the moral. The principle — that key loss is
data loss, and the only question is whether you planned for it — lands by implication, not
by statement. The transition notes below each candidate explain how the scene hands off to
the existing architectural prose.

---

## Candidate A — The Forgotten Master-Password

It was a Saturday in November, two days after the new laptop arrived, when Elena finally
sat down to finish the migration.

She had done everything right. She had backed up the old machine. She had exported her
browser profile. She had transferred the photos. The last thing on the list was the
password manager, and she opened it on the old machine to verify the export before
wiping it.

The prompt asked for her master password.

She typed the phrase she always used. Incorrect.

She tried the variation with the capital letter. Incorrect.

She sat with her hands in her lap. The house was quiet. Her husband walked in from the
kitchen, coffee in hand, and looked at her face.

"What's wrong?"

"I can't remember it," she said. "The one password I needed to remember."

He sat down across from her. "What does it protect?"

She thought for a moment. "Everything."

She clicked through to the recovery screen. It asked for her emergency kit — the printed
sheet she had been prompted to save when she first set the account up, two years ago. She
did not have it. She had closed that dialog. She had meant to print it later.

---

**Transition note:** Elena's situation is not a software failure. The password manager
worked exactly as designed — her key, her custody, her loss. The scene sets the emotional
ground for the architectural claim that follows: key loss is not an edge case. It is the
honest edge of the P7 ownership property. The existing opening — "Incident response handles
the case where an attacker compromises a key. Key-loss recovery handles the case where the
legitimate user loses one." — lands harder after the reader has already felt what
*legitimate user loses one* means.

---

## Candidate B — The Executor's Second Loss

Daniel found the drives in the third box he opened.

His father had died in March — quickly, which was a mercy — and by late April Daniel was
working through the study. Two external drives, a laptop with a broken hinge, and a folder
of papers that turned out to be mostly cable receipts. He recognized the drives. His father
had been meticulous about backups. That, at least, was a relief.

He plugged in the first drive. An encrypted container. A password prompt.

He called his sister. "Do you know if Dad left any passwords written down anywhere?"

A long pause. "There might be something in the filing cabinet. Under the stairs."

There was nothing under the stairs. There was a sticky note on the bottom of the keyboard
tray that had three passwords on it — none of them matched.

The drives had photographs. Forty years of them, Daniel guessed. His father had been
converting slides from before Daniel was born. They were there. He just could not reach
them.

He sat on the floor of the study for a while. He was not sure what he was grieving, exactly.

---

**Transition note:** The second loss is quieter than the first — the photographs were
never gone, only locked. That distinction is the emotional center of what follows. The
existing architectural prose opens with two scenarios that look superficially similar and
differ in one critical way; Daniel's story gives the reader a felt sense of the difference
before the section names it. The scene also surfaces the succession scenario — one of the
five real-world failure modes the section enumerates — so the reader recognizes it when it
appears in the list rather than encountering it for the first time as an abstraction.

---

## Candidate C — The Missing Hardware Token

Marcus noticed it was gone on a Monday morning, standing at his desk with his badge in one
hand and his laptop bag in the other.

He had moved apartments over the weekend. He was a careful packer. The YubiKey had been
in the small zippered pocket of the bag — he was sure of that — and now it was not.

He checked three times. He checked the old apartment. He drove back on his lunch break.

His colleague Priya was in the kitchen when he came back.

"What happened to you?" she asked.

"Lost my key," Marcus said. "The hardware one. For the signing certificates."

She looked at him. "The repository signing key?"

"And the deployment credentials. And the encrypted backups."

Priya set down her coffee. "When did you last push a backup?"

He thought about it. "Before the move. So — Friday."

"Is it recoverable?"

Marcus had set up the recovery path eighteen months ago, when he first started the project.
He had registered a backup code and left it in his notes app. He opened his laptop and
searched. The note was there. He let out a breath.

"I think so," he said. "But I had forgotten I'd done that."

---

**Transition note:** Marcus's story ends with relief rather than loss — which is exactly
the point. The recovery worked because he had set it up before he needed it. The scene
creates a concrete referent for the section's core design argument: a recovery primitive
must be in place before the event. The existing opening that follows — distinguishing
compromise from loss, attacker-unknown from user-unknown — carries more weight when the
reader has just watched a user nearly become the unknown party.
