$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

New-Item -ItemType Directory -Force -Path "reports\evidence" | Out-Null

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    python -m venv .venv
}

& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt

& ".\.venv\Scripts\python.exe" -m pytest
exit $LASTEXITCODE
