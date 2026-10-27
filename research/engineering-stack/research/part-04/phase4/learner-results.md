# Learner test: Part 04, Sections 3 and 7 to 9 (Linux)

Date: 2026-10-13. Tester: a beginner following the text literally on Ubuntu 24.04.5 LTS.
Folder: `/tmp/learner04/ai-stack` (used in place of `~/ai-stack`, as instructed), made fresh; zip unzipped with
`unzip engineering-stack-lab-part-04.zip -d /tmp/learner04/ai-stack`. Tutorial and lab files were not edited
(the Section 8 step 1 edit was made in the unzipped copy, then restored).

## Versions used

| Python | pip | What ran |
|---|---|---|
| 3.13.16 (`python3`, venv `.venv`) | 26.2.1 | All of Section 7.3, 7.4, 7.5, 7.7, every step of Section 8, every exercise in Section 9 |
| 3.12.3 (`/usr/bin/python3.12`, fresh venv) | 24.0 | run_lab.py, mutation_check.py, every demo script (diffed against 3.13), tiktoken install and check |
| 3.11.17 (`/usr/bin/python3.11`, fresh venv) | 24.0 | the same as 3.12 |
| 3.10.20 and 3.14.6 (installed with uv, fresh venvs) | 23.0.1 and 26.1.2 | only to reproduce the Section 7.6 `python_version` row |

## What matched exactly

Every output block in the text was diffed against the real output and matched byte for byte:
Section 3.2 (token_budget part 1), 3.3 (part 2), 3.4 (placement_test), 3.5 (cache_sim A to D),
Section 8 step 3 (cost line), step 4 (cache_cost), step 5 (`--trials 20`: 80% at both ends, 50% at position 6,
intervals 58.4 to 91.9 and 29.9 to 70.1, verdict "no clear position effect"), step 6 (run_lab 13 of 13).
Step 1's edited run printed exactly the `kept:` line the text gives. run_lab.py 13 of 13 and mutation_check.py
"Every mutation behaved as expected." on 3.13.16, 3.12.3 and 3.11.17 (outputs identical apart from the version
line). Exit codes from `echo $?`: 0 on success, 1 on a failed check. Exercises 1 to 3 printed `2`,
`[0, 10000, 10000]` and 4.0. The tiktoken install (`--require-hashes`) succeeded on all three Pythons and the
check failed with the ProxyError line in Section 7.6. 7.7 uninstall worked as written.
Section 3's arithmetic (break-even 0.28 and 1.11, Sonnet totals, Gemini 0.74/2.5/4.0, Liu 22.0 points,
NoLiMa 70.2%, 10,000,000 tokens per minute, 922,000 + 128,000) all agree with the scripts.

## Problems, most serious first

### 1. Section 7.4: "three lines of counts" will not appear from `run_lab.py --with-tiktoken`
- **Text:** "On a normal connection, expect `14 of 14 checks passed.` and three lines of counts, one per sample text [R]."
- **What happens:** `run_lab.py` keeps only the *last* line of the optional script's output
  (`optional()` returns `text.strip().splitlines()[-1]`). With a stub tiktoken that loads (to simulate a working
  connection), run_lab printed:
  ```
  [PASS] check 14: tiktoken_counts: PASS  tiktoken counted every sample
  14 of 14 checks passed.
  ```
  The three count lines appear only when `python optional_tiktoken_check.py` is run directly.
- **Fix:** add `python optional_tiktoken_check.py` to 7.4 and say the counts come from it, or make run_lab print the
  script's full output for check 14.

### 2. Section 3.1 / 3.2: a 0.3 margin is not what "30% more tokens" works out to, and the worked example's conclusion depends on it
- **Text (3.1):** margin "0.3 when moving to a tokenizer that gives about 30% more tokens". (3.2): "With a 30% margin for a
  newer tokenizer, the budget shrinks to 610,400 and the handbook goes too."
