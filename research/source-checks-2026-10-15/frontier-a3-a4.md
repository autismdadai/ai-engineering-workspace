# frontier-a3-a4: what is new on Axis 3 (Reasoning Topology) and Axis 4 (Decoding and Inference Compute)

Window: 2025-07-01 to 2026-10-15. Lookups used: 24 of 24 (cap reached). Status: complete.
Novelty check: none of the sources below appear in the manual's Works Cited. The manual cites only these arXiv IDs from 2507 onward: 2507.11473, 2507.11538, 2507.19457, 2508.00614, 2508.02452, 2509.04664, 2510.09023, 2511.15169, 2601.04426, 2601.23273.
Manual sections read: headings 9.1 to 10.5; text of 9.1 update, 10.1, 10.4, 10.5; keyword scans of 9.2, 9.5, 10.2, 10.3.

## Axis 3: Reasoning Topology

### F01. Longer reasoning can lower accuracy (Gema et al., arXiv 2507.14417)
- Class: peer-reviewed (TMLR, December 2025). arXiv v1 19 Jul 2025, v2 15 Dec 2025.
- Measured: tasks built so that letting a reasoning model think longer lowers accuracy: counting with distractors, regression with spurious features, deduction with constraint tracking, and AI-risk scenarios. Five failure modes. Claude models get distracted by irrelevant information. OpenAI o-series models overfit to how a problem is framed. Longer reasoning amplified some concerning behaviours (self-preservation statements in Claude Sonnet 4).
- Number with scope: Claude Opus 4, Misleading Math task, controlled-overthinking setup: accuracy "dropping from nearly 100% to around 85-90% as reasoning extends" (Figure 3 caption; no token budgets given there). DeepSeek R1, natural-overthinking setup: 70% to 30% with five distractors (distractor count, not reasoning length). These are purpose-built stress tasks, not typical workloads.
- Do differently: do not assume higher effort or a bigger thinking budget always helps. If the prompt contains irrelevant or misleading detail, test a lower effort level too, and remove the distractors.
- Manual: small change. 10.4 describes only gains (Snell et al.). Add one sentence and a Works Cited entry; add "also test lower effort" to protocol step 2.

### F02. Decomposition adds little on frontier models, but disagreement is a useful warning (Madhwal et al., arXiv 2602.04853)
- Class: peer-reviewed (Findings of ACL 2026; ACL Anthology listing seen in search results, not opened). arXiv v2 dated 6 Jul 2026.
- Measured: direct prompting versus two decomposed-prompting styles ("Assistive", "Incremental") on six multi-hop factual QA benchmarks (1,433 verified instances), nine models: Mistral-7B, Llama-3.1-8B, Qwen3-8B, Qwen3-32B, Llama-3.3-70B, Qwen2.5-72B, GPT-5.1, Gemini-2.5-Pro, Gemini-2.5-Flash.
- Numbers with scope: Bamboogle, Llama-3.3-70B direct 45.5%, decomposition +26.8 and +22.8 points. Bamboogle, GPT-5.1 direct 84.6%, +3.2 and +2.4. MuSiQue, GPT-5.1 direct 53.9%, +0.4 and -7.8. Gains plateau or turn negative on frontier models.
- Use that holds up: Disagreement-Based Abstention (treat a disagreement between direct and decomposed answers as "do not trust"). GPT-5.1 abstention F1 (Are-you-sure baseline to DBA-Assistive): Bamboogle 0.47 to 0.73, MuSiQue 0.38 to 0.66. On CRAG the baseline is higher (0.66 versus 0.53); the combined ensemble reaches 0.75.
- Do differently: on a frontier model do not expect decomposition to lift accuracy on factual multi-hop questions. If the answer matters, ask both ways and send disagreements for checking.
- Manual: change. 9.2 cites only Zhou et al. (ICLR 2023) and has no frontier-model caveat. Add a short 2026 note, scoped to factual multi-hop QA (not math or code).

### F03. Code interpreters raise answers but can weaken the reasoning (Bayat, Pezeshkpour, Hruschka, arXiv 2511.10899)
- Class: preprint, no venue listed. v1 14 Nov 2025, v2 20 Apr 2026.
- Measured: tool-augmented models with a Code Interpreter against their non-tool counterparts on PYMATH (1,679 competition-level maths problems where Python helps but is not sufficient). The abstract does not name the models.
- Numbers with scope: final-answer accuracy up to +19.3 percentage points with the tool ("up to" = best case). In pairwise comparisons of the reasoning, non-tool models win "up to 41.5% more often". The failure the authors call Tool-Induced Myopia appears in about 55% of "high-risk cases" (not defined in the abstract).
- Do differently: a code interpreter helps calculation-heavy maths, but read the working, not only the final number. Having the model re-check the code's result by a separate route is a reasonable response; that is my inference, not tested in the paper.
- Manual: small change. 9.5 rests on 2023 evidence (PoT, PAL). Add a caution with this scope. Only the abstract was read; check the full text before quoting more.

