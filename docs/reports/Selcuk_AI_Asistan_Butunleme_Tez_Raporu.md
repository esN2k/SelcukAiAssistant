|  |  |
| :---: | :---- |
| **T.C. SELÇUK ÜNİVERSİTESİ TEKNOLOJİ FAKÜLTESİ BİLGİSAYAR MÜHENDİSLİĞİ** |  |
| **YAPAY ZEKA DESTEKLİ ÜNİVERSİTE BİLGİ ASİSTANI: SELÇUK AI ASİSTAN**<br/>**Doğukan BALAMAN (203311066) • Ali YILDIRIM (203311008)**<br/>**BİLGİSAYAR MÜHENDİSLİĞİ UYGULAMALARI** |  |
| **01-2025** **KONYA Her Hakkı Saklıdır** |  |

**PROJE KABUL VE ONAYI**

................................. tarafından hazırlanan “Yapay Zeka Destekli Üniversite Bilgi Asistanı: Selçuk AI Asistan” adlı proje çalışması …/…/… tarihinde aşağıdaki jüri üyeleri tarafından oy birliği/oy çokluğu ile Selçuk Üniversitesi Teknoloji Fakültesi Bilgisayar Mühendisliği bölümünde Bilgisayar Mühendisliği Uygulamaları Projesi olarak kabul edilmiştir.

| Jüri Üyeleri | İmza |
| :---- | :---: |
| **Danışman** Prof. Dr. Nurettin DOĞAN |  |
| **Danışman** Dr. Öğr. Üyesi Onur İNAN |  |
| **Üye** ................................ |  |

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

**Doğukan BALAMAN (203311066)**  \
**Ali YILDIRIM (203311008)**

**SELÇUK ÜNİVERSİTESİ**   \
**TEKNOLOJİ FAKÜLTESİ**  \
**BİLGİSAYAR MÜHENDİSLİĞİ BÖLÜMÜ**

**Danışman: Prof. Dr. Nurettin DOĞAN**  \
**Danışman: Dr. Öğr. Üyesi Onur İNAN**

**2025, 50+ Sayfa**

**Jüri**  \
**Prof. Dr. Nurettin DOĞAN**  \
**Dr. Öğr. Üyesi Onur İNAN**  \
**................................**

Bu çalışma, Selçuk Üniversitesi öğrenci ve personeline 7/24 bilgi sağlayabilen yapay zeka destekli bir bilgi asistanının tasarım ve geliştirme sürecini kapsamaktadır. Sistem, yerel LLM sağlayıcısı olarak Ollama altyapısı ve Retrieval Augmented Generation (RAG) yaklaşımı ile güvenilir yanıt üretmeyi hedefler. Arka uç katmanı FastAPI üzerinde çalışmakta, veri katmanında FAISS tabanlı vektör indeksleme kullanılmaktadır. Mobil istemci Flutter ile geliştirilmiş ve iOS/Android platformlarını hedeflemiştir.

Projede web kazıma ile üniversite web sayfalarından toplanan içerikler, 645 dokümanlık bir bilgi tabanına dönüştürülmüştür. Yeniden kazıma sürecinde 135 hatalı URL tekrar denenmiş, 92 URL başarıyla çekilmiş, 43 URL kalıcı hata olarak sınıflandırılmıştır. Bu değerler %68.15 başarı oranına karşılık gelmektedir. Sistem, RAG bağlamı ile LLM yanıtlarını sınırlandırarak “uydurma bilgi” riskini azaltmayı amaçlamıştır. Kullanılabilirlik açısından temel API uçları (/chat, /chat/stream, /health, /models) aktif durumdadır. TranslateGemma, Redis Cache ve PostgreSQL Analytics bileşenleri ise altyapı olarak hazır olup, dış bağımlılıkların (HF_TOKEN, Redis, PostgreSQL) kurulmasına bağlıdır.

Anahtar Kelimeler: RAG, LLM, Ollama, FAISS, FastAPI, Flutter, Selçuk Üniversitesi, Bilgi Asistanı

**ABSTRACT**

**COMPUTER ENGINEERING APPLICATIONS PROJECT**

