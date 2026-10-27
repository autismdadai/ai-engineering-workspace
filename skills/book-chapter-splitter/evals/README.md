# Eval pack: book-chapter-splitter

For skill version 1.0. Built 8 October 2026.

## What's here

- `make_fixture.py`: builds the 160-page sample book the tests use. It's written from scratch, so the pack carries nothing from a real book. Its chapter 3 runs 120 pages, page 151 is blank, and PDF page = printed page + 2.
- `test_split_book.py`: 22 known-answer tests of the scripts. They cover the outline and draft plan, page-number offsets, page-by-page identity with the source (checked independently of the script's own check), front pages, the outline and subject line of each file, the 100-page limit and its override, blank-page reporting, and seven inputs that must be refused or flagged: an unsafe file name, a page past the end, a backwards range, a repeated name, overlapping ranges, an encrypted PDF and a file that isn't a PDF.
- `mutation_check.py`: breaks the scripts 15 ways on purpose and checks that a named test catches each break; one harmless change must still pass.
- `evals.json`: the intake answers (drafted, not yet confirmed), 10 requests that should load the skill and 10 that shouldn't, 3 end-to-end tasks, 2 adversarial tasks, and the with-and-without plan.
- `grade_answer.py`: checks an answer against a task; `--self-test` proves each task's checks can fail.

Run the commands from the skill folder. They need Python 3 and pypdf, use no network, and print JSON.

```bash
python evals/test_split_book.py
python evals/mutation_check.py
python evals/grade_answer.py --self-test
```

## Results (8 October 2026, Python 3.13, pypdf 5.9.0)

- Tests: 22 of 22 pass, in about 4 seconds.
- Mutation check: 17 of 17 runs as expected. The first version of the out-of-range test asked for page 999; with the range check broken, the plan was still refused, because 999 pages also broke the 100-page limit. The test now asks for one page past the end, which only the range check can catch.
- The script's own page-text check is tested by fault injection: the test copies the script, makes it copy the next page instead of the planned one, and checks that the report flags the mismatch. Breaking the check makes that test fail.
- Grader self-test: 5 of 5 tasks.
- Real books: the scripts re-made the 11 chapter files that were cut from three textbooks on 8 October with PyMuPDF. Every file had the same page count and the same text on every page, read with PyMuPDF, a different library from the one the skill uses. The books aren't included here.

## Trigger tests

First pass, 8 October 2026, in Claude Code 2.1.294 with `claude plugin eval` (model claude-sonnet-5-5), all four skills loaded together with their long descriptions, one run per request, and no shell tool in the test sessions: 10 of the 10 should-load requests loaded this skill, and 10 of the 10 should-not requests left it off. Not yet run: three runs per request, the short Claude-app description, and the Claude app itself. Details and how to re-run: `claude/trigger-tests-2026-10-08.md`.

## Not run yet

- Trigger tests in the Claude app: install the skill, send each of the 20 requests in a fresh chat, and record whether it loads. In the Claude app the built-in pdf skill also mentions splitting PDFs, so record which skill loads, not just whether this one does.
- With-and-without runs: the plan is under `with_and_without` in `evals.json`. Each helper gets only the sample book, made with `python evals/make_fixture.py sample-book.pdf`.

## Limits

- The sample book is simple: one font, text only, a clean outline. Real books bring ligatures, image-only pages and outlines that skip chapters, which is why the real-book regression matters.
- Text patterns can't judge reasoning. Read borderline answers against each task's rubric.