### F04. Visible reasoning often hides what influenced the answer (Young, arXiv 2603.22582, "Lie to Me")
- Class: preprint, no venue listed. 23 Mar 2026. Single author.
- Measured: how often a model's chain of thought admits a planted hint that changed its answer. 12 open-weight reasoning models from 9 families (7B to 685B parameters); 498 multiple-choice questions from MMLU and GPQA Diamond; six hint types; 41,832 runs.
- Numbers with scope: overall acknowledgement from 39.7% (Seed-1.6-Flash) to 89.9% (DeepSeek-V3.2-Speciale). Lowest by hint type: consistency hints 35.5%, sycophancy hints 53.9%. Keyword analysis: about 87.5% in thinking tokens versus about 28.6% in the final answer text. Training method and model family predicted faithfulness better than size.
- Do differently: do not treat a model's explanation as proof of what drove its answer. Check the answer against the source. Final-answer explanations are weaker evidence than the raw thinking, but many APIs show only a summary of the thinking.
- Manual: optional. The manual cites Chen et al. (2505.05410) on faithfulness; this widens the measurement to 12 open-weight models. Mark it a single-author preprint.

## Axis 4: Decoding and Inference Compute

### F05. Google now says to leave Gemini sampling controls alone and use thinking_level (Gemini API docs)
- Class: vendor documentation. Two pages: "Gemini 3 Developer Guide" (ai.google.dev/gemini-api/docs/gemini-3), last updated 2026-10-09, with a notice that it will be removed in favour of a Gemini 3.8 Flash guide; and "What's new in Gemini 3.8" (ai.google.dev/gemini-api/docs/whats-new-gemini-3.8), last updated 2026-10-13.
- Gemini 3 guide: "For all Gemini 3 models, we strongly recommend keeping the temperature parameter at its default value of 1.0." Reason given: reasoning is "optimized for the default setting"; lower values "may lead to unexpected behavior, such as looping or degraded performance". thinking_level values minimal/low/medium/high, default high if unset (Gemini 3.1 Pro and 3 Flash); 3.1 Pro does not support minimal.
- Gemini 3.8 page: migration checklist says "Remove deprecated sampling parameters (temperature, top_p, top_k)" (gives no values and, on this page, does not say they are ignored). thinking_level low/medium/high, default medium; "minimal" returns an error on 3.8 Flash. "Replace thinking_budget with the string enum thinking_level."
- Not verified: a Google Cloud search snippet said these parameters are ignored by the backend on newer models. I did not open that page.
- Do differently: before setting temperature, read the current docs for your exact model. For Gemini 3.x reasoning tasks do not lower it; on 3.8 Flash drop it and set thinking_level.
- Manual: change. 10.1 ("keep temperature low where one answer is correct") and the settings sketch (temperature: 0) need a provider caveat.

### F06. Asking for JSON can cost accuracy; reformat in a second step (Lee, D'Antoni, Berg-Kirkpatrick, arXiv 2604.03616, "The Format Tax")
- Class: preprint. 4 Apr 2026.
- Measured: six open-weight and four API models; four formats (JSON, XML, LaTeX, Markdown); MATH-500, GPQA-Diamond, ZebraLogic, WritingBench; with and without grammar-constrained decoding (GCD).
- Numbers with scope: open-weight, MATH-500, JSON: qwen3-32b freeform 84.4%, minus 5.3 points with the format request alone and minus 9.8 with GCD added; qwen3-8b freeform 84.0%, minus 11.5 and minus 16.7. Averaged over 72 open-weight model-task-format cells: prompt-only minus 3.9 points; GCD minus 1.6 points (my source summary does not make clear whether the second figure is added on top). Averaged over the three reasoning benchmarks, GCD raised format validity from 55.7% to 92.2% but accuracy was 57.3% without GCD, 55.7% with GCD, 61.5% freeform. Closed models: gpt-5-nano shows the tax (minus 5.2, minus 8.0 with GCD); gpt-5.4-nano (average +2.5), claude-haiku-4.5 (+1.2) and grok-4.1-fast (+2.5) show near-zero or positive change without GCD. Most loss comes from the format instruction, before any decoder constraint. Writing freeform first and reformatting in a second pass, or turning on extended thinking, recovers most of it.
- Do differently: on open-weight models doing reasoning-heavy work, let the model think in free text, then convert to JSON in a second call. Keep schema-constrained decoding for the conversion step. Measure the tax on your own model; recent closed models mostly showed none.
- Manual: change. 10.5 says the format-versus-reasoning debate "is unsettled" (Tam et al. versus the dottxt rebuttal). Add this 2026 measurement and the two-step pattern.

