# Eval pack: trig-check

For skill version 1.0. Built 7 October 2026.

## What's here

- `test_trig_check.py`: 21 known-answer tests of the script. They cover identities that hold and identities that fail, exact values, degree handling, conversions, every triangle case (including SSA with 0, 1 and 2 triangles), and two inputs that must be refused.
- `mutation_check.py`: breaks the script 12 ways on purpose and checks that a named test catches each break; one harmless change must still pass.
- `evals.json`: 10 requests that should load the skill and 10 that shouldn't, 3 end-to-end tasks, 2 adversarial tasks, and the with-and-without plan.
- `grade_answer.py`: checks an answer against a task; `--self-test` proves each task's checks can fail.

Run the commands from the skill folder. They need Python 3 and SymPy, use no network, and print JSON.

```bash
python evals/test_trig_check.py
python evals/mutation_check.py
python evals/grade_answer.py --self-test
```

## Results (7 October 2026, Python 3.13, SymPy 1.14.0)

- Tests: 21 of 21 pass.
- Mutation check: 14 of 14 runs as expected. The first version of the allowlist test sent `Symbol(x)`, which was refused for an unrelated reason even with the allowlist switched off, so it couldn't show the guard was working. It now sends `factorial(5)`, which SymPy would compute if the guard were off.
- Grader self-test: 5 of 5 tasks.

## Trigger tests

First pass, 8 October 2026, in Claude Code 2.1.294 with `claude plugin eval` (model claude-sonnet-5-5), all four skills loaded together with their long descriptions, one run per request, and no shell tool in the test sessions: 6 of the 10 should-load requests loaded this skill, and 10 of the 10 should-not requests left it off. Missed: requests 2, 3, 8 and 9: three quick exact-value or conversion questions and one SSA triangle count. In the one read in full (request 2), the model answered by itself, correctly, without loading any skill. Not yet run: three runs per request, the short Claude-app description, and the Claude app itself. Details and how to re-run: `claude/trigger-tests-2026-10-08.md`.

## Not run yet

- Trigger tests in the Claude app: install the skill, send each of the 20 requests in a fresh chat, and record whether it loads. Use the description that host uses.
- With-and-without runs: the plan is under `with_and_without` in `evals.json`. Each helper run cost about 100,000 tokens in the October 2026 lab test.
