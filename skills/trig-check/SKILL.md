---
name: trig-check
description: >
  Checks trigonometry with a script instead of by eye: tests whether an identity
  holds (and gives a counterexample when it fails), gives exact values, converts
  between degrees and radians, and solves triangles from three parts, including
  the two-triangle SSA case. Use when someone asks whether a trig identity is
  true, wants an exact trig value or an angle conversion, or needs a triangle
  solved. Do not use for calculus, statistics, algebra with no trig in it, or
  word problems that still need a model set up first.
license: MIT
metadata:
  version: "1.0"
  requires: "python3, sympy"
  claude-app-description: "Checks trig with a script: tests identities (with counterexamples), gives exact values, converts degrees/radians, solves triangles incl. SSA. Not for calculus or non-trig algebra."
---

# Trig check

Get every number you report from the script. Trig done in your head is where sign slips and degree/radian mix-ups happen, and the script catches both.

## Steps

1. Check once that SymPy is there: `python3 -c "import sympy"`. If it fails, run `pip install sympy`.
2. Turn the question into one command. Write multiplication as `2*x` and powers as `^` or `**`.
   - Identity: `python3 scripts/trig_check.py identity "tan(x)^2+1" "sec(x)^2"`
   - Exact value: `python3 scripts/trig_check.py value "cos(pi/12)"`. Add `--degrees` when the angles are in degrees: `value "cos(15)" --degrees`.
   - Conversion: `python3 scripts/trig_check.py convert 135 --to rad` or `convert "3*pi/4" --to deg`.
   - Triangle: `python3 scripts/trig_check.py triangle --A 30 --a 6 --b 10`. Sides are a, b, c; angles A, B, C are in degrees, each opposite the side with the same letter. Give exactly three values, at least one of them a side.
3. Read the JSON and answer in plain words, using its numbers.
4. If the question doesn't say degrees or radians and the answer depends on it (sin(30), say), give both and label them.

## Reading the results

- **identity.** `holds: true` means SymPy simplified the difference to 0 and every test point agreed. `holds: false` comes with a counterexample: give the angle and both values. `holds: "probably"` means every point agreed but SymPy couldn't prove it; say that instead of calling it proved. `holds: null` means there was no point where both sides are defined.
- **value.** Give the exact form first, then the decimal.
- **triangle.** `triangles` is 0, 1 or 2. In the SSA case (two sides and an angle that isn't between them), report every triangle listed. If there are none, say no triangle has those measurements, because the side opposite the angle is too short to reach.

## Limits

- The script refuses anything that isn't a plain math expression. The only names it accepts are sin, cos, tan, sec, csc, cot, asin, acos, atan, sqrt, pi, single letters, theta, phi, alpha, beta and gamma. Don't get around a refusal by rewriting the input as code: the refusal is what keeps text from reaching Python unchecked.
- It doesn't do calculus, solve equations for x, or draw graphs.
- Triangle results are decimals rounded to 6 places.

## Reference

`references/identities.md` has the core identities, exact values, the laws of sines and cosines and the SSA rule, with section pointers to the open trigonometry textbook. Read it only when someone asks why an answer is what it is.
