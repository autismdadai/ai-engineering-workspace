"""Package the Planetary Council plugin and the standalone skills for upload to claude.ai.

    python tools/package_for_claude_ai.py

Writes to dist/claude-ai/ (zips are git-ignored):
  planetary-council-system.zip   the plugin folder's contents, with
                                 .claude-plugin/plugin.json at the top, for
                                 Customize > Plugins > Add > Upload plugin
  <skill>.zip                    one skill folder at the top of the archive, for
                                 Customize > Skills; only SKILL.md, scripts/,
                                 references/ and assets/ go in (evals/ holds test
                                 material with known wrong answers, so it stays out)

claude.ai's help article caps a skill description at 200 characters, and the
first upload (October 21, 2026) kept the plugin but none of its skills, whose
descriptions ran 335 to 727 characters [T]. So each packaged SKILL.md gets the
short description from metadata.claude-app-description in place of its long
one; the files in the workspace keep the long description for Claude Code. A
skill whose description is over 200 characters and has no short one fails the
build.

Skips the standalone skills the plugin already carries, so claude.ai doesn't get
two skills with one name. Standard library only; writes only inside dist/claude-ai/.
"""
import json
import pathlib
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "planetary-council"
OUT = ROOT / "dist" / "claude-ai"
SKILL_PARTS = ("scripts", "references", "assets")
ZIP_TIME = (2026, 1, 1, 0, 0, 0)  # fixed, so the same files always give the same archive
LIMIT = 200


def field(lines, key, indent=0):
    """A frontmatter value: one line, quoted, or a folded (>) / literal (|) block."""
    prefix = " " * indent + key + ":"
    for i, line in enumerate(lines):
        if line.startswith(prefix):
            value = line[len(prefix):].strip()
            if value[:1] in (">", "|"):
                body = []
                for nxt in lines[i + 1:]:
                    if nxt.strip() and len(nxt) - len(nxt.lstrip()) <= indent:
                        break
                    if nxt.strip():
                        body.append(nxt.strip())
                return (" " if value[0] == ">" else "\n").join(body)
            return json.loads(value) if value[:1] == '"' else value.strip("'")
    return None


def short_skill_md(skill_md):
    """Return (SKILL.md text with the short description swapped in, problem or None)."""
    text = skill_md.read_bytes().decode("utf-8")
    front, rest = text[4:].split("\n---\n", 1)
    lines = front.split("\n")
    short = field(lines, "claude-app-description", indent=2)
    if not short:
        if 0 < len(field(lines, "description") or "") <= LIMIT:
            return text, None  # already short enough for claude.ai
        return text, "description over 200 characters and no metadata.claude-app-description"
    if len(short) > LIMIT:
        return text, f"claude-app-description is {len(short)} characters"
    out, i, done = [], 0, False
    while i < len(lines):
        if not done and lines[i].startswith("description:"):
            out.append("description: " + json.dumps(short, ensure_ascii=False))
            i += 1
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                i += 1  # skip the long value's continuation lines
            done = True
            continue
        out.append(lines[i])
        i += 1
    if field(out, "description") != short:
        return text, "the swapped description doesn't read back"
    return "---\n" + "\n".join(out) + "\n---\n" + rest, None


def write_zip(path, entries):
    """entries: (archive name, bytes). Folder entries are added for every parent."""
    folders = sorted({str(pathlib.PurePosixPath(name).parents[k]) + "/"
                      for name, _ in entries
                      for k in range(len(pathlib.PurePosixPath(name).parents) - 1)})
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for folder in folders:
            info = zipfile.ZipInfo(folder, date_time=ZIP_TIME)
            info.external_attr = (0o40755 << 16) | 0x10
            zf.writestr(info, b"")
        for name, data in entries:
            info = zipfile.ZipInfo(name, date_time=ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, data)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    problems = []

    def entry(name, path):
        if path.name == "SKILL.md":
            text, problem = short_skill_md(path)
            if problem:
                problems.append(f"{path.parent.relative_to(ROOT).as_posix()}: {problem}")
            return name, text.encode("utf-8")
        return name, path.read_bytes()

    plugin_files = [p for p in sorted(PLUGIN.rglob("*"))
                    if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"]
    write_zip(OUT / "planetary-council-system.zip",
              [entry(p.relative_to(PLUGIN).as_posix(), p) for p in plugin_files])
    plugin_skills = {p.parent.name for p in PLUGIN.glob("skills/*/SKILL.md")}

    skipped = []
    for skill_md in sorted(ROOT.glob("skills/*/SKILL.md")):
        folder = skill_md.parent
        if folder.name.startswith("_"):
            continue
        if folder.name in plugin_skills:
            skipped.append(folder.name)
            continue
        files = [skill_md] + [p for p in sorted(folder.rglob("*"))
                              if p.is_file() and p.relative_to(folder).parts[0] in SKILL_PARTS
                              and "__pycache__" not in p.parts]
        write_zip(OUT / f"{folder.name}.zip",
                  [entry(f"{folder.name}/{p.relative_to(folder).as_posix()}", p) for p in files])

    ok = not problems
    for archive in sorted(OUT.glob("*.zip")):
        with zipfile.ZipFile(archive) as zf:
            names = zf.namelist()
            sound = zf.testzip() is None
            skill_files = [n for n in names if n.endswith("SKILL.md")]
            lengths = [len(field(zf.read(n).decode("utf-8")[4:].split("\n---\n", 1)[0].split("\n"),
                                 "description") or "") for n in skill_files]
        stem = archive.stem
        if stem == "planetary-council-system":
            shape = names.count(".claude-plugin/plugin.json") == 1
        else:
            shape = f"{stem}/SKILL.md" in names and all(n.startswith(stem + "/") for n in names)
        short = all(0 < n <= LIMIT for n in lengths)
        ok = ok and sound and shape and short
        print(f"{'OK  ' if sound and shape and short else 'FAIL'} {archive.relative_to(ROOT).as_posix()}: "
              f"{len(names) - sum(n.endswith('/') for n in names)} files, {len(skill_files)} skills, "
              f"longest description {max(lengths, default=0)} characters, {archive.stat().st_size:,} bytes")
    print("Not packaged (the plugin already carries them): " + (", ".join(skipped) or "none"))
    for problem in problems:
        print("FAIL " + problem)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
