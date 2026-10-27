# Engineering Stack, Part 11: reader test R4, second try.
# Run by Claude on October 19, 2026, with the owner's go-ahead. The first R4 download
# of the model file stopped halfway (curl error 56, the server closed the connection),
# so the checksum didn't match and R4 stopped. This script resumes the download
# where it stopped, checks the SHA-256 again, and runs llama-bench. It adds to the same log.
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

# ---------------------------------------------------------------- R4
Step 'R4, second try: resume the model download'
try {
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) { throw 'winget is not available on this computer.' }
    Run $winget.Source '--version' 'winget-version' | Out-Null

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
    $url = 'https://huggingface.co/Qwen/Qwen3-4B-GGUF/resolve/main/' + $name
    for ($try = 1; $try -le 6; $try++) {
        $have = 0
        if (Test-Path $gguf) { $have = (Get-Item $gguf).Length }
        if ($have -ge $entry.size) { break }
        Log ('Download try ' + $try + ': resuming at byte ' + $have + ' of ' + $entry.size)
        Run 'curl.exe' ('-L --fail -sS -C - -o "' + $gguf + '" "' + $url + '"') ('dl-gguf-' + $try) $Work 0 3600 | Out-Null
    }
    Log ('File size now: ' + (Get-Item $gguf).Length + ' bytes')
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
