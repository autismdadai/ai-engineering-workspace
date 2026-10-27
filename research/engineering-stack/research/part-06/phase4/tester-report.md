# Learner-tester report: Part 06, Graphs and Memory

Tester: beginner role, Linux, October 14, 2026. Fresh home folder: /home/claude/tester6/home. Inputs: /home/claude/tester6/engineering-stack-part-06-graphs-and-memory.md and engineering-stack-lab-part-06.zip.

(Report written as I go; problems and runs appended below.)

## Runs log

### Setup ("Before you start", Linux)
- `cd /home/claude/tester6` (the folder that holds the zip), then `python3 -m zipfile -e engineering-stack-lab-part-06.zip ~/ai-stack` with HOME=/home/claude/tester6/home: exit 0, folder `engineering-stack-lab-part-06` with 9 files, as the document says.
- The appendix listings of graph.py, memory.py, run_lab.py and mutation_check.py are byte-identical to the zip's files (extracted from the document and diffed).

### Core lab, Section 7.3, fresh venv each time (`<python> -m venv .venv`, `source .venv/bin/activate`)
| Python | pip in venv | demo.py | run_lab.py final line | mutation_check.py final line |
|---|---|---|---|---|
| 3.13.16 (python3) | 26.2.1 | exit 0, output as Sections 3.2, 3.3, 3.8 | `21 of 21 checks passed` (exit 0) | `16 of 16 mutations caught` (exit 0) |
| 3.12.3 (python3.12) | 24.0 | same, identical text | `21 of 21 checks passed` (exit 0) | `16 of 16 mutations caught` (exit 0) |
| 3.11.17 (python3.11) | 24.0 | same, identical text | `21 of 21 checks passed` (exit 0) | `16 of 16 mutations caught` (exit 0) |

Output was identical across the three versions. Every PASS line in Section 8 step 6 matches the real run word for word, except the two `[...]` placeholders (see problems).

### Section 7.4, networkx cross-check (fresh venv each time; `python -m pip install -r requirements-crosscheck.txt`, then `python crosscheck.py`)
| Python | pip | networkx installed | crosscheck.py output | exit |
|---|---|---|---|---|
| 3.13.16 | 26.2.1 | 3.7 | 3 PASS + `INFO networkx Leiden (modularity) finds 2 communities` | 0 |
| 3.12.3 | 24.0 | 3.7 | 3 PASS + `INFO networkx Leiden (modularity) finds 2 communities` | 0 |
| 3.11.17 | 24.0 | 3.6.1 | 3 PASS + `INFO networkx Leiden not usable here: NotImplementedError` | 0 |

All three match Section 7.4 exactly. Also confirmed:
- Before the install, `python crosscheck.py` prints `FAIL nothing was checked: install requirements-crosscheck.txt in this environment` and exits 1, as in 7.6 and 7.7.
- On 3.11, `python -m pip install networkx==3.7` ends `ERROR: No matching distribution found for networkx==3.7` (pip shows `3.7 Requires-Python !=3.14.1,>=3.12`), as in 7.7.
- In networkx 3.7, `leiden_communities` has `metric='cpm'` as its default (inspect.signature), as Section 3.3 and the cheat sheet say.
- `run_lab.py` still prints `21 of 21 checks passed` with networkx installed.
- The pip `[notice] A new release of pip is available: 24.0 -> 26.2.1` appeared on 3.11 only; on 3.12 it did not show (pip only checks about once a week, and the 3.13 run had just checked). 7.7 already says it is not an error.

