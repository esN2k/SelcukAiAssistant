param(
    [string]$InputPath = "data/rag/selcuk",
    [string]$OutputPath = "data/rag"
)

$ErrorActionPreference = "Stop"

$root = $PSScriptRoot
$input = Join-Path $root $InputPath
$output = Join-Path $root $OutputPath

if (-not (Test-Path $input)) {
    throw "Input path not found: $input"
}

if (-not (Test-Path $output)) {
    New-Item -ItemType Directory -Force -Path $output | Out-Null
}

python (Join-Path $root "rag_ingest.py") --input $input --output $output --reset
