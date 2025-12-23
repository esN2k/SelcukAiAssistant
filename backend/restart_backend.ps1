# Backend yeniden başlatma scripti
$utf8 = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding  = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8

Write-Host "Backend yeniden başlatılıyor..." -ForegroundColor Yellow

# Mevcut backend'i durdur
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if ($pythonProcesses)
{
    Write-Host "Mevcut backend süreçleri durduruluyor..." -ForegroundColor Red
    $pythonProcesses | Stop-Process -Force
    Start-Sleep -Seconds 2
}

# Yeni backend'i başlat
Write-Host "Backend (geliştirilmiş bellek temizliğiyle) başlatılıyor..." -ForegroundColor Green
cd D:\Projects\SelcukAiAssistant\backend
python main.py

