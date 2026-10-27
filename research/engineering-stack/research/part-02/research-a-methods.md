# Research A: methods sources for the evals teaching paper

Source-checking notes. Started 2026-10-09 (task date 2026-10-10).
Rule: every fact below comes from a page opened in this run. Quotes are as returned by WebFetch when asked for exact wording
(curl was blocked by the egress policy, so nothing was read as raw text). NOT FOUND is written where a lookup failed.

Lookup log (count toward ~40 budget) is kept at the bottom of this file.

Class codes: OD official documentation; PR peer-reviewed; PP preprint; VB vendor blog; PB personal blog.


## Environment note
- curl to export.arxiv.org (arXiv API) was refused by this session's egress policy (403 CONNECT, "connect_rejected").
  Per the proxy README, not retried or routed around. All further web lookups use the WebFetch/WebSearch tools,
  which return a model-written extraction of the page, so "verbatim" quotes below are as returned by WebFetch when
  asked for exact wording. Spot risk: small paraphrase errors are possible; flag anything load-bearing for a
  re-check in a browser.

## A1. Anthropic documentation on evaluations

Source: Anthropic, "Define success criteria and build evaluations - Claude Platform Docs".
URL opened: https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
Redirects observed: docs.claude.com/en/docs/test-and-evaluate/develop-tests -> 302 -> platform.claude.com/docs/en/test-and-evaluate/develop-tests.
ALSO docs.claude.com/en/docs/test-and-evaluate/define-success -> 302 -> the SAME develop-tests page
(the separate "Define success criteria" page appears to have been merged into this one; page title confirms both topics).
Class: OD. Accessed 2026-10-09.

Top-level headings: "Define your success criteria"; "Build evaluations"; "Grade your evaluations"; "Next steps".
Subheadings: "Common success criteria"; "Eval design principles"; "Example evals"; "Tips for LLM-based grading".

Success criteria (under "Define your success criteria", "Good success criteria are:"):
- Specific: "Clearly define what you want to achieve. Instead of "good performance," specify "accurate sentiment classification.""
- Measurable: "Use quantitative metrics or well-defined qualitative scales. Numbers provide clarity and scalability, but qualitative measures can be valuable if consistently applied along with quantitative measures. Even "hazy" topics such as ethics and safety can be quantified:"
- Achievable: "Base your targets on industry benchmarks, prior experiments, AI research, or expert knowledge. Your success metrics should not be unrealistic to current frontier model capabilities."
- Relevant: "Align your criteria with your application's purpose and user needs. Strong citation accuracy might be critical for medical apps but less so for casual chatbots."
Common success criteria (list "is non-exhaustive"): Task fidelity ("...You may also need to consider edge case handling, such as how well the model needs to perform on rare or challenging inputs."), Consistency ("...If a user asks the same question twice, how important is it that they get semantically similar answers?"), Relevance and coherence, Tone and style, Privacy preservation, Context utilization, Latency, Price.

Grader types (under "Grade your evaluations"): "When deciding which method to use to grade evals, choose the fastest, most reliable, most scalable method:"
- Code-based grading: "Fastest and most reliable, extremely scalable, but also lacks nuance for more complex judgments that require less rule-based rigidity." Examples given: "Exact match: output == golden_answer"; "String match: key_phrase in output".
- Human grading: "Most flexible and high quality, but slow and expensive. Avoid if possible."
- LLM-based grading: "Fast and flexible, scalable and suitable for complex judgment. Test to ensure reliability first then scale."

Volume vs quality (Eval design principles): "Prioritize volume over quality: More questions with slightly lower signal automated grading is better than fewer questions with high-quality human hand-graded evals."

Edge cases / writing test cases (Eval design principles):
- "Be task-specific: Design evals that mirror your real-world task distribution. Don't forget to factor in edge cases!"
- "Example edge cases": "Irrelevant or nonexistent input data"; "Overly long input data or user input [Chat use cases]"; "Poor, harmful, or irrelevant user input"; "Ambiguous test cases where even humans would find it hard to reach an assessment consensus".
- "Automate when possible: Structure questions to allow for automated grading (for example, multiple-choice, string match, code-graded, LLM-graded)."
- "Writing hundreds of test cases can be hard to do by hand! Get Claude to help you generate more from a baseline set of example test cases. If you don't know what eval methods might be useful to assess for your success criteria, you can also brainstorm with Claude!"

Tips for LLM-based grading:
- "Have detailed, clear rubrics: "The answer should always mention 'Acme Inc.' in the first sentence. If it does not, the answer is automatically graded as 'incorrect.'" A given use case, or even a specific success criteria for that use case, might require several rubrics for holistic evaluation."
- "Empirical or specific: For example, instruct the LLM to output only 'correct' or 'incorrect', or to judge from a scale of 1-5. Purely qualitative evaluations are hard to assess quickly and at scale."
- "Encourage reasoning: Use a grader model with thinking on, so that it reasons before it produces an evaluation score. This increases evaluation performance, particularly for tasks requiring complex judgment."
  NOTE: the current page (Oct 2026) says "thinking on". The WebFetch extraction did NOT return any "then discard the reasoning" wording; older versions of this tip may have worded it differently. If the paper quotes older wording, re-check.
- Example grader prompt (build_grader_prompt): "Grade this answer based on the rubric: <rubric>{rubric}</rubric> <answer>{answer}</answer> Output 'correct' or 'incorrect' in <result> tags."
- Code comment in examples: "Generally best practice to use a different model to evaluate than the model used to generate the evaluated output"

Temperature 0 determinism: platform.claude.com/docs/en/api/messages (title "Messages - Claude API Reference") was opened;
WebFetch reported the temperature parameter text ABSENT from the extracted content (page lists types/endpoints, not the create-request params). See follow-up below.

A1 follow-up, temperature 0:
Source: Anthropic, "Create a Message - Claude API Reference", https://platform.claude.com/docs/en/api/messages/create (OD), accessed 2026-10-09.
`temperature` description as returned (WebFetch, asked for verbatim):
 "Amount of randomness injected into the response.
  Deprecated. Models released after Claude Opus 4.6 do not support setting temperature. A value of 1.0 will be accepted for backwards compatibility, all other values will be rejected with a 400 error.
  Defaults to `1.0`. Ranges from `0.0` to `1.0`. Use `temperature` closer to `0.0` for analytical / multiple choice, and closer to `1.0` for creative and generative tasks.
  Note that even with `temperature` of `0.0`, the results will not be fully deterministic."
IMPORTANT for the paper: as of Oct 2026 the parameter is marked Deprecated; newer models (released after Claude Opus 4.6) reject any value other than 1.0 with a 400 error. So "set temperature 0 for evals" advice does not apply to the newest Claude models.

## A2. OpenAI documentation

### A2-i Evaluation best practices
Source: OpenAI, "Evaluation best practices | OpenAI API", https://developers.openai.com/api/docs/guides/evaluation-best-practices
(platform.openai.com/docs/guides/evaluation-best-practices 302-redirects here). Class OD. Accessed 2026-10-09.
Process steps (under "Design your eval process"):
 1. "Define eval objective. What's the success criteria for the eval?"
 2. "Collect dataset. Which data will help you evaluate against your objective?"
 3. "Define eval metrics. How will you check that the success criteria are met?"
 4. "Run and compare evals. Iterate and improve model performance for your task or system."
 5. "Continuously evaluate. Set up continuous evaluation (CE) to run evals on every change" (continues: monitor production, grow the eval set).
Evaluator types (under "Create and combine different types of evaluators"):
 - Metric-based evals: "Quantitative evals provide a numerical score you can use to filter and rank results." Challenges: "May not be tailored to specific use cases, may miss nuance."
 - Human evals: "Human judgment evals provide the highest quality but are slow and expensive." Challenges: "Disagreement among human experts, expensive, slow."
 - LLM-as-a-judge and model graders: "Using models to judge output is cheaper to run and more scalable than human evaluation."
LLM-as-a-judge (under "LLM-as-a-judge and model graders"):
 - "Pairwise comparison: Present the judge model with two responses and ask it to determine which one is better based on specific criteria"
 - "Single answer grading: The judge model evaluates a single response in isolation, assigning a score or rating based on predefined quality metrics"
 - "Reference-guided grading: Provide the judge model with a reference or "gold standard" answer"
 - Biases named: "Position bias (response order), verbosity bias (preferring longer responses)." Self-enhancement bias: ABSENT. No numbers.
 - Recommendations: "Use pairwise comparison or pass/fail for more reliability"; "Use the most capable model to grade if you can."; "Control for response lengths as LLMs bias towards longer responses in general"; "Add reasoning and chain-of-thought as reasoning before scoring improves eval performance"; "Ensure eval rubrics are clear and detailed"; "validate whether a specialized reasoning model performs better for your rubric".
   Also returned: "Start with gpt-6-astra when you need a strong LLM judge" (model name as returned by WebFetch; post-dates my knowledge, verify in a browser before quoting).
 - Caveat: "The quality of LLM-as-Judge varies depending on problem context"
Human calibration: "Conduct multiple rounds of detailed human review to refine the scorecard"; "Implement a "show rather than tell" policy by providing examples of different score levels (e.g., 1, 3, and 8 out of 10)"; "Include a pass/fail threshold in addition to the numerical score"; "A simple way to aggregate multiple reviewers is to take consensus votes"; "Maintain agreement: Use human feedback to calibrate automated scoring."; "validate agreement against your human labels before optimizing for cost or latency."
Test data: "Ensure your test data includes typical cases, edge cases, and adversarial cases."; edge-case buckets "Input variability", "Contextual complexity", "Personalization and customization". "Adopt eval-driven development: Evaluate early and often. Write scoped tests at every stage." No general dataset-size number (only "a held-out set of 1000 reference transcripts" in one worked example).
Anti-patterns: "Overly generic metrics: Relying solely on academic metrics like perplexity or BLEU score."; "Biased design: Creating eval datasets that don't faithfully reproduce production traffic patterns."; "Vibe-based evals: Using "it seems like it's working" as an evaluation strategy, or waiting until you ship before implementing any evals."; "Ignoring human feedback: Not calibrating your automated metrics against human evals."

### A2-ii Evals guide
Source: OpenAI, "Working with evals | OpenAI API", https://developers.openai.com/api/docs/guides/evals (302 from platform.openai.com/docs/guides/evals). OD. Accessed 2026-10-09.
 - DEPRECATION: "OpenAI is deprecating the Evals platform." (intro)
 - "Broadly, there are three steps to build and run evals for your LLM application." 1 "Describe the task to be done as an eval" 2 "Run your eval with test inputs (a prompt and input data)" 3 "Analyze the results, then iterate and improve on your prompt".
 - "An eval needs two key ingredients:" "`data_source_config`: A schema for the test data you will use along with the eval." and "`testing_criteria`: The graders that determine if the model output is correct."
 - Only grader named on this page: `string_check` (example: "type": "string_check", "name": "Match output to human label", "input": "{{ sample.output_text }}", "operation": "eq", "reference": "{{ item.correct_label }}").
 - LLM-as-judge / bias / pairwise: ABSENT on this page.

