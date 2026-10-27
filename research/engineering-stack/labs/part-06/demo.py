"""Print what the lab builds: triples, the graph's answers, communities, and
how three memory designs handle a changed fact. Standard library only."""
from graph import DOCS, build_graph, extract_triples, louvain, modularity
from memory import Fact, Memory

print("1. Triples extracted (subject, relation, object, note)")
for t in extract_triples(DOCS):
    print("  ", t)

for mode in ("exact", "normalized"):
    g = build_graph(DOCS, mode)
    w = g.undirected_weights()
    parts = louvain(w)
    print(f"\n2. Graph with {mode} names: {len(g.nodes)} nodes")
    print("   Who leads the team that owns the ledger database?",
          g.follow("ledger database", "OWNED_BY", "^LEADS") or "no answer")
    print(f"   communities (modularity {modularity(w, [frozenset(c) for c in parts]):.3f}):")
    for c in parts:
        print("     ", c)

print("\n3. The user moved from Lisbon (day 10) to Oslo (day 40)")
for mode in ("overwrite", "add_only", "temporal"):
    m = Memory(mode)
    m.write(Fact("user", "home_city", "Lisbon", valid_at=10))
    m.write(Fact("user", "home_city", "Oslo", valid_at=40))
    print(f"   {mode:9}  current {m.current('user', 'home_city')}   on day 20 {m.as_of('user', 'home_city', 20)}")
