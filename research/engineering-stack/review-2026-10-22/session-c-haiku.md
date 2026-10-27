# Session C summary (Haiku)

**What it is.** An overview, dated October 20, 2026, of a 13-part series. The series checks an AI-written Gemini report on AI engineering and turns it into a teachable reference. It adds no new research. Each figure keeps the tag and scope of the part or ledger that supplies it ([V] verified, [T] tested, [R] reader test, [U] unverified, [I] illustrative). Its 30 topics fall into seven layers and five concerns, and every lab runs on an ordinary computer with no account or API key.

**Main findings**

- **Most of the source report does not hold.** A project audit of 137 checkable claims found 50 hold (36.5%), 55 are overstated (40.1%) and 32 are wrong (23.4%) [T]. These are shares of the 137 claims.
- **Retrieval beats fine-tuning for new facts** by 19 to 37 pp on questions about events after training (Ovadia et al., EMNLP 2024) [V][T].
- **Position effects were measured in 2023 models.** Liu et al.: accuracy was 75.8% with the answer document first and 53.8% at position 10, a 22.0-point drop (GPT-3.5-Turbo, 20 documents) [V][T]. NoLiMa (ICML 2025): 11 of 13 models fell below half their short-context score at 32,000 tokens; GPT-4o fell from 99.3% to 69.7% [V]. For current models, length degradation is the more robust finding.
- **Caching savings depend on the workload.** A 5-minute cache pays back after one read, a 1-hour cache after two [T, arithmetic on vendor prices]. A January 2026 preprint measured 79 to 81% savings on GPT-5.2 and 28 to 41% on Gemini 2.5 Pro, for one deep-research agent with a 10,000-token system prompt [V].
- **Local models are capped by memory bandwidth.** Llama 3 8B at Q4_K_M needs 4.91 GB and loses 2.79% perplexity on Wikitext-2 [V][T]. Its decode ceiling is 8.5 tokens per second on a Core i5-9500T. On the owner's PC, a different model (qwen3:1.7b) measured 8.4 and 8.0 tokens per second under its own ceilings of 30.6 and 15.7 [T]. The 8.5 figure is a ceiling, not a measurement.
- **Speculative decoding results conflict.** NVIDIA measured 3.55 times faster at batch size 1 (Llama 3.3 70B, one H200). The vLLM team measured 1.4 to 1.8 times slower at high load (Llama 3 70B, four H100s, 2024) [V].
- **Guards are imperfect.** Llama Guard 4 had 69% recall and 11% false positives on Meta's own English set [V]. Adaptive attacks beat spotlighting 99% of the time on three of four target models [V, preprint].
- **Extra agents cost tokens.** Anthropic's internal evaluation (June 2025) found a multi-agent system beat a single agent by 90.2%, using about 15 times a chat's tokens against about 4 times for one agent [V, vendor report].

**How it was checked.** A lead session wrote each part. Separate agents, on a different model and without seeing the part, re-checked its claims against the sources. Labs ran by script on a Windows 11 PC on October 12, 19 and 20, 2026. No hosted model was called, so live API behavior rests on vendor documentation [R].

**Open items.** The separate-session review of the whole series has not been run (Appendix L). Reader tests remain open for Parts 01, 02, 04 (full size), 07 and 08. macOS steps have never been run. Network behavior was read from source code, not captured [U].
