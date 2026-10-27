#!/usr/bin/env python3
"""Check an Agent Skill folder and build the packages each host needs.

Usage:
  python skills/build_skill.py skills/quantum-entanglement-lab --out dist

Outputs, in --out:
  <name>.zip              The skill folder with its spec description (up to 1,024
                          characters), for Claude Code and other hosts that load
                          skill folders.
  <name>-claude-app.zip   The same folder with the short description from
                          metadata.claude-app-description (up to 200 characters),
                          for uploading where that limit applies.
  <name>.single-file.md   One SKILL.md with the short description and the skill's
                          other files bundled at the end, for hosts that save only
                          SKILL.md (such as the Claude app's save card).

Only SKILL.md, scripts/, references/ and assets/ are packaged. Everything else,
including evals/ (test material with known wrong answers), is left out and listed.

Checks: the agentskills.io name rules (1-64 characters; lowercase letters, digits
and single hyphens; matching the folder), description lengths, no angle brackets
in descriptions, SKILL.md under 500 lines, and that every bundled file reads back
byte for byte from the single-file version.

Output: JSON. Exit code 0 when every check passes, 1 when any fails, 2 on a setup
error. Needs PyYAML. Writes only inside --out; no network, no prompts.
"""
import argparse
import hashlib
import json
import pathlib
import re
import sys
import zipfile

try:
    import yaml
except ImportError:
    print(json.dumps({"error": "PyYAML is required: pip install pyyaml"}))
    sys.exit(2)

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
BUNDLE_DIRS = ("scripts", "references", "assets")
LANG = {".py": "python", ".md": "markdown", ".json": "json", ".sh": "bash"}
ZIP_TIME = (2026, 1, 1, 0, 0, 0)  # fixed, so the same files always give the same archive


def split_skill(text: str) -> tuple[str, str]:
    """Return (frontmatter, body) of a SKILL.md."""
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with a '---' line")
    end = text.find("\n---\n", 3)
    if end == -1:
        raise ValueError("the frontmatter has no closing '---' line")
    return text[4:end + 1], text[end + 5:]


def replace_description(front: str, new_desc: str) -> str:
    """Swap the top-level description, keeping the rest of the frontmatter as written."""
    lines = front.splitlines(keepends=True)
    out, i, done = [], 0, False
    while i < len(lines):
        if not done and lines[i].startswith("description:"):
            out.append("description: " + json.dumps(new_desc, ensure_ascii=False) + "\n")
            i += 1
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                i += 1  # skip the old value's continuation lines
            done = True
            continue
        out.append(lines[i])
        i += 1
    if not done:
        raise ValueError("no top-level description in the frontmatter")
    return "".join(out)


def bundled_files(skill_dir: pathlib.Path) -> list[pathlib.Path]:
    files = []
    for top in BUNDLE_DIRS:
        root = skill_dir / top
        if root.is_dir():
            for path in sorted(root.rglob("*")):
                rel = path.relative_to(skill_dir)
                hidden = any(part.startswith(".") or part == "__pycache__" for part in rel.parts)
                if path.is_file() and not hidden:
                    files.append(rel)
    return files


def write_zip(path: pathlib.Path, name: str, skill_md: str, skill_dir: pathlib.Path, files) -> None:
    entries = [("SKILL.md", skill_md.encode("utf-8"))]
    entries += [(rel.as_posix(), (skill_dir / rel).read_bytes()) for rel in files]
    dirs = sorted({f"{name}/"} | {f"{name}/{p}/" for arc, _ in entries
                                   for p in [str(pathlib.PurePosixPath(arc).parent)] if p != "."})
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for d in dirs:
            info = zipfile.ZipInfo(d, date_time=ZIP_TIME)
            info.external_attr = (0o40755 << 16) | 0x10
            zf.writestr(info, b"")
        for arc, data in entries:
            info = zipfile.ZipInfo(f"{name}/{arc}", date_time=ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if arc.startswith("scripts/") else 0o644) << 16
            zf.writestr(info, data)


def single_file(skill_md: str, skill_dir: pathlib.Path, files) -> str:
    parts = [skill_md.rstrip("\n") + "\n\n## Bundled files\n\n"
             "This single-file copy carries the skill's other files. Before following the steps "
             "above, recreate each file below at the path shown, relative to one working folder, "
             "copying the block exactly, and run the commands from that folder. To confirm a copy, "
             "compare `sha256sum <path>` with the value given.\n"]
    for rel in files:
        data = (skill_dir / rel).read_bytes()
        text = data.decode("utf-8")
        longest = max((len(run) for run in re.findall(r"`+", text)), default=0)
        fence = "`" * max(3, longest + 1)  # longer than any backtick run inside the file
        tail = "" if text.endswith("\n") else "\n"
        parts.append(f"\n### `{rel.as_posix()}`\n\nSHA-256 {hashlib.sha256(data).hexdigest()}, "
                     f"{len(data)} bytes\n\n{fence}{LANG.get(rel.suffix, '')}\n{text}{tail}{fence}\n")
    return "".join(parts)


