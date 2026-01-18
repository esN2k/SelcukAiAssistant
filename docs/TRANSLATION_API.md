# 🌐 Translation API Documentation

TranslateGemma-4B ile çok dilli çeviri API'si.

## Genel Bilgiler

**Model:** `google/translategemma-4b-it`  
**Parametre:** 4 Milyar  
**VRAM:** ~2GB (4-bit quantized)  
**Performans:** 400-600ms (RTX 3060)

### Desteklenen Diller

| Kod | Dil | Örnek |
|-----|-----|-------|
| `tr` | Türkçe | Merhaba dünya |
| `en` | İngilizce | Hello world |
| `ar` | Arapça | مرحبا بالعالم |
| `fa` | Farsça | سلام دنیا |
| `de` | Almanca | Hallo Welt |
| `ru` | Rusça | Привет мир |

---

## Endpoints

### 1. Tekil Çeviri

**Endpoint:** `POST /api/translate`

Bir metni kaynak dilden hedef dile çevirir.

#### Request

```bash
curl -X POST "http://localhost:8000/api/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Selçuk Üniversitesi Konya'\''da bulunmaktadır.",
    "source_lang": "tr",
    "target_lang": "en",
    "num_beams": 4
  }'
```

#### Request Parametreleri

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `text` | string | ✅ | - | Çevrilecek metin (max 2048 karakter) |
| `source_lang` | string | ❌ | `"auto"` | Kaynak dil kodu (`auto`/`tr`/`en`/`ar`/`fa`/`de`/`ru`) |
| `target_lang` | string | ❌ | `"tr"` | Hedef dil kodu |
| `num_beams` | int | ❌ | `4` | Beam search sayısı (1-8). 1=hızlı, 4=kaliteli |

#### Response

```json
{
  "original": "Selçuk Üniversitesi Konya'da bulunmaktadır.",
  "translated": "Selcuk University is located in Konya.",
  "source_lang": "tr",
  "target_lang": "en",
  "inference_time_ms": 520,
  "model_info": {
    "model_name": "google/translategemma-4b-it",
    "device": "cuda",
    "vram_usage_gb": 1.98,
    "max_vram_gb": 2.15,
    "quantization": "4-bit NF4",
    "supported_languages": ["tr", "en", "ar", "fa", "de", "ru"],
    "loaded": true
  }
}
```

---

### 2. Toplu Çeviri (Batch)

**Endpoint:** `POST /api/translate/batch`

Birden fazla metni aynı anda çevirir. Performans avantajı sağlar.

#### Request

```bash
curl -X POST "http://localhost:8000/api/translate/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Hello world",
      "How are you?",
      "Good morning"
    ],
    "source_lang": "en",
    "target_lang": "tr"
  }'
```

#### Request Parametreleri

| Parametre | Tip | Zorunlu | Açıklama |
|-----------|-----|---------|----------|
| `texts` | array[string] | ✅ | Çevrilecek metinler (max 10) |
| `source_lang` | string | ✅ | Kaynak dil kodu |
| `target_lang` | string | ✅ | Hedef dil kodu |

#### Response

```json
{
  "translations": [
    {"original": "Hello world", "translated": "Merhaba dünya"},
    {"original": "How are you?", "translated": "Nasılsınız?"},
    {"original": "Good morning", "translated": "Günaydın"}
  ],
  "total_time_ms": 1450,
  "model_info": {
    "model_name": "google/translategemma-4b-it",
    "device": "cuda",
    "vram_usage_gb": 1.98,
    "quantization": "4-bit NF4",
    "supported_languages": ["tr", "en", "ar", "fa", "de", "ru"],
    "loaded": true
  }
}
```

---

### 3. Model Bilgileri

**Endpoint:** `GET /api/translate/info`

Çeviri modelinin durumu ve istatistiklerini döndürür.

#### Request

```bash
curl -X GET "http://localhost:8000/api/translate/info"
```

#### Response

