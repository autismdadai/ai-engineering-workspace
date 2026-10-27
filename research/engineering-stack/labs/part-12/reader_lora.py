"""Reader test R3 (Engineering Stack, Part 12): a small LoRA run on your processor.

It trains a small LoRA adapter on your computer's processor and checks the lab's
arithmetic against PEFT's own count.

    python reader_lora.py --plan         # no downloads, no extra packages: predictions only
    python reader_lora.py --steps 24     # needs torch, transformers and peft (Section 7.5)

The full run downloads HuggingFaceTB/SmolLM2-135M-Instruct (Apache-2.0) from
Hugging Face once, trains LoRA (r 8, alpha 16, PEFT's default q and v targets)
on data/train.jsonl with a plain PyTorch loop, and saves the adapter to
lora-out/. It turns Hugging Face telemetry off before importing anything, and
doesn't use TRL, whose trainers send a usage ping by default.
"""
import argparse
import json
import os
import statistics
import sys
import time

os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("DO_NOT_TRACK", "1")

import adaptmath as am  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = "HuggingFaceTB/SmolLM2-135M-Instruct"
R, ALPHA = 8, 16


def plan():
    n = am.count_params(am.SMOLLM2_135M)
    a = am.lora_params(am.SMOLLM2_135M, am.PEFT_DEFAULT_TARGETS["llama"], R)
    return {"weights": n, "adapter": a, "gb": am.training_bytes(n, "lora_fp32", a) / 1e9}


def encode(tok, messages):
    """Token ids and labels; the prompt's labels are -100 so only the answer is learned."""
    prompt = tok.apply_chat_template(messages[:-1], tokenize=False, add_generation_prompt=True)
    full = tok.apply_chat_template(messages, tokenize=False)
    ids = tok(full, add_special_tokens=False)["input_ids"]
    head = tok(prompt, add_special_tokens=False)["input_ids"]
    if ids[:len(head)] != head:
        raise SystemExit("The chat template's prompt isn't a prefix of the full example.")
    return ids, [-100] * len(head) + ids[len(head):]


def train(steps, lr, out):
    try:
        import torch
        from peft import LoraConfig, get_peft_model
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as error:
        print(f"Missing package ({error.name}). Install torch, transformers and peft first "
              "(Part 12, Section 7.5), or run with --plan.")
        return 2

    torch.manual_seed(0)
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.float32)
    model = get_peft_model(model, LoraConfig(r=R, lora_alpha=ALPHA, task_type="CAUSAL_LM"))
    trainable, total = model.get_nb_trainable_parameters()
    p = plan()
    print(f"PEFT:       {trainable:,} trainable of {total:,} parameters")
    print(f"adaptmath:  {p['adapter']:,} trainable of {p['weights'] + p['adapter']:,} parameters")
    with open(os.path.join(HERE, "data", "train.jsonl"), encoding="utf-8") as f:
        data = [encode(tok, json.loads(line)["messages"]) for line in f if line.strip()]
    opt = torch.optim.AdamW([q for q in model.parameters() if q.requires_grad], lr=lr)
    model.train()
    losses, seconds, tokens = [], [], 0
    for step in range(steps):
        ids, labels = data[step % len(data)]
        start = time.perf_counter()
        result = model(input_ids=torch.tensor([ids]), labels=torch.tensor([labels]))
        result.loss.backward()
        opt.step()
        opt.zero_grad()
        seconds.append(time.perf_counter() - start)
        losses.append(result.loss.item())
        tokens += len(ids)
    first, last = statistics.mean(losses[:3]), statistics.mean(losses[-3:])
    print(f"Loss on the answers: {first:.3f} (first 3 steps) to {last:.3f} (last 3 steps)")
    print(f"Speed: {statistics.median(seconds):.2f} s per step (median), "
          f"{tokens / sum(seconds):.0f} tokens per second over {steps} steps")
    model.save_pretrained(out)
    size = sum(os.path.getsize(os.path.join(out, f)) for f in os.listdir(out))
    print(f"Adapter saved to {out}: {size / 1e6:.1f} MB")
    return 0 if trainable == p["adapter"] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--plan", action="store_true", help="print predictions only")
    parser.add_argument("--steps", type=int, default=24)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--out", default=os.path.join(HERE, "lora-out"))
    args = parser.parse_args()
    p = plan()
    print(f"{MODEL}: {p['weights']:,} weights; LoRA r={R} on q and v trains {p['adapter']:,}")
    print(f"Model states for LoRA in 32-bit: {p['gb']:.2f} GB, plus activations")
    if args.plan:
        return 0
    return train(args.steps, args.lr, args.out)


if __name__ == "__main__":
    sys.exit(main())
