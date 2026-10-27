# Part 11, Sections 6 to 9 (as given to the beginner tester)

## 6. What you need

Checked October 16, 2026 [V: PYPI, GHT]. Licences from each project's licence file; information, not legal advice.

| Tool | What it's for | Licence | Runs on | Account or key? | Version |
|---|---|---|---|---|---|
| The lab's scripts | Memory, file-size, speed and serving arithmetic | This series | Python 3.11 to 3.13, standard library [T] | No | Lab zip |
| Ollama | Run local models with one command | MIT | Windows 10 22H2 or later, macOS 14 or later, Linux | Not for local models; cloud models need one | v0.40.5 |
| llama.cpp | Run and benchmark GGUF models; no background service | MIT | Windows, macOS, Linux; CPU or most GPUs | No; gated Hugging Face models need an account (Part 10) | b11691 |
| LM Studio | A desktop app for local models | Proprietary, free for personal and internal business use | Windows with AVX2, macOS 14 on Apple silicon | No | Terms of August 23, 2026 |
| vLLM | Serving many users on GPUs | Apache-2.0 | Linux; NVIDIA, AMD, Intel GPUs | No; usage statistics on by default | 0.31.0 |
| SGLang | The same, with a radix prefix cache | Apache-2.0 | Linux, Python 3.11 or later, CUDA 13 | No | 0.5.22 |
| TensorRT-LLM | NVIDIA's engine | Apache-2.0 | Linux on NVIDIA GPUs only | No | 1.2.1 (stable) |
| MLX-LM | Local models on Apple silicon | MIT | macOS on Apple silicon | No | 0.32.2 |
| llm-compressor, GPTQModel | Making AWQ and GPTQ models | Apache-2.0 | GPUs | No | 0.14.0; 7.6.0 |

Sources: Sections 3.3, 3.7 and 3.8 [V: OLS, LCP, LMS, VSR, SGS, TRL, MLX, QTL].

Picks, and when to skip them:

- **Best default for a solo builder on an ordinary computer:** Ollama for the easiest start, or llama.cpp when you'd rather have no background service and no update checks, with a 1 to 4 billion parameter model under Apache-2.0 or MIT at Q4_K_M. With Ollama, set `OLLAMA_NO_CLOUD=1` unless you want its cloud models [V: OLS, LCP, MCD].
- **For production on GPUs:** vLLM or SGLang, both Apache-2.0 and active; turn off vLLM's usage statistics, and measure TTFT and TPOT on your own traffic. TensorRT-LLM if NVIDIA-only Linux suits you. Don't start new work on TGI, which is in maintenance mode [V: VSR, SGS, TRL, TGI].
- **On a Mac:** Ollama or llama.cpp (Metal), or MLX-LM; MLX-LM's own docs warn against its server in production [V: LCP, MLX].
- **Best free option:** all of these are free to download; the cost is the hardware, or the hours of a rented GPU.
- **No single best engine.** No independent comparison of engines on the same hardware was read; MLPerf compares whole systems their makers submit [V: MLP].
- **When not to run your own:** light or bursty traffic and no GPU. A hosted API bills per token, while your own GPU costs the same idle or busy [I].

## 7. Set it up

**Before you start.** Part 01's setup: Python 3.11 to 3.13 and the series folder `ai-stack` in your home folder. Unzip `engineering-stack-lab-part-11.zip` into `ai-stack`: on Windows, right-click, Extract All, destination `ai-stack` (if the folder ends up inside another of the same name, move the inner one up) [R]; on macOS, double-click and move the folder into `ai-stack`; on Linux, from the folder holding the zip, `python3 -m zipfile -e engineering-stack-lab-part-11.zip ~/ai-stack` [T on Linux]. The core lab needs nothing installed. Type each command on its own line.

### 7.1 to 7.3 Windows, macOS and Linux

The same steps as Part 10, Sections 7.1 to 7.3, in this lab's folder. In PowerShell on Windows [R: typed steps not run on Windows; Parts 01 and 02's labs ran there on October 12, 2026]:

```
cd $HOME\ai-stack\engineering-stack-lab-part-11
py -V:3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python run_lab.py
```

On macOS [R: no macOS test machine] and Linux [T]:

```
cd ~/ai-stack/engineering-stack-lab-part-11
python3.13 -m venv .venv
source .venv/bin/activate
python run_lab.py
```

