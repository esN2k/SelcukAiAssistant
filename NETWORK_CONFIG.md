# Backend ve Frontend Bağlantı Konfigürasyonu

**Tarih**: 16 Aralık 2025  
**Durum**: ✅ Düzeltildi

## 📋 Yapılan Değişiklikler

### 1. Backend Host Ayarı (`backend/config.py`)

**Önceki:**

```python
HOST: str = os.getenv("HOST", "127.0.0.1")  # Sadece localhost
```

**Şimdi:**

```python
HOST: str = os.getenv("HOST", "0.0.0.0")  # Tüm network interfaceleri
```

**Açıklama:**

- `127.0.0.1`: Sadece aynı makineden bağlantı (localhost only)
- `0.0.0.0`: Tüm network interfacelerinden bağlantı kabul eder:
    - ✅ `localhost` üzerinden
    - ✅ `127.0.0.1` üzerinden
    - ✅ Makine IP'si üzerinden (ör: `192.168.1.x`)
    - ✅ Android emulator için `10.0.2.2`

### 2. Timeout Ayarı (`backend/config.py`)

**Önceki:**

```python
OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "30"))  # 30 saniye
```

**Şimdi:**

```python
OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "120"))  # 120 saniye
```

**Açıklama:**

- Ollama model yanıt süreleri değişkenlik gösterir
- Karmaşık sorularda 30 saniye yetersiz kalabilir
- 120 saniye daha güvenli bir timeout değeri
- `.env` dosyasındaki değerle uyumlu

---

## 🚀 Backend Başlatma

### Doğru Kullanım

```powershell
cd D:\Projects\SelcukAiAssistant\backend
python main.py
```

**Beklenen Log:**

```
INFO - Starting server on 0.0.0.0:8000  # ✅ 0.0.0.0
INFO - Uvicorn running on http://0.0.0.0:8000
```

❌ **Yanlış Log:**

```
INFO - Starting server on 127.0.0.1:8000  # ❌ 127.0.0.1
```

### Host Override (Gerekirse)

Eğer `.env` dosyasını değiştirmek istemiyorsanız:

```powershell
# PowerShell
$env:HOST = "0.0.0.0"; python main.py

# Veya komut satırı argümanı ile (eğer destekleniyorsa)
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 📱 Flutter Frontend Yapılandırması

### Platform Bazlı URL'ler (`lib/helper/global.dart`)

```dart
static String get backendUrl {
  if (kIsWeb) {
    return 'http://localhost:8000'; // ✅ Web/Chrome
  } else if (Platform.isAndroid) {
    return 'http://10.0.2.2:8000'; // ✅ Android Emulator
  } else {
    return 'http://localhost:8000'; // ✅ iOS Simulator
  }
}
```

**Önemli:**

- Web için `localhost` kullanılmalı (CORS izni var)
- Android emulator için `10.0.2.2` (host makinenin loopback'i)
- iOS simulator için `localhost` (aynı network namespace)

### Test Komutları

```powershell
# Web (Chrome)
flutter run -d chrome

# Android Emulator
flutter run -d emulator-5554

# iOS Simulator (macOS)
flutter run -d iPhone
```

---

## 🔍 Bağlantı Sorunları Giderme

### 1. Backend Erişilebilirlik Testi

```powershell
# Localhost testi
Invoke-WebRequest -Uri http://localhost:8000/health -Method GET

# 127.0.0.1 testi
Invoke-WebRequest -Uri http://127.0.0.1:8000/health -Method GET

# Makine IP testi (kendi IP'nizi yazın)
Invoke-WebRequest -Uri http://192.168.1.100:8000/health -Method GET
```

**Başarılı Yanıt:**

```json
{
  "status": "ok",
  "message": "Backend is running"
}
```

### 2. CORS Hatası

**Hata:**

```
Access to fetch at 'http://localhost:8000/chat' from origin 'http://localhost:XXXX' 
has been blocked by CORS policy
```

**Çözüm:**
`.env` dosyasında CORS ayarını kontrol edin:

```dotenv
ALLOWED_ORIGINS=*  # Geliştirme için tüm originlere izin ver
```

### 3. Connection Refused Hatası

**Hata:**

```
Failed to connect to localhost:8000
Connection refused
```

**Çözüm:**

1. Backend'in çalıştığından emin olun
2. Port 8000'in başka bir uygulama tarafından kullanılmadığını kontrol edin:
   ```powershell
   netstat -ano | findstr :8000
   ```
3. Firewall kurallarını kontrol edin

### 4. Timeout Hatası

**Hata Log:**

```
WARNING - Ollama request timed out (attempt 1/3)
```

**Çözüm:**

1. `.env` dosyasında timeout'u artırın:
   ```dotenv
   OLLAMA_TIMEOUT=180  # 3 dakika
   ```
2. Ollama'nın çalıştığını kontrol edin:
   ```powershell
   ollama list
   ollama run selcuk_ai_assistant
   ```
3. Model'in yüklendiğini doğrulayın

---

## 📊 Network Akış Diyagramı

```
┌─────────────────────────────────────────────────────────────┐
│                     Flutter Frontend                        │
├─────────────────────────────────────────────────────────────┤
│  Web (Chrome)     → http://localhost:8000/chat              │
│  Android Emulator → http://10.0.2.2:8000/chat              │
│  iOS Simulator    → http://localhost:8000/chat              │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP POST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend (FastAPI) - 0.0.0.0:8000               │
├─────────────────────────────────────────────────────────────┤
│  ✅ CORS Middleware (ALLOWED_ORIGINS=*)                     │
│  ✅ /chat endpoint                                          │
│  ✅ ChatRequest validation                                  │
└────────────────────────┬────────────────────────────────────┘
                         │ Generate prompt
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Ollama Service (localhost:11434)           │
├─────────────────────────────────────────────────────────────┤
│  Model: selcuk_ai_assistant                                 │
│  Timeout: 120s                                              │
│  Options: temperature=0.7, top_p=0.9, ...                  │
└────────────────────────┬────────────────────────────────────┘
                         │ AI Response
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Appwrite (Optional Logging)                    │
├─────────────────────────────────────────────────────────────┤
│  Database: 694083cb0031903b17d5                             │
│  Collection: chat_logs                                      │
│  Fields: question, answer, timestamp                        │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ Kontrol Listesi

Backend başlatmadan önce:

- [ ] `.env` dosyası var ve doğru yapılandırılmış
- [ ] Ollama çalışıyor (`ollama list`)
- [ ] Model yüklenmiş (`ollama run selcuk_ai_assistant`)
- [ ] Port 8000 boş

Frontend başlatmadan önce:

- [ ] Backend çalışıyor ve `0.0.0.0:8000` üzerinde
- [ ] Backend health endpoint yanıt veriyor
- [ ] CORS ayarları doğru

---

## 🎯 Özet

| Ayar           | Önceki           | Şimdi            | Neden                      |
|----------------|------------------|------------------|----------------------------|
| Backend Host   | `127.0.0.1`      | `0.0.0.0`        | Tüm interfacelerden erişim |
| Backend Port   | `8000`           | `8000`           | Değişmedi                  |
| Ollama Timeout | `30s`            | `120s`           | Timeout hatalarını önler   |
| Web URL        | `localhost:8000` | `localhost:8000` | Değişmedi                  |
| Android URL    | `10.0.2.2:8000`  | `10.0.2.2:8000`  | Değişmedi                  |

**Sonuç**: Backend artık tüm platformlardan erişilebilir ve timeout hataları minimuma indirildi. ✅

