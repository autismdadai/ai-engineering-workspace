# The AI Engineering Stack, Part 12: Adapting Models

*October 19, 2026; reader tests added October 20, 2026. Part 12 of 13 (claude/engineering-stack-plan.md). Tags in this part: 182 [V], 76 [T], 10 [R], 23 [U], 20 [I], counted in Sections 1 to 12 and the checks after them. Still open: no model was trained or evaluated on the test machine, which has no GPU and can't reach Hugging Face; fine-tuning is described from papers, library source code and vendor documentation, the lab's arithmetic reproduces published figures to the parameter [T], and a small LoRA run, written for your own computer, passed on the owner's Windows PC on October 20, 2026 [T]. Rankings and leaderboards were read, not re-run. Hosted fine-tuning was read from vendors' pages only; no account was opened.*

**What this part gives you.** Two decisions. **Which model?** Where public comparisons come from and how far to trust each, why benchmark scores drift upward over time, what a model card should tell you, and why every serious source ends with the same advice: test the candidates on your own task. **Should you change the model?** When fine-tuning helps and when retrieval or a better prompt is the right tool, what LoRA and QLoRA actually train and how much memory they need, how to check training data before you use it, and what changes after you fine-tune (safety, licence duties). The lab counts trainable parameters from a model's configuration file and reproduces the numbers PEFT and the LoRA paper print, sizes training memory, checks a data set for duplicates and test leaks, and encodes the decision guide so you can argue with it.

## How to read this part

The tags are Part 01's. **[V: KEY]** points to Section 12, which gives each source's class and the place used. **[T]** ran on the test machine. **[R]** is a reader test. **[U]** names what would settle it. **[I]** is invented for teaching. Source classes: official documentation, specifications and source code (OD), peer-reviewed (PR), preprint (PP), vendor blog (VB). A publisher's own page is the authority on what its model is and under which licence; its benchmark scores are claims until someone else reproduces them. References like "ledger P10-09b" point to rows of claude/engineering-stack-claim-ledger.md, this series' audit of the Gemini report.

**Units.** A model "8B" has about 8 billion weights (parameters). GB is a billion bytes. A rank r of 16 means each adapted matrix gets two thin matrices 16 wide. "Points" means percentage points.

**The test machine:** Ubuntu 24.04 in a cloud container, October 19, 2026, with Python 3.13.16, 3.12.3 and 3.11.17, 2 processors and 7.8 GB of memory. No GPU.

**This part covers two topics** (plan, Section 7), both in the **Model** layer: T26, choosing a model, and T27, fine-tuning. Part 02 covers evals, which both topics lean on; Part 05 covers retrieval; Part 10 covers licences; Part 11 covers whether a model fits and how fast it runs.

## 1. In plain words

**T26, choosing a model.** Hundreds of models are published, and every publisher shows a table where its model wins. Public leaderboards help you narrow the field, but each measures something particular (crowd votes on chat answers, a fixed set of exam questions, a weighted mix of tasks), and test questions leak into training data over time, so scores drift upward without the models getting better at your job [V: ARN, GSM, LVB]. The model card tells you the licence, what the model is meant for and how it was tested, when it's filled in [V: MCR, HFC]. After that, your own test answers your question best: run your short list on a set of your real tasks and compare (Part 02); Mistral's guide says 100 good test cases "can be enough to provide a meaningful signal" [V: SEL].

*Analogy.* Hiring. Rankings and references get you a short list; the work sample you set decides.

**T27, fine-tuning.** Fine-tuning means training an existing model a little more on your own examples, so its weights change. It is good at teaching a format, a style or a narrow behaviour that prompting can't hold steady [V: HFL], and poor at teaching new facts: on questions about events after training, retrieval beat fine-tuning by 19 to 37 percentage points in one peer-reviewed study [V: OVA][T]. LoRA, the common method, freezes the model and trains two thin matrices beside each chosen layer, often under 1% of the weights, so it needs far less memory than training everything [V: LOR]. In October 2026 the big hosted services are closing it to newcomers: OpenAI's is shut to new organizations, Gemini's API has no tunable model, and Mistral's docs mark it deprecated [V: OAI, GEM, MIS]. For anyone starting now, that points to an open-weight model on your own or rented hardware [I].

*Analogy.* Prompting is giving a skilled temp worker written instructions; retrieval is giving them the filing cabinet; fine-tuning is sending them on a training course. The course is worth it for a habit they must show every day, not for facts that change next week.

**Where it sits in the stack** (plan, Section 5). The Model layer: which weights do the work. Everything above it (context, tools, agents) is built on that choice, and everything below (runtime, hardware) has to carry it.

## 2. Definitions

Every term is also in claude/engineering-stack-glossary.md.

| Plain words | Technical term | Notes |
|---|---|---|
| A ranking from crowd votes on pairs of anonymous answers | Chatbot Arena (its links now lead to arena.ai) | Bradley-Terry scores [V: ARN, ARP] |
| Test questions that were in the training data | Contamination | Inflates scores [V: GSM, DEN] |
| A benchmark most models now ace | Saturation | Can no longer separate them [V: LVB] |
| A model's documentation page | Model card | Mitchell et al.'s nine sections [V: MCR] |
| Weights you can download and run yourself | Open-weight model | Not the same as open source (Part 10) |
| Training a model further on your own examples | Fine-tuning; supervised fine-tuning (SFT) | Weights change |
| Training every weight | Full fine-tuning | 16 bytes per weight with Adam [V: ZER] |
| Training a small add-on instead of the weights | Parameter-efficient fine-tuning (PEFT) | LoRA is the common kind [V: PFT] |
| Two thin matrices whose product updates a frozen layer | LoRA (low-rank adaptation) | ΔW = BA [V: LOR] |
| The width of those matrices | Rank (r) | Trainable: r x (inputs + outputs) per matrix [V: LOR] |
| How strongly the update is applied | alpha; scaling alpha / r | PEFT default 8 / 8 [V: PFT] |
| The saved LoRA matrices | Adapter | Megabytes, not gigabytes [T] |
| LoRA on a 4-bit frozen model | QLoRA | NF4 and double quantization [V: QLR] |
| Training on pairs of better and worse answers | Preference tuning; DPO | No separate reward model [V: DPO] |
| Training with a score instead of example answers | Reinforcement fine-tuning; GRPO | [V: TRL] |
| Learning only from the answer part of each example | Completion-only loss; prompt masking | TRL's default for prompt and completion data [V: TRL] |
| The model's fixed way of laying out a chat as text | Chat template | Wrong template, worse model [V: TFM] |
| A model losing earlier skills after training | Forgetting | LoRA forgets less [V: BID] |

## 3. How it works

### 3.1 Where comparisons come from, and how far to trust each

| Source | Who runs it | What it measures | Known weaknesses, from its own pages or papers |
|---|---|---|---|
| Arena (arena.ai) | The Chatbot Arena team, later LMArena; its old links now lead to arena.ai (no rename notice was read) | Votes on pairs of anonymous answers to prompts users type; Bradley-Terry scores with confidence intervals [V: ARN] | Its paper says users are likely "LLM hobbyists and researchers" and prompts may not reflect production or specialist use [V: ARN]; length and formatting sway votes, so it adds "style control" [V: ARP] |
| Artificial Analysis Intelligence Index v4.3.2 | Artificial Analysis | A weighted average of 10 evaluations it runs itself: agents 30%, general 30%, coding 20%, scientific reasoning 20% [V: AAI] | Mostly English text; some private data sets; an LLM grades open answers; "may not apply directly to every use case" [V: AAI] |
| LiveBench | LiveBench team (ICLR 2025, per its repository) | 18 tasks with objective answers, scored without an LLM judge, refreshed over time against contamination [V: LVB] | Its own changelog replaced coding questions "likely heavily contaminated for newer models"; the newest entry was 284 days old on October 19, 2026 [V: LVB][T] |
| HELM | Stanford CRFM | Many scenarios and metrics beyond accuracy [V: HLM] | In maintenance mode since June 1, 2026: "no new evaluations will be added to the HELM leaderboards" [V: HLM] |
| Open LLM Leaderboard | Hugging Face | Fixed academic benchmarks run on submitted open models | Retired March 13, 2025, after "over 13K models", because "benchmarks need to follow" new capabilities [V: OLL]; older model cards still quote its numbers [V: HFC] |

**The Arena dispute.** "The Leaderboard Illusion" (Singh et al., a preprint) argues that Arena's rankings are distorted: a few providers test many private variants before release and can withhold scores (it counts 27 private variants from Meta before Llama 4), proprietary models are sampled more often, and Google and OpenAI received an estimated 19.2% and 20.4% of Arena's data against 29.7% for 83 open-weight models together [V: ILL]. Arena's reply (May 9, 2025) disputes several numbers, for example that the "112%" gain from extra Arena data was measured on Arena-Hard, a 500-question benchmark judged by an LLM, not on Arena itself, and puts the boost from pre-release testing at "around +11 Elo after 50 tests and 3000 votes" by its own analysis [V: ARP]. Both sides agree on the mechanism: Arena's policy lets providers "test multiple variants of their models pre-release" and receive their own battle data [V: ARP]. The argument is about whether that is fair, which no arithmetic settles. Neither side's numbers were re-run here [U].

**What to take from this.** Use a public ranking to build a short list, not to decide. Check what it measures (votes, exams or agent tasks), whether it is still updated, and who runs it.

### 3.2 Contamination and saturation

**Contamination is measured, not hypothetical.** Zhang et al. wrote new grade-school maths problems in the style of GSM8k (GSM1k) and found accuracy drops of "up to 8%" for some models, with "several families of models showing evidence of systematic overfitting across almost all model sizes", while many frontier models showed little (NeurIPS 2024, Datasets and Benchmarks Track) [V: GSM]. Deng et al. hid one wrong option of MMLU questions and asked models to fill it in: ChatGPT and GPT-4 reproduced it exactly 52% and 57% of the time, which points to test items seen in training (NAACL 2024) [V: DEN]. Whether GSM1k's 8% is points or relative was not read in the paper [U].

**Saturation.** Benchmark operators report it themselves. LiveBench refreshed tasks in November 2025 "to resolve (to some extent) saturation and contamination", and Hugging Face retired its leaderboard as "slowly becoming obsolete" [V: LVB, OLL].

**The 13-word rule.** GPT-3's authors flagged a test example as possibly contaminated when it shared a run of 13 words with the training data, or, if shorter than 13 words, appeared whole [V: GP3]. The lab's data checker uses the same rule on your own fine-tuning data (Section 3.8), because the same leak inflates your own eval.

### 3.3 Reading a model card

Mitchell et al. proposed nine sections for a model card: model details (developer, date, version, licence), intended use (including out-of-scope uses), factors, metrics, evaluation data, training data, quantitative analyses, ethical considerations, and caveats [V: MCR]. They ask for results "disaggregated, that is, broken down by the chosen factors" [V: MCR]. Hugging Face's annotated template admits the evaluation section "is most commonly used to report aggregate evaluation performance on different task benchmarks" [V: HFC].

On Hugging Face a card is the repository's README with a metadata block. `license` is shown and filterable; a custom licence is `license: other` with a name and link, which means you must read it (Part 10) [V: HFC]. `base_model` shows whether you are looking at a fine-tune, adapter, quantization or merge of another model, whose licence can still apply [V: HFC]. Scores on a model page are self-reported unless marked: Hugging Face's newer evaluation results show "verified" only when the run happened in its own jobs service with inspect-ai, and "community" for scores proposed by pull request [V: HFC].

