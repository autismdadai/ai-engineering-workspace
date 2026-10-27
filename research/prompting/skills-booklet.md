# Skills Booklet: Plan, Build, Test, Add and Use a Skill

*Version 1.0, October 8, 2026. It replaces claude/skill-install-guide.md (October 7), whose steps are all carried over here. The product steps were checked against the official pages under Sources on October 8, 2026. Menus change: if a step doesn't match your screen, the linked page wins.*

## How to use this booklet

- **Building a new skill:** do Steps 1 to 10 in order. Each step ends with a **Done when** line, the check that says you can move on.
- **Installing a skill that's already built:** Step 8. **Using one:** Step 9.
- **The running example** is trig-check (built October 7). book-chapter-splitter (October 8) was built by these steps from start to finish.
- **Words used here:** a *skill* is the folder; *loading* (also called *triggering*) is Claude deciding to open it; the *host* is the app that runs it: the Claude app, Claude Code, Cursor and so on.

## The whole job on one page

| Step | What you do | Done when |
|---|---|---|
| 1. Decide | Check that a skill is the right tool | You can say the one job in one sentence |
| 2. Intake | Answer five questions; write 10 requests that should load it and 10 that shouldn't | They're in the skill's evals/evals.json |
| 3. Describe | Write the long and the short description | Both fit their limits and match the requests |
| 4. Write | SKILL.md: steps, rules, limits | A stranger could follow it |
| 5. Script | Exact work goes in scripts that print JSON | Normal input works; bad input is refused |
| 6. Test | Known answers, mutation check, grader, trigger tests, with and without | Every test can fail, and the README says what ran |
| 7. Package | build_skill.py makes three packages | It prints PASS |
| 8. Add | Install it in each app you use | It's listed and switched on |
| 9. Use | Ask normally, or ask for it by name | A fresh chat loads it and runs its script |
| 10. Maintain | New version, re-test, re-package, update the file map | Every copy shows the same version |

## Step 0. What a skill is

**In plain words:** a folder of instructions that Claude reads only when a request needs it. **The technical term:** an Agent Skill, an open format (agentskills.io) that Claude and other AI tools load.

```
my-skill/
├── SKILL.md       name and description at the top, then the instructions
├── scripts/       code Claude runs for the exact parts (optional)
├── references/    longer notes Claude reads only when needed (optional)
├── assets/        templates, images or data (optional)
└── evals/         your tests; never shipped with the skill
```

Claude uses a skill in three stages, which the spec calls progressive disclosure:

1. **At the start of every session,** Claude sees only each skill's name and description, about 100 tokens per skill.
2. **When a request matches a description,** Claude reads the whole SKILL.md. The spec recommends keeping it under 500 lines and 5,000 tokens.
3. **Only when a step needs them,** Claude opens a reference file or runs a script.

So the description decides whether a skill is used at all, the body decides how well it's used, and the scripts make the exact parts exact.

## Step 1. Decide whether it should be a skill

| You want | Use |
|---|---|
| A rule for every chat in one project | Project instructions |
| Documents to look things up in | Project knowledge (docs and files) |
| A one-off task | Just ask |
| A repeatable job with steps, used in several chats or apps, ideally with a script for the exact parts | A skill |
| Several jobs at once, or an independent check | Still one agent plus skills by default. Add agents only for separate jobs that can run side by side, or for a check that must not see the work, and say what they cost (project rule) |

**Done when:** you can say the one job in one sentence. trig-check's: "Check trigonometry with a script instead of by eye."

## Step 2. Intake: five questions before writing anything

1. **The one job,** in one sentence.
2. **Who uses it, and where:** the Claude app, Claude Code, other tools.
3. **Twenty test requests:** 10 that should load it, written the way people really ask, and 10 that shouldn't. Make the second list near misses: keyword traps ("Convert 70°F to Celsius" for a skill about degrees), other skills' jobs, and look-alike tasks.
4. **Tools and permissions:** what it may run, read and write, and whether it needs the network.
5. **What right looks like:** three tasks with known answers, and what it must refuse.

Template:

```
ONE JOB:
WHO AND WHERE:
SHOULD LOAD (10):
SHOULD NOT LOAD (10, each with why):
TOOLS AND PERMISSIONS:
THREE TEST TASKS WITH ANSWERS:
MUST REFUSE:
```

A shortcut: the Claude app has a built-in skill-creator skill, switched on in your account. Describe the job and answer its questions, and it drafts a skill for you to save. Hold its draft to Steps 3 to 6 before you rely on it.

**Done when:** the answers are in the skill's `evals/evals.json`, under `intake` and `triggers`.

