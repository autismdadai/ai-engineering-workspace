"""Walk through the Part 09 lab: a refund workflow that pauses for a person,
survives a lost reply, and a few numbers about several agents.
Run from this folder: python demo.py
"""
import os
import random
import shutil
import tempfile

import multi_agent as ma
from examples import FakePaymentService, build_refund_workflow
from workflow import FileCheckpointer

waits = []
folder = tempfile.mkdtemp(prefix="demo09-")
store = FileCheckpointer(os.path.join(folder, "checkpoints"), secret="demo-only-secret")
payments = FakePaymentService(lose_reply_times=1)
counters = {}
flow = build_refund_workflow(payments, counters)
start = {"order": "A17", "amount": 250, "request": "Refund please, item arrived broken"}

print("1. Start the thread")
cp = flow.run("A17", store, state=start, sleep=waits.append, rng=random.Random(1))
print(f"   status {cp['status']} after {cp['step']} steps; model {cp['state']['model']}; "
      f"drafts {cp['state']['drafts']}")
print(f"   waiting for a person: {cp['pending']['value']}")

print("2. A person approves; the payment service loses its first reply")
cp = flow.run("A17", store, resume={"decision": "approve", "by": "manager"},
              sleep=waits.append, rng=random.Random(1))
print(f"   status {cp['status']}; refund {cp['state']['refund_id']}")
for entry in cp["log"]:
    print(f"   retry log: {entry}")
print(f"   waited {', '.join(f'{w:.2f} s' for w in waits)} before retrying (full jitter)")
print(f"   charges at the payment service: {len(payments.charges)} (the key stopped a second one)")
print(f"   step code ran: {counters}  (approve's 'notify' ran twice: before and after the pause)")

print("3. The same lost reply without an idempotency key")
payments2 = FakePaymentService(lose_reply_times=1)
flow2 = build_refund_workflow(payments2, {}, use_key=False)
store2 = FileCheckpointer(os.path.join(folder, "checkpoints2"))
flow2.run("A17", store2, state=start, sleep=lambda s: None)
flow2.run("A17", store2, resume={"decision": "approve"}, sleep=lambda s: None)
print(f"   charges: {len(payments2.charges)}  <- the customer was refunded twice")

print("4. Several agents, in toy numbers (words stand in for tokens)")
workers, lead, single = ma.orchestrator_cost(3, 20_000, 1_000, 300)
print(f"   3 workers reading 20,000 each: workers process {workers:,}; "
      f"the lead's context grows {lead:,}; one agent's would grow {single:,}")
print(f"   five steps at 95% each all succeed {ma.chain_success(0.95, 5):.1%} of the time")
for shared in (0.0, 0.5, 1.0):
    acc = ma.majority_vote_accuracy(0.6, 5, shared, 20_000, seed=1)
    print(f"   5 voters, each right 60%, shared mistakes {shared:.0%}: majority right {acc:.1%}")

shutil.rmtree(folder, ignore_errors=True)  # the demo's checkpoints, no longer needed
