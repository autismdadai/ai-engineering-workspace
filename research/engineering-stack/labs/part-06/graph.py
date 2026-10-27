"""A tiny property graph, a stand-in extractor, entity resolution, path queries
and community detection. Standard library only (Python 3.11+).

Part 06 of The AI Engineering Stack. The documents and names are invented [I].
"""
import re
from collections import defaultdict, deque

# ---------- the data: short invented notes about a small company ----------

DOCS = {
    "n1": "The billing service is owned by the Payments team.",
    "n2": "Avery Lin leads the Payments team.",
    "n3": "The Payments team reports to the Finance group.",
    "n4": "The search service is owned by the Discovery team.",
    "n5": "Rowan Park leads the Discovery team.",
    "n6": "The Discovery team reports to the Product group.",
    "n7": "The billing service depends on the ledger database.",
    "n8": "The ledger DB is owned by the Payments team.",
    "n9": "The search service depends on the index store.",
    "n10": "The index store is owned by the Discovery team.",
}

# Stand-in for LLM extraction [I]: fixed phrases map to relation types.
# A real pipeline asks a model for (subject, relation, object) triples.
RELATIONS = [
    (r"(.+?) is owned by (.+)", "OWNED_BY"),
    (r"(.+?) leads (.+)", "LEADS"),
    (r"(.+?) reports to (.+)", "REPORTS_TO"),
    (r"(.+?) depends on (.+)", "DEPENDS_ON"),
]


def extract_triples(docs):
    """Return [(subject, relation, object, source_id)] from simple sentences."""
    triples = []
    for doc_id, text in docs.items():
        sentence = text.strip().rstrip(".")
        for pattern, rel in RELATIONS:
            m = re.fullmatch(pattern, sentence)
            if m:
                subj, obj = (_clean(x) for x in m.groups())
                triples.append((subj, rel, obj, doc_id))
                break
    return triples


def _clean(phrase):
    return re.sub(r"^the\s+", "", phrase.strip(), flags=re.I)


# ---------- entity resolution ----------

ALIASES = {"ledger db": "ledger database"}   # a hand-made alias table [I]


def resolve(name, mode="exact"):
    """'exact' keeps names as written (neo4j-graphrag's default merges only
    identical names); 'normalized' lowercases, collapses spaces and applies
    the alias table, so 'ledger DB' and 'ledger database' become one node."""
    if mode == "exact":
        return name
    key = re.sub(r"\s+", " ", name.lower()).strip()
    return ALIASES.get(key, key)


# ---------- the graph ----------

class Graph:
    """Directed property graph: nodes are names, edges carry a relation type
    and the id of the note they came from (provenance)."""

    def __init__(self):
        self.out = defaultdict(list)    # node -> [(relation, node, source)]
        self.inn = defaultdict(list)
        self.nodes = set()

    def add(self, subj, rel, obj, source):
        self.nodes.update((subj, obj))
        self.out[subj].append((rel, obj, source))
        self.inn[obj].append((rel, subj, source))

    def follow(self, start, *rels):
        """Walk a chain of relation types; '^REL' walks an edge backwards.
        Returns [(end_node, [sources])] for every path that matches."""
        frontier = [(start, [])]
        for rel in rels:
            nxt = []
            backwards = rel.startswith("^")
            name = rel.lstrip("^")
            for node, sources in frontier:
                edges = self.inn[node] if backwards else self.out[node]
                for r, other, src in edges:
                    if r == name:
                        nxt.append((other, sources + [src]))
            frontier = nxt
        return sorted(frontier)

    def shortest_path(self, a, b):
        """Breadth-first search ignoring direction; returns the node list or None."""
        seen, queue = {a: None}, deque([a])
        while queue:
            node = queue.popleft()
            if node == b:
                path = []
                while node is not None:
                    path.append(node)
                    node = seen[node]
                return path[::-1]
            for _, other, _ in self.out[node] + self.inn[node]:
                if other not in seen:
                    seen[other] = node
                    queue.append(other)
        return None

    def undirected_weights(self):
        """Edge weights for community detection: each pair counted once per edge."""
        w = defaultdict(float)
        for subj in self.out:
            for _, obj, _ in self.out[subj]:
                if subj != obj:
                    w[frozenset((subj, obj))] += 1.0
        return w


def build_graph(docs, mode="exact"):
    g = Graph()
    for subj, rel, obj, src in extract_triples(docs):
        g.add(resolve(subj, mode), rel, resolve(obj, mode), src)
    return g


# ---------- communities: modularity and one level of Louvain ----------

def modularity(weights, communities):
    """Newman's modularity Q = sum over communities c of
    [ L_c / m  -  (d_c / 2m)^2 ], with m the total edge weight, L_c the weight
    inside c and d_c the summed degree of c's nodes."""
    m = sum(weights.values())
    degree = defaultdict(float)
    for pair, wt in weights.items():
        for n in pair:
            degree[n] += wt
    where = {n: i for i, c in enumerate(communities) for n in c}
    inside = defaultdict(float)
    for pair, wt in weights.items():
        a, b = tuple(pair)
        if where[a] == where[b]:
            inside[where[a]] += wt
    q = 0.0
    for i, c in enumerate(communities):
        d = sum(degree[n] for n in c)
        q += inside[i] / m - (d / (2 * m)) ** 2
    return q


def louvain_level(weights):
    """The local-moving phase of Louvain (Blondel et al.), deterministic: start
    with every node alone, then move each node, in sorted order, to the
    neighbouring community that raises modularity most, until nothing moves.
    Real Louvain then merges communities and repeats; Leiden adds a refinement
    step so every community stays connected."""
    nodes = sorted({n for pair in weights for n in pair})
    comm = {n: i for i, n in enumerate(nodes)}

    def parts():
        groups = defaultdict(set)
        for n, c in comm.items():
            groups[c].add(n)
        return [frozenset(g) for _, g in sorted(groups.items())]

    neighbours = defaultdict(set)
    for pair in weights:
        a, b = tuple(pair)
        neighbours[a].add(b)
        neighbours[b].add(a)
    moved = True
    while moved:
        moved = False
        for n in nodes:
            best_c, best_q = comm[n], modularity(weights, parts())
            for c in sorted({comm[x] for x in neighbours[n]} - {comm[n]}):
                old = comm[n]
                comm[n] = c
                q = modularity(weights, parts())
                comm[n] = old
                if q > best_q + 1e-12:
                    best_c, best_q = c, q
            if best_c != comm[n]:
                comm[n] = best_c
                moved = True
    return sorted((sorted(c) for c in parts()), key=lambda c: c[0])


def louvain(weights):
    """Local moving, then repeated merging of whole communities while that
    raises modularity: a simplified stand-in for Louvain's aggregation phase
    (real Louvain rebuilds a smaller graph and runs local moving on it)."""
    parts = [frozenset(c) for c in louvain_level(weights)]
    linked = lambda a, b: any(frozenset((x, y)) in weights for x in a for y in b)
    while True:
        base = modularity(weights, parts)
        best = None
        for i in range(len(parts)):
            for j in range(i + 1, len(parts)):
                if not linked(parts[i], parts[j]):
                    continue
                trial = [p for k, p in enumerate(parts) if k not in (i, j)] + [parts[i] | parts[j]]
                gain = modularity(weights, trial) - base
                if gain > 1e-12 and (best is None or gain > best[0]):
                    best = (gain, i, j)
        if best is None:
            return sorted((sorted(c) for c in parts), key=lambda c: c[0])
        _, i, j = best
        parts = [p for k, p in enumerate(parts) if k not in (i, j)] + [parts[i] | parts[j]]
