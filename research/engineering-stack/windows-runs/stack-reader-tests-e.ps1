# Engineering Stack: Part 04 R4, a variant with thinking off (October 20, 2026).
# Run by Claude with the owner's go-ahead. Script D's run at 50 documents still stopped at the
# lab's 300-second limit per call, because qwen3:1.7b thinks before it answers. This runs the
# lab's own test through placement_think_off.py: thinking off, 900 seconds per call, each call timed.
# Nothing is downloaded or installed; it talks only to the Ollama server on this computer.
# Everything is written to stack-reader-tests-e.log in this folder.

$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$Root = Join-Path $env:USERPROFILE 'Downloads\ai-stack'
$Work = Join-Path $Root 'stack-reader-tests'
$Log  = Join-Path $Root 'stack-reader-tests-e.log'
New-Item -ItemType Directory -Force -Path $Work | Out-Null
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:HF_HUB_DISABLE_TELEMETRY = '1'
$env:DO_NOT_TRACK = '1'

function Log([string]$text) {
    Add-Content -Path $Log -Value $text -Encoding UTF8
    Write-Host $text
}
function Step([string]$name) {
    Log ''
    Log ('==== ' + $name + '  [' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + ']')
}
function Run([string]$file, [string]$argString, [string]$name, [string]$dir = $Work, [int]$limit = 600) {
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
    if ($err) { Log $err.TrimEnd() }
    Log ('(exit code ' + $code + ', ' + $secs + ' s)')
    return $code
}
function Lab([string]$nn) { Join-Path $Root ('engineering-stack-lab-part-' + $nn) }
function VPy([string]$nn) { Join-Path (Lab $nn) '.venv\Scripts\python.exe' }
function SizeOf([string]$path) {
    $sum = (Get-ChildItem -Path $path -Recurse -File -Force -ErrorAction SilentlyContinue |
            Measure-Object -Property Length -Sum).Sum
    if (-not $sum) { $sum = 0 }
    return [math]::Round($sum / 1MB, 1)
}
function ListFolder([string]$path) {
    if (-not (Test-Path $path)) { Log ($path + ': not there'); return }
    Log ($path + ': ' + (SizeOf $path) + ' MB in all')
    Get-ChildItem -Path $path -Force -ErrorAction SilentlyContinue | ForEach-Object {
        if ($_.PSIsContainer) { Log ('  ' + $_.Name + '\  ' + (SizeOf $_.FullName) + ' MB') }
        else { Log ('  ' + $_.Name + '  ' + [math]::Round($_.Length / 1KB, 1) + ' KB') }
    }
}

function FreeState {
    $os = Get-CimInstance Win32_OperatingSystem
    Log ('Free memory: ' + [math]::Round($os.FreePhysicalMemory / 1MB, 2) + ' GB')
}
Step 'Part 04 R4 variant: thinking off, 50 documents, num_ctx 4096, 10 trials'
try {
    $lab = Lab '04'; $vpy = VPy '04'
    $variant = Join-Path $Root 'placement_think_off.py'
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
    FreeState
    Run $vpy ('"' + $variant + '" "' + $lab + '" qwen3:1.7b 50 4096 10') 'p04-r4-think-off' $Root 14400 | Out-Null
    Run $ollama 'ps' 'p04-r4-ps-think-off' | Out-Null
    Run $ollama 'stop qwen3:1.7b' 'p04-r4-stop-think-off' | Out-Null
} catch { Log ('Part 04 R4 stopped: ' + $_.Exception.Message) }

Step 'FINISHED'
FreeState