### A2-iii Graders guide
Source: OpenAI, "Graders | OpenAI API", https://developers.openai.com/api/docs/guides/graders. OD. Accessed 2026-10-09.
 - Status: "OpenAI is deprecating graders as part of the evals and fine-tuning workflows they support."
 - Types and descriptions: string_check ("Use these basic string operations to return a 0 or 1."); text_similarity ("...evaluate how close the model-generated output is to the reference"); score_model ("A score model grader will take the input and return a numeric score based on the prompt within the given range."); python ("This grader allows you to execute arbitrary python code to grade the model output."); multi ("A `multigrader` object combines the output of multiple graders to produce a single score." - "only used for Reinforcement fine-tuning"). label_model: ABSENT from this guide (check the Evals API reference).
 - string_check operations: eq, ne (bullet list says neq; schema says ne - page inconsistent), like, ilike.
 - text_similarity evaluation_metric: fuzzy_match, bleu, gleu, meteor, cosine, rouge_1..rouge_5, rouge_l (cosine "Only available for evals").
 - Model grader advice: "Writing grader prompts is an iterative process."; range: "The output of the grader will be truncated to the given `range`, and default to 0 for all non-numeric outputs."; "Provide few-shot examples of great, fair, and poor answers in the prompt."; "run multiple candidate responses and ground truths through your LLM judge to ensure grading is stable"; reward hacking: "A model that's hacked the grader will score highly on model grader evals but score poorly on expert human evaluations."
 - Python grader limits: "<256kB", no network access, "limited to 2 minutes", 2Gb memory, 1Gb disk, 2 CPU cores.

### A2-iv Evals API reference (grader object names)
Source: OpenAI, "Create eval | OpenAI API Reference", https://developers.openai.com/api/reference/resources/evals/methods/create
(302 from platform.openai.com/docs/api-reference/evals/create). OD. Accessed 2026-10-09.
 - testing_criteria grader objects shown: "LabelModelGrader" ("A LabelModelGrader object which uses a model to assign labels to each item in the evaluation."), "StringCheckGrader", "TextSimilarityGrader", then "or 2 more" (not expanded in the extracted text). Exact `type` strings were not shown in the extraction.
 - Combined with A2-iii, grader types confirmed from opened pages: string_check, text_similarity, score_model, python, multi (Graders guide) and LabelModelGrader (Evals API reference). The `label_model` type string itself: NOT FOUND in extracted text.

### A2-v seed / reproducibility
 - Chat Completions reference https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create (title "Create chat completion | OpenAI API Reference"): extraction truncated; `seed` text NOT FOUND there.
 - Source used instead: OpenAI, "Advanced usage | OpenAI API", https://developers.openai.com/api/docs/guides/advanced-usage, section "Reproducible outputs". OD. Accessed 2026-10-09.
   "Chat Completions are non-deterministic by default (which means model outputs may differ from request to request)."
   Instruction: "Set the seed parameter to any integer of your choice" and reuse it across requests.
   Outputs described as "(mostly) deterministic".
   "Sometimes, determinism may be impacted due to necessary changes OpenAI makes to model configurations on our end."
   system_fingerprint: "If this value is different, you may see different outputs due to changes we've made on our systems."
   The extraction reported that the exact phrases "best effort" and "not guaranteed" do NOT appear on this guide page, and no Beta/deprecated label was shown.
   (The API-reference wording of `seed`, which may contain "best effort", was NOT FOUND because the page extraction was truncated.)

TOOL CAVEAT discovered: WebFetch's extractor said it is limited to quotes of about 125 characters from a source. Longer quotes above were returned anyway, but any long quote should be treated as "near-verbatim" until checked in a browser.

Note: curl to arxiv.org was ALSO refused by the egress policy (403). No further curl web access attempted.

## A3. Zheng et al. 2023, "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (arXiv 2306.05685)
Source opened: https://arxiv.org/pdf/2306.05685 (resolved to v4). Page-1 header: "arXiv:2306.05685v4 [cs.CL] 24 Dec 2023".
Venue (page-1 line): "37th Conference on Neural Information Processing Systems (NeurIPS 2023) Track on Datasets and Benchmarks." -> Class PR (NeurIPS 2023 D&B track).
Agreement, Table 5, caption "Agreement between two types of judges on MT-bench." S1 = ties and position-inconsistent votes counted as ties (random baseline 33%); S2 = non-tie votes only (random baseline 50%). Cells: agreement % (number of votes).
 Table 5(a) FIRST turn, S1 / S2:
  GPT-4 pairwise vs human: 66% (1343) / 85% (859)
  GPT-4 single-answer vs human: 60% (1280) / 85% (739)
  Human vs human: 63% (721) / 81% (479)
 Table 5(b) SECOND turn, S1 / S2:
  GPT-4 pairwise vs human: 66% (1325) / 85% (864)
  GPT-4 single-answer vs human: 59% (1285) / 84% (776)
  Human vs human: 67% (707) / 82% (474)
 Text (Sec. 4.2): "reaches 85%, which is even higher than the agreement among humans (81%)." (first turn, S2).
 Abstract: "achieving over 80% agreement, the same level of agreement between humans."
Position bias: Table 2 (repeated as Table 9), GPT-4 default prompt: Consistency 65.0%, Biased toward first 30.0%, Biased toward second 5.0%, Error 0.0%.
 Table 12, GPT-4 few-shot: Consistency 77.5%, Biased toward first 10.0%, Biased toward second 12.5%, Error 0.0%.
 Sec. 3.4: "increase the consistency of GPT-4 from 65.0% to 77.5%." -> EXPECTATION CONFIRMED (65.0% -> 77.5%).
Verbosity ("repetitive list" attack), Table 3, caption "Failure rate under "repetitive list" attack for different LLM judges on 23 answers.": Claude-v1 91.3%, GPT-3.5 91.3%, GPT-4 8.7%.
Self-enhancement (Sec. 3.3, Fig. 3(b)): "For example, GPT-4 favors itself with a 10% higher win rate; Claude-v1 favors itself with a 25% higher win rate."
 Caveats: "However, they also favor other models and GPT-3.5 does not favor itself." and "Due to limited data and small differences, our study cannot determine whether the models exhibit a self-enhancement bias."
 (The paper writes "10% higher win rate"; it is a difference in win rate, i.e. percentage points; underlying win rates not given in text.)
Math/reasoning grading, Table 4, caption "Judge failure rate on 10 math questions with different prompts.": Default 14/20 (70%); CoT 6/20 (30%); Reference 3/20 (15%).
 Sec. 3.4: "a significant improvement in failure rate (from 70% to 15%) over the default prompt." (reference-guided). 20 = 10 questions x 2 orders (inferred, not spelled out).

## A6. Miller 2024, "Adding Error Bars to Evals" (arXiv 2411.00640)
Source opened: https://arxiv.org/html/2411.00640 (header "arXiv:2411.00640v1 [stat.AP] 01 Nov 2024").
Author/affiliation: Evan Miller, Anthropic ([email removed]).
Venue: NO venue/conference/workshop statement in the HTML text -> treat as preprint (PP); arXiv abs Comments field not opened (budget).
Recommendations (Sec. 1, numbered list), near-verbatim:
 1. "Computing standard errors of the mean using the Central Limit Theorem"
 2. "When questions are drawn in related groups, computing clustered standard errors"
 3. "Reducing variance by resampling answers and by analyzing next-token probabilities"
 4. "When two models are being compared, conducting statistical inference on the question-level paired differences, rather than the population-level summary statistics"
 5. "Using power analysis to determine whether an eval (or a random subsample) is capable of testing a hypothesis of interest"
Other reporting advice: Sec. 2.1 "We suggest reporting the standard error of the mean alongside (beneath) the mean when reporting eval scores."; Table 2 caption "We suggest two new reporting practices: including the number of questions in each eval, and the standard error of each estimate in parentheses"; Table 3 caption "We suggest including the cluster count alongside the question count when reporting cluster-adjusted standard errors"; Sec. 2.1 "we regard bootstrapping as unnecessary unless a complicated sampling scheme or estimator is being used."; Sec. 3.3 "In neither case should the sampling temperature be adjusted for the sake of reducing variance in the scores."
SE formula, Eq. (1), Sec. 2.1: SE_CLT = sqrt(Var(s)/n) = sqrt( [ (1/(n-1)) * sum_i (s_i - s_bar)^2 ] / n ). Eq. (2) binary scores: SE_Bernoulli = sqrt( s_bar (1 - s_bar) / n ).
Clustering: Table 4 caption "Analyzing the same data, clustered standard errors can be over 3X larger than naive standard errors."; Sec. 2.2 "the cluster adjustment in our real-world example is far from trivial (up to 3X)." Table 4 ratios: DROP 3.05 (clustered 1.34 vs naive 0.44), RACE-H 1.10, MGSM 1.88. Only DROP exceeds 3x.
Paired: Sec. 4.2 "We can thus reduce the variance with paired differences as long as the conditional means of the model scores are correlated"; Var(mu_paired) = Var(mu_unpaired) - 2 Cov(x_A, x_B)/n; example "Suppose that the model scores have a correlation coefficient of 0.5."

## A8a. Farquhar et al. 2024, Nature 630, "Detecting hallucinations in large language models using semantic entropy"
Source opened: https://www.nature.com/articles/s41586-024-07421-0 (PR, Nature). Page text 101,531 chars; first 100,000 read (last 1,531, likely references/end matter, not read).
Samples: "We use ten generations to compute entropy" (Results, "Detecting confabulations in QA and math").
 Methods ("Generating a set of answers from the model"): "we sample at temperature 1 using nucleus sampling (P = 0.9) and top-K sampling (K = 50)"; plus one low-temperature (0.1) generation used as the "best generation" for accuracy.
Same meaning: "A sequence, s, means the same thing as a second sequence, s', only if the sequences entail (that is, logically imply) each other" (Methods, "Clustering by semantic equivalence").
 Entailment models: "We rely on language models to predict entailment, such as DeBERTa-Large-MNLI, or general-purpose LLMs such as GPT-3.5" ; LLaMA 2 and GPT-4 also listed under "Entailment estimator"; "We settle on using GPT-3.5 with the above prompt" (Methods, "Entailment estimator"; Supplementary Note 2).
 (Extractor also said the biography experiments use DeBERTa with a "non-defeating" bidirectional check; flag: verify before citing.)
Formula: Eq. 2 P(c|x) = sum_{s in c} P(s|x). Eq. 5 SE(x) ~= - sum_i P(C_i|x) log P(C_i|x), with P(C_i|x) = P(c_i|x) / sum_c P(c|x) (normalised over sampled clusters). "Without this normalization step cluster 'probabilities' could exceed one because of length normalization."
 Discrete semantic entropy: "we approximate P(C_i|x) directly from the number of generations in each cluster." ... "results in similar performance empirically."
