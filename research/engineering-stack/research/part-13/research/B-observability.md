# B: Observability and tracing of AI applications (T29)

Topic group: T29, for a reader who wants to see what their model calls and agents did, what they cost and where they were slow, without leaking users' data.
Date: 2026-10-20. Researcher B.
Lookups used: 9 of 40 (WebFetch and WebSearch). Everything else came from git clones and PyPI.

Repositories read (shallow clones; commit and commit date):
- open-telemetry/semantic-conventions-genai 547934af (2026-10-18) [GAI]
- open-telemetry/semantic-conventions 02e6d3e3 (2026-10-20) [SCV]
- open-telemetry/opentelemetry-specification e30cae5c (2026-10-20) [SPEC]; opentelemetry-proto 09769935 (2026-10-19) [PROTO]
- open-telemetry/opentelemetry.io 2695b91f (2026-10-20), docs source [OIO]
- open-telemetry/opentelemetry-python-contrib de43f819 (2026-10-16) [CON]; opentelemetry-python-genai cb6592a9 (2026-10-20) [PYG]
- langfuse/langfuse 6343bd81 [LFS]; langfuse/langfuse-docs ab9037b0 [LFD]; Arize-ai/phoenix 57b83036 [PHX]; Arize-ai/openinference ca3ed460 [OI]; openlit/openlit 9654e6c0 [OLT]; Helicone/helicone 6b057cda [HEL]; mlflow/mlflow 8fe044b5 (main, version 3.17.2.dev0, not the 3.17.1 tag) [MLF]; comet-ml/opik b53e27c5 [OPK]; pydantic/logfire f3fc0ecb [LGF]; traceloop/openllmetry 8d9c93f3 [OLM]; langchain-ai/docs f8f2328e [LSD]; prometheus/docs 73e91696 [PROM]; OWASP/www-project-top-10-for-large-language-model-applications 99f43955 [OW25]; GenAI-Security-Project/GenAI-LLM-Top10 9253e38a [OW26]
- PyPI wheels unpacked and read (exact released code): opentelemetry-instrumentation-openai-v2 2.4b0 [OAV2], opentelemetry-util-genai 1.2b0 [UGA], opentelemetry-sdk 1.45.1 [SDK], opentelemetry-exporter-otlp-proto-http and -grpc 1.45.1 [HTX, GRX], langfuse 5.0.3 [LFP], traceloop-sdk 0.62.4 [TLS], openlit 1.45.0, langsmith 0.14.11 [LSP], opik 2.2.109 [OPW], weave 0.53.12 [WV], logfire 5.2.0 [LGW], arize-phoenix-otel 0.17.2 [PHO]
- One local run [LAB]: Python 3 venv in /home/claude/part13/research/b, opentelemetry-sdk and exporter-otlp-proto-http 1.45.1, no collector running.

## Claims

### 1. OpenTelemetry basics

| ID | Claim | Source key | Class | Place | Quote | Scope and date | Conf. |
|---|---|---|---|---|---|---|---|
| B1 | A span is one unit of work; spans are the building blocks of a trace. | OIO | SB | concepts/signals/traces.md, "Spans" | "A span represents a unit of work or operation. Spans are the building blocks of Traces." | opentelemetry.io source at 2695b91f | 9 |
| B2 | Attributes are key-value metadata on a span; add them at creation so samplers can see them. | OIO | SB | traces.md, "Attributes" | "Prefer adding attributes at span creation to make the attributes available to SDK sampling." | same | 9 |
| B3 | Use a span event when the moment something happened matters; use an attribute when it does not. | OIO | SB | traces.md, "When to use span events versus span attributes" | "consider whether a specific timestamp is meaningful" | same | 9 |
| B4 | Span status is Unset, Error or Ok; Unset (the default) already means success. | OIO | SB | traces.md, "Span Status" | "A span status that is Unset means that the operation it tracked successfully completed without an error." | same | 9 |
| B5 | Context propagation is what lets spans made in different services join one trace. | OIO | SB | traces.md, "Context Propagation" | "Context Propagation is the core concept that enables Distributed Tracing." | same | 9 |
| B6 | W3C Trace Context is a W3C Recommendation (Level 1, 23 November 2021); `traceparent` is `version-traceid-parentid-traceflags`: 2, 32, 16 and 2 hex characters. | W3C | SB | Sections "traceparent Header" | Example: "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01" | REC-trace-context-1-20211123, read 2026-10-20 | 9 |
| B7 | The lowest bit of trace-flags is the sampled flag: the caller may have recorded the trace. `tracestate` carries vendor-specific data, up to 32 entries. | W3C | SB | "Sampled flag", "tracestate Header" | "the least significant bit (right-most), denotes that the caller may have recorded trace data" | same | 8 |
| B8 | Head sampling decides early (usually by trace ID and a percentage) without seeing the whole trace, so it cannot guarantee keeping every trace with an error. | OIO | SB | concepts/sampling/index.md, "Head Sampling" | "you cannot ensure that all traces with an error within them are sampled with head sampling alone" | same | 9 |
| B9 | Tail sampling decides after seeing all or most spans, for example keep all errors or slow traces; it is harder to implement and operate; the Collector has a Tail Sampling Processor. | OIO | SB | sampling/index.md, "Tail Sampling", "Support > Collector" | "Tail sampling can be difficult to implement." | same | 9 |
| B10 | The SDK default sampler is `parentbased_always_on`, so with no settings every trace is kept. | SPEC | SB | specification/configuration/sdk-environment-variables.md line 120 | `OTEL_TRACES_SAMPLER` default "parentbased_always_on" | spec at e30cae5c | 9 |
| B11 | OpenTelemetry recommends a Collector beside the service in general; it handles retries, batching, encryption and sensitive data filtering. Direct export is fine for getting started. | OIO | SB | collector/_index.md, "When to use a collector" | "the collector can take care of additional handling like retries, batching, encryption or even sensitive data filtering" | same | 9 |
| B12 | The Collector's attributes processor can update, insert, delete or replace span attributes, which is one place to drop prompt content before storage. | OIO | SB | collector/transforming-telemetry.md, "Adding or Deleting Attributes" | "The attributes processor can be used to update, insert, delete, or replace existing attributes" | same | 8 |
| B13 | OTLP default ports: 4317 for gRPC, 4318 for HTTP. | PROTO | SB | docs/specification.md lines 425 and 717 | "The default network port for OTLP/gRPC is 4317." | proto at 09769935 | 10 |
| B14 | `OTEL_SDK_DISABLED=true` swaps in a no-op SDK for all signals; any other value leaves it on. `OTEL_TRACES_EXPORTER` defaults to `otlp` in the spec. | SPEC | SB | sdk-environment-variables.md lines 115 and 244 | "If "true", a no-op SDK implementation will be used for all telemetry signals." | same | 9 |
| B15 | "Development" maturity means configuration may break often, the component should not be used in production, and it may be removed without notice. | SPEC | SB | specification/maturity-levels.md, "Development" | "The component SHOULD NOT be used in production. The component MAY be removed without prior notice." | same. Note: this file is written for components; the GenAI docs link the document-status page, which points to it | 8 |

