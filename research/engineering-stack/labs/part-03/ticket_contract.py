"""The ticket-routing contract: one JSON Schema plus a small validator.

The validator covers only the keywords this schema uses (type, enum,
properties, required, additionalProperties). It is a teaching aid; in real
work use a full validator such as Pydantic or jsonschema.
"""
import json

TICKET_SCHEMA = {
    "type": "object",
    "properties": {
        "queue": {"type": "string", "enum": ["billing", "shipping", "account"]},
        "priority": {"type": "string", "enum": ["low", "normal", "urgent"]},
        "summary": {"type": "string"},
    },
    "required": ["queue", "priority", "summary"],
    "additionalProperties": False,
}

TYPES = {"object": dict, "string": str, "integer": int, "boolean": bool, "array": list}


def validate(value, schema, path="$"):
    """Return a list of error strings; an empty list means valid."""
    errors = []
    expected = TYPES.get(schema.get("type"))
    if expected and not isinstance(value, expected):
        return [f"{path}: expected {schema['type']}, got {type(value).__name__}"]
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} is not one of {schema['enum']}")
    if schema.get("type") == "object":
        props = schema.get("properties", {})
        for name in schema.get("required", []):
            if name not in value:
                errors.append(f"{path}: missing required field {name!r}")
        if schema.get("additionalProperties") is False:
            for name in value:
                if name not in props:
                    errors.append(f"{path}: unexpected field {name!r}")
        for name, sub in props.items():
            if name in value:
                errors.extend(validate(value[name], sub, f"{path}.{name}"))
    return errors


def parse_and_validate(text):
    """Parse model text as JSON, then validate it. Returns (data, errors)."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        return None, [f"$: not valid JSON ({error.msg} at character {error.pos})"]
    return data, validate(data, TICKET_SCHEMA)


if __name__ == "__main__":
    print(json.dumps(TICKET_SCHEMA, indent=2))
