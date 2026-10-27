#!/usr/bin/env python3
"""Mutation check for quantum-entanglement-lab: proves each lab test can fail.

It runs the lab once as written (all six tests must pass), then runs copies
that each carry one deliberate bug. Every bug must stop the lab at the test it
targets, with the earlier tests still passing. One change that leaves the
physics alone (X*Z instead of Z*X, which differ only by a global phase) must
still pass. A broken lab run under `python -O` must refuse to run instead of
printing PASS lines.

Usage:
  python evals/mutation_check.py [--script PATH]

--script defaults to scripts/entanglement_lab.py beside this evals/ folder,
the packaged skill layout. Pass --script to test a copy kept somewhere else,
such as an older version.

Output: one JSON object per run, then a summary object. Exit code 0 when every
run behaved as expected, 1 when any did not, 2 on a setup error. It needs no
network and writes only to a temporary folder.
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys
import tempfile

TESTS = ["S(φ+)", "X/Z local flips", "partial Z", "Bell decoder", "CHSH", "teleportation"]
FLIPS_DONE = 'print("[PASS] X/Z local flips")'
SVAL = "Sval=abs(E(0,np.pi/4)+E(0,-np.pi/4)+E(np.pi/2,np.pi/4)-E(np.pi/2,-np.pi/4))"

# Each mutation replaces one exact string. "passes" is how many PASS lines must
# print before the run stops; 0 means it stops before the first test.
MUTATIONS = [
    {"id": "hadamard-unnormalized", "passes": 0,
     "why": "Hadamard missing its 1/sqrt(2); the unitarity check must stop the run",
     "old": "H=(X+Z)/np.sqrt(2)", "new": "H=(X+Z)"},
    {"id": "entropy-natural-log", "passes": 0,
     "why": "entropy in nats instead of bits (ln 2 = 0.693)",
     "old": "entropy_vn(phi.ptrace(0),base=2)", "new": "entropy_vn(phi.ptrace(0))"},
    {"id": "x-gate-is-y", "passes": 1,
     "why": "X gate defined as Pauli Y, so Alice's flip lands on the wrong Bell state",
     "old": "I,X,Z = qeye(2),sigmax(),sigmaz()", "new": "I,X,Z = qeye(2),sigmay(),sigmaz()"},
    {"id": "z-flip-uses-x", "passes": 1,
     "why": "the phase flip applies X instead of Z",
     "old": "assert fidelity(tensor(Z,I)*phi,bell(1))>0.999",
     "new": "assert fidelity(tensor(X,I)*phi,bell(1))>0.999"},
    {"id": "partial-z-wrong-bell-state", "passes": 2,
     "why": "partial measurement made on |ψ+⟩, whose outcomes are anti-correlated",
     "old": FLIPS_DONE, "new": FLIPS_DONE + "\nphi=bell(2)"},
    {"id": "partial-z-wrong-basis", "passes": 2,
     "why": "partial measurement made in the X basis instead of Z",
     "old": FLIPS_DONE, "new": FLIPS_DONE + "\nP0,P1=(I+X)/2,(I-X)/2"},
    {"id": "decoder-missing-h", "passes": 3,
     "why": "Bell decoder skips the Hadamard",
     "old": "dec=tensor(H,I)*CNOT", "new": "dec=CNOT"},
    {"id": "cnot-reversed", "passes": 3,
     "why": "CNOT with control and target swapped",
     "old": "CNOT=tensor(P0,I)+tensor(P1,X)", "new": "CNOT=tensor(I,P0)+tensor(X,P1)"},
    {"id": "chsh-angle-off", "passes": 4,
     "why": "Bob's angle b off by 0.05 rad: |S| falls below 2*sqrt(2) but stays above 2.8",
     "old": SVAL,
     "new": "Sval=abs(E(0,np.pi/4+0.05)+E(0,-np.pi/4)+E(np.pi/2,np.pi/4+0.05)-E(np.pi/2,-np.pi/4))"},
    {"id": "chsh-successive-45-degree-angles", "passes": 4,
     "why": "b' = 3π/4 (the successive-45° set) gives |S| = 0 with this sign arrangement",
     "old": SVAL, "new": SVAL.replace("-np.pi/4", "3*np.pi/4")},
    {"id": "x-correction-deleted", "passes": 5,
     "why": "Bob skips the X correction for bits 01",
     "old": "(0,1):X,", "new": "(0,1):I,"},
    {"id": "correction-bits-swapped", "passes": 5,
     "why": "the bit that should select X selects Z, and the other way round",
     "old": "(0,1):X,(1,0):Z", "new": "(0,1):Z,(1,0):X"},
    {"id": "alice-skips-hadamard", "passes": 5,
     "why": "Alice's Bell measurement skips the Hadamard",
     "old": "dec3=tensor(H,I,I)*C01*tot", "new": "dec3=C01*tot"},
]

EQUIVALENT = [
    {"id": "zx-order-global-phase",
     "why": "X*Z instead of Z*X differs only by a global phase, so the lab must still pass",
     "old": "(1,1):Z*X}", "new": "(1,1):X*Z}"},
]

OPTIMIZED = {"id": "run-under-python-O",
             "why": "python -O strips asserts; a broken lab must refuse to run, not print PASS lines",
             "old": "(0,1):X,", "new": "(0,1):I,"}


def run(source: str, flags=()) -> tuple[int, list[str]]:
    """Run one copy of the lab in a temporary folder; return exit code and PASS lines."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        path = pathlib.Path(tmp, "entanglement_lab.py")
        path.write_text(source, encoding="utf-8")
        proc = subprocess.run([sys.executable, *flags, str(path)], capture_output=True,
                              text=True, encoding="utf-8", timeout=300, env=env, cwd=tmp)
    return proc.returncode, [line for line in proc.stdout.splitlines() if line.startswith("[PASS]")]


