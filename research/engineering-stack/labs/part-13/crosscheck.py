"""crosscheck: the lab's SSE parser and tracing rules against real libraries
(Engineering Stack, Part 13).

Needs the packages in requirements-crosscheck.txt (FastAPI 0.156.1, uvicorn
0.54.0, the OpenTelemetry SDK 1.45.1) in this lab's virtual environment.
Everything runs on 127.0.0.1; no exporter is configured, so no telemetry
leaves the computer, and no account or key is needed.
"""
from __future__ import annotations

import asyncio
import http.client
import ipaddress
import json
import os
import socket
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.pop("FASTAPI_OTEL_AUTO_CONFIGURE", None)   # keep FastAPI from setting up exporters

try:
    import fastapi
    import fastapi.routing
    import uvicorn
    from fastapi.sse import EventSourceResponse, ServerSentEvent
    from opentelemetry.propagators.textmap import DefaultGetter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
    from opentelemetry.trace import get_current_span
    from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
except ImportError as error:
    print(f"Install the cross-check packages first (Part 13, Section 7.4): {error}")
    sys.exit(2)

_outside = []
_real = {"connect": socket.socket.connect, "connect_ex": socket.socket.connect_ex,
         "sendto": socket.socket.sendto, "getaddrinfo": socket.getaddrinfo}


def _local(host) -> bool:
    host = str(host)
    if host == "localhost" or host == "":
        return True
    try:
        return ipaddress.ip_address(host.split("%")[0]).is_loopback
    except ValueError:
        return False


def _check(address) -> None:
    if not isinstance(address, tuple):
        return                      # a Unix socket path stays on this computer
    host = address[0]
    if not _local(host):
        _outside.append(str(host))
        raise OSError(f"blocked by the lab: {host}")


def _connect(self, address):
    _check(address)
    return _real["connect"](self, address)


def _connect_ex(self, address):
    _check(address)
    return _real["connect_ex"](self, address)


def _sendto(self, data, *args):
    _check(args[-1])
    return _real["sendto"](self, data, *args)


def _getaddrinfo(host, *args, **kwargs):
    if host is not None and not _local(host if not isinstance(host, bytes) else host.decode()):
        _outside.append(str(host))
        raise OSError(f"blocked by the lab: {host}")
    return _real["getaddrinfo"](host, *args, **kwargs)


# Anything that tries to leave this computer (TCP, UDP or a name lookup) is stopped and logged.
socket.socket.connect, socket.socket.connect_ex = _connect, _connect_ex
socket.socket.sendto, socket.getaddrinfo = _sendto, _getaddrinfo

import shipmath as sm  # noqa: E402
import ssewire  # noqa: E402

RESULTS = []
yields = {"count": 0}


def result(ok: bool, name: str, detail: str) -> None:
    RESULTS.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}\n      {detail}")


def make_app(provider: TracerProvider) -> fastapi.FastAPI:
    app = fastapi.FastAPI(telemetry={"tracer_provider": provider})

    @app.post("/sse", response_class=EventSourceResponse)
    async def sse():
        yield ServerSentEvent(data="hello", event="token", id="1")
        yield {"text": "a dict"}
        yield ServerSentEvent(raw_data="plain text")

    @app.post("/slow", response_class=EventSourceResponse)
    async def slow():
        await asyncio.sleep(0.7)
        yield ServerSentEvent(data="late")

    @app.post("/long", response_class=EventSourceResponse)
    async def long():
        for i in range(200):
            yields["count"] += 1
            yield ServerSentEvent(data=i)
            await asyncio.sleep(0.02)

    return app


def start(app) -> tuple[uvicorn.Server, int]:
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, log_level="warning", lifespan="off"))
    threading.Thread(target=lambda: asyncio.run(server.serve(sockets=[sock])), daemon=True).start()
    for _ in range(100):
        if server.started:
            break
        time.sleep(0.05)
    return server, port


