# Works Cited entries without an arXiv ID or DOI, and stated venues

Checked 2026-10-15. New lookups used: 30 of 30 (cap reached). Three items (39, 123, and the Prompt Engineering Playbook half of 20) were settled from pages the earlier run had already saved.

Method notes
- OpenReview and OWASP's site (genai.owasp.org) refuse automated fetches (browser check or HTTP 403). Venue checks therefore used the venue's own paper lists: iclr.cc, neurips.cc, proceedings.neurips.cc, ACL Anthology, USENIX.
- "Page text read" means I read the page itself. "Listed" means the venue's page appeared in a search result with a matching title and I did not open it. The evidence column says which.

## Result in one view

| Result | Entries |
|---|---|
| Confirmed as stated | 16, 17, 20, 37, 39, 45, 46, 47, 48, 58, 59, 68, 80, 87, 109, 110, 113, 119, 123, 132 |
| Needs a correction | 91 (snapshot date; one sentence in Section 16.2 not found in the cited blog), 128 (title) |
| Could not be checked | 74, 81, 136 (site blocked); 111, 112 (not reached, cap) |

## Corrections to make

1. Entry 128 (Perez et al.). The ICLR 2025 paper list on iclr.cc names the paper "When LLMs Play the Telephone Game: Cultural Attractors as Conceptual Tools to Evaluate LLMs in Multi-turn Settings". The manual's title, "Cumulative Changes and Attractors in Iterated Cultural Transmissions", is the earlier arXiv title. Answer to the question asked: the ICLR version used the new title. Cite the new title; the earlier one can go in a note.
2. Entry 91 (Vectara). The leaderboard README says "Last updated on September 22, 2026" and "uses HHEM-2.3". The manual says "as updated May 2026". The figures the manual gives for HHEM-2.3 (DeepSeek-R1 11.3%, DeepSeek-V3 6.1%, over 7,700 articles) still match today's README, so only the snapshot date is unconfirmed. Give the access date instead of "May 2026".
3. Section 16.2 (line 2260 of the manual). The sentence "R1 producing 71.7% 'benign hallucinations' against V3's 36.8%, which Vectara attributes to R1 'overhelping'" is not in the Vectara post that entry 91 cites ("DeepSeek-R1 hallucinates more than DeepSeek-V3", 30 January 2025). I read the whole post: it has no "benign" and no "overhelping", and no 71.7 or 36.8. What it does report: HHEM-2.1 rates of 14.3% (R1) and 3.9% (V3); HHEM score standard deviation 0.23 against 0.06; and a guess that R1 produces "many more samples that are borderline hallucinated". Either find the post these figures came from, or remove the sentence. The 14.3% and 3.9% figures are correct.

## Entry by entry

Format: entry, status, what the primary source says.

