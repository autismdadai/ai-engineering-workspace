# Engineering Stack, Part 10 lab: defences in code

Standard library only; Python 3.11 to 3.13. No model, account or API key.
Everything in the data is invented (example.com addresses, 555-01xx numbers,
documentation IP ranges, published test card numbers).

| File | What it is |
|---|---|
| `guard.py` | The defences: a tool-call gate with the Rule of Two, output cleaning, invisible-character stripping, pattern redaction, classifier arithmetic, licence buckets |
| `examples.py` | The invented email assistant, a stand-in model that obeys any instruction it reads, and a labelled record set |
| `demo.py` | A walk through all of it |
| `run_lab.py` | 28 checks; exit code 0 only if all pass |
| `mutation_check.py` | Breaks the lab 50 ways in a temporary copy; each must make `run_lab.py` fail |
| `crosscheck.py` | Optional: compares redaction with Microsoft Presidio's pattern recognizers and the Luhn check with python-stdnum, with network connections blocked and logged |
| `requirements-crosscheck.txt` | Pins for the cross-check (about 50 packages, about 380 MB) |

Run:

```
python run_lab.py
python mutation_check.py
python demo.py
```

Optional, in a virtual environment:

```
python -m pip install -r requirements-crosscheck.txt
python crosscheck.py
```

What this does not do: find names or street addresses (that needs a model,
such as Presidio with a spaCy model), detect prompt injection (no reliable
detector exists), or replace legal advice. See Part 10, Sections 3 and 10.
