# Hata Çözümleme

Bu bölümde sık karşılaşılan hatalar ve pratik çözümleri listelenmiştir.

## 1) Ollama Bağlantı Hatası
**Belirti:** API yanıtı `Ollama servisine bağlanılamadı`.

**Çözüm:**
- Ollama servisinin çalıştığından emin olun: `ollama list`
- `OLLAMA_BASE_URL` değerini kontrol edin.
- Gerekirse Ollama servisini yeniden başlatın.

## 2) Model Bulunamadı
**Belirti:** `Bilinmeyen model sağlayıcısı` veya `model bulunamadı`.

**Çözüm:**
- `.env` içindeki `OLLAMA_MODEL` değerini kontrol edin.
- `ollama pull <model>` ile modeli indirin.
- Model adını `/models` endpoint çıktısı ile doğrulayın.

## 3) RAG Servisi Hazır Değil
**Belirti:** `Bilgi tabanı servisi hazır değil`.

**Çözüm:**
- `RAG_ENABLED=true` ise `RAG_VECTOR_DB_PATH` mutlaka tanımlı olmalı.
- `backend/rag_ingest.py` ile indeks oluşturun.

## 4) Port Çakışması
**Belirti:** `Address already in use`.

**Çözüm:**
- 8000 portunu kullanan uygulamayı kapatın.
- Alternatif portla çalıştırın: `uvicorn main:app --port 8010`

## 5) HuggingFace Bağımlılık Hatası
**Belirti:** `HuggingFace bağımlılıkları eksik`.

**Çözüm:**
- `backend/requirements-hf.txt` paketlerini kurun.
- GPU yoksa `HF_DEVICE=cpu` deneyin.

## 6) Flutter Cihaz Bağlantısı
**Belirti:** Mobilde backend'e erişilemiyor.

**Çözüm:**
- Android emulator için `http://10.0.2.2:8000` kullanın.
- iOS simulator için `http://127.0.0.1:8000` kullanın.
- Gerçek cihazda aynı ağdaki IP adresini girin.

## 7) Çeviri Hatası
**Belirti:** `Çeviri başarısız oldu`.

**Çözüm:**
- Backend çalışıyor mu kontrol edin.
- Çeviri modeli için yeterli bellek olduğundan emin olun.
- Gerekirse `TRANSLATE_MODEL_NAME` değerini güncelleyin.
