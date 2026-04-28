# V12: Expose emotion-control parameters in /v1/audio/speech

> Feature request for the Windows TTS wrapper. Self-contained — implementation
> pointers, validation rules, smoke tests, and Mac-side consumption plan all
> in one place.

## Summary

Add `exaggeration`, `cfg_weight`, and `temperature` as optional fields on
`POST /v1/audio/speech`. Plumb them through to the underlying
`ChatterboxTTS.generate()` call. All optional; defaults preserve current
behavior. ~15 lines of code.

## Why this matters (the gap we found 2026-04-28)

The wrapper currently exposes:

```json
{ "model": str, "input": str, "voice": str,
  "response_format": "mp3"|"wav"|"flac"|"pcm", "speed": float }
```

Chatterbox (the original 500M model behind the wrapper — not Turbo) takes
two additional emotional-control parameters that are **not surfaced**.
The original Chatterbox's headline feature is exactly these knobs; per
the upstream README at
[resemble-ai/chatterbox#original-chatterbox-tips](https://github.com/resemble-ai/chatterbox#original-chatterbox-tips):

> **Expressive or Dramatic Speech:**
> - Try lower `cfg_weight` values (e.g. `~0.3`) and increase `exaggeration` to around `0.7` or higher.
> - Higher `exaggeration` tends to speed up speech; reducing `cfg_weight` helps compensate with slower, more deliberate pacing.

Without these knobs, audiobook renders are stuck on the model defaults
(`exaggeration=0.5, cfg_weight=0.5`) — fine for neutral narration, wrong
for the book's narrative-driven Part I (Marcus's bid-deadline scene)
and the council deliberations in Part II.

What we tested without the knobs:

| Lever | Verdict |
|---|---|
| Inline paralinguistic tags (`[sigh]`, `[laugh]`, `[chuckle]`, `[cough]`) | Real but small. Tag set is comedic-leaning; `[sigh]` is the only one that fits non-comic registers. One or two beats per scene is the ceiling. |
| Punctuation cues (em-dashes, ellipses, exclamation marks) | The model parses these as pacing. Already in the book's house style — gives ~30% of the emotional arc for free. |
| `speed` parameter | Coarse global multiplier; sounds artificial when pushed beyond ~0.92–1.08. Not an emotion lever. |
| **`exaggeration` + `cfg_weight`** | **Documented dramatic-narrator recipe; not currently reachable.** |

So `exaggeration` + `cfg_weight` are the load-bearing change that unlocks
per-chapter emotional differentiation.

## API changes

### Schema addition (`SpeechRequest`)

```python
class SpeechRequest(BaseModel):
    """POST /v1/audio/speech body."""
    model: str = Field(description="Server-defined model label (logged but not used for routing)")
    input: str = Field(min_length=1, max_length=4096)
    voice: str = Field(min_length=1)
    response_format: Literal["mp3", "wav", "flac", "pcm"] = "mp3"
    speed: float = 1.0

    # NEW IN V12 — Chatterbox-Turbo emotional control surface
    exaggeration: float | None = Field(
        default=None,
        ge=0.0, le=2.0,
        description=(
            "Emotional intensity. Model default 0.5 used when omitted. "
            "0.3 = subdued, 0.5 = neutral (default), 0.7+ = dramatic. "
            "Higher values speed up speech; pair with lower cfg_weight."
        ),
    )
    cfg_weight: float | None = Field(
        default=None,
        ge=0.0, le=1.0,
        description=(
            "Classifier-free guidance weight. Model default 0.5 used when "
            "omitted. Lower values (0.3) produce slower, more deliberate "
            "pacing; useful as the dramatic-narrator counterweight to "
            "exaggeration=0.7+."
        ),
    )
    temperature: float | None = Field(
        default=None,
        ge=0.0, le=2.0,
        description=(
            "Sampling temperature for token generation. Model default "
            "(typically ~0.8) used when omitted. Lower (0.5) = more "
            "deterministic / consistent across re-renders; higher (1.0+) "
            "= more variation. For audiobook reproducibility, prefer 0.5–0.7."
        ),
    )
```

