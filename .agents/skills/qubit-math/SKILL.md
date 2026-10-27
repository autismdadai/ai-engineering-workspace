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
## Canonical instructions

This is a Codex discovery entry. Read and follow the full [canonical skill](../../../skills/qubit-math/SKILL.md). Resolve any scripts, references, and assets relative to that canonical skill's directory. If it names a host tool that is unavailable in this session, say so and use the documented fallback where possible. Keep the canonical source in its original project folder; this entry only exposes it to Codex.
