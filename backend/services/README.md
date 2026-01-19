# Services Klasörü

## 📁 İçerik

Bu klasör, backend uygulamasının iş mantığını içeren servis modüllerini barındırır.

## 📄 Dosyalar

### `translator.py` ⭐ YENİ
**Amaç:** Helsinki-NLP Opus-MT ile Türkçe ↔ İngilizce çeviri  
**Ana Sınıf:** `Translator`  
**Modeller:** 
- TR→EN: Helsinki-NLP/opus-mt-tr-en
- EN→TR: Helsinki-NLP/opus-mt-en-tr

**Özellikler:**
- Çift yönlü çeviri (Turkish ↔ English)
- Akademik terim sözlüğü (glossary)
- Batch çeviri desteği
- LRU cache (1000 cümle)
- < 200ms hedef performans

**Kullanım:**
```python
from services.translator import translator

# Türkçe → İngilizce
result = translator.translate(
    "Selçuk Üniversitesi Konya'dadır",
    source_lang="tr",
    target_lang="en"
)
print(result)  # "Selcuk University is in Konya"

# Batch çeviri
results = translator.translate_batch(
    ["Merhaba", "Nasılsın?"],
    source_lang="tr",
    target_lang="en"
)
```

**Performans:**
- Tek cümle: ~150ms (CPU), ~50ms (GPU)
- Batch (10): ~800ms (CPU), ~300ms (GPU)
- Cache hit: < 1ms

---

## 🔗 İlişkiler

```
translator.py
    ↓ kullanır
translation_glossary.json (data/)
    ↓ sağlar
Akademik terim çevirileri
    ↓ kullanılır
API endpoints (api/endpoints/translate.py)
```

---

## 📊 Servis Mimarisi

```
┌─────────────────────────────────────┐
│  API Endpoint (/api/translate)      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Translator Service                 │
│  ┌───────────────────────────────┐  │
│  │ Helsinki-NLP Opus-MT Models   │  │
│  │ • TR→EN (opus-mt-tr-en)       │  │
│  │ • EN→TR (opus-mt-en-tr)       │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ Glossary (Akademik Terimler)  │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ LRU Cache (1000 entries)      │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## 🧪 Test Coverage

| Test Dosyası | Coverage | Durum |
|--------------|----------|-------|
| `tests/test_translator.py` | 95% | ✅ Kapsamlı |

**Test Kategorileri:**
- ✅ Temel çeviri (TR↔EN)
- ✅ Akademik terim koruması
- ✅ Batch çeviri
- ✅ Özel isim koruması (Selçuk, Konya)
- ✅ Performans (<200ms)
- ✅ Hata yönetimi
- ✅ Cache etkinliği

---

## 🚀 Gelecek Geliştirmeler

1. **Çoklu Dil Desteği:** Arapça, Farsça eklenmesi
2. **Fine-tuning:** Selçuk Üniversitesi spesifik dataset ile
3. **Streaming Translation:** Uzun metinler için
4. **Quality Metrics:** BLEU, METEOR skorları

---

## 📚 Kaynaklar

- [Helsinki-NLP Opus-MT](https://github.com/Helsinki-NLP/Opus-MT)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [MarianMT Documentation](https://huggingface.co/docs/transformers/model_doc/marian)
