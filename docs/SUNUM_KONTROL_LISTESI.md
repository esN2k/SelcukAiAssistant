# SUNUM KONTROL L

İSTESİ
## Final Sunum Öncesi Kontrol

**Sunum Tarihi**: [Tarih]  
**Sunum Saati**: [Saat]  
**Yer**: [Salon/Oda]

---

## 📄 DÖKÜMANLAR

- [ ] Tez raporu yazdırıldı (3 kopya: jüri üyeleri için)
- [ ] Sunum PDF export edildi
- [ ] USB'de yedek dosyalar kopyalandı
- [ ] GitHub repo erişilebilir durumda
- [ ] Demo video hazır (internet kesilirse)
- [ ] Proje dokümantasyonu güncel

---

## 💻 TEKNİK HAZIRLIK

### Donanım
- [ ] Laptop tam şarjlı (%100)
- [ ] Güç adaptörü yanımda
- [ ] HDMI kablosu test edildi
- [ ] Mouse çalışıyor
- [ ] Yedek laptop hazır (opsiyonel)

### Yazılım
- [ ] Backend çalışıyor (`python main.py`)
- [ ] Frontend çalışıyor (`flutter run`)
- [ ] Ollama servisi aktif (`ollama serve`)
- [ ] Model yüklü (`ollama list`)
- [ ] ChromaDB hazır (rag_service.py)
- [ ] İnternet bağlantısı test edildi

### Demo Hazırlığı
- [ ] Test kullanıcısı oluşturuldu
- [ ] Demo senaryosu hazır
- [ ] 3-5 örnek soru listesi
- [ ] Ekran kayıt yazılımı hazır (OBS/QuickTime)

---

## 🎤 SUNUM İÇERİĞİ

### Dosyalar
- [ ] SUNUM.md dosyası güncel
- [ ] SUNUM_KONUSMA_NOTLARI.md yazdırıldı
- [ ] QA_HAZIRLIK.md gözden geçirildi
- [ ] Slaytlar PDF'e çevrildi

### Zaman Yönetimi
- [ ] Toplam süre: 25 dakika
- [ ] Giriş: 3 dakika
- [ ] Literatür: 4 dakika
- [ ] Yöntem: 6 dakika
- [ ] Uygulama: 5 dakika
- [ ] Sonuçlar: 4 dakika
- [ ] Demo: 3 dakika

### Önemli Noktalar
- [ ] %96 doğruluk vurgusu
- [ ] RAG + Fine-Tuning hibrit yaklaşım
- [ ] Gizlilik odaklı (tamamen yerel)
- [ ] 6 platform desteği
- [ ] Açık kaynak katkı

---

## 👔 KİŞİSEL HAZIRLIK

### Kıyafet ve Görünüm
- [ ] Formal kıyafet (takım elbise/gömlek)
- [ ] Ayakkabılar temiz
- [ ] Saç/sakal düzenli
- [ ] Gerekli belgeler yanımda (kimlik, öğrenci kartı)

### Malzemeler
- [ ] Sunum notları yazdırıldı
- [ ] Kalem ve not kağıdı
- [ ] Su şişesi
- [ ] Zaman tutucu (saat/telefon)
- [ ] Yedek kalem

### Mental Hazırlık
- [ ] Sunumu en az 2 kez prova ettim
- [ ] Muhtemel sorulara hazırlandım
- [ ] Rahatım ve kendime güveniyorum
- [ ] Sabah iyi bir kahvaltı yaptım

---

## 🧪 DEMO SENARYOSU

### Adım Adım
1. [ ] Uygulamayı aç (Flutter desktop/web)
2. [ ] Giriş yap (test hesabı: demo@selcuk.edu.tr)
3. [ ] Ana ekranı göster (chat interface)
4. [ ] **Soru 1**: "Final sınavları ne zaman?"
5. [ ] Streaming yanıt göster
6. [ ] Kaynak gösterimini vurgula
7. [ ] **Soru 2**: "Bilgisayar Mühendisliği hangi fakültede?"
8. [ ] RAG'ın doküman bulduğunu göster
9. [ ] **Çeviri**: Türkçe → İngilizce örnek
10. [ ] Sohbet geçmişini göster
11. [ ] Uygulamayı kapat

### Yedek Planlar
- [ ] İnternet kesilirse: Ekran videosu oynat
- [ ] Backend çökerse: Önceden kaydedilmiş demo
- [ ] Frontend hata verirse: Screenshot'ları göster

---

