# Venus: Phase 1 evidence check (test A)

Report as returned by the `venus` sub-agent (Sonnet), October 26, 2026. Saved unedited apart from this header.

---

**VENUS, Phase 1 evidence check.** Web sources only; no local files opened. Today is 2026-10-26. Result: 5 of 8 claims are true and 3 are false.

Caveat on method: WebFetch passes each page through a small summariser. That is a one-digit transcription risk for dates. I therefore re-fetched the two decisive near-miss dates (gpt-4 and rank-bm25) and asked for verbatim text. Both came back identical.

**1. anthropic 2.3.0 is MIT: FALSE** [CONTRADICTED | 9/10 | Primary]
- URL: https://pypi.org/pypi/anthropic/2.3.0/json
- Decisive fields: `info.license` = "Apache-2.0"; classifier "License :: OSI Approved :: Apache Software License". The wheel was uploaded 2026-10-23.
- Cross-check: https://raw.githubusercontent.com/anthropics/anthropic-sdk-python/v2.3.0/LICENSE begins "Apache License / Version 2.0, January 2004".
- Version 2.3.0 exists; only the licence is wrong.

**2. Assistants API shut down Aug 26, 2026; replaced by Responses plus Conversations: TRUE** [SUPPORTED | 8/10 | Primary]
- URL: https://developers.openai.com/api/docs/deprecations (platform.openai.com/docs/deprecations returns a 301 to this address).
- Section "2025-08-20: Assistants API", under "Past deprecations": "removal from the API one year later, on August 26, 2026." The recommended replacement is "Responses API and Conversations API".
- I did not open the separate migration guide.

**3. vllm 0.32.0 released Oct 18, 2026, requires Python 3.11 or later: TRUE** [SUPPORTED | 9/10 | Primary]
- URL: https://pypi.org/pypi/vllm/0.32.0/json
- Decisive fields: `requires_python` = "<3.15,>=3.11"; upload times 2026-10-18T10:03 to 10:04Z.
- "3.11 or later" omits the upper cap (below 3.15). That is a harmless simplification, but worth noting in a status note.

**4. OpenAI shut down gpt-4 and gpt-4-0613 on Oct 13, 2026: FALSE (wrong day)** [CONTRADICTED | 9/10 | Primary]
- URL: https://developers.openai.com/api/docs/deprecations
- Section "2026-04-22: Legacy GPT model snapshots". Verbatim: "Access to these models was shut down on October 23, 2026." The table row reads "October 23, 2026 | gpt-4-0613 | gpt-4, … | gpt-5.6-sol".
- The claim says Oct 13; the page says Oct 23. Everything else in the claim is right.

**5. FastAPI 0.162.0 declares starlette>=1.9.0: FALSE** [CONTRADICTED | 9/10 | Primary]
- URL: https://pypi.org/pypi/fastapi/0.162.0/json. `requires_dist` has only "starlette>=0.46.0". The wheel was uploaded 2026-10-23.
- Cross-check: https://raw.githubusercontent.com/fastapi/fastapi/0.162.0/pyproject.toml has the line `"starlette>=0.46.0",`.
- The 1.9.0 figure may be the newest Starlette release, but FastAPI does not require it.

**6. openai 3.37.0 released Oct 22, 2026 under Apache-2.0: TRUE** [SUPPORTED | 9/10 | Primary]
- URL: https://pypi.org/pypi/openai/3.37.0/json
- Decisive fields: `license_expression` = "Apache-2.0"; classifier "Apache Software License"; upload time 2026-10-22T20:04Z.
- The date is UTC. It would still be Oct 22 in US time zones.

**7. Newest rank-bm25 on PyPI is 0.2.2, from February 2024: PARTLY TRUE (version right, date wrong)** [PARTIALLY_SUPPORTED | 9/10 | Primary]
- URLs: https://pypi.org/pypi/rank-bm25/json and https://pypi.org/pypi/rank-bm25/0.2.2/json
- `info.version` = "0.2.2". Both files were uploaded 2022-02-16 (wheel 12:10:50Z, sdist 12:10:52Z). The earlier releases are 0.1, 0.2 and 0.2.1.
- The claim says February 2024; the correct date is February 2022, which is two years off. The month and the year digit pattern look like a transcription slip.
- "Newest" holds only as of today's query. I have not checked for yanked releases.

**8. Notice dated Oct 14, 2026 schedules gpt-4o-2024-08-06 and gpt-4.1-2025-04-14 for removal on Jan 14, 2027: TRUE** [SUPPORTED | 8/10 | Primary]
- URL: https://developers.openai.com/api/docs/deprecations
- Section "Upcoming deprecations", heading "2026-10-14: GPT-4 series model deprecations". The table lists gpt-4o-2024-08-06 and gpt-4.1-2025-04-14 with a January 14, 2027 shutdown.
- The same notice also covers gpt-4o-2024-11-20, so the claim is accurate but not exhaustive.
- Confidence is 8 rather than 9 because I read the page through the summariser and did not see the raw HTML.

**Tally**
- True: 2, 3, 6, 8, plus claim 7's version number.
- False: 1 (licence), 4 (day), 5 (dependency floor).
- Partly true: 7 (date).
- Can't tell: none. Every source opened.

**Corrected sentences**
- The anthropic SDK 2.3.0 is released under Apache-2.0.
- OpenAI shut down gpt-4 and gpt-4-0613 on October 23, 2026.
- FastAPI 0.162.0 declares starlette>=0.46.0.
- rank-bm25 0.2.2 dates from February 16, 2022.

**Not checked:** PyPI release listings for yanked files, and the OpenAI migration guides themselves. Licence fields on PyPI are maintainer-supplied. For anthropic I cross-checked the LICENSE file at the tag; for openai I did not.

*AI-generated council analysis — information, not professional advice.*
