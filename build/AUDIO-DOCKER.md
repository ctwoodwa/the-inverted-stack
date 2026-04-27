# Audiobook Generation — Docker Setup

This repo's audiobook pipeline (`build/audiobook.py`) calls a local
OpenAI-compatible TTS server. Two engines are documented here:

| Engine | Quality | Speed on the workstation (Intel i9, 32 GB, no GPU) | Voice cloning | When to use |
|---|---|---|---|---|
| **Kokoro-82M** (FastAPI) | Good — clearly TTS but listenable | ~0.6× realtime (~5 sec audio per 3 sec compute) | No (67 preset voices, includes blends) | Daily iteration, full-book first drafts, sample renders |
| **Higgs Audio v2** (faster-higgs-audio fork) | High — close to ElevenLabs in long-form coherence | ~0.05–0.15× realtime (~60–180 hr to render the full book) | Yes (3-second sample) | Once-per-chapter quality A/B against Kokoro; pre-final-master comparison; voice-cloned stretches |

Both speak `POST /v1/audio/speech` (OpenAI shape), so `audiobook.py --base-url`
points at one or the other and the rest of the pipeline (chunking,
lexicon, silence injection, alignment, mastering) is identical.

---

## 1. Kokoro — daily driver (already set up)

The compose file at `build/docker-compose.audio.yml` defines a `kokoro`
service. Bring it up:

```bash
docker compose -f build/docker-compose.audio.yml up -d kokoro
docker compose -f build/docker-compose.audio.yml logs -f kokoro     # watch boot
```

The image is **5.6 GB on disk** (`ghcr.io/remsky/kokoro-fastapi-cpu:latest`)
and warms up in ~4 seconds on this hardware. After warmup you should see:

```
67 voice packs loaded
Beta Web Player: http://0.0.0.0:8880/web/
Application startup complete.
```

Smoke-test:

```bash
curl -X POST http://localhost:8880/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model":"kokoro","input":"Test.","voice":"am_michael","response_format":"mp3"}' \
  --output /tmp/k.mp3 && open /tmp/k.mp3
```

List available voices:

```bash
curl -s http://localhost:8880/v1/audio/voices | jq
```

The audiobook pipeline picks voices via `build/audiobook.py` presets
(`am_michael`, `af_bella`, `bm_fable`, blends like `am_michael+am_fenrir`).
See the `PRESETS` and `CHAPTER_PRESET_MAP` dicts in that file for what the
book uses.

### Pipeline smoke test

After installing Python deps (`pip install openai imageio-ffmpeg`):

```bash
make audiobook-sample ch=ch01 paragraphs=2
# -> build/output/audiobook/ch01-when-saas-fights-reality_sample.mp3 (~30s)

# Try a different voice without changing the chapter map:
make audiobook-sample ch=ch15 paragraphs=3 preset=fenrir
```

---

## 2. Higgs Audio v2.5 on the Windows GPU box (high-quality path)

**Hardware:** RTX 4070 Ti (12 GB VRAM) on a Windows gaming machine on
the same LAN as the Mac. With this card, **target Higgs Audio v2.5**
(the 1B model that supersedes v2 — faster, smaller, more accurate, fits
comfortably in fp16 with VRAM headroom). Expect **~2–3× realtime**
inference: ~3–4 hours of GPU compute for a 9-hour audiobook.

The Mac stays the workstation. The Windows box runs Higgs as an HTTP
service. `audiobook.py --engine higgs --base-url http://<windows-lan-ip>:8881/v1`
points the pipeline at it; the rest (chunking, lexicon, mastering)
runs on the Mac as today.

### Two install paths on Windows — pick one

| Path | Recommended? | Tradeoff |
|---|---|---|
| **A — Native Windows Python + CUDA** | **Yes** | Simplest in 2025. PyTorch ships pre-built CUDA wheels, no container indirection, direct LAN networking. Slight host pollution mitigated by venv. |
| **B — Podman with GPU passthrough** | Only if container isolation matters more than setup time | Podman GPU on Windows works as of Podman 4.7+ but requires installing NVIDIA Container Toolkit *inside* the Podman Machine WSL2 VM and configuring CDI. Multiple known sharp edges. |

The user already has Podman installed but not GPU-configured. **Path A
is the lower-friction path.** Path B is documented below for
completeness.

---

### Path A — Native Windows + PowerShell (recommended)

#### Prerequisites — verify these once before starting

