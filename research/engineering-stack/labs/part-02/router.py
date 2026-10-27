"""Two stand-in ticket routers, so the eval harness can be tested without a model.

A real router would send each support ticket to a language model with a prompt.
These use keyword rules instead: free, instant, and the same answer every run.
v1 is the version in use. v2 is a change under review that tries to catch more
technical tickets by checking technical words first and adding five of them.
"""
LABELS = ["billing", "technical", "account", "other"]

BILLING = ["refund", "charged", "invoice", "payment", "receipt", "subscription",
           "price", "billing", "card", "renew"]
ACCOUNT = ["password", "log in", "login", "sign in", "username", "locked out",
           "two-factor", "email address", "delete my account"]
TECHNICAL = ["error", "crash", "bug", "slow", "freeze", "won't open", "not loading",
             "sync", "upload"]
TECHNICAL_V2 = TECHNICAL + ["app", "page", "screen", "not working", "doesn't work"]

RULES = {
    "v1": [("billing", BILLING), ("account", ACCOUNT), ("technical", TECHNICAL)],
    "v2": [("billing", BILLING), ("technical", TECHNICAL_V2), ("account", ACCOUNT)],
}


def route(text, version="v1"):
    """Return the first label whose keywords appear in the ticket, else "other"."""
    lowered = text.lower()
    for label, keywords in RULES[version]:
        if any(word in lowered for word in keywords):
            return label
    return "other"
