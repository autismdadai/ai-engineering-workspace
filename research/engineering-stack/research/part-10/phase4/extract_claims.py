"""Make blind claim lists from the Part 10 draft (Phase 4).

Each claim is a sentence or table row that carries a [V: ...] tag, with every
tag stripped, plus the source rows it cites. The checkers never see the draft
itself, the tags or the lead's reasoning.
"""
import re

DRAFT = "/home/claude/part10/draft/engineering-stack-part-10-security.md"
OUT = "/home/claude/part10/phase4/"

text = open(DRAFT, encoding="utf-8").read()
sources_block = text[text.index("## 12. Sources"):text.index("## Run on your computer")]
SOURCES = {}
for line in sources_block.splitlines():
    m = re.match(r"^\| ([A-Z0-9]{2,5}) \| (.+?) \| ([A-Z]{2}) \|", line)
    if m:
        SOURCES[m.group(1)] = f"{m.group(2)} [class {m.group(3)}]"

body = text[text.index("## 1. In plain words"):text.index("## 12. Sources")]
TAG = re.compile(r"\[(?:V|T|R|U|I)(?::[^\]]*)?\]|\[T on [^\]]*\]")


def units(section_text):
    """Split into table rows and sentences."""
    for line in section_text.splitlines():
        if line.startswith("|") and "[V:" in line:
            yield line
        elif "[V:" in line:
            for sentence in re.split(r"(?<=[.;])\s+(?=[A-Z*(])", line):
                if "[V:" in sentence:
                    yield sentence


def section_of(pos):
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"^#{2,3} (\d+(?:\.\d+)?)", body, re.M)]
    current = "?"
    for start, num in heads:
        if start <= pos:
            current = num
    return current


groups = {"A": [], "B": []}
B_SECTIONS = {"3.6", "3.7", "3.8", "3.9", "3.10", "3.11", "6", "10"}
for m in re.finditer(r"^#{2,3} \d.*$", body, re.M):
    pass
blocks = re.split(r"(?=^#{2,3} \d)", body, flags=re.M)
for block in blocks:
    head = re.match(r"#{2,3} (\d+(?:\.\d+)?)", block)
    if not head:
        continue
    sec = head.group(1)
    group = "B" if sec in B_SECTIONS else "A"
    if sec in ("4",):
        group = "A"
    for unit in units(block):
        keys = set()
        for g in re.findall(r"\[V: ([^\]]+)\]", unit):
            keys |= {k.strip() for k in g.split(",")}
        keys.discard("KEY")
        clean = TAG.sub("", unit).strip()
        clean = re.sub(r"\s{2,}", " ", clean)
        if keys:
            groups[group].append((sec, clean, sorted(keys)))

for name, claims in groups.items():
    used = sorted({k for _, _, ks in claims for k in ks})
    with open(f"{OUT}claims-{name}.md", "w", encoding="utf-8") as handle:
        handle.write(f"# Claims to check, list {name}\n\n")
        for i, (sec, clean, keys) in enumerate(claims, 1):
            handle.write(f"{name}{i:03}. {clean}\n    Sources: {', '.join(keys)}\n\n")
        handle.write("\n# Sources\n\n")
        for k in used:
            handle.write(f"- {k}: {SOURCES.get(k, 'MISSING')}\n")
    print(name, len(claims), "claims,", len(used), "sources")
