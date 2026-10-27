import sys
P = "/home/claude/part13/save/p13.md"
t = open(P, encoding="utf-8").read()
E = []
def e(old, new): E.append((old, new))
# Section 5
e("Ask the platform team to turn off buffering on the streaming route anyway, and raise `proxy_read_timeout` above the longest silent thinking time [V: NGX].",
  "Ask the platform team to turn off buffering on the streaming route anyway, and raise `proxy_read_timeout` above the longest silent thinking time, on that route only, with a send timeout and a connection limit beside them (Section 3.1) [V: NGX].")
e("the daily average is 10,000 / 86,400 = 0.93 a second, about 7 streams [V: LIT][T]. Size worker connections, proxy limits and the rate limit for the peak.",
  "the daily average is 10,000 / 86,400 = 0.116 a second, which holds about 0.93 streams open, around one [V: LIT][T]. Size worker connections, proxy limits and the rate limit for the peak of 40, not the average.")
e("*Step 4, tracing.* OpenTelemetry's instrumentation with content capture off, which is its default; a Collector whose attributes processor deletes `gen_ai.input.messages` and `gen_ai.output.messages` in case anyone turns it on; the tracing UI self-hosted with its maker's telemetry switched off [V: OTS, GAI, OPY]. Alerts on p95 time to first token and on errors by type, not on means [V: PRM].",
  "*Step 4, tracing.* OpenTelemetry's instrumentation with content capture off, which is its default [V: OPY]. In case anyone turns it on, a Collector that deletes all four content attributes (`gen_ai.input.messages`, `gen_ai.output.messages`, `gen_ai.system_instructions`, `gen_ai.tool.definitions`) and `url.query` from spans, and filters content-carrying events and log records on the logs pipeline too [V: OTS, GAI]; exceptions recorded by type, not by message; and a test in staging that turns capture on and confirms nothing reaches storage [I]. The gateway strips incoming `traceparent` headers (Section 3.6). The tracing UI is self-hosted, with authentication on, a private address and its maker's telemetry switched off (Section 6). Alerts on p95 time to first token, computed from histograms [V: PRM], and on errors by type, not on means [I].")
e("*Step 5, failures.* Clients treat an `error` event as a failure even after a 200; the server stops reading the model's stream when the browser leaves; retries obey `retry-after`, and an Anthropic 429 with no `retry-after` pages a person instead of retrying [V: AND][T].",
  "*Step 5, failures.* Clients count a turn as done only at its last event, so an `error` event or a stream that just stops is a failure even after a 200; the server stops reading the model's stream when the browser leaves; retries happen in one layer, only before the first token, and obey `retry-after` up to a cap; the spend-cap 429, the one Anthropic 429 without `retry-after`, pages a person instead of retrying [V: AND][T].")
# Section 6
e("in the window that starts it) [R].",
  "in the window that starts it) [R]. If you serve with vLLM, add `VLLM_NO_USAGE_STATS=1` [V: VLM].")
e("- **Skip for new work:** LangServe, archived [V: LCS].",
  "- **Self-hosting a tracing UI:** turn on its authentication, keep it on 127.0.0.1 or a private network, and change every default secret before the first trace. Phoenix's settings default to listening on every address (`0.0.0.0`) with `PHOENIX_ENABLE_AUTH` off, so a solo setup should set `PHOENIX_HOST=127.0.0.1`; Langfuse's Docker Compose file marks its default passwords and keys `# CHANGEME` and publishes the web app's port 3000 on every address [V: PHX, LFS].\n- **Skip for new work:** LangServe, archived [V: LCS].")
# Section 7
e("[R]; on Linux, from the folder holding the zip, `python3 -m zipfile -e engineering-stack-lab-part-13.zip ~/ai-stack` [T].",
  "[R]; on macOS and Linux, from the folder holding the zip, `python3 -m zipfile -e engineering-stack-lab-part-13.zip ~/ai-stack` [T on Linux].")
e("Expect `17 of 17 checks passed` after about five seconds.",
  "Expect `21 of 21 checks passed` after about ten seconds; timings in the output vary from run to run.")
