$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$project = (Resolve-Path $PSScriptRoot).Path
$destination = Join-Path (Split-Path -Parent $project) "QA-BP-ejercicios-qa.zip"
$excludeDirs = @(
    ".venv", ".git", ".pytest_cache", "__pycache__", ".idea", ".vscode",
    "node_modules", "videos", "screenshots"
)

if (Test-Path $destination) {
    Remove-Item $destination -Force
}

$zip = [System.IO.Compression.ZipFile]::Open($destination, [System.IO.Compression.ZipArchiveMode]::Create)
try {
    Get-ChildItem -Path $project -Recurse -File | ForEach-Object {
        $relative = $_.FullName.Substring($project.Length).TrimStart("\")
        $skip = $false
        foreach ($part in $relative.Split("\")) {
            if ($excludeDirs -contains $part) {
                $skip = $true
                break
            }
        }
        if (-not $skip) {
            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
                $zip,
                $_.FullName,
                $relative.Replace("\", "/")
            ) | Out-Null
        }
    }
}
finally {
    $zip.Dispose()
}

Write-Output "Paquete único creado: $destination"
