# Engineering Stack, Part 12 lab: choosing and adapting a model

Standard library only; Python 3.11 to 3.13. No model, GPU, account or key is needed for the core lab. The sample data in `data/` is invented for teaching.

| File | What it does |
|---|---|
| `adaptmath.py` | The lab itself: weight counts from config files, LoRA parameter counts, training memory (full, LoRA, QLoRA), a fit check, OpenAI's fine-tuning dates, a decision guide, licence naming rules, a first shortlist |
| `datacheck.py` | Checks a fine-tuning data set: formats, examples a trainer would reject, duplicates, and test examples that leak from the training file |
| `run_lab.py` | 17 checks; exit code 0 only if all pass |
| `mutation_check.py` | Breaks the lab 33 ways in temporary copies; each must make `run_lab.py` fail |
| `demo.py` | Prints the part's worked tables |
| `reader_lora.py` | Reader test R3: trains a small LoRA adapter on your processor and compares PEFT's count with the lab's; `--plan` needs nothing extra |
| `data/train.jsonl`, `data/test.jsonl` | 12 and 4 invented chat examples, with one duplicate and one leak planted on purpose |

Run, from this folder, with your virtual environment active:

```
python run_lab.py
python mutation_check.py
python demo.py
python datacheck.py data/train.jsonl data/test.jsonl
python reader_lora.py --plan
```

Expected: `17 of 17 checks passed`, `33 of 33 mutations caught`, and the data check ending `2 problem(s) found` (the planted duplicate and leak; its exit code is 1 on purpose). Memory figures count model states only, not activations; the part's Section 3 says where each input comes from.
