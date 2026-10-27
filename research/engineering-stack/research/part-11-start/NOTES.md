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
