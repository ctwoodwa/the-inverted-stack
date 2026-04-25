"""Tests for the stale-draft check."""
from __future__ import annotations
import os
import time
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "check_stale",
    Path(__file__).resolve().parents[2] / "build" / "check_stale.py",
)
check_stale = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_stale)


def test_detects_stale_when_source_newer_than_draft(tmp_path):
    src = tmp_path / "chapters" / "part-1" / "ch01.md"
    src.parent.mkdir(parents=True)
    src.write_text("source", encoding="utf-8")

    draft = tmp_path / "chapters" / "_voice-drafts" / "final" / "ch01.md"
    draft.parent.mkdir(parents=True)
    draft.write_text("draft", encoding="utf-8")
    # Make draft older than source
    old = time.time() - 3600
    os.utime(draft, (old, old))

    stale = check_stale.find_stale_drafts(tmp_path / "chapters")
    assert "ch01" in stale


def test_no_stale_when_draft_newer(tmp_path):
    src = tmp_path / "chapters" / "part-1" / "ch01.md"
    src.parent.mkdir(parents=True)
    src.write_text("source", encoding="utf-8")
    old = time.time() - 3600
    os.utime(src, (old, old))

    draft = tmp_path / "chapters" / "_voice-drafts" / "final" / "ch01.md"
    draft.parent.mkdir(parents=True)
    draft.write_text("draft", encoding="utf-8")

    stale = check_stale.find_stale_drafts(tmp_path / "chapters")
    assert "ch01" not in stale


def test_skips_sources_without_corresponding_drafts(tmp_path):
    """A source with no draft is not 'stale' — it just hasn't been voice-passed yet."""
    src = tmp_path / "chapters" / "part-1" / "ch99-orphan.md"
    src.parent.mkdir(parents=True)
    src.write_text("source", encoding="utf-8")
    # No draft created
    (tmp_path / "chapters" / "_voice-drafts" / "final").mkdir(parents=True)

    stale = check_stale.find_stale_drafts(tmp_path / "chapters")
    assert "ch99-orphan" not in stale
    assert stale == []


def test_returns_empty_when_final_dir_missing(tmp_path):
    """If chapters/_voice-drafts/final/ does not exist, nothing is stale."""
    src = tmp_path / "chapters" / "part-1" / "ch01.md"
    src.parent.mkdir(parents=True)
    src.write_text("source", encoding="utf-8")
    # No _voice-drafts/final/ created at all

    stale = check_stale.find_stale_drafts(tmp_path / "chapters")
    assert stale == []
