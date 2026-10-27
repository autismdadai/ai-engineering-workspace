"""Prompt-caching cost arithmetic: break-even points and worked totals.

Part 04 of The AI Engineering Stack. Standard library only.

Multipliers and prices were read from the providers' pages on
October 13, 2026 (Part 04, Section 6, and the freshness ledger). They change;
pass your own numbers rather than trusting these defaults later.
"""
from __future__ import annotations

from fractions import Fraction as F

# Multipliers of the base (uncached) input price.
ANTHROPIC_5M = {"write": F(125, 100), "read": F(1, 10)}
ANTHROPIC_1H = {"write": F(2), "read": F(1, 10)}
OPENAI_GPT56_PLUS = {"write": F(125, 100), "read": F(1, 10)}
OPENAI_EARLIER = {"write": F(1), "read": None}  # read rate varies by model


def cost_without_cache(prefix_tokens: int, requests: int, base_price: F) -> F:
    """Every request pays full price for the shared prefix."""
    return F(prefix_tokens) * requests * base_price


def cost_with_cache(prefix_tokens: int, requests: int, base_price: F,
                    write: F, read: F, writes: int = 1) -> F:
    """`writes` requests write the cache; the rest read it.

    writes=1 means the entry never expired between uses. If it expired
    before every reuse, writes equals requests and nothing is ever read.
    """
    if not 1 <= writes <= requests:
        raise ValueError("writes must be between 1 and requests")
    reads = requests - writes
    return F(prefix_tokens) * base_price * (write * writes + read * reads)


def break_even_reads(write: F, read: F) -> int:
    """Smallest number of reads k after one write for which caching costs less.

    Without caching, 1 + k requests cost (1 + k) units; with caching,
    write + read * k. Caching wins when k > (write - 1) / (1 - read).
    """
    if read >= 1:
        raise ValueError("a read must cost less than an uncached input")
    threshold = (write - 1) / (1 - read)
    if threshold < 0:
        return 0
    return int(threshold) + 1  # strictly more than the threshold


def gemini_explicit_uses_per_hour(input_price: F, cached_price: F,
                                  storage_per_hour: F) -> F:
    """Uses of a cached million tokens per hour needed to pay for storage.

    Each use saves (input - cached); storage costs storage_per_hour.
    Leaves out any charge for creating the cache, which the pages read did
    not state.
    """
    saving = input_price - cached_price
    if saving <= 0:
        raise ValueError("cached price must be below input price")
    return storage_per_hour / saving


def usd(x: F) -> str:
    return f"${float(x):,.4f}"


def demo():
    print("1. Break-even: reads needed after one write before caching costs less")
    for name, m in [("Anthropic 5-minute", ANTHROPIC_5M),
                    ("Anthropic 1-hour", ANTHROPIC_1H),
                    ("OpenAI GPT-5.6 and later", OPENAI_GPT56_PLUS)]:
        print(f"   {name:26s} write {float(m['write']):.2f}x, read {float(m['read']):.2f}x"
              f" -> {break_even_reads(m['write'], m['read'])} read(s)")
    print("   1-hour cache with 0.05x and with 0.025x reads:",
          break_even_reads(F(2), F(1, 20)), "and", break_even_reads(F(2), F(1, 40)), "reads")

    print("\n2. Claude Sonnet 5.5: $2 per million input tokens, reads 0.05x; 100,000-token prefix")
    base = F(2, 1_000_000)
    sonnet55_read = F(1, 20)
    for n in (2, 10):
        none = cost_without_cache(100_000, n, base)
        five = cost_with_cache(100_000, n, base, ANTHROPIC_5M["write"], sonnet55_read)
        hour = cost_with_cache(100_000, n, base, ANTHROPIC_1H["write"], sonnet55_read)
        print(f"   {n:2d} requests: no cache {usd(none)}; 5-minute {usd(five)}; 1-hour {usd(hour)}")
    worst = cost_with_cache(100_000, 10, base, ANTHROPIC_5M["write"], sonnet55_read, writes=10)
    print(f"   10 requests, each arriving after the entry expired: {usd(worst)}"
          f" ({float(worst / cost_without_cache(100_000, 10, base)):.2f}x the uncached cost)")

    print("\n3. Gemini explicit caching: uses per hour to cover storage (per million tokens)")
    rows = [("Gemini 3.8 Flash", F(75, 100), F(75, 1000), F(50, 100)),
            ("Gemini 3.1 Pro Preview (<=200K)", F(2), F(20, 100), F(450, 100)),
            ("Gemini 2.5 Pro", F(125, 100), F(125, 1000), F(450, 100))]
    for name, inp, cached, storage in rows:
        u = gemini_explicit_uses_per_hour(inp, cached, storage)
        print(f"   {name:32s} {float(u):.2f} uses per hour")


if __name__ == "__main__":
    demo()
