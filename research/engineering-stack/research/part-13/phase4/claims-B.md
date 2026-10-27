# Claims to check, set B

B1. Where they live. On May 5, 2026, OpenTelemetry moved the GenAI conventions out of its main conventions repository into `semantic-conventions-genai`; the old pages now say "This page has moved and is no longer maintained in this repository" .
   Sources: GAI, SCV

B2. The whole set is at status Development, which under OpenTelemetry's maturity rules means it "SHOULD NOT be used in production" and may change or disappear without notice .
   Sources: GAI, OTS

B3. Input tokens "SHOULD include all types of input tokens, including cached tokens" .
   Sources: GAI

B4. Attributes a sampler needs (operation, provider, model, server) should be set when the span starts .
   Sources: GAI

B5. Agents and tools get spans named `invoke_agent {gen_ai.agent.name}` and `execute_tool {gen_ai.tool.name}`; MCP calls get `{mcp.method.name} {target}`, and because one HTTP connection carries many MCP messages, the trace context goes inside each message's `params._meta` .
   Sources: GAI

B6. Content is opt-in. Prompts, system instructions and answers go in `gen_ai.input.messages`, `gen_ai.system_instructions` and `gen_ai.output.messages`, each marked as likely to hold "sensitive information including user/PII data", and "OpenTelemetry instrumentations SHOULD NOT capture them by default" .
   Sources: GAI

B7. The conventions describe three patterns: record nothing; record on spans, for testing or storage cleared for it; or upload the content to separate storage and keep only a reference, which they recommend for production .
   Sources: GAI

B8. Structured content goes on spans as a JSON string .
   Sources: GAI

B9. Metrics, renamed this year. The conventions now define `gen_ai.client.inference.duration`, `gen_ai.client.inference.time_to_first_chunk` and `.time_per_output_chunk` (histograms in seconds), token counters such as `gen_ai.client.inference.usage.input_tokens` for totals and cost, and per-call token histograms that "should not be used for total usage or cost calculations" .
   Sources: GAI

B10. These come from unreleased changes: `gen_ai.client.token.usage` was replaced, `cache_creation` became `cache_write`, and `gen_ai.client.operation.duration` is now only for operations other than inference .
   Sources: GAI

B11. Earlier, convention release 1.37.0 had renamed `gen_ai.system` to `gen_ai.provider.name` .
   Sources: SCV

B12. The released code lags: `opentelemetry-instrumentation-openai-v2` 2.4b0 (May 1, 2026) follows conventions 1.30.0 by default, still writes `gen_ai.system` and still records `gen_ai.client.token.usage` and `gen_ai.client.operation.duration` .
   Sources: OPY

B13. Its newer behaviour is behind `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`, which changes what `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` accepts: `true` on the old path, `span_only`, `event_only` or `span_and_event` on the new one .
   Sources: OPY

B14. The Python GenAI instrumentations have also moved, to `opentelemetry-python-genai`, which now includes an official Anthropic instrumentation, `opentelemetry-instrumentation-genai-anthropic` 1.2b0, with content off by default .
   Sources: OPY

B15. Read from each project's source at the version named, October 20, 2026 . "Content by default" means prompts and answers are recorded unless you switch it off.
   Sources: HEL, LFS, LGF, LSM, MLF, OIN, OLT, OPK, PHX, TLP, WVE

B16. Defaults disagree: OpenTelemetry's own instrumentations record no prompts, while Traceloop, OpenLIT and OpenInference record them unless told not to .
   Sources: OIN, OLT, OPY, TLP

B17. OWASP agrees this matters: its 2026 list keeps sensitive information disclosure at LLM02 and says "Observability platforms (Langfuse, LangSmith, Datadog LLM Observability) log full prompts, completions, chunks, and traces by default"; it advises scrubbing logs and traces "before APM ingestion" .
   Sources: OWS

B18. The maker's own telemetry is a separate switch from your traces: Phoenix, MLflow, Opik, Weave and the self-hosted Langfuse server report usage by default .
   Sources: LFS, MLF, OPK, PHX, WVE

