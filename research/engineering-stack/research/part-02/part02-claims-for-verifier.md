# Claims to verify (Part 02: evals, test data and judges)

Each claim names the source key(s) it rests on. Source URLs are listed at the end. Quoted words are claimed to appear in the source as written (allowing for straight versus curly quotes).

## Group A: papers, statistics and vendor guidance

A1. OpenAI's "Evaluation best practices" lists five steps: define the eval objective, collect a dataset, define eval metrics, run and compare evals, and continuously evaluate, running evals "on every change".  Sources: OBP

A2. OpenAI's guide names "vibe-based evals" as an anti-pattern; it also lists "Overly generic metrics" and "Ignoring human feedback: Not calibrating your automated metrics against human evals" as anti-patterns.  Sources: OBP

A3. OpenAI's guide: "Ensure your test data includes typical cases, edge cases, and adversarial cases".  Sources: OBP

A4. OpenAI's guide names three judge setups (pairwise comparison, single answer grading, reference-guided grading) and warns of position bias and verbosity bias (preferring longer responses).  Sources: OBP

A5. OpenAI's guide: human judgment evals give "the highest quality but are slow and expensive"; and "the quality of LLM-as-Judge varies depending on problem context".  Sources: OBP

A6. Anthropic's API reference for `temperature`: "Note that even with `temperature` of `0.0`, the results will not be fully deterministic." The parameter is marked deprecated: "Models released after Claude Opus 4.6 do not support setting temperature. A value of 1.0 will be accepted for backwards compatibility, all other values will be rejected with a 400 error."  Sources: ANT

A7. Anthropic's eval guide names three ways to grade (code-based, human, LLM-based) and says to "choose the fastest, most reliable, most scalable method".  Sources: ANE

A8. Anthropic's guide on code-based grading: "Fastest and most reliable, extremely scalable, but also lacks nuance for more complex judgments that require less rule-based rigidity". On LLM-based grading: "Fast and flexible, scalable and suitable for complex judgment. Test to ensure reliability first then scale". On human grading: "Most flexible and high quality, but slow and expensive. Avoid if possible".  Sources: ANE

A9. Anthropic's guide asks for success criteria that are specific, measurable, achievable and relevant, for example "accurate sentiment classification" instead of "good performance".  Sources: ANE

A10. Anthropic's guide: "Design evals that mirror your real-world task distribution. Don't forget to factor in edge cases!" Its edge-case examples include irrelevant or nonexistent input, overly long input, poor or harmful input, and "ambiguous test cases where even humans would find it hard to reach an assessment consensus".  Sources: ANE

A11. Anthropic's guide: "Prioritize volume over quality: More questions with slightly lower signal automated grading is better than fewer questions with high-quality human hand-graded evals".  Sources: ANE

A12. Anthropic's guide suggests getting Claude "to help you generate more from a baseline set of example test cases".  Sources: ANE

A13. Anthropic's LLM-grading tips: detailed, clear rubrics; empirical output, for example "only 'correct' or 'incorrect', or to judge from a scale of 1-5"; a grader model "with thinking on, so that it reasons before it produces an evaluation score". A code comment in its example says it is "Generally best practice to use a different model to evaluate than the model used to generate the evaluated output".  Sources: ANE

A14. OpenAI's "Advanced usage" guide (section "Reproducible outputs"): Chat Completions "are non-deterministic by default"; setting `seed` makes output "(mostly) deterministic"; a changed `system_fingerprint` signals changes on OpenAI's side.  Sources: OAD

A15. Inspect AI's documentation describes an evaluation's dataset as labelled samples with an `input` and a `target`.  Sources: INS

A16. scikit-learn: precision = tp / (tp + fp); recall = tp / (tp + fn); the F-beta score with beta = 1 is F1, weighting precision and recall equally.  Sources: SKM

A17. scikit-learn's user guide on kappa: scores "above .8 are generally considered good agreement; zero or lower means no agreement (practically random labels)".  Sources: SKM

A18. scikit-learn's `cohen_kappa_score`: kappa = (p_o - p_e) / (1 - p_e), with p_o the observed agreement and p_e the expected agreement, estimated using a per-annotator empirical prior over the class labels; it cites Cohen 1960.  Sources: SKK

A19. The Wilson score interval: centre = (p + z^2/(2n)) / (1 + z^2/n); half-width = z * sqrt(p(1 - p)/n + z^2/(4n^2)) / (1 + z^2/n).  Sources: NIST

