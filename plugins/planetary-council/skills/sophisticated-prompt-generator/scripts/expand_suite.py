#!/usr/bin/env python3
"""CLI entry point for deterministic expansion of a full 50-prompt suite."""

import sys
from pathlib import Path

# Allow running from scripts/ or project root
sys.path.insert(0, str(Path(__file__).resolve().parent / "expanders"))

from topic_templates import expand_all, skeletons_to_markdown

def main():
    import argparse
    p = argparse.ArgumentParser(description="Expand seed → 50-prompt suite (deterministic)")
    p.add_argument("seed", nargs="?", help="Seed question / goal")
    p.add_argument("--fill", action="store_true", default=True, help="Fill deterministic drafts (default True)")
    p.add_argument("--skeletons-only", action="store_true", help="Emit structure only, no drafts")
    p.add_argument("-o", "--output", help="Output Markdown path")
    p.add_argument("--json", action="store_true", help="Also emit JSON of skeletons")
    args = p.parse_args()

    if not args.seed:
        print("Usage: expand_suite.py \"your seed question\" [-o suite.md]", file=sys.stderr)
        sys.exit(2)

    fill = args.fill and not args.skeletons_only
    sks = expand_all(args.seed, fill_draft=fill)
    md = skeletons_to_markdown(sks, args.seed)

    if args.output:
        Path(args.output).write_text(md, encoding="utf-8")
        print(f"Wrote {len(sks)} prompts to {args.output}")
    else:
        print(md)

    if args.json and args.output:
        import json
        from topic_templates import PromptSkeleton
        jpath = Path(args.output).with_suffix(".json")
        jpath.write_text(json.dumps([s.to_dict() for s in sks], indent=2), encoding="utf-8")
        print(f"Also wrote JSON to {jpath}")

if __name__ == "__main__":
    main()
