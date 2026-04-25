"""Tests for build/voice-pass.py."""
from __future__ import annotations
from pathlib import Path

import importlib.util

# Import the module-under-test by file path (the filename has a hyphen)
_REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "voice_pass",
    _REPO_ROOT / "build" / "voice-pass.py",
)
voice_pass = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(voice_pass)


def test_build_prompt_references_in_repo_agent_path():
    """The prompt should point to .claude/agents/voice-X.md (in repo),
    not ~/.claude/agents/voice-X.md (user-scope)."""
    src = _REPO_ROOT / "chapters" / "part-1" / "ch01.md"
    dst = _REPO_ROOT / "chapters" / "_voice-drafts" / "final" / "ch01.md"
    prompt = voice_pass.build_prompt("sinek", src, dst)
    assert ".claude/agents/voice-sinek.md" in prompt
    assert "~/.claude/agents/voice-sinek.md" not in prompt
