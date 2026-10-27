#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:[a-z0-9-]*[a-z0-9]+)?$")

def extract_frontmatter(text: str):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "frontmatter does not start on line 1"
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, "frontmatter closing delimiter not found"
    fields = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return None, f"unparseable frontmatter line: {line}"
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip("'").strip('"')
    return fields, None

def audit(skill_dir: Path):
    errors, warnings = [], []
    skill_dir = skill_dir.resolve()
    skill_file = skill_dir / "SKILL.md"
    if not skill_dir.is_dir(): return ["skill directory not found"], []
    if not skill_file.is_file(): return ["SKILL.md not found"], []
    
    text = skill_file.read_text(encoding="utf-8", errors="replace")
    fields, fm_error = extract_frontmatter(text)
    if fm_error:
        errors.append(fm_error)
        fields = {}
        
    name = fields.get("name", "")
    desc = fields.get("description", "")
    
    if not name: errors.append("name is missing")
    else:
        if len(name) > 64: errors.append("name exceeds 64 characters")
        if "--" in name: errors.append("name contains consecutive hyphens")
        if not NAME_RE.fullmatch(name): errors.append("name contains invalid characters or hyphen placement")
        if name != skill_dir.name: errors.append("name does not match the Skill folder name")
        
    if not desc: errors.append("description is missing")
    elif len(desc) > 1024: errors.append("description exceeds 1024 characters")
    
    lines = text.splitlines()
    if len(lines) > 500: warnings.append(f"SKILL.md is {len(lines)} lines; keep it under 500 where practical")
    if "\\" in text: warnings.append("backslashes found; review path portability")
    
    absolute_patterns = [r"(?m)^\s*/Users/", r"(?m)^\s*/home/", r"(?m)^\s*/root/", r"[A-Za-z]:[\\/]+"]
    for pat in absolute_patterns:
        if re.search(pat, text):
            warnings.append("possible absolute path found")
            break
            
    if re.search(r"(?i)\b(password|api[_]?key|secret|token)\s*[:=]\s*['\"][^\"]+", text):
        warnings.append("possible hardcoded credential; inspect manually")
        
    return errors, warnings

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_dir")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    
    errors, warnings = audit(Path(args.skill_dir))
    result = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"STATUS: {result['status']}")
        for e in errors: print(f"ERROR: {e}", file=sys.stderr)
        for w in warnings: print(f"WARNING: {w}", file=sys.stderr)
    return 0 if not errors else 3

if __name__ == "__main__":
    sys.exit(main())
