# Engineering Stack Part 01: Review Findings

*Phase 4 record for claude/engineering-stack-part-01-setup.md, October 9, 2026, in the finding format of claude/fabel-prompt-audit.md. Evidence class: project review. Two independent checks ran on separate agents (Claude Sonnet), neither seeing the other's work or the author's reasoning:*

- *a **blind source check**, given only the draft's 94 [V] claims and their source links: 54 supported, 39 partly supported, 0 contradicted, 1 claim with no text, after a second pass that covered the 7 it could not reach at first (one link failed, four sources were past its 40-lookup limit);*
- *a **beginner test** that followed Sections 7.3 to 9 literally on the Linux test machine, in a clean folder, with Python 3.13.16 and with Ubuntu's own 3.12.3: every output the draft showed reproduced, and it reported 15 problems.*

*Each finding below was checked by the author against the source or by re-running it before being accepted; none was accepted on the checker's word alone. All are fixed in the saved part. After the fixes, `run_lab.py` passed 7 of 7 and `mutation_check.py` 7 of 7, with Python 3.13.16 (pip 26.2.1) and 3.12.3 (pip 24.0).*

**Severity.** Critical: likely to put false content in the final document. High: likely to weaken reliability or safety. Medium: quality and clarity. Low: polish.

### F-01 · High · The main break-it step tested nothing

- **The draft said:** "In a copy of `requirements.txt`, change the last character of both hashes, make a fresh virtual environment, and install from the copy." (Section 8, step 3)
- **What goes wrong:** The tester made a new environment but left the old one active, which already had packaging installed. pip printed `Requirement already satisfied: packaging==26.3` and exited 0, so no hash was checked, and the lab appeared to show that hash checking doesn't work. Exercise 3 had the same trap.
- **Why:** Reproduced by the author: in an environment that already has the package, the all-wrong file gives `Requirement already satisfied`; in a fresh one, the same command refuses [T].
- **Fix:** The step now runs the fresh environment's own Python, without activating it, and says why. A row in Section 7.6 covers the message.

### F-02 · High · "The last character" was ambiguous