Headline: "Averaged across the 30 combinations of tasks and models we study, semantic entropy achieves the best AUROC value of 0.790." Baselines: "naive entropy (0.691), P(True) (0.698) and the embedding regression baseline (0.687) lag behind it." Fig. 2 caption: "Semantic entropy outperforms leading baselines and naive entropy." ... "Results are an average over five datasets."
Confabulation: "we focus on a subset of hallucinations which we call 'confabulations' for which LLMs fluently make claims that are both wrong and arbitrary" ... "by which we mean that the answer is sensitive to irrelevant details such as random seed".
Limitations: "when LLMs are consistently wrong as a result of being trained on erroneous data"; method "does not guarantee factuality because it does not help when LLM outputs are systematically bad"; Discussion: "Our method explicitly does not directly address situations in which LLMs are confidently wrong"; clustering: "This highlights the importance of context and judgement in clustering"; evaluations are "a lower bound on the effectiveness of semantic entropy"; "Care should be taken comparing very different models and contexts". Cost: main text only points to Supplementary Note 3 for "the computational cost and choosing the number of generations" -> quantified cost NOT FOUND in main text.

## A10. Thinking Machines Lab, "Defeating Nondeterminism in LLM Inference"
Source opened: https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ (VB, Connectionism blog). Author Horace He "in collaboration with others at Thinking Machines"; Sep 10, 2025.
Cause: "concurrency + floating point" hypothesis "is not entirely wrong, it doesn't reveal the full picture"; "concurrency (and atomic adds) end up being completely uninvolved in LLM inference nondeterminism"; primary cause: "our forward pass lacks "batch invariance"" and "the load (and thus batch-size) nondeterministically varies!"
Experiment: Qwen/Qwen3-235B-A22B-Instruct-2507; 1,000 completions at temperature 0, 1,000 tokens each; prompt "Tell me about Richard Feynman" (non-thinking mode). "we generate 80 unique completions, with the most common of these occuring 78 times." First divergence at token 103: 992 "Queens, New York" vs 8 "New York City". With batch-invariant kernels: all 1,000 completions identical.
Fix: batch-invariant kernels for RMSNorm, matmul and attention (fixed-size split-KV); vLLM demo (FlexAttention backend, torch.Library); library "thinking-machines-lab/batch-invariant-ops". Cost: matmul "we only lose about 20% performance compared to cuBLAS"; end-to-end Qwen-3-8B, 1,000 sequences, one GPU: default vLLM 26 s, unoptimized deterministic 55 s, improved attention kernel 42 s; "performance is not *disastrous*."
RL: "the different numerics between training and inference implicitly turns our on-policy RL into off-policy RL."; deterministic inference -> "KL-divergence stays flat at 0".

Lookups used so far: ~22 (incl. 2 refused curl attempts and 7 redirect-only WebFetch responses).

## A4. Wang et al., "Large Language Models are not Fair Evaluators" (arXiv 2305.17926)
Source opened: ACL Anthology, https://aclanthology.org/2024.acl-long.511/ (PR).
Venue: "Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)", ACL 2024, August 2024, Bangkok, Thailand, pages 9440-9450.
Authors: Peiyi Wang, Lei Li, Liang Chen, Zefan Cai, Dawei Zhu, Binghuai Lin, Yunbo Cao, Lingpeng Kong, Qi Liu, Tianyu Liu, Zhifang Sui.
Abstract (ACL version) quotes: "uncover a positional bias in the evaluation paradigm of adopting large language models (LLMs)"; HEADLINE: "Vicuna-13B could beat ChatGPT on 66 over 80 tested queries with ChatGPT as an evaluator."; "We propose a simple yet effective calibration framework to address our discovered positional bias."; "Extensive experiments demonstrate that our approach successfully alleviates evaluation bias".
Paraphrase (not quote): ranking can be manipulated just by changing order of candidate responses; authors manually annotated win/tie/lose for ChatGPT vs Vicuna-13B on Vicuna Benchmark questions.
Calibration method NAMES: not in the ACL abstract (it only says "calibration framework") - see arXiv follow-up below.

## A5. Panickssery, Bowman, Feng, "LLM Evaluators Recognize and Favor Their Own Generations" (arXiv 2404.13076)
Source opened: https://arxiv.org/abs/2404.13076. Only v1, submitted Mon 15 Apr 2024. Comments: none. Journal ref: none. -> arXiv page shows no venue (PP on this evidence).
Abstract (extractor quoted one phrase; rest paraphrased by extractor): "self-recognition capability contributes to self-preference." Models named in abstract: GPT-4 and Llama 2. Paraphrase: they distinguish their own text from other LLMs' and humans' text with non-trivial accuracy out of the box; fine-tuning shows a (linear) correlation between self-recognition and self-preference strength; controlled experiments suggest a causal link not explained by simple confounders. Datasets and numbers: not in abstract.

## A8b. Kuhn, Gal, Farquhar 2023, "Semantic Uncertainty..." (arXiv 2302.09664)
Source opened: https://arxiv.org/abs/2302.09664. Latest v3, 2023-04-15. Comments: none. Journal ref: none. Venue not shown on arXiv abs page (see follow-up).

## A8c. Kossen et al. 2024, "Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs" (arXiv 2406.15927)
Source opened: https://arxiv.org/abs/2406.15927. Only v1, 2024-06-22. Comments: none. Journal ref: none -> preprint, no venue found (PP).
Authors: Jannik Kossen, Jiatong Han, Muhammed Razzak, Lisa Schut, Shreshth Malik, Yarin Gal.
Abstract quotes (segments verbatim): "We propose semantic entropy probes (SEPs), a cheap and reliable method for uncertainty quantification" "in Large Language Models (LLMs)."; "However, the 5-to-10-fold increase in computation cost associated with SE computation hinders practical adoption."; "To address this, we propose SEPs, which directly approximate SE from the hidden states of a single generation."; "SEPs are simple to train and do not require sampling multiple model generations at test time," "reducing the overhead of semantic uncertainty quantification to almost zero."; "We show that SEPs retain high performance for hallucination detection and generalize better" "to out-of-distribution data than previous probing methods that directly predict model accuracy."; "Our results across models and tasks suggest that model hidden states capture SE,".

## A9a. Zhang et al. 2024, GSM1k (arXiv 2405.00332)
Source opened: https://arxiv.org/abs/2405.00332 -> shows v4, "This version" 2024-11-22, submitted 2024-05-01. Comments/Journal ref: not shown in extraction -> no venue found on arXiv page.
Latest (v4) abstract: "accuracy drops of up to 8%"; memorization: "a positive relationship (Spearman's r^2 = 0.36)" between a model's "probability of generating an example from GSM8k" and its GSM8k-GSM1k performance gap; "suggesting that some models may have partially memorized GSM8k".
Source opened: https://arxiv.org/abs/2405.00332v1 (v1, 2024-05-01): extraction returned the SAME numbers: "we observe accuracy drops of up to 8%" and "Further analysis suggests a positive relationship (Spearman's r^2 = 0.36)". Note the statistic is labelled r^2, not r.
Caveat: WebFetch is a summarizer; a v1-PDF check was planned to confirm no version difference (see follow-up).

## A9b. Shankar et al. 2024, "Who Validates the Validators?" (arXiv 2404.12272)
Source opened: https://arxiv.org/abs/2404.12272. Only v1, 2024-04-18. Comments: none. Journal ref: none. DOI: none -> no venue shown on arXiv page.
Authors: Shreya Shankar, J. D. Zamfirescu-Pereira, Bjorn Hartmann, Aditya G. Parameswaran, Ian Arawjo.
Criteria drift (abstract): "users need criteria to grade outputs, but grading outputs helps users define criteria."; "some criteria appears dependent on the specific LLM outputs observed" (rather than criteria that "can be defined a priori"), "rais[ing] serious questions" for approaches that assume evaluation is independent of observed outputs. (The phrase "criteria drift" itself was not returned in the abstract extraction.)

Lookups used so far: ~29.

A4 follow-up: https://arxiv.org/abs/2305.17926 opened. Latest v2, 2023-08-30. Comments: none; Journal ref: none.
 Calibration strategies named in arXiv abstract: "Multiple Evidence Calibration", "Balanced Position Calibration", "Human-in-the-Loop Calibration".
 Headline (same in arXiv abstract): "Vicuna-13B could beat ChatGPT on 66 over 80 tested queries with ChatGPT as an evaluator."
 Peer review: PR via ACL 2024 Long Papers (ACL Anthology page above), although arXiv page lists no venue.

## A7. Statistics references

### A7(a) Wilson score interval
Source opened: NIST/SEMATECH e-Handbook of Statistical Methods, section "7.2.4.1. Confidence intervals", https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm (OD, US government reference). Accessed 2026-10-09.
 Formulas ("Formulas for the confidence intervals"), as extracted:
  U.L. = [ p_hat + z^2_{1-a/2}/(2n) + z_{1-a/2} * sqrt( p_hat(1-p_hat)/n + z^2_{1-a/2}/(4n^2) ) ] / [ 1 + z^2_{1-a/2}/n ]
  L.L. = [ p_hat + z^2_{a/2}/(2n) + z_{a/2} * sqrt( p_hat(1-p_hat)/n + z^2_{a/2}/(4n^2) ) ] / [ 1 + z^2_{a/2}/n ]   (z_{a/2} is negative, giving the lower limit)
  Contrasted "common" expression: p_hat +/- z_{1-a/2} sqrt(p_hat(1-p_hat)/n).
 Naming: "Wilson method", "introduced by Wilson (1927), recommended by Brown, Cai and DasGupta (2001) and Agresti and Coull (1998)"; "common practice in the statistics literature is to refer to the method given here as the Wilson method" (handbook formerly called it "Agresti-Coull method").
 On the normal-approximation interval: lower limit can be negative ("an inferior approach"); "symmetical [sic] confidence limits that are approximated using the normal distribution may not be accurate enough for some applications" when "the number of failures is very small or if the sample size N is very small." Page does not use the name "Wald".
Brown, Cai & DasGupta 2001: Project Euclid page https://projecteuclid.org/journals/statistical-science/volume-16/issue-2/Interval-Estimation-for-a-Binomial-Proportion/10.1214/ss/1009213286.full returned a bot-protection (Incapsula) challenge -> NOT FOUND there. (Alternative tried below.)