e("This installs FastAPI 0.156.1, uvicorn 0.54.0 and the OpenTelemetry SDK 1.45.1 with their dependencies, 16 packages in all [T]. The script starts FastAPI on 127.0.0.1, blocks and counts any connection that tries to leave your computer, and gives FastAPI a tracer provider without an exporter, so nothing is sent. Expect seven PASS lines, `Network attempts outside this computer: 0 []` and `7 of 7 cross-checks passed` [T on Python 3.13.16, 3.12.3, 3.11.17].",
  """This installs FastAPI 0.156.1, uvicorn 0.54.0 and the OpenTelemetry SDK 1.45.1 with their dependencies, 16 packages in all [T]; on Python 3.11, pip also lists setuptools, and pip may print a notice about a newer version of itself, both harmless [T]. The file pins exact versions but not file hashes. The script starts FastAPI on 127.0.0.1, gives it a tracer provider without an exporter, so nothing is sent, and blocks and counts any attempt to reach another computer through Python's socket functions (TCP and UDP connections and name lookups). That is a check on these libraries, not a sandbox [T]. Expect, abridged [T on Python 3.13.16, 3.12.3, 3.11.17]:

```
fastapi 0.156.1, uvicorn 0.54.0, Python 3.13.16
PASS  X1 the lab's parser reads FastAPI's EventSourceResponse
...
PASS  X7 the lab's traceparent rules match OpenTelemetry's W3C propagator
Network attempts outside this computer: 0 []
7 of 7 cross-checks passed
```""")
e("Open two terminal windows, activate the lab's environment in both, and go to the lab folder.",
  "Open two terminal windows. In each, go to the lab folder, then activate its environment (Section 7.1 or 7.2).")
e("with your own timings [T: on Linux]. Stop the server with Ctrl+C.",
  "with your own timings [T: on Linux]. The stand-in gives the same answer whatever the prompt says [I]. Stop the server with Ctrl+C.")
e("| `python run_lab.py` | 17 checks; exit code 0 only if all pass |\n| `python mutation_check.py` | Breaks the lab 32 ways in temporary copies; each must make `run_lab.py` fail (about 3 minutes) |",
  "| `python run_lab.py` | 21 checks; exit code 0 only if all pass |\n| `python mutation_check.py` | Breaks the lab 48 ways in temporary copies; each must make `run_lab.py` fail (about 5 minutes) |")
e("In your own code, after `import shipmath as sm`:",
  "The lab's server is for learning on 127.0.0.1; don't expose it to a network. From the lab folder, in Python, after `import shipmath as sm`:")
e("| Another program, or an earlier server, holds port 8013 | Stop it, or pass another port (Section 7.5) [T on Linux][R on Windows] |",
  "| Another program, or an earlier server, holds port 8013 | Stop it, or pass another port (Section 7.5) [T on Linux]. On Windows a second server may start without this error, because Python's server asks for address reuse [U] |")
e("| A FastAPI stream shows `data: \"hello\"` with quotes |",
  "| `The stream did not finish (no done event)` from `sse_client.py` | The server stopped mid-stream, or the client's deadline passed | Look at the server's window; restart it [T] |\n| A FastAPI stream shows `data: \"hello\"` with quotes |")
e("The cross-check's packages go with the virtual environment.",
  "The cross-check's packages go with the virtual environment; pip keeps a copy of what it downloaded in its cache, which `python -m pip cache purge` empties (run it before `deactivate`) [T].")
# Section 8
e("**Time:** about 30 minutes by hand, under a minute automated (the mutation check about 3 minutes).",
  "**Time:** about 30 minutes by hand, under a minute automated (the mutation check about 5 minutes).")
e("1. **Read the parser.** Open `ssewire.py`: `Parser._line` is the spec's list of field rules, and `_dispatch` is what happens at a blank line.",
  "1. **Read the parser.** Open `ssewire.py`: `Parser.feed` decodes the bytes, `_lines` splits them at CRLF, LF or CR, `_line` is the spec's list of field rules, and `_dispatch` is what happens at a blank line.")
e("prints three events: `first event` with ID `1`; `second event` with an empty ID, because an `id` line with no value resets it; and ` third event` with its second space kept [T].",
  "prints three events: `first event` with `last_event_id='1'`; `second event` with an empty `last_event_id`, because an `id` line with no value resets it; and ` third event` with its second space kept [T].")
e("`python run_lab.py` now ends `16 of 17 checks passed`, with `FAIL c11_long_context_whole_request: AssertionError 1103/200`: $5.515 instead of $2.77 [T]. Put it back and confirm 17 of 17.",
  "`python run_lab.py` now ends `20 of 21 checks passed`, with `FAIL c11_long_context_whole_request: AssertionError 1103/200`: $5.515 instead of $2.77 [T]. Put it back and confirm 21 of 21.")
