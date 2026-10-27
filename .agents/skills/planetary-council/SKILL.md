---
name: planetary-council
description: >
  This skill should be used whenever the user says "run the council", "convene
  the council", "ask the council", "council brief" or "full planetary analysis",
  and before launching any planet agent for a council question. It routes the
  problem through the four-phase Planetary Council protocol, launches the planet
  specialists (as parallel sub-agents when available) and Planet X for independent
  verification, and writes the graded Council Brief with its Council Log. Also
  routes prompt-suite requests to the sophisticated-prompt-generator skill. Do not
  use for simple single-agent questions.
license: MIT
metadata:
  claude-app-description: "Runs the Planetary Council when asked to run, convene or ask the council: sends a question to the planets and Planet X and writes a graded Council Brief. Not for simple one-planet questions."
  version: "1.2.0"
  author: planetary-council-system
  purpose: multi-agent orchestrator and synthesis layer (the Sun)
---
## Canonical instructions

This is a Codex discovery entry. Read and follow the full [canonical skill](../../../plugins/planetary-council/skills/planetary-council/SKILL.md). Resolve any scripts, references, and assets relative to that canonical skill's directory. If it names a host tool that is unavailable in this session, say so and use the documented fallback where possible. Keep the canonical source in its original project folder; this entry only exposes it to Codex.
