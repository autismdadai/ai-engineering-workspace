# skills-research report (R01-R04 + new findings)

Date: 2026-10-15. Web lookups used: 20 of 20 (cap reached). Local file reads cost no lookups. Every item R01-R04 was reached; nothing is marked "not reached".

How the lookups were spent: R01 x4 (abstract page, v1 abstract, HTML body, HTML body second part); R02 x3 (search, Snyk post, Snyk table recheck); R03 x5 (search, Snyk post, arXiv 2604.02837, Snyk article, arXiv 2608.03509); R04 x2 (skill-creator raw file, Anthropic docs); new findings x6 (arXiv 2605.11418, one search, then 2608.11888, 2609.29454 abstract, 2607.01456, 2609.29454 body). 2604.02837 and 2608.03509 were opened under R03 and are also listed as new findings. Total 20.

Caveat that applies to everything below: the fetch tool answers through a small summarising model and would not give long verbatim passages. Numbers, filenames and dates come from those answers. I did not open PDFs. Where a figure came from a search summary and not from a page I opened, I say so.

## Verdicts at a glance

| Item | Verdict |
|---|---|
| R01 "focused skills (2-3 modules) beat comprehensive docs" | True of SkillsBench v1 (as the Reference cites it). Newer version restates it with different numbers; the "comprehensive" bucket is only 5 tasks. |
| R01 "self-generated skills gave no average benefit" | True of v1. Latest version reports a drop (-8.1 to -11.5 pp) on all three configurations tested. Out of date. |
| R02 Reference wording (36.82% any flaw, 13.4% critical, 76 malicious, 3,984 skills) | Faithful. |
| R02 Omnibus wording ("36.8% ... contain architectural flaws") | Not faithful. Number right, description wrong. |
| R03 indirect prompt injection via loaded skill files | Supported, with a scope note. |
| R03 persistent poisoning of memory files (MEMORY.md) | Supported for OpenClaw's files; Omnibus generalises. |
| R03 conditional backdoors hidden from static analysis | Only partly supported. The "encrypted payloads ... specific prompt strings" wording was not found in any source I opened. |
| R04 "20 queries split 60/40" | Real, but it is the default of Anthropic's skill-creator tool for tuning a description, not a documented standard. "Similarity loops" is not Anthropic's term. |

## R01  SkillsBench (arXiv 2602.12670)

Pages opened: arxiv.org/abs/2602.12670 (shows four versions: v1 13 Feb 2026, v2 7 Mar, v3 13 Mar, v4 14 Jun 2026), arxiv.org/abs/2602.12670v1, arxiv.org/html/2602.12670 (latest, v4). I did not open v2 or v3.

Version 1 abstract (the Reference v1.2 line 29 says "version 1", so it is citing this):
- 86 tasks, 11 domains, 7 agent-model configurations, 7,308 trajectories. Each task run with no Skills, curated Skills and self-generated Skills.
- Curated Skills raised average pass rate by 16.2 percentage points (+4.5 pp Software Engineering to +51.9 pp Healthcare; 16 of 84 tasks got worse).
- Focused Skills with 2 to 3 modules beat comprehensive documentation.
- Self-generated Skills gave no benefit on average; the authors conclude models cannot reliably write the procedural knowledge they benefit from reading.

