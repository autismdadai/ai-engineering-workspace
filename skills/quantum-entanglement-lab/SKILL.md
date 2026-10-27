---
name: quantum-entanglement-lab
description: >
  Run verified quantum entanglement experiments and explain results.
  Use when the user asks about Bell states, entanglement entropy,
  CHSH inequality, quantum teleportation, partial measurement,
  or wants to execute the entanglement laboratory script.
  Do not use for general quantum field theory, hardware control,
  or non-educational production quantum computing tasks.
license: MIT
metadata:
  version: "1.2.1"
  author: expert-skill-builder
  purpose: educational + research verification of core entanglement protocols
  requires: "python3, qutip>=5.0, numpy, scipy"
  claude-app-description: "Runs and explains a verified quantum entanglement lab: Bell states, entanglement entropy, CHSH, teleportation, partial measurement. Not for quantum field theory, hardware control or production use."
---

# Quantum Entanglement Laboratory

## Purpose
Provide a single, reliable skill that lets an agent run the six core entanglement experiments that were verified to pass with fidelity 1.000000 and CHSH = 2√2. The skill teaches both the concepts and the executable verification.

## When to use
- User asks to demonstrate or verify Bell states, entanglement entropy, local Pauli actions, partial measurement, Bell decoding, CHSH violation, or quantum teleportation.
- User wants a runnable laboratory script for educational or research checking.
- User requests “run the entanglement tests” or “show me that teleportation works”.

## When not to use
- Pure theoretical quantum field theory or continuous-variable quantum optics.
- Control of real quantum hardware (lasers, dilution refrigerators, etc.).
- High-stakes medical, financial, or safety decisions.

## Procedure

### 1. Confirm environment
Ask or check that the host can run:
```bash
python3 -c "import qutip, numpy, scipy; print('ok')"
```
If missing, instruct: `pip install qutip numpy scipy`

### 2. Run the laboratory
Execute the deterministic script:
```bash
python scripts/entanglement_lab.py
```
Expected output (all must appear):
```
[PASS] S(φ+)=1.000000
[PASS] X/Z local flips
[PASS] partial Z
[PASS] Bell decoder
[PASS] CHSH |S|=2.828427
[PASS] teleportation all branches F=1
ALL TESTS PASSED — you have a working entanglement laboratory.
```

### 3. Explain results on request
If the user asks for explanation, use the short reference cards in `references/`:
- `bell-states.md` — the four Bell states and local Pauli actions
- `chsh.md` — why |S| = 2√2 violates local realism
- `teleportation.md` — resource cost and correction table

### 4. Optional deeper inspection
Only when the user asks for the math, read the corresponding reference file. Never load all references by default.

## Gotchas
- QuTiP 5.x no longer ships `qutip.qip` by default; the script builds CNOT and Hadamard from tensor products so it stays portable.
- CHSH angle set (0, π/2, π/4, −π/4) reaches the Tsirelson bound with the singlet for S = E(a,b)+E(a,b′)+E(a′,b)−E(a′,b′). It is not the only optimal set (rotating all four angles together gives the same |S|), but the angles must match which term carries the minus sign: Preskill's successive-45° set gives 2√2 in his arrangement and 0 in this one.
- QuTiP's `fidelity()` is the square-root fidelity |⟨a|b⟩| for pure states (|0⟩ vs |+⟩ gives 0.707, not 0.5) and does not normalize kets, so a broken gate can score above 1. Say which convention you report.
- Test teleportation on more than one message state. X leaves |+⟩ unchanged, so a |+⟩-only test cannot see X-correction bugs.
- Teleportation corrections are {I, X, Z, ZX}, keyed by the two classical bits. Which bit selects X and which selects Z matters. The order inside ZX does not: XZ = −ZX, a global phase, so it teleports the same state.
- The script uses assertions; any failure raises and stops, which is intentional for verification. Don't run it with `python -O`, which strips assertions; version 1.2 refuses to run under -O.

## Success criteria
- Script exits 0 and prints all six [PASS] lines.
- Agent can correctly name the Bell state that results from applying X or Z to one share of |φ+⟩.
- Agent can state the two classical bits + one ebit resource cost of teleportation.
---