Open PowerShell on the Windows machine and run each command. If any
fails, fix that step before proceeding.

```powershell
# 1. NVIDIA driver + CUDA-capable GPU visible
nvidia-smi
# -> should show RTX 4070 Ti and a CUDA driver version (12.x recommended)

# 2. Python 3.10 or 3.11 installed (NOT 3.12+ yet — some ML wheels lag)
python --version
# -> Python 3.10.x or 3.11.x

# 3. Git installed
git --version
```

If `python` isn't installed: install Python 3.11 from python.org (check
"Add to PATH" during install). If `nvidia-smi` isn't found: install the
latest NVIDIA Game Ready or Studio Driver from nvidia.com.

#### Install Higgs Audio v2.5

```powershell
# 1. Clone outside any container path
cd C:\
git clone https://github.com/boson-ai/higgs-audio
cd higgs-audio

# 2. Create an isolated venv so Higgs deps don't pollute the system Python
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install PyTorch with CUDA 12.4 wheels (matches recent driver)
#    Adjust cu124 -> cu121 if your driver is on the older CUDA 12.1 line
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124

# 4. Install Higgs requirements
pip install -r requirements.txt

# 5. Install the OpenAI-compatible API server (Boson ships one in
#    examples/openai_server, or use the higgs_audio.serve module)
pip install fastapi uvicorn[standard]

# 6. Pre-download model weights (one-time, ~3-6 GB to %USERPROFILE%\.cache\huggingface)
python -c "from huggingface_hub import snapshot_download; snapshot_download('bosonai/higgs-audio-v2.5')"
```

#### Smoke-test on the Windows box

```powershell
# From the higgs-audio repo, with .venv activated
python -c "
import torch
from higgs_audio import HiggsAudioPipeline
print('CUDA available:', torch.cuda.is_available())
print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu')
pipe = HiggsAudioPipeline.from_pretrained('bosonai/higgs-audio-v2.5', torch_dtype=torch.float16, device_map='cuda')
audio = pipe('Local first, cloud second.', voice='default')
audio.save('smoke-test.wav')
print('Wrote smoke-test.wav')
"
```

If this prints `CUDA available: True`, names the RTX 4070 Ti, and writes
`smoke-test.wav` (~1-3 seconds wall time), the GPU stack is healthy.

#### Run the OpenAI-compatible API server

The exact entry point depends on the upstream repo's current layout —
check `examples/openai_server/` or the README's "OpenAI-compatible API"
section. Typical command:

```powershell
# Bind to 0.0.0.0 so the Mac on the LAN can reach it; default would be localhost
python -m higgs_audio.openai_server --host 0.0.0.0 --port 8881 --device cuda --dtype float16
```

If the Boson repo doesn't ship the server module under that name, fall
back to the **`sorbetstudio/faster-higgs-audio`** fork — same install
pattern but ships the FastAPI server explicitly. Replace step 1 with:

```powershell
git clone https://github.com/sorbetstudio/faster-higgs-audio
cd faster-higgs-audio
# Then the same venv + pip install pattern, with their server entry point
```

#### Open the Windows Firewall for port 8881

```powershell
# Run this PowerShell as Administrator
New-NetFirewallRule `
  -DisplayName "Higgs Audio API (LAN inbound)" `
  -Direction Inbound `
  -Protocol TCP `
  -LocalPort 8881 `
  -RemoteAddress LocalSubnet `
  -Action Allow
```

The `RemoteAddress LocalSubnet` scope means only machines on your home
LAN can reach the port — not the public internet. Safer than wide-open.

#### Find the Windows LAN IP

```powershell
ipconfig | Select-String "IPv4"
# -> note the 192.168.x.x or 10.x.x.x address; that is what the Mac dials
```

Pin a DHCP reservation on your router for this IP, or note that DHCP
lease renewal can shift it (in which case you re-look it up). For
zero-friction, install Tailscale on both machines — see "Tailscale"
below.

#### Run as a Windows service (optional but recommended)

If you want Higgs running in the background after every boot, use
**NSSM** (Non-Sucking Service Manager) to wrap the python command as a
Windows service:

```powershell
# Download nssm.cc, then:
nssm install HiggsAudio C:\higgs-audio\.venv\Scripts\python.exe `
  "-m higgs_audio.openai_server --host 0.0.0.0 --port 8881 --device cuda --dtype float16"
