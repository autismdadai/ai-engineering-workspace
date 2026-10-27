# Claims A

A001. That limit is its **context window**, measured in **tokens**, the pieces of words a model reads .
   Sources: OTK: https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them

A002. Everything counts against it: the system prompt, the tool definitions, every document, every past turn and the answer the model writes .
   Sources: ACW: https://platform.claude.com/docs/en/build-with-claude/context-windows

A003. And a request that fits can still go wrong: accuracy falls as inputs get longer, on every model tested in the studies read here , and some models use facts in the middle of a long input less well than facts at the start or end .
   Sources: CHR: https://www.trychroma.com/research/context-rot; LIU: https://arxiv.org/abs/2307.03172; NOL: https://arxiv.org/abs/2502.05167; RUL: https://arxiv.org/abs/2404.06654

A004. The piece of text a model reads as one unit, often part of a word | Token | About 4 characters of English on average, by OpenAI's and Google's rules of thumb
   Sources: GTK: https://ai.google.dev/gemini-api/docs/tokens; OTK: https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them

A005. The program that splits text into tokens | Tokenizer; encoding | Differs between vendors and model generations
   Sources: ATC: https://platform.claude.com/docs/en/build-with-claude/token-counting; TIK: https://pypi.org/project/tiktoken/ https://github.com/openai/tiktoken

A006. Everything the model reads and writes in one request, and its maximum size | Context; context window | Includes input, output and any thinking
   Sources: ACW: https://platform.claude.com/docs/en/build-with-claude/context-windows; OCS: https://developers.openai.com/api/docs/guides/conversation-state.md

A007. Choosing and arranging what goes into the window | Context engineering | Anthropic: curating "the smallest possible set of high-signal tokens"
   Sources: ACE: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

A008. Replacing old turns with a summary written by the model | Compaction | A server feature at Anthropic and OpenAI
   Sources: ACO: https://platform.claude.com/docs/en/build-with-claude/compaction https://platform.claude.com/docs/en/build-with-claude/compaction-threshold; OCP: https://developers.openai.com/api/docs/guides/compaction.md

A009. Removing old tool results or thinking from the history | Context editing | Anthropic, beta
   Sources: ACX: https://platform.claude.com/docs/en/build-with-claude/context-editing

A010. A model using facts at the start and end of a long input better than facts in the middle | Position effect; "lost in the middle"; U-shaped curve | Named by Liu et al. for 2023 models
   Sources: LIU: https://arxiv.org/abs/2307.03172

A011. Accuracy falling as the input gets longer | Length degradation; "context rot" | "Context rot" is Chroma's name
   Sources: CHR: https://www.trychroma.com/research/context-rot

A012. A test that hides one fact in a long input and asks for it | Needle in a haystack (NIAH) | The simplest long-context test; it can overstate ability
   Sources: HEL: https://arxiv.org/abs/2410.02694; RUL: https://arxiv.org/abs/2404.06654

A013. **Rules of thumb, and their limits.** OpenAI: "1 token is approximately 4 characters", about three quarters of a word, so 100 tokens is about 75 English words .
   Sources: OTK: https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them

A014. Google: about 4 characters, and 100 tokens is 60 to 80 English words .
   Sources: GTK: https://ai.google.dev/gemini-api/docs/tokens

A015. Anthropic publishes no ratio, but says that Claude Opus 4.7 and later models (and the Fable and Mythos models) use a newer tokenizer that turns the same text into "approximately 30 percent more tokens than on earlier models" .
   Sources: ATC: https://platform.claude.com/docs/en/build-with-claude/token-counting

A016. Anthropic | `POST /v1/messages/count_tokens` (`client.messages.count_tokens` in the Python SDK) | Free, with its own requests-per-minute limits; counts system prompt, tools, images and PDFs; the result "is an estimate"
   Sources: ATC: https://platform.claude.com/docs/en/build-with-claude/token-counting

A017. OpenAI | `POST /v1/responses/input_tokens` | Counts the full Responses input, including tools and files, with the formatting tokens a plain tokenizer misses; the page doesn't say whether it's free
   Sources: OTC: https://developers.openai.com/api/docs/guides/token-counting.md

