"""Arithmetic behind derived figures in the claim ledger. Prints JSON."""
import json, math
out = {}
# RRF, k = 60, two ranked lists (Cormack et al. 2009 formula, ranks from 1)
k = 60
lone_first = 1 / (k + 1)
agree_2_5 = 1 / (k + 2) + 1 / (k + 5)
out["rrf_redis_example"] = {"rank2+rank5": round(agree_2_5, 6), "lone_rank1": round(lone_first, 6),
                            "ratio": round(agree_2_5 / lone_first, 3)}
out["rrf_both_rank_r_vs_lone_first_ratio"] = {r: round((2 / (k + r)) / lone_first, 3) for r in (1, 5, 20, 60, 61, 62)}
out["rrf_crossover_rank"] = max(r for r in range(1, 500) if 2 / (k + r) > lone_first)
out["rrf_k1_lone_first_vs_rank5_both"] = [round(1 / 2, 4), round(2 / 6, 4)]
# Elasticsearch worked example, rank_constant 1: ranks 2 and 1
out["elastic_example"] = round(1 / (1 + 2) + 1 / (1 + 1), 4)
# H100 SXM (NVIDIA product page): sparse FP8 3958 TFLOPS -> dense
out["h100_fp8_dense_tflops"] = 3958 / 2
out["h100_8gpu_tdp_w"] = 8 * 700
out["nvlink_per_direction_GBps"] = 900 / 2
out["nic_per_direction_GBps"] = 400 / 8          # 400 Gb/s ConnectX-7
out["nvlink_vs_one_nic_ratio"] = (900 / 2) / (400 / 8)
out["nvlink_vs_pcie5_x16_ratio"] = 900 / 128
# llama.cpp scoreboard, LLaMA 3 8B, Wikitext-2, f16 vs q4_K_M
ppl_f16, ppl_q4 = 6.233160, 6.407115
out["q4km_ppl_increase_pct"] = round((ppl_q4 / ppl_f16 - 1) * 100, 2)
out["q4km_top_token_changed_pct"] = round(100 - 91.901, 1)
out["q4km_size_vs_f16"] = round(4.58 / 14.97, 3)
# GEPA (arXiv 2507.19457v2 Table 1 aggregates as read by checker)
out["gepa_vs_miprov2_points"] = {"qwen3_8b": round(54.85 - 47.84, 2), "gpt41mini": round(65.22 - 58.67, 2)}
out["gepa_vs_grpo_points_qwen3_8b"] = round(54.85 - 48.91, 2)
out["grpo_rollouts_over_ifbench_gepa"] = round(24000 / 678, 1)
out["grpo_over_gepa_rollout_range"] = [round(24000 / 7051, 1), round(24000 / 1839, 1)]
# MIPRO ScoNe, Llama-3-8B (arXiv 2406.11695 Table 1 as read)
out["mipro_scone_points"] = round(79.4 - 69.1, 1)
out["mipro_scone_relative_pct"] = round((79.4 / 69.1 - 1) * 100, 1)
# Speculative decoding expected tokens per target call (Leviathan et al. Eq. 1)
def expected_tokens(alpha, gamma):
    return (1 - alpha ** (gamma + 1)) / (1 - alpha)
out["spec_expected_tokens"] = {f"a={a},g={g}": round(expected_tokens(a, g), 3)
                               for a in (0.6, 0.8) for g in (3, 5)}
# NVIDIA TRT-LLM spec decoding, Llama 3.3 70B + 3.2 1B draft, H200, batch 1
out["trtllm_1b_draft_speedup"] = round(181.74 / 51.14, 2)
# vLLM: KV cache per token, OPT-13B, FP16 (2 for K and V, 5120 hidden, 40 layers, 2 bytes)
kv_bytes = 2 * 5120 * 40 * 2
out["opt13b_kv_per_token_KB"] = kv_bytes / 1000
out["opt13b_kv_2048_tokens_GB"] = round(kv_bytes * 2048 / 1e9, 2)
# Semantic entropy: toy split of 10 samples into clusters 6/3/1 (discrete variant), natural log and bits
counts = [6, 3, 1]; n = sum(counts)
h_nats = -sum(c / n * math.log(c / n) for c in counts)
out["semantic_entropy_toy_6_3_1"] = {"nats": round(h_nats, 4), "bits": round(h_nats / math.log(2), 4)}
# Prompt caching read cost multiplier example: 0.1x base (Anthropic docs as read)
out["cache_read_saving_pct"] = 90
print(json.dumps(out, indent=1))
