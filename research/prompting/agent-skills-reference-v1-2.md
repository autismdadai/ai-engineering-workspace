# Agent Skills and Advanced Prompt Engineering

## A Practical Reference for Any AI System

**Version 1.2 — October 2026; corrected and updated 6–7 October 2026 (quantum lab 1.2.1, its eval pack and test results, and packaging).** This version corrects version 1.1. Every status line says what was checked in this project and what could not be checked, because some skills' files are not in the project. Nothing here uses personas.

**Contents**

1. Design principles
2. What an Agent Skill is
3. Anatomy of a portable skill
4. Catalog of project skills
5. The seven-axis taxonomy, in summary
6. Practical everyday frameworks
7. Generating a 50-prompt suite
8. How to build a skill
9. Testing, validation, and evidence
10. Tips by category
11. Quick reference cards

## 1. Design principles

An Agent Skill is a reusable, version-controlled package of procedural knowledge that an AI agent loads when a request calls for it. It is not a one-off prompt, a system prompt, or a tool definition. It is a folder that teaches the agent how to do one recurring job reliably.

- **Evals first.** Write the success criteria and realistic test cases before writing instructions.
- **Progressive disclosure.** Keep SKILL.md lean, and put long material in `references/`.
- **Hybrid design.** Use the model for judgment and routing, and scripts for exact calculation and for anything with side effects.
- **Evidence discipline.** Grade factual claims as SUPPORTED, PARTIALLY_SUPPORTED, CONTRADICTED, or UNVERIFIED.
- **One job per skill.** Focused skills outperform sprawling ones. In SkillsBench, focused skills with two or three modules did better than comprehensive documentation, and self-generated skills gave no average benefit (arXiv 2602.12670, version 1).
- **Host-aware packaging.** Use only the front-matter fields and installation methods your host supports.
- **A verification layer.** High-stakes output needs success checks or an audit step.
- **No persona.** State the standard of work as behavior. Personas did not improve accuracy across 162 personas and 2,410 MMLU questions (Zheng et al., Findings of EMNLP 2024).

## 2. What an Agent Skill is

A skill is a folder containing at least a `SKILL.md` file. The file begins with YAML front matter:

```
---
name: lowercase-hyphenated-name
description: >
  What the skill does, when to use it, and when not to use it.
---
```

The body holds the procedure. Optional folders in the agentskills.io specification are `scripts/`, `references/`, and `assets/`. This project also keeps an `evals/` folder for test cases; that is a project convention, not part of the specification.

When a compatible host sees that a request matches the description, it loads the skill and follows the procedure. The host reads only the name and description until then, so the description decides whether the skill is ever used.

## 3. Anatomy of a portable skill

| Component | Required? | Purpose | Project practice |
|---|---|---|---|
| `name` | Yes | Identifies the skill | 1–64 characters: lowercase letters, numbers, and single hyphens, not at the start or end; must match the folder name |
| `description` | Yes | Discovery and triggering | Third person; what it does, when to use it, and when not to. Up to 1,024 characters in the specification; up to 200 for skills uploaded to the Claude app |
| SKILL.md body | Yes | Step-by-step procedure | Under 500 lines; steps, decision rules, limits |
| `references/` | No | Detail loaded on demand | Long examples and background |
| `scripts/` | No | Exact or side-effecting work | Non-interactive; print structured output; document side effects |
| `evals/` | Project convention | Measurable quality | Trigger and non-trigger lists; at least 3 end-to-end tasks run with and without the skill; adversarial cases |

The agentskills.io reference validator is `skills-ref validate <path>`. Version 1.1 of this reference cited a project script, `validate_skill.sh`, which is not in this project. For a worked example of an `evals/` folder, see `skills/quantum-entanglement-lab/evals/`; to check a skill folder and package it for the Claude app and other hosts, use `skills/build_skill.py`.

## 4. Catalog of project skills

### 4.1 sophisticated-prompt-generator (1.2.1)

**What it does.** Turns one seed question or goal into a suite of prompts: by default 50 prompts in 10 fixed topics with 5 variants each. Every prompt is placed on the seven axes and ends with a success check. Topic 10 is reserved for debug, audit, faithfulness, and meta prompts.

**How.** The model specialises the seed into each topic using the seven-axis checklist, then audits the suite: every topic present, no near-duplicates, every prompt runnable with placeholders only for the user's data, and no persona lines.