e("`python mutation_check.py` breaks the lab 32 ways (comments read as data, the space after the colon kept, a CRLF split across reads counted twice, the buffering header not sent, generation going on after the client leaves, an error sent as a token, no size limit, content captured by default, cached tokens left out of input tokens, an all-zero trace ID accepted, a 400 retried, the batch discount ignored, the server listening on every address, and more) and expects `run_lab.py` to fail each time: `32 of 32 mutations caught` [T].",
  "`python mutation_check.py` breaks the lab 48 ways (comments read as data, the space after the colon kept, a CRLF split across reads counted twice, the buffering header not sent, generation going on after the client leaves, an error sent as a token, no size limit, a wrong field type accepted, no cap on clients, content captured by default, cached tokens left out of input tokens, an all-zero trace ID accepted, a 400 retried, a day-long `retry-after` obeyed, the batch discount ignored, a proxy that trusts any `Content-Length`, an error event that shows internal details, the server listening on every address, and more) and expects `run_lab.py` to fail each time: `48 of 48 mutations caught` [T].")
e("PASS c06_proxy_buffering: header honoured: first token 0.08 of 0.54 s; ignored: 0.54 of 0.54 s, all at once\n...\nPASS c17_standard_library_only: the core lab imports only Python's standard library\n17 of 17 checks passed",
  "PASS c06_proxy_buffering: header honoured: first token 0.08 of 0.54 s; ignored: 0.54 of 0.54 s, all at once\n...\nPASS c21_proxy_refuses_bad_requests: bad Content-Length 400, too big 413, none 411, upstream down 502\n21 of 21 checks passed")
# Section 9
e("**Exercises, with checked answers.** Run the checks from the lab folder.",
  "**Exercises, with checked answers.** Run the checks from the lab folder, with its environment active.")
e("""- *"SSE delivers each token the moment it exists."* Proxies buffer by default, and the spec itself warns about delays [V: NGX, WSS][T].""",
  """- *"SSE delivers each token the moment it exists."* nginx buffers by default, and the spec warns about buffering on the reader's side too [V: NGX, WSS][T].""")
e("""- *"A 200 status means the answer succeeded."* Errors can arrive inside the stream after the 200 [V: AND][T].""",
  """- *"A 200 status means the answer succeeded."* Errors can arrive inside the stream after the 200, and a stream can stop with no event at all; only the last event means done [V: AND, OAS][T].""")
e("""- *"Long-context pricing charges extra only for the extra tokens."* It reprices the whole request [V: OAD, GMD, AND][T].""",
  """- *"Long-context pricing charges extra only for the extra tokens."* At OpenAI and for Haiku 5.5 it reprices the whole request [V: OAD, AND][T].""")
e("From January 1, 2027 the prices double, and so does the answer [V: GMD].",
  "From January 1, 2027 this model's prices double, and so does the answer; other Gemini models change on their own dates [V: GMD].")
e("(2) The status was sent with the first byte; later failures can only be events [V: AND].",
  "(2) The status was sent with the first byte; later failures can only be events, or the stream just stops [V: AND].")
# Section 10
e("- **Routing savings are from 2023 to 2024 model pairs.** RouteLLM's 2x and 85% and FrugalGPT's 98% weren't re-run [V: RTL, FRG][U].",
  "- **Routing savings come from GPT-4-era model pairs.** RouteLLM's 2x and 85% and FrugalGPT's 98% weren't re-run [V: RTL, FRG][U].")
e("- **The proxy is a model of nginx, not nginx.**",
  "- **The lab's server and proxy are teaching code.** They have the limits the security review asked for (checks c18 to c21), not what a public service needs (Section 3.1) [T][I].\n- **The proxy is a model of nginx, not nginx.**")
# Run on your computer
e("| R1 | `python run_lab.py` | `17 of 17 checks passed` |\n| R2 | `python mutation_check.py` | `32 of 32 mutations caught` |",
  "| R1 | `python run_lab.py` | `21 of 21 checks passed` |\n| R2 | `python mutation_check.py` | `48 of 48 mutations caught` |")
# Cheat sheet
e("long-context price     = applies to the whole request once the prompt passes the line",
  "long-context price     = OpenAI and Haiku 5.5: the whole request, once the prompt passes the line")
