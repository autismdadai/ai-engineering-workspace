#!/usr/bin/env python3
"""Build the 160-page sample book the tests split. Nothing in it comes from a real book.

Usage: python evals/make_fixture.py out.pdf [--encrypted out-locked.pdf]

Layout (PDF page = printed page + 2):
  1-2      title and license pages
  3-12     Chapter 1, Alpha Basics        (sections 1.1 at 3, 1.2 at 8)
  13-30    Chapter 2, Beta Methods        (section 2.1 at 20)
  31-150   Chapter 3, Gamma Long Chapter  (sections 3.1 at 31, 3.2 at 90): 120 pages
  151      blank page
  152-160  Chapter 4, Delta Ending
Even printed pages carry the number before the running head, odd ones after it, and a
chapter's first page carries it alone on the last line. Every page has a unique marker.
The page tree holds the font and page size, so pages inherit them, as in many real PDFs.
"""
import argparse
import io
import sys

from pypdf import PdfReader, PdfWriter

CHAPTERS = [(1, "Alpha Basics", 3, 12), (2, "Beta Methods", 13, 30),
            (3, "Gamma Long Chapter", 31, 150), (4, "Delta Ending", 152, 160)]
SECTIONS = {1: [("1.1 First Section", 3), ("1.2 Second Section", 8)], 2: [("2.1 Only Section", 20)],
            3: [("3.1 Part One", 31), ("3.2 Part Two", 90)], 4: []}
TOTAL, OFFSET, BLANK = 160, 2, {151}


def page_lines(p):
    if p == 1:
        return ["SAMPLE BOOK OF TESTS", "A fixture for book-chapter-splitter"]
    if p == 2:
        return ["License page", "Free to copy for testing"]
    if p in BLANK:
        return []
    for num, title, first, last in CHAPTERS:
        if first <= p <= last:
            printed = p - OFFSET
            if p == first:
                return [f"Chapter {num}", title, f"Opening text of chapter {num}.", str(printed)]
            head = f"{printed} {title}" if printed % 2 == 0 else f"{title} {printed}"
            return [head, f"Body text of chapter {num}, page {p - first + 1}.", f"Marker c{num}p{p}."]
    raise ValueError(p)


def literal(text):
    return "(" + text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)") + ")"


def base_pdf():
    """A plain PDF written by hand, so the fixture doesn't depend on a drawing library."""
    body, page_ids, next_id = {}, [], 4
    for p in range(1, TOTAL + 1):
        pid, cid = next_id, next_id + 1
        next_id += 2
        page_ids.append(pid)
        shows = " ".join(f"1 0 0 1 72 {720 - 18 * k} Tm {literal(line)} Tj" for k, line in enumerate(page_lines(p)))
        stream = f"BT /F1 12 Tf {shows} ET".encode("latin-1")
        body[cid] = b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream"
        body[pid] = f"<< /Type /Page /Parent 2 0 R /Contents {cid} 0 R >>".encode()
    body[1] = b"<< /Type /Catalog /Pages 2 0 R >>"
    kids = " ".join(f"{p} 0 R" for p in page_ids)
    body[2] = (f"<< /Type /Pages /Kids [{kids}] /Count {TOTAL} /MediaBox [0 0 612 792] "
               "/Resources << /Font << /F1 3 0 R >> >> >>").encode()
    body[3] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
    out, offsets = bytearray(b"%PDF-1.4\n"), {}
    for i in range(1, next_id):
        offsets[i] = len(out)
        out += f"{i} 0 obj\n".encode() + body[i] + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {next_id}\n0000000000 65535 f \n".encode()
    out += "".join(f"{offsets[i]:010d} 00000 n \n" for i in range(1, next_id)).encode()
    out += f"trailer\n<< /Size {next_id} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return bytes(out)


def build(path, locked_path=None):
    writer = PdfWriter(clone_from=PdfReader(io.BytesIO(base_pdf())))
    for num, title, first, _last in CHAPTERS:
        parent = writer.add_outline_item(f"{num} {title}", first - 1)
        for name, page in SECTIONS[num]:
            writer.add_outline_item(name, page - 1, parent=parent)
    writer.add_metadata({"/Title": "Sample Book of Tests"})
    with open(path, "wb") as fh:
        writer.write(fh)
    if locked_path:
        locked = PdfWriter(clone_from=PdfReader(path))
        locked.encrypt(user_password="pw", owner_password="pw", algorithm="RC4-128")
        with open(locked_path, "wb") as fh:
            locked.write(fh)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build the sample book.")
    ap.add_argument("out")
    ap.add_argument("--encrypted", help="also write a password-locked copy here")
    a = ap.parse_args()
    build(a.out, a.encrypted)
    print(f'{{"fixture": "{a.out}", "pages": {TOTAL}}}')
    sys.exit(0)
