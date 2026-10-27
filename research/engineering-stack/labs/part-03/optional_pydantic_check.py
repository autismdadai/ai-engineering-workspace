"""Optional: check that Pydantic agrees with the lab's small validator.

Needs requirements-optional.txt installed. Builds the same contract as a
Pydantic model, prints the JSON Schema Pydantic generates, lints it, and
compares both validators on every recorded reply.
"""
import json
from typing import Literal

from pydantic import BaseModel, ConfigDict, ValidationError

from schema_lint import lint
from ticket_contract import parse_and_validate

REPLIES = [
    '{"queue": "billing", "priority": "urgent", "summary": "Charged twice"}',
    '{"queue": "billing", "priority": "high", "summary": "Charged twice"}',
    '{"queue": "billing", "priority": "urgent"}',
    '{"queue": "billing", "priority": "urgent", "summary": "x", "agent": "ann"}',
    '{"queue": 7, "priority": "urgent", "summary": "x"}',
    '{"queue": "billing", "priority": "urgent", "summary": "x"',
]


class Ticket(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    queue: Literal["billing", "shipping", "account"]
    priority: Literal["low", "normal", "urgent"]
    summary: str


def pydantic_ok(text):
    try:
        Ticket.model_validate_json(text)
        return True
    except ValidationError:
        return False


if __name__ == "__main__":
    schema = Ticket.model_json_schema()
    print("lint:", json.dumps(lint(schema)))
    agree = [pydantic_ok(r) == (not parse_and_validate(r)[1]) for r in REPLIES]
    print(f"agreement: {sum(agree)} of {len(agree)}")
