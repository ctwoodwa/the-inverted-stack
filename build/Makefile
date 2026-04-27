# The Inverted Stack — Build Targets
# Requires: pandoc, python3 (for word-count)

CHAPTERS_DIR := chapters
OUT_DIR := build/output
PANDOC := pandoc

CHAPTER_FILES := \
	$(CHAPTERS_DIR)/front-matter/preface.md \
	$(CHAPTERS_DIR)/part-1-thesis-and-pain/ch01-when-saas-fights-reality.md \
	$(CHAPTERS_DIR)/part-1-thesis-and-pain/ch02-local-first-serious-stack.md \
	$(CHAPTERS_DIR)/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md \
	$(CHAPTERS_DIR)/part-1-thesis-and-pain/ch04-choosing-your-architecture.md \
	$(CHAPTERS_DIR)/part-2-council-reads-the-paper/ch05-enterprise-lens.md \
	$(CHAPTERS_DIR)/part-2-council-reads-the-paper/ch06-distributed-systems-lens.md \
	$(CHAPTERS_DIR)/part-2-council-reads-the-paper/ch07-security-lens.md \
	$(CHAPTERS_DIR)/part-2-council-reads-the-paper/ch08-product-economic-lens.md \
	$(CHAPTERS_DIR)/part-2-council-reads-the-paper/ch09-local-first-practitioner-lens.md \
	$(CHAPTERS_DIR)/part-2-council-reads-the-paper/ch10-synthesis.md \
	$(CHAPTERS_DIR)/part-3-reference-architecture/ch11-node-architecture.md \
	$(CHAPTERS_DIR)/part-3-reference-architecture/ch12-crdt-engine-data-layer.md \
	$(CHAPTERS_DIR)/part-3-reference-architecture/ch13-schema-migration-evolution.md \
	$(CHAPTERS_DIR)/part-3-reference-architecture/ch14-sync-daemon-protocol.md \
	$(CHAPTERS_DIR)/part-3-reference-architecture/ch15-security-architecture.md \
	$(CHAPTERS_DIR)/part-3-reference-architecture/ch16-persistence-beyond-the-node.md \
	$(CHAPTERS_DIR)/part-4-implementation-playbooks/ch17-building-first-node.md \
	$(CHAPTERS_DIR)/part-4-implementation-playbooks/ch18-migrating-existing-saas.md \
	$(CHAPTERS_DIR)/part-4-implementation-playbooks/ch19-shipping-to-enterprise.md \
	$(CHAPTERS_DIR)/part-4-implementation-playbooks/ch20-ux-sync-conflict.md \
	$(CHAPTERS_DIR)/epilogue/epilogue-what-the-stack-owes-you.md \
	$(CHAPTERS_DIR)/appendices/appendix-a-sync-daemon-wire-protocol.md \
	$(CHAPTERS_DIR)/appendices/appendix-b-threat-model-worksheets.md \
	$(CHAPTERS_DIR)/appendices/appendix-c-further-reading.md \
	$(CHAPTERS_DIR)/appendices/appendix-d-testing-the-inverted-stack.md \
	$(CHAPTERS_DIR)/appendices/appendix-e-citation-style.md

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

.PHONY: draft-pdf
draft-pdf: $(OUT_DIR)
	$(PANDOC) $(CHAPTER_FILES) \
		--from markdown \
		--to pdf \
		--pdf-engine=xelatex \
		--metadata title="The Inverted Stack: Local-First Nodes in a SaaS World" \
		--metadata author="Christopher Wood" \
		--output $(OUT_DIR)/draft.pdf
	@echo "Draft PDF written to $(OUT_DIR)/draft.pdf"

