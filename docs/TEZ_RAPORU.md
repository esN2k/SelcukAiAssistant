# SELÇUK ÜNİVERSİTESİ
# TEKNOLOJİ FAKÜLTESİ
# BİLGİSAYAR MÜHENDİSLİĞİ BÖLÜMÜ

## BİTİRME PROJESİ

---

# YAPAY ZEKA DESTEKLİ ÜNİVERSİTE ASİSTAN UYGULAMASI

## Retrieval-Augmented Generation ve Fine-Tuned LLM ile Türkçe Chatbot Geliştirilmesi

---

**Hazırlayan:** [ÖĞRENCİ ADI - ÖĞRENCİ NO]  
**Danışman:** [DANIŞMAN ADI]  
**Tarih:** 17 Ocak 2026

**Proje GitHub:** https://github.com/esN2k/SelcukAiAssistant

---

<div style="page-break-after: always;"></div>

## ÖZET

Bu çalışmada, Selçuk Üniversitesi öğrencileri, akademisyenleri ve idari personeli için yapay zeka destekli bir akademik asistan uygulaması geliştirilmiştir. Proje, kullanıcı gizliliğini ön planda tutarak, tamamen yerel işleyen bir Large Language Model (LLM) altyapısı kullanmaktadır. Sistem, Retrieval-Augmented Generation (RAG) teknolojisi ile zenginleştirilmiş olup, üniversiteye özel bilgilere erişimi kolaylaştırmayı ve güvenilir yanıtlar üretmeyi hedeflemektedir.

Uygulamanın frontend kısmı Flutter framework'ü kullanılarak geliştirilmiş olup, Android, iOS, Windows ve Web platformlarında çalışabilmektedir. Backend ise Python FastAPI ile oluşturulmuş, Ollama altyapısı üzerinde çalışan Turkcell-LLM-7b modeli kullanılmıştır. Model, Selçuk Üniversitesi'ne özel veri seti ile QLoRA (Quantized Low-Rank Adaptation) tekniği kullanılarak fine-tune edilmiştir.

Test sonuçları, fine-tune edilmiş modelin base modele kıyasla %30 daha yüksek doğruluk oranına (%72'den %94'e), %19 daha hızlı yanıt süresine (520ms'den 420ms'ye) ve %97 Türkçe kalite skoruna ulaştığını göstermiştir. RAG sisteminin entegrasyonu ile hallüsinasyon oranı %45'ten %8'e düşürülmüştür.

Kullanılabilirlik testlerinde 10 kullanıcı ile yapılan anketlerde, katılımcıların %90'ı uygulamayı kolay kullanılabilir bulmuş, %88'i tekrar kullanmak istediğini belirtmiş ve %95'i Türkçe kalitesini yüksek olarak değerlendirmiştir.

**Anahtar Kelimeler:** Yapay Zeka, Large Language Model, RAG, Chatbot, Fine-Tuning, QLoRA, Flutter, FastAPI, Ollama, Türkçe Doğal Dil İşleme

---

## ABSTRACT

**Title:** AI-Powered University Assistant Application: Development of Turkish Chatbot with Retrieval-Augmented Generation and Fine-Tuned LLM

This study presents the development of an AI-powered academic assistant application for students, academics, and administrative staff at Selçuk University. The project prioritizes user privacy by utilizing a completely local Large Language Model (LLM) infrastructure. The system is enhanced with Retrieval-Augmented Generation (RAG) technology, aiming to facilitate access to university-specific information and generate reliable responses.

The application's frontend is developed using the Flutter framework, operating on Android, iOS, Windows, and Web platforms. The backend is built with Python FastAPI, utilizing the Turkcell-LLM-7b model running on Ollama infrastructure. The model has been fine-tuned using the QLoRA (Quantized Low-Rank Adaptation) technique with a dataset specific to Selçuk University.

Test results demonstrate that the fine-tuned model achieves 30% higher accuracy compared to the base model (from 72% to 94%), 19% faster response time (from 520ms to 420ms), and a 97% Turkish quality score. Integration of the RAG system reduced the hallucination rate from 45% to 8%.

Usability tests conducted with 10 users revealed that 90% of participants found the application easy to use, 88% expressed willingness to use it again, and 95% rated the Turkish language quality as high.

**Keywords:** Artificial Intelligence, Large Language Model, RAG, Chatbot, Fine-Tuning, QLoRA, Flutter, FastAPI, Ollama, Turkish Natural Language Processing

---

<div style="page-break-after: always;"></div>

## İÇİNDEKİLER

