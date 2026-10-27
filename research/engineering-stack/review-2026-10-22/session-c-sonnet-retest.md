# Session C summary (Sonnet, re-test)

**What it is.** An overview and appendices (dated October 20, 2026) for a 13-part series that turns an AI-written Gemini report on AI engineering into a checked, teachable reference. It adds no new research; it gathers figures, tools, decision guides and corrections from the parts. Every lab runs on an ordinary computer with no account or API key, and no hosted model was called anywhere. The separate-session review of the whole series has not yet been run.

**Audit of the Gemini report.** Of 137 checkable claims, 50 hold (36.5%), 55 are overstated (40.1%) and 32 are wrong (23.4%) (the project's claim ledger, after Phase 5). Twenty-one corrections to project documents were applied on October 20, 2026.

**Key figures, with scope.**

*Context and caching*
- Answer document first: 75.8% accuracy; at the 10th position: 53.8%, a 22.0-point drop (GPT-3.5-Turbo, 20 documents, 2023 models). For later models, length degradation is the robust finding and position matters less.
- 11 of 13 models fell below half their short-context score at 32,000 tokens; GPT-4o went from 99.3% to 69.7% (NoLiMa).
- Caching cut cost 79 to 81% on GPT-5.2 and 28 to 41% on Gemini 2.5 Pro (one deep-research agent study, January 2026 prices). A 5-minute Anthropic cache pays after one read, a 1-hour cache after two (list prices read October 13, 2026).
- Over 272,000 input tokens, OpenAI's GPT-6 models bill the whole request at 2x input and 1.5x output.

*Retrieval*
- Dense retrieval (DPR) beat BM25 by 9 to 19 percentage points of top-20 accuracy, on the sets DPR was trained for.
- GPT-4 answered 56% correctly from retrieved chunks and 89% given the right evidence (MultiHop-RAG).
- Legal research tools built on retrieval hallucinated about 17% (Lexis+ AI) to about 33% (Westlaw) of the time (202 questions, 2024).
- Retrieval beat fine-tuning on new facts by 19 to 37 points (Ovadia et al., EMNLP 2024).
- Prompt size per question: about 900 tokens for vector RAG, 39,000 for GraphRAG local search, 331,000 for global (one study, novels).

*Agents and security*
- A multi-agent research system beat a single agent by 90.2% using about 15 times a chat's tokens (about 4 times for one agent); Anthropic's own evaluation, June 2025, a vendor report.
- Users approve 93% of Claude Code permission prompts (data source not stated).
- Adaptive attacks beat spotlighting 99% of the time on three of four targets, 47% on GPT-5 Mini (preprint).
- Llama Guard 4: recall 69%, false positives 11% (Meta's in-house English set). Prompt Guard 2 (86M): recall 97.5% at 1% false positives.

*Running models*
- Q4_K_M for Llama 3 8B: 4.91 GB, +2.79% perplexity (llama.cpp's scoreboard, Wikitext-2).
- Speculative decoding: 3.55 times at batch size 1 (NVIDIA, one H200), but 1.4 to 1.8 times slower at high load (vLLM team).
- Paging raised throughput 2 to 4 times, since only 20.4% to 38.2% of KV memory held real data (vLLM paper).
- The 8.5 tokens per second decode ceiling for Llama 3 8B on an office PC is worked out, not measured. The 8.4 and 8.0 measured were a different, smaller model and do not test it.

*Other*
- `temperature: 0` returns a 400 error on Claude's 5.x-era models (checked October 12, 2026).
- A toy prompt search scoring 1.0 on 5 tickets fell to 0.417 on new ones (invented data).
- Batch APIs cost 50% less, with answers within 24 hours.

**Decision rules.** Build the eval first, then try prompting. Put missing facts in retrieval, and fine-tune for formats and habits. Use one agent by default, with caps in code. For local versus cloud, check fit, speed ceiling, traffic, data and licence. OpenAI closed hosted fine-tuning to new organizations on May 7, 2026, and to all new jobs from January 6, 2027.

**Limits the document states.** macOS steps were never run. No independent benchmarks exist for vector databases, graph databases or serving engines. Much of the injection-defence and multi-agent evidence is preprints or vendor reports. Network behaviour was read in source code, not captured. Prices and versions go stale fastest; check the freshness ledger.
