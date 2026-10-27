# Claims to check, set A

A1. The common way to do it over plain HTTP is Server-Sent Events (SSE): one long response made of small text events .
   Sources: WSS

A2. Every big vendor streams this way .
   Sources: AND, GMD, OAD

A3. Two surprises: anything between your server and the reader can hold the pieces back and deliver them in one lump (nginx does by default) , and once streaming has started the status code is already "200 OK", so an error has to arrive as an event inside the stream .
   Sources: AND, NGX

A4. T29, observability and tracing. A trace is a timeline of one request: the web call, the model call inside it, each tool the agent ran, with how long each took and what it cost .
   Sources: OTS

A5. OpenTelemetry is the open standard for recording traces, and it has conventions for AI calls: names for the model, the token counts and the finish reason .
   Sources: GAI

A6. The conventions say prompts and answers must not be recorded unless you switch that on ; several popular tracing tools record them by default , and OWASP's 2026 list calls out observability platforms for exactly this .
   Sources: GAI, OIN, OLT, OWS, TLP

A7. T30, cost and latency. You pay per token, input and output at different prices, with discounts for cached input and for batch jobs, and surcharges for very long prompts or for keeping data in one country .
   Sources: AND, GMD, OAD

A8. Speed has two numbers: how soon the first words appear and how long the whole answer takes .
   Sources: AND, OAD

A9. | One long HTTP response made of small text events | Server-Sent Events (SSE); `text/event-stream` | WHATWG HTML standard, section 9.2  |
   Sources: WSS

A10. | The browser object that reads SSE and reconnects | `EventSource` | Sends `Last-Event-ID` when it reconnects  |
   Sources: WSS

A11. | A two-way connection that stays open | WebSocket | RFC 6455  |
   Sources: RFC

A12. | A proxy holding a response back before passing it on | Response buffering | nginx: on by default  |
   Sources: NGX

A13. | A line that keeps an idle stream open | Keep-alive comment | `: ping`, every 15 seconds or so  |
   Sources: FAS, WSS

A14. | How many requests are open at once | Concurrency | Little's law: L = λW  |
   Sources: LIT

A15. | The value that 95% of measurements are at or below | 95th percentile, p95 | Use histograms to compute it  |
   Sources: PRM

A16. | A timeline of one request | Trace | Made of spans  |
   Sources: OTS

A17. | One timed step inside a trace | Span | Has a name, attributes, a status  |
   Sources: OTS

A18. | The header that joins spans across services | `traceparent` (W3C Trace Context) | `version-traceid-parentid-flags`  |
   Sources: W3C

A19. | The wire protocol for traces, metrics and logs | OTLP | Ports 4317 (gRPC) and 4318 (HTTP)  |
   Sources: OTS

A20. | A program that receives, filters and forwards telemetry | OpenTelemetry Collector | Can drop attributes before storage  |
   Sources: OTS

A21. | Keeping only some traces | Sampling (head or tail) | Head sampling can't promise to keep every error  |
   Sources: OTS

A22. | Agreed names for AI telemetry | OpenTelemetry GenAI semantic conventions | Status Development  |
   Sources: GAI

A23. | Recording prompts and answers in traces | Content capture | Off by default in the conventions  |
   Sources: GAI

A24. | Half-price jobs answered within a day | Batch API | All three big vendors  |
   Sources: AND, GMD, OAD

A25. | A higher price for the whole request past a length | Long-context pricing | OpenAI over 272,000 tokens; Gemini 3.1 Pro over 200,000; Haiku 5.5 over 100,000  |
   Sources: AND, GMD, OAD

A26. | Reusing a stored answer for a similar question | Semantic caching | Can return wrong or stale answers  |
   Sources: AZS

A27. | Sending easy requests to a cheaper model | Model routing | Savings depend on the model pair  |
   Sources: RTL

A28. | A limit on requests or tokens per minute | Rate limit; HTTP 429 | Anthropic also returns 529 when overloaded  |
   Sources: AND

