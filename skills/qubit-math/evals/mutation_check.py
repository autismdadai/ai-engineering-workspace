#!/usr/bin/env python3
"""Mutation check for qubit-math: proves the tests can fail.

It runs evals/test_qubit_math.py on the script as written (every test must pass),
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
    ("hadamard-unnormalized", ["h-makes-plus", "bell-from-circuit"],
     "H = np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)", "H = np.array([[1, 1], [1, -1]], dtype=complex)"),
    ("qubit-order-reversed", ["cnot-control-first", "expect-order"], "    for q in range(n):\n", "    for q in reversed(range(n)):\n"),
    ("cnot-applies-z", ["bell-from-circuit", "cnot-control-first"],
     "return on(n, {a: p0}) + on(n, {a: p1, b: X})", "return on(n, {a: p0}) + on(n, {a: p1, b: Z})"),
    ("entropy-in-nats", ["bell-reduced-mixed", "ghz-two-qubits-mixed"], "v * math.log2(v)", "v * math.log(v)"),
    ("partial-trace-keeps-wrong-qubits", ["reduce-keeps-right-qubit"], ".transpose(keep + traced)", ".transpose(traced + keep)"),
    ("probabilities-not-squared", ["measure-x-real", "measure-z-all"],
     "probs = np.abs(basis_change(basis, n, range(n)) @ vec) ** 2", "probs = np.abs(basis_change(basis, n, range(n)) @ vec)"),
    ("fidelity-conventions-swapped", ["fidelity-conventions"],
     '"abs_overlap": round(float(amp), 6), "probability": round(float(amp ** 2), 6)',
     '"abs_overlap": round(float(amp ** 2), 6), "probability": round(float(amp), 6)'),
    ("no-normalisation", ["normalised-input"], "return vec / norm, n", "return vec, n"),
    ("eval-instead-of-whitelist", ["guard-unlisted-function"],
     "vec = np.array([complex(safe_eval(e)) for e in tree.elts], dtype=complex)",
     "vec = np.array([complex(eval(ast.unparse(e))) for e in tree.elts], dtype=complex)"),
    ("x-basis-uses-s", ["measure-x-plus"], '"X": H, "Y"', '"X": S, "Y"'),
    ("y-basis-missing-dagger", ["measure-y"], "H @ S.conj().T", "H @ S"),
    ("state-after-not-renormalised", ["measure-one-qubit"],
     "post = U.conj().T @ (part / math.sqrt(p))", "post = U.conj().T @ part"),
    ("s-gate-wrong-sign", ["s-gate"], "S, T = np.diag([1, 1j]),", "S, T = np.diag([1, -1j]),"),
]
EQUIVALENT = [("smaller-display-cutoff", "abs(a) > 1e-9", "abs(a) > 1e-10")]


def run_tests(source):
    with tempfile.TemporaryDirectory() as tmp:
        path = pathlib.Path(tmp, "qubit_math.py")
        path.write_text(source, encoding="utf-8")
        proc = subprocess.run([sys.executable, str(HERE / "test_qubit_math.py"), "--script", str(path)],
                              capture_output=True, text=True, timeout=1200)
    return json.loads(proc.stdout.strip().splitlines()[-1])["failed"]


def main():
    ap = argparse.ArgumentParser(description="Prove the qubit-math tests can fail.")
    ap.add_argument("--script", default=str(HERE.parent / "scripts" / "qubit_math.py"))
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
