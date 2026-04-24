# Preface

<!-- icm/prose-review -->
<!-- Target: ~1,300 words -->
<!-- Source: source/local_node_saas_v13.md preface, source/inverted-stack-v5.md §1 -->

The gap this book addresses is not a gap in research. The local-first ideals — offline operation, real-time collaboration without a central authority, data portability, user ownership — date to Kleppmann et al.'s 2019 essay. The distributed systems components that make those ideals technically achievable — CRDTs, gossip protocols, envelope encryption, distributed leases — are all production-proven in individual systems. The gap is a blueprint: a single resource that specifies how to compose those components into production software that survives contact with enterprise IT, adversarial security review, and the commercial reality of building a business on top of it.

This book is that blueprint.

## Why I Wrote This

I spent a year designing a local-node architecture and subjecting it to the kind of adversarial review that standard technical publishing does not provide. The council — five domain experts representing enterprise IT, distributed systems research, security, product management, and the local-first community — reviewed the architecture twice. The first round produced two BLOCK verdicts. The architecture failed on CRDT garbage collection, distributed lease correctness, key compromise incident response, commercial viability, and data portability simultaneously. Those failures were not superficial. Fixing them required substantive redesign.

What emerged from Round 2 was an architecture I could not find fault with. Not because it is perfect — the open questions in the epilogue are genuine — but because it had earned its claims through a process that tried to find the failure modes before the first production deployment did.

This book is the result of that process, written to be the resource I needed when I started.

## Who This Book Is For

**Software architects and senior engineers** building or evaluating local-first systems will find a complete distributed systems specification in Parts III and IV: CRDT engine selection and GC policy, schema migration for mixed-version fleets, sync daemon protocol, security key hierarchy, and the full Sunfish package reference. The technical sections are precise enough to implement from.

**Enterprise evaluators, IT architects, and technical decision-makers** will find a governance-first design in Chapters 5, 7, 15, and 19: named MDM policies, SBOM toolchain specification, compliance framework mappings, and an incident response runbook written to answer procurement questions directly. Chapter 19 covers code signing, MDM deployment, and air-gap operation as first-class requirements, not afterthoughts.

**Open-source contributors, technical founders, and product teams** will find a viable project model in Chapters 8, 10, and 16: relay economics modeled at 10/100/1,000 teams, a first-customer archetype with an acquisition channel, a dual-license strategy, and a governance model that does not rely on "community adoption" as a plan.

## How to Read This Book

Part I convinces. It establishes the failure modes of centralized SaaS — not as abstractions but as specific, domain-grounded scenarios — and introduces the architecture that addresses them. If you finish Chapter 4 unconvinced that the local-node architecture is worth the implementation complexity for your use case, the selection framework there will tell you why, and Parts III and IV are not for you.

Part II stress-tests. Five domain experts challenged the architecture across two rounds of adversarial review. Each chapter presents one lens, one set of objections, and one verdict. You need not agree with every council member's conclusion, but understand what each raised — because the same objections will come from your own enterprise customers, security auditors, and commercial partners.

Parts III and IV are reference material. Part III specifies the architecture component by component — read it when you are ready to build or need to understand why a design choice was made. Part IV provides the minimal path to a working implementation — read it when you are ready to run something.

## A Note on Sunfish

Sunfish (`github.com/ctwoodwa/Sunfish`) is the open-source reference implementation developed alongside this book. Two canonical accelerators exist: **Anchor**, a Zone A local-first desktop built on .NET MAUI Blazor Hybrid, and **Bridge**, a Zone C hybrid multi-tenant SaaS built on .NET Aspire and Blazor Server.

Sunfish is pre-1.0. This book references it by package name — `Sunfish.Kernel.Sync`, `Sunfish.Foundation.LocalFirst` — rather than specific class APIs, which evolve. The architectural patterns and the package contracts are stable enough to cite and build against. Specific method signatures are not. When Sunfish reaches 1.0, a companion release of this book will update any implementation-specific guidance.

## A Note on the CRDT Engine

The architecture specifies Loro as the aspirational primary CRDT engine for .NET: compact binary encoding, shallow snapshots, Rust-native performance through P/Invoke bindings. Sunfish's current reference implementation uses YDotNet (Yjs .NET bindings) — the practical choice while the `loro-cs` C# bindings mature. Both paths are viable. The `ICrdtEngine` abstraction in `Sunfish.Kernel.Crdt` keeps the choice reversible. Chapter 12 covers both engines, the evaluation criteria for choosing between them, and the migration path if you start with YDotNet and later switch.

## A Note on the Kleppmann Council

The five council members in Part II are named personas representing real professional domains. A charter written before the review defines their scoring dimensions, standard prompts, and verdict rules. The council's job is to find the conditions under which the architecture fails, not to endorse it.

Part II can be read as a narrative — what failed, what changed, what the architecture earned — or as a reference for the specific technical and commercial problems each chapter resolves. Read Part II before you build — the council's objections are the ones your enterprise customers, security auditors, and commercial partners will raise.

---

*C.W., April 2026*
