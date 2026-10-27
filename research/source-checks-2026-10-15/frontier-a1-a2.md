# frontier-a1-a2: what is new on Axis 1 (Contextual Conditioning) and Axis 2 (Representation)
Date of check: 2026-10-15. Lookups used: 24 of 24 (cap reached). Pages opened by me; no PDFs downloaded.
Window: published or substantially updated 2025-07-01 to 2026-10-15. None is in the manual's Works Cited (checked by Grep on arXiv IDs and titles).
Final numbering: F01-F04 are Axis 1, F05-F08 are Axis 2 (this renumbers the working drafts saved earlier).

How I read numbers: "abs page" means I read the arXiv abstract page. "html" means WebFetch returned the sentence or table cell from the arXiv HTML page. WebFetch passes pages through a small model, so table-cell readings are second-hand and flagged where they matter.

## AXIS 1

### F01  Length alone hurts accuracy even when retrieval is perfect; recite the evidence first
- Source: Du, Tian, Ronanki, Rongali, Bodapati, Galstyan, Wells, Schwartz, Huerta, Peng. "Context Length Alone Hurts LLM Performance Despite Perfect Retrieval." arXiv 2510.05381, 2025-10-06. Findings of EMNLP 2025 (stated in arXiv comments; ACL Anthology page not opened). https://arxiv.org/abs/2510.05381
- Measured: 5 open and closed LLMs on math, question answering and coding, with the needed evidence supplied perfectly while input length grows. Abstract: performance "still degrades substantially (13.9%--85%) as input length increases". The drop persists when irrelevant tokens are replaced with whitespace or fully masked.
- Scope of the number: the paper never says whether 13.9%-85% is relative or absolute. In the HTML appendix tables (two open models only, Llama-3.1-8B and Mistral-v0.3-7B; VarSum, GSM8K, MMLU, HumanEval) the figures read as absolute points: Llama on VarSum falls from 96.0 to 11.0 at 30,000 tokens (85 points); Mistral's MMLU change at 7,500 tokens matches 13.9. This is the fetch tool's reading, not a sentence in the paper.
- Fix tested: have the model "recite the retrieved evidence before attempting to solve the problem". Abstract: "a consistent improvement of GPT-4o up to 4% on an already strong baseline" on RULER. In HTML Table 5, QA2 at 32K goes 68.4 to 72.4 (4.0 points).
- Evidence class: peer-reviewed (Findings of EMNLP 2025).
- Do differently: after pasting a long document, ask the model to quote the passages that answer the question, then answer from the quotes. Do not assume a clean, well-retrieved context removes the cost of length.
- Manual change: Section 7.4 explains length cost through irrelevant padding (Levy et al.). Add Du et al.: the cost remains when the padding is masked, and recite-then-answer is a measured mitigation (up to 4 points, GPT-4o, RULER).

### F02  Expert personas still do not raise factual accuracy (replication on 2025 models)
- Source: Basil, Shapiro, Shapiro, Mollick, Mollick, Meincke. "Prompting Science Report 4: Playing Pretend: Expert Personas Don't Improve Factual Accuracy." arXiv 2512.05858, 2025-12-05. Wharton Generative AI Labs report page: https://gail.wharton.upenn.edu/research-and-insights/playing-pretend-expert-personas/ ; abstract: https://arxiv.org/abs/2512.05858
- Measured (Wharton page): six models (GPT-4o, GPT-4o-mini, o3-mini, o4-mini, Gemini 2.0 Flash, Gemini 2.5 Flash) on GPQA Diamond and MMLU-Pro. Matched expert, mismatched expert and low-knowledge personas against a no-persona baseline.
- Results: GPQA, no expert or low-knowledge persona reliably beat baseline for any model. MMLU-Pro, for five of six models no expert persona significantly improved on baseline. The one exception: Gemini 2.0 Flash on MMLU-Pro, Engineering Expert persona, about +8.9 percentage points (RD 0.089, p = 0.002); Gemini 2.5 Flash showed no such gain, so the authors suggest a model quirk. Low-knowledge personas "often reduce accuracy" (GPQA: all three low-knowledge personas below baseline on o4-mini; Toddler significantly negative on GPT-4o; MMLU-Pro: Toddler and Layperson hurt Gemini 2.0 Flash). Gemini 2.5 Flash with mismatched experts declined to answer on average 10.56 of 25 trials per question.
- Evidence class: preprint / technical report (not peer-reviewed as far as the pages I opened show).
- Do differently: do not add "you are a world-class expert" to raise accuracy on hard factual or reasoning questions. Use a role for tone, format and audience. Never assign a mismatched or low-knowledge persona on a task that needs accuracy; some models refuse more.
- Manual change: Section 7.3 rests on Zheng et al. 2024 (open models, MMLU, 2023-era). Add Basil et al. 2025 as a second, newer test on 2025 closed models, and update the evidence-class line. The conclusion stands; the scope widens.

