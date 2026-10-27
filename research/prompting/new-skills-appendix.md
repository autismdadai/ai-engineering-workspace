# New Skills Appendix

**October 2026** · Companion to *Agent Skills and Advanced Prompt Engineering Reference* (version 1.2). Post-edition notes of October 20, 2026 in Sections 1 and 4. Updated 6–7 October 2026: quantum-entanglement-lab 1.2.1, its eval pack and test results, two new skills (trig-check and qubit-math), and project paths in Section 2.

This appendix records skills and skill-related files added or materially changed after the original skills catalog, aligned to the **seven-axis taxonomy**. Each status line says what was checked in this project and what could not be.

---

## 1. sophisticated-prompt-generator 1.2.1

**Status.** The SKILL.md and its two reference files were reviewed and corrected in this project. The version 1.2 scripts and two further reference files live in the Planetary Council package, not in this project. They were run here on October 2, 2026: the scripts work, but the quality harness can be gamed (see below).

**What changed from 1.1 to 1.2** (as described by the 1.2 files)

- The taxonomy target moved from six axes to **seven**, adding **Decoding & Inference Compute** as Axis 4.
- The expander was said to emit decoding-aware variants for Topics 2, 3, 9, and 10: self-consistency or best-of-N with an explicit N and selection rule, plan-then-execute with a temperature or reasoning-effort note, schema-constrained decoding notes, and low-temperature settings for structured output. *Post-edition note (October 20, 2026):* use those settings only where the model accepts them; Claude's 5.x-era models reject any non-default temperature (Engineering Stack, Part 03).
- The checklist became `references/seven-axis-checklist.md`, and the practical frameworks file was updated to seven-axis language.

**What changed from 1.2 to 1.2.1** (this project)

- Topic 6 is "Multi-Perspective & Specialist Lenses". The leftover "Planetary Council" topic name and lens metadata are removed; each viewpoint is defined by what it checks, not by a character.
- Persona lines are removed from the practical frameworks. Personas did not improve accuracy across 162 personas and 2,410 MMLU questions (Zheng et al., Findings of EMNLP 2024).
- The skill may ask up to three clarifying questions when the seed is ambiguous.
- The suite size is 50 by default (10 topics × 5 variants); the user may ask for 3 or 4 variants per topic to avoid filler.
- The harness score is no longer presented as a quality bar. Run in this project, the version 1.2 harness scored a nonsense suite 0.880, above a real suite at 0.857. It checks structure, not quality.
- The checklist's negative-instruction item now says to state what to do and why, adding "do not" lines only for a known failure, as vendor guidance advises.
- Axis names match the manual: Contextual Conditioning, Representation, Reasoning Topology, Decoding & Inference Compute, Orchestration & Grounding, Optimization, Verification & Security.

**How to invoke.** Give one seed and ask for a prompt suite. With the version 1.2 scripts from the Planetary Council package, the deterministic path is:

```bash
python scripts/expand_suite.py "your seed question" -o suite.md
python scripts/validate_suite.py suite.md
```

Treat the expander's output as templates to specialise, and judge the suite by whether each prompt runs and each success check can fail.

---

## 2. Supporting files in the final set

| File | Purpose |
|------|---------|
| `skills/sophisticated-prompt-generator/SKILL.md` | The corrected skill, version 1.2.1 |
| `skills/sophisticated-prompt-generator/references/seven-axis-checklist.md` | Checklist for all seven axes, including Decoding |
| `skills/sophisticated-prompt-generator/references/practical-frameworks.md` | Everyday formulas, without persona lines |
| `claude/taxonomy-of-prompt-engineering-3e.md` | The authoritative seven-axis manual |
| `claude/prompt-construction-guide-2e.md` | Build steps and 150 worked examples |
| `claude/task-type-index.md` | Task-to-technique lookup aligned to the seven axes |
| `claude/edition-protocol-v3.md` | The verification-first revision protocol behind the Third Edition |
| `claude/verification-and-benchmark-report.md` | What was checked in the final editions, how, and what remains unverified |

PDF copies of these documents, and a combined volume of all of them, are kept outside the project for reading and sharing.

---

## 3. Other skills

