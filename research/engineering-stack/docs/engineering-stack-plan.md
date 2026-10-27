# Engineering Stack Plan

*Phase 2 of claude/engineering-stack-prompt.md, October 9, 2026. It builds on claude/engineering-stack-claim-ledger.md (Phase 1) and claude/engineering-stack-freshness-ledger.md. Status: proposed; Phase 3 waits for the owner's go. Evidence class: project plan. Factual statements carry the ledger's tags and source keys; everything else is a design choice, given with its reason.*

## 1. Decisions in brief

1. **A new paper, not a continuation.** Neither claude/project-file-map.md nor claude/handoff-2026-10-08.md numbers a paper series, so this starts a new one: *The AI Engineering Stack*, in 13 parts plus front matter and appendices. Files: claude/engineering-stack-part-NN-topic.md.
2. **Teach from the ledger, not from Gemini.** Each part starts from the corrected ledger rows and adds what the Gemini paper left out. Its twelve "pillars" become plain topic names. Four of its "X engineering" labels mean something else in current use or aren't established (agent, harness, orchestration, platform), and two weren't found in use or weren't checked (retrieval; rack and infrastructure) (ledger §6).
3. **No taxonomy-style axes.** None of the six candidate axes places every topic (Section 5). The paper uses a two-part map instead: seven layers that a request passes through, and five concerns that run through every layer.
4. **Measure first.** Evals come right after setup, so every later part can test its claims and labs against something.
5. **Link, don't repeat.** Prompting technique stays in the taxonomy (3e) and the guide (2e); Agent Skills stay in the skills reference and the booklet. Parts link to them by section.

## 2. Overlaps: what merges

| Gemini sections | The overlap | Decision | Parts |
|---|---|---|---|
| Context (P2), memory (P3), retrieval (P5), knowledge mapping (B3) | All four decide what goes into the model's context window and where it comes from. P2 also mixes in KV-cache internals that belong to serving (P2-04). | One context family in three parts: what fits and where (04), finding it (05), structured and remembered knowledge (06). KV-cache internals move to Running models. | 04, 05, 06, 11 |
| Harness (P7) and eval (P9) | Gemini's "harness" is test scaffolding plus sandboxes; the current meaning is an agent's working environment (P7-01). | Test scaffolding joins evals. Sandboxing joins agents. "Harness" is taught in its current meaning. | 02, 08 |
| Agents (P6), orchestration (P8), multi-agent (B1) | One family: a loop that calls tools, fixed workflows around it, and several agents working together. | Split by what the reader builds: one agent and its environment; then workflows, frameworks, several agents and human approval. | 08, 09 |
| Security (P12), guardrails (B2), the privacy half of local models (B4) | All are about what must not happen and how to check it. | One part with a security reviewer. HIPAA and licences join it, with not-legal-advice notes. | 10 |
| Rack and infrastructure (P4), inference (P10), the runtime half of B4 | All are about running a model: hardware, serving software, local runtimes. | One part, Running models. Datacenter rack detail shrinks to reading a datasheet, since most readers will rent hardware or use hosted models. | 11 |
| Platform (P11) | It describes an AI product's API layer, not platform engineering (P11-01). | Joins observability and cost in Shipping and operating. | 13 |
| Prompt engineering (P1) | Covered in depth by the taxonomy and the guide. | A short part on prompts as software interfaces: structured outputs, tool schemas, reasoning models and prompt optimization, linking the taxonomy for technique. | 03 |

## 3. Gaps: what to add

Each candidate gap from the prompt was checked against the Gemini paper and against a source, not assumed.

