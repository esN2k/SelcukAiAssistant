# DeepSeek-R1-Distill Qwen 7B kurulum scripti
# Uncensored DeepSeek-R1 modelini indirir ve kurar
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

Write-Host "=== DeepSeek-R1-Distill Kurulumu ===" -ForegroundColor Cyan
Write-Host ""

# Model detayları
$modelName = "deepseek-r1-distill-qwen-7b"
$quantLevel = "Q4_K_M"  # 4-bit quantization (~4.4GB)
$fileName = "DeepSeek-R1-Distill-Qwen-7B-$quantLevel.gguf"
$downloadUrl = "https://huggingface.co/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF/resolve/main/$fileName"

# Ollama model dizini
$ollamaDir = "$env:USERPROFILE\.ollama\models"
$blobsDir = "$ollamaDir\blobs"

Write-Host "Model: DeepSeek-R1-Distill-Qwen-7B" -ForegroundColor Green
Write-Host "Nicemleme: $quantLevel (4-bit)" -ForegroundColor Green
Write-Host "Boyut: ~4.4 GB" -ForegroundColor Green
Write-Host "Yetenekler: Sınırsız, Gelişmiş muhakeme" -ForegroundColor Green
Write-Host ""

# Dizinler yoksa oluştur
New-Item -ItemType Directory -Force -Path $blobsDir | Out-Null

# İndirme konumu
$downloadPath = "D:\Projects\SelcukAiAssistant\backend\$fileName"

Write-Host "Adım 1: Model dosyası var mı kontrol ediliyor..." -ForegroundColor Yellow
if (Test-Path $downloadPath)
{
    Write-Host "  Model dosyası zaten var: $downloadPath" -ForegroundColor Green
}
else
{
    Write-Host "  Model HuggingFace üzerinden indiriliyor..." -ForegroundColor Yellow
    Write-Host "  URL: $downloadUrl" -ForegroundColor Gray
    Write-Host "  Bağlantınıza göre 10-20 dakika sürebilir..." -ForegroundColor Gray
    Write-Host ""

    # İndirme (ilerleme göstergeli)
    $ProgressPreference = 'Continue'
    try
    {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $downloadPath -UseBasicParsing
        Write-Host "  İndirme tamamlandı." -ForegroundColor Green
    }
    catch
    {
        Write-Host "  İndirme başarısız: $( $_.Exception.Message )" -ForegroundColor Red
        Write-Host ""
        Write-Host "ALTERNATİF: Şuradan manuel indirin:" -ForegroundColor Yellow
        Write-Host "  $downloadUrl" -ForegroundColor Blue
        Write-Host ""
        Write-Host "Şuraya kaydedin: $downloadPath" -ForegroundColor Blue
        exit 1
    }
}

Write-Host ""
Write-Host "Adım 2: Ollama Modelfile oluşturuluyor..." -ForegroundColor Yellow

# Modelfile oluştur
$modelfilePath = "D:\Projects\SelcukAiAssistant\backend\Modelfile.deepseek"
$modelfileContent = @"
# DeepSeek-R1-Distill-Qwen-7B (Uncensored)
# Selçuk Üniversitesi Yapay Zeka Asistanı için gelişmiş muhakeme modeli

FROM $downloadPath

# Selçuk Üniversitesi Yapay Zeka Asistanı için sistem istemi
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

- Tarihler: Her yıl akademik takvimde duyurulur
- İletişim: Öğrenci İşleri Daire Başkanlığı - 0332 223 XXXX
"""

# Qwen modelleri için şablon
TEMPLATE """<|im_start|>system
{{.System}}<|im_end|>
<|im_start|>user
{{.Prompt}}<|im_end|>
<|im_start|>assistant
"""

# RTX 3060 için optimize parametreler
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
Write-Host "  Modelfile oluşturuldu: $modelfilePath" -ForegroundColor Green

Write-Host ""
Write-Host "Adım 3: Ollama modeli oluşturuluyor..." -ForegroundColor Yellow

# Ollama ile model oluştur
Write-Host "  Çalıştırılıyor: ollama create selcuk_ai_assistant -f $modelfilePath" -ForegroundColor Gray

try
{
    ollama create selcuk_ai_assistant -f $modelfilePath
    Write-Host "  Model başarıyla oluşturuldu." -ForegroundColor Green
}
catch
{
    Write-Host "  Model oluşturma hatası: $( $_.Exception.Message )" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Adım 4: Model test ediliyor..." -ForegroundColor Yellow

$testPrompt = "Merhaba, sen kimsin?"
Write-Host "  Test istemi: $testPrompt" -ForegroundColor Gray

try
{
    $response = ollama run selcuk_ai_assistant $testPrompt
    Write-Host ""
    Write-Host "  Model yanıtı:" -ForegroundColor Cyan
    Write-Host "  $response" -ForegroundColor White
}
catch
{
    Write-Host "  Test başarısız: $( $_.Exception.Message )" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Kurulum tamamlandı! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Model: selcuk_ai_assistant" -ForegroundColor Cyan
Write-Host "Taban: DeepSeek-R1-Distill-Qwen-7B (Q4_K_M)" -ForegroundColor Cyan
Write-Host "Durum: Hazır, kullanıma açık" -ForegroundColor Green
Write-Host ""
Write-Host "Sonraki adımlar:" -ForegroundColor Yellow
Write-Host "1. Backend'i yeniden başlat: cd backend; python main.py" -ForegroundColor White
Write-Host "2. Flutter uygulamasında test et" -ForegroundColor White
Write-Host "3. Yanıt kalitesindeki iyileşmeyi kontrol et" -ForegroundColor White
Write-Host ""
Write-Host "GPU Kullanımı: RTX 3060 6GB bu model için yeterli." -ForegroundColor Green
