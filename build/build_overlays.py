"""Whispersync-capable EPUB build (Phases B-E).

Reads:
- build/output/the-inverted-stack.epub                    (Pandoc-generated input EPUB)
- chapters/_voice-drafts/_alignments/<chapter>.json       (per-chunk timing from audiobook.py)
- build/output/audiobook/<chapter>.mp3                    (per-chapter audio)

Writes:
- build/output/the-inverted-stack-overlays.epub           (output EPUB with overlays)

Pipeline:
1. Unpack input EPUB to a temp directory
2. Map Pandoc's spine file order (chNNN.xhtml) to our chapter stems via the
   spine declaration in content.opf
3. For each chapter that has alignment data:
   a. Inject <span class='overlay-fragment' id='{chunk_id}'> wrappers around
      sentences in the XHTML using fuzzy text matching against alignment
   b. Generate EPUB/overlays/<chapter-stem>.smil from the alignment
   c. Copy the chapter's MP3 into EPUB/audio/
4. Update EPUB/content.opf:
   - Add overlay + audio items to <manifest>
   - Add media-overlay attribute on each <spine itemref> with overlays
   - Add media:duration metadata (per overlay + total)
   - Add media:active-class metadata
5. Append overlay-active CSS to existing stylesheet
6. Re-pack EPUB (mimetype first uncompressed, rest deflated)

Usage:
    python build/build_overlays.py
    python build/build_overlays.py --output build/output/custom-name.epub
    python build/build_overlays.py --skip-audio  (don't bundle MP3s; smaller EPUB,
                                                  audio served externally)
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

REPO = Path(__file__).resolve().parent.parent
INPUT_EPUB = REPO / "build" / "output" / "the-inverted-stack.epub"
DEFAULT_OUTPUT_EPUB = REPO / "build" / "output" / "the-inverted-stack-overlays.epub"
ALIGNMENTS_DIR = REPO / "chapters" / "_voice-drafts" / "_alignments"
AUDIO_DIR = REPO / "build" / "output" / "audiobook"

# Namespaces used by EPUB 3 / OPF / SMIL
NS = {
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
    "smil": "http://www.w3.org/ns/SMIL",
    "epub": "http://www.idpf.org/2007/ops",
    "x": "http://www.w3.org/1999/xhtml",
}
ET.register_namespace("", NS["opf"])
ET.register_namespace("dc", NS["dc"])

OVERLAY_ACTIVE_CSS = """
/* EPUB 3 Media Overlay highlight — applied by the reading system to the
   currently-narrated text fragment. Subtle yellow that works in light + dark. */
.overlay-active {
    background-color: rgba(255, 235, 59, 0.4);
    transition: background-color 200ms ease-in-out;
}
.overlay-fragment {
    /* No default styling — only highlighted when active. */
}
"""


def normalize_text(text: str) -> str:
    """Lowercase, collapse whitespace, strip punctuation for fuzzy matching."""
    text = re.sub(r"[^\w\s]", " ", text.lower())
    text = re.sub(r"\s+", " ", text).strip()
    return text


def seconds_to_clock(seconds: float) -> str:
    """Convert seconds to EPUB media:duration format: HH:MM:SS.fff"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:06.3f}"


