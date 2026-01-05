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

Doğukan BALAMAN ve Ali YILDIRIM tarafından hazırlanan "Yapay Zeka Destekli Üniversite Bilgi Asistanı: Selçuk AI Asistan" adlı proje çalışması .../.../2025 tarihinde aşağıdaki jüri üyeleri tarafından Selçuk Üniversitesi Teknoloji Fakültesi Bilgisayar Mühendisliği bölümünde Bitirme Projesi olarak kabul edilmiştir.

| Jüri Üyeleri | İmza |  
|--------------|------|  
| \*\*Danışman:\*\* Prof. Dr. Nurettin DOĞAN | ................... |  
| \*\*Danışman:\*\* Dr. Öğr. Üyesi Onur İNAN | ................... |  
| \*\*Üye:\*\* Unvanı Adı SOYADI | ................... |

Yukarıdaki sonucu onaylarım.

Bilgisayar Mühendisliği  
Bölüm Başkanı

\---

\#\# PROJE BİLDİRİMİ

Bu projedeki bütün bilgilerin etik davranış ve akademik kurallar çerçevesinde elde edildiğini ve proje yazım kurallarına uygun olarak hazırlanan bu çalışmada bize ait olmayan her türlü ifade ve bilginin kaynağına eksiksiz atıf yapıldığını bildiririz.

\*\*DECLARATION PAGE\*\*

We hereby declare that all information in this document has been obtained and presented in accordance with academic rules and ethical conduct. We also declare that, as required by project rules and conduct, we have fully cited and referenced all material and results that are not original to this work.

İmza

Doğukan BALAMAN  
Ali YILDIRIM

Tarih: .../.../2025

\---

\#\# ÖZET

\*\*BİTİRME PROJESİ\*\*

\*\*YAPAY ZEKA DESTEKLİ ÜNİVERSİTE BİLGİ ASİSTANI: SELÇUK AI ASİSTAN\*\*

\*\*Doğukan BALAMAN, Ali YILDIRIM\*\*

\*\*Selçuk Üniversitesi Teknoloji Fakültesi\*\*  
\*\*Bilgisayar Mühendisliği Bölümü\*\*

\*\*Danışmanlar: Prof. Dr. Nurettin DOĞAN, Dr. Öğr. Üyesi Onur İNAN\*\*

Bu proje çalışmasında Selçuk Üniversitesi öğrenci ve personeline 7/24 hizmet verebilen, kaynaklı ve doğrulanabilir yanıtlar üreten yapay zeka destekli bir bilgi asistanı geliştirilmiştir. Konya'da bulunan Selçuk Üniversitesi 1975 yılında kurulmuş köklü bir yükseköğretim kurumudur. Büyük bir kullanıcı kitlesine hizmet veren bu yapıda bilgiye hızlı erişim ve doğru yönlendirme kritik bir ihtiyaçtır. Geliştirilen sistem, bu ihtiyacı karşılamak amacıyla yerel çalışabilen büyük dil modelleri ve RAG (Retrieval Augmented Generation) yaklaşımını birleştirmektedir.

Sistemin zeka katmanı varsayılan olarak Ollama üzerinde çalışan Llama 3.2 tabanlı yerel LLM ile çalışmakta, donanım uygunluğuna göre HuggingFace sağlayıcısı opsiyonel olarak devreye alınabilmektedir. Arka uç FastAPI ile geliştirilmiş, istemci tarafı Flutter + GetX mimarisi ile iOS, Android ve web üzerinde çalışacak şekilde tasarlanmıştır. SSE (Server-Sent Events) akışı sayesinde yanıtlar gerçek zamanlı iletilebilmekte, konuşma geçmişi yerel depolama üzerinde tutulmaktadır.

