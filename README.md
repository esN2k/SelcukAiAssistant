# 🎓 Selçuk AI Akademik Asistan

> Selçuk Üniversitesi Bilgisayar Mühendisliği Uygulamaları Dersi - Final Projesi
> 
> **Proje Sahibi:** esN2k
> **Akademik Yıl:** 2025-2026

[![Backend CI](https://github.com/esN2k/SelcukAiAssistant/actions/workflows/backend.yml/badge.svg?branch=main)](https://github.com/esN2k/SelcukAiAssistant/actions/workflows/backend.yml)
[![Flutter Build](https://github.com/esN2k/SelcukAiAssistant/actions/workflows/dart.yml/badge.svg?branch=main)](https://github.com/esN2k/SelcukAiAssistant/actions/workflows/dart.yml)
[![Ruff](https://img.shields.io/badge/ruff-enabled-2?logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)

---

## 📖 Proje Hakkında

Bu proje, Selçuk Üniversitesi öğrencileri, akademisyenleri ve idari personeli için geliştirilmiş **yerli ve milli** bir yapay zeka asistanıdır. Proje tamamen gizlilik odaklı olup, kullanıcı verilerinin dışarıya sızmaması için yerel LLM (Large Language Model) altyapısı kullanmaktadır.

### 🎯 Projenin Amacı

1. **Akademik Destek:** Öğrencilere ders, sınav, burs konularında yardımcı olmak
2. **Veri Güvenliği:** Tüm veriler yerel olarak işlenir, hiçbir bilgi dış servislere gönderilmez
3. **RAG Teknolojisi:** Retrieval-Augmented Generation ile kaynak göstererek güvenilir yanıtlar üretmek
4. **Çoklu Platform Desteği:** Android, iOS, Windows, Web üzerinde çalışabilme

### 🏆 Projenin Öne Çıkan Özellikleri

- ✅ **100% Yerel İşlem:** Google Gemini API'den tamamen bağımsız, Ollama (Llama 3.1) kullanımı
- ✅ **Gizlilik Garantisi:** Hiçbir kullanıcı verisi dışarıya gitmez
- ✅ **Kaynak Gösterimi:** RAG teknolojisi ile yanıtlar belge kaynaklarıyla desteklenir
- ✅ **Çoklu Model Desteği:** Ollama ve HuggingFace modelleri kullanılabilir
- ✅ **Modern UI/UX:** Flutter Material 3 tasarımı
- ✅ **Otomatik Test:** CI/CD pipeline ile kod kalitesi garantisi

> 🎓 **Jüri Sunumuna Hazırlık:** [docs/JURI_HAZIRLIK.md](docs/JURI_HAZIRLIK.md) dosyasında sunum kontrol listesi ve demo senaryoları bulunmaktadır.

---

## 🗂️ PROJE YAPISININ DETAYLI AÇIKLAMASI

### 📁 Kök Dizin Dosyaları

| Dosya/Klasör | Ne İşe Yarar | Neden Önemli |
|--------------|--------------|--------------|
| **README.md** | Projenin ana dokümantasyonu | İlk bakılan dosya, projeyi anlamak için kritik |
| **pubspec.yaml** | Flutter projesi bağımlılık yönetimi | Hangi paketlerin kullanıldığını gösterir |
| **analysis_options.yaml** | Dart kod analiz kuralları | Kod kalitesini garanti altına alır |
| **.env.example** | Ortam değişkenleri şablonu | API anahtarları ve yapılandırma |
| **docker-compose.yml** | Backend servislerini Docker ile çalıştırma | Kolay kurulum için |
| **l10n.yaml** | Çoklu dil desteği yapılandırması | Türkçe ve İngilizce dil desteği |
| **INSTALL.md** | Detaylı kurulum rehberi | Adım adım kurulum talimatları |
| **CONTRIBUTORS.md** | Katkıda bulunanlar listesi | Proje ekibi bilgileri |

### 📁 /android
Android uygulaması için gerekli Java/Kotlin yapılandırma dosyaları.

**Ne İçerir:**
- `app/` → Android uygulama modülü
- `build.gradle` → Android derleme ayarları
- `AndroidManifest.xml` → Uygulama izinleri ve yapılandırma

**Neden Önemli:** Flutter uygulamasının Android'de çalışabilmesi için gerekli.

### 📁 /ios
iOS uygulaması için gerekli Swift/Objective-C yapılandırma dosyaları.

**Ne İçerir:**
- `Runner.xcodeproj` → Xcode proje dosyası
- `Info.plist` → iOS uygulama yapılandırması

**Neden Önemli:** Flutter uygulamasının iOS'ta çalışabilmesi için gerekli.

### 📁 /windows
Windows masaüstü uygulaması için gerekli C++ yapılandırma dosyaları.

**Ne İçerir:**
- `runner/` → Windows uygulama çalıştırıcısı
- `CMakeLists.txt` → C++ derleme yapılandırması

**Neden Önemli:** Flutter uygulamasının Windows'ta masaüstü uygulama olarak çalışması için gerekli.

### 📁 /web
Web uygulaması için gerekli HTML/CSS/JavaScript dosyaları.

**Ne İçerir:**
- `index.html` → Web uygulaması ana sayfası
- `manifest.json` → PWA (Progressive Web App) yapılandırması

**Neden Önemli:** Flutter uygulamasının tarayıcıda çalışabilmesi için gerekli.

### 📁 /lib (ANA UYGULAMA KODU)
Flutter uygulamasının tüm Dart kodlarının bulunduğu klasör.

#### /lib/screen
Uygulama ekranlarını içerir.

| Dosya | Ne İşe Yarar |
|-------|--------------|
| **splash_screen.dart** | Uygulama açılış ekranı (logo gösterimi) |
| **home_screen.dart** | Ana sayfa ekranı |
| **feature/chatbot_feature.dart** | Sohbet arayüzü ekranı |
| **feature/new_chat_screen.dart** | Yeni sohbet başlatma ekranı |
| **settings_screen.dart** | Ayarlar ekranı |
| **model_picker_screen.dart** | Model seçim ekranı |
| **diagnostics_screen.dart** | Tanılama ve hata ayıklama ekranı |
| **onboarding_screen.dart** | İlk kullanım karşılama ekranı |
| **auth/** | Giriş ve kayıt ekranları |

#### /lib/services
Backend servisleriyle iletişim ve veri yönetimi.

| Dosya | Ne İşe Yarar |
|-------|--------------|
| **appwrite_service.dart** | Appwrite backend entegrasyonu |
| **conversation_service.dart** | Sohbet oturumlarını yönetme |
| **model_service.dart** | Model listesi ve seçimi |
| **sse_client.dart** | Server-Sent Events (SSE) istemcisi |
| **voice_service.dart** | Sesli giriş servisi |
| **image_picker_service.dart** | Görsel seçim servisi |
| **response_cleaner.dart** | Yanıt temizleme yardımcısı |
| **storage/** | Yerel veri saklama (SharedPreferences, Hive) |

#### /lib/model
Veri modellerini içerir.

| Dosya | Ne İşe Yarar |
|-------|--------------|
| **message.dart** | Sohbet mesajı veri modeli |
| **chat_message.dart** | API chat mesaj modeli |
| **conversation.dart** | Sohbet oturumu veri modeli |
| **model_info.dart** | Model bilgisi veri modeli |
| **model_pref.dart** | Model tercihleri |
| **onboard.dart** | Onboarding veri modeli |

#### /lib/controller (GetX State Management)
Uygulama durumu yönetimi.

| Dosya | Ne İşe Yarar |
|-------|--------------|
| **chat_controller.dart** | Sohbet ekranı durum yönetimi |
| **enhanced_chat_controller.dart** | Gelişmiş sohbet özellikleri |
| **settings_controller.dart** | Ayarlar ekranı durum yönetimi |

#### /lib/widget
Tekrar kullanılabilir UI bileşenleri.

| Dosya | Ne İşe Yarar |
|-------|--------------|
| **message_card.dart** | Sohbet mesajı kartı |
| **enhanced_message_card.dart** | Gelişmiş mesaj kartı |
| **typing_indicator.dart** | "Yazıyor..." göstergesi |
| **custom_btn.dart** | Özel düğme tasarımı |
| **custom_loading.dart** | Yükleme göstergesi |
| **markdown_message_view.dart** | Markdown mesaj görüntüleyici |
| **model_card.dart** | Model seçim kartı |
| **availability_badge.dart** | Uygunluk rozeti |
| **conversation_list_drawer.dart** | Sohbet listesi çekmecesi |

#### /lib/helper
Yardımcı fonksiyonlar ve sabitler.

| Dosya | Ne İşe Yarar |
|-------|--------------|
| **global.dart** | Global sabitler ve değişkenler |
| **pref.dart** | Kullanıcı tercihleri yönetimi |
| **my_dialog.dart** | Özel diyalog pencereleri |
| **ad_helper.dart** | Reklam yardımcısı |

#### /lib/theme
Tema ve renk tanımlamaları.

| Dosya | Ne İşe Yarar |
|-------|--------------|
| **selcuk_theme.dart** | Selçuk teması (açık/koyu mod) |

#### /lib/l10n
Çoklu dil desteği.

| Dosya | Ne İşe Yarar |
|-------|--------------|
| **l10n.dart** | Dil desteği ana dosyası |
| **app_localizations.dart** | Lokalizasyon yardımcıları |
| **app_en.arb** | İngilizce çeviriler |
| **app_tr.arb** | Türkçe çeviriler |

### 📁 /backend (PYTHON FASTAPI BACKEND)
Python FastAPI ile yazılmış backend servisi.

#### Backend Ana Dosyaları

| Dosya | Ne İşe Yarar | Detaylı Açıklama |
|-------|--------------|------------------|
| **main.py** | FastAPI uygulamasının ana giriş noktası | HTTP endpoint'leri tanımlanır (/health, /chat, /models, /chat/stream) |
| **config.py** | Ortam değişkenlerini yükler | .env dosyasından API anahtarları ve ayarları okur |
| **schemas.py** | Pydantic veri doğrulama | API istek/yanıt modellerini tanımlar |
| **utils.py** | Yardımcı fonksiyonlar | Token hesaplama, mesaj normalizasyonu, SSE yardımcıları |
| **prompts.py** | Sistem promptları | Selçuk Üniversitesi bilgileri içeren prompt şablonları |
| **accuracy_guard.py** | Doğruluk kontrolü | Kritik bilgileri (Konya, 1975) doğrular |
| **rag_service.py** | RAG servisi | FAISS ile vektör araması |
| **rag_ingest.py** | RAG indeksleme | Belgeleri vektörlere dönüştürür |
| **response_cleaner.py** | Yanıt temizleme | Gereksiz karakterleri temizler |
| **ollama_service.py** | Ollama sarmalayıcı | Ollama API yardımcı fonksiyonları |
| **selcuk_data.py** | Selçuk bilgileri | Selçuk Üniversitesi hakkında sabit veriler |

#### /backend/providers
LLM sağlayıcı adaptörleri (Provider Pattern).

| Dosya | Ne İşe Yarar |
|-------|--------------|
| **base.py** | Temel provider arayüzü (abstract class) |
| **ollama_provider.py** | Ollama API entegrasyonu |
| **huggingface_provider.py** | HuggingFace model entegrasyonu |
| **registry.py** | Model kayıt sistemi ve yönlendirme |

#### /backend/tests
Backend testleri.

| Dosya | Ne İşe Yarar |
|-------|--------------|
| **test_main.py** | API endpoint testleri |
| **test_accuracy_guard.py** | Doğruluk kontrolü testleri |
| **test_response_cleaner.py** | Yanıt temizleme testleri |
| **test_critical_facts.py** | Kritik bilgi testleri |
| **test_model.py** | Model testleri |

### 📁 /assets
Uygulama görselleri ve varlıkları.

| Alt Klasör | İçerik |
|------------|--------|
| **/images** | Logo, ikon dosyaları |
| **/fonts** | Özel fontlar |
| **/lottie** | Lottie animasyonları |

### 📁 /docs
Detaylı dokümantasyon dosyaları.

| Dosya | Ne Anlatır |
|-------|------------|
| **JURI_HAZIRLIK.md** | Jüri sunumu hazırlık kontrol listesi |
| **JURY_QUICK_REFERENCE.md** | Jüri için hızlı başvuru |
| **DEMO_SCRIPT.md** | Demo senaryoları |
| **SUNUM_NOTLARI.md** | Sunum notları |
| **ARCHITECTURE.md** | Mimari açıklaması |
| **API_CONTRACT.md** | API endpoint dokümantasyonu |
| **RAG.md** | RAG teknolojisi açıklaması |
| **MODELLER.md** | Model yönetimi |
| **DAGITIM.md** | Dağıtım rehberi |
| **SORUN_GIDERME.md** | Sorun giderme |
| **TEST_RAPORU.md** | Test sonuçları |
| **BENCHMARK_RAPORU.md** | Performans ölçümleri |
| **GUVENLIK_OZETI.md** | Güvenlik özeti |

### 📁 /tools
Yardımcı scriptler.

| Dosya | Ne İşe Yarar |
|-------|--------------|
| **test_api.ps1** | Backend API test scripti |
| **smoke_test.ps1** | Hızlı sistem testi |

---

## 🚀 SIFIRDAN KURULUM (BOŞ BİLGİSAYAR)

Bu bölüm, hiç programlama bilgisi olmayan birinin bile projeyi kurabilmesini sağlar.

### 📌 Adım 1: Gerekli Yazılımları İndirin

#### 1.1 Git Kurulumu
- **Git nedir:** Kod versiyonlama sistemi
- **İndirme linki:** https://git-scm.com/download/win
- **Kurulum:** "Next" diyerek varsayılan ayarlarla kurun

**[SCREENSHOT GEREKLİ: Git kurulum ekranı]**
> Bu ekranda "Add Git to PATH" seçeneğini işaretlemelisiniz.

#### 1.2 Flutter SDK Kurulumu
- **Flutter nedir:** Mobil/web/masaüstü uygulaması geliştirme framework'ü
- **İndirme linki:** https://docs.flutter.dev/get-started/install/windows
- **Kurulum adımları:**
  1. ZIP dosyasını indirin
  2. `C:\src\flutter` klasörüne çıkartın
  3. Sistem değişkenlerine `C:\src\flutter\bin` ekleyin

**[SCREENSHOT GEREKLİ: Flutter PATH ayarı]**

**Doğrulama:**
```bash
flutter doctor
```

#### 1.3 Python Kurulumu
- **Python nedir:** Backend geliştirme dili
- **İndirme linki:** https://www.python.org/downloads/
- **Önerilen sürüm:** Python 3.12
- **Kurulum:** "Add Python to PATH" seçeneğini işaretleyin

**[SCREENSHOT GEREKLİ: Python kurulum ekranı]**

**Doğrulama:**
```bash
python --version
```

#### 1.4 Ollama Kurulumu
- **Ollama nedir:** Yerel LLM çalıştırma platformu
- **İndirme linki:** https://ollama.ai/download
- **Kurulum:** Varsayılan ayarlarla kurun

**[SCREENSHOT GEREKLİ: Ollama kurulum ekranı]**

**Model İndirme:**
```bash
ollama pull llama3.1
```

**[SCREENSHOT GEREKLİ: Model indirme süreci]**

---

### 📌 Adım 2: Projeyi İndirin

#### 2.1 Repository'yi Klonlayın
```bash
git clone https://github.com/esN2k/SelcukAiAssistant.git
cd SelcukAiAssistant
```

**[SCREENSHOT GEREKLİ: Git clone işlemi]**

---

### 📌 Adım 3: Backend Kurulumu

#### 3.1 Backend Klasörüne Gidin
```bash
cd backend
```

#### 3.2 Python Sanal Ortamı Oluşturun
```bash
python -m venv .venv
```

**Sanal ortam nedir:** Python paketlerini izole eder, sistem Python'unu kirletmez.

#### 3.3 Sanal Ortamı Aktifleştirin

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

**Ne oldu:** Komut satırında `(.venv)` öneki görünecek.

**[SCREENSHOT GEREKLİ: Aktif sanal ortam]**

#### 3.4 Bağımlılıkları Kurun
```bash
pip install -r requirements.txt
```

**Ne kuruluyor:**
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `langchain`: RAG orchestration
- `faiss-cpu`: Vektör araması
- `sentence-transformers`: Metin embedding

**[SCREENSHOT GEREKLİ: pip install süreci]**

#### 3.5 Ortam Değişkenlerini Ayarlayın

**Windows:**
```bash
copy .env.example .env
```

**Linux / macOS:**
```bash
cp .env.example .env
```

**.env dosyasını açın ve düzenleyin:**
```env
# Ollama Ayarları
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

# RAG Ayarları
RAG_ENABLED=true
RAG_VECTOR_DB_PATH=./data/rag

# CORS Ayarları
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

**[SCREENSHOT GEREKLİ: .env dosyası düzenleme]**

#### 3.6 RAG İndeksini Oluşturun (Opsiyonel)
```bash
python rag_ingest.py --input ../docs --output ./data/rag
```

**Ne oluyor:** Dokümantasyon dosyaları vektörlere dönüştürülüyor.

**[SCREENSHOT GEREKLİ: RAG indeksleme süreci]**

#### 3.7 Backend'i Başlatın
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Başarılı başlatma çıktısı:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

**[SCREENSHOT GEREKLİ: Çalışan backend]**

#### 3.8 Test Edin
Tarayıcınızda açın: http://localhost:8000/docs

**[SCREENSHOT GEREKLİ: FastAPI Swagger UI]**

---

### 📌 Adım 4: Flutter Frontend Kurulumu

#### 4.1 Ana Klasöre Dönün
```bash
cd ..
```

#### 4.2 Flutter Bağımlılıklarını Kurun
```bash
flutter pub get
```

**Ne kuruluyor:**
- `get`: State management
- `http`: HTTP istekleri
- `flutter_dotenv`: Ortam değişkenleri
- `hive`: Yerel veritabanı

**[SCREENSHOT GEREKLİ: flutter pub get çıktısı]**

#### 4.3 Ortam Değişkenlerini Ayarlayın

**Windows:**
```bash
copy .env.example .env
```

**Linux / macOS:**
```bash
cp .env.example .env
```

**.env dosyasını açın:**
```env
# Backend URL
API_BASE_URL=http://localhost:8000

# Uygulama Ayarları
APP_NAME=Selçuk AI Asistan
APP_VERSION=1.0.0
```

**[SCREENSHOT GEREKLİ: Flutter .env dosyası]**

#### 4.4 Uygulamayı Çalıştırın

**Windows için:**
```bash
flutter run -d windows
```

**Chrome için (Web):**
```bash
flutter run -d chrome
```

**Android için:**
```bash
flutter run
```

**[SCREENSHOT GEREKLİ: Çalışan Flutter uygulaması]**

---

## 🧪 TESTLERİ ÇALIŞTIRMA

### Backend Testleri
```bash
cd backend
python -m pytest -v
```

**[SCREENSHOT GEREKLİ: Başarılı test sonuçları]**

### Flutter Testleri
```bash
flutter test
```

### Kod Kalitesi Kontrolü

**Backend (Python):**
```bash
cd backend
ruff check .
mypy .
```

**Frontend (Flutter):**
```bash
flutter analyze
```

**[SCREENSHOT GEREKLİ: Kod kalitesi raporları]**

### Smoke Test (Backend çalışırken)
```bash
tools/test_api.ps1
tools/smoke_test.ps1
```

---

## 📚 KULLANIM KLAVUZU

### İlk Kullanım
1. Uygulamayı açın
2. "Merhaba" yazarak test edin
3. "Selçuk Üniversitesi nerede?" sorusunu sorun
4. RAG özelliğini test edin: "Bilgisayar Mühendisliği bölümü hakkında bilgi ver"

**[SCREENSHOT GEREKLİ: Örnek sohbet ekranı]**

### Ayarlar Menüsü
- Tema değiştirme (Açık/Koyu)
- Dil seçimi (Türkçe/İngilizce)
- Model seçimi (Llama 3.1, Qwen, vb.)
- Sesli giriş ayarları

**[SCREENSHOT GEREKLİ: Ayarlar ekranı]**

---

## 🏗️ MİMARİ AÇIKLAMA

### Genel Mimari

```
┌─────────────┐
│   Flutter   │ (Kullanıcı Arayüzü)
│   (Dart)    │
└──────┬──────┘
       │ HTTP/SSE
       ▼
┌─────────────┐
│   FastAPI   │ (Backend API)
│  (Python)   │
└──────┬──────┘
       │
       ├──────► Ollama (Yerel LLM)
       │
       └──────► RAG (FAISS + LangChain)
```

### Veri Akışı

1. **Kullanıcı mesaj yazar** → Flutter UI
2. **HTTP POST /chat** → FastAPI backend
3. **RAG sorgusu** → FAISS vektör araması
4. **LLM çağrısı** → Ollama API
5. **Yanıt akışı** → Server-Sent Events (SSE)
6. **UI güncelleme** → Flutter Stream

### Çoklu Sağlayıcı Desteği (Provider Pattern)

- Backend tarafında `providers/` katmanı ile Ollama ve HF aynı arayüzden çağrılır
- `MODEL_BACKEND` alanı varsayılan sağlayıcıyı belirler
- `/models` çıktısında uygunluk (availability) bilgisi sunulur

---

## 🎓 JÜRİ SUNUMU İÇİN NOTLAR

### Projenin Güçlü Yönleri

1. **Yerli ve Milli:** Tamamen yerel işlem, veri güvenliği
2. **Akademik Odaklı:** Selçuk Üniversitesi'ne özel
3. **Modern Teknolojiler:** Flutter, FastAPI, Ollama, RAG
4. **Test Edilebilir:** CI/CD pipeline, birim testleri
5. **Ölçeklenebilir:** Modüler mimari, provider pattern

### Sık Sorulan Sorular

**S: Neden Google Gemini yerine Ollama kullandınız?**
C: Veri gizliliği için. Öğrenci verileri dışarıya çıkmamalı.

**S: RAG nedir ve neden kullanıldı?**
C: Retrieval-Augmented Generation. Yanıtları belgelerle destekleyerek doğruluğu artırır.

**S: Proje gerçek hayatta kullanılabilir mi?**
C: Evet! Şu anda Selçuk Üniversitesi sunucularında test edilebilir.

**S: Hangi zorlukları aştınız?**
C: Ollama model yönetimi, RAG indeksleme, Türkçe karakter kodlaması.

---

## 📋 Dokümantasyon Tablosu

| Belge | Açıklama | Konum |
| --- | --- | --- |
| **Jüri Hazırlık** | **Sunum hazırlık kontrol listesi ve öneriler** | **`docs/JURI_HAZIRLIK.md`** |
| Sunum Notları | Jüri odaklı sunum akışı ve Soru-Cevap hazırlığı | `docs/SUNUM_NOTLARI.md` |
| Test Raporu | CI/test çıktılarının akademik özeti | `docs/TEST_RAPORU.md` |
| Benchmark Raporu | Ollama hızlı ölçüm sonuçları | `docs/BENCHMARK_RAPORU.md` |
| LoRA Planı | İnce ayar stratejisi ve veri hazırlama | `docs/LORA_PLANI.md` |
| Veri Kaynakları | RAG veri toplama özeti | `docs/VERI_KAYNAKLARI.md` |
| Kurulum Rehberi | Platform bazlı kurulum adımları | `INSTALL.md` |
| Katkıda Bulunanlar | Proje ekibi ve teşekkürler | `CONTRIBUTORS.md` |
| Mimari (Özet) | Yüksek seviye mimari | `ARCHITECTURE.md` |
| Mimari (Detay) | RAG ve provider akışları | `docs/ARCHITECTURE.md` |
| RAG Rehberi | İndeksleme ve ayarlar | `docs/RAG.md` |
| Modeller | Ollama/HF/API model notları | `docs/MODELLER.md` |
| Dağıtım | Yerel/Docker dağıtım | `docs/DAGITIM.md` |
| Sorun Giderme | Yaygın hata ve çözümler | `docs/SORUN_GIDERME.md` |
| API Sözleşmesi | Endpoint ve şema detayları | `docs/API_CONTRACT.md` |
| Yol Haritası | Gelişim planı | `docs/YOL_HARITASI.md` |
| Sürüm Kontrol Listesi | Kalite kapıları | `docs/SURUM_KONTROL_LISTESI.md` |

---

## 📞 İLETİŞİM

- **Proje Sahibi:** esN2k
- **GitHub:** https://github.com/esN2k/SelcukAiAssistant

---

## 📄 LİSANS

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🙏 TEŞEKKÜRLER

- Selçuk Üniversitesi Bilgisayar Mühendisliği Bölümü
- Açık kaynak toplulukları: Flutter, FastAPI, Ollama, HuggingFace, LangChain

---

## Katkıda Bulunanlar

Katkıda bulunanlar listesi ve teşekkürler için [CONTRIBUTORS.md](CONTRIBUTORS.md) dosyasına bakın.
