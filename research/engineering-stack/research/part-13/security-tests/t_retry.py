import sys; sys.path.insert(0, "/home/claude/part13/phase4/security/lab/engineering-stack-lab-part-13")
import shipmath as sm, time
for h in ({"retry-after": "86400"}, {"retry-after-ms": "-5000"}, {"retry-after-ms": "nan"}, {"retry-after-ms": "inf"}, {"retry-after-ms": "soon"}):
    try:
        w = sm.retry_plan("openai", 429, h, 0); print(f"{h} -> wait {w!r}", end="")
        try: time.sleep(w if w < 0 or w != w else 0); print("")
        except Exception as e: print(f"; time.sleep(wait) raises {type(e).__name__}: {e}")
    except Exception as e: print(f"{h} -> {type(e).__name__}: {e}")
# layered retries: lab plan (2 retries) on top of an SDK that also retries twice by default
lab = 1 + sum(1 for a in range(10) if sm.retry_plan("anthropic", 529, {}, a) is not None)
print(f"attempts per call: lab plan {lab}, SDK default 3 (max_retries=2); layered {lab} x 3 = {lab*3} model calls for one user request")
