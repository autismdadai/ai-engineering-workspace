"""adaptmath: the arithmetic of choosing and adapting a model (Engineering Stack, Part 12).

Standard library only. Nothing here downloads or trains a model. Each table
names where its numbers come from; Part 12, Section 12, gives the sources.
"""
import math
from datetime import date

GB = 1e9

# ----------------------------------------------------------- 1. model shapes
# From each model's config.json. Qwen2 puts a bias on q, k and v; Qwen3 adds a
# small norm on q and on k instead. "tied": the output layer reuses the
# embedding matrix, so it is stored once.
LLAMA3_8B = dict(hidden=4096, layers=32, heads=32, kv_heads=8, head_dim=128, ffn=14336,
                 vocab=128256, tied=False, qkv_bias=False, qk_norm=False)
QWEN25_3B = dict(hidden=2048, layers=36, heads=16, kv_heads=2, head_dim=128, ffn=11008,
                 vocab=151936, tied=True, qkv_bias=True, qk_norm=False)
QWEN3_06B = dict(hidden=1024, layers=28, heads=16, kv_heads=8, head_dim=128, ffn=3072,
                 vocab=151936, tied=True, qkv_bias=False, qk_norm=True)
SMOLLM2_135M = dict(hidden=576, layers=30, heads=9, kv_heads=3, head_dim=64, ffn=1536,
                    vocab=49152, tied=True, qkv_bias=False, qk_norm=False)
# GPT-3 175B (Brown et al. 2020, Table 2.1): only the attention shapes are used.
GPT3_175B = dict(hidden=12288, layers=96, heads=96, kv_heads=96, head_dim=128, ffn=4 * 12288,
                 vocab=50257, tied=True, qkv_bias=True, qk_norm=False)

ALL_LINEAR = ("q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj")
# PEFT 0.21.2, src/peft/utils/constants.py: the default when you name no target.
PEFT_DEFAULT_TARGETS = {"llama": ("q_proj", "v_proj"), "mistral": ("q_proj", "v_proj"),
                        "qwen2": ("q_proj", "v_proj"), "qwen3": ("q_proj", "v_proj")}


def linear_shapes(c):
    """(inputs, outputs) of each linear layer in one transformer block."""
    q, kv, h, f = c["heads"] * c["head_dim"], c["kv_heads"] * c["head_dim"], c["hidden"], c["ffn"]
    return {"q_proj": (h, q), "k_proj": (h, kv), "v_proj": (h, kv), "o_proj": (q, h),
            "gate_proj": (h, f), "up_proj": (h, f), "down_proj": (f, h)}


def count_params(c):
    """All weights: embedding, blocks, final norm, and the output layer unless tied."""
    shapes = linear_shapes(c)
    block = sum(i * o for i, o in shapes.values()) + 2 * c["hidden"]       # two RMSNorms
    if c["qkv_bias"]:
        block += sum(shapes[n][1] for n in ("q_proj", "k_proj", "v_proj"))
    if c["qk_norm"]:
        block += 2 * c["head_dim"]
    embed = c["vocab"] * c["hidden"]
    return embed * (1 if c["tied"] else 2) + c["layers"] * block + c["hidden"]


# ------------------------------------------------------------ 2. LoRA counts
def lora_params(c, targets, r):
    """LoRA trains B (outputs x r) and A (r x inputs): r * (d + k) per matrix (Hu et al.)."""
    shapes = linear_shapes(c)
    return c["layers"] * sum(r * sum(shapes[t]) for t in targets)


def lora_scaling(alpha, r, rslora=False):
    """How much the update BA is multiplied by: alpha / r, or alpha / sqrt(r) with rsLoRA."""
    return alpha / math.sqrt(r) if rslora else alpha / r


# --------------------------------------------------- 3. memory for training
# ZeRO (Rajbhandari et al.), Section 3.1: mixed-precision Adam keeps 2 bytes of
# weights, 2 of gradients and 12 of optimizer state per trained parameter.
ADAM_MIXED_BYTES = 2 + 2 + 12
# QLoRA (Dettmers et al.): NF4 is 4 bits; one 32-bit constant per 64 weights adds
# 0.5 bits, and double quantization cuts that to 8/64 + 32/(64*256) = 0.127 bits.
NF4_BITS = 4 + 8 / 64 + 32 / (64 * 256)
NF4_BITS_NO_DOUBLE = 4 + 32 / 64
BASE_BITS = {"full": None, "lora_fp32": 32, "lora_bf16": 16, "qlora": NF4_BITS}


def training_bytes(n_base, method, n_adapter=0):
    """Model states only: no activations, batch, sequence length or framework overhead."""
    if method == "full":
        return ADAM_MIXED_BYTES * n_base
    return n_base * BASE_BITS[method] / 8 + ADAM_MIXED_BYTES * n_adapter


def fits(memory_gb, need_bytes, overhead=0.2):
    """Same rule as Part 11: keep a fifth of the memory free for everything not counted."""
    return need_bytes <= memory_gb * GB * (1 - overhead)


