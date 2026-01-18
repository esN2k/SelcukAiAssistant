# 🎬 SELÇUK AI ASİSTAN - DEMO SENARYO KILAVUZU

## 📋 Bu Doküman Nedir?

Bu doküman, jüri sunumu sırasında **canlı demo** yaparken
adım adım takip edeceğiniz detaylı senaryoları içerir.
Her adım için ne yapacağınız ve ne söyleyeceğiniz yazılıdır.

---

## 🔧 DEMO ÖNCESİ TEKNİK KONTROL LİSTESİ

### ⏰ Sunum Öncesi 1 Saat
- [ ] Laptop şarjda ve %100
- [ ] İnternet bağlantısı stabil
- [ ] Ollama servisi çalışıyor
- [ ] Backend başlatıldı
- [ ] Flutter app hazır

### ⏰ Sunum Öncesi 15 Dakika
Bu komutları sırayla çalıştırın ve her birinin başarılı olduğunu doğrulayın:

#### ADIM 1: Ollama Kontrolü
```bash
ollama list
```
**Beklenen Çıktı:** Model listesi (llama3.2:3b veya benzeri)

**Başarısızsa:**
```bash
ollama serve
# Ayrı terminalde:
ollama pull llama3.2:3b
```

#### ADIM 2: Backend Kontrolü
```bash
curl http://localhost:8000/health
```
**Beklenen Çıktı:**
```json
{"status": "ok", "message": "Selçuk AI Asistanı backend çalışıyor"}
```

**Başarısızsa:**
```bash
cd backend
source .venv/bin/activate  # Linux/Mac
# veya
.venv\Scripts\activate     # Windows
python main.py
```

#### ADIM 3: Model Listesi Kontrolü
```bash
curl http://localhost:8000/models
```
**Beklenen Çıktı:** Model listesi, `available: true`

#### ADIM 4: Flutter App Kontrolü (Opsiyonel)
```bash
flutter run -d chrome
# veya
flutter run -d windows
```
**Beklenen:** Uygulama açılıyor, ana ekran görünüyor

#### ADIM 5: Projeksiyon/Ekran Kontrolü
- [ ] Laptop ekranı projeksiyon/TV'ye yansıyor
- [ ] Yazı boyutu jürinin göreceği kadar büyük
- [ ] Terminal font boyutu min 14pt
- [ ] Flutter app görünür durumda

---

## 🎯 DEMO SENARYOLARI

---

### 📌 SENARYO 1: SAĞLIK KONTROLÜ

**Amaç:** Sistemin çalıştığını kanıtlamak
**Süre:** 30 saniye

#### ADIM 1: Giriş
🎯 **Jüriye Söyleyeceğiniz:**
> "Öncelikle sistemin çalıştığını göstereyim.
> Backend'e sağlık kontrolü isteği atıyorum."

#### ADIM 2: Komutu Çalıştırın
```bash
curl http://localhost:8000/health
```

#### ADIM 3: Sonucu Açıklayın
🎯 **Jüriye Söyleyeceğiniz:**
> "Görüldüğü gibi `status: ok` dönüyor.
> Backend hazır ve çalışıyor."

**Beklenen Çıktı:**
```json
{
  "status": "ok",
  "message": "Selçuk AI Asistanı backend çalışıyor"
}
```

#### ✅ SENARYO 1 BAŞARI KRİTERLERİ
- [ ] `status: ok` döndü
- [ ] Hata mesajı yok
- [ ] Jüri çıktıyı gördü

---

### 📌 SENARYO 2: KONUM SORUSU (KRİTİK TEST)

**Amaç:** Doğruluk garantisini göstermek
**Süre:** 1 dakika

#### ADIM 1: Giriş
🎯 **Jüriye Söyleyeceğiniz:**
> "Şimdi kritik bir test yapacağım.
> Selçuk Üniversitesi'nin konumunu soracağım.
> Bu, Accuracy Guard sistemimizin en önemli test senaryosu."

#### ADIM 2: Komutu Çalıştırın
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Selçuk Üniversitesi nerede?"
      }
    ],
    "model": "ollama:llama3.2:3b",
    "rag_enabled": true,
    "temperature": 0.1
  }'
