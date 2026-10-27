"""Mutation check (Engineering Stack, Part 12): break the lab on purpose and
make sure run_lab.py notices every break.

Each mutation edits one spot in a fresh copy of the lab in a temporary folder,
then runs run_lab.py there. A mutation is caught when run_lab.py exits with a
failure. An unbroken copy must pass first. Runs with -B and
PYTHONDONTWRITEBYTECODE=1 so Python never reuses a stale compiled file, and
deletes every temporary folder it makes.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ["adaptmath.py", "datacheck.py", "run_lab.py", "reader_lora.py"]

MUTATIONS = [  # (file, old text, new text, what the break means)
    ("adaptmath.py", '"k_proj": (h, kv)', '"k_proj": (h, q)', "grouped-query attention ignored"),
    ("adaptmath.py", '"o_proj": (q, h)', '"o_proj": (h, h)', "o_proj sized from the hidden width"),
    ("adaptmath.py", "+ 2 * c[\"hidden\"]       # two RMSNorms", "+ c[\"hidden\"]       # two RMSNorms",
     "one norm per block"),
    ("adaptmath.py", 'if c["qkv_bias"]:', "if False:", "q, k and v biases left out"),
    ("adaptmath.py", 'if c["qk_norm"]:', "if False:", "Qwen3's q and k norms left out"),
    ("adaptmath.py", 'embed * (1 if c["tied"] else 2)', "embed * 2", "tied output layer counted twice"),
    ("adaptmath.py", '+ c["layers"] * block + c["hidden"]', '+ c["layers"] * block',
     "final norm left out"),
    ("adaptmath.py", "r * sum(shapes[t])", "r * shapes[t][0]", "only A counted, not B"),
    ("adaptmath.py", 'return c["layers"] * sum(', "return sum(", "one layer instead of all"),
    ("adaptmath.py", "alpha / math.sqrt(r) if rslora", "alpha / r if rslora", "rsLoRA ignored"),
    ("adaptmath.py", "ADAM_MIXED_BYTES = 2 + 2 + 12", "ADAM_MIXED_BYTES = 2 + 2 + 8",
     "optimizer state without the fp32 weight copy"),
    ("adaptmath.py", "NF4_BITS = 4 + 8 / 64 + 32 / (64 * 256)", "NF4_BITS = 4 + 32 / 64",
     "double quantization ignored"),
    ("adaptmath.py", "+ ADAM_MIXED_BYTES * n_adapter", "+ 2 * n_adapter",
     "adapter gradients and optimizer state left out"),
    ("adaptmath.py", "return need_bytes <= memory_gb * GB * (1 - overhead)",
     "return need_bytes <= memory_gb * GB", "no spare memory kept"),
    ("adaptmath.py", "if day >= OPENAI_CLOSED_TO_ALL:", "if day > OPENAI_CLOSED_TO_ALL:",
     "closing day off by one"),
    ("adaptmath.py", "return tuned_before and inference_last_60_days", "return tuned_before",
     "60-day rule ignored"),
    ("adaptmath.py", '("new_facts", True, "retrieve"', '("new_facts", None, "retrieve"',
     "new facts sent to fine-tuning"),
    ("adaptmath.py", '("prompt_meets_bar", True, "stop"', '("prompt_meets_bar", False, "stop"',
     "stop rule inverted"),
    ("adaptmath.py", "model_name.startswith(prefix)", "prefix in model_name",
     "name prefix accepted anywhere"),
    ("adaptmath.py", 'SHARING["llama4"] = SHARING["llama3.1"]', 'SHARING["llama4"] = SHARING["llama3"]',
     "Llama 4 given Llama 3's terms"),
    ("adaptmath.py", "if licence in licences and", "if True and", "licence filter ignored"),
    ("adaptmath.py", "Q4_K_M_BITS = 4.89", "Q4_K_M_BITS = 4.0", "a 4-bit file taken at 4 bits"),
    ("datacheck.py", 'if "messages" in keys:', 'if "message" in keys:', "chat format not recognized"),
    ("datacheck.py", 'm.get("role") not in ROLES', 'm.get("role") is None', "any role accepted"),
    ("datacheck.py", ' or not m["content"].strip()', "", "blank content accepted"),
    ("datacheck.py", 'msgs[-1].get("role") != "assistant"', 'msgs[-1].get("role") == "nobody"',
     "no answer to learn accepted"),
    ("datacheck.py", 'if k == "preference" and ex["chosen"] == ex["rejected"]:', "if False:",
     "identical chosen and rejected accepted"),
    ("datacheck.py", "N = 13", "N = 12", "12-word runs counted as leaks"),
    ("datacheck.py", 'if value.get("role") == "system":', "if False:", "shared system prompt counted"),
    ("datacheck.py", "pairs.append((seen[key], i))", "pass", "duplicates never reported"),
    ("datacheck.py", "if len(ws) >= n else any(contains(t, ws) for t in train_words)",
     "if len(ws) >= n else False", "short test examples never checked"),
    ("reader_lora.py", "return ids, [-100] * len(head) + ids[len(head):]", "return ids, ids",
     "prompt not masked: the model learns to write the question"),
    ("reader_lora.py", 'am.PEFT_DEFAULT_TARGETS["llama"], R)', "am.ALL_LINEAR, R)",
     "prediction for the wrong target layers"),
]


def run(folder):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    shutil.rmtree(os.path.join(folder, "__pycache__"), ignore_errors=True)
    done = subprocess.run([sys.executable, "-B", "run_lab.py"], cwd=folder, env=env,
                          capture_output=True, text=True, timeout=120)
    return done.returncode


def fresh_copy(parent):
    folder = tempfile.mkdtemp(prefix="lab12-", dir=parent)
    for name in FILES:
        shutil.copy(os.path.join(HERE, name), folder)
    shutil.copytree(os.path.join(HERE, "data"), os.path.join(folder, "data"))
    return folder


def main():
    parent = tempfile.mkdtemp(prefix="lab12-mutations-")
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
