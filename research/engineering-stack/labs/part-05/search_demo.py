"""Show the top 3 from each method for each query, with nDCG@3.
Standard library only. Usage: python search_demo.py [k]   (k for RRF, default 60)"""
import sys

from corpus import DOCS, QUERIES, QRELS, CONCEPTS
from retrieval import BM25, ConceptSearch, rrf, convex, ndcg_at_k

k = int(sys.argv[1]) if len(sys.argv) > 1 else 60
bm25, dense = BM25(DOCS), ConceptSearch(DOCS, CONCEPTS)
for qid, text in QUERIES.items():
    print(f"{qid} {text!r}  (relevant: {QRELS[qid]})")
    runs = {
        "BM25": bm25.search(text),
        "stand-in dense": dense.search(text),
        f"RRF k={k}": rrf([bm25.search(text), dense.search(text)], k=k),
        "convex a=0.5": convex(dense.search(text), bm25.search(text)),
    }
    for name, ranking in runs.items():
        top = ", ".join(f"{d} {s:.3f}" for d, s in ranking[:3]) or "(nothing)"
        score = ndcg_at_k([d for d, _ in ranking], QRELS[qid], 3)
        print(f"   {name:15} nDCG@3 {score:.3f}   {top}")
