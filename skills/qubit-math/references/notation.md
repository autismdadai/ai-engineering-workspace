# Qubit notation card

Page pointers go to two reference books in the project: *The Physics of Quantum Mechanics* (Binney and Skinner) and the UCSD Physics 130 course notes. Page numbers are the books' printed ones. These notes are written fresh, not copied; read the pages for the full derivations.

## States (Binney & Skinner §1.3, p. 7; Dirac notation, p. 9)

- A qubit state is |ψ⟩ = a|0⟩ + b|1⟩ with |a|² + |b|² = 1.
- Common states: |+⟩ = (|0⟩ + |1⟩)/√2, |−⟩ = (|0⟩ − |1⟩)/√2, |+i⟩ = (|0⟩ + i|1⟩)/√2, |−i⟩ = (|0⟩ − i|1⟩)/√2.
- Two qubits: |ab⟩ = |a⟩ ⊗ |b⟩, written with qubit 0 on the left.
- Bell states: |φ±⟩ = (|00⟩ ± |11⟩)/√2 and |ψ±⟩ = (|01⟩ ± |10⟩)/√2.

## Gates (UCSD notes ch. 18, p. 247, for operators as matrices; Binney & Skinner §6.2, p. 116, for quantum computing)

- X = [[0, 1], [1, 0]], Y = [[0, −i], [i, 0]], Z = [[1, 0], [0, −1]]
- H = (1/√2)[[1, 1], [1, −1]], S = diag(1, i), T = diag(1, e^{iπ/4})
- Rotations: R_a(θ) = cos(θ/2) I − i sin(θ/2) σ_a, for a = X, Y or Z
- CNOT with control c and target t: |0⟩⟨0| on c (and nothing on t) plus |1⟩⟨1| on c with X on t

## Measurement (Binney & Skinner §1.4, p. 15; operators, §2.1, p. 17)

- The probability of outcome k is |⟨k|ψ⟩|², the squared magnitude of its amplitude.
- After outcome k, the state is the part of |ψ⟩ consistent with k, renormalised.
- To measure in the X or Y basis, rotate to Z first: H for X, H S† for Y.

## Entanglement and reduced states (Binney & Skinner §6.1, p. 105; development of entanglement, p. 110; Bell's inequality, p. 113; reduced density operators, §6.3, p. 125)

- A pure two-qubit state is entangled exactly when it can't be written as a product |a⟩ ⊗ |b⟩.
- The reduced density matrix of one qubit comes from tracing out the others. For every Bell state, each qubit on its own is I/2.
- Purity, Tr(ρ²), is 1 for a pure state and 1/2 for a maximally mixed qubit.
- Entanglement entropy is S = −Σ λ log₂ λ over the eigenvalues λ of the reduced matrix: 0 for a product state, 1 bit for one qubit of a Bell pair.

## Spin and adding spins (Binney & Skinner §7.4, p. 158; two spin-halves, §7.5, p. 173; UCSD notes ch. 21, p. 311)

- The Pauli matrices are the spin-½ operators, up to a factor of ħ/2.
- Two spin-halves combine into a triplet of three symmetric states and one singlet, (|01⟩ − |10⟩)/√2, which is |ψ−⟩.

## The two "fidelity" conventions

|⟨a|b⟩| is what QuTiP's fidelity() returns for pure states. |⟨a|b⟩|² is the probability that measuring b finds it in state a. For |0⟩ against |+⟩ they are 0.707 and 0.5. Always say which one you mean.
