# Source check, set B (claims B001-B087)
B001 | SUPPORTED | evidence: MAR "outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval"; "token usage by itself explains 80% of the variance"; "about 4× more tokens than chat interactions"; "about 15× more tokens than chats"; "Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents" (web) | none
B002 | SUPPORTED | evidence: SCAL arXiv html v3 "maintains identical task prompts, tools, and computational budgets across all configurations"; "+80.8% on decomposable financial reasoning to -70.0% on sequential planning"; "single-agent performance already exceeds 45% accuracy experience negative returns" (abstract page itself only says "standardizing tools, prompts, and compute"; the "identical ... budgets" wording is in the body) | none
B003 | SUPPORTED | evidence: TRAN v2 (11 Apr 2026) Table 1 average at 1,000 tokens: SAS 0.418, sequential 0.379, debate 0.388; abstract "SAS consistently match or outperform MAS" | gaps 3.9 and 3.0 pp are correct arithmetic
B004 | SUPPORTED | evidence: MAST v3 intro "1642 annotated execution traces", 7 frameworks, 14 modes, 3 categories; FM-1.3 step repetition 15.7%, FM-2.6 reasoning-action mismatch 13.2% (first and second largest) | NeurIPS 2025 spotlight status not on the arXiv page (not checked)
B005 | SUPPORTED | evidence: DU pdf Table 1 "Single Agent 67.0", "Multiagent (Majority) 75.0", "Multiagent (Debate) 81.8"; "run with 3 agents and two rounds of debate"; "chatGPT-3.5"; majority "total of 6 agents to match the cost of using 3 agents with 2 rounds of debate" | none
B006 | SUPPORTED | evidence: SMIT abstract "do not reliably outperform other proposed prompting strategies, such as self-consistency"; "more sensitive to different hyperparameter settings" ; GPT-3.5, medical and non-medical sets | none
B007 | SUPPORTED | evidence: MAR 80% variance; SCAL/TRAN equal-budget results | none
B008 | PARTLY | evidence: SCAL "+80.8% on decomposable financial reasoning ... -70.0% on sequential planning" | "wide, separable research helped" comes from MAR, not SCAL (only SCAL is cited); SCAL's positive case is financial reasoning, not research
B009 | SUPPORTED | evidence: MAST v3 "we conjecture that improvements in the base model capabilities will be insufficient to address the full MAST" | none
B010 | SUPPORTED | evidence: CG1 both quotes verbatim, 2025-06-12 | none
B011 | SUPPORTED | evidence: CG2 "Our original observations still hold today for parallel-writer swarms"; "while writes stay single-threaded"; reviewer with clean context, stronger "smart friend" model, manager Devin spawning child Devins; 2026-04-22 | none
B012 | SUPPORTED | evidence: MAR "some domains that require all agents to share the same context"; "most coding tasks involve fewer truly parallelizable tasks than research" | "poor fits" is mild paraphrase of "not a good fit"
B013 | SUPPORTED | evidence: MAR, MAST, SCAL as above | interpretive, consistent with sources
B014 | SUPPORTED | evidence: OAS docs/handoffs.md:112 "gets to see the entire previous conversation history. If you want to change this, you can set an input_filter" | none
B015 | SUPPORTED | evidence: OAS tools.md "the parent run's conversation state is not inherited automatically"; as_tool default input {"input": "..."}; agent.py as_tool returns run_result.final_output (agent.py:1071-1100) | none
B016 | SUPPORTED | evidence: CSA "The only content you pass from parent to subagent is the Agent tool's prompt string"; "only its final message returns to the parent"; table: receives "Its own system prompt (AgentDefinition.prompt) and the Agent tool's prompt", not "The parent's conversation history" | none
B017 | SUPPORTED | evidence: LGSU supervisor.py:225 output_mode: OutputMode = "last_message"; "last_message: add only the last message" | none
B018 | SUPPORTED | evidence: MAF _handoff.py:24 "The entire conversation is maintained and reused on every hop" | none
B019 | SUPPORTED | evidence: OAS handoffs.md:154 "`remove_all_tools` removes structured tool items. It does not redact tool arguments or results already copied into ordinary messages or nested-history summaries." | lab check 9b out of scope
B020 | SUPPORTED | evidence: OAS handoffs.md:122 "available as an opt-in beta and is disabled by default while we stabilize it"; :136 "Input guardrails still apply only to the first agent in the chain" | none
B021 | SUPPORTED | evidence: CCS "By default, a subagent can spawn subagents of its own, up to three layers below the main conversation"; CSA table: 20 at once default, max_budget_usd "No limit" | none
B022 | SUPPORTED | evidence: CCS "each subagent spends tokens of its own while it runs" | none
B023 | SUPPORTED | evidence: MAF orchestrations/__init__.py lists SequentialBuilder, ConcurrentBuilder, HandoffBuilder, GroupChatBuilder, MagenticBuilder | MSL overview page does not name these, but claim cites MAF repo
B024 | SUPPORTED | evidence: CRW process.py Process: sequential, hierarchical; crew.py:728-732 "manager_llm or manager_agent is required when using hierarchical process" | Flows event-driven not separately opened
B025 | SUPPORTED | evidence: ADK 2.12.0 agents/sequential_agent.py, parallel_agent.py, loop_agent.py class definitions | none
B026 | SUPPORTED | evidence: LGSW handoff.py:83-85 Command(... graph=Command.PARENT); LGSU METADATA "We now recommend using the **supervisor pattern directly via tools** rather than this library for most use cases" | quote matches apart from markdown bold
B027 | SUPPORTED-OUT-OF-SCOPE | evidence: absence-of-comparison claim | not checkable as a negative; features exist in LGS/MAF/OAS (checkpoints, interrupts, needs_approval)
B028 | SUPPORTED | evidence: MAR 4x/15x | none
B029 | SUPPORTED | evidence: SCAL html "Independent systems reach 17.2× amplification" vs centralized "4.4×", trace-level | none
B030 | SUPPORTED | evidence: SCAL "trace-level error amplification factor ... measures how much extra computational work arises from inter-agent coordination failures" | none
B031 | PARTLY | evidence: ZHNG abstract "model heterogeneity ... a universal antidote to consistently improve current MAD frameworks"; MAD "often fail to outperform simple single-agent baselines" | the causal mechanism "copies of one model share mistakes" is not stated in the abstract or in SMIT (not found); mixing models proposal is supported; ZHNG v3 dated 2025-06-21
B032 | PARTLY | evidence: PINF "full infection is achieved by turn 4.7" for 10 agents; "The Marking + LLM Tagging strategy successfully prevents all attacks" | paper defines Marking as "Inserting a special symbol like ^ to distinguish between user and agent prompts", not "marking inter-agent text as data"; standalone Marking still allowed 76% of attacks; 4.7 given as a turn, not clearly an average
B033 | SUPPORTED | evidence: see B034, B036, B037 (PYPI/OADP/AGN/MAF checks) | none
B034 | SUPPORTED | evidence: OADP page "2026-08-26" shutdown; replacement "Responses API and Conversations API" (web) | none
B035 | SUPPORTED | evidence: PYPI json openai-agents 0.24.0 upload_time 2026-10-15T02:38:18 | none
B036 | SUPPORTED | evidence: AGN README.md:21 "It will not receive new features or enhancements and is community managed going forward."; git commit 027ecf0 dated 2026-04-06; PYPI autogen-agentchat 0.7.5 uploaded 2025-09-30 | none
B037 | SUPPORTED | evidence: MSL "In short, Agent Framework is the next generation of both Semantic Kernel and AutoGen."; PYPI agent-framework 1.0.0 2026-04-02T16:39, 1.22.0 2026-10-15T09:54; classifier "License :: OSI Approved :: MIT License" | none
B038 | SUPPORTED | evidence: PYPI latest langgraph 1.2.15 (2026-10-12), crewai 1.15.28 (2026-10-14) | "remain current" true only as of the PyPI snapshot
B039 | SUPPORTED | evidence: CRW crewai_core/telemetry.py:1 "Anonymous telemetry collection"; :356-358 OTEL_SDK_DISABLED, CREWAI_DISABLE_TELEMETRY, CREWAI_DISABLE_TRACKING | code accepts true/1/yes/on, not only "true"
B040 | SUPPORTED | evidence: MSL "If you can write a function to handle the task, do that instead of using an AI agent." | none
B041 | SUPPORTED | evidence: AFL airflow dag_cycle_tester / check_cycle (acyclic DAG); LGD graph-api "looping, stateful workflows"; DBS README "annotating ordinary functions as workflows and steps"; TDC workflow-definition.mdx "a sequence of steps written in a general-purpose programming language" | Restate is not among the cited sources for this row (not checked here)
B042 | SUPPORTED | evidence: BEA "Routing easy/common questions to smaller, cost-efficient models like Claude Haiku 4.5" | "quantization is a different technique" is outside the source
B043 | SUPPORTED | evidence: BEA evaluator-optimizer has no numeric threshold; agents section "it's also common to include stopping conditions (such as a maximum number of iterations)"; LGD recursion limit | none
B044 | SUPPORTED-OUT-OF-SCOPE | evidence: tools exist and do different jobs (AFL, CEL, LGD, TDC) | "no adoption data found" is a negative, not checkable
B045 | SUPPORTED | evidence: BEA "Literary translation where there are nuances..."; CEL canvas.rst chord (line 284), chunks (line 312); LGS types.py:738 class Send | none
B046 | SUPPORTED | evidence: LGD graph-api "build looping, stateful workflows"; AWC backoff_simulator.py ExpoBackoffEqualJitter/FullJitter | none
B047 | SUPPORTED | evidence: OADP, AGN, MAF as above | none
B048 | SUPPORTED | evidence: MAR (~15x tokens), SCAL (-70.0% sequential planning), TRAN (single matches or beats at equal reasoning tokens) | "often matches" is slightly softer than TRAN "consistently"; fine
B049 | SUPPORTED | evidence: LGD graph-api "looping, stateful workflows"; checkpointers by thread_id | none
B050 | SUPPORTED | evidence: LGD graph-api.mdx:873-906 cache is specified at compile and per-node CachePolicy (opt-in); checkpointers.mdx:29 "Pending writes ... When you resume ... you don't re-run the successful nodes." | none
B051 | SUPPORTED-OUT-OF-SCOPE | evidence: LGS checkpoints, OAS needs_approval/interruptions (tools.md:779), MAF tool approval state in _tools.py | "no comparison found" is a negative
B052 | SUPPORTED | evidence: CRW Process enum sequential/hierarchical | "fastest way to prototype" correctly flagged unmeasured
B053 | SUPPORTED | evidence: CRW docs v1.15.28 learn/human-feedback-in-flows.mdx:11 "requires CrewAI version 1.8.0 or higher"; :486 "The flow framework automatically persists state when HumanFeedbackPending is raised" | "since 1.8.0 saves state automatically" is a slight inference: 1.8.0 is when the decorator arrived, auto-persistence is described in current docs
B054 | SUPPORTED | evidence: LGD interrupts.mdx:1578 "Static interrupts are **not** recommended for human-in-the-loop workflows. Use the interrupt function instead."; :1571 "To debug and test a graph, you can use static interrupts as breakpoints" | none
B055 | SUPPORTED | evidence: MAR "spawning 50 subagents for simple queries" | none
B056 | SUPPORTED | evidence: LGD graph-api.mdx:1502 "Starting in version 1.0.6, the default recursion limit is set to 1000 steps" (also :1512 JS "25"); LGS _config.py:32 default 10007 | none
B057 | SUPPORTED | evidence: OADP | none
B058 | SUPPORTED | evidence: PYPI json files, upload times through 2026-10-15 | none
B059 | SUPPORTED | evidence: ING LICENSE.md "Server Side Public License ... Apache 2.0 Future License"; RST LICENSE "Business Source License 1.1" | "Neither is OSI open source" is general knowledge, not in the files
B060 | SUPPORTED | evidence: LGD checkpointers.mdx:629 SqliteSaver "Ideal for experimentation and local workflows"; :630 PostgresSaver "Ideal for using in production" | none
B061 | SUPPORTED | evidence: MSL quote verbatim; BEA "finding the simplest solution possible, and only increasing complexity when needed" | none
B062 | SUPPORTED | evidence: MAR shared-context caveat; SCAL -70.0% on sequential planning | none
B063 | SUPPORTED | evidence: LGD interrupts.mdx:1010 "the runtime restarts the entire node from the beginning ... it does not resume from the exact line where interrupt was called" | none
B064 | SUPPORTED | evidence: ANS and OAI _base_client.py: _idempotency_header = None (line 456 / 472), key only added if header set (551 / 540) | none
B065 | SUPPORTED | evidence: LGS 1.2.15 _config.py:32 "10007"; langgraph 1.0.5 wheel default "25", 1.0.6 wheel "10000" | none
B066 | SUPPORTED | evidence: see B054 | none
B067 | SUPPORTED | evidence: MAR, SCAL, TRAN | none
B068 | SUPPORTED | evidence: AAM "Claude Code users approve 93% of permission prompts"; "approval fatigue, where people stop paying close attention to what they're approving"; GRW abstract on over-reliance on automation | GRW is about clinical decision support
B069 | SUPPORTED | evidence: TDC retry-policies.mdx:136-137 1s initial, 2.0 coefficient, max interval 100s, max attempts unlimited; :174 "Maximum Interval = 100 × Initial Interval" | docs line 31 mentions a 10 minute cap, but for Workflow Tasks, not Activities
B070 | SUPPORTED | evidence: BEA orchestrator-workers "dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results" | the quiz question itself is not visible; answer is plausible
B071 | SUPPORTED | evidence: LGD interrupts.mdx:1352-1354 "side effects called before interrupt should (ideally) be idempotent" | none
B072 | SUPPORTED | evidence: STR "if a connection error occurs, you can safely repeat the request"; "unique key that the server uses to recognize subsequent retries" | none
B073 | SUPPORTED | evidence: OAS handoffs.md:112; tools.md as_tool input | none
B074 | SUPPORTED | evidence: MAR 15x, 80% variance on BrowseComp, Opus 4 lead + Sonnet 4 | none
B075 | SUPPORTED | evidence: BEA and MAR titles/URLs fetched | none
B076 | SUPPORTED | evidence: LGD interrupts.mdx and checkpointers.mdx exist | none
B077 | SUPPORTED | evidence: TDC docs workflow-definition.mdx, retry-policies.mdx, activities/ exist | none
B078 | SUPPORTED | evidence: MAST arXiv 2503.13657 | none
B079 | SUPPORTED | evidence: SCAL, TRAN arXiv-only; MAR "internal research eval"; DU "chatGPT-3.5", SMIT "GPT-3.5" | none
B080 | SUPPORTED | evidence: TRAN abstract "We identify significant artifacts in API-based budget control (particularly in Gemini 2.5)" | none
B081 | PARTLY | evidence: DU appendix "6 agents to match the cost of using 3 agents with 2 rounds of debate" | paper says it matched cost via agent/call count; it does not say "not tokens". "calls, not tokens" is an inference (6 = 3x2 generations)
B082 | SUPPORTED | evidence: AAM "Claude Code users approve 93% of permission prompts" with no dataset or method stated; "17% false-negative rate on real overeager actions", test set of 52 cases | none
B083 | SUPPORTED | evidence: GRW abstract: automation bias in healthcare / clinical decision support systems | none
B084 | SUPPORTED | evidence: LGD :1502 "1000" vs LGS 10007; ANS _base_client.py:924 comment "plus-or-minus half a second" vs code `jitter = 1 - 0.25 * random()` (0-25% reduction); BEA post edited (Haiku 4.5 reference) | none
B085 | SUPPORTED-OUT-OF-SCOPE | evidence: TDC (general-purpose code workflows), DBS README | the ledger row and verdict are outside scope; Celery not separately checked as "neither"
B086 | SUPPORTED | evidence: LGD graph-api.mdx:873-906 cache needs cache= at compile and CachePolicy per node | none
B087 | SUPPORTED | evidence: CCS "By default, a subagent can spawn subagents of its own, up to three layers below the main conversation" | the quoted "unbounded bill" sentence is from another document, out of scope

