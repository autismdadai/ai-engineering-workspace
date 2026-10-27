# Part 05 lab: keyword, dense and hybrid search, and how to measure them

Companion to claude/engineering-stack-part-05-retrieval.md (The AI Engineering Stack, Part 05).
The core lab is standard library only; no AI model, account or API key is needed.

```
python run_lab.py          # 19 checks; ends "19 of 19 checks passed"
python mutation_check.py   # breaks the lab 16 ways; ends "16 of 16 mutations caught"
python search_demo.py      # top 3 per method for each question; add a number to change RRF's k
```

| File | What it is |
|---|---|
| corpus.py | 12 invented chunks, 4 questions, relevance grades, and the stand-in's word-to-concept table |
| retrieval.py | BM25 (Lucene variant), a stand-in dense search, RRF, convex combination, metrics, a chunker |
| run_lab.py | The checks |
| mutation_check.py | Proves each check can fail |
| search_demo.py | Prints each method's results |
| crosscheck.py | Optional: compares with bm25s, rank_bm25 and ir_measures (requirements-crosscheck.txt) |
| real_models.py | Reader test: a real embedding model and reranker (requirements-real.txt; downloads models) |

Tested October 13, 2026 on Ubuntu 24.04 with Python 3.13.16, 3.12.3 and 3.11.17.
