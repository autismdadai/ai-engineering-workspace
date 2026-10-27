# Claims to check, set A

## Sources (key, class: citation with URL)

- **AAM** (VB): Anthropic Engineering, "Claude Code auto mode", March 25, 2026. https://www.anthropic.com/engineering/claude-code-auto-mode
- **AFL** (OD): Apache Airflow 3.3.2: "Dags" page (https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html) and apache-airflow-core 3.3.2 wheel (utils/dag_cycle_tester.py; default retries)
- **ANE** (OD): Claude API docs, "Errors". https://platform.claude.com/docs/en/api/errors
- **ANS** (OD): anthropic 1.14.0 wheel (PyPI): `_constants.py`, `_base_client.py`
- **AWB** (VB): Brooker, "Exponential Backoff And Jitter", AWS Architecture Blog, March 4, 2015 (updated May 2023). https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
- **AWC** (OD): aws-samples/aws-arch-backoff-simulator, src/backoff_simulator.py (the post's companion code)
- **BEA** (VB): Anthropic Engineering, "Building effective agents", December 19, 2024, edited since (read October 15, 2026). https://www.anthropic.com/engineering/building-effective-agents
- **CAP** (OD): Claude Agent SDK docs, permissions. https://code.claude.com/docs/en/agent-sdk/permissions
- **CEL** (OD): Celery 5.6.3 wheel and docs at tag v5.6.3 (configuration, tasks, Redis broker, canvas)
- **CRW** (OD): crewai 1.15.28 and crewai-core 1.15.28 wheels; crewAIInc/crewAI docs at v1.15.28 (human feedback in flows, checkpointing)
- **CSA** (OD): Claude Agent SDK docs, "Subagents in the SDK". https://code.claude.com/docs/en/agent-sdk/subagents
- **DBS** (OD): dbos 3.2.0 wheel; dbos-inc/dbos-transact-py README
- **EUA** (SB): Regulation (EU) 2024/1689 (AI Act), Articles 14 and 113, consolidated as of July 27, 2026, read via the European Commission's AI Act Service Desk. https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-14
- **GRW** (PR): Goddard, Roudsari and Wyatt, "Automation bias: a systematic review of frequency, effect mediators, and mitigators", JAMIA 19(1):121-127, 2012 (abstract). doi:10.1136/amiajnl-2011-000089
- **LGD** (OD): LangChain docs repository (source of docs.langchain.com/oss/python/langgraph/), commit 5cd646e: graph-api, checkpointers, functional-api, interrupts, fault-tolerance, workflows-agents
- **LGH** (OD): langgraph wheels 1.0.5, 1.0.6, 1.1.0, 1.2.0 (PyPI), `_internal/_config.py`
- **LGS** (OD): langgraph 1.2.15 wheel (PyPI): `_internal/_config.py`, `types.py`, `errors.py`, `pregel/main.py`, `_internal/_retry.py`
- **MAF** (OD): microsoft/agent-framework repository (python/CHANGELOG.md, orchestrations, `_handoff.py`) and agent-framework-core 1.22.0 wheel (`_tools.py`)
- **MAR** (VB): Hadfield et al., "How we built our multi-agent research system", Anthropic Engineering, June 13, 2025. https://www.anthropic.com/engineering/multi-agent-research-system
- **OAI** (OD): openai 3.31.0 wheel (PyPI): `_constants.py`, `_base_client.py`
- **OAS** (OD): openai-agents 0.24.0 and 0.23.1 wheels; openai/openai-agents-python docs (human_in_the_loop.md, handoffs.md, multi_agent.md, tools.md) at commit 17d994b
- **OWA** (SB): OWASP, "LLM06:2025 Excessive Agency". https://genai.owasp.org/llmrisk/llm062025-excessive-agency/
- **RST** (OD): restatedev/restate LICENSE and README
- **STR** (OD): Stripe API reference, "Idempotent requests". https://docs.stripe.com/api/idempotent_requests
- **TDC** (OD): temporalio/documentation repository (source of docs.temporal.io), commit cdc231e: glossary, workflow definition and execution, activities, retry policies, limits, message passing, timers, pricing
- **TPS** (OD): temporalio 1.34.0 wheel (PyPI), `common.py`, `workflow/_context.py`
- **TSV** (OD): temporalio/temporal server repository: LICENSE; common/dynamicconfig/constants.go

## Claims

A001. [1. In plain words] **T16, workflows and durable execution.** Anthropic separates **workflows**, "systems where LLMs and tools are orchestrated through predefined code paths", from **agents**, where "LLMs dynamically direct their own processes and tool usage" .  SOURCES: BEA
A002. [1. In plain words] Its advice is to find "the simplest solution possible, and only increasing complexity when needed" .  SOURCES: BEA
A003. [1. In plain words] **Durable execution** is Temporal's term for "the ability of a Workflow Execution to maintain its state and progress even in the face of failures, crashes, or server outages" .  SOURCES: TDC
A004. [1. In plain words] It can help with wide, separable work; Anthropic's research system beat a single agent by 90.2% on its own internal evaluation, while using "about 15× more tokens than chats" .  SOURCES: MAR
A005. [1. In plain words] OWASP advises using "human-in-the-loop control to require a human to approve high-impact actions before they are taken" .  SOURCES: OWA
A006. [1. In plain words] The hard parts are waiting for days without losing state, and making sure people read what they approve: Anthropic reports that "Claude Code users approve 93% of permission prompts" .  SOURCES: AAM
A007. [2. Definitions] | Fixed steps written in code, some of them model calls | Workflow |  |  SOURCES: BEA
A008. [2. Definitions] | A chain of model calls, each using the last one's output | Prompt chaining |  |  SOURCES: BEA
A009. [2. Definitions] | Sending each request to the step or model that suits it | Routing |  |  SOURCES: BEA
A010. [2. Definitions] | Running parts at once, or the same task several times | Parallelization (sectioning; voting) |  |  SOURCES: BEA
A011. [2. Definitions] | One model splits the work and hands parts to others | Orchestrator-workers |  |  SOURCES: BEA
A012. [2. Definitions] | One model writes, another judges, in a loop | Evaluator-optimizer |  |  SOURCES: BEA
A013. [2. Definitions] | A graph whose steps can loop back | State graph (not a DAG) |  |  SOURCES: LGD
A014. [2. Definitions] | A graph with no loops | Directed acyclic graph (DAG) | Airflow's model  |  SOURCES: AFL
A015. [2. Definitions] | A saved snapshot of a run's state | Checkpoint | Keyed by a thread id  |  SOURCES: LGD
A016. [2. Definitions] | One conversation or job, with its own checkpoints | Thread |  |  SOURCES: LGD
A017. [2. Definitions] | Progress that survives crashes and waits | Durable execution |  |  SOURCES: TDC
A018. [2. Definitions] | A step that can run again with the same effect as once | Idempotent step |  |  SOURCES: LGD, TDC
A019. [2. Definitions] | A unique label sent with a request so a repeat is recognized | Idempotency key |  |  SOURCES: STR
A020. [2. Definitions] | Waits that grow each time, with a random part | Exponential backoff with jitter |  |  SOURCES: AWB
A021. [2. Definitions] | A cap on steps before the run is stopped | Recursion limit; step limit |  |  SOURCES: LGS
A022. [2. Definitions] | Pausing a run until a person answers | Interrupt |  |  SOURCES: LGD
A023. [2. Definitions] | A run paused at a fixed step, for debugging | Static breakpoint | Not for approval  |  SOURCES: LGD
A024. [2. Definitions] | Handing the whole conversation to another agent | Handoff |  |  SOURCES: OAS
A025. [2. Definitions] | Calling another agent like a tool, with only a brief | Agent as tool |  |  SOURCES: OAS
A026. [2. Definitions] | A worker agent with its own context window | Subagent |  |  SOURCES: CSA
A027. [2. Definitions] | Trusting an automated suggestion without checking it | Automation bias |  |  SOURCES: GRW
A028. [3.1 Five workflow patterns, and when each fits] Anthropic's "Building effective agents" names five workflow patterns before it gets to agents .  SOURCES: BEA
A029. [3.1 Five workflow patterns, and when each fits] The post has been edited since December 2024: it now names Claude Haiku 4.5 and Sonnet 4.5 and says "Much of the tooling landscape described in this post has changed since December 2024" .  SOURCES: BEA
A030. [3.1 Five workflow patterns, and when each fits] Routing's example sends "easy/common questions to smaller, cost-efficient models like Claude Haiku 4.5", not to "highly quantized" models; quantization is a separate technique (ledger P8-02; Part 11) .  SOURCES: BEA
A031. [3.1 Five workflow patterns, and when each fits] And the evaluator-optimizer loop has no numeric quality threshold in the source; LangGraph's version loops "until an acceptable response is generated" .  SOURCES: LGD
A032. [3.1 Five workflow patterns, and when each fits] Since a judge may never be satisfied, the loop also needs an iteration cap, which is how Anthropic's post describes agents in general: "stopping conditions (such as a maximum number of iterations)" (ledger P8-03) .  SOURCES: BEA
A033. [3.2 Three ways to describe a workflow] That's two of three common models :  SOURCES: AFL, DBS, LGD, TDC
A034. [3.2 Three ways to describe a workflow] Airflow's model; its name comes from "the mathematical concept "directed acyclic graph"", and its code rejects a cycle with `AirflowDagCycleException` .  SOURCES: AFL
A035. [3.2 Three ways to describe a workflow] LangGraph's model, for "looping, stateful workflows" .  SOURCES: LGD
A036. [3.2 Three ways to describe a workflow] So the curriculum row that calls a LangGraph graph with conditional edges a "DAG" is imprecise (ledger P8-06) .  SOURCES: LGD
A037. [3.2 Three ways to describe a workflow] Temporal, DBOS and Restate run a normal function and record each step's result, so a restarted function skips what already happened .  SOURCES: DBS, RST, TDC
A038. [3.2 Three ways to describe a workflow] None of the four tools Gemini names is "the industry standard" in any source found (ledger P8-04): they do four different jobs, namely durable execution (Temporal), scheduled pipelines (Airflow), agent graphs (LangGraph) and a task queue (Celery) .  SOURCES: AFL, CEL, LGD, TDC
A039. [3.3 Checkpoints, threads and resuming] LangGraph runs a graph in **super-steps**: "a single iteration over the graph nodes", where nodes that run in parallel share one super-step .  SOURCES: LGD
A040. [3.3 Checkpoints, threads and resuming] It "creates a checkpoint at each super-step boundary", keyed by a thread: "When invoking a graph with a checkpointer, you **must** specify a `thread_id`" .  SOURCES: LGD
A041. [3.3 Checkpoints, threads and resuming] **When the checkpoint is written** is a setting, `durability` :  SOURCES: LGD, LGS
A042. [3.3 Checkpoints, threads and resuming] Code and side effects before the pause run again" .  SOURCES: LGD
A043. [3.3 Checkpoints, threads and resuming] So it advises: "Use idempotency keys, upserts, or read-before-write checks" .  SOURCES: LGD
A044. [3.3 Checkpoints, threads and resuming] One help: if several nodes run in one super-step and one fails, "the successful nodes' writes are already durable and don't need to be re-run on resume" (pending writes) .  SOURCES: LGD
A045. [3.3 Checkpoints, threads and resuming] Node caching is a separate, opt-in feature: you compile with a cache and give a node a `cache_policy`, whose key "defaults to a hash of the input with pickle" (ledger B1-03: overstated as a default) .  SOURCES: LGD, LGS
A046. [3.3 Checkpoints, threads and resuming] LangGraph raises `GraphRecursionError`, "Recursion limit of {n} reached without hitting a stop condition" .  SOURCES: LGS
A047. [3.3 Checkpoints, threads and resuming] It became 10,000 in 1.0.6 and is 10,007 in 1.2.x, read from the package source: `DEFAULT_RECURSION_LIMIT = int(getenv("LANGGRAPH_DEFAULT_RECURSION_LIMIT", "10007"))` .  SOURCES: LGH, LGS
A048. [3.3 Checkpoints, threads and resuming] LangGraph's own docs say "Starting in version 1.0.6, the default recursion limit is set to 1000 steps", which disagrees with the code .  SOURCES: LGD
A049. [3.4 Temporal: workflows as replayed code] **Activities** are ordinary functions that do "a single, well-defined action ... such as calling another service", model calls included .  SOURCES: TDC
A050. [3.4 Temporal: workflows as replayed code] **Workflow code** decides what happens next, and it must be deterministic: "any time your Workflow code is executed it makes the same Workflow API calls in the same sequence, given the same input" .  SOURCES: TDC
A051. [3.4 Temporal: workflows as replayed code] After a crash, Temporal runs the workflow function again from the top, and "the Commands that are emitted are compared with the existing Event History"; activities that already finished return their recorded results instead of running .  SOURCES: TDC
A052. [3.4 Temporal: workflows as replayed code] A mismatch gives "a _non-deterministic_ error", so workflow code can't branch on the clock or a random number except through the SDK's replay-safe versions .  SOURCES: TDC
A053. [3.4 Temporal: workflows as replayed code] | Activity retries | first wait 1 s, coefficient 2.0, longest wait 100 x the first (100 s), unlimited attempts |  |  SOURCES: TDC, TPS
A054. [3.4 Temporal: workflows as replayed code] | Workflow retries | none: "Workflow Executions do not retry by default" |  |  SOURCES: TDC
A055. [3.4 Temporal: workflows as replayed code] | Event history per run | 51,200 events or 50 MiB (warnings at 10,240 and 10 MiB) | docs and server code  |  SOURCES: TDC, TSV
A056. [3.4 Temporal: workflows as replayed code] | Waiting | "A Workflow can sleep for months" |  |  SOURCES: TDC
A057. [3.4 Temporal: workflows as replayed code] | Licence | MIT, server and Python SDK; Temporal Cloud is paid, "consumption-based" |  |  SOURCES: TDC, TPS, TSV
A058. [3.4 Temporal: workflows as replayed code] The history limit matters for agents: a long agent loop that records every model call as an event can hit it, which is why Temporal offers "continue-as-new", a fresh run that carries the state forward .  SOURCES: TSV
A059. [3.5 Retries, jitter and doing things once] Both official Python SDKs retry for you: `DEFAULT_MAX_RETRIES = 2` (three attempts in all), starting at 0.5 seconds and doubling to at most 8 seconds, on 408, 409, 429 and 5xx responses (anthropic 1.14.0, openai 3.31.0) .  SOURCES: ANS, OAI
A060. [3.5 Retries, jitter and doing things once] Their jitter is `1 - 0.25 * random()`, a delay cut by up to a quarter, though the code's comment says "plus-or-minus half a second" .  SOURCES: ANS
A061. [3.5 Retries, jitter and doing things once] Anthropic adds that a spend-cap 429 "has no retry-after header and keeps failing" .  SOURCES: ANE
A062. [3.5 Retries, jitter and doing things once] LangGraph's `RetryPolicy` defaults are 0.5 seconds, a factor of 2.0, a 128-second cap and 3 attempts "including the first", with jitter on (check L4) .  SOURCES: LGS
A063. [3.5 Retries, jitter and doing things once] Its default skips errors that retrying won't fix, such as `ValueError` and `TypeError` .  SOURCES: LGS
A064. [3.5 Retries, jitter and doing things once] AWS's analysis compared ways to spread them; its companion code defines **full jitter** as `sleep = random.uniform(0, min(cap, base * 2 ** attempt))` , and the post concludes "Equal Jitter" is "the loser" while "Full Jitter" uses "less work, but slightly more time" (a 2015 simulation of one contention model) .  SOURCES: AWB, AWC
A065. [3.5 Retries, jitter and doing things once] Stripe's version saves the "status code and body of the first request ... including 500 errors", takes keys "up to 255 characters", refuses a key reused with different parameters, and "you can remove keys from the system automatically after they're at least 24 hours old" .  SOURCES: STR
A066. [3.5 Retries, jitter and doing things once] One trap: the Anthropic and OpenAI SDKs generate an idempotency key for retries but don't send it (`_idempotency_header = None`), so model calls are not deduplicated .  SOURCES: ANS, OAI
A067. [3.5 Retries, jitter and doing things once] However, the Activity may be executed multiple times and may even partially complete more than once"; it calls the result an "effectively once" experience .  SOURCES: TDC
A068. [3.5 Retries, jitter and doing things once] Make sure your tasks are idempotent" .  SOURCES: CEL
A069. [3.5 Retries, jitter and doing things once] The messages come back after a visibility timeout, by default one hour on Redis .  SOURCES: CEL
A070. [3.6 Pausing for a person] | LangGraph 1.2.15 | `interrupt(value)` inside a node | `Command(resume=answer)` on the same thread | The node runs again from its start; answers match interrupts "strictly index-based"; don't wrap `interrupt` in try/except  |  SOURCES: LGD
A071. [3.6 Pausing for a person] | OpenAI Agents SDK 0.24.0 | A tool with `needs_approval=True`; calls appear in `result.interruptions` | `state = result.to_state()`, `state.approve(...)` or `state.reject(...)`, then `Runner.run(agent, state)` | `RunState` "is designed to be durable", but the docs say they "do not authenticate the snapshot or the person submitting it"  |  SOURCES: OAS
A072. [3.6 Pausing for a person] | Claude Agent SDK 0.2.167 | Hooks, deny and ask rules, the permission mode, allow rules, then the `canUseTool` callback | The callback's answer | "Auto-approved tools never reach `canUseTool`"; for checks on every call, "use a PreToolUse hook"  |  SOURCES: CAP
A073. [3.6 Pausing for a person] | Microsoft Agent Framework 1.22.0 | A function tool with `approval_mode="always_require"` | A function-approval response | The default is `"never_require"`  |  SOURCES: MAF
A074. [3.6 Pausing for a person] | CrewAI 1.15.28 | `@human_feedback` in a Flow (since 1.8.0) | `flow.resume(feedback)` | State is saved "automatically" when feedback is pending  |  SOURCES: CRW
A075. [3.6 Pausing for a person] | Temporal | The workflow waits on a condition (`workflow.wait_condition`) | A **signal** ("an asynchronous message ... to change its state") or an **update** ("a trackable synchronous request") | Built for waits of days  |  SOURCES: TDC, TPS
A076. [3.6 Pausing for a person] Use the interrupt function instead" (ledger B1-07: corrected) .  SOURCES: LGD
A077. [3.6 Pausing for a person] CrewAI's `@human_feedback` and its opt-in checkpointing make Gemini's "less structural durability" claim (ledger B1-06) unsupported: no source compares the two .  SOURCES: CRW
A078. [3.6 Pausing for a person] OpenAI's docs make the same point about `RunState` .  SOURCES: OAS
A079. [3.6 Pausing for a person] Anthropic's post on Claude Code's auto mode reports that users "approve 93% of permission prompts" and names the risk, "approval fatigue, where people stop paying close attention to what they're approving"; the post doesn't say what data the 93% comes from .  SOURCES: AAM
A080. [3.6 Pausing for a person] Its fix is a classifier that decides instead, with its own errors: 0.4% false positives on 10,000 real actions and 17% false negatives on 52 real "overeager" actions, which the post calls "the honest number" .  SOURCES: AAM
A081. [3.6 Pausing for a person] A 2012 systematic review of clinical decision support (74 studies) found that over-reliance on automation grows with workload, task complexity and time pressure, and that accountability and training reduce it .  SOURCES: GRW
A082. [3.6 Pausing for a person] **The law, where it applies.** The EU AI Act requires that high-risk AI systems "shall be designed and developed" for effective human oversight, including staying aware of automation bias and being able to override or stop the system (Article 14) .  SOURCES: EUA
A083. [3.6 Pausing for a person] In the consolidated text as of July 27, 2026, which includes the "Digital Omnibus" amendments, those duties apply from December 2, 2027 for the Annex III high-risk uses and August 2, 2028 for Annex I products; the 2024 text's earlier dates are out of date .  SOURCES: EUA
