"""Voice-agent orchestrator: rewrite chapters through guest voice agents
(pass 1) and then through Simon Sinek's voice as a house-voice
normalization (pass 2).

Reads chapters/voice-plan.yaml to map each chapter to its primary voice
agent. Iterates chapters in plan order. Pass 1 invokes the mapped voice
agent for chapters whose primary voice is not sinek. Pass 2 invokes
voice-sinek over the pass-1 output (or the original markdown, if pass 1
was skipped).

Outputs go to chapters/_voice-drafts/{pass1,final}/<chapter>.md and the
whole drafts directory is gitignored. Review and merge selectively.

Requires: Claude Code CLI on PATH (`claude --version` succeeds). The
orchestrator dispatches via `claude -p` in headless mode and depends on
the user-scope voice agents at ~/.claude/agents/voice-*.md.

Usage:
    python build/voice-pass.py                    # full run, both passes
    python build/voice-pass.py --pass 1           # only pass 1 (guest voices)
    python build/voice-pass.py --pass 2           # only pass 2 (Sinek house voice)
    python build/voice-pass.py --only ch05        # one chapter, both passes
    python build/voice-pass.py --force            # overwrite existing drafts
    python build/voice-pass.py --dry-run          # show plan without invoking
    python build/voice-pass.py --plan-only        # print the plan and exit
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHAPTERS = REPO / "chapters"
PLAN = CHAPTERS / "voice-plan.yaml"
DRAFTS = CHAPTERS / "_voice-drafts"
PASS1_DIR = DRAFTS / "pass1"
PASS2_DIR = DRAFTS / "final"
USER_AGENTS = Path.home() / ".claude" / "agents"

VALID_VOICES = {"sinek", "gladwell", "brown", "grant", "godin", "lencioni"}


def load_plan() -> dict[str, str]:
    """Parse voice-plan.yaml as a flat key: value map. Inline comments
    after `#` and blank/comment lines are stripped. No external YAML dep."""
    plan: dict[str, str] = {}
    for line in PLAN.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.split("#", 1)[0].strip()
        if not value:
            continue
        if value not in VALID_VOICES:
            print(f"WARN: unknown voice '{value}' for {key.strip()}", file=sys.stderr)
            continue
        plan[key.strip()] = value
    return plan


def find_chapter(chapter_stem: str) -> Path | None:
    """Return the source markdown path for chapter_stem under chapters/,
    excluding anything inside chapters/_voice-drafts/."""
    matches = [
        p for p in CHAPTERS.glob(f"**/{chapter_stem}.md")
        if "_voice-drafts" not in p.parts
    ]
    return matches[0] if matches else None


def find_claude_cli() -> str:
    """Locate the Claude Code CLI binary. Returns the executable path or
    raises RuntimeError if not found."""
    candidate = shutil.which("claude")
    if candidate:
        return candidate
    raise RuntimeError(
        "Claude Code CLI not found on PATH. Install Claude Code "
        "(https://docs.anthropic.com/en/docs/claude-code) or run this script "
        "from a shell where `claude` is available."
    )


def build_prompt(voice: str, source_path: Path, output_path: Path) -> str:
    """Construct the headless prompt. References the user-scope agent file
    by path so the agent's tool config and instructions apply, and
    instructs Claude to read the source, rewrite, and write the result.
    The agent does the file I/O via its Read and Write tools."""
    rel_src = source_path.relative_to(REPO).as_posix()
    rel_dst = output_path.relative_to(REPO).as_posix()
    return f"""Operate as the voice-{voice} agent (defined in ~/.claude/agents/voice-{voice}.md).

TASK
1. Read the chapter markdown at {rel_src}
2. Rewrite it in your voice following ALL instructions in your agent file.
3. Apply your calibration self-check before producing the rewrite.
4. Write the rewritten markdown to {rel_dst} (create parent directories if needed).

PRESERVATION RULES (do not rewrite these — copy them through verbatim):
- YAML frontmatter at the top of the file IF AND ONLY IF the source already has it.
  Do NOT invent or add YAML frontmatter when the source has none. The presence of
  HTML comments at the top is not frontmatter.
- HTML comments (<!-- ... -->)
- Fenced code blocks (```...```)
- Fenced mermaid diagrams (```mermaid...```)
- Markdown tables (| ... | rows)
- Inline image syntax ![...](...)
- Inline link syntax [...](...)

REWRITE TARGETS:
- Prose paragraphs
- Prose-style headings (titles, section labels)
- Prose list items (when the bullet contains sentences, not just citations)

