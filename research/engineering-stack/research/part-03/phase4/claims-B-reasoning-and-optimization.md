# Claims to check

Each numbered claim cites source keys. Sources are listed at the end.

1. **T04, prompt optimization.** Instead of rewriting a prompt by hand and guessing, a program tries many versions (different instructions, different examples), scores each on test cases with your metric, and keeps the best .  [sources: DSD, MIP]
2. | A program that searches for a better prompt against a metric | Prompt optimizer | DSPy calls them optimizers, formerly "teleprompters" . |  [sources: DSD]
3. | A typed description of a task's inputs and outputs | Signature (DSPy) | "a declarative specification of input/output behavior" . |  [sources: DSD]
4. | One run of the program on one example, during a search | Rollout; trial | The GEPA paper counts rollouts . |  [sources: GEP]
5. **DSPy's pieces** (version 3.4.0, MIT, Python 3.10 to below 3.15 ).  [sources: PYPI]
6. 1. A **signature** says what goes in and what comes out .  [sources: DSD]
7. 2. A **module** runs it; all built-in modules are built on `dspy.Predict` .  [sources: DSD]
8. 3. A **metric** is a function of an example and a prediction that "outputs a `float` (or `int` or `bool`) score" .  [sources: DSD]
9. 4. An **optimizer** tunes "the prompts and/or the LM weights" to raise the metric; you run it with `.compile(program, trainset=...)` .  [sources: DSD]
10. **Three optimizers, in order of cost** :  [sources: DSD]
11. - **MIPROv2** ("Multiprompt Instruction PRoposal Optimizer Version 2") also writes candidate instructions, then searches combinations of instructions and examples "using Bayesian Optimization" , implemented with Optuna's tree-structured Parzen estimator .  [sources: DSD, DSR, MIP]
12. Its presets: `light` tries 6 candidates against up to 100 validation examples, `medium` 12 and 300, `heavy` 18 and 1,000 .  [sources: DSR]
13. The docs suggest it for 200 or more examples, "to prevent overfitting" .  [sources: DSD]
14. - **GEPA** ("Genetic-Pareto") has a second model read the program's traces and written feedback, propose new instructions, and keep every candidate that is best on at least one validation example (a Pareto front) .  [sources: DSD, GEP]
15. It needs that second, "reflection" model .  [sources: DSD]
16. **What they reported.** MIPRO, on Llama-3-8B, ScoNe test set (exact match): 69.1 unoptimized to 79.4, +10.3 points .  [sources: MIP]
17. In the same table, demos-only BootstrapFewShot with random search beat MIPRO on two of the tasks .  [sources: MIP]
18. GEPA's aggregate over six benchmarks: +7.01 points over MIPROv2 with Qwen3 8B and +6.55 with GPT-4.1 Mini .  [sources: GEP]
19. Against GRPO, a reinforcement-learning method that changes the model's weights, GEPA used 1,839 to 7,051 rollouts per benchmark where GRPO used 24,000 (3.4x to 13.1x fewer), and GRPO still scored higher on AIME-2025 (38.00 against 32.00) .  [sources: GEP]
20. **What they cost.** DSPy's docs say a single GEPA or MIPROv2 run "can spend hundreds of dollars in LM calls" ; the RAG tutorial's MIPROv2 run cost "around $1.5" with gpt-4o-mini .  [sources: DSD]
21. **The trap: overfitting.** DSPy's docs recommend a 20% training and 80% validation split for most prompt optimizers, because they "often overfit to small training sets" .  [sources: DSD]
22. The MIPRO paper's appendix reports that proposers tend to fit instructions to the few-shot examples .  [sources: MIP]
23. | Tools: OpenAI API, Anthropic Workbench, DSPy, Promptfoo (P1-08) | Confirmed. The Workbench needs a login to the Claude Console , and its usage is "billed via prepaid usage credits", the same credits as the API . DSPy 3.4.0 is current . promptfoo: Part 02 | 6 |  [sources: AWB, AWP, PYPI]
24. | MIPROv2 stands for "Multiprompt Instruction PRoposal Optimizer Version 2" (P9-06) | Confirmed . The paper calls it MIPRO | 3.7 |  [sources: DSD, MIP]
25. | MIPROv2 uses Bayesian optimization over instructions and few-shot examples (P9-07) | Confirmed: Optuna's tree-structured Parzen estimator, scored on minibatches | 3.7 |  [sources: DSR, MIP]
26. | GEPA "frequently" scores higher with "vastly fewer" rollouts (P9-08) | Overstated. Neither word is in the abstract, which says GEPA beats GRPO "by 6% on average" with "up to 35x fewer rollouts" . Per benchmark, 3.4x to 13.1x fewer; GRPO won on AIME-2025 | 3.7 |  [sources: GEP]
27. | MIPROv2 raises validation exact-match accuracy "by 15%" (P9-11) | Unsupported. No source has 15%. The nearest figure is ScoNe's test set with Llama-3-8B: +10.3 points, 14.9% relative; the abstract says "as much as 13% accuracy" | 3.7 |  [sources: MIP]
28. 5. **Prompt optimization on an agent** (DSPy tutorial "Agents"): MIPROv2 raised a Llama-3.2-3B ReAct agent's recall on 100 dev examples from 8.0% to 41.7%, at a stated cost of about $5 .  [sources: DSD]
29. 6. **Gains that varied** (Lemos et al., preprint): DSPy optimization's effect "varies by task"; in one case the optimized prompt did not help a cheaper model .  [sources: LEM]
30. Checked October 12, 2026. Versions from PyPI .  [sources: PYPI]
31. | DSPy | Prompt optimization | MIT | Free; optimizer runs pay for model calls | Python 3.10 to below 3.15; about 400 MB installed | A model: hosted (key) or local (Ollama) . None for `DummyLM` tests | 3.4.0, September 25, 2026 | PyPI, `dspy` |  [sources: DSD]
32. **Telemetry and network.** No telemetry code was found in DSPy's source; it sets LiteLLM's `telemetry` off when it loads it .  [sources: DSR]
33. It fetches a model price list from GitHub once, on the first price lookup, unless `LITELLM_LOCAL_MODEL_COST_MAP=true` is set .  [sources: DSR]
34. - **For prompt optimization:** DSPy, starting with BootstrapFewShot; MIPROv2 or GEPA only with a few hundred examples, a budget cap, and a test set the search never touches .  [sources: DSD]
35. Expect `8 of 8 checks passed.`, then `9 of 9 checks passed.` [T on Linux with Python 3.11.17, 3.12.3 and 3.13.16]. `requirements-dspy.txt` pins versions without hashes, because DSPy brings about 70 packages and the file says so. It picks numpy 2.5.4 on Python 3.12 or later and 2.4.4 on 3.11, because numpy 2.5.4 needs Python 3.12 .  [sources: PYPI]
36. 8. **Optional:** the Pydantic and DSPy checks (Section 7.4). The DSPy check compiles a tiny program with `DummyLM`, which returns scripted answers : BootstrapFewShot keeps 2 of 3 training runs as examples, because the scripted answer for the third is wrong and the metric rejects it .  [sources: DSR]
37. - DSPy, "Optimizers" (in the repository's docs): https://github.com/stanfordnlp/dspy  [sources: DSD]
38. - Opsahl-Ong et al., MIPRO (EMNLP 2024): https://aclanthology.org/2024.emnlp-main.525/  [sources: MIP]
39. - Agrawal et al., GEPA (ICLR 2026): https://arxiv.org/abs/2507.19457  [sources: GEP]
40. - **Optimizer gains are scoped.** The headline numbers come from the method authors, on their chosen tasks and models .  [sources: GEP, MIP]
41. Independent evidence is thin: one preprint found gains that "varies by task" , and a peer-reviewed revisit found OPRO "shows limited effectiveness in small-scale LLMs" .  [sources: LEM, ROP]
42. - **Optimized prompts may not transfer.** GEPA's prompts optimized on Qwen3 8B kept most of their gain on GPT-4.1 Mini ; Lemos et al. saw no gain moving an optimized prompt to a cheaper model .  [sources: GEP, LEM]
43. **T03, reasoning models.** Some models think before they answer: they write hidden working-out first, then the reply. Both vendors let you set how much: Anthropic with an `effort` setting, OpenAI with `reasoning.effort` .  [sources: AEF, ORS]
44. | Hidden working-out a model writes before its answer | Thinking; reasoning tokens | Billed as output even when hidden . |  [sources: ATK, ORS]
45. - **Adaptive thinking with an effort setting** is the current way: `thinking: {type: "adaptive"}` and `output_config: {effort: ...}`, with `low`, `medium`, `high`, `xhigh` and `max` .  [sources: AEF, AXT]
46. Claude Opus 5.5 and Haiku 5.5 default to `medium`; other models default to `high` .  [sources: AEF]
47. - **The older token budget is retired.** `thinking: {type: "enabled", budget_tokens: N}` is deprecated on the Claude 4.6 models, and "Claude 4.7 and later models do not support it" (they return a 400 error) .  [sources: AXT]
48. - **Thinking is on by default** on the 5.x-era models, including Opus 5.5, Sonnet 5.5 and Haiku 5.5 .  [sources: ATK]
49. - **You may not see the thinking.** On newer models the default display is `omitted`, and "No display setting returns the raw chain of thought" .  [sources: ATK]
50. It is "billed as output tokens, even when the thinking text isn't returned" .  [sources: ATK]
51. - **Sampling settings are locked.** On the 5.x-era models, any `temperature`, `top_p` or `top_k` other than the default returns a 400 error on every request .  [sources: ATK]
52. The API reference marks all three as deprecated for models released after Claude Opus 4.6 .  [sources: ANT]
53. - **With tools,** thinking blocks must be passed back "complete and unmodified" .  [sources: ATK]
54. - `reasoning.effort` takes model-dependent values that "can include none, minimal", up to `max` .  [sources: OAPI, ORS]
55. - "we don't expose the raw reasoning tokens"; you can ask for a summary (`auto`, `concise` or `detailed`) .  [sources: ORS]
56. Reasoning tokens are billed as output, and the guide suggests "reserving at least 25,000 tokens for reasoning and outputs" when you start .  [sources: ORS]
57. - Reasoning models take developer messages, which are "prioritized ahead of user messages" .  [sources: ORB, OTX]
58. - OpenAI: prompting them to "think step by step" is "unnecessary"; keep prompts simple and try zero-shot first .  [sources: ORB]
59. Give "a clear goal, strong constraints, and an explicit output contract"; effort is a tuning knob, not the main fix for quality .  [sources: ORS]
60. - Anthropic: "think thoroughly" "often produces better reasoning than a hand-written step-by-step plan"; worked examples "shape how Claude approaches similar problems"; lower the effort if the model overthinks .  [sources: ABP]
61. | Separate system, user and assistant roles (P1-13) | Confirmed, with a caveat. OpenAI says developer messages are "prioritized ahead of user messages" by its Model Spec, a trained priority, not code . The Anthropic page read states no priority rule | 3.6 |  [sources: ABP, OTX]
62. - *"Put 'think step by step' in every prompt."* For reasoning models, OpenAI calls it "unnecessary" ; test it on your model (taxonomy §9.1).  [sources: ORB]
63. (4) A small validation set rewards prompts that fit its quirks; the toy's winner fell to 41.7% on new tickets . (5) A 400 error: the 5.x-era models reject any non-default temperature .  [sources: ATK]
64. 2. The skill reference skills/sophisticated-prompt-generator/references/seven-axis-checklist.md suggests a low temperature for single-answer tasks, and claude/new-skills-appendix.md says the generator's expander emits "low-temperature settings for structured output". On Claude's 5.x-era models any non-default temperature is rejected .  [sources: ATK]

## Sources

- ABP: Anthropic, "Prompting best practices". https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices (class OD)
- AEF: Anthropic, "Effort". https://platform.claude.com/docs/en/build-with-claude/effort (class OD)
- ANT: Anthropic, "Create a Message", API reference. https://platform.claude.com/docs/en/api/messages/create (class OD)
- ATK: Anthropic, "Thinking". https://platform.claude.com/docs/en/build-with-claude/thinking (class OD)
- AWB: Anthropic Help Center, "How do I use the Workbench?" (date shown July 16, 2026). https://support.claude.com/en/articles/8606378-how-do-i-use-the-workbench (class OD)
- AWP: Anthropic Help Center, "How do I pay for my API usage?". https://support.claude.com/en/articles/8977456-how-do-i-pay-for-my-api-usage (class OD)
- AXT: Anthropic, "Extended thinking". https://platform.claude.com/docs/en/build-with-claude/extended-thinking (class OD)
- DSD: DSPy documentation in the repository at commit 1dcdf86 (github.com/stanfordnlp/dspy, docs/docs/): learn/programming/signatures.md, modules.md, language_models.md; learn/evaluation/metrics.md; learn/optimization/optimizers.md, overview.md; diving-deeper/choosing-an-optimizer.md; api/optimizers/MIPROv2.md, GEPA/overview.md; tutorials agents, rag (class OD)
- DSR: DSPy 3.4.0 source (PyPI wheel and repository): dspy/utils/dummies.py, teleprompt/mipro_optimizer_v2.py, clients/_litellm.py, clients/model_metadata/__init__.py (class OD)
- GEP: Agrawal et al., "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning", ICLR 2026 (Oral). https://arxiv.org/abs/2507.19457 (v2); https://iclr.cc/virtual/2026/oral/10009494 (class PR)
- LEM: Lemos, Alves and Ferraz, "Is It Time To Treat Prompts As Code?", arXiv 2507.03620v1, July 2025 (class PP)
- MIP: Opsahl-Ong et al., "Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs", EMNLP 2024, pp. 9340-9366, DOI 10.18653/v1/2024.emnlp-main.525. https://aclanthology.org/2024.emnlp-main.525/ ; arXiv 2406.11695v2 (class PR)
- OAPI: OpenAI's OpenAPI specification, openapi.yaml at the 2026-10-09 commit (github.com/openai/openai-openapi): `logit_bias`; `CreateResponse`; `ReasoningEffort` (class OD)
- ORB: OpenAI, "Reasoning best practices". https://developers.openai.com/api/docs/guides/reasoning-best-practices (class OD)
- ORS: OpenAI, "Reasoning models". https://developers.openai.com/api/docs/guides/reasoning (class OD)
- OTX: OpenAI, "Text generation", section on message roles. https://developers.openai.com/api/docs/guides/text (class OD)
- PYPI: PyPI JSON API, https://pypi.org/pypi/PACKAGE/json, read October 12, 2026 (class OD)
- ROP: Zhang et al., "Revisiting OPRO: The Limitations of Small-Scale LLMs as Optimizers", Findings of ACL 2024, pp. 1727-1735. https://aclanthology.org/2024.findings-acl.100/ (class PR)
