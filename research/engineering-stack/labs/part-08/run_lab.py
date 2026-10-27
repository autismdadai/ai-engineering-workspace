"""Part 08 lab checks: an agent loop driven by a scripted stand-in model, a
docker-run reviewer, a computer-use harness and the not-a-sandbox demo.
Standard library only. Run: python run_lab.py

Each check runs on its own, so one failure prints FAIL and the rest still run.
"""
import json
import sys
import time

from agent_loop import context_tokens, run_agent
from not_a_sandbox import escaped
from sandbox_check import review
from screen_agent import Action, NaiveModel, Policy, run as run_screen
from stand_in import LoopingModel, ScriptedModel, call, lab_tools, response, text

CHECKS = []


def check(label):
    def register(fn):
        CHECKS.append((label, fn))
        return fn
    return register


def results_of(message):
    return [b for b in message["content"] if b.get("type") == "tool_result"]


@check("1 tool_use, then end_turn: the loop runs the tool, sends the result back, and stops")
def _():
    model = ScriptedModel([response("tool_use", text("Looking."), call("t1", "list_files")),
                           response("end_turn", text("There are three files."))])
    result = run_agent(model, lab_tools(), "What files are there?")
    sent_back = model.seen[1][0][-1]
    first = sent_back["content"][0]
    ok = (result.status == "done" and result.turns == 2 and first["type"] == "tool_result"
          and first["tool_use_id"] == "t1" and "README.md" in first["content"]
          and result.final_text == "There are three files.")
    return ok, f"{result.status} after {result.turns} turns"


@check("1b two calls in one response: both results go back in one message, in order, results first")
def _():
    model = ScriptedModel([response("tool_use", call("a", "read_file", path="README.md"),
                                    call("b", "read_file", path="notes.txt")),
                           response("end_turn", text("Done."))])
    run_agent(model, lab_tools(), "Read both.")
    blocks = model.seen[1][0][-1]["content"]
    ids = [b["tool_use_id"] for b in blocks]
    return ids == ["a", "b"] and all(b["type"] == "tool_result" for b in blocks), ids


@check("1c end_turn ends the loop even if the response also holds a tool call; nothing runs")
def _():
    model = ScriptedModel([response("end_turn", text("Done."), call("t1", "issue_refund",
                                                                  order_id="A1", amount=5))])
    result = run_agent(model, lab_tools(), "Go.", approver=lambda n, a: True)
    return result.status == "done" and result.tool_log == [] and model.calls == 1, result.status


@check("2 an unknown tool comes back as is_error, naming the real tools, and the loop goes on")
def _():
    model = ScriptedModel([response("tool_use", call("t1", "delete_everything")),
                           response("end_turn", text("I can't do that."))])
    result = run_agent(model, lab_tools(), "Clean up.")
    block = results_of(model.seen[1][0][-1])[0]
    ok = (block.get("is_error") is True and "list_files" in block["content"]
          and result.status == "done" and result.tool_log == [("delete_everything", "unknown tool")])
    return ok, block["content"][:60]


@check("2b bad arguments are refused before the tool runs")
def _():
    model = ScriptedModel([response("tool_use", call("t1", "read_file"),
                                    call("t2", "read_file", path=7)),
                           response("end_turn", text("ok"))])
    result = run_agent(model, lab_tools(), "Read.")
    blocks = results_of(model.seen[1][0][-1])
    ok = ([b.get("is_error") for b in blocks] == [True, True]
          and "missing required argument 'path'" in blocks[0]["content"]
          and "must be string" in blocks[1]["content"]
          and result.tool_log == [("read_file", "invalid arguments")] * 2)
    return ok, [b["content"][:40] for b in blocks]


@check("2c an unexpected error reaches the model as a generic message; details go to the developer's log")
def _():
    model = ScriptedModel([response("tool_use", call("t1", "broken_tool")),
                           response("end_turn", text("The service is down."))])
    result = run_agent(model, lab_tools(), "Try it.")
    block = results_of(model.seen[1][0][-1])[0]
    logged = "".join(result.errors[0][1]) if result.errors else ""
    ok = (block.get("is_error") is True and "sk-test-0000" not in block["content"]
          and "Traceback" not in block["content"] and "sk-test-0000" in logged)
    return ok, block["content"]


@check("2d a ToolError's message, written for the model, does reach it")
def _():
    model = ScriptedModel([response("tool_use", call("t1", "read_file", path="nope.txt")),
                           response("end_turn", text("ok"))])
    run_agent(model, lab_tools(), "Read.")
    block = results_of(model.seen[1][0][-1])[0]
    return block.get("is_error") is True and "call list_files" in block["content"], block["content"]


