"""Show the lab's parts at work. Run: python demo.py"""
import json

from agent_loop import run_agent
from sandbox_check import review
from screen_agent import Action, NaiveModel, Policy, run as run_screen
from stand_in import ScriptedModel, call, lab_tools, response, text

print("=== 1. One agent run, turn by turn (a scripted stand-in plays the model) ===\n")
model = ScriptedModel([
    response("tool_use", text("Let me look."), call("t1", "list_files")),
    response("tool_use", call("t2", "read_file", path="notes.txt"),
             call("t3", "issue_refund", order_id="A17", amount=250)),
    response("tool_use", call("t4", "read_file", path="missing.txt")),
    response("end_turn", text("Refunds over 100 need a manager, so I didn't issue it.")),
])
result = run_agent(model, lab_tools(), "Refund order A17 (250) if the notes allow it.")
for message in result.messages:
    for block in (message["content"] if isinstance(message["content"], list)
                  else [{"type": "text", "text": message["content"]}]):
        if block["type"] == "text":
            print(f"{message['role']:>9}: {block['text']}")
        elif block["type"] == "tool_use":
            print(f"{'model':>9}: call {block['name']}({json.dumps(block['input'])})  [id {block['id']}]")
        else:
            flag = "  is_error" if block.get("is_error") else ""
            print(f"{'loop':>9}: result for {block['tool_use_id']}{flag}: {block['content']}")
print(f"\nstatus: {result.status}, turns: {result.turns}, tool log: {result.tool_log}\n")

print("=== 2. Reviewing two docker run commands (nothing is run) ===\n")
for command in ["docker run --privileged -v /var/run/docker.sock:/var/run/docker.sock python:3.12-slim",
                "docker run --rm --network none --cap-drop ALL --security-opt no-new-privileges "
                "--read-only --pids-limit 128 --memory 512m --memory-swap 512m --cpus 1 "
                "--user 65534:65534 --log-opt max-size=1m python:3.12-slim timeout 300 python main.py"]:
    report = review(command)
    print(command)
    print(f"  dangerous: {list(report['dangerous']) or 'none'}")
    print(f"  missing:   {list(report['missing']) or 'none'}")
    print(f"  runtime:   {report['runtime']}\n")

print("=== 3. A screen that tries to give orders ===\n")
model = NaiveModel([Action("open", "shop.example"), Action("click", "Add to cart"), Action("done")])
outcome = run_screen(model, Policy(allowed_sites={"shop.example"}, allowed_kinds={"open", "click"}))
for action in outcome.performed:
    print(f"  done:    {action.kind} {action.target}")
for action, reason in outcome.blocked:
    print(f"  blocked: {action.kind} {action.target} ({reason})")
print(f"  finished: {outcome.done} in {outcome.steps} steps")