**ARTIFICIAL INTELLIGENCE POWERED UNIVERSITY INFORMATION ASSISTANT: SELCUK AI ASSISTANT**

**Doğukan BALAMAN (203311066)**  \
**Ali YILDIRIM (203311008)**

**SELCUK UNIVERSITY**   \
**FACULTY OF TECHNOLOGY**  \
**DEPARTMENT OF COMPUTER ENGINEERING**

**Advisor: Prof. Dr. Nurettin DOĞAN**  \
**Advisor: Dr. Öğr. Üyesi Onur İNAN**

**2025, 50+ Pages**

**Jury**  \
**Prof. Dr. Nurettin DOĞAN**  \
**Dr. Öğr. Üyesi Onur İNAN**  \
**................................**

This study covers the design and development of an AI-powered information assistant for Selcuk University that provides 24/7 access to institutional knowledge. The system relies on a local LLM stack via Ollama and a Retrieval Augmented Generation (RAG) approach to produce reliable responses. The backend is implemented with FastAPI, while FAISS-based vector indexing is used for retrieval. The client application is built with Flutter to support iOS and Android.

A knowledge base of 645 documents was constructed from official university web sources. During the rescrape phase, 135 failed URLs were retried; 92 succeeded and 43 remained as permanent errors, yielding a 68.15% success rate. Core API endpoints are functional, while TranslateGemma, Redis Cache, and PostgreSQL Analytics remain optional due to external dependencies. The project demonstrates a modular architecture that can scale and evolve as more integrations are enabled.

Keywords: RAG, LLM, Ollama, FAISS, FastAPI, Flutter, Selcuk University, Information Assistant

**ÖNSÖZ**

Bu çalışma Selçuk Üniversitesi Teknoloji Fakültesi Bilgisayar Mühendisliği Bölümü'nde bütünleme projesi kapsamında hazırlanmıştır. Proje süresince katkı sağlayan danışman hocalarımıza, bölüm akademik kadrosuna ve destek veren ailelerimize teşekkür ederiz.

|  | Doğukan BALAMAN (203311066) • Ali YILDIRIM (203311008) |
| :---: | :---: |
|  | Konya / 2025 |

**İÇİNDEKİLER**

- ÖZET
- ABSTRACT
- ÖNSÖZ
- İÇİNDEKİLER
- SİMGELER VE KISALTMALAR
- 1. GİRİŞ
- 2. KAYNAK ARAŞTIRMASI
- 3. MATERYAL VE YÖNTEM
- 4. SİSTEM TASARIMI VE UYGULAMA
- 5. BULGULAR
- 6. SONUÇLAR VE ÖNERİLER
- KAYNAKLAR
- EKLER
- ÖZGEÇMİŞ

**SİMGELER VE KISALTMALAR**

API : Application Programming Interface  \
FAISS : Facebook AI Similarity Search  \
HF : Hugging Face  \
HTTP : Hypertext Transfer Protocol  \
HTTPS : Hypertext Transfer Protocol Secure  \
LLM : Large Language Model  \
NLP : Natural Language Processing  \
RAG : Retrieval Augmented Generation  \
SSE : Server-Sent Events  \
UI : User Interface

# 1. GİRİŞ

Selçuk Üniversitesi ölçek, fakülte çeşitliliği ve hizmet birimleri açısından Türkiye’nin en büyük kurumlarından biridir. Kurum genelindeki bilginin çok sayıda web sayfasına dağılmış olması, öğrencilerin ve personelin hızlı ve doğru bilgiye erişimini zorlaştırmaktadır. Bu çalışma, söz konusu problemi çözmek amacıyla Selçuk Üniversitesi özelinde eğitilebilir ve genişletilebilir bir yapay zeka bilgi asistanı tasarlamayı hedefler.

Bu bağlamda Selçuk AI Asistan projesi, yerel çalışabilen bir LLM sağlayıcısı (Ollama), RAG tabanlı getirim yaklaşımı ve mobil uygulama arayüzü ile uçtan uca bir çözüm sunar. Proje, veri gizliliğini koruyan, maliyet ve erişilebilirlik açısından avantaj sağlayan, modüler bir mimari üzerine kurulmuştur.

