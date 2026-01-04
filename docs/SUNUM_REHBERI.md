# PowerPoint Sunum Rehberi
# Selçuk Üniversitesi AI Asistan Projesi

## 📊 Sunum Yapısı (15-20 Slayt Önerisi)

### 1. Kapak Slaytı
**İçerik:**
- Proje Adı: "Selçuk AI Akademik Asistan"
- Alt Başlık: "Gizlilik Odaklı Yerel Yapay Zeka Asistanı"
- Ders: Bilgisayar Mühendisliği Uygulamaları
- Takım Üyeleri
- Tarih
- Selçuk Üniversitesi Logosu

**Tasarım Önerileri:**
- Canva'da profesyonel bir şablon seçin (örn: "University Presentation" teması)
- Selçuk Üniversitesi renklerini kullanın (mavi/beyaz tonları)
- Arka planda hafif bir üniversite görseli

---

### 2. Projenin Amacı ve Motivasyon
**İçerik:**
- **Problem:** Öğrencilerin akademik bilgilere erişim zorluğu
- **Çözüm:** Selçuk Üniversitesi'ne özel AI asistan
- **Temel Özellikler:**
  - ✅ Veri Gizliliği (Yerel LLM kullanımı)
  - ✅ Doğru ve Güvenilir Bilgi
  - ✅ 7/24 Erişilebilir
  - ✅ Kaynak Gösterimli Yanıtlar (RAG)

**Animasyon:** Madde işaretlerini tek tek belirme animasyonu
**Görsel:** Öğrenci + AI + Üniversite ikonları

---

### 3. Projenin Önemi ve Benzersizliği
**İçerik:**
- **Neden Önemli?**
  - Öğrenci memnuniyetini artırır
  - Akademik personelin iş yükünü azaltır
  - Bilgiye anında erişim sağlar
  
- **Diğer Projelerden Farkı:**
  - ❌ Google Gemini gibi dış servislere bağımlı DEĞİL
  - ✅ Tamamen yerel (Ollama + Llama 3.1)
  - ✅ Selçuk Üniversitesi'ne özel verilerle eğitilmiş
  - ✅ RAG ile kaynak gösterebilir

**Animasyon:** Karşılaştırma tablosu için wipe animasyonu
**Görsel:** Yerel vs. Cloud karşılaştırması

---

### 4. Teknoloji Mimarisi
**İçerik:**
```
┌─────────────┐
│   Flutter   │ ← Kullanıcı Arayüzü (iOS/Android/Web)
│   Frontend  │
└──────┬──────┘
       │ HTTP/SSE
┌──────▼──────┐
│   FastAPI   │ ← Python Backend
│   Backend   │
└──┬───────┬──┘
   │       │
   ▼       ▼
┌──────┐ ┌──────┐
│Ollama│ │ RAG  │ ← Yerel LLM + Kaynak Arama
│Llama │ │FAISS │
└──────┘ └──────┘
```

**Teknoloji Yığını:**
- **Frontend:** Flutter + GetX
- **Backend:** Python + FastAPI
- **LLM:** Ollama (Llama 3.1 / Qwen2)
- **RAG:** LangChain + FAISS + ChromaDB
- **Veritabanı:** Opsiyonel Appwrite

**Animasyon:** Mimari şeması için morph/fade animasyonu
**Görsel:** Sistem mimarisi diyagramı

---

### 5. Temel Özellikler - Gizlilik (Privacy)
**İçerik:**
- **Yerel İşleme:** Tüm veriler kullanıcının cihazında/üniversite sunucusunda işlenir
- **Dış Servise Bağımlılık Yok:** Google, OpenAI gibi servislere veri gönderilmez
- **KVKK Uyumlu:** Kişisel veri koruması sağlanır
- **İnternet Kesintisinde Çalışır:** Temel sohbet özellikleri offline kullanılabilir

**Animasyon:** Güvenlik kilitlerinin açılması animasyonu
**Görsel:** Güvenlik/gizlilik ikonları

---

### 6. Temel Özellikler - RAG (Retrieval-Augmented Generation)
**İçerik:**
- **RAG Nedir?**
  - Yapay zekanın yanıtlarını belgelerle destekleme sistemi
  - Uydurma bilgi riskini azaltır
  - Kaynağı gösterir → Doğrulanabilir
  
