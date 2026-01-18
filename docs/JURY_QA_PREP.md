# ❓ JÜRİ SORU-CEVAP HAZIRLIK DOKÜMANI

## 🎯 KULLANIM

Bu dokümanı sunum öncesi **3 kez oku**. Soruları ezberle, cevapları
kafanda netleştir. Her soruya hazırlıklı ol.

**Çalışma Yöntemi:**
1. Soruyu oku, gözlerini kapat, cevabını söyle
2. Yazılı cevapla karşılaştır
3. Eksik kaldığın yerleri tekrar çalış
4. Arkadaşınla karşılıklı prova yap

---

## 📚 SORU KATEGORİLERİ

---

## 1️⃣ TEKNİK SORULAR (15 soru)

---

### SORU 1.1: "Backend'deki `main.py` dosyasının 157. satırı ne yapıyor?"

**CEVAP STRATEJİSİ:**
- Sakin kal, panik yapma
- "Bir saniye koduma bakayım" de (zaman kazan)
- Eğer biliyorsan net açıkla
- Bilmiyorsan genel fonksiyonu açıkla

**ÖRNEK CEVAP:**
> "Bu satırda muhtemelen mesaj normalizasyonu yapılıyor. Eğer 
> kullanıcının gönderdiği mesaj listesinde 'system' rolü yoksa,
> varsayılan sistem promptu otomatik ekleniyor. Bu sayede AI'ya
> 'Sen Selçuk Üniversitesi asistanısın' talimatı her zaman veriliyor."

**DETAY İSTERSE:**
> "Bu `normalize_messages()` fonksiyonunun bir parçası.
> `utils.py` dosyasında detaylı açıklaması var."

**BİLMİYORSAN:**
> "Bu kısmı tam hatırlamıyorum ama fonksiyonun genel amacı
> mesajları normalize etmek. Detayını koddan gösterebilirim."

---

### SORU 1.2: "RAG nedir, nasıl çalışıyor?"

**CEVAP:**
> "RAG, Retrieval-Augmented Generation'ın kısaltması.
> Türkçesi: 'Bilgi getirerek üretim yapma.'

Şöyle çalışıyor:

**ADIM 1: Belge Hazırlama**
Selçuk Üniversitesi dokümanlarını topluyoruz (bölüm bilgileri,
akademik takvim, sık sorulan sorular vb.)

**ADIM 2: Vektörleştirme**
Bu belgeleri küçük parçalara (chunk) bölüp sayısal vektörlere
dönüştürüyoruz. Bunun için `paraphrase-multilingual-MiniLM`
embedding modeli kullanıyoruz.

**ADIM 3: Sorgulama**
Kullanıcı soru sorduğunda, soru da vektöre dönüştürülüp
FAISS ile en benzer 4 belge bulunuyor.

**ADIM 4: Yanıt Üretme**
Bulunan belgeler + Soru birlikte Ollama'ya gönderiliyor.
Model, verilen kaynaklardan cevap üretiyor.

**FAYDA:** AI uydurma yapmaz, her yanıt kaynaklıdır.
Kullanıcı 'Bu bilgi nereden geldi?' diye sorabilir."

---

### SORU 1.3: "FAISS nedir, neden kullandın?"

**CEVAP:**
> "FAISS, Facebook AI Research'ün geliştirdiği açık kaynak
> vektör arama kütüphanesi. 'Facebook AI Similarity Search'
> kelimelerinin kısaltması.

**Neden FAISS:**
1. **Hızlı:** Milyonlarca vektörde milisaniye düzeyinde arama
2. **Yerel:** Bulut servisi gerektirmiyor (Pinecone, Weaviate gibi)
3. **Ücretsiz:** Açık kaynak, lisans ücreti yok
4. **Python uyumlu:** pip install ile kolay kurulum
5. **Kanıtlanmış:** Meta (Facebook) production'da kullanıyor

**Alternatifler:**
- Pinecone: Bulut tabanlı, ücretli
- Milvus: Daha karmaşık kurulum
- ChromaDB: Daha yeni, az test edilmiş"

---

### SORU 1.4: "Neden Flutter kullandın?"

**CEVAP:**
> "Flutter'ı seçmemin **üç ana nedeni** var:

**1. TEK KOD TABANI:**
Bir kez yazıp Android, iOS, Windows, Web'de çalıştırabiliyorum.
Native geliştirmede her platform için ayrı kod gerekir.

**2. PERFORMANS:**
Flutter, native'e yakın performans sunuyor. Dart dili ahead-of-time
(AOT) compile ediliyor, JavaScript köprüsü yok.

**3. MODERN UI:**
Material Design 3 hazır widget'ları var. GetX ile state management
çok kolay. Hot reload ile anlık değişiklik görebiliyorum.

**Alternatifler neden seçilmedi:**
- React Native: JavaScript köprüsü performans kaybı yaratıyor
- Native (Swift/Kotlin): Her platform için ayrı kod yazılması gerekiyor
- Web-only: Mobil deneyim kısıtlı"

---

### SORU 1.5: "Neden FastAPI kullandın?"

**CEVAP:**
> "FastAPI'yi seçmemin nedenleri:

**1. PERFORMANS:**
Python web framework'leri içinde en hızlısı. Async/await
desteği ile yüksek throughput sağlıyor.

**2. TYPE SAFETY:**
Pydantic ile otomatik veri doğrulama yapılıyor.
Yanlış formatta istek gelirse hata dönüyor.

**3. STREAMING:**
Server-Sent Events (SSE) built-in destekliyor.
LLM yanıtlarını token token akıtabiliyorum.

**4. AUTOMATIC DOCS:**
`/docs` endpoint'inde Swagger UI otomatik oluşuyor.
API'yi test etmek çok kolay.

**Karşılaştırma:**
- Flask: Async yok, daha eski
- Django: Çok ağır, API-first değil
- Express.js: Python ekosisteminden yararlanamama"

---

### SORU 1.6: "Neden Ollama kullandın? Neden OpenAI değil?"

**CEVAP:**
> "Ollama'yı seçmemin **birincil nedeni GİZLİLİK**.

**GİZLİLİK:**
- Tüm veri işleme yerel olarak yapılıyor
- Öğrenci bilgileri, sınav soruları dışarıya gitmiyor
- KVKK/GDPR uyumlu

**YEREL ÇALIŞMA:**
- İnternet bağlantısı gerekmiyor
- Üniversite güvenlik duvarı arkasında çalışabilir
- Maliyet yok (API ücreti yok)

**TEKNİK AVANTAJLAR:**
- Kolay kurulum (`ollama pull llama3.2`)
- Çoklu model desteği (Llama, Mistral, Qwen)
- GPU/CPU otomatik optimizasyon
- REST API ile kolay entegrasyon

**Neden OpenAI değil:**
1. Veri gizliliği riski (veriler yurt dışına gider)
2. Maliyet (token başına ücret)
3. Bağımlılık (servis kesintisi riski)
4. Yasal sorunlar (KVKK)"

---

### SORU 1.7: "Accuracy Guard nasıl çalışıyor?"

**CEVAP:**
> "Accuracy Guard, **kritik bilgiler için otomatik doğrulama** sistemi.

**Korunan Bilgiler:**
1. Selçuk Üniversitesi konumu: **Konya**
2. Kuruluş yılı: **1975**
3. Kampüs isimleri: Alaeddin Keykubat, Ardıçlı

**Çalışma Prensibi:**

**ADIM 1:** Kullanıcı sorusu kategorize edilir
- Konum sorusu mu?
- Kuruluş yılı sorusu mu?

**ADIM 2:** Model yanıtı kontrol edilir
- Yanlış şehir var mı? (İzmir, Ankara, İstanbul)
- Yanlış yıl var mı? (1976, 1982)

**ADIM 3:** Düzeltme uygulanır
- Yanlış bilgi tespit edilirse → Doğrusuyla değiştirilir
- Eksik bilgi varsa → Eklenir

**ADIM 4:** Log kaydedilir
- `accuracy_guard_corrected` eventi loglanır
- Hangi yanlış bilginin düzeltildiği kaydedilir

**Garanti:** Model ne derse desin, Konya bilgisi HER ZAMAN doğru verilir."

---

### SORU 1.8: "Provider pattern nedir, neden kullandın?"

