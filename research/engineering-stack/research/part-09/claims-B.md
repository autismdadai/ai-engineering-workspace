# Claims to check, set B

## Sources (key, class: citation with URL)

- **AAM** (VB): Anthropic Engineering, "Claude Code auto mode", March 25, 2026. https://www.anthropic.com/engineering/claude-code-auto-mode
- **ADK** (OD): google-adk 2.12.0 wheel (PyPI), google/adk/agents
- **AFL** (OD): Apache Airflow 3.3.2: "Dags" page (https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html) and apache-airflow-core 3.3.2 wheel (utils/dag_cycle_tester.py; default retries)
- **AGN** (OD): microsoft/autogen README and git history (commits 84f21a08, October 2, 2025; 027ecf0a, April 6, 2026)
- **ANS** (OD): anthropic 1.14.0 wheel (PyPI): `_constants.py`, `_base_client.py`
- **AWC** (OD): aws-samples/aws-arch-backoff-simulator, src/backoff_simulator.py (the post's companion code)
- **BEA** (VB): Anthropic Engineering, "Building effective agents", December 19, 2024, edited since (read October 15, 2026). https://www.anthropic.com/engineering/building-effective-agents
- **CCS** (OD): Claude Code docs, "Create custom subagents". https://code.claude.com/docs/en/sub-agents
- **CEL** (OD): Celery 5.6.3 wheel and docs at tag v5.6.3 (configuration, tasks, Redis broker, canvas)
- **CG1** (VB): Yan, "Don't Build Multi-Agents", Cognition, June 12, 2025. https://cognition.com/blog/dont-build-multi-agents
- **CG2** (VB): Yan, "Multi-Agents: What's Actually Working", Cognition, April 22, 2026. https://cognition.com/blog/multi-agents-working
- **CRW** (OD): crewai 1.15.28 and crewai-core 1.15.28 wheels; crewAIInc/crewAI docs at v1.15.28 (human feedback in flows, checkpointing)
- **CSA** (OD): Claude Agent SDK docs, "Subagents in the SDK". https://code.claude.com/docs/en/agent-sdk/subagents
- **DBS** (OD): dbos 3.2.0 wheel; dbos-inc/dbos-transact-py README
- **DU** (PR): Du et al., "Improving Factuality and Reasoning in Language Models through Multiagent Debate", ICML 2024, PMLR 235. https://proceedings.mlr.press/v235/du24e.html
- **GRW** (PR): Goddard, Roudsari and Wyatt, "Automation bias: a systematic review of frequency, effect mediators, and mitigators", JAMIA 19(1):121-127, 2012 (abstract). doi:10.1136/amiajnl-2011-000089
- **ING** (OD): inngest/inngest LICENSE.md
- **LGD** (OD): LangChain docs repository (source of docs.langchain.com/oss/python/langgraph/), commit 5cd646e: graph-api, checkpointers, functional-api, interrupts, fault-tolerance, workflows-agents
- **LGS** (OD): langgraph 1.2.15 wheel (PyPI): `_internal/_config.py`, `types.py`, `errors.py`, `pregel/main.py`, `_internal/_retry.py`
- **LGSU** (OD): langgraph-supervisor 0.0.31 wheel and README
- **LGSW** (OD): langgraph-swarm 0.1.0 wheel, `handoff.py`
- **MAF** (OD): microsoft/agent-framework repository (python/CHANGELOG.md, orchestrations, `_handoff.py`) and agent-framework-core 1.22.0 wheel (`_tools.py`)
- **MAR** (VB): Hadfield et al., "How we built our multi-agent research system", Anthropic Engineering, June 13, 2025. https://www.anthropic.com/engineering/multi-agent-research-system
- **MAST** (PR): Cemri et al., "Why Do Multi-Agent LLM Systems Fail?", arXiv 2503.13657v3 (October 26, 2025); NeurIPS 2025 (spotlight poster)
- **MSL** (OD): Microsoft Learn, "Agent Framework overview". https://learn.microsoft.com/en-us/agent-framework/overview/
- **OADP** (OD): OpenAI API deprecations page, entry "2025-08-20: Assistants API". https://developers.openai.com/api/docs/deprecations
- **OAI** (OD): openai 3.31.0 wheel (PyPI): `_constants.py`, `_base_client.py`
- **OAS** (OD): openai-agents 0.24.0 and 0.23.1 wheels; openai/openai-agents-python docs (human_in_the_loop.md, handoffs.md, multi_agent.md, tools.md) at commit 17d994b
- **PINF** (PP): Lee and Tiwari, "Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems", arXiv 2410.07283v1 (October 2024)
- **PYPI** (OD): PyPI JSON API, read October 15, 2026
- **RST** (OD): restatedev/restate LICENSE and README
- **SCAL** (PP): Kim et al., "Towards a Science of Scaling Agent Systems", arXiv 2512.08296v3 (April 8, 2026)
- **SMIT** (PR): Smit et al., "Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs", ICML 2024, PMLR 235. https://proceedings.mlr.press/v235/smit24a.html
- **STR** (OD): Stripe API reference, "Idempotent requests". https://docs.stripe.com/api/idempotent_requests
- **TDC** (OD): temporalio/documentation repository (source of docs.temporal.io), commit cdc231e: glossary, workflow definition and execution, activities, retry policies, limits, message passing, timers, pricing
- **TRAN** (PP): Tran and Kiela, "Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets", arXiv 2604.02460v2 (April 11, 2026)
- **ZHNG** (PP): Zhang et al., "Stop Overvaluing Multi-Agent Debate", arXiv 2502.08788v3 (June 21, 2025)

## Claims

B001. [3.7 Several agents: what the evidence says] | Anthropic's research system, June 2025  | Claude Opus 4 leading Claude Sonnet 4 subagents, against a single Opus 4, on Anthropic's internal research evaluation | "outperformed single-agent Claude Opus 4 by 90.2%". Not equal compute: on BrowseComp, "token usage by itself explains 80% of the variance". Agents use "about 4× more tokens than chat interactions"; multi-agent systems "about 15×" | VB |  SOURCES: MAR
B002. [3.7 Several agents: what the evidence says] | Kim et al., "Towards a Science of Scaling Agent Systems"  | 260 configurations, 6 benchmarks, 5 architectures, at "identical ... computational budgets" | From "+80.8% on decomposable financial reasoning" to "-70.0% on sequential planning"; adding agents had negative returns once a single agent scored above 45% | PP |  SOURCES: SCAL
B003. [3.7 Several agents: what the evidence says] | Tran and Kiela, 2026  | Single against multi-agent on multi-hop questions at equal thinking-token budgets | The single agent matched or beat them; at 1,000 tokens, 0.418 against 0.379 (sequential) and 0.388 (debate) average accuracy, gaps of 3.9 and 3.0 percentage points | PP |  SOURCES: TRAN
B004. [3.7 Several agents: what the evidence says] | MAST, Cemri et al., NeurIPS 2025  | 1,642 traces from 7 multi-agent frameworks | 14 failure modes in 3 categories; the largest single modes were step repetition (15.7%) and a mismatch between reasoning and action (13.2%) | PR |  SOURCES: MAST
B005. [3.7 Several agents: what the evidence says] | Du et al., ICML 2024  | 3 agents, 2 rounds of debate, GPT-3.5 | Arithmetic 67.0 (single) and 75.0 (majority vote of 6, equal call count) against 81.8 (debate) | PR |  SOURCES: DU
B006. [3.7 Several agents: what the evidence says] | Smit et al., ICML 2024  | Debate protocols against self-consistency and ensembles, GPT-3.5, medical and reasoning sets | Debate does "not reliably outperform" self-consistency; "more sensitive to different hyperparameter settings" | PR |  SOURCES: SMIT
B007. [3.7 Several agents: what the evidence says] First, multi-agent systems win partly by spending more: Anthropic's own analysis credits tokens with most of the variance, and the equal-budget studies find smaller or negative gains .  SOURCES: MAR, SCAL, TRAN
B008. [3.7 Several agents: what the evidence says] Second, the gain depends on the task: wide, separable research helped; sequential planning got worse .  SOURCES: SCAL
B009. [3.7 Several agents: what the evidence says] MAST's authors "conjecture that improvements in the base model capabilities will be insufficient" to fix them .  SOURCES: MAST
B010. [3.7 Several agents: what the evidence says] Cognition's 2025 post "Don't Build Multi-Agents" set two principles: "Share context, and share full agent traces, not just individual messages", and "Actions carry implicit decisions, and conflicting decisions carry bad results" .  SOURCES: CG1
B011. [3.7 Several agents: what the evidence says] Its April 2026 follow-up keeps them for "parallel-writer swarms" but reports multi-agent setups working when "writes stay single-threaded": a reviewer with a clean context, a stronger model consulted for advice, a manager delegating to children .  SOURCES: CG2
B012. [3.7 Several agents: what the evidence says] Anthropic's post says shared-context domains and "most coding tasks" are poor fits .  SOURCES: MAR
B013. [3.7 Several agents: what the evidence says] So Gemini's claim that splitting a fragile mega-prompt into specialists fixes it (ledger B1-01) is overstated: it helps for parallel, separable work and adds failures of its own .  SOURCES: MAR, MAST, SCAL
B014. [3.8 How context moves between agents] | OpenAI handoff | "the entire previous conversation history", unless an `input_filter` trims it | Nothing: the receiver takes over the conversation |  |  SOURCES: OAS
B015. [3.8 How context moves between agents] | OpenAI `Agent.as_tool()` | Only the input the manager generated | The nested run's final output |  |  SOURCES: OAS
B016. [3.8 How context moves between agents] | Claude subagent | Its own system prompt and "the Agent tool's prompt string"; not the parent's history | "only its final message" |  |  SOURCES: CSA
B017. [3.8 How context moves between agents] | LangGraph supervisor (`langgraph-supervisor` 0.0.31) | What the supervisor passes | By default only the worker's last message (`output_mode="last_message"`) |  |  SOURCES: LGSU
B018. [3.8 How context moves between agents] | Microsoft Agent Framework handoff | "The entire conversation is maintained and reused on every hop" | Control moves to the next agent |  |  SOURCES: MAF
B019. [3.8 How context moves between agents] And trimming history has limits: OpenAI's built-in filter "removes structured tool items" but "does not redact tool arguments or results already copied into ordinary messages"; the lab shows tool output surviving inside an assistant message (check 9b) .  SOURCES: OAS
B020. [3.8 How context moves between agents] Two more details from the OpenAI docs: the option that compacts earlier history on handoff, `nest_handoff_history`, is "an opt-in beta and is disabled by default"; and "Input guardrails still apply only to the first agent in the chain" .  SOURCES: OAS
B021. [3.8 How context moves between agents] By default, "a subagent can spawn subagents of its own, up to three layers below the main conversation", up to 20 run at once, and the SDK offers a spend cap (`max_budget_usd`, unlimited by default) .  SOURCES: CCS, CSA
B022. [3.8 How context moves between agents] Each subagent "spends tokens of its own while it runs" .  SOURCES: CCS
B023. [3.8 How context moves between agents] Microsoft Agent Framework ships Sequential, Concurrent, Handoff, GroupChat and Magentic builders .  SOURCES: MAF
B024. [3.8 How context moves between agents] CrewAI's `Process` has two values, `sequential` and `hierarchical`, the second requiring a `manager_llm` or `manager_agent`; its Flows add event-driven steps (ledger B1-05: the processes are confirmed; "fastest way to prototype" is unmeasured) .  SOURCES: CRW
B025. [3.8 How context moves between agents] Google's ADK has `SequentialAgent`, `ParallelAgent` and `LoopAgent` .  SOURCES: ADK
B026. [3.8 How context moves between agents] LangGraph's swarm hands off with `Command(goto=agent_name, graph=Command.PARENT)`, and the `langgraph-supervisor` README now recommends "the supervisor pattern directly via tools rather than this library for most use cases" .  SOURCES: LGSU, LGSW
B027. [3.8 How context moves between agents] Gemini's claim that LangGraph is "vastly superior" for resumable, compliant work (ledger B1-04) is unsupported: it has those features, and so do the others; no comparison was found .  SOURCES: LGS, MAF, OAS
B028. [3.9 What several agents cost, and how errors spread] Anthropic's measured multipliers are the real-world version: about 4x a chat for one agent and about 15x for its multi-agent system .  SOURCES: MAR
B029. [3.9 What several agents cost, and how errors spread] A verifier that checks the final result catches some of this; Kim et al. report that independent agents amplified errors 17.2 times at the trace level, against 4.4 for a centralized design with a coordinator .  SOURCES: SCAL
B030. [3.9 What several agents cost, and how errors spread] That factor counts the extra work caused by coordination failures in their traces, not 17 times more wrong answers .  SOURCES: SCAL
B031. [3.9 What several agents cost, and how errors spread] Copies of one model with one prompt tend to share mistakes, which is a reason debate and voting gains shrink at equal budgets and why one 2025 audit proposed mixing different models .  SOURCES: SMIT, ZHNG
B032. [3.9 What several agents cost, and how errors spread] A 2024 preprint showed a self-replicating injection passing through simulated agent societies, reaching all of 10 agents in about 4.7 turns, and found that marking inter-agent text as data combined with a tagging step blocked it in its tests .  SOURCES: PINF
B033. [3.10 Which frameworks are current] Gemini's framework list (ledger P6-05) is outdated :  SOURCES: AGN, MAF, OADP, PYPI
B034. [3.10 Which frameworks are current] - **OpenAI Assistants API**: removed from the API on August 26, 2026; the replacement is the Responses API with the Conversations API .  SOURCES: OADP
B035. [3.10 Which frameworks are current] The OpenAI Agents SDK (0.24.0, released October 15, 2026) is OpenAI's agent framework .  SOURCES: PYPI
B036. [3.10 Which frameworks are current] It will not receive new features or enhancements and is community managed going forward" (README, April 6, 2026); its last release, autogen-agentchat 0.7.5, dates from September 30, 2025 .  SOURCES: AGN, PYPI
B037. [3.10 Which frameworks are current] - **Microsoft Agent Framework**: "the next generation of both Semantic Kernel and AutoGen" ; 1.0.0 on April 2, 2026, 1.22.0 on October 15, 2026, MIT .  SOURCES: MAF, MSL, PYPI
B038. [3.10 Which frameworks are current] - **LangGraph** (1.2.15) and **CrewAI** (1.15.28) remain current .  SOURCES: PYPI
B039. [3.10 Which frameworks are current] CrewAI sends anonymous telemetry unless `CREWAI_DISABLE_TELEMETRY`, `CREWAI_DISABLE_TRACKING` or `OTEL_SDK_DISABLED` is set to true .  SOURCES: CRW
B040. [3.10 Which frameworks are current] Microsoft's own overview gives the simplest advice of all: "If you can write a function to handle the task, do that instead of using an AI agent" .  SOURCES: MSL
B041. [4. Gemini said, evidence says] | Orchestration is a DAG or a cyclic state graph (P8-01) | Overstated: true of Airflow (a DAG) and LangGraph (a state graph); Temporal, DBOS and Restate run ordinary code with recorded steps  | 3.2 |  SOURCES: AFL, DBS, LGD, TDC
B042. [4. Gemini said, evidence says] | Routers send simple queries to "highly quantized, rapid models" (P8-02) | Corrected: Anthropic's example routes to "smaller, cost-efficient models like Claude Haiku 4.5"; quantization is a different technique  | 3.1 |  SOURCES: BEA
B043. [4. Gemini said, evidence says] | Evaluator-optimizer loops rewrite until a quality threshold is met (P8-03) | Overstated: the source has no numeric threshold; the loop runs until the judge accepts, and needs an iteration cap  | 3.1 |  SOURCES: BEA, LGD
B044. [4. Gemini said, evidence says] | Temporal, Airflow, LangGraph and Celery are "the industry standard" (P8-04) | Unsupported: four tools for four different jobs; no adoption data found  | 3.2 |  SOURCES: AFL, CEL, LGD, TDC
B045. [4. Gemini said, evidence says] | Examples: routing to a cache, a translation loop, map-reduce over 50 chunks with Celery (P8-05) | Illustrative ; the mechanisms exist (routing, Anthropic's literary-translation example, Celery chords and chunks, LangGraph's `Send`)  | 3.1 |  SOURCES: BEA, CEL, LGS
B046. [4. Gemini said, evidence says] | Curriculum: asyncio, backoff with jitter, a LangGraph "DAG" with conditional edges (P8-06) | Corrected: a LangGraph graph may loop, so it is a state graph; backoff with jitter is sound  | 3.2, 3.5 |  SOURCES: AWC, LGD
B047. [4. Gemini said, evidence says] | Frameworks: LangGraph, CrewAI, AutoGen, OpenAI Assistants API (P6-05) | Outdated: the Assistants API was removed on August 26, 2026; AutoGen is in maintenance mode, succeeded by Microsoft Agent Framework  | 3.10 |  SOURCES: AGN, MAF, OADP
B048. [4. Gemini said, evidence says] | One mega-prompt is "highly fragile"; specialized agents fix this (B1-01) | Overstated: gains on wide, separable research at much higher token cost; losses on sequential planning; at equal budgets a single agent often matches  | 3.7 |  SOURCES: MAR, SCAL, TRAN
B049. [4. Gemini said, evidence says] | LangGraph: a cyclic state graph, explicit routing, thread-scoped checkpoints (B1-02) | Confirmed  | 3.3 |  SOURCES: LGD
B050. [4. Gemini said, evidence says] | LangGraph caches node results and skips unchanged nodes (B1-03) | Overstated: node caching is opt-in per node; what skips finished sibling nodes after a failure is "pending writes"  | 3.3 |  SOURCES: LGD, LGS
B051. [4. Gemini said, evidence says] | LangGraph is "vastly superior" for compliant, resumable work (B1-04) | Unsupported: no comparison found; other frameworks have checkpoints and approvals too  | 3.8 |  SOURCES: LGS, MAF, OAS
B052. [4. Gemini said, evidence says] | CrewAI: sequential or hierarchical delegation; "the fastest way to prototype" (B1-05) | First half confirmed; speed unmeasured; Flows add event-driven steps  | 3.8 |  SOURCES: CRW
B053. [4. Gemini said, evidence says] | CrewAI has "less structural durability" for approval chains (B1-06) | Unsupported and partly outdated: `@human_feedback` since 1.8.0 saves state automatically while it waits  | 3.6 |  SOURCES: CRW
B054. [4. Gemini said, evidence says] | Human-in-the-loop breakpoints let a person approve high-stakes actions (B1-07) | Corrected: LangGraph says static breakpoints are for debugging and "not recommended for human-in-the-loop"; use `interrupt()`  | 3.6 |  SOURCES: LGD
B055. [5. Examples] *An orchestrator that over-delegated* .  SOURCES: MAR
B056. [5. Examples] *Docs and code that disagree* .  SOURCES: LGD, LGS
B057. [5. Examples] *A framework shut down under its users* .  SOURCES: OADP
B058. [6. What you need] Checked October 15, 2026 .  SOURCES: PYPI
B059. [6. What you need] | Restate, Inngest | Durable execution services | Restate: Business Source License 1.1; Inngest server: SSPL with a future Apache-2.0 licence. Neither is OSI open source today  | Self-hosted or their clouds | Cloud only | see their sites |  SOURCES: ING, RST
B060. [6. What you need] - **Build a small app:** LangGraph with the SQLite checkpointer while developing; its docs name `PostgresSaver` for production .  SOURCES: LGD
B061. [6. What you need] Anthropic's and Microsoft's advice agree: start with the simplest thing; "If you can write a function to handle the task, do that instead of using an AI agent" .  SOURCES: BEA, MSL
B062. [6. What you need] **When not to use several agents:** when the work is sequential or every step needs the whole context .  SOURCES: MAR, SCAL
B063. [9. Teach it] - *"Resuming continues from the line where it paused."* It restarts the paused step from its beginning; code before the pause runs again .  SOURCES: LGD
B064. [9. Teach it] - *"The SDK makes my model calls idempotent."* The Anthropic and OpenAI SDKs generate a key but don't send it .  SOURCES: ANS, OAI
B065. [9. Teach it] - *"LangGraph stops a runaway graph at 25 steps."* Not since 1.0.6; in 1.2.15 the default is 10,007 .  SOURCES: LGS
B066. [9. Teach it] - *"A breakpoint is an approval step."* LangGraph says static breakpoints are for debugging; use `interrupt()` .  SOURCES: LGD
B067. [9. Teach it] - *"More agents, better answers."* At equal budgets the gains shrink or reverse on sequential work; much of the measured gain comes from spending more tokens .  SOURCES: MAR, SCAL, TRAN
B068. [9. Teach it] - *"A person approved it, so it was checked."* People approve almost everything they're shown when prompts are frequent .  SOURCES: AAM, GRW
B069. [9. Teach it] Answer: 1, 2, 4, 8, 16, 32, 64 and then 100 seconds, since the longest wait is 100 times the first; attempts never run out by default .  SOURCES: TDC
B070. [9. Teach it] *Answers.* (1) Orchestrator-workers .  SOURCES: BEA
B071. [9. Teach it] (2) It's sent again, because the node runs again from its start; move it after the interrupt or make it idempotent .  SOURCES: LGD
B072. [9. Teach it] (3) If the reply is lost, the caller never learns the result, so only the service can recognize the repeat .  SOURCES: STR
B073. [9. Teach it] (4) "the entire previous conversation history"; only the input the manager generated .  SOURCES: OAS
B074. [9. Teach it] (5) Tokens (multi-agent systems used about 15 times a chat's tokens, and token usage explained 80% of the variance on BrowseComp) and models (an Opus 4 lead with Sonnet 4 workers against Opus 4 alone) .  SOURCES: MAR
B075. [9. Teach it] - Anthropic, "Building effective agents"  and "How we built our multi-agent research system" .  SOURCES: BEA, MAR
B076. [9. Teach it] - LangGraph's docs on interrupts and checkpointers .  SOURCES: LGD
B077. [9. Teach it] - Temporal's documentation on workflows, activities and retry policies .  SOURCES: TDC
B078. [9. Teach it] - Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" .  SOURCES: MAST
B079. [10. Limits and debates] - **Most multi-agent evidence is young.** Kim et al. and Tran and Kiela are preprints; Anthropic's 90.2% comes from an internal evaluation nobody else can run; the debate studies used GPT-3.5 .  SOURCES: DU, MAR, SCAL, SMIT, TRAN
B080. [10. Limits and debates] - **"Equal budget" is hard to define.** Calls, tokens, thinking tokens and money give different answers, and Tran and Kiela report "significant artifacts in API-based budget control" .  SOURCES: TRAN
B081. [10. Limits and debates] Du et al. matched the number of calls, not tokens .  SOURCES: DU
B082. [10. Limits and debates] - **Vendor figures without methods.** The 93% approval rate has no stated dataset; the auto-mode classifier's 17% miss rate comes from 52 cases .  SOURCES: AAM
B083. [10. Limits and debates] The automation-bias review covers clinical tools, not AI agents .  SOURCES: GRW
B084. [10. Limits and debates] - **Documentation drifts from code.** LangGraph's step limit (docs 1,000, code 10,007), the SDKs' jitter comment, and Anthropic's edited "Building effective agents" post all show it .  SOURCES: ANS, BEA, LGD, LGS
B085. [10. Limits and debates] *Claim ledger, row P8-01.* The row's note says Temporal and Celery "are neither" a DAG nor a state graph; the evidence supports that, and the row's verdict, "confirmed", should read "overstated", as Section 4 does .  SOURCES: DBS, TDC
B086. [10. Limits and debates] *Row B1-03* is marked confirmed; the evidence shows the caching is opt-in, so "overstated" fits better .  SOURCES: LGD
B087. [10. Limits and debates] An orchestrator that can spawn workers that spawn workers is an unbounded bill." It agrees with this part, and matters more now that Claude Code's subagents can nest three layers by default .  SOURCES: CCS