### A7(b) McNemar
Source opened: Fagerland, Lydersen & Laake 2013, "The McNemar test for binary matched-pairs data: mid-p and asymptotic are better than exact conditional", BMC Medical Research Methodology 13:91, https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-91 (PR; page marked "Open Access", CC BY; has "Peer Review reports" link).
 Discordant pairs: "The asymptotic McNemar test conditions on the number of discordant pairs"; statistic z = (n12 - n21)/sqrt(n12 + n21), chi^2 = (n12 - n21)^2/(n12 + n21) (symbols garbled in extraction; formula reconstructed by extractor - verify on page).
 Exact conditional: "The conditional probability under H 0 of observing any outcome x 12 given n=n 12+n 21 discordant pairs" (binomial, p = 1/2; two-sided p = twice one-sided - paraphrase).
 On exact conditional test: "Quite often, the type I error rates of the exact conditional test were half that of the nominal level or lower."; "This conservatism leads to poor power and a need for unnecessary large sample sizes."
 Recommendations: Abstract: "The easy-to-calculate mid-p test is an excellent alternative to the complex exact unconditional test."; "We also recommend the asymptotic test if small but frequent violations of the nominal level is acceptable." Conclusions: "The most powerful test is the McNemar asymptotic test (without CC), which we recommend if small but frequent violations of the nominal level is acceptable."; "We do not recommend use of the McNemar exact conditional test nor the asymptotic test with CC in any situation."; asymptotic test without CC "performs surprisingly well, even for quite small sample sizes." No numeric sample-size threshold given.

### A7(c) Cohen's kappa / McHugh 2012
 PMC page https://pmc.ncbi.nlm.nih.gov/articles/PMC3900052/ returned a reCAPTCHA "Checking your browser" page -> NOT FOUND there. (Alternative tried below.)

### A7(e) scikit-learn user guide
Source opened: "3.4. Metrics and scoring: quantifying the quality of predictions - scikit-learn 1.9.1 documentation", https://scikit-learn.org/stable/modules/model_evaluation.html (OD).
 Sec. 3.4.4.9.1 Binary classification: precision = tp/(tp + fp); recall = tp/(tp + fn).
 "F-measure is the weighted harmonic mean of precision and recall, with precision's contribution to the mean weighted by some parameter beta": F_beta = (1 + beta^2) * (precision x recall)/(beta^2 precision + recall); computed as F_beta = (1 + beta^2) tp / ((1 + beta^2) tp + fp + beta^2 fn) "To avoid division by zero when precision and recall are zero".
 F1: "With beta = 1, F_beta and F_1 are equivalent, and the recall and the precision are equally important." (explicit 2PR/(P+R) form NOT printed on the page).
 Cohen's kappa (Sec. 3.4.4.5): formula NOT on this page; "The kappa score is a number between -1 and 1. Scores above .8 are generally considered good agreement; zero or lower means no agreement (practically random labels)."; intended "to compare labelings by different human annotators, not a classifier versus a ground truth." No Cohen (1960) citation on this page.

## A11. Chen et al. 2021, "Evaluating Large Language Models Trained on Code" (arXiv 2107.03374)
Source opened: https://arxiv.org/pdf/2107.03374 (page-1 stamp "arXiv:2107.03374v2 [cs.LG] 14 Jul 2021"). No venue statement in the PDF -> preprint, no venue found (PP). (arXiv abs Comments field not opened.)
 Eq. (1), Sec. 2.1: pass@k := E_Problems[ 1 - C(n-c, k) / C(n, k) ], n = samples generated per task, c = correct samples ("count the number of correct samples c <= n which pass unit tests").
 "we use n = 200 and k <= 100" (APPS: 1000 samples per task, Sec. 3.5).
 Why: "computing pass@k in this way can have high variance."; "One may be tempted to estimate pass@k with 1-(1-p_hat)^k ... but we show that it is biased in Appendix A."; Appendix A: it "results in a consistent underestimate as shown in Figure 13"; Eq. (1) is unbiased.
 Stability: "Calculating this estimator directly results in very large numbers and numerical instability."; Figure 3 numpy pass_at_k(n, c, k): returns 1.0 if n - c < k, else 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1)).

Lookups used so far: ~36.

A7(a) follow-up, Brown, Cai & DasGupta 2001:
Source opened: author-hosted PDF of the published article, https://www-stat.wharton.upenn.edu/~tcai/paper/Binomial-StatSci.pdf (header "Statistical Science 2001, Vol. 16, No. 2, 101-133"). PR (Statistical Science). Accessed 2026-10-10.
 Abstract: "erratic behavior of the coverage probability of the standard Wald confidence interval has previously been remarked on in the literature"; "the chaotic coverage properties of the Wald interval are far more persistent than is appreciated"; textbook prescriptions "are misleading and defective in several respects and cannot be trusted"; recommend "the Wilson interval or the equal-tailed Jeffreys prior interval for small n" and "the interval suggested in Agresti and Coull for larger n."
 Small n: Sec. 1 "for small n (40 or less)"; Sec. 5 "small n (n <= 40)"; for n > 40 Wilson, Jeffreys and Agresti-Coull are "all very similar" (Sec. 1).
 Sec. 2.2: "the standard interval can have coverage noticeably smaller than its nominal value even for values of n" that are not small; extractor also reported Example 3 (Sec. 2.1): p = 0.005, coverage 0.792 at n = 592 (verify on page before quoting).
 Wilson (Sec. 3.1.1, Eq. 4; extraction garbled, reconstructed): CI_W = (X + k^2/2)/(n + k^2) +/- (k n^{1/2}/(n + k^2)) (p_hat q_hat + k^2/(4n))^{1/2}, k = z_{a/2}; attributed to Wilson (1927).

A7(c) follow-up, McHugh 2012:
Source opened: publisher page, https://www.biochemia-medica.com/en/journal/22/3/10.11613/BM.2012.031 (PR; Biochem Med (Zagreb) 2012;22(3):276-282; DOI 10.11613/BM.2012.031; author shown as "Marry L. McHugh").
 Formula: printed as an IMAGE -> exact printed form NOT FOUND in text. Terms: "Where Pr(a) represents the actual observed agreement, and Pr(e) represents chance agreement." Pr(e) computed from row/column marginals; "n represents the number of observations (not the number of raters)."
 Cohen 1960: Abstract "In 1960, Jacob Cohen critiqued use of percent agreement due to its inability to account for chance agreement."; text "developed the key statistic for measurement of interrater reliability, Cohen's kappa (5), in the 1960s."; ref 5 = Cohen J. "A coefficient of agreement for nominal scales." Educ Psychol Meas 1960;20:37-46.
 Interpretation bands: Landis and Koch are NOT named in the text. The paper attributes the familiar bands to Cohen: "Cohen suggested the Kappa result be interpreted as follows": <=0 no agreement; 0.01-0.20 none to slight; 0.21-0.40 fair; 0.41-0.60 moderate; 0.61-0.80 substantial; 0.81-1.00 almost perfect.
 Criticism: "this interpretation allows for very little agreement among raters to be described as "substantial"."; abstract: Cohen's interpretation "may be too lenient for health related studies because it implies that a score as low as 0.41 might be acceptable."
 Own levels: Table 3 is an IMAGE -> exact ranges/labels/% reliable NOT FOUND in text. Text: "any kappa below 0.60 indicates inadequate agreement among the raters and little confidence should be placed in the study results."; "When agreement is less than 80%, over 20% of the data being analyzed are erroneous."; for kappa 0.50-0.60 "40% to 50% of the data being analyzed are erroneous"; "many texts recommend 80% agreement as the minimum acceptable interrater agreement."
 Kappa formula with Cohen-1960 origin: the formula kappa = (p_o - p_e)/(1 - p_e) as TEXT was NOT FOUND on any opened page (McHugh prints it as an image; scikit-learn user guide does not print it). Terms and Cohen 1960 attribution are confirmed.

### A7(d) Fawcett 2006
Source opened: PDF copy of the journal article hosted on an ELTE university staff page, https://people.inf.elte.hu/kiss/11dwhdm/roc.pdf (shows "An introduction to ROC analysis", Tom Fawcett, Pattern Recognition Letters 27 (2006) 861-874). PR (content), third-party host.
 Sec. 7 (Area under an ROC curve): "the AUC of a classifier is equivalent to the probability that the classifier will rank a randomly chosen positive instance" "higher than a randomly chosen negative instance."
 "This is equivalent to the Wilcoxon test of ranks" (citing Hanley and McNeil, 1982). Mann-Whitney not named.

A8b follow-up: https://arxiv.org/pdf/2302.09664v3 opened: extraction found NO arXiv stamp and NO venue statement on page 1 -> venue still NOT FOUND (see final attempt below).

A5 follow-up: https://arxiv.org/html/2404.13076v1 opened (100,000 of 100,544 chars read).
 Venue: no venue statement; keywords line reads "Machine Learning, ICML" (template keywords, not an acceptance statement).
 Models (Sec. 2.1): "Llama-2-7b-chat", "GPT-3.5", "GPT-4". Datasets (Sec. 2.1): "XSUM" and "CNN/DailyMail", 1,000 articles sampled from each.
 Key numbers: Introduction: "GPT-4 is 73.5% accurate distinguishing itself from two other LLMs and humans." Table 7 (pairwise, out of the box; averaged confidence scores, not accuracy): GPT-4 self-recognition 0.672 (XSUM), 0.747 (CNN); GPT-4 self-preference 0.705 (XSUM), 0.912 (CNN); GPT-3.5 self-preference 0.582 / 0.431; Llama-2-7b 0.511 / 0.505.
 Fine-tuning: "strong linear correlation" (Sec. 3.2, Figs. 1 and 7), no single coefficient given; Table 1 example-level Kendall's tau, e.g. GPT-3.5 on XSUM 0.41 (no fine-tuning) -> 0.74 (fine-tuned on 500 examples) (as extracted; verify).
 Abstract: "we discover a linear correlation between self-recognition capability and the strength of self-preference bias"

Lookups used so far: ~41.

A8b final attempt: OpenReview forum page https://openreview.net/forum?id=VD-AYtP0dve returned a "Verifying your browser | OpenReview" page with no paper content -> Kuhn et al. venue NOT FOUND.

## Lookup log (total 42; no WebSearch used)
 1 curl export.arxiv.org API (refused, egress policy)      22 WebFetch arxiv html 2411.00640 (Miller)
 2 WebFetch docs.claude.com develop-tests (redirect)       23 WebFetch aclanthology 2024.acl-long.511 (Wang)
 3 WebFetch docs.claude.com define-success (redirect)      24 WebFetch arxiv abs 2405.00332 (GSM1k latest)
 4 WebFetch docs.claude.com api/messages (redirect)        25 WebFetch arxiv abs 2405.00332v1
 5 WebFetch platform.claude.com develop-tests              26 WebFetch arxiv abs 2404.12272 (Shankar)
 6 WebFetch platform.claude.com api/messages (no temp)     27 WebFetch arxiv abs 2302.09664 (Kuhn)
 7 WebFetch platform.claude.com api/messages/create        28 WebFetch arxiv abs 2406.15927 (Kossen)
 8 WebFetch platform.openai.com eval best practices (redir) 29 WebFetch arxiv abs 2404.13076 (Panickssery)
 9 WebFetch platform.openai.com evals guide (redirect)     30 WebFetch arxiv abs 2305.17926 (Wang)
