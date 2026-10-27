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
## Canonical instructions

This is a Codex discovery entry. Read and follow the full [canonical skill](../../../skills/cross-model-accuracy-verifier/SKILL.md). Resolve any scripts, references, and assets relative to that canonical skill's directory. If it names a host tool that is unavailable in this session, say so and use the documented fallback where possible. Keep the canonical source in its original project folder; this entry only exposes it to Codex.
