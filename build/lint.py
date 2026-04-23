#!/usr/bin/env python3
"""Structural integrity checks for The Inverted Stack manuscript.

Checks:
- All chapters in book-structure.md have corresponding stub files
- Chapter numbering is consistent (ch01 through ch20 in order)
- Internal markdown links resolve to real files
- Cross-reference mentions ("see Chapter N", "Chapter N covers") point to valid chapters
- Unresolved <!-- TODO --> and <!-- CLAIM --> markers
- Stub chapters still at initial state ("Draft not started")
"""

import os
import re
import sys

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
CHAPTERS_DIR = os.path.join(REPO_ROOT, "chapters")

EXPECTED_CHAPTERS = [
    ("front-matter/preface.md", "preface"),
    ("part-1-thesis-and-pain/ch01-when-saas-fights-reality.md", "ch01"),
    ("part-1-thesis-and-pain/ch02-local-first-serious-stack.md", "ch02"),
    ("part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md", "ch03"),
    ("part-1-thesis-and-pain/ch04-choosing-your-architecture.md", "ch04"),
    ("part-2-council-reads-the-paper/ch05-enterprise-lens.md", "ch05"),
    ("part-2-council-reads-the-paper/ch06-distributed-systems-lens.md", "ch06"),
    ("part-2-council-reads-the-paper/ch07-security-lens.md", "ch07"),
    ("part-2-council-reads-the-paper/ch08-product-economic-lens.md", "ch08"),
    ("part-2-council-reads-the-paper/ch09-local-first-practitioner-lens.md", "ch09"),
    ("part-2-council-reads-the-paper/ch10-synthesis.md", "ch10"),
    ("part-3-reference-architecture/ch11-node-architecture.md", "ch11"),
    ("part-3-reference-architecture/ch12-crdt-engine-data-layer.md", "ch12"),
    ("part-3-reference-architecture/ch13-schema-migration-evolution.md", "ch13"),
    ("part-3-reference-architecture/ch14-sync-daemon-protocol.md", "ch14"),
    ("part-3-reference-architecture/ch15-security-architecture.md", "ch15"),
    ("part-3-reference-architecture/ch16-persistence-beyond-the-node.md", "ch16"),
    ("part-4-implementation-playbooks/ch17-building-first-node.md", "ch17"),
    ("part-4-implementation-playbooks/ch18-migrating-existing-saas.md", "ch18"),
    ("part-4-implementation-playbooks/ch19-shipping-to-enterprise.md", "ch19"),
    ("part-4-implementation-playbooks/ch20-ux-sync-conflict.md", "ch20"),
    ("epilogue/epilogue-what-the-stack-owes-you.md", "epilogue"),
    ("appendices/appendix-a-sync-daemon-wire-protocol.md", "appendix-a"),
    ("appendices/appendix-b-threat-model-worksheets.md", "appendix-b"),
    ("appendices/appendix-c-further-reading.md", "appendix-c"),
    ("appendices/appendix-d-testing-the-inverted-stack.md", "appendix-d"),
]

CHAPTER_NUMBER_MAP = {f"ch{i:02d}": i for i in range(1, 21)}

errors = []
warnings = []


def check(label, ok, message):
    if not ok:
        errors.append(f"  ERROR [{label}] {message}")


def warn(label, message):
    warnings.append(f"  WARN  [{label}] {message}")