def read_back(single: str, rel: pathlib.Path):
    """Extract one bundled file's block from the single-file text, or None."""
    head = re.search(r"\n### `" + re.escape(rel.as_posix()) +
                     r"`\n\nSHA-256 [0-9a-f]{64}, \d+ bytes\n\n(`{3,})[a-z]*\n", single)
    if not head:
        return None
    fence, start = head.group(1), head.end()
    end = single.find("\n" + fence + "\n", start - 1)
    return None if end == -1 else single[start:end + 1]


def describe(path: pathlib.Path) -> dict:
    data = path.read_bytes()
    return {"file": path.name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a skill folder and build its packages.")
    parser.add_argument("skill_dir", help="the skill folder, holding SKILL.md")
    parser.add_argument("--out", required=True, help="folder for the packages")
    args = parser.parse_args()
    skill_dir, out = pathlib.Path(args.skill_dir).resolve(), pathlib.Path(args.out).resolve()

    if not (skill_dir / "SKILL.md").is_file():
        print(json.dumps({"error": f"no SKILL.md in {skill_dir}"}))
        return 2
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    try:
        front, body = split_skill(text)
        meta = yaml.safe_load(front)
        if not isinstance(meta, dict):
            raise ValueError("the frontmatter is not a mapping")
    except (ValueError, yaml.YAMLError) as exc:
        print(json.dumps({"error": f"cannot read the frontmatter: {exc}"}))
        return 2

    checks = []

    def check(label, ok, detail=""):
        checks.append({"check": label, "ok": bool(ok), "detail": detail})

    name = meta.get("name") if isinstance(meta.get("name"), str) else ""
    desc = meta.get("description").strip() if isinstance(meta.get("description"), str) else ""
    app = (meta.get("metadata") or {}).get("claude-app-description")
    app = app.strip() if isinstance(app, str) else None

    check("name follows the spec", 1 <= len(name) <= 64 and NAME_RE.match(name), name)
    check("name matches the folder", name == skill_dir.name, f"{name} / {skill_dir.name}")
    check("description is 1-1,024 characters", 1 <= len(desc) <= 1024, f"{len(desc)} characters")
    check("description has no angle brackets", not re.search(r"[<>]", desc))
    lines = len(text.splitlines())
    check("SKILL.md is under 500 lines", lines < 500, f"{lines} lines")

    files = bundled_files(skill_dir)
    left_out = sorted(p.name + ("/" if p.is_dir() else "") for p in skill_dir.iterdir()
                      if p.name != "SKILL.md" and p.name not in BUNDLE_DIRS)
    out.mkdir(parents=True, exist_ok=True)
    built = [out / f"{name}.zip"]
    write_zip(built[0], name, text, skill_dir, files)

    if app is None:
        check("metadata.claude-app-description is present", False,
              "add it to build the Claude app versions")
    else:
        check("app description is 1-200 characters", 1 <= len(app) <= 200, f"{len(app)} characters")
        check("app description has no angle brackets", not re.search(r"[<>]", app))
        short_front = replace_description(front, app)
        again = yaml.safe_load(short_front)
        same_rest = {k: v for k, v in again.items() if k != "description"} == \
                    {k: v for k, v in meta.items() if k != "description"}
        check("app frontmatter re-reads with only the description changed",
              again.get("description") == app and same_rest)
        short_md = "---\n" + short_front + "---\n" + body
        built.append(out / f"{name}-claude-app.zip")
        write_zip(built[-1], name, short_md, skill_dir, files)
        single = single_file(short_md, skill_dir, files)
        check("single-file version is under 500 lines", len(single.splitlines()) < 500,
              f"{len(single.splitlines())} lines")
        bad = [rel.as_posix() for rel in files
               if (read_back(single, rel) or "").encode("utf-8") != (skill_dir / rel).read_bytes()]
        check("every bundled file reads back byte for byte", not bad, ", ".join(bad) or f"{len(files)} files")
        built.append(out / f"{name}.single-file.md")
        built[-1].write_text(single, encoding="utf-8")

    for path in built:
        if path.suffix == ".zip":
            with zipfile.ZipFile(path) as zf:
                check(f"{path.name} opens cleanly", zf.testzip() is None, f"{len(zf.namelist())} entries")

    ok = all(c["ok"] for c in checks)
    print(json.dumps({"skill": name, "description_chars": len(desc),
                      "app_description_chars": None if app is None else len(app),
                      "bundled": [rel.as_posix() for rel in files], "left_out": left_out,
                      "checks": checks, "outputs": [describe(p) for p in built],
                      "result": "PASS" if ok else "FAIL"}, ensure_ascii=False, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