A018. OpenAI, offline | `tiktoken` (MIT, 0.14.0, August 17, 2026) | Plain text only. Its model table maps gpt-5, gpt-4.1 and gpt-4o to the `o200k_base` encoding and has no entry for GPT-6 models, so `encoding_for_model("gpt-6-astra")` would fail . No OpenAI page read here names GPT-6's encoding . The first use downloads the encoding file from `openaipublic.blob.core.windows.net`, which the test machine's network blocks
   Sources: TIK: https://pypi.org/project/tiktoken/ https://github.com/openai/tiktoken

A019. Google | `countTokens` | Counts system instructions, tools and media; an image of up to 384 pixels per side is 258 tokens
   Sources: GTK: https://ai.google.dev/gemini-api/docs/tokens

A020. where *window* is the model's context window in tokens and *reserved output* is the largest answer you allow, thinking included (`max_tokens` at Anthropic) .
   Sources: ACW: https://platform.claude.com/docs/en/build-with-claude/context-windows

A021. Tool definitions count, and so do cached prefixes: caching "changes what you pay for those tokens, not whether they count" .
   Sources: ACW: https://platform.claude.com/docs/en/build-with-claude/context-windows

A022. OpenAI GPT-6 Astra, GPT-6.1 Sol, GPT-6 Luna | 1,050,000: up to 922,000 in and 128,000 out | 128,000 | Over 272,000 input tokens, the whole request is billed at 2x input and 1.5x output
   Sources: OMD: https://developers.openai.com/api/docs/models.md https://developers.openai.com/api/docs/models/gpt-6-astra.md https://developers.openai.com/api/docs/models/gpt-6.1-sol.md https://developers.openai.com/api/docs/models/gpt-6-luna.md

A023. Google Gemini 3.8 Flash; Gemini 3.1 Pro (preview) | 1,048,576 input | 65,536 | 3.1 Pro: $2 per million input tokens up to 200,000, $4 above
   Sources: GMD: https://ai.google.dev/gemini-api/docs/models https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview; GPR: https://ai.google.dev/gemini-api/docs/pricing

A024. Chroma found that every one of 18 models did better on a conversation-memory test given a focused prompt of about 300 tokens than given the full history of about 113,000 tokens .
   Sources: CHR: https://www.trychroma.com/research/context-rot

A025. Anthropic | Input alone over the window: HTTP 400, "prompt is too long". On Claude 4.5 and newer, input plus `max_tokens` over the window is accepted, and generation stops with `stop_reason: "model_context_window_exceeded"`. Nothing is cut silently | An error, or that stop reason
   Sources: ACW: https://platform.claude.com/docs/en/build-with-claude/context-windows

A026. OpenAI, Responses API | `truncation` defaults to `disabled`: an input over the window fails with a 400 error. Set to `auto`, it drops items "from the beginning of the conversation" to fit | With `auto`, nothing tells you in the reply what was dropped
   Sources: OTR: https://developers.openai.com/api/reference/terraform/resources/responses

A027. Ollama (a local runtime) | For chat requests, truncation is on by default: the oldest messages are dropped until the rest fits, keeping system messages and always the last message, and the server logs this only at debug level | Only by comparing `prompt_eval_count` with what you sent
   Sources: OLS: https://github.com/ollama/ollama

A028. Ollama's default context length is documented three ways on its own pages: by graphics memory (4K, 32K or 256K tokens) on the context-length page, 4096 in the FAQ, and 2048 in the Modelfile reference .
   Sources: OLC: https://docs.ollama.com/context-length https://docs.ollama.com/faq https://docs.ollama.com/modelfile

A029. Set `num_ctx` yourself in each request, or `OLLAMA_CONTEXT_LENGTH` for the server, and check with `ollama ps` .
   Sources: OLC: https://docs.ollama.com/context-length https://docs.ollama.com/faq https://docs.ollama.com/modelfile

A030. There are two kinds: on demand (header `compact-2026-09-04`, which the docs recommend wherever available) and at a token threshold (header `compact-2026-01-12`, default trigger 150,000 input tokens, minimum 50,000) .
   Sources: ACO: https://platform.claude.com/docs/en/build-with-claude/compaction https://platform.claude.com/docs/en/build-with-claude/compaction-threshold

