# Cerebrum

> OpenWolf's learning memory. Updated automatically as the AI learns from interactions.
> Do not edit manually unless correcting an error.
> Last updated: 2026-04-23

## User Preferences

<!-- How the user likes things done. Code style, tools, patterns, communication. -->

## Key Learnings

- **Project:** the-inverted-stack
- **Description:** A practitioner book for software architects, technical founders, and senior engineers
- **Sunfish package split — schema migration:** `Sunfish.Kernel.Runtime` owns `ISchemaVersion` (upcaster registration only). `Sunfish.Kernel.SchemaRegistry` owns `ISchemaLens`, `LensGraph`, epoch coordinator, copy-transform migrator, and compaction scheduler. These are separate packages; do not attribute the lens engine to Kernel.Runtime.
- **Sunfish.Kernel.SchemaRegistry DI method:** `AddSunfishKernelSchemaRegistry()` (confirmed in ch11 code example).
- **Lens registration API:** `LensGraph.AddLens()` in `Sunfish.Kernel.SchemaRegistry` — not via `ISchemaVersion`.
- **ICrdtEngine real API:** `CreateDocument(string documentId)` and `OpenDocument(string documentId, ReadOnlyMemory<byte> snapshot)` — both synchronous.
- **IPostingEngine real API:** `PostAsync(Transaction tx, CancellationToken ct)` where `Transaction` = `{TransactionId, IdempotencyKey, Postings, CreatedAt}`.
- **loro-cs state:** Very bare bones (v1.10.3), snapshot/delta/vector-clock surface not exposed, multi-week binding effort needed. YDotNet is the default; Loro is aspirational.
- **SyncState component:** Lives in `Sunfish.UIAdapters.Blazor.Components.LocalFirst.SyncState`, not `Sunfish.Foundation`.
- **TFMs:** `net11.0-windows10.0.19041.0` and `net11.0-maccatalyst`.
- **DI registration for CRDT engine:** `AddSunfishCrdtEngine()`.
- **Sunfish.Foundation.LocalFirst IS a valid package** — `packages/foundation-localfirst/` exists in the Sunfish repo; `AddSunfishLocalFirst()` is a real method (takes no parameters). `LocalFirstMode` enum does NOT exist. Earlier session notes incorrectly marked this package as invalid.
- **AddSunfishKernelSync() and AddSunfishKernelSecurity()** take no parameters — do not invent options lambdas. GossipDaemonOptions uses `RoundIntervalSeconds` (int), not `GossipInterval` (TimeSpan). `AntiEntropyEnabled` does not exist.
- **Package names: Sunfish.UICore and Sunfish.UIAdapters.Blazor** are correct per repo PackageId values. Not `Sunfish.UI.Core` or `Sunfish.UI.Adapters.Blazor`.
- **SyncState enum valid values:** `Healthy`, `Stale`, `Offline`, `ConflictPending`, `Quarantine`. Do NOT use Linked, Searching, Fresh, Unknown, Degraded, or Error — none exist.
- **ILocalNodePlugin real members:** `Id` (string), `Version` (string), `Dependencies` (IReadOnlyCollection<string>), lifecycle method `OnLoadAsync(IPluginContext context, CancellationToken ct)`. Not PluginId, DependsOn, or Register(ILocalNodeBuilder).
- **IStreamDefinition real members:** `EventTypes`, `BucketContributions` — NOT DocumentTypes, StreamId as StreamId type, or BucketPolicy.
- **IProjectionBuilder real member:** `RebuildAsync(CancellationToken ct)` — NOT Build(IProjectionRegistry).
- **AddSunfishPlugin<T>()** does NOT exist in Sunfish repo.
- **GenerateFounderBundleAsync real signature:** `GenerateFounderBundleAsync(string teamName, CancellationToken ct)` — no teamId parameter.
- **IssueJoinerAttestationAsync real signature:** `IssueJoinerAttestationAsync(byte[] teamId, byte[] joinerPublicKey, ReadOnlyMemory<byte> founderPrivateKey, ...)` — NOT GenerateJoinerBundleAsync.
- **AttestationBundle:** No version field inside the CBOR payload — flat array of 7-field attestation records.
- **WriteState enum:** Does NOT exist. Do not reference WriteState.Pending, WriteState.Confirmed, or WriteState.Failed.
- **MDM node-config.json schema:** Known fields: schemaVersion, teamId, relayEndpoint, allowedBuckets, dataDirectory, logLevel, updateServerUrl, enterpriseAttestationIssuerPublicKey. `storageEncryption` field does NOT exist.
- **Mac Python on this workstation:** Only `python3` is available — no `python` symlink. `build/Makefile` uses `PYTHON ?= python3` and `$(PYTHON)` in all recipe lines (added 2026-04-28). Override per-call via `make PYTHON=/path/to/venv/bin/python <target>`. Do NOT add a bare `python` recipe back.
- **Audiobook pipeline on Mac (Kokoro daily-driver):** Kokoro-FastAPI runs as Docker container `kokoro-fastapi` on `:8880` (image `ghcr.io/remsky/kokoro-fastapi-cpu:latest`). Health endpoint `/health` returns JSON `{"status":"healthy"}`. The OpenAI-compatible `/v1/audio/voices` lists ~58 voices; `/v1/audio/speech` accepts `{model:"kokoro", voice:"<id>", input:"<text>", response_format:"mp3"}`. Default chapter-map preset for body chapters is `male` (am_michael+am_fenrir, speed=0.92). End-to-end pipeline validated 2026-04-28: render → normalize-acx → output at 192 kbps mono 24 kHz.
- **Sunfish.Kernel.Audit IS a real package** (verified 2026-04-28 by @technical-reviewer at iter-0026) — `packages/kernel-audit/` exists in the Sunfish repo. Earlier extensions (#48 #45 #47 #9) declared it "forward-looking" in their HTML annotation headers; that's incorrect. Treat as in-canon going forward; existing annotation headers in Ch15 should be corrected on next sweep (low-priority cleanup).
- **Sunfish.Foundation.Fleet is FORWARD-LOOKING, not in canon** (verified 2026-04-28 by @general-purpose code-checker at iter-0033) — `packages/foundation-fleet/` does NOT exist on disk. Ch21:8 correctly declares it forward-looking ("Volume 1 extension roadmap, not yet present in the Sunfish reference implementation"). Any chapter referencing `Sunfish.Foundation.Fleet` must declare it forward-looking, not in-canon. #44 draft incorrectly declared it in-canon at Ch16:134; queued for tech-review fix.
- **Audiobook Windows-side engine is original Chatterbox 500M (Resemble AI)**, deliberately chosen over Chatterbox-Turbo for the headline `cfg_weight` + `exaggeration` emotion knobs (Turbo had inline `[laugh]`/`[chuckle]` tags but weaker numeric control; we picked knobs over tags). **Canonical client guide lives at** `/Users/christopherwood/Library/CloudStorage/Dropbox/ideas/notes/the-inverted-stack/mac-client-guide.md` — read it for the authoritative endpoint contract, validation bounds, and recipes. Server at `http://desktop-umt08rn:8881/v1` (Tailscale `100.99.202.114`, LAN `192.168.8.168`), OpenAI-compatible surface, voice-cloning native, NSSM Windows service auto-restart. Auth: `Authorization: Bearer $TTS_API_KEY` (Bearer only; X-API-Key returns 401). Stock catalog has 16 voices but only 4 are narrator-fit (en_man, en_woman, broom_salesman, mabel) — the rest are sitcom characters / child voices / non-English. Persona slots in `PRESETS_CHATTERBOX` (sinek, practitioner, fenrir) require custom reference-clip uploads via `build/voice_upload.py put <id> --audio <wav> --transcript "..."`. The OpenAI Python client passes `api_key=` as `Authorization: Bearer <key>` automatically — no header surgery needed for synthesis.
- **Chatterbox emotion control: V12 dramatic recipe is `exaggeration=0.7, cfg_weight=0.3`** (verified ear-test 2026-04-28 on Ch15 Uncle Charlie passage — produced clearly better pauses than model defaults). This is the documented "expressive or dramatic" preset from the upstream README. Use for narrative-driven chapters (Part I + Epilogue + the personal anecdotes inside spec chapters like Ch15 §Key-Loss Recovery). Use model defaults (omit both fields) for spec chapters (Part III). Wrapper exposure of these params is V12; Mac-side `audiobook.py` consumption is the follow-up patch.
- **Inline paralinguistic tags do NOT work on this server** (verified 2026-04-28): `[sigh]`, `[laugh]`, `[chuckle]`, `[cough]` are Turbo-only features; the deployed original Chatterbox doesn't parse them. Worse, inserting them into V12-tuned prose actively disrupts the pause structure that `cfg_weight=0.3` produces. **Do not use paralinguistic tags in audiobook renders.** If inline tag support becomes required, the path is a model swap to Chatterbox-Turbo, not a wrapper change.
- **`narratable_text()` espeak hacks hurt Chatterbox** (verified 2026-04-28 ear-test on Ferreira/Ch09 trial render). Three preprocessing passes designed for Kokoro's espeak engine — `PROPER_NOUN_FIXES` ("Tomás Ferreira" → "toh-MAHS feh-RAY-rah"), `ACRONYM_FIXES` ("CRDT" → "C-R-D-T"), and em-dash → comma collapse — all produce noticeably worse Chatterbox output. The dashed pronunciations force letter-by-letter enunciation; the comma-replacement removes the rhythmic pauses Chatterbox relies on. `narratable_text()` is now engine-aware via an `engine` parameter; pass `engine="chatterbox"` to skip the espeak passes. `build_script()` and the main() `--scripts-only`/`--dry-run` paths thread it through automatically.
- **Word-like acronyms must be expanded for Chatterbox** (verified 2026-04-29 ear-test on broom_salesman + Ch01 + Ch18 SaaS samples — fix solid). Chatterbox neural model misreads acronyms that look like pronounceable syllables: "SaaS" → "saaars", "IaaS"/"PaaS"/"IoT" same failure mode. `CHATTERBOX_EXPANSIONS` in `build/audiobook.py` handles these via two ordered patterns per term: first-use parenthetical pattern collapses "SaaS (Software as a Service)" → "Software as a Service" (avoids doubled phrasing), then standalone form expands bare "SaaS" → "Software as a Service". Also handles hyphenated forms cleanly (e.g. "SaaS-to-local-first" → "Software as a Service-to-local-first"). Currently covers SaaS/IaaS/PaaS/IoT. **Verified-safe acronyms (no expansion needed):** KEK + DEK confirmed via 2026-04-29 ear-test using `00c-kek-dek-verification.mp3` excerpt — broom_salesman pronounces both letter-by-letter ("kay-ee-kay", "dee-ee-kay") naturally without expansion. HSM/TPM/GDPR/HIPAA/CRDT/CISO/DNS also confirmed via absence of complaint across pre-fix render. The pattern: short acronyms with explicit consonant-vowel-consonant structure (KEK, DEK) get spelled even though they look pronounceable; the SaaS family gets word-pronounced because of the doubled-vowel "aa" pattern that registers as a syllable. If a new acronym surfaces as misread, ear-test before adding to expansions.
- **Per-voice emotion-knob strategy** (verified 2026-04-28 ear-test on cloned RogerioM/Ferreira): **stock voices** (en_man, en_woman, mabel, broom_salesman) benefit from V12 dramatic recipe (exag=0.7, cfg=0.3) — they're trained for neutral/clinical reads and need expressivity added. **Cloned voices** (LibriVox-sourced reference clips like ferreira-trial-rogeriom) already carry the reader's natural pacing and character; layering V12 dramatic on top over-pushes into stilted enunciation. **For cloned voices use neutral params** (omit --exaggeration / --cfg-weight). Future enhancement: per-voice metadata in `PRESETS_CHATTERBOX` could store recommended emotion knobs (or omit-flag) per slot.
- **Engine-aware chunk budget** (added 2026-04-28): `CHUNK_BUDGETS_BY_ENGINE` in `build/audiobook.py` defaults Kokoro to 700 chars (existing) and Chatterbox to 400. Chatterbox's ~100 sec / ~2500 token output cap silently truncates longer chunks to silence, especially under V12 dramatic recipe (slower pacing) or cloned voices (different sample/char ratios). 400 chars is the safe ceiling that keeps every chunk well under the cap. `render_chapter` looks up the engine-specific budget when calling `chunk_text_paired`.
- **Audiobook universal-narrator decision** (set 2026-04-28): the author chose `broom_salesman` (stock Chatterbox, older British male, Ollivander register) as the SINGLE narrator for the entire audiobook — Parts I/III/IV, Epilogue, Preface, AND all Part II council chapters. No per-persona voicing in the production audiobook. `PRESETS_CHATTERBOX` now routes ALL preset slots (male/female/sinek/practitioner/british/fenrir/etc.) to `broom_salesman`. `CHAPTER_PRESET_MAP` is preserved as-is for Kokoro renders; for Chatterbox it's effectively a no-op since every slot resolves identically. The 5 cloned LibriVox voices (`ferreira-trial-rogeriom`, `shevchenko-trial-yakovlev`, `voss-trial-savage`, `okonkwo-trial-klett`, `kelsey-trial-smith`) are PRESERVED on the TTS server and documented in `references/CREDITS.md` for optional per-chapter regeneration via `--voice <id>` CLI override. Sinek-style author-voice search is CANCELED — `broom_salesman` covers that slot too. Stock voice + V12 dramatic recipe (`--exaggeration 0.7 --cfg-weight 0.3`) is the recommended config for narrative chapters; neutral params for specification chapters.
- **LibriVox attribution policy for cloned voices** (set 2026-04-28): per [librivox.org/pages/public-domain](https://librivox.org/pages/public-domain/), all LibriVox recordings are CC0 public domain. Credit is **NOT legally required** but LibriVox "much prefers" it with a link to their site. We standardize on **three attribution layers**: (1) `references/CREDITS.md` is the canonical version-controlled record, one section per voice with persona/book/reader/URLs/license; (2) the TTS server's `notes` field on each uploaded voice carries the same attribution (accessible via `GET /v1/audio/voices/{id}` for verification); (3) the eventual M4B end-credits track will name readers + LibriVox sources verbally. Workflow: when uploading a new LibriVox-sourced voice, add a section to `references/CREDITS.md` AND set the `notes` field with the standardized format ("Source: '<title>' by <author>. Reader: <name>. LibriVox book: <url> | LibriVox reader: <url> | Used §<sec>, <window>. License: Public domain (CC0). Credit preferred per https://librivox.org/pages/public-domain/."). When promoting a trial voice (`*-trial-*` → clean slug), preserve the attribution unchanged; only the voice ID renames.
- **Server contract per canonical client guide (mac-client-guide.md, 2026-04-28):** `max_new_tokens=2500` ≈ ~100 sec audio cap (operator-tunable in `.env`); concurrency 4 (5th request 503); validation `exaggeration ∈ [0.0, 1.5]`, `cfg_weight ∈ [0.1, 1.0]`, `temperature ∈ [0.0, 2.0]`, `speed ∈ [0.5, 2.0]`; `input` 1-4096 chars; up to 60s warmup after restart; default voice `en_woman` if omitted. Quality (not the cap) is the real chunking constraint — degrades past ~60-90 sec contiguous output. `audiobook.py` `CHUNK_CHAR_BUDGET=700` is in the recommended 600-900 sweet spot. Server tolerates `application/octet-stream` MIME by falling back to filename extension, so vanilla `curl -F "audio=@x.mp3"` works without `;type=audio/mpeg`. The earlier "~40 sec cap" finding was wrong — it was either a transient model state or a different `max_new_tokens` setting at probe time.
- **Audiobook concurrency does NOT help on Chatterbox** (tested 2026-04-28). The canonical guide's "4 simultaneous" is a 503-tolerance threshold, NOT GPU parallel throughput. Chatterbox doesn't batch on the GPU; concurrent requests serialize at the model layer. A/B on Ch05 (3 prose chunks): serial 29.2s vs concurrency=4 36.2s (24% SLOWER due to coordination overhead). A/B on Ch06 (2 prose chunks): serial 54.8s vs concurrency=2 55.4s (identical). Implementation was attempted via `ThreadPoolExecutor` (synth phase parallel, write phase serial — chunks finished in correct order, smoke clean) but produced no wall-clock win. **Reverted.** Future sessions: do not re-add `--concurrency` to `audiobook.py` for Chatterbox without server-side batching support. If a different engine (Kokoro local Docker, OpenAI cloud TTS) ever shows GPU parallelism, re-evaluate then.
- **LibriVox sifting workflow** — `build/librivox_browse.py search/sections/preview/extract`. The API at `https://librivox.org/api/feed/audiobooks/?format=json&extended=1` returns books with sections including `listen_url` (archive.org MP3) + per-section `readers[]`. Solo books: every section has the same single reader_id. ffmpeg with `-ss <time> -i <url> -t <length>` does HTTP range requests against archive.org (which supports them) — pulls ~250KB instead of full ~14MB chapter. Default extract is WAV 24kHz mono (matches Chatterbox internals). Skip the first ~1:00 of any LibriVox section to avoid the boilerplate intro ("Section N of <book> by <author>, read by <reader> for LibriVox") and last ~10s for the closing boilerplate.

## Do-Not-Repeat

<!-- Mistakes made and corrected. Each entry prevents the same mistake recurring. -->
<!-- Format: [YYYY-MM-DD] Description of what went wrong and what to do instead. -->
- [2026-04-24] Do NOT attribute `ISchemaLens` or `LensGraph` to `Sunfish.Kernel.Runtime`. They live in `Sunfish.Kernel.SchemaRegistry`. Runtime owns upcasters (`ISchemaVersion`) only.
- [2026-04-24] Do NOT invent ICrdtEngine methods like `OpenOrCreateAsync()`. Real API: `CreateDocument()` and `OpenDocument()` (both sync).
- [2026-04-24] Do NOT describe loro-cs as "actively maintained with small version lag" — it's very bare bones, multi-week effort to complete bindings.
- [2026-04-24] Do NOT use SyncState.Linked, .Searching, .Fresh, .Unknown, .Degraded, or .Error — valid values are only Healthy, Stale, Offline, ConflictPending, Quarantine.
- [2026-04-24] Do NOT invent plugin API members (PluginId, DependsOn, Register). Use Id, Dependencies, OnLoadAsync.
- [2026-04-24] Do NOT use WriteState enum (Pending/Confirmed/Failed) — does not exist in Sunfish repo.
- [2026-04-24] Do NOT invent MDM config key `storageEncryption: required` — not in node-config.json schema.
- [2026-04-24] Do NOT reference OnboardingState enum — use AnchorSessionService.IsOnboarded (bool) instead.
- [2026-04-24] Do NOT claim AddSunfishKernelRuntime() wires sync daemon, mDNS, gossip, or ICrdtEngine — it only registers INodeHost and IPluginRegistry.
- [2026-04-24] Do NOT claim AddSunfishKernelSecurity() loads/generates keypair or registers onboarding state machine — cryptographic services only.
- [2026-04-24] Do NOT describe Sunfish's CRDT as "working CRDT merge." Current StubCrdtEngine uses total-order replay, not CRDT semantics; real engine (YDotNet) validated in spike 2026-04-22 but not yet integrated into kernel-crdt. Stub file self-marks "DO NOT SHIP TO PRODUCTION."
- [2026-04-24] Do NOT claim GossipDaemon applies deltas back into ICrdtDocument — code comment confirms apply-back "still lands in Wave 2.6." Two nodes can exchange state vectors today, but concurrent edits don't converge without manual intervention.
- [2026-04-24] Do NOT claim full `dotnet build` passes on Sunfish repo — test projects (kernel-lease/tests, local-node-host/tests, blocks-forms/tests) have interface mismatches. Only apps/local-node-host builds cleanly as of 2026-04-24.
- [2026-04-24] Do NOT claim OnboardAsync persists attestation or applies snapshot in Wave 3.x — both are deferred to Wave 4.
- [2026-04-24] SunfishNodeHealthBar lives in Sunfish.UIAdapters.Blazor, NOT Sunfish.Foundation.LocalFirst.
- [2026-04-24] Razor illustrative marker syntax: use @* illustrative — not runnable (pre-1.0 API) *@ not HTML comment syntax inside fenced razor blocks.

## Decision Log

<!-- Significant technical decisions with rationale. Why X was chosen over Y. -->

## Decision Log — 2026-04-25 — Phase 0.0 timing pilot

**Decision: skip Task 2 (MED-tier pilot); proceed to Phase 0 sweep without timing data.**

**Reasoning:** Author has stated the project has no deadline and will take as long as it takes. Real timing data is therefore not load-bearing for the continue/abort decision. Use a conservative estimate as a sanity check rather than a budget.

**Conservative estimate for Phase 0** (assuming Claude does the compression with author review):
- 12 HIGH-severity paragraphs × ~5 min Claude generation + ~5 min author review = 2 hours
- ~30 MED-severity paragraphs × ~3 min generation + ~3 min review = 3 hours
- Appendix F creation (Task 6) = ~4 hours (substantive compilation work)
- Disclosures + verification + commit hygiene = ~2 hours
- **Conservative total: ~11 hours.** Well within the original 24-48h budget; no need to invoke Alternative A or B.

**Decision: CONTINUE with Phase 0 sweep.** Plan Task 3 (the projection gate) is satisfied: projection ≤48h, continue.

## Decision Log — 2026-04-25 — Phase 0.5 result

**Decision: ORIGINAL PLAN stands.** Phase 0.5 methodology test produced a fresh Gladwell pass-1 on cleaned Ch01 (`chapters/_voice-drafts/pass1/ch01-when-saas-fights-reality.md`, 5,447 words). Author's verdict: "the ch01 reality check looks good" — confirming pass-1 did not regress after Phase 0a; pass-2 (Sinek polish over Gladwell) is still needed for the book's house voice.

**Phase 1 scope unchanged:** tune all six voice agents (sinek + 5 guests). Polish/normalize tier system as planned.

## GitButler state — 2026-04-25

GitButler was set up earlier in the session and torn down via `but teardown`
after a workspace-conflict error during `but setup` retry. Current state:

- `.git/gitbutler` directory still exists (residual)
- `gitbutler/target` and `gitbutler/workspace` branches still exist locally
  with leftover commits (b244d05, adef29e, db4a0a1)
- Working in plain git mode on `main`; no GitButler hooks active
- All work since teardown has been clean linear commits on `main`

**Implication for future sessions:** the user's global GitButler detection
(`test -d .git/gitbutler`) will return "GitButler-managed" and trigger the
`use-gitbutler.md` workflow. But `but` commands will fail until either:
(a) the leftover gitbutler/* branches are cleaned and `but setup` re-run,
or (b) the .git/gitbutler directory is removed to make the repo look like
plain git again.

User has not asked for cleanup — leaving as-is. If a future session
hits `but` errors, surface this state immediately rather than retrying.

## Phase 1 → Phase 2 transition — 2026-04-25

Phase 1 closed at commit `af4e113`. Six voice agents tuned per the
ORIGINAL PLAN (Phase 0.5 decision):
- voice-sinek: chapter-scale calibration, scene preservation, audiobook
  cadence, register variation, 10% cut, preserve definitions, second
  canonical example (chapter-opening register)
- voice-gladwell, voice-brown: universal tunes (audiobook + preserve
  definitions) + 10% cut
- voice-grant: universal tunes + 10% cut + citation-enumeration guard
  (Grant-specific compounding pattern)
- voice-godin: universal tunes only (existing brevity rule already
  prevents Sinek-style compounding)
- voice-lencioni: universal tunes + preserve-narrative-scenes (fable
  agent needs scene preservation more than others) + scene-safe 10% cut

Per-invocation logging (B3/C9) added to voice-pass.py: every voice-pass
run now writes a JSON audit entry to chapters/_voice-drafts/_log/.

Phase 2 dispatched as background process bzduwnh42 — 4 pilots serial
(Ch04, Ch05, Ch11, Ch01), ~40 min wall-clock. Grading template at
docs/superpowers/specs/2026-04-25-phase2-pilot-grading.md.

In parallel: promote.py (Phase 4 prep) dispatched as subagent — TDD
work, ~20 min, non-overlapping with pilot run.
