# Audio QA Fixtures

A curated test set of "hard sentences" for the audiobook TTS pipeline. Render
this file with the audiobook script after every change to `build/audiobook.py`,
then listen for regressions in pronunciation, prosody, or pacing.

To render this fixture as a single MP3:

```bash
python build/audiobook.py --only audio-fixtures --force
```

To compare chunk-mode vs sentence-mode prosody:

```bash
python build/audiobook.py --only audio-fixtures --force                  # chunk
python build/audiobook.py --only audio-fixtures --force --per-sentence   # sentence
```

The expected pronunciations are in inline comments. Update the comments only
after a deliberate decision — they are the contract the audiobook script must
satisfy.

---

## Council member names

Shevchenko reviewed the architecture twice. <!-- shev-CHEN-koh -->

Okonkwo brought twenty years of healthcare-security experience. <!-- oh-KONK-woh -->

Tomás Ferreira sat across from non-technical users. <!-- toh-MAHS feh-RAY-rah -->

Kelsey scored unit economics 8 out of 10. <!-- KEL-see -->

Voss does not issue scores generously. <!-- VOSS -->

---

## Acronyms and technical terms

The CRDT engine handles convergence; the AP/CP split governs consistency. <!-- C-R-D-T, A-P / C-P -->

Sunfish uses YDotNet today; Loro is the aspirational primary engine. <!-- Y-dot-Net, LORE-oh -->

Build with .NET MAUI Blazor Hybrid for Anchor and ASP.NET for Bridge. <!-- MOW-ee, ASP dot NET -->

DEK and KEK form the envelope encryption hierarchy. <!-- D-E-K, K-E-K -->

Run CI/CD with reproducible SBOM generation and SignalR for real-time. <!-- C-I C-D, S-bom, Signal-R -->

Deploy via gRPC over WebAssembly with SQLCipher at rest. <!-- G-R-P-C, Web Assembly, SQL Cipher -->

---

## Roman numerals after "Part"

Part I introduces the thesis. Part II runs the council review.
Part III specifies the architecture. Part IV is the playbook.
<!-- "Part 1" "Part 2" "Part 3" "Part 4" — never "Part eye-eye" -->

---

## Jurisdictions and regulations

GDPR Article 17 and Schrems II shape the European compliance posture.
<!-- shrems -->

DPDP, UAE DPL, DIFC DPL, NDPR, POPIA, PIPL, Japan PIPA, Korea PIPA, and
Federal Law 242-FZ are the global compliance frame. <!-- read as letters -->

Roskomnadzor enforced 242-FZ against LinkedIn in 2016. <!-- ros-kom-NOD-zor -->

ANPD oversees LGPD compliance in Brazil. <!-- A-N-P-D -->

---

## Numbers, currency, percentages

The relay scales to 100M+ records. <!-- "100M plus records" — left as M -->

Cost stays under $10K per month at 20% margin. <!-- ten thousand dollars, twenty percent -->

Linear claims $30M ARR with 5,000+ enterprise customers. <!-- thirty million dollars, five thousand plus -->

Compliance turnaround: 72-hour notification, 24-hour for high-risk breaches.
<!-- seventy-two-hour, twenty-four-hour -->

---

## Abbreviations

The lease protocol fails under partition (i.e., split-brain),
e.g., a network partition during CAPABILITY_NEG, etc. <!-- "that is", "for example", "and so on" -->

Compare cf. Flease and Raft (vs. Paxos) for the consensus baseline.
<!-- compare, fleeze, versus -->

Standby maintenance window: 2:00 a.m. to 5:00 a.m. <!-- A-M -->

---

## Inline ordinal markers

Three priorities: (1) the relay handles enterprise scale,
(2) Schrems II compliance is non-negotiable, (3) operating cost stays
under target. <!-- "First," "Second," "Third," — not "left-paren one right-paren" -->

---

## Em-dash, en-dash, smart quotes

The architecture — as the council observed — clears Round 2 with conditions.
<!-- " ... " (long pause) around the apposition, not a comma -->

Self-described — but procurement-blocked — proposals fail Round 1.
<!-- comma micro-pause for bare em-dash usage -->

Voss said, "The send-tier filter runs before the byte leaves the originating
node." <!-- straight quotes, no phantom pauses from curly quotes -->

The lens — Kelsey's — covers commercial viability. <!-- comma micro-pauses -->

---

## RFC and standards references

Ed25519 is specified in RFC 8032. <!-- R-F-C eight thousand thirty-two -->

Argon2id parameters per RFC 9106. <!-- R-F-C nine thousand one hundred six -->

CBOR encoding follows RFC 8949 Section 4.2 for canonical form. <!-- R-F-C eight thousand nine hundred forty-nine -->

---

## Code-block surrogates

The architecture defines:

```python
# Code listing omitted in audio
```

Diagrams render visually only:

```mermaid
graph LR
  A --> B
```

<!-- Both should produce: "Code listing omitted. See the book." and
     "Diagram omitted. See the book." with the surrounding prose flowing
     naturally into and out of the surrogate. -->

---

## Footnote references

The CRDT GC literature [^1] establishes the bounded-staleness invariant.
<!-- the [^1] should be silent — stripped before TTS -->

Schrems II [1] [3] [5] cites multiple authorities. <!-- bracket numerals stay or get stripped depending on the citation style chosen -->

---

## Long-form prose with multiple beats

What changed between Round 1 and Round 2 is not that the architecture
became simpler — it became precise. The earlier draft had handled the happy
path cleanly; the partition-recovery path, not at all. A Flease-family
protocol needs a quorum reduction rule under partition, and the original
specification did not have one. The key compromise response had no test of
whether a revoked device could still decrypt ciphertext already in transit.
The commercial model assumed community adoption as a plan. Reading those
verdicts was not a comfortable afternoon.

<!-- Multi-sentence paragraph with em-dash appositions, complex clause
     structure, and a memorable closing sentence. Listen for prosody
     consistency across sentence boundaries (chunk vs sentence mode). -->