def read_file(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


# ── 1. All expected chapter files exist ────────────────────────────────────────

print("\n[1] Chapter file existence")
for rel_path, key in EXPECTED_CHAPTERS:
    full_path = os.path.join(CHAPTERS_DIR, rel_path)
    exists = os.path.exists(full_path)
    check(key, exists, f"Missing: chapters/{rel_path}")
    if exists:
        print(f"  OK    {rel_path}")


# ── 2. Chapter numbering: ch01–ch20 in order with no gaps ─────────────────────

print("\n[2] Chapter numbering")
chapter_files = []
for root, dirs, files in os.walk(CHAPTERS_DIR):
    dirs.sort()
    for fname in sorted(files):
        m = re.match(r"ch(\d+)", fname)
        if m:
            chapter_files.append((int(m.group(1)), os.path.join(root, fname)))

chapter_files.sort()
expected_nums = list(range(1, 21))
actual_nums = [n for n, _ in chapter_files]

for n in expected_nums:
    if n not in actual_nums:
        check("numbering", False, f"Chapter {n:02d} file not found")
    else:
        print(f"  OK    ch{n:02d}")

gaps = [n for n in expected_nums if n not in actual_nums]
extras = [n for n in actual_nums if n not in expected_nums]
if extras:
    for n in extras:
        warn("numbering", f"Unexpected chapter number: ch{n:02d}")


# ── 3. Internal markdown links resolve ────────────────────────────────────────

print("\n[3] Internal link resolution")
link_errors = 0
for rel_path, key in EXPECTED_CHAPTERS:
    full_path = os.path.join(CHAPTERS_DIR, rel_path)
    content = read_file(full_path)
    if content is None:
        continue
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
    for text, href in links:
        if href.startswith("http") or href.startswith("#"):
            continue  # external links and anchors not checked
        target = os.path.normpath(os.path.join(os.path.dirname(full_path), href))
        if not os.path.exists(target):
            errors.append(f"  ERROR [{key}] Broken link: [{text}]({href}) → {target}")
            link_errors += 1
        else:
            print(f"  OK    [{key}] [{text}]({href})")

if link_errors == 0:
    print("  OK    All internal links resolve")


# ── 4. Cross-reference mentions point to valid chapter numbers ────────────────

print("\n[4] Cross-reference validation")
xref_pattern = re.compile(r"[Cc]hapter\s+(\d{1,2})\b")
xref_errors = 0
for rel_path, key in EXPECTED_CHAPTERS:
    full_path = os.path.join(CHAPTERS_DIR, rel_path)
    content = read_file(full_path)
    if content is None:
        continue
    for m in xref_pattern.finditer(content):
        n = int(m.group(1))
        if n < 1 or n > 20:
            errors.append(
                f"  ERROR [{key}] Cross-reference to Chapter {n} — out of range (1–20)"
            )
            xref_errors += 1

if xref_errors == 0:
    print("  OK    All chapter cross-references in range")


# ── 5. Unresolved markers ──────────────────────────────────────────────────────

print("\n[5] Unresolved markers")
marker_counts = {"TODO": 0, "CLAIM": 0, "SUNFISH-API": 0}
for rel_path, key in EXPECTED_CHAPTERS:
    full_path = os.path.join(CHAPTERS_DIR, rel_path)
    content = read_file(full_path)
    if content is None:
        continue
    for marker_type in marker_counts:
        found = re.findall(rf"<!--\s*{marker_type}[^>]*-->", content)
        if found:
            marker_counts[marker_type] += len(found)
            warn(key, f"{len(found)} unresolved {marker_type} marker(s)")

total_markers = sum(marker_counts.values())
if total_markers == 0:
    print("  OK    No unresolved markers")
else:
    print(f"  WARN  Total unresolved markers: {total_markers}")
    for t, n in marker_counts.items():
        if n:
            print(f"         {t}: {n}")


# ── 6. Stub chapters ───────────────────────────────────────────────────────────

print("\n[6] Stub chapters (not yet drafted)")
stub_count = 0
for rel_path, key in EXPECTED_CHAPTERS:
    full_path = os.path.join(CHAPTERS_DIR, rel_path)
    content = read_file(full_path)
    if content is None:
        continue
    if "Draft not started" in content or "Draft not yet started" in content:
        stub_count += 1
        print(f"  STUB  chapters/{rel_path}")

if stub_count == 0:
    print("  OK    No stubs remaining")
else:
    print(f"\n  {stub_count} of {len(EXPECTED_CHAPTERS)} files are stubs")


# ── Summary ────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("LINT SUMMARY")
print("=" * 60)

if errors:
    print(f"\nERRORS ({len(errors)}) — must fix before assembly:")
    for e in errors:
        print(e)

if warnings:
    print(f"\nWARNINGS ({len(warnings)}) — review before publishing:")
    for w in warnings:
        print(w)

if not errors and not warnings:
    print("\nAll checks passed.")

print()

if errors:
    sys.exit(1)
