#!/usr/bin/env python3
"""Split a PDF into chapter files from a plan, then check every page against the original.

Usage: python3 scripts/split_book.py plan.json book.pdf out_dir [--max-pages 100]
Refuses a bad plan before writing anything (see SKILL.md). Prints JSON. Exit code 0 when
every check passes, 1 when a check fails (files written; see the report), 2 when the plan
or input is refused (nothing written). Writes only inside out_dir. No network, no prompts.
"""
import argparse
import hashlib
import json
import os
import re
import sys

from pypdf import PdfReader, PdfWriter

NAME = re.compile(r"^[a-z0-9][a-z0-9-]{0,80}\.pdf$")


def refuse(problems):
    print(json.dumps({"refused": problems, "written": []}, ensure_ascii=False, indent=1))
    sys.exit(2)


def squash(text):
    return " ".join(text.split()).lower()


def page_text(reader, index):
    return reader.pages[index].extract_text() or ""


def is_page(value, n):
    return type(value) is int and 1 <= value <= n


def outline_entries(reader):
    found = []

    def walk(items, level):
        for item in items:
            if isinstance(item, list):
                walk(item, level + 1)
                continue
            try:
                found.append((level, " ".join(str(item.title).split()), reader.get_destination_page_number(item) + 1))
            except Exception:
                pass

    walk(reader.outline, 1)
    return found


def check_plan(plan, n, max_pages):
    problems, warnings = [], []
    front = plan.get("front", [])
    if not isinstance(front, list) or not all(is_page(p, n) for p in front):
        problems.append(f"front must be a list of page numbers from 1 to {n}")
        front = []
    chapters = plan.get("chapters")
    if not isinstance(chapters, list) or not chapters:
        return problems + ["the plan has no chapters"], warnings
    names, spans = set(), []
    for k, ch in enumerate(chapters, 1):
        if not isinstance(ch, dict):
            problems.append(f"chapter {k}: must be an object with file, first and last")
            continue
        name, first, last = ch.get("file"), ch.get("first"), ch.get("last")
        where = f"chapter {k} ({name})"
        if not isinstance(name, str) or not NAME.match(name):
            problems.append(f"{where}: the file name must be lowercase letters, digits and hyphens "
                            "ending in .pdf, with no folder in it")
        elif name in names:
            problems.append(f"{where}: the file name is used twice")
        names.add(name)
        if not (is_page(first, n) and is_page(last, n) and first <= last):
            problems.append(f"{where}: first and last must be page numbers with 1 <= first <= last <= {n}")
            continue
        size = len(front) + last - first + 1
        if size > max_pages:
            problems.append(f"{where}: {size} pages with the front pages, over the {max_pages}-page limit; "
                            "split it at a section start, or raise --max-pages if text-only reading is fine")
        spans.append((first, last, name))
    spans.sort()
    for (a1, b1, f1), (a2, b2, f2) in zip(spans, spans[1:]):
        if a2 <= b1:
            warnings.append(f"{f1} and {f2} overlap on pages {a2} to {min(b1, b2)}")
    return problems, warnings


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description="Split a PDF into checked chapter files.")
    ap.add_argument("plan")
    ap.add_argument("pdf")
    ap.add_argument("out_dir")
    ap.add_argument("--max-pages", type=int, default=100, help="largest file allowed, front pages included")
    args = ap.parse_args()
    try:
        with open(args.plan, encoding="utf-8") as fh:
            plan = json.load(fh)
    except (OSError, ValueError) as exc:
        refuse([f"cannot read the plan: {exc}"])
    if not isinstance(plan, dict):
        refuse(["the plan must be a JSON object"])
    try:
        src = PdfReader(args.pdf)
        if src.is_encrypted:
            refuse(["the PDF is encrypted; ask for an unlocked copy"])
        n = len(src.pages)
    except Exception as exc:  # pypdf raises many types on a damaged or non-PDF file
        refuse([f"cannot read {args.pdf} as a PDF: {exc.__class__.__name__}: {exc}"])
    problems, warnings = check_plan(plan, n, args.max_pages)
    if problems:
        refuse(problems)

    os.makedirs(args.out_dir, exist_ok=True)
    front = plan.get("front", [])
    label = plan.get("front_label") or "Front pages"
    book = str(plan.get("book_title") or "").strip()
    offset = plan.get("printed_offset")
    toc = outline_entries(src)
    files, all_ok = [], True
    for ch in plan["chapters"]:
        first, last = ch["first"], ch["last"]
        title = str(ch.get("title") or ch["file"][:-4])
        page_map = list(front) + list(range(first, last + 1))
        nf = len(front)
        writer = PdfWriter()
        for p in page_map:
            writer.add_page(src.pages[p - 1])
        if nf:
            writer.add_outline_item(label, 0)
        top = writer.add_outline_item(title, nf)
        for _level, entry, p in toc:
            if first < p <= last:
                writer.add_outline_item(entry, nf + p - first, parent=top)
        printed = f" (printed pages {first - offset} to {last - offset})" if type(offset) is int else ""
        writer.add_metadata({
            "/Title": f"{book}: {title}" if book else title,
            "/Subject": f"{title}: PDF pages {first} to {last} of the full book{printed}, "
                        f"after {nf} front page(s). Page content unchanged.",
            "/Creator": "book-chapter-splitter split_book.py (pypdf)",
        })
        path = os.path.join(args.out_dir, ch["file"])
        with open(path, "wb") as fh:
            writer.write(fh)

        out = PdfReader(path)
        texts = [page_text(out, i) for i in range(len(out.pages))]
        mismatched = [i + 1 for i, p in enumerate(page_map)
                      if i >= len(texts) or texts[i] != page_text(src, p - 1)]
        expect = ch.get("expect_first")
        heading = None
        if expect:
            heading = nf < len(texts) and squash(str(expect)) in squash(texts[nf])
        next_head = None
        if last < n:
            lines = [ln.strip() for ln in page_text(src, last).splitlines() if ln.strip()]
            next_head = " / ".join(lines[:3])[:120] or "(no text: a blank or image-only page)"
        ok = len(out.pages) == len(page_map) and not mismatched and heading is not False
        all_ok &= ok
        files.append({
            "file": ch["file"], "title": title, "pdf_pages": f"{first}-{last}",
            "printed_pages": f"{first - offset}-{last - offset}" if type(offset) is int else None,
            "pages": len(out.pages), "expected_pages": len(page_map),
            "text_mismatch_pages": mismatched, "pages_without_text": sum(1 for t in texts if not t.strip()),
            "first_heading_found": heading, "next_page_head": next_head,
            "outline_entries": len(out.outline), "bytes": os.path.getsize(path), "sha256": sha256(path),
            "ok": ok,
        })
    print(json.dumps({"all_ok": all_ok, "source_pages": n, "max_pages": args.max_pages,
                      "warnings": warnings, "files": files}, ensure_ascii=False, indent=1))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