B19. Retention. Hosted free tiers keep traces for a limited time: Langfuse Cloud's Hobby tier shows 30 days of data access, LangSmith keeps base traces 14 days and extended ones 180, Logfire's free tier 30 days, Arize AX Free 15 days .
   Sources: LFS, LGF, LSM, PHX

B20. Langfuse runs model-graded evaluators on new traces with filters and a sampling rate, and needs your model provider key; LangSmith does the same and moves every trace it scores to the longer, more expensive retention; open-source Phoenix runs evaluators on datasets, and its docs send production monitoring to the paid Arize AX .
   Sources: LFS, LSM, PHX

B21. Prices (per million tokens, read October 20, 2026) :
   Sources: AND, GMD, OAD

B22. Discounts and surcharges. All three vendors' batch APIs charge half price for jobs answered within a day: Anthropic up to 100,000 requests or 256 MB per batch, most done within an hour, expired after 24 hours, results kept 29 days; OpenAI up to 50,000 requests or 200 MB, a 24-hour window, output deleted after 30 days; Gemini inline under 20 MB or files up to 2 GB, target 24 hours, expired after 48, results kept six weeks .
   Sources: AND, GMD, OAD

B23. Anthropic says batch and caching discounts "can stack", with cache hits "on a best-effort basis", typically 30% to 98% .
   Sources: AND

B24. OpenAI also sells Flex at the batch price and Fast (called "Priority processing" until July 30, 2026) at about twice the standard price .
   Sources: OAD

B25. Keeping data in one region costs extra: Anthropic 1.1x for `inference_geo: "us"`, OpenAI 10% for models released from March 5, 2026 .
   Sources: AND, OAD

B26. Long-context pricing applies to the whole request. One token over the line changes the price of all of them .
   Sources: AND, GMD, OAD

B27. Anthropic counts cache reads and writes toward the Haiku threshold ; the lab counts them for all three, which OpenAI's and Google's pages read didn't state .
   Sources: AND

B28. Where the money is reported. Per request, in each response's usage fields; across an organization, in usage and cost APIs that need an administrator key: Anthropic's Usage and Cost API (cost in daily buckets, usage within about five minutes) and OpenAI's organization usage and costs endpoints .
   Sources: AND, OAS

B29. The GenAI conventions' token counters are meant as "a proxy for cost approximation" ; the vendor's invoice is the authority.
   Sources: GAI

B30. Cheaper answers. Routing easy requests to a smaller model saved money in research: RouteLLM (ICLR 2025) reports cutting costs "by over 2 times without sacrificing response quality" on its benchmarks, its repository claims up to 85% while keeping 95% of GPT-4's MT-Bench score, and the FrugalGPT preprint up to 98%, all on 2023 to 2024 model pairs .
   Sources: FRG, RTL

B31. Semantic caching returns a stored answer to a question that looks similar; Microsoft's documentation for its gateway warns it "can surface responses that are incorrect, outdated, or unsafe" and says to keep caches separate per user .
   Sources: AZS

B32. Anthropic's list of levers: pick a faster model or lower effort, shorten the prompt and the output, and stream .
   Sources: AND

B33. OpenAI's seven principles include generating fewer tokens, using fewer input tokens, making fewer requests and running steps in parallel; it claims that cutting output by half "may cut ~50% of your latency" while halving the prompt saves only 1 to 5%, a vendor estimate with no model named .
   Sources: OAD

B34. Independent measurements of hosted models depend on where they're taken: Artificial Analysis measures from one Google Cloud region and notes its time to first token "includes network latency" .
   Sources: AAM

B35. How many streams at once. Little's law: the average number of requests in a system equals the arrival rate times the average time each spends there, whatever the order of service .
   Sources: LIT

B36. Record durations as histograms: Prometheus explains that pre-computed quantiles can't be combined across servers, while histograms can, with `histogram_quantile(0.95, sum by (le) (rate(..._bucket[5m])))` ; the GenAI conventions suggest histogram buckets for durations from 0.01 to about 82 seconds, doubling .
   Sources: GAI, PRM

