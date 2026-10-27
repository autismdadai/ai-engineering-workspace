# Engineering Stack: Windows Run, October 19, 2026

*The Part 11 reader tests R1 to R4 on the owner's Windows 11 computer, run by Claude through the desktop app with the owner's go-ahead to install and run R3 and R4. The session could click but not type in Windows' terminals, so each step ran from a PowerShell script started by double-clicking a .bat file in Downloads\ai-stack, and every result below is copied from the script's log, part11-reader-tests.log. Downloads came only from official sources and each was checked against its published SHA-256 before use.*

## The computer

Windows 11 Pro 10.0.26300; PowerShell 5.1.26100.9711; Intel Core i5-9500T (6 cores, 6 threads); 7.79 GB of memory with 0.66 to 3 GB free during the runs; Intel UHD Graphics 630 (driver 31.0.101.2141); Python 3.13.16 from python.org (installed October 12).

**One finding that changes Part 11's numbers for this PC:** a single 8 GB module in slot DIMM1, rated and running at 2,666 MT/s. One module means one memory channel, so the bandwidth is about 2,666 million x 8 bytes = 21.3 GB/s, half of Intel's 41.6 GB/s figure, which assumes two channels [T: the arithmetic; the module data from Windows].

## Results

| Test | What ran | Result |
|---|---|---|
| R1 | `run_lab.py` in a fresh virtual environment | 14 of 14 checks passed |
| R2 | `mutation_check.py` | 31 of 31 mutations caught, 20.2 s |
| Self-test | `reader_local.py --self-test` | "Self-test passed" |
| R3 setup | OllamaSetup.exe v0.40.6 (1,584,629,376 bytes) from its GitHub release; SHA-256 933794ee...0828 matched both sha256sum.txt and the release page; installed for this user only; `OLLAMA_NO_CLOUD=1` set as a user variable first | Ollama's log: "Ollama cloud disabled: true"; it dropped the integrated GPU ("to enable, set OLLAMA_IGPU_ENABLE=1") and ran on the processor, reporting 7.8 GiB total and 825.6 MiB available |
| R3 | `ollama pull qwen3:1.7b` (1,359,293,444 bytes), then `reader_local.py --runs 5` at 41.6 and at 21.3 GB/s | 8.4 and 8.0 tokens per second (two runs, each the median of five). Ceilings: 30.6 at 41.6 GB/s (27%) and 15.7 at 21.3 GB/s (51%) |
| R4 setup | `winget install llama.cpp`: build b11706, Vulkan, from llama.cpp's GitHub release (hash verified by winget); Qwen3-4B-Q4_K_M.gguf (2,497,280,256 bytes) from Qwen's Hugging Face repository | The first download broke at 1,242,463,457 bytes (curl error 56, the server closed the connection), so the checksum refused it; a resumed download completed and matched the published SHA-256 7485fe6f...fdf5 |
| R4 | `llama-bench -m Qwen3-4B-Q4_K_M.gguf`, default settings (all layers on the Vulkan device, the UHD 630, 3,588 MiB free) | pp512 8.61 ± 0.48, tg128 2.19 ± 0.05 tokens per second |
| R4 | The same with `-dev none` (processor only) | pp512 34.90 ± 0.82, tg128 3.93 ± 0.07 tokens per second. Ceilings for generation: 16.7 at 41.6 GB/s (24%) and 8.5 at 21.3 GB/s (46%) |

## What it shows

- Every measured generation speed stayed below its bandwidth ceiling, as Part 11 predicts; with the single-channel figure the processor reached about half its ceiling in both tests [T].
- On this PC the integrated GPU through Vulkan was slower than the processor alone: 4.1 times slower reading the prompt and 1.8 times slower writing. Ollama's default of skipping the integrated GPU suits it [T]. Part 11 had left Vulkan on the UHD 630 untested [U].
- Free memory was low (under 1 GB before the Ollama run), which may have cost some speed; not measured separately.

## Problems met, and fixes

- The first script used `Start-Process -Wait`, which in Windows PowerShell 5.1 waits for every process the started program launches. Ollama's installer starts the Ollama app, so the script waited until the evening. A follow-up script waited for each program alone (`WaitForExit`) and stopped the stuck run.
- The model download broke halfway; a second script resumed it with `curl -C -` and checked the hash again.

## What stays installed

Ollama v0.40.6 with qwen3:1.7b, the `OLLAMA_NO_CLOUD` user variable, llama.cpp b11706 (winget) and Qwen3-4B-Q4_K_M.gguf in Downloads. Part 11, Section 7.5, says how to remove them.

## Still not run on this PC

Part 11's typed PowerShell steps (the scripts ran them instead), Parts 01 and 02's R4, and the reader tests of Parts 03 to 10 and 12.