### 2. OpenTelemetry GenAI semantic conventions (repository semantic-conventions-genai)

| ID | Claim | Source key | Class | Place | Quote | Scope and date | Conf. |
|---|---|---|---|---|---|---|---|
| B16 | The whole GenAI convention set has status Development. The old pages in the main repository now say they moved. | GAI; SCV | SB | GAI docs/gen-ai/README.md line 7; SCV docs/gen-ai/README.md lines 9 to 11 | "This page has moved and is no longer maintained in this repository." | GAI at 547934af (no release tag); SCV at 02e6d3e3 | 10 |
| B17 | The model-call span is now named `gen_ai.client.inference` in the model files; its span name is `{gen_ai.operation.name} {gen_ai.request.model}` (for example `chat gpt-4`), kind CLIENT. | GAI | SB | docs/gen-ai/client-inference.md lines 42 to 58 | "Span name SHOULD be `{gen_ai.operation.name} {gen_ai.request.model}`." | same | 10 |
| B18 | Required on that span: `gen_ai.operation.name` and `gen_ai.provider.name`. `gen_ai.request.model` is Conditionally Required ("If available"). `gen_ai.response.model`, `gen_ai.response.id`, `gen_ai.response.finish_reasons`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens` are Recommended. | GAI | SB | client-inference.md attribute table lines 70 to 105 | `gen_ai.provider.name` ... `Required` | same | 10 |
| B19 | Cache tokens: `gen_ai.usage.cache_read.input_tokens` and `gen_ai.usage.cache_write.input_tokens` (Recommended when non-zero) and both SHOULD be counted inside `gen_ai.usage.input_tokens`. Reasoning tokens: `gen_ai.usage.reasoning.output_tokens`. | GAI | SB | client-inference.md lines 99, 100, 106; notes [23], [24], [28] | "This value SHOULD include all types of input tokens, including cached tokens." | same | 10 |
| B20 | New span attribute `gen_ai.response.time_to_first_chunk` (seconds, streaming only); also `gen_ai.request.stream`, `gen_ai.request.reasoning.level`, per-modality token counts (`gen_ai.usage.text/image/audio.*`). | GAI | SB | client-inference.md lines 80, 88, 95 to 109 | "Time to first chunk in a streaming response, measured from request issuance, in seconds." | same | 9 |
| B21 | Attributes useful for sampling (operation name, provider, request model, server address and port) SHOULD be set at span creation. | GAI | SB | client-inference.md after note [39] | "SHOULD be provided at span creation time (if provided at all)" | same | 9 |
| B22 | Prompt and completion content goes in Opt-In attributes `gen_ai.system_instructions`, `gen_ai.input.messages`, `gen_ai.output.messages` (also `gen_ai.tool.definitions`, `gen_ai.prompt.variable`), each with a warning about sensitive data. | GAI | SB | client-inference.md lines 111 to 115 and note [35] | "This attribute is likely to contain sensitive information including user/PII data." | same | 10 |
| B23 | Instrumentations SHOULD NOT capture content by default and SHOULD offer an opt-in. Three patterns: record nothing (default); record on spans (pre-production or compliant storage); store content externally and keep references (recommended for production). | GAI | SB | docs/gen-ai/gen-ai-spans.md, "Capturing instructions, inputs, and outputs" | "OpenTelemetry instrumentations SHOULD NOT capture them by default, but SHOULD provide an option for users to opt in." | same | 10 |
| B24 | Structured content attributes may not yet be supported on spans; then they SHOULD be JSON strings on spans and structured on events. Truncation options MAY be offered. | GAI | SB | gen-ai-spans.md, "Recording content on attributes" | "the corresponding attribute value SHOULD be serialized to JSON string on spans" | same | 9 |
| B25 | An upload hook MAY receive content for external storage, and SHOULD run regardless of the sampling decision; the example opt-in variable named in the registry is `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`. | GAI | SB | gen-ai-spans.md "Uploading content to external storage"; docs/registry/attributes/gen-ai.md line 144 | "instrumentations SHOULD invoke it regardless of the span sampling decision" | same | 9 |
| B26 | Event `gen_ai.client.inference.operation.details` can hold inputs and outputs separately from traces, severity DEBUG; it was changed from opt-in to Recommended. Content attributes on it remain Opt-In. | GAI | SB | client-inference.md line 835 onward; changelog.d/579.enhancement.md | "This event could be used to store input and output details independently from traces." | same | 8 |
| B27 | Agent spans: `create_agent {gen_ai.agent.name}` (CLIENT); `invoke_agent {gen_ai.agent.name}` as CLIENT (remote agent) or INTERNAL (in-process); `execute_tool {gen_ai.tool.name}` (INTERNAL); also `invoke_workflow`, `plan`, and Agent Skills spans (`execute_tool {gen_ai.tool.name} {gen_ai.skill.name}`). | GAI | SB | gen-ai-agent-spans.md lines 49, 204, 560, 838, 1010, 1116; gen-ai-spans.md line 769 | "Span name SHOULD be `execute_tool {gen_ai.tool.name}`." | same | 9 |
| B28 | Agent metrics: `gen_ai.invoke_agent.duration`, `gen_ai.invoke_agent.inference_calls`, `gen_ai.invoke_agent.tool_calls`, `gen_ai.execute_tool.duration`, `gen_ai.invoke_workflow.duration`. | GAI | SB | gen-ai-metrics.md lines 556 to 776 | headings "Metric: `gen_ai.invoke_agent.duration`" etc. | same | 9 |
| B29 | Model-call metrics: `gen_ai.client.inference.duration` (histogram, s), `gen_ai.client.inference.time_to_first_chunk` (s, streaming only), `gen_ai.client.inference.time_per_output_chunk` (s). Suggested buckets 0.01 to 81.92 s, doubling. | GAI | SB | client-inference.md lines 446 to 590 | "This metric SHOULD be reported for streaming calls and SHOULD NOT be reported otherwise." | same | 10 |
| B30 | Token metrics are now counters `gen_ai.client.inference.usage.input_tokens`, `.output_tokens`, `.cache_read.input_tokens`, `.cache_write.input_tokens`, `.reasoning.output_tokens` (unit `{token}`, by `gen_ai.token.modality`) for totals and cost, plus histograms `gen_ai.client.inference.operation.input_tokens` and `.output_tokens` for per-call percentiles only. | GAI | SB | gen-ai-token-metrics.md lines 22 to 90 | "They should not be used for total usage or cost calculations." | same | 10 |
| B31 | When a provider reports both used and billable tokens, instrumentation MUST report billable; failed calls record 0 with modality `unknown`. | GAI | SB | gen-ai-token-metrics.md note [1] under usage.input_tokens | "instrumentation MUST report billable tokens" | same | 9 |
| B32 | `gen_ai.client.operation.duration` (histogram, s) still exists but is now for non-inference operations; server metrics are `gen_ai.server.request.duration`, `gen_ai.server.time_to_first_token`, `gen_ai.server.time_per_output_token`, all histograms in seconds. | GAI | SB | gen-ai-metrics.md lines 50 to 453; changelog.d/521.breaking.md | "Clarify that `gen_ai.client.operation.duration` is not for inference." | same | 9 |
| B33 | MCP spans are named `{mcp.method.name} {target}` (for example `tools/call get-weather`); metrics `mcp.client.operation.duration`, `mcp.server.operation.duration`, `mcp.client.session.duration`, `mcp.server.session.duration` (s). | GAI | SB | docs/gen-ai/mcp.md lines 143, 595 to 1030, 1163 | "Span name SHOULD follow the format `{mcp.method.name} {target}`" | same | 9 |
| B34 | MCP trace context goes in each request's `params._meta` as unprefixed `traceparent`, `tracestate`, `baggage`, because HTTP headers only cover the HTTP request, not each JSON-RPC message. | GAI | SB | mcp.md "Context propagation" lines 43 to 60 | "the context propagation keys SHOULD be written unprefixed" | same; cites MCP spec 2025-11-25 and SEP-414 | 9 |
| B35 | Rename history: `gen_ai.system` became `gen_ai.provider.name` in semantic conventions v1.37.0, which also replaced per-message events (`gen_ai.user.message`, `gen_ai.choice` and so on) with the three content attributes. | SCV | SB | CHANGELOG.md, v1.37.0 "Breaking changes", lines 581 to 598 | "Rename `gen_ai.system` to `gen_ai.provider.name`" | main repo at 02e6d3e3 | 10 |
| B36 | Unreleased breaking changes in the new repo: `gen_ai.client.token.usage` and `gen_ai.token.type` replaced (374); `gen_ai.usage.cache_creation.input_tokens` renamed to `cache_write` (440); `gen_ai.client.operation.time_to_first_chunk` renamed to `gen_ai.client.inference.*` (521); provider value `mistral_ai` renamed `mistral`. | GAI | SB | changelog.d/374.breaking.md, 440.breaking.md, 521.breaking.md, +.breaking.md | "Replace the `gen_ai.client.token.usage` histogram (and the `gen_ai.token.type` attribute it relied on)" | towncrier fragments, unreleased as of 547934af | 10 |
| B37 | `OTEL_SEMCONV_STABILITY_OPT_IN` is the standard migration switch in the main conventions (database, RPC, code attributes); `gen_ai_latest_experimental` is not in the GenAI spec docs; it appears in the Python instrumentation (B40). | SCV; GAI | SB | SCV docs/non-normative/db-migration.md line 18; grep of GAI docs found no match | "SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`" | grep on both clones | 8 |

