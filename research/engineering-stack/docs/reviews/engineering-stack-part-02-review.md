# Engineering Stack Part 02: Review Findings

*Phase 4 record for claude/engineering-stack-part-02-evals.md, October 12, 2026, in the finding format of claude/fabel-prompt-audit.md. Evidence class: project review. Three independent checks ran on separate agents (Claude Sonnet), none seeing the others' work or the author's reasoning:*

- *two **blind source checks**, given only the draft's claims and their source links, never the part: 52 claims about papers, statistics and vendor guidance, and 24 about tools and platforms. Together: 74 supported, 2 partly supported, 0 contradicted, 0 unchecked;*
- *a **beginner test** that followed Sections 7 to 9 literally on the Linux test machine, in clean folders, with Python 3.13.16, Ubuntu's 3.12.3 and 3.11.17. Every output the draft showed reproduced, every statistic it quoted matched the tester's own calculation, and it reported 17 problems.*

*Each finding below was checked by the author against the source or by re-running it before being accepted; none was accepted on a checker's word alone. All are fixed in the saved part. After the fixes, `run_lab.py` passed 8 of 8 and `mutation_check.py` 11 of 11 with Python 3.13.16, 3.12.3 and 3.11.17, and `mutation_check.py` behaved as the part describes with `--offline` and with PyPI unreachable.*

**Severity.** Critical: likely to put false content in the final document. High: likely to weaken reliability or safety. Medium: quality and clarity. Low: polish.

### F-01 · High · "Step" meant two different things

- **The draft said:** "Internet access to PyPI for step 7; without it, `python run_lab.py --offline` runs the rest." and "`python run_lab.py` runs steps 1 to 7 on a copy in a temporary folder". Section 7.7: "Step 8 of `run_lab.py` fails". Section 9: "ends with `8 of 8 steps passed.`"
- **What goes wrong:** `run_lab.py` prints eight numbered items, and its item 1 (the statistics) is not one of Section 8's steps, so its items 2 to 8 are Section 8's steps 1 to 7. The PyPI and offline sentences used the two numberings interchangeably, and an offline reader saw `7 of 7` where the text promised `8 of 8`.
- **Why:** The beginner test, problem 1, reproduced by the author: `python run_lab.py --offline` ends with `7 of 7 ... passed.`
- **Fix:** `run_lab.py`'s items are "checks" in the scripts and the text; the part says once that check 1 is the statistics and checks 2 to 8 repeat steps 1 to 7; the offline line and the "you've got it" line give both endings.

### F-02 · High · The promptfoo step never said which folder to run it from

- **The draft said:** "from the lab's `promptfoo` folder ... run the command below", with no `cd` line, while Section 8 said "Run every command from the lab folder".
- **What goes wrong:** Run from the lab folder, promptfoo stops with `Error: No configuration file found at promptfooconfig.yaml. Run "promptfoo init" to create one`, followed by a Node.js stack trace. The suggested `promptfoo init` is the wrong fix.
- **Why:** The beginner test, problem 2; the author reproduced the message.
- **Fix:** The command block starts with `$ cd promptfoo` and is followed by `cd ..`; Section 8 says step 8 runs from that folder; Section 7.7 has a row for the message.

### F-03 · High · The mutation check could report success without testing anything

- **The draft said:** "`python mutation_check.py` ... confirms that exactly the expected steps fail", with no mention of the network.
- **What goes wrong:** M7 and M8 expect check 8 (the pytest check) to fail. When PyPI is unreachable, check 8 fails because pip can't download, so both mutations were reported `OK` and the script ended with `Every mutation behaved as expected.`
- **Why:** The beginner test, problem 4. Reproduced by the author with `PIP_INDEX_URL=http://127.0.0.1:9/simple` [T].
- **Fix:** `mutation_check.py` now looks for `run_lab.py`'s "can't reach PyPI" message and reports those mutations as BAD, with an explanation, and gains `--offline` to skip them; the part says M7 and M8 need PyPI.

### F-04 · Medium · The disk use and the uninstall left about 1 GB out

- **The draft said:** "The first run downloaded 625 packages, about 1.4 GB, into npm's cache"; the uninstall deleted only the `_npx` folder and `~/.promptfoo`.
- **What goes wrong:** npm also keeps a download cache (`_cacache`). After the first run it held about 1 GB more, which the uninstall left behind.
- **Why:** The beginner test, problem 3. Reproduced by the author in an empty npm cache: the first run took 99 seconds and left 1.4 GB in `_npx` and 963 MB in `_cacache`, 2.3 GB in all; `npm cache clean --force` removed `_cacache` and printed `npm warn using --force Recommended protections disabled.` [T].
- **Fix:** Sections 6 and 7.6 give about 2.3 GB; Section 7.8 adds `npm cache clean --force`, its warning line, and the note that it empties npm's cache for every project.

### F-05 · Medium · Two claims went beyond their sources, and four were wider than needed

