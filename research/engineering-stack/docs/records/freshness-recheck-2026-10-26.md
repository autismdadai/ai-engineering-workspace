# Freshness re-check, October 26, 2026 (P-03, first part)

The owner approved re-checking the ledger's package versions with the existing script, plus its one overdue dated row (Oct 26, Claude chat). This record reports what changed. **The ledger, the claim ledger and the parts are not edited yet**; the ledger's own rule says to update a row here first and then every row and part it lists, and the owner decides that next.

## Python packages: Section 2 of `../engineering-stack-freshness-ledger.md`

`research/engineering-stack/research/part-11/tools/pypi_fresh.py` ran on all 40 packages in Section 2's table, from this PC (Python 3.13.16, Windows), reading only PyPI's public JSON API. Raw output: `pypi-2026-10-26.txt`. No lookup failed [T].

**19 of 40 differ from the ledger; 21 are unchanged** [T]:

| Package | Ledger (released) | PyPI on Oct 26 | Released |
|---|---|---|---|
| anthropic | 1.14.0 (2026-10-14) | **2.3.0**, a new major version | 2026-10-23 |
| openai | 3.29.0 (2026-10-11) | 3.37.0 | 2026-10-22 |
| vllm | 0.31.0 (2026-10-05) | 0.32.0 | 2026-10-18 |
| fastapi | 0.156.1 (2026-10-20) | 0.162.0 | 2026-10-23 |
| agent-framework | 1.21.0 (2026-10-08) | 1.23.0 | 2026-10-22 |
| openai-agents | 0.23.1 (2026-10-02) | 0.24.0 | 2026-10-15 |
| qdrant-client | 1.19.1 (2026-09-16) | 1.20.0 | 2026-10-22 |
| pinecone | 10.0.0 (2026-09-03) | 10.2.0 | 2026-10-23 |
| sentence-transformers | 6.1.0 (2026-09-18) | 6.2.0 | 2026-10-21 |
| sse-starlette | 3.5.0 (2026-09-28) | 3.6.0 | 2026-10-25 |
| deepeval | 4.2.8 (2026-10-02) | 4.3.1 | 2026-10-16 |
| arize-phoenix | 20.23.0 (2026-10-20) | 20.26.1 | 2026-10-25 |
| langgraph | 1.2.14 (2026-10-06) | 1.2.17 | 2026-10-24 |
| langchain | 1.4.5 (2026-10-12) | 1.4.7 | 2026-10-21 |
| crewai | 1.15.27 (2026-10-09) | 1.15.30 | 2026-10-24 |
| dspy | 3.4.0 (2026-09-25) | 3.4.1 | 2026-10-12 |
| garak | 0.17.0 (2026-09-09) | 0.17.1 | 2026-10-16 |
| presidio-analyzer | 2.2.364 (2026-07-22) | 2.2.365 | 2026-10-25 |
| transformers | 5.20.0 (2026-10-15) | 5.20.2 | 2026-10-19 |

Some differences may already be noted in later sections: for example, the October 20 Windows run installed transformers 5.20.2 (`engineering-stack-windows-run-2026-10-20.md`). This table compares only against Section 2.

## The overdue dated row (Section 1)

The ledger said: OpenAI gpt-4 and gpt-4-0613 listed for shutdown on October 23, 2026, replacement printed as gpt-5.6-sol; "Re-check after October 23, 2026."

On October 26, 2026, OpenAI's deprecations page (https://developers.openai.com/api/docs/deprecations, read in the browser) still lists **October 23, 2026** for `gpt-4-0613` and `gpt-4` (plus `gpt-4-0613-completions` and `gpt-4-completions`), with replacement `gpt-5.6-sol` [V]. The same date covers gpt-4-1106-preview, gpt-4-turbo and gpt-4.1-nano. The date has passed. Whether the models stopped answering wasn't tested, since that would need a paid API call [U].

## Not re-checked this time

- Section 3 (npm packages) and Section 4 (GitHub release tags): the script reads PyPI only.
- Package versions mentioned inside the later sections' text (Sections 5 to 19).
- About 140 product, model, standard and licence facts that need a web lookup each. The owner chose to leave them for a later, capped run.
- The next dated rows: one "Re-check after October 31, 2026" and one "Re-check after November 30, 2026" (ledger lines 121 and 137).

## Addendum, later on October 26, 2026: all columns, and Section 2 updated

The table above compared versions only. The owner approved the ledger update (Oct 26, Claude chat). A new read-only script, `research/engineering-stack/research/part-11/tools/ledger_compare.py`, compared all four columns of the same raw output with Section 2. Output: `ledger-compare-2026-10-26.txt` [T].