def load_alignments() -> dict[str, dict]:
    """Load all per-chapter alignment files. Key = chapter stem."""
    if not ALIGNMENTS_DIR.exists():
        print(f"ERROR: alignments dir not found: {ALIGNMENTS_DIR}", file=sys.stderr)
        print("Run `python build/audiobook.py --force` first to generate alignment data.",
              file=sys.stderr)
        sys.exit(2)
    out: dict[str, dict] = {}
    for path in sorted(ALIGNMENTS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        out[data["chapter_stem"]] = data
    return out


_TAG_RE = re.compile(r"<[^>]+>")
_OMISSION_TEXT = ("code listing omitted", "diagram omitted", "table omitted")


def _paragraph_text(html_body: str) -> str:
    """Extract visible text from an XHTML paragraph body for matching."""
    text = _TAG_RE.sub(" ", html_body)
    return normalize_text(text)


def _is_omission_chunk(source_text: str) -> bool:
    """A chunk that announces an omitted code listing/diagram/table — has no
    matching <p> in the XHTML (Pandoc emits <pre>/<figure>/<table>)."""
    norm = normalize_text(source_text)
    return any(stub in norm for stub in _OMISSION_TEXT)


def inject_fragment_ids(xhtml_path: Path, alignment: dict
                         ) -> dict[str, list[str]]:
    """Walk <p> elements in document order and assign each paragraph a unique
    fragment ID derived from the matching chapter chunk. Chunks come from
    chunk_text_paired() which packs by char budget — a single chunk may cover
    several adjacent paragraphs, so each paragraph in a chunk gets a unique
    suffix (chunk_id, chunk_id-p2, chunk_id-p3, ...) to keep XHTML IDs unique.

    Returns a mapping {chunk_id: [fragment_id_1, fragment_id_2, ...]} for
    every chunk that received at least one matched paragraph. SMIL generation
    uses this to emit one <par> per fragment, distributing the chunk's audio
    time evenly across its paragraphs. Chunks with empty lists (chapter
    titles, code-omission stubs) are skipped from SMIL entirely.
    """
    raw = xhtml_path.read_text(encoding="utf-8")
    p_pattern = re.compile(r"(<p\b[^>]*>)(.*?)(</p>)", re.DOTALL)
    text_chunks = [c for c in alignment["chunks"] if not c["is_pause"]]
    chunk_meta: list[dict] = []
    for c in text_chunks:
        source = c.get("source_text") or c["text"]
        paras = [p.strip() for p in re.split(r"\n{2,}", source) if p.strip()]
        chunk_meta.append({
            "chunk_id": c["chunk_id"],
            "norm_full": normalize_text(source),
            "para_count": max(1, len(paras)),
        })

    fragment_map: dict[str, list[str]] = {c["chunk_id"]: [] for c in text_chunks}
    state = {"chunk_idx": 0, "paras_into_chunk": 0}

    def wrap(match: re.Match) -> str:
        open_tag, body, close_tag = match.group(1), match.group(2), match.group(3)
        if not body.strip():
            return match.group(0)
        para_norm = _paragraph_text(body)
        if not para_norm:
            return match.group(0)

        # Advance past omission/heading chunks (chunks whose text doesn't
        # appear in our paragraph). Capped at 6 lookahead so a real mismatch
        # doesn't blow through the whole chapter.
        for _ in range(7):
            if state["chunk_idx"] >= len(chunk_meta):
                return match.group(0)
            meta = chunk_meta[state["chunk_idx"]]
            if (para_norm in meta["norm_full"]
                    or meta["norm_full"] in para_norm
                    or _ratio(para_norm, meta["norm_full"]) >= 0.6):
                chunk_id = meta["chunk_id"]
                # Unique per-paragraph fragment ID
                frag_n = state["paras_into_chunk"] + 1
                fragment_id = chunk_id if frag_n == 1 else f"{chunk_id}-p{frag_n}"
                fragment_map[chunk_id].append(fragment_id)
                new_body = (f'<span class="overlay-fragment" id="{fragment_id}">'
                            f'{body}</span>')
                state["paras_into_chunk"] += 1
                if state["paras_into_chunk"] >= meta["para_count"]:
                    state["chunk_idx"] += 1
                    state["paras_into_chunk"] = 0
                return f"{open_tag}{new_body}{close_tag}"
            state["chunk_idx"] += 1
            state["paras_into_chunk"] = 0

        return match.group(0)

    new_content = p_pattern.sub(wrap, raw)
    total_injected = sum(len(v) for v in fragment_map.values())
    if total_injected:
        xhtml_path.write_text(new_content, encoding="utf-8")
    return fragment_map


def _ratio(a: str, b: str) -> float:
    """Cheap word-overlap ratio for fuzzy paragraph matching when one string
    isn't a clean substring of the other (e.g., punctuation differences after
    normalization). Returns shared-word count over min word count."""
    if not a or not b:
        return 0.0
    aw = set(a.split())
    bw = set(b.split())
    if not aw or not bw:
        return 0.0
    return len(aw & bw) / min(len(aw), len(bw))


def generate_smil(alignment: dict, xhtml_filename: str,
                   fragment_map: dict[str, list[str]]) -> str:
    """Generate EPUB 3 SMIL Media Overlay XML for one chapter.

    Emits one <par> per fragment ID. Chunks that span multiple paragraphs
    get one <par> per paragraph with the chunk's audio time range divided
    evenly across them. Chunks with no fragment IDs (chapter titles, code
    omissions, etc. that didn't match any <p>) are omitted from SMIL — the
    audio still plays as part of the continuous MP3, just without a
    text-highlight cue during that span.
    """
    chapter_stem = alignment["chapter_stem"]
    audio_filename = f"{chapter_stem}.mp3"
    pars: list[str] = []
    for chunk in alignment["chunks"]:
        if chunk["is_pause"]:
            continue
        fragments = fragment_map.get(chunk["chunk_id"], [])
        if not fragments:
            continue
        n = len(fragments)
        chunk_start = chunk["start_seconds"]
        chunk_dur = chunk["end_seconds"] - chunk_start
        per_dur = chunk_dur / n
        for i, fragment_id in enumerate(fragments):
            sub_start = chunk_start + i * per_dur
            sub_end = chunk_start + (i + 1) * per_dur if i < n - 1 else chunk["end_seconds"]
            par_id = f"par-{fragment_id}"
            pars.append(
                f'    <par id="{par_id}">\n'
                f'      <text src="../text/{xhtml_filename}#{fragment_id}"/>\n'
                f'      <audio src="../audio/{audio_filename}" '
                f'clipBegin="{sub_start:.3f}s" '
                f'clipEnd="{sub_end:.3f}s"/>\n'
                f'    </par>'
            )
    seq_id = f"seq-{chapter_stem}"
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<smil xmlns="http://www.w3.org/ns/SMIL" '
        'xmlns:epub="http://www.idpf.org/2007/ops" version="3.0">\n'
        '  <body>\n'
        f'    <seq id="{seq_id}" epub:textref="../text/{xhtml_filename}" '
        'epub:type="bodymatter chapter">\n'
        + "\n".join(pars) + "\n"
        '    </seq>\n'
        '  </body>\n'
        '</smil>\n'
    )


