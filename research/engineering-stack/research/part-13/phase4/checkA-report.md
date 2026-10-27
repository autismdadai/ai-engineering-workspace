# Blind source check, set A (claims A1 to A77)

Summary: 77 claims. Supported 64, partly supported 12 (A2, A6, A8, A27, A29, A36, A40, A46, A47, A53, A66, A71), contradicted 0, not checkable 1 (A14). Lookups used: 34 of 45 (WebFetch/WebSearch). Source repos read from shallow clones; short SHAs could not be fetched for llama.cpp, ollama, vllm (clones are current heads 839a572, 52f1681, 005cef0, not ead9f32, 3aa41cb, 7b569ec); opentelemetry-python read from the 1.45.1 wheels instead. Pinned commits matched for fastapi f6ce798, anthropic-sdk 2d555d1, openai-python b1a1a10, sse-starlette 4632103, starlette dc20b21, uvicorn cc6fea5, openinference ca3ed46, openlit 9654e6c, openllmetry 8d9c93f, genai conventions 547934a, GenAI-LLM-Top10 9253e38, k8s website 6df0b1b, otel spec e30cae5, otel.io 2695b91.

Abbreviations: WH = WHATWG page, AD = Anthropic docs, OD = OpenAI docs.

| Claim | Verdict | Evidence | What to change |
|---|---|---|---|
| A1 | Supported | WH 9.2: "This event stream format's MIME type is text/event-stream." | none |
| A2 | Partly supported | AD streaming: "stream... using server-sent events (SSE)". OD streaming: "over server-sent events (SSE)". Gemini api/generate-content only shows `streamGenerateContent?alt=sse` in examples and never says "server-sent events" | Add that Gemini REST needs `alt=sse`. |
| A3 | Supported | nginx proxy_module: "proxy_buffering on;"; AD errors: "an error can occur after the API returns a 200 response" | none |
| A4 | Supported | otel.io traces page (spans, root span, timing). Cost is the author's gloss, OTel traces do not record cost by themselves | optional: say cost comes from token attributes |
| A5 | Supported | genai gen-ai-spans.md: `gen_ai.response.model`, `gen_ai.usage.input_tokens`, `gen_ai.response.finish_reasons` | none |
| A6 | Partly supported | gen-ai-spans.md: "SHOULD NOT capture them by default, but SHOULD provide an option for users to opt in." OpenInference configuration.md HIDE_INPUTS default False; openlit `capture_message_content = True`; openllmetry `os.getenv(TRACELOOP_TRACE_CONTENT, "true")`; OWASP LLM02: "Observability platforms (Langfuse, LangSmith, Datadog LLM Observability) log full prompts, completions, chunks, and traces by default" | "must not" overstates; the convention says "should not ... by default". |
| A7 | Supported | AD pricing: batch "50% discount", cache hit "10% of the standard input price", `inference_geo` "1.1x multiplier"; OD pricing: "10% uplift" for regional processing; OD gpt-6-astra: >272K priced "2x input and cache rates and 1.5x output"; Gemini pricing: ">200k" tiers, "Batch API (50% cost reduction)". Gemini data-residency surcharge not found on pages read | none (Gemini residency unverified) |
| A8 | Partly supported | AD latency page defines TTFT ("time it takes for the model to generate the first token") and latency. OD latency page defines neither TTFT nor total time | Drop OAD as source for the two-number framing, or mark it as the author's framing. |
| A9 | Supported | WH 9.2 and MIME type as above | none |
| A10 | Supported | WH: EventSource "reports... last event ID string to the server when the user agent is to reestablish the connection" | none |
| A11 | Supported | RFC 6455 abstract: "enables two-way communication" | none |
| A12 | Supported | nginx: "proxy_buffering on;" default | none |
| A13 | Supported | WH authoring notes: comment line "every 15 seconds or so"; fastapi/sse.py `KEEPALIVE_COMMENT = b": ping\n\n"`, `_PING_INTERVAL = 15.0` | none |
| A14 | Not checkable | INFORMS page blocked by robots (fetch refused); paper not opened | Mark unverified or cite an openable copy. |
| A15 | Supported | prometheus/docs practices/histograms.md: histograms let you calculate "arbitrary quantiles". The definition of p95 itself is general knowledge, not in the source | none |
| A16 | Supported | otel.io traces.md (trace made of spans, root span) | none |
| A17 | Supported | traces.md span JSON: "name", "attributes", "status_code" | none |
| A18 | Supported | W3C Trace Context: four fields version, trace-id, parent-id, trace-flags, dash-delimited | none |
| A19 | Supported | opentelemetry-proto docs/specification.md: "default network port for OTLP/gRPC is 4317"; "OTLP/HTTP is 4318"; README lists logs, metrics, traces, profiles | none |
| A20 | Supported | otel.io collector/_index.md: "retries, batching, encryption or even sensitive data filtering"; transforming-telemetry.md attributes processor can "delete" | none |
| A21 | Supported | otel.io sampling/index.md: "you cannot ensure that all traces with an error within them are sampled with head sampling alone" | none |
| A22 | Supported | genai docs/gen-ai/README.md: "**Status**: Development" | none |
| A23 | Supported | gen-ai-spans.md: `gen_ai.input.messages`/`output.messages` marked `Opt-In`; "[Default] Don't record instructions, inputs, or outputs." | none |
| A24 | Supported | OD batch: "50% cost discount", "within 24 hours"; Gemini batch: "50% of the standard cost", "target turnaround time is 24 hours"; AD pricing: Batch API "50% discount". 24h window for Anthropic not seen on pages read | none |
| A25 | Supported | OD model page: ">272K input tokens ... for the full request"; Gemini: "$4.00, prompts > 200k tokens" for 3.1 Pro; AD pricing: "Haiku 5.5 ... over 100,000 tokens pays higher prices" | none (page says 272K, claim writes 272,000) |
| A26 | Supported | Microsoft Learn: "it can surface responses that are incorrect, outdated, or unsafe"; page "Last updated on 2026-08-19" | none |
| A27 | Partly supported | RouteLLM README: "reduce costs by up to 85% while maintaining 95% GPT-4 performance"; trained on gpt-4-1106-preview and mixtral pair; ICLR abstract says routers "maintain performance even when routing between LLMs not included in training" | Sources do not say savings depend on the pair; say savings were measured for a specific pair (GPT-4/Mixtral). |
| A28 | Supported | AD errors: 429 rate_limit_error, 529 "The API is temporarily overloaded." | none |
| A29 | Partly supported | llama.cpp, Ollama, vLLM docs show separate servers with own HTTP routes. Ledger P11-06 and the Gemini report quote not provided | Ledger half not checkable. |
| A30 | Supported | vLLM openai_compatible_server.md lists `/v1/chat/completions` and `/v1/responses`; llama.cpp README has both POST routes; Ollama docs have `/v1/chat/completions` and "POST /v1/responses" (read at current heads) | none |
| A31 | Supported | vLLM: "`user` parameter is ignored" (chat) and "`suffix` parameter is not supported" (completions); llama.cpp: "no strong claims of compatibility with OpenAI API spec is being made" | note: `suffix` note is under Completions, `user` under Chat. |
| A32 | Supported | Ollama: "Only the non-stateful flavor is supported"; "The OpenAI API does not have a way of setting the context size"; Modelfile `PARAMETER num_ctx` | none |
| A33 | Supported | fastapi release notes "0.135.0 (2026-03-01)" "Add support for Server Sent Events"; docs "set `response_class=EventSourceResponse`" and `yield` | minor: you set it as response_class and yield, not "return" it. |
| A34 | Supported | routing.py: `Cache-Control` "no-cache", `X-Accel-Buffering` "no"; ping via `anyio.fail_after(_PING_INTERVAL)` on idle | none |
| A35 | Supported | SSE tutorial: "The `data` field is always encoded as JSON... use `raw_data` instead" | none |
| A36 | Partly supported | Release notes 0.143.0 (2026-10-08): "Automatic OpenTelemetry exporter setup is now opt-in... `FASTAPI_OTEL_AUTO_CONFIGURE=true`". Native OTel support was added in 0.142.0 (2026-09-29) | Say spans since 0.142.0; 0.143.0 made exporter setup opt-in. |
| A37 | Supported | oauth2-jwt.md: "Install `PyJWT`", pwdlib with "Argon2"; no limiter found by grep in fastapi/ and docs (absence) | none |
| A38 | Supported | langserve repo: "deprecated since Nov 18, 2024"; "archived by the owner on May 5, 2026" | none |
| A39 | Supported | langchain.com/langsmith/deployment: "renamed to LangSmith Deployment as of October 2025"; pricing: Enterprise lists "Self-hosted and hybrid deployment options", only plan; PyPI langgraph-api license "Elastic-2.0" | none (source-available is the author's gloss) |
| A40 | Partly supported | k8s multi-tenancy.md: "there is no single definition that will apply to all users. Rather, 'hardness' or 'softness' is better understood as a broad spectrum"; "Sandboxing is often recommended when you are running untrusted code"; shared kernel text | "no single definition" and "broad spectrum" are about the hard/soft terms, not tenant isolation itself; "often recommended" not "recommends". |
| A41 | Supported | WH header: "Last Updated 20 October 2026", section 9.2 | none |
| A42 | Supported | WH: "any pending data must be discarded" at end of file | none |
| A43 | Supported | WH: "Legacy proxy servers are known to, in certain cases, drop HTTP connections after a short timeout."; nginx: "proxy_read_timeout 60s"; "only between two successive read operations" | none |
| A44 | Supported | fastapi `_PING_INTERVAL = 15.0`; sse-starlette `DEFAULT_PING_INTERVAL = 15` | none |
| A45 | Supported | RFC 6455: "handshake is an HTTP Upgrade request"; two-way | none |
| A46 | Partly supported | Same as A2 (Gemini needs `alt=sse`) | as A2 |
| A47 | Partly supported | OD realtime: "The session connects over WebRTC in the browser or WebSocket on the server."; openai-python beta_response_steer_event.py `type: Literal["response.steer"]`, "Queues user input to steer a response on this WebSocket connection" | 3.35.1 changelog is a single bug fix, so it did not "add" the mode; say "has". Steer type sits under `beta`. |
| A48 | Supported | MDN: "per browser + domain", "set to a very low number (6)", "(from Stack Overflow)", HTTP/2 "defaults to 100" | none |
| A49 | Supported | WH: "might run into trouble when opening multiple pages from a site" | none |
| A50 | Supported | starlette responses.py `stream_response` sends each chunk; gzip.py excludes `"text/event-stream"` by default | none |
| A51 | Supported | nginx: X-Accel-Buffering "yes" or "no"; "can be disabled using the proxy_ignore_headers" | none |
| A52 | Supported | WH: buffering "can cause delays in event dispatch" | none |
| A53 | Partly supported | sse-starlette sse.py sets `Cache-Control` via `setdefault("Cache-Control", "no-store")` and `X-Accel-Buffering: no`; FastAPI sets `no-cache` | sse-starlette uses `no-store`, not `no-cache`. |
| A54 | Supported | AD streaming: "overloaded_error, which would normally correspond to an HTTP 529" | none |
| A55 | Supported | openai-python types/responses: response_failed_event.py, response_incomplete_event.py, response_error_event.py | none |
| A56 | Supported | `Response.usage` in response_completed; chat stream options: "If the stream is interrupted, you may not receive the final usage" | none |
| A57 | Supported | AD streaming: "usage field of the message_delta event are cumulative" | none |
| A58 | Supported | Gemini reference: "stream of GenerateContentResponse instances"; "usageMetadata": "Metadata on the generation requests' token usage."; no statement on which chunk | none |
| A59 | Supported | AD streaming: Claude 4.5 and earlier "partial assistant response as the beginning of a new assistant message"; 4.6 and later "add a user message that instructs the model to continue" | none |
| A60 | Supported | starlette responses.py: `spec_version >= (2, 4)` takes the no-listener path, else `listen_for_disconnect` on `http.disconnect`; uvicorn h11/httptools `"spec_version": "2.3"`, `__version__ = "0.54.0"` | none |
| A61 | Supported | uvicorn main.py `--timeout-graceful-shutdown` `default=None`; sse-starlette `_shutdown_watcher` | none |
| A62 | Supported | both `_constants.py`: `timeout=600, connect=5.0`, `DEFAULT_MAX_RETRIES = 2`; versions 3.35.1 / 1.16.0 | none |
| A63 | Supported | anthropic `_base_client.py` raises "Streaming is required for operations that may take longer than 10 minutes" from an estimate on max_tokens | none |
| A64 | Supported | both `_constants.py`: `import httpx2`; pyproject `httpx2>=...` | none |
| A65 | Supported | AD rate limits: "RPM... ITPM... OTPM for each model class"; "For most Claude models, only uncached input tokens count toward your ITPM" | none |
| A66 | Partly supported | AD rate limits: "Not every 429 carries it; the spend-cap 429 never does." | "comes with retry-after" is too broad; add "usually". |
| A67 | Supported | AD rate limits: "Start, Build, and Scale tiers carries a monthly spend cap"; Custom none; errors: "A tier spend-cap 429 has no `retry-after` header" | none |
| A68 | Supported | OD rate limits: RPM/RPD/TPM/TPD; `x-ratelimit-limit-requests`; "Treat this value as a minimum" | none |
| A69 | Supported | `_base_client.py`: `retry-after-ms` first, then `retry-after`; retries 408, 409, 429, >=500 | none |
| A70 | Supported | PyPI: slowapi MIT; fastapi-limiter Apache-2.0; limits MIT | none |
| A71 | Partly supported | W3C: example "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"; sampled bit: "denotes that the caller may have recorded trace data" | "says the caller sampled it" should be "the caller may have recorded it". |
| A72 | Supported | proto specification as A19 | none |
| A73 | Supported | otel.io collector page (retries, batching, filtering) plus attributes processor "delete"; tail sampling processor in scaling.md | none |
| A74 | Supported | sampling/index.md quote; tail sampling "difficult to implement", "Always sampling traces that contain an error", "overall latency" | none |
| A75 | Supported | 1.45.1 wheel: `InMemorySpanExporter`, `ConsoleSpanExporter`, `OTEL_SDK_DISABLED`; local run printed `'service.name': 'unknown_service:python'` | none |
| A76 | Supported | I reproduced it (SDK 1.45.1, SimpleSpanProcessor to 127.0.0.1:4318, nothing listening): 7.74 s and 6.69 s per span, retry messages, then "Failed to export spans batch due to timeout, max retries or shutdown." and no crash | "about 7.5 s" is within run-to-run spread (6.7 to 7.7). |
| A77 | Supported | wheel: `_DEFAULT_SCHEDULE_DELAY_MILLIS = 5000` in BatchSpanProcessor | none |

Not reached: nothing skipped except A14 (paper behind a block), the Gemini data-residency surcharge, the ledger entries P11-03/04/06, and the exact commits of llama.cpp, ollama and vllm (read at current heads). Page text addressed to AI agents: none seen.