@check("2e the loop stops waiting for a slow tool at its time limit, and goes on")
def _():
    model = ScriptedModel([response("tool_use", call("t1", "slow_report")),
                           response("end_turn", text("It was too slow."))])
    start = time.monotonic()
    result = run_agent(model, lab_tools(timeout=0.5), "Report.")
    seconds = time.monotonic() - start
    block = results_of(model.seen[1][0][-1])[0]
    ok = (block.get("is_error") is True and "may still finish" in block["content"]
          and "do not call it again" in block["content"] and seconds < 3 and result.status == "done")
    return ok, f"{seconds:.1f} s; told the model: {block['content'][:60]}..."


@check("2f a timed-out tool can still finish: the log says so (threads can't be stopped)")
def _():
    from agent_loop import Tool
    done = []

    def slow_write():
        time.sleep(0.6)
        done.append("written")
        return "ok"

    tools = [Tool("slow_write", slow_write, {"type": "object", "properties": {}}, timeout=0.2)]
    model = ScriptedModel([response("tool_use", call("t1", "slow_write")),
                           response("end_turn", text("ok"))])
    result = run_agent(model, tools, "Write.")
    time.sleep(1.0)
    ok = result.tool_log == [("slow_write", "timeout, may still finish")] and done == ["written"]
    return ok, f"log: {result.tool_log[0][1]}; the tool finished anyway: {done == ['written']}"


@check("3 a high-impact tool doesn't run unless a person approves it")
def _():
    script = lambda: [response("tool_use", call("r1", "issue_refund", order_id="A17", amount=250)),
                      response("end_turn", text("ok"))]
    denied = run_agent(ScriptedModel(script()), lab_tools(), "Refund A17.")
    asked = []
    approved = run_agent(ScriptedModel(script()), lab_tools(), "Refund A17.",
                         approver=lambda name, args: asked.append((name, args)) or True)
    ok = (denied.tool_log == [("issue_refund", "denied")]
          and approved.tool_log == [("issue_refund", "ok")]
          and asked == [("issue_refund", {"order_id": "A17", "amount": 250})])
    return ok, f"default: {denied.tool_log[0][1]}; approved: {approved.tool_log[0][1]}"


@check("3b only an exact True approves: an approver that says 'no' or crashes counts as a no")
def _():
    script = lambda: [response("tool_use", call("r1", "issue_refund", order_id="A17", amount=250)),
                      response("end_turn", text("ok"))]

    def crashing(name, args):
        raise RuntimeError("approval service down")

    outcomes = [run_agent(ScriptedModel(script()), lab_tools(), "Refund.", approver=a).tool_log[0][1]
                for a in (lambda n, a: "no", lambda n, a: 1, crashing)]
    flag = run_agent(ScriptedModel([response("tool_use", call("r1", "issue_refund", order_id="A1",
                                                              amount=True)),
                                    response("end_turn", text("ok"))]), lab_tools(), "Refund.",
                     approver=lambda n, a: True).tool_log[0][1]
    ok = outcomes == ["denied", "denied", "denied"] and flag == "invalid arguments"
    return ok, f"'no', 1, crash: {outcomes}; amount=True: {flag}"


@check("4 a model that never stops is cut off at the turn cap")
def _():
    model = LoopingModel()
    result = run_agent(model, lab_tools(), "Go.", max_turns=10)
    return result.status == "max_turns" and model.calls == 10, f"{result.status} after {model.calls} model calls"


@check("4b the token budget stops the loop too")
def _():
    model = LoopingModel()   # each response reports 120 tokens
    result = run_agent(model, lab_tools(), "Go.", max_turns=100, token_budget=600)
    return result.status == "budget" and model.calls == 5, f"{result.status} after {model.calls} calls, {result.tokens} tokens"


@check("5 a tool call cut off by max_tokens is never run; the loop asks again with more room")
def _():
    model = ScriptedModel([response("max_tokens", text("I will refund"),
                                    call("r1", "issue_refund", order_id="A1")),
                           response("tool_use", call("t1", "list_files")),
                           response("end_turn", text("ok"))])
    result = run_agent(model, lab_tools(), "Go.", approver=lambda n, a: True)
    budgets = [m for _, m in model.seen]
    ok = (result.status == "done" and budgets[:2] == [1024, 4096]
          and ("issue_refund", "ok") not in result.tool_log
          and result.tool_log == [("list_files", "ok")])
    return ok, f"max_tokens sent: {budgets}"


