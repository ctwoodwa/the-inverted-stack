# Assembly Manifest

*This file defines the final manuscript assembly order for `make draft-pdf` and `make epub`.*
*Update as chapters reach `icm/assembled`.*

## Status

| Chapter | File | Status | Words |
|---|---|---|---|
| Preface | `chapters/front-matter/preface.md` | stub | — |
| Ch 1 | `chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md` | stub | — |
| Ch 2 | `chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md` | stub | — |
| Ch 3 | `chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md` | stub | — |
| Ch 4 | `chapters/part-1-thesis-and-pain/ch04-choosing-your-architecture.md` | stub | — |
| Ch 5 | `chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md` | stub | — |
| Ch 6 | `chapters/part-2-council-reads-the-paper/ch06-distributed-systems-lens.md` | stub | — |
| Ch 7 | `chapters/part-2-council-reads-the-paper/ch07-security-lens.md` | stub | — |
| Ch 8 | `chapters/part-2-council-reads-the-paper/ch08-product-economic-lens.md` | stub | — |
| Ch 9 | `chapters/part-2-council-reads-the-paper/ch09-local-first-practitioner-lens.md` | stub | — |
| Ch 10 | `chapters/part-2-council-reads-the-paper/ch10-synthesis.md` | stub | — |
| Ch 11 | `chapters/part-3-reference-architecture/ch11-node-architecture.md` | stub | — |
| Ch 12 | `chapters/part-3-reference-architecture/ch12-crdt-engine-data-layer.md` | stub | — |
| Ch 13 | `chapters/part-3-reference-architecture/ch13-schema-migration-evolution.md` | stub | — |
| Ch 14 | `chapters/part-3-reference-architecture/ch14-sync-daemon-protocol.md` | stub | — |
| Ch 15 | `chapters/part-3-reference-architecture/ch15-security-architecture.md` | stub | — |
| Ch 16 | `chapters/part-3-reference-architecture/ch16-persistence-beyond-the-node.md` | stub | — |
| Ch 17 | `chapters/part-4-implementation-playbooks/ch17-building-first-node.md` | stub | — |
| Ch 18 | `chapters/part-4-implementation-playbooks/ch18-migrating-existing-saas.md` | stub | — |
| Ch 19 | `chapters/part-4-implementation-playbooks/ch19-shipping-to-enterprise.md` | stub | — |
| Ch 20 | `chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md` | stub | — |
| Epilogue | `chapters/epilogue/epilogue-what-the-stack-owes-you.md` | stub | — |
| Appendix A | `chapters/appendices/appendix-a-sync-daemon-wire-protocol.md` | stub | — |
| Appendix B | `chapters/appendices/appendix-b-threat-model-worksheets.md` | stub | — |
| Appendix C | `chapters/appendices/appendix-c-further-reading.md` | stub | — |
| Appendix D | `chapters/appendices/appendix-d-testing-the-inverted-stack.md` | stub | — |
| Appendix E | `chapters/appendices/appendix-e-citation-style.md` | approved | ~500 |
| Foreword | `chapters/front-matter/foreword-placeholder.md` | placeholder | — |

## Running Word Count

```bash
make word-count
```

## Build

```bash
make draft-pdf   # Full PDF draft
make epub        # ePub for Leanpub preview
```