- **Nasıl Çalışır?**
  1. Soru gelir
  2. İlgili belge parçaları bulunur (FAISS vektör arama)
  3. Belgeler + Soru → LLM'e gönderilir
  4. Kaynaklı yanıt üretilir

**Animasyon:** RAG akış şeması için adım adım belirme
**Görsel:** RAG süreci akış diyagramı

---

### 7. Kullanıcı Arayüzü - Ana Ekran
**İçerik:**
- Mobil ve Web uyumlu
- Sohbet arayüzü
- Markdown formatında yanıtlar
- Kaynak gösterim bölümü

**Görsel:** Ana ekran ekran görüntüleri (iOS, Android, Web)
**Animasyon:** Ekranlar arası geçiş animasyonu

---

### 8. Kullanıcı Arayüzü - Özellikler Ekranı
**İçerik:**
- Model seçimi (Ollama/HuggingFace)
- RAG açma/kapama
- Parametre ayarları (temperature, top_p)
- Tema seçimi (light/dark)

**Görsel:** Ayarlar ekranı ekran görüntüsü
**Animasyon:** Ayar panellerinin açılması

---

### 9. Backend API Yapısı
**İçerik:**
```
Endpoint'ler:
- GET  /              → Sağlık kontrolü
- GET  /health        → Detaylı durum
- GET  /health/ollama → Ollama sağlığı
- GET  /models        → Mevcut modeller
- POST /chat          → Tek yanıt
- POST /chat/stream   → Akış yanıtı (SSE)
```

**Özellikler:**
- RESTful API
- Server-Sent Events (SSE) ile gerçek zamanlı akış
- CORS desteği
- Hata yönetimi ve loglama

**Animasyon:** API endpoint listesi için liste animasyonu
**Görsel:** API request/response örneği

---

### 10. Veri Kaynakları ve Eğitim
**İçerik:**
- **Manuel Doğrulanmış Veriler:**
  - `selcuk_data.py` → Kritik bilgiler (Konya, 1975, vb.)
  - Q&A çiftleri (75+ soru-cevap)
  
- **Web Scraping:**
  - `scrape_selcuk_edu.py` → Resmi web sitesinden veri toplama
  - `scrape_bilgisayar.py` → Bölüm sayfası kazıma
  
- **RAG Dokümanları:**
  - Genel bilgiler
  - Bilgisayar Mühendisliği detayları
  - SSS (Sıkça Sorulan Sorular)

**Animasyon:** Veri akışı diyagramı
**Görsel:** Veri toplama süreci

---

### 11. Kalite Güvencesi ve Testler
**İçerik:**
- **CI/CD Pipeline:**
  - ✅ Backend CI (pytest, ruff, mypy)
  - ✅ Flutter Build (flutter analyze, flutter test)
  
- **Test Kapsamı:**
  - Birim testler
  - Entegrasyon testleri
  - API testleri
  - Encoding testleri (Türkçe karakter desteği)

- **Kod Kalitesi:**
  - Ruff (linting)
  - Mypy (type checking)
  - Test coverage

**Animasyon:** Test geçişlerini gösteren tick animasyonları
**Görsel:** CI/CD pipeline diyagramı veya test sonuçları

---

### 12. Performans ve Optimizasyon
**İçerik:**
- **Model Performansı:**
  - Llama 3.1 (3B): ~2-3 saniye yanıt süresi
  - Qwen2 (7B): ~5-8 saniye yanıt süresi
  
- **Optimizasyonlar:**
  - Akış yanıtı (streaming) → Kullanıcı hemen görebilir
  - Bağlam budama → Token limiti yönetimi
  - FAISS vektör araması → Hızlı RAG
  - Response cleaning → Düşünce bloklarını filtreleme

**Animasyon:** Performans grafikleri
**Görsel:** Yanıt süresi karşılaştırmaları

---

### 13. Güvenlik Özellikleri
**İçerik:**
- **Veri Güvenliği:**
  - Kişisel veri toplama yok
  - Sohbet kayıtları opsiyonel (Appwrite)
  
- **API Güvenliği:**
  - CORS politikaları
  - Input sanitization
  - Rate limiting (gelecek sürüm)
  