def post(port: int, path: str, read_events: int | None = None):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=20)
    conn.request("POST", path, body=b"{}", headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    raw, events, parser = b"", [], ssewire.Parser()
    while True:
        chunk = resp.read1(256)
        if not chunk:
            break
        raw += chunk
        events += parser.feed(chunk)
        if read_events is not None and len(events) >= read_events:
            break
    headers = {k.lower(): v for k, v in resp.getheaders()}
    conn.close()
    return headers, raw, events


def main() -> int:
    print(f"fastapi {fastapi.__version__}, uvicorn {uvicorn.__version__}, Python {sys.version.split()[0]}")
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    fastapi.routing._PING_INTERVAL = 0.2     # FastAPI's keep-alive is 15 s; shortened for the test
    server, port = start(make_app(provider))
    try:
        headers, raw, events = post(port, "/sse")
        got = [(e.type, e.data, e.last_event_id) for e in events]
        want = [("token", '"hello"', "1"), ("message", '{"text": "a dict"}', "1"),
                ("message", "plain text", "1")]
        result(got == want, "X1 the lab's parser reads FastAPI's EventSourceResponse",
               f"{got}; note the JSON quotes around a plain string")
        ok = headers.get("x-accel-buffering") == "no" and headers.get("cache-control") == "no-cache" \
            and headers.get("content-type", "").startswith("text/event-stream")
        result(ok, "X2 FastAPI sets the anti-buffering headers itself",
               f"content-type {headers.get('content-type')}, cache-control "
               f"{headers.get('cache-control')}, x-accel-buffering {headers.get('x-accel-buffering')}")

        _, raw, events = post(port, "/slow")
        result(raw.startswith(b": ping") and [e.data for e in events] == ['"late"'],
               "X3 an idle FastAPI stream sends ': ping' comments, which the parser skips",
               f"first bytes {raw[:20]!r}; events {[e.data for e in events]}")

        post(port, "/long", read_events=3)
        time.sleep(0.6)
        first = yields["count"]
        time.sleep(0.6)
        result(first < 200 and yields["count"] == first,
               "X4 FastAPI stops the generator when the client leaves",
               f"the client read 3 events and left; the generator stopped at {first} of 200")

        names = [s.name for s in exporter.get_finished_spans()]
        result(any("/sse" in n for n in names),
               "X5 FastAPI 0.156.1 makes its own spans when given a tracer provider",
               f"span names seen: {sorted(set(names))[:6]}")
    finally:
        server.should_exit = True
        time.sleep(0.3)

    exporter.clear()
    tracer = provider.get_tracer("lab")
    usage = {"input": 200, "cache_read": 1_800, "output": 50}
    name, attrs = sm.chat_span("anthropic", "claude-sonnet-5-5", usage, ["end_turn"])
    with tracer.start_as_current_span(name, attributes=attrs):
        pass
    span = exporter.get_finished_spans()[0]
    same = span.name == name and {k: (list(v) if isinstance(v, tuple) else v)
                                  for k, v in span.attributes.items()} == attrs
    result(same, "X6 the lab's GenAI span attributes are valid OpenTelemetry attributes",
           f"{span.name}: {len(span.attributes)} attributes kept unchanged by SDK 1.45.1")

    example = "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"
    ctx = TraceContextTextMapPropagator().extract({"traceparent": example}, getter=DefaultGetter())
    sc = get_current_span(ctx).get_span_context()
    mine = sm.parse_traceparent(example)
    zero = TraceContextTextMapPropagator().extract(
        {"traceparent": "00-" + "0" * 32 + "-00f067aa0ba902b7-01"}, getter=DefaultGetter())
    ok = f"{sc.trace_id:032x}" == mine["trace_id"] and f"{sc.span_id:016x}" == mine["parent_id"] \
        and sc.trace_flags.sampled == mine["sampled"] \
        and not get_current_span(zero).get_span_context().is_valid
    result(ok, "X7 the lab's traceparent rules match OpenTelemetry's W3C propagator",
           f"trace {sc.trace_id:032x}, parent {sc.span_id:016x}, sampled {sc.trace_flags.sampled}; "
           "an all-zero trace ID is invalid in both")

    print(f"Network attempts outside this computer: {len(_outside)} {sorted(set(_outside))}")
    print(f"{sum(RESULTS)} of {len(RESULTS)} cross-checks passed")
    return 0 if all(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
