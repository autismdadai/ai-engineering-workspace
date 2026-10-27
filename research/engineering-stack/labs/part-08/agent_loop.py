"""A minimal, careful agent loop, standard library only.

The model is anything with a .respond(messages, max_tokens) method that returns a
dict shaped like an Anthropic Messages API response:

    {"stop_reason": "tool_use" | "end_turn" | "max_tokens" | "pause_turn" |
                    "refusal" | "stop_sequence" | "model_context_window_exceeded",
     "content": [{"type": "text", "text": ...},
                 {"type": "tool_use", "id": ..., "name": ..., "input": {...}}],
     "usage": {"input_tokens": n, "output_tokens": m}}

In the lab a scripted stand-in plays the model, so every branch can be tested
without a model, an account or a key. The loop:

  - continues only on tool_use, and finishes on end_turn
  - handles every other stop reason explicitly
  - never runs a tool call cut off by max_tokens; asks again with more room
  - validates each call (known tool, required arguments, types) before running it
  - asks an approver before any tool marked high-impact
  - waits for each tool only up to a time limit (a Python thread can't be
    stopped, so a tool that times out may still finish: the loop says so and
    tells the model not to retry; to really stop a tool, run it in a separate
    process)
  - returns failures to the model as is_error results: a ToolError's message,
    written for the model, or a generic message for any other exception, whose
    details go to the developer's log instead (they may hold secrets)
  - sends all results back in one message, results first
  - stops at a turn cap and a token budget
"""
import json
import math
import threading
import traceback
from dataclasses import dataclass, field

KNOWN_STOP_REASONS = {"tool_use", "end_turn", "max_tokens", "pause_turn", "refusal",
                      "stop_sequence", "model_context_window_exceeded"}


class ToolError(Exception):
    """An error whose message is safe and useful to show the model."""


@dataclass
class Tool:
    name: str
    function: callable
    schema: dict
    high_impact: bool = False   # needs a person's approval before it runs
    timeout: float = 2.0        # seconds


@dataclass
class RunResult:
    status: str                 # "done", "max_turns", "budget", "refusal", "context_full",
                                # "stop_sequence", "unknown_stop_reason", "max_tokens"
    turns: int
    final_text: str = ""
    tokens: int = 0
    messages: list = field(default_factory=list)
    tool_log: list = field(default_factory=list)   # (name, outcome) for each call
    errors: list = field(default_factory=list)     # tracebacks, for the developer only


def validate_call(tool, arguments):
    """Return None if the arguments fit the tool's schema, else a short reason."""
    if not isinstance(arguments, dict):
        return "arguments must be a JSON object"
    for name in tool.schema.get("required", []):
        if name not in arguments:
            return f"missing required argument '{name}'"
    properties = tool.schema.get("properties", {})
    types = {"string": str, "integer": int, "number": (int, float), "boolean": bool}
    for name, value in arguments.items():
        if name not in properties:
            return f"unknown argument '{name}'"
        expected = types.get(properties[name].get("type"))
        if expected and (not isinstance(value, expected) or
                         (expected is not bool and isinstance(value, bool))):
            return f"argument '{name}' must be {properties[name]['type']}"
        if isinstance(value, float) and not math.isfinite(value):
            return f"argument '{name}' must be a finite number"
    return None
    # Types only: business rules (no negative refunds, limits) belong in the tool.


def run_with_timeout(function, arguments, seconds):
    """Run function(**arguments) in a thread; raise TimeoutError if it runs too long."""
    box = {}

    def target():
        try:
            box["value"] = function(**arguments)
        except Exception as error:  # reported to the model as a short message
            box["error"] = error

    worker = threading.Thread(target=target, daemon=True)
    worker.start()
    worker.join(seconds)
    if worker.is_alive():
        raise TimeoutError(f"timed out after {seconds:g} seconds")
    if "error" in box:
        raise box["error"]
    return box["value"]


def tool_result(call_id, text, is_error=False):
    block = {"type": "tool_result", "tool_use_id": call_id, "content": text}
    if is_error:
        block["is_error"] = True
    return block


def approved(approver, name, arguments):
    """Only an exact True approves; an approver that fails counts as a no."""
    try:
        return approver(name, arguments) is True
    except Exception:
        return False


