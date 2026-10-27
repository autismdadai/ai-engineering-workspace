---
name: cross-model-accuracy-verifier
description: >
  Verifies factual claims in AI-generated text across multiple models by extracting
  atomic claims, requiring primary-source checks, scoring support, and producing a
  structured accuracy report. Use when the user asks to fact-check, verify accuracy,
  measure hallucination rate, compare model outputs, score truthfulness, or reduce
  fabrication. Do not use for creative writing, pure opinion, or irreversible actions.
license: MIT
metadata:
  claude-app-description: "Fact-checks AI-written text: splits it into single claims, checks each against primary sources, scores support and writes an accuracy report. Not for creative writing, opinion or irreversible actions."
  version: "1.0"
  author: expert-skill-builder
  purpose: multi-model accuracy measurement without side effects
---
# Cross-Model Accuracy Verifier

## Purpose
Reduce fabrication by forcing every material claim through an explicit, auditable verification loop. Works the same way whether the output came from one model or many. Manual input only—never executes external writes, sends, deploys, or spends.

## Procedure (follow in order)
1. **Collect inputs**
Ask the user (or read from the message) for:
- The exact text(s) to verify
- The original question or task that produced them
- Any preferred primary sources or domains
- Whether a numeric score is required

2. **Extract atomic claims**
Break the text into the smallest verifiable statements. Rules: one claim = one proposition that can be true or false.
C1: <cleaned claim> [source sentence: "..."]

3. **Classify each claim**
- FACT / INFERENCE / OPINION / UNCLEAR
Only FACT and INFERENCE enter the verification loop.

4. **Verification loop (per claim)**
1. State what would count as primary evidence.
2. Search or request primary sources.
3. Record: Source title, URL or identifier, date; Direct quote or data point.
4. Assign support status: SUPPORTED, PARTIALLY_SUPPORTED, CONTRADICTED, or UNVERIFIED.

5. **Score**
Accuracy = (SUPPORTED + 0.5 * PARTIALLY_SUPPORTED) / (FACT + INFERENCE claims)
Report overall accuracy (0-100%), count of each status, and list of CONTRADICTED and UNVERIFIED claims.

6. **Output format**
Use a strict Markdown table output.
