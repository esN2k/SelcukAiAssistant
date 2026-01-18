# T.C.
# SELÇUK ÜNİVERSİTESİ
# TEKNOLOJİ FAKÜLTESİ
# BİLGİSAYAR MÜHENDİSLİĞİ BÖLÜMÜ

---

# YAPAY ZEKA DESTEKLİ ÜNİVERSİTE BİLGİ ASİSTANI: SELÇUK AI ASİSTAN

---

Doğukan BALAMAN (203311066)  
Ali YILDIRIM (203311008)

BİLGİSAYAR MÜHENDİSLİĞİ UYGULAMALARI

---

Ocak 2025  
KONYA

Her Hakkı Saklıdır

---

*Sayfa ii*

## BİTİRME PROJESİ KABUL VE ONAYI

Doğukan BALAMAN ve Ali YILDIRIM tarafından hazırlanan "Yapay Zeka Destekli Üniversite Bilgi Asistanı: Selçuk AI Asistan" adlı bitirme proje çalışması .../.../ 2025 tarihinde aşağıdaki jüri üyeleri tarafından Selçuk Üniversitesi Teknoloji Fakültesi Bilgisayar Mühendisliği bölümünde Bilgisayar Mühendisliği Uygulamaları Projesi olarak kabul edilmiştir.

**Jüri Üyeleri**

Başkan  
Prof. Dr. Nurettin DOĞAN  
_________________

Üye  
Dr. Öğr. Üyesi Onur İNAN  
_________________

Üye  
Unvanı Adı SOYADI  
_________________

Yukarıdaki sonucu onaylarım.

Prof. Dr. Şakir TAŞDEMİR  
Bilgisayar Mühendisliği Bölüm Başkanı

---

*Sayfa iii*

## PROJE BİLDİRİMİ

Bu projedeki bütün bilgilerin etik davranış ve akademik kurallar çerçevesinde elde edildiğini ve proje yazım kurallarına uygun olarak hazırlanan bu çalışmada bize ait olmayan her türlü ifade ve bilginin kaynağına eksiksiz atıf yapıldığını bildiririz.

## DECLARATION PAGE

We hereby declare that all information in this document has been obtained and presented in accordance with academic rules and ethical conduct. We also declare that, as required by these rules and conduct, we have fully cited and referenced all materials and results that are not original to this work.

İmza: _________________  
Doğukan BALAMAN  
Tarih: .../.../ 2025

İmza: _________________  
Ali YILDIRIM  
Tarih: .../.../ 2025

---

*Sayfa iv*

## ÖZET

**BİLGİSAYAR MÜHENDİSLİĞİ UYGULAMALARI PROJESİ**

**YAPAY ZEKA DESTEKLİ ÜNİVERSİTE BİLGİ ASİSTANI: SELÇUK AI ASİSTAN**

Doğukan BALAMAN, Ali YILDIRIM

Selçuk Üniversitesi  
Teknoloji Fakültesi  
Bilgisayar Mühendisliği Bölümü

Danışman: Prof. Dr. Nurettin DOĞAN  
İkinci Danışman: Dr. Öğr. Üyesi Onur İNAN  
2025, 78 Sayfa

**Jüri**  
Prof. Dr. Nurettin DOĞAN  
Dr. Öğr. Üyesi Onur İNAN  
Unvanı Adı SOYADI

Bu projede, Selçuk Üniversitesi öğrencileri, akademisyenleri ve idari personeli için gizlilik odaklı bir yapay zeka destekli bilgi asistanı geliştirilmiştir. Sistem, kullanıcı verilerinin gizliliğini korumak amacıyla yerel büyük dil modelleri (LLM) kullanarak, tamamen çevrimdışı ortamda çalışabilmektedir. Geliştirilen asistan, Retrieval-Augmented Generation (RAG) tekniği ile üniversiteye özgü bilgi tabanından kaynak gösterimli yanıtlar üretmektedir. Backend tarafında Python FastAPI framework'ü, Ollama LLM çalıştırma motoru, FAISS vektör veritabanı ve LangChain orchestration kütüphanesi kullanılmıştır. Frontend tarafında ise Flutter framework'ü ile çoklu platform (iOS, Android, Web) desteği sağlanmıştır. Proje kapsamında çoklu sağlayıcı (multi-provider) mimarisi tasarlanarak Ollama ve HuggingFace LLM'leri entegre edilmiş, Llama 3.1, Qwen2 ve Deepseek modelleri test edilmiştir. RAG implementasyonu ile %95 üzerinde doğruluk oranı ve %100 kaynak gösterim başarısı elde edilmiştir. CI/CD pipeline kurulumu ile kod kalitesi kontrolleri (pytest, ruff, mypy, flutter analyze) otomatize edilmiştir. Sistem, kritiik bilgi testlerinde (Selçuk Üniversitesi'nin konumu, kuruluş yılı, fakülte bilgileri) %100 başarı göstermiştir. Proje, açık kaynak olarak MIT lisansı altında yayınlanmış ve akademik gizlilik standartlarına uygun şekilde tasarlanmıştır.

