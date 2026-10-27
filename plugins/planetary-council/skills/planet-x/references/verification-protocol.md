# Planet X — Verification Protocol
**Inherits and extends patterns from the project’s cross-model-accuracy-verifier skill.**

## Atomic Claim Extraction
Break any text or assertion into the smallest verifiable propositions.
- One claim = one proposition that can be true or false.
- Label each: C1, C2, …

## Classification
- FACT — empirically checkable
- INFERENCE — reasoned from facts
- OPINION — value judgement
- UNCLEAR — cannot be classified cleanly

Only FACT and INFERENCE enter the verification loop.

## Verification Loop (per claim)
1. State what would count as primary evidence.
2. Search or request primary sources; cite only what was actually opened, otherwise UNVERIFIED.
3. Record: Source title / identifier / date; direct quote or data point.
4. Assign Support Status:
   - SUPPORTED
   - PARTIALLY_SUPPORTED
   - CONTRADICTED
   - UNVERIFIED
5. Assign Confidence 1–10 and Source Class.

## Aggregate Score (when useful)
Accuracy ≈ (SUPPORTED + 0.5 × PARTIALLY_SUPPORTED) / (FACT + INFERENCE claims)

## Matrix Decision
If any claim or finding meets Matrix trigger conditions (shared/matrix-protocol.md), put the sensitive, non-actionable content in a MATRIX APPENDIX at the end of the answer (or references/matrix.md where the host allows file writes) and emit only a pointer in the main answer. Anything that would be refused is declined, not diverted.