- **The draft said:** "change the last character of both hashes" (Section 8, step 3)
- **What goes wrong:** The first hash line ends with ` \`, so its last character is the backslash. Editing that makes pip warn that the line "has --hash but no requirement, and will be ignored", then install normally.
- **Why:** The tester ran three variants of the edit; all installed without an error.
- **Fix:** The lab now ships `requirements-one-hash-wrong.txt` and `requirements-all-hashes-wrong.txt`, and `run_lab.py` checks that each is `requirements.txt` with exactly the intended change. The text says where the changed character sits.

### F-03 · High · Shown output didn't match real output

- **The draft said:** a `git check-ignore -v` box tagged [T], with a file-name column and a line for `notes.env` (Section 3.4).
- **What goes wrong:** Git prints no such column and prints nothing for a path no rule matches. A [T] tag promises captured output.
- **Why:** The tester's run, and the author's re-run [T].
- **Fix:** The box now shows Git's real output, and `git status --ignored --short` gives a positive check (`!! .env`).

### F-04 · High · Several claims went beyond their sources

- **The draft said:** that Python lists GPG signatures "for every file"; that pip checks hashes "only in hash-checking mode"; that pins must use `==`; "Free" for tools whose pages don't say so; that uv "installs Python, creates environments and installs packages".
- **What goes wrong:** Each is stronger or wider than the source. pip also checks the hash PyPI supplies with each download, against corruption; pins can also be URLs or file paths; not every row on Python's release page has a GPG signature.
- **Why:** The blind check (claims C18, C23, C30, C31, C36 to C38, C43, C44, C80), each confirmed against the source.
- **Fix:** Each claim now says only what its source says. Cost cells cite the licence or terms that make a tool free, or are marked [U]. uv is described in its own words.

### F-05 · Medium · Tags covered more than their sources

- **The draft said:** sentences in which one [V] tag covered a sourced fact plus a cross-reference, a recommendation, a command or a reason the source doesn't give (for example "Needed only for the sandbox labs in Part 08", `shasum -a 256`, `export`, "which is why Node.js signs its list").
- **What goes wrong:** A reader can't tell which part was checked.
- **Why:** The blind check (C1, C11 to C14, C24, C25, C34, C42, C53, C55, C62, C65 to C69, C88, C90, C91).
- **Fix:** Sentences were split so each tag covers only what its source or test supports. Commands were tested here [T] or marked [R], and PATH order was demonstrated with two scripts [T].

### F-06 · Medium · The Linux path was missing steps

- **The draft said:** Section 7.3 had no terminal step, no folder, no unzip, no editor, and no commands for Node.js; Section 9 said the only prerequisite was typing a command.
- **What goes wrong:** A beginner reaches Section 8 unable to edit a file or find the lab.
- **Why:** The beginner test, problems 3 and 12.
- **Fix:** Unzip, hidden-file, editor and folder steps for all three systems; Node.js commands for Linux [R]; honest prerequisites.

### F-07 · Medium · Hidden files and the success check

- **The draft said:** "Copy `.env.example` to `.env`." (Section 8, step 4)
- **What goes wrong:** Names starting with a dot are hidden, and the only success signal was a line's absence.
- **Why:** The beginner test, problem 4.
- **Fix:** `ls -a` and `Get-ChildItem -Force`; copy commands for each system; `git status --ignored --short` as a positive check.

### F-08 · Medium · An exercise didn't reproduce

- **The draft said:** compute the SHA-256 of `hello`, with a table of expected values (Sections 3.3 and 9).
- **What goes wrong:** `echo hello > hello.txt` adds a newline, so the hash differs from the table, in a guide whose rule is "different hash, stop".
- **Why:** The tester got `5891b5b5...`; the author reproduced it [T].
- **Fix:** The exercise uses a Python one-liner, and the table shows the newline case as a lesson.

### F-09 · Medium · The Python version story contradicted itself

- **The draft said:** "Use Python 3.13" in several places, while also calling Ubuntu's 3.12.3 fine; the sample outputs came from a test machine whose default Python isn't stock.
- **What goes wrong:** Linux readers get 3.12.3 and pip 24.0 and can't tell whether that's a problem.
- **Why:** The beginner test, problem 6, and the series' PyPI data (3.11 to 3.13 satisfy all 40 packages).
- **Fix:** "Python 3.11 to 3.13: install 3.13, or use Ubuntu 24.04's 3.12" throughout; the test machine is described; the lab was re-run on stock 3.12.3 [T].

### F-10 · Medium · Normal messages looked like failures

- **The draft said:** nothing about Git's `hint:` lines after `git init`, the WARN line when Node.js is missing, `fatal: not a git repository`, or running the check from another folder.
- **What goes wrong:** Each looks like a broken setup to a beginner.
- **Why:** The beginner test, problems 7, 9 and 10.
- **Fix:** Section 7.4 explains WARN versus FAIL and shows the Node.js WARN line; Sections 3.4, 7.6 and 8 cover the hints and the repository precondition; `check_setup.py`'s messages now point to Section 7.

### F-11 · Medium · Unsafe order when deleting an environment

- **The draft said:** "A virtual environment: delete its `.venv` folder."
- **What goes wrong:** Deleting it while active leaves the prompt in place, and `python` silently falls back to the system's copy.
- **Why:** The beginner test, problem 11, re-run by the author.
- **Fix:** `deactivate` first, with the delete command for each system.

### F-12 · Medium · No guidance when PyPI is unreachable

- **The draft said:** prerequisites "Sections 7.1 to 7.4", with `--offline` only in the README.
- **What goes wrong:** Offline, steps 2 to 4 fail with plain pip errors and no pointer to `--offline`.
- **Why:** The beginner test, problem 12; reproduced by pointing pip at a dead index [T].
- **Fix:** `run_lab.py` now prints `If this computer can't reach PyPI, run: python run_lab.py --offline`, and the prerequisites mention it.

### F-13 · Medium · A source link the checker couldn't open

- **The draft said:** the execution-policy page's address without its `?view=` parameter.
- **What goes wrong:** The page failed twice for the checker, so three claims went unchecked.
- **Why:** The blind check, C49, C81 and C92; the author's first fetch of the same address failed too.
- **Fix:** The working address is in Section 12; the second pass found all three supported.

### F-14 · Low · Smaller items

- **The draft said / did:** an unexplained `$ ` prompt prefix; Windows and macOS commands on the same lines of the cheat sheet; bare tags under code blocks (one reached the checker as a claim with no text); a shortened error quote not marked as shortened; "requires a different Python" where pip says "Ignored the following versions that require a different python version"; "quietly builds" for about 14 lines of output; no way to clear a variable; `pip freeze` printing nothing in a new environment; the wrong mutation number in `mutation_check.py`'s docstring; README missing from an appendix described as complete; "free online" for a book page that says "available".
- **Fix:** Each corrected.

**Not tested here** (marked [R] or [U] in the part): every Windows and macOS step, `sudo apt` installs, Node.js downloads (nodejs.org is blocked from the test machine's shell), and reading uv's install script (astral.sh is blocked too).
