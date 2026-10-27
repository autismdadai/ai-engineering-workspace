"""sse_client: read a model's stream and time it (Engineering Stack, Part 13).

Standard library only. Posts a prompt, parses the Server-Sent Events with
ssewire, and reports time to first token, total time, the text and the usage
event. Usage: python sse_client.py "your prompt" [port]
"""
from __future__ import annotations

import http.client
import json
import sys
import time

import ssewire


def stream(prompt: str, port: int = 8013, max_tokens: int = 64, fail_after=None,
           stop_after: int | None = None, api_key: str | None = None,
           traceparent: str | None = None, read_size: int = 256,
           deadline: float = 120.0) -> dict:
    """Read one stream. Gives up after `deadline` seconds in all; success is the `done` event."""
    body = {"prompt": prompt, "max_tokens": max_tokens}
    if fail_after is not None:
        body["fail_after"] = fail_after
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    if traceparent:
        headers["traceparent"] = traceparent
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=60)
    t0 = time.perf_counter()
    conn.request("POST", "/v1/stream", body=json.dumps(body), headers=headers)
    resp = conn.getresponse()
    out = {"status": resp.status, "headers": dict(resp.getheaders()), "text": "",
           "token_times": [], "usage": None, "error": None, "events": 0, "done": False}
    if resp.status != 200:
        out["body"] = resp.read().decode("utf-8", "replace")
        conn.close()
        return out
    parser = ssewire.Parser()
    try:
        while True:
            if time.perf_counter() - t0 > deadline:
                out["error"] = {"type": "client_deadline", "message": f"no end after {deadline} s"}
                break
            chunk = resp.read1(read_size)
            if not chunk:
                break
            for ev in parser.feed(chunk):
                out["events"] += 1
                if ev.type == "token":
                    out["token_times"].append(time.perf_counter() - t0)
                    out["text"] += json.loads(ev.data)["text"]
                    if stop_after is not None and len(out["token_times"]) >= stop_after:
                        raise StopIteration
                elif ev.type == "usage":
                    out["usage"] = json.loads(ev.data)
                elif ev.type == "error":
                    out["error"] = json.loads(ev.data)
                elif ev.type == "done":
                    out["done"] = True
    except StopIteration:
        pass                       # the reader leaves early, e.g. the user closed the tab
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        out["error"] = {"type": "bad_stream", "message": type(error).__name__}
    except (TimeoutError, ConnectionError) as error:
        out["error"] = {"type": "connection", "message": type(error).__name__}
    finally:
        conn.close()
    out["total"] = time.perf_counter() - t0
    out["ttft"] = out["token_times"][0] if out["token_times"] else None
    return out


if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Tell me about streaming"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8013
    r = stream(prompt, port)
    if r["status"] != 200:
        print(f"HTTP {r['status']}: {r.get('body')}")
        sys.exit(1)
    print(r["text"])
    first = "none" if r["ttft"] is None else f"{r['ttft']:.3f} s"
    print(f"time to first token {first}, total {r['total']:.3f} s, "
          f"{len(r['token_times'])} tokens, usage {r['usage']}")
    if not r["done"]:
        print(f"The stream did not finish (no done event): {r['error']}")
        sys.exit(1)
