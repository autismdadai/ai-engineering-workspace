# Engineering Stack: heavy reader tests on this computer (October 20, 2026).
# Run by Claude with the owner's go-ahead, after stack-reader-tests-a.ps1 made each lab's
# virtual environment. Downloads come only from PyPI, Hugging Face (the models' own
# repositories), spaCy's GitHub releases and the local Ollama server already installed.
#   R2 again for each part, without PYTHONIOENCODING (as a reader's console runs it).
#   Part 12 R3: torch 2.14.1, transformers 5.20.2, peft 0.21.2; SmolLM2-135M-Instruct; 24 LoRA steps.
#   Part 05 R4: sentence-transformers 6.1.0 (pulls torch); two MiniLM models; real_models.py.
#   Part 10 R4: spaCy's en_core_web_lg (about 382 MB); reader_presidio.py.
#   Part 10 R5: garak 0.17.0 in its own virtual environment; --list_probes; the test.Blank self-test.
#   Part 04 R4: the position test on qwen3:1.7b in Ollama (200 documents, num_ctx 16384, 10 trials).
# Hugging Face telemetry is off (HF_HUB_DISABLE_TELEMETRY=1, DO_NOT_TRACK=1) for every step.
# Everything is written to stack-reader-tests-b.log in this folder.

$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$Root = Join-Path $env:USERPROFILE 'Downloads\ai-stack'
$Zips = Join-Path $env:USERPROFILE 'Downloads'
$Work = Join-Path $Root 'stack-reader-tests'
$Log  = Join-Path $Root 'stack-reader-tests-b.log'
New-Item -ItemType Directory -Force -Path $Work | Out-Null
# Python writes redirected output in UTF-8, so non-ASCII characters in a lab's output
# can't crash it when it goes to a file instead of a console.
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'

function Log([string]$text) {
    Add-Content -Path $Log -Value $text -Encoding UTF8
    Write-Host $text
}
function Step([string]$name) {
    Log ''
    Log ('==== ' + $name + '  [' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + ']')
}
function Run([string]$file, [string]$argString, [string]$name, [string]$dir = $Work, [int]$tailErr = 0, [int]$limit = 1800) {
    # Waits for this one process only (Start-Process -Wait would wait for its children too).
    $o = Join-Path $Work ($name + '.out.txt')
    $e = Join-Path $Work ($name + '.err.txt')
    Log ('> ' + $argString)
    $start = Get-Date
    try {
        $p = Start-Process -FilePath $file -ArgumentList $argString -WorkingDirectory $dir `
             -RedirectStandardOutput $o -RedirectStandardError $e -NoNewWindow -PassThru
        $null = $p.Handle
        if (-not $p.WaitForExit($limit * 1000)) {
            Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
            Log ('Stopped it after ' + $limit + ' s.')
        }
        $code = $p.ExitCode
    } catch {
        Log ('Could not start it: ' + $_.Exception.Message)
        return 999
    }
    $secs = [math]::Round(((Get-Date) - $start).TotalSeconds, 1)
    $out = Get-Content $o -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    $err = Get-Content $e -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    if ($out) { Log $out.TrimEnd() }
    if ($err) {
        if ($tailErr -gt 0) {
            $lines = $err -split "[`r`n]+" | Where-Object { $_.Trim() -ne '' }
            $err = ($lines | Select-Object -Last $tailErr) -join "`n"
        }
        Log $err.TrimEnd()
    }
    Log ('(exit code ' + $code + ', ' + $secs + ' s)')
    return $code
}
function Sha256([string]$path) { (Get-FileHash -Path $path -Algorithm SHA256).Hash.ToLower() }

$py = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'

