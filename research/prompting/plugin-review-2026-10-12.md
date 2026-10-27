# Plugin and connector review, October 12, 2026

What was checked in the claude.ai directory for this project's work (prompting, evals, skill building, papers, math), and what the code of four community plugins can reach. Read on October 12, 2026; plugins change, so re-read before installing a newer version.

## Sign-in needed (from each connector's detail page, "Sign-in" field)

| Connector | Publisher | Sign-in | Use here |
|---|---|---|---|
| Wolfram | Wolfram Research | Not required | Independent exact computation to check trig-check, qubit-math and paper arithmetic |
| alphaXiv | alphaXiv | Required | arXiv search and full text |
| Consensus | Consensus | Required | Paper search |
| Scholar Feed | Scholar Feed | Required | CS and AI paper search |
| Hugging Face | Hugging Face | Account needed (owner's note) | Model cards, Part 11 |

## Community plugins: code read in full

Method: shallow git clone of each repository, every file listed, manifests and skills read, code searched for network calls, shell commands, file writes and hidden Unicode characters (none found).

| Plugin | What ships | Sends data anywhere? | Writes or deletes | Fit here | Verdict |
|---|---|---|---|---|---|
| Prompt Design (bogheorghiu/prompt-design 0.1.5, MIT) | Instructions only: one SKILL.md (177 lines) and two example files. No scripts, hooks or MCP servers | No. Its PRIVACY.md says it sends nothing; the code agrees. It does tell Claude to verify claims with web search or subagents when available, so prompt text can reach those tools | Nothing | Prompt review in the fabel style; overlaps the project's own guides. Opens with a persona ("You are a prompt-engineering specialist"), which project rule 4 for skills avoids, and asks for up to three-source verification passes, which costs usage | Safe to add; optional |
| skill-validator (aliksir 1.3.1, MIT) | One Node.js script (1,045 lines) plus two slash commands, documented in Japanese | No user data. A normal run asks the npm registry for its own latest version at the end (`--no-version-check` skips it). `--update` pulls new code into your skills from their git origins; `--self-update` reinstalls itself from npm | `--fix` edits skill files, with a backup | Claude Code only: scans `~/.claude/skills`, needs Node.js on the computer. Does not see claude.ai account skills | Safe, but not useful until Claude Code and Node.js are set up; never run `--update` |
| skill-doctor (amaljithkuttamath 1.0.0, MIT) | Three skills (instructions), no scripts or network calls | No network. Sends each skill's text to a Claude subagent for review (stays inside Claude) | Reads CLAUDE.md and all skills; writes `~/.skill-doctor/`; its migrate step replaces your skill files after a backup and per-skill confirmation; `rm -rf` on its own staging folder | Claude Code only. The main skill has Bash and Write and can trigger on its own | Safe in design; not useful for claude.ai skills; would need watching |
| DeepEval (confident-ai/deepeval 1.0.0, Apache-2.0) | Three instruction skills that teach Claude to add the DeepEval library to code | The skills send nothing. The library they install sends anonymous usage events to PostHog (us.i.posthog.com) unless `DEEPEVAL_TELEMETRY_OPT_OUT` is set; tracing and reports go to Confident AI's cloud with an API key | Writes test files into a project | Its metrics need model credentials (an API key) and its cloud features need `deepeval login`, both against this project's no-keys rule | Skip for now; material for Part 02's tool comparison |

## Not added

The session's attempt to click Connect for Wolfram was stopped by the permission check, so nothing was connected; the owner clicks Connect himself.
