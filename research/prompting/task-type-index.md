# Task-Type Index for Prompt Engineering

**Companion to** *The Taxonomy of Prompt Engineering* (Third Edition) and *The Prompt Construction Guide* (Second Edition) · **Version:** October 2026 · **Aligned with** the seven-axis taxonomy

Find the job you need to do. Start with the technique in the **Start with** column. Move to **Then consider** only when a measurement on your own data shows the first choice falling short. Section signs (§) point to the guide; "Section" points to the manual.

| **If you need to…** | **Start with** | **Then consider** | **Primary axis** |
|---|---|---|---|
| Answer from documents you have | Context anchoring (§4) | Retrieval (§15); Chain-of-Verification (§19) | 1 Contextual Conditioning |
| Answer from a large or changing collection | Retrieval-augmented generation (§15) | Chain-of-Verification (§19); factuality check (Example 20.4) | 5 Orchestration & Grounding |
| Extract fields for another system | Schema-constrained generation (§18) | Reflexion against the validator (§17); settings in Example 34.1 | 4 Decoding & Inference Compute |
| Classify or triage | Few-shot (§2) with a schema enum (§18) | Routing (§23); self-consistency on costly classes (§10) | 1, with 4 for the schema |
| Edit text someone supplied | Context anchoring (§4) with constraint framing (§5) | Evaluator-optimizer (§26) | 1 Contextual Conditioning |
| Draft a document or message | System rules (§3) and a template (§6) | Prompt chaining (§22); Chain-of-Verification on facts (§19) | 1 and 2 Representation |
| Compute a number | Program-of-Thoughts (§13) | Self-consistency over programs (§10) | 3 Reasoning Topology |
| Solve a multi-step problem on a non-reasoning model | Chain-of-Thought (§9) | Least-to-Most (§11); Tree-of-Thoughts (§12) | 3 Reasoning Topology |
| Cut the cost of reasoning | Chain-of-Draft, few-shot only (§7) | Routing by difficulty (§23; Example 34.5) | 2 Representation |
| Reduce run-to-run variation | Decoding controls (§34) | Self-consistency (§10) | 4 Decoding & Inference Compute |
| Use tools or take actions | ReAct (§16) | Reflexion (§17); orchestrator-workers (§25) | 5 Orchestration & Grounding |
| Check a conclusion before acting on it | Disconfirmation pass (§21) | Independent parallel review (§35); debate (§27) | 7 Verification & Security |
| Score outputs at volume | LLM-as-a-judge (§20) | Independent parallel review (§35) | 7 Verification & Security |
| Review a document or prompt with several models | Independent parallel review (§35) | Independent-model disconfirmation (Example 21.5) | 7 Verification & Security |
| Tune a prompt that runs at scale | Automated optimization (§28), after the decision harness (Example 28.5) | — | 6 Optimization |
| Defend against prompt injection | Least privilege, with permissions enforced in code, and marking of untrusted text (spotlighting) (manual Section 17.3) | Isolation patterns such as the quarantine design, where the call with tools never sees untrusted prose (manual Section 17.3) | 7 Verification & Security |
| Handle long context without losing information in the middle | Critical instructions at the beginning, repeated at the end (manual Section 7.4 and Chapter 4) | Retrieve the relevant passages instead of pasting everything (§15) | 1 Contextual Conditioning |
| Check whether visible reasoning can be trusted | Verify the conclusion externally: re-derive it independently and compare (§21; Example 21.5) | Independent parallel review (§35) | 7 Verification & Security |
| Route easy and hard traffic | A small-model router with explicit labels (§23; Example 34.5) | Reasoning effort chosen by measurement (Example 34.4), with accuracy logged separately for each path | 5, with 4 for effort |

The last four rows go beyond the guide's own task index. Each points to the manual section that holds the evidence.

## Quick decision rules

1. **Start with the lightest technique that can work.** Try zero-shot with clear rules for unusual input first. Add few-shot examples when the content is right but the shape is wrong.
2. **Measure before adding layers.** Every extra call, candidate, or reasoning structure multiplies cost and latency.
3. **Set decoding controls on purpose, and measure them.** State temperature, number of candidates, reasoning effort, and schema constraints. Don't tune temperature to fix what is really a prompt or grounding problem (manual Section 10.1). Temperature 0 does not guarantee identical reruns.
4. **Visible reasoning is not an audit trail.** Treat it as generated text, and verify independently when the stakes are high (manual Chapter 15).
5. **Re-measure after every model upgrade.** Effects measured on 2022–2023 models often shrink on current reasoning models (manual Sections 7.2 and 9.1).

## Mapping to the seven axes

| **Axis** | **Techniques in this index** |
|---|---|
| 1. Contextual Conditioning | Zero-shot, few-shot, system rules, context anchoring and placement, constraint framing |
| 2. Representation | Templates, Chain-of-Draft, Chain-of-Symbol, prompt compression |
| 3. Reasoning Topology | Chain-of-Thought, Least-to-Most, Tree-of-Thoughts, Program-of-Thoughts |
| 4. Decoding & Inference Compute | Sampling controls, self-consistency, best-of-N with a verifier, reasoning effort, schema-constrained decoding |
| 5. Orchestration & Grounding | Retrieval-augmented generation, ReAct, prompt chaining, routing, orchestrator-workers, multi-agent debate |
| 6. Optimization | Automated prompt search and compilation (APE, OPRO, GEPA, DSPy) |
| 7. Verification & Security | Chain-of-Verification, LLM-as-a-judge, disconfirmation, independent review, prompt-injection defenses |

A technique's primary axis is where its defining component lives; everything else it touches is a secondary tag (manual Section 6.2).

*This index is a design aid. It is not a substitute for an evaluation set built from your own traffic.*
