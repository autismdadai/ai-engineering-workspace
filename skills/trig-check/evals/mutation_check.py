#!/usr/bin/env python3
"""Mutation check for trig-check: proves the tests can fail.

It runs evals/test_trig_check.py on the script as written (every test must pass),
then on copies that each carry one deliberate bug (at least one of the named tests
must fail), and on one harmless change (every test must still pass).

Usage: python evals/mutation_check.py [--script PATH]
Output: JSON lines, then a summary. Exit code 0 when every run behaved as expected,
1 when any did not, 2 on a setup error. No network; writes only to a temporary folder.
"""
import argparse
import json
import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
MUTATIONS = [
    ("law-of-cosines-sign", ["tri-sss-345"], "A = acos((b * b + c * c - a * a) / (2 * b * c))",
     "A = acos((b * b - c * c + a * a) / (2 * b * c))"),
    ("ssa-drops-second-triangle", ["tri-ssa-two"], "for Q in (Q1, 180 - Q1):", "for Q in (Q1,):"),
    ("ssa-keeps-impossible-triangle", ["tri-ssa-obtuse-one"], "if ang + Q < 180 - 1e-9 and", "if True and"),
    ("ssa-right-angle-by-rounding", ["tri-ssa-right"],
     "Q1 = 90.0 if abs(ratio - 1) < 1e-9 else asin(ratio)", "Q1 = asin(min(ratio, 1.0))"),
    ("sas-law-of-cosines-sign", ["tri-sas"], "x * x + y * y - 2 * x * y * cos(ang)", "x * x + y * y + 2 * x * y * cos(ang)"),
    ("aas-cosine-for-sine", ["tri-aas"], "ratio = s / sin(angles[opp[k]])", "ratio = s / cos(angles[opp[k]])"),
    ("no-triangle-inequality", ["tri-impossible-sss"], "if a + b <= c or a + c <= b or b + c <= a:", "if False:"),
    ("degrees-ignored", ["value-degrees-30", "value-exact-15deg"],
     "local[f] = (lambda g: lambda z: g(z * sp.pi / 180))(FUNCS[f])", "local[f] = (lambda g: lambda z: g(z))(FUNCS[f])"),
    ("wrong-degree-factor", ["convert-to-rad"], "sp.nsimplify(e) * sp.pi / 180", "sp.nsimplify(e) * sp.pi / 200"),
    ("decimal-instead-of-exact", ["value-exact-15deg"], "exact = sp.simplify(e)", "exact = sp.N(e, 15)"),
    ("counterexamples-never-found", ["id-false-double-angle", "id-false-tan", "id-false-difference-sign"],
     "if abs(a - b) > TOL * (1 + abs(a) + abs(b)):", "if abs(a - b) > 1e9 * (1 + abs(a) + abs(b)):"),
    ("name-allowlist-off", ["guard-unknown-name"], "    if unknown:\n", "    if False:\n"),
]
EQUIVALENT = [("tighter-tolerance", "TOL = 1e-9", "TOL = 1e-10")]


def run_tests(source):
    with tempfile.TemporaryDirectory() as tmp:
        path = pathlib.Path(tmp, "trig_check.py")
        path.write_text(source, encoding="utf-8")
        proc = subprocess.run([sys.executable, str(HERE / "test_trig_check.py"), "--script", str(path)],
                              capture_output=True, text=True, timeout=1200)
    return json.loads(proc.stdout.strip().splitlines()[-1])["failed"]


def main():
    ap = argparse.ArgumentParser(description="Prove the trig-check tests can fail.")
    ap.add_argument("--script", default=str(HERE.parent / "scripts" / "trig_check.py"))
    source = pathlib.Path(ap.parse_args().script).read_text(encoding="utf-8")
    rows = []
    failed = run_tests(source)
    rows.append({"kind": "clean", "id": "as-written", "ok": not failed, "tests_failed": failed})
    for mid, targets, old, new in MUTATIONS + [(e[0], None, e[1], e[2]) for e in EQUIVALENT]:
        if source.count(old) != 1:
            print(json.dumps({"error": f"{mid}: target text found {source.count(old)} times"}))
            return 2
        failed = run_tests(source.replace(old, new))
        ok = (not failed) if targets is None else any(t in failed for t in targets)
        rows.append({"kind": "equivalent" if targets is None else "mutation", "id": mid, "ok": ok,
                     "expected_to_fail": targets, "tests_failed": failed})
    for row in rows:
        print(json.dumps(row))
    bad = [r["id"] for r in rows if not r["ok"]]
    print(json.dumps({"runs": len(rows), "as_expected": len(rows) - len(bad), "not_as_expected": bad,
                      "result": "PASS" if not bad else "FAIL"}))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