nssm set HiggsAudio AppDirectory C:\higgs-audio
nssm set HiggsAudio Start SERVICE_AUTO_START
nssm start HiggsAudio
```

Now `Get-Service HiggsAudio` shows it running, and it survives reboots.

---

### Path B — Podman with GPU passthrough on Windows

Path A is recommended. Path B works but expect 1-2 hours of debugging.

```powershell
# 1. Verify Podman version (need 4.7+; older has bad GPU support)
podman --version

# 2. Open the Podman Machine WSL2 VM
podman machine ssh

# Now inside the WSL2 VM (Linux shell):
sudo dnf install -y dnf-plugins-core
sudo dnf config-manager --add-repo https://nvidia.github.io/libnvidia-container/stable/rpm/nvidia-container-toolkit.repo
sudo dnf install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=podman
sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml
exit

# 3. Back in PowerShell — verify GPU passthrough works
podman run --rm --device nvidia.com/gpu=all nvidia/cuda:12.4.0-base-ubuntu22.04 nvidia-smi
# -> should list the RTX 4070 Ti
```

If step 3 succeeds, you can run the Boson AI official image:

```powershell
git clone https://github.com/boson-ai/higgs-audio
cd higgs-audio
podman build -t higgs-audio:local .
podman run -d \
  --name higgs-audio \
  --device nvidia.com/gpu=all \
  -p 8881:8000 \
  -v higgs-models:/root/.cache/huggingface \
  -e MODEL=bosonai/higgs-audio-v2.5 \
  -e DTYPE=float16 \
  higgs-audio:local
```

If step 3 fails (most common: Podman Machine kernel doesn't expose the
NVIDIA WSL device), drop to Path A.

---

### Networking — Mac dials the Windows box

Two options. **Same LAN** is simplest if both machines stay home:

```bash
# On the Mac, from this repo:
make audiobook-sample-higgs ch=ch01 paragraphs=2 higgs_url=http://192.168.1.50:8881/v1

# Or set HIGGS_URL once per shell session:
export HIGGS_URL=http://192.168.1.50:8881/v1
make audiobook-sample-higgs ch=ch01 paragraphs=2
```

#### Tailscale — recommended for resilience

Free for personal use, ~10 min setup, gives both machines stable
WireGuard-based IPs (`100.x.y.z`) that work regardless of network. Big
quality-of-life win when you're working from a coffee shop, when the
home LAN's DHCP shifts, or when you want to render from anywhere.

On both Mac and Windows: install Tailscale, sign in with the same
account, run `tailscale up`. Each machine gets a stable IP and a magic
DNS hostname. Then:

```bash
export HIGGS_URL=http://gaming-rig.tail-scale.ts.net:8881/v1
# Or: http://100.x.y.z:8881/v1
```

The Windows Firewall rule above already allows `LocalSubnet` — you may
also need to allow the Tailscale subnet (`100.64.0.0/10`) explicitly:

```powershell
New-NetFirewallRule `
  -DisplayName "Higgs Audio API (Tailscale inbound)" `
  -Direction Inbound `
  -Protocol TCP `
  -LocalPort 8881 `
  -RemoteAddress 100.64.0.0/10 `
  -Action Allow
```

---

### Run a sample render against Higgs

On the Mac, after Higgs is up on the Windows box:

```bash
# 1. List available Higgs voices (from the Mac, via the LAN)
curl -s http://192.168.1.50:8881/v1/audio/voices | jq

# 2. Fill in the voice IDs in PRESETS_HIGGS (see audiobook.py)
#    OR pass --voice explicitly for a one-off:
HIGGS_URL=http://192.168.1.50:8881/v1 \
make audiobook-sample-higgs ch=ch01 paragraphs=2

# 3. Listen
open build/output/audiobook/ch01-when-saas-fights-reality_sample.mp3

# 4. Render a full chapter when satisfied with the voice mapping
HIGGS_URL=http://192.168.1.50:8881/v1 \
python3 build/audiobook.py --engine higgs --only ch01 --base-url $HIGGS_URL --force
```

On the first sample render against `--engine higgs` you'll get a clear
error if `PRESETS_HIGGS` voice IDs are still placeholder `None`. The
error message tells you to query `/v1/audio/voices`, fill in the IDs,
and retry. This is intentional — voice catalog is engine-specific and
must be populated explicitly before unattended renders.

### Setup path C — Replicate (cloud API, no local install)

Still useful as a quick A/B if you want to hear v2.5 quality before
committing to the Windows install. Pricing was $0.005–0.05 per second
of audio at last check; a 1-paragraph quality test costs ~$1–2.

```bash
export REPLICATE_API_TOKEN=r8_...
curl -s -X POST https://api.replicate.com/v1/predictions \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "version": "lucataco/higgs-audio-v2:latest",
    "input": {"text": "Local first, cloud second.", "voice": "default"}
  }'
