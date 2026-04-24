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
import re
import sys
import time
from pathlib import Path

from openai import OpenAI

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
}

# Named voice + speed presets. --preset selects one; --voice/--speed override.
# Rationale for each is documented in the audiobook research notes.
PRESETS: dict[str, dict] = {
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

# Per-chapter preset overrides. Key is matched as a substring against the
# source path. Part II council chapters each get a distinct voice so the
# "different expert per chapter" conceit is audible. Ch10 returns to the
# main narrator because it's the book's synthesis of the council's output.
CHAPTER_PRESET_MAP: dict[str, str] = {
    "ch05-enterprise-lens":                "fenrir",       # corporate confident
    "ch06-distributed-systems-lens":       "fry",          # British academic
    "ch07-security-lens":                  "british-male", # analytical, dry
    "ch08-product-economic-lens":          "female-solo",  # warm persuasive
    "ch09-local-first-practitioner-lens":  "british",      # practitioner
    "ch10-synthesis":                      "sinek",        # main narrator returns
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
    "epilogue/epilogue-what-the-stack-owes-you.md",
    "appendices/appendix-a-sync-daemon-wire-protocol.md",
    "appendices/appendix-b-threat-model-worksheets.md",
    "appendices/appendix-c-further-reading.md",
    "appendices/appendix-d-testing-the-inverted-stack.md",
    "appendices/appendix-e-citation-style.md",
]

CHUNK_CHAR_BUDGET = 1400  # target per-request size in characters


def narratable_text(md: str) -> str:
    """Convert a chapter markdown file to a clean narration script."""
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

    # Headings: drop the hashes so they read as plain sentences.
    # H1 (chapter titles) get a longer trailing beat than H2+.
    # "# Chapter 1 — Foo" -> "\n\nChapter 1, Foo.\n\n...\n\n"
    def _heading_sub(match: re.Match) -> str:
        level = len(match.group(1))
        body = match.group(2).strip().rstrip(".")
        # Em-dash in titles reads cleaner as a comma pause for headings.
        body = body.replace("—", ",").replace("–", ",")
        if level == 1:
            return f"\n\n{body}.\n\n...\n\n"
        return f"\n\n{body}.\n\n...\n\n" if level == 2 else f"\n\n{body}.\n\n"

    t = re.sub(r"(?m)^(#{1,6})\s+(.+?)\s*$", _heading_sub, t)

    # Blockquote markers
    t = re.sub(r"(?m)^\s*>\s?", "", t)

    # Horizontal rules
    t = re.sub(r"(?m)^\s*---+\s*$", "", t)

    # List bullets: "- foo" / "* foo" / "1. foo" -> "foo"
    t = re.sub(r"(?m)^\s*[-*+]\s+", "", t)
    t = re.sub(r"(?m)^\s*\d+\.\s+", "", t)

    # Em-dash / en-dash -> comma pause. Kokoro's espeak backend handles these
    # inconsistently; a comma gives a reliable micro-pause.
    t = t.replace(" — ", ", ").replace("—", ", ").replace(" – ", ", ")

    # Acronym pre-processing for known-mangled terms (applied before
    # terminal-punctuation guarantee so word boundaries still match).
    for pat, repl in ACRONYM_FIXES.items():
        t = re.sub(pat, repl, t)

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


_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")


def chunk_text(text: str, budget: int = CHUNK_CHAR_BUDGET) -> list[str]:
    """Split text into ~budget-sized chunks at paragraph and sentence boundaries."""
    chunks: list[str] = []
    buf = ""
    for para in re.split(r"\n{2,}", text):
        para = para.strip()
        if not para:
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


def synth_chunk(client: OpenAI, voice: str, text: str, speed: float, retries: int = 3) -> bytes:
    last_err = None
    extra_body = {"speed": speed} if speed and abs(speed - 1.0) > 1e-3 else None
    for attempt in range(1, retries + 1):
        try:
            kwargs = dict(
                model="kokoro",
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
    raise RuntimeError(f"Kokoro synth failed after {retries} retries: {last_err!r}")


def build_script(md_path: Path) -> str:
    """Build the narration script from a chapter markdown file."""
    raw = md_path.read_text(encoding="utf-8")
    script = narratable_text(raw)
    # Chapter lead-in pause — gives listener a beat before the chapter title.
    script = "... \n\n" + script
    return script


def render_chapter(
    client: OpenAI,
    voice: str,
    speed: float,
    md_path: Path,
    out_path: Path,
    script_path: Path,
) -> dict:
    script = build_script(md_path)
    script_path.parent.mkdir(parents=True, exist_ok=True)
    script_path.write_text(script, encoding="utf-8")
    chunks = chunk_text(script)
    total_chars = sum(len(c) for c in chunks)
    print(f"  {md_path.name}: {len(chunks)} chunks, {total_chars:,} chars")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    with out_path.open("wb") as f:
        for i, chunk in enumerate(chunks, 1):
            mp3 = synth_chunk(client, voice, chunk, speed)
            if i > 1:
                mp3 = strip_id3v2(mp3)
            f.write(mp3)
            pct = 100 * i / len(chunks)
            elapsed = time.time() - t0
            print(f"    [{i:3d}/{len(chunks)}] {pct:5.1f}%  {len(chunk):4d} chars  {elapsed:6.1f}s", flush=True)
    return {
        "source": str(md_path.relative_to(REPO).as_posix()),
        "output": str(out_path.relative_to(REPO).as_posix()),
        "script": str(script_path.relative_to(REPO).as_posix()),
        "chunks": len(chunks),
        "chars": total_chars,
        "bytes": out_path.stat().st_size,
        "seconds": round(time.time() - t0, 1),
    }


def out_name_for(src_rel: str) -> str:
    stem = Path(src_rel).stem
    return f"{stem}.mp3"


def main() -> None:
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Presets:\n  " + "\n  ".join(
            f"{name:<14} {cfg['voice']:<28} speed={cfg['speed']}"
            for name, cfg in PRESETS.items()
        ),
    )
    ap.add_argument("--preset", choices=list(PRESETS.keys()), default="sinek",
                    help="default voice preset. Default: sinek. Part II chapters "
                         "override via CHAPTER_PRESET_MAP unless --no-chapter-map is set.")
    ap.add_argument("--no-chapter-map", action="store_true",
                    help="disable per-chapter preset overrides (use --preset for all)")
    ap.add_argument("--voice", default=None,
                    help="explicit Kokoro voice (blend with +). Overrides --preset.")
    ap.add_argument("--speed", type=float, default=None,
                    help="TTS speed multiplier (0.5-2.0). Overrides --preset.")
    ap.add_argument("--base-url", default="http://localhost:8880/v1")
    ap.add_argument("--only", help="render only chapters whose source name contains this string (e.g. 'ch05')")
    ap.add_argument("--force", action="store_true", help="re-render even if an MP3 already exists")
    ap.add_argument("--dry-run", action="store_true", help="print chunk counts only")
    ap.add_argument("--scripts-only", action="store_true",
                    help="regenerate narration scripts from markdown without calling TTS")
    ap.add_argument("--list-presets", action="store_true", help="print presets and exit")
    args = ap.parse_args()

    if args.list_presets:
        for name, cfg in PRESETS.items():
            print(f"{name:<14} voice={cfg['voice']:<28} speed={cfg['speed']}")
        sys.exit(0)

    def resolve_preset(rel_path: str) -> tuple[str, str, float]:
        """Return (preset_name, voice, speed) for a chapter."""
        name = args.preset
        if not args.no_chapter_map and not args.voice:
            for key, preset_name in CHAPTER_PRESET_MAP.items():
                if key in rel_path:
                    name = preset_name
                    break
        cfg = PRESETS[name]
        v = args.voice or cfg["voice"]
        s = args.speed if args.speed is not None else cfg["speed"]
        return name, v, s

    print(f"Default preset: {args.preset}  chapter-map: {'off' if args.no_chapter_map else 'on'}")

    client = OpenAI(base_url=args.base_url, api_key="not-needed")

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
        out_path = OUT_DIR / out_name_for(rel)

        script_path = SCRIPTS_DIR / (Path(rel).stem + ".txt")

        if args.dry_run:
            script = build_script(md_path)
            chunks = chunk_text(script)
            print(f"{rel}: {len(chunks)} chunks, {sum(len(c) for c in chunks):,} chars")
            continue

        if args.scripts_only:
            script = build_script(md_path)
            script_path.parent.mkdir(parents=True, exist_ok=True)
            script_path.write_text(script, encoding="utf-8")
            print(f"  wrote {script_path.relative_to(REPO).as_posix()} ({len(script):,} chars)")
            continue

        if out_path.exists() and not args.force:
            print(f"SKIP existing: {out_path.relative_to(REPO).as_posix()} (use --force to re-render)")
            continue

        preset_name, voice, speed = resolve_preset(rel)
        print(f"\n=> {rel}  [preset={preset_name} voice={voice} speed={speed}]")
        entry = render_chapter(client, voice, speed, md_path, out_path, script_path)
        entry["preset"] = preset_name
        entry["voice"] = voice
        entry["speed"] = speed
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
