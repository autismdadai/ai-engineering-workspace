# Part 06 lab: a small knowledge graph and three kinds of agent memory

Companion to claude/engineering-stack-part-06-graphs-and-memory.md (The AI Engineering Stack, Part 06).
Standard library only; no model, database, account or API key is needed.

```
python demo.py             # triples, two graphs' answers and communities, three memory designs
python run_lab.py          # 21 checks; ends "21 of 21 checks passed"
python mutation_check.py   # breaks the lab 16 ways; ends "16 of 16 mutations caught"
```

| File | What it is |
|---|---|
| graph.py | Invented notes, a stand-in extractor, entity resolution, a property graph, modularity, Louvain |
| memory.py | Overwrite, add-only and temporal memory; a quarantine for untrusted writes; a safe path check |
| run_lab.py | The checks |
| mutation_check.py | Proves each check can fail |
| demo.py | Prints what the lab builds |
| crosscheck.py | Optional: compares with networkx (requirements-crosscheck.txt) |

Tested October 14, 2026 on Ubuntu 24.04 with Python 3.13.16, 3.12.3 and 3.11.17.