### F07. Confidence-filtered voting cuts the cost of self-consistency (Fu, Wang, Tian, Zhao, arXiv 2508.15260, "Deep Think with Confidence")
- Class: preprint (no venue seen). 21 Aug 2025.
- Measured: DeepConf uses the model's own token-level confidence to drop weak reasoning traces. AIME 2025, Qwen3 and GPT-OSS models. Needs no extra training.
- Numbers with scope (GPT-OSS-120B, AIME 2025): pass@1 91.8%; majority vote over 512 traces 97.0% using about 3.23e8 tokens; offline DeepConf@512 99.9%; online DeepConf-low 97.9% with 84.7% fewer tokens; online DeepConf-high 97.0% with 56.0% fewer tokens. The abstract's "99.9%" and "84.7%" come from different variants, not one run.
- Needs top-k token log-probabilities (vLLM integration), so it suits self-hosted serving or APIs that return them.
- Do differently: if you self-host, confidence-based early stopping is a cheaper way to vote. With a hosted API, the usable lesson is to stop adding samples once the vote settles.
- Manual: optional. Add a line in 10.2 as an efficiency variant. The advice to start at N=5 still stands.

### F08. Effort setting is now the main control; prompt wording is unreliable for it (Anthropic and OpenAI documentation)
- Class: vendor documentation. Anthropic "Steering thinking" (platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost) and OpenAI reasoning guide (developers.openai.com/api/docs/guides/reasoning). Neither page shows a date. The Anthropic page describes Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5, which the manual does not name.
- Anthropic: effort levels max, xhigh, high (default on most models), medium (default on Opus 5.5 and Haiku 5.5), low; set at output_config.effort. "You don't set a thinking token budget": max_tokens is a hard cap on thinking plus answer, effort is soft guidance. Asking Sonnet 5.5 in the system prompt to think less "doesn't reliably reduce its thinking", so lower effort instead. Changing effort between requests invalidates the prompt cache (the page's example shows cache creation 3546 tokens again after a switch from medium to low). usage.output_tokens_details.thinking_tokens reports reasoning tokens.
- OpenAI: reasoning.effort values are model-dependent and "can include none, minimal, low, medium, high, xhigh, and max"; newer GPT-6 models default to medium. "Treat reasoning.effort as a tuning knob, not the primary way to recover quality." Reasoning models work best with "a clear goal, strong constraints, and an explicit output contract."
- Do differently: pick an effort level per conversation and keep it; do not rely on "think less" prompts; check the default for your model.
- Manual: small change. 10.4 already covers adaptive thinking and effort; add per-model defaults, the cache effect and the prompt-steering caveat.

## Manual claims checked along the way
- C01. 10.4 quotes OpenAI "Avoid chain-of-thought prompts: ...". VERIFIED in substance. The bullet is on the separate "Reasoning best practices" page (developers.openai.com/api/docs/guides/reasoning-best-practices); the tool output elided the middle of the sentence, so "or explain your reasoning" is not confirmed word for word. The main reasoning guide page did not contain "think step by step". Fix: name the page "Reasoning best practices".
- C02. 10.4 says Anthropic's budget_tokens is deprecated on Claude 4.6 and unsupported on 4.7 and later. UNVERIFIABLE on the page I opened: it speaks of a "legacy manual thinking budget" and says you do not set a thinking budget, but shows no version numbers.
- C03. 10.1 "Keep temperature low where one answer is correct" (and the temperature 0 sketch). MISSING_SCOPE: see F05.
- C04. 10.5 "The format-versus-reasoning debate is unsettled". MISSING_SCOPE: see F06.

## Opened but not counted
- Bay and Yearick, arXiv 2606.28661 (27 Jun 2026), "When More Sampling Hurts". Preprint, no venue. Voting settles "within a few dozen draws" and extra draws can lock in a wrong answer; coverage with a verifier keeps rising. Data are released logs from Llama-3-8B and 70B (GSM8K, MATH, up to 10^4 samples) and Llama-3.2-1B (MATH-500, 256 attempts: single-sample about 0.27, plurality plateau about 0.45 by about N=64). Old, small models, so held back; it agrees with the manual's N=5 start.
- Zhao et al., arXiv 2508.01191, "Is Chain-of-Thought Reasoning of LLMs a Mirage?" ACL 2026 (v6 8 May 2026). Models trained from scratch in a toy environment; abstract has no numbers. Held back.

## Gaps
- Tree and graph of thoughts: one search found no primary head-to-head against native reasoning models. Seen in search results only, not opened: Lateral ToT (2510.01500), Structural CoT (2610.15107).
- Seen in search results only: arXiv 2609.23742 (constrained decoding, small models), 2604.25359 (Structured Output Benchmark), 2510.17922 (Select-Then-Decompose, EMNLP 2025).
- Not reached: newer work on temperature-0 nondeterminism, verifier or process-reward models for best-of-N (one search only), and OpenAI or Anthropic structured-outputs documentation changes.
