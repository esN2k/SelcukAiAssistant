# DeepSeek-R1 Model - Hızlı İndirme Rehberi

**Tarih**: 16 Aralık 2025  
**Sorun**: PowerShell `Invoke-WebRequest` çok yavaş (KB/s seviyesinde)  
**Çözüm**: Tarayıcı veya hızlı indirme araçları (MB/s seviyesinde)

---

## ⚡ HIZLI İNDİRME YÖNTEMLERİ

### Seçenek 1: Tarayıcıdan İndir (ÖNERİLEN - EN HIZLI)

✅ **Otomatik olarak açıldı!** Tarayıcınızda indirme başladı.

**İndirme Detayları:**

- **Dosya**: `DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf`
- **Boyut**: ~4.4 GB
- **Hız**: 5-20 MB/s (internet hızınıza göre)
- **Süre**: 5-10 dakika (High-speed WiFi ile)

**İndirme Tamamlandığında:**

1. **Dosyayı kontrol edin**: `Downloads` klasöründe olmalı
2. **Dosyayı taşıyın**:
   ```
   Kaynak: C:\Users\Esen\Downloads\DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf
   Hedef: D:\Projects\SelcukAiAssistant\backend\DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf
   ```

3. **Model'i oluşturun**:
   ```powershell
   cd D:\Projects\SelcukAiAssistant\backend
   .\create_model.ps1
   ```

---

### Seçenek 2: aria2c (Çok Hızlı - Alternatif)

**aria2c kurulu değilse:**

```powershell
# Chocolatey ile kur
choco install aria2
```

**İndirme komutu:**

```powershell
cd D:\Projects\SelcukAiAssistant\backend

aria2c -x 16 -s 16 -k 1M `
  -o "DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf" `
  "https://huggingface.co/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF/resolve/main/DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf"
```

**Avantajları:**

- ✅ 16 paralel bağlantı → Çok hızlı
- ✅ Kesintiye uğrarsa devam eder (resume)
- ✅ Hız: 10-30 MB/s

---

### Seçenek 3: wget (Hızlı)

**wget kurulu değilse:**

```powershell
# Chocolatey ile kur
choco install wget
```

**İndirme komutu:**

```powershell
cd D:\Projects\SelcukAiAssistant\backend

wget -O "DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf" `
  "https://huggingface.co/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF/resolve/main/DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf"
```

---

### Seçenek 4: curl (Built-in Windows)

```powershell
cd D:\Projects\SelcukAiAssistant\backend

curl -L -o "DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf" `
  "https://huggingface.co/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF/resolve/main/DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf"
```

**Not**: curl Windows 10+ ile birlikte gelir, ekstra kurulum gerekmez.

---

## 📊 Hız Karşılaştırması

| Yöntem                       | Ortalama Hız | Tahmini Süre (4.4 GB) |
|------------------------------|--------------|-----------------------|
| PowerShell Invoke-WebRequest | 100-500 KB/s | 2-12 saat ❌           |
| Chrome/Edge Tarayıcı         | 5-20 MB/s    | 5-10 dakika ✅         |
| aria2c (16 paralel)          | 10-30 MB/s   | 3-7 dakika ✅✅         |
| wget                         | 5-15 MB/s    | 5-12 dakika ✅         |
| curl                         | 5-15 MB/s    | 5-12 dakika ✅         |

---

## 🚀 İndirme Tamamlandıktan Sonra

### Adım 1: Dosyayı Kontrol Et

```powershell
# Downloads klasöründe mi?
Get-ChildItem C:\Users\Esen\Downloads\DeepSeek*.gguf

# Boyutu doğru mu? (~4.4 GB)
(Get-Item C:\Users\Esen\Downloads\DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf).Length / 1GB
```

**Beklenen**: ~4.4 GB (4,400,000,000 bytes civarı)

### Adım 2: Dosyayı Taşı (Eğer Downloads'ta ise)

```powershell
Move-Item `
  C:\Users\Esen\Downloads\DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf `
  D:\Projects\SelcukAiAssistant\backend\DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf
```

### Adım 3: Ollama Modeli Oluştur

```powershell
cd D:\Projects\SelcukAiAssistant\backend
.\create_model.ps1
```

**Script otomatik olarak:**

1. ✅ Dosya varlığını kontrol eder
2. ✅ Modelfile oluşturur
3. ✅ `ollama create selcuk_ai_assistant` çalıştırır
4. ✅ Modeli test eder
5. ✅ Başarı mesajı gösterir

**Tahmini Süre**: 1-2 dakika

### Adım 4: Backend'i Başlat

```powershell
cd D:\Projects\SelcukAiAssistant\backend
python main.py
```

**Beklenen log:**

```
INFO - Ollama service initialized: model=selcuk_ai_assistant
INFO - Appwrite client initialized
INFO - Starting server on 0.0.0.0:8000
```

### Adım 5: Test Et

Flutter'da soru sorun: **"Selçuk Üniversitesi hakkında bilgi ver"**

**Beklenen yanıt**: Markdown formatında, yapılandırılmış, profesyonel ✅

---

## 🔍 Sorun Giderme

### İndirme Çok Yavaş (KB/s)

**Sebep**: Tarayıcı veya aria2c yerine PowerShell kullanıyorsunuz

**Çözüm**:

1. PowerShell indirmeyi durdurun (`Ctrl+C`)
2. Tarayıcıdan indirin (yukarıdaki link otomatik açıldı)

### İndirme Yarıda Kesildi

**aria2c ile devam**:

```powershell
aria2c -c -x 16 -s 16 -k 1M `
  -o "DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf" `
  "https://huggingface.co/..."
```

`-c` parametresi kaldığı yerden devam ettirir.

### Dosya Boyutu Yanlış

**Kontrol**:

```powershell
(Get-Item DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf).Length
```

**Beklenen**: ~4,400,000,000 bytes

**Küçükse**: İndirme yarım kalmış, tekrar indirin

### HuggingFace Yavaş

**Alternatif mirror** (eğer varsa):

- ModelScope (Çin)
- Hugging Face CDN
- Torrent (eğer destekleniyorsa)

---

## 📝 Özet

1. ✅ **Tarayıcıda indirme başladı** (otomatik açıldı)
2. ⏳ **İndirme tamamlanmasını bekleyin** (5-10 dakika)
3. 📁 **Dosyayı `backend/` klasörüne taşıyın**
4. 🚀 **`.\create_model.ps1` çalıştırın**
5. ✅ **Backend'i başlatın ve test edin**

**Tarayıcı indirmesi PowerShell'den 10-50x daha hızlı!** 🚀

---

## 🎯 Neden PowerShell Yavaş?

**Teknik Açıklama:**

- `Invoke-WebRequest`: HTTP streaming yerine tüm dosyayı RAM'e yükler
- Çok büyük dosyalarda (.NET memory management) yavaşlar
- Tek bağlantı kullanır (paralel download yok)
- Progress tracking overhead ekler

**Tarayıcı/aria2c Neden Hızlı:**

- Paralel bağlantılar (16 stream)
- Chunk-based download (bellek verimli)
- Resume capability
- Native HTTP/2 desteği
- Daha iyi buffer management

**Sonuç**: 4.4 GB+ dosyalar için PowerShell kullanmayın! ❌

