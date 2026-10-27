# Engineering Stack, Part 09 lab: workflows that survive, and several agents

Companion to claude/engineering-stack-part-09-workflows-and-multi-agent.md, Section 8.
Tested October 15, 2026 on Linux with Python 3.13.16, 3.12.3 and 3.11.17.

The core lab uses only Python's standard library: no installs, no model, no
account, no API key, no network.

| File | What it is |
|---|---|
| `workflow.py` | A small durable workflow engine: steps that may loop, a step limit, a checkpoint after every step, pauses for a person, retries with full jitter, signed checkpoints, an idempotency store |
| `examples.py` | A refund workflow (routing, a draft-and-review loop with a cap, approval, a retried refund) and a stand-in payment service that can lose its reply |
| `multi_agent.py` | Several agents in miniature: handoff versus agent-as-tool, a subagent's summary, cost arithmetic, compounding errors, voting with shared mistakes |
| `crash_run.py` | Used by check 3: a process killed mid-step, continued by another |
| `demo.py` | The refund run step by step, the double refund without a key, the agent numbers |
| `run_lab.py` | 30 checks |
| `mutation_check.py` | Breaks the lab 33 ways; each must make `run_lab.py` fail |
| `crosscheck.py`, `requirements-crosscheck.txt` | Optional: the same behaviours in LangGraph 1.2.15, with network connections blocked |

Quick start, from this folder, in a virtual environment (Part 01, Section 7):

    python run_lab.py            # expect: 30 of 30 checks passed
    python mutation_check.py     # expect: 33 of 33 mutations caught (under a minute)
    python demo.py

Optional (downloads LangGraph and its dependencies from PyPI):

    python -m pip install -r requirements-crosscheck.txt
    python crosscheck.py         # expect: 6 of 6 cross-checks passed

Everything here is for learning. The orders, payments and agents are invented.
The engine runs one process per thread at a time and does no locking; use a
real durable-execution tool for real work (Section 6 of the part).
