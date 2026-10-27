# Mercury: Phase 1 triage (test A)

Report as returned by the `mercury` sub-agent (Sonnet), October 26, 2026. Saved unedited apart from this header.

---

**MERCURY, PHASE 1 TRIAGE: 8 claims. Web sources only; I opened no local files.**

Result: 4 true, 1 partly true, 3 false. Noo we're cookin' wi' gas, but three of these are wrong.

Method caveat: WebFetch returns a small-model extraction of each page, not raw bytes. Each of the three "false" verdicts on versions and licences (claims 1, 5 and 7) is backed by a second primary source. The gpt-4 date (claim 4) rests on one OpenAI page read twice. No source failed to open.

**1. anthropic 2.3.0 is MIT: FALSE** [CONTRADICTED | 9/10 | Primary] (Tier 4)
- Pure nonsense, away an' boil yer heid. The licence attribute is wrong against the primary record.
- https://pypi.org/pypi/anthropic/2.3.0/json shows `"license": "Apache-2.0"` and the classifier `License :: OSI Approved :: Apache Software License`. Upload was 2026-10-23.
- Repo at tag v2.3.0: `pyproject.toml` has `license = "Apache-2.0"`, and the LICENSE file opens "Apache License, Version 2.0".
- 2.3.0 does exist, and PyPI's newest-release JSON also reports 2.3.0.

**2. Assistants API shut down Aug 26, 2026; replaced by Responses plus Conversations: TRUE** [SUPPORTED | 8/10 | Primary] (Tier 1)
- https://developers.openai.com/api/docs/deprecations. The old platform.openai.com/docs/deprecations URL returns a 301 to this one.
- The entry dated 2025-08-20 says "removal from the API one year later, on August 26, 2026". The replacement column reads "Responses API and Conversations API".
- Confidence is 8, not 9, because I saw the scheduled date and not a separate past-tense "was shut down" line. The date has passed.

**3. vllm 0.32.0, released Oct 18, 2026, requires Python 3.11 or later: TRUE** [SUPPORTED | 9/10 | Primary] (Tier 1)
- https://pypi.org/pypi/vllm/0.32.0/json shows `upload_time_iso_8601` 2026-10-18T10:03:29Z (wheel) and `"requires_python":"<3.15,>=3.11"`.
- "3.11 or later" is incomplete: there is also an upper bound below 3.15. It isn't wrong.

**4. gpt-4 and gpt-4-0613 shut down Oct 13, 2026: FALSE (date wrong)** [CONTRADICTED | 8/10 | Primary] (Tier 4)
- The shutdown is real. The date in the note is not.
- https://developers.openai.com/api/docs/deprecations, entry "Legacy GPT model snapshots", dated 2026-04-22: "Access to these models was shut down on October 23, 2026."
- The table row reads `October 23, 2026 | gpt-4-0613 | gpt-4, gpt-4-0613-completions, gpt-4-completions | gpt-5.6-sol`.
- The note has Oct 13; the page has Oct 23. Failure mode: transposed or mistyped date. The page carries several entries with the same title; I used the one that lists gpt-4.

**5. FastAPI 0.162.0 requires starlette>=1.9.0: FALSE** [CONTRADICTED | 9/10 | Primary] (Tier 4)
- Christ, dae they think we're daft?
- https://pypi.org/pypi/fastapi/0.162.0/json shows `requires_dist` entry 1 as `starlette>=0.46.0` (unconditional, not tied to an extra). Upload was 2026-10-23.
- Repo at tag 0.162.0, `pyproject.toml`: `"starlette>=0.46.0"`.
- Two independent primary sources agree. 1.9.0 may be a newer Starlette release, but FastAPI does not require it.

**6. openai 3.37.0, released Oct 22, 2026, Apache-2.0: TRUE** [SUPPORTED | 9/10 | Primary] (Tier 1)
- https://pypi.org/pypi/openai/3.37.0/json shows upload 2026-10-22T20:04:37Z and `"license_expression":"Apache-2.0"`.
- The `license` field is null; the Apache classifier is present. That is a metadata-style difference, not a contradiction.

**7. Newest rank-bm25 is 0.2.2, from February 2024: PARTLY TRUE** [PARTIALLY_SUPPORTED | 9/10 | Primary] (Tier 4 on the date)
- https://pypi.org/pypi/rank-bm25/json: `info.version` is `0.2.2`. Both files were uploaded 2022-02-16 (wheel 12:10:50Z, sdist 12:10:52Z).
- The version and the month are right. The year is wrong by two years: the release is from February 2022, not 2024.
- "Newest" holds as of today's fetch (2026-10-26).

**8. Notice of Oct 14, 2026 schedules gpt-4o-2024-08-06 and gpt-4.1-2025-04-14 for removal on Jan 14, 2027: TRUE** [SUPPORTED | 9/10 | Primary] (Tier 1)
- https://developers.openai.com/api/docs/deprecations, entry dated 2026-10-14, "GPT-4 series model deprecations": "On October 14, 2026, we notified developers using certain GPT-4 series models". It says "removal from the API on January 14, 2027".
- The rows list `gpt-4o-2024-08-06` (with `gpt-4o-2024-11-20`) and `gpt-4.1-2025-04-14`. The recommended replacement is `gpt-6-luna`.

**Corrections for the status note**
- Claim 1: Apache-2.0, not MIT.
- Claim 4: Oct 23, not Oct 13.
- Claim 5: `starlette>=0.46.0`, not `>=1.9.0`.
- Claim 7: February 2022, not 2024.

**Gaps**
- I did not check vllm's repo at the release tag; PyPI metadata alone decides claim 3.
- All "newest release" statements are snapshots from today's fetch.
- The source-class tag is Primary throughout. The reading tool is a summariser, which is why the confidence scores stop at 9.

Sources:
- [PyPI anthropic 2.3.0](https://pypi.org/pypi/anthropic/2.3.0/json)
- [PyPI anthropic (newest)](https://pypi.org/pypi/anthropic/json)
- [anthropic-sdk-python v2.3.0 LICENSE](https://raw.githubusercontent.com/anthropics/anthropic-sdk-python/v2.3.0/LICENSE)
- [anthropic-sdk-python v2.3.0 pyproject.toml](https://raw.githubusercontent.com/anthropics/anthropic-sdk-python/v2.3.0/pyproject.toml)
- [PyPI openai 3.37.0](https://pypi.org/pypi/openai/3.37.0/json)
- [PyPI vllm 0.32.0](https://pypi.org/pypi/vllm/0.32.0/json)
- [PyPI fastapi 0.162.0](https://pypi.org/pypi/fastapi/0.162.0/json)
- [fastapi 0.162.0 pyproject.toml](https://raw.githubusercontent.com/fastapi/fastapi/0.162.0/pyproject.toml)
- [PyPI rank-bm25](https://pypi.org/pypi/rank-bm25/json)
- [OpenAI API deprecations](https://developers.openai.com/api/docs/deprecations)

*AI-generated council analysis — information, not professional advice.*
