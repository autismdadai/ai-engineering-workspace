"""Run every Part 03 check. Ends with "N of N checks passed." when all pass.

python run_lab.py                  core checks (standard library only)
python run_lab.py --with-pydantic  also the Pydantic cross-check
python run_lab.py --with-dspy      also the offline DSPy compile
"""
import json
import os
import subprocess
import sys
import tempfile

import paper_numbers
import tool_loop
import toy_optimizer
import validate_retry
from schema_lint import lint, load_schema
from ticket_contract import TICKET_SCHEMA, parse_and_validate

CHECKS = []


def check(func):
    CHECKS.append(func)
    return func


@check
def python_version():
    """Python is 3.11, 3.12 or 3.13 (the series' range)."""
    return (3, 11) <= sys.version_info[:2] <= (3, 13), sys.version.split()[0]


@check
def contract_verdicts():
    """The validator accepts the good reply and rejects five kinds of bad one."""
    cases = {
        '{"queue": "billing", "priority": "urgent", "summary": "x"}': "valid",
        '{"queue": "billing", "priority": "high", "summary": "x"}': "not one of",
        '{"queue": "billing", "priority": "urgent"}': "missing required",
        '{"queue": "billing", "priority": "urgent", "summary": "x", "y": 1}': "unexpected field",
        '{"queue": 7, "priority": "urgent", "summary": "x"}': "expected string",
        '{"queue": "billing"': "not valid JSON",
    }
    for text, expected in cases.items():
        errors = parse_and_validate(text)[1]
        if expected == "valid" and errors:
            return False, f"rejected a good reply: {errors}"
        if expected != "valid" and not any(expected in e for e in errors):
            return False, f"missed '{expected}' in {text}"
    return True, f"{len(cases)} of {len(cases)} verdicts right"


@check
def schema_lint_rules():
    """The linter passes the ticket schema and flags each strict-mode problem."""
    if not lint(TICKET_SCHEMA)["ok"]:
        return False, "ticket schema flagged"
    bad = {"type": "object",
           "properties": {"name": {"type": "string", "maxLength": 20},
                          "age": {"type": "integer", "minimum": 0}},
           "required": ["name"]}
    report = lint(bad)
    a, o = " ".join(report["anthropic"]), " ".join(report["openai"])
    typeless = lint({"properties": {"a": {"type": "string"}}})
    with tempfile.TemporaryDirectory() as tmp:  # files as Windows and editors write them
        utf16 = os.path.join(tmp, "utf16.json")
        with open(utf16, "w", encoding="utf-16") as handle:
            json.dump(TICKET_SCHEMA, handle)
        broken = os.path.join(tmp, "broken.json")
        with open(broken, "w", encoding="utf-8") as handle:
            handle.write('{"type": "object",}')
        read_utf16 = load_schema(utf16)[0] == TICKET_SCHEMA
        broken_error = load_schema(broken)[1] or ""
    wanted = ["additionalProperties" in a, "maxLength" in a, "minimum" in a,
              "additionalProperties" in o, "not in required: age" in o,
              not typeless["ok"], read_utf16, "not valid JSON" in broken_error]
    return all(wanted), f"{sum(wanted)} of {len(wanted)} linter checks right"


@check
def retry_loop():
    """A bad reply is retried with its error; three bad replies give up."""
    model = validate_retry.StandInModel(validate_retry.RECORDED_REPLIES)
    good = validate_retry.route_ticket(model, "charged twice")
    told = "is not one of" in model.prompts[-1]
    bad_model = validate_retry.StandInModel([validate_retry.RECORDED_REPLIES[0]] * 3)
    bad = validate_retry.route_ticket(bad_model, "charged twice")
    ok = good["ok"] and good["attempts"] == 2 and told and not bad["ok"] \
        and len(bad_model.prompts) == 3
    return ok, f"fixed on attempt {good['attempts']}; gave up after {len(bad_model.prompts)}"


@check
def tool_loop_guards():
    """Bad arguments and unknown tools come back as errors; the step cap holds."""
    text, transcript, reason = tool_loop.agent_loop(tool_loop.SCRIPT_GOOD)
    first = transcript[1]
    unknown = tool_loop.run_tool({"name": "delete_order", "input": {}})
    _, _, runaway = tool_loop.agent_loop(tool_loop.SCRIPT_RUNAWAY, max_steps=5)
    ok = (reason == "answered" and first.get("is_error") is True
          and unknown["is_error"] and runaway == "max_steps")
    return ok, f"good run {reason}; runaway run {runaway}"


@check
def optimizer_overfits_small_val():
    """Chosen on 5 tickets, the best prompt does worse on new tickets than one chosen on 15."""
    rows = toy_optimizer.report()
    small, big = rows["small_val"], rows["big_val"]
    ok = small["val"] == 1.0 and small["test"] < big["test"]
    return ok, f"small-val pick test {small['test']}; big-val pick test {big['test']}"


@check
def paper_arithmetic():
    """The cited MIPRO and GEPA differences recompute from the tables."""
    got = paper_numbers.compute()
    ok = (got["mipro_scone_points"] == 10.3 and got["mipro_scone_relative_pct"] == 14.9
          and got["gepa_minus_mipro_points"] == {"qwen3_8b": 7.01, "gpt_4_1_mini": 6.55}
          and got["grpo_over_gepa_rollouts"] == [3.4, 13.1])
    return ok, "10.3 points; 7.01 and 6.55 points; 3.4x to 13.1x"


def optional(script, expected):
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    return expected in result.stdout, (result.stdout.strip().splitlines() or
                                       [result.stderr.strip()[-200:]])[-1]


def main():
    def pydantic_agrees():
        return optional("optional_pydantic_check.py", "agreement: 6 of 6")

    def dspy_compiles_offline():
        return optional("optional_dspy_check.py", "kept 2 of 3")

    if "--with-pydantic" in sys.argv:
        CHECKS.append(pydantic_agrees)
    if "--with-dspy" in sys.argv:
        CHECKS.append(dspy_compiles_offline)
    passed = 0
    for number, func in enumerate(CHECKS, 1):
        try:
            ok, detail = func()
        except Exception as error:  # a crash counts as a failed check
            ok, detail = False, f"{type(error).__name__}: {error}"
        name = getattr(func, "__name__", "optional")
        print(f"[{'PASS' if ok else 'FAIL'}] check {number}: {name}: {detail}")
        passed += ok
    print(f"{passed} of {len(CHECKS)} checks passed.")
    sys.exit(0 if passed == len(CHECKS) else 1)


if __name__ == "__main__":
    main()