### 3. Official Python instrumentations

| ID | Claim | Source key | Class | Place | Quote | Scope and date | Conf. |
|---|---|---|---|---|---|---|---|
| B38 | The GenAI instrumentations moved from opentelemetry-python-contrib to opentelemetry-python-genai; the contrib copies get only security patches and will be removed. | CON | OD | instrumentation-genai/README.md lines 1 to 6 | "The copies that still live in this directory only receive security patches" | contrib at de43f819 | 10 |
| B39 | `opentelemetry-instrumentation-openai-v2` 2.4b0 (2026-05-01) by default follows conventions v1.30.0 and captures no prompt or completion content. | OAV2 | OD | openai_v2/__init__.py docstring, "Configuration" | "By default, the instrumentation aligns with Semantic Conventions v1.30.0 ... and does not capture prompt or completion content." | wheel 2.4b0 | 10 |
| B40 | `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental` opts into the newer conventions; then `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` takes `span_only`, `event_only` or `span_and_event`; on the legacy path it takes `true`. | OAV2 | OD | __init__.py docstring; utils.py line 49 | "Without this flag, the instrumentation stays on v1.30.0 conventions." | same | 10 |
| B41 | On the legacy default path the spans carry `gen_ai.system=openai` (old name), request settings, response model and id, finish reasons and usage tokens; content goes into old-style events `gen_ai.{role}.message` and `gen_ai.choice`, whose body content is only filled when capture is on. | OAV2 | OD | patch.py lines 383 to 486, 845 to 850; utils.py lines 130 to 181 | `event_name=f"gen_ai.{role}.message"` | same | 9 |
| B42 | The 2.4b0 package still records the older metric names `gen_ai.client.operation.duration` and `gen_ai.client.token.usage` (via util-genai 1.2b0), not the newer `gen_ai.client.inference.*` names. | OAV2; UGA | OD | openai_v2/instruments.py; util/genai/_instruments.py lines 88 to 109 | `name=gen_ai_metrics.GEN_AI_CLIENT_TOKEN_USAGE` | wheels 2.4b0 and util-genai 1.2b0 | 9 |
| B43 | Content upload instead of inline capture: `OTEL_INSTRUMENTATION_GENAI_COMPLETION_HOOK=upload` with `OTEL_INSTRUMENTATION_GENAI_UPLOAD_BASE_PATH=<fsspec-uri>` records `gen_ai.input.messages.ref` and `gen_ai.output.messages.ref`. | OAV2 | OD | __init__.py docstring | "Inline content is not captured unless OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT is also set." | same | 9 |
| B44 | There is now an official OpenTelemetry Anthropic instrumentation, `opentelemetry-instrumentation-genai-anthropic` 1.2b0 (2026-09-24, Apache-2.0), plus a new `opentelemetry-instrumentation-genai-openai` 1.2b0. Content is off by default; modes `NO_CONTENT`, `SPAN_ONLY`, `EVENT_ONLY`, `SPAN_AND_EVENT`. | PYG; PYPI | OD | PYG instrumentation/opentelemetry-instrumentation-genai-anthropic/README.rst lines 52 to 61; PyPI JSON | "By default, prompts and completions are not captured." | PYG at cb6592a9; PyPI read 2026-10-20 | 9 |
| B45 | Third-party Anthropic instrumentations also exist: Traceloop's `opentelemetry-instrumentation-anthropic` 0.62.4 and Arize's `openinference-instrumentation-anthropic` 3.0.3, both Apache-2.0. | PYPI | OD | PyPI JSON | n/a (metadata) | read 2026-10-20 | 9 |

