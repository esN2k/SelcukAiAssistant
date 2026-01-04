# Selçuk AI Akademik Asistan

[![Arka uç CI](https://github.com/esN2k/SelcukAiAssistant/actions/workflows/backend.yml/badge.svg?branch=main)](https://github.com/esN2k/SelcukAiAssistant/actions/workflows/backend.yml)
[![Flutter Derleme](https://github.com/esN2k/SelcukAiAssistant/actions/workflows/dart.yml/badge.svg?branch=main)](https://github.com/esN2k/SelcukAiAssistant/actions/workflows/dart.yml)
[![Ruff](https://img.shields.io/badge/ruff-enabled-2?logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)

Selçuk Üniversitesi “Bilgisayar Mühendisliği Uygulamaları” dersi için geliştirilen,
gizliliğe odaklı bir **yerel yapay zeka akademik asistan** projesidir. Sistem,
Google Gemini API kullanımından tamamen vazgeçmiş ve **yerel Ollama (Llama 3.1)**
altyapısına geçirilmiştir.

> 🎓 **Jüri Sunumuna Hazırlık:** [docs/presentation/JURI_HAZIRLIK.md](docs/presentation/JURI_HAZIRLIK.md) dosyasında sunum kontrol listesi ve gösterim senaryoları bulunmaktadır.

## Amaç
- Öğrenci, akademisyen ve idari personel için güvenilir akademik bilgi desteği sağlamak.
- Yerel LLM kullanımıyla veri gizliliğini korumak.
- RAG (Geri Getirim Destekli Üretim) ile kaynak gösteren yanıt üretmek.

## Proje Kimliği
- **Gizlilik:** Veri işleme yerel LLM üzerinde yapılır, dış servis zorunlu değildir.
- **Yerel çıkarım:** İnternet yokken bile temel sohbet akışı sürdürülür.
- **Kaynaklı yanıt (atıf):** RAG ile akademik doğrulanabilirlik artırılır.
- **Çoklu sağlayıcı:** Ollama ve HuggingFace (HF) aynı arayüzle yönetilir.
- **Kalite kapıları:** CI'da test ve kod kalitesi kontrolleri uygulanır.

## Teknoloji Yığını
- **Ön uç:** Flutter + GetX (Material 3, çoklu platform)
- **Arka uç:** Python + FastAPI
- **Yerel LLM:** Ollama (Llama 3.1)
- **Yerel LLM (opsiyonel):** HuggingFace (HF, açık model deposu)
- **RAG:** LangChain (orkestrasyon), FAISS (vektör arama), ChromaDB (vektör veritabanı)

## Sunum Özeti (Jüri için)
- **Gizlilik:** Kullanıcı verisi yerel LLM'de işlenir; harici API bağımlılığı yoktur.
- **Yerel çıkarım:** İnternet kesilse bile çekirdek sohbet akışı çalışır.
- **Kaynaklı yanıt (atıf):** RAG, yanıtı belge parçalarıyla ilişkilendirir.
- **Hata toleransı:** Ollama/RAG hataları Türkçe ve anlaşılır döner.
- **Kalite kapıları:** CI'da `pytest`, `ruff`, `mypy`, `flutter analyze/test`, encoding guard çalışır.
- **Akademik doğruluk:** Yerel veri ve kaynak gösterimi ile doğrulanabilir çıktı üretir.

## Mimari Özet
```
Flutter (arayüz) ──HTTP/SSE──> FastAPI ──> LLM (Ollama)
                         └──> RAG (FAISS + ChromaDB)
```
- **/chat** ve **/chat/stream** uç noktaları ile istek/akış yanıtı.
- RAG açıksa, önce kaynak parçaları toplanır ve isteme eklenir.

## Çoklu Sağlayıcı Desteği (Sağlayıcı Deseni)
- Arka uç tarafında `providers/` katmanı ile Ollama ve HF aynı arayüzden çağrılır.
- `MODEL_BACKEND` alanı varsayılan sağlayıcıyı belirler.
- `/models` çıktısında uygunluk (kullanılabilirlik) bilgisi sunulur.

## Hızlı Başlangıç
### Arka Uç
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Ön Uç (Flutter)
```bash
flutter pub get
copy .env.example .env
flutter run
```

> Not: HuggingFace (HF) yerel model akışı opsiyoneldir. Windows'ta `torch_python.dll`
> hatası için `docs/ops/SORUN_GIDERME.md` dosyasına bakın. HF çevrimdışı/önbellek ayarları
> için `docs/technical/MODELLER.md` ve `INSTALL.md` dosyalarını inceleyin.

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
| **Jüri Hazırlık** | **Sunum hazırlık kontrol listesi ve öneriler** | **`docs/presentation/JURI_HAZIRLIK.md`** |
| Sunum Notları | Jüri odaklı sunum akışı ve Soru‑Cevap hazırlığı | `docs/presentation/final_raporu/SPEAKER_NOTES.md` |
| Test Raporu | CI/test çıktılarının akademik özeti | `docs/reports/TEST_RAPORU.md` |
| Kıyaslama Raporu | Ollama hızlı ölçüm sonuçları | `docs/reports/BENCHMARK_RAPORU.md` |
| İnce Ayar Raporu | İnce ayar ve veri hazırlama özeti | `docs/reports/FINE_TUNING_REPORT.md` |
| Veri Kaynakları | RAG veri toplama özeti | `docs/reports/VERI_KAYNAKLARI.md` |
| Kurulum Rehberi | Platform bazlı kurulum adımları | `INSTALL.md` |
| Katkıda Bulunanlar | Proje ekibi ve teşekkürler | `CONTRIBUTORS.md` |
| Mimari (Özet) | Yüksek seviye mimari | `docs/technical/ARCHITECTURE_OVERVIEW.md` |
| Mimari (Detay) | RAG ve sağlayıcı akışları | `docs/technical/ARCHITECTURE.md` |
| RAG Rehberi | İndeksleme ve ayarlar | `docs/technical/RAG.md` |
| Modeller | Ollama/HF/API model notları | `docs/technical/MODELLER.md` |
| Dağıtım | Yerel/Docker dağıtım | `docs/ops/DAGITIM.md` |
| Sorun Giderme | Yaygın hata ve çözümler | `docs/ops/SORUN_GIDERME.md` |
| API Sözleşmesi | Uç nokta ve şema detayları | `docs/technical/API_CONTRACT.md` |

## Test / Kalite Kapıları
Arka Uç:
- `python -m pytest -q`
- `ruff check .`
- `mypy .`

Ön Uç (Flutter):
- `flutter analyze`
- `flutter test`

Duman testi (arka uç çalışırken):
- `tools/test_api.ps1`
- `tools/smoke_test.ps1`

## Lisans
Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## Katkıda Bulunanlar
Katkıda bulunanlar listesi ve teşekkürler için [CONTRIBUTORS.md](CONTRIBUTORS.md) dosyasına bakın.
