# Blind check, list A

Each claim below comes with the keys of the sources it rests on; the source list follows.

A001. Public leaderboards help you narrow the field, but each measures something particular (crowd votes on chat answers, a fixed set of exam questions, a weighted mix of tasks), and test questions leak into training data over time, so scores drift upward without the models getting better at your job .  [sources: ARN, GSM, LVB]
A002. The model card tells you the licence, what the model is meant for and how it was tested, when it's filled in .  [sources: HFC, MCR]
A003. After that, the only measurement that answers your question is your own: run your short list on a few dozen of your real tasks and compare (Part 02) .  [sources: SEL]
A004. It is good at teaching a format, a style or a narrow behaviour that prompting can't hold steady, and poor at teaching new facts: on questions about events after training, retrieval beat fine-tuning by 19 to 31 points in one peer-reviewed study .  [sources: OVA]
A005. LoRA, the common method, freezes the model and trains two thin matrices beside each chosen layer, often under 1% of the weights, so it needs far less memory than training everything .  [sources: LOR]
A006. In October 2026 the big hosted services have mostly stopped selling it, so fine-tuning now means an open-weight model on your own or rented hardware .  [sources: GEM, MIS, OAI]
A007. A ranking from crowd votes on pairs of anonymous answers | Arena (formerly Chatbot Arena, LMArena) | Bradley-Terry scores  [sources: ARN]
A008. Test questions that were in the training data | Contamination | Inflates scores  [sources: DEN, GSM]
A009. A benchmark most models now ace | Saturation | Can no longer separate them  [sources: LVB]
A010. A model's documentation page | Model card | Mitchell et al.'s nine sections  [sources: MCR]
A011. Training every weight | Full fine-tuning | 16 bytes per weight with Adam  [sources: ZER]
A012. Training a small add-on instead of the weights | Parameter-efficient fine-tuning (PEFT) | LoRA is the common kind  [sources: PFT]
A013. Two thin matrices whose product updates a frozen layer | LoRA (low-rank adaptation) | ΔW = BA  [sources: LOR]
A014. The width of those matrices | Rank (r) | Trainable: r x (inputs + outputs) per matrix  [sources: LOR]
A015. How strongly the update is applied | alpha; scaling alpha / r | PEFT default 8 / 8  [sources: PFT]
A016. LoRA on a 4-bit frozen model | QLoRA | NF4 and double quantization  [sources: QLR]
A017. Training on pairs of better and worse answers | Preference tuning; DPO | No separate reward model  [sources: DPO]
A018. Training with a score instead of example answers | Reinforcement fine-tuning; GRPO  [sources: TRL]
A019. Learning only from the answer part of each example | Completion-only loss; prompt masking | TRL's default for prompt and completion data  [sources: TRL]
A020. The model's fixed way of laying out a chat as text | Chat template | Wrong template, worse model  [sources: TFM]
A021. A model losing earlier skills after training | Forgetting | LoRA forgets less  [sources: BID]
A022. Arena (arena.ai) | The Chatbot Arena team, later LMArena; its old links now lead to arena.ai (no rename notice was read) | Votes on pairs of anonymous answers to prompts users type; Bradley-Terry scores with confidence intervals | Its paper says users are likely "LLM hobbyists and researchers" and prompts may not reflect production or specialist use ; length and formatting sway votes, so it adds "style control"  [sources: ARN, ARP]
A023. Artificial Analysis Intelligence Index v4.3.2 | Artificial Analysis | A weighted average of 10 evaluations it runs itself: agents 30%, general 30%, coding 20%, scientific reasoning 20% | Mostly English text; some private data sets; an LLM grades open answers; "may not apply directly to every use case"  [sources: AAI]
A024. LiveBench | LiveBench team (ICLR 2025, per its repository) | 18 tasks with objective answers, scored without an LLM judge, refreshed over time against contamination | Its own changelog replaced coding questions "likely heavily contaminated for newer models"; the newest entry was 284 days old on October 19, 2026  [sources: LVB]
A025. HELM | Stanford CRFM | Many scenarios and metrics beyond accuracy | In maintenance mode since June 1, 2026: "no new evaluations will be added to the HELM leaderboards"  [sources: HLM]
A026. Open LLM Leaderboard | Hugging Face | Fixed academic benchmarks run on submitted open models | Retired March 13, 2025, after "over 13K models", because "benchmarks need to follow" new capabilities ; older model cards still quote its numbers  [sources: HFC, OLL]
A027. **The Arena dispute.** "The Leaderboard Illusion" (Singh et al., a preprint) argues that Arena's rankings are distorted: a few providers test many private variants before release and can withhold scores (it counts 27 private variants from Meta before Llama 4), proprietary models are sampled more often, and Google and OpenAI received an estimated 19.2% and 20.4% of Arena's data against 29.7% for 83 open-weight models together .  [sources: ILL]
A028. Arena's reply (May 9, 2025) disputes several numbers, for example that the "112%" gain from extra Arena data was measured on Arena-Hard, a 500-question benchmark judged by an LLM, not on Arena itself, and puts the boost from pre-release testing at "around +11 Elo after 50 tests and 3000 votes" by its own analysis .  [sources: ARP]
A029. Both sides agree on the mechanism: Arena's policy lets providers "test multiple variants of their models pre-release" and receive their own battle data .  [sources: ARP]
A030. **Contamination is measured, not hypothetical.** Zhang et al. wrote new grade-school maths problems in the style of GSM8k (GSM1k) and found accuracy drops of "up to 8%" for some models, with "several families of models showing evidence of systematic overfitting across almost all model sizes", while many frontier models showed little (NeurIPS 2024, Datasets and Benchmarks Track) .  [sources: GSM]
A031. Deng et al. hid one wrong option of MMLU questions and asked models to fill it in: ChatGPT and GPT-4 reproduced it exactly 52% and 57% of the time, which points to test items seen in training (NAACL 2024) .  [sources: DEN]
A032. LiveBench refreshed tasks in November 2025 "to resolve (to some extent) saturation and contamination", and Hugging Face retired its leaderboard because its tasks no longer separated models .  [sources: LVB, OLL]
A033. **The 13-word rule.** GPT-3's authors flagged a test example as possibly contaminated when it shared a run of 13 words with the training data, or, if shorter than 13 words, appeared whole .  [sources: GP3]
A034. Mitchell et al. proposed nine sections for a model card: model details (developer, date, version, licence), intended use (including out-of-scope uses), factors, metrics, evaluation data, training data, quantitative analyses, ethical considerations, and caveats .  [sources: MCR]
A035. They ask for results "disaggregated, that is, broken down by the chosen factors" .  [sources: MCR]
A036. Hugging Face's annotated template admits the evaluation section "is most commonly used to report aggregate evaluation performance on different task benchmarks" .  [sources: HFC]
A037. On Hugging Face a card is the repository's README with a metadata block. `license` is shown and filterable; a custom licence is `license: other` with a name and link, which means you must read it (Part 10) . `base_model` shows whether you are looking at a fine-tune, adapter, quantization or merge of another model, whose licence can still apply .  [sources: HFC]
A038. Scores on a model page are self-reported unless marked: Hugging Face's newer evaluation results show "verified" only when the run happened in its own jobs service with inspect-ai, and "community" for scores proposed by pull request .  [sources: HFC]
A039. From the publishers' own pages, October 16 to 19, 2026 .  [sources: MUS, PUB]
A040. **Licences differ inside one family, so read each card.** Meta's newest open model is not Apache-2.0: Muse Spark Open's card gives the licence as "muse-model-license", gated behind a form (legal name, date of birth, organization), and requires products to "prominently display 'Built with Muse Spark Open'"; above a revenue threshold a separate agreement with Meta is needed .  [sources: MUS]
A041. Muse Glimmer 30B, from the same organization two months earlier, is Apache-2.0 .  [sources: MUS]
A042. Qwen3.8-27B is Apache-2.0 while the Qwen3.8 flagship is "qwen3.8-max" .  [sources: PUB]
A043. Mistral's own docs disagree with each other: one page says open-weight models are "Apache 2.0", another that they are "under the Mistral license", and the models overview lists Apache 2.0, Modified MIT and a non-commercial licence model by model .  [sources: MIS]
A044. **Open weights don't mean small.** Muse Spark Open "requires a GPU with at least 700GB of VRAM for NVFP4 and 2TB for BF16" .  [sources: MUS]
A045. Part 11's fit arithmetic applies: at about Q4_K_M (4.89 bits per weight), Llama 4 Scout's 109 billion weights take 66.6 GB, more than an 80 GB card with a fifth kept free (64 GB), although Meta says it fits one H100 at 4 bits on the fly .  [sources: PUB]
A046. OpenAI: "The best way to find the right model for your workflow is to experiment with different models", using "the same inputs" and keeping "the lightest setting that meets your quality bar" .  [sources: SEL]
A047. Anthropic: "having a good evaluation set is the most important step in the process", and "Test with your actual prompts and data" .  [sources: SEL]
A048. Mistral's evaluation guide: public benchmarks "may not cover real-world customer use cases", so "it is often preferable to create your own evaluation dataset", one hard enough that the models differ: "If every model being tested achieves over 90% accuracy, the differences between them might not be meaningful" .  [sources: SEL]
A049. Muse Glimmer's card recommends "building dedicated evaluation datasets for your use case", Llama 4's says much the same, and Muse Spark Open's card adds that its results "should not be assumed to apply to modified models" .  [sources: MUS, PUB]
A050. Two anchors from vendors: try the smallest model that passes, and change one thing at a time .  [sources: SEL]
A051. (EMNLP 2024) taught three 7B models (Llama2, Mistral, Orca2) 910 questions about US events from August to November 2023, after their training .  [sources: OVA]
A052. Retrieval on the base model beat fine-tuning on the source text and its paraphrases for every model: Mistral 7B scored 0.875 with retrieval against 0.588 fine-tuned on paraphrases, a gap of 28.7 points; across the three models the gap was 19.3 to 31.0 points .  [sources: OVA]
A053. Plain fine-tuning even lowered Llama2 7B's score, from 0.353 to 0.219 .  [sources: OVA]
A054. The authors found fine-tuning absorbed facts better the more paraphrases it saw, and hypothesize that "the knowledge must be repeated in numerous ways" .  [sources: OVA]
A055. Unknown facts were learned much more slowly, and "as the examples with new knowledge are eventually learned, they linearly increase the model's tendency to hallucinate" .  [sources: GEK]
A056. Stopping early on a held-out set avoided most of the harm, and leaving the unknown examples out did as well or better .  [sources: GEK]
A057. One model and one task type; long answers weren't tested .  [sources: GEK]
A058. **Prompt and measure first.** OpenAI: "The prompt engineering process may be all you need in order to get great results for your use case", and "You might even consider writing evals before you start writing prompts" .  [sources: OAI]
A059. Hugging Face's course says fine-tuning "should only be pursued when prompting existing models proves insufficient" .  [sources: HFL]
A060. Two vendor pages still list "domain-specific knowledge" or "new facts" as reasons to fine-tune, with no evidence given; the two studies above say otherwise .  [sources: HFL, MIS]
A061. **What fine-tuning is for.** A fixed output format or style the model must hit every time, a narrow classification or extraction task, a smaller model doing one job that only a larger one could do by prompting, or a behaviour that would otherwise need a very long prompt on every call .  [sources: HFL]

