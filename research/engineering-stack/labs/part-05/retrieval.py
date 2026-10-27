"""Keyword search (BM25), a stand-in dense search, two fusion methods and
retrieval metrics. Standard library only, so it runs on any Python 3.11+.

Every function returns plain data so the checks in run_lab.py can test it.
"""
import math
import re
from collections import Counter

STOPWORDS = {"a", "an", "the", "to", "and", "or", "of", "on", "in", "is", "it",
             "for", "with", "when", "they", "are", "every", "will", "not", "my",
             "how", "your", "you", "means", "check", "below", "near", "often"}


def tokenize(text):
    """Lowercase, split on anything that isn't a letter or digit, drop stopwords."""
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]


# ---------- BM25 (the Lucene variant) ----------

class BM25:
    """BM25 with Lucene's IDF, log(1 + (N - df + 0.5) / (df + 0.5)), which is
    never negative. k1 sets how fast repeated words stop adding score; b sets
    how much long documents are penalized (0 = not at all, 1 = fully)."""

    def __init__(self, docs, k1=1.2, b=0.75):
        self.ids = list(docs)
        self.toks = {d: tokenize(docs[d]) for d in self.ids}
        self.k1, self.b = k1, b
        self.n = len(self.ids)
        self.avgdl = sum(len(t) for t in self.toks.values()) / self.n
        df = Counter()
        for t in self.toks.values():
            df.update(set(t))
        self.idf = {w: math.log(1 + (self.n - c + 0.5) / (c + 0.5)) for w, c in df.items()}

    def score(self, query, doc_id):
        tf = Counter(self.toks[doc_id])
        dl = len(self.toks[doc_id])
        total = 0.0
        for w in tokenize(query):
            if w not in tf:
                continue
            f = tf[w]
            denom = f + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            total += self.idf[w] * f * (self.k1 + 1) / denom
        return total

    def search(self, query, top_k=None):
        """Ranked [(doc_id, score)], best first; zero scores dropped; ties by id."""
        scored = [(d, self.score(query, d)) for d in self.ids]
        scored = [(d, s) for d, s in scored if s > 0]
        scored.sort(key=lambda x: (-x[1], x[0]))
        return scored[:top_k] if top_k else scored


# ---------- stand-in dense search ----------

class ConceptSearch:
    """Stand-in for an embedding model: map words to concepts, compare bags of
    concepts by cosine similarity. Illustrative only (see corpus.CONCEPTS)."""

    def __init__(self, docs, concepts):
        self.concepts = concepts
        self.ids = list(docs)
        self.vecs = {d: self.embed(docs[d]) for d in self.ids}

    def embed(self, text):
        bag = Counter(self.concepts[t] for t in tokenize(text) if t in self.concepts)
        norm = math.sqrt(sum(v * v for v in bag.values())) or 1.0
        return {k: v / norm for k, v in bag.items()}  # unit length

    def search(self, query, top_k=None):
        q = self.embed(query)
        scored = [(d, sum(q.get(k, 0.0) * v for k, v in self.vecs[d].items())) for d in self.ids]
        scored = [(d, s) for d, s in scored if s > 0]
        scored.sort(key=lambda x: (-x[1], x[0]))
        return scored[:top_k] if top_k else scored


# ---------- fusion ----------

def rrf(rankings, k=60, top_k=None):
    """Reciprocal rank fusion: score(d) = sum over lists of 1 / (k + rank),
    ranks starting at 1. Uses ranks only, so the lists' scores never mix."""
    fused = Counter()
    for ranking in rankings:
        for rank, (doc_id, _score) in enumerate(ranking, start=1):
            fused[doc_id] += 1.0 / (k + rank)
    out = sorted(fused.items(), key=lambda x: (-x[1], x[0]))
    return out[:top_k] if top_k else out


def min_max(ranking):
    """Rescale one list's scores to 0..1 (one document, or all equal, gives 1.0)."""
    if not ranking:
        return {}
    lo = min(s for _, s in ranking)
    hi = max(s for _, s in ranking)
    return {d: (s - lo) / (hi - lo) if hi > lo else 1.0 for d, s in ranking}


def convex(dense, sparse, alpha=0.5, top_k=None):
    """Convex combination: alpha * dense + (1 - alpha) * sparse, after min-max
    scaling each list. A document missing from a list gets 0 from it."""
    dn, sn = min_max(dense), min_max(sparse)
    fused = {d: alpha * dn.get(d, 0.0) + (1 - alpha) * sn.get(d, 0.0) for d in set(dn) | set(sn)}
    out = sorted(fused.items(), key=lambda x: (-x[1], x[0]))
    return out[:top_k] if top_k else out


# ---------- metrics ----------

def recall_at_k(ranked_ids, rels, k):
    """Share of the relevant documents (grade > 0) that appear in the top k."""
    relevant = {d for d, g in rels.items() if g > 0}
    return len(relevant & set(ranked_ids[:k])) / len(relevant) if relevant else 0.0


def precision_at_k(ranked_ids, rels, k):
    """Share of the top k that are relevant (divides by k even if fewer came back)."""
    return sum(1 for d in ranked_ids[:k] if rels.get(d, 0) > 0) / k


def mrr(ranked_ids, rels):
    """1 / rank of the first relevant document; 0 if none was found."""
    for rank, d in enumerate(ranked_ids, start=1):
        if rels.get(d, 0) > 0:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(ranked_ids, rels, k, exp_gain=False):
    """nDCG@k with a log2(rank + 1) discount. Gain is the grade (trec_eval's
    default) or 2**grade - 1 (exp_gain=True, the Burges variant)."""
    gain = (lambda g: 2 ** g - 1) if exp_gain else (lambda g: g)
    dcg = sum(gain(rels.get(d, 0)) / math.log2(i + 1) for i, d in enumerate(ranked_ids[:k], start=1))
    ideal = sorted(rels.values(), reverse=True)[:k]
    idcg = sum(gain(g) / math.log2(i + 1) for i, g in enumerate(ideal, start=1))
    return dcg / idcg if idcg else 0.0


# ---------- chunking ----------

def chunk_text(text, size=200, overlap=40, seps=("\n\n", "\n", ". ", " ")):
    """Split text into pieces of at most `size` characters, preferring to cut
    at paragraph, line, sentence, then word breaks (the idea behind LangChain's
    RecursiveCharacterTextSplitter, written from scratch). Each chunk after the
    first starts with up to `overlap` characters copied from the end of the
    previous one, so a fact cut in half still appears whole somewhere."""
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    pieces = _split(text, size - overlap, list(seps))
    chunks = []
    for piece in pieces:
        if chunks:
            tail = chunks[-1][-overlap:] if overlap else ""
            piece = tail + piece
        chunks.append(piece)
    return chunks


def _split(text, limit, seps):
    if len(text) <= limit:
        return [text] if text else []
    if not seps:  # no break left: hard cut
        return [text[i:i + limit] for i in range(0, len(text), limit)]
    sep, rest = seps[0], seps[1:]
    parts = text.split(sep)
    out, current = [], ""
    for i, part in enumerate(parts):
        piece = part + (sep if i < len(parts) - 1 else "")
        if len(current) + len(piece) <= limit:
            current += piece
        else:
            if current:
                out.append(current)
            if len(piece) <= limit:
                current = piece
            else:
                out.extend(_split(piece, limit, rest))
                current = ""
    if current:
        out.append(current)
    return out
