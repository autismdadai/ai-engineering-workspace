"""Measure whether a model's accuracy depends on where a fact sits in its context.

Part 04 of The AI Engineering Stack. Standard library only.

The test hides one fact (a locker code) among filler documents, moves it
through every position, asks for it, and reports accuracy per position with
a 95% Wilson interval. Two stand-in models make the harness testable without
any AI model: one with a built-in U-shaped bias and one with none. Their
behaviour is invented [I]; only the harness is under test.

Reader test (needs Ollama running locally and a pulled model; nothing is
sent anywhere else):
    python placement_test.py --ollama MODEL_NAME --trials 10
On a slow computer, raise --timeout (seconds per call, default 300); for a
thinking model such as qwen3, --no-think asks Ollama to answer directly.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import urllib.request

FILLER = ("Locker {n} is on floor {f}. Cleaning staff check it on {d}. "
          "Its door was repainted last spring and the hinge was oiled.")
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def build_context(n_docs, gold_pos, code, rng):
    """n_docs short documents; the one at gold_pos holds the code."""
    docs = []
    for i in range(n_docs):
        n = 100 + i
        text = FILLER.format(n=n, f=rng.randint(1, 9), d=rng.choice(DAYS))
        if i == gold_pos:
            text += f" The access code for the blue locker is {code}."
        docs.append(f"Document {i + 1}: {text}")
    question = "What is the access code for the blue locker? Reply with the four digits only."
    return "\n".join(docs), question


def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, centre - half), min(1.0, centre + half))


class StandInU:
    """Invented stand-in: answers correctly with a probability that is high at
    the edges and low in the middle, shaped loosely like the U-curve Liu et al.
    reported for 2023 models. Illustrative only."""
    def __init__(self, edge=0.9, middle=0.55, seed=0):
        self.edge, self.middle = edge, middle
        self.rng = random.Random(seed)

    def answer(self, context, question, gold_pos, n_docs, code):
        x = gold_pos / max(1, n_docs - 1)          # 0 at the start, 1 at the end
        p = self.middle + (self.edge - self.middle) * (2 * x - 1) ** 2
        return code if self.rng.random() < p else "0000"


class StandInFlat(StandInU):
    """Invented stand-in with the same average accuracy at every position."""
    def answer(self, context, question, gold_pos, n_docs, code):
        return code if self.rng.random() < 0.75 else "0000"


class OllamaModel:
    """Calls a local Ollama server. Sets num_ctx explicitly, because Ollama
    otherwise uses a default context that may silently cut a long prompt."""
    def __init__(self, model, num_ctx=8192, host="http://127.0.0.1:11434",
                 timeout=300, think=None):
        self.model, self.num_ctx, self.host = model, num_ctx, host
        self.timeout, self.think = timeout, think

    def answer(self, context, question, gold_pos, n_docs, code):
        body = {"model": self.model, "stream": False,
                "prompt": f"{context}\n\n{question}",
                "options": {"num_ctx": self.num_ctx, "temperature": 0}}
        if self.think is not None:
            body["think"] = self.think   # Ollama's switch for thinking models
        req = urllib.request.Request(f"{self.host}/api/generate",
                                     data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            out = json.loads(r.read())
        if out.get("prompt_eval_count", 0) and out["prompt_eval_count"] >= self.num_ctx:
            raise RuntimeError("prompt filled the context; raise num_ctx")
        return out.get("response", "")


def run_test(model, n_docs=20, positions=None, trials=40, seed=1):
    rng = random.Random(seed)
    positions = positions or [0, n_docs // 4, n_docs // 2, 3 * n_docs // 4, n_docs - 1]
    results = {}
    for pos in positions:
        right = 0
        for _ in range(trials):
            code = f"{rng.randint(0, 9999):04d}"
            ctx, q = build_context(n_docs, pos, code, rng)
            if code in model.answer(ctx, q, pos, n_docs, code):
                right += 1
        results[pos] = (right, trials)
    return results


def verdict(results, gap_points=10.0):
    """'U-shaped' only if both ends beat the worst middle position by at least
    gap_points AND the intervals don't overlap; else 'no clear position effect'."""
    pos = sorted(results)
    first, last, middle = pos[0], pos[-1], pos[1:-1]
    acc = {p: results[p][0] / results[p][1] for p in pos}
    lo = {p: wilson(*results[p])[0] for p in pos}
    hi = {p: wilson(*results[p])[1] for p in pos}
    worst = min(middle, key=lambda p: acc[p])
    clear = all(100 * (acc[e] - acc[worst]) >= gap_points and lo[e] > hi[worst]
                for e in (first, last))
    return ("U-shaped" if clear else "no clear position effect"), worst


def report(results):
    for p in sorted(results):
        k, n = results[p]
        lo, hi = wilson(k, n)
        print(f"   position {p + 1:3d}: {k:3d}/{n} = {100 * k / n:5.1f}%"
              f"  (95% interval {100 * lo:5.1f} to {100 * hi:5.1f})")
    v, worst = verdict(results)
    print(f"   verdict: {v} (lowest middle position {worst + 1})")
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ollama", metavar="MODEL")
    ap.add_argument("--num-ctx", type=int, default=8192)
    ap.add_argument("--docs", type=int, default=20)
    ap.add_argument("--trials", type=int, default=None,
                    help="per position; default 200 for the stand-ins, 10 for --ollama")
    ap.add_argument("--timeout", type=float, default=300,
                    help="seconds to wait for each --ollama call (default 300)")
    ap.add_argument("--no-think", action="store_true",
                    help="ask Ollama to turn a thinking model's thinking off")
    a = ap.parse_args()
    if a.ollama:
        trials = a.trials or 10
        print(f"Local model {a.ollama}, {a.docs} documents, num_ctx {a.num_ctx},"
              f" {trials} trials per position ({5 * trials} model calls),"
              f" {a.timeout:g} seconds per call{', thinking off' if a.no_think else ''}")
        model = OllamaModel(a.ollama, a.num_ctx, timeout=a.timeout,
                            think=False if a.no_think else None)
        try:
            report(run_test(model, a.docs, trials=trials))
        except OSError as error:   # urllib's URLError and timeouts are OSErrors
            if isinstance(getattr(error, "reason", error), TimeoutError):
                print(f"Ollama didn't answer within {a.timeout:g} seconds: the model is slow on"
                      " this computer. Lower --docs and --num-ctx, raise --timeout, or for a"
                      " thinking model add --no-think.")
            else:
                print(f"Could not reach Ollama at http://127.0.0.1:11434 ({error}). Is it running?")
            raise SystemExit(1)
        return
    a.trials = a.trials or 200
    print(f"Stand-in with a built-in U-shaped bias [I], {a.trials} trials per position")
    report(run_test(StandInU(), a.docs, trials=a.trials))
    print(f"Stand-in with no position bias [I], {a.trials} trials per position")
    report(run_test(StandInFlat(), a.docs, trials=a.trials))


if __name__ == "__main__":
    main()
