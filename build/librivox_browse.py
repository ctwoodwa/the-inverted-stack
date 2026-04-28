"""Browse LibriVox for usable narrator reference clips.

LibriVox audio is public domain (CC0). The API at
https://librivox.org/api/feed/audiobooks/ returns book metadata plus
per-section MP3 URLs hosted on archive.org. Archive.org supports HTTP
range requests, so ffmpeg can pull a 30-sec slice without downloading
the full ~14 MB chapter.

Workflow:
    # Browse solo audiobooks in a language
    python build/librivox_browse.py search --language English --solo-only --limit 30

    # See sections + readers for a candidate book
    python build/librivox_browse.py sections --book 47

    # Preview a 30-sec window from a section (writes to /tmp; tells you
    # the path to play yourself — this script can't open Audio.app for you)
    python build/librivox_browse.py preview --book 47 --section 1 \\
      --start 1:30 --length 30

    # Extract a clean reference clip ready for upload to Chatterbox
    python build/librivox_browse.py extract --book 47 --section 1 \\
      --start 2:00 --length 28 --out references/voss-30s.wav

Per-clip best practice:
    - Pick a section >= 30 sec into the chapter (skip the LibriVox boilerplate
      intro: "Section <N> of <book> by <author>, read by <reader> for LibriVox").
    - Skip the closing boilerplate too ("End of section <N>").
    - Aim for 20-30 sec of clean reading. Chatterbox cloning quality plateaus
      around there.
    - WAV mono 24 kHz is the safe upload format (matches Chatterbox internals).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import httpx

LIBRIVOX_API = "https://librivox.org/api/feed/audiobooks"
DEFAULT_TIMEOUT = 30.0


def _ffmpeg_exe() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def _parse_timecode(s: str) -> float:
    """Accept '90', '1:30', '1:30.5', '1:02:30' and return seconds (float)."""
    parts = s.strip().split(":")
    if len(parts) == 1:
        return float(parts[0])
    if len(parts) == 2:
        m, sec = parts
        return int(m) * 60 + float(sec)
    if len(parts) == 3:
        h, m, sec = parts
        return int(h) * 3600 + int(m) * 60 + float(sec)
    raise ValueError(f"timecode {s!r} not in [SS|MM:SS|HH:MM:SS] form")


def _fmt_seconds(total: int) -> str:
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def _fetch_books(*, language: str | None = None, title: str | None = None,
                 author: str | None = None, reader: str | None = None,
                 limit: int = 30, offset: int = 0,
                 extended: bool = True) -> list[dict[str, Any]]:
    params: dict[str, Any] = {
        "format": "json",
        "limit": limit,
        "offset": offset,
        "extended": 1 if extended else 0,
    }
    if language:
        params["language"] = language
    if title:
        params["title"] = title
    if author:
        params["author"] = author
    if reader:
        params["reader"] = reader
    r = httpx.get(LIBRIVOX_API, params=params, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    data = r.json()
    return data.get("books", []) or []


def _fetch_book(book_id: str) -> dict[str, Any]:
    books = _fetch_books(extended=True, limit=1)  # placeholder for shape
    # the feed endpoint accepts ?id= as well
    params = {"format": "json", "extended": 1, "id": book_id}
    r = httpx.get(LIBRIVOX_API, params=params, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    books = r.json().get("books", []) or []
    if not books:
        raise RuntimeError(f"no book with id={book_id} on LibriVox")
    return books[0]


def _is_solo(book: dict[str, Any]) -> bool:
    """A book is solo iff every section has exactly one reader and they all match."""
    seen: set[str] = set()
    for sec in book.get("sections", []) or []:
        readers = sec.get("readers") or []
        if len(readers) != 1:
            return False
        seen.add(readers[0].get("reader_id", ""))
    return len(seen) == 1


def _solo_reader(book: dict[str, Any]) -> str | None:
    if not _is_solo(book):
        return None
    secs = book.get("sections", []) or []
    if not secs:
        return None
    r = secs[0]["readers"][0]
    return f'{r.get("display_name","?")} (id={r.get("reader_id","?")})'


def _format_book_row(book: dict[str, Any]) -> str:
    book_id = book.get("id", "?")
    title = (book.get("title") or "")[:60]
    author = ""
    auths = book.get("authors") or []
    if auths:
        a = auths[0]
        author = f'{a.get("first_name","")} {a.get("last_name","")}'.strip()
    nsec = book.get("num_sections", "?")
    total = book.get("totaltime", "?")
    reader = _solo_reader(book) or "(multi-reader)"
    return f"  [{book_id:>6}]  {title:<60} {author:<28} sections={nsec:<4} {total:<10}  reader={reader}"


# --- subcommands -----------------------------------------------------------

def _cmd_search(args: argparse.Namespace) -> int:
    books = _fetch_books(language=args.language, title=args.title,
                         author=args.author, reader=args.reader,
                         limit=args.limit, offset=args.offset, extended=True)
    if args.solo_only:
        books = [b for b in books if _is_solo(b)]
    if args.json:
        print(json.dumps({"books": books}, indent=2))
        return 0
    if not books:
        print("(no matches)")
        return 0
    print(f"{len(books)} book(s):")
    for b in books:
        print(_format_book_row(b))
    return 0


def _cmd_sections(args: argparse.Namespace) -> int:
    book = _fetch_book(args.book)
    title = book.get("title", "?")
    auths = book.get("authors") or []
    author = " / ".join(
        f'{a.get("first_name","")} {a.get("last_name","")}'.strip()
        for a in auths
    )
    print(f"Book {args.book}: {title}")
    if author:
        print(f"  by {author}")
    print(f"  sections: {book.get('num_sections','?')}, total: {book.get('totaltime','?')}")
    print(f"  url: {book.get('url_librivox','')}")
    print()
    secs = book.get("sections", []) or []
    if args.json:
        print(json.dumps({"sections": secs}, indent=2))
        return 0
    for sec in secs:
        n = sec.get("section_number", "?")
        t = sec.get("title", "")[:50]
        playtime = int(sec.get("playtime") or 0)
        readers = sec.get("readers") or []
        rdr = readers[0].get("display_name", "?") if readers else "?"
        rdr_id = readers[0].get("reader_id", "?") if readers else "?"
        print(f"  [{n:>3}] {t:<52} {_fmt_seconds(playtime):<10} {rdr} (id={rdr_id})")
    return 0


def _section_url(book: dict[str, Any], section_num: int) -> tuple[str, dict[str, Any]]:
    for sec in book.get("sections", []) or []:
        if int(sec.get("section_number", -1)) == section_num:
            return sec["listen_url"], sec
    raise RuntimeError(
        f"section {section_num} not found in book {book.get('id','?')} "
        f"({book.get('num_sections','?')} sections total)"
    )


def _ffmpeg_extract(url: str, out_path: Path, *, start_sec: float,
                    length_sec: float, sample_rate: int = 24000,
                    mono: bool = True) -> None:
    """Stream-extract a window from a remote MP3 to a local file.

    Output format inferred from out_path suffix. WAV defaults to PCM s16le
    mono at sample_rate; MP3 keeps the source bitrate via -c copy when
    possible (faster, no re-encode).
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = _ffmpeg_exe()
    suffix = out_path.suffix.lower()

    # -ss BEFORE -i = seek by HTTP range when the source supports it
    # (archive.org does). Saves bandwidth — ~250 KB instead of ~14 MB.
    cmd = [
        ffmpeg, "-hide_banner", "-loglevel", "warning", "-y",
        "-ss", f"{start_sec:.3f}",
        "-i", url,
        "-t", f"{length_sec:.3f}",
    ]
    if suffix == ".wav":
        cmd += ["-ac", "1" if mono else "2", "-ar", str(sample_rate),
                "-c:a", "pcm_s16le"]
    elif suffix == ".mp3":
        cmd += ["-c:a", "copy"]
    elif suffix == ".flac":
        cmd += ["-ac", "1" if mono else "2", "-ar", str(sample_rate),
                "-c:a", "flac"]
    else:
        raise RuntimeError(f"unsupported output extension {suffix!r}; "
                           f"use .wav / .mp3 / .flac")
    cmd.append(str(out_path))

    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        raise RuntimeError(
            f"ffmpeg failed (exit {proc.returncode}):\n"
            f"  cmd: {' '.join(cmd)}\n"
            f"  stderr: {proc.stderr.strip()[:500]}"
        )


