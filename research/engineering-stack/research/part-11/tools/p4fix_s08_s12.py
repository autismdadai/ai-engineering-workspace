import sys
sys.path.insert(0, "/home/claude/part11/tools")
from p4fix_lib import patch

D = "/home/claude/part11/draft/"

OLD_STEP2 = """2. **Print the tables.** `python demo.py` prints this part's tables, starting with the file sizes beside llama.cpp's own:

   ```
   1. Llama 3 8B file sizes (tensor data), against llama.cpp's published table
      8,030,261,248 weights
      F16     16.0005 bits/weight  14.96 GiB  16.06 GB   llama.cpp: 16.0005 and 14.96 GiB
      Q4_K_M   4.8944 bits/weight   4.58 GiB   4.91 GB   llama.cpp: 4.8944 and 4.58 GiB
   ```
"""
NEW_STEP2 = """2. **Print the tables.** `python demo.py` prints eight worked tables, starting with the file sizes beside llama.cpp's own (abridged: the Q8_0, Q6_K and Q5_K_M rows sit where the dots are):

   ```
   1. Llama 3 8B file sizes (tensor data), against llama.cpp's published table
      8,030,261,248 weights
      F16     16.0005 bits/weight  14.96 GiB  16.06 GB   llama.cpp: 16.0005 and 14.96 GiB
      ...
      Q4_K_M   4.8944 bits/weight   4.58 GiB   4.91 GB   llama.cpp: 4.8944 and 4.58 GiB
   ```
"""

OLD_OUT = """```
PASS c01_feed_forward_width
PASS c05_file_sizes_match_llama_cpp
PASS c06_gpt_oss_20b
PASS c11_speculative_decoding
PASS c14_reader_test_logic
...
14 of 14 checks passed
```"""
NEW_OUT = """```
PASS c01_feed_forward_width
...
PASS c05_file_sizes_match_llama_cpp
PASS c06_gpt_oss_20b
...
PASS c11_speculative_decoding
...
PASS c14_reader_test_logic
14 of 14 checks passed
```"""

patch(D + "s08.md", [
    ("Open `runmath.py`: each function is a few lines, and its docstring names the source.",
     "Open `runmath.py`: most functions are a few lines, and the sources are named in the comments above the tables and in docstrings."),
    (OLD_STEP2, NEW_STEP2),
    ("Llama 3 8B's cache for one 32,768-token conversation is as large as its 4-bit weights [T].",
     "Llama 3 8B's cache for one 32,768-token conversation is nearly as large as its 4-bit weights (4.58 GiB) [T]."),
    ("5. **Break it.** In `runmath.py`, change `\"Q6_K\": (256, 210)` to `\"Q6_K\": (256, 208)`, two bytes short per block. `python run_lab.py` now ends `10 of 14 checks passed`: the file sizes, the fit check and the speed ceiling all move, because Q4_K_M uses Q6_K for some tensors [T].",
     "5. **Break it.** In `runmath.py` (line 83; any text editor, such as Notepad, TextEdit or nano), change `\"Q6_K\": (256, 210)` to `\"Q6_K\": (256, 208)`, two bytes short per block. `python run_lab.py` now ends `10 of 14 checks passed`: four checks fail (bits per weight, file sizes, the fit check and the speed ceiling), because Q4_K_M uses Q6_K for some tensors, and each FAIL line shows the value it got [T]."),
    (" Expect `31 of 31 mutations caught` in about 15 seconds [T]. All 31 were caught on the first run; one check (c08) failed on its own first run because its expected value had been typed in rather than computed, and was corrected to the computed 80,482 tokens [T].",
     " Expect `31 of 31 mutations caught` in about 15 seconds [T]."),
    (OLD_OUT, NEW_OUT),
    ("**If it fails.** A FAIL line names the check and the failing value; Section 7.6 covers the common errors. A check that fails only on your machine is worth reporting: send the whole output.",
     "**If it fails.** A FAIL line names the check and, for checks that compare numbers, the value it got; Section 7.6 covers the common errors. If a check fails only on your machine, keep the whole output for reader test R1 (Section 12)."),
    ("Ollama calls ollama.com unless told not to [V: OLS].",
     "Ollama calls ollama.com; `OLLAMA_NO_CLOUD=1` stops most of those calls, but not its apps' hourly update check [V: OLS]."),
    ("Answer: about 62.5 tokens per second. Check: `python -c",
     "Answer: about 62.5 tokens per second. Check, with the Q4_K_M file's 4,912,898,048 bytes from Section 7.4: `python -c"),
    ("A draft is accepted half the time and costs 0.4 of a target pass. Answer: yes, barely: α beats c, the best γ is 1,",
     "A draft is accepted half the time (α = 0.5) and one draft run costs 0.4 of a target run (c = 0.4). Answer: yes, barely: α beats c, the best number of guesses per pass (γ) is 1,"),
    ("so bytes per second sets the pace [V: VLL][T].", "so bytes per second sets the pace [V: POP][T]."),
])