A29. The Gemini report's advice to "separate the web server from the heavy inference engine" holds: the serving engines of Part 11 are separate programs with their own HTTP APIs (ledger P11-06) .
   Sources: LCP, OLL, VLM

A30. OpenAI-compatible, mostly. vLLM, llama.cpp's server and Ollama each offer `/v1/chat/completions`, and newer releases also `/v1/responses`, so one client library can talk to all of them .
   Sources: LCP, OLL, VLM

A31. The match isn't complete. vLLM ignores the `user` parameter and doesn't support `suffix` . llama.cpp says "no strong claims of compatibility with OpenAI API spec is being made" .
   Sources: LCP, VLM

A32. Ollama's `/v1/responses` is "non-stateful" only and can't set the context size through the OpenAI API; that takes a `num_ctx` setting in a Modelfile .
   Sources: OLL

A33. FastAPI changed in 2026. It now has its own SSE support, since 0.135.0 (March 1, 2026): return `EventSourceResponse` and yield events .
   Sources: FAS

A34. It sends a `: ping` comment after 15 seconds of silence and sets `Cache-Control: no-cache` and `X-Accel-Buffering: no` for you .
   Sources: FAS

A35. One trap: it JSON-encodes `data`, so `data="hello"` goes out as `data: "hello"`, with the quotes; use `raw_data` for plain text .
   Sources: FAS

A36. Since 0.143.0 (October 8, 2026), FastAPI also creates OpenTelemetry spans by itself when you give it a tracer provider, and sets up exporters from `OTEL_` variables only if you opt in with `FASTAPI_OTEL_AUTO_CONFIGURE=true` .
   Sources: FAS

A37. Its security tutorial now uses PyJWT and Argon2 password hashing (pwdlib); it has no built-in rate limiter .
   Sources: FAS

A38. LangServe is gone. Deprecated since November 18, 2024 and archived on May 5, 2026 (ledger P11-04) .
   Sources: LCS

A39. Its suggested successor, LangGraph Platform, was renamed LangSmith Deployment in October 2025; LangChain's pricing page lists self-hosting only on its Enterprise plan, and the `langgraph-api` server package is under the Elastic License 2.0, which is source-available, not open source .
   Sources: LCS, PYPI

A40. Kubernetes' own page treats tenant isolation as "a broad spectrum" with "no single definition", lists the tools (namespaces, access control, quotas, network policies, sandboxed containers, dedicated nodes) and recommends sandboxing "when you are running untrusted code", because ordinary containers share the host's kernel .
   Sources: K8S

A41. The format (WHATWG HTML, section 9.2, last updated October 20, 2026) .
   Sources: WSS

A42. Text after the last blank line is thrown away when the stream ends .
   Sources: WSS

A43. Why the 15-second ping. The spec's authoring notes warn that "legacy proxy servers are known to, in certain cases, drop HTTP connections after a short timeout" and suggest a comment line "every 15 seconds or so" . nginx's `proxy_read_timeout` is 60 seconds by default, counted between two reads, so a model that thinks quietly for longer than that is cut off unless something is sent .
   Sources: NGX, WSS

A44. FastAPI and sse-starlette both ping every 15 seconds by default .
   Sources: FAS, SSS

A45. A WebSocket upgrades the connection to a two-way channel (RFC 6455) .
   Sources: RFC

A46. For a text answer, SSE is enough, and every big vendor's text API streams with it .
   Sources: AND, GMD, OAD

A47. WebSockets earn their place where both sides talk at once: OpenAI's Realtime API uses WebRTC in browsers and WebSocket on servers, and the openai SDK 3.35.1 adds a persistent WebSocket mode for the Responses API that accepts `response.steer` events while an answer is being written .
   Sources: OAD, OAS

