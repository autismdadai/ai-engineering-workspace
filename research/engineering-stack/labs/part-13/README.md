# Engineering Stack, Part 13 lab: shipping and operating

Put a (stand-in) model behind a streaming API, watch a proxy buffer it, trace
it without recording prompts, and do the cost and load arithmetic.
Standard library only, Python 3.11 to 3.13; no model, account or key.

| File | What it is |
|---|---|
| `shipmath.py` | Cost per request (cache, batch, data residency, long-context rules), Little's law, percentiles, when to retry, W3C `traceparent`, GenAI span attributes. Printed in Part 13's appendix |
| `ssewire.py` | Server-Sent Events encoder and parser, following the WHATWG spec |
| `stream_server.py` | A stand-in model streamed over SSE on 127.0.0.1:8013 (timings invented; a teaching server, not for production) |
| `sse_client.py` | Reads the stream and times it |
| `buffer_proxy.py` | A proxy that buffers like nginx's default, unless told `X-Accel-Buffering: no` |
| `tinytrace.py` | A tiny tracer that shows what spans are |
| `run_lab.py` | 21 checks; exit code 0 only if all pass |
| `mutation_check.py` | Breaks the lab 48 ways in temporary copies; each must fail (about 5 minutes) |
| `demo.py` | The worked tables behind the part |
| `crosscheck.py`, `requirements-crosscheck.txt` | Optional: the same rules against FastAPI 0.156.1 and the OpenTelemetry SDK 1.45.1 |

Start: `python run_lab.py`. Then `python demo.py`.
Two windows: `python stream_server.py` in one, `python sse_client.py "your prompt"` in the other.
Prices were read on October 20, 2026; they change, so pass your own.