def mutate(source: str, spec: dict) -> str:
    count = source.count(spec["old"])
    if count != 1:
        raise LookupError(f"{spec['id']}: target text found {count} times, expected once")
    return source.replace(spec["old"], spec["new"])


def main() -> int:
    default = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "entanglement_lab.py"
    parser = argparse.ArgumentParser(description="Prove each entanglement-lab test can fail.")
    parser.add_argument("--script", default=str(default), help="path to entanglement_lab.py")
    args = parser.parse_args()
    script = pathlib.Path(args.script)
    if not script.is_file():
        print(json.dumps({"error": f"lab script not found: {script}"}))
        return 2
    source = script.read_text(encoding="utf-8")

    plan = [("clean", {"id": "as-written", "why": "the unmodified lab must pass all six tests"}, None, ())]
    plan += [("mutation", spec, spec["passes"], ()) for spec in MUTATIONS]
    plan += [("equivalent", spec, None, ()) for spec in EQUIVALENT]
    plan += [("python-O", OPTIMIZED, 0, ("-O",))]

    results = []
    for kind, spec, stop_after, flags in plan:
        try:
            code = source if kind == "clean" else mutate(source, spec)
        except LookupError as exc:
            print(json.dumps({"error": str(exc)}, ensure_ascii=False))
            return 2
        exit_code, passes = run(code, flags)
        if kind in ("clean", "equivalent"):
            ok = exit_code == 0 and len(passes) == len(TESTS)
            expected = "exit 0 with all 6 PASS lines"
        else:
            ok = exit_code != 0 and len(passes) == stop_after
            target = "the unitarity check or first test" if stop_after == 0 else TESTS[stop_after]
            expected = f"stops at {target} after {stop_after} PASS lines"
        row = {"kind": kind, "id": spec["id"], "ok": ok, "expected": expected,
               "exit_code": exit_code, "pass_lines": len(passes), "why": spec["why"]}
        results.append(row)
        print(json.dumps(row, ensure_ascii=False))

    failed = [row["id"] for row in results if not row["ok"]]
    print(json.dumps({"script": str(script), "runs": len(results),
                      "as_expected": len(results) - len(failed), "not_as_expected": failed,
                      "result": "PASS" if not failed else "FAIL"}, ensure_ascii=False))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
