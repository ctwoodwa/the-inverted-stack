# The Inverted Stack: Local-First Nodes in a SaaS World

A practitioner book for software architects, technical founders, and senior engineers
building production-grade local-first systems.

**Status:** In active development — Part I drafting

---

## What This Book Is

Modern SaaS puts the database in someone else's cloud and calls it a feature. *The Inverted
Stack* argues for a different default: a full-capability node on the user's machine — UI,
business logic, sync daemon, and encrypted local storage — with the cloud reduced to a
relay and backup peer.

This is not a toy sync demo. It is a complete architecture for production software:
CRDT-backed document stores, distributed lease coordination for CP-class records,
a five-phase gossip anti-entropy protocol, DEK/KEK envelope encryption, and a
schema migration strategy that survives mixed-version fleets.

The architecture was stress-tested by a five-member adversarial council across two rounds.
Part II of the book documents what failed on first inspection and what changed to pass the second.

## Reference Implementation

**Sunfish** (`github.com/ctwoodwa/Sunfish`) is the open-source reference implementation
developed alongside this book.

- **Anchor** — Zone A local-first desktop (.NET MAUI Blazor Hybrid)
- **Bridge** — Zone C hybrid multi-tenant SaaS (.NET Aspire, Blazor Server)

## Structure

| Part | Chapters | Words |
|---|---|---|
| I — The Thesis and the Pain | 1–4 | ~15,000 |
| II — The Council Reads the Paper | 5–10 | ~20,000 |
| III — The Reference Architecture | 11–16 | ~22,000 |
| IV — Implementation Playbooks | 17–20 | ~14,000 |
| Epilogue + Appendices | — | ~10,500 |
| **Total** | **20 chapters** | **~83,500** |

See `book-structure.md` for the full chapter-by-chapter outline.

## Building

```bash
make draft-pdf     # Full manuscript draft (requires Pandoc)
make word-count    # Word count per chapter vs. targets
make epub          # ePub for Leanpub preview
```

## Contributing

This book is CC-BY 4.0. Contributions welcome — see `CONTRIBUTING.md`.
Technical corrections, improved examples, and additional war stories are especially valuable.

## License

[Creative Commons Attribution 4.0 International](LICENSE)