### 4. OpenTelemetry Python SDK 1.45.1, offline

| ID | Claim | Source key | Class | Place | Quote | Scope and date | Conf. |
|---|---|---|---|---|---|---|---|
| B46 | `SimpleSpanProcessor` passes each ended span straight to the exporter; `BatchSpanProcessor` queues and batches. | SDK | OD | opentelemetry/sdk/trace/export/__init__.py lines 88 and 143 | "passes ended spans directly to the configured `SpanExporter`" | wheel 1.45.1 | 10 |
| B47 | BatchSpanProcessor defaults: schedule delay 5000 ms, max export batch 512, export timeout 30000 ms, max queue 2048 (env `OTEL_BSP_*`). | SDK | OD | trace/export/__init__.py lines 41 to 44 | `_DEFAULT_MAX_QUEUE_SIZE = 2048` | same | 10 |
| B48 | `InMemorySpanExporter` lives in `opentelemetry.sdk.trace.export.in_memory_span_exporter`; `ConsoleSpanExporter` in `opentelemetry.sdk.trace.export`. | SDK | OD | in_memory_span_exporter.py line 12; export/__init__.py line 291 | `class InMemorySpanExporter(SpanExporter):` | same | 10 |
| B49 | OTLP HTTP exporter default endpoint `http://localhost:4318/` plus `v1/traces`, timeout 10 s; gRPC default `http://localhost:4317`, 6 retries. | HTX; GRX | OD | http trace_exporter/__init__.py lines 61 to 63; grpc exporter.py lines 121 and 286 | `DEFAULT_ENDPOINT = "http://localhost:4318/"` | wheels 1.45.1 | 10 |
| B50 | With no collector running, a span exported through SimpleSpanProcessor plus OTLP/HTTP logged three "Transient error ... retrying" warnings, then "Failed to export spans batch", and blocked the calling thread for about 7.5 s. The application did not crash. | LAB | OD | labtest/t.py run | "Failed to export spans batch due to timeout, max retries or shutdown." | one run, 2026-10-20, Linux, Python 3, 1.45.1 | 8 |
| B51 | In the same run, an in-memory exporter needed no network, and with no settings the resource was `service.name=unknown_service:python`. | LAB | OD | labtest/t.py output | "unknown_service:python" | same | 9 |
| B52 | `OTEL_SERVICE_NAME` sets `service.name` and wins over `OTEL_RESOURCE_ATTRIBUTES`; `OTEL_SDK_DISABLED` defaults to "false". | SDK | OD | sdk/environment_variables/__init__.py lines 4 to 9 and 701 to 715 | "If both are set, OTEL_SERVICE_NAME takes precedence." | same | 10 |

### 5. Tracing tools

