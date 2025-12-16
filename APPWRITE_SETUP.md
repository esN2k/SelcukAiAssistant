# Appwrite Collection Yapılandırma Rehberi

## 🗄️ Database: `chat_logs` (Tables kullanıyor)

> **NOT**: Appwrite'ın yeni versiyonunda "Collections" yerine "Tables" kullanılıyor.
> "Tables" → "Columns" ile "Collections" → "Attributes" aynı işlevi görür.

### Gerekli Columns (Sütunlar)

Appwrite Console'da şu adımları izleyin:

1. **Database**: `694083cb0031903b17d5` ✅ (zaten var)
2. **Tables**: `chat_logs` ✅ (zaten var)
3. **Columns** (Sütunlar) ekleyin:

#### ⚠️ Önemli: Ücretsiz Plan Limitleri

Appwrite Free Tier'da **toplam sütun boyutu limiti** vardır (~64KB).
Bu yüzden sütun boyutlarını küçük tutmalıyız:

#### 1. `question` (String)

- **Type**: String
- **Size**: **2000 characters** ← (5000 yerine küçültüldü)
- **Required**: Yes
- **Array**: No

#### 2. `answer` (String)

- **Type**: String
- **Size**: **4000 characters** ← (10000 yerine küçültüldü)
- **Required**: Yes
- **Array**: No

#### 3. `timestamp` (DateTime)

- **Type**: DateTime
- **Required**: Yes
- **Array**: No

> **NOT**: Eğer "The maximum number or size of columns has been reached" hatası alırsanız,
> `answer` boyutunu **2000** veya **1000** karaktere düşürün.

### Permissions (İzinler)

**Document Security** ayarlarını kontrol edin:

#### Create Documents:

```
Role: Any
```

veya backend için API Key kullanıyorsanız:

```
Role: Server "Backend Server Key"
```

#### Read Documents:

```
Role: Any
```

(Sadece admin okuyabilsin istiyorsanız kısıtlayabilirsiniz)

---

## 🔍 Appwrite Console'da Kontrol

### 1. Databases → Database → chat_logs → Columns

Şu sütunları görmelisiniz:

```
✓ question   [String, 2000]    Required
✓ answer     [String, 4000]    Required  
✓ timestamp  [DateTime]        Required
```

### 2. Columns Yoksa veya Hata Alıyorsanız:

#### Senaryo A: "Maximum columns reached" Hatası

Bu hata, toplam sütun boyutunun limitini aştığınız anlamına gelir.

**Çözüm**:

1. Mevcut `question` ve `timestamp` sütunlarını SİLMEYİN
2. `answer` sütununu şu boyutlarla ekleyin:
    - İlk deneme: **4000** karakter
    - Hala hata alıyorsanız: **2000** karakter
    - Son çare: **1000** karakter

#### Senaryo B: Columns Nasıl Eklenir?

1. Appwrite Console → Databases
2. Database seçin (694083cb0031903b17d5)
3. `chat_logs` tablosuna tıklayın
4. **"Columns"** tab'ına gidin
5. **"Add Column"** butonuna tıklayın
6. Her sütun için yukarıdaki özellikleri girin

#### Senaryo C: Tablo Yeniden Oluşturma (Son Çare)

Eğer limitleri aşıp tablo bozulduysa:

1. `chat_logs` tablosunu SİLİN
2. **"Create Table"** butonuna tıklayın
3. Table ID: `chat_logs` yazın
4. Sütunları tekrar ekleyin (küçük boyutlarla)

---

### 3. Table Settings → Permissions

**Document Security**:

- Table Level Security kullanıyorsanız izinleri kontrol edin
- Document Level Security tercih edilir

**Create Permission** eklemeniz gerekiyor:

```
Role: Any
```

veya

```
Role: Server (API Key ile)
```

---

## 🧪 Manuel Test

### PowerShell ile Test:

```powershell
$headers = @{
    "X-Appwrite-Project" = "69407f8200300e7093d8"
    "X-Appwrite-Key" = "standard_26cd773293db96c9c9552975851221c90042f4f188c1daef00fb988dd823af265af7ebe768bc4e6fa4df64faff9aead5d93fe7fb8f1a776949e84ae913cecd0c453b6f52ee028e216adb5f98bccca9ee078a8f2f28a907e60cbb8d921f05f4b3099bf37ee1cdc4406f80220d4319b65297dc8458d296429bad14ac3d6c40c7ce"
    "Content-Type" = "application/json"
}

$body = @{
    documentId = "test_manual_$( Get-Random )"
    data = @{
        question = "Test soru - Appwrite entegrasyonu çalışıyor mu?"
        answer = "Test cevap - Evet, başarıyla çalışıyor!"
        timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
    }
} | ConvertTo-Json

Invoke-WebRequest `
    -Uri "https://fra.cloud.appwrite.io/v1/databases/694083cb0031903b17d5/collections/chat_logs/documents" `
    -Method POST `
    -Headers $headers `
    -Body $body
```