## 1.1. Problem Tanımı

- Üniversiteye ait bilgi kaynakları dağınıktır ve farklı alt alan adları üzerinde yayınlanmaktadır.
- 7/24 hizmet sağlayabilecek bir bilgi altyapısı bulunmamaktadır.
- Geleneksel arama yöntemleri kullanıcıya bağlamlı ve özetlenmiş yanıt üretmede yetersizdir.

## 1.2. Projenin Amacı

- Selçuk Üniversitesi hakkında güncel ve güvenilir bilgi sunan bir AI asistan geliştirmek.
- RAG yaklaşımı ile LLM yanıtlarının doğruluğunu artırmak.
- Flutter tabanlı mobil uygulama ile kullanıcı deneyimini iyileştirmek.
- Performans ve doğrulama metriklerini ölçülebilir hale getirmek.

## 1.3. Katkılar

- 645 dokümanlık kurumsal bilgi tabanı oluşturulmuştur.
- FAISS tabanlı RAG altyapısı ile kaynaklı yanıt akışı sağlanmıştır.
- FastAPI üzerinde modüler servis yapısı (LLM sağlayıcıları, cache, analytics) geliştirilmiştir.
- Flutter tabanlı mobil istemci ve çeviri ekranı entegre edilmiştir.

# 2. KAYNAK ARAŞTIRMASI

## 2.1. Büyük Dil Modelleri (LLM)

LLM'ler, büyük metin veri setleri üzerinde eğitilen ve doğal dil üretiminde yüksek performans sunan modellerdir. Projede yerel çalışma, veri gizliliği ve maliyet avantajları nedeniyle Ollama tabanlı modeller önceliklendirilmiştir. Model kataloğunda `llama3.2:3b`, `qwen2.5:7b`, `deepseek-r1:8b` gibi alternatifler tanımlıdır (bkz. `backend/providers/registry.py`).

## 2.2. Retrieval Augmented Generation (RAG)

RAG, LLM’lerin bilgi tabanından bağlam getirerek yanıt üretmesini sağlar. Bu yaklaşım, modelin “uydurma bilgi” üretme eğilimini azaltır. Projede RAG servisi, FAISS indeksleme ve çok dilli embedding modeli üzerinden çalışmaktadır.

## 2.3. FAISS ve Vektör İndeksleme

FAISS, yüksek boyutlu vektörler üzerinde hızlı benzerlik araması yapmaya olanak tanır. `rag_service.py` içinde FAISS indeks dosyaları (`index.faiss`, `metadata.json`, `index_meta.json`) yönetilmekte ve bağlam üretimi yapılmaktadır.

## 2.4. Web Scraping ve Bilgi Toplama

Kurumsal içerik, web scraping yoluyla toplanmıştır. Yeni robust scraper yapısı SSL fallback, yeniden deneme ve timeout mekanizmaları sunarak hata oranını azaltmıştır. Bu sayede 135 hatalı URL’den 92’si tekrar erişilebilir hale getirilmiştir.

## 2.5. Mobil Uygulama ve Flutter

Flutter, tek kod tabanıyla iOS ve Android hedeflemek için kullanılmıştır. GetX tabanlı state yönetimi ve SSE akışı ile gerçek zamanlı yanıt güncellemesi sağlanmaktadır.

## 2.6. Benzer Çalışmalar

Üniversite bilgi asistanları genellikle bulut tabanlı chatbot çözümlerine dayanır. Bu projede yerel LLM altyapısı seçilerek veri gizliliği artırılmış, kurum içi kullanım için bağımsız bir yapı hedeflenmiştir.

# 3. MATERYAL VE YÖNTEM

## 3.1. Geliştirme Ortamı

- Backend: Python 3.11, FastAPI
- LLM sağlayıcı: Ollama (yerel), HuggingFace (opsiyonel)
- RAG: FAISS + SentenceTransformers
- Frontend: Flutter 3.x, Dart
- Veri tabanı: FAISS indeks ve JSON metadata

## 3.2. Veri Toplama Süreci