### Section 8, step by step (Python 3.13.16 venv unless noted)
| Step | Command | Result | Matches doc? |
|---|---|---|---|
| 1 | read graph.py | `DOCS` has 10 notes, `RELATIONS` 4 patterns | yes |
| 2 | `python demo.py` | exact: 11 nodes, `no answer`; normalized: 10 nodes, `[('avery lin', ['n8', 'n2'])]` | yes |
| 3 | edit `ALIASES = {"ledger db": "ledger database"}` to `ALIASES = {}`, `python demo.py` | normalized graph: `11 nodes`, `no answer`, modularity 0.505 | yes. Restored afterwards; `cmp` with the original copy shows identical; `21 of 21 checks passed` again |
| 4 | `python -c "...follow('billing service', 'DEPENDS_ON', 'OWNED_BY', '^LEADS')..."` | `[('avery lin', ['n7', 'n8', 'n2'])]` | yes |
| 5 | by hand | Q = 0.5 (see arithmetic below) | yes |
| 6 | `python run_lab.py` | all 21 PASS lines identical to the block except the two `[...]` placeholders; `21 of 21 checks passed` | yes (see P1) |
| 7 | Section 7.4 | see table above | yes |
| auto | `python mutation_check.py` | `OK   the unbroken copy passes` ... `16 of 16 mutations caught`; first and last CAUGHT lines identical to the block | yes |
| 7.6 | `python -c "...follow('search service', 'OWNED_BY', '^LEADS')..."` | `[('rowan park', ['n4', 'n5'])]` | yes |

### Section 9
- Exercise 1: command prints `0.5`. By hand: m = 6, each triangle L = 3, degree sum 6; 2 x (3/6 - (6/12)^2) = 2 x (0.5 - 0.25) = 0.5. Correct.
- Exercise 2: no command given; I wrote `python -c "from graph import *; g = build_graph(DOCS, 'normalized'); print(g.follow('search service', 'DEPENDS_ON', 'OWNED_BY', '^LEADS'))"` by copying step 4. Prints `[('rowan park', ['n9', 'n10', 'n5'])]`. Correct.
- Exercise 3: no command given; needed memory.py to learn Fact's arguments. `Memory('temporal')`, Lisbon valid_at=10, Oslo valid_at=40: `as_of(..., 39)` gives `['Lisbon']`, `as_of(..., 40)` gives `['Oslo']`, Lisbon's invalid_at is 40. Answer and reason are correct.
- Self-check answers (2) to (5) agree with Sections 3.2, 3.5, 3.8, 3.10 and the lab. Answer (1) is slightly off (P6).

### Arithmetic checked by hand
- Section 3.3, two-team split of the resolved graph: Payments side edges n1, n2, n3, n7, n8 = 5; Discovery side n4, n5, n6, n9, n10 = 5; edges between = 0; m = 10; each side's degree sum = 2 x 5 = 10. Q = 2 x (5/10 - (10/20)^2) = 2 x 0.25 = 0.5. Correct.
- Section 3.3, the 0.505 for the unresolved graph: {Avery Lin, Finance group, Payments team, ledger DB}: L = 3, d = 7; {billing service, ledger database}: L = 1, d = 3; Discovery side: L = 5, d = 10. Q = (0.3 - 0.1225) + (0.1 - 0.0225) + (0.5 - 0.25) = 0.1775 + 0.0775 + 0.25 = 0.505. Correct.
- Section 3.5: 64.78 - 63.01 = 1.77 (text "about 1.8"); 63.01 - 60.04 = 2.97; 70.27 - 67.02 = 3.25; 331,375 / 879 = 376.99, so 377. All correct. Section 3.9: 66.88 - 52.90 = 13.98; 66.88 / 52.90 = 1.264, so 26% relative; 72.90 - 66.88 = 6.02. Correct. 100 - 65.8 = 34.2. Correct.
- Header tag counts: counting `[V`, `[T`, `[R`, `[U`, `[I` from Section 1 up to the Cheat sheet gives 150, 51, 6, 8, 5, as stated.

### Section 7.5 (not installed, reading only)
A beginner would understand that this is optional, outside the lab, and needs a server, an account or a model key. They would not know how to actually start: there is no link to the Neo4j download or AuraDB sign-up in 7.5 (the URL is only in Section 12), no word on which environment to install graphrag into, and no next command after the install (the `graphrag init` and `graphrag index` lines are only in the cheat sheet). That is acceptable for a section marked "not part of the lab"; see P11 for a small fix.

### Uninstall (7.8), tried on a throwaway copy
`deactivate`, `cd ..`, `rm -rf engineering-stack-lab-part-06` (exit 0), `python -m pip cache purge` (`Files removed: 12`, exit 0). It worked here only because this machine has a `/usr/bin/python` link (see P10).

