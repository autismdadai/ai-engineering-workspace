# Engineering Stack Part 13: Phase 4 Review

*October 20, 2026. The Phase 4 record for claude/engineering-stack-part-13-shipping.md, in the finding format of claude/fabel-prompt-audit.md (number, severity, quote, what goes wrong, why with source, fix). Every finding below was reproduced by the lead session before it was fixed: the security reviewer's scripts were rerun against the lab on 127.0.0.1, source files were reopened at the pinned commits (FastAPI f6ce798, Kubernetes website 6df0b1b, RouteLLM README, Phoenix 57b8303, Langfuse 6343bd8, vLLM 7b569ec, the logfire 5.2.0 wheel, opentelemetry-python-contrib's GenAI README), and every lab output was rerun. Raw checker notes are in engineering-stack-research-part-13.zip, sent to the owner.*

## Who checked what

| Check | By | Result |
|---|---|---|
| Blind source check A | Fresh agent; only claims and sources (Sections 1 to 3.6) | 77 claims: 64 supported, 12 partly, 0 contradicted, 1 not checkable; 34 lookups |
| Blind source check B | Same rules (Section 3.7 onward) | 81 claims: 50 supported, 22 partly, 3 contradicted, 6 not checkable; 25 lookups |
| Beginner test | Fresh agent, Sections 6 to 9 literally, as a new Linux user, fresh environments on Python 3.13.16, 3.12.3, 3.11.17 | 0 high, 4 medium, 12 low; every printed number matched |
| Security review | Fresh agent, defence only: the lab's code tested on loopback addresses only, and the paper's security and privacy advice read against its sources | 21 findings: 2 high and 5 medium in the advice, 5 medium in the code, 8 low, 1 note; every code finding reproduced |

## Findings

### F-01 · High · A public streaming endpoint needs more than the draft listed (security P1)
- **The draft said:** Section 3.5, "An API that calls a paid model needs its own: per-key request and token limits, a request-size limit, and a spending alarm."
- **What goes wrong:** a streaming request lasts seconds to minutes, so one key can hold dozens of open streams inside any per-minute limit; there were no timeouts, no stream-length limit, no hard spend cap and no warning that turning off proxy buffering removes the proxy's shield against slow readers. The lab's server, offered as the example, held a thread per stalled client with no limit.
- **Why:** reproduced with the reviewer's scripts: three stalled clients raised the server's threads from 3 to 7 and kept them.
- **Fix:** a "What a public endpoint needs" checklist in Section 3.1 (authenticate, cap open streams per key and IP, cap input and `max_tokens` on the server, time out headers, bodies and idle streams, a longest stream length, a daily spend cap per key before the model call, rate-limited failed attempts), with the buffering trade-off scoped to the streaming route [U: not run against nginx]; Section 5 step 1 updated; cheat-sheet rule 9; the lab labelled as a teaching server in Sections 3.1, 7.6 and 10 and in its README.

### F-02 · High · No browser or CORS guidance (security P2)
- **The draft said:** Section 3.2 introduced `EventSource` and said nothing about keys or origins.
- **What goes wrong:** `EventSource` can't send an `Authorization` header, so people put keys in URLs, which reach logs and traces; nothing said to keep the vendor key server-side or how to allow origins.
- **Why:** reproduced: FastAPI 0.156.1's own spans recorded `url.query = api_key=...`; WHATWG 9.2 for what `EventSource` can send.
- **Fix:** a "From a browser" paragraph in Section 3.2: vendor key on the server, a same-site `HttpOnly` cookie plus an `Origin` check or `fetch()` streaming, never keys in URLs, an explicit `allow_origins` list and never `*` with credentials.

### F-03 · High · The worked example's daily average was wrong (checker B, B50)
- **The draft said:** Section 5 step 2, "10,000 / 86,400 = 0.93 a second, about 7 streams".
- **What goes wrong:** 10,000 / 86,400 is 0.116 a second; at 8 seconds each that holds about 0.93 streams, not 7.
- **Why:** recomputed with `shipmath.concurrent(Fraction(10000, 86400), 8)`.
- **Fix:** "0.116 a second, which holds about 0.93 streams open, around one", and size for the peak of 40.

### F-04 · Medium · Lab code: unchecked fields, no timeouts or caps, unbounded spans (security C1, C2, C3, C8, C12)
- **The draft's code:** `stream_server.py` read `max_tokens` and `fail_after` without checks, had no socket timeout, no thread cap, a backlog of 5, a list of spans that grew forever, accepted an empty `LAB_API_KEY`, matched only `Bearer` in one case, allowed `::1` past the guard and promised a log line that didn't exist.
- **What goes wrong:** `max_tokens: 1e400` gave an `OverflowError` and an empty reply; `fail_after: "x"` gave a 200 and then nothing; client text reached stderr in a traceback; an empty key accepted `Bearer `.
- **Why:** each reproduced with the reviewer's scripts before the change.
- **Fix:** fields checked as whole numbers (not true or false) before the 200, else 400; any crash sends a short `server_error` event and records only the exception's type; 30-second socket timeouts; 32 clients at once, then 503; a queue of 64; spans kept in a `deque` of 10,000; an empty key refused at start; the scheme matched in any case; `::1` removed; the docstring fixed. Checks c18 and c20 and 8 new mutations cover them.

