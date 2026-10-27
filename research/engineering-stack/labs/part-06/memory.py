"""Three ways an agent's long-term memory can handle a changed fact, a
provenance gate against memory poisoning, and a safe path check for a
file-based memory tool. Standard library only (Python 3.11+).

Part 06 of The AI Engineering Stack. The facts are invented [I].
"""
import posixpath
from dataclasses import dataclass


@dataclass
class Fact:
    subject: str
    attribute: str
    value: str
    valid_at: int                 # when it became true (a day number, for simplicity)
    invalid_at: int | None = None  # when it stopped being true
    source: str = "user"


class Memory:
    """mode 'overwrite': a new value replaces the old one (like the UPDATE
    operation in Mem0's 2025 paper); history is lost.
    mode 'add_only': every fact is kept as written, nothing is changed (like
    Mem0's April 2026 default, "nothing is overwritten").
    mode 'temporal': the old fact is kept but closed, with invalid_at set to
    the new fact's valid_at (like Graphiti's edge invalidation)."""

    TRUSTED = {"user", "system"}

    def __init__(self, mode="temporal"):
        if mode not in ("overwrite", "add_only", "temporal"):
            raise ValueError(mode)
        self.mode = mode
        self.facts = []
        self.quarantine = []

    def write(self, fact, approved=False):
        """Facts from untrusted sources (tool output, web pages, other agents)
        wait in quarantine unless approved: one control against memory
        poisoning (OWASP ASI06), not a complete defence."""
        if fact.source not in self.TRUSTED and not approved:
            self.quarantine.append(fact)
            return "quarantined"
        same = [f for f in self.facts if (f.subject, f.attribute) == (fact.subject, fact.attribute)]
        if self.mode == "overwrite":
            self.facts = [f for f in self.facts if f not in same]
        elif self.mode == "temporal":
            for f in same:
                if f.invalid_at is None and f.valid_at < fact.valid_at and f.value != fact.value:
                    f.invalid_at = fact.valid_at
        self.facts.append(fact)
        return "stored"

    def recall(self, subject, attribute):
        """All stored values for a question, newest first, as a retriever would
        hand them to the model."""
        hits = [f for f in self.facts if (f.subject, f.attribute) == (subject, attribute)]
        return [f.value for f in sorted(hits, key=lambda f: -f.valid_at)]

    def current(self, subject, attribute):
        """Facts still valid (temporal mode closes the old ones)."""
        return [f.value for f in self.facts
                if (f.subject, f.attribute) == (subject, attribute) and f.invalid_at is None]

    def as_of(self, subject, attribute, day):
        """What was true on a given day; only answerable if history was kept."""
        return [f.value for f in self.facts
                if (f.subject, f.attribute) == (subject, attribute)
                and f.valid_at <= day and (f.invalid_at is None or day < f.invalid_at)]


def safe_memory_path(path, root="/memories"):
    """Accept only paths inside the memory folder. Anthropic's memory-tool docs
    tell developers to validate every path against traversal such as
    '/memories/../../secrets.env'. Returns the normalized path or raises."""
    if not isinstance(path, str) or "\x00" in path or "\\" in path:
        raise ValueError("bad path")
    norm = posixpath.normpath(path)
    if norm != root and not norm.startswith(root + "/"):
        raise ValueError(f"outside {root}: {path}")
    return norm