```

### Voice cloning (Higgs)

3-second clean recording of a target voice → drop into the voices
directory mounted at `./audio/voices` → reference by filename in the
TTS request. The faster-higgs-audio README has the exact field name.

For commercial-licensed pro VA samples (the path discussed earlier — no
celebrity cloning), download an MIT/CC-licensed clip from Higgs's
preset voice library or VCTK, clone, render.

---

## 3. Voice options summary

What the audiobook pipeline can use, organized by source and license:

### Kokoro presets (already wired into `build/audiobook.py`)

67 voices available; the book's `PRESETS` dict uses these blends:

- **female / female-solo** — `af_bella` (+ `af_nicole` blend) — Voss, narrator alt
- **male / male-solo** — `am_michael` (+ `am_fenrir` blend) — narrator default
- **sinek** — `am_michael` at 0.88 speed — preface/epilogue/ch10 deliberate cadence
- **practitioner** — `am_michael` at 0.95 speed — Ferreira (Ch09)
- **british / british-male** — `bf_emma`, `bm_george` — Okonkwo (Ch07)
- **fry / fry-blend** — `bm_fable` (+ `bm_george` blend) — Shevchenko (Ch06)
- **fenrir** — `am_fenrir` solo — Kelsey (Ch08)

License: Kokoro-82M is Apache 2.0, voice samples included with the model
are documented as commercially usable (verify per voice in the upstream
repo — `hexgrad/Kokoro-82M`).

### Higgs preset voices

Boson AI ships ~25 preset voices in the v2 release. License terms in the
upstream repo's MODEL_CARD; commercial use generally permitted but verify
per voice before publishing.

### Commercially-licensed VA voices (for sellable-on-Audible final master)

Not in this Docker stack — see the parallel discussion on cloud APIs:

- **ElevenLabs Voice Library** — 50+ pro VA voices, explicit commercial AI license
- **Findaway Voices AI Generation Library** — designed for Audible-grade AI audiobooks
- **Hire-and-clone** — pay a real VA $200–500 for a 5-minute recording, license it explicitly for AI cloning, then clone via Higgs/F5/XTTS

### Voices NOT to use

Cloning identifiable real people without explicit consent:

- **Celebrities** (Morgan Freeman, James Earl Jones, etc.) — right of publicity
  liability under US state law (Bette Midler v. Ford 1988, Tom Waits v. Frito-Lay
  1992); Tennessee ELVIS Act 2024; pending federal NO FAKES Act
- **Real VAs without their AI license** — SAG-AFTRA actively monitors and pursues
- **Public figures, podcasters, journalists** — same right-of-publicity exposure

ACX/Audible terms of service require warranty that you own the voice
rights. Submission with an unauthorized cloned voice is grounds for
delisting.

---

## 4. Operational notes

### Bring everything up after a reboot

```bash
docker compose -f build/docker-compose.audio.yml up -d kokoro
# (and 'higgs' once the local image is built and uncommented)
```

### Stop everything

```bash
docker compose -f build/docker-compose.audio.yml down
```

### Free disk space

```bash
docker volume rm kokoro-models           # ~440 MB cache wipe
docker rmi ghcr.io/remsky/kokoro-fastapi-cpu:latest    # ~5.6 GB image wipe
```

### Health check

```bash
curl -s http://localhost:8880/health
# Kokoro returns: {"status":"healthy"}
```

### Listen to a sample

The `audiobook-sample` Make target writes to
`build/output/audiobook/<stem>_sample.mp3`. On macOS:

```bash
open build/output/audiobook/ch01-when-saas-fights-reality_sample.mp3
```

### Memory tuning (if Docker is slow or higgs OOMs)

Docker Desktop → Settings → Resources → Memory:

- **Kokoro alone**: 4 GB Docker memory is sufficient (current default)
- **Higgs (quantized int8) alone**: 12 GB minimum
- **Both running concurrently**: 16 GB minimum

The host is 32 GB DDR4; allocating 16 GB to Docker leaves enough
headroom for the parent shell + audiobook.py + ffmpeg mastering pipeline.
