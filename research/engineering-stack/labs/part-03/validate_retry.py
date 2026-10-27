"""Validate a model's JSON and retry with the error, using a scripted stand-in.

The stand-in model returns recorded replies in order. No real model,
network or API key is involved; the replies are illustrative.
"""
from ticket_contract import parse_and_validate

RECORDED_REPLIES = [
    '{"queue": "billing", "priority": "high", "summary": "Charged twice"}',
    '{"queue": "billing", "priority": "urgent", "summary": "Charged twice"}',
]


class StandInModel:
    """Returns recorded replies one at a time and logs every prompt."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.prompts = []

    def complete(self, prompt):
        self.prompts.append(prompt)
        return self.replies.pop(0)


def route_ticket(model, ticket, max_attempts=3):
    """Ask, validate, and on failure ask again with the errors attached."""
    prompt = f"Route this ticket as JSON (queue, priority, summary): {ticket}"
    for attempt in range(1, max_attempts + 1):
        reply = model.complete(prompt)
        data, errors = parse_and_validate(reply)
        if not errors:
            return {"ok": True, "attempts": attempt, "data": data}
        prompt = (f"{prompt}\nYour last reply was invalid: {'; '.join(errors)}"
                  "\nReply again with corrected JSON only.")
    return {"ok": False, "attempts": max_attempts, "errors": errors}


if __name__ == "__main__":
    model = StandInModel(RECORDED_REPLIES)
    result = route_ticket(model, "I was charged twice for order 1182")
    print(result)
    print("Second prompt sent:", model.prompts[-1].splitlines()[-2])
