# Claims to check, set A

## Sources (key, class: citation with URL)

- **AGE** (OD): Apache AGE, LICENSE and README. https://github.com/apache/age
- **AMT** (OD): Anthropic, "Memory tool", Claude API docs. https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool
- **APO** (PR): Chen et al., "AgentPoison", NeurIPS 2024 (poster page https://neurips.cc/virtual/2024/poster/94715); arXiv 2407.12784 (abstract)
- **AUR** (OD): Neo4j pricing and Aura FAQ. https://neo4j.com/pricing/ ; https://neo4j.com/cloud/platform/aura-graph-database/faq/
- **COA** (PR): Sumers et al., "Cognitive Architectures for Language Agents" (CoALA), TMLR 2024, arXiv 2309.02427v3, §4.1
- **DNK** (PP): Zheng et al., "Less is More: Denoising Knowledge Graphs For Retrieval Augmented Generation", arXiv 2510.14271v1 (abstract)
- **EDG** (PP): Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization", arXiv 2404.16130v2 (ledger)
- **FDB** (OD): FalkorDB, LICENSE and README. https://github.com/FalkorDB/FalkorDB ; PyPI `falkordb`
- **GHT** (OD): Tags read with `git ls-remote --tags` from github.com on October 14, 2026: neo4j/neo4j, microsoft/graphrag, letta-ai/letta, networkx/networkx, mem0ai/mem0, getzep/graphiti, kuzudb/kuzu
- **GQL** (SB): ISO/IEC 39075:2024, catalogue page. https://www.iso.org/standard/76120.html
- **GRA** (OD): Graphiti, README, `graphiti_core/edges.py`, `graphiti_core/utils/maintenance/edge_operations.py`, `graphiti_core/telemetry/telemetry.py` (main, October 14, 2026); PyPI `graphiti-core` 0.30.2. https://github.com/getzep/graphiti
- **GRB** (PR): Xiang et al., "When to use Graphs in RAG: A Comprehensive Analysis for Graph Retrieval-Augmented Generation", arXiv 2506.05690v3, Table 2 and token-cost tables; ICLR 2026 poster (https://iclr.cc/virtual/2026/poster/10007992)
- **HAN** (PP): Han et al., "RAG vs. GraphRAG: A Systematic Evaluation and Key Insights", arXiv 2502.11371v3, Tables 1 and 2, §4.2, §5.3
- **HIP** (PR): Gutiérrez et al., "HippoRAG", NeurIPS 2024 (https://papers.nips.cc/paper_files/paper/2024/hash/6ddc001d07ca4f319af96a3024f6dbd1-Abstract-Conference.html); arXiv 2405.14831
- **KUZ** (OD): Kuzu, README and repository banner. https://github.com/kuzudb/kuzu
- **LEI** (PR): Traag, Waltman and van Eck, "From Louvain to Leiden: guaranteeing well-connected communities", Scientific Reports 9:5233 (2019), DOI 10.1038/s41598-019-41695-z
- **LTC** (OD): Letta Code, README and `src/telemetry/index.ts` (commit of October 13, 2026). https://github.com/letta-ai/letta-code
- **LZY** (VB): Microsoft Research blog, "LazyGraphRAG: Setting a new standard for quality and cost", November 25, 2024 (updated June 6, 2025)
- **MGM** (OD): Memgraph, LICENSE and `licenses/BSL.txt`. https://github.com/memgraph/memgraph
- **MGR** (OD): Microsoft GraphRAG repository: README (maintenance notice), `docs/index/methods.md`, `docs/index/default_dataflow.md`, `docs/query/overview.md`, `docs/config/models.md`, `config/defaults.py`, `pyproject.toml` (commit 5faaaf4, October 8, 2026). https://github.com/microsoft/graphrag
- **MIN** (PP): Dong et al., "Memory Injection Attacks on LLM Agents via Query-Only Interaction" (MINJA), arXiv 2503.03704v5 (abstract)
- **N4G** (OD): neo4j-graphrag, `retrievers/__init__.py`, `experimental/pipeline/kg_builder.py`, resolver components; PyPI 1.22.0. https://github.com/neo4j/neo4j-graphrag-python
- **N4J** (OD): neo4j/neo4j at tag 2026.09.0: README.asciidoc "Licensing", LICENSE.txt. https://github.com/neo4j/neo4j
- **NPG** (OD): Neo4j, "What is a graph database". https://neo4j.com/docs/getting-started/graph-database/
- **NXR** (OD): networkx release notes (`doc/release/release_3.7.rst`, `release_3.5.rst`) and the 3.7 and 3.6.1 wheels' `leiden.py`
- **OCY** (OD): openCypher (https://opencypher.org/) and Neo4j Cypher Manual, "GQL conformance"
- **OWA** (SB): OWASP GenAI Security Project, "Memory Is a Feature. It Is Also an Attack Surface", May 13, 2026, and the Top 10 for Agentic Applications resource page (December 9, 2025). https://genai.owasp.org/blog/memory-is-a-feature-it-is-also-an-attack-surface/
- **PYPI** (OD): The Python Package Index, JSON API, October 14, 2026. https://pypi.org/pypi/NAME/json
- **RDF** (SB): W3C, "RDF 1.1 Concepts and Abstract Syntax", Recommendation, February 25, 2014. https://www.w3.org/TR/rdf11-concepts/
- **T2C** (PP): Ozsoy et al., "Text2Cypher", arXiv 2412.10064v1 (abstract)
- **TOG** (PP): Sun et al., "Think-on-Graph", arXiv 2307.07697v6 (abstract)
- **ZHU** (PP): Zhu et al., "LLMs for Knowledge Graph Construction and Reasoning", arXiv 2305.13168v4, Table 1

## Claims

A001. [1. In plain words] **GraphRAG** is the name Microsoft gave its method of having a model build such a graph from documents and summarize groups of related things, so it can answer broad questions about a whole collection .  SOURCES: EDG
A002. [1. In plain words] Microsoft's own README warns that "GraphRAG indexing can be an expensive operation" , and in one independent study only about 65.5% to 65.8% of answer entities made it into the model-built graph .  SOURCES: MGR, HAN
A003. [1. In plain words] **T09, agent memory.** A model is stateless: each call starts from what is in its context, and nothing is kept between calls (ledger P3-01) . "Memory" is a system around the model that saves facts, preferences or past events and puts the relevant ones back into the context next time.  SOURCES: COA
A004. [2. Definitions] Nodes and edges that each carry key-value details | Property graph | Neo4j's model: a relationship has a start node, an end node, "exactly one type" and a direction  SOURCES: NPG
A005. [2. Definitions] A fact written as subject, predicate, object | Triple; RDF | "An RDF graph is a set of RDF triples" (W3C)  SOURCES: RDF
A006. [2. Definitions] The ISO standard query language for property graphs | GQL (ISO/IEC 39075:2024) | Published April 2024  SOURCES: GQL
A007. [2. Definitions] Two common community-detection methods | Louvain; Leiden | Leiden guarantees connected communities  SOURCES: LEI
A008. [2. Definitions] Microsoft's graph-based retrieval method and library | GraphRAG | Global, local, DRIFT and basic search  SOURCES: MGR
A009. [2. Definitions] Memory for the current task only | Working memory | CoALA  SOURCES: COA
A010. [2. Definitions] Memory of what happened before | Episodic memory | CoALA  SOURCES: COA
A011. [2. Definitions] Memory of facts about the world and the agent | Semantic memory | CoALA  SOURCES: COA
A012. [2. Definitions] The weights plus the agent's own code | Procedural memory | CoALA  SOURCES: COA
A013. [2. Definitions] Memory work done in the background, not during the reply | Sleep-time compute; "dreaming" (Letta)  SOURCES: LTC
A014. [2. Definitions] When a fact became true; when it stopped | Valid time (`valid_at`, `invalid_at`) | Graphiti's edge fields  SOURCES: GRA
A015. [2. Definitions] Planting false or hostile entries in an agent's memory | Memory poisoning | OWASP ASI06  SOURCES: OWA
A016. [2. Definitions] Escaping a folder with `..` in a file path | Path traversal  SOURCES: AMT
A017. [3.1 Two ways to store a graph] **Property graphs.** In Neo4j's model, nodes have labels and "any number of key-value pairs as properties"; a relationship "must always have a start node, an end node, and exactly one type", "must have a direction", and "can have properties, like nodes" .  SOURCES: NPG
A018. [3.1 Two ways to store a graph] **RDF triples.** The W3C's RDF writes every fact as a triple, subject, predicate, object, and "An RDF graph is a set of RDF triples" .  SOURCES: RDF
A019. [3.1 Two ways to store a graph] Objects can be other nodes or literals, "values such as strings, numbers, and dates" .  SOURCES: RDF
A020. [3.1 Two ways to store a graph] ISO published GQL, a standard query language for property graphs, in April 2024 as ISO/IEC 39075:2024 . openCypher calls itself "a key inspiration for the ISO/IEC 39075 GQL project" and says its specification "evolves towards" GQL; Neo4j says it is "working towards full GQL conformance" .  SOURCES: GQL, OCY
A021. [3.2 From text to graph] Microsoft GraphRAG's standard pipeline, from its documentation :  SOURCES: MGR
A022. [3.2 From text to graph] Its documentation estimates graph extraction at "roughly 75% of indexing cost", and offers a cheaper `fast` method that replaces the model with noun phrases and co-occurrence, which "tends to be quite a bit noisier" .  SOURCES: MGR
A023. [3.2 From text to graph] **Extraction misses things.** In an independent study, graphs built by GPT-4o-mini contained only about 65.8% (HotpotQA) and 65.5% (NQ) of the entities that appear in the answers, and graphs built by the larger GPT-4o did better .  SOURCES: HAN
A024. [3.2 From text to graph] Older measurements were worse: in a 2023 preprint, zero-shot GPT-4 scored micro F1 15.5 on Re-TACRED relation extraction against 91.4 for the best fine-tuned model, though strict exact-match scoring penalizes free-form answers .  SOURCES: ZHU
A025. [3.2 From text to graph] **Entity resolution.** The same thing gets written different ways, and a graph that keeps "ledger DB" and "ledger database" as two nodes can't connect facts about them. neo4j-graphrag's `SimpleKGPipeline` resolves entities by default, but its docstring says it merges only "entities with same label and name", using an exact-match resolver; fuzzy and spaCy-based resolvers exist but must be switched on .  SOURCES: N4G
A026. [3.2 From text to graph] A 2025 preprint names "redundant entities and unreliable relationships" as the main noise in model-built graphs and reports better QA after removing them .  SOURCES: DNK
A027. [3.3 Communities, modularity, Louvain and Leiden] GraphRAG's global search depends on grouping the graph into communities and summarizing each one .  SOURCES: EDG, MGR
A028. [3.3 Communities, modularity, Louvain and Leiden] **Leiden** fixes a flaw: "the Louvain algorithm may yield arbitrarily badly connected communities", while Leiden's communities are "guaranteed to be connected" (Traag, Waltman and van Eck, Scientific Reports, 2019) .  SOURCES: LEI
A029. [3.3 Communities, modularity, Louvain and Leiden] GraphRAG uses hierarchical Leiden with at most 10 nodes per cluster, and pins its Leiden library below version 1.3 because 1.3 "changes Leiden clustering output", a reminder that communities depend on the implementation .  SOURCES: MGR
A030. [3.3 Communities, modularity, Louvain and Leiden] **Tools.** networkx (BSD-3-Clause) has Louvain built in; version 3.7 (September 21, 2026) added Leiden, with its default metric CPM rather than modularity, and needs Python 3.12 or later; in 3.6.1, the last for Python 3.11, the Leiden function raises `NotImplementedError` unless a separate backend is installed . leidenalg and igraph are GPL, which matters if you ship code that includes them .  SOURCES: NXR, PYPI
A031. [3.4 Asking the graph] **GraphRAG's four query modes** :  SOURCES: MGR
A032. [3.4 Asking the graph] **Other patterns.** **Text-to-Cypher**: a model writes the query from the question; neo4j-graphrag ships a `Text2CypherRetriever`, and a 2024 preprint built a 44,387-example dataset for it .  SOURCES: N4G, T2C
A033. [3.4 Asking the graph] **Vector plus graph**: find entry nodes by embedding similarity, then traverse; neo4j-graphrag's `VectorCypherRetriever` and `HybridCypherRetriever` (ledger B3-05) .  SOURCES: N4G
A034. [3.4 Asking the graph] **HippoRAG** (NeurIPS 2024) links passages through a model-built graph and ranks with Personalized PageRank .  SOURCES: HIP
A035. [3.4 Asking the graph] **Think-on-Graph** lets a model search an existing curated graph step by step; it targets graphs like Wikidata rather than building its own .  SOURCES: TOG
A036. [3.5 Does GraphRAG beat plain retrieval?] **Han et al.** (preprint; graphs built with GPT-4o-mini, answers by Llama-3.1-8B) .  SOURCES: HAN
A037. [3.5 Does GraphRAG beat plain retrieval?] **Xiang et al., "When to use Graphs in RAG"** (ICLR 2026; answers by GPT-4o-mini; a medical corpus and a novels corpus) .  SOURCES: GRB
A038. [3.5 Does GraphRAG beat plain retrieval?] **Cost.** In the same ICLR study, the average prompt per question was about 900 tokens for vector RAG, about 39,000 for GraphRAG local search and about 331,000 for global search (331,375 against 879 on the novels: 377 times as many) .  SOURCES: GRB
A039. [3.5 Does GraphRAG beat plain retrieval?] HippoRAG2 used about 1,000 and was the strongest graph method in both studies .  SOURCES: HAN, GRB
A040. [3.5 Does GraphRAG beat plain retrieval?] **The 2024 headline needs a caveat.** Microsoft's paper reported that model judges preferred GraphRAG's answers to global questions on comprehensiveness in 72% to 83% of comparisons (ledger B3-04) .  SOURCES: EDG
A041. [3.5 Does GraphRAG beat plain retrieval?] Han et al. found strong position bias when model judges compare RAG and GraphRAG summaries: reversing the order gave "substantially different, and in some cases opposite, judgments" .  SOURCES: HAN
A042. [3.5 Does GraphRAG beat plain retrieval?] **LazyGraphRAG.** Microsoft Research's blog describes a version that skips model extraction at indexing time and claims indexing "identical to vector RAG and 0.1% of the costs of full GraphRAG", with global-query quality comparable at "more than 700 times lower query cost" .  SOURCES: LZY
A043. [3.5 Does GraphRAG beat plain retrieval?] The 0.1% has no stated dataset or model, no independent replication was found, and it isn't in the open-source repository; the repo only links the post .  SOURCES: LZY, MGR
A044. [3.5 Does GraphRAG beat plain retrieval?] **Microsoft GraphRAG is now in maintenance mode.** Its README (October 8, 2026, version 3.3.0) says: "This project is largely in maintenance mode, and won't be accepting new PRs or implementing new features", with bug fixes and security updates only, and that the code "serves as a demonstration and is not an officially supported Microsoft offering" .  SOURCES: MGR
A045. [3.10 Memory as an attack surface] AgentPoison (NeurIPS 2024) planted records in agents' memory or knowledge bases and reported an average attack success above 80% with a poison rate below 0.1% .  SOURCES: APO
A046. [3.10 Memory as an attack surface] MINJA (preprint) injected malicious records "by only interacting with the agent via queries and output observations", with no direct write access .  SOURCES: MIN
A047. [3.10 Memory as an attack surface] OWASP's Top 10 for Agentic Applications (December 2025) lists "ASI06: Memory & Context Poisoning" .  SOURCES: OWA
A048. [3.10 Memory as an attack surface] Anthropic's memory-tool docs tell developers that "Your implementation must validate every path in every command to prevent directory traversal attacks", with `/memories/../../secrets.env` as the example .  SOURCES: AMT
A049. [6. What you need] Checked October 14, 2026 .  SOURCES: PYPI, GHT
A050. [6. What you need] networkx | Graphs in Python: paths, Louvain, Leiden (3.7) | BSD-3-Clause | 3.7 needs Python 3.12 or later; 3.6.1 for 3.11 | No | Yes | 3.7, September 21, 2026  SOURCES: PYPI
A051. [6. What you need] Microsoft GraphRAG (`graphrag`) | Model-built graph index with community summaries | MIT | Python 3.11 to 3.13 | A model API; `graphrag init` defaults to OpenAI `gpt-4.1` and `text-embedding-3-large` | "largely in maintenance mode" | 3.3.0, October 8, 2026  SOURCES: PYPI, MGR
A052. [6. What you need] Neo4j | Graph database server with Cypher | Community Edition GPLv3; Enterprise commercial | A server (Java); AuraDB Free hosted: up to 200,000 nodes and 400,000 relationships, deleted after 30 days without activity, no card needed | Free account for Aura | Yes | 2026.09.0  SOURCES: N4J, AUR
A053. [6. What you need] neo4j-graphrag | Building and querying graphs in Neo4j with a model | Apache-2.0 | Python 3.10 to 3.14; needs Neo4j | A model API or local model | Yes | 1.22.0, October 1, 2026  SOURCES: N4G
A054. [6. What you need] Kuzu | Embedded graph database (no server) | MIT | Python library | No | **Archived**: "read-only" since October 10, 2025 | 0.11.3  SOURCES: KUZ
A055. [6. What you need] FalkorDB | Graph database (a Redis module) | Server SSPL v1; Python client MIT | A server | No | Yes | client 1.8.0  SOURCES: FDB
A056. [6. What you need] Apache AGE | Cypher in PostgreSQL | Apache-2.0 | A Postgres extension | No | Yes  SOURCES: AGE
A057. [6. What you need] Memgraph | In-memory graph database | BSL 1.1, which says it is "not an 'open source' license", becoming Apache-2.0 in 2030 | A server | No | Yes  SOURCES: MGM
A058. [6. What you need] For memory, start with something you can read: a folder of Markdown files behind a path check, like Anthropic's memory tool design, with your own code deciding what is written .  SOURCES: AMT
A059. [6. What you need] Neo4j has the most mature tooling around Cypher and neo4j-graphrag, under GPLv3 for Community Edition ; Apache AGE keeps the graph inside Postgres under Apache-2.0 .  SOURCES: N4J, N4G, AGE
A060. [6. What you need] For memory that must answer "what was true then?", a temporal design like Graphiti's is the documented option, with its OpenAI default and telemetry switched as you need .  SOURCES: GRA
A061. [6. What you need] **When not to use a graph:** single-fact lookups, where plain RAG matched or beat graph methods in both studies ; small corpora that fit in a context window (Part 04); and anything where a model-built graph's missing third of entities would hurt .  SOURCES: HAN, GRB
A062. [6. What you need] **Strongest alternatives to name:** HippoRAG2 was the strongest graph method in both independent studies and cheap per question ; for Microsoft GraphRAG specifically, plan for a library that gets bug fixes but no new features .  SOURCES: HAN, GRB, MGR
A063. [6. What you need] Kuzu, often recommended for embedded graphs, is archived .  SOURCES: KUZ
