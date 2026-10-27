#!/usr/bin/env python3
"""Look inside a PDF before splitting it: its outline, or the lines at the top and bottom of pages.

Usage:
  python3 scripts/inspect_pdf.py outline book.pdf [--level 1] [--plan-out plan.json]
  python3 scripts/inspect_pdf.py heads book.pdf --pages 1-40 [--lines 3]
Prints JSON. Exit code 0 on success, 2 when the input is refused. Reads only the PDF and
writes only the --plan-out file. No network, no prompts.
"""
import argparse
import collections
import json
import re
import sys

from pypdf import PdfReader

LONE = re.compile(r"^(?:page\s+)?(\d{1,4})$", re.I)
LEAD = re.compile(r"^(\d{1,4})\s+\D")
TRAIL = re.compile(r"\D\s+(\d{1,4})$")
MAX_HEAD_PAGES = 200


def fail(message):
    print(json.dumps({"refused": message}))
    sys.exit(2)


def open_pdf(path):
    try:
        reader = PdfReader(path)
        if reader.is_encrypted:
            fail("the PDF is encrypted; ask for an unlocked copy")
        return reader, len(reader.pages)
    except Exception as exc:  # pypdf raises many types on a damaged or non-PDF file
        fail(f"cannot read {path} as a PDF: {exc.__class__.__name__}: {exc}")


def walk(reader, items, level, out):
    for item in items:
        if isinstance(item, list):  # a sub-list holds the children of the entry before it
            walk(reader, item, level + 1, out)
            continue
        try:
            page = reader.get_destination_page_number(item) + 1
        except Exception:
            page = 0
        out.append({"level": level, "title": " ".join(str(item.title).split()),
                    "page": page if page >= 1 else None})


def bare(title):
    # the title without a leading "Chapter 3", "3.", "IV" or similar
    return re.sub(r"^\s*(?:chapter|part)?\s*[\dIVXLC]+[.:)]?\s+", "", title, flags=re.I).strip() or title


def slug(title):
    return "-".join(re.sub(r"[^a-z0-9]+", " ", bare(title).lower()).split())[:40].strip("-") or "chapter"


def heading_hint(title):
    # a phrase the chapter's first page should contain
    return " ".join(bare(title).split()[:4])


def cmd_outline(args):
    reader, n = open_pdf(args.pdf)
    entries = []
    walk(reader, reader.outline, 1, entries)
    tops = [e for e in entries if e["level"] == args.level and e["page"]]
    chapters = []
    for i, e in enumerate(tops):
        nxt = min((t["page"] for t in tops[i + 1:] if t["page"] > e["page"]), default=n + 1)
        chapters.append({"file": f"ch{i + 1:02d}-{slug(e['title'])}.pdf", "title": e["title"],
                         "first": e["page"], "last": nxt - 1, "expect_first": heading_hint(e["title"]),
                         "next_start": nxt if nxt <= n else None})
    meta = reader.metadata or {}
    plan = {"book_title": str(meta.get("/Title") or "").strip(), "front": [], "front_label": "Front pages",
            "printed_offset": None, "chapters": chapters}
    if args.plan_out:
        if not args.plan_out.endswith(".json"):
            fail("--plan-out must name a .json file")
        with open(args.plan_out, "w", encoding="utf-8") as fh:
            json.dump(plan, fh, indent=1, ensure_ascii=False)
    shown = [e for e in entries if e["level"] <= args.level + 1]
    print(json.dumps({"pdf_pages": n, "outline_entries": len(entries), "outline": shown,
                      "draft_plan": plan,
                      "note": "Draft only: set front, trim blank pages from each last, and confirm "
                              "each first page with the heads command before splitting."},
                     ensure_ascii=False, indent=1))
    return 0


def numbers(lines):
    found = []
    for line in lines:
        for pattern in (LONE, LEAD, TRAIL):
            m = pattern.search(line)
            if m:
                found.append(int(m.group(1)))
                break
    return found


def cmd_heads(args):
    reader, n = open_pdf(args.pdf)
    m = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+))?\s*", args.pages)
    if not m:
        fail("--pages must look like 12 or 5-40")
    a, b = int(m.group(1)), int(m.group(2) or m.group(1))
    if not 1 <= a <= b <= n:
        fail(f"--pages must lie inside 1-{n}")
    if b - a + 1 > MAX_HEAD_PAGES:
        fail(f"ask for at most {MAX_HEAD_PAGES} pages at a time")
    rows = []
    for p in range(a, b + 1):
        lines = [ln.strip() for ln in (reader.pages[p - 1].extract_text() or "").splitlines() if ln.strip()]
        k = args.lines
        rows.append({"pdf_page": p, "head": [ln[:90] for ln in lines[:k]],
                     "foot": [ln[:90] for ln in lines[k:][-k:]],
                     "number_candidates": numbers(lines[:2] + lines[2:][-2:]),
                     "chars": sum(len(ln) for ln in lines)})
    offsets = collections.Counter(r["pdf_page"] - c for r in rows for c in r["number_candidates"])
    best = offsets.most_common(1)
    print(json.dumps({"pdf_pages": n, "pages": rows,
                      "likely_offset": {"offset": best[0][0], "pages_agreeing": best[0][1]} if best else None},
                     ensure_ascii=False, indent=1))
    return 0


def main():
    ap = argparse.ArgumentParser(description="Inspect a PDF before splitting it.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("outline", help="outline entries and a draft plan")
    o.add_argument("pdf")
    o.add_argument("--level", type=int, default=1, help="outline level that holds the chapters")
    o.add_argument("--plan-out", help="write the draft plan to this .json file")
    h = sub.add_parser("heads", help="first and last lines of pages")
    h.add_argument("pdf")
    h.add_argument("--pages", required=True, help="a page or range, such as 5-40")
    h.add_argument("--lines", type=int, default=3, help="lines to show at each end")
    args = ap.parse_args()
    return cmd_outline(args) if args.cmd == "outline" else cmd_heads(args)


if __name__ == "__main__":
    sys.exit(main())
