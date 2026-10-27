# Part 11 start (October 15, 2026, evening)

## Freshness re-check (PyPI 2026-10-15; git ls-remote)
- Changed since ledger Section 2/4: sglang 0.5.22 (2026-10-16 UTC) now requires Python >=3.11 (was >=3.10); transformers 5.20.0 (2026-10-15); ollama app tag v0.40.5 (was v0.40.2); llama.cpp b11672 (was b11534), v-tags now to v0.7.0.
- Unchanged: vllm 0.31.0 (v0.32.0rc2 pre-release exists), tensorrt-llm 1.2.1 (v1.4.0rc0 pre-release), llama-cpp-python 0.3.36, ollama client 0.6.3, torch 2.14.1.
- Also read: gguf 0.19.0, bitsandbytes 0.50.2, optimum 2.3.0; auto-gptq 0.7.1 (last 2024-03-01), autoawq 0.2.9 (2025-05-11), exllamav2 0.3.2 (2025-07-14): check maintenance status.
- Full output: pypi-2026-10-15.txt, tags-2026-10-15.txt.

## Lab so far (runmath.py, run_lab.py): 7 of 7 on 3.13.16, 3.12.3, 3.11.17
- Llama 3 8B shapes from meta-llama/llama-models commit 0e0b8c5 (models/sku_list.py; FFN rule in models/llama3/model.py): dim 4096, 32 layers, 32 heads, 8 KV heads, vocab 128256, ffn multiplier 1.3, multiple_of 1024 -> FFN 14336.
- Computed: 8,030,261,248 params; 14.96 GiB at 16 bits, 7.48 at 8, 3.74 at 4; KV 131,072 bytes/token at 16 bits (1 GiB per 8,192 tokens); bandwidth ceiling 208.6 tokens/s on 3.35 TB/s at 16 bits, batch 1; speculative expected tokens 3.3616 at alpha 0.8, gamma 4.
- To do: mutation check; quantization formats' real bits per weight (GGUF Q4_K_M etc., from llama.cpp source) [researcher]; gpt-oss-20b shapes and MXFP4; Leviathan formula source check; CPU reader test steps for Ollama/llama.cpp (1 to 3B model) on the owner's PC.
- Not yet launched: 3 researchers (serving engines; local models and quantization; hardware).

## Freshness re-check, October 16, 2026 (10:21 UTC; PyPI script and git ls-remote; pages via WebFetch)
- PyPI (fresh/pypi-2026-10-16.txt): unchanged since Oct 15 for vllm 0.31.0, sglang 0.5.22 (Python >=3.11), tensorrt-llm 1.2.1 (2026-04-20), llama-cpp-python 0.3.36, ollama 0.6.3, torch 2.14.1, transformers 5.20.0, gguf 0.19.0, bitsandbytes 0.50.2, optimum 2.3.0. New rows read: llmcompressor 0.14.0, gptqmodel 7.6.0 (2026-10-12), huggingface-hub 2.2.0, accelerate 1.15.0, mlx 0.32.4, mlx-lm 0.32.2 (2026-10-16, Python >=3.11), safetensors 0.8.0, openvino 2026.4.1, optimum-intel 2.2.0, onnxruntime-genai 0.18.0, lmdeploy 0.18.0, nvidia-ml-py 13.615.71.
- Tags (fresh/tags-2026-10-16.txt): ollama v0.40.5 (final); llama.cpp b11691 (b11672 last evening), v0.7.0; TensorRT-LLM v1.4.0rc0; vLLM v0.32.0rc2 and v0.31.1rc0; SGLang v0.5.22; mlx-lm v0.32.2; TGI v3.3.7; lmdeploy v0.18.0.
- NVIDIA H100 page: unchanged. FP8 3,958, BF16/FP16 1,979, TF32 989, INT8 3,958 TOPS, all "* With sparsity"; FP64 34, FP64 TC 67, FP32 67; 80 GB; 3.35 TB/s; up to 700 W; NVLink 900 GB/s. Page still sells H100; its FAQ compares with B200 (April 2026 benchmarks); navigation promotes Blackwell, GB200/GB300 NVL72, Vera Rubin.
- NVIDIA newsroom (Oct 13 to 16): no data-center GPU or earnings release; "NVIDIA RTX Spark" launch blog (Oct 15) and Nemotron models. Vera Rubin status unchanged since Aug 26.
- gpt-oss (OpenAI page, Aug 5, 2025): 20b = 21B total, 3.6B active, 24 layers, 32 experts, 4 active, 128k context, runs within 16 GB; 120b = 117B, 5.1B active, 36 layers, 128 experts, 4 active, 80 GB; both natively MXFP4; Apache 2.0. The fetch tool reported text on the page aimed at AI assistants; ignored.
- Hugging Face meta-llama org: Llama 4 labelled "Current"; nothing newer; Meta-Llama-3-8B-Instruct updated Jun 18, 2025.
- Ollama docs: cloud models need an account and send prompts to Ollama ("We do not use them to train models"; FAQ: not stored or logged); OLLAMA_NO_CLOUD=1 turns off cloud models and web search; macOS and Windows "automatically download updates", no off switch documented; default context window 4096 tokens (FAQ).