Expect `14 of 14 checks passed`. If `py -V:3.13` or `python3.13` isn't found, use the 3.11 or 3.12 from Part 01. A virtual environment isn't strictly needed, since nothing gets installed, but it keeps the habit.

### 7.4 A tour

| Command | What it does |
|---|---|
| `python run_lab.py` | 14 checks; exit code 0 only if all pass |
| `python mutation_check.py` | Breaks the lab 31 ways in temporary copies; each must make `run_lab.py` fail (about 15 seconds) |
| `python demo.py` | Prints Sections 3 and 5's tables |
| `python reader_local.py --self-test` | Runs the reader test against a stand-in for Ollama |

In your own code: `rm.gguf_bytes(rm.llama_tensors(cfg), rm.k_quant_m("Q4_K", "Q6_K"), n_layers)` sizes a Q4_K_M file from a Llama-style configuration, `rm.kv_bytes(layers, kv_heads, head_size, tokens)` sizes the cache, and `rm.decode_ceiling(bandwidth, bytes_per_token)` gives the speed limit.

### 7.5 Reader test R3: a small model on your computer [R]

This downloads Ollama and a 1.4 GB model, and installs Ollama as an app with a background service; skip it if you'd rather not. On Windows:

1. Download `OllamaSetup.exe` from https://ollama.com/download and run it. It installs in your home folder without administrator rights and needs at least 4 GB of disk [V: OLS].
2. To keep it local, quit Ollama from the taskbar, open *Edit environment variables for your account*, add `OLLAMA_NO_CLOUD` with the value `1`, and start Ollama again from the Start menu, the route Ollama's FAQ gives for its settings [V: OLS]. If you want to choose when it updates, turn off *Auto-download updates* in its settings; it will still check hourly [V: OLS].
3. In PowerShell: `ollama pull qwen3:1.7b` (1.4 GB; Apache-2.0) [V: OLB, MCD].
4. In the lab folder: `python reader_local.py --model qwen3:1.7b --bandwidth 41.6`, using your own processor's memory bandwidth (Intel lists it on each processor's specification page) [R].

**Expected:** a measured speed below the printed ceiling, which for a 1.4 GB file at 41.6 GB/s is 29.7 tokens per second [T: the ceiling]. The script exits with an error if the measurement beats the ceiling, because then the bandwidth or the model name is wrong [T]. Send back what it prints. On macOS, Ollama installs as an app [R]; on Linux, read its install script first (Section 3.8) [R].

**The llama.cpp route,** with no service left running: `winget install llama.cpp`, download Qwen's own GGUF of Qwen3 4B at Q4_K_M (2.5 GB) from Hugging Face, then `llama-bench -m` with that file. It prints prompt (`pp512`) and generation (`tg128`) speeds; the generation speed should stay below 41.6 / 2.5 = 16.6 tokens per second [V: LCP, MCD][R].

**To uninstall Ollama:** *Add or remove programs* in Windows Settings; its uninstaller removes models kept in the default place [V: OLS]. Delete the `OLLAMA_NO_CLOUD` variable the same way you added it.

### 7.6 Common errors and fixes

| What you see | Why | Fix |
|---|---|---|
| `can't open file '.../run_lab.py'` | The terminal isn't in the lab folder | `cd` into it [T] |
| `qwen3:1.7b isn't pulled yet. Run: ollama pull qwen3:1.7b` | The model isn't downloaded | Run that command [T] |
| `Can't reach Ollama at http://127.0.0.1:11434: is it running?` | Ollama isn't running | Start it from the Start menu [T: the message] |
| `Above the ceiling: check --bandwidth and the model name.` | A wrong bandwidth figure | Look up your processor's figure [T] |

### 7.7 How to uninstall the lab

`deactivate`, move up one folder with `cd ..`, and delete `engineering-stack-lab-part-11`: `rm -rf engineering-stack-lab-part-11` on macOS and Linux [T], `Remove-Item -Recurse -Force engineering-stack-lab-part-11` in PowerShell [R]. The mutation check deletes its own temporary folders [T].

## 8. Hands-on lab: will it fit, and how fast can it go?

**Goal.** Size a model's file and its KV cache from its configuration, find the speed ceiling on any hardware, reproduce llama.cpp's published file sizes, see why speculative decoding can't always help, break the arithmetic on purpose, and prove the checks notice. Then, if you like, time a real model on your own computer.

