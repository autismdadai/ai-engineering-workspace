import sys
sys.path.insert(0, "/home/claude/part11/tools")
from p4fix_lib import patch

D = "/home/claude/part11/draft/"

OLD_71 = """### 7.1 to 7.3 Windows, macOS and Linux

The same steps as Part 10, Sections 7.1 to 7.3, in this lab's folder. In PowerShell on Windows [R: typed steps not run on Windows; Parts 01 and 02's labs ran there on October 12, 2026]:
"""
NEW_71 = """### 7.1 to 7.3 Windows, macOS and Linux

**7.1 Windows,** in PowerShell [R: typed steps not run on Windows; Parts 01 and 02's labs ran there on October 12, 2026]:
"""

OLD_72 = """python run_lab.py
```

On macOS [R: no macOS test machine] and Linux [T]:
"""
NEW_72 = """python run_lab.py
```

If PowerShell refuses to run `Activate.ps1`, use Part 01's one-time fix (Part 01, Section 7.1, step 5), then activate again.

**7.2 macOS** [R: no macOS test machine] **and 7.3 Linux** [T]:
"""

OLD_75 = """1. Download `OllamaSetup.exe` from https://ollama.com/download and run it. It installs in your home folder without administrator rights and needs at least 4 GB of disk [V: OLS].
2. To keep it local, quit Ollama from the taskbar, open *Edit environment variables for your account*, add `OLLAMA_NO_CLOUD` with the value `1`, and start Ollama again from the Start menu, the route Ollama's FAQ gives for its settings [V: OLS]. If you want to choose when it updates, turn off *Auto-download updates* in its settings; it will still check hourly [V: OLS].
3. In PowerShell: `ollama pull qwen3:1.7b` (1.4 GB; Apache-2.0) [V: OLB, MCD].
4. In the lab folder: `python reader_local.py --model qwen3:1.7b --bandwidth 41.6`, using your own processor's memory bandwidth (Intel lists it on each processor's specification page) [R].

**Expected:** a measured speed below the printed ceiling, which for a 1.4 GB file at 41.6 GB/s is 29.7 tokens per second [T: the ceiling]. The script exits with an error if the measurement beats the ceiling, because then the bandwidth or the model name is wrong [T]. Send back what it prints. On macOS, Ollama installs as an app [R]; on Linux, read its install script first (Section 3.8) [R].

**The llama.cpp route,** with no service left running: `winget install llama.cpp`, download Qwen's own GGUF of Qwen3 4B at Q4_K_M (2.5 GB) from Hugging Face, then `llama-bench -m` with that file. It prints prompt (`pp512`) and generation (`tg128`) speeds; the generation speed should stay below 41.6 / 2.5 = 16.6 tokens per second [V: LCP, MCD][R].
"""
NEW_75 = """1. Download `OllamaSetup.exe` from https://ollama.com/download and run it. It installs in your home folder without administrator rights and needs at least 4 GB of disk [V: OLS].
2. To keep it mostly local, follow Ollama's FAQ: quit Ollama by clicking its icon in the taskbar, open Settings (Windows 11) or Control Panel (Windows 10) and search for *environment variables*, click *Edit environment variables for your account*, create `OLLAMA_NO_CLOUD` with the value `1`, click OK, and start Ollama again from the Start menu [V: OLS]. That stops its cloud models, web search and model recommendations, not its hourly update check; turning off *Auto-download updates* in its settings stops only the download [V: OLS].
3. Open a new PowerShell window, since one opened before the install won't find `ollama` (Part 01, Section 7.6), and run `ollama pull qwen3:1.7b` (1.4 GB; Apache-2.0) [V: OLB, MCD].
4. In that window, go to the lab folder and activate its environment again (Section 7.1), then run `python reader_local.py --model qwen3:1.7b --bandwidth 41.6` with your own memory bandwidth in place of 41.6 [R]. Intel lists it on each processor's specification page; *Settings, System, About* names your processor [R]. Otherwise multiply the memory's transfer rate by 8 bytes and by the number of channels: DDR4-2666 in two channels gives 2,666 million x 8 x 2 = 42.7 GB/s, near Intel's 41.6 [T: the arithmetic]. If Ollama runs the model on a GPU or a Mac, use that memory's bandwidth (Section 3.9).

**Expected:** a measured speed below the printed ceiling. For qwen3:1.7b at 41.6 GB/s the ceiling is about 30 tokens per second (29.7 for exactly 1.4 GB; the script uses the exact size it prints) [T]. The script exits with an error if the measurement beats the ceiling, because then the bandwidth or the model name is wrong [T]. Note what it prints for reader test R3 (Section 12).

**On macOS,** Ollama installs as an app from the same page; set the variable with `launchctl setenv OLLAMA_NO_CLOUD 1`, restart Ollama, then do steps 3 and 4 in Terminal [V: OLS][R]. **On Linux,** read the install script first (Section 3.8); it sets up a system service, so add `Environment="OLLAMA_NO_CLOUD=1"` under `[Service]` with `sudo systemctl edit ollama.service`, then run `sudo systemctl daemon-reload` and `sudo systemctl restart ollama` [V: OLS][R].

**The llama.cpp route** (reader test R4): `winget install llama.cpp`, then open a new PowerShell window. In your browser, open https://huggingface.co/Qwen/Qwen3-4B-GGUF, go to *Files and versions*, and download `Qwen3-4B-Q4_K_M.gguf` (2.5 GB; Apache-2.0) [V: MCD]. Then run `llama-bench -m $HOME\\Downloads\\Qwen3-4B-Q4_K_M.gguf`. It prints prompt (`pp512`) and generation (`tg128`) speeds [V: LCP]; the generation speed should stay below your bandwidth divided by 2.5 GB, 16.6 tokens per second at 41.6 GB/s [T: the arithmetic][R].
"""

