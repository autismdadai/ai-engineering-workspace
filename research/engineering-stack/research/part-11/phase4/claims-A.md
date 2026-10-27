# Blind check, list A

Each claim below comes with the keys of the sources it rests on; the source list follows.

A001. Engines such as vLLM and SGLang manage that memory the way an operating system manages pages of RAM .  [sources: SGS, VLL, VSR]
A002. Quantization stores each weight in fewer bits (4 instead of 16, say), so the file shrinks to about a third and speed rises, at a small, measurable cost in quality that differs by model and task .  [sources: KRT, LCP]
A003. Tools such as Ollama and llama.cpp do this on ordinary computers using a file format called GGUF .  [sources: GGS, OLS]
A004. **T25, hardware.** For generating text one token at a time, the speed limit is usually memory bandwidth, how many bytes per second the chip can read, not raw computing power: each new token needs every weight read once .  [sources: NVI, VLL]
A005. Reading the prompt | Prefill | Many tokens at once; limited by compute  [sources: NVI, VLL]
A006. Writing the answer, one token at a time | Decode | Limited by memory bandwidth at small batch sizes  [sources: POP, VLL]
A007. Stored keys and values for every token so far | KV cache | Grows by a fixed amount per token  [sources: VLL]
A008. Several query heads sharing one key and value head | Grouped-query attention (GQA) | Llama 3 8B: 32 query heads, 8 KV heads  [sources: LLM]
A009. Attention that looks back only a fixed number of tokens | Sliding window | gpt-oss: 128 tokens on alternate layers  [sources: GOS]
A010. Bytes per second a chip can read from its memory | Memory bandwidth | H100 SXM: 3.35 TB/s  [sources: NVH]
A011. Operations per byte at which compute and memory limit equally | Ridge point (roofline model)  [sources: RFL]
A012. Storing weights in fewer bits | Quantization | A format (GGUF) is not a method (AWQ, GPTQ)  [sources: AWQ, GGS, GPQ]
A013. The file format llama.cpp and Ollama load | GGUF | Tensors plus metadata, chat template included; version 3  [sources: GGS]
A014. A group of weights sharing one scale | Block | Q4_K: 256 weights in 144 bytes  [sources: LCP]
A015. Average storage per weight, scales included | Bits per weight (bpw) | Q4_K_M on Llama 3 8B: 4.8944  [sources: LCP]
A016. A model where each token uses only some of its parts (experts) | Mixture of experts (MoE) | gpt-oss-20b: 4 of 32 experts per token  [sources: GOS]
A017. Working on many requests in the same step | Continuous batching; iteration-level scheduling | Orca's idea (OSDI 2022)  [sources: ORC]
A018. Storing the KV cache in small fixed blocks | PagedAttention | vLLM  [sources: VLL]
A019. Pausing a request when memory runs out, to redo it later | Preemption | vLLM 0.31.0 recomputes; it no longer swaps  [sources: VSR]
A020. A small model guessing tokens a big one checks | Speculative decoding | Same output distribution  [sources: LEV]
A021. Share of draft guesses accepted | Acceptance rate (alpha)  [sources: LEV]
A022. Time to first token; time per output token; gap between streamed chunks | TTFT; TPOT; ITL | Tools disagree on names (Section 3.6)  [sources: APF, VSR]
A023. Weights pruned to a pattern of zeros the chip can skip | Structured sparsity | Doubles a datasheet's TFLOPS figure  [sources: HGX, NVB]
A024. Usage data an engine sends its maker | Telemetry; usage statistics | On by default in vLLM  [sources: VSR]
A025. The vLLM paper calls decoding "memory-bound, underutilizing the computation power of GPUs"; NVIDIA's inference guide says the same of decode and calls prefill "highly parallelized" .  [sources: NVI, VLL]
A026. With 16-bit Llama 3 8B (16.06 GB) on an H100 SXM (3.35 TB/s) the ceiling is 208.6 tokens per second; with the 4-bit file (4.91 GB) on a Core i5-9500T office PC (41.6 GB/s, Intel's figure), 8.5 .  [sources: ARK, NVH]
A027. **When compute takes over.** Williams, Waterman and Patterson's roofline model says attainable speed is the smaller of peak compute and bandwidth times operational intensity, the operations done per byte read .  [sources: RFL]
A028. Each sequence has its own, so at large batches and long contexts reading it dominates: Pope et al. give 2,048 tokens at batch 512 as an example (preprint, Google, 2022) .  [sources: POP]
A029. The lab counts Llama 3 8B from Meta's own configuration (model width 4,096, 32 layers, 32 query heads, 8 key-value heads, vocabulary 128,256, feed-forward width 14,336) and gets 8,030,261,248 weights: 16.06 GB (14.96 GiB) at 16 bits .  [sources: LLM]
A030. For OPT-13B in 16-bit that is 2 x 5,120 x 40 x 2 = 819,200 bytes, the vLLM paper's "800 KB" per token (§3), so the cache grows in a straight line with length (ledger P2-15) .  [sources: VLL]
A031. The vLLM paper's Figure 1, a 13-billion-parameter model on a 40 GB A100, gives 65% of memory to weights and over 30% to the KV cache: the cache is what limits how many requests fit .  [sources: VLL]
A032. **Two shapes that change the sums.** gpt-oss-20b gives every other layer a 128-token sliding window, so those layers keep at most 128 tokens .  [sources: GOS]
A033. It is also a **mixture of experts**: 20.91 billion weights, of which a token uses 3.61 billion (4 of 32 experts per layer), matching OpenAI's model card .  [sources: GMC]
A034. Its expert matrices are stored in MXFP4 at 4.25 bits and everything else in BF16, so the checkpoint is 12.8 GiB (13.76 GB), while one token reads only about 3.71 GB .  [sources: GOS]
A035. OpenAI says it runs within 16 GB of memory .  [sources: OPN]
A036. **How.** Weights are stored in blocks: a few bits per weight plus a shared scale, so the small numbers can be turned back into approximate real ones. llama.cpp's Q4_K packs 256 weights into 144 bytes, 4.5 bits each including scales (ggml-common.h) .  [sources: LCP]
A037. GGUF is a file format: tensors plus metadata, including the chat template (`tokenizer.chat_template`), now at version 3 .  [sources: GGS]
A038. AWQ (MLSys 2024) and GPTQ (ICLR 2023, published as "OPTQ") are methods for choosing the quantized values .  [sources: AWQ, GPQ]
A039. Q8_0 | 32 | 34 | 8.5  [sources: LCP]
A040. Q6_K | 256 | 210 | 6.5625  [sources: LCP]
A041. Q5_K | 256 | 176 | 5.5  [sources: LCP]
A042. Q4_K, Q4_0 | 256, 32 | 144, 18 | 4.5  [sources: LCP]
A043. NVFP4 | 64 | 36 | 4.5  [sources: LCP]
A044. IQ4_XS, MXFP4 | 256, 32 | 136, 17 | 4.25  [sources: LCP]
A045. Q3_K | 256 | 110 | 3.4375  [sources: LCP]
A046. Q2_K | 256 | 84 | 2.625  [sources: LCP]
A047.   [sources: LCP]
A048. MXFP4 is the Open Compute Project's microscaling format: 32 four-bit floating-point values share one 8-bit power-of-two scale .  [sources: MXS]
A049. **A "4-bit" file isn't all 4-bit.** In llama.cpp's Q4_K_M, the attention value matrix and the feed-forward down matrix get Q6_K on 16 of Llama 3 8B's 32 layers (the first eighth, the last eighth and every third layer between), the output matrix gets Q6_K, and the norms stay 32-bit (src/llama-quant.cpp) .  [sources: LCP]
A050. Applying those rules, the lab reproduces llama.cpp's published table for Llama 3.1 8B, which has the same shapes, to four decimal places :  [sources: LCP]
A051. So the community's "4.92 GB" Llama 3 8B Q4_K_M file (ledger P10-09) is 4.91 GB of tensors plus metadata .  [sources: LCP]
A052. **What it costs.** llama.cpp's own scoreboard (base Llama 3 8B, Wikitext-2, measured by its contributors) :  [sources: LCP]
A053. At Q4_K_M the most likely next token differs from f16's at about 8.1% of positions, and 1% of tokens lose at least 19.6 percentage points of probability on the right answer; Llama 3 8B loses more than Llama 2 7B at the same type .  [sources: LCP]
A054. Benchmarks move less: a single-author 2026 preprint found Llama 3.1 8B Instruct's average over five benchmarks went from 69.47 to 69.15 (-0.32 points) at Q4_K_M .  [sources: KRT]
A055. A peer-reviewed study of the Llama 3.1 family (ACL 2025, over 500,000 evaluations, vLLM on GPUs) found 8-bit floating point "lossless", 8-bit integers 1% to 3% worse and 4-bit weights competitive .  [sources: KUR]
A056. (NeurIPS 2024) warn that averages hide answers that flip from right to wrong , and preprints find that small models and low-resource languages lose most, and that reasoning models lose accuracy below 4 bits .  [sources: DUT, LQR, MAR]
A057. **The KV cache can shrink too.** Ollama's FAQ says a 4-bit KV cache takes about a quarter of the memory of 16-bit with "a small-medium loss in precision" ; vLLM offers 8-bit options .  [sources: OLS, VSR]
A058. **The tools changed.** AutoAWQ is deprecated (adopted by vLLM's llm-compressor), AutoGPTQ is unmaintained (its README points to GPTQModel), ExLlamaV2 is archived in favour of ExLlamaV3, and bitsandbytes 0.50.2 has a CPU backend needing AVX2 .  [sources: QTL]
A059. **Batching by step.** Orca (OSDI 2022) schedules work one model step at a time, so a new request joins the next step instead of waiting for the whole batch to finish; its authors measured 36.9 times FasterTransformer's throughput at the same latency on GPT-3 175B . vLLM calls this continuous batching, TensorRT-LLM in-flight batching, LMDeploy persistent batching .  [sources: LMD, ORC, TRL, VSR]
A060. **Paged KV memory.** Earlier systems reserved each request's KV memory in advance, in one contiguous piece; the worst variant the vLLM paper tested reserved enough for the longest reply the model allows .  [sources: VLL]
A061. The vLLM paper measured only 20.4% to 38.2% of KV memory holding real token data in its own reimplementations of Orca (Figure 2) .  [sources: VLL]
A062. PagedAttention stores the cache in small blocks placed anywhere, like an operating system's memory pages, so waste is limited to the unfilled part of each request's last block (§4.3); the paper says "near-zero waste" with no percentage, and vLLM's launch blog says "under 4%", without a method (ledger P10-03) .  [sources: VBL, VLL]
A063. **What that bought.** 2 to 4 times the throughput at similar latency against FasterTransformer and the authors' Orca reimplementations (OPT and LLaMA models on A100s, 2023), and 2.2 times as many requests at once as Orca (Oracle) on OPT-13B, from memory management, since both batch by step (ledger P10-04) .  [sources: VLL]
A064. The paper preempted requests by swapping their blocks to CPU memory or by recomputing them later (§4.5) . vLLM 0.31.0 only recomputes: the scheduler frees the blocks of the request scheduled last, resets its progress and puts it back in the queue, and its V1 guide lists CPU swapping as removed .  [sources: VLL, VSR]
A065. SGLang "retracts" requests the same way .  [sources: SGS]
A066. **Defaults that set capacity**, read in source. vLLM 0.31.0 takes 92% of GPU memory (`gpu_memory_utilization`), uses 16-token blocks, turns prefix caching and chunked prefill on, and caps concurrent sequences at 256 or 1,024 depending on GPU memory .  [sources: VSR]
A067. SGLang 0.5.22 computes its memory share per GPU, and keeps its prefix cache (RadixAttention) on .  [sources: SGS]
A068. One security default: vLLM's `--api-key` guards only the `/v1`, `/v2` and `/inference` paths, and its docs say "Do not rely on --api-key alone" .  [sources: VSR]
A069. A small draft model guesses gamma (γ) tokens; the big target model checks them all in one pass and keeps the longest accepted run, with a correction rule that leaves the output distribution exactly the target's (Leviathan, Kalman and Matias, ICML 2023) .  [sources: LEV]
A070. Equation (1) gives the tokens produced per target pass, (1 - α^(γ+1)) / (1 - α); Theorem 3.8 gives the expected speed-up, that divided by (γc + 1); Corollary 3.9 says that if α beats c, some γ helps, by at least (1 + α) / (1 + c) ; when α is below c, no γ helps, since each extra guess adds less than it costs .  [sources: LEV]
A071. Leviathan et al.: 2 to 3 times on T5-XXL, batch size 1, one TPU-v4 .  [sources: LEV]
A072. NVIDIA: 3.55 times for Llama 3.3 70B with a Llama 3.2 1B draft on one H200 (FP8, batch size 1, TensorRT-LLM 0.15.0, measured December 11, 2024), but 2.86 times with the same draft and Llama 3.1 70B .  [sources: TR2, TRT]
A073. The vLLM team: up to 1.5 times with a draft model at one request per second, and 1.4 to 1.8 times slower at high load (Llama 3 70B, four H100s, 2024) .  [sources: VBL]
A074. EAGLE-3's authors, in SGLang on an H100: 1.81 times at batch 2, and 1.32 to 1.39 times from batch 24 to 64 (preprint) .  [sources: EG3]
A075. MagicDec found gains that survive large batches when contexts are long, because reading the KV cache then dominates, and slowdowns with short ones (preprint) . vLLM's own docs pitch it "to reduce inter-token latency under medium-to-low QPS" .  [sources: MGD, VSR]
A076. Inter-token latency (ITL): the gap between streamed chunks . vLLM's benchmark docs warn that "metric terminology is not standardized"; NVIDIA's AIPerf calls vLLM's TPOT "ITL" and vLLM's ITL "inter chunk latency" .  [sources: APF, VSR]
A077. They split apart when a chunk carries several tokens, as with speculative decoding: in vLLM's example, a 5-token reply with TTFT 100 ms that ends at 180 ms in chunks of 1, 2 and 2 tokens has TPOT 20 ms but ITL 40 ms; the lab's `stream_metrics` reproduces it .  [sources: VSR]
A078. **Throughput** is tokens or requests per second of benchmark time; AIPerf notes its output throughput includes TTFT, so it isn't comparable to per-user throughput .  [sources: APF]
A079. **The main independent benchmark** is MLPerf Inference: round 6.1, published September 16, 2026, has 492 results from 33 organizations, submitted by vendors and reviewed by other submitters .  [sources: MLP]
A080. Its closed data-center results are dominated by Blackwell (B300 and GB300) and AMD's MI355X; Vera Rubin appears as "preview", and no H100 result was submitted .  [sources: MLP]
A081. vLLM 0.31.0 | Apache-2.0 | Linux on NVIDIA, AMD, Intel GPUs; CPUs from a separate `+cpu` wheel (x86 AVX-512 recommended); Apple through a plugin | Active; the default install pulls 199 packages, 3.93 GB (Linux x86-64, Python 3.13) | Yes, to stats.vllm.ai every 600 s; off with `VLLM_NO_USAGE_STATS=1` or `DO_NOT_TRACK=1`  [sources: LCP, LMD, MLX, OLS, SGS, TGI, TRL, VSR]
A082. SGLang 0.5.22 | Apache-2.0 | Python 3.11 or later, CUDA 13; NVIDIA, AMD, TPU, Intel, Ascend; Xeon CPUs with AMX | Active | None found in its code  [sources: LCP, LMD, MLX, OLS, SGS, TGI, TRL, VSR]
A083. TensorRT-LLM 1.2.1 | Apache-2.0 | Linux on NVIDIA only; PyPI holds a stub that fetches the wheel from NVIDIA's index | Stable from April 2026; release candidates since | Not in 1.2.1; on in 1.3.0rc29 and 1.4.0rc0 (`TRTLLM_NO_USAGE_STATS=1`)  [sources: LCP, LMD, MLX, OLS, SGS, TGI, TRL, VSR]
A084. Text Generation Inference | Apache-2.0 | Docker on NVIDIA, AMD, Gaudi, others | **Maintenance mode** since December 11, 2025; last tag v3.3.7 | Yes when run in a container; `--usage-stats=off`  [sources: LCP, LMD, MLX, OLS, SGS, TGI, TRL, VSR]
A085. LMDeploy 0.18.0 | Apache-2.0 | Linux and Windows on NVIDIA | Active | None found  [sources: LCP, LMD, MLX, OLS, SGS, TGI, TRL, VSR]
A086. MLX-LM 0.32.2 | MIT | Apple silicon | Active; its server is "not recommended for production" | None found  [sources: LCP, LMD, MLX, OLS, SGS, TGI, TRL, VSR]
A087. llama.cpp (b11691) | MIT | CPUs, Apple, NVIDIA, AMD, Intel, Vulkan GPUs | Active; several builds a day | Not searched  [sources: LCP, LMD, MLX, OLS, SGS, TGI, TRL, VSR]
A088. Ollama v0.40.5 | MIT | Windows, macOS, Linux; runs llama.cpp's server inside | Active | No analytics library, but calls to ollama.com (Section 3.8)  [sources: LCP, LMD, MLX, OLS, SGS, TGI, TRL, VSR]
A089. "None found" means a search of the code found no telemetry, not a network audit .  [sources: LCP, LMD, MLX, OLS, SGS, TGI, TRL, VSR]
A090. **Ollama is a manager around llama.cpp.** Version 0.40.5 runs llama.cpp's own server (pinned build b11669) as its engine .  [sources: OLS]
A091. It installs per user on Windows without administrator rights (Windows 10 22H2 or newer, at least 4 GB of disk), as an app on macOS 14 or newer, or on Linux by a script that uses sudo, creates an `ollama` user, installs a system service and can install NVIDIA drivers; read it before running it (Part 01) .  [sources: OLS]
A092. Ollama says "We don't see your prompts or data when you run locally" .  [sources: OLS]
A093. But unless cloud features are off, every Ollama server contacts ollama.com at startup to list cloud models and fetches model recommendations every 4 hours; the Windows and macOS apps check ollama.com/api/update every hour, and the "Auto-download updates" setting (on by default) stops only the download, not the check; models come from registry.ollama.ai . `OLLAMA_NO_CLOUD=1` (or `"disable_ollama_cloud": true` in `~/.ollama/server.json`) stops the cloud and recommendation calls, and the server logs "Ollama cloud disabled: true" .  [sources: OLS]
A094. Cloud models need an account and send prompts to Ollama's servers .  [sources: OLW]
A095. No analytics library turned up in its code .  [sources: OLS]
A096. **Defaults to know.** Ollama sets the context window from GPU memory: 4,096 tokens below 23 GiB (so on a CPU-only PC), 32,768 from 23 GiB, 262,144 from 47 GiB, while its FAQ still says a flat 4,096 ; Part 04 showed it drops old chat turns silently when the window fills.  [sources: OLS]
A097. Models unload after 5 idle minutes, so the next request waits for a reload .  [sources: OLS]
A098. An Intel UHD 630 (8th to 10th generation Core chips) probably won't help: Ollama ignores integrated GPUs unless `OLLAMA_IGPU_ENABLE=1`, and llama.cpp's SYCL backend for Intel GPUs starts at 11th generation ; whether its Vulkan backend helps on a UHD 630 wasn't measured .  [sources: INT, LCP, OLS]
A099. **llama.cpp directly.** Official routes are `winget install llama.cpp`, `brew install llama.cpp`, release zips on GitHub (the Windows CPU x64 build carries several CPU variants and picks one at run time), or a new `llama.app` script that downloads from a Hugging Face bucket into `~/.local/bin` with no checksum step .  [sources: LAP, LCP]
A100. Its server speaks OpenAI's chat and Responses formats, listens on 127.0.0.1, and its default port is now 9931 (the same README's Docker examples still pass 8080); `-hf` downloads a model from Hugging Face, Q4_K_M by default; `llama-bench` measures prompt and generation speed .  [sources: LCP]
A101. **LM Studio** is free for personal and internal business use under a proprietary licence; its policy says it has no telemetry but checks for updates, and on Windows it needs AVX2 .  [sources: LMS]
A102. Qwen3 0.6B, 1.7B, 4B (April 2025) | Apache-2.0 | 0.52, 1.4, 2.5 GB; Qwen's own GGUF of 4B at Q4_K_M: 2.5 GB  [sources: MCD, OLB]
A103. Qwen3.5 0.8B, 2B, 4B (March 2026) | Apache-2.0 on the 0.8B card; check the others | 1.2, 2.7, 3.3 GB and up  [sources: MCD, OLB]
A104. Llama 3.2 1B, 3B | Llama 3.2 Community License (custom) | 1.3, 2.0 GB  [sources: MCD, OLB]
A105. Phi-4-mini 3.8B | MIT | 2.5 GB  [sources: MCD, OLB]
A106. Granite 4 micro (3B) | Apache-2.0 | 2.1 GB  [sources: MCD, OLB]
A107. Gemma 4 E2B, E4B | Apache 2.0 | 4.6 GB and up: tight in 8 GB  [sources: MCD, OLB]
A108. Ollama's library pages don't name the quantization or the licence; take the licence from the publisher .  [sources: MCD, OLB]

## Sources

- APF: NVIDIA AIPerf (ai-dynamo/aiperf at c622220), docs/metrics-reference.md (class OD)
- ARK: Intel, Core i5-9500T specifications page (intel.com, SKU 191052) (class OD)
- AWQ: Lin et al., "AWQ", arXiv 2306.00978; MLSys 2024 per mit-han-lab/llm-awq's README (d6e797a) and a proceedings listing seen in search (class PR)
- DUT: Dutta et al., "Accuracy is Not All You Need", NeurIPS 2024, abstract (class PR)
- EG3: Li et al., "EAGLE-3", arXiv 2503.01840v3, abstract and Table 3 (class PP)
- GGS: GGUF specification, ggml-org/ggml at a05c992, docs/gguf.md; llama.cpp `gguf.h` (class OD)
- GMC: OpenAI, gpt-oss model card, arXiv 2508.10925v1, §2 and Table 1 (class OD)
- GOS: openai/gpt-oss at 5681a6b: README and `gpt_oss/torch/model.py`; the 20b `config.json` on Hugging Face (class OD)
- GPQ: Frantar et al., GPTQ, arXiv 2210.17323; ICLR 2023 poster page, as "OPTQ" (class PR)
- HGX: NVIDIA HGX page (class OD)
- INT: Intel, list of Core desktop processors' graphics (PDF) (class OD)
- KRT: Kurt, arXiv 2601.14277v1 (January 2026), Table 2 (class PP)
- KUR: Kurtic et al., "Give Me BF16 or Give Me Death", ACL 2025, pp. 26872 to 26886, doi:10.18653/v1/2025.acl-long.1304 (class PR)
- LAP: `llama.app/install.sh`, read as text (class OD)
- LCP: ggml-org/llama.cpp at f336359 and tag b11691: `ggml-common.h`, `src/llama-quant.cpp`, `tools/quantize/README.md`, `tools/perplexity/README.md`, server README, `common.h`, SYCL and install docs, release workflow, LICENSE (class OD)
- LEV: Leviathan, Kalman and Matias, "Fast Inference from Transformers via Speculative Decoding", ICML 2023, PMLR 202: Definitions 3.1 and 3.7, Equation (1), Theorem 3.8, Corollary 3.9, §4.1 (class PR)
- LLM: meta-llama/llama-models at 0e0b8c5: `models/sku_list.py`, `models/llama3/model.py`, Llama 3.2 model card and licence (class OD)
- LMD: InternLM/lmdeploy at 110965c (v0.18.0): LICENSE, README, installation docs (class OD)
- LMS: LM Studio app terms (August 23, 2026) and privacy policy; lmstudio-ai/docs at 4f8082f (class OD)
- LQR: Liu et al., "Quantization Hurts Reasoning?", arXiv 2504.04823v2, abstract (class PP)
- MAR: Marie and Fujita, arXiv 2508.20893v1 (class PP)
- MCD: Publishers' pages: QwenLM/Qwen3 README (7a2f61f) and Qwen/Qwen3-4B-GGUF files; QwenLM/Qwen3.5 README and the Qwen3.5-0.8B card; Phi-4-mini-instruct card; IBM Granite 4 README; Gemma 4 model card (class OD)
- MGD: Sadhukhan et al., "MagicDec", arXiv 2408.11049v5, §1 and §3.2 (class PP)
- MLP: mlcommons/inference_results_v6.1 at 4bb63cd (`summary.csv`, supplemental PDF); mlcommons/policies at 45b8b62 (class OD)
- MLX: ml-explore/mlx-lm at 93e6d4a (v0.32.2): LICENSE, README, SERVER.md (class OD)
- MXS: Open Compute Project, Microscaling Formats (MX) Specification v1.0, §5, Table 1 (class SB)
- NVB: NVIDIA Technical Blog, "NVIDIA Hopper Architecture In-Depth" (March 22, 2022; modified July 22, 2025) (class VB)
- NVH: NVIDIA H100 page, specifications table (class OD)
- NVI: NVIDIA Technical Blog, "Mastering LLM Techniques: Inference Optimization" (November 17, 2023) (class VB)
- OLB: Ollama library pages: qwen3, qwen3.5, llama3.2, phi4-mini, granite4, gemma4 (class OD)
- OLS: ollama/ollama at v0.40.5 (d919272): `app/updater/updater.go`, `server/routes.go`, `server/model_recommendations.go`, `envconfig/config.go`, `discover/runner.go`, `scripts/install.sh`, `app/ollama.iss`, `docs/faq.mdx`, `docs/gpu.mdx`, `docs/windows.mdx`, `docs/api.md`, LICENSE (class OD)
- OLW: Ollama docs site, Cloud page (class OD)
- OPN: OpenAI, "Introducing gpt-oss", August 5, 2025 (class VB)
- ORC: Yu et al., "Orca", OSDI 2022, USENIX page and abstract (class PR)
- POP: Pope et al., "Efficiently Scaling Transformer Inference", arXiv 2211.05102v1, §2 and §4.4 (class PP)
- QTL: AutoAWQ README and PyPI page; AutoGPTQ README; exllamav2 and exllamav3 READMEs; PyPI pages of gptqmodel and llmcompressor; bitsandbytes 0.50.2 wheel and README (class OD)
- RFL: Williams, Waterman and Patterson, "Roofline", technical report UCB/EECS-2008-134 (the 2009 CACM version not opened) (class PP)
- SGS: sgl-project/sglang at baa9bef and the 0.5.22 wheel: docs, memory and scheduling defaults, `schedule_batch.py` (class OD)
- TGI: huggingface/text-generation-inference at b4adbf2: README, launcher, `usage_stats.rs` (class OD)
- TR2: NVIDIA Technical Blog, "TensorRT-LLM Speculative Decoding Boosts Inference Throughput by up to 3.6x" (December 2, 2024), Tables 1 and 2 (class VB)
- TRL: NVIDIA/TensorRT-LLM tags v1.2.1, v1.3.0rc29, v1.4.0rc0: docs, `tensorrt_llm/usage/`; PyPI stubs; pypi.nvidia.com (class OD)
- TRT: NVIDIA Technical Blog, "Boost Llama 3.3 70B Inference Throughput 3x with NVIDIA TensorRT-LLM Speculative Decoding" (December 17, 2024), Table 1 (class VB)
- VBL: vLLM blog (vllm-project.github.io at 005f295): June 20, 2023 launch post; October 17, 2024 speculative decoding post (class VB)
- VLL: Kwon et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention", SOSP 2023, doi:10.1145/3600006.3613165, read as arXiv 2309.06180v1: §1, §2.2, §3, §4.1, §4.3, §4.5, §6.1, §6.2, Figures 1 and 2 (class PR)
- VSR: vllm-project/vllm at v0.31.0 (db9527a): `v1/core/sched/scheduler.py`, `usage/usage_lib.py`, `config/cache.py`, `config/scheduler.py`, `engine/arg_utils.py`; docs on speculative decoding, metrics, optimization, the V1 guide, benchmarking, CPU install and the OpenAI-compatible server (class OD)
