# Engineering Stack Claim Ledger

*Audit of ai-reports/gemini-ai-engineering-stack.md ("The Modern AI Engineering Stack", made with Gemini Deep Research), October 9, 2026; corrections from the series' parts applied in Phase 5 on October 20, 2026 (Section 12); package versions re-checked on October 26, 2026 (Section 13). This is Phase 1 of claude/engineering-stack-prompt.md. Evidence class: project audit. Every verdict rests on a source opened on October 9, 2026, unless the row is tagged [U] or [I]. Rows about law or licences are information, not legal advice.*

## How to read this ledger

- **One row per claim, number, formula, named tool or citation.** IDs follow the paper: S0 is the introduction, P1 to P12 are the twelve pillars, B1 to B4 the four blueprints, C the conclusion, W1 to W33 the works cited.
- **Gemini cit.** The paper has no inline citation markers and no links, so works cited were matched to claims by topic. Every match is inferred. The cell says whether the matched citation opens and supports the claim.
- **Verdict:** confirmed; corrected (the right version is in the note); outdated (true once, not on October 9, 2026); overstated (direction right, strength or scope wrong); unsupported (no source found, or the cited source doesn't say it); illustrative (an invented example); not checked yet (deferred to the part that covers the topic, with what would settle it). The last label is not in the prompt's list; it is added so that nothing unchecked passes as checked.
- **Tag:** [V] verified against an opened source; [T] arithmetic run in this session (Section 5); [U] not checked yet; [I] illustrative, nothing to check.
- **Grade:** confidence in the verdict (1 to 10, a rating, not a probability), then the best source class behind it. OD official spec or docs (including package registries and vendor product pages), PR peer-reviewed, PP preprint, SB standards or foundation body, GOV government guidance, VB vendor blog or comparison, PB personal or independent blog, MC mirror or copy, AI AI-written.
- **Merged rows.** Where the claim inventory split one sentence into several claims, one row covers them and says so ("Covers P2-07 to P2-10"). The inventory's 170 claims became 163 rows: eight were merged and one (P10-09b) was added.
- **Sources** are keys such as `NVH`. Section 11 gives each key's title, URL, class and date. Locations (section, table, heading) are in the rows.
- **How the checking was done.** Seven checker agents, one per topic group with at most 40 web lookups each, opened the citations and primary sources and returned claim tables. Five were cut off by a usage limit and wrote up what they had found the next morning, without new lookups. The lead session re-opened the headline sources (marked ✓ in Section 11), filled the gaps the checkers could not reach, ran the arithmetic, and settled conflicts. Pages were read through a fetch tool that summarizes each page with a small model, so numbers were requested verbatim and anything that decides a verdict was read twice or from two sources. A blind verifier has not yet re-checked these rows; that happens per part in Phase 4.

## 1. Headline findings

1. **The paper isn't what it says it is.** It calls itself "an exhaustive, peer-reviewed framework" (S0-03). One of its 33 works cited is a peer-reviewed version of record (W26). Thirteen are vendor or personal blogs, 3 are mirrors or copies, 10 are preprints or preprint copies, and 3 did not open. Four entries cite one paper (Olsson et al.), and seven of its 16 sections cite nothing at all.
2. **Several named tools are retired or superseded on the run date.** The OpenAI Assistants API shut down on August 26, 2026 (P6-05). AutoGen is in maintenance mode (P6-05). LangServe has been deprecated since November 18, 2024, and its repository was archived on May 5, 2026 (P11-04). OpenAI has deprecated gpt-4 and gpt-4-0613, the paper's judge example, and schedules them to shut down on October 23, 2026 (P9-12). Llama Guard 4 has replaced Llama Guard 3 as Meta's newest (P12-03). The OWASP Top 10 for LLM Applications has a 2026 edition (P12-06). H100 is a previous generation: NVIDIA called Vera Rubin "in full production" on August 26, 2026 (P4-01).
3. **"Deterministic" is the paper's most repeated error (12 uses).** Deployed inference isn't deterministic even at temperature 0 (TML). Safety classifiers have published error rates (Llama Guard 3: F1 0.939 and false-positive rate 0.040 on Meta's internal English response set). Some NeMo Guardrails rails call an LLM. OWASP's 2026 edition says no reliable prevention mechanism for prompt injection exists today.
4. **"Harness engineering" is defined wrongly.** In 2026 use (OpenAI, February 11; Thoughtworks, February 17) it means designing an agent's working environment and feedback loops, not test scaffolding and sandboxes (P7-01).
5. **The hardware numbers are mostly right but mis-scoped.** 3,958 TFLOPS is FP8 with 2:4 sparsity (dense: 1,979). 132 SMs is the H100 SXM5 product, not the GH100 die (144). 900 GB/s NVLink counts both directions. Eight GPUs are not one "unified memory pool", and 5.6 kW is a ceiling, not a floor (P4-04 to P4-15).
6. **Three numbers have no source:** the "15%" MIPROv2 gain (P9-11; nearest real figure +10.3 points), "doubles tokens per second" for speculative decoding (P10-11; measured results run from slowdowns at high load to 3.55x at batch size 1), and "rarely compute-bound" (P4-05).
7. **The induction-heads story is presented as settled** ("verified peer-reviewed analyses", "causal reality"). Olsson et al. is not peer-reviewed, and its authors call their large-model evidence preliminary. A peer-reviewed 2025 study of 12 models (Yin & Steinhardt, ICML 2025) finds few-shot learning depends mainly on function-vector heads. This also touches the project's own taxonomy (Section 9).
8. **The HIPAA example is wrong as stated (B4-08).** The Security Rule covers ePHI that is "maintained", not only transmitted, and requires administrative, physical and technical safeguards, so local processing alone does not make a system compliant. Cloud use isn't a "non-starter" either: HHS says covered entities may use a cloud provider under a business associate agreement (B4-01). Information, not legal advice.
9. **The skeleton is sound.** The mechanisms it names are real and mostly described correctly: RRF and its k = 60 default, MaxSim, semantic entropy, speculative decoding's acceptance rule, PagedAttention's paging analogy, RadixAttention's radix tree and LRU eviction, LangGraph's checkpoints and interrupts, and gVisor's Sentry and platforms. The errors are in strength, scope, freshness and attribution.
10. **Coverage gaps.** It has nothing on the Model Context Protocol, Agent Skills, fine-tuning, observability and tracing, provider prompt caching and batch APIs, reasoning models, building evaluation data, multimodal and computer-use agents, or licensing and data governance. These are handled in claude/engineering-stack-plan.md.

## 2. The 33 works cited

| W | As printed (shortened) | Opens? | What it actually is | Class | Matched to (inferred) | Supports? | Replace with |
|---|---|---|---|---|---|---|---|
| 1 | Induction Heads: The Mechanism of In-Context Learning (contextjamming.com) | yes | Explainer page summarizing Olsson et al.; no byline or date | PB | P1-03 to P1-07, P1-14 | Repeats the pattern and the PCA turn; nothing on peer review | OLS |
| 2 | In-context Learning and Induction Heads, alphaXiv | yes | Viewer page for arXiv 2209.11895 with an AI-written overview whose figures ("1-2 billion tokens", "about 250% improvement") are not in the paper | MC | P1-03, P1-04 | Abstract only; lists no venue | OLS |
| 3 | In-context Learning and Induction Heads, Transformer Circuits Thread | yes | The original article (Anthropic, March 8, 2022); no venue, no peer review | PP | P1-03 to P1-07, P1-14 | P1-04, P1-06, the early window; not "peer-reviewed" | itself |
| 4 | [2209.11895] arXiv | yes | arXiv copy, v1 only (September 24, 2022), no journal reference | PP | same | P1-04 | cite with W3 |
| 5 | SGLang: Efficient Execution of Structured Language Model Programs (arXiv v2) | yes | Latest arXiv version (June 6, 2024) of a NeurIPS 2024 paper | PP | P2-01, P2-04 to P2-14 | P2-05 to P2-10, except DFS for matching | SGL (proceedings) |
| 6 | Efficiently Programming LLMs using SGLang (arXiv v1) | yes | The same paper, first version, old title | PP | same | as W5 | merge into W5 |
| 7 | NVIDIA H100 8x 80GB SXM Server Review (Catalyst Data Solutions) | yes | Reseller's buyer's guide (March 31, 2026) | VB | P4-01 to P4-17 | P4-02, P4-03, P4-07, P4-13; origin of the "unified memory pool" heading and 5.6 kW | NVH, DGX |
| 8 | NVIDIA H100 Specs (2026) ... Datasheet (Spheron) | yes | GPU rental provider's blog (May 20, 2026; updated September 17, 2026); does not cite the datasheet | VB | P4-02 to P4-13 | Labels 3,958 as sparse and dense as 1,979; states the E4M3/E5M2 mapping | NVH, NVB |
| 9 | NVIDIA Hopper Architecture In-Depth (NVIDIA Technical Blog) | yes | NVIDIA's launch-time architecture post (March 22, 2022; modified July 22, 2025); some preliminary numbers | OD | P4-02 to P4-17 | P4-04 (144/132/114 SMs), P4-07, FP8 formats | itself, plus NVH for final numbers |
| 10 | Unpacking the NVIDIA H100 ... (hawkvelt.id.au) | yes | Personal blog, likely AI-assisted (leftover "oaicite" markers); stale 3 TB/s | PB | P4-02 to P4-13 | P4-02, P4-07, P4-13 only | NVH |
| 11 | Reciprocal rank fusion, Elasticsearch Reference | yes | Official docs; rank_constant default 60; ranks start at 1 | OD | P5-02 to P5-06 | P5-02 to P5-05 | itself; COR for the method |
| 12 | Reciprocal Rank Fusion ... (Redis blog) | yes | Vendor blog (August 9, 2026), prose only | VB | P5-02 to P5-06 | P5-03, P5-05; its own example gives 1.9x, not "vast" | COR |
| 13 | Flash-MaxSim (arXiv 2605.29517v3) | yes | IBM Research preprint on a GPU kernel for MaxSim (FMS) | PP | P5-07 to P5-09 | P5-08 formula only; no accuracy comparison | COL, CB2 |
| 14 | arXiv:2112.01488v3 (stamp line only) | yes | The ColBERTv2 paper (arXiv version of July 10, 2022) | PP | P5-07 to P5-09 | P5-07, P5-08; P5-09 only modestly | CB2 |
| 15 | What is gVisor? (Northflank blog) | yes | Vendor blog (April 16, 2026), promotional | VB | P7-03 to P7-09 | P7-03; unsourced microVM figures | GVD |
| 16 | What is gVisor? (gvisor.dev/docs) | yes | Official docs; its Gofer text still says 9P (stale) | OD | P7-03, P7-06 | P7-03 | itself, plus GVF |
| 17 | Platform Guide (gVisor) | yes | Official docs: systrap the default since mid-2023; ptrace no longer supported | OD | P7-05 | P7-05 | itself |
| 18 | gVisor vs Edera (docs.edera.dev) | yes | A competitor's comparison (March 7, 2026) | VB | P7-03 to P7-07 | P7-03; says directfs is the default | GVD, GVF |
| 19 | Detecting hallucinations ... semantic entropy (ResearchGate) | no (2 tries) | Mirror listing of the Nature paper | MC | P9-02 to P9-05, P9-10 | not readable | FAR |
| 20 | Semantic Energy ... (OpenReview PDF) | no (3 tries) | A different method (probably arXiv 2508.14496, seen in search results only) | PP? | P9-02, P9-10 | cannot support semantic-entropy claims | FAR |
| 21 | Prompt Triage ... (arXiv 2511.11898v1) | yes | Stanford preprint: DSPy optimizers on medical-imaging benchmarks; internal inconsistencies | PP | P9-06 to P9-08, P9-11 | no 15% figure | MIP, DSD, GEP |
| 22 | MIPROv2 vs GEPA in DSPy (particula.tech) | yes | Vendor blog (June 24, 2026) relaying the GEPA paper | VB | P9-06 to P9-08, P9-11 | uncited restatements; no 15% | DSD, GEP |
| 23 | Is It Time To Treat Prompts As Code? (arXiv 2507.03620v1) | yes | University of Minho preprint: DSPy case studies | PP | P9-06, P9-11 | P9-06 wording; no 15% | MIP |
| 24 | DSPy Optimizers Explained: 2026 Comparison (Future AGI) | yes | Vendor blog (May 29, 2026); its "13 percent aggregate" does not match the GEPA paper | VB | P9-06 to P9-08 | uncited restatements | DSD, GEP |
| 25 | sources/arxiv-2309.06180.md (Hugging Face dataset, pull-request ref) | no | A copy of the vLLM paper on an unmerged pull-request ref | MC | P10-01 to P10-04 | not readable | VLL |
| 26 | Fast Inference from Transformers via Speculative Decoding (PMLR) | yes | ICML 2023 paper, version of record | PR | P10-05 to P10-07, P10-11 | P10-05 to P10-07 | itself |
| 27 | Fast Inference ... (arXiv 2211.17192) | yes | arXiv copy of W26 | PP | same | same | merge into W26 |
| 28 | Purifying Finetuning Data to Preserve LLM Safety Alignment (arXiv 2507.18631v2) | yes | Preprint on filtering fine-tuning data (LARF); uses Llama Guard 3 only as an evaluator | PP | P12-03, P12-04 | at most "Llama Guard 3 is an 8B safety classifier" | LG3 |
| 29 | Do Encoders Suffice? (arXiv 2606.25782) | yes | Preprint (PwC) comparing safety judges for red-team evaluation | PP | P12-03, P12-04 | argues against P12-04 (Llama Guard 4 false-negative rate 0.658 on its holdout set) | LG3, LG4, NAS |
| 30 | LangGraph vs. AutoGen vs. CrewAI (JetBrains) | yes | Vendor guide page, no date | VB | P6-05, B1-02 to B1-06 | B1-02 partly; no "vastly superior" | LGD, CRD |
| 31 | Top Agent Frameworks To Use in 2026 (Splunk) | yes | Vendor blog (September 22, 2026); sells observability for these frameworks | VB | P6-05, B1-02 to B1-06 | B1-02, B1-03, B1-07; probable origin of B1-06; lists Microsoft Agent Framework, not AutoGen | LGD, CRD, MAF |
| 32 | Claude Managed Agents vs. LangGraph vs. CrewAI (Till Freitag) | yes | Consultancy post (April 9, 2026), unsourced numbers | VB | B1-02 to B1-06 | B1-05's "fastest" opinion only | LGD, CRD |
| 33 | Crewai vs LangGraph (TrueFoundry) | yes | Vendor blog (June 12, 2026); sells a gateway for both | VB | B1-02 to B1-07 | B1-02, B1-07 | LGD, CRD |

**Tally.** Blogs and vendor comparisons: 13 (W1, W7, W8, W10, W12, W15, W18, W22, W24, W30 to W33). Mirrors: 3 (W2, W19, W25). Preprints or preprint copies: 10 (W4 to W6, W13, W14, W21, W23, W27 to W29). The original lab article: 1 (W3). Official docs: 4 (W9, W11, W16, W17). Peer-reviewed version of record: 1 (W26). Unknown: 1 (W20). Three did not open (W19, W20, W25). Sections with no matching citation: P3, P6, P8, P11, B2, B3, B4. Two cited pages carry text aimed at AI assistants ("Summarize with AI" buttons on W12 and W33, a "Hey AI, learn about us" link on W33); none was followed.

## 3. Claim rows

### Introduction (S0)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| S0-01 | The field has "definitively" become a "rigorous, deterministic systems discipline" | framing | none | overstated [V] | 7 VB | TML ("How nondeterministic are completions?") | No source says "definitively". Deployed inference isn't deterministic even at temperature 0: 1,000 completions of one prompt gave 80 distinct outputs on Qwen3-235B-A22B-Instruct-2507 with default kernels (company report, September 2025). |
| S0-02 | Prompting works by "mathematical manipulation of transformer attention weights" | mechanism | W1 to W4: open; no | overstated [V] | 6 PP | OLS ("Key Concepts"); ACE | A prompt supplies tokens; the model computes attention scores from them, and its learned weights don't change (P1-01). No opened source describes prompting as manipulating attention weights. |
| S0-03 | The report is "an exhaustive, peer-reviewed framework" | self-description | none | corrected [V] | 10 AI | Section 2 of this ledger | An AI-written synthesis, not peer-reviewed. One of its 33 works cited is a peer-reviewed version of record. It omits MCP, fine-tuning, observability, prompt caching and licensing. |
| S0-04 | Twelve pillars and four blueprints cover the stack | scope | none | overstated [V] | 7 AI | claude/engineering-stack-plan.md, Section 1 | The structure exists as stated; the coverage claim is too strong (gaps are listed in the plan). |

### 1. Prompt engineering (P1)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| P1-01 | Prompting conditions the output distribution without gradient updates to the weights | mechanism | none | confirmed [V] | 7 PR | COA §4.1; OLS "Key Concepts: In-context Learning" | Definitional. CoALA says language models are stateless across calls; Olsson et al. measure in-context learning inside one context, with weights fixed. |
| P1-02 | Formula P(output given context) | formula | none | confirmed [V] | 8 PR | project taxonomy §3; COA §4.1 | Standard notation for an autoregressive model's conditional distribution. The PDF printed it as raw LaTeX source. |
| P1-03 | "Verified peer-reviewed analyses" show in-context learning is driven by induction heads that form in a narrow, abrupt window early in training | attribution + mechanism | W1 to W4: open; partly | corrected [V] | 9 PP | OLS (header; Introduction; Argument 1); W4 metadata | Olsson et al. is a Transformer Circuits article plus an arXiv preprint, not peer-reviewed. The abrupt early window is right: about 2.5 to 5 billion training tokens in their model sweep. "Driven by" is their hypothesis, with causal evidence only for small attention-only models. |
| P1-04 | An induction head finds an earlier copy of the current token, attends to the token after it (prefix matching) and raises its logit (copying): [A][B] ... [A] → [B] | mechanism + formula | W3, W4: open; yes | confirmed [V] | 9 PP | OLS "Key Concepts: Induction Heads"; arXiv 2209.11895 abstract | A behavioural definition, tested on repeated random tokens. Covers P1-04 and P1-05. |
| P1-06 | The formation shows as a turn in the training trajectory, seen with PCA | mechanism | W3: opens; yes | confirmed [V] | 8 PP | OLS Argument 1, "Per-Token Loss Analysis" | PCA of per-token loss vectors across checkpoints (output space, not weight space). Descriptive, not a causal test. |
| P1-07 | This explains why few-shot examples "drastically" improve abstract pattern matching | causal claim | W1 to W4: open; partly | overstated [V] | 8 PR | CRO abstract; YIN (PMLR 267); OLS Argument 6 | Ablating a few induction heads in Llama-3-8B and InternLM2-20B cut abstract pattern-task accuracy by up to about 32% (CRO, preprint). But across 12 models, few-shot learning relied mainly on function-vector heads, more so in larger models (YIN, ICML 2025). Nothing supports "drastically". |
| P1-08 | Tools: OpenAI API, Anthropic Workbench, DSPy, Promptfoo | named tools | none | confirmed [V]; Workbench [U] | 7 OD | OSO; PYPI (dspy 3.4.0, September 25, 2026, MIT); PFO README; NPM (promptfoo 0.124.1, October 8, 2026) | All but Workbench re-checked. Promptfoo's README says it "is now part of OpenAI" and stays MIT-licensed. OpenAI's docs moved to developers.openai.com. Workbench: settle in Part 03 from Anthropic's Console docs. |
| P1-09 | Zero-shot role prompting "enforces output determinism" for JSON ticket routing | example + mechanism | none | unsupported [V] | 8 OD | TML; OSO "Introduction" | Run-to-run sameness depends on the inference stack (TML: 80 distinct outputs in 1,000 temperature-0 runs of one prompt; 1 with batch-invariant kernels). Format comes from schema enforcement, not from a role. |
| P1-10 | Three few-shot demonstrations for legal entity extraction | example | none | illustrative [I] | - | - | Invented. Few-shot practice is covered in the taxonomy §7.2. |
| P1-11 | A system prompt can "severely penalize" out-of-character tokens | mechanism | none | unsupported [V] | 6 OD | OSO; OpenAI Chat Completions reference (logit_bias section not read) | A prompt shifts probabilities softly. Hard token control is a decoding-time setting (logit_bias, not read here) or constrained decoding. Settle logit_bias in Part 03. |
| P1-12 | Curriculum: tokenization and BPE explain how text becomes vectors | curriculum | none | illustrative [I] | - | - | A teaching suggestion; Part 03 will source it. |
| P1-13 | Curriculum: separate system, user and assistant roles | curriculum | none | illustrative [I] | - | ATU; OFC | Roles exist in both vendors' APIs. Any priority among them is trained, not architectural (taxonomy §3). |
| P1-14 | Induction heads give the "mechanistic, causal reality" of few-shot learning | causal claim | W3, W4: open; no | overstated [V] | 9 PR | OLS Introduction, Arguments 3 and 6; YIN | The authors claim strong causal evidence only for small attention-only models; for large models their evidence is correlational ("preliminary and indirect" in the abstract). YIN (ICML 2025) finds function-vector heads matter more for few-shot learning in larger models. |
| P1-15 | Schema enforcement bridges text and "deterministic software execution" | tool + mechanism | none | overstated [V] | 8 OD | OSO "Introduction"; "Structured Outputs vs JSON mode" | Structured Outputs guarantees adherence to the supplied JSON Schema. It doesn't guarantee correct values or identical reruns. |

### 2. Context engineering (P2)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| P2-01 | Self-attention cost is quadratic, O(N^2) | formula | W5, W6: open; no | confirmed [V] | 9 PR | VAS Table 1 (p. 6) | O(n²·d) per layer for full self-attention (n tokens, d dimensions). |
| P2-02 | Attention quality "frequently degrades" with length; in "lost in the middle" models "ignore" mid-prompt information | finding | none | overstated [V] | 8 PR | LIU §2.3, §3.2; RUL; NOL; CHR | 2023 models (GPT-3.5-Turbo, Claude-1.3, MPT-30B-Instruct, LongChat-13B) were less accurate mid-context, not blind (a U-shaped curve). Length degradation is robust: about half of 17 models hold up at 32K (RULER); 11 of 13 fall below half their short-context score at 32K (NoLiMa); all 18 degraded (Chroma, July 2025). Chroma's needle test found no notable position effect. |
| P2-03 | The context window is a finite, curated resource | framing | none | confirmed [V] | 9 VB | ACE "Why context engineering is important..." | Anthropic's own definition (September 29, 2025). |
| P2-04 | Context engineering "inherently" involves manipulating the KV cache | mechanism | W5, W6: open; no | corrected [V] | 8 OD | ACE; APC; SGL §3 | Three separate things: choosing what goes in the context (application), provider prompt caching (you mark stable prefixes), and server-side KV reuse (inside an engine you run). Anthropic's context-engineering post never mentions the KV cache. |
| P2-05 | A prompt produces key and value tensors per token; recomputing shared prefixes wastes compute | mechanism | W5, W6: open; yes | confirmed [V] | 9 PR | VLL §2.2; SGL §3; APC "Cache storage and sharing" | Reuse needs an identical prefix (Anthropic: 100% identical segments). Covers P2-05 and P2-06. |
| P2-07 | RadixAttention reuses KV automatically through a radix tree, matches prefixes by "depth-first search", and evicts LRU with reference counting | mechanism | W5, W6: open; partly | corrected [V] | 8 PR | SGL §3, Theorem 3.1, Appendix A.2 Algorithm 1 | All confirmed except the DFS part. Prefixes are matched by radix-tree lookup; depth-first order is the paper's optimal scheduling order for queued requests (offline case). Covers P2-07 to P2-10. |
| P2-11 | Anthropic's guidance, SGLang and LangChain are "critical" tools | named tools | none | overstated [V] | 5 VB | ACE; APC; SGL | Real tools; "critical" is a judgment no source makes. SGLang matters to people running their own servers; hosted-API users get prefix caching from provider features. |
| P2-12 | Example: sliding-window truncation that keeps system instructions through KV reuse | example | none | illustrative [I] | - | - | - |
| P2-13 | Advice: put aggressively summarized documents in the middle to fight attention decay | advice | none | unsupported [V] | 6 PR | LIU §4.2, §5; CHR | Liu et al. suggest reranking so relevant passages come first, truncating long retrieved lists, and (for key-value retrieval) repeating the query before and after the data. No source recommends summaries in the middle, and summarizing can drop needed facts. |
| P2-14 | SGLang serves "thousands" of parallel requests sharing one system prompt without recomputing it | example claim | W5: opens; no | overstated [V] | 7 PR | SGL §6 | No "thousands" figure. Production cache hit rates were 52.4% and 74.1% (Chatbot Arena, one month, low traffic). LRU eviction can drop the prefix. |
| P2-15 | The KV cache grows linearly with sequence length | mechanism | none | confirmed [V][T] | 8 PR | VLL §3 "Large KV cache" | OPT-13B in FP16: 2 × 5,120 × 40 layers × 2 bytes = 819,200 bytes (about 800 KiB) per token, so 2,048 tokens take about 1.68 GB (Section 5). Holds for standard attention. |
| P2-16 | Curriculum: caching middleware that tracks tokens and evicts stale context | curriculum | none | illustrative [I] | - | - | - |

### 3. Memory engineering (P3)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| P3-01 | Generation is stateless; the model has no persistent memory outside its frozen weights | mechanism | none | confirmed [V] | 8 PR | COA §4.1; MEM abstract | True per call; product memory features are built around the model. |
| P3-02 | Memory engineering "relies on" a three-part taxonomy: episodic, semantic, procedural | taxonomy | none | corrected [V] | 8 PR | COA §4.1 | CoALA defines four modules: working memory plus three long-term ones (episodic, semantic, procedural). MemGPT uses a different two-tier scheme. |
| P3-03 | Episodic memory is "typically" kept in NoSQL databases or run through MemGPT | practice | none | unsupported [V] | 7 PR | COA §4.1, §4.3; MEM §2.2 | CoALA names no storage technology, and nothing supports "typically". |
| P3-04 | In embedding space, proximity "equates to" semantic similarity | mechanism | none | not checked yet [U] | - | - | Settle in Part 05 with the embedding model's docs and a measured failure case. |
| P3-05 | Procedural memory stores executable skills, rules and configurations | definition | none | not checked yet [U] | - | - | Settle in Part 06 against CoALA's definition. |
| P3-06 | Memory reads and writes run asynchronously in parallel with the model | mechanism | none | not checked yet [U] | - | - | A design choice in some systems; settle in Part 06 from Letta's docs. |
| P3-07 | "Strictly necessary" tools: MemGPT ("illusion of infinite context"), Redis ("sub-millisecond"), Pinecone, ChromaDB, Qdrant | tools + number | none | overstated [V] | 8 PP | MEM abstract, §1; LET; PYPI (letta 0.34.8) | No source calls any tool necessary. MemGPT does use "the illusion of an infinite context" for its paging design, and MemGPT is now part of Letta (September 23, 2024). Redis latency: settle in Part 06. |
| P3-08 | Examples: preference recall, scratchpads, vector-indexed history | examples | none | illustrative [I] | - | - | - |
| P3-09 | Curriculum: a MemGPT-style loop where the agent manages its own memory | curriculum | none | confirmed [V] | 9 PP | MEM §2.2 to §2.4 | The model's function calls move data between main context and recall or archival storage. |

### 4. Rack and infrastructure engineering (P4)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| P4-01 | AI infrastructure is centred on NVIDIA Hopper | currency | W7 to W10: open; no | outdated [V] | 8 OD | NQ2 (August 26, 2026); RUB (January 5, 2026); NVH | Hopper is a previous generation. Blackwell is current, and NVIDIA called Vera Rubin "in full production" with racks at partners. Hopper is still sold and deployed. |
| P4-02 | H100 SXM5 has 80 GB of HBM3 | number | W7 to W10: open; yes | confirmed [V] | 10 OD | NVH spec table | SXM only; H100 NVL has 94 GB. |
| P4-03 | Up to 3.35 TB/s memory bandwidth | number | W7 to W10: open; yes | confirmed [V] | 10 OD | NVH | NVIDIA's 2022 launch post said 3 TB/s (preliminary). |
| P4-04 | 132 SMs "on the GH100 die" | number | W9: opens; corrects it | corrected [V] | 9 OD | NVB "NVIDIA H100 GPU architecture in-depth" | The full GH100 die has 144 SMs; H100 SXM5 enables 132 and H100 PCIe 114. |
| P4-05 | Multi-node training is "rarely" compute-bound and usually interconnect-bound | claim | W7: opens; no | unsupported [V] | 5 VB | W7 | No opened source says this. Which limit binds depends on model size, parallelism, batch size and overlap. |
| P4-06 | Fourth-generation NVLink and NVSwitch "resolve" that bottleneck | mechanism | W9: opens; partly | overstated [V][T] | 8 OD | DGX "Component Descriptions"; NVB | They raise bandwidth inside one node (900 GB/s per GPU, 450 each way). Between DGX H100 nodes, traffic uses eight ConnectX-7 NICs at up to 400 Gb/s (50 GB/s each way), about 9x less per GPU (Section 5). |
| P4-07 | NVLink gives 900 GB/s bidirectional | number | W9: opens; yes | confirmed [V] | 10 OD | NVH; NVB | 18 links; 900 GB/s counts both directions; about 7x PCIe Gen5 x16 (128 GB/s). |
| P4-08 | Eight GPUs act as a "unified memory pool" | mechanism | W7: opens; heading only | overstated [V] | 8 OD | DGX "Component Descriptions"; NVB | NVIDIA lists 640 GB total GPU memory. Each GPU keeps its own HBM3 and reaches its peers over NVLink. The phrase comes from W7's heading (a reseller's blog). |
| P4-09 | The Transformer Engine runs FP8: E4M3 for forward-pass weights and activations, E5M2 for gradients, with dynamic scaling | mechanism | W8, W9: open; partly | confirmed [V]; mapping [U] | 6 OD | NVB "Hopper FP8 data format", "Transformer engine"; W8 | NVIDIA confirms both formats and per-layer scaling; the Transformer Engine's Hopper default is delayed scaling, and Blackwell's default recipe uses E4M3 throughout (Phase 5, §12). The forward/gradient mapping is stated only by W8 (a vendor blog); settle in Part 11 from NVIDIA's Transformer Engine docs. Covers P4-09 to P4-11. |
| P4-12 | "Nearly 3,958 sparse TFLOPS" per GPU | number | W8, W9: open; yes | confirmed [V][T] | 9 OD | NVH spec table and its "* With sparsity" footnote | Exactly 3,958 FP8 TFLOPS with 2:4 sparsity. Dense FP8 is half, 1,979 (Section 5); NVIDIA prints FP16 and BF16 as 1,979 with the same footnote. A theoretical peak. |
| P4-13 | 700 W thermal design power | number | W8, W9: open; yes | confirmed [V] | 10 OD | NVH | "Up to 700W (configurable)". |
| P4-14 | Tools: CUDA, Slurm, Kubernetes, vLLM | named tools | none | confirmed (vLLM) [V]; others [U] | 6 OD | PYPI (vllm 0.31.0) | Settle the rest in Part 11. |
| P4-15 | 8x H100 data-parallel training draws "upwards of 5.6 kW" of GPU power | number | W7: opens; yes | overstated [V][T] | 6 OD | DGX "Power Specifications"; W7 | 5.6 kW is 8 × 700 W, the GPUs' combined ceiling (Section 5), not a floor. A DGX H100 system is rated at up to 10.2 kW in total. No measured training power was opened. |
| P4-16 | nvidia-smi and DCGM monitor NVLink throughput and thermal throttling | tools | none | not checked yet [U] | - | - | Settle in Part 11 from NVIDIA's DCGM docs. |
| P4-17 | NVLink and NVSwitch "radically reduce latency" versus PCIe Gen5 | comparison | W9: opens; no | unsupported [V] | 6 OD | NVB | NVIDIA quantifies bandwidth (about 7x), not latency. |
| P4-18 | Curriculum: HBM3 versus DDR; PyTorch distributed data parallel | curriculum | none | illustrative [I] | - | - | - |

### 5. Retrieval engineering (P5)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| P5-01 | RAG turns recall into reading comprehension, "drastically reducing" hallucination | finding | none | overstated [V] | 8 PR | LEW §4.3, Table 4; MAG §6 | Lewis et al. measured one thing: on Jeopardy question generation (452 pairs), judges found RAG more factual than closed-book BART in 42.7% of pairs and BART in 7.1%. RAG-based legal tools still hallucinated about 17% (Lexis+ AI) to about 33% (Westlaw AI-Assisted Research) of the time on 202 queries in 2024. Grounding helps; "drastically" is unmeasured. |
| P5-02 | Modern retrieval fuses dense and sparse signals | practice | W11, W12: open; yes | confirmed [V] | 7 OD | ESR "Reciprocal rank fusion using multiple standard retrievers" | Shipped practice (BM25 or ELSER sparse search plus kNN dense search, fused by RRF). No prevalence data was opened. |
| P5-03 | RRF needs no score normalization or supervised tuning | mechanism | W11, W12: open; yes | confirmed [V] | 8 PR | COR §1, §2, Table 3; ESR intro | It uses ranks only, so scores need no common scale. k and the window size are still settings. |
| P5-04 | Formula score = Σ 1/(k + rank(d)) | formula | W11: opens; yes | confirmed [V][T] | 10 PR | COR §1; ESR pseudocode | Summed over rankers; ranks start at 1. Elastic's worked example (k = 1, ranks 2 and 1) gives 0.8333 (recomputed, Section 5). |
| P5-05 | k is "typically 60" | number | W11, W12: open; yes | confirmed [V] | 9 PR | COR §1, Table 1; ESR "rank_constant" | Cormack et al. fixed k = 60 on one 2009 pilot (MAP about .2145 at 60, peak about .2146 near 70) and called the choice not critical. Elasticsearch defaults to 60 (minimum 1). |
| P5-06 | Agreement across retrievers "vastly outweighs" one anomalous first place | mechanism | W12: opens; partly | overstated [V][T] | 9 PR | COR §1; RDB | With k = 60 and two lists, a document ranked r in both beats a lone first place only when r ≤ 61, and by at most 2x (both first): 1.88x at rank 5, 1.52x at rank 20 (Section 5). Redis's own example gives 1.92x. |
| P5-07 | ColBERTv2 is late interaction and keeps token-level embeddings | mechanism | W14: opens; yes | confirmed [V] | 9 PP | CB2 abstract, Eq. 1 | Token vectors are kept in compressed form (20 or 36 bytes each, versus 256 in ColBERT v1). |
| P5-08 | MaxSim: score = Σ over query tokens of the max over document tokens of Q_i · D_j | formula | W13, W14: open; yes | confirmed [V] | 9 PR | COL Eq. 3, §3.2; CB2 Eq. 1 | Embeddings are L2-normalized, so the inner product equals cosine similarity. |
| P5-09 | Late interaction "vastly improves accuracy" over single-vector pooling | finding | W13: no; W14: partly | overstated [V] | 8 PP | CB2 Tables 4, 5a, 5b | MS MARCO dev MRR@10: ColBERTv2 39.7 versus single-vector 30.4 (RepBERT) to 38.8 (RocketQAv2), a gap of 0.9 to 9.3 points (Phase 5, §12). On BEIR it led on 6 of 13 sets, tied 1 and trailed 6, mostly to SPLADEv2 (a learned sparse model). The baselines are 2020 to 2021 systems. |
| P5-10 | Tools: Elasticsearch, ChromaDB, FAISS, Pinecone | named tools | W11: opens; partly | confirmed [V] | 8 OD | PYPI (elasticsearch 9.5.1; chromadb 1.5.9; faiss-cpu 1.15.1; pinecone 10.0.0) | All maintained in 2026. They are different kinds of thing: a search engine, a vector database, a similarity-search library and a managed vector service. Server versions and licences: Part 05. |
| P5-11 | Example: BM25 top 100, then a cross-encoder reranks the top 10 | example | none | illustrative [I] | - | COL Table 1; MHR Table 5 | Retrieve-then-rerank is standard practice; 100 and 10 are arbitrary. |
| P5-12 | Curriculum: recursive and semantic chunking; BM25 fails on vocabulary mismatch | curriculum | none | not checked yet [U] | - | - | Settle in Part 05 from chunking docs and the BEIR paper. |

### 6. Agent engineering (P6)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| P6-01 | ReAct is "the foundational paradigm of agent engineering" | attribution | none | overstated [V] | 5 PR | REA abstract, §2 to §4 | ReAct (ICLR 2023) is an influential origin of the thought, action, observation loop; "the" foundational paradigm is the paper's framing. |
| P6-02 | In ReAct, tools are "strictly mapped via JSON schemas" | mechanism | none | corrected [V] | 9 PR | REA §3.1, §3.2, Appendix C; ATU; OFC | ReAct used plain-text actions in few-shot prompts (search[entity], lookup[string], finish[answer]), with no JSON. JSON Schema tool definitions belong to today's APIs: Anthropic's input_schema, OpenAI's parameters with optional strict mode. |
| P6-03 | The loop: reason, act, a "deterministic execution layer" runs the tool, observe, repeat until done | mechanism | none | confirmed [V] | 7 PR | REA §3.2, Appendix C; ATU "Handling results from client tools" | Loop shape confirmed; ReAct also capped the steps (7 for HotpotQA, 5 for FEVER). "Deterministic" is the paper's word, not the sources'. |
| P6-04 | Error handling is "the most critical component"; stack traces let the model correct itself | claim | none | overstated [V] | 8 OD | ATU "Handling errors with is_error"; REA §3.3, Table 2 | Anthropic documents returning errors with is_error and advises short, instructive messages. ReAct's own error analysis put reasoning errors first (47% of failures). Nothing supports "most critical". |
| P6-05 | Frameworks: LangGraph, CrewAI, AutoGen, OpenAI Assistants API | named tools | W30, W31: open; partly | outdated [V] | 9 OD | OAM; ODP "2025-08-20: Assistants API"; AGN README; MAF; PYPI | The Assistants API shut down on August 26, 2026 (replacement: the Responses API with the Conversations API). AutoGen is in maintenance mode; its successor, Microsoft Agent Framework, reached 1.0.0 on April 2, 2026 and 1.21.0 on October 8, 2026. LangGraph (1.2.14) and CrewAI (1.15.26) are current. On October 26, 2026 the newest were LangGraph 1.2.17, CrewAI 1.15.30 and Agent Framework 1.23.0 (October 26, §13). |
| P6-06 | Examples: a coding agent fixes its own syntax error; an analyst reads SEC filings with OCR; an agent issues refunds on its own | examples | none | illustrative [I] | - | OW5 | An agent that moves money without a human check runs against OWASP's advice to require human approval for high-risk actions. |
| P6-07 | Curriculum: a raw while-loop that runs local functions from model output strings | curriculum | none | illustrative [I] | - | ATU | Matches the documented client-side tool loop. Running model-chosen strings needs input validation. |

### 7. Harness engineering (P7)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| P7-01 | "Harness engineering" means building deterministic test scaffolding, sandboxes and verification harnesses for agents | term | none | corrected [V] | 7 VB | OHE (February 11, 2026); FOW (February 17, 2026); AHL (November 26, 2025); LEH | In current use it means designing an agent's working environment and feedback loops: repository knowledge, architectural constraints, tests and observability around a coding agent (OpenAI; Thoughtworks' "guides and sensors", which date from Böckeler's article of April 2, 2026, not the February 17 memo (Phase 5, §12)). The paper blends the older "evaluation harness" sense (EleutherAI) with sandboxing. |
| P7-02 | Isolation is a "mandatory security primitive" for agents that run code | claim | W15 to W18 | overstated [V] | 5 OD | GVD security page | gVisor's threat model supports isolating untrusted code, but no opened source calls it mandatory, and gVisor says a sandbox doesn't replace a secure architecture. |
| P7-03 | gVisor is an application kernel written in Go that intercepts system calls | mechanism | W15 to W18: open; yes | confirmed [V] | 9 OD | GVD intro | Runs in user space; ships the OCI runtime runsc. |
| P7-04 | Docker containers share the host kernel, a "massive attack surface" | mechanism | W15, W18: open; partly | overstated [V] | 6 VB | NFK; GVD security page | The shared kernel is confirmed; no opened source quantifies the surface. Docker's own security docs: Part 08. |
| P7-05 | The Sentry intercepts syscalls through seccomp (systrap) or KVM | mechanism | W16, W17: open; yes | confirmed [V] | 8 OD | GVD Platform Guide | systrap has been the default since mid-2023; ptrace is no longer supported. |
| P7-06 | File access goes through an unprivileged Gofer over 9P or directfs | mechanism | W16: opens; stale | outdated [V] | 8 OD | GVF (June 27, 2023); EDR | directfs is the default in runsc, and the gofer protocol is LISAFS, not 9P. directfs gave the sandbox gofer-level file privileges. gVisor's intro page still says 9P. |
| P7-07 | gVisor isolates better than namespaces without the "heavy boot times and memory overhead" of VMs like Firecracker | comparison | W15, W18: open; no | overstated [V] | 8 OD | FCR; GVD performance page | Firecracker claims boot under 125 ms and under 5 MiB per microVM (vendor figures; its SPECIFICATION.md states the test conditions (Phase 5, §12)). gVisor lists higher per-syscall overhead and a poor fit for syscall-heavy workloads. Neither is lighter on every measure. |
| P7-08 | Tools: Pytest, Docker, gVisor (runsc), custom eval runners | named tools | W16 | confirmed [V] | 6 OD | GVD Docker quick start; PYPI (pytest 9.1.1); GHT (gVisor release-20261005.0) | runsc registers as a Docker runtime. |
| P7-09 | A gVisor sandbox "ensures" malicious syscalls cannot compromise the host | claim | W15 to W17: open; no | overstated [V] | 9 OD | GVD security page ("Defense-in-Depth", "Other Vectors") | gVisor claims layered risk reduction, not a guarantee, and says it doesn't protect against hardware side channels. |
| P7-10 | Examples: 500 prompt variations in Pytest; GitHub Actions tests before merging prompt changes | examples | none | illustrative [I] | - | - | - |
| P7-11 | Standard Docker is insufficient for untrusted code; switch the runtime to runsc to observe interception | claim + procedure | W16 | overstated [V] | 6 OD | GVD install page, Docker quick start | The procedure is right (sudo runsc install, restart Docker, docker run --runtime=runsc), and syscall logging is shown with the debug --strace option. No opened source says plain Docker is insufficient, though gVisor's README comes close for untrusted code (Phase 5, §12). |

### 8. Orchestration engineering (P8)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| P8-01 | Orchestration is modeled as a DAG or a cyclic state graph | framing | none | overstated [V] (Phase 5, §12) | 7 OD | AFL "Dags"; LGD Graph API | Both models exist. Temporal (durable code) and Celery (a task queue) are neither. |
| P8-02 | Routers send simple queries to "highly quantized, rapid models" and complex ones to larger models | pattern | none | corrected [V] | 7 VB | BEA "Workflow: Routing" | The documented pattern routes easy queries to smaller, cheaper models; quantization is a separate technique. |
| P8-03 | Evaluator-optimizer loops rewrite until a quality threshold is met | pattern | none | confirmed [V] | 7 VB | BEA "Workflow: Evaluator-optimizer" | The threshold is a common implementation detail, not part of the pattern's definition. |
| P8-04 | Temporal, Airflow, LangGraph and Celery are "the industry standard" | named tools | none | overstated [V] | 6 OD | TMP; AFL; CEL; LGD | Four tools for different jobs: durable execution, scheduled batch pipelines, a task queue, agent graphs. None calls itself the standard, and no adoption data was found. |
| P8-05 | Examples: FAQ routing to a cache; a translation loop; map-reduce over 50 chunks with Celery | examples | none | illustrative [I] | - | LGD "Send"; CEL canvas | The techniques exist; the scenarios are invented. |
| P8-06 | Curriculum: asyncio; retries with exponential backoff and jitter; a LangGraph "DAG" with conditional edges | curriculum | none | illustrative [I] | - | AWS; ORL; LGD "Edges" | AWS and OpenAI recommend backoff with jitter. A LangGraph graph may contain cycles, so "DAG" is imprecise. |

### 9. Eval engineering (P9)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| P9-01 | Evals replace subjective "vibe checks" with datasets, metrics and programmatic scoring | framing | none | overstated [V] | 6 PR | ZHE Table 5, §3.3 | Automated scorers approximate human judgment and are validated against it. A GPT-4 judge agreed with human votes 66% of the time with ties counted and 85% without, against 63% and 81% between humans (MT-bench, first turn), and showed position, verbosity and self-enhancement bias. |
| P9-02 | String matching and token probabilities "fail" to catch meaning-level hallucination | claim | W19, W20: did not open | overstated [V] | 7 PR | FAR Results, Fig. 2 | Token-level entropy averaged AUROC 0.691 against 0.790 for semantic entropy (30 dataset-model pairs): weaker, not failing. |
| P9-03 | Semantic entropy: sample answers, cluster by bidirectional entailment, take the entropy over clusters | mechanism | W19: did not open | confirmed [V] | 9 PR | FAR Methods | Ten samples per question; entailment judged by an LLM or an NLI model. |
| P9-04 | Formula H = -Σ p(C_k) log p(C_k) | formula | W19 | confirmed [V][T] | 8 PR | FAR Methods ("Computing the semantic entropy"; discrete variant) | The paper leaves out how p(C_k) is estimated: summed sequence probabilities, or (the discrete variant) each cluster's share of the samples. A toy split of 10 samples into 6/3/1 gives 0.898 nats, 1.296 bits (Section 5). |
| P9-05 | Low entropy means a confident meaning; high entropy flags confabulations | finding | W19 | confirmed [V] | 8 PR | FAR Discussion | Missing caveat: low entropy is not correctness, and errors a model makes consistently go undetected. |
| P9-06 | MIPROv2 stands for "Multiprompt Instruction PRoposal Optimizer Version 2" | name | W22 to W24: open; restate | confirmed [V] | 9 OD | DSD MIPROv2 page; MIP §4.3 | "Version 2" is DSPy's naming; the paper says MIPRO. |
| P9-07 | MIPROv2 uses Bayesian optimization over instructions and few-shot examples | mechanism | W22 to W24 | confirmed [V] | 9 OD | DSD; MIP §3.2 | A Tree-structured Parzen Estimator (Optuna) over instruction and demonstration choices, scored on minibatches. |
| P9-08 | GEPA evolves prompts across a Pareto front, "frequently" scoring higher with "vastly fewer" rollouts | finding | W22, W24 | overstated [V][T] | 8 PR | GEP Table 1, Table 2; DSD GEPA page | Aggregate gains over MIPROv2 were 7.01 points (Qwen3 8B) and 6.55 (GPT-4.1 mini). "35x fewer rollouts" compares GEPA with GRPO, a reinforcement-learning method, on one benchmark (24,000 / 678); across benchmarks it was 3.4x to 13.1x (Section 5). GRPO beat GEPA on AIME-2025. |
| P9-09 | Tools: DeepEval, Ragas, Phoenix (Arize), DSPy | named tools | none | confirmed [V] | 8 OD | PYPI (deepeval 4.2.8, Apache-2.0; ragas 0.4.3, Apache; arize-phoenix 20.20.0, Elastic-2.0; dspy 3.4.0, MIT) | Phoenix's Elastic License 2.0 is source-available, not an OSI open-source licence. |
| P9-10 | Example: semantic entropy probes flag divergent answers across seeds in a medical RAG pipeline | example | W19, W20 | illustrative [I] | - | KOS abstract | It mixes two methods: probes read one generation's hidden states, while sampling across seeds is the original method. |
| P9-11 | Example: MIPROv2 raises validation exact-match accuracy "by 15%" | number | W21 to W24: open; no | unsupported [V][T] | 8 PP | MIP Tables 1, 2; DSD | No source has 15%. The nearest figure is ScoNe exact match 69.1 to 79.4 with Llama-3-8B: +10.3 points, or 14.9% relative (Section 5). MIPROv2 runs a fixed trial budget, not "until" a target. |
| P9-12 | Example: GPT-4 as the judge of a smaller local model | example + model | none | outdated [V] | 9 OD | ODP "2026-04-22: Legacy GPT model snapshots" | Deprecated in OpenAI's April 22, 2026 notice: gpt-4 and gpt-4-0613 are scheduled to shut down on October 23, 2026, two weeks after this audit (replacement printed as "gpt-5.6-sol"); gpt-4-0314 shut down on March 26, 2026. Judges also favour their own outputs (PAN). (October 26, §14) |
| P9-13 | Curriculum: precision, recall, F1 and AUROC have "severe limitations"; calibrate an LLM judge with few-shot rubrics | curriculum | none | overstated [V] | 6 PR | FAR; ZHE §3.4, Table 4 | AUROC is how the semantic-entropy paper scores its detectors. Few-shot judging raised GPT-4's position consistency from 65.0% to 77.5% in Zheng et al. |

### 10. Inference engineering (P10)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| P10-01 | KV fragmentation limits batch size; PagedAttention, modeled on OS paging, stores KV in non-contiguous blocks | mechanism | W25: did not open | confirmed [V] | 9 PR | VLL abstract, §1, §4 | Earlier systems used only 20.4% to 38.2% of KV-cache memory for token states. Covers P10-01 and P10-02. |
| P10-03 | PagedAttention cuts internal fragmentation "to near-zero" | number | W25 | confirmed [V] | 9 PR | VLL abstract, §1, §4.3; VBL | The paper says "near-zero waste" for KV-cache memory as a whole and gives no percentage; waste is bounded to under one block per request. The vLLM blog says "under 4%". |
| P10-04 | It allows "massive" batch-size increases through continuous batching | claim | W25 | corrected [V] | 7 PR | VLL §2.3, §6.2; ORC | Iteration-level scheduling comes from Orca (OSDI 2022); PagedAttention's contribution is memory efficiency. Measured gain: 2x to 4x throughput at the same latency versus FasterTransformer and the authors' own reimplementations of Orca (OPT-13B to 175B and LLaMA-13B on A100s) (Phase 5, §12). |
| P10-05 | Autoregressive generation is memory-bandwidth bound | mechanism | W26, W27: open; yes | confirmed [V] | 8 PR | VLL §1, §2.2; LEV §1 | True for small-batch decoding; large models on some workloads become compute-bound (VLL §6.2). |
| P10-06 | Speculative decoding: draft M_q proposes γ tokens, target M_p scores them in one pass, rejection sampling accepts or rejects | mechanism + notation | W26, W27: open; yes | confirmed [V][T] | 9 PR | LEV §2.1, §2.3, Algorithm 1 | Notation matches. Expected tokens per target call: (1 - α^(γ+1)) / (1 - α), for example 2.95 at α = 0.8 and γ = 3 (Section 5). |
| P10-07 | It speeds generation without changing the output distribution | finding | W26: opens; yes | confirmed [V] | 9 PR | LEV §2.3, Appendix A.1; CHE | The same distribution, not bit-identical text across runs. |
| P10-08 | Tools: vLLM, TensorRT-LLM, Ollama, llama.cpp | named tools | none | confirmed [V] | 9 OD | PYPI (vllm 0.31.0, October 5, 2026); GHT (TensorRT-LLM v1.2.1; ollama v0.40.2; llama.cpp build b11534) | All maintained. |
| P10-09 | Llama 3 8B in GGUF Q4_K_M fits a consumer GPU | number | none | confirmed [V] | 8 MC | BTW file list | The file is 4.92 GB, so the weights fit an 8 GB GPU, with room still needed for the KV cache. |
| P10-09b | Llama 3 8B as the local example in 2026 | currency | none | outdated [V] | 8 OD | HFM; L3L; OSS | Llama 3 (April 2024) has been followed by Llama 3.1 to 3.3 and then Llama 4 (April 2025). Its licence bars using outputs to improve other models and requires "Built with Meta Llama 3". Models with fewer conditions exist; gpt-oss-20b is Apache 2.0 and runs in 16 GB. Since then Llama 4 is no longer Meta's newest open-weight line: Muse Glimmer 30B (Apache-2.0, August 2026) and Muse Spark Open (October 15, 2026, a custom gated licence). Llama 3's licence also requires "Llama 3" at the start of a shared fine-tune's name; from Llama 3.1 the prefix is "Llama" and the ban on improving other models is gone (Phase 5, §12). |
| P10-10 | vLLM serves hundreds of concurrent requests "without running out of KV cache memory" | claim | W25 | overstated [V] | 8 PR | VLL §4.5 | When blocks run out, vLLM preempts sequences: the 2023 paper swaps to CPU or recomputes, and vLLM 0.31.0 recomputes only, CPU swapping removed (Phase 5, §12); still recompute-only in vLLM 0.32.0, the newest on October 26, 2026 [V] (October 26, §13). Capacity depends on model, GPU memory and lengths. |
| P10-11 | A 1B draft with a 70B target "effectively doubles" tokens per second | number | W26, W27: open; no | overstated [V][T] | 7 VB | TRT Table 1; VSD | NVIDIA measured 3.55x (Llama 3.3 70B with a Llama 3.2 1B draft, one H200, FP8, batch size 1; the draft length of 10 appears in its build commands, not the measured table's settings (Phase 5, §12)). The vLLM team measured up to 1.5x with a 0.5B draft at low load and slowdowns of 1.4x to 1.8x at high load (Llama3-70B, 4x H100). Vendor measurements; no single factor holds. |
| P10-12 | Curriculum: FP16, INT8 and INT4 trade-offs; linear KV growth; rejection sampling keeps the exact distribution | curriculum | W25 to W27 | illustrative [I] | - | - | The facts are checked in P2-15 and P10-07. |

### 11. Platform engineering (P11)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| P11-01 | Platform engineering packages models, retrieval and orchestration behind REST or GraphQL APIs | term | none | corrected [V] | 7 SB | CNC | CNCF defines a platform as integrated capabilities offered to internal users through self-service and "golden paths". The paper describes building an AI product's API layer, which is closer to LLM serving and API work. |
| P11-02 | Server-Sent Events push tokens "the exact moment they are generated" | mechanism | none | corrected [V] (Phase 5, §12) | 8 OD | WHATWG HTML §9.2; nginx proxy module (Part 13) | Wrong as worded: nginx buffers proxied responses by default (`proxy_buffering on`) unless the response says `X-Accel-Buffering: no`, and the spec warns that buffering on the reader's side "can cause delays in event dispatch". Part 13's lab showed a stream arriving all at once through a proxy that ignored the header. |
| P11-03 | Kubernetes supports secure multi-tenant environments | claim | none | overstated [V] (Phase 5, §12) | 9 OD | kubernetes.io, "Multi-tenancy" (Part 13) | Kubernetes supports multi-tenant designs and lists the tools (namespaces, access control, quotas, network policies, sandboxed containers, dedicated nodes); it calls isolation "a broad spectrum" and says sandboxing "is often recommended when you are running untrusted code". It doesn't make them secure by itself. |
| P11-04 | Tools: FastAPI, LangServe, Docker, API gateways | named tools | none | outdated [V] | 9 OD | LSV README; PYPI (fastapi 0.143.0) | LangServe has been deprecated since November 18, 2024, and its repository was archived on May 5, 2026; LangChain recommends LangGraph Platform for new projects. FastAPI is current. Since then LangGraph Platform was renamed LangSmith Deployment, whose self-hosting is an Enterprise add-on, and FastAPI gained built-in SSE (0.135.0) and OpenTelemetry (0.142.0) (Phase 5, §12). |
| P11-05 | Examples: FastAPI with OAuth2 and JWT; a gateway that logs every prompt; SSE to React | examples | none | illustrative [I] | - | - | Logging every prompt is a privacy decision (OWASP's sensitive-information risk). Settled in Part 13: OWASP LLM02:2026 names observability platforms that "log full prompts" by default, and the OpenTelemetry GenAI conventions say instrumentations "SHOULD NOT capture them by default" (Phase 5, §12). |
| P11-06 | Curriculum: WebSockets versus SSE; separate the web server from the inference engine; auth, rate limits, logs | curriculum | none | illustrative [I] | - | - | - |

### 12. Security engineering (P12)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| P12-01 | Threats include prompt injection, jailbreaking, data exfiltration and toxic output | taxonomy | none | confirmed [V] | 8 SB | OW5; OW6; GAR README | All recognised. The paper merges security risks (OWASP) with content-safety harms (Llama Guard's job). |
| P12-02 | Separating data from instructions is "fundamentally challenging at the transformer level" | mechanism | none | overstated [V] | 6 SB | GRE abstract; OW5 LLM01; OW6 p. 13 | Documented at the application level (one text stream, no reliable separation today); no opened source shows it at the architecture level. Part 10 judged the claim mostly right, closer to "partly supported" (Phase 5, §12). |
| P12-03 | Llama Guard 3 is an LLM fine-tuned for safety classification "across diverse risk taxonomies" | named tool | W28, W29: open; barely | outdated [V] | 8 OD | LG3 card; LG4 card; HFM | Llama Guard 3 (8B, from Llama-3.1-8B) uses one fixed taxonomy of 14 MLCommons-aligned hazards; its licence files name the Llama 3.2 licence (Phase 5, §12). Llama Guard 4 (12B, multimodal) is Meta's newest. |
| P12-04 | Routing prompts and responses through Llama Guard "deterministically blocks" violating text | claim | W28: no; W29: contradicts | overstated [V] | 9 OD | LG3 card Table 1, Limitations; LG4 card; W29 §6.1; NAS | Classifiers have error rates. Llama Guard 3: F1 0.939, false-positive rate 0.040 (Meta's internal English response set). Llama Guard 4: English recall 69%, false-positive rate 11% (a different in-house set). Both cards warn of adversarial bypass. |
| P12-05 | Defense in depth requires sanitizing inputs (Base64, role-play) | practice | none | overstated [V] | 7 SB | OW5 LLM01 "Prevention and Mitigation Strategies"; OW6 p. 13; NAS | Input filtering is one of several controls, alongside least privilege, human approval, segregating external content and adversarial testing. Adaptive attacks beat most of 12 published defenses at over 90% success (Nasr et al., preprint). |
| P12-06 | Tools: OWASP Top 10 for LLMs, NeMo Guardrails, Garak ("a comprehensive LLM vulnerability scanner") | named tools | none | overstated [V] | 7 SB | OW6 release post (September 1, 2026); NEM (0.24.1, Apache-2.0); GAR (0.17.0) | No edition is named; the 2026 edition is current. Garak calls itself a red-teaming and assessment kit, not "comprehensive", and it scans a model rather than guarding live traffic. |
| P12-07 | Examples: an input classifier, PII masking, Llama Guard refusals | examples | none | illustrative [I] | - | LG3 card; NEM docs | Llama Guard outputs a label and categories; the application writes the refusal. |
| P12-08 | Curriculum: an input filter with a risk threshold; output guardrails that "enforce rigid" policy on "all" generated text | curriculum | none | overstated [V] | 8 OD | PG2 card; LG3 card; NEM README | Prompt Guard 2 (86M) catches 97.5% of Meta's private jailbreak set at a 1% false-positive rate, so some attacks pass. NeMo's README says evaluating safety is still an open research question. |

### Blueprint 1. Multi-agent orchestration (B1)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| B1-01 | One mega-prompt becomes "highly fragile"; specialized agents fix this | claim | W30 to W33 | overstated [V] | 8 VB | AMR; COG; MAS; BEA | Anthropic's multi-agent research system beat a single agent by 90.2% on its internal research eval but used about 15x the tokens of a chat, and fits poorly where agents share context (coding). Cognition argues for one agent; Cemri et al. catalogue 14 failure modes in more than 1,600 traces. Anthropic's advice is to start with one call. |
| B1-02 | LangGraph: a cyclic state graph, explicit routing, thread-scoped checkpoints | tool mechanism | W30, W31, W33: open; yes | confirmed [V] | 9 OD | LGD Graph API, Persistence, Interrupts | Cycles, conditional edges, checkpointers keyed by thread_id. |
| B1-03 | LangGraph caches node results and skips nodes whose input is unchanged | tool feature | W31: opens; yes | overstated [V] (Phase 5, §12) | 8 OD | LGD "Node caching" | Opt-in per node (a CachePolicy with key and TTL), not default behaviour. |
| B1-04 | LangGraph is "vastly superior" for high-compliance, resumable work | comparison | W30 to W33: open; no | overstated [V] | 7 VB | W30 to W33; LGD | The features are real; no source measures compliance fitness or says "vastly superior". |
| B1-05 | CrewAI: role-based sequential or hierarchical delegation; the fastest way to prototype linear teams | tool mechanism | W30, W32, W33 | overstated [V] | 7 OD | CRD Processes, Flows; PYPI | Processes are sequential or hierarchical, but CrewAI also ships Flows (event-driven, with state and persistence), so "linear" is dated; "fastest" is unmeasured, and the sources disagree. |
| B1-06 | CrewAI has "less structural durability" for multi-stage approval chains | comparison | W31: opens; probable origin | overstated [V] | 5 OD | CRD Flows ("Human Feedback"), HITL page, changelog; LGD Interrupts | Partly outdated since CrewAI 1.8.0 (January 8, 2026) added @human_feedback alongside @persist. The remaining gap concerns what the open-source docs promise for long-running approvals, not a measured difference. |
| B1-07 | Human-in-the-loop breakpoints let a person approve high-stakes actions | tool feature | W33: opens; yes | confirmed [V] | 8 OD | LGD Interrupts ("approve or reject") | LangGraph's docs recommend interrupt() for human approval; static breakpoints are for debugging. |

### Blueprint 2. Programmable guardrails (B2)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| B2-01 | Prompt-only alignment ("do not be toxic") is highly susceptible to jailbreaks | claim | none | confirmed [V] | 5 SB | OW5; OW6 p. 13; NAS | Supported indirectly: OWASP lists system-prompt constraints as one control among many and says no reliable prevention exists. No study of prompt-only alignment was opened. |
| B2-02 | Programmable guardrails "solve this fundamental flaw" with "deterministic, isolated" filters | claim | none | overstated [V] | 9 OD | NEM README and docs home; OW6 | Guardrails add layers. NeMo's docs say some rails use the LLM itself to check inputs and outputs; only plain application code is deterministic. |
| B2-03 | NeMo Guardrails uses Colang to define deterministic dialog flows | tool mechanism | none | overstated [V] | 6 OD | NEM README and docs | Colang 1.0 is the default and 2.0 is supported. Flows can call the model, so they aren't deterministic as a whole. |
| B2-04 | Guardrails reroute to a fallback "without ever invoking" the generative model | mechanism | none | overstated [V] | 7 OD | NEM docs home | True of pattern-based rails; false of LLM self-check and safety-model rails, which call a model. |
| B2-05 | Llama Guard scores inputs and agent outputs against customized taxonomies | tool mechanism | none | overstated [V] | 6 OD | LG3 and LG4 cards | Prompts and responses: yes. The cards describe one fixed taxonomy and don't mention custom categories; settle in Part 10. Part 10 judged the claim mostly right, closer to "partly supported" (Phase 5, §12). |
| B2-06 | Example: a "deterministic" guardrail blocks "any" input similar to an instruction override | example | none | overstated [V] | 8 OD | PG2 card; NAS | Such filters are classifiers that trade misses against false alarms (Prompt Guard 2: 97.5% recall at a 1% false-positive rate on Meta's set). |
| B2-07 | Example: Colang flows force a banking assistant to refuse off-topic branches | example | none | illustrative [I] | - | NEM docs ("Topic Control") | Topic control exists; "force" overstates it. |
| B2-08 | Curriculum: the limits of "soft-prompt alignment (RLHF)" | terminology | none | corrected [V] | 9 PP | LES abstract; OUY abstract | Soft prompts are trained vectors (prompt tuning); RLHF trains weights from human rankings; a written instruction is neither. Say "instruction-only alignment" and "training-based alignment such as RLHF". |

### Blueprint 3. Knowledge mapping (B3)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| B3-01 | Dense-vector RAG "frequently struggles" with multi-hop reasoning | finding | none | confirmed [V] | 7 PP | MHR Tables 5, 6 | GPT-4 answered 56% of 2,556 multi-hop news queries correctly from retrieved chunks, against 89% from gold evidence. "Frequently" is unquantified. |
| B3-02 | GraphRAG has an LLM extract entities and relationships into a graph database such as Neo4j | mechanism | none | corrected [V] | 7 PP | EDG method; MGR releases; N4G | Microsoft's GraphRAG extracts with an LLM into a graph index with Leiden communities and LLM-written community summaries; it uses no graph database and no Cypher. Neo4j's neo4j-graphrag is a separate stack. |
| B3-03 | Retrieval uses graph traversal such as Cypher instead of only cosine similarity | mechanism | none | overstated [V] | 7 OD | N4G retriever sections; EDG | True of Neo4j's retrievers (vector search, then Cypher traversal). Microsoft's global search uses map-reduce over community summaries. |
| B3-04 | This "drastically" improves global synthesis questions | finding | none | overstated [V] | 8 PP | EDG Fig. 2, Tables 2 and 6 | Against vector RAG, LLM judges preferred GraphRAG on comprehensiveness in 72% to 83% of comparisons and on diversity in 62% to 82% (two corpora of about 1M and 1.7M tokens, 125 generated questions each). Directness favoured vector RAG. A preprint under review. |
| B3-05 | Hybrid GraphRAG combines vector similarity with graph traversal | mechanism | none | confirmed [V] | 8 OD | N4G (VectorCypherRetriever, HybridCypherRetriever) | - |

### Blueprint 4. Total privacy: local models (B4)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| B4-01 | Cloud APIs are "a non-starter" for medical, defense and finance work | claim | none | corrected [V] | 9 GOV | HHC | HHS says a covered entity may use a cloud provider for ePHI under a business associate agreement, plus its own risk analysis. Defense and finance rules not checked. Not legal advice. |
| B4-02 | Local orchestration "ensures complete data sovereignty, zero cloud telemetry and total air-gapped security" | claim | none | overstated [V] | 8 OD | OLF; OLC | Ollama doesn't see prompts run locally, but it pulls models from the internet, auto-downloads app updates on macOS and Windows, and offers cloud models that send prompts to its servers (off with OLLAMA_NO_CLOUD=1). Air-gapping has to be configured; it isn't a property of running locally. |
| B4-03 | Local deployment uses containerized runtimes | mechanism | none | overstated [V] | 6 OD | OLF | Containers are one option; Ollama also ships native apps and a Linux install script. |
| B4-04 | llama.cpp and Ollama run models on consumer hardware through GGUF quantization | tool mechanism | none | confirmed [V] | 8 OD | GGF; OSS | GGUF is the file format llama.cpp and similar runtimes load. OpenAI says gpt-oss-20b runs in 16 GB with Ollama, llama.cpp and LM Studio. |
| B4-05 | 16-bit to 4-bit compression with "minimal precision loss" | claim | none | overstated [V][T] | 8 OD | LQP "LLaMA 3 8b Scoreboard" | Llama 3 8B on Wikitext-2: perplexity rose from 6.233 (f16) to 6.407 (Q4_K_M), +2.79%; the top token changed at about 8.1% of positions; the file shrank to 31% (Section 5). Small but measurable, and it varies by task. |
| B4-06 | Runs on Apple Silicon unified memory or local NVIDIA GPUs | tool support | none | not checked yet [U] | - | - | Settle in Part 11 from the llama.cpp and Ollama hardware docs. |
| B4-07 | It creates a "zero-latency inference boundary entirely disconnected from the internet" | claim | none | overstated [V] | 8 PR | VLL §1, §2.2; OLF | Local decoding still takes time per token; being offline removes only network latency, and staying offline has to be configured (B4-02). |
| B4-08 | Summarizing patient records locally avoids violating HIPAA "by ensuring zero external network transmission" | legal claim | none | corrected [V] | 9 GOV | HHS (content last reviewed August 7, 2026) | The Security Rule covers ePHI an entity creates, receives, maintains or transmits. It requires administrative (risk analysis, training, contingency planning), physical (device and media controls) and technical (access control, audit controls, integrity, authentication) safeguards. No network transmission addresses only transmission security. Not legal advice. |
| B4-09 | Examples: air-gapped M&A analysis; code assistance on a defense intranet | examples | none | illustrative [I] | - | - | - |
| B4-10 | Curriculum: GGUF versus AWQ versus GPTQ; map parameters to VRAM; serve Llama 3 with Ollama | curriculum | none | corrected [V] | 8 OD | GGF; AWQ; GPQ | GGUF is a file format that can hold tensors in many quantization types; AWQ and GPTQ are quantization algorithms. Compare AWQ, GPTQ and llama.cpp's K-quants as methods, not against a file format. |

### Conclusion (C)

| ID | Claim (paraphrased) | Type | Gemini cit. | Verdict | Grade | Primary source (location) | Note (what the evidence says, with scope) |
|---|---|---|---|---|---|---|---|
| C-01 | The shift is a "fundamental, permanent maturation" | framing | none | unsupported [V] | 9 AI | Section 2 of this ledger | Nothing is cited for it, and no evidence could show that a change is permanent. An opinion; drop it. |
| C-02 | The blueprints are "the definitive roadmap" | framing | none | overstated [V] | 9 OD | rows P6-05, P11-04, P12-03 | Several named tools were superseded before this audit. |
| C-03 | Systems built this way are "highly deterministic, optimized and secure" | claim | none | overstated [V] | 8 SB | OW6 p. 13; TML; LG3 card | OWASP's 2026 edition says no reliable prevention mechanism for prompt injection exists today; deployed inference isn't deterministic; safety classifiers have error rates. |

## 4. Absolute and intensifier words

| Words | Uses | Where | Supported? | Rows |
|---|---|---|---|---|
| "deterministic", "deterministically" | 10, 2 | Intro, 1, 6, 7 (×2), 12, B2 (×5), Conclusion | No for inference, classifiers or LLM-based rails; yes only for plain application-code checks | S0-01, P1-15, P6-03, P7-01, P12-04, B2-02, B2-03, B2-06, C-03 |
| "definitively", "definitive", "exhaustive", "peer-reviewed", "verified" | 1, 2, 1, 2, 1 | Intro, 1, Conclusion | No | S0-01, S0-03, P1-03, C-02 |
| "drastically" | 5 | 1, 5, 10 (×2), B3 | Only PagedAttention's "near-zero" waste has a source; the others are unmeasured | P1-07, P5-01, P10-03, B3-04 |
| "vastly" | 4 | 5 (×2), 9, B1 | No: at most 2x (RRF), 0.9 to 9.3 points (ColBERTv2), 3.4x to 35x fewer rollouts against GRPO (GEPA), unmeasured (LangGraph) | P5-06, P5-09, P9-08, B1-04 |
| "strictly" | 5 | 3, 6, 7, B2, B4 | No | P3-07, P6-02, P7-02, B2-07 |
| "ensures", "ensuring" | 4, 4 | 3, 5, 7 (×2), 11, B4 (×2), Conclusion | Only where it restates a mechanism; not as a guarantee | P7-09, B4-02, B4-08 |
| "solve", "solves" | 2 | 9, B2 | Semantic entropy catches some confabulations, not all; guardrails don't solve injection | P9-05, B2-02 |
| "near-zero" | 1 | 10 | Yes: the vLLM paper's own wording for total KV-cache waste | P10-03 |
| "zero-latency", "zero cloud telemetry", "total air-gapped", "complete data sovereignty", "non-starter", "minimal precision loss" | 1 each | B4 | No | B4-01, B4-02, B4-05, B4-07 |
| "industry standard" | 1 | 8 | No adoption data | P8-04 |
| "the exact moment", "instantly", "without ever invoking" | 1 each | 11, B2 | Not checked (SSE); no for model-based rails | P11-02, B2-04 |
| "fail" | 1 | 9 | Overstated | P9-02 |
| "massive" (15 uses), "immense", "profound", "radically", "highly fragile", "permanent" | 20 | throughout | Rhetoric without measurable content; "radically reduce latency" is unsupported | P4-17, B1-01, C-01 |

## 5. Formulas and calculations

**Formulas.** The PDF printed every formula as raw LaTeX source, so a reader of the PDF sees backslash commands rather than mathematics. Checked against the primary papers:

| Formula as printed (rendered) | Where | Primary source | Result |
|---|---|---|---|
| P(output given context) | 1 | taxonomy §3; COA | Correct notation |
| O(N²) | 2 | VAS Table 1 | Correct for full self-attention: O(n²·d) per layer |
| [A][B] ... [A] → [B] | 1 | OLS | Correct as the authors' behavioural definition |
| score = Σ 1/(k + rank(d)) | 5 | COR §1; ESR | Correct; sum over rankers, ranks from 1 |
| score(Q, D) = Σ_i max_j ⟨Q_i, D_j⟩ | 5 | COL Eq. 3; CB2 Eq. 1 | Correct; vectors L2-normalized |
| H = -Σ p(C_k) log p(C_k) | 9 | FAR Methods | Correct form; the estimator of p(C_k) is omitted |
| M_q, M_p, γ, rejection sampling | 10 | LEV §2 | Correct notation; γ is the number of draft tokens per target call |

**Calculations run [T].** Python 3.13.16 on Linux (standard library only), October 9, 2026. Inputs are the published figures named; the semantic-entropy split and the α values are illustrative inputs [I].

| Calculation | Result |
|---|---|
| RRF, k = 60: ranks 2 and 5 versus a lone first place | 0.031514 versus 0.016393, ratio 1.922 |
| RRF, k = 60: same rank r in both lists versus a lone first place | r = 1: 2.000x; r = 5: 1.877x; r = 20: 1.525x; r = 60: 1.017x; r = 62: tie; wins for r ≤ 61 |
| RRF, k = 1: lone first versus rank 5 in both lists | 0.500 versus 0.333 (the lone first place wins) |
| Elasticsearch worked example (k = 1, ranks 2 and 1) | 0.8333 |
| H100 SXM dense FP8 | 3,958 / 2 = 1,979 TFLOPS |
| Eight H100 SXM at TDP | 8 × 700 W = 5,600 W |
| NVLink per direction; one ConnectX-7 per direction; ratio | 450 GB/s; 50 GB/s; 9.0 |
| NVLink versus PCIe Gen5 x16 | 900 / 128 = 7.03 |
| Llama 3 8B, Q4_K_M versus f16 (Wikitext-2) | perplexity +2.79%; top token changed at 8.1% of positions; size 0.306 of f16 |
| GEPA versus MIPROv2, aggregate | +7.01 points (Qwen3 8B); +6.55 (GPT-4.1 mini); versus GRPO +5.94 (Qwen3 8B) |
| GRPO rollouts over GEPA rollouts | 35.4 (IFBench); 3.4 to 13.1 across benchmarks |
| MIPRO on ScoNe (Llama-3-8B) | +10.3 points; 14.9% relative |
| Speculative decoding, expected tokens per target call | α = 0.6: 2.176 (γ = 3), 2.383 (γ = 5); α = 0.8: 2.952 (γ = 3), 3.689 (γ = 5) |
| TensorRT-LLM, Llama 3.3 70B with a 1B draft | 181.74 / 51.14 = 3.55x |
| KV cache per token, OPT-13B, FP16 | 819,200 bytes; 2,048 tokens = 1.68 GB |
| Semantic entropy, 10 samples split 6/3/1 | 0.8979 nats = 1.2955 bits |

## 6. Are the pillar names established terms?

| Heading | Established? | Who uses it (source, date) | Matches Gemini's definition? | Tag |
|---|---|---|---|---|
| Prompt engineering | Yes | ACE (Anthropic, 2025) treats it as the existing practice that context engineering grows out of; the project's taxonomy | Mostly; the "manipulating attention weights" framing isn't standard (S0-02) | [V] |
| Context engineering | Yes, since 2025 | ACE (September 29, 2025) | Partly: "finite resource" yes, "inherently the KV cache" no (P2-04) | [V] |
| Memory engineering | Emerging | MLM (July 3, 2026): what persists across calls, as opposed to one call's context window | Roughly, but Gemini ties it to a three-part taxonomy that is CoALA's four-part one (P3-02) | [V] |
| Rack and infrastructure engineering | Not checked | - | Its content is GPU hardware and datacenter interconnect | [U] |
| Retrieval engineering | Not found in use; a search returned job titles such as "RAG engineer", titles only | none opened | Its content (hybrid search, fusion, reranking) is standard retrieval practice | [U] |
| Agent engineering | Emerging, vendor-promoted | LCA (LangChain, December 9, 2025): "the iterative process of refining non-deterministic LLM systems into reliable production experiences" | No: LangChain means a build, test, observe, refine cycle; Gemini means ReAct mechanics | [V] |
| Harness engineering | Yes, since February 2026 | OHE (OpenAI, February 11, 2026); FOW (Thoughtworks, February 17, 2026) | No (P7-01) | [V] |
| Orchestration engineering | Not established | UNI (a vendor CEO's op-ed, April 27, 2026) calls it emerging and means something else | No; "orchestration" itself is standard (AFL, BEA) | [V] |
| Eval engineering | Emerging, vendor-promoted | GAL (Galileo, 2026) calls it "the new discipline that combines data science with software engineering" | Roughly; Gemini overstates "replaces" human judgment (P9-01) | [V] |
| Inference engineering | Yes, in industry use | PRA (The Pragmatic Engineer, March 31, 2026, adapted from Philip Kiely's book *Inference Engineering*): optimizing production serving through batching, KV caching, quantization and speculative decoding | Yes | [V] |
| Platform engineering | Yes, as a general field | CNC (CNCF Platforms white paper v1.0): internal platforms with self-service and golden paths | No: Gemini means an AI product's API layer (P11-01) | [V] |
| Security engineering | Yes, as a general field | OW6 frames LLM mitigations as classic security controls (least privilege, policy checks in code, human confirmation) | Partly: Gemini merges security with content safety | [V] |
| Blueprints | "Programmable guardrails" is NeMo's own term (NEM); "GraphRAG" is Microsoft's name (EDG); "multi-agent orchestration" is a common phrase (BEA uses "orchestrator-workers"); "total privacy" is not a term | - | - | [V] |

## 7. Answers to the audit questions

1. **Induction heads.** Not peer-reviewed: a Transformer Circuits article (March 8, 2022) plus an arXiv preprint. The authors claim strong causal evidence only for small attention-only models and call their large-model evidence "preliminary and indirect". Later work: Yin & Steinhardt (YIN; ICML 2025, peer-reviewed, 12 models) find few-shot learning relies mainly on function-vector heads, more so in larger models, and many of those heads begin as induction heads during training. Crosbie & Shutova (CRO; preprint) find ablating a few induction heads hurts abstract pattern tasks in Llama-3-8B and InternLM2-20B. Singh et al. (SIN) and Reddy (RED), both preprints, study how induction heads form in small synthetic settings. Rows P1-03, P1-07, P1-14.
2. **Lost in the middle.** It holds for the 2023 models Liu et al. tested. For current models, length degradation is robust (RULER, NoLiMa, Chroma), but Chroma's July 2025 needle test across 18 models (including Claude Opus 4, GPT-4.1, Gemini 2.5 Pro and Qwen3-235B) found no notable position effect. Which current models still show the U-shape was not established; vendor long-context reports were not opened [U]. Rows P2-02, P2-13.
3. **H100 SXM5.** 3,958 TFLOPS is the FP8 Tensor Core figure with 2:4 sparsity; dense is 1,979. 132 SMs are enabled out of 144 on the full GH100 die. H100 is a previous generation: Blackwell is current, and NVIDIA said on August 26, 2026 that Vera Rubin is in full production. Rows P4-01, P4-04, P4-12.
4. **Still current?** Llama Guard 3: no, Llama Guard 4 is newest (P12-03). OpenAI Assistants API: shut down August 26, 2026 (P6-05). LangServe: deprecated since November 18, 2024, archived May 5, 2026 (P11-04). GPT-4 as a judge: deprecated, with gpt-4 and gpt-4-0613 scheduled to shut down on October 23, 2026 (P9-12). Llama 3 8B as the local example: two generations old, with licence conditions (P10-09b). OWASP Top 10 for LLMs: the 2026 edition, released September 1, 2026 (P12-06). Colang: NeMo Guardrails 0.24.1 supports Colang 1.0 (the default) and 2.0 (B2-03).
5. **PagedAttention.** The paper says "near-zero waste" in its abstract and introduction and gives no percentage; waste is bounded to under one block per request. The "under 4%" figure comes from the vLLM blog (P10-03).
6. **"Doubling tokens per second."** No source. Measured results: 2.3x to 3.4x for T5-XXL with T5-small drafts at batch size 1 on TPU-v4 (Leviathan et al.); 2x to 2.5x for Chinchilla 70B (Chen et al.); 3.55x for Llama 3.3 70B with a 1B draft on one H200 at batch size 1 (NVIDIA); up to 1.5x at low load and slowdowns at high load (vLLM). Row P10-11.
7. **MIPROv2 "15%".** Not sourced; it reads as invented. The nearest real figure is +10.3 points on ScoNe with Llama-3-8B (P9-11).
8. **HIPAA.** No. Local processing does not by itself make a summarization system compliant; the Security Rule's safeguards apply to ePHI wherever it is maintained. Cloud processing is permitted under a business associate agreement. Rows B4-01, B4-08. Information, not legal advice.
9. **NeMo Guardrails.** Not deterministic as a whole: the self-check input and output rails call an LLM, and safety-model rails call a model. Pattern-based checks and plain code are deterministic. Rows B2-02 to B2-04.
10. **LangGraph and CrewAI, from official docs.** LangGraph 1.2.14: cycles, conditional edges, checkpointers keyed by thread_id, interrupt() for human approval, and opt-in node caching, all confirmed. CrewAI 1.15.26: sequential and hierarchical processes plus Flows with state, persistence and @human_feedback (since 1.8.0, January 8, 2026). "Vastly superior" and "less structural durability" come from vendor blogs, not measurements. Rows B1-02 to B1-07.

## 8. Errata summary

**Verdicts by section.** Counted by script from Section 3 (one verdict per row; where a confirmed row has an unchecked part, P1-08, P4-09 and P4-14, it is counted as confirmed).

| Section | confirmed | corrected | outdated | overstated | unsupported | illustrative | not checked yet | Rows |
|---|---|---|---|---|---|---|---|---|
| S0 | 0 | 1 | 0 | 3 | 0 | 0 | 0 | 4 |
| P1 | 5 | 1 | 0 | 3 | 2 | 3 | 0 | 14 |
| P2 | 4 | 2 | 0 | 3 | 1 | 2 | 0 | 12 |
| P3 | 2 | 1 | 0 | 1 | 1 | 1 | 3 | 9 |
| P4 | 7 | 1 | 1 | 3 | 2 | 1 | 1 | 16 |
| P5 | 7 | 0 | 0 | 3 | 0 | 1 | 1 | 12 |
| P6 | 1 | 1 | 1 | 2 | 0 | 2 | 0 | 7 |
| P7 | 3 | 1 | 1 | 5 | 0 | 1 | 0 | 11 |
| P8 | 1 | 1 | 0 | 2 | 0 | 2 | 0 | 6 |
| P9 | 6 | 0 | 1 | 4 | 1 | 1 | 0 | 13 |
| P10 | 7 | 1 | 1 | 2 | 0 | 1 | 0 | 12 |
| P11 | 0 | 2 | 1 | 1 | 0 | 2 | 0 | 6 |
| P12 | 1 | 0 | 1 | 5 | 0 | 1 | 0 | 8 |
| B1 | 2 | 0 | 0 | 5 | 0 | 0 | 0 | 7 |
| B2 | 1 | 1 | 0 | 5 | 0 | 1 | 0 | 8 |
| B3 | 2 | 1 | 0 | 2 | 0 | 0 | 0 | 5 |
| B4 | 1 | 3 | 0 | 4 | 0 | 1 | 1 | 10 |
| C | 0 | 0 | 0 | 2 | 1 | 0 | 0 | 3 |
| Total | 50 | 17 | 7 | 55 | 8 | 20 | 6 | 163 |

**Overall** (after the Phase 5 corrections of October 20, 2026; the October 9 figures were 135 checkable rows, 52 holding, 52 overstated, 31 wrong). Of the 137 rows that make a checkable claim (163 less 20 illustrative and 6 not checked yet), 50 hold as stated (36.5%), 55 are overstated (40.1%) and 32 are wrong as stated (23.4%: 17 corrected, 7 outdated, 8 unsupported). The paper's main failure is strength and scope, not direction. Retrieval (P5) and inference (P10) are its most reliable sections; security (P12), guardrails (B2) and harness engineering (P7) are its least.

**Errata by section.** Each line says what to keep and what to write instead. Row IDs carry the evidence.

- **Introduction (S0).** Keep: the twelve-pillar outline as a starting map. Fix: it is an AI-written synthesis, not peer-reviewed (S0-03); prompting supplies tokens and does not manipulate attention weights (S0-02); the field is not "deterministic" (S0-01); coverage is partial (S0-04).
- **Prompt engineering (P1).** Keep: in-context learning without weight updates, the induction-head pattern and its abrupt early formation. Fix: Olsson et al. is not peer-reviewed (P1-03); induction heads are one contested account of few-shot learning, with function-vector heads mattering more in larger models (P1-07, P1-14); a role prompt does not make output deterministic, and a system prompt cannot hard-penalize tokens (P1-09, P1-11); Structured Outputs guarantees schema adherence, not correct values (P1-15).
- **Context engineering (P2).** Keep: quadratic attention, KV reuse for identical prefixes, RadixAttention's radix tree with LRU eviction, linear KV growth. Fix: context engineering is choosing what goes in the window, which is separate from provider caching and server-side KV reuse (P2-04); depth-first order is SGLang's scheduling order, not how it matches prefixes (P2-07); "lost in the middle" means less accurate, not blind, and was measured on 2023 models (P2-02); drop the advice to put summaries in the middle (P2-13) and the "thousands" figure (P2-14).
- **Memory engineering (P3).** Keep: stateless generation and the MemGPT paging design. Fix: CoALA has four memory modules, working memory plus three long-term ones (P3-02); "typically NoSQL" has no source (P3-03); no tool is "strictly necessary", and MemGPT is now Letta (P3-07). Three rows are deferred to Parts 05 and 06.
- **Rack and infrastructure (P4).** Keep, for H100 SXM5: 80 GB HBM3, 3.35 TB/s, 700 W, 900 GB/s NVLink (both directions). Fix: 3,958 TFLOPS is FP8 with sparsity, dense 1,979 (P4-12); 132 SMs is the H100 SXM5 product, the full die has 144 (P4-04); eight GPUs are not one memory pool (P4-08); 5.6 kW is the GPUs' ceiling, not a floor (P4-15); NVLink helps inside a node, not between nodes (P4-06); drop "rarely compute-bound" and "radically reduce latency" (P4-05, P4-17); Hopper is a previous generation (P4-01).
- **Retrieval (P5).** Keep: dense plus sparse fusion, RRF with k = 60, MaxSim, ColBERTv2's compressed token vectors. Fix: grounding reduces hallucination by unmeasured amounts, and RAG-based legal tools still hallucinated on about 17% to 33% of 202 queries in a 2024 study (P5-01); with two lists and k = 60, agreement beats a lone first place by at most 2x (P5-06); late interaction led single-vector baselines by 0.9 to 9.3 points of MRR@10 on MS MARCO dev, not "vastly" (P5-09).
- **Agent engineering (P6).** Keep: the reason, act, observe loop. Fix: ReAct used plain-text actions; JSON Schema tool definitions belong to today's APIs (P6-02); the Assistants API has shut down and AutoGen is in maintenance mode, with Microsoft Agent Framework as its successor (P6-05); "most critical" error handling is unsupported (P6-04).
- **Harness engineering (P7).** Keep: gVisor's Sentry, its platforms (systrap by default) and the runsc procedure. Fix: "harness engineering" means designing a coding agent's working environment and feedback loops (P7-01); the gofer now speaks LISAFS and directfs is the default, not 9P (P7-06); isolation reduces risk and guarantees nothing (P7-02, P7-09); gVisor and Firecracker trade off differently, neither is lighter on every measure (P7-07); drop "massive attack surface" and "insufficient" (P7-04, P7-11).
- **Orchestration (P8).** Keep: DAG and state-graph models, the evaluator-optimizer pattern. Fix: routing sends easy queries to smaller models; quantization is a separate technique (P8-02); the four tools do different jobs and none is "the industry standard" (P8-04).
- **Eval engineering (P9).** Keep: semantic entropy and its formula, MIPROv2's Bayesian search. Fix: drop the "15%" MIPROv2 gain (P9-11); token-level scores are weaker, not failing (P9-02); "35x fewer rollouts" compares GEPA with GRPO, and the aggregate gain over MIPROv2 was 6.55 to 7.01 points on two models (P9-08); automated scorers approximate human judgment and must be checked against it (P9-01); the gpt-4 judge models are deprecated and due to shut down on October 23, 2026 (P9-12).
- **Inference (P10).** Keep: PagedAttention and its "near-zero waste", memory-bound decoding, speculative decoding's exact output distribution. Fix: continuous batching comes from Orca, and PagedAttention's gain is memory efficiency (P10-04); measured speculative-decoding results run from slowdowns at high load to 3.55x at batch size 1 (vendor measurements), not "doubles" (P10-11); vLLM preempts requests when KV memory runs out (P10-10); pick a newer or less restricted local model than Llama 3 8B (P10-09b).
- **Platform (P11).** Keep: FastAPI. Fix: "platform engineering" means internal developer platforms; the section describes an AI product's API layer (P11-01); LangServe is deprecated and archived (P11-04); SSE doesn't deliver tokens "the exact moment" they exist when a proxy buffers (P11-02); Kubernetes supports multi-tenancy but doesn't make it secure by itself (P11-03).
- **Security (P12).** Keep: the threat list. Fix: classifiers have error rates and do not "deterministically block" (P12-04); input filtering is one control among several, and adaptive attacks beat most published defenses (P12-05); Llama Guard 4 is current (P12-03); name the OWASP edition, now 2026 (P12-06); output rails do not "enforce rigid" policy on "all" text (P12-08); the instruction-and-data problem is shown at the application level, not the architecture level (P12-02).
- **Multi-agent (B1).** Keep: LangGraph's cycles, checkpoints, interrupts and opt-in node caching. Fix: multi-agent systems cost far more tokens (about 15x a chat in Anthropic's research system) and suit work that splits into independent parts; start simple and add agents only when needed (B1-01); "vastly superior" is unmeasured (B1-04); CrewAI has Flows and @human_feedback since 1.8.0, so "linear" and "less durable" are dated (B1-05, B1-06).
- **Guardrails (B2).** Keep: layered guardrails, Colang, topic control. Fix: some NeMo rails call an LLM, so the system is not deterministic and can invoke a model (B2-02 to B2-04); injection filters are classifiers with misses and false alarms (B2-06); Llama Guard's cards describe a fixed taxonomy (B2-05); "soft-prompt alignment (RLHF)" confuses three things (B2-08).
- **Knowledge mapping (B3).** Keep: vector RAG's multi-hop weakness and hybrid graph-plus-vector retrieval. Fix: Microsoft's GraphRAG uses no graph database or Cypher; Neo4j's library is a separate stack (B3-02); the global-question gains are LLM-judged win rates in a preprint, not "drastic" (B3-04).
- **Local models (B4).** Keep: GGUF runtimes on consumer hardware. Fix: local processing alone does not satisfy HIPAA, and cloud use is allowed under a business associate agreement (B4-01, B4-08; not legal advice); GGUF is a file format, while AWQ and GPTQ are algorithms (B4-10); local runtimes still reach the internet unless configured not to (B4-02); 4-bit quantization has a measurable cost (B4-05); offline is not zero-latency (B4-07).
- **Conclusion (C).** Fix: drop "permanent" and "definitive"; the systems described are neither deterministic nor secure by construction (C-01 to C-03).

## 9. Where this audit touches existing project docs

These are flagged, not applied. Each is settled from primary sources; the owner decides on any edit.

1. **Induction heads (taxonomy 3e, §4.1 and conclusion 2).** The taxonomy calls induction heads "the best-supported mechanistic account of why few-shot examples work at all" and "the leading explanation, not a proven one". Yin & Steinhardt (ICML 2025, PMLR 267, peer-reviewed) find that few-shot learning across 12 models relies mainly on function-vector heads, more so in larger models. **Settlement:** the taxonomy's caveat about large models stands, but "best-supported account of why few-shot examples work" is now contested by a later peer-reviewed study. **Suggested erratum:** "Induction heads are the best-supported account of how in-context copying emerges in training; for few-shot task learning in larger models, a 2025 peer-reviewed study finds function-vector heads matter more (Yin & Steinhardt, ICML 2025)." The same wording would fit Appendix A's induction-heads row.
2. **OWASP edition (taxonomy §17.1 and §17.3).** The taxonomy cites LLM01:2025 and LLM07:2025, correctly for that edition. The 2026 edition was released on September 1, 2026. Read from its PDF (whose cover still shows a placeholder publication date), System Prompt Leakage became "Hidden Context Exposure" (LLM08:2026), and LLM01 says no reliable prevention mechanism exists today. **Settlement:** no error; update the edition at the next revision.
3. **Position effects (taxonomy §4.1 analogy and §7.4 protocol step 4).** The analogy ("reads best at the top and bottom; the middle smudges") is stated generally. Chroma (July 2025, 18 models) found no notable position effect in its needle test while confirming length degradation. **Settlement:** Liu et al. remains right for its 2023 models; the analogy should carry that scope. Keeping critical facts out of the middle remains harmless advice.
4. **Prompt-caching prices (taxonomy §11.6).** The taxonomy says cache reads are "typically 0.1×". Anthropic's docs, read October 9, 2026, list 0.1x with lower multipliers (0.025x or 0.05x) on some newest models. **Settlement:** not a conflict ("typically"); a freshness note for the next edition.
5. **No conflicts found** with the prompt guide (2e), the skills reference, the skills booklet or the handoff. The guide's and taxonomy's LLM-judge figure ("over 80% agreement") matches Zheng et al. (85% with ties excluded).

## 10. Not checked yet

| Row | What would settle it | Part |
|---|---|---|
| P1-08 (Anthropic Workbench) | Anthropic's Console docs | 03 |
| P1-11 (logit_bias) | OpenAI's Chat Completions reference | 03 |
| P3-04 (embedding proximity) | The embedding model's docs; a measured failure case | 05 |
| P3-05, P3-06 (procedural memory; asynchronous memory) | CoALA §4; Letta docs | 06 |
| P3-07 (Redis "sub-millisecond") | Redis docs plus an independent measurement | 06 |
| P4-09 (E4M3 forward, E5M2 gradients) | NVIDIA Transformer Engine docs | 11 |
| P4-14, P4-16 (CUDA, Slurm, Kubernetes; DCGM) | NVIDIA and SchedMD docs | 11 |
| P5-12 (chunking; BM25 vocabulary mismatch) | Chunking docs; the BEIR paper | 05 |
| P11-02, P11-03 (SSE timing; Kubernetes multi-tenancy) | WHATWG SSE spec, vendor streaming docs; kubernetes.io | 13 |
| B4-06 (Apple Silicon and NVIDIA support) | llama.cpp and Ollama hardware docs | 11 |
| Terms: rack and infrastructure engineering; retrieval engineering | A search with pages opened | 11, 05 |
| Which current models still show the U-shaped position effect | Vendor long-context reports; 2025 to 2026 position studies | 04 |

Also deferred to the parts: server versions and licences of Elasticsearch, Neo4j and Qdrant; Pinecone's hosting model; Cypher's relation to ISO GQL; venues of ColBERTv2 (NAACL 2022), AWQ and GPTQ, which the arXiv pages did not show.

## 11. Sources

Opened October 9, 2026. ✓ means the lead session re-opened it; the rest were opened by a checker agent. Class codes as in "How to read".

| Key | Source | Class |
|---|---|---|
| ACE | Anthropic, "Effective context engineering for AI agents", September 29, 2025. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | VB |
| AFL | Apache Airflow docs 3.3.2, "What is Airflow?". https://airflow.apache.org/docs/apache-airflow/stable/index.html | OD |
| AGN | Microsoft AutoGen README (maintenance-mode notice). https://github.com/microsoft/autogen | OD |
| AHL | Anthropic, "Effective harnesses for long-running agents", November 26, 2025. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | VB |
| AMR | Anthropic, "How we built our multi-agent research system", June 13, 2025. https://www.anthropic.com/engineering/multi-agent-research-system | VB |
| APC | Anthropic docs, prompt caching. https://platform.claude.com/docs/en/build-with-claude/prompt-caching | OD |
| ATU | Anthropic docs, tool use: "Define tools" and "Handle tool calls". https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use ; https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls | OD |
| AWQ ✓ | Lin et al., "AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration", arXiv 2306.00978 (v6, April 25, 2026). https://arxiv.org/abs/2306.00978 | PP |
| AWS | Brooker, "Exponential Backoff And Jitter", AWS Architecture Blog, March 4, 2015 (updated 2023). https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/ | VB |
| BEA | Anthropic, "Building effective agents", December 19, 2024 (revised since). https://www.anthropic.com/engineering/building-effective-agents | VB |
| BTW | bartowski, Meta-Llama-3-8B-Instruct-GGUF (file list). https://huggingface.co/bartowski/Meta-Llama-3-8B-Instruct-GGUF | MC |
| CB2 | Santhanam et al., "ColBERTv2", arXiv 2112.01488v3 (July 10, 2022). https://arxiv.org/abs/2112.01488 | PP |
| CEL | Celery docs 5.6, introduction. https://docs.celeryq.dev/en/stable/getting-started/introduction.html | OD |
| CHE | Chen et al., "Accelerating Large Language Model Decoding with Speculative Sampling", arXiv 2302.01318. https://arxiv.org/abs/2302.01318 | PP |
| CHR | Hong, Troynikov & Huber, "Context Rot", Chroma, July 14, 2025. https://www.trychroma.com/research/context-rot | VB |
| CNC ✓ | CNCF TAG App Delivery, Platforms white paper v1.0. https://tag-app-delivery.cncf.io/whitepapers/platforms/ | SB |
| COA | Sumers et al., "Cognitive Architectures for Language Agents" (CoALA), TMLR 2024, arXiv 2309.02427v3. https://arxiv.org/abs/2309.02427 | PR |
| COG | Yan, "Don't Build Multi-Agents", Cognition, June 12, 2025. https://cognition.com/blog/dont-build-multi-agents | VB |
| COL | Khattab & Zaharia, "ColBERT", SIGIR 2020, arXiv 2004.12832. https://arxiv.org/abs/2004.12832 | PR |
| COR | Cormack, Clarke & Büttcher, "Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods", SIGIR 2009. https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf | PR |
| CRD | CrewAI docs: Processes, Flows, Human-in-the-loop, changelog. https://docs.crewai.com/en/concepts/processes ; https://docs.crewai.com/en/concepts/flows ; https://docs.crewai.com/en/learn/human-in-the-loop ; https://docs.crewai.com/en/changelog | OD |
| CRO | Crosbie & Shutova, induction-head ablations in large models, arXiv 2407.07011v3 (April 2, 2025). https://arxiv.org/abs/2407.07011 | PP |
| DGX | NVIDIA DGX H100 User Guide, "Introduction to the NVIDIA DGX H100 System". https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html | OD |
| DSD | DSPy docs, MIPROv2 and GEPA. https://dspy.ai/current/api/optimizers/MIPROv2/ ; https://dspy.ai/current/api/optimizers/GEPA/overview/ | OD |
| EDG | Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization", arXiv 2404.16130v2 (February 19, 2025; under review). https://arxiv.org/abs/2404.16130 | PP |
| EDR | Edera docs, "gVisor vs Edera", March 7, 2026. https://docs.edera.dev/technical-overview/concepts/edera-vs-gvisor/ | VB |
| ESR | Elasticsearch Reference, reciprocal rank fusion. https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion | OD |
| FAR | Farquhar, Kossen, Kuhn & Gal, "Detecting hallucinations in large language models using semantic entropy", Nature 630:625-630 (2024), DOI 10.1038/s41586-024-07421-0. https://www.nature.com/articles/s41586-024-07421-0 | PR |
| FCR | Firecracker site. https://firecracker-microvm.github.io/ | OD |
| FMS | Pony et al., "Flash-MaxSim", arXiv 2605.29517v3. https://arxiv.org/html/2605.29517v3 | PP |
| FOW | Böckeler, "Harness Engineering - first thoughts", martinfowler.com, February 17, 2026. https://www.martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html | PB |
| GAL ✓ | Galileo, "Eval engineering" (2026). https://galileo.ai/evalengineering | VB |
| GAR | garak README and PyPI page (0.17.0, September 9, 2026). https://github.com/NVIDIA/garak ; https://pypi.org/project/garak/ | OD |
| GEP | Agrawal et al., "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning", arXiv 2507.19457v2 (February 14, 2026; ICLR 2026 oral per the PDF header). https://arxiv.org/abs/2507.19457 | PR |
| GGF ✓ | Hugging Face Hub docs, GGUF. https://huggingface.co/docs/hub/gguf | OD |
| GHT ✓ | Release tags read with git ls-remote from github.com (ollama/ollama, ggml-org/llama.cpp, google/gvisor, NVIDIA/TensorRT-LLM, firecracker-microvm/firecracker), October 9, 2026 | OD |
| GPQ ✓ | Frantar et al., "GPTQ", arXiv 2210.17323 (v2, March 22, 2023). https://arxiv.org/abs/2210.17323 | PP |
| GRE | Greshake et al., indirect prompt injection, arXiv 2302.12173 (AISec 2023 per the project taxonomy). https://arxiv.org/abs/2302.12173 | PR |
| GVD | gVisor docs: introduction, Platform Guide, Security Model, Performance Guide, Installation, Docker quick start. https://gvisor.dev/docs/ | OD |
| GVF | gVisor blog, "Optimizing gVisor filesystems with Directfs", June 27, 2023. https://gvisor.dev/blog/2023/06/27/directfs/ | OD |
| HFM ✓ | Meta's meta-llama organization page on Hugging Face. https://huggingface.co/meta-llama | OD |
| HHC ✓ | HHS, "Guidance on HIPAA & Cloud Computing" (last reviewed December 23, 2022). https://www.hhs.gov/hipaa/for-professionals/special-topics/health-information-technology/cloud-computing/index.html | GOV |
| HHS ✓ | HHS, "Summary of the HIPAA Security Rule" (content last reviewed August 7, 2026). https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html | GOV |
| KOS | Kossen et al., "Semantic Entropy Probes", arXiv 2406.15927v1. https://arxiv.org/abs/2406.15927 | PP |
| L3L ✓ | Meta Llama 3 Community License (version release date April 18, 2024). https://dev.meta.ai/llama/llama3/license | OD |
| LCA ✓ | LangChain, "Agent Engineering: A New Discipline", December 9, 2025. https://www.langchain.com/blog/agent-engineering-a-new-discipline | VB |
| LEH | EleutherAI lm-evaluation-harness README. https://github.com/EleutherAI/lm-evaluation-harness | OD |
| LES | Lester et al., "The Power of Scale for Parameter-Efficient Prompt Tuning", arXiv 2104.08691. https://arxiv.org/abs/2104.08691 | PP |
| LET | Letta, "MemGPT is now part of Letta", September 23, 2024. https://www.letta.com/blog/memgpt-and-letta | VB |
| LEV | Leviathan, Kalman & Matias, "Fast Inference from Transformers via Speculative Decoding", ICML 2023, PMLR 202. https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf | PR |
| LEW | Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", NeurIPS 2020, arXiv 2005.11401v4. https://arxiv.org/abs/2005.11401 | PR |
| LG3 | Meta, Llama Guard 3 8B model card. https://github.com/meta-llama/PurpleLlama/blob/main/Llama-Guard3/8B/MODEL_CARD.md | OD |
| LG4 | Meta, Llama Guard 4 12B model card. https://github.com/meta-llama/PurpleLlama/blob/main/Llama-Guard4/12B/MODEL_CARD.md | OD |
| LGD | LangGraph docs: Graph API, Persistence, Interrupts. https://docs.langchain.com/oss/python/langgraph/graph-api ; https://docs.langchain.com/oss/python/langgraph/persistence ; https://docs.langchain.com/oss/python/langgraph/interrupts | OD |
| LIU | Liu et al., "Lost in the Middle", arXiv 2307.03172v3; TACL 12:157-173 (2024), DOI 10.1162/tacl_a_00638, as recorded in the project taxonomy. https://arxiv.org/abs/2307.03172 | PR |
| LQP ✓ | llama.cpp, tools/perplexity README ("LLaMA 3 8b Scoreboard", commit f364eb6f, RTX 4090). https://github.com/ggml-org/llama.cpp/blob/master/tools/perplexity/README.md | OD |
| LSV ✓ | LangServe README (deprecation notice; archived May 5, 2026). https://github.com/langchain-ai/langserve | OD |
| MAF | Microsoft Agent Framework on PyPI; Microsoft Learn migration guide from AutoGen. https://pypi.org/project/agent-framework/ ; https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/ | OD |
| MAG | Magesh et al., "Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools", arXiv 2405.20362; Journal of Empirical Legal Studies 22:216 (2025), DOI 10.1111/jels.12413, as recorded in the project taxonomy. https://arxiv.org/abs/2405.20362 | PR |
| MAS | Cemri et al., "Why Do Multi-Agent LLM Systems Fail?", arXiv 2503.13657v3 (October 26, 2025). https://arxiv.org/abs/2503.13657 | PP |
| MCP ✓ | Model Context Protocol specification, latest (schema 2026-07-28). https://modelcontextprotocol.io/specification/latest | OD |
| MEM | Packer et al., "MemGPT: Towards LLMs as Operating Systems", arXiv 2310.08560v2. https://arxiv.org/abs/2310.08560 | PP |
| MGR | Microsoft GraphRAG repository and releases. https://github.com/microsoft/graphrag | OD |
| MHR | Tang & Yang, "MultiHop-RAG", arXiv 2401.15391v1. https://arxiv.org/abs/2401.15391 | PP |
| MIP | Opsahl-Ong et al., "Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs" (MIPRO), arXiv 2406.11695. https://arxiv.org/abs/2406.11695 | PP |
| MLM ✓ | Bala Priya C, "Context vs memory engineering in agentic AI systems", Machine Learning Mastery, July 3, 2026. https://machinelearningmastery.com/context-vs-memory-engineering-in-agentic-ai-systems/ | PB |
| N4G | Neo4j, neo4j-graphrag user guide. https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html | OD |
| NAS | Nasr et al., "The Attacker Moves Second", arXiv 2510.09023. https://arxiv.org/abs/2510.09023 | PP |
| NEM | NeMo Guardrails README, docs and PyPI page (0.24.1, September 16, 2026). https://github.com/NVIDIA/NeMo-Guardrails ; https://docs.nvidia.com/nemo/guardrails/latest/index.html ; https://pypi.org/project/nemoguardrails/ | OD |
| NFK | Northflank, "What is gVisor?", April 16, 2026. https://northflank.com/blog/what-is-gvisor | VB |
| NOL | Modarressi et al., "NoLiMa", arXiv 2502.05167v3 (ICML 2025 per arXiv comments). https://arxiv.org/abs/2502.05167 | PR |
| NPM ✓ | npm registry (npm view), October 9, 2026 | OD |
| NQ2 ✓ | NVIDIA, second-quarter fiscal 2027 results, August 26, 2026. https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027 | OD |
| NVB | NVIDIA Technical Blog, "NVIDIA Hopper Architecture In-Depth", March 22, 2022 (modified July 22, 2025). https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/ | OD |
| NVH ✓ | NVIDIA H100 product page, specifications table. https://www.nvidia.com/en-us/data-center/h100/ | OD |
| OAM | OpenAI, Assistants API migration guide. https://developers.openai.com/api/docs/assistants/migration | OD |
| ODP ✓ | OpenAI, deprecations page (newest entry October 1, 2026). https://developers.openai.com/api/docs/deprecations | OD |
| OFC | OpenAI, function calling guide. https://developers.openai.com/api/docs/guides/function-calling | OD |
| OHE | OpenAI, "Harness engineering", February 11, 2026. https://openai.com/index/harness-engineering/ | VB |
| OLC ✓ | Ollama docs, Cloud. https://docs.ollama.com/cloud | OD |
| OLF ✓ | Ollama docs, FAQ. https://docs.ollama.com/faq | OD |
| OLS | Olsson et al., "In-context Learning and Induction Heads", Transformer Circuits Thread, March 8, 2022; arXiv 2209.11895. https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html | PP |
| ORC | Yu et al., "Orca: A Distributed Serving System for Transformer-Based Generative Models", OSDI 2022. https://www.usenix.org/conference/osdi22/presentation/yu | PR |
| ORL | OpenAI, rate limits guide. https://developers.openai.com/api/docs/guides/rate-limits | OD |
| OSO | OpenAI, Structured Outputs guide. https://developers.openai.com/api/docs/guides/structured-outputs | OD |
| OSS ✓ | OpenAI, "Introducing gpt-oss", August 5, 2025. https://openai.com/index/introducing-gpt-oss/ | VB |
| OUY | Ouyang et al., "Training language models to follow instructions with human feedback", arXiv 2203.02155. https://arxiv.org/abs/2203.02155 | PP |
| OW5 | OWASP GenAI, LLM01:2025 Prompt Injection, and the 2025 list. https://genai.owasp.org/llmrisk/llm01-prompt-injection/ ; https://genai.owasp.org/llm-top-10/ | SB |
| OW6 ✓ | OWASP GenAI, 2026 Top 10 for LLM Applications: release post (September 1, 2026) and resource page with PDF. https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/ ; https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/ | SB |
| PAN | Panickssery et al., "LLM Evaluators Recognize and Favor Their Own Generations", arXiv 2404.13076 (NeurIPS 2024 per the project taxonomy). https://arxiv.org/abs/2404.13076 | PR |
| PFO ✓ | promptfoo README. https://github.com/promptfoo/promptfoo | OD |
| PG2 | Meta, Llama Prompt Guard 2 86M model card. https://github.com/meta-llama/PurpleLlama/blob/main/Llama-Prompt-Guard-2/86M/MODEL_CARD.md | OD |
| PRA ✓ | Orosz, "What is inference engineering?", The Pragmatic Engineer, March 31, 2026. https://newsletter.pragmaticengineer.com/p/what-is-inference-engineering | PB |
| PYPI ✓ | PyPI JSON API (https://pypi.org/pypi/PACKAGE/json), queried October 9, 2026 | OD |
| RDB | Redis blog, reciprocal rank fusion, August 9, 2026. https://redis.io/blog/reciprocal-rank-fusion/ | VB |
| REA | Yao et al., "ReAct", ICLR 2023, arXiv 2210.03629v3. https://arxiv.org/abs/2210.03629 | PR |
| RED | Reddy, induction-head emergence in a minimal network, arXiv 2312.03002. https://arxiv.org/abs/2312.03002 | PP |
| RUB | NVIDIA, Rubin platform press release, January 5, 2026. https://nvidianews.nvidia.com/news/rubin-platform-ai-supercomputer | OD |
| RUL | Hsieh et al., "RULER", arXiv 2404.06654v3. https://arxiv.org/abs/2404.06654 | PP |
| SGL ✓ | Zheng et al., "SGLang: Efficient Execution of Structured Language Model Programs", NeurIPS 2024 (main track); arXiv 2312.07104v2. https://proceedings.neurips.cc/paper_files/paper/2024/hash/724be4472168f31ba1c9ac630f15dec8-Abstract.html | PR |
| SIN | Singh et al., induction-head formation, arXiv 2404.07129. https://arxiv.org/abs/2404.07129 | PP |
| TML | He et al., "Defeating Nondeterminism in LLM Inference", Thinking Machines Lab, September 10, 2025. https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ | VB |
| TMP | Temporal docs, "What is Temporal?". https://docs.temporal.io/temporal | OD |
| TRT | NVIDIA Technical Blog, "Boost Llama 3.3 70B Inference Throughput 3x with NVIDIA TensorRT-LLM Speculative Decoding", December 17, 2024. https://developer.nvidia.com/blog/boost-llama-3-3-70b-inference-throughput-3x-with-nvidia-tensorrt-llm-speculative-decoding/ | VB |
| UNI | Filev, "The rise of AI orchestration engineering", Unite.AI, April 27, 2026. https://www.unite.ai/the-rise-of-ai-orchestration-engineering/ | VB |
| VAS | Vaswani et al., "Attention Is All You Need", NeurIPS 2017, arXiv 1706.03762. https://arxiv.org/abs/1706.03762 | PR |
| VBL | vLLM blog, "vLLM: Easy, Fast, and Cheap LLM Serving with PagedAttention", June 20, 2023. https://vllm.ai/blog/2023-06-20-vllm | VB |
| VLL ✓ | Kwon et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention", SOSP 2023, arXiv 2309.06180. https://arxiv.org/abs/2309.06180 | PR |
| VSD | vLLM blog, speculative decoding, October 17, 2024. https://vllm.ai/blog/2024-10-17-spec-decode | VB |
| YIN ✓ | Yin & Steinhardt, "Which Attention Heads Matter for In-Context Learning?", ICML 2025, PMLR 267. https://proceedings.mlr.press/v267/yin25e.html | PR |
| ZHE | Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena", NeurIPS 2023 Datasets and Benchmarks, arXiv 2306.05685. https://arxiv.org/abs/2306.05685 | PR |

## 12. Phase 5 corrections (October 20, 2026)

The series' parts flagged these in their Section 10 and left this ledger unedited until the series was finished. The owner approved applying them on October 20, 2026. Each row above that changed carries "(Phase 5, §12)". The evidence is in the part named.

| Row | Change | From |
|---|---|---|
| P5-09 | Gap 0.9 to 9.3 points (RepBERT, 30.4, is the lowest single-vector model in ColBERTv2's Table 4), not 0.9 to 8.6; also in Sections 4 and 8 | Part 05 §3.5, §4 |
| P7-01 | Böckeler's "guides and sensors" date from April 2, 2026 | Part 08 §10 |
| P7-07 | Firecracker's specification states test conditions | Part 08 §10 |
| P7-11 | gVisor's README comes close to calling plain containers insufficient for untrusted code | Part 08 §10 |
| P8-01 | confirmed → overstated: Temporal, DBOS and Restate are neither a DAG nor a state graph | Part 09 §4, §10 |
| B1-03 | confirmed → overstated: node caching is opt-in | Part 09 §10 |
| P12-02, B2-05 | Verdicts kept; note added that Part 10 judged them closer to "partly supported", a label this ledger's scale doesn't have | Part 10 §10 |
| P12-03 | Llama Guard 3's licence files name the Llama 3.2 licence | Part 10 §10 |
| P4-09 | Hopper's default is delayed scaling; Blackwell's default recipe uses E4M3 throughout | Part 11 §10 |
| P10-04 | The 2x to 4x is against FasterTransformer and the authors' own Orca reimplementations (Part 11 judged it closer to "partly supported") | Part 11 §10 |
| P10-10 | vLLM 0.31.0 recomputes only; CPU swapping was removed | Part 11 §10 |
| P10-11 | "Draft length 10" is in NVIDIA's build commands, not the measured table's settings | Part 11 §10 |
| P10-09b | Llama 4 is no longer Meta's newest open-weight line (Muse Glimmer 30B, Muse Spark Open); Llama 3's naming rule | Parts 11 and 12 §10 |
| P11-02 | not checked yet → corrected | Part 13 §3.3, §4 |
| P11-03 | not checked yet → overstated | Part 13 §3.1, §4 |
| P11-04 | LangSmith Deployment; FastAPI's built-in SSE and OpenTelemetry | Part 13 §3.1, §4 |
| P11-05 | OWASP LLM02:2026 and the conventions' opt-in rule | Part 13 §3.7, §3.8 |

**Rows settled in the parts but not re-labelled here.** P1-08, P1-11 (Part 03), P3-04, P5-12 (Part 05), P3-05 to P3-07 (Part 06), P4-09's mapping, P4-14, P4-16 and B4-06 (Part 11) carry "not checked yet" or [U] in Section 3 but are settled in those parts' Section 4 tables. Read the part for the current verdict. Section 9's taxonomy flags were applied to the taxonomy and the guide on October 20, 2026 (see claude/project-file-map.md).

## 13. Package-version re-check (October 26, 2026)

The freshness ledger's PyPI table was re-checked on October 26, 2026, with the owner's approval; 19 of its 40 packages had newer releases (`records/freshness-recheck-2026-10-26.md`). The rows above cite the versions opened on October 9, 2026 as their evidence, so those citations stay. Rows whose wording depends on the version carry "(October 26, §13)".

| Row | Change | From |
|---|---|---|
| P6-05 | "LangGraph (1.2.14) and CrewAI (1.15.26) are current" no longer holds as worded; the newest on October 26 were LangGraph 1.2.17, CrewAI 1.15.30 and Agent Framework 1.23.0. Verdict unchanged | PyPI, October 26 |
| P10-10 | vLLM 0.32.0 (October 18, 2026) replaced 0.31.0; "recomputes only" re-checked at 0.32.0 the same day: unchanged [V]. Verdict unchanged | PyPI and vLLM's scheduler at v0.32.0, October 26 |

**Evidence versions superseded, verdicts unchanged.** P1-08 and P9-09 (dspy 3.4.0, now 3.4.1); P4-14 and P10-08 (vllm 0.31.0, now 0.32.0); P5-10 (pinecone 10.0.0, now 10.2.0); P9-09 (deepeval 4.2.8, now 4.3.1; arize-phoenix 20.20.0, now 20.26.1; licences unchanged); P11-04 (fastapi 0.143.0, now 0.162.0, so FastAPI is still current); P12-06 and source GAR (garak 0.17.0, now 0.17.1). These rows judge whether named tools exist, are maintained and carry a licence; a newer release doesn't change that. Section 7's item 10 names LangGraph 1.2.14 and CrewAI 1.15.26 as the versions checked then. No row cites a version of the anthropic or openai packages, so anthropic 2.x affects the parts, not this ledger.

## 14. gpt-4 shutdown re-check (October 26, 2026)

The freshness ledger's one passed "Re-check after" date (Section 1, gpt-4) was re-checked on October 26, 2026, with the owner's approval, on OpenAI's deprecations page (https://developers.openai.com/api/docs/deprecations). The row above keeps its October 9 wording.

| Row | Change | From |
|---|---|---|
| P9-12 | gpt-4 and gpt-4-0613 were shut down on October 23, 2026, as scheduled: the page says access to the April 22 notice's models "was shut down on October 23, 2026" and lists `gpt-4-0613` (aliases `gpt-4`, `gpt-4-0613-completions`, `gpt-4-completions`) with substitute gpt-5.6-sol [V]. `ft-gpt-4` was shut down the same day. Verdict unchanged (outdated) | ODP, October 26 |

The same page's newest notice, dated October 14, 2026, schedules GPT-4o, GPT-4o mini, GPT-4.1 and GPT-4.1 mini for removal on January 14, 2027 [V]. In this ledger those models appear only as models tested in cited studies (P9-08, Section 5's figures, Section 7's answer on lost in the middle), where a removal doesn't change the results. The parts that name them weren't re-checked for this.