OUTPUT TO STDOUT:
After successfully writing the file, output a single line of the form:
DONE: <output-path> (<word-count> words)
Output nothing else. Do not explain. Do not summarize the rewrite.
"""


def run_voice_pass(
    claude: str, voice: str, source: Path, output: Path,
    timeout_s: int = 600,
) -> tuple[bool, str]:
    """Dispatch one voice-pass via headless Claude Code. Returns
    (success, message). On success the output file is written by the
    agent itself; the orchestrator just verifies the file exists."""
    output.parent.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt(voice, source, output)
    try:
        proc = subprocess.run(
            [claude, "-p", prompt],
            capture_output=True, text=True, cwd=REPO, timeout=timeout_s,
        )
    except subprocess.TimeoutExpired:
        # Check whether the agent wrote the file before being killed —
        # claude -p sometimes lingers after the agent's tool calls return,
        # producing a false-positive timeout while the actual work is done.
        if output.exists() and output.stat().st_size > 0:
            return True, f"timeout-but-output-written ({output.stat().st_size} bytes)"
        return False, f"timeout after {timeout_s}s, no output written"
    if proc.returncode != 0:
        return False, f"claude exited {proc.returncode}: {proc.stderr.strip()[:240]}"
    if not output.exists() or output.stat().st_size == 0:
        return False, f"agent did not write {output.relative_to(REPO).as_posix()}"
    last_line = (proc.stdout.strip().splitlines() or [""])[-1]
    return True, last_line[:160]


def plan_summary(plan: dict[str, str]) -> str:
    counts: dict[str, int] = {}
    for v in plan.values():
        counts[v] = counts.get(v, 0) + 1
    parts = ", ".join(f"{v}={n}" for v, n in sorted(counts.items()))
    return f"{len(plan)} chapters: {parts}"


def main() -> None:
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )
    ap.add_argument("--pass", dest="pass_n", type=int, choices=[1, 2],
                    help="run only pass 1 (guest voices) or pass 2 (Sinek)")
    ap.add_argument("--only",
                    help="filter chapters whose name contains this substring "
                         "(e.g. --only ch05, --only appendix)")
    ap.add_argument("--force", action="store_true",
                    help="overwrite existing drafts")
    ap.add_argument("--dry-run", action="store_true",
                    help="show plan and what would run without invoking Claude")
    ap.add_argument("--plan-only", action="store_true",
                    help="print the parsed plan and exit")
    ap.add_argument("--timeout", type=int, default=600,
                    help="per-chapter timeout in seconds (default: 600)")
    args = ap.parse_args()

    if not PLAN.exists():
        print(f"Voice plan not found: {PLAN}", file=sys.stderr)
        sys.exit(2)

    plan = load_plan()
    if args.only:
        plan = {k: v for k, v in plan.items() if args.only in k}
    if not plan:
        print("Nothing to process (filter matched zero chapters).")
        return

    print(f"Plan: {plan_summary(plan)}")
    if args.plan_only:
        for ch, voice in plan.items():
            print(f"  {ch:<48} -> voice-{voice}")
        return

    # Ensure CLI is available before doing any work (unless --dry-run).
    claude = None
    if not args.dry_run:
        try:
            claude = find_claude_cli()
        except RuntimeError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(2)

    # Resolve source paths up-front so we fail fast on missing chapters.
    sources: dict[str, Path] = {}
    for ch in plan:
        src = find_chapter(ch)
        if not src:
            print(f"WARN: source file not found for {ch}", file=sys.stderr)
            continue
        sources[ch] = src

    # Pass 1 — guest voices over original sources.
    if args.pass_n in (None, 1):
        print("\n=== PASS 1 (guest voices) ===")
        ran = 0
        skipped = 0
        for ch, voice in plan.items():
            if voice == "sinek":
                continue  # sinek-mapped chapters skip pass 1
            src = sources.get(ch)
            if not src:
                continue
            dst = PASS1_DIR / f"{ch}.md"
            if dst.exists() and not args.force:
                print(f"  SKIP {ch:<48} (exists; use --force to overwrite)")
                skipped += 1
                continue
            label = f"  {ch:<48} -> voice-{voice}"
            if args.dry_run:
                print(f"  WOULD-RUN {label}")
                continue
            t0 = time.time()
            ok, msg = run_voice_pass(claude, voice, src, dst, timeout_s=args.timeout)
            dt = time.time() - t0
            status = "OK" if ok else "FAIL"
            print(f"  [{status}] {ch:<48} ({dt:5.1f}s) {msg[:80]}")
            if ok:
                ran += 1
        if not args.dry_run:
            print(f"  pass 1: {ran} ran, {skipped} skipped")

    # Pass 2 — Sinek over pass-1 output (or original, for sinek-mapped).
    if args.pass_n in (None, 2):
        print("\n=== PASS 2 (Sinek house voice) ===")
        ran = 0
        skipped = 0
        for ch, voice in plan.items():
            if voice == "sinek":
                src = sources.get(ch)
            else:
                src = PASS1_DIR / f"{ch}.md"
                if not src.exists():
                    print(f"  SKIP {ch:<48} (no pass-1 output to normalize)")
                    skipped += 1
                    continue
            if not src:
                continue
            dst = PASS2_DIR / f"{ch}.md"
            if dst.exists() and not args.force:
                print(f"  SKIP {ch:<48} (exists; use --force)")
                skipped += 1
                continue
            label = f"  {ch:<48} (source: {'pass1' if voice != 'sinek' else 'original'})"
            if args.dry_run:
                print(f"  WOULD-RUN {label}")
                continue
            t0 = time.time()
            ok, msg = run_voice_pass(claude, "sinek", src, dst, timeout_s=args.timeout)
            dt = time.time() - t0
            status = "OK" if ok else "FAIL"
            print(f"  [{status}] {ch:<48} ({dt:5.1f}s) {msg[:80]}")
            if ok:
                ran += 1
        if not args.dry_run:
            print(f"  pass 2: {ran} ran, {skipped} skipped")

    if not args.dry_run:
        print(f"\nDrafts: {DRAFTS.relative_to(REPO).as_posix()}/")
        print("Review with: git diff --no-index chapters/<part>/<ch>.md "
              "chapters/_voice-drafts/final/<ch>.md")


if __name__ == "__main__":
    main()
