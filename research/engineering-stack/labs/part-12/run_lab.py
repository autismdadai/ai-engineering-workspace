"""Checks for adaptmath.py and datacheck.py (Engineering Stack, Part 12).

Each check prints PASS or FAIL; a crash counts as a FAIL. Exit code 0 only if
every check passes. Each comment names the published figure it compares against.
"""
import os
import sys
from datetime import date

import adaptmath as am
import datacheck as dc

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = []


def check(fn):
    CHECKS.append(fn)
    return fn


def chat(*pairs):
    return {"messages": [{"role": r, "content": c} for r, c in pairs]}


@check
def c01_weight_counts():
    assert am.count_params(am.LLAMA3_8B) == 8_030_261_248          # Part 11 ("8B")
    assert am.count_params(am.SMOLLM2_135M) == 134_515_008          # "135M"
    q3 = am.count_params(am.QWEN3_06B)
    embed = am.QWEN3_06B["vocab"] * am.QWEN3_06B["hidden"]
    assert q3 == 596_049_920 and round((q3 - embed) / 1e9, 2) == 0.44, q3   # card: 0.6B, 0.44B


@check
def c02_reproduces_peft_readme():
    # PEFT 0.21.2 README: Qwen2.5-3B-Instruct, r=16, default targets, prints
    # "trainable params: 3,686,400 || all params: 3,089,625,088"
    lora = am.lora_params(am.QWEN25_3B, am.PEFT_DEFAULT_TARGETS["qwen2"], 16)
    assert lora == 3_686_400, lora
    assert am.count_params(am.QWEN25_3B) + lora == 3_089_625_088


@check
def c03_reproduces_lora_paper():
    # Hu et al., Table 4: GPT-3 with LoRA on Wq and Wv, 4.7M (r=1) and 37.7M (r=8)
    qv = ("q_proj", "v_proj")
    assert am.lora_params(am.GPT3_175B, qv, 1) == 4_718_592
    assert am.lora_params(am.GPT3_175B, qv, 8) == 37_748_736
    # Section 4.2: r=4 on q and v, checkpoint "35MB": 37.7 MB at 2 bytes, 36.0 MiB
    assert round(am.lora_params(am.GPT3_175B, qv, 4) * 2 / 2 ** 20) == 36


@check
def c04_llama3_8b_adapters():
    assert am.lora_params(am.LLAMA3_8B, ("q_proj", "v_proj"), 8) == 3_407_872
    every = am.lora_params(am.LLAMA3_8B, am.ALL_LINEAR, 16)
    assert every == 41_943_040 and round(100 * every / 8_030_261_248, 2) == 0.52


@check
def c05_one_matrix():
    cfg = dict(am.LLAMA3_8B, layers=1)
    assert am.lora_params(cfg, ("q_proj",), 8) == 8 * (4096 + 4096) == 65_536   # 0.39% of 4096 x 4096


@check
def c06_scaling():
    assert am.lora_scaling(8, 8) == 1.0                   # PEFT's defaults: r 8, alpha 8
    assert am.lora_scaling(32, 16) == 2.0                 # alpha = 2r (Biderman et al.)
    assert am.lora_scaling(16, 16, rslora=True) == 4.0    # alpha / sqrt(r)


@check
def c07_full_finetuning_memory():
    got = am.training_bytes(1.5e9, "full")
    assert got == 24e9, got                               # ZeRO: GPT-2 1.5B, "at least 24GB"
    assert am.training_bytes(7e9, "full") == 112e9
    assert am.training_bytes(65e9, "full") > 780e9        # QLoRA: 16-bit LLaMA 65B, "more than 780 GB"


@check
def c08_qlora_bits():
    assert am.NF4_BITS_NO_DOUBLE == 4.5                   # 32/64 = 0.5 bits of constants
    assert round(am.NF4_BITS - 4, 3) == 0.127             # "0.127 bits per parameter"
    saved = (am.NF4_BITS_NO_DOUBLE - am.NF4_BITS) * 65e9 / 8
    assert round(saved / 1e9, 1) == 3.0                   # "approximately 3 GB for a 65B model"
    assert am.training_bytes(65e9, "qlora") < 48e9        # base fits the 48 GB GPU of the claim


@check
def c09_lora_memory_and_fit():
    n = am.count_params(am.QWEN3_06B)
    a = am.lora_params(am.QWEN3_06B, am.PEFT_DEFAULT_TARGETS["qwen3"], 8)
    assert a == 1_146_880, a
    need = am.training_bytes(n, "lora_fp32", a)
    assert round(need / 1e9, 2) == 2.40, need
    assert am.fits(7.79, need) and not am.fits(7.79, am.training_bytes(n, "full"))
    assert not am.fits(2.9, need)                         # 2.9 GB x 0.8 = 2.32 GB


@check
def c10_openai_dates():
    f = am.openai_can_start_job
    assert f(date(2026, 5, 6), False, False)
    assert not f(date(2026, 5, 7), False, False) and f(date(2026, 5, 7), True, False)
    assert not f(date(2026, 7, 2), True, False) and f(date(2026, 7, 2), True, True)
    assert f(date(2027, 1, 5), True, True) and not f(date(2027, 1, 6), True, True)


