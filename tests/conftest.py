# tests/conftest.py
"""Shared pytest fixtures."""
from __future__ import annotations
from pathlib import Path

import pytest

SAMPLE_CHAPTER = """\
# Sample Chapter

This is a paragraph of prose.

## Section

Another paragraph with some content.
"""


@pytest.fixture
def tmp_repo(tmp_path: Path) -> Path:
    """Create a minimal repo skeleton: chapters/, agents/, _voice-drafts/."""
    (tmp_path / "chapters" / "part-1").mkdir(parents=True)
    (tmp_path / "agents").mkdir()
    (tmp_path / "chapters" / "_voice-drafts" / "pass1").mkdir(parents=True)
    (tmp_path / "chapters" / "_voice-drafts" / "final").mkdir(parents=True)
    (tmp_path / "chapters" / "_voice-drafts" / "_log").mkdir(parents=True)
    return tmp_path


@pytest.fixture
def sample_chapter(tmp_repo: Path) -> Path:
    """Write a sample chapter into the tmp repo."""
    p = tmp_repo / "chapters" / "part-1" / "ch99-sample.md"
    p.write_text(SAMPLE_CHAPTER, encoding="utf-8")
    return p


@pytest.fixture
def sample_agent(tmp_repo: Path) -> Path:
    """Write a sample agent file."""
    p = tmp_repo / "agents" / "voice-sinek.md"
    p.write_text("---\nname: voice-sinek\nmodel: sonnet\n---\nAgent prompt body.\n", encoding="utf-8")
    return p