def update_opf(opf_path: Path, chapter_to_idref: dict[str, str],
                alignments: dict[str, dict], skip_audio: bool) -> None:
    """Inject overlay + audio items into <manifest>, add media-overlay attribute
    on <spine itemref>, add media:duration and media:active-class metadata.

    chapter_to_idref maps chapter_stem -> the actual spine idref (e.g.
    "ch001_xhtml" for Pandoc-generated EPUBs).
    """
    raw = opf_path.read_text(encoding="utf-8")

    # Build new <manifest> entries
    new_manifest_items: list[str] = []
    for chapter_stem in alignments:
        # Overlay item
        new_manifest_items.append(
            f'    <item id="ovr-{chapter_stem}" href="overlays/{chapter_stem}.smil" '
            f'media-type="application/smil+xml"/>'
        )
        # Audio item (unless --skip-audio)
        if not skip_audio:
            new_manifest_items.append(
                f'    <item id="audio-{chapter_stem}" href="audio/{chapter_stem}.mp3" '
                f'media-type="audio/mpeg"/>'
            )

    # Inject before </manifest>
    raw = raw.replace(
        "</manifest>",
        "\n".join(new_manifest_items) + "\n  </manifest>"
    )

    # Add media-overlay attribute to spine itemrefs. Pandoc emits self-closing
    # itemrefs with optional whitespace and optional linear="yes". Use a regex
    # that matches the actual idref and inserts media-overlay before "/>".
    for chapter_stem, idref in chapter_to_idref.items():
        if chapter_stem not in alignments:
            continue
        # Match: <itemref idref="ch001_xhtml" ... /> or <itemref idref="ch001_xhtml" ...></itemref>
        # Insert media-overlay="ovr-..." right after the idref attribute.
        pattern = re.compile(
            r'(<itemref\s+idref="' + re.escape(idref) + r'"\s*)([^/>]*?)(/?>)'
        )

        def _add_overlay(m: re.Match, stem: str = chapter_stem) -> str:
            head, middle, tail = m.group(1), m.group(2), m.group(3)
            return f'{head}media-overlay="ovr-{stem}" {middle}{tail}'

        raw = pattern.sub(_add_overlay, raw)

    # Add media:duration and media:active-class metadata
    duration_metas: list[str] = []
    total_seconds = 0.0
    for chapter_stem, alignment in alignments.items():
        secs = alignment["total_seconds"]
        total_seconds += secs
        duration_metas.append(
            f'    <meta property="media:duration" refines="#ovr-{chapter_stem}">'
            f'{seconds_to_clock(secs)}</meta>'
        )
    duration_metas.append(
        f'    <meta property="media:duration">{seconds_to_clock(total_seconds)}</meta>'
    )
    duration_metas.append(
        '    <meta property="media:active-class">overlay-active</meta>'
    )
    # Inject before </metadata>
    raw = raw.replace(
        "</metadata>",
        "\n".join(duration_metas) + "\n  </metadata>"
    )

    opf_path.write_text(raw, encoding="utf-8")


