"""Check a skill folder's SKILL.md front matter, standard library only.

Rules from the Agent Skills specification (agentskills.io): name 1 to 64
characters of lowercase letters, digits and hyphens, no hyphen at either end,
no two hyphens in a row, the same as the folder name; description 1 to 1024
characters; compatibility at most 500 characters.

Two optional product profiles add rules that are not in the open spec:
  claude-api  name must not contain "anthropic" or "claude", and no XML tags
              in name or description (Claude API docs)
  claude-app  description at most 200 characters, for skills uploaded to the
              Claude app (Claude help center)

Usage: python skill_check.py FOLDER [--profile claude-api|claude-app]
"""
import json
import pathlib
import re
import sys

NAME_MAX, DESCRIPTION_MAX, COMPATIBILITY_MAX, APP_DESCRIPTION_MAX = 64, 1024, 500, 200
NAME_CHARS = re.compile(r"^[a-z0-9-]+$")
XML_TAG = re.compile(r"<[^>]+>")


def read_front_matter(text):
    """Parse simple 'key: value' front matter between two '---' lines.

    Enough for the flat fields checked here; a nested 'metadata:' map is read
    as indented 'key: value' lines. Not a full YAML parser.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with a '---' line")
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        raise ValueError("front matter has no closing '---' line") from None
    fields, current_map = {}, None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) and current_map is not None:
            key, _, value = line.strip().partition(":")
            fields[current_map][key.strip()] = value.strip().strip("\"'")
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise ValueError(f"cannot read front matter line: {line!r}")
        key, value = key.strip(), value.strip()
        if value == "":
            fields[key], current_map = {}, key
        else:
            fields[key], current_map = value.strip("\"'"), None
    return fields, "\n".join(lines[end + 1:])


def check_skill(folder, profile=None):
    """Return a list of problems (empty means the skill passes)."""
    folder = pathlib.Path(folder)
    path = folder / "SKILL.md"
    if not path.is_file():
        return ["no SKILL.md in the folder"]
    try:
        fields, body = read_front_matter(path.read_text(encoding="utf-8"))
    except ValueError as error:
        return [str(error)]
    problems = []
    name = fields.get("name")
    description = fields.get("description")
    if not isinstance(name, str) or not name:
        problems.append("name is required")
    else:
        if len(name) > NAME_MAX:
            problems.append(f"name is {len(name)} characters; the limit is {NAME_MAX}")
        if not NAME_CHARS.match(name):
            problems.append("name may only use lowercase letters, digits and hyphens")
        if name.startswith("-") or name.endswith("-"):
            problems.append("name must not start or end with a hyphen")
        if "--" in name:
            problems.append("name must not contain two hyphens in a row")
        if name != folder.name:
            problems.append(f"name '{name}' does not match the folder '{folder.name}'")
    if not isinstance(description, str) or not description:
        problems.append("description is required")
    elif len(description) > DESCRIPTION_MAX:
        problems.append(f"description is {len(description)} characters; the limit is {DESCRIPTION_MAX}")
    compatibility = fields.get("compatibility")
    if isinstance(compatibility, str) and len(compatibility) > COMPATIBILITY_MAX:
        problems.append(f"compatibility is {len(compatibility)} characters; the limit is {COMPATIBILITY_MAX}")
    if "metadata" in fields and not isinstance(fields["metadata"], dict):
        problems.append("metadata must be a map of keys to strings")

    if profile == "claude-api":
        if isinstance(name, str) and re.search(r"anthropic|claude", name):
            problems.append("claude-api: name must not contain 'anthropic' or 'claude'")
        for field in ("name", "description"):
            if isinstance(fields.get(field), str) and XML_TAG.search(fields[field]):
                problems.append(f"claude-api: {field} must not contain XML tags")
    elif profile == "claude-app":
        if isinstance(description, str) and len(description) > APP_DESCRIPTION_MAX:
            problems.append(f"claude-app: description is {len(description)} characters; "
                            f"the app limit is {APP_DESCRIPTION_MAX}")
    elif profile is not None:
        problems.append(f"unknown profile {profile!r}")

    if len(body.splitlines()) > 500:
        problems.append("advice: the spec suggests keeping SKILL.md under 500 lines")
    return problems


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    profile = None
    if "--profile" in argv:
        i = argv.index("--profile")
        profile = argv[i + 1] if i + 1 < len(argv) else ""
        argv = argv[:i] + argv[i + 2:]
    problems = check_skill(argv[0], profile)
    print(json.dumps({"folder": argv[0], "profile": profile, "ok": not problems,
                      "problems": problems}, indent=2))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