**Prerequisites.** Section 7 for your system. **Time:** about 30 minutes by hand, under a minute automated. **Cost:** none. **Pinned:** the standard library only. **Data:** the published configurations of Llama 3 8B and gpt-oss-20b, and the published figures named in each check [V: LLM, GOS, LCP]; the PC's free memory and the lab's 10% margin are invented [I]. **Files:** all are in the zip; `runmath.py`, the arithmetic, is also printed in the appendix. The others: `run_lab.py`, `mutation_check.py`, `demo.py`, `reader_local.py` and `README.md`.

**Steps.** Outputs are from the test machine, Python 3.13.16, October 16, 2026 [T].

1. **Read the arithmetic.** Open `runmath.py`: each function is a few lines, and its docstring names the source.
2. **Print the tables.** `python demo.py` prints this part's tables, starting with the file sizes beside llama.cpp's own:

   ```
   1. Llama 3 8B file sizes (tensor data), against llama.cpp's published table
      8,030,261,248 weights
      F16     16.0005 bits/weight  14.96 GiB  16.06 GB   llama.cpp: 16.0005 and 14.96 GiB
      Q4_K_M   4.8944 bits/weight   4.58 GiB   4.91 GB   llama.cpp: 4.8944 and 4.58 GiB
   ```

3. **Size a longer context.** `python -c "import runmath as rm; print(rm.kv_bytes(32, 8, 128, 32768) / rm.GIB)"` prints `4.0`: Llama 3 8B's cache for one 32,768-token conversation is as large as its 4-bit weights [T].
4. **Find your own ceiling.** `python -c "import runmath as rm; print(rm.decode_ceiling(41.6e9, 1.4e9))"` prints `29.714285714285715`: the most a 1.4 GB model can do on a 41.6 GB/s PC [T]. Put in your own figures.
5. **Break it.** In `runmath.py`, change `"Q6_K": (256, 210)` to `"Q6_K": (256, 208)`, two bytes short per block. `python run_lab.py` now ends `10 of 14 checks passed`: the file sizes, the fit check and the speed ceiling all move, because Q4_K_M uses Q6_K for some tensors [T]. Put it back and confirm 14 of 14.
6. **Speculation.** `python -c "import runmath as rm; print(rm.best_gamma(0.8, 0.05), rm.speedup(0.8, 8, 0.05))"` prints `8 3.0920795428571433` [T]. Try an acceptance rate below the draft's cost, such as `rm.speedup(0.2, 4, 0.25)`: under 1, slower than not speculating.
7. **Prove the checks can fail.** `python mutation_check.py` breaks the lab 31 ways (a block without its scales, a wrong layer rule, keys without values, the sliding window ignored, the ceiling upside down, TPOT divided by every token, nanoseconds read as seconds, and more) and expects `run_lab.py` to fail each time. Expect `31 of 31 mutations caught` in about 15 seconds [T]. All 31 were caught on the first run; one check (c08) failed on its own first run because its expected value had been typed in rather than computed, and was corrected to the computed 80,482 tokens [T].
8. **Time a real model (optional).** Section 7.5 [R].

**Expected output** (`python run_lab.py`, abridged):

```
PASS c01_feed_forward_width
PASS c05_file_sizes_match_llama_cpp
PASS c06_gpt_oss_20b
PASS c11_speculative_decoding
PASS c14_reader_test_logic
...
14 of 14 checks passed
```

**If it fails.** A FAIL line names the check and the failing value; Section 7.6 covers the common errors. A check that fails only on your machine is worth reporting: send the whole output.

## 9. Teach it

**Learning objectives.** After this part you can:

1. work out a model's weight and KV-cache memory from its configuration, and whether it fits;
2. give a speed ceiling for decoding from bandwidth and bytes per token, and say when compute takes over;
3. explain what a quantization type stores, why "4-bit" files are nearer 5 bits, and what quantization costs;
4. say what a serving engine adds (batching by step, paged KV memory, preemption, prefix caching) and read TTFT, TPOT and ITL by their formulas;
5. read a GPU datasheet for what matters: memory, bandwidth, sparse versus dense, and whether a figure is preliminary.

**Prerequisites.** Part 01; Part 04 for the KV cache and prefix caching. Reading a little Python.

**Common misconceptions.**