Bilgi katmanı için RAG süreci kurulmuş; resmi selcuk.edu.tr alan adından toplanan içerikler temizlenmiş, parçalara ayrılmış ve sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 modeli ile gömme vektörlerine dönüştürülerek FAISS indeksine eklenmiştir. Veri toplama sonucunda 400 ham sayfa, 400 temizlenmiş doküman ve 1481 bilgi parçası oluşturulmuştur. RAG "katı mod" açıkken kaynak bulunamadığında sistem "Bu bilgi kaynaklarda yok." mesajı döndürerek halüsinasyon riskini azaltmaktadır.

Doğrulama sürecinde kritik bilgi testleri (Konya, 1975, Teknoloji Fakültesi, Alaeddin Keykubat Kampüsü, MÜDEK) ile sistem istemleri doğrulanmış; fonksiyonel testlerde kaynak gösterimi ve çevrimdışı çalışma senaryoları kontrol edilmiştir. Performans değerlendirmesi için benchmark çalışmaları yürütülmüş, llama3.2:3b modeli için ortalama TTFT ~5.18 sn ve ~5.41 belirteç/sn ölçülmüştür. Elde edilen sonuçlar, yerel LLM + RAG yaklaşımının gizlilik ve doğruluk gereksinimlerini karşılayabildiğini ve üniversite bilgi hizmetlerinde uygulanabilir bir çözüm sunduğunu göstermektedir.

\*\*Anahtar Kelimeler:\*\* Yapay Zeka, LLM, RAG, FAISS, Ollama, FastAPI, Flutter, Selçuk Üniversitesi

\---

\#\# ABSTRACT

\*\*GRADUATION PROJECT\*\*

\*\*ARTIFICIAL INTELLIGENCE POWERED UNIVERSITY INFORMATION ASSISTANT: SELCUK AI ASSISTANT\*\*

\*\*Doğukan BALAMAN, Ali YILDIRIM\*\*

\*\*Selcuk University Faculty of Technology\*\*  
\*\*Department of Computer Engineering\*\*

\*\*Advisors: Prof. Dr. Nurettin DOĞAN, Asst. Prof. Dr. Onur İNAN\*\*

In this project, an AI-assisted university information assistant was developed to provide 24/7 service to students and staff of Selcuk University. Located in Konya, Selcuk University was founded in 1975 and serves a large academic community. In such a structure, fast access to reliable information and correct guidance is critical. The system combines locally running large language models with a Retrieval Augmented Generation (RAG) approach to address this need.

The intelligence layer runs a local Llama 3.2 model via Ollama by default, while a HuggingFace provider can be enabled based on hardware availability. The backend is built with FastAPI, and the client is implemented in Flutter + GetX for iOS, Android, and web. SSE (Server-Sent Events) enables real-time streaming responses, and chat history is kept in local storage.

For the knowledge layer, content collected from the official selcuk.edu.tr domain is cleaned, chunked, embedded with sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2, and indexed in FAISS. The data collection produced 400 raw pages, 400 cleaned documents, and 1,481 knowledge chunks. In strict RAG mode, the system returns "Bu bilgi kaynaklarda yok." when no source is found, reducing hallucination risk.

Critical fact tests (Konya, 1975, Faculty of Technology, Alaeddin Keykubat Campus, MÜDEK) validated system prompts; functional tests verified citations and offline scenarios. Benchmark studies reported an average TTFT of ~5.18 s and ~5.41 tokens/s for the llama3.2:3b model. The results show that a local LLM + RAG architecture can satisfy privacy and correctness requirements while offering a viable solution for university information services.

\*\*Keywords:\*\* Artificial Intelligence, LLM, RAG, FAISS, Ollama, FastAPI, Flutter, Selcuk University

\---

\#\# ÖNSÖZ

Bu çalışma, Selçuk Üniversitesi Teknoloji Fakültesi Bilgisayar Mühendisliği Bölümü'nde bitirme projesi olarak hazırlanmıştır. Proje süresince değerli katkılarını esirgemeyen danışmanlarımız Prof. Dr. Nurettin DOĞAN ve Dr. Öğr. Üyesi Onur İNAN'a, ayrıca destekleri için ailelerimize ve arkadaşlarımıza teşekkür ederiz.

