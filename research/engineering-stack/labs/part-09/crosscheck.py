"""Optional: check the lab's claims against LangGraph itself (Part 09).

Needs: python -m pip install -r requirements-crosscheck.txt
No model, no API key, no account. Network connections are blocked inside
this script, so a check that tried to reach the internet would fail.
Run from this folder: python crosscheck.py
"""
import os
import shutil
import socket
import sqlite3
import sys
import tempfile
import traceback
from typing import TypedDict

os.environ["LANGSMITH_TRACING"] = "false"  # keep any tracing off


def _no_network(*args, **kwargs):
    raise RuntimeError("network blocked by crosscheck.py")


socket.socket.connect = _no_network
socket.create_connection = _no_network

from langgraph.checkpoint.memory import InMemorySaver  # noqa: E402
from langgraph.checkpoint.sqlite import SqliteSaver  # noqa: E402
from langgraph.errors import GraphRecursionError  # noqa: E402
from langgraph.graph import END, START, StateGraph  # noqa: E402
from langgraph.types import Command, RetryPolicy, interrupt  # noqa: E402
import langgraph._internal._config as lg_config  # noqa: E402

CHECKS = []


def check(name):
    def register(fn):
        CHECKS.append((name, fn))
        return fn
    return register


class State(TypedDict, total=False):
    n: int
    answer: str
    second: str


@check("L1 resume re-runs the paused node from its start; earlier nodes don't re-run")
def l1():
    counts = {"before": 0, "ask": 0}

    def before(state):
        counts["before"] += 1
        return {"n": 1}

    def ask(state):
        counts["ask"] += 1  # code before interrupt()
        return {"answer": interrupt("approve?")}

    graph = StateGraph(State)
    graph.add_node("before", before)
    graph.add_node("ask", ask)
    graph.add_edge(START, "before")
    graph.add_edge("before", "ask")
    graph.add_edge("ask", END)
    app = graph.compile(checkpointer=InMemorySaver())
    config = {"configurable": {"thread_id": "t1"}}
    first = app.invoke({"n": 0}, config)
    assert "__interrupt__" in first, first
    result = app.invoke(Command(resume="approve"), config)
    assert result["answer"] == "approve", result
    assert counts == {"before": 1, "ask": 2}, counts


@check("L2 two interrupts in one node get their answers by position")
def l2():
    def ask(state):
        return {"answer": interrupt("first?"), "second": interrupt("second?")}

    graph = StateGraph(State)
    graph.add_node("ask", ask)
    graph.add_edge(START, "ask")
    graph.add_edge("ask", END)
    app = graph.compile(checkpointer=InMemorySaver())
    config = {"configurable": {"thread_id": "t2"}}
    app.invoke({"n": 0}, config)
    app.invoke(Command(resume="A"), config)
    result = app.invoke(Command(resume="B"), config)
    assert (result["answer"], result["second"]) == ("A", "B"), result


@check("L3 the default step limit is 10007 in this version, and a limit raises GraphRecursionError")
def l3():
    assert lg_config.DEFAULT_RECURSION_LIMIT == 10007, lg_config.DEFAULT_RECURSION_LIMIT

    def spin(state):
        return {"n": state.get("n", 0) + 1}

    graph = StateGraph(State)
    graph.add_node("spin", spin)
    graph.add_edge(START, "spin")
    graph.add_conditional_edges("spin", lambda s: END if s["n"] >= 30 else "spin")
    app = graph.compile()
    assert app.invoke({"n": 0})["n"] == 30  # 30 steps: more than the old default of 25
    try:
        app.invoke({"n": 0}, {"recursion_limit": 7})
    except GraphRecursionError as error:
        assert "Recursion limit of 7 reached" in str(error), error
        return
    raise AssertionError("no GraphRecursionError")


@check("L4 RetryPolicy defaults: 0.5 s, factor 2, 128 s cap, 3 attempts, jitter on")
def l4():
    p = RetryPolicy()
    assert (p.initial_interval, p.backoff_factor, p.max_interval, p.max_attempts,
            p.jitter) == (0.5, 2.0, 128.0, 3, True), p


@check("L5 a graph with a checkpointer refuses to run without a thread_id")
def l5():
    graph = StateGraph(State)
    graph.add_node("one", lambda s: {"n": 1})
    graph.add_edge(START, "one")
    graph.add_edge("one", END)
    app = graph.compile(checkpointer=InMemorySaver())
    try:
        app.invoke({"n": 0})
    except ValueError as error:
        assert "thread_id" in str(error), error
        return
    raise AssertionError("ran without a thread_id")


@check("L6 a pause saved in SQLite is resumed through a new connection")
def l6():
    path = os.path.join(tempfile.mkdtemp(prefix="lg09-"), "cp.sqlite")

    def build(conn):
        graph = StateGraph(State)
        graph.add_node("ask", lambda s: {"answer": interrupt("ok?")})
        graph.add_edge(START, "ask")
        graph.add_edge("ask", END)
        return graph.compile(checkpointer=SqliteSaver(conn))

    config = {"configurable": {"thread_id": "t6"}}
    conn = sqlite3.connect(path, check_same_thread=False)
    build(conn).invoke({"n": 0}, config)
    conn.close()  # as if the process had stopped
    conn = sqlite3.connect(path, check_same_thread=False)
    result = build(conn).invoke(Command(resume="yes"), config)
    conn.close()
    shutil.rmtree(os.path.dirname(path), ignore_errors=True)
    assert result["answer"] == "yes", result


def main():
    passed = 0
    for name, fn in CHECKS:
        try:
            fn()
        except Exception:
            detail = traceback.format_exc().strip().splitlines()[-1]
            print(f"FAIL  {name}\n      {detail[:300]}")
        else:
            passed += 1
            print(f"PASS  {name}")
    print(f"\n{passed} of {len(CHECKS)} cross-checks passed")
    return 0 if passed == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())
