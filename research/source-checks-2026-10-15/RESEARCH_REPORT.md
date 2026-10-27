# The Seven-Axis Taxonomy and the Skill-Builder Kit, Checked Against Their Sources

**Date:** October 15, 2026 · **Covers:** *The Taxonomy of Prompt Engineering*, Third Edition (September 2026), and the agent-skill-building kit (Universal Master Prompt v2.0, Advanced Agent Skills Omnibus, Agent Skills Reference v1.2, `validate_skill.sh`, `skill_audit.py`, and your four skills).

## 1. Bottom line

- **Your manual's sources are real and correctly identified.** All 124 arXiv IDs and all 8 DOIs point to the papers named, with the right first authors. Of the 14 figures the manual itself listed as "carried over, never re-read," 8 checked out exactly. Two quotations need one-word fixes, and four need their scope added.
- **One sentence has no source behind it.** Section 16.2 says Vectara found DeepSeek-R1 produced 71.7% "benign hallucinations" against V3's 36.8%, attributed to "overhelping." The Vectara post the manual cites says none of this. Find the real source or delete the sentence.
- **The field moved since your edition.** 28 new primary sources from July 2025 to October 2026 matter for how you prompt. The independent re-check confirmed 23 outright and the main results of 4 more. It partly refuted 1 on a side remark, and that one is left out of this report. The biggest shifts:
  - expert personas still don't raise accuracy on 2025 models;
  - forcing JSON output can cost reasoning accuracy;
  - more "thinking" can make answers worse on tasks with distractors;
  - multi-agent setups help only for independent subtasks;
  - automatic prompt optimizers give small, noisy gains;
  - hand-written skills help, while AI-written skills hurt.
- **Your skill-builder kit is mostly right about the spec and the hosts.** 13 of 17 host and spec claims are fully supported, and the other 4 need small corrections. Your two validators have real bugs: one passes skills it never actually read, and the other fails valid skills. Your own example skill also fails both.
- **Your three skills are too long for claude.ai.** Their descriptions are 610, 411 and 253 characters, and claude.ai uploads allow at most 200.

## 2. How this was checked

Your Edition Protocol v3 shaped the method:

- **Primary sources only.** Checkers read the papers, official docs or standards bodies, never the manual's own text or another AI's summary.
- **Lookup caps.** Each checker had a capped number of web lookups, and saved its report as it went.
- **Independent re-checks.** Every correction and every new source was re-checked by a different model in a separate session.
  - Bibliography: a script compared every identifier with the arXiv API and Crossref.
  - Research: Sonnet-class checkers (9 of them).
  - Re-checks: Haiku-class.
  - Disputed items: settled by Opus-class, against the source.

**Not covered:**
- figures the October 2026 verification already confirmed (all of Appendix A plus the 46-item citation audit);
- the Prompt Construction Guide;
- most of Chapters 18–23.

**Fetch limits.** Web pages were read through a tool that summarizes, and checkers asked it for verbatim quotes. A few items are marked "re-check not reached" where the re-checker's lookup cap ran out.

**Where everything is.** The detailed reports, with quotes and URLs, are in this folder (see the file list in Section 8).

## 3. Your manual: what holds and what to fix

### 3.1 Bibliography (full table: `bibliography-audit.md`)

| Check | Result |
|---|---|
| 124 arXiv IDs | All resolve to the named paper, with the right first author |
| 8 DOIs | All resolve; pages and volumes match where given |
| Web-only entries and stated venues (27 items) | 20 confirmed; 2 corrected (entries 91 and 128); 5 open: entries 74, 81 and 136 can't be read automatically (OpenAI and OWASP block it), and the venues of entries 111 and 112 weren't reached. Entries 21, 108, 117 and 118 (mnemonics, classic psychology works, vendor doc sets) were not checked |

### 3.2 Corrections (each confirmed by an independent re-check unless marked)