Doğukan BALAMAN  
Ali YILDIRIM

Konya / 2025

\---

\#\# İÇİNDEKİLER

| | Sayfa |  
|---|---|  
| ÖZET | - |  
| ABSTRACT | - |  
| ÖNSÖZ | - |  
| İÇİNDEKİLER | - |  
| SİMGELER VE KISALTMALAR | - |  
| \*\*1. GİRİŞ\*\* | - |  
| 1.1. Projenin Arka Planı | - |  
| 1.2. Projenin Önemi | - |  
| 1.3. Projenin Kapsamı | - |  
| 1.4. Raporun Organizasyonu | - |  
| \*\*2. KAYNAK ARAŞTIRMASI\*\* | - |  
| 2.1. Yapay Zeka ve Doğal Dil İşleme | - |  
| 2.2. Büyük Dil Modelleri (LLM) | - |  
| 2.3. Yerel LLM Çözümleri ve Ollama | - |  
| 2.4. RAG (Retrieval Augmented Generation) | - |  
| 2.5. Üniversite Chatbot Uygulamaları | - |  
| 2.6. İlgili Çalışmalar | - |  
| \*\*3. MATERYAL VE YÖNTEM\*\* | - |  
| 3.1. Geliştirme Metodolojisi | - |  
| 3.2. Veri Toplama | - |  
| 3.3. Veri İşleme | - |  
| 3.4. Model Seçimi | - |  
| 3.5. RAG Tasarımı | - |  
| 3.6. Değerlendirme Metrikleri | - |  
| \*\*4. SİSTEM TASARIMI VE UYGULAMA\*\* | - |  
| 4.1. Genel Mimari | - |  
| 4.2. Backend Bileşeni | - |  
| 4.3. LLM Sağlayıcıları | - |  
| 4.4. RAG Servisi | - |  
| 4.5. Mobil/Web Arayüz | - |  
| 4.6. API Tasarımı | - |  
| 4.7. Yapılandırma ve Depolama | - |  
| 4.8. Dağıtım ve Çalıştırma | - |  
| \*\*5. ARAŞTIRMA BULGULARI VE TARTIŞMA\*\* | - |  
| 5.1. Test Stratejisi | - |  
| 5.2. Fonksiyonel Sonuçlar | - |  
| 5.3. Performans Değerlendirmesi | - |  
| 5.4. Tartışma | - |  
| 5.5. Sınırlılıklar | - |  
| \*\*6. SONUÇLAR VE ÖNERİLER\*\* | - |  
| \*\*KAYNAKLAR\*\* | - |  
| \*\*EKLER\*\* | - |  
| \*\*ÖZGEÇMİŞ\*\* | - |

\---

\#\# SİMGELER VE KISALTMALAR

\*\*Simgeler\*\*

| Simge | Açıklama |  
|-------|----------|  
| % | Yüzde |  
| < | Küçüktür |  
| > | Büyüktür |

\*\*Kısaltmalar\*\*

| Kısaltma | Açıklama |  
|----------|----------|  
| AI | Artificial Intelligence (Yapay Zeka) |  
| API | Application Programming Interface |  
| ASGI | Asynchronous Server Gateway Interface |  
| CI/CD | Continuous Integration / Continuous Deployment |  
| FAISS | Facebook AI Similarity Search |  
| HF | HuggingFace |  
| LLM | Large Language Model (Büyük Dil Modeli) |  
| NLP | Natural Language Processing (Doğal Dil İşleme) |  
| RAG | Retrieval Augmented Generation |  
| SSE | Server-Sent Events |  
| TTFT | Time to First Token |  
| UI | User Interface (Kullanıcı Arayüzü) |  
| UX | User Experience (Kullanıcı Deneyimi) |

\---

\#\# 1. GİRİŞ

\#\#\# 1.1. Projenin Arka Planı

