# Researcher A: choosing a model (topic T26)

Read /home/claude/part12/research/BRIEF-common.md first; its rules apply. Write to /home/claude/part12/research/choosing/claims.md (IDs C001, C002, ...). Work only in /home/claude/part12/research/choosing/.

Questions, in priority order:
1. **Where model comparisons come from in October 2026, and how far to trust each.** LMArena (formerly Chatbot Arena): method, current state, the "Leaderboard Illusion" critique (Singh et al., 2025) and LMArena's reply; Artificial Analysis: what its index measures and how; LiveBench (designed against contamination); HELM; Hugging Face's Open LLM Leaderboard (retired March 2025: confirm the date from Hugging Face). For each: who runs it, what it measures, its known weaknesses from primary or peer-reviewed sources.
2. **Benchmark contamination and saturation:** one or two peer-reviewed or well-cited studies showing benchmark scores inflated by training-data overlap, with scope.
3. **Current open-weight model families, as their publishers state them (October 2026):** Meta (Muse Glimmer, Muse Spark Open, Llama 4: dates, sizes, licences from the model cards or Meta's own pages), Qwen (Qwen3, Qwen3.5), Google Gemma 4, Microsoft Phi-4, IBM Granite 4, OpenAI gpt-oss, Mistral (which models are Apache-2.0 and which are not), DeepSeek, and any other family the sources show as widely used. For each: newest release, sizes, licence name, context length, and the publisher's own page. Keep it to what the publisher's pages say.
4. **Model cards and what to read in them:** Hugging Face's model card guidance and Mitchell et al., "Model Cards for Model Reporting" (FAT* 2019): what a card should state; which fields matter for choosing (licence, intended use, training data, evaluation scope).
5. **Choosing by your own evaluation:** any vendor or peer-reviewed guidance that says to evaluate candidate models on your own task data (OpenAI's or Anthropic's model-selection docs, for example). Link to Part 02 rather than repeating eval mechanics.
6. **Hosted versus open-weight trade-offs** only where a primary source states them (data handling is Part 10; cost and latency are Part 13): keep this short.

Ledger rows this part settles (already settled in Part 11; confirm or update only): P10-09b ("Llama 3 8B as the local example" is outdated) and B4-10 (GGUF versus AWQ versus GPTQ: a file format against two methods).