```

#### ADIM 3: Sonucu Gösterin ve Açıklayın
🎯 **Jüriye Söyleyeceğiniz:**
> "Yanıta bakarsak, **Konya** bilgisi doğru şekilde verildi.
> Accuracy Guard modülü bu bilgiyi garanti ediyor.
> Model İzmir deseydi bile, sistem otomatik düzeltecekti."

**Beklenen Anahtar Kelimeler:**
- ✅ **"Konya"** - MUTLAKA olmalı
- ✅ "Alaeddin Keykubat" veya "Ardıçlı" kampüsü
- ❌ "İzmir", "Ankara", "İstanbul" - OLMAMALI

#### ADIM 4: (Opsiyonel) Log Gösterimi
```bash
# Ayrı terminalde backend loglarını gösterin
tail -f backend/logs/app.log | grep accuracy
```

🎯 **Jüriye Söyleyeceğiniz:**
> "Backend loglarında accuracy kontrolü görünüyor.
> Her kritik soru için bu kontrol yapılıyor."

#### ✅ SENARYO 2 BAŞARI KRİTERLERİ
- [ ] "Konya" kelimesi yanıtta var
- [ ] Yanlış şehir adı yok
- [ ] Accuracy Guard çalıştı

---

### 📌 SENARYO 3: RAG KAYNAK GÖSTERİMİ

**Amaç:** RAG sisteminin çalıştığını ve kaynak gösterdiğini kanıtlamak
**Süre:** 1.5 dakika

#### ADIM 1: Giriş
🎯 **Jüriye Söyleyeceğiniz:**
> "Şimdi RAG sistemini test edeceğim.
> Bilgisayar Mühendisliği hakkında soruyorum.
> Yanıtta kaynak referansları göreceğiz."

#### ADIM 2: Komutu Çalıştırın
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Bilgisayar Mühendisliği bölümü hakkında bilgi ver"
      }
    ],
    "model": "ollama:llama3.2:3b",
    "rag_enabled": true,
    "rag_strict": true,
    "temperature": 0.1
  }'
```

#### ADIM 3: Citations Bölümünü Gösterin
🎯 **Jüriye Söyleyeceğiniz:**
> "Yanıtın altında `citations` bölümü var.
> Burada hangi belgeden bilgi alındığı gösteriliyor.
> Bu sayede kullanıcı kaynağı doğrulayabilir."

**Beklenen Çıktı Yapısı:**
```json
{
  "content": "Bilgisayar Mühendisliği bölümü Teknoloji Fakültesi...",
  "citations": [
    {
      "source": "bolumler.json",
      "chunk": "Bilgisayar Mühendisliği..."
    }
  ]
}
```

🎯 **Vurgulayacağınız Noktalar:**
- Fakülte bilgisi doğru (Teknoloji Fakültesi)
- MÜDEK akreditasyonu varsa bahsedin
- Kaynak dosya adı görünüyor

#### ✅ SENARYO 3 BAŞARI KRİTERLERİ
- [ ] Yanıt bölüm hakkında bilgi içeriyor
- [ ] `citations` alanı dolu
- [ ] Kaynak dosya/doküman adı görünüyor

---

### 📌 SENARYO 4: STRICT MODE TESTİ

**Amaç:** Kaynak yokken uydurma yapmadığını göstermek
**Süre:** 1 dakika

#### ADIM 1: Giriş
🎯 **Jüriye Söyleyeceğiniz:**
> "Şimdi çok önemli bir özelliği test edeceğim.
> Kaynaklarda olmayan bir bilgi sorduğumda ne oluyor?
> Strict mode aktif, uydurma yapmaması gerekiyor."

#### ADIM 2: Komutu Çalıştırın
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Selçuk Üniversitesinde kaç tane roket var?"
      }
    ],
    "model": "ollama:llama3.2:3b",
    "rag_enabled": true,
    "rag_strict": true,
    "temperature": 0.1
  }'
