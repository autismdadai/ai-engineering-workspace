# Works Cited audit, The Taxonomy of Prompt Engineering (Third Edition)

Checked 2026-10-15 by script against the primary records: the arXiv API (export.arxiv.org) for every arXiv ID, and Crossref for every DOI. Each automated match was then read by hand. Raw output: `bib-check.json`, `bib-check.md`. Scripts: `../tools/bibcheck2.py`.

## Result

| Check | Count | Result |
|---|---|---|
| Entries in Works Cited | 139 | |
| arXiv IDs | 124 | All 124 resolve to the paper named, with the right first author |
| DOIs | 8 | All 8 resolve (entries 12, 14, 73, 89, 106, 107, 114, 126) |
| Entries with no arXiv ID or DOI | 21 | Web pages, reports and books; checked separately (`web-sources.md`) |

No identifier points to the wrong paper, and no cited work is missing.

## Corrections and improvements

| # | What the manual says | What the record shows | Action |
|---|---|---|---|
| 73 | XGrammar-2, CAIS 2026, DOI 10.1145/3786335.3813124; the Third Edition removed "pp. 1009–1022" as unverified (changelog 27.1 #15) | Crossref: *Proceedings of the ACM Conference on AI and Agentic Systems*, pages 1009–1022 | Restore the page numbers; the second edition was right |
| 105 | DeepSeek-R1 cited as arXiv 2501.12948 only | arXiv journal reference: *Nature* 645, 633–638 (2025) | Add the Nature citation (now peer-reviewed) |
| 89 | *Hallucination-Free? Assessing Legal AI Research Tools* | Published title: *Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools*, J. Empirical Legal Studies 22:216–242 | Use the full title and page range |
| 18 | *Refusal Is Mediated by a Single Direction* | *Refusal in Language Models Is Mediated by a Single Direction* (Section 4.1 already has it right) | Use the full title |
| 44 | *Improving Factuality via Multiagent Debate* | *Improving Factuality and Reasoning in Language Models through Multiagent Debate* | Use the full title |
| 12 | Findings of EMNLP 2024 | Crossref adds pages 15126–15154 | Optional: add pages |
| 128 | *When LLMs Play the Telephone Game: Cumulative Changes and Attractors in Iterated Cultural Transmissions*, ICLR 2025 | Current arXiv title: *When LLMs Play the Telephone Game: Cultural Attractors as Conceptual Tools to Evaluate LLMs in Multi-turn Settings* | Use the title of the version cited (see `web-sources.md`) |

## Short names used as titles

Several entries give a technique's short name in the title position (APE, OPRO, ProTeGi, PAL, P-Tuning, Self-Ask, MIPROv2, Step-Back, Multi-Agent Debate, InstructGPT). The identifiers are right, but a reviewer checking titles will not find these titles. A format such as *OPRO: Large Language Models as Optimizers* keeps the label and makes the title checkable. Actual titles:

- 4 InstructGPT: *Training language models to follow instructions with human feedback*
- 36 Step-Back: *Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models*
- 43 Multi-Agent Debate: *Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate*
- 49 APE: *Large Language Models Are Human-Level Prompt Engineers*
- 50 OPRO: *Large Language Models as Optimizers*
- 53 ProTeGi: *Automatic Prompt Optimization with "Gradient Descent" and Beam Search*
- 57 MIPROv2: *Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs*
- 63 P-Tuning: *GPT Understands, Too*
- 95 Self-Ask: *Measuring and Narrowing the Compositionality Gap in Language Models*
- 103 HyDE: *Precise Zero-Shot Dense Retrieval without Relevance Labels*; GraphRAG: *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*

Entry 22's paper spells its own title "Langauge" (*Chain-of-Symbol Prompting Elicits Planning in Large Langauge Models*); like entry 60's "Promts", that is the paper's spelling.

## Not checkable by script

Venue claims that arXiv does not record (ICLR, NAACL, NeurIPS, COLM, ICML, USENIX) and the 21 entries without identifiers are checked in `web-sources.md`. DBLP refused scripted queries (HTTP 202 with empty body) and Semantic Scholar rate-limited batch requests, so those checks were done by reading the venue pages.