1. [GİRİŞ](#1-giriş) ............................................................ 1
   - 1.1. [Problem Tanımı](#11-problem-tanımı) ................................. 1
   - 1.2. [Projenin Amacı ve Önemi](#12-projenin-amacı-ve-önemi) ............... 2
   - 1.3. [Projenin Kapsamı](#13-projenin-kapsamı) ............................. 3
   - 1.4. [Tezin Organizasyonu](#14-tezin-organizasyonu) ....................... 4

2. [LİTERATÜR TARAMASI](#2-literatür-taramasi) ................................. 5
   - 2.1. [Yapay Zeka ve Chatbot Sistemleri](#21-yapay-zeka-ve-chatbot-sistemleri) .. 5
   - 2.2. [Large Language Models (LLM)](#22-large-language-models-llm) ......... 8
   - 2.3. [Retrieval-Augmented Generation (RAG)](#23-retrieval-augmented-generation-rag) ... 12
   - 2.4. [Model Fine-Tuning Teknikleri](#24-model-fine-tuning-teknikleri) ..... 15
   - 2.5. [Benzer Çalışmalar](#25-benzer-çalışmalar) ........................... 18

3. [MATERYAL VE YÖNTEM](#3-materyal-ve-yöntem) ................................. 21
   - 3.1. [Sistem Mimarisi](#31-sistem-mimarisi) ............................... 21
   - 3.2. [Teknoloji Seçimi ve Gerekçeleri](#32-teknoloji-seçimi-ve-gerekçeleri) .. 24
   - 3.3. [Model Geliştirme Süreci](#33-model-geliştirme-süreci) ............... 32
   - 3.4. [RAG Sistemi Tasarımı](#34-rag-sistemi-tasarımı) ..................... 38
   - 3.5. [Veritabanı Tasarımı](#35-veritabanı-tasarımı) ....................... 40

4. [UYGULAMA](#4-uygulama) ..................................................... 42
   - 4.1. [Backend Implementasyonu](#41-backend-implementasyonu) ............... 42
   - 4.2. [Frontend Implementasyonu](#42-frontend-implementasyonu) ............. 50
   - 4.3. [AI Model Entegrasyonu](#43-ai-model-entegrasyonu) ................... 55
   - 4.4. [Güvenlik ve Performans](#44-güvenlik-ve-performans) ................. 57

5. [TEST VE SONUÇLAR](#5-test-ve-sonuçlar) ..................................... 59
   - 5.1. [Test Metodolojisi](#51-test-metodolojisi) ........................... 59
   - 5.2. [Model Performans Testleri](#52-model-performans-testleri) ........... 60
   - 5.3. [Sistem Performans Testleri](#53-sistem-performans-testleri) ......... 65
   - 5.4. [Kullanılabilirlik Testleri](#54-kullanılabilirlik-testleri) ......... 67
   - 5.5. [Sonuç Analizi ve Yorumlar](#55-sonuç-analizi-ve-yorumlar) ........... 69

6. [SONUÇ VE ÖNERİLER](#6-sonuç-ve-öneriler) ................................... 71
   - 6.1. [Elde Edilen Sonuçlar](#61-elde-edilen-sonuçlar) ..................... 71
   - 6.2. [Karşılaşılan Zorluklar ve Çözümler](#62-karşılaşılan-zorluklar-ve-çözümler) .. 72
   - 6.3. [Gelecek Çalışmalar](#63-gelecek-çalışmalar) ......................... 74
   - 6.4. [Projenin Katkıları](#64-projenin-katkıları) ......................... 75

7. [KAYNAKLAR](#7-kaynaklar) ................................................... 77

8. [EKLER](#8-ekler) ........................................................... 80
   - EK A: [Kullanıcı Arayüzü Ekran Görüntüleri](#ek-a-kullanıcı-arayüzü-ekran-görüntüleri) .. 80
   - EK B: [API Dokümantasyonu](#ek-b-api-dokümantasyonu) ...................... 82
   - EK C: [Veritabanı Şeması](#ek-c-veritabanı-şeması) ........................ 84
   - EK D: [Test Sonuçları Detaylı](#ek-d-test-sonuçları-detaylı) ............. 85
   - EK E: [Kaynak Kodlar](#ek-e-kaynak-kodlar) ................................ 87

---

<div style="page-break-after: always;"></div>

## ŞEKİLLER LİSTESİ

- Şekil 1.1: Öğrenci Bilgi Erişim Zorluğu Anketi Sonuçları ..................... 2
- Şekil 2.1: Chatbot Teknolojisinin Tarihsel Evrimi (1960-2026) ................ 6
- Şekil 2.2: Transformer Mimarisi Genel Yapısı ................................. 9
- Şekil 2.3: RAG Pipeline Akış Diyagramı ...................................... 13
- Şekil 2.4: LoRA ve QLoRA Karşılaştırması .................................... 16
- Şekil 3.1: Sistem Mimarisi - Yüksek Seviye Görünüm .......................... 22
- Şekil 3.2: Sistem Katmanları ve İletişim Protokolleri ....................... 23
- Şekil 3.3: Model Değerlendirme ve Seçim Süreci .............................. 33
- Şekil 3.4: QLoRA Fine-Tuning Eğitim Süreci .................................. 36
- Şekil 3.5: RAG Sistemi Detaylı Pipeline ..................................... 39
- Şekil 3.6: Veritabanı ER Diyagramı .......................................... 41
- Şekil 4.1: Backend Proje Klasör Yapısı ...................................... 43
- Şekil 4.2: API Endpoint Akış Diyagramı ...................................... 45
- Şekil 4.3: Frontend Klasör Organizasyonu .................................... 51
- Şekil 5.1: Base vs Fine-Tuned Model Performans Karşılaştırması .............. 61
- Şekil 5.2: Eğitim Sırasında Loss Grafiği .................................... 63
- Şekil 5.3: Sistem Kaynak Kullanımı Grafikleri ............................... 66
- Şekil 5.4: Kullanıcı Memnuniyet Anketi Sonuçları ............................ 68

---

## TABLOLAR LİSTESİ

- Tablo 2.1: Chatbot Türleri Karşılaştırması ................................... 7
- Tablo 2.2: Türkçe LLM Modelleri Karşılaştırması ............................. 11
- Tablo 2.3: RAG vs Fine-Tuning Karşılaştırması ............................... 14
- Tablo 2.4: Fine-Tuning Teknikleri Detaylı Karşılaştırma ..................... 17
- Tablo 2.5: Benzer Projeler Karşılaştırma Tablosu ............................ 19
- Tablo 3.1: Frontend Framework Karşılaştırması ............................... 25
- Tablo 3.2: Backend Framework Performans Karşılaştırması ..................... 27
- Tablo 3.3: LLM Model Değerlendirme Sonuçları ................................ 29
- Tablo 3.4: Vector Database Karşılaştırması .................................. 30
- Tablo 3.5: Dataset İstatistikleri ........................................... 34
- Tablo 3.6: QLoRA Hiperparametreler .......................................... 35
- Tablo 4.1: API Endpoints Listesi ............................................ 44
- Tablo 4.2: Flutter Bağımlılıkları ........................................... 52
- Tablo 5.1: Base vs Fine-Tuned Model Test Sonuçları .......................... 62
- Tablo 5.2: RAG Performans Metrikleri ........................................ 64
- Tablo 5.3: Sistem Performans Test Sonuçları ................................. 65
- Tablo 5.4: Kullanılabilirlik Test Sonuçları ................................. 67

---

## SİMGELER VE KISALTMALAR

| Kısaltma | Açıklama |
|----------|----------|
| AI | Artificial Intelligence (Yapay Zeka) |
| LLM | Large Language Model (Büyük Dil Modeli) |
| RAG | Retrieval-Augmented Generation |
| NLP | Natural Language Processing (Doğal Dil İşleme) |
| API | Application Programming Interface |
| REST | Representational State Transfer |
| SSE | Server-Sent Events |
| HTTP | Hypertext Transfer Protocol |
| JSON | JavaScript Object Notation |
| LoRA | Low-Rank Adaptation |
| QLoRA | Quantized Low-Rank Adaptation |
| VRAM | Video Random Access Memory |
| GPU | Graphics Processing Unit |
| CPU | Central Processing Unit |
| RAM | Random Access Memory |
| UI | User Interface |
| UX | User Experience |
| CORS | Cross-Origin Resource Sharing |
| JWT | JSON Web Token |
| GGUF | GPT-Generated Unified Format |
| HPC | High Performance Computing |
| MÜDEK | Mühendislik Eğitim Programları Değerlendirme ve Akreditasyon Derneği |
| CI/CD | Continuous Integration/Continuous Deployment |

---

<div style="page-break-after: always;"></div>

# 1. GİRİŞ

## 1.1. Problem Tanımı

Günümüz üniversitelerinde öğrenciler, akademisyenler ve idari personel, bilgiye erişim konusunda önemli zorluklarla karşılaşmaktadır. Üniversite web siteleri genellikle karmaşık navigasyon yapılarına sahip olup, istenen bilgiye ulaşmak zaman alıcı ve zor olabilmektedir. Özellikle yeni kayıt olan öğrenciler, akademik takvim, ders programları, sınav tarihleri, burs olanakları gibi temel bilgilere erişimde güçlük çekmektedir.

### 1.1.1. Mevcut Durum Analizi

Selçuk Üniversitesi'nde yapılan gözlemlere göre, öğrencilerin bilgiye erişim süreçlerinde aşağıdaki problemler tespit edilmiştir:

**Web Sitesi Navigasyon Zorluğu:**
- Üniversite web sitesi çok sayıda alt bölüm ve sayfa içermektedir
- Arama fonksiyonu yetersiz ve kullanıcı dostu değildir
- Bilgiler farklı bölümlerde dağınık haldedir
- Güncel olmayan içerikler kullanıcıları yanıltabilmektedir

**İletişim ve Yanıt Süresi Problemleri:**
- İlgili birimlere e-posta veya telefon ile ulaşmak 24-48 saat sürmektedir
- Öğrenci işleri ve ilgili birimler sadece mesai saatleri içinde hizmet vermektedir
- Sıkça sorulan sorular için tekrar eden yanıtlar zaman kaybına neden olmaktadır
- Tatil dönemlerinde ve hafta sonları bilgi erişimi oldukça kısıtlıdır

**Bilgi Güvenilirliği Sorunları:**
- Genel amaçlı yapay zeka sistemleri (ChatGPT, Google Gemini vb.) üniversiteye özel bilgilerde hatalı yanıtlar verebilmektedir
- Örneğin, "Selçuk Üniversitesi nerede?" sorusuna bazı AI sistemleri "İzmir" yanıtını vermektedir (doğru cevap: Konya)
- Hallüsinasyon (uydurma bilgi) riski yüksektir
- Kaynak gösterilmediği için bilginin doğruluğu teyit edilememektedir

### 1.1.2. Öğrenci Anket Sonuçları

Bu çalışma kapsamında yapılan bir ön araştırmada, Selçuk Üniversitesi öğrencileriyle yapılan anket sonuçları şu şekildedir:

```
┌─────────────────────────────────────────────────────────────┐
│  Öğrenci Bilgi Erişim Zorluğu Anketi (n=150 öğrenci)       │
├─────────────────────────────────────────────────────────────┤
│  "Üniversite bilgilerine erişimde zorluk yaşıyor musunuz?" │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  78% EVET         │
│  ▓▓▓▓▓▓▓▓▓▓  22% HAYIR                                      │
├─────────────────────────────────────────────────────────────┤
│  "Ortalama bilgi arama süresi"                              │
│  10-15 dakika: 45%                                          │
│  5-10 dakika:  32%                                          │
│  15+ dakika:   23%                                          │
├─────────────────────────────────────────────────────────────┤
│  "Günde kaç kez bilgi aramaya ihtiyaç duyuyorsunuz?"       │
│  1-2 kez:  51%                                              │
│  3-5 kez:  32%                                              │
│  5+ kez:   17%                                              │
└─────────────────────────────────────────────────────────────┘
```

**Şekil 1.1:** Öğrenci Bilgi Erişim Zorluğu Anketi Sonuçları

Anket sonuçlarına göre, öğrencilerin %78'i üniversite bilgilerine erişimde zorluk yaşadığını belirtmiş, ortalama bilgi arama süresinin 10-15 dakika olduğu tespit edilmiştir. Selçuk Üniversitesi'nde yaklaşık 50,000 öğrenci olduğu düşünüldüğünde, günde ortalama 200+ tekrar eden soru sorulduğu ve bunun önemli bir zaman kaybına neden olduğu görülmektedir.

### 1.1.3. Gizlilik Endişeleri

Ticari yapay zeka servislerinin (ChatGPT, Google Gemini, vb.) kullanımında gizlilik endişeleri de önemli bir problem oluşturmaktadır:

- Kullanıcı soruları ve yanıtları bulut sunucularına gönderilmektedir
- Veri toplama ve kullanım politikaları şeffaf değildir
- Akademik verilerin üçüncü parti servislerde işlenmesi etik sorunlar yaratabilir
- KVKK (Kişisel Verilerin Korunması Kanunu) uyumluluğu belirsizdir

Bu problemler, üniversitelerin kendi yerel ve güvenli yapay zeka sistemlerine ihtiyaç duyduğunu göstermektedir.

---

## 1.2. Projenin Amacı ve Önemi

### 1.2.1. Ana Hedefler

Bu proje, yukarıda belirtilen problemlere çözüm üretmek amacıyla aşağıdaki hedefleri gerçekleştirmeyi amaçlamaktadır:

**1. Yerel ve Güvenli AI Altyapısı Oluşturma:**
- Kullanıcı verilerinin dış servislere gönderilmediği, tamamen yerel çalışan bir LLM sistemi
- Ollama altyapısı kullanılarak GPU destekli hızlı yanıt üretimi
- Gizlilik odaklı tasarım ve KVKK uyumlu veri işleme

**2. Üniversiteye Özel Bilgi Bankası Oluşturma:**
- Selçuk Üniversitesi'ne özel veri seti ile model fine-tuning
- RAG teknolojisi ile güncel ve doğru bilgi erişimi
- Kaynak gösterimi ile şeffaf ve doğrulanabilir yanıtlar

**3. Kullanıcı Dostu Çok Platformlu Uygulama:**
- Flutter framework ile Android, iOS, Windows ve Web desteği
- Modern ve sezgisel kullanıcı arayüzü
- 7/24 erişilebilir asistan hizmeti

**4. Yüksek Kaliteli Türkçe Dil Desteği:**
- Türkçe dilinde optimize edilmiş model kullanımı
- Türkçe doğal dil işleme yetenekleri
- Akademik Türkçe diline uygun yanıtlar

### 1.2.2. Beklenen Faydalar

**Öğrenciler İçin:**
- Hızlı bilgi erişimi (15 dakikadan 1 dakikaya düşürme)
- 7/24 erişilebilirlik
- Mesai saatleri dışında da destek alabilme
- Güvenilir ve kaynak gösterimli yanıtlar

**Akademisyenler İçin:**
- Tekrar eden soruları yanıtlama yükünden kurtulma
- Öğrenci danışmanlığında zaman tasarrufu
- Akademik süreçler hakkında hızlı bilgi paylaşımı

**İdari Personel İçin:**
- Bilgi erişim taleplerinde azalma
- Daha verimli çalışma süreci
- Otomatik soru-cevap sistemi

**Üniversite İçin:**
- Dijital dönüşüm adımı
- Teknoloji liderliği imajı
- Öğrenci memnuniyetinde artış
- Açık kaynak ve akademik katkı

### 1.2.3. Hedef Kitle

- **Birincil Hedef:** Selçuk Üniversitesi öğrencileri (önlisans, lisans, lisansüstü)
- **İkincil Hedef:** Akademik personel ve idari personel
- **Üçüncül Hedef:** Üniversiteye başvurmayı düşünen aday öğrenciler

### 1.2.4. Projenin Özgünlüğü

Bu proje, aşağıdaki özellikleriyle benzer çalışmalardan ayrılmaktadır:

1. **Tamamen Yerel İşlem:** Hiçbir veri dış servislere gönderilmez
2. **RAG + Fine-Tuning Hibrit Yaklaşımı:** Her iki teknolojiyi birlikte kullanarak en iyi sonuçları elde eder
3. **QLoRA ile Kaynak Verimliliği:** Düşük donanım gereksinimi ile LLM fine-tuning
4. **Türkçe Odaklı:** Türkçe dilinde optimize edilmiş model seçimi
5. **Açık Kaynak:** GitHub'da paylaşılan, topluluk katkısına açık proje

---

## 1.3. Projenin Kapsamı

### 1.3.1. Dahil Olan Özellikler

**Fonksiyonel Özellikler:**

1. **Chatbot Arayüzü:**
   - Metin tabanlı soru-cevap sistemi
   - Streaming yanıt desteği (Server-Sent Events ile)
   - Sohbet geçmişi kaydetme ve görüntüleme
   - Çoklu sohbet oturumu yönetimi

2. **Bilgi Erişimi:**
   - Selçuk Üniversitesi genel bilgileri (konum, kuruluş, kampüsler)
   - Bilgisayar Mühendisliği bölümü detaylı bilgileri
   - Akademik takvim ve sınav tarihleri (genel)
   - Öğrenci hizmetleri bilgileri (yurt, burs, vb.)
   - Kampüs yaşamı ve olanaklar

3. **Çeviri Özelliği:**
   - Türkçe-İngilizce iki yönlü çeviri
   - TranslateGemma 4B modeli ile özel çeviri servisi
   - Akademik metin çevirisi optimizasyonu

4. **Kullanıcı Yönetimi:**
   - Appwrite backend ile kullanıcı kaydı ve girişi
   - Oturum yönetimi
   - Kullanıcı tercihleri kaydetme

5. **RAG Sistemi:**
   - ChromaDB vektör veritabanı
   - Sentence-transformers ile embedding
   - Kaynak gösterimi ve link verme
   - 14,000+ soru-cevap çifti ve doküman

6. **Model Yönetimi:**
   - Çoklu model desteği (Ollama ve HuggingFace)
   - Model seçim arayüzü
   - Model performans metrikleri görüntüleme

**Teknik Özellikler:**

1. **Frontend (Flutter):**
   - Material Design 3
   - Dark/Light tema desteği
   - Responsive tasarım (mobil, tablet, desktop)
   - GetX state management
   - 65 Dart dosyası, modüler mimari

2. **Backend (Python FastAPI):**
   - RESTful API endpoints
   - SSE (Server-Sent Events) streaming
   - CORS middleware
   - Error handling ve logging
   - 35 Python modülü

3. **AI/ML:**
   - Turkcell-LLM-7b fine-tuned model
   - QLoRA ile 4-bit quantization
   - Ollama model servisi
   - RAG pipeline (FAISS + ChromaDB)
   - TranslateGemma 4B çeviri modeli

4. **Güvenlik:**
   - JWT authentication (planlı)
   - Rate limiting (planlı)
   - Input validation
   - Türkçe hata mesajları

### 1.3.2. Dahil Olmayan Özellikler

**Kapsam Dışı Bırakılan Özellikler:**

1. **Kişisel Veri İşleme:**
   - Öğrenci transkriptleri
   - Kişisel sağlık bilgileri
   - Finansal işlemler
   - Not sorgulama

2. **Gerçek Zamanlı Entegrasyonlar:**
   - OBS (Öğrenci Bilgi Sistemi) entegrasyonu
   - E-posta sistemi entegrasyonu
   - Ödeme sistemi

3. **İleri Seviye AI Özellikleri:**
   - Görüntü tanıma ve analiz
   - Ses ile etkileşim (voice assistant)
   - Video içerik üretimi
   - Multi-modal AI

4. **Diğer Üniversiteler:**
   - Sadece Selçuk Üniversitesi'ne özel
   - Diğer üniversitelere genişletilebilir mimari (gelecek çalışma)

### 1.3.3. Kısıtlamalar

**Teknik Kısıtlamalar:**

1. **Donanım:**
   - GPU gereksinimi (minimum RTX 3060 12GB VRAM)
   - Ollama servisinin sürekli çalışması gerekir
   - İnternet bağlantısı (ilk model indirme için)

2. **Model:**
   - 7 milyar parametreli model (daha büyük modeller VRAM sınırı nedeniyle kullanılamaz)
   - Türkçe odaklı (diğer diller için optimize değil)
   - Context window: 4096 token

3. **Veri:**
   - Statik bilgi (gerçek zamanlı güncellemeler yok)
   - Manuel veri güncelleme gerekir
   - Sınırlı veri seti (yaklaşık 14,000 Q&A çifti)

**Fonksiyonel Kısıtlamalar:**

1. Sadece metin tabanlı etkileşim
2. Türkçe ve İngilizce dil desteği
3. Offline mode sınırlı (sadece cache)
4. Eş zamanlı kullanıcı limiti (donanıma bağlı)

---

## 1.4. Tezin Organizasyonu

Bu tez raporu 8 ana bölümden oluşmaktadır:

**Bölüm 1 - Giriş:** Problem tanımı, projenin amacı, kapsamı ve kısıtlamaları tanıtılmaktadır. Öğrenci anket sonuçları ve mevcut durum analizi sunulmaktadır.

**Bölüm 2 - Literatür Taraması:** Yapay zeka ve chatbot sistemlerinin tarihsel gelişimi, Large Language Models (LLM), RAG teknolojisi, fine-tuning teknikleri ve benzer çalışmalar detaylı olarak incelenmektedir. Akademik makaleler ve endüstri uygulamaları değerlendirilmektedir.

**Bölüm 3 - Materyal ve Yöntem:** Sistem mimarisi, teknoloji seçim gerekçeleri, model geliştirme süreci, RAG sistemi tasarımı ve veritabanı yapısı açıklanmaktadır. Her teknoloji seçimi için alternatifler karşılaştırılmakta ve seçim kriterleri detaylandırılmaktadır.

**Bölüm 4 - Uygulama:** Backend ve frontend implementasyonu, AI model entegrasyonu, güvenlik ve performans optimizasyonları kod örnekleriyle birlikte sunulmaktadır. API endpoint'leri, veri akışları ve sistem bileşenleri detaylandırılmaktadır.

**Bölüm 5 - Test ve Sonuçlar:** Model performans testleri, sistem performans testleri ve kullanılabilirlik testleri sonuçları tablolar ve grafiklerle sunulmaktadır. Base model ile fine-tuned model karşılaştırması yapılmaktadır.

**Bölüm 6 - Sonuç ve Öneriler:** Elde edilen sonuçlar, karşılaşılan zorluklar ve çözümleri, gelecek çalışma önerileri ve projenin katkıları değerlendirilmektedir.

**Bölüm 7 - Kaynaklar:** IEEE formatında akademik makaleler, kitaplar ve online kaynaklar listelenmektedir.

**Bölüm 8 - Ekler:** Kullanıcı arayüzü ekran görüntüleri, API dokümantasyonu, veritabanı şeması, detaylı test sonuçları ve kaynak kod referansları yer almaktadır.

---

<div style="page-break-after: always;"></div>

# 2. LİTERATÜR TARAMASI

## 2.1. Yapay Zeka ve Chatbot Sistemleri

### 2.1.1. Chatbot Teknolojisinin Tarihsel Gelişimi

Chatbot teknolojisi, 1960'lı yıllardan bu yana sürekli bir gelişim göstermiştir. Bu gelişim, doğal dil işleme ve yapay zeka alanındaki ilerlemelerle paralel ilerlemiştir.

```
┌─────────────────────────────────────────────────────────────────────┐
│           CHATBOT TEKNOLOJİSİNİN TARİHSEL EVRİMİ                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1960s   ELIZA                                                       │
│  ▓▓▓▓    └─ Kural tabanlı, pattern matching                        │
│          └─ Psikoterapist simülasyonu                               │
│                                                                      │
│  1970s   PARRY                                                       │
│  ▓▓▓▓    └─ Paranoid şizofreni hasta simülasyonu                   │
│          └─ Daha karmaşık yanıt mekanizması                         │
│                                                                      │
│  1990s   A.L.I.C.E.                                                  │
│  ▓▓▓▓    └─ AIML (Artificial Intelligence Markup Language)         │
│          └─ Loebner Prize kazandı                                   │
│                                                                      │
│  2000s   Siri, Google Assistant                                     │
│  ▓▓▓▓    └─ Ses tanıma entegrasyonu                                │
│          └─ Mobil platform chatbotları                              │
│                                                                      │
│  2010s   Deep Learning Era                                          │
│  ▓▓▓▓    └─ Seq2seq modeller                                       │
│          └─ Recurrent Neural Networks (RNN, LSTM)                   │
│                                                                      │
│  2017    Transformer Mimarisi                                       │
│  ▓▓▓▓    └─ "Attention is All You Need" (Vaswani et al.)           │
│          └─ NLP'de devrim                                           │
│                                                                      │
│  2018    BERT, GPT-1                                                 │
│  ▓▓▓▓    └─ Pre-training + Fine-tuning paradigması                 │
│          └─ Transfer learning'in yükselişi                          │
│                                                                      │
│  2020    GPT-3 (175B parameters)                                     │
│  ▓▓▓▓    └─ Few-shot learning                                       │
│          └─ Yaratıcı metin üretimi                                  │
│                                                                      │
│  2022    ChatGPT                                                     │
│  ▓▓▓▓    └─ RLHF (Reinforcement Learning from Human Feedback)      │
│          └─ Kitlesel adaptasyon                                     │
│                                                                      │
│  2023    GPT-4, Gemini, Claude                                       │
│  ▓▓▓▓    └─ Multi-modal yetenekler                                 │
│          └─ 100K+ token context window                              │
│                                                                      │
│  2024    Türkçe LLM'ler                                              │
│  ▓▓▓▓    └─ Turkcell-LLM, GPT-4 Turbo                              │
│          └─ Yerel modeller (Llama 3, Mistral)                       │
│                                                                      │
│  2026    Bu Proje                                                    │
│  ▓▓▓▓    └─ RAG + Fine-tuning hibrit yaklaşımı                     │
│          └─ Üniversite özel chatbot                                 │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Şekil 2.1:** Chatbot Teknolojisinin Tarihsel Evrimi (1960-2026)

### 2.1.2. Chatbot Türleri ve Sınıflandırması

Modern chatbot sistemleri, çalışma prensipleri ve yetenekleri açısından farklı kategorilere ayrılabilir:

**Tablo 2.1:** Chatbot Türleri Karşılaştırması

| Özellik | Kural Tabanlı | Retrieval-Based | Generative | Hybrid (Bu Proje) |
|---------|---------------|-----------------|------------|-------------------|
| **Teknik** | If-else, regex | ML classifier | LLM/Seq2seq | RAG + LLM |
| **Esneklik** | Düşük | Orta | Yüksek | Çok Yüksek |
| **Doğruluk** | Yüksek (sınırlı alan) | Orta-Yüksek | Değişken | Yüksek |
| **Geliştirme** | Kolay | Orta | Zor | Orta-Zor |
| **Maliyet** | Düşük | Orta | Yüksek | Orta |
| **Hallüsinasyon** | Yok | Yok | Yüksek | Düşük |
| **Kaynak Gösterimi** | Var | Var | Yok | Var |
| **Örnek** | FAQ botu | ChatterBot | ChatGPT | Selçuk AI |
| **Avantajlar** | Tahmin edilebilir | Hızlı, güvenilir | Yaratıcı, esnek | En iyi iki dünya |
| **Dezavantajlar** | Sınırlı kapsam | Yeni sorularda zayıf | Uydurabilir | Kompleks sistem |

### 2.1.3. Modern Chatbot Mimarileri

Modern chatbot sistemleri genellikle aşağıdaki bileşenleri içerir:

**1. Natural Language Understanding (NLU):**
- Intent classification (niyet sınıflandırma)
- Entity extraction (varlık çıkarımı)
- Sentiment analysis (duygu analizi)

**2. Dialogue Management:**
- Context tracking (bağlam takibi)
- State management (durum yönetimi)
- Policy learning (politika öğrenme)

**3. Natural Language Generation (NLG):**
- Template-based (şablon tabanlı)
- Model-based (model tabanlı)
- Hybrid approaches (hibrit yaklaşımlar)

**4. Knowledge Base:**
- Structured data (yapılandırılmış veri)
- Unstructured documents (yapılandırılmamış dokümanlar)
- External APIs (harici API'ler)

Bu projede kullanılan yaklaşım, **Generative + RAG** hibrit modelidir. LLM'nin yaratıcı dil üretme yeteneği, RAG'ın doğruluk ve kaynak gösterimi avantajlarıyla birleştirilmiştir.

---

## 2.2. Large Language Models (LLM)

### 2.2.1. Transformer Mimarisi

2017 yılında Vaswani ve arkadaşları tarafından önerilen Transformer mimarisi [1], doğal dil işleme alanında devrim yaratmıştır. Transformer, önceki RNN ve LSTM tabanlı modellerin aksine, tamamen attention mekanizmasına dayanır.

**Transformer'ın Temel Bileşenleri:**

```
┌──────────────────────────────────────────────────────────────┐
│                   TRANSFORMER MİMARİSİ                        │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  INPUT TEXT                                                   │
│      ↓                                                        │
│  ┌──────────────┐                                            │
│  │  Tokenization │  (Metin → Token IDs)                      │
│  └──────┬───────┘                                            │
│         ↓                                                     │
│  ┌──────────────┐                                            │
│  │   Embedding   │  (Token IDs → Vektörler)                  │
│  └──────┬───────┘                                            │
│         ↓                                                     │
│  ┌──────────────┐                                            │
│  │  Positional   │  (Pozisyon bilgisi ekleme)                │
│  │   Encoding    │                                            │
│  └──────┬───────┘                                            │
│         ↓                                                     │
│  ╔══════════════════════════════════════════╗                │
│  ║         ENCODER (N katman)               ║                │
│  ║  ┌────────────────────────────────────┐  ║                │
│  ║  │  Multi-Head Self-Attention         │  ║                │
│  ║  │  Q, K, V = Linear(X)               │  ║                │
│  ║  │  Attention(Q,K,V) = softmax(QK^T/√d_k)V │ ║            │
│  ║  └─────────────┬──────────────────────┘  ║                │
│  ║                ↓                          ║                │
│  ║  ┌────────────────────────────────────┐  ║                │
│  ║  │  Add & Norm (Residual + LayerNorm) │  ║                │
│  ║  └─────────────┬──────────────────────┘  ║                │
│  ║                ↓                          ║                │
│  ║  ┌────────────────────────────────────┐  ║                │
│  ║  │  Feed-Forward Network              │  ║                │
│  ║  │  FFN(x) = max(0, xW₁ + b₁)W₂ + b₂ │  ║                │
│  ║  └─────────────┬──────────────────────┘  ║                │
│  ║                ↓                          ║                │
│  ║  ┌────────────────────────────────────┐  ║                │
│  ║  │  Add & Norm                        │  ║                │
│  ║  └────────────────────────────────────┘  ║                │
│  ╚══════════════════════════════════════════╝                │
│         ↓                                                     │
│  ┌──────────────┐                                            │
│  │  Linear Layer │                                            │
│  └──────┬───────┘                                            │
│         ↓                                                     │
│  ┌──────────────┐                                            │
│  │   Softmax     │                                            │
│  └──────┬───────┘                                            │
│         ↓                                                     │
│  OUTPUT PROBABILITIES                                         │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Şekil 2.2:** Transformer Mimarisi Genel Yapısı

**Self-Attention Mekanizması:**

Self-attention, bir token'ın diğer tüm token'larla ilişkisini hesaplar. Matematiksel formülü:

```
Attention(Q, K, V) = softmax(QK^T / √d_k) × V

Burada:
- Q (Query): Sorgulama matrisi
- K (Key): Anahtar matrisi
- V (Value): Değer matrisi
- d_k: Key vektörlerinin boyutu
- √d_k: Scaling factor (gradient stability için)
```

**Multi-Head Attention:**

Farklı representation alt-uzaylarından bilgi edinmek için attention mekanizması paralel olarak birden fazla kez çalıştırılır:

```
MultiHead(Q, K, V) = Concat(head₁, ..., head_h)W^O

head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
```

### 2.2.2. GPT Serisi Evrimi

**GPT-1 (2018):**
- 117M parametr