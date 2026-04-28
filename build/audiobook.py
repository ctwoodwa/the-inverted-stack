"""Generate audiobook MP3s from chapter markdown using a local Kokoro TTS server.

Usage:
    python build/audiobook.py                         # build everything (skip existing)
    python build/audiobook.py --only ch05             # single chapter
    python build/audiobook.py --force                 # re-render everything
    python build/audiobook.py --voice af_sky          # pick a different voice
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from openai import OpenAI

# Whispersync alignment capture: emit per-chunk timing for EPUB 3 Media Overlays
ALIGNMENTS_DIR = Path(__file__).resolve().parent.parent / "chapters" / "_voice-drafts" / "_alignments"


_DURATION_RE = re.compile(r"time=(\d+):(\d+):(\d+(?:\.\d+)?)")


def _mp3_duration_seconds(mp3_bytes: bytes) -> float:
    """Measure MP3 duration via ffmpeg's stderr parsing (bundled binary).

    Pipes the MP3 bytes through `ffmpeg -i pipe:0 -f null -`, which reports
    `time=HH:MM:SS.fff` on stderr at process end. This is more robust than
    a CBR byte-rate estimate for variable Kokoro chunk lengths.

    Used during render to build the per-chunk alignment table for EPUB 3
    Media Overlays. Adds ~30-50ms per chunk; total overhead for a 27-chapter
    rebuild is ~1 minute of extra wall clock.
    """
    import imageio_ffmpeg  # local import to avoid breaking environments without it
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    proc = subprocess.run(
        [ffmpeg_exe, "-hide_banner", "-loglevel", "info", "-i", "pipe:0", "-f", "null", "-"],
        input=mp3_bytes, capture_output=True, timeout=30,
    )
    # ffmpeg writes progress to stderr; the final time= line gives total duration
    stderr = proc.stderr.decode("utf-8", errors="replace") if proc.stderr else ""
    matches = _DURATION_RE.findall(stderr)
    if matches:
        h, m, s = matches[-1]  # last time= is end of stream
        return int(h) * 3600 + int(m) * 60 + float(s)
    # Fallback: estimate from byte size assuming 128 kbps CBR mono (Kokoro default)
    return len(mp3_bytes) / (16 * 1024)

REPO = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = REPO / "chapters"
OUT_DIR = REPO / "build" / "output" / "audiobook"
SCRIPTS_DIR = OUT_DIR / "scripts"

# Conservative: only acronyms/proper nouns that espeak demonstrably mangles.
# Capitalized common acronyms (CRDT, JWT, OAuth, HTTP, JSON, etc.) spell out
# correctly in Kokoro by default — leave them alone to avoid over-correction.
ACRONYM_FIXES = {
    r"\bSaaS\b": "SASS",
    r"\bYDotNet\b": "Y-dot-Net",
    r"\bSQLCipher\b": "SQL Cipher",
    r"\bSQLite\b": "S-Q-Lite",
    r"\bLoro\b": "LORE-oh",
    r"\bMAUI\b": "MOW-ee",
    r"\bCI/CD\b": "C-I C-D",
    r"\bI/O\b": "I-O",
    r"\bP2P\b": "peer to peer",
    r"\bK8s\b": "Kubernetes",
    r"\bASP\.NET\b": "ASP dot NET",
    r"\bCRDT\b": "C-R-D-T",
    r"\bgRPC\b": "G-R-P-C",
    r"\bWebAssembly\b": "Web Assembly",
    r"\bSignalR\b": "Signal-R",
    r"\bYjs\b": "Y-J-S",
    r"\bDEK\b": "D-E-K",
    r"\bKEK\b": "K-E-K",
    r"\bMDM\b": "M-D-M",
    r"\bSBOM\b": "S-bom",
    r"\bAP/CP\b": "A-P / C-P",
    r"\bRFC (\d+)\b": r"R-F-C \1",

    # Regulatory initialisms (heavy throughout this book). Plurals listed
    # separately to keep word boundaries clean.
    r"\bGDPR\b":   "G-D-P-R",
    r"\bDPDP\b":   "D-P-D-P",
    r"\bNDPR\b":   "N-D-P-R",
    r"\bNDPA\b":   "N-D-P-A",
    r"\bLGPD\b":   "L-G-P-D",
    r"\bDIFC\b":   "D-I-F-C",
    r"\bDPL\b":    "D-P-L",
    r"\bDPA\b":    "D-P-A",
    r"\bEDPB\b":   "E-D-P-B",
    r"\bCNIL\b":   "C-N-I-L",
    r"\bBSI\b":    "B-S-I",
    r"\bRBI\b":    "R-B-I",
    r"\bBFSI\b":   "B-F-S-I",
    r"\bMLPS\b":   "M-L-P-S",
    r"\bFERPA\b":  "F-E-R-P-A",
    r"\bGLBA\b":   "G-L-B-A",
    r"\bCCPA\b":   "C-C-P-A",
    r"\bCPRA\b":   "C-P-R-A",
    r"\bITAR\b":   "I-T-A-R",
    r"\bCMMC\b":   "C-M-M-C",
    r"\bADR\b":    "A-D-R",
    r"\bARCO\b":   "A-R-C-O",
    r"\bSCCs\b":   "S-C-C-s",  # keep lowercase 's' for plural
    r"\bSCC\b":    "S-C-C",
    r"\bBCRs\b":   "B-C-R-s",
    r"\bBCR\b":    "B-C-R",

    # Cryptography & security
    r"\bHSM\b":    "H-S-M",
    r"\bMFA\b":    "M-F-A",
    r"\bSSO\b":    "S-S-O",
    r"\bCMK\b":    "C-M-K",
    r"\bBYOC\b":   "B-Y-O-C",
    r"\bTPM\b":    "T-P-M",
    r"\bTLS\b":    "T-L-S",
    r"\bTCP\b":    "T-C-P",
    r"\bWAL\b":    "W-A-L",
    r"\bDAG\b":    "D-A-G",
    r"\bHKDF\b":   "H-K-D-F",
    r"\bKDF\b":    "K-D-F",
    r"\bKMS\b":    "K-M-S",
    r"\bSDK\b":    "S-D-K",
    r"\bCLI\b":    "C-L-I",
    r"\bIDE\b":    "I-D-E",
    r"\bFFI\b":    "F-F-I",

    # Tech and engineering
    r"\bAPIs\b":   "A-P-Is",
    r"\bAPI\b":    "A-P-I",
    r"\bSLA\b":    "S-L-A",
    r"\bSLO\b":    "S-L-O",
    r"\bSLI\b":    "S-L-I",
    r"\bCISO\b":   "C-I-S-O",
    r"\bCTO\b":    "C-T-O",
    r"\bCIO\b":    "C-I-O",
    r"\bICT\b":    "I-C-T",
    r"\bIoT\b":    "I-O-T",
    r"\bIPC\b":    "I-P-C",
    r"\bISV\b":    "I-S-V",
    r"\bIETF\b":   "I-E-T-F",
    r"\bPDF\b":    "P-D-F",
    r"\bHTML\b":   "H-T-M-L",
    r"\bCSS\b":    "C-S-S",
    r"\bSQL\b":    "S-Q-L",
    r"\bCSV\b":    "C-S-V",
    r"\bMP3\b":    "M-P-3",
    r"\bTTS\b":    "T-T-S",
    r"\bM4B\b":    "M-4-B",
    r"\bEBU\b":    "E-B-U",
    r"\bCBOR\b":   "C-B-O-R",

    # Geographic / org
    r"\bEEA\b":    "E-E-A",
    r"\bGCC\b":    "G-C-C",
    r"\bICP\b":    "I-C-P",
    r"\bICM\b":    "I-C-M",

    # Audit / compliance abbreviations
    r"\bSOC (\d)\b": r"S-O-C \1",  # SOC 2, SOC 1, etc.

    # Plurals of CRDT, APIs (defined above)
    r"\bCRDTs\b":  "C-R-D-T-s",

    # Roman numerals after "Part" — espeak mispronounces these as
    # "eye", "eye-eye", "triple-eye" etc. Spell them as Arabic digits.
    # Word boundaries prevent shorter forms from matching inside longer
    # ones (e.g. \bPart I\b does not match inside "Part II").
    r"(?i)\bPart I\b":    "Part 1",
    r"(?i)\bPart II\b":   "Part 2",
    r"(?i)\bPart III\b":  "Part 3",
    r"(?i)\bPart IV\b":   "Part 4",
    r"(?i)\bPart V\b":    "Part 5",
    r"(?i)\bPart VI\b":   "Part 6",
    r"(?i)\bPart VII\b":  "Part 7",
    r"(?i)\bPart VIII\b": "Part 8",
    r"(?i)\bPart IX\b":   "Part 9",
    r"(?i)\bPart X\b":    "Part 10",
}

# Proper-noun pronunciation lexicon. These are the names espeak gets wrong
# enough that listeners notice. Add entries by listening to a render and
# noting any name that came out wrong. Format is the same as ACRONYM_FIXES:
# regex (with \b word boundaries) -> respelling that espeak phonemizes
# correctly. Stress is denoted by capital letters on the stressed syllable.
PROPER_NOUN_FIXES = {
    # Council members in Part II (named in chapters' first-person rewrites)
    r"\bShevchenko\b":    "shev-CHEN-koh",
    r"\bOkonkwo\b":       "oh-KONK-woh",
    r"\bFerreira\b":      "feh-RAY-rah",
    r"\bTomás\b":         "toh-MAHS",
    # Tomas without accent — fallback if the diacritic is stripped upstream
    r"\bTomas\b":         "toh-MAHS",
    # Voss / Kelsey / Voss read correctly by default — no override needed.

    # Technical and legal proper nouns the book cites repeatedly.
    r"\bSchrems\b":       "shrems",
    r"\bKleppmann\b":     "KLEP-mahn",
    r"\bFlease\b":        "fleeze",
    r"\bRoskomnadzor\b":  "ros-kom-NOD-zor",
    r"\bAnpd\b":          "A-N-P-D",
    r"\bANPD\b":          "A-N-P-D",
}

# Common abbreviations that espeak mispronounces or reads literally.
# Order matters: longer patterns first so "i.e." doesn't match part of a
# longer compound. Apply with re.sub(pattern, replacement, text).
ABBREVIATION_FIXES = {
    r"(?i)\bi\.e\.,?": "that is,",
    r"(?i)\be\.g\.,?": "for example,",
    r"(?i)\betc\.":    "and so on",
    r"(?i)\bvs\.":     "versus",
    r"(?i)\bcf\.":     "compare",
    r"(?i)\bc\.f\.":   "compare",
    r"(?i)\bp\.m\.":   "P-M",
    r"(?i)\ba\.m\.":   "A-M",
    r"(?i)\bv1\.0\b":  "version one point zero",
    r"(?i)\bpre-1\.0\b": "pre-version-one",
}

# Named voice + speed presets. --preset selects one; --voice/--speed override.
# Rationale for each is documented in the audiobook research notes.
#
# Two engine catalogs share the same preset KEY space — "sinek", "british",
# "fenrir", etc. — so CHAPTER_PRESET_MAP works across both engines without
# rewiring. The VOICE values differ because Kokoro and Higgs have different
# voice catalogs. resolve_preset() picks the right catalog based on --engine.
PRESETS_KOKORO: dict[str, dict] = {
    # Female — HH-hour trained voices. Bella = professional core, Nicole = breath texture.
    "female":      {"voice": "af_bella+af_nicole", "speed": 0.92},
    "female-solo": {"voice": "af_bella",           "speed": 0.92},

    # Male — all C+ / H-hour. Michael = lower-pitch non-fiction register;
    # Fenrir adds "velvety texture" to counter Michael's known dryness.
    "male":        {"voice": "am_michael+am_fenrir", "speed": 0.92},
    "male-solo":   {"voice": "am_michael",           "speed": 0.92},

    # Sinek — am_michael has the lowest pitch (~125 Hz) and warmest register
    # in the male lineup. Slow speed (0.88) approximates Sinek's signature
    # deliberate, emphatic cadence. Pauses already injected at section breaks.
    "sinek":       {"voice": "am_michael",           "speed": 0.88},

    # Practitioner — am_michael at 0.95 (slightly faster than the male/sinek
    # body cadences). Used for Ferreira (Ch09 — Lusophone practitioner). The
    # speed shift differentiates Ferreira from the narrator (who uses sinek
    # 0.88 and male 0.92) without changing the base voice — Kokoro has no
    # Lusophone-accented English voice, so the prose carries the accent work
    # via first-person register. If listening tests show narrator confusion,
    # switch to bm_george for a clearer voice break.
    "practitioner":{"voice": "am_michael",           "speed": 0.95},

    # British — bf_emma is the only B-grade UK voice. bm_george for male
    # British is C/MM — expect lower quality, use only if accent matters.
    "british":     {"voice": "bf_emma",              "speed": 0.92},
    "british-male":{"voice": "bm_george",            "speed": 0.92},

    # Fry — Stephen Fry-adjacent: British RP, theatrical warmth, measured
    # narrator cadence. bm_fable is the community's go-to British male for
    # storytelling (name aside, it's the most narrator-like). Caveat: C-grade
    # MM-minutes training — expect audibly lower quality than female presets.
    "fry":         {"voice": "bm_fable",             "speed": 0.92},
    "fry-blend":   {"voice": "bm_fable+bm_george",   "speed": 0.92},

    # Fenrir — am_fenrir solo. Higher pitch (144 Hz), "velvety texture,
    # tech-savvy." Polished corporate confident register.
    "fenrir":      {"voice": "am_fenrir",            "speed": 0.92},
}

# Chatterbox preset voices. Chatterbox is voice-cloning native — non-stock
# voice IDs are reference-clip uploads, queried via `GET /v1/audio/voices`
# (auth required). Stock voices that ship with the model are used as
# fallbacks for `male`/`female`; persona-specific slots stay None until
# reference clips are uploaded via build/voice_upload.py.
#
# Stock catalog (verified 2026-04-28 against the Windows server):
#   en_man, en_woman, broom_salesman (Ollivander/British male older),
#   mabel (warm British-leaning female). The other ~12 stock voices are
#   sitcom characters, child voices, or non-English — not narrator-fit.
#
# NOTE: Chatterbox renders at 24 kHz mono. Speed values below are kept
# as hints; the server clamps to a sane range. Verify when wiring up
# new persona voices via build/audiobook_voices_init.py (planned).
PRESETS_CHATTERBOX: dict[str, dict] = {
    "female":      {"voice": "en_woman",       "speed": 1.0},   # stock fallback
    "female-solo": {"voice": "en_woman",       "speed": 1.0},   # stock fallback
    "male":        {"voice": "en_man",         "speed": 1.0},   # stock fallback
    "male-solo":   {"voice": "en_man",         "speed": 1.0},   # stock fallback
    "sinek":       {"voice": "en_man",         "speed": 0.92},  # stock fallback; TODO upload warm low-pitch male
    "practitioner":{"voice": "en_man",         "speed": 1.0},   # stock fallback; TODO upload Lusophone-adjacent male (Ferreira)
    "british":     {"voice": "mabel",          "speed": 1.0},   # stock British-leaning female (warm)
    "british-male":{"voice": "broom_salesman", "speed": 1.0},   # stock older British male
    "fry":         {"voice": "broom_salesman", "speed": 1.0},   # closest stock RP register
    "fry-blend":   {"voice": "broom_salesman", "speed": 1.0},   # alias (no blend support in Chatterbox)
    "fenrir":      {"voice": "en_man",         "speed": 1.0},   # stock fallback; TODO upload polished corporate male
}

# Backwards-compat alias — old code paths may import PRESETS_HIGGS.
# Removable once the rest of the tree is swept; harmless until then.
PRESETS_HIGGS = PRESETS_CHATTERBOX

# Engine catalog. Add a new entry here to support a new TTS backend; the
# rest of the script picks up the new engine via --engine.
#
# `requires_auth: True` engines pull a Bearer token from the TTS_API_KEY env
# var (or --api-key CLI flag). Kokoro runs locally without auth; Chatterbox
# on the Windows box requires it.
ENGINES: dict[str, dict] = {
    "kokoro": {
        "presets": PRESETS_KOKORO,
        "default_base_url": "http://localhost:8880/v1",
        "model_name": "kokoro",
        "requires_auth": False,
        "description": "Kokoro-82M FastAPI on the local Mac (default daily-driver)",
    },
    "chatterbox": {
        "presets": PRESETS_CHATTERBOX,
        # Override at the CLI with --base-url. Default is the Tailscale
        # hostname for the Windows GPU box. Override examples:
        #   CHATTERBOX_URL=http://192.168.1.50:8881/v1 python build/audiobook.py --engine chatterbox
        #   --base-url http://desktop-umt08rn.taildefd38.ts.net:8881/v1
        "default_base_url": "http://desktop-umt08rn:8881/v1",
        "model_name": "chatterbox",
        "requires_auth": True,
        "description": "Chatterbox (Resemble AI) on the Windows GPU box — voice-cloning, high-quality path",
    },
}

# Backwards-compatibility alias — older callers (tests, external scripts)
# may import PRESETS directly. Defaults to the Kokoro catalog.
PRESETS = PRESETS_KOKORO

# Per-chapter preset overrides. Key is matched as a substring against the
# source path. Part II council chapters each get a voice that gender-matches
# the named member; Ch10 returns to the main narrator because it's the
# book's synthesis of the council's output. Council members and their
# personas are: Voss (Ch05, F), Shevchenko (Ch06, M, Slavic), Okonkwo
# (Ch07, F, Nigerian), Kelsey (Ch08, M), Ferreira (Ch09, M, Lusophone).
# Kokoro lacks Slavic/Nigerian/Lusophone English accents, so prose register
# carries the accent work; voices select for gender + persona register.
CHAPTER_PRESET_MAP: dict[str, str] = {
    "preface":                             "sinek",        # author's voice, deliberate cadence
    "ch05-enterprise-lens":                "female-solo",  # Voss — F, professional/authoritative (af_bella)
    "ch06-distributed-systems-lens":       "fry",          # Shevchenko — M, academic researcher (bm_fable)
    "ch07-security-lens":                  "british",      # Okonkwo — F, international serious-security (bf_emma)
    "ch08-product-economic-lens":          "fenrir",       # Kelsey — M, polished corporate confident (am_fenrir)
    "ch09-local-first-practitioner-lens":  "practitioner", # Ferreira — M, am_michael at 0.95 (warm, faster than narrator)
    "ch10-synthesis":                      "sinek",        # main narrator returns
    "epilogue":                            "sinek",        # closing, deliberate
}

CHAPTER_FILES = [
    "front-matter/preface.md",
    "part-1-thesis-and-pain/ch01-when-saas-fights-reality.md",
    "part-1-thesis-and-pain/ch02-local-first-serious-stack.md",
    "part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md",
    "part-1-thesis-and-pain/ch04-choosing-your-architecture.md",
    "part-2-council-reads-the-paper/ch05-enterprise-lens.md",
    "part-2-council-reads-the-paper/ch06-distributed-systems-lens.md",
    "part-2-council-reads-the-paper/ch07-security-lens.md",
    "part-2-council-reads-the-paper/ch08-product-economic-lens.md",
    "part-2-council-reads-the-paper/ch09-local-first-practitioner-lens.md",
    "part-2-council-reads-the-paper/ch10-synthesis.md",
    "part-3-reference-architecture/ch11-node-architecture.md",
    "part-3-reference-architecture/ch12-crdt-engine-data-layer.md",
    "part-3-reference-architecture/ch13-schema-migration-evolution.md",
    "part-3-reference-architecture/ch14-sync-daemon-protocol.md",
    "part-3-reference-architecture/ch15-security-architecture.md",
    "part-3-reference-architecture/ch16-persistence-beyond-the-node.md",
    "part-4-implementation-playbooks/ch17-building-first-node.md",
    "part-4-implementation-playbooks/ch18-migrating-existing-saas.md",
    "part-4-implementation-playbooks/ch19-shipping-to-enterprise.md",
    "part-4-implementation-playbooks/ch20-ux-sync-conflict.md",
    "part-5-operational-concerns/ch21-operating-a-fleet.md",
    "epilogue/epilogue-what-the-stack-owes-you.md",
    "appendices/appendix-a-sync-daemon-wire-protocol.md",
    "appendices/appendix-b-threat-model-worksheets.md",
    "appendices/appendix-c-further-reading.md",
    "appendices/appendix-d-testing-the-inverted-stack.md",
    "appendices/appendix-e-citation-style.md",
    "appendices/appendix-f-regulatory-coverage.md",
]

CHUNK_CHAR_BUDGET = 700  # target per-request size in characters (Kokoro default)

# Engine-aware chunk budget. Chatterbox caps each request at ~100 sec /
# ~2500 tokens; cloned voices + V12 dramatic recipe (cfg_weight=0.3
# slows pacing) push longer chunks past the cap, producing trailing
# silence. 400 char target keeps each chunk well under the limit even
# with the slowest combinations.
CHUNK_BUDGETS_BY_ENGINE: dict[str, int] = {
    "kokoro":     700,
    "chatterbox": 400,
}
# Lowered from 1400 (2026-04-28, bug-096/bug-097). Root cause is
# *progressive* slowdown in the CPU Kokoro container — early chunks
# render in ~3-5s, but after ~70 chunks the same-sized chunk takes
# 30-60s and the worker eventually hangs (memory leak / thermal /
# worker degradation). Lowering chunk size is a partial mitigation,
# not a fix. For long renders on CPU Kokoro the practical paths are:
# (a) wrap with periodic `docker restart kokoro-fastapi` every ~50
# chunks; (b) add resume-capable rendering (sidecar manifest + chunk
# concat); (c) run on a GPU instance. See .wolf/buglog.json bug-097.

# Mapping from dot count to silence duration (seconds). Empirically, Kokoro
# treats consecutive periods as ~one sentence terminator regardless of count
# — six dots produce ~0.7s, the same as one period. To get the long pauses
# the prose design intended (H1 chapter break, H2 section break, em-dash
# apposition), we render dot-only chunks as explicit silence MP3 segments
# rather than sending them to the TTS.
PAUSE_DURATIONS = {
    2: 0.30,   # rare; treat as a beat
    3: 0.70,   # ... — em-dash apposition
    4: 1.20,   # .... — H2 section break
    5: 1.50,
    6: 1.80,   # ...... — H1 chapter break
    7: 2.00,
    8: 2.20,
}

# Cache silence MP3 segments by duration (in 100ms buckets). 24kHz mono
# 128kbps to match Kokoro's raw output format — concatenation requires
# identical sample rate and channel layout.
_SILENCE_CACHE: dict[int, bytes] = {}


def _is_pause_only(text: str) -> int:
    """Return the dot count if the chunk contains only dots and whitespace,
    otherwise 0. Used to identify pause markers in sentence-mode chunking."""
    s = text.strip()
    if not s:
        return 0
    if all(c in ". \t\n" for c in s):
        return s.count(".")
    return 0


def silence_mp3(duration_s: float) -> bytes:
    """Return an MP3 byte string of the given duration in 24kHz mono 128kbps,
    matching Kokoro's raw output format. Cached by 100ms bucket."""
    import imageio_ffmpeg
    import subprocess
    bucket_ms = int(round(duration_s * 10)) * 100  # 100ms buckets
    if bucket_ms in _SILENCE_CACHE:
        return _SILENCE_CACHE[bucket_ms]
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    duration = bucket_ms / 1000.0
    cmd = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
        "-t", f"{duration:.3f}",
        "-c:a", "libmp3lame", "-b:a", "128k",
        "-f", "mp3", "pipe:1",
    ]
    proc = subprocess.run(cmd, capture_output=True, check=True)
    _SILENCE_CACHE[bucket_ms] = proc.stdout
    return proc.stdout


