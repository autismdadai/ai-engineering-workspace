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

# Book chapter splitter

Cut chapters out of a PDF with the scripts, and report only what their checks confirm. Page ranges worked out by eye are where off-by-one errors, missing pages and stray blank pages come from; the scripts read the book's outline and page text instead.

## Steps

1. Check pypdf once: `python3 -c "import pypdf"`. If that fails, run `pip install pypdf`.
2. Read the outline and write a draft plan:
   `python3 scripts/inspect_pdf.py outline book.pdf --plan-out plan.json`
   It prints the page count, the outline entries with their PDF pages, and a draft with one chapter per top-level entry. If the chapters sit one level down (under "Part" entries), add `--level 2`. If the book has no outline, find the chapter openings with step 3 and write the plan by hand.
3. Look at the pages around each chapter start, and at the first pages of the book:
   `python3 scripts/inspect_pdf.py heads book.pdf --pages 1-12`
   Use it to confirm where each chapter opens, to pick front pages worth copying (the title page and the copyright or license page), and to read `likely_offset`: the PDF page minus the printed page number.
4. Edit plan.json (format below). Keep only the chapters wanted. End each chapter on its last page of text, leaving out blank pages and the next chapter's opener. Put a phrase from the chapter's first page in `expect_first`.
5. Split and check:
   `python3 scripts/split_book.py plan.json book.pdf out/`
   Nothing is written if the plan has a page outside the book, a range that runs backwards, an unsafe or repeated file name, or a file over 100 pages (front pages included).
6. Read the JSON. Every file needs `ok: true`, which means the right page count, an empty `text_mismatch_pages` and `first_heading_found` true. Then read each `next_page_head`: it should be the next chapter's opening or a blank page. Anything else means the range is wrong.
7. If you can view PDF pages, look at each file's first chapter page and its last page. It confirms the opener and catches a stray blank or next-chapter page the text checks can't see on a scanned book.
8. Report a table: file, chapter, PDF pages, printed pages, page count and size. Then list any warnings, any chapter you split into parts, and anything left unchecked.

## The plan

```json
{"book_title": "Trigonometry", "front": [3, 4], "front_label": "Acknowledgements and license pages",
 "printed_offset": null,
 "chapters": [{"file": "trig-ch01-foundations.pdf", "title": "Chapter 1: Foundations of Trigonometry",
               "first": 7, "last": 100, "expect_first": "FOUNDATIONS OF TRIGONOMETRY"}]}
```

- Pages are PDF pages counted from 1, not printed page numbers. When a book numbers its pages consistently, printed page = PDF page − `printed_offset`. The offset is optional and only labels the report and each file's subject line.
- `front` pages go at the start of every file, in the order given.
- File names use lowercase letters, digits and hyphens and end in .pdf, such as `book-ch03-identities.pdf`. The script refuses folders in names, so a plan can't write outside `out/`.

## Decisions

- **Over 100 pages.** The Claude Help Center says Claude reads the images and charts in PDFs of 100 pages or fewer, but only the text of longer ones. Split a long chapter at a section start from the outline into `-part1` and `-part2` files. Raise `--max-pages` only if the person says text-only reading is fine.
- **Front pages.** Keep one or two pages that name the book and its license. Skip a cover that is only an image: it adds size and no text.
- **Scanned books.** When `pages_without_text` is high, the page-text check can't tell pages apart. Look at the pages instead (step 7), and say the text check didn't apply.
- **Project space.** In one project, chapter files used about twice the knowledge space per page that the whole books did (references/planning.md), so split only the chapters the work needs.

## Limits

- The scripts copy pages unchanged. They don't fix formulas that come out garbled as text, and they don't OCR scans. For a garbled formula, the page image or the printed book is the reference.
- An encrypted PDF is refused; ask for an unlocked copy.
- The files are copies of the book's pages, so the book's license still covers them.

## Reference

`references/planning.md` has a worked example (three textbooks cut to 11 chapter files in October 2026), how to read printed page numbers and offsets, what the checks caught, and how much project space the chapter files used. Read it when planning a split for a new book or when a check fails.
