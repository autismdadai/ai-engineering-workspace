# Planet X — Deep Research Protocol

## Goal
Produce research grounded in primary sources — going past the first page of results and following citations back to the original documents — rather than repeating what a model remembers or what summaries say.

## Tools
Use web search and fetch when the host provides them, and cite only what was actually opened. Without them, say so and mark unchecked claims UNVERIFIED.

## Methods (ordered preference)
1. **Primary sources first** — original documents, raw data, FOIA / declassified releases, peer-reviewed primary literature, official records, direct measurements.
2. **Multi-hop search** — follow citations, footnotes, and archival references rather than stopping at secondary summaries.
3. **Adversarial / alternative search** — deliberately seek sources that challenge the dominant narrative; include Global South, non-English primary material where relevant.
4. **Preprints & working papers** — arXiv, bioRxiv, SSRN, institutional repositories when peer-reviewed versions are unavailable.
5. **Cross-lingual primary material** — do not limit to English-language sources when the claim involves non-Anglophone domains.
6. **Negative evidence** — record what was searched and not found; absence can be informative.

## Output Requirements
- Every material claim carries Support Status + Confidence 1–10 + Source Class (see shared/evidence-grading.md).
- Prefer primary over secondary; secondary over tertiary.
- When sources conflict, surface the conflict explicitly rather than averaging.
- Reproducibility notes must allow a third party to re-check the key findings.

## Prohibited
- Inventing sources or DOIs.
- Presenting tertiary media summaries as primary evidence.
- Actionable construction details for weapons, explosives, biological agents, or criminal tradecraft (historical / religious context only, never how-to).
