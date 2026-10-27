# Blind check, list B

Each claim below comes with the keys of the sources it rests on; the source list follows.

B001. With Adam in mixed precision, the ZeRO paper counts 2 bytes for the 16-bit weights, 2 for gradients and 12 for the optimizer (a 32-bit copy of the weights plus two moment estimates): "In total, this results in 2Ψ+2Ψ+KΨ=16Ψ bytes" for Ψ weights, before activations .  [sources: ZER]
B002. So a 1.5B model needs "at least 24GB" and a 7B model 112 GB .  [sources: ZER]
B003. LLaMA-Factory's README estimates 120 GB for a 7B model, ZeRO's figure plus a margin it doesn't explain .  [sources: LLF]
B004. **LoRA.** Hu et al. freeze the weight matrix W0 and learn an update ΔW = BA, where B is outputs x r and A is r x inputs, with r much smaller than either: the layer computes W0x + BAx .  [sources: LOR]
B005. A starts random and B at zero, so training starts from the unchanged model; the update is scaled by alpha / r .  [sources: LOR]
B006. On GPT-3 175B the paper reports training memory falling from 1.2 TB to 350 GB, and the checkpoint from 350 GB to 35 MB with r = 4 on two matrices per layer .  [sources: LOR]
B007. After training, BA can be added into W0, so inference costs nothing extra .  [sources: LOR]
B008. Qwen2.5-3B-Instruct, r = 16, PEFT's default targets | "trainable params: 3,686,400 \ | \ | all params: 3,089,625,088" (PEFT 0.21.2 README) | 3,686,400 and 3,085,938,688 + 3,686,400 = 3,089,625,088  [sources: PFT]
B009. GPT-3 175B, LoRA on Wq and Wv, r = 1 and r = 8 | 4.7M and 37.7M (LoRA paper, Table 4) | 4,718,592 and 37,748,736  [sources: LOR]
B010. Same, r = 4, saved at 2 bytes per weight | "35MB" (Section 4.2) | 37.7 MB (36.0 MiB)  [sources: LOR]
B011. Qwen3-0.6B, all weights | "0.6B", "Non-Embedding: 0.44B" (model card) | 596,049,920; 440,466,432 without the embedding  [sources: QCF]
B012. GPT-3's shape (96 layers, width 12,288) is from its paper's Table 2.1 .  [sources: GP3]
B013. Qwen2 models add a bias to q, k and v, and Qwen3 adds a small norm to q and k; the counts match only when those are included .  [sources: QCF]
B014. **Which layers.** The LoRA paper adapted only the query and value projections "in most experiments for simplicity" , and PEFT 0.21.2 still defaults to `q_proj` and `v_proj` for Llama, Mistral, Qwen2 and Qwen3 models, with r = 8 and alpha = 8 .  [sources: LOR, PFT]
B015. QLoRA found LoRA "on all linear transformer block layers" was needed to match full fine-tuning .  [sources: QLR]
B016. Biderman et al. found LoRA nearly matched full fine-tuning for instruction tuning only at rank 256 on all modules, and advise alpha = 2r and a learning rate about ten times full fine-tuning's .  [sources: BID]
B017. TRL's docs relay Thinking Machines' "LoRA Without Regret" (a company blog): adapt all weight matrices, and "Attention-only LoRA underperforms even when using a higher rank" .  [sources: TRL]
B018. So set `target_modules="all-linear"` unless memory forbids it, and treat r as a setting to test .  [sources: BID, PFT]
B019. **LoRA learns less and forgets less.** Biderman et al. compared LoRA with full fine-tuning of Llama-2-7B on code and maths .  [sources: BID]
B020. In continued pretraining on billions of tokens, the best LoRA trailed by 3.9 points on HumanEval and 9.0 on GSM8K; in instruction tuning it came within 0.8 points or matched .  [sources: BID]
B021. It also kept more of the model's general skills: on code instruction tuning, 0.509 against 0.414 on an average of three general benchmarks .  [sources: BID]
B022. A preprint, with its TMLR venue stated only by the authors .  [sources: BID]
B023. (NeurIPS 2023) back-propagate through a frozen 4-bit model into LoRA adapters, which "reduces memory usage enough to finetune a 65B parameter model on a single 48GB GPU" .  [sources: QLR]
B024. Three parts: the NF4 data type for normally distributed weights, in blocks of 64; double quantization, which shrinks each block's scale and cuts its cost from 0.5 to 0.127 bits per weight, "approximately 3 GB for a 65B model"; and paged optimizers, which move optimizer state to CPU memory during spikes .  [sources: QLR]
B025. NF4 is a bitsandbytes type for training, not a GGUF type (Part 11) .  [sources: QLR]
B026. **One line each on the other methods.** *DoRA* (ICML 2024) splits each weight into a magnitude and a direction and uses LoRA for the direction; its authors report it "consistently outperforms LoRA" on their tasks, and PEFT offers it as `use_dora=True` .  [sources: DOR, PFT]
B027. *DPO* (NeurIPS 2023) trains on pairs of a preferred and a rejected answer directly, "essentially solving a classification problem on the human preference data", with no separate reward model .  [sources: DPO]
B028. *GRPO*, in TRL, samples several answers per prompt, scores each with a reward function, and learns from each answer's score relative to the group's average .  [sources: TRL]
B029. **Formats.** TRL 1.16.0 names them: conversational (`messages`, each with `role` and `content`), language modelling (`text`), prompt and completion, and preference (`prompt`, `chosen`, `rejected`) .  [sources: TRL]
B030. OpenAI's DPO format used different names (`input`, `preferred_output`, `non_preferred_output`) ; MLX-LM reads `chat`, `tools`, `completions` and `text` ; LLaMA-Factory reads "alpaca" and "sharegpt" .  [sources: LLF, MLX, OAI]
B031. **Templates.** Chat models expect the exact control tokens they were trained with: "with the wrong control tokens, these models would have drastically worse performance" .  [sources: TFM]
B032. TRL applies the model's chat template to conversational data for you, and for prompt and completion data it computes loss "on the completion tokens only, ignoring the prompt tokens" by default .  [sources: TRL]
B033. MLX-LM computes loss on every token unless you pass `--mask-prompt` .  [sources: MLX]
B034. **How many examples.** OpenAI's guide set a minimum of 10 and said improvements usually show from 50 to 100 well-made examples .  [sources: OAI]
B035. **Check before you train.** `datacheck.py` reports, per file: each example's format; examples a trainer would reject or learn nothing from (an unknown role, empty content, a conversation that doesn't end with the assistant, identical chosen and rejected answers); exact duplicates; and test examples that share 13 words in a row with training data, GPT-3's contamination rule .  [sources: GP3]
B036. Qi et al. fine-tuned GPT-3.5 Turbo through OpenAI's API and Llama-2-7b-Chat, and scored 330 harmful instructions with a GPT-4 judge .  [sources: QIS]
B037. Ten harmful examples raised GPT-3.5 Turbo's harmfulness rate from 1.8% to 88.8%, for "less than $0.20" in 2023 .  [sources: QIS]
B038. Ten examples with no toxic content, training the model to put obedience first, raised it to 87.3% .  [sources: QIS]
B039. Even one epoch on ordinary helpful data weakened safety: GPT-3.5 Turbo on the Alpaca data set went from 5.5% to 31.8% .  [sources: QIS]
B040. These are 2023 models and the preprint's first version; the authors give ICLR 2024 as the venue, not confirmed on the conference's page .  [sources: QIS]
B041. Re-run a safety test after every fine-tune, not only your task eval; screening data for toxic text alone would have missed the "obedience" examples .  [sources: QIS]
B042. And Muse Spark Open's card says the same about its own scores: they "should not be assumed to apply to modified models" .  [sources: MUS]
B043. OpenAI's hosted service checked each tuned model "across 13 distinct safety categories" before deployment ; your own run has no such check unless you add one.  [sources: OAI]
B044. **OpenAI** is "winding down the fine-tuning platform" .  [sources: OAI]
B045. Its deprecations page: from May 7, 2026, organizations that had never fine-tuned can't create jobs; from July 2, 2026, neither can those with no inference on a fine-tuned model in the past 60 days; and on January 6, 2027, "Active existing customers will no longer be able to create new fine-tuning jobs" .  [sources: OAI]
B046. Tuned models keep serving until their base models are retired; several, including `ft-gpt-4` and `ft-gpt-3.5-turbo`, are removed on October 23, 2026 .  [sources: OAI]
B047. **Google's Gemini API:** "we no longer have a model available which supports fine-tuning in the Gemini API or AI Studio" since May 2025; tuning moved to its enterprise platform, which wasn't read .  [sources: GEM]
B048. **Mistral** marks its fine-tuning "deprecated and ... no longer actively supported" in its docs, and archived its open-source trainer .  [sources: MIS]
B049. **Anthropic:** the only offer found was Claude 3 Haiku through Amazon Bedrock (2024); that model left Anthropic's API on April 20, 2026, and Bedrock's current status wasn't checked .  [sources: ANT]
B050. Read from each project's source at the version named, October 19, 2026 .  [sources: AXO, LCF, LLF, MLX, PFT, PYPI, TRL, TTN, UNS]
B051. **Telemetry differs by library and has different switches:** `DO_NOT_TRACK=1` stops TRL's and Axolotl's, but not Unsloth's or Gradio's .  [sources: AXO, HHB, LLF, TRL, UNS]
B052. **llama.cpp's fine-tuning is not LoRA:** its README calls the code "very much WIP", it trains every weight in 32-bit, and it says a tiny test model and Llama 3.2 1B "seem to work with 24 GB of memory" .  [sources: LCF]
B053. **Versions clash.** Axolotl 0.21.0 pins `trl==1.14.1`; Unsloth 2026.10.7 caps TRL at 1.15.0 and transformers at 5.17.0; LLaMA-Factory 0.9.5 caps PEFT at 0.18.1 and TRL at 0.24.0 .  [sources: PYPI]
B054. **On an ordinary computer.** Transformers' Trainer, which PEFT and TRL build on, trains on a CPU with `use_cpu=True` and says "CPU training works well when GPUs aren't available", with no speed figures .  [sources: TFM]
B055. On a Mac, both PyTorch's MPS backend and MLX-LM are documented for training; MLX-LM's guide gives the only measured consumer figure found, "about 250 tokens-per-second" for LoRA on Mistral 7B on an M1 Max with 32 GB .  [sources: MLX, TFM]
B056. - **Apache-2.0** (Section 4 of the licence): give recipients a copy of the licence, mark files you changed, and keep the notices in any NOTICE file .  [sources: APL]
B057. - **Llama 3** (April 18, 2024): show "Built with Meta Llama 3", put "Llama 3" at the beginning of any fine-tuned model's name you distribute, and "You will not use the Llama Materials or any output or results of the Llama Materials to improve any other large language model" .  [sources: LLL]
B058. Show "Built with Llama", and if you use Llama "or any outputs or results" to "create, train, fine tune, or otherwise improve an AI model" that you distribute, "include 'Llama' at the beginning of any such AI model name" .  [sources: LLL]
B059. - **Muse Model License:** "Built with Muse Spark Open" in the product's interface, a revenue threshold above which Meta wants a separate agreement, and a gated text to read first .  [sources: MUS]
B060. - **Hosted models' outputs:** OpenAI's terms for individuals forbid using output "to develop models that compete with OpenAI"; Anthropic's commercial terms forbid using its services "to build a competing product or service, including to train competing AI models", while both say you own your outputs .  [sources: ANT, OAI]
B061. Llama 3 8B as the local example (P10-09b) | Outdated, with more detail than Part 11 gave: Meta's newest open model is Muse Spark Open (October 15, 2026) under a custom, gated licence, after Muse Glimmer 30B (Apache-2.0, August 2026). Llama 3's licence also required "Llama 3" at the start of a shared fine-tune's name; from Llama 3.1 the ban on improving other models is gone and the prefix is "Llama" | 3.4, 3.12  [sources: LLL, MUS]
B062. GGUF versus AWQ versus GPTQ (B4-10) | Corrected in Part 11, and unchanged. One addition: Meta publishes its own GGUF of Muse Glimmer 30B, so check `base_model` and the uploader rather than assuming a GGUF comes from a third party | 3.3  [sources: HFC, MUS]
B063. "Soft-prompt alignment (RLHF)" (B2-08) | Corrected in the ledger. This part adds the training methods themselves: SFT and LoRA change or add weights, DPO trains on preference pairs, GRPO on scores | 3.7  [sources: DPO, LOR, TRL]
B064. GPT-4 as a judge (P9-12) | Still outdated: fine-tuned GPT-4 models are removed with their base on October 23, 2026 | 3.10  [sources: OAI]
B065. Routing easy queries to smaller models (P8-02) | Consistent with vendors' model-selection advice: keep the lightest model that meets your bar | 3.5  [sources: SEL]
B066. Llama Guard is a model fine-tuned for safety (P12-03) | Settled in Part 10. The reverse also holds: fine-tuning can remove a model's safety behaviour, even on harmless data | 3.9  [sources: QIS]
B067. *A leaderboard retired by its own operator* .  [sources: OLL]
B068. *One publisher, two licences, two months apart* .  [sources: MUS]
B069. *A platform closing* .  [sources: OAI]
B070. For training on a processor, smaller is faster; this example uses Qwen3-0.6B (Apache-2.0), whose shape the lab knows .  [sources: QCF]
B071. *Step 5, after training.* Run the same 40 notes; ship only if the paired test (Part 02) says the tuned model beats the prompted one, and run a safety test too, since even harmless data can weaken refusals .  [sources: QIS]
B072. *Step 6, share.* Qwen3-0.6B is Apache-2.0: include the licence, mark what changed, keep any notices .  [sources: APL]
B073. Had the base been Llama 3.1 or later, the model's name would have to start with "Llama" .  [sources: LLL]
B074. Checked October 19, 2026 .  [sources: PYPI]
B075. The lab's scripts | Parameter counts, memory, data checks, decision rules | This series | Python 3.11 to 3.13, standard library | No | Lab zip  [sources: AXO, LLF, MLX, PFT, PYPI, TFM, TRL, UNS]
B076. PyTorch | The training engine under everything below | PyPI gives a combined expression for its bundled parts: Apache-2.0, BSD-2-Clause, BSD-3-Clause, BSL-1.0 and MIT | Windows, macOS, Linux; Python 3.10 or later | No | 2.14.1 (Windows wheel 124 MB)  [sources: AXO, LLF, MLX, PFT, PYPI, TFM, TRL, UNS]
B077. transformers | Loads models and tokenizers; the Trainer | Apache-2.0 | As PyTorch | No; gated models need a Hugging Face account (Part 10) | 5.20.2  [sources: AXO, LLF, MLX, PFT, PYPI, TFM, TRL, UNS]
B078. PEFT | LoRA and other adapters | Apache-2.0 | As PyTorch | No | 0.21.2  [sources: AXO, LLF, MLX, PFT, PYPI, TFM, TRL, UNS]
B079. TRL | SFT, DPO and GRPO trainers | Apache-2.0 | As PyTorch; Python 3.11 or later | No; telemetry on by default | 1.16.0  [sources: AXO, LLF, MLX, PFT, PYPI, TFM, TRL, UNS]
B080. MLX-LM | Fine-tuning on Apple silicon | MIT | macOS on Apple silicon | No | 0.32.2  [sources: AXO, LLF, MLX, PFT, PYPI, TFM, TRL, UNS]
B081. Unsloth | Faster LoRA on GPUs | Apache-2.0 with AGPL-3.0 files | GPU or Apple silicon | No; statistics on by default | 2026.10.7  [sources: AXO, LLF, MLX, PFT, PYPI, TFM, TRL, UNS]
B082. Axolotl | Fine-tuning from a YAML file | Apache-2.0 | NVIDIA or AMD GPU; Windows through WSL2 or Docker; Python 3.12 or later | No; telemetry on by default | 0.21.0  [sources: AXO, LLF, MLX, PFT, PYPI, TFM, TRL, UNS]
B083. LLaMA-Factory | Web UI and command line | Apache-2.0 | NVIDIA, Ascend; Python 3.11 or later | No; the web UI reports usage | 0.9.5  [sources: AXO, LLF, MLX, PFT, PYPI, TFM, TRL, UNS]
B084. Sources: Sections 3.7 and 3.11 .  [sources: AXO, LLF, MLX, PFT, PYPI, TFM, TRL, UNS]
B085. - **Best default for a solo builder with a GPU:** transformers plus PEFT with your own short loop or TRL's `SFTTrainer`, LoRA on all linear layers; set `HF_HUB_DISABLE_TELEMETRY=1` before TRL runs .  [sources: PFT, TRL]
B086. - **On a Mac:** MLX-LM's `mlx_lm.lora`, which also does QLoRA when given a quantized model .  [sources: MLX]
B087. - **On an ordinary PC with no GPU:** transformers and PEFT on the processor, with a model under 1B parameters, as in reader test R3 .  [sources: TFM]
B088. Unsloth and Axolotl won't train there .  [sources: AXO, UNS]
B089. - **Faster on NVIDIA:** Unsloth, after reading its two licence files, with `UNSLOTH_DISABLE_STATISTICS` set .  [sources: UNS]
B090. - **Skip for new work:** torchtune, which says it is "no longer actively maintained"; llama.cpp's fine-tuning, an experiment; hosted fine-tuning on OpenAI, Gemini or Mistral, which is closed or deprecated .  [sources: GEM, LCF, MIS, OAI, TTN]
B091. This installs PyTorch, transformers and PEFT into the lab's environment (about 170 MB in about 40 packages on Windows, most of it PyTorch's 124 MB wheel, estimated from PyPI ), and downloads SmolLM2-135M-Instruct (Apache-2.0, 135 million weights) from Hugging Face once; skip it if you'd rather not .  [sources: PYPI, QCF]
B092. The script uses a plain PyTorch loop rather than TRL, so nothing pings a server, and it sets `HF_HUB_DISABLE_TELEMETRY=1` and `DO_NOT_TRACK=1` before importing anything .  [sources: HHB, TRL]
B093. It masks each prompt so the model learns only the answer, the same default TRL uses for prompt and completion data .  [sources: TRL]
B094. **Data:** the published configurations of Llama 3 8B, Qwen2.5-3B-Instruct, Qwen3-0.6B, SmolLM2-135M-Instruct and GPT-3, and the figures named in each check ; the support notes in `data/` are invented .  [sources: GP3, LOR, PFT, QCF]
B095. - *"The top of the leaderboard is the best model for me."* Rankings measure votes or fixed tests; the vendors themselves say to test on your own data .  [sources: ARN, SEL]
B096. - *"Fine-tuning teaches the model our documents."* New facts are learned slowly and raise hallucination; retrieval beat fine-tuning by 19 to 31 points on new facts .  [sources: GEK, OVA]
B097. - *"LoRA is a smaller model."* LoRA adds small matrices beside a full, frozen model; you still load every weight .  [sources: LOR]
B098. - *"Open-weight means Apache-2.0."* Meta, Qwen and Mistral each publish models under several licences .  [sources: MIS, MUS, PUB]
B099. - *"Harmless training data can't hurt safety."* One epoch on Alpaca raised GPT-3.5 Turbo's harmfulness rate from 5.5% to 31.8% .  [sources: QIS]
B100. *Answers.* (1) Contamination (test items in training data) and saturation (a test most models ace) .  [sources: DEN, GSM, LVB]
B101. (2) `base_model`; the base model's licence and limits can still apply .  [sources: HFC]
B102. (3) Retrieve: facts that change belong in retrieval, and fine-tuned facts raise hallucination .  [sources: GEK, OVA]
B103. (4) 2 bytes of weights, 2 of gradients and 12 of optimizer state (a 32-bit copy plus two moments) .  [sources: ZER]
B104. (5) Its name must start with "Llama", and you must show "Built with Llama" and ship the licence .  [sources: LLL]
B105. **Best next resources** (checked to exist on October 19, 2026): the LoRA paper ; QLoRA ; Ovadia et al. and Gekhman et al. ; PEFT's README and LoRA docs ; TRL's dataset formats and SFT pages ; Mitchell et al.'s model cards paper .  [sources: GEK, LOR, MCR, OVA, PFT, QLR, TRL]
B106. - **The fine-tune or retrieve evidence is narrow.** Two peer-reviewed studies: three 2023 7B models on one set of news questions, and one model (PaLM 2-S) on closed-book questions .  [sources: GEK, OVA]
B107. - **Preprints and blogs carry weight here.** Biderman et al. and Qi et al. are preprints whose venues come only from their authors' pages; "LoRA Without Regret" is a company blog relayed by TRL's docs; ZeRO's 16 bytes is from the arXiv version .  [sources: BID, QIS, TRL, ZER]
B108. - **Rankings were read, not re-run.** Arena's live policy page renders by script and couldn't be read; the Leaderboard Illusion dispute rests on numbers neither side published in full .  [sources: ARP, ILL]
B109. - **Network behaviour was read, not watched.** The telemetry in TRL, Axolotl, Unsloth and Gradio comes from their code; Axolotl's docs mention a 10-second pause at startup that its code at this tag doesn't show .  [sources: AXO]
B110. *Claim ledger P10-09b* should add that Meta's newest open model, Muse Spark Open (October 15, 2026), is under a custom, gated licence, and that Llama 3's licence also required "Llama 3" at the start of a shared fine-tune's name; from Llama 3.1 the prefix is "Llama" and the ban on improving other models is gone .  [sources: LLL, MUS]