**Status.** The corrected SKILL.md and its two reference files are in `skills/sophisticated-prompt-generator/`. The version 1.2 scripts (`expand_suite.py`, `validate_suite.py`, `eval_harness.py`, and the expander library) live in the Planetary Council package, not in this project. Running them here on October 2, 2026 found three limits:

- the expander only fills templates;
- the heuristic harness scored a nonsense suite 0.880, above a real suite at 0.857;
- the model-judge hook was a stub written for an outdated API.

### 4.2 skill-builder (1.0.1)

**What it does.** Turns a recurring workflow into a complete, portable skill package: clarification, baseline evals, design, scaffolding, writing, testing, delivery.

**Status.** The text below is from version 1.1 of this reference, with the trigger counts raised to this project's standard; that change makes it version 1.0.1. The skill's files are not in this project, so it was not validated here.

```
---
name: skill-builder
description: >
  Turns a recurring workflow into a complete, portable Agent Skill package.
  Use when the user asks to build, create, or design a new skill from a
  workflow description. Do not use for editing an existing skill, general
  prompt writing, or explaining the Agent Skills specification without
  building something.
license: MIT
metadata:
  version: "1.0.1"
---

# Skill Builder

## Purpose
Produce the smallest useful, fully tested, portable skill that closes a real gap.

## Procedure
1. Clarify only what is missing: the one recurring job, what is out of scope,
   10 requests that should trigger the skill and 10 that should not, the host
   and its constraints, and what success looks like.
2. Confirm a skill is the right mechanism (versus a tool, a standing
   instruction, or a subagent).
3. Write baseline tasks and evals before writing instructions.
4. Write a lean SKILL.md; move long material to references/.
5. Add scripts only where they add exactness or control side effects;
   document every side effect.
6. Run the evals with and without the skill. Break the skill on purpose and
   confirm each test fails.
7. Deliver: file tree, full contents, eval results, trigger results,
   side-effect notes, version.

## Success criteria
- Valid SKILL.md; name matches the folder.
- At least three realistic end-to-end tasks plus trigger and non-trigger sets.
- Every test shown to fail when the skill is broken.
- Side effects listed.
```

### 4.3 quantum-entanglement-lab (1.2.1)

**What it does.** Runs a deterministic Python laboratory that checks Bell states, local Pauli actions, partial measurement, a Bell-state decoder, the CHSH inequality at the Tsirelson bound (|S| = 2√2), and teleportation. It also provides short reference cards for explanations.

**What changed from 1.0.** Version 1.0 tested teleportation only on the |+⟩ state. Because X leaves |+⟩ unchanged, a broken correction step still passed. Version 1.1 teleports six states (|0⟩, |1⟩, |+⟩, |+i⟩, and two generic states) and checks that every hand-built gate is unitary. In this project, deleting the X corrections or removing the Hadamard's 1/√2 makes version 1.1 fail, as it should.

**What changed in 1.2.** A mutation check found three version 1.1 checks that could not fail. Partial measurement checked only the 50/50 odds, so the wrong Bell state or the wrong basis passed; it now also checks that each outcome leaves |00⟩ or |11⟩. CHSH needed only |S| > 2.8, so an angle 0.05 rad off passed; |S| must now equal 2√2. And `python -O` strips every assert, so a broken lab printed six PASS lines; version 1.2 refuses to run under -O.

**What changed in 1.2.1.** The teleportation card now says which bit selects X and which selects Z, a gap that a test run found on 7 October. The script is unchanged. The skill also carries two descriptions: 365 characters for Claude Code and other hosts, and 197 for the Claude app; `skills/build_skill.py` builds a package for each.

**Expected output** (requires `qutip`, `numpy`, `scipy`):

```
[PASS] S(φ+)=1.000000
[PASS] X/Z local flips
[PASS] partial Z
[PASS] Bell decoder
[PASS] CHSH |S|=2.828427
[PASS] teleportation all branches F=1
ALL TESTS PASSED — you have a working entanglement laboratory.
```

**Watch for these QuTiP 5 traps:**

