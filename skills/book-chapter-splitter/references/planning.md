# Planning a split

## Worked example (October 2026)

Three reference books for a Claude Project: a quantum mechanics textbook (Binney and Skinner), physics course notes (UCSD Physics 130) and an open trigonometry textbook (Utah, CC BY-NC-SA 3.0). Together they ran to 1,321 pages. They were cut to the 11 chapters the project's skills use: 478 pages, front pages included.

| Book | Printed page numbers | Front pages copied | Chapters kept |
|---|---|---|---|
| Binney and Skinner | printed = PDF page − 8 | title and copyright (PDF 1–2) | 1, 2, 6, 7 |
| UCSD 130 notes | printed = PDF page | title page (PDF 1) | 18, 21 |
| Trigonometry v2 | page codes such as T3-19, not plain numbers | acknowledgements and license (PDF 3–4) | 1, 3, 5, 6, 7 |

What the checks caught:

- Trigonometry chapters 3 and 7 each ended on a blank page. The page after the planned range showed no text, and the next chapter began one page later, so each range was ended before the blank page.
- The trigonometry cover was a large image whose text came out garbled, so the license pages became the front pages instead.
- Every file's text matched the book page for page. This was checked with two different PDF libraries (pypdf, which the skill uses, and PyMuPDF).

## Printed page numbers and offsets

- `heads` lists numbers found in the first two and last two lines of each page. `likely_offset` is the most common value of PDF page minus that number.
- Check the offset on pages far apart. Books often restart numbering after the front matter, use roman numerals there, or print codes such as T3-19 instead of numbers.
- A chapter's first page often carries its number alone at the bottom, while other pages carry it in the running head.
- Text extraction can join letters into ligatures ("ﬁelds" for "fields"). If `first_heading_found` is false for a heading you can see on the page, try a shorter `expect_first` phrase without "fi" or "fl".

## When a check fails

- `text_mismatch_pages` isn't empty: the file doesn't hold the pages the plan names. Run the split again. If it persists, the PDF may be damaged; say so rather than reporting success.
- `first_heading_found` is false: the range starts on the wrong page, or the phrase doesn't match the page's extracted text. Check with `heads`.
- `next_page_head` shows more of this chapter: the range ends too early. It shows the next chapter's text halfway down a page: the chapter ends mid-page, so that page belongs to both. Keep it in the earlier chapter and say so.

## The 100-page line

The Claude Help Center says Claude reads the images and charts in PDFs of 100 pages or fewer, but only the text of longer ones. For project files it says text extraction only, except for "multimodal PDFs", which it doesn't define. Source: "Upload files to Claude", https://support.claude.com/en/articles/8241126-upload-files-to-claude (checked October 8, 2026). Menus and limits change, so check the page when it matters.

## Project space (one project's measurements)

The Projects tool reports a knowledge size against a maximum of 2,000,000; its units aren't documented. In one project on October 8, 2026:

- the three whole books added 834,669 units for 1,321 pages, about 630 per page;
- ten chapter files added 552,678 units for 427 pages (front pages included), about 1,290 per page.

That is one project and one set of books. Treat the figures as a rough guide to how much space a split will take, not as a rule.
