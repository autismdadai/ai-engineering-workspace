# A: APIs and streaming (T28), cost and latency (T30)

Topic group: T28 APIs and streaming, T30 cost and latency, for a reader putting a model behind their own web API.
Date: 2026-10-20. Web lookups used: 36 of 40 (WebSearch plus WebFetch, including one fetch that only returned a redirect and one that returned an overview page).

Repositories cloned (depth 1) under /home/claude/part13/research/a/, read at these commits:
- fastapi/fastapi f6ce798fa2d51d0f477b99cf40fda6f97cff7a2e (`__version__ = "0.156.1"`)
- sysid/sse-starlette 463210322ccfc208572c1703c27939d68fe9f21f (3.5.0)
- encode/starlette dc20b216f065af3a487722141da9a29dcac388d1 (1.9.0)
- encode/uvicorn cc6fea5b40ad559f7ca358a24b1a521451232281 (0.54.0)
- openai/openai-python b1a1a100d38d84dd556319e207880d85d23559cd (3.35.1)
- anthropics/anthropic-sdk-python 2d555d1416344a44af9322c88cb04b75df9c878d (1.16.0)
- googleapis/python-genai 4c1abccf258c9247218e66610790043893cd6950 (2.31.0)
- ollama/ollama 3aa41cbdc3cc49bbed816b12617257223813a37e (main, not a release tag)
- vllm-project/vllm 7b569ec8953cf8099638a6d2ee1e915b75867c3a (main, commit dated 2026-10-20; sparse: docs, vllm/envs.py, vllm/usage)
- ggml-org/llama.cpp ead9f3205848f81ca079b4e760b76a01a6359f4b (main; sparse: docs, tools/server/README.md)
- lm-sys/RouteLLM 0b64fdafe049e596a3f5657c219329f24af24198
- kubernetes/website 6df0b1bb954d774cf01fd539e4b66cfe80cdf62f (sparse: content/en/docs/concepts/security/multi-tenancy.md; commit dated 2026-10-20)

PyPI JSON read from the shell (not counted as lookups): slowapi 0.1.10 (MIT), fastapi-limiter 0.2.0 (Apache-2.0), limits 5.8.0 (MIT), pyjwt 2.15.1 (MIT, uploaded 2026-09-28), pwdlib 0.3.1 (MIT), python-jose 3.5.0 (MIT, last upload 2025-05-28), routellm 0.2.0 (2024-07-08), langgraph-cli 0.4.37 (MIT), langgraph-api 0.16.2 (Elastic-2.0, uploaded 2026-10-20).

## Claims

