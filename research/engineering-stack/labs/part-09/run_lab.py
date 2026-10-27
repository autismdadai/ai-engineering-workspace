"""Checks for the Part 09 lab. Run from this folder: python run_lab.py

Standard library only. Each check prints PASS or FAIL; a check that crashes
counts as a FAIL. Exit code 0 only when every check passes.
"""
import ast
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import traceback

import multi_agent as ma
from examples import FakePaymentService, build_refund_workflow, route
from workflow import (END, Context, FileCheckpointer, IdempotencyError,
                      IdempotencyStore, RetryPolicy, StateTamperedError,
                      StepLimitError, TransientError, Workflow, approved)

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = []
TEMP = []  # folders made by the checks, removed at the end
START = {"order": "A17", "amount": 250, "request": "Refund please, item arrived broken"}


def check(name):
    def register(fn):
        CHECKS.append((name, fn))
        return fn
    return register


def temp_folder(prefix):
    folder = tempfile.mkdtemp(prefix=prefix)
    TEMP.append(folder)
    return folder


def no_sleep(seconds):
    pass


def fresh():
    folder = temp_folder("lab09-")
    return folder, FileCheckpointer(os.path.join(folder, "cp"))


def refund_flow(**kwargs):
    payments = FakePaymentService(kwargs.pop("lose_reply_times", 0))
    counters = {}
    return build_refund_workflow(payments, counters, **kwargs), payments, counters


@check("1 a refund run pauses for approval, then finishes with one refund")
def c1():
    flow, pay, n = refund_flow()
    _, cp_store = fresh()
    cp = flow.run("t1", cp_store, state=START, sleep=no_sleep)
    assert cp["status"] == "interrupted", cp["status"]
    cp = flow.run("t1", cp_store, resume={"decision": "approve", "by": "manager"},
                  sleep=no_sleep)
    assert cp["status"] == "done" and cp["state"]["refund_id"] == "rf_1", cp
    assert len(pay.charges) == 1 and cp["state"]["drafts"] == 2, (pay.charges, cp)


@check("1b routing sends hard requests to the larger model")
def c1b():
    assert route("I will file a chargeback") == "large-model"
    assert route("Refund please") == "small-model"


@check("2 the pause carries what the person must decide")
def c2():
    flow, pay, n = refund_flow()
    _, cp_store = fresh()
    cp = flow.run("t1", cp_store, state=START, sleep=no_sleep)
    pending = cp["pending"]
    assert pending["step"] == "approve" and pending["value"]["amount"] == 250, pending
    assert n["notify"] == 1 and not pay.charges, (n, pay.charges)


@check("2b resuming re-runs the paused step from its start, and only that step")
def c2b():
    flow, pay, n = refund_flow()
    _, cp_store = fresh()
    flow.run("t1", cp_store, state=START, sleep=no_sleep)
    flow.run("t1", cp_store, resume={"decision": "approve"}, sleep=no_sleep)
    assert n["notify"] == 2, n  # code before interrupt() ran twice
    assert n["classify"] == 1 and n["draft"] == 2 and n["review"] == 2, n


@check("2c a rejection ends the run with no refund")
def c2c():
    flow, pay, n = refund_flow()
    _, cp_store = fresh()
    flow.run("t1", cp_store, state=START, sleep=no_sleep)
    cp = flow.run("t1", cp_store, resume={"decision": "reject"}, sleep=no_sleep)
    assert cp["status"] == "done" and not cp["state"]["approved"], cp
    assert not pay.charges and "refund" not in n, (pay.charges, n)


@check("2d only an explicit approval approves (it fails closed)")
def c2d():
    for answer in ("yes", "approve", {"decision": "Approve"}, {"approved": True},
                   {"decision": ["approve"]}, 1, True):
        assert not approved(answer), answer
    assert approved({"decision": "approve"})
    flow, pay, n = refund_flow()
    _, cp_store = fresh()
    flow.run("t1", cp_store, state=START, sleep=no_sleep)
    cp = flow.run("t1", cp_store, resume="yes", sleep=no_sleep)
    assert cp["status"] == "done" and not pay.charges, (cp, pay.charges)


