# Engineering Stack, Part 11: reader tests R1 to R4 on this computer.
# Run by Claude on October 19, 2026, with the owner's go-ahead.
# Downloads come only from official sources, and each is checked against its
# published SHA-256 before use. Everything is written to part11-reader-tests.log.
#   R1, R2: the lab's checks and mutation check (no downloads).
#   R3: Ollama v0.40.6 from its GitHub release, OLLAMA_NO_CLOUD=1, qwen3:1.7b, reader_local.py.
#   R4: llama.cpp from winget, Qwen's own Qwen3-4B Q4_K_M GGUF, llama-bench.

$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$Root = Join-Path $env:USERPROFILE 'Downloads\ai-stack'
$Work = Join-Path $Root 'part11-reader-tests'
$Log  = Join-Path $Root 'part11-reader-tests.log'
$Lab  = Join-Path $Root 'engineering-stack-lab-part-11'
New-Item -ItemType Directory -Force -Path $Work | Out-Null

function Log([string]$text) {
    Add-Content -Path $Log -Value $text -Encoding UTF8
    Write-Host $text
}
function Step([string]$name) {
    Log ''
    Log ('==== ' + $name + '  [' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + ']')
}
function Run([string]$file, [string]$argString, [string]$name, [string]$dir = $Work, [int]$tailErr = 0) {
    $o = Join-Path $Work ($name + '.out.txt')
    $e = Join-Path $Work ($name + '.err.txt')
    Log ('> ' + $file + ' ' + $argString)
    $start = Get-Date
    try {
        $p = Start-Process -FilePath $file -ArgumentList $argString -WorkingDirectory $dir `
             -RedirectStandardOutput $o -RedirectStandardError $e -NoNewWindow -Wait -PassThru
        $code = $p.ExitCode
    } catch {
        Log ('Could not start it: ' + $_.Exception.Message)
        return 999
    }
    $secs = [math]::Round(((Get-Date) - $start).TotalSeconds, 1)
    $out = Get-Content $o -Raw -ErrorAction SilentlyContinue
    $err = Get-Content $e -Raw -ErrorAction SilentlyContinue
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
function Download([string]$url, [string]$dest, [string]$name) {
    $code = Run 'curl.exe' ('-L --fail -sS -o "' + $dest + '" "' + $url + '"') $name
    if (Test-Path $dest) { Log ('Downloaded ' + (Get-Item $dest).Length + ' bytes to ' + $dest) }
    return $code
}

Remove-Item $Log -ErrorAction SilentlyContinue
Step 'This computer'
try {
    $os = Get-CimInstance Win32_OperatingSystem
    $cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
    Log ('Windows: ' + $os.Caption + ' ' + $os.Version)
    Log ('PowerShell: ' + $PSVersionTable.PSVersion.ToString())
    Log ('Processor: ' + $cpu.Name.Trim() + ', ' + $cpu.NumberOfCores + ' cores, ' + $cpu.NumberOfLogicalProcessors + ' threads')
    Log ('Memory: ' + [math]::Round($os.TotalVisibleMemorySize / 1MB, 2) + ' GB total, ' + [math]::Round($os.FreePhysicalMemory / 1MB, 2) + ' GB free now')
    foreach ($m in Get-CimInstance Win32_PhysicalMemory) {
        Log ('Memory module: ' + [math]::Round($m.Capacity / 1GB, 1) + ' GB in ' + $m.DeviceLocator + ', rated ' + $m.Speed + ' MT/s, running at ' + $m.ConfiguredClockSpeed + ' MT/s')
    }
    foreach ($g in Get-CimInstance Win32_VideoController) { Log ('Graphics: ' + $g.Name + ', driver ' + $g.DriverVersion) }
    $disk = Get-PSDrive C
    Log ('Free disk on C: ' + [math]::Round($disk.Free / 1GB, 1) + ' GB')
} catch { Log ('Could not read the hardware details: ' + $_.Exception.Message) }

# ---------------------------------------------------------------- R1 and R2
Step 'R1 and R2: the lab on Windows'
$py = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
if (-not (Test-Path $py)) {
    $cmd = Get-Command py -ErrorAction SilentlyContinue
    if ($cmd) { $py = $cmd.Source } else { $py = $null }
}
$vpy = Join-Path $Lab '.venv\Scripts\python.exe'
try {
    $zip = Join-Path $Root 'engineering-stack-lab-part-11.zip'
    Log ('Lab zip SHA-256: ' + (Sha256 $zip))
    Expand-Archive -Path $zip -DestinationPath $Root -Force
    Log ('Unzipped to ' + $Lab + ': ' + ((Get-ChildItem $Lab -File | ForEach-Object Name) -join ', '))
    if ($py) {
        if ($py -like '*py.exe') { Run $py '-3.13 -m venv .venv' 'venv' $Lab | Out-Null }
        else { Run $py '-m venv .venv' 'venv' $Lab | Out-Null }
        Run $vpy '--version' 'python-version' $Lab | Out-Null
        Run $vpy 'run_lab.py' 'r1-run-lab' $Lab | Out-Null
        Run $vpy 'mutation_check.py' 'r2-mutation-check' $Lab | Out-Null
        Run $vpy 'reader_local.py --self-test' 'reader-self-test' $Lab | Out-Null
    } else { Log 'Python 3.13 not found; skipped R1 and R2.' }
} catch { Log ('R1 and R2 stopped: ' + $_.Exception.Message) }

# ---------------------------------------------------------------- R3
Step 'R3: Ollama and qwen3:1.7b'
$ollamaDir = Join-Path $env:LOCALAPPDATA 'Programs\Ollama'
$ollama = Join-Path $ollamaDir 'ollama.exe'
$api = 'http://127.0.0.1:11434'
function OllamaUp { try { Invoke-RestMethod -Uri ($api + '/api/version') -TimeoutSec 3 } catch { $null } }
try {
    # Section 7.5, step 2: the user variable, set before Ollama first starts.
    [Environment]::SetEnvironmentVariable('OLLAMA_NO_CLOUD', '1', 'User')
    $env:OLLAMA_NO_CLOUD = '1'
    Log ('OLLAMA_NO_CLOUD for this user: ' + [Environment]::GetEnvironmentVariable('OLLAMA_NO_CLOUD', 'User'))

    if (Test-Path $ollama) {
        Log ('Ollama is already installed at ' + $ollama)
    } else {
        $rel = 'https://github.com/ollama/ollama/releases/download/v0.40.6'
        $setup = Join-Path $Work 'OllamaSetup.exe'
        $sums = Join-Path $Work 'ollama-sha256sum.txt'
        Download ($rel + '/sha256sum.txt') $sums 'dl-ollama-sums' | Out-Null
        Download ($rel + '/OllamaSetup.exe') $setup 'dl-ollama-setup' | Out-Null
        $want = ''
        foreach ($line in Get-Content $sums) {
            if ($line -match '^([0-9a-fA-F]{64})\s+\*?\.?/?OllamaSetup\.exe\s*$') { $want = $Matches[1].ToLower() }
        }
        $page = '933794ee1d670137f5116c9de7fc7db092fa97c6b823aba848ddb8a7ea030828'
        $got = Sha256 $setup
        Log ('OllamaSetup.exe SHA-256: ' + $got)
        Log ('sha256sum.txt says:      ' + $want)
        Log ('release page says:       ' + $page)
        if (($got -ne $want) -or ($got -ne $page)) { throw 'The installer does not match its published SHA-256; not installing it.' }
        Log 'Checksum matches. Installing for this user only (no administrator rights).'
        Run $setup '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART' 'ollama-install' | Out-Null
    }

    $v = $null
    for ($i = 0; $i -lt 30 -and -not $v; $i++) { Start-Sleep -Seconds 2; $v = OllamaUp }
    if (-not $v) {
        Log 'The server did not answer within 60 s; starting the Ollama app.'
        Start-Process -FilePath (Join-Path $ollamaDir 'ollama app.exe')
        for ($i = 0; $i -lt 45 -and -not $v; $i++) { Start-Sleep -Seconds 2; $v = OllamaUp }
    }
    if (-not $v) { throw ('Ollama is not answering at ' + $api) }
    Log ('Ollama server version: ' + $v.version)

    $slog = Join-Path $env:LOCALAPPDATA 'Ollama\server.log'
    if (Test-Path $slog) {
        Log 'server.log lines about cloud, compute and GPUs:'
        Select-String -Path $slog -Pattern 'cloud|inference compute|no compatible GPU|library=|total_vram' |
            Select-Object -Last 12 | ForEach-Object { Log ('  ' + $_.Line) }
    }

    Run $ollama 'pull qwen3:1.7b' 'ollama-pull' $Work 6 | Out-Null
    Run $ollama 'list' 'ollama-list' | Out-Null
    try {
        $tags = Invoke-RestMethod -Uri ($api + '/api/tags') -TimeoutSec 10
        foreach ($m in $tags.models) { Log ('Model ' + $m.name + ': ' + $m.size + ' bytes, digest ' + $m.digest) }
    } catch { Log 'Could not read /api/tags.' }

    if (Test-Path $vpy) {
        Run $vpy 'reader_local.py --model qwen3:1.7b --bandwidth 41.6' 'r3-reader-local' $Lab | Out-Null
    } else { Log 'The lab environment is missing; skipped reader_local.py.' }
    Run $ollama 'ps' 'ollama-ps' | Out-Null
} catch { Log ('R3 stopped: ' + $_.Exception.Message) }

# ---------------------------------------------------------------- R4
Step 'R4: llama.cpp and Qwen3-4B'
try {
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) { throw 'winget is not available on this computer.' }
    Run $winget.Source '--version' 'winget-version' | Out-Null
    Run $winget.Source 'install llama.cpp --accept-source-agreements --accept-package-agreements' 'winget-install' $Work 25 | Out-Null

    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
    $bench = $null
    $c = Get-Command llama-bench -ErrorAction SilentlyContinue
    if ($c) { $bench = $c.Source }
    if (-not $bench) {
        $found = Get-ChildItem (Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet') -Recurse -Filter 'llama-bench.exe' -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) { $bench = $found.FullName }
    }
    if (-not $bench) { throw 'llama-bench was not found after the install.' }
    Log ('llama-bench: ' + $bench)

    $name = 'Qwen3-4B-Q4_K_M.gguf'
    $gguf = Join-Path $env:USERPROFILE ('Downloads\' + $name)
    $tree = Invoke-RestMethod -Uri 'https://huggingface.co/api/models/Qwen/Qwen3-4B-GGUF/tree/main' -TimeoutSec 30
    $entry = $tree | Where-Object { $_.path -eq $name } | Select-Object -First 1
    $want = $entry.lfs.oid.ToLower()
    Log ('Hugging Face lists ' + $name + ': ' + $entry.size + ' bytes, SHA-256 ' + $want)
    if (-not ((Test-Path $gguf) -and ((Sha256 $gguf) -eq $want))) {
        Download ('https://huggingface.co/Qwen/Qwen3-4B-GGUF/resolve/main/' + $name) $gguf 'dl-gguf' | Out-Null
    }
    $got = Sha256 $gguf
    Log ('Downloaded file SHA-256: ' + $got)
    if ($got -ne $want) { throw 'The model file does not match its published SHA-256; not using it.' }
    Log 'Checksum matches.'

    Run $bench '--list-devices' 'bench-devices' | Out-Null
    Run $bench ('-m "' + $gguf + '"') 'r4-bench-default' | Out-Null
    Run $bench ('-m "' + $gguf + '" -dev none') 'r4-bench-cpu-only' | Out-Null
} catch { Log ('R4 stopped: ' + $_.Exception.Message) }

Step 'FINISHED'
Log 'Ollama, its model, llama.cpp and the model file stay installed. Section 7.5 of Part 11 says how to remove them.'
