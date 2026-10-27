"""datacheck: check a fine-tuning data set before you train on it (Engineering Stack, Part 12).

Standard library only. It reads JSON Lines files (one example per line) and reports:
  - the format of each example (the names TRL 1.16.0 uses, plus OpenAI's DPO format),
  - examples a trainer would reject or learn nothing from,
  - exact duplicates inside the training file,
  - test examples that leak from the training file: they share a run of 13 words
    with a training example, the rule GPT-3's authors used to flag contamination
    (Brown et al. 2020, Section 4), or, when shorter than 13 words, appear whole.
    System messages are left out of both comparisons, since every example may share one.

    python datacheck.py data/train.jsonl data/test.jsonl
"""
import json
import re
import sys

ROLES = {"system", "user", "assistant", "tool"}
N = 13


def load_jsonl(path):
    """[(line number, example or None, error or None)] for each non-empty line."""
    rows = []
    with open(path, encoding="utf-8") as f:
        for number, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                rows.append((number, json.loads(line), None))
            except json.JSONDecodeError as error:
                rows.append((number, None, f"not JSON: {error.msg}"))
    return rows


def kind(ex):
    keys = set(ex) if isinstance(ex, dict) else set()
    if "messages" in keys:
        return "conversational"
    if {"prompt", "chosen", "rejected"} <= keys:
        return "preference"
    if {"input", "preferred_output", "non_preferred_output"} <= keys:
        return "openai-dpo"
    if {"prompt", "completion"} <= keys:
        return "prompt-completion"
    if "text" in keys:
        return "language-modeling"
    return "unknown"


def problems(ex):
    """Reasons a trainer would reject this example or learn nothing from it."""
    k = kind(ex)
    if k == "unknown":
        return ["no known format (messages, prompt and completion, prompt/chosen/rejected, or text)"]
    found = []
    if k == "conversational":
        msgs = ex["messages"]
        if not isinstance(msgs, list) or not msgs:
            return ["messages is empty or not a list"]
        for i, m in enumerate(msgs):
            if not isinstance(m, dict) or m.get("role") not in ROLES:
                found.append(f"message {i}: role must be one of {sorted(ROLES)}")
            elif not isinstance(m.get("content"), str) or not m["content"].strip():
                found.append(f"message {i}: empty content")
        if isinstance(msgs[-1], dict) and msgs[-1].get("role") != "assistant":
            found.append("last message isn't the assistant's, so there is no answer to learn")
    else:
        fields = {"preference": ("prompt", "chosen", "rejected"),
                  "openai-dpo": ("preferred_output", "non_preferred_output"),
                  "prompt-completion": ("prompt", "completion"),
                  "language-modeling": ("text",)}[k]
        for field in fields:
            if not isinstance(ex[field], (str, list)) or not ex[field]:
                found.append(f"{field} is empty")
        if k == "preference" and ex["chosen"] == ex["rejected"]:
            found.append("chosen and rejected are the same, so there is nothing to prefer")
        if k == "openai-dpo" and ex["preferred_output"] == ex["non_preferred_output"]:
            found.append("preferred and non-preferred outputs are the same")
    return found


def text_of(value):
    """All the words in an example, whatever its format."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(text_of(v) for v in value)
    if isinstance(value, dict):
        if value.get("role") == "system":       # a shared system prompt isn't a leak
            return ""
        return " ".join(text_of(v) for key, v in sorted(value.items()) if key != "role")
    return ""


def words(ex):
    return re.findall(r"[a-z0-9']+", text_of(ex).lower())


def grams(ws, n=N):
    return {tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def contains(long, short):
    return any(long[i:i + len(short)] == short for i in range(len(long) - len(short) + 1))


def duplicates(examples):
    """Pairs (first, later) of examples with the same words, by position."""
    seen, pairs = {}, []
    for i, ex in enumerate(examples):
        key = tuple(words(ex))
        if key in seen:
            pairs.append((seen[key], i))
        else:
            seen[key] = i
    return pairs


def leaks(train, test, n=N):
    """Positions of test examples that overlap a training example."""
    train_words = [words(ex) for ex in train]
    pool = set().union(*(grams(ws, n) for ws in train_words)) if train_words else set()
    found = []
    for j, ex in enumerate(test):
        ws = words(ex)
        hit = (grams(ws, n) & pool) if len(ws) >= n else any(contains(t, ws) for t in train_words)
        if ws and hit:
            found.append(j)
    return found


def check(train_path, test_path=None):
    """Print a report; return the number of problems found."""
    bad = 0
    sets = {}
    for label, path in (("train", train_path), ("test", test_path)):
        if not path:
            continue
        rows = load_jsonl(path)
        kinds = {}
        for number, ex, error in rows:
            issues = [error] if error else problems(ex)
            kinds[kind(ex)] = kinds.get(kind(ex), 0) + 1
            for issue in issues:
                print(f"  {label} line {number}: {issue}")
                bad += 1
        sets[label] = [ex for _, ex, error in rows if not error]
        print(f"{label}: {len(rows)} examples, formats {kinds}")
    for first, later in duplicates(sets["train"]):
        print(f"  train: example {later + 1} repeats example {first + 1}")
        bad += 1
    if "test" in sets:
        for j in leaks(sets["train"], sets["test"]):
            print(f"  test: example {j + 1} shares {N} words in a row with the training data")
            bad += 1
    if len(sets["train"]) < 10:
        print("  note: OpenAI's fine-tuning minimum was 10 examples; most tasks need far more")
    print(f"{bad} problem(s) found")
    return bad


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__.split("\n\n")[-1])
    sys.exit(1 if check(*sys.argv[1:]) else 0)