| Candidate | In Gemini? | Evidence it matters | Decision | Parts |
|---|---|---|---|---|
| Model Context Protocol (MCP) and other agent protocols | No | A versioned specification, latest revision 2026-07-28, with SDKs on npm (@modelcontextprotocol/sdk 1.32.1) and PyPI (mcp 2.3.0) [V] (MCP, NPM, PYPI). Other protocols, such as Agent2Agent, not checked yet [U]. | Add | 07 |
| Agent Skills | No | The project's own references: claude/agent-skills-reference-v1-2.md and claude/skills-booklet.md | Add a short section that links them | 07 |
| Fine-tuning, and fine-tune versus prompt versus retrieve | No | Not researched yet [U]; the LoRA and QLoRA papers and the vendors' fine-tuning docs would settle it | Add | 12 |
| Observability and tracing | No | Maintained tools exist (arize-phoenix 20.20.0, Elastic License 2.0) [V] (PYPI); OpenTelemetry's conventions for generative AI not opened yet [U] | Add | 13 |
| Cost and latency: prompt caching, batch processing, routing | Partly (routing, P8-02) | Anthropic prices cache reads at 0.1x of base input, lower on some newest models [V] (APC); routing easy queries to smaller models is a documented pattern [V] (BEA); batch APIs not opened yet [U] | Add: caching in 04, routing in 09, batching and budgets in 13 | 04, 09, 13 |
| Reasoning models and how they change prompting | No | Covered in the taxonomy 3e: Phase 6 of its history, Chapter 10 on inference compute, and its chain-of-thought protocol for reasoning models | Add a short section that links the taxonomy | 03 |
| Structured outputs and tool calling | Partly (P1-15, P6-02) | Both vendors' official docs [V] (OSO, OFC, ATU); taxonomy §10.5 and guide §18 | Add, centred on the API contract | 03 |
| Building evaluation data | No | Not researched yet [U] | Add | 02 |
| Multimodal and computer-use agents | No | Not researched yet [U] | Computer use joins agents, because it needs a sandbox; multimodal retrieval gets a section in 05, not a part of its own | 08, 05 |
| Data governance and licensing | Barely (B4) | Model licences differ in ways that matter: Llama 3's conditions against gpt-oss's Apache 2.0 [V] (L3L, OSS); an "open" tool may be source-available, as Phoenix is [V] (PYPI) | Add | 10, 12 |
| Human-in-the-loop design | Partly (B1-07) | LangGraph's interrupt() and CrewAI's @human_feedback [V] (LGD, CRD); OWASP advises human approval for high-risk actions [V] (OW5) | Add | 09 |

## 4. What shrinks or goes

- **Datacenter racks** (P4) shrink to one section on reading a GPU datasheet and doing the memory arithmetic. Multi-node NVLink, NVSwitch and rack power suit a datacenter team, not a solo builder on an ordinary computer.
- **"X engineering" headings** go. Memory engineering is an emerging term, retrieval engineering wasn't found in use, orchestration engineering isn't established, and Gemini's "platform" and "harness" engineering mean something else in current use (ledger §6).
- **Gemini's invented examples** (the refund agent, the M&A analysis and the rest) are replaced with real, sourced examples and one fully worked example per topic.
- **Retired tools** (the Assistants API, LangServe, AutoGen as a new choice, gpt-4 as a judge) appear only in "what changed" notes, each with its replacement.
- **Rhetoric** ("deterministic", "definitive", "zero-latency" and the like) goes; ledger §8 says what replaces each.

## 5. The axes test

**The rule.** Keep an axis only if every topic places on it cleanly: one value, without "it depends". The test uses the 30 topics of the part plan, listed before any structure was chosen.

**Candidate axes and their values.**
- *Layer:* where the topic's defining component sits on the path of a request: delivery, control, integration, context, model, runtime, compute.
- *What it changes:* the input (context), the model (weights), control flow, serving, the environment, or nothing (measurement).
- *Hardware needed:* none (hosted), a laptop, a consumer GPU, a datacenter GPU.
- *Cost:* free, or one fixed cost level.
- *Maturity:* standard, established, emerging, research.
- *Risk:* low, medium or high harm if it fails.

**Why a cell fails (✗).** *path:* it depends on the path the reader takes (hosted, laptop or cloud). *mix:* it varies within the topic. *two:* two values apply. *use:* it depends on how the thing is deployed. *cuts across:* it applies to every layer. *none:* no value fits. An asterisk marks a placement made by a tie-break rule (below).

