# tests/build/test_check_audit.py
"""Tests for the reference-integrity audit checker."""
from __future__ import annotations
from pathlib import Path

import pytest

from build.check_audit import find_jurisdictions_in_chapter, find_jurisdictions_in_appendix_f


def test_finds_jurisdictions_in_chapter(tmp_path: Path):
    ch = tmp_path / "ch01.md"
    ch.write_text("The EU's GDPR and India's DPDP Act apply.", encoding="utf-8")
    found = find_jurisdictions_in_chapter(ch)
    assert "GDPR" in found
    assert "DPDP" in found


def test_finds_jurisdictions_in_appendix_f(tmp_path: Path):
    apx = tmp_path / "appendix-f.md"
    apx.write_text("# Appendix F\n\n### GDPR\n### DPDP Act 2023\n", encoding="utf-8")
    found = find_jurisdictions_in_appendix_f(apx)
    assert "GDPR" in found
    assert "DPDP" in found
