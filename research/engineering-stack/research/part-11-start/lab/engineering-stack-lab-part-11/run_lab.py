"""Checks for runmath.py. Each check prints PASS or FAIL; any exception is a FAIL."""
import sys
import runmath as rm

CHECKS = []


def check(fn):
    CHECKS.append(fn)
    return fn


@check
def c1_ffn_width():
    # 2*16384/3 = 10922; *1.3 = 14198; rounded up to a multiple of 1024 = 14336
    assert rm.ffn_width(4096, 1024, 1.3) == 14336
    assert rm.ffn_width(4096, 256, None) == 11008  # the Llama 2 7B rule, as a second case


@check
def c2_param_count():
    n = rm.llama_params(rm.LLAMA3_8B)
    assert n == 8_030_261_248, n          # "8B"
    tied = dict(rm.LLAMA3_8B, tied_embeddings=True)
    assert n - rm.llama_params(tied) == 128256 * 4096


@check
def c3_weights():
    n = rm.llama_params(rm.LLAMA3_8B)
    assert round(rm.weight_bytes(n, 16) / rm.GIB, 2) == 14.96
    assert round(rm.weight_bytes(n, 8) / rm.GIB, 2) == 7.48
    assert round(rm.weight_bytes(n, 4) / rm.GIB, 2) == 3.74


@check
def c4_kv_cache():
    assert rm.kv_bytes_per_token(rm.LLAMA3_8B) == 131072          # 128 KiB at 16 bits
    assert rm.kv_bytes(rm.LLAMA3_8B, 8192) == 1 * rm.GIB
    assert rm.kv_bytes(rm.LLAMA3_8B, 8192, batch=4) == 4 * rm.GIB
    assert rm.kv_bytes(rm.LLAMA3_8B, 8192, bytes_per_value=1) == rm.GIB // 2
    no_gqa = dict(rm.LLAMA3_8B, n_kv_heads=32)                  # without grouped-query attention
    assert rm.kv_bytes_per_token(no_gqa) == 4 * rm.kv_bytes_per_token(rm.LLAMA3_8B)


@check
def c5_fits():
    n = rm.llama_params(rm.LLAMA3_8B)
    w16, w4 = rm.weight_bytes(n, 16), rm.weight_bytes(n, 4)
    kv = rm.kv_bytes(rm.LLAMA3_8B, 8192)
    assert not rm.fits(16 * rm.GIB, w16, kv)      # 16 GB card: 16-bit weights plus 8k context too big
    assert rm.fits(8 * rm.GIB, w4, kv)            # 4-bit weights fit in 8 GB
    assert not rm.fits(7.8 * 1e9, w16, 0)         # not on a 7.8 GB machine at 16 bits


@check
def c6_bandwidth_ceiling():
    # 3.35 TB/s (H100 SXM) reading 16-bit Llama 3 8B weights once per token
    n = rm.llama_params(rm.LLAMA3_8B)
    t = rm.decode_tokens_per_second_ceiling(3.35e12, rm.weight_bytes(n, 16))
    assert 208 < t < 209, t


@check
def c7_speculative():
    assert rm.speculative_expected_tokens(0, 4) == 1
    assert rm.speculative_expected_tokens(1, 4) == 5
    assert abs(rm.speculative_expected_tokens(0.8, 4) - 3.3616) < 1e-4
    for bad in [(-0.1, 4), (1.1, 4), (0.5, -1)]:
        try:
            rm.speculative_expected_tokens(*bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted {bad}")


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
