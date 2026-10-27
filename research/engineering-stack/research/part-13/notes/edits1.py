import sys
P = "/home/claude/part13/save/p13.md"
t = open(P, encoding="utf-8").read()
E = []
def e(old, new):
    E.append((old, new))

# Section 1
e("Every big vendor streams this way [V: AND, OAD, GMD].",
  "Every big vendor streams this way; Gemini's REST API does when you add `alt=sse` to the URL [V: AND, OAD, GMD].")
e("The conventions say prompts and answers must not be recorded unless you switch that on [V: GAI];",
  "The conventions say instrumentations SHOULD NOT record prompts and answers unless you switch that on [V: GAI];")
e("Speed has two numbers: how soon the first words appear and how long the whole answer takes [V: AND, OAD].",
  "Speed has two numbers: how soon the first words appear and how long the whole answer takes [V: AND].")
# Definitions
e("| A higher price for the whole request past a length | Long-context pricing | OpenAI over 272,000 tokens; Gemini 3.1 Pro over 200,000; Haiku 5.5 over 100,000 [V: OAD, GMD, AND] |",
  "| A higher price once a prompt passes a length | Long-context pricing | OpenAI over 272,000 tokens and Haiku 5.5 over 100,000, for the whole request; Gemini 3.1 Pro over 200,000 [V: OAD, AND, GMD] |")
e("| Sending easy requests to a cheaper model | Model routing | Savings depend on the model pair [V: RTL] |",
  "| Sending easy requests to a cheaper model | Model routing | Savings were measured on particular model pairs [V: RTL] |")
# 3.1
e("streams the answer back. The Gemini report's advice",
  "streams the answer back. The Gemini report's advice")
e("""(ledger P11-06) [V: VLM, OLL, LCP].

**OpenAI-compatible, mostly.**""",
"""(ledger P11-06) [V: VLM, OLL, LCP].

**What a public endpoint needs.** A model behind a public URL spends your money on every request, so the limits come first [I: from this part's security review]. Authenticate every request, with keys stored hashed, scoped and easy to rotate, and rate-limit failed attempts. Cap open streams per key and per IP address: a per-minute request limit doesn't stop one key from holding dozens of long streams. Cap input size and `max_tokens` on the server, where the client can't raise them. Time out slow headers, slow bodies and idle streams, and set a longest stream length. Enforce a daily spending cap per key before calling the model; an alarm only tells you after the money is gone. Turning off proxy buffering (Section 3.3) also removes the proxy's shield against slow readers, so scope that change to the streaming route and pair it there with a send timeout and a connection limit (nginx's `send_timeout` and `limit_conn`; not run against nginx here) [U]. The lab's server shows some of this in miniature (Section 3.5); it's a teaching server for 127.0.0.1, not one to put on a network.

**OpenAI-compatible, mostly.**""")
e("Test the features you use against the engine you run.",
  "Test the features you use against the engine you run. vLLM also sends anonymous usage statistics to its makers by default; `VLLM_NO_USAGE_STATS=1` or `DO_NOT_TRACK=1` switches that off [V: VLM].")
e("since 0.135.0 (March 1, 2026): return `EventSourceResponse` and yield events [V: FAS].",
  "since 0.135.0 (March 1, 2026): set `response_class=EventSourceResponse` on the route and yield events [V: FAS].")
e("Since 0.143.0 (October 8, 2026), FastAPI also creates OpenTelemetry spans by itself when you give it a tracer provider, and sets up exporters from `OTEL_*` variables only if you opt in with `FASTAPI_OTEL_AUTO_CONFIGURE=true` [V: FAS][T].",
  "Since 0.142.0 (September 29, 2026), FastAPI also creates OpenTelemetry spans by itself when you give it a tracer provider; since 0.143.0 (October 8, 2026) it sets up exporters from `OTEL_*` variables only if you opt in with `FASTAPI_OTEL_AUTO_CONFIGURE=true` [V: FAS][T].")
e("LangChain's pricing page lists self-hosting only on its Enterprise plan,",
  "LangChain's docs describe self-hosting as an add-on to its Enterprise plan,")
