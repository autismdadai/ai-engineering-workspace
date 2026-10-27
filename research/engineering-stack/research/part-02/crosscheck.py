"""Cross-check evalkit's numbers against scikit-learn, statsmodels and SciPy."""
import sys, math, json
sys.path.insert(0, ".")
import numpy as np
import evalkit, run_eval, semantic_entropy, judge_check
from router import route, LABELS
from statsmodels.stats.proportion import proportion_confint
from statsmodels.stats.contingency_tables import mcnemar as sm_mcnemar
from scipy.stats import binom, entropy as sp_entropy
from sklearn.metrics import precision_recall_fscore_support, cohen_kappa_score, roc_auc_score, confusion_matrix
ok = True
def same(name, a, b, tol=1e-9):
    global ok
    good = abs(a - b) <= tol
    ok &= good
    print(f"{'OK ' if good else 'BAD'} {name}: evalkit {a:.10f}  library {b:.10f}")
# Wilson
for k, n in [(48, 60), (46, 60), (12, 15), (15, 15), (0, 10)]:
    lo, hi = evalkit.wilson_interval(k, n)
    slo, shi = proportion_confint(k, n, alpha=0.05, method="wilson")
    same(f"wilson {k}/{n} low", lo, slo); same(f"wilson {k}/{n} high", hi, shi)
# McNemar exact (statsmodels) and mid-p (scipy binom)
for b, c in [(6, 4), (6, 0), (0, 4), (3, 3), (10, 2), (1, 0)]:
    exact, mid = evalkit.mcnemar(b, c)
    sm = sm_mcnemar(np.array([[0, b], [c, 0]]), exact=True).pvalue
    n = b + c; k = min(b, c)
    if b == c:
        mid_ref = 1 - 0.5 * binom.pmf(b, n, 0.5)
    else:
        mid_ref = 2 * (binom.cdf(k, n, 0.5) - 0.5 * binom.pmf(k, n, 0.5))
    same(f"mcnemar exact b={b} c={c}", exact, min(1.0, sm)); same(f"mcnemar mid-p b={b} c={c}", mid, mid_ref)
# per-class and confusion
rows = evalkit.load_jsonl("data/tickets.jsonl")
gold = [r["label"] for r in rows]
for v in ["v1", "v2"]:
    pred = [route(r["text"], v) for r in rows]
    mine = evalkit.per_class(gold, pred, LABELS)
    p, r, f, s = precision_recall_fscore_support(gold, pred, labels=LABELS, zero_division=0)
    for i, lab in enumerate(LABELS):
        same(f"{v} {lab} precision", mine[lab]["precision"], p[i]); same(f"{v} {lab} recall", mine[lab]["recall"], r[i]); same(f"{v} {lab} f1", mine[lab]["f1"], f[i])
    cm = confusion_matrix(gold, pred, labels=LABELS)
    mcm = evalkit.confusion_matrix(gold, pred, LABELS)
    good = all(cm[i][j] == mcm[g][q] for i, g in enumerate(LABELS) for j, q in enumerate(LABELS))
    ok &= good; print(("OK " if good else "BAD") + f" {v} confusion matrix")
# kappa
jr = evalkit.load_jsonl("data/judge_pairs.jsonl")
res = judge_check.analyse(jr)
combined = []
for row in jr:
    ab = judge_check.underlying(row["judge_ab"], "A"); ba = judge_check.underlying(row["judge_ba"], "B")
    combined.append(ab if ab == ba else "tie")
same("kappa judge vs people", res["kappa"], cohen_kappa_score(combined, [r["human"] for r in jr]))
same("kappa small table", evalkit.cohen_kappa(list("AABBA"), list("ABBBA")), cohen_kappa_score(list("AABBA"), list("ABBBA")))
# entropy
for counts in [[6, 3, 1], [5, 4, 1], [4, 3, 2, 1], [9, 1], [8, 2], [10]]:
    same(f"entropy nats {counts}", evalkit.entropy(counts), sp_entropy(counts))
    same(f"entropy bits {counts}", evalkit.entropy(counts, 2), sp_entropy(counts, base=2))
# AUROC
se = semantic_entropy.analyse(evalkit.load_jsonl("data/samples.jsonl"))
wrong = [not r["correct"] for r in se]
same("auroc semantic entropy", evalkit.auroc([r["se_nats"] for r in se], wrong), roc_auc_score(wrong, [r["se_nats"] for r in se]))
same("auroc wording entropy", evalkit.auroc([r["wording_nats"] for r in se], wrong), roc_auc_score(wrong, [r["wording_nats"] for r in se]))
# pass@k against Chen et al.'s numerically stable form
for n, c, k in [(10, 3, 1), (10, 3, 5), (200, 13, 100), (10, 9, 5)]:
    stable = 1.0 if n - c < k else 1.0 - float(np.prod(1.0 - k / np.arange(n - c + 1, n + 1)))
    same(f"pass@k n={n} c={c} k={k}", evalkit.pass_at_k(n, c, k), stable, tol=1e-12)
print("ALL MATCH" if ok else "MISMATCH")
