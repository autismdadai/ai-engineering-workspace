---
name: book-chapter-splitter
description: >
  Splits a long PDF (a textbook, manual, course notes or report) into one file per
  chapter, copies the book's title or license pages to the front of each file, and
  checks every output page against the original. Use when someone wants chapters cut
  out of a PDF, wants files under 100 pages so Claude reads page images as well as
  text, needs to find where chapters start or how printed page numbers map to PDF
  pages, or wants chapter files checked against the book. Do not use to edit, OCR,
  summarize, translate, compress or merge PDFs, or to split a PDF into single pages.
license: MIT
metadata:
  version: "1.0"
  requires: "python3, pypdf"
  claude-app-description: "Splits a PDF book into checked chapter files under 100 pages, title or license pages kept at the front; finds chapter starts and page offsets. Not for editing, OCR, summarizing or merging PDFs."
---
## Canonical instructions

This is a Codex discovery entry. Read and follow the full [canonical skill](../../../skills/book-chapter-splitter/SKILL.md). Resolve any scripts, references, and assets relative to that canonical skill's directory. If it names a host tool that is unavailable in this session, say so and use the documented fallback where possible. Keep the canonical source in its original project folder; this entry only exposes it to Codex.
