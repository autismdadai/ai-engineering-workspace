# Part 02 lab: measure a system and catch a regression

From *The AI Engineering Stack*, Part 02: evals, test data and judges. The part explains every step; this file is the short version.

- **Goal:** score a stand-in support-ticket router on 60 labelled tickets, decide with a gate set in advance whether a change may ship, and try the tools evals rely on: a confidence interval, a paired test, an overlap check, semantic entropy and a check of a model judge.
- **Time:** about 30 minutes by hand, or 1 minute for the automated check.
- **Cost:** none. No model, account or API key: the "systems" are keyword rules and the judge's verdicts are recorded.
- **Data:** every ticket, sampled answer and judge verdict in `data/` was invented for teaching. The arithmetic is real; the data describes no real system.
- **Needs:** Python 3.11 to 3.13 and the Part 01 setup. Internet access to PyPI to install pytest, and for check 8 of `run_lab.py`. Node.js 22.22 or newer only for the optional promptfoo step.
- **Pinned:** pytest 9.1.1 and its dependencies, with SHA-256 hashes from PyPI (read October 10, 2026).
- **Tested:** Linux (Ubuntu 24.04 in a cloud container), October 12, 2026, with Python 3.13.16, 3.12.3 and 3.11.17: 8 of 8 checks passed, and all 11 mutations behaved as expected. promptfoo 0.124.1 ran on Node.js 22.22.0. Windows and macOS are not yet tested.

## Run it

Open a terminal in this folder, with your virtual environment active, and run:

```
python run_lab.py
python mutation_check.py
```

| Command | What it does | Expected last line |
|---|---|---|
| `python run_eval.py` | Scores v1, the version in use, and applies the gate | `GATE: PASS` |
| `python run_eval.py --candidate v2` | Scores the change under review against v1 | the reason the gate failed |
| `python semantic_entropy.py` | Semantic entropy over recorded samples | the AUROC line |
| `python judge_check.py` | Position bias and agreement of a recorded judge | `JUDGE: PASS` |
| `python check_overlap.py` | Looks for test tickets among the prompt's examples | `OVERLAP: none ...` |
| `python -m pytest -q test_evals.py` | The gate as tests (after installing `requirements.txt`) | `5 passed in ...` |
| `python run_lab.py` | Eight checks: the statistics, then everything above with its break-it steps, in a temporary folder. `--offline` skips check 8, the one that needs PyPI. | `8 of 8 checks passed.` (`7 of 7` with `--offline`) |
| `python mutation_check.py` | Damages copies of the files one at a time and confirms the matching checks fail. `--offline` skips M7 and M8, which need PyPI. | `Every mutation behaved as expected.` |

On macOS and Linux, use `python3` instead of `python` if no virtual environment is active.

## Files

| File | Purpose |
|---|---|
| `evalkit.py` | The statistics: Wilson interval, per-label scores, McNemar test, kappa, entropy, AUROC, pass@k, overlap |
| `router.py` | Two stand-in systems: v1 (in use) and v2 (the change under review) |
| `run_eval.py` | The report and the gate |
| `semantic_entropy.py` | The semantic entropy demo |
| `judge_check.py` | The judge check |
| `check_overlap.py` | The test-data overlap check |
| `test_evals.py` | The gate as pytest tests |
| `requirements.txt` | pytest and its dependencies, pinned with hashes |
| `data/tickets.jsonl` | 60 test tickets with their correct labels |
| `data/examples.jsonl` | 8 examples a prompt might show the model |
| `data/samples.jsonl` | 8 questions with 10 recorded answers each |
| `data/judge_pairs.jsonl` | 20 recorded judge verdicts in both orders, with people's verdicts |
| `promptfoo/promptfooconfig.yaml`, `promptfoo/bridge.py` | The same ticket eval in promptfoo (optional; needs Node.js) |
| `run_lab.py`, `mutation_check.py` | The automated lab and the proof that its checks can fail |
| `.gitignore` | Keeps environments, caches and promptfoo's output out of Git |

## Privacy

Nothing in the Python lab sends data anywhere. If you run the optional promptfoo step, turn off its usage telemetry first (`PROMPTFOO_DISABLE_TELEMETRY=1`) and keep `--no-share`. promptfoo also writes a debug log containing the test cases to `~/.promptfoo/logs`; Part 02, Section 7.6, explains both.
