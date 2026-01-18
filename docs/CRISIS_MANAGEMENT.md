# 🚨 KRİZ YÖNETİMİ REHBERİ

> Sunum sırasında ters gidebilecek her şey için acil durum planları.
> Bu dokümanı sunum öncesi **ezberle**. Kriz anında panik yapmadan çözüm üret.

---

## 📋 İÇİNDEKİLER

1. [Teknik Krizler](#1-teknik-krizler)
2. [Sunum Krizleri](#2-sunum-krizleri)
3. [Bilgi Krizleri](#3-bilgi-krizleri)
4. [Psikolojik Krizler](#4-psikolojik-krizleri)
5. [Acil Durum Kartları](#5-acil-durum-kartları)

---

## 1️⃣ TEKNİK KRİZLER

### KRİZ 1.1: Demo Çalışmıyor (Backend Down)

**🔴 Belirti:**
- Flutter uygulaması "Bağlantı hatası" veriyor
- API yanıt vermiyor
- Mesaj gönderilemiyor

**✅ Plan A: Hızlı Restart**
1. Terminal'de `Ctrl+C` ile backend'i durdur
2. `cd backend && python -m uvicorn main:app --reload` ile yeniden başlat
3. 10 saniye bekle
4. Flutter'da tekrar dene

**✅ Plan B: Ollama Kontrol**
1. `ollama list` komutu ile modellerin varlığını kontrol et
2. `ollama run llama3.1` ile modeli manuel test et
3. Çalışıyorsa backend'i yeniden başlat

**✅ Plan C: Ekran Görüntüsü Göster**
1. Önceden hazırladığın demo video/GIF'i göster
2. "Şu an teknik bir sorun var, size önceden kaydettiğim demoyu göstereyim"

**💬 Jüriye Söyle:**
> "Şu an yerel ağda bir gecikme yaşanıyor. Ben size bu arada sistemin 
> mimarisini anlatayım, ardından demo'ya döneriz."

---

### KRİZ 1.2: Ollama Modeli Yok / Yanıt Vermiyor

**🔴 Belirti:**
- "Model not found" hatası
- Ollama timeout
- Boş yanıt

**✅ Plan A: Model Pull**
```bash
ollama pull llama3.1
```

**✅ Plan B: Alternatif Model**
```bash
ollama run qwen2.5:7b
```
Backend'de model adını değiştir.

**✅ Plan C: Kayıtlı Demo**
1. Önceden kaydedilmiş ekran görüntülerini göster
2. "Şu an model indiriliyor, size kayıtlı demo üzerinden göstereyim"

**💬 Jüriye Söyle:**
> "Yerel model şu an yüklenmiyor, muhtemelen RAM sınırlaması. 
> Size sistemin çalışma mantığını kod üzerinden göstereyim."

---

### KRİZ 1.3: Projeksiyon / Ekran Kesildi

**🔴 Belirti:**
- Ekran karardı
- Projeksiyon bağlantısı koptu
- Laptop ekranı görünmüyor

**✅ Plan A: Kablo Kontrolü**
1. HDMI/VGA kablosunu çıkar-tak
2. 5 saniye bekle

**✅ Plan B: Ekran Ayarları**
- Windows: `Win + P` → "Yalnızca İkinci Ekran" veya "Çoğalt"
- Mac: `Cmd + F1` veya Sistem Tercihleri > Ekranlar

**✅ Plan C: Laptop Ekranından Devam**
1. "Jürinin yanına geçebilir miyim?" de
2. Laptop ekranından göster

**💬 Jüriye Söyle:**
> "Teknik bir sorun yaşadık, bir saniye çözeyim. Bu arada size projenin 
> ana hedeflerinden bahsedeyim..."

---

### KRİZ 1.4: Laptop Dondu / Çöktü

**🔴 Belirti:**
- Ekran dondu
- Fare/klavye çalışmıyor
- Uygulama yanıt vermiyor

**✅ Plan A: Force Quit**
- Windows: `Ctrl + Alt + Del` → Görev Yöneticisi
- Mac: `Cmd + Option + Esc`

**✅ Plan B: Yeniden Başlat**
1. Güç tuşuna 5 saniye bas
2. Yeniden aç
3. Uygulamaları hızlıca başlat

**✅ Plan C: Telefon Demo**
1. Telefondan Flutter web versiyonunu göster
2. Veya telefondaki demo videosunu göster

**💬 Jüriye Söyle:**
> "Sistemim dondu, hemen yeniden başlatıyorum. Bu arada size projenin 
> gizlilik yaklaşımını anlatabilirim."

---

### KRİZ 1.5: İnternet Yok

**🔴 Belirti:**
- WiFi bağlantısı yok
- Hotspot çalışmıyor

**✅ Plan A: Hotspot**
1. Telefondan hotspot aç
2. Laptop'u bağla

**✅ Plan B: Offline Demo**
> "Projemizin en güçlü yanı tamamen yerel çalışması! İnternet olmadan 
> da çalıştığını göstereyim."

Ollama zaten yerel çalışıyor, demo yapılabilir.

**💬 Jüriye Söyle:**
> "İnternet bağlantısı yok ama projemiz tamamen yerel çalıştığı için 
> bu bir avantaj aslında. Göstereyim..."

---

## 2️⃣ SUNUM KRİZLERİ

### KRİZ 2.1: Süre Yetmiyor

**🔴 Belirti:**
- 10 dakika geçti, daha demo yapmadın
- Jüri "Hızlandır" diyor

**✅ Plan A: Hızlı Özet**
1. Detayları atla
2. Sadece 3 ana noktaya odaklan:
   - Yerel çalışma (gizlilik)
   - RAG teknolojisi
   - Canlı demo (1 soru)

**✅ Plan B: Demo Önceliği**
1. Slaytları atla
2. Direkt demo'ya geç
3. "Size direkt çalışan sistemi göstereyim"

**💬 Jüriye Söyle:**
> "Zamanımız sınırlı, en önemli kısma geçeyim: canlı demo."

---

### KRİZ 2.2: Süre Bitti Ama Bitiremedim

**🔴 Belirti:**
- Jüri "Süreniz doldu" dedi
- Demo gösteremedim

**✅ Plan A: Özet Kapanış**
> "Teşekkürler. Özetle: Projemiz tamamen yerel çalışan, gizlilik odaklı 
> bir akademik asistan. Sorularınızı almak isterim."

**✅ Plan B: Demo Teklifi**
> "Demo göstermek ister misiniz? 2 dakikada tamamlayabilirim."

**💬 Jüriye Söyle:**
> "Anlayışınız için teşekkürler. Kalan detayları sorularınızla 
> yanıtlayabilirim."

---

### KRİZ 2.3: Slayt Atlama Gerekti

**🔴 Belirti:**
- Jüri sıkıldı
- Detaylara gerek yok

**✅ Plan A: Özet Slaytına Git**
1. Slayt 13 "Sonuç" slaytına atla
2. 3 ana maddeyi özetle

**✅ Plan B: Demo'ya Git**
1. "Size direkt sistemi göstereyim" de
2. Demo slaytına (Slayt 11) atla

**💬 Jüriye Söyle:**
> "Teknik detayları atlayıp size çalışan sistemi göstereyim."

---

### KRİZ 2.4: Jüri Çok Soru Soruyor (Sunumu Kesiyor)

**🔴 Belirti:**
- Her slayttan sonra soru geliyor
- Sunumu tamamlayamıyorsun

**✅ Plan A: Not Al, Sonra Cevapla**
> "Çok güzel soru, bunu not alayım ve sunum sonunda detaylı cevaplayayım."

**✅ Plan B: Kısa Cevap Ver**
1. Tek cümleyle cevapla
2. "Detayını demo'da göstereceğim" de

**💬 Jüriye Söyle:**
> "Bu soruyu not aldım, demo kısmında detaylı göstereceğim."

---

## 3️⃣ BİLGİ KRİZLERİ

### KRİZ 3.1: Cevabı Bilmiyorum

**🔴 Belirti:**
- Jüri teknik bir soru sordu
- Cevabı bilmiyorsun

**✅ Plan A: Dürüst Ol**
> "Bu konuyu detaylı araştırmadım, ama genel olarak şöyle 
> çalıştığını biliyorum..."

**✅ Plan B: İlişkili Bilgi Ver**
> "Tam o konuyu bilmiyorum ama benzer bir konu olan X hakkında 
> şunu söyleyebilirim..."

**✅ Plan C: Araştırma Sözü**
> "Bu çok güzel bir soru. Detaylı araştırıp size mail atabilirim."

**💬 Jüriye Söyle:**
> "Dürüst olmak gerekirse bu detayı bilmiyorum. Ama projenin genel 
> mantığı şöyle çalışıyor..."

**❌ YAPMA:**
- Uydurma
- Panikle yanlış bilgi verme
- "Hiçbir fikrim yok" deme

---

### KRİZ 3.2: Kod Satırı Hatırlamıyorum

**🔴 Belirti:**
- "Şu dosyanın X. satırı ne yapıyor?" sorusu
- Tam hatırlamıyorsun

**✅ Plan A: Genel Açıklama**
> "O dosya genel olarak şu işi yapıyor... Tam satır numarasını 
> hatırlamıyorum ama fonksiyonun amacı şu..."

**✅ Plan B: Kod Göster**
> "Bir saniye koda bakayım" (IDE'yi aç, dosyayı bul)

**✅ Plan C: Dokümantasyon Referansı**
> "Bu fonksiyonun detaylı açıklaması kodun başındaki docstring'de var."

**💬 Jüriye Söyle:**
> "Tam satır numarasını hatırlamıyorum ama o bölümde [X işlemi] 
> yapılıyor. İsterseniz kodu açıp gösterebilirim."

---

### KRİZ 3.3: Rakam/İstatistik Emin Değilim

**🔴 Belirti:**
- "Test coverage kaç?" sorusu
- Kesin sayıyı bilmiyorsun

**✅ Plan A: Yaklaşık Ver**
> "Kesin rakamı hatırlamıyorum ama yaklaşık %80 civarında."

**✅ Plan B: Göster**
> "Bir saniye, size direkt test sonuçlarını göstereyim."

**💬 Jüriye Söyle:**
> "Kesin rakamı doğrulamak için test raporuna bakayım..."

---

## 4️⃣ PSİKOLOJİK KRİZLER

### KRİZ 4.1: Heyecandan Dondum

**🔴 Belirti:**
- Kelimeler gelmiyor
- Beyaz beyaz bakıyorsun
- Eller titriyor

**✅ Plan A: Derin Nefes**
1. 3 saniye derin nefes al
2. Suyu iç (varsa)
3. Notlarına bak

**✅ Plan B: Açık Ol**
> "Bir saniye, çok heyecanlandım. Notlarıma bakayım."

**✅ Plan C: Slayta Odaklan**
1. Slaytı oku (ayıp değil)
2. Okurken sakinleş
3. Devam et

**💬 Jüriye Söyle:**
> "Kusura bakmayın, biraz heyecanlandım. Bir saniye toparlayayım."

**🧘 Sakinleşme Teknikleri:**
- 4-7-8 Nefes: 4 saniye nefes al, 7 saniye tut, 8 saniye ver
- Ayaklarını hisset (grounding)
- "Ben bunu biliyorum" diye içinden tekrarla

---

### KRİZ 4.2: Yanlış Cevap Verdim

**🔴 Belirti:**
- Jüri düzeltti
- Yanlış bilgi verdiğini fark ettin

**✅ Plan A: Düzelt ve Devam**
> "Haklısınız, yanlış söyledim. Doğrusu şöyle..."

**✅ Plan B: Teşekkür Et**
> "Düzeltme için teşekkürler, haklısınız."

**💬 Jüriye Söyle:**
> "Özür dilerim, karıştırdım. Doğrusu şöyle..."

**❌ YAPMA:**
- Savunmaya geçme
- Tartışma
- "Ben öyle demedim" deme

---

### KRİZ 4.3: Jüri Eleştiri Yaptı

**🔴 Belirti:**
- "Bu yaklaşım yanlış" dedi
- "Neden X yapmadın?" diye sordu
- Sert bir üslup kullandı

**✅ Plan A: Dinle ve Kabul Et**
> "Çok haklısınız, bu bir geliştirme alanı. Gelecek versiyonda 
> bunu düşüneceğim."

**✅ Plan B: Açıkla (Savunmadan)**
> "O konuda şöyle bir karar verdim: [neden]. Ama haklısınız, 
> alternatif yaklaşım da değerlendirilmeli."

**💬 Jüriye Söyle:**
> "Bu çok değerli bir geri bildirim, teşekkür ederim. 
> Kesinlikle üzerinde çalışacağım."

**❌ YAPMA:**
- Alınma
- Savunmaya geçme
- Karşı çıkma

---

### KRİZ 4.4: Sesim Çıkmıyor / Titriyor

**🔴 Belirti:**
- Ses kısık
- Ses titriyor
- Boğazın kurudu

**✅ Plan A: Su İç**
1. "Bir saniye su içeyim" de
2. Yavaşça su iç
3. Derin nefes al

**✅ Plan B: Yavaşla**
1. Konuşma hızını düşür
2. Her kelimeyi net söyle
3. Duraklama yap

**💬 Jüriye Söyle:**
> "Kusura bakmayın, biraz su içeyim." (Normal bir şey)

---

## 5️⃣ ACİL DURUM KARTLARI

Bu kartları telefonuna kaydet veya yazdırıp yanında taşı:

### 🆘 KART 1: DEMO ÇALIŞMIYOR
```
1. "Teknik sorun var, bir saniye"
2. Backend restart: Ctrl+C → python -m uvicorn main:app --reload
3. Çalışmazsa: "Size kayıtlı demoyu göstereyim"
4. Devam: Mimariyi anlat
```

### 🆘 KART 2: CEVABI BİLMİYORUM
```
1. "Güzel soru"
2. "Bu detayı araştırmadım ama..."
3. İlişkili bir şey söyle
4. "Araştırıp mail atabilirim"
```

### 🆘 KART 3: DONDUM
```
1. Derin nefes (4 saniye)
2. Su iç
3. Notlara bak
4. Slaytı oku
5. "Heyecanlandım, toparlayayım"
```

### 🆘 KART 4: SÜRE YETMİYOR
```
1. Detayları atla
2. 3 ana noktaya odaklan:
   - Yerel çalışma
   - RAG
   - Demo (1 soru)
3. "Kalan detayları sorularınızla yanıtlayabilirim"
```

### 🆘 KART 5: JÜRİ ELEŞTİRDİ
```
1. "Haklısınız"
2. "Değerli geri bildirim"
3. "Gelecek versiyonda düşüneceğim"
4. GÜlümse, devam et
```

---

## 📱 ACİL İLETİŞİM

Sunum öncesi bunları hazırla:
- [ ] Hotspot açık (telefon)
- [ ] Demo videosu telefonda
- [ ] Notlar cebinde
- [ ] Su yanında
- [ ] Yedek laptop (varsa)

---

## 🧘 SON SÖZ

**Unutma:**
1. Herkes hata yapar, önemli olan toparlamak
2. Jüri seni desteklemek istiyor
3. Dürüstlük her zaman kazandırır
4. En kötü senaryoda bile "öğrendim" de

**Mantra:**
> "Ben bu projeyi yaptım. Ben biliyorum. Kriz olursa çözerim."

---

*Bu doküman en az 3 kez okunmalı ve kritik kartlar ezberlenmelidir.*