patch(D + "s10.md", [
    ("NVIDIA's 3.55 times, the vLLM team's figures, EAGLE-3's and MagicDec's are measurements by vendors or method authors; LMDeploy's README claims \"up to 1.8x higher request throughput than vLLM\" with no scope at all [V: TRT, VBL, EG3, MGD, LMD]. MLPerf is the independent benchmark, and its results are still submitted by vendors [V: MLP].",
     "NVIDIA's 3.55 times, the vLLM team's figures, EAGLE-3's and MagicDec's are measurements by vendors, engine teams or method authors (EAGLE-3's batch table was run by the SGLang team); LMDeploy's README claims \"up to 1.8x higher request throughput than vLLM\" with no scope beyond a 2024 note naming one model [V: TRT, VBL, EG3, MGD, LMD]. MLPerf has rules and peer review, but vendors submit the results and review each other's [V: MLP]."),
    ("a capture of a fresh install with and without `OLLAMA_NO_CLOUD=1` would settle them [U].",
     "a capture of a fresh install with and without `OLLAMA_NO_CLOUD=1` would settle them, and would show whether a later release starts using the stored `Survey` setting (Section 3.8) [U]."),
    ("6. No conflict found with the taxonomy or the guide:",
     "6. *Part 10 and claim ledger P10-09b* call Llama 4 Meta's current line. Meta's verified Hugging Face organization has since published Muse Glimmer 30B (Apache-2.0, August 2026) and lists the much larger Muse Spark Open [V: MUS]. Part 10's text and the ledger note should say so.\n7. No conflict found with the taxonomy or the guide:"),
])

