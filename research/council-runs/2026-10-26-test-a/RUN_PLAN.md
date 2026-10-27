# Council test A: planted errors

**Date:** October 26, 2026 (local). **Asked for by:** the owner, as the first half of a question on the owner's decisions page, which stays private (a real task through the council, compared with one plain agent).

## What it tests

Whether Phase 1 (Mercury, Venus) and Planet X can tell true claims from quietly wrong ones by checking primary sources, and whether they do it better than one plain agent given the same task.

## Design

- **The input:** one paragraph of 8 claims about software releases and model shutdowns. Four are true and four have one detail changed (a date, a version or a licence). The facts come from the workspace's freshness ledger, whose rows were checked against primary sources between October 13 and 26, 2026.
- **The answer key** was written before any agent ran and kept outside the workspace, so no agent could read it. It is added to this folder after scoring.
- **Agents:**
  - Wave 1, in parallel: Mercury and Venus (planet agents, Sonnet) and one plain `general-purpose` agent on Sonnet. All three get the same paragraph and the same rules.
  - Wave 2: Planet X gets the 8 claims stated neutrally as a list, without the planets' reasoning, as the council skill requires.
- **Rules every agent got:** web sources only (the workspace holds notes on the same facts, so reading local files would void the test); primary sources first; for each claim a verdict, the URL opened, the deciding text and a confidence; "can't tell" rather than a guess; under 700 words.

## Scoring (fixed before the run)

- **Catch:** a planted claim graded false (or partly true with the wrong part named), with a primary source showing the right value.
- **False alarm:** a true claim graded false.
- **Unsourced:** a verdict with no primary source opened, or with a local file as its source.
- **Pass:** Planet X catches all 4 planted claims with no false alarms, and Mercury and Venus together catch at least 3 of 4. The plain agent is scored the same way.
- When an agent cites a primary source that disagrees with the key, Claude re-checks that source before scoring.

## Cost

- **Estimate:** about 15 points of the 5-hour window and about 2 weekly points [I], scaled from the October 26 full council (10 agents, about 40 points and 5 weekly points [T]).
- **Before the run:** 3% of the 5-hour window, 19% weekly [T: get_usage].
