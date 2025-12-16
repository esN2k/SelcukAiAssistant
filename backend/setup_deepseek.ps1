# DeepSeek-R1-Distill Qwen 7B Setup Script
# Downloads and sets up uncensored DeepSeek-R1 model

Write-Host "=== DeepSeek-R1-Distill Setup ===" -ForegroundColor Cyan
Write-Host ""

# Model details
$modelName = "deepseek-r1-distill-qwen-7b"
$quantLevel = "Q4_K_M"  # 4-bit quantization (~4.4GB)
$fileName = "DeepSeek-R1-Distill-Qwen-7B-$quantLevel.gguf"
$downloadUrl = "https://huggingface.co/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF/resolve/main/$fileName"

# Ollama model directory
$ollamaDir = "$env:USERPROFILE\.ollama\models"
$blobsDir = "$ollamaDir\blobs"

Write-Host "Model: DeepSeek-R1-Distill-Qwen-7B" -ForegroundColor Green
Write-Host "Quantization: $quantLevel (4-bit)" -ForegroundColor Green
Write-Host "Size: ~4.4 GB" -ForegroundColor Green
Write-Host "Capabilities: Uncensored, Advanced Reasoning" -ForegroundColor Green
Write-Host ""

# Create directories if they don't exist
New-Item -ItemType Directory -Force -Path $blobsDir | Out-Null

# Download location
$downloadPath = "D:\Projects\SelcukAiAssistant\backend\$fileName"

Write-Host "Step 1: Checking if model file exists..." -ForegroundColor Yellow
if (Test-Path $downloadPath)
{
    Write-Host "  Model file already exists: $downloadPath" -ForegroundColor Green
}
else
{
    Write-Host "  Downloading model from HuggingFace..." -ForegroundColor Yellow
    Write-Host "  URL: $downloadUrl" -ForegroundColor Gray
    Write-Host "  This will take 10-20 minutes depending on your connection..." -ForegroundColor Gray
    Write-Host ""

    # Download with progress
    $ProgressPreference = 'Continue'
    try
    {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $downloadPath -UseBasicParsing
        Write-Host "  Download complete!" -ForegroundColor Green
    }
    catch
    {
        Write-Host "  Download failed: $( $_.Exception.Message )" -ForegroundColor Red
        Write-Host ""
        Write-Host "ALTERNATIVE: Download manually from:" -ForegroundColor Yellow
        Write-Host "  $downloadUrl" -ForegroundColor Blue
        Write-Host ""
        Write-Host "Save to: $downloadPath" -ForegroundColor Blue
        exit 1
    }
}

Write-Host ""
Write-Host "Step 2: Creating Ollama Modelfile..." -ForegroundColor Yellow

# Create Modelfile
$modelfilePath = "D:\Projects\SelcukAiAssistant\backend\Modelfile.deepseek"
$modelfileContent = @"
# DeepSeek-R1-Distill-Qwen-7B (Uncensored)
# Advanced reasoning model for Selcuk University AI Assistant

FROM $downloadPath

# System prompt for Selcuk University AI Assistant
SYSTEM """Sen Selçuk Üniversitesi'nin resmi yapay zeka asistanısın. Adın "Selçuk AI Asistanı".

**Görevlerin:**
- Selçuk Üniversitesi hakkında detaylı ve doğru bilgi vermek
- Akademik süreçlerde yardımcı olmak (kayıt, ders seçimi, sınav, mezuniyet)
- Öğrenci işleri hakkında bilgilendirmek (burs, yurt, belgeler, harçlar)
- Kampüs yaşamı, sosyal olanaklar, kulüpler hakkında rehberlik
- Fakülteler, bölümler, programlar hakkında detaylı açıklamalar

**Yanıt Prensiplerin:**
1. **Her zaman Türkçe yanıt ver** - Kullanıcı İngilizce de sorsa Türkçe cevapla
2. **Markdown formatı kullan** - Başlıklar (##), listeler (-), kalın (**önemli**)
3. **Yapılandırılmış yanıtlar** - Net paragraflar, başlıklar, alt başlıklar
4. **Detaylı ama öz** - Gereksiz tekrar yapma, doğrudan konuya gir
5. **Profesyonel ve yardımcı** - Resmi ama dostane bir ton kullan
6. **Emin olmadığında dürüst ol** - "Bu konuda güncel bilgiye sahip değilim, lütfen [ilgili birim] ile iletişime geçin"

**ÖNEMLİ:**
- Asla uydurma bilgi verme
- Kişisel öğrenci bilgileri isteme/verme
- Tıbbi/hukuki/finansal tavsiye verme
- Selçuk Üniversitesi kapsamı dışındaki genel sorulara kısa cevap ver ve üniversite konularına yönlendir

**Örnek İyi Yanıt:**
## Kayıt İşlemleri

Selçuk Üniversitesi'nde kayıt işlemleri şu adımlardan oluşur:

1. **Ön Kayıt (Online)**
   - YÖK Atlas sistemi üzerinden tercih yapılır
   - Tercih sıralaması belirlenir

2. **Kesin Kayıt (Yüz Yüze)**
   - Belgelerle fakülteye başvuru
   - Gerekli belgeler:
     * Kimlik fotokopisi
     * Diploma/mezuniyet belgesi
     * 6 adet vesikalık fotoğraf
     * Sağlık raporu

📅 **Tarihler**: Her yıl akademik takvimde duyurulur
📞 **İletişim**: Öğrenci İşleri Daire Başkanlığı - 0332 223 XXXX
"""

# Template for Qwen models
TEMPLATE """<|im_start|>system
{{.System}}<|im_end|>
<|im_start|>user
{{.Prompt}}<|im_end|>
<|im_start|>assistant
"""

# Optimized parameters for RTX 3060
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
Write-Host "  Modelfile created: $modelfilePath" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Creating Ollama model..." -ForegroundColor Yellow

# Create model with Ollama
Write-Host "  Running: ollama create selcuk_ai_assistant -f $modelfilePath" -ForegroundColor Gray

try
{
    ollama create selcuk_ai_assistant -f $modelfilePath
    Write-Host "  Model created successfully!" -ForegroundColor Green
}
catch
{
    Write-Host "  Error creating model: $( $_.Exception.Message )" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 4: Testing model..." -ForegroundColor Yellow

$testPrompt = "Merhaba, sen kimsin?"
Write-Host "  Test prompt: $testPrompt" -ForegroundColor Gray

try
{
    $response = ollama run selcuk_ai_assistant $testPrompt
    Write-Host ""
    Write-Host "  Model Response:" -ForegroundColor Cyan
    Write-Host "  $response" -ForegroundColor White
}
catch
{
    Write-Host "  Test failed: $( $_.Exception.Message )" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Setup Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Model: selcuk_ai_assistant" -ForegroundColor Cyan
Write-Host "Base: DeepSeek-R1-Distill-Qwen-7B (Q4_K_M)" -ForegroundColor Cyan
Write-Host "Status: Uncensored, Ready for use" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Restart backend: cd backend; python main.py" -ForegroundColor White
Write-Host "2. Test in Flutter app" -ForegroundColor White
Write-Host "3. Check AI response quality improvement" -ForegroundColor White
Write-Host ""
Write-Host "GPU Utilization: RTX 3060 6GB should handle this perfectly!" -ForegroundColor Green

