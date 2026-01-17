# Selçuk AI Asistanı

Selçuk Üniversitesi için geliştirilmiş, **tamamen Türkçe** konuşan ve öğrencilerin akademik süreçlerinde yardımcı olan bir yapay zeka asistanıdır. Proje öğrenci düzeyinde anlaşılır olacak şekilde tasarlanmıştır.

## Amaç
- Öğrenci, akademisyen ve idari personel için doğru ve sade bilgi sunmak
- Yerel LLM kullanımıyla veri gizliliğini korumak
- RAG (Geri Getirim Destekli Üretim) ile kaynaklı yanıt üretmek

## Öne Çıkan Özellikler
- %100 Türkçe kullanıcı arayüzü ve hata mesajları
- Merkezi hata yönetimi (backend + Flutter)
- Yerel Ollama modeli ile çalışma
- İsteğe bağlı HuggingFace desteği
- RAG ile kaynak gösterme

## Mimari Özet
```
Flutter (UI) ──HTTP/SSE──> FastAPI ──> Ollama / HF
                         └──> RAG (FAISS)
```

## Hızlı Kurulum
### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Flutter
```bash
flutter pub get
flutter run
```

## Önemli Notlar
- `OLLAMA_MODEL` değeri sistemde bulunan modele göre ayarlanmalıdır.
- RAG kullanımı için `RAG_VECTOR_DB_PATH` zorunludur.

## Dokümantasyon
- `docs/BASLANGIC_REHBERI.md`
- `docs/PROJE_YAPISI.md`
- `docs/HATA_COZUMLEME.md`
- `docs/KOD_STANDARTLARI.md`
- `docs/API_DOKUMANTASYONU.md`

## Model Geliştirme Scriptleri
- `backend/scripts/model_evaluation.py`
- `backend/scripts/prepare_selcuk_dataset.py`
- `backend/scripts/finetune_model.py`
- `backend/scripts/benchmark_models.py`

## Lisans
Bu proje eğitim amaçlı hazırlanmıştır.
