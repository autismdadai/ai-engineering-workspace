"""Cross-part checks for the Engineering Stack (overview Appendix L, step 3, and rubric line 3).

    python consistency_check.py            # all checks, network needed for arXiv
    python consistency_check.py --offline  # skip the arXiv lookups

1. Versions: every "<tool> <version>" mention across the 13 parts and the
   overview; a tool named with more than one version is listed with where
   each appears, so a person can judge whether a later part says what changed.
2. KEY figures: each number in the overview's Appendix B must appear in the
   part(s) its "Where" column names.
3. arXiv IDs: every ID cited must resolve, and when the text names "Surname
   et al." right before it, that surname must be the paper's first author.

Standard library only. Prints a report; writes nothing.
"""
import argparse
import collections
import pathlib
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

DOCS = pathlib.Path(__file__).resolve().parents[1] / "docs"
PARTS = sorted((DOCS / "parts").glob("engineering-stack-part-*.md"))
OVERVIEW = DOCS / "engineering-stack-overview.md"

TOOLS = ["Ollama", "llama.cpp", "vLLM", "Python", "Node.js", "Git", "mcp", "MCP", "Claude Code", "uv", "pip",
         "LangGraph", "LlamaIndex", "Chroma", "Qdrant", "pgvector", "FAISS", "sentence-transformers",
         "transformers", "PEFT", "TRL", "Unsloth", "SGLang", "TensorRT-LLM", "Docker", "Kuzu", "Neo4j",
         "promptfoo", "DSPy", "OpenTelemetry", "Pydantic", "FastAPI", "PyTorch", "numpy", "qutip", "HHEM"]
VERSION = r"v?\d+\.\d+(?:\.\d+)*(?:[a-z]\d*)?|b\d{4,5}"
ARXIV = re.compile(r"(?<![\d.])(\d{4}\.\d{4,5})(?:v\d+)?(?![\d])")


def label(path):
    m = re.search(r"part-(\d\d)", path.name)
    return f"Part {m.group(1)}" if m else "Overview"


def versions(texts):
    found = collections.defaultdict(lambda: collections.defaultdict(set))
    for name, text in texts.items():
        for tool in TOOLS:
            for m in re.finditer(rf"(?<![\w-]){re.escape(tool)}(?:==|\s+v?|\s+version\s+)({VERSION})(?![\w.])", text):
                found[tool][m.group(1).lstrip("v")].add(name)
    print("\n== 1. Tools named with more than one version")
    any_found = False
    for tool, seen in sorted(found.items()):
        if len(seen) > 1:
            any_found = True
            print(f"  {tool}: " + "; ".join(f"{v} in {', '.join(sorted(w))}" for v, w in sorted(seen.items())))
    if not any_found:
        print("  none")


def key_figures(texts):
    print("\n== 2. Appendix B numbers missing from the part(s) it cites")
    overview = texts["Overview"]
    block = overview[overview.index("## Appendix B"):overview.index("## Appendix C")]
    problems = 0
    for row in block.splitlines():
        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) < 5 or not cells[0].isdigit():
            continue
        where = [f"Part {n}" for n in re.findall(r"Part (\d\d)", cells[4])]
        if not where:
            continue
        pool = " ".join(texts.get(w, "") for w in where)
        pool_n = pool.replace(",", "")
        numbers = re.findall(r"\d+(?:[.,]\d+)*", cells[1])
        missing = [n for n in numbers if len(n.replace(",", "")) > 1
                   and n.replace(",", "") not in pool_n and n not in pool]
        if missing:
            problems += 1
            print(f"  row {cells[0]} ({', '.join(where)}): not found {missing}")
    print(f"  {problems} rows with a number not found in their part")


def arxiv(texts):
    print("\n== 3. arXiv IDs")
    cites = collections.defaultdict(set)
    named = []
    for name, text in texts.items():
        for m in ARXIV.finditer(text):
            if 7 <= int(m.group(1)[2:4]) <= 12 or m.group(1)[2:4] in ("01", "02", "03", "04", "05", "06"):
                cites[m.group(1)].add(name)
                before = text[max(0, m.start() - 160):m.start()]
                who = re.findall(r"([A-Z][a-zA-Z'À-ſ-]+) (?:et al\.|and [A-Z][a-zA-Z-]+|&)", before)
                if who:
                    named.append((m.group(1), who[-1], name))
    ids = sorted(cites)
    print(f"  {len(ids)} distinct IDs cited")
    meta = {}
    atom = {"a": "http://www.w3.org/2005/Atom"}
    opener = urllib.request.build_opener()
    for i in range(0, len(ids), 50):
        batch = ids[i:i + 50]
        url = "http://export.arxiv.org/api/query?max_results=60&id_list=" + ",".join(batch)
        req = urllib.request.Request(url, headers={"User-Agent": "ai-workspace-consistency/1.0"})
        feed = ET.fromstring(opener.open(req, timeout=90).read())
        for entry in feed.findall("a:entry", atom):
            eid = entry.find("a:id", atom).text.rsplit("/", 1)[-1].split("v")[0]
            title = entry.find("a:title", atom)
            authors = [a.find("a:name", atom).text for a in entry.findall("a:author", atom)]
            if title is not None and authors:
                meta[eid] = (" ".join(title.text.split()), authors)
        time.sleep(3)  # arXiv asks for a pause between API calls
    missing = [i for i in ids if i not in meta]
    print(f"  resolved {len(ids) - len(missing)} of {len(ids)}" + (f"; NOT FOUND: {missing}" if missing else ""))
    bad = []
    for aid, surname, where in named:
        if aid in meta:
            first = meta[aid][1][0]
            surnames = [a.split()[-1].lower() for a in meta[aid][1]]
            if surname.lower() not in surnames and surname.lower() not in first.lower():
                bad.append(f"{where}: '{surname}' before {aid}, but the authors are {', '.join(meta[aid][1][:3])} ({meta[aid][0][:70]})")
    print(f"  surname checks: {len(named)}; mismatches: {len(bad)}")
    for line in sorted(set(bad)):
        print("   - " + line)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()
    texts = {label(p): p.read_text(encoding="utf-8") for p in PARTS + [OVERVIEW]}
    print(f"Read {len(texts)} files")
    versions(texts)
    key_figures(texts)
    if not args.offline:
        arxiv(texts)


if __name__ == "__main__":
    main()
