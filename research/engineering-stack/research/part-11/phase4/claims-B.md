# Blind check, list B

Each claim below comes with the keys of the sources it rests on; the source list follows.

B001. **Sparse or dense?** NVIDIA's H100 page lists 3,958 TFLOPS at FP8 and 1,979 at BF16, both footnoted "With sparsity": they count a pattern of zeroed weights the chip can skip, which a model has to be pruned for .  [sources: NVB, NVH]
B002. NVIDIA's HGX page states the rule, "Dense is ½ sparse", so dense FP8 is 1,979 and dense BF16 989.5 (ledger P4-12); no NVIDIA page read states the H100's dense figures in words .  [sources: HGX]
B003. **Preliminary or shipping?** NVIDIA's 2022 Hopper architecture post still carries its "preliminary" table (3,000 GB/s, FP8 2,000 dense and 4,000 sparse); the shipping H100 SXM has 3.35 TB/s .  [sources: NVB, NVH]
B004. Use that post for design facts: the full GH100 chip has 144 streaming multiprocessors, the H100 SXM5 enables 132 and the PCIe card 114, so "132 SMs on the die" is wrong (ledger P4-04) .  [sources: NVB]
B005. **Do the pages agree?** Not always: NVIDIA's HGX page gives each Rubin GPU 22 TB/s and 3.6 TB/s of NVLink, its Vera Rubin NVL72 page 19.2 TB/s and 3 TB/s .  [sources: HGX, VRP]
B006. Hopper is a generation back but still sold: the H200 has 141 GB of HBM3e at 4.8 TB/s .  [sources: H2P]
B007. NVIDIA says HGX B200 and B300 are "shipping now" (1.4 TB and 2.1 TB of GPU memory per eight GPUs) and the GB300 NVL72 rack (72 GPUs, 20 TB, up to 576 TB/s, so 8 TB/s each) is "Available Now" .  [sources: G3P, HGX]
B008. Vera Rubin is "ramping into full production" (results of August 26, 2026), and its page says "Available Now", yet its MLPerf results a few weeks later were in the "preview" category, for systems not yet available .  [sources: MLP, NQ2, VRP]
B009. AMD's MI355X matches Blackwell Ultra's memory: 288 GB of HBM3E at 8 TB/s, 1,400 W .  [sources: MI3]
B010. Core i5-9500T office PC (dual-channel DDR4-2666) | as fitted (the demo assumes 7.8 GB ) | 41.6 GB/s  [sources: AMR, APL, ARK, CON, NWS]
B011. Apple M5, M5 Pro, M5 Max (MacBook Pro page, October 2026) | up to 128 GB unified (M5 Max) | 153, 307, up to 614 GB/s  [sources: AMR, APL, ARK, CON, NWS]
B012. AMD Ryzen AI Max+ 395 | up to 128 GB LPDDR5x-8000, 256-bit | about 256 GB/s, derived  [sources: AMR, APL, ARK, CON, NWS]
B013. NVIDIA DGX Spark (GB10) | 128 GB unified | 273 GB/s  [sources: AMR, APL, ARK, CON, NWS]
B014. RTX 5060 Ti 16 GB | 16 GB GDDR7 | 448 GB/s  [sources: AMR, APL, ARK, CON, NWS]
B015. RTX 5090 | 32 GB GDDR7 | 1,792 GB/s  [sources: AMR, APL, ARK, CON, NWS]
B016. The i5-9500T has AVX2 but no AVX-512, 6 cores and 6 threads, and Intel lists it as discontinued .  [sources: AMR, APL, ARK, CON]
B017. NVIDIA's newsroom celebrated the launch of "RTX Spark" on October 15, 2026, and its DGX Spark page advertises it for Windows PCs; its specifications weren't read .  [sources: CON, NWS]
B018. NVIDIA's DGX H100 guide lists 8 x 80 GB = 640 GB of GPU memory, never as one pool .  [sources: DGX]
B019. NVLink's 900 GB/s counts both directions: 18 links at 25 GB/s each way, 450 GB/s per direction, about 7 times PCIe Gen5 .  [sources: NVB]
B020. Between servers, eight ConnectX-7 adapters at up to 400 Gb/s carry 50 GB/s each way per GPU, 9 times less again; a GPU's own memory, at 3.35 TB/s, is about 7.4 times faster than NVLink in one direction .  [sources: DGX]
B021. NVIDIA quantifies NVLink's bandwidth but only describes its latency, so "radically reduces latency" has no number behind it (ledger P4-17) .  [sources: NVB]
B022. **Power** (ledger P4-15). 8 x 700 W = 5.6 kW is the GPUs' ceiling; the whole DGX H100 is rated at up to 10.2 kW .  [sources: DGX, NVH]
B023. NVIDIA's Megatron-LM reports 41% to 48% of peak compute used on up to 6,144 H100s, falling from 47% to 42% when one job spreads from 96 to 4,608 GPUs as communication "becomes more exposed" (its own figures) .  [sources: MEG]
B024. Its default recipe depends on the GPU: on Hopper and Ada, "delayed scaling" from a history of past maximums; on Blackwell (compute capability 10.x), MXFP8, E4M3 everywhere with one scale per 32 values; on 12.x, scaling from the current tensor .  [sources: TEN]
B025. CUDA 13.4 Update 2 is current; its cuBLAS adds Rubin (compute capability 10.7), and CUDA 13's libraries dropped Maxwell, Pascal and Volta .  [sources: CUD]
B026. Slurm 26.05.5 (GPL-2.0) schedules jobs on clusters .  [sources: SLM]
B027. Kubernetes reaches GPUs through vendor device plugins (stable since 1.26) and dynamic resource allocation (stable since 1.34) .  [sources: K8S]
B028. NVIDIA's DCGM reports NVLink bytes sent and received and "clocks event reasons", its new name for throttle reasons; the dcgm-exporter for Prometheus leaves the throttling counters off by default .  [sources: DCG]
B029. The KV cache grows linearly with length (P2-15) | Confirmed: a fixed amount per token, 819,200 bytes for OPT-13B in 16-bit, the vLLM paper's "800 KB" | 3.2  [sources: VLL]
B030. AI infrastructure is centred on NVIDIA Hopper (P4-01) | Outdated: Blackwell is shipping, GB300 NVL72 is "Available Now", Vera Rubin is ramping; MLPerf Inference 6.1 had no H100 result | 3.9  [sources: G3P, HGX, MLP, NQ2]
B031. H100 SXM5: 80 GB of HBM3, 3.35 TB/s, 700 W (P4-02, P4-03, P4-13) | Confirmed for the SXM model; NVIDIA's 2022 table (3,000 GB/s) was preliminary; H100 NVL's 94 GB not re-checked | 3.9  [sources: DGX, NVB, NVH]
B032. 132 SMs "on the GH100 die" (P4-04) | Corrected: 144 on the full die, 132 enabled on SXM5, 114 on PCIe | 3.9  [sources: NVB]
B033. Multi-node training is "rarely" compute-bound (P4-05) | Unsupported: NVIDIA reports 41% to 48% of peak compute used on up to 6,144 H100s | 3.10  [sources: MEG]
B034. NVLink and NVSwitch "resolve" the bottleneck; 900 GB/s; eight GPUs as one "unified memory pool" (P4-06 to P4-08) | 900 GB/s confirmed, counting both directions; it helps inside a server, with 9 times less per GPU between servers; memory is 8 x 80 GB, not a pool: overstated | 3.10  [sources: DGX, NVB]
B035. The Transformer Engine runs FP8: E4M3 forward, E5M2 for gradients, with dynamic scaling (P4-09 to P4-11) | Partly supported: that is the HYBRID format, the default on Hopper and Ada with delayed scaling from past maximums; Blackwell's default, MXFP8, uses E4M3 throughout | 3.10  [sources: TEN]
B036. "Nearly 3,958 sparse TFLOPS" (P4-12) | Confirmed as FP8 with sparsity; dense is half, 1,979, by NVIDIA's stated rule | 3.9  [sources: HGX, NVH]
B037. Tools: CUDA, Slurm, Kubernetes, vLLM (P4-14) | Confirmed, current: CUDA 13.4 Update 2, Slurm 26.05.5, Kubernetes device plugins, vLLM 0.31.0 | 3.10  [sources: CUD, K8S, PYPI, SLM]
B038. 8 x H100 draws "upwards of 5.6 kW" (P4-15) | Overstated: 5.6 kW is the GPUs' ceiling; the DGX H100 is rated up to 10.2 kW | 3.10  [sources: DGX, NVH]
B039. nvidia-smi and DCGM monitor NVLink throughput and thermal throttling (P4-16) | Partly supported: DCGM has the fields; its Prometheus exporter leaves throttling off by default; nvidia-smi's field names not checked | 3.10  [sources: DCG]
B040. NVLink "radically" reduces latency versus PCIe Gen5 (P4-17) | Unsupported: NVIDIA quantifies bandwidth (about 7 times), not latency | 3.10  [sources: NVB]
B041. KV fragmentation limits batch size; PagedAttention stores it in blocks (P10-01, P10-02) | Confirmed; the 20.4% to 38.2% was measured against the authors' own Orca reimplementations | 3.4  [sources: VLL]
B042. PagedAttention cuts waste "to near-zero" (P10-03) | Confirmed as the paper's words, with no percentage; "under 4%" is the vLLM blog's, without a method | 3.4  [sources: VBL, VLL]
B043. "Massive" batch increases through continuous batching (P10-04) | Partly supported: step-level batching is Orca's (2022); vLLM's 2 to 4 times came from memory management | 3.4  [sources: ORC, VLL]
B044. Generation is memory-bandwidth bound (P10-05) | Confirmed at small batches; past the ridge point the weights become compute-bound, while each sequence's KV cache stays memory-bound | 3.1  [sources: POP, VLL]
B045. Speculative decoding's notation; output distribution unchanged (P10-06, P10-07) | Confirmed: Definition 3.1, Equation (1), Theorem 3.8 | 3.5  [sources: LEV]
B046. vLLM, TensorRT-LLM, Ollama, llama.cpp (P10-08) | Confirmed, all maintained; TGI, which Gemini didn't name, is in maintenance mode | 3.7  [sources: GHT, PYPI, TGI]
B047. Llama 3 8B Q4_K_M fits a consumer GPU (P10-09) | Confirmed: 4.91 GB of tensors, computed from llama.cpp's rules | 3.3  [sources: LCP]
B048. Llama 3 8B as the local example (P10-09b) | Outdated (settled in Part 10): Llama 4 is Meta's current line; Apache-2.0 and MIT small models exist | 3.8  [sources: HFM, MCD]
B049. vLLM serves hundreds of requests "without running out of KV cache memory" (P10-10) | Overstated: it preempts; 0.31.0 recomputes only | 3.4  [sources: VLL, VSR]
B050. A 1B draft with a 70B target "effectively doubles" speed (P10-11) | Overstated as a rule: 3.55 times at batch size 1 in NVIDIA's test, slowdowns at high load in vLLM's | 3.5  [sources: EG3, TRT, VBL]
B051. Local use "ensures complete data sovereignty, zero cloud telemetry and total air-gapped security" (B4-02) | Overstated: Ollama calls ollama.com at startup and every 4 hours unless cloud is off, and its apps check for updates hourly | 3.8  [sources: OLS]
B052. Local deployment uses containers (B4-03) | Overstated: native installers are the main route | 3.8  [sources: OLS]
B053. llama.cpp and Ollama run models on consumer hardware through GGUF (B4-04) | Confirmed; Ollama runs llama.cpp's server | 3.8  [sources: GGS, OLS]
B054. 16 to 4 bits with "minimal precision loss" (B4-05) | Overstated: +2.79% perplexity and a different top token at 8.1% of positions (Q4_K_M, Llama 3 8B); larger losses for small models and other languages | 3.3  [sources: LCP, MAR]
B055. Runs on Apple Silicon or NVIDIA GPUs (B4-06) | Partly supported: also AMD, Intel, Vulkan and plain CPUs; Ollama needs NVIDIA compute capability 5.0 or later | 3.8  [sources: LCP, OLS]
B056. GGUF versus AWQ versus GPTQ (B4-10) | Corrected: a file format against two methods | 3.3  [sources: AWQ, GGS, GPQ]
B057. *A paper's design isn't today's code* .  [sources: VLL, VSR]
B058. *One name, two numbers* .  [sources: OLS]
B059. *The old flagship left the benchmark* .  [sources: MLP]
B060. Checked October 16, 2026 .  [sources: GHT, PYPI]
B061. The lab's scripts | Memory, file-size, speed and serving arithmetic | This series | Python 3.11 to 3.13, standard library | No | Lab zip  [sources: LCP, LMS, MLX, OLS, QTL, SGS, TRL, VSR]
B062. Ollama | Run local models with one command | MIT | Windows 10 22H2 or later, macOS 14 or later, Linux | Not for local models; cloud models need one | v0.40.5  [sources: LCP, LMS, MLX, OLS, QTL, SGS, TRL, VSR]
B063. llama.cpp | Run and benchmark GGUF models; no background service | MIT | Windows, macOS, Linux; CPU or most GPUs | No; gated Hugging Face models need an account (Part 10) | b11691  [sources: LCP, LMS, MLX, OLS, QTL, SGS, TRL, VSR]
B064. LM Studio | A desktop app for local models | Proprietary, free for personal and internal business use | Windows with AVX2, macOS 14 on Apple silicon | No | Terms of August 23, 2026  [sources: LCP, LMS, MLX, OLS, QTL, SGS, TRL, VSR]
B065. vLLM | Serving many users on GPUs | Apache-2.0 | Linux; NVIDIA, AMD, Intel GPUs | No; usage statistics on by default | 0.31.0  [sources: LCP, LMS, MLX, OLS, QTL, SGS, TRL, VSR]
B066. SGLang | The same, with a radix prefix cache | Apache-2.0 | Linux, Python 3.11 or later, CUDA 13 | No | 0.5.22  [sources: LCP, LMS, MLX, OLS, QTL, SGS, TRL, VSR]
B067. TensorRT-LLM | NVIDIA's engine | Apache-2.0 | Linux on NVIDIA GPUs only | No | 1.2.1 (stable)  [sources: LCP, LMS, MLX, OLS, QTL, SGS, TRL, VSR]
B068. MLX-LM | Local models on Apple silicon | MIT | macOS on Apple silicon | No | 0.32.2  [sources: LCP, LMS, MLX, OLS, QTL, SGS, TRL, VSR]
B069. llm-compressor, GPTQModel | Making AWQ and GPTQ models | Apache-2.0 | GPUs | No | 0.14.0; 7.6.0  [sources: LCP, LMS, MLX, OLS, QTL, SGS, TRL, VSR]
B070. Sources: Sections 3.3, 3.7 and 3.8 .  [sources: LCP, LMS, MLX, OLS, QTL, SGS, TRL, VSR]
B071. With Ollama, set `OLLAMA_NO_CLOUD=1` unless you want its cloud models .  [sources: LCP, MCD, OLS]
B072. Don't start new work on TGI, which is in maintenance mode .  [sources: SGS, TGI, TRL, VSR]
B073. - **On a Mac:** Ollama or llama.cpp (Metal), or MLX-LM; MLX-LM's own docs warn against its server in production .  [sources: LCP, MLX]
B074. - **No single best engine.** No independent comparison of engines on the same hardware was read; MLPerf compares whole systems their makers submit .  [sources: MLP]
B075. It installs in your home folder without administrator rights and needs at least 4 GB of disk .  [sources: OLS]
B076. To keep it local, quit Ollama from the taskbar, open *Edit environment variables for your account*, add `OLLAMA_NO_CLOUD` with the value `1`, and start Ollama again from the Start menu, the route Ollama's FAQ gives for its settings .  [sources: OLS]
B077. If you want to choose when it updates, turn off *Auto-download updates* in its settings; it will still check hourly .  [sources: OLS]
B078. In PowerShell: `ollama pull qwen3:1.7b` (1.4 GB; Apache-2.0) .  [sources: MCD, OLB]
B079. It prints prompt (`pp512`) and generation (`tg128`) speeds; the generation speed should stay below 41.6 / 2.5 = 16.6 tokens per second .  [sources: LCP, MCD]
B080. **To uninstall Ollama:** *Add or remove programs* in Windows Settings; its uninstaller removes models kept in the default place .  [sources: OLS]
B081. **Data:** the published configurations of Llama 3 8B and gpt-oss-20b, and the published figures named in each check ; the PC's free memory and the lab's 10% margin are invented .  [sources: GOS, LCP, LLM]
B082. - *"More TFLOPS means faster chat."* One conversation at a time is limited by bandwidth; compute matters for prompts and for big batches .  [sources: NVI, VLL]
B083. - *"Quantization is free."* +2.79% perplexity on Llama 3 8B at Q4_K_M, and averages hide flipped answers .  [sources: DUT, LCP]
B084. - *"Running locally means nothing leaves my computer."* Ollama calls ollama.com unless told not to .  [sources: OLS]
B085. *Answers.* (1) Each new token reads every weight once while doing little arithmetic per byte, so bytes per second sets the pace .  [sources: VLL]
B086. (3) GGUF .  [sources: GGS]
B087. (4) It preempts the request scheduled last and recomputes it later; swapping to CPU was removed .  [sources: VSR]
B088. (5) Which precision, and with or without sparsity; also whether the table is preliminary .  [sources: HGX, NVB, NVH]
B089. **Best next resources** (checked to exist on October 16, 2026): the vLLM paper ; Leviathan et al. ; llama.cpp's quantize and perplexity READMEs ; Ollama's FAQ ; Williams, Waterman and Patterson's roofline report .  [sources: LCP, LEV, OLS, RFL, VLL]
B090. - **Speed claims come from interested parties.** NVIDIA's 3.55 times, the vLLM team's figures, EAGLE-3's and MagicDec's are measurements by vendors or method authors; LMDeploy's README claims "up to 1.8x higher request throughput than vLLM" with no scope at all .  [sources: EG3, LMD, MGD, TRT, VBL]
B091. MLPerf is the independent benchmark, and its results are still submitted by vendors .  [sources: MLP]
B092. - **Quality evidence is uneven.** llama.cpp's scoreboard is its contributors' own, its README warns that perplexity isn't comparable between models or projects, and most of the newer studies are preprints; the one large peer-reviewed study tested GPU formats in vLLM, not GGUF .  [sources: KUR, LCP]
B093. - **Makers' pages disagree and move.** NVIDIA's own pages give two different per-GPU bandwidths for Rubin, Vera Rubin is "Available Now" on one page and "preview" in MLPerf, and the RTX Spark platform's specifications weren't read .  [sources: HGX, MLP, VRP]
B094. - **The lab is a teaching tool.** Its Q4_K_M rule covers dense Llama-style models only (llama.cpp has extra rules for mixture-of-experts and Falcon models), its KV sizes are what the model needs rather than what an engine allocates, and its 10% memory margin is invented .  [sources: LCP]
B095. A model that doesn't fit: below about 4 bits the scoreboard's losses grow fast (Q3_K_M +10.5%, Q2_K +56% perplexity) ; whether a smaller model at more bits would do better depends on the model and task, and wasn't measured here .  [sources: LCP]
B096. That is the 2023 paper; vLLM 0.31.0 removed swapping .  [sources: VSR]
B097. *Claim ledger P10-04's* 2 to 4 times should be scoped to FasterTransformer and the authors' own Orca reimplementations, and its verdict could read "partly supported", as Section 4 does .  [sources: VLL]
B098. *Claim ledger P4-09* calls the Transformer Engine's scaling "dynamic"; its Hopper default is delayed scaling, and Blackwell's default recipe uses E4M3 throughout .  [sources: TEN]
B099. *Claim ledger P10-11's* "draft length 10" appears only in NVIDIA's build commands, not in the measured table's settings .  [sources: TRT]

