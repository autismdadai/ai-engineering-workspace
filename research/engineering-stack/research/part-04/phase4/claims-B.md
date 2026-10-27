# Claims B

B001. You pay less for the reused part, and the reply can start sooner .
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; GCC: https://ai.google.dev/gemini-api/docs/caching https://ai.google.dev/gemini-api/docs/generate-content/caching; OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

B002. The catch is the word *exactly*: one changed character early in the prompt means everything after it is processed again .
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching

B003. Reusing the processed start of a prompt in a later request | Prompt caching; prefix caching | The provider stores the processed form, not your text's meaning
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching

B004. The place in a prompt where you ask the provider to cache everything before it | Breakpoint; `cache_control` | Anthropic's name; up to 4 per request
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching

B005. Storing a prefix the first time; using it again later | Cache write; cache read (hit) | A write can cost more than normal input; a read costs much less
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

B006. How long a cached prefix stays usable | Lifetime; time to live (TTL) | 5 minutes or 1 hour at Anthropic; 30 minutes or more at OpenAI's newest models
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

B007. The model's stored working state for each processed token | KV cache (key-value cache) | What a prefix cache keeps; Part 11 covers it inside engines
   Sources: SGL: https://arxiv.org/abs/2312.07104; VPC: https://docs.vllm.ai/en/latest/design/prefix_caching.html https://github.com/vllm-project/vllm

B008. A shortcut that leaks information through how long something takes | Timing side channel | How caches shared between users were detected
   Sources: GUA: https://arxiv.org/abs/2502.07776

B009. Claude Fable 5.1 and 5, Mythos 5.1 and 5, Opus 5.5 to 4.6, Sonnet 5.5, 5 and 4.6, Haiku 5.5 | 1,000,000 tokens, no beta header needed | Up to 128,000 | None, except Haiku 5.5: prompts over 100,000 tokens cost more
   Sources: ACW: https://platform.claude.com/docs/en/build-with-claude/context-windows; APR: https://platform.claude.com/docs/en/about-claude/pricing

B010. llama.cpp server | The context size comes from the model unless set (`-c`, `--ctx-size`); context shift is off by default | The README read doesn't say whether an oversized prompt errors or is cut
   Sources: LCS: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md

B011. That's why caching works on a **prefix**: the identical start of a prompt .
   Sources: SGL: https://arxiv.org/abs/2312.07104; VPC: https://docs.vllm.ai/en/latest/design/prefix_caching.html https://github.com/vllm-project/vllm

B012. Anthropic: "Cache hits require 100% identical prompt segments" .
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching

B013. **The order that matters.** At Anthropic, a request is cached in the order tools, then system, then messages, and a change at one level invalidates that level and everything after it .
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching

B014. Changing the tools clears everything; changing thinking or effort settings clears the message blocks .
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching

B015. OpenAI routes each request by a hash of its first tokens, tools included .
   Sources: OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

B016. Turned on by | You: one top-level `cache_control` (automatic: the breakpoint moves to the last cacheable block as a chat grows), or `cache_control` on up to 4 blocks | On by default; explicit breakpoints also supported | Implicit caching on by default for Gemini 2.5 and newer; explicit caches through `client.caches.create` (beta)
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; GCC: https://ai.google.dev/gemini-api/docs/caching https://ai.google.dev/gemini-api/docs/generate-content/caching; OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

B017. Minimum length | 512 tokens on the newest models (Fable 5.1 and 5, Mythos 5.1 and 5, Opus 5.5 and 5, Sonnet 5.5, Haiku 5.5); 1,024 on Sonnet 5, Opus 4.8 and Sonnet 4.6 and 4.5; up to 4,096 on older ones. Shorter prefixes are "processed without caching, and no error is returned" | 1,024 visible input tokens | Implicit: 4,096 on Gemini 3.8 Flash, 3.6 Flash and 3.1 Pro; 2,048 on 2.5 Flash and Pro. Explicit: not stated
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; GCC: https://ai.google.dev/gemini-api/docs/caching https://ai.google.dev/gemini-api/docs/generate-content/caching; OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