## Problems

**P1. Medium. Section 8 step 6 and step 2 point to community lists in Section 3.3 that are not there.**
- Quote: "(`[...]` stands for the community lists, shown in full in Section 3.3's runs.)" and step 2: "Its graph and memory blocks are in Sections 3.2, 3.3 and 3.8".
- What happened: Section 3.3 has no output block and no community lists. It only describes them in prose ("Local moving alone stops at 4 small communities"). `python run_lab.py` prints, for check 6: `[['avery lin', 'finance group', 'payments team'], ['billing service', 'ledger database'], ['discovery team', 'product group', 'rowan park'], ['index store', 'search service']]`, and `python demo.py` prints a `communities (modularity 0.505):` / `(modularity 0.500):` block for each graph that appears nowhere in the document.
- Why it matters: a beginner goes looking for the expected lists to compare with, cannot find them, and cannot tell if their output is right.
- Fix: add the demo's two community blocks (with the 0.505 and 0.500 lines) as an output block in 3.3, or spell out the lists in step 6 instead of `[...]`.

**P2. Medium. Forgetting to restore the alias in step 3 makes run_lab.py crash with a traceback, not FAIL lines.**
- Quote: "Put the alias back." (step 3), followed by step 6 "Run the checks."
- What happened: with `ALIASES = {}` still in graph.py, `python run_lab.py` prints `FAIL 2b ...`, `FAIL 3 ...`, then `Traceback ... KeyError: 'ledger db'` from `modularity` at check 5, and no summary line. `python mutation_check.py` prints `STOP the unbroken lab fails run_lab.py; fix that first`.
- Why it matters: a beginner who skips the restore sees a crash that 7.7 doesn't mention and may think the lab is broken. "Put the alias back" also doesn't say the exact text to restore.
- Fix: in step 3, say "change it back to `ALIASES = {"ledger db": "ledger database"}`" and add a 7.7 row: "`KeyError: 'ledger db'` from run_lab.py: the alias edit from Section 8 step 3 is still in graph.py; put the alias back".

**P3. Medium. Exercises 2 and 3 give no command, and the document never shows how to create a Fact.**
- Quote: "With `Memory("temporal")`, store Lisbon on day 10 and Oslo on day 40." and 7.6: "`write(Fact(...))`, `current(...)`, `as_of(..., day)`".
- What happened: `Fact(...)` hides the arguments. I had to read memory.py (or the appendix) to find `Fact(subject, attribute, value, valid_at=...)`. A first guess like `python -c "from memory import *; m = Memory('temporal'); print(m.as_of('user', 'home_city', 39))"` prints `[]` because nothing was stored. Exercise 2 is easy to adapt from step 4, but exercise 3 is not.
- Why it matters: the "checked answer" can't be checked without code the reader isn't shown.
- Fix: give the command, e.g. `python -c "from memory import *; m = Memory('temporal'); m.write(Fact('user', 'home_city', 'Lisbon', valid_at=10)); m.write(Fact('user', 'home_city', 'Oslo', valid_at=40)); print(m.as_of('user', 'home_city', 39))"` (prints `['Lisbon']`), and in 7.6 write `Fact(subject, attribute, value, valid_at=day, source="user")`.

**P4. Medium. Benchmark jargon in Sections 1 to 3 is never explained.**
- Quotes: "zero-shot GPT-4 scored micro F1 15.5 on Re-TACRED relation extraction against 91.4 for the best fine-tuned model" (3.2); "NQ F1 64.78", "HotpotQA", "MultiHop-RAG accuracy" (3.5); "answer entities" (1, 3.2); "map-reduce", "Personalized PageRank" (3.4); "LoCoMo ... judge score" (3.9).
- What happened: F1, micro F1, zero-shot, fine-tuned, the dataset names (NQ, HotpotQA, Re-TACRED, MultiHop-RAG) and "answer entities" are not defined in Section 2 or anywhere in this part. They may be in Parts 02 and 05, but the text doesn't say so.
- Why it matters: the key evidence in 3.5 ("plain RAG did best on NQ, graphs on HotpotQA") only makes sense if you know NQ is single-fact questions and HotpotQA multi-hop. The self-check answer (2) relies on exactly that.
- Fix: add rows to Section 2 (F1 score, zero-shot vs fine-tuned, answer-entity coverage) and a one-line gloss for each dataset at first use, e.g. "NQ (Natural Questions: single-fact questions)", "HotpotQA (questions that need two passages)".