### F03  Prompt repetition: sending the same prompt twice helps non-reasoning models
- Source: Leviathan, Kalman, Matias (Google Research). "Prompt Repetition Improves Non-Reasoning LLMs." arXiv 2512.14982, 2025-12-17. No venue listed. https://arxiv.org/abs/2512.14982 ; https://arxiv.org/html/2512.14982v1
- Measured: input changed from QUERY to QUERY QUERY, no extra output tokens. Seven models: Gemini 2.0 Flash, Gemini 2.0 Flash Lite, GPT-4o-mini, GPT-4o, Claude 3 Haiku, Claude 3.7 Sonnet, DeepSeek V3. Several benchmarks.
- Key number (html, verbatim): "prompt repetition wins 47 out of 70 benchmark-model combinations, with 0 losses" (non-reasoning setting). With step-by-step reasoning on: "neutral to slightly positive (5 wins, 1 loss, 22 ties)". The abstract page gives no win/loss count; it says repetition "improves performance for popular models (Gemini, GPT, Claude, and Deepseek)".
- Not verified: one secondary summary quotes NameIndex on Gemini 2.0 Flash-Lite going 21.33% to 97.33%; I did not see that on a primary page, so I do not use it.
- Evidence class: preprint.
- Do differently: on a non-reasoning model, for look-up from the prompt or options-first multiple choice, paste the question twice as a free test. Do not expect a gain once reasoning is on. It doubles input tokens, not output.
- Manual change: add one line to 7.4 beside "documents first, question last": repetition is a separately tested lever. Scope is 2024-25 non-reasoning models; none of the tested Claude models is a 2026 model.

### F04  Anthropic's current Claude prompting guides: less emphasis, explicit scope, keep "find" and "filter" apart
- Sources (vendor documentation, opened 2026-10-15): Prompting best practices https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices (page lists models up to Claude Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5) and Prompting Claude Sonnet 5 https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5
- Verbatim lines:
  - "Claude Opus 4.5 and Claude Opus 4.6 are also more responsive to the system prompt than previous models. If your prompts were designed to reduce undertriggering on tools or skills, these models may now overtrigger. The fix is to dial back any aggressive language. Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'."
  - "Prefilled responses on the last assistant turn are no longer supported starting with Claude 4.6 models and Claude Mythos Preview."
  - Sonnet 5: "interprets prompts literally and explicitly, particularly at lower effort levels. It does not silently generalize an instruction from one item to another"; fix: "state the scope explicitly (for example, 'Apply this formatting to every section, not just the first one')."
  - Sonnet 5 code review: instructions such as "only report high-severity issues" or "don't nitpick" are followed more faithfully, so recall can fall while precision rises; the page tells the model to report every finding with confidence and severity and to filter in a separate step.
  - "Positive examples ... tend to be more effective than negative examples or instructions that tell the model what not to do"; generic "don't use that color" instructions "tend to shift the model to a different fixed palette".
  - Page rule: "Where a technique names a specific model, treat it as measured on that model and re-check it against your own evals".
- No test numbers are published for these statements. Scope is the named Claude models.
- Evidence class: vendor documentation.
- Do differently: remove ALL CAPS, MUST and "if in doubt, use the tool" from system prompts carried over from older models; say each rule once, plainly. If you want a rule applied everywhere, say "everywhere". For review or extraction jobs, ask for everything with a confidence score, then filter in a second step. Do not rely on prefilled assistant text on 4.6 and later.
- Manual change: the manual has no guidance on emphasis, literal reading or prefill (Grep found none). Add a short vendor-doc note to 7.3 and 7.5, scoped by model name. It also supports 7.5's positive-reframing rule with a second vendor statement.

## AXIS 2

