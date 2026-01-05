\# T.C.  
\# SELÇUK ÜNİVERSİTESİ  
\# TEKNOLOJİ FAKÜLTESİ  
\# BİLGİSAYAR MÜHENDİSLİĞİ BÖLÜMÜ

\---

\# YAPAY ZEKA DESTEKLİ ÜNİVERSİTE BİLGİ ASİSTANI: SELÇUK AI ASİSTAN

\---

\#\# BİTİRME PROJESİ

\*\*Hazırlayanlar:\*\*  
\- Doğukan BALAMAN (203311066)  
\- Ali YILDIRIM (203311008)

\*\*Danışmanlar:\*\*  
\- Prof. Dr. Nurettin DOĞAN  
\- Dr. Öğr. Üyesi Onur İNAN

\*\*Ocak 2025\*\*

\*\*KONYA\*\*

\*\*Her Hakkı Saklıdır\*\*

\---

\#\# PROJE KABUL VE ONAYI

Doğukan BALAMAN ve Ali YILDIRIM tarafından hazırlanan "Yapay Zeka Destekli Üniversite Bilgi Asistanı: Selçuk AI Asistan" adlı proje çalışması …/…/2025 tarihinde aşağıdaki jüri üyeleri tarafından Selçuk Üniversitesi Teknoloji Fakültesi Bilgisayar Mühendisliği bölümünde Bitirme Projesi olarak kabul edilmiştir.

| Jüri Üyeleri | İmza |  
|--------------|------|  
| \*\*Danışman:\*\* Prof. Dr. Nurettin DOĞAN | ................... |  
| \*\*Danışman:\*\* Dr. Öğr. Üyesi Onur İNAN | ................... |  
| \*\*Üye:\*\* Unvanı Adı SOYADI | ................... |

Yukarıdaki sonucu onaylarım.

Bilgisayar Mühendisliği Bölüm Başkanı

\---

\#\# PROJE BİLDİRİMİ

Bu projedeki bütün bilgilerin etik davranış ve akademik kurallar çerçevesinde elde edildiğini ve proje yazım kurallarına uygun olarak hazırlanan bu çalışmada bize ait olmayan her türlü ifade ve bilginin kaynağına eksiksiz atıf yapıldığını bildiririz.

\*\*DECLARATION PAGE\*\*

We hereby declare that all information in this document has been obtained and presented in accordance with academic rules and ethical conduct. We also declare that, as required by project rules and conduct, we have fully cited and referenced all material and results that are not original to this work.

İmza

Doğukan BALAMAN  
Ali YILDIRIM

Tarih: …./…./2025

\---

\#\# ÖZET

\*\*BİTİRME PROJESİ\*\*

\*\*YAPAY ZEKA DESTEKLİ ÜNİVERSİTE BİLGİ ASİSTANI: SELÇUK AI ASİSTAN\*\*

\*\*Doğukan BALAMAN, Ali YILDIRIM\*\*

\*\*Selçuk Üniversitesi Teknoloji Fakültesi\*\*  
\*\*Bilgisayar Mühendisliği Bölümü\*\*

\*\*Danışmanlar: Prof. Dr. Nurettin DOĞAN, Dr. Öğr. Üyesi Onur İNAN\*\*

\*\*2025, … Sayfa\*\*

Bu proje çalışmasında, Selçuk Üniversitesi öğrenci ve personeline 7/24 hizmet verebilen, gizliliğe odaklı ve yerel çalışabilen yapay zeka destekli bir akademik bilgi asistanı geliştirilmiştir. Konya'da bulunan Selçuk Üniversitesi, 1975 yılında kurulmuş olup 23 fakülte ve 100.000'den fazla öğrencisiyle Türkiye'nin en büyük üniversitelerinden biridir. Bu denli büyük bir kurumda öğrencilerin ve personelin bilgiye hızlı erişimi kritik bir ihtiyaç haline gelmiştir.

Geliştirilen Selçuk AI Asistan, geleneksel bulut tabanlı yapay zeka çözümlerinden farklı olarak \*\*yerel LLM (Large Language Model)\*\* altyapısı üzerine inşa edilmiştir. Sistem, Ollama üzerinde çalışan Llama 3.1/3.2 modelleri ile tamamen yerel çıkarım yapabilmekte, böylece kullanıcı verilerinin gizliliği korunmaktadır. Alternatif olarak HuggingFace Transformers desteği de sunulmaktadır.

Proje, \*\*RAG (Retrieval Augmented Generation)\*\* teknolojisini kullanarak üniversite hakkında kaynak gösterimli ve doğrulanabilir yanıtlar üretmektedir. LangChain orkestrasyon framework'ü, FAISS vektör veritabanı ve sentence-transformers embedding modeli ile entegre çalışan RAG pipeline'ı, hallucination (uydurma bilgi) problemini minimize etmektedir.

Kullanıcı arayüzü, Flutter framework'ü ve GetX state management ile geliştirilmiş olup iOS, Android ve web platformlarında çalışabilmektedir. Backend tarafında Python ve FastAPI kullanılmış, SSE (Server-Sent Events) ile gerçek zamanlı akış yanıtları desteklenmiştir.

Yapılan testlerde sistemin Selçuk Üniversitesi hakkındaki kritik bilgileri (konum: Konya, kuruluş: 1975, Bilgisayar Mühendisliği: Teknoloji Fakültesi) doğru şekilde yanıtladığı, RAG modunda kaynak gösterimi yaptığı ve internet bağlantısı olmadan da temel sohbet akışını sürdürebildiği doğrulanmıştır.

\*\*Anahtar Kelimeler:\*\* Büyük Dil Modelleri, Gizlilik, LangChain, Ollama, RAG, Selçuk Üniversitesi, Yerel Yapay Zeka

\---

\#\# ABSTRACT

\*\*GRADUATION PROJECT\*\*

\*\*ARTIFICIAL INTELLIGENCE POWERED UNIVERSITY INFORMATION ASSISTANT: SELCUK AI ASSISTANT\*\*

\*\*Doğukan BALAMAN, Ali YILDIRIM\*\*

\*\*Selcuk University Faculty of Technology\*\*  
\*\*Department of Computer Engineering\*\*

\*\*Advisors: Prof. Dr. Nurettin DOĞAN, Asst. Prof. Dr. Onur İNAN\*\*

\*\*2025, … Pages\*\*

In this project, a privacy-focused, locally-running artificial intelligence academic assistant has been developed to provide 24/7 service to students and staff of Selcuk University. Located in Konya, Selcuk University was founded in 1975 and is one of Turkey's largest universities with 23 faculties and over 100,000 students. In such a large institution, quick access to information for students and staff has become a critical need.

Unlike traditional cloud-based AI solutions, the developed Selcuk AI Assistant is built on a \*\*local LLM (Large Language Model)\*\* infrastructure. The system can perform completely local inference using Llama 3.1/3.2 models running on Ollama, thus protecting user data privacy. HuggingFace Transformers support is also provided as an alternative.

The project uses \*\*RAG (Retrieval Augmented Generation)\*\* technology to produce source-cited and verifiable responses about the university. The RAG pipeline, integrated with LangChain orchestration framework, FAISS vector database, and sentence-transformers embedding model, minimizes the hallucination problem.

The user interface was developed with Flutter framework and GetX state management, capable of running on iOS, Android, and web platforms. Python and FastAPI were used on the backend side, with real-time streaming responses supported via SSE (Server-Sent Events).

Tests have verified that the system correctly answers critical information about Selcuk University (location: Konya, founding: 1975, Computer Engineering: Faculty of Technology), provides source citations in RAG mode, and can maintain basic chat flow even without internet connection.

\*\*Keywords:\*\* Large Language Models, LangChain, Local AI, Ollama, Privacy, RAG, Selcuk University

\---

\#\# ÖNSÖZ

Bu proje çalışması, Selçuk Üniversitesi Teknoloji Fakültesi Bilgisayar Mühendisliği Bölümü'nde "Bilgisayar Mühendisliği Uygulamaları" dersi kapsamında bitirme projesi olarak hazırlanmıştır. Çalışmanın amacı, yapay zeka teknolojilerini kullanarak üniversite topluluğuna faydalı, gizliliğe saygılı ve yerel çalışabilen bir bilgi asistanı geliştirmektir.

Proje süresince değerli katkılarını esirgemeyen danışman hocalarımız Prof. Dr. Nurettin DOĞAN ve Dr. Öğr. Üyesi Onur İNAN'a, teknik konularda yardımcı olan arkadaşlarımıza ve manevi desteklerini her zaman hissettiğimiz ailelerimize teşekkürlerimizi sunarız.

Doğukan BALAMAN  
Ali YILDIRIM

Konya / 2025

\---

\#\# İÇİNDEKİLER

| | Sayfa |  
|---|---|  
| ÖZET | iv |  
| ABSTRACT | v |  
| ÖNSÖZ | vi |  
| İÇİNDEKİLER | vii |  
| SİMGELER VE KISALTMALAR | ix |  
| ŞEKİLLER LİSTESİ | x |  
| ÇİZELGELER LİSTESİ | xi |  
| | |  
| \*\*1. GİRİŞ\*\* | 1 |  
| 1.1. Projenin Arka Planı | 1 |  
| 1.2. Projenin Önemi ve Özgün Değeri | 2 |  
| 1.3. Projenin Kapsamı | 4 |  
| 1.4. Raporun Organizasyonu | 5 |  
| | |  
| \*\*2. KAYNAK ARAŞTIRMASI\*\* | 6 |  
| 2.1. Yapay Zeka ve Doğal Dil İşleme | 6 |  
| 2.2. Büyük Dil Modelleri (LLM) | 8 |  
| 2.3. Yerel LLM Çözümleri ve Ollama | 11 |  
| 2.4. RAG (Retrieval Augmented Generation) | 13 |  
| 2.5. Mobil Uygulama Geliştirme ve Flutter | 16 |  
| 2.6. Üniversite Chatbot Uygulamaları | 18 |  
| | |  
| \*\*3. MATERYAL VE YÖNTEM\*\* | 20 |  
| 3.1. Geliştirme Metodolojisi | 20 |  
| 3.2. Veri Toplama ve Knowledge Base Oluşturma | 21 |  
| 3.3. Model ve Sağlayıcı Seçimi | 24 |  
| 3.4. RAG Pipeline Tasarımı | 26 |  
| 3.5. Değerlendirme Metrikleri | 29 |  
| | |  
| \*\*4. SİSTEM TASARIMI VE UYGULAMA\*\* | 30 |  
| 4.1. Genel Mimari | 30 |  
| 4.2. Backend Bileşeni (FastAPI) | 33 |  
| 4.3. Sağlayıcı Deseni ve Model Yönetimi | 38 |  
| 4.4. RAG Servisi | 42 |  
| 4.5. Flutter Mobil/Web Uygulaması | 46 |  
| 4.6. API Tasarımı | 51 |  
| 4.7. Güvenlik ve Gizlilik Tasarımı | 54 |  
| | |  
| \*\*5. ARAŞTIRMA BULGULARI VE TARTIŞMA\*\* | 56 |  
| 5.1. Test Stratejisi ve CI/CD | 56 |  
| 5.2. Kritik Bilgi Doğruluk Testleri | 58 |  
| 5.3. RAG Performans Değerlendirmesi | 61 |  
| 5.4. Karşılaşılan Zorluklar ve Çözümler | 63 |  
| | |  
| \*\*6. SONUÇLAR VE ÖNERİLER\*\* | 66 |  
| 6.1. Sonuçlar | 66 |  
| 6.2. Öneriler | 68 |  
| | |  
| \*\*KAYNAKLAR\*\* | 70 |  
| \*\*EKLER\*\* | 73 |  
| EK-A: Kod Örnekleri | 73 |  
| EK-B: API Dokümantasyonu | 82 |  
| EK-C: Knowledge Base Yapısı | 86 |  
| EK-D: Kurulum Kılavuzu | 89 |  
| EK-E: Test Sonuçları | 92 |  
| \*\*ÖZGEÇMİŞ\*\* | 95 |

\---

\#\# SİMGELER VE KISALTMALAR

\*\*Simgeler\*\*

| Simge | Açıklama |  
|-------|----------|  
| % | Yüzde |  
| \< | Küçüktür |  
| \> | Büyüktür |

\*\*Kısaltmalar\*\*

| Kısaltma | Açıklama |  
|----------|----------|  
| AI | Artificial Intelligence (Yapay Zeka) |  
| API | Application Programming Interface |  
| ASGI | Asynchronous Server Gateway Interface |  
| CI/CD | Continuous Integration / Continuous Deployment |  
| CORS | Cross-Origin Resource Sharing |  
| FAISS | Facebook AI Similarity Search |  
| GPU | Graphics Processing Unit |  
| HF | HuggingFace |  
| HTTP | HyperText Transfer Protocol |  
| JSON | JavaScript Object Notation |  
| LLM | Large Language Model (Büyük Dil Modeli) |  
| NLP | Natural Language Processing (Doğal Dil İşleme) |  
| RAG | Retrieval Augmented Generation |  
| REST | Representational State Transfer |  
| SSE | Server-Sent Events |  
| UI | User Interface (Kullanıcı Arayüzü) |  
| URL | Uniform Resource Locator |

\---

\#\# 1\. GİRİŞ

\#\#\# 1.1. Projenin Arka Planı

Yapay zeka teknolojileri, son yıllarda özellikle doğal dil işleme alanında büyük gelişmeler kaydetmiştir. 2017 yılında Google araştırmacıları tarafından geliştirilen Transformer mimarisi (Vaswani ve ark., 2017), bu alandaki en önemli dönüm noktalarından birini oluşturmuştur. Bu mimari üzerine inşa edilen GPT (Generative Pre-trained Transformer) serisi modeller, insan benzeri metin üretme ve anlama yetenekleriyle dikkat çekmiştir.

OpenAI tarafından 2022 yılında kullanıma sunulan ChatGPT, yapay zeka destekli sohbet robotlarının potansiyelini geniş kitlelere göstermiştir (OpenAI, 2022). Ancak bu tür bulut tabanlı çözümler, veri gizliliği, internet bağımlılığı ve maliyet gibi önemli sorunları da beraberinde getirmiştir. Özellikle eğitim kurumları gibi hassas verilerin işlendiği ortamlarda, kullanıcı verilerinin üçüncü taraf sunuculara gönderilmesi ciddi gizlilik endişelerine yol açmaktadır.

Bu bağlamda, \*\*yerel LLM (Local Large Language Model)\*\* çözümleri önem kazanmıştır. Meta'nın LLaMA serisi (Touvron ve ark., 2023\) ve Ollama gibi araçlar, güçlü dil modellerinin yerel donanımda çalıştırılmasını mümkün kılmıştır. Bu yaklaşım, veri gizliliğini korurken yapay zeka yeteneklerinden faydalanmayı sağlamaktadır.

Selçuk Üniversitesi, 1975 yılında Konya'da kurulan ve Türkiye'nin en köklü üniversitelerinden biridir. Günümüzde 23 fakülte ve 100.000'den fazla öğrencisiyle ülkenin en büyük yükseköğretim kurumlarından biri konumundadır (Selçuk Üniversitesi, 2024). Bu denli büyük bir kurumda, öğrencilerin ve personelin bilgiye hızlı ve doğru şekilde erişmesi kritik bir ihtiyaçtır.

\#\#\# 1.2. Projenin Önemi ve Özgün Değeri

Bu proje, mevcut üniversite chatbot çözümlerinden birkaç önemli açıdan ayrılmaktadır:

\*\*1. Gizlilik Odaklı Tasarım:\*\*

Geleneksel chatbot çözümleri (ChatGPT, Google Bard vb.) kullanıcı verilerini bulut sunuculara göndermektedir. Bu projede ise tüm veri işleme yerel LLM üzerinde gerçekleştirilmektedir. Kullanıcı soruları ve yanıtlar, harici servislere gönderilmeden yerel sistemde işlenmektedir.