## Step 3. Write the description: it decides whether the skill loads

Rules:

- **Third person:** what it does, when to use it, and when not to.
- **The words people type.** A description that says "computes reduced density matrices" can miss "what's left of qubit 1?"
- **Name the neighbors.** Say which nearby jobs belong to another skill: "Do not use to run the six standard entanglement experiments (quantum-entanglement-lab does that)."
- **Easy-looking requests.** If the skill should load even when a question looks easy, say so. In the first trigger tests (October 8), Claude Code loaded trig-check and qubit-math for requests that asked to check, solve or show something, and skipped them for quick textbook questions it answered itself (claude/trigger-tests-2026-10-08.md).

Two descriptions, because the hosts have different limits:

| Field | Limit | Used by |
|---|---|---|
| `description` | 1,024 characters (the spec) | Claude Code, Cursor, Gemini CLI, Codex, Copilot |
| `metadata.claude-app-description` | 200 characters | Uploads to the Claude app |

`skills/build_skill.py` swaps in the short one for the Claude app packages.

**The name:** 1 to 64 characters; lowercase letters, digits and single hyphens, not at the start or end; the same as the folder's name. Anthropic's docs add two rules for Claude: no XML tags in the name or description, and no "anthropic" or "claude" in the name.

Example, trig-check:

- **Long (515 characters):** "Checks trigonometry with a script instead of by eye: tests whether an identity holds (and gives a counterexample when it fails), gives exact values, converts between degrees and radians, and solves triangles from three parts, including the two-triangle SSA case. Use when someone asks whether a trig identity is true, wants an exact trig value or an angle conversion, or needs a triangle solved. Do not use for calculus, statistics, algebra with no trig in it, or word problems that still need a model set up first."
- **Short (179 characters):** "Checks trig with a script: tests identities (with counterexamples), gives exact values, converts degrees/radians, solves triangles incl. SSA. Not for calculus or non-trig algebra."

**Done when:** both fit their limits, each should-load request shares words with the description, and each should-not request is ruled out by it.

## Step 4. Write SKILL.md

Skeleton:

```markdown
---
name: my-skill
description: >
  Does X with a script instead of by eye. Use when someone asks for A, B or C.
  Do not use for D or E (other-skill does E).
license: MIT
metadata:
  version: "1.0"
  requires: "python3, somepackage"
  claude-app-description: "Under 200 characters: what it does; not for D or E."
---

# My skill

One or two sentences: what to do, and why the script matters.

## Steps
1. Check the package once: `python3 -c "import somepackage"`. If that fails, run `pip install somepackage`.
2. Turn the request into one command: `python3 scripts/my_script.py ...`
3. Read the JSON and answer in plain words, using its numbers.

## Reading the results
What each field means, and what to say when a check fails.

## Limits
What it doesn't do, why, and what to do instead.

## Reference
`references/notes.md` has ... Read it only when ...
```

