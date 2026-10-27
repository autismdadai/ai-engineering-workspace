"""evalkit: small scoring tools for evals, using only Python's standard library.

Part 02 of The AI Engineering Stack. Each function names the source of its
formula. Nothing here calls a model or the network.
"""
import json
import math
from collections import Counter

Z95 = 1.959963984540054  # 97.5th percentile of the normal distribution: 95% two-sided


def load_jsonl(path):
    """Read a file with one JSON object per line."""
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def wilson_interval(successes, n, z=Z95):
    """Wilson score interval for a proportion (NIST/SEMATECH e-Handbook 7.2.4.1)."""
    if n == 0:
        return 0.0, 1.0
    p = successes / n
    denominator = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denominator
    half_width = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return max(0.0, centre - half_width), min(1.0, centre + half_width)


def confusion_matrix(gold, predicted, labels):
    """counts[g][p] = how many items with correct label g got label p."""
    counts = {g: {p: 0 for p in labels} for g in labels}
    for g, p in zip(gold, predicted):
        counts[g][p] += 1
    return counts


def per_class(gold, predicted, labels):
    """Precision, recall, F1 and support per label (scikit-learn's definitions)."""
    rows = {}
    for label in labels:
        tp = sum(1 for g, p in zip(gold, predicted) if g == label and p == label)
        fp = sum(1 for g, p in zip(gold, predicted) if g != label and p == label)
        fn = sum(1 for g, p in zip(gold, predicted) if g == label and p != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        rows[label] = {"precision": precision, "recall": recall, "f1": f1, "support": tp + fn}
    return rows


def _point(k, n):
    """Binomial probability of k successes in n tries with p = 1/2."""
    return math.comb(n, k) / 2 ** n


def mcnemar(b, c):
    """Paired test for two systems scored on the same items.

    b = items only the first system got right, c = items only the second got right.
    Items both got right or both got wrong carry no information about the difference.
    Returns (exact conditional p, mid-p), two-sided, as defined by Fagerland,
    Lydersen and Laake (2013), who recommend the mid-p over the exact test.
    """
    n = b + c
    if n == 0:
        return 1.0, 1.0  # no item separates the systems
    if b == c:
        return 1.0, 1.0 - 0.5 * _point(b, n)
    k = min(b, c)
    one_sided = sum(_point(i, n) for i in range(k + 1))
    return min(1.0, 2 * one_sided), 2 * (one_sided - 0.5 * _point(k, n))


def cohen_kappa(rater_a, rater_b):
    """Agreement beyond chance, (p_o - p_e) / (1 - p_e) (Cohen 1960)."""
    n = len(rater_a)
    p_o = sum(1 for x, y in zip(rater_a, rater_b) if x == y) / n
    count_a, count_b = Counter(rater_a), Counter(rater_b)
    p_e = sum(count_a[k] * count_b[k] for k in count_a) / (n * n)
    if p_e == 1:
        return float("nan")  # both raters used one label throughout: kappa is undefined
    return (p_o - p_e) / (1 - p_e)


def entropy(counts, base=math.e):
    """Shannon entropy of a list of counts: nats with base e, bits with base 2."""
    total = sum(counts)
    shares = [c / total for c in sorted(counts, reverse=True) if c]
    return 0.0 - sum(s * math.log(s, base) for s in shares)


def cluster(answers, same_meaning):
    """Group answers by meaning. Each answer is compared with the first member of
    each existing cluster, as in Farquhar et al. (2024); a new meaning starts a new
    cluster."""
    clusters = []
    for answer in answers:
        for group in clusters:
            if same_meaning(answer, group[0]):
                group.append(answer)
                break
        else:
            clusters.append([answer])
    return clusters


def auroc(scores, is_positive):
    """Chance that a random positive scores higher than a random negative;
    ties count one half (Fawcett 2006)."""
    pos = [s for s, y in zip(scores, is_positive) if y]
    neg = [s for s, y in zip(scores, is_positive) if not y]
    wins = sum(1.0 if p > q else 0.5 if p == q else 0.0 for p in pos for q in neg)
    return wins / (len(pos) * len(neg))


def pass_at_k(n, c, k):
    """Unbiased pass@k from n samples of which c passed (Chen et al. 2021, eq. 1)."""
    if n - c < k:
        return 1.0
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)


def words(text):
    """Lower-case words, with punctuation treated as spaces."""
    return "".join(ch.lower() if ch.isalnum() else " " for ch in text).split()


def overlaps(test_texts, other_texts, threshold=0.8):
    """Pairs (i, j) where test item i and other item j have the same words in the
    same order, or share at least `threshold` of their distinct words (Jaccard)."""
    found = []
    for i, a in enumerate(test_texts):
        wa = set(words(a))
        for j, b in enumerate(other_texts):
            wb = set(words(b))
            same = words(a) == words(b)
            jaccard = len(wa & wb) / len(wa | wb) if wa | wb else 0.0
            if same or jaccard >= threshold:
                found.append((i, j))
    return found
