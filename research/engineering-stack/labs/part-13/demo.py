"""demo: the worked tables behind Part 13 (Engineering Stack).

Standard library only. Prints a cost table, the long-context jump, a load
estimate, the tail-latency example, and the buffering demonstration.
"""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import buffer_proxy  # noqa: E402
import shipmath as sm  # noqa: E402
import sse_client  # noqa: E402
import stream_server  # noqa: E402


def money(x) -> str:
    if x < F(1, 1000):
        return f"${float(x):.6f}"     # small enough that 5 places would round
    if x < F(1, 100):
        return f"${float(x):.5f}"
    return f"${float(x):,.4f}" if x < 1 else f"${float(x):,.2f}"


def main() -> None:
    print("1. One request: 2,000 tokens in, 500 out (October 20, 2026 prices)")
    u = {"input": 2_000, "output": 500}
    for model in ("claude-haiku-5-5", "claude-sonnet-5-5", "gemini-3.1-pro-preview", "gpt-6-astra"):
        c = sm.request_cost(model, u)
        print(f"   {model:24s} {money(c):>9}  batch {money(sm.request_cost(model, u, batch=True)):>9}"
              f"  x 10,000 a day for 30 days {money(sm.monthly(c, 10_000)):>10}")

    print("\n2. The same 2,000 tokens with 1,800 read from a prompt cache (Sonnet 5.5)")
    cached = {"input": 200, "cache_read": 1_800, "output": 500}
    print(f"   {money(sm.request_cost('claude-sonnet-5-5', cached))} instead of "
          f"{money(sm.request_cost('claude-sonnet-5-5', u))}; batched as well: "
          f"{money(sm.request_cost('claude-sonnet-5-5', cached, batch=True))}")

    print("\n3. Long-context pricing applies to the whole request")
    for model, edge in (("gpt-6-astra", 272_000), ("gemini-3.1-pro-preview", 200_000),
                        ("claude-haiku-5-5", 100_000)):
        a = sm.request_cost(model, {"input": edge, "output": 1_000})
        b = sm.request_cost(model, {"input": edge + 1, "output": 1_000})
        print(f"   {model:24s} {edge:>7,} in: {money(a):>8}   {edge + 1:>7,} in: {money(b):>8}"
              f"  ({float(b / a):.2f}x)")

    print("\n4. How many streams are open at once (Little's law)")
    for rate, secs in ((1, 8), (5, 8), (20, 8), (20, 30)):
        print(f"   {rate:>3} requests/s x {secs:>2} s per answer = {sm.concurrent(rate, secs):>4.0f} open")

    print("\n5. Why a mean hides the slow requests")
    times = [1.0] * 94 + [9.0] * 6
    print(f"   94 answers in 1 s, 6 in 9 s: mean {sm.mean(times):.2f} s, "
          f"p50 {sm.percentile(times, 50):.0f} s, p95 {sm.percentile(times, 95):.0f} s")

    print("\n6. The same stream, direct and through a buffering proxy (stand-in model [I])")
    httpd = stream_server.serve(0)
    port = httpd.server_address[1]
    honour = buffer_proxy.serve(port, honour_header=True)
    ignore = buffer_proxy.serve(port, honour_header=False)
    for label, p in (("direct", port), ("proxy, header honoured", honour.server_address[1]),
                     ("proxy, header ignored", ignore.server_address[1])):
        r = sse_client.stream("Tell me about streaming", p)
        print(f"   {label:24s} first token {r['ttft']:.2f} s, last {r['total']:.2f} s, "
              f"{len(r['token_times'])} tokens")

    print("\n7. The trace of one request (no prompt text recorded)")
    n = len(stream_server.Handler.tracer.spans)
    sse_client.stream("Tell me about streaming", port)
    for s in list(stream_server.Handler.tracer.spans)[n:]:
        ms = (s["end"] - s["start"]) / 1e6
        attrs = {k: v for k, v in s["attributes"].items() if k.startswith("gen_ai.")}
        print(f"   {s['kind']:6s} {s['name']:20s} {ms:7.1f} ms  {json.dumps(attrs)}")
    for h in (honour, ignore, httpd):
        h.shutdown()
        h.server_close()


if __name__ == "__main__":
    main()
