# Jarvis one-click setup for Windows. Safe to re-run. Free, local, no API keys.
#   Right-click > Run with PowerShell, or double-click Setup-Jarvis.bat
param(
    [switch]$SkipWebUI,    # skip Open WebUI (big install)
    [switch]$WithCoder,    # also pull the coding model
    [string]$Model         # force a specific Ollama model, e.g. qwen2.5:14b
)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

function Say($m)  { Write-Host "[jarvis] $m" -ForegroundColor Cyan }
function Warn($m) { Write-Host "[jarvis] $m" -ForegroundColor Yellow }
function Have($c) { [bool](Get-Command $c -ErrorAction SilentlyContinue) }
function Refresh-Path {
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
}
function Winget-Install($id) {
    if (-not (Have winget)) { throw "winget not found. Install 'App Installer' from the Microsoft Store, then re-run." }
    winget install -e --id $id --silent --accept-package-agreements --accept-source-agreements
    Refresh-Path
}

# ---------- 1. Hardware ----------
$ramGB = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB)
$gpuNames = (Get-CimInstance Win32_VideoController | ForEach-Object { $_.Name }) -join ', '
$vramGB = 0
if (Have nvidia-smi) {
    try { $vramGB = [math]::Round([double]((nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | Select-Object -First 1).Trim()) / 1024) } catch {}
}
$freeGB = [math]::Round((Get-PSDrive -Name ($Root.Substring(0,1))).Free / 1GB)
Say "RAM: $ramGB GB | GPU: $gpuNames | NVIDIA VRAM: $vramGB GB | Free disk: $freeGB GB"

# ---------- 2. Pick model for this hardware ----------
if ($Model) { $main = $Model }
elseif ($vramGB -ge 24) { $main = 'qwen2.5:32b' }
elseif ($vramGB -ge 12) { $main = 'qwen2.5:14b' }
elseif ($vramGB -ge 8)  { $main = 'qwen2.5:7b' }
elseif ($ramGB -ge 32)  { $main = 'qwen2.5:14b' }
elseif ($ramGB -ge 16)  { $main = 'qwen2.5:7b' }
elseif ($ramGB -ge 8)   { $main = 'qwen2.5:3b' }
else                    { $main = 'qwen2.5:1.5b' }
$coder = $main -replace '^qwen2\.5:', 'qwen2.5-coder:'
Say "Chosen model: $main"
if ($freeGB -lt 15) { Warn "Low disk space ($freeGB GB free). Models are 2-20 GB; free some space if the download fails." }

# ---------- 3. Ollama ----------
if (-not (Have ollama)) {
    $guess = Join-Path $env:LOCALAPPDATA 'Programs\Ollama'
    if (Test-Path (Join-Path $guess 'ollama.exe')) { $env:Path += ";$guess" }
}
if (-not (Have ollama)) { Say 'Installing Ollama...'; Winget-Install 'Ollama.Ollama' }
if (-not (Have ollama)) { $env:Path += ';' + (Join-Path $env:LOCALAPPDATA 'Programs\Ollama') }
if (-not (Have ollama)) { throw 'Ollama installed but not on PATH. Open a new terminal and re-run setup.' }