### Generation call passthrough

Wherever the current code calls `ChatterboxTTS.generate()`, add the
three optional parameters. Pattern:

```python
gen_kwargs: dict[str, Any] = {}
if req.exaggeration is not None:
    gen_kwargs["exaggeration"] = req.exaggeration
if req.cfg_weight is not None:
    gen_kwargs["cfg_weight"] = req.cfg_weight
if req.temperature is not None:
    gen_kwargs["temperature"] = req.temperature

wav = model.generate(req.input, audio_prompt_path=voice_path, **gen_kwargs)
```

The `if not None` guard is load-bearing: passing `None` to the model
function may override its internal default with `None`, which fails. Only
pass the kwarg when the client supplied a value.

### Defaults policy

**Server uses the model's defaults when the field is omitted.** The wrapper
should NOT set its own opinionated defaults. Two reasons:

1. The upstream model may revise its own defaults (e.g. Turbo → Turbo-v2);
   if the wrapper hardcodes 0.5, it pins behavior across model upgrades.
2. The Mac-side `audiobook.py` will drive emotion settings from per-preset
   config (see "Mac-side follow-up" below); the wrapper should not double
   up on that policy.

### Validation (server-side, return 422 with detail)

| Field | Bound | Reason |
|---|---|---|
| `exaggeration` | `0.0 ≤ x ≤ 2.0` | Model accepts >1.0 but README warns it gets erratic; cap at 2.0 to prevent abuse |
| `cfg_weight` | `0.0 ≤ x ≤ 1.0` | Model expects [0,1]; outside this range produces undefined behavior |
| `temperature` | `0.0 ≤ x ≤ 2.0` | Standard sampling-temperature bounds |

`ge`/`le` Field constraints handle this in pydantic — no custom validator
needed.

## Implementation checklist

| Step | File | Effort |
|---|---|---|
| 1 | Add three optional fields to `SpeechRequest` pydantic model | 1 line each + Field args |
| 2 | Build `gen_kwargs` dict in synthesis handler with `if not None` guards | 8 lines |
| 3 | Pass `**gen_kwargs` to `ChatterboxTTS.generate()` | 1-line change |
| 4 | Update `openapi.json` (auto-generated by FastAPI) — should regenerate on next start | 0 lines |
| 5 | Add 3 new unit/integration tests covering: omitted (default behavior), mid-range value, out-of-range rejection | ~30 lines |
| 6 | (Optional) Log received emotion params at INFO level — useful for postmortem when a render sounds wrong | 1 line |

Total: ~50 lines of code + tests. Single-commit V12 PR.

## Smoke tests (post-deploy, run from Mac)

After `nssm restart TTSService`:

```bash
KEY=cPXXLUOv1iZ854eirIW_Vi28Q7iIZjkOKSAdlHtBlfk
HOST=desktop-umt08rn:8881

# 1. Baseline (no new params) — same audio as before V12
curl -X POST "http://$HOST/v1/audio/speech" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"model":"chatterbox","input":"This is the V12 baseline render.","voice":"en_man","response_format":"mp3"}' \
  --output /tmp/v12-baseline.mp3 -w "baseline: HTTP %{http_code} %{size_download} bytes\n"

# 2. Subdued (exaggeration low, cfg_weight high) — should sound flatter
curl -X POST "http://$HOST/v1/audio/speech" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"model":"chatterbox","input":"This is the V12 baseline render.","voice":"en_man","response_format":"mp3","exaggeration":0.3,"cfg_weight":0.7}' \
  --output /tmp/v12-subdued.mp3 -w "subdued: HTTP %{http_code} %{size_download} bytes\n"

# 3. Dramatic (the documented dramatic-narrator recipe) — should sound more energetic + paced
curl -X POST "http://$HOST/v1/audio/speech" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"model":"chatterbox","input":"This is the V12 baseline render.","voice":"en_man","response_format":"mp3","exaggeration":0.7,"cfg_weight":0.3}' \
  --output /tmp/v12-dramatic.mp3 -w "dramatic: HTTP %{http_code} %{size_download} bytes\n"

# 4. Out-of-range — should return 422
curl -X POST "http://$HOST/v1/audio/speech" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"model":"chatterbox","input":"oob test","voice":"en_man","response_format":"mp3","exaggeration":3.0}' \
  -w "out-of-range: HTTP %{http_code}\n"

# 5. A/B listen
afplay /tmp/v12-baseline.mp3
afplay /tmp/v12-subdued.mp3
afplay /tmp/v12-dramatic.mp3
```

