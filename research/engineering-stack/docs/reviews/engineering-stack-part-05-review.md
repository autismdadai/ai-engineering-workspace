# Engineering Stack Part 05: Phase 4 Review

*October 13, 2026. The Phase 4 record for claude/engineering-stack-part-05-retrieval.md, in the finding format of claude/fabel-prompt-audit.md (number, severity, quote, what goes wrong, why with source, fix). Every finding was reproduced by the author before it was fixed, except four whose fix only removes or weakens wording (marked "not re-opened"); one that didn't reproduce is listed with that result. Raw reports went to the owner in engineering-stack-research-part-05.zip.*

## Who checked what

| Check | By | Scope | Result |
|---|---|---|---|
| Blind source check A | Fresh agent on Claude Sonnet, given only claims and source links | 81 claims: keyword, dense and hybrid search, stores, licences | 72 supported, 8 partly, 0 contradicted, 1 not checkable; 31 web lookups |
| Blind source check B | Fresh agent on Claude Sonnet, same rules | 79 claims: reranking, late interaction, chunking, metrics, RAG evaluation, Sections 4, 5, 9, 10 | 69 supported, 10 partly, 0 contradicted; 35 web lookups |
| Beginner test | Fresh agent following Sections 3 and 7 to 9 literally, fresh virtual environments | Python 3.13.16, 3.12.3, 3.11.17; core lab, cross-check install, the real-models install up to its download | 14 problems: 1 high, 4 medium, 9 low |
| Mutation check | The lab's own `mutation_check.py` | 16 deliberate breaks | First run caught 11 of 16; after five new test cases, 16 of 16 |
| Lead re-checks | The author | Elasticsearch licence gate, Qdrant's RRF formula, each finding below | See findings |

## Findings