| ID | Topic | Part | Layer | What it changes | Hardware | Cost | Maturity | Risk |
|---|---|---|---|---|---|---|---|---|
| T01 | Evals, test data and judges | 02 | ✗ cuts across | measurement | ✗ path | ✗ path | ✗ mix | ✗ use |
| T02 | Structured outputs and tool calling | 03 | Integration | ✗ two | ✗ path | ✗ path | established | ✗ use |
| T03 | Reasoning models | 03 | Model | model | ✗ path | ✗ path | established | ✗ use |
| T04 | Prompt optimization (DSPy) | 03 | Context | input | ✗ path | ✗ path | emerging | ✗ use |
| T05 | Context budget and placement | 04 | Context | input | ✗ path | ✗ path | ✗ mix | ✗ use |
| T06 | Provider prompt caching | 04 | Runtime* | serving | none | ✗ path | established | ✗ use |
| T07 | Retrieval: hybrid search, fusion, reranking | 05 | Context | input | ✗ path | ✗ path | ✗ mix | ✗ use |
| T08 | GraphRAG and knowledge graphs | 06 | Context | input | ✗ path | ✗ path | emerging | ✗ use |
| T09 | Agent memory | 06 | Context | input | ✗ path | ✗ path | emerging | ✗ use |
| T10 | MCP and other agent protocols | 07 | Integration | ✗ two | ✗ path | ✗ path | ✗ mix | ✗ use |
| T11 | Agent Skills | 07 | Integration* | ✗ two | none | free | emerging | ✗ use |
| T12 | The agent loop | 08 | Control | control flow | ✗ path | ✗ path | established | ✗ use |
| T13 | Harness: the agent's working environment | 08 | Control* | environment | ✗ path | ✗ path | emerging | ✗ use |
| T14 | Sandboxing | 08 | Integration | environment | laptop | ✗ path | established | ✗ use |
| T15 | Computer use | 08 | Integration | ✗ two | ✗ path | ✗ path | emerging | ✗ use |
| T16 | Workflows and durable execution | 09 | Control | control flow | laptop | ✗ path | established | ✗ use |
| T17 | Multi-agent systems and frameworks | 09 | Control | control flow | ✗ path | ✗ path | ✗ mix | ✗ use |
| T18 | Human-in-the-loop | 09 | Control | control flow | none | ✗ use | established | ✗ use |
| T19 | Prompt injection and excessive agency | 10 | ✗ cuts across | ✗ mix | none | free | ✗ mix | ✗ use |
| T20 | Guardrails and safety classifiers | 10 | Control* | ✗ two | ✗ path | ✗ path | ✗ mix | ✗ use |
| T21 | Privacy and compliance | 10 | ✗ cuts across | ✗ mix | none | ✗ use | ✗ mix | ✗ use |
| T22 | Licences and data governance | 10 | ✗ cuts across | ✗ none | none | ✗ mix | ✗ mix | ✗ use |
| T23 | Serving engines | 11 | Runtime | serving | ✗ path | ✗ path | established | ✗ use |
| T24 | Local models and quantization | 11 | Runtime* | ✗ two | ✗ path | ✗ path | established | ✗ use |
| T25 | Hardware | 11 | Compute | ✗ none | ✗ none | ✗ path | established | ✗ use |
| T26 | Choosing a model | 12 | Model | model | ✗ path | ✗ path | ✗ mix | ✗ use |
| T27 | Fine-tuning | 12 | Model | model | ✗ path | ✗ path | established | ✗ use |
| T28 | APIs and streaming | 13 | Delivery | serving | laptop | ✗ path | established | ✗ use |
| T29 | Observability and tracing | 13 | ✗ cuts across | measurement | ✗ path | ✗ path | ✗ mix | ✗ use |
| T30 | Cost and latency | 13 | ✗ cuts across | ✗ mix | ✗ path | ✗ path | ✗ mix | ✗ use |
| | **Topics placed cleanly** | | **24 of 30** | **19 of 30** | **9 of 30** | **2 of 30** | **18 of 30** | **0 of 30** |

The table and its counts were generated by a script from the placements, so the counts match the cells [T].

**Result: no axis places all 30 topics.**
- *Risk* fails everywhere. The same agent loop is low-risk with read-only tools and high-risk with a payments tool; OWASP calls the second case excessive agency (OW5).
- *Cost* and *hardware* fail because most topics can be done hosted, on a laptop or in the cloud. They become the three paths per topic (Section 6) and the cost and hardware columns of each part's tool table.
- *Maturity* varies inside topics (BM25 is decades old; late interaction is recent), so it moves to the tool tables as maintenance status, version and date.
- *What it changes* fails for the interface topics, where two values apply.
- *Layer* comes closest: 24 of 30 topics place, 5 of them only through a tie-break rule. It fails for the 6 topics that apply to every layer.

