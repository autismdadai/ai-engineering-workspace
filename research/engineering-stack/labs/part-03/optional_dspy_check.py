"""Optional: compile a tiny DSPy program offline with DSPy's DummyLM.

Needs requirements-dspy.txt (about 400 MB). DummyLM returns scripted
answers, so no model, key or network is needed; the scores mean nothing.
What it shows is the mechanics: an optimizer runs the program on training
examples, keeps the runs the metric accepts, and stores them as demos.
"""
import os

os.environ.setdefault("LITELLM_LOCAL_MODEL_COST_MAP", "true")  # no price-list fetch

import dspy  # noqa: E402
from dspy.utils.dummies import DummyLM  # noqa: E402


class Route(dspy.Signature):
    """Route a support ticket to a queue."""
    ticket: str = dspy.InputField()
    queue: str = dspy.OutputField(desc="billing, shipping or account")


ANSWERS = {  # keyed by text that appears in the prompt
    "charged twice": {"queue": "billing"},
    "package lost": {"queue": "shipping"},
    "forgot password": {"queue": "billing"},  # a wrong answer, on purpose
}

TRAIN = [dspy.Example(ticket=t, queue=q).with_inputs("ticket") for t, q in
         [("charged twice", "billing"), ("package lost", "shipping"),
          ("forgot password", "account")]]


def metric(example, prediction, trace=None):
    return example.queue == prediction.queue


if __name__ == "__main__":
    dspy.configure(lm=DummyLM(ANSWERS))
    optimizer = dspy.BootstrapFewShot(metric=metric, max_bootstrapped_demos=3,
                                      max_labeled_demos=0, max_rounds=1)
    compiled = optimizer.compile(dspy.Predict(Route), trainset=TRAIN)
    kept = sorted(d.ticket for d in compiled.demos)
    print(f"dspy {dspy.__version__}: kept {len(kept)} of {len(TRAIN)} as demos: {kept}")