B018. Write | 1.25x base input (5-minute lifetime) or 2x (1 hour) | 1.25x; earlier models: no write charge | Storage per million tokens per hour, by model (Section 3.6)
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; GPR: https://ai.google.dev/gemini-api/docs/pricing; OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md; OPP: https://developers.openai.com/api/docs/pricing.md

B019. Read | 0.1x; 0.05x on Opus 5.5 and Sonnet 5.5; 0.025x on Fable 5.1 and Mythos 5.1 | 0.1x; 0.05x on GPT-6.1 Sol | 0.1x on every model listed (computed from the price table)
   Sources: APR: https://platform.claude.com/docs/en/about-claude/pricing; GPR: https://ai.google.dev/gemini-api/docs/pricing; OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md; OPP: https://developers.openai.com/api/docs/pricing.md

B020. Lifetime | 5 minutes, refreshed free on each hit; or `"ttl": "1h"` | At least 30 minutes after the last write or use (`prompt_cache_options.ttl`, only value `30m`) | Explicit: 1 hour unless set; implicit: not stated
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; GCC: https://ai.google.dev/gemini-api/docs/caching https://ai.google.dev/gemini-api/docs/generate-content/caching; OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

B021. Lookback | Each breakpoint checks at most 20 block positions back for an earlier entry | Automatic routing | Automatic
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; GCC: https://ai.google.dev/gemini-api/docs/caching https://ai.google.dev/gemini-api/docs/generate-content/caching; OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

B022. Reported as | `cache_creation_input_tokens`, `cache_read_input_tokens`, `input_tokens` (the uncached tail) | `usage.input_tokens_details.cached_tokens` and `cache_write_tokens` | `usage_metadata`
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; GCC: https://ai.google.dev/gemini-api/docs/caching https://ai.google.dev/gemini-api/docs/generate-content/caching; OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

B023. Shared with | Isolated between organizations; per workspace on the Claude API | "not shared across organizations" | Not checked
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

B024. DeepSeek caches on disk by default and bills a hit at about 0.02x of a miss on its flash model .
   Sources: DSC: https://api-docs.deepseek.com/guides/kv_cache https://api-docs.deepseek.com/quick_start/pricing

B025. Amazon Bedrock offers explicit `cachePoint`s with up to 4 checkpoints and a 5-minute lifetime reset on each hit, and says "Repeating an identical prompt doesn't guarantee a cache hit" .
   Sources: BRK: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html

B026. That last warning holds everywhere: implicit caches are best effort .
   Sources: BRK: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html; GCC: https://ai.google.dev/gemini-api/docs/caching https://ai.google.dev/gemini-api/docs/generate-content/caching

B027. **Rate limits differ too.** At Anthropic, cache reads don't count toward the input-tokens-per-minute limit on most models, so with an 80% hit rate a 2,000,000-token limit lets through 10,000,000 input tokens per minute .
   Sources: ARL: https://platform.claude.com/docs/en/api/rate-limits

B028. At OpenAI, "Cached input tokens still count toward tokens-per-minute limits" .
   Sources: OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

B029. And a 300-token prefix on a model with a 512-token minimum is never cached, and no error says so, exactly as Anthropic documents :
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching

B030. **What caching doesn't do.** It doesn't change the answer: "Prompt caching has no effect on output token generation" .
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching

B031. It doesn't make generation faster, only the processing of the prompt .
   Sources: VPC: https://docs.vllm.ai/en/latest/design/prefix_caching.html https://github.com/vllm-project/vllm

B032. Anthropic's pricing page says the same: caching "pays off after one cache read for the 5-minute duration", and after two for the 1-hour one .
   Sources: APR: https://platform.claude.com/docs/en/about-claude/pricing

B033. OpenAI's GPT-5.6 and later have the same 1.25x and 0.1x, so the same single read .
   Sources: OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

B034. **Worked totals.** Claude Sonnet 5.5 costs $2 per million input tokens and reads at 0.05x .
   Sources: APR: https://platform.claude.com/docs/en/about-claude/pricing

B035. On the October 13 prices , that's 0.74 uses per hour on Gemini 3.8 Flash ($0.75 input, $0.075 cached, $0.50 storage), 2.5 on Gemini 3.1 Pro preview ($2, $0.20, $4.50) and 4.0 on Gemini 2.5 Pro ($1.25, $0.125, $4.50) .
   Sources: GPR: https://ai.google.dev/gemini-api/docs/pricing

