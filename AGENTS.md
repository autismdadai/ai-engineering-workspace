# Codex project guidance

This repository is shared across models. Before substantial work, read `README.md`, `CLAUDE.md` and `LESSONS.md`, and check the current files rather than relying on older notes.

## Project skills

Codex discovers repository skills under `.agents/skills/`. Each `SKILL.md` there is a small entry that points to the canonical skill instructions elsewhere in this repository. When one is selected, read and follow its linked canonical `SKILL.md`; resolve its scripts and references relative to that canonical skill folder. Edit canonical skill sources only. If a skill refers to an MCP tool that is not available in this session, state that and use its documented fallback rather than claiming the tool ran.

Canonical sources remain in `skills/`, `plugins/planetary-council/skills/`, `.claude/skills/`, and the Part 07 lab's `research/engineering-stack/labs/part-07/skills/` folder. Duplicate source copies with the same name are exposed once in `.agents/skills/`.

## Owner boundaries

Every rule in `CLAUDE.md` applies to Codex exactly as it does to Claude, in all its sections, including no spending and asking before any download, install, or running code. Report exact commands and captured results for tests that were actually run.

Traps already hit here are in `LESSONS.md`. `CLAUDE.md` loads `LESSONS.md` with an `@LESSONS.md` line; read the file directly.