**CEVAP:**
> "Provider pattern, **farklı LLM sağlayıcılarını** ortak bir
> arayüz üzerinden kullanmamı sağlayan tasarım deseni.

**Nasıl Çalışıyor:**

```
BaseProvider (Soyut Sınıf)
    ├── OllamaProvider
    ├── HuggingFaceProvider (gelecekte)
    └── TurkcellLLMProvider (gelecekte)
```

**Faydası:**
1. Yeni model eklemek kolay (sadece yeni provider yaz)
2. Model değiştirmek tek satır değişiklik
3. Test yazmak kolay (mock provider kullanılabilir)
4. Kod tekrarı yok

**Örnek:**
Yarın Turkcell LLM kullanmak istersem, sadece
`TurkcellLLMProvider` sınıfı yazıp `registry`'ye ekliyorum.
Ana kodda değişiklik yapmama gerek yok."

---

### SORU 1.9: "GetX nedir, neden kullandın?"

**CEVAP:**
> "GetX, Flutter için **state management** kütüphanesi.

**Neden GetX:**
1. **Basit:** Provider, Riverpod'a göre daha az boilerplate
2. **Hızlı:** Performans optimizasyonları hazır
3. **All-in-one:** Route management, dependency injection dahil
4. **Reactive:** `Obx()` ile otomatik UI güncelleme

**Alternatifler:**
- Provider: Daha verbose, boilerplate fazla
- Riverpod: Öğrenme eğrisi dik
- Bloc: Çok karmaşık, küçük projeler için overkill

**Kullanım Örneği:**
```dart
// Controller'da
var messages = <Message>[].obs;

// UI'da
Obx(() => ListView(children: controller.messages))
```

Mesaj eklendiğinde UI otomatik güncellenir."

---

### SORU 1.10: "SSE (Server-Sent Events) nedir?"

**CEVAP:**
> "SSE, sunucudan istemciye **tek yönlü gerçek zamanlı** veri akışı.

**Nasıl Çalışıyor:**
1. İstemci bir HTTP bağlantısı açar
2. Sunucu bu bağlantıyı açık tutar
3. Sunucu hazır oldukça veri gönderir
4. İstemci gelen veriyi anlık işler

**Projede Kullanımı:**
LLM yanıtları token token geliyor. Her token geldiğinde
UI'da mesaj güncelleniyor. Kullanıcı yanıtın oluştuğunu
canlı olarak görüyor.

**WebSocket'ten Farkı:**
- SSE: Tek yönlü (sunucu → istemci), HTTP tabanlı
- WebSocket: Çift yönlü, ayrı protokol

SSE bu proje için yeterli çünkü LLM -> Kullanıcı akışı var."

---

### SORU 1.11: "Embedding nedir?"

**CEVAP:**
> "Embedding, **metni sayısal vektöre dönüştürme** işlemi.

**Örnek:**
'Selçuk Üniversitesi Konya'da' → [0.23, -0.45, 0.12, ...]

**Neden Gerekli:**
Bilgisayarlar metin anlayamaz, sayı anlar. Embedding ile
metinler sayısal uzayda temsil edilir. Benzer metinler
birbirine yakın vektörler olur.

**Projede Kullanımı:**
RAG'da dokümanlar ve sorular embedding'e dönüştürülüyor.
FAISS bu vektörler arasında benzerlik araması yapıyor.

**Model:**
`paraphrase-multilingual-MiniLM-L12-v2` kullanıyorum.
Türkçe dahil 50+ dil destekliyor."

---

### SORU 1.12: "Test coverage'ınız nedir?"

**CEVAP:**
> "Backend için **93 test** yazıldı ve hepsi geçiyor.

**Test Kategorileri:**
1. **Unit testler:** Fonksiyonlar ayrı ayrı test ediliyor
2. **Integration testler:** API endpoint'leri test ediliyor
3. **Accuracy testler:** Kritik bilgiler doğrulanıyor

**Önemli Test Dosyaları:**
- `test_main.py`: API endpoint testleri
- `test_accuracy_guard.py`: Doğruluk kontrol testleri
- `test_critical_facts.py`: Konya, 1975 bilgi testleri
- `test_rag_service.py`: RAG servisi testleri

