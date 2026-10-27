# The AI Engineering Stack, Part 13: Shipping and Operating

*October 20, 2026. Part 13 of 13 (claude/engineering-stack-plan.md). Tags in this part: 185 [V], 92 [T], 7 [R], 16 [U], 20 [I], counted in Sections 1 to 12 and the checks after them (recounted October 26, 2026, after the Windows run and the package re-check). Still open: no hosted model was called (no keys, by the owner's decision), so the vendors' streams, rate limits and usage APIs are described from their documentation and SDK source code [R]; the lab streams from an invented stand-in model [I] and checks the wire format, the proxies, the tracing rules and the cost arithmetic [T]. The OpenTelemetry GenAI conventions are still at status Development and changed this year; the released Python instrumentation lags them. Prices were read on October 20, 2026 and change often.*

**What this part gives you.** How to put a model behind your own web API and keep it running. **Streaming:** how Server-Sent Events work on the wire, why a stream can still arrive all at once (a buffering proxy), what to do when an error arrives after the "200 OK", and when a client leaves. **Tracing:** what OpenTelemetry records for a model call, which tools record your users' prompts by default, and how to keep them out. **Cost and latency:** what one request costs with caching, batching and long-context surcharges, how many streams you hold open at once, and why you watch the 95th percentile, not the average. The lab runs a stand-in model behind a streaming server, a buffering proxy and a tiny tracer, all on your own computer, and cross-checks them against FastAPI and the OpenTelemetry SDK.

## How to read this part

The tags are Part 01's. **[V: KEY]** points to Section 12, which gives each source's class and the place used. **[T]** ran on the test machine. **[R]** is a reader test. **[U]** names what would settle it. **[I]** is invented for teaching. Source classes: official documentation, specifications and source code (OD), standards bodies (SB), peer-reviewed (PR), preprint (PP), vendor blog or marketing (VB). A vendor's docs are the authority on how its product works, not on how good it is. References like "ledger P11-02" point to rows of claude/engineering-stack-claim-ledger.md, this series' audit of the Gemini report.

**Units.** Prices are US dollars per million tokens ("$2 in, $10 out"). "p95" is the 95th percentile: 95 of every 100 requests were at least this fast. "Points" means percentage points.

**The test machine:** Ubuntu 24.04 in a cloud container, October 20, 2026, with Python 3.13.16, 3.12.3 and 3.11.17. No AI model, no API key, and no network beyond package registries and code hosts.

**This part covers three topics** (plan, Section 7): T28, APIs and streaming, the **Delivery** layer; and two concerns that cut across every layer, T29, observability and tracing, and T30, cost and latency. Part 04 covers prompt caching; Part 09, retries and idempotency keys; Part 10, prompt injection and redaction; Part 11, serving engines and the TTFT, TPOT and ITL definitions.

## 1. In plain words

**T28, APIs and streaming.** A model writes its answer one piece at a time, and the whole answer can take many seconds. Streaming sends each piece as soon as it exists, so the reader sees words within a second instead of waiting for the end. The common way to do it over plain HTTP is Server-Sent Events (SSE): one long response made of small text events [V: WSS]. Every big vendor streams this way; Gemini's REST API does when you add `alt=sse` to the URL [V: AND, OAD, GMD]. Two surprises: anything between your server and the reader can hold the pieces back and deliver them in one lump (nginx does by default) [V: NGX][T], and once streaming has started the status code is already "200 OK", so an error has to arrive as an event inside the stream [V: AND].

*Analogy.* A letter versus a phone call. SSE turns the letter into a call, unless a switchboard in between records the whole call and plays it back at the end.

**T29, observability and tracing.** A trace is a timeline of one request: the web call, the model call inside it, each tool the agent ran, with how long each took and what it cost [V: OTS]. OpenTelemetry is the open standard for recording traces, and it has conventions for AI calls: names for the model, the token counts and the finish reason [V: GAI]. The conventions say instrumentations SHOULD NOT record prompts and answers unless you switch that on [V: GAI]; several popular tracing tools record them by default [V: TLP, OLT, OIN], and OWASP's 2026 list calls out observability platforms for exactly this [V: OWS].

*Analogy.* A flight recorder. It should record the altitude and the engine settings, not everything said in the cabin.

**T30, cost and latency.** You pay per token, input and output at different prices, with discounts for cached input and for batch jobs, and surcharges for very long prompts or for keeping data in one country [V: AND, OAD, GMD]. Speed has two numbers: how soon the first words appear and how long the whole answer takes [V: AND]. And a few slow requests matter more than the average suggests: the mean of 94 one-second answers and six nine-second answers is 1.48 seconds, which describes none of them [T].

*Analogy.* A taxi meter that charges a different rate for the luggage, and a dispatcher who judges the service by the longest waits, not the average.

**Where it sits in the stack** (plan, Section 5). Delivery is the top layer: how people and programs reach the system. Observe and Economize are two of the five concerns that run through every layer.

## 2. Definitions

Every term is also in claude/engineering-stack-glossary.md.

| Plain words | Technical term | Notes |
|---|---|---|
| One long HTTP response made of small text events | Server-Sent Events (SSE); `text/event-stream` | WHATWG HTML standard, section 9.2 [V: WSS] |
| The browser object that reads SSE and reconnects | `EventSource` | Sends `Last-Event-ID` when it reconnects [V: WSS] |
| A two-way connection that stays open | WebSocket | RFC 6455 [V: RFC] |
| A proxy holding a response back before passing it on | Response buffering | nginx: on by default [V: NGX] |
| A line that keeps an idle stream open | Keep-alive comment | `: ping`, every 15 seconds or so [V: WSS, FAS] |
| How many requests are open at once | Concurrency | Little's law: L = λW [V: LIT] |
| The value that 95% of measurements are at or below | 95th percentile, p95 | Use histograms to compute it [V: PRM] |
| The time until the first piece arrives | Time to first token (TTFT); first chunk | Part 11, Section 3.6 defines the family |
| A timeline of one request | Trace | Made of spans [V: OTS] |
| One timed step inside a trace | Span | Has a name, attributes, a status [V: OTS] |
| The header that joins spans across services | `traceparent` (W3C Trace Context) | `version-traceid-parentid-flags` [V: W3C] |
| The wire protocol for traces, metrics and logs | OTLP | Ports 4317 (gRPC) and 4318 (HTTP) [V: OTS] |
| A program that receives, filters and forwards telemetry | OpenTelemetry Collector | Can drop attributes before storage [V: OTS] |
| Keeping only some traces | Sampling (head or tail) | Head sampling can't promise to keep every error [V: OTS] |
| Agreed names for AI telemetry | OpenTelemetry GenAI semantic conventions | Status Development [V: GAI] |
| Recording prompts and answers in traces | Content capture | Off by default in the conventions [V: GAI] |
| Half-price jobs answered within a day | Batch API | All three big vendors [V: AND, OAD, GMD] |
| A higher price once a prompt passes a length | Long-context pricing | OpenAI over 272,000 tokens and Haiku 5.5 over 100,000, for the whole request; Gemini 3.1 Pro over 200,000 [V: OAD, AND, GMD] |
| Reusing a stored answer for a similar question | Semantic caching | Can return wrong or stale answers [V: AZS] |
| Sending easy requests to a cheaper model | Model routing | Savings were measured on particular model pairs [V: RTL] |
| A limit on requests or tokens per minute | Rate limit; HTTP 429 | Anthropic also returns 529 when overloaded [V: AND] |

## 3. How it works

### 3.1 Putting a model behind an API

**The shape.** A client sends a request to your web server; your server checks who is calling and whether the request is allowed, calls the model (a hosted API or your own serving engine, Part 11), and streams the answer back. The Gemini report's advice to "separate the web server from the heavy inference engine" holds: the serving engines of Part 11 are separate programs with their own HTTP APIs (ledger P11-06) [V: VLM, OLL, LCP].

**What a public endpoint needs.** A model behind a public URL spends your money on every request, so the limits come first [I: from this part's security review]. Authenticate every request, with keys stored hashed, scoped and easy to rotate, and rate-limit failed attempts. Cap open streams per key and per IP address: a per-minute request limit doesn't stop one key from holding dozens of long streams. Cap input size and `max_tokens` on the server, where the client can't raise them. Time out slow headers, slow bodies and idle streams, and set a longest stream length. Enforce a daily spending cap per key before calling the model; an alarm only tells you after the money is gone. Turning off proxy buffering (Section 3.3) also removes the proxy's shield against slow readers, so scope that change to the streaming route and pair it there with a send timeout and a connection limit (nginx's `send_timeout` and `limit_conn`; not run against nginx here) [U]. The lab's server shows some of this in miniature (Section 3.5); it's a teaching server for 127.0.0.1, not one to put on a network.

**OpenAI-compatible, mostly.** vLLM, llama.cpp's server and Ollama each offer `/v1/chat/completions`, and newer releases also `/v1/responses`, so one client library can talk to all of them [V: VLM, LCP, OLL]. The match isn't complete. vLLM ignores the `user` parameter and doesn't support `suffix` [V: VLM]. llama.cpp says "no strong claims of compatibility with OpenAI API spec is being made" [V: LCP]. Ollama's `/v1/responses` is "non-stateful" only and can't set the context size through the OpenAI API; that takes a `num_ctx` setting in a Modelfile [V: OLL]. Test the features you use against the engine you run. vLLM also sends anonymous usage statistics to its makers by default; `VLLM_NO_USAGE_STATS=1` or `DO_NOT_TRACK=1` switches that off [V: VLM].

**FastAPI changed in 2026.** It now has its own SSE support, since 0.135.0 (March 1, 2026): set `response_class=EventSourceResponse` on the route and yield events [V: FAS]. It sends a `: ping` comment after 15 seconds of silence and sets `Cache-Control: no-cache` and `X-Accel-Buffering: no` for you [V: FAS][T]. One trap: it JSON-encodes `data`, so `data="hello"` goes out as `data: "hello"`, with the quotes; use `raw_data` for plain text [V: FAS][T]. Since 0.142.0 (September 29, 2026), FastAPI also creates OpenTelemetry spans by itself when you give it a tracer provider; since 0.143.0 (October 8, 2026) it sets up exporters from `OTEL_*` variables only if you opt in with `FASTAPI_OTEL_AUTO_CONFIGURE=true` [V: FAS][T]. Its security tutorial, a user login with OAuth2 and JWT rather than an API-key design, now uses PyJWT and Argon2 password hashing (pwdlib); it has no built-in rate limiter [V: FAS].

**LangServe is gone.** Deprecated since November 18, 2024 and archived on May 5, 2026 (ledger P11-04) [V: LCS]. Its suggested successor, LangGraph Platform, was renamed LangSmith Deployment in October 2025; LangChain's docs describe self-hosting as an add-on to its Enterprise plan, and the `langgraph-api` server package is under the Elastic License 2.0, which is source-available, not open source [V: LCS, PYPI].

**Kubernetes and "secure multi-tenancy"** (ledger P11-03). Kubernetes' own page says there is "no single definition" of how hard or soft isolation is, calls it "a broad spectrum", lists the tools (namespaces, access control, quotas, network policies, sandboxed containers, dedicated nodes) and says sandboxing "is often recommended when you are running untrusted code", because ordinary containers share the host's kernel [V: K8S]. It supports multi-tenant designs; it doesn't make them secure by itself. Part 08 covers sandboxes.

### 3.2 Server-Sent Events on the wire

**The format** (WHATWG HTML, section 9.2, last updated October 20, 2026) [V: WSS]. The response has type `text/event-stream` and must be UTF-8. Each line is a field: `data:` (the payload; several lines join with newlines), `event:` (a name; "message" if absent), `id:` (the browser reports it back as `Last-Event-ID` when it reconnects) and `retry:` (milliseconds to wait before reconnecting). A line starting with a colon is a comment and is ignored. A blank line ends the event. Lines may end in CRLF, LF or CR.

```
event: token
id: 3
data: {"text": " pieces"}

: ping

```

**Rules people get wrong.** One space after the colon is dropped, but only one. An `id` containing a NUL character is ignored. A `retry` that isn't all digits is ignored. An event with no `data` lines isn't delivered. Text after the last blank line is thrown away when the stream ends [V: WSS]. The lab's parser follows these steps and gives the spec's own results on its four examples; fed one byte at a time, including a CRLF and a two-byte character split across reads, it returns the same events (checks c02 to c04) [T].

**Why the 15-second ping.** The spec's authoring notes warn that "legacy proxy servers are known to, in certain cases, drop HTTP connections after a short timeout" and suggest a comment line "every 15 seconds or so" [V: WSS]. nginx's `proxy_read_timeout` is 60 seconds by default, counted between two reads, so a model that thinks quietly for longer than that is cut off unless something is sent [V: NGX]. FastAPI and sse-starlette both ping every 15 seconds by default [V: FAS, SSS].

**SSE or WebSocket?** (ledger P11-06). SSE is one-way, server to client, over ordinary HTTP, which proxies, load balancers and authentication already understand. A WebSocket upgrades the connection to a two-way channel (RFC 6455) [V: RFC]. For a text answer, SSE is enough, and every big vendor's text API streams with it [V: AND, OAD, GMD]. WebSockets earn their place where both sides talk at once: OpenAI's Realtime API uses WebRTC in browsers and WebSocket on servers, and the openai SDK 3.35.1 has a persistent WebSocket mode for the Responses API, with a beta `response.steer` event for steering an answer while it's being written [V: OAD, OAS].

**Many tabs.** Over HTTP/1.1, browsers allow about six connections per site, shared by all tabs, so a page that opens one stream per tab can stall; MDN gives the figure of six (citing a Stack Overflow answer rather than a standard) and says HTTP/2 raises it, by default to 100 streams [V: MDN]. The spec itself only says clients with per-server limits "might run into trouble" [V: WSS].

**From a browser.** Keep the vendor's API key on your server; a key in browser code is public. `EventSource` makes a plain GET request and can't add an `Authorization` header [V: WSS], so people put keys in the URL, where they reach proxy logs, browser history and traces: FastAPI 0.156.1's own spans record the query string as `url.query` [T: this part's security review]. Either authenticate the stream with a same-site, `HttpOnly` cookie and check the `Origin` header, or read the stream with `fetch()`, which can send headers. Allow only your own origins in CORS (FastAPI's `CORSMiddleware` with an explicit `allow_origins` list, never `*` together with credentials) [I].

### 3.3 Why a stream can arrive all at once

The Gemini report says SSE pushes tokens "the exact moment they are generated" (ledger P11-02). Not always. Four things sit between the model and the reader, and each can hold bytes back:

1. **Your own code.** A generator that collects text before yielding, or a framework that buffers output. Starlette's `StreamingResponse` sends each yielded piece; its gzip middleware leaves `text/event-stream` alone by default [V: STL].
2. **Reverse proxies.** nginx buffers proxied responses by default (`proxy_buffering on`); a response header `X-Accel-Buffering: no` turns it off for that one response, unless the proxy is configured to ignore that header [V: NGX].
3. **Other boxes in between** (load balancers, CDNs, corporate proxies): their behaviour varies and wasn't checked here [U].
4. **The reader.** The spec warns that block or line buffering on the receiving side "can cause delays in event dispatch", so a client should handle each line as it arrives [V: WSS].

**The lab shows it** (check c06) [T]. The stand-in model sends 24 words over about half a second [I: invented timings]. Straight to the client, the first word arrives at 0.08 seconds. Through a proxy that buffers in 4 KB blocks unless the response says `X-Accel-Buffering: no` (a simplified model of nginx's default [I]), the first word still arrives at 0.08 seconds, because the server sends that header. Through the same proxy set to ignore the header, every word arrives together at 0.54 seconds: the stream became a single delivery, and the client can't tell why.

```
direct                   first token 0.08 s, last 0.55 s, 24 tokens
proxy, header honoured   first token 0.08 s, last 0.55 s, 24 tokens
proxy, header ignored    first token 0.55 s, last 0.55 s, 24 tokens
```

**What to do.** Send `X-Accel-Buffering: no` and a `Cache-Control` header that stops caching (FastAPI sends `no-cache`, sse-starlette `no-store`) [V: FAS, SSS]; configure your own proxy for the streaming route; ping more often than the shortest idle timeout on the path; and measure time to first token from the reader's side, through the real network, not only on the server.

### 3.4 Errors, disconnects and shutdown

**An error after the 200.** Once the first byte of a stream is out, the HTTP status can't change. Anthropic sends `event: error` with, for example, `overloaded_error`, which "would normally correspond to an HTTP 529" [V: AND]. OpenAI's Responses stream has `response.failed`, `response.incomplete` and `error` events [V: OAS]. So a client must check event types, not only the status code, and should count a stream as finished only when its last event arrives (`message_stop` at Anthropic, `response.completed` at OpenAI, `done` in the lab). A stream that simply stops, with no error event, is a failure too [V: AND, OAS]. The lab's server sends three words, then an error event, and no usage event (check c07); its client reports a stream with no `done` as unfinished and gives up after a total deadline (check c20) [T]. Keep error events short, a code and a plain message, never the vendor's raw error body or a stack trace; log the details on your server. The lab's server sends `server_error` with "the stream failed" for any crash and records only the exception's type (check c20) [T].

**Usage is at the end.** OpenAI's Responses stream carries token counts in `response.completed`; Chat Completions streams send usage only if you ask for `stream_options.include_usage`, and warn "If the stream is interrupted, you may not receive the final usage chunk" [V: OAS]. Anthropic's `message_delta` events carry cumulative usage [V: AND]. Gemini streams `GenerateContentResponse` objects with `usageMetadata`; which chunk carries the final counts wasn't stated on the pages read [V: GMD][U]. If a stream breaks, count what you received, or check the vendor's usage reports later (Section 3.8).

**Resuming.** Anthropic's advice now differs by model: for Claude 4.5 and earlier, send the partial answer back as the start of the assistant's turn; for Claude 4.6 and later, add a user message asking the model to continue from where it stopped [V: AND].

**When the reader leaves.** If nobody is reading, stop generating: you pay for every output token. Starlette notices a disconnect by listening for the ASGI `http.disconnect` message, and stops the generator [V: STL]; under uvicorn 0.54.0, which reports ASGI version 2.3, that listener is the path used [V: UVI]. The cross-check shows it: a client read three events from FastAPI and left, and the generator stopped at 3 of 200 [T]. In the lab's own server, a client that leaves after two words stops the stand-in at 3 of 24, because the next write fails (check c08) [T]. A hosted model keeps generating unless your server stops reading from it; closing the vendor stream when your client leaves is your code's job [I].

**Shutdown.** uvicorn's `--timeout-graceful-shutdown` has no default limit, so a long open stream can hold a deploy; sse-starlette hooks shutdown to end its streams [V: UVI, SSS]. Set a limit and let clients reconnect.

**SDK defaults.** The openai 3.35.1 and anthropic 1.16.0 Python SDKs wait up to 600 seconds per request (5 seconds to connect) and retry twice [V: OAS, ANS]. The anthropic SDK refuses a non-streaming call it estimates will take over 10 minutes, saying "Streaming is required for operations that may take longer than 10 minutes" [V: ANS]. Both now use `httpx2`, a newer HTTP library, not `httpx` [V: OAS, ANS].

### 3.5 Rate limits and retries

Part 09 covered backoff with jitter and idempotency keys; what's specific here:

- **Anthropic** limits requests, input tokens and output tokens per minute per model class, and for most models only uncached input counts toward the input limit [V: AND]. A 429 is your organization's limit and usually comes with `retry-after`; a 529 means the platform as a whole is overloaded [V: AND]. Its tiers are now Start, Build, Scale and Custom, with monthly spend caps, and "A tier spend-cap 429 has no `retry-after` header": retrying won't help until the cap is raised [V: AND].
- **OpenAI** limits requests and tokens per minute and per day; its headers are `x-ratelimit-limit-requests`, `x-ratelimit-remaining-tokens` and so on, and `Retry-After` is to be treated "as a minimum" [V: OAD].
- **The SDKs** read `retry-after-ms` before `retry-after` (anthropic) and retry 408, 409, 429 and server errors (Part 09) [V: ANS].

The lab's `retry_plan` encodes these rules: obey the server's wait, never retry a 400, stop after two retries, and don't retry an Anthropic 429 with no `retry-after` (check c13) [T]. It also caps the wait: it obeys up to 60 seconds, gives up beyond that, and ignores a value that isn't a plain number, so an HTTP-date `retry-after` falls back to the backoff, a simplification [T][I].

**Don't multiply retries.** The SDKs already retry twice [V: OAS, ANS]. Your own loop of three tries around them makes nine paid calls for one user request during an outage, and a gateway that also retries makes more [I: arithmetic]. Retry in one layer: if your code retries, set the SDK's `max_retries=0`. Give each user request a retry budget and a total deadline. Retry a stream only before its first token; after that, a retry pays again for the input and every token already written, so report the error instead. Browsers add a loop of their own: `EventSource` reconnects by itself after a dropped stream, so a server that starts a fresh generation on each reconnect pays each time. Resume from `Last-Event-ID`, or answer with HTTP 204 No Content, which tells `EventSource` to stop reconnecting [V: WSS].

**Your own limits.** Section 3.1 lists what a public endpoint needs. FastAPI has no built-in limiter; slowapi (MIT), fastapi-limiter (Apache-2.0) and limits (MIT) are common choices [V: FAS, PYPI]. The lab's server refuses bodies over 64 KB before reading them, answers a wrong field type with a 400 before any stream starts, drops a client that stays silent for 30 seconds, answers 503 past 32 clients at once, checks an optional API key in constant time (`hmac.compare_digest`) and listens only on 127.0.0.1 (checks c09, c18 and c20). Its buffering proxy refuses a bad or missing `Content-Length` and answers 502 when the server is down (check c21) [T].

### 3.6 Tracing with OpenTelemetry

**The pieces** [V: OTS]. A **trace** is one request's timeline; a **span** is one timed step in it, with a name, **attributes** (key and value pairs), events and a status (unset, error or OK; unset already means success). Spans in different services join one trace through the W3C `traceparent` header: `00-` then a 32-hex-digit trace ID, a 16-digit parent span ID and two flag digits, for example `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`, whose last bit says the caller may have recorded it [V: W3C]. Telemetry travels as **OTLP**, to port 4317 (gRPC) or 4318 (HTTP) [V: OTS]. A **Collector** sitting beside your service can batch, retry, sample and delete attributes before anything is stored [V: OTS].

**Sampling.** The SDK's default sampler keeps every trace (`parentbased_always_on`). **Head sampling** decides at the start, cheaply, so it "cannot ensure that all traces with an error within them are sampled"; **tail sampling** decides after the trace ends, for example keeping all errors and slow requests, and is harder to run [V: OTS].

**At the public edge, don't trust an incoming `traceparent`.** Any caller can send one with trace IDs of its choosing, and a parent-based sampler follows the caller's flag. With the SDK 1.45.1 and `ParentBased(TraceIdRatioBased(0.01))`, a client sending flag `01` had 1,000 of 1,000 requests kept, one sending `00` had none, and requests with no header 7 of 1,000 [T: this part's security review]. Strip the header at your gateway, or give `ParentBased` ratio samplers for remote parents as well (`remote_parent_sampled` and `remote_parent_not_sampled`), so a caller can't change what you keep; treat the `baggage` header the same way [V: OTS]. Between your own services, joining the trace is the point.

**Exporting beyond your computer.** Over the network, export over TLS (`https://` endpoints), keep the Collector's receivers on a private address, and treat `OTEL_EXPORTER_OTLP_HEADERS`, which often holds a hosted platform's key, as a secret [V: OTS][I].

**Running it offline.** The Python SDK 1.45.1 has an in-memory exporter for tests and a console exporter; `OTEL_SDK_DISABLED=true` switches everything off, and with no service name the resource says `unknown_service:python` [V: OPY]. One researcher's run found that a `SimpleSpanProcessor` exporting to an OTLP endpoint with no collector listening blocked the calling thread for about 7.5 seconds per span while it retried, then logged a failure without crashing [V: OPY]. Use `BatchSpanProcessor` in a request path; it queues spans and exports every 5 seconds by default [V: OPY].

### 3.7 The GenAI conventions: names for model calls

**Where they live.** On May 5, 2026, OpenTelemetry moved the GenAI conventions out of its main conventions repository into `semantic-conventions-genai`; the old pages now say "This page has moved and is no longer maintained in this repository" [V: SCV, GAI][T: the move dated from git history]. The whole set is at status **Development**, which under OpenTelemetry's maturity rules means it "SHOULD NOT be used in production" and may change or disappear without notice [V: OTS, GAI]. In practice everyone uses it anyway; expect renames.

**A model call** [V: GAI]. The span is named `{gen_ai.operation.name} {gen_ai.request.model}`, for example `chat claude-sonnet-5-5`. Required attributes: `gen_ai.operation.name` and `gen_ai.provider.name`. `gen_ai.request.model` is required when known. Recommended: `gen_ai.response.model`, `gen_ai.response.finish_reasons`, `gen_ai.usage.input_tokens` and `gen_ai.usage.output_tokens`, with cache tokens as `gen_ai.usage.cache_read.input_tokens` and `gen_ai.usage.cache_write.input_tokens` and reasoning tokens as `gen_ai.usage.reasoning.output_tokens`. Input tokens "SHOULD include all types of input tokens, including cached tokens" [V: GAI]. Attributes a sampler needs (operation, provider, model, server) should be set when the span starts [V: GAI]. **Agents and tools** get spans named `invoke_agent {gen_ai.agent.name}` and `execute_tool {gen_ai.tool.name}`; **MCP** calls get `{mcp.method.name} {target}`, and because one HTTP connection carries many MCP messages, the trace context goes inside each message's `params._meta` [V: GAI].

**Content is opt-in.** Prompts, system instructions and answers go in `gen_ai.input.messages`, `gen_ai.system_instructions` and `gen_ai.output.messages`, each marked as likely to hold "sensitive information including user/PII data", and "OpenTelemetry instrumentations SHOULD NOT capture them by default" [V: GAI]. The conventions describe three patterns: record nothing; record on spans, for testing or storage cleared for it; or upload the content to separate storage and keep only a reference, which they recommend for production [V: GAI]. Where a language can't put structured values on spans, the content goes there as a JSON string [V: GAI].

**Metrics, renamed this year.** The conventions now define `gen_ai.client.inference.duration`, `gen_ai.client.inference.time_to_first_chunk` and `.time_per_output_chunk` (histograms in seconds), token counters such as `gen_ai.client.inference.usage.input_tokens` for totals and cost, and per-call token histograms that "should not be used for total usage or cost calculations" [V: GAI]. These come from unreleased changes: `gen_ai.client.token.usage` was replaced, `cache_creation` became `cache_write`, and `gen_ai.client.operation.duration` is now only for operations other than inference [V: GAI]. Earlier, convention release 1.37.0 had renamed `gen_ai.system` to `gen_ai.provider.name` [V: SCV]. **The released code lags:** `opentelemetry-instrumentation-openai-v2` 2.4b0 (May 1, 2026) follows conventions 1.30.0 by default, still writes `gen_ai.system` and still records `gen_ai.client.token.usage` and `gen_ai.client.operation.duration` [V: OPY]. Its newer behaviour is behind `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`, which changes what `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` accepts: `true` on the old path, `span_only`, `event_only` or `span_and_event` on the new one [V: OPY]. A dashboard built from the spec and one built from what the instrumentation emits will not match today. The Python GenAI instrumentations have also moved, to `opentelemetry-python-genai`; the copies left in the contrib repository, openai-v2 2.4b0 among them, get security patches only. The new repository includes an official Anthropic instrumentation, `opentelemetry-instrumentation-genai-anthropic` 1.2b0, with content off by default [V: OPY].

**The lab** builds the attributes for one model call by these rules: span `chat {model}`, input tokens including cached ones, no content unless asked, content as a JSON string when asked, and a filter that drops content the way a Collector can (check c15) [T]. The OpenTelemetry SDK 1.45.1 accepts those attributes unchanged, and its W3C propagator reads `traceparent` exactly as the lab does, rejecting an all-zero trace ID (cross-checks X6 and X7) [T]. The lab's server joins an incoming trace, as an internal service should (Section 3.6), and its model-call span is the server span's child (check c16) [T].

### 3.8 Tracing tools: what they keep and what they send

Read from each project's source at the version named, October 20, 2026 [V: LFS, PHX, OIN, LSM, TLP, OLT, MLF, OPK, WVE, LGF, HEL]. "Content by default" means prompts and answers are recorded unless you switch it off. Licences are information, not legal advice.

| Tool | What it is | Licence | Content by default? | Sends usage data to its maker by default? | Takes OTLP? |
|---|---|---|---|---|---|
| OpenTelemetry instrumentations | Official libraries for OpenAI, Anthropic and others | Apache-2.0 | No | No (they send only to the exporter you configure) | Is OTLP |
| Langfuse (server; SDK 5.0.3) | Tracing, evaluation and prompt UI; self-hostable | MIT core, commercial `ee/` folders | Yes, through its SDK; masking available (`mask_otel_spans`) | Self-hosted server: usage statistics to PostHog, off with `TELEMETRY_ENABLED=false` (ignored when an enterprise licence key is set); SDK: none found | Yes |
| Arize Phoenix 20.23.0 | Tracing and evaluation UI | Elastic-2.0 (source-available) | Through OpenInference: yes | Yes (FullStory, Scarf); off with `PHOENIX_TELEMETRY_ENABLED=false` | Yes |
| OpenInference | Arize's instrumentations and attribute names (`llm.token_count.prompt`, not the GenAI names) | Apache-2.0 | Yes; `OPENINFERENCE_HIDE_INPUTS` and `_OUTPUTS` default false | None noted | Sends OTLP |
| LangSmith (SDK 0.14.11) | LangChain's hosted tracing; self-hosting is an Enterprise add-on | SDK MIT; service proprietary | Yes; `LANGSMITH_HIDE_INPUTS`, `_OUTPUTS` | SDK: none found | Yes |
| Traceloop OpenLLMetry (traceloop-sdk 0.62.4) | Instrumentations plus an SDK | Apache-2.0 | Yes: `TRACELOOP_TRACE_CONTENT` defaults to true | None found; its `telemetry_enabled` setting is now unused | Is OTLP |
| OpenLIT 1.45.0 | Instrumentations plus a UI | Apache-2.0 | Yes: `capture_message_content=True` | Fetches a price list from GitHub unless given one | Is OTLP |
| MLflow 3.17 | Experiment tracking with tracing | Apache-2.0 | Yes, with `mlflow.openai.autolog()` | Yes; off with `MLFLOW_DISABLE_TELEMETRY=true` or `DO_NOT_TRACK=true` | Yes |
| Opik 2.2.109 | Comet's tracing and evaluation | Apache-2.0 | Not stated in what was read [U] | Yes (usage statistics and error reports); off with `OPIK_ANALYTICS_ENABLE=false`, `OPIK_SENTRY_ENABLE=false` | Yes |
| W&B Weave 0.53.12 | Weights & Biases tracing | Apache-2.0 | Yes; traces go to `trace.wandb.ai` | Error reports; off with `WANDB_ERROR_REPORTING=false` | Yes |
| Pydantic Logfire 5.2.0 | Hosted tracing; SDK open, server closed | SDK MIT | Yes: `instrument_openai()` records `gen_ai.input.messages`; it also scrubs values that look like secrets | `send_to_logfire` defaults to true; with no token it tries to create a project | Is OTLP |
| Helicone | A proxy you point your API calls at | Apache-2.0; self-hostable | It logs what it proxies, and as a proxy it sees your vendor API key on every request; `Helicone-Omit-Request` and `-Response` headers leave bodies out | Not checked [U] | Not found in its docs |

Three things in that table change what you should do. **Defaults disagree:** OpenTelemetry's own instrumentations record no prompts, while Traceloop, OpenLIT, OpenInference and Logfire record them unless told not to [V: OPY, TLP, OLT, OIN, LGF]. **OWASP agrees this matters:** its 2026 list keeps sensitive information disclosure at LLM02 and says "Observability platforms (Langfuse, LangSmith, Datadog LLM Observability) log full prompts, completions, chunks, and traces by default"; it advises scrubbing logs and traces "before APM ingestion" [V: OWS]. **The maker's own telemetry is a separate switch** from your traces: Phoenix, MLflow, Opik and the self-hosted Langfuse server report usage by default, Weave sends error reports, and vLLM (Section 3.1) sends usage statistics [V: PHX, MLF, OPK, LFS, WVE, VLM]. Set those switches before the first run.

**Retention.** Hosted free tiers keep traces for a limited time: Langfuse Cloud's Hobby tier shows 30 days of data access, LangSmith keeps base traces 14 days and extended ones 180, Logfire's free tier 30 days, Arize AX Free 15 days [V: LFS, LSM, LGF, PHX]. Vendor statements, read on their pages.

**Evaluating live traffic** (Part 02's evals, run on production traces). Langfuse runs model-graded evaluators on new traces with filters and a sampling rate, and needs your model provider key; LangSmith does the same and moves every trace it scores to the longer, more expensive retention; open-source Phoenix can run evaluators on production traces as well as datasets, and its docs send continuous monitoring with alerts to Arize AX, which has a free tier [V: LFS, LSM, PHX]. Each evaluation is another paid model call.

### 3.9 What it costs

**Prices** (per million tokens, read October 20, 2026) [V: AND, OAD, GMD]:

| Model | Input | Cached input | Output | Notes |
|---|---|---|---|---|
| Claude Haiku 5.5 | $0.10 | (not read) | $0.50 | Prompts over 100,000 tokens: $0.50 and $2.50 |
| Claude Sonnet 5.5 | $2 | $0.10 to read; $2.50 to write for 5 minutes | $10 | Read 0.05x and write 1.25x the input price (Part 04) |
| Claude Opus 5.5 | $4 | | $20 | Fast mode $8 and $40, not with batch |
| Claude Fable 5.1 | $10 | | $50 | |
| GPT-6 Luna | $0.10 | $0.01 | $0.50 | |
| GPT-6 Astra | $10 | $1; $12.50 to write | $50 | Over 272,000 input tokens: 2x input and cache, 1.5x output |
| Gemini 3.8 Flash | $0.75 | | $3.75 | Doubles on January 1, 2027 |
| Gemini 3.1 Pro (preview) | $2 | | $12 | Over 200,000 prompt tokens: $4 and $18 |

**Discounts and surcharges.** All three vendors' batch APIs charge half price for jobs answered within a day: Anthropic up to 100,000 requests or 256 MB per batch, most done within an hour, expired after 24 hours, results kept 29 days; OpenAI up to 50,000 requests or 200 MB, a 24-hour window, output deleted after 30 days; Gemini inline under 20 MB or files up to 2 GB, target 24 hours, expired after 48, results kept six weeks [V: AND, OAD, GMD]. Anthropic says batch and caching discounts "can stack", with cache hits "on a best-effort basis", typically 30% to 98% [V: AND]. OpenAI also sells **Flex** at the batch price and **Fast** (called "Priority processing" until July 30, 2026) at a higher price; for GPT-5.6 Sol, OpenAI states twice the standard rate [V: OAD]. Keeping data in one region costs extra: Anthropic 1.1x for `inference_geo: "us"`, OpenAI 10% for models released from March 5, 2026 [V: AND, OAD].

**Long-context pricing can apply to the whole request.** OpenAI prices GPT-6 Astra past 272,000 input tokens at higher rates "for the full request", and Anthropic says a Haiku 5.5 request over its threshold pays the higher prices; Anthropic's other current models have no long-context surcharge [V: OAD, AND]. Google's pricing page shows Gemini 3.1 Pro's higher tier without saying whether it covers the whole prompt or only the excess [V: GMD][U]. The lab's `request_cost` reprices the whole request for all three [T]:

```
gpt-6-astra              272,000 in:    $2.77   272,001 in:    $5.52  (1.99x)
gemini-3.1-pro-preview   200,000 in:  $0.4120   200,001 in:  $0.8180  (1.99x)
claude-haiku-5-5         100,000 in:  $0.0105   100,001 in:  $0.0525  (5.00x)
```

Anthropic counts cache reads and writes toward the Haiku threshold [V: AND]; the lab counts them for all three, which OpenAI's and Google's pages read didn't state [U]. For Gemini that is an assumption [U]. The lab also doubles OpenAI's cache-write rate past the line, reading "2x input and cache rates" as covering both cache prices [I].

**One request** (2,000 tokens in, 500 out; `python demo.py`) [T]:

```
claude-haiku-5-5         $0.000450  batch $0.000225  x 10,000 a day for 30 days    $135.00
claude-sonnet-5-5         $0.00900  batch  $0.00450  x 10,000 a day for 30 days  $2,700.00
gemini-3.1-pro-preview     $0.0100  batch  $0.00500  x 10,000 a day for 30 days  $3,000.00
gpt-6-astra                $0.0450  batch   $0.0225  x 10,000 a day for 30 days $13,500.00
```

The same Sonnet 5.5 request with 1,800 of the 2,000 input tokens read from a prompt cache costs $0.00558 instead of $0.009 [T]. Output dominates: in the uncached Sonnet request, the 500 output tokens cost $0.005 of the $0.009 [T].

**Where the money is reported.** Per request, in each response's usage fields; across an organization, in usage and cost APIs that need an administrator key: Anthropic's Usage and Cost API (cost in daily buckets, usage within about five minutes) and OpenAI's organization usage and costs endpoints [V: AND, OAS]. The GenAI conventions' token counters are meant as "a proxy for cost approximation" [V: GAI]; the vendor's invoice is the authority.

**Cheaper answers.** **Routing** easy requests to a smaller model saved money in research: RouteLLM (ICLR 2025) reports cutting costs "by over 2 times without sacrificing response quality" on its benchmarks, its repository claims up to 85% while keeping 95% of GPT-4's MT-Bench score, with GPT-4 as the strong model and Mixtral 8x7B as the weak one, and the FrugalGPT preprint up to 98% against GPT-4 [V: RTL, FRG]. Those are older models; whether the savings hold for today's pairs wasn't checked [U]. Measure on your own traffic (Part 02). **Semantic caching** returns a stored answer to a question that looks similar; Microsoft's documentation for its gateway warns it "can surface responses that are incorrect, outdated, or unsafe" and says to keep caches separate per user [V: AZS]. No guidance on it was found from OpenAI, Anthropic or Google [U].

### 3.10 Latency and load

**Where the time goes.** For an answer streamed to a person, two numbers matter: time to the first words and time to the last (Part 11, Section 3.6 defines TTFT, TPOT and ITL). Anthropic's list of levers: pick a faster model or lower effort, shorten the prompt and the output, and stream [V: AND]. OpenAI's seven principles include generating fewer tokens, using fewer input tokens, making fewer requests and running steps in parallel; it claims that cutting output by half "may cut ~50% of your latency" while halving the prompt saves only 1 to 5%, a vendor estimate with no model named [V: OAD]. Independent measurements of hosted models depend on where they're taken: Artificial Analysis measures from one Google Cloud region and notes its time to first token "includes network latency" [V: AAM].

**How many streams at once.** Little's law: the average number of requests in a system equals the arrival rate times the average time each spends there, whatever the order of service [V: LIT]. At 5 requests a second and 8 seconds per streamed answer, your server holds 40 streams open; at 20 a second and 30 seconds, 600 (check c12) [T]. Each needs a connection through every proxy and a slot in your rate limits. The browser's six-connection limit (Section 3.2) caps one user's tabs, not your server.

**Watch the tail.** In the lab's example, 94 answers take 1 second and 6 take 9: the mean is 1.48 seconds, the median 1, the 95th percentile 9 (check c12) [T]. The mean describes nobody. Record durations as histograms: Prometheus explains that pre-computed quantiles can't be combined across servers, while histograms can, with `histogram_quantile(0.95, sum by (le) (rate(..._bucket[5m])))` [V: PRM]; the GenAI conventions suggest histogram buckets for durations from 0.01 to about 82 seconds, doubling [V: GAI].

**What to measure in production** [V: GAI, PRM]: requests and errors by `error.type`; time to first chunk and total duration as histograms; input, cached, output and reasoning tokens as counters by model; cost from those counters and the price sheet; and the share of streams that ended early (client gone, timeout, error), this part's own suggestion [I].

## 4. Gemini said, evidence says

| Gemini (ledger row) | Evidence | Section |
|---|---|---|
| "Platform engineering" packages models behind REST or GraphQL APIs (P11-01) | Still a misused term: CNCF's platform is internal self-service tooling. What the report describes is putting a model behind an API, this part's T28 | 3.1 |
| SSE pushes tokens "the exact moment they are generated" (P11-02) | Wrong as worded. nginx buffers proxied responses by default; the spec warns that buffering in the reader "can cause delays in event dispatch"; the lab's stream arrived all at once through a proxy that ignored `X-Accel-Buffering: no` [V: WSS, NGX][T] | 3.3 |
| Kubernetes "supports secure multi-tenant environments" (P11-03) | Overstated. Kubernetes calls isolation "a broad spectrum" and says sandboxing "is often recommended" for untrusted code, with separate clusters for some cases [V: K8S] | 3.1 |
| FastAPI, LangServe, Docker, API gateways (P11-04) | LangServe is still outdated: archived May 5, 2026; its successor was renamed LangSmith Deployment, and self-hosting it is an Enterprise add-on. FastAPI is current and now has built-in SSE (0.135.0) and OpenTelemetry (0.142.0) [V: LCS, FAS] | 3.1 |
| A gateway that logs "every incoming prompt, outgoing generation, token count, and latency metric" (P11-05) | Logging every prompt is a privacy decision, not a default to copy. The GenAI conventions say instrumentations "SHOULD NOT capture them by default"; OWASP LLM02:2026 names observability platforms that "log full prompts ... by default" [V: GAI, OWS] | 3.7, 3.8 |
| WebSockets versus SSE; separate the web server from the inference engine; auth, rate limits, logs (P11-06) | Consistent, with an update: OpenAI now offers WebSocket modes for Realtime and for ordinary Responses; FastAPI has no built-in rate limiter; serving engines are separate programs [V: OAD, OAS, FAS, VLM] | 3.1, 3.2, 3.5 |
| Routing easy queries to smaller models (P8-02) | In the spirit of the vendors' advice to pick a faster or smaller model; research reports 2x to 98% savings, measured on GPT-4-era model pairs [V: RTL, FRG, AND, OAD] | 3.9 |
| Phoenix as an evaluation tool (P9-09) | Still Elastic License 2.0 at 20.23.0; it can evaluate production traces itself, and its docs send continuous monitoring with alerts to Arize AX [V: PHX] | 3.8 |

## 5. Examples

**Real examples.**

1. *A standard library that waits for nobody* [V: FAS]. FastAPI added first-party SSE in March 2026 and first-party OpenTelemetry in October 2026, after years of both being third-party add-ons. A 2025 tutorial for streaming with FastAPI is already out of date in what it imports.
2. *A convention that moved while people used it* [V: GAI, SCV, OPY]. The GenAI conventions changed repository in May 2026 and renamed their main metrics, while the released OpenAI instrumentation still emits the old names. Two teams can both "follow the OpenTelemetry conventions" and build dashboards that don't agree.
3. *A security list naming tools* [V: OWS]. OWASP's 2026 LLM Top 10 names Langfuse, LangSmith and Datadog when it warns that observability platforms log full prompts by default.

**A fully worked example: a support chat goes live** [I: the team, its traffic and its proxy are invented; every computed number came from the lab].

*Input.* A support team will answer 10,000 chats a day with Claude Sonnet 5.5. A typical turn has a 1,800-token system prompt (product notes), 200 tokens of question and a 500-token answer. Peak traffic is 5 requests a second, and an answer takes about 8 seconds to stream. The company's nginx sits in front of every service. Policy says customer messages may not leave the support system.

*Step 1, the API.* FastAPI with `EventSourceResponse`, which sends `X-Accel-Buffering: no` and pings every 15 seconds [V: FAS]. Ask the platform team to turn off buffering on the streaming route anyway, and raise `proxy_read_timeout` above the longest silent thinking time, on that route only, with a send timeout and a connection limit beside them (Section 3.1) [V: NGX]. Measure time to first token through nginx before launch, as in check c06 [T].

*Step 2, capacity.* By Little's law, 5 requests a second times 8 seconds is 40 open streams at peak; the daily average is 10,000 / 86,400 = 0.116 a second, which holds about 0.93 streams open, around one [V: LIT][T]. Size worker connections, proxy limits and the rate limit for the peak of 40, not the average.

*Step 3, cost.* Without caching, $0.009 a turn and $2,700 for 30 days [T]. With the shared 1,800-token system prompt cached, $0.00558 a turn and $1,674 for 30 days, provided the prefix stays identical between turns (Part 04) [T]. Cache hits aren't guaranteed, so budget for the uncached figure and watch `gen_ai.usage.cache_read.input_tokens` [V: GAI].

*Step 4, tracing.* OpenTelemetry's instrumentation with content capture off, which is its default [V: OPY]. In case anyone turns it on, a Collector that deletes all four content attributes (`gen_ai.input.messages`, `gen_ai.output.messages`, `gen_ai.system_instructions`, `gen_ai.tool.definitions`) and `url.query` from spans, and filters content-carrying events and log records on the logs pipeline too [V: OTS, GAI]; exceptions recorded by type, not by message; and a test in staging that turns capture on and confirms nothing reaches storage [I]. The gateway strips incoming `traceparent` headers (Section 3.6). The tracing UI is self-hosted, with authentication on, a private address and its maker's telemetry switched off (Section 6). Alerts on p95 time to first token, computed from histograms [V: PRM], and on errors by type, not on means [I].

*Step 5, failures.* Clients count a turn as done only at its last event, so an `error` event or a stream that just stops is a failure even after a 200; the server stops reading the model's stream when the browser leaves; retries happen in one layer, only before the first token, and obey `retry-after` up to a cap; the spend-cap 429, the one Anthropic 429 without `retry-after`, pages a person instead of retrying [V: AND][T].

*Step 6, the night job.* A nightly summary of the day's tickets (4,000 tokens in, 300 out each) goes through the Batch API at half price: $0.0055 instead of $0.011 per summary [V: AND][T].

*Output.* A streaming endpoint that has been measured through the real proxy, sized for 40 streams, budgeted at $1,674 to $2,700 a month for chat, traced without customer text, and alerting on the slow tail.

## 6. What you need

Checked October 20, 2026 [V: PYPI]. Licences from each project's licence file or PyPI metadata; information, not legal advice.

| Tool | What it's for | Licence | Runs on | Account or key? | Version |
|---|---|---|---|---|---|
| The lab's scripts | SSE, a stand-in server, proxy and tracer, cost and load arithmetic | This series | Python 3.11 to 3.13, standard library [T] | No | Lab zip |
| FastAPI | Web API framework with SSE and OpenTelemetry built in | MIT | Python 3.10 or later; declares `starlette>=0.46.0`, and Starlette 1.9.0, the newest on October 20, needs Python 3.11 or later [V: FAS] (corrected October 26, 2026 from "needs Starlette 1.9.0") | No | 0.162.0 (October 23, 2026) [T: PyPI, October 26]; the rest of this row was checked at 0.156.1 |
| uvicorn | The server that runs FastAPI | BSD-3-Clause | Python 3.10 or later | No | 0.54.0 |
| sse-starlette | SSE for Starlette apps, older than FastAPI's own | BSD-3-Clause | Python 3.11 or later since 3.6.0 (3.10 before) [T: PyPI] | No | 3.6.0 (October 25, 2026) [T: PyPI, October 26]; ping still 15 s [V: SSS] |
| OpenTelemetry Python SDK | Traces, metrics and logs | Apache-2.0 | Python 3.10 or later | No | 1.45.1 |
| OpenTelemetry GenAI instrumentations | Spans for OpenAI and Anthropic calls | Apache-2.0 | Python 3.10 or later | No (the model API needs one) | openai-v2 2.4b0; genai-anthropic 1.2b0 |
| OpenTelemetry Collector | Receives, filters and forwards telemetry | Apache-2.0 | A separate program | No | (not read) [U] |
| Langfuse | Tracing and evaluation, self-hosted or hosted | MIT core, commercial `ee/` | Docker for self-hosting | Hosted: yes | SDK 5.0.3 |
| Arize Phoenix | Tracing and evaluation | Elastic-2.0 | Python 3.11 to 3.14 | No, self-hosted | 20.26.1 (October 25, 2026) [T: PyPI, October 26]; the rest of this row was checked at 20.23.0 |

Sources: Sections 3.1, 3.7 and 3.8 [V: FAS, UVI, SSS, OPY, LFS, PHX, PYPI].

Picks, and when to skip them:

- **Best default for a solo builder:** FastAPI's own `EventSourceResponse`, the OpenTelemetry SDK with a `BatchSpanProcessor`, content capture off, and a self-hosted tracing UI with its telemetry switch set; Phoenix (`PHOENIX_TELEMETRY_ENABLED=false`) or Langfuse (`TELEMETRY_ENABLED=false`) [V: FAS, OPY, PHX, LFS] (in PowerShell `$env:PHOENIX_TELEMETRY_ENABLED = "false"`, in macOS and Linux shells `export PHOENIX_TELEMETRY_ENABLED=false`, in the window that starts it) [R]. If you serve with vLLM, add `VLLM_NO_USAGE_STATS=1` [V: VLM].
- **If you already use LangChain's hosted tools:** LangSmith, with `LANGSMITH_HIDE_INPUTS=true` and `LANGSMITH_HIDE_OUTPUTS=true` until you've decided what you may store [V: LSM].
- **If you use Traceloop, OpenLIT or OpenInference:** turn content off first: `TRACELOOP_TRACE_CONTENT=false`, `openlit.init(capture_message_content=False)`, `OPENINFERENCE_HIDE_INPUTS=true` and `OPENINFERENCE_HIDE_OUTPUTS=true` [V: TLP, OLT, OIN].
- **Self-hosting a tracing UI:** turn on its authentication, keep it on 127.0.0.1 or a private network, and change every default secret before the first trace. Phoenix's settings default to listening on every address (`0.0.0.0`) with `PHOENIX_ENABLE_AUTH` off, so a solo setup should set `PHOENIX_HOST=127.0.0.1`; Langfuse's Docker Compose file marks its default passwords and keys `# CHANGEME` and publishes the web app's port 3000 on every address [V: PHX, LFS].
- **Skip for new work:** LangServe, archived [V: LCS].
- **When not to stream:** background jobs, evaluations and anything a person isn't waiting for; send those to a batch API at half price [V: AND, OAD, GMD].

## 7. Set it up

**Before you start.** Part 01's setup: Python 3.11 to 3.13 and the series folder `ai-stack` in your home folder. Unzip `engineering-stack-lab-part-13.zip` into `ai-stack` (on Windows: right-click, Extract All, then Browse to `C:\Users\<your name>\ai-stack` as the destination; if the folder ends up inside another of the same name, move the inner one up) [R], or in PowerShell, from the folder holding the zip, `Expand-Archive engineering-stack-lab-part-13.zip $HOME\ai-stack`, which is easier if Browse won't lead you to your home folder [T on Windows, October 26, 2026]; on macOS and Linux, from the folder holding the zip, `python3 -m zipfile -e engineering-stack-lab-part-13.zip ~/ai-stack` [T on Linux]. The core lab needs nothing installed. Type each command on its own line.

### 7.1 to 7.3 Windows, macOS and Linux

**7.1 Windows,** in PowerShell [T on Windows 11 with Python 3.13.16, typed by a reader, October 26, 2026; `Activate.ps1` was refused there, so `run_lab.py` ran as described below the commands]:

```
cd $HOME\ai-stack\engineering-stack-lab-part-13
py -V:3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python run_lab.py
```

If PowerShell refuses to run `Activate.ps1`, use Part 01's one-time fix (Part 01, Section 7.1, step 5), then activate again. Or change no setting and type `.venv\Scripts\python.exe` wherever a step says `python`, for example `.venv\Scripts\python.exe run_lab.py` [T on Windows]. The first run may make Windows Firewall ask whether Python may use the network; the lab only listens on 127.0.0.1, so you can choose Cancel [U: whether the prompt appears for 127.0.0.1 only].

**7.2 macOS** [R: no macOS test machine] **and 7.3 Linux** [T]:

```
cd ~/ai-stack/engineering-stack-lab-part-13
python3.13 -m venv .venv
source .venv/bin/activate
python run_lab.py
```

Expect `21 of 21 checks passed` after about ten seconds; timings in the output vary from run to run. If `py -V:3.13` or `python3.13` isn't found, use the 3.11 or 3.12 from Part 01 (for example `py -V:3.12 -m venv .venv` or `python3.12 -m venv .venv`).

### 7.4 Optional: check against FastAPI and OpenTelemetry [T]

With the virtual environment active:

```
python -m pip install -r requirements-crosscheck.txt
python crosscheck.py
```

This installs FastAPI 0.156.1, uvicorn 0.54.0 and the OpenTelemetry SDK 1.45.1 with their dependencies, 16 packages in all [T]; on Python 3.11, pip also lists setuptools, and pip may print a notice about a newer version of itself, both harmless [T]. The file pins exact versions but not file hashes. The script starts FastAPI on 127.0.0.1, gives it a tracer provider without an exporter, so nothing is sent, and blocks and counts any attempt to reach another computer through Python's socket functions (TCP and UDP connections and name lookups). That is a check on these libraries, not a sandbox [T]. Expect, abridged [T on Python 3.13.16, 3.12.3, 3.11.17]:

```
fastapi 0.156.1, uvicorn 0.54.0, Python 3.13.16
PASS  X1 the lab's parser reads FastAPI's EventSourceResponse
...
PASS  X7 the lab's traceparent rules match OpenTelemetry's W3C propagator
Network attempts outside this computer: 0 []
7 of 7 cross-checks passed
```

### 7.5 Reader test R4: stream in two windows [T]

Open two terminal windows. In each, go to the lab folder, then activate its environment (Section 7.1 or 7.2). In the first: `python stream_server.py`. It prints `Stand-in model streaming on http://127.0.0.1:8013/v1/stream (Ctrl+C to stop)` [T]. In the second: `python sse_client.py "Tell me about streaming"`. It prints the answer and a line like `time to first token 0.085 s, total 0.552 s, 24 tokens, usage {'input_tokens': 4, 'output_tokens': 24}`, with your own timings [T: on Linux; on Windows, October 26, 2026, `time to first token 0.112 s, total 0.590 s`]. The stand-in gives the same answer whatever the prompt says [I]. Stop the server with Ctrl+C. Port 8013 must be free; `python stream_server.py 8014` and `python sse_client.py "hi" 8014` use another.

### 7.6 A tour

| Command | What it does |
|---|---|
| `python run_lab.py` | 21 checks; exit code 0 only if all pass |
| `python mutation_check.py` | Breaks the lab 48 ways in temporary copies; each must make `run_lab.py` fail (about 5 minutes) |
| `python demo.py` | Prints the seven worked tables behind Sections 3 and 5 |
| `python stream_server.py` and `python sse_client.py` | Section 7.5 |
| `python crosscheck.py` | Section 7.4 |

The lab's server is for learning on 127.0.0.1; don't expose it to a network. From the lab folder, in Python, after `import shipmath as sm`: `sm.request_cost("claude-sonnet-5-5", {"input": 2000, "output": 500})` returns `Fraction(9, 1000)`, and `batch=True` halves it [T]. Add a model by adding its prices to `PRICES` and any long-context rule to `LONG_CONTEXT`. `sm.concurrent(5, 8)` returns `40` [T]. `import ssewire` gives `ssewire.encode(...)` and `ssewire.Parser().feed(bytes)` [T].

### 7.7 Common errors and fixes

| What you see | Why | Fix |
|---|---|---|
| PowerShell refuses to run `Activate.ps1` (seen on Windows 11, October 26, 2026 [T]) | Its script policy | Part 01's one-time fix (Part 01, Section 7.1, step 5) [R], or type `.venv\Scripts\python.exe` in place of `python` [T] |
| `can't open file '.../run_lab.py': [Errno 2] No such file or directory` | The terminal isn't in the lab folder | `cd` into it [T] |
| `OSError: [Errno 98] Address already in use` (Windows: `[WinError 10048]`) from `stream_server.py` | Another program, or an earlier server, holds port 8013 | Stop it, or pass another port (Section 7.5) [T on Linux]. On Windows a second server may start without this error, because Python's server asks for address reuse [U] |
| `ConnectionRefusedError` from `sse_client.py` | The server isn't running, or runs on another port | Start `stream_server.py` first [T] |
| `Install the cross-check packages first (Part 13, Section 7.4)` | `crosscheck.py` without its packages | Section 7.4 [T] |
| `FAIL c06_proxy_buffering` on a busy computer | The timing checks compare first and last arrival; a heavily loaded computer can blur them | Close other programs and rerun; if it persists, keep the output for R1 [I] |
| `The stream did not finish (no done event)` from `sse_client.py` | The server stopped mid-stream, or the client's deadline passed | Look at the server's window; restart it [T] |
| A FastAPI stream shows `data: "hello"` with quotes | FastAPI JSON-encodes `data` | Use `raw_data` for plain text [V: FAS][T] |

### 7.8 How to uninstall the lab

`deactivate`, move up one folder with `cd ..`, and delete `engineering-stack-lab-part-13`: `rm -rf engineering-stack-lab-part-13` on macOS and Linux [T], `Remove-Item -Recurse -Force engineering-stack-lab-part-13` in PowerShell [R]. The cross-check's packages go with the virtual environment; pip keeps a copy of what it downloaded in its cache, which `python -m pip cache purge` empties (run it before `deactivate`) [T]. The lab writes no files outside its folder, and the mutation check deletes its temporary copies [T].

## 8. Hands-on lab: stream it, buffer it, trace it, price it

**Goal.** Stream a stand-in model over SSE and read it back with a parser that follows the spec, watch a buffering proxy turn the stream into one delivery, trace a request without recording the prompt, and do the cost and load arithmetic from Section 3.

**Prerequisites.** Section 7 for your system. **Time:** about 30 minutes by hand, under a minute automated (the mutation check about 5 minutes). **Cost:** none. **Pinned:** the standard library only; the optional cross-check pins FastAPI 0.156.1, uvicorn 0.54.0 and the OpenTelemetry SDK 1.45.1. **Data:** the stand-in model and its timings are invented [I]; prices as read on October 20, 2026. **Files:** all are in the zip; `shipmath.py`, the arithmetic and rules, is also printed in the appendix. The others: `ssewire.py`, `stream_server.py`, `sse_client.py`, `buffer_proxy.py`, `tinytrace.py`, `run_lab.py`, `mutation_check.py`, `demo.py`, `crosscheck.py`, `requirements-crosscheck.txt` and `README.md`.

**Steps.** Run every command from the lab folder, with its virtual environment active (Section 7). Outputs are from the test machine, Python 3.13.16, October 20, 2026 [T].

1. **Read the parser.** Open `ssewire.py`: `Parser.feed` decodes the bytes, `_lines` splits them at CRLF, LF or CR, `_line` is the spec's list of field rules, and `_dispatch` is what happens at a blank line.
2. **Feed it the spec's example.** `python -c "import ssewire; [print(e) for e in ssewire.parse_all(b': test stream\n\ndata: first event\nid: 1\n\ndata:second event\nid\n\ndata:  third event\n\n')]"` prints three events: `first event` with `last_event_id='1'`; `second event` with an empty `last_event_id`, because an `id` line with no value resets it; and ` third event` with its second space kept [T].
3. **Print the tables.** `python demo.py` prints seven: one request at four prices, the cached request, the long-context jumps, Little's law, the tail example, the buffering demonstration, and one request's trace with token counts and no prompt text [T].
4. **Stream in two windows.** Section 7.5 [T].
5. **Break it.** In `shipmath.py` (line 58), change `prompt_tokens(usage) > rule["over"]` to `>=`, so a prompt of exactly 272,000 tokens pays the long-context price. `python run_lab.py` now ends `20 of 21 checks passed`, with `FAIL c11_long_context_whole_request: AssertionError 1103/200`: $5.515 instead of $2.77 [T]. Put it back and confirm 21 of 21.
6. **Prove the checks can fail.** `python mutation_check.py` breaks the lab 48 ways (comments read as data, the space after the colon kept, a CRLF split across reads counted twice, the buffering header not sent, generation going on after the client leaves, an error sent as a token, no size limit, a wrong field type accepted, no cap on clients, content captured by default, cached tokens left out of input tokens, an all-zero trace ID accepted, a 400 retried, a day-long `retry-after` obeyed, the batch discount ignored, a proxy that trusts any `Content-Length`, an error event that shows internal details, the server listening on every address, and more) and expects `run_lab.py` to fail each time: `48 of 48 mutations caught` [T].
7. **Cross-check (optional).** Section 7.4 [T].

**Expected output** (`python run_lab.py`, abridged; timings vary by a few hundredths):

```
PASS c01_sse_encode: multi-line data, fields, comment; bad event and id refused
PASS c02_sse_spec_examples: the four examples in the WHATWG spec give the spec's results
...
PASS c06_proxy_buffering: header honoured: first token 0.08 of 0.54 s; ignored: 0.54 of 0.54 s, all at once
...
PASS c21_proxy_refuses_bad_requests: bad Content-Length 400, too big 413, none 411, upstream down 502
21 of 21 checks passed
```

**If it fails.** A FAIL line names the check; Section 7.7 covers the common errors. If a check fails only on your machine, keep the whole output for reader test R1 ("Run on your computer", after Section 12).

## 9. Teach it

**Learning objectives.** After this part you can:

1. write and read Server-Sent Events by the spec's rules, and say what can delay a stream between the model and the reader;
2. handle an error that arrives after "200 OK", a reader who leaves, and the vendors' rate-limit replies;
3. record a model call as an OpenTelemetry span with the GenAI names, keep prompts out of traces, and pick a tracing tool knowing what it sends by default;
4. price a request with caching, batching, residency and long-context rules, and size how many streams you hold with Little's law;
5. explain why you alert on the 95th percentile and record durations as histograms.

**Prerequisites.** Part 01's setup; Part 02 (evals), Part 04 (caching), Part 09 (retries), Part 10 (privacy), Part 11 (serving and its timing terms). Reading a little Python.

**Common misconceptions.**

- *"SSE delivers each token the moment it exists."* nginx buffers by default, and the spec warns about buffering on the reader's side too [V: NGX, WSS][T].
- *"A 200 status means the answer succeeded."* Errors can arrive inside the stream after the 200, and a stream can stop with no event at all; only the last event means done [V: AND, OAS][T].
- *"Following OpenTelemetry means recording the prompts."* Its conventions say not to by default; some tools do it anyway [V: GAI, TLP, OLT].
- *"Long-context pricing charges extra only for the extra tokens."* At OpenAI and for Haiku 5.5 it reprices the whole request [V: OAD, AND][T].
- *"Average latency is a good health check."* A mean of 1.48 seconds hid a 95th percentile of 9 [T].

**Exercises, with checked answers.** Run the checks from the lab folder, with its environment active.

1. *A new price.* Gemini 3.8 Flash costs $0.75 in and $3.75 out until the end of 2026. What does a 2,000-in, 500-out request cost? Answer: $0.003375. Check: `python -c "import shipmath as sm; from fractions import Fraction as F; sm.PRICES['gemini-3.8-flash'] = dict(input=F(3, 4), output=F(15, 4), cache_read=None, cache_write=None); print(float(sm.request_cost('gemini-3.8-flash', {'input': 2000, 'output': 500})))"` prints `0.003375` [T]. From January 1, 2027 this model's prices double, and so does the answer; other Gemini models change on their own dates [V: GMD].
2. *Open streams.* 12 requests a second, 20 seconds each: how many streams are open? Answer: 240. Check: `python -c "import shipmath as sm; print(sm.concurrent(12, 20))"` prints `240` [T].
3. *Read a stream by hand.* What two events are in `event: a`, `data: x`, `data: y`, a blank line, `: c`, a blank line, `data:z`, a blank line? Answer: type `a` with data `x`, newline, `y`; then type `message` with data `z`; the comment is skipped. Check: `python -c "import ssewire; print([(e.type, e.data) for e in ssewire.parse_all(b'event: a\ndata: x\ndata: y\n\n: c\n\ndata:z\n\n')])"` prints `[('a', 'x\ny'), ('message', 'z')]` [T].

**Five-question self-check.** Answers follow.

1. Your stream reaches users all at once. Name two places to look.
2. Why must a client check for an `error` event even after a 200?
3. Which GenAI attribute holds the prompt, and is it recorded by default?
4. A prompt goes from 272,000 to 272,001 tokens on GPT-6 Astra. What happens to the price?
5. 94 requests take 1 second and 6 take 9. Which number belongs in your alert?

*Answers.* (1) A proxy buffering the response (send `X-Accel-Buffering: no`, check the proxy's settings) and your own code collecting text before yielding [V: NGX, STL]. (2) The status was sent with the first byte; later failures can only be events, or the stream just stops [V: AND]. (3) `gen_ai.input.messages`; no, it's opt-in [V: GAI]. (4) The whole request is repriced: input and cache rates double and output rises 1.5 times [V: OAD][T]. (5) The 95th percentile, 9 seconds, not the mean of 1.48 [T].

**You've got it when** you can take a design with a model behind an API and say, with numbers, what users will wait for, how many streams you'll hold, what it costs per month, and what your traces will and won't contain.

**Best next resources** (checked to exist on October 20, 2026): the WHATWG server-sent events section [V: WSS]; the OpenTelemetry GenAI conventions repository [V: GAI]; OpenTelemetry's sampling and Collector docs [V: OTS]; Prometheus's "Histograms and summaries" [V: PRM]; OWASP's LLM02:2026 [V: OWS]; the vendors' batch and rate-limit pages [V: AND, OAD, GMD].

**A tutor prompt to practise with.** Paste this into Claude (modelled on claude/github-tutor-prompt.md):

```
Help me learn to run an AI model behind my own web API.

How to teach me: one idea at a time, a question I answer before you go on,
and a small worked example with real numbers for each idea. When I'm wrong,
show me the reasoning rather than the answer, so I can find the mistake.

Topics, in order:
1. Server-Sent Events: the wire format, and what can delay a stream.
2. Errors inside a stream, readers who leave, rate limits and retries.
3. Tracing a model call with OpenTelemetry, without recording prompts.
4. Choosing a tracing tool: what it records and sends by default.
5. Pricing a request: caching, batch, long-context rules.
6. Load and latency: Little's law, percentiles, histograms.

For any product, version, price, limit or default, tell me it may have
changed since your training and that I should check the vendor's page.

Start by asking what I'm building and who will use it.
```

**What to learn next.** Phase 5 assembles the series. From here, Part 02's evals on live traffic and Part 10's privacy rules are the two that matter most once real users arrive.

## 10. Limits and debates

- **No hosted model was called.** Streams, rate limits and usage APIs come from the vendors' docs and SDK source code; a stand-in replaced the model [R][I]. The wire format, proxies, tracing rules and arithmetic ran [T].
- **The lab's server and proxy are teaching code.** They have the limits the security review asked for (checks c18 to c21), not what a public service needs (Section 3.1) [T][I].
- **The proxy is a model of nginx, not nginx.** It shows the mechanism; real proxies have more settings, and CDNs and load balancers weren't checked [I][U].
- **The GenAI conventions are a moving target.** Status Development, renamed metrics this year, a repository move in May, and instrumentation that lags; names in this part are as of October 18, 2026 [V: GAI, OPY].
- **Tool behaviour was read, not watched.** Telemetry and content defaults come from source code at the versions named; no network traffic was captured [U].
- **Prices change.** All figures were read on October 20, 2026; some change on a set date (Gemini's on January 1, 2027) [V: GMD].
- **Routing savings come from GPT-4-era model pairs.** RouteLLM's 2x and 85% and FrugalGPT's 98% weren't re-run [V: RTL, FRG][U].
- **When this is the wrong tool.** A batch job doesn't need streaming; an internal tool with ten users doesn't need a tracing platform, a log file with token counts will do [I].
- **Open questions.** Which Gemini stream chunk carries the final usage; how CDNs buffer SSE; when the GenAI conventions reach a release.

**Where this part touches project docs** (flagged, not applied; plan, Section 8):

1. *Claim ledger P11-02* should read "wrong as worded": buffering can delay delivery [V: WSS, NGX][T]. *P11-03* should read "overstated" [V: K8S]. *P11-04* should add LangSmith Deployment and FastAPI's built-in SSE [V: LCS, FAS]. *P11-05* should cite OWASP LLM02:2026 and the conventions' opt-in rule [V: OWS, GAI].
2. *Part 11, Section 3.6* defines TTFT, TPOT and ITL by formula; the GenAI conventions now add their own names (`gen_ai.client.inference.time_to_first_chunk` for clients, `gen_ai.server.time_to_first_token` for servers), worth a line there [V: GAI].
3. *Freshness ledger:* FastAPI 0.156.1 and Phoenix 20.23.0 replace Section 2's 0.143.0 and 20.21.0; Section 19 records the rest.
4. No conflict found with the taxonomy or the guide: the project's search for observability, tracing and streaming found nothing there to correct.

## 11. Skill opportunity

claude/new-skills-appendix.md has no matching idea. A **llm-cost-check** skill would take a model name, token counts (or a usage export) and a traffic pattern, and report the cost per request and per month with caching, batch, residency and long-context rules, and the number of open streams by Little's law. `shipmath.py` would be its script, with a dated price sheet it refuses to use past a set age; checks c10 to c13 with their mutations would start its eval pack. It would do arithmetic on numbers it is given, never call a model or a billing API. Like every skill here, it needs the owner's trigger and non-trigger lists first (project instructions, "Building a skill", step 1).

## 12. Sources

All opened October 20, 2026, by the lead session or one of two researcher agents. Code and documentation in repositories were read from git clones at the commits named or from wheels downloaded from PyPI, so quotes come with file and line; web pages through a fetch tool that summarizes, with quotes asked for verbatim. The lead re-read in source FastAPI's SSE encoder, ping and headers and its telemetry opt-in, Starlette's gzip exclusion, sse-starlette's defaults, the Kubernetes multi-tenancy page, the GenAI conventions' span name, content rule, metric names and their changelog fragments, Traceloop's and OpenLIT's content defaults and OWASP's LLM02:2026 text, re-fetched the WHATWG authoring notes and the vendors' batch, streaming and pricing pages, and ran every number in the lab [T]. Grade: confidence from 1 to 10 that the source supports the use made of it.

| Key | Source | Class | Used for | Grade |
|---|---|---|---|---|
| AAM | Artificial Analysis, "Performance benchmarking methodology" (v2.2.0, March 2, 2026) | VB | Where its latency numbers are measured | 7 |
| AND | Anthropic docs: Streaming messages; Errors; Rate limits; Usage and Cost API; Pricing; Reducing latency; Batch processing | OD | Event types and the final `message_stop`, mid-stream errors, resuming, 429 and 529, tiers and spend caps, admin reports, prices, residency, fast mode, latency levers, batch limits | 9 |
| ANS | anthropics/anthropic-sdk-python at 2d555d1 (1.16.0): `_constants.py`, `_base_client.py`, `types/usage.py`. Re-checked October 26, 2026 at v2.3.0: the facts used here are unchanged | OD | Timeouts, retries, the 10-minute rule, usage fields | 10 |
| AZS | Microsoft Learn, Azure API Management `llm-semantic-cache-lookup` policy (updated 2026-08-19) | OD | Semantic caching's risks and per-user caches | 8 |
| FAS | fastapi/fastapi at f6ce798 (0.156.1): `fastapi/sse.py`, `routing.py`, `applications.py`, `telemetry/`, release notes, security tutorial. Re-checked October 26, 2026 at 0.162.0 (`sse.py`, `pyproject.toml`): ping still 15 s; `starlette>=0.46.0`, as in 0.156.1 | OD | Built-in SSE, ping, headers, JSON-encoded data, telemetry opt-in, PyJWT and pwdlib, no rate limiter | 10 |
| FRG | Chen, Zaharia and Zou, "FrugalGPT", arXiv 2305.05176v1 (abstract) | PP | "Up to 98%" | 6 |
| GAI | open-telemetry/semantic-conventions-genai at 547934a (2026-10-18): `docs/gen-ai/` (client-inference, gen-ai-spans, gen-ai-agent-spans, gen-ai-metrics, gen-ai-token-metrics, mcp), `changelog.d/` | SB | Status, span names, attributes, content rule, metrics and renames | 10 |
| GMD | Google AI for Developers: API reference "Generating content"; Batch API (updated 2026-09-17); Pricing | OD | `streamGenerateContent`, usage fields, batch limits, prices | 8 |
| HEL | Helicone/helicone at 6b057cd: README, LICENSE, header docs | OD | What Helicone is; omit headers | 8 |
| K8S | kubernetes/website at 6df0b1b: `concepts/security/multi-tenancy.md` | OD | Ledger P11-03 | 9 |
| LCP | ggml-org/llama.cpp at ead9f32: `tools/server/README.md` | OD | OpenAI-style routes and the compatibility disclaimer | 9 |
| LCS | langchain-ai/langserve repository page; LangChain's LangSmith Deployment page and pricing page | OD, VB | Archived May 5, 2026; the rename; Enterprise self-hosting | 8 |
| LFS | langfuse/langfuse at 6343bd8 (LICENSE, telemetry, `docker-compose.yml`); langfuse/langfuse-docs at ab9037b; langfuse 5.0.3 wheel | OD | Licence split, telemetry switch, default secrets and ports, masking, retention, online evaluation | 9 |
| LGF | pydantic/logfire at f3fc0ec; logfire 5.2.0 wheel (`_internal/main.py`, `integrations/llm_providers/openai.py`); pydantic.dev pricing | OD, VB | Closed server, `send_to_logfire`, messages recorded by `instrument_openai`, scrubbing, retention | 8 |
| LIT | Little, "Little's Law as Viewed on Its 50th Anniversary", Operations Research 59(3), 2011, pp. 536 to 549 (reprint; neither blind checker could open it) | PR | L = λW and its conditions | 6 |
| LSM | langchain-ai/docs at f8f2328 (LangSmith pages); langsmith 0.14.11 wheel | OD | Self-hosting, OTLP, hide switches, retention, online evaluators | 9 |
| MDN | MDN Web Docs, "EventSource" (modified March 13, 2025) | OD | Six connections without HTTP/2 | 7 |
| MLF | mlflow/mlflow at 8fe044b (main, 3.17.2.dev0, not the 3.17.1 tag) | OD | Telemetry switch, OTLP, autolog | 8 |
| NGX | nginx, "Module ngx_http_proxy_module" | OD | `proxy_buffering`, `X-Accel-Buffering`, `proxy_read_timeout` | 9 |
| OAD | OpenAI developer docs: Streaming API responses; Realtime; Rate limits; Latency optimization; Batch; Pricing; gpt-6-astra model page | OD | Streaming, WebSocket and WebRTC, limits and headers, latency principles, batch limits, prices, Fast and Flex, residency, long context | 9 |
| OAS | openai/openai-python at b1a1a10 (3.35.1): response event types, stream options, WebSocket mode, admin usage, `_constants.py`. Re-checked October 26, 2026 at v3.37.0: the facts used here are unchanged | OD | Event names, usage in streams, padding, WebSocket mode, timeouts, admin key | 9 |
| OIN | Arize-ai/openinference at ca3ed46: `spec/` | OD | Attribute names; content on by default | 9 |
| OLL | ollama/ollama at 3aa41cb: `docs/api/openai-compatibility.mdx` | OD | OpenAI-compatible routes and gaps | 9 |
| OLT | openlit/openlit at 9654e6c (Python SDK 1.45.0) | OD | Content on by default; console fallback; price-list fetch | 9 |
| OPK | comet-ml/opik at b53e27c; opik 2.2.109 wheel | OD | Analytics and error-report switches; OTLP | 8 |
| OPY | OpenTelemetry Python: SDK and OTLP exporter 1.45.1 wheels; opentelemetry-python-contrib at de43f81; opentelemetry-python-genai at cb6592a; instrumentation-openai-v2 2.4b0 and util-genai 1.2b0 wheels; one local run without a collector | OD | Offline exporters, defaults, the 7.5-second block, the move, what 2.4b0 emits, the Anthropic instrumentation | 9 |
| OTS | OpenTelemetry specification at e30cae5 (maturity levels, SDK variables); opentelemetry-proto at 0976993; opentelemetry.io docs source at 2695b91 (traces, sampling, Collector) | SB | Spans, status, sampling, OTLP ports, the Collector, "Development" | 9 |
| OWS | GenAI-Security-Project/GenAI-LLM-Top10 at 9253e38 (`2026/final`); OWASP project site source at 99f4395 | SB | LLM02:2026 text; publication date | 9 |
| PHX | Arize-ai/phoenix at 57b8303 (LICENSE, `config.py`, docs); arize-phoenix-otel 0.17.2 wheel; Arize pricing page | OD, VB | Licence, telemetry switch, default host and authentication, OTLP, evaluation scope, AX free tier and retention | 9 |
| PRM | prometheus/docs at 73e9169: `practices/histograms.md` | OD | Histograms over summaries; `histogram_quantile` | 9 |
| PYPI | PyPI JSON API, October 20, 2026 | OD | Versions, licences, Python ranges | 9 |
| RFC | RFC 6455, "The WebSocket Protocol" (December 2011) | SB | What a WebSocket is | 9 |
| RTL | Ong et al., "RouteLLM", ICLR 2025 (proceedings abstract); lm-sys/RouteLLM at 0b64fda (README) | PR, OD | Routing savings and their scope | 7 |
| SCV | open-telemetry/semantic-conventions at 02e6d3e: CHANGELOG (v1.37.0), `docs/gen-ai/README.md`, git history | SB | The `gen_ai.provider.name` rename; the May 5, 2026 move | 10 |
| SSS | sysid/sse-starlette at 4632103 (3.5.0): `sse_starlette/sse.py`. Re-checked October 26, 2026 at v3.6.0: `DEFAULT_PING_INTERVAL = 15` unchanged | OD | Ping, headers, shutdown hook | 10 |
| STL | encode/starlette at dc20b21 (1.9.0): `responses.py`, `middleware/gzip.py` | OD | Disconnect detection; gzip skips SSE | 9 |
| TLP | traceloop-sdk 0.62.4 wheel; traceloop/openllmetry at 8d9c93f | OD | Content on by default; unused telemetry flag | 10 |
| UVI | encode/uvicorn at cc6fea5 (0.54.0): `config.py`, `server.py`, protocol files | OD | ASGI 2.3, timeouts, graceful shutdown | 9 |
| VLM | vllm-project/vllm at 7b569ec (main): OpenAI-compatible server docs, `envs.py` (lines 831 to 835), usage-stats docs | OD | Routes and gaps; usage statistics on by default and their switches | 9 |
| W3C | W3C Recommendation "Trace Context", November 23, 2021 | SB | `traceparent` format and the sampled flag | 9 |
| WSS | WHATWG HTML Living Standard, 9.2 "Server-sent events" (last updated October 20, 2026) | SB | Wire format, parsing rules, `EventSource`, reconnection and 204, authoring notes | 10 |
| WVE | weave 0.53.12 wheel | OD | Destination and error-report switch | 8 |

## Run on your computer

| Test | Command | Expected result |
|---|---|---|
| R1 | `python run_lab.py` | `21 of 21 checks passed` |
| R2 | `python mutation_check.py` | `48 of 48 mutations caught` |
| R3 | Section 7.4: `python -m pip install -r requirements-crosscheck.txt`, then `python crosscheck.py` | `7 of 7 cross-checks passed`, with 0 network attempts outside your computer |
| R4 | Section 7.5: `python stream_server.py` in one window, `python sse_client.py "Tell me about streaming"` in another | The answer, then the time to first token and total; send back the timings |

Send back the output; each [R] above then becomes [T] with the date.

Windows 11, Python 3.13.16, October 26, 2026: R4 gave the answer and its timings. R1 found a Windows-only fault in c20: the server's 503 to a client over the cap was lost to an aborted connection. It was fixed the same day, and R1 and R2, run by script, then gave 21 of 21 and 48 of 48 [T]. R3 waits until its pins are 14 days old (on or after November 3). Details: `engineering-stack-windows-run-2026-10-26.md` in the records folder.

## Checks run on this part

| Check | By | Result |
|---|---|---|
| Lab | `run_lab.py` on Python 3.13.16, 3.12.3 and 3.11.17 | 17 of 17 on each before the fixes; 21 of 21 on each after them, with checks c18 to c21 added for the security findings [T] |
| Mutation check | `mutation_check.py` | 32 of 32 caught before the fixes; after them, 48 deliberate breaks, 48 of 48 caught on each of the three Pythons [T] |
| Windows run | The owner typing Sections 7.1 and 7.5 on Windows 11 with Python 3.13.16, October 26, 2026; then `run_lab.py` and `mutation_check.py` by script | Before the fix, 20 of 21: c20's client over the cap got the 503 in 7 of 20 tries and otherwise `WinError 10053`, because the server closed without reading the refused request. The server now reads it first (at most 0.5 s). After that, 21 of 21 on five runs, the 503 in 20 of 20 tries, and 48 of 48 mutations caught [T]. The Linux rows above were run on the earlier code |
| Cross-check | `crosscheck.py` against FastAPI 0.156.1, uvicorn 0.54.0 and the OpenTelemetry SDK 1.45.1, on all three Pythons | 7 of 7 on each, 0 network attempts, before and after the blocker was widened to `connect_ex`, UDP and name lookups [T] |
| Worked tables | `demo.py` | Every number quoted in Sections 3, 5 and 8 came from it or from the commands shown [T] |
| Blind source check A | A separate agent that saw only 77 claims from Sections 1 to 3.6 and their sources; 34 web lookups | 64 supported, 12 partly supported, none contradicted, 1 not checkable (the Little's law paper, blocked) |
| Blind source check B | The same, for 81 claims from Section 3.7 onward; 25 web lookups | 50 supported, 22 partly supported, 3 contradicted (a FastAPI version, the worked example's daily-average arithmetic, and "prices double" for all Gemini models), 6 not checkable; all three fixed |
| Beginner test | A separate agent following Sections 6 to 9 only, as a new Linux user, on all three Pythons | Every printed number matched; 16 problems in the text (0 high, 4 medium, 12 low) |
| Security review | A separate agent testing the lab's code on 127.0.0.1 only, and reading the advice | 21 findings (2 high and 5 medium in the advice, 5 medium in the code, 8 low, 1 note); every code finding reproduced, then fixed except one low (the stand-in's prefill time still grows with prompt length, an invented timing) |
| Fixes | The lead reproduced each finding, or reopened its source, before changing anything | Findings, fixes and what was left: claude/engineering-stack-part-13-review.md |

## Cheat sheet

**Terms.** SSE: one HTTP response of text events. Span: one timed step; trace: one request's spans. `traceparent`: the header that joins them. OTLP: the wire protocol for telemetry. Content capture: recording prompts and answers in traces, opt-in. Batch API: half price, answered within a day. Little's law: open requests = arrival rate x time each takes.

**Formulas.**

```
SSE event              = field lines ("event: x", "id: 7", "data: ...") then a blank line
keep-alive             = ": ping" about every 15 s, shorter than any idle timeout on the path
open streams           = requests per second x seconds per answer          (Little's law)
request cost           = sum(tokens x price per token), x 0.5 batch, x 1.1 US-only (Anthropic)
long-context price     = OpenAI and Haiku 5.5: the whole request, once the prompt passes the line
input_tokens (GenAI)   = uncached + cache reads + cache writes
p95                    = from a histogram, never from averaging averages
```

**Facts (read October 20, 2026; check before use).**

```
FastAPI 0.156.1    EventSourceResponse built in (since 0.135.0); pings at 15 s; JSON-encodes data
nginx              proxy_buffering on by default; X-Accel-Buffering: no; proxy_read_timeout 60 s
Anthropic          error events after the 200; 529 = overloaded; spend-cap 429 has no retry-after
OpenAI             usage in response.completed; Priority renamed Fast; over 272K: 2x in, 1.5x out
Batch APIs         50% at Anthropic, OpenAI and Google; answered within 24 h (Gemini expires at 48 h)
GenAI semconv      status Development; moved May 5, 2026; content off by default
Content by default Traceloop, OpenLIT, OpenInference, Logfire: on; OpenTelemetry's own: off
LangServe          archived May 5, 2026; LangGraph Platform renamed LangSmith Deployment
```

**Decision rules.**

1. Stream to people; batch everything a person isn't waiting for.
2. Send `X-Accel-Buffering: no`, ping every 15 seconds, and measure time to first token through the real proxy.
3. A stream is done only at its last event; an `error` event or a silent stop is a failure even after a 200. Stop generating when the reader leaves.
4. Retry in one layer, with a budget, never after the first token; obey `retry-after` up to a cap; never retry a 400; a spend-cap 429 needs a person.
5. Trace every model call with the GenAI names; keep content capture off, and delete all four content attributes, `url.query`, content events and logs in the Collector too.
6. Turn off each tool's own telemetry (vLLM's too) before its first run; give a self-hosted UI authentication and a private address.
7. Price the whole request, watch for long-context lines, and size for peak with Little's law.
8. Alert on percentiles from histograms, not on means.
9. Authenticate, cap open streams and spend per key, time out slow clients, and don't trust a `traceparent` from outside.

## Appendix: lab listing

The core file of the lab folder `engineering-stack-lab-part-13`, as tested: the arithmetic and rules. The other files are in the zip (Section 8).

### shipmath.py

```python
"""shipmath: the arithmetic and rules of running a model behind an API
(Engineering Stack, Part 13).

Standard library only. Prices and rules were read from the vendors' pages on
October 20, 2026 (Part 13, Section 12); they change, so pass your own. All
money is in US dollars, kept as Fractions so the checks are exact.
"""
from __future__ import annotations

import json
import math
import re
from fractions import Fraction as F

M = 1_000_000  # prices are per million tokens

# ------------------------------------------------------------ 1. price sheets
# Per million tokens. "cache_read" and "cache_write" are what a cached prefix
# costs to read or to write. None means the page read gave no figure.
PRICES = {
    # Anthropic pricing page: Sonnet 5.5 $2 in, $10 out; cache reads 0.05x
    # and 5-minute writes 1.25x the input price (Part 04, Section 3.5).
    "claude-sonnet-5-5": dict(input=F(2), output=F(10), cache_read=F(1, 10), cache_write=F(5, 2)),
    # Haiku 5.5: $0.10 / $0.50; a prompt over 100,000 tokens (cache reads and
    # writes included) pays $0.50 / $2.50 for the whole request.
    "claude-haiku-5-5": dict(input=F(1, 10), output=F(1, 2), cache_read=None, cache_write=None),
    # OpenAI gpt-6-astra: $10 in, $1 cached, $12.50 cache write, $50 out;
    # over 272,000 input tokens: 2x input and cache rates, 1.5x output.
    "gpt-6-astra": dict(input=F(10), output=F(50), cache_read=F(1), cache_write=F(25, 2)),
    # Gemini 3.1 Pro Preview: $2 / $12 up to 200k prompt tokens, $4 / $18 above.
    "gemini-3.1-pro-preview": dict(input=F(2), output=F(12), cache_read=None, cache_write=None),
}

# Whole-request long-context rules: (threshold in prompt tokens, how the
# threshold counts tokens, multipliers or replacement prices).
LONG_CONTEXT = {
    "claude-haiku-5-5": dict(over=100_000, counts="all_input",
                             prices=dict(input=F(1, 2), output=F(5, 2))),
    "gpt-6-astra": dict(over=272_000, counts="all_input",
                        times=dict(input=F(2), cache_read=F(2), cache_write=F(2), output=F(3, 2))),
    "gemini-3.1-pro-preview": dict(over=200_000, counts="all_input",
                                   prices=dict(input=F(4), output=F(18))),
}

BATCH = F(1, 2)            # all three vendors: half price (Section 3.9)
RESIDENCY = {"anthropic-us": F(11, 10), "openai-regional": F(11, 10)}


def prompt_tokens(usage: dict) -> int:
    """All input tokens of a request: uncached, cache reads and cache writes."""
    return usage.get("input", 0) + usage.get("cache_read", 0) + usage.get("cache_write", 0)


def rates_for(model: str, usage: dict) -> dict:
    """The per-million rates that apply to this one request."""
    rates = dict(PRICES[model])
    rule = LONG_CONTEXT.get(model)
    if rule and prompt_tokens(usage) > rule["over"]:
        for key, value in rule.get("prices", {}).items():
            rates[key] = value
        for key, factor in rule.get("times", {}).items():
            if rates.get(key) is not None:
                rates[key] = rates[key] * factor
    return rates


def request_cost(model: str, usage: dict, batch: bool = False,
                 residency: str | None = None) -> F:
    """Dollars for one request. usage: input (uncached), cache_read,
    cache_write, output, in tokens. Batch and residency multiply the total."""
    rates = rates_for(model, usage)
    total = F(0)
    for key in ("input", "cache_read", "cache_write", "output"):
        tokens = usage.get(key, 0)
        if tokens:
            if rates.get(key) is None:
                raise ValueError(f"no {key} price for {model}")
            total += rates[key] * tokens / M
    if batch:
        total *= BATCH
    if residency:
        total *= RESIDENCY[residency]
    return total


def monthly(cost_per_request: F, requests_per_day: float, days: int = 30) -> F:
    return cost_per_request * F(requests_per_day).limit_denominator() * days


# ----------------------------------------------------- 2. load and latency
def concurrent(arrivals_per_second: float, seconds_in_system: float) -> float:
    """Little's law: average number in the system L = lambda x W."""
    if arrivals_per_second < 0 or seconds_in_system < 0:
        raise ValueError("rates and times are not negative")
    return arrivals_per_second * seconds_in_system


def percentile(values: list[float], q: float) -> float:
    """Nearest-rank percentile: the smallest value with at least q% at or below it."""
    if not values or not 0 < q <= 100:
        raise ValueError("need values and 0 < q <= 100")
    ordered = sorted(values)
    rank = math.ceil(q / 100 * len(ordered))
    return ordered[rank - 1]


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def stream_timing(t_request: float, chunk_times: list[float]) -> dict:
    """Time to first chunk, total time and mean gap between chunks, in seconds."""
    if not chunk_times:
        raise ValueError("no chunks")
    gaps = [b - a for a, b in zip(chunk_times, chunk_times[1:])]
    return {"time_to_first_chunk": chunk_times[0] - t_request,
            "total": chunk_times[-1] - t_request,
            "mean_gap": sum(gaps) / len(gaps) if gaps else 0.0}


# ------------------------------------------------------ 3. when to retry
MAX_WAIT = 60.0            # longest wait obeyed from a retry-after header


def retry_plan(vendor: str, status: int, headers: dict, attempt: int,
               max_retries: int = 2, base: float = 0.5, cap: float = 8.0) -> float | None:
    """Seconds to wait before retrying, or None for "don't retry".

    Rules from the vendors' pages (Part 13, Section 3.5): retry 408, 409,
    429 and 5xx (529 is Anthropic's "overloaded"); obey retry-after-ms, then
    retry-after; an Anthropic 429 with no retry-after is a spend cap and a
    retry won't succeed. A wait over MAX_WAIT seconds means give up; a value
    that is not a plain number (a date, "-5") is ignored. Otherwise the wait
    doubles from `base` up to `cap` (Part 09 adds jitter; it is left out here
    so the checks are exact).
    """
    h = {k.lower(): v for k, v in headers.items()}
    if attempt >= max_retries:
        return None
    if not (status in (408, 409, 429) or status >= 500):
        return None
    if vendor == "anthropic" and status == 429 and "retry-after" not in h \
            and "retry-after-ms" not in h:
        return None
    for name, scale in (("retry-after-ms", 1000), ("retry-after", 1)):
        value = str(h.get(name, "")).strip()
        if re.fullmatch(r"\d{1,9}(\.\d+)?", value):
            wait = float(value) / scale
            return wait if wait <= MAX_WAIT else None   # a wait that long: give up, don't hang
    return min(cap, base * 2 ** attempt)


# --------------------------------------------- 4. tracing: names and rules
TRACEPARENT = re.compile(r"^([0-9a-f]{2})-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})$")


def parse_traceparent(value: str) -> dict | None:
    """W3C Trace Context `traceparent`: version-traceid-parentid-flags.
    Returns None when invalid (all-zero IDs, version ff, wrong lengths)."""
    m = TRACEPARENT.match(value.strip())
    if not m:
        return None
    version, trace_id, parent_id, flags = m.groups()
    if version == "ff" or set(trace_id) == {"0"} or set(parent_id) == {"0"}:
        return None
    return {"trace_id": trace_id, "parent_id": parent_id,
            "sampled": bool(int(flags, 16) & 1)}


CONTENT_ATTRIBUTES = ("gen_ai.system_instructions", "gen_ai.input.messages",
                      "gen_ai.output.messages", "gen_ai.tool.definitions")


def chat_span(provider: str, model: str, usage: dict, finish_reasons: list[str],
              messages: list | None = None, output: list | None = None,
              capture_content: bool = False) -> tuple[str, dict]:
    """Span name and attributes for one model call, per the OpenTelemetry
    GenAI conventions (status Development, read October 20, 2026).

    gen_ai.usage.input_tokens counts every input token, cached ones included;
    the cache counts are reported separately as well. Prompt and answer text
    are recorded only when capture_content is True (opt-in)."""
    attrs = {
        "gen_ai.operation.name": "chat",
        "gen_ai.provider.name": provider,
        "gen_ai.request.model": model,
        "gen_ai.usage.input_tokens": prompt_tokens(usage),
        "gen_ai.usage.output_tokens": usage.get("output", 0),
        "gen_ai.response.finish_reasons": list(finish_reasons),
    }
    if usage.get("cache_read"):
        attrs["gen_ai.usage.cache_read.input_tokens"] = usage["cache_read"]
    if usage.get("cache_write"):
        attrs["gen_ai.usage.cache_write.input_tokens"] = usage["cache_write"]
    if capture_content:   # structured content goes on spans as a JSON string
        if messages is not None:
            attrs["gen_ai.input.messages"] = json.dumps(messages)
        if output is not None:
            attrs["gen_ai.output.messages"] = json.dumps(output)
    return f"chat {model}", attrs


def drop_content(attrs: dict) -> dict:
    """What a Collector's attributes processor can do before storage:
    remove prompt and answer text from a span's attributes."""
    return {k: v for k, v in attrs.items() if k not in CONTENT_ATTRIBUTES}
```
