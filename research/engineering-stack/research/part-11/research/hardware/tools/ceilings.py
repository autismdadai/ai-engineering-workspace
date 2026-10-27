# WARNING (2026-10-16): the row IDs in this file point to an earlier claims file that was never written.
# They do NOT match claims.md. Use ceilings_checked.py, whose inputs are all re-read rows in claims.md.
# Upper bound on single-stream decode speed: tokens/s <= bandwidth / bytes read per token.
# Bytes per token approximated by weight bytes only (ignores KV cache, activations, overheads).
hw = [  # name, peak memory bandwidth GB/s, memory capacity GB (usable by model, approx), source row
    ("Core i5-9500T, dual-channel DDR4-2666 (Intel max)", 41.6, None, "H089"),
    ("Apple M5", 153, 32, "H083"),
    ("AMD Ryzen AI Max+ 395 (derived 256-bit x 8000 MT/s)", 256, 128, "H087"),
    ("DGX Spark (GB10)", 273, 128, "H077"),
    ("RTX Spark (porting guide)", 300, 128, "H081"),
    ("Apple M5 Pro", 307, 64, "H083"),
    ("RTX 5060 Ti 16 GB", 448, 16, "H073"),
    ("Apple M5 Max 40-core GPU", 614, 128, "H083"),
    ("RTX 5070 Ti", 896, 16, "H072"),
    ("RTX 5080", 960, 16, "H071"),
    ("Apple M5 Ultra", 1200, 512, "H084"),
    ("RTX 5090", 1792, 32, "H070"),
    ("H100 SXM (caller's product-page read)", 3350, 80, "ledger"),
    ("H200 SXM", 4800, 141, "H024"),
    ("MI355X", 8000, 288, "H067"),
    ("Rubin GPU (NVL72 page)", 19200, 288, "H008"),
]
models = [("8B params at 4 bits (~4.0 GB)", 8e9*0.5/1e9), ("8B params at 16 bits (~16 GB)", 8e9*2/1e9), ("70B params at 4 bits (~35 GB)", 70e9*0.5/1e9)]
print("| Hardware | Peak GB/s | " + " | ".join(m[0] for m in models) + " |")
print("|---|---|" + "---|"*len(models))
for name, bw, cap, src in hw:
    cells = []
    for mname, gb in models:
        if cap is not None and gb > cap:
            cells.append("does not fit")
        else:
            cells.append(f"{bw/gb:,.0f}")
    print(f"| {name} [{src}] | {bw:,.1f} | " + " | ".join(cells) + " |")
# DGX H100 networking vs NVLink
nvlink_total=900; nvlink_each=nvlink_total/2; ib_each=400/8
print("\nNVLink each way GB/s:", nvlink_each, "IB 400 Gb/s each way GB/s:", ib_each, "ratio:", nvlink_each/ib_each)
print("H100 local HBM 3350 GB/s vs NVLink each way 450 GB/s ratio:", round(3350/450,1))
print("i5-9500T theoretical 2ch x 64-bit x 2666 MT/s =", round(2*8*2666/1000,2), "GB/s (Intel lists 41.6)")
print("8 x 700 W =", 8*700, "W; DGX H100 max 10.2 kW; ratio", round(5600/10200,2))
print("Ryzen AI Max+ 395: 256 bit/8 * 8000 MT/s =", 256/8*8000/1000, "GB/s")
print("GB300 NVL72 576 TB/s / 72 =", 576/72, "TB/s; GB200 superchip 16 TB/s / 2 =", 16/2)
print("Rubin NVL72 1400 TB/s / 72 =", round(1400/72,2), "; 216/72 =", 216/72, "; 20.7 TB/72 =", round(20.7e3/72,1), "GB")
print("HGX Vera Rubin NVL8 130 TB/s / 8 =", 130/8, "; 2 TB / 8 =", 2000/8, "GB")
print("HGX B300 2.1 TB/8 =", 2100/8, "GB; HGX B200 1.4 TB/8 =", 1400/8, "GB")
print("H100 FP8 sparse 3958 / 2 =", 3958/2)
