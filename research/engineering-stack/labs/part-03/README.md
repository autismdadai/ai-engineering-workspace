# Lab for Part 03: prompts as software interfaces

Free. No account, API key or model download. The core checks use only
Python's standard library; two optional checks add Pydantic and DSPy.

Tested October 12, 2026 on Ubuntu 24.04 with Python 3.11.17, 3.12.3 and
3.13.16: 9 of 9 checks passed on each, and mutation_check.py reported
"Every mutation behaved as expected." Windows and macOS: not run here.

## Run it

From this folder, inside a fresh virtual environment (Part 01, Section 7):

    python run_lab.py

Expected last line: `7 of 7 checks passed.` (check 3 has 8 parts, so it prints `8 of 8 linter checks right`)

Optional cross-checks (install each file with its own command; pip will not
mix a hash-pinned file and a plain one in one install):

    python -m pip install --require-hashes -r requirements-optional.txt
    python run_lab.py --with-pydantic          # 8 of 8
    python -m pip install -r requirements-dspy.txt     # about 400 MB
    python run_lab.py --with-pydantic --with-dspy      # 9 of 9

Prove the checks can fail:

    python mutation_check.py

Expected last line: `Every mutation behaved as expected.`

## Files

| File | What it does |
|---|---|
| ticket_contract.py | The ticket JSON Schema and a small validator |
| schema_lint.py | Reusable: checks any JSON Schema against two vendors' strict-mode rules |
| validate_retry.py | Validate a reply; on failure, ask again with the error attached (up to 3 attempts) |
| tool_loop.py | A tool loop that validates arguments and stops after a step cap |
| toy_optimizer.py | A toy prompt search that overfits a small validation set |
| paper_numbers.py | Recomputes the MIPRO and GEPA figures the part cites |
| optional_pydantic_check.py | Pydantic generates the same contract; both validators agree |
| optional_dspy_check.py | DSPy compiles a tiny program offline with its DummyLM |
| run_lab.py | Runs the checks |
| mutation_check.py | Breaks the code 17 ways and expects each check to catch it |

The stand-in models return recorded replies. Their outputs are
illustrative, not measurements of any real model.
