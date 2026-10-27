# Engineering Stack Part 06: Phase 4 Review

*October 14, 2026. The Phase 4 record for claude/engineering-stack-part-06-graphs-and-memory.md, in the finding format of claude/fabel-prompt-audit.md (number, severity, quote, what goes wrong, why with source, fix). Every finding was reproduced by the author before it was fixed, or is marked otherwise. Raw reports went to the owner in engineering-stack-research-part-06.zip.*

## Who checked what

| Check | By | Scope | Result |
|---|---|---|---|
| Blind source check A | Fresh agent on Claude Sonnet, given only claims and source links | 63 claims: graphs, GraphRAG, tools, picks | 56 supported, 6 partly, 0 contradicted, 1 not checkable; 29 web lookups |
| Blind source check B | Fresh agent on Claude Sonnet, same rules | 64 claims: memory, comparisons, examples, teaching, limits | 56 supported, 8 partly, 0 contradicted; 31 web lookups |
| Beginner test | Fresh agent following Sections 3 and 7 to 9 literally, fresh virtual environments | Python 3.13.16, 3.12.3, 3.11.17; core lab and the networkx install on all three | 14 problems: 0 high, 6 medium, 8 low |
| Mutation check | The lab's own `mutation_check.py` | 16 deliberate breaks | 15 of 16 on the first run; the miss was an equivalent mutant, replaced |
| Lead re-checks | The author | GraphRAG notice, Letta retirement, Mem0 add-only default and Leiden in networkx (in source); Edge et al. §5.1; Han et al. §3.4, Tables 1 and 5; the dates of the GraphRAG and Zep notices (git history) | See findings |

## Findings

| # | Severity | Quote (draft) | What goes wrong | Why, with source | Fix |
|---|---|---|---|---|---|
| 1 | Medium | "on comprehensiveness in 72% to 83% of comparisons" | The range is podcasts only; news is 72% to 80% | Reproduced: Edge et al. §5.1, "72-83% ... for Podcast transcripts" and "72-80% ... for News articles" | Both ranges given, with "global approaches" quoted |
| 2 | Medium | "answers by Llama-3.1-8B"; "used one 8-billion-parameter model" | Han et al. also used Llama-3.1-70B-Instruct | Reproduced: §3.4 names both | Says "mainly 8B, with 70B in further tables" |
| 3 | Medium | "graphs built by the larger GPT-4o did better" | The paper measured answer accuracy, not entity coverage, for GPT-4o-built graphs | Reproduced: Table 5, MultiHop-RAG, 75.08 against 71.17 with a 70B answering model | Gives what was measured |
| 4 | Medium | "HippoRAG2 ... the strongest graph method in both studies" | Community-GraphRAG local led on NQ; RAPTOR led on one novels column; the ICLR study names no overall winner | Checker A's table reads; Table 1 reproduced for NQ | "among the strongest" |
| 5 | Medium | "plain RAG matched or beat graph methods in both studies" | On the medical corpus HippoRAG2 led fact retrieval (66.28 against 64.73) | Checker A and B quoting Table 2; the 66.28 matches the researcher's table | Scoped to Han et al. and the novels corpus |
| 6 | Medium | "In 2026 alone: ... Kuzu was archived, ... Zep dropped its self-hosted edition" | Kuzu's archive is October 2025, Zep's notice June 2025 | Reproduced from git history (Zep commit f5f56a0, 2025-06-29) and the Kuzu banner | Dated list "since mid-2025" |
| 7 | Low | "with bug fixes and security updates only" | Not the README's words | Reproduced: "bug fixes and dependency updates as appropriate, particularly to address CVEs" | Quoted |
| 8 | Low | "graph methods gain about 3 points on multi-hop sets" | Only the best method; a triples-only method lost heavily | Table 1 reproduced | "the best graph method gained about 3 points ... and some lost" |
| 9 | Low | "strong position bias" | The paper says "clearly present" | Reproduced from §5.3 | Quoted |
| 10 | Low | "Memory for the current task only" | CoALA says "the current decision cycle" | Checker A quoting §4.1; the researcher's quote agrees | Reworded |
| 11 | Low | Quarantine cited with [V: AMT, OWA] in the self-check | No source read prescribes quarantine | Checker B; nothing in the researchers' rows says so | Labelled as the lab's own design |
| 12 | Low | Graphiti "needs Neo4j, FalkorDB or Neptune" | Kuzu is still listed, as deprecated | Checker B; the researcher's row agrees | Added |
| 13 | Low | "`pip install graphrag==3.3.0` ... indexing calls a model for every chunk" | Bare `pip`, no environment advice, "every chunk" an inference | Checker B; the dataflow doc says each text unit is analysed | `python -m pip`, a separate environment, `graphrag init`, "standard indexing has a model analyse each chunk"; download page added as a source (read by the author) |
| 14 | Medium | Section 8 points to community lists "shown in full in Section 3.3's runs" | Section 3.3 had no output block | Reproduced | `demo.py`'s graph output added to Section 3.3 |
| 15 | Medium | Section 8, step 3, "Put the alias back." | Left empty, `run_lab.py` crashed with `KeyError: 'ledger db'` | Reproduced | Check 5 now fails cleanly when the nodes change; exact text to restore given; row added to 7.7 |
| 16 | Medium | Exercises 2 and 3 | No commands to check the answers | Reproduced by reading | Commands added, run and matched |
| 17 | Medium | F1, zero-shot, fine-tuned, NQ, HotpotQA, Re-TACRED, RDF, W3C | Used without explanation | Reproduced by reading | Definitions added; product names pointed to their sections |
| 18 | Medium | Self-check 1, "properties on the nodes and on the relationships" | Conflicts with Section 3.1, where RDF nodes can carry literals | Reproduced by reading | Question and answer rewritten to edge properties |
| 19 | Low | Check 9 "the two studies' gaps" | Both gaps were Han et al.'s; the MultiHop-RAG gap wasn't checked | Reproduced | Check 9 now has 8 figures, including 3.25 |
| 20 | Low | pip's "Ignoring networkx: markers ..." | Looks like a failure | Reproduced | Explained in 7.4 |
| 21 | Low | `deactivate` then `python -m pip cache purge` | Outside the environment, `python` may not exist | Not reproduced (it exists here); moved anyway | Purge comes first |
| 22 | Low | Two "63.01" values in 3.5 | Looks like a copy error | Reproduced as a coincidence: NQ local and HotpotQA HippoRAG2 are both 63.01 | Text says so |
| 23 | Low | The lab's two teams | No edge joins them, so the split is obvious | Reproduced | Text says it's deliberate |
| 24 | Low | Check 6c prints ": 3" | No unit | Reproduced | ": 3 communities" |
| 25 | Low | Mutation "local moving accepts no-gain moves" | Caught by nothing: no ties occur on this graph, so it doesn't change the result | The first mutation run | Replaced with "local moving never moves a node"; reported in Section 8 |
| 26 | n/a | One claim (A021) | A lead-in sentence without its list | Not a defect | No change |

## Not changed, with reasons

- Checker A noted that ISO's page describes GQL as for "specifying and modifying" property graphs rather than "a query language"; the part's wording is a fair plain-language summary of a standard whose title is "Database languages, GQL".
- Checker B noted that the Mem0 paper doesn't name its judge model; the part doesn't claim it does.
- Ledger rows P3-05 and P3-06 are corrected in the part's Section 4, not in the ledger, by the series' rule.
