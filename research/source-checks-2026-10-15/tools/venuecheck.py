"""Look up venue claims in DBLP by title. Usage: python venuecheck.py OUT_MD"""
import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
# (works-cited number, venue the manual states, title to search)
CLAIMS = [
    (12, "Findings of EMNLP 2024", "When A Helpful Assistant Is Not Really Helpful Personas in System Prompts"),
    (32, "AAAI 2024", "Graph of Thoughts: Solving Elaborate Problems with Large Language Models"),
    (37, "ICLR 2024", "Skeleton-of-Thought"),
    (39, "ICML 2025 (PMLR v267)", "Mind Your Step (by Step): Chain-of-Thought can Reduce Performance"),
    (51, "Findings of ACL 2024", "Revisiting OPRO: The Limitations of Small-Scale LLMs as Optimizers"),
    (58, "ICLR 2026 (Oral)", "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning"),
    (59, "NAACL 2025", "Local Prompt Optimization"),
    (68, "NAACL 2025", "Adaptive Prompting: Ad-hoc Prompt Composition for Social Bias Detection"),
    (77, "NeurIPS 2024", "LLM Evaluators Recognize and Favor Their Own Generations"),
    (80, "ICLR 2024", "Large Language Models Cannot Self-Correct Reasoning Yet"),
    (87, "NeurIPS 2025", "Why Do Some Language Models Fake Alignment While Others Don't"),
    (111, "COLM 2024", "RULER: What's the Real Context Size of Your Long-Context Language Models"),
    (112, "ICML 2025", "NoLiMa: Long-Context Evaluation Beyond Literal Matching"),
    (119, "NeurIPS 2024 Datasets and Benchmarks", "A Careful Examination of Large Language Model Performance on Grade School Arithmetic"),
    (122, "Findings of EMNLP 2024", "The Effect of Sampling Temperature on Problem Solving in Large Language Models"),
    (125, "TACL 2023", "In-Context Retrieval-Augmented Language Models"),
    (128, "ICLR 2025", "When LLMs Play the Telephone Game"),
    (132, "USENIX Security 2025", "StruQ: Defending Against Prompt Injection with Structured Queries"),
    (116, "PMLR 203 (2023)", "Can Large Language Models Truly Understand Prompts? A Case Study with Negated Prompts"),
    (53, "EMNLP 2023 (per Ch. 27.2)", "Automatic Prompt Optimization with Gradient Descent and Beam Search"),
]


def get(url):
    # curl uses the Windows certificate store; Python's bundled store rejects dblp.org's chain here
    for attempt in range(3):
        r = subprocess.run(["curl", "-sS", "-m", "40", "-A", "venuecheck/1.0 (personal citation audit)", url],
                           capture_output=True)
        if r.returncode == 0 and r.stdout:
            try:
                return json.loads(r.stdout)
            except ValueError:
                pass
        print("retry", attempt, r.stderr[:200], file=sys.stderr)
        time.sleep(5 * (attempt + 1))
    return None


out = ["| # | manual says | DBLP records (venue, year, title) |", "|---|---|---|"]
for n, claimed, title in CLAIMS:
    data = get("https://dblp.org/search/publ/api?" + urllib.parse.urlencode({"q": title, "format": "json", "h": 6}))
    hits = ((data or {}).get("result", {}).get("hits", {}) or {}).get("hit", []) or []
    recs = []
    for h in hits:
        i = h.get("info", {})
        recs.append(f"{i.get('venue')} {i.get('year')} [{i.get('type', '')}]: {str(i.get('title'))[:70]}")
    line = f"| {n} | {claimed} | " + "<br>".join(recs or ["no DBLP hit"]) + " |"
    out.append(line)
    print(line)
    time.sleep(1.5)
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(out) + "\n")
