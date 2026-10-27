"""Plan what fits in a context window, and show what each overflow rule does.

Part 04 of The AI Engineering Stack. Standard library only.

Token counts here are estimates (about 4 characters per token for English,
the rule of thumb OpenAI and Google publish). Count with the provider's own
counter before relying on a number near the limit.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field


def estimate_tokens(text: str, chars_per_token: float = 4.0) -> int:
    """Rough token estimate for English text. Never 0 for non-empty text."""
    if not text:
        return 0
    return max(1, math.ceil(len(text) / chars_per_token))


@dataclass
class Part:
    """One piece of a request: a system prompt, a document, a chat turn."""
    name: str
    tokens: int
    priority: int = 0          # higher is kept first
    must_keep: bool = False    # the request is useless without it
    order: int = 0             # position in the request, for reporting


@dataclass
class Plan:
    window: int
    reserved_output: int
    kept: list = field(default_factory=list)
    dropped: list = field(default_factory=list)

    @property
    def input_budget(self) -> int:
        return self.window - self.reserved_output

    @property
    def used(self) -> int:
        return sum(p.tokens for p in self.kept)

    @property
    def remaining(self) -> int:
        return self.input_budget - self.used


class BudgetError(ValueError):
    """The parts that must be kept don't fit, so no plan exists."""


def plan_context(parts, window: int, reserved_output: int, growth: float = 1.0) -> Plan:
    """Keep must-keep parts, then add the rest in priority order. A part that
    doesn't fit is dropped, and smaller, lower-priority parts can still go in.

    `growth` is how much bigger the real counts may be than these estimates:
    1.3 if a newer tokenizer gives about 30% more tokens for the same text.
    The budget is divided by it, which is the same as a margin of
    1 - 1/1.3, about 23%.
    """
    if reserved_output >= window:
        raise BudgetError("reserved output leaves no room for input")
    plan = Plan(window=window, reserved_output=reserved_output)
    if growth < 1:
        raise BudgetError("growth below 1 would assume fewer tokens than estimated")
    budget = math.floor((window - reserved_output) / growth)
    must = [p for p in parts if p.must_keep]
    need = sum(p.tokens for p in must)
    if need > budget:
        raise BudgetError(f"must-keep parts need {need} tokens; budget is {budget}")
    plan.kept.extend(must)
    used = need
    rest = sorted((p for p in parts if not p.must_keep),
                  key=lambda p: (-p.priority, p.order))
    for p in rest:
        if used + p.tokens <= budget:
            plan.kept.append(p)
            used += p.tokens
        else:
            plan.dropped.append(p)
    plan.kept.sort(key=lambda p: p.order)
    return plan


# Overflow rules, as the providers document them (Part 04, Section 3.3).
# Each takes chat messages [(role, tokens)] and a token limit for the input.

def overflow_error(messages, limit):
    """Anthropic and OpenAI by default: refuse the request (HTTP 400)."""
    total = sum(t for _, t in messages)
    if total > limit:
        return {"status": 400, "kept": None, "dropped": None}
    return {"status": 200, "kept": list(range(len(messages))), "dropped": []}


def overflow_drop_oldest(messages, limit):
    """OpenAI Responses with truncation "auto": drop items from the start."""
    idx = list(range(len(messages)))
    dropped = []
    while idx and sum(messages[i][1] for i in idx) > limit:
        dropped.append(idx.pop(0))
    return {"status": 200 if idx else 400, "kept": idx, "dropped": dropped}


def overflow_keep_system_and_last(messages, limit):
    """Ollama's chat default, read from its source: drop the oldest messages,
    but keep system messages and always the last message. No error is
    returned; the server logs it only at debug level."""
    keep_always = {i for i, (role, _) in enumerate(messages) if role == "system"}
    keep_always.add(len(messages) - 1)
    idx = list(range(len(messages)))
    dropped = []
    while sum(messages[i][1] for i in idx) > limit:
        removable = [i for i in idx if i not in keep_always]
        if not removable:
            break
        dropped.append(removable[0])
        idx.remove(removable[0])
    return {"status": 200, "kept": idx, "dropped": dropped}


def demo():
    print("1. Planning a request for a 1,000,000-token window, 128,000 reserved for output")
    parts = [
        Part("system prompt", 2_000, must_keep=True, order=0),
        Part("tool definitions", 6_000, must_keep=True, order=1),
        Part("contract.pdf as text", 400_000, priority=5, order=2),
        Part("old email thread", 300_000, priority=1, order=3),
        Part("policy handbook", 250_000, priority=3, order=4),
        Part("question", 200, must_keep=True, order=5),
    ]
    plan = plan_context(parts, window=1_000_000, reserved_output=128_000)
    print(f"   input budget {plan.input_budget:,}; used {plan.used:,}; left {plan.remaining:,}")
    print("   kept:   ", ", ".join(p.name for p in plan.kept))
    print("   dropped:", ", ".join(p.name for p in plan.dropped) or "nothing")
    g = plan_context(parts, window=1_000_000, reserved_output=128_000, growth=1.3)
    print(f"   if real counts are 30% higher (growth 1.3): budget {math.floor(g.input_budget / 1.3):,};"
          f" left {math.floor(g.input_budget / 1.3) - g.used:,}; dropped:",
          ", ".join(p.name for p in g.dropped) or "nothing")

    print("\n2. The same chat sent to three overflow rules, input limit 4,096 tokens")
    chat = [("system", 300), ("user", 1_500), ("assistant", 900),
            ("user", 1_200), ("assistant", 700), ("user", 400)]
    total = sum(t for _, t in chat)
    print(f"   chat total {total:,} tokens; the first user turn holds the key fact")
    for name, rule in [("error (Anthropic, OpenAI default)", overflow_error),
                       ("drop oldest (OpenAI truncation auto)", overflow_drop_oldest),
                       ("keep system and last (Ollama chat)", overflow_keep_system_and_last)]:
        r = rule(chat, 4_096)
        print(f"   {name:40s} status {r['status']}; dropped {r['dropped']}")


if __name__ == "__main__":
    demo()