# ------------------------------------------------ 4. hosted fine-tuning dates
# OpenAI deprecations page, "Update to OpenAI's self-serve fine-tuning" (read
# October 19, 2026). Other providers: Part 12, Section 3.6.
OPENAI_CLOSED_TO_NEW = date(2026, 5, 7)
OPENAI_RECENT_ONLY = date(2026, 7, 2)
OPENAI_CLOSED_TO_ALL = date(2027, 1, 6)


def openai_can_start_job(day, tuned_before, inference_last_60_days):
    """Can this organization create a new fine-tuning job on OpenAI on this day?"""
    if day >= OPENAI_CLOSED_TO_ALL:
        return False
    if day >= OPENAI_RECENT_ONLY:
        return tuned_before and inference_last_60_days
    if day >= OPENAI_CLOSED_TO_NEW:
        return tuned_before
    return True


# -------------------------------------------------- 5. which way to adapt
# First rule that matches wins. Evidence: retrieval beat fine-tuning on new facts
# (Ovadia et al.); unknown facts raise hallucination once learned (Gekhman et al.);
# vendors say prompt and measure first (OpenAI, Anthropic, Hugging Face, Mistral).
RULES = [  # (question, answer that triggers the rule, advice, why)
    ("new_facts", True, "retrieve",
     "new facts are learned slowly and raise hallucination; retrieve (Part 05)"),
    ("have_eval", False, "build an eval",
     "without your own test set you can't tell if anything helped (Part 02)"),
    ("prompt_tried", False, "prompt", "try prompting and a stronger or smaller model first"),
    ("prompt_meets_bar", True, "stop", "prompting already passes your eval; keep it"),
    ("have_hardware", False, "rent a GPU", "no machine you have can train it (Section 6)"),
]


def choose_approach(**need):
    """need: new_facts, have_eval, prompt_tried, prompt_meets_bar, have_hardware (all bool)."""
    for key, value, answer, why in RULES:
        if need[key] == value:
            return answer, why
    return ("fine-tune with LoRA",
            "a measured gap on your eval that prompting couldn't close; re-run safety tests after")


# ------------------------------------------- 6. licence duties when sharing
# From each licence's own text (Part 12, Section 3.7). Information, not legal advice.
SHARING = {
    "apache-2.0": {"prefix": None, "notes": ["give a copy of the licence", "mark files you changed",
                                             "keep the NOTICE file's notices"]},
    "mit": {"prefix": None, "notes": ["keep the copyright and licence notice"]},
    "llama3": {"prefix": "Llama 3", "notes": ['show "Built with Meta Llama 3"', "ship the licence",
                                              "no outputs to improve other LLMs"]},
    "llama3.1": {"prefix": "Llama", "notes": ['show "Built with Llama"', "ship the licence"]},
    "muse-model-license": {"prefix": None, "notes": [
        'show "Built with Muse Spark Open"', "separate agreement to host it above a revenue threshold",
        "gated: read the full licence first"]},
}
SHARING["llama4"] = SHARING["llama3.1"]      # Llama 3.2 and Llama 4 use the same clause


def name_ok(licence, model_name):
    """Llama licences require the shared model's name to start with their word."""
    prefix = SHARING[licence]["prefix"]
    return prefix is None or model_name.startswith(prefix)


# ------------------------------------------------- 7. a first shortlist
# Publisher-stated facts read October 16 to 19, 2026 (Part 11 and Part 12).
# params: billions stored (all experts count, Part 11); ctx: tokens, with "128K"
# read as 131,072 and "1M" as 1,000,000.
CANDIDATES = [
    ("Qwen3.5-0.8B", 0.8, "apache-2.0", 262144),
    ("Granite 4.1 3B", 3.0, "apache-2.0", 524288),          # "up to 512K"
    ("Phi-4-mini-instruct", 3.8, "mit", 131072),
    ("Gemma 4 E2B", 5.1, "apache-2.0", 131072),
    ("gpt-oss-20b", 21.0, "apache-2.0", 131072),
    ("Qwen3.8-27B", 27.0, "apache-2.0", 262144),
    ("Muse Glimmer 30B", 29.6, "apache-2.0", 131072),
    ("Llama 4 Scout", 109.0, "llama4", 10_000_000),
    ("Muse Spark Open", 816.0, "muse-model-license", 1_000_000),
]
Q4_K_M_BITS = 4.89          # Part 11: about 4.89 bits per weight for Llama 3 8B


def shortlist(memory_gb, licences, min_ctx=0, bits=Q4_K_M_BITS):
    """Candidates whose weights fit at about Q4_K_M, with an allowed licence and context."""
    keep = []
    for name, params, licence, ctx in CANDIDATES:
        if licence in licences and ctx >= min_ctx and fits(memory_gb, params * 1e9 * bits / 8):
            keep.append(name)
    return keep
