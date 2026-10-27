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

# Sophisticated Prompt Generator

## Purpose

Turn one seed (a question, goal, or problem statement) into a suite of prompts that a person can run, test, and compare. The value is coverage: the same seed approached through ten different techniques, each with a check that tells you whether it worked.

## When to use

- The user gives one seed and wants a full prompt suite or many variants.
- The user asks for debug, audit, or verification prompts as part of the set.

## When not to use

- A single prompt rewrite or light polishing.
- Creative writing that does not need a structured set.
- Any task that does not produce prompts.

## Inputs

- **Seed** (required).
- Optional: audience, model type (reasoning, tool-using, standard), domain, length limits, safety constraints, output formats, and suite size.

If the seed is ambiguous in a way that would change the suite, ask up to three clarifying questions before generating. Otherwise, state your reading of the seed in one sentence and continue.

## Output

```
# Prompt Suite: <seed restated in one sentence>

## Generation Metadata
- Seed
- Suite size (topics x variants)
- Axes emphasised
- Assumptions made about the seed

## Topic 1 — <name>
### Prompt 1.1
<complete prompt, with {placeholders} only for the user's own data>
**Success check:** <an objective test the output can fail>
**Axes:** <primary axis; secondary tags>

### Prompt 1.2
...

## Topic 10 — Debug, Audit, Faithfulness & Meta
...
```

## The 10 topics (fixed)

1. **Core Execution & Zero/Few-Shot** — clean task prompts with constraints and residue handling.
2. **Reasoning Topology** — CoT, Least-to-Most, Tree-of-Thoughts, plan-then-execute.
3. **Structured Output & Schema Enforcement** — JSON, tables, schema-constrained decoding.
4. **Orchestration, Tool Use & Agent Patterns** — ReAct-style loops, chaining, hand-offs.
5. **Grounding, Retrieval & Context Anchoring** — answer only from supplied sources, with citations and a refusal path.
6. **Multi-Perspective & Specialist Lenses** — distinct viewpoints, each defined by what it checks (cost, risk, evidence, users), not by a character.
7. **Verification, Fact-Checking & Evidence Grading** — independent checks, evidence grades (SUPPORTED / PARTIALLY_SUPPORTED / CONTRADICTED / UNVERIFIED).
8. **Robustness, Adversarial & Edge Cases** — injection resistance, ambiguity, empty or contradictory input.
9. **Optimization, Compression & Refinement** — shorter versions, revise loops, Chain-of-Draft with few-shot drafts.
10. **Debug, Audit, Faithfulness & Meta** — prompt debugging, faithfulness audits of visible reasoning, failure diagnosis, security review.

**Suite size.** The default is 5 variants per topic (50 prompts). If the user asks for fewer, keep all 10 topics and use 3 or 4 variants each. Fewer, distinct prompts are better than filler.

Variants within a topic differ along: difficulty or depth; how explicit the reasoning is; how rigid the output is; the audience; and whether a self-check is included.

## Procedure

1. **Restate and scope the seed** in one sentence: domain, stakes, and whether independent review is worth its cost.
2. **Map the seed to each topic.** Specialise the fixed topics; do not invent new ones.
3. **Write the variants** using `references/seven-axis-checklist.md`. State decoding choices where they matter: low temperature for single-answer tasks, where the model accepts it; the number of candidates and how one is chosen, reasoning effort, and schema constraints. Temperature 0 is not deterministic in deployed systems, so say how a rerun will be checked.
4. **Build in checking.** Outside Topic 10, include at least one prompt with an internal self-check. Topic 10 is entirely debug, audit, and meta prompts.
5. **Add a success check to every prompt** that a wrong output would fail.
6. **Label the axes** for each prompt: one primary axis and any secondary tags.
7. **Audit the suite before delivery:**
   - every topic is present and Topic 10 is genuine audit work, not "check your work";
   - no two prompts are near-duplicates;
   - every prompt runs as written, with {placeholders} only for the user's data;
   - no persona lines ("You are an expert ..."); state the standard of work instead;
   - any number quoted in a prompt keeps its model, task, and source.
8. **Deliver** in the skeleton above.

## References

- `references/seven-axis-checklist.md` — the checklist used in step 3.
- `references/practical-frameworks.md` — quick everyday formulas, adapted without personas.
- `references/topic-templates.md` — templates and variation patterns for each of the 10 topics.
- `references/debug-audit-protocol.md` — patterns for Topic 10.
- `references/planetary-lenses.md` — what each Planetary Council planet checks, for Topic 6 when the seed benefits from the council's viewpoints. Use a planet's lens, meaning what it checks, not a voice or character.
- *The Taxonomy of Prompt Engineering*, Third Edition, and *The Prompt Construction Guide*, Second Edition — the evidence and the worked examples behind each technique.

## Scripts

This copy, in the Planetary Council plugin, includes the version 1.2 scripts. Run them from this skill's folder:

- `scripts/expand_suite.py` — fills fixed templates with the seed: `python scripts/expand_suite.py "SEED" -o suite.md`
- `scripts/validate_suite.py` — checks structure: `python scripts/validate_suite.py suite.md`
- `scripts/eval_harness.py` — heuristic scores: `python scripts/eval_harness.py suite.md`
- `scripts/expanders/topic_templates.py` — the expander's templates

They were run in this project on October 2, 2026, with these results:

- **Expander:** fills fixed templates with the seed. Every prompt still has to be specialised to the seed.
- **Validator:** checks structure only (counts, topics, success checks). It expects exactly 50 prompts, so it flags a smaller suite the user asked for.
- **Heuristic harness:** measures vocabulary, not quality. A nonsense suite of 50 "say the word banana" prompts, padded with the right keywords, scored 0.880, higher than a real suite at 0.857.
- **Model-judge hook:** an unfinished stub whose example code uses an OpenAI SDK call that was removed in 2023.

## Gotchas

- Keep all 10 topics; the fixed set is what gives coverage.
- Topic 10 must contain real audit prompts: faithfulness checks, failure diagnosis, injection review.
- For a very narrow seed, raise it to a more general framing so every topic still applies, and say that you did.
- Prefer measurable success checks over "be accurate".
- Judge the suite by whether its prompts run and their checks can fail, not by a harness score.