- **Also changed:** anthropic's licence metadata, MIT → Apache-2.0; vllm's Python range, `>=3.10` → `>=3.11`; sse-starlette's, `>=3.10` → `>=3.11`; dspy's, `<3.15` → `<3.16`. The same 19 packages; no others changed in any column.
- **Python 3.10** is now also excluded by vllm and sse-starlette; 3.11 to 3.13 still satisfy all 40. Run on the earlier rows, the script reproduced the ledger's earlier Python note [T].
- **Section 2 is updated:** 19 rows, its intro and its Python note, plus the run log in Section 7. Re-running the script on the edited ledger gives 0 differences in all 40 rows; the table row count stayed 266 [T].
- **Claim ledger, done:** its new Section 13 lists what the re-check changed. Two rows were re-worded (P6-05's "are current"; P10-10's vLLM 0.31.0 behaviour, now [U] for 0.32.0). Nine rows keep their October 9 evidence versions with unchanged verdicts. No row cites the anthropic or openai packages.
- **Still to do:** the parts that cite the older versions, anthropic 2.x first.

## Addendum: anthropic 2.x against the parts (October 26, 2026)

The owner asked for anthropic 2.x first. No lab code imports the package (the labs use stand-ins), so this checks only facts the parts state. Read in the built-in browser from the official repository, `anthropics/anthropic-sdk-python` on GitHub, at tag v2.3.0 unless noted [V]:

| Fact the parts use | Where | At v2.3.0 |
|---|---|---|
| 600 s timeout, 5 s connect, `DEFAULT_MAX_RETRIES = 2`, 0.5 to 8 s, `httpx2` | Parts 09, 13 | unchanged (`_constants.py`) |
| Jitter `1 - 0.25 * random()` under a "plus-or-minus half a second" comment; retries 408, 409, 429, 5xx; `retry-after-ms` before `retry-after`; "Streaming is required for operations that may take longer than 10 minutes" | Parts 09, 13 | unchanged (`_base_client.py`) |
| `_idempotency_header = None` | Part 09 | unchanged; `_client.py` doesn't override it |
| Usage fields `input_tokens`, `output_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens` | Part 13 | present (`types/usage.py`) |
| `client.messages.count_tokens` | Part 04 | present, on `/v1/messages/count_tokens` (`resources/messages/messages.py`) |
| Licence | Part 04 | LICENSE is MIT at v1.14.0, Apache 2.0 at v2.0.0 and v2.3.0 |

- **What 2.0.0 broke:** its GitHub release notes list one breaking change, support for the new API version 2026-10-21 (`ANTHROPIC_API_VERSION` in `_constants.py`). No part quotes the API version header. `CHANGELOG.md` at v2.3.0 stops at 1.12.0, so it doesn't cover 2.x.
- **Edited (one line each, on scratch copies, then diffed):** Part 04's tools-table row (licence, version, the 2.0.0 note); the ANS source rows of Parts 09 and 13 ("re-checked at v2.3.0: unchanged"); the ledger's anthropic row (note, and "Used in" now 03, 04, 09, 13). Table and line counts unchanged; the ledger still shows 0 differences from PyPI [T].
- **Still to do:** the other 18 packages in the parts, openai next (Parts 09 and 13 cite openai 3.31.0 and 3.35.1).

## Addendum: openai 3.37.0 against the parts (October 26, 2026)

Read the same way, from `openai/openai-python` on GitHub at tag v3.37.0 [V]. "OAS" in Part 13 is this SDK; in Parts 07 to 09 it is the separate openai-agents package, which is not checked here.