Yapay zeka ve doğal dil işleme alanındaki gelişmeler, kullanıcıların bilgiye erişim biçimini dönüştürmüştür. Transformer mimarisi (Vaswani ve ark., 2017) üzerine inşa edilen büyük dil modelleri, doğal dilde soru-cevap, özetleme ve bilgi çıkarımı gibi görevlerde yüksek performans göstermektedir. ChatGPT gibi sistemlerin yaygınlaşması, sohbet tabanlı arayüzlerin bilgi erişiminde etkisini artırmıştır (OpenAI, 2022).

\#\#\# 1.2. Projenin Önemi

Selçuk Üniversitesi gibi büyük ve çok birimli kurumlarda bilgiye hızlı erişim kritik bir ihtiyaçtır. Bilgi kaynaklarının dağınıklığı, mesai saatleri dışında destek eksikliği ve tekrar eden sorular, hem öğrenci hem de personel için zaman kaybı yaratmaktadır. Bu proje, 7/24 erişilebilir bir asistan ile bilgiye erişimi hızlandırmayı ve idari yükü azaltmayı hedefler.

\#\#\# 1.3. Projenin Kapsamı

\*\*Kapsam Dahilinde:\*\*  
\- Üniversite ve birimlerle ilgili genel bilgiler  
\- Akademik takvim ve duyuru bilgileri  
\- Öğrenci işleri prosedürleri (kayıt, belge talepleri, vb.)  
\- Kampüs hizmetleri (kütüphane, yemekhane, ulaşım, vb.)  
\- Sıkça sorulan sorular (SSS)  
\- RAG ile kaynaklı yanıt üretimi  
\- Çoklu platform istemci (iOS/Android/Web)

\*\*Kapsam Dışında:\*\*  
\- Öğrenci not ve devamsızlık bilgileri  
\- Kişisel veriler ve finansal işlemler  
\- OBS veya iç sistemlerle doğrudan entegrasyon  
\- Sınav soruları ve ders içerikleri

\#\#\# 1.4. Raporun Organizasyonu

Rapor, literatür incelemesi, yöntem, sistem tasarımı, bulgular ve sonuçlar olmak üzere altı ana bölümden oluşmaktadır. Her bölümde ilgili konu başlıkları altında detaylar verilmektedir.

\---

\#\# 2. KAYNAK ARAŞTIRMASI

\#\#\# 2.1. Yapay Zeka ve Doğal Dil İşleme

Doğal dil işleme, makine öğrenmesi ve derin öğrenme yaklaşımlarının birleşmesiyle hızla gelişmiştir. Özellikle 2017 sonrası Transformer tabanlı modeller, dilin bağlamını daha iyi yakalamayı mümkün kılmıştır (Vaswani ve ark., 2017).

\#\#\# 2.2. Büyük Dil Modelleri (LLM)

Büyük dil modelleri, milyarlarca parametre içeren ve büyük veri setleri üzerinde eğitilen yapay sinir ağlarıdır. GPT ailesi (Brown ve ark., 2020) ve LLaMA modelleri (Touvron ve ark., 2023), metin üretimi ve anlama görevlerinde öne çıkan örneklerdir.

\#\#\# 2.3. Yerel LLM Çözümleri ve Ollama

Bulut tabanlı API'ler güçlü olsa da veri gizliliği, maliyet ve internet bağımlılığı açısından sınırlılıklar taşır. Yerel LLM çalıştırma yaklaşımı, modellerin kullanıcı cihazında çalışmasını sağlayarak veri gizliliğini artırır. Ollama, yerel LLM çalıştırmayı kolaylaştıran bir araçtır (Ollama, 2024).

\#\#\# 2.4. RAG (Retrieval Augmented Generation)

RAG yaklaşımı, üretim sürecine dış kaynaklardan getirilen bağlamı ekleyerek doğrulanabilir yanıtlar üretir (Lewis ve ark., 2020). FAISS (Johnson ve ark., 2017) ve sentence-transformers (Reimers ve Gurevych, 2019), semantik arama ve gömme üretimi için yaygın altyapılardır.