**Expected outcomes:**

- Steps 1, 2, 3 return 200 + MP3 bytes; durations differ (dramatic likely
  shorter due to higher exaggeration speeding speech).
- Step 4 returns 422 with detail mentioning `exaggeration` and the bound.
- Listen test: dramatic should clearly sound more energetic than baseline;
  subdued should sound flatter / more clinical.

If the audio doesn't change between subdued and dramatic, the `gen_kwargs`
plumbing didn't reach the model — check that the kwargs survive whatever
caching / batching layer sits between FastAPI and `ChatterboxTurboTTS`.

## Backward compatibility

**100%.** All three new fields are optional with default `None`. Existing
clients (audiobook.py V11, the Mac voice_upload helper, any curl scripts)
send only the original fields and get the same behavior they had before
V12.

The `voice_upload.py` and `audiobook.py` helpers ignore unknown response
fields, so adding fields to the response is also safe (though the V12
spec doesn't require any response schema changes).

## Mac-side follow-up (after V12 deploys)

Once V12 is live, two changes land on the Mac side in a single audiobook
pipeline patch:

### 1. `build/audiobook.py` — CLI flags

```python
ap.add_argument("--exaggeration", type=float, default=None,
                help="Emotion intensity (Chatterbox only). 0.5 default; "
                     "0.7+ for dramatic chapters.")
ap.add_argument("--cfg-weight", type=float, default=None,
                help="Classifier-free guidance weight (Chatterbox only). "
                     "0.5 default; 0.3 for slower/more deliberate pacing.")
ap.add_argument("--temperature", type=float, default=None,
                help="Sampling temperature (Chatterbox only). Model default "
                     "(~0.8) used when omitted; 0.5 for reproducibility.")
```

Pass through to the synthesis call as `extra_body={"exaggeration": ...}`
on the OpenAI client (the OpenAI Python client supports arbitrary extras
when the server accepts them).

### 2. `PRESETS_CHATTERBOX` — per-preset emotion bundles

```python
PRESETS_CHATTERBOX: dict[str, dict] = {
    "male":   {"voice": "en_man", "speed": 1.0,
               "exaggeration": 0.5, "cfg_weight": 0.5},   # neutral narrator default
    "female": {"voice": "en_woman", "speed": 1.0,
               "exaggeration": 0.5, "cfg_weight": 0.5},
    "sinek":  {"voice": None,      "speed": 0.92,
               "exaggeration": 0.6, "cfg_weight": 0.4},   # warm, slightly slower
    # …per-persona tuning per the chapter-preset map
}
```

### 3. `CHAPTER_PRESET_MAP` — narrative-driven chapters get the dramatic bundle

```python
# Part I narrative chapters use a more expressive register
NARRATIVE_PRESET_OVERRIDES = {
    "ch01-when-saas-fights-reality":   {"exaggeration": 0.7, "cfg_weight": 0.3},
    "ch02-local-first-serious-stack":  {"exaggeration": 0.6, "cfg_weight": 0.4},
    # …
    # Part III specification chapters stay neutral (no override)
    # Part II council uses per-member voices (Voss/Shevchenko/etc) with their own bundles
}
```

This puts the emotional decision in the per-chapter config, not in the
prose. Same chapter file, different render energy depending on which
preset bundle the chapter map selects.

## Out of scope for V12

These are real but not in this PR — separate tickets, smaller priority:

- **Per-segment emotion control via inline paralinguistic tags.** The
  original Chatterbox model (this server's deployed variant) does not
  parse inline tags like `[laugh]`, `[chuckle]`, `[sigh]` — those are
  Chatterbox-Turbo-only features. Confirmed by ear test 2026-04-28: a
  `[sigh]` insertion in the Uncle Charlie passage didn't produce an
  audible sigh and disrupted the V12 dramatic-recipe pause structure.
  If paralinguistic tags become a requirement, model swap is the path,
  not a wrapper change.
- **Sample rate selection in the response.** Currently 24kHz mono fixed.
  Audiobook spec is fine with that; podcast workflows may want 48kHz
  later.
- **Streaming response (chunked transfer).** Useful for low-latency voice
  agents; not needed for offline audiobook batch render.
- **Per-voice default emotion overrides on `PUT /v1/audio/voices/{id}`.**
  Could let voice metadata carry a recommended `exaggeration`/`cfg_weight`
  pair so the synth call inherits from the voice if not supplied. Marginal
  utility once Mac-side preset bundles handle this; defer.

## Definition of done

- [ ] V12 PR merged on the Windows side
- [ ] `nssm restart TTSService` + post-deploy smoke tests above all green
- [ ] OpenAPI shows the three new fields in `SpeechRequest`
- [ ] Mac-side `build/audiobook.py` PR adds `--exaggeration`/`--cfg-weight`/`--temperature`
- [ ] Mac-side `PRESETS_CHATTERBOX` extended with per-preset bundles
- [ ] Re-render Ch01 ¶1 with the dramatic recipe, A/B against the V11 baseline
- [ ] Decision recorded in the project audiobook topology memory: "use
      `exaggeration=0.7, cfg_weight=0.3` for narrative chapters, defaults
      for spec chapters" (or whatever the ear test concludes)

## Cross-references

- **Canonical client contract** (read first): `~/Library/CloudStorage/Dropbox/ideas/notes/the-inverted-stack/mac-client-guide.md`
- `memory/project_audiobook_topology.md` — current topology + Mac/Windows pipeline split
- Upstream model: <https://github.com/resemble-ai/chatterbox> — section "Original Chatterbox Tips" documents the recipe
- V11 deploy notes: voice catalog management (PUT/DELETE custom voices, stock voice protection); curl 415 footgun fixed by accepting file-extension fallback for Content-Type

## Verification log

**2026-04-28 — V12 deployed.** Mac-side smoke from this brief's §Smoke tests
all green (steps 1-4 returned 200/200/200/422 as expected). Audio
differentiation between `subdued (0.3/0.7)` and `dramatic (0.7/0.3)` later
confirmed audible in book context (Ch15 Uncle Charlie anecdote — dramatic
recipe produced clearly better pauses than model defaults; v11 baseline
was flatter/faster).

**2026-04-28 — Mac-side consumption complete.**
`build/audiobook.py` gained `--exaggeration` / `--cfg-weight` /
`--temperature` flags, threaded through `render_chapter` →
`synth_chunk` → `extra_body`. Manifest records the params per chapter
for reproducibility. Default behavior unchanged when flags omitted.

**Spec-vs-deployed delta (resolved):**

| Spec said | Deployed reality | Resolution |
|---|---|---|
| `exaggeration ≤ 2.0` | Server enforces `≤ 1.5` | Server is correct; spec was speculative cap |
| `cfg_weight ∈ [0.0, 1.0]` | Server enforces `≥ 0.1` | Floor at 0.1 makes sense; values near 0 produce noise |

The brief's bounds in §API changes overstate `exaggeration` upper bound by
0.5; canonical mac-client-guide.md §3 has the deployed values.

**V13 candidate — superseded.** The "expose `max_new_tokens` to lift the
~40s cap" follow-up is no longer needed. Per canonical guide §10,
`TTS_MAX_NEW_TOKENS=2500` is already at ~100s cap (not the ~40s I'd
observed in earlier probes — that was a transient wrong reading) and is
operator-tunable in `.env` without a code change. Quality (not the cap)
is the real constraint past ~60–90s contiguous output, so per-request
exposure isn't valuable anyway. Brief kept for historical record;
no V13 PR needed.