OLD_76 = """| `can't open file '.../run_lab.py'` | The terminal isn't in the lab folder | `cd` into it [T] |
| `qwen3:1.7b isn't pulled yet. Run: ollama pull qwen3:1.7b` | The model isn't downloaded | Run that command [T] |
| `Can't reach Ollama at http://127.0.0.1:11434: is it running?` | Ollama isn't running | Start it from the Start menu [T: the message] |
| `Above the ceiling: check --bandwidth and the model name.` | A wrong bandwidth figure | Look up your processor's figure [T] |
"""
NEW_76 = """| PowerShell refuses to run `Activate.ps1` | Its script policy | Part 01's one-time fix (Part 01, Section 7.1, step 5) [R] |
| `can't open file '.../run_lab.py': [Errno 2] No such file or directory` | The terminal isn't in the lab folder | `cd` into it [T] |
| `ollama` is "not recognized" just after installing | The window was opened before the install | Open a new PowerShell window (Part 01, Section 7.6) [R] |
| `qwen3:1.7b isn't pulled yet. Run: ollama pull qwen3:1.7b` | The model isn't downloaded | Run that command [T] |
| `Can't reach Ollama at http://127.0.0.1:11434: is it running?`, then a reason in brackets | Ollama isn't running | Start it: Start menu (Windows), Applications (macOS), `sudo systemctl start ollama` (Linux) [T: the message][V: OLS] |
| `Above the ceiling: check --bandwidth (on a GPU or a Mac, use that memory's figure) and the model name.` | The model ran on a GPU, or the bandwidth figure is wrong | Use the bandwidth of the memory the model ran on [T: the message] |
"""

patch(D + "s06.md", [
    ("| llama.cpp | Run and benchmark GGUF models; no background service |",
     "| llama.cpp | Run and benchmark GGUF models from the command line |"),
    ("| LM Studio | A desktop app for local models | Proprietary, free for personal and internal business use | Windows with AVX2, macOS 14 on Apple silicon |",
     "| LM Studio | A desktop app for local models | Proprietary; personal and internal business use; some features paid | Windows (x64 with AVX2, or Arm), macOS 14 on Apple silicon, Linux |"),
    ("or llama.cpp when you'd rather have no background service and no update checks, with",
     "or llama.cpp when you'd rather start each program yourself, with"),
    ("- **Best free option:** all of these are free to download; the cost is the hardware, or the hours of a rented GPU.",
     "- **Best free option:** every tool here but LM Studio is open source under MIT or Apache-2.0; the cost is the hardware, or the hours of a rented GPU [V: LMS]."),
    ("`python3 -m zipfile -e engineering-stack-lab-part-11.zip ~/ai-stack` [T on Linux].",
     "`python3 -m zipfile -e engineering-stack-lab-part-11.zip ~/ai-stack` [T on Linux]; it prints nothing, so check with `ls ~/ai-stack/engineering-stack-lab-part-11`, which should list six files [T]."),
    (OLD_71, NEW_71),
    (OLD_72, NEW_72),
    ("| `python demo.py` | Prints Sections 3 and 5's tables |",
     "| `python demo.py` | Prints the eight worked tables behind Sections 3 and 5 |"),
    ("| `python reader_local.py --self-test` | Runs the reader test against a stand-in for Ollama |",
     "| `python reader_local.py --self-test` | Runs the reader test against a stand-in for Ollama; its last line is `Self-test passed: these numbers come from the stand-in, not a model.` [T] |"),
    ("In your own code: `rm.gguf_bytes(rm.llama_tensors(cfg), rm.k_quant_m(\"Q4_K\", \"Q6_K\"), n_layers)` sizes a Q4_K_M file from a Llama-style configuration, `rm.kv_bytes",
     "In your own code, after `import runmath as rm` and `cfg = rm.LLAMA3_8B`: `rm.gguf_bytes(rm.llama_tensors(cfg), rm.k_quant_m(\"Q4_K\", \"Q6_K\"), cfg[\"n_layers\"])` returns 4912898048, the bytes of a Q4_K_M file's tensors [T]; `rm.kv_bytes"),
    (OLD_75, NEW_75),
    (OLD_76, NEW_76),
    ("`Remove-Item -Recurse -Force engineering-stack-lab-part-11` in PowerShell [R]. The mutation check",
     "`Remove-Item -Recurse -Force engineering-stack-lab-part-11` in PowerShell [R]. After `deactivate`, type `python3` rather than `python` on macOS and Linux. The mutation check"),
])
