# The Inverted Stack — Build Targets
# Requires: pandoc, python3 (for word-count)

CHAPTERS_DIR := chapters
OUT_DIR := build/output
PANDOC := pandoc
PYTHON ?= python3

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
	$(CHAPTERS_DIR)/part-5-operational-concerns/ch21-operating-a-fleet.md \
	$(CHAPTERS_DIR)/part-5-operational-concerns/ch22-security-operations.md \
	$(CHAPTERS_DIR)/part-5-operational-concerns/ch23-endpoint-collaborator-ops.md \
	$(CHAPTERS_DIR)/epilogue/epilogue-what-the-stack-owes-you.md \
	$(CHAPTERS_DIR)/appendices/appendix-a-sync-daemon-wire-protocol.md \
	$(CHAPTERS_DIR)/appendices/appendix-b-threat-model-worksheets.md \
	$(CHAPTERS_DIR)/appendices/appendix-c-further-reading.md \
	$(CHAPTERS_DIR)/appendices/appendix-d-testing-the-inverted-stack.md \
	$(CHAPTERS_DIR)/appendices/appendix-e-citation-style.md \
	$(CHAPTERS_DIR)/appendices/appendix-f-regulatory-coverage.md \
	$(CHAPTERS_DIR)/appendices/appendix-g-glossary.md

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
	$(PYTHON) build/audiobook.py

.PHONY: audiobook-hd
audiobook-hd:
	$(PYTHON) build/audiobook.py --per-sentence

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
	$(PYTHON) build/audiobook.py $(sample_args)

# Chatterbox-engine variants — render against the Windows GPU box's
# Chatterbox (Resemble AI) server. Auth via Bearer token in TTS_API_KEY.
# CHATTERBOX_URL points at the Tailscale hostname (default) or LAN IP.
# Override per-render or once per shell session:
#
#   export TTS_API_KEY=<token>
#   CHATTERBOX_URL=http://192.168.1.50:8881/v1 make audiobook-sample-chatterbox ch=ch01
#   CHATTERBOX_URL=http://desktop-umt08rn.taildefd38.ts.net:8881/v1 make audiobook-chatterbox
CHATTERBOX_URL ?= http://desktop-umt08rn:8881/v1
chatterbox_args = --engine chatterbox --base-url $(CHATTERBOX_URL)

.PHONY: audiobook-chatterbox
audiobook-chatterbox:
	$(PYTHON) build/audiobook.py $(chatterbox_args)

.PHONY: audiobook-sample-chatterbox
audiobook-sample-chatterbox:
	$(PYTHON) build/audiobook.py $(sample_args) $(chatterbox_args)

# audiobook-voices-chatterbox: query the Chatterbox server for its voice
# catalog. Run this after standing up the Windows server, after every voice
# upload, and before filling persona slots in PRESETS_CHATTERBOX.
.PHONY: audiobook-voices-chatterbox
audiobook-voices-chatterbox:
	@$(PYTHON) build/voice_upload.py --base-url $(CHATTERBOX_URL) list || \
		(echo "Could not reach $(CHATTERBOX_URL). Check TTS_API_KEY + Windows server." && exit 1)

# audiobook-voice-upload: upload (or replace) a single voice via the
# multipart PUT API. Args:
#   id=<voice_id>          required — slug (lowercase alphanumeric/_/-)
#   audio=<path>           required — wav/mp3/flac
#   transcript=<text>      required — exact text spoken in the clip
#   display_name=<text>    optional — human label
#   language=<bcp47>       optional — en-US, ru, pt-BR, …
#   notes=<text>           optional — provenance
#
# Example:
#   make audiobook-voice-upload id=voss audio=references/voss-30s.wav \
#     transcript="Procurement isn't where compliance lives." \
#     display_name="Council member — Voss" language=en-US
.PHONY: audiobook-voice-upload
audiobook-voice-upload:
	@test -n "$(id)"          || (echo "id=<voice_id> required" && exit 2)
	@test -n "$(audio)"       || (echo "audio=<path> required" && exit 2)
	@test -n "$(transcript)"  || (echo "transcript=<text> required" && exit 2)
	$(PYTHON) build/voice_upload.py --base-url $(CHATTERBOX_URL) put $(id) \
	  --audio "$(audio)" --transcript "$(transcript)" \
	  $(if $(display_name),--display-name "$(display_name)") \
	  $(if $(language),--language "$(language)") \
	  $(if $(notes),--notes "$(notes)")

# audiobook-voice-delete: remove a voice. Stock voices (en_man, en_woman,
# etc.) are protected on the server side and return 403.
.PHONY: audiobook-voice-delete
audiobook-voice-delete:
	@test -n "$(id)" || (echo "id=<voice_id> required" && exit 2)
	$(PYTHON) build/voice_upload.py --base-url $(CHATTERBOX_URL) delete $(id)

# librivox-search: find candidate audiobooks for narrator reference clips.
# Args:
#   language=<text>   default English
#   solo=1            restrict to single-reader books (best for cloning)
#   limit=<n>         default 30
#   reader=<id>       LibriVox reader_id (find via https://librivox.org/reader/<id>)
#
# Example:
#   make librivox-search language=Russian solo=1
#   make librivox-search reader=263 solo=1
language ?= English
limit    ?= 30
.PHONY: librivox-search
librivox-search:
	$(PYTHON) build/librivox_browse.py search --language "$(language)" --limit $(limit) \
	  $(if $(solo),--solo-only) \
	  $(if $(reader),--reader "$(reader)")

# librivox-sections: list sections + per-section reader for a book.
.PHONY: librivox-sections
librivox-sections:
	@test -n "$(book)" || (echo "book=<id> required" && exit 2)
	$(PYTHON) build/librivox_browse.py sections --book $(book)