**The structure used instead: layers and concerns.** Think of a building. The floors are layers, and the plumbing and wiring that run through every floor are concerns. Every topic gets exactly one home.

*Seven layers*, in the order a request meets them:

| Layer | What it is | Topics |
|---|---|---|
| Delivery | How people and programs reach the system | T28 |
| Control | What decides the next step | T12, T13*, T16, T17, T18, T20* |
| Integration | How the model reaches tools and other systems | T02, T10, T11*, T14, T15 |
| Context | What goes into the context window | T04, T05, T07, T08, T09 |
| Model | Which weights do the work | T03, T26, T27 |
| Runtime | The software that runs the model | T06*, T23, T24* |
| Compute | The hardware under it | T25 |

*Five concerns*, each with its own topic and part, and linked from every layer part: Evaluate (T01, Part 02), Secure (T19, Part 10), Govern (T21 and T22, Part 10), Observe (T29, Part 13), Economize (T30, Part 13).

**Tie-break rules (the five asterisks).**
1. A topic goes to the layer of the component it defines, not where the reader acts. Prompt caching (T06) is a cache kept where the model runs, though the reader's lever is prompt order, which Part 04 teaches.
2. A component that serves a concern stays in its layer, with a link from the concern's part. Guardrails (T20) sit on the request path and can reroute it; they also serve Secure.

The other three placements by these rules: Agent Skills (T11) package capabilities an agent loads, like tools, though their instructions enter the context; the harness (T13) shapes how an agent decides and checks its work, though it includes tools; local models (T24) are mainly about running a model, though quantization changes the model file. Each part states its placement, so a reader who disagrees can see why it was made.

## 6. Learning map

**Prerequisites.**

| Part | Needs | Why |
|---|---|---|
| 01 Setup | nothing | Everything else uses it |
| 02 Evals | 01 | Later parts test their labs against an eval |
| 03 Prompts as interfaces | 01, 02 | Schemas and optimizers need a metric |
| 04 Context | 03 | Builds on how a prompt is assembled |
| 05 Retrieval | 02, 04 | Retrieval fills the context and needs its own evals |
| 06 Graphs and memory | 05 | Extends retrieval |
| 07 Tools and protocols | 03 | Builds on tool calling |
| 08 Agents | 03, 07 (02 for agent evals) | An agent is a loop over tools |
| 09 Workflows and multi-agent | 08 | Composes agents |
| 10 Security, privacy and licences | 08 (05 for injection through retrieved text) | Agents and retrieval create the attack surface; the basics can be read at any time |
| 11 Running models | 01 (04 for the KV cache) | Independent of 03 to 10 |
| 12 Adapting models | 02, 05, 11 | Fine-tuning is judged by evals, weighed against retrieval, and needs a runtime |
| 13 Shipping and operating | 02, 08 or 09, 10 | What gets shipped, tested and secured |

**Recommended order:** 01 to 13 in sequence. **Two shortcuts:** *build something this week:* 01, 02, 03, 05, 08, 13. *Local first* (for privacy, or no budget for APIs): 01, 11, 02, 03, 05, 10.

**Three paths per part.** Each topic section in Phase 3 gives its own three paths; this table sets the default for each part. A hosted path may need a free account, which readers create for themselves; this work creates none (rule 9).

