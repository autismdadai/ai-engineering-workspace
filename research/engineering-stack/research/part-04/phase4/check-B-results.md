# Check B results
B001 | supported | Anthropic reads 0.1x; latency benefit generic; OpenAI/Gemini pass savings on
B002 | supported | "Cache hits require 100% identical prompt segments"; invalidation by level
B003 | supported | Anthropic page describes prefix caching
B004 | supported | "up to 4 cache breakpoints"
B005 | supported | write 1.25x/2x, read 0.1x or less
B006 | supported | 5m/1h Anthropic; OpenAI "remains eligible... 30 minutes"
B007 | supported | SGLang abstract: "KV cache reuse"; definition is generic
B008 | supported | GUA abstract: timing variations/global cache sharing
B009 | supported | Context-windows page lists these; "up to 128k"; Haiku 5.5 >100,000 costs more. (Mythos Preview also listed, omitted; fine)
B010 | supported | "-c ... default: 0 = loaded from model"; context-shift "default: disabled"; no oversize-prompt text seen in README grep
B011 | supported | vLLM/SGLang prefix-based reuse
B012 | supported | exact quote present
B013 | supported | "tools, system, then messages"; "invalidate that level and all subsequent levels"
B014 | supported | tools change "invalidates the entire cache"; thinking/effort "always invalidates message blocks" (tool/system also on some models)
B015 | supported | "hash of the initial tokens... including tool definitions"
B016 | supported | all three cells match (Gemini: "enabled by default for all Gemini 2.5 and newer"; "Beta")
B017 | supported | Anthropic list exact; OpenAI "1,024 visible input tokens" (GPT-5.6+ only); Gemini 4,096/2,048 exact; explicit not stated
B018 | supported | Anthropic 1.25x/2x; OpenAI 1.25x for GPT-5.6+, earlier "No additional cache-write charge"; Gemini storage per MTok-hour
B019 | supported | Anthropic/OpenAI exact; Gemini 3.8 Flash .075/.75, 3.1 Pro .2/2, 2.5 Pro .125/1.25 = 0.1x; 2.5 Flash price not read
B020 | supported | all three cells match
B021 | partly supported | Anthropic 20 positions ok; OpenAI "Automatic routing" is not the lookback: page says GPT-5.6+ checks "up to 20 earlier eligible message endings"; Gemini "Automatic" not stated on pages
B022 | supported | field names match; Gemini page says usage_metadata
B023 | supported | Anthropic isolation per org/workspace ok; OpenAI "Caches are not shared across organizations"; Gemini not stated (claim says Not checked)
B024 | supported | "enabled by default"; flash hit $0.003 vs miss $0.15 = 0.02x
B025 | supported | up to 4 for Claude; TTL resets on hit; quote exact "Repeating an identical prompt doesn't guarantee a cache hit" (5 min is "many models", 1h also possible)
B026 | partly supported | Bedrock: "Implicit Prompt Caching is best effort"; Gemini page says "no cost saving guarantee" for implicit, not "best effort"; "everywhere" is broader than sources (DeepSeek also says best-effort)
B027 | supported | exact 2M ITPM/80%/10,000,000 example; "most Claude models"
B028 | supported | exact quote
B029 | supported | 512 min, "processed without caching, and no error is returned"
B030 | supported | exact quote
B031 | partly supported | cited vLLM page doesn't address decode vs prefill; Anthropic says no effect on output generation (not speed)
B032 | supported | quote appears in pricing page
B033 | partly supported | GPT-5.6+ write 1.25x ok; read 0.1x on most but 0.05x on GPT-6.1 Sol
B034 | supported | Sonnet 5.5 $2/MTok, read $0.10 = 0.05x
B035 | supported | prices match ($0.75/.075/.50; $2/.20/4.50; $1.25/.125/4.50); recomputed 0.50/0.675=0.74, 4.5/1.8=2.5, 4.5/1.125=4.0 (<=200k prompt tiers)
B036 | supported | 3.8 Flash and 3.6 Flash: "$1.50 starting January 1, 2027" vs 0.75
B037 | supported | "discounted up to 95%"
B038 | supported | 10,000-token system prompt; "40 independent agent sessions per cache condition"
B039 | partly supported | numbers match (79.3-81.4; 77.8-78.5; 45.9-47.8; 27.8-41.4) but fetch labelled it Table 2 not Table 1
B040 | supported | -8.8% (GPT-4o full) to 30.9%
B041 | supported | abstract "41-80%" and "13-31%"; table has 27.8% cost and -8.8%/-2.9% TTFT
B042 | supported | matches paper recommendations
B043 | supported | hash by block tokens + prefix/parent; "We only cache full blocks"; LRU free queue
B044 | supported | cache_salt text and "As of v0.11, the default hashing algorithm is sha256"
B045 | partly supported | v0.31.0 cache.py: enable_prefix_caching: bool = True (ok); release dated "05 Oct" (year not shown); cited docs page does not mention enable_prefix_caching at all
B046 | partly supported | SGLang parts ok (LRU leaf, 50-99%, up to 6.4x); first sentence "only prompt processing, not new tokens" is not in either cited source
B047 | supported | docs: radix-eviction-policy default "lru"
B048 | supported | v0.5.21 arg_groups/fields/memory.py disable_radix_cache = False (not in server_args.py itself); llama.cpp cache_prompt default true + nondeterministic quote; Ollama 5 min and quote exact; no reuse mechanism documented
B049 | supported | 17 providers, 8 caching, 7 global, Anthropic Haiku & GPT-4o mini per-org; Sept-early Oct 2024
B050 | supported | "at least five providers made changes"; paper says OpenAI patched, generic fix otherwise
B051 | supported | "OpenAI's embedding model is a decoder-only Transformer"
B052 | supported | Anthropic per org/workspace; OpenAI not shared across orgs
B053 | partly supported | "every major API" overbroad: Anthropic needs cache_control; Gemini implicit; OpenAI default. Not an exhaustive source
B054 | supported | paper: DFS order for scheduling (Thm 3.1); prefix matching via radix tree
B055 | couldn't check | original P2-11 text not given; sources are consistent (SGLang is server software)
B056 | supported | no "thousands" in paper; 50-99%; Arena 52.4% and 74.1% with low traffic
B057 | supported | LUM paper is about agent caching
B058 | supported | SGL paper RadixAttention in production (Chatbot Arena)
B059 | supported | $2, 0.05x
B060 | supported | 5-min refreshed on each hit; gap<4 min safely under 5
B061 | couldn't check | 91,500 depends on unseen document setup; field names correct
B062 | supported | field semantic ok; 1h vs 5m arithmetic holds (2.1x vs 2.5x for two requests/hour)
B063 | partly supported | break-even is 4.0 only for 2.5 Pro; 0.74 for 3.8 Flash, 2.5 for 3.1 Pro
B064 | supported | prefix must be identical
B065 | supported | "discounted up to 95%" = 0.05x ratio; list price
B066 | partly supported | 28-81% ok (27.8-81.4); Gemini quote "aren't guaranteed" not on caching pages (they say "no cost saving guarantee"); Bedrock quote exact
B067 | partly supported | 15 rpm overflow routing ok ("load" not seen); Song preprint: single author, 2026, ~3,500 tokens, 0.83 plateau is "below that threshold"
B068 | supported | 0.1x others; 0.05x Opus/Sonnet 5.5; 0.025x Fable/Mythos 5.1
B069 | supported | OpenAI "up to 95%"; GPT-5.6+ writes 1.25x, earlier none
