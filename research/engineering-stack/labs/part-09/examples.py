"""Stand-in services and an example refund workflow (Part 09 lab).

Everything here is invented for teaching: the orders, the payment service
and the "models" are scripted, and nothing leaves this computer.
"""
from workflow import END, RetryPolicy, TransientError, Workflow, approved


class FakePaymentService:
    """A payment service that can lose its reply after charging.

    With lose_reply_times = n, the first n charge calls succeed on the
    service's side but raise TransientError (a timeout) to the caller. Like
    real payment APIs, it remembers idempotency keys: a repeated key returns
    the first result instead of charging again.
    """

    def __init__(self, lose_reply_times=0):
        self.charges = []
        self.keys = {}
        self.lose_reply_times = lose_reply_times

    def refund(self, order, amount, idempotency_key=None):
        if idempotency_key is not None and idempotency_key in self.keys:
            first = self.keys[idempotency_key]
            if first["order"] != order or first["amount"] != amount:
                raise ValueError("idempotency key reused with different parameters")
            return first["id"]
        refund_id = f"rf_{len(self.charges) + 1}"
        self.charges.append({"order": order, "amount": amount, "id": refund_id})
        if idempotency_key is not None:
            self.keys[idempotency_key] = {"order": order, "amount": amount, "id": refund_id}
        if self.lose_reply_times > 0:
            self.lose_reply_times -= 1
            raise TransientError("timeout: the reply was lost")
        return refund_id


def route(text):
    """Routing: easy requests to a small model, hard ones to a larger one."""
    hard = ("legal", "chargeback", "fraud", "complaint")
    return "large-model" if any(word in text.lower() for word in hard) else "small-model"


def build_refund_workflow(payments, counters, use_key=True, max_drafts=3,
                          review_passes_on=2):
    """Classify, draft and review (in a loop), ask a person, then refund.

    counters records how often each step's code ran, so a check can see
    what ran again after a pause, a crash or a retry.
    """
    flow = Workflow()

    def classify(state, ctx):
        counters["classify"] = counters.get("classify", 0) + 1
        return {"model": route(state["request"])}

    def draft(state, ctx):
        counters["draft"] = counters.get("draft", 0) + 1
        n = state.get("drafts", 0) + 1
        return {"drafts": n, "reply": f"Draft {n}: refund {state['amount']} for {state['order']}"}

    def review(state, ctx):
        counters["review"] = counters.get("review", 0) + 1
        return {"review_ok": state["drafts"] >= review_passes_on}

    def after_review(state):
        if state["review_ok"]:
            return "approve"
        if state["drafts"] >= max_drafts:
            return END  # give up: the iteration cap, not a quality score, ends the loop
        return "draft"

    def approve(state, ctx):
        counters["notify"] = counters.get("notify", 0) + 1  # runs again on resume
        answer = ctx.interrupt({"action": "refund", "order": state["order"],
                                "amount": state["amount"]})
        return {"approved": approved(answer), "approver": str(answer.get("by", ""))
                if isinstance(answer, dict) else ""}

    def refund(state, ctx):
        counters["refund"] = counters.get("refund", 0) + 1
        key = f"refund-{state['order']}" if use_key else None
        return {"refund_id": payments.refund(state["order"], state["amount"], key)}

    flow.add_node("classify", classify)
    flow.add_node("draft", draft)
    flow.add_node("review", review)
    flow.add_node("approve", approve)
    flow.add_node("refund", refund,
                  retry=RetryPolicy(max_attempts=3, initial=0.5, factor=2.0, cap=8.0))
    flow.add_edge("classify", "draft")
    flow.add_edge("draft", "review")
    flow.add_router("review", after_review)
    flow.add_router("approve", lambda s: "refund" if s["approved"] else END)
    flow.add_edge("refund", END)
    return flow