| ID | Claim | Source key | Class | Place | Quote | Scope and date | Conf. |
|---|---|---|---|---|---|---|---|
| B53 | Langfuse server is open core: MIT except `ee/`, `web/src/ee/`, `worker/src/ee/` under a commercial licence; copyright now reads ClickHouse, Inc. | LFS | OD | LICENSE lines 1 to 7; ee/LICENSE | "Langfuse is an open core project." | repo at 6343bd81 | 10 |
| B54 | Self-hosted Langfuse reports usage statistics to PostHog by default (no traces or prompts); opt out with `TELEMETRY_ENABLED=false`. The check skips the opt-out when `LANGFUSE_EE_LICENSE_KEY` is set. | LFS | OD | web/src/features/telemetry/README.md; index.ts lines 24 to 33 | "By default, Langfuse automatically reports basic usage statistics to a centralized server (PostHog)." | same | 9 |
| B55 | Langfuse Python SDK 5.0.3 (MIT) defaults `base_url` to `https://cloud.langfuse.com`; `tracing_enabled` and `sample_rate` (default 1.0) switches; accepts OTLP/HTTP at `/api/public/otel/v1/traces`. No PostHog or Sentry code in the wheel (grep for posthog, sentry, segment, usage_stats). | LFP; LFD | OD | langfuse/_client/client.py lines 196 to 214; LFD docs/observability/get-started.mdx line 338 | "Defaults to "https://cloud.langfuse.com"" | wheel 5.0.3 | 9 |
| B56 | Langfuse masking: `mask_otel_spans` (recommended, export stage, covers third-party OTel spans) and legacy `mask` (only Langfuse SDK calls). | LFP; LFD | OD | client.py lines 215 to 218; LFD docs/observability/features/masking.mdx | "Use this for spans created by third-party OpenTelemetry instrumentations" | same | 9 |
| B57 | Arize Phoenix server is Elastic License 2.0 (source-available). Telemetry (FullStory and Scarf.sh) is on by default; `PHOENIX_TELEMETRY_ENABLED=false` turns it off, and it is also off when external resources are disallowed. | PHX; PYPI | OD | LICENSE line 1; src/phoenix/config.py lines 158 and 3706 to 3720 | "When set to False, disables both FullStory and Scarf.sh tracking" | repo at 57b83036; arize-phoenix 20.23.0 on PyPI | 9 |
| B58 | `arize-phoenix-otel` 0.17.2 sends OTLP (default gRPC port 4317; HTTP examples use port 6006 `/v1/traces`), so Phoenix accepts OTLP natively. | PHO | OD | phoenix/otel/settings.py line 31; otel.py line 227 | "The default network port for OTLP/gRPC is 4317." | wheel 0.17.2 | 8 |
| B59 | Self-hosted Phoenix retention: `PHOENIX_DEFAULT_RETENTION_POLICY_DAYS`, default 0. What 0 means was not confirmed in the function read. | PHX | OD | config.py lines 873 and 1053 to 1064 | "defaulting to 0 if not set" | same | 5 |
| B60 | OpenInference uses its own attribute names (`openinference.span.kind` required, `llm.model_name`, `llm.token_count.prompt`, `input.value`), not OTel GenAI names, though it is carried over OTLP. | OI | OD | spec/semantic_conventions.md lines 8, 73, 82, 89, 92, 127 | "The `openinference.span.kind` attribute is required for all OpenInference spans" | repo at ca3ed460; openinference-semantic-conventions 0.1.41 | 9 |
| B61 | OpenInference captures inputs and outputs by default; `OPENINFERENCE_HIDE_INPUTS`, `OPENINFERENCE_HIDE_OUTPUTS` and finer `HIDE_*` switches all default False. | OI | OD | spec/configuration.md lines 9 to 24 | "OPENINFERENCE_HIDE_INPUTS ... bool False" | same | 9 |
| B62 | LangSmith SDK 0.14.11 is MIT. Self-hosted LangSmith is an Enterprise add-on needing a licence key and, unless air-gapped, egress to beacon.langchain.com for licence checks and usage reporting. No posthog or sentry code found in the SDK wheel (grep). | PYPI; LSD; LSP | OD | LSD src/langsmith/kubernetes.mdx lines 8, 44, 100 | "Self-hosted LangSmith is an add-on to the Enterprise plan" | docs at f8f2328e | 9 |
| B63 | LangSmith accepts OTLP at `https://api.smith.langchain.com/otel` (base URL); hides content with `LANGSMITH_HIDE_INPUTS`, `LANGSMITH_HIDE_OUTPUTS`, `LANGSMITH_HIDE_METADATA` or an anonymizer. | LSD; LSP | OD | trace-with-opentelemetry.mdx line 120; mask-inputs-outputs.mdx lines 26 to 27, 118; client.py line 1399 | "LANGSMITH_HIDE_INPUTS=true" | same | 9 |
| B64 | Traceloop SDK 0.62.4 (Apache-2.0) defaults to `https://api.traceloop.com` and records content by default: `TRACELOOP_TRACE_CONTENT` defaults to "true". | TLS | OD | traceloop/sdk/__init__.py line 52; config/__init__.py line 9 | `(os.getenv("TRACELOOP_TRACE_CONTENT") or "true").lower() == "true"` | wheel 0.62.4 | 10 |
| B65 | Traceloop SDK 0.62.4 still accepts `telemetry_enabled=True` but the parameter is not used anywhere and posthog is not a dependency; no self-telemetry code found (grep for posthog, sentry, telemetry_enabled). | TLS | OD | __init__.py line 57 (only occurrence); METADATA Requires-Dist | `telemetry_enabled: bool = True,` | same | 8 |
| B66 | OpenLIT 1.45.0 (Apache-2.0) captures message content by default (`capture_message_content=True`), falls back to the console exporter without an OTLP endpoint, and fetches a pricing JSON from raw.githubusercontent.com unless given `pricing_json`. No PostHog, Segment, Scarf or Sentry code found (grep). | OLT | OD | sdk/python/src/openlit/__init__.py line 192; otel/tracing.py lines 103, 130; __helpers.py lines 518 to 545 | `capture_message_content=True,` | repo at 9654e6c0, pyproject 1.45.0 | 9 |
| B67 | MLflow (Apache-2.0) sends usage telemetry by default; `MLFLOW_DISABLE_TELEMETRY=true` or `DO_NOT_TRACK=true` turns it off; config fetched from `config.mlflow-telemetry.io`. It accepts OTLP at `/v1/traces`. | MLF | OD | mlflow/telemetry/utils.py lines 154 to 155; environment_variables.py line 1632; telemetry/constant.py line 9; tracing/utils/otlp.py line 20 | `MLFLOW_DISABLE_TELEMETRY = _BooleanEnvironmentVariable("MLFLOW_DISABLE_TELEMETRY", False)` | main at 8fe044b5 (3.17.2.dev0), not the 3.17.1 release | 8 |
| B68 | `mlflow.openai.autolog()` logs traces for OpenAI calls by default (`log_traces=True`); the OpenAI Agents SDK tracer is disabled by default. | MLF | OD | mlflow/openai/autolog.py lines 34 to 70 | "If True, traces are logged for OpenAI models." | same | 8 |
| B69 | Opik SDK 2.2.109 (Apache-2.0) sends usage analytics by default to stats.comet.com (forwarded to Segment and PostHog; no trace contents) and Sentry error reports; switches `OPIK_ANALYTICS_ENABLE=false` and `OPIK_SENTRY_ENABLE=false`. Self-hosted backend: `OPIK_USAGE_REPORT_ENABLED` defaults to true in docker-compose. OTLP ingest at `/api/v1/private/otel/v1/traces`. | OPW; OPK | OD | opik/analytics/__init__.py; analytics/comet_stats.py; config.py lines 37, 93, 198, 211; deployment/docker-compose/docker-compose.yaml line 270; docs-v2 integrations microsoft-agent-framework-dotnet.mdx line 58 | "Trace, span, prompt and dataset contents are never sent, nor is the API key." | wheel 2.2.109; repo b53e27c5 | 8 |
| B70 | W&B Weave 0.53.12 (Apache-2.0) sends traces to `https://trace.wandb.ai` by default and Sentry error reports unless `WANDB_ERROR_REPORTING=false`; sentry-sdk is a hard dependency. It has OTel ingest paths (`/otel/v1/traces`, `/agents/otel/v1/traces`). | WV | OD | weave/trace/env.py lines 20, 60; weave/telemetry/trace_sentry.py lines 39 to 86; trace/urls.py line 11 | `return _parse_bool(os.getenv("WANDB_ERROR_REPORTING", "true"))` | wheel 0.53.12 | 8 |
| B71 | Pydantic Logfire: SDK MIT; the server and UI are closed source, self-hosting needs an enterprise licence. `send_to_logfire` defaults to True; with no token, `configure()` tries to create a project; `send_to_logfire='if-token-present'` or False keeps data local. | LGF; LGW | OD | README.md lines 27, 118; _internal/config.py lines 548 to 553, 1243 to 1249 | "the server application for recording and displaying data is closed source" | repo f3fc0ecb; wheel 5.2.0 | 9 |
| B72 | Logfire scrubs by default, matching patterns such as password, secret, auth, api key, session, cookie, credit card; `scrubbing=False` disables it. | LGW | OD | _internal/scrubbing.py lines 38 to 70; config.py line 535 | `'api[._ -]?key',` | same | 9 |
| B73 | Helicone today calls itself "an AI Gateway & LLM Observability Platform": a proxy you point your client's base URL at; Apache-2.0; self-hostable with Docker or Helm. The `helicone` PyPI package (1.0.14) dates from 2023-11-03. | HEL; PYPI | OD | README.md headings and "Self-Hosting"; LICENSE | "Helicone is an AI Gateway & LLM Observability Platform for AI Engineers" | repo 6b057cda | 9 |
| B74 | Helicone can drop bodies per request with headers `Helicone-Omit-Request: true` and `Helicone-Omit-Response: true`. Its docs had no OTLP ingest page (grep of docs/ for otlp and opentelemetry hit one unrelated page). | HEL | OD | docs/helicone-headers/header-directory.mdx lines 147 to 152 | "Whether to exclude the response from the request." (sic) | same | 7 |

