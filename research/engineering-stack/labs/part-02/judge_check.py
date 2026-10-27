"""Check a model judge before trusting it: position bias and agreement with people.

    python judge_check.py
    python judge_check.py --always-first      a judge that always picks the first answer
    python judge_check.py --pairs other_file.jsonl

data/judge_pairs.jsonl holds 20 recorded comparisons (invented for this lab). For
each pair of answers, A and B, a judge was asked which is better twice: once with
A shown first ("judge_ab") and once with B shown first ("judge_ba"). Each verdict
is "first", "second" or "tie". "human" is the people's verdict (A, B or tie) and
"longer" says which answer is longer. Following Zheng et al. (2023), a win counts
only when the judge prefers the same answer in both orders; otherwise it's a tie.
Exit code 0 means the judge passed this lab's bar; 1 means it didn't.
"""
import argparse
import os
import sys

import evalkit

HERE = os.path.dirname(os.path.abspath(__file__))
PAIRS = os.path.join(HERE, "data", "judge_pairs.jsonl")
MIN_CONSISTENCY = 0.80  # this lab's choice
MIN_KAPPA = 0.60        # McHugh (2012): below 0.60 means inadequate agreement


def underlying(verdict, first_answer):
    """Turn "first"/"second"/"tie" into the answer it points to (A, B or tie)."""
    second_answer = "B" if first_answer == "A" else "A"
    return {"first": first_answer, "second": second_answer, "tie": "tie"}[verdict]


def analyse(rows):
    counts = {"consistent": 0, "biased toward first": 0, "biased toward second": 0, "other": 0}
    combined = []
    for row in rows:
        ab = underlying(row["judge_ab"], "A")  # A was shown first
        ba = underlying(row["judge_ba"], "B")  # B was shown first
        if ab == ba:
            counts["consistent"] += 1
            combined.append(ab)
        else:
            if row["judge_ab"] == row["judge_ba"] == "first":
                counts["biased toward first"] += 1
            elif row["judge_ab"] == row["judge_ba"] == "second":
                counts["biased toward second"] += 1
            else:
                counts["other"] += 1
            combined.append("tie")
    human = [row["human"] for row in rows]
    agree = sum(1 for j, h in zip(combined, human) if j == h)
    longer = [row["longer"] for row in rows]
    judge_decisive = [(j, l) for j, l in zip(combined, longer) if j != "tie"]
    human_decisive = [(h, l) for h, l in zip(human, longer) if h != "tie"]
    return {
        "n": len(rows), "counts": counts, "agree": agree,
        "kappa": evalkit.cohen_kappa(combined, human),
        "judge_longer": (sum(1 for j, l in judge_decisive if j == l), len(judge_decisive)),
        "human_longer": (sum(1 for h, l in human_decisive if h == l), len(human_decisive)),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pairs", default=PAIRS)
    parser.add_argument("--always-first", action="store_true",
                        help="replace every verdict with 'first' (a position-biased judge)")
    args = parser.parse_args(argv)
    rows = evalkit.load_jsonl(args.pairs)
    if args.always_first:
        rows = [dict(row, judge_ab="first", judge_ba="first") for row in rows]
    r = analyse(rows)
    n = r["n"]
    print(f"Judge position check: {n} pairs, each judged in both orders")
    for name, k in r["counts"].items():
        print(f"  {name:<22} {k:>3}  ({100 * k / n:.1f}%)")
    consistency = r["counts"]["consistent"] / n
    print("\nCombined verdicts (a win only if it holds in both orders; otherwise a tie)")
    print(f"  agreement with people: {r['agree']} of {n} ({100 * r['agree'] / n:.1f}%), "
          f"Cohen's kappa {r['kappa']:.3f}")
    (jl, jn), (hl, hn) = r["judge_longer"], r["human_longer"]
    print(f"  chose the longer answer: judge {jl} of {jn} decisive verdicts, "
          f"people {hl} of {hn}")
    problems = []
    if consistency < MIN_CONSISTENCY:
        problems.append(f"consistency {100 * consistency:.1f}% is below {100 * MIN_CONSISTENCY:.0f}%")
    if not r["kappa"] >= MIN_KAPPA:  # also catches an undefined (nan) kappa
        problems.append(f"kappa {r['kappa']:.3f} is below {MIN_KAPPA:.2f}")
    print("\nJUDGE: " + ("PASS" if not problems else "FAIL"))
    for problem in problems:
        print("  - " + problem)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
