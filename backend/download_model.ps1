# DeepSeek-R1 modeli için hızlı indirme
# Doğrudan indirme bağlantısı kullanılır - en hızlısı tarayıcı ile indirme
$utf8 = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding  = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8

Write-Host "=== DeepSeek-R1 Hızlı İndirme ===" -ForegroundColor Cyan
Write-Host ""

$modelUrl = "https://huggingface.co/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF/resolve/main/DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf"
$downloadPath = "D:\Projects\SelcukAiAssistant\backend\DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf"

Write-Host "Model: DeepSeek-R1-Distill-Qwen-7B (Q4_K_M)" -ForegroundColor Green
Write-Host "Boyut: ~4.4 GB" -ForegroundColor Green
Write-Host "Hedef: $downloadPath" -ForegroundColor Green
Write-Host ""

Write-Host "SEÇENEK 1: Tarayıcı ile indirme (EN HIZLI - ÖNERİLEN)" -ForegroundColor Yellow
Write-Host "====================================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "İndirme bağlantısı tarayıcıda açılıyor..." -ForegroundColor Cyan
Write-Host "İndirme otomatik başlayacak!" -ForegroundColor Green
Write-Host ""
Write-Host "URL: $modelUrl" -ForegroundColor Blue
Write-Host ""
Write-Host "İndirme tamamlandıktan sonra:" -ForegroundColor Yellow
Write-Host "1. Dosyayı şuraya taşı/kopyala: $downloadPath" -ForegroundColor White
Write-Host "2. Şunu çalıştır: .\\create_model.ps1" -ForegroundColor White
Write-Host ""

# Open in default browser
Start-Process $modelUrl

Write-Host ""
Write-Host "SEÇENEK 2: Komut satırı ile aria2 (HIZLI)" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "Eğer aria2 kuruluysa:" -ForegroundColor Cyan
Write-Host "  aria2c -x 16 -s 16 -k 1M -o `"$downloadPath`" `"$modelUrl`"" -ForegroundColor Gray
Write-Host ""

Write-Host "SEÇENEK 3: wget (kuruluysa)" -ForegroundColor Yellow
Write-Host "===========================" -ForegroundColor Yellow
Write-Host "  wget -O `"$downloadPath`" `"$modelUrl`"" -ForegroundColor Gray
Write-Host ""

Write-Host "İndirme tamamlanınca bir tuşa basın..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
