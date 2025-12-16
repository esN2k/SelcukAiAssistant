# Restart Backend Script
Write-Host "Restarting backend..." -ForegroundColor Yellow

# Stop existing backend
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if ($pythonProcesses)
{
    Write-Host "Stopping existing backend processes..." -ForegroundColor Red
    $pythonProcesses | Stop-Process -Force
    Start-Sleep -Seconds 2
}

# Start new backend
Write-Host "Starting backend with improved reasoning cleanup..." -ForegroundColor Green
cd D:\Projects\SelcukAiAssistant\backend
python main.py

