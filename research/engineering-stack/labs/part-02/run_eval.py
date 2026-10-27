"""Score the stand-in ticket router and decide whether a change may ship.

    python run_eval.py                    the version in use (v1), against itself
    python run_eval.py --candidate v2     the change under review
    python run_eval.py --limit 15         only the first 15 tickets

Exit code 0 means the gate passed and 1 means it failed. The gate's rules sit at
the top of this file and were fixed before any results were seen.
"""
import argparse
import os
import sys

import evalkit
from router import LABELS, route

HERE = os.path.dirname(os.path.abspath(__file__))
TICKETS = os.path.join(HERE, "data", "tickets.jsonl")

# The gate. These thresholds are this lab's choices, not a standard.
ACCURACY_FLOOR = 0.60   # the lower end of accuracy's 95% interval must reach 60%
MAX_RECALL_DROP = 0.15  # no label may lose more than 15 points of recall
ALPHA = 0.05            # when a paired test puts the loss's mid-p below 0.05


def pct(x):
    return f"{100 * x:.1f}%"


def check(tickets, baseline="v1", candidate="v1"):
    """Score both versions on the same tickets and apply the gate."""
    gold = [t["label"] for t in tickets]
    pred = {v: [route(t["text"], v) for t in tickets] for v in (baseline, candidate)}
    right = {v: [p == g for p, g in zip(pred[v], gold)] for v in pred}
    n = len(tickets)
    result = {"n": n, "baseline": baseline, "candidate": candidate, "problems": []}
    result["accuracy"] = {v: (sum(right[v]), evalkit.wilson_interval(sum(right[v]), n))
                          for v in pred}
    result["per_class"] = {v: evalkit.per_class(gold, pred[v], LABELS) for v in pred}
    result["confusion"] = evalkit.confusion_matrix(gold, pred[candidate], LABELS)
    b = sum(1 for x, y in zip(right[baseline], right[candidate]) if x and not y)
    c = sum(1 for x, y in zip(right[baseline], right[candidate]) if y and not x)
    result["paired"] = (b, c) + evalkit.mcnemar(b, c)

    low = result["accuracy"][candidate][1][0]
    if low < ACCURACY_FLOOR:
        result["problems"].append(
            f"accuracy: the 95% interval's lower end, {pct(low)}, is below the "
            f"{pct(ACCURACY_FLOOR)} floor ({n} tickets)")
    if b > c and result["paired"][3] < ALPHA:
        result["problems"].append(
            f"overall: {candidate} is worse than {baseline} on the same tickets "
            f"({b} lost, {c} gained; mid-p {result['paired'][3]:.3f})")
    result["recall_change"] = {}
    for label in LABELS:
        idx = [i for i, g in enumerate(gold) if g == label]
        lb = sum(1 for i in idx if right[baseline][i] and not right[candidate][i])
        lc = sum(1 for i in idx if right[candidate][i] and not right[baseline][i])
        before = result["per_class"][baseline][label]["recall"]
        after = result["per_class"][candidate][label]["recall"]
        mid_p = evalkit.mcnemar(lb, lc)[1]
        result["recall_change"][label] = (before, after, mid_p)
        if before - after > MAX_RECALL_DROP and mid_p < ALPHA:
            result["problems"].append(
                f"{label}: recall fell {100 * (before - after):.1f} points "
                f"({pct(before)} to {pct(after)}), paired mid-p {mid_p:.3f}")
    return result


def report(r):
    base, cand = r["baseline"], r["candidate"]
    print(f"Ticket router eval: candidate {cand}, baseline {base}, {r['n']} tickets\n")
    print("Accuracy, with its 95% Wilson interval")
    for v in dict.fromkeys((base, cand)):
        k, (lo, hi) = r["accuracy"][v]
        print(f"  {v}  {k}/{r['n']} = {pct(k / r['n']):>6}   {pct(lo)} to {pct(hi)}")
    print(f"\n{cand} by label    precision  recall      F1  tickets")
    for label, row in r["per_class"][cand].items():
        print(f"  {label:<10} {pct(row['precision']):>11} {pct(row['recall']):>7} "
              f"{pct(row['f1']):>7} {row['support']:>8}")
    print(f"\nConfusion matrix for {cand} (rows: correct label; columns: {cand}'s label)")
    print(" " * 12 + "".join(f"{p:>10}" for p in LABELS))
    for g in LABELS:
        print(f"  {g:<10}" + "".join(f"{r['confusion'][g][p]:>10}" for p in LABELS))
    if base != cand:
        b, c, exact, mid = r["paired"]
        print(f"\nPaired comparison on the same {r['n']} tickets")
        print(f"  only {base} right: {b}   only {cand} right: {c}   "
              f"McNemar mid-p {mid:.3f} (exact test {exact:.3f})")
        print(f"\nRecall by label, {base} to {cand}")
        for label, (before, after, mid_p) in r["recall_change"].items():
            note = f"   paired mid-p {mid_p:.3f}" if before != after else ""
            print(f"  {label:<10} {pct(before):>6} to {pct(after):>6}{note}")
    print("\nGATE: " + ("PASS" if not r["problems"] else "FAIL"))
    for problem in r["problems"]:
        print("  - " + problem)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--baseline", default="v1", choices=["v1", "v2"])
    parser.add_argument("--candidate", default="v1", choices=["v1", "v2"])
    parser.add_argument("--limit", type=int, help="use only the first N tickets")
    parser.add_argument("--tickets", default=TICKETS, help="a JSONL file of tickets")
    args = parser.parse_args(argv)
    tickets = evalkit.load_jsonl(args.tickets)[: args.limit]
    result = check(tickets, args.baseline, args.candidate)
    report(result)
    return 0 if not result["problems"] else 1


if __name__ == "__main__":
    sys.exit(main())