def execute(call, tools, approver, log, errors):
    """Run one tool call and return its tool_result block. Never raises."""
    tool = tools.get(call["name"])
    if tool is None:
        log.append((call["name"], "unknown tool"))
        names = ", ".join(sorted(tools))
        return tool_result(call["id"], f"No tool named '{call['name']}'. Available: {names}.", True)
    problem = validate_call(tool, call.get("input"))
    if problem:
        log.append((tool.name, "invalid arguments"))
        return tool_result(call["id"], f"Invalid arguments: {problem}. Fix them and call again.", True)
    if tool.high_impact and not approved(approver, tool.name, call["input"]):
        log.append((tool.name, "denied"))
        return tool_result(call["id"], "A person declined this action. Do not retry it; "
                                       "explain what you would have done instead.", True)
    try:
        value = run_with_timeout(tool.function, call["input"], tool.timeout)
    except TimeoutError as error:
        log.append((tool.name, "timeout, may still finish"))
        return tool_result(call["id"], f"Tool '{tool.name}' {error} and may still finish. Its outcome "
                                       "is unknown: do not call it again; tell the user.", True)
    except ToolError as error:
        log.append((tool.name, "error"))
        return tool_result(call["id"], f"Tool '{tool.name}' failed: {error}", True)
    except Exception as error:
        log.append((tool.name, "error"))
        errors.append((tool.name, traceback.format_exception(error)))
        # The model gets no details: exception text can hold paths, URLs or keys.
        return tool_result(call["id"], f"Tool '{tool.name}' failed with an internal error "
                                       f"({type(error).__name__}). Details were logged.", True)
    log.append((tool.name, "ok"))
    if isinstance(value, str):
        return tool_result(call["id"], value)
    try:
        return tool_result(call["id"], json.dumps(value))
    except (TypeError, ValueError):
        return tool_result(call["id"], str(value))


def deny_all(name, arguments):
    return False


def run_agent(model, tools, task, max_turns=10, token_budget=50_000, max_tokens=1024,
              approver=deny_all):
    """Run the loop until the model finishes or a cap is reached."""
    tools = {tool.name: tool for tool in tools}
    messages = [{"role": "user", "content": task}]
    log, errors, tokens, turns = [], [], 0, 0
    while True:
        if turns >= max_turns:
            return RunResult("max_turns", turns, tokens=tokens, messages=messages, tool_log=log, errors=errors)
        if tokens >= token_budget:
            return RunResult("budget", turns, tokens=tokens, messages=messages, tool_log=log, errors=errors)
        response = model.respond(messages, max_tokens=max_tokens)
        turns += 1
        usage = response.get("usage", {})
        tokens += usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
        reason = response.get("stop_reason")
        content = response.get("content", [])
        text = "".join(b.get("text", "") for b in content if b.get("type") == "text")

        if reason not in KNOWN_STOP_REASONS:
            return RunResult("unknown_stop_reason", turns, text, tokens, messages, log, errors)
        if reason == "max_tokens":
            if any(b.get("type") == "tool_use" for b in content):
                # The last tool call may be cut off: never run it. Ask again with more room,
                # once; the truncated response is discarded, not added to the history.
                if max_tokens >= 4 * 1024:
                    return RunResult("max_tokens", turns, text, tokens, messages, log, errors)
                max_tokens *= 4
                continue
            return RunResult("max_tokens", turns, text, tokens, messages, log, errors)
        messages.append({"role": "assistant", "content": content})
        if reason == "pause_turn":
            continue  # a server-side tool paused; send the response back as it is
        if reason == "end_turn":
            return RunResult("done", turns, text, tokens, messages, log, errors)
        if reason == "refusal":
            return RunResult("refusal", turns, text, tokens, messages, log, errors)
        if reason == "stop_sequence":
            return RunResult("stop_sequence", turns, text, tokens, messages, log, errors)
        if reason == "model_context_window_exceeded":
            return RunResult("context_full", turns, text, tokens, messages, log, errors)

        # tool_use: run every call in order, then send all results back together.
        calls = [b for b in content if b.get("type") == "tool_use"]
        if not calls:
            return RunResult("done", turns, text, tokens, messages, log, errors)
        results = [execute(call, tools, approver, log, errors) for call in calls]
        messages.append({"role": "user", "content": results})


def context_tokens(prefix, per_turn, turns):
    """Input tokens sent on the last turn, and in total, when the whole history is resent."""
    last = prefix + per_turn * (turns - 1)
    total = sum(prefix + per_turn * (n - 1) for n in range(1, turns + 1))
    return last, total
