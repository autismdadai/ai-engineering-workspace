"""Checks for runmath.py and reader_local.py (Engineering Stack, Part 11).

Each check prints PASS or FAIL; a crash counts as a FAIL. Exit code 0 only if
every check passes. Published figures each check compares against are named
in its comment.
"""
import sys

import runmath as rm

CHECKS = []
LLAMA = rm.llama_tensors(rm.LLAMA3_8B)
N = rm.count(LLAMA)


def check(fn):
    CHECKS.append(fn)
    return fn


def close(a, b, tol):
    return abs(a - b) <= tol


@check
def c01_feed_forward_width():
    # 2*16384/3 = 10922; x1.3 = 14198; up to a multiple of 1024 = 14336
    assert rm.ffn_width(4096, 1024, 1.3) == 14336
    assert rm.ffn_width(4096, 256, None) == 11008       # Llama 2 7B's rule


@check
def c02_llama3_8b_weights():
    assert N == 8_030_261_248, N                          # "8B"
    assert sum(n for name, _, n in LLAMA if name == "attn_k") == 32 * 4096 * 1024


@check
def c03_bits_per_weight_from_block_layouts():
    want = {"Q4_0": 4.5, "Q8_0": 8.5, "MXFP4": 4.25, "Q2_K": 2.625, "Q3_K": 3.4375,
            "Q4_K": 4.5, "Q5_K": 5.5, "Q6_K": 6.5625, "IQ4_XS": 4.25, "F16": 16}
    for kind, bits in want.items():
        assert rm.bits_per_weight(kind) == bits, (kind, rm.bits_per_weight(kind))


@check
def c04_more_bits_layers():
    picked = [i for i in range(32) if rm.use_more_bits(i, 32)]
    assert picked == [0, 1, 2, 3, 6, 9, 12, 15, 18, 21, 24, 27, 28, 29, 30, 31], picked


@check
def c05_file_sizes_match_llama_cpp():
    # llama.cpp tools/quantize/README.md, Llama 3.1 8B: bits per weight and GiB
    table = {"F16": (rm.uniform("F16"), 16.0005, 14.96),
             "Q8_0": (rm.uniform("Q8_0"), 8.5008, 7.95),
             "Q6_K": (rm.uniform("Q6_K"), 6.5633, 6.14),
             "Q5_K_M": (rm.k_quant_m("Q5_K", "Q6_K"), 5.7036, 5.33),
             "Q4_K_M": (rm.k_quant_m("Q4_K", "Q6_K"), 4.8944, 4.58)}
    for label, (choose, bpw, gib) in table.items():
        size = rm.gguf_bytes(LLAMA, choose, 32)
        assert round(size * 8 / N, 4) == bpw, (label, size * 8 / N)
        assert round(size / rm.GIB, 2) == gib, (label, size / rm.GIB)
    assert rm.gguf_bytes(LLAMA, rm.k_quant_m("Q4_K", "Q6_K"), 32) == 4_912_898_048
    try:
        rm.gguf_bytes([("x", 0, 100)], rm.uniform("Q4_K"), 1)
    except ValueError:
        return
    raise AssertionError("accepted a tensor that doesn't fill whole blocks")


@check
def c06_gpt_oss_20b():
    # model card (arXiv 2508.10925) Table 1: 20.91B total, 3.61B active, 12.8 GiB
    p = rm.gpt_oss_params(rm.GPT_OSS_20B)
    assert round(p["total"] / 1e9, 2) == 20.91, p
    assert round(p["active"] / 1e9, 2) == 3.61, p
    stored, read = rm.gpt_oss_bytes(rm.GPT_OSS_20B)
    assert round(stored / rm.GIB, 1) == 12.8, stored
    assert 3.70e9 < read < 3.72e9, read                 # what one token reads


@check
def c07_kv_cache():
    assert rm.kv_bytes(40, 40, 128, 1) == 819_200       # OPT-13B, FP16: the vLLM paper's "800 KB"
    assert rm.kv_bytes(32, 8, 128, 1) == 131_072        # Llama 3 8B: 128 KiB per token
    assert rm.kv_bytes(32, 8, 128, 8192) == rm.GIB
    assert rm.kv_bytes(32, 8, 128, 8192, batch=4) == 4 * rm.GIB
    assert rm.kv_bytes(32, 8, 128, 8192, value_bytes=1) == rm.GIB // 2
    assert rm.kv_bytes(32, 32, 128, 1) == 4 * rm.kv_bytes(32, 8, 128, 1)   # no GQA
    full = rm.kv_bytes(24, 8, 64, 131072)
    windowed = rm.kv_bytes(24, 8, 64, 131072, window=128, windowed_layers=12)
    assert windowed == 2048 * (12 * 131072 + 12 * 128), windowed
    assert windowed < full / 1.99
    assert rm.kv_bytes(24, 8, 64, 100, window=128, windowed_layers=12) == rm.kv_bytes(24, 8, 64, 100)


