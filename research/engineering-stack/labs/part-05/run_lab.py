"""Part 05 lab: run every check and print PASS or FAIL for each.
Standard library only. Exit code 0 only if every check passes."""
import math
import sys

from corpus import DOCS, QUERIES, QRELS, CONCEPTS
from retrieval import (BM25, ConceptSearch, rrf, convex, chunk_text, tokenize,
                       recall_at_k, precision_at_k, mrr, ndcg_at_k)

results = []


def check(name, condition, detail=""):
    results.append(bool(condition))
    print(f"{'PASS' if condition else 'FAIL'} {name}{': ' + detail if detail else ''}")


bm25 = BM25(DOCS)
dense = ConceptSearch(DOCS, CONCEPTS)

# 1. BM25 by hand: "dishwasher E42" against d03, from the formula alone.
toks = {d: tokenize(t) for d, t in DOCS.items()}
n, avgdl = len(toks), sum(map(len, toks.values())) / len(toks)
hand = 0.0
for w in ("dishwasher", "e42"):
    df = sum(w in t for t in toks.values())
    idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
    f, dl = toks["d03"].count(w), len(toks["d03"])
    hand += idf * f * 2.2 / (f + 1.2 * (1 - 0.75 + 0.75 * dl / avgdl))
got = bm25.score("dishwasher E42", "d03")
check("1 BM25 score matches the formula by hand", abs(hand - got) < 1e-12, f"{got:.6f} vs {hand:.6f}")

# 2. Keyword search wins on a rare exact term.
top = [d for d, _ in bm25.search(QUERIES["q1"], 1)]
check("2 BM25 puts the E42 document first", top == ["d03"], str(top))

# 3. Vocabulary mismatch: no shared words, so BM25 finds nothing; the stand-in dense search finds d01.
check("3 BM25 finds nothing for 'fix a flat bicycle tyre'", bm25.search(QUERIES["q2"]) == [])
check("3b stand-in dense search puts d01 first", dense.search(QUERIES["q2"], 1)[0][0] == "d01")
check("3c 'squeaky brakes': BM25 finds nothing, dense finds d06",
      bm25.search(QUERIES["q4"]) == [] and [d for d, _ in dense.search(QUERIES["q4"])] == ["d06"])

# 4. RRF arithmetic, k = 60.
fused = dict(rrf([[("a", 9), ("b", 8)], [("b", 0.9), ("c", 0.1)]], k=60))
check("4 RRF scores", abs(fused["b"] - (1 / 62 + 1 / 61)) < 1e-15 and abs(fused["a"] - 1 / 61) < 1e-15,
      f"b={fused['b']:.6f}, a={fused['a']:.6f}")
lone = 1 / 61
wins = [r for r in range(1, 200) if 2 / (60 + r) > lone]
check("4b agreement at rank r in both lists beats a lone first place only while r <= 61",
      max(wins) == 61 and abs((2 / 61) / lone - 2.0) < 1e-12, f"last winning rank {max(wins)}")

# 5. RRF uses ranks only: rescaling one list's scores changes nothing.
q = QUERIES["q3"]
a = rrf([bm25.search(q), dense.search(q)])
b = rrf([[(d, 1000 * s + 7) for d, s in bm25.search(q)], dense.search(q)])
check("4c RRF's default k is 60", rrf([[("a", 1.0)]]) == [("a", 1 / 61)])
# Qdrant's code: 1 / ((position + 1) / weight + k - 1) with 0-based positions, default k = 2.
qdrant = lambda pos, k=2, w=1.0: 1.0 / ((pos + 1) / w + k - 1)
same_as_k1 = all(abs(qdrant(p) - 1 / (1 + (p + 1))) < 1e-15 for p in range(100))
lone_k1, both5_k1 = 1 / (1 + 1), 2 / (1 + 5)
check("4d Qdrant's default (k = 2, 0-based) equals Cormack's formula with k = 1, where a lone first place beats rank 5 in both lists",
      same_as_k1 and lone_k1 > both5_k1, f"{lone_k1:.3f} vs {both5_k1:.3f}")
check("5 RRF ignores score scale", [d for d, _ in a] == [d for d, _ in b])

# 6. Convex combination, alpha = 0.5: min-max scaling by hand for q1.
cc = dict(convex(dense.search(QUERIES["q1"]), bm25.search(QUERIES["q1"]), alpha=0.5))
d_s, b_s = dict(dense.search(QUERIES["q1"])), dict(bm25.search(QUERIES["q1"]))
mm = lambda x, s: (x - min(s.values())) / (max(s.values()) - min(s.values()))
hand_cc = 0.5 * mm(d_s["d03"], d_s) + 0.5 * mm(b_s["d03"], b_s)
check("6 convex combination by hand", abs(cc["d03"] - hand_cc) < 1e-12, f"{cc['d03']:.4f}")
cc8 = dict(convex(dense.search(QUERIES["q1"]), bm25.search(QUERIES["q1"]), alpha=0.8))
hand_cc8 = 0.8 * mm(d_s["d04"], d_s) + 0.2 * mm(b_s["d04"], b_s)
check("6b alpha weights the dense list (alpha = 0.8)", abs(cc8["d04"] - hand_cc8) < 1e-12, f"{cc8['d04']:.4f}")

