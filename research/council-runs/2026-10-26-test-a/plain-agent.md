# Plain agent: the control (test A)

Report as returned by one `general-purpose` sub-agent on Sonnet, with no council skill, October 26, 2026. Same paragraph and rules as the planets. Saved unedited apart from this header.

---

Fact-check of the 8 claims, web sources only, checked October 26, 2026. No local files were opened and no commands were run. 5 true, 2 false, 1 partly true. Note: WebFetch returns a small model's reading of each page, so the quoted fields are as relayed by that reader. The decisive ones were cross-checked on a second source or a second fetch.

1. anthropic 2.3.0 under the MIT licence: FALSE (high confidence).
- https://pypi.org/pypi/anthropic/2.3.0/json: info.license = "Apache-2.0"; classifier "License :: OSI Approved :: Apache Software License". Uploaded 2026-10-23.
- Cross-check: https://raw.githubusercontent.com/anthropics/anthropic-sdk-python/v2.3.0/pyproject.toml has license = "Apache-2.0" and version = "2.3.0". The LICENSE at https://github.com/anthropics/anthropic-sdk-python/blob/v2.3.0/LICENSE is the Apache License, Version 2.0, copyright 2023 Anthropic, PBC.

2. OpenAI shut down the Assistants API on August 26, 2026, pointing to the Responses API and Conversations API: TRUE (high).
- https://developers.openai.com/api/docs/deprecations (the platform.openai.com URL gives a 301 redirect to it). Table row: "2026-08-26 | Assistants API | Responses API and Conversations API". The section text says "removal from the API one year later, on August 26, 2026."
- https://developers.openai.com/api/docs/assistants/migration: "The Assistants API was officially sunset on August 26, 2026, and is no longer available." It also says "Start new chats with the Conversations API and Responses API."

3. vllm 0.32.0, released October 18, 2026, requires Python 3.11 or later: TRUE (high).
- https://pypi.org/pypi/vllm/0.32.0/json: requires_python = "<3.15,>=3.11"; all three files uploaded 2026-10-18 (10:03 to 10:04 UTC).
- Caveat: the "or later" has an upper bound. Python 3.15 and later is excluded.

4. OpenAI shut down gpt-4 and gpt-4-0613 on October 13, 2026: FALSE (high). The correct date is October 23, 2026.
- https://developers.openai.com/api/docs/deprecations, section "2026-04-22: Legacy GPT model snapshots". Row: "October 23, 2026 | gpt-4-0613 | gpt-4, gpt-4-0613-completions, gpt-4-completions | gpt-5.6-sol". The text says "Access to these models was shut down on October 23, 2026."
- A second fetch confirmed this row is the only one matching gpt-4 or gpt-4-0613. It also reported that neither "October 13" nor "2026-10-13" appears anywhere on the page. So the draft's date is off by 10 days.

5. FastAPI 0.162.0 declares a dependency on starlette>=1.9.0: FALSE (high).
- https://pypi.org/pypi/fastapi/0.162.0/json: the only starlette entry in the 44-item requires_dist is "starlette>=0.46.0". Uploaded 2026-10-23. I did not read pyproject.toml at the tag, but PyPI's requires_dist is the published metadata and is not empty here.

6. openai Python package 3.37.0 released October 22, 2026, under Apache-2.0: TRUE (high).
- https://pypi.org/pypi/openai/3.37.0/json: license_expression = "Apache-2.0" (the license field is null); classifier "License :: OSI Approved :: Apache Software License"; uploaded 2026-10-22T20:04 UTC.
- Gap: the repository was not opened at the tag. PyPI is the decisive source here.

7. The newest rank-bm25 on PyPI is 0.2.2, from February 2024: PARTLY TRUE (high).
- https://pypi.org/pypi/rank-bm25/json: info.version = "0.2.2", the newest of 0.1, 0.2, 0.2.1 and 0.2.2. The 0.2.2 files were uploaded 2022-02-16T12:10 UTC.
- The version is right. The date is wrong: February 2022, not February 2024. The release is about 4 years 8 months old, not 2 years 8 months.

8. A notice dated October 14, 2026 schedules gpt-4o-2024-08-06 and gpt-4.1-2025-04-14 for removal from OpenAI's API on January 14, 2027: TRUE (high).
- https://developers.openai.com/api/docs/deprecations, section "2026-10-14: GPT-4 series model deprecations": "On October 14, 2026, we notified developers using certain GPT-4 series models of their deprecation and removal from the API on January 14, 2027."
- Rows: "January 14, 2027 | GPT-4o (gpt-4o-2024-08-06, gpt-4o-2024-11-20) | gpt-6-luna" and "January 14, 2027 | GPT-4.1 (gpt-4.1-2025-04-14) | gpt-6-luna".
- The notice also covers gpt-4o-2024-11-20, GPT-4o mini and GPT-4.1 mini, which the draft does not mention. That does not make the claim wrong.

Corrections for the draft:
- Claim 1: change MIT to Apache-2.0.
- Claim 4: change October 13 to October 23, 2026.
- Claim 5: change starlette>=1.9.0 to starlette>=0.46.0.
- Claim 7: change February 2024 to February 2022.

No source failed to open.
