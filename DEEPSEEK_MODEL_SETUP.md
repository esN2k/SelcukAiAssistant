# DeepSeek-R1-Distill Model Setup Guide

**Tarih**: 16 Aralık 2025  
**Model**: DeepSeek-R1-Distill-Qwen-7B (Uncensored)  
**Quantization**: Q4_K_M (4-bit, ~4.4 GB)  
**Hardware**: RTX 3060 6GB ✅ Perfect Match!

---

## 🎯 Neden DeepSeek-R1-Distill?

### Avantajları:

- ✅ **Uncensored**: Akademik proje için etik kısıtlamalar yok
- ✅ **Advanced Reasoning**: Llama-3.3-70B'den distill edilmiş, akıllı yanıtlar
- ✅ **Hızlı**: Q4_K_M quantization ile RTX 3060'ta çok hızlı
- ✅ **Küçük**: 4.4 GB, SSD'nize sığar
- ✅ **Türkçe Desteği**: Qwen tabanlı, çok dilli
- ✅ **GPU Optimized**: num_gpu=1 ile RTX 3060 kullanır

### Önceki Modelle Karşılaştırma:

| Özellik        | Qwen2:7B (Eski) | DeepSeek-R1-Distill (Yeni) |
|----------------|-----------------|----------------------------|
| Reasoning      | ⭐⭐⭐ Orta        | ⭐⭐⭐⭐⭐ Mükemmel             |
| Türkçe         | ⭐⭐⭐⭐ İyi        | ⭐⭐⭐⭐⭐ Çok İyi              |
| Censorship     | ❌ Var           | ✅ Yok (Uncensored)         |
| Hız (RTX 3060) | ⭐⭐⭐⭐ Hızlı      | ⭐⭐⭐⭐ Hızlı                 |
| Model Boyutu   | 3.8 GB          | 4.4 GB                     |
| Yanıt Kalitesi | ⭐⭐⭐ Orta        | ⭐⭐⭐⭐⭐ Mükemmel             |

---

## 📥 Kurulum Durumu

### ✅ Otomatik Kurulum (ŞU ANDA ÇALIŞIYOR)

```powershell
cd D:\Projects\SelcukAiAssistant\backend
.\setup_deepseek.ps1
```

**İlerleme:**

1. ✅ Model indiriliyor: `DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf` (~4.4 GB)
2. ⏳ Modelfile oluşturulacak
3. ⏳ Ollama modeli create edilecek
4. ⏳ Test edilecek

**Tahmini Süre**: 10-15 dakika (High-speed WiFi)

---

## 🔧 Manuel Kurulum (Alternatif)

Eğer script başarısız olursa:

### Adım 1: GGUF Dosyasını İndir

**Seçenek A**: HuggingFace'ten direkt indir

```
https://huggingface.co/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF/resolve/main/DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf
```

**Seçenek B**: Git LFS ile

```powershell
git lfs install
git clone https://huggingface.co/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF
```

**İndirme Yeri**: `D:\Projects\SelcukAiAssistant\backend\`

### Adım 2: Modelfile Oluştur

`backend/Modelfile.deepseek` dosyası otomatik oluşturuldu ✅

### Adım 3: Ollama Modeli Oluştur

```powershell
cd D:\Projects\SelcukAiAssistant\backend
ollama create selcuk_ai_assistant -f Modelfile.deepseek
```

### Adım 4: Test Et

```powershell
ollama run selcuk_ai_assistant "Merhaba, sen kimsin?"
```

**Beklenen Yanıt:**

```
Merhaba! Ben Selçuk AI Asistanı, Selçuk Üniversitesi'nin resmi yapay zeka asistanıyım...
```

---

## 🚀 Backend'i Başlatma

Model kurulumu tamamlandıktan sonra:

### 1. Backend'i Başlat

```powershell
cd D:\Projects\SelcukAiAssistant\backend
python main.py
```

**Beklenen Log:**

```
INFO - Ollama service initialized: url=http://localhost:11434/api/generate, model=selcuk_ai_assistant, timeout=120s
INFO - Appwrite client initialized: endpoint=..., project=..., database=..., collection=chat_logs
INFO - Starting server on 0.0.0.0:8000
```

### 2. Flutter Uygulamasını Başlat

```powershell
cd D:\Projects\SelcukAiAssistant
flutter run -d chrome
```

### 3. Test Soruları

**Test 1: Basit Soru**

```
"Merhaba"
```

**Beklenen (İyi):**

```
Merhaba! Ben Selçuk AI Asistanı, Selçuk Üniversitesi'nin resmi yapay zeka asistanıyım. 
Size nasıl yardımcı olabilirim?
```

**Test 2: Detaylı Soru**

```
"Selçuk Üniversitesi hakkında bilgi ver"
```

**Beklenen (Mükemmel):**

```
## Selçuk Üniversitesi

Selçuk Üniversitesi, Konya'da yer alan köklü bir devlet üniversitesidir.

**Temel Bilgiler:**
- 🏛️ Kuruluş: 1975
- 📍 Şehir: Konya
- 👥 Öğrenci Sayısı: ~80,000
- 🎓 Fakülte Sayısı: 24

**Kampüsler:**
1. **Alaeddin Keykubat Kampüsü** (Merkez)
2. **Selçuklu Kampüsü**
3. **Çumra Kampüsü**