### 6. Privacy of traces

| ID | Claim | Source key | Class | Place | Quote | Scope and date | Conf. |
|---|---|---|---|---|---|---|---|
| B75 | The current OWASP list is the "OWASP GenAI LLM Top 10 2026", published August 4, 2026; sensitive information disclosure stays at number two: LLM02:2026. | OW25; OW26 | SB | OW25 README.md line 8; OW26 2026/final/LLM02_SensitiveInformationDisclosure.md line 1 | "Current release: OWASP GenAI LLM Top 10 2026 ... published August 4, 2026." | repos at 99f43955 and 9253e38a | 9 |
| B76 | LLM02:2026 names observability platforms explicitly: they log full prompts, completions and traces by default. | OW26 | SB | LLM02 item 7, "Platform and ecosystem disclosure" | "Observability platforms (Langfuse, LangSmith, Datadog LLM Observability) log full prompts, completions, chunks, and traces by default." | same | 9 |
| B77 | Its mitigations include scrubbing logs and traces before APM ingestion and never logging raw reasoning traces to unrestricted observability. | OW26 | SB | LLM02 prevention items 7 and 11 | "restrict and scrub logs and traces before APM ingestion" | same | 9 |
| B78 | The 2026 list was reordered: LLM03 Excessive Agency, LLM06 Unbounded Consumption, and a new LLM08 Hidden Context Exposure. | OW26 | SB | 2026/final file list | file names LLM03_ExcessiveAgency.md, LLM08_HiddenContextExposure.md | same | 9 |
| B79 | genai.owasp.org's llm-top-10 page still showed only the 2025 list on 2026-10-20. | OWW | SB | web page | "LLM02:2025 Sensitive Information Disclosure" | fetched 2026-10-20 | 7 |

Hosted free-tier retention (as stated by vendors, information only):

| ID | Claim | Source key | Class | Place | Quote | Scope and date | Conf. |
|---|---|---|---|---|---|---|---|
| B80 | Langfuse Cloud: Hobby 30 days, Core 90 days of "data access" (viewing), which the page says is separate from retention (deletion); configurable retention is Pro or Enterprise, minimum 3 days. | LFD | OD | components/home/pricing/PricingFAQ.tsx line 43; PricingTable.tsx line 51; docs/administration/data-retention.mdx | "This is separate from data retention, which deletes data." | docs at ab9037b0 | 8 |
| B81 | LangSmith: base traces 14 days, extended 180 days by default; from September 14, 2026 the SaaS maximum is 180 days; running an online evaluator upgrades the trace to extended retention. | LSD | OD | billing.mdx lines 127 to 130; online-evaluations-llm-as-judge.mdx line 10 | "Base traces have the base retention and are short-lived (14 days)" | docs at f8f2328e | 9 |
| B82 | Pydantic Logfire free (Personal) tier: 30 days retention, about 10 million records a month. | LGFP | VB | pydantic.dev/pricing | "Query your traces, logs, and metrics for the last 30 days." | fetched 2026-10-20 | 7 |
| B83 | Arize AX Free: 15 days retention, 25k spans a month; the pricing page lists no price for self-hosted Phoenix. | ARZ | VB | arize.com/pricing | n/a (table values) | fetched 2026-10-20 | 7 |

### 7. Metrics that matter

| ID | Claim | Source key | Class | Place | Quote | Scope and date | Conf. |
|---|---|---|---|---|---|---|---|
| B84 | Prometheus recommends native histograms over classic histograms and summaries where possible. | PROM | OD | docs/practices/histograms.md lines 12 to 14 | "If you can, use native histograms and prefer them over both classic histograms and summaries." | prometheus/docs at 73e91696 | 9 |
| B85 | Pre-computed quantiles (summaries) cannot be aggregated across replicas; histograms can, with `histogram_quantile()`. | PROM | OD | histograms.md lines 44 to 56, 395 to 406 | "you cannot aggregate quantiles" | same | 9 |
| B86 | Example query: `histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))` for classic histograms. | PROM | OD | histograms.md line 406 | (query as given) | same | 10 |
| B87 | The GenAI token-metrics page shows the same `histogram_quantile(0.95, ...)` pattern and explains why it does not split percentiles by modality. | GAI | SB | gen-ai-token-metrics.md lines 40 to 60 | "percentiles across modalities do not add up" | GAI at 547934af | 9 |
| B88 | The conventions define the parts of an AI dashboard: duration and time to first chunk histograms (seconds), token counters by type, `error.type` for errors by type, and say token counters are the proxy for cost. | GAI | SB | client-inference.md metrics; gen-ai-token-metrics.md lines 30 to 36; changelog.d/536.enhancement.md | "serve as a proxy for cost approximation" | same | 8 |

### 8. Evaluating in production (link to Part 02)

