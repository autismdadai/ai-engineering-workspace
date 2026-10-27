#!/usr/bin/env bash
set -euo pipefail
usage() {
cat <<EOF
Usage: package_skill.sh SKILL_DIR OUTPUT.zip [--dry-run]
Validates a Skill directory, then creates a zip containing the Skill folder.
The script does not upload, install, or execute the Skill.
EOF
}
[[ "${1:-}" == "--help" ]] && { usage; exit 0; }
[ $# -ge 2 ] && [ $# -le 3 ] || { usage >&2; exit 2; }

SKILL_DIR="$1"
OUTPUT="$2"
DRY_RUN="${3:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/validate_skill.sh" "$SKILL_DIR" >/dev/null
parent="$(cd "$(dirname "$SKILL_DIR")" && pwd)"
folder="$(basename "$SKILL_DIR")"

if [[ "$DRY_RUN" == "--dry-run" ]]; then
    printf '{"action": "package", "source": "%s", "output": "%s", "status": "DRY_RUN"}\n' "$SKILL_DIR" "$OUTPUT"
    exit 0
fi

mkdir -p "$(dirname "$OUTPUT")"
rm -f "$OUTPUT"
(
    cd "$parent"
    zip -qr "$OUTPUT" "$folder"
)
printf '{"source": "%s", "output": "%s", "status": "PACKAGED"}\n' "$SKILL_DIR" "$OUTPUT"