B37. What to measure in production : requests and errors by `error.type`; time to first chunk and total duration as histograms; input, cached, output and reasoning tokens as counters by model; cost from those counters and the price sheet; and the share of streams that ended early (client gone, timeout, error).
   Sources: GAI, PRM

B38. | SSE pushes tokens "the exact moment they are generated" (P11-02) | Wrong as worded. The spec warns buffering "can cause delays in event dispatch"; nginx buffers proxied responses by default; the lab's stream arrived all at once through a proxy that ignored `X-Accel-Buffering: no`  | 3.3 |
   Sources: NGX, WSS

B39. | Kubernetes "supports secure multi-tenant environments" (P11-03) | Overstated. Kubernetes calls isolation "a broad spectrum" with "no single definition" and recommends sandboxing for untrusted code, or separate clusters for some cases  | 3.1 |
   Sources: K8S

B40. | FastAPI, LangServe, Docker, API gateways (P11-04) | LangServe is still outdated: archived May 5, 2026; its successor was renamed LangSmith Deployment and self-hosts only on an Enterprise plan. FastAPI is current and now has built-in SSE (0.135.0) and OpenTelemetry (0.143.0)  | 3.1 |
   Sources: FAS, LCS

B41. | A gateway that logs "every incoming prompt, outgoing generation, token count, and latency metric" (P11-05) | Logging every prompt is a privacy decision, not a default to copy. The GenAI conventions say instrumentations "SHOULD NOT capture them by default"; OWASP LLM02:2026 names observability platforms that "log full prompts ... by default"  | 3.7, 3.8 |
   Sources: GAI, OWS

B42. | WebSockets versus SSE; separate the web server from the inference engine; auth, rate limits, logs (P11-06) | Consistent, with an update: OpenAI now offers WebSocket modes for Realtime and for ordinary Responses; FastAPI has no built-in rate limiter; serving engines are separate programs  | 3.1, 3.2, 3.5 |
   Sources: FAS, OAD, OAS, VLM

B43. | Routing easy queries to smaller models (P8-02) | Consistent with the vendors' latency advice; the savings are 2x to 98% depending on the study and model pair, all on 2023 to 2024 models  | 3.9 |
   Sources: AND, FRG, OAD, RTL

B44. | Phoenix as an evaluation tool (P9-09) | Still Elastic License 2.0 at 20.23.0; its open-source version evaluates datasets, and its docs send live-traffic evaluation to the paid Arize AX  | 3.8 |
   Sources: PHX

B45. A standard library that waits for nobody .
   Sources: FAS

B46. A convention that moved while people used it .
   Sources: GAI, OPY, SCV

B47. A security list naming tools .
   Sources: OWS

B48. Step 1, the API. FastAPI with `EventSourceResponse`, which sends `X-Accel-Buffering: no` and pings every 15 seconds .
   Sources: FAS

B49. Ask the platform team to turn off buffering on the streaming route anyway, and raise `proxy_read_timeout` above the longest silent thinking time .
   Sources: NGX

B50. Step 2, capacity. By Little's law, 5 requests a second times 8 seconds is 40 open streams at peak; the daily average is 10,000 / 86,400 = 0.93 a second, about 7 streams .
   Sources: LIT

B51. Cache hits aren't guaranteed, so budget for the uncached figure and watch `gen_ai.usage.cache_read.input_tokens` .
   Sources: GAI

B52. Step 4, tracing. OpenTelemetry's instrumentation with content capture off, which is its default; a Collector whose attributes processor deletes `gen_ai.input.messages` and `gen_ai.output.messages` in case anyone turns it on; the tracing UI self-hosted with its maker's telemetry switched off .
   Sources: GAI, OPY, OTS

B53. Alerts on p95 time to first token and on errors by type, not on means .
   Sources: PRM

B54. Step 5, failures. Clients treat an `error` event as a failure even after a 200; the server stops reading the model's stream when the browser leaves; retries obey `retry-after`, and an Anthropic 429 with no `retry-after` pages a person instead of retrying .
   Sources: AND