e("""Kubernetes' own page treats tenant isolation as "a broad spectrum" with "no single definition", lists the tools (namespaces, access control, quotas, network policies, sandboxed containers, dedicated nodes) and recommends sandboxing "when you are running untrusted code", because ordinary containers share the host's kernel [V: K8S].""",
  """Kubernetes' own page says there is "no single definition" of how hard or soft isolation is, calls it "a broad spectrum", lists the tools (namespaces, access control, quotas, network policies, sandboxed containers, dedicated nodes) and says sandboxing "is often recommended when you are running untrusted code", because ordinary containers share the host's kernel [V: K8S].""")
# 3.2
e("and the openai SDK 3.35.1 adds a persistent WebSocket mode for the Responses API that accepts `response.steer` events while an answer is being written [V: OAD, OAS].",
  "and the openai SDK 3.35.1 has a persistent WebSocket mode for the Responses API, with a beta `response.steer` event for steering an answer while it's being written [V: OAD, OAS].")
e("""The spec itself only says clients with per-server limits "might run into trouble" [V: WSS].""",
  """The spec itself only says clients with per-server limits "might run into trouble" [V: WSS].

**From a browser.** Keep the vendor's API key on your server; a key in browser code is public. `EventSource` makes a plain GET request and can't add an `Authorization` header [V: WSS], so people put keys in the URL, where they reach proxy logs, browser history and traces: FastAPI 0.156.1's own spans record the query string as `url.query` [T: this part's security review]. Either authenticate the stream with a same-site, `HttpOnly` cookie and check the `Origin` header, or read the stream with `fetch()`, which can send headers. Allow only your own origins in CORS (FastAPI's `CORSMiddleware` with an explicit `allow_origins` list, never `*` together with credentials) [I].""")
# 3.3
e("""4. **The spec's own warning:** buffering "can cause delays in event dispatch" [V: WSS].""",
  """4. **The reader.** The spec warns that block or line buffering on the receiving side "can cause delays in event dispatch", so a client should handle each line as it arrives [V: WSS].""")
e("**What to do.** Send `X-Accel-Buffering: no` and `Cache-Control: no-cache` (FastAPI and sse-starlette do) [V: FAS, SSS];",
  "**What to do.** Send `X-Accel-Buffering: no` and a `Cache-Control` header that stops caching (FastAPI sends `no-cache`, sse-starlette `no-store`) [V: FAS, SSS];")
# 3.4
e("So a client must check event types, not only the status code. The lab's server sends three words, then an error event, and no usage event (check c07) [T].",
  "So a client must check event types, not only the status code, and should count a stream as finished only when its last event arrives (`message_stop` at Anthropic, `response.completed` at OpenAI, `done` in the lab). A stream that simply stops, with no error event, is a failure too [V: AND, OAS]. The lab's server sends three words, then an error event, and no usage event (check c07); its client reports a stream with no `done` as unfinished and gives up after a total deadline (check c20) [T]. Keep error events short, a code and a plain message, never the vendor's raw error body or a stack trace; log the details on your server. The lab's server sends `server_error` with \"the stream failed\" for any crash and records only the exception's type (check c20) [T].")
# 3.5
e("A 429 is your organization's limit and comes with `retry-after`;",
  "A 429 is your organization's limit and usually comes with `retry-after`;")
e("""An HTTP-date `retry-after` falls back to the backoff in the lab, a simplification [I].

**Your own limits.** An API that calls a paid model needs its own: per-key request and token limits, a request-size limit, and a spending alarm. FastAPI has no built-in limiter; slowapi (MIT), fastapi-limiter (Apache-2.0) and limits (MIT) are common choices [V: FAS, PYPI]. The lab's server refuses bodies over 64 KB before reading them, checks an optional API key in constant time (`hmac.compare_digest`) and listens only on 127.0.0.1 (check c09) [T].""",
"""It also caps the wait: it obeys up to 60 seconds, gives up beyond that, and ignores a value that isn't a plain number, so an HTTP-date `retry-after` falls back to the backoff, a simplification [T][I].

**Don't multiply retries.** The SDKs already retry twice [V: OAS, ANS]. Your own loop of three tries around them makes nine paid calls for one user request during an outage, and a gateway that also retries makes more [I: arithmetic]. Retry in one layer: if your code retries, set the SDK's `max_retries=0`. Give each user request a retry budget and a total deadline. Retry a stream only before its first token; after that, a retry pays again for the input and every token already written, so report the error instead. Browsers add a loop of their own: `EventSource` reconnects by itself after a dropped stream, so a server that starts a fresh generation on each reconnect pays each time. Resume from `Last-Event-ID`, or answer with HTTP 204 No Content, which tells `EventSource` to stop reconnecting [V: WSS].

**Your own limits.** Section 3.1 lists what a public endpoint needs. FastAPI has no built-in limiter; slowapi (MIT), fastapi-limiter (Apache-2.0) and limits (MIT) are common choices [V: FAS, PYPI]. The lab's server refuses bodies over 64 KB before reading them, answers a wrong field type with a 400 before any stream starts, drops a client that stays silent for 30 seconds, answers 503 past 32 clients at once, checks an optional API key in constant time (`hmac.compare_digest`) and listens only on 127.0.0.1 (checks c09, c18 and c20). Its buffering proxy refuses a bad or missing `Content-Length` and answers 502 when the server is down (check c21) [T].""")
# 3.6
e("whose last bit says the caller sampled it [V: W3C].",
  "whose last bit says the caller may have recorded it [V: W3C].")