A48. Many tabs. Over HTTP/1.1, browsers allow about six connections per site, shared by all tabs, so a page that opens one stream per tab can stall; MDN gives the figure of six (citing a Stack Overflow answer rather than a standard) and says HTTP/2 raises it, by default to 100 streams .
   Sources: MDN

A49. The spec itself only says clients with per-server limits "might run into trouble" .
   Sources: WSS

A50. Starlette's `StreamingResponse` sends each yielded piece; its gzip middleware leaves `text/event-stream` alone by default .
   Sources: STL

A51. Reverse proxies. nginx buffers proxied responses by default (`proxy_buffering on`); a response header `X-Accel-Buffering: no` turns it off for that one response, unless the proxy is configured to ignore that header .
   Sources: NGX

A52. The spec's own warning: buffering "can cause delays in event dispatch" .
   Sources: WSS

A53. What to do. Send `X-Accel-Buffering: no` and `Cache-Control: no-cache` (FastAPI and sse-starlette do) ; configure your own proxy for the streaming route; ping more often than the shortest idle timeout on the path; and measure time to first token from the reader's side, through the real network, not only on the server.
   Sources: FAS, SSS

A54. Anthropic sends `event: error` with, for example, `overloaded_error`, which "would normally correspond to an HTTP 529" .
   Sources: AND

A55. OpenAI's Responses stream has `response.failed`, `response.incomplete` and `error` events .
   Sources: OAS

A56. Usage is at the end. OpenAI's Responses stream carries token counts in `response.completed`; Chat Completions streams send usage only if you ask for `stream_options.include_usage`, and warn "If the stream is interrupted, you may not receive the final usage chunk" .
   Sources: OAS

A57. Anthropic's `message_delta` events carry cumulative usage .
   Sources: AND

A58. Gemini streams `GenerateContentResponse` objects with `usageMetadata`; which chunk carries the final counts wasn't stated on the pages read .
   Sources: GMD

A59. Resuming. Anthropic's advice now differs by model: for Claude 4.5 and earlier, send the partial answer back as the start of the assistant's turn; for Claude 4.6 and later, add a user message asking the model to continue from where it stopped .
   Sources: AND

A60. Starlette notices a disconnect by listening for the ASGI `http.disconnect` message, and stops the generator ; under uvicorn 0.54.0, which reports ASGI version 2.3, that listener is the path used .
   Sources: STL, UVI

A61. Shutdown. uvicorn's `--timeout-graceful-shutdown` has no default limit, so a long open stream can hold a deploy; sse-starlette hooks shutdown to end its streams .
   Sources: SSS, UVI

A62. SDK defaults. The openai 3.35.1 and anthropic 1.16.0 Python SDKs wait up to 600 seconds per request (5 seconds to connect) and retry twice .
   Sources: ANS, OAS

A63. The anthropic SDK refuses a non-streaming call it estimates will take over 10 minutes, saying "Streaming is required for operations that may take longer than 10 minutes" .
   Sources: ANS

A64. Both now use `httpx2`, a newer HTTP library, not `httpx` .
   Sources: ANS, OAS

A65. - Anthropic limits requests, input tokens and output tokens per minute per model class, and for most models only uncached input counts toward the input limit .
   Sources: AND

A66. A 429 is your organization's limit and comes with `retry-after`; a 529 means the platform as a whole is overloaded .
   Sources: AND

A67. Its tiers are now Start, Build, Scale and Custom, with monthly spend caps, and "A tier spend-cap 429 has no `retry-after` header": retrying won't help until the cap is raised .
   Sources: AND

A68. - OpenAI limits requests and tokens per minute and per day; its headers are `x-ratelimit-limit-requests`, `x-ratelimit-remaining-tokens` and so on, and `Retry-After` is to be treated "as a minimum" .
   Sources: OAD

A69. - The SDKs read `retry-after-ms` before `retry-after` (anthropic) and retry 408, 409, 429 and server errors (Part 09) .
   Sources: ANS