Veri toplama, Selçuk Üniversitesi ve alt birimlerinin web sitelerinden web kazıma ile yapılmıştır. Metinler `backend/data/scraped/` dizininde saklanmış, metadata bilgileri `backend/data/rag/scraped/metadata.jsonl` dosyasında tutulmuştur.

## 3.3. Veri Temizleme ve Dönüştürme

Scraper çıktıları HTML gürültüsünden arındırılmış, paragraflar normalize edilmiş ve minimum uzunluk kontrolü yapılmıştır. Kısa veya boş içerikler “skipped” olarak işaretlenmiştir.

## 3.4. RAG İndeksleme

Varsayılan ayarlar (bkz. `backend/config.py`):
- RAG_CHUNK_SIZE: 500
- RAG_CHUNK_OVERLAP: 50
- RAG_TOP_K: 4
- Embedding modeli: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

## 3.5. Model Yönlendirme ve Sağlayıcılar

Model sağlayıcıları `providers/` katmanında soyutlanmıştır. Varsayılan sağlayıcı Ollama, alternatif sağlayıcı HuggingFace’tir. `ModelRegistry` sınıfı model alias ve katalog yönetimi yapmaktadır.

## 3.6. Değerlendirme Metrikleri

- Scraping başarı oranı
- API çalışabilirlik testleri
- RAG bağlam doğrulama (RAG guard mekanizması)
- Benchmark performans metrikleri (TTFT, belirteç/sn)

## 3.7. Test Yöntemi

Backend test dosyaları doğrudan `backend/` dizininde bulunmaktadır. `backend/tests` dizini bulunmadığından toplam test sayısı 8 olarak hesaplanmıştır (test_*.py).

# 4. SİSTEM TASARIMI VE UYGULAMA

## 4.1. Genel Mimari

**Şekil 4.1. Sistem Mimarisi**

[PLACEHOLDER: 3-tier architecture diyagramı]

**Çizim Talimatı:** draw.io ile çiz:
- Presentation: Flutter (Android/iOS)
- Application: FastAPI + RAG Engine
- Data: FAISS (645 docs) + Ollama (LLM sağlayıcı)

## 4.2. Backend Bileşeni

Backend bileşeni FastAPI üzerinde çalışır. CORS, model yönlendirme, RAG entegrasyonu ve SSE tabanlı stream yanıtlar ana mimariyi oluşturur.

**Kod Bloğu 4.1. FastAPI Ana Uygulama**

```python name=main.py url=https://github.com/esN2k/SelcukAiAssistant/blob/main/repo/backend/main.py
app = FastAPI(title="Selçuk AI Asistanı Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=not allow_all_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(translate_router, prefix="/api", tags=["translation"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])

ollama_provider = OllamaProvider()
huggingface_provider = HuggingFaceProvider()

providers: dict[str, ModelProvider] = {
    "ollama": ollama_provider,
    "huggingface": huggingface_provider,
}
model_registry = ModelRegistry(providers)
```

Bu blok, FastAPI uygulamasının kurulumu, CORS ayarları, router entegrasyonları ve LLM sağlayıcılarının kayıt altına alınma sürecini göstermektedir.

## 4.3. RAG Engine Bileşeni

RAG servisi FAISS tabanlı indeksleme ile bağlam üretir. Aşağıdaki kod parçası, getirim sürecinde bağlam ve alıntı listesi oluşturma mekanizmasını gösterir.

**Kod Bloğu 4.2. RAG Bağlam Üretimi**

```python name=rag_service.py url=https://github.com/esN2k/SelcukAiAssistant/blob/main/repo/backend/rag_service.py
    def get_context(
        self,
        query: str,
        top_k: Optional[int] = None,
    ) -> tuple[str, list[str]]:
        if not self.enabled:
            return "", []
        if not self.available:
            raise RuntimeError(self.error_message or "RAG servisi hazır değil.")
        docs = self.search(query, top_k=top_k)
        if not docs:
            return "", []

        context_parts: list[str] = []
        citations: list[str] = []
        for idx, doc in enumerate(docs, 1):
            citations.append(_citation_label(doc.metadata))
            context_parts.append(f"[{idx}] {doc.content}")
        return "\n\n".join(context_parts), citations
```