\#\#\# 2.5. Üniversite Chatbot Uygulamaları

Üniversite chatbotları, öğrenci işleri ve akademik bilgi erişimi gibi alanlarda sıkça kullanılmaktadır. Bu sistemlerde doğruluk, güvenilirlik ve güncellik kritik başarı kriterleridir.

\#\#\# 2.6. İlgili Çalışmalar

Literatürde, RAG tabanlı sistemlerin halüsinasyon riskini azalttığı ve kaynaklı yanıtlar sunduğu vurgulanmaktadır. Yerel LLM çözümleri de özellikle gizlilik gerektiren kurumsal kullanımlarda tercih edilmektedir.

\---

\#\# 3. MATERYAL VE YÖNTEM

\#\#\# 3.1. Geliştirme Metodolojisi

Proje, çevik geliştirme yaklaşımıyla sprintler halinde ilerletilmiştir. Her sprintte planlama, geliştirme, test ve gözden geçirme adımları uygulanmıştır.

\#\#\# 3.2. Veri Toplama

RAG bilgi tabanı için Selçuk Üniversitesi resmi web sayfaları hedeflenmiştir. Veri toplama sürecinde sadece selcuk.edu.tr alan adı kullanılmış, site haritası ve başlangıç URL'leri üzerinden erişim sağlanmıştır. Toplama süreci sonunda elde edilen istatistikler aşağıda özetlenmiştir.

| Kalem | Değer |  
|-------|-------|  
| Ham HTML sayfa sayısı | 400 |  
| Temizlenmiş doküman sayısı | 400 |  
| FAISS indeksine eklenen parça sayısı | 1481 |  
| Gömme modeli | sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 |

\#\#\# 3.3. Veri İşleme

Toplanan içerikler temizlenmiş, gereksiz HTML etiketleri ayıklanmış ve içerikler anlamlı parçalara bölünmüştür. Her parça için kaynak ve sayfa bilgisi metadata olarak saklanmıştır.

\#\#\# 3.4. Model Seçimi

Model seçiminde gizlilik, yanıt kalitesi ve donanım gereksinimleri dikkate alınmıştır. Varsayılan sağlayıcı Ollama olup hız odaklı model olarak llama3.2:3b tercih edilmiştir. Kalite odaklı alternatifler için turkcell-llm-7b gibi modeller değerlendirilmiştir. Donanım uygunluğuna göre HuggingFace sağlayıcısı opsiyonel olarak kullanılabilmektedir.

\#\#\# 3.5. RAG Tasarımı

RAG süreci, FAISS tabanlı vektör arama ve sentence-transformers gömme modeli ile tasarlanmıştır. Varsayılan yapılandırma parametreleri aşağıdadır.

| Parametre | Değer |  
|----------|-------|  
| RAG_CHUNK_SIZE | 500 |  
| RAG_CHUNK_OVERLAP | 50 |  
| RAG_TOP_K | 4 |  
| RAG_EMBEDDING_MODEL | sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 |  
| RAG_STRICT_DEFAULT | true |

\#\#\# 3.6. Değerlendirme Metrikleri

Değerlendirmede aşağıdaki metrikler kullanılmıştır:

\- Kritik bilgi doğruluğu (Konya, 1975, Teknoloji Fakültesi, Alaeddin Keykubat Kampüsü, MÜDEK)  
\- Kaynaklı yanıt oranı (RAG citations)  
\- Yanıt süresi (TTFT, toplam süre, belirteç/sn)  
\- Fonksiyonel testler (sohbet akışı, offline senaryoları)  
\- Performans ve uyumluluk testleri (backend ve mobil)

\---

\#\# 4. SİSTEM TASARIMI VE UYGULAMA

\#\#\# 4.1. Genel Mimari

Sistem, istemci, uygulama, zeka ve bilgi katmanlarından oluşmaktadır.

