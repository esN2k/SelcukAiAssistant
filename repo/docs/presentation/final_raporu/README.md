# Selçuk Üniversitesi Bitirme Projesi Raporu

## 📋 Genel Bakış

Bu klasör, "Yapay Zeka Destekli Üniversite Bilgi Asistanı: Selçuk AI Asistan" projesinin bitirme raporu dosyalarını içermektedir.

## 📂 Dosyalar

### 1. `BITIRME_PROJESI_RAPORU.md`
- **Açıklama:** Markdown formatında hazırlanmış, 60-80 sayfalık kapsamlı bitirme projesi raporu
- **İçerik:** Proje şablonuna uygun olarak hazırlanmış tüm bölümler (kısmen)
- **Kullanım:** Bu dosya, Word/PDF'e dönüştürülebilir veya doğrudan okunabilir

### 2. `generate_final_report.py`
- **Açıklama:** Şablona uygun Word dökümanı üreten Python scripti
- **Kullanım:**
  ```bash
  python3 generate_final_report.py
  ```
- **Çıktı:** `Selcuk_AI_Asistan_Bitirme_Raporu_Part1.docx` (ön kısım sayfaları)

### 3. `Selcuk_AI_Asistan_Bitirme_Raporu_Part1.docx`
- **Açıklama:** Otomatik üretilen Word dökümanı (ön kısım)
- **İçerik:**
  - İç Kapak
  - Onay Sayfası
  - Proje Bildirimi
  - Özet (Türkçe)
  - Abstract (İngilizce)
  - Önsöz
  - İçindekiler
  - Simgeler ve Kısaltmalar

## 📝 Format Özellikleri

### Sayfa Düzeni
- **Kağıt:** A4 (21 x 29.7 cm)
- **Sol Kenar:** 3.5 cm
- **Diğer Kenarlar:** 2.5 cm
- **Yazı Tipi:** Times New Roman
- **Yazı Boyutu:** 12 pt (metin), 10 pt (özet, tablo)
- **Satır Aralığı:** 1.5 (metin), 1.0 (özet, tablo, kaynaklar)

### Sayfa Numaralandırma
- **Ön Kısım:** Küçük Romen rakamları (i, ii, iii, iv, v, vi, vii, viii, ix...)
  - İç Kapak, Onay, Bildirimi: Numarasız (ama i, ii, iii olarak sayılır)
  - Özet'ten başlayarak numara gösterilir
- **Ana Bölümler:** Arapça rakamlar (1, 2, 3, 4...), sağ üst köşe

## 📖 Rapor Yapısı

### ÖN KISIM (Romen sayfa no)
- [x] İç Kapak
- [x] Onay Sayfası
- [x] Proje Bildirimi
- [x] Özet (Türkçe, 10pt)
- [x] Abstract (İngilizce, 10pt)
- [x] Önsöz
- [x] İçindekiler
- [x] Simgeler ve Kısaltmalar

### ANA BÖLÜMLER (Arapça sayfa no)
- [ ] 1. GİRİŞ
  - [ ] 1.1. Projenin Arka Planı
  - [ ] 1.2. Projenin Önemi
  - [ ] 1.3. Projenin Kapsamı
  - [ ] 1.4. Raporun Organizasyonu

- [ ] 2. KAYNAK ARAŞTIRMASI
  - [ ] 2.1. Yapay Zeka ve Doğal Dil İşleme Tarihi
  - [ ] 2.2. Büyük Dil Modelleri (LLM)
  - [ ] 2.3. Yerel LLM Çözümleri ve Ollama
  - [ ] 2.4. RAG (Retrieval-Augmented Generation)
  - [ ] 2.5. Flutter ve Mobil Uygulama Geliştirme
  - [ ] 2.6. Üniversite Chatbot Örnekleri

- [ ] 3. MATERYAL VE YÖNTEM
  - [ ] 3.1. Geliştirme Metodolojisi
  - [ ] 3.2. Veri Toplama ve Hazırlama
  - [ ] 3.3. Model Seçimi
  - [ ] 3.4. RAG Pipeline Tasarımı
  - [ ] 3.5. Değerlendirme Metrikleri

- [ ] 4. SİSTEM TASARIMI VE UYGULAMA
  - [ ] 4.1. Genel Mimari
  - [ ] 4.2. Backend Mimarisi
  - [ ] 4.3. Sağlayıcı Deseni (Provider Pattern)
  - [ ] 4.4. RAG Servisi Implementasyonu
  - [ ] 4.5. Frontend Mimarisi (Flutter)
  - [ ] 4.6. API Tasarımı
  - [ ] 4.7. Güvenlik ve Gizlilik

