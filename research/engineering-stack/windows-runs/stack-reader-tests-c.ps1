# Engineering Stack: three small follow-up checks (October 20, 2026).
# Run by Claude with the owner's go-ahead, after stack-reader-tests-b.ps1. Nothing is
# downloaded or installed; folders are only listed, never changed.
#   Part 04: the tiktoken counts themselves (optional_tiktoken_check.py; the encoding is cached).
#   Part 10: where spaCy's en_core_web_lg went (pip show inside the lab's environment).
#   Parts 05, 10, 12: what the reader tests left outside the lab folders (model caches, garak files).
# Everything is written to stack-reader-tests-c.log in this folder.

$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$Root = Join-Path $env:USERPROFILE 'Downloads\ai-stack'
$Work = Join-Path $Root 'stack-reader-tests'
$Log  = Join-Path $Root 'stack-reader-tests-c.log'
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

Step 'Part 04: the tiktoken counts'
Run (VPy '04') 'optional_tiktoken_check.py' 'p04-tiktoken-counts' (Lab '04') | Out-Null

Step 'Part 10: where spaCy put en_core_web_lg'
Run (VPy '10') '-m pip show en_core_web_lg' 'p10-spacy-model-show' (Lab '10') | Out-Null

Step 'What the reader tests left outside the lab folders'
ListFolder (Join-Path $env:USERPROFILE '.cache\huggingface\hub')
ListFolder (Join-Path $env:USERPROFILE '.cache\huggingface')
ListFolder (Join-Path $env:USERPROFILE '.local\share\garak')
ListFolder (Join-Path $env:USERPROFILE '.config\garak')
ListFolder (Join-Path $env:USERPROFILE '.cache\garak')
ListFolder (Join-Path $env:LOCALAPPDATA 'garak')
ListFolder (Join-Path $env:USERPROFILE '.tiktoken')
Log ('TIKTOKEN_CACHE_DIR=' + $env:TIKTOKEN_CACHE_DIR + '; DATA_GYM_CACHE_DIR=' + $env:DATA_GYM_CACHE_DIR + '; TEMP=' + $env:TEMP)
ListFolder (Join-Path $env:TEMP 'data-gym-cache')

Step 'FINISHED'
Log ('Free disk on C: ' + [math]::Round((Get-PSDrive C).Free / 1GB, 1) + ' GB')