e("""and is harder to run [V: OTS].""",
  """and is harder to run [V: OTS].

**At the public edge, don't trust an incoming `traceparent`.** Any caller can send one with trace IDs of its choosing, and a parent-based sampler follows the caller's flag. With the SDK 1.45.1 and `ParentBased(TraceIdRatioBased(0.01))`, a client sending flag `01` had 1,000 of 1,000 requests kept, one sending `00` had none, and requests with no header 7 of 1,000 [T: this part's security review]. Strip the header at your gateway, or give `ParentBased` ratio samplers for remote parents as well (`remote_parent_sampled` and `remote_parent_not_sampled`), so a caller can't change what you keep; treat the `baggage` header the same way [V: OTS]. Between your own services, joining the trace is the point.

**Exporting beyond your computer.** Over the network, export over TLS (`https://` endpoints), keep the Collector's receivers on a private address, and treat `OTEL_EXPORTER_OTLP_HEADERS`, which often holds a hosted platform's key, as a secret [V: OTS][I].""")
# 3.7
e("Structured content goes on spans as a JSON string [V: GAI].",
  "Where a language can't put structured values on spans, the content goes there as a JSON string [V: GAI].")
e("The Python GenAI instrumentations have also moved, to `opentelemetry-python-genai`, which now includes an official Anthropic instrumentation,",
  "The Python GenAI instrumentations have also moved, to `opentelemetry-python-genai`; the copies left in the contrib repository, openai-v2 2.4b0 among them, get security patches only. The new repository includes an official Anthropic instrumentation,")
e("The lab's server joins an incoming trace, and its model-call span is the server span's child (check c16) [T].",
  "The lab's server joins an incoming trace, as an internal service should (Section 3.6), and its model-call span is the server span's child (check c16) [T].")
# 3.8
e("| Scrubs common secrets by default |",
  "| Yes: `instrument_openai()` records `gen_ai.input.messages`; it also scrubs values that look like secrets |")
e("| It logs what it proxies; `Helicone-Omit-Request` and `-Response` headers leave bodies out |",
  "| It logs what it proxies, and as a proxy it sees your vendor API key on every request; `Helicone-Omit-Request` and `-Response` headers leave bodies out |")
e("**Defaults disagree:** OpenTelemetry's own instrumentations record no prompts, while Traceloop, OpenLIT and OpenInference record them unless told not to [V: OPY, TLP, OLT, OIN].",
  "**Defaults disagree:** OpenTelemetry's own instrumentations record no prompts, while Traceloop, OpenLIT, OpenInference and Logfire record them unless told not to [V: OPY, TLP, OLT, OIN, LGF].")
e("Phoenix, MLflow, Opik, Weave and the self-hosted Langfuse server report usage by default [V: PHX, MLF, OPK, WVE, LFS].",
  "Phoenix, MLflow, Opik and the self-hosted Langfuse server report usage by default, Weave sends error reports, and vLLM (Section 3.1) sends usage statistics [V: PHX, MLF, OPK, LFS, WVE, VLM].")
e("open-source Phoenix runs evaluators on datasets, and its docs send production monitoring to the paid Arize AX [V: LFS, LSM, PHX].",
  "open-source Phoenix can run evaluators on production traces as well as datasets, and its docs send continuous monitoring with alerts to Arize AX, which has a free tier [V: LFS, LSM, PHX].")