- *"More TFLOPS means faster chat."* One conversation at a time is limited by bandwidth; compute matters for prompts and for big batches [V: VLL, NVI][T].
- *"A 4-bit model is a quarter of the 16-bit file."* Q4_K_M is 4.89 bits per weight, 30.6% of 16-bit [T].
- *"Quantization is free."* +2.79% perplexity on Llama 3 8B at Q4_K_M, and averages hide flipped answers [V: LCP, DUT].
- *"Running locally means nothing leaves my computer."* Ollama calls ollama.com unless told not to [V: OLS].
- *"A 21-billion-weight model needs 21 billion weights' worth of bandwidth."* Not a mixture of experts: gpt-oss-20b reads 3.71 GB per token [T].

**Exercises, with checked answers.** Run the checks from the lab folder.

1. *A long context on a window model.* How much KV cache does gpt-oss-20b need for 32,768 tokens? Answer: 0.75 GiB, since half its layers keep only 128 tokens. Check: `python -c "import runmath as rm; print(rm.kv_bytes(24, 8, 64, 32768, window=128, windowed_layers=12) / rm.GIB)"` prints `0.7529296875` [T].
2. *A Mac.* What is the ceiling for Llama 3 8B at Q4_K_M on an Apple M5 Pro (307 GB/s)? Answer: about 62.5 tokens per second. Check: `python -c "import runmath as rm; print(rm.decode_ceiling(307e9, 4.912898048e9))"` prints `62.48857537863566` [T].
3. *Worth speculating?* A draft is accepted half the time and costs 0.4 of a target pass. Answer: yes, barely: α beats c, the best γ is 1, and the speed-up is (1 + 0.5) / (1 + 0.4) = 1.07 times. Check: `python -c "import runmath as rm; g = rm.best_gamma(0.5, 0.4); print(g, rm.speedup(0.5, g, 0.4))"` prints `1 1.0714285714285714` [T].

**Five-question self-check.** Answers follow.

1. Why is decoding one conversation limited by memory bandwidth rather than compute?
2. Which numbers do you need to size a KV cache, and what is Llama 3 8B's per token?
3. GGUF, AWQ and GPTQ: which is a file format?
4. What does vLLM 0.31.0 do when it runs out of KV blocks?
5. An NVIDIA table lists 3,958 TFLOPS. What two questions do you ask?

*Answers.* (1) Each new token reads every weight once while doing little arithmetic per byte, so bytes per second sets the pace [V: VLL][T]. (2) Layers, KV heads, head size, bytes per value and tokens; 131,072 bytes [T]. (3) GGUF [V: GGS]. (4) It preempts the request scheduled last and recomputes it later; swapping to CPU was removed [V: VSR]. (5) Which precision, and with or without sparsity; also whether the table is preliminary [V: NVH, HGX, NVB].

**You've got it when** you can take any model card and any computer's specifications and say, within a minute, whether it fits, roughly how fast it can go at best, and which of the two you would change first.

**Best next resources** (checked to exist on October 16, 2026): the vLLM paper [V: VLL]; Leviathan et al. [V: LEV]; llama.cpp's quantize and perplexity READMEs [V: LCP]; Ollama's FAQ [V: OLS]; Williams, Waterman and Patterson's roofline report [V: RFL].

**A tutor prompt to practise with.** Paste this into Claude (modelled on claude/github-tutor-prompt.md):

```
Help me learn to run AI models on my own hardware and to size servers for them.

How to teach me: one idea at a time, a question I answer before you go on,
and a small worked example with real arithmetic for each idea. When I'm
wrong, show me the reasoning rather than the answer, so I can find the
mistake myself.

Topics, in order:
1. Prefill and decode, and why decoding is limited by memory bandwidth.
2. Weight memory and the KV cache: the formulas, with a model card I choose.
3. Quantization: what a block stores, bits per weight, what quality it costs.
4. Serving engines: batching, paged KV memory, prefix caching, and the
   metrics TTFT, TPOT and ITL.
5. Speculative decoding: acceptance rate, draft cost, when it pays.
6. Reading a GPU datasheet: memory, bandwidth, sparse versus dense.

For any product, version, price or benchmark figure, tell me it may have
changed since your training and that I should check the maker's page.

Start by asking what computer I have and which model I want to run.
```

**What to learn next.** Part 12, adapting models: choosing a model, and when fine-tuning beats prompting or retrieval.

