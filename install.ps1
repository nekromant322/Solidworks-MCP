# SolidWorks MCP - one-click setup for Windows + SOLIDWORKS 2026 + Claude Desktop
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
Write-Host "== SolidWorks MCP setup ==" -ForegroundColor Cyan

# 1. Python 3.10+
function Test-Py($exe, $pre) {
  try { $v = & $exe @pre -c "import sys;print(sys.version_info>=(3,10))" 2>$null; return ($v -eq "True") } catch { return $false }
}
$pyExe = $null; $pyPre = @()
if (Test-Py "py" @("-3")) { $pyExe = "py"; $pyPre = @("-3") }
elseif (Test-Py "python" @()) { $pyExe = "python" }
else {
  Write-Host "Python 3.10+ not found - installing Python 3.12 via winget..." -ForegroundColor Yellow
  winget install -e --id Python.Python.3.12 --scope user --accept-package-agreements --accept-source-agreements
  $pyExe = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"
}
Write-Host "[1/4] Python: $(& $pyExe @pyPre --version)"

# 2. venv + dependencies
if (-not (Test-Path ".venv\Scripts\python.exe")) { & $pyExe @pyPre -m venv .venv }
$vpy = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
& $vpy -m pip install --upgrade pip -q
& $vpy -m pip install -r requirements.txt -q
Write-Host "[2/4] Dependencies installed in .venv"

# 3. Claude Desktop config
Write-Host "[3/4] Registering MCP server 'solidworks' in Claude Desktop:"
& $vpy setup\configure_claude.py

# 4. Diagnostics
Write-Host "[4/4] SOLIDWORKS check:"
& $vpy setup\check_solidworks.py

Write-Host ""
Write-Host "Done. Fully quit Claude Desktop (tray icon -> Quit) and start it again." -ForegroundColor Green
Write-Host "Then start SOLIDWORKS 2026 and ask Claude: 'Connect to SolidWorks'." -ForegroundColor Green
