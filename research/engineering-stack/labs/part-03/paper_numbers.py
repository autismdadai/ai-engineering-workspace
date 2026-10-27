"""Recompute the published figures Part 03 cites, from the papers' tables.

Inputs are copied from the papers (October 12, 2026 reading):
MIPRO, EMNLP 2024, Table 2 (Llama-3-8B, test column);
GEPA, ICLR 2026 (arXiv 2507.19457v2), Tables 1 and 2.
"""
import json

MIPRO_SCONE = {"baseline": 69.1, "mipro": 79.4}          # exact match, test
GEPA_AGG = {"qwen3_8b": {"mipro_v2": 47.84, "gepa": 54.85},
            "gpt_4_1_mini": {"mipro_v2": 58.67, "gepa": 65.22}}
GRPO_ROLLOUTS = 24_000
GEPA_BUDGETS = [6871, 3593, 7051, 2426, 1839, 1839]      # per benchmark, Table 1


def compute():
    gain = MIPRO_SCONE["mipro"] - MIPRO_SCONE["baseline"]
    ratios = [GRPO_ROLLOUTS / b for b in GEPA_BUDGETS]
    return {
        "mipro_scone_points": round(gain, 1),
        "mipro_scone_relative_pct": round(100 * gain / MIPRO_SCONE["baseline"], 1),
        "gepa_minus_mipro_points": {m: round(v["gepa"] - v["mipro_v2"], 2)
                                    for m, v in GEPA_AGG.items()},
        "grpo_over_gepa_rollouts": [round(min(ratios), 1), round(max(ratios), 1)],
        "ifbench_rollout_ratio": round(GRPO_ROLLOUTS / 678, 1),
    }


if __name__ == "__main__":
    print(json.dumps(compute(), indent=2))
