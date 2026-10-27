# frontier-a5-a6: what is new on Axis 5 (Orchestration and Grounding) and Axis 6 (Optimization)
Date of check: 2026-10-15. Status: COMPLETE. Lookups used: 24 of 24 (cap reached). Pages opened by me; no PDFs downloaded.
Window: published or substantially updated 2025-07-01 to 2026-10-15. None of the sources below is in the manual's Works Cited (checked by Grep on arXiv IDs, titles and post names: zero hits).
Manual coverage I read first: sections 11.1-11.7 (Axis 5) and 12.1-12.8 (Axis 6), including the multi-agent text in 11.5, the thin MCP/caching paragraph in 11.6, the one-paragraph memory/skills/subagents section 11.7, and the GEPA, UPA and LPO sections.
Final numbering: F01-F04 are Axis 5, F05-F08 are Axis 6.

How I read numbers: WebFetch passes each page through a small model, so every figure below is a second-hand reading of the page text. "abs" means the arXiv abstract page, "html" means the arXiv HTML version. Percent signs are copied as printed; where a paper does not say whether it means points or relative change, I say so. Several of these papers changed numbers between versions, so I cite the version I read.

## AXIS 5

### F01  Multi-agent systems help on parallel work and hurt on sequential work
- Source: Kim and 18 co-authors, "Towards a Science of Scaling Agent Systems", arXiv 2512.08296, v1 2025-12-09, v3 2026-04-08. https://arxiv.org/abs/2512.08296 . No venue listed.
- Measured: 5 architectures (1 single agent, 4 multi-agent), 3 model families, 260 configurations (v1 had 180), six benchmarks: BrowseComp-Plus, Finance-Agent, PlanCraft, Workbench, SWE-bench Verified, Terminal-Bench. Models: GPT-5-nano/mini/5, Gemini 2.0 Flash / 2.5 Flash / 2.5 Pro, Claude Sonnet 3.7 / 4 / 4.5.
- Key numbers with scope (html v3): Finance-Agent, centralized coordination +80.8% over a single agent (mean 0.631 vs 0.349; the v1 abstract said +80.9%). PlanCraft, every multi-agent variant worse, -70% to -39%. Tasks where a single agent already scores above 45% get negative returns from added agents. Independent agents amplify errors 17.2x, centralized coordination 4.4x.
- Not verified: the abstract says the fitted model picks the best architecture for 87% of held-out configurations; a search snippet said the later version has a lower cross-validated R2 (0.373). I did not open that, so do not quote the 87% in the manual.
- Evidence class: preprint.
- What an everyday advanced user does differently: start with one agent. Use several agents only when the subtasks are independent (research across many sources, parallel analyses) and give them an orchestrator that checks results. Keep step-by-step planning and tool-heavy work in one agent. If one agent already does well, extra agents more likely hurt.
- Manual change: yes. 11.5 has debate and pass^k but no measured "when multi-agent helps" rule. Add one paragraph with the two scoped numbers; cite v3 and note numbers moved slightly between versions.

### F02  Repository context files (AGENTS.md, CLAUDE.md) do not reliably help coding agents
- Source: Gloaguen, Mundler, Muller, Raychev, Vechev, "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?", arXiv 2602.11988, v1 2026-02-12, v2 2026-06-23, v3 2026-09-29. https://arxiv.org/abs/2602.11988 . No venue listed.
- Measured: Claude Code (Sonnet 4.5), Codex (GPT-5.2, GPT-5.1 mini) and Qwen Code (Qwen3-30B-coder) on SWE-bench Lite (300 tasks, 11 repositories, LLM-generated context files) and on the authors' CTXbench (138 instances, 12 repositories, developer-written files). The text says "four coding agents" but I could see three named. Search snippets used another name for the benchmark (AGENTbench); I used the html v3 name.
- Key numbers with scope (html v3; units as printed): LLM-generated files change the resolution rate by -0.5% (SWE-bench Lite) and -2% (CTXbench), neither significant. Developer-written files +2.4% on average (p=21%, CTXbench only). Cost up 20% (SWE-bench Lite) and 23% (CTXbench) for LLM-generated files, at most 19% for developer-written. Warning: a search summary of v1 gave -3% and +4%, so the headline moved between versions; cite v3.
- Evidence class: preprint.
- What to do differently: do not run /init and keep the generated file. Keep a developer-written file to what the agent cannot get from the README (build and test commands, non-standard practices) and drop repository overviews. Test with and without the file on your own tasks.
- Manual change: yes. 11.7 presents persistent instruction files as the frontier but has no evidence that they help. Add this result.

