# Prompt Suite Method

*Extracted October 2, 2026 from the Planetary Council package's prompt-generator skill (version 1.2), with the character personas removed; updated October 3, 2026. Evidence class: project method, AI-assisted, not benchmarked. Builds on claude/taxonomy-of-prompt-engineering-3e.md and claude/prompt-construction-guide-2e.md. The corrected skill itself is skills/sophisticated-prompt-generator/ (version 1.2.1).*

## The taxonomy edition

The generator follows *The Taxonomy of Prompt Engineering*, Third Edition. That edition has seven axes: it adds **Decoding & Inference Compute** as Axis 4 and moves Self-Consistency and schema-constrained decoding there. The checked Third Edition is now in this project as claude/taxonomy-of-prompt-engineering-3e.md.

## What the method does

It turns one seed question into a set of prompts covering ten areas, with five variants each, and every prompt ends in a success check. It is most useful for test suites, where a model, skill or agent is stress-tested from many angles, and for exploring different ways to ask the same question.

## Seven-axis checklist (for each prompt)

1. **Contextual Conditioning:**
   - an operation verb;
   - the standard of work stated as behavior, not as a persona;
   - constraints;
   - rules for unusual input (empty, ambiguous, multi-fit, contradictory and out-of-scope);
   - positive instructions with their reasons, plus "do not" lines only for known failures.
2. **Representation:** a declared output format; consistent delimiters; compression or expansion chosen on purpose; for long contexts, critical instructions at both the start and the end.
3. **Reasoning Topology:** none, linear steps, decompose-then-solve, tree or graph search, or plan-then-execute. Pick the lightest shape that closes a measured gap.
4. **Decoding & Inference Compute:**
   - low temperature when one answer is right, and higher only when variety is the goal and a later step selects;
   - several samples plus a vote, or best-of-N with a verifier written before sampling;
   - on reasoning models, state the goal, constraints and format instead of "think step by step";
   - schema-constrained decoding when a parser reads the output; it guarantees the form, not the truth.
5. **Orchestration & Grounding:** a single call, tool calls, retrieval ("answer only from the provided context"), hand-offs, or several perspectives.
6. **Optimization:** length control, critique-and-revise against an external signal, staged refinement, compression.
7. **Verification & Security:** success criteria you can check; evidence grades; contradictions and uncertainty brought into the open; injection defense; faithfulness language when reasoning is shown.

## Ten coverage areas (five variants each)

1. **Core execution:**
   - zero-shot with full rules for unusual input;
   - few-shot with 2–3 boundary examples;
   - a stated standard of work;
   - extremely constrained output;
   - the same task for an expert and for a beginner.
2. **Reasoning shape:** linear steps; decompose then solve; explore alternatives; three independent paths then a vote; plan, then execute separately.
3. **Structured output:** strict JSON with required keys and a null policy; a fixed-column table; YAML or TOML; tagged sections; free reasoning followed by a schema block.
4. **Tools and agents:** a thought/action/observation loop; an explicit tool list with when to call each; a hand-off brief to a specialist; parallel calls then a synthesis; multi-turn memory rules.
5. **Grounding:** "only from this context, otherwise UNKNOWN"; citations with source IDs; contradiction detection inside the context; long-context position rules; staged context windows.
6. **Multiple perspectives:**
   - evidence hunter plus precision checker;
   - power and incentives plus rules and time;
   - risk plus synthesis;
   - the four-stage review skeleton;
   - an independent verifier on top of another perspective (see claude/multi-lens-review-method.md).
7. **Verification:**
   - claim extraction with a status per claim;
   - confidence plus source class;
   - an attempt to falsify;
   - a cross-source consistency check;
   - "list every assumption that would change the answer if it were false."
8. **Robustness:** injection defense; contradictory instructions; empty, gibberish or off-topic input; an adversarial test of the prompt itself; ambiguity rules that force a clarifying question.
9. **Optimization:** 40% shorter with the same behavior; draft, critique, final; a token budget; samples plus a vote; three variants, then pick the strongest.
10. **Debug and audit (always included):** the five prompts below.

## Five debug and audit prompts

1. **Failure diagnosis:** given the prompt, the bad output and the expected behavior, name the axis that failed, quote the language that caused it, rewrite it, and give a success check for the rewrite.
2. **Faithfulness audit:** given a reasoning trace, judge whether the steps actually drove the answer or were written afterward, and flag unsupported leaps. Visible reasoning is generated text, not a log of the computation, so check high-stakes conclusions independently.
3. **Seven-axis audit:** score a prompt 0–2 on each axis and give a prioritized fix list.
4. **Security review:** instruction-hierarchy weaknesses, remaining attack surfaces, and hardening language.
5. **Improver:** return a strictly better version with a changelog tied to the axes.

## Before delivering a suite

- Every prompt is complete and usable as written, with {placeholders} only for the user's data.
- No near-duplicates.
- Every prompt ends with a success check that a wrong output would fail.
- The debug and audit area holds real diagnostics, not "check your work."
- No persona lines.

## What was tested, and the limits found

- **The scripts run.** The expander turned a test seed into 50 prompts, the validator passed them, and the quality harness scored them 0.857 (its bar is 0.55).
- **The quality harness measures vocabulary, not quality.**
  - A suite of 50 prompts that each say "say the word banana", padded with the right keywords, passed the validator and scored 0.880, higher than the real suite.
  - Treat the harness as a format check.
  - Real quality means running the prompts on actual tasks and grading the outputs. The guide's §28 says to score candidates by running them, never by asking a model how good they look.
- **The optional model judge is an unfinished stub,** and its example code uses an OpenAI SDK call that was removed in 2023.
- **The deterministic expander fills fixed templates with the seed.** It makes a useful skeleton, not tailored prompts.
- **A fixed 50 is a quota.** On a narrow seed it forces filler, which goes against the manual's minimal-sufficient-structure rule. Use the ten areas as a coverage menu, and keep the full 50 only when the goal is a broad test suite. Version 1.2.1 of the skill allows 3–5 variants per topic.
- **Where the scripts are.** They stay in the Planetary package (`sophisticated-prompt-generator/scripts/`) and were not copied here.