## Summary
Counts (87 claims): SUPPORTED 79 ; SUPPORTED-OUT-OF-SCOPE 4 (B027, B044, B051, B085) ; PARTLY 4 (B008, B031, B032, B081) ; CONTRADICTED 0 ; NOT CHECKABLE 0.
Web lookups used: 28 of 40 (one, a PubMed query, was rate limited and not retried; the abstract was read from the OUP page instead).
Non-SUPPORTED claims:
- B008: "wide, separable research helped" is from MAR; SCAL (the only cited source) has financial reasoning +80.8% and sequential planning -70.0%.
- B031: "shared mistakes" mechanism not found in SMIT or ZHNG abstract; ZHNG does propose model heterogeneity.
- B032: the paper's Marking defense is a special symbol (^) distinguishing user and agent prompts, not "marking inter-agent text as data"; Marking alone still allowed 76% of attacks; 4.7 is a turn count for 10 agents.
- B081: Du et al. matched "cost" via 6 agents vs 3 agents x 2 rounds; "not tokens" is an inference.
- B027, B044, B051, B085: negative or ledger-level statements (no comparison / no adoption data found / row verdict), not checkable against sources; underlying facts check out.
Minor notes: B004 NeurIPS 2025 spotlight and B059 "neither is OSI" are not in the fetched sources; B041 names Restate, which is not among its cited sources; B053 "since 1.8.0 saves state" is a slight inference. No instructions aimed at AI assistants were found in any source.