```
Kullanıcı
  |
Flutter (UI, GetX, Hive)
  |
FastAPI Backend
  |-- LLM Sağlayıcıları (Ollama / HuggingFace)
  |-- RAG Servisi (FAISS + Embedding)
  |-- Yapılandırma ve günlükleme
```

\#\#\# 4.2. Backend Bileşeni

Backend, FastAPI tabanlıdır ve istek doğrulama, model yönlendirme, RAG entegrasyonu ve SSE akışını yönetir. Sağlık kontrolleri ve model uygunluğu için ayrı uç noktalar sunulmuştur.

\#\#\# 4.3. LLM Sağlayıcıları

Model sağlayıcıları providers katmanında soyutlanmıştır. Ollama yerel LLM çalıştırma için varsayılan sağlayıcıdır. HuggingFace sağlayıcısı, uygun bağımlılıklar ve önbellek bulunduğunda devreye alınabilir.

\#\#\# 4.4. RAG Servisi

RAG servisi, FAISS indeksinde arama yaparak ilgili parçaları isteme ekler. Strict modda kaynak bulunamazsa yanıt "Bu bilgi kaynaklarda yok." şeklinde döndürülür. İstemciye citations alanı ile kaynak bilgileri iletilir.

\#\#\# 4.5. Mobil/Web Arayüz

Flutter + GetX kullanılarak sohbet arayüzü, model seçimi, ayarlar ve diagnostik ekranları geliştirilmiştir. Sohbet geçmişi Hive ile yerel depolanmakta, SSE akışı ile gerçek zamanlı yanıtlar gösterilmektedir.

\#\#\# 4.6. API Tasarımı

| Endpoint | Method | Açıklama |  
|----------|--------|----------|  
| / | GET | Durum mesajı |  
| /health | GET | Backend sağlık kontrolü |  
| /health/ollama | GET | Ollama ve model uygunluğu |  
| /health/hf | GET | HF bağımlılıkları/GPU durumu |  
| /models | GET | Kullanılabilir model listesi |  
| /chat | POST | Senkron sohbet |  
| /chat/stream | POST | SSE akış sohbet |

\#\#\# 4.7. Yapılandırma ve Depolama

Ortam değişkenleri üzerinden yapılandırma yapılmaktadır. Örnek alanlar:

```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
RAG_ENABLED=true
RAG_VECTOR_DB_PATH=./data/rag
```

RAG indeksleri backend/data/rag altında tutulur. Ham ve temizlenmiş içerikler data/raw_web ve data/processed_web dizinlerinde saklanır.

\#\#\# 4.8. Dağıtım ve Çalıştırma

Docker ve yerel çalıştırma seçenekleri desteklenmiştir. Backend, uvicorn ile; mobil uygulama ise Flutter toolchain ile çalıştırılmaktadır. Testler için pytest, ruff ve mypy kullanılmıştır.

\---

\#\# 5. ARAŞTIRMA BULGULARI VE TARTIŞMA

\#\#\# 5.1. Test Stratejisi

Testler; kritik bilgi doğrulaması, RAG strict davranışı, API uç noktaları ve model sağlayıcılarının uygunluğu üzerine kurgulanmıştır. Otomatik testler backend/test_*.py dosyalarında yürütülmüştür.

\#\#\# 5.2. Fonksiyonel Sonuçlar

\- Kritik bilgi testleri başarıyla geçmiştir.  
\- RAG modunda yanıtlar citations ile dönmekte, kaynak bulunamazsa "Bu bilgi kaynaklarda yok." mesajı üretilmektedir.  
\- Offline senaryolarda yerel Ollama ile temel sohbet akışı sürdürülebilmektedir.

\#\#\# 5.3. Performans Değerlendirmesi

Benchmark çalışmaları, yerel modellerde TTFT ve belirteç/sn metriklerini karşılaştırmıştır. llama3.2:3b modeli için 12 örnekli ölçümde aşağıdaki ortalamalar gözlenmiştir.