B55. Step 6, the night job. A nightly summary of the day's tickets (4,000 tokens in, 300 out each) goes through the Batch API at half price: $0.0055 instead of $0.011 per summary .
   Sources: AND

B56. Checked October 20, 2026 .
   Sources: PYPI

B57. Sources: Sections 3.1, 3.7 and 3.8 .
   Sources: FAS, LFS, OPY, PHX, PYPI, SSS, UVI

B58. - Best default for a solo builder: FastAPI's own `EventSourceResponse`, the OpenTelemetry SDK with a `BatchSpanProcessor`, content capture off, and a self-hosted tracing UI with its telemetry switch set; Phoenix (`PHOENIX_TELEMETRY_ENABLED=false`) or Langfuse (`TELEMETRY_ENABLED=false`)
   Sources: FAS, LFS, OPY, PHX

B59. - If you already use LangChain's hosted tools: LangSmith, with `LANGSMITH_HIDE_INPUTS=true` and `LANGSMITH_HIDE_OUTPUTS=true` until you've decided what you may store .
   Sources: LSM

B60. - If you use Traceloop, OpenLIT or OpenInference: turn content off first: `TRACELOOP_TRACE_CONTENT=false`, `openlit.init(capture_message_content=False)`, `OPENINFERENCE_HIDE_INPUTS=true` and `OPENINFERENCE_HIDE_OUTPUTS=true` .
   Sources: OIN, OLT, TLP

B61. - Skip for new work: LangServe, archived .
   Sources: LCS

B62. - When not to stream: background jobs, evaluations and anything a person isn't waiting for; send those to a batch API at half price .
   Sources: AND, GMD, OAD

B63. | A FastAPI stream shows `data: "hello"` with quotes | FastAPI JSON-encodes `data` | Use `raw_data` for plain text  |
   Sources: FAS

B64. - "SSE delivers each token the moment it exists." Proxies buffer by default, and the spec itself warns about delays .
   Sources: NGX, WSS

B65. - "A 200 status means the answer succeeded." Errors can arrive inside the stream after the 200 .
   Sources: AND

B66. - "Following OpenTelemetry means recording the prompts." Its conventions say not to by default; some tools do it anyway .
   Sources: GAI, OLT, TLP

B67. - "Long-context pricing charges extra only for the extra tokens." It reprices the whole request .
   Sources: AND, GMD, OAD

B68. From January 1, 2027 the prices double, and so does the answer .
   Sources: GMD