- **The draft said:** that Farquhar et al. judge entailment with a model "such as DeBERTa-Large-MNLI, or general-purpose LLMs such as GPT-3.5"; that DeepEval's "exact-match, pattern-match and JSON-correctness metrics need no model" and its hosted platform "is optional"; that a comment sits in Anthropic's "example"; the Wilson formula as NIST's; that Panickssery et al. found the self-preference correlation with GPT-4, GPT-3.5 and Llama-2-7b-chat; that Phoenix's licence bars offering it "as a hosted or managed service"; that Ragas "moved" organizations.
- **What goes wrong:** The quotation skipped a clause ("which has been trained to predict entailment"). DeepEval's JSON-correctness metric calls a model to explain a failure unless `include_reason` is off, and its README calls an account "highly recommended". The comment is in Anthropic's LLM-graded examples, not the first snippet. NIST prints each end of the Wilson interval as one fraction. The correlation came from fine-tuning Llama 2 and GPT-3.5; GPT-4 was tested as is. The licence restriction covers a service giving access to "any substantial set of the features". No page says Ragas moved.
- **Why:** The blind source checks, claims A13, A19, A37, A44 (papers) and B17, B18, B19 (tools), each confirmed by the author.
- **Fix:** Each statement now says only what its source says; the Wilson split is marked as an equivalent form, checked numerically [T].

### F-06 · Medium · Privacy facts were incomplete

- **The draft said:** that promptfoo's telemetry covers commands and assertion types; that `--no-write` keeps results out of promptfoo's database; nothing about `results.json`.
- **What goes wrong:** With a cloud login, promptfoo's telemetry also includes the user ID and email address. With `--no-write`, promptfoo still creates an empty database file. `results.json` holds every test case's text.
- **Why:** The blind source check, claim B5 (the telemetry page); the beginner test, problems 11 and 15; the author confirmed an empty database (0 evals, 0 results) with a fresh config folder [T].
- **Fix:** Sections 6 and 7.6 say so, and advise deleting the logs and `results.json` after runs on private data. The part also shows that `PROMPTFOO_CONFIG_DIR` moves all of these files [T].

### F-07 · Medium · Exercise answers that a reader couldn't check, and one wrong sentence

- **The draft said:** for 9 of 10, "nowhere near the 90% you might report"; Exercises 3 and 4 had answers but no command to check them.
- **What goes wrong:** 90% lies inside 59.6% to 98.2%; only the interval's lower end is far from it. Without commands, readers had to find the function names in `evalkit.py`, and a plain `print` shows `0.30000000000000004`.
- **Why:** The beginner test, problems 7 and 8; the author ran each new command [T].
- **Fix:** The sentence is corrected, and each exercise has a check command that prints the stated answer.

### F-08 · Medium · The tutor prompt didn't define b and c

- **The draft said:** "McNemar test: uses only the cases where the two versions differ (b and c)", then asked for a verdict on b = 9 and c = 2.
- **What goes wrong:** Without knowing which version b counts, the final-check question can't be answered from the prompt.
- **Why:** The beginner test, problem 9.
- **Fix:** The FACTS block defines b and c. (With b = 9 and c = 2, the mid-p is 0.039 [T].)

### F-09 · Medium · Printed output differed from the text

- **The draft said:** that promptfoo's output "starts with a table of every ticket"; that `judge_check.py --always-first` "ends with `JUDGE: FAIL`"; that pytest prints `5 passed`; and `48/60 = 80.0%`.
- **What goes wrong:** On a first run npm prints `npm warn deprecated` lines before the table, and the table shows 25 tickets. Two reason lines follow `JUDGE: FAIL`; pytest prints `5 passed in 0.03s`; the accuracy line has extra spaces.
- **Why:** The beginner test, problems 5 and 6; reproduced by the author [T].
- **Fix:** Each sentence now matches the output, and the npm warnings are explained as harmless.

### F-10 · Low · Common errors were missing

- **The draft said:** a 7.7 table without the errors a beginner meets first.
- **What goes wrong:** Running from the wrong folder gives `can't open file ... [Errno 2]`, pytest's `ERROR: file or directory not found` or `No module named 'evalkit'`; half of Exercise 2 gives `invalid choice: 'v3'`.
- **Why:** The beginner test, problem 13; the author captured each message [T].
- **Fix:** Rows for each, with the fix.

### F-11 · Low · The lab's files disagreed with the text

- **The draft's lab said:** `promptfooconfig.yaml` pointed to "Section 8, step 7" and left out `--no-write`; the README pointed to a project path a reader doesn't have, and the part said the README "lists every file".
- **Why:** The beginner test, problem 12.
- **Fix:** The comment, the README and the sentence now agree with the part.

### F-12 · Low · Smaller items

- **The draft said / did:** no word on blocks without `$`; no word on pip's upgrade notice; the `export` lines without saying they last for one window; an uninstall run from inside the folder it deletes; no editor named; step 5 asked for an answer the script prints; the hash row said "download again", although pip may reuse a cached copy; step 2 asked "which of them" without naming the lines.
- **Why:** The beginner test, problems 10, 14, 16 and 17.
- **Fix:** Each corrected.

**Not tested here** (marked [R] or [U] in the part): every Windows and macOS step; the tutor prompt in a live chat; whether `PROMPTFOO_DISABLE_TELEMETRY` stops all network calls (no traffic capture); `promptfoo view`, which needs a browser; a stock Ubuntu without `python3-venv`.