| Fact the parts use | Where | At v3.37.0 |
|---|---|---|
| 600 s timeout, 5 s connect, `DEFAULT_MAX_RETRIES = 2`, 0.5 to 8 s, `httpx2` | Parts 09, 13 | unchanged (`_constants.py`) |
| Retries 408, 409, 429, 5xx; jitter `1 - 0.25 * random()`; `retry-after-ms` before `retry-after` | Parts 09, 13 | unchanged (`_base_client.py`) |
| `_idempotency_header = None` | Part 09 | unchanged; `_client.py` doesn't override it |
| Responses stream events `response.completed`, `response.failed`, `response.incomplete`, `error` | Part 13 | unchanged (each event type's `Literal`) |
| `stream_options.include_usage` and "If the stream is interrupted, you may not receive the final usage chunk" | Part 13 | unchanged (`chat_completion_stream_options_param.py`) |
| "Connect to a persistent Responses API WebSocket", with `response.create` and `response.steer` | Part 13 | unchanged (`resources/responses/responses.py`) |
| Organization usage and costs endpoints (admin key) | Part 13 | present (`client.admin.organization.usage`, `api.md`) |
| Token counting | Part 04 | `client.beta.responses.input_tokens.count`, beta in 3.35.1 too (`api.md` at both tags) |
| `ResponseFunctionToolCall`, `ResponseOutputMessage`, `ResponseOutputText` | Part 08 lab `crosscheck.py` | present (`types/responses/__init__.py`) |

- **New, not cited by any part:** `MAX_RETRY_AFTER_DELAY = 2 * 60`; the SDK obeys a server's wait only up to 120 seconds. Part 13's 60-second cap is the lab's own rule.
- **Loose end:** Part 13's OAS row lists "padding" among its uses, but no sentence in Part 13 mentions padding. Left as is.
- **Edited (one line each, on scratch copies, then diffed):** Part 04's tools row (version, the beta token counter); the OAI source row of Part 09 and the OAS row of Part 13 ("re-checked at v3.37.0: unchanged"); the ledger's openai row (note, and "Used in" now 03, 04, 09, 13). Table and line counts unchanged; the ledger still shows 0 differences from PyPI [T].
- **Still to do:** the other 17 packages in the parts.

## Addendum: openai-agents 0.24.0 against the parts (October 26, 2026)

Read the same way, from `openai/openai-agents-python` on GitHub at tag v0.24.0 [V]. Part 09 already cites 0.24.0, so this covers Parts 07 and 08.

| Fact the parts use | Where | At v0.24.0 |
|---|---|---|
| `DEFAULT_MAX_TURNS = 10` | Part 08 | unchanged (`src/agents/run_config.py`) |
| A turn is "one AI invocation (including any tool calls that might occur)" | Part 08 | unchanged (`src/agents/run.py`) |
| `MaxTurnsExceeded`, unless an `error_handlers` entry handles it | Part 08 | unchanged (`exceptions.py`; `docs/running_agents.md`, key `"max_turns"`) |
| "An error occurred while running the tool. Please try again.", "without exposing the exception to the model" | Part 08 | unchanged (`src/agents/tool.py`) |
| `needs_approval` can "pause agent execution until a person approves or rejects sensitive tool calls" | Part 08 | unchanged (`docs/human_in_the_loop.md`) |
| stdio, Streamable HTTP, SSE and hosted MCP servers; `mcp` from 1.19 up to (not including) 3 | Part 07 | unchanged (`docs/mcp.md`; `pyproject.toml`: `mcp>=1.19.0, <3`) |

- **Fits openai 3.37.0:** `pyproject.toml` requires `openai>=3.0.0,<4`.
- **Lab pin kept:** Part 08's `requirements-crosscheck.txt` pins `openai-agents==0.23.1`. A pinned version keeps the optional cross-check repeatable; moving it to 0.24.0 would need an install and a re-run, which the owner decides.
- **Edited (one line each, on scratch copies, then diffed):** the OAS source rows of Parts 07 and 08 ("re-checked at v0.24.0: unchanged"); the ledger's openai-agents row (note, "Used in" now 07, 08, 09). Table and line counts unchanged; the ledger still shows 0 differences from PyPI [T].
- **Still to do:** the other 16 packages in the parts.

## Addendum: the other 16 packages in the parts (October 26, 2026)

**Rule used.** Tools-table rows take the new version and the PyPI facts (licence, Python range) from `pypi-2026-10-26.txt` [T]; the row's other cells keep the version they were checked at, marked "the rest of this row was checked at X". Prose such as "vLLM 0.31.0 recomputes" stays as a dated record. Facts were re-read from official code only where a part's wording depends on the version and carries weight [V].

| Package | Parts | What changed in the parts |
|---|---|---|
| vllm 0.32.0 | 04, 11 | Part 04 row: version, Python 3.11 to below 3.15. Part 11 row and VSR source: re-checked at v0.32.0, preemption still recomputes (default policy: the request scheduled last; `PREEMPTED`, `num_computed_tokens = 0`, no swap path), usage statistics still on, every 600 s to `https://stats.vllm.ai` |
| dspy 3.4.1 | 03 | Row: version; Python below 3.16 |
| deepeval 4.3.1, arize-phoenix 20.26.1 | 02, 13 | Rows: version only |
| sentence-transformers 6.2.0, pinecone 10.2.0 | 05 | Rows: version only |
| langgraph 1.2.17, agent-framework 1.23.0, crewai 1.15.30 | 09 | Tools rows: version only; Part 09's prose already cited 1.2.15, 1.22.0 and 1.15.28 |
| presidio-analyzer 2.2.365, garak 0.17.1 | 10 | Rows: version only; the lab's cross-check ran on 2.2.364 and stays so |
| fastapi 0.162.0 | 13 | Row: version, and a **correction**: FastAPI 0.156.1 and 0.162.0 both declare `starlette>=0.46.0` (`pyproject.toml`); "needs Starlette 1.9.0" was wrong, since it is Starlette 1.9.0 that needs Python 3.11. FAS source: ping still 15 s (`_PING_INTERVAL: float = 15.0` in `sse.py`) |
| sse-starlette 3.6.0 | 13 | Row: version, Python 3.11 or later; ping still 15 s (`DEFAULT_PING_INTERVAL = 15`) |
| transformers 5.20.2 | 12 | Already current; no change |
| langchain 1.4.7, qdrant-client 1.20.0 | none | No part gives these packages a version |

- **Claim ledger:** P10-10's [U] is settled; vLLM 0.32.0 still recomputes only [V].
- **Ledger notes:** vllm (now "Used in" 04, 11), fastapi (the correction) and sse-starlette record these checks.
- **Checks [T]:** ten files edited on scratch copies; each changed exactly the lines intended, with row and line counts unchanged; all 13 versions and dates typed match the PyPI output; the ledger shows 0 differences from PyPI.
- **Not covered:** the overview (`engineering-stack-overview.md`) still lists older versions and the old Starlette wording in its tools table; the other cells of the version-only rows (telemetry switches, default models and so on) were not re-read at the new versions.

## Addendum: the overview's tools table (October 26, 2026, later)

- **Edited (owner approved), on a scratch copy, then diffed:** Appendix C, 16 rows. The 15 changed packages it lists get their new version marked "(Oct 26)": DeepEval, anthropic (with the licence, Apache-2.0, MIT up to 1.14.0), openai, DSPy, sentence-transformers, Pinecone's SDK, LangGraph, Agent Framework, CrewAI, Presidio, garak, vLLM, FastAPI, sse-starlette and Phoenix. The OpenAI Agents SDK row now gives 0.24.0, still the newest. FastAPI's "Needs" cell is corrected to `starlette>=0.46.0`. The intro says what "(Oct 26)" means.
- **Also corrected:** the "Every lab" note said "optional cross-checks pin their packages with hashes". The labs' requirements files show that only Parts 01 to 04 pin hashes (and not Part 03's DSPy file); Parts 05 to 10 and 13 pin versions only [T].
- **Checks [T]:** all 16 versions match `pypi-2026-10-26.txt`; 520 lines and 289 table rows before and after; the diff is 18 lines in and 18 out.
- **Found, not fixed:** Part 03's tools row for anthropic and openai still reads "MIT; Apache-2.0 ... 1.13.0, October 9; 3.29.0, October 11". The anthropic and openai addenda edited Part 04's row and missed this one.

