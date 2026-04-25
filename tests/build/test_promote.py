"""Tests for the Phase 4 promotion script."""
from __future__ import annotations
import json
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "promote",
    Path(__file__).resolve().parents[2] / "build" / "promote.py",
)
promote = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(promote)


def test_compute_sha256_is_stable(tmp_path):
    p = tmp_path / "f.txt"
    p.write_text("hello\n", encoding="utf-8")
    assert promote.compute_sha256(p) == promote.compute_sha256(p)


def test_compute_sha256_matches_for_identical_files(tmp_path):
    p = tmp_path / "f.txt"
    p.write_text("hello\n", encoding="utf-8")
    p2 = tmp_path / "g.txt"
    p2.write_text("hello\n", encoding="utf-8")
    assert promote.compute_sha256(p) == promote.compute_sha256(p2)


def test_promote_copies_draft_and_writes_manifest(tmp_repo):
    # Set up: a source, a draft, and a matching log entry
    source = tmp_repo / "chapters" / "part-1" / "ch01-foo.md"
    source.write_text("source v1", encoding="utf-8")
    draft = tmp_repo / "chapters" / "_voice-drafts" / "final" / "ch01-foo.md"
    draft.write_text("voice-passed v1", encoding="utf-8")
    log_dir = tmp_repo / "chapters" / "_voice-drafts" / "_log"
    log_entry = {
        "chapter": "ch01-foo",
        "pass_num": 2,
        "input_sha256": promote.compute_sha256(source),
        "output_sha256": promote.compute_sha256(draft),
        "agent_path": ".claude/agents/voice-sinek.md",
        "agent_sha256": "0" * 64,
        "claude_cli_version": "claude 1.0.0",
        "model": "claude-sonnet-4-6",
        "prompt_mode": "normalize",
        "exit_code": 0,
        "duration_s": 1.0,
        "wall_clock_start_iso": "2026-04-25T10:00:00Z",
        "wall_clock_end_iso": "2026-04-25T10:00:01Z",
    }
    (log_dir / "20260425T100000Z-ch01-foo-pass2.json").write_text(
        json.dumps(log_entry), encoding="utf-8"
    )
    promoted_at = "2026-04-25T11:00:00Z"
    manifest_path = promote.promote_chapter(
        source=source, draft=draft, log_dir=log_dir,
        promoter="Test User <t@example.com>",
        promoted_at_iso=promoted_at,
    )
    # Source now has the draft content
    assert source.read_text(encoding="utf-8") == "voice-passed v1"
    # Manifest exists alongside source
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["promoted_at_iso"] == promoted_at
    assert manifest["promoter"] == "Test User <t@example.com>"
    assert manifest["promoted_sha256"] == promote.compute_sha256(source)
    assert manifest["manual_edit"] is False


def test_promote_fails_on_hash_mismatch(tmp_repo):
    source = tmp_repo / "chapters" / "part-1" / "ch01-foo.md"
    source.write_text("source v1", encoding="utf-8")
    draft = tmp_repo / "chapters" / "_voice-drafts" / "final" / "ch01-foo.md"
    draft.write_text("voice-passed v1", encoding="utf-8")
    log_dir = tmp_repo / "chapters" / "_voice-drafts" / "_log"
    # Log entry with WRONG output sha
    log_entry = {
        "chapter": "ch01-foo", "pass_num": 2,
        "input_sha256": promote.compute_sha256(source),
        "output_sha256": "f" * 64,  # mismatch
        "agent_path": ".claude/agents/voice-sinek.md", "agent_sha256": "0" * 64,
        "claude_cli_version": "claude 1.0.0", "model": "claude-sonnet-4-6",
        "prompt_mode": "normalize", "exit_code": 0, "duration_s": 1.0,
        "wall_clock_start_iso": "2026-04-25T10:00:00Z",
        "wall_clock_end_iso": "2026-04-25T10:00:01Z",
    }
    (log_dir / "20260425T100000Z-ch01-foo-pass2.json").write_text(
        json.dumps(log_entry), encoding="utf-8"
    )
    with pytest.raises(promote.HashMismatchError):
        promote.promote_chapter(
            source=source, draft=draft, log_dir=log_dir,
            promoter="t", promoted_at_iso="2026-04-25T11:00:00Z",
        )