- **What the arithmetic says:** if every count is 1.3 times higher, the plan that keeps contract and handbook needs
  1.3 x 658,200 = 855,660 tokens, which still fits in 872,000. The matching margin is 1 - 1/1.3 = 0.231, and with it
  the plan drops only the email thread:
  ```
  contract+handbook+must at 1.3x: 855660 vs budget 872,000
  margin equivalent to 30% more tokens: 0.2308
  dropped with that margin: ['email']
  dropped when counts really are 30% higher: ['email'] 855660
  ```
  So "the handbook goes too" comes from over-correcting, not from the new tokenizer.
- **Fix:** either use margin 0.23 ("30% more tokens means shrinking the budget to 1/1.3, about 77%") and change the
  example, or keep 0.3 and call it a generous safety margin, not the equivalent of 30% more tokens.

### 3. Section 3.2 step 3 says "until the next piece wouldn't fit", but the code skips that piece and keeps going; Section 8 step 1 shows the difference without explaining it
- **Text (3.2, step 3):** "Add the rest in order of priority, until the next piece wouldn't fit."
- **Code:** `plan_context` goes through every piece and adds any later, smaller one that still fits.
- **Where a reader sees it:** after Section 8 step 1's edit (email priority 9), the margin line reads
  ```
     with a 30% margin for a newer tokenizer, dropped: contract.pdf as text
  ```
  so the priority-5 contract is dropped while the priority-3 handbook is kept. Read by step 3's wording, both would
  go. The text quotes only the `kept:` line of that run.
- **Also:** step 1 never says to set the priority back to 1, so a later rerun of `token_budget.py` no longer matches
  Section 3.2 (run_lab and mutation_check still pass with the edit).
- **Fix:** reword step 3 ("add each remaining piece, highest priority first, if it still fits; skip it if not"),
  show and explain the margin line in step 1, and add "then change it back to 1".

### 4. Section 7.6 row 1: the wrong-folder error a reader actually gets is different
- **Text:** `ModuleNotFoundError: No module named 'cache_sim'` means the terminal isn't in the lab folder.
- **What happens** from `/tmp/learner04/ai-stack` (one level up):
  ```
  $ python run_lab.py
  python: can't open file '/tmp/learner04/ai-stack/run_lab.py': [Errno 2] No such file or directory
  $ echo $?
  2
  $ python -c "from cache_cost import *; ..."     (exercise 1)
  ModuleNotFoundError: No module named 'cache_cost'
  $ python -c "from cache_sim import *; ..."      (exercise 2)
  ModuleNotFoundError: No module named 'cache_sim'
  ```
  `python engineering-stack-lab-part-04/run_lab.py` from the parent folder works (13 of 13).
  The `cache_sim` message only comes from the exercise 2 one-liner.
- **Also:** 7.5 says the exit code is 0 or 1; this case gives 2 (and a Python traceback also gives 1).
- **Fix:** add a row for `can't open file ... No such file or directory`, write row 1 as
  `ModuleNotFoundError: No module named 'cache_sim'` (or `'cache_cost'`) "from the Section 9 one-liners", and say
  "0 means every check passed; anything else means something failed".

### 5. Section 7 "Before you start": the Linux unzip command
- **Text:** `unzip engineering-stack-lab-part-04.zip -d ~/ai-stack` [T on Linux].
- **Issue:** it worked here (unzip is installed on this image), but Part 01 Section 7 deliberately uses
  `python3 -m zipfile -e ... .` and its beginner test listed "missing unzip" as a fix. A stock or minimal Ubuntu
  without unzip gets "Command 'unzip' not found". The text also doesn't say to run the command in the folder that
  holds the zip (for example `~/Downloads`).
- **Tested alternative:** `python3 -m zipfile -e engineering-stack-lab-part-04.zip ~/ai-stack` gives the same
  `engineering-stack-lab-part-04` folder.
- **Fix:** use the zipfile form (as Part 01 does), or add `sudo apt install unzip`, and add "in the folder where you
  downloaded the zip".