## Addendum: Part 03's anthropic and openai row (October 26, 2026, later)

- **Fixed (owner approved), on a scratch copy, then diffed:** Part 03's tools row now gives anthropic 2.3.0 and openai 3.37.0 [T: PyPI], with anthropic's licence as Apache-2.0 (MIT up to 1.14.0) and the rest of the row noted as checked at 1.13.0 and 3.29.0.
- **Source row OSDK:** Part 03 cites openai-python 3.29.0's `src/openai/lib/_pydantic.py` for "the SDK rewrites schemas into strict form". Read at tags v3.29.0 and v3.37.0 on raw.githubusercontent.com, the file is the same at both: 5,623 characters, the same SHA-256 of the page text, and the same `to_strict_json_schema` lines [V]. The row now says so.
- **Header tag count:** recounted with the header's own method, which reproduces the original 172, 56, 7, 5, 6 at `b24f88c`. It was already stale (an October 22 edit added a [V], the package re-check two [T]). Now 174 [V], 59 [T], 7 [R], 5 [U], 6 [I].
- **Checks [T]:** 1,497 lines and 139 table rows before and after; the diff is 3 lines in and 3 out.

## Addendum: the dated gpt-4 row (October 26, 2026, later)

- **Read [V]:** OpenAI's deprecations page (https://developers.openai.com/api/docs/deprecations) in the built-in browser. Under "2026-04-22: Legacy GPT model snapshots" it now says access to those models "was shut down on October 23, 2026". It lists `gpt-4-0613` (aliases `gpt-4`, `gpt-4-0613-completions`, `gpt-4-completions`) with substitute gpt-5.6-sol, and `ft-gpt-4` and `ft-gpt-3.5-turbo` among the fine-tuned models shut down the same day.
- **Edited (owner approved), on scratch copies, then diffed:** the freshness ledger's Section 1 gpt-4 row ("Re-check after October 23" replaced by the result; no further re-check needed); the claim ledger (P9-12 marked "(October 26, §14)", a new Section 14); Part 02 (the P9-12 row, "Not for new work", the cheat sheet, source ODP); Part 12 (the `ft-` sentence and its P9-12 row); and the overview's "What goes stale fastest" line. Each now says "were shut down" or "were removed" where it said "are scheduled" or "are removed".
- **Left as dated text:** the claim ledger's October 9 summaries (its opening note, Section 7 and Section 8), `project-file-map.md` ("retired or superseded on October 9"), and the research notes.
- **Checks [T]:** Parts 02 and 12 and the freshness ledger and overview keep their line and table-row counts; the claim ledger gains 10 lines and 3 table rows (Section 14). The tag counts of Parts 02 and 12 are unchanged (207, 84, 7, 8, 7 and 182, 76, 10, 23, 20), because the edits extend existing tags.
- **New on the same page, not followed up:** a notice dated October 14, 2026 schedules GPT-4o, GPT-4o mini, GPT-4.1 and GPT-4.1 mini for removal on January 14, 2027 [V]. Parts 03, 04, 05, 06 and 08 name some of these models (27 mentions [T: grep]); those mentions weren't re-checked.

