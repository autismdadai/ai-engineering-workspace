# Council test A: answer key (written before any agent ran)

Written October 26, 2026 (local), before launching any agent. Kept outside the workspace so no agent can read it.
Source of each answer: the workspace's freshness ledger (`research/engineering-stack/docs/engineering-stack-freshness-ledger.md`), rows checked against primary sources on the dates shown. If an agent cites a primary source that disagrees, Claude re-checks that source before scoring.

## The paragraph the agents receive

A draft status note for a software project says: The anthropic Python SDK, version 2.3.0, is released under the MIT licence. OpenAI shut down the Assistants API on August 26, 2026, and points users to the Responses API together with the Conversations API. vllm 0.32.0, released on October 18, 2026, requires Python 3.11 or later. OpenAI shut down access to gpt-4 and gpt-4-0613 on October 13, 2026. FastAPI 0.162.0 declares a dependency on starlette>=1.9.0. The openai Python package 3.37.0 was released on October 22, 2026, under the Apache-2.0 licence. The newest release of rank-bm25 on PyPI is 0.2.2, from February 2024. A notice dated October 14, 2026 schedules gpt-4o-2024-08-06 and gpt-4.1-2025-04-14 for removal from OpenAI's API on January 14, 2027.

## Key

| # | Claim | Answer | The fact (ledger row) |
|---|---|---|---|
| C1 | anthropic 2.3.0 is MIT | FALSE (planted) | Apache-2.0; the repository LICENSE is MIT at v1.14.0 and Apache 2.0 from v2.0.0 (line 82, Oct 26) |
| C2 | Assistants API shut down Aug 26, 2026; Responses + Conversations | TRUE | line 16 |
| C3 | vllm 0.32.0, Oct 18, 2026, Python 3.11+ | TRUE | `<3.15,>=3.11`, 2026-10-18 (line 47, Oct 26) |
| C4 | gpt-4 shut down Oct 13, 2026 | FALSE (planted) | October 23, 2026 (line 17, Oct 26) |
| C5 | FastAPI 0.162.0 needs starlette>=1.9.0 | FALSE (planted) | declares `starlette>=0.46.0` (line 75, Oct 26) |
| C6 | openai 3.37.0, Oct 22, 2026, Apache-2.0 | TRUE | line 81, Oct 26 |
| C7 | rank-bm25 newest 0.2.2 from February 2024 | FALSE (planted) | 0.2.2 is from February 16, 2022 (line 68, re-checked Oct 13) |
| C8 | Oct 14 notice; removal Jan 14, 2027 | TRUE | line 18, Oct 26 |

## Scoring (decided before the run)

- **Catch:** a planted claim graded false (or "partly true" with the wrong part named) with a primary source that shows the right value.
- **False alarm:** a true claim graded false.
- **Source quality:** each verdict names a primary source it opened (vendor page, PyPI JSON, repository at the tag). A local file path or no source counts as unsourced.
- **Pass for test A:** Planet X catches all 4 planted claims with no false alarms; Mercury and Venus together catch at least 3 of 4. The plain agent is scored the same way for comparison.