**Başarılı Yanıt (201 Created):**

```json
{
  "$id": "test_manual_123",
  "$collectionId": "chat_logs",
  "$databaseId": "694083cb0031903b17d5",
  "$createdAt": "2025-12-16T...",
  "$updatedAt": "2025-12-16T...",
  "$permissions": [],
  "question": "Test soru",
  "answer": "Test cevap",
  "timestamp": "2025-12-16T..."
}
```

**Hata Yanıtları:**

#### 400 Bad Request - Attribute eksik:

```json
{
  "message": "Invalid document structure: Missing required attribute: timestamp",
  "code": 400
}
```

**Çözüm**: Columns/Attributes'ları yukarıdaki gibi ekleyin

#### 400 Bad Request - Column size limit:

```json
{
  "message": "The maximum number or size of columns for table 'chat_logs' has been reached.",
  "code": 400
}
```

**Çözüm**:

1. `answer` column size'ı küçültün (4000 → 2000 → 1000)
2. Veya gereksiz sütunları silin
3. Son çare: Tabloyu silip yeniden oluşturun (daha küçük boyutlarla)

#### 401 Unauthorized - API Key yanlış:

```json
{
  "message": "Invalid API key",
  "code": 401
}
```

**Çözüm**: API Key'i `.env` dosyasında kontrol edin

#### 404 Not Found - Collection yok:

```json
{
  "message": "Collection with the requested ID could not be found",
  "code": 404
}
```

**Çözüm**: Collection ID'yi kontrol edin

---

## 📝 Backend Log Mesajları

Backend'i yeniden başlattığınızda şunları görmelisiniz:

### ✅ Başarılı Yapılandırma:

```
INFO - Appwrite client initialized: endpoint=https://fra.cloud.appwrite.io/v1, 
       project=69407f8200300e7093d8, 
       database=694083cb0031903b17d5, 
       collection=chat_logs
```

### ❌ Yapılandırma Yok:

```
WARNING - Appwrite not configured: endpoint=True, project_id=True, api_key=False
```

(Yukarıdaki örnek API key eksik olduğunda)

### ✅ Başarılı Log Kaydı:

```
DEBUG - Attempting to log to Appwrite: chat_abc123def456
INFO - ✅ Appwrite log kaydı başarılı: chat_abc123def456
```

### ❌ Başarısız Log Kaydı:

```
DEBUG - Attempting to log to Appwrite: chat_abc123def456
WARNING - ❌ Appwrite log kaydı başarısız: 400 Client Error: Bad Request
WARNING - Appwrite error details: {"message": "Missing required attribute: timestamp", "code": 400}
```

---

## 🔧 Olası Sorunlar ve Çözümleri

| Sorun                    | Semptom                                     | Çözüm                                        |
|--------------------------|---------------------------------------------|----------------------------------------------|
| **Column size limit**    | "Maximum number or size of columns reached" | `answer` boyutunu 4000 → 2000 → 1000'e düşür |
| **Attributes eksik**     | 400 Bad Request                             | Console'da columns ekle                      |
| **API Key yanlış**       | 401 Unauthorized                            | `.env` dosyasında API key kontrol et         |
| **Collection ID yanlış** | 404 Not Found                               | Table/Collection ID'yi doğrula               |
| **Permissions eksik**    | 403 Forbidden                               | Table permissions ayarla                     |
| **Field type uyumsuz**   | 400 Bad Request                             | Column tiplerini kontrol et                  |

---

## ✅ Kontrol Listesi

Backend'i başlatmadan önce:

- [ ] Appwrite Console'da `chat_logs` collection var
- [ ] `question`, `answer`, `timestamp` attributes tanımlı
- [ ] Attribute tipleri doğru (String, String, DateTime)
- [ ] Create permission ayarlanmış
- [ ] `.env` dosyasında tüm Appwrite değişkenleri var
- [ ] API Key doğru ve Server type

Backend başlatıldıktan sonra:

- [ ] "Appwrite client initialized" log mesajı görünüyor
- [ ] Test sorusu sonrası "✅ Appwrite log kaydı başarılı" görünüyor
- [ ] Appwrite Console'da Documents tab'ında yeni kayıt var

---

## 🎯 Hızlı Düzeltme

Eğer hâlâ çalışmıyorsa:

1. **Backend'i durdur** (Ctrl+C)
2. **Appwrite Console'da attributes kontrol et**
3. **Manuel test yap** (yukarıdaki PowerShell komutu)
4. **Backend'i yeniden başlat**
5. **Logları izle** - Appwrite client initialized görmeli
6. **Test sorusu sor** - ✅ işareti görmeli
7. **Console'da refresh** - Yeni belge görmeli

---

## 📞 Destek

Hâlâ sorun varsa backend loglarını ve Appwrite Console screenshot'unu paylaşın.

