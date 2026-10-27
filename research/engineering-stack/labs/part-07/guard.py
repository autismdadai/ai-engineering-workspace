"""Client-side controls for MCP tools, standard library only.

Three controls a host can apply before a model ever sees a tool:
  pin_tools / changed_tools  fingerprint each tool definition when the user
                             approves it, and flag any later change (a "rug
                             pull", in Invariant Labs' term)
  scan_description           flag text in a description that addresses the
                             model rather than describing the tool. A heuristic
                             for review, not a defense: rewording defeats it.
  needs_approval             decide whether a call needs the user, trusting
                             annotations only from servers the user trusts
"""
import hashlib
import json
import re
import unicodedata


def fingerprint(tool):
    """SHA-256 of the tool's canonical JSON: any change to any field changes it."""
    canonical = json.dumps(tool, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def pin_tools(tools):
    return {tool["name"]: fingerprint(tool) for tool in tools}


def changed_tools(pins, tools):
    """Names of tools that are new, changed or gone since they were pinned."""
    current = pin_tools(tools)
    changed = sorted(name for name in current if pins.get(name) != current[name])
    removed = sorted(name for name in pins if name not in current)
    return changed + removed


# Patterns seen in published tool-poisoning examples [I: the list is the lab's
# own and is not exhaustive].
SUSPICIOUS = [
    (r"<\s*important\s*>", "a tag addressed to the model"),
    (r"\bignore (all |any )?(previous|prior|above)\b", "asks to ignore instructions"),
    (r"\bdo not (tell|mention|inform)\b.*\buser\b", "asks to hide something from the user"),
    (r"\bbefore using this tool\b", "a precondition on other actions"),
    (r"(~|\$home|/home/\w+)/\.(ssh|aws|config)\b|id_rsa|\.env\b", "names a credential file"),
    (r"\b(read|open|cat) (the )?file\b", "asks the model to read files"),
]

INVISIBLE = {"Cf"}  # format characters, such as zero-width spaces


def scan_description(text):
    """Return a list of reasons the text deserves a human look (empty if none)."""
    reasons = []
    lowered = text.lower()
    for pattern, reason in SUSPICIOUS:
        if re.search(pattern, lowered):
            reasons.append(reason)
    if any(unicodedata.category(ch) in INVISIBLE for ch in text):
        reasons.append("invisible characters")
    if len(text) > 1000:
        reasons.append("unusually long")
    return reasons


def scan_tools(tools):
    """Map tool name to reasons, for every tool whose description is flagged."""
    report = {}
    for tool in tools:
        text = " ".join([tool.get("title", ""), tool.get("description", "")])
        reasons = scan_description(text)
        if reasons:
            report[tool["name"]] = reasons
    return report


def needs_approval(tool, server_trusted):
    """True if the user must approve this call.

    The spec says clients MUST treat annotations as untrusted unless they come
    from trusted servers. So an untrusted server's readOnlyHint counts for
    nothing, and every call to it is approved by the user. The missing-value
    defaults follow the spec: destructiveHint true, readOnlyHint false.
    """
    if not server_trusted:
        return True
    annotations = tool.get("annotations") or {}
    if annotations.get("readOnlyHint", False):
        return False
    return True