- 16 Elhage, Toy Models of Superposition. VERIFIED. Transformer Circuits Thread index (transformer-circuits.pub), page text read: "September 2022 ... Toy Models of Superposition, Elhage et al., 2022". The paper's own page title is "Toy Models of Superposition". The manual's "Anthropic, 2022" is right. Optional: write "Transformer Circuits Thread, September 2022".
- 17 Templeton, Scaling Monosemanticity. VERIFIED. Same index: "May 2024 Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet, Templeton et al., 2024". The manual uses the short title; the full title has the subtitle.
- 20 CO-STAR (Teo). VERIFIED. Towards Data Science page, text read: "How I Won Singapore's GPT-4 Prompt Engineering Competition", Sheila Teo, December 29, 2023 (page metadata 2023-12-29). It says "The CO-STAR framework, a brainchild of GovTech Singapore's Data Science & AI team". The Playbook half was confirmed earlier on tech.gov.sg (page dated 3 April 2025): "CO-STAR Framework, featured in our Prompt Engineering Playbook". The earlier run could not read the date; this run did.
- 37 Skeleton-of-Thought, ICLR 2024. VERIFIED. iclr.cc/virtual/2024/papers.html (page text read) lists "Skeleton-of-Thought: Prompting LLMs for Efficient Parallel Generation". The arXiv comment field also reads "In ICLR'24".
- 39 Mind Your Step (by Step), PMLR v267. VERIFIED (earlier saved page). proceedings.mlr.press/v267/liu25t.html: authors Ryan Liu, Jiayi Geng, Addison J. Wu, Ilia Sucholutsky, Tania Lombrozo, Thomas L. Griffiths; "Proceedings of the 42nd International Conference on Machine Learning, PMLR 267:38489-38517, 2025." Optional: add the pages.
- 45 Building Effective Agents. VERIFIED. anthropic.com/engineering/building-effective-agents: "Building effective agents", "Published Dec 19, 2024" (the browser title reads "Building Effective AI Agents"). The page was modified on 2026-08-10, so recheck any quote against the current text.
- 46 Model Context Protocol. VERIFIED. anthropic.com/news/model-context-protocol: "Introducing the Model Context Protocol", Nov 25, 2024, "Today, we're open-sourcing the Model Context Protocol (MCP)". Last modified 2026-05-07.
- 47 Contextual Retrieval. VERIFIED. anthropic.com/news/contextual-retrieval: heading "Introducing Contextual Retrieval", "Published Sep 19, 2024" (browser title "Contextual Retrieval in AI Systems"). Last modified 2026-01-07.
- 48 Effective Context Engineering for AI Agents. VERIFIED. anthropic.com/engineering/effective-context-engineering-for-ai-agents: "Published Sep 29, 2025". Last modified 2026-01-06.
- 58 GEPA, ICLR 2026 Oral. VERIFIED. iclr.cc/virtual/2026/events/oral (page text read) lists "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning" with the event-type badge "Oral"; first author Lakshya A Agrawal.
- 59 Local Prompt Optimization, NAACL 2025. VERIFIED (listed). ACL Anthology lists "Local Prompt Optimization" as 2025.naacl-short.7, Yash Jain and Vishal Chowdhary, a short paper (pages 75-81 per the search summary). I did not open the page. Optional: add "short paper" and the Anthology ID.
- 68 Spliethover et al., Adaptive Prompting. VERIFIED. aclanthology.org/2025.naacl-long.122 (page text read): "Adaptive Prompting: Ad-hoc Prompt Composition for Social Bias Detection"; Maximilian Spliethover, Tim Knebler, Fabian Fumagalli, Maximilian Muschalik, Barbara Hammer, Eyke Hullermeier, Henning Wachsmuth; Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the ACL; pages 2421-2449; April 2025. The manual gives the short title only.
- 74 OpenAI Structured Outputs, 6 Aug 2024. UNVERIFIABLE. openai.com returned HTTP 403 to WebFetch and to curl, and the Wayback copy also returned 403 (earlier run). The date is not confirmed from the page. Check it by hand in a normal browser.
- 80 Huang et al., ICLR 2024. VERIFIED. iclr.cc/virtual/2024/papers.html lists "Large Language Models Cannot Self-Correct Reasoning Yet". The manual's "LLMs Cannot Self-Correct Reasoning Yet" is a shortened title; use the full one.
- 81 OWASP LLM01:2025 and LLM07:2025. UNVERIFIABLE. genai.owasp.org returned HTTP 403 (WebFetch) and a browser-check page (curl) for both the Top 10 list and the Agentic page. Check by hand.
- 87 Sheshadri et al., NeurIPS 2025. VERIFIED. neurips.cc/virtual/2025/papers.html lists "Why Do Some Language Models Fake Alignment While Others Don't?" (poster 120242).
- 91 Vectara. CORRECTED (see Corrections 2 and 3). Blog confirmed: "DeepSeek-R1 hallucinates more than DeepSeek-V3", JAN 30, 2025, by Forrest Bao, Chenyu Xu, Ofer Mendelevitch; HHEM 2.1 gives R1 14.3% and V3 3.9%. Leaderboard README (raw GitHub, text read): "uses HHEM-2.3"; "Last updated on September 22, 2026"; DeepSeek-R1 11.3%, DeepSeek-V3 6.1%; "over 7700 articles".
- 109 NBER Working Paper 34255. VERIFIED. nber.org/papers/w34255: "How People Use ChatGPT"; Aaron Chatterji, Thomas Cunningham, David J. Deming, Zoe Hitzig, Christopher Ong, Carl Yan Shan, Kevin Wadman; Working Paper 34255; September 2025. The manual's author list matches in order.
- 110 Anthropic Economic Index reports. VERIFIED (titles from page titles, months from address names). Page titles listed: "Economic Index report: Economic primitives" (address ends anthropic-economic-index-january-2026-report), "Anthropic Economic Index report: Learning curves" (economic-index-march-2026-report), "Anthropic Economic Index report: Cadences" (economic-index-june-2026-report). The search summary adds that Learning curves uses February 2026 usage and Cadences is June 2026. I did not open the three report pages, so no printed publication date was read. The index page itself says "Last updated: Jun 26, 2026".
- 111 RULER, COLM 2024. UNVERIFIABLE (not reached). Lookup cap.
- 112 NoLiMa, ICML 2025. UNVERIFIABLE (not reached). The search for it returned nothing. For context, the PMLR citation line for entry 39 shows that PMLR 267 is the 42nd ICML, so the volume label is consistent, but NoLiMa's own page was not opened.
- 113 Chroma, Context Rot. VERIFIED. research.trychroma.com/context-rot (page text read): "Chroma Technical Report July 14, 2025"; "Context Rot: How Increasing Input Tokens Impacts LLM Performance"; Kelly Hong, Anton Troynikov, Jeff Huber.
- 119 GSM1k, NeurIPS 2024 Datasets and Benchmarks. VERIFIED. proceedings.neurips.cc/paper_files/paper/2024 (page text read): "A Careful Examination of Large Language Model Performance on Grade School Arithmetic", filed under the datasets_and_benchmarks_track; Hugh Zhang first.
- 123 Thinking Machines, Defeating Nondeterminism. VERIFIED (earlier saved page). Byline "Horace He in collaboration with others at Thinking Machines", "Sep 10, 2025" (metadata 2025-09-10). Optional: write "He and others".
- 128 Perez et al., ICLR 2025. CORRECTED (see Corrections 1). Venue confirmed: ICLR 2025 papers list, poster 28880.
- 132 StruQ, USENIX Security 2025. VERIFIED (listed). usenix.org/conference/usenixsecurity25/presentation/chen-sizhe appeared in search with the exact title; Sizhe Chen, Julien Piet, Chawin Sitawarin, David Wagner; 34th USENIX Security Symposium, pages 2383-2400 (from the search summary, not from opening the page). The same search turned up a USENIX Security 2026 paper (Nasr et al., "Stronger Adaptive Attacks Bypass Defenses Against LLM ...") that reports an adaptive attack succeeding against StruQ; I did not open it.
- 136 OWASP Top 10 for Agentic Applications, Dec 2025. UNVERIFIABLE. genai.owasp.org returned HTTP 403 (WebFetch) and a browser-check page (curl). Check by hand.

## Left for a person with a normal browser

74 (OpenAI date), 81 and 136 (OWASP pages), 111 (RULER at COLM 2024), 112 (NoLiMa at ICML 2025).
