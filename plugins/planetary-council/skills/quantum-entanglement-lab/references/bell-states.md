# Bell States and Local Pauli Actions

## The four maximally entangled two-qubit states

```
|φ+⟩ = 1/√2 (|00⟩ + |11⟩)
|φ-⟩ = 1/√2 (|00⟩ − |11⟩)
|ψ+⟩ = 1/√2 (|01⟩ + |10⟩)
|ψ-⟩ = 1/√2 (|01⟩ − |10⟩)   (the singlet)
```

For any of these, the reduced density matrix of one qubit is completely mixed:
ρ_A = (1/2) I. Local measurement yields a random bit and reveals nothing about which Bell state was prepared.

## Local operations (Alice holds the first qubit)

- X_A |φ+⟩ → |ψ+⟩
- Z_A |φ+⟩ → |φ-⟩
- X_A |φ-⟩ → −|ψ-⟩
- Z_A |ψ+⟩ → |ψ-⟩

These operations flip the parity bit or the phase bit but leave ρ_A unchanged. The information remains hidden until a joint measurement or classical communication of correlators is performed.
