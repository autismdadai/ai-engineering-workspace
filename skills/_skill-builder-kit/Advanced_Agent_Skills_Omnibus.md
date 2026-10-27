# Advanced Agent Skills: The Master Omnibus Guide
**Date: September 27, 2026 | Comprehensive Master Build**

This document consolidates findings from five deep-research reports on AI Agent Skills (including Snyk ToxicSkills audits, Anthropic guidelines, OpenAI Codex integrations, and agentskills.io specifications), deduplicates conflicting data, and provides advanced integrations tailored for highly automated workflows.

## Table of Contents
1. Definitions and System Boundaries
2. Platform Support Matrix
3. Step-by-Step Build Framework
4. Security and Threat Vector Analysis
5. The Universal Master Prompt
6. Advanced Automations: Integrating Agent Skills with Relevance AI, Zapier, and 3D WebGL

---

## 1. Definitions and System Boundaries
An **Agent Skill** is an open-standard, file-system-based packaging layer structured as a portable local folder containing at minimum a `SKILL.md` root file. 
*   **Skill vs. System Prompt:** System prompts are fixed global context structures. Skills utilize progressive disclosure, populating context on active intent match to eliminate idle token costs.
*   **Skill vs. Tool / MCP Server:** Model Context Protocol (MCP) servers expose low-level atomic access pipelines. Agent Skills supply the cognitive behavioral orchestration framework detailing exactly when and how to deploy those integrations.
*   **Skill vs. Custom Assistants (GPTs/Gems):** Assistants operate as monolithic vendor ecosystem runtime wrappers. Agent Skills are local, completely portable file structures.

## 2. Platform Support Matrix
*   **Agent Skills Spec:** A folder with `SKILL.md`. Metadata (~100 tokens) loads at startup, body on activation. Limits: name 64 chars, description <1,024, body <500 lines.
*   **Claude API:** Upload to `/v1/skills` referenced in `container.skills`. Limit 20 skills/request. 30 MB uncompressed limit. No network/runtime installs.
*   **Claude Code:** `~/.claude/skills`. Listing uses 1% of context. Full network access.
*   **OpenAI Codex:** `.agents/skills`. Initial list <2% context window (or 8,000 chars).
*   **OpenAI API:** Upload to `/v1/skills`. 50 MB zip max. 500 files per version.
*   **Cursor:** `.agents/skills` or `.cursor/skills`. Agent decides execution.

## 3. Step-by-Step Build Framework
1. **Spot the Need:** Identify high-frequency operations causing repetitive prompt injection overhead.
2. **Run Baseline:** Test operations against the raw baseline model to map edge-case failure loops.
3. **Coherent Scoping:** Bound the package to a singular clear activity.
4. **Domain Extraction:** Compile error traces and specific schemas.
5. **Freedom Calibration:** Choose prose for creative loops and scripts for precision parameters.
6. **Header Authoring:** Write standard-compliant YAML frontmatter spanning line 1 without XML tokens.
7. **Body Scripting:** Build the instruction markdown body below 500 lines.
8. **Reference Partitioning:** Offload heavy background text into `references/`.
9. **Non-Interactive Automation:** Program script components within `scripts/` reading parameters strictly via CLI.
10. **Invocation Controls:** Lock sensitive operations behind `disable-model-invocation: true`.
11. **Syntax Linting:** Validate directory structures locally running `skills-ref validate`.
12. **Trigger Evals:** Verify similarity loops against 20 queries split 60/40.
13. **Quality Assertion:** Execute double-blind test matrices comparing with-skill behavior against baseline logs.

## 4. Security and Threat Vector Analysis
According to independent Snyk analysis, 36.8% of available community registry assets contain architectural flaws.
*   **Indirect Prompt Injection (IPI):** Adversarial text strings hidden inside loaded references read by the model.
*   **Persistent Context Poisoning:** Compromised instructions trick an agent into injecting malicious lines directly into localized files (`MEMORY.md`).
*   **Conditional Backdoors:** Encrypted payloads stay entirely hidden during static source code analysis, triggering only on specific prompt strings.
*   **Mitigation:** `allowed-tools` is an experimental pre-approval grant. It is not a universal security boundary. Audit all scripts before running. 

## 5. The Universal Master Prompt
*Copy this block into any capable AI model to generate new Agent Skills:*

> **ROLE:** You are a Skill engineer. Your job is to turn my recurring workflow into a functional Agent Skill package.
> **EVIDENCE RULES:** Do not invent frontmatter fields, host limits, commands, paths, APIs. Separate facts from design choices using [SOURCE], [INFERENCE], [UNVERIFIED], [PROPOSED].
> **PHASE 0 (CLARIFY):** Ask only necessary questions: What is the recurring job? What is out of scope? 3-5 real requests that trigger it. Host/models. Network constraints.
> **PHASE 1 (MECHANISM):** Verify a Skill is the right mechanism vs a Tool, Prompt, or Subagent.
> **PHASE 2 (BASELINE & EVALS):** Create 3 realistic tasks. Run without the skill. Record the gap. Create 20 trigger queries (60/40 train/val).
> **PHASE 3 (DESIGN):** Scope to one job. Choose prose, templates, or scripts.
> **PHASE 4 (PORTABLE SKILL):** Create folder tree (`SKILL.md`, `scripts/`, `references/`). Frontmatter requires `name` (lowercase-hyphenated) and `description`.
> **PHASE 5-8 (BODY & SAFETY):** Keep under 500 lines. Explicit steps. Relative paths. Scripts must be non-interactive, accept CLI inputs, and exit cleanly. Document all file access, tool use, and side effects.
> **PHASE 9-12 (PACKAGE & DELIVER):** Run validation. Return the file tree, full file contents in code blocks, host-specific installation steps, test results, and security audit.

## 6. Advanced Automations: Integrating Agent Skills with Relevance AI, Zapier, and 3D WebGL
To elevate Agent Skills beyond simple log parsing or text verification, developers can orchestrate advanced web automations and API handoffs.

### 6.1. Handoff to Relevance AI & Zapier (Lead Extraction Agents)
When building a client lead processing AI agent (e.g., extracting landscaping leads, urgency categorization), your Agent Skill should act as the **cognitive router**, not the execution engine.
*   **Architecture:** The Agent Skill's `SKILL.md` identifies the parsed lead data (Name, Service, Urgency). It then invokes a dedicated deterministic script in `scripts/webhook_push.py`.
*   **Execution:** The python script formats the payload into JSON and posts to a Zapier Webhook URL.
*   **Relevance AI Orchestration:** The Webhook triggers a Relevance AI Subagent which reaches out to the client. The Agent Skill prevents LLM hallucination by forcing the data into a rigid JSON schema *before* network transmission.

### 6.2. Generating 3D Interactive Graphics (Three.js WebGL) via Skills
For advanced frontend outputs, an Agent Skill can scaffold standalone WebGL/Three.js environments (e.g., interactive planetary terraforming or technology trees).
*   **The Skill Structure:** Create a `threejs-scaffolder` skill.
*   **Assets:** Place boilerplate `index.html` and `vite.config.js` files into `assets/`.
*   **Cognitive Loop:** The LLM's role is exclusively to generate the mathematics for the 3D scene (camera positioning, mesh geometry, shaders). It calls `scripts/build_scene.py` to inject the generated JavaScript logic into the boilerplate asset.
*   **Result:** A fully functional, locally hosted WebGL application, bypassing the standard chat interface entirely.