Bu parça, arama sonuçlarının numaralandırılması ve alıntı listesi üretimi üzerinden RAG bağlamını oluşturmaktadır.

## 4.4. TranslateGemma Bileşeni

TranslateGemma sağlayıcısı, özel chat template yapısı ile çeviri sağlar. Model yükleme ve metin çevirisi fonksiyonları aşağıdaki gibidir.

**Kod Bloğu 4.3. TranslateGemma Çeviri Çağrısı**

```python name=translate_provider.py url=https://github.com/esN2k/SelcukAiAssistant/blob/main/repo/backend/providers/translate_provider.py
    def translate(
        self,
        text: str,
        source_lang: str = "tr",
        target_lang: str = "en",
        max_new_tokens: int = 512,
    ) -> str:
        self._ensure_loaded()
        if self.processor is None or self.model is None:
            raise RuntimeError("TranslateGemma is not initialized.")

        source_lang = self._normalize_lang(source_lang)
        target_lang = self._normalize_lang(target_lang)

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "source_lang_code": source_lang,
                        "target_lang_code": target_lang,
                        "text": text,
                    }
                ],
            }
        ]
```

TranslateGemma modeli HF_TOKEN ve lisans onayı gerektirdiğinden test aşaması manuel olarak tamamlanacaktır.

## 4.5. API Tasarımı

**Çizelge 4.1. API Endpoint Listesi**

| Endpoint | Method | Açıklama | Durum |
|----------|--------|----------|-------|
| / | GET | Basit durum mesajı | ✅ |
| /health | GET | Sağlık kontrolü | ✅ |
| /health/ollama | GET | Ollama sağlık kontrolü | ✅ |
| /health/hf | GET | HF bağımlılık kontrolü | ✅ |
| /models | GET | Model listesi | ✅ |
| /chat | POST | Sohbet yanıtı | ✅ |
| /chat/stream | POST | SSE streaming sohbet | ✅ |
| /api/translate | POST | Metin çeviri | ⏭️ (HF_TOKEN) |
| /api/translate/image | POST | Görsel çeviri | ⏭️ (HF_TOKEN) |
| /api/translate/languages | GET | Dil listesi | ⏭️ (HF_TOKEN) |
| /admin/cache/stats | GET | Cache istatistikleri | ⏭️ (Redis) |
| /admin/analytics/popular | GET | Popüler sorular | ⏭️ (PostgreSQL) |
| /admin/analytics/hourly | GET | Saatlik istatistik | ⏭️ (PostgreSQL) |
| /admin/analytics/models | GET | Model istatistik | ⏭️ (PostgreSQL) |

*Kaynak: `backend/main.py`, `backend/api/endpoints/`*

## 4.6. Mobil Uygulama Bileşeni

Flutter istemcisi, sohbet arayüzü, ayarlar ve çeviri ekranı dahil olmak üzere modüler bir yapıya sahiptir. Aşağıdaki örnek, çeviri ekranının istek atma mekanizmasını gösterir.

**Kod Bloğu 4.4. Flutter Çeviri İsteği**

```dart name=translate_screen.dart url=https://github.com/esN2k/SelcukAiAssistant/blob/main/repo/lib/screen/translate_screen.dart
  Future<void> _translate() async {
    final text = _sourceController.text.trim();
    if (text.isEmpty) return;

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final locale = Pref.localeCode ?? L10n.fallbackLocale.languageCode;
      final payload = jsonEncode({
        'text': text,
        'source_lang': _sourceLang,
        'target_lang': _targetLang,
      });
      final response = await http
          .post(
            Uri.parse(BackendConfig.translateTextEndpoint),
            headers: {
              'Content-Type': 'application/json; charset=utf-8',
              'Accept-Language': locale,
            },
            body: payload,
          )
          .timeout(
            const Duration(seconds: 180),
            onTimeout: () => http.Response('Timeout', 408),
          );
```

Bu kod parçası, Flutter istemcisinin backend çeviri API’sine HTTP POST isteği oluşturduğunu göstermektedir.

## 4.7. Scraper ve Veri Toplama