10 WebFetch developers.openai.com best practices           31 WebFetch BMC Fagerland 2013
11 WebFetch developers.openai.com evals guide              32 WebFetch PMC McHugh (reCAPTCHA, failed)
12 WebFetch developers.openai.com graders                  33 WebFetch scikit-learn model_evaluation
13 WebFetch platform.openai.com evals create (redirect)    34 WebFetch NIST e-Handbook 7.2.4.1
14 WebFetch platform.openai.com chat create (redirect)     35 WebFetch Project Euclid Brown et al. (bot wall, failed)
15 WebFetch developers.openai.com evals create ref         36 WebFetch arxiv pdf 2107.03374 (Chen)
16 WebFetch developers.openai.com chat create ref (trunc.) 37 WebFetch biochemia-medica.com McHugh
17 WebFetch developers.openai.com advanced-usage           38 WebFetch wharton.upenn.edu Brown et al. PDF
18 curl arxiv.org abs (refused, egress policy)             39 WebFetch elte.hu Fawcett PDF
19 WebFetch arxiv pdf 2306.05685 (Zheng)                   40 WebFetch arxiv pdf 2302.09664v3 (Kuhn)
20 WebFetch nature.com s41586-024-07421-0                  41 WebFetch arxiv html 2404.13076v1 (Panickssery)
21 WebFetch thinkingmachines.ai blog                       42 WebFetch openreview VD-AYtP0dve (bot wall, failed)
# Research A (methods): claim tables

How this was gathered: all page content came through WebFetch (40 calls, 7 of them redirect notices). curl to export.arxiv.org and arxiv.org was refused by this session's egress policy (403) and was not retried. No WebSearch was used. Total lookups: 42. WebFetch returns a model's extraction of the page and says it caps quotes at about 125 characters, so long quotes are near-verbatim, and formulas marked "reconstructed" were rebuilt from garbled PDF text. Check any load-bearing long quote in a browser before printing it. Full notes: /tmp/claude-0/-home-claude/90458136-4335-5a63-afc3-c1753bd527bc/scratchpad/p02/research-a-methods.md

Class codes: OD official documentation; PR peer-reviewed; PP preprint; VB vendor blog; PB personal blog.

## A1. Anthropic documentation

Sources:
- AN-EV: Anthropic, "Define success criteria and build evaluations", Claude Platform Docs, accessed 2026-10-09, https://platform.claude.com/docs/en/test-and-evaluate/develop-tests (docs.claude.com .../develop-tests AND .../define-success both 302-redirect to this one combined page)
- AN-API: Anthropic, "Create a Message", Claude API Reference, accessed 2026-10-09, https://platform.claude.com/docs/en/api/messages/create

| ID | Claim, stated narrowly | Source | Class | Location | Verbatim quote or exact numbers | Conf | Notes |
|---|---|---|---|---|---|---|---|
| A1-1 | Names three grading methods; pick the fastest, most reliable, most scalable | AN-EV | OD | "Grade your evaluations" | "When deciding which method to use to grade evals, choose the fastest, most reliable, most scalable method:" (code-based, human, LLM-based) | 9 | Docs as of Oct 2026 |
| A1-2 | Code-based grading trade-off | AN-EV | OD | same | "Fastest and most reliable, extremely scalable, but also lacks nuance for more complex judgments that require less rule-based rigidity." Examples: "Exact match: output == golden_answer"; "String match: key_phrase in output" | 8 | |
| A1-3 | Human grading trade-off | AN-EV | OD | same | "Most flexible and high quality, but slow and expensive. Avoid if possible." | 9 | |
| A1-4 | LLM-based grading trade-off | AN-EV | OD | same | "Fast and flexible, scalable and suitable for complex judgment. Test to ensure reliability first then scale." | 9 | |
| A1-5 | More auto-graded cases beat fewer hand-graded ones | AN-EV | OD | "Eval design principles" | "Prioritize volume over quality: More questions with slightly lower signal automated grading is better than fewer questions with high-quality human hand-graded evals." | 8 | |
| A1-6 | Mirror the real task distribution and include edge cases | AN-EV | OD | same | "Be task-specific: Design evals that mirror your real-world task distribution. Don't forget to factor in edge cases!" Listed examples: "Irrelevant or nonexistent input data"; "Overly long input data or user input [Chat use cases]"; "Poor, harmful, or irrelevant user input"; "Ambiguous test cases where even humans would find it hard to reach an assessment consensus" | 8 | |
| A1-7 | Automate grading; use Claude to expand a seed set of cases | AN-EV | OD | same | "Automate when possible: Structure questions to allow for automated grading (for example, multiple-choice, string match, code-graded, LLM-graded)."; "Writing hundreds of test cases can be hard to do by hand! Get Claude to help you generate more from a baseline set of example test cases." | 8 | |
| A1-8 | Good success criteria: specific, measurable, achievable, relevant | AN-EV | OD | "Define your success criteria" | Specific: "Clearly define what you want to achieve. Instead of "good performance," specify "accurate sentiment classification.""; Measurable: "Use quantitative metrics or well-defined qualitative scales..."; Achievable: "Base your targets on industry benchmarks, prior experiments, AI research, or expert knowledge..."; Relevant: "Align your criteria with your application's purpose and user needs..." | 8 | "Common success criteria" (non-exhaustive): task fidelity, consistency, relevance and coherence, tone and style, privacy preservation, context utilization, latency, price |
| A1-9 | LLM grading: detailed, clear rubrics | AN-EV | OD | "Tips for LLM-based grading" | "Have detailed, clear rubrics: "The answer should always mention 'Acme Inc.' in the first sentence. If it does not, the answer is automatically graded as 'incorrect.'"" | 8 | Also: a use case "might require several rubrics for holistic evaluation" |
| A1-10 | LLM grading: constrained output (label or scale) | AN-EV | OD | same | "Empirical or specific: For example, instruct the LLM to output only 'correct' or 'incorrect', or to judge from a scale of 1-5. Purely qualitative evaluations are hard to assess quickly and at scale." | 8 | Example grader prompt ends: "Output 'correct' or 'incorrect' in <result> tags." |
| A1-11 | LLM grading: grader reasons before scoring (thinking on) | AN-EV | OD | same | "Encourage reasoning: Use a grader model with thinking on, so that it reasons before it produces an evaluation score. This increases evaluation performance, particularly for tasks requiring complex judgment." | 8 | No "discard the reasoning" wording came back from the current page |
| A1-12 | Grade with a different model than the one that generated | AN-EV | OD | code comment in "Example evals" | "Generally best practice to use a different model to evaluate than the model used to generate the evaluated output" | 7 | A code comment, not body text |
| A1-13 | Temperature 0 is not fully deterministic | AN-API | OD | `temperature` parameter | "Note that even with `temperature` of `0.0`, the results will not be fully deterministic." | 9 | |
| A1-14 | `temperature` is deprecated for the newest Claude models | AN-API | OD | same | "Deprecated. Models released after Claude Opus 4.6 do not support setting temperature. A value of 1.0 will be accepted for backwards compatibility, all other values will be rejected with a 400 error." Default 1.0; range 0.0 to 1.0 | 8 | As of Oct 2026. "Set temperature 0 for evals" advice cannot be followed on these models |

## A2. OpenAI documentation

Sources (all OD, accessed 2026-10-09; platform.openai.com URLs now 302-redirect to developers.openai.com):
- OA-BP: OpenAI, "Evaluation best practices", https://developers.openai.com/api/docs/guides/evaluation-best-practices
- OA-EV: OpenAI, "Working with evals", https://developers.openai.com/api/docs/guides/evals
- OA-GR: OpenAI, "Graders", https://developers.openai.com/api/docs/guides/graders
- OA-REF: OpenAI, "Create eval", OpenAI API Reference, https://developers.openai.com/api/reference/resources/evals/methods/create
- OA-ADV: OpenAI, "Advanced usage", section "Reproducible outputs", https://developers.openai.com/api/docs/guides/advanced-usage

| ID | Claim, stated narrowly | Source | Class | Location | Verbatim quote or exact numbers | Conf | Notes |
|---|---|---|---|---|---|---|---|
| A2-1 | Recommended five-step process | OA-BP | OD | "Design your eval process" | 1 "Define eval objective. What's the success criteria for the eval?" 2 "Collect dataset. Which data will help you evaluate against your objective?" 3 "Define eval metrics. How will you check that the success criteria are met?" 4 "Run and compare evals. Iterate and improve model performance for your task or system." 5 "Continuously evaluate. Set up continuous evaluation (CE) to run evals on every change" | 8 | |
| A2-2 | Three evaluator families and trade-offs | OA-BP | OD | "Create and combine different types of evaluators" | Metric-based: "Quantitative evals provide a numerical score you can use to filter and rank results." (challenge "May not be tailored to specific use cases, may miss nuance."); Human: "Human judgment evals provide the highest quality but are slow and expensive." (challenge "Disagreement among human experts, expensive, slow."); LLM-as-a-judge: "Using models to judge output is cheaper to run and more scalable than human evaluation." | 8 | |
| A2-3 | Three judging setups | OA-BP | OD | "LLM-as-a-judge and model graders" | "Pairwise comparison: Present the judge model with two responses and ask it to determine which one is better based on specific criteria"; "Single answer grading: The judge model evaluates a single response in isolation, assigning a score or rating based on predefined quality metrics"; "Reference-guided grading: Provide the judge model with a reference or "gold standard" answer" | 8 | |
| A2-4 | Judge biases named, and mitigations | OA-BP | OD | same | "Position bias (response order), verbosity bias (preferring longer responses)."; "Use pairwise comparison or pass/fail for more reliability"; "Control for response lengths as LLMs bias towards longer responses in general"; "Add reasoning and chain-of-thought as reasoning before scoring improves eval performance"; "Use the most capable model to grade if you can."; "The quality of LLM-as-Judge varies depending on problem context" | 8 | Self-enhancement bias not named; no numbers. Page also returned "Start with gpt-6-astra when you need a strong LLM judge" (model name post-dates my knowledge; verify) |
| A2-5 | Calibrate automated graders against human labels | OA-BP | OD | "Anti-patterns"; human-eval section | "Ignoring human feedback: Not calibrating your automated metrics against human evals."; "validate agreement against your human labels before optimizing for cost or latency." | 8 | Also "Vibe-based evals", "Biased design", "Overly generic metrics" anti-patterns |
| A2-6 | Test data should include typical, edge and adversarial cases | OA-BP | OD | edge-case section | "Ensure your test data includes typical cases, edge cases, and adversarial cases." | 8 | No general dataset-size number on the page |
| A2-7 | Evals guide: three steps, two ingredients; platform being deprecated | OA-EV | OD | intro; "Create an eval for a task" | "Describe the task to be done as an eval"; "Run your eval with test inputs (a prompt and input data)"; "Analyze the results, then iterate and improve on your prompt"; "`data_source_config`: A schema for the test data you will use along with the eval."; "`testing_criteria`: The graders that determine if the model output is correct."; "OpenAI is deprecating the Evals platform." | 8 | Only `string_check` appears on this page; no LLM-judge content |
| A2-8 | Grader type names (Graders guide) | OA-GR | OD | Overview | `string_check` ("Use these basic string operations to return a 0 or 1."); `text_similarity`; `score_model` ("...return a numeric score based on the prompt within the given range."); `python` ("...execute arbitrary python code to grade the model output."); `multi` ("only used for Reinforcement fine-tuning") | 8 | "OpenAI is deprecating graders as part of the evals and fine-tuning workflows they support." string_check ops: eq, ne (bullet says neq), like, ilike. text_similarity metrics: fuzzy_match, bleu, gleu, meteor, cosine, rouge_1 to rouge_5, rouge_l |
| A2-9 | Evals API testing_criteria grader objects | OA-REF | OD | `testing_criteria` | "LabelModelGrader" ("A LabelModelGrader object which uses a model to assign labels to each item in the evaluation."), "StringCheckGrader", "TextSimilarityGrader", then "or 2 more" | 6 | Exact `label_model` type string and the 2 unexpanded objects NOT FOUND |
| A2-10 | `seed` gives mostly, not fully, deterministic output | OA-ADV | OD | "Reproducible outputs" | "Chat Completions are non-deterministic by default (which means model outputs may differ from request to request)."; "Set the seed parameter to any integer of your choice"; outputs "(mostly) deterministic"; "Sometimes, determinism may be impacted due to necessary changes OpenAI makes to model configurations on our end."; `system_fingerprint`: "If this value is different, you may see different outputs due to changes we've made on our systems." | 7 | The words "best effort" / "not guaranteed" were NOT FOUND (API reference extraction truncated before `seed`; the guide does not use them) |

