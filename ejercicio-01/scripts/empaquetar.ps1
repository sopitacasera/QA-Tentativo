$ErrorActionPreference = "Stop"
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
& powershell -ExecutionPolicy Bypass -File (Join-Path $root "empaquetar.ps1")
exit $LASTEXITCODE
