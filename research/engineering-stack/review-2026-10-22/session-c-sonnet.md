# Session C summary (Sonnet)

**What the document is.** An overview and appendices (dated October 20, 2026) for a 13-part series that turns an AI-written Gemini report on AI engineering into a checked reference. It adds no new research. It sorts 30 topics into seven layers and five concerns, and it uses source tags: [V] verified, [T] tested, [R] reader test, [U] unverified, [I] invented for teaching. Labs use only the Python standard library (3.11 to 3.13). No hosted model was called anywhere, so live structured output, caching, streaming and rate limits come from vendor documentation. The separate-session review of the whole series has not been run.

**Audit of the Gemini report.** Of 137 checkable claims, 50 hold (36.5%), 55 are overstated (40.1%) and 32 are wrong (23.4%). Examples: 144 streaming multiprocessors on the full H100 die versus the claimed 132 (132 are enabled on SXM5); 5.6 kW is the GPUs' ceiling while the whole DGX H100 is rated up to 10.2 kW.

**Context and retrieval.**
- "Lost in the Middle" (GPT-3.5-Turbo, 20 documents, 2023 models): 75.8% accuracy with the answer first, 53.8% at the 10th position, a 22.0-point drop. For later models the effect is weaker and task-dependent.
- NoLiMa (ICML 2025): 11 of 13 models fell below half their short-context score at 32,000 tokens; GPT-4o went from 99.3% to 69.7%.
- Prompt caching (Anthropic list prices, read October 13, 2026; write 1.25x or 2x, read 0.1x): a 5-minute cache pays after one read, a 1-hour cache after two. A preprint on a deep-research agent reported 79 to 81% savings on GPT-5.2 and 28 to 41% on Gemini 2.5 Pro.
- DPR beat BM25 by 9 to 19 percentage points of top-20 accuracy, on the question-answering sets it was trained for. ColBERTv2 led single-vector models by 0.9 to 9.3 MRR@10 points on MS MARCO dev.
- GPT-4 answered 56% correctly from retrieved chunks and 89% with the right evidence (MultiHop-RAG). Retrieval-based legal tools hallucinated about 17% to 33% (202 questions, 2024).
- Prompt per question: about 900 tokens for vector RAG, about 39,000 for GraphRAG local search, about 331,000 for global search (one ICLR study, novels).

**Agents and security.**
- Anthropic's multi-agent research system beat a single agent by 90.2% on its own internal evaluation (June 2025), using about 15 times a chat's tokens versus about 4 times for one agent. This is a vendor report.
- Adaptive attacks beat spotlighting 99% of the time on three of four targets, and 47% on GPT-5 Mini (preprint). Llama Guard 4 had 69% recall and an 11% false-positive rate on Meta's own English set.

**Running and adapting models.**
- Llama 3 8B at Q4_K_M: 4.91 GB, 4.8944 bits per weight, +2.79% perplexity (Wikitext-2, llama.cpp scoreboard).
- Speculative decoding gave 3.55 times at batch size 1 (NVIDIA, one H200) but was 1.4 to 1.8 times slower at high load in a vLLM test.
- A bandwidth-based decode ceiling of 8.5 tokens per second on an office PC was matched by 8.4 and 8.0 measured on a smaller model. A ceiling is never a prediction.
- Retrieval beat fine-tuning on new facts by 19 to 37 percentage points (Ovadia et al., EMNLP 2024). LoRA often trains under 1% of weights.
- Batch APIs cost 50% less with answers within 24 hours (read October 20, 2026).

**Decision guides.** Build the eval first. Put missing or changing facts in retrieval, not training. Use a workflow when the steps are known; one agent is the default. Check local fit and speed, but local is not offline: Ollama calls ollama.com unless told not to.

**What stays unverified.** macOS steps were never run. Several reader tests are open. Network behavior was read from source code. No independent benchmarks exist for vector databases, graph databases or serving engines. Much injection-defense and multi-agent evidence is preprints or vendor reports. Prices, model names and maintenance status go stale fastest.