```

#### ADIM 3: Sonucu Gösterin
🎯 **Jüriye Söyleyeceğiniz:**
> "Görüldüğü gibi sistem **uydurma yapmadı**.
> Açıkça 'Bu bilgi kaynaklarda yok' veya benzeri bir yanıt verdi.
> Bu, güvenilirlik için kritik bir özellik."

**Beklenen Yanıt (veya benzeri):**
```
"Bu bilgi kaynaklarda yok."
"Bu konuda bilgim bulunmuyor."
"Kaynaklarımda bu soruya yanıt bulamadım."
```

🎯 **Ekstra Açıklama:**
> "ChatGPT olsaydı, '15 roket var' gibi uydurma bir cevap verebilirdi.
> Bizim sistemimiz bunu **yapmıyor** çünkü akademik güvenilirlik
> en önemli önceliğimiz."

#### ✅ SENARYO 4 BAŞARI KRİTERLERİ
- [ ] Uydurma yanıt verilmedi
- [ ] "Bilmiyorum" tarzı yanıt döndü
- [ ] Jüri strict mode'u anladı

---

### 📌 SENARYO 5: KURULUŞ YILI TESTİ

**Amaç:** Başka bir kritik bilgiyi doğrulamak
**Süre:** 45 saniye

#### ADIM 1: Giriş
🎯 **Jüriye Söyleyeceğiniz:**
> "Son olarak kuruluş yılını test ediyorum.
> Bu da Accuracy Guard'ın koruduğu kritik bilgilerden biri."

#### ADIM 2: Komutu Çalıştırın
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Selçuk Üniversitesi ne zaman kuruldu?"
      }
    ],
    "model": "ollama:llama3.2:3b",
    "rag_enabled": true,
    "temperature": 0.1
  }'
```

#### ADIM 3: Sonucu Doğrulayın
🎯 **Jüriye Söyleyeceğiniz:**
> "**1975** yılı doğru şekilde verildi.
> Accuracy Guard bu bilgiyi de garanti ediyor."

**Beklenen Anahtar Kelimeler:**
- ✅ **"1975"** - MUTLAKA olmalı
- ❌ "1974", "1976", "1982" - OLMAMALI

#### ✅ SENARYO 5 BAŞARI KRİTERLERİ
- [ ] "1975" yanıtta var
- [ ] Yanlış yıl yok
- [ ] Demo tamamlandı

---

## 📱 FLUTTER APP DEMO (OPSİYONEL)

Eğer zaman varsa veya jüri isterse Flutter uygulamasını gösterin:

### ADIM 1: Uygulamayı Açın
```bash
flutter run -d chrome
```

### ADIM 2: Ana Ekranı Gösterin
🎯 **Jüriye Söyleyeceğiniz:**
> "Bu Flutter ile geliştirdiğim mobil/web uygulaması.
> Modern Material 3 tasarımı kullanıyor."

### ADIM 3: Sohbet Ekranına Gidin
🎯 **Jüriye Söyleyeceğiniz:**
> "Sohbet ekranında aynı testleri yapabiliriz.
> Arka planda aynı backend çalışıyor."

### ADIM 4: Mesaj Gönderin
- "Selçuk Üniversitesi nerede?" yazın
- Yanıtı bekleyin
- "Konya" bilgisini gösterin

🎯 **Jüriye Söyleyeceğiniz:**
> "Aynı doğruluk garantisi burada da geçerli.
> Kullanıcı dostu arayüzle aynı güçlü backend."

---

## 🚨 YEDEK PLANLAR

### PLAN A: Backend Çalışmıyor

**Belirtiler:**
- `curl` komutu timeout veriyor
- "Connection refused" hatası

**Çözüm Adımları:**
1. Sakin olun, jüriye: "Teknik bir aksaklık var, hemen çözüyorum"
2. Terminalde:
   ```bash
   cd backend
   python main.py
   ```
3. 30 saniye bekleyin
4. Tekrar deneyin

**Çözülmezse:**
- "Kayıtlı demo videom var, onu gösterebilir miyim?"
- USB'de veya laptop'ta demo.mp4 hazır olsun

---

### PLAN B: Ollama Yanıt Vermiyor

**Belirtiler:**
- Backend çalışıyor ama LLM timeout
- "Model not found" hatası

**Çözüm Adımları:**
1. Ayrı terminalde:
   ```bash
   ollama serve
   ```
2. Model kontrolü:
   ```bash
   ollama list
   ```