## Addendum: GPT-4o and GPT-4.1, removal on January 14, 2027 (October 26, 2026, later)

- **New freshness-ledger row (owner approved):** Section 1, right after the gpt-4 row. It records the October 14 notice [V: ODP, read October 26]: `gpt-4o-2024-08-06`, `gpt-4o-2024-11-20`, `gpt-4o-mini-2024-07-18`, `gpt-4.1-2025-04-14` and `gpt-4.1-mini-2025-04-14` are removed on January 14, 2027, each with "gpt-6-luna" as the recommended replacement, and fine-tuned versions follow their bases. **Re-check after January 14, 2027.** Checks [T]: 423 → 424 lines, 284 → 285 table rows, 5 cells like its neighbours, 6 → 7 "Re-check after" mentions.
- **Map of every mention in the parts** (27 lines [T: grep for gpt-4o, gpt-4.1, GPT-4o, GPT-4.1]). "Depends" means the text stops being usable or accurate once the models are gone:

| Part | Lines | How the models appear | Depends? |
|---|---|---|---|
| 03 | 242 | DSPy's RAG tutorial: a MIPROv2 run "around $1.5" with gpt-4o-mini [V: DSD] | Yes, lightly: the example model goes, and the cost stays a dated figure |
| 03 | 240, 586, 604 | GEPA paper's results on GPT-4.1 Mini [V: GEP] | No: study results |
| 04 | 172, 179, 644 | OpenAI's GPT-4.1 prompting guide (source OG41): instructions at both ends of a long context; recall degrades with many items | Yes: guidance written for a model being removed. Re-check that the guide is still published (179 already marks newer guides [U]) |
| 04 | 70, 1421 | tiktoken 0.14.0's model table maps gpt-4.1 and gpt-4o to `o200k_base` | No: it describes tiktoken 0.14.0 |
| 04 | 169, 291, 304, 641, 1359, 1404 | Models tested in NoLiMa, Chroma's needle test, a caching study and a cache-sharing audit; the lab listing reproduces the NoLiMa figure | No: study results |
| 05 | 258 | GPT-4o in a 2024 long-context study [V: LIL] | No |
| 06 | 288, 616 | `graphrag init` defaults to OpenAI `gpt-4.1` (tools row; cheat sheet) [V: MGR] | Yes: unless GraphRAG changes its default, a new project would point at a removed model. GraphRAG is "largely in maintenance mode" |
| 06 | 88, 158, 159, 230, 452, 514, 516, 604 | Models in cited studies (Han et al., Xiang et al., Mem0's paper) and the review notes | No |
| 08 | 169 | τ-bench's result with gpt-4o [V: TAR] | No |

- **Outside the parts:** the freshness ledger's GraphRAG row (Section 12) also gives the `gpt-4.1` default (depends); its Structured Outputs row says "starting with GPT-4o" (no: it names where support began). The overview's key-figures row 2 (the NoLiMa figure) and the claim ledger's three mentions are all study results (no).
- **Not changed:** the parts themselves. The row's re-check date brings the three "Yes" places back up after January 14, 2027.