@check("2e two pauses in one step get their answers by position")
def c2e():
    seen = []

    def two_questions(state, ctx):
        first = ctx.interrupt("amount?")
        second = ctx.interrupt("reason?")
        seen.append((first, second))
        return {"amount": first, "reason": second}

    flow = Workflow()
    flow.add_node("ask", two_questions)
    flow.add_node("confirm", lambda s, ctx: {"confirmed": ctx.interrupt("confirm?")})
    flow.add_edge("ask", "confirm")
    _, cp_store = fresh()
    cp = flow.run("t2", cp_store, state={}, sleep=no_sleep)
    assert cp["pending"]["index"] == 0, cp
    cp = flow.run("t2", cp_store, resume=40, sleep=no_sleep)
    assert cp["pending"]["index"] == 1 and cp["pending"]["value"] == "reason?", cp
    cp = flow.run("t2", cp_store, resume="damaged", sleep=no_sleep)
    assert cp["pending"]["step"] == "confirm" and cp["pending"]["index"] == 0, cp
    assert cp["state"] == {"amount": 40, "reason": "damaged"} and seen == [(40, "damaged")], cp
    cp = flow.run("t2", cp_store, resume=True, sleep=no_sleep)  # a new step starts with no answers
    assert cp["status"] == "done" and cp["state"]["confirmed"] is True, cp


@check("2f misuse is refused: no answer for a pause, an answer with no pause, a reused id")
def c2f():
    flow, pay, n = refund_flow()
    _, cp_store = fresh()
    flow.run("t1", cp_store, state=START, sleep=no_sleep)
    for kwargs in ({}, {"state": START}):
        try:
            flow.run("t1", cp_store, sleep=no_sleep, **kwargs)
        except ValueError:
            continue
        raise AssertionError(f"accepted {kwargs}")
    flow.run("t1", cp_store, resume={"decision": "approve"}, sleep=no_sleep)
    cp = flow.run("t1", cp_store, sleep=no_sleep)  # finished: returned as is
    assert cp["status"] == "done"
    try:
        flow.run("t1", cp_store, state=START, sleep=no_sleep)  # same id, new run
    except ValueError:
        pass
    else:
        raise AssertionError("restarted a finished thread under the same id")
    try:
        flow.run("missing", cp_store, sleep=no_sleep)
    except ValueError:
        return
    raise AssertionError("ran a thread that doesn't exist")


@check("3 a process killed mid-step is continued by a new process from its checkpoint")
def c3():
    folder = temp_folder("lab09-crash-")
    script = os.path.join(HERE, "crash_run.py")
    first = subprocess.run([sys.executable, script, folder, "crash"],
                           capture_output=True, text=True, timeout=60, cwd=HERE)
    assert first.returncode == 9, (first.returncode, first.stderr)
    with open(os.path.join(folder, "checkpoints", "t1.json"), encoding="utf-8") as h:
        saved = json.loads(json.load(h)["checkpoint"])
    assert saved["node"] == "review" and saved["step"] == 2, saved
    second = subprocess.run([sys.executable, script, folder, "resume"],
                            capture_output=True, text=True, timeout=60, cwd=HERE)
    assert second.returncode == 0, second.stderr
    result = json.loads(second.stdout)
    assert result["status"] == "interrupted", result
    with open(os.path.join(folder, "counts.json"), encoding="utf-8") as h:
        counts = json.load(h)
    # classify and the first draft were not repeated; the killed review was
    assert counts["classify"] == 1 and counts["draft"] == 2, counts
    assert counts["review"] == 3, counts


@check("4 a loop with no way out stops at the step limit")
def c4():
    flow = Workflow()
    flow.add_node("spin", lambda s, ctx: {"n": s.get("n", 0) + 1})
    flow.add_router("spin", lambda s: "spin")
    _, cp_store = fresh()
    try:
        flow.run("t4", cp_store, state={}, step_limit=7, sleep=no_sleep)
    except StepLimitError as error:
        assert "7" in str(error)
        assert cp_store.load("t4")["state"]["n"] == 7
        return
    raise AssertionError("no StepLimitError")


