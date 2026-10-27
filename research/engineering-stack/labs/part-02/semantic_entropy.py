"""Semantic entropy on recorded samples: a toy version of Farquhar et al. (2024).

    python semantic_entropy.py

data/samples.jsonl holds, for each question, ten answers "sampled from a model"
and the correct answer. All of it is invented for this lab. The script groups the
answers by meaning, takes the entropy over the groups, and flags questions whose
entropy is high. A real system decides "same meaning" with an entailment model
(answer a implies b, and b implies a). This toy uses a small table of equivalent
phrasings instead, so it runs anywhere with no model.
"""
import os
import sys
from collections import Counter

import evalkit

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLES = os.path.join(HERE, "data", "samples.jsonl")
FLAG_ABOVE = 0.6  # nats; this lab's choice of threshold

# The stand-in for an entailment model: phrasings that mean the same thing.
EQUIVALENT = {
    "fourteen days": "14 days", "two weeks": "14 days", "the trial lasts 14 days": "14 days",
    "a pdf file": "pdf", "25 megabytes": "25 mb", "five": "5", "three": "3",
    "ten": "10", "10 people": "10", "control n": "ctrl n",
}


def meaning(answer):
    text = " ".join(evalkit.words(answer))
    return EQUIVALENT.get(text, text)


def same_meaning(a, b):
    return meaning(a) == meaning(b)


def analyse(rows):
    results = []
    for row in rows:
        clusters = evalkit.cluster(row["samples"], same_meaning)
        sizes = sorted((len(c) for c in clusters), reverse=True)
        majority = max(clusters, key=len)[0]
        wordings = Counter(" ".join(evalkit.words(s)) for s in row["samples"])
        results.append({
            "id": row["id"], "sizes": sizes, "answer": majority,
            "se_nats": evalkit.entropy(sizes), "se_bits": evalkit.entropy(sizes, 2),
            "wording_nats": evalkit.entropy(list(wordings.values())),
            "correct": same_meaning(majority, row["reference"]),
        })
    return results


def main():
    results = analyse(evalkit.load_jsonl(SAMPLES))
    print("Semantic entropy over 10 sampled answers per question")
    print("(discrete version: each meaning's share of the samples)\n")
    print("id  meanings (sizes)   SE nats  SE bits  wording H  majority answer   right?  flagged?")
    for r in results:
        sizes = f"{len(r['sizes'])} ({'/'.join(map(str, r['sizes']))})"
        flagged = r["se_nats"] > FLAG_ABOVE
        print(f"{r['id']:<3} {sizes:<18} {r['se_nats']:>7.3f} {r['se_bits']:>8.3f} "
              f"{r['wording_nats']:>10.3f}  {r['answer']:<16}  {'yes' if r['correct'] else 'NO':<6}  "
              f"{'yes' if flagged else 'no'}")
    flagged = [r["id"] for r in results if r["se_nats"] > FLAG_ABOVE]
    missed = [r["id"] for r in results if not r["correct"] and r["se_nats"] <= FLAG_ABOVE]
    wrong = [not r["correct"] for r in results]
    se_auc = evalkit.auroc([r["se_nats"] for r in results], wrong)
    word_auc = evalkit.auroc([r["wording_nats"] for r in results], wrong)
    print(f"\nFlagged (semantic entropy above {FLAG_ABOVE} nats): {', '.join(flagged) or 'none'}")
    print(f"Wrong but not flagged: {', '.join(missed) or 'none'}")
    print(f"AUROC for spotting wrong answers: semantic entropy {se_auc:.4f}, "
          f"entropy of the wording {word_auc:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
