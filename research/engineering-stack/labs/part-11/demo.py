"""Print the worked tables of Part 11 (Engineering Stack). Standard library only."""
import runmath as rm

LLAMA = rm.llama_tensors(rm.LLAMA3_8B)
N = rm.count(LLAMA)
Q4KM = rm.k_quant_m("Q4_K", "Q6_K")

print("1. Llama 3 8B file sizes (tensor data), against llama.cpp's published table")
print(f"   {N:,} weights")
published = {"F16": (16.0005, 14.96), "Q8_0": (8.5008, 7.95), "Q6_K": (6.5633, 6.14),
             "Q5_K_M": (5.7036, 5.33), "Q4_K_M": (4.8944, 4.58)}
choosers = {"F16": rm.uniform("F16"), "Q8_0": rm.uniform("Q8_0"), "Q6_K": rm.uniform("Q6_K"),
            "Q5_K_M": rm.k_quant_m("Q5_K", "Q6_K"), "Q4_K_M": Q4KM}
for label, choose in choosers.items():
    size = rm.gguf_bytes(LLAMA, choose, 32)
    bpw, gib = published[label]
    print(f"   {label:7} {size * 8 / N:7.4f} bits/weight {size / rm.GIB:6.2f} GiB "
          f"{size / 1e9:6.2f} GB   llama.cpp: {bpw} and {gib} GiB")

print("\n2. KV cache")
for label, args, kw in [("OPT-13B, 16-bit, 1 token", (40, 40, 128, 1), {}),
                        ("Llama 3 8B, 16-bit, 1 token", (32, 8, 128, 1), {}),
                        ("Llama 3 8B, 16-bit, 8,192 tokens", (32, 8, 128, 8192), {}),
                        ("gpt-oss-20b, 131,072 tokens, no window", (24, 8, 64, 131072), {}),
                        ("gpt-oss-20b, 131,072 tokens, 128-token window on 12 layers",
                         (24, 8, 64, 131072), {"window": 128, "windowed_layers": 12})]:
    b = rm.kv_bytes(*args, **kw)
    print(f"   {label}: {b:,} bytes = {b / rm.GIB:.3f} GiB")

p = rm.gpt_oss_params(rm.GPT_OSS_20B)
stored, read = rm.gpt_oss_bytes(rm.GPT_OSS_20B)
print(f"\n3. gpt-oss-20b: {p['total']:,} weights, {p['active']:,} used per token")
print(f"   stored {stored / rm.GIB:.2f} GiB ({stored / 1e9:.2f} GB); one token reads {read / 1e9:.2f} GB")

print("\n4. Decode ceilings, tokens per second at batch 1 (bandwidth / bytes per token)")
models = {"qwen3:1.7b (1.4 GB)": 1.4e9, "Llama 3 8B Q4_K_M": rm.gguf_bytes(LLAMA, Q4KM, 32),
          "gpt-oss-20b (reads)": read, "Llama 3 8B F16": rm.gguf_bytes(LLAMA, rm.uniform("F16"), 32)}
stored = {"qwen3:1.7b (1.4 GB)": 1.4e9, "gpt-oss-20b (reads)": rm.gpt_oss_bytes(rm.GPT_OSS_20B)[0]}
chips = {"Core i5-9500T, 41.6 GB/s": (41.6e9, 7.8e9), "Apple M5, 153 GB/s": (153e9, None),
         "DGX Spark, 273 GB/s": (273e9, 128e9), "RTX 5060 Ti, 448 GB/s": (448e9, 16e9),
         "RTX 5090, 1,792 GB/s": (1792e9, 32e9), "H100 SXM, 3,350 GB/s": (3350e9, 80e9)}
print("   " + " " * 26 + "".join(f"{m[:19]:>21}" for m in models))
for chip, (bandwidth, memory) in chips.items():
    cells = []
    for name, b in models.items():
        too_big = memory is not None and stored.get(name, b) > memory
        cells.append(f"{'too big':>21}" if too_big else f"{rm.decode_ceiling(bandwidth, b):21.1f}")
    print(f"   {chip:26}" + "".join(cells))
print("   (too big: the weights alone exceed the memory; Apple M5 memory depends on the model bought)")

print("\n5. Roofline, H100 SXM, dense BF16 (989.5 TFLOPS) and 3.35 TB/s")
print(f"   ridge point {rm.ridge_point(989.5e12, 3.35e12):.1f} operations per byte")
print(f"   1,000-token prompt through 8.03B weights: at least "
      f"{rm.prefill_seconds(N, 1000, 989.5e12) * 1000:.1f} ms")

print("\n6. Speculative decoding: draft cost c = 0.05 of a target pass")
for alpha in (0.5, 0.6, 0.7, 0.8, 0.9):
    g = rm.best_gamma(alpha, 0.05)
    print(f"   alpha {alpha}: best gamma {g:2}, {rm.expected_tokens(alpha, g):.2f} tokens per pass, "
          f"speed-up {rm.speedup(alpha, g, 0.05):.2f}x")
print(f"   alpha 0.2 with c = 0.25: best {max(rm.speedup(0.2, g, 0.25) for g in range(1, 21)):.2f}x")

lengths = [100, 200, 37, 512]
print(f"\n7. KV memory for requests of {lengths} tokens")
print(f"   reserve 2,048 slots each: {rm.reserved_waste(lengths, 2048):.1%} empty")
print(f"   blocks of 16 tokens:     {rm.paged_waste(lengths, 16):.1%} empty")

m = rm.stream_metrics(0.0, [(0.100, 1), (0.140, 3), (0.180, 1)])
print("\n8. One streamed reply: chunks at 100, 140 and 180 ms carrying 1, 3 and 1 tokens")
print(f"   TTFT {m['ttft'] * 1000:.0f} ms, TPOT {m['tpot'] * 1000:.0f} ms, "
      f"ITL {m['itl'] * 1000:.0f} ms, {m['tokens']} tokens")