B69. Answers. (1) A proxy buffering the response (send `X-Accel-Buffering: no`, check the proxy's settings) and your own code collecting text before yielding .
   Sources: NGX, STL

B70. (2) The status was sent with the first byte; later failures can only be events .
   Sources: AND

B71. (3) `gen_ai.input.messages`; no, it's opt-in .
   Sources: GAI

B72. (4) The whole request is repriced: input and cache rates double and output rises 1.5 times .
   Sources: OAD

B73. Best next resources (checked to exist on October 20, 2026): the WHATWG server-sent events section ; the OpenTelemetry GenAI conventions repository ; OpenTelemetry's sampling and Collector docs ; Prometheus's "Histograms and summaries" ; OWASP's LLM02:2026 ; the vendors' batch and rate-limit pages .
   Sources: AND, GAI, GMD, OAD, OTS, OWS, PRM, WSS

B74. - The GenAI conventions are a moving target. Status Development, renamed metrics this year, a repository move in May, and instrumentation that lags; names in this part are as of October 18, 2026 .
   Sources: GAI, OPY

B75. - Prices change. All figures were read on October 20, 2026; some change on a set date (Gemini's on January 1, 2027) .
   Sources: GMD

B76. - Routing savings are from 2023 to 2024 model pairs. RouteLLM's 2x and 85% and FrugalGPT's 98% weren't re-run .
   Sources: FRG, RTL

B77. Claim ledger P11-02 should read "wrong as worded": buffering can delay delivery .
   Sources: NGX, WSS

B78. P11-03 should read "overstated" .
   Sources: K8S

B79. P11-04 should add LangSmith Deployment and FastAPI's built-in SSE .
   Sources: FAS, LCS

B80. P11-05 should cite OWASP LLM02:2026 and the conventions' opt-in rule .
   Sources: GAI, OWS

B81. Part 11, Section 3.6 defines TTFT, TPOT and ITL by formula; the GenAI conventions now add their own names (`gen_ai.client.inference.time_to_first_chunk` for clients, `gen_ai.server.time_to_first_token` for servers), worth a line there .
   Sources: GAI


# Sources

| Key | Source | Class | Used for | Grade |
|---|---|---|---|---|
| AAM | Artificial Analysis, "Performance benchmarking methodology" (v2.2.0, March 2, 2026) | VB | Where its latency numbers are measured | 7 |
| AND | Anthropic docs: Streaming messages; Errors; Rate limits; Usage and Cost API; Pricing; Reducing latency; Batch processing | OD | Event types, mid-stream errors, resuming, 429 and 529, tiers and spend caps, admin reports, prices, residency, fast mode, latency levers, batch limits | 9 |
| AZS | Microsoft Learn, Azure API Management `llm-semantic-cache-lookup` policy (updated 2026-08-19) | OD | Semantic caching's risks and per-user caches | 8 |
| FAS | fastapi/fastapi at f6ce798 (0.156.1): `fastapi/sse.py`, `routing.py`, `applications.py`, `telemetry/`, release notes, security tutorial | OD | Built-in SSE, ping, headers, JSON-encoded data, telemetry opt-in, PyJWT and pwdlib, no rate limiter | 10 |
| FRG | Chen, Zaharia and Zou, "FrugalGPT", arXiv 2305.05176v1 (abstract) | PP | "Up to 98%" | 6 |
| GAI | open-telemetry/semantic-conventions-genai at 547934a (2026-10-18): `docs/gen-ai/` (client-inference, gen-ai-spans, gen-ai-agent-spans, gen-ai-metrics, gen-ai-token-metrics, mcp), `changelog.d/` | SB | Status, span names, attributes, content rule, metrics and renames | 10 |
| GMD | Google AI for Developers: API reference "Generating content"; Batch API (updated 2026-09-17); Pricing | OD | `streamGenerateContent`, usage fields, batch limits, prices | 8 |
| HEL | Helicone/helicone at 6b057cd: README, LICENSE, header docs | OD | What Helicone is; omit headers | 8 |
| K8S | kubernetes/website at 6df0b1b: `concepts/security/multi-tenancy.md` | OD | Ledger P11-03 | 9 |
| LCS | langchain-ai/langserve repository page; LangChain's LangSmith Deployment page and pricing page | OD, VB | Archived May 5, 2026; the rename; Enterprise self-hosting | 8 |
| LFS | langfuse/langfuse at 6343bd8 (LICENSE, telemetry); langfuse/langfuse-docs at ab9037b; langfuse 5.0.3 wheel | OD | Licence split, telemetry switch, masking, retention, online evaluation | 9 |
| LGF | pydantic/logfire at f3fc0ec; logfire 5.2.0 wheel; pydantic.dev pricing | OD, VB | Closed server, `send_to_logfire`, scrubbing, retention | 8 |
| LIT | Little, "Little's Law as Viewed on Its 50th Anniversary", Operations Research 59(3), 2011, pp. 536 to 549 (reprint) | PR | L = λW and its conditions | 8 |
| LSM | langchain-ai/docs at f8f2328 (LangSmith pages); langsmith 0.14.11 wheel | OD | Self-hosting, OTLP, hide switches, retention, online evaluators | 9 |
| MLF | mlflow/mlflow at 8fe044b (main, 3.17.2.dev0, not the 3.17.1 tag) | OD | Telemetry switch, OTLP, autolog | 8 |
| NGX | nginx, "Module ngx_http_proxy_module" | OD | `proxy_buffering`, `X-Accel-Buffering`, `proxy_read_timeout` | 9 |
| OAD | OpenAI developer docs: Streaming API responses; Realtime; Rate limits; Latency optimization; Batch; Pricing; gpt-6-astra model page | OD | Streaming, WebSocket and WebRTC, limits and headers, latency principles, batch limits, prices, Fast and Flex, residency, long context | 9 |
| OAS | openai/openai-python at b1a1a10 (3.35.1): response event types, stream options, WebSocket mode, admin usage, `_constants.py` | OD | Event names, usage in streams, padding, WebSocket mode, timeouts, admin key | 9 |
| OIN | Arize-ai/openinference at ca3ed46: `spec/` | OD | Attribute names; content on by default | 9 |
| OLT | openlit/openlit at 9654e6c (Python SDK 1.45.0) | OD | Content on by default; console fallback; price-list fetch | 9 |
| OPK | comet-ml/opik at b53e27c; opik 2.2.109 wheel | OD | Analytics and error-report switches; OTLP | 8 |
| OPY | OpenTelemetry Python: SDK and OTLP exporter 1.45.1 wheels; opentelemetry-python-contrib at de43f81; opentelemetry-python-genai at cb6592a; instrumentation-openai-v2 2.4b0 and util-genai 1.2b0 wheels; one local run without a collector | OD | Offline exporters, defaults, the 7.5-second block, the move, what 2.4b0 emits, the Anthropic instrumentation | 9 |
| OTS | OpenTelemetry specification at e30cae5 (maturity levels, SDK variables); opentelemetry-proto at 0976993; opentelemetry.io docs source at 2695b91 (traces, sampling, Collector) | SB | Spans, status, sampling, OTLP ports, the Collector, "Development" | 9 |
| OWS | GenAI-Security-Project/GenAI-LLM-Top10 at 9253e38 (`2026/final`); OWASP project site source at 99f4395 | SB | LLM02:2026 text; publication date | 9 |
| PHX | Arize-ai/phoenix at 57b8303 (LICENSE, `config.py`, docs); arize-phoenix-otel 0.17.2 wheel; Arize pricing page | OD, VB | Licence, telemetry switch, OTLP, evaluation scope, AX retention | 9 |
| PRM | prometheus/docs at 73e9169: `practices/histograms.md` | OD | Histograms over summaries; `histogram_quantile` | 9 |
| PYPI | PyPI JSON API, October 20, 2026 | OD | Versions, licences, Python ranges | 9 |
| RTL | Ong et al., "RouteLLM", ICLR 2025 (proceedings abstract); lm-sys/RouteLLM at 0b64fda (README) | PR, OD | Routing savings and their scope | 7 |
| SCV | open-telemetry/semantic-conventions at 02e6d3e: CHANGELOG (v1.37.0), `docs/gen-ai/README.md`, git history | SB | The `gen_ai.provider.name` rename; the May 5, 2026 move | 10 |
| SSS | sysid/sse-starlette at 4632103 (3.5.0): `sse_starlette/sse.py` | OD | Ping, headers, shutdown hook | 10 |
| STL | encode/starlette at dc20b21 (1.9.0): `responses.py`, `middleware/gzip.py` | OD | Disconnect detection; gzip skips SSE | 9 |
| TLP | traceloop-sdk 0.62.4 wheel; traceloop/openllmetry at 8d9c93f | OD | Content on by default; unused telemetry flag | 10 |
| UVI | encode/uvicorn at cc6fea5 (0.54.0): `config.py`, `server.py`, protocol files | OD | ASGI 2.3, timeouts, graceful shutdown | 9 |
| VLM | vllm-project/vllm at 7b569ec (main): OpenAI-compatible server docs, `envs.py`, usage-stats docs | OD | Routes and gaps; usage statistics on by default | 9 |
| WSS | WHATWG HTML Living Standard, 9.2 "Server-sent events" (last updated October 20, 2026) | SB | Wire format, parsing rules, authoring notes | 10 |
| WVE | weave 0.53.12 wheel | OD | Destination and error-report switch | 8 |
