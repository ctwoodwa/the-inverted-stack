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


def test_log_invocation_writes_json_with_required_fields(tmp_repo):
    """Per-invocation log file contains all required fields."""
    log_dir = tmp_repo / "chapters" / "_voice-drafts" / "_log"
    src = tmp_repo / "chapters" / "part-1" / "ch99-sample.md"
    src.write_text("source content", encoding="utf-8")
    dst = tmp_repo / "chapters" / "_voice-drafts" / "final" / "ch99-sample.md"
    dst.write_text("output content", encoding="utf-8")
    agent = tmp_repo / "agents" / "voice-sinek.md"
    agent.parent.mkdir(exist_ok=True, parents=True)
    agent.write_text("agent content", encoding="utf-8")

    log_path = voice_pass.log_invocation(
        log_dir=log_dir,
        chapter="ch99-sample",
        pass_num=2,
        source=src,
        output=dst,
        agent_path=agent,
        cli_version="claude 1.0.0",
        model="claude-sonnet-4-6",
        mode="polish",
        exit_code=0,
        duration_s=12.5,
        start_iso="2026-04-25T10:00:00Z",
        end_iso="2026-04-25T10:00:12Z",
    )
    import json
    data = json.loads(log_path.read_text(encoding="utf-8"))
    for key in ("chapter", "pass_num", "input_sha256", "output_sha256",
                "agent_path", "agent_sha256", "claude_cli_version", "model",
                "prompt_mode", "exit_code", "duration_s",
                "wall_clock_start_iso", "wall_clock_end_iso"):
        assert key in data, f"missing {key}"
    assert data["chapter"] == "ch99-sample"
    assert data["pass_num"] == 2
    assert data["prompt_mode"] == "polish"
    assert len(data["input_sha256"]) == 64