.PHONY: epub
epub: $(OUT_DIR)
	$(PANDOC) $(CHAPTER_FILES) \
		--from markdown \
		--to epub3 \
		--toc --toc-depth=2 \
		--split-level=1 \
		--epub-cover-image=assets/cover-large.jpg \
		--metadata title="The Inverted Stack: Local-First Nodes in a SaaS World" \
		--metadata subtitle="A Practitioner's Guide to Building for the Offline-First Era" \
		--metadata author="Christopher Wood" \
		--metadata lang=en-US \
		--metadata publisher="Christopher Wood" \
		--metadata date="2026-04-25" \
		--metadata description="A practitioner's guide to local-first architecture for software architects, technical founders, and senior engineers." \
		--metadata rights="Copyright (c) 2026 Christopher Wood. All rights reserved." \
		--output $(OUT_DIR)/the-inverted-stack.epub
	@echo "EPUB 3 written to $(OUT_DIR)/the-inverted-stack.epub"

.PHONY: audiobook
audiobook:
	python build/audiobook.py

.PHONY: audiobook-hd
audiobook-hd:
	python build/audiobook.py --per-sentence

# audiobook-sample: render the first N body paragraphs of a single chapter
# to <stem>_sample.mp3. Fast voice/preset iteration loop — typically ~30s
# of compute for ~30-60s of audio. Override defaults inline:
#
#   make audiobook-sample ch=ch01
#   make audiobook-sample ch=ch15 paragraphs=5 preset=fenrir
#   make audiobook-sample ch=ch07 paragraphs=2 preset=british
#
# Output lands at build/output/audiobook/<chapter-stem>_sample.mp3 and does
# not overwrite the full-chapter render. Use --force is implicit on samples.
ch ?= ch01
paragraphs ?= 3
preset ?=
sample_args = --only $(ch) --max-paragraphs $(paragraphs) --output-suffix _sample --force
ifneq ($(preset),)
sample_args += --preset $(preset) --no-chapter-map
endif

.PHONY: audiobook-sample
audiobook-sample:
	python build/audiobook.py $(sample_args)

.PHONY: m4b
m4b:
	python build/m4b.py

# normalize: EBU R128 loudness normalization. Default target is `podcast`
# spec (-16 LUFS / -1.5 dBTP / 96 kbps) for Apple Books / Leanpub. Use
# `make normalize-acx` for ACX submission spec (-19 LUFS / -3 dBTP / 192 kbps).
# Two-pass mode is the default for both — single-pass not recommended for ACX.
.PHONY: normalize
normalize:
	python build/normalize.py

.PHONY: normalize-acx
normalize-acx:
	python build/normalize.py --target acx

.PHONY: normalize-fast
normalize-fast:
	python build/normalize.py --single-pass

# verify-loudness: re-measure each normalized MP3 against its target spec
# and exit non-zero if any chapter is out of spec. Run after `make normalize`
# (or `make normalize-acx`) to confirm the output actually landed in spec —
# ACX rejects ~30% of submissions for loudness/peak issues that two-pass
# loudnorm should have caught but didn't (silent drift on long files).
.PHONY: verify-loudness
verify-loudness:
	python build/verify_loudness.py

.PHONY: verify-loudness-acx
verify-loudness-acx:
	python build/verify_loudness.py --target acx

# embed-cover: add ID3v2 APIC frame (cover image) to every chapter MP3
# so individual chapter files display book art in audiobook players.
.PHONY: embed-cover
embed-cover:
	python build/embed-cover.py

# voice-pass: rewrite chapters through voice agents per chapters/voice-plan.yaml.
# Pass 1 applies the guest voice (Gladwell, Brown, Grant, Godin, Lencioni)
# per the plan; Pass 2 normalizes everything through Sinek (the house voice).
# Outputs go to chapters/_voice-drafts/{pass1,final}/<chapter>.md (gitignored).
# Review and merge selectively — does not overwrite source chapters.
.PHONY: voice-pass
voice-pass:
	python build/voice-pass.py

.PHONY: voice-pass-1
voice-pass-1:
	python build/voice-pass.py --pass 1

.PHONY: voice-pass-2
voice-pass-2:
	python build/voice-pass.py --pass 2

.PHONY: voice-plan
voice-plan:
	python build/voice-pass.py --plan-only

