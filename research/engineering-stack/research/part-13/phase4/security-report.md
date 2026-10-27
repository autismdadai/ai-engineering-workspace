# Part 13 security review: lab code and the paper's security and privacy advice

October 20, 2026. Reviewer: defensive security pass on `part13-draft.md` and `engineering-stack-lab-part-13.zip`.

**Scope and method.** The zip was unpacked into `/home/claude/part13/phase4/security/lab/`, a Python 3.13.16 virtual environment was made at `/home/claude/part13/phase4/security/venv/` with `requirements-crosscheck.txt` installed, and `run_lab.py` (17 of 17) and `crosscheck.py` (7 of 7, 0 network attempts) passed before any test. Every test ran against 127.0.0.1 or 127.0.0.2 (loopback) only, with at most 45 concurrent connections and payloads of at most 8 MiB. Test scripts are in `/home/claude/part13/phase4/security/tests/` (`t_server.py`, `t_auth.py`, `t_proxy.py`, `t_parser.py`, `t_client.py`, `t_block.py`, `t_fastapi.py`, `t_sampling.py`, `t_retry.py`); run each with `../venv/bin/python -I <script> <test>` from that folder. Line numbers refer to the files as shipped in the zip.

Every code finding below was reproduced. Paper findings that rest on behaviour I could not run here are marked "not reproduced".

## Summary

