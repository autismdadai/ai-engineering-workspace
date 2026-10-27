"""Mutation check (Engineering Stack, Part 11): break the lab on purpose and
make sure run_lab.py notices every break.

Each mutation edits one line of a fresh copy of the lab in a temporary
folder, then runs run_lab.py there. A mutation is caught when run_lab.py
exits with a failure. An unbroken copy must pass first. Runs with -B and
PYTHONDONTWRITEBYTECODE=1 so Python never reuses a stale compiled file, and
deletes every temporary folder it makes.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ["runmath.py", "run_lab.py", "reader_local.py"]

MUTATIONS = [  # (file, old text, new text, what the break means)
    ("runmath.py", "hidden = int(multiplier * hidden)", "hidden = int(hidden)",
     "feed-forward multiplier ignored"),
    ("runmath.py", 'kv = cfg["n_kv_heads"] * (d // cfg["n_heads"])',
     'kv = cfg["n_heads"] * (d // cfg["n_heads"])', "grouped-query attention ignored"),
    ("runmath.py", '"Q4_K": (256, 144)', '"Q4_K": (256, 128)', "Q4_K block without its scales"),
    ("runmath.py", '"Q6_K": (256, 210)', '"Q6_K": (256, 208)', "Q6_K block two bytes short"),
    ("runmath.py", '"MXFP4": (32, 17)', '"MXFP4": (32, 16)', "MXFP4 without its shared scale"),
    ("runmath.py", "(i - n // 8) % 3 == 2", "(i - n // 8) % 3 == 1", "wrong every-third-layer rule"),
    ("runmath.py", "return i < n // 8 or i >= 7 * n // 8 or", "return i >= 7 * n // 8 or",
     "first eighth of layers not upgraded"),
    ("runmath.py", 'if name == "output":\n            return "Q6_K"',
     'if name == "output":\n            return base', "output matrix not upgraded"),
    ("runmath.py", 'if name in ("attn_v", "ffn_down")', 'if name in ("attn_v",)',
     "ffn_down not upgraded"),
    ("runmath.py", 'if name.endswith("norm"):\n            return "F32"',
     'if name.endswith("norm"):\n            return base', "norms quantized"),
    ("runmath.py", "if n % weights:", "if False:", "partial blocks accepted"),
    ("runmath.py", 'expert + 2 * embed + h', 'expert + embed + h', "unembedding left out of the total"),
    ("runmath.py", 'n * c["per_token"] * expert + embed + h', 'n * c["n_experts"] * expert + embed + h',
     "every expert counted as active"),
    ("runmath.py", 'mx_one = c["n_layers"] * c["per_token"] * per_expert', "mx_one = 0",
     "active experts read at 16 bits"),
    ("runmath.py", "per_layer_token = 2 * n_kv_heads * head_dim * value_bytes",
     "per_layer_token = n_kv_heads * head_dim * value_bytes", "keys stored without values"),
    ("runmath.py", "(min(tokens, window) if window else tokens)", "tokens", "sliding window ignored"),
    ("runmath.py", "return per_layer_token * kept * batch", "return per_layer_token * kept",
     "batch ignored"),
    ("runmath.py", "return weights + kv <= memory * (1 - overhead)", "return weights + kv <= memory",
     "no spare memory kept"),
    ("runmath.py", "return max(0, int(room // (kv_per_token * batch)))",
     "return int(room // (kv_per_token * batch))", "negative room allowed"),
    ("runmath.py", "return bandwidth / bytes_per_token", "return bytes_per_token / bandwidth",
     "ceiling upside down"),
    ("runmath.py", "return flops / bandwidth", "return bandwidth / flops", "ridge point upside down"),
    ("runmath.py", "return 2 * n_weights * tokens / flops", "return n_weights * tokens / flops",
     "one operation per weight"),
    ("runmath.py", "return (1 - alpha ** (gamma + 1)) / (1 - alpha)",
     "return (1 - alpha ** gamma) / (1 - alpha)", "gamma instead of gamma + 1"),
    ("runmath.py", "return expected_tokens(alpha, gamma) / (gamma * c + 1)",
     "return expected_tokens(alpha, gamma) / (gamma * c)", "target pass left out of the cost"),
    ("runmath.py", "if not 0 <= alpha <= 1 or gamma < 0 or c < 0:", "if False:", "no input checks"),
    ("runmath.py", "range(1, largest + 1)", "range(0, largest + 1)", "gamma 0 allowed"),
    ("runmath.py", "allocated = sum(-(-n // block) * block for n in lengths)",
     "allocated = sum(lengths)", "partly filled blocks not counted"),
    ("runmath.py", "return 1 - sum(lengths) / (reserve * len(lengths))",
     "return 1 - sum(lengths) / (max(lengths) * len(lengths))", "reservation sized to the longest request"),
    ("runmath.py", '"tpot": (e2e - ttft) / (n - 1) if n > 1 else 0.0',
     '"tpot": (e2e - ttft) / n if n > 1 else 0.0', "TPOT divided by every token"),
    ("runmath.py", "gaps = [b - a for a, b in zip(times, times[1:])]",
     "gaps = [b - a for a, b in zip([sent] + times, times)]", "first gap measured from the request"),
    ("reader_local.py", 'return r["eval_count"] / r["eval_duration"] * 1e9',
     'return r["eval_count"] / r["eval_duration"]', "nanoseconds read as seconds"),
]


def run(folder):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    shutil.rmtree(os.path.join(folder, "__pycache__"), ignore_errors=True)
    done = subprocess.run([sys.executable, "-B", "run_lab.py"], cwd=folder, env=env,
                          capture_output=True, text=True, timeout=120)
    return done.returncode


def fresh_copy(parent):
    folder = tempfile.mkdtemp(prefix="lab11-", dir=parent)
    for name in FILES:
        shutil.copy(os.path.join(HERE, name), folder)
    return folder


def main():
    parent = tempfile.mkdtemp(prefix="lab11-mutations-")
    try:
        if run(fresh_copy(parent)) != 0:
            print("FAIL the unbroken copy doesn't pass; fix the lab first")
            return 1
        caught = 0
        for name, old, new, label in MUTATIONS:
            folder = fresh_copy(parent)
            path = os.path.join(folder, name)
            text = open(path, encoding="utf-8").read()
            if text.count(old) != 1:
                print(f"ERROR {label}: the text to change was found {text.count(old)} times")
                continue
            with open(path, "w", encoding="utf-8") as f:
                f.write(text.replace(old, new))
            if run(folder) != 0:
                caught += 1
                print(f"caught  {label}")
            else:
                print(f"MISSED  {label}")
        print(f"{caught} of {len(MUTATIONS)} mutations caught")
        return 0 if caught == len(MUTATIONS) else 1
    finally:
        shutil.rmtree(parent, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
