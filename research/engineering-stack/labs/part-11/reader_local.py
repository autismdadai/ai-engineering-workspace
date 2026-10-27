"""Reader test R3 (Engineering Stack, Part 11): time a small local model in
Ollama and compare its speed with the memory-bandwidth ceiling.

Needs Ollama running on this computer with the model already pulled (the
part's Section 7.5). Standard library only. It talks only to Ollama on this
computer (127.0.0.1) and ignores any proxy settings.

    python reader_local.py --model qwen3:1.7b --bandwidth 41.6
    python reader_local.py --self-test      # no Ollama needed
"""
import argparse
import json
import statistics
import sys
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

import runmath as rm

PROMPT = "In three sentences, explain why the sky is blue."
LOCAL = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def call(base, path, body=None):
    data = None if body is None else json.dumps(body).encode()
    request = urllib.request.Request(base + path, data=data,
                                     headers={"Content-Type": "application/json"})
    with LOCAL.open(request, timeout=900) as response:
        return json.load(response)


def model_size(base, model):
    """Bytes on disk, from Ollama's /api/tags list."""
    for entry in call(base, "/api/tags").get("models", []):
        if model in (entry.get("name"), entry.get("model")):
            return entry["size"]
    raise SystemExit(f"{model} isn't pulled yet. Run: ollama pull {model}")


def tokens_per_second(base, model, tokens=64):
    """Generation speed of one reply. Ollama reports eval_duration in
    nanoseconds (docs/api.md)."""
    r = call(base, "/api/generate", {"model": model, "prompt": PROMPT, "stream": False,
                                     "options": {"num_predict": tokens}})
    return r["eval_count"] / r["eval_duration"] * 1e9


def measure(base, model, bandwidth_gbs, runs=3):
    size = model_size(base, model)
    tokens_per_second(base, model, 8)            # warm-up: loads the model
    measured = statistics.median(tokens_per_second(base, model) for _ in range(runs))
    ceiling = rm.decode_ceiling(bandwidth_gbs * 1e9, size)
    return {"model": model, "size": size, "measured": round(measured, 2),
            "ceiling": ceiling, "share": measured / ceiling}


class StandIn(BaseHTTPRequestHandler):
    """A fake Ollama with fixed answers, for the self-test."""

    def do_GET(self):
        self._send({"models": [{"name": "stand-in:1.7b", "size": 1_400_000_000}]})

    def do_POST(self):
        self.rfile.read(int(self.headers["Content-Length"]))
        self._send({"response": "...", "eval_count": 64, "eval_duration": 5_120_000_000})

    def _send(self, body):
        data = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


def self_test():
    server = HTTPServer(("127.0.0.1", 0), StandIn)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        return measure(f"http://127.0.0.1:{server.server_port}", "stand-in:1.7b", 41.6)
    finally:
        server.shutdown()
        server.server_close()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--model", default="qwen3:1.7b")
    parser.add_argument("--bandwidth", type=float, default=41.6,
                        help="memory bandwidth in GB/s (41.6 is Intel's figure "
                             "for the Core i5-9500T; look up your own)")
    parser.add_argument("--host", default="http://127.0.0.1:11434")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        r = self_test() if args.self_test else measure(args.host, args.model,
                                                       args.bandwidth, args.runs)
    except urllib.error.URLError as error:
        print(f"Can't reach Ollama at {args.host}: is it running? ({error.reason})")
        return 2
    print(f"Model {r['model']}, file {r['size'] / 1e9:.2f} GB")
    print(f"Measured: {r['measured']:.1f} tokens/s (median of the timed runs)")
    print(f"Ceiling:  {r['ceiling']:.1f} tokens/s (bandwidth / file size)")
    print(f"Measured is {r['share']:.0%} of the ceiling.")
    if r["share"] >= 1:
        print("Above the ceiling: check --bandwidth (on a GPU or a Mac, use that memory's figure) and the model name.")
        return 1
    if args.self_test:
        print("Self-test passed: these numbers come from the stand-in, not a model.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
