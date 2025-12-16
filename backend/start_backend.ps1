# Quick Test Script for Backend
Write-Host "=== Backend Test ===" -ForegroundColor Cyan

# Navigate to backend
cd D:\Projects\SelcukAiAssistant\backend

# Check Python
Write-Host "Python version:" -ForegroundColor Yellow
python --version

# Check venv
Write-Host "`nActivating venv..." -ForegroundColor Yellow
if (Test-Path ".\.venv\Scripts\Activate.ps1")
{
    & .\.venv\Scripts\Activate.ps1
    Write-Host "Venv activated!" -ForegroundColor Green
}
else
{
    Write-Host "Venv not found, using system Python" -ForegroundColor Yellow
}

# Check Ollama
Write-Host "`nOllama models:" -ForegroundColor Yellow
ollama list | Select-String "selcuk"

# Start backend
Write-Host "`nStarting backend..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor Gray
python main.py