A031. The summary is an extra model call, billed and reported in `usage.iterations` .
   Sources: ACO: https://platform.claude.com/docs/en/build-with-claude/compaction https://platform.claude.com/docs/en/build-with-claude/compaction-threshold

A032. Anthropic's context-windows page calls compaction "the primary strategy" for long conversations . - **Anthropic context editing** (beta) clears old tool results (`clear_tool_uses_20250919`, default trigger 100,000 input tokens, keeping the last 3 tool uses) or old thinking blocks .
   Sources: ACW: https://platform.claude.com/docs/en/build-with-claude/context-windows; ACX: https://platform.claude.com/docs/en/build-with-claude/context-editing

A033. Clearing "invalidates cached prompt prefixes", so the docs advise clearing enough at once to be worth the new cache write . - **OpenAI compaction** works automatically through `context_management` with a `compact_threshold`, or on request at `/responses/compact`; the result is an encrypted item, "opaque and not intended to be human-interpretable" .
   Sources: ACX: https://platform.claude.com/docs/en/build-with-claude/context-editing; OCP: https://developers.openai.com/api/docs/guides/compaction.md

A034. Anthropic's engineering post adds the techniques an application can use itself: keep identifiers and fetch the full text just in time, keep structured notes outside the context, and give sub-agents their own context so they return short summaries ("often 1,000-2,000 tokens") .
   Sources: ACE: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

A035. It calls clearing old tool results "one of the safest lightest touch forms of compaction" .
   Sources: ACE: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

A036. **What Liu et al. found (2023 models).** "Lost in the Middle" tested question answering over 10, 20 or 30 documents, exactly one of which held the answer, plus a key-value lookup task .
   Sources: LIU: https://arxiv.org/abs/2307.03172

A037. Accuracy was "often highest when relevant information occurs at the beginning or end" and lowest in the middle: a U-shaped curve .
   Sources: LIU: https://arxiv.org/abs/2307.03172

A038. For GPT-3.5-Turbo with 20 documents, accuracy by the position of the answer document was 75.8% (first), 57.2% (5th), 53.8% (10th), 55.4% (15th) and 63.2% (20th) . (location: Table 6)
   Sources: LIU: https://arxiv.org/abs/2307.03172

A039. That's a drop of 22.0 percentage points from the first position to the worst middle one, and at the 10th and 15th positions it scored below its closed-book score of 56.1%, with no documents at all . (location: Table 1)
   Sources: LIU: https://arxiv.org/abs/2307.03172

A040. The models were all from 2023: GPT-3.5-Turbo, Claude-1.3, MPT-30B-Instruct, LongChat-13B and others .
   Sources: LIU: https://arxiv.org/abs/2307.03172

A041. Its own advice: put the most relevant documents first (rerank) and keep retrieved lists short, since going from 20 to 50 documents added only about 1.5 points for GPT-3.5-Turbo . (location: §5)
   Sources: LIU: https://arxiv.org/abs/2307.03172

A042. Repeating the question before and after the data fixed the key-value task but barely changed document question answering . (location: §4.2)
   Sources: LIU: https://arxiv.org/abs/2307.03172

A043. - *Length hurts, robustly.* RULER (17 models, 2024): near-perfect on the simple needle test, but only about half kept satisfactory performance at 32,000 tokens, though all claimed at least that much .
   Sources: RUL: https://arxiv.org/abs/2404.06654

A044. GPT-4o went from 99.3% to 69.7%, that is to 70.2% of its base score .
   Sources: NOL: https://arxiv.org/abs/2502.05167

A045. Chroma (18 models including Claude Opus 4, GPT-4.1, Gemini 2.5 Pro and Qwen3, July 2025): performance "grows increasingly unreliable as input length grows", even on simple tasks .
   Sources: CHR: https://www.trychroma.com/research/context-rot

A046. HELMET (59 models, ICLR 2025) adds that needle tests "do not reliably predict downstream performance" . - *Position matters less, and depends on the task.* Chroma's needle test found "no notable variation" across 11 positions, but its repeated-words task did better when the unique word was near the beginning .
   Sources: CHR: https://www.trychroma.com/research/context-rot; HEL: https://arxiv.org/abs/2410.02694

