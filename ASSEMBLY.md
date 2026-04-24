# Assembly Manifest

*This file defines the final manuscript assembly order for `make draft-pdf` and `make epub`.*
*Update as chapters reach `icm/assembled`.*

## Status

| Chapter | File | ICM Stage | Words | Target | QC-1 |
|---|---|---|---|---|---|
| Foreword | `chapters/front-matter/foreword-placeholder.md` | placeholder | — | — | pending contributor |
| Preface | `chapters/front-matter/preface.md` | icm/prose-review | 926 | ~1,300 | ⚠ expand in voice-check |
| Ch 1 | `chapters/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md` | icm/prose-review | 4,168 | ~4,500 | ✓ |
| Ch 2 | `chapters/part-1-thesis-and-pain/ch02-local-first-serious-stack.md` | icm/prose-review | 3,974 | ~4,000 | ✓ |
| Ch 3 | `chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md` | icm/prose-review | 3,096 | ~3,000 | ✓ |
| Ch 4 | `chapters/part-1-thesis-and-pain/ch04-choosing-your-architecture.md` | icm/prose-review | 3,250 | ~3,500 | ✓ |
| Ch 5 | `chapters/part-2-council-reads-the-paper/ch05-enterprise-lens.md` | icm/prose-review | 3,446 | ~3,500 | ✓ |
| Ch 6 | `chapters/part-2-council-reads-the-paper/ch06-distributed-systems-lens.md` | icm/prose-review | 3,345 | ~3,500 | ✓ |
| Ch 7 | `chapters/part-2-council-reads-the-paper/ch07-security-lens.md` | icm/prose-review | 3,353 | ~3,500 | ✓ |
| Ch 8 | `chapters/part-2-council-reads-the-paper/ch08-product-economic-lens.md` | icm/prose-review | 3,449 | ~3,500 | ✓ |
| Ch 9 | `chapters/part-2-council-reads-the-paper/ch09-local-first-practitioner-lens.md` | icm/prose-review | 3,720 | ~3,500 | ✓ |
| Ch 10 | `chapters/part-2-council-reads-the-paper/ch10-synthesis.md` | icm/prose-review | 2,463 | ~2,500 | ✓ |
| Ch 11 | `chapters/part-3-reference-architecture/ch11-node-architecture.md` | icm/prose-review | 3,833 | ~4,000 | ✓ |
| Ch 12 | `chapters/part-3-reference-architecture/ch12-crdt-engine-data-layer.md` | icm/prose-review | 4,369 | ~4,000 | ✓ |
| Ch 13 | `chapters/part-3-reference-architecture/ch13-schema-migration-evolution.md` | icm/prose-review | 3,833 | ~3,500 | ✓ |
| Ch 14 | `chapters/part-3-reference-architecture/ch14-sync-daemon-protocol.md` | icm/prose-review | 3,462 | ~3,500 | ✓ |
| Ch 15 | `chapters/part-3-reference-architecture/ch15-security-architecture.md` | icm/prose-review | 3,616 | ~3,500 | ✓ |
| Ch 16 | `chapters/part-3-reference-architecture/ch16-persistence-beyond-the-node.md` | icm/prose-review | 2,949 | ~3,500 | ⚠ expanding |
| Ch 17 | `chapters/part-4-implementation-playbooks/ch17-building-first-node.md` | icm/prose-review | 3,520 | ~4,000 | ⚠ expanding |
| Ch 18 | `chapters/part-4-implementation-playbooks/ch18-migrating-existing-saas.md` | icm/prose-review | 3,286 | ~3,500 | ✓ |
| Ch 19 | `chapters/part-4-implementation-playbooks/ch19-shipping-to-enterprise.md` | icm/prose-review | 3,148 | ~3,500 | ⚠ expanding |
| Ch 20 | `chapters/part-4-implementation-playbooks/ch20-ux-sync-conflict.md` | icm/prose-review | 2,934 | ~3,000 | ✓ |
| Epilogue | `chapters/epilogue/epilogue-what-the-stack-owes-you.md` | icm/prose-review | 2,219 | ~2,500 | ⚠ expanding |
| Appendix A | `chapters/appendices/appendix-a-sync-daemon-wire-protocol.md` | icm/prose-review | 2,181 | ~2,000 | ✓ |
| Appendix B | `chapters/appendices/appendix-b-threat-model-worksheets.md` | icm/prose-review | 1,942 | ~1,800 | ✓ |
| Appendix C | `chapters/appendices/appendix-c-further-reading.md` | icm/prose-review | 1,053 | ~1,000 | ✓ |
| Appendix D | `chapters/appendices/appendix-d-testing-the-inverted-stack.md` | icm/prose-review | 2,282 | ~2,200 | ✓ |
| Appendix E | `chapters/appendices/appendix-e-citation-style.md` | icm/approved | 476 | ~500 | ✓ |

**Running total (excluding foreword/placeholder):** ~82,000 words
**Target:** ~83,500 words
**Gap:** ~1,500 words — covered by expansion in progress on ch16/ch17/ch19/epilogue

## Next Steps

1. **icm/voice-check** (author, all chapters): personal anecdotes, field stories, consistent authorial voice
2. **Preface expansion** (author): ~374 words needed to reach 1,300-word target
3. **Ch16/Ch17/Ch19/Epilogue expansion**: in progress (automated)
4. **Foreword**: external contributor needed
5. **Final assembly**: set all chapters to `icm/assembled` and run `make draft-pdf`

## Build

```bash
make draft-pdf   # Full PDF draft
make epub        # ePub for Leanpub preview
make word-count  # Per-chapter word count vs. targets
make lint        # Check broken cross-references
```
