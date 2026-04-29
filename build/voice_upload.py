"""Mac-side client for the Chatterbox voice-upload API.

The Windows TTS server exposes (per the spec at
docs/audio/CHATTERBOX-VOICE-API.md):

    PUT    /v1/audio/voices/{voice_id}   multipart upload
    GET    /v1/audio/voices              list (already existed)
    GET    /v1/audio/voices/{voice_id}   one voice
    DELETE /v1/audio/voices/{voice_id}   remove

This module wraps those four operations as both importable functions
and a CLI. Auth is `Authorization: Bearer $TTS_API_KEY`.

Usage (CLI):
    # List voices
    python build/voice_upload.py list

    # Inspect one
    python build/voice_upload.py get voss

    # Upload (or replace)
    python build/voice_upload.py put voss \\
      --audio references/voss-30s.wav \\
      --transcript "Procurement isn't where compliance lives — it's where it dies." \\
      --display-name "Council member — Voss (enterprise lens)" \\
      --language en-US

    # Delete
    python build/voice_upload.py delete voss

Usage (importable):
    from build.voice_upload import put_voice
    put_voice("voss", "references/voss-30s.wav", "Procurement…", language="en-US")
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import httpx

DEFAULT_BASE_URL = "http://desktop-umt08rn:8881/v1"
SLUG_RE = re.compile(r"^[a-z0-9_-]{1,64}$")
ALLOWED_AUDIO_EXTS = {".wav", ".mp3", ".flac"}
MAX_AUDIO_BYTES = 10 * 1024 * 1024  # 10 MB
MIN_TRANSCRIPT_CHARS = 8


class VoiceUploadError(RuntimeError):
    """Raised for client-side validation failures and server errors."""


def _resolve_base_url(base_url: str | None) -> str:
    return base_url or os.environ.get("CHATTERBOX_URL") or DEFAULT_BASE_URL


def _resolve_api_key(api_key: str | None) -> str:
    key = api_key or os.environ.get("TTS_API_KEY")
    if not key:
        raise VoiceUploadError(
            "TTS_API_KEY not set. Export it (export TTS_API_KEY=…) or pass "
            "--api-key on the CLI."
        )
    return key


def _headers(api_key: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {api_key}"}


def _validate_voice_id(voice_id: str) -> None:
    if not SLUG_RE.match(voice_id):
        raise VoiceUploadError(
            f"voice_id {voice_id!r} invalid. Must match {SLUG_RE.pattern} "
            f"(lowercase alphanumeric, hyphen, underscore; 1-64 chars)."
        )


def _validate_audio(path: Path) -> None:
    if not path.exists():
        raise VoiceUploadError(f"audio file not found: {path}")
    if path.suffix.lower() not in ALLOWED_AUDIO_EXTS:
        raise VoiceUploadError(
            f"audio extension {path.suffix!r} not in "
            f"{sorted(ALLOWED_AUDIO_EXTS)}"
        )
    size = path.stat().st_size
    if size > MAX_AUDIO_BYTES:
        raise VoiceUploadError(
            f"audio file too large: {size:,} bytes > {MAX_AUDIO_BYTES:,} "
            f"({path.name})"
        )
    if size == 0:
        raise VoiceUploadError(f"audio file is empty: {path}")


def list_voices(*, base_url: str | None = None, api_key: str | None = None,
                refresh: bool = False) -> list[dict[str, Any]]:
    """GET /v1/audio/voices — return the parsed `voices` list."""
    url = f"{_resolve_base_url(base_url)}/audio/voices"
    params = {"refresh": 1} if refresh else {}
    r = httpx.get(url, headers=_headers(_resolve_api_key(api_key)),
                  params=params, timeout=30.0)
    r.raise_for_status()
    return r.json().get("voices", [])


def get_voice(voice_id: str, *, base_url: str | None = None,
              api_key: str | None = None) -> dict[str, Any]:
    """GET /v1/audio/voices/{voice_id}."""
    _validate_voice_id(voice_id)
    url = f"{_resolve_base_url(base_url)}/audio/voices/{voice_id}"
    r = httpx.get(url, headers=_headers(_resolve_api_key(api_key)),
                  timeout=30.0)
    r.raise_for_status()
    return r.json()


def put_voice(voice_id: str, audio_path: str | Path, transcript: str, *,
              display_name: str | None = None, language: str | None = None,
              notes: str | None = None, base_url: str | None = None,
              api_key: str | None = None) -> dict[str, Any]:
    """PUT /v1/audio/voices/{voice_id} — create or replace.

    Returns the server's response (id, transcript, sample_rate, etc.).
    Raises VoiceUploadError for client-side validation failures and
    httpx.HTTPStatusError for server-side errors (the response body is
    in `.response.text` on the exception).
    """
    _validate_voice_id(voice_id)
    audio_path = Path(audio_path)
    _validate_audio(audio_path)
    transcript = transcript.strip()
    if len(transcript) < MIN_TRANSCRIPT_CHARS:
        raise VoiceUploadError(
            f"transcript too short ({len(transcript)} chars; min "
            f"{MIN_TRANSCRIPT_CHARS}). Chatterbox uses the transcript "
            f"for cloning fidelity — don't skip it."
        )

    url = f"{_resolve_base_url(base_url)}/audio/voices/{voice_id}"
    fields: dict[str, str] = {"transcript": transcript}
    if display_name:
        fields["display_name"] = display_name
    if language:
        fields["language"] = language
    if notes:
        fields["notes"] = notes

    with audio_path.open("rb") as f:
        files = {"audio": (audio_path.name, f, _audio_mime(audio_path))}
        r = httpx.put(url, headers=_headers(_resolve_api_key(api_key)),
                      data=fields, files=files, timeout=120.0)
    r.raise_for_status()
    return r.json()


def delete_voice(voice_id: str, *, base_url: str | None = None,
                 api_key: str | None = None) -> None:
    """DELETE /v1/audio/voices/{voice_id}. Raises on 4xx/5xx."""
    _validate_voice_id(voice_id)
    url = f"{_resolve_base_url(base_url)}/audio/voices/{voice_id}"
    r = httpx.delete(url, headers=_headers(_resolve_api_key(api_key)),
                     timeout=30.0)
    r.raise_for_status()


def _audio_mime(path: Path) -> str:
    return {
        ".wav": "audio/wav",
        ".mp3": "audio/mpeg",
        ".flac": "audio/flac",
    }[path.suffix.lower()]


# --- CLI -------------------------------------------------------------------

def _cmd_list(args: argparse.Namespace) -> int:
    voices = list_voices(base_url=args.base_url, api_key=args.api_key,
                         refresh=args.refresh)
    if args.json:
        print(json.dumps({"voices": voices}, indent=2))
        return 0
    if not voices:
        print("(no voices registered)")
        return 0
    name_w = max(len(v.get("id", "")) for v in voices)
    for v in voices:
        sr = v.get("sample_rate", "?")
        excerpt = (v.get("transcript", "") or "").replace("\n", " ")
        if len(excerpt) > 60:
            excerpt = excerpt[:57] + "…"
        print(f"  {v.get('id', ''):<{name_w}}  sr={sr}  {excerpt}")
    return 0


def _cmd_get(args: argparse.Namespace) -> int:
    info = get_voice(args.voice_id, base_url=args.base_url, api_key=args.api_key)
    print(json.dumps(info, indent=2))
    return 0


def _cmd_put(args: argparse.Namespace) -> int:
    transcript = args.transcript
    if args.transcript_file:
        transcript = Path(args.transcript_file).read_text(encoding="utf-8").strip()
    if not transcript:
        print("--transcript or --transcript-file required", file=sys.stderr)
        return 2
    info = put_voice(
        args.voice_id, args.audio, transcript,
        display_name=args.display_name, language=args.language,
        notes=args.notes, base_url=args.base_url, api_key=args.api_key,
    )
    print(json.dumps(info, indent=2))
    return 0


def _cmd_delete(args: argparse.Namespace) -> int:
    delete_voice(args.voice_id, base_url=args.base_url, api_key=args.api_key)
    print(f"deleted voice: {args.voice_id}")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Manage Chatterbox voice catalog (list / get / put / delete).",
    )
    ap.add_argument("--base-url", default=None,
                    help=f"server base URL (default: $CHATTERBOX_URL or {DEFAULT_BASE_URL})")
    ap.add_argument("--api-key", default=None,
                    help="Bearer token (default: $TTS_API_KEY)")

    sub = ap.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="list registered voices")
    p_list.add_argument("--refresh", action="store_true",
                        help="force server-side cache invalidation (?refresh=1)")
    p_list.add_argument("--json", action="store_true",
                        help="emit raw JSON instead of a table")
    p_list.set_defaults(func=_cmd_list)

    p_get = sub.add_parser("get", help="fetch one voice's metadata")
    p_get.add_argument("voice_id")
    p_get.set_defaults(func=_cmd_get)

    p_put = sub.add_parser("put", help="upload (create or replace) a voice")
    p_put.add_argument("voice_id")
    p_put.add_argument("--audio", required=True, help="path to reference clip (wav/mp3/flac)")
    p_put.add_argument("--transcript", default=None,
                       help="exact text spoken in the clip (use --transcript-file for long ones)")
    p_put.add_argument("--transcript-file", default=None,
                       help="read transcript from a UTF-8 text file")
    p_put.add_argument("--display-name", default=None,
                       help="human-friendly label, e.g. 'Council member — Voss'")
    p_put.add_argument("--language", default=None, help="BCP-47 tag (en-US, ru, pt-BR, …)")
    p_put.add_argument("--notes", default=None,
                       help="free-text provenance, e.g. 'recorded 2026-04-28, SM7B'")
    p_put.set_defaults(func=_cmd_put)

    p_del = sub.add_parser("delete", help="remove a voice")
    p_del.add_argument("voice_id")
    p_del.set_defaults(func=_cmd_delete)

    return ap


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        return args.func(args)
    except VoiceUploadError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except httpx.HTTPStatusError as e:
        body = (e.response.text or "")[:400]
        print(f"server returned {e.response.status_code}: {body}", file=sys.stderr)
        return 1
    except httpx.RequestError as e:
        print(f"network error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
