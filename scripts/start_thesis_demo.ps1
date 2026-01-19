# ============================================
# Selçuk AI Asistan - Tez Demo Başlatma
# ============================================

Write-Host "=" -ForegroundColor Cyan -NoNewline; Write-Host ("=" * 58) -ForegroundColor Cyan
Write-Host "🎓 Selçuk AI Asistan - Tez Demo Başlatılıyor" -ForegroundColor Green
Write-Host "=" -ForegroundColor Cyan -NoNewline; Write-Host ("=" * 58) -ForegroundColor Cyan
Write-Host ""

# Değişkenler
$PROJECT_ROOT = "e:\SelcukAiAssistant\repo"
$BACKEND_DIR = "$PROJECT_ROOT\backend"

# 1. Sistem Kontrolleri
Write-Host "🔍 Sistem kontrolleri..." -ForegroundColor Yellow

# Python kontrolü
Write-Host "   Checking Python..." -NoNewline
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonVersion = python --version
    Write-Host " ✅ $pythonVersion" -ForegroundColor Green
} else {
    Write-Host " ❌ Python bulunamadı!" -ForegroundColor Red
    exit 1
}

# Ollama kontrolü
Write-Host "   Checking Ollama..." -NoNewline
if (Get-Process -Name ollama -ErrorAction SilentlyContinue) {
    Write-Host " ✅ Çalışıyor" -ForegroundColor Green
} else {
    Write-Host " ⚠️  Başlatılıyor..." -ForegroundColor Yellow
    Start-Process ollama -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
}

# Model kontrolü
Write-Host "   Checking Models..." -NoNewline
$llamaCheck = ollama list | Select-String "llama"
$translateCheck = ollama list | Select-String "translategemma"
if ($llamaCheck -and $translateCheck) {
    Write-Host " ✅ Llama + TranslateGemma yüklü" -ForegroundColor Green
} elseif ($llamaCheck) {
    Write-Host " ⚠️  TranslateGemma eksik" -ForegroundColor Yellow
    Write-Host "   Kurulum için: python backend/install_translation.py" -ForegroundColor Gray
} else {
    Write-Host " ⚠️  Modeller bulunamadı" -ForegroundColor Yellow
}

Write-Host ""

# 2. Backend Başlatma
Write-Host "🔧 Backend başlatılıyor..." -ForegroundColor Yellow
Set-Location $BACKEND_DIR

# Backend'i arka planda başlat
Write-Host "   Starting FastAPI server..." -ForegroundColor Gray
$backendJob = Start-Job -ScriptBlock {
    param($dir)
    Set-Location $dir
    if (Test-Path ".\venv\Scripts\Activate.ps1") {
        & .\venv\Scripts\Activate.ps1
    }
    python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
} -ArgumentList $BACKEND_DIR

Write-Host "   Loading RAG service and models (30 seconds)..." -ForegroundColor Gray
Start-Sleep -Seconds 30

# Backend health check with retries
Write-Host "   Health check..." -NoNewline
$maxRetries = 5
$retryCount = 0
$success = $false

while ($retryCount -lt $maxRetries -and -not $success) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Host " ✅ Backend hazır" -ForegroundColor Green
            $success = $true
        }
    } catch {
        $retryCount++
        if ($retryCount -lt $maxRetries) {
            Write-Host "." -NoNewline -ForegroundColor Yellow
            Start-Sleep -Seconds 5
        }
    }
}

if (-not $success) {
    Write-Host " ❌ Backend başlatılamadı!" -ForegroundColor Red
    Write-Host "   Lütfen backend loglarını kontrol edin" -ForegroundColor Yellow
    Stop-Job $backendJob
    exit 1
}

Write-Host ""

# 3. API Docs Aç
Write-Host "📖 API Dokümantasyonu açılıyor..." -ForegroundColor Yellow
Start-Process "http://localhost:8000/docs"
Start-Sleep -Seconds 2
Write-Host "   ✅ Tarayıcıda açıldı: http://localhost:8000/docs" -ForegroundColor Green

Write-Host ""

# 4. Demo Bilgileri
Write-Host "=" -ForegroundColor Cyan -NoNewline; Write-Host ("=" * 58) -ForegroundColor Cyan
Write-Host "✅ TÜM SERVİSLER HAZIR!" -ForegroundColor Green
Write-Host "=" -ForegroundColor Cyan -NoNewline; Write-Host ("=" * 58) -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Erişim Noktaları:" -ForegroundColor Yellow
Write-Host "   Backend API:  http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs:     http://localhost:8000/docs" -ForegroundColor White
Write-Host "   Health Check: http://localhost:8000/health" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Demo Test Komutları:" -ForegroundColor Yellow
Write-Host "   1. Chat Test:" -ForegroundColor White
Write-Host '   curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"message\":\"Teknoloji Fakültesinde kaç bölüm var?\"}"' -ForegroundColor Gray
Write-Host ""
Write-Host "   2. Translation Test (TranslateGemma 4B):" -ForegroundColor White
Write-Host '   curl -X POST http://localhost:8000/translate -H "Content-Type: application/json" -d "{\"text\":\"Yapay Zeka\",\"source_lang\":\"tr\",\"target_lang\":\"en\"}"' -ForegroundColor Gray
Write-Host ""
Write-Host "⏹️  Durdurmak için: Ctrl+C" -ForegroundColor Red
Write-Host "=" -ForegroundColor Cyan -NoNewline; Write-Host ("=" * 58) -ForegroundColor Cyan

# Servislerin çalışmasını bekle
Write-Host ""
Write-Host "Servisler çalışıyor... (Ctrl+C ile çıkış)" -ForegroundColor Yellow
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host "`nServisler durduruluyor..." -ForegroundColor Yellow
    Stop-Job $backendJob
    Remove-Job $backendJob
}
