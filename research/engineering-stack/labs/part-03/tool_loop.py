"""A tool-calling loop driven by a scripted stand-in model.

The program, not the model, runs tools. It checks each call's name and
arguments against the tool's schema before running it, sends errors back
marked is_error, and stops after max_steps. The message shapes follow
Anthropic's tool_use / tool_result blocks in simplified form.
"""
from ticket_contract import validate

ORDERS = {"1182": {"status": "shipped", "carrier": "post"}}

TOOLS = {
    "lookup_order": {
        "description": "Look up an order by its number, e.g. '1182'.",
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"],
            "additionalProperties": False,
        },
        "run": lambda args: ORDERS.get(args["order_id"], {"status": "not found"}),
    },
}

SCRIPT_GOOD = [  # recorded, illustrative turns
    {"type": "tool_use", "id": "t1", "name": "lookup_order", "input": {"order_id": 1182}},
    {"type": "tool_use", "id": "t2", "name": "lookup_order", "input": {"order_id": "1182"}},
    {"type": "text", "text": "Order 1182 has shipped."},
]
SCRIPT_RUNAWAY = [{"type": "tool_use", "id": f"r{i}", "name": "lookup_order",
                   "input": {"order_id": "1182"}} for i in range(10)]


def run_tool(call):
    tool = TOOLS.get(call["name"])
    if tool is None:
        return {"is_error": True, "content": f"unknown tool {call['name']!r}"}
    errors = validate(call["input"], tool["input_schema"], "input")
    if errors:
        return {"is_error": True, "content": "; ".join(errors)}
    return {"is_error": False, "content": tool["run"](call["input"])}


def agent_loop(script, max_steps=5):
    """Return (final_text or None, transcript, reason_stopped)."""
    turns, transcript = list(script), []
    for _ in range(max_steps):
        block = turns.pop(0)
        transcript.append(block)
        if block["type"] == "text":
            return block["text"], transcript, "answered"
        result = run_tool(block)
        transcript.append({"type": "tool_result", "tool_use_id": block["id"], **result})
    return None, transcript, "max_steps"


if __name__ == "__main__":
    for name, script in (("good", SCRIPT_GOOD), ("runaway", SCRIPT_RUNAWAY)):
        text, transcript, reason = agent_loop(script)
        errors = sum(1 for b in transcript if b.get("is_error"))
        print(f"{name}: stopped={reason} answer={text!r} tool_errors={errors} "
              f"blocks={len(transcript)}")