| # | Severity | Quote (draft) | What goes wrong | Why, with source | Fix |
|---|---|---|---|---|---|
| 1 | High | "PyTorch (124.1 MB for torch 2.14.1 on Windows x86-64, 554.6 MB on Linux x86-64 ...)" | On Linux the install pulls far more: the tester's pip cache passed 2.2 GB before it was stopped | Reproduced from PyPI metadata: torch 2.14.1 requires `cuda-toolkit[...]==13.0.3`, `nvidia-cudnn-cu13` and others when `platform_system == "Linux"` | Section 7.5 and `requirements-real.txt` now say to install PyTorch's CPU-only build first, from the pytorch.org selector; Windows unchanged; macOS marked unchecked |
| 2 | Medium | "0.9 and 8.6 points above the single-vector models it compared" | RepBERT (30.4) is a single-vector model in the same table, so the gap reaches 9.3 | Reproduced: ColBERTv2 Table 4 (arXiv 2112.01488v3) lists RepBERT 30.4, DPR 31.1, RocketQAv2 38.8, ColBERTv2 39.7 | Now 0.9 to 9.3; Section 4 notes that ledger row P5-09 has the same slip (ledger not edited) |
| 3 | Medium | "four INFO lines" (7.4 and test R3) | `crosscheck.py` prints five | Reproduced: one line per question plus a summary | Changed to five |
| 4 | Medium | "on Linux, `python3 -m zipfile -e engineering-stack-lab-part-05.zip ~/ai-stack`" | Fails with `FileNotFoundError` unless run in the zip's folder | Reproduced on the test machine | Added "go to the folder that holds the zip first" and a row in 7.7 |
| 5 | Medium | (no row in 7.7) | A blocked model download ends in a long traceback with no explanation | Reproduced: huggingface-hub on the test machine ends in `ProxyError: 403 Forbidden` | New 7.7 row |
| 6 | Medium | MS MARCO, zero-shot, fine-tuned, "@10", "ledger P5-xx" used without explanation | A beginner can't follow Sections 3 and 4 | Reproduced by reading: none was defined before use | Five definition rows; a note on what the ledger is |
| 7 | Medium | "Raw scores range roughly from -10 to 10" [V: SCE] | The usage page and `model.py` don't say it | Reproduced: the sentence is in `docs/cross_encoder/pretrained_models.md` line 40 | Quoted and attributed to that page |
| 8 | Medium | "SPLADE (SIGIR 2021) and its later versions reach ... 34.0 and 38.8" | The README table starts at SPLADE v2 | Reproduced: naver/splade README lines 71-77 | Now "SPLADE v2 and later versions" |
| 9 | Medium | "with small differences in recall next to large spreads between questions" [V: CCR] | The report says strategy matters, "by up to 9% in recall" | Reproduced from the report's abstract | Quoted the report |
| 10 | Low | "TREC calls that **Success@k**" | ir_measures' sentence is about its own naming, following TREC's convention | Reproduced: ir_measures `measures/r.py` lines 8-9 | "ir_measures, following TREC's convention, calls that Success@k" |
| 11 | Low | "to put confidence intervals on the scores" (ARES) | The abstract names prediction-powered inference, not confidence intervals | Not re-opened by the author; the fix only removes wording the abstract doesn't show | Now names the method |
| 12 | Low | "the 12-layer MiniLM costs twice as much for no measured gain" | 960 against 1,800 documents per second is 1.9x; the gain is 0.01, small but measured; and the claim cited the wrong source | Reproduced from the model card numbers | "about 1.9x slower for a gain of 0.01", cited [V: MML]; added that PyLate's PLAID indexing has "no Sentence Transformers equivalent" (reproduced in `docs/migration_guide.md` line 61) |
| 13 | Low | "NumPy and SciPy" for bm25s | bm25s 0.3.13 requires only NumPy | Reproduced from PyPI `requires_dist` | "NumPy (SciPy optional, for indexing)" |
| 14 | Low | "Weaviate's hybrid search uses this idea" | Read as RRF; its default is relative-score fusion | Not re-opened by the author; the new wording uses only what the part's own researcher row and the checker both read | Describes `alpha`, the default and the rank-based option |
| 15 | Low | "so any two tend to look similar" [V: ETH] | The abstract says "not isotropic in any layer", nothing about similarity | Not re-opened by the author; the fix quotes the abstract and weakens the claim | Quoted, with the reading marked as interpretation |
| 16 | Low | "(d × 4 + M × 2 × 4) bytes per vector" [V: FAW] | FAISS's index table adds a factor x | Reproduced: `Faiss-indexes.md` line 9 against `Guidelines-to-choose-an-index.md` line 29 | Both forms given |
| 17 | Low | ranx "Slow but maintained" | A judgment | Release and last commit both August 7, 2025 | Dates stated instead |
| 18 | Low | Hosted rerankers "publish prices" | Only Voyage's page lists simple per-token prices | Not re-opened by the author; the fix removes the claim | Reworded |
| 19 | Low | Elasticsearch commit "October 14, 2026 UTC"; Lucene "lines 121-122" | The commit is 01:06 +0200, October 13 23:06 UTC; the default constructor is line 122 | Reproduced with `git log` and `grep` | Fixed both |
| 20 | Low | "shares no word"; "agree on every top 3" | Both texts contain "a"; two of the four "agreements" were both tools finding nothing | Reproduced from the corpus and the cross-check output | Reworded |
| 21 | Low | "DPR averaged 47.7% below BM25" | Relative or points? | BEIR Table 2 gives relative performance | "(relative to BM25's score, not percentage points)" |
| 22 | Low | Section 8, step 3 "Change q3" | A beginner may edit `corpus.py` | Reproduced by reading | "nothing in `corpus.py` needs editing" |
| 23 | Low | `$` convention; Mermaid shown as code; pip cache; tag-count scope | Small beginner confusions | Reproduced by reading and by counting | Notes added; header counts now start at Section 1 |
| 24 | Low | Ubuntu may lack `python3-venv` | Not reproduced: the test machine has it | Same note as Part 04 | Added as an [R] note |
| 25 | n/a | "Negation is mostly missed" | Checker B said NevIR's abstract says "many" | **Not reproduced**: the abstract reads "most information retrieval models (including SOTA ones) do not consider negation" | Kept |
| 26 | Medium | `run_lab.py`, first version | 5 of 16 mutations passed: RRF's default k, swapped convex weights, precision's divisor, an unsorted nDCG ideal, a wrong concept mapping | The mutation check's own first run | Checks 3c, 4c, 6b, 7 (precision@5) and 7b (unsorted grades) added; an unbroken-copy control added |
| 27 | Low | Check 8's expected values | Typed from rounded sums (0.4175, 0.8649, 0.8875) and failed | The run gives 0.4174, 0.8651, 0.8877 | Set from the run |
| 28 | Medium | `crosscheck.py`, first version | With nothing installed it printed three SKIP lines and exited 0 | Reproduced | Now fails with "nothing was checked" |
| 29 | Low | One claim (A015, "four steps") | Not checkable without the list | The checker got the sentence only | The diagram lists the steps; no change |

## Not changed, with reasons

- B005 (monoT5's 0.398): the published Findings version has 0.398; the arXiv version shows 0.382. The part cites the Findings version.
- B040 (Self-Route): the numbers match Table 1; the paper's prose gives slightly different ones. The part names Table 1's.
- Ledger row P5-09 (0.9 to 8.6): flagged in the part's Section 4, not edited, following the series' rule.