### F05  The Format Tax: asking for JSON, XML, LaTeX or Markdown lowers reasoning accuracy on open-weight models
- Source: Lee, D'Antoni, Berg-Kirkpatrick. "The Format Tax." arXiv 2604.03616, 2026-04-04. No venue listed. https://arxiv.org/abs/2604.03616 ; https://arxiv.org/html/2604.03616v1
- Measured: six open-weight models (qwen3-32b, qwen3-8b, olmo3.1-32b, olmo3-7b, smollm3-3b, nemotron3-nano) and four API models (gpt-5-nano, gpt-5.4-nano, claude-haiku-4.5, grok-4.1-fast); four formats; math, science, logic and writing tasks.
- Abstract (abs page): structured output requirements "substantially degrade reasoning and writing performance across open-weight models"; "format-requesting instructions alone cause most of the accuracy loss"; "decoupling recovers most lost accuracy" (reformat in a second pass, or use extended thinking); "most recent closed-weight models show little to no format tax".
- Example number (html, Table 10, second-hand reading): qwen3-32b on GPQA with JSON requested by prompt, no constrained decoding: 52.0% to 43.4% (-8.6 points). Two-turn (free answer, then reformat): 53.0%. With extended thinking the format penalty shrank to -2.2 points against a 52.2% thinking baseline.
- Scope caution: the API models are small or fast tiers; "closed models show little tax" does not cover large frontier models.
- Evidence class: preprint.
- Do differently: on open-weight or small models, get the answer in free text first and ask for the JSON in a second step, or turn thinking on. On current closed models, test before paying for a second call.
- Manual change: 8.1 and 10.5 should say that the cost sits in the format instruction itself, not only in the decoder. Today 10.5 says "constraints guarantee form, not truth"; this adds that asking for form can lower truth on smaller models.

### F06  Anthropic Sonnet 5.5 guide: JSON-only output removes working space on reasoning tasks
- Source: Anthropic, "Prompting Claude Sonnet 5.5" (opened 2026-10-15). https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5
- Verbatim fragments: with structured outputs "the response text holds only the JSON, so the model can work the problem out only in its thinking. When it skips thinking, it can be less accurate on these tasks." Remedy with adaptive thinking: add "Think the problem through before you answer." At high effort the line "brings accuracy close to what the model reaches at xhigh". Without structured outputs the model "often works the problem out in the response text and writes the JSON at the end", so parse the last JSON value; "In testing, this made nearly every response usable without changing its accuracy". "Asking it in the system prompt to think less doesn't reliably reduce its thinking." An instruction not to think makes it "more likely that the model writes internal XML tags in its visible output". Treat a response with stop_reason max_tokens as failed even if the JSON parses.
- No accuracy numbers published. Scope: Claude Sonnet 5.5; tasks needing a few steps of working out (totalling figures, applying a rule, ranking).
- Evidence class: vendor documentation.
- Do differently: when you need JSON from a task that needs working out, keep thinking on (or let the model reason in text and parse the last JSON value); never tell a reasoning model "do not think"; treat max_tokens stops as failures.
- Manual change: 10.5 and Chapter 15 (reasoning visibility): add as vendor-documented evidence that schema-forced output can cost accuracy on current Claude models; pairs with F05 (preprint) from a different model family.

