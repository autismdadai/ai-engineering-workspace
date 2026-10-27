"""Optional checks against published libraries. Needs the packages in
requirements-crosscheck.txt; prints SKIP for any that aren't installed.

  bm25s (method="lucene"): same formula without the constant (k1 + 1) factor,
     which modern Lucene dropped because it never changes the ranking.
  rank_bm25 BM25Okapi: a different IDF (Robertson's, with negative values
     replaced by epsilon times the mean IDF), so scores differ; we report it.
  ir_measures: nDCG@k, recall@k and reciprocal rank on the same runs.
"""
import sys

from corpus import DOCS, QUERIES, QRELS, CONCEPTS
from retrieval import BM25, ConceptSearch, rrf, tokenize, recall_at_k, ndcg_at_k, mrr

ok = True
ran = 0  # comparisons that actually ran
model = BM25(DOCS, k1=1.2, b=0.75)
ids = list(DOCS)
corpus_tokens = [tokenize(DOCS[d]) for d in ids]

# --- bm25s ---
try:
    import bm25s
    index = bm25s.BM25(k1=1.2, b=0.75, method="lucene")
    index.index(corpus_tokens, show_progress=False)
    worst = 0.0
    for q in QUERIES.values():
        theirs = index.get_scores(tokenize(q))
        for i, d in enumerate(ids):
            ours = model.score(q, d) / (1.2 + 1)
            worst = max(worst, abs(ours - float(theirs[i])))
    passed = worst < 1e-5
    ok &= passed
    ran += 1
    print(f"{'PASS' if passed else 'FAIL'} bm25s {bm25s.__version__} lucene: largest score gap {worst:.2e} over {len(QUERIES)}x{len(ids)} pairs")
except ImportError:
    print("SKIP bm25s not installed")

# --- rank_bm25 (reported, not required to match) ---
try:
    from rank_bm25 import BM25Okapi
    okapi = BM25Okapi(corpus_tokens, k1=1.2, b=0.75)
    same = 0
    for q in QUERIES.values():
        theirs = okapi.get_scores(tokenize(q))
        their_top = [d for _, d in sorted(zip(theirs, ids), key=lambda x: (-x[0], x[1])) if _ > 0][:3]
        our_top = [d for d, _ in model.search(q, 3)]
        same += their_top == our_top
        print(f"INFO rank_bm25 top 3 for {q!r}: {their_top} (ours {our_top})")
    print(f"INFO rank_bm25 agrees on the top 3 for {same} of {len(QUERIES)} queries (different IDF, so not required)")
except ImportError:
    print("SKIP rank_bm25 not installed")

# --- ir_measures ---
try:
    import ir_measures
    from ir_measures import nDCG, R, RR
    dense = ConceptSearch(DOCS, CONCEPTS)
    run, worst = {}, 0.0
    for q, text in QUERIES.items():
        fused = rrf([model.search(text), dense.search(text)])
        # give strictly decreasing scores so ties can't reorder anything
        run[q] = {d: float(len(fused) - i) for i, (d, _) in enumerate(fused)}
    qrels = {q: dict(r) for q, r in QRELS.items()}
    measures = [nDCG @ 3, R @ 3, RR]
    for m in ir_measures.iter_calc(measures, qrels, run):
        ranked = sorted(run[m.query_id], key=lambda d: -run[m.query_id][d])
        name = str(m.measure)
        ours = {"nDCG@3": ndcg_at_k(ranked, QRELS[m.query_id], 3),
                "R@3": recall_at_k(ranked, QRELS[m.query_id], 3),
                "RR": mrr(ranked, QRELS[m.query_id])}[name]
        worst = max(worst, abs(ours - m.value))
    passed = worst < 1e-9
    ok &= passed
    ran += 1
    print(f"{'PASS' if passed else 'FAIL'} ir_measures {ir_measures.__version__}: nDCG@3, R@3, RR largest gap {worst:.2e}")
except ImportError:
    print("SKIP ir_measures not installed")

if ran == 0:
    print("FAIL nothing was checked: install requirements-crosscheck.txt in this environment")
    ok = False
sys.exit(0 if ok else 1)