### F-05 · Medium · The proxy trusted `Content-Length` and the upstream (security C4)
- **What goes wrong:** a non-numeric length crashed the handler, a negative one hung, no size limit (8 MiB held in memory), and a dead upstream gave an empty reply instead of 502.
- **Why:** reproduced with the reviewer's proxy script.
- **Fix:** the length must be 1 to 9 digits (else 400), missing gives 411, over 64 KB gives 413, the path must start with `/`, `Host` is fixed to 127.0.0.1, an upstream failure gives 502, and a 30-second socket timeout. Check c21 and 3 new mutations.

### F-06 · Medium · Parser and client failed open (security C5, C11)
- **What goes wrong:** invalid UTF-8 raised `UnicodeDecodeError` (the spec says replace with U+FFFD); a CR, then an empty read, then LF split one event in two; no limit on line length; the client had no total deadline, crashed on non-JSON data and printed a stream with no `done` as if complete.
- **Why:** each reproduced before the change.
- **Fix:** an incremental UTF-8 decoder with `errors="replace"`, a pending CR kept across empty reads, a 1 MiB line limit, line splitting in one regular-expression pass; the client gets a total deadline, reports bad data as an error and its command line exits non-zero without `done`. Check c19 and 4 new mutations.

### F-07 · Medium · The Collector safety net covered two of the places content leaks (security P3)
- **The draft said:** Section 5 step 4, a Collector "deletes `gen_ai.input.messages` and `gen_ai.output.messages` in case anyone turns it on".
- **What goes wrong:** the lab's own `CONTENT_ATTRIBUTES` lists four; content also reaches storage through span events, the logs pipeline, `url.query` and exception messages.
- **Why:** `shipmath.CONTENT_ATTRIBUTES`; the `url.query` run in F-02; Section 3.7's own note that openai-v2 records content as events.
- **Fix:** step 4 and rule 5 now cover all four attributes, `url.query`, content events and logs, exceptions by type, and a staging test with capture turned on.

### F-08 · Medium · A client's `traceparent` was trusted at the edge (security P4)
- **What goes wrong:** any caller picks its trace IDs, and with ratio sampling a parent-based sampler follows the caller's flag.
- **Why:** reproduced: SDK 1.45.1, `ParentBased(TraceIdRatioBased(0.01))`: flag `01` kept 1,000 of 1,000, flag `00` kept 0, no header kept 7.
- **Fix:** Section 3.6: strip it at the gateway or set remote-parent samplers, `baggage` too; Section 3.7 says the lab joins because it plays an internal service; rule 9.

### F-09 · Medium · Retries and reconnects multiply cost (security P5, C10)
- **What goes wrong:** layered retries (your loop of 3 around an SDK that tries 3 times) make 9 paid calls per user request; retrying a stream after the first token pays again; `EventSource` reconnects by itself; `retry_plan` obeyed a `retry-after` of 86,400 seconds or `-5`.
- **Why:** C10 reproduced; the SDK figure is the SDKs' `max_retries=2`; WHATWG 9.2 for reconnection and HTTP 204.
- **Fix:** a "Don't multiply retries" paragraph in Section 3.5; `retry_plan` obeys up to 60 seconds, gives up beyond, and ignores a value that isn't a plain number (check c13 and 1 new mutation); rule 4.