| ID | Claim | Source key | Class | Place | Quote | Scope and date | Conf. |
|---|---|---|---|---|---|---|---|
| B89 | Langfuse: LLM-as-a-judge evaluators run on live observations via rules (filters plus sampling rate); they need an "LLM Connection" (your provider key); the self-hosted worker container calls the model, so it needs egress. | LFD | OD | docs/evaluation/evaluation-methods/llm-as-a-judge.mdx lines 46, 182 to 184, 262 to 264; get-started/online.mdx line 148 | "To use an LLM-as-a-Judge evaluator, you need to set up an LLM Connection." | docs at ab9037b0 | 9 |
| B90 | Phoenix (open source): server LLM evaluators score dataset and experiment outputs using a provider and model configured in the prompt; for evals on production traffic its docs point to the commercial Arize AX "Online Evals". | PHX | OD | docs/phoenix/evaluation/server-evals/llm-evaluators.mdx lines 6, 68 to 72; evaluation/llm-evals.mdx line 88 | "For continuous monitoring of application performance ... see Arize AX Online Evals" | repo at 57b83036 | 8 |
| B91 | LangSmith: online LLM-as-judge evaluators run on production runs with filters and a sampling rate (example 10%), and auto-upgrade those traces to extended retention (higher price); the judge needs a model provider key (or a TypeSafe key for "decision model" judges). | LSD | OD | online-evaluations-llm-as-judge.mdx lines 10, 27 to 48; online-evaluations-decision-models.mdx line 23 | "to control costs, you may want to set a filter to only apply the evaluator to 10% of traces" | docs at f8f2328e | 8 |

## Facts for the lab

- Offline tracing: `TracerProvider()` + `SimpleSpanProcessor(InMemorySpanExporter())`; import from `opentelemetry.sdk.trace.export.in_memory_span_exporter` (B48). `get_finished_spans()` returns spans (B51).
- Console: `ConsoleSpanExporter` from `opentelemetry.sdk.trace.export` (B48).
- Do not pair `SimpleSpanProcessor` with OTLP in a request path when no collector may be running: it blocked about 7.5 s per span in our run (B50). `BatchSpanProcessor` defaults 5000 ms, 512, 30000 ms, 2048 (B47).
- `OTEL_SDK_DISABLED=true` (only the string "true") gives a no-op SDK (B14, B52). `OTEL_SERVICE_NAME` beats `OTEL_RESOURCE_ATTRIBUTES` (B52). Unset gives `unknown_service:python` (B51).
- OTLP: gRPC 4317, HTTP 4318 with path `/v1/traces` (B13, B49).
- Span name for a model call: `chat {model}`; required `gen_ai.operation.name`, `gen_ai.provider.name` (B17, B18). Tool: `execute_tool {tool}`; agent: `invoke_agent {agent}` (B27).
- Token attributes: `gen_ai.usage.input_tokens` (includes cached), `gen_ai.usage.output_tokens`, `gen_ai.usage.cache_read.input_tokens`, `gen_ai.usage.cache_write.input_tokens`, `gen_ai.usage.reasoning.output_tokens` (B18, B19).
- Metrics (new names, unreleased spec): `gen_ai.client.inference.duration`, `gen_ai.client.inference.time_to_first_chunk`, `gen_ai.client.inference.usage.input_tokens` (counter, `{token}`) (B29, B30). Released Python 2.4b0 emits `gen_ai.client.operation.duration` and `gen_ai.client.token.usage` (B42).
- Content capture: `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`; legacy value `true`; with `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental` use `span_only`, `event_only`, `span_and_event` (B40); util-genai 1.2b0 accepts names case-insensitively (`SPAN_ONLY` and so on) and an invalid value such as `true` logs a warning and falls back to `NO_CONTENT` (UGA utils.py lines 32 to 48).
- MCP propagation: put `traceparent` in `params._meta` (B34). W3C example `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01` (B6).
- Tool switches: `PHOENIX_TELEMETRY_ENABLED=false` (B57); `TELEMETRY_ENABLED=false` for self-hosted Langfuse (B54); `MLFLOW_DISABLE_TELEMETRY=true` or `DO_NOT_TRACK=true` (B67); `OPIK_ANALYTICS_ENABLE=false`, `OPIK_SENTRY_ENABLE=false` (B69); `WANDB_ERROR_REPORTING=false` (B70); `logfire.configure(send_to_logfire=False)` (B71); `TRACELOOP_TRACE_CONTENT=false` (B64); `openlit.init(capture_message_content=False)` (B66); `OPENINFERENCE_HIDE_INPUTS=true`, `OPENINFERENCE_HIDE_OUTPUTS=true` (B61); `LANGSMITH_HIDE_INPUTS=true` (B63).
- Prometheus percentile: `histogram_quantile(0.95, sum by (le) (rate(x_bucket[5m])))` (B86).

## Disagreements and surprises

1. Content defaults split the field. The OTel spec and both official instrumentations capture no content by default (B23, B39, B44). Traceloop (B64), OpenLIT (B66) and OpenInference (B61) capture it by default, and OWASP 2026 says observability platforms log full prompts by default (B76). A lab should show the difference.
2. The spec moved ahead of the code. The spec renamed the token metric and the inference duration and TTFT metrics (B36), but the released Python 2.4b0 still emits `gen_ai.client.token.usage`, `gen_ai.client.operation.duration` and the old `gen_ai.system` attribute by default (B41, B42). Dashboards built from the spec and from real instrumentation will not match today.
3. The repo moves: GenAI conventions moved to semantic-conventions-genai on 2026-05-05 (known); the Python GenAI instrumentations also moved, to opentelemetry-python-genai (B38). Is `gen_ai_latest_experimental` still needed with the new 1.2b0 packages? Not checked; the Anthropic README read does not mention it.
4. The series may assume there is no official Anthropic instrumentation. There is one now, `opentelemetry-instrumentation-genai-anthropic` 1.2b0 (B44).
5. `gen_ai.client.operation.duration` is no longer for model calls (B32); `gen_ai.client.inference.duration` replaces it. The span "type" is `gen_ai.client.inference`, but changelog.d/469 writes `gen_ai.inference.client`: an inconsistency inside the repo's own changelog.
6. OWASP: the brief expected LLM02 might move; it stays LLM02 in the 2026 edition (B75), but the OWASP website page still shows 2025 (B79). Other entries moved (B78).
7. Langfuse's `TELEMETRY_ENABLED=false` is ignored when an EE licence key is set (B54). Langfuse "data access" days are not the same as retention (B80).
8. Phoenix open source has evaluators, but its own docs send production online evals to the paid Arize AX (B90). The brief's "online evaluation in Phoenix" row should say so.
9. Traceloop: earlier sources describe its own PostHog telemetry with a `telemetry_enabled` switch; in 0.62.4 the parameter remains but does nothing (B65).
10. LangSmith online evaluators raise cost twice: judge tokens and the forced upgrade to extended retention (B81, B91).
11. Prometheus's histogram page does not itself say "averages mislead"; it shows how to compute an average and why quantiles must come from histograms to aggregate (B85). The "averages hide tail latency" point needs another source.
12. MLflow licence field on PyPI is a Databricks copyright line; the classifier and LICENSE.txt say Apache-2.0. MLflow read at main (3.17.2.dev0), not the 3.17.1 tag.
13. Several repos (contrib, python-genai, Helicone, Phoenix docs) contain AGENTS.md, CLAUDE.md or PROMPT.md files addressed to AI agents. They were not read as instructions.