@check
def c08_what_fits():
    w16 = rm.gguf_bytes(LLAMA, rm.uniform("F16"), 32)
    w4 = rm.gguf_bytes(LLAMA, rm.k_quant_m("Q4_K", "Q6_K"), 32)
    kv = rm.kv_bytes(32, 8, 128, 8192)
    assert not rm.fits(16 * rm.GIB, w16, kv), (w16, kv)  # 16-bit plus 8k context: too big for 16 GiB
    assert rm.fits(8 * rm.GIB, w4, kv), (w4, kv)        # Q4_K_M plus 8k context fits 8 GiB
    assert not rm.fits(7.8e9, w4, kv, overhead=0.5), (w4, kv)  # not if half the memory is taken
    per_token = rm.kv_bytes(32, 8, 128, 1)
    most = rm.max_tokens(16 * rm.GIB, w4, per_token)
    assert most == 80_482, most
    none = rm.max_tokens(4 * rm.GIB, w4, per_token)
    assert none == 0, none


@check
def c09_decode_ceiling():
    # H100 SXM, 3.35 TB/s, reading 16-bit Llama 3 8B once per token
    t = rm.decode_ceiling(3.35e12, rm.gguf_bytes(LLAMA, rm.uniform("F16"), 32))
    assert 208 < t < 209, t
    # Core i5-9500T: Intel lists 41.6 GB/s; Q4_K_M Llama 3 8B
    t = rm.decode_ceiling(41.6e9, rm.gguf_bytes(LLAMA, rm.k_quant_m("Q4_K", "Q6_K"), 32))
    assert close(t, 8.47, 0.01), t


@check
def c10_roofline():
    # H100 SXM dense BF16 = 1,979 / 2 (NVIDIA lists 1,979 with sparsity)
    assert close(rm.ridge_point(989.5e12, 3.35e12), 295.4, 0.1)
    assert close(rm.prefill_seconds(8e9, 1000, 989.5e12), 0.01617, 1e-5)


@check
def c11_speculative_decoding():
    assert rm.expected_tokens(0, 4) == 1
    assert rm.expected_tokens(1, 4) == 5
    assert close(rm.expected_tokens(0.8, 3), 2.952, 1e-3)   # the claim ledger's worked value
    assert close(rm.expected_tokens(0.8, 4), 3.3616, 1e-4)
    assert close(rm.speedup(0.8, 4, 0.05), 3.3616 / 1.2, 1e-4)
    for alpha, c in [(0.6, 0.05), (0.8, 0.05), (0.8, 0.3), (0.5, 0.2)]:
        best = rm.speedup(alpha, rm.best_gamma(alpha, c), c)
        assert best >= (1 + alpha) / (1 + c) - 1e-12, (alpha, c)   # Corollary 3.9
    for gamma in range(1, 21):
        assert rm.speedup(0.2, gamma, 0.25) < 1          # alpha below c never pays
    assert rm.best_gamma(0.2, 0.25) == 1                 # gamma counts from 1
    for bad in [(-0.1, 4), (1.1, 4), (0.5, -1)]:
        try:
            rm.expected_tokens(*bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted {bad}")


@check
def c12_paged_memory():
    lengths = [100, 200, 37, 512]
    assert close(rm.reserved_waste(lengths, 2048), 1 - 849 / 8192, 1e-12)
    assert close(rm.paged_waste(lengths, 16), 1 - 849 / 880, 1e-12)
    assert rm.paged_waste([32, 48], 16) == 0
    assert all(rm.paged_waste([n], 16) < 16 / (n + 15) for n in range(1, 300))
    try:
        rm.reserved_waste([3000], 2048)
    except ValueError:
        return
    raise AssertionError("accepted a request longer than its reservation")


@check
def c13_stream_metrics():
    # vLLM docs/benchmarking/cli.md example: TTFT 100 ms, 5 tokens by 180 ms
    m = rm.stream_metrics(0.0, [(0.100, 1), (0.140, 3), (0.180, 1)])
    assert close(m["ttft"], 0.100, 1e-9) and m["tokens"] == 5
    assert close(m["tpot"], 0.020, 1e-9), m              # vLLM's TPOT, AIPerf's ITL
    assert close(m["itl"], 0.040, 1e-9), m               # vLLM's ITL, AIPerf's ICL
    one = rm.stream_metrics(0.0, [(0.5, 1)])
    assert one["tpot"] == 0 and one["itl"] == 0


@check
def c14_reader_test_logic():
    import reader_local
    report = reader_local.self_test()
    assert report["measured"] == 12.5, report             # 64 tokens in 5.12 s
    assert close(report["ceiling"], 41.6e9 / 1.4e9, 1e-9), report


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
