"""Check a JSON Schema against two vendors' strict-mode rules.

Usage: python schema_lint.py schema.json
Prints one JSON report. Exit code 0: no problems; 1: problems found;
2: the file couldn't be read as JSON, or no file was given.
It never calls a model or the network.

Rules as documented on October 12, 2026 (re-check the pages; they change):
- Anthropic structured outputs: objects need additionalProperties false;
  no recursion, external $ref, numeric or string-length limits, or array
  limits beyond minItems 0 or 1.
- OpenAI strict mode: every object needs additionalProperties false and
  must list every property in "required" (make a field optional by
  allowing null instead).
"""
import json
import sys

ANTHROPIC_UNSUPPORTED = {"minimum", "maximum", "exclusiveMinimum",
                         "exclusiveMaximum", "multipleOf", "minLength",
                         "maxLength", "maxItems"}


def walk(schema, path="$"):
    """Yield (path, subschema) for every schema object in the tree."""
    if not isinstance(schema, dict):
        return
    yield path, schema
    for name, sub in schema.get("properties", {}).items():
        yield from walk(sub, f"{path}.{name}")
    if isinstance(schema.get("items"), dict):
        yield from walk(schema["items"], f"{path}[]")
    for key in ("anyOf", "allOf", "oneOf"):
        for i, sub in enumerate(schema.get(key, [])):
            yield from walk(sub, f"{path}.{key}[{i}]")
    for name, sub in schema.get("$defs", {}).items():
        yield from walk(sub, f"$defs.{name}")


def lint(schema):
    anthropic, openai = [], []
    for path, node in walk(schema):
        if "properties" in node and node.get("type") != "object":
            problem = f'{path}: has properties but no "type": "object"'
            anthropic.append(problem)
            openai.append(problem)
        if node.get("type") == "object":
            if node.get("additionalProperties") is not False:
                anthropic.append(f"{path}: additionalProperties must be false")
                openai.append(f"{path}: additionalProperties must be false")
            props = set(node.get("properties", {}))
            missing = sorted(props - set(node.get("required", [])))
            if missing:
                openai.append(f"{path}: not in required: {', '.join(missing)}")
        for key in sorted(ANTHROPIC_UNSUPPORTED & set(node)):
            anthropic.append(f"{path}: '{key}' is not supported")
        if node.get("minItems", 0) > 1:
            anthropic.append(f"{path}: minItems above 1 is not supported")
        ref = node.get("$ref", "")
        if ref.startswith("http"):
            anthropic.append(f"{path}: external $ref is not supported")
        if ref == "#":
            anthropic.append(f"{path}: recursive schema is not supported")
    return {"anthropic": anthropic, "openai": openai,
            "ok": not anthropic and not openai}


def load_schema(path):
    """Read a schema file. Returns (schema, None) or (None, error message).

    Accepts UTF-8 (with or without a byte-order mark) and UTF-16, which is
    what Windows PowerShell 5.1 writes when you redirect output with >.
    """
    raw = open(path, "rb").read()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        text = raw.decode("utf-16")
    else:
        text = raw.decode("utf-8-sig")
    try:
        return json.loads(text), None
    except json.JSONDecodeError as error:
        return None, (f"not valid JSON: {error.msg} at line {error.lineno}, "
                      f"column {error.colno}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"error": "usage: python schema_lint.py schema.json"}))
        sys.exit(2)
    schema, problem = load_schema(sys.argv[1])
    if problem:
        print(json.dumps({"error": problem}))
        sys.exit(2)
    report = lint(schema)
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["ok"] else 1)
