"""Run the refund workflow in its own process, optionally dying mid-step.

Used by check 3 of run_lab.py: one process starts a thread and is killed
inside the "review" step; a second process continues the same thread from
its checkpoint. Step counts are kept in a file so both processes add to them.

Usage: python crash_run.py FOLDER start|crash|resume
"""
import json
import os
import sys

from examples import FakePaymentService, build_refund_workflow
from workflow import FileCheckpointer

folder, mode = sys.argv[1], sys.argv[2]
counts_path = os.path.join(folder, "counts.json")
counters = {}
if os.path.exists(counts_path):
    with open(counts_path, encoding="utf-8") as handle:
        counters = json.load(handle)

flow = build_refund_workflow(FakePaymentService(), counters)
if mode == "crash":
    real_review = flow.nodes["review"]

    def dying_review(state, ctx):
        real_review(state, ctx)
        with open(counts_path, "w", encoding="utf-8") as handle:
            json.dump(counters, handle)
        os._exit(9)  # the process dies here, mid-step, as in a power cut

    flow.nodes["review"] = dying_review

checkpointer = FileCheckpointer(os.path.join(folder, "checkpoints"))
start = {"order": "A17", "amount": 250, "request": "Refund please"}
cp = flow.run("t1", checkpointer, state=start if mode != "resume" else None,
              sleep=lambda s: None)
with open(counts_path, "w", encoding="utf-8") as handle:
    json.dump(counters, handle)
print(json.dumps({"status": cp["status"], "node": cp["node"], "step": cp["step"]}))