## A3. Zheng et al. 2023

Source ZH: Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena", arXiv 2306.05685v4 (24 Dec 2023), https://arxiv.org/pdf/2306.05685

| ID | Claim, stated narrowly | Source | Class | Location | Verbatim quote or exact numbers | Conf | Notes |
|---|---|---|---|---|---|---|---|
| A3-0 | Venue: NeurIPS 2023 Datasets and Benchmarks | ZH | PR | p. 1 | "37th Conference on Neural Information Processing Systems (NeurIPS 2023) Track on Datasets and Benchmarks." | 9 | |
| A3-1 | MT-bench turn 1 agreement | ZH | PR | Table 5(a), "Agreement between two types of judges on MT-bench." | S1 (ties counted, random 33%) / S2 (no ties, random 50%): GPT-4 pairwise vs human 66% (1343 votes) / 85% (859); GPT-4 single-answer vs human 60% (1280) / 85% (739); human vs human 63% (721) / 81% (479) | 8 | Who the human judges were was not re-checked in this run |
| A3-2 | MT-bench turn 2 agreement | ZH | PR | Table 5(b) | S1 / S2: GPT-4 pairwise vs human 66% (1325) / 85% (864); GPT-4 single vs human 59% (1285) / 84% (776); human vs human 67% (707) / 82% (474) | 8 | |
| A3-3 | Headline wording | ZH | PR | Sec. 4.2; abstract | "reaches 85%, which is even higher than the agreement among humans (81%)."; abstract: "achieving over 80% agreement, the same level of agreement between humans." | 8 | 85 vs 81 is turn 1, S2 (no ties) |
| A3-4 | GPT-4 position consistency, default prompt | ZH | PR | Table 2 (repeated as Table 9) | Consistency 65.0%; biased toward first 30.0%; biased toward second 5.0%; error 0.0% | 8 | Expectation 65.0% CONFIRMED |
| A3-5 | Few-shot judging raises consistency | ZH | PR | Table 12; Sec. 3.4 | Consistency 77.5%; first 10.0%; second 12.5%; error 0.0%. "increase the consistency of GPT-4 from 65.0% to 77.5%." | 8 | Expectation 77.5% CONFIRMED |
| A3-6 | Verbosity ("repetitive list") attack | ZH | PR | Table 3, "Failure rate under "repetitive list" attack for different LLM judges on 23 answers." | Claude-v1 91.3%; GPT-3.5 91.3%; GPT-4 8.7% | 8 | n = 23 answers |
| A3-7 | Self-enhancement: observed, but not established | ZH | PR | Sec. 3.3, Fig. 3(b) | "GPT-4 favors itself with a 10% higher win rate; Claude-v1 favors itself with a 25% higher win rate." Caveats: "However, they also favor other models and GPT-3.5 does not favor itself."; "Due to limited data and small differences, our study cannot determine whether the models exhibit a self-enhancement bias." | 8 | "10%" is a win-rate difference (percentage points); underlying rates not in text |
| A3-8 | Math grading failures; CoT and reference-guided fixes | ZH | PR | Table 4, "Judge failure rate on 10 math questions with different prompts."; Sec. 3.4 | Default 14/20 (70%); CoT 6/20 (30%); Reference 3/20 (15%). "a significant improvement in failure rate (from 70% to 15%) over the default prompt." | 8 | 20 = 10 questions x 2 orders (inferred). Judge model for Table 4 not restated in the extraction; check the table |

## A4. Wang et al. 2023/2024

Sources:
- WA-ACL: Wang, Li, Chen, Cai, Zhu, Lin, Cao, Kong, Liu, Liu, Sui, "Large Language Models are not Fair Evaluators", ACL 2024, https://aclanthology.org/2024.acl-long.511/
- WA-AX: same paper, arXiv 2305.17926v2 (2023-08-30), https://arxiv.org/abs/2305.17926

| ID | Claim, stated narrowly | Source | Class | Location | Verbatim quote or exact numbers | Conf | Notes |
|---|---|---|---|---|---|---|---|
| A4-0 | Venue: ACL 2024 main conference, long paper | WA-ACL | PR | Anthology page | "Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)", August 2024, Bangkok, pp. 9440-9450 | 9 | arXiv page lists no Comments/Journal ref |
| A4-1 | Changing answer order alone flips a judge's verdicts | WA-ACL, WA-AX | PR | Abstract | "Vicuna-13B could beat ChatGPT on 66 over 80 tested queries with ChatGPT as an evaluator." | 9 | Judge: ChatGPT; 80 Vicuna Benchmark questions; 2023 models |
| A4-2 | Three calibration strategies | WA-AX | PP (arXiv copy of PR paper) | Abstract, arXiv v2 | "Multiple Evidence Calibration", "Balanced Position Calibration", "Human-in-the-Loop Calibration" | 8 | The ACL abstract names none; it says "a simple yet effective calibration framework" |
| A4-3 | Calibration reduces the bias | WA-ACL | PR | Abstract | "Extensive experiments demonstrate that our approach successfully alleviates evaluation bias" | 8 | No effect sizes checked |

## A5. Panickssery, Bowman and Feng 2024

Source PA: Panickssery, Bowman, Feng, "LLM Evaluators Recognize and Favor Their Own Generations", arXiv 2404.13076v1 (15 Apr 2024), https://arxiv.org/abs/2404.13076 and https://arxiv.org/html/2404.13076v1

| ID | Claim, stated narrowly | Source | Class | Location | Verbatim quote or exact numbers | Conf | Notes |
|---|---|---|---|---|---|---|---|
| A5-0 | Peer-review status | PA | PP | arXiv abs; HTML header | Only v1; Comments: none; Journal ref: none; HTML keywords line "Machine Learning, ICML" (template, not an acceptance note) | 7 | Preprint, no venue found |
| A5-1 | Main finding | PA | PP | Abstract | "we discover a linear correlation between self-recognition capability and the strength of self-preference bias"; "self-recognition capability contributes to self-preference." | 8 | Abstract names GPT-4 and Llama 2 |
| A5-2 | Models and datasets | PA | PP | Sec. 2.1 | Models: "Llama-2-7b-chat", "GPT-3.5", "GPT-4". Datasets: "XSUM" and "CNN/DailyMail", 1,000 articles sampled from each (summarization) | 8 | |
| A5-3 | GPT-4 recognizes itself out of the box | PA | PP | Introduction | "GPT-4 is 73.5% accurate distinguishing itself from two other LLMs and humans." | 7 | |
| A5-4 | GPT-4 self-preference is high | PA | PP | Table 7 | Pairwise self-preference: GPT-4 0.705 (XSUM), 0.912 (CNN); GPT-3.5 0.582 / 0.431; Llama-2-7b 0.511 / 0.505. GPT-4 self-recognition 0.672 / 0.747 | 6 | Averaged confidence scores, not accuracy. Fine-tuning link reported as example-level Kendall's tau (e.g., GPT-3.5 XSUM 0.41 to 0.74), no single coefficient; verify |

## A6. Miller 2024

Source MI: Evan Miller (Anthropic), "Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations", arXiv 2411.00640v1 (1 Nov 2024), https://arxiv.org/html/2411.00640

| ID | Claim, stated narrowly | Source | Class | Location | Verbatim quote or exact numbers | Conf | Notes |
|---|---|---|---|---|---|---|---|
| A6-0 | Affiliation and status | MI | PP | Header | Affiliation: Anthropic ([email removed]); "arXiv:2411.00640v1 [stat.AP] 01 Nov 2024"; no venue statement in text | 8 | arXiv abs Comments field not opened |
| A6-1 | Five recommendations | MI | PP | Sec. 1, numbered list | (1) "Computing standard errors of the mean using the Central Limit Theorem" (2) "When questions are drawn in related groups, computing clustered standard errors" (3) "Reducing variance by resampling answers and by analyzing next-token probabilities" (4) "When two models are being compared, conducting statistical inference on the question-level paired differences, rather than the population-level summary statistics" (5) "Using power analysis to determine whether an eval (or a random subsample) is capable of testing a hypothesis of interest" | 8 | |
| A6-2 | SE of a mean score | MI | PP | Eq. (1), Sec. 2.1; Eq. (2) | SE_CLT = sqrt(Var(s)/n), Var(s) = (1/(n-1)) sum_i (s_i - s_bar)^2. Binary scores: SE = sqrt(s_bar(1 - s_bar)/n) | 8 | |
| A6-3 | Clustering can more than triple the SE | MI | PP | Table 4 caption; Sec. 2.2 | "Analyzing the same data, clustered standard errors can be over 3X larger than naive standard errors."; "far from trivial (up to 3X)". Ratios: DROP 3.05 (1.34 vs 0.44), RACE-H 1.10, MGSM 1.88 | 8 | Only DROP exceeds 3x |
| A6-4 | Paired differences cut variance when scores correlate | MI | PP | Sec. 4.2 | "We can thus reduce the variance with paired differences as long as the conditional means of the model scores are correlated"; Var(paired) = Var(unpaired) - 2 Cov(x_A, x_B)/n | 7 | Worked example uses correlation 0.5 |
| A6-5 | Reporting conventions | MI | PP | Sec. 2.1; Table 2 and 3 captions | "We suggest reporting the standard error of the mean alongside (beneath) the mean when reporting eval scores."; report number of questions and SE in parentheses; report cluster count with question count | 8 | |
| A6-6 | Do not change temperature to shrink variance; bootstrap usually unnecessary | MI | PP | Sec. 3.3; Sec. 2.1 | "In neither case should the sampling temperature be adjusted for the sake of reducing variance in the scores."; "we regard bootstrapping as unnecessary unless a complicated sampling scheme or estimator is being used." | 7 | |

