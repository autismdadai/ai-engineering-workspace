"""shipmath: the arithmetic and rules of running a model behind an API
(Engineering Stack, Part 13).

Standard library only. Prices and rules were read from the vendors' pages on
October 20, 2026 (Part 13, Section 12); they change, so pass your own. All
money is in US dollars, kept as Fractions so the checks are exact.
"""
from __future__ import annotations

import json
import math
import re
from fractions import Fraction as F

M = 1_000_000  # prices are per million tokens

# ------------------------------------------------------------ 1. price sheets
# Per million tokens. "cache_read" and "cache_write" are what a cached prefix
# costs to read or to write. None means the page read gave no figure.
PRICES = {
    # Anthropic pricing page: Sonnet 5.5 $2 in, $10 out; cache reads 0.05x
    # and 5-minute writes 1.25x the input price (Part 04, Section 3.5).
    "claude-sonnet-5-5": dict(input=F(2), output=F(10), cache_read=F(1, 10), cache_write=F(5, 2)),
    # Haiku 5.5: $0.10 / $0.50; a prompt over 100,000 tokens (cache reads and
    # writes included) pays $0.50 / $2.50 for the whole request.
    "claude-haiku-5-5": dict(input=F(1, 10), output=F(1, 2), cache_read=None, cache_write=None),
    # OpenAI gpt-6-astra: $10 in, $1 cached, $12.50 cache write, $50 out;
    # over 272,000 input tokens: 2x input and cache rates, 1.5x output.
    "gpt-6-astra": dict(input=F(10), output=F(50), cache_read=F(1), cache_write=F(25, 2)),
    # Gemini 3.1 Pro Preview: $2 / $12 up to 200k prompt tokens, $4 / $18 above.
    "gemini-3.1-pro-preview": dict(input=F(2), output=F(12), cache_read=None, cache_write=None),
}

# Whole-request long-context rules: (threshold in prompt tokens, how the
# threshold counts tokens, multipliers or replacement prices).
LONG_CONTEXT = {
    "claude-haiku-5-5": dict(over=100_000, counts="all_input",
                             prices=dict(input=F(1, 2), output=F(5, 2))),
    "gpt-6-astra": dict(over=272_000, counts="all_input",
                        times=dict(input=F(2), cache_read=F(2), cache_write=F(2), output=F(3, 2))),
    "gemini-3.1-pro-preview": dict(over=200_000, counts="all_input",
                                   prices=dict(input=F(4), output=F(18))),
}

BATCH = F(1, 2)            # all three vendors: half price (Section 3.9)
RESIDENCY = {"anthropic-us": F(11, 10), "openai-regional": F(11, 10)}


def prompt_tokens(usage: dict) -> int:
    """All input tokens of a request: uncached, cache reads and cache writes."""
    return usage.get("input", 0) + usage.get("cache_read", 0) + usage.get("cache_write", 0)


def rates_for(model: str, usage: dict) -> dict:
    """The per-million rates that apply to this one request."""
    rates = dict(PRICES[model])
    rule = LONG_CONTEXT.get(model)
    if rule and prompt_tokens(usage) > rule["over"]:
        for key, value in rule.get("prices", {}).items():
            rates[key] = value
        for key, factor in rule.get("times", {}).items():
            if rates.get(key) is not None:
                rates[key] = rates[key] * factor
    return rates


def request_cost(model: str, usage: dict, batch: bool = False,
                 residency: str | None = None) -> F:
    """Dollars for one request. usage: input (uncached), cache_read,
    cache_write, output, in tokens. Batch and residency multiply the total."""
    rates = rates_for(model, usage)
    total = F(0)
    for key in ("input", "cache_read", "cache_write", "output"):
        tokens = usage.get(key, 0)
        if tokens:
            if rates.get(key) is None:
                raise ValueError(f"no {key} price for {model}")
            total += rates[key] * tokens / M
    if batch:
        total *= BATCH
    if residency:
        total *= RESIDENCY[residency]
    return total


def monthly(cost_per_request: F, requests_per_day: float, days: int = 30) -> F:
    return cost_per_request * F(requests_per_day).limit_denominator() * days


# ----------------------------------------------------- 2. load and latency
def concurrent(arrivals_per_second: float, seconds_in_system: float) -> float:
    """Little's law: average number in the system L = lambda x W."""
    if arrivals_per_second < 0 or seconds_in_system < 0:
        raise ValueError("rates and times are not negative")
    return arrivals_per_second * seconds_in_system