### F03  Skills: curated ones help, self-written ones hurt, short ones beat long ones
- Source: Li and 76 co-authors, "SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks", arXiv 2602.12670, v1 2026-02-13, v4 2026-06-14. https://arxiv.org/abs/2602.12670 . No venue listed.
- Measured: 87 tasks, 8 domains, 18 model-harness configurations (Claude Code, Codex CLI, Gemini CLI, OpenHands), each with and without Skills.
- Key numbers with scope (v4; headline from abs, rest from html): curated Skills raise the average pass rate from 33.9% to 50.5% (+16.6 points; per-configuration range +4.1 to +25.7). Self-generated Skills land below the no-Skills baseline on all three main configurations: -8.1 points (Claude Code + Opus 4.7), -11.3 (Codex + GPT-5.5), -11.5 (Gemini CLI + Gemini 3.1 Pro). 2-3 Skills give +19.0 points, 4 or more only +10.1, comprehensive documentation +0.7. 13 of 87 tasks got worse with Skills. Biggest gain Natural Science (+28.8), smallest Mathematics and OR (+9.7). MiniMax M2.7 with Skills (34.9%) beats OpenHands + GLM 5.1 without (32.7%). v1 used 84 tasks and a +16.2 headline (search snippet), so cite v4.
- Evidence class: preprint.
- What to do differently: write or edit skills by hand from real procedure knowledge; do not ask the model to write its own skill and trust it. Keep each skill focused. Test each skill with and without it, because about 1 task in 7 got worse.
- Manual change: yes. 11.7 mentions skills only as a concept. Add this evidence. It also supports the skill-building kit (hand-curated, focused, tested).

### F04  Fewer tool definitions in context: tool search, programmatic tool calling, tool examples (vendor numbers)
- Source: Anthropic Engineering, "Introducing advanced tool use on the Claude Developer Platform", 2025-11-24, https://www.anthropic.com/engineering/advanced-tool-use ; and "Code execution with MCP: building more efficient AI agents", 2025-11-04, https://www.anthropic.com/engineering/code-execution-with-mcp . I opened both.
- Measured (Anthropic internal testing; no public task list, not independently replicated): with a Tool Search Tool, MCP evaluation accuracy Opus 4 49% to 74%, Opus 4.5 79.5% to 88.1%. Programmatic tool calling: average tokens on complex research tasks 43,588 to 27,297 (-37%); accuracy 25.6% to 28.5% (internal knowledge retrieval) and 46.5% to 51.2% (GIA benchmarks). Tool use examples: 72% to 90% on complex parameter handling. Code execution post: one Google Drive to Salesforce workflow, 150,000 tokens to 2,000 (98.7%), with the caveat that generated code needs a sandbox, resource limits and monitoring.
- Evidence class: vendor documentation (engineering posts, internal measurements).
- What to do differently: do not attach every MCP server to every session. With many tools, use tool search so only names load first. For multi-step tool chains, let the model write code that calls the tools so intermediate results stay out of the context window. Put one to three worked examples of tricky parameters in the tool definition.
- Manual change: yes, small. 11.6 says MCP was widely adopted but gives no tool-count guidance. Add one sentence with these numbers marked as vendor-reported.

## AXIS 6