function PrepLab([string]$nn) {
    # Unzip the owner's lab zip into ai-stack and make the lab's own virtual environment.
    $name = 'engineering-stack-lab-part-' + $nn
    $zip = Join-Path $Zips ($name + '.zip')
    $lab = Join-Path $Root $name
    Log ('Lab zip: ' + $zip + ', ' + (Get-Item $zip).Length + ' bytes, SHA-256 ' + (Sha256 $zip))
    Expand-Archive -Path $zip -DestinationPath $Root -Force
    $vpy = Join-Path $lab '.venv\Scripts\python.exe'
    if (-not (Test-Path $vpy)) { Run $py '-m venv .venv' ('p' + $nn + '-venv') $lab | Out-Null }
    Run $vpy '--version' ('p' + $nn + '-python-version') $lab | Out-Null
    return $lab
}
function CoreTests([string]$nn, [string]$lab) {
    $vpy = Join-Path $lab '.venv\Scripts\python.exe'
    Run $vpy 'run_lab.py' ('p' + $nn + '-r1-run-lab') $lab | Out-Null
    Run $vpy 'mutation_check.py' ('p' + $nn + '-r2-mutation-check') $lab | Out-Null
}
function PipInstall([string]$nn, [string]$lab, [string]$pipArgs, [string]$tag) {
    $vpy = Join-Path $lab '.venv\Scripts\python.exe'
    $code = Run $vpy ('-m pip install --disable-pip-version-check ' + $pipArgs) ('p' + $nn + '-' + $tag) $lab 8 3600
    $f = Join-Path $Work ('p' + $nn + '-' + $tag + '.out.txt')
    if (Test-Path $f) {
        $ok = Select-String -Path $f -Pattern '^Successfully installed' | Select-Object -Last 1
        if ($ok) { Log ('pip: ' + $ok.Line) }
    }
    return $code
}

$env:HF_HUB_DISABLE_TELEMETRY = '1'
$env:DO_NOT_TRACK = '1'
function Lab([string]$nn) { Join-Path $Root ('engineering-stack-lab-part-' + $nn) }
function VPy([string]$nn) { Join-Path (Lab $nn) '.venv\Scripts\python.exe' }
function FreeState {
    try {
        $os = Get-CimInstance Win32_OperatingSystem
        Log ('Free memory: ' + [math]::Round($os.FreePhysicalMemory / 1MB, 2) + ' GB; free disk on C: ' + [math]::Round((Get-PSDrive C).Free / 1GB, 1) + ' GB')
    } catch { }
}

Remove-Item $Log -ErrorAction SilentlyContinue
Step 'This computer'
FreeState
if ((Get-PSDrive C).Free / 1GB -lt 8) { Log 'Less than 8 GB free on C:, so the heavy tests were not started.'; exit 1 }

# ---------------------------------------------------------------- R2 again, default encoding
Step 'R2 again for Parts 03 to 10 and 12, with Python''s default Windows encoding'
# Script A set PYTHONIOENCODING=utf-8 so output going to a file couldn't crash. The mutation
# checks pass that setting on to the run_lab.py copies they start, but decode their output with
# Windows' default code page, which is not how a reader's console runs them. This repeats R2
# without the setting, as a reader would get it.
$saved = $env:PYTHONIOENCODING
Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
foreach ($nn in '03', '04', '05', '06', '07', '08', '09', '10', '12') {
    Log ('Part ' + $nn + ':')
    Run (VPy $nn) 'mutation_check.py' ('p' + $nn + '-r2-default-encoding') (Lab $nn) 6 | Out-Null
}
$env:PYTHONIOENCODING = $saved