# librivox-preview: extract a clip to /tmp/ for listening. Args:
#   book=<id>     required
#   section=<n>   required — section number (1-indexed)
#   start=<tc>    default 1:00 (skip LibriVox boilerplate intro)
#   length=<sec>  default 30
.PHONY: librivox-preview
librivox-preview:
	@test -n "$(book)"    || (echo "book=<id> required" && exit 2)
	@test -n "$(section)" || (echo "section=<n> required" && exit 2)
	$(PYTHON) build/librivox_browse.py preview --book $(book) --section $(section) \
	  $(if $(start),--start $(start)) $(if $(length),--length $(length))

# librivox-extract: extract a clean reference clip to disk for upload.
# Args same as preview, plus:
#   out=<path>    required — .wav (preferred) / .mp3 / .flac
.PHONY: librivox-extract
librivox-extract:
	@test -n "$(book)"    || (echo "book=<id> required" && exit 2)
	@test -n "$(section)" || (echo "section=<n> required" && exit 2)
	@test -n "$(out)"     || (echo "out=<path> required" && exit 2)
	$(PYTHON) build/librivox_browse.py extract --book $(book) --section $(section) \
	  --out $(out) $(if $(start),--start $(start)) $(if $(length),--length $(length))

.PHONY: m4b
m4b:
	$(PYTHON) build/m4b.py

# normalize: EBU R128 loudness normalization. Default target is `podcast`
# spec (-16 LUFS / -1.5 dBTP / 96 kbps) for Apple Books / Leanpub. Use
# `make normalize-acx` for ACX submission spec (-19 LUFS / -3 dBTP / 192 kbps).
# Two-pass mode is the default for both — single-pass not recommended for ACX.
.PHONY: normalize
normalize:
	$(PYTHON) build/normalize.py

.PHONY: normalize-acx
normalize-acx:
	$(PYTHON) build/normalize.py --target acx

.PHONY: normalize-fast
normalize-fast:
	$(PYTHON) build/normalize.py --single-pass

# verify-loudness: re-measure each normalized MP3 against its target spec
# and exit non-zero if any chapter is out of spec. Run after `make normalize`
# (or `make normalize-acx`) to confirm the output actually landed in spec —
# ACX rejects ~30% of submissions for loudness/peak issues that two-pass
# loudnorm should have caught but didn't (silent drift on long files).
.PHONY: verify-loudness
verify-loudness:
	$(PYTHON) build/verify_loudness.py

.PHONY: verify-loudness-acx
verify-loudness-acx:
	$(PYTHON) build/verify_loudness.py --target acx

# embed-cover: add ID3v2 APIC frame (cover image) to every chapter MP3
# so individual chapter files display book art in audiobook players.
.PHONY: embed-cover
embed-cover:
	$(PYTHON) build/embed-cover.py

# voice-pass: rewrite chapters through voice agents per chapters/voice-plan.yaml.
# Pass 1 applies the guest voice (Gladwell, Brown, Grant, Godin, Lencioni)
# per the plan; Pass 2 normalizes everything through Sinek (the house voice).
# Outputs go to chapters/_voice-drafts/{pass1,final}/<chapter>.md (gitignored).
# Review and merge selectively — does not overwrite source chapters.
.PHONY: voice-pass
voice-pass:
	$(PYTHON) build/voice-pass.py

.PHONY: voice-pass-1
voice-pass-1:
	$(PYTHON) build/voice-pass.py --pass 1

.PHONY: voice-pass-2
voice-pass-2:
	$(PYTHON) build/voice-pass.py --pass 2

.PHONY: voice-plan
voice-plan:
	$(PYTHON) build/voice-pass.py --plan-only

# audio-copy: run alone, with stability check on (protects against picking
# up in-flight files when an audiobook render is happening in another shell).
.PHONY: audio-copy
audio-copy:
	$(PYTHON) build/copy-to-dropbox.py

.PHONY: audio-copy-all
audio-copy-all:
	$(PYTHON) build/copy-to-dropbox.py --include-m4b --include-scripts --include-epub

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
	$(PYTHON) build/copy-to-dropbox.py --include-m4b --no-stability-check

# audiobook-deploy-mp3 is the lighter variant: regen MP3s, normalize,
# embed cover, copy. Skip the .m4b rebuild. Useful for iteration on
# individual chapters.
.PHONY: audiobook-deploy-mp3
audiobook-deploy-mp3: audiobook normalize embed-cover
	$(PYTHON) build/copy-to-dropbox.py --no-stability-check

# epub-deploy: regenerate the .epub and copy it to Dropbox. Independent
# of the audiobook pipeline; can run any time the manuscript is updated.
.PHONY: epub-deploy
epub-deploy: epub
	$(PYTHON) build/copy-to-dropbox.py --include-epub --no-stability-check

# book-deploy: ship everything — audiobook (regen + normalize + per-chapter
# cover + .m4b) AND .epub. Canonical "ship the entire book in every
# format" target.
.PHONY: book-deploy
book-deploy: audiobook normalize embed-cover m4b epub
	$(PYTHON) build/copy-to-dropbox.py --include-m4b --include-epub --no-stability-check

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
	$(PYTHON) build/check_audit.py

.PHONY: promote-chapter promote-all promote-reject
promote-chapter:
	$(PYTHON) build/promote.py --chapter $(ch)

promote-all:
	$(PYTHON) build/promote.py --all

promote-reject:
	$(PYTHON) build/promote.py --reject $(ch) --reason "$(reason)"

.PHONY: check-stale
check-stale:
	$(PYTHON) build/check_stale.py
