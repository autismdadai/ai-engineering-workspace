"""Assemble Part 11 from its section files and the lab's core file; count tags."""
import pathlib
import re
import sys

DRAFT = pathlib.Path("/home/claude/part11/draft")
LAB = pathlib.Path("/home/claude/part11/lab/engineering-stack-lab-part-11")
OUT = pathlib.Path("/home/claude/part11/engineering-stack-part-11-running-models.md")
ORDER = ["s01", "s03", "s04", "s06", "s08", "s10", "s12", "checks", "cheat"]
TAG = re.compile(r"\[(V|T|R|U|I)(?::[^\]]*)?\]")

parts = [(DRAFT / f"{name}.md").read_text(encoding="utf-8").strip() for name in ORDER]
appendix = ("## Appendix: lab listing\n\nThe core file of the lab folder `engineering-stack-lab-part-11`, "
            "as tested: the arithmetic itself. `run_lab.py`, `mutation_check.py`, `demo.py`, "
            "`reader_local.py` and `README.md` are in the zip (Section 8).\n\n### runmath.py\n\n```python\n"
            + (LAB / "runmath.py").read_text(encoding="utf-8").rstrip() + "\n```")
text = "\n\n".join(parts + [appendix]) + "\n"

body = text[text.index("## 1. In plain words"):text.index("## Cheat sheet")]
counts = {k: 0 for k in "VTRUI"}
for m in TAG.finditer(body):
    counts[m.group(1)] += 1
summary = ", ".join(f"{counts[k]} [{k}]" for k in "VTRUI")
text = text.replace("TAGCOUNTS", summary)
OUT.write_text(text, encoding="utf-8")

size = len(text.encode("utf-8"))
dashes = len(re.findall("[—–]", text))
print(f"{OUT.name}: {size:,} bytes ({size / 1024:.1f} KB); tags {summary}; em or en dashes: {dashes}")
sys.exit(0 if size <= 100 * 1024 and dashes == 0 else 1)
