"""Re-derive numbers Part 04 quotes, so the arithmetic is tested, not trusted.

Each value is copied from the source named beside it (read October 13, 2026);
the checks test the arithmetic and the comparisons the text makes.
"""
from fractions import Fraction as F

# Liu et al., "Lost in the Middle" (arXiv 2307.03172v3), GPT-3.5-Turbo,
# 20 documents. Table 6 (Appendix G.2): accuracy by gold-document index.
LIU_20DOC = {0: 75.8, 4: 57.2, 9: 53.8, 14: 55.4, 19: 63.2}
LIU_CLOSED_BOOK = 56.1   # Table 1
LIU_ORACLE = 88.3        # Table 1

# NoLiMa (arXiv 2502.05167, ICML 2025), abstract: GPT-4o at 32K.
NOLIMA_GPT4O_BASE, NOLIMA_GPT4O_32K = 99.3, 69.7

# OpenAI GPT-6 Astra model page: context, max input, max output.
ASTRA = {"context": 1_050_000, "input": 922_000, "output": 128_000}

# Anthropic rate-limits page: 2M ITPM limit, 80% cache hit rate.
ITPM, HIT_RATE = 2_000_000, F(8, 10)

# Lumer et al., "Don't Break the Cache" (arXiv 2601.06007v2): cost cut and
# time-to-first-token change, abstract versus Table 1 ranges (percent).
LUMER_ABSTRACT = {"cost": (41, 80), "ttft": (13, 31)}
LUMER_TABLE = {"cost": (28, 81), "ttft": (-8.8, 30.9)}


def liu_checks():
    out = {}
    out["edge_minus_worst_middle"] = round(LIU_20DOC[0] - min(LIU_20DOC[i] for i in (4, 9, 14)), 1)
    # positions counted from 1, as the text does (the table's index + 1)
    out["middle_positions_below_closed_book"] = [i + 1 for i in (4, 9, 14)
                                                 if LIU_20DOC[i] < LIU_CLOSED_BOOK]
    out["best_below_oracle"] = round(LIU_ORACLE - max(LIU_20DOC.values()), 1)
    return out


def nolima_share():
    return round(100 * NOLIMA_GPT4O_32K / NOLIMA_GPT4O_BASE, 1)


def astra_adds_up():
    return ASTRA["input"] + ASTRA["output"] == ASTRA["context"]


def effective_input_per_minute():
    return int(ITPM / (1 - HIT_RATE))


def lumer_table_lows_below_abstract():
    """The abstract's lower ends (41% cost, 13% time) are above the lowest
    results in the paper's own table (28% and -8.8%, a slowdown)."""
    return all(LUMER_TABLE[k][0] < LUMER_ABSTRACT[k][0] for k in LUMER_ABSTRACT)


if __name__ == "__main__":
    print("Liu et al., GPT-3.5-Turbo, 20 documents:", liu_checks())
    print("NoLiMa, GPT-4o at 32K as a share of its base score:", nolima_share(), "%")
    print("GPT-6 Astra input plus output equals the context window:", astra_adds_up())
    print("Anthropic example, input tokens per minute at an 80% hit rate:",
          f"{effective_input_per_minute():,}")
    print("Lumer et al. table's lowest results fall below the abstract's ranges:",
          lumer_table_lows_below_abstract())