### F07  In long agent sessions, hiding old tool outputs matched LLM summarization at half the cost
- Source: Lindenbauer, Slinko, Felder, Bogomolov, Zharov. "The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management." arXiv 2508.21433, v1 2025-08-29, v3 2025-10-27 (camera-ready for the DL4C workshop at NeurIPS 2025, per arXiv comments). https://arxiv.org/abs/2508.21433
- Measured: SWE-agent on SWE-bench Verified, five model configurations; first check on OpenHands. Abstract: observation masking "halves cost relative to the raw agent" and is "matching, and sometimes slightly exceeding, the solve rate of LLM summarization"; a hybrid "further reduces costs by 7% and 11% compared to just observation masking or LLM summarization, respectively".
- Evidence class: preprint / workshop paper.
- Do differently: in a long coding or agent run, first try dropping or truncating old tool outputs (keep the model's own reasoning and actions) before adding a summarizer model. Scope is software-engineering agents; not tested on chat or research tasks.
- Manual change: Section 8.4 covers compression of static prompts (LLMLingua family) only. Add a short paragraph on agent-trajectory compression; also relevant to Chapter 22 (context engineering).

### F08  Chain-of-Draft's idea is being trained into reasoning models, not prompted
- Source: Cao, Lin, Lin, Fan, Cao, Yuan, Zhao, Yan, Zhang, Tang. "Draft-Thinking: Learning Efficient Reasoning in Long Chain-of-Thought LLMs." arXiv 2603.00578, v1 2026-02-28, v2 2026-10-14. No venue listed. https://arxiv.org/abs/2603.00578
- Measured (abs page): learned draft mode (supervised fine-tuning plus two-stage RL; 847 training problems, 120 RL steps). On MATH500 the draft mode cuts average response length "from 5,668 to 986 tokens, an 82.6% reduction", at "90.6% accuracy compared with 93.0% for the original long CoT model". The base model was not named in the text I read. The page does not mention Chain-of-Draft; it contrasts itself with methods that "primarily rely on prompting, post-hoc compression, or length-regularized optimization".
- Evidence class: preprint.
- Do differently: nothing to change in daily prompting. It is a reason not to expect a "draft, five words per step" prompt to match training-level gains on a reasoning model; use the effort setting for cost control (no source here tests that comparison).
- Manual change: Section 8.2 can note that draft-style brevity is also pursued through training, with the number above and its 2.4-point accuracy cost on MATH500. Appendix A's Chain-of-Draft row (GPT-4o and Claude 3.5 Sonnet on GSM8K) is unchanged.

## Opened and held back (cap of 4 per axis)
- ACON, Kang et al., arXiv 2510.00615, v1 2025-10-01, v3 2026-06-01, "ICML 2026" in arXiv comments. Agent context compression on AppWorld, OfficeBench, Multi-objective QA. Abstract: "reduces peak token usage by 26-54%" "while improving task success over existing compression baselines"; compressor distilled into smaller models; "up to 46% performance improvement" for smaller LMs. Overlaps F07; the strongest peer-reviewed source on agent compression if the manual wants a second citation.
- "The Few-shot Dilemma: Over-prompting Large Language Models," Tang et al., arXiv 2509.13196, v1 2025-09-16, v2 2026-07-26, "accepted to the main track of IEEE FLLM" per arXiv comments. Seven models, one task family (classifying functional and non-functional software requirements). Too many examples "can paradoxically degrade performance in certain LLMs"; best count differs per model; the only abstract number is +1% over prior best. Single-domain; use only as a hedge in 7.2.
- "Thinking with Reasoning Skills: Fewer Tokens, More Accuracy," Zhao et al., arXiv 2604.21764 (April 2026 by ID). On GPT-OSS-120B a Chain-of-Draft-like "Draft" prompt (at most 5 words per step) "achieves the highest accuracy while retaining strong efficiency" and a "Short" token-budget prompt "leads to noticeably larger accuracy degradation", but the numbers are only in Figure 7, which I could not read. Direction only, no number. The paper's own method (retrieved reasoning skills) is not prompt engineering in the manual's sense.

## Manual claims checked on the way (current Anthropic page, opened 2026-10-15)
- 7.3 role quote: the page says "Setting a role in the system prompt focuses Claude's behavior and tone for your use case." Matches the manual.
- 7.4: page says "(20k+ tokens)", "near the top of your prompt, above your query, instructions, and examples", and "Queries at the end can improve response quality by up to 30 percent in tests". Matches the manual; the page still publishes no test details, as the manual says.
- 7.5: page says "Tell Claude what to do instead of what not to do", replacing "Do not use markdown in your response" with "Your response should be composed of smoothly flowing prose paragraphs." Matches the manual.
- Chapter 28 item 7 and 10.4: Sonnet 5 page says manual extended thinking (budget_tokens) "is not supported on Claude Sonnet 5 and returns a 400 error. It was deprecated on Claude Sonnet 4.6 and is now removed." Consistent with the manual's description.

## Cross-axis notes (seen while reading, not Axis 1/2 findings)
- Sonnet 5 page: setting temperature, top_p or top_k to a non-default value "returns a 400 error on Claude Sonnet 5" and a new tokenizer "produces approximately 30% more tokens for the same text". Relevant to Axis 4 (Section 10.1 on sampling controls) and to any token-count comparison on Axis 2 (compression, Chain-of-Draft). Not checked on other model pages.
- Sonnet 5.5 page: "reasoning_extraction" is a refusal category; prompts asking the model to put its reasoning in the reply can trigger a refusal. Relevant to Chapter 15 and to any "show your reasoning" template.

## Not reached
- Chain-of-Symbol: no search made, so no statement about newer evidence either way (the manual's Chapter 28 item 10 stands).
- Few-shot on current reasoning models: one search found only secondary commentary about DeepSeek-R1; no primary source in the window. Open question.
- Persona numbers for the 2026 USC study ("Expert Personas Improve LLM Alignment but Damage Accuracy"): only secondary coverage found, no primary page opened; not used.
