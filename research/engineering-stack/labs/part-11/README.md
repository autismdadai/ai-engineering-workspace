# Engineering Stack, Part 11 lab: the arithmetic of running a model

Standard library only; Python 3.11 to 3.13. No model, GPU, account or key is needed for the core lab.

| File | What it does |
|---|---|
| `runmath.py` | The lab itself: weight counts, quantized file sizes (from llama.cpp's block layouts and its Q4_K_M rule), KV cache, decode ceilings, roofline, speculative decoding, paged KV memory, serving metrics |
| `run_lab.py` | 14 checks; exit code 0 only if all pass |
| `mutation_check.py` | Breaks the lab 31 ways in temporary copies; each must make `run_lab.py` fail |
| `demo.py` | Prints the part's worked tables |
| `reader_local.py` | Reader test R3: times a small model in Ollama and compares it with the bandwidth ceiling; `--self-test` runs against a stand-in |

Run, from this folder, with your virtual environment active:

```
python run_lab.py
python mutation_check.py
python demo.py
python reader_local.py --self-test
```

Expected: `14 of 14 checks passed`, `31 of 31 mutations caught`, and the self-test ending `Self-test passed`. Every number is a bound or an estimate, not a measurement; the part's Section 3 says where each input comes from.