## A7. Statistics references

Sources:
- NIST: NIST/SEMATECH e-Handbook of Statistical Methods, "7.2.4.1. Confidence intervals", https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm
- BCD: Brown, Cai, DasGupta, "Interval Estimation for a Binomial Proportion", Statistical Science 16(2):101-133, 2001; author-hosted PDF https://www-stat.wharton.upenn.edu/~tcai/paper/Binomial-StatSci.pdf (Project Euclid was bot-blocked)
- FLL: Fagerland, Lydersen, Laake, "The McNemar test for binary matched-pairs data: mid-p and asymptotic are better than exact conditional", BMC Medical Research Methodology 13:91, 2013, https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-91
- MCH: McHugh, "Interrater reliability: the kappa statistic", Biochem Med (Zagreb) 22(3):276-282, 2012, DOI 10.11613/BM.2012.031, https://www.biochemia-medica.com/en/journal/22/3/10.11613/BM.2012.031 (PMC copy was CAPTCHA-blocked)
- FAW: Fawcett, "An introduction to ROC analysis", Pattern Recognition Letters 27:861-874, 2006; PDF copy at https://people.inf.elte.hu/kiss/11dwhdm/roc.pdf (university-hosted copy, not the publisher)
- SKL: scikit-learn developers, "3.4. Metrics and scoring: quantifying the quality of predictions", scikit-learn 1.9.1 documentation, https://scikit-learn.org/stable/modules/model_evaluation.html

| ID | Claim, stated narrowly | Source | Class | Location | Verbatim quote or exact numbers | Conf | Notes |
|---|---|---|---|---|---|---|---|
| A7a-1 | Wilson score interval formula | NIST | OD | 7.2.4.1, "Formulas for the confidence intervals" | U.L. = [p_hat + z^2/(2n) + z sqrt(p_hat(1-p_hat)/n + z^2/(4n^2))] / [1 + z^2/n], z = z_(1-alpha/2); L.L. is the same with z_(alpha/2) (negative) | 7 | Transcribed by the extractor; check symbols on the page |
| A7a-2 | NIST names it the Wilson method and cites Brown et al. | NIST | OD | same | "introduced by Wilson (1927), recommended by Brown, Cai and DasGupta (2001) and Agresti and Coull (1998)" | 8 | Handbook formerly called it "Agresti-Coull method" |
| A7a-3 | Brown et al. recommendation | BCD | PR | Abstract, p. 101 | Recommend "the Wilson interval or the equal-tailed Jeffreys prior interval for small n" and "the interval suggested in Agresti and Coull for larger n." | 9 | |
| A7a-4 | Brown et al. on the Wald interval | BCD | PR | Abstract | "erratic behavior of the coverage probability of the standard Wald confidence interval has previously been remarked on in the literature"; "the chaotic coverage properties of the Wald interval are far more persistent than is appreciated"; textbook prescriptions "are misleading and defective in several respects and cannot be trusted" | 9 | |
| A7a-5 | "Small n" means n <= 40 | BCD | PR | Sec. 1; Sec. 5 | "for small n (40 or less)"; "small n (n <= 40)"; for n > 40 the three recommended intervals are "all very similar" | 7 | Extractor also reported Example 3: p = 0.005, coverage 0.792 at n = 592; verify before use |
| A7b-1 | McNemar uses only the discordant pairs | FLL | PR | Methods | "The asymptotic McNemar test conditions on the number of discordant pairs"; z = (n12 - n21)/sqrt(n12 + n21) | 7 | Formula reconstructed from garbled text |
| A7b-2 | Exact version is binomial on the discordant pairs | FLL | PR | Methods | "The conditional probability under H 0 of observing any outcome x 12 given n=n 12+n 21 discordant pairs" | 6 | "binomial with p = 1/2; two-sided p = twice one-sided" is the extractor's paraphrase |
| A7b-3 | Exact conditional test is conservative and underpowered | FLL | PR | Results/Discussion | "Quite often, the type I error rates of the exact conditional test were half that of the nominal level or lower."; "This conservatism leads to poor power and a need for unnecessary large sample sizes." | 9 | |
| A7b-4 | Recommendation: mid-p, or asymptotic without CC; never exact conditional | FLL | PR | Abstract; Conclusions | "The easy-to-calculate mid-p test is an excellent alternative to the complex exact unconditional test."; "The most powerful test is the McNemar asymptotic test (without CC), which we recommend if small but frequent violations of the nominal level is acceptable."; "We do not recommend use of the McNemar exact conditional test nor the asymptotic test with CC in any situation." | 9 | No numeric sample-size threshold given |
| A7c-1 | Kappa terms | MCH | PR | Cohen's kappa section | "Where Pr(a) represents the actual observed agreement, and Pr(e) represents chance agreement." | 7 | Formula printed as an image; its text form NOT FOUND |
| A7c-2 | Kappa originates with Cohen (1960) | MCH | PR | Abstract; reference 5 | "In 1960, Jacob Cohen critiqued use of percent agreement due to its inability to account for chance agreement."; ref 5: Cohen J. "A coefficient of agreement for nominal scales." Educ Psychol Meas 1960;20:37-46 | 8 | |
| A7c-3 | The usual bands, and McHugh's criticism | MCH | PR | Measurement section | "Cohen suggested the Kappa result be interpreted as follows": <=0 no agreement; 0.01-0.20 none to slight; 0.21-0.40 fair; 0.41-0.60 moderate; 0.61-0.80 substantial; 0.81-1.00 almost perfect. "this interpretation allows for very little agreement among raters to be described as "substantial"." Abstract: "may be too lenient for health related studies because it implies that a score as low as 0.41 might be acceptable." | 7 | McHugh attributes these bands to Cohen; Landis and Koch are NOT named in the text |
| A7c-4 | McHugh's own threshold | MCH | PR | Table 3 discussion | "any kappa below 0.60 indicates inadequate agreement among the raters and little confidence should be placed in the study results." | 8 | Table 3 levels are an image, NOT FOUND as text |
| A7c-5 | scikit-learn kappa reading | SKL | OD | 3.4.4.5 | "The kappa score is a number between -1 and 1. Scores above .8 are generally considered good agreement; zero or lower means no agreement (practically random labels)." | 8 | No formula on this page |
| A7d-1 | AUC equals a ranking probability | FAW | PR | Sec. 7 | "the AUC of a classifier is equivalent to the probability that the classifier will rank a randomly chosen positive instance" + "higher than a randomly chosen negative instance." | 9 | Returned as two pieces of one sentence |
| A7d-2 | AUC is equivalent to the Wilcoxon rank test | FAW | PR | Sec. 7 | "This is equivalent to the Wilcoxon test of ranks" (cites Hanley and McNeil, 1982) | 8 | Mann-Whitney not named |
| A7e-1 | Precision and recall | SKL | OD | 3.4.4.9.1 | precision = tp/(tp + fp); recall = tp/(tp + fn) | 9 | |
| A7e-2 | F-measure and F1 | SKL | OD | 3.4.4.9 and 3.4.4.9.1 | F_beta = (1 + beta^2) (precision x recall)/(beta^2 precision + recall); "With beta = 1, F_beta and F_1 are equivalent, and the recall and the precision are equally important." | 8 | The 2PR/(P+R) form is not printed |

## A8. Semantic entropy

Sources:
- FA: Farquhar, Kossen, Kuhn, Gal, "Detecting hallucinations in large language models using semantic entropy", Nature, 2024, https://www.nature.com/articles/s41586-024-07421-0 (volume/pages 630:625-630 not re-checked in this run)
- KU: Kuhn, Gal, Farquhar, "Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation", arXiv 2302.09664v3 (2023-04-15), https://arxiv.org/abs/2302.09664
- KO: Kossen, Han, Razzak, Schut, Malik, Gal, "Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs", arXiv 2406.15927v1 (2024-06-22), https://arxiv.org/abs/2406.15927

| ID | Claim, stated narrowly | Source | Class | Location | Verbatim quote or exact numbers | Conf | Notes |
|---|---|---|---|---|---|---|---|
| A8a-1 | Ten samples at temperature 1 | FA | PR | Results; Methods "Generating a set of answers from the model" | "We use ten generations to compute entropy"; "we sample at temperature 1 using nucleus sampling (P = 0.9) and top-K sampling (K = 50)" | 8 | One extra low-temperature (0.1) "best generation" is used to judge accuracy |
| A8a-2 | Same meaning = bidirectional entailment | FA | PR | Methods "Clustering by semantic equivalence" | "A sequence, s, means the same thing as a second sequence, s', only if the sequences entail (that is, logically imply) each other" | 8 | |
| A8a-3 | Which model checks entailment | FA | PR | Methods "Entailment estimator"; Suppl. Note 2 | "We rely on language models to predict entailment, such as DeBERTa-Large-MNLI, or general-purpose LLMs such as GPT-3.5"; "We settle on using GPT-3.5 with the above prompt" | 7 | LLaMA 2 and GPT-4 also listed as options. Extractor said the biography experiments use DeBERTa with a "non-defeating" check; verify |
| A8a-4 | Formula and cluster probabilities | FA | PR | Methods, Eq. 2 and Eq. 5 | P(c given x) = sum of P(s given x) over sequences s in cluster c; SE(x) ~= -sum_i P(C_i given x) log P(C_i given x), with cluster probabilities normalised over the sampled clusters. "Without this normalization step cluster 'probabilities' could exceed one because of length normalization." | 7 | Reconstructed by extractor |
| A8a-5 | Discrete semantic entropy | FA | PR | Methods | "we approximate P(C_i given x) directly from the number of generations in each cluster"; "results in similar performance empirically." | 8 | Used when token probabilities are unavailable |
| A8a-6 | Headline AUROC | FA | PR | Results "Detecting confabulations in QA and math"; Fig. 2 caption | "Averaged across the 30 combinations of tasks and models we study, semantic entropy achieves the best AUROC value of 0.790."; "naive entropy (0.691), P(True) (0.698) and the embedding regression baseline (0.687) lag behind it."; Fig. 2: "Results are an average over five datasets." | 9 | 30 task-model combinations |
| A8a-7 | Definition of confabulation | FA | PR | Main text | "we focus on a subset of hallucinations which we call 'confabulations' for which LLMs fluently make claims that are both wrong and arbitrary" + "by which we mean that the answer is sensitive to irrelevant details such as random seed" | 9 | |
| A8a-8 | Limits: consistent errors | FA | PR | Main text; Discussion | "when LLMs are consistently wrong as a result of being trained on erroneous data"; it "does not help when LLM outputs are systematically bad"; "Our method explicitly does not directly address situations in which LLMs are confidently wrong" | 8 | Cost: main text only points to Supplementary Note 3; a cost figure was NOT FOUND |
| A8b-1 | Kuhn et al. venue | KU | PP (on evidence opened) | arXiv abs; PDF v3 p. 1 | Comments: none; Journal ref: none; no venue line extracted from the PDF | n/a | NOT FOUND (OpenReview page was bot-blocked) |
| A8c-1 | SEPs read the hidden states of one generation | KO | PP | Abstract | "To address this, we propose SEPs, which directly approximate SE from the hidden states of a single generation." | 9 | |
| A8c-2 | Cost claim | KO | PP | Abstract | "However, the 5-to-10-fold increase in computation cost associated with SE computation hinders practical adoption."; "SEPs are simple to train and do not require sampling multiple model generations at test time," + "reducing the overhead of semantic uncertainty quantification to almost zero." | 9 | Authors' claim |
| A8c-3 | Peer-review status | KO | PP | arXiv abs | Only v1 (2024-06-22); Comments: none; Journal ref: none | 7 | Preprint, no venue found |

