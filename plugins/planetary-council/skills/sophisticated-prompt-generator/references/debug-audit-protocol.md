# Debug / Audit / Meta Protocol (Topic 10)

Topic 10 is non-negotiable and must contain genuine diagnostic power.

## Required coverage inside the 5 prompts of Topic 10

1. **Prompt Failure Diagnosis**  
   Input: original prompt + observed bad output + optional expected behaviour.  
   Output: which axes failed, concrete rewrite, and a success check for the rewrite.

2. **Faithfulness / CoT Audit**  
   Given a reasoning trace, determine whether the visible steps are causally necessary or post-hoc rationalisation. Surface unsupported leaps.

3. **Seven-Axis Structural Audit**  
   Score a supplied prompt on each of the seven axes (0–2) and produce a prioritised improvement list.

4. **Security & Injection Surface Review**  
   Identify instruction-hierarchy weaknesses, residual attack surfaces, and hardening language.

5. **Meta-Prompt Improver**  
   Take any mediocre prompt related to the seed and return a strictly superior version with an explicit changelog of what changed and why (tied to axes).

## Shared language to use
- Support Status: SUPPORTED | PARTIALLY_SUPPORTED | CONTRADICTED | UNVERIFIED
- Confidence: 1–10
- Axis scores and failure modes from the seven-axis checklist
- “Visible reasoning is a generated artifact, not a causal log” (faithfulness reminder)

These prompts must themselves be high-quality examples of the skill they teach.
