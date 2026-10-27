# Sub-Skills & Delegated Capabilities (Orchestrator)

The Planetary Council Orchestrator may invoke specialised project skills when the user’s request matches their trigger conditions. These are not planetary agents; they are high-leverage tooling skills that the Sun can route to.

## sophisticated-prompt-generator

**Location:** a separate skill named `sophisticated-prompt-generator`; install it alongside this one. Skills can't open each other's files, so hand the request to that skill and let it run its own scripts.

**When to invoke / route:**
- User asks for “prompt generator”, “generate prompts”, “50 prompts”, “prompt suite”, “sophisticated prompts”, “prompt variants”, or similar.
- User wants a full production-grade prompt suite from a single seed idea.
- Phase 4 (Implementation) or any phase where high-quality prompts are the deliverable rather than an analysis.

**What it produces:**
By default 50 prompts in 10 fixed topics (5 variants each; 3 or 4 each when the user asks for fewer), placed on the seven-axis taxonomy, with Topic 10 = Debug, Audit, Faithfulness & Meta. Topic 6 can use the planets' lenses, meaning what each one checks.

**How to invoke:**
1. Treat the user’s seed question as the generator seed.
2. Either:
   - Activate the skill directly (portable skill path), or
   - Run the deterministic expander for a baseline suite (from the sophisticated-prompt-generator skill's own folder):
     ```bash
     python scripts/expand_suite.py "SEED" -o suite.md --fill
     ```
   - Then optionally refine the suite with the full generator procedure or council specialists.
3. Validate (same folder):
     ```bash
     python scripts/validate_suite.py suite.md
     ```
   The validator checks structure only. Don't use `scripts/eval_harness.py` as a quality bar: it measures vocabulary, and a padded nonsense suite outscored a real one (October 2, 2026).

**Integration notes:**
- The generator already understands Planetary lenses (Topic 6 + optional annotations).
- When the seed itself is a council-level problem, prefer generating the suite *after* a short Phase 1–2 intelligence pass so the prompts are grounded.
- Topic 10 of the generator is complementary to Planet X verification; both may be used.

**Do not use for:** single casual prompt rewrites or non-prompt tasks.