**A five-point check for any card** (this series' advice, drawn from the two sources): (1) the licence, and its full text when it says `other`; (2) intended and out-of-scope uses; (3) what the training data is said to be, and its cutoff date; (4) which benchmarks, in which settings, run by whom; (5) `base_model`, to know what you are really getting.

### 3.4 The open-weight field, October 2026

From the publishers' own pages, October 16 to 19, 2026 [V: PUB, MUS]. "Total" counts every weight you must store (Part 11); a mixture-of-experts model uses only its active weights per token.

| Family | Newest seen | Sizes | Licence (per model) | Context |
|---|---|---|---|---|
| Meta | Muse Spark Open, October 15, 2026; Muse Glimmer 30B, August 2026; Llama 4, April 5, 2025 | 816B total, 42B active; 29.6B dense; Scout 109B total, 17B active | Custom gated Muse Model License; Apache-2.0; Llama 4 Community License | 1M; 131,072+; Scout 10M |
| Qwen (Alibaba) | Qwen3.8, August 2026; Qwen3.5, February to March 2026 | 2.4T total, 95B active; 27B; Qwen3.5 0.8B to 397B | Largest "qwen3.8-max"; 27B Apache-2.0; Qwen3.5 small models Apache-2.0 | 262,144 native |
| DeepSeek | DeepSeek-V4.1-Flash, about October 16 to 17, 2026 | Mixture of experts; 763B listed by the Hub | MIT | Up to one million |
| OpenAI | gpt-oss, August 5, 2025 | 117B total, 5.1B active; 21B total, 3.6B active | Apache 2.0 | (Part 11) |
| Google | Gemma 4 | E2B, E4B, 12B, 26B A4B, 31B | Apache 2.0 (earlier Gemma: Google's own terms) | 128K for E2B and E4B |
| IBM | Granite 4.1 | 3B, 8B, 30B dense | Apache 2.0 | Up to 512K |
| Microsoft | Phi-4-reasoning-vision, March 4, 2026 | 15B; Phi-4-mini 3.8B | MIT | 16,384; Phi-4-mini 128K |
| Mistral | Mistral Large 4 (v26.10) | Several | Apache 2.0, Modified MIT, CC BY-NC 4.0 or API only, per model | Varies |

**Licences differ inside one family, so read each card.** Meta's newest open model is not Apache-2.0: Muse Spark Open's card gives the licence as "muse-model-license", gated behind a form (legal name, date of birth, organization), and requires products to "prominently display 'Built with Muse Spark Open'"; offering it as a hosted model service above 20 million US dollars of revenue needs a separate agreement with Meta [V: MUS]. Muse Glimmer 30B, from the same organization two months earlier, is Apache-2.0 [V: MUS]. Qwen3.8-27B is Apache-2.0 while the largest Qwen3.8 model (2.4T) is "qwen3.8-max" [V: PUB]. Mistral's own docs disagree with each other: one page says open-weight models are "Apache 2.0", another that they are "under the Mistral license", and the models overview lists Apache 2.0, Modified MIT and a non-commercial licence model by model [V: MIS]. The full texts of the Muse, qwen3.8-max and Mistral Large 4 licences were not read [U].

**Open weights don't mean small.** Muse Spark Open "requires a GPU with at least 700GB of VRAM for NVFP4 and 2TB for BF16" [V: MUS]. Part 11's fit arithmetic applies: at about Q4_K_M (4.89 bits per weight, Part 11's figure for Llama 3 8B), Llama 4 Scout's 109 billion weights take 66.6 GB, more than an 80 GB card with a fifth kept free (64 GB), although Meta says it fits one H100 at 4 bits on the fly [V: PUB][T].

**A first shortlist.** The lab's `shortlist` keeps the models that fit at about Q4_K_M with a fifth of memory spare, under the licences you allow and with the context you need [T]:

```
 7.79 GB: Qwen3.5-0.8B, Granite 4.1 3B, Phi-4-mini-instruct, Gemma 4 E2B
   24 GB: the same, plus gpt-oss-20b, Qwen3.8-27B, Muse Glimmer 30B
```

These are only candidates that load. Section 3.5 decides between them. The uniform 4.89 bits is a simplification: gpt-oss ships in MXFP4, and real files differ by model (Part 11) [I].

### 3.5 Choosing by your own eval

Every kind of source ends with the same advice. OpenAI: "The best way to find the right model for your workflow is to experiment with different models", using "the same inputs" and keeping "the lightest setting that meets your quality bar" [V: SEL]. Anthropic: "having a good evaluation set is the most important step in the process", and "Test with your actual prompts and data" [V: SEL]. Mistral's evaluation guide: public benchmarks "may not cover real-world customer use cases", so "it is often preferable to create your own evaluation dataset", one hard enough that the models differ: "If every model being tested achieves over 90% accuracy, the differences between them might not be meaningful" [V: SEL]. Muse Glimmer's card recommends "building dedicated evaluation datasets for your use case", Llama 4's says much the same, and Muse Spark Open's card adds that its results "should not be assumed to apply to modified models" [V: PUB, MUS]. That last sentence matters for fine-tuning: a fine-tuned model needs its own eval.

**How, in practice** (Part 02 has the tools): write 30 to 100 real tasks with checkable answers before you look at any model's output [I]; run every candidate on the same tasks with the same prompt; compare pairs with McNemar's test on the items where they disagree, not by overall scores alone; look at the failures by type; then weigh licence, memory (Part 11) and cost (Part 13). Anthropic's path starts with a faster, cheaper model and says "Upgrade only if necessary" [V: SEL]; changing one thing at a time keeps the comparison readable [I].

### 3.6 Fine-tune, prompt or retrieve?

**For new facts, retrieve.** Ovadia et al. (EMNLP 2024) taught three 7B models (Llama2, Mistral, Orca2) 910 questions about US events from August to November 2023, after their training [V: OVA]. Retrieval on the base model beat fine-tuning on the source text and its paraphrases for every model: Mistral 7B scored 0.875 with retrieval against 0.588 fine-tuned on paraphrases, a gap of 28.7 points; across the three models the gap was 19.3 to 31.0 points, and 36.5 to 37.1 points against fine-tuning without paraphrases [V: OVA][T]. Plain fine-tuning even lowered Llama2 7B's score, from 0.353 to 0.219 [V: OVA]. The authors found fine-tuning absorbed facts better the more paraphrases it saw, and hypothesize that "the knowledge must be repeated in numerous ways" [V: OVA].

**New facts learned by fine-tuning raise hallucination.** Gekhman et al. (EMNLP 2024) fine-tuned PaLM 2-S on closed-book questions sorted by whether the model already knew each answer. Unknown facts were learned much more slowly, and "as the examples with new knowledge are eventually learned, they linearly increase the model's tendency to hallucinate" [V: GEK]. Stopping early on a held-out set avoided most of the harm, and leaving the unknown examples out did as well or better [V: GEK]. One model and one task type; long answers weren't tested [V: GEK].

**Prompt and measure first.** OpenAI: "The prompt engineering process may be all you need in order to get great results for your use case", and "You might even consider writing evals before you start writing prompts" [V: OAI]. Hugging Face's course says fine-tuning "should only be pursued when prompting existing models proves insufficient" [V: HFL]. Two vendor pages still list "domain-specific knowledge" or "new facts" as reasons to fine-tune, with no evidence given; the two studies above say otherwise [V: HFL, MIS].

**What fine-tuning is for.** A fixed output format or style the model must hit every time, or a smaller model doing one job that only a larger one could do by prompting [V: HFL]. A narrow classification or extraction task, or a behaviour that would otherwise need a very long prompt on every call, are common further reasons [I].

**The decision guide.** The lab's `choose_approach` applies these rules in order; the first that matches wins [T]:

| If | Then | Why |
|---|---|---|
| The need is new or changing facts | Retrieve (Part 05) | Ovadia et al.; Gekhman et al. |
| You have no test set of your own | Build an eval first (Part 02) | Nothing else can show improvement |
| You haven't tried prompting and other models | Prompt first | Vendors' advice; it's cheaper |
| Prompting already passes your eval | Stop | Nothing to fix |
| No machine you have can train it | Rent a GPU (Section 6) | Hosted fine-tuning has mostly closed (Section 3.10) |
| Otherwise | Fine-tune with LoRA, then re-run your eval and a safety test | A measured gap that prompting couldn't close |

### 3.7 What fine-tuning trains, and the memory it needs

**Full fine-tuning.** Every weight gets a gradient and optimizer state. With Adam in mixed precision, the ZeRO paper counts 2 bytes for the 16-bit weights, 2 for gradients and 12 for the optimizer (a 32-bit copy of the weights plus two moment estimates): "In total, this results in 2Ψ+2Ψ+KΨ=16Ψ bytes" for Ψ weights, before activations [V: ZER]. So a 1.5B model needs "at least 24GB" and a 7B model 112 GB [V: ZER][T]. LLaMA-Factory's README estimates 120 GB for a 7B model, ZeRO's figure plus a margin it doesn't explain [V: LLF][T].

**LoRA.** Hu et al. freeze the weight matrix W0 and learn an update ΔW = BA, where B is outputs x r and A is r x inputs, with r much smaller than either: the layer computes W0x + BAx [V: LOR]. A starts random and B at zero, so training starts from the unchanged model; the update is scaled by alpha / r [V: LOR]. Trainable weights per matrix: r x (inputs + outputs). A 4,096 x 4,096 projection at r = 8 trains 65,536 weights instead of 16,777,216, 0.39% [T]. On GPT-3 175B the paper reports training memory falling from 1.2 TB to 350 GB, and the checkpoint from 350 GB to 35 MB with r = 4 on two matrices per layer [V: LOR]. After training, BA can be added into W0, so inference costs nothing extra [V: LOR].

**The lab reproduces both libraries' and the paper's own numbers.** From each model's config file and the formula alone [T]:

| What | Published | Lab |
|---|---|---|
| Qwen2.5-3B-Instruct, r = 16, PEFT's default targets | "trainable params: 3,686,400 \|\| all params: 3,089,625,088" (PEFT 0.21.2 README) [V: PFT] | 3,686,400 and 3,085,938,688 + 3,686,400 = 3,089,625,088 |
| GPT-3 175B, LoRA on Wq and Wv, r = 1 and r = 8 | 4.7M and 37.7M (LoRA paper, Table 4) [V: LOR] | 4,718,592 and 37,748,736 |
| Same, r = 4, saved at 2 bytes per weight | "35MB" (Section 4.2) [V: LOR] | 37.7 MB (36.0 MiB) |
| Qwen3-0.6B, all weights | "0.6B", "Non-Embedding: 0.44B" (model card) [V: QCF] | 596,049,920; 440,467,456 without the embedding |

GPT-3's shape (96 layers, width 12,288) is from its paper's Table 2.1 [V: GP3]. Qwen2 models add a bias to q, k and v, and Qwen3 adds a small norm to q and k; the counts match only when those are included [V: QCF][T].

**Which layers.** The LoRA paper adapted only the query and value projections "in most experiments for simplicity" [V: LOR], and PEFT 0.21.2 still defaults to `q_proj` and `v_proj` for Llama, Mistral, Qwen2 and Qwen3 models, with r = 8 and alpha = 8 [V: PFT]. Later work points the other way. QLoRA found LoRA "on all linear transformer block layers" was needed to match full fine-tuning [V: QLR]. Biderman et al. found LoRA on all modules matched full fine-tuning in instruction tuning only at high rank: 256 for code, while 64 came close for maths [V: BID]. They advise alpha = 2r and a learning rate about ten times full fine-tuning's [V: BID]. TRL's docs relay Thinking Machines' "LoRA Without Regret" (a company blog): adapt all weight matrices, and "Attention-only LoRA underperforms even when using a higher rank" [V: TRL]. So set `target_modules="all-linear"` unless memory forbids it, and treat r as a setting to test [V: PFT, BID][I].

| Model | LoRA setting | Trainable | Share | Adapter at 2 bytes |
|---|---|---|---|---|
| Llama 3 8B | q, v, r = 8 (PEFT default) | 3,407,872 | 0.04% | 6.8 MB |
| Llama 3 8B | all linear, r = 16 | 41,943,040 | 0.52% | 83.9 MB |
| Llama 3 8B | all linear, r = 256 | 671,088,640 | 8.36% | 1.34 GB |
| Qwen3-0.6B | all linear, r = 16 | 10,092,544 | 1.69% | 20.2 MB |

All from `python demo.py` [T]. At r = 256 the "small" adapter is over a gigabyte.

**LoRA learns less and forgets less.** Biderman et al. compared LoRA with full fine-tuning of Llama-2-7B on code and maths [V: BID]. In continued pretraining on billions of tokens, the best LoRA trailed by 3.9 points on HumanEval and 9.0 on GSM8K; in instruction tuning it came within 0.8 points or matched [V: BID][T]. It also kept more of the model's general skills: on code instruction tuning, 0.509 against 0.414 on an average of three general benchmarks [V: BID]. A preprint, with its TMLR venue stated only by the authors [V: BID].

**QLoRA.** Dettmers et al. (NeurIPS 2023) back-propagate through a frozen 4-bit model into LoRA adapters, which "reduces memory usage enough to finetune a 65B parameter model on a single 48GB GPU" [V: QLR]. Three parts: the NF4 data type for normally distributed weights, in blocks of 64; double quantization, which shrinks each block's scale and cuts its cost from 0.5 to 0.127 bits per weight, "approximately 3 GB for a 65B model"; and paged optimizers, which move optimizer state to CPU memory during spikes [V: QLR][T]. NF4 is a bitsandbytes type for training, not a GGUF type (Part 11) [V: QLR].

**Memory, model states only** (`demo.py`; activations, batch size and sequence length add more and aren't modelled [U]):

```
Llama 3 8B  full        128.48 GB    7.79 GB: no   24 GB: no   80 GB: no
Llama 3 8B  lora_bf16    16.73 GB             no          yes         yes
Llama 3 8B  qlora         4.81 GB             yes         yes         yes
Qwen3-0.6B  full          9.54 GB             no          yes         yes
Qwen3-0.6B  lora_fp32     2.55 GB             yes         yes         yes
```

"Fits" here is memory only, with a fifth kept free. QLoRA as published runs on NVIDIA GPUs; whether 4-bit training works on a plain processor wasn't checked [U]. On a CPU, training usually runs in 32-bit, which is why the table has an fp32 row [I].

**One line each on the other methods.** *DoRA* (ICML 2024) splits each weight into a magnitude and a direction and uses LoRA for the direction; its authors report it "consistently outperforms LoRA" on their tasks, and PEFT offers it as `use_dora=True` [V: DOR, PFT]. *DPO* (NeurIPS 2023) trains on pairs of a preferred and a rejected answer directly, "essentially solving a classification problem on the human preference data", with no separate reward model [V: DPO]. *GRPO*, in TRL, samples several answers per prompt, scores each with a reward function, and learns from each answer's score relative to the group's average [V: TRL]. Ledger B2-08 already separates these training methods from a written instruction.

### 3.8 Data: formats, templates and leaks

**Formats.** TRL 1.16.0 names them: conversational (`messages`, each with `role` and `content`), language modelling (`text`), prompt and completion, and preference (`prompt`, `chosen`, `rejected`) [V: TRL]. OpenAI's DPO format used different names (`input`, `preferred_output`, `non_preferred_output`) [V: OAI]; MLX-LM reads `chat`, `tools`, `completions` and `text` [V: MLX]; LLaMA-Factory reads "alpaca" and "sharegpt" [V: LLF]. Converting between them is routine, and a silent mismatch is a common way to train on nothing useful [I].

**Templates.** Chat models expect the exact control tokens they were trained with: "with the wrong control tokens, these models would have drastically worse performance" [V: TFM]. TRL applies the model's chat template to conversational data for you, and for prompt and completion data it computes loss "on the completion tokens only, ignoring the prompt tokens" by default [V: TRL]. MLX-LM computes loss on every token unless you pass `--mask-prompt` [V: MLX]. The reader test does the masking itself (Section 7.5).

**How many examples.** OpenAI's guide set a minimum of 10 and said improvements usually show from 50 to 100 well-made examples [V: OAI]. That is one vendor's guidance for its hosted service, not a law [I].

**Check before you train.** `datacheck.py` reports, per file: each example's format; examples a trainer would reject or learn nothing from (an unknown role, empty content, a conversation that doesn't end with the assistant, identical chosen and rejected answers); exact duplicates; and test examples that share 13 words in a row with training data, GPT-3's contamination rule [V: GP3][T]. It leaves system messages out of the comparison, since every example may share one [T]. On the lab's invented data it finds the two problems planted there:

```
$ python datacheck.py data/train.jsonl data/test.jsonl
train: 12 examples, formats {'conversational': 12}
test: 4 examples, formats {'conversational': 4}
  train: example 12 repeats example 3
  test: example 2 shares 13 words in a row with the training data
2 problem(s) found
```

A leaked test example makes the fine-tuned model look better than it is, the same way contamination inflates public benchmarks (Section 3.2).

### 3.9 Safety after fine-tuning

Qi et al. fine-tuned GPT-3.5 Turbo through OpenAI's API and Llama-2-7b-Chat, and scored 330 harmful instructions with a GPT-4 judge [V: QIS]. Ten harmful examples raised GPT-3.5 Turbo's harmfulness rate from 1.8% to 88.8%, for "less than $0.20" in 2023 [V: QIS]. Ten examples with no toxic content, training the model to put obedience first, raised it to 87.3% [V: QIS]. Even one epoch on ordinary helpful data weakened safety: GPT-3.5 Turbo on the Alpaca data set went from 5.5% to 31.8% [V: QIS]. These are 2023 models and the preprint's first version; the authors give ICLR 2024 as the venue, not confirmed on the conference's page [V: QIS][U].

Two lessons. Re-run a safety test after every fine-tune, not only your task eval; screening data for toxic text alone would have missed the "obedience" examples [V: QIS][I]. And Muse Spark Open's card says the same about its own scores: they "should not be assumed to apply to modified models" [V: MUS]. OpenAI's hosted service checked each tuned model "across 13 distinct safety categories" before deployment [V: OAI]; your own run has no such check unless you add one.

### 3.10 Hosted fine-tuning in October 2026

The pay-per-job services have mostly closed. **OpenAI** is "winding down the fine-tuning platform" [V: OAI]. Its deprecations page: from May 7, 2026, organizations that had never fine-tuned can't create jobs; from July 2, 2026, neither can those with no inference on a fine-tuned model in the past 60 days; and on January 6, 2027, "Active existing customers will no longer be able to create new fine-tuning jobs" [V: OAI]. Tuned models keep serving until their base models are retired; several, including `ft-gpt-4` and `ft-gpt-3.5-turbo`, were removed on October 23, 2026 [V: OAI, re-checked October 26, 2026]. The lab's `openai_can_start_job` encodes these dates [T]. **Google's Gemini API:** "we no longer have a model available which supports fine-tuning in the Gemini API or AI Studio" since May 2025; tuning moved to its enterprise platform, which wasn't read [V: GEM][U]. **Mistral's** docs mark its fine-tuning pages "deprecated and ... no longer actively supported", while a guide elsewhere in the same docs source still describes "a fine-tuning API in Studio"; whether that guide is still published wasn't checked [V: MIS][U]. It archived its open-source trainer [V: MIS]. **Anthropic:** the only offer found was Claude 3 Haiku through Amazon Bedrock (2024); that model left Anthropic's API on April 20, 2026, and Bedrock's current status wasn't checked [V: ANT][U].

For a reader starting now, that leaves open-weight models on your own hardware or a rented GPU. No price was read for any of these [U].

### 3.11 The libraries

Read from each project's source at the version named, October 19, 2026 [V: PFT, TRL, UNS, AXO, LLF, MLX, TTN, LCF, PYPI]. Licences are information, not legal advice.

| Library | What it is | Licence | Hardware | Telemetry on by default? |
|---|---|---|---|---|
| PEFT 0.21.2 | LoRA, DoRA and other adapters for transformers models | Apache-2.0 | Wherever PyTorch runs | None found in a code search of its source [T] |
| TRL 1.16.0 | Trainers for SFT, DPO, GRPO and more | Apache-2.0 | As PyTorch | Yes: "A single ping is sent each time a trainer is instantiated"; off with `HF_HUB_DISABLE_TELEMETRY=1` or `DO_NOT_TRACK=1` |
| Unsloth 2026.10.7 | Faster fine-tuning with its own kernels | Says Apache-2.0, but 81 of 159 files in its core package carry AGPL-3.0 headers; needs unsloth_zoo (LGPL-3.0-or-later) [T] | Stops with "You need a GPU" without one; Apple silicon goes through MLX | Yes: downloads "statistics" repositories when it loads a model; off with `UNSLOTH_DISABLE_STATISTICS` |
| Axolotl 0.21.0 | Fine-tuning from YAML files | Apache-2.0 | NVIDIA or AMD; Mac "partially usable"; Windows through WSL2 or Docker | Yes: PostHog events; off with `AXOLOTL_DO_NOT_TRACK=1` or `DO_NOT_TRACK=1` |
| LLaMA-Factory 0.9.5 | A web UI and command line over many methods | Apache-2.0 | NVIDIA, AMD (ROCm), Ascend; Windows with manual steps | Its web UI uses Gradio, which reports usage unless `GRADIO_ANALYTICS_ENABLED=False` |
| MLX-LM 0.32.2 | LoRA, DoRA, QLoRA and full fine-tuning | MIT | Apple silicon (PyPI also lists Linux builds of MLX) | None found in a code search [U] |
| torchtune 0.6.1 | PyTorch's own recipes | BSD-3-Clause | Wherever PyTorch runs | None found; its README says it is "no longer actively maintained" |
| llama.cpp (`llama-finetune`) | An experiment | MIT | CPU builds, or GPU backends | Not applicable |

Three facts in that table change what you should do. **Unsloth's licence label is incomplete:** the released wheel ships both an Apache and an AGPL licence file, and the AGPL headers include kernels such as `unsloth/kernels/nf4.py`, while its LoRA path (`fast_lora.py`) is Apache [T]. If you redistribute software that includes it, read both [I]. **Telemetry differs by library and has different switches:** `DO_NOT_TRACK=1` stops TRL's and Axolotl's, but not Unsloth's or Gradio's [V: TRL, HHB, AXO, UNS, LLF]. **llama.cpp's fine-tuning is not LoRA:** its README calls the code "very much WIP", it trains every weight in 32-bit, and and of a tiny test model and Llama 3.2 1B it says fine-tuning "seems to work with 24 GB of memory" [V: LCF].

**Versions clash.** Axolotl 0.21.0 pins `trl==1.14.1`; Unsloth 2026.10.7 caps TRL at 1.15.0 and transformers at 5.17.0; LLaMA-Factory 0.9.5 caps PEFT at 0.18.1 and TRL at 0.24.0 [V: PYPI]. Give each its own virtual environment.

**On an ordinary computer.** Transformers' Trainer, which PEFT and TRL build on, trains on a CPU with `use_cpu=True` and says "CPU training works well when GPUs aren't available", with no speed figures [V: TFM]. On a Mac, both PyTorch's MPS backend and MLX-LM are documented for training; MLX-LM's guide gives the only measured consumer figure found, "about 250 tokens-per-second" for LoRA on Mistral 7B on an M1 Max with 32 GB [V: TFM, MLX]. How long a LoRA run takes on a CPU was not measured by any source read [U]; reader test R3 measures it on yours. On the owner's test PC (an Intel Core i5-9500T, no GPU) it took 0.89 seconds per step, about 103 tokens per second, for SmolLM2-135M [T].

### 3.12 Licences when you share a fine-tune

Information, not legal advice. Read the licence of the exact base model, from its own file.

- **Apache-2.0** (Section 4 of the licence): give recipients a copy of the licence, mark files you changed, and keep the notices in any NOTICE file [V: APL].
- **Llama 3** (April 18, 2024): show "Built with Meta Llama 3", put "Llama 3" at the beginning of any fine-tuned model's name you distribute, and "You will not use the Llama Materials or any output or results of the Llama Materials to improve any other large language model (excluding Meta Llama 3 or derivative works thereof)" [V: LLL].
- **Llama 3.1, 3.2 and 4:** that last ban is gone. Show "Built with Llama", and if you use Llama "or any outputs or results" to "create, train, fine tune, or otherwise improve an AI model" that you distribute, "include 'Llama' at the beginning of any such AI model name" [V: LLL]. The lab's `name_ok` checks the prefix [T].
- **Muse Model License:** "Built with Muse Spark Open" in the product's interface, a separate agreement with Meta before offering it as a hosted model service above 20 million US dollars of revenue, and a gated text to read first [V: MUS][U].
- **Hosted models' outputs:** OpenAI's terms for individuals forbid using output "to develop models that compete with OpenAI"; Anthropic's commercial terms forbid using its services "to build a competing product or service, including to train competing AI models", while both say you own your outputs [V: OAI, ANT]. Training a model on another vendor's outputs therefore depends on that vendor's terms, not on who owns the text [I].

## 4. Gemini said, evidence says

| Gemini (ledger row) | Evidence | Section |
|---|---|---|
| Llama 3 8B as the local example (P10-09b) | Outdated, with more detail than Part 11 gave: Meta's newest open model is Muse Spark Open (October 15, 2026) under a custom, gated licence, after Muse Glimmer 30B (Apache-2.0, August 2026). Llama 3's licence also required "Llama 3" at the start of a shared fine-tune's name; from Llama 3.1 the ban on improving other models is gone and the prefix is "Llama" [V: MUS, LLL] | 3.4, 3.12 |
| GGUF versus AWQ versus GPTQ (B4-10) | Corrected in Part 11, and unchanged. One addition: Meta publishes its own GGUF of Muse Glimmer 30B, so check `base_model` and the uploader rather than assuming a GGUF comes from a third party [V: MUS, HFC] | 3.3 |
| "Soft-prompt alignment (RLHF)" (B2-08) | Corrected in the ledger. This part adds the training methods themselves: SFT and LoRA change or add weights, DPO trains on preference pairs, GRPO on scores [V: LOR, DPO, TRL] | 3.7 |
| The report has nothing on fine-tuning (ledger, headline 10) | Filled by Sections 3.6 to 3.12 | 3.6 |
| GPT-4 as a judge (P9-12) | Still outdated: fine-tuned GPT-4 models were removed with their base on October 23, 2026 [V: OAI, re-checked October 26, 2026] | 3.10 |
| Routing easy queries to smaller models (P8-02) | Consistent with vendors' model-selection advice: keep the lightest model that meets your bar [V: SEL] | 3.5 |
| Llama Guard is a model fine-tuned for safety (P12-03) | Settled in Part 10. The reverse also holds: fine-tuning can remove a model's safety behaviour, even on harmless data [V: QIS] | 3.9 |

## 5. Examples

**Real examples.**

1. *A leaderboard retired by its own operator* [V: OLL]. Hugging Face's Open LLM Leaderboard stopped in March 2025 because "benchmarks need to follow" new capabilities. Scores from it still sit on older model cards.
2. *One publisher, two licences, two months apart* [V: MUS]. Meta's Muse Glimmer 30B is Apache-2.0; Muse Spark Open, from the same organization, needs a gated form and carries attribution and revenue conditions. "Meta's open models" is not a licence.
3. *A platform closing* [V: OAI]. OpenAI's self-serve fine-tuning closed to new organizations on May 7, 2026 and closes to everyone for new jobs on January 6, 2027. A plan built on it in 2025 has to move.

**A fully worked example: should a support team fine-tune, and can an office PC do it?** [I: the team, its notes and the prompting scores are invented; every computed number came from the lab]

*Input.* Support notes must become JSON with three keys (product, urgency, summary), every time. The team has 40 notes with correct answers as a test set [I]. The best prompt on a small model gets 31 of 40 right; the misses are mostly urgency labels and stray text around the JSON [I]. The office PC has 7.79 GB of memory, no usable GPU, and the team will share the result inside the company.

*Step 1, decide.* The need is a format and a labelling habit, not new facts; there is an eval; prompting was tried and falls short; so `choose_approach` returns "fine-tune with LoRA" [T].

*Step 2, pick a base.* Under Apache-2.0 or MIT, the models that load in 7.79 GB at about Q4_K_M are Qwen3.5-0.8B, Granite 4.1 3B, Phi-4-mini-instruct and Gemma 4 E2B [T]. For training on a processor, smaller is faster; this example uses Qwen3-0.6B (Apache-2.0), whose shape the lab knows [V: QCF].

*Step 3, check the data.* `datacheck.py` on 12 training and 4 test examples finds one duplicate and one test note copied from the training set [T]. Remove both before training, or the test score means less.

*Step 4, size the run.* LoRA on all linear layers at r = 16 trains 10,092,544 weights, 1.69% of 596,049,920, and saves a 20.2 MB adapter at 2 bytes per weight [T]. In 32-bit on a processor, model states take 2.55 GB: fits in 7.79 GB with a fifth kept free [T]. Full fine-tuning would need 9.54 GB, which doesn't [T]. Free memory, not total, decides: Part 11's reader test found under 1 GB free on such a PC with everyday programs open [T: Part 11, R3].

*Step 5, after training.* Run the same 40 notes; ship only if the paired test (Part 02) says the tuned model beats the prompted one, and run a safety test too, since even harmless data can weaken refusals [V: QIS].

*Step 6, share.* Qwen3-0.6B is Apache-2.0: include the licence, mark what changed, keep any notices [V: APL]. Had the base been Llama 3.1 or later, the model's name would have to start with "Llama" [V: LLL].

*Output.* Fine-tune a 0.6B model with LoRA on the processor, after cleaning two data problems; expect it to fit with about 2.5 GB of model states; judge it only on the paired eval and a safety test. How long training takes on this PC is what reader test R3 measures: on the owner's test PC, 0.89 seconds per step for the 135-million-weight SmolLM2 [T: October 20, 2026]; a 0.6B model takes longer [I].

## 6. What you need

Checked October 19, 2026 [V: PYPI]. Licences from each project's licence file; information, not legal advice.

| Tool | What it's for | Licence | Runs on | Account or key? | Version |
|---|---|---|---|---|---|
| The lab's scripts | Parameter counts, memory, data checks, decision rules | This series | Python 3.11 to 3.13, standard library [T] | No | Lab zip |
| PyTorch | The training engine under everything below | PyPI gives a combined expression for its bundled parts: Apache-2.0, Apache-2.0 WITH LLVM-exception, BSD-2-Clause, BSD-3-Clause, BSL-1.0 and MIT | Wheels for 64-bit Windows, Apple-silicon Macs on macOS 14 or later, and Linux (x86-64 and Arm); Python 3.10 or later | No | 2.14.1 (Windows wheel, the package file pip downloads, 124 MB; Linux 555 MB) |
| transformers | Loads models and tokenizers; the Trainer | Apache-2.0 | As PyTorch | No; gated models need a Hugging Face account (Part 10) | 5.20.2 |
| PEFT | LoRA and other adapters | Apache-2.0 | As PyTorch | No | 0.21.2 |
| TRL | SFT, DPO and GRPO trainers | Apache-2.0 | As PyTorch; Python 3.11 or later | No; telemetry on by default | 1.16.0 |
| MLX-LM | Fine-tuning on Apple silicon | MIT | Apple silicon; PyPI also lists Linux | No | 0.32.2 |
| Unsloth | Faster LoRA on GPUs | Apache-2.0 with AGPL-3.0 files | GPU or Apple silicon | No; statistics on by default | 2026.10.7 |
| Axolotl | Fine-tuning from a YAML file | Apache-2.0 | NVIDIA or AMD GPU; Windows through WSL2 or Docker; Python 3.12 or later | No; telemetry on by default | 0.21.0 |
| LLaMA-Factory | Web UI and command line | Apache-2.0 | NVIDIA, AMD, Ascend; Python 3.11 or later | No; the web UI reports usage | 0.9.5 |

Sources: Sections 3.7 and 3.11 [V: PFT, TRL, UNS, AXO, LLF, MLX, TFM, PYPI].

Picks, and when to skip them:

- **Best default for a solo builder with a GPU:** transformers plus PEFT with your own short loop or TRL's `SFTTrainer`, LoRA on all linear layers; set `HF_HUB_DISABLE_TELEMETRY=1` before TRL runs [V: PFT, TRL] (in PowerShell `$env:HF_HUB_DISABLE_TELEMETRY = "1"`, in macOS and Linux shells `export HF_HUB_DISABLE_TELEMETRY=1`, in the same window that runs the training) [R].
- **On a Mac:** MLX-LM's `mlx_lm.lora`, which also does QLoRA when given a quantized model [V: MLX].
- **On an ordinary PC with no GPU:** transformers and PEFT on the processor, with a model under 1B parameters, as in reader test R3 (Section 7.5) [V: TFM][T: R3 on the owner's Windows PC, October 20, 2026]. Unsloth's training code stops without a GPU, though its README lists CPUs for running models, and Axolotl documents no processor-only path [V: UNS, AXO].
- **Faster on NVIDIA:** Unsloth, after reading its two licence files, with `UNSLOTH_DISABLE_STATISTICS` set [V: UNS].
- **Skip for new work:** torchtune, which says it is "no longer actively maintained"; llama.cpp's fine-tuning, an experiment; hosted fine-tuning on OpenAI or Gemini, which is closed, and Mistral's, which its docs mark deprecated [V: TTN, LCF, OAI, GEM, MIS].
- **When not to fine-tune at all:** facts that change, no eval, or a prompt that already passes (Section 3.6).

## 7. Set it up

**Before you start.** Part 01's setup: Python 3.11 to 3.13 and the series folder `ai-stack` in your home folder. Unzip `engineering-stack-lab-part-12.zip` into `ai-stack` (on Windows: right-click, Extract All, destination `ai-stack`; if the folder ends up inside another of the same name, move the inner one up) [R]; on Linux, from the folder holding the zip, `python3 -m zipfile -e engineering-stack-lab-part-12.zip ~/ai-stack` [T]. The core lab needs nothing installed. Type each command on its own line.

### 7.1 to 7.3 Windows, macOS and Linux

**7.1 Windows,** in PowerShell [R: typed steps not run on Windows; this lab ran there by script on October 20, 2026]:

```
cd $HOME\ai-stack\engineering-stack-lab-part-12
py -V:3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python run_lab.py
```

If PowerShell refuses to run `Activate.ps1`, use Part 01's one-time fix (Part 01, Section 7.1, step 5), then activate again.

**7.2 macOS** [R: no macOS test machine] **and 7.3 Linux** [T]:

```
cd ~/ai-stack/engineering-stack-lab-part-12
python3.13 -m venv .venv
source .venv/bin/activate
python run_lab.py
```

Expect `17 of 17 checks passed`. If `py -V:3.13` or `python3.13` isn't found, use the 3.11 or 3.12 from Part 01.

### 7.4 A tour

| Command | What it does |
|---|---|
| `python run_lab.py` | 17 checks; exit code 0 only if all pass |
| `python mutation_check.py` | Breaks the lab 33 ways in temporary copies; each must make `run_lab.py` fail (a few seconds) |
| `python demo.py` | Prints the six worked tables behind Sections 3 and 5 |
| `python datacheck.py data/train.jsonl data/test.jsonl` | Checks the sample data; finds the duplicate and the leak planted in it, and exits with code 1 on purpose [T] |
| `python reader_lora.py --plan` | Prints the reader test's predictions without downloading anything [T] |

In your own code, after `import adaptmath as am`: `am.lora_params(am.QWEN3_06B, am.ALL_LINEAR, 16)` returns 10092544 [T]; `am.training_bytes(weights, "qlora", adapter_weights)`, with your own two counts, sizes model states; and `am.shortlist(memory_gb, {"apache-2.0", "mit"})` lists candidates. To add a model, copy these fields from its `config.json` into a dict like `QWEN3_06B`: `hidden_size` to `hidden`, `num_hidden_layers` to `layers`, `num_attention_heads` to `heads`, `num_key_value_heads` to `kv_heads`, `head_dim` (or `hidden_size` divided by the heads) to `head_dim`, `intermediate_size` to `ffn`, `vocab_size` to `vocab` and `tie_word_embeddings` to `tied`. `qkv_bias` and `qk_norm` aren't config fields: they are true for Qwen2 and Qwen3 models respectively, from their model code [V: QCF]. The counts are right only for this dense block layout (q, k, v, o, gate, up, down); mixture-of-experts and hybrid models need more [I].

### 7.5 Reader test R3: train a small LoRA adapter on your processor [T: on the owner's Windows PC, October 20, 2026]

This installs PyTorch, transformers and PEFT into the lab's environment and downloads SmolLM2-135M-Instruct (Apache-2.0, 135 million weights) from Hugging Face once; skip it if you'd rather not [V: PYPI, QCF]. On 64-bit Windows that is about 170 MB in about 40 packages, most of it PyTorch's 124 MB wheel; on Linux, PyPI's PyTorch wheel is 555 MB and pulls NVIDIA's CUDA libraries, several hundred MB each, even on a computer with no GPU, so allow a few GB of disk [T: estimated from PyPI's listings]. PyTorch 2.14.1 has no wheel for Intel Macs or Windows on Arm; there, pip reports "No matching distribution" [T: PyPI's file list]. PyTorch's own site offers smaller processor-only builds, not checked here [U]. Apart from the downloads the script is meant to send nothing; that wasn't watched on the network [U]. From the lab folder, with its environment active:

```
pip install torch==2.14.1 transformers==5.20.2 peft==0.21.2
python reader_lora.py --steps 24
```

**Expected:** first the two lines `--plan` also prints [T]:

```
HuggingFaceTB/SmolLM2-135M-Instruct: 134,515,008 weights; LoRA r=8 on q and v trains 460,800
Model states for LoRA in 32-bit: 0.55 GB, plus activations
```

Then two lines that should agree, PEFT's own count and the lab's prediction, both ending `460,800 trainable of 134,975,808 parameters`: the model's 134,515,008 weights plus the 460,800 new ones [T: the prediction; PEFT's count on the owner's Windows PC, October 20, 2026]. Then the loss on the answers falling between the first and last three steps, a median time per step, and an adapter of about 1.9 MB saved in `lora-out` [T]. Exit code 0 means the counts agreed, 1 that they differ, 2 that a package is missing [T]. Send back what it prints ("Run on your computer", after Section 12): the time per step on a processor is the number no source read here gives [U].

The script uses a plain PyTorch loop rather than TRL, so nothing pings a server, and it sets `HF_HUB_DISABLE_TELEMETRY=1` and `DO_NOT_TRACK=1` before importing anything [V: TRL, HHB]. It masks each prompt so the model learns only the answer, the same default TRL uses for prompt and completion data [V: TRL].

### 7.6 Common errors and fixes

| What you see | Why | Fix |
|---|---|---|
| PowerShell refuses to run `Activate.ps1` | Its script policy | Part 01's one-time fix (Part 01, Section 7.1, step 5) [R] |
| `can't open file '.../run_lab.py': [Errno 2] No such file or directory` | The terminal isn't in the lab folder | `cd` into it [T] |
| `Missing package (torch). Install torch, transformers and peft first (Part 12, Section 7.5), or run with --plan.` | Reader test R3 without its packages | Install them, or use `--plan` [T: the message] |
| `2 problem(s) found` from `datacheck.py` on the sample data | Planted on purpose | Nothing; on your own data, fix each line it names [T] |
| `ModuleNotFoundError: No module named 'adaptmath'` | Python was started outside the lab folder | `cd` into the lab folder first [T] |
| `python: command not found`, or `python3.13: command not found` | No environment active, or that version isn't installed | Activate the environment (Section 7); otherwise use `python3` with Part 01's 3.11 or 3.12 [R] |
| `Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN ...` | `reader_lora.py` downloads the model without a Hugging Face account | Nothing: it is a warning, and the run goes on; no account or token is needed for this public model [T] |
| `No matching distribution found for torch==2.14.1` | Your computer has no wheel (an Intel Mac, Windows on Arm) | Skip reader test R3, or use another computer [T: PyPI's file list][R] |
| `The chat template's prompt isn't a prefix of the full example.` | The model's template lays out the last turn differently once an answer follows [I] | Use another model, or mask by hand [T: the message] |

### 7.7 How to uninstall the lab

`deactivate`, move up one folder with `cd ..`, and delete `engineering-stack-lab-part-12`: `rm -rf engineering-stack-lab-part-12` on macOS and Linux [T], `Remove-Item -Recurse -Force engineering-stack-lab-part-12` in PowerShell [R]. Deleting the folder removes R3's packages and `lora-out` with it; the downloaded model stays in Hugging Face's cache, `.cache\huggingface` in your home folder [T: on the owner's Windows PC, October 20, 2026]. The mutation check deletes its own temporary folders [T].

## 8. Hands-on lab: count it, size it, check it

**Goal.** Count what LoRA trains from a model's configuration and match the libraries' own printouts, size training memory for each method, find the leaks and duplicates in a data set, and see the decision guide and licence rules as code you can test. Then, if you like, train a small adapter on your own computer.

**Prerequisites.** Section 7 for your system. **Time:** about 30 minutes by hand, under a minute automated. **Cost:** none. **Pinned:** the standard library only. **Data:** the published configurations of Llama 3 8B (Part 11), Qwen2.5-3B-Instruct, Qwen3-0.6B, SmolLM2-135M-Instruct and GPT-3, and the figures named in each check [V: QCF, GP3, PFT, LOR]; the support notes in `data/` are invented [I]. **Files:** all are in the zip; `adaptmath.py`, the arithmetic, is also printed in the appendix. The others: `datacheck.py`, `run_lab.py`, `mutation_check.py`, `demo.py`, `reader_lora.py`, `README.md` and `data/`.

**Steps.** Run every command from the lab folder, with its virtual environment active (Section 7). Outputs are from the test machine, Python 3.13.16, October 19, 2026 [T].

1. **Read the arithmetic.** Open `adaptmath.py`: each table names its source in a comment, and most functions are a few lines.
2. **Match PEFT's printout.** `python -c "import adaptmath as am; print(am.lora_params(am.QWEN25_3B, am.PEFT_DEFAULT_TARGETS['qwen2'], 16), am.count_params(am.QWEN25_3B))"` prints `3686400 3085938688`; their sum is PEFT's "all params: 3,089,625,088" [T].
3. **Print the tables.** `python demo.py` prints six tables: weight counts, LoRA sizes, training memory and fit, OpenAI's dates, the shortlist, and the decision guide (Sections 3.4 to 3.10 quote them).
4. **Check data.** `python datacheck.py data/train.jsonl data/test.jsonl` prints the report in Section 3.8 [T]. Then copy `data/train.jsonl` to a new file, `data/mytrain.jsonl` (leave the original alone, since check c14 reads it), open the copy in a text editor, change the first `"role": "assistant"` on its first line to `"role": "bot"`, save, and run `python datacheck.py data/mytrain.jsonl`. It prints [T]:

   ```
     train line 1: message 2: role must be one of ['assistant', 'system', 'tool', 'user']
     train line 1: last message isn't the assistant's, so there is no answer to learn
   train: 12 examples, formats {'conversational': 12}
     train: example 12 repeats example 3
   3 problem(s) found
   ```

   Delete `data/mytrain.jsonl` when you're done.
5. **Break it.** In `adaptmath.py` (line 67; any text editor), change `ADAM_MIXED_BYTES = 2 + 2 + 12` to `2 + 2 + 8`, leaving out Adam's 32-bit copy of the weights. `python run_lab.py` now ends `16 of 17 checks passed`, with `FAIL c07_full_finetuning_memory: AssertionError 18000000000.0`: 18 GB instead of the ZeRO paper's "at least 24GB" for 1.5 billion weights [T]. Put it back and confirm 17 of 17.
6. **Prove the checks can fail.** `python mutation_check.py` breaks the lab 33 ways (grouped-query attention ignored, Qwen's biases left out, only A counted and not B, double quantization ignored, the 60-day rule ignored, a name prefix accepted anywhere, any role accepted, 12-word runs counted as leaks, the prompt left unmasked, and more) and expects `run_lab.py` to fail each time: `33 of 33 mutations caught` [T].
7. **Train one (optional).** Section 7.5 [T: on the owner's Windows PC, October 20, 2026].

**Expected output** (`python run_lab.py`, abridged):

```
PASS c01_weight_counts
PASS c02_reproduces_peft_readme
PASS c03_reproduces_lora_paper
...
PASS c16_leak_rules
PASS c17_reader_test_logic
17 of 17 checks passed
```

**If it fails.** A FAIL line names the check; Section 7.6 covers the common errors. If a check fails only on your machine, keep the whole output for reader test R1 ("Run on your computer", after Section 12).

## 9. Teach it

**Learning objectives.** After this part you can:

1. say what a leaderboard measures, who runs it, and why its scores drift (contamination, saturation);
2. read a model card for licence, intended use, evaluation scope and lineage, and build a short list that fits your hardware and licence needs;
3. decide between prompting, retrieval and fine-tuning from evidence, and say why new facts belong in retrieval;
4. count LoRA's trainable weights from a configuration file and size training memory for full fine-tuning, LoRA and QLoRA;
5. check training data for format errors, duplicates and test leaks, and name what to test after fine-tuning and what a licence requires when you share the result.

**Prerequisites.** Part 01's setup; Part 02 (evals), Part 05 (retrieval), Part 10 (licences), Part 11 (fit and speed). Reading a little Python.

**Common misconceptions.**

- *"The top of the leaderboard is the best model for me."* Rankings measure votes or fixed tests; the vendors themselves say to test on your own data [V: ARN, SEL].
- *"Fine-tuning teaches the model our documents."* New facts are learned slowly and raise hallucination [V: GEK]; in one study, retrieval beat fine-tuning by 19 to 37 percentage points on new facts [V: OVA][T].
- *"LoRA is a smaller model."* LoRA adds small matrices beside a full, frozen model; you still load every weight [V: LOR].
- *"Open-weight means Apache-2.0."* Meta, Qwen and Mistral each publish models under several licences [V: MUS, PUB, MIS].
- *"Harmless training data can't hurt safety."* One epoch on Alpaca raised GPT-3.5 Turbo's harmfulness rate from 5.5% to 31.8% [V: QIS].

**Exercises, with checked answers.** Run the checks from the lab folder.

1. *A bigger adapter.* How many weights does LoRA train on Llama 3 8B with all linear layers at r = 64, and what share is that? Answer: 167,772,160, 2.09%. Check: `python -c "import adaptmath as am; a = am.lora_params(am.LLAMA3_8B, am.ALL_LINEAR, 64); print(a, round(100 * a / am.count_params(am.LLAMA3_8B), 2))"` prints `167772160 2.09` [T].
2. *Full fine-tuning on a laptop.* Does full fine-tuning of Qwen3-0.6B fit in 16 GB of memory, and in 8 GB? Answer: 9.54 GB of model states; yes and no. Check: `python -c "import adaptmath as am; b = am.training_bytes(am.count_params(am.QWEN3_06B), 'full'); print(b / 1e9, am.fits(16, b), am.fits(8, b))"` prints `9.53679872 True False` [T].
3. *QLoRA on a small GPU.* Llama 3 8B, QLoRA, all linear layers at r = 16: does it fit a 12 GB card? Answer: 4.81 GB of model states, yes, before activations. Check: `python -c "import adaptmath as am; a = am.lora_params(am.LLAMA3_8B, am.ALL_LINEAR, 16); b = am.training_bytes(am.count_params(am.LLAMA3_8B), 'qlora', a); print(round(b / 1e9, 2), am.fits(12, b))"` prints `4.81 True` [T].

**Five-question self-check.** Answers follow.

1. Name two reasons a public benchmark score can overstate a model's skill.
2. Which Hugging Face card field tells you a model is a fine-tune of another, and why does it matter?
3. A product manual changes every month. Fine-tune or retrieve?
4. Why does full fine-tuning with Adam need about 16 bytes per weight?
5. You fine-tuned Llama 3.1 and want to publish the result as "SupportBot". What must change?

*Answers.* (1) Contamination (test items in training data) and saturation (a test most models ace) [V: GSM, DEN, LVB]. (2) `base_model`; the base model's licence and limits can still apply [V: HFC]. (3) Retrieve: facts that change belong in retrieval, and fine-tuned facts raise hallucination [V: OVA, GEK]. (4) 2 bytes of weights, 2 of gradients and 12 of optimizer state (a 32-bit copy plus two moments) [V: ZER]. (5) Its name must start with "Llama", and you must show "Built with Llama" and ship the licence [V: LLL].

**You've got it when** you can take a task, a computer and a list of models and say, with numbers, whether to prompt, retrieve or fine-tune, which models to test, whether LoRA fits, and what you would test before shipping.

**Best next resources** (checked to exist on October 19, 2026): the LoRA paper [V: LOR]; QLoRA [V: QLR]; Ovadia et al. and Gekhman et al. [V: OVA, GEK]; PEFT's README and LoRA docs [V: PFT]; TRL's dataset formats and SFT pages [V: TRL]; Mitchell et al.'s model cards paper [V: MCR].

**A tutor prompt to practise with.** Paste this into Claude (modelled on claude/github-tutor-prompt.md):

```
Help me learn to choose an AI model and decide whether to fine-tune it.

How to teach me: one idea at a time, a question I answer before you go on,
and a small worked example with real numbers for each idea. When I'm wrong,
show me the reasoning rather than the answer, so I can find the mistake.

Topics, in order:
1. Leaderboards: what each measures, contamination and saturation.
2. Reading a model card: licence, intended use, evaluation, base model.
3. Testing candidates on my own task, and comparing two models fairly.
4. Prompt, retrieve or fine-tune: what the evidence says about each.
5. LoRA and QLoRA: what they train, and the memory arithmetic.
6. Training data: formats, chat templates, duplicates and test leaks.
7. After fine-tuning: re-testing quality and safety; licence duties.

For any product, version, price, licence or benchmark figure, tell me it may
have changed since your training and that I should check the publisher's page.

Start by asking what task I have in mind and what computer I have.
```

**What to learn next.** Part 13, delivery and operations: APIs and streaming, observability, and cost and latency.

## 10. Limits and debates

- **No model was trained or tested on the test machine.** It has no GPU and can't reach Hugging Face, so every library is described from its source code at a pinned version and every result from its paper [R]. The one model trained for this part is reader test R3's small adapter, on the owner's PC ("Run on your computer"). The arithmetic ran, and reproduces PEFT's, the LoRA paper's and Qwen's published counts exactly [T].
- **The fine-tune or retrieve evidence is narrow.** Two peer-reviewed studies: three 2023 7B models on five MMLU subjects and one set of news questions, and one model (PaLM 2-S) on closed-book questions [V: OVA, GEK]. Both found results sensitive to settings. Whether 2026 models behave the same wasn't tested [U].
- **Preprints and blogs carry weight here.** Biderman et al. and Qi et al. are preprints whose venues come only from their authors' pages; "LoRA Without Regret" is a company blog relayed by TRL's docs; ZeRO's 16 bytes is from the arXiv version [V: BID, QIS, TRL, ZER].
- **The memory model leaves out activations.** It counts weights, gradients and optimizer state; activations grow with batch size and sequence length, and tricks such as gradient checkpointing change them [U]. Real runs need more than the table says.
- **Rankings were read, not re-run.** Arena's live policy page renders by script and couldn't be read, and neither side's numbers in the Leaderboard Illusion dispute were recomputed here [V: ARP, ILL][U].
- **Network behaviour was read, not watched.** The telemetry in TRL, Axolotl, Unsloth and Gradio comes from their code; Axolotl's docs mention a 10-second pause at startup that its code at this tag doesn't show [V: AXO][U]. "None found" for PEFT, MLX-LM and torchtune means a keyword search came up empty [U].
- **Licence texts not read in full:** the Muse Model License, "qwen3.8-max", Mistral Large 4 [U]. Information, not legal advice.
- **Hosted services:** no prices were read; Google's enterprise tuning and Amazon Bedrock's current Claude 3 Haiku tuning weren't checked [U].
- **When this is the wrong tool.** Facts that change: retrieval (Part 05). No eval: Part 02 first. A prompt that already passes: stop. Only a handful of examples: few-shot prompting usually beats training on them [I].
- **Open questions.** How long LoRA takes on processors other than the owner's (reader test R3 gave 0.89 seconds per step there); how much contamination inflates 2026 models' scores; what Arena's current policy says.

**Where this part touches project docs** (flagged, not applied; plan, Section 8):

1. *Claim ledger P10-09b* should add that Meta's newest open model, Muse Spark Open (October 15, 2026), is under a custom, gated licence, and that Llama 3's licence also required "Llama 3" at the start of a shared fine-tune's name; from Llama 3.1 the prefix is "Llama" and the ban on improving other models is gone [V: MUS, LLL].
2. *Claim ledger, headline finding 10,* lists fine-tuning as a gap; this part fills it.
3. *Part 11's reader tests ran on the test PC on October 19, 2026,* and found one 8 GB memory module, so the PC runs in single channel at about 21.3 GB/s (2,666 million transfers x 8 bytes), half the 41.6 GB/s Part 11 uses; qwen3:1.7b measured 8.4 and 8.0 tokens per second against ceilings of 30.6 and 15.7 [T]. Applied the same day, as the series' prompt asks for reader-test results: Part 11's Section 7.5 now says one module halves the figure, its "Run on your computer" section carries the results, and claude/engineering-stack-windows-run-2026-10-19.md has the full record.
4. No conflict found with the taxonomy or the guide: the project's search for fine-tuning found it only in the plan, which assigns it here, and in the taxonomy's note that directional stimulus prompting bridges prompting and light tuning.

## 11. Skill opportunity

claude/new-skills-appendix.md has no matching idea. A **finetune-readiness** skill would take a task description, a test set, a training file and a base model's `config.json`, and report: what the decision guide says (prompt, retrieve or fine-tune) and why; format problems, duplicates and test leaks in the data; LoRA's trainable weights and the memory for each method; and the base licence's duties when sharing. `adaptmath.py` and `datacheck.py` would be its scripts, and checks c02 to c16 with their mutations would start its eval pack. It would read files and do arithmetic, never download or train a model. Like every skill here, it needs the owner's trigger and non-trigger lists first (project instructions, "Building a skill", step 1).

## 12. Sources

All opened October 19, 2026, by the lead session or one of two researcher agents, except where Part 11 is named. Code and documentation were read from git clones at the commits named, or from wheels downloaded from PyPI, so quotes come with file and line; web pages through a fetch tool that summarizes, with quotes asked for verbatim. The lead re-read in source PEFT's README example, defaults and target modules, TRL's telemetry, the Llama 3, 3.1, 3.2 and 4 licence clauses, Unsloth's licence headers (recounted from the wheel), OpenAI's deprecation dates, the Gemini API's tuning notice, Muse Spark Open's card, GPT-3's Table 2.1 and 13-word rule, and the four configuration files, and ran every number in the lab [T]. Grade: confidence from 1 to 10 that the source supports the use made of it.

| Key | Source | Class | Used for | Grade |
|---|---|---|---|---|
| AAI | Artificial Analysis, "Intelligence Benchmarking Methodology" page (Intelligence Index v4.3.2) | OD | What the index measures; its caveats | 7 |
| ANT | Anthropic: "Fine-tune Claude 3 Haiku in Amazon Bedrock" (2024 article); model deprecations page; Commercial Terms of Service (effective June 17, 2025) | VB, OD | The Bedrock offer; Claude 3 Haiku's retirement; terms on outputs | 7 |
| APL | Apache License 2.0, Section 4, as shipped in PEFT's LICENSE | OD | Duties when redistributing | 10 |
| ARN | Chiang et al., "Chatbot Arena", ICML 2024, PMLR 235, pp. 8359 to 8388 (mlresearch/v235 at d8ed297; the PDF) | PR | Method; limitations; agreement figures | 9 |
| ARP | Arena's blog source (lmarena/lmarena.github.io at 3366281): policy, style control, the May 9, 2025 reply; live copy at arena.ai/blog/our-response | VB | Pre-release testing policy; the reply's figures | 7 |
| AXO | axolotl-ai-cloud/axolotl at v0.21.0 (1f1eb05): LICENSE, README, telemetry manager and docs, installation and Mac docs | OD | Licence, hardware, telemetry | 9 |
| BID | Biderman et al., "LoRA Learns Less and Forgets Less", arXiv 2405.09673v2 (TMLR 2024 per the authors' README; not confirmed) | PP | LoRA against full fine-tuning; best practices | 7 |
| DEN | Deng et al., NAACL 2024 (Volume 1), pp. 8706 to 8719, doi:10.18653/v1/2024.naacl-long.482 (ACL Anthology data at 0d4dd55) | PR | 52% and 57% on masked MMLU options | 8 |
| DOR | Liu et al., "DoRA", ICML 2024, PMLR 235, pp. 32100 to 32121 (mlresearch/v235) | PR | Magnitude and direction | 7 |
| DPO | Rafailov et al., "Direct Preference Optimization", NeurIPS 2023, pp. 53728 to 53741 (proceedings abstract page) | PR | Preference tuning without a reward model | 8 |
| GEK | Gekhman et al., "Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?", EMNLP 2024, pp. 7765 to 7784 (ACL Anthology PDF and data) | PR | Unknown facts learned slowly; hallucination; early stopping | 9 |
| GEM | Google, Gemini API "Fine-tuning" page (last updated 2026-04-28) | OD | No tunable model since May 2025 | 9 |
| GP3 | Brown et al., "Language Models are Few-Shot Learners", arXiv 2005.14165: Table 2.1; Section 4 | PP | GPT-3's shape; the 13-word rule | 8 |
| GSM | Zhang et al., GSM1k, NeurIPS 2024 Datasets and Benchmarks Track (proceedings abstract page) | PR | "Up to 8%" drops; overfitting families | 7 |
| HFC | huggingface/hub-docs at 76be11b: model-cards.md, model-card-annotated.md, eval-results.md | OD | Card fields; `license: other`; `base_model`; verified scores | 9 |
| HFL | huggingface/course at 8b893f0, chapter 11, "When to Use SFT" | OD | Prompt first; reasons to fine-tune | 7 |
| HHB | huggingface_hub 2.2.0 wheel: constants.py, utils/_telemetry.py | OD | What switches its telemetry off | 9 |
| HLM | stanford-crfm/helm at 63754d0: README, docs/maintenance_mode.md | OD | Maintenance mode since June 1, 2026 | 9 |
| ILL | Singh et al., "The Leaderboard Illusion", arXiv 2504.20879 (abstract) | PP | The critique and its figures | 6 |
| LCF | ggml-org/llama.cpp at b11739: examples/training README and finetune.cpp | OD | An experimental, full-weight, 32-bit trainer | 9 |
| LLF | hiyouga/LLaMA-Factory at v0.9.5: LICENSE, README (memory table, Windows), data README; Gradio 5.49.1 analytics.py | OD | Licence, estimates, formats, web UI analytics | 8 |
| LLL | meta-llama/llama-models at 0e0b8c5: models/llama3, llama3_1, llama3_2, llama4 LICENSE | OD | Attribution, naming and output clauses | 10 |
| LOR | Hu et al., "LoRA", arXiv 2106.09685v2: Sections 4.1, 4.2, 5.1, Table 4; ICLR 2022 poster page | PR | ΔW = BA; scaling; q and v; GPT-3 figures | 9 |
| LVB | LiveBench/LiveBench at 1d1006a: README, changelog.md | OD | Design; self-reported contamination; ICLR 2025 per README | 8 |
| MCR | Mitchell et al., "Model Cards for Model Reporting", arXiv 1810.03993 (FAT* '19 per the authors' PDF; the publisher's page didn't load) | PR | Nine sections; disaggregated results | 8 |
| MIS | mistralai/platform-docs-public at e7de7a7 (deployment, migration guide, deprecated fine-tuning pages, evaluation guide); docs.mistral.ai models overview; mistralai/mistral-finetune README (archived) | OD | Licences per model; fine-tuning deprecated | 8 |
| MLX | ml-explore/mlx-lm at v0.32.2: LICENSE, mlx_lm/LORA.md, lora.py | OD | LoRA, DoRA, QLoRA on Apple silicon; data formats; 250 tokens per second | 9 |
| MUS | Hugging Face: meta-models organization page; Muse-Glimmer-30B card; Muse-Spark-Open-816B-A42B card (gated; licence summary only) | OD | Dates, sizes, licences, conditions, hardware | 7 |
| OAI | OpenAI developer docs: deprecations page ("Update to OpenAI's self-serve fine-tuning"; 2026-04-22 and 2026-10-14 entries); model-optimization, supervised fine-tuning and DPO guides; Terms of Use (effective January 1, 2026) | OD | Wind-down dates; methods; formats; minimum examples; safety checks; terms on outputs | 9 |
| OLL | Hugging Face: Open LLM Leaderboard discussion 1135 (retirement post) and organization page | OD | Retired March 13, 2025 | 9 |
| OVA | Ovadia et al., "Fine-Tuning or Retrieval?", EMNLP 2024, pp. 237 to 250 (ACL Anthology PDF and data) | PR | Retrieval against fine-tuning on new facts | 9 |
| PFT | huggingface/peft at v0.21.2 (eaa35c7): README, lora/config.py, utils/constants.py, lora/layer.py, LICENSE | OD | The printed example; defaults; target modules; scaling | 10 |
| PUB | Publishers' pages: QwenLM/Qwen3.8 README (2ea10dc) and the Qwen3.8 cards; openai/gpt-oss (5681a6b); ibm-granite Granite 4.1 README; microsoft/PhiCookBook and the Phi-4-reasoning-vision card; deepseek-ai organization and V4.1-Flash card; llama-models Llama 4 card; Gemma 4 (Part 11) | OD | The table in Section 3.4 | 7 |
| PYPI | PyPI JSON API, October 19, 2026 | OD | Versions, dates, pins, wheel sizes | 9 |
| QCF | config.json of Qwen2.5-3B-Instruct, Qwen3-0.6B and SmolLM2-135M-Instruct; the Qwen3-0.6B and SmolLM2 cards | OD | Shapes for the counts; licences | 9 |
| QIS | Qi et al., "Fine-tuning Aligned Language Models Compromises Safety", arXiv 2310.03693v1 (ICLR 2024 per the authors' README; not confirmed) | PP | Harmfulness after fine-tuning | 7 |
| QLR | Dettmers et al., "QLoRA", NeurIPS 2023 (proceedings page); artidoro/qlora at 7f4e95a | PR | 65B on 48 GB; NF4; double quantization; all linear layers | 9 |
| SEL | OpenAI model-selection guide; Anthropic "Choosing the right model"; Mistral evaluation guide (docs source) | OD | Test candidates on your own data | 8 |
| TFM | huggingface/transformers at v5.20.2: docs cpu.md, apple_silicon.md, chat_templating.md | OD | CPU and Mac training; chat templates | 9 |
| TRL | huggingface/trl at v1.16.0 (1b5c75e): usage_stats.md, trainer/base_trainer.py, dataset_formats.md, sft_trainer.md, lora_without_regret.md, grpo_trainer.md | OD | Telemetry; formats; completion-only loss; LoRA advice relayed; GRPO | 9 |
| TTN | pytorch/torchtune: v0.6.1 LICENSE; main README (bd2a0fc) | OD | No longer maintained | 9 |
| UNS | Unsloth 2026.10.7 and unsloth_zoo 2026.10.7 wheels from PyPI; unslothai/unsloth at 73d2598 (README, device_type.py, models/_utils.py) | OD | Licence headers; GPU requirement; statistics | 9 |
| ZER | Rajbhandari et al., "ZeRO", arXiv 1910.02054, Section 3 | PP | 16 bytes per parameter | 8 |

## Run on your computer

| Test | Command | Expected result |
|---|---|---|
| R1 | `python run_lab.py` | `17 of 17 checks passed` |
| R2 | `python mutation_check.py` | `33 of 33 mutations caught` |
| R3 | Section 7.5: `pip install torch==2.14.1 transformers==5.20.2 peft==0.21.2`, then `python reader_lora.py --steps 24` | PEFT's count equals the lab's (460,800 trainable); the loss falls; note the seconds per step |

Send back the output; each [R] above then becomes [T] with the date.

**Results so far** (October 20, 2026, on the owner's test PC: Windows 11 Pro, an Intel Core i5-9500T with 7.79 GB of memory (about 1.2 GB free during the run) and no GPU, Python 3.13.16, a fresh virtual environment made from the lab zip; run by script, not typed; record in claude/engineering-stack-windows-run-2026-10-20.md) [T]: R1 printed `17 of 17 checks passed`. R2 printed `33 of 33 mutations caught`, both with the script's UTF-8 output setting and without it. R3's install of torch 2.14.1, transformers 5.20.2 and PEFT 0.21.2 added 38 packages in 266 seconds, downloading 153 MB (the torch file was 124.1 MB; pip reused files cached for earlier labs). `reader_lora.py --steps 24` then printed both expected lines, with PEFT's own count and the lab's agreeing at `460,800 trainable of 134,975,808 parameters`; `Loss on the answers: 1.764 (first 3 steps) to 1.001 (last 3 steps)`; `Speed: 0.89 s per step (median), 103 tokens per second over 24 steps`; and an adapter of 1,858,776 bytes in `lora-out`. It exited with code 0 after 53.6 seconds, including the model download. Hugging Face's cache held 435 MB afterwards, for this model and Part 05's two.

## Checks run on this part

| Check | By | Result |
|---|---|---|
| Lab | `run_lab.py` on Python 3.13.16, 3.12.3 and 3.11.17 | 17 of 17 on each, before and after the fixes [T] |
| Mutation check | `mutation_check.py`, 33 deliberate breaks | 33 of 33 caught on each Python, before and after the fixes [T] |
| Worked tables | `demo.py` on all three Pythons | Identical output; every number quoted in Sections 3, 5 and 8 came from it or from the commands shown [T] |
| Reader test logic | `reader_lora.py --plan`; check c17's stand-in tokenizer for the prompt masking; the full run without its packages | The prediction, the masked labels and the missing-package message as shown in Section 7 [T]; the full run passed on the owner's Windows PC (row below) |
| Blind source check A | A separate agent that saw only 61 claims from Sections 1 to 3.6 and their sources; 41 web lookups | 52 supported, 8 partly supported, none contradicted, 1 not checkable |
| Blind source check B | The same, for 110 claims from Section 3.7 onward; 39 web lookups | 97 supported, 10 partly supported, none contradicted, 3 not checkable |
| Beginner test | A separate agent following Sections 6 to 9 only, as a new Linux user, on all three Pythons, without the reader test's packages | Every printed number matched; 30 problems in the text (2 high, 7 medium, 21 low) |
| Fixes | The lead reopened the source or reran the command behind each finding before changing anything | Findings, fixes and what was left: claude/engineering-stack-part-12-review.md |
| Windows run | The owner's Windows 11 PC, Python 3.13.16, by script, October 20, 2026 | R1 17 of 17, R2 33 of 33, R3 passed: counts agreed, loss 1.764 to 1.001, 0.89 s per step, 1.9 MB adapter [T]. Record: claude/engineering-stack-windows-run-2026-10-20.md |

## Cheat sheet

**Terms.** Contamination: test items in training data. Saturation: a test most models ace. Model card: a model's documentation; read licence, intended use, evaluation and `base_model`. Fine-tuning: more training on your examples. LoRA: two thin trained matrices beside a frozen layer. QLoRA: LoRA on a 4-bit frozen model. DPO: training on preferred and rejected pairs. Adapter: the saved LoRA matrices. Chat template: the model's fixed layout of a conversation.

**Formulas.**

```
LoRA trainable per matrix   = r x (inputs + outputs)
LoRA update                 = (alpha / r) x B A          (rsLoRA: alpha / sqrt(r))
full fine-tuning, Adam      = 16 bytes per weight + activations     (2 + 2 + 12)
LoRA, 16-bit base           = 2 bytes per base weight + 16 per trained weight + activations
QLoRA base                  = 4.127 bits per weight (NF4 with double quantization)
contamination check         = 13 words in a row shared with training data (GPT-3's rule)
```

**Facts (read October 19, 2026; check before use).**

```
PEFT 0.21.2       defaults r 8, alpha 8, q_proj and v_proj for Llama, Mistral, Qwen2, Qwen3
TRL 1.16.0        one telemetry ping per trainer; HF_HUB_DISABLE_TELEMETRY=1 or DO_NOT_TRACK=1
Unsloth 2026.10.7 needs a GPU (or Apple silicon via MLX); AGPL-3.0 headers in 81 of 159 core files
OpenAI            fine-tuning closed to new organizations since May 7, 2026; to all new jobs January 6, 2027
Gemini API        no tunable model since May 2025
Meta              Muse Spark Open (Oct 15, 2026): custom gated licence; Muse Glimmer 30B: Apache-2.0
Llama 3.1+        shared fine-tunes must be named "Llama..." and show "Built with Llama"
HELM              maintenance mode since June 1, 2026; Open LLM Leaderboard retired March 13, 2025
```

**Decision rules.**

1. Shortlist by licence and fit (Part 11), then decide on your own eval, never on a leaderboard alone.
2. Changing facts go in retrieval; formats, labels and habits are what fine-tuning is for.
3. Build the eval first; try prompting and other models second; fine-tune last.
4. Start with LoRA on all linear layers; test the rank; QLoRA when memory is short and you have an NVIDIA GPU.
5. Check data for format errors, duplicates and test leaks before training.
6. After training, re-run your eval with a paired test and a safety test; the base model's scores don't carry over.
7. Read the base model's licence before you name or share the result; turn off telemetry you didn't choose.

## Appendix: lab listing

The core file of the lab folder `engineering-stack-lab-part-12`, as tested: the arithmetic itself. `datacheck.py`, `run_lab.py`, `mutation_check.py`, `demo.py`, `reader_lora.py`, `README.md` and `data/` are in the zip (Section 8).

### adaptmath.py

```python
"""adaptmath: the arithmetic of choosing and adapting a model (Engineering Stack, Part 12).

Standard library only. Nothing here downloads or trains a model. Each table
names where its numbers come from; Part 12, Section 12, gives the sources.
"""
import math
from datetime import date

GB = 1e9

# ----------------------------------------------------------- 1. model shapes
# From each model's config.json. Qwen2 puts a bias on q, k and v; Qwen3 adds a
# small norm on q and on k instead. "tied": the output layer reuses the
# embedding matrix, so it is stored once.
LLAMA3_8B = dict(hidden=4096, layers=32, heads=32, kv_heads=8, head_dim=128, ffn=14336,
                 vocab=128256, tied=False, qkv_bias=False, qk_norm=False)
QWEN25_3B = dict(hidden=2048, layers=36, heads=16, kv_heads=2, head_dim=128, ffn=11008,
                 vocab=151936, tied=True, qkv_bias=True, qk_norm=False)
QWEN3_06B = dict(hidden=1024, layers=28, heads=16, kv_heads=8, head_dim=128, ffn=3072,
                 vocab=151936, tied=True, qkv_bias=False, qk_norm=True)
SMOLLM2_135M = dict(hidden=576, layers=30, heads=9, kv_heads=3, head_dim=64, ffn=1536,
                    vocab=49152, tied=True, qkv_bias=False, qk_norm=False)
# GPT-3 175B (Brown et al. 2020, Table 2.1): only the attention shapes are used.
GPT3_175B = dict(hidden=12288, layers=96, heads=96, kv_heads=96, head_dim=128, ffn=4 * 12288,
                 vocab=50257, tied=True, qkv_bias=True, qk_norm=False)

ALL_LINEAR = ("q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj")
# PEFT 0.21.2, src/peft/utils/constants.py: the default when you name no target.
PEFT_DEFAULT_TARGETS = {"llama": ("q_proj", "v_proj"), "mistral": ("q_proj", "v_proj"),
                        "qwen2": ("q_proj", "v_proj"), "qwen3": ("q_proj", "v_proj")}


def linear_shapes(c):
    """(inputs, outputs) of each linear layer in one transformer block."""
    q, kv, h, f = c["heads"] * c["head_dim"], c["kv_heads"] * c["head_dim"], c["hidden"], c["ffn"]
    return {"q_proj": (h, q), "k_proj": (h, kv), "v_proj": (h, kv), "o_proj": (q, h),
            "gate_proj": (h, f), "up_proj": (h, f), "down_proj": (f, h)}


def count_params(c):
    """All weights: embedding, blocks, final norm, and the output layer unless tied."""
    shapes = linear_shapes(c)
    block = sum(i * o for i, o in shapes.values()) + 2 * c["hidden"]       # two RMSNorms
    if c["qkv_bias"]:
        block += sum(shapes[n][1] for n in ("q_proj", "k_proj", "v_proj"))
    if c["qk_norm"]:
        block += 2 * c["head_dim"]
    embed = c["vocab"] * c["hidden"]
    return embed * (1 if c["tied"] else 2) + c["layers"] * block + c["hidden"]


# ------------------------------------------------------------ 2. LoRA counts
def lora_params(c, targets, r):
    """LoRA trains B (outputs x r) and A (r x inputs): r * (d + k) per matrix (Hu et al.)."""
    shapes = linear_shapes(c)
    return c["layers"] * sum(r * sum(shapes[t]) for t in targets)


def lora_scaling(alpha, r, rslora=False):
    """How much the update BA is multiplied by: alpha / r, or alpha / sqrt(r) with rsLoRA."""
    return alpha / math.sqrt(r) if rslora else alpha / r


# --------------------------------------------------- 3. memory for training
# ZeRO (Rajbhandari et al.), Section 3.1: mixed-precision Adam keeps 2 bytes of
# weights, 2 of gradients and 12 of optimizer state per trained parameter.
ADAM_MIXED_BYTES = 2 + 2 + 12
# QLoRA (Dettmers et al.): NF4 is 4 bits; one 32-bit constant per 64 weights adds
# 0.5 bits, and double quantization cuts that to 8/64 + 32/(64*256) = 0.127 bits.
NF4_BITS = 4 + 8 / 64 + 32 / (64 * 256)
NF4_BITS_NO_DOUBLE = 4 + 32 / 64
BASE_BITS = {"full": None, "lora_fp32": 32, "lora_bf16": 16, "qlora": NF4_BITS}


def training_bytes(n_base, method, n_adapter=0):
    """Model states only: no activations, batch, sequence length or framework overhead."""
    if method == "full":
        return ADAM_MIXED_BYTES * n_base
    return n_base * BASE_BITS[method] / 8 + ADAM_MIXED_BYTES * n_adapter


def fits(memory_gb, need_bytes, overhead=0.2):
    """Same rule as Part 11: keep a fifth of the memory free for everything not counted."""
    return need_bytes <= memory_gb * GB * (1 - overhead)


# ------------------------------------------------ 4. hosted fine-tuning dates
# OpenAI deprecations page, "Update to OpenAI's self-serve fine-tuning" (read
# October 19, 2026). Other providers: Part 12, Section 3.6.
OPENAI_CLOSED_TO_NEW = date(2026, 5, 7)
OPENAI_RECENT_ONLY = date(2026, 7, 2)
OPENAI_CLOSED_TO_ALL = date(2027, 1, 6)


def openai_can_start_job(day, tuned_before, inference_last_60_days):
    """Can this organization create a new fine-tuning job on OpenAI on this day?"""
    if day >= OPENAI_CLOSED_TO_ALL:
        return False
    if day >= OPENAI_RECENT_ONLY:
        return tuned_before and inference_last_60_days
    if day >= OPENAI_CLOSED_TO_NEW:
        return tuned_before
    return True


# -------------------------------------------------- 5. which way to adapt
# First rule that matches wins. Evidence: retrieval beat fine-tuning on new facts
# (Ovadia et al.); unknown facts raise hallucination once learned (Gekhman et al.);
# vendors say prompt and measure first (OpenAI, Anthropic, Hugging Face, Mistral).
RULES = [  # (question, answer that triggers the rule, advice, why)
    ("new_facts", True, "retrieve",
     "new facts are learned slowly and raise hallucination; retrieve (Part 05)"),
    ("have_eval", False, "build an eval",
     "without your own test set you can't tell if anything helped (Part 02)"),
    ("prompt_tried", False, "prompt", "try prompting and a stronger or smaller model first"),
    ("prompt_meets_bar", True, "stop", "prompting already passes your eval; keep it"),
    ("have_hardware", False, "rent a GPU", "no machine you have can train it (Section 6)"),
]


def choose_approach(**need):
    """need: new_facts, have_eval, prompt_tried, prompt_meets_bar, have_hardware (all bool)."""
    for key, value, answer, why in RULES:
        if need[key] == value:
            return answer, why
    return ("fine-tune with LoRA",
            "a measured gap on your eval that prompting couldn't close; re-run safety tests after")


# ------------------------------------------- 6. licence duties when sharing
# From each licence's own text (Part 12, Section 3.7). Information, not legal advice.
SHARING = {
    "apache-2.0": {"prefix": None, "notes": ["give a copy of the licence", "mark files you changed",
                                             "keep the NOTICE file's notices"]},
    "mit": {"prefix": None, "notes": ["keep the copyright and licence notice"]},
    "llama3": {"prefix": "Llama 3", "notes": ['show "Built with Meta Llama 3"', "ship the licence",
                                              "no outputs to improve other LLMs"]},
    "llama3.1": {"prefix": "Llama", "notes": ['show "Built with Llama"', "ship the licence"]},
    "muse-model-license": {"prefix": None, "notes": [
        'show "Built with Muse Spark Open"', "separate agreement to host it above a revenue threshold",
        "gated: read the full licence first"]},
}
SHARING["llama4"] = SHARING["llama3.1"]      # Llama 3.2 and Llama 4 use the same clause


def name_ok(licence, model_name):
    """Llama licences require the shared model's name to start with their word."""
    prefix = SHARING[licence]["prefix"]
    return prefix is None or model_name.startswith(prefix)


# ------------------------------------------------- 7. a first shortlist
# Publisher-stated facts read October 16 to 19, 2026 (Part 11 and Part 12).
# params: billions stored (all experts count, Part 11); ctx: tokens, with "128K"
# read as 131,072 and "1M" as 1,000,000.
CANDIDATES = [
    ("Qwen3.5-0.8B", 0.8, "apache-2.0", 262144),
    ("Granite 4.1 3B", 3.0, "apache-2.0", 524288),          # "up to 512K"
    ("Phi-4-mini-instruct", 3.8, "mit", 131072),
    ("Gemma 4 E2B", 5.1, "apache-2.0", 131072),
    ("gpt-oss-20b", 21.0, "apache-2.0", 131072),
    ("Qwen3.8-27B", 27.0, "apache-2.0", 262144),
    ("Muse Glimmer 30B", 29.6, "apache-2.0", 131072),
    ("Llama 4 Scout", 109.0, "llama4", 10_000_000),
    ("Muse Spark Open", 816.0, "muse-model-license", 1_000_000),
]
Q4_K_M_BITS = 4.89          # Part 11: about 4.89 bits per weight for Llama 3 8B


def shortlist(memory_gb, licences, min_ctx=0, bits=Q4_K_M_BITS):
    """Candidates whose weights fit at about Q4_K_M, with an allowed licence and context."""
    keep = []
    for name, params, licence, ctx in CANDIDATES:
        if licence in licences and ctx >= min_ctx and fits(memory_gb, params * 1e9 * bits / 8):
            keep.append(name)
    return keep
```