Latest version (v4, June 2026):
- 87 tasks, 8 domains, 18 model-harness configurations. Curated Skills lift the average pass rate from 33.9% to 50.5% (+16.6 pp, my subtraction), range +4.1 to +25.7 pp.
- Abstract now says focused Skills of at most three modules beat larger bundles. My paraphrase of the v4 abstract page did not mention self-generated Skills; the body does (next point).
- Self-generated Skills: the body says they land below the no-Skills baseline on all three configurations in that test: Claude Code with Opus 4.7 -8.1 pp, Codex with GPT-5.5 -11.3 pp, Gemini CLI with Gemini 3.1 Pro -11.5 pp. This condition was run on those three configurations only. The paper gives no pooled figure (the simple mean is about -11 pp; that is my arithmetic).
- Appendix F (18 configurations, 87 tasks, three trials). Skills per task: 1 Skill, 23 tasks, +18.0 pp; 2-3 Skills, 43 tasks, +19.0 pp; 4 or more Skills, 21 tasks, +10.1 pp. Skill size: compact 22 tasks +19.0 pp; standard 22 tasks +21.5 pp; detailed 38 tasks +14.5 pp; comprehensive only 5 tasks, +0.7 pp. "Comprehensive" means the largest SKILL.md text sizes (above roughly the 95th percentile of the benchmark's skills); exact character thresholds not found.
- My caution, not the paper's: these buckets compare different tasks, so they show a pattern, not a controlled test. Five tasks is a thin base for the "comprehensive is flat" line.

Grade for the Reference sentence: SUPPORTED as a version-1 statement; PARTIALLY SUPPORTED as a current one. Suggested rewrite: "In SkillsBench (arXiv 2602.12670, v4), curated Skills raised average pass rate from 33.9% to 50.5% across 18 configurations; tasks with 2-3 Skills gained about 19 pp versus about 10 pp for 4 or more; Skills built by the model itself lowered pass rate by 8.1 to 11.5 pp on the three configurations tested."

## R02  Snyk ToxicSkills (published 5 Feb 2026)

Source: snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/ (opened twice; publication date 2026-02-05 in the page metadata).
- Scanned 3,984 skills from ClawHub and skills.sh as of 5 Feb 2026.
- 36.82% (1,467 skills) have at least one security flaw. This counts any flaw at any severity (the post gives examples such as hardcoded API keys, insecure credential handling, risky third-party content). It is not a count of prompt injection or of malware.
- 13.4% (534 skills) have at least one critical-level issue.
- 76 malicious payloads confirmed by human review.
- Table in the post (percent of skills; columns skills.sh top 100 / confirmed malicious / ClawHub all): prompt injection 0.0 / 91 / 2.6; malicious code 0.0 / 100 / 5.3; suspicious download 0.0 / 100 / 10.9; credential handling 5.0 / 63 / 7.1; secret detection 2.0 / 32 / 10.9; third-party content 9.0 / 54 / 17.7; unverifiable dependencies 2.0 / 21 / 2.9; direct money access 2.0 / 10 / 8.7.
- Trap inside the source: the post's headline says prompt injection in 36% and 1,467 malicious payloads. The body and table do not support that. Prompt injection on ClawHub is 2.6%; 1,467 is skills with any flaw; the malicious count is 76. Anyone quoting the headline gets it wrong.
- The word "architectural" does not appear. Nearest wording is "insecure by design".

Omnibus line 46 ("36.8% of available community registry assets contain architectural flaws"): NOT faithful. (1) "architectural" is not Snyk's term; (2) it drops "at least one" and the any-severity scope; (3) it turns a two-registry snapshot of 3,984 skills into "available community registry assets". Reference v1.2 line 264 is faithful. Suggested Omnibus text: "In Snyk's 5 Feb 2026 scan of 3,984 skills from ClawHub and skills.sh, 36.82% had at least one security flaw of any severity, 13.4% had a critical issue, and 76 were confirmed malicious."

## R03  Primary sources for the Omnibus threat types (Omnibus lines 47-49)

Opened: the Snyk ToxicSkills post; Snyk article "From SKILL.md to Shell Access in Three Lines of Markdown" (Liran Tal, 3 Feb 2026, snyk.io/articles/skill-md-shell-access/); arXiv 2604.02837; arXiv 2608.03509. The manual already cites Greshake et al. (arXiv 2302.12173; Works Cited item 82, already verified), so I did not reopen it.

1. Indirect prompt injection via loaded skill files: SUPPORTED, with a scope note.
 - Origin: Greshake et al. 2023 (arXiv 2302.12173): instructions hidden in content a model retrieves (web pages, documents, emails).
 - Skills: the Snyk post lists skills that fetch untrusted content, which enables indirect prompt injection, and describes a chain where an attacker posts poisoned content, a legitimate skill retrieves it, and the agent treats it as commands (the skill author may have done nothing wrong). arXiv 2604.02837 names the missing separation between data and instructions as one of the most severe structural threats to Agent Skills.
 - Scope note: text written directly into a SKILL.md or bundled reference by a malicious author is a supply-chain attack, not "indirect" in Greshake's sense. Per the table above, 91% of the 76 confirmed malicious skills also used prompt injection. The Omnibus line mixes the two cases.

2. Persistent poisoning of memory files such as MEMORY.md: SUPPORTED, with a scope note.
 - Snyk post: tells readers to review the memory files SOUL.md and MEMORY.md for unauthorized changes and warns that malicious skills can change agent behaviour permanently (persistent memory that survives across sessions is on its list of what makes skills dangerous).
 - Snyk article: ClawHavoc attackers targeted OpenClaw's SOUL.md and MEMORY.md; it also describes a staged attack where a first skill plants instructions in memory that run later when a specific user query triggers them (no concrete example given).
 - Scope note: those two files are OpenClaw's in Snyk's text. The Omnibus calls them generic "localized files". The mechanism fits any agent that auto-loads a writable memory file, but Snyk's evidence is about OpenClaw.
 - More on persistence: arXiv 2608.03509 (SkillJack) found 80.0% of skill-mediated attacks still worked after the original poisoned records were deleted.

3. Conditional backdoors hidden from static analysis ("encrypted payloads ... triggering only on specific prompt strings"): PARTIALLY SUPPORTED. The exact claim was not found.
 - Found in the Snyk post: obfuscated commands using base64 or Unicode to evade detection (example: a base64 eval that decodes to a credential-stealing curl); skills that look benign at review and change later because the logic is fetched from attacker-controlled servers.
 - Found in the Snyk article: instructions obfuscated to evade pattern matching; a malicious release pushed after a skill gains adoption; malicious functionality hidden in auxiliary files; the staged memory attack above.
 - Not found: explicit trigger-conditioned logic and "encrypted payloads" (the fetch reported both absent from the Snyk post and the article). arXiv 2608.03509 describes no trigger mechanism. arXiv 2605.11418 describes no trigger-conditioned backdoor either.
 - Suggested rewrite: "Payloads can be obfuscated (base64, Unicode), fetched from attacker servers after review, hidden in auxiliary files, or planted in memory to fire on a later query; pattern-matching scanners can miss these." Drop "triggering only on specific prompt strings" unless a source is added. Trigger-conditioned backdoors are documented for model weights (Sleeper Agents, arXiv 2401.05566; I did not open it), which is a different thing from a skill file.

## R04  "Trigger evals: 20 queries split 60/40"

Origin: Anthropic's skill-creator skill, Description Optimization section, plus its script scripts/run_loop.py. Checked in the public repo (raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md) and in the copy installed on this machine (skills-plugin/.../skills/skill-creator/SKILL.md line 339 and scripts/run_loop.py), which gave the exact defaults.

Exact content:
- The one quote I am keeping: "Create 20 eval queries — a mix of should-trigger and should-not-trigger."
- 8-10 should-trigger queries (varied phrasing, formal and casual, cases where the skill is not named, cases where it competes with another skill but should win) and 8-10 should-not-trigger queries. The valuable negatives are near-misses that share keywords but need something different; the text warns that obviously unrelated negatives test nothing.
- 60/40: run_loop.py has --holdout with default 0.4. split_eval_set holds out 40% of the should-trigger queries and 40% of the should-not-trigger queries separately (fixed seed 42), leaving 60% to train on. The loop rewrites the description using training results and chooses the final description by held-out test score.
- Other defaults in run_loop.py: 3 runs per query, trigger threshold 0.5 (a query counts as triggered if it fires in at least half its runs), up to 5 iterations, 30 s timeout per query, 10 parallel workers.

Anthropic's official docs (platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, opened): no mention of 20 queries, a 60/40 split, a held-out set or a trigger-rate threshold. They recommend writing three evaluation scenarios before extensive documentation, comparing against a no-skill baseline, testing with Haiku, Sonnet and Opus, and they state there is no built-in way to run such evaluations. Their checklist says at least three evaluations.

So 20 and 60/40 are the defaults of one Anthropic tool for tuning a skill's description. They are a reasonable starting design, not a validated sample size and not a documented requirement.

Faithfulness of the kit's wording:
- Omnibus line 42 ("Verify similarity loops against 20 queries split 60/40"): loose. "Similarity loops" is not Anthropic's term. Better: "Tune the description on about 12 of 20 queries (8-10 should-trigger, 8-10 near-miss should-not-trigger), pick the version by the roughly 8 held-out queries (the script rounds down per group), 3 runs each."
- Omnibus line 59 / Master prompt Phase 2 ("20 trigger queries (60/40 train/val)"): correct as a default, but should say it is skill-creator's default and add the near-miss requirement and the 3 runs.
- Universal master prompt v2.0 Phase 2 as written (read locally): at least 3 realistic tasks, run without the Skill and record the gap, trigger set with should-trigger and near-miss requests, validation kept separate from training, trigger tests kept apart from output quality. That matches the docs and skill-creator and needs no change.

## New findings (6 primary sources, 2026-07 to 2026-10; each opened)

All six are arXiv pages opened for this report. Submission dates are from the pages. They are preprints, not peer reviewed as far as I could see.

N1. arXiv 2609.29454, "Demystifying Agent Skills for Smart Contract Auditing: Design, Effectiveness, Behavioral Impact" (Cuifeng Gao et al., 24 Sep 2026). 83 public audit skills, EVMBench, seven agent-model setups, 40 audits per setup. A skill counts as triggered only if the agent actually loads its full SKILL.md; the name and description alone do not count. Activation varied from 40 of 40 audits (Codex with GPT-5.5) through 13 (Antigravity with Gemini 3.5 Flash), 3 and 1 (OpenCode with two models) to 0 of 40 (three setups, including Claude with Opus 4.8). Setups with no or little activation showed negligible or negative change in detection score (for example -9.4%, -5.9%, -8.8% for three DeepSeek-V4-Pro setups); Claude with Opus 4.8 gained 3.2% despite zero activation, unexplained. The top setup gained 22.8% detection score and 43.2% captured award. The paper says triggering is driven mainly by the model, not the harness. Scope: one domain, discovery left to the agent with no instruction to use skills. It gives no advice to authors on improving triggering.

N2. arXiv 2608.11888, "Agent Skills Can Be Harmful: An Empirical Study of Skill-Induced Failures in LLM Agents" (Gen Dong et al., 12 Aug 2026). Compared each skill-guided run with a no-skill or matched-skill run on SkillsBench and SWE-Skills-Bench: 307 skill-induced failures, 125 functional and 182 efficiency regressions. Functional failures usually came from skills that look relevant, leading the agent to implement parts wrongly or skip required parts. Efficiency regressions are not explained by prompt length alone; the biggest cause was excessive procedure, mainly excessive verification (67 cases) and heavy implementation pipelines (30 cases). They introduce a triage tool, SkillTriage. The abstract does not state the models used.

N3. arXiv 2605.11418, "Under the Hood of SKILL.md: Semantic Supply-chain Attacks on AI Agent Skill Registry" (Shoumik Saha et al., 12 May 2026). On real ClawHub skills: short text triggers in a skill reached an 86% pairwise win rate and 80% top-10 placement in embedding-based retrieval; description-only framing made agents pick functionally equivalent adversarial variants in 77.6% of paired trials on average; semantic evasion strategies avoided a blocking verdict from the governance check in 36.5% to 100% of cases depending on strategy. No defense is described on the page.

N4. arXiv 2604.02837, "Towards Secure Agent Skills: Architecture, Threat Taxonomy, and Security Analysis" (Zhiyuan Li et al., v1 3 Apr 2026, v2 revised 14 Oct 2026, so it may still change). Taxonomy of 7 categories and 19 scenarios across three attack layers over four lifecycle phases (creation, distribution, deployment, execution), mapped onto seven documented incidents. The authors say the most severe threats are structural: no clear separation between data and instructions, a single-approval persistent trust model, and capability declarations with no enforcement behind them, and that incremental patches will not fix them. This supports the Omnibus line that allowed-tools is not a security boundary (that line is outside R01-R04, so I did not check it separately).

N5. arXiv 2608.03509, "SkillJack: Persistent Skill Backdoors in Self-Evolving Agents" (Zonghao Ying et al., 4 Aug 2026, revised 7 Aug). Attack on agents that turn their own interaction histories into reusable skills. On SkillX, a safety detector's catch rate fell from 98.5% on poisoned trajectories to 11.4% on the skills extracted from them; implanted skills reached attack success of 56.2% (SkillX) and 89.2% (Anything2Skill); 80.0% of skill-mediated attacks still worked after the original poisoned records were deleted. 150 trajectories, four risk categories. The authors argue for tracking where each skill came from; they did not test a defense.

N6. arXiv 2607.01456, "From Anatomy to Smells: An Empirical Study of SKILL.md in Agent Skills" (David Boram Hong et al., 1 Jul 2026, v2 3 Jul). Analysis of 238 real skills gave a taxonomy of 13 higher-level and 44 lower-level components; best practices from a review of 29 sources; their detector found at least one "skill smell" (a break from those practices) in more than 99% of SKILL.md files, and smells rarely go away as skills change. They call for automated fixing tools and developer awareness.

## What someone building their own skills should do differently

1. Do not ship skills the model wrote on its own. SkillsBench v4 found self-written skills lowered pass rates by 8.1 to 11.5 pp on three configurations. Use the model to draft, then measure the draft against a no-skill run, then cut what does not close a measured gap. Your master prompt already says to record the gap first; add a plain rule that an unmeasured model-written skill is a draft, not a result.
2. Compare with and without the skill, on both pass rate and cost. Skills that look relevant can cause wrong or missing work, and mandatory verification checklists and heavy build recipes can add cost without benefit (N2). When a skill adds a required step, ask whether the task needs it.
3. Keep it small and few. Tasks with 2-3 Skills did better than tasks with 4 or more, and the very longest SKILL.md files showed no lift (R01; the long-file group is only 5 tasks). Your 500-line limit and one-job rule fit this. Consider also warning when a skill set for one task exceeds three.
4. Measure triggering from traces, separately from output quality, on each model you will use. Count a trigger only when the full SKILL.md was loaded. One study saw activation range from 0 to 40 of 40 audits across models (N1), so a skill that works on one model may never fire on another. Your master prompt already keeps these apart; add "per model" and "from the trace".
5. Use the 20-query / 60-40 design as a starting point, not a standard. About 12 training and 8 held-out queries is thin; near-miss negatives matter more than count. Report held-out results and say how many runs each.
6. Treat descriptions as a security surface when you pick other people's skills. A description alone swayed agent choice in 77.6% of paired trials (N3). Choose by reading the whole skill, not by its summary.
7. Do your own security pass; scanners are a floor. Snyk found 36.82% of 3,984 skills had at least one flaw and 76 were malicious. Read every script and reference, pin the version you reviewed (a skill can be updated after review), and check for fetched remote content, base64 or eval, hidden Unicode and writes to memory files. My keyword search of your two validators (validate_skill.sh, skill_audit.py) found none of those checks; I did not read them in full. Adding warnings for them is cheap but will not catch everything: one study saw governance checks evaded in 36.5% to 100% of cases (N3).
8. Be careful with skills that are built automatically from your own sessions. Poison in one input can become a lasting skill that survives deletion of the source (N5). Keep a note of where each skill came from and re-read generated skills before keeping them.
9. After removing a suspect skill, re-read your memory files. Snyk advises reviewing SOUL.md and MEMORY.md for unauthorized changes.
10. Run a lint for authoring smells. More than 99% of 238 real skills had at least one (N6). Your skill_audit.py covers some structure checks; compare it against the best-practice list in the Anthropic docs.

## Documents to correct

- Reference v1.2 line 29: add that the figures are from v1 and give the v4 numbers (R01 rewrite above).
- Omnibus line 46: replace with the R02 rewrite.
- Omnibus line 48: say "for example OpenClaw's SOUL.md and MEMORY.md" instead of a generic "localized files".
- Omnibus line 49: replace with the R03 rewrite; remove "encrypted" and "specific prompt strings" unless sourced.
- Omnibus lines 42 and 59: replace "similarity loops" and name skill-creator as the source of the defaults.
- Reference v1.2 line 264 (Snyk): faithful, no change.
- Universal master prompt v2.0 Phase 2: no change needed.

## Not verified

- SkillsBench v2 and v3 were not opened; only v1 and v4 were compared.
- The per-model lists for the SkillsBench Appendix F buckets were not found.
- The 2609.29454 triggering table and definition came from the paper body via the summarising fetch; the abstract page itself did not give them.
- Sleeper Agents (arXiv 2401.05566) and Agent Skills in the Wild (arXiv 2601.10338) appeared in results but were not opened.
- "Chapter 28 Still Unverified" and Appendix A of the Taxonomy were out of scope and not touched.