### F-10 · Medium · A stream that just stops looked like success (security P6)
- **Fix:** Section 3.4, rule 3, the self-check and the misconception now say a stream is done only at its last event (`message_stop`, `response.completed`, the lab's `done`); Section 3.4 adds that error events carry a code and a plain message, never internals.

### F-11 · Medium · Telemetry and exposure gaps (security P7, P8)
- **The draft said:** Logfire "Scrubs common secrets by default" in the content column; nothing on vLLM's usage statistics, Helicone seeing the vendor key, self-hosted UI exposure, or OTLP over the network.
- **Why:** reopened: logfire 5.2.0 `instrument_openai` defaults to `version=2` and `openai.py` lines 150 to 155 record `gen_ai.input.messages`; vLLM `envs.py` lines 831 to 835 (`VLLM_NO_USAGE_STATS`, `DO_NOT_TRACK`); Phoenix `config.py` `HOST = "0.0.0.0"` and `PHOENIX_ENABLE_AUTH` default false; Langfuse `docker-compose.yml` with `# CHANGEME` defaults and port 3000 on every address.
- **Fix:** the Logfire cell and the "defaults disagree" sentence now list Logfire as recording content; vLLM in Sections 3.1, 3.8 and 6; Helicone's row says it sees the key; a self-hosting pick with the Phoenix and Langfuse defaults; an OTLP-over-the-network paragraph in Section 3.6.

### F-12 · Medium · Version and source wording (checkers)
- A36/B40: FastAPI's native OpenTelemetry is from 0.142.0 (September 29, 2026); 0.143.0 made exporter setup opt-in. Fixed in Sections 3.1 and 4.
- B68: only some Gemini prices double on January 1, 2027 (another model changes on December 1, 2026). Exercise 1 now names its model and says others change on their own dates.
- B26/B67: whole-request repricing is stated by OpenAI and, for Haiku 5.5, by Anthropic; Anthropic's other models have no surcharge; Google's page doesn't say. Sections 2, 3.9, 9 and the cheat sheet now say so, with Gemini marked [U].
- B38/B64: the WHATWG buffering warning is about the receiving side, not proxies. Section 3.3 item 4, Section 4 and the misconception reworded.

### F-13 · Medium · Beginner steps (tester 1 to 4)
- Section 7.5 told readers to activate before going to the folder; now folder first. macOS had no unzip step; now the same `python3 -m zipfile` command. pip's cache stayed behind; Section 7.8 adds `python -m pip cache purge` [T]. The Windows port-in-use row may not appear, because Python's server asks for address reuse; now marked [U].

### F-14 · Low · Smaller source mismatches (checkers)
- A6: "must not" became the convention's "SHOULD NOT". A71: the sampled bit says the caller "may have recorded" the trace. A66: a 429 "usually" carries `retry-after`. A47: the openai SDK "has" a WebSocket mode, with `response.steer` under beta. A40: Kubernetes' "no single definition" is about hard and soft isolation, and sandboxing "is often recommended". A27, B30, B43, B76: RouteLLM's savings were measured with GPT-4 and Mixtral 8x7B; the "2023 to 2024" scope was this part's own reading, now "GPT-4-era" with [U] for today's pairs. A2, A46: Gemini streams SSE with `alt=sse`. A8: OAD dropped as a source for the two-number latency framing. A33: FastAPI's docs say set `response_class=EventSourceResponse` and yield. A53: sse-starlette sends `no-store`, FastAPI `no-cache`. B8: a JSON string is the fallback where structured attributes aren't supported. B18: Weave sends error reports, not usage. B20, B44: Phoenix can evaluate production traces; continuous monitoring with alerts goes to Arize AX, which has a free tier. B24: twice the standard rate is stated for GPT-5.6 Sol. B53: alerting "not on means" is this part's advice, now [I]. B37: the early-end share is marked as this part's suggestion. A14, B35: the Little's law paper couldn't be opened by either checker; its grade dropped from 8 to 6.

### F-15 · Low · Polish (tester 5 to 16, security C9, P9 and small points)
- The stand-in's answer is the same for any prompt (7.5); "in your own code" works from the lab folder (7.6); pip may list setuptools on 3.11 and print a notice (7.4); sample cross-check output added (7.4); step 2 names `last_event_id`; timings vary (7.1, 8); Section 9 needs the environment active; the BATCH comment pointed to Section 3.7, now 3.9 in the code and appendix; the Haiku batch price shows $0.000225; step 1 names `feed`, `_lines` and `_line`; the fallback `venv` command; the Windows Extract All destination.
- C9, P9: the cross-check's blocker now also wraps `connect_ex`, UDP `sendto` and `getaddrinfo` and counts any loopback address as local; reproduced blocked for all three before rewording Section 7.4, which now calls it a check on these libraries, not a sandbox.
- Requirements are pinned without hashes; Section 7.4 says so.
- A literal byte-order mark in `run_lab.py` was replaced by its escape, as was done in `ssewire.py`.

## Not acted on, with reasons

- **C7, the stand-in's prefill time grows with prompt length** (one 60 KB prompt held a thread for 30 seconds). The timing is invented for teaching; the 64 KB limit, the 32-client cap and the socket timeouts bound it.
- **B15, content defaults for eight tools** were read by a researcher, not by the blind checkers; the Logfire cell was reopened and corrected, and the rest stand at the versions named.
- **A29, the ledger half of P11-06**, and the claims that point to this series' own ledger and sections, can't be checked against an outside source.
- **Not run:** nginx itself (the `send_timeout` and `limit_conn` advice is [U]); Windows and macOS for the new steps ([R]).

## After the fixes

`run_lab.py` 21 of 21 and `mutation_check.py` 48 of 48 on Python 3.13.16, 3.12.3 and 3.11.17; `crosscheck.py` 7 of 7 with 0 network attempts on all three; `run_lab.py` 21 of 21 again from a fresh unzip of the rebuilt zip on all three; the break-it step gives `20 of 21` with `AssertionError 1103/200`; `demo.py` prints every number quoted; the appendix matches `shipmath.py` byte for byte [T]. The part is about 95 KB, under the 100 KB cap, with no em or en dashes.
