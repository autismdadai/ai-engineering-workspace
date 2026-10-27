# Check A results
A001 | supported | OTK mentions tokens and context window cap per request
A002 | supported | ACW: "system prompt, every message... tool definitions... output... counts too"
A003 | partly supported | Length degradation shown, but "every model tested" not stated: RULER says only half failed 32K; Chroma says "Not every model appears in every experiment"; Liu/NoLiMa middle effect fine
A004 | supported | OpenAI "approximately 4 characters"; Google "about 4 characters" (Google does not say English)
A005 | supported | ATC: counts depend on model/tokenizer; tiktoken is OpenAI tokenizer
A006 | supported | ACW and OCS: input, output, reasoning tokens count
A007 | supported | quote verified in ACE
A008 | supported | both vendors document server-side compaction
A009 | supported | ACX: beta, clears tool results/thinking
A010 | supported | Liu abstract
A011 | supported | Chroma
A012 | supported | HELMET: NIAH-type tasks "do not reliably predict downstream performance"; RULER near-perfect on vanilla NIAH
A013 | supported | "1 token is approximately 4 characters", three-quarters of a word, 100 tokens ~75 words
A014 | supported | "about 4 characters"; "100 tokens is equal to about 60-80 English words"
A015 | supported | "approximately 30% more tokens"; Opus 4.7 and later, Mythos, Fable models; no chars/token ratio published (page words "30%"; quote in claim uses "30 percent", minor)
A016 | supported | POST /v1/messages/count_tokens, free, RPM limits, estimate, system/tools/images/PDFs (PDFs base64 only)
A017 | supported | endpoint, tools, files (PDFs), formatting tokens; page silent on price
A018 | partly supported | tiktoken 0.14.0, Aug 17 2026, MIT, o200k_base for gpt-5/4.1/4o (in tiktoken/model.py) and blob host verified; GPT-6 absent from table verified; NOT checkable: "plain text only", test machine network blocking, "download on first use" not in README; GPT-6 Astra model page names no encoding (consistent)
A019 | partly supported | 258 tokens for images up to 384 px verified; page shows system instructions/tools counted via usage fields, not explicitly for countTokens
A020 | supported | ACW: thinking is a subset of max_tokens; page gives no explicit formula
A021 | supported | exact quote verified
A022 | supported | all three pages: 1,050,000 ctx, 922,000 in, 128,000 out, >272K input: 2x input, 1.5x output, whole request
A023 | supported | both models 1,048,576 in / 65,536 out; 3.1 Pro $2 up to 200k, $4 above
A024 | partly supported | Chroma: every model better on ~300 vs ~113k tokens, but "Not every model appears in every experiment", so "every one of 18" for this test not confirmed
A025 | supported | 400 "prompt is too long"; Claude 4.5+ accepted; stop_reason verified
A026 | partly supported | default disabled, 400, auto "dropping items from the beginning of the conversation" verified; "nothing tells you in the reply" not in source
A027 | supported | verified in ollama server/prompt.go (system + last message kept, slog.Debug); README itself silent
A028 | supported | VRAM tiers 4k/32k/256k; FAQ 4096; Modelfile "Default: 2048"
A029 | supported | OLLAMA_CONTEXT_LENGTH, ollama ps (context-length page), num_ctx per request (FAQ)
A030 | supported | compact-2026-09-04 "wherever it is available"; compact-2026-01-12 150,000 default, 50,000 min
A031 | supported | "extra sampling step that is billed", usage.iterations
A032 | supported | "primary strategy"; clear_tool_uses_20250919, 100,000, keep 3
A033 | supported | "invalidates cached prompt prefixes", clear_at_least; OpenAI context_management/compact_threshold, /responses/compact, "opaque and not intended to be human-interpretable"
A034 | supported | all verified incl. "often 1,000-2,000 tokens"
A035 | supported | quote verified
A036 | supported | 10/20/30 docs, key-value task (one answer document each; "exactly one" not separately checked)
A037 | supported | abstract wording "often highest when relevant information occurs at the beginning or end of the input context"
A038 | supported | Table 6 (Appendix G.2) values match
A039 | supported | 75.8-53.8=22.0; closed-book 56.1% in Table 1; 53.8 and 55.4 below it
A040 | supported | Table 1 models
A041 | supported | Sec 5: 50 vs 20 docs ~1.5 points for GPT-3.5-Turbo
A042 | supported | Sec 4.2: dramatic gain on key-value; "minimally affects" multi-doc QA
A043 | supported | 17 models; "only half" satisfactory at 32K; all claim >=32K
A044 | supported | 99.3% to 69.7% (70.2% is the correct ratio)
A045 | supported | 18 models, July 14 2025, quote verified
A046 | supported | HELMET 59 models ICLR 2025, quote (qualifier "synthetic tasks like NIAH"); Chroma "no notable variation" across 11 positions; repeated words better near beginning
A047 | partly supported | middle dip at 32K on one-hop verified; "two-step... sank toward zero even at the edges" overstated: source says "shift the entire trendline downward toward zero" and "declines even at the edges"; two-hop 32K without CoT is 25.9%
A048 | supported | Veseli et al. 2025: strongest up to 50% of window, then recency/distance pattern
A049 | supported | Feb 2026 (submitted 15 Feb), "largely resolved in newer models"; abstract names Grok-4, GPT-4, Gemini 2.5, GPT-5 (claim omits GPT-4); abstract doesn't describe position test
A050 | supported | models match; accuracy drops when evidence scattered
A051 | supported | both quotes verified
A052 | supported | "near the top of your prompt", 20k+, "up to 30 percent in tests", XML tags with source, quote first; no model/benchmark/date
A053 | supported | both-ends best; above better than below; page has no date, April 2025 inferred from model ID
A054 | supported | query at end; "Last updated 2026-06-22 UTC"
A055 | supported | ACW cached prefixes occupy window
A056 | supported | length degradation robust; Liu models less accurate in middle; weaker later (VES, Chroma, NoLiMa)
A057 | supported | "Context is a critical but finite resource"
A058 | supported | clearing invalidates cache (ACX); compaction/context editing documented
A059 | supported | Liu Sec 5 reranking/short lists; "no source read recommends" is a negative, not checkable
A060 | supported | Chroma LongMemEval result
A061 | partly supported | Chroma page does not itself say it sells a retrieval database (calls itself "open-source search infrastructure for AI", lists ChromaDB); "in line with RULER and NoLiMa" fine
A062 | supported | ATC: ~30% more tokens, recount
A063 | supported | consistent with ABP (docs top, XML source) and OG41 (instructions both ends)
A064 | couldn't check | placeholder URL (pypi.org/pypi/NAME/json), no concrete claim
A065 | supported | ATC says counting free; also PyPI anthropic 1.13.0, Oct 9 2026, MIT, Python>=3.10 (not in cited source ATC)
A066 | supported | Anthropic top-level cache_control; OpenAI "enabled by default"; Gemini implicit caching default
A067 | supported | Anthropic mins 512 to 4,096; Ollama points verified above; (OpenAI/Gemini minimums differ but claim range is Anthropic-compatible)
A068 | partly supported | same as A024: "in every model Chroma tested" not confirmed (not all models in every experiment)
A069 | partly supported | 300 vs 113,000 for "all 18" (see A024); 1.25x/2x write verified; "lab's timestamp case 38,700 vs 31,200" is own lab data, not checkable; rest supported
A070 | supported | ACW incl. cached tokens
A071 | supported | truncation disabled default => 400
A072 | supported | via ollama source; no error
A073 | supported | Liu 2023 models incl. GPT-3.5-Turbo, Claude-1.3
A074 | supported | NoLiMa: 13 LLMs, 11 below 50% at 32K (low-overlap needle condition per paper)
A075 | supported | titles/URLs exist
A076 | supported | NoLiMa 2502.05167; ACE title matches
A077 | supported | ESM "largely resolved"; VES depends on window fill; Chroma/NoLiMa task dependence
A078 | supported | RULER near-perfect vanilla NIAH, harder tasks fail
A079 | supported | HELMET (qualifier "synthetic tasks like NIAH")
A080 | supported | 30% claim has no model/benchmark/date in page; "lab's placement test" own
A081 | partly supported | OpenAI opaque item verified; "doesn't match Anthropic's documented exact-match rules" refers to an unseen claim; "nobody has repeated it" not checkable
A082 | partly supported | tool-result clearing breaks cache, org isolation (Anthropic, OpenAI), thresholds 272k/200k/100k (Haiku 5.5) verified; GUA (arXiv 2502.07776) is a 2025 paper (submitted Feb 11 2025) not 2024; it found global cache sharing at seven providers; Google isolation not checked
A083 | supported | consistent with sources
A084 | supported | old long-context-tips address serves "Prompting best practices" page with "Long context prompting" subsection
A085 | supported | OG41 both-ends; Google query at end; Anthropic docs-top, query at end
