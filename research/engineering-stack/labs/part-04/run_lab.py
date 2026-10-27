"""Run every Part 04 check. Ends with "N of N checks passed." when all pass.

python run_lab.py                 core checks (standard library only)
python run_lab.py --with-tiktoken also the optional tiktoken comparison
"""
import subprocess
import sys
from fractions import Fraction as F

import cache_cost
import paper_numbers
import placement_test
import token_budget as tb
from cache_sim import Block, OrderError, PromptCache, conversation, cost_units, run

CHECKS = []


def check(func):
    CHECKS.append(func)
    return func


@check
def python_version():
    """Python is 3.11, 3.12 or 3.13 (the series' range)."""
    return (3, 11) <= sys.version_info[:2] <= (3, 13), sys.version.split()[0]


@check
def budget_plan():
    """Must-keep parts stay, the lowest priority goes first, and a margin drops more."""
    parts = [tb.Part("system", 2_000, must_keep=True, order=0),
             tb.Part("a", 400_000, priority=5, order=1),
             tb.Part("b", 300_000, priority=1, order=2),
             tb.Part("c", 250_000, priority=3, order=3),
             tb.Part("question", 200, must_keep=True, order=4)]
    plan = tb.plan_context(parts, 1_000_000, 128_000)
    names = [p.name for p in plan.dropped]
    if names != ["b"] or plan.used > plan.input_budget:
        return False, f"dropped {names}, used {plan.used}"
    tight = [p.name for p in tb.plan_context(parts, 1_000_000, 128_000, growth=1.5).dropped]
    if tight != ["c", "b"]:
        return False, f"with growth 1.5 dropped {tight}"
    try:
        tb.plan_context([tb.Part("huge", 900_000, must_keep=True)], 1_000_000, 128_000)
        return False, "no error when must-keep parts overflow"
    except tb.BudgetError:
        pass
    return True, "kept the must-keep parts; dropped b, then c and b with growth 1.5"


@check
def overflow_rules():
    """Refuse (400), drop the oldest items, or keep system and last (silent)."""
    chat = [("system", 300), ("user", 1_500), ("assistant", 900),
            ("user", 1_200), ("assistant", 700), ("user", 400)]
    e = tb.overflow_error(chat, 4_096)
    d = tb.overflow_drop_oldest(chat, 4_096)
    k = tb.overflow_keep_system_and_last(chat, 4_096)
    ok = (e["status"] == 400 and d["dropped"] == [0, 1] and k["dropped"] == [1]
          and 0 in k["kept"] and 5 in k["kept"] and k["status"] == 200)
    # A last message that alone overflows is still kept (Ollama never drops it).
    one = tb.overflow_keep_system_and_last([("system", 300), ("user", 5_000)], 4_096)
    ok = ok and one["kept"] == [0, 1]
    return ok, f"error {e['status']}; drop-oldest {d['dropped']}; keep-system-and-last {k['dropped']}"


@check
def estimate_is_rough():
    """The estimate never returns 0 for text and is about 4 characters per token."""
    ok = tb.estimate_tokens("a") == 1 and tb.estimate_tokens("x" * 400) == 100 \
        and tb.estimate_tokens("") == 0
    return ok, "1, 100 and 0 tokens for 1, 400 and 0 characters"


@check
def break_even():
    """One read pays back a 1.25x write; a 2x write needs two reads."""
    got = (cache_cost.break_even_reads(F(125, 100), F(1, 10)),
           cache_cost.break_even_reads(F(2), F(1, 10)),
           cache_cost.break_even_reads(F(2), F(1, 40)))
    return got == (1, 2, 2), f"5-minute {got[0]}, 1-hour {got[1]}, 1-hour at 0.025x {got[2]}"


@check
def sonnet_totals():
    """Sonnet 5.5 (base $2 per million, reads 0.05x), 100,000-token prefix."""
    base, read = F(2, 1_000_000), F(1, 20)
    rows = []
    for n in (2, 10):
        rows += [cache_cost.cost_without_cache(100_000, n, base),
                 cache_cost.cost_with_cache(100_000, n, base, F(125, 100), read),
                 cache_cost.cost_with_cache(100_000, n, base, F(2), read)]
    cents = [round(float(x) * 100) for x in rows]
    worst = cache_cost.cost_with_cache(100_000, 10, base, F(125, 100), read, writes=10)
    ok = cents == [40, 26, 41, 200, 34, 49] and worst == F(125, 100) * rows[3]
    return ok, f"cents {cents}; always-expired costs {float(worst / rows[3]):.2f}x"


@check
def gemini_storage():
    """Uses per hour to pay for Gemini explicit-cache storage."""
    u = [round(float(cache_cost.gemini_explicit_uses_per_hour(*r)), 2) for r in
         [(F(75, 100), F(75, 1000), F(50, 100)), (F(2), F(20, 100), F(450, 100)),
          (F(125, 100), F(125, 1000), F(450, 100))]]
    return u == [0.74, 2.5, 4.0], f"{u}"


