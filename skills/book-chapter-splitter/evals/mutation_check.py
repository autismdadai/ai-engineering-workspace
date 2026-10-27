#!/usr/bin/env python3
"""Mutation check for book-chapter-splitter: proves the tests can fail.

It runs evals/test_split_book.py on the scripts as written (every test must pass), then
on copies that each carry one deliberate bug (at least one of the named tests must
fail), and on one harmless change (every test must still pass).

Usage: python evals/mutation_check.py [--scripts-dir DIR]
Output: JSON lines, then a summary. Exit code 0 when every run behaved as expected,
1 when any did not, 2 on a setup error. No network; writes only to a temporary folder.
"""
import argparse
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
S, I = "split_book.py", "inspect_pdf.py"
MUTATIONS = [
    ("front-pages-dropped", ["split-front-pages-first", "split-good-plan"], S,
     "page_map = list(front) + list(range(first, last + 1))", "page_map = list(range(first, last + 1))"),
    ("range-shifted-one-page", ["split-pages-match-source"], S,
     "page_map = list(front) + list(range(first, last + 1))",
     "page_map = list(front) + list(range(first + 1, min(last + 2, n + 1)))"),
    ("outline-section-off-by-one", ["split-outline-pages"], S,
     "nf + p - first, parent=top", "nf + p - first + 1, parent=top"),
    ("page-limit-ignored", ["refuse-over-limit"], S, "if size > max_pages:", "if False:"),
    ("file-name-check-off", ["refuse-unsafe-name"], S,
     "if not isinstance(name, str) or not NAME.match(name):", "if not isinstance(name, str):"),
    ("page-range-check-off", ["refuse-out-of-range", "refuse-reversed-range"], S,
     "if not (is_page(first, n) and is_page(last, n) and first <= last):",
     "if not (type(first) is int and type(last) is int):"),
    ("duplicate-name-check-off", ["refuse-duplicate-name"], S, "elif name in names:", "elif False:"),
    ("overlap-warning-off", ["warn-overlap"], S, "if a2 <= b1:", "if False:"),
    ("heading-check-always-passes", ["heading-mismatch-fails"], S,
     "heading = nf < len(texts) and squash(str(expect)) in squash(texts[nf])", "heading = True"),
    ("page-text-check-off", ["self-check-catches-wrong-page"], S,
     "if i >= len(texts) or texts[i] != page_text(src, p - 1)]", "if i >= len(texts)]"),
    ("encryption-not-named", ["refuse-encrypted"], S, "if src.is_encrypted:", "if False:"),
    ("outline-wrong-level", ["outline-draft-chapters"], I,
     'if e["level"] == args.level and e["page"]]', 'if e["level"] == args.level + 1 and e["page"]]'),
    ("draft-last-page-off-by-one", ["outline-draft-chapters"], I, '"last": nxt - 1,', '"last": nxt,'),
    ("offset-sign-flipped", ["heads-offset"], I,
     'collections.Counter(r["pdf_page"] - c for', 'collections.Counter(c - r["pdf_page"] for'),
    ("leading-page-number-missed", ["heads-offset"], I,
     'LEAD = re.compile(r"^(\\d{1,4})\\s+\\D")', 'LEAD = re.compile(r"(?!x)x(\\d)")'),
]
EQUIVALENT = [("report-indent-2", S, '"files": files}, ensure_ascii=False, indent=1)',
               '"files": files}, ensure_ascii=False, indent=2)')]


def run_tests(scripts_dir):
    proc = subprocess.run([sys.executable, str(HERE / "test_split_book.py"), "--scripts-dir", str(scripts_dir)],
                          capture_output=True, text=True, timeout=1200)
    return json.loads(proc.stdout.strip().splitlines()[-1])["failed"]


def main():
    ap = argparse.ArgumentParser(description="Prove the book-chapter-splitter tests can fail.")
    ap.add_argument("--scripts-dir", default=str(HERE.parent / "scripts"))
    scripts = pathlib.Path(ap.parse_args().scripts_dir).resolve()
    rows = [{"kind": "clean", "id": "as-written", "tests_failed": run_tests(scripts)}]
    rows[0]["ok"] = not rows[0]["tests_failed"]
    plan = [(m[0], m[1], m[2], m[3], m[4]) for m in MUTATIONS] + [(e[0], None, e[1], e[2], e[3]) for e in EQUIVALENT]
    for mid, targets, fname, old, new in plan:
        source = (scripts / fname).read_text(encoding="utf-8")
        if source.count(old) != 1:
            print(json.dumps({"error": f"{mid}: target text found {source.count(old)} times in {fname}"}))
            return 2
        with tempfile.TemporaryDirectory() as tmp:
            copy = pathlib.Path(tmp, "scripts")
            shutil.copytree(scripts, copy)
            (copy / fname).write_text(source.replace(old, new), encoding="utf-8")
            failed = run_tests(copy)
        ok = (not failed) if targets is None else any(t in failed for t in targets)
        rows.append({"kind": "equivalent" if targets is None else "mutation", "id": mid, "file": fname,
                     "ok": ok, "expected_to_fail": targets, "tests_failed": failed})
    for row in rows:
        print(json.dumps(row))
    bad = [r["id"] for r in rows if not r["ok"]]
    print(json.dumps({"runs": len(rows), "as_expected": len(rows) - len(bad), "not_as_expected": bad,
                      "result": "PASS" if not bad else "FAIL"}))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
