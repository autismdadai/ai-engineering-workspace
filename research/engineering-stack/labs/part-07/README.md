# Engineering Stack, Part 07 lab: an MCP server and client from scratch

Companion to claude/engineering-stack-part-07-tools-and-protocols.md, Section 8.
Tested October 14, 2026 on Linux with Python 3.13.16, 3.12.3 and 3.11.17.

The core lab uses only Python's standard library: no installs, no model, no
account, no API key. Nothing here connects to the internet.

| File | What it is |
|---|---|
| `notes_server.py` | An MCP server over stdio for revision 2026-07-28, with three tools and a confirm-before-delete round trip |
| `mcp_client.py` | A matching client: starts the server, sends one JSON line per request |
| `guard.py` | Tool pinning, a description scanner (a review aid, not a defense) and the annotation rule |
| `skill_check.py` | Checks a skill folder's `SKILL.md` against the Agent Skills spec, with optional product profiles |
| `skills/note-finder/` | An example skill that passes |
| `demo.py` | Prints every JSON-RPC line exchanged |
| `run_lab.py` | 22 checks |
| `mutation_check.py` | Breaks the lab 20 ways; each must make `run_lab.py` fail |
| `crosscheck.py`, `requirements-crosscheck.txt` | Optional: interop with the official SDK, `mcp==2.3.0` |

Quick start, from this folder, in a virtual environment (Part 01, Section 7):

    python run_lab.py            # expect: 22 of 22 checks passed
    python mutation_check.py     # expect: 20 of 20 mutations caught
    python demo.py

Optional:

    python -m pip install -r requirements-crosscheck.txt
    python crosscheck.py         # expect: 8 of 8 cross-checks passed

The notes and names are invented. The server is for learning: it has no
authorization, uses a fixed signing secret unless `NOTES_STATE_KEY` is set,
and speaks only protocol revision 2026-07-28.