def _cmd_preview(args: argparse.Namespace) -> int:
    book = _fetch_book(args.book)
    url, sec = _section_url(book, args.section)
    start_sec = _parse_timecode(args.start)
    out = Path(args.out) if args.out else Path("/tmp") / (
        f"librivox_book{args.book}_sec{args.section}"
        f"_{int(start_sec)}s_{args.length}s.mp3"
    )
    _ffmpeg_extract(url, out, start_sec=start_sec, length_sec=float(args.length))
    size = out.stat().st_size
    print(f"wrote {out} ({size:,} bytes)")
    print(f"  source: {url}")
    print(f"  reader: {(sec.get('readers') or [{}])[0].get('display_name','?')}")
    print(f"  open with: open '{out}'   (or afplay '{out}')")
    return 0


def _cmd_extract(args: argparse.Namespace) -> int:
    book = _fetch_book(args.book)
    url, sec = _section_url(book, args.section)
    start_sec = _parse_timecode(args.start)
    out = Path(args.out)
    _ffmpeg_extract(url, out, start_sec=start_sec, length_sec=float(args.length),
                    sample_rate=args.sample_rate, mono=not args.stereo)
    size = out.stat().st_size
    print(f"wrote {out} ({size:,} bytes)")
    print(f"  source: {url}")
    rdr = (sec.get("readers") or [{}])[0]
    print(f"  reader: {rdr.get('display_name','?')} (id={rdr.get('reader_id','?')})")
    print(f"  next: python3 build/voice_upload.py put <voice_id> "
          f"--audio {out} --transcript '<exact text spoken in clip>'")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Sift LibriVox for narrator reference clips.",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_search = sub.add_parser("search", help="search audiobooks")
    p_search.add_argument("--language", default=None,
                          help="e.g. English, Russian, Portuguese (case-sensitive on the API)")
    p_search.add_argument("--title", default=None, help="title substring")
    p_search.add_argument("--author", default=None, help="author id or name")
    p_search.add_argument("--reader", default=None,
                          help="LibriVox reader_id (find via https://librivox.org/reader/<id>)")
    p_search.add_argument("--solo-only", action="store_true",
                          help="restrict to single-reader books (best for cloning)")
    p_search.add_argument("--limit", type=int, default=30)
    p_search.add_argument("--offset", type=int, default=0)
    p_search.add_argument("--json", action="store_true")
    p_search.set_defaults(func=_cmd_search)

    p_secs = sub.add_parser("sections", help="list sections of a book")
    p_secs.add_argument("--book", required=True, help="LibriVox book id")
    p_secs.add_argument("--json", action="store_true")
    p_secs.set_defaults(func=_cmd_sections)

    p_prev = sub.add_parser("preview", help="extract a clip to /tmp for listening")
    p_prev.add_argument("--book", required=True)
    p_prev.add_argument("--section", type=int, required=True)
    p_prev.add_argument("--start", default="1:00",
                        help="start timecode SS / MM:SS / HH:MM:SS (default 1:00 — skip boilerplate intro)")
    p_prev.add_argument("--length", type=int, default=30,
                        help="clip length in seconds (default 30)")
    p_prev.add_argument("--out", default=None, help="output path (default: /tmp/...)")
    p_prev.set_defaults(func=_cmd_preview)

    p_ext = sub.add_parser("extract", help="extract a clean reference clip for upload")
    p_ext.add_argument("--book", required=True)
    p_ext.add_argument("--section", type=int, required=True)
    p_ext.add_argument("--start", default="1:00",
                       help="start timecode SS / MM:SS / HH:MM:SS")
    p_ext.add_argument("--length", type=int, default=28,
                       help="clip length in seconds (default 28 — Chatterbox sweet spot)")
    p_ext.add_argument("--out", required=True,
                       help="output path; .wav / .mp3 / .flac inferred from suffix")
    p_ext.add_argument("--sample-rate", type=int, default=24000,
                       help="target sample rate for WAV/FLAC (default 24000 — Chatterbox native)")
    p_ext.add_argument("--stereo", action="store_true",
                       help="keep stereo (default mono — Chatterbox doesn't use stereo)")
    p_ext.set_defaults(func=_cmd_extract)

    return ap


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        return args.func(args)
    except httpx.HTTPStatusError as e:
        print(f"librivox API returned {e.response.status_code}", file=sys.stderr)
        return 1
    except httpx.RequestError as e:
        print(f"network error: {e}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
