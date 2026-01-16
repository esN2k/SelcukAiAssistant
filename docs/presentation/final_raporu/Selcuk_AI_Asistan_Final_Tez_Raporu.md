

|  |  |
| :---: | :---- |
| **T.C. SELÇUK ÜNİVERSİTESİ TEKNOLOJİ FAKÜLTESİBİLGİSAYAR MÜHENDİSLİĞİ**  |  |
| **YAPAY ZEKA DESTEKLİ ÜNİVERSİTE BİLGİ ASİSTANI  SELÇUK AI ASİSTAN  Doğukan BALAMAN (203311066) Ali YILDIRIM (203311008) BİLGİSAYAR MÜHENDİSLİĞİ UYGULAMALARI**  |  |
| **01-2025** **KONYA Her Hakkı Saklıdır** |  |

**PROJE KABUL VE ONAYI**

................................. tarafından hazırlanan “…………………………………..” adlı proje çalışması …/…/… tarihinde aşağıdaki jüri üyeleri tarafından oy birliği/oy çokluğu ile Selçuk Üniversitesi Teknoloji Fakültesi Bilgisayar Mühendisliği bölümünde Bilgisayar Mühendisliği Uygulamaları Projesi olarak kabul edilmiştir.

| Jüri Üyeleri | İmza |
| :---- | :---: |
| **Danışman** Prof. Dr. Nurettin DOĞAN **Danışman** Dr. Öğr. Üyesi Onur İNAN |  |
| **Üye** PROF. DR. HUMAR KAHRAMANLI ÖRNEK |  |
| **Üye** Dr. Öğr. Üyesi Selahattin ALAN |  |

| Yukarıdaki sonucu onaylarım. |
| :---: |
| Bilgisayar Mühendisliği Bölüm Başkanı |

**PROJE BİLDİRİMİ**

Bu projedeki bütün bilgilerin etik davranış ve akademik kurallar çerçevesinde elde edildiğini ve proje yazım kurallarına uygun olarak hazırlanan bu çalışmada bana ait olmayan her türlü ifade ve bilginin kaynağına eksiksiz atıf yapıldığını bildiririm.

**DECLARATION PAGE**

I hereby declare that all information in this document has been obtained and presented in accordance with academic rules and ethical conduct. I also declare that, as required by project rules and conduct, I have fully cited and referenced all material and results that are not original to this work.

| İmza | İmza |
| :---: | :---: |
| Doğukan BALAMAN | Ali YILDIRIM |
| Tarih: …./…./…. | Tarih: …./…./…. |

**ÖZET**

**BİLGİSAYAR MÜHENDİSLİĞİ UYGULAMALARI PROJESİ**

**YAPAY ZEKA DESTEKLİ ÜNİVERSİTE BİLGİ ASİSTANI: SELÇUK AI ASİSTAN**

**Doğukan BALAMAN (203311066)**  
**Ali YILDIRIM (203311008)**

**SELÇUK ÜNİVERSİTESİ**   
**TEKNOLOJİ FAKÜLTESİ**  
**BİLGİSAYAR MÜHENDİSLİĞİ BÖLÜMÜ**

**Danışman: Prof. Dr. Nurettin DOĞAN**  
**Danışman: Dr. Öğr. Üyesi Onur İNAN**

**2025, 27 Sayfa**

**Jüri**  
**Prof. Dr. Nurettin DOĞAN**  
**Dr. Öğr. Üyesi Onur İNAN**  
**Prof. Dr. Humar KAHRAMANLI ÖRNEK**  
**Dr. Öğr. Üyesi Selahattin ALAN**

Bu proje çalışmasında, Selçuk Üniversitesi öğrenci ve personeline 7/24 hizmet verebilen, yapay zeka destekli bir bilgi asistanı geliştirilmiştir. Konya'da bulunan Selçuk Üniversitesi, Türkiye'nin en büyük üniversitelerinden biri olup 23 fakülte, 6 enstitü ve 20'den fazla meslek yüksekokulu ile yaklaşık 80.000 öğrenciye eğitim vermektedir. Bu denli büyük bir kurumda öğrencilerin ve personelin bilgiye hızlı erişimi kritik bir ihtiyaç haline gelmiştir.

Geliştirilen Selçuk AI Asistan, Büyük Dil Modelleri (Large Language Models \- LLM) ve Retrieval Augmented Generation (RAG) teknolojilerini kullanarak üniversite hakkında doğru ve güncel bilgiler sunmaktadır. Sistem, Python programlama dili ile geliştirilmiş backend servisleri ve Dart/Flutter ile geliştirilmiş mobil uygulama bileşenlerinden oluşmaktadır. Backend tarafında FastAPI framework'ü kullanılmış, RAG pipeline'ı için LangChain kütüphanesi ve FAISS vektör veritabanı entegre edilmiştir.

Proje kapsamında üniversitenin resmi web sitesinden ve kurumsal kaynaklardan derlenen bilgiler, yapılandırılmış bir knowledge base oluşturularak sisteme entegre edilmiştir. Bu sayede, yapay zeka modellerinin 'hallucination' (uydurma bilgi üretme) problemi minimize edilmiş ve kullanıcılara güvenilir yanıtlar sağlanmıştır. Sistem; akademik takvim, fakülte bilgileri, öğrenci işleri prosedürleri, kampüs hizmetleri ve sıkça sorulan sorular gibi konularda bilgi sağlamaktadır.

Yapılan testlerde sistemin %90 üzerinde doğruluk oranı ile yanıt verdiği ve ortalama yanıt süresinin 3 saniyenin altında kaldığı tespit edilmiştir. Bu çalışma, üniversitelerde dijital dönüşüm sürecine katkı sağlamakta ve yapay zeka teknolojilerinin eğitim kurumlarında etkin kullanımına örnek teşkil etmektedir.

Anahtar Kelimeler: Büyük Dil Modelleri, Chatbot, Doğal Dil İşleme, Flutter, RAG, Selçuk Üniversitesi, Yapay Zeka

**ABSTRACT**

**COMPUTER ENGINEERING APPLICATIONS PROJECT**

**ARTIFICIAL INTELLIGENCE POWERED UNIVERSITY INFORMATION ASSISTANT: SELCUK AI ASSISTANT**

**Doğukan BALAMAN (203311066)**  
**Ali YILDIRIM (203311008)**

**SELCUK UNIVERSITY**   
**FACULTY OF TECHNOLOGY**  
**DEPARTMENT OF COMPUTER ENGINEERING**

**Danışman: Prof. Dr. Nurettin DOĞAN**  
**Danışman: Dr. Öğr. Üyesi Onur İNAN**

**2025, 27 Sayfa**

**Jury**  
**Prof. Dr. Nurettin DOĞAN**  
**Dr. Öğr. Üyesi Onur İNAN**  
**Prof. Dr. Humar KAHRAMANLI ÖRNEK**  
**Dr. Öğr. Üyesi Selahattin ALAN**

In this project, an artificial intelligence-powered information assistant has been developed to provide 24/7 service to students and staff of Selcuk University. Located in Konya, Selcuk University is one of Turkey's largest universities, serving approximately 80,000 students through 23 faculties, 6 institutes, and more than 20 vocational schools. In such a large institution, quick access to information for students and staff has become a critical need.

The developed Selcuk AI Assistant provides accurate and up-to-date information about the university using Large Language Models (LLM) and Retrieval Augmented Generation (RAG) technologies. The system consists of backend services developed with Python and mobile application components developed with Dart/Flutter. FastAPI framework was used on the backend side, and LangChain library and FAISS vector database were integrated for the RAG pipeline.

Within the scope of the project, information compiled from the university's official website and institutional resources was integrated into the system by creating a structured knowledge base. This approach minimizes the 'hallucination' problem of AI models and provides reliable responses to users. The system provides information on topics such as academic calendar, faculty information, student affairs procedures, campus services, and frequently asked questions.

Tests have shown that the system responds with an accuracy rate of over 90% and an average response time of less than 3 seconds. This study contributes to the digital transformation process in universities and serves as an example of the effective use of artificial intelligence technologies in educational institutions.

Keywords: Artificial Intelligence, Chatbot, Flutter, Large Language Models, Natural Language Processing, RAG, Selcuk University

**ÖNSÖZ**

Bu proje çalışması, Selçuk Üniversitesi Teknoloji Fakültesi Bilgisayar Mühendisliği Bölümü'nde bitirme projesi olarak hazırlanmıştır. Çalışmanın amacı, yapay zeka teknolojilerini kullanarak üniversite topluluğuna faydalı bir bilgi asistanı geliştirmektir.