A70. FastAPI has no built-in limiter; slowapi (MIT), fastapi-limiter (Apache-2.0) and limits (MIT) are common choices .
   Sources: FAS, PYPI

A71. Spans in different services join one trace through the W3C `traceparent` header: `00-` then a 32-hex-digit trace ID, a 16-digit parent span ID and two flag digits, for example `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`, whose last bit says the caller sampled it .
   Sources: W3C

A72. Telemetry travels as OTLP, to port 4317 (gRPC) or 4318 (HTTP) .
   Sources: OTS

A73. A Collector sitting beside your service can batch, retry, sample and delete attributes before anything is stored .
   Sources: OTS

A74. Head sampling decides at the start, cheaply, so it "cannot ensure that all traces with an error within them are sampled"; tail sampling decides after the trace ends, for example keeping all errors and slow requests, and is harder to run .
   Sources: OTS

A75. Running it offline. The Python SDK 1.45.1 has an in-memory exporter for tests and a console exporter; `OTEL_SDK_DISABLED=true` switches everything off, and with no service name the resource says `unknown_service:python` .
   Sources: OPY

A76. One researcher's run found that a `SimpleSpanProcessor` exporting to an OTLP endpoint with no collector listening blocked the calling thread for about 7.5 seconds per span while it retried, then logged a failure without crashing .
   Sources: OPY

A77. Use `BatchSpanProcessor` in a request path; it queues spans and exports every 5 seconds by default .
   Sources: OPY


# Sources

