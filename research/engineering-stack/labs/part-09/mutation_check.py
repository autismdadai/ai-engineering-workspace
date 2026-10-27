"""Prove the checks can fail: break the lab on purpose, one change at a time,
in a temporary copy, and confirm run_lab.py notices each break.
A break that makes a run never stop counts as caught when run_lab.py
exceeds its time limit. Run: python mutation_check.py
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
FILES = ["workflow.py", "examples.py", "multi_agent.py", "crash_run.py", "run_lab.py"]
TIME_LIMIT = 120  # seconds for one run of run_lab.py

# (description, file, original text, broken text)
MUTATIONS = [
    ("answers never reach a paused step", "workflow.py",
     '            ctx = Context(cp["resume"])', "            ctx = Context([])"),
    ("answers matched to the wrong pause", "workflow.py",
     "        self._index += 1\n", ""),
    ("a new answer replaces earlier ones", "workflow.py",
     '            cp["resume"].append(resume)', '            cp["resume"] = [resume]'),
    ("answers carried into the next step", "workflow.py",
     '                  "step": cp["step"] + 1, "resume": [], "status": "running",',
     '                  "step": cp["step"] + 1, "resume": cp["resume"], "status": "running",'),
    ("a retried step keeps its place among answers", "workflow.py",
     "            ctx._index = 0  # a retried step starts over, interrupts included\n", ""),
    ("a pause is retried like a failure", "workflow.py",
     "            except Interrupt:\n                raise  # a pause is not a failure: never retried\n", ""),
    ("every error is retried", "workflow.py",
     "            except policy.retry_on as error:", "            except Exception as error:"),
    ("one attempt too few", "workflow.py",
     "                if attempt + 1 == policy.max_attempts:",
     "                if attempt + 2 >= policy.max_attempts:"),
    ("the last failure is swallowed", "workflow.py",
     "                    raise\n                sleep(", "                    return {}\n                sleep("),
    ("no cap on the wait", "workflow.py",
     "        return rng.uniform(0, min(self.cap, self.initial * self.factor ** n))",
     "        return rng.uniform(0, self.initial * self.factor ** n)"),
    ("waits never grow", "workflow.py",
     "self.initial * self.factor ** n))", "self.initial))"),
    ("step limit off by one", "workflow.py",
     '            if cp["step"] >= step_limit:', '            if cp["step"] > step_limit:'),
    ("no checkpoint after a step", "workflow.py",
     '            checkpointer.save(thread_id, cp)  # saved before the next step starts\n', ""),
    ("signature not checked", "workflow.py",
     "            if not hmac.compare_digest(expected, str(record.get(\"signature\", \"\"))):",
     "            if \"signature\" in record and not hmac.compare_digest(expected, record[\"signature\"]):"),
    ("signed files load without a check", "workflow.py",
     "        body = record[\"checkpoint\"]\n        if self.secret:",
     "        body = record[\"checkpoint\"]\n        if False:"),
    ("thread ids only checked at the start", "workflow.py",
     "_THREAD_ID.fullmatch(thread_id)", "_THREAD_ID.match(thread_id)"),
    ("an existing thread restarted from scratch", "workflow.py",
     "        elif state is not None:\n            raise ValueError(f\"thread {thread_id!r} already exists\")\n", ""),
    ("a paused thread continues with no answer", "workflow.py",
     "            if resume is None:\n                raise ValueError(f\"thread {thread_id!r} is paused; pass resume=\")\n", ""),
    ("idempotency key reuse with new parameters allowed", "workflow.py",
     "            if records[key][\"fingerprint\"] != fingerprint:", "            if False:"),
    ("idempotency results not saved", "workflow.py",
     "        records[key] = {\"fingerprint\": fingerprint, \"result\": result}\n", ""),
    ("approval is case-insensitive", "workflow.py",
     'answer.get("decision") == "approve"', 'str(answer.get("decision")).lower() == "approve"'),
    ("any answer approves", "examples.py",
     'flow.add_router("approve", lambda s: "refund" if s["approved"] else END)',
     'flow.add_edge("approve", "refund")'),
    ("payment service ignores idempotency keys", "examples.py",
     "        if idempotency_key is not None and idempotency_key in self.keys:",
     "        if False:"),
    ("review loop has no cap", "examples.py",
     '        if state["drafts"] >= max_drafts:', '        if state["drafts"] > max_drafts:'),
    ("routing ignores hard words", "examples.py",
     '    return "large-model" if any(', '    return "small-model" if any('),
    ("refund step not retried", "examples.py",
     "                  retry=RetryPolicy(max_attempts=3, initial=0.5, factor=2.0, cap=8.0))",
     "                  retry=None)"),
    ("handoff passes only the last message", "multi_agent.py",
     '    return [{"role": "system", "text": instructions}] + list(history)',
     '    return [{"role": "system", "text": instructions}] + list(history)[-1:]'),
    ("subagent returns everything it read", "multi_agent.py",
     '    text = " ".join(" ".join(documents).split()[:summary_words])',
     '    text = " ".join(documents)'),
    ("lead pays for what workers read", "multi_agent.py",
     "    lead_extra = n_workers * (brief + summary)", "    lead_extra = n_workers * (brief + read + summary)"),
    ("correlated voters treated as independent", "multi_agent.py",
     "            votes = [rng.random() < p_correct] * voters",
     "            votes = [rng.random() < p_correct for _ in range(voters)]"),
    ("ties counted as right", "multi_agent.py",
     "        right += sum(votes) * 2 > voters", "        right += sum(votes) * 2 >= voters"),
    ("tagging does nothing", "multi_agent.py",
     "            text = f\"<data from='agent-{i}'>{text}</data>\"", "            pass"),
    ("chain success adds instead of multiplying", "multi_agent.py",
     "    return p ** k", "    return 1 - (1 - p) * k"),
]


def copy_lab():
    folder = pathlib.Path(tempfile.mkdtemp(prefix="lab09-mut-"))
    for name in FILES:
        shutil.copy(HERE / name, folder / name)
    return folder


def run(folder):
    try:
        return subprocess.run([sys.executable, "run_lab.py"], cwd=folder,
                              capture_output=True, text=True, timeout=TIME_LIMIT)
    except subprocess.TimeoutExpired:
        return None


def main():
    control_folder = copy_lab()
    control = run(control_folder)
    shutil.rmtree(control_folder, ignore_errors=True)
    if control is None or control.returncode != 0:
        print("FAIL the unbroken copy does not pass; fix the lab first")
        print(control.stdout[-2000:] if control else "it timed out")
        return 1
    print("OK   the unbroken copy passes")

    caught = 0
    for description, filename, original, broken in MUTATIONS:
        folder = copy_lab()
        path = folder / filename
        source = path.read_text(encoding="utf-8")
        if source.count(original) != 1:
            print(f"ERROR {description}: the text to change was found "
                  f"{source.count(original)} times")
            shutil.rmtree(folder, ignore_errors=True)
            continue
        path.write_text(source.replace(original, broken), encoding="utf-8")
        result = run(folder)
        if result is None:
            caught += 1
            print(f"CAUGHT {description}: run_lab.py ran past {TIME_LIMIT} s")
        elif result.returncode != 0:
            caught += 1
            failed = [l for l in result.stdout.splitlines() if l.startswith("FAIL")]
            first = failed[0] if failed else "crashed: " + (
                result.stderr.strip().splitlines() or ["?"])[-1]
            print(f"CAUGHT {description}: {first[:110]}")
        else:
            print(f"MISSED {description}")
        shutil.rmtree(folder, ignore_errors=True)

    print(f"\n{caught} of {len(MUTATIONS)} mutations caught")
    return 0 if caught == len(MUTATIONS) else 1


if __name__ == "__main__":
    sys.exit(main())