### 6. `run_lab.py --with-tiktoken` before installing: FAIL that says SKIP (not in Section 7.6)
- **What happens:**
  ```
  [FAIL] check 14: tiktoken_counts: SKIP  tiktoken is not installed (see the install line at the top)
  13 of 14 checks passed.
  ```
  (exit 1). "FAIL" and "SKIP" on one line is confusing, and "the install line at the top" refers to the top of
  `optional_tiktoken_check.py`, a file the reader hasn't opened.
- **Fix:** add a 7.6 row ("tiktoken isn't installed in this environment; run the pip line in 7.4 first"), or make
  the optional script say "run: python -m pip install --require-hashes -r requirements-optional.txt".

### 7. Section 3.5: "one 8,000-token document", but every line shows 10,000
- **Text:** "A chat about one 8,000-token document, with the breakpoint after the document", followed by
  `'cache_creation_input_tokens': 10000` and `'cache_read_input_tokens': 10000`.
- **Why:** the cached prefix is tools (400) + system prompt (1,600) + document (8,000) = 10,000. The text doesn't say
  so, and doesn't explain `input_tokens` 50, 400, 750 (the growing chat after the breakpoint: 50 per question,
  300 per answer). A beginner checking the numbers gets stuck here.
- **Fix:** one sentence: "The cached prefix is 10,000 tokens: a 400-token tool definition, a 1,600-token system prompt
  and the 8,000-token document. `input_tokens` is the chat after the breakpoint, which grows each turn."

### 8. `paper_numbers.py` (Section 7.5 tour): no expected output, and its indices are 0-based
- **What it prints:**
  ```
  Liu et al., GPT-3.5-Turbo, 20 documents: {'edge_minus_worst_middle': 22.0, 'middle_below_closed_book': [9, 14], 'best_below_oracle': 12.5}
  NoLiMa, GPT-4o at 32K as a share of its base score: 70.2 %
  GPT-6 Astra input plus output equals the context window: True
  Anthropic example, input tokens per minute at an 80% hit rate: 10,000,000
  Lumer et al. table's lowest results fall below the abstract's ranges: True
  ```
  Section 3.4 says the 10th and 15th positions scored below closed-book; the script prints `[9, 14]` (0-based).
  `best_below_oracle 12.5` isn't mentioned in the text. No section shows this output.
- **Fix:** show the output in 7.5 or Section 8 and note "positions counted from 0", or print 1-based positions.

### 9. Section 8 step 7 and Section 7.6 (Ollama): what the reader actually sees
- Without Ollama: the 7.6 message is correct, but it is the last line of a **65-line traceback** (starting with
  `ConnectionRefusedError: [Errno 111] Connection refused`). The text shows only the last line.
- The 7.5 tour suggests `python placement_test.py --ollama MODEL` alone. `--trials` defaults to 200 in that mode too,
  so that is 5 x 200 = 1,000 model calls; only Section 8 step 7 adds `--trials 10`.
- Argument parsing works: `--ollama` with no name gives `error: argument --ollama: expected one argument`;
  `--num-ctx abc` gives `invalid int value: 'abc'`. `--help` lists the options with no descriptions.
- Against a fake local server on port 11434 (my stand-in, not Ollama) the run printed a header line
  `Local model fake, 200 documents, num_ctx 16384`, five accuracy lines and a verdict; when the fake server reported
  `prompt_eval_count` equal to `num_ctx`, it stopped with `RuntimeError: prompt filled the context; raise num_ctx`
  (matching the 7.6 row), again at the end of a traceback, with no partial results.
- The "about 34 tokens" per document checked out: 34.17 average by the 4-characters rule; 200 documents plus the
  question come to about 6,810 tokens.
- **Fix:** in 7.6 say "the last line of a long error message"; in the 7.5 tour write `--ollama MODEL --trials 10`;
  in step 7 say "a header line, five lines of accuracy and a verdict".