- [ ] 5. ARAŞTIRMA BULGULARI VE TARTIŞMA
  - [ ] 5.1. Test Stratejisi
  - [ ] 5.2. Kritik Bilgi Doğruluk Testleri
  - [ ] 5.3. RAG Performans Testleri
  - [ ] 5.4. Model Karşılaştırması
  - [ ] 5.5. Karşılaşılan Zorluklar ve Çözümler

- [ ] 6. SONUÇLAR VE ÖNERİLER
  - [ ] 6.1. Sonuçlar
  - [ ] 6.2. Özgün Katkılar
  - [ ] 6.3. Gelecek Çalışmalar

### SON KISIM
- [ ] KAYNAKLAR (alfabetik sıra, APA formatı)
- [ ] EKLER
  - [ ] EK-1: API Endpoint Dokümantasyonu
  - [ ] EK-2: Kod Örnekleri
  - [ ] EK-3: Test Sonuçları
  - [ ] EK-4: Kullanıcı Arayüzü Ekran Görüntüleri
- [ ] ÖZGEÇMİŞ

## 🎯 Tamamlama Rehberi

### Adım 1: Repository Analizi
Aşağıdaki dosyaları inceleyin ve bilgileri rapora aktarın:

**Backend:**
- `backend/main.py` - FastAPI uygulaması
- `backend/rag_service.py` - RAG implementasyonu
- `backend/providers/ollama_provider.py` - Ollama entegrasyonu
- `backend/providers/huggingface_provider.py` - HuggingFace entegrasyonu
- `backend/prompts.py` - System prompt'lar
- `backend/config.py` - Konfigürasyon
- `backend/test_*.py` - Test dosyaları

**Frontend:**
- `lib/controller/chat_controller.dart` - Chat controller
- `lib/screen/` - UI ekranları
- `lib/services/` - Servisler
- `pubspec.yaml` - Bağımlılıklar

**Dokümantasyon:**
- `README.md` - Ana dokümantasyon
- `docs/ARCHITECTURE.md` - Mimari detaylar
- `docs/TEST_RAPORU.md` - Test sonuçları
- `docs/JURI_HAZIRLIK.md` - Jüri hazırlık notları
- `docs/API_CONTRACT.md` - API dokümantasyonu
- `docs/RAG.md` - RAG açıklamaları

### Adım 2: Ana Bölümleri Yazma

#### Bölüm 1: GİRİŞ
- Transformer mimarisinden başlayarak LLM'lerin gelişimini anlatın
- Selçuk Üniversitesi'nin tanıtımını yapın (1975, Konya, 20+ fakülte)
- Gizlilik, çevrimdışı çalışma, RAG avantajlarını vurgulayın

#### Bölüm 2: KAYNAK ARAŞTIRMASI
- NLP tarihini özetleyin (ELIZA → Word2Vec → Transformer → GPT)
- LLM'leri karşılaştırın (GPT-4, Llama, Qwen2)
- Ollama ve RAG'ı detaylı açıklayın
- Benzer projeleri (Georgia Tech, Deakin) analiz edin

