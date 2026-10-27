# Source check, set A (claims A001-A083)
A001 | SUPPORTED | evidence: BEA "Workflows are systems where LLMs and tools are orchestrated through predefined code paths"; "LLMs dynamically direct their own processes and tool usage" (web) | none
A002 | SUPPORTED | evidence: BEA "we recommend finding the simplest solution possible, and only increasing complexity when needed" | none
A003 | SUPPORTED | evidence: TDC docs/encyclopedia/temporal.mdx:31 exact quote | none
A004 | SUPPORTED | evidence: MAR "outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval"; "multi-agent systems use about 15× more tokens than chats" | none (comparison is vs single-agent Opus 4)
A005 | SUPPORTED | evidence: OWA "Utilise human-in-the-loop control to require a human to approve high-impact actions before they are taken" | quote begins mid-sentence, fine
A006 | SUPPORTED | evidence: AAM "Claude Code users approve 93% of permission prompts." | none
A007 | SUPPORTED | evidence: BEA workflow definition | none
A008 | SUPPORTED | evidence: BEA prompt chaining: sequential LLM steps | none
A009 | SUPPORTED | evidence: BEA routing: classifies input, sends to specialized task | none
A010 | SUPPORTED | evidence: BEA parallelization: sectioning, voting | none
A011 | SUPPORTED | evidence: BEA orchestrator-workers | none
A012 | SUPPORTED | evidence: BEA evaluator-optimizer "in a loop" | none
A013 | SUPPORTED | evidence: LGD graph-api.mdx:4 "looping, stateful workflows"; graph-api.mdx:41 | none
A014 | SUPPORTED | evidence: AFL docs "The term “DAG” comes from the mathematical concept “directed acyclic graph”"; dag_cycle_tester.py raises AirflowDagCycleException | none
A015 | SUPPORTED | evidence: LGD checkpointers.mdx:7 "saves a snapshot of graph state at each super-step, organized into threads"; :37 thread_id must | none
A016 | SUPPORTED | evidence: LGD checkpointers.mdx:35 "A thread is a unique ID ... assigned to each checkpoint" | none
A017 | SUPPORTED | evidence: TDC temporal.mdx:31 | none
A018 | SUPPORTED | evidence: LGD interrupts.mdx:1354 "idempotency means that the same operation can be applied multiple times without changing the result beyond the initial execution"; TDC glossary.md:310 | none
A019 | SUPPORTED | evidence: STR "a unique key that the server uses to recognize subsequent retries of the same request" | none
A020 | SUPPORTED | evidence: AWB / AWC (expo + random jitter) | none
A021 | SUPPORTED | evidence: LGS pregel/main.py:3096 "Recursion limit of {n} reached without hitting a stop condition"; LGD graph-api.mdx:1502 "maximum number of super-steps" | none
A022 | SUPPORTED | evidence: LGD interrupts.mdx (interrupt pauses until resumed with Command) | none
A023 | SUPPORTED | evidence: LGD interrupts.mdx:1571,1578 "Static interrupts are **not** recommended for human-in-the-loop workflows" | none
A024 | SUPPORTED | evidence: OAS handoffs.md:112 "the new agent takes over the conversation, and gets to see the entire previous conversation history" | none
A025 | PARTLY | evidence: OAS multi_agent.md "agents as tools ... bounded subtask but should not take over the user-facing conversation" | "with only a brief" (the sub-agent seeing only a short instruction, not the conversation) is not stated in the docs read
A026 | SUPPORTED | evidence: CSA "each subagent runs in its own conversation, which starts fresh"; "its context window starts fresh" | none
A027 | SUPPORTED | evidence: GRW "the tendency to over-rely on automation" (abstract, via OUP page) | none
A028 | SUPPORTED | evidence: BEA page names five workflow patterns | none
A029 | SUPPORTED | evidence: BEA "Much of the tooling landscape described in this post has changed since December 2024"; Haiku 4.5 and Sonnet 4.5 appear | none
A030 | SUPPORTED | evidence: BEA "Routing easy/common questions to smaller, cost-efficient models like Claude Haiku 4.5"; "highly quantized" absent | none
A031 | SUPPORTED | evidence: LGD workflows-agents.mdx:1513 "This loop continues until an acceptable response is generated." | BEA has no numeric threshold (checked page text)
A032 | SUPPORTED | evidence: BEA "common to include stopping conditions (such as a maximum number of iterations)" | none
A033 | SUPPORTED-OUT-OF-SCOPE | evidence: the three models are sourced by A034-A037 | sourced part checks out
A034 | SUPPORTED | evidence: AFL "The term “DAG” comes from the mathematical concept “directed acyclic graph”" (Airflow 3.3.2 docs); airflow/utils/dag_cycle_tester.py:42 ":raises AirflowDagCycleException: If cycle is found" | none
A035 | SUPPORTED | evidence: LGD graph-api.mdx:4 "build looping, stateful workflows" | none
A036 | SUPPORTED | evidence: LGD graph-api.mdx:41 "complex, looping workflows" (cycles allowed, so not a DAG) | the ledger reference is outside scope
A037 | SUPPORTED | evidence: DBS README "checkpointing its state in Postgres"; RST README "prevent re-executing completed steps"; TDC workflow-definition.mdx:220 replay | none
A038 | SUPPORTED-OUT-OF-SCOPE | evidence: AFL METADATA "author, schedule, and monitor workflows"; CEL README.rst:91 "What's a Task Queue?"; TDC durable execution; LGD agent graphs | the four jobs check out; absence of an "industry standard" claim in any source cannot be proven
A039 | SUPPORTED | evidence: LGD graph-api.mdx:49 "A super-step can be considered a single iteration over the graph nodes. Nodes that run in parallel are part of the same super-step" | none
A040 | SUPPORTED | evidence: LGD checkpointers.mdx:65 "LangGraph creates a checkpoint at each **super-step** boundary"; :37 "you **must** specify a `thread_id`" | none
A041 | SUPPORTED | evidence: LGD checkpointers.mdx:581-605 durability modes "exit", "async", "sync"; LGS types.py:98 Durability = Literal["sync","async","exit"] | none
A042 | SUPPORTED | evidence: LGD graph-api.mdx:772 "Code and side effects before the pause run again." | none
A043 | SUPPORTED | evidence: LGD graph-api.mdx:774 "Use idempotency keys, upserts, or read-before-write checks." | none
A044 | SUPPORTED | evidence: LGD checkpointers.mdx:67 "the successful nodes' writes are already durable and don't need to be re-run on" resume | none
A045 | SUPPORTED | evidence: LGD graph-api.mdx:875 "`key_func` ... defaults to a `hash` of the input with pickle"; :906 compile(cache=InMemoryCache()) | quote omits backticks only
A046 | SUPPORTED | evidence: LGS pregel/main.py:3096-3098 "Recursion limit of {config['recursion_limit']} reached without hitting a stop condition" ; errors.py GraphRecursionError | none
A047 | SUPPORTED | evidence: LGH lg_1.0.5 default "25"; lg_1.0.6 "10000"; lg_1.1.0 "10000"; lg_1.2.0 and 1.2.15 `DEFAULT_RECURSION_LIMIT = int(getenv("LANGGRAPH_DEFAULT_RECURSION_LIMIT", "10007"))` | none
A048 | SUPPORTED | evidence: LGD graph-api.mdx:1502 "Starting in version 1.0.6, the default recursion limit is set to 1000 steps" | (the JS variant at :1512 says 25)
A049 | SUPPORTED | evidence: TDC core-primitives.mdx:23 "Activities perform a single, well-defined action, such as calling another service" | "model calls included" is the document's gloss, not in source
A050 | SUPPORTED | evidence: TDC workflow-definition.mdx:201 exact | none
A051 | SUPPORTED | evidence: TDC workflow-definition.mdx:220 "the Commands that are emitted are compared with the existing Event History" | none
A052 | SUPPORTED | evidence: TDC workflow-definition.mdx:228 "returns a _non-deterministic_ error" | clock/random gloss is general Temporal doctrine
A053 | SUPPORTED | evidence: TDC retry-policies.mdx:172-175 Initial 1 s, coefficient 2.0, max 100 x initial, attempts unlimited; TPS common.py initial_interval=1s, backoff 2.0, "Default 100x", maximum_attempts 0 | none
A054 | SUPPORTED | evidence: TDC retry-policies.mdx:146 "Workflow Executions do not retry by default" | none
A055 | SUPPORTED | evidence: TDC limits.mdx:5 "51,200 Events or 50 MB ... warn after 10,240 Events or 10 MB"; TSV constants.go 50*1024*1024, 10*1024*1024, historyCount 50*1024 / 10*1024 | docs say MB; code is MiB (claim says docs and server code)
A056 | SUPPORTED | evidence: TDC develop/python/workflows/timers.mdx:18 "A Workflow can sleep for months." | none
A057 | SUPPORTED | evidence: TSV LICENSE "The MIT License"; temporalio_sdk-python LICENSE MIT; temporalio 1.34.0 METADATA License-Expression: MIT; TDC pricing.mdx:14 "Temporal Cloud is a consumption-based service" | none
A058 | SUPPORTED | evidence: TSV constants.go limit.historyCount.suggestContinueAsNew; TDC continue-as-new.mdx "passed to a new Workflow Execution, with a fresh Event History" | agent-loop inference is the document's
A059 | SUPPORTED | evidence: ANS/OAI _constants.py DEFAULT_MAX_RETRIES = 2, INITIAL_RETRY_DELAY = 0.5, MAX_RETRY_DELAY = 8.0; _should_retry 408/409/429/>=500 | none
A060 | SUPPORTED | evidence: ANS _base_client.py:924-925 "# Apply some jitter, plus-or-minus half a second." / `jitter = 1 - 0.25 * random()` | none
A061 | SUPPORTED | evidence: ANE "A tier spend-cap 429 has no `retry-after` header and keeps failing until access resumes" | none
A062 | SUPPORTED | evidence: LGS types.py:433-441 initial_interval 0.5, backoff_factor 2.0, max_interval 128.0, max_attempts 3 "including the first", jitter True | none
A063 | SUPPORTED | evidence: LGS _internal/_retry.py default_retry_on returns False for ValueError, TypeError, etc. | none
A064 | PARTLY | evidence: AWB "Of the jittered approaches, “Equal Jitter” is the loser."; "Full Jitter" "less work, but slightly more time"; AWC backoff_simulator.py:41-43 `return random.uniform(0, v)` with v = min(cap, pow(2,n)*base) | the formula shown is a rewrite (equivalent), not the code's literal text; post's "less work, but slightly more time" is relative to Decorrelated Jitter, not stated in the claim
A065 | PARTLY | evidence: STR "saves the status code and body of the first request ... Retries ... return the saved response, including `500` errors"; "up to 255 characters long"; "you can remove keys ... after they’re at least 24 hours old"; errors if params differ | the source scopes these to "For API v1"; claim omits that (API v2 behaves differently)
A066 | SUPPORTED | evidence: ANS/OAI _base_client.py:456/472 `self._idempotency_header = None`; :1248 key generated for non-GET retries but header only sent if _idempotency_header set (line 551/562) | none
A067 | SUPPORTED | evidence: TDC activity-definition.mdx:229 "the Activity may be executed multiple times and may even partially complete more than once"; tasks.mdx:140 "effectively once" | none
A068 | SUPPORTED | evidence: CEL docs/userguide/tasks.rst:1085 "Make sure your tasks are :term:`idempotent`." | none
A069 | SUPPORTED | evidence: CEL redis.rst:89 "The default visibility timeout for Redis is 1 hour."; :184 redelivered if not acknowledged | none
A070 | SUPPORTED | evidence: LGD interrupts.mdx:1118 "Matching is **strictly index-based**"; :1013 "Do not wrap `interrupt` calls in try/except"; node restarts from beginning | version 1.2.15 is the wheel, docs unversioned
A071 | SUPPORTED | evidence: OAS human_in_the_loop.md:54 to_state/approve/reject/Runner.run; :193 "`RunState` is designed to be durable"; :197 "do not authenticate the snapshot or the person submitting it" | none
A072 | SUPPORTED | evidence: CAP evaluation order Hooks, Deny, Ask, Permission mode, Allow, canUseTool; "**Auto-approved tools never reach `canUseTool`.**"; "For checks that must run on every tool call, use a [`PreToolUse` hook]" | docs not tied to SDK version 0.2.167
A073 | SUPPORTED | evidence: MAF _tools.py:300 ApprovalMode = Literal["always_require","never_require"]; :755 `approval_mode or "never_require"` | none
A074 | SUPPORTED | evidence: CRW human-feedback-in-flows.mdx:11 "requires **CrewAI version 1.8.0 or higher**"; :486 "automatically persists state"; :514 flow.resume(feedback) | none
A075 | SUPPORTED | evidence: TDC message-passing.mdx:78 "A Signal is an asynchronous message sent to a running Workflow Execution to change its state"; :145 "An Update is a trackable synchronous request"; TPS wait_condition | "Built for waits of days" = timers "sleep for months"
A076 | SUPPORTED | evidence: LGD interrupts.mdx:1578 "Static interrupts are **not** recommended for human-in-the-loop workflows. Use the @[`interrupt`] function instead." | none
A077 | SUPPORTED-OUT-OF-SCOPE | evidence: CRW checkpointing.mdx:52 checkpoint arg, "Enable checkpointing"; human-feedback-in-flows.mdx persistence | opt-in checkpointing and @human_feedback check out; "no source compares the two" is an absence claim
A078 | SUPPORTED | evidence: OAS human_in_the_loop.md:197 RunState snapshots not authenticated | none
A079 | SUPPORTED | evidence: AAM "Over time that leads to approval fatigue, where people stop paying close attention to what they're approving."; "Claude Code users approve 93% of permission prompts."; no data source named | none
A080 | SUPPORTED | evidence: AAM 0.4% false positives on 10,000 real tool calls; 17% false negatives on 52 real overeager actions; "The 17% false-negative rate on real overeager actions is the honest number." | none
A081 | SUPPORTED | evidence: GRW abstract "Of 13 821 retrieved papers, 74 met the inclusion criteria"; workload, task complexity, time constraint as mediators; training and user accountability as mitigators | only a summary of the abstract was retrievable (not verbatim); direction "grows with" inferred from mediator framing
A082 | SUPPORTED | evidence: EUA Art 14(1) "shall be designed and developed in such a way"; 14(4)(b) "remain aware of the possible tendency of automatically relying or over-relying"; 14(4)(e) "interrupt the system through a 'stop' button or a similar procedure" | override clause (14(4)(d)) not separately fetched
A083 | SUPPORTED | evidence: EUA Art 113 (consolidated as at 27 July 2026, Digital Omnibus) "2 December 2027 as regards ... Article 6(2) and Annex III"; "2 August 2028 as regards ... Article 6(1) and Annex I" | "2024 text's earlier dates" not separately checked (original was 2 Aug 2026 / 2 Aug 2027)

## Summary
Counts (83 claims): SUPPORTED 77; PARTLY 3 (A025, A064, A065); SUPPORTED-OUT-OF-SCOPE 3 (A033, A038, A077); CONTRADICTED 0; NOT CHECKABLE 0.
Lookups used: 16 WebFetch (BEA x2, MAR, AAM x2, AWB, Stripe, ANE, CAP, OWA, EUA 14, EUA 113, GRW x2 incl. redirect, Airflow docs, CSA).
Non-SUPPORTED:
- A025 PARTLY: "with only a brief" not stated in OpenAI docs; only "bounded subtask".
- A064 PARTLY: formula is a paraphrase of the code, and "less work, but slightly more time" is relative to Decorrelated Jitter.
- A065 PARTLY: Stripe behaviors are scoped "For API v1"; claim omits this.
- A033, A038, A077 SUPPORTED-OUT-OF-SCOPE: sourced parts check out; absence claims cannot be proven.
No text aimed at AI assistants was found in any source.
