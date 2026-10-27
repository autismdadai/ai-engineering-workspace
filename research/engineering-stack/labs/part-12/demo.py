"""Print the worked tables of Part 12 (Engineering Stack). Standard library only."""
from datetime import date

import adaptmath as am

MODELS = [("Llama 3 8B", am.LLAMA3_8B, "llama"), ("Qwen2.5-3B", am.QWEN25_3B, "qwen2"),
          ("Qwen3-0.6B", am.QWEN3_06B, "qwen3"), ("SmolLM2-135M", am.SMOLLM2_135M, "llama")]

print("1. Weights, counted from each config.json")
for name, cfg, _ in MODELS:
    print(f"   {name:13} {am.count_params(cfg):>15,}")

print("\n2. LoRA trainable parameters (share of the model; adapter at 2 bytes each)")
for name, cfg, family in MODELS:
    n = am.count_params(cfg)
    for label, targets, r in [("q, v (PEFT default)", am.PEFT_DEFAULT_TARGETS[family], 8),
                              ("all linear", am.ALL_LINEAR, 16), ("all linear", am.ALL_LINEAR, 256)]:
        a = am.lora_params(cfg, targets, r)
        print(f"   {name:13} {label:20} r={r:<4} {a:>12,} {100 * a / n:6.2f}%  {2 * a / 1e6:8.1f} MB")

print("\n3. Training memory, model states only (no activations), and what fits")
print("   with a fifth kept free: 7.79 GB (an office PC's RAM), 24 GB, 80 GB")
for name, cfg, family in MODELS[:1] + MODELS[2:3]:
    n = am.count_params(cfg)
    a = am.lora_params(cfg, am.ALL_LINEAR, 16)
    for method in ("full", "lora_fp32", "lora_bf16", "qlora"):
        need = am.training_bytes(n, method, 0 if method == "full" else a)
        marks = " ".join("yes" if am.fits(g, need) else " no" for g in (7.79, 24, 80))
        print(f"   {name:11} {method:10} {need / 1e9:7.2f} GB   {marks}")

print("\n4. Can an organization start a fine-tuning job on OpenAI?")
print("   (never tuned / tuned, no recent use / tuned and used in the last 60 days)")
for day in (date(2026, 5, 1), date(2026, 6, 1), date(2026, 10, 19), date(2027, 1, 6)):
    row = [am.openai_can_start_job(day, t, i) for t, i in ((False, False), (True, False), (True, True))]
    print(f"   {day}  " + "  ".join("yes" if x else " no" for x in row))

print("\n5. First shortlist: fits at about Q4_K_M, Apache-2.0 or MIT")
for memory in (7.79, 16, 24, 80):
    print(f"   {memory:>5} GB: {', '.join(am.shortlist(memory, {'apache-2.0', 'mit'}))}")

print("\n6. Which way to adapt")
base = dict(new_facts=False, have_eval=True, prompt_tried=True, prompt_meets_bar=False,
            have_hardware=True)
for label, change in [("product docs change weekly", {"new_facts": True}),
                      ("no test set yet", {"have_eval": False}),
                      ("prompting already passes", {"prompt_meets_bar": True}),
                      ("fixed JSON format, prompting falls short", {})]:
    answer, why = am.choose_approach(**dict(base, **change))
    print(f"   {label:41} -> {answer}: {why}")