| Where | Manual says | Source says | Fix |
|---|---|---|---|
| §16.2, line 2260 | R1 produced 71.7% "benign hallucinations" vs V3's 36.8%, attributed to "overhelping" | The cited Vectara post (30 Jan 2025) has no "benign," no "overhelping," and neither number. It reports mean HHEM scores of 0.82 vs 0.92 | Find the source or delete. The 14.3% vs 3.9% figures are correct. *(re-check not run; the post was read in full)* |
| §8.4, line 776 | LLMLingua: "up to 20x compression with **minimal** performance loss" (in quotation marks) | "up to 20x compression with **little** performance loss" (arXiv 2310.05736; ACL Anthology 2023.emnlp-main.825) | Fix the quoted word |
| Ch. 4, line 98 | NoLiMa "**removed** literal word overlap" | "questions and needles have **minimal** lexical overlap" (arXiv 2502.05167) | "minimized" |
| Entry 128 | *…Cumulative Changes and Attractors in Iterated Cultural Transmissions*, ICLR 2025 | The ICLR 2025 version is titled *When LLMs Play the Telephone Game: Cultural Attractors as Conceptual Tools to Evaluate LLMs in Multi-turn Settings* | Use the ICLR title |
| Entry 91 | Leaderboard "as updated May 2026" | The README says HHEM-2.3, last updated 22 September 2026; R1 11.3%, V3 6.1% (figures still match) | Give the access date |
| Entry 73 | Page numbers removed as unverified (changelog 27.1 #15) | Crossref: pp. 1009–1022 | Restore them |
| Entry 105 | DeepSeek-R1, arXiv only | Published in *Nature* 645:633–638 (2025) | Add the journal |
| §10.1 | Keep temperature low where one answer is correct; the sketch uses temperature 0 | Google's Gemini 3 guide (updated 9 Oct 2026): keep temperature at the default 1.0, since lower "may lead to … looping or degraded performance." The Gemini 3.8 page says to remove sampling parameters and use `thinking_level` | Add a provider caveat: check the current docs for your exact model |
| §10.5 | The format-vs-reasoning debate is "unsettled" | Lee, D'Antoni & Berg-Kirkpatrick, *The Format Tax* (arXiv 2604.03616, Apr 2026): format instructions cost open-weight models accuracy, averaging −3.9 points over 72 cells; recent closed models lose little | Replace "unsettled" with this scoped finding |

### 3.3 Right numbers that are missing their scope

| Where | Add |
|---|---|
| §8.4 LLMLingua 20x | Best case, GSM8K, about 1.5 exact-match points lost (78.85 → 77.33) |
| §9.5 PoT "around 12%" | Mainly Codex; about 12% is the zero-shot average on the math datasets; the few-shot averages are about 8% (math) and 15% (financial QA) |
| §11.3 Reflexion 91% (GPT-4, HumanEval) | It used unit tests the model wrote itself, not hidden tests; in the same paper Reflexion did worse than GPT-4 on MBPP Python. Reword "needs a ground-truth signal" to "needs an executable check (such as tests the agent writes) or an external signal" |
| Ch. 28 #5 DSPy "over 25% and 65%" | The paper never says whether these are relative gains or percentage points; GPT-3.5 and llama2-13b-chat, GSM8K and HotPotQA, 2023 |

Confirmed exactly as written: LongLLMLingua, LLMLingua-2, PAL, Cobbe et al.'s verifier result, RULER (17 models, 13 tasks, half fail at 32K), NoLiMa (11 of 13 below 50% at 32K; GPT-4o 99.3% → 69.7%), and the wording of the DSPy quote.

### 3.4 Needs a person with a normal browser (five minutes)

- Entry 74: the date of OpenAI's *Structured Outputs* post.
- Entries 81 and 136: the OWASP pages (LLM01/LLM07:2025; Top 10 for Agentic Applications, December 2025).
- Entry 111: RULER at COLM 2024.
- Entry 112: NoLiMa in PMLR 267.

## 4. What's new on each axis (July 2025 – October 2026)

Evidence class follows each source. "Confirmed" means the independent re-check read the same numbers in the source.

### Axis 1: Contextual Conditioning

| Finding | Source | Status | What to do |
|---|---|---|---|
| Expert personas gave no reliable accuracy gain on GPQA Diamond across six 2025 models; on MMLU-Pro, five of six models showed no significant gain. Low-knowledge personas often lowered scores | Basil, Mollick, Meincke et al., *Prompting Science Report 4* (arXiv 2512.05858, Dec 2025), preprint | Core results confirmed; one per-model figure not re-read | Keep your "no persona" rule; now backed on 2025 closed models too |
| Length alone hurts. With perfect retrieval, performance still fell 13.9%–85% as input grew, even when the extra tokens were masked | Du et al., arXiv 2510.05381 (Oct 2025), Findings | Confirmed | Put the document first and the question last, and ask the model to quote the passages that answer before it answers |
| Pasting the question twice won 47 of 70 benchmark-model pairs with 0 losses on non-reasoning models; neutral with reasoning on | Leviathan, Kalman & Matias (Google), arXiv 2512.14982 (Dec 2025), preprint | Confirmed | A free test on fast models; little benefit once thinking is on |
| Current Claude models follow the system prompt more closely, so "dial back aggressive language" (CRITICAL/MUST); newer models read prompts literally; prefill is unsupported from Claude 4.6 | Anthropic, *Prompting best practices* and model guides (read 15 Oct 2026), vendor docs | Confirmed | State each rule once, calmly; say "everywhere" if you mean it |

### Axis 2: Representation

| Finding | Source | Status | What to do |
|---|---|---|---|
| The "format tax": asking for JSON, XML or LaTeX lowers reasoning accuracy on open-weight models, and most of the loss comes from the format instruction itself, not the decoder; reasoning freely and converting afterwards recovers most of it | Lee, D'Antoni & Berg-Kirkpatrick, arXiv 2604.03616 (Apr 2026), preprint | Confirmed | Reason in plain text first, convert to JSON second |
| Anthropic: with structured outputs the model can work things out only in its thinking; skipping thinking costs accuracy | Anthropic, *Prompting Claude Sonnet 5.5* (read 15 Oct 2026), vendor docs | Confirmed | Keep thinking on when you need JSON from a hard task |
| In long agent sessions, hiding old tool outputs halved cost and matched LLM summarization | Lindenbauer et al., *The Complexity Trap* (arXiv 2508.21433; NeurIPS 2025 DL4C workshop) | Confirmed | Trim old tool output before paying for a summarizer |

### Axis 3: Reasoning Topology

| Finding | Source | Status | What to do |
|---|---|---|---|
| More thinking can lower accuracy. On counting with distractors, spurious-feature regression and constraint tracking, longer reasoning made models worse: Claude models get distracted, o-series models overfit to the framing | Gema et al., *Inverse Scaling in Test-Time Compute* (arXiv 2507.14417; TMLR, Dec 2025), peer-reviewed | Confirmed | Test a lower effort level too, and strip irrelevant detail |
| Decomposition doesn't fix knowledge gaps on frontier models (Bamboogle: GPT-5.1 +3.2 points vs Llama-3.3-70B +26.8), but it helps models say "I don't know" | Madhwal et al., arXiv 2602.04853 (2026; Findings of ACL 2026 per listing) | Confirmed | Ask direct and decomposed versions; treat disagreement as a warning |
| Code interpreters raise final-answer accuracy (up to +19.3 points on PYMATH) but can introduce reasoning errors | Bayat et al., arXiv 2511.10899 (Nov 2025), preprint | Confirmed | Read the working, not just the number |
| CoT faithfulness across 12 open-weight reasoning models: hint acknowledgement ranged from 39.7% to 89.9% | Young, arXiv 2603.22582 (Mar 2026), preprint, single author | Confirmed | Visible reasoning is evidence, not proof |

### Axis 4: Decoding & Inference Compute

| Finding | Source | Status | What to do |
|---|---|---|---|
| Gemini 3: keep temperature at 1.0; Gemini 3.8: remove sampling parameters and use `thinking_level` | Google Gemini API docs (updated 9 and 13 Oct 2026), vendor docs | Confirmed | Check the docs for your exact model before touching temperature |
| Anthropic now steers thinking with effort levels (max, xhigh, high, medium, low), set at `output_config.effort`. You don't set a token budget. Defaults differ by model, and changing effort breaks the prompt cache | Anthropic, *Steering thinking* (read 15 Oct 2026), vendor docs | Confirmed | Pick an effort level per conversation and keep it; don't rely on "think less" wording |
| DeepConf: confidence-filtered voting reached 97.9% on AIME 2025 with 84.7% fewer tokens (GPT-OSS-120B) | Fu et al., arXiv 2508.15260 (Aug 2025), preprint | Core idea confirmed; numbers not re-read | For hosted models, stop adding samples once the vote settles |

### Axis 5: Orchestration & Grounding

| Finding | Source | Status | What to do |
|---|---|---|---|
| Multi-agent helps only some tasks: centralized coordination gave +80.8% on Finance-Agent, but every multi-agent variant was worse on PlanCraft (−39% to −70%); tasks where one agent already scores above 45% see negative returns (260 configurations) | Kim et al., arXiv 2512.08296 (v3 Apr 2026), preprint | Confirmed | Start with one agent; add agents only for independent subtasks, with a checker |
| AGENTS.md-style context files: LLM-generated ones lowered resolution (−0.5% SWE-bench, −2% CTXbench); developer-written ones helped slightly (+2.4%) | Gloaguen et al., arXiv 2602.11988 (v3 Sep 2026), preprint | Confirmed | Write instruction files by hand and keep them short; don't keep auto-generated ones |
| Curated skills raised pass rate from 33.9% to 50.5%. Self-generated skills fell below no skills (−8.1 to −11.5 points). 2–3 skills gave +19.0 points vs +10.1 for four or more | Li et al., *SkillsBench* (arXiv 2602.12670, v4 Jun 2026), preprint | Confirmed | See Section 5 |
| Tool Search raised Opus 4 MCP accuracy from 49% to 74%; code execution with MCP cut one workflow from 150,000 to 2,000 tokens | Anthropic Engineering (Nov 2025), vendor-reported | Confirmed | Don't load every tool into every session |

### Axis 6: Optimization

| Finding | Source | Status | What to do |
|---|---|---|---|
| ACE (an evolving "playbook" built from small itemized edits) beat ReAct+GEPA by 11.9% on AppWorld | Zhang et al., arXiv 2510.04618 (ICLR 2026 per arXiv) | Confirmed | Keep a running playbook; edit single items from hard feedback; never let the model rewrite the whole thing |
| Optimizing skill files with GEPA gave +4.9 points, not statistically significant (best p = 0.29) | Kozyrev et al., arXiv 2609.12742 (Sep 2026), preprint, small scale | Confirmed | Treat optimizer gains as noise until repeated on unseen tasks |
| GEPA variants scored at or below the unoptimized prompt on AIME 25 with Qwen3-4B (46.35–46.87 vs 47.03) | Gao et al., *p1* (arXiv 2604.08801), preprint, one small model | Confirmed | Always compare against the unoptimized prompt |
| PrefPO, MIPROv2 and GEPA tie on BIG-Bench Hard (0.875 / 0.873 / 0.870); TextGrad's prompts grew up to 14.7× | Singhal et al., arXiv 2603.19311 (Mar 2026), method authors' own comparison | Confirmed | Read the winning prompt for bloat and gaming |

### Axis 7: Verification & Security

| Finding | Source | Status | What to do |
|---|---|---|---|
| A self-correction blind spot: models fix an error presented as the user's but miss the same error presented as their own (64.5% average across 14 non-reasoning models). Appending "Wait" cut the blind spot by 89.3% | Tsui, arXiv 2507.02778 (v2 Oct 2025), preprint | Main numbers confirmed | Don't ask for a re-check in the same chat; present the draft as someone else's, or use a fresh chat |
| LLM judges: exact-match agreement overstates chance-corrected agreement by 33.8–41.3 points; rankings shift by up to 14 places (21 judges, about 541,000 judgments) | Norman, Rivera & Hughes, arXiv 2606.19544 (Jun 2026), preprint | Confirmed | Swap answer order and call a flip a tie; check the judge against a few human-labeled cases |
| Monitors that read the chain of thought catch target behaviors better than action-only monitors | Guan et al., *Monitoring Monitorability* (arXiv 2512.18311, Dec 2025), preprint | Confirmed | For long agent runs, review the reasoning log together with the actions |
| Agents Rule of Two: until prompt injection can be reliably stopped, give an agent at most two of (untrusted input, private data, ability to act or send) | Meta AI (31 Oct 2025), vendor guidance | Confirmed | Count the three before connecting an agent to your accounts |

### 4.1 Suggested manual changes from the new research

1. **§7.3:** add Prompting Science Report 4 as a 2025 replication of the persona result.
2. **§7.4:** add Du et al. (length alone hurts), the quote-first fix, and prompt repetition (scoped to non-reasoning models).
3. **§7.5:** add vendor guidance on emphasis, literal reading and prefill.
4. **§8.4:** add agent-trajectory compression (observation masking).
5. **§9.2 and §9.5:** add the frontier-model caveats for decomposition and code tools.
6. **§10.1:** add the provider caveat on temperature. **§10.4:** add inverse scaling and the per-model effort defaults. **§10.5:** add the format tax and the two-step pattern.
7. **§11.5:** add the scoped "when multi-agent helps" rule. **§11.7:** add SkillsBench v4 and the AGENTS.md study.
8. **§12.5:** add the replication cautions (Kozyrev, p1, PrefPO) beside GEPA's figures, and ACE as context-level optimization.
9. **§13.2:** add the self-correction blind spot. **§13.3:** add chance-corrected judge agreement. **§15.3:** add Guan et al. **§17.3:** add the Rule of Two.

## 5. Agent skill builders

### 5.1 Spec and host facts (`skills-hosts.md`)

Correct as written: the folder plus `SKILL.md` format; about 100 tokens of metadata at startup; the name rules; description ≤ 1,024 (spec) and ≤ 200 for claude.ai uploads; the 500-line guideline; Claude API limits (`/v1/skills`, 20 skills per request, 30 MB, no network or runtime installs); Claude Code's `~/.claude/skills` with a listing budget of 1% of context; OpenAI API limits (50 MB zip, 500 files); Cursor paths; `allowed-tools` as experimental; `skills-ref validate`.

Corrections:

1. **Frontmatter fields.** The spec has six: `name` and `description` (required), plus `license`, `compatibility` (≤ 500 characters), `metadata` (a string map) and `allowed-tools` (experimental). Your Reference table lists only four of them.
2. **"No XML tags" and "no 'anthropic'/'claude' in the name"** are Anthropic-host rules, not spec rules. Your validators check neither.
3. **Codex:** the skill list uses at most 2% of context. The 8,000-character figure applies only when the window size is unknown.
4. **`disable-model-invocation`** works in Claude Code and Cursor only. In Codex, use `allow_implicit_invocation: false` in `agents/openai.yaml`.
5. **`skills-ref`** describes itself as "for demonstration purposes only," so don't treat it as a production gate.
6. **Missing details:**
   - The OpenAI API also has a 25 MB limit per uncompressed file.
   - Claude Code caps each listing entry at 1,536 characters.
   - Cursor also reads `.claude/skills` and `.codex/skills`.

### 5.2 Your validators (tested on this PC, then compared with the official validators)

| Skill | `validate_skill.sh` | `skill_audit.py` | Truth |
|---|---|---|---|
| sophisticated-prompt-generator | PASS, description length **1** | FAIL: "name is missing" | Valid (folded `>` description, 610 characters) |
| cross-model-accuracy-verifier | PASS, description length **1** | FAIL: "name is missing" | Valid (411 characters) |
| server-log-triager | PASS | PASS | Valid (253 characters) |
| example-skill (from your bundle) | FAIL | FAIL | Actually invalid: the folder name ≠ the `name` field, and the description's second line is unindented, which breaks YAML 1.2 §8.2.3 |

**Why:**
- `validate_skill.sh` reads only the first line after `description:`, so a folded `>` description becomes the single character ">" and is never checked.
- `skill_audit.py` rejects valid indented continuation lines and then throws away the fields it had already read, which produces the false "name is missing."

**Fixes:**
1. Parse the frontmatter as real YAML. Anthropic's `quick_validate.py` uses PyYAML `safe_load`, and `skills-ref` uses strictyaml.
2. Reject unknown top-level keys.
3. Check `compatibility` ≤ 500 characters and that `metadata` is a map.
4. Reject `<` or `>` in the name and description.
5. Reject reserved words in the name.
6. Warn when a description is over 200 characters (the claude.ai limit).
7. Add host "profiles" (spec, claude.ai, Claude Code, API).
8. Ship a set of test cases with expected verdicts.
9. Fix the example skill so it passes its own validator.

Full list: `skills-method.md`.

### 5.3 Your build method compared with official guidance

**Aligned:**
- baseline first;
- evals before instructions;
- one default approach rather than a menu;
- a lean SKILL.md with references one level deep;
- your script rules;
- checking each host's own docs.

**Missing or different:**
- **Trigger testing.** Anthropic's skill-creator uses about 20 queries (8–10 should trigger, 8–10 near-misses that shouldn't), a 60/40 train/held-out split, 3 runs per query, a 0.5 trigger threshold and up to 5 iterations. Your three documents disagree with each other (3–5, 10+10, and 20 at 60/40). Pick one.
- **Test on every model you'll use.** Anthropic's checklist names Haiku, Sonnet and Opus. A 2026 study saw the same skill trigger anywhere from 0 of 40 to 40 of 40 times depending on the model (arXiv 2609.29454).
- **Freedom levels.** Anthropic gives three (text instructions; pseudocode or scripts with parameters; fixed scripts). Your kit has two.
- **"Double-blind test matrices"** is not official wording. The official version is: run with-skill and baseline together, an optional blind comparison by an independent judge, mean ± standard deviation over repeated runs, and human review.
- **Break-on-purpose testing** is your own addition, and a good one. Keep it.
- **Author/tester loop.** Anthropic recommends a Claude A (author) and Claude B (tester) loop, and says no special system prompt is needed to teach Claude the format. The master prompt's value is its gates (baselines, evidence labels), not format teaching.

