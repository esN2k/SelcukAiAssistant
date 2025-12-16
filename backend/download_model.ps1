# Fast DeepSeek-R1 Model Download
# Uses direct download link - open in browser for fastest download

Write-Host "=== DeepSeek-R1 Fast Download ===" -ForegroundColor Cyan
Write-Host ""

$modelUrl = "https://huggingface.co/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF/resolve/main/DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf"
$downloadPath = "D:\Projects\SelcukAiAssistant\backend\DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf"

Write-Host "Model: DeepSeek-R1-Distill-Qwen-7B (Q4_K_M)" -ForegroundColor Green
Write-Host "Size: ~4.4 GB" -ForegroundColor Green
Write-Host "Target: $downloadPath" -ForegroundColor Green
Write-Host ""

Write-Host "OPTION 1: Browser Download (FASTEST - RECOMMENDED)" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "Opening download link in browser..." -ForegroundColor Cyan
Write-Host "Download will start automatically!" -ForegroundColor Green
Write-Host ""
Write-Host "URL: $modelUrl" -ForegroundColor Blue
Write-Host ""
Write-Host "After download completes:" -ForegroundColor Yellow
Write-Host "1. Move/Copy file to: $downloadPath" -ForegroundColor White
Write-Host "2. Run: .\create_model.ps1" -ForegroundColor White
Write-Host ""

# Open in default browser
Start-Process $modelUrl

Write-Host ""
Write-Host "OPTION 2: Command Line with aria2 (FAST)" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "If you have aria2 installed:" -ForegroundColor Cyan
Write-Host "  aria2c -x 16 -s 16 -k 1M -o `"$downloadPath`" `"$modelUrl`"" -ForegroundColor Gray
Write-Host ""

Write-Host "OPTION 3: wget (if installed)" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Yellow
Write-Host "  wget -O `"$downloadPath`" `"$modelUrl`"" -ForegroundColor Gray
Write-Host ""

Write-Host "Press any key when download is complete..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