## Sources

- AAI: Artificial Analysis, "Intelligence Benchmarking Methodology" page (Intelligence Index v4.3.2) (class OD)
- ARN: Chiang et al., "Chatbot Arena", ICML 2024, PMLR 235, pp. 8359 to 8388 (mlresearch/v235 at d8ed297; the PDF) (class PR)
- ARP: Arena's blog source (lmarena/lmarena.github.io at 3366281): policy, style control, the May 9, 2025 reply; live copy at arena.ai/blog/our-response (class VB)
- BID: Biderman et al., "LoRA Learns Less and Forgets Less", arXiv 2405.09673v2 (TMLR 2024 per the authors' README; not confirmed) (class PP)
- DEN: Deng et al., NAACL 2024 (Volume 1), pp. 8706 to 8719, doi:10.18653/v1/2024.naacl-long.482 (ACL Anthology data at 0d4dd55) (class PR)
- DPO: Rafailov et al., "Direct Preference Optimization", NeurIPS 2023, pp. 53728 to 53741 (proceedings abstract page) (class PR)
- GEK: Gekhman et al., "Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?", EMNLP 2024, pp. 7765 to 7784 (ACL Anthology PDF and data) (class PR)
- GEM: Google, Gemini API "Fine-tuning" page (last updated 2026-04-28) (class OD)
- GP3: Brown et al., "Language Models are Few-Shot Learners", arXiv 2005.14165: Table 2.1; Section 4 (class PP)
- GSM: Zhang et al., GSM1k, NeurIPS 2024 Datasets and Benchmarks Track (proceedings abstract page) (class PR)
- HFC: huggingface/hub-docs at 76be11b: model-cards.md, model-card-annotated.md, eval-results.md (class OD)
- HFL: huggingface/course at 8b893f0, chapter 11, "When to Use SFT" (class OD)
- HLM: stanford-crfm/helm at 63754d0: README, docs/maintenance_mode.md (class OD)
- ILL: Singh et al., "The Leaderboard Illusion", arXiv 2504.20879 (abstract) (class PP)
- LOR: Hu et al., "LoRA", arXiv 2106.09685v2: Sections 4.1, 4.2, 5.1, Table 4; ICLR 2022 poster page (class PR)
- LVB: LiveBench/LiveBench at 1d1006a: README, changelog.md (class OD)
- MCR: Mitchell et al., "Model Cards for Model Reporting", arXiv 1810.03993 (FAT* '19 per the authors' PDF; the publisher's page didn't load) (class PR)
- MIS: mistralai/platform-docs-public at e7de7a7 (deployment, migration guide, deprecated fine-tuning pages, evaluation guide); docs.mistral.ai models overview; mistralai/mistral-finetune README (archived) (class OD)
- MUS: Hugging Face: meta-models organization page; Muse-Glimmer-30B card; Muse-Spark-Open-816B-A42B card (gated; licence summary only) (class OD)
- OAI: OpenAI developer docs: deprecations page ("Update to OpenAI's self-serve fine-tuning"; 2026-04-22 and 2026-10-14 entries); model-optimization, supervised fine-tuning and DPO guides; Terms of Use (effective January 1, 2026) (class OD)
- OLL: Hugging Face: Open LLM Leaderboard discussion 1135 (retirement post) and organization page (class OD)
- OVA: Ovadia et al., "Fine-Tuning or Retrieval?", EMNLP 2024, pp. 237 to 250 (ACL Anthology PDF and data) (class PR)
- PFT: huggingface/peft at v0.21.2 (eaa35c7): README, lora/config.py, utils/constants.py, lora/layer.py, LICENSE (class OD)
- PUB: Publishers' pages: QwenLM/Qwen3.8 README (2ea10dc) and the Qwen3.8 cards; openai/gpt-oss (5681a6b); ibm-granite Granite 4.1 README; microsoft/PhiCookBook and the Phi-4-reasoning-vision card; deepseek-ai organization and V4.1-Flash card; llama-models Llama 4 card; Gemma 4 (Part 11) (class OD)
- QLR: Dettmers et al., "QLoRA", NeurIPS 2023 (proceedings page); artidoro/qlora at 7f4e95a (class PR)
- SEL: OpenAI model-selection guide; Anthropic "Choosing the right model"; Mistral evaluation guide (docs source) (class OD)
- TFM: huggingface/transformers at v5.20.2: docs cpu.md, apple_silicon.md, chat_templating.md (class OD)
- TRL: huggingface/trl at v1.16.0 (1b5c75e): usage_stats.md, trainer/base_trainer.py, dataset_formats.md, sft_trainer.md, lora_without_regret.md, grpo_trainer.md (class OD)
- ZER: Rajbhandari et al., "ZeRO", arXiv 1910.02054, Section 3 (class PP)
