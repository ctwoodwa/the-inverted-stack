#!/usr/bin/env python3
"""Validate code snippets in a chapter file.

Usage: python3 build/code-check.py ch01

Checks:
- Sunfish package names against a known-good list
- Code blocks are either marked // illustrative or flagged for manual review
"""

import os
import re
import sys

SUNFISH_PACKAGES = {
    "Sunfish.Kernel.Sync",
    "Sunfish.Kernel.Crdt",
    "Sunfish.Kernel.Security",
    "Sunfish.Kernel.Ledger",
    "Sunfish.Kernel.Runtime",
    "Sunfish.Foundation",
    "Sunfish.Foundation.LocalFirst",
    "Sunfish.Foundation.FeatureManagement",
    "Sunfish.UI.Core",
    "Sunfish.UI.Adapters.Blazor",
    "Sunfish.Blocks.Tasks",
    "Sunfish.Blocks.Forms",
    "Sunfish.Blocks.Scheduling",
    "Sunfish.Blocks.Assets",
    "Sunfish.Compat.Telerik",
    "Sunfish.Compat.Syncfusion",
    "Sunfish.Compat.Infragistics",
}

INVENTED_API_PATTERNS = [
    r"new\s+SunfishNode\(",
    r"\.GetDocument\(",
    r"SunfishClient\.",
    r"SunfishContext\.",
]

def find_chapter(key):
    chapters_dir = os.path.join(os.path.dirname(__file__), "..", "chapters")
    for root, dirs, files in os.walk(chapters_dir):
        for fname in files:
            if fname.endswith(".md") and key in fname:
                return os.path.join(root, fname)
    return None

def check_chapter(key):
    path = find_chapter(key)
    if not path:
        print(f"ERROR: Chapter '{key}' not found")
        sys.exit(1)

    with open(path, encoding="utf-8") as f:
        content = f.read()

    code_blocks = re.findall(r"```[\w]*\n(.*?)```", content, re.DOTALL)
    errors = []
    warnings = []

    for i, block in enumerate(code_blocks):
        is_illustrative = "// illustrative" in block or "# illustrative" in block
        for pat in INVENTED_API_PATTERNS:
            if re.search(pat, block) and not is_illustrative:
                warnings.append(f"Block {i+1}: possible invented API — {pat} (mark // illustrative if intentional)")

        sunfish_refs = re.findall(r"Sunfish\.\w+(?:\.\w+)*", block)
        for ref in sunfish_refs:
            package = re.match(r"(Sunfish(?:\.\w+){1,2})", ref)
            if package and package.group(1) not in SUNFISH_PACKAGES:
                errors.append(f"Block {i+1}: unknown Sunfish package '{package.group(1)}'")

    claim_markers = re.findall(r"<!-- CLAIM:.*?-->", content)
    if claim_markers:
        for m in claim_markers:
            errors.append(f"Unresolved CLAIM marker: {m}")

    print(f"\nCode check: {os.path.basename(path)}")
    print(f"  Code blocks: {len(code_blocks)}")
    if errors:
        print(f"\n  ERRORS ({len(errors)}):")
        for e in errors:
            print(f"    - {e}")
    if warnings:
        print(f"\n  WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"    - {w}")
    if not errors and not warnings:
        print("  All checks passed.")
    print()

    if errors:
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 build/code-check.py ch01")
        sys.exit(1)
    check_chapter(sys.argv[1])
