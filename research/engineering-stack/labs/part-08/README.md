# Engineering Stack, Part 08 lab: an agent loop you can break

Companion to claude/engineering-stack-part-08-agents.md, Section 8.
Tested October 14, 2026 on Linux with Python 3.13.16, 3.12.3 and 3.11.17.

The core lab uses only Python's standard library: no installs, no model, no
account, no API key, no network. A scripted stand-in plays the model.

| File | What it is |
|---|---|
| `agent_loop.py` | The loop: every stop reason, call validation, approval, time limits (a timed-out tool may still finish), error results that keep exception text from the model, caps |
| `stand_in.py` | Scripted stand-in models and the example tools |
| `sandbox_check.py` | Checks a `docker run` command against known options; never runs it; a checklist, not a guarantee |
| `screen_agent.py` | A computer-use loop in miniature, with an instruction planted on screen |
| `not_a_sandbox.py` | Shows code with no builtins reaching the `os` module (it only reads the working folder's path) |
| `demo.py` | One agent run turn by turn, two commands reviewed, the screen demo |
| `run_lab.py` | 27 checks |
| `mutation_check.py` | Breaks the lab 28 ways; each must make `run_lab.py` fail |
| `crosscheck.py`, `requirements-crosscheck.txt` | Optional: the OpenAI Agents SDK 0.23.1 with a fake model, tracing off, no key |

Quick start, from this folder, in a virtual environment (Part 01, Section 7):

    python run_lab.py            # expect: 27 of 27 checks passed
    python mutation_check.py     # expect: 28 of 28 mutations caught
    python demo.py

Optional:

    python -m pip install -r requirements-crosscheck.txt
    python crosscheck.py         # expect: 3 of 3 cross-checks passed

Everything here is for learning. The files, order and web pages are invented.
Reviewing a `docker run` command doesn't make it safe, and nothing in this
folder is a security boundary.