### 10. Terms used in Section 3 and never defined
- "needle", "needle test" and "needles" (3.4, RULER/NoLiMa/Chroma bullets and Google's quote) are never explained.
  The placement test is a needle test, but the text never says so.
- `prompt_eval_count` (3.3, and what the script checks) isn't explained: it's Ollama's count of the prompt tokens it
  processed.
- **Fix:** "a needle test hides one fact (the needle) in long filler text and asks for it"; gloss
  `prompt_eval_count` once.

### 11. Section 3.3 versus placement_test.py (Ollama)
- 3.3's Ollama row describes **chat** requests ("For chat requests, truncation is on by default") and says you'd
  notice "only by comparing `prompt_eval_count` with what you sent". The script calls `/api/generate` (not chat) and
  compares `prompt_eval_count` with `num_ctx`, not with the prompt's size. That's not wrong, but a reader checking 3.3
  against the code will find two different things.
- **Fix:** one line in step 7: "the script uses Ollama's generate endpoint and stops if the prompt filled `num_ctx`".

### 12. Section 7.6 row 3 points to the wrong Part 01 section
- **Text:** "Make the environment with Python 3.13 (Part 01, Section 6)". In Part 01, Section 6 is "What you need"
  (why 3.13); installing 3.13 and making the environment is Section 7 (7.1 `py install 3.13`, 7.2, 7.3).
- Reproduced the row itself: `[FAIL] check 1: python_version: 3.10.20` and `... 3.14.6`, `12 of 13 checks passed.`, exit 1.
- **Fix:** "(Part 01, Section 7)".

### 13. Output blocks that show only part of the output, unmarked
- 3.2's block starts `$ python token_budget.py` but shows only part 1; part 2 prints too (it's shown in 3.3 without
  the command). 3.5's `$ python cache_sim.py` block shows A and B; C, D and the cost lines follow. A literal reader
  sees more than shown.
- **Fix:** add "(first part of the output)" or drop the `$` line from the partial blocks.

### 14. Section 7.7 [U] can be settled from the installed source
- **Text:** tiktoken's cache folder is "set by `TIKTOKEN_CACHE_DIR`, otherwise a temporary folder [U: tiktoken's source]".
- **tiktoken 0.14.0 `tiktoken/load.py`:** `TIKTOKEN_CACHE_DIR`, else `DATA_GYM_CACHE_DIR`, else
  `os.path.join(tempfile.gettempdir(), "data-gym-cache")` (`/tmp/data-gym-cache` on Linux).
- **Fix:** replace the [U] with that (tag [T: read from the installed 0.14.0 source]).

### 15. Small things
- `cache_cost.py` prints `Lower read rates (0.05x, 0.025x) don't change these counts: 2 2`. The two numbers are
  unlabelled and test only the 1-hour cache (2x write); the 5-minute case at lower rates isn't printed. Text 3.6
  says "those counts" (plural). Suggest labelling: `1-hour at 0.05x: 2, at 0.025x: 2`.
- On Python 3.11 and 3.12 (pip 24.0) the tiktoken install ends with `[notice] A new release of pip is available:
  24.0 -> 26.2.1`. Harmless, but a beginner may think it's an error; one line in 7.4 would help.
- 3.1 calls about 30 percent more tokens "a third more"; learning objective 1 repeats "a third". 30% is not a third.
- Section 7.4 says pip "installed cleanly"; here pip showed `Using cached` because of an earlier download; a fresh
  machine shows `Downloading`. No change needed.

### Not Linux, noticed in passing (not tested)
- 7.2 (macOS) uses `python3 -m venv`; Part 01's macOS steps use `python3.13`. On a Mac whose `python3` is 3.14,
  check 1 fails. Suggest `python3.13 -m venv .venv`.
- 7.1 (Windows): "Extract All" proposes a destination folder named after the zip, so the default result is
  `...\engineering-stack-lab-part-04\engineering-stack-lab-part-04`, and the `cd` line won't match unless the reader
  picks `ai-stack` as the destination. [Unverified here: no Windows machine.]