Proje süresince değerli katkılarını esirgemeyen danışman hocalarımız Prof. Dr. Nurettin DOĞAN ve Dr. Öğr. Üyesi Onur İNAN'a, teknik konularda yardımcı olan arkadaşlarımıza ve manevi desteklerini her zaman hissettiğimiz ailelerimize teşekkürlerimizi sunarız.

|  | Doğukan BALAMAN (203311066) Ali YILDIRIM (203311008) |
| :---: | :---: |
|  | Konya / 2025 |

**İÇİNDEKİLER**

[**ÖZET	iv**](#özet)

[**ABSTRACT	v**](#abstract)

[**ÖNSÖZ	vi**](#önsöz)

[**İÇİNDEKİLER	vii**](#i̇çi̇ndeki̇ler)

[**SİMGELER VE KISALTMALAR	iv**](#si̇mgeler-ve-kisaltmalar)

[**1\. GİRİŞ	1**](#heading=h.axb8gk2f2o4g)

[1.1. Birinci Bölüm İkinci Derece Başlık	1](#heading=h.3nmt7outqoyx)  
[1.1.1. Birinci bölüm üçüncü derece başlık	1](#heading=h.rtso072yhdi1)

**2\. KAYNAK ARAŞTIRMASI	2**

[2.1.](#heading=h.k5qvm09t7f0y) Yapay Zeka ve Doğal Dil İşleme	[2](#heading=h.k5qvm09t7f0y)  
     [2.2.](#heading=h.kv10dd53hzvd) Büyük Dil Modelleri	[2](#heading=h.kv10dd53hzvd)  
     [2.3.](#heading=h.kv10dd53hzvd) RAG (Retrieval Augmented Generation)	[2](#heading=h.kv10dd53hzvd)  
     [2.4.](#heading=h.kv10dd53hzvd) Mobil Uygulama Geliştirme ve Flutter	[2](#heading=h.kv10dd53hzvd)  
     2.5. Üniversite Chatbot Uygulamaları	[2](#heading=h.kv10dd53hzvd)  
     2.6. İlgili Çalışmalar	[2](#heading=h.kv10dd53hzvd)

[**3\. MATERYAL VE YÖNTEM	3**](#heading=h.gk93wr2type1)

3.1. Geliştirme Metodolojisi	[3](#heading=h.hd326fxbelm)  
     3.2. Veri Toplama	[3](#heading=h.7x2e6djap0xy)  
     3.3. Veri İşleme	[3](#heading=h.7x2e6djap0xy)  
     3.4. Model Seçimi	[3](#heading=h.7x2e6djap0xy)  
     3.5. RAG Pipeline Tasarımı	[3](#heading=h.7x2e6djap0xy)  
     3.6. Değerlendirme Metrikleri	[3](#heading=h.7x2e6djap0xy)

[**4\. SİSTEM TASARIMI VE UYGULAMA	5**](#heading=h.pomrz3jva4yl)

4.1. Genel Mimari	[5](#heading=h.kybrirjbk2si)  
     4.2. Backend Bileşeni	[5](#heading=h.2hq720ozw952)  
     4.3. Mobil Uygulama Bileşeni	[5](#heading=h.2hq720ozw952)  
     4.4. RAG Engine Bileşeni	[5](#heading=h.2hq720ozw952)  
     4.5. API Tasarımı	[5](#heading=h.2hq720ozw952)  
     4.6. Veritabanı ve Knowledge Base	[5](#heading=h.2hq720ozw952)  
     4.7. Güvenlik Tasarımı	[5](#heading=h.2hq720ozw952)  
     4.8. Test Stratejisi	[5](#heading=h.2hq720ozw952)  
     4.9. Test Senaryoları ve Sonuçları	[5](#heading=h.2hq720ozw952)  
     4.10. Performans Değerlendirmesi	[5](#heading=h.2hq720ozw952)  
     4.11. Karşılaşılan Zorluklar ve Çözümler	[5](#heading=h.2hq720ozw952)

[**5\. SONUÇLAR VE ÖNERİLER	6**](#heading=h.m3c2jl6amub4)

[5.1 Sonuçlar	6](#heading=h.w76hllby11j4)  
[5.2 Öneriler	6](#heading=h.kr4zycv0bork)

[**KAYNAKLAR	7**](#heading=h.k7pz15n79h5y)

[**EKLER	8**](#ekler)

[**ÖZGEÇMİŞ	10**](#özgeçmi̇ş)

**SİMGELER VE KISALTMALAR**

**Simgeler**

**Kısaltmalar**

API : Application Programming Interface (Uygulama Programlama Arayüzü)  
LLM : Large Language Model (Büyük Dil Modeli)  
RAG : Retrieval-Augmented Generation (Getirim Destekli Üretim)  
NLP : Natural Language Processing (Doğal Dil İşleme)  
UI : User Interface (Kullanıcı Arayüzü)  
JWT : JSON Web Token  
JSON : JavaScript Object Notation  
HTTP : Hypertext Transfer Protocol  
HTTPS : Hypertext Transfer Protocol Secure  
REST : Representational State Transfer  
SQL : Structured Query Language

**1\. GİRİŞ**

Yapay zeka teknolojileri, son yıllarda özellikle doğal dil işleme alanında büyük gelişmeler kaydetmiştir. 2017 yılında Google araştırmacıları tarafından geliştirilen Transformer mimarisi (Vaswani ve ark., 2017), bu alandaki en önemli dönüm noktalarından birini oluşturmuştur. Bu mimari üzerine inşa edilen GPT (Generative Pre-trained Transformer) serisi modeller, insan benzeri metin üretme ve anlama yetenekleriyle dikkat çekmiştir.

OpenAI tarafından 2022 yılında kullanıma sunulan ChatGPT, yapay zeka destekli sohbet robotlarının potansiyelini geniş kitlelere göstermiştir (OpenAI, 2022). Bu gelişme, eğitim kurumları dahil birçok sektörde yapay zeka uygulamalarına olan ilgiyi artırmıştır. Üniversiteler, öğrenci hizmetlerini iyileştirmek ve bilgiye erişimi kolaylaştırmak amacıyla bu teknolojileri kullanmaya başlamıştır.

Türkiye'de yükseköğretim kurumları, dijital dönüşüm sürecinde önemli adımlar atmaktadır. Yükseköğretim Kurulu (YÖK) tarafından desteklenen dijitalleşme çalışmaları, üniversitelerin teknoloji kullanımını teşvik etmektedir. Bu bağlamda, yapay zeka destekli asistanlar, öğrenci memnuniyetini artırma ve idari yükü azaltma potansiyeli taşımaktadır.

Selçuk Üniversitesi, 1975 yılında Konya'da kurulan ve Türkiye'nin en köklü üniversitelerinden biridir. Günümüzde 23 fakülte, 6 enstitü, 4 yüksekokul ve 21 meslek yüksekokulu ile yaklaşık 80.000 öğrenciye hizmet vermektedir (Selçuk Üniversitesi, 2024). Bu denli büyük bir kurumda, öğrencilerin ve personelin bilgiye hızlı ve doğru şekilde erişmesi kritik bir ihtiyaçtır.

Mobil teknolojilerin yaygınlaşması ile birlikte, kullanıcıların bilgiye erişim alışkanlıkları da değişmiştir. Günümüzde öğrencilerin büyük çoğunluğu akıllı telefon kullanmakta ve bilgiye mobil cihazlar üzerinden erişmeyi tercih etmektedir. Bu nedenle, geliştirilen sistemin hem web hem de mobil platformlarda erişilebilir olması önem taşımaktadır.

## **1.1. Projenin Arka Planı**

Son yıllarda yapay zekâ tabanlı dil modellerinin gelişmesiyle birlikte, eğitim süreçlerinde kişiselleştirilmiş destek sunabilen dijital asistanların kullanımı belirgin biçimde artmıştır. Özellikle üniversite öğrencileri; ders içeriklerini anlamlandırma, kaynak bulma, ödev/proje üretim sürecini planlama, yazım kurallarına uyum ve sınav takibi gibi konularda hızlı, erişilebilir ve güvenilir rehberliğe ihtiyaç duymaktadır. Bu ihtiyaçlar, klasik arama motorları veya statik dokümanlar ile her zaman etkin şekilde karşılanamamakta; öğrencinin bağlamına uygun, adım adım yönlendiren etkileşimli çözümler daha fazla önem kazanmaktadır.

Selçuk Üniversitesi Bilgisayar Mühendisliği öğrencilerinin bitirme/araştırma projeleri gibi süreçlerinde karşılaşılan en yaygın sorunlar; gereksinimlerin netleştirilememesi, şablon-yazım esaslarına uyumsuzluk, kaynakça düzeni hataları, zaman yönetimi ve raporlama formatında tutarsızlıklardır. Bu proje, söz konusu problemleri azaltmak amacıyla “Selçuk YZ Asistan (Selcuk AI Assistant)” yaklaşımıyla; öğrencinin hedeflerine göre yönlendirme yapabilen, yazım kurallarına uygun çıktı üretimini destekleyen ve proje sürecini parçalara ayırarak takip edilebilir hale getiren bir dijital asistan fikrinden doğmuştur.

Bu bağlamda projenin arka planı; (i) büyük dil modellerinin eğitimde danışman/rehber rolünü desteklemesi, (ii) üniversite proje dokümantasyonunun biçimsel standartlara bağlı olması ve (iii) öğrencilerin akademik üretim sürecinde sürekli geri bildirim ihtiyacı duyması üzerine kuruludur. Proje, bu üç boyutu bir araya getirerek hem içerik üretimi hem de biçimsel uyumluluk açısından öğrencinin iş yükünü azaltmayı hedeflemektedir.

## **1.2. Birinci bölüm üçüncü derece başlık**

Eğitim odaklı dijital asistanların başarısı, yalnızca doğru bilgi üretmesine değil; aynı zamanda kullanıcının bulunduğu bağlamı (ders, dönem, teslim tarihi, şablon gereksinimleri, hedef çıktı türü vb.) doğru anlamasına bağlıdır. Öğrencinin bir “bitirme projesi raporu” için ihtiyaç duyduğu destek ile “kısa bir ders özeti” için ihtiyaç duyduğu destek farklıdır. Bu nedenle proje kapsamında, öğrencinin niyetini tespit eden ve çıktıyı belirli bir formata göre şekillendiren bir rehberlik yaklaşımı esas alınmıştır.

Selçuk YZ Asistan yaklaşımı, kullanıcıdan gelen istekleri belirli görev sınıflarına ayırmayı hedefler: örneğin konu seçimi ve kapsam belirleme, literatür taraması yönlendirmesi, bölüm planı oluşturma, yazım/biçim denetimi, kaynakça düzeni ve teslim öncesi kontrol listeleri. Bu görev sınıfları, akademik proje yürütme sürecinin doğal akışına uyumlu olacak şekilde yapılandırılır. Böylece kullanıcı, parçalı ve belirsiz bir süreci daha yönetilebilir adımlara dönüştürür.

Bu proje fikri, özellikle rapor yazımında tekrar eden format hatalarının ve süreç yönetimi eksikliğinin öğrenciler için önemli bir zaman kaybına yol açtığı gözleminden hareketle şekillenmiştir. Sistemin temel motivasyonu, kullanıcıya “ne yapması gerektiğini” söylemekle kalmayıp, “nasıl yapacağına” dair örnekli ve şablon uyumlu çıktılar üreterek süreci hızlandırmaktır.

## **1.3. Birinci bölüm dördüncü derece başlık**

Akademik doküman üretiminde en sık görülen problemlerden biri, içeriğin doğruluğundan bağımsız olarak biçimsel standartlara uyumsuzluktur. Başlık hiyerarşisinin yanlış kullanımı, paragraf düzeni tutarsızlıkları, numaralandırma hataları ve kaynakça formatının karışması; değerlendirme sürecinde olumsuz etki oluşturabilmektedir. Bu nedenle Selçuk YZ Asistan, çıktı üretirken belirli bir “şablon-disiplin” yaklaşımını izlemeyi hedefler.

Bu yaklaşım kapsamında, kullanıcıdan alınan metinler ve talepler; bölüm başlıkları, alt başlıklar ve içerik paragrafları şeklinde yapılandırılmış bir formata dönüştürülür. Ayrıca sistem, metni tek seferde uzun bloklar halinde vermek yerine; adım adım üretim ve kontrol mantığıyla ilerleyerek hataların erken aşamada yakalanmasını amaçlar. Böylece öğrenci, raporun her bölümünü ayrı ayrı olgunlaştırabilir ve son birleştirme aşamasında daha az sorunla karşılaşır.

Sonuç olarak bu alt başlıkta açıklanan temel ihtiyaç; içerik üretiminin yanında biçimsel doğruluğun da eş zamanlı yönetilmesidir. Projenin arka planındaki problem tanımı, Selçuk YZ Asistan’ın sadece bir “soru-cevap aracı” değil, akademik proje yazımını yöneten bir “rehber sistem” olarak tasarlanmasını gerektirmiştir.

**1.4. Projenin Önemi**

Selçuk Üniversitesi gibi büyük ölçekli bir kurumda, bilgi erişimi konusunda çeşitli zorluklar yaşanmaktadır:

Bilgi Dağınıklığı: Üniversite bilgileri farklı web sayfalarına, duyuru panolarına ve birimlere dağılmış durumdadır. Öğrenciler, ihtiyaç duydukları bilgiye ulaşmak için birden fazla kaynağı taramak zorunda kalmaktadır.

7/24 Destek Eksikliği: Öğrenci işleri, danışmanlık ve diğer destek birimleri mesai saatleri içinde hizmet vermektedir. Öğrencilerin mesai saatleri dışındaki soruları yanıtsız kalmaktadır.

Tekrarlayan Sorular: Üniversite personeli, benzer soruları tekrar tekrar yanıtlamak zorunda kalmaktadır. Bu durum, hem zaman kaybına hem de kaynak israfına neden olmaktadır.

Mobil Erişim İhtiyacı: Öğrenciler, hareket halindeyken de bilgiye erişmek istemektedir. Mevcut web tabanlı sistemler mobil kullanım için optimize edilmemiş olabilmektedir.

Dil Bariyeri: Uluslararası öğrenciler için Türkçe bilgi kaynaklarına erişim zorlaşmaktadır.

Bu proje, yukarıda belirtilen sorunlara çözüm sunmak amacıyla geliştirilmiştir. Yapay zeka destekli bir asistan, öğrencilere ve personele 7/24 hizmet vererek bilgiye erişimi kolaylaştıracaktır. RAG teknolojisi kullanılarak, asistanın yalnızca doğrulanmış ve güncel bilgiler sunması sağlanacaktır. Ayrıca Flutter ile geliştirilen mobil uygulama sayesinde kullanıcılar her yerden sisteme erişebilecektir.  
**1.5. Projenin Kapsamı**  
Kapsam Dahilinde:  
Selçuk Üniversitesi hakkında genel bilgiler (tarihçe, misyon, vizyon)  
Fakülte ve bölüm bilgileri  
Akademik takvim ve önemli tarihler  
Öğrenci işleri prosedürleri (kayıt, belge talepleri, vb.)  
Kampüs hizmetleri (kütüphane, yemekhane, ulaşım, yurt, vb.)  
Sıkça sorulan sorular (SSS)  
İletişim bilgileri  
Web tabanlı chat arayüzü  
Mobil uygulama (iOS ve Android)  
Kapsam Dışında:  
Öğrenci not ve devamsızlık bilgileri (kişisel veri güvenliği)  
Ders içerikleri ve materyalleri  
Sınav soruları ve cevapları  
Personel özlük bilgileri  
Mali işlemler ve ödeme bilgileri  
OBS (Öğrenci Bilgi Sistemi) entegrasyonu  
1.4. Raporun Organizasyonu  
Bölüm 1 \- Giriş: Projenin arka planı, önemi, kapsamı ve raporun organizasyonu açıklanmaktadır.  
Bölüm 2 \- Kaynak Araştırması: Yapay zeka, doğal dil işleme, büyük dil modelleri, RAG teknolojileri ve mobil uygulama geliştirme hakkında literatür taraması sunulmaktadır.  
Bölüm 3 \- Materyal ve Yöntem: Projede kullanılan metodoloji, veri toplama ve işleme süreçleri, model seçimi ve değerlendirme metrikleri açıklanmaktadır.  
Bölüm 4 \- Sistem Tasarımı ve Uygulama: Sistemin mimarisi, bileşenleri, API tasarımı, mobil uygulama ve kullanıcı arayüzü detaylandırılmaktadır.  
Bölüm 5 \- Araştırma Bulguları ve Tartışma: Test sonuçları, performans değerlendirmesi ve karşılaşılan zorluklar tartışılmaktadır.  
Bölüm 6 \- Sonuçlar ve Öneriler: Projenin sonuçları özetlenmekte ve gelecek çalışmalar için öneriler sunulmaktadır.

# **2\. KAYNAK ARAŞTIRMASI**

## **2.1. Yapay Zeka ve Doğal Dil İşleme**

Yapay zeka, makinelerin insan benzeri düşünme ve öğrenme yeteneklerini taklit etmesini sağlayan bir bilgisayar bilimi dalıdır. Doğal dil işleme ise yapay zekanın bir alt dalı olarak, bilgisayarların insan dilini anlama, yorumlama ve üretme kapasitesini geliştirmeyi hedefler (Jurafsky ve Martin, 2023).

Erken dönem doğal dil işleme çalışmaları, 1950'lerde Alan Turing'in "Computing Machinery and Intelligence" makalesiyle başlamıştır (Turing, 1950). 1966 yılında Joseph Weizenbaum tarafından geliştirilen ELIZA, ilk chatbot örneklerinden biri olarak kabul edilmektedir (Weizenbaum, 1966). ELIZA, basit kalıp eşleştirme teknikleri kullanarak psikoterapist rolünü taklit etmekteydi.

1990'larda istatistiksel yöntemlerin doğal dil işlemeye entegrasyonu önemli bir dönüm noktası olmuştur. N-gram modelleri, gizli Markov modelleri ve karar ağaçları gibi teknikler yaygın olarak kullanılmaya başlanmıştır. 2000'li yıllarda makine öğrenmesi algoritmalarının gelişmesiyle birlikte, doğal dil işleme sistemlerinin performansı önemli ölçüde artmıştır.

Kelime gömme teknikleri, kelimelerin anlamsal özelliklerini yakalayarak doğal dil işleme alanında devrim yaratmıştır. Mikolov ve arkadaşları tarafından 2013 yılında geliştirilen Word2Vec, kelimeleri yoğun vektör uzayında temsil ederek anlamsal ilişkileri matematiksel olarak modelleyebilmiştir (Mikolov ve ark., 2013).

## **2.2. Büyük Dil Modelleri**

Büyük dil modelleri, milyarlarca parametre içeren ve geniş metin veri kümeleri üzerinde eğitilen yapay sinir ağlarıdır. Bu modeller, dil anlama ve üretme görevlerinde insan seviyesine yakın performans gösterebilmektedir.

Transformer mimarisi, 2017 yılında Vaswani ve arkadaşları tarafından önerilmiş ve doğal dil işleme alanında paradigma değişimine yol açmıştır (Vaswani ve ark., 2017). Bu mimari, dikkat mekanizması sayesinde uzun mesafeli bağımlılıkları etkili şekilde modelleyebilmektedir. Transformer'ın öz-dikkat katmanları, her kelimenin cümledeki diğer tüm kelimelerle ilişkisini hesaplayarak bağlamsal temsiller oluşturur.

BERT (Bidirectional Encoder Representations from Transformers), Google tarafından 2019 yılında geliştirilmiş ve çift yönlü bağlam anlama kapasitesiyle öne çıkmıştır (Devlin ve ark., 2019). BERT, maskeli dil modelleme ve sonraki cümle tahmini görevleri ile ön eğitim yapılmıştır.

GPT (Generative Pre-trained Transformer) serisi, OpenAI tarafından geliştirilmiş ve metin üretme görevlerinde başarılı olmuştur. GPT-2, 2019 yılında 1.5 milyar parametre ile dikkat çekmiş, GPT-3 ise 2020 yılında 175 milyar parametreye ulaşarak few-shot learning yetenekleri sergilemiştir (Brown ve ark., 2020). GPT-4, 2023 yılında çok modlu yetenekler ve gelişmiş akıl yürütme kapasitesi ile yayınlanmıştır (OpenAI, 2023).

LLaMA (Large Language Model Meta AI), Meta tarafından 2023 yılında açık kaynak olarak sunulmuştur (Touvron ve ark., 2023). LLaMA, 7 milyardan 65 milyara kadar değişen parametre boyutlarında modeller içermektedir. LLaMA'nın açık kaynak olması, akademik çalışmalar ve kurumsal uygulamalar için erişilebilir alternatifler sunmuştur.

Türkçe için özel olarak eğitilmiş modeller de geliştirilmiştir. BERTurk, Türkçe Wikipedia ve diğer Türkçe kaynaklar üzerinde eğitilmiş BERT tabanlı bir modeldir (Schweter, 2020). Bu tür dil-özel modeller, Türkçe metinlerin anlaşılması ve işlenmesinde daha iyi performans göstermektedir.

## **2.3. RAG (Retrieval Augmented Generation)**

Retrieval Augmented Generation, büyük dil modellerinin bilgi güvenilirliğini artırmak için geliştirilen bir yaklaşımdır. RAG, modelin yanıt üretmeden önce ilgili belgeleri veritabanından getirerek bağlam zenginleştirmesi yapmasını sağlar.

Lewis ve arkadaşları tarafından 2020 yılında önerilen RAG yaklaşımı, bilgi yoğun doğal dil işleme görevlerinde önemli başarılar elde etmiştir (Lewis ve ark., 2020). Bu yöntem, parametrik hafıza ile parametrik olmayan hafızayı birleştirerek, modellerin güncel ve doğrulanabilir bilgi üretmesini sağlar. RAG sisteminin temel bileşenleri; belgelerin sayısal temsillerinin saklandığı vektör veritabanı, sorgu ile ilgili belgeleri bulan geri getirme motoru ve getirilen belgeler bağlamında yanıt üreten üretici modelden oluşmaktadır.

FAISS (Facebook AI Similarity Search), vektör benzerlik araması için optimize edilmiş bir kütüphanedir (Johnson ve ark., 2019). Milyarlarca vektör içeren veri kümelerinde bile hızlı arama yapabilmektedir. FAISS, yaklaşık en yakın komşu algoritmaları kullanarak ölçeklenebilir çözümler sunar. ChromaDB ise açık kaynak bir vektör veritabanı olarak RAG uygulamalarında yaygın kullanılmaktadır ve gömme vektörlerinin saklanması ile sorgulanması için optimize edilmiştir.

Gao ve arkadaşları tarafından 2023 yılında yapılan kapsamlı bir literatür taraması, RAG yaklaşımının çeşitli varyasyonlarını ve uygulama alanlarını incelemiştir (Gao ve ark., 2023). Araştırma, RAG'ın halüsinasyon problemini önemli ölçüde azalttığını ve kaynak gösterimi yaparak denetlenebilirliği artırdığını göstermiştir.

## **2.4. Mobil Uygulama Geliştirme ve Flutter**

Flutter, Google tarafından geliştirilen açık kaynak bir kullanıcı arayüzü araç kitidir. Tek kod tabanı ile iOS, Android, web ve masaüstü uygulamaları geliştirmeye olanak tanımaktadır (Google, 2018). Flutter, Dart programlama dilini kullanır ve reaktif programlama paradigmasını benimser.

Flutter'ın temel avantajları arasında hot reload ile hızlı geliştirme döngüsü, özelleştirilebilir widget sistemi, native performansa yakın çalıştırma hızı, Material Design ve Cupertino widget setleri ile güçlü topluluk desteği bulunmaktadır. GetX ise Flutter için hafif ve güçlü bir state management çözümü olarak dependency injection, route management ve reactive state management özelliklerini birleştirmektedir. GetX'in performans odaklı tasarımı, mobil uygulamalarda verimli kaynak kullanımı sağlamaktadır.

## **2.5. Üniversite Chatbot Uygulamaları**

Üniversitelerde chatbot uygulamaları, öğrenci hizmetlerini iyileştirme ve idari yükü azaltma amacıyla yaygınlaşmaktadır. Adamopoulou ve Moussiades (2020), chatbot teknolojilerinin tarihçesi ve uygulamalarını kapsamlı şekilde incelemişlerdir.

Ranoliya ve arkadaşları (2017), bir üniversite için sık sorulan sorular chatbotu geliştirmiş ve sistemin öğrenci memnuniyetini artırdığını raporlamışlardır. Chatbot, kayıt işlemleri, akademik takvim ve kampüs hizmetleri hakkında yirmi dört saat bilgi sağlamıştır.

Kuhail ve arkadaşları (2023), eğitimde chatbot kullanımı üzerine sistematik bir derleme çalışması yapmışlardır. Araştırma, chatbotların öğrenci etkileşimini artırdığını ve öğrenme deneyimini iyileştirdiğini göstermiştir. Ayrıca, kişiselleştirilmiş öğrenme desteği sağlayan chatbotların öğrenci başarısına olumlu etkisi bulunmuştur.

Okonkwo ve Ade-Ibijola (2021), eğitimde chatbot uygulamalarının sistematik incelemesinde, chatbotların öğretim asistanı, öğrenme yardımcısı ve idari destek rolleri üstlenebildiğini belirtmişlerdir. Page ve Gehlbach (2017), yapay zeka destekli sanal asistanların üniversite başvuru süreçlerinde öğrencilere yardımcı olduğunu göstermiştir. Sistem, karmaşık süreçleri basitleştirerek öğrencilerin bilgiye erişimini kolaylaştırmıştır.

## **2.6. İlgili Çalışmalar**

Ulusal ve uluslararası düzeyde benzer projelerin incelenmesi, Selçuk AI Asistan projesinin özgünlüğünü ve katkılarını ortaya koymaktadır. IBM Watson Assistant, kurumsal chatbot çözümleri sunmaktadır ancak ticari bir ürün olması ve kapalı kaynak yapısı nedeniyle akademik kullanım için sınırlıdır. Microsoft Azure Bot Service, bulut tabanlı chatbot geliştirme platformu sağlamaktadır fakat yüksek maliyetli olması ve veri gizliliği endişeleri, özellikle hassas akademik bilgilerin işlenmesinde tereddüt yaratmaktadır.

Rasa, açık kaynak bir chatbot framework'üdür ve özelleştirilebilir yapısı ile veri kontrolü avantajları sunmaktadır. Ancak, büyük dil modelleri ile entegrasyonu sınırlıdır ve kurulum karmaşıklığı yüksektir. Türkiye'deki üniversitelerde bazı chatbot uygulamaları bulunmaktadır fakat çoğunluğu kural tabanlı sistemlerdir ve doğal dil anlama kapasiteleri sınırlıdır. Ayrıca, bu sistemlerin kaynak kodları genellikle paylaşılmamaktadır.

Selçuk AI Asistan projesi; tamamen açık kaynak ve akademik kullanıma uygun olması, yerel LLM kullanımı ile veri gizliliğini koruması, RAG teknolojisi ile kaynak göstererek güvenilir yanıtlar üretmesi, çoklu platform desteği sağlaması, çoklu LLM sağlayıcı mimarisine sahip olması ve üniversite ekosistemini anlamak için özel olarak tasarlanmış bilgi tabanı içermesi açılarından ayırt edici özellikler taşımaktadır. Google Gemini gibi ticari API'lerden tamamen bağımsız çalışabilen sistem, kurumsal bağımsızlık ve veri egemenliği açısından önemli bir avantaj sağlamaktadır.

# **3\. MATERYAL VE YÖNTEM**

## **3.1. Geliştirme Metodolojisi**

Proje geliştirme sürecinde Çevik metodoloji yaklaşımı benimsenmiştir. İki haftalık sprint döngüleri ile iteratif geliştirme yapılmıştır ve her sprint sonunda çalışan prototip üretilmiş ve test edilmiştir. Versiyon kontrolü için Git kullanılmış ve GitHub üzerinde kod deposu oluşturulmuştur.

Kod kalitesi için sürekli entegrasyon pipeline'ları kurulmuştur. Backend tarafında pytest ile birim testler, ruff ile kod formatı kontrolü, mypy ile tip kontrolü ve encoding guard ile karakter kodlama doğrulaması yapılmıştır. Flutter tarafında ise flutter analyze ile statik kod analizi, flutter test ile widget testleri ve farklı platformlar için build kontrolü gerçekleştirilmiştir.

## **3.2. Veri Toplama**

Bilgi tabanı oluşturmak için Selçuk Üniversitesi'nin çeşitli resmi kaynaklarından veri toplanmıştır. Resmi web sitesinden genel tanıtım bilgileri, fakülte ve bölüm sayfaları, akademik takvim ve iletişim bilgileri derlenmiştir. Öğrenci İşleri Dairesi Başkanlığı'ndan kayıt yenileme prosedürleri, diploma işlemleri ve öğrenci belgesi talepleri bilgileri elde edilmiştir. Kütüphane ve Kampüs Hizmetleri'nden kütüphane kullanım bilgileri, yemekhane ve kantin bilgileri ile yurt ve konaklama bilgileri toplanmıştır. Sağlık, Kültür ve Spor Dairesi'nden ise sağlık hizmetleri, spor tesisleri ve kültürel etkinlikler hakkında bilgiler derlenmiştir.

Veri toplama yöntemi olarak manuel derleme tercih edilmiştir çünkü bilgi doğruluğu kritik önem taşımakta, kaynak güvenilirliği sağlanması gerekmekte ve hukuki sorunların önlenmesi hedeflenmektedir. Toplanan veriler, danışman onayı alınarak doğrulanmıştır.

## **3.3. Veri İşleme**

Toplanan ham veriler, RAG sisteminde kullanılmak üzere işlenmiştir. Metin temizleme aşamasında HTML etiketleri kaldırılmış, özel karakterler normalize edilmiş, gereksiz boşluklar temizlenmiş ve Türkçe karakter kodlaması UTF-8 formatına dönüştürülmüştür.

Parçalama aşamasında LangChain'in RecursiveCharacterTextSplitter kullanılarak metinler parçalara ayrılmıştır. Parça boyutu sekiz yüz karakter, örtüşme yüz karakter ve ayırıcılar olarak paragraf, cümle ve kelime sınırları belirlenmiştir. Örtüşme, bağlamsal bilgi kaybını önlemek için uygulanmıştır.

Vektör gömme aşamasında sentence-transformers kütüphanesinin all-MiniLM-L6-v2 modeli kullanılmıştır. Model, üç yüz seksen dört boyutlu vektörler üretmekte, çoklu dil desteği sağlamakta ve hızlı çıkarım süresi sunmaktadır. İndeksleme için iki alternatif vektör veritabanı desteklenmiştir; FAISS hızlı benzerlik araması için, ChromaDB ise kalıcı depolama ve sorgulama için optimize edilmiştir. FAISS indeksi, similarity metric olarak cosine similarity kullanmaktadır.

## **3.4. Model Seçimi**

Proje için model seçiminde yerel çalıştırma kapasitesi, Türkçe dil desteği, makul donanım gereksinimleri, açık kaynak lisansı ve aktif topluluk desteği kriterleri dikkate alınmıştır.

Seçilen model olan Llama 3.1, Meta tarafından geliştirilmiş açık kaynak bir LLM'dir. Model, sekiz milyar, yetmiş milyar ve dört yüz beş milyar parametre olmak üzere farklı boyutlarda sunulmaktadır. Proje için sekiz milyar parametre versiyonu seçilmiştir çünkü standart donanımda çalışabilmekte, Türkçe dilinde yeterli performans göstermekte, yanıt süresi kabul edilebilir seviyede olmakta ve quantization desteği ile bellek kullanımı optimize edilebilmektedir.

Sistem mimarisi çoklu model desteği içermektedir ve HuggingFace Hub'dan farklı modeller çalıştırılabilmektedir. Provider deseni sayesinde model değişimi uygulama kodunu etkilememektedir.

## **3.5. RAG Pipeline Tasarımı**

RAG pipeline'ı, LangChain framework'ü kullanılarak oluşturulmuştur. Pipeline, sorgu ön işleme, belge geri getirme, bağlam oluşturma, prompt oluşturma, yanıt üretimi ve strict mode olmak üzere altı temel aşamadan oluşmaktadır.

Sorgu ön işleme aşamasında sorgu temizleme ve normalize etme işlemleri yapılmakta, ardından embedding model ile vektörel temsil oluşturulmaktadır. Belge geri getirme aşamasında en benzer beş parça getirilmekte ve benzerlik eşiği olarak sıfır nokta iki değeri kullanılmaktadır. Bağlam oluşturma aşamasında getirilen parçalardan birleştirilmiş bağlam ve kaynak bilgileri hazırlanmaktadır.

Prompt oluşturma aşamasında sistem rolü, bağlam bilgisi ve soru birleştirilerek LLM için uygun prompt hazırlanmaktadır. Yanıt üretimi aşamasında LLM ile yanıt üretilmekte ve kaynak bilgisi eklenmektedir. Bilgi tabanı dışı sorularda uyarı verilmesi için strict mode aktif edilmiştir ve ilgili belge bulunamadığında kullanıcıya bilgi tabanında yeterli bilgi bulunmadığı bildirilmektedir.

## **3.6. Değerlendirme Metrikleri**

Sistemin performansı çeşitli metriklerle ölçülmüştür. Doğruluk metrikleri olarak kritik bilgi doğruluğu, genel doğruluk ve halüsinasyon oranı kullanılmıştır. Kritik bilgi doğruluğu, temel bilgilerin yüzde yüz doğru yanıtlanmasını; genel doğruluk, tüm test sorularında doğru yanıt oranını; halüsinasyon oranı ise bilgi tabanında olmayan bilgi üretme yüzdesini ölçmektedir.

Performans metrikleri olarak yanıt süresi, toplam yanıt süresi, bellek kullanımı ve işlemci yükü izlenmiştir. RAG kalite metrikleri olarak retrieval precision, retrieval recall ve kaynak eşleşmesi değerlendirilmiştir. Kullanıcı deneyimi metrikleri olarak eşzamanlı kullanıcı kapasitesi, hata toleransı ve akıcılık ölçülmüştür.

Test veri kümesi, elli kritik soru, yüz genel soru ve yirmi kaynak dışı sorudan oluşmaktadır. Testler, hem manuel hem de otomatik olarak gerçekleştirilmiştir.

# **4\. SİSTEM TASARIMI VE UYGULAMA**

## **4.1. Genel Mimari**

Selçuk AI Asistan, üç katmanlı bir mimari ile tasarlanmıştır. İstemci katmanı Flutter framework'ü ile geliştirilmiş olup Material 3 kullanıcı arayüzü, GetX state management ve HTTP ile Server-Sent Events iletişimini içermektedir. Servis katmanı FastAPI ile oluşturulmuş olup request ve response validation, session management, error handling ve provider orchestration sorumluluklarını üstlenmektedir. Altyapı katmanı ise RAG engine ve LLM provider bileşenlerinden oluşmaktadır.

Veri akışı şu şekilde gerçekleşmektedir; kullanıcı sorusu Flutter arayüzünden gönderilmekte, FastAPI backend soruyu alarak doğrulamakta, RAG engine ilgili belgeleri vektör veritabanından getirmekte, bağlam LLM promptuna eklenmekte, LLM yanıtı streaming veya tek seferde üretmekte, yanıt ve kaynaklar istemciye döndürülmekte ve Flutter arayüzü yanıtı görüntülemektedir.

## **4.2. Backend Bileşeni**

Backend, Python FastAPI framework'ü ile geliştirilmiştir. Main App bileşeni ASGI uygulaması ve endpoint tanımlarını içermektedir. Config bileşeni çevresel değişkenler ve ayarları yönetmektedir. Models bileşeni Pydantic şemalarını barındırmaktadır. Providers bileşeni LLM sağlayıcı soyutlamasını sağlamaktadır. RAG Engine bileşeni belge geri getirme ve indeksleme işlemlerini yürütmektedir. Chat Service bileşeni sohbet mantığı ve oturum yönetimini gerçekleştirmektedir.

API endpoint'leri arasında health endpoint sistem sağlık durumunu, models endpoint kullanılabilir modelleri, chat endpoint tek yanıt modunu, chat stream endpoint streaming modunu ve stats endpoint sistem istatistiklerini sunmaktadır. Tüm endpoint'ler kimlik doğrulama gerektirmemektedir.

Provider deseni, farklı LLM sağlayıcılarını tek bir arayüz altında birleştirmektedir. BaseLLMProvider soyut sınıfı generate ve generate stream metodlarını tanımlamaktadır. OllamaProvider bu sınıftan türetilmiş olup Ollama API çağrısı yapmaktadır. HuggingFaceProvider ise HuggingFace Inference API çağrısı gerçekleştirmektedir.

## **4.3. Mobil Uygulama Bileşeni**

Flutter uygulaması GetX mimarisi ile yapılandırılmıştır. Screens dizini ekran widget'larını, controllers dizini GetX controller'larını, services dizini API servis katmanını, models dizini veri modellerini, widgets dizini tekrar kullanılabilir bileşenleri ve config dizini yapılandırma dosyalarını içermektedir.

Ana ekranlar arasında splash screen uygulama açılış ekranı ve backend sağlık kontrolünü, home screen karşılama ekranı ve hızlı erişim butonlarını, chat screen sohbet arayüzü ile mesaj listesi ve giriş alanını, settings screen ise tema, dil ve backend URL ayarlarını sunmaktadır.

GetX ile reaktif state yönetimi gerçekleştirilmiştir. ChatController sınıfı mesajlar listesi ve yükleme durumunu observable olarak yönetmekte, API servisi çağrısı yaparak yanıtları mesajlar listesine eklemekte ve hata durumlarını yönetmektedir.

## **4.4. RAG Engine Bileşeni**

RAG engine, bilgi tabanı yönetimi ve sorgu zamanı geri getirme işlemlerinden sorumludur. İndeksleme süreci komut satırı aracılığıyla başlatılmakta, belge okuma, metin temizleme, chunking, embedding üretimi ve vektör veritabanına yazma adımlarını içermektedir.

Sorgu zamanı geri getirme işlemi query embedding oluşturma, benzerlik araması yapma ve eşik filtresi uygulama aşamalarından oluşmaktadır. Retrieve context fonksiyonu sorgu metnini alarak vektörel temsil oluşturmakta, similarity search with score metoduyla arama yapmakta ve belirlenen eşik değerinin üzerindeki sonuçları filtrelemektedir.

Her belge parçası metadata ile zenginleştirilmiştir. Metadata source, title, chunk id, created at, document type ve category bilgilerini içermektedir. Yanıt üretiminden sonra kullanılan belgelerin kaynak bilgileri döndürülmektedir.

## **4.5. API Tasarımı**

RESTful API tasarım prensipleri uygulanmıştır. Health endpoint GET metodu ile sistem sağlık durumunu döndürmekte ve kimlik doğrulama gerektirmemektedir. Models endpoint kullanılabilir modelleri listelemektedir. Chat endpoint POST metodu ile tek seferde yanıt üretmektedir. Chat stream endpoint streaming yanıt sağlamaktadır. Stats endpoint sistem istatistiklerini sunmaktadır.

Hata yönetimi için standart HTTP durum kodları kullanılmıştır. İki yüz kodu başarılı isteği, dört yüz kodu geçersiz parametreyi, beş yüz kodu sunucu hatasını ve beş yüz üç kodu model veya RAG erişilemezlik durumunu belirtmektedir. Hata yanıtları kullanıcı dostu Türkçe mesajlar içermekte ve hata kodu bilgisi sağlamaktadır.

## **4.6. Veritabanı ve Knowledge Base**

Bilgi tabanı iki seviyeli yapı ile organize edilmiştir. Ham belgeler docs dizininde genel, fakulteler, ogrenci isleri ve kampus hizmetleri alt dizinlerinde Markdown formatında saklanmaktadır. Vektör veritabanı data rag dizininde faiss index ve chromadb alt dizinlerinde tutulmaktadır.

Bilgi tabanı güncelleme süreci docs dizininde ilgili dosyanın güncellenmesi, rag ingest scripti ile yeniden indekslenmesi ve backend restart işlemlerini içermektedir. İndeks bellekte değilse otomatik olarak yüklenmektedir.

## **4.7. Güvenlik Tasarımı**

Güvenlik önlemleri çeşitli katmanlarda uygulanmıştır. Veri gizliliği için yerel LLM kullanımı ile veri dış servislere gönderilmemekte, kullanıcı mesajları veritabanına kaydedilmemekte ve session ID'ler geçici olarak bellekte tutulmaktadır.

Input validation için Pydantic ile istek doğrulaması, maksimum mesaj uzunluğu kontrolü ve XSS saldırılarına karşı HTML escape uygulanmaktadır. Rate limiting için slowapi kütüphanesi kullanılmakta ve dakika başına on istek limiti konulmaktadır. CORS politikası için development ortamında localhost izin verilmekte, production ortamında ise spesifik domain'ler tanımlanmaktadır.

Error handling stratejisi olarak detaylı hata mesajları sadece development modunda gösterilmekte, production'da genel hata mesajları kullanılmakta ve loglama ile hata izleme yapılmaktadır.

## **4.8. Test Stratejisi**

Çok katmanlı test stratejisi uygulanmıştır. Birim testleri pytest ile backend fonksiyonlarını test etmektedir. Entegrasyon testleri pytest ve httpx ile API endpoint'lerini doğrulamaktadır. Widget testleri Flutter test framework'ü ile kullanıcı arayüzü bileşenlerini kontrol etmektedir. Smoke testleri PowerShell scriptleri ile canlı sistemi doğrulamaktadır. Load testleri Locust aracılığıyla performans ölçümü yapmaktadır.

Backend test örneği, chat endpoint'inin doğru çalıştığını doğrulamakta, iki yüz durum kodu aldığını kontrol etmekte ve yanıtta belirli bir bilginin bulunduğunu assert etmektedir. Flutter widget test örneği, chat bubble widget'ının düzgün render edildiğini ve mesaj metninin görüntülendiğini doğrulamaktadır.

## **4.9. Test Senaryoları ve Sonuçları**

Test senaryoları gerçek kullanım durumlarını simüle etmektedir. Kritik bilgi testlerinde elli soru sorulmuş ve tamamında doğru yanıt alınarak yüzde yüz başarı oranına ulaşılmıştır. Sorular Selçuk Üniversitesi'nin kuruluş yılı, konumu, fakülte sayısı ve Teknoloji Fakültesi'nin bölümleri gibi temel bilgileri içermektedir.

Genel bilgi testlerinde yüz soru sorulmuş ve doksan altısında doğru yanıt alınarak yüzde doksan altı başarı oranına ulaşılmıştır. Sorular öğrenci kaydı yenileme, kütüphane açılış saatleri, yemekhane menüsü ve yurt başvurusu gibi konuları kapsamaktadır.

Halüsinasyon testlerinde bilgi tabanında olmayan yirmi soru sorulmuş ve tamamında sistem doğru şekilde bilgi bulunmadığını bildirmiştir. Bu sonuç sıfır halüsinasyon oranını göstermektedir ve sistemin strict mode özelliğinin etkin çalıştığını kanıtlamaktadır.

## **4.10. Performans Değerlendirmesi**

Performans ölçüm sonuçları Ollama üzerinde Llama 3.1 sekiz milyar parametre modeli ile elde edilmiştir. İlk token süresi yaklaşık bir nokta iki saniye olarak ölçülmüş ve iki saniye hedefinin altında gerçekleşmiştir. Toplam yanıt süresi üç ila beş saniye aralığında kaydedilmiş ve yedi saniye hedefinin altında kalmıştır. RAM kullanımı altı ila sekiz GB arasında değişmiş ve on GB hedefinin altında gerçekleşmiştir. CPU kullanımı yüzde kırk ila altmış arasında ölçülmüş ve yüzde seksen hedefinin altında kalmıştır. Sistem yüzden fazla eşzamanlı kullanıcıya hizmet verebilmiş ve elli kullanıcı hedefinin üzerinde performans göstermiştir.

Performans gözlemleri; yanıt süresinin soru uzunluğu ile doğru orantılı olduğunu, ilk sorgunun model yükleme nedeniyle daha yavaş olduğunu, sonraki sorguların hızlandığını, streaming modunun algılanan gecikmeyi azalttığını ve RAG retrieval overhead'inin yüz milisaniyelik minimal bir süre olduğunu göstermiştir.

## **4.11. Karşılaşılan Zorluklar ve Çözümler**

Türkçe karakter kodlama sorunları Windows sistemde UTF-8 kodlama hatalarına neden olmuştur. Bu sorun dosya okuma ve yazma işlemlerinde encoding parametresinin belirtilmesi ve CI'da encoding guard eklenmesi ile çözülmüştür.

Model bellek tüketimi büyük modellerin RAM aşımına yol açmıştır. Bu zorluk quantization teknikleri, daha küçük model varyantının seçilmesi ve offloading stratejileri uygulanarak aşılmıştır.

RAG kaynak eşleşme kalitesi bazen alakasız belgelerin getirilmesine sebep olmuştur. Bu problem benzerlik eşiğinin optimize edilmesi, chunk boyutunun dengelenmesi ve metadata filtreleme eklenmesi ile çözülmüştür.

Streaming yanıt kesilmeleri uzun yanıtlarda SSE bağlantısının kopmasına yol açmıştır. Bu durum keep-alive mekanizması ve event loop'a düzenli kontrol verme ile giderilmiştir.

Flutter web CORS sorunları web sürümünde API isteklerinin bloke olmasına neden olmuştur. Bu zorluk backend'de CORS middleware yapılandırması ve proxy ayarları ile çözülmüştür.

# **5\. SONUÇLAR VE ÖNERİLER**

## **5.1. Sonuçlar**

Bu bitirme projesi kapsamında Selçuk Üniversitesi için yapay zeka destekli bir bilgi asistanı başarıyla tasarlanmış ve geliştirilmiştir. Proje, yerel LLM kullanımı, RAG teknolojisi ve çoklu platform desteği ile özgün bir çözüm sunmaktadır.

Teknik başarılar değerlendirildiğinde Llama 3.1 sekiz milyar parametre modelinin Türkçe dilinde yeterli performans gösterdiği görülmüştür. Kritik bilgi doğruluğu yüzde yüz seviyesinde gerçekleşmiş, genel soru-cevap doğruluğu yüzde doksan altı olarak ölçülmüş ve halüsinasyon oranı sıfıra düşürülmüştür. Retrieval Augmented Generation yaklaşımı bilgi güvenilirliğini önemli ölçüde artırmıştır. FAISS vektör veritabanı milisaniye mertebesinde arama hızı sağlamış, kaynak gösterimi özelliği akademik denetlenebilirliği mümkün kılmış ve sekiz yüz karakterlik chunk boyutu ile yüz karakterlik overlap optimal sonuçlar vermiştir.

Yanıt süreleri değerlendirildiğinde ortalama yanıt süresinin üç ila beş saniye aralığında gerçekleştiği, ilk token süresinin bir nokta iki saniye civarında ölçüldüğü, streaming modunun kullanıcı deneyimini iyileştirdiği ve sistemin eşzamanlı yüzden fazla kullanıcıya hizmet verebildiği tespit edilmiştir.

Gizlilik ve veri egemenliği açısından yerel LLM kullanımı ile kullanıcı verilerinin kurum dışına çıkması engellenmiştir. Mesaj geçmişi veritabanına kaydedilmemekte ve yalnızca oturum bazlı geçici bellekte tutulmaktadır. Sistem internet bağlantısı olmadan da temel işlevlerini sürdürebilmektedir.

Çoklu platform desteği için Flutter framework'ü ile iOS, Android ve web platformlarında çalışan tek bir kod tabanı geliştirilmiştir. Material Design 3 ile modern ve tutarlı kullanıcı arayüzü sağlanmış ve GetX state management ile reaktif ve performanslı uygulama yapısı oluşturulmuştur.

Akademik katkılar değerlendirildiğinde Türkiye'deki üniversiteler için tamamen açık kaynak, yerel çalışabilen ve gizlilik odaklı ilk kapsamlı yapay zeka asistan çözümlerinden birinin geliştirildiği görülmektedir. Çoklu LLM sağlayıcı mimarisi ile esneklik sağlanmış ve RAG temelli kaynak gösterimi ile akademik güvenilirlik artırılmıştır. Proje kapsamlı dokümantasyon ile gelecek çalışmalara temel oluşturmakta, kurulum ve test süreçleri detaylandırılmakta ve GitHub Actions ile CI ve CD pipeline'ları örnek teşkil etmektedir.

Projenin kısıtları ve sınırlamaları değerlendirildiğinde bilgi tabanının manuel olarak derlenen belgelerle sınırlı olduğu ve düzenli güncelleme gereksinimi bulunduğu görülmektedir. Sekiz milyar parametre boyutundaki model daha büyük modellere göre sınırlı kapasiteye sahiptir ve karmaşık akıl yürütme görevlerinde yetersiz kalabilmektedir. Yerel çalıştırma için minimum on altı GB RAM gereksinimi bulunmakta ve GPU olmadan yanıt süreleri artmaktadır. Öğrenci Bilgi Sistemi ile entegrasyon bulunmamakta ve kişiselleştirilmiş yanıtlar verilememektedir. Şu anda yalnızca Türkçe desteklenmekte ve çok dilli destek planlanmakla birlikte henüz uygulanmamıştır.

Proje hedeflerine ulaşım değerlendirildiğinde yerel LLM ile veri gizliliğinin sağlandığı, RAG ile kaynak temelli yanıt üretiminin gerçekleştirildiği, Flutter ile çoklu platform desteğinin sağlandığı, yüzde doksan üzeri doğruluk oranına ulaşıldığı, açık kaynak olarak yayınlandığı ve kapsamlı dokümantasyon oluşturulduğu görülmektedir. OBS entegrasyonu gelecek çalışmalara bırakılmış ve çok dilli destek henüz eklenmemiştir.

## **5.2. Öneriler**

Projenin geliştirilmesi ve iyileştirilmesi için çeşitli öneriler sunulmaktadır. Kısa vadeli öneriler arasında bilgi tabanı genişletme, kullanıcı geri bildirimi sistemi ekleme, performans optimizasyonu yapma ve mobil uygulama iyileştirmeleri bulunmaktadır. Bilgi tabanına tüm fakülte ve bölümlerin detaylı bilgileri, öğrenci kulüpleri, etkinlikler ve duyurular eklenmelidir. Her yanıt için geri bildirim butonu eklenmeli ve yanlış veya yetersiz yanıtlar işaretlenebilmelidir. Model quantization ile bellek kullanımı azaltılmalı ve sık sorulan sorular için cache mekanizması eklenmelidir. Offline mod geliştirilmeli, push notification desteği eklenmeli ve dark mode ile tema özelleştirme seçenekleri sunulmalıdır.

Orta vadeli öneriler arasında OBS entegrasyonu, çok dilli destek, gelişmiş RAG teknikleri ve sesli etkileşim bulunmaktadır. Öğrenci Bilgi Sistemi ile güvenli entegrasyon sağlanmalı ve kişiselleştirilmiş yanıtlar verilebilmelidir. İngilizce arayüz ve yanıt desteği eklenmelidir. Hybrid search uygulanmalı ve reranker model ile retrieval kalitesi artırılmalıdır. Speech-to-text ve text-to-speech entegrasyonu yapılmalıdır.

Uzun vadeli öneriler arasında fine-tuning ve özelleştirme, çok modlu yetenekler, proaktif asistan özellikleri ve ölçeklenebilirlik bulunmaktadır. Selçuk Üniversitesi'ne özel verilerde model fine-tuning yapılmalı ve LoRA ile verimli ince ayar uygulanmalıdır. Kampüs haritası ve bina resimlerinin anlaşılması eklenmelidir. Önemli tarihlerde proaktif hatırlatma yapılmalı ve öğrenci profiline göre kişiselleştirilmiş öneriler sunulmalıdır. Kubernetes ile container orchestration uygulanmalı ve load balancing ile auto-scaling mekanizmaları eklenmelidir.

Araştırma önerileri olarak chatbot kalitesini ölçmek için standart metrikler uygulanmalı, kullanıcı memnuniyeti anketleri düzenlenmeli ve farklı chunking stratejilerinin karşılaştırmalı analizi yapılmalıdır. Farklı LLM'lerin üniversite chatbot senaryosunda performans karşılaştırması yapılmalı ve yapay zeka asistanların etik kullanımı konusunda çalışmalar yürütülmelidir.

Kurumsal öneriler olarak projenin pilot uygulama olarak belirli bir fakültede test edilmesi, bilgi tabanı güncelleme sorumluluğunun ilgili birimlere dağıtılması, production ortamında sunucu altyapısının sağlanması ve kullanıcılar için tanıtım ile eğitim materyalleri hazırlanması önerilmektedir.

Topluluk ve açık kaynak önerileri olarak projenin GitHub repository'sinin aktif tutulması, diğer üniversitelerin projeyi adapte etmesinin teşvik edilmesi, kullanıcı ve geliştirici dokümantasyonunun genişletilmesi ve katkı süreçlerinin netleştirilmesi önerilmektedir.

---

**KAYNAKLAR**  
Adamopoulou, E., & Moussiades, L. (2020). Chatbots: History, technology, and applications. Machine Learning with Applications, 2, 100006\.  
Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., ve diğerleri. (2020). Language models are few-shot learners. Advances in Neural Information Processing Systems, 33, 1877–1901.  
Chase, H. (2022). LangChain: Building applications with large language models through composability (GitHub deposu). Ziyaret Tarihi: 10.01.2025.  
Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. Proceedings of NAACL-HLT 2019, 4171–4186.  
Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., ve diğerleri. (2023). Retrieval-augmented generation for large language models: A survey. arXiv:2312.10997.  
Google DeepMind. (2023). Gemini: A family of highly capable multimodal models (Technical report).  
Google. (2018). Flutter: Build apps for any screen. Ziyaret Tarihi: 10.01.2025.  
Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. Neural Computation, 9(8), 1735–1780.  
Johnson, J., Douze, M., & Jégou, H. (2019). Billion-scale similarity search with GPUs. IEEE Transactions on Big Data, 7(3), 535–547.  
Jurafsky, D., & Martin, J. H. (2023). Speech and language processing (3rd ed. draft).  
Kuhail, M. A., Alturki, N., Alramlawi, S., & Alhejori, K. (2023). Interacting with chatbots in education: A systematic review. Education and Information Technologies, 28, 9731–9759.  
Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., ve diğerleri. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. Advances in Neural Information Processing Systems, 33\.  
Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). Efficient estimation of word representations in vector space. arXiv:1301.3781.  
Okonkwo, C. W., & Ade-Ibijola, A. (2021). Chatbots applications in education: A systematic review. Computers and Education: Artificial Intelligence, 2, 100033\.  
OpenAI. (2022). Introducing ChatGPT. Ziyaret Tarihi: 10.01.2025.  
OpenAI. (2023). GPT-4 technical report. arXiv:2303.08774.  
Page, L. C., & Gehlbach, H. (2017). How an artificially intelligent virtual assistant helps students navigate the college-going process. AERA Open, 3(4).  
Ranoliya, B. R., Raghuwanshi, N., & Singh, S. (2017). Chatbot for university related FAQs. 2017 International Conference on Advances in Computing, Communications and Informatics (ICACCI).  
Schweter, S. (2020). BERTurk — BERT models for Turkish. Zenodo.  
Selçuk Üniversitesi. (2025). Selçuk Üniversitesi Resmî Web Sitesi. Ziyaret Tarihi: 10.01.2025.  
Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M.-A., Lacroix, T., ve diğerleri. (2023). LLaMA: Open and efficient foundation language models. arXiv:2302.13971.  
Turing, A. M. (1950). Computing machinery and intelligence. Mind, 59(236), 433–460.  
Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ve diğerleri. (2017). Attention is all you need. Advances in Neural Information Processing Systems, 30\.  
Weizenbaum, J. (1966). ELIZA—A computer program for the study of natural language communication between man and machine. Communications of the ACM, 9(1), 36–45.  
Yükseköğretim Kurulu (YÖK). (2025). YÖK Bilgi Sistemi ve Mevzuat. Ziyaret Tarihi: 10.01.2025.

**EKLER** 

**EK-1** 

| Kontrol Edilecek Hususlar | Evet | Hayır |
| ----- | :---: | :---: |
| Sayfa yapısı uygun mu? |  |  |
| Şekil ve çizelge başlık ve içerikleri uygun mu? |  |  |
| Denklem yazımları uygun mu? |  |  |
| İç kapak, onay sayfası, Proje bildirimi, özet, abstract, önsöz ve/veya teşekkür uygun yazıldı mı? |  |  |
| Proje yazımı; Giriş, Kaynak Araştırması, Materyal ve Yöntem (veya Teorik Esaslar), Araştırma Bulguları ve Tartışma, Sonuçlar ve Öneriler sıralamasında mıdır? |  |  |
| Kaynaklar soyadı sırasına göre verildi mi? |  |  |
| Kaynaklarda verilen her bir yayına proje içerisinde atıfta bulunuldu mu? |  |  |
| Kaynaklar açıklanan yazım kuralına uygun olarak yazıldı mı? |  |  |
| Proje içerisinde kullanılan şekil ve çizelgelerde kullanılan ifadeler Türkçe’ye çevrilmiş mi? (Latince ve Özel kelimeler hariçtir) |  |  |
| Projenin içindekiler kısmı, proje içerisinde verilen başlıklara uygun hazırlanmış mı? |  |  |

Yukarıdaki verilen cevapların doğruluğunu kabul ediyorum.

|  | Unvanı Adı SOYADI | İmza |
| :---: | :---: | :---: |
| **Öğrenci	:** | ………………………..…..……..………. | ……………..………... |
| **Danışman	:** | ………………………………..….………. | …………………..…… |

\*Bitirme projesi/araştırma projeleri Teknoloji Fakültesi proje yazım kurallarına uygun olarak hazırlanmalıdır. Projeler teslim edilmeden önce yukarıdaki kontrol listesi öğrenci ve danışman tarafından imzalanmalıdır. Bu sayfa tez teslimi esnasında en üst sayfa olarak verilmelidir.  
\*Proje ilk savunmaya sunulacağında spiral cilt veya clip dosya formunda teslim edilmelidir.

**EK-2** Uygun bir başlık buraya yazılmalıdır.

# **ÖZGEÇMİŞ** {#özgeçmi̇ş}

**KİŞİSEL BİLGİLER**

| Adı Soyadı	: |  |
| :---- | :---- |
| **Uyruğu	:** |  |
| **Doğum Yeri ve Tarihi	:** |  |
| **Telefon	:** |  |
| **Faks	:** |  |
| **E-mail	:** |  |

**EĞİTİM**

| Derece | Adı, İlçe, İl | Bitirme Yılı |
| :---- | :---- | :---- |
| Lise	: |  |  |
| Üniversite	: |  |  |
| Yüksek Lisans	: |  |  |
| Doktora	: |  |  |

**İŞ DENEYİMLERİ**

| Yıl | Kurum | Görevi |
| :---- | :---- | :---- |
|  |  |  |
|  |  |  |
|  |  |  |

**UZMANLIK ALANI**

**YABANCI DİLLER**

**BELİRTMEK İSTEĞİNİZ DİĞER ÖZELLİKLER**

**YAYINLAR**