- **Model Güvenliği:**
  - Prompt injection koruması
  - Düşünce blokları filtreleme
  - Hata mesajları sanitizasyonu

**Animasyon:** Güvenlik katmanlarının oluşması
**Görsel:** Güvenlik mimarisi

---

### 14. Kullanım Senaryoları ve Demo
**İçerik:**
**Senaryo 1:** Öğrenci Bilgi Talebi
```
Soru: "Bilgisayar Mühendisliği hangi kampusta?"
Yanıt: "Alaeddin Keykubat Yerleşkesi, Konya"
```

**Senaryo 2:** Akreditasyon Sorgusu
```
Soru: "Bölüm akredite mi?"
Yanıt: "Evet, MÜDEK akreditasyonuna sahip"
```

**Senaryo 3:** RAG ile Kaynaklı Yanıt
```
Soru: "Erasmus programı var mı?"
Yanıt: "Evet, Erasmus+ programı mevcut"
Kaynak: [02_bilgisayar_muhendisligi.txt]
```

**Animasyon:** Sohbet baloncukları animasyonu
**Görsel:** Gerçek uygulama ekran görüntüleri

---

### 15. Sorunlar ve Çözümler
**İçerik:**
| Sorun | Çözüm |
|-------|-------|
| Yanlış bilgi (İzmir vs Konya) | ✅ System prompt'a kritik bilgiler eklendi |
| Model hallüsinasyonu | ✅ RAG ile kaynak gösterim zorunlu hale getirildi |
| Türkçe karakter sorunu | ✅ UTF-8 encoding guard testleri eklendi |
| Yavaş yanıt süresi | ✅ Streaming response implementasyonu |

**Animasyon:** Sorun → Çözüm ok animasyonu
**Görsel:** Before/After karşılaştırması

---

### 16. Gelecek Geliştirmeler (Roadmap)
**İçerik:**
- **Kısa Vadeli (1 ay):**
  - [ ] Daha fazla bölüm verisi ekleme
  - [ ] Fine-tuning ile model özelleştirme
  - [ ] Sesli asistan desteği
  
- **Orta Vadeli (3 ay):**
  - [ ] Çoklu dil desteği (İngilizce)
  - [ ] Akademik takvim entegrasyonu
  - [ ] Push notification desteği
  
- **Uzun Vadeli (6 ay+):**
  - [ ] Kişiselleştirilmiş öğrenci profilleri
  - [ ] Ders içerik analizi
  - [ ] Sınav hazırlık asistanı

**Animasyon:** Timeline animasyonu
**Görsel:** Roadmap zaman çizelgesi

---

### 17. Projenin Kazanımları
**İçerik:**
- **Teknik Kazanımlar:**
  - Flutter cross-platform development
  - Python FastAPI backend geliştirme
  - LLM entegrasyonu (Ollama, HuggingFace)
  - RAG sistemi implementasyonu
  - CI/CD pipeline kurulumu
  
- **Proje Yönetimi:**
  - Agile metodolojisi
  - Git version control
  - Dokümantasyon yazımı
  - Test-driven development

**Animasyon:** Kazanım listesi için progressive reveal
**Görsel:** Öğrenilen teknolojilerin logoları

---

### 18. Ekip ve Katkılar
**İçerik:**
- Ekip üyeleri ve rolleri
- Her üyenin katkıları
- Danışman hoca
- Teşekkürler

**Animasyon:** Ekip üyelerinin fotoğrafları için fade-in
**Görsel:** Ekip fotoğrafı veya avatarları

---

### 19. Sonuç
**İçerik:**
- **Proje Başarıları:**
  - ✅ Çalışan yerel AI asistan
  - ✅ Gizlilik odaklı mimari
  - ✅ RAG ile doğru bilgi
  - ✅ Cross-platform destek
  - ✅ Kalite güvencesi (CI/CD)
  
- **Öğrenilen Dersler:**
  - LLM'ler güçlü ama hallüsinasyon riski var
  - RAG bu riski önemli ölçüde azaltır
  - Yerel deployment, gizlilik için kritik
  - Test ve CI/CD, kalite için vazgeçilmez

**Animasyon:** Başarı checklist animasyonu
**Görsel:** Proje özet infografiği

