# Engineering Stack Glossary

*Terms defined in the AI Engineering Stack series (claude/engineering-stack-plan.md), with the plain meaning first. Each part adds its terms here when it is saved; the part that defines a term carries its sources and tags, so a key such as `[V: FAR]` points to that part's Section 12. Last updated October 20, 2026, with Part 13 (313 terms).*

| Term | In plain words | Notes | Defined in |
|---|---|---|---|
| 400 error | The API rejecting a request as invalid | An HTTP status code; the request never reaches the model. | Part 03, §2 |
| 95th percentile; p95 | The value that 95 of every 100 measurements are at or below | Compute it from histograms, which can be combined across servers; pre-computed quantiles can't [V: PRM]. | Part 13, §2 |
| A2A (Agent2Agent) | A protocol for agents to hand work to other agents | v1.0.1; a Linux Foundation project [V: A2S, A2L]. | Part 07, §3.9 |
| Acceptance rate (α) | The share of a draft model's guesses the big model accepts | Leviathan et al.'s α; speculation can pay only if α beats the draft's cost c [V: LEV][T]. | Part 11, §3.5 |
| Accessibility tree | A text outline of a page's elements that programs can read | An alternative to screenshots for web agents [V: PWM]. | Part 08, §3.10 |
| Accuracy | The share of cases right | Report it with its interval and the number of cases. | Part 02, §2 |
| Activity (Temporal) | One action a Temporal workflow hands off, such as calling a service or a model | Retried by default (1 s, x2, up to 100 s, no attempt limit); "may be executed multiple times" [V: TDC, TPS]. | Part 09, §3.4 |
| Adapter (LoRA) | The saved LoRA matrices, loaded on top of the base model | Megabytes, not gigabytes: 83.9 MB for Llama 3 8B at r = 16 on all linear layers, at 2 bytes per weight [T] | Part 12, §3.7 |
| Adaptive attack | An attack tuned against the specific defence it faces | Nasr et al. got past all 12 defences they tested this way [V: NAS]. | Part 10, §3.4 |
| Agent; agent loop | A model calling tools in a loop until the task is done | "LLMs using tools based on environmental feedback in a loop" [V: BEA]. | Part 08, §1 |
| Agent as tool | Calling another agent like a tool, with only the input the manager writes for it | OpenAI's `Agent.as_tool()`; only the final output comes back [V: OAS]. | Part 09, §2 |
| Agent Card | A public file describing an A2A agent | At `/.well-known/agent-card.json` (`agent.json` before 0.3.0) [V: A2S]. | Part 07, §3.9 |
| Agent Skill; `SKILL.md` | A folder of instructions and scripts an agent loads when needed | Name 1 to 64 characters, description 1 to 1,024 in the open spec [V: ASK]. | Part 07, §3.10 |
| Agents Rule of Two | At most two of untrusted input, sensitive access and outward action in a session without a person's approval | Meta's rule; OWASP 2026 calls it "a floor" [V: RO2, OW6]. | Part 10, §3.3 |
| `AGENTS.md` | A project instruction file for coding agents | Plain Markdown; stewarded by the Agentic AI Foundation [V: AGM]. | Part 07, §3.9 |
| alpha; LoRA scaling | How strongly a LoRA update is applied | The update is multiplied by alpha / r (alpha / sqrt(r) with rsLoRA); PEFT's defaults are r 8, alpha 8 [V: PFT] | Part 12, §3.7 |
| API key | A password that lets a program use a paid service | No lab in this series needs one. | Part 01, §2 |
| Approximate nearest neighbour search (ANN) | Finding close vectors fast without checking every one | Trades a little recall for speed; HNSW and IVF are two methods. Exact search is often fast enough for small collections [V: FAW, PGV]. | Part 05, §3.3 |
| Arena (Chatbot Arena) | A ranking built from crowd votes on pairs of anonymous answers | Bradley-Terry scores with confidence intervals; its links now lead to arena.ai [V: ARN, ARP] | Part 12, §3.1 |
| Attack success rate (ASR) | The share of attack attempts that work | Always give its model, setting and attacker [V: API]. | Part 08, §3.11 |
| AUROC, the area under the ROC curve | How well a score separates two groups | The chance that a random positive scores above a random negative [V: FAW]: 0.5 is chance, 1.0 is perfect. | Part 02, §2 |
| Automation bias | Trusting an automated suggestion without checking it | Grows with workload, task complexity and time pressure in a 2012 review of clinical tools [V: GRW]. | Part 09, §2 |
| Base rate | How common the thing you're screening for really is | At low base rates most of a classifier's flags are false alarms [T]. | Part 10, §3.7 |
| `base_model` | The model a fine-tune, adapter, quantization or merge was made from | A Hugging Face model-card field; the base model's licence can still apply [V: HFC] | Part 12, §3.3 |
| Batch API | Half-price jobs answered within a day | All three big vendors; Anthropic and OpenAI give 24 hours, Gemini expires jobs at 48 [V: AND, OAD, GMD]. | Part 13, §2 |
| Bi-encoder | An embedding model that encodes the question and each chunk separately | Fast: chunk vectors are made once, in advance. | Part 05, §2 |
| Bits per weight (bpw) | Average storage per weight, scales included | Q4_K_M on Llama 3 8B: 4.8944 [T], as llama.cpp's table gives for Llama 3.1 8B [V: LCP]. | Part 11, §3.3 |
| Block (quantization) | A group of weights sharing one scale | Q4_K: 256 weights in 144 bytes [V: LCP]. | Part 11, §3.3 |
| BM25 (Okapi BM25) | The standard keyword scoring formula | Rare words count more, repeats help less and less, long chunks are penalized; k1 and b set how much [V: RZ09]. | Part 05, §3.1 |
| Break-even point | The number of reuses at which caching starts to save money | One write at *w* times the input price, then reads at *r*: caching wins when reads exceed (*w* - 1) / (1 - *r*); one read for a 1.25x write, two for a 2x write [T]. | Part 04, §3.6 |
| Breakpoint; `cache_control` | The place in a prompt where you ask the provider to cache everything before it | Anthropic allows up to 4 per request [V: APC]. | Part 04, §2 |
| Business associate agreement (BAA) | A contract that lets a vendor handle a HIPAA covered entity's health data | Needed before PHI reaches a cloud or model provider [V: HHC]. | Part 10, §3.9 |
| Cache write; cache read (hit); cache miss | Storing a prefix the first time; using it again; finding nothing usable | A write can cost more than normal input (1.25x or 2x at Anthropic); a read costs much less [V: APC, OPC]. | Part 04, §2 |
| Capabilities (MCP) | What a client or server says it can do | Sent with every request since 2026-07-28 [V: MCL]. | Part 07, §2 |
| Chat template | A model's fixed way of laying out a conversation as text | With the wrong control tokens, "drastically worse performance" [V: TFM] | Part 12, §3.8 |
| Checkpoint | A saved snapshot of a run's state | LangGraph saves one per super-step, keyed by a thread id [V: LGD]. | Part 09, §2 |
| Checksum | A fingerprint the publisher lists, to compare with your own | Python and Node.js publish SHA-256 checksums for their downloads [V: P313, NVB]. | Part 01, §2 |
| Chunk; passage; chunking | One searchable piece of a document; cutting documents into such pieces | No single best size; test a few on your own questions [V: BHT]. | Part 05, §3.7 |
| Cohen's kappa | Agreement between two graders beyond what chance gives | (p_o - p_e) / (1 - p_e) [V: SKK]. | Part 02, §2 |
| Community; community detection | A group of nodes more connected to each other than to the rest; finding such groups | GraphRAG summarizes each community [V: MGR]. | Part 06, §3.3 |
| Compaction | Replacing old turns of a conversation with a summary the model writes | A server feature (beta at Anthropic); the summary is an extra billed call and loses detail [V: ACO, OCP]. | Part 04, §3.3 |
| Compaction; context editing | Shortening an old conversation, or clearing old tool results, to make room | Early instructions may be lost; keep lasting rules in instruction files [V: SDL, CED]. | Part 08, §3.4 |
| Complete mediation | Checking authorization in code for every action, never by asking the model | An OWASP LLM03:2026 mitigation [V: OW6]. | Part 10, §3.3 |
| Completion-only loss; prompt masking | Learning only from the answer part of each training example | TRL's default for prompt and completion data [V: TRL] | Part 12, §3.8 |
| Computer use | A model operating a screen with mouse and keyboard | Each screenshot costs about 1,000 to 1,800 input tokens (Anthropic) [V: ACU]. | Part 08, §3.10 |
| Confabulation | A wrong answer that changes from one sample to the next | Farquhar et al.: claims "both wrong and arbitrary" [V: FAR]. | Part 02, §2 |
| Confidence interval | A range that probably holds the true value | The series writes "interval"; its labs use the Wilson score interval [V: NIST]. | Part 02, §2 |
| Confused deputy | An attacker tricking a trusted program into using its own permissions for them | In MCP, a proxy server forwarding to another service [V: MAU]. | Part 07, §3.7 |
| Confusion matrix | A table of which label went where | Rows: the correct label. Columns: the label given [T]. | Part 02, §2 |
| Constrained decoding; structured outputs | Making the model's output follow a schema as it is written | Anthropic: "guarantee schema-compliant responses through constrained decoding", with documented exceptions [V: ASO]. | Part 03, §2 |
| Container escape | Breaking out of a container to the host | runc has had several; keep the runtime patched [V: C24, RUN]. | Part 08, §3.7 |
| Container runtime (runc; runsc) | The software that starts containers | runsc is gVisor's runtime [V: GVQ]. | Part 08, §3.7 |
| Contamination | Test items that leaked into what the model saw | Scores then measure memory as well as skill [V: GSM]. | Part 02, §2 |
| Content capture | Recording prompts and answers in traces | Opt-in in the GenAI conventions ("SHOULD NOT capture them by default"); Traceloop, OpenLIT, OpenInference and Logfire record them by default [V: GAI, TLP, OLT, OIN, LGF]. | Part 13, §2 |
| Context budget | Planning which parts of a request go into the window | This series' term: reserve output, keep the essentials, add the rest by priority. | Part 04, §3.2 |
| Context; context window | Everything a model reads and writes in one request, and its maximum size | Input, output and thinking all count, cached tokens too [V: ACW]. | Part 04, §2 |
| Context editing | Removing old tool results or thinking from a conversation's history | Anthropic, beta; it invalidates cached prefixes [V: ACX]. | Part 04, §3.3 |
| Context engineering | Choosing and arranging what goes into the context window | Anthropic: "the smallest possible set of high-signal tokens" [V: ACE]. | Part 04, §2 |
| Contextual retrieval | Prepending a short, model-written note on where a chunk sits in its document before indexing it | Anthropic's method and its own evaluation [V: ACR]. | Part 05, §3.6 |
| Continue-as-new | Starting a fresh Temporal run that carries the state forward | A way round the per-run history limit (51,200 events or 50 MiB) [V: TSV]. | Part 09, §3.4 |
| Continuous batching; iteration-level scheduling | Letting requests join and leave a batch at every model step | Orca's idea (OSDI 2022); also called in-flight or persistent batching [V: ORC, VSR]. | Part 11, §3.4 |
| Continuous integration (CI) | Tests that run automatically on every change | Not the same as a confidence interval. | Part 02, §2 |
| Convex combination (CC); weighted fusion | Merging two result lists by a weighted sum of rescaled scores | Beat RRF in a peer-reviewed comparison once its weight was tuned [V: BRU]. | Part 05, §3.4 |
| Corpus | The pile of documents you search |  | Part 05, §2 |
| Cosine similarity; dot product | How closely two vectors point the same way | Equal when both vectors have length 1 [V: STD]. | Part 05, §3.2 |
| Covered entity (HIPAA) | A health plan, health-care clearinghouse, or provider that sends health information electronically in standard transactions | HIPAA applies to these and their business associates [V: HHS]. | Part 10, §3.9 |
| Cross-encoder | A model that reads a question and one chunk together and scores the pair | Usually more accurate, much slower; used to rerank a short list [V: SBR, SCE]. | Part 05, §3.5 |
| CVE; CVSS; NVD | A public ID for a security flaw; its severity score; the US database that lists them | CVSS 3.1 and 4.0 scores aren't comparable; note who scored it [V: C49]. | Part 07, §3.11 |
| Cypher; GQL | Neo4j's graph query language; the ISO standard (ISO/IEC 39075:2024) it helped shape | Neo4j is "working towards full GQL conformance" [V: GQL, OCY]. | Part 06, §3.1 |
| De-identification (Safe Harbor; Expert Determination) | HIPAA's two routes to data that is no longer protected health information | Safe Harbor removes 18 kinds of identifier; remaining risk is "very small", not zero [V: HHD]. | Part 10, §3.8 |
| Decode | Writing the answer one token at a time | Limited by memory bandwidth at small batch sizes [V: VLL, POP]. | Part 11, §3.1 |
| Demonstrations; demos; few-shot examples | Worked input and output pairs placed in a prompt |  | Part 03, §2 |
| Dense retrieval; semantic search; vector search | Search by comparing embeddings | Strong in domain; can fall well below BM25 out of domain [V: DPR, BEI]. | Part 05, §3.2 |
| Digital signature | A publisher's tamper-evident seal | Python offers Sigstore and GPG signatures; Node.js signs its list of checksums [V: P313, NVB]. | Part 01, §2 |
| Directed acyclic graph (DAG) | A graph of steps with no loops | Airflow's model; a LangGraph graph may loop, so it isn't one [V: AFL, LGD]. | Part 09, §2 |
| Discordant pairs | The cases where only one of two versions is right | McNemar's test uses only these [V: FLL]. | Part 02, §2 |
| DPO (direct preference optimization) | Training on pairs of a preferred and a rejected answer | No separate reward model (NeurIPS 2023) [V: DPO] | Part 12, §3.7 |
| Durability mode | When a checkpoint is written | LangGraph: `"exit"`, `"async"` (the default) or `"sync"` [V: LGS]. | Part 09, §3.3 |
| Durable execution | Progress that survives crashes, restarts and long waits | Temporal's definition [V: TDC]. | Part 09, §2 |
| Effectively once | Run at least once, with the effect made idempotent, so the result happens once | Temporal's phrase [V: TDC]. | Part 09, §3.5 |
| Effort; reasoning effort | How hard a reasoning model thinks | Anthropic `output_config.effort`; OpenAI `reasoning.effort` [V: AEF, ORS]. | Part 03, §3.6 |
| Elicitation | An MCP server asking the user a question through the client | The one client feature the 2026-07-28 overview lists [V: MSP]. | Part 07, §3.2 |
| Embedding; vector | A list of numbers that stands for a text's meaning, as a model learned it | Nearness approximates relatedness; it isn't the same as meaning [V: MTB, NEV]. | Part 05, §3.2 |
| Entity and relation extraction | Turning text into nodes and edges, usually with a model | Misses things: about a third of answer entities in one study [V: HAN]. | Part 06, §3.2 |
| Entity resolution | Deciding that two names mean the same thing and merging them | neo4j-graphrag merges only identical names by default [V: N4G]. | Part 06, §3.2 |
| Enum | A fixed list of allowed values | `"enum": ["low", "normal", "urgent"]` | Part 03, §2 |
| `.env` file | A file of `NAME=value` lines that stays out of Git | Plain text on your disk [T]. | Part 01, §2 |
| Environment variable | A named setting that programs started from your terminal can read | Programs started from a terminal inherit it, and a change made in PowerShell lasts only for that session [V: PSE]. | Part 01, §2 |
| ePHI | Health information HIPAA protects, in electronic form | Covered whether created, received, maintained or transmitted [V: HHS]. | Part 10, §3.9 |
| Episodic, semantic, procedural and working memory | CoALA's four kinds of agent memory: past events, facts, the weights plus the agent's code, and the current decision cycle | [V: COA] | Part 06, §3.6 |
| Eval | A repeatable test of an AI system | Inputs, a grading rule and a summary. | Part 02, §2 |
| Evaluator-optimizer | One model writes, another judges, in a loop | Needs an iteration cap; no numeric threshold in the source [V: BEA]. | Part 09, §2 |
| `EventSource` | The browser object that reads SSE and reconnects by itself | Sends `Last-Event-ID` when it reconnects; can't add an `Authorization` header; an HTTP 204 stops it reconnecting [V: WSS]. | Part 13, §2 |
| Excessive agency | An agent with more tools, permissions or freedom than its job needs | OWASP LLM03:2026 [V: OW6]. | Part 10, §1 |
| Exfiltration through rendered output | Data leaving through a link or image URL the model writes | ATLAS AML.T0077; the lab's `clean_output` removes such links [V: ATL][T]. | Part 10, §3.3 |
| F1 | One number that balances precision and recall | 2PR / (P + R) [V: SKM]. | Part 02, §2 |
| False-positive rate (FPR) | The share of harmless items a classifier wrongly flags | Published rates are measured on the vendor's own test set [V: LG4]. | Part 10, §2 |
| Fine-tuned | Trained further on labelled examples for one task |  | Part 05, §2 |
| Fine-tuning; supervised fine-tuning (SFT) | Training an existing model further on your own examples, so its weights change | Good for formats and habits; poor for new facts, where retrieval beat it by 19 to 37 points in one study [V: HFL, OVA] | Part 12, §1 |
| Firecracker; microVM | A very small virtual machine, and the program that runs them | Specification: 125 ms boot and 5 MiB overhead under stated conditions [V: FCS]. | Part 08, §3.8 |
| Forgetting | A model losing earlier skills after more training | LoRA forgets less than full fine-tuning in Biderman et al. [V: BID] | Part 12, §3.7 |
| Full fine-tuning | Training every weight of a model | About 16 bytes per weight with Adam in mixed precision, before activations [V: ZER] | Part 12, §3.7 |
| Full jitter | Waiting a random time between zero and the backoff limit before a retry | `uniform(0, min(cap, base * 2 ** n))` [V: AWC]. | Part 09, §3.5 |
| Gate | Pass-or-fail rules applied to eval results before a change ships | Fixed before the results are seen. | Part 02, §2 |
| GenAI semantic conventions (OpenTelemetry) | Agreed names for AI telemetry: the model, token counts, finish reason | Status Development; moved to `semantic-conventions-genai` on May 5, 2026; span name `chat {model}` [V: GAI, SCV]. | Part 13, §2 |
| GGUF | The file format llama.cpp and Ollama load | Tensors plus metadata, chat template included; version 3. A format, not a method like AWQ or GPTQ [V: GGS]. | Part 11, §3.3 |
| Git; the folder plus its history is a repository | The program that keeps every saved version of a folder | Open source under the GNU GPL version 2.0 [V: GAB]. | Part 01, §2 |
| `.gitignore` | The list of files Git should leave alone | It doesn't affect files Git already tracks [V: GIG]. | Part 01, §2 |
| Grader, or scorer | The rule that scores one output | Code, a model or a person [V: ANE]. | Part 02, §2 |
| Grammar; GBNF | A rulebook that tells a local model which tokens are allowed next | llama.cpp's format [V: LCG]. | Part 03, §2 |
| GraphRAG | Microsoft's method of building a graph and community summaries with a model, then searching them | Its repository is "largely in maintenance mode" [V: MGR]. | Part 06, §3.2 |
| Grouped-query attention (GQA) | Several query heads sharing one key and value head | Shrinks the KV cache; Llama 3 8B has 32 query heads and 8 KV heads [V: LLM]. | Part 11, §3.2 |
| GRPO (group relative policy optimization) | Reinforcement fine-tuning that scores several answers per prompt against their group's average | A TRL trainer [V: TRL] | Part 12, §3.7 |
| Guardrails | Checks around a model, by rules in code or by models | NeMo's term is "programmable guardrails"; not a security boundary by themselves [V: NEM]. | Part 10, §3.6 |
| Guides; sensors | Controls that steer an agent before it acts; checks that catch mistakes after | Böckeler's terms [V: FW2]. | Part 08, §3.5 |
| gVisor; Sentry | A kernel written in Go that runs in user space and handles a sandbox's system calls | Not a guarantee: "A sandbox is not a substitute for a secure architecture" [V: GVS]. | Part 08, §3.8 |
| Handoff | Passing the whole conversation to another agent, which takes over | OpenAI's default passes "the entire previous conversation history" [V: OAS]. | Part 09, §2 |
| Harness | Everything around the model that steers and checks an agent | Three senses: evaluation harness, built-in harness, guides and sensors [V: FW2, LEH, AHL]. | Part 08, §3.5 |
| Hash | A file's fingerprint | SHA-256 here. Change one byte of a file and its SHA-256 changes completely [T]. | Part 01, §2 |
| Head sampling; tail sampling | Deciding which traces to keep at the start, or after they end | Head sampling "cannot ensure that all traces with an error within them are sampled" [V: OTS]. | Part 13, §2 |
| Hidden Context Exposure | Extraction of system prompts, retrieved policy text or tool schemas | OWASP LLM08:2026, replacing System Prompt Leakage [V: OW6]. | Part 10, §3.1 |
| HMAC | A short code proving a message came from someone holding a secret key, and wasn't changed | The lab signs `requestState` with HMAC-SHA256 [T]. | Part 07, §3.6 |
| HNSW (hierarchical navigable small world) | A graph-based method for approximate nearest neighbour search | Settings M, efConstruction and efSearch [V: HNS, FAW]. | Part 05, §3.3 |
| Hook (agent) | Code that runs at fixed points in the loop and can block a tool | Enforced, unlike instruction files [V: CMM, CAS]. | Part 08, §3.5 |
| Host; client; server (MCP) | The AI application; its connector for one server; the program that offers tools | "Each client ... communicates with exactly one server" [V: MAR]. | Part 07, §3.2 |
| HTTP 429; 529 | Too many requests; Anthropic's platform overloaded | A 429 usually carries `retry-after`; Anthropic's spend-cap 429 never does [V: AND]. | Part 13, §2 |
| Human approval; human in the loop | A person approving an action before it runs | OWASP advises it for high-impact actions [V: OWL]. | Part 08, §3.3 |
| Hybrid search; fusion | Running keyword and dense search and merging the lists | Fusion can lose on a single question; measure it [T]. | Part 05, §3.4 |
| HyDE (hypothetical document embeddings) | Searching with an embedding of a fake answer a model wrote | One model call per question [V: HYD]. | Part 05, §3.6 |
| Idempotency key | A unique label sent with a request so a repeat is recognized | Must be checked by the side that performs the effect [V: STR][T]. | Part 09, §2 |
| Idempotent step | A step that has the same effect whether it runs once or twice | Needed because resumed and retried steps run again [V: LGD, TDC]. | Part 09, §2 |
| Importance matrix (imatrix) | Statistics from sample text that tell quantization which weights matter most | Llama 3 8B at Q4_K_M: +2.40% perplexity with one, +2.79% without, in llama.cpp's scoreboard [V: LCP][T]. | Part 11, §3.3 |
| Indirect prompt injection | Text on a page, screenshot or tool result that tries to instruct the model | Part 10 covers it in depth. | Part 08, §3.11 |
| Install script | A script piped from the web straight into a shell | `curl ... \| sh` or `irm ... \| iex`. | Part 01, §2 |
| Interrupt | Pausing a run until a person answers | LangGraph's `interrupt()`; the paused node runs again from its start on resume [V: LGD]. | Part 09, §2 |
| Inverse document frequency (IDF) | How rare a word is across the corpus; rare words count more | Lucene's version, log(1 + (N - n + 0.5) / (n + 0.5)), is never negative [V: LUC]. | Part 05, §3.1 |
| Inverted index | A lookup table from each word to the chunks that contain it | What keyword search engines build. | Part 05, §2 |
| Invisible Unicode; tag characters | Characters that render as nothing, some able to spell hidden text | U+E0000 to U+E007F; variation selectors can carry data too [V: OW6][T]. | Part 10, §3.2 |
| Jailbreak | Injection aimed at getting around safety rules | OWASP treats it as a kind of prompt injection [V: OW6]. | Part 10, §2 |
| JSON | Data written as nested names and values | `{"queue": "billing"}` | Part 03, §2 |
| JSON mode | A setting that only promises valid JSON, not your schema | OpenAI: "only Structured Outputs ensure schema adherence" [V: OSO]. | Part 03, §2 |
| JSON Schema; schema | A written description of the shape data must have | The current version is 2020-12 [V: JSS]. | Part 03, §2 |
| JSON-RPC 2.0 | A request and reply format written in JSON | Requests carry an `id`; replies carry `result` or `error` [V: MBP]. | Part 07, §3.2 |
| Keep-alive comment | A line that keeps an idle stream open | `: ping`, about every 15 seconds; FastAPI and sse-starlette send one after 15 seconds of silence [V: WSS, FAS, SSS]. | Part 13, §2 |
| Keyword search; lexical search; sparse retrieval | Search by matching the question's words | Fails on synonyms (vocabulary mismatch); strong on exact codes and names. | Part 05, §3.1 |
| Knowledge graph | A map of facts as nodes (things) and edges (links) | | Part 06, §1 |
| KV cache (key-value cache) | The model's stored working state for each processed token | What a prefix cache reuses; Part 11 covers it inside serving engines [V: VPC, SGL]. | Part 04, §2 |
| Late interaction; multi-vector retrieval (ColBERT) | Keeping one vector per token and matching token to token | MaxSim scoring; more storage than one vector per chunk [V: CB2]. | Part 05, §3.5 |
| Learned sparse retrieval (SPLADE) | Keyword-style vectors a model learns, adding related words | Runs on an ordinary inverted index [V: SPL]. | Part 05, §3.5 |
| Length degradation; "context rot" | Accuracy falling as the input gets longer | Robust across current studies [V: RUL, NOL, CHR]; "context rot" is Chroma's name. | Part 04, §3.4 |
| Lethal trifecta | Private data, untrusted content and a way to send data out, in one agent | Willison's term: remove one leg [V: LTF]. | Part 10, §3.3 |
| `LicenseRef-` identifier | A custom name for a licence the SPDX list doesn't have | Used for the Llama and Gemma terms [V: SPX]. | Part 10, §3.10 |
| Linux capabilities | Root's powers split into pieces that can be given or removed | Docker keeps 14 by default [V: MOB]. | Part 08, §3.7 |
| Little's law | Requests open at once = arrival rate x time each spends | L = λW; 5 requests a second at 8 seconds each holds 40 streams [V: LIT][T]. | Part 13, §2 |
| Long-context pricing | A higher price once a prompt passes a length | Whole request at OpenAI (GPT-6 Astra over 272,000 tokens) and for Claude Haiku 5.5 (over 100,000); Gemini's page doesn't say [V: OAD, AND, GMD]. | Part 13, §2 |
| Long-term support (LTS) | A release line kept up for years | nodejs.org says production applications should use only LTS releases [V: NPR]. | Part 01, §2 |
| LoRA (low-rank adaptation) | Two thin trained matrices beside a frozen layer | ΔW = BA; r x (inputs + outputs) trained weights per matrix [V: LOR] | Part 12, §3.7 |
| Louvain; Leiden | Two community-detection methods; Leiden guarantees connected communities | [V: LEI] | Part 06, §3.3 |
| `max_tokens` | The most tokens a reply may use | A reply that hits it stops mid-way and may break a schema [V: ASO]. | Part 03, §2 |
| MCP extension | An optional add-on both sides must agree to use | Tasks, MCP Apps, Skills over MCP [V: MSP, MSK]. | Part 07, §3.3 |
| Memory bandwidth | Bytes per second a chip can read from its memory | Sets the decode ceiling, bandwidth / bytes per token; H100 SXM: 3.35 TB/s [V: NVH][T]. | Part 11, §3.1 |
| Memory poisoning | Planting false or hostile entries in an agent's memory | OWASP ASI06, "Memory & Context Poisoning" [V: OWA]. | Part 06, §3.10 |
| `_meta` envelope | Extra information sent with every MCP request | Holds the protocol version and the client's capabilities; required since 2026-07-28 [V: MCL]. | Part 07, §2 |
| Mixture of experts (MoE) | A model where each token uses only some of its parts (experts) | gpt-oss-20b: 4 of 32 experts per token, about 3.71 GB read per token [V: GOS][T]. | Part 11, §3.2 |
| Model card | A model's documentation page | Mitchell et al.'s nine sections; read the licence, intended use, evaluation and `base_model` [V: MCR, HFC] | Part 12, §3.3 |
| Model Context Protocol (MCP) | A shared way for AI apps to reach tools and data | Newest revision 2026-07-28; Agentic AI Foundation since December 9, 2025 [V: MGT, AAF]. | Part 07, §1 |
| Model FLOP utilization (MFU) | The share of a chip's peak compute doing useful model work | Megatron-LM reports 41% to 48% on H100s, by its own measure [V: MEG]. | Part 11, §3.10 |
| Model routing | Sending easy requests to a cheaper model | RouteLLM reports over 2 times lower cost on its benchmarks, measured on particular model pairs [V: RTL]. | Part 13, §2 |
| Model-graded eval; "LLM-as-a-judge" | A model used as the grader | It can compare two answers, score one, or score one against a reference [V: OBP]. | Part 02, §2 |
| Modularity | A score for how much more a split's communities connect inside than chance would give | Q = Σ [L_c / m − (d_c / 2m)²] [T]. | Part 06, §3.3 |
| MS MARCO | A large public set of web questions and judged passages, from Microsoft | Results are often reported on its "dev" set and a held-out "eval" set. | Part 05, §2 |
| Multi round-trip request (MRTR); `input_required` | The server asking for more information and the client asking again with the answers | Replaces server-to-client requests; `requestState` must be integrity-protected [V: MRT]. | Part 07, §3.6 |
| Multi-hop question | A question whose answer needs several facts joined | Where graphs helped most in the studies read [V: HAN]. | Part 06, §1 |
| Mutation check | Breaking the code on purpose to prove a test notices | Every lab in the series ships one. | Part 01; Part 03, §2 |
| MXFP4 | A 4-bit floating-point format in which 32 values share one 8-bit power-of-two scale | 4.25 bits per weight; an Open Compute Project format; gpt-oss stores its experts in it [V: MXS, GOS]. | Part 11, §3.3 |
| Namespaces; cgroups | Linux features that give a process its own view, and limits on what it can use | What Docker sets up for each container [V: DSE]. | Part 08, §3.7 |
| Nats and bits | Units of entropy | Natural logarithm and base 2; 1 nat = 1.443 bits [T]. | Part 02, §2 |
| nDCG@k (normalized discounted cumulative gain) | A ranking score that rewards right results near the top and allows graded relevance | Two gain versions (the grade, or 2^grade - 1) give different numbers on graded labels; say which [V: TRE, IRM, RNX]. | Part 05, §3.8 |
| Needle in a haystack (NIAH); needle | A test that hides one fact (the needle) in a long input and asks for it | The simplest long-context test; it can overstate what a model can do [V: RUL, HEL]. | Part 04, §3.4 |
| Node; edge | A thing in a graph; a link between two things | Also vertex; relationship. | Part 06, §2 |
| Node.js; npm is its package installer | The program that runs JavaScript outside a browser | Some tools in later parts are npm packages. | Part 01, §2 |
| Nondeterminism | Different outputs from the same input | Even at temperature 0 [V: ANT, TML]. | Part 02, §2 |
| OAuth 2.1 (in MCP) | The standard way MCP servers check who is calling over HTTP | Still an IETF draft; not used for stdio [V: MAU]. | Part 07, §3.7 |
| Open Source AI Definition | OSI's 2024 standard for calling an AI system open source | Asks for data information, code and parameters [V: OSD]. | Part 10, §3.10 |
| Open-weight model | A model whose weights you can download and run yourself | Not the same as open source (Part 10); the licence varies by model, even within one family [V: MUS] | Part 12, §3.4 |
| OpenTelemetry Collector | A program that receives, filters and forwards telemetry | Can delete attributes, such as prompt text, before storage [V: OTS]. | Part 13, §2 |
| Orchestrator-workers | One model splits the work and hands parts to others | For tasks whose subtasks can't be predicted [V: BEA]. | Part 09, §2 |
| OTLP | The wire protocol for traces, metrics and logs | Ports 4317 (gRPC) and 4318 (HTTP); over a network, use TLS [V: OTS]. | Part 13, §2 |
| Overfitting | Doing well on the examples you tuned on, worse on new ones | Prompt optimizers overfit small training sets [V: DSD]. | Part 03, §3.7 |
| Overflow; truncation | What happens when a request is too big for the window | An error at Anthropic and by default at OpenAI; dropped messages, without an error, in Ollama's chat [V: ACW, OTR, OLS]. | Part 04, §3.3 |
| Package | Reusable code someone else published | PyPI, the Python Package Index, is the official public collection for Python. | Part 01, §2 |
| PagedAttention | Storing the KV cache in small fixed blocks placed anywhere in memory | vLLM; waste is limited to each request's last block [V: VLL]. | Part 11, §3.4 |
| Paired comparison | Comparing two versions case by case on the same test set | [V: MIL] | Part 02, §2 |
| Parallelization (sectioning, voting) | Running independent parts at once, or the same task several times | [V: BEA]. | Part 09, §2 |
| Parser differential | Two programs reading the same URL or text differently | Python and browsers disagree on a backslash in a URL, which can bypass an allowlist [V: WHW][T]. | Part 10, §3.5 |
| pass@k | The chance that at least one of k tries passes | Used for code; unbiased formula from Chen et al. [V: CHE]. | Part 02, §2 |
| pass^k | Success on every one of k tries of the same task | A reliability measure from τ-bench [V: TAU]. | Part 08, §3.6 |
| PATH, an environment variable | The list of folders searched when you type a command's name | Windows separates the folders with `;`, macOS and Linux with `:` [V: PSE]. | Part 01, §2 |
| Path traversal | Escaping a folder with `..` in a file path | Anthropic's memory-tool docs require validating every path [V: AMT]. | Part 06, §3.10 |
| PEFT (parameter-efficient fine-tuning) | Training a small add-on instead of the model's weights | Also the name of Hugging Face's library for it [V: PFT] | Part 12, §2 |
| Pending writes | Results of steps that already finished, kept when a sibling step fails | So they don't run again on resume; not a cache [V: LGD]. | Part 09, §3.3 |
| Pinning | Asking for one exact version | `packaging==26.3`. | Part 01, §2 |
| Pinning (tool definitions) | Fixing a tool's definition at approval time to detect later changes | The lab's `guard.pin_tools` [T]. | Part 07, §3.11 |
| pip | The tool that downloads and installs Python packages | Run it as `python -m pip`, so it belongs to the Python you mean [T]. | Part 01, §2 |
| Position bias | A judge favouring an answer for where it appears | [V: ZHE] | Part 02, §2 |
| Position effect; "lost in the middle" | A model using facts at the start and end of a long input better than facts in the middle | A U-shaped curve in 2023 models [V: LIU]; weaker and task-dependent since [V: NOL, CHR]. Not the same as a judge's position bias (Part 02). | Part 04, §3.4 |
| Precision | Of the items labelled X, the share that really are X | tp / (tp + fp) [V: SKM]. | Part 02, §2 |
| Precision@k | The share of the top k results that are relevant | Divides by k even if fewer came back [V: IRM]. | Part 05, §3.8 |
| Preemption; retraction | Pausing a request when KV memory runs out, to redo it later | vLLM 0.31.0 recomputes (CPU swapping removed); SGLang calls it retraction [V: VSR, SGS]. | Part 11, §3.4 |
| Prefill | Reading the prompt, many tokens at once | Limited by compute; at least 2 x weights x tokens / peak operations per second [V: VLL, NVI][T]. | Part 11, §3.1 |
| Prefix | The start of a prompt that repeats exactly across requests | Any change in it means everything after the change is processed again [V: APC]. | Part 04, §2 |
| Progressive disclosure (skills) | Loading only skill names first, full text when needed | About 100 tokens per skill up front [V: ASK]. | Part 07, §3.10 |
| Prompt caching; prefix caching | Reusing the processed start of a prompt in a later request | Cheaper and faster prompt processing; no effect on the answer [V: APC, OPC, GCC]. | Part 04, §3.5 |
| Prompt chaining | A chain of model calls, each using the last one's output | [V: BEA]. | Part 09, §2 |
| Prompt injection; direct prompt injection | Instructions smuggled into a model's input; injection typed by the user | OWASP LLM01:2026: no reliable prevention exists today [V: OW6]. | Part 10, §1 |
| Prompt optimizer | A program that searches for a better prompt against a metric | DSPy's optimizers were formerly called "teleprompters" [V: DSD]. | Part 03, §2 |
| Property graph | A graph whose nodes and edges carry key-value details | Neo4j's model [V: NPG]. | Part 06, §3.1 |
| Pseudonymization | Replacing personal data with a placeholder only a key holder can link back | Still personal data to whoever holds the key [I]. | Part 10, §3.8 |
| p-value; mid-p | How surprising a result would be if the versions really didn't differ | The labs treat a value below 0.05 as evidence; the mid-p is a less conservative version [V: FLL]. | Part 02, §2 |
| Python interpreter | The program that runs Python code | `python` on Windows and inside an active virtual environment; often `python3` on macOS and Linux. | Part 01, §2 |
| Q4_K_M; K-quant mixture | llama.cpp's "4-bit" type, which gives some tensors more bits | Q6_K for two matrices on 16 of Llama 3 8B's 32 layers and for the output matrix: 4.89 bits per weight [V: LCP][T]. | Part 11, §3.3 |
| QLoRA | LoRA on a frozen model stored in 4 bits | NF4 and double quantization; a 65B model on one 48 GB GPU (NeurIPS 2023) [V: QLR] | Part 12, §3.7 |
| Quantization | Storing weights in fewer bits | A smaller file and faster generation, at a measurable quality cost [V: LCP]. | Part 11, §3.3 |
| Rank (r, LoRA) | The width of LoRA's thin matrices | A setting to test; PEFT's default is 8 [V: PFT] | Part 12, §3.7 |
| Recall | Of the items that really are X, the share labelled X | tp / (tp + fn) [V: SKM]. | Part 02, §2 |
| Recall@k | The share of all relevant chunks that appear in the top k | Not the same as Success@k [V: IRM]. | Part 05, §3.8 |
| Reciprocal rank fusion (RRF) | Merging ranked lists by 1 / (k + rank), using positions only | k = 60 with ranks from 1 in Cormack et al. and Elasticsearch; tools that count from 0 shift what k means [V: COR, ESR, QDH]. | Part 05, §3.4 |
| Reciprocal rank; mean reciprocal rank (MRR) | 1 divided by the rank of the first right result; its average over questions | [V: IRM] | Part 05, §3.8 |
| Recursion limit; step limit | A cap on steps before a run is stopped | LangGraph 1.2.15's default is 10,007 in code; its docs say 1,000 [V: LGS, LGD][T]. | Part 09, §2 |
| Redaction | Replacing personal data with a placeholder | Pattern rules find shapes, not names [T]. | Part 10, §3.8 |
| Refusal | The model declining a request, for example for safety reasons | Its reply may not follow your schema [V: ASO, OSO]. | Part 03, §2 |
| Regression | A change that makes results worse |  | Part 02, §2 |
| Relevance judgments; qrels | Questions with their known right chunks, often graded | The test data for retrieval. | Part 05, §3.8 |
| Requirements file | A file listing the packages a project needs | Usually `requirements.txt`. | Part 01, §2 |
| Reranking; retrieve-then-rerank | Re-sorting the top results with a better, slower model | Typically the top 50 to 100 [V: SBR]. | Part 05, §3.5 |
| Response buffering | A proxy holding a response back before passing it on | On by default in nginx (`proxy_buffering on`); `X-Accel-Buffering: no` turns it off for one response [V: NGX][T]. | Part 13, §2 |
| Retrieval-augmented generation (RAG) | Finding passages, then having the model answer from them | Reduces wrong answers but doesn't end them [V: LEW, MAG]. | Part 05, §1 |
| Ridge point; roofline model | The operations per byte at which compute and memory limit equally | Peak operations / bandwidth; H100 BF16 dense: 295 per byte [V: RFL][T]. | Part 11, §3.1 |
| Rollout; trial | One run of the program on one example, during a search | The GEPA paper counts rollouts [V: GEP]. | Part 03, §2 |
| Routing | Sending each input to the step or model that suits it | Easy questions to "smaller, cost-efficient models" [V: BEA]. | Part 09, §2 |
| Rug pull | A tool's definition changing after the user approved it | Invariant Labs' term [V: INV]. | Part 07, §3.11 |
| Safety classifier; guard model | A small model that labels text safe or unsafe | Llama Guard 4, Prompt Guard 2; error rates on every set measured [V: LG4, PG2]. | Part 10, §3.7 |
| Sampling; roots | The server asking the client's model to write; the client listing its folders | Both deprecated in MCP 2026-07-28 [V: MDP]. | Part 07, §3.3 |
| Sandbox | An isolated environment for running untrusted code | Reduces risk; guarantees nothing. | Part 08, §1 |
| Saturation | A benchmark most models now ace | It can no longer separate them; operators retire or refresh such tests [V: LVB, OLL] | Part 12, §3.2 |
| SDK (software development kit) | A kit of code for building on a protocol or service |  | Part 07, §2 |
| seccomp profile | A filter on which kernel calls a process may make | Docker's default blocks about 44 of 300+ [V: DSC]. | Part 08, §3.7 |
| Self-preference, or self-enhancement, bias | A judge favouring its own answers | [V: PAN, ZHE] | Part 02, §2 |
| Semantic caching | Reusing a stored answer for a question that looks similar | Microsoft: it "can surface responses that are incorrect, outdated, or unsafe"; keep caches per user [V: AZS]. | Part 13, §2 |
| Semantic entropy | How spread out a model's answers are in meaning | Sample answers, group them by meaning, take the entropy over the groups [V: FAR]. | Part 02, §3.7 |
| Server-Sent Events (SSE); `text/event-stream` | One long HTTP response made of small text events | WHATWG HTML 9.2; how the big vendors stream (Gemini with `alt=sse`) [V: WSS, AND, OAD, GMD]. | Part 13, §2 |
| `server/discover` | An MCP request asking what a server supports | Servers MUST implement it [V: MDI]. | Part 07, §3.3 |
| Signal; update (Temporal) | A message sent to a running workflow, without or with a reply | The durable way to deliver a person's answer [V: TDC]. | Part 09, §3.6 |
| Signature (DSPy) | A typed description of a task's inputs and outputs | [V: DSD] | Part 03, §2 |
| Sleep-time compute; "dreaming" | Memory work done in the background rather than during the reply | Letta's term for it now is "dreaming" [V: LTC]. | Part 06, §3.6 |
| Sliding window (attention) | Attention that looks back only a fixed number of tokens | gpt-oss: 128 tokens on alternate layers, which caps those layers' KV cache [V: GOS][T]. | Part 11, §3.2 |
| Source-available licence | Code you can read but not use freely | This series' label for Elastic-2.0, SSPL-1.0 and BUSL-1.1, which SPDX marks as not OSI-approved [V: SPX]. | Part 10, §3.10 |
| Span | One timed step inside a trace | Has a name, attributes, events and a status [V: OTS]. | Part 13, §2 |
| SPDX identifier | A standard short name for a licence | From the SPDX License List (3.29.0, September 2026) [V: SPX]. | Part 10, §3.10 |
| Speculative decoding | A small model guessing tokens the big one checks in one pass | Output distribution unchanged; helps at low load and can slow high load [V: LEV, VBL]. | Part 11, §3.5 |
| Spotlighting | Marking untrusted text so the model can tell where it came from | Adaptive attacks got through it 99% of the time on three of four targets [V: SPT, NAS]. | Part 10, §3.4 |
| Standard output (stdout); standard error (stderr) | A program's normal output and its separate channel for messages and errors | An MCP stdio server may write only protocol messages to stdout [V: MST]. | Part 07, §3.5 |
| Stand-in model | A fake model that returns recorded replies | How the labs test code without a model or key. | Part 03, §2 |
| State graph | A graph whose steps read and write shared state and may loop back | LangGraph's model [V: LGD]. | Part 09, §2 |
| Static breakpoint | A run paused at a fixed step, for debugging | "not recommended for human-in-the-loop" [V: LGD]. | Part 09, §2 |
| stdio transport | Talking to an MCP server started as a child program, through its input and output | One JSON message per line [V: MST]. | Part 07, §3.5 |
| Stemming | Reducing words to a shared stem ("draining" to "drain") so keyword search matches them | Fixes some vocabulary mismatches; can merge words wrongly [T]. | Part 05, §3.1 |
| Stop reason (`stop_reason`) | Why the model stopped this time | Seven values in Anthropic's API; handle all of them [V: STOP]. | Part 08, §3.1 |
| Streamable HTTP | Talking to an MCP server over the web | Each message an HTTP POST; validate `Origin` [V: MSH]. | Part 07, §3.5 |
| Strict tool use; strict mode | A setting that makes the model follow a tool's input schema exactly | `"strict": true` on the tool [V: ASO, OFC]. | Part 03, §2 |
| Structured sparsity | Zeros in a fixed pattern the chip can skip | Doubles a datasheet's TFLOPS figure; NVIDIA: "Dense is ½ sparse spec shown" [V: NVB, HGX]. | Part 11, §3.9 |
| `structuredContent`; `outputSchema` | A tool's result data in a fixed shape; the schema it must follow | Any JSON value since 2026-07-28 [V: MTO]. | Part 07, §3.4 |
| Subagent | A worker agent with its own context window | A Claude subagent gets only the prompt string and returns only its final message [V: CSA]. | Part 09, §2 |
| Success@k | Whether any relevant chunk is in the top k | Often mislabelled "recall@k" [V: IRM]. | Part 05, §3.8 |
| Super-step | One round of running the graph's ready nodes | Parallel nodes share one; LangGraph checkpoints between them [V: LGD]. | Part 09, §3.3 |
| Telemetry | Usage data a tool sends to its maker | On by default in promptfoo, DeepEval, Ragas and Phoenix [V: PFY, DEV, RAG, PHX]; vLLM's usage statistics too (Part 11, §3.7). | Part 02, §2 |
| Terminal; the shell runs inside it | The window where you type commands | On Windows, PowerShell; on macOS, the Terminal app; on Linux, usually a terminal running bash. | Part 01, §2 |
| Test case; test set | One input with the right answer or grading guidance; a set of them | [V: INS] | Part 02, §2 |
| Thinking; reasoning tokens | Hidden working-out a model writes before its answer | Billed as output even when hidden [V: ATK, ORS]. | Part 03, §2 |
| Thread | One conversation or job, with its own checkpoints | Identified by a `thread_id` [V: LGD]. | Part 09, §2 |
| Time to live (TTL); lifetime | How long a cached prefix stays usable | 5 minutes or 1 hour at Anthropic, refreshed on each hit; at least 30 minutes at OpenAI's newest models [V: APC, OPC]. | Part 04, §2 |
| Timing side channel | Learning something from how long a reply takes | How caches shared between users were detected [V: GUA]. | Part 04, §3.8 |
| Token | The piece of text a model reads as one unit, often part of a word | About 4 characters of English by OpenAI's and Google's rules of thumb [V: OTK, GTK]. | Part 04, §2 |
| Tokenizer; encoding | The program that splits text into tokens | Differs between vendors and model generations; Claude Opus 4.7 and later give about 30% more tokens for the same text [V: ATC]. | Part 04, §3.1 |
| Tool annotations | Hints about what an MCP tool does, such as read-only | Untrusted unless the server is trusted [V: MTO]. | Part 07, §3.4 |
| Tool call; function call | The model asking your program to run a function | The model asks; your program decides and acts [V: ATD, OFC]. | Part 03, §2 |
| Tool choice | A setting that says whether, and which, tool the model must call | Forcing a tool returns a 400 error on Claude's newest models [V: ATD]. | Part 03, §3.3 |
| Tool definition | The description of one tool the model may call | Name, description and an input schema [V: ATD, OFC]. | Part 03, §2 |
| Tool error result (`is_error`) | A failed tool call reported back to the model | Short and actionable; never raw exception text, which can hold secrets [V: HTC, WTA][T]. | Part 08, §3.2 |
| Tool execution error (`isError: true`) | A failure inside a tool, reported so the model can try again | Not a protocol error; includes bad input [V: MTO]. | Part 07, §3.4 |
| Tool poisoning | Hidden instructions placed in a tool's description | Invariant Labs' term [V: INV]. | Part 07, §3.11 |
| Tool result | What your program sends back after running a tool | Anthropic's `tool_result`, with `is_error` for failures [V: AHT]. | Part 03, §2 |
| Tools; resources; prompts (MCP) | Functions the model may call; data the app may read; templates the user picks | Model-, application- and user-controlled [V: MSP]. | Part 07, §3.2 |
| Trace | A timeline of one request, made of spans | Spans in different services join through `traceparent` [V: OTS, W3C]. | Part 13, §2 |
| `traceparent` (W3C Trace Context) | The header that joins spans across services | `version-traceid-parentid-flags`; don't trust one from outside your own services [V: W3C, OTS]. | Part 13, §2 |
| Triple; RDF | A fact written as subject, predicate, object; the W3C's Resource Description Framework | "An RDF graph is a set of RDF triples" [V: RDF]. | Part 06, §3.1 |
| TTFT; TPOT; ITL | Time to first token; time per output token after the first; the gap between streamed chunks | Define them by formula: NVIDIA's AIPerf calls vLLM's TPOT "ITL" [V: VSR, APF]. | Part 11, §3.6 |
| Turn; turn cap; budget | One model call plus its tools; limits on turns, tokens or money | SDK defaults differ: 10 turns (OpenAI), none (Claude) [V: OAS, SDL]. | Part 08, §3.3 |
| Upsert | A write that creates a record or updates it if it exists | Doing it twice leaves one record [V: LGD]. | Part 09, §3.3 |
| Valid time (`valid_at`, `invalid_at`) | When a fact became true and when it stopped | How Graphiti handles a changed fact [V: GRA]. | Part 06, §3.8 |
| Validation | Checking data against a schema in your own code | Pydantic and jsonschema [V: PYD, JSL]. | Part 03, §2 |
| Vector store; vector database | A library, database or service built to store and search vectors | Six kinds, from a library (FAISS) to a managed service (Pinecone). | Part 05, §3.3 |
| Verbosity bias | A judge favouring an answer for being longer | [V: ZHE, OBP] | Part 02, §2 |
| Virtual environment ("venv") | A private package space for one project | A folder, here `.venv`, with its own `python` and packages. It isn't committed to Git or moved; you recreate it instead [V: VNV]. | Part 01, §2 |
| Visibility timeout | How long a queue waits before handing an unacknowledged task to another worker | One hour on Celery's Redis broker [V: CEL]. | Part 09, §3.5 |
| Vocabulary mismatch | A question and its answer using different words for the same thing | Why keyword search misses synonyms [T]. | Part 05, §3.1 |
| WebSocket | A two-way connection that stays open | RFC 6455; OpenAI's Realtime API uses it on servers [V: RFC, OAD]. | Part 13, §2 |
| Weights; parameters | The model's learned numbers | Llama 3 8B has 8,030,261,248 [T]. | Part 11, §2 |
| WinGet, the Windows Package Manager | Windows' command-line app installer | Windows 10 version 1809 or later, and Windows 11 [V: WGT]. | Part 01, §2 |
| Workflow | A fixed sequence of model calls written in code | Part 09 [V: BEA]. | Part 08, §1 |
| WSL, the Windows Subsystem for Linux | Linux running inside Windows | Lets Windows run a Linux distribution and its programs [V: WSL]. This series needs it only for the sandbox labs in Part 08. | Part 01, §2 |
| Zero data retention (ZDR) | An agreement that a provider keeps no copy of your data | The Claude API's MCP connector isn't covered [V: CMC]. | Part 07, §3.8 |
| Zero-shot; out of domain | Tested on data unlike anything the model was trained on | The opposite is in domain. | Part 05, §2 |
