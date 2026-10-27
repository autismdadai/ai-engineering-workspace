#!/usr/bin/env python3
"""Check an answer against one task in evals.json, or self-test every task.

Usage:
  python evals/grade_answer.py --task e1-run-lab --answer answer.txt
  python evals/grade_answer.py --task a1-chsh-four --answer -      (reads stdin)
  python evals/grade_answer.py --self-test

Each task lists patterns an answer must contain and patterns it must not.
They are a first-pass filter, not a judge: read borderline answers against the
task's rubric. --self-test grades each task's known-good answer (it must pass)
and known-bad answer (it must fail), which proves every task's checks can fail.

Output: JSON. Exit code 0 on pass, 1 on fail, 2 on a usage or setup error.
"""
import argparse
import json
import pathlib
import re
import sys


def load_tasks(path: pathlib.Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    tasks = {task["id"]: task for task in data["end_to_end"] + data["adversarial"]}
    for task in tasks.values():
        for pattern in task.get("must_include", []) + task.get("must_not_include", []):
            re.compile(pattern)  # fail early on a broken pattern
    return tasks


def grade(task: dict, answer: str) -> list:
    failed = []
    for pattern in task.get("must_include", []):
        if not re.search(pattern, answer):
            failed.append({"check": "must_include", "pattern": pattern})
    for pattern in task.get("must_not_include", []):
        if re.search(pattern, answer):
            failed.append({"check": "must_not_include", "pattern": pattern})
    return failed


def main() -> int:
    parser = argparse.ArgumentParser(description="Grade an answer against an entanglement-lab eval task.")
    parser.add_argument("--evals", default=str(pathlib.Path(__file__).with_name("evals.json")))
    parser.add_argument("--task", help="task id, for example e1-run-lab")
    parser.add_argument("--answer", help="file holding the answer, or - for stdin")
    parser.add_argument("--self-test", action="store_true", help="grade every task's known-good and known-bad answers")
    args = parser.parse_args()

    try:
        tasks = load_tasks(pathlib.Path(args.evals))
    except (OSError, ValueError, KeyError, re.error) as exc:
        print(json.dumps({"error": f"cannot load tasks: {exc}"}))
        return 2

    if args.self_test:
        all_ok = True
        for task_id, task in tasks.items():
            good, bad = grade(task, task["known_good"]), grade(task, task["known_bad"])
            ok = not good and bool(bad)
            all_ok &= ok
            print(json.dumps({"task": task_id, "ok": ok, "known_good_passes": not good,
                              "known_bad_fails": bool(bad), "known_bad_checks_failed": len(bad),
                              "known_good_failures": good}, ensure_ascii=False))
        print(json.dumps({"self_test": "PASS" if all_ok else "FAIL", "tasks": len(tasks)}))
        return 0 if all_ok else 1

    if not args.task or not args.answer:
        print(json.dumps({"error": "give --task and --answer, or --self-test", "tasks": sorted(tasks)}))
        return 2
    if args.task not in tasks:
        print(json.dumps({"error": f"unknown task: {args.task}", "tasks": sorted(tasks)}))
        return 2
    answer = sys.stdin.read() if args.answer == "-" else pathlib.Path(args.answer).read_text(encoding="utf-8")
    failed = grade(tasks[args.task], answer)
    print(json.dumps({"task": args.task, "passed": not failed, "failed_checks": failed}, ensure_ascii=False))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