Rules (from the project's instructions):

- **Short.** Under 500 lines, and shorter is better: trig-check's is 47 lines.
- **No persona** ("You are an expert..."). Personas didn't improve accuracy across 162 personas and 2,410 MMLU questions (Zheng et al., Findings of EMNLP 2024), and they cost words.
- **Reasons, not capitals.** Give the reason for a rule instead of writing it in capitals; a reason lets Claude handle cases the rule didn't name.
- **One level of references.** Point to each reference file from SKILL.md and say when to read it.

**Done when:** someone who has never seen the skill could follow the steps without asking you anything.

## Step 5. Scripts and references

Put anything exact in a script: math, page ranges, parsing, counting. Script rules:

1. **Print JSON,** so Claude reads structured results, not prose.
2. **Never ask for input.** A script waiting for an answer hangs the run.
3. **Refuse bad input instead of guessing.** Check input against an allowlist and never pass it to `eval` or a shell. trig-check accepts only named math functions; book-chapter-splitter refuses file names with folders in them.
4. **Fail loudly.** Use explicit checks, not `assert`: running Python with `-O` strips every assert, which let a broken lab print six PASS lines in version 1.1.
5. **Write only where told,** and use no network unless the job needs it.
6. **Exit codes:** 0 when everything passed, 1 when a check failed, 2 when the input was refused.

References hold the long parts: tables, worked examples, sources with dates.

**Done when:** each script runs from the skill folder, prints JSON for a normal input, and refuses a bad one with exit code 2.

## Step 6. Test it: the eval pack

The project's rule: prove that each test can fail. A test that can't fail proves nothing.

| Layer | Where | What it shows | trig-check |
|---|---|---|---|
| a. Known answers | `evals/test_<name>.py` | The script gives the right answers and refuses bad input | 21 of 21 |
| b. Mutation check | `evals/mutation_check.py` | Breaks the script on purpose, one way at a time; a named test must catch each break, and a harmless change must still pass | 14 of 14 runs as expected |
| c. Answer grader | `evals/grade_answer.py --self-test` | Each task's known-good answer passes and its known-bad answer fails | 5 of 5 |
| d. Trigger tests | `triggers` in evals.json | The skill loads for its 10 requests and stays off for the other 10 | 6 of 10 loaded, 10 of 10 left off (Claude Code, first pass) |
| e. With and without | `with_and_without` in evals.json | Answers are better with the skill, not just different | Not run yet |
| f. Adversarial cases | `adversarial` in evals.json | False premises and traps are caught | In the grader |

Run a to c from the skill folder:

```bash
python evals/test_trig_check.py
python evals/mutation_check.py
python evals/grade_answer.py --self-test
```

What the mutation checks caught: the lab's version 1.1 tests let 4 of 16 deliberate faults through, including a CHSH angle 0.05 rad off; book-chapter-splitter's first out-of-range test was masked by its page-limit rule until it asked for one page past the end.

**Trigger tests (d), two ways:**

- **By hand, in any app:** install the skill, send each request in a fresh chat, and note which skill loaded. In the Claude app, Claude's thinking shows it reading the skill.
- **Automatically, in Claude Code:** `claude plugin eval` (Claude Code 2.1.269 or later) sends each request to a fresh, isolated session and checks whether Claude called the Skill tool. The starter kit's `tools/make_trigger_evals.py` writes every case from each skill's evals.json. A case is a folder with a prompt and a grader:

`evals/trig-check-yes-01/prompt.md`

```markdown
---
tags: [trigger, trig-check]
max_turns: 4
allowed_tools: [Skill, Read, Glob, Grep]
---

Is sin(2x) = 2 sin(x) cos(x) actually an identity? Check it.
```

`evals/trig-check-yes-01/graders/trig-check-loads.md`

```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?trig-check"'
---
```

For a request that shouldn't load the skill, the grader adds `min: 0`, `max: 0` and `arm: both`, so it passes only if the skill was never called.

Run one skill's cases: `claude plugin eval trigger-tests --ablation none --runs 1 --tag trig-check --no-publish`. Each run is a real model call on your account; on October 8 each one cost about $0.04 to $0.06 at list price, as the tool estimated. `--no-publish` keeps the report on your computer.

**With and without (e):** run the same tasks with and without the skill, three times each, in fresh sessions. Each helper works in its own empty folder that can't see `evals/`, so it can't read the known answers. Write the decision rule before running ("keep the skill if it wins on t3 and loses on none"). In Claude Code, `claude plugin eval` without `--ablation none` adds a no-skill baseline and reports the difference.

Record every result in the skill's `evals/README.md`: the date, versions, numbers, and what hasn't been run.

**Done when:** a to c pass, the mutation check shows every test can fail, and the README says what ran and what didn't.

## Step 7. Package it

From the folder that holds `skills/`:

```bash
python skills/build_skill.py skills/trig-check --out dist
```

| Package | For |
|---|---|
| `trig-check.zip` | Claude Code and other tools: the folder, with the long description |
| `trig-check-claude-app.zip` | Uploading to the Claude app: the same folder, with the short description |
| `trig-check.single-file.md` | Save cards and chat apps: one SKILL.md with the scripts bundled at the end, each with its SHA-256 so a copy can be checked |

It checks the name rules, both description lengths, angle brackets, the 500-line limit (for the single file too), and that every bundled file reads back byte for byte. `evals/` never goes into a package, because it holds known wrong answers that an agent shouldn't see.

**Done when:** it prints `"result": "PASS"`.

## Step 8. Add it

### 8a. The Claude app

Once, before the first skill: open **Settings > Capabilities** and turn on **Code execution and file creation**. Skills don't run without it. The Help Center lists skills for Free, Pro, Max, Team and Enterprise plans. On Team and Enterprise, an owner turns skills on under **Organization settings > Plugins & skills > Policy**.

From a ZIP:

1. Open **Customize > Skills**.
2. Click **+**, then **+ Create skill**, then **Upload a skill**.
3. Choose `<name>-claude-app.zip`. The skill folder must be the ZIP's top level and carry the skill's name; build_skill.py does both.
4. Switch the skill on.

From a save card: when Claude shows a skill card in a chat, click **Save**. A card carries one SKILL.md (its name, description and instructions; other frontmatter and extra files are dropped), so a skill with scripts comes as its single-file version, with the scripts inside.

Sharing: on Team and Enterprise you can share a skill with colleagues, who can view it but not edit it. On Free, Pro and Max, each person uploads their own copy.

Removing (checked October 7): open the skill, switch it off, click **…** next to the switch, and choose **Delete**.

### 8b. Claude Code

| Scope | Put the folder in | Notes |
|---|---|---|
| You, every project | `~/.claude/skills/<name>/` (on Windows, `C:\Users\<you>\.claude\skills\<name>\`) | Loads in sessions on your computer |
| One project | `<project>/.claude/skills/<name>/` | Commit it, and Claude Code on the web loads it from the repository |

- Edits to an existing skill apply right away. A new top-level skills folder needs `/reload-skills`. `/skills` lists what's loaded.
- Skills switched on in the Claude app also carry over to Claude Code on the web.
- To share several skills from GitHub, make them a plugin: a folder with `.claude-plugin/plugin.json` and `skills/<name>/SKILL.md`. Others add it with `/plugin marketplace add owner/repo`, then `/plugin install <plugin>@<marketplace>`. Check one with `claude plugin validate <folder>`. A plugin runs code with your permissions, so read it before installing it.

### 8c. Other tools

| Tool | Project folder | Personal folder |
|---|---|---|
| Cursor | `.agents/skills/` or `.cursor/skills/` (it also reads `.claude/skills/`) | `~/.agents/skills/` or `~/.cursor/skills/` |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/` | `~/.gemini/skills/` or `~/.agents/skills/` |
| OpenAI Codex | `.agents/skills/` | `~/.agents/skills/` |
| GitHub Copilot | `.github/skills/`, `.claude/skills/` or `.agents/skills/` | `~/.copilot/skills/` or `~/.agents/skills/` |
| VS Code | the same three as Copilot | `~/.copilot/skills/`, `~/.claude/skills/` or `~/.agents/skills/` |

One copy in `~/.agents/skills/` covers Cursor, Gemini CLI, Codex and Copilot; Claude Code needs its own copy in `~/.claude/skills/`.

Calling a skill by hand (checked October 7): in Cursor, type `/` in Agent chat and pick it; Gemini CLI asks you to approve activating a skill, and can also install one with `gemini skills install <path or Git URL>`; in Codex, type `$` or `/skills`. The ChatGPT desktop app lists standalone skills under **Skills** in its sidebar (type `@` to use one); on ChatGPT's web and mobile apps, OpenAI's docs offer skills only inside plugins.

On Windows (PowerShell):

```powershell
py -m pip install pypdf sympy numpy scipy qutip
mkdir $HOME\.agents\skills -Force
mkdir $HOME\.claude\skills -Force
Expand-Archive $HOME\Downloads\trig-check.zip -DestinationPath $HOME\.agents\skills
Expand-Archive $HOME\Downloads\trig-check.zip -DestinationPath $HOME\.claude\skills
```

Each ZIP holds one folder named after the skill, so you end up with `...\skills\trig-check\SKILL.md`. trig-check needs sympy, qubit-math numpy, book-chapter-splitter pypdf, and the lab qutip, numpy and scipy.

### 8d. Chat apps that don't load skills

Grok, the Gemini web app and ChatGPT on the web don't read skill folders (checked October 7). Paste `<name>.single-file.md` into the app's custom instructions, a project or a Gem, or attach it and say "Follow this skill." The scripts run only if the app can run Python and install packages; if it can't, treat its numbers as unchecked. trig-check (sympy), qubit-math (numpy) and book-chapter-splitter (pypdf) travel best; the lab needs qutip, which most chat sandboxes don't have.

**Done when:** the skill shows in the app's list and is switched on.

## Step 9. Use it

- **Ask normally.** Claude picks a skill by matching your request to its description.
- **Or ask for it by name:** "Use trig-check to solve this triangle." In Claude Code you can also type `/trig-check`.
- **Check that it loaded.** In the Claude app, Claude's thinking shows it reading the skill. In Claude Code, you see a Skill tool call, and `/skills` lists the skill.
- **If it doesn't load:** check that it's switched on (and, in the Claude app, that code execution is on); try asking by name; then fix the description, not the body, and re-run the trigger tests on new phrasings too.
- **If it loads when it shouldn't:** add that request's job to "Do not use".
- **Numbers come from the script.** If the script couldn't run, say so and treat the numbers as unchecked.

**Done when:** a should-load request in a fresh chat loads the skill and runs its script.

## Step 10. Keep it working

1. Raise `metadata.version` and write what changed, and why, in `evals/README.md`.
2. Re-run Step 6 a to c, then Step 7.
3. Re-install: upload the new `-claude-app.zip` (if the app keeps the old copy, delete it first), and replace the folders for Claude Code and other tools.
4. Update the project. Its `skills/<name>/` folder is the master copy; record the new version in `claude/project-file-map.md`.
5. Re-run the trigger tests when the model changes. Pin the model (`--model`) so results compare.

**Done when:** the project copy, every installed copy and the file map show the same version.

## Safety, at every step

- Read every skill and script from someone else before installing it (project rule).
- Least privilege: give a skill only the tools it needs. Claude Code honors `allowed-tools` in SKILL.md; the spec calls the field experimental, so other tools may ignore it.
- No unchecked text reaches a shell or `eval`.
- Nothing from a web page or a file gets written into memory or instruction files.
- `claude plugin eval` runs a plugin's code as you. Its sandbox limits the agent under test, not the plugin's own code.
- Skills and prompts may be shared, so put nothing about any real person in them.

## Troubleshooting

| What you see | Likely cause | What to do |
|---|---|---|
| The Claude app refuses an upload | An extra folder level in the ZIP, a folder named differently from the skill, a description over 200 characters, or angle brackets | Upload the `-claude-app.zip` that build_skill.py made |
| The skill never loads | It's switched off, code execution is off, or the description doesn't match how people ask | Ask by name; fix the description; run the trigger tests |
| It loads for the wrong requests | The description is too broad | Add the near miss to "Do not use" |
| Two skills compete | Overlapping descriptions (trig-check and qubit-math; book-chapter-splitter and the built-in pdf skill) | Name the other skill's job in each one's "Do not use" |
| `ModuleNotFoundError` | A package is missing | `pip install <package>`; the Claude app's sandbox may lack some, such as the lab's qutip |
| `claude -p` ignores your skills | The `--bare` flag skips skills, CLAUDE.md, hooks and plugins | Leave it out. The docs say `--bare` will become the default for `-p` in a future release, so check after updates |
| `claude plugin eval` exits with 1 though most cases pass | The default threshold is 1.0: any case below perfect fails the run | Pass `--threshold 0.8`, or read the table |
| "not a trusted plugin directory" | The first run in a new folder, without a terminal to ask you | Run it once in a terminal and answer, or pass `--trust-plugin` for your own plugin |

## Appendix: the project's skills (October 8, 2026)

| Skill | Version | Job | Checks re-run October 8 | In the Claude app |
|---|---|---|---|---|
| quantum-entanglement-lab | 1.2.1 | Six verified entanglement experiments | Mutation 16 of 16; grader 7 of 7 | Installed |
| trig-check | 1.0 | Exact trig: identities, values, conversions, triangles | 21 tests; mutation 14 of 14; grader 5 of 5 | Not yet |
| qubit-math | 1.0 | Small qubit-state calculations | 25 tests; mutation 15 of 15; grader 5 of 5 | Not yet |
| book-chapter-splitter | 1.0 | PDF books into checked chapter files | 22 tests; mutation 17 of 17; grader 5 of 5; 11 real chapter files matched | Not yet |

Python 3.13; SymPy 1.14.0, QuTiP 5.3.1, numpy 2.5.3, pypdf 5.9.0. What to build next: claude/handoff-2026-10-08.md.

## Sources (checked October 8, 2026)

- Agent Skills specification: https://agentskills.io/specification
- Claude Help Center, "Use skills in Claude": https://support.claude.com/en/articles/12512180-use-skills-in-claude
- Claude Help Center, "How to create custom skills": https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- Claude Help Center, sharing skills and plugins: https://support.claude.com/en/articles/13119606
- Anthropic Academy, "How to create a skill with Claude through conversation": https://academy.claude.com/tutorials/how-to-create-a-skill-with-claude-through-conversation
- Claude Code docs, skills: https://code.claude.com/docs/en/skills
- Claude Code docs, plugins: https://code.claude.com/docs/en/plugins/overview and https://code.claude.com/docs/en/plugins/install
- Claude Code docs, plugin evals: https://code.claude.com/docs/en/plugin-evals
- Claude Code docs, headless mode: https://code.claude.com/docs/en/headless
- Cursor: https://cursor.com/docs/context/skills
- Gemini CLI: https://geminicli.com/docs/cli/skills/
- OpenAI Codex: https://developers.openai.com/codex/skills/ (now redirects to OpenAI's "Build skills" page for Codex and ChatGPT, https://learn.chatgpt.com/docs/build-skills)
- GitHub Copilot: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
- VS Code: https://code.visualstudio.com/docs/copilot/customization/agent-skills