**P5. Medium. Section 2's table uses names before they are explained, and some are never expanded.**
- Quotes: "CoALA [V: COA]" (rows for working, episodic, semantic, procedural memory); "Sleep-time compute; "dreaming" (Letta)"; "Graphiti's edge fields"; "OWASP ASI06"; "A fact written as subject, predicate, object | Triple; RDF"; "The query language Neo4j introduced".
- What happened: CoALA is expanded only in 3.6; Letta and Graphiti are introduced in 3.7; OWASP in 3.10; Neo4j is described only in Section 6 ("Graph database server with Cypher"); RDF and W3C are never expanded.
- Why it matters: the definitions table is where a beginner looks first, and half the Notes column points at unknown names.
- Fix: expand on first use (e.g. "CoALA, a 2024 research framework for agent memory (3.6)", "RDF, the W3C's Resource Description Framework", "Neo4j, a graph database"), or add "see 3.x" after each name.

**P6. Medium. Self-check answer (1) doesn't match what Section 3.1 teaches.**
- Quote: "(1) Key-value properties on the nodes and on the relationships themselves [V: NPG, RDF]."
- What happened: Section 3.1 says RDF objects can be literals, "values such as strings, numbers, and dates", so a node in RDF can carry a value through a triple; the only thing 3.1 says RDF lacks is "a property on the edge" ("A detail about a link (since when) needs extra triples rather than a property on the edge"). A reader who answers from 3.1 says "properties on the relationship" and then sees "on the nodes" too.
- Why it matters: the answer key teaches a slightly different (and less accurate) contrast than the section.
- Fix: "Properties on the relationship itself (e.g. `since: 2024`); RDF needs extra triples for that. Nodes can carry values in both, as properties or as literal-valued triples."

**P7. Low. "Checks run on this part" is an unfilled placeholder.**
- Quote: "To be filled after Phase 4."
- Why it matters: a learner sees an internal workflow note and wonders if the part is unfinished.
- Fix: fill it in or remove the heading before publishing.

**P8. Low. The pip line "Ignoring networkx: markers ... don't match your environment" is not mentioned.**
- Quote (7.4): "This installs networkx 3.7 on Python 3.12 and later, or 3.6.1 on Python 3.11 [T]."
- What happened: every install begins with `Ignoring networkx: markers 'python_version < "3.12"' don't match your environment` (or `>= "3.12"` on 3.11).
- Why it matters: "Ignoring" sounds like a failure to a beginner.
- Fix: one sentence in 7.4 or a 7.7 row: "pip prints `Ignoring networkx: markers ...` for the line meant for the other Python versions; that's expected."

**P9. Low. Check 9 and its description don't match.**
- Quote (step 6): "Check 9 re-derives ... the two studies' gaps"; 3.5: "MultiHop-RAG accuracy 70.27 against 67.02 [T: the differences]".
- What happened: check 9's seven rows include two gaps, both from Han et al. (NQ 1.77, HotpotQA 2.97); none from the ICLR study, and the MultiHop-RAG gap (3.25) is not checked, although 3.5 tags it [T].
- Fix: say "Han et al.'s two gaps", and either add the 3.25 row to check 9 or narrow the [T] tag to the HotpotQA and NQ differences.

**P10. Low. The uninstall step may fail on a stock Ubuntu install.**
- Quote (7.8): "`deactivate`, move up one folder with `cd ..`, and delete the lab folder ... `python -m pip cache purge` empties pip's download cache [T]."
- What happened: on this machine it worked (`Files removed: 12`), but only because `/usr/bin/python` exists here. On a stock Ubuntu 24.04 without the `python-is-python3` package, `python` is not a command once the venv is deactivated and deleted, and Ubuntu's system python3 may not have pip. I could not reproduce that failure here, so this is a reader-risk note.
- Fix: run `python -m pip cache purge` before `deactivate`, or write `python3 -m pip cache purge`.

