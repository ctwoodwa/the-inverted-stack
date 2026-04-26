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


def test_promoted_chapter_with_matching_manifest_is_not_stale(tmp_path):
    """Phase 4 promotion overwrites source with draft, updating mtime past
    the draft's. If a manifest exists alongside source AND its
    promoted_sha256 matches the source's actual SHA, the chapter is
    post-promotion (not stale)."""
    import hashlib
    import json
    src = tmp_path / "chapters" / "part-1" / "ch01.md"
    src.parent.mkdir(parents=True)
    src.write_text("promoted content", encoding="utf-8")

    draft = tmp_path / "chapters" / "_voice-drafts" / "final" / "ch01.md"
    draft.parent.mkdir(parents=True)
    draft.write_text("promoted content", encoding="utf-8")
    # Draft is older than source (post-promotion mtime inversion).
    old = time.time() - 3600
    os.utime(draft, (old, old))

    # Matching manifest at source location.
    sha = hashlib.sha256(src.read_bytes()).hexdigest()
    manifest = src.with_suffix(".manifest.json")
    manifest.write_text(json.dumps({"promoted_sha256": sha}), encoding="utf-8")

    stale = check_stale.find_stale_drafts(tmp_path / "chapters")
    assert "ch01" not in stale, "promoted chapter must not be flagged as stale"


def test_promoted_chapter_with_mismatched_manifest_is_stale(tmp_path):
    """If a manifest exists but the source SHA does not match the manifest's
    promoted_sha256, the source has been edited post-promotion and the
    chapter IS stale (need to re-run voice-pass and re-promote)."""
    import json
    src = tmp_path / "chapters" / "part-1" / "ch01.md"
    src.parent.mkdir(parents=True)
    src.write_text("post-promotion edit", encoding="utf-8")

    draft = tmp_path / "chapters" / "_voice-drafts" / "final" / "ch01.md"
    draft.parent.mkdir(parents=True)
    draft.write_text("draft content", encoding="utf-8")
    old = time.time() - 3600
    os.utime(draft, (old, old))

    # Manifest with WRONG sha (doesn't match current source).
    manifest = src.with_suffix(".manifest.json")
    manifest.write_text(json.dumps({"promoted_sha256": "f" * 64}), encoding="utf-8")

    stale = check_stale.find_stale_drafts(tmp_path / "chapters")
    assert "ch01" in stale, "post-promotion edit must be flagged as stale"