B036. Gemini 3.8 Flash and 3.6 Flash prices double on January 1, 2027 .
   Sources: GPR: https://ai.google.dev/gemini-api/docs/pricing

B037. OpenAI's caching page says input can be "discounted up to 95%" .
   Sources: OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

B038. (preprint, 2026) ran a deep-research agent with a 10,000-token system prompt, 40 sessions per condition per model .
   Sources: LUM: https://arxiv.org/abs/2601.06007

B039. Against no caching, cost fell 79 to 81% on GPT-5.2, 78 to 79% on Claude Sonnet 4.5, 46 to 48% on GPT-4o and 28 to 41% on Gemini 2.5 Pro, across three caching strategies . (location: Table 1)
   Sources: LUM: https://arxiv.org/abs/2601.06007

B040. Time to first token didn't always improve: it ranged from 8.8% slower to 30.9% faster depending on model and strategy .
   Sources: LUM: https://arxiv.org/abs/2601.06007

B041. The abstract reports the rosier "41-80%" and "13-31%"; its own table's lowest results fall below both ranges .
   Sources: LUM: https://arxiv.org/abs/2601.06007

B042. Its advice matches this part's: cache the stable system prompt, keep tool definitions fixed, put changing content last, and don't cache tool results .
   Sources: LUM: https://arxiv.org/abs/2601.06007

B043. - **vLLM** hashes each full block of KV cache from the previous block's hash and the block's tokens, caches only full blocks, and evicts the least recently used first .
   Sources: VPC: https://docs.vllm.ai/en/latest/design/prefix_caching.html https://github.com/vllm-project/vllm

B044. A per-request `cache_salt` limits sharing to requests with the same salt, to stop timing attacks between users of a shared server; the default hash has been SHA-256 since v0.11 .
   Sources: VPC: https://docs.vllm.ai/en/latest/design/prefix_caching.html https://github.com/vllm-project/vllm

B045. In the source of release 0.31.0 (October 5, 2026), `enable_prefix_caching` defaults to `True`, while the docs still tell you to set it .
   Sources: VPC: https://docs.vllm.ai/en/latest/design/prefix_caching.html https://github.com/vllm-project/vllm

B046. It speeds up only the processing of the prompt, not the writing of new tokens . - **SGLang**'s RadixAttention keeps finished requests' KV cache in a radix tree and evicts the least recently used leaf first; its paper measured cache hit rates of 50% to 99% across its benchmarks and up to 6.4x throughput, on its authors' own system .
   Sources: SGL: https://arxiv.org/abs/2312.07104; VPC: https://docs.vllm.ai/en/latest/design/prefix_caching.html https://github.com/vllm-project/vllm

B047. Its server's eviction policy defaults to LRU .
   Sources: SGA: https://docs.sglang.io/docs/advanced_features/server_arguments.md https://github.com/sgl-project/sglang

B048. In the release 0.5.21 source the switch is named `disable_radix_cache` and defaults to `False` where it is declared, which suggests the cache is on unless turned off . - **llama.cpp**'s server reuses the previous request's KV cache by default (`cache_prompt`), and warns that "enabling this option can cause nondeterministic results" . - **Ollama** keeps a model loaded for 5 minutes by default (`keep_alive`) and reports `prompt_eval_cached_count`, "Number of prompt tokens read from the cache", but doesn't document how the reuse works .
   Sources: LCS: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md; OLF: https://docs.ollama.com/faq.md https://docs.ollama.com/api/generate.md; SGA: https://docs.sglang.io/docs/advanced_features/server_arguments.md https://github.com/sgl-project/sglang

B049. (preprint, 2025) audited 17 API providers in autumn 2024 with timing tests and found caching at 8 of them, shared across users at 7 (including OpenAI's and Azure's text-embedding-3-small) and kept per organization at Anthropic and OpenAI's GPT-4o mini .
   Sources: GUA: https://arxiv.org/abs/2502.07776

B050. After they disclosed it, "at least five providers made changes"; only OpenAI's embedding fix is named .
   Sources: GUA: https://arxiv.org/abs/2502.07776

B051. As a side result, the timing told them that OpenAI's embedding model is a decoder-only Transformer .
   Sources: GUA: https://arxiv.org/abs/2502.07776

