# İndirilen GGUF dosyasından Ollama modeli oluştur
# Model dosyası indirildikten sonra çalıştırın
$utf8 = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding  = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8

function Write-Utf8NoBom {
  param(
    [string]$Path,
    [string]$Content
  )
  $encoding = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($Path, $Content, $encoding)
}

Write-Host "=== Ollama modeli oluşturuluyor ===" -ForegroundColor Cyan
Write-Host ""

$modelFile = "D:\Projects\SelcukAiAssistant\backend\DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf"
$modelfilePath = "D:\Projects\SelcukAiAssistant\backend\Modelfile.deepseek"

# Model dosyası var mı kontrol et
if (-not (Test-Path $modelFile))
{
    Write-Host "HATA: Model dosyası bulunamadı!" -ForegroundColor Red
    Write-Host "Beklenen konum: $modelFile" -ForegroundColor Red
    Write-Host ""
    Write-Host "Önce download_model.ps1 ile modeli indirin." -ForegroundColor Yellow
    exit 1
}

Write-Host "Model dosyası bulundu: $modelFile" -ForegroundColor Green
$fileSize = (Get-Item $modelFile).Length / 1GB
Write-Host "Dosya boyutu: $([math]::Round($fileSize, 2) ) GB" -ForegroundColor Green
Write-Host ""

# Modelfile yoksa oluştur
if (-not (Test-Path $modelfilePath))
{
    Write-Host "Modelfile oluşturuluyor..." -ForegroundColor Yellow

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

- Tarihler: Akademik takvimde
- İletişim: Öğrenci İşleri
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

    Write-Utf8NoBom -Path $modelfilePath -Content $modelfileContent
    Write-Host "Modelfile oluşturuldu." -ForegroundColor Green
}
else
{
    Write-Host "Modelfile zaten var: $modelfilePath" -ForegroundColor Green
}

Write-Host ""
Write-Host "Ollama modeli oluşturuluyor: selcuk_ai_assistant" -ForegroundColor Yellow
Write-Host "Bu işlem 1-2 dakika sürebilir..." -ForegroundColor Gray
Write-Host ""

try
{
    ollama create selcuk_ai_assistant -f $modelfilePath

    Write-Host ""
    Write-Host "BAŞARILI! Model oluşturuldu." -ForegroundColor Green
    Write-Host ""
    Write-Host "Model test ediliyor..." -ForegroundColor Yellow

    $testResponse = ollama run selcuk_ai_assistant "Merhaba, sen kimsin?" --verbose:false

    Write-Host ""
    Write-Host "Test yanıtı:" -ForegroundColor Cyan
    Write-Host $testResponse -ForegroundColor White
    Write-Host ""
    Write-Host "=== Kurulum tamamlandı! ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Sonraki adımlar:" -ForegroundColor Yellow
    Write-Host "1. Backend'i başlat: cd backend; python main.py" -ForegroundColor White
    Write-Host "2. Flutter uygulamasında test et" -ForegroundColor White
    Write-Host ""

}
catch
{
    Write-Host ""
    Write-Host "Model oluşturma hatası: $( $_.Exception.Message )" -ForegroundColor Red
    Write-Host ""
    Write-Host "Manuel dene:" -ForegroundColor Yellow
    Write-Host "  ollama create selcuk_ai_assistant -f $modelfilePath" -ForegroundColor Gray
}