#### Bölüm 3: MATERYAL VE YÖNTEM
- Agile metodolojinizi açıklayın (sprint'ler)
- Veri toplama yöntemlerini belgeleyin (web scraping, manuel veri)
- Model seçim kriterlerini açıklayın (3B vs 7B, Llama vs Qwen)
- RAG pipeline'ı şema ile gösterin

#### Bölüm 4: SİSTEM TASARIMI VE UYGULAMA
- Mimari diyagramı ekleyin
- `backend/main.py`'dan kod örnekleri verin
- Provider Pattern'i açıklayın
- Flutter UI ekran görüntüleri ekleyin
- API endpoint'lerini listeleyin

#### Bölüm 5: ARAŞTIRMA BULGULARI VE TARTIŞMA
- Test sonuçlarını (`docs/TEST_RAPORU.md`) özetleyin
- Kritik bilgi testlerini gösterin ("Selçuk Üniversitesi nerede?" → "Konya" ✅)
- Model performans karşılaştırması yapın (3B vs 7B, hız vs kalite)
- Karşılaşılan sorunları ve çözümleri anlatın (UTF-8, hallüsinasyon)

#### Bölüm 6: SONUÇLAR VE ÖNERİLER
- Hedeflere ulaşma yüzdesini belirtin (%95+ doğruluk)
- Özgün katkıları listeleyin (gizlilik, RAG, multi-provider)
- Gelecek çalışmaları önerin (fine-tuning, sesli asistan, OBS entegrasyonu)

### Adım 3: Kaynakça Hazırlama

APA formatında kaynakları alfabetik sıraya koyun:

```
Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & 
Polosukhin, I., 2017, Attention is all you need, Advances in neural information 
processing systems, 30.

Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M. A., Lacroix, T., ... 
& Lample, G., 2023, Llama: Open and efficient foundation language models, arXiv 
preprint arXiv:2302.13971.

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., ... & 
Kiela, D., 2020, Retrieval-augmented generation for knowledge-intensive nlp tasks, 
Advances in Neural Information Processing Systems, 33, 9459-9474.
```

### Adım 4: Ekler Hazırlama

**EK-1: API Endpoint Dokümantasyonu**
```
GET  /health           - Sağlık kontrolü
GET  /models           - Mevcut modeller
POST /chat             - Sohbet (tek yanıt)
POST /chat/stream      - Sohbet (streaming)
```

**EK-2: Kod Örnekleri**
`backend/rag_service.py`'dan `get_context()` fonksiyonu
`lib/controller/chat_controller.dart`'dan `sendMessage()` fonksiyonu

**EK-3: Test Sonuçları**
Pytest çıktısı, coverage raporu

**EK-4: Ekran Görüntüleri**
Ana sohbet ekranı, ayarlar, model seçimi

### Adım 5: Özgeçmiş
Her öğrenci için ayrı özgeçmiş sayfası oluşturun:
- Kişisel bilgiler
- Eğitim geçmişi
- İş deneyimleri (varsa)
- Uzmanlık alanları
- Yabancı diller
- Yayınlar (varsa)

## 🔧 Teknik Bilgiler

### Repo İstatistikleri
- **Backend:** 26 Python dosyası
- **Frontend:** 65 Dart dosyası
- **Toplam Satır:** ~10,000+
- **Test Coverage:** %93
- **CI/CD:** GitHub Actions

### Teknoloji Stack'i
**Backend:**
- Python 3.11+
- FastAPI 0.115.5
- Ollama (Llama 3.1, Qwen2)
- FAISS 1.9.0
- LangChain
- sentence-transformers

**Frontend:**
- Flutter 3.x
- Dart
- GetX 4.6+
- http, flutter_markdown

## 📚 Referanslar

### Şablon Dosyaları
- `docs/vize_raporu/proje_sablonu.md` - Proje şablonu
- `docs/vize_raporu/yazim_kilavuzu.md` - Yazım kılavuzu
- `docs/vize_raporu/uygulama_projeleri_yonergesi.md` - Yönerge

### Mevcut Dokümantasyon
- `README.md` - Ana README
- `docs/JURI_HAZIRLIK.md` - Jüri hazırlık
- `docs/TEST_RAPORU.md` - Test raporu
- `docs/ARCHITECTURE.md` - Mimari
- `JURI_HAZIRLIK_OZET.md` - Özet

## ✅ Kontrol Listesi

Teslim öncesi kontrol edilecek hususlar:

- [ ] Sayfa yapısı uygun mu? (A4, kenarlar doğru)
- [ ] Şekil ve çizelge başlıkları uygun mu?
- [ ] Denklem yazımları uygun mu? (varsa)
- [ ] İç kapak, onay sayfası, özet, abstract, önsöz uygun mu?
- [ ] Bölüm sıralaması doğru mu? (Giriş, Kaynak, Materyal, Bulgular, Sonuç)
- [ ] Kaynaklar alfabetik sırada mı?
- [ ] Tüm kaynaklara metin içinde atıf yapıldı mı?
- [ ] Kaynaklar yazım kuralına uygun mu?
- [ ] Şekil/çizelgelerdeki ifadeler Türkçe mi?
- [ ] İçindekiler, metin içi başlıklarla uyumlu mu?

## 📥 Teslim

1. **Spiral Cilt:** İlk savunmaya spiral cilt veya clip dosya
2. **Elektronik:** PDF ve Word formatında CD/DVD
3. **Kontrol Listesi:** Öğrenci ve danışman imzalı (en üstte)

## 👥 Proje Ekibi

**Öğrenciler:**
- Doğukan BALAMAN (203311066)
- Ali YILDIRIM (203311008)

**Danışmanlar:**
- Prof. Dr. Nurettin DOĞAN
- Dr. Öğr. Üyesi Onur İNAN

**Bölüm:** Bilgisayar Mühendisliği - Teknoloji Fakültesi - Selçuk Üniversitesi

## 📧 İletişim

GitHub Repo: https://github.com/esN2k/SelcukAiAssistant  
Lisans: MIT License

---

**Son Güncelleme:** 5 Ocak 2025