| Key | Source | Class | Used for | Grade |
|---|---|---|---|---|
| AND | Anthropic docs: Streaming messages; Errors; Rate limits; Usage and Cost API; Pricing; Reducing latency; Batch processing | OD | Event types, mid-stream errors, resuming, 429 and 529, tiers and spend caps, admin reports, prices, residency, fast mode, latency levers, batch limits | 9 |
| ANS | anthropics/anthropic-sdk-python at 2d555d1 (1.16.0): `_constants.py`, `_base_client.py`, `types/usage.py` | OD | Timeouts, retries, the 10-minute rule, usage fields | 10 |
| AZS | Microsoft Learn, Azure API Management `llm-semantic-cache-lookup` policy (updated 2026-08-19) | OD | Semantic caching's risks and per-user caches | 8 |
| FAS | fastapi/fastapi at f6ce798 (0.156.1): `fastapi/sse.py`, `routing.py`, `applications.py`, `telemetry/`, release notes, security tutorial | OD | Built-in SSE, ping, headers, JSON-encoded data, telemetry opt-in, PyJWT and pwdlib, no rate limiter | 10 |
| GAI | open-telemetry/semantic-conventions-genai at 547934a (2026-10-18): `docs/gen-ai/` (client-inference, gen-ai-spans, gen-ai-agent-spans, gen-ai-metrics, gen-ai-token-metrics, mcp), `changelog.d/` | SB | Status, span names, attributes, content rule, metrics and renames | 10 |
| GMD | Google AI for Developers: API reference "Generating content"; Batch API (updated 2026-09-17); Pricing | OD | `streamGenerateContent`, usage fields, batch limits, prices | 8 |
| K8S | kubernetes/website at 6df0b1b: `concepts/security/multi-tenancy.md` | OD | Ledger P11-03 | 9 |
| LCP | ggml-org/llama.cpp at ead9f32: `tools/server/README.md` | OD | OpenAI-style routes and the compatibility disclaimer | 9 |
| LCS | langchain-ai/langserve repository page; LangChain's LangSmith Deployment page and pricing page | OD, VB | Archived May 5, 2026; the rename; Enterprise self-hosting | 8 |
| LIT | Little, "Little's Law as Viewed on Its 50th Anniversary", Operations Research 59(3), 2011, pp. 536 to 549 (reprint) | PR | L = λW and its conditions | 8 |
| MDN | MDN Web Docs, "EventSource" (modified March 13, 2025) | OD | Six connections without HTTP/2 | 7 |
| NGX | nginx, "Module ngx_http_proxy_module" | OD | `proxy_buffering`, `X-Accel-Buffering`, `proxy_read_timeout` | 9 |
| OAD | OpenAI developer docs: Streaming API responses; Realtime; Rate limits; Latency optimization; Batch; Pricing; gpt-6-astra model page | OD | Streaming, WebSocket and WebRTC, limits and headers, latency principles, batch limits, prices, Fast and Flex, residency, long context | 9 |
| OAS | openai/openai-python at b1a1a10 (3.35.1): response event types, stream options, WebSocket mode, admin usage, `_constants.py` | OD | Event names, usage in streams, padding, WebSocket mode, timeouts, admin key | 9 |
| OIN | Arize-ai/openinference at ca3ed46: `spec/` | OD | Attribute names; content on by default | 9 |
| OLL | ollama/ollama at 3aa41cb: `docs/api/openai-compatibility.mdx` | OD | OpenAI-compatible routes and gaps | 9 |
| OLT | openlit/openlit at 9654e6c (Python SDK 1.45.0) | OD | Content on by default; console fallback; price-list fetch | 9 |
| OPY | OpenTelemetry Python: SDK and OTLP exporter 1.45.1 wheels; opentelemetry-python-contrib at de43f81; opentelemetry-python-genai at cb6592a; instrumentation-openai-v2 2.4b0 and util-genai 1.2b0 wheels; one local run without a collector | OD | Offline exporters, defaults, the 7.5-second block, the move, what 2.4b0 emits, the Anthropic instrumentation | 9 |
| OTS | OpenTelemetry specification at e30cae5 (maturity levels, SDK variables); opentelemetry-proto at 0976993; opentelemetry.io docs source at 2695b91 (traces, sampling, Collector) | SB | Spans, status, sampling, OTLP ports, the Collector, "Development" | 9 |
| OWS | GenAI-Security-Project/GenAI-LLM-Top10 at 9253e38 (`2026/final`); OWASP project site source at 99f4395 | SB | LLM02:2026 text; publication date | 9 |
| PRM | prometheus/docs at 73e9169: `practices/histograms.md` | OD | Histograms over summaries; `histogram_quantile` | 9 |
| PYPI | PyPI JSON API, October 20, 2026 | OD | Versions, licences, Python ranges | 9 |
| RFC | RFC 6455, "The WebSocket Protocol" (December 2011) | SB | What a WebSocket is | 9 |
| RTL | Ong et al., "RouteLLM", ICLR 2025 (proceedings abstract); lm-sys/RouteLLM at 0b64fda (README) | PR, OD | Routing savings and their scope | 7 |
| SSS | sysid/sse-starlette at 4632103 (3.5.0): `sse_starlette/sse.py` | OD | Ping, headers, shutdown hook | 10 |
| STL | encode/starlette at dc20b21 (1.9.0): `responses.py`, `middleware/gzip.py` | OD | Disconnect detection; gzip skips SSE | 9 |
| TLP | traceloop-sdk 0.62.4 wheel; traceloop/openllmetry at 8d9c93f | OD | Content on by default; unused telemetry flag | 10 |
| UVI | encode/uvicorn at cc6fea5 (0.54.0): `config.py`, `server.py`, protocol files | OD | ASGI 2.3, timeouts, graceful shutdown | 9 |
| VLM | vllm-project/vllm at 7b569ec (main): OpenAI-compatible server docs, `envs.py`, usage-stats docs | OD | Routes and gaps; usage statistics on by default | 9 |
| W3C | W3C Recommendation "Trace Context", November 23, 2021 | SB | `traceparent` format and the sampled flag | 9 |
| WSS | WHATWG HTML Living Standard, 9.2 "Server-sent events" (last updated October 20, 2026) | SB | Wire format, parsing rules, authoring notes | 10 |
