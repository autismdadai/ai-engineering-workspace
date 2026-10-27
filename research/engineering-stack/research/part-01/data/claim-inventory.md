# Claim inventory: Gemini "Modern AI Engineering Stack" (working file)

Built October 9, 2026 from ai-reports/gemini-ai-engineering-stack.md. One row per factual claim, number, formula, term and citation. "Cit." = works-cited numbers matched by topic (inferred: the PDF has no inline citation markers). Flag = absolute or intensifier wording to test. Group = researcher group (R1 to R7, or LEAD for the lead session).

| ID | Sec. | Claim (paraphrased) | Type | Cit. (inferred) | Flag | Group |
|---|---|---|---|---|---|---|
| S0-01 | Intro | The field has definitively moved from trial-and-error prompting to a rigorous, deterministic systems discipline | framing | none | definitively; deterministic | LEAD |
| S0-02 | Intro | Prompting works by mathematically manipulating transformer attention weights through in-context conditioning | mechanism | 1-4 | | R1 |
| S0-03 | Intro | The report is an exhaustive, peer-reviewed framework | self-description | none | exhaustive; peer-reviewed | LEAD |
| S0-04 | Intro | Twelve pillars and four blueprints cover the stack | scope | none | | LEAD |
| P1-01 | 1 | Prompting shapes the conditional distribution of outputs given the context, without gradient updates to the weights | mechanism | none | | R1 |
| P1-02 | 1 | Formula P(output given context) | formula | none | | R1 |
| P1-03 | 1 | Verified peer-reviewed analyses show in-context learning is driven by induction heads that form in a narrow, abrupt window early in training | attribution + mechanism | 1-4 | verified; peer-reviewed | R1 |
| P1-04 | 1 | An induction head finds an earlier copy of the current token, attends to the token that followed it (prefix matching) and raises that token's logit (copying) | mechanism | 3, 4 | | R1 |
| P1-05 | 1 | Formula [A][B] ... [A] -> [B] | formula | 3, 4 | | R1 |
| P1-06 | 1 | The formation shows as a distinct turn in the model's trajectory in function space, seen with PCA | mechanism | 3, 4 | | R1 |
| P1-07 | 1 | This explains why few-shot examples drastically improve abstract pattern-matching | causal claim | 1-4 | drastically | R1 |
| P1-08 | 1 | Tools: OpenAI API, Anthropic Workbench, DSPy, Promptfoo | named tools | none | | R1 |
| P1-09 | 1 | Example: zero-shot role prompting enforces output determinism for JSON ticket routing | example + mechanism | none | determinism | R1 |
| P1-10 | 1 | Example: three few-shot demonstrations for legal entity extraction | example | none | | R1 |
| P1-11 | 1 | Example: a system prompt can severely penalize out-of-character tokens and restrict vocabulary | example + mechanism | none | | R1 |
| P1-12 | 1 | Curriculum: tokenization and BPE explain how text becomes vectors | curriculum | none | | R1 |
| P1-13 | 1 | Curriculum: separate system, user and assistant roles in API payloads | curriculum | none | | R1 |
| P1-14 | 1 | Curriculum: induction heads give the mechanistic, causal reality of few-shot learning | causal claim | 3, 4 | causal reality | R1 |
| P1-15 | 1 | Curriculum: schema enforcement (OpenAI Structured Outputs) bridges text generation and deterministic software execution | tool + mechanism | none | deterministic | R1 |
| P2-01 | 2 | Standard self-attention is quadratic in sequence length, O(N^2) | formula | 5, 6 | | R1 |
| P2-02 | 2 | Attention quality frequently degrades as context grows; in "lost in the middle" models ignore information placed mid-prompt | finding | none | ignore | R1 |
| P2-03 | 2 | Context engineering treats the context window as a finite, curated resource | framing | none | | R1 |
| P2-04 | 2 | Optimizing context inherently involves manipulating the KV cache | mechanism | 5, 6 | inherently | R1 |
| P2-05 | 2 | Processing a prompt computes key and value tensors for each token | mechanism | 5, 6 | | R1 |
| P2-06 | 2 | Recomputing KV for shared prefixes across turns wastes immense compute | mechanism | 5, 6 | immense | R1 |
| P2-07 | 2 | RadixAttention reuses the KV cache automatically at run time | mechanism | 5, 6 | | R1 |
| P2-08 | 2 | It maps token sequences to KV tensors in a radix tree | mechanism | 5, 6 | | R1 |
| P2-09 | 2 | The engine runs a depth-first search to match incoming prefixes to cached tensors | mechanism | 5, 6 | | R1 |
| P2-10 | 2 | LRU eviction plus reference counting for running batches prevents GPU memory exhaustion | mechanism | 5, 6 | | R1 |
| P2-11 | 2 | Anthropic's context-engineering guidance, SGLang and LangChain are critical tools | named tools | 5, 6 | critical | R1 |
| P2-12 | 2 | Example: sliding-window truncation that keeps system instructions through KV cache reuse | example | none | | R1 |
| P2-13 | 2 | Example: put aggressively summarized documents in the middle of prompts to fight attention decay | example + advice | none | | R1 |
| P2-14 | 2 | Example: SGLang serves thousands of parallel requests sharing one system prompt without recomputing the prefix | example | 5, 6 | | R1 |
| P2-15 | 2 | Curriculum: the KV cache grows linearly with sequence length | mechanism | none | | R1 |
| P2-16 | 2 | Curriculum: caching middleware that tracks tokens, evicts stale context and monitors API cost | curriculum | none | | R1 |
| P3-01 | 3 | Generation is stateless; the model has no persistent memory outside its frozen weights | mechanism | none | | R1 |
| P3-02 | 3 | Memory engineering relies on a three-part taxonomy: episodic, semantic, procedural | taxonomy | none | | R1 |
| P3-03 | 3 | Episodic memory is typically kept in NoSQL document databases or run through MemGPT | practice | none | typically | R1 |
| P3-04 | 3 | In embedding space, geometric proximity equates to semantic similarity | mechanism | none | equates | R1 |
| P3-05 | 3 | Procedural memory stores executable skills, rules and configurations | definition | none | | R1 |
| P3-06 | 3 | Memory reads and writes run asynchronously in parallel with model execution | mechanism | none | | R1 |
| P3-07 | 3 | Strictly necessary tools: MemGPT (illusion of infinite context), Redis (sub-millisecond retrieval), Pinecone, ChromaDB, Qdrant | named tools + number | none | strictly necessary; infinite | R1 |
| P3-08 | 3 | Examples: multi-week preference recall, agent scratchpads, vector-indexed conversation history | examples | none | | R1 |
| P3-09 | 3 | Curriculum: cosine similarity and Euclidean distance; Redis-backed sliding window; MemGPT-style self-managed memory loop | curriculum | none | | R1 |
| P4-01 | 4 | AI infrastructure is centered on NVIDIA Hopper | currency | 7-10 | | R2 |
| P4-02 | 4 | H100 SXM5 has 80 GB of HBM3 | number | 7-10 | | R2 |
| P4-03 | 4 | Up to 3.35 TB/s memory bandwidth | number | 7-10 | | R2 |
| P4-04 | 4 | 132 SMs on the GH100 die | number | 9, 10 | | R2 |
| P4-05 | 4 | Multi-node training is rarely compute-bound and usually bound by inter-GPU bandwidth | claim | 7-10 | rarely | R2 |
| P4-06 | 4 | Fourth-generation NVLink and NVSwitch resolve that bottleneck | mechanism | 9 | | R2 |
| P4-07 | 4 | NVLink gives 900 GB/s bidirectional GPU-to-GPU bandwidth | number | 9 | | R2 |
| P4-08 | 4 | Eight GPUs on one baseboard act as a unified memory pool | mechanism | 7, 9 | | R2 |
| P4-09 | 4 | The Transformer Engine supports FP8 natively | mechanism | 9 | | R2 |
| P4-10 | 4 | E4M3 for forward-pass weights and activations, E5M2 for gradients | mechanism | 9 | | R2 |
| P4-11 | 4 | Precision is scaled dynamically | mechanism | 9 | | R2 |
| P4-12 | 4 | Nearly 3,958 sparse TFLOPS per GPU | number | 8, 9 | | R2 |
| P4-13 | 4 | 700 W thermal design power | number | 8, 9 | | R2 |
| P4-14 | 4 | Tools: CUDA, Slurm, Kubernetes, vLLM | named tools | none | | R2 |
| P4-15 | 4 | Example: 8x H100 SXM5 DDP training draws upwards of 5.6 kW of GPU power | number | 7 | | R2 |
| P4-16 | 4 | Example: Kubernetes autoscaling over PCIe H100s; nvidia-smi and DCGM for NVLink throughput and thermal throttling | examples + tools | none | | R2 |
| P4-17 | 4 | Curriculum: NVLink and NVSwitch radically reduce latency versus PCIe Gen5 | comparison | 9 | radically | R2 |
| P4-18 | 4 | Curriculum: HBM3 versus DDR; PyTorch distributed data parallel | curriculum | none | | R2 |
| P5-01 | 5 | RAG turns recall into reading comprehension, drastically reducing hallucination | finding | none | drastically | R3 |
| P5-02 | 5 | Modern retrieval fuses dense and sparse signals rather than plain cosine similarity | practice | 11, 12 | | R3 |
| P5-03 | 5 | RRF needs no score normalization or supervised tuning | mechanism | 11, 12 | | R3 |
| P5-04 | 5 | Formula score = sum of 1/(k + rank(d)) | formula | 11, 12 | | R3 |
| P5-05 | 5 | k is a stabilizing constant, typically 60 | number | 11, 12 | | R3 |
| P5-06 | 5 | Agreement across retrievers vastly outweighs one anomalous first place | mechanism | 11, 12 | vastly | R3 |
| P5-07 | 5 | ColBERTv2 is late interaction and keeps token-level embeddings | mechanism | 13, 14 | | R3 |
| P5-08 | 5 | Formula MaxSim: score(Q, D) = sum over query tokens of the max inner product with document tokens | formula | 13, 14 | | R3 |
| P5-09 | 5 | Late interaction vastly improves accuracy over single-vector pooling | finding | 13, 14 | vastly | R3 |
| P5-10 | 5 | Tools: Elasticsearch, ChromaDB, FAISS, Pinecone | named tools | 11 | | R3 |
| P5-11 | 5 | Examples: hybrid BM25 + dense policy bot; ColBERTv2 contract matching; BM25 top-100 then cross-encoder rerank of top 10 | examples | none | | R3 |
| P5-12 | 5 | Curriculum: recursive and semantic chunking; BM25's vocabulary-mismatch failure | curriculum | none | | R3 |
| P6-01 | 6 | ReAct is the foundational paradigm of agent engineering | attribution | none | | R4 |
| P6-02 | 6 | In ReAct, tools are strictly mapped through JSON schemas in the system prompt | mechanism | none | strictly | R4 |
| P6-03 | 6 | Loop: reasoning, action, deterministic execution, observation fed back, until a terminal output | mechanism | none | deterministic | R4 |
| P6-04 | 6 | Error handling is the most critical part; feeding stack traces back lets the model self-correct | claim | none | most critical | R4 |
| P6-05 | 6 | Frameworks: LangGraph, CrewAI, AutoGen, OpenAI Assistants API | named tools | 30-33 | | R5 |
| P6-06 | 6 | Examples: sandboxed coding agent; analyst reading SEC filings with OCR; agent that executes refunds on its own | examples | none | | R4 |
| P6-07 | 6 | Curriculum: a raw while-loop that runs local functions from model output strings | curriculum | none | | R4 |
| P7-01 | 7 | "Harness engineering" means building deterministic test scaffolding, sandboxes and verification harnesses for agents | term | none | deterministic | R4 |
| P7-02 | 7 | Isolation is a mandatory security primitive for agents that run code | claim | 15-18 | mandatory | R4 |
| P7-03 | 7 | gVisor is an application kernel: a user-space Go process that intercepts system calls | mechanism | 15, 16 | | R4 |
| P7-04 | 7 | Docker containers share the host kernel, a massive attack surface | mechanism | 15, 18 | massive | R4 |
| P7-05 | 7 | The Sentry intercepts syscalls via seccomp (systrap) or KVM | mechanism | 16, 17 | | R4 |
| P7-06 | 7 | File access goes through a separate unprivileged Gofer process over 9P or directfs | mechanism | 16 | | R4 |
| P7-07 | 7 | gVisor isolates better than namespaces without the heavy boot time and memory overhead of VMs like Firecracker | comparison | 15, 18 | heavy | R4 |
| P7-08 | 7 | Tools: Pytest, Docker, gVisor (runsc), custom eval runners | named tools | 16 | | R4 |
| P7-09 | 7 | Example: a gVisor sandbox ensures malicious syscalls cannot compromise the host | claim | 15-17 | ensuring | R4 |
| P7-10 | 7 | Examples: 500 prompt variations in Pytest; GitHub Actions behavioral tests before merging prompt changes | examples | none | | R4 |
| P7-11 | 7 | Curriculum: standard Docker is insufficient for untrusted code; switch the runtime to runsc | claim + procedure | 15, 16, 18 | | R4 |
| P8-01 | 8 | Orchestration is modeled as a DAG or a cyclic state graph | framing | none | | R5 |
| P8-02 | 8 | Routers send simple queries to highly quantized fast models and complex ones to larger models | pattern | none | | R5 |
| P8-03 | 8 | Evaluator-optimizer loops rewrite until a quality threshold is met | pattern | none | | R5 |
| P8-04 | 8 | Temporal, Airflow, LangGraph and Celery are the industry standard | named tools | none | industry standard | R5 |
| P8-05 | 8 | Examples: FAQ routing to a cache; translation evaluator-optimizer; map-reduce over 50 chunks with Celery | examples | none | | R5 |
| P8-06 | 8 | Curriculum: asyncio; retries with exponential backoff and jitter; LangGraph conditional edges on structured outputs | curriculum | none | | R5 |
| P9-01 | 9 | Evals replace subjective vibe checks with datasets, metrics and programmatic scoring | framing | none | | R6 |
| P9-02 | 9 | String matching and token-level probabilities fail to detect meaning-level hallucination | claim | 19, 20 | fail | R6 |
| P9-03 | 9 | Semantic entropy: sample answers, cluster by bidirectional meaning, take entropy over clusters | mechanism | 19 | | R6 |
| P9-04 | 9 | Formula H = - sum p(C_k) log p(C_k) | formula | 19 | | R6 |
| P9-05 | 9 | Low semantic entropy means confident meaning; high flags arbitrary, incorrect confabulations | finding | 19 | | R6 |
| P9-06 | 9 | MIPROv2 stands for Multiprompt Instruction PRoposal Optimizer Version 2 | name | 22, 24 | | R6 |
| P9-07 | 9 | MIPROv2 uses Bayesian optimization over instruction and few-shot combinations | mechanism | 22, 24 | | R6 |
| P9-08 | 9 | GEPA evolves prompts reflectively across a Pareto front, frequently scoring higher with vastly fewer rollouts | finding | 22, 24 | vastly | R6 |
| P9-09 | 9 | Tools: DeepEval, Ragas, Phoenix (Arize), DSPy | named tools | none | | R6 |
| P9-10 | 9 | Example: semantic entropy probes flag divergent answers in a medical RAG pipeline | example | 19, 20 | | R6 |
| P9-11 | 9 | Example: MIPROv2 raises validation exact-match accuracy by 15% | number | 21-24 | | R6 |
| P9-12 | 9 | Example: GPT-4 as judge of a smaller local quantized model | example | none | | R6 |
| P9-13 | 9 | Curriculum: precision, recall, F1 and AUROC have severe limits for generative text; calibrate an LLM judge with few-shot rubrics | curriculum | none | | R6 |
| P10-01 | 10 | KV cache fragmentation limits batch size | mechanism | 25 | | R2 |
| P10-02 | 10 | PagedAttention, modeled on OS virtual-memory paging, stores KV in non-contiguous blocks | mechanism | 25 | | R2 |
| P10-03 | 10 | PagedAttention cuts internal fragmentation to near-zero | number | 25 | near-zero | R2 |
| P10-04 | 10 | It allows massive batch-size increases through continuous batching | claim | 25 | massive | R2 |
| P10-05 | 10 | Autoregressive generation is memory-bandwidth bound | mechanism | 26, 27 | | R2 |
| P10-06 | 10 | Speculative decoding: draft M_q proposes gamma tokens; target M_p scores them in one parallel pass; rejection sampling accepts or rejects | mechanism + notation | 26, 27 | | R2 |
| P10-07 | 10 | It speeds generation without changing the output distribution | finding | 26, 27 | | R2 |
| P10-08 | 10 | Tools: vLLM, TensorRT-LLM, Ollama, llama.cpp | named tools | none | | R2 |
| P10-09 | 10 | Example: Llama 3 8B in GGUF Q4_K_M fits a consumer GPU | number + example | none | | R2 |
| P10-10 | 10 | Example: vLLM serves hundreds of concurrent requests without running out of KV cache memory | claim | 25 | | R2 |
| P10-11 | 10 | Example: a 1B draft with a 70B target effectively doubles tokens per second | number | 26, 27 | | R2 |
| P10-12 | 10 | Curriculum: FP16, INT8, INT4 trade-offs; KV cache grows linearly with context; rejection sampling keeps the exact distribution | curriculum | 25-27 | | R2 |
| P11-01 | 11 | Platform engineering packages models, retrieval and orchestration behind REST or GraphQL APIs | framing | none | | R4 |
| P11-02 | 11 | Server-Sent Events push tokens to the client the exact moment they are generated | mechanism | none | exact moment | R4 |
| P11-03 | 11 | Kubernetes supports secure multi-tenant environments | claim | none | | R4 |
| P11-04 | 11 | Tools: FastAPI, LangServe, Docker, API gateways | named tools | none | | R4 |
| P11-05 | 11 | Examples: FastAPI with OAuth2 and JWT; a gateway logging every prompt and generation to Datadog or Prometheus; SSE to React | examples | none | | R4 |
| P11-06 | 11 | Curriculum: WebSockets versus SSE; separate web server from inference engine; auth, rate limits, structured logs | curriculum | none | | R4 |
| P12-01 | 12 | Threats include prompt injection, jailbreaking, data exfiltration and toxic output | taxonomy | none | | R7 |
| P12-02 | 12 | Data and instructions are hard to separate at the transformer level | mechanism | none | | R7 |
| P12-03 | 12 | Llama Guard 3 is an LLM fine-tuned for safety classification across risk taxonomies | named tool | 28, 29 | | R7 |
| P12-04 | 12 | Routing prompts and responses through Llama Guard deterministically blocks policy-violating text | claim | 28, 29 | deterministically | R7 |
| P12-05 | 12 | Defense in depth requires sanitizing inputs against injection (Base64 obfuscation, role-play) | practice | none | | R7 |
| P12-06 | 12 | Tools: OWASP Top 10 for LLMs, NeMo Guardrails, Garak (a comprehensive vulnerability scanner) | named tools | none | comprehensive | R7 |
| P12-07 | 12 | Examples: input classifier that blocks jailbreaks; PII redaction; Llama Guard 3 refusals for harmful code | examples | none | | R7 |
| P12-08 | 12 | Curriculum: study injection mechanics; filter proxy with a risk threshold; output guardrails enforce rigid policy on all generated text | curriculum | none | all | R7 |
| B1-01 | B1 | One mega-prompt doing zero-shot reasoning becomes highly fragile as tasks grow; specialized agents fix this | claim | 30-33 | highly fragile | R5 |
| B1-02 | B1 | LangGraph: controllable cyclic state graph, explicit routing, thread-scoped checkpoints | tool mechanism | 30-33 | | R5 |
| B1-03 | B1 | LangGraph caches node results and skips nodes whose input state is unchanged | tool feature | 30-33 | | R5 |
| B1-04 | B1 | LangGraph is vastly superior for high-compliance work and resuming tasks | comparison | 30-33 | vastly | R5 |
| B1-05 | B1 | CrewAI: role-based, task-centric sequential delegation, hierarchical; fastest to prototype linear teams | tool mechanism | 30-33 | | R5 |
| B1-06 | B1 | CrewAI has less structural durability for complex multi-stage approval chains | comparison | 30-33 | | R5 |
| B1-07 | B1 | Examples and curriculum: legal swarm, software team with Jira, escalation to a human on frustration; HITL breakpoints | examples | none | | R5 |
| B2-01 | B2 | Prompt-based alignment ("do not be toxic") is highly susceptible to jailbreaks | claim | none | | R7 |
| B2-02 | B2 | Programmable guardrails solve this with deterministic, isolated filter boundaries | claim | none | solve; deterministic | R7 |
| B2-03 | B2 | NeMo Guardrails uses Colang to define deterministic dialog flows | tool mechanism | none | deterministic | R7 |
| B2-04 | B2 | Guardrails can reroute to a safe fallback without ever invoking the generative model | mechanism | none | never | R7 |
| B2-05 | B2 | Llama Guard scores inputs and agent strings against customized taxonomies | tool mechanism | none | | R7 |
| B2-06 | B2 | Example: a deterministic guardrail blocks any input semantically similar to an instruction-override request | example | none | deterministic | R7 |
| B2-07 | B2 | Example: Colang flows force a banking assistant to refuse political or off-topic branches | example | none | | R7 |
| B2-08 | B2 | Curriculum: limits of "soft-prompt alignment (RLHF)"; Colang syntax; local Llama Guard | terminology | none | | R7 |
| B3-01 | B3 | Dense-vector RAG frequently struggles with multi-hop reasoning | finding | none | | R3 |
| B3-02 | B3 | GraphRAG has an LLM extract entities and relationships into a graph database such as Neo4j | mechanism | none | | R3 |
| B3-03 | B3 | Retrieval uses graph traversal queries such as Cypher | mechanism | none | | R3 |
| B3-04 | B3 | This drastically improves global synthesis questions | finding | none | drastically | R3 |
| B3-05 | B3 | Examples and curriculum: regulatory webs, enterprise knowledge graphs, drug side effects; Cypher; hybrid vector plus graph traversal | examples | none | | R3 |
| B4-01 | B4 | Sending data to cloud APIs is a non-starter for medical, defense and finance work | claim | none | non-starter | R7 |
| B4-02 | B4 | Local orchestration ensures complete data sovereignty, zero cloud telemetry and total air-gapped security | claim | none | ensures; complete; zero; total | R2 |
| B4-03 | B4 | Local deployment uses containerized runtimes | mechanism | none | | R2 |
| B4-04 | B4 | llama.cpp and Ollama run models on consumer and edge hardware through GGUF quantization | tool mechanism | none | | R2 |
| B4-05 | B4 | 16-bit to 4-bit compression runs with minimal precision loss | claim | none | minimal | R2 |
| B4-06 | B4 | Runs on Apple Silicon unified memory or local NVIDIA GPUs | tool support | none | | R2 |
| B4-07 | B4 | It creates a zero-latency inference boundary entirely disconnected from the internet | claim | none | zero-latency; entirely | R2 |
| B4-08 | B4 | Example: local summarization of patient records avoids violating HIPAA through zero external network transmission | legal claim | none | | R7 |
| B4-09 | B4 | Examples: air-gapped M&A analysis; code assistance inside a defense intranet | examples | none | | R2 |
| B4-10 | B4 | Curriculum: GGUF vs AWQ vs GPTQ; map parameters to VRAM by quantization level; serve a quantized Llama 3 with Ollama; call its HTTP API like a cloud API | curriculum | none | | R2 |
| C-01 | Concl. | The shift is a fundamental, permanent maturation | framing | none | permanent | LEAD |
| C-02 | Concl. | The blueprints are the definitive roadmap | framing | none | definitive | LEAD |
| C-03 | Concl. | Systems built this way are highly deterministic, optimized and secure | claim | none | deterministic | LEAD |
| T-01 | Terms | Each of the 16 headings names an established discipline, defined as commonly used | terms | none | | R1-R7 (own pillars) |