A047. NoLiMa saw a middle dip on one-step questions at 32,000 tokens; on two-step questions length dominated and accuracy sank toward zero even at the edges . (location: §4.4.2)
   Sources: NOL: https://arxiv.org/abs/2502.05167

A048. (preprint, 2025) found the U-shape strongest when the input fills up to half the window, turning into a bias toward the end beyond that .
   Sources: VES: https://arxiv.org/abs/2508.07479

A049. A February 2026 preprint testing GPT-5, Grok-4 and Gemini 2.5 says the problem is "largely resolved in newer models", but its abstract doesn't show how position was tested, so it's weak evidence .
   Sources: ESM: https://arxiv.org/abs/2602.14188

A050. A 2026 preprint on Gemini 2.5 Flash, GPT-5-mini, Claude 4.5 Haiku and DeepSeek-v3.2 found accuracy drops when the needed evidence is spread across the input .
   Sources: EBR: https://arxiv.org/abs/2601.02023

A051. Even the vendors say so: Google's docs say that with many needles "the model does not perform with the same accuracy" , and OpenAI's GPT-4.1 guide says performance can "degrade as more items are required to be retrieved" .
   Sources: GLC: https://ai.google.dev/gemini-api/docs/long-context; OG41: https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide.md

A052. Anthropic | For inputs of 20,000 tokens or more, put long documents "near the top of your prompt", above the query and instructions; queries at the end "can improve response quality by up to 30 percent in tests"; wrap each document in tags with its source; ask the model to quote the relevant parts first | The 30% has no model, benchmark or date: a vendor claim
   Sources: ABP: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices

A053. OpenAI (GPT-4.1 guide) | Instructions at both the beginning and the end of a long context work best; if only once, above the context is better than below | GPT-4.1, April 2025; newer guides not read
   Sources: OG41: https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide.md

A054. Google | Put the query at the end, after the other context | Gemini long-context page, updated June 22, 2026
   Sources: GLC: https://ai.google.dev/gemini-api/docs/long-context

A055. And it doesn't make a cached prefix free of the window: those tokens still count .
   Sources: ACW: https://platform.claude.com/docs/en/build-with-claude/context-windows

A056. Attention quality "frequently degrades" with length; models "ignore" mid-prompt information (P2-02) | Half right. Length degradation is robust across current studies . "Ignore" is too strong: Liu et al.'s 2023 models were less accurate in the middle, not blind , and for current models the position effect is weaker and task-dependent | 3.4
   Sources: CHR: https://www.trychroma.com/research/context-rot; HEL: https://arxiv.org/abs/2410.02694; LIU: https://arxiv.org/abs/2307.03172; NOL: https://arxiv.org/abs/2502.05167; RUL: https://arxiv.org/abs/2404.06654; VES: https://arxiv.org/abs/2508.07479

A057. The context window is a finite, curated resource (P2-03) | Confirmed: Anthropic's own definition | 1, 3.2
   Sources: ACE: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

A058. Sliding-window truncation that keeps system instructions through KV reuse (P2-12) | Illustrative . The documented versions today are server compaction and context editing; note that clearing content invalidates the cache | 3.3
   Sources: ACO: https://platform.claude.com/docs/en/build-with-claude/compaction https://platform.claude.com/docs/en/build-with-claude/compaction-threshold; ACX: https://platform.claude.com/docs/en/build-with-claude/context-editing

A059. Put "aggressively summarized" documents in the middle to fight attention decay (P2-13) | Unsupported. Liu et al. advise reranking relevant passages to the front and keeping lists short ; no source read recommends summaries in the middle | 3.4 (location: §5)
   Sources: LIU: https://arxiv.org/abs/2307.03172

A060. *Less context, better answers* .
   Sources: CHR: https://www.trychroma.com/research/context-rot

A061. Chroma sells a retrieval database, so read it as a vendor's report; the result is in line with RULER and NoLiMa .
   Sources: NOL: https://arxiv.org/abs/2502.05167; RUL: https://arxiv.org/abs/2404.06654