patch(D + "s12.md", [
    ("All opened October 16, 2026, by the lead session or one of three researcher agents.",
     "All opened October 16, 2026, by the lead session or one of three researcher agents, except MUS (October 19)."),
    ("and ran every number in the lab [T].",
     "and ran every number in the lab [T]; after the checks, the lead reopened the source behind every finding before fixing it (Checks section)."),
    ("| DUT | Dutta et al., \"Accuracy is Not All You Need\", NeurIPS 2024, abstract | PR |",
     "| DUT | Dutta et al., \"Accuracy is Not All You Need\", NeurIPS 2024 (Advances in Neural Information Processing Systems 37, Main Conference Track), abstract page on proceedings.neurips.cc | PR |"),
    ("| EG3 | Li et al., \"EAGLE-3\", arXiv 2503.01840v3, abstract and Table 3 | PP | Speed-up falling with batch size | 7 |",
     "| EG3 | Li et al., \"EAGLE-3\", arXiv 2503.01840v3, abstract and Table 3 (run by the SGLang team) | PP | Speed-up falling with batch size | 7 |"),
    ("| LMS | LM Studio app terms (August 23, 2026) and privacy policy; lmstudio-ai/docs at 4f8082f | OD | Licence, telemetry, AVX2 | 7 |",
     "| LMS | LM Studio app terms (August 23, 2026) and privacy policy; lmstudio-ai/docs at 4f8082f, system requirements | OD | Licence scope, paid features, telemetry, platforms | 7 |"),
    ("| MAR | Marie and Fujita, arXiv 2508.20893v1 | PP | Small models and languages lose most | 6 |",
     "| MAR | Marie and Fujita, arXiv 2508.20893v1, abstract | PP | Low-resource languages lose most; GGUF most consistent | 6 |"),
    ("| MEG | NVIDIA/Megatron-LM at 3888b34, README, \"Performance Benchmarking\" | OD | 41% to 48% of peak (self-reported) | 7 |",
     "| MEG | NVIDIA/Megatron-LM at 3888b34, README, \"Performance Benchmarking\" | OD | 41% to 48% MFU (self-reported) | 7 |"),
    ("| MLP | mlcommons/inference_results_v6.1 at 4bb63cd (`summary.csv`, supplemental PDF); mlcommons/policies at 45b8b62 | OD | Round 6.1: date, counts, preview rule | 9 |",
     "| MLP | mlcommons/inference_results_v6.1 at 4bb63cd (`summary.csv`; the supplemental PDF, whose title reads \"UNDER EMBARGO UNTIL 9/16/26 8:00 AM PT\"); mlcommons/policies at 45b8b62 | OD | Round 6.1: date, counts, preview rule, review by submitters | 9 |"),
    ("| MLX | ml-explore/mlx-lm at 93e6d4a (v0.32.2): LICENSE, README, SERVER.md | OD | Licence; server warning | 8 |\n",
     "| MLX | ml-explore/mlx-lm at 93e6d4a (v0.32.2): LICENSE, README, SERVER.md | OD | Licence; server warning | 8 |\n| MUS | Hugging Face: the meta-models organization page (\"Meta Inc.\", verified) and the Muse-Glimmer-30B model card, read October 19, 2026 | OD | Muse Glimmer 30B: Apache-2.0, August 2026; Muse Spark Open listed | 7 |\n"),
    ("| OLB | Ollama library pages: qwen3, qwen3.5, llama3.2, phi4-mini, granite4, gemma4 | OD | Download sizes | 7 |",
     "| OLB | Ollama library pages: qwen3, qwen3.5, llama3.2, phi4-mini, granite4, gemma4 | OD | Download sizes; granite4's licence line | 7 |"),
    ("`scripts/install.sh`, `app/ollama.iss`, `docs/faq.mdx`, `docs/gpu.mdx`, `docs/windows.mdx`, `docs/api.md`, LICENSE | OD | Engine, installers, network calls, defaults, API, Windows steps | 9 |",
     "`scripts/install.sh`, `app/ollama.iss`, `app/store/store.go`, `app/store/database.go`, `docs/faq.mdx`, `docs/gpu.mdx`, `docs/windows.mdx`, `docs/linux.mdx`, `docs/api.md`, LICENSE | OD | Engine, installers, network calls, the `Survey` setting, defaults, API, setup steps | 9 |"),
    ("| POP | Pope et al., \"Efficiently Scaling Transformer Inference\", arXiv 2211.05102v1, §2 and §4.4 | PP | Weights versus KV cache as the bottleneck | 7 |",
     "| POP | Pope et al., \"Efficiently Scaling Transformer Inference\", arXiv 2211.05102v1, §2 and §4.4 | PP | Weights and KV cache read once per forward pass; which dominates | 7 |"),
    ("| SLM | SchedMD/slurm at ad46cad: META, COPYING | OD | 26.05.5; GPL-2.0 | 9 |",
     "| SLM | SchedMD/slurm at ad46cad: META, COPYING | OD | 26.05.5; GPL version 2 or later | 9 |"),
    ("| A measured speed below the printed ceiling; send back what it prints |",
     "| A measured speed below the printed ceiling; note what it prints |"),
])

patch(D + "cheat.md", [
    ("Q4_K_M           4.8944 bits per weight on Llama 3 8B: 4.58 GiB, 4.91 GB; +2.79% perplexity",
     "Q4_K_M           4.8944 bits per weight on Llama 3 8B: 4.58 GiB, 4.91 GB; +2.79% perplexity\n                 (+2.40% with an importance matrix)"),
    ("Ollama v0.40.5   runs llama.cpp's server; OLLAMA_NO_CLOUD=1; hourly update check in the apps",
     "Ollama v0.40.5   runs llama.cpp's server; OLLAMA_NO_CLOUD=1; hourly update check in the apps\n                 (not stopped by OLLAMA_NO_CLOUD)"),
])