# 7. Metrics on a fixed ranking with graded labels.
rels = {"y": 1, "x": 2, "z": 1}  # deliberately not sorted
ranked = ["w", "x", "v", "y"]
ndcg_lin = (2 / math.log2(3) + 1 / math.log2(5)) / (2 + 1 / math.log2(3) + 1 / math.log2(4))
check("7 recall@4, precision@4, precision@5, MRR",
      recall_at_k(ranked, rels, 4) == 2 / 3 and precision_at_k(ranked, rels, 4) == 0.5
      and precision_at_k(ranked, rels, 5) == 0.4 and mrr(ranked, rels) == 0.5)
check("7b nDCG@4 (gain = grade)", abs(ndcg_at_k(ranked, rels, 4) - ndcg_lin) < 1e-12, f"{ndcg_lin:.4f}")
binary = {"x": 1, "y": 1, "z": 1}
same = abs(ndcg_at_k(ranked, binary, 4) - ndcg_at_k(ranked, binary, 4, exp_gain=True)) < 1e-12
differ = abs(ndcg_at_k(ranked, rels, 4) - ndcg_at_k(ranked, rels, 4, exp_gain=True)) > 1e-3
check("7c the two nDCG gains agree on yes/no labels and differ on graded ones", same and differ,
      f"graded: {ndcg_at_k(ranked, rels, 4):.4f} vs {ndcg_at_k(ranked, rels, 4, exp_gain=True):.4f}")

# 8. The table the part prints: mean nDCG@3 over the four queries.
def mean_ndcg(fn):
    return sum(ndcg_at_k([d for d, _ in fn(t)], QRELS[q], 3) for q, t in QUERIES.items()) / len(QUERIES)

table = {
    "BM25": mean_ndcg(bm25.search),
    "stand-in dense": mean_ndcg(dense.search),
    "RRF (k=60)": mean_ndcg(lambda t: rrf([bm25.search(t), dense.search(t)])),
    "convex (alpha=0.5)": mean_ndcg(lambda t: convex(dense.search(t), bm25.search(t))),
}
for name, value in table.items():
    print(f"     mean nDCG@3 {name:20} {value:.4f}")
expected = {"BM25": 0.4174, "stand-in dense": 0.8651, "RRF (k=60)": 0.8877, "convex (alpha=0.5)": 0.8877}
check("8 mean nDCG@3 table matches the part", all(abs(table[k] - v) < 5e-5 for k, v in expected.items()))
per_q = {q: ndcg_at_k([d for d, _ in rrf([bm25.search(t), dense.search(t)])], QRELS[q], 3)
         for q, t in QUERIES.items()}
dense_q3 = ndcg_at_k([d for d, _ in dense.search(QUERIES["q3"])], QRELS["q3"], 3)
check("8b fusion can lose on one query: RRF below dense on q3", per_q["q3"] < dense_q3,
      f"{per_q['q3']:.4f} vs {dense_q3:.4f}")

# 9. Chunker: size limit, overlap, nothing lost.
text = open("corpus.py", encoding="utf-8").read()
chunks = chunk_text(text, size=200, overlap=40)
rebuilt = chunks[0] + "".join(c[40:] for c in chunks[1:])
check("9 chunks stay within 200 characters, overlap 40, and rebuild the text",
      max(map(len, chunks)) <= 200 and rebuilt == text and
      all(chunks[i][:40] == chunks[i - 1][-40:] for i in range(1, len(chunks))),
      f"{len(chunks)} chunks, longest {max(map(len, chunks))}")

# 10. Arithmetic behind numbers the part quotes (inputs are the published figures).
paper = {
    "contextual retrieval 5.7 -> 3.7 (relative %)": (round((5.7 - 3.7) / 5.7 * 100, 1), 35.1),
    "contextual retrieval 5.7 -> 2.9 (relative %)": (round((5.7 - 2.9) / 5.7 * 100, 1), 49.1),
    "contextual retrieval 5.7 -> 1.9 (relative %)": (round((5.7 - 1.9) / 5.7 * 100, 1), 66.7),
    "contextual retrieval 5.7 -> 1.9 (points)": (round(5.7 - 1.9, 1), 3.8),
    "BERT rerank vs previous best, eval MRR@10 (relative %)": (round((35.8 - 28.1) / 28.1 * 100, 1), 27.4),
    "BERT rerank vs previous best, eval MRR@10 (points)": (round(35.8 - 28.1, 1), 7.7),
    "ColPali vs best text pipeline, nDCG@5 (points)": (round(81.3 - 67.0, 1), 14.3),
    "HyDE vs Contriever, DL19 nDCG@10 (points)": (round(61.3 - 44.5, 1), 16.8),
    "MiniLM L12 speed as a share of L6": (round(960 / 1800, 3), 0.533),
    "ColBERTv2 vs best single-vector baseline, MRR@10 (points)": (round(39.7 - 38.8, 1), 0.9),
    "worked example RRF scores d03, d04, d09 (4 decimals)": (tuple(round(x, 4) for x in (1/61 + 1/62, 1/61 + 1/63, 1/62 + 1/63)), (0.0325, 0.0323, 0.032)),
    "ColPali indexing speed-up per page (7.22 / 0.39)": (round(7.22 / 0.39, 1), 18.5),
    "HNSW bytes per 384-dim vector, M = 16 (FAISS formula d*4 + M*2*4)": (384 * 4 + 16 * 2 * 4, 1664),
}
bad = [k for k, (got, want) in paper.items() if got != want]
check("10 paper arithmetic", not bad, ", ".join(bad) or f"{len(paper)} figures")

print(f"\n{sum(results)} of {len(results)} checks passed")
sys.exit(0 if all(results) else 1)