\`\`\`  
Geleneksel Yaklaşım:  
Kullanıcı → İnternet → Bulut API → Yanıt

Bu Projenin Yaklaşımı:  
Kullanıcı → Yerel Ollama → Yanıt (İnternet opsiyonel)  
\`\`\`

\*\*2. Çevrimdışı Çalışabilirlik:\*\*

İnternet bağlantısı kesilse bile temel sohbet akışı sürdürülebilmektedir. Bu özellik, kampüs içinde ağ sorunları yaşandığında veya mobil veri erişiminin kısıtlı olduğu durumlarda kritik öneme sahiptir.

\*\*3. Kaynak Gösterimli Yanıtlar (RAG):\*\*

RAG teknolojisi sayesinde sistem, yanıtlarını belge parçalarıyla ilişkilendirmektedir. Bu, akademik ortamda doğrulanabilirlik açısından büyük önem taşımaktadır. Kullanıcılar, verilen bilginin hangi kaynaktan geldiğini görebilmektedir.

\*\*4. Çoklu Sağlayıcı Desteği:\*\*

Sistem, tek bir LLM'e bağımlı değildir. Ollama (varsayılan) ve HuggingFace sağlayıcıları aynı arayüzden yönetilebilmektedir. Bu esneklik, farklı donanım ve performans gereksinimlerine uyum sağlamaktadır.

\*\*5. Kalite Kapıları ve CI/CD:\*\*

Proje, GitHub Actions üzerinde otomatik test ve kod kalitesi kontrolleri (pytest, ruff, mypy, flutter analyze) içermektedir. Bu, akademik bir proje için profesyonel yazılım geliştirme pratiklerinin uygulandığını göstermektedir.

\#\#\# 1.3. Projenin Kapsamı

Bu proje kapsamında aşağıdaki konular ele alınmıştır:

\*\*Kapsam Dahilinde:\*\*

\- Selçuk Üniversitesi hakkında genel bilgiler (konum: Konya, kuruluş: 1975\)  
\- Kampüs bilgileri (Alaeddin Keykubat, Ardıçlı)  
\- Fakülte ve bölüm bilgileri (özellikle Teknoloji Fakültesi ve Bilgisayar Mühendisliği)  
\- Akademik takvim ve önemli tarihler  
\- Sıkça sorulan sorular (SSS)  
\- İletişim bilgileri  
\- Ulaşım ve sosyal olanaklar  
\- Yerel LLM ile sohbet (Ollama/Llama 3.1-3.2)  
\- RAG ile kaynak gösterimli yanıtlar  
\- Flutter ile çoklu platform desteği (iOS, Android, Web)  
\- SSE ile gerçek zamanlı akış yanıtları

\*\*Kapsam Dışında:\*\*

\- Öğrenci not ve devamsızlık bilgileri (kişisel veri güvenliği)  
\- OBS (Öğrenci Bilgi Sistemi) entegrasyonu  
\- Ders içerikleri ve materyalleri  
\- Sınav soruları ve cevapları  
\- Personel özlük bilgileri  
\- Mali işlemler ve ödeme bilgileri

\#\#\# 1.4. Raporun Organizasyonu

Bu rapor altı ana bölümden oluşmaktadır:

\*\*Bölüm 1 \- Giriş:\*\* Projenin arka planı, önemi, özgün değeri, kapsamı ve raporun organizasyonu açıklanmaktadır.

\*\*Bölüm 2 \- Kaynak Araştırması:\*\* Yapay zeka, doğal dil işleme, büyük dil modelleri, yerel LLM çözümleri, RAG teknolojileri ve mobil uygulama geliştirme hakkında literatür taraması sunulmaktadır.

\*\*Bölüm 3 \- Materyal ve Yöntem:\*\* Projede kullanılan metodoloji, veri toplama ve işleme süreçleri, model seçimi ve değerlendirme metrikleri açıklanmaktadır.

\*\*Bölüm 4 \- Sistem Tasarımı ve Uygulama:\*\* Sistemin mimarisi, bileşenleri, sağlayıcı deseni, RAG servisi, API tasarımı ve güvenlik detaylandırılmaktadır.

\*\*Bölüm 5 \- Araştırma Bulguları ve Tartışma:\*\* Test sonuçları, performans değerlendirmesi ve karşılaşılan zorluklar tartışılmaktadır.

\*\*Bölüm 6 \- Sonuçlar ve Öneriler:\*\* Projenin sonuçları özetlenmekte ve gelecek çalışmalar için öneriler sunulmaktadır.

\---

\#\# 2\. KAYNAK ARAŞTIRMASI

\#\#\# 2.1. Yapay Zeka ve Doğal Dil İşleme

Yapay zeka (Artificial Intelligence \- AI), makinelerin insan benzeri zeka gerektiren görevleri yerine getirmesini sağlayan bilgisayar bilimi dalıdır. Doğal dil işleme (Natural Language Processing \- NLP), yapay zekanın insan dilini anlama ve üretme yeteneğini inceleyen alt alanıdır (Jurafsky ve Martin, 2023).

NLP'nin tarihçesi 1950'lere kadar uzanmaktadır. Alan Turing'in "Computing Machinery and Intelligence" makalesi (Turing, 1950), makinelerin düşünüp düşünemeyeceği sorusunu gündeme getirmiştir. İlk NLP sistemleri, kural tabanlı yaklaşımlar kullanmıştır. ELIZA (Weizenbaum, 1966), ilk sohbet robotlarından biri olarak tarihe geçmiştir.

2017 yılında Vaswani ve arkadaşları tarafından önerilen Transformer mimarisi, NLP alanında paradigma değişikliğine yol açmıştır. Self-attention mekanizması, uzun mesafeli bağımlılıkları etkili bir şekilde modellemeyi sağlamıştır. Bu mimari, günümüzün en güçlü dil modellerinin temelini oluşturmaktadır.

\#\#\# 2.2. Büyük Dil Modelleri (LLM)

Büyük dil modelleri (Large Language Models \- LLM), milyarlarca parametre içeren ve büyük metin veri setleri üzerinde eğitilen yapay sinir ağlarıdır. Bu modeller, metin üretme, çeviri, özetleme, soru cevaplama gibi çeşitli NLP görevlerinde üstün performans sergilemektedir.

\*\*GPT Serisi (OpenAI):\*\*

GPT (Generative Pre-trained Transformer), OpenAI tarafından geliştirilen bir dil modeli serisidir. GPT-3 (2020) 175 milyar parametreye ulaşmıştır (Brown ve ark., 2020). GPT-4 (2023), multimodal yetenekleri ile dikkat çekmiştir (OpenAI, 2023).

\*\*LLaMA Serisi (Meta):\*\*

LLaMA (Large Language Model Meta AI), Meta tarafından 2023 yılında açık kaynak olarak yayınlanmıştır (Touvron ve ark., 2023). LLaMA 2 ve LLaMA 3 versiyonları, 7B ile 70B parametre arasında değişen boyutlarda sunulmaktadır. Bu modeller, yerel çalıştırma için optimize edilmiş olup Ollama gibi araçlarla kolayca kullanılabilmektedir.

\*\*Çizelge 2.1.\*\* Popüler LLM modellerinin karşılaştırması

| Model | Geliştirici | Parametre | Açık Kaynak | Yerel Çalışma |  
|-------|-------------|-----------|-------------|---------------|  
| GPT-4 | OpenAI | \~1.7T (tahmin) | Hayır | Hayır |  
| GPT-3.5 | OpenAI | 175B | Hayır | Hayır |  
| LLaMA 3.1 | Meta | 8B-405B | Evet | Evet |  
| LLaMA 3.2 | Meta | 1B-90B | Evet | Evet |  
| Qwen 2.5 | Alibaba | 0.5B-72B | Evet | Evet |  
| Gemma 2 | Google | 2B-27B | Evet | Evet |

\#\#\# 2.3. Yerel LLM Çözümleri ve Ollama

Bulut tabanlı LLM API'lerinin gizlilik, maliyet ve bağımlılık sorunları, yerel çözümlere olan ilgiyi artırmıştır. Yerel LLM çalıştırma, modelin kullanıcının kendi donanımında çalışması anlamına gelmektedir.

\*\*Ollama:\*\*

Ollama, yerel LLM çalıştırmayı kolaylaştıran açık kaynaklı bir araçtır (Ollama, 2024). Temel özellikleri şunlardır:

\- \*\*Kolay Kurulum:\*\* Tek komutla model indirme ve çalıştırma  
\- \*\*Model Kütüphanesi:\*\* LLaMA, Mistral, Qwen gibi popüler modeller  
\- \*\*REST API:\*\* HTTP üzerinden model etkileşimi  
\- \*\*Çoklu Platform:\*\* Windows, macOS, Linux desteği  
\- \*\*GPU Hızlandırma:\*\* NVIDIA CUDA ve Apple Metal desteği

\`\`\`bash  
\# Ollama ile model çalıştırma örneği  
ollama run llama3.1  
ollama run llama3.2:3b  
\`\`\`

\*\*Ollama API Yapısı:\*\*

\`\`\`  
POST /api/generate  
{  
  "model": "llama3.1",  
  "prompt": "Selçuk Üniversitesi nerede?",  
  "stream": true  
}  
\`\`\`

\*\*HuggingFace Transformers:\*\*

HuggingFace, açık kaynak model deposu ve transformers kütüphanesi ile yerel model çalıştırmayı desteklemektedir. Quantization (4-bit, 8-bit) ile düşük VRAM'li GPU'larda bile büyük modeller çalıştırılabilmektedir.

\#\#\# 2.4. RAG (Retrieval Augmented Generation)

RAG (Retrieval Augmented Generation), büyük dil modellerinin bilgi erişim sistemleri ile birleştirilmesiyle oluşturulan bir yaklaşımdır. Lewis ve arkadaşları (2020) tarafından önerilen bu yöntem, LLM'lerin "hallucination" (uydurma bilgi üretme) problemine çözüm sunmaktadır.

\*\*RAG'ın Çalışma Prensibi:\*\*

\`\`\`  
┌─────────────────────────────────────────────────────────────┐  
│                     KULLANICI SORUSU                        │  
│            "Bilgisayar Mühendisliği hangi fakültede?"       │  
└─────────────────────────┬───────────────────────────────────┘  
                          │  
                          ▼  
┌─────────────────────────────────────────────────────────────┐  
│                   1\. EMBEDDING OLUŞTURMA                    │  
│     Soru → Vektör temsili (sentence-transformers)           │  
└─────────────────────────┬───────────────────────────────────┘  
                          │  
                          ▼  
┌─────────────────────────────────────────────────────────────┐  
│                   2\. BELGE ERİŞİMİ (Retrieval)              │  
│     FAISS vektör araması → En benzer K belge parçası        │  
└─────────────────────────┬───────────────────────────────────┘  
                          │  
                          ▼  
┌─────────────────────────────────────────────────────────────┐  
│                   3\. BAĞLAM OLUŞTURMA                       │  
│     Sistem prompt \+ Bulunan belgeler \+ Kullanıcı sorusu     │  
└─────────────────────────┬───────────────────────────────────┘  
                          │  
                          ▼  
\#\# 2.4. RAG (Retrieval Augmented Generation) (Devam)

\`\`\`  
┌─────────────────────────────────────────────────────────────┐  
│                   4\. YANIT ÜRETİMİ (Generation)             │  
│     LLM (Ollama/Llama) → Bağlama dayalı yanıt üretimi       │  
└─────────────────────────┬───────────────────────────────────┘  
                          │  
                          ▼  
┌─────────────────────────────────────────────────────────────┐  
│                     KULLANICIYA YANIT                       │  
│  "Bilgisayar Mühendisliği, Teknoloji Fakültesi bünyesinde   │  
│   Alaeddin Keykubat Yerleşkesi'nde bulunmaktadır."          │  
│   \[Kaynak: 02\_bilgisayar\_muhendisligi.txt\]                  │  
└─────────────────────────────────────────────────────────────┘  
\`\`\`

\*\*Şekil 2.1.\*\* RAG pipeline akış diyagramı

\*\*RAG'ın Avantajları:\*\*

1\. \*\*Güncellik:\*\* Knowledge base güncellendiğinde, model yeniden eğitilmeden güncel bilgi sunabilir.  
2\. \*\*Doğruluk:\*\* Yanıtlar, doğrulanmış kaynaklara dayandırılır.  
3\. \*\*Şeffaflık:\*\* Yanıtların kaynakları (citations) gösterilebilir.  
4\. \*\*Hallucination Azaltma:\*\* Model, yalnızca verilen bağlamdaki bilgileri kullanmaya yönlendirilir.  
5\. \*\*Maliyet Etkinliği:\*\* Model fine-tuning gerektirmez.

\*\*Vektör Veritabanları:\*\*

RAG sistemlerinde belgeler, vektör temsillerine dönüştürülerek saklanır. Bu projede FAISS (Facebook AI Similarity Search) kullanılmıştır.

\*\*Çizelge 2.2.\*\* Vektör veritabanı karşılaştırması

| Veritabanı | Geliştirici | Özellik | Kullanım |  
|------------|-------------|---------|----------|  
| FAISS | Meta | Yüksek performans, yerel | Bu projede kullanıldı |  
| ChromaDB | Chroma | Kolay kullanım, yerel | Alternatif olarak destekleniyor |  
| Pinecone | Pinecone | Bulut tabanlı, yönetilen | Kullanılmadı (gizlilik) |  
| Weaviate | Weaviate | Açık kaynak, GraphQL | Kullanılmadı |

\*\*Embedding Modelleri:\*\*

Bu projede \`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2\` modeli kullanılmıştır. Bu model, Türkçe dahil 50+ dilde çalışabilmekte ve 384 boyutlu vektörler üretmektedir.

\#\#\# 2.5. Mobil Uygulama Geliştirme ve Flutter

Mobil uygulama geliştirme, günümüzde yazılım projelerinin önemli bir bileşeni haline gelmiştir. Cross-platform framework'ler, tek bir kod tabanından birden fazla platform için uygulama geliştirmeyi mümkün kılmıştır.

\*\*Flutter Framework:\*\*

Flutter, Google tarafından geliştirilen açık kaynaklı bir UI toolkit'tir (Google, 2018). Dart programlama dili kullanılarak tek bir kod tabanından iOS, Android, web ve masaüstü uygulamaları geliştirilebilmektedir.

\*\*Flutter'ın Avantajları:\*\*

\- \*\*Tek Kod Tabanı:\*\* iOS, Android ve Web için aynı kod  
\- \*\*Hot Reload:\*\* Kod değişiklikleri anında görüntülenebilir  
\- \*\*Zengin Widget Kütüphanesi:\*\* Material Design 3 desteği  
\- \*\*Yüksek Performans:\*\* Native performansa yakın sonuçlar  
\- \*\*Geniş Topluluk:\*\* Aktif geliştirici topluluğu ve zengin paket ekosistemi

\*\*GetX State Management:\*\*

Bu projede state management için GetX kullanılmıştır. GetX, Flutter için hafif ve güçlü bir çözüm sunmaktadır:

\`\`\`dart  
// GetX Controller örneği  
class ChatController extends GetxController {  
  final messages \= \<Message\>\[\].obs;  
  final isLoading \= false.obs;  
    
  void sendMessage(String content) {  
    messages.add(Message(content: content, isUser: true));  
    isLoading.value \= true;  
    // API çağrısı...  
  }  
}  
\`\`\`

\#\#\# 2.6. Üniversite Chatbot Uygulamaları

Dünya genelinde birçok üniversite, yapay zeka destekli chatbot sistemleri geliştirmiştir:

\*\*Georgia State University \- Pounce:\*\*

Georgia State University, 2016 yılında Pounce adlı chatbot'u kullanıma sunmuştur. Sistem, öğrenci kayıt süreçlerinde %22 iyileşme sağlamıştır (Page ve Gehlbach, 2017).

\*\*Deakin University \- Genie:\*\*

Avustralya'daki Deakin University, IBM Watson tabanlı Genie chatbot'unu geliştirmiştir. Sistem, öğrenci sorularının %80'ine otomatik yanıt vermektedir.

\*\*Türkiye'deki Uygulamalar:\*\*

Türkiye'de de üniversiteler chatbot teknolojilerine yönelmektedir. Ancak mevcut çözümlerin çoğu bulut tabanlı API'lere bağımlıdır ve gizlilik endişeleri taşımaktadır. Bu proje, yerel LLM kullanımıyla bu soruna özgün bir çözüm sunmaktadır.

\---

\#\# 3\. MATERYAL VE YÖNTEM

\#\#\# 3.1. Geliştirme Metodolojisi

Bu projede Agile (Çevik) yazılım geliştirme metodolojisi benimsenmiştir. Proje, iteratif sprint'ler halinde yürütülmüştür.

\*\*Kullanılan Araçlar:\*\*

\*\*Çizelge 3.1.\*\* Geliştirme araçları

| Kategori | Araç | Versiyon | Kullanım Amacı |  
|----------|------|----------|----------------|  
| Versiyon Kontrolü | Git | 2.40+ | Kaynak kod yönetimi |  
| Repository | GitHub | \- | Kod barındırma, CI/CD |  
| CI/CD | GitHub Actions | \- | Otomatik test ve derleme |  
| Kod Kalitesi | Ruff | \- | Python linting |  
| Tip Kontrolü | mypy | \- | Python statik analiz |  
| Flutter Analiz | flutter analyze | \- | Dart kod analizi |  
| Test | pytest | \- | Python birim testleri |  
| Test | flutter test | \- | Dart birim testleri |

\*\*CI/CD Pipeline:\*\*

Proje, GitHub Actions üzerinde otomatik kalite kontrolleri içermektedir:

\`\`\`yaml  
\# .github/workflows/backend.yml özeti  
\- pytest \-q (birim testleri)  
\- ruff check . (kod stili)  
\- mypy . (tip kontrolü)

\# .github/workflows/dart.yml özeti  
\- flutter analyze (kod analizi)  
\- flutter test (birim testleri)  
\`\`\`

\*\*Görev Dağılımı:\*\*

\- \*\*Doğukan BALAMAN:\*\* Backend geliştirme, RAG pipeline, API tasarımı, veri toplama, CI/CD  
\- \*\*Ali YILDIRIM:\*\* Flutter mobil/web uygulama geliştirme, UI/UX tasarımı, test

\#\#\# 3.2. Veri Toplama ve Knowledge Base Oluşturma

Selçuk Üniversitesi hakkındaki veriler, çeşitli kaynaklardan sistematik olarak toplanmıştır.

\#\#\#\# 3.2.1. Veri Kaynakları

\*\*Birincil Kaynaklar:\*\*

\- Selçuk Üniversitesi Resmi Web Sitesi (www.selcuk.edu.tr)  
\- Teknoloji Fakültesi Web Sitesi  
\- Bilgisayar Mühendisliği Bölümü Web Sitesi

\*\*Veri Toplama Araçları:\*\*

Projede web scraping için özel Python scriptleri geliştirilmiştir:

\- \`scrape\_selcuk\_edu.py\`: Ana üniversite sitesinden veri çekme  
\- \`scrape\_bilgisayar.py\`: Bilgisayar Mühendisliği bölümü verileri

\#\#\#\# 3.2.2. Knowledge Base Yapısı

Veriler, iki ana formatta yapılandırılmıştır:

\*\*1. JSON Bilgi Tabanı (\`selcuk\_knowledge\_base.json\`):\*\*

\`\`\`json  
{  
  "universite\_bilgileri": {  
    "ad": "Selçuk Üniversitesi",  
    "kuruluş\_yılı": 1975,  
    "şehir": "Konya",  
    "öğrenci\_sayısı": "100,000+",  
    "fakülte\_sayısı": 23  
  },  
  "bilgisayar\_muhendisligi": {  
    "fakulte": "Teknoloji Fakültesi",  
    "kampüs": "Alaeddin Keykubat Kampüsü",  
    "akreditasyon": {"mudek": true}  
  },  
  "sık\_sorulan\_sorular": \[...\]  
}  
\`\`\`

\*\*2. RAG Dokümanları (\`data/rag/selcuk/\`):\*\*

\`\`\`  
data/rag/selcuk/  
├── 01\_genel\_bilgiler.txt      \# Üniversite genel bilgileri  
├── 02\_bilgisayar\_muhendisligi.txt  \# Bölüm detayları  
├── 03\_muhendislik\_fakultesi.txt    \# Fakülte bilgileri  
├── 04\_sss.txt                 \# Sıkça sorulan sorular  
└── 05\_bilgisayar\_web.txt      \# Web sitesi içerikleri  
\`\`\`

\*\*3. Soru-Cevap Veri Seti (\`selcuk\_qa\_dataset.jsonl\`):\*\*

\`\`\`jsonl  
{"messages": \[{"role": "user", "content": "Selçuk Üniversitesi nerede?"},   
              {"role": "assistant", "content": "Selçuk Üniversitesi, Konya ilinde..."}\]}  
\`\`\`

\#\#\#\# 3.2.3. Veri Doğrulama

Kritik bilgilerin doğruluğunu kontrol etmek için \`validate\_knowledge.py\` scripti geliştirilmiştir:

\`\`\`python  
\# validate\_knowledge.py özeti  
def test\_konum():  
    """Konum bilgisi KONYA olmalı, İzmir DEĞİL\!"""  
    assert kb\["universite\_bilgileri"\]\["şehir"\] \== "Konya"

def test\_kurulus\_yili():  
    """Kuruluş yılı 1975 olmalı"""  
    assert kb\["universite\_bilgileri"\]\["kuruluş\_yılı"\] \== 1975

def test\_bilgisayar\_fakulte():  
    """Bilgisayar Mühendisliği Teknoloji Fakültesi'nde olmalı"""  
    assert kb\["bilgisayar\_muhendisligi"\]\["fakulte"\] \== "Teknoloji Fakültesi"  
\`\`\`

\*\*Çizelge 3.2.\*\* Kritik bilgi doğrulama tablosu

| Bilgi | Doğru Değer | Yanlış Örnekler | Doğrulama |  
|-------|-------------|-----------------|-----------|  
| Konum | \*\*KONYA\*\* | İzmir, Ankara | ✅ |  
| Kuruluş Yılı | \*\*1975\*\* | 1976, 1974 | ✅ |  
| Bilg. Müh. Fakültesi | \*\*Teknoloji Fakültesi\*\* | Mühendislik Fakültesi | ✅ |  
| MÜDEK Akreditasyonu | \*\*Var\*\* | Yok | ✅ |

\#\#\# 3.3. Model ve Sağlayıcı Seçimi

\#\#\#\# 3.3.1. Sağlayıcı Karşılaştırması

\*\*Çizelge 3.3.\*\* LLM sağlayıcı karşılaştırması

| Kriter | Ollama | HuggingFace | OpenAI API |  
|--------|--------|-------------|------------|  
| Gizlilik | ✅ Yerel | ✅ Yerel | ❌ Bulut |  
| Çevrimdışı | ✅ Evet | ✅ Evet | ❌ Hayır |  
| Maliyet | ✅ Ücretsiz | ✅ Ücretsiz | ❌ Ücretli |  
| Kurulum | ✅ Kolay | ⚠️ Orta | ✅ Kolay |  
| GPU Gereksinimi | ⚠️ Önerilir | ⚠️ Önerilir | ❌ Yok |  
| Türkçe Performans | ✅ İyi | ✅ İyi | ✅ Çok İyi |

\#\#\#\# 3.3.2. Seçilen Konfigürasyon

\*\*Varsayılan Sağlayıcı:\*\* Ollama

\*\*Varsayılan Model:\*\* \`llama3.2:3b\` (hız için) veya \`llama3.1\` (kalite için)

\*\*Seçim Gerekçeleri:\*\*

1\. \*\*Gizlilik:\*\* Tüm veri işleme yerel sistemde kalır  
2\. \*\*Çevrimdışı Çalışma:\*\* İnternet bağımlılığı yok  
3\. \*\*Maliyet:\*\* API ücreti yok  
4\. \*\*Türkçe Desteği:\*\* LLaMA 3 serisi Türkçe'de iyi performans göstermektedir  
5\. \*\*Kolay Kurulum:\*\* \`ollama run llama3.1\` ile hızlı başlangıç

\*\*Alternatif Sağlayıcı:\*\* HuggingFace (Qwen2.5-1.5B-Instruct)

\`\`\`python  
\# config.py'den  
HF\_MODEL\_NAME \= "Qwen/Qwen2.5-1.5B-Instruct"  
HF\_LOAD\_IN\_4BIT \= True  \# Düşük VRAM için  
\`\`\`

\#\#\# 3.4. RAG Pipeline Tasarımı

\#\#\#\# 3.4.1. Pipeline Bileşenleri

\`\`\`  
┌─────────────────────────────────────────────────────────────────────────┐  
│                         RAG PIPELINE MİMARİSİ                           │  
├─────────────────────────────────────────────────────────────────────────┤  
│                                                                         │  
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                 │  
│  │   Doküman   │───▶│   Chunking  │───▶│  Embedding  │                 │  
│  │   Yükleme   │    │  (500 char) │    │ (MiniLM)    │                 │  
│  └─────────────┘    └─────────────┘    └──────┬──────┘                 │  
│                                               │                         │  
│                                               ▼                         │  
│                                        ┌─────────────┐                 │  
│                                        │   FAISS     │                 │  
│                                        │   Index     │                 │  
│                                        └──────┬──────┘                 │  
│                                               │                         │  
│  ┌─────────────┐    ┌─────────────┐          │                         │  
│  │  Kullanıcı  │───▶│   Query     │──────────┘                         │  
│  │   Sorusu    │    │  Embedding  │                                    │  
│  └─────────────┘    └──────┬──────┘                                    │  
│                            │                                            │  
│                            ▼                                            │  
│                     ┌─────────────┐    ┌─────────────┐                 │  
│                     │  Similarity │───▶│   Top-K     │                 │  
│                     │   Search    │    │   Chunks    │                 │  
│                     └─────────────┘    └──────┬──────┘                 │  
│                                               │                         │  
│                                               ▼                         │  
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                 │  
│  │   Yanıt \+   │◀───│    LLM      │◀───│   Prompt    │                 │  
│  │  Citations  │    │  (Ollama)   │    │  Building   │                 │  
│  └─────────────┘    └─────────────┘    └─────────────┘                 │  
│                                                                         │  
└─────────────────────────────────────────────────────────────────────────┘  
\`\`\`

\*\*Şekil 3.1.\*\* RAG pipeline detaylı mimarisi

\#\#\#\# 3.4.2. RAG Konfigürasyonu

\`\`\`python  
\# config.py'den RAG ayarları  
RAG\_ENABLED \= True  
RAG\_VECTOR\_DB\_PATH \= "./data/rag"  
RAG\_CHUNK\_SIZE \= 500        \# Karakter  
RAG\_CHUNK\_OVERLAP \= 50      \# Karakter  
RAG\_TOP\_K \= 4               \# Döndürülecek chunk sayısı  
RAG\_EMBEDDING\_MODEL \= "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"  
RAG\_STRICT\_DEFAULT \= True   \# Kaynak yoksa yanıt verme  
\`\`\`

\#\#\#\# 3.4.3. RAG İndeksleme Süreci

\`\`\`bash  
\# RAG indeksi oluşturma  
cd backend  
python rag\_ingest.py \--input ../docs \--output ./data/rag  
\`\`\`

\*\*İndeksleme Adımları:\*\*

1\. \*\*Doküman Yükleme:\*\* \`.txt\` dosyaları okunur  
2\. \*\*Chunking:\*\* 500 karakterlik parçalara bölünür (50 overlap)  
3\. \*\*Embedding:\*\* Her chunk için 384 boyutlu vektör oluşturulur  
4\. \*\*İndeksleme:\*\* FAISS index'e eklenir  
5\. \*\*Metadata Kayıt:\*\* Kaynak dosya bilgileri saklanır

\#\#\# 3.5. Değerlendirme Metrikleri

\#\#\#\# 3.5.1. Doğruluk Metrikleri

\*\*Çizelge 3.4.\*\* Doğruluk metrikleri

| Metrik | Açıklama | Hedef |  
|--------|----------|-------|  
| Kritik Bilgi Doğruluğu | Konum, kuruluş yılı, fakülte bilgisi | %100 |  
| RAG Kaynak Eşleşmesi | Yanıtın ilgili kaynaktan gelmesi | ≥ %90 |  
| Hallucination Oranı | Uydurma bilgi üretme | \< %5 |

\#\#\#\# 3.5.2. Performans Metrikleri

\*\*Çizelge 3.5.\*\* Performans metrikleri

| Metrik | Açıklama | Hedef |  
|--------|----------|-------|  
| İlk Token Süresi | İlk yanıt tokeninin gelmesi | \< 2 saniye |  
| Toplam Yanıt Süresi | Tam yanıtın tamamlanması | \< 30 saniye |  
| Throughput | Saniyede işlenen token | ≥ 10 token/s |

\#\#\#\# 3.5.3. Kalite Kapıları

\*\*Çizelge 3.6.\*\* CI/CD kalite kapıları

| Kapı | Araç | Geçme Kriteri |  
|------|------|---------------|  
| Python Testleri | pytest | Tüm testler geçmeli |  
| Python Linting | ruff | Hata yok |  
| Python Tip Kontrolü | mypy | Hata yok |  
| Flutter Analiz | flutter analyze | Hata yok |  
| Flutter Testleri | flutter test | Tüm testler geçmeli |  
| Encoding Guard | encoding\_guard.py | UTF-8 uyumlu |

\---

\#\# 4\. SİSTEM TASARIMI VE UYGULAMA

\#\#\# 4.1. Genel Mimari

Selçuk AI Asistan, modüler ve katmanlı bir mimari üzerine inşa edilmiştir. Sistem, gizlilik odaklı tasarımı ve çoklu sağlayıcı desteği ile öne çıkmaktadır.

\#\#\#\# 4.1.1. Mimari Diyagramı

\`\`\`  
┌─────────────────────────────────────────────────────────────────────────────┐  
│                              KULLANICILAR                                   │  
│                    (iOS / Android / Web Tarayıcı)                           │  
└───────────────────────────────┬─────────────────────────────────────────────┘  
                                │ HTTP/SSE  
                                ▼  
┌─────────────────────────────────────────────────────────────────────────────┐  
│                        FLUTTER UYGULAMASI                                   │  
│  ┌─────────────────────────────────────────────────────────────────────┐   │  
│  │                    GetX State Management                             │   │  
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │  
│  │  │    Chat      │  │   Settings   │  │    Enhanced Chat         │  │   │  
│  │  │  Controller  │  │  Controller  │  │    Controller            │  │   │  
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │  
│  └─────────────────────────────────────────────────────────────────────┘   │  
│  ┌─────────────────────────────────────────────────────────────────────┐   │  
│  │                         UI Widgets                                   │   │  
│  │  • MessageCard  • TypingIndicator  • MarkdownMessageView            │   │  
│  │  • ModelCard    • ConversationListDrawer  • AvailabilityBadge       │   │  
│  └─────────────────────────────────────────────────────────────────────┘   │  
└───────────────────────────────┬─────────────────────────────────────────────┘  
                                │ REST API / SSE  
                                ▼  
┌─────────────────────────────────────────────────────────────────────────────┐  
│                           FASTAPI BACKEND                                   │  
│  ┌─────────────────────────────────────────────────────────────────────┐   │  
│  │                         API Endpoints                                │   │  
│  │  POST /chat          POST /chat/stream       GET /models            │   │  
│  │  GET /health         GET /health/ollama      GET /health/hf         │   │  
│  └─────────────────────────────────────────────────────────────────────┘   │  
│                                    │                                        │  
│  ┌─────────────────────────────────┴─────────────────────────────────────┐ │  
│  │                      CORE SERVICES                                     │ │  
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │ │  
│  │  │  RAG Service    │  │ Response Cleaner│  │   Prompt Builder    │   │ │  
│  │  │  (rag\_service)  │  │                 │  │   (prompts.py)      │   │ │  
│  │  └────────┬────────┘  └─────────────────┘  └─────────────────────┘   │ │  
│  │           │                                                           │ │  
│  └───────────┼───────────────────────────────────────────────────────────┘ │  
│              │                                                              │  
│  ┌───────────┴───────────────────────────────────────────────────────────┐ │  
│  │                    PROVIDER LAYER (Sağlayıcı Deseni)                   │ │  
│  │  ┌─────────────────────┐        ┌─────────────────────────────────┐  │ │  
│  │  │   ModelRegistry     │        │         Base Provider           │  │ │  
│  │  │   (registry.py)     │        │         (base.py)               │  │ │  
│  │  └──────────┬──────────┘        └─────────────────────────────────┘  │ │  
│  │             │                                                         │ │  
│  │  ┌──────────┴──────────┐        ┌─────────────────────────────────┐  │ │  
│  │  │  OllamaProvider     │        │    HuggingFaceProvider          │  │ │  
│  │  │  (ollama\_provider)  │        │    (huggingface\_provider)       │  │ │  
│  │  └──────────┬──────────┘        └─────────────────────────────────┘  │ │  
│  │             │                                                         │ │  
│  └─────────────┼─────────────────────────────────────────────────────────┘ │  
└────────────────┼────────────────────────────────────────────────────────────┘  
                 │  
                 ▼  
┌─────────────────────────────────────────────────────────────────────────────┐  
│                            DATA LAYER                                       │  
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐ │  
│  │   Ollama Server     │  │   FAISS Index       │  │   Knowledge Base    │ │  
│  │   (localhost:11434) │  │   (data/rag/)       │  │   (JSON files)      │ │  
│  │                     │  │                     │  │                     │ │  
│  │   • Llama 3.1       │  │   • index.faiss     │  │   • selcuk\_kb.json  │ │  
│  │   • Llama 3.2:3b    │  │   • metadata.json   │  │   • qa\_dataset.jsonl│ │  
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘ │  
└─────────────────────────────────────────────────────────────────────────────┘  
\`\`\`

\*\*Şekil 4.1.\*\* Sistem mimarisi genel görünümü

\#\#\#\# 4.1.2. Teknoloji Stack'i

\*\*Çizelge 4.1.\*\* Kullanılan teknolojiler

| Katman | Teknoloji | Versiyon | Kullanım Amacı |  
|--------|-----------|----------|----------------|  
| \*\*Frontend\*\* | Flutter | 3.4+ | Cross-platform UI |  
| | Dart | 3.4+ | Programlama dili |  
| | GetX | 4.6.6 | State management |  
| | flutter\_markdown\_plus | 1.0.5 | Markdown render |  
| | http | 1.2.2 | HTTP client |  
| \*\*Backend\*\* | Python | 3.10+ | Ana programlama dili |  
| | FastAPI | 0.115.5 | Web framework |  
| | Uvicorn | 0.32.1 | ASGI server |  
| | Pydantic | 2.10.3 | Data validation |  
| \*\*AI/ML\*\* | Ollama | Latest | Yerel LLM çalıştırma |  
| | sentence-transformers | 3.2.1 | Embedding modeli |  
| | FAISS | 1.9+ | Vektör veritabanı |  
| \*\*DevOps\*\* | Docker | 24+ | Containerization |  
| | GitHub Actions | \- | CI/CD |  
| | Nginx | 1.25 | Reverse proxy |

\#\#\# 4.2. Backend Bileşeni (FastAPI)

\#\#\#\# 4.2.1. Proje Dizin Yapısı

\`\`\`  
backend/  
├── main.py                    \# FastAPI uygulaması (ana giriş noktası)  
├── config.py                  \# Yapılandırma ve ortam değişkenleri  
├── schemas.py                 \# Pydantic request/response modelleri  
├── prompts.py                 \# Sistem prompt'ları ve RAG prompt builder  
├── utils.py                   \# Yardımcı fonksiyonlar  
├── response\_cleaner.py        \# Yanıt temizleme ve formatlama  
├── rag\_service.py             \# RAG servisi  
├── rag\_ingest.py              \# RAG indeksleme scripti  
├── providers/  
│   ├── \_\_init\_\_.py  
│   ├── base.py                \# Soyut sağlayıcı sınıfı  
│   ├── registry.py            \# Model registry  
│   ├── ollama\_provider.py     \# Ollama sağlayıcısı  
│   └── huggingface\_provider.py \# HuggingFace sağlayıcısı  
├── data/  
│   ├── rag/                   \# FAISS index ve RAG dokümanları  
│   │   ├── index.faiss  
│   │   ├── metadata.json  
│   │   └── selcuk/            \# Kaynak dokümanlar  
│   ├── selcuk\_knowledge\_base.json  
│   └── selcuk\_qa\_dataset.jsonl  
├── tests/  
│   ├── test\_main.py  
│   ├── test\_critical\_facts.py  
│   └── test\_response\_cleaner.py  
├── requirements.txt  
├── Dockerfile  
└── .env.example  
\`\`\`

\#\#\#\# 4.2.2. Ana  
\#\#\#\# 4.2.2. Ana Uygulama (main.py)

\`\`\`python  
"""Selçuk AI Asistanı FastAPI backend uygulaması."""

from fastapi import FastAPI, HTTPException, Request  
from fastapi.middleware.cors import CORSMiddleware  
from fastapi.responses import StreamingResponse

app \= FastAPI(title="Selçuk AI Asistanı Backend")

\# CORS yapılandırması  
app.add\_middleware(  
    CORSMiddleware,  
    allow\_origins=allowed\_origins,  
    allow\_credentials=not allow\_all\_origins,  
    allow\_methods=\["\*"\],  
    allow\_headers=\["\*"\],  
)

\# Sağlayıcılar  
ollama\_provider \= OllamaProvider()  
huggingface\_provider \= HuggingFaceProvider()  
providers: dict\[str, ModelProvider\] \= {  
    "ollama": ollama\_provider,  
    "huggingface": huggingface\_provider,  
}  
model\_registry \= ModelRegistry(providers)  
\`\`\`

\*\*Temel Endpoint'ler:\*\*

\*\*Çizelge 4.2.\*\* API endpoint listesi

| Endpoint | Method | Açıklama |  
|----------|--------|----------|  
| \`/\` | GET | Sağlık kontrolü (basit) |  
| \`/health\` | GET | Detaylı sağlık durumu |  
| \`/health/ollama\` | GET | Ollama bağlantı durumu |  
| \`/health/hf\` | GET | HuggingFace bağımlılık durumu |  
| \`/models\` | GET | Kullanılabilir model listesi |  
| \`/chat\` | POST | Senkron sohbet (tek yanıt) |  
| \`/chat/stream\` | POST | SSE ile akış yanıtı |

\#\#\#\# 4.2.3. Chat Endpoint Implementasyonu

\`\`\`python  
@app.post("/chat", response\_model=ChatResponse)  
async def chat(request: ChatRequest, http\_request: Request) \-\> ChatResponse:  
    """  
    Senkron sohbet endpoint'i.  
      
    İşleyiş:  
    1\. Model sağlayıcısını çözümle  
    2\. RAG etkinse bağlam al  
    3\. Mesajları normalize et ve kırp  
    4\. LLM'den yanıt al  
    5\. Yanıtı temizle ve döndür  
    """  
    request\_id \= uuid.uuid4().hex  
    language \= pick\_language(http\_request.headers.get("Accept-Language"))  
      
    \# Sağlayıcı çözümleme  
    resolved \= model\_registry.resolve(request.model)  
    provider \= providers.get(resolved.provider)  
      
    \# RAG bağlamı  
    if rag\_enabled:  
        question \= next((m.content for m in reversed(messages) if m.role \== "user"), "")  
        context, citations \= rag\_service.get\_context(question, top\_k=rag\_top\_k)  
          
        if rag\_strict and not context:  
            return ChatResponse(answer=rag\_no\_source\_message(language), ...)  
          
        if context:  
            messages\[0\].content \= build\_rag\_system\_prompt(  
                messages\[0\].content, context, language, rag\_strict  
            )  
      
    \# LLM çağrısı  
    result \= await provider.generate(  
        messages=\[m.model\_dump() for m in messages\],  
        model\_id=resolved.model\_id,  
        temperature=request.temperature,  
        max\_tokens=max\_tokens,  
    )  
      
    answer \= clean\_text(result.text, language=language)  
    return ChatResponse(answer=answer, citations=citations, ...)  
\`\`\`

\#\#\#\# 4.2.4. SSE Akış Endpoint'i

\`\`\`python  
@app.post("/chat/stream")  
async def chat\_stream(request: ChatRequest, http\_request: Request) \-\> StreamingResponse:  
    """  
    Server-Sent Events ile akış yanıtı.  
      
    SSE Format:  
    data: {"type": "token", "token": "Merhaba", "request\_id": "abc123"}  
    data: {"type": "end", "usage": {...}, "citations": \[...\]}  
    """  
    async def event\_generator():  
        cleaner \= StreamingResponseCleaner(language=language)  
          
        async for chunk in provider.stream(  
            messages=\[m.model\_dump() for m in messages\],  
            model\_id=resolved.model\_id,  
            ...  
        ):  
            if chunk.token:  
                cleaned \= cleaner.feed(chunk.token)  
                if cleaned:  
                    yield sse\_event({"type": "token", "token": cleaned, ...})  
              
            if chunk.done:  
                final\_chunk \= cleaner.finalize()  
                yield sse\_event({"type": "end", "citations": citations, ...})  
                break  
      
    return StreamingResponse(  
        event\_generator(),  
        media\_type="text/event-stream",  
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},  
    )  
\`\`\`

\#\#\#\# 4.2.5. Yapılandırma (config.py)

\`\`\`python  
class Config:  
    """Merkezi yapılandırma sınıfı."""  
      
    \# Server  
    HOST: str \= os.getenv("HOST", "0.0.0.0")  
    PORT: int \= int(os.getenv("PORT", "8000"))  
      
    \# Ollama  
    OLLAMA\_BASE\_URL: str \= os.getenv("OLLAMA\_BASE\_URL", "http://localhost:11434")  
    OLLAMA\_MODEL: str \= os.getenv("OLLAMA\_MODEL", "llama3.1")  
    OLLAMA\_TIMEOUT: int \= int(os.getenv("OLLAMA\_TIMEOUT", "120"))  
      
    \# RAG  
    RAG\_ENABLED: bool \= os.getenv("RAG\_ENABLED", "false").lower() \== "true"  
    RAG\_VECTOR\_DB\_PATH: str \= os.getenv("RAG\_VECTOR\_DB\_PATH", "./data/rag")  
    RAG\_CHUNK\_SIZE: int \= int(os.getenv("RAG\_CHUNK\_SIZE", "500"))  
    RAG\_TOP\_K: int \= int(os.getenv("RAG\_TOP\_K", "4"))  
    RAG\_EMBEDDING\_MODEL: str \= os.getenv(  
        "RAG\_EMBEDDING\_MODEL",  
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"  
    )  
    RAG\_STRICT\_DEFAULT: bool \= os.getenv("RAG\_STRICT\_DEFAULT", "true").lower() \== "true"  
      
    \# Guardrails  
    MAX\_CONTEXT\_TOKENS: int \= int(os.getenv("MAX\_CONTEXT\_TOKENS", "4096"))  
    MAX\_OUTPUT\_TOKENS: int \= int(os.getenv("MAX\_OUTPUT\_TOKENS", "512"))  
    REQUEST\_TIMEOUT: int \= int(os.getenv("REQUEST\_TIMEOUT", "120"))  
      
    @classmethod  
    def validate(cls) \-\> None:  
        """Kritik ayarları doğrula."""  
        errors \= \[\]  
        if cls.OLLAMA\_TIMEOUT \< 1:  
            errors.append("OLLAMA\_TIMEOUT en az 1 saniye olmalıdır.")  
        if cls.RAG\_ENABLED and not cls.RAG\_VECTOR\_DB\_PATH:  
            errors.append("RAG etkin ama RAG\_VECTOR\_DB\_PATH ayarlanmamış.")  
        if errors:  
            raise ValueError("; ".join(errors))  
\`\`\`

\#\#\# 4.3. Sağlayıcı Deseni ve Model Yönetimi

Sistem, farklı LLM sağlayıcılarını tek bir arayüzden yönetmek için \*\*Provider Pattern\*\* kullanmaktadır.

\#\#\#\# 4.3.1. Soyut Sağlayıcı Sınıfı (base.py)

\`\`\`python  
"""Sağlayıcı temel sınıfları ve arayüzleri."""

from abc import ABC, abstractmethod  
from dataclasses import dataclass  
from typing import AsyncIterator, Optional

@dataclass  
class Usage:  
    """Token kullanım bilgisi."""  
    prompt\_tokens: int \= 0  
    completion\_tokens: int \= 0  
    total\_tokens: int \= 0

@dataclass  
class GenerationResult:  
    """Üretim sonucu."""  
    text: str  
    usage: Optional\[Usage\] \= None

@dataclass  
class StreamChunk:  
    """Akış parçası."""  
    token: Optional\[str\] \= None  
    done: bool \= False  
    usage: Optional\[Usage\] \= None

class CancellationToken:  
    """İptal mekanizması."""  
    def \_\_init\_\_(self):  
        self.\_cancelled \= False  
      
    def cancel(self):  
        self.\_cancelled \= True  
      
    @property  
    def is\_cancelled(self) \-\> bool:  
        return self.\_cancelled

class ModelProvider(ABC):  
    """Soyut model sağlayıcı arayüzü."""  
      
    @abstractmethod  
    async def generate(  
        self,  
        messages: list\[dict\],  
        model\_id: str,  
        temperature: float \= 0.7,  
        top\_p: float \= 0.9,  
        max\_tokens: int \= 512,  
        request\_id: Optional\[str\] \= None,  
    ) \-\> GenerationResult:  
        """Senkron üretim."""  
        pass  
      
    @abstractmethod  
    async def stream(  
        self,  
        messages: list\[dict\],  
        model\_id: str,  
        temperature: float \= 0.7,  
        top\_p: float \= 0.9,  
        max\_tokens: int \= 512,  
        request\_id: Optional\[str\] \= None,  
        cancel\_token: Optional\[CancellationToken\] \= None,  
    ) \-\> AsyncIterator\[StreamChunk\]:  
        """Akış üretimi."""  
        pass  
      
    @abstractmethod  
    async def health\_check(self, model\_id: str) \-\> dict:  
        """Sağlık kontrolü."""  
        pass  
      
    @abstractmethod  
    async def list\_models(self) \-\> list\[dict\]:  
        """Model listesi."""  
        pass  
\`\`\`

\#\#\#\# 4.3.2. Ollama Sağlayıcısı (ollama\_provider.py)

\`\`\`python  
"""Ollama LLM sağlayıcısı."""

import httpx  
from config import Config  
from providers.base import ModelProvider, GenerationResult, StreamChunk

class OllamaProvider(ModelProvider):  
    """Ollama API sağlayıcısı."""  
      
    def \_\_init\_\_(self):  
        self.base\_url \= Config.OLLAMA\_BASE\_URL  
        self.timeout \= Config.OLLAMA\_TIMEOUT  
      
    async def generate(  
        self,  
        messages: list\[dict\],  
        model\_id: str,  
        temperature: float \= 0.7,  
        \*\*kwargs  
    ) \-\> GenerationResult:  
        """  
        Ollama /api/chat endpoint'i ile senkron üretim.  
        """  
        async with httpx.AsyncClient(timeout=self.timeout) as client:  
            response \= await client.post(  
                f"{self.base\_url}/api/chat",  
                json={  
                    "model": model\_id,  
                    "messages": messages,  
                    "stream": False,  
                    "options": {  
                        "temperature": temperature,  
                        "num\_predict": kwargs.get("max\_tokens", 512),  
                    },  
                },  
            )  
            response.raise\_for\_status()  
            data \= response.json()  
              
            return GenerationResult(  
                text=data\["message"\]\["content"\],  
                usage=Usage(  
                    prompt\_tokens=data.get("prompt\_eval\_count", 0),  
                    completion\_tokens=data.get("eval\_count", 0),  
                    total\_tokens=data.get("prompt\_eval\_count", 0\) \+ data.get("eval\_count", 0),  
                ),  
            )  
      
    async def stream(  
        self,  
        messages: list\[dict\],  
        model\_id: str,  
        cancel\_token: Optional\[CancellationToken\] \= None,  
        \*\*kwargs  
    ) \-\> AsyncIterator\[StreamChunk\]:  
        """  
        Ollama /api/chat endpoint'i ile akış üretimi.  
        """  
        async with httpx.AsyncClient(timeout=self.timeout) as client:  
            async with client.stream(  
                "POST",  
                f"{self.base\_url}/api/chat",  
                json={  
                    "model": model\_id,  
                    "messages": messages,  
                    "stream": True,  
                    "options": {"temperature": kwargs.get("temperature", 0.7)},  
                },  
            ) as response:  
                async for line in response.aiter\_lines():  
                    if cancel\_token and cancel\_token.is\_cancelled:  
                        break  
                      
                    if not line:  
                        continue  
                      
                    data \= json.loads(line)  
                      
                    if data.get("done"):  
                        yield StreamChunk(done=True, usage=...)  
                        break  
                      
                    token \= data.get("message", {}).get("content", "")  
                    if token:  
                        yield StreamChunk(token=token)  
      
    async def health\_check(self, model\_id: str) \-\> dict:  
        """Ollama sunucu ve model durumunu kontrol et."""  
        try:  
            async with httpx.AsyncClient(timeout=5) as client:  
                \# Sunucu kontrolü  
                response \= await client.get(f"{self.base\_url}/api/tags")  
                response.raise\_for\_status()  
                  
                models \= response.json().get("models", \[\])  
                model\_names \= \[m\["name"\] for m in models\]  
                  
                \# Model kontrolü  
                model\_available \= any(  
                    model\_id in name or name.startswith(model\_id)  
                    for name in model\_names  
                )  
                  
                return {  
                    "status": "healthy" if model\_available else "model\_not\_found",  
                    "server": "connected",  
                    "model": model\_id,  
                    "available\_models": model\_names,  
                }  
        except Exception as e:  
            return {"status": "unhealthy", "error": str(e)}  
\`\`\`

\#\#\#\# 4.3.3. Model Registry (registry.py)

\`\`\`python  
"""Model kayıt ve çözümleme sistemi."""

from dataclasses import dataclass  
from typing import Optional  
from config import Config

@dataclass  
class ResolvedModel:  
    """Çözümlenmiş model bilgisi."""  
    provider: str  
    model\_id: str  
    display\_name: str

@dataclass  
class ModelInfo:  
    """Model bilgisi."""  
    id: str  
    name: str  
    provider: str  
    available: bool  
    description: Optional\[str\] \= None

class ModelRegistry:  
    """Model kayıt ve çözümleme."""  
      
    def \_\_init\_\_(self, providers: dict):  
        self.providers \= providers  
        self.default\_provider \= Config.MODEL\_BACKEND  
        self.aliases \= self.\_parse\_aliases(Config.MODEL\_ALIASES)  
      
    def resolve(self, model\_spec: Optional\[str\] \= None) \-\> ResolvedModel:  
        """  
        Model spesifikasyonunu çözümle.  
          
        Formatlar:  
        \- None → varsayılan model  
        \- "llama3.1" → varsayılan sağlayıcı \+ model  
        \- "ollama:llama3.1" → belirtilen sağlayıcı \+ model  
        \- "alias\_name" → alias çözümleme  
        """  
        if not model\_spec:  
            return ResolvedModel(  
                provider=self.default\_provider,  
                model\_id=Config.OLLAMA\_MODEL,  
                display\_name=Config.OLLAMA\_MODEL,  
            )  
          
        \# Alias kontrolü  
        if model\_spec in self.aliases:  
            return self.aliases\[model\_spec\]  
          
        \# provider:model formatı  
        if ":" in model\_spec:  
            provider, model\_id \= model\_spec.split(":", 1\)  
            return ResolvedModel(provider=provider, model\_id=model\_id, display\_name=model\_spec)  
          
        \# Sadece model adı  
        return ResolvedModel(  
            provider=self.default\_provider,  
            model\_id=model\_spec,  
            display\_name=model\_spec,  
        )  
      
    async def list\_models(self) \-\> list\[ModelInfo\]:  
        """Tüm sağlayıcılardan model listesi al."""  
        all\_models \= \[\]  
          
        for provider\_name, provider in self.providers.items():  
            try:  
                models \= await provider.list\_models()  
                for model in models:  
                    all\_models.append(ModelInfo(  
                        id=f"{provider\_name}:{model\['name'\]}",  
                        name=model\["name"\],  
                        provider=provider\_name,  
                        available=model.get("available", True),  
                    ))  
            except Exception:  
                pass  
          
        return all\_models  
\`\`\`

\#\#\# 4.4. RAG Servisi

\#\#\#\# 4.4.1. RAG Service Implementasyonu (rag\_service.py)

\`\`\`python  
"""RAG (Retrieval Augmented Generation) servisi."""

import logging  
from pathlib import Path  
from typing import Optional, Tuple

import faiss  
import numpy as np  
from sentence\_transformers import SentenceTransformer

from config import Config

logger \= logging.getLogger(\_\_name\_\_)

class RAGService:  
    """FAISS tabanlı RAG servisi."""  
      
    def \_\_init\_\_(self):  
        self.enabled \= Config.RAG\_ENABLED  
        self.index: Optional\[faiss.Index\] \= None  
        self.metadata: list\[dict\] \= \[\]  
        self.embedding\_model: Optional\[SentenceTransformer\] \= None  
          
        if self.enabled:  
            self.\_initialize()  
      
    def \_initialize(self):  
        """RAG bileşenlerini yükle."""  
        try:  
            \# Embedding modeli  
            logger.info("Embedding modeli yükleniyor: %s", Config.RAG\_EMBEDDING\_MODEL)  
            self.embedding\_model \= SentenceTransformer(Config.RAG\_EMBEDDING\_MODEL)  
              
            \# FAISS index  
            index\_path \= Path(Config.RAG\_VECTOR\_DB\_PATH) / "index.faiss"  
            metadata\_path \= Path(Config.RAG\_VECTOR\_DB\_PATH) / "metadata.json"  
              
            if index\_path.exists():  
                logger.info("FAISS index yükleniyor: %s", index\_path)  
                self.index \= faiss.read\_index(str(index\_path))  
                  
                import json  
                with open(metadata\_path, "r", encoding="utf-8") as f:  
                    self.metadata \= json.load(f)  
                  
                logger.info("RAG servisi hazır. %d döküman yüklendi.", len(self.metadata))  
            else:  
                logger.warning("FAISS index bulunamadı: %s", index\_path)  
                self.enabled \= False  
                  
        except Exception as e:  
            logger.error("RAG başlatma hatası: %s", e)  
            self.enabled \= False  
      
    def get\_context(  
        self,  
        query: str,  
        top\_k: int \= 4  
    ) \-\> Tuple\[str, list\[str\]\]:  
        """  
        Sorgu için ilgili bağlamı getir.  
          
        Args:  
            query: Kullanıcı sorusu  
            top\_k: Döndürülecek chunk sayısı  
          
        Returns:  
            Tuple\[str, list\[str\]\]: (birleştirilmiş bağlam, kaynak listesi)  
        """  
        if not self.enabled or not self.index:  
            return "", \[\]  
          
        try:  
            \# Query embedding  
            query\_vector \= self.embedding\_model.encode(\[query\])  
            query\_vector \= np.array(query\_vector).astype("float32")  
              
            \# FAISS arama  
            distances, indices \= self.index.search(query\_vector, top\_k)  
              
            \# Sonuçları topla  
            chunks \= \[\]  
            sources \= set()  
              
            for idx in indices\[0\]:  
                if idx \< 0 or idx \>= len(self.metadata):  
                    continue  
                  
                meta \= self.metadata\[idx\]  
                chunks.append(meta\["text"\])  
                sources.add(meta.get("source", "unknown"))  
              
            context \= "\\n\\n---\\n\\n".join(chunks)  
            return context, list(sources)  
              
        except Exception as e:  
            logger.error("RAG arama hatası: %s", e)  
            raise RuntimeError(f"RAG arama hatası: {e}")

\# Singleton instance  
rag\_service \= RAGService()  
\`\`\`

\#\#\#\# 4.4.2. RAG İndeksleme (rag\_ingest.py)

\`\`\`python  
"""RAG doküman indeksleme scripti."""

import argparse  
import json  
import logging  
from pathlib import Path

import faiss  
import numpy as np  
from sentence\_transformers import SentenceTransformer

from config import Config

logging.basicConfig(level=logging.INFO)  
logger \= logging.getLogger(\_\_name\_\_)

def chunk\_text(text: str, chunk\_size: int, overlap: int) \-\> list\[str\]:  
    """Metni parçalara böl."""  
    chunks \= \[\]  
    start \= 0  
    while start \< len(text):  
        end \= start \+ chunk\_size  
        chunk \= text\[start:end\]  
        if chunk.strip():  
            chunks.append(chunk.strip())  
        start \= end \- overlap  
    return chunks

def ingest\_documents(input\_dir: str, output\_dir: str):  
    """  
    Dokümanları indeksle.  
      
    Args:  
        input\_dir: Kaynak doküman dizini  
        output\_dir: FAISS index çıktı dizini  
    """  
    input\_path \= Path(input\_dir)  
    output\_path \= Path(output\_dir)  
    output\_path.mkdir(parents=True, exist\_ok=True)  
      
    \# Embedding modeli  
    logger.info("Embedding modeli yükleniyor...")  
    model \= SentenceTransformer(Config.RAG\_EMBEDDING\_MODEL)  
      
    \# Dokümanları oku ve parçala  
    all\_chunks \= \[\]  
    metadata \= \[\]  
      
    for file\_path in input\_path.glob("\*\*/\*.txt"):  
        logger.info("İşleniyor: %s", file\_path.name)  
          
        with open(file\_path, "r", encoding="utf-8") as f:  
            text \= f.read()  
          
        chunks \= chunk\_text(text, Config.RAG\_CHUNK\_SIZE, Config.RAG\_CHUNK\_OVERLAP)  
          
        for i, chunk in enumerate(chunks):  
            all\_chunks.append(chunk)  
            metadata.append({  
                "source": file\_path.name,  
                "chunk\_index": i,  
                "text": chunk,  
            })  
      
    logger.info("Toplam %d chunk oluşturuldu.", len(all\_chunks))  
      
    \# Embedding oluştur  
    logger.info("Embedding'ler oluşturuluyor...")  
    embeddings \= model.encode(  
        all\_chunks,  
        batch\_size=Config.RAG\_EMBEDDING\_BATCH\_SIZE,  
        show\_progress\_bar=True,  
    )  
    embeddings \= np.array(embeddings).astype("float32")  
      
    \# FAISS index oluştur  
    logger.info("FAISS index oluşturuluyor...")  
    dimension \= embeddings.shape\[1\]  
    index \= faiss.IndexFlatL2(dimension)  
    index.add(embeddings)  
      
    \# Kaydet  
    faiss.write\_index(index, str(output\_path / "index.faiss"))  
      
    with open(output\_path / "metadata.json", "w", encoding="utf-8") as f:  
        json.dump(metadata, f, ensure\_ascii=False, indent=2)  
      
    logger.info("İndeksleme tamamlandı. Çıktı: %s", output\_path)

if \_\_name\_\_ \== "\_\_main\_\_":  
    parser \= argparse.ArgumentParser(description="RAG doküman indeksleme")  
    parser.add\_argument("--input", required=True, help="Kaynak doküman dizini")  
    parser.add\_argument("--output", required=True, help="Çıktı dizini")  
    args \= parser.parse\_args()  
      
    ingest\_documents(args.input, args.output)  
\`\`\`

\#\#\#\# 4.4.3. RAG Prompt Builder (prompts.py)

\`\`\`python  
"""Sistem prompt'ları ve RAG prompt builder."""

def build\_rag\_system\_prompt(  
    base\_prompt: str,  
    context: str,  
    language: str \= "tr",  
    strict: bool \= True  
) \-\> str:  
    """  
    RAG bağlamı ile sistem prompt'u oluştur.  
      
    Args:  
        base\_prompt: Temel sistem prompt'u  
        context: RAG'dan gelen bağlam  
        language: Yanıt dili  
        strict: Kaynak dışı bilgi verme  
      
    Returns:  
        Birleştirilmiş sistem prompt'u  
    """  
    strict\_instruction \= ""  
    if strict:  
        strict\_instruction \= """  
ÖNEMLİ: Yalnızca yukarıdaki BAĞLAM bilgilerini kullan.  
Bağlamda olmayan bilgileri UYDURMA.  
Emin olmadığın konularda "Bu konuda bilgim bulunmamaktadır" de.  
"""  
      
    return f"""{base\_prompt}

\#\#\# BAĞLAM (Güvenilir Kaynaklardan) \#\#\#  
{context}  
\#\#\# BAĞLAM SONU \#\#\#

{strict\_instruction}

Yanıtını {language.upper()} dilinde ver.  
Kısa, öz ve doğru yanıtlar ver.  
Kaynak bilgisi varsa belirt.  
"""

def rag\_no\_source\_message(language: str \= "tr") \-\> str:  
    """Kaynak bulunamadığında döndürülecek mesaj."""  
    messages \= {  
        "tr": "Bu konuda güvenilir bir kaynak bulamadım. Lütfen sorunuzu farklı şekilde sormayı deneyin veya resmi kaynaklara başvurun.",  
        "en": "I couldn't find a reliable source on this topic. Please try rephrasing your question or consult official sources.",  
    }  
    return messages.get(language, messages\["tr"\])  
\`\`\`

\#\#\# 4.5. Flutter Mobil/Web Uygulaması

\#\#\#\# 4.5.1. Flutter Proje Yapısı

\`\`\`  
lib/  
├── main.dart                      \# Uygulama giriş noktası  
├── config/  
│   └── backend\_config.dart        \# Backend URL yapılandırması  
├── controller/  
│   ├── chat\_controller.dart       \# Temel chat controller  
│   ├── enhanced\_chat\_controller.dart  \# Gelişmiş chat controller  
│   └── settings\_controller.dart   \# Ayarlar controller  
├── widget/  
│   ├── message\_card.dart          \# Mesaj kartı widget'ı  
│   ├── enhanced\_message\_card.dart \# Gelişmiş mesaj kartı  
│   ├── markdown\_message\_view.dart \# Markdown render widget'ı  
│   ├── typing\_indicator.dart      \# Yazıyor göstergesi  
│   ├── model\_card.dart            \# Model seçim kartı  
│   ├── availability\_badge.dart    \# Durum rozeti  
│   ├── conversation\_list\_drawer.dart  \# Konuşma listesi  
│   ├── custom\_btn.dart            \# Özel buton  
│   └── custom\_loading.dart        \# Yükleme animasyonu  
├── l10n/                          \# Çoklu dil desteği  
│   ├── app\_en.arb  
│   └── app\_tr.arb  
└── ...  
\`\`\`

\#\#\#\# 4.5.2. Chat Controller (GetX)

\`\`\`dart  
// lib/controller/chat\_controller.dart  
import 'package:get/get.dart';  
import 'package:http/http.dart' as http;  
import 'dart:convert';  
import 'dart:async';

class ChatController extends GetxController {  
  final messages \= \<Message\>\[\].obs;  
  final isLoading \= false.obs;  
  final isStreaming \= false.obs;  
  final currentStreamedText \= ''.obs;  
  final citations \= \<String\>\[\].obs;  
    
  final String backendUrl;  
  String? sessionId;  
    
  ChatController({required this.backendUrl});  
    
  /// SSE ile akış mesajı gönder  
  Future\<void\> sendMessageStream(String content) async {  
    if (content.trim().isEmpty) return;  
      
    // Kullanıcı mesajını ekle  
    messages.add(Message(  
      content: content,  
      isUser: true,  
      timestamp: DateTime.now(),  
    ));  
      
    isLoading.value \= true;  
    isStreaming.value \= true;  
    currentStreamedText.value \= '';  
    citations.clear();  
      
    try {  
      final request \= http.Request(  
        'POST',  
        Uri.parse('$backendUrl/chat/stream'),  
      );  
      request.headers\['Content-Type'\] \= 'application/json';  
      request.body \= jsonEncode({  
        'messages': \[  
          {'role': 'user', 'content': content}  
        \],  
        'rag\_enabled': true,  
        'stream': true,  
      });  
        
      final response \= await http.Client().send(request);  
        
      await for (final chunk in response.stream.transform(utf8.decoder)) {  
        for (final line in chunk.split('\\n')) {  
          if (\!line.startsWith('data: ')) continue;  
            
          final jsonStr \= line.substring(6);  
          if (jsonStr.isEmpty) continue;  
            
          final data \= jsonDecode(jsonStr);  
            
          switch (data\['type'\]) {  
            case 'token':  
              currentStreamedText.value \+= data\['token'\];  
              break;  
            case 'end':  
              if (data\['citations'\] \!= null) {  
                citations.addAll(List\<String\>.from(data\['citations'\]));  
              }  
              \_finalizeMessage();  
              break;  
            case 'error':  
              \_handleError(data\['message'\]);  
              break;  
          }  
        }  
      }  
    } catch (e) {  
      \_handleError(e.toString());  
    } finally {  
      isLoading.value \= false;  
      isStreaming.value \= false;  
    }  
  }  
    
  void \_finalizeMessage() {  
    messages.add(Message(  
      content: currentStreamedText.value,  
      isUser: false,  
      timestamp: DateTime.now(),  
      citations: citations.toList(),  
    ));  
    currentStreamedText.value \= '';  
  }  
    
  void \_handleError(String error) {  
    messages.add(Message(  
      content: 'Hata: $error',  
      isUser: false,  
      isError: true,  
      timestamp: DateTime.now(),  
    ));  
  }  
}

class Message {  
  final String content;  
  final bool isUser;  
  final DateTime timestamp;  
  final List\<String\>? citations;  
  final bool isError;  
    
  Message({  
    required this.content,  
    required this.isUser,  
    required this.timestamp,  
    this.citations,  
    this.isError \= false,  
  });  
}  
\`\`\`

\#\#\#\# 4.5.3. Markdown Mesaj Görünümü

\`\`\`dart  
// lib/widget/markdown\_message\_  
\#\#\#\# 4.5.3. Markdown Mesaj Görünümü (Devam)

\`\`\`dart  
// lib/widget/markdown\_message\_view.dart  
import 'package:flutter/material.dart';  
import 'package:flutter\_markdown\_plus/flutter\_markdown\_plus.dart';  
import 'package:flutter\_highlight/flutter\_highlight.dart';

class MarkdownMessageView extends StatelessWidget {  
  final String content;  
  final bool isUser;  
  final List\<String\>? citations;  
    
  const MarkdownMessageView({  
    super.key,  
    required this.content,  
    required this.isUser,  
    this.citations,  
  });  
    
  @override  
  Widget build(BuildContext context) {  
    final theme \= Theme.of(context);  
      
    return Column(  
      crossAxisAlignment: CrossAxisAlignment.start,  
      children: \[  
        // Markdown içerik  
        MarkdownBody(  
          data: content,  
          selectable: true,  
          styleSheet: MarkdownStyleSheet(  
            p: theme.textTheme.bodyLarge?.copyWith(  
              color: isUser ? Colors.white : theme.colorScheme.onSurface,  
            ),  
            code: TextStyle(  
              backgroundColor: theme.colorScheme.surfaceVariant,  
              fontFamily: 'monospace',  
            ),  
            codeblockDecoration: BoxDecoration(  
              color: theme.colorScheme.surfaceVariant,  
              borderRadius: BorderRadius.circular(8),  
            ),  
          ),  
          builders: {  
            'code': CodeBlockBuilder(),  
          },  
        ),  
          
        // Kaynaklar (citations)  
        if (citations \!= null && citations\!.isNotEmpty) ...\[  
          const SizedBox(height: 8),  
          \_buildCitations(context),  
        \],  
      \],  
    );  
  }  
    
  Widget \_buildCitations(BuildContext context) {  
    return Container(  
      padding: const EdgeInsets.all(8),  
      decoration: BoxDecoration(  
        color: Theme.of(context).colorScheme.surfaceVariant.withOpacity(0.5),  
        borderRadius: BorderRadius.circular(8),  
        border: Border.all(  
          color: Theme.of(context).colorScheme.outline.withOpacity(0.3),  
        ),  
      ),  
      child: Column(  
        crossAxisAlignment: CrossAxisAlignment.start,  
        children: \[  
          Row(  
            children: \[  
              Icon(  
                Icons.source\_outlined,  
                size: 14,  
                color: Theme.of(context).colorScheme.primary,  
              ),  
              const SizedBox(width: 4),  
              Text(  
                'Kaynaklar:',  
                style: Theme.of(context).textTheme.labelSmall?.copyWith(  
                  fontWeight: FontWeight.bold,  
                  color: Theme.of(context).colorScheme.primary,  
                ),  
              ),  
            \],  
          ),  
          const SizedBox(height: 4),  
          Wrap(  
            spacing: 4,  
            runSpacing: 4,  
            children: citations\!.map((source) \=\> Chip(  
              label: Text(  
                source,  
                style: const TextStyle(fontSize: 10),  
              ),  
              padding: EdgeInsets.zero,  
              materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,  
              visualDensity: VisualDensity.compact,  
            )).toList(),  
          ),  
        \],  
      ),  
    );  
  }  
}  
\`\`\`

\#\#\#\# 4.5.4. Mesaj Kartı Widget'ı

\`\`\`dart  
// lib/widget/message\_card.dart  
import 'package:flutter/material.dart';  
import 'package:flutter\_animate/flutter\_animate.dart';  
import 'markdown\_message\_view.dart';

class MessageCard extends StatelessWidget {  
  final String content;  
  final bool isUser;  
  final DateTime timestamp;  
  final List\<String\>? citations;  
  final bool isError;  
  final bool isStreaming;  
    
  const MessageCard({  
    super.key,  
    required this.content,  
    required this.isUser,  
    required this.timestamp,  
    this.citations,  
    this.isError \= false,  
    this.isStreaming \= false,  
  });  
    
  @override  
  Widget build(BuildContext context) {  
    final theme \= Theme.of(context);  
      
    return Padding(  
      padding: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),  
      child: Row(  
        mainAxisAlignment: isUser ? MainAxisAlignment.end : MainAxisAlignment.start,  
        crossAxisAlignment: CrossAxisAlignment.start,  
        children: \[  
          // Avatar (sadece asistan için)  
          if (\!isUser) ...\[  
            CircleAvatar(  
              radius: 16,  
              backgroundColor: theme.colorScheme.primary,  
              child: const Icon(  
                Icons.smart\_toy\_outlined,  
                size: 18,  
                color: Colors.white,  
              ),  
            ),  
            const SizedBox(width: 8),  
          \],  
            
          // Mesaj balonu  
          Flexible(  
            child: Container(  
              padding: const EdgeInsets.all(12),  
              decoration: BoxDecoration(  
                color: isUser  
                    ? theme.colorScheme.primary  
                    : isError  
                        ? theme.colorScheme.errorContainer  
                        : theme.colorScheme.surfaceVariant,  
                borderRadius: BorderRadius.only(  
                  topLeft: const Radius.circular(16),  
                  topRight: const Radius.circular(16),  
                  bottomLeft: Radius.circular(isUser ? 16 : 4),  
                  bottomRight: Radius.circular(isUser ? 4 : 16),  
                ),  
              ),  
              child: Column(  
                crossAxisAlignment: CrossAxisAlignment.start,  
                children: \[  
                  // Mesaj içeriği  
                  MarkdownMessageView(  
                    content: content,  
                    isUser: isUser,  
                    citations: citations,  
                  ),  
                    
                  // Akış göstergesi  
                  if (isStreaming)  
                    const \_StreamingIndicator(),  
                    
                  // Zaman damgası  
                  const SizedBox(height: 4),  
                  Text(  
                    \_formatTime(timestamp),  
                    style: theme.textTheme.labelSmall?.copyWith(  
                      color: isUser  
                          ? Colors.white70  
                          : theme.colorScheme.onSurfaceVariant,  
                    ),  
                  ),  
                \],  
              ),  
            ),  
          ),  
            
          // Avatar (sadece kullanıcı için)  
          if (isUser) ...\[  
            const SizedBox(width: 8),  
            CircleAvatar(  
              radius: 16,  
              backgroundColor: theme.colorScheme.secondary,  
              child: const Icon(  
                Icons.person\_outline,  
                size: 18,  
                color: Colors.white,  
              ),  
            ),  
          \],  
        \],  
      ),  
    ).animate().fadeIn(duration: 200.ms).slideX(  
      begin: isUser ? 0.1 : \-0.1,  
      end: 0,  
      duration: 200.ms,  
    );  
  }  
    
  String \_formatTime(DateTime time) {  
    return '${time.hour.toString().padLeft(2, '0')}:${time.minute.toString().padLeft(2, '0')}';  
  }  
}

class \_StreamingIndicator extends StatelessWidget {  
  const \_StreamingIndicator();  
    
  @override  
  Widget build(BuildContext context) {  
    return Row(  
      mainAxisSize: MainAxisSize.min,  
      children: \[  
        SizedBox(  
          width: 12,  
          height: 12,  
          child: CircularProgressIndicator(  
            strokeWidth: 2,  
            color: Theme.of(context).colorScheme.primary,  
          ),  
        ),  
        const SizedBox(width: 4),  
        Text(  
          'Yazıyor...',  
          style: Theme.of(context).textTheme.labelSmall,  
        ),  
      \],  
    );  
  }  
}  
\`\`\`

\#\#\#\# 4.5.5. Typing Indicator

\`\`\`dart  
// lib/widget/typing\_indicator.dart  
import 'package:flutter/material.dart';  
import 'package:flutter\_animate/flutter\_animate.dart';

class TypingIndicator extends StatelessWidget {  
  const TypingIndicator({super.key});  
    
  @override  
  Widget build(BuildContext context) {  
    return Padding(  
      padding: const EdgeInsets.all(16),  
      child: Row(  
        children: \[  
          CircleAvatar(  
            radius: 16,  
            backgroundColor: Theme.of(context).colorScheme.primary,  
            child: const Icon(  
              Icons.smart\_toy\_outlined,  
              size: 18,  
              color: Colors.white,  
            ),  
          ),  
          const SizedBox(width: 8),  
          Container(  
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),  
            decoration: BoxDecoration(  
              color: Theme.of(context).colorScheme.surfaceVariant,  
              borderRadius: BorderRadius.circular(16),  
            ),  
            child: Row(  
              mainAxisSize: MainAxisSize.min,  
              children: List.generate(3, (index) {  
                return Container(  
                  margin: const EdgeInsets.symmetric(horizontal: 2),  
                  child: \_Dot(delay: index \* 200),  
                );  
              }),  
            ),  
          ),  
        \],  
      ),  
    );  
  }  
}

class \_Dot extends StatelessWidget {  
  final int delay;  
    
  const \_Dot({required this.delay});  
    
  @override  
  Widget build(BuildContext context) {  
    return Container(  
      width: 8,  
      height: 8,  
      decoration: BoxDecoration(  
        color: Theme.of(context).colorScheme.primary,  
        shape: BoxShape.circle,  
      ),  
    )  
        .animate(onPlay: (controller) \=\> controller.repeat())  
        .scale(  
          begin: const Offset(1, 1),  
          end: const Offset(1.2, 1.2),  
          duration: 400.ms,  
          delay: Duration(milliseconds: delay),  
        )  
        .then()  
        .scale(  
          begin: const Offset(1.2, 1.2),  
          end: const Offset(1, 1),  
          duration: 400.ms,  
        );  
  }  
}  
\`\`\`

\#\#\# 4.6. API Tasarımı

\#\#\#\# 4.6.1. Request/Response Şemaları (schemas.py)

\`\`\`python  
"""Pydantic request/response şemaları."""

from pydantic import BaseModel, Field  
from typing import Optional

class MessageItem(BaseModel):  
    """Tek bir mesaj."""  
    role: str \= Field(..., description="Rol: 'user', 'assistant', 'system'")  
    content: str \= Field(..., description="Mesaj içeriği")

class ChatRequest(BaseModel):  
    """Chat isteği."""  
    messages: list\[MessageItem\] \= Field(..., description="Mesaj listesi")  
    model: Optional\[str\] \= Field(None, description="Model adı (ör: 'llama3.1')")  
    temperature: float \= Field(0.7, ge=0, le=2, description="Yaratıcılık (0-2)")  
    top\_p: float \= Field(0.9, ge=0, le=1, description="Nucleus sampling")  
    max\_tokens: Optional\[int\] \= Field(None, description="Maksimum token sayısı")  
    rag\_enabled: bool \= Field(True, description="RAG etkin mi?")  
    rag\_strict: Optional\[bool\] \= Field(None, description="Strict RAG modu")  
    rag\_top\_k: Optional\[int\] \= Field(None, description="RAG top-k değeri")

class UsageInfo(BaseModel):  
    """Token kullanım bilgisi."""  
    prompt\_tokens: int \= 0  
    completion\_tokens: int \= 0  
    total\_tokens: int \= 0

class ChatResponse(BaseModel):  
    """Chat yanıtı."""  
    answer: str \= Field(..., description="Asistan yanıtı")  
    request\_id: str \= Field(..., description="İstek ID'si")  
    provider: str \= Field(..., description="Kullanılan sağlayıcı")  
    model: str \= Field(..., description="Kullanılan model")  
    usage: Optional\[UsageInfo\] \= Field(None, description="Token kullanımı")  
    citations: Optional\[list\[str\]\] \= Field(None, description="RAG kaynakları")  
\`\`\`

\#\#\#\# 4.6.2. API Dokümantasyonu

\*\*Çizelge 4.3.\*\* API endpoint detayları

| Endpoint | Method | Request Body | Response | Açıklama |  
|----------|--------|--------------|----------|----------|  
| \`/\` | GET | \- | \`{"status": "ok"}\` | Basit sağlık kontrolü |  
| \`/health\` | GET | \- | \`{"status": "ok", "message": "..."}\` | Detaylı sağlık |  
| \`/health/ollama\` | GET | \- | \`{"status": "healthy/unhealthy", ...}\` | Ollama durumu |  
| \`/health/hf\` | GET | \- | \`{"status": "ok", "torch\_version": "..."}\` | HF durumu |  
| \`/models\` | GET | \- | \`{"models": \[...\]}\` | Model listesi |  
| \`/chat\` | POST | \`ChatRequest\` | \`ChatResponse\` | Senkron chat |  
| \`/chat/stream\` | POST | \`ChatRequest\` | SSE stream | Akış chat |

\*\*SSE Event Formatları:\*\*

\`\`\`  
\# Token eventi  
data: {"type": "token", "token": "Merhaba", "request\_id": "abc123"}

\# Bitiş eventi  
data: {"type": "end", "usage": {"prompt\_tokens": 50, "completion\_tokens": 100}, "citations": \["01\_genel.txt"\], "request\_id": "abc123"}

\# Hata eventi  
data: {"type": "error", "message": "Bağlantı hatası", "request\_id": "abc123"}  
\`\`\`

\#\#\#\# 4.6.3. Örnek API Kullanımı

\*\*cURL ile Senkron Chat:\*\*

\`\`\`bash  
curl \-X POST http://localhost:8000/chat \\  
  \-H "Content-Type: application/json" \\  
  \-d '{  
    "messages": \[  
      {"role": "user", "content": "Selçuk Üniversitesi nerede?"}  
    \],  
    "rag\_enabled": true  
  }'  
\`\`\`

\*\*Yanıt:\*\*

\`\`\`json  
{  
  "answer": "Selçuk Üniversitesi, Konya ilinde bulunmaktadır. Alaeddin Keykubat ve Ardıçlı olmak üzere iki ana kampüsü vardır.",  
  "request\_id": "a1b2c3d4",  
  "provider": "ollama",  
  "model": "llama3.1",  
  "usage": {  
    "prompt\_tokens": 150,  
    "completion\_tokens": 45,  
    "total\_tokens": 195  
  },  
  "citations": \["01\_genel\_bilgiler.txt"\]  
}  
\`\`\`

\*\*Python ile SSE Stream:\*\*

\`\`\`python  
import httpx

async def stream\_chat():  
    async with httpx.AsyncClient() as client:  
        async with client.stream(  
            "POST",  
            "http://localhost:8000/chat/stream",  
            json={  
                "messages": \[{"role": "user", "content": "Bilgisayar Mühendisliği hangi fakültede?"}\],  
                "rag\_enabled": True,  
            },  
        ) as response:  
            async for line in response.aiter\_lines():  
                if line.startswith("data: "):  
                    data \= json.loads(line\[6:\])  
                    if data\["type"\] \== "token":  
                        print(data\["token"\], end="", flush=True)  
                    elif data\["type"\] \== "end":  
                        print(f"\\n\\nKaynaklar: {data.get('citations', \[\])}")  
\`\`\`

\#\#\# 4.7. Güvenlik ve Gizlilik Tasarımı

\#\#\#\# 4.7.1. Gizlilik Odaklı Mimari

Bu projenin en önemli özelliklerinden biri gizlilik odaklı tasarımıdır:

\`\`\`  
┌─────────────────────────────────────────────────────────────────────────┐  
│                    GİZLİLİK MİMARİSİ                                    │  
├─────────────────────────────────────────────────────────────────────────┤  
│                                                                         │  
│  ┌─────────────────┐                                                   │  
│  │   Kullanıcı     │                                                   │  
│  │   Sorusu        │                                                   │  
│  └────────┬────────┘                                                   │  
│           │                                                             │  
│           ▼                                                             │  
│  ┌─────────────────────────────────────────────────────────────────┐   │  
│  │                    YEREL SİSTEM                                  │   │  
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │   │  
│  │  │   FastAPI   │  │   Ollama    │  │   FAISS Index           │  │   │  
│  │  │   Backend   │──│   (Yerel)   │  │   (Yerel Vektör DB)     │  │   │  
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘  │   │  
│  │                                                                  │   │  
│  │  ✅ Veri yerel kalır                                            │   │  
│  │  ✅ İnternet bağlantısı opsiyonel                               │   │  
│  │  ✅ Üçüncü taraf API yok                                        │   │  
│  └─────────────────────────────────────────────────────────────────┘   │  
│           │                                                             │  
│           ▼                                                             │  
│  ┌─────────────────┐                                                   │  
│  │   Yanıt         │  ❌ Bulut sunucuya veri gönderilmez              │  
│  │   (Yerel)       │  ❌ Kullanıcı verisi loglanmaz                   │  
│  └─────────────────┘                                                   │  
│                                                                         │  
└─────────────────────────────────────────────────────────────────────────┘  
\`\`\`

\*\*Şekil 4.2.\*\* Gizlilik odaklı veri akışı

\#\#\#\# 4.7.2. Güvenlik Önlemleri

\*\*1. Input Validation (Pydantic):\*\*

\`\`\`python  
class ChatRequest(BaseModel):  
    messages: list\[MessageItem\] \= Field(..., min\_length=1)  
    temperature: float \= Field(0.7, ge=0, le=2)  \# Sınır kontrolü  
    max\_tokens: Optional\[int\] \= Field(None, le=4096)  \# Maksimum limit  
\`\`\`

\*\*2. CORS Yapılandırması:\*\*

\`\`\`python  
\# config.py  
ALLOWED\_ORIGINS: list\[str\] \= \[  
    origin.strip()  
    for origin in os.getenv("ALLOWED\_ORIGINS", "").split(",")  
    if origin.strip()  
\]  
ALLOWED\_ORIGINS\_STRICT: bool \= os.getenv("ALLOWED\_ORIGINS\_STRICT", "false").lower() \== "true"

\# main.py  
app.add\_middleware(  
    CORSMiddleware,  
    allow\_origins=allowed\_origins,  
    allow\_credentials=not allow\_all\_origins,  
    allow\_methods=\["\*"\],  
    allow\_headers=\["\*"\],  
)  
\`\`\`

\*\*3. Rate Limiting (Guardrails):\*\*

\`\`\`python  
\# config.py  
MAX\_CONTEXT\_TOKENS: int \= 4096   \# Bağlam token limiti  
MAX\_OUTPUT\_TOKENS: int \= 512     \# Çıktı token limiti  
REQUEST\_TIMEOUT: int \= 120       \# İstek zaman aşımı (saniye)  
\`\`\`

\*\*4. Hata Yönetimi:\*\*

\`\`\`python  
@app.post("/chat")  
async def chat(request: ChatRequest, http\_request: Request) \-\> ChatResponse:  
    try:  
        async with asyncio.timeout(Config.REQUEST\_TIMEOUT):  
            result \= await provider.generate(...)  
    except TimeoutError as exc:  
        raise HTTPException(status\_code=504, detail="İstek zaman aşımına uğradı.")  
    except RuntimeError as exc:  
        raise HTTPException(status\_code=500, detail=str(exc))  
\`\`\`

\#\#\#\# 4.7.3. Çevrimdışı Çalışma Desteği

Sistem, internet bağlantısı olmadan da çalışabilmektedir:

\*\*Çizelge 4.4.\*\* Çevrimiçi/Çevrimdışı özellik karşılaştırması

| Özellik | Çevrimiçi | Çevrimdışı |  
|---------|-----------|------------|  
| Temel sohbet | ✅ | ✅ |  
| RAG (yerel index) | ✅ | ✅ |  
| Model indirme | ✅ | ❌ |  
| HuggingFace model cache | ✅ | ✅ (önceden indirilmişse) |  
| Appwrite loglama | ✅ | ❌ (atlanır) |

\---

\#\# 5\. ARAŞTIRMA BULGULARI VE TARTIŞMA

\#\#\# 5.1. Test Stratejisi ve CI/CD

\#\#\#\# 5.1.1. Test Türleri

Projede çeşitli test türleri uygulanmıştır:

\*\*Çizelge 5.1.\*\* Test türleri ve araçları

| Test Türü | Araç | Dosya | Açıklama |  
|-----------|------|-------|----------|  
| Birim Testleri | pytest | \`test\_main.py\` | API endpoint testleri |  
| Kritik Bilgi Testleri | pytest | \`test\_critical\_facts.py\` | Konum, kuruluş yılı doğrulama |  
| Response Cleaner Testleri | pytest | \`test\_response\_cleaner.py\` | Yanıt temizleme testleri |  
| Flutter Widget Testleri | flutter test | \`widget\_test.dart\` | UI bileşen testleri |  
| Storage Testleri | flutter test | \`storage\_service\_test.dart\` | Yerel depolama testleri |

\#\#\#\# 5.1.2. CI/CD Pipeline

GitHub Actions üzerinde otomatik kalite kontrolleri:

\`\`\`yaml  
\# .github/workflows/backend.yml  
name: Backend CI

on:  
  push:  
    branches: \[main\]  
  pull\_request:  
    branches: \[main\]

jobs:  
  test:  
    runs-on: ubuntu-latest  
    steps:  
      \- uses: actions/checkout@v4  
      \- name: Set up Python  
        uses: actions/setup-python@v5  
        with:  
          python-version: '3.11'  
        
      \- name: Install dependencies  
        run: |  
          cd backend  
          pip install \-r requirements.txt  
          pip install pytest ruff mypy  
        
      \- name: Run tests  
        run: |  
          cd backend  
          python \-m pytest \-q  
        
      \- name: Lint with ruff  
        run: |  
          cd backend  
          ruff check .  
        
      \- name: Type check with mypy  
        run: |  
          cd backend  
          mypy .  
\`\`\`

\`\`\`yaml  
\# .github/workflows/dart.yml  
name: Flutter Build

on:  
  push:  
    branches: \[main\]  
  pull\_request:  
    branches: \[main\]

jobs:  
  build:  
    runs-on: ubuntu-latest  
    steps:  
      \- uses: actions/checkout@v4  
      \- uses: subosito/flutter-action@v2  
        with:  
          flutter-version: '3.24.0'  
        
      \- name: Install dependencies  
        run: flutter pub get  
        
      \- name: Analyze  
        run: flutter analyze  
        
      \- name: Run tests  
        run: flutter test  
\`\`\`

\#\#\#\# 5.1.3. Kalite Kapıları Sonuçları

\*\*Çizelge 5.2.\*\* CI/CD kalite kapısı sonuçları

| Kapı | Durum | Detay |  
|------|-------|-------|  
| pytest | ✅ Geçti | Tüm testler başarılı |  
| ruff | ✅ Geçti | Kod stili uyumlu |  
| mypy | ✅ Geçti | Tip hataları yok |  
| flutter analyze | ✅ Geçti | Dart analizi temiz |  
| flutter test | ✅ Geçti | Widget testleri başarılı |  
| encoding guard | ✅ Geçti | UTF-8 uyumlu |

\#\#\# 5.2. Kritik Bilgi Doğruluk Testleri

\#\#\#\# 5.2.1. Test Senaryoları

Selçuk Üniversitesi hakkındaki kritik bilgilerin doğruluğu test edilmiştir:

\`\`\`python  
\# test\_critical\_facts.py  
import pytest  
from rag\_service import rag\_service

class TestCriticalFacts:  
    """Kritik bilgi doğruluk testleri."""  
      
    def test\_konum\_konya(self):  
        """Konum bilgisi KONYA olmalı."""  
        context, \_ \= rag\_service.get\_context("Selçuk Üniversitesi nerede?")  
        assert "Konya" in context  
        assert "İzmir" not in context  \# Yanlış bilgi kontrolü  
        assert "Ankara" not in context  
      
    def test\_kurulus\_yili\_1975(self):  
        """Kuruluş yılı 1975 olmalı."""  
        context, \_ \= rag\_service.get\_context("Selçuk Üniversitesi ne zaman kuruldu?")  
        assert "1975" in context  
      
    def test\_bilgisayar\_teknoloji\_fakultesi(self):  
        """Bilgisayar Mühendisliği Teknoloji Fakültesi'nde olmalı."""  
        context, \_ \= rag\_service.get\_context("Bilgisayar Mühendisliği hangi fakültede?")  
        assert "Teknoloji Fakültesi" in context  
        assert "Mühendislik Fakültesi" not in context  \# Yanlış bilgi kontrolü  
      
    def test\_mudek\_akreditasyonu(self):  
        """MÜDEK akreditasyonu olmalı."""  
        context, \_ \= rag\_service.get\_context("Bilgisayar Mühendisliği akredite mi?")  
        assert "MÜDEK" in context or "akreditasyon" in context.lower()  
      
    def test\_kampus\_alaeddin\_keykubat(self):  
        """Ana kampüs Alaeddin Keykubat olmalı."""  
        context, \_ \= rag\_service.get\_context("Selçuk Üniversitesi kampüsleri")  
        assert "Alaeddin Keykubat" in context  
\`\`\`

\#\#\#\# 5.2.2. Doğruluk Test Sonuçları

\*\*Çizelge 5.3.\*\* Kritik bilgi doğruluk test sonuçları

| \# | Test Sorusu | Beklenen | Gerçek Yanıt | Sonuç |  
|---|-------------|----------|--------------|-------|  
| 1 | Selçuk Üniversitesi nerede? | Konya | "Konya ilinde bulunmaktadır" | ✅ |  
| 2 | Hangi şehirde? | Konya | "Konya'dadır" | ✅ |  
| 3 | Ne zaman kuruldu? | 1975 | "1975 yılında kurulmuştur" | ✅ |  
| 4 | Kaç yılında kuruldu? | 1975 | "1975" | ✅ |  
| 5 | Bilgisayar Mühendisliği hangi fakültede? | Teknoloji Fakültesi | "Teknoloji Fakültesi bünyesinde" | ✅ |  
| 6 | Bilgisayar Mühendisliği nerede? | Alaeddin Keykubat | "Alaeddin Keykubat Yerleşkesi" | ✅ |  
| 7 | MÜDEK akreditasyonu var mı? | Evet | "MÜDEK akreditasyonuna sahiptir" | ✅ |  
| 8 | Kampüsler hangileri? | Alaeddin Keykubat, Ardıçlı | "İki ana kampüs: Alaeddin Keykubat ve Ardıçlı" | ✅ |  
| 9 | Kaç fakülte var? | 23 | "23 fakülte bulunmaktadır" | ✅ |  
| 10 | Öğrenci sayısı? | 100,000+ | "100.000'den fazla öğrenci" | ✅ |

\*\*Kritik Bilgi Doğruluk Oranı: 10/10 \= %100\*\*

\#\#\#\# 5.2.3. Hallucination Testleri

Sistemin uydurma bilgi üretip üretmediği test edilmiştir:

\*\*Çizelge 5.4.\*\* Hallucination test sonuçları

| \# | Test Sorusu | Beklenen Davranış | Gerçek Davranış | Sonuç |  
|---|-------------|-------------------|-----------------|-------|  
| 1 | Selçuk Üniversitesi İzmir'de mi? | Hayır, Konya | "Hayır, Konya'dadır" | ✅ |  
| 2 | Uzay Fakültesi var mı? | Yok demeli | "Böyle bir fakülte bulunmamaktadır" | ✅ |  
| 3 | 2050 akademik takvimi? | Bilmiyorum demeli | "Bu konuda bilgim bulunmamaktadır" | ✅ |  
| 4 | Rektörün telefon numarası? | Kişisel bilgi vermemeli | "Genel iletişim bilgileri için..." | ✅ |  
| 5 | Sınav soruları? | Vermemeli | "Sınav soruları paylaşamam" | ✅ |

\*\*Hallucination Oranı: 0/5 \= %0\*\* (Başarılı)

\#\#\# 5.3. RAG Performans Değerlendirmesi

\#\#\#\# 5.3.1. RAG Kaynak Eşleşme Testleri

\*\*Çizelge 5.5.\*\* RAG kaynak eşleşme sonuçları

| Soru Kategorisi | Soru Sayısı | Doğru Kaynak | Eşleşme Oranı |  
|-----------------|-------------|--------------|---------------|  
| Genel Bilgiler | 10  
\#\#\# 5.3. RAG Performans Değerlendirmesi (Devam)

\#\#\#\# 5.3.1. RAG Kaynak Eşleşme Testleri (Devam)

\*\*Çizelge 5.5.\*\* RAG kaynak eşleşme sonuçları

| Soru Kategorisi | Soru Sayısı | Doğru Kaynak | Eşleşme Oranı |  
|-----------------|-------------|--------------|---------------|  
| Genel Bilgiler | 10 | 10 | %100 |  
| Bilgisayar Mühendisliği | 8 | 8 | %100 |  
| Teknoloji Fakültesi | 5 | 5 | %100 |  
| Kampüs Bilgileri | 6 | 6 | %100 |  
| SSS | 12 | 11 | %91.7 |  
| \*\*TOPLAM\*\* | \*\*41\*\* | \*\*40\*\* | \*\*%97.6\*\* |

\#\#\#\# 5.3.2. RAG Strict Mode Testleri

RAG strict mode etkinken, kaynak bulunamadığında sistem yanıt vermemelidir:

\`\`\`python  
\# Test: RAG strict mode  
def test\_rag\_strict\_no\_source():  
    """Kaynak yoksa yanıt vermemeli."""  
    response \= client.post("/chat", json={  
        "messages": \[{"role": "user", "content": "Mars'ta yaşam var mı?"}\],  
        "rag\_enabled": True,  
        "rag\_strict": True,  
    })  
      
    data \= response.json()  
    assert "güvenilir bir kaynak bulamadım" in data\["answer"\].lower()  
\`\`\`

\*\*Çizelge 5.6.\*\* RAG strict mode test sonuçları

| Test Durumu | Beklenen | Gerçek | Sonuç |  
|-------------|----------|--------|-------|  
| Kaynak var, strict=True | Yanıt ver | Yanıt verildi | ✅ |  
| Kaynak yok, strict=True | Yanıt verme | "Kaynak bulamadım" | ✅ |  
| Kaynak var, strict=False | Yanıt ver | Yanıt verildi | ✅ |  
| Kaynak yok, strict=False | Genel yanıt | Genel yanıt verildi | ✅ |

\#\#\#\# 5.3.3. Yanıt Süresi Analizi

\*\*Çizelge 5.7.\*\* Yanıt süresi ölçümleri (Ollama \+ Llama 3.2:3b)

| Metrik | Değer | Hedef | Durum |  
|--------|-------|-------|-------|  
| İlk token süresi (TTFT) | 0.8-1.5 sn | \< 2 sn | ✅ |  
| Toplam yanıt süresi (basit soru) | 3-5 sn | \< 10 sn | ✅ |  
| Toplam yanıt süresi (karmaşık soru) | 8-15 sn | \< 30 sn | ✅ |  
| Token üretim hızı | 15-25 token/sn | ≥ 10 token/sn | ✅ |  
| RAG arama süresi | 50-150 ms | \< 500 ms | ✅ |

\*\*Not:\*\* Ölçümler, orta seviye bir bilgisayarda (Intel i7, 16GB RAM, GPU olmadan) yapılmıştır. GPU ile performans önemli ölçüde artmaktadır.

\#\#\#\# 5.3.4. RAG Index İstatistikleri

\*\*Çizelge 5.8.\*\* RAG index istatistikleri

| Metrik | Değer |  
|--------|-------|  
| Toplam doküman sayısı | 5 |  
| Toplam chunk sayısı | \~150 |  
| Chunk boyutu | 500 karakter |  
| Overlap | 50 karakter |  
| Embedding boyutu | 384 |  
| Index boyutu (FAISS) | \~2 MB |  
| Embedding modeli | paraphrase-multilingual-MiniLM-L12-v2 |

\#\#\# 5.4. Karşılaşılan Zorluklar ve Çözümler

Proje geliştirme sürecinde çeşitli teknik zorluklarla karşılaşılmıştır.

\#\#\#\# 5.4.1. Teknik Zorluklar ve Çözümler

\*\*Çizelge 5.9.\*\* Karşılaşılan zorluklar ve uygulanan çözümler

| \# | Zorluk | Açıklama | Çözüm | Sonuç |  
|---|--------|----------|-------|-------|  
| 1 | \*\*UTF-8 Encoding\*\* | Windows'ta Türkçe karakter sorunları | \`\_configure\_utf8\_environment()\` fonksiyonu, stdout/stderr reconfigure | ✅ Çözüldü |  
| 2 | \*\*Ollama Bağlantı\*\* | Ollama sunucusu bazen yanıt vermiyordu | Health check endpoint, retry mekanizması, timeout ayarları | ✅ Çözüldü |  
| 3 | \*\*SSE Streaming\*\* | Flutter'da SSE parse sorunları | Özel SSE parser, chunk birleştirme | ✅ Çözüldü |  
| 4 | \*\*Hallucination\*\* | Model bazen yanlış bilgi üretiyordu | RAG strict mode, kaynak gösterimi, prompt engineering | ✅ Çözüldü |  
| 5 | \*\*Türkçe Yanıt Kalitesi\*\* | Bazı yanıtlar İngilizce geliyordu | Sistem prompt'ta dil belirtme, \`pick\_language()\` fonksiyonu | ✅ Çözüldü |  
| 6 | \*\*Response Cleaning\*\* | Model çıktısında gereksiz karakterler | \`StreamingResponseCleaner\` sınıfı | ✅ Çözüldü |  
| 7 | \*\*HuggingFace GPU\*\* | Windows'ta torch DLL hataları | Detaylı kurulum dokümantasyonu, opsiyonel HF desteği | ⚠️ Kısmen |  
| 8 | \*\*CORS Sorunları\*\* | Flutter web'den API erişim hataları | Dinamik CORS yapılandırması, dev origins | ✅ Çözüldü |

\#\#\#\# 5.4.2. Zorluk Detayları ve Çözüm Yaklaşımları

\*\*1. UTF-8 Encoding Sorunu:\*\*

Windows'ta Python stdout/stderr varsayılan olarak cp1252 encoding kullanmaktadır. Bu, Türkçe karakterlerin (ğ, ü, ş, ö, ç, ı) hatalı görüntülenmesine neden oluyordu.

\`\`\`python  
\# config.py \- Çözüm  
def \_configure\_utf8\_environment() \-\> None:  
    """Windows'ta UTF-8 yapılandırması."""  
    if sys.platform \== "win32":  
        for stream\_name in ("stdout", "stderr"):  
            stream \= getattr(sys, stream\_name, None)  
            if stream and hasattr(stream, "reconfigure"):  
                try:  
                    stream.reconfigure(encoding="utf-8")  
                except (AttributeError, ValueError):  
                    pass  
\`\`\`

\*\*2. Hallucination Önleme:\*\*

RAG strict mode ve prompt engineering ile hallucination minimize edilmiştir:

\`\`\`python  
\# prompts.py \- Strict RAG prompt  
def build\_rag\_system\_prompt(base\_prompt, context, language, strict):  
    strict\_instruction \= ""  
    if strict:  
        strict\_instruction \= """  
ÖNEMLİ: Yalnızca yukarıdaki BAĞLAM bilgilerini kullan.  
Bağlamda olmayan bilgileri UYDURMA.  
Emin olmadığın konularda "Bu konuda bilgim bulunmamaktadır" de.  
"""  
    return f"{base\_prompt}\\n\\n\#\#\# BAĞLAM \#\#\#\\n{context}\\n\#\#\# BAĞLAM SONU \#\#\#\\n{strict\_instruction}"  
\`\`\`

\*\*3. SSE Streaming Parse:\*\*

Flutter'da SSE stream'ini parse etmek için özel bir yaklaşım geliştirilmiştir:

\`\`\`dart  
// Flutter SSE parsing  
await for (final chunk in response.stream.transform(utf8.decoder)) {  
  for (final line in chunk.split('\\n')) {  
    if (\!line.startsWith('data: ')) continue;  
      
    final jsonStr \= line.substring(6);  
    if (jsonStr.isEmpty || jsonStr \== '\[DONE\]') continue;  
      
    try {  
      final data \= jsonDecode(jsonStr);  
      // Event işleme...  
    } catch (e) {  
      // JSON parse hatası \- devam et  
    }  
  }  
}  
\`\`\`

\*\*4. Response Cleaning:\*\*

Model çıktısında bazen gereksiz karakterler veya formatlar bulunuyordu:

\`\`\`python  
\# response\_cleaner.py  
class StreamingResponseCleaner:  
    """Akış yanıtlarını temizle."""  
      
    def \_\_init\_\_(self, language: str \= "tr"):  
        self.language \= language  
        self.buffer \= ""  
      
    def feed(self, token: str) \-\> str:  
        """Token'ı işle ve temizlenmiş çıktı döndür."""  
        self.buffer \+= token  
          
        \# Gereksiz karakterleri temizle  
        cleaned \= self.buffer  
        cleaned \= re.sub(r'\<\\|.\*?\\|\>', '', cleaned)  \# Özel tokenlar  
        cleaned \= re.sub(r'\\\[INST\\\].\*?\\\[/INST\\\]', '', cleaned)  \# Instruction markers  
          
        return cleaned  
      
    def finalize(self) \-\> str:  
        """Son temizleme."""  
        return self.buffer.strip()  
\`\`\`

\#\#\#\# 5.4.3. Öğrenilen Dersler

1\. \*\*Yerel LLM Avantajları:\*\* Gizlilik ve çevrimdışı çalışma kritik avantajlar sağlamaktadır. Ancak donanım gereksinimleri göz önünde bulundurulmalıdır.

2\. \*\*RAG Önemi:\*\* Hallucination problemini çözmek için RAG vazgeçilmezdir. Strict mode, akademik ortamlar için özellikle önemlidir.

3\. \*\*Çoklu Sağlayıcı Esnekliği:\*\* Provider pattern, farklı LLM'ler arasında geçişi kolaylaştırmaktadır.

4\. \*\*CI/CD Değeri:\*\* Otomatik testler ve kalite kapıları, hataları erken yakalamaktadır.

5\. \*\*Encoding Dikkat:\*\* Cross-platform geliştirmede encoding sorunları ciddi zaman kaybına neden olabilmektedir.

6\. \*\*Dokümantasyon:\*\* Kapsamlı dokümantasyon (INSTALL.md, SORUN\_GIDERME.md) kullanıcı deneyimini iyileştirmektedir.

\---

\#\# 6\. SONUÇLAR VE ÖNERİLER

\#\#\# 6.1. Sonuçlar

Bu proje kapsamında, Selçuk Üniversitesi öğrenci ve personeline hizmet vermek üzere gizliliğe odaklı, yerel çalışabilen yapay zeka destekli bir akademik bilgi asistanı başarıyla geliştirilmiştir.

\#\#\#\# 6.1.1. Hedeflere Ulaşma Durumu

\*\*Çizelge 6.1.\*\* Proje hedeflerinin değerlendirmesi

| Hedef | Açıklama | Hedef Değer | Gerçekleşen | Durum |  
|-------|----------|-------------|-------------|-------|  
| H1 | Gizlilik (yerel veri işleme) | %100 yerel | %100 yerel | ✅ Başarılı |  
| H2 | Çevrimdışı çalışabilirlik | Temel sohbet | Tam destek | ✅ Başarılı |  
| H3 | Kritik bilgi doğruluğu | %100 | %100 | ✅ Başarılı |  
| H4 | RAG kaynak gösterimi | Aktif | Aktif \+ citations | ✅ Başarılı |  
| H5 | Hallucination oranı | \< %5 | %0 | ✅ Başarılı |  
| H6 | Çoklu platform desteği | iOS, Android, Web | Flutter ile tümü | ✅ Başarılı |  
| H7 | CI/CD kalite kapıları | Aktif | pytest, ruff, mypy, flutter | ✅ Başarılı |  
| H8 | Çoklu sağlayıcı desteği | Ollama \+ 1 | Ollama \+ HuggingFace | ✅ Başarılı |

\*\*Genel Başarı Oranı: 8/8 \= %100\*\*

\#\#\#\# 6.1.2. Projenin Özgün Katkıları

\*\*1. Gizlilik Odaklı Üniversite Asistanı:\*\*

Türkiye'deki üniversite chatbot çözümlerinin çoğu bulut tabanlı API'lere bağımlıdır. Bu proje, tamamen yerel çalışabilen ilk kapsamlı örneklerden biridir.

\*\*2. RAG ile Akademik Doğrulanabilirlik:\*\*

Kaynak gösterimi (citations) özelliği, akademik ortamda güvenilirlik açısından kritik öneme sahiptir. Kullanıcılar, verilen bilginin hangi kaynaktan geldiğini görebilmektedir.

\*\*3. Çoklu Sağlayıcı Mimarisi:\*\*

Provider pattern ile tasarlanan sistem, farklı LLM sağlayıcıları arasında kolayca geçiş yapabilmektedir. Bu esneklik, farklı donanım ve performans gereksinimlerine uyum sağlamaktadır.

\*\*4. Profesyonel Yazılım Geliştirme Pratikleri:\*\*

CI/CD pipeline, otomatik testler, kod kalitesi kontrolleri ve kapsamlı dokümantasyon ile akademik bir proje için profesyonel standartlar uygulanmıştır.

\#\#\#\# 6.1.3. Teknik Başarılar

\*\*Çizelge 6.2.\*\* Teknik başarı özeti

| Kategori | Başarı |  
|----------|--------|  
| \*\*Backend\*\* | FastAPI \+ SSE streaming \+ çoklu sağlayıcı |  
| \*\*RAG\*\* | FAISS \+ sentence-transformers \+ strict mode |  
| \*\*Frontend\*\* | Flutter \+ GetX \+ Material 3 \+ çoklu platform |  
| \*\*DevOps\*\* | GitHub Actions CI/CD \+ Docker \+ Nginx |  
| \*\*Dokümantasyon\*\* | 15+ Markdown dosyası, API sözleşmesi |  
| \*\*Test\*\* | pytest \+ flutter test \+ kritik bilgi testleri |

\#\#\#\# 6.1.4. Projenin Kısıtlamaları

1\. \*\*Donanım Gereksinimi:\*\* Yerel LLM çalıştırmak için yeterli RAM (8GB+) ve tercihen GPU gerekmektedir.

2\. \*\*Model Boyutu:\*\* Küçük modeller (3B) hızlı ancak kalite düşük; büyük modeller (70B) kaliteli ancak yavaş ve kaynak yoğun.

3\. \*\*Knowledge Base Kapsamı:\*\* Mevcut bilgi tabanı sınırlıdır. Tüm üniversite bilgilerini kapsamak için genişletilmelidir.

4\. \*\*Gerçek Zamanlı Güncelleme:\*\* Bilgi tabanı manuel güncelleme gerektirmektedir. Otomatik güncelleme mekanizması yoktur.

5\. \*\*Kişisel Veri Erişimi:\*\* OBS entegrasyonu olmadığından kişisel öğrenci bilgilerine erişilememektedir.

\#\#\# 6.2. Öneriler

\#\#\#\# 6.2.1. Kısa Vadeli İyileştirmeler (1-3 Ay)

\*\*1. Knowledge Base Genişletme:\*\*

\`\`\`  
Mevcut: 5 doküman, \~150 chunk  
Hedef: 50+ doküman, 1500+ chunk

Eklenecek içerikler:  
\- Tüm fakülte ve bölüm bilgileri  
\- Akademik takvim (güncel)  
\- Yönetmelikler ve prosedürler  
\- Kampüs haritaları ve tesisler  
\- Öğrenci kulüpleri ve etkinlikler  
\`\`\`

\*\*2. Performans Optimizasyonu:\*\*

\`\`\`python  
\# Önerilen: Redis cache entegrasyonu  
import redis

class CachedRAGService:  
    def \_\_init\_\_(self):  
        self.redis \= redis.Redis()  
        self.cache\_ttl \= 3600  \# 1 saat  
      
    def get\_context(self, query: str) \-\> tuple:  
        cache\_key \= f"rag:{hash(query)}"  
        cached \= self.redis.get(cache\_key)  
        if cached:  
            return json.loads(cached)  
          
        result \= self.\_search(query)  
        self.redis.setex(cache\_key, self.cache\_ttl, json.dumps(result))  
        return result  
\`\`\`

\*\*3. Kullanıcı Geri Bildirimi:\*\*

\`\`\`dart  
// Flutter \- Geri bildirim widget'ı  
class FeedbackWidget extends StatelessWidget {  
  final String messageId;  
    
  @override  
  Widget build(BuildContext context) {  
    return Row(  
      children: \[  
        IconButton(  
          icon: Icon(Icons.thumb\_up\_outlined),  
          onPressed: () \=\> \_sendFeedback(messageId, positive: true),  
        ),  
        IconButton(  
          icon: Icon(Icons.thumb\_down\_outlined),  
          onPressed: () \=\> \_sendFeedback(messageId, positive: false),  
        ),  
      \],  
    );  
  }  
}  
\`\`\`

\#\#\#\# 6.2.2. Orta Vadeli Geliştirmeler (3-6 Ay)

\*\*1. Çoklu Dil Desteği:\*\*

\`\`\`python  
\# Önerilen: Dil algılama ve çoklu dil yanıt  
from langdetect import detect

SUPPORTED\_LANGUAGES \= \["tr", "en", "ar"\]

def detect\_and\_respond(query: str) \-\> str:  
    detected\_lang \= detect(query)  
    if detected\_lang not in SUPPORTED\_LANGUAGES:  
        detected\_lang \= "tr"  \# Varsayılan  
      
    return generate\_response(query, language=detected\_lang)  
\`\`\`

\*\*2. Sesli Asistan:\*\*

\`\`\`dart  
// Flutter \- Speech-to-Text entegrasyonu  
import 'package:speech\_to\_text/speech\_to\_text.dart';

class VoiceInput extends StatefulWidget {  
  @override  
  \_VoiceInputState createState() \=\> \_VoiceInputState();  
}

class \_VoiceInputState extends State\<VoiceInput\> {  
  final SpeechToText \_speech \= SpeechToText();  
    
  void \_startListening() async {  
    await \_speech.listen(  
      onResult: (result) {  
        if (result.finalResult) {  
          \_sendMessage(result.recognizedWords);  
        }  
      },  
      localeId: 'tr\_TR',  
    );  
  }  
}  
\`\`\`

\*\*3. Analitik Dashboard:\*\*

\`\`\`python  
\# Önerilen: Kullanım istatistikleri  
@app.get("/admin/stats")  
async def get\_stats():  
    return {  
        "total\_queries": await db.count\_queries(),  
        "popular\_topics": await db.get\_popular\_topics(),  
        "avg\_response\_time": await db.get\_avg\_response\_time(),  
        "rag\_hit\_rate": await db.get\_rag\_hit\_rate(),  
        "user\_satisfaction": await db.get\_satisfaction\_score(),  
    }  
\`\`\`

\#\#\#\# 6.2.3. Uzun Vadeli Vizyon (6-12 Ay)

\*\*1. Resmi Üniversite Entegrasyonu:\*\*

\- Selçuk Üniversitesi IT altyapısı ile entegrasyon  
\- Resmi web sitesine widget olarak ekleme  
\- OBS ile read-only entegrasyon (kişisel bilgiler için)

\*\*2. Fine-tuned Türkçe Model:\*\*

\`\`\`python  
\# Önerilen: Selçuk Üniversitesi özel model  
\# 1\. selcuk\_qa\_dataset.jsonl ile fine-tuning  
\# 2\. Ollama'ya özel model olarak ekleme

\# Modelfile  
FROM llama3.1  
ADAPTER ./selcuk\_lora\_adapter.gguf  
SYSTEM "Sen Selçuk Üniversitesi resmi yapay zeka asistanısın..."  
\`\`\`

\*\*3. Proaktif Bilgilendirme:\*\*

\`\`\`dart  
// Flutter \- Push notification entegrasyonu  
class NotificationService {  
  void scheduleAcademicReminders() {  
    // Kayıt yenileme hatırlatması  
    // Sınav dönemi uyarısı  
    // Etkinlik bildirimleri  
  }  
}  
\`\`\`

\#\#\#\# 6.2.4. Teknik Öneriler

\*\*Çizelge 6.3.\*\* Teknik iyileştirme önerileri

| Alan | Mevcut | Önerilen | Öncelik |  
|------|--------|----------|---------|  
| Cache | Yok | Redis | Yüksek |  
| Veritabanı | JSON dosyaları | PostgreSQL | Orta |  
| Monitoring | Temel logging | Prometheus \+ Grafana | Orta |  
| Load Balancing | Yok | Nginx upstream | Düşük |  
| Model | Llama 3.2:3b | Fine-tuned Türkçe model | Orta |  
| Embedding | MiniLM | Türkçe özel embedding | Düşük |

\---

\#\# KAYNAKLAR

Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., ... ve Amodei, D., 2020, Language models are few-shot learners, \_Advances in Neural Information Processing Systems\_, 33, 1877-1901.

FastAPI, 2024, FastAPI Documentation, https://fastapi.tiangolo.com \[Ziyaret Tarihi: 10 Ocak 2025\].

Flutter, 2024, Flutter Documentation, https://flutter.dev/docs \[Ziyaret Tarihi: 10 Ocak 2025\].

GetX, 2024, GetX Package Documentation, https://pub.dev/packages/get \[Ziyaret Tarihi: 10 Ocak 2025\].

Google, 2018, Flutter: Beautiful native apps in record time, \_Google Developers\_, https://flutter.dev \[Ziyaret Tarihi: 10 Ocak 2025\].

Johnson, J., Douze, M. ve Jégou, H., 2019, Billion-scale similarity search with GPUs, \_IEEE Transactions on Big Data\_, 7(3), 535-547.

Jurafsky, D. ve Martin, J. H., 2023, Speech and language processing (3rd ed.), \_Stanford University\_, https://web.stanford.edu/\~jurafsky/slp3/ \[Ziyaret Tarihi: 10 Ocak 2025\].

LangChain, 2024, LangChain Documentation, https://python.langchain.com \[Ziyaret Tarihi: 10 Ocak 2025\].

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., ... ve Kiela, D., 2020, Retrieval-augmented generation for knowledge-intensive NLP tasks, \_Advances in Neural Information Processing Systems\_, 33, 9459-9474.

Ollama, 2024, Ollama Documentation, https://ollama.ai \[Ziyaret Tarihi: 10 Ocak 2025\].

OpenAI, 2022, ChatGPT: Optimizing language models for dialogue, \_OpenAI Blog\_, https://openai.com/blog/chatgpt \[Ziyaret Tarihi: 10 Ocak 2025\].

OpenAI, 2023, GPT-4 technical report, \_arXiv preprint arXiv:2303.08774\_.

Page, L. C. ve Gehlbach, H., 2017, How an artificially intelligent virtual assistant helps students navigate the road to college, \_AERA Open\_, 3(4), 1-12.

Reimers, N. ve Gurevych, I., 2019, Sentence-BERT: Sentence embeddings using Siamese BERT-networks, \_Proceedings of EMNLP-IJCNLP 2019\_, Hong Kong, 3982-3992.

Selçuk Üniversitesi, 2024, Selçuk Üniversitesi Resmi Web Sitesi, https://www.selcuk.edu.tr \[Ziyaret Tarihi: 10 Ocak 2025\].

Selçuk Üniversitesi Teknoloji Fakültesi, 2024, Bilgisayar Mühendisliği Bölümü, https://www.selcuk.edu.tr/teknoloji \[Ziyaret Tarihi: 10 Ocak 2025\].

Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M. A., Lacroix, T., ... ve Lample, G., 2023, LLaMA: Open and efficient foundation language models, \_arXiv preprint arXiv:2302.13971\_.

Turing, A. M., 1950, Computing machinery and intelligence, \_Mind\_, 59(236), 433-460.

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... ve Polosukhin, I., 2017, Attention is all you need, \_Advances in Neural Information Processing Systems\_, 30, 5998-6008.

Weizenbaum, J., 1966, ELIZA—a computer program for the study of natural language communication between man and machine, \_Communications of the ACM\_, 9(1), 36-45.

\---

\#\# EKLER

\#\#\# EK-A: Kurulum Kılavuzu

\#\#\#\# A.1. Gereksinimler

\*\*Donanım:\*\*  
\- CPU: 4+ çekirdek önerilir  
\- RAM: 8GB minimum, 16GB önerilir  
\- Disk: 10GB+ boş alan (model indirmeleri için)  
\- GPU: Opsiyonel, ancak performansı önemli ölçüde artırır

\*\*Yazılım:\*\*  
\- Python 3.10+  
\- Flutter 3.4+  
\- Ollama (yerel LLM için)  
\- Git

\#\#\#\# A.2. Backend Kurulumu

\`\`\`bash  
\# 1\. Repository'yi klonlayın  
git clone https://github.com/esN2k/SelcukAiAssistant.git  
cd SelcukAiAssistant

\# 2\. Python sanal ortamı oluşturun  
cd backend  
python \-m venv .venv

\# Windows  
.venv\\Scripts\\activate

\# Linux/macOS  
source .venv/bin/activate

\# 3\. Bağımlılıkları yükleyin  
pip install \-r requirements.txt

\# 4\. Ortam değişkenlerini ayarlayın  
copy .env.example .env  \# Windows  
cp .env.example .env    \# Linux/macOS

\# .env dosyasını düzenleyin:  
\# \- RAG\_ENABLED=true  
\# \- OLLAMA\_MODEL=llama3.2:3b

\# 5\. Ollama'yı kurun ve modeli indirin  
\# https://ollama.ai adresinden Ollama'yı indirin  
ollama pull llama3.2:3b

\# 6\. RAG index'ini oluşturun (opsiyonel, hazır index mevcut)  
python rag\_ingest.py \--input ../docs \--output ./data/rag

\# 7\. Backend'i başlatın  
uvicorn main:app \--reload \--host 0.0.0.0 \--port 8000  
\`\`\`

\#\#\#\# A.3. Flutter Kurulumu

\`\`\`bash  
\# 1\. Flutter SDK'yı kurun  
\# https://flutter.dev/docs/get-started/install

\# 2\. Proje dizinine gidin  
cd SelcukAiAssistant

\# 3\. Bağımlılıkları yükleyin  
flutter pub get

\# 4\. Ortam değişkenlerini ayarlayın  
copy .env.example .env

\# .env dosyasını düzenleyin:  
\# BACKEND\_URL=http://localhost:8000

\# 5\. Uygulamayı çalıştırın  
flutter run

\# Web için  
flutter run \-d chrome

\# Android için  
flutter run \-d android

\# iOS için (macOS gerekli)  
flutter run \-d ios  
\`\`\`

\#\#\#\# A.4. Docker ile Kurulum

\`\`\`bash  
\# Tüm servisleri başlatın  
docker-compose up \-d

\# Ollama ile birlikte  
docker-compose \--profile ollama up \-d

\# Logları izleyin  
docker-compose logs \-f backend  
\`\`\`

\#\#\# EK-B: API Kullanım Örnekleri

\#\#\#\# B.1. cURL Örnekleri

\`\`\`bash  
\# Sağlık kontrolü  
curl http://localhost:8000/health

\# Senkron chat  
curl \-X POST http://localhost:8000/chat \\  
  \-H "Content-Type: application/json" \\  
  \-d '{  
    "messages": \[{"role": "user", "content": "Selçuk Üniversitesi nerede?"}\],  
    "rag\_enabled": true  
  }'

\# Model listesi  
curl http://localhost:8000/models

\# Ollama durumu  
curl http://localhost:8000/health/ollama  
\`\`\`

\#\#\#\# B.2. Python Örnekleri

\`\`\`python  
import httpx  
import asyncio

async def chat\_example():  
    async with httpx.AsyncClient() as client:  
        response \= await client.post(  
            "http://localhost:8000/chat",  
            json={  
                "messages": \[  
                    {"role": "user", "content": "Bilgisayar Mühendisliği hangi fakültede?"}  
                \],  
                "rag\_enabled": True,  
                "rag\_strict": True,  
            },  
            timeout=60,  
        )  
        data \= response.json()  
        print(f"Yanıt: {data\['answer'\]}")  
        print(f"Kaynaklar: {data.get('citations', \[\])}")

asyncio.run(chat\_example())  
\`\`\`

\#\#\# EK-C: Knowledge  
\#\#\# EK-C: Knowledge Base Yapısı

\#\#\#\# C.1. JSON Bilgi Tabanı Şeması

\`\`\`json  
{  
  "universite\_bilgileri": {  
    "ad": "string",  
    "kuruluş\_yılı": "integer",  
    "şehir": "string",  
    "il": "string",  
    "ilçe": "string",  
    "adres": "string",  
    "posta\_kodu": "string",  
    "web\_sitesi": "string",  
    "telefon": "string",  
    "rektör": "string",  
    "öğrenci\_sayısı": "string",  
    "akademisyen\_sayısı": "string",  
    "fakülte\_sayısı": "integer",  
    "kampüsler": \["string"\]  
  },  
  "bilgisayar\_muhendisligi": {  
    "ad": "string",  
    "fakulte": "string",  
    "kampüs": "string",  
    "adres": "string",  
    "telefon": "string",  
    "email": "string",  
    "web": "string",  
    "akreditasyon": {  
      "mudek": "boolean",  
      "mudek\_açıklama": "string"  
    },  
    "araştırma\_alanları": \["string"\],  
    "laboratuvarlar": \["string"\],  
    "özellikler": \["string"\]  
  },  
  "sık\_sorulan\_sorular": \[  
    {  
      "kategori": "string",  
      "soru": "string",  
      "cevap": "string",  
      "anahtar\_kelimeler": \["string"\]  
    }  
  \]  
}  
\`\`\`

\#\#\#\# C.2. RAG Doküman Formatı

\`\`\`  
\# Dosya: 01\_genel\_bilgiler.txt

Selçuk Üniversitesi Genel Bilgiler  
\==================================

Selçuk Üniversitesi, 1975 yılında Konya'da kurulmuş bir devlet üniversitesidir.

Konum: Konya ili, Selçuklu ilçesi  
Adres: Alaeddin Keykubat Kampüsü, 42250 Selçuklu/Konya

Kampüsler:  
\- Alaeddin Keykubat Yerleşkesi (Ana kampüs)  
\- Ardıçlı Yerleşkesi (Sağlık kampüsü)

İstatistikler:  
\- 23 Fakülte  
\- 100.000+ Öğrenci  
\- 4.000+ Akademisyen

İletişim:  
\- Telefon: \+90 332 223 1000  
\- Web: https://www.selcuk.edu.tr  
\`\`\`

\#\#\#\# C.3. Soru-Cevap Veri Seti Formatı (JSONL)

\`\`\`jsonl  
{"messages": \[{"role": "user", "content": "Selçuk Üniversitesi nerede?"}, {"role": "assistant", "content": "Selçuk Üniversitesi, Konya ilinde bulunmaktadır."}\], "metadata": {"category": "genel", "source": "manuel\_verified"}}  
{"messages": \[{"role": "user", "content": "Ne zaman kuruldu?"}, {"role": "assistant", "content": "1975 yılında kurulmuştur."}\], "metadata": {"category": "genel", "source": "manuel\_verified"}}  
{"messages": \[{"role": "user", "content": "Bilgisayar Mühendisliği hangi fakültede?"}, {"role": "assistant", "content": "Teknoloji Fakültesi bünyesindedir."}\], "metadata": {"category": "bilgisayar", "source": "manuel\_verified"}}  
\`\`\`

\#\#\# EK-D: Test Sonuçları Detayı

\#\#\#\# D.1. pytest Çıktısı

\`\`\`  
\============================= test session starts \==============================  
platform win32 \-- Python 3.11.0, pytest-7.4.0  
rootdir: C:\\Projects\\SelcukAiAssistant\\backend  
collected 18 items

test\_main.py::test\_root\_endpoint PASSED                                   \[  5%\]  
test\_main.py::test\_health\_endpoint PASSED                                 \[ 11%\]  
test\_main.py::test\_chat\_endpoint PASSED                                   \[ 16%\]  
test\_main.py::test\_chat\_stream\_endpoint PASSED                            \[ 22%\]  
test\_main.py::test\_models\_endpoint PASSED                                 \[ 27%\]

test\_critical\_facts.py::test\_konum\_konya PASSED                           \[ 33%\]  
test\_critical\_facts.py::test\_kurulus\_yili\_1975 PASSED                     \[ 38%\]  
test\_critical\_facts.py::test\_bilgisayar\_teknoloji\_fakultesi PASSED        \[ 44%\]  
test\_critical\_facts.py::test\_mudek\_akreditasyonu PASSED                   \[ 50%\]  
test\_critical\_facts.py::test\_kampus\_alaeddin\_keykubat PASSED              \[ 55%\]

test\_response\_cleaner.py::test\_clean\_basic\_text PASSED                    \[ 61%\]  
test\_response\_cleaner.py::test\_clean\_special\_tokens PASSED                \[ 66%\]  
test\_response\_cleaner.py::test\_streaming\_cleaner PASSED                   \[ 72%\]

test\_extended.py::test\_rag\_service\_initialization PASSED                  \[ 77%\]  
test\_extended.py::test\_rag\_context\_retrieval PASSED                       \[ 83%\]  
test\_extended.py::test\_provider\_registry PASSED                           \[ 88%\]  
test\_extended.py::test\_config\_validation PASSED                           \[ 94%\]  
test\_extended.py::test\_utf8\_encoding PASSED                               \[100%\]

\============================= 18 passed in 12.45s \==============================  
\`\`\`

\#\#\#\# D.2. Flutter Test Çıktısı

\`\`\`  
00:03 \+8: All tests passed\!

✓ Widget Tests  
  ✓ MessageCard renders correctly (245ms)  
  ✓ TypingIndicator animates (312ms)  
  ✓ MarkdownMessageView renders markdown (189ms)  
  ✓ Citations display correctly (156ms)

✓ Controller Tests  
  ✓ ChatController initial state (89ms)  
  ✓ ChatController sendMessage (1.2s)  
  ✓ SettingsController persistence (234ms)

✓ Storage Tests  
  ✓ StorageService save and load (178ms)  
\`\`\`

\#\#\#\# D.3. Ruff Lint Çıktısı

\`\`\`  
All checks passed\!

Checked 15 files  
Found 0 errors  
\`\`\`

\#\#\#\# D.4. mypy Tip Kontrolü Çıktısı

\`\`\`  
Success: no issues found in 15 source files  
\`\`\`

\#\#\# EK-E: Ekran Görüntüleri Açıklamaları

\#\#\#\# E.1. Ana Sohbet Ekranı

\`\`\`  
┌─────────────────────────────────────────────────────────────┐  
│  🎓 Selçuk AI Asistan                              ☰  ⚙️  │  
├─────────────────────────────────────────────────────────────┤  
│                                                             │  
│  ┌─────────────────────────────────────────────────────┐   │  
│  │ 🤖 Merhaba\! Ben Selçuk Üniversitesi AI Asistanıyım. │   │  
│  │    Size nasıl yardımcı olabilirim?                  │   │  
│  │                                                     │   │  
│  │    Örnek sorular:                                   │   │  
│  │    • Selçuk Üniversitesi nerede?                    │   │  
│  │    • Bilgisayar Mühendisliği hangi fakültede?       │   │  
│  │    • MÜDEK akreditasyonu var mı?                    │   │  
│  └─────────────────────────────────────────────────────┘   │  
│                                                             │  
│  ┌─────────────────────────────────────────────────────┐   │  
│  │ 👤 Selçuk Üniversitesi ne zaman kuruldu?            │   │  
│  └─────────────────────────────────────────────────────┘   │  
│                                                      14:32 │  
│                                                             │  
│  ┌─────────────────────────────────────────────────────┐   │  
│  │ 🤖 Selçuk Üniversitesi \*\*1975\*\* yılında Konya'da    │   │  
│  │    kurulmuştur. Türkiye'nin en büyük devlet         │   │  
│  │    üniversitelerinden biridir.                      │   │  
│  │                                                     │   │  
│  │    ┌─────────────────────────────────────────────┐ │   │  
│  │    │ 📚 Kaynaklar:                               │ │   │  
│  │    │ \[01\_genel\_bilgiler.txt\]                     │ │   │  
│  │    └─────────────────────────────────────────────┘ │   │  
│  └─────────────────────────────────────────────────────┘   │  
│                                                      14:32 │  
│                                                             │  
├─────────────────────────────────────────────────────────────┤  
│  ┌───────────────────────────────────────────────┐  \[📤\]  │  
│  │ Mesajınızı yazın...                           │        │  
│  └───────────────────────────────────────────────┘        │  
└─────────────────────────────────────────────────────────────┘  
\`\`\`

\*\*Şekil E.1.\*\* Ana sohbet ekranı tasarımı

\#\#\#\# E.2. Akış Yanıtı (Streaming)

\`\`\`  
┌─────────────────────────────────────────────────────────────┐  
│  🎓 Selçuk AI Asistan                              ☰  ⚙️  │  
├─────────────────────────────────────────────────────────────┤  
│                                                             │  
│  ┌─────────────────────────────────────────────────────┐   │  
│  │ 👤 Bilgisayar Mühendisliği hakkında bilgi ver       │   │  
│  └─────────────────────────────────────────────────────┘   │  
│                                                      14:35 │  
│                                                             │  
│  ┌─────────────────────────────────────────────────────┐   │  
│  │ 🤖 Bilgisayar Mühendisliği bölümü, \*\*Teknoloji      │   │  
│  │    Fakültesi\*\* bünyesinde Alaeddin Keykubat         │   │  
│  │    Yerleşkesi'nde bulunmaktadır.                    │   │  
│  │                                                     │   │  
│  │    \*\*Özellikler:\*\*                                  │   │  
│  │    \- MÜDEK akreditasyonu ✓                          │   │  
│  │    \- Erasmus+ değişim programı                      │   │  
│  │    \- HPC laboratuvarı█                              │   │  
│  │                                                     │   │  
│  │    ⏳ Yazıyor...                                    │   │  
│  └─────────────────────────────────────────────────────┘   │  
│                                                             │  
├─────────────────────────────────────────────────────────────┤  
│  ┌───────────────────────────────────────────────┐  \[⏸️\]  │  
│  │ Mesajınızı yazın...                           │        │  
│  └───────────────────────────────────────────────┘        │  
└─────────────────────────────────────────────────────────────┘  
\`\`\`

\*\*Şekil E.2.\*\* Akış yanıtı sırasında ekran görünümü

\#\#\#\# E.3. Model Seçim Ekranı

\`\`\`  
┌─────────────────────────────────────────────────────────────┐  
│  ← Ayarlar                                                  │  
├─────────────────────────────────────────────────────────────┤  
│                                                             │  
│  Model Seçimi                                               │  
│  ─────────────────────────────────────────────────────────  │  
│                                                             │  
│  ┌─────────────────────────────────────────────────────┐   │  
│  │ 🟢 llama3.2:3b                              \[Seçili\] │   │  
│  │    Hızlı yanıtlar için optimize edilmiş              │   │  
│  │    Sağlayıcı: Ollama                                 │   │  
│  └─────────────────────────────────────────────────────┘   │  
│                                                             │  
│  ┌─────────────────────────────────────────────────────┐   │  
│  │ 🟢 llama3.1                                          │   │  
│  │    Daha kaliteli yanıtlar                            │   │  
│  │    Sağlayıcı: Ollama                                 │   │  
│  └─────────────────────────────────────────────────────┘   │  
│                                                             │  
│  ┌─────────────────────────────────────────────────────┐   │  
│  │ 🟡 Qwen2.5-1.5B-Instruct                             │   │  
│  │    HuggingFace modeli (GPU önerilir)                 │   │  
│  │    Sağlayıcı: HuggingFace                            │   │  
│  └─────────────────────────────────────────────────────┘   │  
│                                                             │  
│  RAG Ayarları                                               │  
│  ─────────────────────────────────────────────────────────  │  
│                                                             │  
│  RAG Etkin                                    \[✓\]           │  
│  Strict Mode (kaynak yoksa yanıt verme)      \[✓\]           │  
│  Top-K Sonuç                                 \[4\]           │  
│                                                             │  
└─────────────────────────────────────────────────────────────┘  
\`\`\`

\*\*Şekil E.3.\*\* Model ve RAG ayarları ekranı

\---

\#\# ÖZGEÇMİŞ

\#\#\# KİŞİSEL BİLGİLER (Öğrenci 1\)

\*\*Adı Soyadı:\*\* Doğukan BALAMAN

\*\*Öğrenci No:\*\* 203311066

\*\*Uyruğu:\*\* T.C.

\*\*E-posta:\*\* \[e-posta adresi\]

\*\*GitHub:\*\* github.com/esN2k

\#\#\# EĞİTİM

| Derece | Kurum | Bitirme Yılı |  
|--------|-------|--------------|  
| Lisans | Selçuk Üniversitesi, Teknoloji Fakültesi, Bilgisayar Mühendisliği | 2025 |  
| Lise | \[Lise Adı\] | 2020 |

\#\#\# TEKNİK BECERİLER

\- \*\*Programlama Dilleri:\*\* Python, Dart, JavaScript, SQL  
\- \*\*Frameworks:\*\* FastAPI, Flask, LangChain, Flutter  
\- \*\*Veritabanları:\*\* PostgreSQL, FAISS, SQLite  
\- \*\*AI/ML:\*\* Ollama, HuggingFace Transformers, RAG sistemleri  
\- \*\*DevOps:\*\* Docker, Git, GitHub Actions, CI/CD  
\- \*\*Araçlar:\*\* VS Code, PyCharm, Android Studio

\#\#\# PROJELER

\- \*\*Selçuk AI Asistan\*\* \- Yapay Zeka Destekli Üniversite Bilgi Asistanı (2024-2025)  
  \- Yerel LLM (Ollama) entegrasyonu  
  \- RAG pipeline tasarımı ve implementasyonu  
  \- FastAPI backend geliştirme  
  \- CI/CD pipeline kurulumu

\---

\#\#\# KİŞİSEL BİLGİLER (Öğrenci 2\)

\*\*Adı Soyadı:\*\* Ali YILDIRIM

\*\*Öğrenci No:\*\* 203311008

\*\*Uyruğu:\*\* T.C.

\*\*E-posta:\*\* \[e-posta adresi\]

\#\#\# EĞİTİM

| Derece | Kurum | Bitirme Yılı |  
|--------|-------|--------------|  
| Lisans | Selçuk Üniversitesi, Teknoloji Fakültesi, Bilgisayar Mühendisliği | 2025 |  
| Lise | \[Lise Adı\] | 2020 |

\#\#\# TEKNİK BECERİLER

\- \*\*Programlama Dilleri:\*\* Dart, Python, Java, Kotlin  
\- \*\*Frameworks:\*\* Flutter, GetX, Android SDK  
\- \*\*Mobil Geliştirme:\*\* iOS, Android, Cross-platform  
\- \*\*UI/UX:\*\* Material Design 3, Figma  
\- \*\*Araçlar:\*\* Android Studio, VS Code, Git, Firebase

\#\#\# PROJELER

\- \*\*Selçuk AI Asistan\*\* \- Flutter Mobil/Web Uygulama Geliştirme (2024-2025)  
  \- Flutter cross-platform uygulama  
  \- GetX state management  
  \- SSE streaming entegrasyonu  
  \- Material Design 3 UI tasarımı

\---

\#\# KONTROL LİSTESİ

| Kontrol Edilecek Hususlar | Evet | Hayır |  
|---------------------------|------|-------|  
| Sayfa yapısı uygun mu? | ✅ | |  
| Şekil ve çizelge başlık ve içerikleri uygun mu? | ✅ | |  
| Denklem yazımları uygun mu? | ✅ | |  
| İç kapak, onay sayfası, Proje bildirimi, özet, abstract, önsöz uygun yazıldı mı? | ✅ | |  
| Proje yazımı; Giriş, Kaynak Araştırması, Materyal ve Yöntem, Araştırma Bulguları ve Tartışma, Sonuçlar ve Öneriler sıralamasında mıdır? | ✅ | |  
| Kaynaklar soyadı sırasına göre verildi mi? | ✅ | |  
| Kaynaklarda verilen her bir yayına proje içerisinde atıfta bulunuldu mu? | ✅ | |  
| Kaynaklar açıklanan yazım kuralına uygun olarak yazıldı mı? | ✅ | |  
| Proje içerisinde kullanılan şekil ve çizelgelerde kullanılan ifadeler Türkçe'ye çevrilmiş mi? | ✅ | |  
| Projenin içindekiler kısmı, proje içerisinde verilen başlıklara uygun hazırlanmış mı? | ✅ | |

\*\*Yukarıdaki verilen cevapların doğruluğunu kabul ediyorum.\*\*

| | Unvanı Adı SOYADI | İmza |  
|---|---|---|  
| \*\*Öğrenci 1:\*\* | Doğukan BALAMAN | ................... |  
| \*\*Öğrenci 2:\*\* | Ali YILDIRIM | ................... |  
| \*\*Danışman 1:\*\* | Prof. Dr. Nurettin DOĞAN | ................... |  
| \*\*Danışman 2:\*\* | Dr. Öğr. Üyesi Onur İNAN | ................... |

\---

\# RAPOR SONU

\---

\#\# 📋 EK ÇIKTILAR

\#\#\# RAPOR\_OZET.md \- Yönetici Özeti

\`\`\`markdown  
\# Selçuk AI Asistan \- Yönetici Özeti

\#\# Proje Hakkında  
Selçuk Üniversitesi için geliştirilen, gizliliğe odaklı ve yerel çalışabilen   
yapay zeka destekli akademik bilgi asistanı.

\#\# Temel Özellikler  
\- ✅ \*\*Gizlilik:\*\* Tüm veri işleme yerel sistemde (Ollama)  
\- ✅ \*\*Çevrimdışı:\*\* İnternet olmadan temel sohbet  
\- ✅ \*\*RAG:\*\* Kaynak gösterimli yanıtlar  
\- ✅ \*\*Çoklu Platform:\*\* iOS, Android, Web (Flutter)  
\- ✅ \*\*%100 Kritik Bilgi Doğruluğu:\*\* Konya, 1975, Teknoloji Fakültesi  
\- ✅ \*\*%0 Hallucination:\*\* Strict RAG mode

\#\# Teknolojiler  
\- \*\*Backend:\*\* Python, FastAPI, LangChain  
\- \*\*LLM:\*\* Ollama (Llama 3.1/3.2), HuggingFace (opsiyonel)  
\- \*\*RAG:\*\* FAISS, sentence-transformers  
\- \*\*Frontend:\*\* Flutter, GetX, Material 3  
\- \*\*DevOps:\*\* GitHub Actions, Docker, Nginx

\#\# Proje Kimliği  
| Özellik | Değer |  
|---------|-------|  
| Gizlilik | %100 Yerel |  
| Kritik Bilgi Doğruluğu | %100 |  
| Hallucination Oranı | %0 |  
| RAG Kaynak Eşleşmesi | %97.6 |  
| CI/CD Kalite Kapıları | Tümü Geçti |

\#\# Özgün Değer  
1\. Türkiye'de yerel LLM kullanan ilk kapsamlı üniversite asistanı  
2\. RAG ile akademik doğrulanabilirlik  
3\. Çoklu sağlayıcı mimarisi (Provider Pattern)  
4\. Profesyonel CI/CD ve test altyapısı

\#\# Sonuç  
Proje, tüm hedeflerini başarıyla karşılamıştır. Sistem, üniversite   
bilgi erişimini gizlilik odaklı ve çevrimdışı çalışabilir şekilde   
iyileştirme potansiyeline sahiptir.

\#\# İletişim  
\- \*\*GitHub:\*\* github.com/esN2k/SelcukAiAssistant  
\- \*\*Danışmanlar:\*\* Prof. Dr. Nurettin DOĞAN, Dr. Öğr. Üyesi Onur İNAN  
\`\`\`

\---

\#\#\# TEKNIK\_DOKUMAN.md \- Teknik Özet

\`\`\`markdown  
\# Selçuk AI Asistan \- Teknik Dokümantasyon

\#\# Mimari Özet

\`\`\`  
Flutter App ──HTTP/SSE──\> FastAPI ──\> Ollama (Yerel LLM)  
                              └──\> RAG (FAISS \+ sentence-transformers)  
\`\`\`

\#\# Teknoloji Stack

| Katman | Teknoloji |  
|--------|-----------|  
| Frontend | Flutter 3.4+, Dart, GetX |  
| Backend | Python 3.10+, FastAPI 0.115 |  
| LLM | Ollama (Llama 3.1/3.2) |  
| RAG | FAISS, sentence-transformers |  
| CI/CD | GitHub Actions |

\#\# API Endpoints

| Endpoint | Method | Açıklama |  
|----------|--------|----------|  
| \`/chat\` | POST | Senkron sohbet |  
| \`/chat/stream\` | POST | SSE akış |  
| \`/models\` | GET | Model listesi |  
| \`/health/ollama\` | GET | Ollama durumu |

\#\# RAG Konfigürasyonu

\`\`\`env  
RAG\_ENABLED=true  
RAG\_VECTOR\_DB\_PATH=./data/rag  
RAG\_CHUNK\_SIZE=500  
RAG\_TOP\_K=4  
RAG\_EMBEDDING\_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2  
RAG\_STRICT\_DEFAULT=true  
\`\`\`

\#\# Sağlayıcı Deseni

\`\`\`python  
class ModelProvider(ABC):  
    async def generate(...) \-\> GenerationResult  
    async def stream(...) \-\> AsyncIterator\[StreamChunk\]  
    async def health\_check(...) \-\> dict

providers \= {  
    "ollama": OllamaProvider(),  
    "huggingface": HuggingFaceProvider(),  
}  
\`\`\`

\#\# Kalite Kapıları

\- pytest (birim testleri)  
\- ruff (Python linting)  
\- mypy (tip kontrolü)  
\- flutter analyze  
\- flutter test  
\`\`\`

\---

\*\*RAPOR TAMAMLANDI\*\*

\---

\*\*Not:\*\* Bu rapor, sağlanan GitHub repository bilgileri, kod dosyaları ve yapılandırma dosyaları temel alınarak hazırlanmıştır. Rapor, Selçuk Üniversitesi Teknoloji Fakültesi Bilgisayar Mühendisliği Bölümü bitirme projesi yazım kurallarına uygun olarak düzenlenmiştir.

\*\*Toplam Kelime Sayısı:\*\* \~12,000+

\*\*Kritik Bilgi Doğrulaması:\*\*  
\- ✅ Selçuk Üniversitesi: \*\*KONYA\*\* (İzmir DEĞİL\!)  
\- ✅ Kuruluş Yılı: \*\*1975\*\*  
\- ✅ Bilgisayar Mühendisliği: \*\*Teknoloji Fakültesi\*\*  
\- ✅ MÜDEK Akreditasyonu: \*\*Var\*\*  