## Sources

- AMR: AMD, Ryzen AI Max+ 395 product page, Specifications (class OD)
- APL: Apple, MacBook Pro technical specifications page (class OD)
- ARK: Intel, Core i5-9500T specifications page (intel.com, SKU 191052) (class OD)
- AWQ: Lin et al., "AWQ", arXiv 2306.00978; MLSys 2024 per mit-han-lab/llm-awq's README (d6e797a) and a proceedings listing seen in search (class PR)
- CON: NVIDIA GeForce RTX 50 series comparison page; NVIDIA DGX Spark page (and its RTX Spark banner) (class OD)
- CUD: NVIDIA, CUDA Toolkit 13.4 Update 2 release notes (class OD)
- DCG: NVIDIA DCGM v4.6.1 `dcgm_fields.h`; dcgm-exporter 4.8.4 `default-counters.csv`; nvidia-ml-py 13.615.71 (class OD)
- DGX: NVIDIA, DGX H100/H200 User Guide, "Introduction" (updated January 26, 2026) (class OD)
- DUT: Dutta et al., "Accuracy is Not All You Need", NeurIPS 2024, abstract (class PR)
- EG3: Li et al., "EAGLE-3", arXiv 2503.01840v3, abstract and Table 3 (class PP)
- G3P: NVIDIA GB300 NVL72 page (class OD)
- GGS: GGUF specification, ggml-org/ggml at a05c992, docs/gguf.md; llama.cpp `gguf.h` (class OD)
- GHT: Release tags read with `git ls-remote` (Ollama, llama.cpp, vLLM, SGLang, TensorRT-LLM, TGI, LMDeploy, MLX-LM) (class OD)
- GOS: openai/gpt-oss at 5681a6b: README and `gpt_oss/torch/model.py`; the 20b `config.json` on Hugging Face (class OD)
- GPQ: Frantar et al., GPTQ, arXiv 2210.17323; ICLR 2023 poster page, as "OPTQ" (class PR)
- H2P: NVIDIA H200 page (class OD)
- HFM: Hugging Face, meta-llama organization page (class OD)
- HGX: NVIDIA HGX page (class OD)
- K8S: kubernetes/website at 109572a (GPU scheduling; dynamic resource allocation); NVIDIA k8s-device-plugin and GPU Operator (class OD)
- KUR: Kurtic et al., "Give Me BF16 or Give Me Death", ACL 2025, pp. 26872 to 26886, doi:10.18653/v1/2025.acl-long.1304 (class PR)
- LCP: ggml-org/llama.cpp at f336359 and tag b11691: `ggml-common.h`, `src/llama-quant.cpp`, `tools/quantize/README.md`, `tools/perplexity/README.md`, server README, `common.h`, SYCL and install docs, release workflow, LICENSE (class OD)
- LEV: Leviathan, Kalman and Matias, "Fast Inference from Transformers via Speculative Decoding", ICML 2023, PMLR 202: Definitions 3.1 and 3.7, Equation (1), Theorem 3.8, Corollary 3.9, §4.1 (class PR)
- LLM: meta-llama/llama-models at 0e0b8c5: `models/sku_list.py`, `models/llama3/model.py`, Llama 3.2 model card and licence (class OD)
- LMD: InternLM/lmdeploy at 110965c (v0.18.0): LICENSE, README, installation docs (class OD)
- LMS: LM Studio app terms (August 23, 2026) and privacy policy; lmstudio-ai/docs at 4f8082f (class OD)
- MAR: Marie and Fujita, arXiv 2508.20893v1 (class PP)
- MCD: Publishers' pages: QwenLM/Qwen3 README (7a2f61f) and Qwen/Qwen3-4B-GGUF files; QwenLM/Qwen3.5 README and the Qwen3.5-0.8B card; Phi-4-mini-instruct card; IBM Granite 4 README; Gemma 4 model card (class OD)
- MEG: NVIDIA/Megatron-LM at 3888b34, README, "Performance Benchmarking" (class OD)
- MGD: Sadhukhan et al., "MagicDec", arXiv 2408.11049v5, §1 and §3.2 (class PP)
- MI3: AMD Instinct MI355X and MI300X product pages (class OD)
- MLP: mlcommons/inference_results_v6.1 at 4bb63cd (`summary.csv`, supplemental PDF); mlcommons/policies at 45b8b62 (class OD)
- MLX: ml-explore/mlx-lm at 93e6d4a (v0.32.2): LICENSE, README, SERVER.md (class OD)
- NQ2: NVIDIA, "NVIDIA Announces Financial Results for Second Quarter Fiscal 2027", August 26, 2026 (class OD)
- NVB: NVIDIA Technical Blog, "NVIDIA Hopper Architecture In-Depth" (March 22, 2022; modified July 22, 2025) (class VB)
- NVH: NVIDIA H100 page, specifications table (class OD)
- NVI: NVIDIA Technical Blog, "Mastering LLM Techniques: Inference Optimization" (November 17, 2023) (class VB)
- NWS: NVIDIA newsroom headlines, October 13 to 16, 2026 (class OD)
- OLB: Ollama library pages: qwen3, qwen3.5, llama3.2, phi4-mini, granite4, gemma4 (class OD)
- OLS: ollama/ollama at v0.40.5 (d919272): `app/updater/updater.go`, `server/routes.go`, `server/model_recommendations.go`, `envconfig/config.go`, `discover/runner.go`, `scripts/install.sh`, `app/ollama.iss`, `docs/faq.mdx`, `docs/gpu.mdx`, `docs/windows.mdx`, `docs/api.md`, LICENSE (class OD)
- ORC: Yu et al., "Orca", OSDI 2022, USENIX page and abstract (class PR)
- POP: Pope et al., "Efficiently Scaling Transformer Inference", arXiv 2211.05102v1, §2 and §4.4 (class PP)
- PYPI: PyPI JSON API, read October 16, 2026 (class OD)
- QTL: AutoAWQ README and PyPI page; AutoGPTQ README; exllamav2 and exllamav3 READMEs; PyPI pages of gptqmodel and llmcompressor; bitsandbytes 0.50.2 wheel and README (class OD)
- RFL: Williams, Waterman and Patterson, "Roofline", technical report UCB/EECS-2008-134 (the 2009 CACM version not opened) (class PP)
- SGS: sgl-project/sglang at baa9bef and the 0.5.22 wheel: docs, memory and scheduling defaults, `schedule_batch.py` (class OD)
- SLM: SchedMD/slurm at ad46cad: META, COPYING (class OD)
- TEN: NVIDIA/TransformerEngine at 33f3b35: `common/recipe/__init__.py`, `pytorch/quantization.py`, FP8 primer (class OD)
- TGI: huggingface/text-generation-inference at b4adbf2: README, launcher, `usage_stats.rs` (class OD)
- TRL: NVIDIA/TensorRT-LLM tags v1.2.1, v1.3.0rc29, v1.4.0rc0: docs, `tensorrt_llm/usage/`; PyPI stubs; pypi.nvidia.com (class OD)
- TRT: NVIDIA Technical Blog, "Boost Llama 3.3 70B Inference Throughput 3x with NVIDIA TensorRT-LLM Speculative Decoding" (December 17, 2024), Table 1 (class VB)
- VBL: vLLM blog (vllm-project.github.io at 005f295): June 20, 2023 launch post; October 17, 2024 speculative decoding post (class VB)
- VLL: Kwon et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention", SOSP 2023, doi:10.1145/3600006.3613165, read as arXiv 2309.06180v1: §1, §2.2, §3, §4.1, §4.3, §4.5, §6.1, §6.2, Figures 1 and 2 (class PR)
- VRP: NVIDIA Vera Rubin NVL72 page (class OD)
- VSR: vllm-project/vllm at v0.31.0 (db9527a): `v1/core/sched/scheduler.py`, `usage/usage_lib.py`, `config/cache.py`, `config/scheduler.py`, `engine/arg_utils.py`; docs on speculative decoding, metrics, optimization, the V1 guide, benchmarking, CPU install and the OpenAI-compatible server (class OD)