| ID | Severity | Where | One line |
|---|---|---|---|
| P1 | High | Sections 3.1, 3.5, 5, cheat sheet | A public streaming endpoint needs more than the paper lists: timeouts, per-key stream caps, a stream time limit, hard budget caps; and the lab server is not labelled as unsafe to copy |
| P2 | High | Sections 3.2, 3.5, 6 | No CORS or browser-client guidance; `EventSource` cannot send headers, so keys end up in URLs, and FastAPI's own spans record the query string (shown) |
| P3 | Medium | Section 3.7, 5 step 4, cheat sheet rule 5 | The Collector safety net deletes two attributes; content and secrets also reach traces through events, logs, `url.query` and exception text |
| P4 | Medium | Sections 3.6, 3.7, 5 | Trusting a client's `traceparent` lets any caller force 100% sampling and choose trace IDs (shown: 1,000 of 1,000 kept at a 1% ratio) |
| P5 | Medium | Sections 3.4, 3.5, 5 step 5, cheat sheet rule 4 | Retries can multiply cost: layered retries give 9 model calls per request; `EventSource` reconnects re-run generation; `retry-after` is obeyed without a cap |
| P6 | Medium | Section 3.4, cheat sheet rule 3 | A stream that just stops (no `error`, no terminal event) looks like success; the lab's own server does this (shown) |
| P7 | Medium | Sections 3.1, 3.8, 6 | Telemetry and exposure gaps: vLLM usage statistics (on by default per the paper's own source) never mentioned; the Logfire content cell answers a different question; self-hosted UIs recommended without auth or bind-address advice |
| P8 | Low | Sections 3.6, 6 | Nothing on TLS and credentials for OTLP export to a remote Collector |
| P9 | Low | Section 7.4 | "blocks and counts any connection that tries to leave your computer" overstates the network blocker |
| C1 | Medium | `stream_server.py` 144 to 151; `buffer_proxy.py` 124 to 128 | No socket timeouts and no thread cap: slow or stalled clients hold a thread each, forever |
| C2 | Medium | `stream_server.py` 91, 117 | Unvalidated `fail_after` and `max_tokens` raise uncaught exceptions: the stream ends with no error event, or the client gets no response at all; client input is echoed to stderr |
| C3 | Medium | `tinytrace.py` 23, 53; `stream_server.py` 54 | `Tracer.spans` grows without limit in the long-running server (about 900 bytes per span, 2 spans per request) |
| C4 | Medium | `buffer_proxy.py` 86 to 91, 92 | Proxy: negative `Content-Length` reads until EOF and hangs; non-numeric crashes the handler; no body-size limit (8 MiB buffered in memory); upstream errors give an empty reply, not 502 |
| C5 | Medium | `ssewire.py` 67 to 106; `sse_client.py` 176 | Parser raises on invalid UTF-8 (the spec says replace), buffers without limit, and is quadratic on long input; the client crashes on bad bytes or non-JSON data and has no overall deadline |
| C6 | Low | `stream_server.py` 148 | Listen backlog of 5: 3 to 5 of 45 concurrent connections were reset |
| C7 | Low | `stream_server.py` 37 to 41, 111 to 115 | Work scales with prompt size: one 60 KB request held a thread for 30 seconds |
| C8 | Low | `stream_server.py` 56, 78 to 81 | Key check is sound for a set key, but an empty `LAB_API_KEY` accepts `Bearer ` (empty key) and there is no limit on wrong attempts |
| C9 | Low | `crosscheck.py` 42 to 50 | The blocker only wraps `socket.connect`: `connect_ex` and UDP `sendto` pass, DNS lookups are not seen |
| C10 | Low | `shipmath.py` 741 to 744 (appendix) | `retry_plan` returns any `retry-after` unchanged: 86,400 s, negative, NaN or infinite waits; non-numeric raises |
| C11 | Low | `ssewire.py` 86 to 88 | A CR, then an empty `feed(b"")`, then LF is read as two line ends and splits one event in two |
| C12 | Info | `stream_server.py` 8 to 9, 146 | Docstring promises "a log line" that does not exist; `serve(host="::1")` passes the guard but fails |

**What held up (verified, no finding):** the server listens only on 127.0.0.1 (`/proc/net/tcp` shows `0100007F:1FA3` for port 8099) and refuses `0.0.0.0` and `""`; no files were written by the server, the tracer (no `path`) or `crosscheck.py`; a marker prompt sent 300 times never appeared in `tracer.spans`; the 64 KB limit returns 413 for missing, negative, zero, huge (`99999999999999999999999`) and 65,537-byte lengths before reading the body; ten clients that never read did not hold threads (the 24-word answer fits in the socket buffer); the key comparison uses `hmac.compare_digest` and runs before the body is read; the proxy forwards only `Content-Type`, `Authorization` and `traceparent`, always to 127.0.0.1 (shown below, including for an absolute-URI request line); `crosscheck.py` stays at 0 outside attempts even with `FASTAPI_OTEL_AUTO_CONFIGURE=true` and an OTLP endpoint set in the environment; FastAPI 0.156.1's spans did not record the `Authorization` header or the JSON body.

---

## Part A. The lab's code

### C1. No timeouts and no thread cap in the server and the proxy (Medium)

**Where.** `stream_server.py` lines 144 to 151 (`ThreadingHTTPServer`, no `timeout` on `Handler`), line 89 (`self.rfile.read(length)`); `buffer_proxy.py` lines 124 to 128 and 87.

**What I did.**

```
$ python -I t_server.py slowloris      # 40 clients send half a request line and stop
after 2 s: threads 42 (before 2); server still answers: True
after 10 s: threads 42 (before 2); server still answers: True
after the 40 clients closed: threads 2

$ python -I t_server.py short_body     # Content-Length: 100, only 10 bytes sent, socket left open
threads before 2 after 5 s with 5 short-body clients 7
threads after the clients closed 2

$ python -I t_proxy.py slow            # same against the buffering proxy
30 unfinished requests to the proxy: threads 3 -> 33 after 6 s
```

**Impact.** Each stalled connection pins one OS thread until the client closes it; nothing ever times it out and nothing caps the number of threads. On 127.0.0.1 this is harmless. A reader who copies `stream_server.py` (or the `ThreadingHTTPServer` pattern) behind a public address, which Section 3.5 invites by presenting the server's limits as the things "an API that calls a paid model needs", gets a server that a handful of slow clients can exhaust.

**Fix.** In `Handler`, set `timeout = 30` (BaseHTTPRequestHandler applies it to the socket, so header and body reads time out); cap threads with a `threading.BoundedSemaphore(32)` acquired in `process_request` (answer 503 when full); do the same in the proxy. In the paper, add one line under Section 3.5: "The lab's server shows the rules, not a production server: it has no timeouts or connection cap. Use uvicorn behind a proxy with header, body and idle timeouts."

### C2. Unvalidated fields crash the handler mid-stream or before the status line (Medium)

**Where.** `stream_server.py` line 91 (`int(req.get("max_tokens", ...))`, `OverflowError` is not caught by `except (ValueError, KeyError, TypeError)`), line 92 (`fail_after` taken unchecked) and line 117 (`int(fail_after)` inside the streaming loop, where only connection errors are caught).

**What I did.**

```
$ python -I t_server.py overflow       # {"prompt": "hi", "max_tokens": 1e400}
client got: b'(nothing; connection closed with no status line)'
server stderr: ['OverflowError: cannot convert float infinity to integer']

$ python -I t_server.py fail_after     # {"prompt": "hi", "max_tokens": 5, "fail_after": "x"}
client got: HTTP/1.0 200 OK ... (headers, then nothing)
has error event: False | has usage: False
server stderr: ["ValueError: invalid literal for int() with base 10: 'x'"]
spans: [('chat standin-1', 'ERROR', 'ValueError'), ('POST /v1/stream', 'ERROR', 'ValueError')]

# fail_after = "CUSTOMER-SSN-000-00-0000"; the server's stderr then contains:
ValueError: invalid literal for int() with base 10: 'CUSTOMER-SSN-000-00-0000'
```

**Impact.** The thread survives (socketserver catches the exception), so this is not a crash of the process, but: (1) a stream can end after the 200 with neither an `error` event nor `usage`/`done`, exactly the silent failure Section 3.4 teaches clients to watch for; (2) `json.loads` accepts `1e400` as infinity, a classic gap; (3) the default `handle_error` prints the traceback, including client-supplied text, to stderr, so the "never the prompt" promise holds for the `prompt` field only.

**Fix.** Validate every field before sending the 200: `fail_after` must be `None` or an `int` in 0 to `MAX_TOKENS`; reject non-`int` `max_tokens` (`isinstance(x, int) and not isinstance(x, bool)`); add `OverflowError` to the caught exceptions; wrap the streaming block in `except Exception` that sends `event: error` with a generic message and logs only `type(error).__name__`; override `handle_error` in the server to log the exception type, not its message.

### C3. The server's tracer keeps every span forever (Medium)

**Where.** `tinytrace.py` lines 23 and 53 (`self.spans.append(record)` with no bound); `stream_server.py` line 54 (one class-level `Tracer` for the life of the server).

**What I did.**

```
$ python -I t_server.py leak            # 300 requests, 30 at a time
300 requests: tracer.spans 0 -> 600; traced memory +530 KiB (about 904 bytes per span, never freed)
prompt text in spans: False
files in cwd: []
```

**Impact.** Memory grows by about 1.8 KB per request with no ceiling: around 1.8 GB per million requests. Harmless in a 30-second lab run; a slow leak in anything that copies the pattern. (The test also confirms the good news: no prompt text in spans and no files written.)

**Fix.** Keep spans in `collections.deque(maxlen=10_000)`, or hand them to an exporter and drop them, which is what the OpenTelemetry `BatchSpanProcessor` the paper recommends does.

### C4. The buffering proxy trusts `Content-Length` and the upstream (Medium)

**Where.** `buffer_proxy.py` line 86 (`int(... or 0)`, no range check), line 87 (`rfile.read(length)`), lines 88 to 92 (no error handling around the upstream call).

**What I did.**

```
$ python -I t_proxy.py cl
not a number             -> b''                       (handler crashed: ValueError ... 'abc')
negative, body then EOF  -> b'HTTP/1.0 200 OK'        (read(-1) read until the client closed, then forwarded)
Content-Length -1, socket open 4 s: threads 3 -> 4, upstream connects so far 1   (hangs until the client closes)

$ python -I t_proxy.py bigbody          # 8 MiB body
8 MiB body through proxy -> b'' | proxy peak traced memory 24.6 MiB
proxy stderr errors: ['BrokenPipeError: [Errno 32] Broken pipe', ...]

$ python -I t_proxy.py updown           # upstream stopped
upstream down -> b'(empty: no 502, connection closed)'
proxy stderr errors: ['ConnectionRefusedError: [Errno 111] Connection refused', ...]
```

Header forwarding, for the record:

```
$ python -I t_proxy.py headers          # request line "POST http://attacker.example/v1/stream", plus Cookie and X-Forwarded-For
client status: b'HTTP/1.0 404 Not Found'
upstream saw path: http://attacker.example/v1/stream
upstream saw headers: {'Host': 'attacker.example', ..., 'Authorization': 'Bearer k', 'traceparent': '00-4bf9...-01'}
all outbound connects: [('127.0.0.1', 33071), ('127.0.0.1', 46293)]
```

**Impact.** The upstream's 64 KB limit does not protect the proxy: it reads the whole body into memory first (8 MiB in, 24.6 MiB peak), then the client gets an empty reply instead of the upstream's 413. A negative length turns into "read until EOF". Any upstream failure is an empty reply rather than 502. On headers, the proxy is sound: `Authorization` goes only to the fixed 127.0.0.1 upstream, `Cookie` and `X-Forwarded-For` are dropped, and an absolute-URI request line does not change the destination; it only makes `http.client` set the upstream `Host` header to the client's chosen host, which matters if a real upstream routes on `Host`.

**Fix.** Parse `Content-Length` with `fullmatch(r"\d{1,9}")`, reject a missing or over-limit length with 411 or 413 before reading; wrap the upstream call in `try/except OSError` and answer 502; pass a fixed `Host` header (`headers["Host"] = "127.0.0.1"`) and reject request lines that are not origin-form (`self.path.startswith("/")`).

### C5. The SSE parser and client fail open on malformed streams (Medium)

**Where.** `ssewire.py` lines 70 to 77 (decode errors other than a split character re-raised), 89 (`self._text += text`, no limit), 91 and 96 (`find` and slice over the whole buffer each line), 122 (`self.data +=` without limit); `sse_client.py` lines 156 and 168 to 184 (per-read timeout only; `json.loads` unguarded).

**What I did.**

```
$ python -I t_parser.py utf8
lone 0xff         -> UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 7: invalid start byte
bad continuation  -> UnicodeDecodeError: ...
later bad byte after a good event -> UnicodeDecodeError
spec's expected (UTF-8 decode with replacement): 'data: a�b'

$ python -I t_parser.py longline        # no newline, fed in 256-byte reads like sse_client
  256 KiB:   0.04 s, buffered 0.3 MiB
  512 KiB:   0.16 s, buffered 0.5 MiB
 1024 KiB:   0.60 s, buffered 1.0 MiB
 2048 KiB:   2.93 s, buffered 2.0 MiB    (doubling the input about quadruples the time)

$ python -I t_parser.py manylines       # many lines in one feed (parse_all)
 10000 data lines (78 KiB):   0.04 s
 80000 data lines (625 KiB):  1.47 s

$ python -I t_parser.py datalines
20,000 data lines with no blank line: parser holds 4.8 MiB, events 0

$ python -I t_client.py badutf8          # a local server sends 0xff inside a token event
sse_client.stream raised UnicodeDecodeError: ...
$ python -I t_client.py notjson
sse_client.stream raised JSONDecodeError: Expecting value: line 1 column 1 (char 0)
$ python -I t_client.py pings            # server sends only ': ping' every 0.5 s for 8 s
returned after 8.0 s: events 0, text '', done False
```

**Impact.** One bad byte from a server or a proxy ends the whole stream with an exception, where the spec's "UTF-8 decode" step replaces it with U+FFFD and carries on; the paper says the parser "follows these steps", so this is also an accuracy point for Section 3.2. A misbehaving or hostile upstream can make the client buffer without limit and spend quadratic CPU. A server that sends only pings keeps the client waiting forever (60 s is per read, not per stream), and a stream that ends without `done` is returned as if it were fine (see P6).

**Fix.** Decode with an incremental decoder: `codecs.getincrementaldecoder("utf-8")(errors="replace")`, which also handles split characters; cap the pending line and the pending `data` (for example 1 MiB each) and raise a clear error past it; keep a list of pieces or a `bytearray` and scan only the new part for line ends, so the work stays linear; in `sse_client.stream`, add a total deadline and treat `json.JSONDecodeError` and a missing `done` as a failed stream.

### C6. Listen backlog of 5 resets connections under modest concurrency (Low)

**Where.** `stream_server.py` line 148 (`ThreadingHTTPServer` keeps `socketserver`'s `request_queue_size = 5`).

**What I did.**

```
$ for i in 1 2 3; do python -I t_server.py concurrency; done      # 45 clients at once
45 concurrent: 45 completed in 2.1 s
45 concurrent: 40 completed in 2.1 s   (5 x ConnectionResetError: [Errno 104] Connection reset by peer)
45 concurrent: 41 completed in 2.1 s   (4 x ConnectionResetError)
$ QSIZE=128 python -I t_server.py concurrency   (three runs)
45 concurrent: 45 completed in 1.1 s   (all three runs; no resets)
```

**Impact.** The paper's own worked example sizes for 40 open streams; at that load the lab server drops connections. It is a teaching server, but this is the kind of default a reader carries forward.

**Fix.** Subclass with `request_queue_size = 128` (and the thread cap from C1), or say in Section 7.6 that the lab server is for one or two clients.

### C7. Server work grows with prompt size (Low)

**Where.** `stream_server.py` lines 37 to 41 and 111 to 115 (prefill of 0.5 ms per character, pinging each second).

**What I did.**

```
$ python -I t_server.py prefill
one 60031-byte request held a server thread for 30.1 s; pings sent: 30
```

**Impact.** Invented timings, so this is a property of the stand-in, but it mirrors the real thing: a large prompt costs the server far more than it costs the client to send. Combined with C1 (no cap), 40 such requests tie up 40 threads for 30 seconds.

**Fix.** None needed in the stand-in beyond C1; in the paper, Section 3.5 should name a per-request input-token cap alongside the byte limit (see P1).

### C8. The API-key check: sound when set, two weak edges (Low)

**Where.** `stream_server.py` line 56 (`os.environ.get("LAB_API_KEY")`, read once at import), lines 78 to 81.

**What I did.**

```
$ LAB_API_KEY=s3cret python -I t_auth.py
Authorization None / '' / 'Bearer' / 'Bearer ' / 'Bearer wrong' -> 401
Authorization 'Bearer s3cret'  -> 200 OK
Authorization 'bearer s3cret'  -> 401          (scheme is case-sensitive here)
Authorization 'Bearer s3cret ' -> 401
$ LAB_API_KEY= python -I t_auth.py               (set but empty)
Authorization 'Bearer '        -> 200 OK       (the empty key is accepted)
$ python -I t_auth.py                             (unset)
Authorization None             -> 200 OK       (no key needed, as documented)
```

**Impact.** The comparison itself is right: constant time, done before the body is read, and the server is local only. But an empty variable (a common slip in `.env` files and CI) produces a server that accepts the empty key, and there is no limit on wrong attempts. RFC 9110 makes the scheme name case-insensitive, so `bearer` should be accepted (an interoperability point, not a hole).

**Fix.** Treat an empty key as a configuration error: `if key == "": raise SystemExit("LAB_API_KEY is empty")`; compare the scheme case-insensitively; in the paper, say that wrong-key attempts need their own rate limit (P1).

### C9. The cross-check's network blocker has gaps (Low)

**Where.** `crosscheck.py` lines 42 to 50 (only `socket.socket.connect` is wrapped).

**What I did** (127.0.0.2 is loopback on Linux, so nothing left the machine):

```
$ python -I t_block.py
socket.connect(('127.0.0.2', p))                      -> OSError: blocked by the lab: 127.0.0.2
socket.connect_ex(('127.0.0.2', p))  [0 = connected]  -> 0
UDP sendto(('127.0.0.2', p))  [bytes sent]            -> 1
UDP datagram arrived                                  -> b'x'
socket.getaddrinfo('lab-check.invalid', 80)           -> gaierror: [Errno -2] Name or service not known
blocker's log of outside attempts: ['127.0.0.2']
```

**Impact.** `connect_ex` and UDP `sendto` bypass the blocker entirely and are not counted; `getaddrinfo` runs in C and is not seen, so a DNS query could leave the machine unlogged (not reproduced: no packet capture was run). The blocker also counts loopback addresses other than 127.0.0.1 as "outside". None of this changes the result today (FastAPI, uvicorn and the SDK make no such calls in the run, and the run reported 0), but Section 7.4 states more than the code does (P9).

**Fix.** Also wrap `connect_ex`, `sendto` and `sendmsg`, and `socket.getaddrinfo`; treat `ipaddress.ip_address(host).is_loopback` as local; or reword Section 7.4 (P9).

### C10. `retry_plan` obeys any `retry-after` (Low)

**Where.** `shipmath.py`, `retry_plan`, appendix lines 741 to 744.

**What I did.**

```
$ python -I t_retry.py
{'retry-after': '86400'}     -> wait 86400.0
{'retry-after-ms': '-5000'}  -> wait -5.0; time.sleep(wait) raises ValueError: sleep length must be non-negative
{'retry-after-ms': 'nan'}    -> wait nan;  time.sleep(wait) raises ValueError: Invalid value NaN (not a number)
{'retry-after-ms': 'inf'}    -> wait inf
{'retry-after-ms': 'soon'}   -> ValueError: could not convert string to float: 'soon'
```

**Impact.** Code that copies the function will sleep for a day, sleep forever, or crash on a bad header. The vendors' "treat as a minimum" advice does not mean "with no ceiling".

**Fix.** Parse with `re.fullmatch(r"\d+(\.\d+)?")` for both headers; clamp to `0 <= wait <= cap_server` (for example 60 s); if the server asks for longer, return `None` and surface the error instead of waiting.

### C11. A CR, an empty feed, then LF splits an event (Low)

**Where.** `ssewire.py` lines 86 to 88: `_pending_cr` is cleared on every call, including one with no text.

**What I did.**

```
$ python -I t_parser.py emptyfeed
CR | empty feed | LF: ['a', 'b']  expected ['a\nb']
```

**Impact.** Correctness only; `sse_client` never feeds an empty chunk, but other callers may.

**Fix.** `if not text: return []` at the top of `_lines`.

### C12. Two small accuracy points (Info)

`stream_server.py` lines 8 to 9 promise "a log line that records counts and timings but never the prompt"; there is no log line (`log_message` is silenced and nothing else logs). `serve()` accepts `"::1"` (line 146) but `ThreadingHTTPServer` is IPv4, so it fails: `gaierror [Errno -9] Address family for hostname not supported`. Fix: drop the docstring claim or add the log line; remove `"::1"` from the allowed list or set `address_family = socket.AF_INET6` for it.

---

## Part B. The paper's security and privacy advice

### P1. A public streaming endpoint needs more than the paper lists (High)

**Where.** Section 3.1 ("checks who is calling" is the only line on authentication), Section 3.5 "Your own limits", Section 5 steps 1 and 2, the cheat sheet's decision rules (none on access control or limits).

**What I did.** C1, C6 and C7 above show what the lab server, the paper's example of "its own limits", does under slow, stalled and concurrent clients: unbounded threads, no timeouts, resets at 45 connections, a 60 KB request holding a thread for 30 s.

**Impact.** A beginner who follows Section 3.5 gets per-key request and token limits, a byte limit and a spending alarm. Missing, for a paid model behind a public URL:

- **Concurrent streams per key and per IP.** Rate limits count requests per minute; a streaming request lasts seconds to minutes, so one key can hold dozens of open streams within any per-minute limit. Section 3.10's Little's-law sizing makes this exact point for capacity but not for abuse.
- **Timeouts on the way in, a limit on the way out.** Header and body read timeouts (nginx `client_header_timeout`, `client_body_timeout`; uvicorn `--timeout-keep-alive`), a maximum stream duration, and a server-side `max_tokens` cap that the client cannot raise.
- **The cost of the paper's own nginx advice.** Section 5 step 1 says to raise `proxy_read_timeout` and turn off buffering. Buffering is also what shields the backend from slow readers; with it off, a slow reader holds an upstream connection and a model stream for its whole length. Scope both changes to the streaming `location`, and add `send_timeout` and `limit_conn` there (not reproduced against nginx; nginx was not available here).
- **A hard budget cap, not only an alarm.** Per key and per day, enforced before the model call. An alarm tells you after the money is spent.
- **Authentication basics.** API keys stored hashed, scoped and rotatable; rate limits on failed key attempts (C8); the FastAPI security tutorial the paper cites is a user-login (OAuth2 password and JWT) tutorial, not an API-key design.
- **A warning label on the lab.** The paper presents the lab server's 64 KB limit, key check and 127.0.0.1 binding as the model of "your own limits", without saying it is not production code.

**Fix.** Add to Section 3.5 a short checklist: authenticate every request; cap open streams per key and per IP; cap input tokens and `max_tokens` on the server; time out slow headers, bodies and idle streams; set a maximum stream duration; enforce a per-key daily spend cap before calling the model; rate-limit failed authentication. Add a ninth decision rule to the cheat sheet: "Authenticate, cap open streams and spend per key, and time out slow clients." Add one sentence to Section 7.6 or 8: "The lab's server is for learning on 127.0.0.1; do not expose it."

### P2. No CORS or browser-client guidance (High)

**Where.** Sections 3.2 (introduces `EventSource`), 3.5, 6; "CORS" and "origin" do not appear in the draft.

**What I did.** A FastAPI 0.156.1 app with its built-in telemetry (as in Section 3.1 and `crosscheck.py`), called with the key in the query string, the way people work around `EventSource`:

```
$ python -I t_fastapi.py
status 422 | response body echoes the prompt: False
SECRET-KEY-123     in FastAPI's spans: True
SECRET-PROMPT-456  in FastAPI's spans: False
SECRET-BEARER-789  in FastAPI's spans: False
 span POST /v1/stream {'url.path': '/v1/stream', 'url.query': 'api_key=SECRET-KEY-123', 'url.scheme': 'http'}
```

**Impact.** The browser's `EventSource` sends only GET and cannot set an `Authorization` header, so beginners put the key in the URL. The URL then lands in FastAPI's own spans (`url.query`, shown above), in proxy access logs and in browser history. Two further gaps: nothing says never to put the vendor's API key in browser code (it must stay on your server); and nothing says how to allow a browser origin. A copied `allow_origins=["*"]` with credentials, or a cookie-authenticated stream with no origin check, lets other sites drive a user's paid session.

**Fix.** Add a paragraph to Section 3.2: "From a browser, keep the vendor key on your server. `EventSource` sends GET without custom headers: either authenticate with a same-site, `HttpOnly` cookie and check the `Origin` header, or use `fetch()` with a streamed body, which can send `Authorization`. Never put keys in URLs: they reach logs and traces (FastAPI records `url.query`). Allow only your own origins in CORS (FastAPI's `CORSMiddleware` with an explicit `allow_origins` list; never `*` with credentials)."

### P3. The content and secrets safety net covers only part of where they leak (Medium)

**Where.** Section 3.7 ("Content is opt-in" and the lab paragraph), Section 5 step 4 (the Collector "deletes `gen_ai.input.messages` and `gen_ai.output.messages`"), cheat sheet rule 5.

**What I did.** (1) Shown above: FastAPI's spans record `url.query` (P2). (2) Shown in C2: exception text echoes client input into stderr, and the tracer records only `error.type`, which is the safe pattern; OpenTelemetry's `record_exception`, by contrast, stores the exception message as a span event (SDK behaviour; not reproduced here). (3) Not reproduced: Section 3.7 itself says the released `openai-v2` instrumentation captures content as events on its default path and offers `event_only` on the new one; events and log records are not span attributes, so an attributes processor on the traces pipeline will not remove them. The lab's own `CONTENT_ATTRIBUTES` lists four attributes; step 4 deletes two (it leaves `gen_ai.system_instructions` and `gen_ai.tool.definitions`).

**Impact.** A reader who follows step 4 believes customer text cannot reach storage "in case anyone turns it on". It still can, through span events, the logs pipeline, `url.query`, exception messages, and tool-call arguments and results on `execute_tool` spans (the last not checked against the conventions here).

**Fix.** Rewrite step 4 and rule 5: delete all four content attributes and drop `url.query` (or hash it) on the traces pipeline; filter content-bearing events and log records on the logs pipeline as well; record exceptions by type, not message, at the edge; and test the safety net by turning content capture on in staging and confirming nothing arrives in storage.

### P4. Trace context from untrusted clients (Medium)

**Where.** Section 3.6 (`traceparent`, sampling), Section 3.7's lab paragraph ("The lab's server joins an incoming trace", check c16), Section 5 step 4.

**What I did.**

```
$ python -I t_server.py traceparent
server span trace_id chosen by the client: deadbeefdeadbeefdeadbeefdeadbeef parent 1111111111111111

$ python -I t_sampling.py        # OpenTelemetry SDK 1.45.1, ParentBased(TraceIdRatioBased(0.01))
  no traceparent            kept 7
  client sends flags 01     kept 1000
  client sends flags 00     kept 0
```

**Impact.** Joining an incoming trace is right between your own services and wrong at the public edge. Any caller can pick its trace IDs (collide with or pollute other traces) and, once a reader switches from the default "keep everything" to ratio sampling to save money, force every one of its requests to be recorded (1,000 of 1,000 above) or hide its requests from tracing (0 of 1,000).

**Fix.** Add to Section 3.6: "At the public edge, do not trust an incoming `traceparent`: strip it at the gateway, or use `ParentBased(root=..., remote_parent_sampled=TraceIdRatioBased(r), remote_parent_not_sampled=TraceIdRatioBased(r))` so remote flags cannot change your sampling. The same applies to the `baggage` header." Note in Section 3.7 that the lab joins incoming traces because it plays an internal service.

### P5. Retries and reconnects can multiply cost (Medium)

**Where.** Section 3.4 ("SDK defaults ... retry twice"), Section 3.5 and `retry_plan`, Section 5 step 5, cheat sheet rule 4.

**What I did.**

```
$ python -I t_retry.py
attempts per call: lab plan 3, SDK default 3 (max_retries=2); layered 3 x 3 = 9 model calls for one user request
```

(The SDK figure is the paper's own [V: OAS, ANS]; the multiplication is arithmetic, not a run against the SDKs.) C10 shows `retry_plan` obeying a 1-day or infinite `retry-after`.

**Impact.** Three things the paper does not say. (1) Retry layers multiply: your loop around an SDK that already retries twice, behind a gateway that retries, gives 9 or more paid calls per user request during an outage, exactly when the vendor is overloaded. (2) Retrying a stream that failed after the first token pays again for the whole input and for every output token already generated. (3) The browser's `EventSource` reconnects by itself after a dropped stream (the paper notes it sends `Last-Event-ID`); if the server starts a fresh generation on every reconnect, a flaky network or a client stuck in a loop re-runs paid generations without limit.

**Fix.** Add to Section 3.5: "Retry in one layer only: if your code retries, set the SDK's `max_retries=0`. Give each user request a retry budget and a total deadline. Retry a stream only before the first token; after that, surface the error. Cap any server-requested wait. On reconnect, resume from `Last-Event-ID` or refuse: a 204 response stops `EventSource` from reconnecting." Extend rule 4: "Retry in one layer, with a budget; cap `retry-after`."

### P6. A stream that just stops is treated as success (Medium)

**Where.** Section 3.4 ("a client must check event types, not only the status code"), cheat sheet rule 3, the lab client.

**What I did.** C2 (`fail_after: "x"`): the server sent the 200 and headers, then closed the connection with no `error`, no `usage` and no `done`. `sse_client.py` returns such a stream with `done: False` and no error, and its command-line mode prints the partial text as the answer (`t_client.py pings` returned `done False` after 8 s with no warning).

**Impact.** Checking for `error` events is not enough: proxies time out, servers crash and connections reset without any event. A client that only looks for `error` shows a truncated answer as complete, and the server's usage for that request is never received (the paper does say "count what you received").

**Fix.** Section 3.4 and rule 3: "Treat a stream as successful only when its terminal event arrives (`message_stop` at Anthropic, `response.completed` at OpenAI, the lab's `done`); anything else, including a clean close, is a failure." Make `sse_client.py` print a warning or exit non-zero when `done` is false.

### P7. Telemetry defaults and exposure of self-hosted tools (Medium)

**Where.** Section 3.1 (vLLM recommended), Section 3.8 table, Section 6 picks ("Best default for a solo builder").

**What I did.** Read the draft against its own sources; nothing here was run, because only the lab's requirements could be installed.

- **vLLM usage statistics: on by default, never mentioned.** Source VLM in Section 12 is cited for "usage statistics on by default", but no section tells the reader. Sections 3.1 and 5 send readers to vLLM; the "maker's own telemetry is a separate switch" advice in Section 3.8 should name it (vLLM documents `VLLM_NO_USAGE_STATS=1` and `DO_NOT_TRACK=1`; check the names against `envs.py` at 7b569ec before printing).
- **Logfire's "Content by default?" cell answers a different question.** "Scrubs common secrets by default" is about passwords and keys, not prompts. A reader will take it as "content off". Whether `logfire.instrument_openai()` and `instrument_anthropic()` record messages by default needs checking in the 5.2.0 wheel (not reproduced).
- **Helicone receives your vendor key.** As a proxy, it sees the `Authorization` header carrying your OpenAI or Anthropic key on every request, as well as all content. The table should say so; that is a different trust decision from an SDK that exports spans.
- **Self-hosted UIs: authentication and bind address unverified.** The "best default" sends a beginner to self-host Phoenix or Langfuse, and traces hold token counts and, if anyone turns content on, prompts. Whether Phoenix enables authentication by default and which address it listens on, and which default secrets and published ports Langfuse's Docker Compose file ships with, were not checked (not reproduced). Both should be read in the sources the paper already cites (Phoenix `config.py` at 57b8303; Langfuse at 6343bd8) before recommending them.

**Impact.** A reader who sets every switch the paper names still sends vLLM usage data, may record prompts in Logfire believing it scrubs them, and may run a tracing UI open to the network.

**Fix.** Add vLLM to the "maker's telemetry" sentence and to the picks; change Logfire's cell to the content answer; add "sees your vendor key and all content" to Helicone's row; add one sentence to the picks: "Self-hosted: turn on its authentication, bind it to 127.0.0.1 or a private network, and change every default secret before the first trace."

### P8. Nothing on securing OTLP export (Low, advice gap, not reproduced)

**Where.** Section 3.6 (OTLP ports, Collector), Section 6.

**Impact.** OTLP endpoints default to plain HTTP and gRPC on localhost. A reader who points the exporter at a remote Collector or a hosted platform sends traces, and any captured content, across the network; hosted platforms authenticate with keys in `OTEL_EXPORTER_OTLP_HEADERS`, which then live in environment dumps and CI logs.

**Fix.** One sentence in Section 3.6: "Beyond localhost, export over TLS (`https://` endpoints), keep the Collector's receivers on a private address, and treat `OTEL_EXPORTER_OTLP_HEADERS` as a secret."

### P9. Section 7.4 overstates the network blocker (Low)

**Where.** Section 7.4: "blocks and counts any connection that tries to leave your computer"; also the R3 row.

**What I did.** C9.

**Impact.** The claim is broader than the code. The run's "0" is still a fair result for this run.

**Fix.** Either harden the blocker (C9) or reword: "blocks and counts TCP connections that `socket.connect` makes to anything but 127.0.0.1 (UDP, DNS lookups and `connect_ex` are not covered)."

### Smaller points on the advice (Low)

- **Error events can leak internals** (Section 3.4; not reproduced). A server that passes the vendor's error body, request IDs or a stack trace into `event: error` shows them to every client. Send a short code and message; log the detail server-side.
- **Pinned but not hashed** (Sections 7.4 and 6). `requirements-crosscheck.txt` pins versions but has no hashes; `pip install --require-hashes` with hashes from the test machine would protect readers against a changed upload.
- **Section 3.5's lab sentence is true but partial.** "The lab's server refuses bodies over 64 KB before reading them" holds (shown in "What held up"); the buffering proxy in front of it has no limit and reads 8 MiB into memory (C4).

## Files

- Report: `/home/claude/part13/phase4/security-report.md`
- Unpacked lab: `/home/claude/part13/phase4/security/lab/engineering-stack-lab-part-13/` (unchanged)
- Virtual environment: `/home/claude/part13/phase4/security/venv/`
- Test scripts: `/home/claude/part13/phase4/security/tests/`
