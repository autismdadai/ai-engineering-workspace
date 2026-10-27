"""The eval gate as tests, so pytest (or a continuous-integration job) can run it.

    python -m pytest -q test_evals.py

To test the change under review, set CANDIDATE=v2 first (Section 8 shows how on
each system). Each test reuses the lab's own scripts, so the rules live in one place.
"""
import os

import check_overlap
import evalkit
import judge_check
import run_eval

CANDIDATE = os.environ.get("CANDIDATE", "v1")
TICKETS = evalkit.load_jsonl(run_eval.TICKETS)
RESULT = run_eval.check(TICKETS, baseline="v1", candidate=CANDIDATE)


def test_accuracy_floor():
    low = RESULT["accuracy"][CANDIDATE][1][0]
    assert low >= run_eval.ACCURACY_FLOOR, f"lower end {low:.3f} is below the floor"


def test_no_label_loses_recall():
    problems = [p for p in RESULT["problems"] if not p.startswith(("accuracy", "overall"))]
    assert not problems, "; ".join(problems)


def test_not_worse_overall():
    problems = [p for p in RESULT["problems"] if p.startswith("overall")]
    assert not problems, "; ".join(problems)


def test_no_test_ticket_in_prompt_examples():
    assert check_overlap.main([]) == 0


def test_judge_is_consistent_and_agrees_with_people():
    assert judge_check.main([]) == 0