- `qutip.qip` no longer exists;
- `fidelity()` returns |⟨a|b⟩|, not its square, and it can exceed 1 for an unnormalized ket (checked on QuTiP 5.3.1: |0⟩ against |+⟩ gives 0.7071, and 2|0⟩ against |0⟩ gives 2.0);
- `entropy_vn` uses the natural log unless you pass `base=2`;
- `ptrace(0)` keeps qubit 0.

The skill is in `skills/quantum-entanglement-lab/`: SKILL.md, the reference cards in `references/`, the script in `scripts/entanglement_lab.py`, and an eval pack in `evals/` (trigger and non-trigger requests, end-to-end and adversarial tasks, a mutation check, an answer grader, and the with-and-without results).

### 4.4 cross-model-accuracy-verifier (1.0)

**What it does.** Reduces fabrication by pushing each atomic claim through an explicit verification loop.

**Status.** The method is in this project as `claude/research-verification-toolkit.md`. The packaged skill's files are not in this project.

```
---
name: cross-model-accuracy-verifier
description: >
  Verifies factual claims in AI-generated text by extracting atomic claims,
  checking each against a primary source, grading support, and producing an
  accuracy report. Use when the user asks to fact-check, verify accuracy,
  measure hallucination, or compare model outputs. Do not use for creative
  writing, pure opinion, or irreversible actions.
---

# Cross-Model Accuracy Verifier

1. Collect the text(s) and the original question.
2. Extract atomic claims, one proposition each.
3. Classify each as FACT, INFERENCE, OPINION, or UNCLEAR. Only FACT and
   INFERENCE go forward.
4. For each claim: state the evidence needed, find a primary source, quote
   it, and grade the claim SUPPORTED, PARTIALLY_SUPPORTED, CONTRADICTED, or
   UNVERIFIED.
5. Accuracy ≈ (SUPPORTED + 0.5 × PARTIALLY_SUPPORTED) / (FACT + INFERENCE).
6. Output a Markdown table plus a list of contradicted and unverified claims.
```

### 4.5 server-log-triager (1.0.0)

**What it does.** Parses unformatted application logs, extracts errors, and redacts personal data into structured Markdown tables, using a deterministic cleaning script.

**Status.** The script is not in this project, so its redaction could not be tested here. Before relying on it, test it on logs that contain known personal data and confirm that none survives.

### 4.6 Multi-agent orchestration pattern

A hierarchical pattern for high-stakes analysis that needs several independent viewpoints:

1. An orchestrator classifies the work and activates the minimum number of specialists.
2. Specialists answer in a fixed structure with evidence grades.
3. A synthesis step resolves conflicts and keeps dissent visible.
4. An independent verifier, with its own context, can be called at any stage.
5. The output is a structured brief.

The persona-free version is `claude/multi-lens-review-method.md`, and the persona version lives in its own separate project. Default to one agent plus skills. Add agents only for parallel, separable work or for independent checking, and state the extra cost.

## 5. The seven-axis taxonomy, in summary

The authoritative reference is *The Taxonomy of Prompt Engineering*, Third Edition. The axes are dimensions that combine, not stages in a ladder.

| Axis | Question | Practical tips |
|---|---|---|
| 1. Contextual Conditioning | What content and rules enter the context? | Say what to do with empty, ambiguous, or out-of-scope input. State instructions positively and give the reason; add a "do not" line only for a specific known failure. |
| 2. Representation | In what form are the context and intermediate text written? | Use clear delimiters and schema-defined output when code will parse it. Chain-of-Draft needs few-shot drafts. |
| 3. Reasoning Topology | What shape does the intermediate computation take? | Choose the lightest structure that closes a measured gap. Visible reasoning is generated text, not a causal log. |
| 4. Decoding & Inference Compute | How are tokens chosen, and how much computation is spent? | State temperature, the number of candidates and how one is chosen, reasoning effort, and schema constraints. Temperature 0 is not deterministic in deployed systems. |
| 5. Orchestration & Grounding | How is the call connected to retrieval, tools, memory, and other calls? | List tools and hand-off conditions. Require citations for grounded claims. Prefer independent parallel review to a relay. |
| 6. Optimization | Who or what writes and tunes the prompt? | Automate only at scale, after building an evaluation set. |
| 7. Verification & Security | How is the output checked and defended? | Attach success checks. Mark untrusted text, give tools least privilege, and enforce permissions in code. |

## 6. Practical everyday frameworks