**CI/CD:**
Her PR'da otomatik test çalışıyor. Test geçmeden
kod merge edilemiyor."

---

### SORU 1.13: "Güvenlik önlemleri neler?"

**CEVAP:**
> "Üç katmanlı güvenlik:

**1. VERİ GÜVENLİĞİ:**
- Tüm işlem yerel (Ollama)
- Dış API çağrısı yok
- Kullanıcı verileri sunucu dışına çıkmaz

**2. GİRDİ DOĞRULAMA:**
- Pydantic ile tip kontrolü
- Maksimum mesaj uzunluğu limiti
- SQL/XSS injection koruması

**3. API GÜVENLİĞİ:**
- CORS koruması (izinli origin'ler)
- Rate limiting (hazırlanabilir)
- Hassas bilgiler .env dosyasında

**4. ÇIKTI KONTROLÜ:**
- Accuracy Guard ile yanlış bilgi engelleme
- Response cleaner ile zararlı içerik temizleme"

---

### SORU 1.14: "Docker kullanıyor musun?"

**CEVAP:**
> "Evet, `docker-compose.yml` dosyası mevcut.

**Servisler:**
1. `backend`: FastAPI uygulaması
2. `ollama`: LLM servisi (opsiyonel)

**Avantajları:**
- Tek komutla (`docker-compose up`) tüm sistem ayağa kalkar
- Ortam bağımsız (hangi bilgisayarda olursa olsun çalışır)
- Production deploy için hazır

**Şu an durum:**
Development'ta Docker olmadan çalışıyorum (daha hızlı debug).
Production için Docker image hazır."

---

### SORU 1.15: "Prompt engineering yaptın mı?"

**CEVAP:**
> "Evet, `prompts.py` dosyasında detaylı prompt tasarımı var.

**System Prompt İçeriği:**
1. Asistanın kimliği: 'Sen Selçuk Üniversitesi AI asistanısın'
2. Görev tanımı: Öğrencilere yardım et
3. Kritik bilgiler: Konya, 1975, kampüs isimleri
4. Davranış kuralları: Nazik ol, kaynak göster, uydurma yapma

**Prompt Türleri:**
- System prompt: Genel talimatlar
- RAG prompt: Kaynak kullanma talimatları
- Strict mode prompt: Kaynak yoksa 'bilmiyorum' de

**Optimizasyonlar:**
- Türkçe yanıt verme talimatı
- Kaynak gösterme formatı
- Emoji kullanım kuralları"

---

## 2️⃣ MİMARİ SORULAR (10 soru)

---

### SORU 2.1: "Proje mimarisi nasıl?"

**CEVAP:**
> "Üç katmanlı mimari:

```
┌─────────────┐
│   Flutter   │  → Kullanıcı Arayüzü (Dart)
│   Frontend  │
└──────┬──────┘
       │ HTTP/SSE
       ▼
┌─────────────┐
│   FastAPI   │  → Backend API (Python)
│   Backend   │
└──────┬──────┘
       │
       ├──────► Ollama (Yerel LLM)
       │
       └──────► FAISS (RAG Vektör DB)
```

**Veri Akışı:**
1. Kullanıcı mesaj yazar → Flutter
2. HTTP POST → FastAPI
3. RAG sorgusu → FAISS
4. LLM çağrısı → Ollama
5. SSE stream → Flutter
6. UI güncelleme"

---

### SORU 2.2: "Neden monolith, neden microservice değil?"

**CEVAP:**
> "Bu proje ölçeği için **monolith yeterli**.

**Monolith Avantajları:**
1. Basit deployment (tek uygulama)
2. Kolay debug (tek log)
3. Az overhead (network call yok)
4. Hızlı geliştirme (tek repo)

**Microservice Ne Zaman:**
- Takım büyükse (5+ developer)
- Farklı diller kullanılacaksa
- Bağımsız ölçekleme gerekiyorsa

**Gelecekte:**
Proje büyürse, Docker Compose ile kolayca microservice'lere
ayrılabilir. Örneğin: RAG ayrı servis, LLM ayrı servis."

---

### SORU 2.3: "Veritabanı kullanıyor musun?"

**CEVAP:**
> "İki farklı veri saklama yöntemi var:

**1. FAISS (Vektör Veritabanı):**
- RAG için doküman vektörleri
- Dosya tabanlı (`index.faiss`, `index.pkl`)
- Kalıcı, disk'te saklanıyor

**2. Flutter Yerel Depolama:**
- Hive: Sohbet geçmişi
- SharedPreferences: Ayarlar

**Neden SQL/NoSQL yok:**
- Bu proje için gerekli değil
- Kullanıcı yönetimi yok
- Sohbet geçmişi yerel cihazda yeterli

**Gelecekte:**
Çoklu kullanıcı desteği eklenirse PostgreSQL eklenebilir."

---

### SORU 2.4: "Ölçeklenebilir mi?"

**CEVAP:**
> "Evet, horizontally scale edilebilir.

**Backend:**
- Stateless tasarım (session yok)
- Birden fazla instance çalıştırılabilir
- Load balancer arkasına konulabilir

**FAISS:**
- Sharding destekliyor
- Büyük veri setleri için optimize

**Ollama:**
- Cluster kurulabilir
- GPU kaynak paylaşımı mümkün

**Pratik Örnek:**
Şu an tek sunucu yeterli. 1000+ eşzamanlı kullanıcı
olursa 3-4 backend instance + Redis cache eklenebilir."

---

### SORU 2.5: "Hata yönetimi nasıl?"

**CEVAP:**
> "Üç seviyeli hata yönetimi:

**1. BACKEND:**
- Try-except blokları
- HTTP status kodları (400, 500, vb.)
- Detaylı hata mesajları
- Logging ile hata kaydı

**2. FLUTTER:**
- GetX error handling
- Snackbar ile kullanıcı bilgilendirme
- Retry mekanizması

**3. ACCURACY GUARD:**
- Yanlış bilgi tespit → Düzeltme
- Düzeltme yapılamıyorsa → Genel yanıt

**Log Formatı:**
```
[2025-01-15 12:00:00] ERROR main.py:157 - Ollama timeout
[2025-01-15 12:00:01] INFO accuracy_guard.py - Corrected: izmir→konya
```"

---

### SORU 2.6: "API versiyonlama var mı?"

**CEVAP:**
> "Şu an tek versiyon (`/v1` implicit).

**Endpoint'ler:**
- `/health` - Sağlık kontrolü
- `/chat` - Sohbet
- `/chat/stream` - Streaming sohbet
- `/models` - Model listesi

**Gelecekte:**
Breaking change olursa `/v2/chat` gibi yeni endpoint
eklenebilir. Eski versiyon bir süre korunur."

---

### SORU 2.7: "Caching var mı?"

**CEVAP:**
> "Şu an limited caching var:

**Mevcut:**
- FAISS index memory'de (ilk yüklemeden sonra hızlı)
- Embedding model memory'de (tekrar yükleme yok)

**Yok (henüz):**
- Response cache (aynı soru → aynı cevap)
- Redis/Memcached

**Neden yok:**
- LLM yanıtları değişken (temperature)
- Her soru benzersiz bağlam
- Şu an performans yeterli

**Gelecekte:**
Sık sorulan sorular için Redis cache eklenebilir."

---

### SORU 2.8: "Monitoring/Logging nasıl?"

**CEVAP:**
> "Python `logging` modülü kullanıyorum.

**Log Seviyeleri:**
- DEBUG: Geliştirme detayları
- INFO: Normal operasyonlar
- WARNING: Dikkat gerektiren durumlar
- ERROR: Hatalar

**Log İçeriği:**
- Timestamp
- Dosya ve satır numarası
- Mesaj

**Örnek:**
```
[INFO] main.py:45 - Chat request received
[INFO] rag_service.py:78 - Found 4 relevant documents
[WARNING] accuracy_guard.py:92 - Corrected city: izmir→konya
```

**Production için:**
- Log rotation (dosya boyutu limiti)
- Centralized logging (ELK stack)
- Metrics (Prometheus)"

---

### SORU 2.9: "Deployment nasıl yapılır?"

**CEVAP:**
> "İki yöntem:

**1. Manuel Deployment:**
```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Flutter
flutter build web/android/windows
```

**2. Docker Deployment:**
```bash
docker-compose up -d
```

**Production Önerisi:**
1. Docker image build
2. Container registry'ye push
3. Kubernetes veya Docker Swarm ile deploy
4. Nginx reverse proxy
5. SSL/TLS sertifikası"

---

### SORU 2.10: "CI/CD pipeline var mı?"

**CEVAP:**
> "Evet, GitHub Actions ile CI/CD kurulu.

**Backend CI:**
1. Kod push edildiğinde tetiklenir
2. Python kurulumu
3. Bağımlılık yükleme
4. Ruff (linting)
5. Mypy (type check)
6. Pytest (testler)

**Flutter CI:**
1. Flutter kurulumu
2. pub get
3. flutter analyze
4. flutter test
5. flutter build

**Merge Kuralı:**
Tüm CI check'ler geçmeden PR merge edilemiyor."

---

## 3️⃣ PROJE YÖNETİMİ SORULARI (5 soru)

---

### SORU 3.1: "Projeyi ne kadar sürede yaptın?"

**CEVAP:**
> "Aktif geliştirme yaklaşık **3 ay** sürdü.

**Zaman Çizelgesi:**
- 1. Ay: Araştırma, mimari tasarım, backend temeli
- 2. Ay: RAG sistemi, Ollama entegrasyonu, testler
- 3. Ay: Flutter UI, entegrasyon, dokümantasyon

**Toplam Commit:** 100+ commit
**Kod Satırı:** Backend ~3000, Flutter ~5000"

---

### SORU 3.2: "Hangi zorlukları yaşadın?"

**CEVAP:**
> "Üç ana zorluk yaşadım:

**1. TÜRKÇE NLP:**
- Türkçe embedding modeli bulmak zor
- Çoğu model İngilizce optimize
- Çözüm: Multilingual model kullandım

**2. OLLAMA MODEL YÖNETİMİ:**
- Model boyutları büyük (4-7 GB)
- GPU bellek yönetimi
- Çözüm: Küçük modeller (3B) tercih ettim

**3. RAG CHUNK BOYUTU:**
- Çok küçük: Bağlam eksik
- Çok büyük: Irrelevant bilgi
- Çözüm: 500 karakter, 50 overlap deneysel belirlendi"

---

### SORU 3.3: "Tek başına mı yaptın?"

**CEVAP:**
> "Evet, projeyi **tek başıma** geliştirdim.

**Kanıtlar:**
- GitHub'da tüm commit'ler benim adıma
- Kod stili tutarlı
- Dokümantasyon aynı üslupla

**Yardım Aldığım Kaynaklar:**
- FastAPI, Flutter resmi dokümantasyonu
- LangChain tutorials
- Stack Overflow
- GitHub Copilot (bazı kod tamamlamaları)"

---

### SORU 3.4: "Proje gerçek hayatta kullanılabilir mi?"

**CEVAP:**
> "**MVP olarak hazır**, production için ek çalışma gerekli.

**Şu an:**
✅ Temel sohbet çalışıyor
✅ RAG kaynak gösteriyor
✅ Accuracy Guard aktif
✅ Testler geçiyor

**Production için gerekli:**
- [ ] Kullanıcı yönetimi (authentication)
- [ ] Rate limiting
- [ ] Load balancing
- [ ] Monitoring (Prometheus/Grafana)
- [ ] Yedekleme stratejisi
- [ ] SLA tanımları

**Pilot Uygulama:**
Üniversite onayıyla küçük bir pilot yapılabilir."

---

### SORU 3.5: "Gelecek planların neler?"

**CEVAP:**
> "Kısa ve uzun vadeli planlarım var:

**Kısa Vadeli (3 ay):**
- Sesli asistan özelliği
- Takvim entegrasyonu
- Push notification

**Uzun Vadeli (1 yıl):**
- Turkcell LLM entegrasyonu
- Fine-tuning (Selçuk Üniversitesi verisiyle)
- Çoklu dil desteği
- Diğer üniversitelere adapte etme

**Hayalim:**
Tüm Türkiye üniversitelerinde kullanılan yerli ve milli
bir akademik asistan platformu."

---

## 4️⃣ GİZLİLİK VE ETİK SORULAR (5 soru)

---

### SORU 4.1: "KVKK uyumlu mu?"

**CEVAP:**
> "Evet, KVKK prensiplerine uygun tasarlandı.

**Uyum Noktaları:**
1. **Veri Minimizasyonu:** Sadece gerekli veri işleniyor
2. **Yerel İşleme:** Veri yurt dışına gitmiyor
3. **Şeffaflık:** Kullanıcı ne işlendiğini biliyor
4. **Güvenlik:** Şifreli iletişim, güvenli depolama

**Dikkat:**
Kullanıcı profili oluşturulmuyor, kişisel veri saklanmıyor.
Sohbet geçmişi sadece kullanıcının cihazında."

---

### SORU 4.2: "Yanıltıcı bilgi riski?"

**CEVAP:**
> "Risk minimize edildi ama sıfır değil.

**Önlemler:**
1. **RAG:** Kaynaklara dayalı yanıt
2. **Strict Mode:** Kaynak yoksa 'bilmiyorum'
3. **Accuracy Guard:** Kritik bilgi düzeltme
4. **Disclaimer:** 'Tıbbi/hukuki tavsiye değildir' uyarısı

**Kalan Risk:**
- RAG kaynakları güncel olmayabilir
- Nadir edge case'ler

**Çözüm:**
Düzenli kaynak güncellemesi + kullanıcı geri bildirimi"

---

### SORU 4.3: "Telif hakkı sorunları?"

**CEVAP:**
> "Kullandığım tüm kaynaklar açık kaynak:

**Lisanslar:**
- Ollama: MIT License
- FastAPI: MIT License
- Flutter: BSD License
- FAISS: MIT License
- LangChain: MIT License

**RAG Kaynakları:**
- Selçuk Üniversitesi kamuya açık bilgileri
- Kendi yazdığım dokümantasyon

**Dikkat:**
Ticari LLM (OpenAI, Anthropic) kullanmıyorum,
lisans sorunu yok."

---

### SORU 4.4: "Kötüye kullanım riski?"

**CEVAP:**
> "Potansiyel riskler ve önlemler:

**Risk 1: Spam/Abuse**
- Önlem: Rate limiting (hazırlanabilir)

**Risk 2: Zararlı İçerik Üretimi**
- Önlem: System prompt ile kısıtlama
- Önlem: Response filtering

**Risk 3: Veri Sızıntısı**
- Önlem: Yerel işleme, dış API yok

**Gelecekte:**
- Content moderation API
- Anomaly detection
- Kullanıcı raporlama sistemi"

---

### SORU 4.5: "Açık kaynak mı?"

**CEVAP:**
> "Evet, **MIT lisansı** ile GitHub'da yayında.

**Ne Anlama Geliyor:**
- Herkes inceleyebilir
- Fork'layabilir
- Kendi projelerinde kullanabilir
- Ticari kullanım serbest

**Neden Açık Kaynak:**
- Şeffaflık
- Topluluk katkısı
- Akademik referans olabilmesi
- Diğer üniversitelerin adapte edebilmesi

**GitHub:** https://github.com/esN2k/SelcukAiAssistant"

---

## 5️⃣ ZOR/TUZAK SORULAR (5 soru)

---

### SORU 5.1: "Bu zaten ChatGPT değil mi? Farkı ne?"

**CEVAP:**
> "Hayır, **beş temel fark** var:

**1. GİZLİLİK:**
ChatGPT: Veriler OpenAI sunucularına gider
Biz: Tüm işlem yerel

**2. AKADEMİK ODAK:**
ChatGPT: Genel amaçlı
Biz: Selçuk Üniversitesi'ne özel içerik

**3. KAYNAK GÖSTERİMİ:**
ChatGPT: Kaynak göstermez
Biz: RAG ile her yanıtta kaynak

**4. MALİYET:**
ChatGPT: API ücreti var
Biz: Tamamen ücretsiz (yerel)

**5. DOĞRULUK GARANTİSİ:**
ChatGPT: Hallucination yapabilir
Biz: Accuracy Guard ile kritik bilgiler korumalı"

---

### SORU 5.2: "Model küçük, kaliteli cevap verebilir mi?"

**CEVAP:**
> "Evet, küçük model bu kullanım için **yeterli**.

**Neden:**
1. **Dar Alan:** Genel sohbet değil, üniversite soruları
2. **RAG Desteği:** Model bilgiyi üretmiyor, var olan bilgiyi sunuyor
3. **Basit Sorular:** 'Selçuk nerede?' gibi faktüel sorular

**Büyük Model Ne Zaman Gerekli:**
- Karmaşık reasoning
- Kod yazma
- Çoklu adım problem çözme

Bu proje için Llama 3.2 3B **fazlasıyla yeterli**."

---

### SORU 5.3: "Neden fine-tuning yapmadın?"

**CEVAP:**
> "Fine-tuning yerine RAG tercih ettim, nedenleri:

**Fine-tuning Dezavantajları:**
1. Çok veri gerekli (binlerce örnek)
2. GPU yoğun işlem
3. Güncelleme zor (her değişiklikte yeniden train)
4. Hallucination riski azalmaz

**RAG Avantajları:**
1. Az veri ile çalışır
2. CPU'da çalışır
3. Kaynak güncelleme kolay (JSON değiştir)
4. Kaynak gösterimi mümkün
5. Hallucination minimize

**Gelecekte:**
Daha fazla veri toplandığında LoRA fine-tuning
denenebilir."

---

### SORU 5.4: "Başka biri de aynısını yapmış olabilir mi?"

**CEVAP:**
> "Benzer projeler olabilir ama **bu proje benzersiz**:

**Özgün Yönler:**
1. Selçuk Üniversitesi'ne özel
2. Accuracy Guard sistemi (kendi tasarımım)
3. Türkçe odaklı prompt engineering
4. Provider pattern ile modüler mimari

**Araştırdım:**
- Türkiye'de benzer açık kaynak proje bulamadım
- Üniversiteye özel AI asistan projesi az

**Fark:**
Kod bir yerden kopyalanmadı. Mimari kararlar,
test yazımı, dokümantasyon hep orijinal."

---

### SORU 5.5: "Bu proje başarısız olursa ne öğrendin?"

**CEVAP:**
> "Başarılı olsa da olmasa da çok şey öğrendim:

**Teknik Öğrenmeler:**
- LLM entegrasyonu
- RAG sistemi kurulumu
- Flutter state management
- FastAPI streaming
- CI/CD pipeline

**Soft Skills:**
- Proje planlama
- Dokümantasyon yazma
- Problem çözme
- Zaman yönetimi

**Kariyer için:**
Bu teknolojiler (LLM, RAG) çok güncel.
İş başvurularında büyük avantaj olacak."

---

## 🎯 SORU SORULMADAN ÖNCE HAZIRLIK

### ✅ Sunum Öncesi Gece
- [ ] Tüm soruları 1 kez oku
- [ ] Zor soruları işaretle
- [ ] Cevapları kendi cümlelerinle özetle

### ✅ Sunum Günü Sabahı
- [ ] Zor soruları tekrar oku
- [ ] Arkadaşınla 5 soru prova yap
- [ ] Özgüven affirmation: "Tüm sorulara cevap verebilirim"

### ✅ Sunum Öncesi 30 dk
- [ ] Derin nefes
- [ ] Hızlı göz atma (başlıklar)
- [ ] "Bilmiyorsam dürüst olurum" hatırlatması

---

## 🚨 BİLMEDİĞİN SORUYA CEVAP

**ASLA uydurma!** Bunun yerine:

**Seçenek 1 - Dürüstlük:**
> "Bu soruyu tam bilmiyorum. Araştırıp size dönebilirim."

**Seçenek 2 - Yönlendirme:**
> "Bu konunun detayına bakmadım ama genel olarak şöyle çalışıyor..."

**Seçenek 3 - Koda Bakma:**
> "Koduma bakarak gösterebilir miyim?"

**EN KÖTÜ:** Yanlış bilgi vermek > Bilmemekten daha kötü.

---

**Bu doküman [Tarih] tarihinde hazırlanmıştır.**
**Başarılar! 🍀**