```json
{
  "model_name": "google/translategemma-4b-it",
  "device": "cuda",
  "vram_usage_gb": 1.98,
  "max_vram_gb": 2.15,
  "quantization": "4-bit NF4",
  "supported_languages": ["tr", "en", "ar", "fa", "de", "ru"],
  "loaded": true
}
```

---

## Hata Kodları

| Kod | Açıklama | Örnek |
|-----|----------|-------|
| `400` | Geçersiz istek (yanlış dil kodu vb.) | `{"detail": "Desteklenmeyen kaynak dil: xyz"}` |
| `500` | Sunucu hatası (model yüklenemedi vb.) | `{"detail": "Çeviri hatası: ..."}` |
| `503` | Servis kullanılamıyor | `{"detail": "Çeviri servisi kullanılamıyor..."}` |

---

## Performans Benchmarks

### RTX 3060 (6GB VRAM)

| Dil Çifti | Ortalama Süre | Min | Max |
|-----------|---------------|-----|-----|
| TR → EN | 480ms | 420ms | 550ms |
| EN → TR | 510ms | 450ms | 580ms |
| AR → TR | 620ms | 550ms | 700ms |
| FA → TR | 590ms | 520ms | 670ms |
| DE → TR | 530ms | 470ms | 600ms |
| RU → TR | 580ms | 510ms | 660ms |

**VRAM Kullanımı:** ~2GB (4-bit quantization)

### Batch vs Tekil Karşılaştırma

| Yöntem | 10 Çeviri | Avantaj |
|--------|-----------|---------|
| Tekil (10 istek) | ~5000ms | - |
| Batch (1 istek) | ~1800ms | **3x hızlı** |

---

## Otomatik Dil Algılama

`source_lang: "auto"` parametresi kullanıldığında, sistem basit karakter analizi ile dili algılar:

- **Türkçe:** `ç, ğ, ı, ö, ş, ü` karakterleri
- **Arapça:** Unicode U+0600-U+06FF aralığı
- **Farsça:** Arapça + `پ, چ, ژ, گ, ک` karakterleri
- **Rusça:** Kiril alfabesi (U+0400-U+04FF)
- **Almanca:** `ä, ö, ü, ß` karakterleri
- **İngilizce:** Varsayılan (diğerleri eşleşmezse)

---

## Troubleshooting

### Model Yüklenmiyor

**Hata:** `TranslateGemma bağımlılıkları eksik`

**Çözüm:**
```bash
pip install torch transformers bitsandbytes accelerate sentencepiece
```

### CUDA Hatası

**Hata:** `CUDA out of memory`

**Çözüm:**
1. 4-bit quantization etkin olduğundan emin olun
2. Diğer GPU uygulamalarını kapatın
3. Batch boyutunu azaltın

### HuggingFace Token Hatası

**Hata:** `401 Unauthorized`

**Çözüm:**
1. `.env` dosyasında `HF_TOKEN` ayarlayın
2. Token'ın geçerli olduğunu kontrol edin
3. Model erişim iznini HuggingFace'de onaylayın

### Yavaş Performans

**Olası Nedenler:**
1. CPU üzerinde çalışıyor (GPU yerine)
2. 4-bit quantization kapalı
3. Flash Attention 2 yok

**Kontrol:**
```bash
curl http://localhost:8000/api/translate/info
```

`device: "cuda"` olmalı.

---

## Örnek Kullanım (Python)

```python
import requests

# Tekil çeviri
response = requests.post(
    "http://localhost:8000/api/translate",
    json={
        "text": "Merhaba, nasılsınız?",
        "source_lang": "tr",
        "target_lang": "en"
    }
)
print(response.json()["translated"])
# Output: Hello, how are you?

# Toplu çeviri
response = requests.post(
    "http://localhost:8000/api/translate/batch",
    json={
        "texts": ["Hello", "World", "Python"],
        "source_lang": "en",
        "target_lang": "tr"
    }
)
for item in response.json()["translations"]:
    print(f"{item['original']} → {item['translated']}")
```

---

## Swagger UI

API dokümantasyonunu interaktif olarak keşfetmek için:

```
http://localhost:8000/docs
```

veya ReDoc formatında:

```
http://localhost:8000/redoc
```
