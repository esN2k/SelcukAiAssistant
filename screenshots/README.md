# 📸 SCREENSHOTS KLASÖRÜ

> Sunum ve dokümantasyon için kullanılacak ekran görüntülerinin saklanacağı klasör.

---

## 📋 KLASÖR AMACI

Bu klasör, aşağıdaki amaçlar için ekran görüntülerini saklamak üzere oluşturulmuştur:

1. **README.md için görselller** - Projenin nasıl göründüğünü göstermek
2. **Sunum materyalleri** - PowerPoint'e eklenecek görüntüler
3. **Demo yedekleri** - Canlı demo çalışmazsa gösterilecek görüntüler
4. **Dokümantasyon** - Kurulum ve kullanım kılavuzları için görüntüler

---

## 📁 KLASÖR YAPISI (ÖNERİLEN)

```
screenshots/
├── README.md              # Bu dosya
├── app/                   # Uygulama ekran görüntüleri
│   ├── splash_screen.png
│   ├── chat_screen.png
│   ├── settings_screen.png
│   └── dark_mode.png
├── demo/                  # Demo ekran görüntüleri
│   ├── health_check.png
│   ├── location_question.png
│   ├── rag_example.png
│   ├── strict_mode.png
│   └── founding_year.png
├── backend/               # Backend ekran görüntüleri
│   ├── swagger_ui.png
│   ├── health_endpoint.png
│   └── chat_response.png
├── architecture/          # Mimari diyagramlar
│   ├── system_architecture.png
│   ├── data_flow.png
│   └── rag_pipeline.png
└── installation/          # Kurulum adımları
    ├── git_install.png
    ├── flutter_install.png
    ├── python_install.png
    ├── ollama_install.png
    └── model_pull.png
```

---

## 📷 ALINMASI GEREKEN EKRAN GÖRÜNTÜLERİ

### 1. Uygulama Ekranları

| Dosya Adı | Açıklama | Öncelik |
|-----------|----------|---------|
| `splash_screen.png` | Uygulama açılış ekranı | ⭐⭐⭐ |
| `chat_screen.png` | Ana sohbet ekranı (boş) | ⭐⭐⭐ |
| `chat_with_messages.png` | Mesajlı sohbet ekranı | ⭐⭐⭐ |
| `settings_screen.png` | Ayarlar ekranı | ⭐⭐ |
| `dark_mode.png` | Karanlık mod görünümü | ⭐⭐ |
| `light_mode.png` | Aydınlık mod görünümü | ⭐⭐ |

### 2. Demo Senaryoları

| Dosya Adı | Senaryo | Öncelik |
|-----------|---------|---------|
| `health_check.png` | Sağlık kontrolü yanıtı | ⭐⭐⭐ |
| `location_question.png` | "Selçuk Üniversitesi nerede?" yanıtı | ⭐⭐⭐ |
| `rag_example.png` | RAG ile kaynak gösterimi | ⭐⭐⭐ |
| `strict_mode_test.png` | Strict mode yanlış bilgi reddi | ⭐⭐⭐ |
| `founding_year.png` | Kuruluş yılı sorusu yanıtı | ⭐⭐ |

### 3. Backend Ekranları

| Dosya Adı | Açıklama | Öncelik |
|-----------|----------|---------|
| `swagger_ui.png` | FastAPI Swagger arayüzü | ⭐⭐⭐ |
| `health_endpoint.png` | /health endpoint yanıtı | ⭐⭐ |
| `models_endpoint.png` | /models endpoint yanıtı | ⭐⭐ |
| `chat_response_json.png` | /chat endpoint JSON yanıtı | ⭐⭐ |

### 4. Kurulum Adımları

| Dosya Adı | Açıklama | Öncelik |
|-----------|----------|---------|
| `git_download.png` | Git indirme sayfası | ⭐ |
| `git_install_path.png` | Git PATH ayarı | ⭐ |
| `flutter_doctor.png` | `flutter doctor` çıktısı | ⭐⭐ |
| `python_path.png` | Python PATH ayarı | ⭐ |
| `ollama_pull.png` | `ollama pull llama3.1` çıktısı | ⭐⭐ |
| `backend_running.png` | Backend başlatma çıktısı | ⭐⭐ |
| `flutter_run.png` | Flutter uygulama başlatma | ⭐⭐ |

### 5. Mimari Diyagramlar

| Dosya Adı | Açıklama | Öncelik |
|-----------|----------|---------|
| `system_architecture.png` | Genel sistem mimarisi | ⭐⭐⭐ |
| `data_flow.png` | Veri akış diyagramı | ⭐⭐ |
| `rag_pipeline.png` | RAG işlem hattı | ⭐⭐ |
| `provider_pattern.png` | Provider pattern diyagramı | ⭐ |

