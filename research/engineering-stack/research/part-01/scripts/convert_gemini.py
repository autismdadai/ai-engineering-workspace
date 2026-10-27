"""Convert the Gemini 'Modern AI Engineering Stack' PDF to Markdown.

Keeps headings (by font size), bold and italic runs, the 16 two-column
tables (merged across page breaks, repeated header rows dropped), the
LaTeX formulas exactly as printed, and the 33 works cited as a list.
Usage: python3 -I convert_gemini.py <pdf> <out.md>
"""
import re
import sys

import pdfplumber

HEAD = {24.0: "#", 18.0: "##", 14.0: "###", 12.0: "##"}
RIGHT = 540.0  # right text edge on a letter page with 1-inch margins; refined at run time
HEADER_ROW = ("Implementation Dimension", "Real-World Examples & Structured Curriculum")


def style(word):
    f = word["fontname"]
    return ("b" if "Bold" in f else "") + ("i" if "Italic" in f else "")


def runs_to_md(seq):
    """Join (word, separator) pairs into Markdown, wrapping bold and italic runs."""
    segs = []
    for w, sep in seq:
        st = style(w)
        st = "b" if "b" in st else ("i" if "i" in st else "")
        if segs and segs[-1][0] == st:
            segs[-1][1].append((w["text"], sep))
        else:
            segs.append([st, [(w["text"], sep)]])
    out = []
    for st, items in segs:
        text = "".join(t + s for t, s in items[:-1]) + items[-1][0]
        trail = items[-1][1]
        if st == "b":
            text = f"**{text}**"
        elif st == "i":
            text = f"*{text}*"
        out.append(text + trail)
    return re.sub(r"[ \t]+", " ", "".join(out)).strip()


def lines_of(words, tol=2.5):
    lines = []
    for w in sorted(words, key=lambda w: (round(w["top"]), w["x0"])):
        if lines and abs(lines[-1][0]["top"] - w["top"]) <= tol:
            lines[-1].append(w)
        else:
            lines.append([w])
    return [sorted(l, key=lambda w: w["x0"]) for l in lines]


def with_seps(lines):
    """Flatten lines into (word, separator) pairs; no space after a line-final hyphen or URL piece."""
    seq = []
    for li, line in enumerate(lines):
        for wi, w in enumerate(line):
            last_in_line = wi == len(line) - 1
            if not last_in_line:
                seq.append((w, " "))
            else:
                t = w["text"]
                joins = t.endswith("-") and not t.endswith(" -") and len(t) > 1
                joins = joins or ("http" in t and li + 1 < len(lines)
                                  and not re.match(r"^\d{1,2}\.$", lines[li + 1][0]["text"]))
                seq.append((w, "" if joins else " "))
    return seq


def page_blocks(page):
    tables = page.find_tables()
    tboxes = [t.bbox for t in tables]

    def in_table(w):
        cx, cy = (w["x0"] + w["x1"]) / 2, (w["top"] + w["bottom"]) / 2
        return any(b[0] - 1 <= cx <= b[2] + 1 and b[1] - 1 <= cy <= b[3] + 1 for b in tboxes)

    words = page.extract_words(extra_attrs=["fontname", "size"], use_text_flow=False, x_tolerance=1.5)
    body = [w for w in words if not in_table(w)]
    blocks = []
    right = RIGHT
    for line in lines_of(body):
        size = round(line[0]["size"], 1)
        blocks.append(("line", line[0]["top"], line, size, right))
    for t in tables:
        rows = []
        for r in t.rows:
            cells = []
            for c in r.cells:
                if c is None:
                    cells.append("")
                    continue
                cw = page.within_bbox(c).extract_words(extra_attrs=["fontname", "size"], x_tolerance=1.5)
                cells.append(runs_to_md(with_seps(lines_of(cw))))
            rows.append(cells)
        blocks.append(("table", t.bbox[1], rows, None, None))
    return sorted(blocks, key=lambda b: b[1])


def convert(pdf_path):
    global RIGHT
    with pdfplumber.open(pdf_path) as pdf:
        xs = sorted(w["x1"] for p in pdf.pages for w in p.extract_words())
        RIGHT = xs[-1]
        stream = [b for page in pdf.pages for b in page_blocks(page)]
    out = []          # ("h", level, text, size) | ("p", [lines]) | ("t", rows)
    para = None
    for i, (kind, top, payload, size, right) in enumerate(stream):
        if kind == "table":
            para = None
            rows = payload
            if out and out[-1][0] == "t" and tuple(rows[0]) == HEADER_ROW:
                rows = rows[1:]
                prev = out[-1][1]
                if rows and rows[0][0] == "":
                    joiner = "" if prev[-1][1].endswith("-") else " "
                    prev[-1][1] = prev[-1][1] + joiner + rows[0][1]
                    rows = rows[1:]
                prev.extend([list(r) for r in rows])
            else:
                out.append(("t", [list(r) for r in rows]))
            continue
        line = payload
        if size in HEAD and all("Bold" in w["fontname"] for w in line):
            text = " ".join(w["text"] for w in line)
            if out and out[-1][0] == "h" and out[-1][3] == size and para is None:
                out[-1] = ("h", HEAD[size], out[-1][2] + " " + text, size)
            else:
                out.append(("h", HEAD[size], text, size))
            para = None
            continue
        if para is None:
            para = []
            out.append(("p", para))
        para.append(line)
        # paragraph ends if the next body line's first word would have fitted on this line
        nxt = stream[i + 1] if i + 1 < len(stream) else None
        if nxt is None or nxt[0] != "line" or (nxt[3] in HEAD and all("Bold" in w["fontname"] for w in nxt[2])):
            para = None
        else:
            w0 = nxt[2][0]
            if line[-1]["x1"] + 3.5 + (w0["x1"] - w0["x0"]) < RIGHT:
                para = None
    md = []
    for item in out:
        if item[0] == "h":
            md.append(f"{item[1]} {item[2]}")
        elif item[0] == "p":
            md.append(runs_to_md(with_seps(item[1])))
        else:
            rows = item[1]
            md.append("| " + " | ".join(rows[0]) + " |")
            md.append("|---|---|")
            for r in rows[1:]:
                md.append("| " + " | ".join(c.replace("|", "\\|") for c in r) + " |")
        md.append("")
    return "\n".join(md)


if __name__ == "__main__":
    text = convert(sys.argv[1])
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        fh.write(text)
    print(len(text.split()), "words written")
