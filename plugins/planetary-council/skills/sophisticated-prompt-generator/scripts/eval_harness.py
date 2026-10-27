#!/usr/bin/env python3
"""
Automated eval harness for sophisticated-prompt-generator suites.

Capabilities:
1. Structural validation (delegates to validate_suite.py logic)
2. Heuristic quality scoring (residue handling, success-check quality,
   axis coverage, uniqueness, length sanity, Topic-10 depth)
3. Optional "real model" interface stub — ready for injection of an
   external LLM judge or API (OpenAI, Anthropic, local, etc.)
4. Produces a machine-readable JSON report + human summary

This harness is deterministic for the structural + heuristic layers.
The real-model layer is deliberately pluggable so the same suite can be
scored against different models without changing the rest of the pipeline.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Callable, Optional

# ---------------------------------------------------------------------------
# Structural checks (mirrors validate_suite.py)
# ---------------------------------------------------------------------------

REQUIRED_TOPICS = 10
PROMPTS_PER_TOPIC = 5
TOTAL_PROMPTS = 50

def structural_checks(text: str) -> list[str]:
    errors = []
    topic_headers = re.findall(r"^## Topic \d+ —", text, re.MULTILINE)
    if len(topic_headers) != REQUIRED_TOPICS:
        errors.append(f"Expected {REQUIRED_TOPICS} topics, found {len(topic_headers)}")
    prompt_headers = re.findall(r"^### Prompt \d+\.\d+", text, re.MULTILINE)
    if len(prompt_headers) != TOTAL_PROMPTS:
        errors.append(f"Expected {TOTAL_PROMPTS} prompts, found {len(prompt_headers)}")
    success_checks = re.findall(r"\*\*Success check:\*\*", text)
    if len(success_checks) < TOTAL_PROMPTS * 0.9:  # allow slight variance
        errors.append(f"Expected ~{TOTAL_PROMPTS} Success checks, found {len(success_checks)}")
    if not re.search(r"## Topic 10 —.*(Debug|Audit|Meta)", text, re.IGNORECASE):
        errors.append("Topic 10 must be the Debug/Audit/Meta topic")
    return errors


# ---------------------------------------------------------------------------
# Heuristic quality scoring
# ---------------------------------------------------------------------------

@dataclass
class HeuristicScore:
    name: str
    score: float  # 0.0 – 1.0
    detail: str


def _count_residue_language(text: str) -> int:
    patterns = [
        r"residue", r"empty", r"ambiguous", r"out[- ]of[- ]scope",
        r"UNCLASSIFIABLE", r"INSUFFICIENT_CONTEXT", r"SEED_TOO_VAGUE",
        r"if the .+ is too vague", r"return only the string",
        r"Do not invent", r"Return only",
    ]
    return sum(1 for p in patterns if re.search(p, text, re.I))


def _success_check_quality(text: str) -> float:
    checks = re.findall(r"\*\*Success check:\*\*\s*(.+)", text)
    if not checks:
        return 0.0
    good = 0
    for c in checks:
        c = c.strip()
        # Prefer concrete, measurable language
        if any(w in c.lower() for w in ["exactly", "parses", "contains", "matches", "present", "integer", "≤", ">="]):
            good += 1
        elif len(c) > 20:
            good += 0.5
    return min(1.0, good / len(checks))


def _axis_coverage(text: str) -> float:
    axes = ["Conditioning", "Representation", "Reasoning Topology", "Decoding", "Orchestration",
            "Grounding", "Optimisation", "Verification", "Security", "Meta", "Robustness"]
    found = sum(1 for a in axes if a in text)
    return min(1.0, found / 8.0)


def _topic10_depth(text: str) -> float:
    # Look for the five required audit flavours
    markers = [
        r"Prompt debugger|axis failed|corrected prompt",
        r"Faithfulness audit|post-hoc|causally necessary",
        r"(?:six|seven)-axis structural audit|Score each axis",
        r"injection-surface|hardening language",
        r"Meta-prompt improver|changelog",
    ]
    # Restrict search to Topic 10 section if possible
    m = re.search(r"## Topic 10 —.*?(?=## Topic|\Z)", text, re.S | re.I)
    section = m.group(0) if m else text
    hits = sum(1 for p in markers if re.search(p, section, re.I))
    return hits / 5.0


def _uniqueness(text: str) -> float:
    """Crude near-duplicate detection via prompt body similarity."""
    bodies = re.findall(r"### Prompt \d+\.\d+\n(.*?)(?=\*\*Success check:|\*\*Axes:|### Prompt|## Topic|\Z)", text, re.S)
    if len(bodies) < 10:
        return 0.5
    # Compare first 120 chars of each body
    prefixes = [re.sub(r"\s+", " ", b.strip())[:120] for b in bodies if b.strip()]
    unique = len(set(prefixes))
    return unique / max(len(prefixes), 1)


def _length_sanity(text: str) -> float:
    """Prefer prompts that are neither tiny stubs nor multi-page essays."""
    bodies = re.findall(r"### Prompt \d+\.\d+\n(.*?)(?=\*\*Success check:|\*\*Axes:|### Prompt|## Topic|\Z)", text, re.S)
    if not bodies:
        return 0.0
    lengths = [len(b.strip()) for b in bodies if b.strip()]
    if not lengths:
        return 0.0
    # Ideal band ~200–1200 chars
    good = sum(1 for L in lengths if 150 <= L <= 1800)
    return good / len(lengths)


def heuristic_scores(text: str) -> list[HeuristicScore]:
    return [
        HeuristicScore("residue_language", min(1.0, _count_residue_language(text) / 25.0),
                       f"residue/edge-case language hits: {_count_residue_language(text)}"),
        HeuristicScore("success_check_quality", _success_check_quality(text),
                       "measurability of success checks"),
        HeuristicScore("axis_coverage", _axis_coverage(text),
                       "breadth of seven-axis vocabulary"),
        HeuristicScore("topic10_depth", _topic10_depth(text),
                       "presence of the five required audit flavours"),
        HeuristicScore("uniqueness", _uniqueness(text),
                       "near-duplicate resistance"),
        HeuristicScore("length_sanity", _length_sanity(text),
                       "prompt length distribution in usable band"),
    ]


# ---------------------------------------------------------------------------
# Pluggable real-model judge (stub)
# ---------------------------------------------------------------------------

JudgeFn = Callable[[str, str], dict[str, Any]]  # (prompt_text, suite_context) -> scores

def null_judge(prompt: str, context: str = "") -> dict[str, Any]:
    """Placeholder. Replace with a real LLM call that returns
    {\"clarity\": 0-1, \"usefulness\": 0-1, \"robustness\": 0-1, \"notes\": \"...\"}.
    """
    return {
        "clarity": None,
        "usefulness": None,
        "robustness": None,
        "notes": "No real-model judge configured. Supply a JudgeFn to eval_suite().",
        "model": None,
    }


# Example of how a real judge would look (not executed unless wired):
#
# def openai_judge(prompt: str, context: str = "") -> dict:
#     import openai
#     resp = openai.ChatCompletion.create(
#         model="gpt-4o",
#         messages=[{
#             "role": "user",
#             "content": f"Score this prompt 0-1 on clarity, usefulness, robustness.\n\n{prompt}"
#         }]
#     )
#     ... parse and return


# ---------------------------------------------------------------------------
# Full evaluation
# ---------------------------------------------------------------------------

@dataclass
class EvalReport:
    path: str
    structural_pass: bool
    structural_errors: list[str]
    heuristics: list[HeuristicScore]
    overall_heuristic: float
    real_model: Optional[dict[str, Any]] = None
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return d

    def summary(self) -> str:
        lines = [
            f"Suite: {self.path}",
            f"Structural: {'PASS' if self.structural_pass else 'FAIL'}",
        ]
        if self.structural_errors:
            for e in self.structural_errors:
                lines.append(f"  - {e}")
        lines.append(f"Overall heuristic score: {self.overall_heuristic:.3f}")
        for h in self.heuristics:
            lines.append(f"  {h.name}: {h.score:.3f}  ({h.detail})")
        if self.real_model:
            lines.append(f"Real-model judge: {json.dumps(self.real_model, indent=2)}")
        for n in self.notes:
            lines.append(f"Note: {n}")
        return "\n".join(lines)


def eval_suite(
    path: str | Path,
    judge: Optional[JudgeFn] = None,
    sample_prompts: int = 0,
) -> EvalReport:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    errors = structural_checks(text)
    heurs = heuristic_scores(text)
    overall = sum(h.score for h in heurs) / max(len(heurs), 1)

    real = None
    notes = []
    if judge and sample_prompts > 0:
        # Extract a few prompt bodies and score them
        bodies = re.findall(
            r"### Prompt (\d+\.\d+)\n(.*?)(?=\*\*Success check:|\*\*Axes:|### Prompt|## Topic|\Z)",
            text, re.S,
        )
        scores = []
        for pid, body in bodies[:sample_prompts]:
            scores.append({"id": pid, **judge(body.strip(), text[:2000])})
        real = {"sampled": scores, "n": len(scores)}
        notes.append(f"Real-model judge ran on {len(scores)} sample prompts.")
    elif judge:
        notes.append("Judge supplied but sample_prompts=0; skipped real-model layer.")

    return EvalReport(
        path=str(path),
        structural_pass=len(errors) == 0,
        structural_errors=errors,
        heuristics=heurs,
        overall_heuristic=overall,
        real_model=real,
        notes=notes,
    )


def main():
    import argparse
    p = argparse.ArgumentParser(description="Eval harness for prompt suites")
    p.add_argument("suite", help="Path to suite Markdown")
    p.add_argument("--json", action="store_true", help="Emit JSON report")
    p.add_argument("--min-score", type=float, default=0.55,
                   help="Minimum overall heuristic to exit 0 (default 0.55)")
    args = p.parse_args()

    report = eval_suite(args.suite)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(report.summary())

    if not report.structural_pass:
        sys.exit(1)
    if report.overall_heuristic < args.min_score:
        print(f"\nHeuristic score {report.overall_heuristic:.3f} < {args.min_score}", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
