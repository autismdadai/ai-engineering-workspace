# Part 04 lab: context budgets, prompt caching and position tests

Companion to claude/engineering-stack-part-04-context.md (The AI Engineering Stack, Part 04).
Standard library only; no AI model, account or API key is needed.

```
python run_lab.py          # 13 checks; ends "13 of 13 checks passed."
python mutation_check.py   # breaks the code 15 ways; ends "Every mutation behaved as expected."
```

Scripts you can run on their own:

| File | What it shows |
|---|---|
| token_budget.py | Planning what fits in a window, with a safety margin; three overflow rules (refuse, drop oldest, keep system and last) |
| cache_cost.py | Break-even reads for cache writes; worked totals; Gemini storage break-even |
| cache_sim.py | A stand-in prompt cache: stable prefix, a timestamp that breaks it, lifetimes, the minimum length |
| placement_test.py | A needle-position test with 95% intervals, on two invented stand-ins, or on a local Ollama model |
| paper_numbers.py | Re-derives numbers the part quotes |

Optional reader tests (need your computer):

```
python -m pip install --require-hashes -r requirements-optional.txt
python run_lab.py --with-tiktoken                 # 14 checks; downloads o200k_base on first use
python placement_test.py --ollama MODEL --docs 200 --num-ctx 16384 --trials 10
```

Tested October 13, 2026 on Ubuntu 24.04 with Python 3.13.16, 3.12.3 and 3.11.17.
