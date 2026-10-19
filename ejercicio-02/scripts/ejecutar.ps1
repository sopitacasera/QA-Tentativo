$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

New-Item -ItemType Directory -Force -Path "reports\evidencia" | Out-Null

if (-not (Test-Path ".\node_modules\cypress")) {
    npm install
}

npx cypress run
$codigo = $LASTEXITCODE
node .\scripts\informe.js
exit $codigo