def percentile(values: list[float], q: float) -> float:
    """Nearest-rank percentile: the smallest value with at least q% at or below it."""
    if not values or not 0 < q <= 100:
        raise ValueError("need values and 0 < q <= 100")
    ordered = sorted(values)
    rank = math.ceil(q / 100 * len(ordered))
    return ordered[rank - 1]


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def stream_timing(t_request: float, chunk_times: list[float]) -> dict:
    """Time to first chunk, total time and mean gap between chunks, in seconds."""
    if not chunk_times:
        raise ValueError("no chunks")
    gaps = [b - a for a, b in zip(chunk_times, chunk_times[1:])]
    return {"time_to_first_chunk": chunk_times[0] - t_request,
            "total": chunk_times[-1] - t_request,
            "mean_gap": sum(gaps) / len(gaps) if gaps else 0.0}


# ------------------------------------------------------ 3. when to retry
MAX_WAIT = 60.0            # longest wait obeyed from a retry-after header


def retry_plan(vendor: str, status: int, headers: dict, attempt: int,
               max_retries: int = 2, base: float = 0.5, cap: float = 8.0) -> float | None:
    """Seconds to wait before retrying, or None for "don't retry".

    Rules from the vendors' pages (Part 13, Section 3.5): retry 408, 409,
    429 and 5xx (529 is Anthropic's "overloaded"); obey retry-after-ms, then
    retry-after; an Anthropic 429 with no retry-after is a spend cap and a
    retry won't succeed. A wait over MAX_WAIT seconds means give up; a value
    that is not a plain number (a date, "-5") is ignored. Otherwise the wait
    doubles from `base` up to `cap` (Part 09 adds jitter; it is left out here
    so the checks are exact).
    """
    h = {k.lower(): v for k, v in headers.items()}
    if attempt >= max_retries:
        return None
    if not (status in (408, 409, 429) or status >= 500):
        return None
    if vendor == "anthropic" and status == 429 and "retry-after" not in h \
            and "retry-after-ms" not in h:
        return None
    for name, scale in (("retry-after-ms", 1000), ("retry-after", 1)):
        value = str(h.get(name, "")).strip()
        if re.fullmatch(r"\d{1,9}(\.\d+)?", value):
            wait = float(value) / scale
            return wait if wait <= MAX_WAIT else None   # a wait that long: give up, don't hang
    return min(cap, base * 2 ** attempt)


# --------------------------------------------- 4. tracing: names and rules
TRACEPARENT = re.compile(r"^([0-9a-f]{2})-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})$")


def parse_traceparent(value: str) -> dict | None:
    """W3C Trace Context `traceparent`: version-traceid-parentid-flags.
    Returns None when invalid (all-zero IDs, version ff, wrong lengths)."""
    m = TRACEPARENT.match(value.strip())
    if not m:
        return None
    version, trace_id, parent_id, flags = m.groups()
    if version == "ff" or set(trace_id) == {"0"} or set(parent_id) == {"0"}:
        return None
    return {"trace_id": trace_id, "parent_id": parent_id,
            "sampled": bool(int(flags, 16) & 1)}


CONTENT_ATTRIBUTES = ("gen_ai.system_instructions", "gen_ai.input.messages",
                      "gen_ai.output.messages", "gen_ai.tool.definitions")


def chat_span(provider: str, model: str, usage: dict, finish_reasons: list[str],
              messages: list | None = None, output: list | None = None,
              capture_content: bool = False) -> tuple[str, dict]:
    """Span name and attributes for one model call, per the OpenTelemetry
    GenAI conventions (status Development, read October 20, 2026).

    gen_ai.usage.input_tokens counts every input token, cached ones included;
    the cache counts are reported separately as well. Prompt and answer text
    are recorded only when capture_content is True (opt-in)."""
    attrs = {
        "gen_ai.operation.name": "chat",
        "gen_ai.provider.name": provider,
        "gen_ai.request.model": model,
        "gen_ai.usage.input_tokens": prompt_tokens(usage),
        "gen_ai.usage.output_tokens": usage.get("output", 0),
        "gen_ai.response.finish_reasons": list(finish_reasons),
    }
    if usage.get("cache_read"):
        attrs["gen_ai.usage.cache_read.input_tokens"] = usage["cache_read"]
    if usage.get("cache_write"):
        attrs["gen_ai.usage.cache_write.input_tokens"] = usage["cache_write"]
    if capture_content:   # structured content goes on spans as a JSON string
        if messages is not None:
            attrs["gen_ai.input.messages"] = json.dumps(messages)
        if output is not None:
            attrs["gen_ai.output.messages"] = json.dumps(output)
    return f"chat {model}", attrs


def drop_content(attrs: dict) -> dict:
    """What a Collector's attributes processor can do before storage:
    remove prompt and answer text from a span's attributes."""
    return {k: v for k, v in attrs.items() if k not in CONTENT_ATTRIBUTES}