| Part | No install (browser or hosted) | Ordinary laptop | Cloud or production |
|---|---|---|---|
| 01 | A hosted notebook or cloud editor | Python 3.12 or 3.13, a virtual environment, Git, an editor, Node | A container image with the same pinned versions |
| 02 | Score outputs by hand in a spreadsheet | pytest plus an eval tool, against a local or hosted model | Evals in continuous integration on every change |
| 03 | A provider's console or playground | SDK calls with JSON Schema; structured output from a local model | Strict schemas, validation and retries in production |
| 04 | Token counts in a provider's console | Placement tests with a small local model | Provider prompt caching, measured on real traffic |
| 05 | A hosted vector database's free tier | BM25, embeddings and FAISS or Chroma on a CPU | A managed search or vector service |
| 06 | A hosted graph database's free tier | A local graph database or networkx; local agent memory | A managed graph database; GraphRAG indexing at scale, which pays for many LLM calls |
| 07 | Connectors in a chat app | A small MCP server, tested with MCP's inspector | A remote MCP server with authorization |
| 08 | A hosted coding agent | A raw tool loop; Docker, and gVisor on Linux | Managed sandboxes such as microVMs |
| 09 | A hosted workflow builder | LangGraph, CrewAI or Microsoft Agent Framework locally; Temporal's development server | A durable workflow service with human approval steps |
| 10 | The OWASP list and published, harmless test cases | garak against a model you own; Prompt Guard 2 on a CPU; Presidio | Guardrail services, a logging policy, review of high-risk actions |
| 11 | A hosted model playground | Ollama or llama.cpp with a 4-bit model | vLLM or SGLang on rented GPUs |
| 12 | A hosted fine-tuning service (paid) | LoRA on a small model with a consumer GPU or Apple Silicon | Rented GPUs |
| 13 | A hosted app platform | FastAPI with streaming, plus local tracing | Containers, a gateway, tracing and budgets |

**The shared setup chapter (Part 01)** covers what most parts need, so each part adds only what's new:
- Python 3.12 or 3.13. Python 3.11 to 3.13 satisfy the declared requirements of all 40 packages in the freshness ledger, and 3.14 is excluded by crewai, graphrag and nemoguardrails [T];
- virtual environments and pinned requirements;
- Git and an editor; Node's long-term-support release for the npm tools (promptfoo, MCP's inspector, Mermaid);
- Docker for the sandbox labs (optional), and WSL2 for Linux-only tools on Windows;
- API keys: kept in environment variables or a .env file that Git ignores; least-privilege keys; spending caps; never pasted into a chat;
- downloads only from official sources, checksums where published, and reading an install script before running it instead of piping it into a shell;
- the "run on your computer" convention: each part's tests run with one command from its folder.

## 7. Part plan

| Part | File (in claude/) | Topics | Ledger rows it settles | Runs here [T] / on your computer [R] | Agents |
|---|---|---|---|---|---|
| 01 | engineering-stack-part-01-setup.md | Setup and safe practice | none | [T] Python, virtual environments, pins, the test runner. [R] Windows and macOS steps, Docker | 1 researcher, tester, verifier |
| 02 | engineering-stack-part-02-evals.md | T01 | P9-01 to P9-05, P9-10, P9-12, P9-13, P7-10, P1-08 | [T] scoring, semantic entropy on a toy split, a judge harness on recorded outputs. [R] live model judges | 2 researchers, verifier, tester |
| 03 | engineering-stack-part-03-prompts-as-interfaces.md | T02, T03, T04 | P1 rows, P6-02, P9-06 to P9-08, P9-11 | [T] schema validation. [R] live structured output and DSPy runs, which need a model | 2 researchers, verifier, tester |
| 04 | engineering-stack-part-04-context.md | T05, T06 | P2 rows; taxonomy flags 3 and 4 (ledger §9) | [T] token budgets and cache-cost arithmetic. [R] placement tests and caching on a live model | 2 researchers, verifier, tester |
| 05 | engineering-stack-part-05-retrieval.md | T07 | P5 rows, P3-04, B3-01 | [T] BM25 and reciprocal rank fusion on a small corpus. [R] neural embeddings (model downloads are blocked here) | 2 researchers, verifier, tester |
| 06 | engineering-stack-part-06-graphs-and-memory.md | T08, T09 | P3 rows, B3-02 to B3-05 | [T] a small graph in networkx. [R] Neo4j, GraphRAG indexing, Letta | 2 researchers, verifier, tester |
| 07 | engineering-stack-part-07-tools-and-protocols.md | T10, T11 | P6-02 | [T] an MCP server and client over standard input and output. [R] host apps | 2 researchers, verifier, tester |
| 08 | engineering-stack-part-08-agents.md | T12 to T15 | P6 rows, P7 rows | [T] a tool loop driven by a scripted stand-in model. [R] Docker, gVisor, computer use | 3 researchers, verifier, tester, security reviewer |
| 09 | engineering-stack-part-09-workflows-and-multi-agent.md | T16 to T18 | P8 rows, B1 rows, P6-05 | [T] LangGraph graphs with checkpoints and interrupts, which need no model. [R] a Temporal server, live agents | 2 to 3 researchers, verifier, tester |
| 10 | engineering-stack-part-10-security.md | T19 to T22 | P12 rows, B2 rows, B4-01, B4-08, P10-09b | [T] policy checks in code, pattern-based redaction. [R] Presidio's model-based detection, garak and guardrail models against a model you own | 3 researchers, verifier, tester, security reviewer |
| 11 | engineering-stack-part-11-running-models.md | T23 to T25 | P4 rows, P10 rows, B4-02 to B4-07, B4-10 | [T] memory, KV-cache and speedup arithmetic. [R] Ollama, llama.cpp, vLLM on a GPU | 3 researchers, verifier, tester |
| 12 | engineering-stack-part-12-adapting-models.md | T26, T27 | P10-09b, B4-10 | [T] the decision guide's arithmetic. [R] any fine-tuning run | 2 researchers, verifier, tester |
| 13 | engineering-stack-part-13-shipping.md | T28 to T30 | P11 rows | [T] FastAPI streaming from a stand-in model, local tracing, cost arithmetic. [R] deployment | 2 researchers, verifier, tester, security reviewer |

