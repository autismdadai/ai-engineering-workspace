# Engineering Stack: Windows Reader-Test Run, October 12, 2026

*The first run of the series' labs on the owner's Windows computer, done by Claude through the Claude desktop app while the owner watched. Evidence class: project test record. It settles reader tests R1 to R3 of Part 01 and R1 and R2 of Part 02; see "What is still [R]" for the rest.*

## How it was run

- **Computer:** Windows 11 (build 10.0.26300), Intel Core i5-9500T (6 logical processors), 7.8 GB of memory reported, Intel UHD Graphics 630, no discrete GPU. Git 2.56.0.windows.2 and WSL were present; Docker and Node.js were not.
- **Python was not installed** (only Windows' Microsoft Store placeholder). The first run of the runner reported that and stopped, which is the setup check's job. With the owner's go, a script downloaded `python-3.13.16-amd64.exe` from python.org with `curl.exe`, compared its SHA-256 with the value python.org publishes (`fb4f9f5d438b2396da0086dc70b935c530cb578e37adc6d354f7ad2037fee83b`) using `certutil`, got a match, and installed it for this user only (`/passive InstallAllUsers=0 PrependPath=1 Include_launcher=1`). It then printed `Python 3.13.16`. This used python.org's full installer, not the Python install manager that Part 01, Section 7.1 recommends: the installer needs no typing, and the session could only click, not type, in Windows' terminals.
- **The labs:** unzipped from the owner's own engineering-stack-lab-part-01.zip and engineering-stack-lab-part-02.zip into Downloads\ai-stack. A double-click script, RUN-LABS.bat, made a fresh virtual environment in each lab folder with Python 3.13.16 and ran each lab's scripts with that environment's Python, saving the output to lab-results.txt. The labs downloaded packaging 26.3 and pytest 9.1.1 (with colorama 0.4.6 on Windows) from PyPI, with the owner's go.

## Results

| Test | Command | Expected | Got |
|---|---|---|---|
| Part 01 R1 | `python check_setup.py` | No FAIL lines | 5 PASS, 1 WARN (Node.js not found), 0 FAIL, 7 INFO |
| Part 01 R2 | `python run_lab.py` | `7 of 7 steps passed.` | `7 of 7 steps passed.` (45 seconds) |
| Part 01 R3 | `python mutation_check.py` | `Every mutation behaved as expected.` | the same, M1 to M7 all OK (105 seconds) |
| Part 02 R1 | `python run_lab.py` | `8 of 8 checks passed.` | `8 of 8 checks passed.` (29 seconds) |
| Part 02 R2 | `python mutation_check.py` | `Every mutation behaved as expected.` | the same, M1 to M11 all OK (57 seconds) |

The check_setup.py INFO lines on Windows matched what Part 01, Section 7.4 predicted: an extra `Graphics:` line and a `wsl:` line.

## What is still [R]

- **The typed PowerShell steps** (Part 01, Section 7.1; Part 02, Section 7.1): `py install 3.13`, `Activate.ps1` and the execution-policy fix weren't exercised, because the runner called each environment's `python.exe` directly.
- **Part 01 R4** (checking the Node.js installer with `Get-FileHash`) and **Part 02 R4** (promptfoo): Node.js isn't installed.
- **Part 02 R3** (`$Env:CANDIDATE = "v2"` with pytest in PowerShell): needs typing in PowerShell. check 8 of run_lab.py covers the same gate through pytest.
- **Part 03 R1 to R3:** not run yet.

## Full output

```text
Lab run started 2026-10-12 20:49:54
Python used to make the environments: 3.13.16 at %USERPROFILE%\AppData\Local\Programs\Python\Python313\python.exe

======================================================================
part-01-setup
======================================================================
Making a fresh virtual environment in part-01-setup\.venv ...

--- python check_setup.py ---
    Setup check for the AI Engineering Stack labs (reads only; changes nothing)
    
    PASS  Python 3.13.16 at %USERPROFILE%\Downloads\ai-stack\part-01-setup\.venv\Scripts\python.exe
    PASS  Running inside a virtual environment: %USERPROFILE%\Downloads\ai-stack\part-01-setup\.venv
    PASS  pip 26.2.1
    PASS  git version 2.56.0.windows.2
    WARN  Node.js not found. Fine for Part 01; needed from Part 02 on (Part 01, Section 7)
    PASS  .gitignore lists .env (this folder is not a Git repository yet)
    INFO  Operating system: Windows-11-10.0.26300-SP0
    INFO  Processor: Intel(R) Core(TM) i5-9500T CPU @ 2.20GHz (6 logical processors)
    INFO  Memory the system reports: 7.8 GB (installed memory is often slightly more)
    INFO  Graphics: Intel(R) UHD Graphics 630
    INFO  Free disk space here: 135.3 GB
    INFO  docker: not found (optional, used in Part 08)
    INFO  wsl: found (Windows Subsystem for Linux, optional, Part 08)
    
    Summary: 5 PASS, 1 WARN, 0 FAIL, 7 INFO
    Ready for the labs. Read the WARN lines too.
--- finished in 2 seconds, exit code 0 ---

--- python run_lab.py ---
    Part 01 lab, run with Python 3.13.16
    
    PASS  1. The setup check reports no FAIL lines
    PASS  2. The hash-pinned install succeeds and gives packaging 26.3
    PASS  3. Break it: with only the wheel's hash wrong, pip skips the wheel and builds from the source archive, whose hash still matches
    PASS  4. Break it: with every hash wrong, pip refuses to install anything
    PASS  5. Git ignores .env but keeps .env.example
    PASS  6. Break it: with .env removed from .gitignore, Git would commit it, and check_setup.py reports FAIL
    PASS  7. read_key.py refuses a missing or placeholder key and never prints a real one
    
    7 of 7 steps passed.
--- finished in 45 seconds, exit code 0 ---

--- python mutation_check.py ---
    OK   M1 .gitignore no longer lists .env: failed steps ['5.'], expected ['5.']
    OK   M2 read_key.py prints the key: failed steps ['7.'], expected ['7.']
    OK   M3 read_key.py accepts the placeholder: failed steps ['7.'], expected ['7.']
    OK   M4 check_setup.py never reports a .env problem: failed steps ['6.'], expected ['6.']
    OK   M5 requirements.txt pins hashes that match no file: failed steps ['2.', '3.', '4.'], expected ['2.', '3.', '4.']
    OK   M6 the all-wrong file has correct hashes again: failed steps ['4.'], expected ['4.']
    OK   M7 harmless: a reworded comment: failed steps none, expected none
    
    Every mutation behaved as expected.
--- finished in 105 seconds, exit code 0 ---

======================================================================
part-02-evals
======================================================================
Making a fresh virtual environment in part-02-evals\.venv ...

--- python run_lab.py ---
    Part 02 lab, run with Python 3.13.16
    
    PASS  1. evalkit's statistics match the reference values
    PASS  2. The version in use (v1) passes its own gate
    PASS  3. Break it: v2 fails the gate on account recall, which overall accuracy can't show
    PASS  4. Break it: with 15 tickets, 12 right can't show the 60% floor
    PASS  5. No test ticket is in the prompt's examples, and a planted near-copy is caught
    PASS  6. Semantic entropy flags the three arbitrary answers and misses the consistently wrong one
    PASS  7. The recorded judge passes, and a judge that always picks the first answer fails
    PASS  8. pytest runs the gate: it passes for v1 and fails for v2
    
    8 of 8 checks passed.
--- finished in 29 seconds, exit code 0 ---

--- python mutation_check.py ---
    OK   M1 the Wilson interval uses 90% instead of 95%: failed checks ['1.', '4.'], expected ['1.', '4.']
    OK   M2 the mid-p forgets to subtract half the point probability: failed checks ['1.', '3.'], expected ['1.', '3.']
    OK   M3 kappa leaves out the correction for chance: failed checks ['1.', '7.'], expected ['1.', '7.']
    OK   M4 entropy reports bits where nats are expected: failed checks ['1.', '6.'], expected ['1.', '6.']
    OK   M5 AUROC counts ties as wins: failed checks ['1.', '6.'], expected ['1.', '6.']
    OK   M6 answers are grouped by exact wording, not meaning: failed checks ['6.'], expected ['6.']
    OK   M7 the gate ignores a label's lost recall: failed checks ['3.', '8.'], expected ['3.', '8.']
    OK   M8 the judge check forgets that B was shown first: failed checks ['7.', '8.'], expected ['7.', '8.']
    OK   M9 the overlap check misses near-copies: failed checks ['5.'], expected ['5.']
    OK   M10 the accuracy floor is never applied: failed checks ['4.'], expected ['4.']
    OK   M11 harmless: a reworded comment: failed checks none, expected none
    
    Every mutation behaved as expected.
--- finished in 57 seconds, exit code 0 ---

======================================================================
SUMMARY (exit code 0 means everything in that script passed)
  OK    part-01-setup  check_setup.py  (exit code 0)
  OK    part-01-setup  run_lab.py  (exit code 0)
  OK    part-01-setup  mutation_check.py  (exit code 0)
  OK    part-02-evals  run_lab.py  (exit code 0)
  OK    part-02-evals  mutation_check.py  (exit code 0)

Saved to %USERPROFILE%\Downloads\ai-stack\lab-results.txt
```