_ORDINAL_WORDS = {
    1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth",
    6: "Sixth", 7: "Seventh", 8: "Eighth", 9: "Ninth", 10: "Tenth",
}


def _ordinal_word(n: int) -> str:
    """Convert a parenthetical (N) marker into a spoken ordinal cue with a
    trailing comma so espeak inserts a micro-pause. Beyond ten, fall back
    to "Item N," which reads correctly without enumerating large ordinals."""
    if n in _ORDINAL_WORDS:
        return f"{_ORDINAL_WORDS[n]},"
    return f"Item {n},"


def _expand_numbers(t: str) -> str:
    """Expand currency and percentage shorthand that espeak mishandles.

    Conservative scope — only the patterns that demonstrably misread:
    - N%       -> "N percent"        (espeak: "N percent" ok but inconsistent)
    - $NK/M/B  -> "N thousand/million/billion dollars"
    - NK/NM    -> left alone (ambiguous: K could be Kelvin, M could be mega)

    Plain integers, decimals, and comma-grouped numbers (10,000) are left
    to espeak's default reader — it handles those cleanly.
    """
    # Percentages: "20%" -> "20 percent"; preserve the integer for espeak
    # to read normally. Decimals like "3.5%" are also handled.
    t = re.sub(r"(\d+(?:\.\d+)?)\s*%", r"\1 percent", t)

    # Currency with magnitude (letter suffix or full word). Choose singular
    # "dollar" vs plural "dollars" by attributive-vs-predicative position:
    #
    #   attributive (modifies a following noun)  -> singular "dollar"
    #     "$4.2 million renovation"   -> "4.2 million dollar renovation"
    #     "$50M Series A round"       -> "50 million dollar Series A round"
    #
    #   predicative (the amount itself, before preposition / conjunction /
    #   verb / sentence end)         -> plural "dollars"
    #     "spent $4.2 million."       -> "spent 4.2 million dollars."
    #     "Revenue of $10 billion."   -> "Revenue of 10 billion dollars."
    #     "$10B in funding"           -> "10 billion dollars in funding"
    #     "$10 million and counting"  -> "10 million dollars and counting"
    suffix_map = {"K": "thousand", "M": "million", "B": "billion", "T": "trillion"}
    _NON_ATTRIBUTIVE_FOLLOWERS = {
        # Coordinating conjunctions / list markers
        "and", "or", "but", "plus", "minus", "nor",
        # Prepositions commonly following amounts
        "in", "of", "for", "to", "on", "per", "from", "over", "under",
        "with", "after", "before", "between", "among", "across", "through",
        "into", "onto", "upon", "since", "until", "against", "beyond",
        "above", "below", "by", "at", "around", "near", "without",
        # BE / HAVE / DO / modal auxiliaries
        "is", "was", "are", "were", "be", "been", "being",
        "has", "had", "have", "having",
        "will", "would", "shall", "should", "could", "might", "may", "can",
        "do", "does", "did", "done", "doing",
    }

    # Prepositions / verbs / quantifiers that, when they PRECEDE the amount,
    # make the amount predicative regardless of what follows. "Revenue of
    # $10 billion last year" — the "of" makes "$10 billion" a quantity,
    # not an adjective modifying "last year."
    _PRECEDED_BY_PREDICATIVE = {
        "of", "for", "with", "at", "by", "to", "in", "on", "from",
        "around", "about", "over", "under", "above", "below", "near",
        "between", "approximately", "roughly", "nearly", "almost", "exactly",
        "spent", "raised", "earned", "lost", "paid", "owes", "owed", "saved",
        "worth", "valued",
    }

    def _decide_dollar_word(before_text: str, after_text: str) -> str:
        """Return 'dollar' or 'dollars' based on context surrounding the amount."""
        # Predicative if PRECEDED by a preposition / quantifier / money verb.
        # Look back for the most recent word before the $.
        prev_match = re.search(r"(\w+)\W*$", before_text)
        if prev_match and prev_match.group(1).lower() in _PRECEDED_BY_PREDICATIVE:
            return "dollars"
        # Predicative if FOLLOWED by punctuation / preposition / verb / conjunction.
        stripped = after_text.lstrip()
        if not stripped or stripped[0] in '.,;:!?)':
            return "dollars"
        next_match = re.match(r"\w+", stripped)
        if not next_match:
            return "dollars"
        if next_match.group(0).lower() in _NON_ATTRIBUTIVE_FOLLOWERS:
            return "dollars"
        # Default: attributive (the amount is modifying the next noun).
        return "dollar"

    def _currency_letter_sub(m: re.Match) -> str:
        amount = m.group(1)
        word = suffix_map[m.group(2).upper()]
        before = m.string[max(0, m.start() - 30):m.start()]
        after = m.string[m.end():m.end() + 30]
        return f"{amount} {word} {_decide_dollar_word(before, after)}"

    def _currency_word_sub(m: re.Match) -> str:
        amount = m.group(1)
        magnitude = m.group(2).lower()
        before = m.string[max(0, m.start() - 30):m.start()]
        after = m.string[m.end():m.end() + 30]
        return f"{amount} {magnitude} {_decide_dollar_word(before, after)}"

    t = re.sub(r"\$(\d+(?:\.\d+)?)\s*([KMBTkmbt])\b", _currency_letter_sub, t)
    t = re.sub(
        r"\$(\d+(?:\.\d+)?)\s+(thousand|million|billion|trillion)\b",
        _currency_word_sub,
        t,
        flags=re.IGNORECASE,
    )
    # Plain "$N" without magnitude suffix: espeak reads as "dollar N" which
    # sounds inverted. Convert to "N dollar(s)" using the same heuristic.
    def _currency_plain_sub(m: re.Match) -> str:
        amount = m.group(1)
        before = m.string[max(0, m.start() - 30):m.start()]
        after = m.string[m.end():m.end() + 30]
        return f"{amount} {_decide_dollar_word(before, after)}"

    t = re.sub(r"\$(\d+(?:\.\d+)?)\b", _currency_plain_sub, t)

    return t


