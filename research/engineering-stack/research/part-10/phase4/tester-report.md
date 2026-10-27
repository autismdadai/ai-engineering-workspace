# Part 10 lab: beginner test report (Sections 6 to 9)

Date: October 15, 2026. Machine: Ubuntu 24.04. HOME set to /home/claude/part10/phase4/tester/home. Each Python had a fresh unzip into ~/ai-stack and a fresh .venv. The session was interrupted once by a usage limit; the 3.13 run was done in two parts, and the 3.12 and 3.11 runs were scripted with the same commands (/home/claude/part10/phase4/tester/run_one.sh; logs out312.log, out311.log).

## Versions and timings
| | 3.13 | 3.12 | 3.11 |
|---|---|---|---|
| Python | 3.13.16 | 3.12.3 | 3.11.17 |
| pip in new venv | 26.2.1 | 24.0 | 24.0 |
| venv creation | 2.2 s | not timed | not timed |
| run_lab.py | 28 of 28, exit 0, 0.09 s | same | same |
| pip install -r requirements-crosscheck.txt | 100 s | 452 s | 200 s |
| "Collecting" lines (packages) | 52 | 52 | 51 |
| packages in venv after install (pip list lines incl. 2 header lines) | 55 | 55 | 55 |
| crosscheck.py | 11.4 s first run, 7 of 7, exit 0 | 7 of 7, about 1 s | 7 of 7, about 1 s |
| mutation_check.py | 46 of 46, 2.5 s | 46 of 46 | 46 of 46 |
| venv size | 378 MB | not measured | not measured |

Cross-check packages (identical on all three): presidio-analyzer 2.2.364, python-stdnum 2.2, spacy 3.8.16, numpy 2.4.6, pydantic 2.14.1, pydantic-core 2.50.1, phonenumbers 9.0.41, tldextract 5.4.0, regex 2026.9.29, requests 2.34.2, thinc 8.3.13, plus others (full list in pip313.log).

## Result: everything the text states matched
- 7.1 to 7.3: `28 of 28 checks passed` on all three.
- 7.4: seven PASS lines, `Network attempts blocked: 2 (publicsuffix.org, raw.githubusercontent.com)`, `7 of 7 cross-checks passed` on all three. Nothing left in home besides pip's cache.
- 7.5 / 7.7: `python reader_presidio.py` prints `spaCy's en_core_web_lg isn't installed: python -m spacy download en_core_web_lg`, exit 1. Matches both sections. (The other quoted message, `Install the cross-check requirements first`, was not triggered: I did not run it without Presidio installed.)
- Section 8 step 2: demo.py runs, exit 0, identical output on all three Pythons (md5 equal). Step 3, 5, 6 printed exactly the text's lines (`Decision('deny', 'amount: must be between 0 and 500')`, `Decision('deny', "unexpected arguments ['approved']")`, `docs.example.com backslash`, `Call Dana at <PHONE_US_1> or <EMAIL_1>`). Step 4: only one `return Decision("ask"` (guard.py line 93); after the change, FAIL on 2, 2b, 2c, 3b and `24 of 28 checks passed`; after putting it back, 28 of 28 and guard.py byte-identical to the zip copy. Step 7 values match (see problem 1). Step 8: `46 of 46 mutations caught`, a few seconds. Step 9: seven results.
- Section 9 exercises: 1 prints `108.8 0.083`; 2 prints `non-commercial`; 3 prints `allow`. All match the stated answers.
- 7.8: `python -m pip cache purge` (removed about 300 files), deactivate, cd .., rm -rf worked. Nothing starting `lab10` in /tmp, before, during or after, on all three runs.
- Node.js 22.22 claim in step 5 (`evil.example`) not tested: no internet use or Node check was part of this run.

## Problems
Counts: high 0, medium 0, low 3.

1. Low. Section 8 step 7. I ran `python -c "from guard import screen; print(screen(10000, 0.001, 0.975, 0.01))"`. Printed: `{'bad': 10.0, 'caught': 9.75, 'missed': 0.25, 'false_alarms': 99.9, 'precision': 0.08891928864569083}`. The text says it "prints `caught` 9.75, `false_alarms` 99.9 and a precision of 0.0889". A beginner expects three items and sees a dictionary of five with an unrounded number. Text should say: "prints a dictionary that includes `caught` 9.75, `false_alarms` 99.9 and `precision` 0.0889 (shown as 0.08891928864569083)".
2. Low. Section 7.8. After `pip cache purge`, an empty `~/.cache/pip` folder remains. Harmless; the text could say the cache is emptied, not that the folder is removed (it does not claim removal).
3. Low. Section 9 self-check, answerability. Questions 1 (OWASP's conclusion) and 4's second half (Llama Guard 4 tested on Meta's in-house, English-only set; an independent test found more misses) are answered only in the "Answers" paragraph and rely on Section 3, which I was not given. From Sections 6 to 9 alone: Q2 (three legs: visible in 7.6 and the step 4 explanation and Exercise 3), Q3 (step 5), Q5 (misconception list on HIPAA) and Q4's first reason (demo.py part 4 shows precision 0.060 for Llama Guard 4 at a 1% attack rate) were findable; Q1 and the in-house-set reason were not. My own answers from Sections 6 to 9: (1) prompting defences aren't enough, so defence has to be checks in code; (2) untrusted input, private data, outward action; (3) browsers read the backslash as a slash, so the host differs from Python's; (4) the rates come from the vendor's own test set, and precision depends on your attack rate; (5) no: stored data still needs safeguards (risk analysis etc.). The text should point each question to the section that teaches it (for example "see Section 3.3").

## Notes (not problems)
- 7.4 says "a few minutes": observed 1.7 to 7.5 minutes depending on the run (the 3.12 install was slowest). "About 50 packages": 51 to 52 downloaded. Accurate.
- A pip "new release" notice appeared on 3.11 only (7.7 covers it as not an error).
- Cleanup: the lab folders, venvs and pip cache were deleted. Left under /home/claude/part10/phase4/tester/: logs (pip313.log, out312.log, out311.log), run_one.sh, empty home/ai-stack containing a pip.log written by my script, home/.cache/pip (empty). Nothing outside that folder; /tmp has no `lab10*`.
