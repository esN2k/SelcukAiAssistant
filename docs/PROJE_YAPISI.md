# Proje Yapısı

Bu belge, klasör ve dosyaların ne işe yaradığını kısa ve anlaşılır şekilde açıklar.

## Üst Seviye Klasörler
```
repo/
  lib/                # Flutter uygulaması (arayüz)
  backend/            # FastAPI arka uç (API, RAG, modeller)
  docs/               # Dokümantasyon ve raporlar
  assets/             # Görseller, lottie ve statik dosyalar
  test/               # Flutter testleri
  tools/              # Yardımcı scriptler
  data/               # Örnek veri ve çıktı dosyaları
```

## Flutter (lib/)
- `screen/`: Ekranlar (splash, ayarlar, sohbet vb.)
- `controller/`: State yönetimi ve akış kontrolü
- `services/`: API çağrıları, SSE bağlantısı, depolama
- `core/errors/`: Hata sınıfları ve mesajları
- `l10n/`: Çoklu dil dosyaları (Türkçe ana dil)
- `model/`: Veri modelleri

## Backend (backend/)
- `main.py`: FastAPI ana giriş noktası
- `api/`: Endpoint tanımları
- `providers/`: Model sağlayıcıları (Ollama, HuggingFace)
- `rag_service.py`: RAG bağlam üretimi
- `error_handlers.py`: Merkezi hata yönetimi
- `exceptions.py`: Özel exception sınıfları
- `scripts/`: Model değerlendirme ve eğitim scriptleri
- `data/`: RAG ve eğitim verileri

## Dokümantasyon (docs/)
- `BASLANGIC_REHBERI.md`: Kurulum ve çalıştırma adımları
- `PROJE_YAPISI.md`: Bu dosya
- `HATA_COZUMLEME.md`: Yaygın hatalar ve çözümler
- `KOD_STANDARTLARI.md`: Kodlama kuralları
- `API_DOKUMANTASYONU.md`: API uç noktaları ve örnekler