def narratable_text(md: str, source_only: bool = False,
                    engine: str = "kokoro") -> str:
    """Convert a chapter markdown file to a clean narration script.

    When ``source_only`` is True, only structural transforms run (strip
    code/tables/comments, normalize headings, list-bullet stripping). All
    TTS-specific token swaps (currency expansion, acronym definitions,
    proper-noun pronunciation, abbreviation expansion, em-dash → comma,
    parenthetical-list ordinals) are SKIPPED. The result preserves the
    original prose words and sentence boundaries, so the per-sentence chunk
    count matches the TTS chunking exactly. Used by render_chapter() to
    capture a ``source_text`` field on each alignment chunk for EPUB 3 Media
    Overlay fragment ID injection — the source text matches what Pandoc
    emits in the XHTML, while the TTS-rendered text does not.

    The ``engine`` parameter gates espeak-specific transforms that hurt
    quality on neural TTS engines like Chatterbox. Chatterbox handles
    foreign names, acronyms, and em-dash pacing natively — the
    PROPER_NOUN_FIXES / ACRONYM_FIXES / em-dash → comma passes were
    designed around espeak's mispronunciations and force unnecessary
    letter-by-letter enunciation on Chatterbox. Default is "kokoro"
    (full preprocessing) to preserve existing behavior; pass
    "chatterbox" to skip espeak-specific transforms.
    """
    is_neural = engine == "chatterbox"
    t = md

    # Strip HTML comments (ICM stage markers, target word counts, etc.)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.DOTALL)

    # Strip fenced code + mermaid blocks; replace with a short verbal cue only
    # when the surrounding prose doesn't already announce them.
    def _fence_sub(match: re.Match) -> str:
        lang = (match.group(1) or "").strip().lower()
        if lang == "mermaid":
            return "\n\n(Diagram omitted. See the book.)\n\n"
        return "\n\n(Code listing omitted. See the book.)\n\n"

    t = re.sub(r"```([^\n`]*)\n.*?\n```", _fence_sub, t, flags=re.DOTALL)

    # Strip tables (GFM pipe tables)
    t = re.sub(
        r"(?m)^\|.*\|\s*$\n(?:\|[\s:\-|]+\|\s*\n)?(?:\|.*\|\s*\n?)+",
        "\n\n(Table omitted. See the book.)\n\n",
        t,
    )

    # Strip images ![alt](url) entirely
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", t)

    # Turn [text](url) into just text
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)

    # Strip IEEE-style "[Online]. Available: URL" boilerplate from references.
    # The audiobook listener can't follow URLs; the print/EPUB version retains them.
    t = re.sub(r"\[Online\]\.?\s*Available:\s*\S+\.?\s*", "", t, flags=re.IGNORECASE)

    # Strip bare protocol URLs that survived markdown link extraction.
    # Consume surrounding whitespace to avoid leaving double-spaces in prose.
    t = re.sub(r"\s*https?://\S+\s*", " ", t)

    # Strip IEEE bracketed citation markers like [1], [2], [1, 2], [1-3].
    # These point to numbered references at the end of each chapter — useful
    # in print, gibberish in audio. The lookahead optionally consumes ", "
    # when another citation follows immediately, so "[2], [4]" becomes ""
    # not ",". Run twice to handle three-or-more chained citations like "[1], [2], [3]".
    _CITATION_RE = r"\s*\[\s*\d+(?:\s*[,\-]\s*\d+)*\s*\](\s*,(?=\s*\[))?"
    t = re.sub(_CITATION_RE, "", t)
    t = re.sub(_CITATION_RE, "", t)

    # Headings: drop the hashes so they read as plain sentences.
    # H1 chapter titles get the longest trailing beat; H2 gets a medium
    # beat; H3+ get no dot-pause (the period alone is enough). Kokoro's
    # espeak backend treats consecutive `.` as additive silence — six
    # dots is audibly longer than three, four is between the two.
    # "# Chapter 1 — Foo" -> "\n\nChapter 1, Foo.\n\n......\n\n"
    def _heading_sub(match: re.Match) -> str:
        level = len(match.group(1))
        body = match.group(2).strip().rstrip(".")
        # Em-dash in titles reads cleaner as a comma pause for headings.
        body = body.replace("—", ",").replace("–", ",")
        if level == 1:
            return f"\n\n{body}.\n\n......\n\n"  # long pause after chapter title
        if level == 2:
            return f"\n\n{body}.\n\n....\n\n"    # medium pause after section
        return f"\n\n{body}.\n\n"                # subsection — no dot pause

    t = re.sub(r"(?m)^(#{1,6})\s+(.+?)\s*$", _heading_sub, t)

    # Blockquote markers. Match horizontal whitespace only — `\s*` would
    # consume the preceding `\n` and collapse the paragraph break, joining
    # the blockquote into the prior paragraph as a single sentence.
    t = re.sub(r"(?m)^[ \t]*>[ \t]?", "", t)

    # Horizontal rules
    t = re.sub(r"(?m)^\s*---+\s*$", "", t)

    # List bullets: "- foo" / "* foo" / "1. foo" -> "foo"
    t = re.sub(r"(?m)^\s*[-*+]\s+", "", t)
    t = re.sub(r"(?m)^\s*\d+\.\s+", "", t)

    # Em-dash / en-dash handling. For espeak-backed engines (Kokoro), the
    # em-dash is unreliable as a pause cue — collapsed to a comma for
    # consistent micro-pauses. Neural engines (Chatterbox) handle em-dash
    # pacing natively and the V12 dramatic recipe relies on em-dashes for
    # rhythmic structure; converting to comma kills that structure and
    # forces a faster, more clipped delivery. Skip for chatterbox.
    if not source_only and not is_neural:
        t = t.replace(" — ", ", ").replace(" – ", ", ")
        t = t.replace("—", ", ").replace("–", ", ")

    # Smart-quote normalization. Espeak handles curly quotes inconsistently;
    # straight ASCII quotes are reliably ignored (they don't introduce
    # phantom pauses or mispronunciations). Apply before footnote-stripping
    # so any captured quoted footnote markers are normalized too.
    t = (t.replace("“", '"').replace("”", '"')   # " "
           .replace("‘", "'").replace("’", "'")   # ' '
           .replace("«", '"').replace("»", '"')   # « »
           .replace("„", '"').replace("‚", "'"))  # „ ‚

    # Ellipsis character normalization. Single-glyph "…" reads inconsistently;
    # three dots is what every other rule in this file expects.
    t = t.replace("…", "...")

    # Strip footnote-style reference markers before the acronym pass.
    # Markdown footnote refs `[^1]` and stray carets read as garbage in TTS.
    t = re.sub(r"\[\^[^\]]+\]", "", t)
    t = re.sub(r"\^", "", t)

    if not source_only:
        # Abbreviation expansion: i.e., e.g., etc., vs., cf., p.m./a.m., v1.0.
        # Run before the acronym pass so "i.e." in "the i.e. clarifier" expands
        # cleanly without acronym-style respelling overriding it.
        for pat, repl in ABBREVIATION_FIXES.items():
            t = re.sub(pat, repl, t)

        # Number-to-word expansion for narrative numbers. Espeak reads "10,000"
        # acceptably but reads "$10K" / "10K" / "100M" / "20%" inconsistently.
        # Normalize the most common patterns to plain English.
        t = _expand_numbers(t)

        # List-marker spoken cues. Markdown numbered lists ("1. foo / 2. bar")
        # were already stripped of leading "1." earlier, but inline ordinal
        # references in prose ("first..., second..., third...") are already
        # natural. The remaining work is enumerated parenthetical lists like
        # "(1) ... (2) ... (3)" which espeak reads as "left-paren one right-paren".
        t = re.sub(r"\((\d+)\)", lambda m: _ordinal_word(int(m.group(1))), t)

        # Acronym pre-processing for known-mangled terms. Espeak says
        # "krdt" for CRDT without dashes; Chatterbox handles acronyms
        # natively and the dashed form ("C-R-D-T") forces stilted
        # letter-by-letter pronunciation. Skip for neural engines.
        if not is_neural:
            for pat, repl in ACRONYM_FIXES.items():
                t = re.sub(pat, repl, t)

        # Proper-noun pronunciation lexicon. Espeak mispronounces foreign
        # names ("Tomás Ferreira" → "tomas ferrera"); the dashed
        # pronunciations ("toh-MAHS feh-RAY-rah") fix that. Chatterbox's
        # neural model handles foreign names natively from training data;
        # the dashed forms force unnatural letter-stress patterns. Skip
        # for neural engines.
        if not is_neural:
            for pat, repl in PROPER_NOUN_FIXES.items():
                t = re.sub(pat, repl, t)

    # Collapse soft newlines (single newlines inside a paragraph) into
    # spaces before guaranteeing terminal punctuation. Markdown soft-wraps
    # paragraphs at column 80; without this collapse, _ensure_period
    # incorrectly inserts periods at every wrap point, producing spurious
    # sentence breaks like "Reading those. verdicts was not...".
    # Paragraph breaks (\n\n) are preserved.
    t = re.sub(r"(?<!\n)\n(?!\n)", " ", t)

    # Guarantee terminal punctuation on every non-empty line so sentence
    # prosody doesn't run past headings and stripped list items.
    def _ensure_period(line: str) -> str:
        stripped = line.rstrip()
        if not stripped:
            return line
        if stripped[-1] in ".!?:,;":
            return line
        return stripped + "."

    t = "\n".join(_ensure_period(ln) for ln in t.splitlines())

    # Inline code `x` -> x (narrate literally)
    t = re.sub(r"`([^`]+)`", r"\1", t)

    # Bold/italic markers
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", t)
    t = re.sub(r"__([^_]+)__", r"\1", t)

    # Collapse whitespace
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)

    return t.strip()