A20. Brown, Cai and DasGupta (2001) recommend "the Wilson interval or the equal-tailed Jeffreys prior interval for small n" (n of 40 or less) and the Agresti-Coull interval for larger n, and describe the coverage of the standard (Wald) interval as "erratic".  Sources: BCD

A21. McNemar's test "conditions on the number of discordant pairs". Under the null hypothesis, the count of one kind of discordant pair follows a binomial distribution with n = b + c and probability 1/2.  Sources: FLL

A22. Fagerland et al.'s formulas: the exact conditional two-sided p-value is twice the one-sided tail (summed from 0 to min(b, c)), and equals 1.0 when b = c; the mid-p equals 2 × (one-sided p - half the point probability of the observed count), and 1 - f(b)/2 when b = c.  Sources: FLL

A23. Fagerland et al.: "Quite often, the type I error rates of the exact conditional test were half that of the nominal level or lower"; the mid-p test is "an excellent alternative" to the complex exact unconditional test; "We do not recommend use of the McNemar exact conditional test nor the asymptotic test with CC in any situation". So the mid-p is less conservative than the exact conditional test.  Sources: FLL

A24. McHugh (2012): "any kappa below 0.60 indicates inadequate agreement among the raters and little confidence should be placed in the study results".  Sources: MCH

A25. Fawcett (2006): the AUC equals the probability that a classifier ranks a randomly chosen positive instance higher than a randomly chosen negative one.  Sources: FAW

A26. Miller (2024) recommends: standard errors of the mean from the Central Limit Theorem, reported alongside the mean, sqrt(s(1 - s)/n) for binary scores, with the number of questions; clustered standard errors "when questions are drawn in related groups"; "conducting statistical inference on the question-level paired differences, rather than the population-level summary statistics"; power analysis to see whether an eval can test a hypothesis of interest; "resampling answers" to reduce variance.  Sources: MIL

A27. Miller: paired differences reduce the variance "as long as the conditional means of the model scores are correlated".  Sources: MIL

A28. Miller's examples: clustered standard errors were 1.10 times the naive value on RACE-H, 1.88 on MGSM and 3.05 on DROP.  Sources: MIL

A29. Miller: the sampling temperature should not be "adjusted for the sake of reducing variance in the scores".  Sources: MIL

A30. Zheng et al. (NeurIPS 2023 Datasets and Benchmarks), MT-bench first turn, Table 5: a GPT-4 pairwise judge agreed with human experts 66% of the time in setup S1 (ties and inconsistent votes counted as ties) and 85% in S2 (non-tie votes only); human-human agreement was 63% and 81%. The human judgments came from 58 expert labelers, about 3,000 votes.  Sources: ZHE

A31. Zheng et al., Table 2: GPT-4's position consistency was 65.0%, biased toward the first answer 30.0%; with few-shot examples (Table 12), 77.5%.  Sources: ZHE

A32. Zheng et al.'s "repetitive list" attack: GPT-4 rephrased an answer's numbered list without adding information, and the rephrased list was put in front of the original. Failure rates on 23 answers: Claude-v1 91.3%, GPT-3.5 91.3%, GPT-4 8.7%.  Sources: ZHE

A33. Zheng et al.: "our study cannot determine whether the models exhibit a self-enhancement bias".  Sources: ZHE

A34. Zheng et al., Table 4: GPT-4 said an incorrect maths answer was correct in 14 of 20 judgments with the default prompt, 6 of 20 with chain-of-thought, and 3 of 20 with a reference answer.  Sources: ZHE

A35. Zheng et al.: swap the answers' positions and "only declare a win when an answer is preferred in both orders"; if inconsistent, "call it a tie". Few-shot examples, chain-of-thought and reference answers are among the fixes they test.  Sources: ZHE

A36. Wang et al. (ACL 2024): with ChatGPT as the evaluator, "Vicuna-13B could beat ChatGPT on 66 over 80 tested queries" by changing the order of the answers. They propose Multiple Evidence Calibration, Balanced Position Calibration and Human-in-the-Loop Calibration.  Sources: WAN

A37. Panickssery, Bowman and Feng (NeurIPS 2024) found "a linear correlation between self-recognition capability and the strength of self-preference bias", with GPT-4, GPT-3.5 and Llama-2-7b-chat, on summarization of news articles (XSUM and CNN/DailyMail).  Sources: PAN

A38. The judge studies by Zheng et al., Wang et al. and Panickssery et al. were published in 2023 and 2024 and tested models of that time.  Sources: ZHE, WAN, PAN

