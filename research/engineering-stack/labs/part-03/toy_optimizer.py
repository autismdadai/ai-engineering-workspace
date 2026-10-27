"""A toy prompt optimizer: search instructions and examples against a metric.

Everything here is illustrative. The "model" is a keyword matcher that reads
hints from the prompt: each instruction carries some hints, and each chosen
example (demo) adds its own. The optimizer tries every candidate prompt,
scores it on a validation set, and keeps the best. Real optimizers (DSPy's
MIPROv2, GEPA) use a real model and smarter search, but face the same risk
shown here: a small validation set can pick a prompt that does worse on new
data.
"""
from itertools import combinations

INSTRUCTIONS = {
    "plain": {},
    "money-vs-delivery": {"charge": "billing", "refund": "billing",
                          "deliver": "shipping", "package": "shipping"},
    "three-queues": {"charge": "billing", "refund": "billing",
                     "deliver": "shipping", "package": "shipping",
                     "password": "account", "login": "account"},
}
DEMOS = {  # example ticket -> (hint word it teaches, label)
    "my order was billed twice": ("order", "billing"),
    "tracking says delayed": ("tracking", "shipping"),
    "invoice shows wrong amount": ("invoice", "billing"),
    "box arrived damaged": ("arrived", "shipping"),
}
DEFAULT = "account"

TRAIN = [("charged twice", "billing"), ("package lost", "shipping"),
         ("forgot password", "account"), ("refund please", "billing")]
SMALL_VAL = [("order 55 invoice wrong", "billing"), ("order total doubled", "billing"),
             ("login broken", "account"), ("package late", "shipping"),
             ("order billed wrong", "billing")]
BIG_VAL = SMALL_VAL + [("where is my order", "shipping"), ("order never arrived", "shipping"),
                       ("invoice copy needed", "billing"), ("order tracking stuck", "shipping"),
                       ("cancel my order delivery", "shipping"), ("refund for order", "billing"),
                       ("change my email", "account"), ("order arrived broken", "shipping"),
                       ("double charge", "billing"), ("order not delivered", "shipping")]
TEST = [("my order has not arrived", "shipping"), ("order stuck in tracking", "shipping"),
        ("invoice is missing", "billing"), ("order delivered to wrong address", "shipping"),
        ("refund my order", "billing"), ("cannot login", "account"),
        ("order 9 charged twice", "billing"), ("where did my order go", "shipping"),
        ("package crushed", "shipping"), ("reset password", "account"),
        ("order delayed again", "shipping"), ("billing invoice error", "billing")]


def stand_in_model(prompt, ticket):
    """Label a ticket from the prompt's hints: examples first, then instruction."""
    text = ticket.lower()
    for word, label in prompt["demo_hints"] + list(prompt["instruction_hints"].items()):
        if word in text:
            return label
    return DEFAULT


def accuracy(prompt, data):
    return sum(stand_in_model(prompt, t) == y for t, y in data) / len(data)


def candidates(max_demos=2):
    for name, hints in INSTRUCTIONS.items():
        for k in range(max_demos + 1):
            for demos in combinations(DEMOS, k):
                yield {"instruction": name, "instruction_hints": hints,
                       "demos": demos, "demo_hints": [DEMOS[d] for d in demos]}


def optimize(valset):
    """Exhaustive search; ties keep the first (simplest) candidate found."""
    best, best_score, tried = None, -1.0, 0
    for prompt in candidates():
        tried += 1
        score = accuracy(prompt, valset)
        if score > best_score:
            best, best_score = prompt, score
    return best, best_score, tried


def report():
    rows = {}
    for name, valset in (("small_val", SMALL_VAL), ("big_val", BIG_VAL)):
        best, score, tried = optimize(valset)
        rows[name] = {"instruction": best["instruction"], "demos": list(best["demos"]),
                      "val": round(score, 3), "test": round(accuracy(best, TEST), 3),
                      "tried": tried, "model_calls": tried * len(valset)}
    return rows


if __name__ == "__main__":
    for name, row in report().items():
        print(name, row)
