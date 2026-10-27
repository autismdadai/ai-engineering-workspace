"""Connects promptfoo to the lab's stand-in router: no model, no API key.

promptfoo calls route_v1 and route_v2 as "providers" (its name for the system
under test) and create_tests to load the tickets as test cases.
"""
import json
import os
import sys

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, LAB)
from router import route  # noqa: E402  (the import needs the path above)


def route_v1(prompt, options, context):
    return {"output": route(prompt, "v1")}


def route_v2(prompt, options, context):
    return {"output": route(prompt, "v2")}


def create_tests():
    with open(os.path.join(LAB, "data", "tickets.jsonl"), encoding="utf-8") as f:
        rows = [json.loads(line) for line in f if line.strip()]
    return [{"description": row["id"], "vars": {"text": row["text"]},
             "assert": [{"type": "equals", "value": row["label"]}]} for row in rows]
