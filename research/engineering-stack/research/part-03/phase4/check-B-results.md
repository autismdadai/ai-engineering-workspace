# Check B results (claims B: reasoning and optimization)
Note: DSPy docs read at repository HEAD (81a41fd, 2026-10-12); commit 1dcdf86 could not be fetched from a shallow clone, so doc wording is checked against HEAD. DSPy source from the 3.4.0 wheel.

| # | Verdict | Evidence (source words, location) | Note |
|---|---|---|---|
| 1 | supported | MIPRO Sec. 4 / DSD optimizers.md: optimizers propose instructions+demos, score on metric | general description |
| 2 | supported | optimizers.md:5 "DSPy Optimizers (formerly Teleprompters)" | |
| 3 | supported | signatures.md:9 "a declarative specification of input/output behavior" | "typed" is the author's gloss |
| 4 | supported | GEPA Sec. 2 "rollouts, concretely, invocations of Phi plus evaluation by mu" | |
| 5 | supported | PyPI: version 3.4.0, license MIT, requires_python "<3.15,>=3.10" | |
| 6 | supported | signatures.md:9 | |
| 7 | supported | modules.md:18 "all other DSPy modules are built using `dspy.Predict`" | |
| 8 | supported | metrics.md:23 "outputs a `float` (or `int` or `bool`) score" | |
| 9 | supported | optimizers.md:8 "the prompts and/or the LM weights"; `.compile(..., trainset=...)` at :107 | |
| 10 | partly supported | choosing-an-optimizer.md: "Zero-config baselines ... cost almost nothing. Search-based optimizers (BootstrapRS, MIPROv2, GEPA) cost real money." | Docs give no cost ordering of BootstrapFewShot < MIPROv2 < GEPA; MIPROv2 and GEPA are grouped together. "In order of cost" is the author's inference |
| 11 | supported | MIPROv2.md "using Bayesian Optimization"; mipro_optimizer_v2.py:658 `optuna.samplers.TPESampler(seed=seed, multivariate=True)`; MIPRO paper "Optuna's implementation of the Tree Structured Parzen Optimizer" | Optuna is an optional extra (`dspy[optuna]`), not installed by default |
| 12 | supported | mipro_optimizer_v2.py:47-49 light n=6 val_size=100; medium 12/300; heavy 18/1000 | "n" is used to compute trial count; val_size caps the validation subset |
| 13 | supported | optimizers.md:90 "200 examples or more to prevent overfitting" | |
| 14 | supported | GEPA overview.md:3, :105 "set of candidates which achieve the highest score on at least one evaluation instance" | |
| 15 | supported | gepa.py docstring "reflection_lm ... Required parameter" (or a custom instruction_proposer) | |
| 16 | supported | MIPRO Table 2 ScoNe test: Baseline 69.1, MIPRO 79.4 (+10.3) | "exact match" metric label not seen in the text read |
| 17 | supported | Table 2 test: Bootstrap RS beats MIPRO on Iris (94.1 v 88.6) and Heart Disease (79.2 v 74.2) | paper gives no count; this is a table reading (2 of 7) |
| 18 | supported | GEPA Table 1 Qwen3 8B MIPROv2 47.84, GEPA 54.85; Table 2 GPT-4.1 Mini 58.67, 65.22 | differences recomputed: 7.01 and 6.55. These are GEPA (not GEPA+Merge) rows. Abstract itself says "over 10%" |
| 19 | supported | Table 1 rollouts "6871 3593 7051 2426 1839 1839", GRPO 24000; AIME-2025 GRPO 38.00, GEPA 32.00 | 24000/7051=3.40, 24000/1839=13.05 (13.1). The rollout row is shared "GEPA (+Merge)". Paper itself does not state 3.4x to 13.1x; abstract says up to 35x |
| 20 | supported | choosing-an-optimizer.md #9 "can spend hundreds of dollars in LM calls"; rag ipynb "cost around $1.5 (for the `medium` auto setting)" | |
| 21 | supported | overview.md:8 "20% for training, 80% for validation ... often overfit to small training sets" | same paragraph says GEPA follows the opposite convention; claim says "most", fine |
| 22 | supported | MIPRO App. H "the tendency to overfit instructions to the few-shot examples provided in the meta-prompt" | paper adds such instructions may still help |
| 23 | supported | AWB: "Log in to the Claude Console" (July 16, 2026); AWP: "Claude API and Workbench usage is billed via prepaid "usage credits."" ; PyPI latest 3.4.0 | AWB itself has no billing text; billing is in AWP. Source has inner quote marks around "usage credits" |
| 24 | supported | MIPROv2.md line 3 full expansion; paper calls it MIPRO | |
| 25 | supported | TPESampler (code); MIPRO paper "evaluating over minibatches" | |
| 26 | supported | arXiv abstract "outperforms GRPO by 6% on average and by up to 20%, while using up to 35x fewer rollouts"; "frequently"/"vastly" absent (abstract uses "often") | "up to 35x" vs table 3.4x-13.1x: the claim already notes both |
| 27 | supported | MIPRO abstract "as much as 13% accuracy"; Table 2 69.1 to 79.4 | 10.3/69.1 = 14.9% relative, recomputed |
| 28 | supported | agents ipynb: "Average Metric: 8.00 / 100 (8.0%)", "41.67 / 100 (41.7%)", "some $5 worth of calls to GPT-4o" | the $5 is GPT-4o teacher calls; ReAct metric is top5_recall |
| 29 | supported | LEM abstract "the impact varies by task"; "using the optimized prompt with a cheaper model did not improve performance" | LEM text read has no arXiv ID/date, but title and authors match |
| 30 | supported | PyPI JSON read Oct 12, 2026: version 3.4.0 | |
| 31 | partly supported | PyPI: MIT, <3.15,>=3.10, upload 2026-09-25 | "about 400 MB installed" and the Ollama/local-model note not verified. Cited key is DSD but facts come from PyPI |
| 32 | supported | _litellm.py:14 `litellm.telemetry = False`; no other telemetry code (only unrelated "decoding telemetry" in vendored lm15) | absence claim; also depends on the gepa dependency not inspected |
| 33 | supported | model_metadata/__init__.py:54 `forced = os.getenv("LITELLM_LOCAL_MODEL_COST_MAP", "").lower() == "true"`; fetches raw.githubusercontent.com on first load | load happens on first metadata use, not only "price"; falls back to bundled snapshot on failure |
| 34 | partly supported | choosing-an-optimizer: BootstrapFewShot "safe first try"; optimizers.md:90 "200 examples or more" for MIPROv2; overview.md "aim for at least 300" | No doc says GEPA needs a few hundred examples; GEPA tutorial uses the opposite split. Budget cap and untouched test set are recommendations by the author (overview.md does mention a held-out test set) |
| 35 | partly supported | PyPI: numpy 2.5.4 requires_python ">=3.12"; 2.4.4 ">=3.11" | check counts, Python patch versions (3.11.17, 3.13.16), "about 70 packages" are the author's own runs; not verifiable |
| 36 | partly supported | dummies.py DummyLM "return the next dictionary in the list for each request" | "2 of 3 kept" is an own-run result, not checked; code not executed |
| 37 | supported | docs/docs/learn/optimization/optimizers.md exists in stanfordnlp/dspy | |
| 38 | supported | ACL Anthology: EMNLP 2024, pp. 9340-9366, DOI 10.18653/v1/2024.emnlp-main.525 | |
| 39 | supported | iclr.cc page: session type "Oral", ICLR 2026, same title; arXiv v2 | the arXiv page itself shows no venue |
| 40 | supported | GEP and MIP are authors' own results | |
| 41 | supported | LEM "varies by task"; ROP "OPRO shows limited effectiveness in small-scale LLMs", Findings of ACL 2024 pp. 1727-1735 | OPRO is a different method from DSPy; "independent" fine |
| 42 | supported | GEP "GEPA-Qwen-Opt" 62.03 on GPT-4.1 Mini (+9.00) vs +12.19 direct; LEM abstract | ~74% of gain kept; "most" ok |
| 43 | supported | AEF "`output_config.effort`"; ORS reasoning.effort | |
| 44 | supported | ATK "billed as output tokens, even when the thinking text isn't returned to you"; ORS reasoning tokens "billed as" output | |
| 45 | supported | AXT "set `thinking: {type: "adaptive"}`, and control reasoning depth with `output_config: {effort: ...}`"; AEF levels `low`,`medium`,`high`,`xhigh`,`max` | not every model supports xhigh/max (Opus 4.6, Sonnet 4.6 lack xhigh) |
| 46 | supported | AEF "Claude Opus 5.5 and Claude Haiku 5.5 default to medium" | |
| 47 | supported | AXT "deprecated on the Claude 4.6 models ... Claude 4.7 and later models do not support it and reject requests that use it, returning a 400 error." | |
| 48 | supported | ATK "On Claude Opus 5.5, ... Claude Sonnet 5.5, ... and Claude Haiku 5.5, thinking is already on" | |
| 49 | supported | ATK omitted is default on Opus 5.5, Sonnet 5.5, Haiku 5.5 etc.; "No `display` setting returns the raw chain of thought." | |
| 50 | supported | ATK intro "billed as output tokens, even when the thinking text isn't returned to you" | quote truncated before "to you" |
| 51 | supported | ATK Sampling parameters: "non-default `temperature`, `top_p`, or `top_k` values return a 400 error on every request" | list includes 4.7/4.8 too; top_p default is 0.99, so top_p 1 also errors |
| 52 | supported | ANT: each of temperature, top_k, top_p "Deprecated. Models released after Claude Opus 4.6" | |
| 53 | supported | ATK "Pass every `thinking` block back to the API complete and unmodified" | |
| 54 | supported | ORS "Supported values are model-dependent and can include `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, and `max`"; OAPI ReasoningEffort enum same | |
| 55 | supported | ORS "While we don't expose the raw reasoning tokens emitted by the model"; summary `auto`,`concise`,`detailed` | |
| 56 | supported | ORS "OpenAI recommends reserving at least 25,000 tokens for reasoning and outputs" | |
| 57 | supported | OTX "prioritized ahead of user messages"; ORB developer messages for reasoning models | phrase is in OTX, not ORB |
| 58 | supported | ORB "Avoid chain-of-thought prompts" bullet: "unnecessary"; "Try zero shot first" bullet | |
| 59 | could not check | phrase "a clear goal, strong constraints, and an explicit output contract" not found in ORS or ORB (searched 3 times) | cited ORS has no prompting section; "tuning knob" also absent |
| 60 | supported | ABP "A prompt like "think thoroughly" often produces better reasoning than a hand-written step-by-step plan"; "Worked examples in your prompt shape how Claude approaches similar problems"; "lower the `effort` setting" | |
| 61 | supported | OTX "prioritized ahead of user messages" + Model Spec link; ABP contains no priority rule | "trained priority, not code" is the author's reading of the Model Spec link |
| 62 | supported | ORB "is unnecessary" | |
| 63 | supported | ATK 400 error on non-default temperature; (4) 41.7% figure is from the toy example, not checked here | 41.7 matches DSPy agents tutorial coincidentally; clarify it is the author's own run |
| 64 | supported | ATK as above; ABP does not mention temperature | quotes of the skill files not checkable |

