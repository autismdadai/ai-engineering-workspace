# Session B review: Part 01

Reviewed: `research/engineering-stack/docs/parts/engineering-stack-part-01-setup.md` against the rubric in `session-b-brief.md` and the KEY rows of Appendix B whose "Where" column names Part 01.

Method note: read in full, including the lab listings and the three code files (checked their printed outputs and the mutation tests against the code by reading, nothing was run). No benchmark, accuracy or model figures appear in Part 01; its numbers are versions, dates, byte counts, hashes and counts of checks.

## Rubric 1: every number carries its model and task, and its year

| Location | Problem | Evidence | Severity |
|---|---|---|---|
| 7.1 step 5, "Check: `python --version` should print `Python 3.13.16`" | An expected output that depends on the day the reader installs. `py install 3.13` gives whatever 3.13.x is current, and Section 10 says later 3.13 releases are coming. No "as of October 9, 2026" here, unlike the Section 7.4 note "Your paths, versions and disk space will differ". | "`python --version` should print `Python 3.13.16`, and the prompt should start with `(.venv)`" ; Section 10: "later 3.13 releases fix security issues only" | missing scope |

Other numbers checked (versions, dates, byte counts, "about 14 lines of build messages", "25 characters", "7 PASS ... 5 INFO") carry their machine, tool version or date in the same sentence or the Section 12 source line. Untagged time estimates are listed under rubric 6.

## Rubric 2: accuracy changes in percentage points

None found. Part 01 contains no accuracy or percentage-change figures.

## Rubric 3: citations complete enough to find

| Location | Problem | Evidence | Severity |
|---|---|---|---|
| Section 6, "Why 3.13 and not the newest Python" (also Section 10, Cheat sheet decision rule 2, `check_setup.py` docstring) | The package-compatibility data (which of "all 40" packages reject Python 3.14 or 3.15) is cited only as "the freshness ledger". No file name is given, unlike every other project document (`claude/...md`), and it is not in the Section 12 table. The 40 packages are not listed, so the reader cannot find the data. | "satisfy all 40, so Ubuntu 24.04's own 3.12.3 works too [T, from the freshness ledger's PyPI data]" ; Cheat sheet: "until the freshness ledger says otherwise" | missing scope |
| Section 12, row PYPI | The URL is a template, not a page: it names no package, yet the row supports three separate facts (packaging 26.3, pip 26.2.1, uv 0.13.0). | "https://pypi.org/pypi/PACKAGE/json" | missing scope |

All other Section 12 rows give a title and a URL; text citation keys all appear in the table (spot-checked every key used in Sections 1 to 10).

## Rubric 4: same number identical everywhere; cross-references resolve

