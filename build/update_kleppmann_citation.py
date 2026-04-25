"""One-shot updater: standardize all Kleppmann et al. 2019 citations
to include DOI and Ink & Switch URL per the publisher's requested attribution.

The book cites this paper in 7 places; existing instances vary slightly
(some omit month, one uses hyphen instead of en-dash). Standardize all
to the canonical IEEE form including doi: and [Online]. Available:.
"""
from __future__ import annotations
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

CANONICAL = ('[1] M. Kleppmann, A. Wiggins, P. van Hardenberg, and M. McGranaghan, '
             '"Local-first software: You own your data, in spite of the cloud," '
             'in *Proc. ACM SIGPLAN Int. Symp. New Ideas, New Paradigms, and '
             'Reflections on Programming and Software (Onward! \'19)*, '
             'Athens, Greece, Oct. 2019, pp. 154–178, doi: 10.1145/3359591.3359737. '
             '[Online]. Available: https://www.inkandswitch.com/essay/local-first/')

# Each tuple: (path, current_text, replacement_text)
REPLACEMENTS: list[tuple[str, str, str]] = [
    # ch02 — no month, no doi
    (
        "chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md",
        '[1] M. Kleppmann, A. Wiggins, P. van Hardenberg, and M. McGranaghan, "Local-first software: You own your data, in spite of the cloud," in *Proc. ACM SIGPLAN Int. Symp. New Ideas, New Paradigms, and Reflections on Programming and Software (Onward!)*, Athens, Greece, 2019, pp. 154–178.',
        CANONICAL,
    ),
    # ch03 — uses curly quotes; no month, no doi
    (
        "chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md",
        '[1] M. Kleppmann, A. Wiggins, P. van Hardenberg, and M. McGranaghan, “Local-first software: You own your data, in spite of the cloud,” in *Proc. ACM SIGPLAN Int. Symp. New Ideas, New Paradigms, and Reflections on Programming and Software (Onward!)*, Athens, Greece, 2019, pp. 154–178.',
        CANONICAL,
    ),
    # ch10 — no city, has month; no doi
    (
        "chapters/part-2-council-reads-the-paper/ch10-synthesis.md",
        '[1] M. Kleppmann, A. Wiggins, P. van Hardenberg, and M. McGranaghan, "Local-first software: you own your data, in spite of the cloud," in *Proc. ACM SIGPLAN Int. Symp. New Ideas, New Paradigms, and Reflections on Programming and Software (Onward!)*, Oct. 2019, pp. 154–178.',
        CANONICAL,
    ),
    # ch09 — no city, no month, hyphen instead of en-dash, lowercase 'you', no doi
    (
        "chapters/part-2-council-reads-the-paper/ch09-local-first-practitioner-lens.md",
        '[1] M. Kleppmann, A. Wiggins, P. van Hardenberg, and M. McGranaghan, "Local-first software: you own your data, in spite of the cloud," in *Proc. ACM SIGPLAN Int. Symp. New Ideas, New Paradigms, and Reflections on Programming and Software (Onward!)*, 2019, pp. 154-178.',
        CANONICAL,
    ),
    # ch12 — no month, no doi
    (
        "chapters/part-3-reference-architecture/ch12-crdt-engine-data-layer.md",
        '[1] M. Kleppmann, A. Wiggins, P. van Hardenberg, and M. McGranaghan, "Local-first software: You own your data, in spite of the cloud," in *Proc. ACM SIGPLAN Int. Symp. New Ideas, New Paradigms, and Reflections on Programming and Software (Onward!)*, Athens, Greece, 2019, pp. 154–178.',
        CANONICAL,
    ),
    # appendix-c — has Onward! '19 form, no doi
    (
        "chapters/appendices/appendix-c-further-reading.md",
        '[1] M. Kleppmann, A. Wiggins, P. van Hardenberg, and M. McGranaghan, "Local-first software: You own your data, in spite of the cloud," in *Proc. ACM SIGPLAN Int. Symp. New Ideas, New Paradigms, and Reflections on Programming and Software (Onward! \'19)*, Athens, Greece, Oct. 2019, pp. 154–178.',
        CANONICAL,
    ),
    # appendix-e (citation-style example) — wrap with the trailing pipe of the table
    (
        "chapters/appendices/appendix-e-citation-style.md",
        '| [1] | Conference paper | M. Kleppmann, A. Wiggins, P. van Hardenberg, and M. McGranaghan, "Local-first software: You own your data, in spite of the cloud," in *Proc. ACM SIGPLAN Int. Symp. New Ideas, New Paradigms, and Reflections on Programming and Software (Onward! \'19)*, Athens, Greece, Oct. 2019, pp. 154–178. |',
        '| [1] | Conference paper | M. Kleppmann, A. Wiggins, P. van Hardenberg, and M. McGranaghan, "Local-first software: You own your data, in spite of the cloud," in *Proc. ACM SIGPLAN Int. Symp. New Ideas, New Paradigms, and Reflections on Programming and Software (Onward! \'19)*, Athens, Greece, Oct. 2019, pp. 154–178, doi: 10.1145/3359591.3359737. [Online]. Available: https://www.inkandswitch.com/essay/local-first/ |',
    ),
]


def main() -> int:
    failures: list[str] = []
    successes: list[str] = []
    for rel_path, old, new in REPLACEMENTS:
        path = REPO / rel_path
        text = path.read_text(encoding="utf-8")
        if old not in text:
            failures.append(f"{rel_path}: old text not found")
            continue
        if text.count(old) > 1:
            failures.append(f"{rel_path}: matches {text.count(old)} times")
            continue
        path.write_text(text.replace(old, new), encoding="utf-8")
        successes.append(rel_path)
    print(f"Applied {len(successes)} of {len(REPLACEMENTS)} updates")
    for s in successes:
        print(f"  OK   {s}")
    for f in failures:
        print(f"  FAIL {f}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
