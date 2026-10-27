"""Extract [V]-tagged claims from the assembled part into two checker lists."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
doc = (ROOT / "engineering-stack-part-09-workflows-and-multi-agent.md").read_text(encoding="utf-8")
body = doc.split("## 1. In plain words")[1].split("## 12. Sources")[0]
body = "## 1. In plain words" + body
sources_md = doc.split("## 12. Sources")[1].split("## Run on your computer")[0]

sources = {}
for line in sources_md.splitlines():
    m = re.match(r"\| (\w+) \| (.*?) \| (\w+) \| (.*?) \| (\d+) \|", line)
    if m:
        sources[m.group(1)] = f"- **{m.group(1)}** ({m.group(3)}): {m.group(2)}"

claims = []
section = ""
in_code = False
for raw in body.splitlines():
    line = raw.strip()
    if line.startswith("```"):
        in_code = not in_code
        continue
    if in_code or not line:
        continue
    if line.startswith("#"):
        section = line.lstrip("#").strip()
        continue
    if "[V:" not in line:
        continue
    if line.startswith("|"):
        pieces = [line]
    else:
        pieces = re.split(r"(?<=[.!?\]])\s+(?=[A-Z*\"(`])", line)
    for piece in pieces:
        keys = re.findall(r"\[V: ([^\]]+)\]", piece)
        if not keys:
            continue
        found = sorted({k.strip() for group in keys for k in group.split(",")})
        text = re.sub(r"\[(V|T|R|U|I)(:[^\]]*)?\]", "", piece).strip()
        claims.append((section, text, found))

split_at = next(i for i, c in enumerate(claims) if c[0].startswith("3.7"))
sets = {"A": claims[:split_at], "B": claims[split_at:]}
for name, items in sets.items():
    used = sorted({k for _, _, keys in items for k in keys})
    lines = [f"# Claims to check, set {name}", "", "## Sources (key, class: citation with URL)", ""]
    lines += [sources.get(k, f"- **{k}**: (no entry in Section 12)") for k in used]
    lines += ["", "## Claims", ""]
    for i, (sec, text, keys) in enumerate(items, 1):
        lines.append(f"{name}{i:03d}. [{sec}] {text}  SOURCES: {', '.join(keys)}")
    (ROOT / "phase4" / f"claims-{name}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    missing = [k for k in used if k not in sources]
    print(name, len(items), "claims,", len(used), "sources", "MISSING:" if missing else "", missing or "")