@check
def cache_stable_prefix():
    """A stable prefix is written once and read on the next two turns."""
    a = run(conversation("You answer questions about the attached document."), [0, 60, 120])
    ok = (a[0]["cache_creation_input_tokens"] == 10_000 and a[0]["cache_read_input_tokens"] == 0
          and all(u["cache_read_input_tokens"] == 10_000 for u in a[1:])
          and all(u["cache_creation_input_tokens"] == 0 for u in a[1:]))
    return ok, f"turns read {[u['cache_read_input_tokens'] for u in a]}"


@check
def cache_timestamp_breaks_it():
    """A changing line at the top means every turn writes and none reads,
    so caching costs more than not caching."""
    stable = "You answer questions about the attached document."
    reqs = [conversation(f"Time now: 09:0{i}. " + stable)[i] for i in range(3)]
    b = run(reqs, [0, 60, 120])
    none = sum(x.tokens for r in reqs for x in r)
    cost = sum(map(cost_units, b))
    ok = all(u["cache_read_input_tokens"] == 0 for u in b) and cost > none
    return ok, f"reads {[u['cache_read_input_tokens'] for u in b]}; cost {cost:,.0f} vs {none:,} uncached"


@check
def cache_lifetime():
    """After 6 minutes a 5-minute entry has expired; a 1-hour entry hasn't.
    A hit refreshes the lifetime."""
    stable = "s"
    c5 = run(conversation(stable, turns=2, ttl=300), [0, 360])
    c60 = run(conversation(stable, turns=2, ttl=3600), [0, 360])
    chain = run(conversation(stable, turns=3, ttl=300), [0, 240, 480])
    ok = (c5[1]["cache_read_input_tokens"] == 0 and c60[1]["cache_read_input_tokens"] == 10_000
          and chain[2]["cache_read_input_tokens"] == 10_000)
    return ok, "5-minute miss at 6 minutes; 1-hour hit; refreshed entry hit at 8 minutes"


@check
def cache_minimum_and_order():
    """Below the minimum nothing is cached and no error is raised; wrong block
    order and a fifth breakpoint are refused."""
    tiny = [[Block("system", "short", 300, breakpoint=True), Block("messages", "hi", 5)]] * 2
    d = run(tiny, [0, 10], minimum=512)
    if any(u["cache_read_input_tokens"] or u["cache_creation_input_tokens"] for u in d):
        return False, "cached a prefix below the minimum"
    cache = PromptCache()
    for bad in ([Block("messages", "m", 10), Block("system", "s", 10)],
                [Block("system", str(i), 300, breakpoint=True) for i in range(5)]):
        try:
            cache.request(bad, 0)
            return False, "accepted a bad request"
        except OrderError:
            pass
    return True, "no caching below 512 tokens; bad order and 5 breakpoints refused"


@check
def placement_harness():
    """The harness finds the built-in U-shape and finds none in the flat stand-in,
    on five different seeds each."""
    u = [placement_test.verdict(placement_test.run_test(placement_test.StandInU(seed=s),
                                                        trials=200, seed=s))[0] for s in range(5)]
    f = [placement_test.verdict(placement_test.run_test(placement_test.StandInFlat(seed=s),
                                                        trials=200, seed=s))[0] for s in range(5)]
    ok = all(v == "U-shaped" for v in u) and all(v == "no clear position effect" for v in f)
    # 10 trials per position: a 20-point gap whose intervals overlap is not enough.
    small = {0: (9, 10), 4: (7, 10), 9: (7, 10), 14: (7, 10), 19: (9, 10)}
    ok = ok and placement_test.verdict(small)[0] == "no clear position effect"
    return ok, f"U stand-in: {u.count('U-shaped')}/5 U-shaped; flat: {f.count('U-shaped')}/5 U-shaped"


@check
def quoted_numbers():
    """Numbers quoted in Part 04 re-derive from their sources' figures."""
    liu = paper_numbers.liu_checks()
    ok = (liu["edge_minus_worst_middle"] == 22.0 and liu["middle_positions_below_closed_book"] == [10, 15]
          and paper_numbers.nolima_share() == 70.2 and paper_numbers.astra_adds_up()
          and paper_numbers.effective_input_per_minute() == 10_000_000
          and paper_numbers.lumer_table_lows_below_abstract())
    return ok, (f"Liu gap {liu['edge_minus_worst_middle']} points; NoLiMa "
                f"{paper_numbers.nolima_share()}%; 10,000,000 tokens per minute")


def optional(script, needle):
    r = subprocess.run([sys.executable, script], capture_output=True, text=True, timeout=300)
    text = r.stdout + r.stderr
    return r.returncode == 0 and needle in text, text.strip().splitlines()[-1] if text.strip() else "no output"


def main():
    def tiktoken_counts():
        return optional("optional_tiktoken_check.py", "PASS")

    if "--with-tiktoken" in sys.argv:
        CHECKS.append(tiktoken_counts)
    passed = 0
    for number, func in enumerate(CHECKS, 1):
        try:
            ok, detail = func()
        except Exception as error:  # a crash counts as a failed check
            ok, detail = False, f"{type(error).__name__}: {error}"
        print(f"[{'PASS' if ok else 'FAIL'}] check {number}: {func.__name__}: {detail}")
        passed += ok
    print(f"{passed} of {len(CHECKS)} checks passed.")
    sys.exit(0 if passed == len(CHECKS) else 1)


if __name__ == "__main__":
    main()