_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])")


def chunk_sentences(text: str) -> list[str]:
    """Split into one chunk per sentence, preserving dot-only chunks
    (`...`, `....`, `......`) as pause markers — the render layer detects
    these via _is_pause_only() and emits silence MP3 instead of calling TTS.
    Used by --per-sentence synthesis. Speech chunks are small (~50-300
    chars typical), giving Kokoro fresh prosody on every utterance at the
    cost of more API calls."""
    chunks: list[str] = []
    for para in re.split(r"\n{2,}", text):
        para = para.strip()
        if not para:
            continue
        # Preserve dot-only paragraphs as pause markers.
        if _is_pause_only(para):
            chunks.append(para)
            continue
        for sent in _SENT_SPLIT.split(para):
            sent = sent.strip()
            if sent:
                chunks.append(sent)
    return chunks


def chunk_text_paired(tts_text: str, src_text: str,
                      budget: int = CHUNK_CHAR_BUDGET
                      ) -> tuple[list[str], list[str]]:
    """Chunk TTS text by char-budget while slicing source text identically.

    Both scripts share paragraph + sentence boundaries (structural transforms
    in narratable_text are deterministic; TTS-only token swaps don't shift
    paragraph splits). This walks both in lockstep, makes packing decisions
    against the TTS budget, and emits the matching source slice on every
    chunk boundary. Returns (tts_chunks, src_chunks) of equal length where
    src_chunks[i] is the source equivalent of tts_chunks[i].

    Used by render_chapter() to capture per-chunk source_text for EPUB Media
    Overlay XHTML matching, where TTS-rendered text diverges from the
    Pandoc-emitted source.
    """
    tts_paras = re.split(r"\n{2,}", tts_text)
    src_paras = re.split(r"\n{2,}", src_text)
    if len(tts_paras) != len(src_paras):
        raise ValueError(f"paragraph count mismatch: tts={len(tts_paras)} "
                         f"src={len(src_paras)} — narratable_text paragraph "
                         f"structure should be identical between TTS and source")

    tts_chunks: list[str] = []
    src_chunks: list[str] = []
    tts_buf = ""
    src_buf = ""

    def flush() -> None:
        nonlocal tts_buf, src_buf
        if tts_buf:
            tts_chunks.append(tts_buf.strip())
            src_chunks.append(src_buf.strip())
            tts_buf = ""
            src_buf = ""

    for tts_para, src_para in zip(tts_paras, src_paras):
        tts_para = tts_para.strip()
        src_para = src_para.strip()
        if not tts_para:
            continue
        if _is_pause_only(tts_para):
            flush()
            tts_chunks.append(tts_para)
            src_chunks.append(src_para)
            continue
        if len(tts_para) > budget:
            tts_sents = _SENT_SPLIT.split(tts_para)
            src_sents = _SENT_SPLIT.split(src_para)
            if len(tts_sents) != len(src_sents):
                # Sentence splits diverged — keep the whole paragraph as one
                # source slice and let multiple TTS sentence-chunks share it.
                src_sents = [src_para] * len(tts_sents)
            for tts_sent, src_sent in zip(tts_sents, src_sents):
                tts_sent = tts_sent.strip()
                src_sent = src_sent.strip()
                if not tts_sent:
                    continue
                if len(tts_buf) + len(tts_sent) + 1 > budget and tts_buf:
                    flush()
                # Pathological-sentence wrapping (TTS-only) collapses many
                # word-chunks into one source sentence: rare in practice.
                if len(tts_sent) > budget:
                    words = tts_sent.split()
                    cur = ""
                    for w in words:
                        if len(cur) + len(w) + 1 > budget and cur:
                            flush()
                            tts_chunks.append(cur.strip())
                            src_chunks.append(src_sent)
                            cur = ""
                        cur = (cur + " " + w).strip()
                    if cur:
                        tts_buf = (tts_buf + " " + cur).strip()
                        src_buf = (src_buf + " " + src_sent).strip()
                else:
                    tts_buf = (tts_buf + " " + tts_sent).strip()
                    src_buf = (src_buf + " " + src_sent).strip()
        else:
            if len(tts_buf) + len(tts_para) + 2 > budget and tts_buf:
                flush()
            tts_buf = (tts_buf + "\n\n" + tts_para).strip()
            src_buf = (src_buf + "\n\n" + src_para).strip()
    flush()
    return tts_chunks, src_chunks


