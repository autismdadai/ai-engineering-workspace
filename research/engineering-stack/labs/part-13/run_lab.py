"""run_lab: every check for Part 13's lab. Exit code 0 only if all pass.

Standard library only. The streaming checks start a stand-in server and two
proxies on 127.0.0.1 with ports the system picks, and stop them at the end.
"""
from __future__ import annotations

import ast
import json
import os
import sys
import time
import traceback
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import buffer_proxy  # noqa: E402
import shipmath as sm  # noqa: E402
import ssewire  # noqa: E402
import sse_client  # noqa: E402
import stream_server  # noqa: E402

CHECKS = []


def check(fn):
    CHECKS.append(fn)
    return fn


_SERVER = {}


def server_port() -> int:
    if "httpd" not in _SERVER:
        _SERVER["httpd"] = stream_server.serve(0)
    return _SERVER["httpd"].server_address[1]


# ------------------------------------------------------------- SSE wire
@check
def c01_sse_encode():
    got = ssewire.encode("line one\nline two", event="token", id="7", retry=3000)
    assert got == b"event: token\nid: 7\nretry: 3000\ndata: line one\ndata: line two\n\n", got
    assert ssewire.comment() == b": ping\n\n"
    for bad in (dict(event="a\nb"), dict(id="1\r"), dict(id="a\0b")):
        try:
            ssewire.encode("x", **bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted {bad}")
    return "multi-line data, fields, comment; bad event and id refused"


@check
def c02_sse_spec_examples():
    ev = ssewire.parse_all(b"data: YHOO\ndata: +2\ndata: 10\n\n")
    assert [(e.type, e.data) for e in ev] == [("message", "YHOO\n+2\n10")], ev
    ev = ssewire.parse_all(b": test stream\n\ndata: first event\nid: 1\n\n"
                           b"data:second event\nid\n\ndata:  third event\n\n")
    assert [(e.data, e.last_event_id) for e in ev] == \
        [("first event", "1"), ("second event", ""), (" third event", "")], ev
    ev = ssewire.parse_all(b"data\n\ndata\ndata\n\ndata:")
    assert [e.data for e in ev] == ["", "\n"], ev
    ev = ssewire.parse_all(b"data:test\n\ndata: test\n\n")
    assert [e.data for e in ev] == ["test", "test"], ev
    return "the four examples in the WHATWG spec give the spec's results"


@check
def c03_sse_any_chunking():
    stream = ("\ufeffevent: token\r\nid: 1\r\ndata: café → ok\r\n\r\n"
              ": ping\r\n\r\ndata: two\rdata: lines\r\r").encode("utf-8")
    whole = [(e.type, e.data, e.last_event_id) for e in ssewire.parse_all(stream)]
    assert whole == [("token", "café → ok", "1"), ("message", "two\nlines", "1")], whole
    for size in (1, 2, 3, 5, 7):
        part = [(e.type, e.data, e.last_event_id) for e in ssewire.parse_all(stream, size)]
        assert part == whole, (size, part)
    return "byte-by-byte feeding (split CRLF, split UTF-8) gives the same events"


@check
def c04_sse_field_rules():
    p = ssewire.Parser()
    ev = p.feed(b"retry: 3x\nretry: 2500\nid: a\0b\ndata: x\nunknown: y\n\n")
    assert p.retry == 2500 and ev[0].last_event_id == "" and ev[0].type == "message", (p.retry, ev)
    assert ssewire.parse_all(b"event: usage\n\n") == []          # no data: nothing dispatched
    ev = ssewire.parse_all(b"event: usage\ndata: a\n\ndata: b\n\n")
    assert [e.type for e in ev] == ["usage", "message"], ev       # event type resets
    assert ssewire.parse_all(b"data: no blank line at the end") == []
    return "retry digits only, NUL ids ignored, no data no event, unfinished event dropped"


# -------------------------------------------------------------- streaming
@check
def c05_stream_end_to_end():
    r = sse_client.stream("Tell me about streaming", server_port())
    assert r["status"] == 200, r
    h = {k.lower(): v for k, v in r["headers"].items()}
    assert h["content-type"].startswith("text/event-stream"), h
    assert h.get("x-accel-buffering") == "no" and h.get("cache-control") == "no-cache", h
    assert r["done"] and r["usage"]["output_tokens"] == len(r["token_times"]) > 10, r
    assert r["text"] == stream_server.ANSWER, r["text"]
    return f"{len(r['token_times'])} tokens, first at {r['ttft']:.2f} s, usage event at the end"


@check
def c06_proxy_buffering():
    port = server_port()
    honour = buffer_proxy.serve(port, honour_header=True)
    ignore = buffer_proxy.serve(port, honour_header=False)
    try:
        a = sse_client.stream("hello", honour.server_address[1])
        b = sse_client.stream("hello", ignore.server_address[1])
    finally:
        honour.shutdown(); ignore.shutdown()
        honour.server_close(); ignore.server_close()
    assert a["ttft"] < 0.5 * a["total"], (a["ttft"], a["total"])
    assert b["ttft"] > 0.9 * b["total"], (b["ttft"], b["total"])
    assert a["text"] == b["text"] == stream_server.ANSWER
    return (f"header honoured: first token {a['ttft']:.2f} of {a['total']:.2f} s; "
            f"ignored: {b['ttft']:.2f} of {b['total']:.2f} s, all at once")


@check
def c07_error_after_200():
    r = sse_client.stream("x", server_port(), fail_after=3)
    assert r["status"] == 200 and r["error"]["type"] == "overloaded_error", r
    assert len(r["token_times"]) == 3 and r["usage"] is None and not r["done"], r
    return "status 200, three tokens, then an error event and no usage"


@check
def c08_client_disconnect_stops_work():
    before = dict(stream_server.Handler.stats)
    r = sse_client.stream("x", server_port(), stop_after=2)
    time.sleep(0.6)
    after = stream_server.Handler.stats
    words = len(stream_server.ANSWER.split(" "))
    assert after["stopped_early"] == before["stopped_early"] + 1, (before, after)
    sent = after["tokens_sent"] - before["tokens_sent"]
    assert len(r["token_times"]) == 2 and sent < words, (sent, words)
    return f"the client left after 2 tokens; the server stopped at {sent} of {words}"


@check
def c09_limits_key_and_logs():
    import http.client
    port = server_port()

    def post(body: bytes, headers=None):
        c = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        c.request("POST", "/v1/stream", body=body,
                  headers={"Content-Type": "application/json", **(headers or {})})
        s = c.getresponse().status
        c.close()
        return s
    assert post(b"x" * (stream_server.MAX_BODY + 1)) == 413
    assert post(b"{not json") == 400
    stream_server.Handler.api_key = "lab-key"
    try:
        assert post(json.dumps({"prompt": "hi"}).encode()) == 401
        assert post(json.dumps({"prompt": "hi"}).encode(), {"Authorization": "Bearer nope"}) == 401
        r = sse_client.stream("secret prompt words", port, api_key="lab-key")
        assert r["status"] == 200, r
    finally:
        stream_server.Handler.api_key = None
    try:
        stream_server.serve(0, host="0.0.0.0")
        raise AssertionError("the lab server agreed to listen on every address")
    except ValueError:
        pass
    dumped = json.dumps(list(stream_server.Handler.tracer.spans))
    assert "secret prompt words" not in dumped
    return "413 too big, 400 bad JSON, 401 wrong key, 200 right key; local only; no prompt in traces"


# ------------------------------------------------------------ cost
@check
def c10_request_cost():
    u = {"input": 2_000, "output": 500}
    assert sm.request_cost("claude-sonnet-5-5", u) == F(9, 1000)            # $0.009
    assert sm.request_cost("claude-sonnet-5-5", u, batch=True) == F(9, 2000)
    assert sm.request_cost("claude-sonnet-5-5", u, residency="anthropic-us") == F(99, 10000)
    cached = {"input": 200, "cache_read": 1_800, "output": 500}
    assert sm.request_cost("claude-sonnet-5-5", cached) == F(5580, 10**6)   # $0.00558
    assert sm.request_cost("gpt-6-astra", {"input": 1_000, "output": 1_000}) == F(6, 100)
    assert sm.monthly(F(9, 1000), 10_000) == F(2700)
    return "Sonnet 5.5: $0.009 a request, $0.0045 batched, $0.0099 US-only, $0.00558 cached"


@check
def c11_long_context_whole_request():
    at = sm.request_cost("gpt-6-astra", {"input": 272_000, "output": 1_000})
    over = sm.request_cost("gpt-6-astra", {"input": 272_001, "output": 1_000})
    assert at == F(272_000 * 10 + 1_000 * 50, 10**6), at
    assert over == F(272_001 * 20 + 1_000 * 75, 10**6), over
    h = sm.request_cost("claude-haiku-5-5", {"input": 100_001, "output": 1_000})
    assert h == F(100_001 * 50 + 1_000 * 250, 10**8), h
    g = sm.request_cost("gemini-3.1-pro-preview", {"input": 200_001, "output": 1_000})
    assert g == F(200_001 * 4 + 1_000 * 18, 10**6), g
    assert sm.prompt_tokens({"input": 10, "cache_read": 20, "cache_write": 30}) == 60
    return (f"one token over 272,000 takes gpt-6-astra from ${float(at):.2f} "
            f"to ${float(over):.2f}; Haiku 5.5 and Gemini 3.1 Pro switch the same way")


# ------------------------------------------------- load, latency, retries
@check
def c12_littles_law_and_tails():
    assert sm.concurrent(5, 8) == 40
    times = [1.0] * 94 + [9.0] * 6
    assert sm.percentile(times, 50) == 1.0 and sm.percentile(times, 95) == 9.0
    assert abs(sm.mean(times) - 1.48) < 1e-9
    assert sm.percentile(list(range(1, 11)), 95) == 10 and sm.percentile(list(range(1, 11)), 10) == 1
    st = sm.stream_timing(0.0, [0.4, 0.5, 0.6])
    assert abs(st["time_to_first_chunk"] - 0.4) < 1e-9 and abs(st["mean_gap"] - 0.1) < 1e-9
    return "5 requests/s x 8 s = 40 open streams; mean 1.48 s hides a p95 of 9 s"


@check
def c13_retry_rules():
    assert sm.retry_plan("openai", 429, {"Retry-After": "3"}, 0) == 3.0
    assert sm.retry_plan("anthropic", 429, {"retry-after-ms": "1500", "retry-after": "9"}, 0) == 1.5
    assert sm.retry_plan("anthropic", 429, {}, 0) is None          # spend cap: retrying won't help
    assert sm.retry_plan("anthropic", 529, {}, 0) == 0.5
    assert sm.retry_plan("anthropic", 529, {}, 1) == 1.0
    assert sm.retry_plan("openai", 500, {}, 2) is None             # out of retries
    assert sm.retry_plan("openai", 400, {}, 0) is None
    assert sm.retry_plan("openai", 503, {"retry-after": "Wed, 21 Oct 2026 07:28:00 GMT"}, 0) == 0.5
    assert sm.retry_plan("openai", 429, {"retry-after": "86400"}, 0) is None   # a day: give up
    assert sm.retry_plan("openai", 429, {"retry-after": "-5"}, 0) == 0.5       # not a plain number
    assert sm.retry_plan("openai", 429, {"retry-after": "60"}, 0) == 60.0
    assert sm.retry_plan("anthropic", 529, {"retry-after-ms": "nan"}, 0) == 0.5
    return ("retry-after obeyed up to 60 s, Anthropic spend-cap 429 not retried, 400 never, "
            "2 retries")


# ------------------------------------------------------------ tracing
@check
def c14_traceparent():
    ok = sm.parse_traceparent("00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01")
    assert ok == {"trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
                  "parent_id": "00f067aa0ba902b7", "sampled": True}, ok
    for bad in ("00-" + "0" * 32 + "-00f067aa0ba902b7-01",
                "00-4bf92f3577b34da6a3ce929d0e0e4736-" + "0" * 16 + "-01",
                "ff-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
                "00-4BF92F3577B34DA6A3CE929D0E0E4736-00f067aa0ba902b7-01",
                "00-4bf92f3577b34da6a3ce929d0e0e47-00f067aa0ba902b7-01"):
        assert sm.parse_traceparent(bad) is None, bad
    return "the W3C example parses; zero IDs, version ff, capitals and short IDs refused"


@check
def c15_genai_span_rules():
    u = {"input": 200, "cache_read": 1_800, "output": 50}
    name, attrs = sm.chat_span("anthropic", "claude-sonnet-5-5", u, ["end_turn"],
                               messages=[{"role": "user", "content": "hi"}])
    assert name == "chat claude-sonnet-5-5", name
    assert attrs["gen_ai.operation.name"] == "chat" and attrs["gen_ai.provider.name"] == "anthropic"
    assert attrs["gen_ai.usage.input_tokens"] == 2_000, attrs          # cached tokens included
    assert attrs["gen_ai.usage.cache_read.input_tokens"] == 1_800
    assert not any(k in attrs for k in sm.CONTENT_ATTRIBUTES), attrs   # off by default
    _, on = sm.chat_span("anthropic", "m", u, ["end_turn"],
                         messages=[{"role": "user", "content": "hi"}], capture_content=True)
    assert json.loads(on["gen_ai.input.messages"]) == [{"role": "user", "content": "hi"}]
    assert "gen_ai.input.messages" not in sm.drop_content(on)
    return "span 'chat {model}', input tokens include cached, content only when opted in"


@check
def c16_trace_joins_across_services():
    tracer = stream_server.Handler.tracer
    incoming = "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"
    n = len(tracer.spans)
    sse_client.stream("hi", server_port(), traceparent=incoming)
    new = list(tracer.spans)[n:]
    server = [s for s in new if s["kind"] == "SERVER"][0]
    chat = [s for s in new if s["name"].startswith("chat ")][0]
    assert server["trace_id"] == chat["trace_id"] == "4bf92f3577b34da6a3ce929d0e0e4736", new
    assert server["parent_id"] == "00f067aa0ba902b7" and chat["parent_id"] == server["span_id"]
    assert chat["attributes"]["gen_ai.usage.output_tokens"] > 0
    return "the server's spans join the caller's trace; the chat span is the server span's child"


@check
def c17_standard_library_only():
    allowed = set(sys.stdlib_module_names) | {"shipmath", "ssewire", "tinytrace", "stream_server",
                                              "buffer_proxy", "sse_client", "run_lab"}
    for name in ("shipmath.py", "ssewire.py", "tinytrace.py", "stream_server.py",
                 "buffer_proxy.py", "sse_client.py", "demo.py", "run_lab.py", "mutation_check.py"):
        tree = ast.parse(open(os.path.join(HERE, name), encoding="utf-8").read())
        for node in ast.walk(tree):
            mods = [a.name for a in node.names] if isinstance(node, ast.Import) else \
                   [node.module] if isinstance(node, ast.ImportFrom) and node.module else []
            for m in mods:
                assert m.split(".")[0] in allowed, f"{name} imports {m}"
    return "the core lab imports only Python's standard library"


# ------------------------------------------------------------ hardening
def _raw(port: int, data: bytes, wait: float = 5.0) -> bytes:
    """Send raw bytes and return what comes back (status line first)."""
    import socket
    with socket.create_connection(("127.0.0.1", port), timeout=wait) as s:
        if data:
            s.sendall(data)
        out = b""
        try:
            while chunk := s.recv(4096):
                out += chunk
        except (TimeoutError, ConnectionError):   # Windows can also say ConnectionAbortedError
            pass
        return out


def _post_status(port: int, body: dict | bytes, headers=None) -> int:
    import http.client
    c = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    data = body if isinstance(body, bytes) else json.dumps(body).encode()
    c.request("POST", "/v1/stream", body=data,
              headers={"Content-Type": "application/json", **(headers or {})})
    status = c.getresponse().status
    c.close()
    return status


@check
def c18_bad_fields_get_400():
    port = server_port()
    for body in ({"prompt": "hi", "max_tokens": "lots"}, {"prompt": "hi", "max_tokens": 1e400},
                 {"prompt": "hi", "max_tokens": True}, {"prompt": "hi", "max_tokens": 0},
                 {"prompt": "hi", "max_tokens": 10_000}, {"prompt": "hi", "fail_after": "x"},
                 {"prompt": 42}, {"no_prompt": "hi"}, [1, 2]):
        status = _post_status(port, body)
        assert status == 400, (body, status)
    assert _post_status(port, b'{"prompt": "hi", "max_tokens": 1e400}') == 400
    return "wrong types, out-of-range numbers and missing fields get a 400 before any stream starts"


@check
def c19_parser_robustness():
    assert [e.data for e in ssewire.parse_all(b"data: a\xffb\n\n")] == ["a\ufffdb"]
    p = ssewire.Parser()
    got = p.feed(b"data: a\r") + p.feed(b"") + p.feed(b"\ndata: b\n\n")
    assert [e.data for e in got] == ["a\nb"], got
    t0 = time.perf_counter()
    try:
        ssewire.Parser().feed(b"data: " + b"x" * (ssewire.MAX_LINE + 10))
        raise AssertionError("a line over MAX_LINE was accepted")
    except ValueError:
        pass
    p, many = ssewire.Parser(), b"data: " + b"y" * 1000 + b"\n"
    for _ in range(500):          # 500 kB of one event, fed a line at a time
        p.feed(many)
    took = time.perf_counter() - t0
    assert took < 2.0, f"took {took:.2f} s"
    return f"bad UTF-8 becomes U+FFFD, CR then LF across feeds is one line end, long lines refused; {took:.2f} s"


@check
def c20_server_limits():
    srv, h = stream_server, stream_server.Handler
    h.api_key = "lab-key"
    try:
        port = server_port()
        assert _post_status(port, {"prompt": "hi", "max_tokens": 2},
                            {"Authorization": "bearer lab-key"}) == 200
        assert _post_status(port, {"prompt": "hi"}, {"Authorization": "Bearer "}) == 401
        h.api_key = ""
        try:
            srv.serve(0)
            raise AssertionError("served with an empty key")
        except ValueError:
            pass
    finally:
        h.api_key = None
    assert h.timeout == srv.SOCKET_TIMEOUT and 0 < srv.SOCKET_TIMEOUT <= 60
    import tinytrace
    small_tracer = tinytrace.Tracer("t", keep=3)
    for _ in range(5):
        with small_tracer.span("s"):
            pass
    assert len(small_tracer.spans) == 3, "the tracer keeps every span forever"

    class Broken(stream_server.StandInModel):
        def tokens(self, max_tokens):
            yield "one"
            raise RuntimeError("internal detail /etc/secret")
    old_model, h.model = h.model, Broken(base=0.0, prefill_per_char=0.0)
    try:
        r = sse_client.stream("hi", server_port())
    finally:
        h.model = old_model
    assert r["error"] == {"type": "server_error", "message": "the stream failed"}, r["error"]
    assert not r["done"]
    r = sse_client.stream("hi", server_port(), deadline=0.1)
    assert r["error"]["type"] == "client_deadline" and not r["done"], r["error"]
    old_timeout, old_cap = h.timeout, srv.MAX_CLIENTS
    h.timeout, srv.MAX_CLIENTS = 0.5, 2
    small = srv.serve(0)
    try:
        sport = small.server_address[1]
        t0 = time.perf_counter()
        assert _raw(sport, b"", wait=5) == b""               # a silent client is dropped
        dropped = time.perf_counter() - t0
        assert dropped < 3, dropped
        import socket
        idle = [socket.create_connection(("127.0.0.1", sport)) for _ in range(2)]
        time.sleep(0.1)
        reply = _raw(sport, b"POST /v1/stream HTTP/1.1\r\nHost: x\r\n\r\n", wait=3)
        for s in idle:
            s.close()
        assert reply.startswith(b"HTTP/1.0 503"), reply[:40]
    finally:
        small.shutdown()
        small.server_close()
        h.timeout, srv.MAX_CLIENTS = old_timeout, old_cap
    return (f"'bearer' in any case, empty key refused, a silent client dropped in {dropped:.1f} s, "
            "a client over the cap gets 503, spans capped, a crash sends a plain error, client deadline")


@check
def c21_proxy_refuses_bad_requests():
    proxy = buffer_proxy.serve(server_port())
    import socket
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    dead_port = s.getsockname()[1]
    s.close()                                                 # nothing listens here now
    dead = buffer_proxy.serve(dead_port)
    try:
        p = proxy.server_address[1]
        def status(raw: bytes, port: int = p) -> bytes:
            return _raw(port, raw)[:12]
        assert status(b"POST /v1/stream HTTP/1.1\r\nHost: x\r\nContent-Length: abc\r\n\r\n") \
            == b"HTTP/1.0 400", "bad length"
        assert status(b"POST /v1/stream HTTP/1.1\r\nHost: x\r\nContent-Length: 99999999\r\n\r\n") \
            == b"HTTP/1.0 413", "too big"
        assert status(b"POST /v1/stream HTTP/1.1\r\nHost: x\r\n\r\n") == b"HTTP/1.0 411", "no length"
        assert status(b"POST /v1/stream HTTP/1.1\r\nHost: x\r\nContent-Length: 2\r\n\r\n{}",
                      dead.server_address[1]) == b"HTTP/1.0 502", "dead upstream"
    finally:
        for x in (proxy, dead):
            x.shutdown()
            x.server_close()
    return "bad Content-Length 400, too big 413, none 411, upstream down 502"


def main() -> int:
    if sys.version_info < (3, 11) or sys.version_info >= (3, 14):
        print(f"Note: tested on Python 3.11 to 3.13; this is {sys.version.split()[0]}")
    passed = 0
    for fn in CHECKS:
        try:
            detail = fn()
            print(f"PASS {fn.__name__}: {detail}")
            passed += 1
        except Exception as error:  # report every check, then fail at the end
            msg = str(error).splitlines()[0][:150] if str(error) else ""
            print(f"FAIL {fn.__name__}: {type(error).__name__} {msg}")
            if "-v" in sys.argv:
                traceback.print_exc()
    if "httpd" in _SERVER:
        _SERVER["httpd"].shutdown()
        _SERVER["httpd"].server_close()
    print(f"{passed} of {len(CHECKS)} checks passed")
    return 0 if passed == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())