$up = $false
try { Invoke-RestMethod http://localhost:11434/api/tags -TimeoutSec 3 | Out-Null; $up = $true } catch {}
if (-not $up) {
    Say 'Starting Ollama...'
    Start-Process ollama -ArgumentList 'serve' -WindowStyle Hidden
    for ($i = 0; $i -lt 20 -and -not $up; $i++) {
        Start-Sleep 1
        try { Invoke-RestMethod http://localhost:11434/api/tags -TimeoutSec 2 | Out-Null; $up = $true } catch {}
    }
}
if (-not $up) { throw 'Could not reach Ollama on localhost:11434.' }

Say "Downloading $main (this can take a while)..."
ollama pull $main
if ($WithCoder) { Say "Downloading $coder..."; ollama pull $coder } else { $coder = '' }

@{ model = $main; coder_model = $coder; api_base = 'http://localhost:11434' } |
    ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $Root 'config.json')

# ---------- 4. Python 3.11 (needed by Open Interpreter / Open WebUI) ----------
function Find-Python {
    foreach ($v in '3.11', '3.12') {
        try {
            $p = (& py "-$v" -c 'import sys;print(sys.executable)' 2>$null)
            if ($LASTEXITCODE -eq 0 -and $p) { return $p.Trim() }
        } catch {}
    }
    foreach ($c in "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe", "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe") {
        if (Test-Path $c) { return $c }
    }
    return $null
}
$py = Find-Python
if (-not $py) { Say 'Installing Python 3.11...'; Winget-Install 'Python.Python.3.11'; $py = Find-Python }
if (-not $py) { throw 'Python 3.11 not found after install. Open a new terminal and re-run.' }
Say "Using Python: $py"

# ---------- 5. Agent + voice environment ----------
if (-not (Test-Path '.venv\Scripts\python.exe')) { & $py -m venv .venv }
$vpy = Join-Path $Root '.venv\Scripts\python.exe'
& $vpy -m pip install --upgrade pip
Say 'Installing Open Interpreter + voice packages...'
& $vpy -m pip install open-interpreter faster-whisper sounddevice numpy
if ($LASTEXITCODE -ne 0) { throw 'pip install failed for the agent environment.' }

# ---------- 6. Chat UI (optional) ----------
if (-not $SkipWebUI) {
    Say 'Installing Open WebUI (chat interface)...'
    if (-not (Test-Path '.venv-webui\Scripts\python.exe')) { & $py -m venv .venv-webui }
    & (Join-Path $Root '.venv-webui\Scripts\python.exe') -m pip install --upgrade pip open-webui
    if ($LASTEXITCODE -ne 0) { Warn 'Open WebUI failed to install. Jarvis still works without it.' }
}

# ---------- 7. Launchers ----------
$bat = @{
    'Jarvis.bat'       = "@echo off`r`ncd /d `"%~dp0`"`r`ntasklist /fi `"imagename eq ollama.exe`" | find /i `"ollama.exe`" >nul || start `"`" /min ollama serve`r`n.venv\Scripts\python.exe jarvis.py %*`r`n"
    'Jarvis-Voice.bat' = "@echo off`r`ncd /d `"%~dp0`"`r`ntasklist /fi `"imagename eq ollama.exe`" | find /i `"ollama.exe`" >nul || start `"`" /min ollama serve`r`n.venv\Scripts\python.exe jarvis_voice.py %*`r`n"
    'Jarvis-UI.bat'    = "@echo off`r`ncd /d `"%~dp0`"`r`ntasklist /fi `"imagename eq ollama.exe`" | find /i `"ollama.exe`" >nul || start `"`" /min ollama serve`r`nstart `"`" http://localhost:8080`r`n.venv-webui\Scripts\open-webui.exe serve --port 8080`r`n"
}
foreach ($k in $bat.Keys) { [IO.File]::WriteAllText((Join-Path $Root $k), $bat[$k], [Text.Encoding]::ASCII) }

# Desktop shortcut for the text agent
try {
    $sh = (New-Object -ComObject WScript.Shell).CreateShortcut((Join-Path ([Environment]::GetFolderPath('Desktop')) 'Jarvis.lnk'))
    $sh.TargetPath = Join-Path $Root 'Jarvis.bat'; $sh.WorkingDirectory = $Root; $sh.Save()
} catch {}

Say 'Done.'
Write-Host ''
Write-Host '  Jarvis.bat          text agent (asks before running code)'
Write-Host '  Jarvis-Voice.bat    say "Jarvis, open Notepad"'
Write-Host '  Jarvis-UI.bat       chat in your browser (Open WebUI)'
Write-Host ''
Write-Host "  Model in use: $main"