def chunk_text(text: str, budget: int = CHUNK_CHAR_BUDGET) -> list[str]:
    """Split text into ~budget-sized chunks at paragraph and sentence boundaries.

    Dot-only paragraphs (pause markers) are preserved as standalone chunks
    so the render layer can emit explicit silence instead of sending them
    to Kokoro. This makes chunk and sentence modes produce the same pause
    structure — the only difference is speech-chunk granularity."""
    chunks: list[str] = []
    buf = ""
    for para in re.split(r"\n{2,}", text):
        para = para.strip()
        if not para:
            continue
        if _is_pause_only(para):
            # Pause marker — flush buffer, then append the marker on its own.
            if buf:
                chunks.append(buf.strip())
                buf = ""
            chunks.append(para)
            continue
        if len(para) > budget:
            # Split long paragraph by sentence
            for sent in _SENT_SPLIT.split(para):
                sent = sent.strip()
                if not sent:
                    continue
                if len(buf) + len(sent) + 1 > budget and buf:
                    chunks.append(buf.strip())
                    buf = ""
                if len(sent) > budget:
                    # Pathological sentence — hard-wrap on word boundaries
                    words = sent.split()
                    cur = ""
                    for w in words:
                        if len(cur) + len(w) + 1 > budget and cur:
                            if buf:
                                chunks.append(buf.strip())
                                buf = ""
                            chunks.append(cur.strip())
                            cur = ""
                        cur = (cur + " " + w).strip()
                    if cur:
                        buf = (buf + " " + cur).strip()
                else:
                    buf = (buf + " " + sent).strip()
        else:
            if len(buf) + len(para) + 2 > budget and buf:
                chunks.append(buf.strip())
                buf = ""
            buf = (buf + "\n\n" + para).strip()
    if buf:
        chunks.append(buf.strip())
    return chunks


