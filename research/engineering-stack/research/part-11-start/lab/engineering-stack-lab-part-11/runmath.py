"""Part 11 lab: the arithmetic of running a model. Standard library only.

Every function takes plain numbers, so you can check each one by hand.
"""

GIB = 1024 ** 3

# Llama 3 8B, from meta-llama/llama-models, models/sku_list.py (commit 0e0b8c5).
LLAMA3_8B = {
    "dim": 4096, "n_layers": 32, "n_heads": 32, "n_kv_heads": 8,
    "vocab_size": 128256, "ffn_dim_multiplier": 1.3, "multiple_of": 1024,
    "tied_embeddings": False,
}


def ffn_width(dim, multiple_of, ffn_dim_multiplier=None):
    """Hidden width of the feed-forward block, as llama3/model.py computes it."""
    hidden = int(2 * (4 * dim) / 3)
    if ffn_dim_multiplier is not None:
        hidden = int(ffn_dim_multiplier * hidden)
    return multiple_of * ((hidden + multiple_of - 1) // multiple_of)


def llama_params(cfg):
    """Count the weights of a Llama-style decoder (no biases, RMSNorm)."""
    d, layers = cfg["dim"], cfg["n_layers"]
    head_dim = d // cfg["n_heads"]
    kv = cfg["n_kv_heads"] * head_dim
    hidden = ffn_width(d, cfg["multiple_of"], cfg.get("ffn_dim_multiplier"))
    attention = d * d + 2 * d * kv + d * d          # wq, wk, wv, wo
    feed_forward = 3 * d * hidden                    # w1, w2, w3
    norms = 2 * d
    per_layer = attention + feed_forward + norms
    embed = cfg["vocab_size"] * d
    output = 0 if cfg.get("tied_embeddings") else cfg["vocab_size"] * d
    return layers * per_layer + embed + output + d   # final norm


def weight_bytes(params, bits_per_weight):
    """Memory for the weights alone at an average number of bits per weight."""
    return params * bits_per_weight / 8


def kv_bytes_per_token(cfg, bytes_per_value=2):
    """Keys and values kept for one token across all layers."""
    head_dim = cfg["dim"] // cfg["n_heads"]
    return 2 * cfg["n_layers"] * cfg["n_kv_heads"] * head_dim * bytes_per_value


def kv_bytes(cfg, tokens, batch=1, bytes_per_value=2):
    return kv_bytes_per_token(cfg, bytes_per_value) * tokens * batch


def fits(memory_bytes, weights, kv, overhead_fraction=0.1):
    """True if weights plus KV cache plus a safety margin fit in memory."""
    return weights + kv <= memory_bytes * (1 - overhead_fraction)


def decode_tokens_per_second_ceiling(bandwidth_bytes_per_s, bytes_read_per_token):
    """Upper bound when each new token must read all weights once (batch 1)."""
    return bandwidth_bytes_per_s / bytes_read_per_token


def speculative_expected_tokens(alpha, gamma):
    """Expected tokens per target-model pass with gamma draft tokens and
    acceptance rate alpha (Leviathan et al., 2023): (1 - alpha^(gamma+1)) / (1 - alpha)."""
    if not 0 <= alpha <= 1 or gamma < 0:
        raise ValueError("alpha must be in [0, 1] and gamma >= 0")
    if alpha == 1:
        return gamma + 1
    return (1 - alpha ** (gamma + 1)) / (1 - alpha)
