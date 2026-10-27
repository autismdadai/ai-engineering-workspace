import sys, time, tracemalloc
sys.path.insert(0, "/home/claude/part13/phase4/security/lab/engineering-stack-lab-part-13")
import ssewire
t = sys.argv[1]
if t == "utf8":
    for label, b in [("lone 0xff", b"data: a\xffb\n\n"), ("bad continuation", b"data: \xe2\x28\xa1\n\n"),
                     ("overlong", b"data: \xc0\xaf\n\n"), ("surrogate", b"data: \xed\xa0\x80\n\n")]:
        try: print(f"{label:17} -> {[e.data for e in ssewire.parse_all(b)]}")
        except Exception as e: print(f"{label:17} -> {type(e).__name__}: {e}")
    p = ssewire.Parser(); p.feed(b"data: ok\n\n")
    try: p.feed(b"\xff"); print("later bad byte: accepted")
    except Exception as e: print("later bad byte after a good event ->", type(e).__name__)
    print("spec's expected (UTF-8 decode with replacement):", repr(b"data: a\xffb".decode("utf-8", "replace")))
elif t == "longline":
    for n in (256*1024, 512*1024, 1024*1024, 2048*1024):
        p = ssewire.Parser(); chunk = b"x" * 256
        tracemalloc.start(); t0 = time.perf_counter()
        for _ in range(n // 256): p.feed(chunk)
        dt = time.perf_counter() - t0; cur = tracemalloc.get_traced_memory()[0]; tracemalloc.stop()
        print(f"{n//1024:5} KiB, no newline, 256-byte reads: {dt:6.2f} s, buffered {cur/2**20:.1f} MiB, events 0")
elif t == "manylines":
    for n in (10_000, 20_000, 40_000, 80_000):
        data = b"data: x\n" * n + b"\n"
        t0 = time.perf_counter(); ev = ssewire.parse_all(data)
        print(f"{n:6} data lines ({len(data)//1024} KiB) in one feed: {time.perf_counter()-t0:6.2f} s, events {len(ev)}")
elif t == "datalines":
    p = ssewire.Parser(); line = b"data: " + b"y" * 250 + b"\n"
    tracemalloc.start()
    for _ in range(20000): p.feed(line)
    print(f"20,000 data lines with no blank line: parser holds {len(p.data)/2**20:.1f} MiB, events 0")
elif t == "emptyfeed":
    p = ssewire.Parser()
    ev = p.feed(b"data: a\r") + p.feed(b"") + p.feed(b"\ndata: b\n\n")
    print("CR | empty feed | LF:", [e.data for e in ev], " expected ['a\\nb']")
