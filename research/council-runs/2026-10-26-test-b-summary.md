# Council test B: the go-public review (summary)

**Date:** October 26, 2026. **Question:** what must change before this workspace goes public on GitHub, and what should change so it looks professional? This summary replaces the agents' full reports, which stay in the private workspace because they describe the personal details they found.

## Design

- **A hidden answer key.** Before any agent ran, Claude wrote down its own read-only scan of the workspace: 5 must-fix items and 4 should-fix items. The key was kept outside the workspace, so no agent could read it.
- **The council:** Mercury (what leaks), Saturn (licences and lasting consequences) and Pluto (what must end) ran first; Earth (steel-man and synthesis) second; Planet X last. Planet X got 10 load-bearing claims, stated neutrally, without the other agents' reasoning. All five ran on Sonnet.
- **A control:** one plain agent, with no council skill, got the same question and rules.
- **Rules for every agent:** read-only, no commands, personal details reported as file, line and kind only, and each finding with its file, line and fix.

Test A, the easier test that ran first, is in `2026-10-26-test-a/`.

## Results

Must-fix items score 2 and should-fix items 1, with half marks for partial finds; the maximum is 14.

| Item on the key | Council (any agent) | Plain agent |
|---|---|---|
| Personal details about the owner in two working notes | found | partly |
| The owner's own words quoted in 9 files | partly | partly |
| No LICENSE file, though the skills declared MIT | found | found |
| Third-party email addresses in a pip report | found | **missed** |
| One personal email address on every commit | found | found |
| A README written for the owner, not for visitors | found | found |
| Hard-coded user paths | found | found |
| Old `claude/...` links that lead nowhere | missed | missed |
| No description, topics, release tag or citation file | missed | missed |
| **Score (of 14)** | **11** | **8** |

Scored one by one, Pluto alone reached 11, Earth 10, and Mercury and Saturn 8 each.

- **False alarms:** none from the council. The plain agent raised one: an ignore rule for a folder this workspace doesn't have.
- **New findings:** the agents found 14 real problems that weren't on the key, each checked by Claude against the file, git or a count. Examples: a log stored twice, byte for byte; 19 links to a local-only file; stray files from an old lab version; hidden Unicode test data that GitHub flags; no `*.pdf` rule in `.gitignore`.
- **A count everyone got wrong.** Agents put the third-party emails at 49, 165 and 219, and Claude's own scan said "about 140" without counting. Planet X found the cause: 219 was a count of lines, and 16 of the "addresses" were code fragments such as `\n@app.get`. The re-count is 189 distinct email-like strings (326 occurrences) [T].
- **Independence:** two agents reported that a broad search listed file names from the folder where the others' answers were being saved; both said they didn't open or use them. Saturn, in the first wave, read the run plan before that folder was excluded from the instructions; the plan holds no answers.

## What it shows

1. On an open-ended review, several agents cover more than one: the council found the third-party emails, which the plain agent missed.
2. Most of the gain comes from having several readers rather than any one lens, since Pluto alone matched the council's combined score.
3. Planet X is worth its place: its grades matched the checks, and it settled a count that every other agent got wrong.
4. The council costs more: 369,915 tokens for its five agents against 154,356 for the plain agent [T], about 2.4 times as much.

## What changed because of it

The findings became the checklist for this public copy: a fresh first commit, licence files, the personal notes and the pip report left out, user paths and emails replaced in the logs, a map for the old `claude/` links, and a README for visitors. The full list is in the root `README.md` ("This public copy") and in `research/engineering-stack/INVENTORY.md`.