**P11. Low. Section 7.5 gives no starting point.**
- Quote: "For Neo4j, its official download or AuraDB Free (an account you create yourself); for GraphRAG, `pip install graphrag==3.3.0` and a model key".
- What happened: no link, no "make a new venv first", no next command; and it uses bare `pip` while every other section uses `python -m pip`.
- Fix: give the two URLs (they are in Section 12), say "in a separate virtual environment", write `python -m pip install graphrag==3.3.0`, and point to the cheat sheet's `graphrag init` line.

**P12. Low. Same number for two different results in 3.5 (worth re-checking against the source).**
- Quote: "NQ F1 64.78 against 63.01 for the best graph method" and "HotpotQA 63.01 (HippoRAG2) against 60.04".
- What happened: 63.01 appears as two different cells (NQ best graph method, HotpotQA HippoRAG2). That could be a coincidence or a copy error. I could not open the paper (no internet beyond PyPI), and check 9 uses the document's own inputs, so it can't catch it.
- Fix: re-read Han et al. Tables 1 and 2 for both cells.

**P13. Low. The lab graph is two disconnected pieces, and the text doesn't say so.**
- Quote (3.3): "splitting it into the two teams puts 5 edges inside each, and each side's degrees sum to 10".
- What happened: by hand, there are 0 edges between the teams, so the "two communities" are simply the graph's two connected pieces. Check 4b ("no path between unconnected names") tests the made-up name "nowhere", not two real nodes from different teams (`shortest_path('avery lin', 'rowan park')` would be the clearer test).
- Why it matters: a beginner may think Louvain discovered something subtle. And Leiden's fix ("connected communities") can't show up on a graph like this.
- Fix: one sentence: "No edge joins the two teams, so here the communities are just the two separate pieces; on real graphs they overlap." Optionally test 4b with two real nodes.

**P14. Low. Small orientation gaps.**
- Section 3.8's output block has no `$ python demo.py` line, though Section 7 says "A line starting with `$ ` in an output block is the command that produced it". Fix: add `$ python demo.py` and `...`.
- Check 6c prints `...: 3` with no unit. Fix: "3 communities".
- Step 1 "Open `graph.py`" doesn't say how (any text editor). 7.3 doesn't say how to check which version `python3` is (`python3 --version`) or that 3.11 and 3.13 on Ubuntu 24.04 need `python3.11-venv` / `python3.13-venv` rather than `python3-venv`.
- The text refers to project files a learner given only this document can't open (claude/engineering-stack-glossary.md, the claim ledger, the guide). Fix: say they are in the project, or link them.

## What worked
- Unzip with `python3 -m zipfile -e engineering-stack-lab-part-06.zip ~/ai-stack`: exit 0 (also creates `ai-stack` if missing). Running it from the wrong folder gives exactly the 7.7 `FileNotFoundError`.
- Core lab on Python 3.13.16 (pip 26.2.1), 3.12.3 (pip 24.0), 3.11.17 (pip 24.0): demo.py exit 0 with identical output; run_lab.py final line `21 of 21 checks passed`; mutation_check.py final line `16 of 16 mutations caught`.
- Cross-check: 3.13.16 and 3.12.3 with networkx 3.7, 3.11.17 with networkx 3.6.1: three PASS lines and the documented INFO line; exit 0.
- Every output block in Sections 3.2, 3.8 and 8 matches a fresh run, except the `[...]` placeholders (P1). Every `python -c` command prints exactly what the document says.
- The appendix listings are byte-identical to the zip's files.
- Every 7.7 error row I could trigger (wrong folder for unzip, crosscheck without networkx, networkx==3.7 on 3.11, `ValueError: outside /memories: ...`, pip notice) appears as described.
- The modularity arithmetic (0.5, 0.505), exercise 1 and all of 3.5's and 3.9's differences and ratios check out by hand.

Note on my own run: my first unzip command had a harness mistake (the `~` expanded to the real home before my HOME override), which put a copy in /root/ai-stack. I deleted it and redid the step with HOME exported. It isn't a document problem.
