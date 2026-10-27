# Engineering Stack: quick reader tests on this computer (October 20, 2026).
# Run by Claude with the owner's go-ahead. No large downloads: the only installs are
# each part's small cross-check packages from PyPI, into that lab's own virtual environment.
#   Parts 03 to 10 and 12: R1 (run_lab.py) and R2 (mutation_check.py).
#   R3 cross-checks: 03 Pydantic (hash-pinned), 04 tiktoken (hash-pinned; fetches o200k_base
#   from OpenAI's public blob store on first use), 05 bm25s and ir_measures, 06 networkx,
#   07 mcp 2.3.0, 08 openai-agents 0.23.1, 09 LangGraph 1.2.15, 10 Presidio and python-stdnum.
#   Part 09 R4: pause in one process, approve in another.
# Everything is written to stack-reader-tests-a.log in this folder.

$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$Root = Join-Path $env:USERPROFILE 'Downloads\ai-stack'
$Zips = Join-Path $env:USERPROFILE 'Downloads'
$Work = Join-Path $Root 'stack-reader-tests'
$Log  = Join-Path $Root 'stack-reader-tests-a.log'
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

Remove-Item $Log -ErrorAction SilentlyContinue
Step 'This computer'
try {
    $os = Get-CimInstance Win32_OperatingSystem
    Log ('Windows: ' + $os.Caption + ' ' + $os.Version + '; PowerShell ' + $PSVersionTable.PSVersion.ToString())
    Log ('Memory: ' + [math]::Round($os.TotalVisibleMemorySize / 1MB, 2) + ' GB total, ' + [math]::Round($os.FreePhysicalMemory / 1MB, 2) + ' GB free now')
    Log ('Free disk on C: ' + [math]::Round((Get-PSDrive C).Free / 1GB, 1) + ' GB')
    Log ('Python: ' + $py + ' exists: ' + (Test-Path $py))
    foreach ($tool in 'docker', 'claude', 'node') {
        $c = Get-Command $tool -ErrorAction SilentlyContinue
        if ($c) { Log ($tool + ' found: ' + $c.Source) } else { Log ($tool + ' not found') }
    }
} catch { Log ('Could not read the computer details: ' + $_.Exception.Message) }

# ---------------------------------------------------------------- Part 03
Step 'Part 03: R1, R2, R3 (Pydantic)'
try {
    $lab = PrepLab '03'
    CoreTests '03' $lab
    PipInstall '03' $lab '--require-hashes -r requirements-optional.txt' 'r3-pip' | Out-Null
    Run (Join-Path $lab '.venv\Scripts\python.exe') 'run_lab.py --with-pydantic' 'p03-r3-run-lab-pydantic' $lab | Out-Null
} catch { Log ('Part 03 stopped: ' + $_.Exception.Message) }

# ---------------------------------------------------------------- Part 04
Step 'Part 04: R1, R2, R3 (tiktoken)'
try {
    $lab = PrepLab '04'
    CoreTests '04' $lab
    PipInstall '04' $lab '--require-hashes -r requirements-optional.txt' 'r3-pip' | Out-Null
    Run (Join-Path $lab '.venv\Scripts\python.exe') 'run_lab.py --with-tiktoken' 'p04-r3-run-lab-tiktoken' $lab | Out-Null
} catch { Log ('Part 04 stopped: ' + $_.Exception.Message) }

# ---------------------------------------------------------------- Part 05
Step 'Part 05: R1, R2, R3 (bm25s, rank_bm25, ir_measures)'
try {
    $lab = PrepLab '05'
    CoreTests '05' $lab
    PipInstall '05' $lab '-r requirements-crosscheck.txt' 'r3-pip' | Out-Null
    Run (Join-Path $lab '.venv\Scripts\python.exe') 'crosscheck.py' 'p05-r3-crosscheck' $lab | Out-Null
} catch { Log ('Part 05 stopped: ' + $_.Exception.Message) }

# ---------------------------------------------------------------- Part 06
Step 'Part 06: R1, R2, R3 (networkx)'
try {
    $lab = PrepLab '06'
    CoreTests '06' $lab
    PipInstall '06' $lab '-r requirements-crosscheck.txt' 'r3-pip' | Out-Null
    Run (Join-Path $lab '.venv\Scripts\python.exe') 'crosscheck.py' 'p06-r3-crosscheck' $lab | Out-Null
} catch { Log ('Part 06 stopped: ' + $_.Exception.Message) }

