# Council test A: score

Scored October 26, 2026 against `ANSWER_KEY.md` (in this folder; written before any agent ran and kept outside the workspace until now). Design and rules: `RUN_PLAN.md`.

## Result: pass

| Agent | Planted errors caught (of 4) | False alarms | Verdicts without a primary source | Summary line matches its own verdicts | Tokens | Tool calls | Time |
|---|---|---|---|---|---|---|---|
| Mercury | 4 | 0 | 0 | yes | 35,402 | 13 | 88 s |
| Venus | 4 | 0 | 0 | no: says "5 of 8 claims are true and 3 are false", but lists 4 true, 3 false, 1 partly true | 30,186 | 12 | 64 s |
| Planet X (claims only) | 4 | 0 | 0 | yes | 37,969 | 13 | 94 s |
| Plain agent (control) | 4 | 0 | 0 | no: says "5 true, 2 false, 1 partly true", but lists 4 true, 3 false, 1 partly true | 106,381 | 14 | 91 s |

All counts [T]. Tokens, tool calls and times are the harness's figures for each sub-agent. "Caught" for C7 means graded partly true with the date named as the wrong part, as the scoring rules allowed.

- **Pass rule met:** Planet X caught all 4 with no false alarms; Mercury and Venus together caught 4 of 4 (the rule asked for 3).
- **Sources:** every verdict from every agent names a primary source: OpenAI's deprecations page, PyPI's JSON API, or the repository at the release tag. No agent's report names a local file.
- **No disputes with the key:** every agent agreed with every answer, so no re-check was needed.
- **Extra true details** found by the agents, not in the key: vllm 0.32.0 also caps Python below 3.15; the October 14 notice also covers gpt-4o-2024-11-20 and the mini models; OpenAI's migration guide says the Assistants API "is no longer available" (plain agent).

## What it shows

1. **The checking works.** On single facts that one primary source settles, all three council agents and Planet X got 8 of 8 right, each from primary sources [T].
2. **This test didn't separate the council from one plain agent.** The plain agent also caught 4 of 4. Every planted error could be settled with one page fetch, so the test was too easy to show any added value from the council. Test B (an open-ended review with no single right page) is the better test of that.
3. **The council cost about the same as one plain agent:** 103,557 tokens for Mercury, Venus and Planet X together against 106,381 for the plain agent [T]. The plain agent carries every tool, while each planet carries only a few. This is a likely reason, not a measured one [U].
4. **Summary lines can't be trusted; the verdicts can.** Two of four reports miscounted their own verdicts in the summary line, though every verdict was right. Whoever writes the Council Brief should recount from the verdicts and never copy a summary line.
5. **Planet X's independence held:** it got the claims without the planets' reasoning and reached the same verdicts from its own fetches. That is agreement from a separate context, not a copy.

## Cost

| | 5-hour window | Weekly |
|---|---|---|
| Estimate [I] | about 15 points | about 2 points |
| Before | 3% | 19% |
| After wave 1 (Mercury, Venus, plain agent) | 10% | 20% |
| After wave 2 (Planet X) | 12% | 20% |
| **Actual** | **9 points** | **1 point** |

The actual figures include Claude's own work as the Sun (planning, saving, scoring).
