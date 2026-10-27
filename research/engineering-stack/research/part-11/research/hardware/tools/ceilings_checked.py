# Upper bound on batch-1 decode speed: tokens/s <= peak memory bandwidth / bytes read per token.
# Bytes per token approximated by weight bytes only (ignores KV cache, activations, kernel efficiency).
hw = [  # name, peak GB/s, memory GB available to the model (None = depends on installed RAM), source row
    ("Core i5-9500T, 2ch DDR4-2666 (Intel max)", 41.6, None, "H061"),
    ("Apple M5", 153, 32, "H071"),
    ("Ryzen AI Max+ 395 (256-bit x 8000 MT/s, derived)", 256, 128, "H072"),
    ("DGX Spark GB10", 273, 128, "H067"),
    ("Apple M5 Pro", 307, 64, "H071"),
    ("RTX 5060 Ti 16 GB", 448, 16, "H069"),
    ("Apple M5 Max 40-core GPU", 614, 128, "H071"),
    ("RTX 5090", 1792, 32, "H069"),
    ("H100 SXM (caller-established page read)", 3350, 80, "caller"),
    ("H200 SXM", 4800, 141, "H050"),
    ("MI355X", 8000, 288, "H058"),
]
models = [("8B @ 4-bit (4.0 GB)", 8e9*0.5/1e9), ("8B @ 16-bit (16 GB)", 8e9*2/1e9), ("70B @ 4-bit (35 GB)", 70e9*0.5/1e9)]
print("| Hardware [row] | Peak GB/s | " + " | ".join(m[0] for m in models) + " |")
print("|---|---|" + "---|"*len(models))
for name, bw, cap, src in hw:
    cells = []
    for mname, gb in models:
        if cap is not None and gb >= cap:
            cells.append("does not fit")
        else:
            cells.append(f"{bw/gb:,.0f}")
    print(f"| {name} [{src}] | {bw:,.1f} | " + " | ".join(cells) + " |")
print()
print("NVLink per direction (H100):", 18*25, "GB/s; 400 Gb/s IB per direction:", 400/8, "GB/s; ratio", (18*25)/(400/8))
print("H100 HBM 3350 GB/s vs NVLink 450 GB/s each way:", round(3350/450,1), "x")
print("8 x 700 W =", 8*700, "W =", 8*0.7, "kW;", round(5600/10200*100), "% of DGX H100 10.2 kW max")
print("i5-9500T: 2 x 8 B x 2666 MT/s =", round(2*8*2666/1000,2), "GB/s; 2 x 8 x 2600 =", 2*8*2600/1000)
print("GB300 NVL72: 576/72 =", 576/72, "TB/s per GPU; 20 TB/72 =", round(20000/72), "GB")
print("Vera Rubin NVL72: 1400/72 =", round(1400/72,2), "TB/s; 20.7 TB/72 =", round(20700/72,1), "GB; 216/72 =", 216/72, "TB/s NVLink")
print("HGX Vera Rubin NVL8: 130/8 =", 130/8, "TB/s; 2 TB/8 =", 2000/8, "GB")
print("HGX B300: 2.1 TB/8 =", 2100/8, "GB; HGX B200: 1.4 TB/8 =", 1400/8, "GB; DGX H200: 1128/8 =", 1128/8, "GB; DGX H100: 640/8 =", 640/8)
print("H100 FP8 sparse 3958 / 2 =", 3958/2, "(dense by NVIDIA's half-of-sparse convention)")
