# Topic Templates & Variation Patterns

Each of the 10 topics receives exactly 5 prompts. Below are the design intents and variation axes to use when specialising the seed.

## Topic 1 — Core Execution & Zero/Few-Shot
**Intent:** Cleanest possible task prompts that handle residue.
**Variation patterns:**
1. Pure zero-shot with exhaustive residue rules
2. Few-shot with 2–3 boundary examples
3. Role-conditioned but still residue-heavy
4. Extremely constrained output (single token / short phrase)
5. Audience-adapted (expert vs novice) while keeping the same core task

## Topic 2 — Reasoning Topology
**Intent:** Force different shapes of intermediate computation.
**Variation patterns:**
1. Classic linear Chain-of-Thought
2. Least-to-Most (decompose then solve)
3. Tree-of-Thoughts style exploration of alternatives
4. Self-Consistency instruction (“generate 3 independent paths then vote”)
5. Plan-then-execute with explicit separation of plan and answer

## Topic 3 — Structured Output & Schema
**Intent:** Parser-friendly, schema-constrained results.
**Variation patterns:**
1. Strict JSON with required keys + null policy
2. Markdown table with fixed columns
3. YAML or TOML
4. XML-style tagged sections
5. Hybrid: free reasoning then final schema-enforced block

## Topic 4 — Orchestration, Tool-Use & Agents
**Intent:** Prompts ready for tool-calling or multi-step agents.
**Variation patterns:**
1. ReAct-style Thought/Action/Observation loop
2. Explicit tool inventory + when to call
3. Multi-agent hand-off (“pass to specialist X with this brief”)
4. Parallel tool calls + synthesis
5. Stateful multi-turn agent memory instructions

## Topic 5 — Grounding, Retrieval & Context Anchoring
**Intent:** Prevent hallucination by binding to supplied context.
**Variation patterns:**
1. “Answer only from the following context; otherwise say UNKNOWN”
2. Citation-required with source IDs
3. Contradiction detection inside the context
4. Long-context position awareness (“priority to beginning and end”)
5. Progressive context windowing instructions

## Topic 6 — Multi-Perspective & Planetary Council Lenses
**Intent:** Inject distinctive specialist voices and force steel-manning.
**Variation patterns:**
1. Mercury (truth-hunting / OSINT) + Venus (empirical precision)
2. Jupiter (power map) + Saturn (temporal / legal)
3. Pluto (shadow / X-risk) + Earth (synthesis)
4. Full four-phase council brief skeleton
5. Planet X independent verification layer on top of another perspective

## Topic 7 — Verification, Fact-Checking & Evidence Grading
**Intent:** Independent checking and graded confidence.
**Variation patterns:**
1. Claim extraction + support status (SUPPORTED / PARTIALLY / CONTRADICTED / UNVERIFIED)
2. Confidence 1–10 + source class
3. Adversarial fact-check (try to falsify)
4. Cross-model or cross-source consistency check
5. “List every assumption that if false would change the answer”

## Topic 8 — Robustness, Adversarial & Edge Cases
**Intent:** Survive messy, malicious, or underspecified input.
**Variation patterns:**
1. Prompt-injection defence language
2. Explicit handling of contradictory instructions
3. Empty / gibberish / off-topic input protocols
4. Jailbreak-style adversarial test of the prompt itself
5. Ambiguity resolution rules with forced clarification questions

## Topic 9 — Optimisation, Compression & Iterative Refinement
**Intent:** Better, shorter, or self-improving versions.
**Variation patterns:**
1. “Rewrite this prompt to be 40 % shorter while preserving behaviour”
2. Progressive refinement loop (draft → critique → final)
3. Token-budget constrained version
4. Self-consistency + majority vote instruction
5. Meta-optimisation: generate three variants then select the strongest

## Topic 10 — Debug, Audit, Faithfulness & Meta-Prompt (Mandatory)
**Intent:** Diagnose, audit, and improve prompts and reasoning traces.
**Variation patterns (must cover these):**
1. Prompt debugger: given a failing prompt + bad output, diagnose the axis failure
2. Faithfulness audit: “Is the visible CoT causally responsible or post-hoc narrative?”
3. Full seven-axis audit of a supplied prompt
4. Security / injection surface review
5. Meta-prompt improver: take a mediocre prompt and return a strictly superior version with changelog

Always specialise every template to the user’s seed. Never leave the seed generic.
