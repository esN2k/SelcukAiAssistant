# /lib Klasörü - Flutter Uygulama Kodu

## 📖 Genel Bakış

Bu klasör, Selçuk AI Akademik Asistan Flutter uygulamasının **tüm Dart kodlarını** içerir.
Flutter'da uygulama kodu `lib/` klasöründe bulunur.

## 📁 Klasör Yapısı

```
lib/
├── main.dart           # Uygulama giriş noktası
├── apis/               # Backend API entegrasyonu
├── config/             # Yapılandırma sabitleri
├── controller/         # GetX state management
├── helper/             # Yardımcı fonksiyonlar
├── l10n/               # Çoklu dil desteği (Türkçe/İngilizce)
├── model/              # Veri modelleri
├── screen/             # Ekran widget'ları
├── services/           # Servis sınıfları
├── theme/              # Tema tanımlamaları
└── widget/             # Tekrar kullanılabilir widget'lar
```

## 📁 Alt Klasörler

### /apis
Backend API iletişimi.

| Dosya | Açıklama |
|-------|----------|
| `apis.dart` | HTTP istek yönetimi, /chat endpoint çağrıları |

### /config
Uygulama yapılandırması.

| Dosya | Açıklama |
|-------|----------|
| `backend_config.dart` | Backend URL ve ayarları |

### /controller
GetX state management controller'ları.

| Dosya | Açıklama |
|-------|----------|
| `chat_controller.dart` | Sohbet ekranı durum yönetimi |
| `enhanced_chat_controller.dart` | Gelişmiş sohbet özellikleri |
| `settings_controller.dart` | Ayarlar ekranı durum yönetimi |

### /helper
Yardımcı sınıflar ve fonksiyonlar.

| Dosya | Açıklama |
|-------|----------|
| `global.dart` | Global sabitler (uygulama adı, vb.) |
| `pref.dart` | Kullanıcı tercihleri (SharedPreferences) |
| `my_dialog.dart` | Özel diyalog pencereleri |
| `ad_helper.dart` | Reklam yönetimi |

### /l10n
Çoklu dil desteği (Localization).

| Dosya | Açıklama |
|-------|----------|
| `l10n.dart` | Dil yönetimi |
| `app_localizations.dart` | Lokalizasyon yardımcıları |
| `app_en.arb` | İngilizce metinler |
| `app_tr.arb` | Türkçe metinler |

### /model
Veri modelleri (data classes).

| Dosya | Açıklama |
|-------|----------|
| `message.dart` | Sohbet mesajı modeli |
| `chat_message.dart` | API mesaj modeli |
| `conversation.dart` | Sohbet oturumu modeli |
| `model_info.dart` | LLM model bilgisi |

### /screen
Uygulama ekranları.

| Dosya/Klasör | Açıklama |
|--------------|----------|
| `splash_screen.dart` | Açılış ekranı |
| `home_screen.dart` | Ana sayfa |
| `settings_screen.dart` | Ayarlar |
| `feature/chatbot_feature.dart` | Sohbet ekranı |
| `feature/new_chat_screen.dart` | Yeni sohbet |
| `auth/` | Giriş ve kayıt ekranları |

### /services
Servis sınıfları.

| Dosya | Açıklama |
|-------|----------|
| `appwrite_service.dart` | Appwrite backend entegrasyonu |
| `conversation_service.dart` | Sohbet yönetimi |
| `model_service.dart` | Model listesi ve seçimi |
| `sse_client.dart` | Server-Sent Events istemcisi |
| `voice_service.dart` | Sesli giriş |
| `storage/` | Yerel depolama |

### /theme
Tema tanımlamaları.

| Dosya | Açıklama |
|-------|----------|
| `selcuk_theme.dart` | Açık/koyu mod temaları |

### /widget
Tekrar kullanılabilir UI bileşenleri.

| Dosya | Açıklama |
|-------|----------|
| `message_card.dart` | Mesaj kartı |
| `typing_indicator.dart` | "Yazıyor..." göstergesi |
| `custom_btn.dart` | Özel buton |
| `model_card.dart` | Model seçim kartı |

## 🏗️ Mimari

Proje **Clean Architecture** prensiplerine uygun yapılandırılmıştır:

```
UI (Screen/Widget)
      │
      ▼
Controller (GetX)
      │
      ▼
Service Layer
      │
      ▼
API / Storage
```

## 🚀 Çalıştırma

```bash
# Bağımlılıkları yükle
flutter pub get

# Web'de çalıştır
flutter run -d chrome

# Windows'ta çalıştır
flutter run -d windows

# Android'de çalıştır
flutter run
```

## 📝 Notlar

- `main.dart` dosyası uygulama başlangıcını tanımlar
- GetX paketi state management ve navigasyon için kullanılır
- Tüm ekranlar `GetMaterialApp` altında çalışır
- Tema değişikliği `Get.changeThemeMode()` ile yapılır
