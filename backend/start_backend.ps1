# Backend için hızlı test scripti
$utf8 = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding  = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8

Write-Host "=== Backend testi ===" -ForegroundColor Cyan

# Backend dizinine geç
cd D:\Projects\SelcukAiAssistant\backend

# Python kontrolü
Write-Host "Python sürümü:" -ForegroundColor Yellow
python --version

# Venv kontrolü
Write-Host "`nVenv etkinleştiriliyor..." -ForegroundColor Yellow
if (Test-Path ".\.venv\Scripts\Activate.ps1")
{
    & .\.venv\Scripts\Activate.ps1
    Write-Host "Venv etkinleştirildi." -ForegroundColor Green
}
else
{
    Write-Host "Venv bulunamadı, sistem Python kullanılacak." -ForegroundColor Yellow
}

# Ollama kontrolü
Write-Host "`nOllama modelleri:" -ForegroundColor Yellow
ollama list | Select-String "selcuk"

# Backend başlat
Write-Host "`nBackend başlatılıyor..." -ForegroundColor Yellow
Write-Host "Durdurmak için Ctrl+C`n" -ForegroundColor Gray
python main.py

