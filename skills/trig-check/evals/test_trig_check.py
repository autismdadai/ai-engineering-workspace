#!/usr/bin/env python3
"""Known-answer tests for scripts/trig_check.py. Prints one JSON line per test, then a summary.

Usage: python evals/test_trig_check.py [--script PATH]
Exit code 0 when every test passes, 1 when any fails. Needs sympy; no network.
"""
import argparse
import json
import pathlib
import subprocess
import sys


def close(x, y, tol=1e-6):
    return abs(x - y) <= tol


def sols(r, key):
    return sorted(s[key] for s in r["solutions"])


TESTS = [
    ("id-true-double-angle", ["identity", "sin(2*x)", "2*sin(x)*cos(x)"], lambda r: r["holds"] is True),
    ("id-false-double-angle", ["identity", "sin(2*x)", "2*sin(x)"], lambda r: r["holds"] is False and r["counterexample"]),
    ("id-false-tan", ["identity", "tan(x)", "sin(x)*cos(x)"], lambda r: r["holds"] is False),
    ("id-true-sec-with-gaps", ["identity", "tan(x)^2+1", "sec(x)^2"], lambda r: r["holds"] is True),
    ("id-true-difference", ["identity", "cos(a-b)", "cos(a)*cos(b)+sin(a)*sin(b)"], lambda r: r["holds"] is True),
    ("id-false-difference-sign", ["identity", "cos(a-b)", "cos(a)*cos(b)-sin(a)*sin(b)"], lambda r: r["holds"] is False),
    ("value-exact-15deg", ["value", "cos(15)", "--degrees"],
     lambda r: "sqrt(6)" in r["exact"] and "sqrt(2)" in r["exact"] and close(r["decimal"], 0.9659258262890683)),
    ("value-degrees-30", ["value", "sin(30)", "--degrees"], lambda r: r["exact"] == "1/2"),
    ("value-radians-by-default", ["value", "sin(30)"], lambda r: close(r["decimal"], -0.9880316240928618)),
    ("convert-to-rad", ["convert", "135", "--to", "rad"], lambda r: r["exact"] == "3*pi/4"),
    ("convert-to-deg", ["convert", "3*pi/4", "--to", "deg"], lambda r: r["exact"] == "135"),
    ("tri-sss-345", ["triangle", "--a", "3", "--b", "4", "--c", "5"],
     lambda r: r["triangles"] == 1 and close(r["solutions"][0]["A"], 36.869898) and close(r["solutions"][0]["C"], 90.0)),
    ("tri-ssa-two", ["triangle", "--A", "30", "--a", "6", "--b", "10"],
     lambda r: r["triangles"] == 2 and close(sols(r, "B")[0], 56.44269) and close(sols(r, "B")[1], 123.55731)
     and close(sols(r, "c")[0], 5.343629) and close(sols(r, "c")[1], 11.976879)),
    ("tri-ssa-none", ["triangle", "--A", "30", "--a", "2", "--b", "10"], lambda r: r["triangles"] == 0),
    ("tri-ssa-right", ["triangle", "--A", "30", "--a", "5", "--b", "10"],
     lambda r: r["triangles"] == 1 and close(r["solutions"][0]["B"], 90.0)),
    ("tri-ssa-obtuse-one", ["triangle", "--A", "100", "--a", "10", "--b", "6"],
     lambda r: r["triangles"] == 1 and close(r["solutions"][0]["B"], 36.219811)),
    ("tri-sas", ["triangle", "--a", "5", "--b", "7", "--C", "60"],
     lambda r: r["triangles"] == 1 and close(r["solutions"][0]["c"], 6.244998)),
    ("tri-aas", ["triangle", "--A", "40", "--B", "60", "--c", "10"],
     lambda r: r["triangles"] == 1 and close(r["solutions"][0]["a"], 6.527036)),
    ("tri-impossible-sss", ["triangle", "--a", "1", "--b", "2", "--c", "5"], lambda r: r["triangles"] == 0),
    ("guard-unknown-name", ["value", "factorial(5)"], "refused"),  # SymPy would happily compute this without the allowlist
    ("guard-code", ["value", "__import__('os')"], "refused"),
]


def main():
    default = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "trig_check.py"
    ap = argparse.ArgumentParser(description="Known-answer tests for trig_check.py")
    ap.add_argument("--script", default=str(default))
    args = ap.parse_args()
    failed = []
    for tid, argv, check in TESTS:
        proc = subprocess.run([sys.executable, args.script, *argv], capture_output=True, text=True, timeout=300)
        try:
            out = json.loads(proc.stdout.strip().splitlines()[-1])
            if check == "refused":
                ok = proc.returncode == 2 and "error" in out
            else:
                ok = proc.returncode == 0 and bool(check(out))
        except (ValueError, IndexError, KeyError, TypeError):
            ok, out = False, {"stdout": proc.stdout[-300:], "stderr": proc.stderr[-300:]}
        if not ok:
            failed.append(tid)
        print(json.dumps({"test": tid, "ok": ok, **({} if ok else {"got": out})}, ensure_ascii=False))
    print(json.dumps({"script": args.script, "tests": len(TESTS), "failed": failed, "result": "PASS" if not failed else "FAIL"}))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
