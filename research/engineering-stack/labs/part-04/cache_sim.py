"""A stand-in for a provider's prompt cache, to see why prompt order matters.

Part 04 of The AI Engineering Stack. Standard library only.

It follows the rules Anthropic documents for explicit breakpoints (Part 04,
Section 3.5): blocks in the order tools, then system, then messages; a cache
entry is written only at a block marked as a breakpoint; a hit needs the
whole prefix up to that point to be identical; each breakpoint looks back at
most 20 block positions for an earlier entry; an entry lives 5 minutes (or 1
hour), and each hit refreshes it; a prefix shorter than the model's minimum
is processed without caching, with no error. It is a model of the
documented behaviour, not the provider's code. Other details (for example a
run of tool_use blocks counting as one position) are left out.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

LEVELS = ("tools", "system", "messages")
LOOKBACK = 20


@dataclass(frozen=True)
class Block:
    level: str          # "tools", "system" or "messages"
    text: str
    tokens: int
    breakpoint: bool = False
    ttl: int = 300      # seconds: 300 (5 minutes) or 3600 (1 hour)


class OrderError(ValueError):
    pass


def check_order(blocks):
    ranks = [LEVELS.index(b.level) for b in blocks]
    if ranks != sorted(ranks):
        raise OrderError("blocks must go tools, then system, then messages")
    if sum(b.breakpoint for b in blocks) > 4:
        raise OrderError("at most 4 breakpoints")


def prefix_key(blocks, end):
    """Fingerprint of blocks[0:end]; any change anywhere before `end` changes it."""
    h = hashlib.sha256()
    for b in blocks[:end]:
        h.update(f"{b.level}\x00{b.text}\x00".encode())
    return h.hexdigest()


class PromptCache:
    def __init__(self, minimum_tokens: int = 1024):
        self.minimum = minimum_tokens
        self.entries = {}   # key -> (expires_at, ttl)

    def request(self, blocks, now: float) -> dict:
        """Process one request at time `now` (seconds). Returns usage counts
        named like Anthropic's: cache_read_input_tokens,
        cache_creation_input_tokens and input_tokens."""
        check_order(blocks)
        cum = [0]
        for b in blocks:
            cum.append(cum[-1] + b.tokens)
        total = cum[-1]
        bps = [i + 1 for i, b in enumerate(blocks) if b.breakpoint]  # prefix ends
        if not bps:
            return {"cache_read_input_tokens": 0, "cache_creation_input_tokens": 0,
                    "input_tokens": total}

        # Longest earlier entry that is still alive, within the lookback window
        # of some breakpoint.
        hit_end = 0
        for bp in bps:
            for end in range(bp, max(0, bp - LOOKBACK), -1):
                key = prefix_key(blocks, end)
                entry = self.entries.get(key)
                if entry and entry[0] > now and end > hit_end:
                    hit_end = end
                    break
        if hit_end:
            key = prefix_key(blocks, hit_end)
            _, ttl = self.entries[key]
            self.entries[key] = (now + ttl, ttl)   # a hit refreshes the lifetime

        # Write an entry at each breakpoint beyond the hit, if long enough.
        written_to = hit_end
        for bp in bps:
            if bp <= hit_end:
                continue
            if cum[bp] < self.minimum:
                continue   # too short: processed without caching, no error
            ttl = blocks[bp - 1].ttl
            self.entries[prefix_key(blocks, bp)] = (now + ttl, ttl)
            written_to = bp
        read = cum[hit_end]
        created = cum[written_to] - cum[hit_end]
        return {"cache_read_input_tokens": read,
                "cache_creation_input_tokens": created,
                "input_tokens": total - read - created}


def cost_units(usage, write=1.25, read=0.1):
    """Cost in units of 'one token at the base input price'."""
    return (usage["input_tokens"] + write * usage["cache_creation_input_tokens"]
            + read * usage["cache_read_input_tokens"])


def conversation(system_text, doc_tokens=8_000, turns=3, ttl=300):
    """Requests for a chat about one long document, one per user turn."""
    reqs = []
    history = []
    for t in range(turns):
        history = history + [Block("messages", f"question {t}", 50)]
        blocks = [Block("tools", "search tool definition", 400),
                  Block("system", system_text, 1_600),
                  Block("system", "the document", doc_tokens, breakpoint=True, ttl=ttl)]
        blocks += history
        reqs.append(blocks)
        history = history + [Block("messages", f"answer {t}", 300)]
    return reqs


def run(reqs, times, minimum=1024):
    cache = PromptCache(minimum)
    return [cache.request(b, t) for b, t in zip(reqs, times)]


def demo():
    stable = "You answer questions about the attached document."
    print("A. Stable prefix, three turns one minute apart")
    a = run(conversation(stable), [0, 60, 120])
    for i, u in enumerate(a):
        print(f"   turn {i}: {u}")

    print("\nB. A timestamp at the top of the system prompt changes every request")
    reqs = [conversation(f"Time now: 09:0{i}. " + stable)[i] for i in range(3)]
    b = run(reqs, [0, 60, 120])
    for i, u in enumerate(b):
        print(f"   turn {i}: {u}")

    print("\nC. Second turn arrives 6 minutes later: 5-minute versus 1-hour lifetime")
    c5 = run(conversation(stable, turns=2, ttl=300), [0, 360])
    c60 = run(conversation(stable, turns=2, ttl=3600), [0, 360])
    print(f"   5-minute: {c5[1]}")
    print(f"   1-hour:   {c60[1]}")

    print("\nD. A 300-token prefix with a breakpoint, model minimum 512")
    tiny = [[Block("system", "short instructions", 300, breakpoint=True),
             Block("messages", "hi", 5)]] * 2
    for i, u in enumerate(run(tiny, [0, 10], minimum=512)):
        print(f"   request {i}: {u}")

    none_cost = sum(b.tokens for r in conversation(stable) for b in r)  # all at base price
    print("\nCost of the three turns in base-price token units (write 1.25x, read 0.1x):")
    print(f"   no caching {none_cost:,.0f}; stable prefix {sum(map(cost_units, a)):,.0f};"
          f" timestamp at top {sum(map(cost_units, b)):,.0f}")


if __name__ == "__main__":
    demo()