A062. Count the real number with `count_tokens` before going live; on this model the newer tokenizer may give about 30% more than the estimate .
   Sources: ATC: https://platform.claude.com/docs/en/build-with-claude/token-counting

A063. *Step 2, placement.* System prompt first; then the contract inside `<document>` tags with its source; then the question, with the key instruction ("answer only from the contract; quote the clause") repeated after the document (Section 3.4) .
   Sources: ABP: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices; OG41: https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide.md

A064. Versions from PyPI .
   Sources: PYPI: https://pypi.org/pypi/NAME/json

A065. anthropic | Claude API, including `count_tokens` and caching | MIT | Free; API usage is paid, token counting is free | Python 3.10 or later | An API key (Part 01, Section 3.5) | 1.13.0, October 9, 2026 | PyPI
   Sources: ATC: https://platform.claude.com/docs/en/build-with-claude/token-counting

A066. - **Best default for a solo builder on a hosted API:** count with the vendor's own counter, plan with a margin, put stable material first, and turn on caching (at Anthropic, one top-level `cache_control`; at OpenAI and Gemini it's already on) .
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; ATC: https://platform.claude.com/docs/en/build-with-claude/token-counting; GCC: https://ai.google.dev/gemini-api/docs/caching https://ai.google.dev/gemini-api/docs/generate-content/caching; OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

A067. Test the placement on your model with your own documents (Section 8, step 7). - **Best free option:** a local model through Ollama with `num_ctx` set explicitly, because its defaults differ between its own pages and it cuts long chats without telling you . - **When not to bother with caching:** prompts under the minimum (512 to 4,096 tokens, by model), or requests too rare to reuse a prefix within its lifetime .
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; OLC: https://docs.ollama.com/context-length https://docs.ollama.com/faq https://docs.ollama.com/modelfile; OLS: https://github.com/ollama/ollama; OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

A068. When not to use a long context at all: when retrieval can find the few passages that matter (Part 05); smaller focused contexts did better in every model Chroma tested .
   Sources: CHR: https://www.trychroma.com/research/context-rot