### F05  Evolving playbooks (ACE): grow a structured context from execution feedback instead of rewriting it
- Source: Zhang and 12 co-authors, "Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models", arXiv 2510.04618, v1 2025-10-06, v3 2026-03-29. https://arxiv.org/abs/2510.04618 . The arXiv comment line says ICLR 2026; I did not open the venue page.
- Measured: a Generator, Reflector and Curator, all the same model (DeepSeek-V3.1 in the main tables), build and update a context "playbook" with small incremental edits. Benchmarks: AppWorld (agent tasks), finance (FiNER and Formula); medical and SQL in the appendix.
- Key numbers with scope (html v3, authors' own comparisons, percent as printed): abstract headline +10.6% on agents, +8.6% on finance. AppWorld offline: ReAct + ACE beats ReAct + ICL by 12.3% and ReAct + GEPA by 11.9%. Without labels, +14.8% over the ReAct baseline. Online, +7.6% over Dynamic Cheatsheet. Finance offline: +10.9% on average over ICL, MIPROv2 and GEPA. Cost: 82.3% less adaptation latency and 75.1% fewer rollouts than GEPA (AppWorld offline).
- Limits stated by the authors: needs a reasonably strong Reflector and a reliable feedback signal; without one, the playbook can be polluted by misleading signals.
- Evidence class: peer-reviewed (ICLR 2026 per arXiv comments).
- What to do differently: for a task you repeat (a recurring report, an agent workflow), keep a running playbook of short, itemised lessons and add or edit single items after each run, using hard signals (tests passed, tool errors, a checker) rather than the model's own opinion. Do not ask the model to rewrite or summarise the whole playbook each time; the paper names two failure modes, brevity bias and context collapse.
- Manual change: yes. 12.5 and 12.7 treat prompt optimization as search over a single prompt. Add ACE as the context-level alternative and as a bridge to 11.7.

### F06  Optimizing a skill file with GEPA gave a gain that could not be told apart from noise
- Source: Kozyrev, Kozyrev, Podkopaev, "Skill Issue: Lessons from Optimizing Repository SKILLs for Coding Agents", arXiv 2609.12742, v1 2026-09-11. https://arxiv.org/abs/2609.12742 . No venue listed.
- Measured: three Kotlin repositories (kotest, ktor, koog), tasks mined from reverted merged pull requests, Claude Code with Sonnet 4.6. A candidate skill document is scored by whether the same agent does better with it than without. Optimizers compared: GEPA and SkillOpt.
- Key numbers with scope: GEPA +4.9 points on average over an empty document; SkillOpt +0.1 points. At the size of one repository's task set the authors say the gain cannot be separated from run-to-run variance; no run reaches p = 0.05, best p = 0.29 (html). Per-repository cells I read did not average to 4.9 (units unclear), so I do not report them. The authors say optimized documents read better than the score suggests, and a maintainer found project knowledge in them.
- Evidence class: preprint, small scale.
- What to do differently: if you tune a skill file or instruction file with an optimizer, run each version several times and compare on tasks the optimizer never saw; a few points of gain on a few dozen tasks is within noise. Read the result and review it like a pull request.
- Manual change: yes, small. Add to 12.5 as a scoped caution: GEPA's gains are measured on benchmark tasks; on a real repository a few points were not significant. The manual's GEPA figures stay valid.

### F07  GEPA stayed near the base model on math reasoning; choosing a few high-variance training prompts did better
- Source: Gao and 5 co-authors, "p1: Better Prompt Optimization with Fewer Prompts", arXiv 2604.08801, v1 2026-04-09, v2 2026-08-26. https://arxiv.org/abs/2604.08801 . No venue listed (a search snippet said "under review").
- Measured: system-prompt optimization on reasoning benchmarks. Response model Qwen3-4B-Instruct-2507 (Qwen3-1.7B also used). Train on AIME 24 prompts; test on AIME 25 and 26 and HMMT 25 and 26.
- Key numbers with scope (html v2 Table 1, second-hand reading of a table; AIME 25 accuracy): base 47.03; GEPA variants 46.35 to 46.87; full-dataset RL 47.24; p1 trained on two chosen prompts ([1, 23]) 54.01. HMMT 25: base 40.68, p1 45.42, GEPA 40.10 to 40.57. The result depends on which prompts are chosen: another single-prompt p1 run ([25]) scored 44.95, below the base. The authors explain: when variation between responses outweighs variation between candidate prompts, optimization gets no signal, and more training prompts can shrink the between-prompt signal.
- Evidence class: preprint, one small response model.
- What to do differently: do not assume a prompt optimizer improves a model on hard math or reasoning tasks; compare against the unoptimized prompt on a held-out set. If you do optimize, a small set of training examples where candidate prompts disagree can work better than a big set, but the choice of examples is itself a risk.
- Manual change: yes, small. 12.5 reports GEPA +12% on AIME-2025 over MIPROv2 on Qwen3 8B (verified earlier). Add that another group found GEPA close to the unoptimized base on AIME and HMMT with a 4B model, so the AIME gain is setup-specific.

### F08  Optimizers differ little on average, but they can bloat and game prompts
- Source: Singhal, Tambwekar, Maamari, "PrefPO: Pairwise Preference Prompt Optimization", arXiv 2603.19311, v1 2026-03-13, v2 2026-03-24. https://arxiv.org/abs/2603.19311 . No venue listed. The authors built PrefPO, so this is a head-to-head by the method's authors.
- Measured: nine BIG-Bench Hard tasks plus IFEval-Hard (authors' own subset). Task model GPT-4o; optimizer and discriminator GPT-5; GPT-4.1 as judge for hygiene and hacking. Compared with GEPA, MIPROv2 and TextGrad.
- Key numbers with scope (html v2 Table 1, BBH mean accuracy over nine tasks): PrefPO 0.875, MIPROv2 0.873, GEPA 0.870, TextGrad 0.850. The top three are within 0.5 points, so I read it as a tie; the abstract's "matches or exceeds on 6/9 tasks" is looser than the table, where PrefPO is above GEPA on 4 of 9. TextGrad prompts grew up to 14.7x the starting length (PrefPO 4.7x); MIPROv2 prompts contained 34% repetitive text (PrefPO 1.4%); prompt hacking rate 86% for TextGrad vs 37% for PrefPO (LLM-judged). On IFEval-Hard TextGrad scored 84.5% vs 82.4% for PrefPO (abs).
- Evidence class: preprint.
- What to do differently: after any automatic optimization, read the winning prompt. Check its length against the original, look for repeated text, and check whether it hard-codes answers or tricks for the test set. Do not pick an optimizer on a one-point gap.
- Manual change: optional. 12.4 failure modes mention a gameable metric; add the measured bloat and hacking rates as one sentence, marked as from the method's authors.

## Practical takeaways
1. Start with one agent; add agents only for independent subtasks, with an orchestrator. Source: Kim et al., arXiv 2512.08296 (+80.8% on Finance-Agent, -70% to -39% on PlanCraft).
2. Hand-write short, focused skills and instruction files, and test with and without them. Self-written skills scored 8 to 11.5 points below no skills; 2-3 focused skills +19.0 vs +10.1 for four or more; generated AGENTS.md files did not help and cost about 20% more. Sources: Li et al., arXiv 2602.12670 (v4); Gloaguen et al., arXiv 2602.11988 (v3).
3. Keep tool definitions out of context until needed: use tool search for large tool sets and let the model call tools from code for multi-step work. Source: Anthropic Engineering, advanced tool use (2025-11-24) and code execution with MCP (2025-11-04); vendor-reported numbers.
4. Treat prompt-optimizer gains as small and noisy until checked on held-out tasks with repeated runs, and read the optimized prompt for bloat and gaming. Sources: Kozyrev et al., arXiv 2609.12742 (+4.9 points, not significant); Gao et al., arXiv 2604.08801 (GEPA near base on AIME with a 4B model); Singhal et al., arXiv 2603.19311 (top optimizers within 0.5 points; TextGrad prompts up to 14.7x longer).
5. For repeated work, keep a running playbook updated in small itemised edits from hard feedback, not whole-file rewrites. Source: Zhang et al., arXiv 2510.04618 (ICLR 2026 per arXiv comments); it needs a strong reflector and reliable feedback.

## Not covered (not reached within the 24-lookup cap)
RAG and contextual retrieval updates, agent memory benchmarks and products, MCP specification changes, agent reliability (pass^k follow-ups), and other vendors' agent documentation. I did not search these, so "nothing new" must not be read for them.

## Manual claims checked along the way
None. I read the manual to avoid duplicates and did not re-check any manual figure, so the findings list is empty. F07 and F05 note scope for the manual's existing GEPA text rather than correcting it.
