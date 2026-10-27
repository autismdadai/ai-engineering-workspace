Engineering stack series: Phase 1 and 2 working files (October 9, 2026)

These are the raw working files behind claude/engineering-stack-claim-ledger.md,
claude/engineering-stack-freshness-ledger.md and claude/engineering-stack-plan.md
in the "Prompting" project. They are not in the project. The project docs are the
checked versions; use these only to trace how a verdict was reached.

checker-notes/   The seven checker agents' full notes (r1 to r7), one per topic group.
                 Written by AI agents from pages read through a summarizing fetch
                 tool. Treat them as working notes, not as sources.
data/            claim-inventory.md (the claims pulled from the Gemini paper before
                 checking), and the raw registry outputs (PyPI, npm) of October 9.
scripts/         The scripts used: the PDF conversion, the ledger arithmetic
                 (ledger_checks.py), the PyPI reader, the verdict counter and the
                 axes-test table generator. Standard-library Python 3.