A069. Accuracy falls with length on every model in the studies read , and a focused 300-token prompt beat a 113,000-token one for all 18 models Chroma tested . - *"Models ignore the middle of the prompt."* 2023 models were less accurate there, not blind ; for current models single-fact recall is mostly robust to position, while many-fact tasks still suffer with length . - *"A token is a word."* About three quarters of a word in English, by OpenAI's rule of thumb , and not the same between tokenizers . - *"Caching changes the answer."* It doesn't; it reuses the processed prompt . - *"Caching always saves money."* A write costs 1.25x or 2x; if nothing reads it, you pay more (the lab's timestamp case cost 38,700 units against 31,200 without caching) . - *"Cached tokens don't count toward the window."* They do .
   Sources: ACW: https://platform.claude.com/docs/en/build-with-claude/context-windows; APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; ATC: https://platform.claude.com/docs/en/build-with-claude/token-counting; CHR: https://www.trychroma.com/research/context-rot; LIU: https://arxiv.org/abs/2307.03172; NOL: https://arxiv.org/abs/2502.05167; OTK: https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them; RUL: https://arxiv.org/abs/2404.06654

A070. *Answers.* (1) Everything: system prompt, tools, messages, documents, the output and any thinking, and cached tokens too .
   Sources: ACW: https://platform.claude.com/docs/en/build-with-claude/context-windows

A071. (2) OpenAI returns a 400 error unless `truncation` is `auto` ;
   Sources: OTR: https://developers.openai.com/api/reference/terraform/resources/responses

A072. Ollama drops the oldest messages, keeping system messages and the last one, without an error .
   Sources: OLS: https://github.com/ollama/ollama

A073. (3) 2023 models such as GPT-3.5-Turbo and Claude-1.3 ;
   Sources: LIU: https://arxiv.org/abs/2307.03172

A074. NoLiMa found that 11 of 13 later models fell below half their short-context score at 32,000 tokens when the needle shares few words with the question .
   Sources: NOL: https://arxiv.org/abs/2502.05167

A075. - Anthropic, "Prompt caching" and "Context windows" (the platform docs) . - OpenAI, "Prompt caching" guide . - Google, "Long context" and "Context caching" . - Liu et al., "Lost in the Middle", arXiv 2307.03172 ;
   Sources: ACW: https://platform.claude.com/docs/en/build-with-claude/context-windows; APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; GCC: https://ai.google.dev/gemini-api/docs/caching https://ai.google.dev/gemini-api/docs/generate-content/caching; GLC: https://ai.google.dev/gemini-api/docs/long-context; LIU: https://arxiv.org/abs/2307.03172; OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

A076. NoLiMa, arXiv 2502.05167 . - Anthropic, "Effective context engineering for AI agents" .
   Sources: ACE: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents; NOL: https://arxiv.org/abs/2502.05167

A077. The studies that exist disagree in emphasis: one 2026 preprint calls the problem "largely resolved" , while others find the effect depends on the task and on how full the window is .
   Sources: CHR: https://www.trychroma.com/research/context-rot; ESM: https://arxiv.org/abs/2602.14188; NOL: https://arxiv.org/abs/2502.05167; VES: https://arxiv.org/abs/2508.07479

A078. Test on your own model and documents. - **Needle tests flatter models.** Simple needle tests are near-perfect while harder tasks fail ;
   Sources: RUL: https://arxiv.org/abs/2404.06654

A079. HELMET found they "do not reliably predict downstream performance" .
   Sources: HEL: https://arxiv.org/abs/2410.02694

A080. The lab's placement test is a needle test too, good for finding a position effect, not for proving a model can use a long context. - **Vendor quality claims are unreplicated.** Anthropic's "up to 30 percent" for queries at the end has no model, benchmark or date .
   Sources: ABP: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices

A081. It doesn't match Anthropic's documented exact-match rules , and nobody has repeated it. - **Compaction is lossy.** A summary drops detail, and OpenAI's compacted item is opaque, so you can't read what it kept .
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; OCP: https://developers.openai.com/api/docs/guides/compaction.md

A082. Clearing tool results also breaks the cache . - **Privacy.** Shared caches leaked through timing at several providers in 2024 ; the big vendors now isolate by organization , but users of one key or organization still share. - **Cost.** Long contexts cost more than short ones even with caching, and some models charge a higher rate above a threshold (OpenAI over 272,000 input tokens, Gemini 3.1 Pro over 200,000, Haiku 5.5 over 100,000) . - **When this is the wrong tool.** When the corpus is too big for any window, or most of it is irrelevant to each question: that's retrieval (Part 05).
   Sources: ACX: https://platform.claude.com/docs/en/build-with-claude/context-editing; APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; APR: https://platform.claude.com/docs/en/about-claude/pricing; GPR: https://ai.google.dev/gemini-api/docs/pricing; GUA: https://arxiv.org/abs/2502.07776; OMD: https://developers.openai.com/api/docs/models.md https://developers.openai.com/api/docs/models/gpt-6-astra.md https://developers.openai.com/api/docs/models/gpt-6.1-sol.md https://developers.openai.com/api/docs/models/gpt-6-luna.md; OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

A083. *Taxonomy flag 3 (position effects, §4.1 and §7.4).* The ledger's settlement stands, with more evidence: the U-shape is documented for 2023 models ; for later models the effect is weaker and task-dependent, and length degradation is the robust finding .
   Sources: CHR: https://www.trychroma.com/research/context-rot; HEL: https://arxiv.org/abs/2410.02694; LIU: https://arxiv.org/abs/2307.03172; NOL: https://arxiv.org/abs/2502.05167; VES: https://arxiv.org/abs/2508.07479

A084. *New: Anthropic's long-context page moved.* Sources that cite Anthropic's "long context tips" page should point to "Prompting best practices", heading "Long context prompting", which the old address now serves .
   Sources: ABP: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices

A085. This part's evidence supports the "again at the end" half for documents-then-question layouts but not a fixed rule, since the vendors differ (Section 3.4).
   Sources: ABP: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices; GLC: https://ai.google.dev/gemini-api/docs/long-context; OG41: https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide.md
