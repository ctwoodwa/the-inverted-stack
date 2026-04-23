# Contributing

*The Inverted Stack* is CC-BY 4.0. Contributions are welcome.

## What's Useful

- **Technical corrections** — something is wrong, incomplete, or contradicts the reference implementation
- **Code example improvements** — a cleaner way to illustrate a concept against Sunfish
- **War stories** — real-world experience that would strengthen a chapter's argument
- **Typos and prose** — always welcome

## What to Expect

This book has a strong editorial voice and a specific thesis. Contributions that add nuance
within the existing argument are welcome. Contributions that argue for a different thesis
are better directed to a blog post or reply article.

## How to Contribute

1. Open an issue describing the change and which chapter it affects
2. Fork the repo and create a branch: `fix/ch05-flease-typo` or `improve/ch12-crdt-example`
3. Make the change; run `make word-count` to confirm you haven't drifted far from targets
4. Open a PR against `main`

## License Agreement

By submitting a pull request, you agree that your contribution is licensed under
[CC BY 4.0](LICENSE), the same license as the rest of the book. You retain copyright
in your contribution.

## Reference Implementation

Code examples reference **Sunfish** (`github.com/ctwoodwa/Sunfish`). Sunfish is pre-1.0;
reference packages by name (`Sunfish.Kernel.Sync`) rather than specific class APIs.
Mark any code not intended to run as `// illustrative`.
