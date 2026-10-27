#!/usr/bin/env bash
set -euo pipefail
usage() {
cat <<EOF
Usage: validate_skill.sh PATH
Checks a portable Agent Skill directory for:
- SKILL.md existence
- frontmatter on line 1
- name/folder agreement
- name syntax
- description presence and length
- SKILL.md line count
- obvious absolute/backslash paths
Exit codes:
0  pass
2  usage error
3  validation failure
EOF
}
[[ "${1:-}" == "--help" ]] && { usage; exit 0; }
[ $# -eq 1 ] || { usage >&2; exit 2; }
SKILL_DIR="$1"
FILE="$SKILL_DIR/SKILL.md"
fail=0

[[ -d "$SKILL_DIR" ]] || { echo '{"error": "skill directory not found"}' >&2; exit 3; }
[[ -f "$FILE" ]] || { echo '{"error": "SKILL.md not found"}' >&2; exit 3; }
first_line="$(head -n 1 "$FILE")"
[[ "$first_line" == "---" ]] || { echo '{"error": "frontmatter must start on line 1"}' >&2; fail=1; }

folder="$(basename "$SKILL_DIR")"
name="$(awk 'NR==1 {in_fm=1; next} in_fm && $0=="---" {exit} in_fm && /^name:/ {sub(/^name:[[:space:]]*/, "", $0); print $0; exit}' "$FILE")"
desc="$(awk 'NR==1 {in_fm=1; next} in_fm && $0=="---" {exit} in_fm && /^description:/ {sub(/^description:[[:space:]]*/, "", $0); print $0; exit}' "$FILE")"

[[ -n "$name" ]] || { echo '{"error": "name missing"}' >&2; fail=1; }
[[ "$name" == "$folder" ]] || { echo "{\"error\": \"name '$name' does not match folder '$folder'\"}" >&2; fail=1; }

if [[ -n "$name" ]] && ! [[ "$name" =~ ^[a-z0-9]+([a-z0-9-]*[a-z0-9]+)?$ ]]; then
    echo '{"error": "name contains invalid characters or hyphen placement"}' >&2
    fail=1
fi

if [[ -n "$name" ]] && [[ ${#name} -gt 64 || "$name" == *--* ]]; then
    echo '{"error": "name exceeds 64 chars or contains consecutive hyphens"}' >&2
    fail=1
fi

if [[ -z "$desc" ]]; then
    echo '{"error": "description missing"}' >&2
    fail=1
elif [[ ${#desc} -gt 1024 ]]; then
    echo '{"error": "description exceeds 1024 characters"}' >&2
    fail=1
fi

lines="$(wc -l < "$FILE" | tr -d ' ')"
if ((lines > 500)); then
    echo "{\"warning\": \"SKILL.md is $lines lines; specification recommends keeping it under 500\"}" >&2
fi

if grep -nE '(^|[[:space:]])([A-Za-z]:\\|/Users/|/home/|/root/|[A-Za-z]:/)' "$FILE" >/dev/null 2>&1; then
    echo '{"warning": "possible absolute or Windows-style path found; review portability"}' >&2
fi

printf '{"skill": "%s", "name": "%s", "description_length": %d, "lines": %d, "status": "%s"}\n' \
    "$SKILL_DIR" "$name" "${#desc}" "$lines" "$([[ $fail -eq 0 ]] && echo PASS || echo FAIL)"
((fail == 0)) || exit 3