@check("4b the draft-and-review loop ends at its cap when the review never passes")
def c4b():
    flow, pay, n = refund_flow(review_passes_on=99, max_drafts=3)
    _, cp_store = fresh()
    cp = flow.run("t1", cp_store, state=START, sleep=no_sleep)
    assert cp["status"] == "done" and cp["state"]["drafts"] == 3, cp
    assert "notify" not in n and not pay.charges, n


@check("5 retries wait with full jitter, within the cap, then give up")
def c5():
    waits = []
    policy = RetryPolicy(max_attempts=4, initial=0.5, factor=2.0, cap=1.5)

    def always_fails(state, ctx):
        raise TransientError("503")

    flow = Workflow()
    flow.add_node("call", always_fails, retry=policy)
    _, cp_store = fresh()
    try:
        flow.run("t5", cp_store, state={}, sleep=waits.append, rng=random.Random(7))
    except TransientError:
        pass
    else:
        raise AssertionError("no error after the last attempt")
    assert len(waits) == 3, waits
    for n, wait in enumerate(waits):
        assert 0 <= wait <= min(1.5, 0.5 * 2 ** n), (n, wait)
    rng = random.Random(7)
    assert waits == [policy.delay(i, rng) for i in range(3)], waits  # seeded, repeatable

    class Highest:  # a stand-in random source that always picks the top
        def uniform(self, low, high):
            return high

    tops = [policy.delay(i, Highest()) for i in range(5)]
    assert tops == [0.5, 1.0, 1.5, 1.5, 1.5], tops  # doubles, then held at the cap
    assert len(cp_store.load("t5")["log"]) == 0  # failed step: no checkpoint past start


@check("5b an error that isn't transient is not retried")
def c5b():
    calls = []

    def bad_input(state, ctx):
        calls.append(1)
        raise ValueError("amount must be positive")

    flow = Workflow()
    flow.add_node("call", bad_input, retry=RetryPolicy(max_attempts=5))
    _, cp_store = fresh()
    try:
        flow.run("t5b", cp_store, state={}, sleep=no_sleep)
    except ValueError:
        assert len(calls) == 1, calls
        return
    raise AssertionError("no ValueError")


@check("5c a pause is not a failure: it is never retried")
def c5c():
    calls = []

    def asks(state, ctx):
        calls.append(1)
        return {"ok": ctx.interrupt("ok?")}

    flow = Workflow()
    flow.add_node("ask", asks, retry=RetryPolicy(max_attempts=5, retry_on=(Exception,)))
    _, cp_store = fresh()
    cp = flow.run("t5c", cp_store, state={}, sleep=no_sleep)
    assert cp["status"] == "interrupted" and len(calls) == 1 and cp["log"] == [], cp


@check("5d a retried step starts over, so an answered pause gets the same answer")
def c5d():
    calls = []

    def ask_then_flaky(state, ctx):
        answer = ctx.interrupt("go ahead?")
        calls.append(answer)
        if len(calls) == 1:
            raise TransientError("timeout")
        return {"answer": answer}

    flow = Workflow()
    flow.add_node("ask", ask_then_flaky, retry=RetryPolicy(max_attempts=3))
    _, cp_store = fresh()
    flow.run("t5d", cp_store, state={}, sleep=no_sleep)
    cp = flow.run("t5d", cp_store, resume="yes", sleep=no_sleep)
    assert cp["status"] == "done" and calls == ["yes", "yes"], (cp, calls)


@check("6 a lost reply plus a retry pays twice without a key, once with one")
def c6():
    results = {}
    for use_key in (False, True):
        flow, pay, n = refund_flow(use_key=use_key, lose_reply_times=1)
        _, cp_store = fresh()
        flow.run("t6", cp_store, state=START, sleep=no_sleep)
        cp = flow.run("t6", cp_store, resume={"decision": "approve"}, sleep=no_sleep)
        assert cp["status"] == "done" and n["refund"] == 2, (cp, n)
        results[use_key] = len(pay.charges)
    assert results == {False: 2, True: 1}, results


