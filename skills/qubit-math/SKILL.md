---
name: qubit-math
description: >
  Works small quantum-state calculations with a numpy script and shows the
  numbers: builds one- to few-qubit states, applies gates (X, Y, Z, H, S, T,
  rotations, CNOT, CZ, SWAP), gives measurement probabilities and the state left
  after measuring, reduced density matrices with purity and entanglement entropy,
  overlaps in both fidelity conventions, and Pauli expectation values. Use when
  someone gives a specific state or circuit and asks what comes out. Do not use to
  run the six standard entanglement experiments (quantum-entanglement-lab does
  that), for real quantum hardware, for more than about 10 qubits, or for quantum
  field theory.
license: MIT
metadata:
  version: "1.0"
  requires: "python3, numpy"
  claude-app-description: "Works small qubit calculations with a script: gates, measurement odds, state after measuring, partial trace, entropy, fidelity, Pauli averages. Not for the lab's six tests or hardware."
---

# Qubit math

Compute with the script instead of doing matrix algebra in your head. Factors of √2, minus signs and qubit order are where hand calculations go wrong.

## Steps

1. Check once that numpy is there: `python3 -c "import numpy"`. If it fails, run `pip install numpy`.
2. Put the state and what to compute into one command:
   `python3 scripts/qubit_math.py --state STATE [--gates G1,G2] [--measure M] [--reduce Q] [--compare STATE] [--expect PAULI]`
   - STATE: one-qubit states joined by commas (`0,+`), a Bell state (`phi+`, `phi-`, `psi+`, `psi-`), `ghz3`, or amplitudes in brackets (`"[0.6, 0.8]"`, `"[1, 1j]"`, `"[1/sqrt(2), i/sqrt(2)]"`), which the script normalises.
   - Gates run left to right: `H0`, `X1`, `S0`, `T0`, `RY0:pi/2`, `CNOT01` (control 0, target 1), `CZ01`, `SWAP01`.
   - `--measure Z` measures every qubit; `--measure X@1` measures one qubit and gives the state left after each outcome.
   - `--reduce 1` keeps qubit 1 and traces out the rest: reduced density matrix, purity, entropy in bits.
   - `--compare phi+` gives |⟨a|b⟩| and |⟨a|b⟩|².
   - `--expect ZZ` gives ⟨ψ|Z⊗Z|ψ⟩.
3. Answer in plain words with the script's numbers, and show the state in Dirac notation from its output.

## Conventions to state in answers

- Qubit 0 is the leftmost: |01⟩ means qubit 0 is 0 and qubit 1 is 1. If the question numbers qubits from the right, say so and translate before running.
- "Fidelity" means two things in different sources: |⟨a|b⟩| (what QuTiP's fidelity() returns) or |⟨a|b⟩|². Say which one you give; the script prints both.
- Probabilities are squared magnitudes of amplitudes, never the amplitudes themselves.
- Entropy is in bits (log base 2). A pure product state has 0; one qubit of a Bell pair has 1, the most a qubit can have.

## Limits

- The script reads numbers through a whitelist (digits, pi, i or j, sqrt, exp, cos, sin, + − * / **) and refuses anything else. Don't rewrite input as code to get around a refusal; the whitelist is what keeps text away from Python's eval.
- Pure states only: no noise and no mixed-state inputs.
- Practical up to about 10 qubits.
- It computes what quantum theory predicts. That is not experimental evidence.

## Reference

`references/notation.md` covers Dirac notation, gate matrices, the measurement rule, partial trace, entropy and the two fidelity conventions, with page pointers to Binney & Skinner and the UCSD Physics 130 notes. Read it when someone asks why.
