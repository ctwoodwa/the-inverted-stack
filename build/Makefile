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
	$(CHAPTERS_DIR)/appendices/appendix-d-testing-the-inverted-stack.md

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

.PHONY: draft-pdf
draft-pdf: $(OUT_DIR)
	$(PANDOC) $(CHAPTER_FILES) \
		--from markdown \
		--to pdf \
		--pdf-engine=xelatex \
		--metadata title="The Inverted Stack: Local-First Nodes in a SaaS World" \
		--metadata author="Chris Woodward" \
		--output $(OUT_DIR)/draft.pdf
	@echo "Draft PDF written to $(OUT_DIR)/draft.pdf"

.PHONY: epub
epub: $(OUT_DIR)
	$(PANDOC) $(CHAPTER_FILES) \
		--from markdown \
		--to epub \
		--metadata title="The Inverted Stack: Local-First Nodes in a SaaS World" \
		--metadata author="Chris Woodward" \
		--output $(OUT_DIR)/the-inverted-stack.epub
	@echo "ePub written to $(OUT_DIR)/the-inverted-stack.epub"

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

.PHONY: clean
clean:
	rm -rf $(OUT_DIR)