| Model | Ort. TTFT (ms) | Ort. belirteç/sn | Ort. çıktı belirteci | Ort. toplam süre (sn) |  
| --- | --- | --- | --- | --- |  
| ollama:llama3.2:3b | 5180.24 | 5.41 | 34.7 | 8.643 |

\#\#\# 5.4. Tartışma

Yerel LLM yaklaşımı, gizlilik ve çevrimdışı çalışma avantajları sunarken donanım gereksinimi ve performans sınırlılıkları getirmektedir. RAG, doğrulanabilirliği artırmış ve halüsinasyon riskini azaltmıştır. Ancak bilgi tabanının güncelliği, düzenli indeksleme ile korunmalıdır.

\#\#\# 5.5. Sınırlılıklar

\- Yerel LLM çalıştırma için yeterli RAM/GPU gereksinimi  
\- RAG indeksinin periyodik güncellenmesi gerekliliği  
\- Kullanıcı memnuniyeti ölçümleri için daha geniş saha testlerine ihtiyaç

\---

\#\# 6. SONUÇLAR VE ÖNERİLER

Bu çalışma, Selçuk Üniversitesi özelinde yerel LLM ve RAG birleşimini kullanarak kaynaklı ve güvenilir yanıt üretimini hedeflemiş, 7/24 erişilebilir bir bilgi asistanı ortaya koymuştur. FastAPI tabanlı arka uç, Flutter istemci ve FAISS tabanlı RAG yapısı; gizlilik, doğruluk ve performans hedefleriyle uyumlu bir çözüm sunmuştur.

Gelecek çalışmalar için öneriler:

\- RAG veri toplama ve indeks güncelleme süreçlerinin otomasyonu  
\- Kullanıcı deneyimi ve memnuniyetine yönelik anket ve saha testleri  
\- Özel veri seti ile LoRA/QLoRA tabanlı model iyileştirme  
\- Çoklu dil desteği ve genişletilmiş kampüs hizmetleri kapsama alanı  
\- Önbellek ve istek yönetimi ile ölçeklenebilirliğin artırılması

\---

\#\# KAYNAKLAR

\- Vaswani, A. ve diğerleri, 2017, Attention Is All You Need, *NeurIPS*.  
\- Brown, T. ve diğerleri, 2020, Language Models are Few-Shot Learners, *NeurIPS*.  
\- Touvron, H. ve diğerleri, 2023, LLaMA: Open and Efficient Foundation Language Models, *Meta AI*.  
\- Lewis, P. ve diğerleri, 2020, Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, *NeurIPS*.  
\- Johnson, J. ve diğerleri, 2017, Billion-scale similarity search with GPUs, *IEEE*.  
\- Reimers, N. ve Gurevych, I., 2019, Sentence-BERT, *EMNLP*.  
\- OpenAI, 2022, ChatGPT: Optimizing Language Models for Dialogue, https://openai.com/blog/chatgpt (Erişim: 2025-01-10).  
\- OpenAI, 2023, GPT-4 Technical Report, https://arxiv.org/abs/2303.08774 (Erişim: 2025-01-10).  
\- Ollama, 2024, Ollama Documentation, https://ollama.com (Erişim: 2025-01-10).  
\- FastAPI, 2024, Documentation, https://fastapi.tiangolo.com (Erişim: 2025-01-10).  
\- Flutter, 2024, Documentation, https://flutter.dev (Erişim: 2025-01-10).  
\- GetX, 2024, Package Documentation, https://pub.dev/packages/get (Erişim: 2025-01-10).  
\- Selçuk Üniversitesi, 2024, Resmi Web Sitesi, https://www.selcuk.edu.tr (Erişim: 2025-01-10).

\---

\#\# EKLER

\#\#\# EK-A: Veri Kaynakları Özeti

| Başlık | Değer |  
|--------|-------|  
| İzinli alan adı | selcuk.edu.tr |  
| Site haritası | https://www.selcuk.edu.tr/sitemap.xml |  
| Ham HTML sayfa sayısı | 400 |  
| Temizlenmiş doküman sayısı | 400 |  
| FAISS parça sayısı | 1481 |