e("Content by default Traceloop, OpenLIT and OpenInference: on; OpenTelemetry's own: off",
  "Content by default Traceloop, OpenLIT, OpenInference, Logfire: on; OpenTelemetry's own: off")
e("3. Treat an `error` event as a failure even after a 200; stop generating when the reader leaves.\n4. Obey `retry-after`; never retry a 400; a spend-cap 429 needs a person.\n5. Trace every model call with the GenAI names; keep content capture off and delete content in the Collector too.\n6. Turn off each tracing tool's own telemetry before its first run.",
  "3. A stream is done only at its last event; an `error` event or a silent stop is a failure even after a 200. Stop generating when the reader leaves.\n4. Retry in one layer, with a budget, never after the first token; obey `retry-after` up to a cap; never retry a 400; a spend-cap 429 needs a person.\n5. Trace every model call with the GenAI names; keep content capture off, and delete all four content attributes, `url.query`, content events and logs in the Collector too.\n6. Turn off each tool's own telemetry (vLLM's too) before its first run; give a self-hosted UI authentication and a private address.")
e("8. Alert on percentiles from histograms, not on means.",
  "8. Alert on percentiles from histograms, not on means.\n9. Authenticate, cap open streams and spend per key, time out slow clients, and don't trust a `traceparent` from outside.")
# Section 12 rows
e("| Event types, mid-stream errors, resuming, 429 and 529, tiers and spend caps,",
  "| Event types and the final `message_stop`, mid-stream errors, resuming, 429 and 529, tiers and spend caps,")
e("| LFS | langfuse/langfuse at 6343bd8 (LICENSE, telemetry); langfuse/langfuse-docs at ab9037b; langfuse 5.0.3 wheel | OD | Licence split, telemetry switch, masking, retention, online evaluation | 9 |",
  "| LFS | langfuse/langfuse at 6343bd8 (LICENSE, telemetry, `docker-compose.yml`); langfuse/langfuse-docs at ab9037b; langfuse 5.0.3 wheel | OD | Licence split, telemetry switch, default secrets and ports, masking, retention, online evaluation | 9 |")
e("| LGF | pydantic/logfire at f3fc0ec; logfire 5.2.0 wheel; pydantic.dev pricing | OD, VB | Closed server, `send_to_logfire`, scrubbing, retention | 8 |",
  "| LGF | pydantic/logfire at f3fc0ec; logfire 5.2.0 wheel (`_internal/main.py`, `integrations/llm_providers/openai.py`); pydantic.dev pricing | OD, VB | Closed server, `send_to_logfire`, messages recorded by `instrument_openai`, scrubbing, retention | 8 |")
e("pp. 536 to 549 (reprint) | PR | L = λW and its conditions | 8 |",
  "pp. 536 to 549 (reprint; neither blind checker could open it) | PR | L = λW and its conditions | 6 |")
e("| PHX | Arize-ai/phoenix at 57b8303 (LICENSE, `config.py`, docs); arize-phoenix-otel 0.17.2 wheel; Arize pricing page | OD, VB | Licence, telemetry switch, OTLP, evaluation scope, AX retention | 9 |",
  "| PHX | Arize-ai/phoenix at 57b8303 (LICENSE, `config.py`, docs); arize-phoenix-otel 0.17.2 wheel; Arize pricing page | OD, VB | Licence, telemetry switch, default host and authentication, OTLP, evaluation scope, AX free tier and retention | 9 |")
e("| VLM | vllm-project/vllm at 7b569ec (main): OpenAI-compatible server docs, `envs.py`, usage-stats docs | OD | Routes and gaps; usage statistics on by default | 9 |",
  "| VLM | vllm-project/vllm at 7b569ec (main): OpenAI-compatible server docs, `envs.py` (lines 831 to 835), usage-stats docs | OD | Routes and gaps; usage statistics on by default and their switches | 9 |")
e("| WSS | WHATWG HTML Living Standard, 9.2 \"Server-sent events\" (last updated October 20, 2026) | SB | Wire format, parsing rules, authoring notes | 10 |",
  "| WSS | WHATWG HTML Living Standard, 9.2 \"Server-sent events\" (last updated October 20, 2026) | SB | Wire format, parsing rules, `EventSource`, reconnection and 204, authoring notes | 10 |")
for old, new in E:
    n = t.count(old)
    if n != 1:
        print("COUNT", n, repr(old[:90])); sys.exit(1)
    t = t.replace(old, new)
open(P, "w", encoding="utf-8").write(t)
print("applied", len(E))
