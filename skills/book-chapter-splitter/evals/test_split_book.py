#!/usr/bin/env python3
"""Known-answer tests for book-chapter-splitter's scripts, run on the sample book that
make_fixture.py builds (nothing from a real book).

Usage: python evals/test_split_book.py [--scripts-dir DIR]
Output: one JSON line per test, then a summary. Exit code 0 when every test passes,
1 otherwise. No network; writes only to a temporary folder.
"""
import argparse
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

from pypdf import PdfReader

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_fixture  # noqa: E402  (lives next to this file)

CH1 = {"file": "sample-ch01-alpha.pdf", "title": "Chapter 1: Alpha Basics", "first": 3, "last": 12,
       "expect_first": "Alpha Basics"}
CH2 = {"file": "sample-ch02-beta.pdf", "title": "Chapter 2: Beta Methods", "first": 13, "last": 30,
       "expect_first": "Beta Methods"}
CH3 = {"file": "sample-ch03-gamma.pdf", "title": "Chapter 3: Gamma Long Chapter", "first": 31, "last": 150,
       "expect_first": "Gamma Long Chapter"}
CH4 = {"file": "sample-ch04-delta.pdf", "title": "Chapter 4: Delta Ending", "first": 152, "last": 160,
       "expect_first": "Delta Ending"}
FRONT = [1, 2]
TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


class Ctx:
    def __init__(self, tmp, scripts):
        self.tmp, self.scripts = tmp, scripts
        self.book, self.locked = tmp / "book.pdf", tmp / "locked.pdf"
        make_fixture.build(str(self.book), str(self.locked))
        self.src = PdfReader(str(self.book))
        self._good = None
        self.count = 0

    def run(self, script, *args, scripts=None):
        proc = subprocess.run([sys.executable, str((scripts or self.scripts) / script), *map(str, args)],
                              capture_output=True, text=True, timeout=600)
        try:
            out = json.loads(proc.stdout)
        except ValueError:
            out = None
        return proc.returncode, out, proc.stderr[-300:]

    def split(self, chapters, *extra, scripts=None, **plan_over):
        self.count += 1
        plan = {"book_title": "Sample Book of Tests", "front": FRONT, "front_label": "Title and license pages",
                "printed_offset": 2, "chapters": chapters}
        plan.update(plan_over)
        plan_path, out_dir = self.tmp / f"plan{self.count}.json", self.tmp / f"out{self.count}"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        code, out, err = self.run("split_book.py", plan_path, self.book, out_dir, *extra, scripts=scripts)
        return code, out, err, out_dir

    @property
    def good(self):
        if self._good is None:
            self._good = self.split([CH1, CH2, CH4])
        return self._good


def text(reader, page):
    return reader.pages[page - 1].extract_text() or ""


def outline_pages(reader):
    found = {}

    def walk(items):
        for item in items:
            if isinstance(item, list):
                walk(item)
            else:
                found[str(item.title)] = reader.get_destination_page_number(item) + 1

    walk(reader.outline)
    return found


def pdfs(folder):
    return sorted(p.name for p in folder.glob("*.pdf")) if folder.exists() else []


@test
def outline_draft_chapters(ctx):
    code, out, err = ctx.run("inspect_pdf.py", "outline", ctx.book)
    chs = out["draft_plan"]["chapters"]
    got = [(c["first"], c["last"]) for c in chs]
    hints = [c["expect_first"] for c in chs]
    ok = (code == 0 and got == [(3, 12), (13, 30), (31, 151), (152, 160)]
          and hints == ["Alpha Basics", "Beta Methods", "Gamma Long Chapter", "Delta Ending"])
    return ok, f"ranges {got}, hints {hints}"


@test
def outline_sections(ctx):
    code, out, err = ctx.run("inspect_pdf.py", "outline", ctx.book)
    want = [{"level": 2, "title": "1.2 Second Section", "page": 8}, {"level": 2, "title": "3.2 Part Two", "page": 90}]
    return code == 0 and all(w in out["outline"] for w in want), f"{len(out['outline'])} entries shown"


@test
def heads_offset(ctx):
    code, out, err = ctx.run("inspect_pdf.py", "heads", ctx.book, "--pages", "3-7")
    cands = {r["pdf_page"]: r["number_candidates"] for r in out["pages"]}
    ok = (code == 0 and cands[6] == [4] and cands[7] == [5] and 1 in cands[3]
          and out["likely_offset"]["offset"] == 2)
    return ok, f"candidates {cands}, likely {out['likely_offset']}"


