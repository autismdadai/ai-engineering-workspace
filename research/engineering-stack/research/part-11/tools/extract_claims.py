"""Make blind-check claim lists from the Part 11 draft: every unit (sentence,
bullet or table row) with a [V: KEY] tag, all tags stripped, plus the source
rows its keys point to. Writes claims-A.md and claims-B.md split by section."""
import re
import pathlib

PART = pathlib.Path("/home/claude/part11/engineering-stack-part-11-running-models.md")
OUT = pathlib.Path("/home/claude/part11/phase4")
text = PART.read_text(encoding="utf-8")
body = text[text.index("## 1. In plain words"):text.index("## 12. Sources")]
sources_md = text[text.index("## 12. Sources"):text.index("## Run on your computer")]
SRC = {}
for line in sources_md.splitlines():
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) == 5 and re.fullmatch(r"[A-Z0-9]{2,5}", cells[0]):
        SRC[cells[0]] = f"{cells[1]} (class {cells[2]})"
TAG = re.compile(r"\[(V|T|R|U|I)(?::([^\]]*))?\]")

def units(section_text):
    """Yield (text, extra_keys). Table rows without their own [V] tags take the
    keys of a tag line right after the table."""
    lines = section_text.splitlines()
    in_code = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            in_code = not in_code
            i += 1
            continue
        if in_code or not line.strip():
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not lines[i].startswith("|---"):
                    rows.append(lines[i])
                i += 1
            j = i
            while j < len(lines) and not lines[j].strip():
                j += 1
            after = lines[j] if j < len(lines) else ""
            extra = []
            if after.lstrip().startswith(("[V", "Sources")):
                for t in TAG.finditer(after.split(")")[0] + ")" if after.startswith("[V") else after):
                    if t.group(1) == "V":
                        extra += [k.strip() for k in t.group(2).split(",")]
            for r in rows[1:]:          # skip the header row
                yield r, extra
            continue
        for piece in re.split(r"(?<=[.!?])(?:\s*\[[^\]]*\])*\s+(?=[A-Z*\"(])", line):
            yield piece, []
        i += 1


def sections(body):
    parts = re.split(r"\n(?=## \d+\. |### \d+\.\d+ )", body)
    for p in parts:
        head = p.strip().splitlines()[0]
        yield head, p

claims = []
for head, sec in sections(body):
    m = re.match(r"#+ (\d+)(?:\.(\d+))?", head)
    num = f"{m.group(1)}.{m.group(2)}" if m.group(2) else m.group(1)
    for u, extra in units(sec):
        keys = list(extra)
        for t in TAG.finditer(u):
            if t.group(1) == "V":
                keys += [k.strip() for k in t.group(2).split(",")]
        if not keys:
            continue
        clean = TAG.sub("", u).strip(" |")
        clean = re.sub(r"\s*\|\s*", " | ", clean)
        claims.append((num, clean, sorted(set(keys))))

def write(name, chosen, label):
    lines = [f"# Blind check, list {label}", "",
             "Each claim below comes with the keys of the sources it rests on; the source list follows.", ""]
    used = set()
    for i, (num, clean, keys) in enumerate(chosen, 1):
        lines.append(f"{label}{i:03d}. {clean}  [sources: {', '.join(keys)}]")
        used.update(keys)
    lines += ["", "## Sources", ""]
    for k in sorted(used):
        lines.append(f"- {k}: {SRC.get(k, 'MISSING')}")
    (OUT / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(chosen), sorted(k for k in used if k not in SRC)

first = {"1", "2", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8"}
A = [c for c in claims if c[0] in first]
B = [c for c in claims if c[0] not in first]
print("A", write("claims-A.md", A, "A"))
print("B", write("claims-B.md", B, "B"))
print("total", len(claims), "sources", len(SRC))
