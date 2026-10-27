"""Part 06 lab: run every check and print PASS or FAIL for each.
Standard library only. Exit code 0 only if every check passes."""
import sys

from graph import DOCS, build_graph, extract_triples, louvain, louvain_level, modularity, resolve
from memory import Fact, Memory, safe_memory_path

results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"{'PASS' if ok else 'FAIL'} {name}{': ' + str(detail) if detail else ''}")


# 1. Extraction: one triple per note, with the note it came from.
triples = extract_triples(DOCS)
check("1 one triple per note, each with its source", len(triples) == len(DOCS)
      and {t[3] for t in triples} == set(DOCS), f"{len(triples)} triples")

# 2. Entity resolution: exact names leave a duplicate; normalizing merges it.
exact, norm = build_graph(DOCS, "exact"), build_graph(DOCS, "normalized")
check("2 exact names: 11 nodes ('ledger DB' and 'ledger database' apart)",
      len(exact.nodes) == 11 and {"ledger DB", "ledger database"} <= exact.nodes)
check("2b normalized names: 10 nodes, one ledger node", len(norm.nodes) == 10
      and resolve("Ledger  DB", "normalized") == "ledger database")

# 3. Two-hop question: who leads the team that owns the ledger database?
q_exact = exact.follow("ledger database", "OWNED_BY", "^LEADS")
q_norm = norm.follow("ledger database", "OWNED_BY", "^LEADS")
check("3 two hops, with provenance: avery lin, from notes n8 and n2",
      q_norm == [("avery lin", ["n8", "n2"])], q_norm)
check("3b the same question finds nothing without entity resolution", q_exact == [], q_exact)
check("3c no single note holds both hops",
      not any("ledger" in t.lower() and "leads" in t.lower() for t in DOCS.values()))

# 4. Path search ignores direction and finds the shortest route.
path = norm.shortest_path("rowan park", "index store")
check("4 shortest path rowan park -> index store", path == ["rowan park", "discovery team", "index store"], path)
check("4b no path between unconnected names", norm.shortest_path("avery lin", "nowhere") is None)

# 5. Modularity by hand: two communities, 5 edges inside each, 10 in all.
w = norm.undirected_weights()
two = [frozenset({"avery lin", "billing service", "finance group", "ledger database", "payments team"}),
       frozenset({"discovery team", "index store", "product group", "rowan park", "search service"})]
hand = 2 * (5 / 10 - (10 / 20) ** 2)
if set(norm.nodes) != two[0] | two[1]:   # e.g. the alias was removed: the split no longer fits
    check("5 modularity of the two-team split = 0.5 by hand", False, f"the graph's nodes changed: {len(norm.nodes)}")
else:
    check("5 modularity of the two-team split = 0.5 by hand", abs(modularity(w, two) - hand) < 1e-12,
          f"{modularity(w, two):.4f}")
check("5b one community for everything has modularity 0", abs(modularity(w, [frozenset(norm.nodes)])) < 1e-12)

# 6. Community detection.
level1 = louvain_level(w)
full = louvain(w)
check("6 local moving alone stops at 4 communities", len(level1) == 4, level1)
check("6b with merging: the two teams", [frozenset(c) for c in full] == sorted(two, key=min), full)
split = louvain(exact.undirected_weights())
check("6c without entity resolution the ledger splits off into its own community",
      ["billing service", "ledger database"] in split, f"{len(split)} communities")

# 7. Memory: three ways to handle a changed fact.
def remember(mode):
    m = Memory(mode)
    m.write(Fact("user", "home_city", "Lisbon", valid_at=10))
    m.write(Fact("user", "home_city", "Oslo", valid_at=40))
    return m

ow, ad, tp = remember("overwrite"), remember("add_only"), remember("temporal")
check("7 overwrite: only Oslo, history lost", ow.current("user", "home_city") == ["Oslo"]
      and ow.as_of("user", "home_city", 20) == [])
check("7b add-only: the stale city is still 'current'",
      sorted(ad.current("user", "home_city")) == ["Lisbon", "Oslo"])
check("7c temporal: Oslo now, Lisbon on day 20",
      tp.current("user", "home_city") == ["Oslo"] and tp.as_of("user", "home_city", 20) == ["Lisbon"]
      and tp.as_of("user", "home_city", 40) == ["Oslo"])
late = Memory("temporal")
late.write(Fact("user", "home_city", "Oslo", valid_at=40))
late.write(Fact("user", "home_city", "Lisbon", valid_at=10))   # an old fact arrives late
check("7d temporal: an older fact arriving late doesn't close the newer one",
      "Oslo" in late.current("user", "home_city"))

# 8. Poisoning gate and path safety.
g = Memory("temporal")
status = g.write(Fact("user", "home_city", "Atlantis", valid_at=50, source="web page"))
check("8 untrusted write is quarantined, memory unchanged", status == "quarantined"
      and g.current("user", "home_city") == [] and len(g.quarantine) == 1)
check("8b the same write is stored once approved",
      g.write(g.quarantine[0], approved=True) == "stored" and g.current("user", "home_city") == ["Atlantis"])
bad = ["/memories/../../secrets.env", "/memoriesX/a.md", "memories/a.md", "/etc/passwd", "/memories/a\\..\\b"]
refused = 0
for p in bad:
    try:
        safe_memory_path(p)
    except ValueError:
        refused += 1
check("8c traversal and look-alike paths refused, normal ones kept", refused == len(bad)
      and safe_memory_path("/memories/notes/today.md") == "/memories/notes/today.md", f"{refused} of {len(bad)} refused")

# 9. Arithmetic behind numbers the part quotes (inputs are the published figures).
paper = {
    "Mem0 vs OpenAI memory, LoCoMo J (points)": (round(66.88 - 52.90, 2), 13.98),
    "Mem0 vs OpenAI memory (relative %)": (round((66.88 / 52.90 - 1) * 100), 26),
    "full context vs Mem0 (points)": (round(72.90 - 66.88, 2), 6.02),
    "GraphRAG global vs vector RAG prompt tokens, Novel (x)": (round(331375 / 879), 377),
    "plain RAG over best graph method on NQ F1 (points)": (round(64.78 - 63.01, 2), 1.77),
    "HippoRAG2 over plain RAG on HotpotQA F1 (points)": (round(63.01 - 60.04, 2), 2.97),
    "HippoRAG2 over plain RAG on MultiHop-RAG accuracy (points)": (round(70.27 - 67.02, 2), 3.25),
    "answer entities missing from the graph, HotpotQA (%)": (round(100 - 65.8, 1), 34.2),
}
bad_rows = [k for k, (got, want) in paper.items() if got != want]
check("9 paper arithmetic", not bad_rows, ", ".join(bad_rows) or f"{len(paper)} figures")

print(f"\n{sum(results)} of {len(results)} checks passed")
sys.exit(0 if all(results) else 1)
