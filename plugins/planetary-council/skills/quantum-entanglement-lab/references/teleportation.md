# Quantum Teleportation Resource Table

## Resources required
- 1 ebit (shared Bell pair, usually |φ+⟩)
- 2 classical bits (result of Alice’s Bell measurement)

## Protocol summary
1. Alice holds the unknown message qubit and her half of the Bell pair.
2. Alice applies CNOT (message = control, her share = target) then H on the message qubit.
3. Alice measures both qubits in the computational basis → two classical bits.
4. Alice sends the two bits to Bob.
5. Bob applies the correction:

| Bits | Correction |
|------|------------|
| 00   | I          |
| 01   | X          |
| 10   | Z          |
| 11   | Z X        |

The first bit is Alice’s result on the message qubit and selects Z; the second is her result on her half of the pair and selects X. So 01 means X only and 10 means Z only, as in the lab script.

After the correction Bob’s qubit is in the original message state.  
The original message qubit is measured (and therefore destroyed) by Alice; only the state is transferred.