def strip_id3v2(mp3: bytes) -> bytes:
    """Remove a leading ID3v2 tag from an MP3 byte string, if present."""
    if len(mp3) < 10 or mp3[:3] != b"ID3":
        return mp3
    # 4 sync-safe size bytes (7 bits each)
    b = mp3[6:10]
    size = (b[0] << 21) | (b[1] << 14) | (b[2] << 7) | b[3]
    return mp3[10 + size :]


SYNTH_HARD_CAP = 1200  # Kokoro prosody degrades past ~900 chars per call;
                       # 1200 is the safety net above CHUNK_CHAR_BUDGET's
                       # 1400 soft target for paragraph grouping.


def synth_chunk(client: OpenAI, voice: str, text: str, speed: float,
                model_name: str = "kokoro", retries: int = 3,
                exaggeration: float | None = None,
                cfg_weight: float | None = None,
                temperature: float | None = None) -> bytes:
    text = text[:SYNTH_HARD_CAP]
    last_err = None
    extra: dict = {}
    if speed and abs(speed - 1.0) > 1e-3:
        extra["speed"] = speed
    # V12 emotion knobs (Chatterbox); silently no-op for engines that
    # ignore unknown body fields (e.g. Kokoro). The wrapper validates
    # bounds — Mac side only forwards the values.
    if exaggeration is not None:
        extra["exaggeration"] = exaggeration
    if cfg_weight is not None:
        extra["cfg_weight"] = cfg_weight
    if temperature is not None:
        extra["temperature"] = temperature
    extra_body = extra or None
    for attempt in range(1, retries + 1):
        try:
            kwargs = dict(
                model=model_name,
                voice=voice,
                input=text,
                response_format="mp3",
            )
            if extra_body is not None:
                kwargs["extra_body"] = extra_body
            with client.audio.speech.with_streaming_response.create(**kwargs) as r:
                return r.read()
        except Exception as e:
            last_err = e
            wait = 2 ** (attempt - 1)
            print(f"      retry {attempt}/{retries} after error: {e!r} (sleep {wait}s)", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"{model_name} synth failed after {retries} retries: {last_err!r}")


def build_script(md_path: Path, engine: str = "kokoro") -> str:
    """Build the narration script from a chapter markdown file."""
    raw = md_path.read_text(encoding="utf-8")
    script = narratable_text(raw, engine=engine)
    # Chapter lead-in pause — gives listener a beat before the chapter title.
    script = "... \n\n" + script
    return script


def truncate_to_paragraphs(script: str, n: int) -> str:
    """Truncate a narration script to its first N body paragraphs.

    A "body paragraph" is any non-empty paragraph that is neither a
    pause-only marker (dot-only chunk) nor the chapter title (which is the
    first non-pause paragraph after the leading pause). Pause markers and
    the chapter title are preserved verbatim; this just bounds how much
    body content gets rendered.

    Used by --max-paragraphs for fast preset/voice iteration: render the
    first 3 body paragraphs of a chapter to <stem><suffix>.mp3 in ~30
    seconds to hear what a voice/speed combination sounds like before
    committing to a full ~30-minute chapter render.
    """
    paragraphs = re.split(r"\n{2,}", script)
    kept: list[str] = []
    body_count = 0
    title_seen = False
    for p in paragraphs:
        kept.append(p)
        s = p.strip()
        if not s:
            continue
        if _is_pause_only(s):
            continue
        if not title_seen:
            # First non-pause paragraph is the chapter title.
            title_seen = True
            continue
        body_count += 1
        if body_count >= n:
            break
    return "\n\n".join(kept)


