# Planetary Council System (plugin)

An orchestrator (the Sun), nine planet specialists and Planet X, an independent fact-checker. Every agent claims only abilities it can prove: sources count only if actually opened, code is run or labelled "not run", and legal, medical, financial, safety and distress topics follow a shared care rule.

## Components
- **Skills (13):** `planetary-council` (the Sun), `mercury`, `venus`, `earth`, `mars`, `jupiter`, `saturn`, `uranus`, `neptune`, `pluto`, `planet-x`, plus two helpers: `quantum-entanglement-lab` (Uranus's quantum checker) and `sophisticated-prompt-generator` (50-prompt suites).
- **Agents (10):** one per planet plus `planet-x`. Each runs in its own context, so Planet X checks claims without seeing the planets' reasoning.

## Usage
- **"Run the council on: …"** — the Sun classifies the problem, launches the chosen planets as sub-agents in parallel, sends the load-bearing claims to Planet X, and writes the Council Brief with a COUNCIL LOG.
- **"Ask Mercury …"**, **"Uranus, prove … with code"** — one planet at a time.
- **"Fact-check this with Planet X"** — independent verification of any text.

## Setup
- Turn on web search and web fetch: agents cite only sources they actually opened, and without them claims are marked UNVERIFIED.
- Uranus and Mars run calculations and code. The quantum lab needs Python 3 with `qutip>=5`, `numpy` and `scipy`; without QuTiP, Uranus falls back to NumPy.

## Notes
- Every Council Brief ends with: *AI-generated council analysis — information, not professional advice.*
- Planet X's Matrix is an appendix at the end of its answer. Anything that would be refused is declined, never stored.
- The shared rules (evidence grading, Matrix protocol, professional-advice and care rules) are bundled inside each skill, because skills can't open each other's files.