@test
def split_good_plan(ctx):
    code, out, err, _ = ctx.good
    pages = [f["pages"] for f in out["files"]] if out else None
    return code == 0 and out["all_ok"] and pages == [12, 20, 11] and not out["warnings"], f"exit {code}, pages {pages}"


@test
def split_pages_match_source(ctx):
    """Independent of the script's own check: page k of each file is the page the plan names."""
    code, out, err, out_dir = ctx.good
    bad = []
    for ch in (CH1, CH2, CH4):
        made = PdfReader(str(out_dir / ch["file"]))
        wanted = FRONT + list(range(ch["first"], ch["last"] + 1))
        if len(made.pages) != len(wanted):
            bad.append(f"{ch['file']}: {len(made.pages)} pages, wanted {len(wanted)}")
            continue
        bad += [f"{ch['file']} p{k}" for k, src_page in enumerate(wanted, 1)
                if text(made, k) != text(ctx.src, src_page)]
    return not bad, f"mismatches {bad[:5]}"


@test
def split_front_pages_first(ctx):
    code, out, err, out_dir = ctx.good
    made = PdfReader(str(out_dir / CH1["file"]))
    ok = ("SAMPLE BOOK OF TESTS" in text(made, 1) and "License page" in text(made, 2)
          and "Alpha Basics" in text(made, 3) and "Chapter 1" in text(made, 3))
    return ok, "pages 1-3 of the chapter 1 file"


@test
def split_outline_pages(ctx):
    code, out, err, out_dir = ctx.good
    one = outline_pages(PdfReader(str(out_dir / CH1["file"])))
    two = outline_pages(PdfReader(str(out_dir / CH2["file"])))
    ok = (one == {"Title and license pages": 1, "Chapter 1: Alpha Basics": 3, "1.2 Second Section": 8}
          and two == {"Title and license pages": 1, "Chapter 2: Beta Methods": 3, "2.1 Only Section": 10})
    return ok, f"{one} / {two}"


@test
def split_metadata(ctx):
    code, out, err, out_dir = ctx.good
    meta = PdfReader(str(out_dir / CH1["file"])).metadata
    ok = (meta.get("/Title") == "Sample Book of Tests: Chapter 1: Alpha Basics"
          and "PDF pages 3 to 12" in meta.get("/Subject", "") and "printed pages 1 to 10" in meta.get("/Subject", ""))
    return ok, f"{dict(meta)}"


@test
def split_next_page_head(ctx):
    code, out, err, _ = ctx.good
    heads = [f["next_page_head"] for f in out["files"]]
    return "Beta Methods" in (heads[0] or "") and heads[2] is None, f"{heads}"


@test
def refuse_over_limit(ctx):
    code, out, err, out_dir = ctx.split([CH3])
    msg = " ".join(out["refused"]) if out and "refused" in out else ""
    return code == 2 and "100-page limit" in msg and not pdfs(out_dir), f"exit {code}: {msg[:120]}"


@test
def allow_over_limit_flag(ctx):
    code, out, err, _ = ctx.split([CH3], "--max-pages", "200")
    pages = out["files"][0]["pages"] if out and "files" in out else None
    return code == 0 and pages == 122, f"exit {code}, pages {pages}"


@test
def blank_page_reported(ctx):
    code, out, err, _ = ctx.split([dict(CH3, last=151)], "--max-pages", "200")
    f = out["files"][0] if out and "files" in out else {}
    ok = code == 0 and f.get("pages_without_text") == 1 and "Delta Ending" in (f.get("next_page_head") or "")
    return ok, f"exit {code}, blank pages {f.get('pages_without_text')}, next {f.get('next_page_head')}"


@test
def refuse_unsafe_name(ctx):
    code, out, err, out_dir = ctx.split([dict(CH1, file="../escape.pdf")])
    escaped = (ctx.tmp / "escape.pdf").exists()
    return code == 2 and not escaped and not pdfs(out_dir), f"exit {code}, escaped {escaped}"


@test
def refuse_out_of_range(ctx):
    """One page past the end: small enough that only the range check can catch it."""
    code, out, err, out_dir = ctx.split([dict(CH4, first=155, last=161)])
    msg = " ".join(out["refused"]) if out and "refused" in out else ""
    return code == 2 and "first <= last" in msg and not pdfs(out_dir), f"exit {code}: {msg[:100]}"


@test
def refuse_reversed_range(ctx):
    code, out, err, out_dir = ctx.split([dict(CH1, first=12, last=3)])
    return code == 2 and not pdfs(out_dir), f"exit {code}"


