---
name: sophisticated-prompt-generator
description: >
  Generates a structured suite of prompts from one seed question or goal. By
  default it writes 50 prompts in 10 fixed topics (5 variants each), places
  each prompt on the seven-axis taxonomy (Contextual Conditioning,
  Representation, Reasoning Topology, Decoding & Inference Compute,
  Orchestration & Grounding, Optimization, Verification & Security), includes
  a dedicated debug and audit topic, and ends every prompt with a success
  check. Use when the user asks for a prompt suite, many prompt variants, or
  "50 prompts" from one idea. Do not use for a single prompt rewrite or for
  tasks that are not about prompts.
license: MIT
metadata:
  claude-app-description: "Turns one seed question into a suite of 50 prompts in 10 topics, each placed on the seven-axis prompt taxonomy, with debug and audit variants. Use for a prompt suite. Not for a single rewrite."
  version: "1.2.1"
  taxonomy: "seven-axis (The Taxonomy of Prompt Engineering, Third Edition)"
---
## Canonical instructions

This is a Codex discovery entry. Read and follow the full [canonical skill](../../../plugins/planetary-council/skills/sophisticated-prompt-generator/SKILL.md). Resolve any scripts, references, and assets relative to that canonical skill's directory. If it names a host tool that is unavailable in this session, say so and use the documented fallback where possible. Keep the canonical source in its original project folder; this entry only exposes it to Codex.