Totals: supported 58, partly 5 (10, 31, 34, 35, 36), contradicted 0, could not check 1 (59). (Claims 63 and 64 include author-run or local-file statements not checkable here.)

## Findings
1. Claim 59, severity medium. Text: Give "a clear goal, strong constraints, and an explicit output contract"; effort is a tuning knob, not the main fix for quality [ORS]. What goes wrong: the quoted phrase is not on the cited page. Why: ORS headings are Reasoning effort, Reasoning mode, How reasoning works, Controlling costs, Preserve reasoning, Change reasoning mid-conversation, Reasoning summaries; none of "contract", "constraints", "goal", "tuning knob" occur. ORB has "Provide specific guidelines" and "Be very specific about your end goal" instead. Fix: find the true source page (maybe another OpenAI guide) or replace with the ORB wording: "outline those constraints in the prompt", "very specific parameters for a successful response"; drop the quote marks.
2. Claim 10, severity low. Text: Three optimizers, in order of cost. What goes wrong: docs do not rank them. Why: "Search-based optimizers (BootstrapRS, MIPROv2, GEPA) cost real money" (choosing-an-optimizer.md). Fix: say "roughly cheapest first (the author's ordering)", or drop "in order of cost".
3. Claim 34, severity low-medium. Text: MIPROv2 or GEPA only with a few hundred examples... What goes wrong: "few hundred" is documented for MIPROv2 only; GEPA's own docs use a different split and no such threshold. Fix: "MIPROv2 (docs: 200+ examples); GEPA needs a reflection model and feedback-style metric", and label budget cap and untouched test set as advice.
4. Claim 31, severity low. "About 400 MB installed" and the local-model note are unverified; cite PyPI for version/date/Python/license, and measure the size or drop it.
5. Claim 35, severity low. Own-run test results, package count and Python patch versions (3.11.17, 3.13.16) cannot be verified from sources; only the numpy Python-version requirements are confirmed. Mark as "T" (author-tested) and double-check the patch versions.
6. Claim 36, severity low. "BootstrapFewShot keeps 2 of 3" is an own-run result; DummyLM scripted-answer behaviour is confirmed. Label as a local test.

Lookups used: 25 web (WebFetch/WebSearch), plus shell: git clone, pip download, PyPI JSON, OpenAI openapi.yaml download.