B052. Today the big vendors' docs state isolation: Anthropic between organizations and per workspace on its own API, OpenAI across organizations .
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

B053. Recomputing shared prefixes wastes compute (P2-05, P2-06) | Confirmed, and now sold as a feature: every major API caches identical prefixes | 3.5
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; GCC: https://ai.google.dev/gemini-api/docs/caching https://ai.google.dev/gemini-api/docs/generate-content/caching; OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

B054. RadixAttention matches prefixes by "depth-first search" (P2-07) | Corrected: prefixes are matched by radix-tree lookup; depth-first order is the paper's scheduling order (ledger P2-07) | 3.7
   Sources: SGL: https://arxiv.org/abs/2312.07104

B055. Anthropic's guidance, SGLang and LangChain are "critical" tools (P2-11) | Overstated. SGLang matters if you run your own server; API users get caching from the provider | 6
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; SGL: https://arxiv.org/abs/2312.07104

B056. SGLang serves "thousands" of requests sharing one system prompt (P2-14) | Overstated: no such figure. The paper reports cache hit rates of 50% to 99% in its benchmarks and 52.4% and 74.1% in a low-traffic Chatbot Arena deployment | 3.7, 5
   Sources: SGL: https://arxiv.org/abs/2312.07104

B057. *Caching in a research agent* .
   Sources: LUM: https://arxiv.org/abs/2601.06007

B058. *A prefix cache in production* .
   Sources: SGL: https://arxiv.org/abs/2312.07104

B059. The model: Claude Sonnet 5.5, $2 per million input tokens, cache reads at 0.05x .
   Sources: APR: https://platform.claude.com/docs/en/about-claude/pricing

B060. Gaps under 4 minutes keep a 5-minute entry alive, because each hit refreshes it ; the 1-hour lifetime isn't needed.
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching

B061. *Step 5, check.* After the second question, `cache_read_input_tokens` should be about 91,500 and `cache_creation_input_tokens` 0 .
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching

B062. Then watch the usage fields: caching that never reads is a surcharge (Section 3.6). - **For production:** explicit breakpoints after the parts that change at different speeds (tools, then system prompt and documents, then history), the 1-hour lifetime when requests come more than 5 minutes apart but at least twice an hour, and an alert when the cache-read share drops .
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching

B063. Fewer than 4 uses an hour, and implicit caching (no storage charge) or no caching is cheaper .
   Sources: GPR: https://ai.google.dev/gemini-api/docs/pricing

B064. (4) A cache hit needs an identical prefix; a changing first line makes every request's prefix new .
   Sources: APC: https://platform.claude.com/docs/en/build-with-claude/prompt-caching

B065. OpenAI's "up to 95%" is a list-price ratio, not a measured saving .
   Sources: OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md

B066. The one independent measurement read found 28% to 81% lower cost, depending on model . - **Implicit caching is best effort.** Gemini's savings "aren't guaranteed" and Bedrock warns that an identical prompt "doesn't guarantee a cache hit" .
   Sources: BRK: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html; GCC: https://ai.google.dev/gemini-api/docs/caching https://ai.google.dev/gemini-api/docs/generate-content/caching; LUM: https://arxiv.org/abs/2601.06007

B067. OpenAI routes by load and prefix hash, and more than about 15 requests per minute on one prefix can spill to other machines . - **An unreplicated oddity.** A single-author 2026 preprint reports that Claude Sonnet 4.6's cache behaves in two tiers around 3,500 tokens, with hit rates levelling off near 0.83 over 30-call sessions .
   Sources: OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md; SON: https://arxiv.org/abs/2607.15516

B068. *Taxonomy flag 4 (§11.6, "typically 0.1×").* Settled: still true for most Claude models; 0.05x on Opus 5.5 and Sonnet 5.5, and 0.025x on Fable 5.1 and Mythos 5.1 . 3.
   Sources: APR: https://platform.claude.com/docs/en/about-claude/pricing

B069. On October 13, 2026, OpenAI's page says "up to 95%", and models from GPT-5.6 on charge 1.25x for cache writes, which earlier ones didn't .
   Sources: OPC: https://developers.openai.com/api/docs/guides/prompt-caching.md; OPP: https://developers.openai.com/api/docs/pricing.md
