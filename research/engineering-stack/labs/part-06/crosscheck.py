"""Optional: compare the lab's graph code with networkx. Needs
requirements-crosscheck.txt (networkx 3.7 on Python 3.12+, 3.6.1 on 3.11)."""
import sys

from graph import DOCS, build_graph, louvain, modularity

try:
    import networkx as nx
    from networkx.algorithms.community import louvain_communities
    from networkx.algorithms.community import modularity as nx_modularity
except ImportError:
    print("FAIL nothing was checked: install requirements-crosscheck.txt in this environment")
    sys.exit(1)

ok = True
g = build_graph(DOCS, "normalized")
w = g.undirected_weights()
G = nx.Graph()
for pair, wt in w.items():
    a, b = sorted(pair)
    G.add_edge(a, b, weight=wt)

ours = [frozenset(c) for c in louvain(w)]
gap = abs(modularity(w, ours) - nx_modularity(G, ours, weight="weight"))
ok &= gap < 1e-12
print(f"{'PASS' if gap < 1e-12 else 'FAIL'} networkx {nx.__version__} modularity of our partition: gap {gap:.1e}")

theirs = {frozenset(c) for c in louvain_communities(G, weight="weight", seed=7)}
same = theirs == set(ours)
ok &= same
print(f"{'PASS' if same else 'FAIL'} networkx louvain_communities (seed 7) finds the same two communities")

path = nx.shortest_path(G, "rowan park", "index store")
same_path = path == g.shortest_path("rowan park", "index store")
ok &= same_path
print(f"{'PASS' if same_path else 'FAIL'} shortest path matches: {path}")

if hasattr(nx.community, "leiden_communities"):
    try:
        lc = nx.community.leiden_communities(G, metric="modularity", seed=7)
        print(f"INFO networkx Leiden (modularity) finds {len(lc)} communities")
    except (NotImplementedError, TypeError) as error:
        print(f"INFO networkx Leiden not usable here: {type(error).__name__}")
sys.exit(0 if ok else 1)