**Anahtar Kelimeler:** büyük dil modeli, Flutter, gizlilik, Ollama, RAG, yapay zeka asistanı, yerel LLM

---

*Sayfa v*

## ABSTRACT

**COMPUTER ENGINEERING APPLICATIONS PROJECT**

**AI-POWERED UNIVERSITY INFORMATION ASSISTANT: SELCUK AI ASSISTANT**

Doğukan BALAMAN, Ali YILDIRIM

Selcuk University  
Faculty of Technology  
Department of Computer Engineering

Advisor: Prof. Dr. Nurettin DOĞAN  
Co-Advisor: Dr. Öğr. Üyesi Onur İNAN  
2025, 78 Pages

**Jury**  
Prof. Dr. Nurettin DOĞAN  
Dr. Öğr. Üyesi Onur İNAN  
Title Name SURNAME

In this project, a privacy-focused artificial intelligence-powered information assistant has been developed for Selcuk University students, academics, and administrative staff. The system uses local large language models (LLM) to protect user data privacy and can operate completely offline. The developed assistant generates source-cited responses from a university-specific knowledge base using Retrieval-Augmented Generation (RAG) technique. On the backend side, Python FastAPI framework, Ollama LLM execution engine, FAISS vector database, and LangChain orchestration library were used. On the frontend side, multi-platform support (iOS, Android, Web) was provided with the Flutter framework. Within the scope of the project, a multi-provider architecture was designed and Ollama and HuggingFace LLMs were integrated, and Llama 3.1, Qwen2, and Deepseek models were tested. With RAG implementation, an accuracy rate above 95% and 100% source citation success were achieved. Code quality checks (pytest, ruff, mypy, flutter analyze) were automated with CI/CD pipeline setup. The system showed 100% success in critical information tests (location of Selcuk University, founding year, faculty information). The project was published as open source under the MIT license and designed in accordance with academic privacy standards.

**Keywords:** artificial intelligence assistant, big language model, Flutter, local LLM, Ollama, privacy, RAG

---

*Sayfa vi*

## ÖNSÖZ

Bu proje, modern yapay zeka teknolojilerinin eğitim sektöründe etik ve gizlilik odaklı kullanımına bir örnek teşkil etmek amacıyla geliştirilmiştir. Ticari yapay zeka hizmetlerinin yaygınlaşmasıyla birlikte ortaya çıkan veri gizliliği endişeleri, yerel çalışan ve açık kaynak LLM çözümlerinin önemini artırmıştır.

Selçuk Üniversitesi öğrencileri olarak, kendi üniversitemizin bilgi sistemlerine erişimde yaşadığımız zorlukları gözlemleyerek, bu problemi çözmek için harekete geçtik. Proje süresince, sadece teknik bir çözüm geliştirmekle kalmayıp, aynı zamanda açık kaynak yazılım geliştirme pratiklerini, test odaklı geliştirmeyi (TDD), sürekli entegrasyon ve dağıtımı (CI/CD) deneyimledik.

Bu çalışmanın gerçekleştirilmesinde değerli katkılarından dolayı danışman hocamız Prof. Dr. Nurettin DOĞAN'a, ikinci danışman hocamız Dr. Öğr. Üyesi Onur İNAN'a, proje süresince bize destek olan Bilgisayar Mühendisliği Bölümü akademik kadrosuna ve ailelerimize teşekkürlerimizi sunarız.

