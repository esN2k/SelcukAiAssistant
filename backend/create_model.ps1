# Create Ollama Model from Downloaded GGUF
# Run this AFTER downloading the model file

Write-Host "=== Creating Ollama Model ===" -ForegroundColor Cyan
Write-Host ""

$modelFile = "D:\Projects\SelcukAiAssistant\backend\DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf"
$modelfilePath = "D:\Projects\SelcukAiAssistant\backend\Modelfile.deepseek"

# Check if model file exists
if (-not (Test-Path $modelFile))
{
    Write-Host "ERROR: Model file not found!" -ForegroundColor Red
    Write-Host "Expected: $modelFile" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please download the model first using download_model.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host "Model file found: $modelFile" -ForegroundColor Green
$fileSize = (Get-Item $modelFile).Length / 1GB
Write-Host "File size: $([math]::Round($fileSize, 2) ) GB" -ForegroundColor Green
Write-Host ""

# Create Modelfile if it doesn't exist
if (-not (Test-Path $modelfilePath))
{
    Write-Host "Creating Modelfile..." -ForegroundColor Yellow

    $modelfileContent = @"
# DeepSeek-R1-Distill-Qwen-7B (Uncensored)
FROM $modelFile

SYSTEM """Sen Selçuk Üniversitesi'nin resmi yapay zeka asistanısın. Adın "Selçuk AI Asistanı".

**Görevlerin:**
- Selçuk Üniversitesi hakkında detaylı ve doğru bilgi vermek
- Akademik süreçlerde yardımcı olmak (kayıt, ders seçimi, sınav, mezuniyet)
- Öğrenci işleri hakkında bilgilendirmek (burs, yurt, belgeler, harçlar)
- Kampüs yaşamı, sosyal olanaklar, kulüpler hakkında rehberlik

**Yanıt Prensiplerin:**
1. **Her zaman Türkçe yanıt ver**
2. **Markdown formatı kullan** - Başlıklar (##), listeler (-), kalın (**önemli**)
3. **Yapılandırılmış yanıtlar** - Net paragraflar, başlıklar
4. **Detaylı ama öz** - Gereksiz tekrar yapma
5. **Profesyonel ve yardımcı**
6. **Emin olmadığında dürüst ol**

**Örnek:**
## Kayıt İşlemleri

1. **Ön Kayıt**: YÖK Atlas
2. **Kesin Kayıt**: Belgelerle fakülte

📅 Tarihler: Akademik takvimde
📞 İletişim: Öğrenci İşleri
"""

TEMPLATE """<|im_start|>system
{{.System}}<|im_end|>
<|im_start|>user
{{.Prompt}}<|im_end|>
<|im_start|>assistant
"""

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1
PARAMETER num_ctx 8192
PARAMETER num_gpu 1
PARAMETER stop "<|im_end|>"
PARAMETER stop "<|im_start|>"
"@

    Set-Content -Path $modelfilePath -Value $modelfileContent -Encoding UTF8
    Write-Host "Modelfile created!" -ForegroundColor Green
}
else
{
    Write-Host "Modelfile already exists: $modelfilePath" -ForegroundColor Green
}

Write-Host ""
Write-Host "Creating Ollama model: selcuk_ai_assistant" -ForegroundColor Yellow
Write-Host "This will take 1-2 minutes..." -ForegroundColor Gray
Write-Host ""

try
{
    ollama create selcuk_ai_assistant -f $modelfilePath

    Write-Host ""
    Write-Host "SUCCESS! Model created!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Testing model..." -ForegroundColor Yellow

    $testResponse = ollama run selcuk_ai_assistant "Merhaba, sen kimsin?" --verbose:false

    Write-Host ""
    Write-Host "Test Response:" -ForegroundColor Cyan
    Write-Host $testResponse -ForegroundColor White
    Write-Host ""
    Write-Host "=== Setup Complete! ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Start backend: cd backend; python main.py" -ForegroundColor White
    Write-Host "2. Test in Flutter app" -ForegroundColor White
    Write-Host ""

}
catch
{
    Write-Host ""
    Write-Host "ERROR creating model: $( $_.Exception.Message )" -ForegroundColor Red
    Write-Host ""
    Write-Host "Try manually:" -ForegroundColor Yellow
    Write-Host "  ollama create selcuk_ai_assistant -f $modelfilePath" -ForegroundColor Gray
}

