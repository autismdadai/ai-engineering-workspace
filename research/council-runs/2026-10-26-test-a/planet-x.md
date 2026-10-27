# Planet X: independent verification (test A)

Report as returned by the `planet-x` sub-agent (Sonnet), October 26, 2026. It received the 8 claims only, not the planets' reasoning. Saved unedited apart from this header.

---

DEEP RESEARCH BRIEF (web only; no local files touched)
Result: 4 SUPPORTED (C2, C3, C6, C8), 1 PARTIALLY_SUPPORTED (C7), 3 CONTRADICTED (C1, C4, C5). Accuracy by protocol formula = (4 + 0.5x1)/8 ~ 56%.

VERIFICATION STATUS [grade | confidence | source class]

C1. anthropic 2.3.0 is MIT. CONTRADICTED | 9/10 | Primary
- https://pypi.org/pypi/anthropic/2.3.0/json (opened twice): info.license = "Apache-2.0"; license_expression = null; classifier "License :: OSI Approved :: Apache Software License". Upload 2026-10-23.
- https://github.com/anthropics/anthropic-sdk-python/blob/v2.3.0/LICENSE: Apache License 2.0, "Copyright 2023 Anthropic, PBC."

C2. Assistants API shut down Aug 26, 2026; users pointed to Responses API + Conversations API. SUPPORTED | 8/10 | Primary
- https://developers.openai.com/api/docs/deprecations (platform.openai.com/docs/deprecations 301-redirects here). Entry "2025-08-20: Assistants API": "removal from the API one year later, on August 26, 2026"; "migrate your current integration to the Responses API and Conversations API."
- Caveat: I did not test the live endpoint; the page states the removal date.

C3. vllm 0.32.0, released Oct 18, 2026, requires Python 3.11+. SUPPORTED | 9/10 | Primary
- https://pypi.org/pypi/vllm/0.32.0/json: requires_python = "<3.15,>=3.11"; upload 2026-10-18T10:03-10:04Z. Note there is also an upper bound (<3.15).

C4. gpt-4 and gpt-4-0613 shut down Oct 13, 2026. CONTRADICTED | 8/10 | Primary
- Same deprecations page, entry "2026-04-22: Legacy GPT model snapshots": gpt-4-0613 plus aliases gpt-4, gpt-4-0613-completions, gpt-4-completions have shutdown date October 23, 2026 ("Access to these models was shut down on October 23, 2026"); substitute gpt-5.6-sol. Nothing gives Oct 13. The page's past tense in an April entry is odd, but the date is Oct 23 either way.

C5. FastAPI 0.162.0 declares starlette>=1.9.0. CONTRADICTED | 9/10 | Primary
- https://pypi.org/pypi/fastapi/0.162.0/json: requires_dist has one unconditional starlette line, "starlette>=0.46.0". Upload 2026-10-23.
- https://raw.githubusercontent.com/fastapi/fastapi/0.162.0/pyproject.toml (release tag): `"starlette>=0.46.0",`. Both sources agree.

C6. openai 3.37.0 released Oct 22, 2026, Apache-2.0. SUPPORTED | 9/10 | Primary
- https://pypi.org/pypi/openai/3.37.0/json: license_expression = "Apache-2.0" (info.license null); classifier Apache Software License; upload 2026-10-22T20:04Z.
- https://github.com/openai/openai-python/blob/v3.37.0/LICENSE: Apache License 2.0, "Copyright 2026 OpenAI".

C7. Newest rank-bm25 is 0.2.2, from February 2024. PARTIALLY_SUPPORTED | 9/10 | Primary
- https://pypi.org/pypi/rank-bm25/json: newest info.version = 0.2.2 (version part SUPPORTED). Upload time 2022-02-16T12:10Z, so "February 2024" is CONTRADICTED (month right, year two years off).
- Release history: 0.1 (2019-01), 0.2 (2019-04 sdist / 2020-06 wheel), 0.2.1 (2020-06), 0.2.2 (2022-02).

C8. Notice dated Oct 14, 2026 schedules gpt-4o-2024-08-06 and gpt-4.1-2025-04-14 for removal Jan 14, 2027. SUPPORTED | 9/10 | Primary
- Deprecations page, entry "2026-10-14: GPT-4 series model deprecations": "On October 14, 2026, we notified developers using certain GPT-4 series models"; "removal from the API on January 14, 2027." Both models are in the table, shutdown Jan 14, 2027, replacement gpt-6-luna. The table also lists gpt-4o-2024-11-20, gpt-4o-mini-2024-07-18 and gpt-4.1-mini-2025-04-14 with the same date.

PRIMARY SOURCES: PyPI JSON for anthropic/2.3.0, vllm/0.32.0, fastapi/0.162.0, openai/3.37.0 and the rank-bm25 index; repo files at release tags (anthropic-sdk-python v2.3.0 LICENSE, openai-python v3.37.0 LICENSE, fastapi 0.162.0 pyproject.toml); https://developers.openai.com/api/docs/deprecations.

MATRIX FLAG: None.

REPRODUCIBILITY AND LIMITS: Re-open each URL and read the named field. All fetches were summarised by a small model, so quotes came through that tool, not raw bytes. Cross-checks with a second source: C1 (twice plus repo), C5 (PyPI and repo), C6 (PyPI and repo), C4 and C8 (two fetches of the deprecations page, which agreed). C2, C3 and C7 rest on one source each. OpenAI's page can change; dates apply as of October 26, 2026.

AI-generated council analysis - information, not professional advice.
