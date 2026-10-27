#!/usr/bin/env python3
"""trig-check: exact trigonometry with SymPy. Prints JSON and never asks for input.

  python scripts/trig_check.py identity "sin(2*x)" "2*sin(x)*cos(x)"
  python scripts/trig_check.py value "cos(pi/12)"
  python scripts/trig_check.py value "cos(15)" --degrees
  python scripts/trig_check.py convert 135 --to rad
  python scripts/trig_check.py convert "3*pi/4" --to deg
  python scripts/trig_check.py triangle --A 30 --a 6 --b 10

Expressions may use numbers, + - * / ^ ( ), pi, sqrt, sin cos tan sec csc cot,
asin acos atan, one-letter variables and theta, phi, alpha, beta, gamma. Write
multiplication as 2*x. Anything else is refused before parsing, so no text
reaches Python's evaluator unchecked. With --degrees, trig functions take
degrees and inverse functions return degrees. Triangle angles are in degrees.
Exit codes: 0 computed, 2 bad input. Needs sympy.
"""
import argparse
import json
import math
import random
import re
import sys

import sympy as sp

FUNCS = {"sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "sec": sp.sec, "csc": sp.csc, "cot": sp.cot,
         "asin": sp.asin, "acos": sp.acos, "atan": sp.atan, "sqrt": sp.sqrt}
GREEK = {"theta", "phi", "alpha", "beta", "gamma"}
TOKEN = re.compile(r"\s*(?:(\d+\.\d*|\.\d+|\d+)|([A-Za-z]+)|(\*\*|[-+*/^(),]))")
TOL = 1e-9


class BadInput(ValueError):
    pass


def parse(text, degrees=False):
    text, pos, names = text.strip(), 0, set()
    while pos < len(text):
        m = TOKEN.match(text, pos)
        if not m:
            raise BadInput(f"not allowed in an expression: {text[pos:pos + 15]!r}")
        if m.group(2):
            names.add(m.group(2))
        pos = m.end()
    unknown = sorted(n for n in names if n not in FUNCS and n != "pi" and n not in GREEK and len(n) != 1)
    if unknown:
        raise BadInput(f"unknown name(s): {', '.join(unknown)}")
    local = {n: sp.Symbol(n, real=True) for n in names if len(n) == 1 or n in GREEK}
    local.update(FUNCS)
    local["pi"] = sp.pi
    if degrees:
        for f in ("sin", "cos", "tan", "sec", "csc", "cot"):
            local[f] = (lambda g: lambda z: g(z * sp.pi / 180))(FUNCS[f])
        for f in ("asin", "acos", "atan"):
            local[f] = (lambda g: lambda z: g(z) * 180 / sp.pi)(FUNCS[f])
    try:
        return sp.sympify(text.replace("^", "**"), locals=local)
    except (sp.SympifyError, SyntaxError, TypeError) as exc:
        raise BadInput(f"could not read {text!r}; write multiplication as 2*x") from exc


def num(expr, subs):
    value = complex(sp.N(expr.subs(subs), 30))
    if not (math.isfinite(value.real) and math.isfinite(value.imag)):
        raise ArithmeticError("not finite")
    return value


def identity(lhs, rhs, degrees):
    L, R = parse(lhs, degrees), parse(rhs, degrees)
    syms = sorted((L - R).free_symbols, key=str)
    proved = sp.simplify(L - R) == 0 or sp.simplify(sp.expand_trig(L - R)) == 0
    unit = 15 if degrees else sp.pi / 12  # try familiar angles first (30, 45, 60, 90 degrees ...), for readable counterexamples
    nice = [k * unit for k in (2, 3, 4, 6, 8, 1, 5, 7, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 12)]
    rng = random.Random(20261007)
    span = 360.0 if degrees else 2 * math.pi
    points = [dict(zip(syms, (nice[(i * (j + 3)) % 23] for j in range(len(syms))))) for i in range(23)]
    points += [{s: rng.uniform(-span, span) for s in syms} for _ in range(300)]
    checked = 0
    for p in points if syms else [{}]:
        try:
            a, b = num(L, p), num(R, p)
        except (ArithmeticError, TypeError, ValueError, ZeroDivisionError):
            continue  # one side is undefined here (for example tan at 90 degrees)
        checked += 1
        if abs(a - b) > TOL * (1 + abs(a) + abs(b)):
            show = {str(s): (str(v) if isinstance(v, sp.Basic) else round(v, 6)) for s, v in p.items()}
            return {"holds": False, "counterexample": show, "lhs_value": round(a.real, 9),
                    "rhs_value": round(b.real, 9), "points_checked": checked}
    if checked == 0:
        return {"holds": None, "reason": "no point where both sides are defined"}
    if proved:
        return {"holds": True, "how": "the difference simplifies to 0", "points_checked": checked}
    return {"holds": "probably", "how": f"agreed at {checked} points, but SymPy could not simplify the difference to 0",
            "points_checked": checked}