# audio-copy: run alone, with stability check on (protects against picking
# up in-flight files when an audiobook render is happening in another shell).
.PHONY: audio-copy
audio-copy:
	python build/copy-to-dropbox.py

.PHONY: audio-copy-all
audio-copy-all:
	python build/copy-to-dropbox.py --include-m4b --include-scripts --include-epub

# audiobook-deploy is the audiobook pipeline: regen MP3s, normalize loudness,
# embed per-chapter cover, bundle .m4b, copy MP3s+manifest+.m4b to Dropbox.
# Canonical "ship the audiobook" target. --no-stability-check is safe in
# chained context because each step is synchronous.
.PHONY: audiobook-deploy
audiobook-deploy: audiobook normalize embed-cover m4b-deploy

# m4b-deploy bundles the existing MP3s into a .m4b and copies both MP3s
# and the .m4b to Dropbox. Use this when MP3s are already normalized and
# only the bundle needs (re)generation + deploy.
.PHONY: m4b-deploy
m4b-deploy: m4b
	python build/copy-to-dropbox.py --include-m4b --no-stability-check

# audiobook-deploy-mp3 is the lighter variant: regen MP3s, normalize,
# embed cover, copy. Skip the .m4b rebuild. Useful for iteration on
# individual chapters.
.PHONY: audiobook-deploy-mp3
audiobook-deploy-mp3: audiobook normalize embed-cover
	python build/copy-to-dropbox.py --no-stability-check

# epub-deploy: regenerate the .epub and copy it to Dropbox. Independent
# of the audiobook pipeline; can run any time the manuscript is updated.
.PHONY: epub-deploy
epub-deploy: epub
	python build/copy-to-dropbox.py --include-epub --no-stability-check

# book-deploy: ship everything — audiobook (regen + normalize + per-chapter
# cover + .m4b) AND .epub. Canonical "ship the entire book in every
# format" target.
.PHONY: book-deploy
book-deploy: audiobook normalize embed-cover m4b epub
	python build/copy-to-dropbox.py --include-m4b --include-epub --no-stability-check

.PHONY: chapter-pdf
chapter-pdf: $(OUT_DIR)
	@test -n "$(ch)" || (echo "Usage: make chapter-pdf ch=ch01" && exit 1)
	$(eval CHAPTER_FILE := $(shell find $(CHAPTERS_DIR) -name "$(ch)-*.md" | head -1))
	@test -n "$(CHAPTER_FILE)" || (echo "Chapter $(ch) not found" && exit 1)
	$(PANDOC) $(CHAPTER_FILE) \
		--from markdown \
		--to pdf \
		--pdf-engine=xelatex \
		--output $(OUT_DIR)/$(ch).pdf
	@echo "PDF written to $(OUT_DIR)/$(ch).pdf"

.PHONY: word-count
word-count:
	@python3 build/word-count.py

.PHONY: code-check
code-check:
	@test -n "$(ch)" || (echo "Usage: make code-check ch=ch01" && exit 1)
	@python3 build/code-check.py $(ch)

.PHONY: lint
lint:
	@python3 build/lint.py

.PHONY: template
template: $(OUT_DIR)
	@test -n "$(type)" || (echo "Usage: make template type=standard|council|reference|playbook" && exit 1)
	@test -n "$(ch)" || (echo "Usage: make template type=X ch=ch01" && exit 1)
	@cp templates/chapter-$(type).md $(shell find $(CHAPTERS_DIR) -name "$(ch)-*.md" | head -1) 2>/dev/null || echo "Chapter $(ch) not found"
	@echo "Template applied to $(ch)"

.PHONY: clean
clean:
	rm -rf $(OUT_DIR)

.PHONY: check-audit
check-audit:
	python build/check_audit.py

.PHONY: promote-chapter promote-all promote-reject
promote-chapter:
	python build/promote.py --chapter $(ch)

promote-all:
	python build/promote.py --all

promote-reject:
	python build/promote.py --reject $(ch) --reason "$(reason)"

.PHONY: check-stale
check-stale:
	python build/check_stale.py