@check("6b the payment service refuses a key reused with different parameters")
def c6b():
    pay = FakePaymentService()
    assert pay.refund("A17", 250, "k1") == pay.refund("A17", 250, "k1") == "rf_1"
    try:
        pay.refund("A17", 999, "k1")
    except ValueError:
        assert len(pay.charges) == 1
        return
    raise AssertionError("accepted a reused key")


@check("6c the idempotency store runs an effect once per key, across restarts")
def c6c():
    folder = temp_folder("lab09-idem-")
    path = os.path.join(folder, "keys.json")
    sent = []

    def send_email(to, body):
        sent.append(to)
        return f"msg-{len(sent)}"

    first = IdempotencyStore(path).run("email-A17", {"to": "a@example.com", "body": "Hi"}, send_email)
    again = IdempotencyStore(path).run("email-A17", {"to": "a@example.com", "body": "Hi"}, send_email)
    assert first == again == "msg-1" and sent == ["a@example.com"], (first, again, sent)
    try:
        IdempotencyStore(path).run("email-A17", {"to": "b@example.com", "body": "Hi"}, send_email)
    except IdempotencyError:
        return
    raise AssertionError("accepted a reused key with new parameters")


@check("6d its limit: a crash after the effect but before the record repeats the effect")
def c6d():
    folder = temp_folder("lab09-idem2-")
    store = IdempotencyStore(os.path.join(folder, "keys.json"))
    sent = []

    class Crash(Exception):
        pass

    def send_then_die(to):
        sent.append(to)
        raise Crash("process died after sending")

    try:
        store.run("k", {"to": "a@example.com"}, send_then_die)
    except Crash:
        pass
    store.run("k", {"to": "a@example.com"}, lambda to: sent.append(to) or "ok")
    assert sent == ["a@example.com", "a@example.com"], sent


@check("7 a signed checkpoint that was edited is refused")
def c7():
    folder = temp_folder("lab09-sig-")
    store = FileCheckpointer(folder, secret="lab-only-secret")
    flow, pay, n = refund_flow()
    flow.run("t7", store, state=START, sleep=no_sleep)
    path = os.path.join(folder, "t7.json")
    with open(path, encoding="utf-8") as h:
        record = json.load(h)
    record["checkpoint"] = record["checkpoint"].replace('"amount": 250', '"amount": 25000')
    with open(path, "w", encoding="utf-8") as h:
        json.dump(record, h)
    try:
        flow.run("t7", store, resume={"decision": "approve"}, sleep=no_sleep)
    except StateTamperedError:
        assert not pay.charges
    else:
        raise AssertionError("ran an edited checkpoint")
    unsigned = FileCheckpointer(folder)  # no secret: the same edit loads quietly
    assert unsigned.load("t7")["state"]["amount"] == 25000
    del record["signature"]
    with open(path, "w", encoding="utf-8") as h:
        json.dump(record, h)
    try:
        store.load("t7")
    except StateTamperedError:
        return
    raise AssertionError("accepted a checkpoint with no signature")


