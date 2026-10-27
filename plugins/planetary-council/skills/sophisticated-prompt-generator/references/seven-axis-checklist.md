# Seven-Axis Checklist for Every Generated Prompt

Derived from *The Taxonomy of Prompt Engineering*, Third Edition. A good prompt makes a deliberate choice on most axes. A technique's primary axis is where its defining component lives; the other axes it touches are secondary tags (manual Section 6.2).

## Axis 1 — Contextual Conditioning

- [ ] A clear operation verb ("classify", "extract", "diagnose", "summarize").
- [ ] The standard of work stated as behavior ("return only corrected text"), not as identity. Personas did not improve accuracy across 162 personas and 2,410 MMLU questions (Zheng et al., Findings of EMNLP 2024); use a role only for tone or format.
- [ ] Constraints: length, vocabulary, what must be preserved.
- [ ] Residue handling: what to do with empty, ambiguous, multi-fit, contradictory, or out-of-scope input.
- [ ] Say what to do, and give the reason. Add a "Do not ..." line only for a specific known failure.
- [ ] For long inputs, put critical instructions at the beginning and repeat them at the end; models use the middle of a long context less well (Liu et al., "Lost in the Middle").

## Axis 2 — Representation

- [ ] Output format declared (JSON schema, Markdown sections, table, numbered list, prose).
- [ ] Delimiters consistent and easy to parse.
- [ ] Compression chosen on purpose. Chain-of-Draft needs few-shot drafts; zero-shot it fell to 65.5% against CoT's 90.4% on GSM8K with Claude 3.5 Sonnet (Xu et al., 2025).

## Axis 3 — Reasoning Topology

- [ ] One of: no intermediate steps; linear CoT; Least-to-Most; Tree or Graph of Thoughts; program of thoughts.
- [ ] Choose the lightest topology that closes a measured gap. On reasoning models, explicit CoT gave small or negative accuracy changes and took 20–80% longer (Meincke et al., 2025).

## Axis 4 — Decoding & Inference Compute

- [ ] Temperature or sampling stated when it matters (low for single-answer tasks, where the model accepts it). Some models reject any non-default temperature: on Claude's 5.x-era models a `temperature` setting returns an error (checked October 12, 2026), so check the model's documentation first.
- [ ] Number of candidates and how one is chosen (majority vote, verifier, tests, judge).
- [ ] Reasoning-effort setting, when the model exposes one; check current documentation for names and values.
- [ ] Schema- or grammar-constrained decoding when the format must be guaranteed; still validate in code.
- [ ] A note that temperature 0 is not deterministic in deployed systems (Thinking Machines Lab, 2025: 1,000 temperature-0 completions of one prompt gave 80 unique outputs).

## Axis 5 — Orchestration & Grounding

- [ ] Single call; or tool calling; or retrieval with "answer only from the provided sources"; or a multi-step hand-off; or independent parallel review.
- [ ] Tools listed with their inputs, outputs, and error behavior; least privilege for anything with side effects.

## Axis 6 — Optimization

- [ ] Length control.
- [ ] A revise loop with an external signal (tests, a validator, a separate evaluator) rather than unaided self-critique.
- [ ] Staged refinement or compression when token cost matters.

## Axis 7 — Verification & Security

- [ ] A success check that a wrong output would fail.
- [ ] Evidence grades where facts are claimed: SUPPORTED / PARTIALLY_SUPPORTED / CONTRADICTED / UNVERIFIED.
- [ ] Contradictions and uncertainty surfaced, not smoothed over.
- [ ] Prompt-injection defense when untrusted text is present: mark the untrusted text, give the model no tools while it reads it, and enforce permissions in code.
- [ ] When visible reasoning is used, treat it as generated text, not a causal record. Claude 3.7 Sonnet verbalized a hint it used 25% of the time on average (Chen et al., 2025).

## For the whole suite

- Each topic exercises a different mix of primary axes.
- Topic 10 leans heavily on Axis 7 and on improving the prompts themselves.
- Every prompt ends with a **Success check:** line.
- Accuracy changes are in percentage points, and every number keeps its model and task.