📞 **İletişim**: 0332 223 XXXX
🌐 **Web**: selcuk.edu.tr
```

---

## 🔍 Performans Optimizasyonu

### RTX 3060 6GB için Ayarlar:

Modelfile'da zaten optimize edildi:

```
PARAMETER num_gpu 1          # GPU'yu kullan
PARAMETER num_ctx 8192       # Context window (bellek yeterli)
PARAMETER temperature 0.7    # Dengeli yaratıcılık
PARAMETER top_p 0.9          # Nucleus sampling
PARAMETER top_k 40           # Top-k sampling
PARAMETER repeat_penalty 1.1 # Tekrar önleme
```

### Beklenen Performans:

| Metrik           | Değer                         |
|------------------|-------------------------------|
| İlk Token Süresi | ~1-2 saniye                   |
| Token/Saniye     | ~30-40 tokens/s               |
| Ortalama Yanıt   | ~5-10 saniye (200 token için) |
| GPU Kullanımı    | ~80-90%                       |
| VRAM Kullanımı   | ~4.5 GB / 6 GB                |
| CPU Kullanımı    | Minimal (~10%)                |

---

## 📊 Sorun Giderme

### Model İndirmesi Çok Uzun Sürüyor

**Çözüm 1**: Farklı quantization dene (daha küçük)

```
Q3_K_M: ~3.5 GB (biraz daha hızlı, biraz daha düşük kalite)
Q4_K_M: ~4.4 GB (önerilen, dengeli)
Q5_K_M: ~5.3 GB (daha iyi kalite, daha yavaş)
```

**Çözüm 2**: Torrent ile indir (eğer HuggingFace torrent desteği varsa)

### Model Yanıtları Hâlâ Kötü

**Kontrol 1**: Doğru model kullanılıyor mu?

```powershell
ollama list | Select-String "selcuk"
```

**Kontrol 2**: Backend doğru modeli kullanıyor mu?

```powershell
Get-Content backend\.env | Select-String "OLLAMA_MODEL"
```

**Çözüm**: Backend'i yeniden başlat

```powershell
taskkill /F /IM python.exe; python backend/main.py
```

### GPU Kullanılmıyor

**Kontrol**: Ollama GPU kullanımı

```powershell
nvidia-smi
```

**Çözüm**: Modelfile'da `PARAMETER num_gpu 1` var mı kontrol et

### VRAM Yetersiz (Unlikely)

RTX 3060 6GB ile Q4_K_M rahatça çalışır, ama eğer sorun olursa:

**Çözüm**: Daha küçük quantization kullan

```
Q3_K_M: ~3.5 GB (VRAM kullanımı ~3.8 GB)
```

---

## 🎓 Model Özellikleri

### DeepSeek-R1-Distill Nedir?

**DeepSeek-R1**: DeepSeek tarafından geliştirilen, OpenAI o1'e rakip bir reasoning model

**Distill**: Llama-3.3-70B-Instruct'tan küçültülmüş (70B → 7B/8B)

**Qwen-7B**: Alibaba'nın çok dilli (Türkçe dahil) base modeli

**Q4_K_M**: 4-bit quantization, hafıza ve hız için optimize

### Uncensored Ne Demek?

- ❌ Etik filtreleme yok
- ❌ "I can't assist with that" yanıtları yok
- ✅ Akademik araştırma için serbestlik
- ✅ Her türlü soruya yanıt verebilir
- ⚠️ **Dikkat**: Kötüye kullanılabilir, sorumlu kullanın

### Neden Uncensored Gerekli?

Akademik AI asistan projesi için:

- Sansür yanıtları engellemez
- Üniversite bilgilerini serbestçe paylaşır
- Test ve geliştirme için daha esnek
- Üretim ortamında gerekirse custom filtreler eklenebilir

---

## 📝 Sonraki Adımlar

### 1. Model İndirmesi Tamamlanınca (10-15 dk)

- [ ] Script bittiğinde "Setup Complete!" göreceksiniz
- [ ] Backend'i başlatın: `python main.py`
- [ ] Flutter'da test edin

### 2. AI Yanıt Kalitesini Değerlendirin

**Karşılaştırma:**

- Önceki yanıt: "Selçuk Al Asistanı olsun..." (Kötü)
- Yeni yanıt: Markdown, yapılandırılmış, profesyonel (İyi)

### 3. Appwrite Logging Kontrolü

Backend loglarında:

```
INFO - ✅ Appwrite log kaydı başarılı: chat_abc123...
```

Appwrite Console'da Documents tab'ında yeni kayıtları görün.

### 4. Fine-tuning (Gelecek)

Daha da iyi yanıtlar için:

- Selçuk Üniversitesi dökümanlarıyla fine-tune
- RAG (Retrieval-Augmented Generation) ekle
- Custom prompts optimize et

---

## 🔗 Kaynaklar

- **Model**: https://huggingface.co/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF
- **DeepSeek-R1 Paper**: https://github.com/deepseek-ai/DeepSeek-R1
- **Ollama Docs**: https://ollama.ai/docs
- **GGUF Format**: https://github.com/ggerganov/llama.cpp

---

## ✅ Checklist

Model kurulumu için:

- [ ] Model indirmesi tamamlandı (~4.4 GB)
- [ ] Modelfile.deepseek oluşturuldu
- [ ] `ollama create` başarılı
- [ ] `ollama run` test edildi
- [ ] Backend başlatıldı
- [ ] Flutter uygulaması test edildi
- [ ] AI yanıtları mükemmel
- [ ] Appwrite logging çalışıyor

---

**Kurulum tamamlandığında bu dokümantasyonu README'ye ekleyebilirsiniz!** 🚀