The introduction (S0) and conclusion (C) rows feed the front matter in Phase 5. Parts 08, 10 and 11 are the largest; if one doesn't fit a session, it splits into a and b rather than being cut.

**How the agents work.** Topic researchers run in parallel, one per topic group, each capped at 40 web lookups and returning a claim table (edition protocol §9.1); topics the ledger already covers need fewer lookups. The blind verifier gets only the claims and their sources, on a different model where one is available (§9.4). The learner-tester is a fresh agent in a clean folder and virtual environment that follows each setup guide and lab literally. Every report is saved as it arrives (§9.3).

**Rough cost** (an estimate from Phase 1's experience, not a measurement): about 0.5 million tokens for Part 01, 0.8 to 1.2 million for most parts, and 1.3 to 1.6 million for Parts 08, 10 and 11; roughly 13 to 17 million for all 13 parts, plus assembly. That is about one part per usage window. Phase 1 alone, with seven researchers, ran past one window. A first batch (Parts 01 to 03) would show the real cost per part before committing to the rest.

**Project knowledge budget.** The counter read 1,238,206 of 2,000,000 (61.9%) after the Phase 1 and 2 files were saved; they added 52,725 units for about 156 KB of text, about 3 bytes per unit. If each part stays near 40,000 units (about 120 KB of Markdown, code listings included), 13 parts plus the glossary and appendices add roughly 570,000, ending near 1.81 million (about 90%). To keep that margin:
- lab code lives inside each part's text, and the runnable folders go to the owner as zip files rather than as separate project docs;
- a part over budget is split, not saved whole;
- any save that would take the counter past 1.9 million (95%) waits for the owner's say.

## 8. Open questions for the owner

1. **Go or no-go** on the scope and the 13 parts, or a first batch (01 to 03).
2. **Your computer** for the [R] tests: operating system, memory, GPU (make and memory, or none), and whether Docker or WSL2 is installed.
3. **API keys and spending.** Hosted-API labs would run on your computer with your own keys in environment variables, never in a chat. Do you want hosted-API labs at all, and with what monthly cap? Otherwise every lab defaults to local models.
4. **The taxonomy flags** (ledger §9): apply the suggested induction-heads erratum to the taxonomy now, or hold it for its next revision?
5. **The knowledge budget:** keep runnable lab folders as zip files outside the project?
6. **The checkers' raw notes** (seven files, about 380 KB): send them as a zip in the chat? They aren't in the project and will be lost when this workspace is reclaimed.

## 9. Risks

- **Scope.** Thirty topics is a lot. If time runs short, cut in this order: computer use (T15); GraphRAG beyond the basics (T08); fine-tuning beyond the decision guide (T27); hardware beyond reading a datasheet (T25).
- **Freshness.** Three of the 40 packages released new versions between two registry checks about six hours apart (freshness ledger §2). Each part re-checks its rows before it is written.
- **[R] backlog.** Many labs need your computer. Each part lists them in "Run on your computer", one command per folder, so they can be run in a batch.
- **Checker independence.** Every checker so far came from one model family. The blind verifier should use a different model where one is offered.