Scraper katmanı, SSL fallback ve retry mekanizmaları ile geliştirilmiştir. Hatalı URL’lerin yeniden denenmesi için `scripts/rescrape_failed.py` aracı kullanılmaktadır.

## 4.8. Cache ve Analytics

Redis tabanlı cache servisi ve asyncpg tabanlı analytics servisi eklenmiştir. Ancak bu bileşenler için Redis ve PostgreSQL kurulumu gereklidir. Mevcut ortamda testler tamamlanmamıştır.

## 4.9. Güvenlik ve Hata Yönetimi

- RAG guard ile bağlama dayalı doğruluk kontrolü
- Timeout ve retry mekanizmaları
- Hata mesajlarının kullanıcıya anlaşılır şekilde iletilmesi

## 4.10. Yazılım Büyüklüğü

**Çizelge 4.2. Kod Satır Sayıları**

| Bileşen | Dosya Sayısı | Toplam Satır | Kaynak |
|---|---:|---:|---|
| Backend (Python) | 44 | 18,770 | `repo/backend/**/*.py` |
| Frontend (Dart) | 66 | 23,398 | `repo/lib/**/*.dart` |

# 5. BULGULAR

## 5.1. Scraping Sonuçları

**Çizelge 5.1. Rescrape Sonuçları (2026-01-17)**

| Metrik | Değer |
|---|---:|
| Toplam yeniden denenen URL | 135 |
| Başarılı | 92 |
| Başarı oranı | %68.15 |
| SSL bypass kullanılan | 74 |
| Kalıcı hata | 43 |

DNS hatası alınan subdomain’ler (36 adet) liste halinde raporlanmıştır:

akademik.selcuk.edu.tr, akademiktakvim.selcuk.edu.tr, bap.selcuk.edu.tr,
bilgisayar.selcuk.edu.tr, cukurovamyo.selcuk.edu.tr, cumramyo.selcuk.edu.tr,
duyuru.selcuk.edu.tr, ebe.selcuk.edu.tr, engelsiz.selcuk.edu.tr,
erasmus.selcuk.edu.tr, fbe.selcuk.edu.tr, ilahiyat.selcuk.edu.tr,
karapinarmyo.selcuk.edu.tr, konservatuar.selcuk.edu.tr, library.selcuk.edu.tr,
mevlanaenstitusu.selcuk.edu.tr, mevzuat.selcuk.edu.tr, mimtasarim.selcuk.edu.tr,
muhendislik.selcuk.edu.tr, ogrenci.selcuk.edu.tr, psikolojikdanisma.selcuk.edu.tr,
sagens.selcuk.edu.tr, saglik.selcuk.edu.tr, saglikmyo.selcuk.edu.tr,
sbe.selcuk.edu.tr, selcukluarastirmalari.selcuk.edu.tr, senato.selcuk.edu.tr,
sinav.selcuk.edu.tr, sosyalbilmyo.selcuk.edu.tr, spor.selcuk.edu.tr,
sudem.selcuk.edu.tr, taskentmyo.selcuk.edu.tr, teknikmyo.selcuk.edu.tr,
turkiyat.selcuk.edu.tr, yabancilar.selcuk.edu.tr, yok.selcuk.edu.tr

## 5.2. Knowledge Base Durumu

- Toplam doküman: 645 (`backend/data/scraped/`)
- Metadata girişleri: `backend/data/rag/scraped/metadata.jsonl`
- RAG indeks dosyaları: `backend/data/rag/index.faiss`, `index_meta.json`

## 5.3. Test Sonuçları

Backend testleri doğrudan `backend/` altında yer almaktadır:

**Çizelge 5.2. Test Dosyaları**

| Test Dosyası | Amaç |
|---|---|
| test_main.py | API kontrat ve sağlık kontrol testleri |
| test_extended.py | Ollama servis uçları ve hata senaryoları |
| test_model.py | Model çalıştırma senaryoları |
| test_rag_guard.py | RAG guard doğrulaması |
| test_critical_guard.py | Kritik bilgi doğrulaması |
| test_critical_facts.py | Kritik bilgi seti doğrulaması |
| test_reasoning_cleanup.py | Yanıt temizleme testleri |
| test_response_cleaner.py | Yanıt temizleme doğrulaması |

