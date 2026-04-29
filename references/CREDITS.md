# Audiobook voice credits

The audiobook for *The Inverted Stack* is narrated by `broom_salesman`,
a stock voice that ships with the Chatterbox TTS server (Resemble AI).
Author decision 2026-04-28: a single universal narrator across all
parts (I/III/IV/Epilogue/Preface AND the Part II council chapters)
gives a more cohesive listening experience than per-persona voicing.

The cloned LibriVox voices below are **preserved on the TTS server and
documented here** as reference material in case the author chooses to
regenerate specific chapters with per-persona voicing later. They are
NOT currently wired into the production audiobook.

LibriVox recordings are released into the **public domain (CC0)**. Per
LibriVox's terms ([librivox.org/pages/public-domain](https://librivox.org/pages/public-domain/)),
credit is **not legally required** but is preferred. This file is the
canonical credits manifest for every LibriVox source we have uploaded.

> "There is no need to credit LibriVox, although of course we much prefer
> if you do credit us (with a link to our site)."
> — LibriVox public-domain page

## How attribution is captured

Three layers, each independent:

1. **This file (`references/CREDITS.md`)** — version-controlled credits in
   the repo. The canonical record. Updated whenever a new voice is uploaded.
2. **TTS server `notes` field on each uploaded voice** — same attribution
   embedded in the voice catalog itself, accessible via
   `GET /v1/audio/voices/{voice_id}` (server at `desktop-umt08rn:8881`).
3. **Audiobook end credits** *(planned)* — when the full audiobook is
   assembled into the final M4B, an end-credits track names every reader
   + LibriVox source verbally.

## Voice catalog (custom uploads — preserved for optional per-chapter regen)

Each entry below names: the voice ID on the TTS server, the persona it
was originally trialed against, the LibriVox source book, the reader,
the specific section + time window from which the 28-second reference
clip was extracted, and links back to the LibriVox book and reader
pages. **None of these voices are currently in `PRESETS_CHATTERBOX`** —
the preset map points all slots at `broom_salesman` (stock). To
resurrect a per-chapter cloned voice, either pass `--voice <id>` to
`audiobook.py` for the specific chapter render, or update the
corresponding preset slot in `PRESETS_CHATTERBOX`.

### `voss-trial-savage`

- **Persona:** Dr. Marguerite Voss — Ch05 The Enterprise Lens (F, executive)
- **Source book:** *Pride and Prejudice (version 3)* by Jane Austen
- **LibriVox book:** <https://librivox.org/pride-and-prejudice-by-jane-austen-2/>
- **Reader:** Karen Savage
- **LibriVox reader profile:** <https://librivox.org/reader/103>
- **Reference clip:** §1 (Chapter 01), window 1:00–1:28 (28 sec)
- **License:** Public domain (CC0)

### `shevchenko-trial-yakovlev`

- **Persona:** Dr. Dmitri Shevchenko — Ch06 The Distributed Systems Lens (M, Slavic, distributed-systems theorist)
- **Source book:** *Записки из подполья (Notes from the Underground)* by Fyodor Dostoyevsky
- **LibriVox book:** <https://librivox.org/zapiski-iz-podpolya-by-fyodor_dostoevsky/>
- **Reader:** Yakovlev Valery
- **LibriVox reader profile:** <https://librivox.org/reader/295>
- **Reference clip:** §2 (Part 1, Chapter 3-4), window 1:00–1:28 (28 sec)
- **License:** Public domain (CC0)

### `okonkwo-trial-klett`

- **Persona:** Adaeze Okonkwo — Ch07 The Security Lens (F, security expert)
- **Source book:** *Persuasion (version 2)* by Jane Austen
- **LibriVox book:** <https://librivox.org/persuasion-by-jane-austen-2/>
- **Reader:** Elizabeth Klett
- **LibriVox reader profile:** <https://librivox.org/reader/1259>
- **Reference clip:** §1 (Chapter 01), window 1:00–1:28 (28 sec)
- **License:** Public domain (CC0)
- **Note on accent:** the persona is Nigerian-English. LibriVox catalog
  has no Nigerian-English solo female reader; Klett (American/measured
  English) was chosen for register-fit (security-expert posture), not
  accent. A future custom recording or VA hire may revisit this.

### `kelsey-trial-smith`

- **Persona:** Jordan Kelsey — Ch08 The Product & Economic Lens (M, polished corporate)
- **Source book:** *Sense and Sensibility (version 2)* by Jane Austen
- **LibriVox book:** <https://librivox.org/sense-and-sensibility-version-2-by-jane-austen/>
- **Reader:** Mark F. Smith
- **LibriVox reader profile:** <https://librivox.org/reader/204>
- **Reference clip:** §1 (Chapter 01), window 1:00–1:28 (28 sec)
- **License:** Public domain (CC0)

### `ferreira-trial-rogeriom`

- **Persona:** Tomás Ferreira — Ch09 The Local-First Practitioner Lens (M, Lusophone, practitioner)
- **Source book:** *Iracema* by José de Alencar (José Martiniano de Alencar)
- **LibriVox book:** <https://librivox.org/iracema-by-jose-de-alencar/>
- **Reader:** RogerioM
- **LibriVox reader profile:** <https://librivox.org/reader/10107>
- **Reference clip:** §2 (Capítulos 6 a 10), window 1:30–1:58 (28 sec)
- **License:** Public domain (CC0)

## Stock voice (Chatterbox built-in) — universal narrator

The Chatterbox TTS server ships with 16 stock voices originally sourced
from the upstream model's training data. **One** stock voice is wired
into `PRESETS_CHATTERBOX` for the audiobook pipeline:

- **`broom_salesman`** — older British male, deliberate cadence
  (Ollivander register from the upstream sample set). The universal
  narrator for the entire audiobook per author decision 2026-04-28.
  Pair with V12 dramatic recipe (`--exaggeration 0.7 --cfg-weight 0.3`)
  for narrative-driven chapters (Part I, Epilogue); use neutral params
  (omit both flags) for specification chapters (Part III) where the
  reader's natural pacing is enough.

Stock voices are not LibriVox-sourced and not subject to the LibriVox
attribution preference. Their license terms are governed by the
Chatterbox/Resemble AI model release.

## When this file changes

- **A new LibriVox voice is uploaded** → add a section above with
  persona + source book + reader + URLs + clip window
- **A trial voice is promoted** (e.g., `ferreira-trial-rogeriom` →
  `ferreira`) → keep the same attribution; just rename the voice ID
- **A voice is replaced or deleted** → remove the section AND issue
  `DELETE /v1/audio/voices/<id>` against the server so the catalog stays
  consistent
- **The audiobook is published** → embed an end-credits track that names
  every reader + book + LibriVox URL aloud (matches the M4B production
  step planned in `build/m4b.py`)

## Cross-references

- LibriVox public-domain page (license terms): <https://librivox.org/pages/public-domain/>
- LibriVox project home: <https://librivox.org/>
- Project Gutenberg (source texts for transcripts): <https://www.gutenberg.org/>
- Mac client guide for the TTS server: `~/Library/CloudStorage/Dropbox/ideas/notes/the-inverted-stack/mac-client-guide.md`
- Voice catalog operations: `build/voice_upload.py` (list/get/put/delete)
- LibriVox sift workflow: `build/librivox_browse.py` (search/sections/preview/extract)