@check("7b thread ids can't reach outside the checkpoint folder")
def c7b():
    _, cp_store = fresh()
    for bad in ("../escape", "a/b", "", "x" * 65, None, "t1.json"):
        try:
            cp_store.load(bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted {bad!r}")


@check("8 a checkpoint is saved after every step, with no temporary files left")
def c8():
    saves = []

    class Recorder(FileCheckpointer):
        def save(self, thread_id, checkpoint):
            saves.append((checkpoint["node"], checkpoint["step"]))
            super().save(thread_id, checkpoint)

    folder = temp_folder("lab09-rec-")
    flow, pay, n = refund_flow()
    flow.run("t8", Recorder(folder), state=START, sleep=no_sleep)
    steps = [step for _, step in saves]
    assert steps == [0, 1, 2, 3, 4, 5, 5], saves  # start, 5 steps, then the pause
    assert saves[-1][0] == "approve"
    assert not [f for f in os.listdir(folder) if f.endswith(".tmp")]


@check("8b the engine uses only the standard library")
def c8b():
    allowed = {"hashlib", "hmac", "json", "os", "random", "re", "time"}
    for name in ("workflow.py", "multi_agent.py"):
        with open(os.path.join(HERE, name), encoding="utf-8") as h:
            tree = ast.parse(h.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                found = {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                found = {node.module.split(".")[0]}
            else:
                continue
            assert found <= allowed, (name, found)


@check("9 a handoff passes the whole history; an agent-as-tool gets only a brief")
def c9():
    history = []
    sizes = []
    for turn in range(1, 6):
        history.append({"role": "user", "text": f"question {turn} " + "word " * 40})
        history.append({"role": "assistant", "text": "answer " * 30})
        sizes.append((ma.words(ma.handoff_input(history, "You handle billing.")),
                      ma.words(ma.as_tool_input("Check order A17's refund rule.",
                                                "You handle billing."))))
    handoff, tool = zip(*sizes)
    assert list(handoff) == sorted(handoff) and handoff[-1] > 4 * handoff[0], handoff
    assert len(set(tool)) == 1 and tool[0] < handoff[0], tool


@check("9b dropping tool messages doesn't remove tool output already quoted")
def c9b():
    history = [{"role": "tool", "text": "balance: 9,120"},
               {"role": "assistant", "text": "The tool said balance: 9,120"}]
    kept = ma.remove_tool_messages(history)
    assert len(kept) == 1 and "9,120" in kept[0]["text"], kept


@check("10 a subagent reads a lot; its parent gets only the summary")
def c10():
    docs = [("lorem ipsum " * 500).strip() for _ in range(4)]
    summary, read = ma.run_subagent("Summarise the four files", docs, summary_words=12)
    assert read == 4 + 4 * 1000 and len(summary.split()) == 13, (read, summary)


@check("10b orchestrator arithmetic: 3 workers each reading 20,000 tokens")
def c10b():
    assert ma.orchestrator_cost(3, 20_000, 1_000, 300) == (63_900, 3_900, 60_000)


@check("11 errors compound: five 95% steps succeed together about 77% of the time")
def c11():
    assert abs(ma.chain_success(0.95, 5) - 0.7738) < 1e-4
    assert ma.chain_success(0.99, 1) == 0.99


@check("12 extra voters help only when their mistakes are independent")
def c12():
    single = ma.majority_vote_accuracy(0.6, 1, 0.0, 20_000, seed=1)
    independent = ma.majority_vote_accuracy(0.6, 5, 0.0, 20_000, seed=1)
    correlated = ma.majority_vote_accuracy(0.6, 5, 1.0, 20_000, seed=1)
    assert abs(single - 0.6) < 0.015, single
    assert independent - single > 0.05, (single, independent)  # about 0.68 in theory
    assert abs(correlated - single) < 0.015, (single, correlated)
    two = ma.majority_vote_accuracy(0.5, 2, 0.0, 20_000, seed=1)
    assert abs(two - 0.25) < 0.015, two  # a 1-1 tie is not a majority


@check("13 text passed between agents arrives either way; tagging marks it as data")
def c13():
    plain = ma.pass_along("MARKER-123", agents=3)
    tagged = ma.pass_along("MARKER-123", agents=3, tag=True)
    assert "MARKER-123" in plain and "MARKER-123" in tagged
    assert "<data" not in plain and tagged.count("<data from=") == 3, tagged


def main():
    passed = 0
    for name, fn in CHECKS:
        try:
            fn()
        except Exception:  # every crash is a FAIL line, never a stack dump
            detail = traceback.format_exc().strip().splitlines()[-1]
            print(f"FAIL  {name}\n      {detail[:300]}")
        else:
            passed += 1
            print(f"PASS  {name}")
    for folder in TEMP:
        shutil.rmtree(folder, ignore_errors=True)
    print(f"\n{passed} of {len(CHECKS)} checks passed")
    return 0 if passed == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())
