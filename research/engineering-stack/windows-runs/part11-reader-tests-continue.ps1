# Engineering Stack, Part 11: reader tests R3 and R4, continued.
# Run by Claude on October 19, 2026, with the owner's go-ahead. The first runner
# (part11-reader-tests.ps1) finished R1, R2 and the Ollama install, then waited on
# the Ollama app that the installer starts. This script carries on from there and
# adds to the same log.
# Downloads come only from official sources, and each is checked against its
# published SHA-256 before use. Everything is written to part11-reader-tests.log.
#   R3: Ollama v0.40.6 (already installed), OLLAMA_NO_CLOUD=1, qwen3:1.7b, reader_local.py.
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
function Run([string]$file, [string]$argString, [string]$name, [string]$dir = $Work, [int]$tailErr = 0, [int]$limit = 1800) {
    # Waits for this process only. Windows PowerShell's "Start-Process -Wait" also waits
    # for every process it starts, so the first runner stopped at Ollama's installer,
    # which leaves the Ollama app running.
    $o = Join-Path $Work ($name + '.out.txt')
    $e = Join-Path $Work ($name + '.err.txt')
    Log ('> ' + $file + ' ' + $argString)
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
function FreeMemory {
    try {
        $os = Get-CimInstance Win32_OperatingSystem
        Log ('Free memory now: ' + [math]::Round($os.FreePhysicalMemory / 1MB, 2) + ' GB')
    } catch { }
}
function Sha256([string]$path) { (Get-FileHash -Path $path -Algorithm SHA256).Hash.ToLower() }
function Download([string]$url, [string]$dest, [string]$name) {
    $code = Run 'curl.exe' ('-L --fail -sS -o "' + $dest + '" "' + $url + '"') $name $Work 0 3600
    if (Test-Path $dest) { Log ('Downloaded ' + (Get-Item $dest).Length + ' bytes to ' + $dest) }
    return $code
}

$vpy = Join-Path $Lab '.venv\Scripts\python.exe'

# ---------------------------------------------------------------- R3
Step 'R3, continued: the first runner waited on the Ollama app the installer starts; carrying on'
$ollamaDir = Join-Path $env:LOCALAPPDATA 'Programs\Ollama'
$ollama = Join-Path $ollamaDir 'ollama.exe'
$api = 'http://127.0.0.1:11434'
function OllamaUp { try { Invoke-RestMethod -Uri ($api + '/api/version') -TimeoutSec 3 } catch { $null } }
try {
    $env:OLLAMA_NO_CLOUD = '1'
    Log ('OLLAMA_NO_CLOUD for this user: ' + [Environment]::GetEnvironmentVariable('OLLAMA_NO_CLOUD', 'User'))
    if (-not (Test-Path $ollama)) { throw ('Ollama is not installed at ' + $ollama) }
    Log ('Ollama installed at ' + $ollama)
    Get-Process -Name 'ollama*' -ErrorAction SilentlyContinue | ForEach-Object { Log ('Running: ' + $_.ProcessName + ' (process ' + $_.Id + ')') }

    $v = OllamaUp
    for ($i = 0; $i -lt 15 -and -not $v; $i++) { Start-Sleep -Seconds 2; $v = OllamaUp }
    if (-not $v) {
        Log 'The server did not answer within 30 s; starting the Ollama app.'
        Start-Process -FilePath (Join-Path $ollamaDir 'ollama app.exe')
        for ($i = 0; $i -lt 45 -and -not $v; $i++) { Start-Sleep -Seconds 2; $v = OllamaUp }
    }
    if (-not $v) { throw ('Ollama is not answering at ' + $api) }
    Log ('Ollama server version: ' + $v.version)
    Run $ollama '--version' 'ollama-version' | Out-Null

    $slog = Join-Path $env:LOCALAPPDATA 'Ollama\server.log'
    if (Test-Path $slog) {
        Log 'server.log lines about cloud, compute and GPUs:'
        Select-String -Path $slog -Pattern 'cloud|inference compute|no compatible GPU|library=|total_vram' |
            Select-Object -Last 12 | ForEach-Object { Log ('  ' + $_.Line) }
    }

    Run $ollama 'pull qwen3:1.7b' 'ollama-pull' $Work 6 3600 | Out-Null
    Run $ollama 'list' 'ollama-list' | Out-Null
    try {
        $tags = Invoke-RestMethod -Uri ($api + '/api/tags') -TimeoutSec 10
        foreach ($m in $tags.models) { Log ('Model ' + $m.name + ': ' + $m.size + ' bytes, digest ' + $m.digest) }
    } catch { Log 'Could not read /api/tags.' }

    if (Test-Path $vpy) {
        FreeMemory
        Run $vpy 'reader_local.py --model qwen3:1.7b --bandwidth 41.6 --runs 5' 'r3-reader-local' $Lab | Out-Null
        Run $vpy 'reader_local.py --model qwen3:1.7b --bandwidth 21.3 --runs 5' 'r3-reader-local-single-channel' $Lab | Out-Null
    } else { Log 'The lab environment is missing; skipped reader_local.py.' }
    Run $ollama 'ps' 'ollama-ps' | Out-Null
    Run $ollama 'stop qwen3:1.7b' 'ollama-stop' | Out-Null
} catch { Log ('R3 stopped: ' + $_.Exception.Message) }

# ---------------------------------------------------------------- R4
Step 'R4: llama.cpp and Qwen3-4B'
try {
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) { throw 'winget is not available on this computer.' }
    Run $winget.Source '--version' 'winget-version' | Out-Null
    Run $winget.Source 'install llama.cpp --accept-source-agreements --accept-package-agreements' 'winget-install' $Work 25 1800 | Out-Null

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
    FreeMemory
    Run $bench ('-m "' + $gguf + '"') 'r4-bench-default' | Out-Null
    FreeMemory
    Run $bench ('-m "' + $gguf + '" -dev none') 'r4-bench-cpu-only' | Out-Null
} catch { Log ('R4 stopped: ' + $_.Exception.Message) }

Step 'FINISHED'
Log 'Ollama, its model, llama.cpp and the model file stay installed. Section 7.5 of Part 11 says how to remove them.'
