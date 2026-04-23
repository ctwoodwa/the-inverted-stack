#!/usr/bin/env python3
"""Word count per chapter vs. target."""

import os
import re

TARGETS = {
    "preface": 1000,
    "ch01": 4500,
    "ch02": 4000,
    "ch03": 3000,
    "ch04": 3500,
    "ch05": 3500,
    "ch06": 3500,
    "ch07": 3500,
    "ch08": 3500,
    "ch09": 3500,
    "ch10": 2500,
    "ch11": 4000,
    "ch12": 4000,
    "ch13": 3500,
    "ch14": 3500,
    "ch15": 4000,
    "ch16": 3000,
    "ch17": 4000,
    "ch18": 3500,
    "ch19": 3500,
    "ch20": 3000,
    "epilogue": 2500,
    "appendix-a": 2000,
    "appendix-b": 2000,
    "appendix-c": 2000,
    "appendix-d": 2000,
}

CHAPTERS_DIR = os.path.join(os.path.dirname(__file__), "..", "chapters")

def count_words(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"#.*", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return len(text.split())

def chapter_key(filename):
    m = re.search(r"(ch\d+|appendix-[a-d]|preface|epilogue)", filename)
    return m.group(1) if m else filename

total_actual = 0
total_target = 0
rows = []

for root, dirs, files in os.walk(CHAPTERS_DIR):
    for fname in sorted(files):
        if not fname.endswith(".md"):
            continue
        key = chapter_key(fname)
        path = os.path.join(root, fname)
        actual = count_words(path)
        target = TARGETS.get(key, 0)
        pct = (actual / target * 100) if target else 0
        status = "  OK" if 90 <= pct <= 110 else ("LOW" if pct < 90 else "HIGH")
        if actual == 0:
            status = "STUB"
        rows.append((key, actual, target, pct, status))
        total_actual += actual
        total_target += target

print(f"\n{'Chapter':<20} {'Actual':>7} {'Target':>7} {'%':>6}  Status")
print("-" * 52)
for key, actual, target, pct, status in rows:
    print(f"{key:<20} {actual:>7,} {target:>7,} {pct:>5.0f}%  {status}")
print("-" * 52)
total_pct = (total_actual / total_target * 100) if total_target else 0
print(f"{'TOTAL':<20} {total_actual:>7,} {total_target:>7,} {total_pct:>5.0f}%")
print()