## 📞 ACİL DURUM PLANLARI

### Teknik Sorunlar

**Senaryo 1: Laptop açılmıyor**
→ Yedek laptop kullan veya USB'den sunumu başka bilgisayarda aç

**Senaryo 2: Projeksiyon çalışmıyor**
→ Laptop ekranından göster veya sözlü anlatım yap

**Senaryo 3: İnternet yok**
→ Offline demo (cached data) veya ekran videosu

**Senaryo 4: Backend çöktü**
→ Önceden kaydedilmiş demo videosu oynat

**Senaryo 5: Zaman yetersiz**
→ Demo'yu kısalt, sadece core features göster

### İletişim

- [ ] Danışman: [Telefon numarası]
- [ ] IT Destek: [Telefon numarası]
- [ ] Arkadaş (yedek): [Telefon numarası]
- [ ] Sunum salonu: [Yer bilgisi]

---

## ⏰ ZAMAN ÇİZELGESİ

### Sunum Günü

**2 Saat Önce**:
- [ ] Tüm sistemleri test et
- [ ] Sunumu bir kez daha gözden geçir
- [ ] WC molası ver
- [ ] Su doldur

**1 Saat Önce**:
- [ ] Salona git, ekipmanları test et
- [ ] HDMI bağlantısını dene
- [ ] Sesin çalıştığını kontrol et
- [ ] Demo uygulamasını aç, test et

**30 Dakika Önce**:
- [ ] Derin nefes al, rahatla
- [ ] Sunum notlarını gözden geçir
- [ ] Telefonu sessiz moda al
- [ ] Pozitif düşün!

**Sunum Başlamadan**:
- [ ] Jüri üyelerini selamla
- [ ] Dökümanları dağıt
- [ ] Mikrofon test et (varsa)
- [ ] Son bir derin nefes!

---

## 📊 DEMO SÜRECİ DETAYLI

### Hazırlık (30 saniye)
```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend  
cd ..
flutter run -d windows
```

### Demo Flow (3 dakika)

**00:00-00:30**: Giriş ve ana ekran
- Login ekranını göster
- Giriş yap (test kullanıcısı)
- Ana chat ekranına geç

**00:30-01:30**: Soru-Cevap Örneği
- "Final sınavları ne zaman?" yaz
- Streaming yanıtı göster
- Kaynakları vurgula
- "Harika! Kaynak gösterimi var" de

**01:30-02:15**: RAG Demonstrasyonu
- "Bilgisayar Mühendisliği hangi kampüste?" sor
- RAG'ın doküman bulduğunu göster
- Retrieved documents'ı göster (eğer UI'da varsa)

**02:15-02:45**: Çeviri Özelliği
- Translate ekranına geç
- "Selçuk Üniversitesi Konya'dadır" → İngilizce
- Sonucu göster

**02:45-03:00**: Kapanış
- Sohbet geçmişini göster
- "Teşekkürler!" de
- Uygulamayı kapat

---

## 🎯 ÖNEMLI VURGULAR

### Mutlaka Söyle

✅ **"Tamamen yerel çalışıyor, veri dışarı çıkmıyor"**  
✅ **"%96 doğruluk oranı, base modelden %30 daha iyi"**  
✅ **"RAG + Fine-Tuning hibrit yaklaşımı kullandık"**  
✅ **"6 farklı platformda çalışıyor"**  
✅ **"Açık kaynak olarak GitHub'da paylaştık"**

### Dikkat Et

⚠️ Çok hızlı konuşma  
⚠️ Teknik jargon fazla kullanma  
⚠️ Zamanı aşma (25 dakika max)  
⚠️ Demo'da panikle, sakin kal  
⚠️ Soruları cevaplarken savunmacı olma

---

## 📝 SON KONTROL

### 5 Dakika Önce

- [ ] Telefon sessiz
- [ ] Su şişesi dolu
- [ ] Sunum notları elimde
- [ ] Laptop açık ve hazır
- [ ] HDMI bağlı
- [ ] Demo çalışıyor
- [ ] Derin nefes aldım
- [ ] Pozitif ve hazırım! 💪

---

## 💬 KENDİNE NOT

> "Sen bunu yapabilirsin! Aylarca çalıştın, her şey hazır. 
> Sadece bildiğini anlat, rahat ol. Jüri senin başarını görmek istiyor.
> İyi şanslar! 🚀"

---

**Her Şey Hazır, Başarılar! 🎉**

---

*Son Güncelleme: 17 Ocak 2026*
