# Eval pack: qubit-math

For skill version 1.0. Built 7 October 2026.

## What's here

- `test_qubit_math.py`: 25 known-answer tests of the script. They cover Bell states and reduced density matrices, entropy and purity, gates and circuits, measurement in the Z, X and Y bases (including the state left after measuring), both fidelity conventions, Pauli expectation values, qubit order, and three inputs that must be refused.
- `mutation_check.py`: breaks the script 13 ways on purpose and checks that a named test catches each break; one harmless change must still pass.
- `evals.json`: 10 requests that should load the skill and 10 that shouldn't, 3 end-to-end tasks, 2 adversarial tasks, and the with-and-without plan.
- `grade_answer.py`: checks an answer against a task; `--self-test` proves each task's checks can fail.

Run the commands from the skill folder. They need Python 3 and numpy, use no network, and print JSON.

```bash
python evals/test_qubit_math.py
python evals/mutation_check.py
python evals/grade_answer.py --self-test
```

## Results (7 October 2026, Python 3.13)

- Tests: 25 of 25 pass.
- Mutation check: 15 of 15 runs as expected. One break swaps the whitelist parser for Python's eval; the test that sends `[abs(-1), 0]` catches it, because eval accepts that input and the whitelist refuses it.
- Grader self-test: 5 of 5 tasks.

## Trigger tests

First pass, 8 October 2026, in Claude Code 2.1.294 with `claude plugin eval` (model claude-sonnet-5-5), all four skills loaded together with their long descriptions, one run per request, and no shell tool in the test sessions: 2 of the 10 should-load requests loaded this skill, and 10 of the 10 should-not requests left it off. Missed: requests 1 to 6, 9 and 10, all short state or gate questions. In the two read in full (requests 1 and 5), the model answered by itself, correctly, without loading any skill. Not yet run: three runs per request, the short Claude-app description, and the Claude app itself. Details and how to re-run: `claude/trigger-tests-2026-10-08.md`.

## Not run yet

- Trigger tests in the Claude app: install the skill, send each of the 20 requests in a fresh chat, and record whether it loads. Use the description that host uses. Watch the boundary with quantum-entanglement-lab: "run the lab" should load the lab, while "compute this state" should load qubit-math.
- With-and-without runs: the plan is under `with_and_without` in `evals.json`. Each helper run cost about 100,000 tokens in the October 2026 lab test.
