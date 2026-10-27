"""Axis test for the engineering-stack plan: does each candidate axis place every topic cleanly?
A cell holds a value (clean) or starts with 'x ' (fails, with the reason code)."""
X = "x "
topics = [
 # id, topic, part, layer, changes, hardware, cost, maturity, risk
 ("T01","Evals, test data and judges","02", X+"cuts across","measurement",X+"path",X+"path",X+"mix",X+"use"),
 ("T02","Structured outputs and tool calling","03","Integration",X+"two",X+"path",X+"path","established",X+"use"),
 ("T03","Reasoning models","03","Model","model",X+"path",X+"path","established",X+"use"),
 ("T04","Prompt optimization (DSPy)","03","Context","input",X+"path",X+"path","emerging",X+"use"),
 ("T05","Context budget and placement","04","Context","input",X+"path",X+"path",X+"mix",X+"use"),
 ("T06","Provider prompt caching","04","Runtime*","serving","none",X+"path","established",X+"use"),
 ("T07","Retrieval: hybrid search, fusion, reranking","05","Context","input",X+"path",X+"path",X+"mix",X+"use"),
 ("T08","GraphRAG and knowledge graphs","06","Context","input",X+"path",X+"path","emerging",X+"use"),
 ("T09","Agent memory","06","Context","input",X+"path",X+"path","emerging",X+"use"),
 ("T10","MCP and other agent protocols","07","Integration",X+"two",X+"path",X+"path",X+"mix",X+"use"),
 ("T11","Agent Skills","07","Integration*",X+"two","none","free","emerging",X+"use"),
 ("T12","The agent loop","08","Control","control flow",X+"path",X+"path","established",X+"use"),
 ("T13","Harness: the agent's working environment","08","Control*","environment",X+"path",X+"path","emerging",X+"use"),
 ("T14","Sandboxing","08","Integration","environment","laptop",X+"path","established",X+"use"),
 ("T15","Computer use","08","Integration",X+"two",X+"path",X+"path","emerging",X+"use"),
 ("T16","Workflows and durable execution","09","Control","control flow","laptop",X+"path","established",X+"use"),
 ("T17","Multi-agent systems and frameworks","09","Control","control flow",X+"path",X+"path",X+"mix",X+"use"),
 ("T18","Human-in-the-loop","09","Control","control flow","none",X+"use","established",X+"use"),
 ("T19","Prompt injection and excessive agency","10",X+"cuts across",X+"mix","none","free",X+"mix",X+"use"),
 ("T20","Guardrails and safety classifiers","10","Control*",X+"two",X+"path",X+"path",X+"mix",X+"use"),
 ("T21","Privacy and compliance","10",X+"cuts across",X+"mix","none",X+"use",X+"mix",X+"use"),
 ("T22","Licences and data governance","10",X+"cuts across",X+"none","none",X+"mix",X+"mix",X+"use"),
 ("T23","Serving engines","11","Runtime","serving",X+"path",X+"path","established",X+"use"),
 ("T24","Local models and quantization","11","Runtime*",X+"two",X+"path",X+"path","established",X+"use"),
 ("T25","Hardware","11","Compute",X+"none",X+"none",X+"path","established",X+"use"),
 ("T26","Choosing a model","12","Model","model",X+"path",X+"path",X+"mix",X+"use"),
 ("T27","Fine-tuning","12","Model","model",X+"path",X+"path","established",X+"use"),
 ("T28","APIs and streaming","13","Delivery","serving","laptop",X+"path","established",X+"use"),
 ("T29","Observability and tracing","13",X+"cuts across","measurement",X+"path",X+"path",X+"mix",X+"use"),
 ("T30","Cost and latency","13",X+"cuts across",X+"mix",X+"path",X+"path",X+"mix",X+"use"),
]
axes = ["Layer","What it changes","Hardware","Cost","Maturity","Risk"]
def cell(v): return "✗ "+v[2:] if v.startswith(X) else v
lines = ["| ID | Topic | Part | " + " | ".join(axes) + " |", "|---|---|---|" + "---|"*len(axes)]
for t in topics:
    lines.append(f"| {t[0]} | {t[1]} | {t[2]} | " + " | ".join(cell(v) for v in t[3:]) + " |")
clean = [sum(1 for t in topics if not t[3+i].startswith(X)) for i in range(len(axes))]
lines.append("| | **Topics placed cleanly** | | " + " | ".join(f"**{c} of {len(topics)}**" for c in clean) + " |")
print("\n".join(lines))
print()
print("CLEAN:", dict(zip(axes, clean)))
# layer census
from collections import Counter
lay = Counter(t[3].rstrip("*") for t in topics if not t[3].startswith(X))
print("LAYERS:", dict(lay), "judgment calls:", [t[0] for t in topics if t[3].endswith("*")])
print("CROSS-CUTTING:", [t[0] for t in topics if t[3].startswith(X)])
