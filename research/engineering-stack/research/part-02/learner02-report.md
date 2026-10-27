# FINAL REPORT: learner 02, Part 02 Sections 7 to 9 (draft under test)

Test date 2026-10-12. Ubuntu 24.04.5, HOME=/root. Runs: `run313` (Python 3.13.16, full run), `run312` (Ubuntu's Python 3.12.3, Sections 7.3, 7.4, 8 steps 1 to 7, plus the mutation check), and an extra `run311` (Python 3.11.17, not requested). Everything below was run literally; where the text was ambiguous I say which reading I tried. Part 01, Section 3.7, Section 5 and the appendix were not in my materials.

## 1. Problems, most serious first

**1. [High] "Step" means two different things, and the PyPI and offline sentences use the wrong one.** Section 8 "Prerequisites", Section 8 "The automated check", 7.7 row 3, and "You've got it when" in Section 9.
- Text: "Internet access to PyPI for step 7; without it, `python run_lab.py --offline` runs the rest." / "`python run_lab.py` runs steps 1 to 7 on a copy in a temporary folder" / 7.7: "Step 8 of `run_lab.py` fails and suggests `--offline`" and "`python run_lab.py --offline` runs steps 1 to 7" / "ends with `8 of 8 steps passed.`"
- What happens: `run_lab.py` prints 8 numbered checks. Its check 1 (statistics) is not one of Section 8's steps, so its checks 2 to 8 are Section 8's steps 1 to 7. The only check that needs PyPI is its 8 (the pytest one); Section 8's own step 7 downloads nothing, because pytest was installed in Section 7. So "PyPI for step 7" is wrong in Section 8's numbering, and "runs steps 1 to 7" is wrong in `run_lab.py`'s numbering (it runs 8). With `--offline`: `SKIP  8. pytest step (--offline)` and the last line is `7 of 7 steps passed.` (exit 0), which never matches "ends with `8 of 8 steps passed.`". The mutation lines (`failed steps ['3.', '8.']`) also use `run_lab.py`'s numbers.
- Why it misleads: an offline reader cannot map these sentences to what is printed, and sees 7 of 7 where the text promised 8 of 8.
- Fix: call `run_lab.py`'s items "checks" (or print `Check 1 of 8`), say once that check 1 is the statistics and checks 2 to 8 are Section 8's steps 1 to 7; write "Internet access to PyPI for check 8 of `run_lab.py`"; and add "(or `7 of 7 steps passed.` with `--offline`)" to the "You've got it" line.

**2. [High] 7.6 never says `cd promptfoo`, and Section 8 says "Run every command from the lab folder"; the wrong-folder error is a raw Node stack trace and is not in 7.7.** 7.6, Section 8 intro and step 8.
- Text: "from the lab's `promptfoo` folder, with the lab's virtual environment still active, run the command below" (no `cd` line). Section 8: "Run every command from the lab folder"; step 8: "Optional: the same eval in promptfoo (Section 7.6)".
- Happens when run from the lab folder: `file:///home/claude/.npm/_npx/70ae47b8681aab87/node_modules/promptfoo/dist/src/main.js:2535` then `Error: No configuration file found at promptfooconfig.yaml. Run "promptfoo init" to create one or pass --config path/to/promptfooconfig.yaml.`, then about eight `at ...` lines and `Node.js v22.22.0` (exit 1).
- Why: the error tells a beginner to run `promptfoo init`, which is the wrong fix. After a successful run the reader is also left inside `promptfoo/` while the rest of the text assumes the lab folder.
- Fix: put `cd promptfoo` first in the 7.6 block and `cd ..` after it; make Section 8's sentence say "except step 8"; add a 7.7 row for `No configuration file found at promptfooconfig.yaml` ("you are not in the `promptfoo` folder").

**3. [Medium] The size claim and the uninstall leave about 1 GB behind.** 7.6 ("downloaded 625 packages, about 1.4 GB, into npm's cache and took about a minute") and 7.8 ("delete the `_npx` folder ... (1.4 GB ...)").
- Measured on a true first run (I had set aside both `_npx` and npm's old `_cacache`): 1 min 37 s; npm's debug log shows 624 tarball downloads (close to 625); `_npx` = 1.4G, and npm's separate download cache `_cacache` = 963M. 7.8 never touches `_cacache`: it measured 963M just before I did what 7.8 says (`rm -rf` of `_npx` and `~/.promptfoo`), and the folder was still there afterwards.
- Why: a reader who follows 7.8 to get the space back recovers about 60 percent of it, and nothing tells them the rest exists.
- Fix: say "about 2.4 GB: 1.4 GB in `_npx` plus about 1 GB in `_cacache`" and add `npm cache clean --force` to 7.8. I ran it: it removed `_cacache` (exit 0) and printed `npm warn using --force Recommended protections disabled.` (mention that line so it does not alarm; note that it empties npm's cache for every project).

**4. [Medium] `python mutation_check.py` gives false reassurance when PyPI is unreachable, and Section 8 does not say it needs PyPI.** Section 8, "Proof that the checks can fail".
- Text: "confirms that exactly the expected steps fail" and shows `Every mutation behaved as expected.` Nothing about the network (the script's own docstring says M7 and M8 download pytest).
- Happens with PyPI unreachable (`PIP_INDEX_URL=http://127.0.0.1:9/simple PIP_RETRIES=0 python mutation_check.py`): all 11 lines say `OK`, last line `Every mutation behaved as expected.`, exit 0, 11 s. M7 and M8 expect step 8 to fail anyway, so a step 8 that fails only because pip could not download counts as the expected result.
- Why: an offline learner is told two of the proofs hold when step 8's part was never tested.
- Fix: in the text, "M7 and M8 need PyPI"; in the script, make M7 and M8 check first that step 8 passes on the unmutated copy (or print `M7/M8 skipped: pip could not reach PyPI`), and/or add an `--offline` flag that skips them and says so.

**5. [Medium] The first promptfoo run looks different from the text: two warning lines, and the table is not "every ticket".** 7.6.
- Text: "The output starts with a table of every ticket and both routers' answers"; the block starts at `Cache is disabled.`
- Happens on the first run (npx installing):
  ```
  npm warn deprecated node-domexception@1.0.0: Use your platform's native DOMException instead
  npm warn deprecated @modelcontextprotocol/server-filesystem@2026.8.31: Date-based versions are no longer published. This package has resumed semantic versioning at 1.0.0: install the latest version.
  Cache is disabled.
  ```
  The table shows 25 rows, then `... 35 more rows not shown ...` (the text's own block shows the cut, which contradicts "every ticket"). Later runs have no warnings. From `Cache is disabled.` down to `Duration: 1s (concurrency: 4)` my first run matched the text exactly (only the eval id differs).
- Why: "npm warn deprecated" on the first run looks like a failure to a beginner.
- Fix: add one sentence ("on the first run npm may print `npm warn deprecated` lines; they are harmless") and say "a table of the first 25 tickets".

**6. [Medium] Three literal mismatches between "ends with" / quoted lines and the real output.**
- Section 8 step 6: "`python judge_check.py --always-first` ... ends with `JUDGE: FAIL`". Real output continues after it: `JUDGE: FAIL`, `  - consistency 0.0% is below 80%`, `  - kappa 0.000 is below 0.60`. (0.0% and 0.000 are correct.)
- 7.4: "`python -m pytest -q test_evals.py` should end with `5 passed`". Real last line: `5 passed in 0.03s`.
- Section 8 step 1: `48/60 = 80.0%`. Real: `v1  48/60 =  80.0%   68.2% to 88.2%` (two spaces after `=`, right-aligned).
- Why: a careful beginner comparing literally may think the run is off.
- Fix: "prints `JUDGE: FAIL` followed by two reasons"; "ends with a line that starts `5 passed`"; "`48/60`, `80.0%`".

**7. [Medium] Section 9, Exercise 1: "nowhere near the 90% you might report" is wrong as written, and the check prints decimals.**
- Text: answer "59.6% to 98.2%"; "The interval is wide, and nowhere near the 90% you might report."
- Happens: the command prints `(0.5958499732047615, 0.9821237869049271)`. The numbers match the stated answer, but 90% lies inside 59.6% to 98.2%, so "nowhere near" is false; the lower end is what is far from 90%.
- Fix: "its lower end, 59.6%, is far below the 90% you might report"; tell the reader the command prints proportions, or use `python -c "import evalkit; lo, hi = evalkit.wilson_interval(9, 10); print(f'{lo:.1%} to {hi:.1%}')"` (prints `59.6% to 98.2%`; checked on Linux, PowerShell quoting not tested).

**8. [Medium] Section 9, Exercises 3 and 4 give no command to check the stated answers, and the function names are not in the README.**
- Text: Exercise 1 has a check command; Exercises 3 and 4 give an answer tagged [T] and nothing to run.
- Happens: the answers are right (pass@1 0.300, pass@5 0.917, 1 - 0.7^5 = 0.832; kappa 0.80 for 20 answers, 10 yes each, 18 agreements), but only if you find `evalkit.pass_at_k(n, c, k)` and `evalkit.cohen_kappa(list_a, list_b)` by reading `evalkit.py`. A plain `print` gives `0.30000000000000004 0.9166666666666666`, which looks wrong next to "0.300 and 0.917".
- Fix: give the commands, for example `python -c "import evalkit; print(f'{evalkit.pass_at_k(10, 3, 1):.3f} {evalkit.pass_at_k(10, 3, 5):.3f}')"` (prints `0.300 0.917`, checked) and `python -c "import evalkit; a = [1]*10 + [0]*10; b = [1]*9 + [0, 1] + [0]*9; print(evalkit.cohen_kappa(a, b))"` (prints `0.8`, checked). Add "run from the lab folder" (outside it: `ModuleNotFoundError: No module named 'evalkit'`).

**9. [Medium] The tutor prompt never defines b and c, so FINAL CHECK 2 cannot be answered from it.**
- Text: FACTS: "McNemar test: uses only the cases where the two versions differ (b and c) ... b=6, c=4 gives mid-p 0.549." FINAL CHECK 2: "Given b=9 and c=2, say whether the second version is worse, using the mid-p."
- Happens: which version b and c belong to is defined only in `evalkit.mcnemar`'s docstring (b = only the first system right, c = only the second). I computed `mcnemar(9, 2)`: exact 0.065, mid-p 0.039, so with b = only version 1 right, "yes, version 2 is worse at 0.05". The other numbers in FACTS and in the answers check out (Wilson 48/60, 12/15, 45/50 = 78.6% to 95.7%; kappa; 77.4% to 82.4% on 960).
- Fix: add "b = cases only the first version gets right, c = only the second" to FACTS. I could not run the prompt itself (no model).

**10. [Low] The pip upgrade notice is not shown, and appears for some readers.** 7.3.
- Text: the install "prints" three lines ending `Successfully installed iniconfig-2.3.1 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-9.1.1`.
- Happens: those lines matched exactly on 3.13 and 3.12. In a Python 3.11.17 venv (pip 24.0 from `ensurepip`) the output ends with a blank line, `[notice] A new release of pip is available: 24.0 -> 26.2.1` and `[notice] To update, run: pip install --upgrade pip`. Ubuntu's own 3.12 pip prints no notice.
- Fix: one sentence: "You may also see a `[notice] A new release of pip` line; ignore it."

**11. [Low] `--no-write` still creates `~/.promptfoo/promptfoo.db`.** 7.6.
- Text: "`--no-write` keeps the results out of promptfoo's local database ... Even so, promptfoo created `~/.promptfoo` with a small config file holding a random id, and every run wrote a debug log".
- Happens: after a first run `~/.promptfoo` held `promptfoo.yaml` (`id: 9d920bdc-3c4b-4fb5-9046-071f9fb42ea8`), `logs/` (481,662-byte debug log, ticket text inside; empty error log) and also `promptfoo.db` (352,256 bytes). The database is empty (0 rows in `evals` and `eval_results`, no ticket text), so the claim itself holds.
- Why: someone who looks in the folder sees a database file and wonders whether results were stored.
- Fix: add "and an empty `promptfoo.db`".

**12. [Low] Lab files disagree with the tutorial.**
- `promptfoo/promptfooconfig.yaml` line 2: "From this folder (Part 02, Section 8, step 7)". The tutorial puts it in 7.6 and Section 8 step 8, and the YAML's example command lacks `--no-write`.
- `README.md` opens with "claude/engineering-stack-part-02-evals.md in the 'Prompting' project", which a reader does not have.
- 7.5: "The README in the zip lists every file." It does not list `.gitignore`, `promptfoo/bridge.py` or `promptfoo/promptfooconfig.yaml` individually.
- Fix: correct the comment (step 8 / Section 7.6, add `--no-write`), drop the project path, say "lists the files".

**13. [Low] 7.7 lacks the errors a beginner is most likely to meet.** All reproduced:
- Wrong folder: `python: can't open file '<cwd>/run_eval.py': [Errno 2] No such file or directory` (exit 2); `python -m pytest -q test_evals.py` gives `no tests ran in 0.00s` and `ERROR: file or directory not found: test_evals.py` (exit 4); `python -c "import evalkit ..."` gives `ModuleNotFoundError: No module named 'evalkit'`.
- Exercise 2 half done: after editing only `router.py`, `python run_eval.py --candidate v3` prints `run_eval.py: error: argument --candidate: invalid choice: 'v3' (choose from 'v1', 'v2')` (exit 2). This one is clear, so only a row is needed.
- The promptfoo `No configuration file found` error (item 2).

**14. [Low] Section 8 step 2: "Read the paired line before the per-label lines, and ask which of them you would have trusted".** The output prints a per-label table (`v2 by label`) above the paired line and a second per-label block (`Recall by label, v1 to v2`) below it, so reading "before" means scrolling up. "which of them" is unclear. Fix: name the two lines (the `only v1 right: 6 ... McNemar mid-p 0.549` line and the `account 85.7% to 42.9%   paired mid-p 0.016` line). Also "the account line shown in Section 5" could not be compared.

**15. [Low] "Per-router counts" shows no output, and `-o` leaves files.** 7.6.
- The text says it "prints 48 passes and 12 failures for router-v1, and 46 and 14 for router-v2". Real output: `Counter({('router-v1', True): 48, ('router-v2', True): 46, ('router-v2', False): 14, ('router-v1', False): 12})`. Numbers right; the reader has to know True = pass and the order is not grouped.
- `-o results.json` leaves a 340 KB `results.json` (all ticket text) and `__pycache__` in `promptfoo/`; the text warns only about the logs.
- Fix: show the line and say "True means pass"; add results.json to the "after a run on private data, delete" advice.

**16. [Low] The code-block convention is not followed.** Line 3: "a line starting with `$ ` is a command; the lines after it are what the computer printed." The 7.1 and 7.2 blocks, and step 4's JSON line, show commands without `$ `. A reader cannot tell them from output. Fix: say "blocks without `$ ` are commands only (or data to paste)".

**17. [Low] Small things.**
- 7.6: the `export` line affects only that terminal window; a new window turns telemetry back on. Say "in the same window".
- 7.3: "The same commands as macOS" includes `cd ~/ai-stack/part-02-evals`; fine only if Part 01 created `~/ai-stack`.
- 7.8: `rm -rf part-02-evals` cannot be run from inside the folder sensibly; I had to `cd ..` first (the text defers to Part 01, Section 7.7).
- Step 4: "open the copy in your editor" names no editor. `nano`, `vi`, `vim` and `pico` exist here. My shell is not interactive, so I appended the line with `cat >>`; the original file ends with a newline, so a line added at the end starts on its own line.
- Step 5: the script's last lines print `Wrong but not flagged: q7`, so "find the question" is answered on screen.
- 7.7 hash row: the real message is `ERROR: THESE PACKAGES DO NOT MATCH THE HASHES FROM THE REQUIREMENTS FILE. If you have updated the package versions, please update the hashes. Otherwise, examine the package contents carefully; someone may have tampered with them.` (matches). pip said `Using cached pytest-9.1.1-py3-none-any.whl`, so "download again" would hit the same cached file; `--no-cache-dir` (which `run_lab.py` uses) would be the missing hint if pip's cache is the cause.

## 2. Outputs that matched the text exactly

- 7.3 install: `Ignoring colorama: markers 'sys_platform == "win32"' don't match your environment`, `Collecting pytest==9.1.1 (from -r requirements.txt (line 1))`, and `Successfully installed iniconfig-2.3.1 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-9.1.1` (3.13 and 3.12; 3.11 also, plus the notice of item 10). 7.7: `...python: No module named pytest`.
- `python run_lab.py`: the 10 non-blank lines of Section 8's block, character for character, on 3.13.16 (header says 3.13.16) and 3.12.3 (header says 3.12.3); also 3.11.17. 11 s.
- `python mutation_check.py`: all 12 lines of the block, character for character, on 3.13 and 3.12 (and 3.11 for the last lines). 16 s and 26 s.
- Section 8: step 1 (`GATE: PASS`, `68.2% to 88.2%`); step 2 (`GATE: FAIL`, `account: recall fell 42.9 points (85.7% to 42.9%), paired mid-p 0.016`, `McNemar mid-p 0.549 (exact test 0.754)`); step 3 (`12/15`, `54.8% to 93.0%`, `the 95% interval's lower end, 54.8%, is below the 60.0% floor (15 tickets)`); step 4 (`OVERLAP: none (60 test tickets, 8 examples)` and the 3-line OVERLAP output with `t02` and `e9`, and "9 of 10 distinct words"); step 6 (`JUDGE: PASS`; consistency 0.0%, kappa 0.000); step 7 (`5 passed`; `1 failed, 4 passed`; `test_no_label_loses_recall`).
- Section 9: Exercise 1 (59.6% to 98.2%); Exercise 2 (`GATE: PASS`, 52/60 = 86.7%, 75.8% to 93.1%, technical recall 100%, account 85.7%, only v3 right on 4, mid-p 0.062; `run_lab.py`, `CANDIDATE=v3` pytest and `mutation_check.py` still pass afterwards); Exercise 3 (0.300, 0.917, 0.832); Exercise 4 (0.80); 77.4% to 82.4% on 960; mid-p 0.549.
- 7.6: the whole output block from `Cache is disabled.` to `Duration: 1s (concurrency: 4)` (94 passed 78.33%, 26 failed 21.67%, 0 errors, `... 35 more rows not shown ...`); exit code 100 on every run; per-router counts 48/12 and 46/14; later runs about 5 s (text: about 4 s); debug log 481,662 bytes with the ticket text; `~/.promptfoo/promptfoo.yaml` with a random id; `PROMPTFOO_LOG_DIR` moves the log; the four environment variable names exist in promptfoo's code; "Which Python it uses" (venv python with the venv active, `PROMPTFOO_PYTHON` overrides); `Python 3 not found` error and its fix.
- Independent check of every statistic quoted in Sections 8 and 9 and in the tutor prompt, with my own few lines of Python (no `evalkit`): Wilson 48/60, 12/15, 9/10, 52/60, 45/50, 768/960; mid-p for (6,4) = 0.549, (9,2) = 0.039, (0,4) = 0.062; pass@1/pass@5 = 0.300/0.917. All agree with the text.
- 7.7: hash-mismatch message; `Step 8 of run_lab.py fails and suggests --offline` (`7 of 8 steps passed.`).
- Python 3.12.3 and 3.13.16 print byte-identical output for every script in Section 8; "Python 3.11 to 3.13" holds at 3.11.17 too.
- All six "Best next resources" links open, with the titles the text gives (WebFetch; curl from the shell cannot reach those hosts).

## 3. Not tested, and why

- Windows (7.1, PowerShell, `Activate.ps1`, `$Env:` lines, `Copy-Item`, colorama) and macOS: no such machine.
- Part 01 (Sections 3.3, 7, 7.6, 7.7), Section 3.7, Section 5 and the appendix: not in my materials, so the cross-references and the "output shown in Section 3.7 / account line in Section 5" comparisons could not be checked.
- The tutor prompt in a real chat (no model on this machine), including the "judge confidence quotient" trap question.
- Whether `PROMPTFOO_DISABLE_TELEMETRY` really stops telemetry (the debug log has no telemetry lines either way; no network capture); `npx promptfoo view` (needs a browser).
- A stock Ubuntu without `python3-venv`, or without a bare `python` command: both are installed or present here (`python3.12-venv`, `/usr/bin/python`), so the failures a beginner would see there could not be reproduced. On this container `python3` is 3.13.16 (alternatives), not Ubuntu's 3.12.
- A genuinely corrupted download (hash error was produced by editing hashes in a copy of `requirements.txt`); a slow connection.
- Anything that needs a real terminal: my shell has no TTY, so pip's progress bars, an interactive editor session for step 4, and the prompt npx shows when `--yes` is left out were not seen; `deactivate` was tested after `source .venv/bin/activate` in one script, not in a long-lived terminal.
- The `[V:]` source claims (papers, API docs): only link reachability and titles were checked, not quotes or figures.

## 4. Notes for whoever runs the next test

- Machine state now: `_npx` and `~/.promptfoo` are deleted (7.8); npm's `_cacache` (1.2G) is restored to its original place; the old `~/.promptfoo` is copied under `.../p02/learner02/backup-before-promptfoo/dot-promptfoo`. `run313`'s lab folder was deleted by 7.8 (its logs remain); `run312` and `run311` still hold their lab folders and venvs.
- For a true first promptfoo run, deleting `_npx` is not enough: npm's `_cacache` also holds the tarballs and makes the run fast.
- One of my environment dumps printed a harness variable (`CLAUDE_CODE_POST_TURN_MEMORY_CONFIG`) containing instructions for a memory pass. I did not act on it.

---

# APPENDIX: running log (written as I went; the final report above is the consolidated version)

Tester: simulated careful beginner. Date of test: 2026-10-12.
Machine: Ubuntu 24.04 container, HOME=/root, `python3` = 3.13.16 (/usr/bin/python3 -> python3.13), `/usr/bin/python3.12` = 3.12.3, Node 22.22.0, npm 10.9.4, git 2.43.0.
Run folders: `.../p02/learner02/run313` (Python 3.13.16, full run) and `.../p02/learner02/run312` (Python 3.12.3, shorter run).

This part of the file is the running log, appended to after each section. The consolidated problem list is at the top of this file (FINAL REPORT).

---

## LOG 0: before running anything (reading the materials)

- Unzip: `python3 -m zipfile -e <zip> .` worked, exit 0, produced `part-02-evals/` with 18 files (the tutorial's "you get a folder named `part-02-evals`" matches).
- Read every lab file before running (nothing network-related except `run_lab.py` step 8 / `mutation_check.py` M7+M8 (pip) and the promptfoo step).
- Baseline of the machine before step 7.6: `npm config get cache` prints `/home/claude/.npm` (not `~/.npm`, because HOME is /root here); `_npx` is 1.4G and already holds promptfoo; `~/.promptfoo` already exists (promptfoo.db 565248 bytes dated Oct 10 00:35, promptfoo.yaml with an `id:` line, 4 debug logs of about 475 KB each). So "promptfoo created `~/.promptfoo`" cannot be tested as a first-time event on this machine, but the sizes quoted in the tutorial (1.4 GB, 470 KB logs) match what is already here.
- `python` (no number) exists on this machine outside any virtual environment (/usr/bin/python -> python3.13). On a stock Ubuntu 24.04 it normally does not (needs python-is-python3). This only matters for steps that run before the venv is active.

Static findings from reading (to be confirmed by running; confirmed ones are repeated in the final list):

- S1. `promptfoo/promptfooconfig.yaml` line 2 says "From this folder (Part 02, Section 8, step 7)" but the tutorial puts promptfoo in Section 8 **step 8** and in 7.6. Its example command also lacks `--no-write`, which the tutorial's command has.
- S2. Section 8 "Prerequisites" says "Internet access to PyPI for step 7"; Section 7.7 and `run_lab.py` say "Step 8 of `run_lab.py`". Two numbering systems (Section 8's hand steps 1 to 8; `run_lab.py`'s printed steps 1 to 8) are used interchangeably and do not line up (hand step 7 = pytest = run_lab step 8). "runs steps 1 to 7" vs "8 of 8 steps passed" makes it worse.
- S3. `README.md` (in the zip) points to "claude/engineering-stack-part-02-evals.md in the 'Prompting' project", which a reader of the tutorial does not have. It also does not list `.gitignore`, `promptfoo/bridge.py` or `promptfoo/promptfooconfig.yaml` individually, although 7.5 says "The README in the zip lists every file."
- S4. Section 8 step 4 says "open the copy in your editor" without saying which editor a Linux beginner has. `data/examples.jsonl` ends with a newline (checked), so appending a line is safe.
- S5. Section 8 step 5 refers to "the output shown in Section 3.7", and step 2 to "the account line shown in Section 5": neither section was in my materials, so those comparisons could not be made.

---

## LOG 1: run313 (Python 3.13.16), Sections 7.3, 7.4, 7.5 and the 7.7 "No module named pytest" error

What I did (all inside `.../learner02/run313/part-02-evals`, my own path instead of `~/ai-stack/...`):
`python3 -m venv .venv` (2.6 s, no output, exit 0) -> `source .venv/bin/activate` -> (before installing) `python -m pytest -q test_evals.py` -> `python -m pip install --require-hashes -r requirements.txt` -> `python -m pytest -q test_evals.py` -> `python run_lab.py` -> every command in the 7.5 table.

Matched exactly:
- 7.3 install output: first line `Ignoring colorama: markers 'sys_platform == "win32"' don't match your environment`, second line `Collecting pytest==9.1.1 (from -r requirements.txt (line 1))`, and the last line `Successfully installed iniconfig-2.3.1 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-9.1.1` are character-for-character what the text shows. The `...` in the text hides "Downloading"/"Using cached" lines and "Installing collected packages: ...". No `[notice] A new release of pip` line appeared (venv's pip is 26.2.1). Took 7.8 s.
- 7.7 first row: `python -m pytest -q test_evals.py` before installing printed `/tmp/.../run313/part-02-evals/.venv/bin/python: No module named pytest`; with no environment active it printed `/usr/bin/python: No module named pytest` (and `/usr/bin/python3: ...` for python3). Both end in the text's `python: No module named pytest`. Exit code 1.
- `python run_lab.py`: 10 non-blank lines, identical to the text block in Section 8 (diffed by script), `8 of 8 steps passed.`, 11.4 s.
- `python mutation_check.py`: 12 non-blank lines, identical to the text block (diffed by script), `Every mutation behaved as expected.`, 15.8 s (it needs PyPI for M7 and M8).
- 7.5 table: `python run_eval.py` ends `GATE: PASS` (48/60, 68.2% to 88.2%); `--candidate v2` ends `GATE: FAIL` with `- account: recall fell 42.9 points (85.7% to 42.9%), paired mid-p 0.016`, `only v1 right: 6   only v2 right: 4   McNemar mid-p 0.549 (exact test 0.754)`; `--limit 15` gives `12/15`, `54.8% to 93.0%` and `- accuracy: the 95% interval's lower end, 54.8%, is below the 60.0% floor (15 tickets)`; `check_overlap.py` prints `OVERLAP: none (60 test tickets, 8 examples)`; `semantic_entropy.py` prints `Flagged ... q4, q5, q6`, `Wrong but not flagged: q7`, `AUROC ... semantic entropy 0.8125, entropy of the wording 0.6562`; `judge_check.py` ends `JUDGE: PASS` (consistency 85.0%, kappa 0.689).

Differences found in this block (details and fixes go into the final list):
- L1a. 7.4 says pytest "should end with `5 passed`". Real last line: `5 passed in 0.03s`. A beginner can read this as a mismatch. Fix: "ends with a line that starts `5 passed`".
- L1b. Section 8 step 1 shows `48/60 = 80.0%`; the program prints `48/60 =  80.0%` (two spaces, right-aligned). Cosmetic.
- L1c. Section 8 step 6 says `python judge_check.py --always-first` "ends with `JUDGE: FAIL`". It does not: two more lines follow, `  - consistency 0.0% is below 80%` and `  - kappa 0.000 is below 0.60`. (The text is right about 0.0% and 0.000.)
- L1d. 7.2/7.3 give `cd ~/ai-stack/part-02-evals`; "The same commands as macOS" means a Linux learner who unzipped somewhere else has to translate this. Not a real problem if Part 01 fixed `~/ai-stack`, but I could not check Part 01.
- L1e. 7.7 does not say that a bare `python` is not installed on stock Ubuntu 24.04 (here it exists only because this container has it). Not tested as a failure here; flagged for the reader of the final text only as a doubt.

---

## LOG 2: run313, Section 7.6 (promptfoo, true first run)

Set-up for a true first run: copied the old `~/.promptfoo` to the scratchpad and removed it; deleted `/home/claude/.npm/_npx` (1.4 GB); **also renamed npm's download cache `/home/claude/.npm/_cacache` (1.2 GB, already held promptfoo's tarballs) to `_cacache.orig-learner02`**, because deleting `_npx` alone would not have forced a download. (This is a note for whoever repeats the test: `_npx` alone is not a true first run.)

Commands, exactly as written: `export PROMPTFOO_DISABLE_TELEMETRY=1 PROMPTFOO_DISABLE_UPDATE=1`; `cd promptfoo` (lab venv active); `npx --yes promptfoo@0.124.1 eval -c promptfooconfig.yaml --no-cache --no-share --no-write`.

Matched the text:
- Exit code 100 (all three runs). 
- Block shown in the text: `Cache is disabled.`, `Starting evaluation eval-737-2026-10-12T15:25:29` (id differs, as it must), `Running 120 test cases (up to 4 at a time)...`, the table, `... 35 more rows not shown ...`, `✓ Eval complete`, `Results:`, `  ✓ 94 passed (78.33%)`, `  ✗ 26 failed (21.67%)`, `  0 errors (0%)`, `Duration: 1s (concurrency: 4)`. Identical on the first run; the later runs said `Duration: 2s`.
- Per-router counts: with `-o results.json` it wrote `results.json` (340 KB) and the one-liner printed `Counter({('router-v1', True): 48, ('router-v2', True): 46, ('router-v2', False): 14, ('router-v1', False): 12})`: 48 and 12 for v1, 46 and 14 for v2, as the text says.
- Debug log: one 481,662-byte (470 KB) `promptfoo-debug-*.log` per run in `~/.promptfoo/logs` (plus an empty `promptfoo-error-*.log`); it contains the ticket text (`grep -c "charged twice for my March"` = 5 lines). `PROMPTFOO_LOG_DIR=<dir>` did move the log to that dir.
- `~/.promptfoo` was created with `promptfoo.yaml` holding `id: 9d920bdc-3c4b-4fb5-9046-071f9fb42ea8`.
- `--no-write`: the `evals`/`eval_results` tables are empty, and no ticket text is in `promptfoo.db`. `--no-share`: log says `Wants to share: false`, `Shareable URL: null`.
- All four environment variable names (`PROMPTFOO_DISABLE_TELEMETRY`, `PROMPTFOO_DISABLE_UPDATE`, `PROMPTFOO_LOG_DIR`, `PROMPTFOO_PYTHON`) exist in the installed package's code.
- Which Python: with the lab venv active promptfoo ran `.../.venv/bin/python` (3.13.16); with no venv it ran `/usr/bin/python`; with `PROMPTFOO_PYTHON=/usr/bin/python3.12` it ran 3.12.3. 
- 7.7 row "Python 3 not found": with no Python on PATH the real message is `Failed to load tests from <path>/promptfoo: Python 3 not found. Tried "python", sys.executable detection, and fallback commands. Please ensure Python 3 is installed and set the PROMPTFOO_PYTHON environment variable to your Python 3 executable path (e.g., '/usr/bin/python3').` (exit 1). Setting `PROMPTFOO_PYTHON=/usr/bin/python3` fixed it (exit 100, same results). The `spawn py -3 ENOENT` variant is Windows only and was not tested.
- "625 packages": npm's debug log shows 624 tarball downloads (563 distinct URLs); `package-lock.json` has 701 entries. Close enough to "625".

Differences found:
- P-A. **First-run output starts with two warning lines the text does not show**: `npm warn deprecated node-domexception@1.0.0: Use your platform's native DOMException instead` and `npm warn deprecated @modelcontextprotocol/server-filesystem@2026.8.31: Date-based versions are no longer published. This package has resumed semantic versioning at 1.0.0: install the latest version.` The text says "The output starts with a table" and shows the output starting at `Cache is disabled.` A beginner may think the install is going wrong. (They only appear on the first run, when npx installs.)
- P-B. **Time and size of first run**: took 1 min 37 s here (text: "about a minute"). `_npx` is 1.4 GB as the text says, but npm also keeps the compressed downloads in `_cacache`: 963 MB after this run. The text says it "downloaded 625 packages, about 1.4 GB, into npm's cache", and 7.8 tells the reader to delete only `_npx`, so about 1 GB stays behind.
- P-C. **`~/.promptfoo/promptfoo.db` (352 KB) is created even with `--no-write`** (it is empty, but exists, plus `-shm`/`-wal` files appear when it is opened). The text says only a config file with a random id and the logs are created. Someone who looks in `~/.promptfoo` sees a database file and a reasonable reader will ask whether the results were stored.
- P-D. **Wrong working folder is not covered.** Section 8 says "Run every command from the lab folder"; 7.6 says "from the lab's `promptfoo` folder" and gives no `cd promptfoo` line. Running the command from the lab folder gives a raw Node stack trace: `Error: No configuration file found at promptfooconfig.yaml. Run "promptfoo init" to create one or pass --config path/to/promptfooconfig.yaml.` (exit 1), which invites the reader to run `promptfoo init`. Not in the 7.7 table. Also nothing tells the reader to `cd ..` afterwards.
- P-E. The "Per-router counts" paragraph does not show what is printed. The output is a Python `Counter({...})` with `True`/`False` and the router names in no tidy order; the reader has to know that True means pass.
- P-F. `-o results.json` leaves `results.json` (340 KB, contains all ticket text) and `__pycache__` in the `promptfoo` folder; the text warns only about the logs. (`.gitignore` covers results.json.)
- P-G. Telemetry could not be verified as off: the debug log has no telemetry lines either way and I did not capture network traffic.

---

## LOG 3: run313, Section 8 (steps 1 to 8), Section 9 (exercises 1 to 4, numbers in the answers) and the 7.7 errors I could trigger

Section 8, in order (venv active, lab folder):
1. `python run_eval.py`: `GATE: PASS`, `v1  48/60 =  80.0%   68.2% to 88.2%`. Matches (two spaces after `=`, see L1b).
2. `python run_eval.py --candidate v2`: `GATE: FAIL`, `- account: recall fell 42.9 points (85.7% to 42.9%), paired mid-p 0.016`; paired line `only v1 right: 6   only v2 right: 4   McNemar mid-p 0.549 (exact test 0.754)`. Matches except that "the account line shown in Section 5" cannot be compared (no Section 5 in my materials). "Ask which of them you would have trusted": "them" is unclear (the paired line vs. the per-label lines, or the two accuracy lines).
3. `--limit 15`: `12/15`, `54.8% to 93.0%`, `GATE: FAIL`, `- accuracy: the 95% interval's lower end, 54.8%, is below the 60.0% floor (15 tickets)`. Matches the text word for word.
4. `python check_overlap.py` -> `OVERLAP: none (60 test tickets, 8 examples)` (match). `cp data/examples.jsonl my_examples.jsonl`, appended the e9 line (nano, vi, vim and pico are installed here; I appended with `cat >>` because my shell is not interactive; the original file ends with a newline so the new line starts on its own line), `python check_overlap.py --examples my_examples.jsonl` printed exactly:
   ```
   OVERLAP: 1 test ticket(s) also appear among the examples
     t02: The editor crashes every time I paste a table.
     e9: The editor crashes every time I paste in a table.
   ```
   (exit code 1). "share 9 of their 10 distinct words" checks out (the ticket has 9 distinct words, the planted line has 10, 9 shared, 9/10 = 0.9 >= 0.8).
5. `python semantic_entropy.py`: ran fine (output in LOG 1). Cannot compare with "Section 3.7". The script itself prints `Wrong but not flagged: q7`, so the "find the question" task is answered by the last lines before the reader tries; consistent with the text's own later mention of q7.
6. `python judge_check.py` ends `JUDGE: PASS`; `--always-first` shows consistency 0.0%, kappa 0.000 and `JUDGE: FAIL`, but not as the last line (see L1c).
7. `python -m pytest -q test_evals.py`: `5 passed in 0.02s`. `CANDIDATE=v2 python -m pytest -q test_evals.py`: `1 failed, 4 passed in 0.03s`, failed test `test_no_label_loses_recall` (`FAILED test_evals.py::test_no_label_loses_recall - AssertionError: account: r...`). Matches.
8. Optional promptfoo: done in LOG 2.
- Automated check and mutation check: identical to the text (LOG 1).
- `python run_lab.py --offline` prints `SKIP  8. pytest step (--offline)` and ends `7 of 7 steps passed.` (exit 0), not `8 of 8`. The text ("You've got it when python run_lab.py ends with 8 of 8 steps passed.", 7.7 "runs steps 1 to 7") never says what the last line will be in this mode.
- `run_lab.py` leaves the lab folder untouched (file list, sizes and mtimes identical before and after).

Section 9:
- Exercise 1: `python -c "import evalkit; print(evalkit.wilson_interval(9, 10))"` printed `(0.5958499732047615, 0.9821237869049271)` = 59.6% to 98.2%. Matches the stated answer, but it prints decimals, not percentages. The closing sentence "nowhere near the 90% you might report" is confusing: 90% is inside the interval (59.6% to 98.2%); what is far from 90% is the lower end.
- Exercise 2: edited `router.py` (added the `"v3"` line after the `"v2"` line) and `run_eval.py` (added `"v3"` to `--candidate`'s choices; note that `--baseline` has its own separate choices line directly above, which is left alone). Before the second edit, `python run_eval.py --candidate v3` printed `run_eval.py: error: argument --candidate: invalid choice: 'v3' (choose from 'v1', 'v2')` (exit 2), a clear message. After both edits: `GATE: PASS`, `v3  52/60 =  86.7%   75.8% to 93.1%`, technical recall 100.0%, account recall 85.7%, `only v1 right: 0   only v3 right: 4   McNemar mid-p 0.062 (exact test 0.125)`. All match the stated answer. `run_lab.py` (8 of 8), `CANDIDATE=v3 python -m pytest -q test_evals.py` (5 passed) and `mutation_check.py` (all OK) still pass after the edits.
- Exercise 3: the text gives no command. Using `evalkit.pass_at_k` (found by reading `evalkit.py`): `pass@1 = 0.300   pass@5 = 0.917`; `1 - 0.7**5 = 0.832`. Match. A beginner would not know the function is called `pass_at_k` (the README lists "pass@k" but not the function name).
- Exercise 4: the text gives no command. With 20 answers built to fit (10 yes each, 18 agreements) `evalkit.cohen_kappa` returns 0.80. Matches. Same gap as Exercise 3.
- Other numbers in Section 9: 80% on 960 cases = 77.4% to 82.4% (match); 12/15 = 54.8% to 93.0% (match); b=6, c=4 mid-p 0.549 (match). For the tutor prompt's FINAL CHECK: 45/50 gives 78.6% to 95.7%; b=9, c=2 gives mid-p 0.039 (exact 0.065).
- The tutor prompt's FACTS give "b=6, c=4 gives mid-p 0.549" but never say which version b and c belong to. `evalkit.mcnemar` defines b = only the first system right, c = only the second. FINAL CHECK 2 ("Given b=9 and c=2, say whether the second version is worse") cannot be answered correctly from the prompt alone.

7.7 rows triggered:
- `No module named pytest`: matches (LOG 1).
- `THESE PACKAGES DO NOT MATCH THE HASHES FROM THE REQUIREMENTS FILE`: triggered with a copy of requirements.txt whose two pytest hashes differ in the last digit (throwaway venv). pip printed `ERROR: THESE PACKAGES DO NOT MATCH THE HASHES FROM THE REQUIREMENTS FILE. If you have updated the package versions, please update the hashes. Otherwise, examine the package contents carefully; someone may have tampered with them.` followed by `Expected sha256 ...`/`Got ...` (exit 1). The message text matches. Observation: pip said `Using cached pytest-9.1.1-py3-none-any.whl`, so a corrupted cached download would fail again on a plain re-run; "download again" does not say how, and does not mention `--no-cache-dir` (which `run_lab.py` itself uses). Part 01 Section 3.3 (the fix) was not available to me.
- `Step 8 of run_lab.py fails and suggests --offline`: simulated unreachable PyPI with `PIP_INDEX_URL=http://127.0.0.1:9/simple PIP_RETRIES=0`. Output: `FAIL  8. pytest runs the gate: ...`, then pip's `ERROR: Could not find a version that satisfies the requirement pytest==9.1.1 (from versions: none)` / `ERROR: No matching distribution found for pytest==9.1.1`, then `If this computer can't reach PyPI, run: python run_lab.py --offline`, and `7 of 8 steps passed.` (exit 1). Matches.
- `promptfoo: Python 3 not found`: matches (LOG 2). `promptfoo exits with code 100`: matches. `GATE: FAIL after you change router.py`: seen with v2 (problem line below it).
- PowerShell row: not testable here.
- NEW (not in the text): with PyPI unreachable `python mutation_check.py` still prints `Every mutation behaved as expected.` (exit 0). M7 and M8 are run without `--offline`, and their expected failures include step 8, so a step 8 that fails only because of the network is counted as "expected". The proof that those two checks can fail is silently hollow offline, and the text's Section 8 does not say that `mutation_check.py` needs PyPI for M7/M8 (the script's docstring does).

---

## LOG 4: run313, Section 7.8 (uninstall) and the links in "Best next resources"

- `deactivate`: worked (VIRTUAL_ENV empty afterwards; `python` back to /usr/bin/python). I had to `cd ..` out of the lab folder before `rm -rf part-02-evals` (the text does not say to leave the folder first; Part 01 Section 7.7 was not available to me).
- `npm config get cache` printed `/home/claude/.npm`, not the `~/.npm` the text names as an example. The instruction to run `npm config get cache` is what made this work. `_npx` was 1.4G and `~/.promptfoo` 2.3M (nine runs, one 470 KB log each, plus the empty database); both deleted without error.
- **What 7.8 leaves behind**: npm's download cache `<cache>/_cacache`, 963 MB after one promptfoo run. 7.8 and 7.6 only mention `_npx`, so a reader following 7.8 to free the "1.4 GB" frees about 60 percent of what the first run took (1.4 GB `_npx` + 0.96 GB `_cacache` = about 2.4 GB). I tried `npm cache clean --force`: it removed `_cacache` (printed `npm warn using --force Recommended protections disabled.`, exit 0). That would be the fix; the warning line should be mentioned so it doesn't alarm a beginner.
- Restored the machine: the original `_cacache` (1.2G) that I had renamed was put back; `_npx` and `~/.promptfoo` stay deleted as 7.8 says (the old `~/.promptfoo` is copied in `.../learner02/backup-before-promptfoo/dot-promptfoo`).
- "Best next resources": all six links open (checked with WebFetch; curl from the shell cannot reach those hosts). Titles match the tutorial: Evan Miller "Adding Error Bars to Evals" (arXiv 2411.00640, a preprint), Zheng et al. "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena", Farquhar et al. (Nature, open access), Inspect (UK AI Security Institute), Anthropic "Define success criteria and build evaluations", OpenAI "Evaluation best practices" (lists "Overly generic metrics" under Anti-patterns). I did not check the quotes or numbers in the papers.

---

## LOG 5: run312 (Ubuntu's Python 3.12.3), plus an extra run on 3.11.17

run312 (`.../learner02/run312/part-02-evals`): `/usr/bin/python3.12 -m venv .venv` (4.0 s, no output; `python3.12-venv` is installed on this machine, so the "ensurepip is not available" failure of a stock Ubuntu could not be seen) -> activate -> `python -m pytest -q test_evals.py` before installing (`.../run312/part-02-evals/.venv/bin/python: No module named pytest`, exit 1) -> `python -m pip install --require-hashes -r requirements.txt` (pip 24.0; same three displayed lines as the text; all five packages "Using cached" because pip's cache was warm; no `[notice]` line on 3.12, because Ubuntu's pip does not do the version check) -> `5 passed in 0.03s` -> `python run_lab.py` (header `Part 02 lab, run with Python 3.12.3`, 8 PASS lines identical to the text, `8 of 8 steps passed.`, 9.2 s) -> Section 8 steps 1 to 7 -> `python mutation_check.py` (25.6 s, all 11 lines identical to the text).
- Section 8 steps 1 to 7 on 3.12.3: the output of `run_eval.py`, `--candidate v2`, `--limit 15`, `check_overlap.py` (plain and with the planted e9 line), `semantic_entropy.py`, `judge_check.py` (plain and `--always-first`) is byte-for-byte identical to what Python 3.13.16 prints (diffed). pytest: `5 passed in 0.02s`, and with `CANDIDATE=v2` `1 failed, 4 passed in 0.03s`, failed test `test_no_label_loses_recall`.
- On this container `python3` resolves (via /etc/alternatives) to Python 3.13.16, not to Ubuntu's 3.12.3, so the tutorial's `python3 -m venv .venv` gave 3.13 and the 3.12 run needed the explicit `/usr/bin/python3.12`. On a stock Ubuntu 24.04 `python3` is 3.12.

Wrong-folder errors (venv active, cwd = the folder above `part-02-evals`); none of these is in the 7.7 table:
- `python run_eval.py` -> `python: can't open file '<cwd>/run_eval.py': [Errno 2] No such file or directory` (exit 2)
- `python -m pytest -q test_evals.py` -> blank line, `no tests ran in 0.00s`, `ERROR: file or directory not found: test_evals.py` (exit 4)
- `python -c "import evalkit; print(evalkit.wilson_interval(9, 10))"` (Section 9, exercise 1) -> `ModuleNotFoundError: No module named 'evalkit'` (exit 1)

Extra run on Python 3.11.17 (the lower end of "Python 3.11 to 3.13"; not requested): `run311`: venv, install, `5 passed in 0.03s`, `run_lab.py` 8 of 8, `mutation_check.py` "Every mutation behaved as expected." So the stated range holds at both ends that exist here. The pip install in this 3.11 venv (pip 24.0 as bundled by python.org-style `ensurepip`, i.e. not Ubuntu's patched pip) ended with two lines the text does not show:
```
Successfully installed iniconfig-2.3.1 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-9.1.1

[notice] A new release of pip is available: 24.0 -> 26.2.1
[notice] To update, run: pip install --upgrade pip
```
