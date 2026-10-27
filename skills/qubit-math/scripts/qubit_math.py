#!/usr/bin/env python3
"""qubit-math: small quantum-state calculations with numpy. Prints JSON and never asks for input.

  python scripts/qubit_math.py --state phi+ --reduce 1
  python scripts/qubit_math.py --state 0,0 --gates H0,CNOT01 --measure Z
  python scripts/qubit_math.py --state "[0.6, 0.8]" --measure X
  python scripts/qubit_math.py --state + --compare 0
  python scripts/qubit_math.py --state psi+ --expect ZZ

--state    comma-separated one-qubit states (0, 1, +, -, +i, -i), a Bell state
           (phi+, phi-, psi+, psi-), ghz3, or amplitudes like "[1, 1j]" (normalised
           for you; the length must be a power of 2). Qubit 0 is the leftmost:
           |01> means qubit 0 is 0 and qubit 1 is 1.
--gates    applied left to right: X0 Y0 Z0 H0 S0 T0, RX0:pi/2 RY1:pi/4 RZ0:0.3
           (radians), CNOT01 (control 0, target 1), CZ01, SWAP01.
--measure  Z, X or Y on every qubit, or one qubit as Z@0, X@1, Y@0.
--reduce   qubits to keep, e.g. 1 or 0,2: reduced density matrix, purity, entropy in bits.
--compare  another state: |<a|b>| and |<a|b>|^2, the two common "fidelity" conventions.
--expect   a Pauli string, one letter per qubit, e.g. ZZ or XI.
Numbers and angles may use digits, pi, sqrt(), exp(), cos(), sin(), + - * / ** and
j or i for the imaginary unit. A small whitelist parser reads them; nothing reaches
Python's eval. Exit codes: 0 computed, 2 bad input. Needs numpy only.
"""
import argparse
import ast
import json
import math
import re
import sys

import numpy as np

R2 = 1 / math.sqrt(2)
ONE = {"0": [1, 0], "1": [0, 1], "+": [R2, R2], "-": [R2, -R2], "+i": [R2, 1j * R2], "-i": [R2, -1j * R2]}
NAMED = {"phi+": [R2, 0, 0, R2], "phi-": [R2, 0, 0, -R2], "psi+": [0, R2, R2, 0], "psi-": [0, R2, -R2, 0],
         "ghz3": [R2, 0, 0, 0, 0, 0, 0, R2]}
I2, X = np.eye(2), np.array([[0, 1], [1, 0]], dtype=complex)
Y, Z = np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)
S, T = np.diag([1, 1j]), np.diag([1, np.exp(1j * math.pi / 4)])
FIXED = {"X": X, "Y": Y, "Z": Z, "H": H, "S": S, "T": T}
PAULI = {"I": I2, "X": X, "Y": Y, "Z": Z}
FUNCS = {"sqrt": np.sqrt, "exp": np.exp, "cos": np.cos, "sin": np.sin}
OPS = {ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b, ast.Mult: lambda a, b: a * b,
       ast.Div: lambda a, b: a / b, ast.Pow: lambda a, b: a ** b}


class BadInput(ValueError):
    pass