def value(text, degrees):
    e = parse(text, degrees)
    if e.free_symbols:
        raise BadInput("value takes numbers only; use identity for expressions with variables")
    exact = sp.simplify(e)
    return {"exact": str(exact), "decimal": float(sp.N(exact, 15))}


def convert(text, to):
    e = parse(text)
    if e.free_symbols:
        raise BadInput("convert takes a number or a multiple of pi")
    out = sp.nsimplify(e) * sp.pi / 180 if to == "rad" else sp.nsimplify(e * 180 / sp.pi)
    out = sp.simplify(out)
    return {"to": to, "exact": str(out), "decimal": float(sp.N(out, 15))}


def triangle(given):
    sides = {k: v for k, v in given.items() if k in "abc" and v is not None}
    angles = {k: v for k, v in given.items() if k in "ABC" and v is not None}
    if len(sides) + len(angles) != 3 or not sides:
        raise BadInput("give exactly three values, at least one of them a side")
    if any(v <= 0 for v in sides.values()) or any(not 0 < v < 180 for v in angles.values()):
        raise BadInput("sides must be positive and angles between 0 and 180 degrees")
    if sum(angles.values()) >= 180:
        raise BadInput("the given angles already add up to 180 degrees or more")
    sin, asin, cos, acos = (lambda d: math.sin(math.radians(d))), (lambda x: math.degrees(math.asin(x))), \
        (lambda d: math.cos(math.radians(d))), (lambda x: math.degrees(math.acos(x)))
    opp = {"a": "A", "b": "B", "c": "C"}

    def from_sides(a, b, c):
        if a + b <= c or a + c <= b or b + c <= a:
            return []
        A = acos((b * b + c * c - a * a) / (2 * b * c))
        B = acos((a * a + c * c - b * b) / (2 * a * c))
        return [dict(a=a, b=b, c=c, A=A, B=B, C=180 - A - B)]

    if len(sides) == 3:
        case, sols = "SSS", from_sides(sides["a"], sides["b"], sides["c"])
    elif len(angles) == 2:
        case = "ASA or AAS"
        missing = next(k for k in "ABC" if k not in angles)
        angles[missing] = 180 - sum(angles.values())
        (k, s), = sides.items()
        ratio = s / sin(angles[opp[k]])
        sols = [dict(a=ratio * sin(angles["A"]), b=ratio * sin(angles["B"]), c=ratio * sin(angles["C"]), **angles)]
    else:
        (K, ang), = angles.items()
        k = K.lower()
        if k not in sides:  # the angle sits between the two sides
            case = "SAS"
            x, y = sides.values()
            third = math.sqrt(x * x + y * y - 2 * x * y * cos(ang))
            full = {**sides, k: third}
            sols = from_sides(full["a"], full["b"], full["c"])
        else:
            case = "SSA"
            q = next(s for s in sides if s != k)
            ratio = sides[q] * sin(ang) / sides[k]
            sols = []
            if ratio <= 1 + 1e-9:
                Q1 = 90.0 if abs(ratio - 1) < 1e-9 else asin(ratio)  # exactly one right triangle at ratio 1
                for Q in (Q1, 180 - Q1):
                    if ang + Q < 180 - 1e-9 and not any(abs(Q - s[opp[q].upper()]) < 1e-9 for s in sols):
                        third = next(x for x in "abc" if x not in (k, q))
                        T = 180 - ang - Q
                        sol = {k: sides[k], q: sides[q], K: ang, opp[q]: Q, opp[third]: T}
                        sol[third] = sides[k] * sin(T) / sin(ang)
                        sols.append(sol)
    out = []
    for s in sols:
        s["area"] = 0.5 * s["b"] * s["c"] * sin(s["A"])
        out.append({key: round(s[key], 6) for key in ("a", "b", "c", "A", "B", "C", "area")})
    return {"case": case, "triangles": len(out), "solutions": out}


def main():
    ap = argparse.ArgumentParser(description="Exact trigonometry checks.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("identity"); p.add_argument("lhs"); p.add_argument("rhs"); p.add_argument("--degrees", action="store_true")
    p = sub.add_parser("value"); p.add_argument("expr"); p.add_argument("--degrees", action="store_true")
    p = sub.add_parser("convert"); p.add_argument("expr"); p.add_argument("--to", choices=("rad", "deg"), required=True)
    p = sub.add_parser("triangle")
    for name in ("a", "b", "c", "A", "B", "C"):
        p.add_argument(f"--{name}", type=float)
    args = ap.parse_args()
    try:
        if args.cmd == "identity":
            result = identity(args.lhs, args.rhs, args.degrees)
        elif args.cmd == "value":
            result = value(args.expr, args.degrees)
        elif args.cmd == "convert":
            result = convert(args.expr, args.to)
        else:
            result = triangle({n: getattr(args, n) for n in ("a", "b", "c", "A", "B", "C")})
    except BadInput as exc:
        print(json.dumps({"error": str(exc)}))
        return 2
    print(json.dumps({"command": args.cmd, **result}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