## A9. Test data and contamination

Sources:
- GS: Zhang, Da, Lee, Robinson, Wu, Song, Zhao, Raja, Zhuang, Slack, Lyu, Hendryx, Kaplan, Lunati, Yue, "A Careful Examination of Large Language Model Performance on Grade School Arithmetic", arXiv 2405.00332 (v1 2024-05-01; v4 2024-11-22), https://arxiv.org/abs/2405.00332 and https://arxiv.org/abs/2405.00332v1
- SH: Shankar, Zamfirescu-Pereira, Hartmann, Parameswaran, Arawjo, "Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences", arXiv 2404.12272v1 (2024-04-18), https://arxiv.org/abs/2404.12272

| ID | Claim, stated narrowly | Source | Class | Location | Verbatim quote or exact numbers | Conf | Notes |
|---|---|---|---|---|---|---|---|
| A9a-1 | Headline drop, latest version | GS | PP | Abstract, v4 | "accuracy drops of up to 8%" (GSM1k vs GSM8k, leading open and closed models) | 8 | |
| A9a-2 | Headline drop, v1 | GS | PP | Abstract, v1 | "we observe accuracy drops of up to 8%" | 6 | Same as v4 in the extraction, so no version difference found; v2 and v3 not opened |
| A9a-3 | Memorization evidence | GS | PP | Abstract (v1 and v4) | "a positive relationship (Spearman's r^2 = 0.36)" between a model's "probability of generating an example from GSM8k" and its GSM8k-to-GSM1k gap; "suggesting that some models may have partially memorized GSM8k" | 8 | The statistic is r^2, not r |
| A9a-4 | Venue | GS | PP | arXiv abs | No Comments/Journal ref in the extraction | 5 | NOT FOUND |
| A9b-1 | Criteria drift | SH | PP | Abstract | "users need criteria to grade outputs, but grading outputs helps users define criteria."; "some criteria appears dependent on the specific LLM outputs observed" (as opposed to criteria that "can be defined a priori") | 8 | The phrase "criteria drift" itself did not come back from the abstract |
| A9b-2 | Venue | SH | PP | arXiv abs | Only v1; Comments: none; Journal ref: none; DOI: none | 6 | NOT FOUND |

## A10. Nondeterminism

Source TM: Horace He with others at Thinking Machines, "Defeating Nondeterminism in LLM Inference", Thinking Machines Lab (Connectionism blog), Sep 10, 2025, https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/

| ID | Claim, stated narrowly | Source | Class | Location | Verbatim quote or exact numbers | Conf | Notes |
|---|---|---|---|---|---|---|---|
| A10-1 | Cause: no batch invariance, not concurrency as such | TM | VB | Body | "our forward pass lacks "batch invariance""; "the load (and thus batch-size) nondeterministically varies!"; "concurrency (and atomic adds) end up being completely uninvolved in LLM inference nondeterminism"; the "concurrency + floating point" hypothesis "doesn't reveal the full picture" | 9 | |
| A10-2 | Experiment | TM | VB | Experiment section | Qwen/Qwen3-235B-A22B-Instruct-2507; 1,000 completions at temperature 0, 1,000 tokens each; prompt "Tell me about Richard Feynman"; "we generate 80 unique completions, with the most common of these occuring 78 times."; first divergence at token 103 (992 "Queens, New York" vs 8 "New York City") | 9 | |
| A10-3 | Fix and its cost | TM | VB | Fix sections | Batch-invariant kernels for RMSNorm, matmul and attention (vLLM demo; library "batch-invariant-ops"); with the fix all 1,000 completions were identical. Matmul: "we only lose about 20% performance compared to cuBLAS"; Qwen-3-8B, 1,000 sequences: 26 s default vs 55 s unoptimized deterministic vs 42 s improved attention | 8 | Also: deterministic inference gives true on-policy RL ("KL-divergence stays flat at 0") |

## A11. Chen et al. 2021

Source CH: Chen et al. (OpenAI), "Evaluating Large Language Models Trained on Code", arXiv 2107.03374v2 (14 Jul 2021), https://arxiv.org/pdf/2107.03374

| ID | Claim, stated narrowly | Source | Class | Location | Verbatim quote or exact numbers | Conf | Notes |
|---|---|---|---|---|---|---|---|
| A11-1 | Unbiased pass@k estimator | CH | PP | Sec. 2.1, Eq. (1) | pass@k := E_Problems[1 - C(n-c, k)/C(n, k)]; n = samples generated per task; c = correct samples ("count the number of correct samples c <= n which pass unit tests") | 8 | |
| A11-2 | Sample sizes | CH | PP | Sec. 2.1 | "we use n = 200 and k <= 100" | 9 | APPS: 1,000 samples per task (Sec. 3.5) |
| A11-3 | Naive estimate is biased (underestimates) | CH | PP | Sec. 2.1; Appendix A; Fig. 13 | "One may be tempted to estimate pass@k with 1-(1-p_hat)^k ... but we show that it is biased in Appendix A."; it "results in a consistent underestimate as shown in Figure 13"; computing pass@k directly from k samples "can have high variance" | 8 | |
| A11-4 | Stable implementation | CH | PP | Sec. 2.1; Fig. 3 | "Calculating this estimator directly results in very large numbers and numerical instability."; numpy: return 1.0 if n - c < k, else 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1)) | 7 | |
| A11-5 | Peer-review status | CH | PP | PDF p. 1 | No venue statement; stamp "arXiv:2107.03374v2 [cs.LG] 14 Jul 2021" | 7 | arXiv abs Comments field not opened |

## NOT FOUND

1. A2: OpenAI's API-reference wording for `seed` ("best effort", "Determinism is not guaranteed"). The Chat Completions reference extraction was truncated before `seed`; the "Reproducible outputs" guide says "(mostly) deterministic" and does not use those phrases.
2. A2: the exact `label_model` type string, and the two grader objects hidden behind "or 2 more" on the Create-eval reference.
3. A5: venue. arXiv shows no Comments/Journal ref; the v1 HTML has no acceptance note.
4. A6 and A11: arXiv abstract-page Comments fields not opened (budget). Neither full text carries a venue statement.
5. A7(c): the kappa formula as text (McHugh prints it as an image; scikit-learn's user guide omits it). McHugh's own Table 3 levels (image). Tried: PMC (CAPTCHA), then the publisher page.
6. A7(a): Project Euclid page for Brown et al. (bot wall). The author-hosted PDF was used instead.
7. A8a: a quantified compute cost (main text defers to Supplementary Note 3, not opened).
8. A8b: Kuhn et al. venue. Tried: the arXiv abstract page (no Comments/Journal ref), the arXiv PDF v3 page 1 (no venue line extracted), and OpenReview (browser-verification wall).
9. A9a: venue, and dates of v2 and v3 (v2 and v3 not opened).
10. A9b: venue (arXiv v1 only, no Comments/Journal ref/DOI). The phrase "criteria drift" did not come back in the abstract extraction.
11. Blocked hosts: export.arxiv.org and arxiv.org for curl (egress policy, not retried); pmc.ncbi.nlm.nih.gov, projecteuclid.org and openreview.net for WebFetch (bot walls).

## Contradictions and surprises versus the brief

1. A3: the expected 65.0% (default) and 77.5% (few-shot) GPT-4 consistency are CONFIRMED (Table 2/9 and Table 12).
2. A1: Anthropic's separate "Define success criteria" page no longer exists. Both old URLs redirect to one page, "Define success criteria and build evaluations". The reasoning tip now reads "Use a grader model with thinking on". No "discard the reasoning" wording came back.
3. A1: `temperature` is now marked Deprecated. Models released after Claude Opus 4.6 reject any value other than 1.0 (400 error). So "use temperature 0" cannot be the paper's general advice for current Claude models. The "not fully deterministic" sentence is still on the page.
4. A2: OpenAI's docs say it "is deprecating the Evals platform" and "deprecating graders as part of the evals and fine-tuning workflows they support". The best-practices page names position and verbosity bias but not self-enhancement bias. The OpenAI judge-model recommendation ("gpt-6-astra") post-dates my knowledge; verify before quoting.
5. A4: the ACL 2024 abstract does not name the three calibration methods. The names come from the arXiv v2 abstract.
6. A7(c): McHugh 2012 does not name Landis and Koch. It credits the 0.01-0.20 to 0.81-1.00 bands to Cohen, then criticizes them, with "below 0.60 = inadequate" as its own line. Cite Landis and Koch 1977 directly if the paper needs their bands. That source was not opened here.
7. A7(e): scikit-learn's user guide gives F_beta and says F1 is the beta = 1 case. It does not print 2PR/(P+R), and it has no kappa formula.
8. A6: "over 3X" clustering inflation rests on one example (DROP, 3.05x). The others are RACE-H 1.10x and MGSM 1.88x.
9. A9a: no difference found between the v1 and v4 abstracts. Both extractions say "up to 8%" and "Spearman's r^2 = 0.36" (r^2, not r). The v1 reading came through a summarizer, so a direct look at the v1 PDF would settle it.
10. A5: the 73.5% figure is accuracy at telling itself apart from two other LLMs and humans. Table 7 values are averaged confidence scores, not accuracies.
11. A8a: the entailment model used for the main results is GPT-3.5 ("We settle on using GPT-3.5"). DeBERTa-Large-MNLI is an option, not the default. A low-temperature (0.1) answer is used separately to score accuracy.
12. A3: the self-enhancement figures are win-rate differences ("10% higher" for GPT-4, "25%" for Claude-v1). The authors themselves say their study "cannot determine whether the models exhibit a self-enhancement bias".