Toplam test sayısı: **8** (backend/tests dizini bulunmamaktadır).

## 5.4. Performans Bulguları (Benchmark)

Repository içindeki benchmark raporundan alınan gerçek veriler:

- Model: `ollama:llama3.2:3b`
- 12 örnek koşumda ort. TTFT: 5180.24 ms
- Ort. belirteç/sn: 5.41
- Ort. toplam süre: 8.643 s

Bu veriler `docs/reports/BENCHMARK_RAPORU.md` dosyasında yer almaktadır.

## 5.5. API Doğrulama

- /health, /models, /chat, /chat/stream uçları çalışır durumdadır.
- TranslateGemma uçları HF_TOKEN gerektirir ve test edilmemiştir.
- Cache ve analytics uçları Redis/PostgreSQL kurulumu gerektirir.

## 5.6. Kısıtlar ve Sorunlar

- DNS hataları nedeniyle bazı alt alan adlarına erişim mümkün olmamıştır.
- TranslateGemma modeli lisans onayı ve HF_TOKEN gerektirdiğinden test aşaması manuel kalmıştır.
- Redis ve PostgreSQL servisleri ortam kısıtları nedeniyle test edilememiştir.

# 6. SONUÇLAR VE ÖNERİLER

## 6.1. Sonuçlar

Bu çalışma, Selçuk Üniversitesi için yerel LLM tabanlı, RAG destekli ve mobil erişimli bir bilgi asistanı mimarisinin kurulabileceğini göstermiştir. 645 dokümanlık bilgi tabanı ve FAISS indeksleme ile bağlamlı cevap üretimi sağlanmıştır. FastAPI tabanlı API katmanı, modüler servis yaklaşımı ile genişletilebilir bir altyapı sunar.

## 6.2. Öneriler

- TranslateGemma entegrasyonu için lisans onayı ve HF_TOKEN tamamlanmalıdır.
- Redis cache ile tekrarlı sorularda performans artırılmalıdır.
- PostgreSQL analytics ile kullanım istatistikleri raporlanmalıdır.
- DNS hatası veren subdomain’ler için üniversite IT birimi ile alan adı doğrulaması yapılmalıdır.

# KAYNAKLAR

1. FastAPI Documentation, https://fastapi.tiangolo.com
2. Ollama Documentation, https://ollama.com/docs
3. FAISS Documentation, https://github.com/facebookresearch/faiss
4. LangChain Documentation, https://python.langchain.com
5. Hugging Face Transformers, https://huggingface.co/docs/transformers
6. Flutter Documentation, https://docs.flutter.dev
7. Selçuk AI Asistan Benchmark Raporu, `docs/reports/BENCHMARK_RAPORU.md`

# EKLER

**Ek-1. Rescrape Özet Çıktısı**

```
🔄 135 hatalı URL bulundu. Tekrar scraping...

📊 Sonuç: 92/135 başarılı
✅ Başarılı: 92 URL (SSL bypass: 74)
❌ Kalıcı hatalar: 43 URL
```

**Ek-2. API Test Örneği**

```
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Selçuk Üniversitesi nerede?"}],
    "model": "qwen2.5:3b"
  }'
```

**Ek-3. Proje Dizin Yapısı (Özet)**

```
repo/
├─ backend/
│  ├─ main.py
│  ├─ rag_service.py
│  ├─ providers/
│  ├─ api/endpoints/
│  └─ data/
└─ lib/
   ├─ screen/
   ├─ controller/
   └─ services/
```

# ÖZGEÇMİŞ

**Doğukan BALAMAN (203311066)**  \
Selçuk Üniversitesi Teknoloji Fakültesi Bilgisayar Mühendisliği öğrencisi. Yapay zeka ve backend sistemleri üzerine çalışmaktadır.

**Ali YILDIRIM (203311008)**  \
Selçuk Üniversitesi Teknoloji Fakültesi Bilgisayar Mühendisliği öğrencisi. Mobil uygulama geliştirme ve kullanıcı deneyimi alanlarına ilgi duymaktadır.