# 3.9
e("**Fast** (called \"Priority processing\" until July 30, 2026) at about twice the standard price [V: OAD].",
  "**Fast** (called \"Priority processing\" until July 30, 2026) at a higher price; for GPT-5.6 Sol, OpenAI states twice the standard rate [V: OAD].")
e("""**Long-context pricing applies to the whole request.** One token over the line changes the price of all of them [V: OAD, GMD, AND]. The lab's `request_cost` encodes this [T]:""",
  """**Long-context pricing can apply to the whole request.** OpenAI prices GPT-6 Astra past 272,000 input tokens at higher rates "for the full request", and Anthropic says a Haiku 5.5 request over its threshold pays the higher prices; Anthropic's other current models have no long-context surcharge [V: OAD, AND]. Google's pricing page shows Gemini 3.1 Pro's higher tier without saying whether it covers the whole prompt or only the excess [V: GMD][U]. The lab's `request_cost` reprices the whole request for all three [T]:""")
e("The lab also doubles OpenAI's cache-write rate past the line,",
  "For Gemini that is an assumption [U]. The lab also doubles OpenAI's cache-write rate past the line,")
e("claude-haiku-5-5          $0.00045  batch  $0.00022  x 10,000 a day for 30 days    $135.00",
  "claude-haiku-5-5         $0.000450  batch $0.000225  x 10,000 a day for 30 days    $135.00")
e("""its repository claims up to 85% while keeping 95% of GPT-4's MT-Bench score, and the FrugalGPT preprint up to 98%, all on 2023 to 2024 model pairs [V: RTL, FRG].""",
  """its repository claims up to 85% while keeping 95% of GPT-4's MT-Bench score, with GPT-4 as the strong model and Mixtral 8x7B as the weak one, and the FrugalGPT preprint up to 98% against GPT-4 [V: RTL, FRG]. Those are older models; whether the savings hold for today's pairs wasn't checked [U].""")
# 3.10
e("and the share of streams that ended early (client gone, timeout, error).",
  "and the share of streams that ended early (client gone, timeout, error), this part's own suggestion [I].")
# Section 4
e("""| Wrong as worded. The spec warns buffering "can cause delays in event dispatch"; nginx buffers proxied responses by default; the lab's stream""",
  """| Wrong as worded. nginx buffers proxied responses by default; the spec warns that buffering in the reader "can cause delays in event dispatch"; the lab's stream""")
e("""| Overstated. Kubernetes calls isolation "a broad spectrum" with "no single definition" and recommends sandboxing for untrusted code, or separate clusters for some cases [V: K8S] |""",
  """| Overstated. Kubernetes calls isolation "a broad spectrum" and says sandboxing "is often recommended" for untrusted code, with separate clusters for some cases [V: K8S] |""")
e("its successor was renamed LangSmith Deployment and self-hosts only on an Enterprise plan. FastAPI is current and now has built-in SSE (0.135.0) and OpenTelemetry (0.143.0) [V: LCS, FAS] |",
  "its successor was renamed LangSmith Deployment, and self-hosting it is an Enterprise add-on. FastAPI is current and now has built-in SSE (0.135.0) and OpenTelemetry (0.142.0) [V: LCS, FAS] |")
e("| Consistent with the vendors' latency advice; the savings are 2x to 98% depending on the study and model pair, all on 2023 to 2024 models [V: RTL, FRG, AND, OAD] | 3.9 |",
  "| In the spirit of the vendors' advice to pick a faster or smaller model; research reports 2x to 98% savings, measured on GPT-4-era model pairs [V: RTL, FRG, AND, OAD] | 3.9 |")
e("| Still Elastic License 2.0 at 20.23.0; its open-source version evaluates datasets, and its docs send live-traffic evaluation to the paid Arize AX [V: PHX] | 3.8 |",
  "| Still Elastic License 2.0 at 20.23.0; it can evaluate production traces itself, and its docs send continuous monitoring with alerts to Arize AX [V: PHX] | 3.8 |")
for old, new in E:
    n = t.count(old)
    if n != 1:
        print("COUNT", n, old[:80]); sys.exit(1)
    t = t.replace(old, new)
open(P, "w", encoding="utf-8").write(t)
print("applied", len(E))