@check
def c11_decision_rules():
    base = dict(new_facts=False, have_eval=True, prompt_tried=True, prompt_meets_bar=False,
                have_hardware=True)
    assert am.choose_approach(**base)[0] == "fine-tune with LoRA"
    assert am.choose_approach(**dict(base, new_facts=True))[0] == "retrieve"
    assert am.choose_approach(**dict(base, new_facts=True, have_eval=False))[0] == "retrieve"
    assert am.choose_approach(**dict(base, have_eval=False))[0] == "build an eval"
    assert am.choose_approach(**dict(base, prompt_tried=False))[0] == "prompt"
    assert am.choose_approach(**dict(base, prompt_meets_bar=True))[0] == "stop"
    assert am.choose_approach(**dict(base, have_hardware=False))[0] == "rent a GPU"


@check
def c12_sharing_names():
    assert am.name_ok("llama3", "Llama 3 Support Notes") and not am.name_ok("llama3", "Llama-Support")
    assert am.name_ok("llama3.1", "Llama-Support") and not am.name_ok("llama4", "SupportBot")
    assert not am.name_ok("llama3.1", "Support-Llama")              # "at the beginning"
    assert am.name_ok("apache-2.0", "SupportBot") and am.name_ok("muse-model-license", "SupportBot")
    assert any("outputs" in note for note in am.SHARING["llama3"]["notes"])
    assert not any("outputs" in note for note in am.SHARING["llama4"]["notes"])


@check
def c13_shortlist():
    open_ok = {"apache-2.0", "mit"}
    small = ["Qwen3.5-0.8B", "Granite 4.1 3B", "Phi-4-mini-instruct", "Gemma 4 E2B"]
    assert am.shortlist(7.79, open_ok) == small
    assert am.shortlist(7.79, open_ok, min_ctx=200_000) == ["Qwen3.5-0.8B", "Granite 4.1 3B"]
    assert am.shortlist(24, open_ok) == small + ["gpt-oss-20b", "Qwen3.8-27B", "Muse Glimmer 30B"]
    assert "Llama 4 Scout" not in am.shortlist(80, open_ok | {"llama4"})   # 66.6 GB > 64 GB
    assert "Llama 4 Scout" not in am.shortlist(100, open_ok)
    assert "Llama 4 Scout" in am.shortlist(100, open_ok | {"llama4"})


@check
def c14_sample_data():
    train = [ex for _, ex, _ in dc.load_jsonl(os.path.join(HERE, "data", "train.jsonl"))]
    test = [ex for _, ex, _ in dc.load_jsonl(os.path.join(HERE, "data", "test.jsonl"))]
    assert dc.duplicates(train) == [(2, 11)]                # example 12 repeats example 3
    assert dc.leaks(train, test) == [1]                     # test example 2 is a near copy
    assert all(not dc.problems(ex) for ex in train + test)


@check
def c15_format_problems():
    good = chat(("user", "hi"), ("assistant", "hello"))
    assert dc.kind(good) == "conversational" and not dc.problems(good)
    assert dc.problems(chat(("bot", "hi"), ("assistant", "hello")))
    assert dc.problems(chat(("user", "hi"), ("assistant", "  ")))
    assert dc.problems(chat(("assistant", "hello"), ("user", "thanks")))
    assert dc.problems({"prompt": "p", "chosen": "a", "rejected": "a"})
    assert not dc.problems({"prompt": "p", "chosen": "a", "rejected": "b"})
    assert dc.kind({"input": {}, "preferred_output": [1], "non_preferred_output": [2]}) == "openai-dpo"
    assert dc.problems({"question": "q"})


@check
def c16_leak_rules():
    long = "one two three four five six seven eight nine ten eleven twelve thirteen fourteen"
    shifted = "zero " + " ".join(long.split()[:13])            # shares exactly 13 in a row
    twelve = "zero " + " ".join(long.split()[:12])             # only 12 in a row
    t = [chat(("user", long), ("assistant", "x"))]
    assert dc.leaks(t, [chat(("user", shifted), ("assistant", "y"))]) == [0]
    assert dc.leaks(t, [chat(("user", twelve), ("assistant", "y"))]) == []
    assert dc.leaks(t, [chat(("user", "five six"), ("assistant", "seven"))]) == [0]  # short, inside
    sysmsg = ("system", long + " " + long)
    a = chat(sysmsg, ("user", "alpha"), ("assistant", "beta"))
    b = chat(sysmsg, ("user", "gamma"), ("assistant", "delta"))
    assert dc.leaks([a], [b]) == [] and dc.duplicates([a, b]) == []


class StubTokenizer:
    """Stands in for a real tokenizer: one token per character."""

    def apply_chat_template(self, messages, tokenize=False, add_generation_prompt=False):
        text = "".join(f"<{m['role']}>{m['content']}" for m in messages)
        return text + ("<assistant>" if add_generation_prompt else "")

    def __call__(self, text, add_special_tokens=False):
        return {"input_ids": [ord(ch) for ch in text]}


@check
def c17_reader_test_logic():
    import reader_lora
    p = reader_lora.plan()
    assert p["adapter"] == 460_800 and p["weights"] == 134_515_008, p
    ids, labels = reader_lora.encode(StubTokenizer(), [{"role": "user", "content": "hi"},
                                                       {"role": "assistant", "content": "ok"}])
    head = len("<user>hi<assistant>")
    assert labels[:head] == [-100] * head and labels[head:] == ids[head:] == [ord("o"), ord("k")]


def main():
    passed = 0
    for fn in CHECKS:
        try:
            fn()
            print(f"PASS {fn.__name__}")
            passed += 1
        except Exception as error:  # a crash counts as a failure
            print(f"FAIL {fn.__name__}: {type(error).__name__} {error}")
    print(f"{passed} of {len(CHECKS)} checks passed")
    return 0 if passed == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())