| ID | Claim | Source key | Class | Place | Quote | Scope and date | Conf. |
|---|---|---|---|---|---|---|---|
| A1 | The SSE stream's MIME type is `text/event-stream` and it must be UTF-8. | WHATWG-SSE | SB | 9.2 Server-sent events, event stream format | "Event streams in this format must always be encoded as UTF-8." | HTML Living Standard, last updated 20 Oct 2026 | 9 |
| A2 | Fields are `event`, `data`, `id`, `retry`; a line starting with a colon is ignored (a comment); a blank line dispatches the event. | WHATWG-SSE | SB | Interpreting an event stream | "If the line starts with a U+003A COLON character (:)" ... "Ignore the line." | same | 9 |
| A3 | The spec gives no fixed default reconnection time; it is implementation-defined, "probably" a few seconds; `retry:` overrides it. | WHATWG-SSE | SB | EventSource processing model | "implementation-defined value, probably in the region of a few seconds" | same | 9 |
| A4 | On reconnect the browser reports the last event ID in the `Last-Event-ID` request header. | WHATWG-SSE | SB | The Last-Event-ID header | "reports an EventSource object's last event ID string to the server" | same | 9 |
| A5 | The spec's authoring notes warn that legacy proxies drop idle connections and suggest a comment line about every 15 seconds. | WHATWG-SSE | SB | Authoring notes | "include a comment line (one starting with a ':' character) every 15 seconds or so" | same | 9 |
| A6 | The spec itself says buffering can delay event dispatch, and HTTP chunking can hurt reliability. This settles P11-02: SSE does not guarantee delivery "the exact moment" tokens are generated. | WHATWG-SSE | SB | Authoring notes | "block buffering or line buffering ... can cause delays in event dispatch" | same | 9 |
| A7 | The spec warns that clients with per-server connection limits "might run into trouble" with many SSE connections. | WHATWG-SSE | SB | Authoring notes | "Clients that support HTTP's per-server connection limitation might run into trouble" | same | 8 |
| A8 | MDN: without HTTP/2, browsers cap SSE at 6 open connections per browser plus domain (across tabs); with HTTP/2 the stream limit is negotiated, default 100. | MDN-ES | OD | EventSource, warning box | "set to a very low number (6)" | MDN page last modified 13 Mar 2025; the "6" is attributed by MDN to Stack Overflow, not to a spec | 7 |
| A9 | nginx buffers proxied responses by default (`proxy_buffering on`); with buffering off the response passes to the client as received. | NGINX-PROXY | OD | ngx_http_proxy_module, proxy_buffering | "When buffering is disabled, the response is passed to a client synchronously" | nginx docs read 2026-10-20 | 9 |
| A10 | nginx honours an `X-Accel-Buffering: no` response header to switch buffering off per response, unless `proxy_ignore_headers` disables it. | NGINX-PROXY | OD | proxy_buffering | "passing “yes” or “no” in the “X-Accel-Buffering” response header field" | same | 9 |
| A11 | nginx `proxy_read_timeout` defaults to 60 s, measured between two reads, not for the whole response; so a silent stream longer than 60 s is cut unless pings are sent. | NGINX-PROXY | OD | proxy_read_timeout | "set only between two successive read operations" | same | 9 |
| A12 | FastAPI has built-in SSE since 0.135.0 (2026-03-01): `fastapi.sse.EventSourceResponse` and `ServerSentEvent`. | FASTAPI-SRC | OD | docs/en/docs/release-notes.md, "## 0.135.0 (2026-03-01)"; fastapi/sse.py:20 | "Add support for Server Sent Events." | fastapi 0.156.1 | 10 |
| A13 | FastAPI's SSE encoder JSON-encodes `data` (strings get quotes); `raw_data` sends text as is; `event` and `id` must be one line; `retry` is milliseconds. | FASTAPI-SRC | OD | fastapi/sse.py:52 to 134 | "All `data` values **including plain strings** are JSON-serialized." | 0.156.1 | 10 |
| A14 | FastAPI SSE sends a `: ping` comment after 15 s of silence and sets `Cache-Control: no-cache` and `X-Accel-Buffering: no`. | FASTAPI-SRC | OD | fastapi/sse.py:237 to 241; fastapi/routing.py:635 to 684 | "# For Nginx proxies to not buffer server sent events" | 0.156.1 | 10 |
| A15 | FastAPI SSE works with any HTTP method, including POST (for MCP-style streaming). | FASTAPI-SRC | OD | fastapi/sse.py:26 | "Works with **any HTTP method** (`GET`, `POST`, etc.)" | 0.156.1 | 10 |
| A16 | Starlette's `StreamingResponse` detects disconnects two ways: if the server reports ASGI spec_version 2.4 or later, an `OSError` on send becomes `ClientDisconnect`; otherwise a task listens for `http.disconnect` and cancels the stream. | STARLETTE-SRC | OD | starlette/responses.py:247 to 285 | `if message["type"] == "http.disconnect":` | starlette 1.9.0 | 9 |
| A17 | uvicorn 0.54.0 reports ASGI `spec_version` "2.3", so under uvicorn Starlette uses the listener-task path. | UVICORN-SRC | OD | uvicorn/protocols/http/h11_impl.py:209, httptools_impl.py:227 | `"spec_version": "2.3"` | uvicorn 0.54.0 | 9 |
| A18 | Starlette's `GZipMiddleware` excludes `text/event-stream` by default, so gzip does not buffer SSE out of the box (minimum_size 500 bytes for other types). | STARLETTE-SRC | OD | starlette/middleware/gzip.py:26, 49 | `"text/event-stream",` | 1.9.0 | 9 |
| A19 | sse-starlette 3.5.0 `EventSourceResponse` defaults: ping every 15 s (0 disables), `send_timeout=None`, separator `\r\n`, headers `Cache-Control: no-store` (overridable), `Connection: keep-alive`, `X-Accel-Buffering: no`. | SSE-STARLETTE-SRC | OD | sse_starlette/sse.py:248 to 321 | "ping: Ping interval in seconds. Default: 15. Set to 0 to disable" | 3.5.0, BSD-3-Clause | 10 |
| A20 | sse-starlette keeps its own disconnect listener on purpose (to call `client_close_handler_callable` and stop pings) and hooks uvicorn shutdown to end streams; it warns streams can hang shutdown if that is disabled. | SSE-STARLETTE-SRC | OD | sse_starlette/sse.py:1 to 17, 194 to 201 | "server will hang indefinitely (or until uvicorn's graceful shutdown timeout expires)" | 3.5.0 | 9 |
| A21 | uvicorn defaults: `--timeout-keep-alive 5` s, `--timeout-graceful-shutdown` none (no limit), `--timeout-worker-healthcheck 5`, `ws_ping_timeout` 20 s. | UVICORN-SRC | OD | uvicorn/config.py:209, 233 to 236; main.py:307 to 312 | "Maximum number of seconds to wait for graceful shutdown." | 0.54.0 | 9 |
| A22 | With no graceful-shutdown timeout uvicorn waits for all tasks; with one set, it cancels running tasks when it expires. | UVICORN-SRC | OD | uvicorn/server.py:296 to 304 | "Cancel %s running task(s), timeout graceful shutdown exceeded" | 0.54.0 | 8 |
| A23 | FastAPI 0.156.1 includes native OpenTelemetry spans, metrics and logs (on by default, using whatever providers exist); automatic OTLP exporter setup is opt-in since 0.143.0 via `FASTAPI_OTEL_AUTO_CONFIGURE=true`. No phone-home found. | FASTAPI-SRC | OD | fastapi/applications.py:1011 to 1024; telemetry/_runtime.py:42 to 104; release-notes "## 0.143.0 (2026-10-08)" | "Automatic OpenTelemetry exporter setup is now opt-in." | 0.156.1 | 9 |
| A24 | FastAPI's JWT tutorial now uses PyJWT (switched from python-jose in 0.111.1, 2024-07-14) and pwdlib with Argon2 for password hashing. | FASTAPI-SRC | OD | docs/en/docs/tutorial/security/oauth2-jwt.md:29 to 80; release-notes line 3393 | "Update JWT auth documentation to use PyJWT instead of python-jose." | docs at 0.156.1 | 10 |
| A25 | FastAPI has no built-in rate limiter; its docs and changelog never mention one for user apps. Common libraries: slowapi (MIT), fastapi-limiter (Apache-2.0), limits (MIT). | FASTAPI-SRC; PYPI | OD | grep of docs/en/docs for "rate limit" found only CI notes in release-notes | (absence; no quote) | 0.156.1; PyPI read 2026-10-20 | 7 |
| A26 | OpenAI Responses API streaming event types include `response.created`, `response.queued`, `response.in_progress`, `response.output_text.delta`, `response.output_text.done`, `response.completed`, `response.failed`, `response.incomplete`, `error`; each carries `sequence_number`. | OPENAI-SDK; OPENAI-STREAM | OD | src/openai/types/responses/*_event.py; guide "Streaming API responses" | "Emitted when an error occurs." | openai 3.35.1 types (generated from OpenAPI spec) | 9 |
| A27 | In OpenAI Responses streams, token usage is on the `Response` object inside `response.completed` (`usage.input_tokens`, `input_tokens_details.cached_tokens`, `cache_write_tokens`, `output_tokens_details.reasoning_tokens`, `total_tokens`). | OPENAI-SDK | OD | types/responses/response_completed_event.py:14; response.py:540; response_usage.py:8 to 46 | `usage: Optional[ResponseUsage] = None` | 3.35.1 | 8 |
| A28 | In OpenAI Chat Completions streams, usage arrives only if `stream_options.include_usage` is set, in an extra chunk before `data: [DONE]`, and may be lost if the stream breaks. | OPENAI-SDK | OD | types/chat/chat_completion_stream_options_param.py | "If the stream is interrupted, you may not receive the final usage chunk" | 3.35.1 | 9 |
| A29 | OpenAI adds random padding (`obfuscation` field) to streaming deltas by default against size side channels; `include_obfuscation: false` turns it off. | OPENAI-SDK | OD | same file | "Stream obfuscation adds random characters to an `obfuscation` field" | 3.35.1 | 9 |
| A30 | OpenAI's streaming guide notes streaming makes moderation harder. | OPENAI-STREAM | OD | Streaming API responses guide | "makes it more difficult to moderate the content of the completions" | read 2026-10-20 | 8 |
| A31 | Anthropic streams can carry `error` events (for example `overloaded_error`) after an HTTP 200; the errors page says standard error handling does not apply then. | ANTH-STREAM; ANTH-ERRORS | OD | Streaming, Error events; Errors page | "an error can occur after the API returns a 200 response" | read 2026-10-20 | 9 |
| A32 | New since Part 09 in Anthropic streaming: a `fallback` content block during server-side fallback, `input_transformations` under beta header `thinking-binding-controls-2026-08-01`, thinking display modes; resumption for 4.6 and later uses a user "continue" message, not assistant prefill. | ANTH-STREAM | OD | Streaming, Event types and Error recovery | "add a user message that instructs the model to continue" | read 2026-10-20 | 8 |
| A33 | Anthropic `message_delta` usage counts are cumulative; usage also reports `inference_geo`, `service_tier` (standard, priority, batch) and `speed` (standard, fast). | ANTH-STREAM; ANTH-SDK | OD | Streaming page; src/anthropic/types/usage.py:13 to 46 | "The cumulative number of output tokens which were used." | anthropic 1.16.0 | 9 |
| A34 | Gemini streams via `POST .../{model}:streamGenerateContent`; the google-genai SDK always adds `?alt=sse`; the body is a stream of `GenerateContentResponse` objects. | GEMINI-API; GENAI-SDK | OD | API reference "Generating content"; google/genai/models.py:4736 | "a stream of `GenerateContentResponse` instances" | google-genai 2.31.0 | 8 |
| A35 | Gemini usage fields: `promptTokenCount`, `cachedContentTokenCount`, `candidatesTokenCount`, `toolUsePromptTokenCount`, `thoughtsTokenCount`, `totalTokenCount` in `usageMetadata`. Which chunk carries final counts was not stated on the page read. | GEMINI-API | OD | GenerateContentResponse, UsageMetadata | "Metadata on the generation requests' token usage." | read 2026-10-20 | 7 |
| A36 | RFC 6455 WebSocket: two-way, an HTTP Upgrade handshake then message framing over TCP; `ws` port 80, `wss` port 443; ping and pong control frames. | RFC6455 | SB | Abstract; 1.7; 3; 5.2 | "an opening handshake followed by basic message framing, layered over TCP" | RFC 6455, Dec 2011 | 9 |
| A37 | OpenAI Realtime connects over WebRTC in the browser or WebSocket on a server; browsers get short-lived credentials from `POST /v1/realtime/client_secrets`. | OPENAI-RT | OD | Realtime guide | "or WebSocket on the server" | read 2026-10-20 | 8 |
| A38 | OpenAI's Responses API now also has a persistent WebSocket mode (`wss://.../v1/responses`) taking `response.create` and `response.steer` events. So "WebSockets are for voice only" is no longer true at OpenAI. | OPENAI-SDK | OD | src/openai/resources/responses/responses.py:1996 to 1999, 4480 to 4490 | "Connect to a persistent Responses API WebSocket." | openai 3.35.1 | 8 |
| A39 | Ollama offers `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/models` and, since v0.13.3, a non-stateful `/v1/responses`; missing pieces include logprobs, `tool_choice`, `logit_bias`, `n`, image URLs, and `previous_response_id`. | OLLAMA-DOC | OD | docs/api/openai-compatibility.mdx:209 to 330 | "Only the non-stateful flavor is supported" | Ollama main 2026-10-20 | 9 |
| A40 | The OpenAI API cannot set an Ollama model's context size; it needs a Modelfile `num_ctx`. | OLLAMA-DOC | OD | same, "Setting the local context size" | "The OpenAI API does not have a way of setting the context size" | same | 9 |
| A41 | vLLM serves `/v1/completions`, `/v1/chat/completions`, `/v1/responses` (with retrieve and cancel), `/v1/embeddings`, audio routes; `suffix` unsupported, `user` ignored, `image_url.detail` unsupported; chat needs a chat template. | VLLM-DOC | OD | docs/serving/online_serving/openai_compatible_server.md:16 to 35, 173 | "*Note: `user` parameter is ignored.*" | vLLM main 7b569ec | 9 |
| A42 | llama.cpp server offers OpenAI-style chat completions, completions, responses and embeddings routes, but disclaims strict compatibility. | LLAMACPP-DOC | OD | tools/server/README.md:9, 1316, 1347, 1494 | "no strong claims of compatibility with OpenAI API spec is being made" | llama.cpp main ead9f32 | 9 |
| A43 | vLLM sends anonymous usage stats by default to `https://stats.vllm.ai`; opt out with `VLLM_NO_USAGE_STATS=1`, `DO_NOT_TRACK=1` or `~/.config/vllm/do_not_track`. | VLLM-DOC | OD | vllm/envs.py:36 to 38, 828 to 835; docs/usage/usage_stats.md:3, 54 | "vLLM collects anonymous usage data by default" | vLLM main | 10 |
| A44 | Kubernetes: "hard" multi-tenancy means tenants do not trust each other; the page calls hard and soft a spectrum with no single definition. | K8S-MT | OD | multi-tenancy.md, Isolation (lines 92 to 103) | "there is no single definition that will apply to all users" | k8s website at 6df0b1b (page last modified 2025-05-22 per live site) | 9 |
| A45 | Kubernetes lists namespaces, access controls (RBAC), quotas, network isolation, storage isolation, sandboxing containers, node isolation, API Priority and Fairness, QoS, DNS, operators; implementations are namespace-per-tenant and virtual control plane per tenant. | K8S-MT | OD | headings, lines 118 to 447 | "### Sandboxing containers" | same | 9 |
| A46 | For untrusted code, Kubernetes recommends sandboxing (VMs or userspace kernels) because containers share the host kernel, and allows that some may need dedicated clusters or hardware. So P11-03 ("supports secure multi-tenant environments") needs qualifying. | K8S-MT | OD | lines 263 to 288, 105 to 108 | "Sandboxing is often recommended when you are running untrusted code" | same | 9 |
| A47 | LangGraph Platform was renamed LangSmith Deployment in October 2025. | LC-PLATFORM | VB | FAQ | "LangGraph Platform has been renamed to LangSmith Deployment as of October 2025." | read 2026-10-20 | 8 |
| A48 | LangSmith pricing lists self-hosted deployment only on Enterprise; the Plus plan includes one free Serverless (Small) cloud deployment; no free self-hosted tier is listed. The server package `langgraph-api` is Elastic-2.0 (source-available). | LC-PRICING; PYPI | VB; OD | Pricing table; PyPI JSON | "1 free Serverless (Small) deployment included" | read 2026-10-20; langgraph-api 0.16.2 | 7 |
| A49 | Anthropic rate limits: RPM, ITPM, OTPM per model class, token-bucket refill; uncached input only counts toward ITPM for most models; 429 with `retry-after`; headers `anthropic-ratelimit-{requests,tokens,input-tokens,output-tokens}-{limit,remaining,reset}`. | ANTH-RL | OD | Rate limits page | "only uncached input tokens count toward your ITPM rate limits" | read 2026-10-20 | 9 |
| A50 | Anthropic tiers are now Start, Build, Scale, Custom with monthly spend caps $500, $1,000, $200,000, none; a spend-cap 429 has no `retry-after` and should not be retried. Rate limits are shared across `inference_geo` values. | ANTH-RL; ANTH-ERRORS | OD | Rate limits; Errors | "A tier spend-cap 429 has no `retry-after` header" | read 2026-10-20 | 8 |
| A51 | Anthropic 529 `overloaded_error` is platform-wide load; 429 is the organisation's limit (or an acceleration limit after a sharp rise). | ANTH-ERRORS | OD | HTTP errors | "529 errors can occur when the API experiences high traffic across all users." | read 2026-10-20 | 9 |
| A52 | OpenAI rate limits: RPM, RPD, TPM, TPD, IPM; headers `x-ratelimit-{limit,remaining,reset}-{requests,tokens}` plus project-token variants and `Retry-After` (treat as a minimum); the limit counts the larger of `max_tokens` and the estimate; tiers Build $5, Launch $100, Grow $500 in credit purchases. | OPENAI-RL | OD | Rate limits guide | "Treat this value as a minimum." | read 2026-10-20 | 8 |
| A53 | Both Python SDKs default to a 600 s total timeout, 5 s connect, 2 retries, 0.5 to 8 s backoff, 1000 max connections; both now use `httpx2`, not `httpx`. | OPENAI-SDK; ANTH-SDK | OD | src/openai/_constants.py:7 to 14; src/anthropic/_constants.py:10 to 15; pyproject.toml:12 | `DEFAULT_TIMEOUT = httpx2.Timeout(timeout=600, connect=5.0)` | openai 3.35.1, anthropic 1.16.0 | 10 |
| A54 | The anthropic SDK refuses non-streaming calls expected to exceed 10 minutes (estimate: 3,600 s times max_tokens / 128,000) and reads `retry-after-ms` before `retry-after`. | ANTH-SDK | OD | src/anthropic/_base_client.py:854 to 887 | "Streaming is required for operations that may take longer than 10 minutes." | 1.16.0 | 10 |
| A55 | Anthropic Usage and Cost API: `/v1/organizations/usage_report/messages` (1m, 1h, 1d buckets) and `/v1/organizations/cost_report` (1d only, USD cents as decimal strings); needs an Admin API key (`sk-ant-admin01-...`) or org-admin credential; not for individual accounts; data within about 5 minutes; Priority Tier costs excluded from cost report. | ANTH-USAGE | OD | Usage and Cost API page | "workspace API keys don't work" | read 2026-10-20 | 9 |
| A56 | OpenAI org usage endpoints `/organization/usage/{completions,embeddings,...}` (1m, 1h, 1d) and `/organization/costs` (1d only) need an admin key (`OPENAI_ADMIN_KEY` in the SDK); costs have `amount.value` and `currency`. | OPENAI-SDK | OD | resources/admin/organization/usage.py:381, 468; _client.py:200 | "Currently only `1d` is supported" | 3.35.1 | 8 |
| A57 | OpenAI gpt-6-astra: prompts over 272K input tokens pay 2x input and cache rates and 1.5x output for the whole request; base $10 in, $1 cached, $12.50 cache write, $50 out; 1,050,000 context; 128,000 max output. | OPENAI-ASTRA | OD | model page | "priced at 2x input and cache rates and 1.5x output for the full request" | read 2026-10-20 | 9 |
| A58 | OpenAI regional processing (data residency) and FedRAMP endpoints cost a 10% uplift for models released on or after March 5, 2026. | OPENAI-PRICING | OD | Pricing page | "charged a 10% uplift for models released on or after March 5, 2026" | read 2026-10-20 | 9 |
| A59 | Gemini 3.1 Pro Preview: $2 in / $12 out up to 200k prompt tokens, $4 / $18 above; caching $0.20 / $0.40 plus $4.50 per 1M tokens per hour storage; Batch and Flex half price, with Batch caching "Same as Standard"; Priority 1.8x. | GEMINI-PRICING | OD | Pricing, Gemini 3.1 Pro Preview table | "Same as Standard" | read 2026-10-20 | 8 |
| A60 | Anthropic Haiku 5.5: a prompt over 100,000 tokens (counting cache reads and writes) pays $0.50 in and $2.50 out per MTok for the whole request; other 4.6-and-later models get 1M context at standard price. | ANTH-PRICING | OD | Pricing, long context | "a request whose prompt is over 100,000 tokens pays higher prices" | read 2026-10-20 | 9 |
| A61 | Anthropic US-only inference (`inference_geo: "us"`) costs 1.1x on all token categories for 4.6-and-later models; multipliers stack with Batch; Batch and caching combine. | ANTH-PRICING | OD | Pricing, data residency; FAQ | "Batch API and prompt caching discounts can be combined." | read 2026-10-20 | 9 |
| A62 | Anthropic fast mode: Opus 5.5 $8 in / $40 out; not available with Batch. | ANTH-PRICING | OD | Pricing, fast mode | "Fast mode is not available with the Batch API." | read 2026-10-20 | 9 |
| A63 | Microsoft's official semantic-cache policy warns similarity matches can return wrong, stale or unsafe answers, recommends a low score threshold (start 0.05; above 0.2 risks mismatch) and partitioning by user with `vary-by`. | AZ-SEMCACHE | OD | llm-semantic-cache-lookup policy, usage notes | "it can surface responses that are incorrect, outdated, or unsafe" | last updated 2026-08-19 | 9 |
| A64 | Anthropic's latency levers: choose the right model (and lower effort), shorten prompt and output (`max_tokens`), stream. It defines TTFT and "baseline latency". | ANTH-LATENCY | OD | Reducing latency | "Streaming is a feature that allows the model to start sending back its response before the full output is complete." | read 2026-10-20 | 9 |
| A65 | OpenAI's seven latency principles: process tokens faster, generate fewer tokens, use fewer input tokens, make fewer requests, parallelize, make users wait less, don't default to an LLM. It claims halving output may cut about half the latency, halving the prompt only 1 to 5% (vendor claim). | OPENAI-LATENCY | OD | Latency optimization guide | "cutting 50% of your output tokens may cut ~50% of your latency" (the prompt figure is written "1 to 5%" here; the page uses a range dash) | read 2026-10-20; vendor claim, no model or date given | 8 |
| A66 | Artificial Analysis measures TTFT and output speed from one Google Cloud us-central1-a VM, 8 times a day for 1k, 10k and vision prompts, weekly for 100k, reporting P50 over 72 hours (14 days for 100k); it notes TTFT includes network latency. | AA-METHOD | VB | Performance benchmarking methodology | "sensitive to server location as it includes network latency" | methodology v2.2.0, 2 Mar 2026 | 8 |
| A67 | Little's law: average number in system L = arrival rate λ times average time in system W; holds regardless of queue discipline and without stationarity, on a sample path whose limits exist. | LITTLE-2011 | PR | Little 2011, Operations Research 59(3):536 to 549 (reprint) | "independent of queue discipline" | original: Little 1961, Operations Research 9(3):383 to 387 | 8 |
| A68 | RouteLLM (ICLR 2025): learned routers between a strong and a weak LLM, trained on preference data, "reduce costs by over 2 times without sacrificing response quality" on public benchmarks. | ROUTELLM-ICLR | PR | ICLR 2025 proceedings abstract | "reduce costs by over 2 times without sacrificing response quality" | ICLR 2025; benchmarks and models not on abstract page | 8 |
| A69 | RouteLLM's repository makes a bigger claim: up to 85% cost cut keeping 95% of GPT-4 performance on MT Bench (GPT-4-1106 vs Mixtral 8x7B, 2024). | ROUTELLM-REPO | OD | README.md:14, 48 to 52 | "reduce costs by up to 85% while maintaining 95% GPT-4 performance" | repo 0b64fda, Apache-2.0, routellm 0.2.0 (2024-07-08) | 8 |
| A70 | FrugalGPT (preprint) claims up to 98% cost reduction while matching the best single LLM (GPT-4) with an LLM cascade. | FRUGALGPT | PP | arXiv 2305.05176 v1 abstract | "up to 98% cost reduction" | 9 May 2023; no journal reference on the arXiv page | 7 |

## Facts for the lab

- SSE wire: `event: x\ndata: ...\nid: 7\nretry: 3000\n\n`; comment `: ping\n\n`; content type `text/event-stream`, UTF-8 only (A1, A2).
- FastAPI 0.156.1: `from fastapi.sse import EventSourceResponse, ServerSentEvent`; `@app.post(..., response_class=EventSourceResponse)` with `yield`; `ServerSentEvent(data=..., raw_data=..., event=..., id=..., retry=ms, comment=...)`; keep-alive `b": ping\n\n"` after `fastapi.sse._PING_INTERVAL = 15.0` s; headers `Cache-Control: no-cache`, `X-Accel-Buffering: no` (A12 to A15).
- sse-starlette 3.5.0: `EventSourceResponse(content, ping=15, send_timeout=None, sep="\r\n", client_close_handler_callable=..., shutdown_event=..., shutdown_grace_period=0)`; `Cache-Control: no-store` (A19, A20).
- Starlette 1.9.0 `StreamingResponse.listen_for_disconnect` (responses.py:247); GZip excludes `text/event-stream` (A16, A18).
- uvicorn 0.54.0: `--timeout-keep-alive 5`, `--timeout-graceful-shutdown` default None, ASGI spec_version "2.3" (A17, A21).
- nginx: `proxy_buffering on` default; `X-Accel-Buffering: no`; `proxy_read_timeout 60s` (A9 to A11).
- OpenAI stream events: `response.created`, `response.in_progress`, `response.output_text.delta`, `response.completed` (usage inside `response.usage`), `response.failed`, `response.incomplete`, `error` with `code`, `message`, `param`, `sequence_number` (A26, A27). Chat: `stream_options={"include_usage": True}`; `include_obfuscation` (A28, A29).
- Anthropic: `event: error` with `overloaded_error` mid-stream; `message_delta.usage` cumulative; usage fields `inference_geo`, `service_tier`, `speed` (A31, A33).
- Gemini: `models/{model}:streamGenerateContent?alt=sse`; `usageMetadata.promptTokenCount`, `candidatesTokenCount`, `cachedContentTokenCount`, `thoughtsTokenCount`, `totalTokenCount` (A34, A35).
- SDK defaults (openai 3.35.1, anthropic 1.16.0): timeout 600 s, connect 5 s, `max_retries=2`, backoff 0.5 to 8 s; `retry-after-ms` then `retry-after`; Anthropic non-streaming refusal threshold `3600 * max_tokens / 128000 > 600` (A53, A54).
- Rate-limit headers: `anthropic-ratelimit-requests-remaining`, `anthropic-ratelimit-input-tokens-reset` and so on; `x-ratelimit-remaining-tokens`, `x-ratelimit-reset-requests`; `retry-after` (A49, A52).
- Admin usage: `GET /v1/organizations/usage_report/messages?bucket_width=1h&group_by[]=model` with an Admin key; `GET /v1/organizations/cost_report`; OpenAI `GET /v1/organization/usage/completions?bucket_width=1d&group_by=model`, `GET /v1/organization/costs` with `OPENAI_ADMIN_KEY` (A55, A56).
- Local OpenAI-compatible base URLs: Ollama `http://localhost:11434/v1/`; vLLM `/v1/...`; llama.cpp server `/v1/chat/completions`, `/v1/responses` (A39 to A42).
- Telemetry off switches: vLLM `VLLM_NO_USAGE_STATS=1` or `DO_NOT_TRACK=1` (A43); FastAPI exports OTLP only with `FASTAPI_OTEL_AUTO_CONFIGURE=true` plus an `OTEL_EXPORTER_OTLP_ENDPOINT`, and honours `OTEL_SDK_DISABLED=true`; `FastAPI(telemetry={"tracing": False})` (A23).
- Planning formula: concurrent requests = arrival rate times mean time in system (A67). Example to check in the lab: 5 requests/s times 8 s per streamed answer = 40 open streams the server must hold at once. (The browser's 6-connection HTTP/1.1 cap in A8 is per browser and domain, so it limits one user's tabs, not the server.)
- Rate limiting libraries: slowapi 0.1.10 (MIT), fastapi-limiter 0.2.0 (Apache-2.0), limits 5.8.0 (MIT) (A25).

## Telemetry notes (per tool covered)

- FastAPI 0.156.1: native OpenTelemetry instrumentation (spans, metrics, logs) is on by default but only reaches providers you configure; no exporter is created unless opted in (A23). Grep of fastapi/ for posthog, segment, usage_stats, analytics found nothing outside docs.
- Starlette 1.9.0: has an optional `OpenTelemetryMiddleware` (starlette/middleware/opentelemetry.py) that you add yourself; no phone-home found (grep for posthog, telemetry, analytics, usage_stats).
- uvicorn 0.54.0, sse-starlette 3.5.0: grep for posthog, telemetry, analytics, usage_stats found nothing.
- openai 3.35.1 and anthropic 1.16.0 SDKs: send `x-stainless-*` client headers with each API call (seen in anthropic _base_client.py); the anthropic SDK imports opentelemetry trace APIs with an `open_telemetry` client option (_base_client.py:44, 440). No separate usage reporting found.
- google-genai 2.31.0: adds an API-client "telemetry header" to requests it sends to Google (_api_client.py:148); no separate endpoint found.
- vLLM: usage stats on by default, see A43.
- Ollama: desktop app checks `https://ollama.com/api/update` (app/updater/updater.go:33); `OLLAMA_NO_CLOUD` disables cloud features (envconfig/config.go:238, 332). Grep of Go source for posthog, segment.io, usage_stats, telemetry found only unrelated hits (it turns off Claude Desktop telemetry in a launcher config).
- llama.cpp: only docs and server README were checked out; telemetry not checked.

## Disagreements and surprises

- P11-02 is wrong as worded. The WHATWG spec itself says buffering can delay event dispatch (A6). Delays can come from nginx default buffering (A9), gzip (excluded by default in Starlette, A18), the app's own generator, and CDNs (not reached). Both FastAPI and sse-starlette now set `X-Accel-Buffering: no` for you (A14, A19).
- P11-06 needs updating: OpenAI now offers a WebSocket mode for the ordinary Responses API, not only for Realtime voice (A38). Realtime itself prefers WebRTC in browsers (A37).
- P11-03 needs qualifying: Kubernetes describes multi-tenancy as a spectrum and recommends sandboxing or separate clusters for untrusted code (A44 to A46).
- FastAPI now has first-party SSE (A12) and first-party OpenTelemetry (A23); a Part 13 lab can drop sse-starlette, or show both. Note the JSON-encoding default: `data="hello"` is sent as `data: "hello"` with quotes (A13), unlike sse-starlette.
- The openai and anthropic SDKs depend on `httpx2`, not `httpx` 0.28.1 (A53). The "Already known" httpx version is not what these SDKs use.
- OpenAI now lists a cache write price ($12.50 per million for gpt-6-astra, A57); Part 04 may describe OpenAI caching as having no write charge. Worth a check.
- Anthropic tier names changed to Start, Build, Scale, Custom with spend caps (A50); earlier parts may say Tier 1 to 4.
- Anthropic resuming an interrupted stream on 4.6-and-later models uses a user message, not assistant prefill (A32).
- Haiku 5.5 is the only current Anthropic model with a long-context surcharge, and it is 5x (A60), much steeper than OpenAI's 2x/1.5x over 272K (A57) or Gemini 3.1 Pro's 2x/1.5x over 200k (A59).
- Routing savings disagree by source: ICLR abstract "over 2 times" (A68), the repo README "up to 85%" (A69), FrugalGPT "up to 98%" (A70). Each is scoped to 2023 to 2024 model pairs and benchmarks. P8-02 is fair as "consistent with vendor advice" (both vendors' latency pages say pick smaller models, A64, A65), but the savings number must carry its scope.
- MDN's "6 connections" is attributed to Stack Overflow on MDN's own page, not a spec; the WHATWG spec only says per-server limits "might" cause trouble (A7, A8).
- OpenAI's streaming guide does not say where usage appears; the SDK types do (A27).
- No page read contained text addressed to an AI agent.

## Not reached

- CDN buffering: Cloudflare search led to an overview page with no buffering detail; no CDN claim made.
- Gemini: which streamed chunk carries final `usageMetadata`, and Gemini mid-stream error behaviour, were not on the pages read.
- OpenAI Responses API reference page redirected (developers.openai.com/api/reference/resources/responses) and was not refetched; event names come from SDK types instead.
- OpenAI's documented interplay of Batch with cached input: the pricing page shows halved cached rates in a second table but no rule text.
- RouteLLM full paper (benchmarks, model pairs behind "over 2 times") not opened; FrugalGPT venue (possibly TMLR) not confirmed.
- RFC 6455 sections 5.5.2 and 5.5.3 text was truncated.
- llama.cpp telemetry and full source not checked (sparse checkout).
- Any independent dated TTFT numbers for specific hosted models: only the methodology was read, no figures recorded.
- Official vendor guidance on semantic caching from OpenAI, Anthropic or Google: not found within budget; Microsoft Azure's policy page used instead.

## Sources

| Key | Title | URL or repository at commit | Class | Read |
|---|---|---|---|---|
| WHATWG-SSE | HTML Living Standard, 9.2 Server-sent events | https://html.spec.whatwg.org/multipage/server-sent-events.html | SB | 2026-10-20 |
| MDN-ES | EventSource (MDN) | https://developer.mozilla.org/en-US/docs/Web/API/EventSource | OD | 2026-10-20 |
| NGINX-PROXY | Module ngx_http_proxy_module | https://nginx.org/en/docs/http/ngx_http_proxy_module.html | OD | 2026-10-20 |
| FASTAPI-SRC | FastAPI source and docs | github.com/fastapi/fastapi @ f6ce798 (0.156.1), MIT | OD | 2026-10-20 |
| STARLETTE-SRC | Starlette source | github.com/encode/starlette @ dc20b21 (1.9.0), BSD-3-Clause | OD | 2026-10-20 |
| UVICORN-SRC | uvicorn source | github.com/encode/uvicorn @ cc6fea5 (0.54.0), BSD-3-Clause | OD | 2026-10-20 |
| SSE-STARLETTE-SRC | sse-starlette source | github.com/sysid/sse-starlette @ 4632103 (3.5.0), BSD-3-Clause | OD | 2026-10-20 |
| OPENAI-SDK | openai-python | github.com/openai/openai-python @ b1a1a10 (3.35.1), Apache-2.0 | OD | 2026-10-20 |
| ANTH-SDK | anthropic-sdk-python | github.com/anthropics/anthropic-sdk-python @ 2d555d1 (1.16.0), MIT | OD | 2026-10-20 |
| GENAI-SDK | python-genai | github.com/googleapis/python-genai @ 4c1abcc (2.31.0), Apache-2.0 | OD | 2026-10-20 |
| OPENAI-STREAM | Streaming API responses | https://developers.openai.com/api/docs/guides/streaming-responses | OD | 2026-10-20 |
| ANTH-STREAM | Streaming messages | https://platform.claude.com/docs/en/build-with-claude/streaming | OD | 2026-10-20 |
| ANTH-ERRORS | Errors | https://platform.claude.com/docs/en/api/errors | OD | 2026-10-20 |
| GEMINI-API | Generating content (API reference) | https://ai.google.dev/api/generate-content | OD | 2026-10-20 |
| RFC6455 | RFC 6455, The WebSocket Protocol | https://www.rfc-editor.org/rfc/rfc6455.html | SB | 2026-10-20 |
| OPENAI-RT | Realtime API guide | https://developers.openai.com/api/docs/guides/realtime | OD | 2026-10-20 |
| OLLAMA-DOC | OpenAI compatibility (Ollama) | github.com/ollama/ollama @ 3aa41cb docs/api/openai-compatibility.mdx, MIT | OD | 2026-10-20 |
| VLLM-DOC | vLLM OpenAI-Compatible Server; usage stats | github.com/vllm-project/vllm @ 7b569ec, Apache-2.0 | OD | 2026-10-20 |
| LLAMACPP-DOC | llama.cpp server README | github.com/ggml-org/llama.cpp @ ead9f32, MIT | OD | 2026-10-20 |
| K8S-MT | Multi-tenancy (Kubernetes concepts) | github.com/kubernetes/website @ 6df0b1b content/en/docs/concepts/security/multi-tenancy.md; live page https://kubernetes.io/docs/concepts/security/multi-tenancy/ | OD | 2026-10-20 |
| LC-PLATFORM | LangSmith Deployment (formerly LangGraph Platform) | https://www.langchain.com/langgraph-platform | VB | 2026-10-20 |
| LC-PRICING | LangSmith pricing | https://www.langchain.com/pricing | VB | 2026-10-20 |
| ANTH-RL | Rate limits | https://platform.claude.com/docs/en/api/rate-limits | OD | 2026-10-20 |
| OPENAI-RL | Rate limits guide | https://developers.openai.com/api/docs/guides/rate-limits | OD | 2026-10-20 |
| ANTH-USAGE | Usage and Cost API | https://platform.claude.com/docs/en/build-with-claude/usage-cost-api | OD | 2026-10-20 |
| OPENAI-PRICING | Pricing | https://developers.openai.com/api/docs/pricing | OD | 2026-10-20 |
| OPENAI-ASTRA | gpt-6-astra model page | https://developers.openai.com/api/docs/models/gpt-6-astra | OD | 2026-10-20 |
| GEMINI-PRICING | Gemini Developer API pricing | https://ai.google.dev/gemini-api/docs/pricing | OD | 2026-10-20 |
| ANTH-PRICING | Pricing | https://platform.claude.com/docs/en/about-claude/pricing | OD | 2026-10-20 |
| ANTH-LATENCY | Reducing latency | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency | OD | 2026-10-20 |
| OPENAI-LATENCY | Latency optimization | https://developers.openai.com/api/docs/guides/latency-optimization | OD | 2026-10-20 |
| AA-METHOD | Performance benchmarking methodology | https://artificialanalysis.ai/methodology/performance-benchmarking | VB | 2026-10-20 |
| LITTLE-2011 | Little, "Little's Law as Viewed on Its 50th Anniversary", Operations Research 59(3), 2011 (reprint) | https://projectproduction.org/journal/reprint-littles-law-as-viewed-on-its-50th-anniversary/ (DOI 10.1287/opre.1110.0940) | PR | 2026-10-20 |
| ROUTELLM-ICLR | Ong et al., "RouteLLM: Learning to Route LLMs from Preference Data", ICLR 2025 | https://proceedings.iclr.cc/paper_files/paper/2025/hash/5503a7c69d48a2f86fc00b3dc09de686-Abstract-Conference.html | PR | 2026-10-20 |
| ROUTELLM-REPO | RouteLLM README | github.com/lm-sys/RouteLLM @ 0b64fda, Apache-2.0 | OD | 2026-10-20 |
| FRUGALGPT | Chen, Zaharia, Zou, "FrugalGPT" | https://arxiv.org/abs/2305.05176 (v1) | PP | 2026-10-20 |
| AZ-SEMCACHE | Azure API Management llm-semantic-cache-lookup policy | https://learn.microsoft.com/en-us/azure/api-management/llm-semantic-cache-lookup-policy | OD | 2026-10-20 |
| PYPI | PyPI JSON API | https://pypi.org/pypi/NAME/json | OD | 2026-10-20 |
