# Selçuk AI Asistanı - Teslim ve Kurulum Notları

Bu proje, Selçuk Üniversitesi için geliştirilmiş, RAG destekli bir yapay zeka asistanıdır.

## Sürüm Bilgisi
**Tarih:** 17.01.2026
**Backend Sürümü:** v1.0.2
**Frontend Sürümü:** v1.0.2+2

## Sistem Gereksinimleri
- **İşletim Sistemi:** Windows 10/11, Linux (Ubuntu 22.04+), macOS
- **Backend:** Python 3.10+
- **Frontend:** Flutter SDK 3.22+
- **Yapay Zeka:** Ollama (yerel model için) ve en az 8GB RAM (16GB önerilir)

## Kurulum Adımları

### 1. Backend (Sunucu) Kurulumu
Backend klasörüne gidin ve gerekli paketleri yükleyin:

```bash
cd backend
# Sanal ortam oluşturma (Önerilen)
python -m venv .venv

# Windows için sanal ortamı aktif etme
.venv\Scripts\activate

# Linux/Mac için sanal ortamı aktif etme
source .venv/bin/activate

# Bağımlılıkları yükleme
pip install -r requirements.txt
```

**Önemli:** `.env` dosyasının oluşturulduğundan ve `OLLAMA_MODEL` gibi ayarların yapıldığından emin olun. Örnek için `.env.example` dosyasına bakabilirsiniz.

Sunucuyu başlatmak için:
```bash
python main.py
# veya
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. Frontend (Mobil/Web) Kurulumu
Ana proje dizininde (repo) aşağıdaki komutları çalıştırın:

```bash
# Bağımlılıkları getir
flutter pub get

# Uygulamayı başlat (Cihaz seçili olmalı)
flutter run
```

### 3. Modellerin Hazırlanması
Ollama'nın kurulu olduğundan ve `selcuk-assistant-v1` veya `.env` dosyasında belirtilen modelin çekildiğinden emin olun:

```bash
ollama pull turkcell-llm-7b-v1
# Veya sizin yapılandırdığınız model ismi
```

## Sorun Giderme
- **503 Hatası:** Ollama servisinin çalıştığından emin olun.
- **RAG Hatası:** `backend/data` altında vektör veritabanının oluştuğunu kontrol edin. Eğer yoksa `python scripts/create_rag_simple.py` scriptini çalıştırın.

## İletişim & Destek
Proje geliştiricisi ile iletişime geçiniz.
