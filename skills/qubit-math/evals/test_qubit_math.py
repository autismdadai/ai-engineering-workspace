#!/usr/bin/env python3
"""Known-answer tests for scripts/qubit_math.py. Prints one JSON line per test, then a summary.

Usage: python evals/test_qubit_math.py [--script PATH]
Exit code 0 when every test passes, 1 when any fails. Needs numpy; no network.
"""
import argparse
import json
import pathlib
import subprocess
import sys


def close(x, y, tol=1e-6):
    return abs(x - y) <= tol


def overlap_one(r):
    return close(r["compare"]["abs_overlap"], 1.0)


TESTS = [
    ("bell-reduced-mixed", ["--state", "phi+", "--reduce", "1"],
     lambda r: r["reduce"]["density_matrix"] == [["0.5", "0"], ["0", "0.5"]] and close(r["reduce"]["purity"], 0.5)
     and close(r["reduce"]["entropy_bits"], 1.0)),
    ("reduce-keeps-right-qubit", ["--state", "0,+", "--reduce", "1"],
     lambda r: r["reduce"]["density_matrix"] == [["0.5", "0.5"], ["0.5", "0.5"]]),
    ("product-entropy-zero", ["--state", "0,+", "--reduce", "0"],
     lambda r: close(r["reduce"]["entropy_bits"], 0.0) and close(r["reduce"]["purity"], 1.0)),
    ("h-makes-plus", ["--state", "0", "--gates", "H0", "--compare", "+"], overlap_one),
    ("bell-from-circuit", ["--state", "0,0", "--gates", "H0,CNOT01", "--compare", "phi+"], overlap_one),
    ("x-on-phi-gives-psi", ["--state", "phi+", "--gates", "X0", "--compare", "psi+"], overlap_one),
    ("z-on-phi-gives-phi-minus", ["--state", "phi+", "--gates", "Z0", "--compare", "phi-"], overlap_one),
    ("measure-z-all", ["--state", "phi+", "--measure", "Z"],
     lambda r: r["measure"]["probabilities"] == {"00": 0.5, "11": 0.5}),
    ("measure-x-plus", ["--state", "+", "--measure", "X"], lambda r: r["measure"]["probabilities"] == {"+": 1.0}),
    ("measure-x-real", ["--state", "[0.6, 0.8]", "--measure", "X"],
     lambda r: close(r["measure"]["probabilities"]["+"], 0.98) and close(r["measure"]["probabilities"]["-"], 0.02)),
    ("measure-one-qubit", ["--state", "phi+", "--measure", "Z@0"],
     lambda r: r["measure"]["results"][0] == {"outcome": "0", "probability": 0.5, "state_after": "(1)|00>"}),
    ("fidelity-conventions", ["--state", "0", "--compare", "+"],
     lambda r: close(r["compare"]["abs_overlap"], 0.707107) and close(r["compare"]["probability"], 0.5)),
    ("expect-zz-phi", ["--state", "phi+", "--expect", "ZZ"], lambda r: close(r["expect"]["value"], 1.0)),
    ("expect-zz-psi", ["--state", "psi+", "--expect", "ZZ"], lambda r: close(r["expect"]["value"], -1.0)),
    ("expect-xx-singlet", ["--state", "psi-", "--expect", "XX"], lambda r: close(r["expect"]["value"], -1.0)),
    ("expect-order", ["--state", "0,1", "--expect", "ZI"], lambda r: close(r["expect"]["value"], 1.0)),
    ("ry-half-pi", ["--state", "0", "--gates", "RY0:pi/2", "--compare", "+"], overlap_one),
    ("cnot-control-first", ["--state", "1,0", "--gates", "CNOT01", "--compare", "1,1"], overlap_one),
    ("normalised-input", ["--state", "[1, 1]", "--compare", "+"], overlap_one),
    ("ghz-two-qubits-mixed", ["--state", "ghz3", "--reduce", "0,1"], lambda r: close(r["reduce"]["entropy_bits"], 1.0)),
    ("s-gate", ["--state", "+", "--gates", "S0", "--compare", "+i"], overlap_one),
    ("measure-y", ["--state", "+i", "--measure", "Y"], lambda r: r["measure"]["probabilities"] == {"+i": 1.0}),
    ("guard-unlisted-function", ["--state", "[abs(-1), 0]"], "refused"),  # plain eval would accept this
    ("guard-code", ["--state", "__import__('os')"], "refused"),
    ("guard-length", ["--state", "[1, 0, 0]"], "refused"),
]


def main():
    default = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "qubit_math.py"
    ap = argparse.ArgumentParser(description="Known-answer tests for qubit_math.py")
    ap.add_argument("--script", default=str(default))
    args = ap.parse_args()
    failed = []
    for tid, argv, check in TESTS:
        proc = subprocess.run([sys.executable, args.script, *argv], capture_output=True, text=True, timeout=120)
        try:
            out = json.loads(proc.stdout.strip().splitlines()[-1])
            ok = (proc.returncode == 2 and "error" in out) if check == "refused" else (proc.returncode == 0 and bool(check(out)))
        except (ValueError, IndexError, KeyError, TypeError):
            ok, out = False, {"stdout": proc.stdout[-300:], "stderr": proc.stderr[-300:]}
        if not ok:
            failed.append(tid)
        print(json.dumps({"test": tid, "ok": ok, **({} if ok else {"got": out})}, ensure_ascii=False))
    print(json.dumps({"script": args.script, "tests": len(TESTS), "failed": failed, "result": "PASS" if not failed else "FAIL"}))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