| Skill | Status in this project |
|-------|------------------------|
| **quantum-entanglement-lab** | Version 1.2.1 is the current one, in `skills/quantum-entanglement-lab/` with its script in `scripts/` and an eval pack in `evals/`. Version 1.1 checked teleportation on six message states and checked that every hand-built gate is unitary; version 1.0 tested only the \|+⟩ state, which let a broken correction pass. Version 1.2 makes three more checks able to fail: partial measurement now checks the state each outcome leaves, CHSH must equal 2√2, and the script refuses to run under `python -O`. The eval pack's mutation check passed 16 of 16 runs on 1.2 and 12 of 16 on 1.1 (6 October 2026, QuTiP 5.3.1). In a quick with-and-without test (7 October, one run per task per condition) answers met their rubric in 7 of 7 tasks with the skill and 6 of 7 without; the difference was running the lab. Version 1.2.1 adds the sentence that test showed the teleportation card was missing, and a 197-character description for the Claude app. Its trigger tests have not been run. |
| **trig-check** | New, version 1.0, in `skills/trig-check/`. Exact trigonometry with a SymPy script. 21 known-answer tests pass, and its mutation check catches all 12 deliberate bugs (7 October 2026). Trigger tests and with-and-without runs not yet run. |
| **qubit-math** | New, version 1.0, in `skills/qubit-math/`. Small qubit calculations with a numpy script. 25 known-answer tests pass, and its mutation check catches all 13 deliberate bugs (7 October 2026). Trigger tests and with-and-without runs not yet run. |
| **skill-builder** | Described in the Agent Skills reference. Its files are not in this project, so its validation could not be checked here. |
| **cross-model-accuracy-verifier** | The method is in the project as `claude/research-verification-toolkit.md` (claim-by-claim checks and evidence grades). The packaged skill's files are not in this project. |
| **server-log-triager** | Described in the Agent Skills reference. Its script is not in this project, so its PII redaction could not be tested here. |

The multi-agent orchestration pattern is kept as a hierarchical orchestrator, the minimum set of specialists, a synthesis step, and an independent verifier, without personas (`claude/multi-lens-review-method.md`). The persona version lives in its own separate project.

---

## 4. Recommended next skills (not yet built)

These gaps are visible from the seven-axis taxonomy and the construction guide:

1. **decoding-controller** — sets temperature, number of candidates, reasoning effort, and schema constraints explicitly, and logs them with every result.
2. **faithfulness-auditor** — runs the external check described in the manual's Chapter 15: re-derive a conclusion independently and compare it with the visible reasoning.
3. **agent-permission-review** (reshaped from "injection-hardening", October 20, 2026) reads an agent's tool definitions (MCP tool lists or function schemas), marks which tools add untrusted input, private data or outside communication (the three legs of the Rule of Two), flags tools without argument limits and sessions that can combine all three, and suggests checks in code that would contain a fooled model. It reads definitions and never calls the tools. Spotlighting and labelling are aids, not a defence: an adaptive attack beat spotlighting 99% of the time on three of four AgentDojo target models (Nasr et al.; Engineering Stack, Part 10, Section 11).
4. **long-context-placer** — rewrites a long prompt so that critical instructions appear at the beginning and again at the end.

Build each with the project's skill-building rules: trigger and non-trigger examples, at least three end-to-end tasks run with and without the skill, and a check that each test fails when the skill is broken on purpose. `skills/quantum-entanglement-lab/evals/` is a worked example of such an eval pack.

---

## 5. Consistency sweep

| Item | Before | Now |
|------|--------|-----|
| sophisticated-prompt-generator SKILL.md | Seven-axis, with "Planetary" topic and lens leftovers | Version 1.2.1, persona-free |
| practical-frameworks.md | Persona lines; "tested for basic usability", unsupported | Persona-free; labeled practitioner patterns |
| seven-axis-checklist.md | "Optimisation"; negative instructions preferred | Manual's axis names; positive instructions with reasons |
| Agent Skills reference | Version 1.1; quantum lab 1.0; harness score as evidence | Version 1.2; quantum lab 1.2.1; harness limits stated |
| quantum-entanglement-lab | Version 1.1; no eval pack; three checks that could not fail | Version 1.2.1; eval pack whose mutation check shows every test can fail; a first with-and-without test; packages for the Claude app and other hosts |
| trig-check and qubit-math | Not built | Version 1.0 each, with tests, mutation checks and eval packs |
| Taxonomy, Third Edition | Unchecked draft | Independently reviewed and corrected |
| Construction Guide, Second Edition | Unchecked draft | Independently reviewed and corrected |
| Task-Type Index | One reversed rule; axis placements that differed from the manual | Aligned with the guide and the manual |

*End of New Skills Appendix*
