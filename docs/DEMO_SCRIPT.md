# Selçuk AI Asistanı - Jüri Demo Senaryosu

## 🎯 Demo Hedefi
Projenin doğruluğunu, güvenilirliğini ve teknik kalitesini göstermek.

## ⏱️ Süre
Toplam: 5-7 dakika

## 📋 Ön Hazırlık

### Gereksinimler
1. ✅ Backend çalışıyor (`http://localhost:8000`)
2. ✅ Ollama kurulu ve model hazır (`llama3.2:3b` veya `turkcell-llm-7b`)
3. ✅ RAG indeksi mevcut (`backend/data/rag/index.faiss`)
4. ✅ Terminal/curl veya Postman hazır
5. ✅ (Opsiyonel) Flutter app çalışıyor

### Başlatma Komutları
```bash
# Terminal 1: Backend başlat
cd backend
python main.py

# Terminal 2: (Opsiyonel) Flutter app
flutter run -d chrome
```

---

## 🎬 Demo Akışı

### 1. Sağlık Kontrolü (30 saniye)

**Amaç:** Sistemin çalıştığını göstermek

```bash
curl http://localhost:8000/health
```

**Beklenen Çıktı:**
```json
{
  "status": "ok",
  "message": "Selçuk AI Asistanı backend çalışıyor"
}
```

**Açıklama:** Backend sağlıklı ve hazır durumda.

---

### 2. Model Listesi (30 saniye)

**Amaç:** Kullanılabilir modelleri göstermek

```bash
curl http://localhost:8000/models
```

**Beklenen Çıktı (örnek):**
```json
{
  "models": [
    {
      "id": "ollama:llama3.2:3b",
      "provider": "ollama",
      "display_name": "Llama 3.2 3B",
      "local_or_remote": "local",
      "available": true,
      "context_length": 4096
    }
  ]
}
```

**Açıklama:** Yerel LLM kullanımı - veri gizliliği garantisi.

---

### 3. ⭐ KRİTİK TEST: Konum Sorusu (1.5 dakika)

**Amaç:** Kritik doğruluk garantisini göstermek

#### 3a. Doğru Yanıt Testi

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Selçuk Üniversitesi nerede?"
      }
    ],
    "model": "ollama:llama3.2:3b",
    "rag_enabled": true,
    "rag_strict": true,
    "temperature": 0.1
  }'
```

**Beklenen Anahtar Kelimeler:**
- ✅ **"Konya"** (MUTLAKA olmalı)
- ✅ Alaeddin Keykubat veya Ardıçlı Kampüsü
- ✅ 1975 kuruluş yılı
- ❌ İzmir, Ankara, İstanbul (olmamalı)

**Demo Vurgusu:**
> "Görüldüğü üzere, sistem 'Konya' bilgisini doğru şekilde veriyor. Backend'de `accuracy_guard.py` modülü sayesinde, yanlış şehir bilgisi (örn. İzmir) verilse bile otomatik olarak düzeltiliyor."

---

### 4. RAG Strict Mode Testi (1 dakika)

**Amaç:** Kaynak olmadığında net davranış

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Selçuk Üniversitesinde kaç tane roket var?"
      }
    ],
    "model": "ollama:llama3.2:3b",
    "rag_enabled": true,
    "rag_strict": true,
    "temperature": 0.1
  }'
```

**Beklenen Çıktı:**
```
"Bu bilgi kaynaklarda yok."
```

**Demo Vurgusu:**
> "RAG strict mode aktifken, kaynaklarda olmayan bilgiler için uydurma yapmıyor, açıkça 'Bu bilgi kaynaklarda yok' diyor."

---

### 5. RAG Kaynaklı Yanıt (1.5 dakika)

**Amaç:** RAG sisteminin çalıştığını göstermek

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Bilgisayar Mühendisliği bölümü hangi fakültede?"
      }
    ],
    "model": "ollama:llama3.2:3b",
    "rag_enabled": true,
    "rag_strict": true,
    "temperature": 0.1
  }'
```

**Beklenen Anahtar Kelimeler:**
- ✅ "Teknoloji Fakültesi"
- ✅ Alaeddin Keykubat Yerleşkesi
- ✅ MÜDEK akreditasyonu
- ✅ `citations` alanında kaynak bilgisi

**Demo Vurgusu:**
> "RAG sistemi, `backend/data/rag/` altındaki FAISS indeksinden ilgili bilgileri getiriyor. Response'ta `citations` alanında kaynak bilgileri de dönüyor."

---

### 6. Stream Yanıtı (1 dakika) - Opsiyonel

**Amaç:** Gerçek zamanlı akış göstermek

```bash
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Selçuk Üniversitesi kaç yılında kuruldu?"
      }
    ],
    "model": "ollama:llama3.2:3b",
    "rag_enabled": true,
    "temperature": 0.1
  }'
