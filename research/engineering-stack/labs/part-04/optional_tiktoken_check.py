"""Optional reader test: compare the 4-characters-per-token estimate with
tiktoken's o200k_base counts.

Install first (hash-pinned): python -m pip install --require-hashes -r requirements-optional.txt
The first call downloads the encoding file from openaipublic.blob.core.windows.net,
so it needs that site to be reachable once; later runs use a local cache.
o200k_base is the encoding tiktoken maps to gpt-5 and gpt-4o; tiktoken 0.14.0
has no entry for GPT-6 models, so treat its counts for those as estimates.
"""
import sys

from token_budget import estimate_tokens

SAMPLES = {
    "plain English": ("The committee met on Tuesday to review the budget. Members asked "
                      "for clearer reporting on travel costs and agreed to meet again "
                      "next month after the auditors finish their work."),
    "Python code": ("def mean(xs):\n    if not xs:\n        raise ValueError('empty')\n"
                    "    return sum(xs) / len(xs)\n"),
    "numbers and IDs": "Order 4821-ZX-0093 shipped 2026-10-13 to 80521; total $1,284.77.",
}


def main():
    try:
        import tiktoken
    except ImportError:
        print("FAIL  tiktoken is not installed in this environment (see the install line at the top)")
        return 1
    try:
        enc = tiktoken.get_encoding("o200k_base")
    except Exception as error:  # first use downloads the encoding file
        print("FAIL  could not load o200k_base; the first use downloads it from "
              f"openaipublic.blob.core.windows.net ({type(error).__name__})")
        return 1
    ok = True
    for name, text in SAMPLES.items():
        real = len(enc.encode(text))
        est = estimate_tokens(text)
        ok &= real > 0
        print(f"{name:16s} {len(text):4d} chars  o200k_base {real:3d} tokens"
              f"  ({len(text) / real:.2f} chars per token)  estimate {est:3d}")
    print("PASS" if ok else "FAIL", " tiktoken counted every sample")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