---

## 📐 EKRAN GÖRÜNTÜSÜ STANDARTLARI

### Boyut
- **Mobil ekranlar:** 1080x1920 (Full HD dikey)
- **Web/Desktop:** 1920x1080 (Full HD yatay)
- **Diyagramlar:** 1600x900 (16:9)

### Format
- **Tercih edilen:** PNG (kayıpsız)
- **Alternatif:** JPEG (yüksek kalite, 90%+)
- **Animasyon:** GIF veya MP4

### İsimlendirme
- Küçük harf kullan
- Boşluk yerine alt çizgi (_) kullan
- Açıklayıcı isimler ver
- Örnek: `chat_screen_dark_mode.png`

---

## 🎨 GÖRSEL TUTARLILIK

### Tema
- [ ] Aynı tema (açık veya koyu) kullan
- [ ] Aynı yazı boyutu
- [ ] Aynı renk paleti

### İçerik
- [ ] Gerçekçi örnek veriler kullan
- [ ] Türkçe içerik
- [ ] Kişisel bilgileri gizle

### Kalite
- [ ] Yüksek çözünürlük
- [ ] Bulanık olmayan
- [ ] Doğru kırpılmış

---

## 📝 EKRAN GÖRÜNTÜSÜ ALMA KILAVUZU

### Windows
- **Tam ekran:** `Print Screen`
- **Aktif pencere:** `Alt + Print Screen`
- **Seçili alan:** `Win + Shift + S`

### Mac
- **Tam ekran:** `Cmd + Shift + 3`
- **Seçili alan:** `Cmd + Shift + 4`
- **Pencere:** `Cmd + Shift + 4` sonra `Space`

### Linux
- **Tam ekran:** `Print Screen`
- **Seçili alan:** `Shift + Print Screen`
- **Uygulama:** `gnome-screenshot`, `flameshot`

### Mobil (Emülatör)
- **Android Studio:** Toolbar'da kamera ikonu
- **iOS Simulator:** `Cmd + S`

---

## 🔧 ÖNERİLEN ARAÇLAR

### Ekran Görüntüsü
- **Snagit** (Windows/Mac) - Profesyonel
- **Flameshot** (Linux) - Ücretsiz
- **ShareX** (Windows) - Ücretsiz, güçlü

### Düzenleme
- **Canva** (Web) - Kolay, ücretsiz
- **GIMP** (Tüm platformlar) - Ücretsiz
- **Photoshop** (Windows/Mac) - Profesyonel

### Diyagram
- **draw.io** (Web) - Ücretsiz, kolay
- **Lucidchart** (Web) - Profesyonel
- **Mermaid** (Kod tabanlı) - Markdown uyumlu

---

## ✅ KONTROL LİSTESİ

Sunum öncesi bu görüntülerin hazır olduğundan emin ol:

### Kritik (Mutlaka olmalı)
- [ ] `chat_screen.png` - Çalışan sohbet ekranı
- [ ] `swagger_ui.png` - Backend API görünümü
- [ ] `system_architecture.png` - Mimari diyagramı

### Önemli (Olması iyi)
- [ ] `splash_screen.png`
- [ ] `rag_example.png`
- [ ] Demo senaryosu görüntüleri

### İsteğe Bağlı
- [ ] Kurulum adımları
- [ ] Karanlık mod görüntüleri
- [ ] Detaylı diyagramlar

---

## 📦 YEDEK DEMO MATERYALLERİ

Canlı demo çalışmazsa kullanılacak yedek materyaller:

### Video Kayıtları (Önerilen)
```
demo_videos/
├── full_demo.mp4          # Tam demo (2-3 dk)
├── quick_demo.mp4         # Hızlı demo (1 dk)
└── rag_demo.mp4           # RAG odaklı demo
```

### GIF Animasyonları
```
demo_gifs/
├── chat_interaction.gif   # Sohbet etkileşimi
├── typing_indicator.gif   # Yazıyor göstergesi
└── response_stream.gif    # Yanıt akışı
```

---

## 📞 YARDIM

Ekran görüntüsü alma konusunda sorun yaşarsan:
1. Google'da "how to take screenshot [işletim sistemi]" ara
2. Ekran kayıt yazılımı kullan (OBS Studio ücretsiz)
3. Emülatörün yerleşik özelliklerini kullan

---

*Bu klasörü sunum öncesi doldur ve kontrol et!*