## Not reached

- OTel website concept pages via WebFetch came back truncated (3 lookups spent); the same pages were read from the opentelemetry.io repository instead.
- What `PHOENIX_DEFAULT_RETENTION_POLICY_DAYS=0` means (B59).
- Whether the new `opentelemetry-instrumentation-genai-*` 1.2b0 packages emit the new metric names or still need `gen_ai_latest_experimental`.
- Helicone hosted free-tier retention, Opik Cloud and W&B Weave free-tier retention, Logfire masking beyond scrubbing patterns, Weave and Opik redaction features.
- MLflow 3.17.1 tag specifically (read main); MLflow autolog span attributes in detail.
- The Gemini report itself; only ledger row P11-05 was read (project file claude/engineering-stack-claim-ledger.md).
- A source for "averages mislead" beyond Prometheus (point 11).

## Sources

| Key | Title | URL or repository at commit | Class | Read |
|---|---|---|---|---|
| GAI | OpenTelemetry GenAI semantic conventions | github.com/open-telemetry/semantic-conventions-genai @547934af | SB | 2026-10-20 |
| SCV | OpenTelemetry semantic conventions (CHANGELOG, migration docs) | github.com/open-telemetry/semantic-conventions @02e6d3e3 | SB | 2026-10-20 |
| SPEC | OpenTelemetry specification (maturity levels, SDK env vars) | github.com/open-telemetry/opentelemetry-specification @e30cae5c | SB | 2026-10-20 |
| PROTO | OTLP specification | github.com/open-telemetry/opentelemetry-proto @09769935 docs/specification.md | SB | 2026-10-20 |
| OIO | opentelemetry.io docs source (traces, sampling, collector) | github.com/open-telemetry/opentelemetry.io @2695b91f | SB | 2026-10-20 |
| W3C | Trace Context, W3C Recommendation 23 November 2021 | https://www.w3.org/TR/trace-context/ | SB | 2026-10-20 |
| CON | opentelemetry-python-contrib | github.com/open-telemetry/opentelemetry-python-contrib @de43f819 | OD | 2026-10-20 |
| PYG | opentelemetry-python-genai | github.com/open-telemetry/opentelemetry-python-genai @cb6592a9 | OD | 2026-10-20 |
| OAV2 | opentelemetry-instrumentation-openai-v2 2.4b0 wheel | pypi.org/project/opentelemetry-instrumentation-openai-v2/2.4b0 | OD | 2026-10-20 |
| UGA | opentelemetry-util-genai 1.2b0 wheel | pypi.org/project/opentelemetry-util-genai/1.2b0 | OD | 2026-10-20 |
| SDK, HTX, GRX | opentelemetry-sdk, exporter-otlp-proto-http, -grpc 1.45.1 wheels | pypi.org | OD | 2026-10-20 |
| LAB | Local run of SDK 1.45.1 with no collector | /home/claude/part13/research/b/labtest/t.py | OD | 2026-10-20 |
| LFS | Langfuse server | github.com/langfuse/langfuse @6343bd81 | OD | 2026-10-20 |
| LFD | Langfuse docs | github.com/langfuse/langfuse-docs @ab9037b0 | OD | 2026-10-20 |
| LFP | langfuse 5.0.3 wheel | pypi.org/project/langfuse/5.0.3 | OD | 2026-10-20 |
| PHX | Arize Phoenix (server and docs) | github.com/Arize-ai/phoenix @57b83036 | OD | 2026-10-20 |
| PHO | arize-phoenix-otel 0.17.2 wheel | pypi.org | OD | 2026-10-20 |
| OI | OpenInference | github.com/Arize-ai/openinference @ca3ed460 | OD | 2026-10-20 |
| LSP | langsmith 0.14.11 wheel | pypi.org | OD | 2026-10-20 |
| LSD | LangChain docs (LangSmith section) | github.com/langchain-ai/docs @f8f2328e | OD | 2026-10-20 |
| TLS | traceloop-sdk 0.62.4 wheel | pypi.org | OD | 2026-10-20 |
| OLM | OpenLLMetry | github.com/traceloop/openllmetry @8d9c93f3 | OD | 2026-10-20 |
| OLT | OpenLIT | github.com/openlit/openlit @9654e6c0 | OD | 2026-10-20 |
| MLF | MLflow | github.com/mlflow/mlflow @8fe044b5 | OD | 2026-10-20 |
| OPW, OPK | opik 2.2.109 wheel; Opik repo | pypi.org; github.com/comet-ml/opik @b53e27c5 | OD | 2026-10-20 |
| WV | weave 0.53.12 wheel | pypi.org | OD | 2026-10-20 |
| LGW, LGF | logfire 5.2.0 wheel; Logfire repo | pypi.org; github.com/pydantic/logfire @f3fc0ecb | OD | 2026-10-20 |
| HEL | Helicone | github.com/Helicone/helicone @6b057cda | OD | 2026-10-20 |
| PROM | Prometheus docs, "Histograms and summaries" | github.com/prometheus/docs @73e91696 docs/practices/histograms.md | OD | 2026-10-20 |
| OW25 | OWASP Top 10 for LLM Applications project site source | github.com/OWASP/www-project-top-10-for-large-language-model-applications @99f43955 | SB | 2026-10-20 |
| OW26 | OWASP GenAI LLM Top 10 2026, final | github.com/GenAI-Security-Project/GenAI-LLM-Top10 @9253e38a 2026/final | SB | 2026-10-20 |
| OWW | OWASP GenAI LLM Top 10 web page | https://genai.owasp.org/llm-top-10/ | SB | 2026-10-20 |
| LGFP | Pydantic pricing | https://pydantic.dev/pricing | VB | 2026-10-20 |
| ARZ | Arize pricing | https://arize.com/pricing/ | VB | 2026-10-20 |
| PYPI | PyPI JSON metadata | https://pypi.org/pypi/NAME/json | OD | 2026-10-20 |
