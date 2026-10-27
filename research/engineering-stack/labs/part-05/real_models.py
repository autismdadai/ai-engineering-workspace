"""Reader test R1 (needs internet once to download two small models of 22.7
million parameters each, about 91 MB each in float32 by arithmetic; the exact
download size wasn't checked. CPU is fine). Same corpus as the lab, but with a real
embedding model and a real cross-encoder reranker instead of stand-ins.

  pip install -r requirements-real.txt
  python real_models.py

Expected (a prediction, not a measurement: no model runs on the test
machine): for "fix a flat bicycle tyre" and "squeaky brakes", where BM25
finds nothing, dense search puts a relevant document first. The script
prints PASS/FAIL for those two and the rest as information.
Models (Apache-2.0): sentence-transformers/all-MiniLM-L6-v2 and
cross-encoder/ms-marco-MiniLM-L6-v2.
"""
import sys

from sentence_transformers import CrossEncoder, SentenceTransformer

from corpus import DOCS, QUERIES, QRELS
from retrieval import BM25, ndcg_at_k, rrf

ids = list(DOCS)
texts = [DOCS[d] for d in ids]
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2", device="cpu")
doc_vecs = embedder.encode(texts, normalize_embeddings=True)
bm25 = BM25(DOCS)


def dense_search(query):
    q = embedder.encode([query], normalize_embeddings=True)
    sims = embedder.similarity(q, doc_vecs)[0].tolist()  # cosine by default
    return sorted(zip(ids, sims), key=lambda x: (-x[1], x[0]))


ok = True
for name, qid in [("R1a", "q2"), ("R1b", "q4")]:
    top = dense_search(QUERIES[qid])[0][0]
    hit = QRELS[qid].get(top, 0) > 0
    ok &= hit
    print(f"{'PASS' if hit else 'FAIL'} {name} dense top for {QUERIES[qid]!r}: {top}"
          f" (relevant: {sorted(QRELS[qid])})")

for qid, q in QUERIES.items():
    fused = rrf([bm25.search(q), dense_search(q)], top_k=10)
    candidates = [d for d, _ in fused]
    ranked = reranker.rank(q, [DOCS[d] for d in candidates], top_k=3)
    reranked = [candidates[r["corpus_id"]] for r in ranked]
    print(f"INFO {qid} nDCG@3 fused {ndcg_at_k(candidates, QRELS[qid], 3):.3f}, "
          f"reranked {ndcg_at_k(reranked, QRELS[qid], 3):.3f}; top 3 after rerank {reranked}")

sys.exit(0 if ok else 1)