3. Model yoksa:
   ```bash
   ollama pull llama3.2:3b
   ```

**Çözülmezse:**
- "Model indirmesi zaman alıyor, video ile göstereyim"

---

### PLAN C: Yanlış Yanıt Geldi

**Belirtiler:**
- "İzmir" veya yanlış şehir adı geldi
- Yanlış kuruluş yılı söylendi

**Çözüm Adımları:**
1. Panik yapmayın!
2. Jüriye: "Görüldüğü gibi LLM hallucination yapabiliyor"
3. "İşte tam da bu nedenle Accuracy Guard geliştirdim"
4. Backend loglarını gösterin:
   ```bash
   grep "accuracy_guard" backend/logs/app.log
   ```
5. "Logda düzeltme kaydı var, normalde bu otomatik düzeltilir"

**Avantaja Çevirin:**
> "Bu durum projenin gerekliliğini gösteriyor.
> Accuracy Guard olmadan bu yanlış bilgi kullanıcıya giderdi."

---

### PLAN D: İnternet Yok

**Belirtiler:**
- Projeksiyon/video bağlantısı koptu
- Laptop offline

**Çözüm:**
- Tüm sistem YEREL çalışıyor, internet gerekmez
- Ollama ve backend zaten yerel
- Demo'ya devam edebilirsiniz

---

### PLAN E: Zaman Yetmiyor

**Belirtiler:**
- Demo için sadece 1-2 dakika kaldı

**Çözüm:**
- Sadece SENARYO 2'yi (Konum Sorusu) gösterin
- En önemli özellik: Doğruluk garantisi
- Diğer senaryoları atlayın

🎯 **Jüriye Söyleyeceğiniz:**
> "Zamanımız sınırlı olduğu için en kritik senaryoyu göstereyim.
> Konum sorusu ve Accuracy Guard'ı test ediyorum."

---

## 📸 DEMO SONRASI EKRAN GÖRÜNTÜLERİ

Demo sırasında şu ekran görüntülerini alın (veya önceden hazırlayın):

1. ✅ Health check başarılı
2. ✅ "Konya" yanıtı
3. ✅ Citations ile kaynak gösterimi
4. ✅ Strict mode "bilmiyorum" yanıtı
5. ✅ "1975" kuruluş yılı yanıtı
6. ✅ Backend log'unda accuracy_guard
7. ✅ Flutter app sohbet ekranı

---

## ✅ DEMO SONRASI KONTROL LİSTESİ

### Demo Başarılı mı?
- [ ] Health check çalıştı
- [ ] "Konya" bilgisi doğru verildi
- [ ] RAG kaynakları gösterildi
- [ ] Strict mode çalıştı ("bilmiyorum" dedi)
- [ ] Kuruluş yılı doğru verildi
- [ ] Jüri demo'yu anladı

### Notlar
Demo sırasında jürinin sorduğu sorular:
1. _________________________________
2. _________________________________
3. _________________________________

Demo sırasında yaşanan sorunlar:
1. _________________________________
2. _________________________________

---

## 🎯 DEMO İPUÇLARI

### ✅ YAPIN
- Her komutu **yavaş** çalıştırın, jüri okusun
- Çıktıyı **gösterin** ve **açıklayın**
- Hata olursa **sakin kalın**
- Terminal fontunu **büyük** tutun (min 14pt)
- Jüriye **göz teması** yapın, sadece ekrana bakmayın

### ❌ YAPMAYIN
- Çok hızlı komut çalıştırmayın
- Çıktıyı açıklamadan geçmeyin
- Hata olunca panik yapmayın
- Jüriyi bekletmeyin, hazır olun
- Bilmediğiniz teknik detaylara girmeyin

---

## 📚 HAZIRLIK KAYNAKLARI

Demo öncesi bu dosyaları gözden geçirin:
- `docs/DEMO_SCRIPT.md` - Eski demo script'i (referans)
- `docs/QA_PREP.md` - Jüri soruları
- `docs/JURI_HAZIRLIK.md` - Genel hazırlık
- `backend/README.md` - API endpoint'leri

---

**Bu doküman [Tarih] tarihinde hazırlanmıştır.**
**Başarılı demolar! 🚀**
