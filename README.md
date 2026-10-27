# AI Engineering Workspace

Research, Agent Skills and a Claude Code plugin for building with AI models, made by Aaron working with AI models. Every claim carries a tag that says how it was checked, the labs prove their own checks can fail, and the mistakes made along the way are kept as rules.

| Tag | Meaning |
|---|---|
| [V] | Verified against a source that was actually opened |
| [T] | Tested: the code was run and the output copied |
| [R] | Reader test: a person ran it at the keyboard |
| [U] | Unverified |
| [I] | Illustrative: an invented example for teaching |

## What's inside

| Folder | What it holds |
|---|---|
| `research/engineering-stack/` | *The AI Engineering Stack*: 13 parts (about 215,000 words) from setup and evals to agents, security, running models and shipping, each with a hands-on lab; the claim and freshness ledgers; Windows test records. Start with its `INVENTORY.md` |
| `research/prompting/` | *The Taxonomy of Prompt Engineering*, 3rd edition (October 20, 2026), *The Prompt Construction Guide*, 2nd edition, and the methods behind them |
| `research/source-checks-2026-10-15/` | A check of the taxonomy and the skill kit against primary sources |
| `research/ai-reports/` | AI-written reports, kept as claims to check, not as facts |
| `research/prompt-organizer/` | A prompt library index and template |
| `research/council-runs/` | Tests of the Planetary Council against an answer key it never saw |
| `plugins/planetary-council/` | The Planetary Council plugin, version 1.3.3: an orchestrator (the Sun), nine specialist agents and Planet X, an independent fact-checker. 10 agents and 13 skills |
| `skills/` | Seven Agent Skills: a prompt-suite generator, a quantum entanglement lab, a cross-model accuracy verifier, a server log triager, trig-check, qubit-math and a book chapter splitter. `build_skill.py` packages a skill; `_skill-builder-kit/` holds the skill-building prompt and validators |
| `tools/` | `check_workspace.py` (checks the pages against the files), `package_for_claude_ai.py` (builds claude.ai upload files) and `local-model/` (a bridge to a small local model) |
| `.agents/skills/`, `AGENTS.md` | Entries that let Codex find the same skills |
| `CLAUDE.md`, `LESSONS.md` | The rules any AI model working here follows, and 45 traps already hit, each with the rule it led to |

## Try it

**Run a lab.** Part 13's lab needs only Python 3.11 to 3.13: no model, account or key.

```
cd research/engineering-stack/labs/part-13
python run_lab.py
```

It runs 21 checks; on Windows 11 with Python 3.13.16 it passed 21 of 21, five times in a row [T, October 26, 2026]. Then `python mutation_check.py` breaks the lab 48 ways, one copy at a time, and each break must be caught (about 5 minutes). All 13 labs have the same pair of scripts.

GitHub shows a hidden-Unicode warning on `research/engineering-stack/labs/part-10/run_lab.py`. The hidden characters are there on purpose: the lab's check 5 tests that invisible text gets stripped.

**Use the plugin.** Open this folder in Claude Code. `.claude/settings.json` registers the folder as a plugin marketplace and turns on `planetary-council-system`. Turn on web search and web fetch, then ask "Run the council on: …", or one specialist at a time ("Ask Mercury …"). The plugin's own `README.md` has the details.

**Check the repository.** `python tools/check_workspace.py` checks that the counts, versions and links in the pages match the files. Standard library only; it changes nothing.

**Optional: the local model.** `tools/local-model/` lets Claude Code hand small text jobs to a model running in Ollama on your computer. Copy `.mcp.json.example` to `.mcp.json` and fill in the two paths. It is slow on ordinary hardware (Part 11 measured qwen3:1.7b at 8.0 to 8.4 tokens per second on an office PC's processor), so it suits short tagging jobs, not long files.

## How the work was checked

- **Tagged claims.** The parts tag each claim; the claim ledger lists the claims against their sources, and the freshness ledger tracks the facts that go stale (versions, prices, model shutdowns), with re-check dates where one is due.
- **Labs that test their own tests.** Each lab's `mutation_check.py` plants faults and expects the checks to catch every one.
- **Reader tests.** The labs were also run on a Windows 11 PC, by script and by hand; the records are in `research/engineering-stack/docs/records/`.
- **The council against a hidden answer key.** Test A planted 4 wrong facts among 8 claims; every agent caught all 4 from primary sources. Test B asked what this repository needed before going public; the council found 11 of 14 points on the hidden key, one plain agent found 8. Details: `research/council-runs/2026-10-26-test-a/SCORE.md` and `research/council-runs/2026-10-26-test-b-summary.md`.
- **Mistakes kept.** `LESSONS.md` lists 45 traps in 7 groups, from Windows encoding errors to tests that passed for the wrong reason.

## How it was made

Aaron built this with AI models: mostly Claude (Anthropic), with some work by Codex (OpenAI). Much of the text was written by AI and checked as described above; the tags show what was checked and what wasn't. Facts with dates go stale, so check the freshness ledger's re-check dates. This project is not affiliated with or endorsed by Anthropic or OpenAI.

## This public copy

Made on October 26, 2026 from a private working repository, as one fresh first commit. Left out: working notes with personal context, the decision and log pages, and a pip report that held third-party email addresses. In logs and records the user folder appears as `%USERPROFILE%` and package maintainers' emails as `[email removed]`. The texts still cite some files by their old `claude/...` names; `research/engineering-stack/INVENTORY.md` maps each one and lists everything left out.

## Licences

- **Code, skills, the plugin and tools:** MIT (`LICENSE`). This includes all code under `research/`, such as the labs.
- **The written research** (the Markdown files under `research/`): CC BY 4.0 (`LICENSE-docs`). You may reuse it with credit.

This is a summary, not legal advice; the licence files are what count.

## Contributing

Found a wrong claim, a broken lab or a stale fact? Please open an issue and say where (file and line) and what you saw. This is a personal research project, so pull requests aren't accepted; corrections that come from issues are made here.