```

**Beklenen Davranış:**
- Token token yanıt akışı (SSE formatında)
- "1975" bilgisi doğru şekilde verilmeli
- Stream bitiminde `citations` ve `usage` bilgisi

**Demo Vurgusu:**
> "Streaming endpoint'i sayesinde kullanıcı yanıtı anlık görebiliyor. Accuracy guard burada da aktif."

---

### 7. Kuruluş Yılı Testi (1 dakika)

**Amaç:** Başka bir kritik bilgiyi doğrulamak

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Selçuk Üniversitesi ne zaman kuruldu?"
      }
    ],
    "model": "ollama:llama3.2:3b",
    "rag_enabled": true,
    "temperature": 0.1
  }'
```

**Beklenen Anahtar Kelimeler:**
- ✅ "1975"
- ❌ 1982, 1976, 1974 (yanlış yıllar olmamalı)

---

## 🎓 Demo Sonrası Açıklamalar

### Teknik Vurgular
1. **Doğruluk Garantisi:**
   - `accuracy_guard.py` modülü ile kritik bilgiler korunuyor
   - Yanlış bilgi tespit edilirse otomatik düzeltme
   - Log'larda `accuracy_guard_corrected` eventi

2. **RAG Sistemi:**
   - FAISS indeks ile hızlı vektör araması
   - Multilingual embedding model (paraphrase-multilingual-MiniLM-L12-v2)
   - Chunk size: 500, overlap: 50
   - Top-K: 4 kaynak

3. **Gizlilik:**
   - Tüm işlem yerel (Ollama)
   - Dış API çağrısı yok
   - Veri üniversiteden çıkmıyor

4. **Kalite Kontrolleri:**
   - Unit testler: `test_accuracy_guard.py`, `test_critical_facts.py`
   - Validation: `validate_knowledge.py`
   - Encoding guard: `tools/encoding_guard.py`

### Jüri Soruları İçin Hazırlık

**S: Yanlış bilgi verilme riski nedir?**
> A: `accuracy_guard.py` modülü ile kritik sorular (konum, kuruluş yılı) için otomatik doğrulama yapılıyor. Yanlış bilgi tespit edilirse, model cevabı ne olursa olsun, doğru bilgiyle değiştiriliyor.

**S: RAG kaynaklarını nasıl güncelliyorsunuz?**
> A: `backend/rag_ingest.py` script'i ile JSON ve scraped veriler indeksleniyor. `backend/data/rag/` altında FAISS index ve metadata tutuluyor.

**S: Neden Ollama kullandınız?**
> A: Gizlilik ve veri güvenliği için yerel LLM şart. Ollama kolay kurulum ve çoklu model desteği sunuyor. Production'da Turkcell LLM veya fine-tune edilmiş model kullanılabilir.

**S: Test coverage nedir?**
> A: Backend için 50+ test var. Kritik bilgiler için özel testler: `test_critical_facts.py` (10 test), `test_accuracy_guard.py` (20+ test), `validate_knowledge.py` (10 kontrol).

---

## 📸 Ekran Görüntüleri Önerileri

1. ✅ Sağlık kontrolü başarılı
2. ✅ Model listesi (yerel model vurgusu)
3. ✅ "Selçuk Üniversitesi nerede?" sorusuna Konya cevabı
4. ✅ RAG strict mode - "Bu bilgi kaynaklarda yok" mesajı
5. ✅ Citations ile kaynak gösterimi
6. ✅ Backend log'larında accuracy_guard uyarısı
7. ✅ Test sonuçları (`pytest -v`)
8. ✅ Encoding guard temiz raporu

---

## ✅ Demo Sonrası Kontrol Listesi

- [ ] Tüm testler başarılı geçti
- [ ] "Konya" bilgisi doğru verildi
- [ ] RAG strict mode çalıştı
- [ ] Citations gösterildi
- [ ] Accuracy guard log'u kaydedildi
- [ ] Yanlış bilgi düzeltme test edildi (manuel test ile)

---

## 🚨 Sorun Giderme

### Backend başlamıyor
```bash
# .env dosyasını kontrol et
cat backend/.env

# Port kullanımda mı?
lsof -i :8000

# Farklı port dene
PORT=8001 python main.py
```

### Ollama model yok
```bash
# Model çek
ollama pull llama3.2:3b

# Mevcut modelleri listele
ollama list
```

### RAG çalışmıyor
```bash
# Index var mı?
ls -la backend/data/rag/index.faiss

# RAG etkin mi?
grep RAG_ENABLED backend/.env

# Index yeniden oluştur
cd backend
python rag_ingest.py
```

---

## 📚 Ek Kaynaklar

- `docs/JURI_HAZIRLIK.md` - Jüri hazırlık kontrol listesi
- `docs/QA_PREP.md` - Jüri soruları ve cevapları
- `README.md` - Proje genel bakış
- `INSTALL.md` - Kurulum kılavuzu
- `ARCHITECTURE.md` - Mimari açıklama