# ---------------------------------------------------------------- Part 12 R3
Step 'Part 12 R3: a small LoRA run on the processor'
try {
    $lab = Lab '12'; $vpy = VPy '12'
    PipInstall '12' $lab 'torch==2.14.1 transformers==5.20.2 peft==0.21.2' 'r3-pip' | Out-Null
    Run $vpy '-m pip show torch transformers peft' 'p12-r3-versions' $lab | Out-Null
    FreeState
    Run $vpy 'reader_lora.py --steps 24' 'p12-r3-lora' $lab 0 3600 | Out-Null
    $out = Join-Path $lab 'lora-out'
    if (Test-Path $out) {
        Get-ChildItem $out -File | ForEach-Object { Log ('lora-out\' + $_.Name + ': ' + $_.Length + ' bytes') }
    }
} catch { Log ('Part 12 R3 stopped: ' + $_.Exception.Message) }

# ---------------------------------------------------------------- Part 05 R4
Step 'Part 05 R4: a real embedding model and reranker'
try {
    $lab = Lab '05'; $vpy = VPy '05'
    PipInstall '05' $lab '-r requirements-real.txt' 'r4-pip' | Out-Null
    Run $vpy '-m pip show torch sentence-transformers' 'p05-r4-versions' $lab | Out-Null
    Run $vpy 'real_models.py' 'p05-r4-real-models' $lab 0 3600 | Out-Null
} catch { Log ('Part 05 R4 stopped: ' + $_.Exception.Message) }

# ---------------------------------------------------------------- Part 10 R4
Step 'Part 10 R4: Presidio with spaCy en_core_web_lg'
try {
    $lab = Lab '10'; $vpy = VPy '10'
    Run $vpy '-m spacy download en_core_web_lg' 'p10-r4-spacy-download' $lab 8 3600 | Out-Null
    Run $vpy 'reader_presidio.py' 'p10-r4-reader-presidio' $lab 0 1800 | Out-Null
} catch { Log ('Part 10 R4 stopped: ' + $_.Exception.Message) }

# ---------------------------------------------------------------- Part 10 R5
Step 'Part 10 R5: garak 0.17.0 in its own virtual environment'
try {
    $lab = Lab '10'
    $gpy = Join-Path $lab '.venv-garak\Scripts\python.exe'
    if (-not (Test-Path $gpy)) { Run $py '-m venv .venv-garak' 'p10-r5-venv' $lab | Out-Null }
    $code = Run $gpy '-m pip install --disable-pip-version-check garak==0.17.0' 'p10-r5-pip' $lab 8 3600
    Log ('pip exit code ' + $code)
    Run $gpy '-m pip show garak torch' 'p10-r5-versions' $lab | Out-Null
    Run $gpy '-m garak --list_probes' 'p10-r5-list-probes' $lab 20 1800 | Out-Null
    Run $gpy '-m garak --target_type test.Blank --spec probes.test.Test' 'p10-r5-self-test' $lab 30 1800 | Out-Null
} catch { Log ('Part 10 R5 stopped: ' + $_.Exception.Message) }

# ---------------------------------------------------------------- Part 04 R4
Step 'Part 04 R4: the position test on a local model in Ollama'
try {
    $lab = Lab '04'; $vpy = VPy '04'
    $ollamaDir = Join-Path $env:LOCALAPPDATA 'Programs\Ollama'
    $ollama = Join-Path $ollamaDir 'ollama.exe'
    $api = 'http://127.0.0.1:11434'
    function OllamaUp { try { Invoke-RestMethod -Uri ($api + '/api/version') -TimeoutSec 3 } catch { $null } }
    $v = OllamaUp
    if (-not $v) {
        Log 'Ollama is not answering; starting the Ollama app.'
        Start-Process -FilePath (Join-Path $ollamaDir 'ollama app.exe')
        for ($i = 0; $i -lt 45 -and -not $v; $i++) { Start-Sleep -Seconds 2; $v = OllamaUp }
    }
    if (-not $v) { throw ('Ollama is not answering at ' + $api) }
    Log ('Ollama server version: ' + $v.version)
    Log ('OLLAMA_NO_CLOUD for this user: ' + [Environment]::GetEnvironmentVariable('OLLAMA_NO_CLOUD', 'User'))
    Run $ollama 'list' 'p04-r4-ollama-list' | Out-Null
    FreeState
    Run $vpy 'placement_test.py --ollama qwen3:1.7b --docs 200 --num-ctx 16384 --trials 10' 'p04-r4-placement' $lab 0 18000 | Out-Null
    Run $ollama 'ps' 'p04-r4-ollama-ps' | Out-Null
    Run $ollama 'stop qwen3:1.7b' 'p04-r4-ollama-stop' | Out-Null
} catch { Log ('Part 04 R4 stopped: ' + $_.Exception.Message) }

Step 'FINISHED'
FreeState
Log 'Everything installed here sits inside the lab folders in Downloads\ai-stack (their .venv folders), plus spaCy and Hugging Face downloads in those environments and in the Hugging Face cache in your user folder; delete a lab folder to remove its packages.'
