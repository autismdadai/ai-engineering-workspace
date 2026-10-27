"""Prove the checks can fail: break the lab on purpose, one change at a time,
in a temporary copy, and confirm run_lab.py notices each break.
A break that makes the loop run forever counts as caught when run_lab.py
exceeds its time limit. Run: python mutation_check.py
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
FILES = ["agent_loop.py", "stand_in.py", "sandbox_check.py", "screen_agent.py",
         "not_a_sandbox.py", "run_lab.py"]
TIME_LIMIT = 60  # seconds for one run of run_lab.py

# (description, file, original text, broken text)
MUTATIONS = [
    ("loop keeps going after end_turn", "agent_loop.py",
     '        if reason == "end_turn":\n            return RunResult("done", turns, text, tokens, messages, log, errors)\n', ""),
    ("text sent before the tool results", "agent_loop.py",
     "        messages.append({\"role\": \"user\", \"content\": results})",
     "        messages.append({\"role\": \"user\", \"content\": [{\"type\": \"text\", \"text\": \"Results:\"}] + results})"),
    ("parallel results sent in reverse order", "agent_loop.py",
     "        results = [execute(call, tools, approver, log, errors) for call in calls]",
     "        results = [execute(call, tools, approver, log, errors) for call in reversed(calls)]"),
    ("unknown tool crashes the loop", "agent_loop.py",
     '        log.append((call["name"], "unknown tool"))\n',
     '        raise KeyError(call["name"])\n'),
    ("arguments not validated", "agent_loop.py",
     '    problem = validate_call(tool, call.get("input"))', "    problem = None"),
    ("a true/false value accepted as a number", "agent_loop.py",
     "(expected is not bool and isinstance(value, bool))", "False"),
    ("exception text sent to the model", "agent_loop.py",
     'f"({type(error).__name__}). Details were logged."', 'f"({type(error).__name__}): {error}"'),
    ("tool time limit ignored", "agent_loop.py",
     "    worker.join(seconds)", "    worker.join()"),
    ("a timed-out tool reported as safe to retry", "agent_loop.py",
     'and may still finish. Its outcome "', 'Try again. "'),
    ("high-impact tools run without approval", "agent_loop.py",
     '    if tool.high_impact and not approved(approver, tool.name, call["input"]):', "    if False:"),
    ("any truthy answer approves", "agent_loop.py",
     "        return approver(name, arguments) is True", "        return bool(approver(name, arguments))"),
    ("a crashing approver crashes the run", "agent_loop.py",
     "    except Exception:\n        return False\n", "    except ZeroDivisionError:\n        return False\n"),
    ("no turn cap", "agent_loop.py",
     "        if turns >= max_turns:", "        if False:"),
    ("token budget ignored", "agent_loop.py",
     "        if tokens >= token_budget:", "        if False:"),
    ("truncated tool call is run", "agent_loop.py",
     '        if reason == "max_tokens":', '        if reason == "max_tokens" and False:'),
    ("pause_turn treated as finished", "agent_loop.py",
     '        if reason == "pause_turn":\n            continue',
     '        if reason == "pause_turn":\n            return RunResult("done", turns, text, tokens, messages, log, errors)'),
    ("refusal treated as a tool call", "agent_loop.py",
     '        if reason == "refusal":\n            return RunResult("refusal", turns, text, tokens, messages, log, errors)\n', ""),
    ("context arithmetic off by one turn", "agent_loop.py",
     "    last = prefix + per_turn * (turns - 1)", "    last = prefix + per_turn * turns"),
    ("--privileged not flagged", "sandbox_check.py",
     '            danger.add("privileged")', "            pass"),
    ("runtime socket mount not flagged", "sandbox_check.py",
     'if ".sock" in source or', 'if False or'),
    ("host-path mounts not flagged", "sandbox_check.py",
     '                danger.add("host_path_mount")', "                pass"),
    ("--cap-drop ALL not recognised", "sandbox_check.py",
     'n == "--cap-drop" and (v or "").upper() == "ALL"', 'n == "--cap-drop" and v == "all"'),
    ("unknown options read as flags (the old bug)", "sandbox_check.py",
     "            elif word in LONG_FLAGS:", "            elif True:"),
    ("first value wins instead of the last", "sandbox_check.py",
     "    return found[-1] if found else None", "    return found[0] if found else None"),
    ("harness trusts the model's account of an action", "screen_agent.py",
     '    if action.kind == "done":\n        return None\n',
     '    if action.kind == "done" or action.source == "task":\n        return None\n'),
    ("recipients not checked", "screen_agent.py",
     "    if action.kind in HIGH_RISK and action.target not in policy.allowed_recipients:",
     "    if False:"),
    ("high-risk actions don't wait for the user", "screen_agent.py",
     "    if action.kind in HIGH_RISK and not policy.confirm(action):", "    if False:"),
    ("demo looks for the wrong class, so it seems safe", "not_a_sandbox.py",
     'cls.__name__ == "BuiltinImporter"', 'cls.__name__ == "BuiltinImporterX"'),
]


def copy_lab():
    folder = pathlib.Path(tempfile.mkdtemp())
    for name in FILES:
        shutil.copy(HERE / name, folder / name)
    return folder


def run(folder):
    try:
        result = subprocess.run([sys.executable, "run_lab.py"], cwd=folder, capture_output=True,
                                text=True, timeout=TIME_LIMIT)
    except subprocess.TimeoutExpired:
        return None
    return result


control_folder = copy_lab()
control = run(control_folder)
shutil.rmtree(control_folder, ignore_errors=True)
if control is None or control.returncode != 0:
    print("FAIL the unbroken copy does not pass; fix the lab first")
    print(control.stdout[-2000:] if control else "it timed out")
    sys.exit(1)
print("OK   the unbroken copy passes")

caught = 0
for description, filename, original, broken in MUTATIONS:
    folder = copy_lab()
    path = folder / filename
    source = path.read_text(encoding="utf-8")
    if source.count(original) != 1:
        print(f"ERROR {description}: the text to change was found {source.count(original)} times")
        shutil.rmtree(folder, ignore_errors=True)
        continue
    path.write_text(source.replace(original, broken), encoding="utf-8")
    result = run(folder)
    if result is None:
        caught += 1
        print(f"CAUGHT {description}: run_lab.py ran past {TIME_LIMIT} s (the loop never stopped)")
    elif result.returncode != 0:
        caught += 1
        failed = [line for line in result.stdout.splitlines() if line.startswith("FAIL")]
        first = failed[0] if failed else "crashed: " + (result.stderr.strip().splitlines() or ["?"])[-1]
        print(f"CAUGHT {description}: {first[:110]}")
    else:
        print(f"MISSED {description}")
    shutil.rmtree(folder, ignore_errors=True)

print(f"\n{caught} of {len(MUTATIONS)} mutations caught")
sys.exit(0 if caught == len(MUTATIONS) else 1)