@test
def refuse_duplicate_name(ctx):
    code, out, err, out_dir = ctx.split([CH1, dict(CH2, file=CH1["file"])])
    return code == 2 and not pdfs(out_dir), f"exit {code}"


@test
def warn_overlap(ctx):
    code, out, err, _ = ctx.split([CH1, {"file": "overlap.pdf", "title": "Overlap", "first": 10, "last": 20}])
    warns = out.get("warnings", []) if out else []
    return code == 0 and any("overlap" in w for w in warns), f"exit {code}, warnings {warns}"


@test
def heading_mismatch_fails(ctx):
    code, out, err, _ = ctx.split([dict(CH1, expect_first="Not On This Page")])
    found = out["files"][0]["first_heading_found"] if out and "files" in out else None
    return code == 1 and found is False, f"exit {code}, heading found {found}"


@test
def refuse_encrypted(ctx):
    plan = ctx.tmp / "plan-locked.json"
    plan.write_text(json.dumps({"front": [], "chapters": [CH1]}), encoding="utf-8")
    code, out, err = ctx.run("split_book.py", plan, ctx.locked, ctx.tmp / "out-locked")
    msg = " ".join(out["refused"]) if out and "refused" in out else ""
    return code == 2 and "encrypted" in msg, f"exit {code}: {msg[:100]}"


@test
def refuse_not_a_pdf(ctx):
    fake = ctx.tmp / "fake.pdf"
    fake.write_text("This is a text file with a .pdf name.\n", encoding="utf-8")
    plan = ctx.tmp / "plan-fake.json"
    plan.write_text(json.dumps({"front": [], "chapters": [CH1]}), encoding="utf-8")
    code, out, err = ctx.run("split_book.py", plan, fake, ctx.tmp / "out-fake")
    msg = " ".join(out["refused"]) if out and "refused" in out else ""
    return code == 2 and "cannot read" in msg, f"exit {code}: {msg[:100]}"


@test
def plan_out_written(ctx):
    draft = ctx.tmp / "draft.json"
    code, out, err = ctx.run("inspect_pdf.py", "outline", ctx.book, "--plan-out", draft)
    plan = json.loads(draft.read_text(encoding="utf-8")) if draft.exists() else {}
    code_txt, _, _ = ctx.run("inspect_pdf.py", "outline", ctx.book, "--plan-out", ctx.tmp / "draft.txt")
    ok = code == 0 and len(plan.get("chapters", [])) == 4 and code_txt == 2
    return ok, f"exit {code}, chapters {len(plan.get('chapters', []))}, .txt exit {code_txt}"


@test
def self_check_catches_wrong_page(ctx):
    """Inject a fault (copy the next page instead of the planned one); the script must report it."""
    source = (ctx.scripts / "split_book.py").read_text(encoding="utf-8")
    target = "writer.add_page(src.pages[p - 1])"
    if source.count(target) != 1:
        return False, "cannot inject the fault: the add_page line changed"
    faulty = ctx.tmp / "faulty"
    faulty.mkdir(exist_ok=True)
    (faulty / "split_book.py").write_text(source.replace(target, "writer.add_page(src.pages[p % n])"), encoding="utf-8")
    code, out, err, _ = ctx.split([CH1], scripts=faulty)
    bad = out["files"][0]["text_mismatch_pages"] if out and "files" in out else []
    return code == 1 and len(bad) > 0, f"exit {code}, mismatched pages {bad[:5]}"


def main():
    ap = argparse.ArgumentParser(description="Run the book-chapter-splitter tests.")
    ap.add_argument("--scripts-dir", default=str(HERE.parent / "scripts"))
    scripts = pathlib.Path(ap.parse_args().scripts_dir).resolve()
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="splitter-test-"))
    failed = []
    try:
        ctx = Ctx(tmp, scripts)
        for fn in TESTS:
            name = fn.__name__.replace("_", "-")
            try:
                ok, detail = fn(ctx)
            except Exception as exc:  # a crash inside a test counts as a failure, with the reason
                ok, detail = False, f"{exc.__class__.__name__}: {exc}"
            if not ok:
                failed.append(name)
            print(json.dumps({"test": name, "ok": bool(ok), "detail": str(detail)[:300]}, ensure_ascii=False))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(json.dumps({"scripts_dir": str(scripts), "tests": len(TESTS), "failed": failed,
                      "result": "PASS" if not failed else "FAIL"}))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