| Location | Problem | Evidence | Severity |
|---|---|---|---|
| Section 3.1 ("Windows PowerShell says the name "is not recognized" [R: no Windows test machine]") and Section 5 worked example ("[R: no Windows test machine; expected output is the same 64 characters]") | The reason given for [R] is out of date. The header, 7.1, 7.4 and "Run on your computer" now say Windows 11 was used on October 12, 2026. A reader sees "no Windows test machine" and "ran on Windows 11" in the same part. (The specific commands may still be untested on Windows; the stated reason is what contradicts.) | Header: "The lab itself ran on Windows 11 on October 12, 2026" ; "Run on your computer": "R1 to R3 ran on Windows 11 on October 12, 2026" | inconsistency |
| Section 3.3, refusal output, versus Section 8 step 3 | Step 3 tells the reader to "Expect the refusal shown in Section 3.3". The shown output names a file that is not in the lab and a line number that does not match the shipped file. In `requirements-all-hashes-wrong.txt` as listed, three comment lines come first, so `packaging==26.3` starts on line 4. | "(from -r req-bad.txt (line 5))" ; listing: three `#` lines, then `packaging==26.3 \` | inconsistency |

Checked and consistent: the three hashes (wheel, source archive, and the one-character-changed versions) are identical in Section 3.3, Section 5, the refusal output, the mutation tests and the requirements listings (counted 64 characters each); Python 3.13.16 / 3.12.3, pip 26.2.1 / 24.0, Git 2.43.0, Node.js 22.22.0, npm 10.9.4, Node 24.21.0 and the 7 PASS / 5 INFO counts agree wherever repeated; "7 of 7" and the M1 to M7 outputs match the code; the blind-check counts add up (47 + 39 + 7 + 1 = 94; second pass 6 + 1 = 7). Internal cross-references (Sections 3.2, 3.3, 3.4, 7.1 step 8, 7.5, 7.6, 7.7, 8 step 3, "Where hashes come from", "Run on your computer") all resolve, and the "Used for" section numbers in Section 12 match the citations in the text. The header's tag counts (133 [V], 83 [T], 26 [R], 13 [U]) are in the range of what I counted, but the counting rule is not stated (prose mentions such as "94 [V] claims" seem to be included), so I did not treat it as a finding.

## Rubric 5: example prompts and code blocks internally correct

| Location | Problem | Evidence | Severity |
|---|---|---|---|
| Section 9, tutor prompt, FACTS, virtual environment line | The tutor is told the generic command is `python -m venv .venv`. On stock Ubuntu 24.04 and on macOS, `python` does not exist before a venv is active; the part's own Section 2 and Sections 7.2 and 7.3 use `python3.13` and `python3`. The prompt asks "Windows, Mac or Linux?" but carries no Linux step (no `python3-venv` install, which 7.3 needs, and no `sha256sum`), so a Linux or Mac learner is taught a command that fails. | "Virtual environment: `python -m venv .venv` (Windows: `py -V:3.13 -m venv .venv`)." ; Section 2: "`python` on Windows and inside an active virtual environment; often `python3` on macOS and Linux" ; 7.3: "`python3 -m venv .venv`" | unusable example |
| Section 8 step 3, "the last character of each hash, just before the ` \`, is different" | The text does not match the file. In the listing of `requirements-all-hashes-wrong.txt` the second hash is the last line and has no backslash after it. A reader looking for " \" after the second hash will not find it. | "...6004aed7a" (end of line, no ` \`) | inconsistency |
| Section 7 intro and 7.1 step 4, unzip path | The text says Extract All yields "a folder named `part-01-setup`" inside `ai-stack`, and step 4 then runs `cd $HOME\ai-stack\part-01-setup`. Windows' Extract All by default creates a new folder named after the zip, which would put the lab one level deeper. The text does not say to change the destination. Needs a reader check on Windows. | "on Windows, right-click the zip and choose Extract All [R]" ; "`cd $HOME\ai-stack\part-01-setup`" | unusable example |

Checked and correct against the code by reading: `check_setup.py` output in 7.4 (formats, counts, WARN and FAIL texts), `read_key.py` outputs including "25 characters" (counted), the `break_hashes` change giving `cd1d` and `aed7a`, the M1 to M7 mutations (each find-string occurs once and the expected failing steps follow from the code), the `git check-ignore -v` line numbers against the `.gitignore` listing, and the SHA-256 values of `hello` and `hello` plus a newline.

## Rubric 6: each technique carries an evidence-class label or tag

| Location | Problem | Evidence | Severity |
|---|---|---|---|
| Section 7.5 table (column "macOS and Linux"); Section 8 steps 3 and 4; Section 7.7 first bullet; "Hidden files" paragraph; Section 9 exercise 3 | [T] is given to commands for "macOS and Linux" together, but the only test machine was Ubuntu 24.04. The header says the macOS steps "have not been run" and 7.2 is headed "[R: no macOS test machine]". The part draws the distinction itself in one cell (`shasum -a 256 FILE` (macOS) [R]; `sha256sum FILE` (Linux) [T]), so the other cells overstate. Exercise 3 is the clearest: it names macOS as tested. | "`cp .env.example .env` on macOS and Linux [T]" ; "`rm -rf .venv` on macOS and Linux [T]" ; "[T for macOS and Linux; R for PowerShell]" ; "`source .venv/bin/activate` [T]" under the heading "macOS and Linux" | missing scope |
| Section 6, "Why 3.13", last two sentences | [T] is defined as "the command or code ran on the test machine, and its output is shown". Here the first [T] is borrowed from a ledger ("from the freshness ledger's PyPI data"), and the second states a prediction ("would fall back") with no output shown. | "asked for crewai without a version, it would fall back to an old release that still accepts that Python [T]" ; How to read: "[T] tested: the command or code ran on the test machine, and its output is shown" | inconsistency |
| Section 1 problem 1; Section 2 "Package" row; Section 6 table columns "Account or key?" and "Hardware"; Section 8 intro ("Time") | Claims with no tag, although the part says "Every claim in a part carries one tag". Examples: "No" for Python, pip, Node.js, Visual Studio Code, WinGet and WSL in "Account or key?" (only Git has [T]); "Any" for hardware on most rows; "Time: about 20 minutes by hand, 1 minute automated" (no machine, no one timed it, no tag). | "PyPI, the Python Package Index, is the official public collection for Python." ; "Pinning exact versions makes a lab repeatable." ; "**Time:** about 20 minutes by hand, 1 minute automated." | inconsistency |
| Section 12, row "ledger" (class "Project audit") and Section 4 "[V: ledger P7-11]" | "Project audit" is not among the classes defined in "How to read" (OD, PR, PP, VB, PB, AI). A [V] tag rests on the project's own ledger, and "No opened source says so [V: ledger P7-11]" is an absence claim tagged as verified. | "Source classes, strongest first: official specifications and documentation (OD), peer-reviewed papers (PR), preprints (PP), vendor or personal blogs (VB, PB), AI-written (AI)" versus "Project audit" | inconsistency |

## Rubric 7: KEY rows for this part

None found. No row of Appendix B (rows 1 to 30, overview lines 128 to 157) names Part 01 in its "Where" column, so there is nothing to compare. Part 01 contains none of the figures in those rows.

## Rubric 8: no claim stronger than its source could support

| Location | Problem | Evidence | Severity |
|---|---|---|---|
| "What this part gives you" | The summary says everything is free with no account, but Section 6 marks Docker Desktop as needing a paid subscription for some commercial use, and marks Docker's account question, the Python install manager's cost and WSL's licence as unchecked. | "Everything here is free and needs no account or API key." versus "Paid subscription required for commercial use in larger enterprises" and "Account or key? Not checked here [U]" and "Cost: Not stated on the pages read [U]" | overclaim |
| Section 5 example 3, "Automatic key revocation"; Section 1 problem 3 | One vendor help article is stated as unconditional fact about a process run by GitHub and Anthropic, with no "Anthropic says" and no date, while Section 10 hedges the same point ("The program Anthropic describes"). The frequency "often" in Section 1 also rests on that one vendor page. Needs source check. | "GitHub notifies Anthropic, Anthropic deactivates the key, and the owner gets an email [V: AKB]" ; "Developers often commit keys to public code repositories by accident [V: AKB]" | overclaim |
| Section 5 example 4 and the tutor prompt FACTS | "newest LTS release" is cited to the post for release 24.21.0 itself (Section 12, NRL: "Node.js 24.21.0 (LTS)", 2026-09-08). One release post cannot show that no later 24.x LTS release came out in the month before October 9, 2026. Needs source check (the release list, NPR, would be the right source). | "nodejs.org's newest LTS release is 24.21.0 [V: NRL]" ; "Node.js 24.21.0 is the LTS release." | overclaim |
| Section 6, "The strongest alternative: uv" | A ranking with no comparison behind it. Section 10 says no comparison was opened. The [V: PYPI] tag covers uv's self-description, licence and version, not "strongest". | "The strongest alternative: uv." versus Section 10: "No measured comparison was opened for this part [U: settle with an independent benchmark, if one exists]" | overclaim |
| Section 7.6 row 3 | One Ubuntu 24.04 test is generalized to Debian. | "Installing into the system's Python on Ubuntu or Debian [T]" | missing scope |

## Rubric 9: no trace of how the document was made

| Location | Problem | Evidence | Severity |
|---|---|---|---|
| "Checks run on this part", paragraphs "Blind source check" and "Beginner test" (also Section 12 intro and the PYPI row) | Beyond recording which checks ran and their counts (which is method), these paragraphs narrate revisions made after review, which a reader of the finished part cannot see: "fixed in this text", "all fixed above", "now tested or marked [R]", "the step now uses a fresh environment", "Also fixed: ...". Agent and tool details also appear: "A second fresh agent followed Sections 7.3 to 9", "the checker read the matching project pages", "a fetch tool that summarizes each page". | "Every partly supported claim was then fixed in this text, by narrowing the claim, splitting off what the source didn't cover, or testing it here" ; "It found 15 problems where a literal reader would get a different result without an error message, all fixed above." | process trace |
| Section 11, second sentence | A note about the project's own backlog, not guidance for the reader. | "claude/new-skills-appendix.md has no matching idea; its four suggestions are decoding-controller, faithfulness-auditor, injection-hardening and long-context-placer." | process trace |

No TODOs, "as discussed", or chat-session references found elsewhere. The tags, the dated "read on" and "checked" notes, and the Windows-run record were treated as method, as the brief says.

Findings by severity: error 0, overclaim 4, missing scope 5, inconsistency 6, unusable example 2, process trace 2 (19 in total).

