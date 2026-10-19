$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Output "=== Ejercicio 01: compra en OpenCart ==="
powershell -ExecutionPolicy Bypass -File ".\ejercicio-01\scripts\ejecutar.ps1"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Output "=== Ejercicio 02: API PetStore ==="
powershell -ExecutionPolicy Bypass -File ".\ejercicio-02\scripts\ejecutar.ps1"
exit $LASTEXITCODE