def safe_eval(node):
    """Evaluate a number-only expression tree; anything not on the whitelist is refused."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, complex)) and not isinstance(node.value, bool):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        v = safe_eval(node.operand)
        return -v if isinstance(node.op, ast.USub) else v
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](safe_eval(node.left), safe_eval(node.right))
    if isinstance(node, ast.Name) and node.id in ("pi", "i", "j"):
        return math.pi if node.id == "pi" else 1j
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in FUNCS
            and len(node.args) == 1 and not node.keywords):
        return FUNCS[node.func.id](safe_eval(node.args[0]))
    raise BadInput("only numbers, pi, i/j, sqrt, exp, cos, sin and + - * / ** are allowed")


def number(text):
    try:
        return complex(safe_eval(ast.parse(text.strip(), mode="eval").body))
    except SyntaxError as exc:
        raise BadInput(f"could not read {text!r}") from exc


def parse_state(text):
    text = text.strip()
    if text in NAMED:
        vec = np.array(NAMED[text], dtype=complex)
    elif text.startswith("["):
        try:
            tree = ast.parse(text, mode="eval").body
        except SyntaxError as exc:
            raise BadInput(f"could not read {text!r}") from exc
        if not isinstance(tree, ast.List):
            raise BadInput("amplitudes must be a list like [1, 1j]")
        vec = np.array([complex(safe_eval(e)) for e in tree.elts], dtype=complex)
    else:
        parts = [p.strip() for p in text.split(",")]
        if not parts or any(p not in ONE for p in parts):
            raise BadInput(f"unknown state {text!r}; use 0, 1, +, -, +i, -i, a Bell name, ghz3 or a list")
        vec = np.array([1], dtype=complex)
        for p in parts:
            vec = np.kron(vec, np.array(ONE[p], dtype=complex))
    n = int(round(math.log2(len(vec)))) if len(vec) else 0
    if len(vec) < 2 or 2 ** n != len(vec):
        raise BadInput("the number of amplitudes must be a power of 2 (2, 4, 8, ...)")
    norm = np.linalg.norm(vec)
    if norm < 1e-12:
        raise BadInput("the state has zero length")
    return vec / norm, n


def on(n, ops):
    """Operator acting with ops[q] on qubit q and identity elsewhere; qubit 0 is the leftmost factor."""
    full = np.array([[1]], dtype=complex)
    for q in range(n):
        full = np.kron(full, ops.get(q, I2))
    return full


def gate(token, n):
    m = re.fullmatch(r"(X|Y|Z|H|S|T)(\d)|(RX|RY|RZ)(\d):(.+)|(CNOT|CZ|SWAP)(\d)(\d)", token.strip())
    if not m:
        raise BadInput(f"unknown gate {token!r}")
    qs = [int(q) for q in m.groups() if q and q.isdigit()]
    if any(q >= n for q in qs) or len(set(qs)) != len(qs):
        raise BadInput(f"gate {token!r} needs distinct qubits below {n}")
    if m.group(1):
        return on(n, {qs[0]: FIXED[m.group(1)]})
    if m.group(3):
        theta = number(m.group(5)).real
        axis = {"RX": X, "RY": Y, "RZ": Z}[m.group(3)]
        return on(n, {qs[0]: math.cos(theta / 2) * I2 - 1j * math.sin(theta / 2) * axis})
    a, b = qs
    p0, p1 = np.diag([1, 0]).astype(complex), np.diag([0, 1]).astype(complex)
    if m.group(6) == "CNOT":
        return on(n, {a: p0}) + on(n, {a: p1, b: X})
    if m.group(6) == "CZ":
        return on(n, {a: p0}) + on(n, {a: p1, b: Z})
    return sum(on(n, {a: P, b: P}) for P in (I2, X, Y, Z)) / 2


def fmt(z):
    z = complex(z)
    re_, im = round(z.real, 6) + 0.0, round(z.imag, 6) + 0.0
    return f"{re_:g}" if abs(im) < 1e-9 else f"{re_:g}{im:+g}j"


def dirac(vec, n):
    terms = [f"({fmt(a)})|{k:0{n}b}>" for k, a in enumerate(vec) if abs(a) > 1e-9]
    return " + ".join(terms) or "0"


def basis_change(basis, n, qubits):
    to_z = {"Z": I2, "X": H, "Y": H @ S.conj().T}[basis]  # rotate so that a Z measurement reads this basis
    return on(n, {q: to_z for q in qubits})


def measure(vec, n, spec):
    m = re.fullmatch(r"(X|Y|Z)(?:@(\d))?", spec.strip())
    if not m:
        raise BadInput("measure as Z, X or Y (all qubits) or Z@0 (one qubit)")
    basis, labels = m.group(1), {"Z": "01", "X": "+-", "Y": ["+i", "-i"]}[m.group(1)]
    if m.group(2) is None:
        probs = np.abs(basis_change(basis, n, range(n)) @ vec) ** 2
        out = {}
        for k, p in enumerate(probs):
            if p > 1e-12:
                bits = f"{k:0{n}b}"
                out["".join(labels[int(b)] if basis == "Z" else labels[int(b)] + " " for b in bits).strip()] = round(float(p), 6)
        return {"basis": basis, "qubits": "all", "probabilities": out}
    q = int(m.group(2))
    if q >= n:
        raise BadInput(f"there is no qubit {q}")
    U = basis_change(basis, n, [q])
    rotated = U @ vec
    results = []
    for outcome in (0, 1):
        proj = on(n, {q: np.diag([1 - outcome, outcome]).astype(complex)})
        part = proj @ rotated
        p = float(np.vdot(part, part).real)
        if p > 1e-12:
            post = U.conj().T @ (part / math.sqrt(p))
            results.append({"outcome": str(labels[outcome]), "probability": round(p, 6), "state_after": dirac(post, n)})
    return {"basis": basis, "qubit": q, "results": results}


def reduce(vec, n, keep):
    keep = sorted(set(keep))
    if not keep or any(q >= n for q in keep):
        raise BadInput(f"keep qubits between 0 and {n - 1}")
    traced = [q for q in range(n) if q not in keep]
    psi = vec.reshape([2] * n).transpose(keep + traced).reshape(2 ** len(keep), -1)
    rho = psi @ psi.conj().T
    evals = np.clip(np.linalg.eigvalsh(rho), 0, None)
    entropy = float(-sum(v * math.log2(v) for v in evals if v > 1e-12))
    return {"kept": keep, "density_matrix": [[fmt(x) for x in row] for row in rho],
            "purity": round(float(np.trace(rho @ rho).real), 6), "entropy_bits": round(entropy, 6) + 0.0}


def main():
    ap = argparse.ArgumentParser(description="Small quantum-state calculations.")
    ap.add_argument("--state", required=True)
    ap.add_argument("--gates")
    ap.add_argument("--measure")
    ap.add_argument("--reduce")
    ap.add_argument("--compare")
    ap.add_argument("--expect")
    args = ap.parse_args()
    try:
        vec, n = parse_state(args.state)
        for token in (args.gates.split(",") if args.gates else []):
            vec = gate(token, n) @ vec
        out = {"qubits": n, "convention": "qubit 0 is the leftmost", "state": dirac(vec, n)}
        if args.measure:
            out["measure"] = measure(vec, n, args.measure)
        if args.reduce:
            out["reduce"] = reduce(vec, n, [int(q) for q in args.reduce.split(",")])
        if args.compare:
            other, m = parse_state(args.compare)
            if m != n:
                raise BadInput(f"--compare needs {n} qubits, got {m}")
            amp = abs(np.vdot(other, vec))
            out["compare"] = {"abs_overlap": round(float(amp), 6), "probability": round(float(amp ** 2), 6)}
        if args.expect:
            letters = args.expect.strip().upper()
            if len(letters) != n or any(c not in PAULI for c in letters):
                raise BadInput(f"--expect needs {n} letters from I, X, Y, Z")
            P = on(n, {q: PAULI[c] for q, c in enumerate(letters)})
            out["expect"] = {"pauli": letters, "value": round(float(np.vdot(vec, P @ vec).real), 6) + 0.0}
    except (BadInput, ValueError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