Projenin GitHub deposu (https://github.com/esN2k/SelcukAiAssistant) üzerinden açık kaynak olarak yayınlanmış olup, diğer üniversitelerin ve araştırmacıların kendi ihtiyaçlarına uyarlamaları için özgür bir şekilde kullanılabilir.

Doğukan BALAMAN  
Ali YILDIRIM  
Konya / 2025

---

*Sayfa vii*

## İÇİNDEKİLER

PROJE BİLDİRİMİ ..................................................................................................... iii

ÖZET ...................................................................................................................... iv

ABSTRACT ............................................................................................................. v

ÖNSÖZ .................................................................................................................. vi

İÇİNDEKİLER ....................................................................................................... vii

SİMGELER VE KISALTMALAR .......................................................................... ix

**1. GİRİŞ** .............................................................................................................. 1

1.1. Projenin Arka Planı .......................................................................................... 1  
1.2. Projenin Önemi ............................................................................................... 2  
1.3. Projenin Kapsamı ............................................................................................ 3  
1.4. Raporun Organizasyonu .................................................................................. 4

**2. KAYNAK ARAŞTIRMASI** .............................................................................. 5

2.1. Yapay Zeka ve Doğal Dil İşleme Tarihi ......................................................... 5  
2.2. Büyük Dil Modelleri (LLM) ........................................................................... 7  
2.3. Yerel LLM Çözümleri ve Ollama ................................................................... 10  
2.4. RAG (Retrieval-Augmented Generation) ....................................................... 12  
2.5. Flutter ve Mobil Uygulama Geliştirme ........................................................... 15  
2.6. Üniversite Chatbot Örnekleri ......................................................................... 17

**3. MATERYAL VE YÖNTEM** ........................................................................... 19

3.1. Geliştirme Metodolojisi .................................................................................. 19  
3.2. Veri Toplama ve Hazırlama ............................................................................ 21  
3.3. Model Seçimi .................................................................................................. 23  
3.4. RAG Pipeline Tasarımı ................................................................................... 25  
3.5. Değerlendirme Metrikleri ............................................................................... 27

**4. SİSTEM TASARIMI VE UYGULAMA** .......................................................... 29

4.1. Genel Mimari .................................................................................................. 29  
4.2. Backend Mimarisi ........................................................................................... 31  
4.3. Sağlayıcı Deseni (Provider Pattern) ............................................................... 34  
4.4. RAG Servisi Implementasyonu ...................................................................... 36  
4.5. Frontend Mimarisi (Flutter) ............................................................................ 39  
4.6. API Tasarımı ................................................................................................... 42  
4.7. Güvenlik ve Gizlilik ....................................................................................... 44

**5. ARAŞTIRMA BULGULARI VE TARTIŞMA** ................................................ 46

5.1. Test Stratejisi .................................................................................................. 46  
5.2. Kritik Bilgi Doğruluk Testleri ........................................................................ 48  
5.3. RAG Performans Testleri ............................................................................... 50  
5.4. Model Karşılaştırması ..................................................................................... 52  
5.5. Karşılaşılan Zorluklar ve Çözümler ................................................................ 54

**6. SONUÇLAR VE ÖNERİLER** ........................................................................ 58

6.1. Sonuçlar .......................................................................................................... 58  
6.2. Özgün Katkılar ............................................................................................... 60  
6.3. Gelecek Çalışmalar ........................................................................................ 61

**KAYNAKLAR** .................................................................................................. 63

**EKLER** .............................................................................................................. 67

EK-1: API Endpoint Dokümantasyonu .................................................................. 68  
EK-2: Kod Örnekleri .............................................................................................. 70  
EK-3: Test Sonuçları .............................................................................................. 73  
EK-4: Kullanıcı Arayüzü Ekran Görüntüleri ......................................................... 75

**ÖZGEÇMİŞ** ...................................................................................................... 77

---

*Sayfa ix*

## SİMGELER VE KISALTMALAR

**Simgeler**

*Bu projede özel simge kullanılmamıştır.*

**Kısaltmalar**

AI : Artificial Intelligence (Yapay Zeka)  
API : Application Programming Interface (Uygulama Programlama Arayüzü)  
CI/CD : Continuous Integration / Continuous Deployment (Sürekli Entegrasyon / Sürekli Dağıtım)  
CORS : Cross-Origin Resource Sharing (Çapraz Kaynak Paylaşımı)  
FAISS : Facebook AI Similarity Search (Facebook AI Benzerlik Araması)  
GPU : Graphics Processing Unit (Grafik İşleme Birimi)  
HF : HuggingFace  
HTTP : HyperText Transfer Protocol (Hipermetin Aktarım Protokolü)  
JSON : JavaScript Object Notation (JavaScript Nesne Gösterimi)  
KVKK : Kişisel Verilerin Korunması Kanunu  
LLM : Large Language Model (Büyük Dil Modeli)  
LoRA : Low-Rank Adaptation (Düşük Dereceli Adaptasyon)  
NLP : Natural Language Processing (Doğal Dil İşleme)  
OBS : Öğrenci Bilgi Sistemi  
RAG : Retrieval-Augmented Generation (Geri-Getirme Artırılmış Üretim)  
REST : Representational State Transfer (Temsili Durum Aktarımı)  
SI : Système International d'Unités (Uluslararası Birimler Sistemi)  
SSE : Server-Sent Events (Sunucu Taraflı Olaylar)  
TDD : Test-Driven Development (Test Odaklı Geliştirme)  
UI : User Interface (Kullanıcı Arayüzü)  
URL : Uniform Resource Locator (Tekdüzen Kaynak Konumlandırıcı)  
UTF-8 : Unicode Transformation Format - 8 bit (Unicode Dönüşüm Formatı - 8 bit)  
UX : User Experience (Kullanıcı Deneyimi)

---

*Sayfa 1*

# 1. GİRİŞ

## 1.1. Projenin Arka Planı

Yapay zeka teknolojileri, son on yılda özellikle doğal dil işleme (NLP) alanında önemli gelişmeler kaydetmiştir. 2017 yılında Vaswani ve arkadaşları tarafından tanıtılan Transformer mimarisi (Vaswani ve ark., 2017), dil modellerinde devrim niteliğinde bir değişim başlatmıştır. Bu mimari üzerine inşa edilen büyük dil modelleri (LLM), ChatGPT, Google Gemini ve Claude gibi ticari uygulamalarda milyonlarca kullanıcıya hizmet vermektedir.

Ancak, bu ticari LLM hizmetlerinin yaygınlaşmasıyla birlikte veri gizliliği, maliyet ve internet bağımlılığı gibi önemli sorunlar ortaya çıkmıştır. Özellikle eğitim kurumları için, öğrenci ve akademik verilerin üçüncü taraf bulut hizmetlerine gönderilmesi ciddi gizlilik endişeleri yaratmaktadır. Bu bağlamda, yerel olarak çalıştırılabilen ve açık kaynak LLM'ler (Llama, Qwen, Mistral gibi) giderek daha fazla ilgi görmektedir.

Selçuk Üniversitesi, 1975 yılında Konya'da kurulmuş, Türkiye'nin köklü eğitim kurumlarından biridir. Üniversite bünyesinde 20'den fazla fakülte, 50.000'den fazla öğrenci ve binlerce akademik personel bulunmaktadır. Bu büyük topluluk, üniversiteye özgü bilgilere (bölüm bilgileri, akademik takvim, kampüs yerleri, idari süreçler vb.) sürekli olarak erişim ihtiyacı duymaktadır.

Mevcut bilgi erişim yöntemleri, web sitesi navigasyonu, arama motorları ve ilgili birimlerle iletişim gibi geleneksel kanallara dayanmaktadır. Bu yöntemler, zaman alıcı ve kullanıcı dostu olmayan süreçler içermektedir. Ayrıca, genel amaçlı yapay zeka asistanları (ChatGPT, Gemini vb.), üniversiteye özgü detaylı bilgilerde yetersiz kalmakta ve hallüsinasyon (uydurma bilgi üretme) riski taşımaktadır.

Bu proje kapsamında geliştirilen "Selçuk AI Asistan", yukarıda belirtilen problemleri çözmek amacıyla tasarlanmıştır. Sistem, tamamen yerel çalışan LLM'ler kullanarak veri gizliliğini korumakta, Retrieval-Augmented Generation (RAG) tekniği ile kaynak gösterimli ve doğrulanabilir yanıtlar üretmekte ve çoklu platform (iOS, Android, Web) desteği ile geniş bir kullanıcı kitlesine erişmektedir.

Projenin teknik altyapısı, modern yazılım geliştirme pratiklerini benimseyerek oluşturulmuştur. Backend tarafında Python FastAPI framework'ü ile RESTful API tasarlanmış, Ollama LLM çalıştırma motoru entegre edilmiş ve FAISS vektör veritabanı ile RAG implementasyonu gerçekleştirilmiştir. Frontend tarafında Flutter framework'ü ile Material Design 3 standartlarına uygun, responsive ve erişilebilir bir kullanıcı arayüzü geliştirilmiştir.

## 1.2. Projenin Önemi

Bu projenin akademik ve pratik önemi aşağıdaki başlıklar altında özetlenebilir:

**Gizlilik ve Veri Güvenliği:** Kullanıcı verileri, üçüncü taraf bulut hizmetlerine gönderilmeden tamamen yerel ortamda işlenmektedir. Bu yaklaşım, KVKK (Kişisel Verilerin Korunması Kanunu) uyumluluğu açısından kritik öneme sahiptir. Akademik kurumların öğrenci ve personel verileri üzerinde tam kontrol sağlaması, modern veri koruma mevzuatının temel gereksinimlerinden biridir.

**Çevrimdışı Çalışabilirlik:** Sistem, internet bağlantısı olmadan temel sohbet işlevlerini sürdürebilmektedir. RAG özelliği, yerel veritabanından bilgi sağladığı için internet kesintilerinden etkilenmemektedir. Bu özellik, sınırlı internet erişimi olan kampüs alanları veya mobil kullanım senaryoları için önemli bir avantaj sağlamaktadır.

**Kaynak Gösterimi ve Doğrulanabilirlik:** RAG implementasyonu sayesinde, sistem verdiği her yanıtın hangi kaynaklardan türetildiğini gösterebilmektedir. Bu özellik, akademik bağlamda kritik öneme sahiptir çünkü kullanıcılar bilginin doğruluğunu kaynak dokümanları kontrol ederek teyit edebilmektedir.

**Çoklu Sağlayıcı Mimarisi:** Sistem, farklı LLM sağlayıcılarını (Ollama, HuggingFace) aynı arayüz üzerinden yönetebilmektedir. Bu esneklik, ilerleyen dönemlerde yeni model ve teknolojilerin entegrasyonunu kolaylaştırmaktadır. Ayrıca, farklı kullanım senaryoları için optimize edilmiş modeller seçilebilmektedir (örneğin, hız için 3B model, kalite için 7B model).

**Açık Kaynak ve Eğitim Değeri:** Proje, MIT lisansı altında açık kaynak olarak yayınlanmıştır. Bu yaklaşım, diğer üniversitelerin ve araştırmacıların benzer sistemler geliştirmesine olanak sağlamaktadır. Ayrıca, modern yazılım geliştirme pratiklerinin (CI/CD, test otomasyonu, kod kalitesi kontrolleri) uygulamalı örneğini sunmaktadır.

**Maliyet Etkinliği:** Ticari LLM API'leri, yoğun kullanımda önemli maliyetler oluşturmaktadır. Yerel LLM çözümü, sadece sunucu maliyeti gerektirdiği için uzun vadede daha ekonomik bir çözüm sunmaktadır. Bir üniversite ölçeğinde, bu maliyet farkı yıllık binlerce dolar tutabilmektedir.

**Akademik Doğruluk:** Genel amaçlı LLM'ler, kuruma özgü detaylarda yanlış bilgi üretebilmektedir. Örneğin, GPT-4'ün "Selçuk Üniversitesi nerede?" sorusuna "İzmir" yanıtı verdiği gözlemlenmiştir. RAG tabanlı sistemimiz, üniversite resmi kaynaklarından beslenen bilgi tabanı sayesinde %100 doğrulukla kritik bilgileri sunmaktadır.

## 1.3. Projenin Kapsamı

Proje kapsamında aşağıdaki bileşenler geliştirilmiştir:

**Backend Sistemi:**
- FastAPI tabanlı RESTful API servisi
- Ollama ve HuggingFace LLM entegrasyonları
- FAISS tabanlı RAG implementasyonu
- LangChain orchestration katmanı
- Çoklu sağlayıcı yönetim sistemi (Provider Pattern)
- CORS, input validation ve error handling güvenlik mekanizmaları
- Server-Sent Events (SSE) ile streaming response desteği

**Frontend Uygulaması:**
- Flutter framework'ü ile cross-platform (iOS, Android, Web) uygulama
- GetX state management
- Material Design 3 uyumlu kullanıcı arayüzü
- Markdown rendering desteği
- Responsive tasarım
- Karanlık mod desteği
- Çoklu dil desteği (Türkçe, İngilizce)

**Veri ve Bilgi Tabanı:**
- Selçuk Üniversitesi genel bilgileri (75+ soru-cevap çifti)
- Bilgisayar Mühendisliği Bölümü detaylı bilgileri
- Web scraping ile toplanan üniversite web sitesi verileri
- RAG için hazırlanmış doküman koleksiyonu
- FAISS vektör indeksi ve metadata depoları

**Test ve Kalite Altyapısı:**
- Backend: pytest, ruff linter, mypy type checker
- Frontend: flutter analyze, flutter test
- CI/CD pipeline (GitHub Actions)
- Encoding guard (UTF-8 doğrulama)
- Kritik bilgi doğruluk testleri

**Dokümantasyon:**
- Kapsamlı README ve kurulum kılavuzları
- API endpoint dokümantasyonu
- Mimari tasarım dokümanları
- Test raporları
- Sorun giderme rehberleri

**Proje Kapsamı Dışında Bırakılan Unsurlar:**

Aşağıdaki özellikler, zaman ve kaynak kısıtları nedeniyle proje kapsamı dışında bırakılmıştır ancak gelecek çalışmalar için planlanmıştır:

- Öğrenci Bilgi Sistemi (OBS) entegrasyonu
- Sesli asistan (speech-to-text ve text-to-speech)
- Kişisel öneri sistemi (öğrenci profiline dayalı)
- Proaktif bildirimler
- Sosyal özellikler (kullanıcı toplulukları)
- Fine-tuned Selçuk-specific model

## 1.4. Raporun Organizasyonu

Bu rapor, altı ana bölümden oluşmaktadır:

**Bölüm 1 - Giriş:** Projenin arka planı, önemi ve kapsamı tanıtılmaktadır.

**Bölüm 2 - Kaynak Araştırması:** Yapay zeka, doğal dil işleme, büyük dil modelleri, RAG tekniği, Flutter framework'ü ve benzer üniversite chatbot projeleri hakkında literatür taraması sunulmaktadır.

**Bölüm 3 - Materyal ve Yöntem:** Geliştirme metodolojisi, veri toplama ve hazırlama süreçleri, model seçim kriterleri, RAG pipeline tasarımı ve değerlendirme metrikleri açıklanmaktadır.

**Bölüm 4 - Sistem Tasarımı ve Uygulama:** Genel mimari, backend ve frontend detayları, API tasarımı ve güvenlik mekanizmaları anlatılmaktadır.

**Bölüm 5 - Araştırma Bulguları ve Tartışma:** Test sonuçları, performans değerlendirmeleri, model karşılaştırmaları ve karşılaşılan zorluklar tartışılmaktadır.

**Bölüm 6 - Sonuçlar ve Öneriler:** Projenin genel değerlendirmesi, özgün katkıları ve gelecek çalışma önerileri sunulmaktadır.

---

*Sayfa 5*

# 2. KAYNAK ARAŞTIRMASI

## 2.1. Yapay Zeka ve Doğal Dil İşleme Tarihi

Yapay zeka alanı, 1950'li yıllarda Alan Turing'in "Computing Machinery and Intelligence" makalesinde ortaya atılan "Turing Testi" kavramı ile başlamıştır (Turing, 1950). Bu test, bir makinenin insan benzeri zeka gösterip gösteremeyeceğini değerlendirmek için tasarlanmıştır.

Doğal dil işleme (NLP), yapay zekanın insan dilini anlama ve üretme yeteneğine odaklanan bir alt dalıdır. İlk önemli NLP sistemlerinden biri, 1966 yılında Joseph Weizenbaum tarafından geliştirilen ELIZA chatbot'udur (Weizenbaum, 1966). ELIZA, basit pattern matching teknikleri kullanarak psikoterapi oturumlarını simüle edebiliyordu.

1980'li ve 1990'lı yıllarda, istatistiksel NLP yöntemleri önem kazanmıştır. Hidden Markov Models (HMM) ve N-gram dil modelleri, makine çevirisi ve konuşma tanıma sistemlerinde yaygın olarak kullanılmaya başlanmıştır.

2000'li yılların başında, makine öğrenmesi algoritmaları NLP alanında devrim yaratmıştır. Support Vector Machines (SVM) ve Maximum Entropy modelleri, metin sınıflandırma ve named entity recognition görevlerinde yüksek başarı göstermiştir.

2013 yılında, Mikolov ve arkadaşları tarafından geliştirilen Word2Vec, kelimelerin vektör uzayında temsil edilmesinde önemli bir ilerleme sağlamıştır (Mikolov ve ark., 2013). Bu yaklaşım, kelimelerin semantik ilişkilerini öğrenebilen yoğun vektör gösterimlerini (dense embeddings) mümkün kılmıştır.

**Transformer Devrimi:**

2017 yılı, NLP tarihinde bir dönüm noktası olmuştur. Vaswani ve arkadaşları, "Attention Is All You Need" makalesinde Transformer mimarisini tanıtmıştır (Vaswani ve ark., 2017). Bu mimari, önceki Recurrent Neural Network (RNN) ve Long Short-Term Memory (LSTM) tabanlı modellerin sınırlamalarını aşmıştır:

- **Self-Attention Mekanizması:** Modelin, bir cümledeki her kelimenin diğer tüm kelimelerle ilişkisini paralel olarak hesaplamasını sağlar.
- **Pozisyonel Encoding:** Kelime sırasını korunmasını mümkün kılar.
- **Paralel İşleme:** RNN'lerin sıralı işleme gereksinimini ortadan kaldırarak eğitim süresini önemli ölçüde azaltır.

Transformer mimarisi üzerine inşa edilen ilk önemli model, 2018 yılında Google tarafından geliştirilen BERT (Bidirectional Encoder Representations from Transformers) olmuştur (Devlin ve ark., 2018). BERT, bidirectional (çift yönlü) context modellemesi ile cümle anlamını daha iyi yakalayabilmiştir.

**Büyük Dil Modelleri Çağı:**

2018-2020 yılları arasında, model boyutları katlanarak artmıştır:

- GPT-1 (OpenAI, 2018): 117M parametre
- GPT-2 (OpenAI, 2019): 1.5B parametre
- GPT-3 (OpenAI, 2020): 175B parametre
- GPT-4 (OpenAI, 2023): ~1.7T parametre (tahmini)

Bu büyüme, LLM'lerin few-shot ve zero-shot learning yeteneklerini ortaya çıkarmıştır. Artık modeller, özel eğitim olmadan birçok görevi gerçekleştirebilmektedir.

**Açık Kaynak LLM'ler:**

2023 yılında Meta AI, Llama (Large Language Model Meta AI) modelini açık kaynak olarak yayınlamıştır (Touvron ve ark., 2023). Bu gelişme, araştırmacıların ve kurumların kendi LLM altyapılarını kurabilmelerini sağlamıştır. Llama, akademik araştırmalar ve özel kullanımlar için değerli bir kaynak haline gelmiştir.

Alibaba Cloud, Qwen (Qianwen) model ailesini geliştirerek çok dilli destek konusunda önemli ilerlemeler kaydetmiştir (Alibaba Cloud, 2023). Qwen modelleri, Çince ve İngilizce başta olmak üzere 50+ dilde yüksek performans göstermektedir.

## 2.2. Büyük Dil Modelleri (LLM)

Büyük dil modelleri, milyarlarca parametre içeren ve büyük metin korpusları üzerinde eğitilmiş yapay sinir ağlarıdır. Bu modeller, dil görevlerinde (metin oluşturma, çeviri, özetleme, soru-cevap vb.) insan benzeri performans gösterebilmektedir.

**LLM'lerin Temel Bileşenleri:**

1. **Tokenization:** Metin girişlerinin, model tarafından işlenebilir alt birimlere (token) dönüştürülmesi. Byte-Pair Encoding (BPE) ve SentencePiece gibi yöntemler kullanılır.

2. **Embedding Layer:** Token'ların yoğun vektör gösterimlerine dönüştürülmesi. Bu katman, semantik benzerlik ilişkilerini öğrenir.

3. **Transformer Blokları:** Çoklu self-attention ve feed-forward katmanlarından oluşur. Modern LLM'ler, onlarca veya yüzlerce transformer bloğu içerebilir.

4. **Output Layer:** Modelin bir sonraki token için olasılık dağılımı ürettiği katman.

**Eğitim Süreci:**

LLM'ler, genellikle iki aşamalı bir eğitim sürecinden geçer:

1. **Pre-training (Ön Eğitim):** Model, geniş bir metin korpusu üzerinde unsupervised learning ile eğitilir. Amaç, dil yapısını ve genel bilgiyi öğrenmektir. Causal language modeling (bir sonraki kelimeyi tahmin etme) veya masked language modeling (maskelenmiş kelimeleri tahmin etme) görevleri kullanılır.

2. **Fine-tuning (İnce Ayar):** Model, belirli görevler için supervised learning ile ince ayar yapılır. Bu aşamada, instruction tuning ve reinforcement learning from human feedback (RLHF) teknikleri uygulanabilir.

**Ticari LLM Servisleri:**

- **GPT-4 (OpenAI):** En güçlü ticari LLM'lerden biri. Multimodal yeteneklere (metin + görsel) sahip. API üzerinden erişilebilir ancak maliyet yüksektir ($0.03/1K token giriş, $0.06/1K token çıkış).

- **Google Gemini:** Google'ın GPT-4 rakibi. Ücretsiz katman sunuyor ancak rate limiting ve veri gizliliği sorunları mevcut.

- **Claude (Anthropic):** Güvenlik ve etik odaklı LLM. Constitutional AI yaklaşımı ile zararlı içerik üretimini azaltıyor.

**Açık Kaynak LLM'ler:**

- **Llama 3.1 (Meta):** 8B, 70B ve 405B parametre boyutlarında modeller. Apache 2.0 lisansı altında akademik ve ticari kullanım için açık. Instruction-tuned ve chat-optimized versiyonları mevcut.

- **Qwen2 (Alibaba):** 0.5B'den 72B'ye kadar çeşitli boyutlarda modeller. Türkçe dahil 50+ dilde yüksek performans. Açık kaynak ve ticari kullanıma uygun.

- **Mistral (Mistral AI):** Avrupa merkezli, açık kaynak LLM. 7B ve Mixtral 8x7B (sparse MoE architecture) versiyonları popüler.

- **Deepseek:** Çince odaklı, açık kaynak LLM. Reasoning yetenekleri güçlü.

**Model Boyutu ve Performans Trade-off'u:**

| Model Boyutu | Parametre Sayısı | VRAM Gereksinimi (FP16) | Hız | Kalite |
|--------------|------------------|-------------------------|-----|--------|
| Küçük | 1B-3B | 2-6 GB | Çok Hızlı | Orta |
| Orta | 7B-13B | 14-26 GB | Orta | İyi |
| Büyük | 30B-70B | 60-140 GB | Yavaş | Çok İyi |
| Çok Büyük | 100B+ | 200+ GB | Çok Yavaş | En İyi |

Projemizde, kullanılabilirlik ve performans dengesi gözetilerek 3B (Llama 3.2) ve 7B (Qwen2) boyutlu modeller tercih edilmiştir.

**Quantization (Nicemleme):**

LLM'lerin bellek gereksinimlerini azaltmak için quantization teknikleri kullanılır:

- **FP16:** %50 bellek tasarrufu, minimal kalite kaybı
- **INT8:** %75 bellek tasarrufu, kabul edilebilir kalite kaybı
- **4-bit (GPTQ, GGUF):** %87.5 bellek tasarrufu, orta kalite kaybı

Ollama, GGUF formatını destekleyerek 4-bit quantized modellerin CPU üzerinde çalıştırılmasını sağlar.

## 2.3. Yerel LLM Çözümleri ve Ollama

Yerel LLM çalıştırma, modelin kullanıcının kendi donanımında (CPU/GPU) execute edilmesi anlamına gelir. Bu yaklaşımın avantajları:

- **Tam Gizlilik:** Veri, cihazdan dışarı çıkmaz
- **Maliyet:** API ücretleri yok, sadece donanım maliyeti
- **Özelleştirilebilirlik:** Model, fine-tune edilebilir
- **Offline Kullanım:** İnternet bağlantısı gerekmiyor

**Yerel LLM Çalıştırma Araçları:**

1. **Ollama:** Docker-benzeri kullanım kolaylığı sunan LLM çalıştırma platformu. Model yönetimi basit (`ollama pull`, `ollama run`). RESTful API sağlar. Mac, Linux ve Windows desteği var.

2. **LM Studio:** Grafiksel arayüzlü desktop uygulaması. Model keşfi ve indirme kolaylığı. Chat arayüzü entegre. Ancak, server deployment için uygun değil.

3. **GPT4All:** Offline çalışan, privacy-first LLM tool. Python bindings mevcut. Ancak, model çeşitliliği Ollama'dan daha az.

4. **llama.cpp:** C++ ile yazılmış, yüksek performanslı inference library. Ollama'nın altında bu kütüphane çalışır.

**Ollama Mimarisi ve Kullanımı:**

Ollama, LLM'leri kolayca indirme, çalıştırma ve yönetme için tasarlanmış bir platformdur. Temel özellikleri:

- **Model Registry:** HuggingFace ve diğer kaynaklardan küratörlü modeller
- **Automatic GPU Detection:** NVIDIA, AMD ve Apple Silicon GPU'larını otomatik algılama
- **Hot Reloading:** Model değişikliklerinde servis yeniden başlatma gerektirmez
- **REST API:** OpenAI-compatible API endpoint'leri

**Ollama Kurulumu:**

```bash
# Windows (Winget)
winget install Ollama.Ollama

# macOS (Homebrew)
brew install ollama

# Linux
curl https://ollama.ai/install.sh | sh
```

**Model İndirme ve Çalıştırma:**

```bash
# Llama 3.2 3B modelini indir
ollama pull llama3.2:3b

# Qwen2 7B modelini indir
ollama pull qwen2:7b

# Model çalıştır (etkileşimli mod)
ollama run llama3.2:3b

# API server başlat (arka planda)
ollama serve
```

**Ollama API Kullanımı:**

```python
import requests

def chat_with_ollama(model, messages):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": False
    }
    response = requests.post(url, json=payload)
    return response.json()["message"]["content"]

# Örnek kullanım
messages = [
    {"role": "user", "content": "Selçuk Üniversitesi hakkında bilgi ver"}
]
answer = chat_with_ollama("llama3.2:3b", messages)
print(answer)
```

**Modelfile ile Özelleştirme:**

Ollama, Dockerfile benzeri bir `Modelfile` formatı ile model özelleştirmesine izin verir:

```modelfile
FROM llama3.2:3b

# System prompt
SYSTEM """
Sen Selçuk Üniversitesi'nin AI asistanısın. 
Görevin, öğrencilere ve akademisyenlere yardımcı olmak.
Daima Türkçe ve saygılı bir dille yanıt ver.
"""

# Model parametreleri
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 4096
```

Model oluşturma:

```bash
ollama create selcuk-assistant -f ./Modelfile
ollama run selcuk-assistant
```

**GPU/CPU Performans Karşılaştırması:**

Projemizde yapılan benchmark testlerinde (Llama 3.2 3B, 512 token çıkış):

| Donanım | İşleme Süresi | Token/sn |
|---------|---------------|----------|
| NVIDIA RTX 3060 (12GB) | 8.2s | 62.4 |
| CPU Intel i7-11700 (8 core) | 24.6s | 20.8 |
| Apple M1 (8 core) | 15.3s | 33.5 |

GPU kullanımı, CPU'ya göre ~3x hızlanma sağlamıştır.

## 2.4. RAG (Retrieval-Augmented Generation)

RAG, LLM'lerin hallüsinasyon problemini azaltmak ve güncel/özel bilgi sağlamak için geliştirilmiş bir tekniktir. Lewis ve arkadaşları tarafından 2020 yılında tanıtılmıştır (Lewis ve ark., 2020).

**RAG'in Temel İlkesi:**

Geleneksel LLM yaklaşımında, model sadece parametrelerinde saklanan bilgiyi kullanarak yanıt üretir. Bu, iki ana problem yaratır:

1. **Güncellik:** Model, eğitim tarihinden sonraki bilgileri bilmez.
2. **Hallüsinasyon:** Model, bilmediği konularda mantıklı görünen ama yanlış bilgiler üretebilir.

RAG, bu problemleri şu şekilde çözer:

1. **Retrieval (Geri-Getirme):** Kullanıcı sorusuna göre, ilgili dokümanlar bir bilgi tabanından aranır.
2. **Augmentation (Zenginleştirme):** Bulunan dokümanlar, LLM'e context olarak sağlanır.
3. **Generation (Üretim):** LLM, sağlanan context'i kullanarak yanıt üretir.

**RAG Pipeline Bileşenleri:**

1. **Doküman İşleme:**
   - **Chunking:** Uzun dokümanlar, 200-1000 token boyutunda parçalara bölünür.
   - **Overlap:** Parçalar arasında 50-100 token overlap bırakılır (context kaybını önler).

2. **Embedding Oluşturma:**
   - Her doküman parçası, embedding modeli ile vektöre dönüştürülür.
   - Popüler embedding modelleri:
     - sentence-transformers/all-MiniLM-L6-v2 (384 dim, İngilizce)
     - sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (768 dim, 50+ dil)
     - OpenAI text-embedding-3-small (1536 dim, ücretli)

3. **Vektör Veritabanı:**
   - Embedding'ler, hızlı similarity search için özel veritabanlarında saklanır.
   - **FAISS (Facebook AI Similarity Search):** C++ tabanlı, CPU-friendly, milyonlarca vektörü saniyeler içinde arayabilir.
   - **ChromaDB:** Python-native, metadata filtering desteği güçlü.
   - **Pinecone:** Cloud-based, scalable ama ücretli.
   - **Weaviate:** GraphQL API, hybrid search desteği.

4. **Similarity Search:**
   - Kullanıcı sorusu embedding'e dönüştürülür.
   - Vektör veritabanında cosine similarity ile en yakın K doküman bulunur.
   - Popüler similarity metrikleri:
     - Cosine Similarity: $\frac{A \cdot B}{||A|| \times ||B||}$
     - Euclidean Distance: $||A - B||$
     - Dot Product: $A \cdot B$

5. **Context Construction:**
   - Bulunan dokümanlar, LLM promptuna eklenir:

```
System: Sen bir yardımcı asistansın.

Context:
[Doküman 1 içeriği]
[Doküman 2 içeriği]
[Doküman 3 içeriği]

User: [Kullanıcı sorusu]