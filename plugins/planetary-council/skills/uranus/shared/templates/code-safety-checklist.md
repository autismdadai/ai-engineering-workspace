# Uranus Code Safety & Quality Checklist

Before presenting any code:

1. **Language choice justified** — Python for AI/ML/scientific; Rust/C++/CUDA for systems/performance; TypeScript for tooling/interfaces.
2. **No secrets** — no API keys, passwords, tokens, or private data in the code.
3. **No hidden network** — any network call must be explicit, documented, and optional.
4. **Bounded output** — default behaviour must not dump unbounded data.
5. **Runnable or clearly marked** — either complete enough to run or labelled as pseudocode / sketch with clear next steps.
6. **Dependencies listed** — every external library named.
7. **Failure modes noted** — what breaks first and how it fails safely.

Code First still applies: demonstrate, do not merely describe.