def append_overlay_css(epub_root: Path) -> None:
    """Append .overlay-active CSS to the existing stylesheet."""
    styles_dir = epub_root / "EPUB" / "styles"
    if not styles_dir.exists():
        return
    for css_path in styles_dir.glob("*.css"):
        content = css_path.read_text(encoding="utf-8")
        if "overlay-active" in content:
            continue
        css_path.write_text(content + OVERLAY_ACTIVE_CSS, encoding="utf-8")


def parse_spine_order(opf_path: Path) -> list[tuple[str, str]]:
    """Return [(spine_idref, xhtml_filename), ...] in spine order."""
    tree = ET.parse(opf_path)
    root = tree.getroot()
    # Build id -> href map from <manifest>
    manifest = root.find("opf:manifest", NS)
    if manifest is None:
        return []
    id_to_href: dict[str, str] = {}
    for item in manifest.findall("opf:item", NS):
        item_id = item.get("id")
        href = item.get("href")
        if item_id and href:
            id_to_href[item_id] = href
    # Walk spine in order
    spine = root.find("opf:spine", NS)
    if spine is None:
        return []
    out: list[tuple[str, str]] = []
    for itemref in spine.findall("opf:itemref", NS):
        idref = itemref.get("idref")
        if idref and idref in id_to_href:
            out.append((idref, id_to_href[idref]))
    return out


# Map our chapter stems to the order they appear in the spine. The Pandoc EPUB
# emits spine items in the same order as the input markdown files.
SPINE_TO_STEM: list[str] = [
    "preface",
    "ch01-when-saas-fights-reality",
    "ch02-local-first-serious-stack",
    "ch03-inverted-stack-one-diagram",
    "ch04-choosing-your-architecture",
    "ch05-enterprise-lens",
    "ch06-distributed-systems-lens",
    "ch07-security-lens",
    "ch08-product-economic-lens",
    "ch09-local-first-practitioner-lens",
    "ch10-synthesis",
    "ch11-node-architecture",
    "ch12-crdt-engine-data-layer",
    "ch13-schema-migration-evolution",
    "ch14-sync-daemon-protocol",
    "ch15-security-architecture",
    "ch16-persistence-beyond-the-node",
    "ch17-building-first-node",
    "ch18-migrating-existing-saas",
    "ch19-shipping-to-enterprise",
    "ch20-ux-sync-conflict",
    "epilogue-what-the-stack-owes-you",
    "appendix-a-sync-daemon-wire-protocol",
    "appendix-b-threat-model-worksheets",
    "appendix-c-further-reading",
    "appendix-d-testing-the-inverted-stack",
    "appendix-e-citation-style",
]


def map_spine_to_chapters(opf_path: Path) -> dict[str, tuple[str, str]]:
    """Return chapter_stem -> (idref, xhtml filename) mapping by walking spine
    in order and lining up with SPINE_TO_STEM. The idref is needed to update
    spine itemrefs since Pandoc uses ids like "ch001_xhtml" rather than the
    bare filename stem."""
    spine = parse_spine_order(opf_path)
    # The Pandoc EPUB has cover, title_page, nav, then chapters in order.
    content_only = [(idref, href) for (idref, href) in spine
                    if not any(skip in idref.lower() for skip in ("cover", "title", "nav"))]
    out: dict[str, tuple[str, str]] = {}
    for i, stem in enumerate(SPINE_TO_STEM):
        if i >= len(content_only):
            break
        idref, href = content_only[i]
        xhtml_filename = Path(href).name
        out[stem] = (idref, xhtml_filename)
    return out