These are in `skills/sophisticated-prompt-generator/references/practical-frameworks.md`, adapted without persona lines. They are practitioner patterns, not tested techniques.

- Task–Result–Goal–Context–Constraints
- Input–Task–Style
- Zero-, one-, and few-shot variants
- Ask-Before-Answer
- Prompt improver (fill-in-the-blank)
- Perspectives (one or several)
- Constructive critique
- Comparison table
- Reverse prompting (style capture)
- Revision commands

Use them for quick work. Before an important prompt goes into production, upgrade it to the seven-axis structure with a success check.

## 7. Generating a 50-prompt suite

1. Give one clear seed.
2. Invoke sophisticated-prompt-generator.
3. Receive the suite across the 10 fixed topics; Topic 10 is always debug, audit, faithfulness, and meta.
4. Every prompt carries a success check.
5. Judge the suite by running a sample of prompts and confirming their checks can fail. A harness score is a structure check, not evidence of quality.

## 8. How to build a skill

1. Pin down the one recurring job and what success looks like.
2. Confirm a skill is the right mechanism.
3. Write baseline tasks and evals before any instructions.
4. Design the smallest solution that works.
5. Write a lean SKILL.md, and put the rest in references.
6. Add scripts only where they add exactness or control side effects.
7. Document every side effect.
8. Run the evals with and without the skill, and break it on purpose to prove each test can fail.
9. Deliver the package with its test evidence.

Don't ship instructions that have not closed a measured gap.

## 9. Testing, validation, and evidence

**Structural.** Validate the front matter with `skills-ref validate`.

**Functional.**

- **quantum-entanglement-lab 1.2.1:** all six tests pass, and `evals/mutation_check.py` shows each one can fail: 16 of 16 runs behaved as expected on 6 and 7 October 2026 (QuTiP 5.3.1), against 12 of 16 for version 1.1. The answer grader's self-test passed all 7 tasks. In a quick with-and-without test (7 October; one run per task per condition, Sonnet 5.5 helpers), answers met their rubric in 7 of 7 tasks with the skill and 6 of 7 without; the one difference was running the lab itself. The trigger tests have not been run.
- **sophisticated-prompt-generator:** its scripts live in the Planetary Council package. Run in this project, the version 1.2 harness rewarded keywords over substance.
- **Other skills:** their files are not in this project.

**A test only counts if a wrong answer would fail it.** Break the skill or script on purpose and confirm that the test catches it.

**Security.** Read every outside skill and script before installing it. In Snyk's February 2026 scan of 3,984 public skills, 36.82% had at least one security flaw, 13.4% had a critical issue, and 76 were confirmed malicious.

**Evidence labels for factual claims:** SUPPORTED | PARTIALLY_SUPPORTED | CONTRADICTED | UNVERIFIED.

## 10. Tips by category

**Triggering.** Write the description as if it were the only thing the host will read. Include positive triggers and clear non-goals.

**Unusual input.** Always say what to do when input is empty, ambiguous, or out of scope. An explicit fallback, such as returning `SEED_TOO_VAGUE`, beats silent failure.

**Success checks.** End every non-trivial prompt with an objective test that a wrong output would fail.

**Faithfulness.** Never treat a chain of thought as an audit trail. When stakes are high, verify the conclusion independently.

**Scripts.** Keep them non-interactive, print clear PASS or FAIL lines, and document required packages and side effects.

**Multi-agent work.** Prefer an explicit orchestrator, the minimum number of specialists, and a synthesis step over free-form discussion.

**Versioning.** Increment the version when behavior changes, and keep old versions for comparison.

## 11. Quick reference cards

**Minimal skill skeleton**

```
---
name: my-skill
description: >
  What it does, when to use it, and when not to use it.
---
# Title
## Purpose
## Procedure
1. ...
## Success criteria
```

**Minimal high-quality prompt**

```
[Task, stated as a verb]
[Standard of work and constraints]
[Output format or schema]
[What to do with empty, ambiguous, or out-of-scope input]
Success check: [an objective test the output can fail]
```

**Evidence grades**

- **SUPPORTED:** a primary source directly confirms the claim.
- **PARTIALLY_SUPPORTED:** a source supports part of it.
- **CONTRADICTED:** a primary source conflicts with it.
- **UNVERIFIED:** no adequate primary source was found.

*End of reference.*
