"""Post-process the converted Gemini Markdown: wrap the LaTeX formulas in $...$,
split the works cited into a numbered list, and add the provenance header."""
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
md = open(src, encoding="utf-8").read()

FORMULAS = [
    r"P(\text{output} \mid \text{context})",
    r"O(N^2)",
    r"[A][B] \dots [A] \to [B]",
    r"\text{score} = \sum \frac{1}{k + \text{rank}(d)}",
    r"score(Q, D) = \sum_{i=1}^{L_q} \max_{j=1}^{L_d} \langle Q_i, D_j \rangle",
    r"H = - \sum p(C_k) \log p(C_k)",
    r"(M_q)",
    r"(\gamma)",
    r"(M_p)",
]
for f in FORMULAS:
    n = md.count(f)
    if n != 1:
        sys.exit(f"formula not found exactly once ({n}): {f}")
    if f.startswith("(") and f.endswith(")") and f not in (r"O(N^2)",):
        md = md.replace(f, "($" + f[1:-1] + "$)")
    else:
        md = md.replace(f, "$" + f + "$")

head, cited = md.split("## Works cited", 1)
body = " ".join(cited.split())
entries, pos = [], 0
for n in range(1, 34):
    tag = f"{n}. "
    start = body.find(tag, pos) if n == 1 else body.find(" " + tag, pos)
    if start < 0:
        sys.exit(f"works-cited entry {n} not found")
    if n > 1:
        entries[-1] = body[entries_start:start].strip()
        start += 1
    entries_start = start
    entries.append(None)
    pos = start + len(tag)
entries[-1] = body[entries_start:].strip()
assert len(entries) == 33 and all(e.startswith(f"{i}. ") for i, e in enumerate(entries, 1))
cited_md = "\n".join(entries) + "\n"

header = """<!--
Converted from "Modern AI Engineering Stack Analysis 11.PDF" (18 pages; Google Docs export; made with Gemini Deep Research).
-->

> **Source class: AI-written synthesis (the lowest trust class in this project).** Treat every statement below as a claim to check, not as evidence. Each claim is checked in `claude/engineering-stack-claim-ledger.md`; read that before quoting anything here.
>
> **Conversion notes (October 9, 2026).** Text, headings, bold and italic runs are as printed. The formulas were printed as raw LaTeX source; they are unchanged here, only wrapped in `$...$` so Markdown renders them. Each pillar's table was rebuilt from the PDF's ruled tables and checked against the page images; header rows repeated at page breaks were dropped and split cells re-joined. The PDF has no inline citation markers and no links, so the works cited below are matched to claims by topic in the ledger (marked "inferred"). The works cited were one run-on paragraph in the PDF; here they are one entry per line, with titles and URLs exactly as printed (some titles are cut short in the original).

"""
out = header + head.rstrip() + "\n\n## Works cited\n\n" + cited_md
open(dst, "w", encoding="utf-8").write(out)
print("ok", len(out.split()), "words")
