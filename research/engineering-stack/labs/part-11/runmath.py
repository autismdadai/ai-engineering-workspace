"""The arithmetic of running a model, for learning (Engineering Stack, Part 11).

Standard library only. Every function takes plain numbers, so each result can
be checked by hand: weights (1), quantized file sizes (2), the KV cache (3),
speed limits (4), speculative decoding (5), paged KV memory (6) and serving
metrics (7). The part's Section 3 explains each one. These are bounds and
estimates, not measurements: a real run is slower and uses more memory.
"""

GIB = 1024 ** 3

# ---------------------------------------------------------------- 1. weights

# Llama 3 8B: meta-llama/llama-models, models/sku_list.py (commit 0e0b8c5).
LLAMA3_8B = {"dim": 4096, "n_layers": 32, "n_heads": 32, "n_kv_heads": 8,
             "vocab": 128256, "ffn_multiplier": 1.3, "multiple_of": 1024}


def ffn_width(dim, multiple_of, multiplier=None):
    """Feed-forward width, as models/llama3/model.py computes it."""
    hidden = int(2 * (4 * dim) / 3)
    if multiplier is not None:
        hidden = int(multiplier * hidden)
    return multiple_of * ((hidden + multiple_of - 1) // multiple_of)


def llama_tensors(cfg):
    """(name, layer, number of weights) for every tensor of a Llama-style model.
    Norms are one-dimensional; everything else is a matrix."""
    d, n = cfg["dim"], cfg["n_layers"]
    kv = cfg["n_kv_heads"] * (d // cfg["n_heads"])
    f = ffn_width(d, cfg["multiple_of"], cfg.get("ffn_multiplier"))
    out = [("token_embd", None, cfg["vocab"] * d)]
    for i in range(n):
        out += [("attn_norm", i, d), ("attn_q", i, d * d), ("attn_k", i, d * kv),
                ("attn_v", i, d * kv), ("attn_output", i, d * d), ("ffn_norm", i, d),
                ("ffn_gate", i, d * f), ("ffn_up", i, d * f), ("ffn_down", i, f * d)]
    return out + [("output_norm", None, d), ("output", None, cfg["vocab"] * d)]


def count(tensors):
    return sum(n for _, _, n in tensors)


# gpt-oss-20b: openai/gpt-oss, gpt_oss/torch/model.py (commit 5681a6b), with
# the 20b values from its config.json: 24 layers and 32 experts.
GPT_OSS_20B = {"hidden": 2880, "n_layers": 24, "n_heads": 64, "n_kv_heads": 8,
               "head_dim": 64, "n_experts": 32, "per_token": 4, "ffn": 2880,
               "vocab": 201088, "window": 128}


def gpt_oss_params(c):
    """Total weights, and the weights one token uses (4 of the experts)."""
    h, hd, n = c["hidden"], c["head_dim"], c["n_layers"]
    qkv = hd * (c["n_heads"] + 2 * c["n_kv_heads"])
    attention = n * (h * qkv + qkv + hd * c["n_heads"] * h + h + c["n_heads"] + h)
    expert = 3 * c["ffn"] * h + 2 * c["ffn"] + h        # two matrices and their biases
    router = n * (h * c["n_experts"] + c["n_experts"] + h)  # gate, its bias, the MLP norm
    embed = c["vocab"] * h                              # the unembedding is the same size
    total = attention + router + n * c["n_experts"] * expert + 2 * embed + h
    active = attention + router + n * c["per_token"] * expert + embed + h
    return {"total": total, "active": active}


def gpt_oss_bytes(c, expert_bits=4.25, other_bits=16):
    """(checkpoint bytes, bytes one token reads): expert matrices in MXFP4,
    everything else in BF16 (openai/gpt-oss README)."""
    p = gpt_oss_params(c)
    per_expert = 3 * c["ffn"] * c["hidden"]
    mx_all = c["n_layers"] * c["n_experts"] * per_expert
    mx_one = c["n_layers"] * c["per_token"] * per_expert
    stored = (mx_all * expert_bits + (p["total"] - mx_all) * other_bits) / 8
    read = (mx_one * expert_bits + (p["active"] - mx_one) * other_bits) / 8
    return stored, read


# ------------------------------------------------------ 2. quantized sizes

# (weights per block, bytes per block), from ggml/src/ggml-common.h
# (llama.cpp commit f336359). F32, F16 and BF16 store each weight alone.
BLOCKS = {"F32": (1, 4), "F16": (1, 2), "BF16": (1, 2), "Q8_0": (32, 34),
          "Q4_0": (32, 18), "MXFP4": (32, 17), "Q2_K": (256, 84), "Q3_K": (256, 110),
          "Q4_K": (256, 144), "Q5_K": (256, 176), "Q6_K": (256, 210), "IQ4_XS": (256, 136)}


def bits_per_weight(kind):
    weights, size = BLOCKS[kind]
    return 8 * size / weights


def use_more_bits(i, n):
    """llama.cpp's rule for which layers get more bits (src/llama-quant.cpp)."""
    return i < n // 8 or i >= 7 * n // 8 or (i - n // 8) % 3 == 2


def k_quant_m(base, upgrade):
    """Q4_K_M (base Q4_K) or Q5_K_M (base Q5_K) for a dense model that isn't
    Falcon: attn_v and ffn_down go to `upgrade` on use-more-bits layers, the
    output matrix to Q6_K, norms stay F32."""
    def choose(name, layer, n_layers):
        if name.endswith("norm"):
            return "F32"
        if name == "output":
            return "Q6_K"
        if name in ("attn_v", "ffn_down") and use_more_bits(layer, n_layers):
            return upgrade
        return base
    return choose


def uniform(kind):
    return lambda name, layer, n_layers: "F32" if name.endswith("norm") else kind


def gguf_bytes(tensors, choose, n_layers):
    """Bytes of tensor data (the file adds a little metadata)."""
    total = 0
    for name, layer, n in tensors:
        weights, size = BLOCKS[choose(name, layer, n_layers)]
        if n % weights:
            raise ValueError(f"{name}: {n} weights don't fill whole blocks")
        total += n // weights * size
    return total


# ----------------------------------------------------------- 3. KV cache

def kv_bytes(n_layers, n_kv_heads, head_dim, tokens, batch=1, value_bytes=2,
             window=None, windowed_layers=0):
    """Keys and values kept for `tokens` tokens of each of `batch` sequences.
    Layers with a sliding window keep at most `window` tokens."""
    per_layer_token = 2 * n_kv_heads * head_dim * value_bytes
    kept = (n_layers - windowed_layers) * tokens
    kept += windowed_layers * (min(tokens, window) if window else tokens)
    return per_layer_token * kept * batch


def fits(memory, weights, kv, overhead=0.1):
    """True if weights plus KV cache fit, keeping `overhead` of memory spare."""
    return weights + kv <= memory * (1 - overhead)


def max_tokens(memory, weights, kv_per_token, batch=1, overhead=0.1):
    """Most tokens per sequence that fit next to the weights (0 if none)."""
    room = memory * (1 - overhead) - weights
    return max(0, int(room // (kv_per_token * batch)))


# ---------------------------------------------------------- 4. speed limits

def decode_ceiling(bandwidth, bytes_per_token):
    """Tokens per second if each new token must read `bytes_per_token` from
    memory once: an upper bound for one sequence, never a prediction."""
    return bandwidth / bytes_per_token


def ridge_point(flops, bandwidth):
    """Operations per byte where compute and memory limit equally (roofline)."""
    return flops / bandwidth


def prefill_seconds(n_weights, tokens, flops):
    """Lower bound for reading a prompt: one multiply and one add per weight
    per token, at the chip's peak (attention's own work not counted)."""
    return 2 * n_weights * tokens / flops


# --------------------------------------------------- 5. speculative decoding

def _check(alpha, gamma, c=0.0):
    if not 0 <= alpha <= 1 or gamma < 0 or c < 0:
        raise ValueError("alpha must be in [0, 1], gamma and c at least 0")


def expected_tokens(alpha, gamma):
    """Tokens per target pass with gamma draft tokens and acceptance rate
    alpha: (1 - alpha^(gamma+1)) / (1 - alpha), Leviathan et al. Eq. (1)."""
    _check(alpha, gamma)
    if alpha == 1:
        return gamma + 1
    return (1 - alpha ** (gamma + 1)) / (1 - alpha)


def speedup(alpha, gamma, c):
    """Expected walltime improvement when one draft run costs c target runs
    (Theorem 3.8). Below 1 means slower than not speculating."""
    _check(alpha, gamma, c)
    return expected_tokens(alpha, gamma) / (gamma * c + 1)


def best_gamma(alpha, c, largest=20):
    return max(range(1, largest + 1), key=lambda g: speedup(alpha, g, c))


# ------------------------------------------------------ 6. paged KV memory

def reserved_waste(lengths, reserve):
    """Share of KV slots holding no token when every request reserves
    `reserve` slots in one piece up front."""
    if max(lengths) > reserve:
        raise ValueError("a request is longer than its reservation")
    return 1 - sum(lengths) / (reserve * len(lengths))


def paged_waste(lengths, block):
    """Share of slots holding no token when memory comes in blocks of `block`
    tokens: only each request's last block can be partly empty."""
    allocated = sum(-(-n // block) * block for n in lengths)
    return 1 - sum(lengths) / allocated


# --------------------------------------------------------- 7. serving metrics

def stream_metrics(sent, chunks):
    """TTFT, TPOT and ITL for one streamed reply. `chunks` lists (arrival
    time, tokens in the chunk). TPOT follows vLLM's formula, which NVIDIA's
    AIPerf calls ITL; ITL here is vLLM's gap between chunks (AIPerf's ICL)."""
    times = [t for t, _ in chunks]
    n = sum(k for _, k in chunks)
    ttft, e2e = times[0] - sent, times[-1] - sent
    gaps = [b - a for a, b in zip(times, times[1:])]
    return {"ttft": ttft, "tpot": (e2e - ttft) / (n - 1) if n > 1 else 0.0,
            "itl": sum(gaps) / len(gaps) if gaps else 0.0, "tokens": n}
