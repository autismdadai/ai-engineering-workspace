# Eval pack: quantum-entanglement-lab

For skill version 1.2.1. Built 6 October 2026; with-and-without results and packaging added 7 October; first trigger tests 8 October.

## What's here

- `evals.json`: 10 requests that should load the skill and 10 that shouldn't (each with the reason), 3 end-to-end tasks, 4 adversarial tasks, and the with-and-without plan.
- `mutation_check.py`: proves each of the lab's six tests can fail.
- `grade_answer.py`: checks an answer against a task; `--self-test` proves each task's checks can fail.
- `with_without_results.json`: the 7 October with-and-without runs: each answer, its grade, whether the lab ran, and token use.

Run the commands from the skill folder, `quantum-entanglement-lab/`, which holds `SKILL.md`, `references/`, `scripts/` and `evals/`. The scripts need Python 3 and, for the lab, `qutip`, `numpy` and `scipy`. They never ask for input, use no network, and print JSON.

## 1. Script tests (run)

```bash
python evals/mutation_check.py
```

It runs the lab as written, then 13 copies that each carry one deliberate bug. Each bug must stop the lab at the test it targets, with the earlier tests still passing. It also runs one harmless change, which must still pass, and a broken copy under `python -O`, which must refuse to run. Add `--script PATH` if the lab script is somewhere else.

Results with QuTiP 5.3.1 (6 and 7 October 2026):

| Lab version | Runs as expected | What it missed |
|---|---|---|
| 1.2.1 (7 October; script unchanged) | 16 of 16 | nothing |
| 1.2 | 16 of 16 | nothing |
| 1.1 | 12 of 16 | partial measurement on the wrong Bell state; partial measurement in the wrong basis; a CHSH angle 0.05 rad off; a broken lab run under `python -O` |

What changed in version 1.2, and why:

- **Partial measurement** now checks that each outcome leaves |00⟩ or |11⟩. Version 1.1 checked only the 50/50 odds, which every Bell state and the wrong basis also give.
- **CHSH** must now equal 2√2, not just exceed 2.8. With an angle 0.05 rad off, |S| is about 2.8267, so version 1.1 passed it.
- **The script refuses to run under `python -O`.** That flag strips every `assert`, so version 1.1 printed six PASS lines even with a broken teleportation correction.

The harmless change shows why one gotcha in `SKILL.md` was reworded. X·Z and Z·X differ only by a global phase, so swapping them still passes. What matters is which bit selects X and which selects Z, and swapping those fails.

## 2. Answer checks (self-test run; model answers not yet)

```bash
python evals/grade_answer.py --self-test
python evals/grade_answer.py --task e1-run-lab --answer answer.txt
```

On 6 October 2026 the self-test passed all 7 tasks: each known-good answer passed and each known-bad answer failed. The checks are text patterns, a first pass and not a judge. Read borderline answers against the task's rubric in `evals.json`. On 7 October three patterns (two for a2, one for a4) were widened after they failed three correct answers in the with-and-without runs. `changes` in `evals.json` records this, and the self-test still passes.

## 3. With and without the skill (quick version run)

The plan: for each of the 7 tasks, run the same model 3 times with the skill installed and 3 times without, each in a fresh session. Keep the settings and tools the same. Save each final answer, grade it with `grade_answer.py`, and note from the tool log whether the agent ran the lab. Compare the two conditions task by task. The plan and decision rule are under `with_and_without` in `evals.json`.

On 7 October 2026 the quick version ran on skill 1.2: one run per task per condition, each a fresh Sonnet 5.5 helper agent working only in its own folder, plus one run of the single-file Claude-app version on e1. Every answer was read against its rubric:

| Task | With the skill | Without |
|---|---|---|
| e1-run-lab | pass (ran the lab) | fail (no lab to run) |
| e2-local-flip | pass | pass |
| e3-teleport-cost | pass | pass |
| a1-chsh-four | pass | pass |
| a2-faster-than-light | pass | pass |
| a3-simulation-not-proof | pass | pass |
| a4-made-up-citation | pass | pass |

The single-file version passed e1 too: the helper rebuilt all four bundled files from SKILL.md, every SHA-256 matched, and the lab passed. Every helper with the skill ran the lab, even when the question didn't need it, and used about 11% more tokens on average (112,323 against 101,150, as the Agent tool reported them). According to their tool logs, no helper read outside its folder or used a forbidden tool. By the decision rule, keep the skill: it wins on e1 and loses nowhere. One run found a gap that 1.2.1 fixes: the teleportation card didn't say which bit selects X and which selects Z. Answers, grades and token counts are in `with_without_results.json`.

Limits of this run: one run per cell, so small differences mean nothing; one model; and the helpers ran inside the Prompting project, so both conditions saw the project's instructions and file list, though not the files.

## 4. Trigger tests (first pass run)

First pass, 8 October 2026, in Claude Code 2.1.294 with `claude plugin eval` (model claude-sonnet-5-5), all four skills loaded together with their long descriptions, one run per request, and no shell tool in the test sessions: 7 of the 10 should-load requests loaded this skill, and 10 of the 10 should-not requests left it off. Missed: requests 4, 7 and 10, which ask about a single gate, a two-gate circuit or an argument rather than asking to run the lab. Their transcripts weren't read; in the qubit-math and trig-check misses that were, the model answered by itself. Not yet run: three runs per request, the short Claude-app description, and the Claude app itself. Details and how to re-run: `claude/trigger-tests-2026-10-08.md`.

The full test: install only this skill. Send each of the 20 requests in a fresh session and record whether the skill loads. All 10 in `should_trigger` should load it, and none of the 10 in `should_not_trigger`. If you change the description to fix a miss, test it on new requests too.

Run them on each host with the description that host uses: the 197-character one in the Claude app, the 365-character one elsewhere (see section 5). A pass for one description says nothing about the other.

## 5. Two descriptions and three packages

The skill has two descriptions. `description` (365 characters) is for Claude Code and other hosts that follow the spec's 1,024-character limit. `metadata.claude-app-description` (197 characters) is for the Claude app, which takes up to 200. `skills/build_skill.py` checks the folder against the spec and builds three versions from the same files:

- `quantum-entanglement-lab.zip`: the folder with the 365-character description;
- `quantum-entanglement-lab-claude-app.zip`: the same folder with the 197-character description;
- `quantum-entanglement-lab.single-file.md`: one SKILL.md with the 197-character description and the script and reference cards bundled at the end, for the Claude app's save card, which keeps only SKILL.md. Each bundled file carries its SHA-256 so a copy can be checked.

```bash
python skills/build_skill.py skills/quantum-entanglement-lab --out dist   # from the folder that holds skills/
```

`evals/` is left out of every package, because it holds known wrong answers that an agent shouldn't see.

## Limits

- Text patterns can't judge reasoning. A wrong answer can pass with the right words, and a right answer phrased oddly can fail.
- The trigger tests have had one first pass, in Claude Code, one run per request. The with-and-without test has run once per task per condition, not three times.
- Everything here is a simulation. Passing shows the code reproduces quantum mechanics' predictions; it says nothing about real hardware.
