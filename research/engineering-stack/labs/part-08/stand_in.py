"""Scripted stand-ins for a model, and the lab's example tools.

A ScriptedModel returns prepared responses in order, so each test fixes exactly
what "the model" does. It records what it was sent, so tests can check the loop.
Nothing here calls a real model.
"""
import time

from agent_loop import Tool, ToolError


def text(t):
    return {"type": "text", "text": t}


def call(call_id, name, **arguments):
    return {"type": "tool_use", "id": call_id, "name": name, "input": arguments}


def response(stop_reason, *blocks, input_tokens=100, output_tokens=20):
    return {"stop_reason": stop_reason, "content": list(blocks),
            "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens}}


class ScriptedModel:
    def __init__(self, responses):
        self.responses = list(responses)
        self.seen = []          # (messages, max_tokens) for each call
        self.calls = 0

    def respond(self, messages, max_tokens):
        self.seen.append(([dict(m) for m in messages], max_tokens))
        self.calls += 1
        if not self.responses:
            raise RuntimeError("the script ran out of responses")
        item = self.responses.pop(0)
        return item(messages, max_tokens) if callable(item) else item


class LoopingModel:
    """Calls the same tool forever: what a stuck agent looks like."""

    def __init__(self):
        self.calls = 0

    def respond(self, messages, max_tokens):
        self.calls += 1
        return response("tool_use", call(f"c{self.calls}", "list_files"))


# ----- example tools: an invented project folder [I] -----

FILES = {
    "README.md": "Billing service. Run tests with: python -m pytest",
    "billing.py": "def total(items):\n    return sum(items)\n",
    "notes.txt": "Refunds over 100 need a manager.",
}


def list_files():
    return sorted(FILES)


def read_file(path):
    if path not in FILES:
        # A ToolError's message is written for the model: what went wrong, what to do next.
        raise ToolError(f"no file '{path}'; call list_files to see what exists")
    return FILES[path]


def issue_refund(order_id, amount):
    return f"refunded {amount} on order {order_id}"


def slow_report():
    time.sleep(5)
    return "report"


def broken_tool():
    # An unexpected error whose text holds an (invented) key: it must not reach the model.
    raise ValueError("GET https://api.example/v1/report?key=sk-test-0000 returned HTTP 500")


def lab_tools(timeout=1.0):
    return [
        Tool("list_files", list_files, {"type": "object", "properties": {}}),
        Tool("read_file", read_file, {"type": "object", "properties": {"path": {"type": "string"}},
                                      "required": ["path"]}),
        Tool("issue_refund", issue_refund,
             {"type": "object", "properties": {"order_id": {"type": "string"},
                                               "amount": {"type": "number"}},
              "required": ["order_id", "amount"]}, high_impact=True),
        Tool("slow_report", slow_report, {"type": "object", "properties": {}}, timeout=timeout),
        Tool("broken_tool", broken_tool, {"type": "object", "properties": {}}),
    ]