---

### 20. Demo ve Sorular
**İçerik:**
- **Canlı Demo:**
  - Mobil uygulamayı açma
  - Örnek soru sorma
  - RAG özelliğini gösterme
  - Ayarları gösterme
  
- **QR Kod:**
  - GitHub repository
  - Demo video linki
  - Dokümantasyon linki

- **Soru-Cevap**

**Animasyon:** QR kod'un ortaya çıkması
**Görsel:** QR kodlar, Demo ekran kaydı

---

## 🎨 Canva Tasarım İpuçları

### Renk Paleti
- **Ana Renk:** Selçuk Üniversitesi mavi (#0066CC veya benzeri)
- **Vurgu Rengi:** Turuncu/sarı (#FFA500)
- **Metin:** Koyu gri (#333333)
- **Arka Plan:** Beyaz/açık gri (#F5F5F5)

### Font Seçimi
- **Başlık:** Montserrat Bold / Raleway Bold
- **Metin:** Open Sans / Roboto
- **Kod:** Courier New / Consolas

### Görsel Öğeler
- **İkonlar:** Flaticon, Font Awesome (ücretsiz)
- **İllüstrasyonlar:** unDraw (AI, teknoloji temalı)
- **Fotoğraflar:** Unsplash (üniversite, teknoloji görselleri)

### Animasyonlar
1. **Giriş Animasyonları:**
   - Fade In (genel içerik için)
   - Slide In (yan paneller için)
   - Rise Up (başlıklar için)

2. **Vurgu Animasyonları:**
   - Pulse (önemli noktalar)
   - Bounce (başarı ikonları)
   - Grow (grafikler)

3. **Geçiş Animasyonları:**
   - Dissolve (slaytlar arası)
   - Push (bölüm geçişleri)

### Layout Önerileri
- Her slayt için maksimum 5-7 madde
- Bol beyaz alan bırakın
- Görseller ve metin dengesini koruyun
- Tutarlı layout kullanın (template)

---

## 📝 Sunum Notları

### Açılış (1-2 dk)
- Kendini tanıtma
- Projeye genel bakış
- Sunum akışı

### Ana Bölüm (12-15 dk)
- Problem ve çözüm (2 dk)
- Teknoloji ve mimari (3 dk)
- Özellikler ve demo (4 dk)
- Testler ve kalite (2 dk)
- Sonuçlar (2 dk)

### Kapanış (2-3 dk)
- Canlı demo (2 dk)
- Sorular (sınırsız)

### Konuşma İpuçları
- Jüri ile göz teması kurun
- Yavaş ve net konuşun
- Teknik terimleri açıklayın
- Demo için yedek plan hazırlayın (ekran kaydı)
- Sorulara hazırlıklı olun

---

## 🎯 Sık Sorulan Sorular (Hazırlık)

**S: Neden Google Gemini yerine yerel LLM?**
C: Veri gizliliği, maliyet kontrolü, internet bağımsızlığı

**S: Model hallüsinasyon yapıyor mu?**
C: RAG kullanımıyla hallüsinasyon riski minimuma indi, kaynak gösterim zorunlu

**S: Performans nasıl?**
C: 3B model 2-3 saniye, 7B model 5-8 saniye. Streaming ile kullanıcı deneyimi iyi.

**S: Gerçek kullanıcılarda test edildi mi?**
C: Alpha testing yapıldı, beta için planlama var

**S: Maliyet?**
C: Açık kaynak araçlar kullanıldı, sadece sunucu maliyeti var

**S: Diğer üniversiteler kullanabilir mi?**
C: Evet, açık kaynak. Sadece veri değiştirilmeli.

---

## 📦 Kaynaklar

- **Canva Şablonları:** https://www.canva.com/templates/presentations/
- **İkonlar:** https://www.flaticon.com/, https://fontawesome.com/
- **İllüstrasyonlar:** https://undraw.co/illustrations
- **Renkler:** https://coolors.co/
- **Ekran Kaydı:** OBS Studio, Loom
- **QR Kod:** https://www.qr-code-generator.com/

---

Bu rehber, profesyonel ve etkileyici bir sunum hazırlamanıza yardımcı olacaktır. Başarılar!