@check("5b pause_turn: the response goes back as it is and the loop continues")
def _():
    paused = response("pause_turn", text("Searching..."))
    model = ScriptedModel([paused, response("end_turn", text("Found it."))])
    result = run_agent(model, lab_tools(), "Search.")
    last = model.seen[1][0][-1]
    ok = result.status == "done" and last == {"role": "assistant", "content": paused["content"]}
    return ok, result.status


@check("5c refusal, a full context window and an unknown stop reason each stop the loop cleanly")
def _():
    outcomes = []
    for reason in ("refusal", "model_context_window_exceeded", "something_new"):
        model = ScriptedModel([response(reason, text("..."), call("t1", "list_files"))])
        result = run_agent(model, lab_tools(), "Go.")
        outcomes.append((result.status, result.tool_log))
    ok = outcomes == [("refusal", []), ("context_full", []), ("unknown_stop_reason", [])]
    return ok, [o[0] for o in outcomes]


@check("6 context growth when the whole history is resent each turn")
def _():
    figures = [context_tokens(5000, 1500, 20), context_tokens(5000, 1500, 40)]
    ok = figures == [(33500, 385000), (63500, 1370000)]
    return ok, f"turn 20: {figures[0][0]:,} sent, {figures[0][1]:,} in total; 40 turns: {figures[1][1]:,}"


HARDENED = ("docker run --rm --network none --cap-drop ALL --security-opt no-new-privileges "
            "--read-only --tmpfs /tmp:rw,noexec,nosuid,size=64m --pids-limit 128 "
            "--memory 512m --memory-swap 512m --cpus 1 --user 65534:65534 --log-opt max-size=1m "
            "-v \"$PWD/task:/work:ro\" -w /work python:3.12-slim timeout 300 python /work/main.py")


@check("7 the hardened command has every hardening option and nothing dangerous")
def _():
    report = review(HARDENED)
    ok = report["ok"] and report["image"] == "python:3.12-slim" and not report["missing"]
    return ok, f"image {report['image']}, runtime: {report['runtime']}"


@check("7b each dangerous option is caught")
def _():
    cases = {
        "privileged": "docker run --privileged img",
        "runtime_socket": "docker run -v /var/run/docker.sock:/var/run/docker.sock img",
        "host_namespace": "docker run --network=host img",
        "seccomp_off": "docker run --security-opt seccomp=unconfined img",
        "root_user": "docker run --user 0 img",
        "cap_add": "docker run --cap-add SYS_ADMIN img",
        "host_path_mount": "docker run -v /:/host img",
        "lsm_off": "docker run --security-opt apparmor=unconfined img",
    }
    missed = [k for k, cmd in cases.items() if k not in review(cmd)["dangerous"]]
    return not missed, f"{len(cases) - len(missed)} of {len(cases)}" + (f", missed {missed}" if missed else "")


@check("7c tricks that fooled an earlier version are caught: unknown options, short flags, weak values")
def _():
    base = HARDENED.replace(' -v "$PWD/task:/work:ro" -w /work python:3.12-slim timeout 300 python /work/main.py', " ")
    tricks = [
        "docker run -p 8080:80 --privileged img",             # an option it didn't know hid the rest
        "docker run --ulimit nofile=10 --restart no --privileged img",
        "docker run -itv /:/host img",                         # combined short flags
        base + "--userns=host img", base + "--ipc host img", base + "--pid container:x img",
        base + "--mount type=bind,source=/var/run,target=/r img",
        base.replace("--read-only", "--read-only=false") + "img",
        base.replace("--memory 512m", "--memory 0") + "img",
        base + "--pids-limit -1 img",                          # the last value wins
    ]
    fooled = [t for t in tricks if review(t)["ok"]]
    return not fooled, f"{len(tricks) - len(fooled)} of {len(tricks)} not ok" + (f"; fooled by {fooled}" if fooled else "")


@check("7d a bare docker run is missing all 8 hardening options and uses the default runtime")
def _():
    report = review("docker run python:3.12-slim python main.py")
    ok = len(report["missing"]) == 8 and not report["dangerous"] and report["runtime"].startswith("default")
    return ok, f"{len(report['missing'])} missing"