A39. GSM1k (NeurIPS 2024 Datasets and Benchmarks): new grade-school maths problems in the style of GSM8k; "accuracy drops of up to 8%" for leading models; a positive relationship (Spearman's r^2 = 0.36) between a model's probability of generating GSM8k examples and its performance gap, "suggesting that some models may have partially memorized GSM8k".  Sources: GSM

A40. Shankar et al. (UIST '24) "identify a phenomenon we dub criteria drift": "users need criteria to grade outputs, but grading outputs helps users define criteria".  Sources: SHA

A41. Farquhar et al. (Nature, 2024) study "confabulations", for which "LLMs fluently make claims that are both wrong and arbitrary", meaning "the answer is sensitive to irrelevant details such as random seed".  Sources: FAR

A42. Semantic entropy was introduced by Kuhn, Gal and Farquhar in an ICLR 2023 paper ("we introduce semantic entropy").  Sources: KUH

A43. Farquhar et al. use "ten generations", sampled at temperature 1 with nucleus sampling (P = 0.9) and top-K sampling (K = 50).  Sources: FAR

A44. Two answers share a meaning when they entail each other (bidirectional entailment), judged by models "such as DeBERTa-Large-MNLI, or general-purpose LLMs such as GPT-3.5"; the main experiments use GPT-3.5. Each new answer is checked against one member of each existing cluster ("we arbitrarily pick the first one"), and an answer matching none gets its own cluster.  Sources: FAR

A45. In the discrete variant, each cluster's probability is estimated from the number of generations in it, which "results in similar performance empirically". The entropy is SE = -sum p(C) log p(C) over clusters.  Sources: FAR

A46. "Averaged across the 30 combinations of tasks and models we study, semantic entropy achieves the best AUROC value of 0.790"; naive entropy 0.691, P(True) 0.698, embedding regression 0.687.  Sources: FAR

A47. Naive entropy is computed from "the length-normalized joint probability of the token sequences".  Sources: FAR

A48. The AUROC in Farquhar et al. scores "the binary event that a given answer is incorrect".  Sources: FAR

A49. Farquhar et al.'s limits: semantic entropy "does not help when LLM outputs are systematically bad", and "does not directly address situations in which LLMs are confidently wrong".  Sources: FAR

A50. Kossen et al. (a preprint) cite a "5-to-10-fold" increase in computation cost for semantic entropy, and propose probes that "directly approximate SE from the hidden states of a single generation".  Sources: KOS

A51. Thinking Machines Lab (September 10, 2025): 1,000 completions of "Tell me about Richard Feynman" at temperature 0 from Qwen3-235B-A22B-Instruct-2507 gave 80 unique completions. The cause they identify is that the forward pass lacks "batch invariance" while the server's load, and so its batch size, varies; with batch-invariant kernels all 1,000 completions were identical.  Sources: TML

A52. Chen et al. (2021): the unbiased pass@k estimator is 1 - C(n - c, k) / C(n, k), averaged over problems, with n samples of which c are correct; they use n = 200 and k <= 100; the simpler 1 - (1 - c/n)^k is biased.  Sources: CHE

## Group B: tools, licences, versions and platforms

B1. promptfoo is MIT-licensed; its npm package version 0.124.1 was published October 8, 2026, and needs Node.js 22.22.0 or newer; the installation docs recommend Node.js 24 LTS.  Sources: NPM, PFR, PFI

B2. promptfoo's README: "Promptfoo is now part of OpenAI. Promptfoo remains open source and MIT licensed."  Sources: PFR

B3. OpenAI announced on March 9, 2026 that it would acquire promptfoo; promptfoo's own post of the same date says it "has agreed to be acquired by OpenAI".  Sources: OAQ, PFB

B4. promptfoo releases often: 0.124.1 on 2026-10-08, 0.124.0 on 2026-10-06, 0.123.1 on 2026-09-18, 0.123.0 on 2026-09-10 (CHANGELOG).  Sources: PFR

B5. promptfoo "collects basic usage telemetry by default": commands run and assertion types used, with package version and whether it runs in CI; telemetry "does not include prompts, model outputs, test cases, provider API keys, or full configuration files". `PROMPTFOO_DISABLE_TELEMETRY=1` turns it off; `PROMPTFOO_DISABLE_UPDATE=1` turns off the update check.  Sources: PFY

B6. promptfoo's model-graded assertions use a default grading provider chosen from the credentials available in the environment (for example OpenAI or Anthropic credentials); the grader can be set explicitly, including to a local Ollama model. Its docs disagree about the default: the llm-rubric page says `gpt-5`; the model-graded overview says "GPT-6 Sol".  Sources: PFE

B7. promptfoo's cloud sharing needs a login (`promptfoo auth login`).  Sources: PFS

B8. promptfoo's `eval` returns exit code 100 when at least one test case fails or the pass rate is below `PROMPTFOO_PASS_RATE_THRESHOLD`, and 1 for other errors. `--no-share` does not create a shareable URL; `--no-write` does not write results to the promptfoo directory; `view` starts a browser UI. Logs are stored in `~/.promptfoo/logs` unless `PROMPTFOO_LOG_DIR` is set.  Sources: PFC

B9. promptfoo's Python provider: a `file://` Python file whose function receives the prompt, options and context and returns a dictionary with `output` (or `error`); a custom function name is given as `file://my_provider.py:function_name`. promptfoo finds Python in this order: `pythonExecutable` in the config, `PROMPTFOO_PYTHON`, on Windows `where python` with Microsoft Store stubs filtered out, asking `python` for `sys.executable`, then the commands `python`, `python3`, `py -3`, `py` (Windows) or `python3`, `python` (macOS, Linux). For `spawn py -3 ENOENT` or "Python 3 not found" errors, it advises setting `PROMPTFOO_PYTHON`.  Sources: PFP

B10. promptfoo can load test cases from a Python function: `tests: file://generate_tests.py:create_tests`.  Sources: PFT

B11. promptfoo's GitHub Action runs "a before vs. after evaluation of edited prompts" on pull requests. Without `PROMPTFOO_API_KEY` or `PROMPTFOO_REMOTE_API_BASE_URL` set, it passes `--no-share`.  Sources: PFG

B12. OpenAI's Cookbook article "Moving from OpenAI Evals to Promptfoo" (June 3, 2026) recommends promptfoo for "continuing and extending your evaluation workflows".  Sources: OMG

B13. OpenAI's hosted Evals platform: deprecation announced June 3, 2026; existing evals become read-only on October 31, 2026; the platform is scheduled to shut down on November 30, 2026.  Sources: OEV, ODP

B14. OpenAI's deprecations page, section "2026-04-22: Legacy GPT model snapshots": gpt-4 and gpt-4-0613 are scheduled to shut down on October 23, 2026, with `gpt-5.6-sol` as the substitute model.  Sources: ODP

B15. pytest is MIT-licensed; pytest 9 supports Python 3.10 or later; pytest 9.1.1 was released June 19, 2026; pytest 9.1.1 requires colorama 0.4 or later on Windows (`sys_platform == "win32"`).  Sources: PYPI, PYT

B16. Inspect AI is MIT-licensed, needs Python 3.10 or later, and is developed by the UK AI Security Institute and Meridian Labs; version 0.3.278 is dated October 9, 2026 in its changelog. Running evaluations usually needs a model and its API key; it supports Ollama; `mockllm/model` is a mock model for tests.  Sources: INS

B17. DeepEval is Apache-2.0, needs Python 3.9 to below 4.0, and its hosted platform (Confident AI) is optional. Its LLM-judged metrics default to OpenAI's `gpt-5.4` and need `OPENAI_API_KEY`; `deepeval set-ollama` configures a local model; ExactMatchMetric, PatternMatchMetric and JsonCorrectnessMetric need no LLM. Telemetry uses PostHog, on by default, and includes the public IP address; `DEEPEVAL_TELEMETRY_OPT_OUT=1` opts out. Version 4.2.8 is dated October 2, 2026 on PyPI.  Sources: DEV, PYPI

B18. Ragas is Apache-2.0 and needs Python 3.9 or later; its main RAG metrics need an LLM, and some (Response Relevancy) also need embeddings. It collects usage data by default; `RAGAS_DO_NOT_TRACK=true` opts out, and the code accepts only the word true. Its last release, 0.4.3, was January 13, 2026; its main branch has had no commits since February 24, 2026; the repository moved to the vibrantlabsai organization.  Sources: RAG

B19. Arize Phoenix uses the Elastic License 2.0, which says "You may not provide the software to third parties as a hosted or managed service"; Arize's docs say self-hosting is free. Phoenix serves its web app on port 6006 by default. Its LLM evaluators need a model; its exact-match and regex evaluators don't. Phoenix collects web analytics by default; `PHOENIX_TELEMETRY_ENABLED=false` turns them off. PyPI lists arize-phoenix 20.21.0, uploaded October 11, 2026, as needing Python 3.11 to below 3.15.  Sources: PHX, PYPI

B20. EleutherAI's lm-evaluation-harness is MIT-licensed and needs Python 3.10 or later; model backends are installed separately as extras; it supports Hugging Face, vLLM, local OpenAI-compatible servers and hosted APIs (through its `api` extra). Version 0.4.13 is dated August 31, 2026 on PyPI. Its README says it is the backend for Hugging Face's Open LLM Leaderboard.  Sources: LME, PYPI

B21. Hugging Face announced on March 13, 2025 that the Open LLM Leaderboard "is officially retiring".  Sources: HFL

B22. OpenAI's Evals repository is MIT-licensed except for its datasets; its README asks for an OpenAI API key, warns about API costs, and gives Python 3.9 as the minimum; it has had 6 commits since June 1, 2024, the latest on April 14, 2026.  Sources: OEG

B23. scikit-learn and statsmodels are BSD-3-Clause; SciPy is BSD-licensed; scikit-learn 1.9.1, statsmodels 0.15.0 and SciPy 1.18.1 were released between August and September 2026.  Sources: PYPI

B24. GitHub Actions usage is "free for self-hosted runners and for public repositories that use standard GitHub-hosted runners"; private repositories on GitHub Free get 2,000 minutes a month.  Sources: GHA

## Sources

| Key | Source |
|---|---|
| ANE | Anthropic, "Define success criteria and build evaluations". https://platform.claude.com/docs/en/test-and-evaluate/develop-tests |
| ANT | Anthropic, "Create a Message" (API reference; see `temperature`). https://platform.claude.com/docs/en/api/messages/create |
| BCD | Brown, Cai, DasGupta, "Interval Estimation for a Binomial Proportion", Statistical Science 16(2), 2001. https://www-stat.wharton.upenn.edu/~tcai/paper/Binomial-StatSci.pdf |
| CHE | Chen et al., "Evaluating Large Language Models Trained on Code", 2021. https://arxiv.org/abs/2107.03374 |
| DEV | DeepEval repository: https://github.com/confident-ai/deepeval (README.md, LICENSE.md, pyproject.toml, deepeval/models/llms/constants.py, docs/content/docs/data-privacy.mdx, docs/content/docs/environment-variables.mdx, docs/content/integrations/models/ollama.mdx, the metric pages under docs/content/docs/) |
| FAR | Farquhar et al., "Detecting hallucinations in large language models using semantic entropy", Nature 2024. https://www.nature.com/articles/s41586-024-07421-0 |
| FAW | Fawcett, "An introduction to ROC analysis", Pattern Recognition Letters 27, 2006. https://people.inf.elte.hu/kiss/11dwhdm/roc.pdf |
| FLL | Fagerland, Lydersen, Laake, BMC Medical Research Methodology 13:91, 2013. https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-91 (may redirect to link.springer.com/article/10.1186/1471-2288-13-91) |
| GHA | GitHub Docs, "GitHub Actions billing". https://docs.github.com/en/billing/concepts/product-billing/github-actions |
| GSM | Zhang et al., GSM1k, NeurIPS 2024. https://proceedings.neurips.cc/paper_files/paper/2024/hash/53384f2090c6a5cac952c598fd67992f-Abstract.html ; https://arxiv.org/abs/2405.00332 |
| HFL | Hugging Face discussion, "end of the Open LLM Leaderboard". https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard/discussions/1135 |
| INS | Inspect AI: https://inspect.aisi.org.uk/ ; https://github.com/UKGovernmentBEIS/inspect_ai (docs/index.qmd, docs/providers.qmd, CHANGELOG.md, LICENSE, pyproject.toml, src/inspect_ai/model/_providers/mockllm.py) |
| KOS | Kossen et al., "Semantic Entropy Probes", 2024. https://arxiv.org/abs/2406.15927 |
| KUH | Kuhn, Gal, Farquhar, "Semantic Uncertainty". https://arxiv.org/abs/2302.09664 ; ICLR 2023 page https://iclr.cc/virtual/2023/poster/11013 |
| LME | https://github.com/EleutherAI/lm-evaluation-harness (README.md, LICENSE.md, pyproject.toml) |
| MCH | McHugh, "Interrater reliability: the kappa statistic", Biochemia Medica 22(3), 2012. https://www.biochemia-medica.com/en/journal/22/3/10.11613/BM.2012.031 |
| MIL | Miller, "Adding Error Bars to Evals", 2024. https://arxiv.org/abs/2411.00640 (HTML: https://arxiv.org/html/2411.00640) |
| NIST | NIST/SEMATECH e-Handbook, 7.2.4.1. https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm |
| NPM | npm registry: run `npm view promptfoo version time.modified license engines` |
| OAD | OpenAI, "Advanced usage" (section "Reproducible outputs"). https://developers.openai.com/api/docs/guides/advanced-usage |
| OAQ | OpenAI, "OpenAI to acquire Promptfoo". https://openai.com/index/openai-to-acquire-promptfoo/ |
| OBP | OpenAI, "Evaluation best practices". https://developers.openai.com/api/docs/guides/evaluation-best-practices |
| ODP | OpenAI, "Deprecations". https://developers.openai.com/api/docs/deprecations |
| OEG | https://github.com/openai/evals (README.md, LICENSE.md, commit history) |
| OEV | OpenAI, "Working with evals". https://developers.openai.com/api/docs/guides/evals |
| OMG | OpenAI Cookbook, "Moving from OpenAI Evals to Promptfoo". https://developers.openai.com/cookbook/examples/evaluation/moving-from-openai-evals-to-promptfoo |
| PAN | Panickssery, Bowman, Feng, NeurIPS 2024. https://papers.nips.cc/paper_files/paper/2024/hash/7f1f0218e45f5414c79c0679633e47bc-Abstract-Conference.html ; https://arxiv.org/abs/2404.13076 |
| PFB | promptfoo blog, "Promptfoo is joining OpenAI". https://www.promptfoo.dev/blog/promptfoo-joining-openai/ |
| PFC | promptfoo docs, "Command line". https://www.promptfoo.dev/docs/usage/command-line/ |
| PFE | promptfoo docs, model-graded assertions. https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/ ; https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/ ; https://www.promptfoo.dev/docs/providers/ollama/ |
| PFG | promptfoo docs, "GitHub Action". https://www.promptfoo.dev/docs/integrations/github-action/ ; https://github.com/promptfoo/promptfoo-action (README.md) |
| PFI | promptfoo docs, "Installation". https://www.promptfoo.dev/docs/installation/ |
| PFP | promptfoo docs, "Python Provider". https://www.promptfoo.dev/docs/providers/python/ |
| PFR | https://github.com/promptfoo/promptfoo (README.md, LICENSE, CHANGELOG.md) |
| PFS | promptfoo docs, "Sharing". https://www.promptfoo.dev/docs/usage/sharing/ |
| PFT | promptfoo docs, "Test Case Configuration". https://www.promptfoo.dev/docs/configuration/test-cases/ |
| PFY | promptfoo docs, "Telemetry". https://www.promptfoo.dev/docs/configuration/telemetry/ |
| PHX | https://github.com/Arize-ai/phoenix (README.md, LICENSE, CHANGELOG.md, docs/phoenix/self-hosting/license.mdx, docs/phoenix/self-hosting/configuration.mdx, docs/phoenix/self-hosting/security/privacy.mdx, packages/phoenix-evals/README.md) |
| PYPI | PyPI JSON API: https://pypi.org/pypi/PACKAGE/json (and https://pypi.org/pypi/pytest/9.1.1/json for its dependencies) |
| PYT | pytest docs: https://docs.pytest.org/en/stable/changelog.html ; https://docs.pytest.org/en/stable/backwards-compatibility.html |
| RAG | https://github.com/vibrantlabsai/ragas (formerly explodinggradients/ragas): README.md, LICENSE, pyproject.toml, src/ragas/_analytics.py, docs/concepts/metrics/, commit history and tags; https://docs.ragas.io |
| SHA | Shankar et al., "Who Validates the Validators?". https://arxiv.org/abs/2404.12272 ; UIST '24 BibTeX https://people.eecs.berkeley.edu/~bjoern/papers/shankar-validators-uist2024.bib |
| SKK | scikit-learn, `cohen_kappa_score`. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html |
| SKM | scikit-learn user guide, "Metrics and scoring". https://scikit-learn.org/stable/modules/model_evaluation.html |
| TML | Thinking Machines Lab, "Defeating Nondeterminism in LLM Inference". https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ |
| WAN | Wang et al., ACL 2024. https://aclanthology.org/2024.acl-long.511/ ; https://arxiv.org/abs/2305.17926 |
| ZHE | Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena". https://arxiv.org/abs/2306.05685 (HTML: https://arxiv.org/html/2306.05685) |
