"""Checks that the workspace's pages agree with the files and git.

    python tools/check_workspace.py

The same facts are copied by hand into several pages (counts, versions,
descriptions), and copies drift. This script checks those facts against the
source. Run it before a commit.

1. Commit hashes named in the README exist in git.
2. The plugin's skill and agent counts match its README; its version matches
   the root README.
3. Each Codex entry in .agents/skills/ links to a canonical SKILL.md that exists,
   and carries the same description.
4. Every skill the packager uploads to claude.ai has a short description of
   200 characters or fewer (claude.ai drops longer ones).
5. The plugin's shared/ files are identical in every skill that bundles them.

This is the public version. The private workspace's checker also compares the
desktop app's copy of the plugin and its own decision pages, which exist only
on the owner's computer.

Standard library only. Reads files and runs read-only git commands; writes
nothing. Exit code 1 if any check fails.
"""
import collections
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "planetary-council"
STATUS_PAGES = ["README.md"]

results = []


def report(level, message):
    results.append(level)
    print(f"{level:4}  {message}")


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")


def check_commits():
    for page in STATUS_PAGES:
        text = (ROOT / page).read_text(encoding="utf-8")
        hashes = {h for h in re.findall(r"`([0-9a-f]{7,10})`", text) if re.search(r"\d", h) and re.search(r"[a-f]", h)}
        missing = sorted(h for h in hashes if git("cat-file", "-e", h + "^{commit}").returncode)
        if missing:
            report("FAIL", f"{page}: no such commit {', '.join(missing)}")
        else:
            report("OK", f"{page}: {len(hashes)} commit hashes all exist")


def check_plugin_counts():
    readme = (PLUGIN / "README.md").read_text(encoding="utf-8")
    skills = len([p for p in (PLUGIN / "skills").glob("*/SKILL.md")])
    agents = len(list((PLUGIN / "agents").glob("*.md")))
    for name, actual in (("Skills", skills), ("Agents", agents)):
        m = re.search(rf"\*\*{name} \((\d+)\):\*\*", readme)
        claimed = int(m.group(1)) if m else None
        report("OK" if claimed == actual else "FAIL", f"plugin README says {name} ({claimed}); folder has {actual}")
    version = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    report("OK" if f"version {version}" in root_readme else "FAIL", f"plugin.json version {version}; root README names it: {f'version {version}' in root_readme}")


def check_codex_entries():
    entries = sorted((ROOT / ".agents" / "skills").glob("*/SKILL.md"))
    broken, drifted = [], []
    for entry in entries:
        text = entry.read_text(encoding="utf-8")
        m = re.search(r"\[canonical skill\]\(([^)]+)\)", text)
        target = (entry.parent / m.group(1)).resolve() if m else None
        if not target or not target.is_file():
            broken.append(entry.parent.name)
        elif description(text) != description(target.read_text(encoding="utf-8")):
            drifted.append(entry.parent.name)
    if broken:
        report("FAIL", f".agents/skills: broken canonical links: {', '.join(broken)}")
    else:
        report("OK", f".agents/skills: {len(entries)} entries, every canonical link resolves")
    report("WARN" if drifted else "OK", ".agents/skills descriptions that differ from their canonical skill: "
           + (", ".join(drifted) or "none"))


def description(text):
    """The front matter's description, joined onto one line (handles '>' folded blocks)."""
    fm = re.match(r"\A---\r?\n(.*?)\r?\n---", text, flags=re.S)
    m = re.search(r"^description:[ \t]*(.*?)(?=^\S|\Z)", fm.group(1) + "\n" if fm else "", flags=re.S | re.M)
    if not m:
        return None
    value = re.sub(r"^[>|][-+]?\s*", "", m.group(1).strip())
    return " ".join(value.split()).strip("\"'")


def front_matter_value(text, key):
    m = re.search(rf"^\s*{key}:\s*(.+)$", text, flags=re.M)
    return m.group(1).strip().strip("\"'") if m else None


def check_short_descriptions():
    # Same set the packager uploads: the plugin's skills, plus standalone skills the plugin doesn't carry
    plugin_skills = sorted(PLUGIN.glob("skills/*/SKILL.md"))
    carried = {p.parent.name for p in plugin_skills}
    paths = plugin_skills + [p for p in sorted(ROOT.glob("skills/*/SKILL.md")) if p.parent.name not in carried]
    bad = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        short = front_matter_value(text, "claude-app-description")
        if short is None or len(short) > 200:
            bad.append(f"{path.relative_to(ROOT).as_posix()} ({'missing' if short is None else len(short)})")
    if bad:
        report("WARN", "short description missing or over 200 characters: " + "; ".join(bad))
    else:
        report("OK", f"{len(paths)} skills have a short description of 200 characters or fewer")


def check_shared_copies():
    groups = collections.defaultdict(set)
    for path in PLUGIN.glob("skills/*/shared/**/*"):
        if path.is_file():
            rel = "/".join(path.relative_to(PLUGIN / "skills").parts[1:])  # drop the skill's own folder name
            groups[rel].add(hashlib.sha256(path.read_bytes()).hexdigest())
    differ = sorted(rel for rel, digests in groups.items() if len(digests) > 1)
    if differ:
        report("WARN", f"plugin shared/ files that differ between skills: {', '.join(differ)}")
    else:
        report("OK", f"plugin shared/: {len(groups)} files, identical in every skill that bundles them")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"Workspace check, HEAD {git('rev-parse', '--short', 'HEAD').stdout.strip()}\n")
    for check in (check_commits, check_plugin_counts, check_codex_entries, check_short_descriptions,
                  check_shared_copies):
        check()
    counts = collections.Counter(results)
    print(f"\n{counts['OK']} OK, {counts['WARN']} WARN, {counts['FAIL']} FAIL")
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
