# Selçuk AI Akademik Asistan

[![Backend CI](https://github.com/esN2k/SelcukAiAssistant/actions/workflows/backend.yml/badge.svg?branch=main)](https://github.com/esN2k/SelcukAiAssistant/actions/workflows/backend.yml)
[![Flutter Build](https://github.com/esN2k/SelcukAiAssistant/actions/workflows/dart.yml/badge.svg?branch=main)](https://github.com/esN2k/SelcukAiAssistant/actions/workflows/dart.yml)
[![Ruff](https://img.shields.io/badge/ruff-enabled-2?logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)

Selçuk Üniversitesi “Bilgisayar Mühendisliği Uygulamaları” dersi için geliştirilen,
gizliliğe odaklı bir **yerel yapay zeka akademik asistan** projesidir. Sistem,
Google Gemini API kullanımından tamamen vazgeçmiş ve **yerel Ollama (Llama 3.1)**
altyapısına geçirilmiştir.

## Amaç
- Öğrenci, akademisyen ve idari personel için güvenilir akademik bilgi desteği sağlamak.
- Yerel LLM kullanımıyla veri gizliliğini korumak.
- RAG (Retrieval-Augmented Generation) ile kaynak gösteren yanıt üretmek.

## Proje Kimliği
- **Gizlilik (Privacy):** Veri işleme yerel LLM üzerinde yapılır, dış servis zorunlu değildir.
- **Yerel çıkarım (Local inference):** İnternet yokken bile temel sohbet akışı sürdürülür.
- **Kaynaklı yanıt (Citations):** RAG ile akademik doğrulanabilirlik artırılır.
- **Çoklu sağlayıcı (Multi‑provider):** Ollama ve HuggingFace (HF) aynı arayüzle yönetilir.
- **Kalite kapıları (Quality gates):** CI’da test ve kod kalitesi kontrolleri uygulanır.

## Teknoloji Yığını
- **Frontend:** Flutter + GetX (Material 3, çoklu platform)
- **Backend:** Python + FastAPI
- **Yerel LLM:** Ollama (Llama 3.1)
- **Yerel LLM (opsiyonel):** HuggingFace (HF, açık model deposu)
- **RAG:** LangChain (orchestrator), FAISS (vektör arama), ChromaDB (vektör DB)

## Sunum Özeti (Jüri için)
- **Gizlilik (Privacy):** Kullanıcı verisi yerel LLM’de işlenir; harici API bağımlılığı yoktur.
- **Yerel çıkarım (Local inference):** İnternet kesilse bile çekirdek sohbet akışı çalışır.
- **Kaynaklı yanıt (Citations):** RAG, yanıtı belge parçalarıyla ilişkilendirir.
- **Hata toleransı (Fault tolerance):** Ollama/RAG hataları Türkçe ve anlaşılır döner.
- **Kalite kapıları (Quality gates):** CI’da `pytest`, `ruff`, `mypy`, `flutter analyze/test`, encoding guard çalışır.
- **Akademik doğruluk (Academic accuracy):** Yerel veri ve kaynak gösterimi ile doğrulanabilir çıktı üretir.

## Mimari Özet
```
Flutter (UI) ──HTTP/SSE──> FastAPI ──> LLM (Ollama)
                         └──> RAG (FAISS + ChromaDB)
```
- **/chat** ve **/chat/stream** uçları ile istek/akış yanıtı.
- RAG açıksa, önce kaynak parçaları toplanır ve prompta eklenir.

## Çoklu Sağlayıcı Desteği (Sağlayıcı Deseni / Provider Pattern)
- Backend tarafında `providers/` katmanı ile Ollama ve HF aynı arayüzden çağrılır.
- `MODEL_BACKEND` alanı varsayılan sağlayıcıyı belirler.
- `/models` çıktısında uygunluk (availability) bilgisi sunulur.

## Hızlı Başlangıç
### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Flutter
```bash
flutter pub get
copy .env.example .env
flutter run
```

> Not: HuggingFace (HF) yerel model akışı opsiyoneldir. Windows’ta `torch_python.dll`
> hatası için `docs/SORUN_GIDERME.md` dosyasına bakın. HF offline/önbellek ayarları
> için `docs/MODELLER.md` ve `INSTALL.md` dosyalarını inceleyin.

## RAG Kullanımı
```bash
cd backend
python rag_ingest.py --input ../docs --output ./data/rag
```
Ardından `backend/.env` içinde:
```
RAG_ENABLED=true
RAG_VECTOR_DB_PATH=./data/rag
```

## Dokümantasyon
| Belge | Açıklama | Konum |
| --- | --- | --- |
| Sunum Notları | Jüri odaklı sunum akışı ve Soru‑Cevap hazırlığı | `docs/SUNUM_NOTLARI.md` |
| Test Raporu | CI/test çıktılarının akademik özeti | `docs/TEST_RAPORU.md` |
| Benchmark Raporu | Ollama hızlı ölçüm sonuçları | `docs/BENCHMARK_RAPORU.md` |
| LoRA Planı | İnce ayar stratejisi ve veri hazırlama | `docs/LORA_PLANI.md` |
| Veri Kaynakları | RAG veri toplama özeti | `docs/VERI_KAYNAKLARI.md` |
| Kurulum Rehberi | Platform bazlı kurulum adımları | `INSTALL.md` |
| Mimari (Özet) | Yüksek seviye mimari | `ARCHITECTURE.md` |
| Mimari (Detay) | RAG ve provider akışları | `docs/ARCHITECTURE.md` |
| RAG Rehberi | İndeksleme ve ayarlar | `docs/RAG.md` |
| Modeller | Ollama/HF/API model notları | `docs/MODELLER.md` |
| Dağıtım | Yerel/Docker dağıtım | `docs/DAGITIM.md` |
| Sorun Giderme | Yaygın hata ve çözümler | `docs/SORUN_GIDERME.md` |
| API Sözleşmesi | Endpoint ve şema detayları | `docs/API_CONTRACT.md` |
| Yol Haritası | Gelişim planı | `docs/YOL_HARITASI.md` |
| Sürüm Kontrol Listesi | Kalite kapıları | `docs/SURUM_KONTROL_LISTESI.md` |

## Test / Kalite Kapıları
Backend:
- `python -m pytest -q`
- `ruff check .`
- `mypy .`

Flutter:
- `flutter analyze`
- `flutter test`

Smoke test (backend çalışırken):
- `tools/test_api.ps1`
- `tools/smoke_test.ps1`