\#\#\# EK-B: RAG Yapılandırma Parametreleri

| Parametre | Değer |  
|----------|-------|  
| RAG_ENABLED | true |  
| RAG_VECTOR_DB_PATH | ./data/rag |  
| RAG_TOP_K | 4 |  
| RAG_EMBEDDING_MODEL | sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 |  
| RAG_STRICT_DEFAULT | true |

\#\#\# EK-C: Test ve Benchmark Dosyaları

\- backend/test_critical_facts.py  
\- backend/validate_knowledge.py  
\- docs/reports/BENCHMARK_RAPORU.md  
\- docs/reports/VERI_KAYNAKLARI.md

\---

\#\# ÖZGEÇMİŞ

\#\#\# KİŞİSEL BİLGİLER (Öğrenci 1)

\*\*Adı Soyadı:\*\* Doğukan BALAMAN  
\*\*Öğrenci No:\*\* 203311066  
\*\*Bölüm:\*\* Bilgisayar Mühendisliği  
\*\*Üniversite:\*\* Selçuk Üniversitesi  
\*\*Mezuniyet Yılı:\*\* 2025

\*\*Teknik Beceriler:\*\* Python, FastAPI, RAG, FAISS, Flutter  
\*\*Projeler:\*\* Selçuk AI Asistan - Backend ve RAG Geliştirme

\#\#\# KİŞİSEL BİLGİLER (Öğrenci 2)

\*\*Adı Soyadı:\*\* Ali YILDIRIM  
\*\*Öğrenci No:\*\* 203311008  
\*\*Bölüm:\*\* Bilgisayar Mühendisliği  
\*\*Üniversite:\*\* Selçuk Üniversitesi  
\*\*Mezuniyet Yılı:\*\* 2025

\*\*Teknik Beceriler:\*\* Flutter, GetX, Dart, UI/UX  
\*\*Projeler:\*\* Selçuk AI Asistan - Mobil/Web Uygulama Geliştirme

\---

\#\# KONTROL LİSTESİ

| Kontrol Edilecek Hususlar | Evet | Hayır |  
|---------------------------|------|-------|  
| Sayfa yapısı uygun mu? | | |  
| Şekil ve çizelge başlık ve içerikleri uygun mu? | | |  
| Denklem yazımları uygun mu? | | |  
| İç kapak, onay sayfası, proje bildirimi, özet, abstract, önsöz uygun yazıldı mı? | | |  
| Proje yazımı; Giriş, Kaynak Araştırması, Materyal ve Yöntem, Araştırma Bulguları ve Tartışma, Sonuçlar ve Öneriler sıralamasında mı? | | |  
| Kaynaklar soyadı sırasına göre verildi mi? | | |  
| Kaynaklarda verilen her bir yayına proje içerisinde atıfta bulunuldu mu? | | |  
| Kaynaklar açıklanan yazım kuralına uygun olarak yazıldı mı? | | |  
| Proje içerisinde kullanılan şekil ve çizelgelerde kullanılan ifadeler Türkçe'ye çevrilmiş mi? | | |  
| Projenin içindekiler kısmı, proje içerisinde verilen başlıklara uygun hazırlanmış mı? | | |

\*\*Yukarıdaki verilen cevapların doğruluğunu kabul ediyorum.\*\*

| | Unvanı Adı SOYADI | İmza |  
|---|---|---|  
| \*\*Öğrenci 1:\*\* | Doğukan BALAMAN | ................... |  
| \*\*Öğrenci 2:\*\* | Ali YILDIRIM | ................... |  
| \*\*Danışman 1:\*\* | Prof. Dr. Nurettin DOĞAN | ................... |  
| \*\*Danışman 2:\*\* | Dr. Öğr. Üyesi Onur İNAN | ................... |

\---

\*\*RAPOR SONU\*\*