def repack_epub(source_dir: Path, output_path: Path) -> None:
    """Re-pack the EPUB. mimetype must be the FIRST file, uncompressed.
    Everything else gets DEFLATE compression."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", allowZip64=True) as zf:
        # mimetype: first, uncompressed
        mimetype_path = source_dir / "mimetype"
        if mimetype_path.exists():
            zf.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)
        # Everything else
        for path in sorted(source_dir.rglob("*")):
            if path.is_dir():
                continue
            if path.name == "mimetype":
                continue
            arcname = path.relative_to(source_dir).as_posix()
            zf.write(path, arcname, compress_type=zipfile.ZIP_DEFLATED)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(INPUT_EPUB),
                    help=f"input EPUB (default: {INPUT_EPUB.relative_to(REPO).as_posix()})")
    ap.add_argument("--output", default=str(DEFAULT_OUTPUT_EPUB),
                    help=f"output EPUB (default: {DEFAULT_OUTPUT_EPUB.relative_to(REPO).as_posix()})")
    ap.add_argument("--skip-audio", action="store_true",
                    help="don't bundle MP3s into the EPUB (smaller file; audio served externally)")
    args = ap.parse_args()

    input_epub = Path(args.input).resolve()
    output_epub = Path(args.output).resolve()
    if not input_epub.exists():
        print(f"ERROR: input EPUB not found: {input_epub}", file=sys.stderr)
        print(f"Build it first via the existing pandoc invocation.", file=sys.stderr)
        return 2

    alignments = load_alignments()
    print(f"Loaded {len(alignments)} chapter alignment(s)")
    if not alignments:
        print("ERROR: no alignment data found. Run audiobook.py --force first.", file=sys.stderr)
        return 2

    total_text_chunks = sum(
        sum(1 for c in a["chunks"] if not c["is_pause"])
        for a in alignments.values()
    )
    print(f"Total: {total_text_chunks} text chunks across {len(alignments)} chapters")

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        # 1. Unpack input EPUB
        print(f"Unpacking {input_epub.relative_to(REPO).as_posix()} ...")
        with zipfile.ZipFile(input_epub, "r") as zf:
            zf.extractall(tmpdir)

        # 2. Find content.opf and map spine to chapter stems
        opf_paths = list(tmpdir.rglob("content.opf"))
        if not opf_paths:
            print("ERROR: content.opf not found in EPUB", file=sys.stderr)
            return 2
        opf_path = opf_paths[0]
        epub_root = opf_path.parent.parent  # OPF lives at EPUB/content.opf
        text_dir = opf_path.parent / "text"
        chapter_to_spine = map_spine_to_chapters(opf_path)
        chapter_to_idref = {stem: idref for stem, (idref, _) in chapter_to_spine.items()}
        print(f"Mapped {len(chapter_to_spine)} chapters to spine files")

        # 3. Per-chapter: inject IDs, generate SMIL, copy audio
        overlays_dir = opf_path.parent / "overlays"
        overlays_dir.mkdir(exist_ok=True)
        audio_target_dir = opf_path.parent / "audio"
        if not args.skip_audio:
            audio_target_dir.mkdir(exist_ok=True)

        for chapter_stem, spine_entry in chapter_to_spine.items():
            xhtml_filename = spine_entry[1]
            if chapter_stem not in alignments:
                print(f"  SKIP {chapter_stem}: no alignment")
                continue
            xhtml_path = text_dir / xhtml_filename
            if not xhtml_path.exists():
                print(f"  SKIP {chapter_stem}: xhtml missing ({xhtml_filename})")
                continue
            alignment = alignments[chapter_stem]

            # B: inject fragment IDs
            fragment_map = inject_fragment_ids(xhtml_path, alignment)
            text_chunks = sum(1 for chunk in alignment["chunks"] if not chunk["is_pause"])
            matched_chunks = sum(1 for v in fragment_map.values() if v)
            total_fragments = sum(len(v) for v in fragment_map.values())
            match_pct = 100 * matched_chunks / text_chunks if text_chunks else 0

            # C: generate SMIL
            smil = generate_smil(alignment, xhtml_filename, fragment_map)
            (overlays_dir / f"{chapter_stem}.smil").write_text(smil, encoding="utf-8")

            # Copy audio
            if not args.skip_audio:
                audio_src = AUDIO_DIR / f"{chapter_stem}.mp3"
                if audio_src.exists():
                    shutil.copy2(audio_src, audio_target_dir / f"{chapter_stem}.mp3")
                else:
                    print(f"  WARN {chapter_stem}: audio file missing at {audio_src}",
                          file=sys.stderr)

            print(f"  OK   {chapter_stem}: {matched_chunks}/{text_chunks} chunks matched "
                  f"({match_pct:.0f}%), {total_fragments} fragments, SMIL written")

        # 4. Update OPF
        update_opf(opf_path, chapter_to_idref, alignments, args.skip_audio)
        print("Updated content.opf with overlays + media:duration + media:active-class")

        # 5. Append CSS
        append_overlay_css(epub_root)
        print("Appended .overlay-active CSS")

        # 6. Re-pack
        repack_epub(tmpdir, output_epub)
        print(f"\nRe-packed: {output_epub.relative_to(REPO).as_posix()} "
              f"({output_epub.stat().st_size / 1_048_576:.1f} MB)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
