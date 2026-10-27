"""Prove each check can fail: break the code on purpose, expect run_lab to fail.

Each mutation copies the lab to a temporary folder, makes one small edit,
runs run_lab.py there and expects a non-zero exit. The unbroken copy must
pass. Ends with "Every mutation behaved as expected." when all do.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

MUTATIONS = [  # (file, text to find, replacement, what it breaks)
    ("ticket_contract.py", 'value not in schema["enum"]', "False", "enum ignored"),
    ("ticket_contract.py", 'if name not in props:', "if False:", "extra fields allowed"),
    ("ticket_contract.py", 'if name not in value:', "if False:", "required ignored"),
    ("ticket_contract.py", "if expected and not isinstance", "if False and not isinstance",
     "types ignored"),
    ("schema_lint.py", 'if node.get("additionalProperties") is not False:', "if False:",
     "lint misses additionalProperties"),
    ("schema_lint.py", "if missing:", "if False:", "lint misses OpenAI required rule"),
    ("schema_lint.py", '"maxLength", "maxItems"', '"maxItems"', "lint misses maxLength"),
    ("schema_lint.py", 'if "properties" in node and node.get("type") != "object":',
     "if False:", "lint misses a missing object type"),
    ("schema_lint.py", 'text = raw.decode("utf-16")', 'text = raw.decode("utf-8")',
     "lint can't read UTF-16"),
    ("schema_lint.py", "except json.JSONDecodeError as error:", "except KeyError as error:",
     "lint crashes on broken JSON"),
    ("validate_retry.py", "Your last reply was invalid: {'; '.join(errors)}",
     "Your last reply was invalid.", "retry hides the error"),
    ("validate_retry.py", "range(1, max_attempts + 1)", "range(1, max_attempts)",
     "one retry too few"),
    ("tool_loop.py", "if errors:", "if False:", "tool runs unvalidated input"),
    ("tool_loop.py", "if tool is None:", "if False:", "unknown tool not caught"),
    ("tool_loop.py", "for _ in range(max_steps):", "while True:", "no step cap"),
    ("toy_optimizer.py", "if score > best_score:", "if score < best_score or best is None:",
     "optimizer keeps the worst"),
    ("paper_numbers.py", '"mipro": 79.4', '"mipro": 79.9', "copied figure wrong"),
]


def run_copy(edit=None):
    with tempfile.TemporaryDirectory() as tmp:
        for path in HERE.glob("*.py"):
            shutil.copy(path, tmp)
        if edit:
            target = Path(tmp) / edit[0]
            text = target.read_text(encoding="utf-8")
            if edit[1] not in text:
                return "missing"
            target.write_text(text.replace(edit[1], edit[2], 1), encoding="utf-8")
        result = subprocess.run([sys.executable, "run_lab.py"], cwd=tmp,
                                capture_output=True, text=True, timeout=120)
        return "pass" if result.returncode == 0 else "fail"


def main():
    good = True
    control = run_copy()
    print(f"[{'OK' if control == 'pass' else 'BAD'}] unbroken copy: {control}")
    good &= control == "pass"
    for edit in MUTATIONS:
        outcome = run_copy(edit)
        ok = outcome == "fail"
        good &= ok
        print(f"[{'OK' if ok else 'BAD'}] {edit[3]} ({edit[0]}): run_lab {outcome}")
    print("Every mutation behaved as expected." if good else "Some mutations did not.")
    sys.exit(0 if good else 1)


if __name__ == "__main__":
    main()