## Sources

- ANT: Anthropic: "Fine-tune Claude 3 Haiku in Amazon Bedrock" (2024 article); model deprecations page; Commercial Terms of Service (effective June 17, 2025) (class VB, OD)
- APL: Apache License 2.0, Section 4, as shipped in PEFT's LICENSE (class OD)
- ARN: Chiang et al., "Chatbot Arena", ICML 2024, PMLR 235, pp. 8359 to 8388 (mlresearch/v235 at d8ed297; the PDF) (class PR)
- ARP: Arena's blog source (lmarena/lmarena.github.io at 3366281): policy, style control, the May 9, 2025 reply; live copy at arena.ai/blog/our-response (class VB)
- AXO: axolotl-ai-cloud/axolotl at v0.21.0 (1f1eb05): LICENSE, README, telemetry manager and docs, installation and Mac docs (class OD)
- BID: Biderman et al., "LoRA Learns Less and Forgets Less", arXiv 2405.09673v2 (TMLR 2024 per the authors' README; not confirmed) (class PP)
- DEN: Deng et al., NAACL 2024 (Volume 1), pp. 8706 to 8719, doi:10.18653/v1/2024.naacl-long.482 (ACL Anthology data at 0d4dd55) (class PR)
- DOR: Liu et al., "DoRA", ICML 2024, PMLR 235, pp. 32100 to 32121 (mlresearch/v235) (class PR)
- DPO: Rafailov et al., "Direct Preference Optimization", NeurIPS 2023, pp. 53728 to 53741 (proceedings abstract page) (class PR)
- GEK: Gekhman et al., "Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?", EMNLP 2024, pp. 7765 to 7784 (ACL Anthology PDF and data) (class PR)
- GEM: Google, Gemini API "Fine-tuning" page (last updated 2026-04-28) (class OD)
- GP3: Brown et al., "Language Models are Few-Shot Learners", arXiv 2005.14165: Table 2.1; Section 4 (class PP)
- GSM: Zhang et al., GSM1k, NeurIPS 2024 Datasets and Benchmarks Track (proceedings abstract page) (class PR)
- HFC: huggingface/hub-docs at 76be11b: model-cards.md, model-card-annotated.md, eval-results.md (class OD)
- HHB: huggingface_hub 2.2.0 wheel: constants.py, utils/_telemetry.py (class OD)
- ILL: Singh et al., "The Leaderboard Illusion", arXiv 2504.20879 (abstract) (class PP)
- LCF: ggml-org/llama.cpp at b11739: examples/training README and finetune.cpp (class OD)
- LLF: hiyouga/LLaMA-Factory at v0.9.5: LICENSE, README (memory table, Windows), data README; Gradio 5.49.1 analytics.py (class OD)
- LLL: meta-llama/llama-models at 0e0b8c5: models/llama3, llama3_1, llama3_2, llama4 LICENSE (class OD)
- LOR: Hu et al., "LoRA", arXiv 2106.09685v2: Sections 4.1, 4.2, 5.1, Table 4; ICLR 2022 poster page (class PR)
- LVB: LiveBench/LiveBench at 1d1006a: README, changelog.md (class OD)
- MCR: Mitchell et al., "Model Cards for Model Reporting", arXiv 1810.03993 (FAT* '19 per the authors' PDF; the publisher's page didn't load) (class PR)
- MIS: mistralai/platform-docs-public at e7de7a7 (deployment, migration guide, deprecated fine-tuning pages, evaluation guide); docs.mistral.ai models overview; mistralai/mistral-finetune README (archived) (class OD)
- MLX: ml-explore/mlx-lm at v0.32.2: LICENSE, mlx_lm/LORA.md, lora.py (class OD)
- MUS: Hugging Face: meta-models organization page; Muse-Glimmer-30B card; Muse-Spark-Open-816B-A42B card (gated; licence summary only) (class OD)
- OAI: OpenAI developer docs: deprecations page ("Update to OpenAI's self-serve fine-tuning"; 2026-04-22 and 2026-10-14 entries); model-optimization, supervised fine-tuning and DPO guides; Terms of Use (effective January 1, 2026) (class OD)
- OLL: Hugging Face: Open LLM Leaderboard discussion 1135 (retirement post) and organization page (class OD)
- OVA: Ovadia et al., "Fine-Tuning or Retrieval?", EMNLP 2024, pp. 237 to 250 (ACL Anthology PDF and data) (class PR)
- PFT: huggingface/peft at v0.21.2 (eaa35c7): README, lora/config.py, utils/constants.py, lora/layer.py, LICENSE (class OD)
- PUB: Publishers' pages: QwenLM/Qwen3.8 README (2ea10dc) and the Qwen3.8 cards; openai/gpt-oss (5681a6b); ibm-granite Granite 4.1 README; microsoft/PhiCookBook and the Phi-4-reasoning-vision card; deepseek-ai organization and V4.1-Flash card; llama-models Llama 4 card; Gemma 4 (Part 11) (class OD)
- PYPI: PyPI JSON API, October 19, 2026 (class OD)
- QCF: config.json of Qwen2.5-3B-Instruct, Qwen3-0.6B and SmolLM2-135M-Instruct; the Qwen3-0.6B and SmolLM2 cards (class OD)
- QIS: Qi et al., "Fine-tuning Aligned Language Models Compromises Safety", arXiv 2310.03693v1 (ICLR 2024 per the authors' README; not confirmed) (class PP)
- QLR: Dettmers et al., "QLoRA", NeurIPS 2023 (proceedings page); artidoro/qlora at 7f4e95a (class PR)
- SEL: OpenAI model-selection guide; Anthropic "Choosing the right model"; Mistral evaluation guide (docs source) (class OD)
- TFM: huggingface/transformers at v5.20.2: docs cpu.md, apple_silicon.md, chat_templating.md (class OD)
- TRL: huggingface/trl at v1.16.0 (1b5c75e): usage_stats.md, trainer/base_trainer.py, dataset_formats.md, sft_trainer.md, lora_without_regret.md, grpo_trainer.md (class OD)
- TTN: pytorch/torchtune: v0.6.1 LICENSE; main README (bd2a0fc) (class OD)
- UNS: Unsloth 2026.10.7 and unsloth_zoo 2026.10.7 wheels from PyPI; unslothai/unsloth at 73d2598 (README, device_type.py, models/_utils.py) (class OD)
- ZER: Rajbhandari et al., "ZeRO", arXiv 1910.02054, Section 3 (class PP)