@check("8 an instruction shown on screen is blocked; the user's task still completes")
def _():
    model = NaiveModel([Action("open", "shop.example"), Action("click", "Add to cart"), Action("done")])
    policy = Policy(allowed_sites={"shop.example"}, allowed_kinds={"open", "click"})
    outcome = run_screen(model, policy)
    performed = [(a.kind, a.target) for a in outcome.performed]
    blocked = [(a.kind, a.target) for a, r in outcome.blocked]
    ok = outcome.done and performed == [("open", "shop.example"), ("click", "Add to cart")] \
        and blocked == [("send", "pay.example")]
    return ok, f"performed {performed}; blocked {blocked}"


@check("8b the harness never trusts the model's account: a mislabelled injection is still blocked")
def _():
    model = NaiveModel([Action("open", "shop.example"), Action("done")], honest_labels=False)
    policy = Policy(allowed_sites={"shop.example"}, allowed_kinds={"open", "send"},
                    allowed_recipients={"receipts.example"}, confirm=lambda action: True)
    outcome = run_screen(model, policy)
    reasons = [r for _, r in outcome.blocked]
    ok = (outcome.done and not any(a.kind == "send" for a in outcome.performed)
          and reasons == ["'pay.example' is not a recipient this task allows"])
    return ok, reasons[0] if reasons else "nothing blocked"


@check("8c sites off the allowlist are blocked; high-risk actions wait for the user")
def _():
    policy = Policy(allowed_sites={"shop.example"}, allowed_kinds={"open", "purchase"},
                    allowed_recipients={"shop.example"})
    off_list = run_screen(NaiveModel([Action("open", "other.example"), Action("done")]), policy)
    unconfirmed = run_screen(NaiveModel([Action("purchase", "shop.example"), Action("done")]), policy)
    policy.confirm = lambda action: True
    confirmed = run_screen(NaiveModel([Action("purchase", "shop.example"), Action("done")]), policy)
    ok = ("allowlist" in off_list.blocked[0][1]
          and "confirmation" in unconfirmed.blocked[0][1] and not unconfirmed.performed
          and [a.kind for a in confirmed.performed] == ["purchase"])
    return ok, ""


@check("8d the limit: an injected action inside the task's scope is not blocked")
def _():
    from screen_agent import check as allowed
    policy = Policy(allowed_sites={"shop.example"}, allowed_kinds={"open", "click"})
    stray = Action("click", "Red mug", source="screen")   # the task wanted the blue one
    return allowed(stray, policy) is None, "a click on the wrong item passes: scope, not intent, is checked"


@check("9 exec() with empty builtins still reaches the os module: not a sandbox")
def _():
    reached, detail = escaped()
    return reached is True and isinstance(detail, str), "reached os.getcwd()"


@check("10 paper arithmetic")
def _():
    figures = {
        "ReAct vs CoT-SC on HotpotQA EM (points)": (round(33.4 - 27.4, 1), 6.0),
        "tau-bench airline, tool calling minus ReAct (pass^1)": (round(0.420 - 0.325, 3), 0.095),
        "Claude for Chrome attack success drop (points)": (round(23.6 - 11.2, 1), 12.4),
        "same, relative (%)": (round((23.6 - 11.2) / 23.6 * 100, 1), 52.5),
        "audited SWE-bench Verified problems with flawed tests": (round(138 * 0.594), 82),
        "Firecracker: 5 per core per second on 36 cores": (5 * 36, 180),
        "OSWorld tasks without Google Drive": (369 - 8, 361),
        "20 screenshots at 1,000 to 1,800 tokens each": ((20 * 1000, 20 * 1800), (20000, 36000)),
        "Docker default capabilities kept": (len("CHOWN DAC_OVERRIDE FSETID FOWNER MKNOD NET_RAW SETGID "
                                                 "SETUID SETFCAP SETPCAP NET_BIND_SERVICE SYS_CHROOT "
                                                 "KILL AUDIT_WRITE".split()), 14),
    }
    wrong = {k: v for k, v in figures.items() if v[0] != v[1]}
    return not wrong, wrong or f"{len(figures)} figures"


passed = 0
for label, fn in CHECKS:
    try:
        ok, detail = fn()
    except Exception as error:  # a crash is a failed check, reported plainly
        ok, detail = False, f"error: {type(error).__name__}: {error}"
    passed += bool(ok)
    print(f"{'PASS' if ok else 'FAIL'} {label}{': ' + str(detail) if detail not in ('', None) else ''}")

print(f"\n{passed} of {len(CHECKS)} checks passed")
sys.exit(0 if passed == len(CHECKS) else 1)
