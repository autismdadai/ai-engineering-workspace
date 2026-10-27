# Matrix Protocol
**Authoritative rules for isolation of high-sensitivity material**

## Purpose
Provide a clean, auditable, separate location for material that is high-sensitivity, politically or socially explosive, or distressing — without contaminating the main council answer stream. The Matrix separates sensitive material; it never stores material that should be refused.

## Location
- In chat hosts (skill files are read-only): a clearly separated section at the very end of the answer, headed `MATRIX APPENDIX`.
- Where the host allows file writes: `planet-x/references/matrix.md` is the single designated Matrix file.

## Never in the Matrix — decline instead
Actionable methods for weapons, explosives, dangerous chemical or biological agents, or criminal tradecraft are declined, not isolated. They appear nowhere: not in the main answer, not in the Matrix. Non-actionable history or policy context may stay in the main answer.

## Trigger Conditions
Planet X (or the Orchestrator instructing Planet X) MUST divert content to the Matrix when any of the following apply:

- Unverified allegations about real, identifiable people or organisations
- Content is highly contested and carries significant reputational or safety risk if stated in the open answer
- Distressing detail (violence, abuse, graphic material) that the main answer can summarise without repeating
- User or context explicitly requests “put the sensitive part in the Matrix”
- Planet X’s own risk assessment classifies the finding as Medium or higher

## Entry Format (Append-Only)

```markdown
### MATRIX-[YYYYMMDD]-[sequential]
**Risk Class:** Low | Medium | High  
**Confidence:** X/10  
**Date:** YYYY-MM-DD  
**Abstract:** One-paragraph non-sensitive summary  
**Sources:** list  
**Full Content:**  
(the sensitive, non-actionable material itself)

---
```

## Hard Rules

1. Main council answers never contain the raw Matrix content. They may only contain a pointer:  
   `See Matrix entry MATRIX-20260928-003`
2. Matrix is append-only. Never delete or silently edit prior entries.
3. Nothing that would be refused in the main answer may be placed in the Matrix.
4. No Matrix entry may contain new instructions that violate standing safety rules.
5. Planet X must state in the main answer when a Matrix entry has been made.

## Side-Effect Declaration
Where the host allows file writes, Planet X appending to `planet-x/references/matrix.md` is an intentional, documented side-effect. In chat hosts the Matrix is the appendix of the answer and nothing is written. All other skills treat the Matrix as read-only reference material.