def build_source_script(md_path: Path) -> str:
    """Source-text twin of build_script: same structural transforms, but no
    TTS-specific token swaps. Sentence boundaries match build_script() so the
    per-chunk source_text aligns 1:1 with the rendered chunks. Used by
    render_chapter() to capture the source sentence on each alignment entry
    for EPUB 3 Media Overlay fragment ID injection."""
    raw = md_path.read_text(encoding="utf-8")
    script = narratable_text(raw, source_only=True)
    script = "... \n\n" + script
    return script


def render_chapter(
    client: OpenAI,
    voice: str,
    speed: float,
    md_path: Path,
    out_path: Path,
    script_path: Path,
    per_sentence: bool = False,
    max_paragraphs: int | None = None,
    model_name: str = "kokoro",
    exaggeration: float | None = None,
    cfg_weight: float | None = None,
    temperature: float | None = None,
) -> dict:
    script = build_script(md_path, engine=model_name)
    source_script = build_source_script(md_path)
    if max_paragraphs is not None:
        script = truncate_to_paragraphs(script, max_paragraphs)
        source_script = truncate_to_paragraphs(source_script, max_paragraphs)
    script_path.parent.mkdir(parents=True, exist_ok=True)
    script_path.write_text(script, encoding="utf-8")

    # Chunk TTS + source in lockstep so source_text on each alignment entry
    # matches the Pandoc XHTML for EPUB Media Overlay fragment ID injection.
    # Engine-aware budget — see CHUNK_BUDGETS_BY_ENGINE for rationale.
    chunk_budget = CHUNK_BUDGETS_BY_ENGINE.get(model_name, CHUNK_CHAR_BUDGET)
    if per_sentence:
        chunks = chunk_sentences(script)
        source_chunks = chunk_sentences(source_script)
    else:
        chunks, source_chunks = chunk_text_paired(script, source_script,
                                                   budget=chunk_budget)
    total_chars = sum(len(c) for c in chunks)
    mode = "sentence" if per_sentence else "chunk"
    print(f"  {md_path.name}: {len(chunks)} {mode}s, {total_chars:,} chars")
    source_aligned = (len(source_chunks) == len(chunks))
    if not source_aligned:
        print(f"    note: source/rendered chunk counts diverge "
              f"({len(source_chunks)} vs {len(chunks)}); source_text=None for this chapter",
              file=sys.stderr)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    chapter_stem = md_path.stem
    alignment: list[dict] = []
    cumulative_seconds = 0.0
    t0 = time.time()
    with out_path.open("wb") as f:
        for i, chunk in enumerate(chunks, 1):
            dots = _is_pause_only(chunk)
            if dots >= 2:
                # Emit explicit silence instead of sending dots to the engine.
                # Default to the 6-dot duration if dot count exceeds the map.
                duration = PAUSE_DURATIONS.get(dots, PAUSE_DURATIONS[6])
                mp3 = silence_mp3(duration)
                tag = f"PAUSE {duration:.2f}s"
                is_pause = True
            else:
                mp3 = synth_chunk(client, voice, chunk, speed,
                                  model_name=model_name,
                                  exaggeration=exaggeration,
                                  cfg_weight=cfg_weight,
                                  temperature=temperature)
                tag = f"{len(chunk):4d} chars"
                is_pause = False
            if i > 1:
                mp3 = strip_id3v2(mp3)
            chunk_duration = _mp3_duration_seconds(mp3)
            chunk_id = f"{chapter_stem}-c{i:04d}"
            source_text = source_chunks[i - 1] if source_aligned else None
            alignment.append({
                "chunk_id": chunk_id,
                "chunk_index": i,
                "text": chunk,
                "source_text": source_text,
                "is_pause": is_pause,
                "start_seconds": round(cumulative_seconds, 3),
                "end_seconds": round(cumulative_seconds + chunk_duration, 3),
                "duration_seconds": round(chunk_duration, 3),
            })
            cumulative_seconds += chunk_duration
            f.write(mp3)
            pct = 100 * i / len(chunks)
            elapsed = time.time() - t0
            print(f"    [{i:3d}/{len(chunks)}] {pct:5.1f}%  {tag:14s}  {elapsed:6.1f}s", flush=True)

    # Emit per-chapter alignment for EPUB 3 Media Overlays generation
    ALIGNMENTS_DIR.mkdir(parents=True, exist_ok=True)
    alignment_path = ALIGNMENTS_DIR / f"{chapter_stem}.json"
    alignment_path.write_text(json.dumps({
        "chapter_stem": chapter_stem,
        "source": str(md_path.relative_to(REPO).as_posix()),
        "audio": str(out_path.relative_to(REPO).as_posix()),
        "total_seconds": round(cumulative_seconds, 3),
        "chunks": alignment,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    return {
        "source": str(md_path.relative_to(REPO).as_posix()),
        "output": str(out_path.relative_to(REPO).as_posix()),
        "script": str(script_path.relative_to(REPO).as_posix()),
        "alignment": str(alignment_path.relative_to(REPO).as_posix()),
        "chunks": len(chunks),
        "chars": total_chars,
        "bytes": out_path.stat().st_size,
        "seconds": round(time.time() - t0, 1),
        "audio_seconds": round(cumulative_seconds, 3),
    }


def out_name_for(src_rel: str) -> str:
    stem = Path(src_rel).stem
    return f"{stem}.mp3"


def main() -> None:
    # Build the help epilog from whichever engine the user is asking about,
    # falling back to Kokoro for the no-args case.
    epilog = "Engines:\n  " + "\n  ".join(
        f"{name:<8} {cfg['description']}" for name, cfg in ENGINES.items()
    )
    epilog += "\n\nKokoro presets:\n  " + "\n  ".join(
        f"{name:<14} voice={cfg['voice']:<28} speed={cfg['speed']}"
        for name, cfg in PRESETS_KOKORO.items()
    )
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog,
    )
    ap.add_argument("--engine", choices=list(ENGINES.keys()), default="kokoro",
                    help="TTS backend (default: kokoro). 'chatterbox' targets the Chatterbox "
                         "(Resemble AI) server on the Windows GPU box; expects the same "
                         "OpenAI-compatible API and a Bearer token via TTS_API_KEY env "
                         "var (or --api-key). Override the per-engine default base URL "
                         "with --base-url.")
    ap.add_argument("--preset", default="male",
                    help="default voice preset. Default: male (Kokoro: am_michael+am_fenrir "
                         "blend at 0.92 — less stylized than sinek, better for straight "
                         "technical non-fiction across Parts I/III/IV). Part II chapters "
                         "and ch10/preface override via CHAPTER_PRESET_MAP unless "
                         "--no-chapter-map is set. Preset KEYS are shared across engines; "
                         "the actual voice ID resolves through the engine's preset catalog.")
    ap.add_argument("--no-chapter-map", action="store_true",
                    help="disable per-chapter preset overrides (use --preset for all)")
    ap.add_argument("--voice", default=None,
                    help="explicit voice ID (engine-native; Kokoro supports + blends). Overrides --preset.")
    ap.add_argument("--speed", type=float, default=None,
                    help="TTS speed multiplier (0.5-2.0). Overrides --preset.")
    ap.add_argument("--base-url", default=None,
                    help="HTTP base URL for the engine API (default: per-engine default — "
                         "Kokoro localhost:8880, Chatterbox desktop-umt08rn:8881). "
                         "Override for remote GPU server, Tailscale FQDN, or stage-vs-prod "
                         "swaps.")
    ap.add_argument("--api-key", default=None,
                    help="Bearer token for engines that require auth. Default: read from "
                         "the TTS_API_KEY env var. Required for --engine chatterbox; "
                         "ignored for engines whose requires_auth=False.")
    ap.add_argument("--exaggeration", type=float, default=None,
                    help="Emotion intensity (Chatterbox V12+ only; ignored by Kokoro). "
                         "Model default ~0.5 used when omitted. 0.7+ for narrative-driven "
                         "chapters; pair with --cfg-weight 0.3 for the documented "
                         "dramatic-narrator recipe.")
    ap.add_argument("--cfg-weight", type=float, default=None,
                    help="Classifier-free guidance weight (Chatterbox V12+ only). "
                         "Model default ~0.5 used when omitted. Lower (0.3) = slower, "
                         "more deliberate pacing; pairs with --exaggeration 0.7+.")
    ap.add_argument("--temperature", type=float, default=None,
                    help="Sampling temperature (Chatterbox V12+ only). Model default "
                         "(~0.8) used when omitted. Lower (0.5) for reproducibility "
                         "across re-renders.")
    ap.add_argument("--only", help="render only chapters whose source name contains this string (e.g. 'ch05')")
    ap.add_argument("--force", action="store_true", help="re-render even if an MP3 already exists")
    ap.add_argument("--dry-run", action="store_true", help="print chunk counts only")
    ap.add_argument("--scripts-only", action="store_true",
                    help="regenerate narration scripts from markdown without calling TTS")
    ap.add_argument("--list-presets", action="store_true", help="print presets and exit")
    ap.add_argument("--per-sentence", action="store_true",
                    help="render one sentence per Kokoro call (cleaner prosody, "
                         "~3-5x more API calls and total time). Default: off.")
    ap.add_argument("--max-paragraphs", type=int, default=None,
                    help="render only the first N body paragraphs of each chapter "
                         "(after the chapter title). Used with --output-suffix for "
                         "fast voice/preset iteration — typically 3-5 paragraphs "
                         "renders in ~30s and produces ~30-60s of audio.")
    ap.add_argument("--output-suffix", default="",
                    help="append this suffix to the output MP3 stem (e.g. '_sample'). "
                         "Use with --max-paragraphs to avoid overwriting full-chapter "
                         "renders during voice/preset iteration. Default: empty.")
    args = ap.parse_args()

    engine = ENGINES[args.engine]
    presets = engine["presets"]
    base_url = args.base_url or engine["default_base_url"]
    model_name = engine["model_name"]

    if args.list_presets:
        for name, cfg in presets.items():
            voice_str = cfg["voice"] if cfg["voice"] is not None else "(unset — TODO)"
            print(f"{name:<14} voice={voice_str:<28} speed={cfg['speed']}")
        sys.exit(0)

    if args.preset not in presets:
        print(f"--preset {args.preset!r} not in --engine {args.engine!r} catalog. "
              f"Available: {sorted(presets.keys())}", file=sys.stderr)
        sys.exit(2)

    def resolve_preset(rel_path: str) -> tuple[str, str, float]:
        """Return (preset_name, voice, speed) for a chapter."""
        name = args.preset
        if not args.no_chapter_map and not args.voice:
            for key, preset_name in CHAPTER_PRESET_MAP.items():
                if key in rel_path:
                    name = preset_name
                    break
        if name not in presets:
            raise RuntimeError(
                f"Chapter map resolved to preset {name!r} but engine "
                f"{args.engine!r} has no such preset. Add it to "
                f"PRESETS_{args.engine.upper()} or pass --no-chapter-map."
            )
        cfg = presets[name]
        v = args.voice or cfg["voice"]
        if v is None:
            raise RuntimeError(
                f"Engine {args.engine!r} preset {name!r} has voice=None — "
                f"the catalog entry hasn't been filled in yet. Either set "
                f"PRESETS_{args.engine.upper()}[{name!r}]['voice'] to a real "
                f"voice ID (query GET {base_url}/audio/voices to list "
                f"available voices) or pass --voice <id> explicitly."
            )
        s = args.speed if args.speed is not None else cfg["speed"]
        return name, v, s

    print(f"Engine: {args.engine} ({engine['description']})")
    print(f"  base_url: {base_url}")
    print(f"  model:    {model_name}")
    print(f"Default preset: {args.preset}  chapter-map: {'off' if args.no_chapter_map else 'on'}")

    if engine.get("requires_auth"):
        api_key = args.api_key or os.environ.get("TTS_API_KEY")
        if not api_key:
            print(
                f"Engine {args.engine!r} requires auth. Set the TTS_API_KEY env "
                f"var or pass --api-key <token>. The token is the same Bearer "
                f"value the Windows server uses for /v1/audio/speech.",
                file=sys.stderr,
            )
            sys.exit(2)
    else:
        api_key = "not-needed"

    client = OpenAI(base_url=base_url, api_key=api_key)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT_DIR / "manifest.json"
    manifest: dict = {"default_preset": args.preset, "chapter_map_on": not args.no_chapter_map, "chapters": []}
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["default_preset"] = args.preset
            manifest["chapter_map_on"] = not args.no_chapter_map
        except json.JSONDecodeError:
            pass

    # Index existing entries by source so we can update in place
    by_source = {c["source"]: c for c in manifest.get("chapters", [])}

    targets = CHAPTER_FILES
    if args.only:
        targets = [p for p in CHAPTER_FILES if args.only in p]
        if not targets:
            print(f"No chapters matched --only={args.only!r}", file=sys.stderr)
            sys.exit(2)

    t_all = time.time()
    for rel in targets:
        md_path = CHAPTERS_DIR / rel
        if not md_path.exists():
            print(f"SKIP missing: {rel}", file=sys.stderr)
            continue
        suffix = args.output_suffix
        out_stem = Path(rel).stem + suffix
        out_path = OUT_DIR / f"{out_stem}.mp3"

        script_path = SCRIPTS_DIR / (out_stem + ".txt")

        if args.dry_run:
            script = build_script(md_path, engine=args.engine)
            chunks = chunk_sentences(script) if args.per_sentence else chunk_text(script)
            mode = "sentence" if args.per_sentence else "chunk"
            print(f"{rel}: {len(chunks)} {mode}s, {sum(len(c) for c in chunks):,} chars")
            continue

        if args.scripts_only:
            script = build_script(md_path, engine=args.engine)
            script_path.parent.mkdir(parents=True, exist_ok=True)
            script_path.write_text(script, encoding="utf-8")
            print(f"  wrote {script_path.relative_to(REPO).as_posix()} ({len(script):,} chars)")
            continue

        if out_path.exists() and not args.force:
            print(f"SKIP existing: {out_path.relative_to(REPO).as_posix()} (use --force to re-render)")
            continue

        preset_name, voice, speed = resolve_preset(rel)
        mode_tag = " per-sentence" if args.per_sentence else ""
        if args.max_paragraphs is not None:
            mode_tag += f" max-paragraphs={args.max_paragraphs}"
        print(f"\n=> {rel}  [preset={preset_name} voice={voice} speed={speed}{mode_tag}]")
        entry = render_chapter(client, voice, speed, md_path, out_path, script_path,
                               per_sentence=args.per_sentence,
                               max_paragraphs=args.max_paragraphs,
                               model_name=model_name,
                               exaggeration=args.exaggeration,
                               cfg_weight=args.cfg_weight,
                               temperature=args.temperature)
        entry["engine"] = args.engine
        entry["preset"] = preset_name
        entry["voice"] = voice
        entry["speed"] = speed
        entry["mode"] = "sentence" if args.per_sentence else "chunk"
        if args.exaggeration is not None:
            entry["exaggeration"] = args.exaggeration
        if args.cfg_weight is not None:
            entry["cfg_weight"] = args.cfg_weight
        if args.temperature is not None:
            entry["temperature"] = args.temperature
        by_source[entry["source"]] = entry
        manifest["chapters"] = [by_source[s] for s in [c["source"] for c in manifest.get("chapters", [])] + [entry["source"]] if s in by_source]
        # deduplicate preserving first-seen order
        seen = set()
        dedup = []
        for c in manifest["chapters"]:
            if c["source"] not in seen:
                dedup.append(c)
                seen.add(c["source"])
        manifest["chapters"] = dedup
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    if not args.dry_run:
        print(f"\nTotal wall time: {time.time() - t_all:.1f}s")
        print(f"Manifest: {manifest_path.relative_to(REPO).as_posix()}")


if __name__ == "__main__":
    main()