### 5.4 Research on skills since mid-2025 (`skills-research.md`)

| Finding | Source | What to do |
|---|---|---|
| AI-written skills hurt (−8.1 to −11.5 points across three agent setups), while curated skills help (+16.6) | SkillsBench v4 (arXiv 2602.12670) | Draft with AI if you like, but edit by hand and measure against a run without the skill |
| Skills can cause failures: 307 cases (125 functional, 182 efficiency); relevant-looking skills misled the agent, and mandatory checklists added cost | Dong et al., arXiv 2608.11888 (Aug 2026) | Compare pass rate and cost with and without the skill; cut steps the task doesn't need |
| Trigger rates differ wildly by model (0/40 to 40/40) | Gao et al., arXiv 2609.29454 (Sep 2026) | Measure triggering from the session trace, per model |
| Malicious skills can win selection through their description wording (86% pairwise win rate) | Saha et al., arXiv 2605.11418 (May 2026) | Read a third-party skill in full before installing it |
| Skills generated from your own sessions can carry planted backdoors (a detector's catch rate fell from 98.5% to 11.4%) | Ying et al., *SkillJack* (arXiv 2608.03509) | Record where each generated skill came from, and re-read it |
| Over 99% of real SKILL.md files deviate from published best practices somewhere ("skill smells") | Hong et al., arXiv 2607.01456 | Run a style check on every skill |
| A security architecture: one-time approval at install is a structural weakness | Li et al., arXiv 2604.02837 | Re-review a skill on every update |

**Fix the Snyk wording.** The figure is 36.82% of 3,984 skills from ClawHub and skills.sh with *at least one security flaw of any severity*, not "architectural flaws." Also: 13.4% had a critical issue, and 76 were confirmed malicious (the headline's 1,467 is the any-flaw count). "Encrypted payloads that trigger on specific prompt strings" is not in the sources. They describe obfuscation, remote content fetched after review, payloads hidden in extra files, and staged memory attacks. The MEMORY.md example comes from Snyk's discussion of OpenClaw.

### 5.5 Getting your skills into your Claude apps

- **claude.ai and Claude Desktop:** Customize → Skills → upload a ZIP whose top folder matches the skill name; "Code execution and file creation" must be on. Descriptions must be **≤ 200 characters**, so each of your three skills needs a shorter description first.
- **Plugins (the recommended way to bundle and share):** one plugin (`.claude-plugin/plugin.json` plus `skills/<name>/SKILL.md`) installs once and works in chat, Cowork and Claude Code.
- **Claude Code:** `~/.claude/skills/<name>/SKILL.md`. Skills you upload to claude.ai sync down to `~/.claude/skills/synced/` when you sign in with a claude.ai account. Don't edit the synced copy.
- **Conflicting Anthropic docs:** the API overview says skills don't sync between surfaces, but the Help Center and Claude Code docs describe syncing and sharing. Trust the newer Help Center and Claude Code pages.

## 6. A practical playbook

These are the rules this research supports for everyday use: health questions, school and IEP documents, money, legal letters, and work. Each names its evidence.

1. **Describe the job, not a character.** Write "Check this letter for errors a school administrator would object to," not "You are an expert." Personas don't add accuracy (Zheng 2024; Prompting Science Report 4, 2025).
2. **Long documents: document first, question last, then "quote the parts that answer this before you answer."** Length alone costs accuracy (Du et al. 2025; Anthropic docs).
3. **Never accept "I double-checked" from the same chat.** Paste the answer into a new chat as "someone's draft" and ask what is wrong with it (Tsui 2025; Huang et al. 2024).
4. **For anything that matters, ask two ways and compare.** Ask directly, then step by step; ask two different models. Disagreement is your signal to check the source (Madhwal et al. 2026; your manual §13.6).
5. **Use thinking or effort settings deliberately.** More isn't always better on messy inputs, so try a lower setting too, and remove irrelevant detail first (Gema et al. 2025).
6. **When you need a table or JSON, let it think first and format second** (Lee et al. 2026; Anthropic docs).
7. **Check the model's current docs before copying settings from old guides.** Temperature advice now differs between providers (Google, Oct 2026).
8. **One assistant first.** Add more agents only for separate, independent pieces of work, with a check at the end (Kim et al. 2025).
9. **Write your own skills and instruction files by hand, keep them short, and test them with and without the skill.** AI-written ones made results worse (SkillsBench v4; Gloaguen et al. 2026).
10. **Before connecting an AI to your email, files or accounts, count the three risks:** reading untrusted content, access to private data, ability to act or send. Allow at most two, or require your approval (Meta's Rule of Two; your manual §17.3).
11. **Read any skill or plugin before installing it,** however good its description sounds (Saha et al. 2026; Snyk 2026).
12. **Treat a model's explanation as a lead, not proof.** Check the claim against the source (Chen et al. 2025; Young 2026).
13. **Grade facts the way your kit already does:** SUPPORTED, PARTIALLY_SUPPORTED, CONTRADICTED or UNVERIFIED. This report was produced that way.

## 7. Still open

**Update, October 22, 2026.** Sections 3.2, 3.3 and 3.4 are applied to the taxonomy and logged in its Section 27.7, each source re-opened first. The five web sources were checked in a browser: entries 74, 81 and 111 hold as written; entry 112 gains its pages (PMLR 267:44554–44570), and entry 136 its full title and date (*OWASP Top 10 for Agentic Applications for 2026*, December 9, 2025). The "71.7% benign" sentence was deleted, since no source for it was found. The first two bullets below are therefore closed.

- Five web sources need a manual browser check (Section 3.4).
- The Section 16.2 "71.7% benign" sentence needs its real source.
- Whether `skills-ref`'s strictyaml parser accepts folded `>` descriptions is unconfirmed. Running `skills-ref validate` once on your two folded-description skills would settle it.
- Several skill-method items were confirmed by the researcher but not reached by the re-checker within its cap (marked in `run2.json`). Their sources are named in `skills-method.md`.
- This research covered the taxonomy and the skill kit. The Prompt Construction Guide's 150 examples and the Engineering Stack parts 1–11 were not part of it.

## 8. Files

| File | What it holds |
|---|---|
| `RESEARCH_REPORT.md` | This report |
| `bibliography-audit.md`, `bib-check.md`, `bib-check.json` | Every citation compared with arXiv and Crossref |
| `carried-over.md`, `web-sources.md` | The never-re-read figures and the web-only sources |
| `frontier-a1-a2.md`, `frontier-a3-a4.md`, `frontier-a5-a6.md`, `frontier-a7.md` | New research per axis, with quotes and URLs |
| `skills-hosts.md`, `skills-method.md`, `skills-research.md` | The skill-builder checks |
| `verify-*.md`, `run2.json` | The independent re-checks and the raw structured results |
| `tools/` | The scripts used (bibliography check, transcript recovery) |