def test_promote_with_accept_manual_edit_flag_succeeds_on_mismatch(tmp_repo):
    """When the user has manually edited the draft post-pass, accept_manual_edit=True
    bypasses hash verification but records the manual_edit flag in the manifest."""
    source = tmp_repo / "chapters" / "part-1" / "ch01-foo.md"
    source.write_text("source v1", encoding="utf-8")
    draft = tmp_repo / "chapters" / "_voice-drafts" / "final" / "ch01-foo.md"
    draft.write_text("manually edited content", encoding="utf-8")
    log_dir = tmp_repo / "chapters" / "_voice-drafts" / "_log"
    log_entry = {
        "chapter": "ch01-foo", "pass_num": 2,
        "input_sha256": promote.compute_sha256(source),
        "output_sha256": "f" * 64,  # mismatch — but accept_manual_edit=True overrides
        "agent_path": ".claude/agents/voice-sinek.md", "agent_sha256": "0" * 64,
        "claude_cli_version": "claude 1.0.0", "model": "claude-sonnet-4-6",
        "prompt_mode": "normalize", "exit_code": 0, "duration_s": 1.0,
        "wall_clock_start_iso": "2026-04-25T10:00:00Z",
        "wall_clock_end_iso": "2026-04-25T10:00:01Z",
    }
    (log_dir / "20260425T100000Z-ch01-foo-pass2.json").write_text(
        json.dumps(log_entry), encoding="utf-8"
    )
    manifest_path = promote.promote_chapter(
        source=source, draft=draft, log_dir=log_dir,
        promoter="t", promoted_at_iso="2026-04-25T11:00:00Z",
        accept_manual_edit=True,
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["manual_edit"] is True


def test_promote_raises_when_no_log_entry_exists(tmp_repo):
    """promote_chapter requires a log entry (audit trail); missing log = no promotion."""
    source = tmp_repo / "chapters" / "part-1" / "ch01-orphan.md"
    source.write_text("source", encoding="utf-8")
    draft = tmp_repo / "chapters" / "_voice-drafts" / "final" / "ch01-orphan.md"
    draft.write_text("draft", encoding="utf-8")
    log_dir = tmp_repo / "chapters" / "_voice-drafts" / "_log"
    # No log files written
    with pytest.raises(FileNotFoundError):
        promote.promote_chapter(
            source=source, draft=draft, log_dir=log_dir,
            promoter="t", promoted_at_iso="2026-04-25T11:00:00Z",
        )


def test_latest_log_for_picks_most_recent_when_multiple_runs_exist(tmp_repo):
    """If a chapter was re-run, latest_log_for picks the most recent timestamp."""
    log_dir = tmp_repo / "chapters" / "_voice-drafts" / "_log"
    earlier = {"chapter": "ch01-foo", "pass_num": 2, "output_sha256": "a" * 64,
               "input_sha256": "1" * 64, "agent_path": "x", "agent_sha256": "y",
               "claude_cli_version": "v", "model": "m", "prompt_mode": "p",
               "exit_code": 0, "duration_s": 0.0,
               "wall_clock_start_iso": "x", "wall_clock_end_iso": "y"}
    later = {**earlier, "output_sha256": "b" * 64}
    (log_dir / "20260425T100000Z-ch01-foo-pass2.json").write_text(
        json.dumps(earlier), encoding="utf-8"
    )
    (log_dir / "20260425T120000Z-ch01-foo-pass2.json").write_text(
        json.dumps(later), encoding="utf-8"
    )
    result = promote.latest_log_for("ch01-foo", 2, log_dir)
    assert result is not None
    assert result["output_sha256"] == "b" * 64  # the later run wins