# ---------------------------------------------------------------- Part 07
Step 'Part 07: R1, R2, R3 (mcp 2.3.0)'
try {
    $lab = PrepLab '07'
    CoreTests '07' $lab
    PipInstall '07' $lab '-r requirements-crosscheck.txt' 'r3-pip' | Out-Null
    Run (Join-Path $lab '.venv\Scripts\python.exe') 'crosscheck.py' 'p07-r3-crosscheck' $lab | Out-Null
} catch { Log ('Part 07 stopped: ' + $_.Exception.Message) }

# ---------------------------------------------------------------- Part 08
Step 'Part 08: R1, R2, R3 (openai-agents 0.23.1, fake model, tracing off)'
try {
    $lab = PrepLab '08'
    CoreTests '08' $lab
    PipInstall '08' $lab '-r requirements-crosscheck.txt' 'r3-pip' | Out-Null
    Run (Join-Path $lab '.venv\Scripts\python.exe') 'crosscheck.py' 'p08-r3-crosscheck' $lab | Out-Null
} catch { Log ('Part 08 stopped: ' + $_.Exception.Message) }

# ---------------------------------------------------------------- Part 09
Step 'Part 09: R1, R2, R3 (LangGraph 1.2.15), R4 (pause in one process, approve in another)'
try {
    $lab = PrepLab '09'
    $vpy = Join-Path $lab '.venv\Scripts\python.exe'
    CoreTests '09' $lab
    PipInstall '09' $lab '-r requirements-crosscheck.txt' 'r3-pip' | Out-Null
    Run $vpy 'crosscheck.py' 'p09-r3-crosscheck' $lab | Out-Null
    $cpdir = Join-Path $lab 'my-checkpoints'
    if (Test-Path $cpdir) { Rename-Item $cpdir ('my-checkpoints-old-' + (Get-Date -Format 'HHmmss')) }
    Run $vpy '-c "from examples import *; from workflow import *; f = build_refund_workflow(FakePaymentService(), {}); cp = f.run(''A17'', FileCheckpointer(''my-checkpoints''), state={''order'': ''A17'', ''amount'': 250, ''request'': ''Refund please''}); print(cp[''status''], cp[''pending''][''value''])"' 'p09-r4-pause' $lab | Out-Null
    $cpfile = Join-Path $cpdir 'A17.json'
    if (Test-Path $cpfile) { Log ('Checkpoint left by the first process: ' + $cpfile + ', ' + (Get-Item $cpfile).Length + ' bytes') }
    Run $vpy '-c "from examples import *; from workflow import *; f = build_refund_workflow(FakePaymentService(), {}); cp = f.run(''A17'', FileCheckpointer(''my-checkpoints''), resume={''decision'': ''approve''}); print(cp[''status''], cp[''state''][''refund_id''])"' 'p09-r4-approve' $lab | Out-Null
    # This run made the folder; remove it as Section 8, step 3 says.
    Remove-Item -Recurse -Force $cpdir -ErrorAction SilentlyContinue
    Log ('my-checkpoints removed: ' + (-not (Test-Path $cpdir)))
} catch { Log ('Part 09 stopped: ' + $_.Exception.Message) }

# ---------------------------------------------------------------- Part 10
Step 'Part 10: R1, R2, R3 (Presidio and python-stdnum, network blocked by the script)'
try {
    $lab = PrepLab '10'
    CoreTests '10' $lab
    PipInstall '10' $lab '-r requirements-crosscheck.txt' 'r3-pip' | Out-Null
    Run (Join-Path $lab '.venv\Scripts\python.exe') 'crosscheck.py' 'p10-r3-crosscheck' $lab | Out-Null
} catch { Log ('Part 10 stopped: ' + $_.Exception.Message) }

# ---------------------------------------------------------------- Part 12
Step 'Part 12: R1, R2, and the R3 plan (no downloads)'
try {
    $lab = PrepLab '12'
    $vpy = Join-Path $lab '.venv\Scripts\python.exe'
    CoreTests '12' $lab
    Run $vpy 'reader_lora.py --plan' 'p12-r3-plan' $lab | Out-Null
} catch { Log ('Part 12 stopped: ' + $_.Exception.Message) }

Step 'FINISHED'
Log ('Free disk on C: ' + [math]::Round((Get-PSDrive C).Free / 1GB, 1) + ' GB')
Log 'Each lab folder and its .venv stay in Downloads\ai-stack; delete a folder to remove it.'
