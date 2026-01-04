# Selçuk AI Asistanı - Sunum İçeriği (Maks 25 Slayt)

Not: Detaylı konuşmacı notları `SPEAKER_NOTES.md` dosyasındadır.

## SLAYT 1: KAPAK
Proje Adı: Selçuk AI Akademik Asistan
Alt Başlık: Yapay Zeka Destekli Üniversite Bilgi Asistanı
Hazırlayanlar: esN2k
Danışman: Repo’da belirtilmemiş
Tarih: 04.01.2026
Kurum: Selçuk Üniversitesi
Görsel Önerisi: Üniversite mührü + proje logosu + kampüs fotoğrafı.
Konuşmacı Notu (özet): Proje adı, ders bağlamı ve gizlilik odaklı yaklaşım vurgulanır.

## SLAYT 2: İÇİNDEKİLER
1. Proje Özeti
2. Problem Tanımı
3. Amaç ve Hedefler
4. Literatür/Mevcut Çözümler
5. Metodoloji
6. Sistem Mimarisi
7. Kullanılan Teknolojiler
8. Uygulama Detayları
9. Ekran Görüntüleri/Gösterim
10. Test ve Değerlendirme
11. Sonuçlar
12. Gelecek Çalışmalar
13. Kaynaklar
Görsel Önerisi: Basit ikon seti (özet, mimari, teknoloji, test, sonuç).
Konuşmacı Notu (özet): Sunumun akışı ve süre dağılımı kısaca paylaşılır.

## SLAYT 3: PROJE ÖZETİ (Yönetici Özeti)
Selçuk AI Akademik Asistan, Selçuk Üniversitesi için gizliliğe odaklı, yerel LLM tabanlı bir bilgi asistanıdır.
Flutter istemci ve FastAPI arka uç ile çoklu platformda çalışır; /chat ve /chat/stream üzerinden yanıt üretir.
RAG (FAISS + SentenceTransformer) ile kaynaklı yanıtlar ve katı mod sunar.
Ollama ana sağlayıcıdır; HuggingFace opsiyonel olarak desteklenir.
Görsel Önerisi: Mimariyi özetleyen tek satırlık akış diyagramı.
Konuşmacı Notu (özet): Yerel çalışma, RAG ve çoklu sağlayıcı temaları öne çıkarılır.

## SLAYT 4: PROBLEM TANIMI
Mevcut Durum:
- Üniversite bilgileri dağınık; erişim ve doğrulama güçlüğü
- 7/24 destek ve hızlı yönlendirme eksikliği
- Tekrarlayan sorular için insan kaynağı yükü
- Bulut tabanlı çözümlerde gizlilik riski

Etkilenen Kitle:
- 100.000+ Selçuk Üniversitesi öğrencisi (bilgi tabanı verisi)
- Akademik ve idari personel
- Aday öğrenciler ve ziyaretçiler
Görsel Önerisi: “Sorun–Etkilenen Kitle” ikonlu infografik.
Konuşmacı Notu (özet): Gizlilik ve doğruluk ihtiyacı vurgulanır.

## SLAYT 5: AMAÇ VE HEDEFLER
Ana Amaç:
Selçuk Üniversitesi’ne özel, doğru ve kaynaklı bilgi veren yerel yapay zeka asistanı geliştirmek.

Hedefler:
- Yerel LLM ile gizlilik ve çevrimdışı çalışma
- RAG ile kaynaklı yanıt ve katı mod
- TR/EN dil desteği ve tutarlı sistem istemi
- Çoklu sağlayıcı/model seçimi (Ollama + opsiyonel HF)
- Kullanıcı dostu, çoklu platform arayüz ve SSE akışı
Görsel Önerisi: Hedefleri simgeleyen beş madde kartı.
Konuşmacı Notu (özet): Hedefler doğrudan repo dokümantasyonundan türetilmiştir.

## SLAYT 6: LİTERATÜR / MEVCUT ÇÖZÜMLER
Benzer Çözümler:
- Üniversite sohbet botları ve SSS portalları
- Bulut tabanlı LLM destekli yardım masaları
- RAG tabanlı bilgi asistanları (Lewis et al., 2020)

Bu Projenin Farkı:
- Selçuk Üniversitesi’ne özel doğrulanmış bilgi tabanı
- Yerel LLM (Ollama) ile gizlilik ve bağımsızlık
- RAG + atıflar (`citations`) + katı mod ile hatalı bilgi riski azaltma
- Sağlayıcı Deseni ile model esnekliği
Görsel Önerisi: Karşılaştırma tablosu (klasik sohbet botu ile RAG/yerel LLM karşılaştırması).
Konuşmacı Notu (özet): Farklılaştırıcılar net ve kısa şekilde aktarılır.

## SLAYT 7: METODOLOJİ
Geliştirme Adımları (repo akışı):
1. İhtiyaç ve gizlilik analizi
2. Veri toplama: resmi kaynaklar (tools/collect_sources.py)
3. Bilgi tabanı oluşturma: selcuk_knowledge_base.json
4. Soru-Cevap veri seti: selcuk_qa_dataset.jsonl + doğrulama (validate_knowledge.py)
5. RAG indeksleme: rag_ingest.py (FAISS)
6. Arka Uç API: FastAPI + Sağlayıcı Deseni
7. Ön Uç: Flutter + GetX + Hive
8. Test/Kıyaslama: pytest, ruff, mypy, benchmark/run.py
9. Dağıtım: Local, Docker, Docker Compose, Nginx
Görsel Önerisi: Süreç akışı (pipeline) diyagramı.
Konuşmacı Notu (özet): Her adımın repo dosyasına karşılığı vurgulanır.

## SLAYT 8: SİSTEM MİMARİSİ
```
Kullanıcı (Flutter/Web/Mobile)
        ↓ HTTP/SSE
FastAPI Arka Uç (/chat, /chat/stream, /models)
   ↙ Sağlayıcı Deseni ↘
Ollama (LLM)      HuggingFace (ops.)
        ↓
RAG (FAISS indeks + metadata)
        ↓
Kaynaklı Yanıt + Citations
```
Görsel Önerisi: Katmanlı mimari diyagramı.
Konuşmacı Notu (özet): SSE akışı ve RAG katı mod akışı anlatılır.

## SLAYT 9: KULLANILAN TEKNOLOJİLER
Arka Uç:
- Python, FastAPI, Pydantic, Uvicorn
- requests/httpx, python-dotenv

Yapay Zeka / Makine Öğrenmesi:
- Ollama (yerel LLM, varsayılan model seçilebilir)
- HuggingFace Transformers (opsiyonel)
- RAG: FAISS + SentenceTransformer gömme vektörleri

Ön Uç:
- Flutter (Material 3) + GetX
- Hive (local storage), flutter_secure_storage
- SSE istemcisi, markdown desteği

Veri/Depolama:
- JSON/JSONL bilgi tabanı
- FAISS indeks + metadata.json
- Opsiyonel: Appwrite (auth/log)

Dağıtım:
- Local run, Docker, Docker Compose, Nginx
Görsel Önerisi: Teknoloji logoları ile katmanlı kolaj.
Konuşmacı Notu (özet): Stack, requirements ve pubspec üzerinden doğrulanmıştır.

## SLAYT 10: VERİ TABANI YAPISI
Knowledge Base İçeriği:
- Üniversite genel bilgileri (Konya, 1975, kampüsler)
- Fakülte/bölüm bilgileri
- Akademik takvim özetleri
- İletişim bilgileri ve SSS

Veri Formatı:
- `backend/data/selcuk_knowledge_base.json`
- `backend/data/selcuk_qa_dataset.jsonl`
- RAG: `backend/data/rag/index.faiss` + `metadata.json`

Uygulama Verisi:
- Flutter: Hive ile konuşma geçmişi
- Opsiyonel: Appwrite ile oturum ve sohbet logları
Görsel Önerisi: Dosya ağacı görseli (data/ dizini).
Konuşmacı Notu (özet): Dosya isimleri doğrudan repo veri dizinlerinden alınmıştır.

## SLAYT 11: UYGULAMA DETAYLARI - Arka Uç
API Uç Noktaları:
- GET /health, /health/ollama, /health/hf
- GET /models
- POST /chat
- POST /chat/stream (SSE)

Core Functions:
- Model yönlendirme: `providers/registry.py`
- RAG bağlamı: `rag_service.py`
- İstem ve katı mod: `prompts.py`
- Akış yanıtı temizleme
- Opsiyonel Appwrite loglama
Görsel Önerisi: API uç nokta listesi + küçük akış şeması.
Konuşmacı Notu (özet): Uç noktaların amacı ve SSE farkı belirtilir.

## SLAYT 12: UYGULAMA DETAYLARI - YAPAY ZEKA ENTEGRASYONU
LLM Konfigürasyonu (istemci varsayılanı):
- temperature: 0.2, top_p: 0.9, max_tokens: 256
- Model sağlayıcı: Ollama (varsayılan), HF opsiyonel

Sistem İstemi (prompts.py):
“Selçuk Üniversitesi’nin resmi yapay zeka asistanısın… Konya (İzmir değil), 1975…”

RAG Akışı:
1. Soru alınır
2. Gömme vektörüne çevrilir (SentenceTransformer)
3. FAISS top_k (varsayılan 4) araması
4. Kaynaklar isteme eklenir (katı mod destekli)
5. Yanıt + citations üretilir
Görsel Önerisi: RAG akış diyagramı.
Konuşmacı Notu (özet): Konya vurgusu ve katı mod mesajı özellikle belirtilir.

## SLAYT 13: UYGULAMA DETAYLARI - Ön Uç
Arayüz Özellikleri:
- ChatGPT benzeri sohbet arayüzü
- SSE akışı ve Markdown destekli mesajlar
- Sesli giriş (speech_to_text)
- Model seçici ve tanılama ekranı
- RAG ve katı mod ayarları
- Sohbet geçmişi, düzenleme, yeniden üretme, dışa aktarma

Kullanıcı Deneyimi:
- TR/EN dil desteği
- Açık/Koyu tema
- Mobil, web ve desktop uyumluluğu
Görsel Önerisi: Chat ekranı + ayarlar ekranı yan yana.
Konuşmacı Notu (özet): Temel arayüz özellikleri docs/guides/FEATURES.md ve Flutter kodu ile uyumlu.

## SLAYT 14: EKRAN GÖRÜNTÜLERİ - ANA SAYFA
Önerilen Görseller:
- Yeni sohbet ekranı (NewChatScreen)
- Sol menü: konuşma listesi
- Üst bar: tema ve menü aksiyonları
- Alt bar: mikrofon + mesaj kutusu + gönder/durdur
Görsel Önerisi: Gerçek uygulamadan ekran görüntüsü.
Konuşmacı Notu (özet): Kullanıcı akışı ilk bakışta anlaşılır şekilde gösterilir.

## SLAYT 15: EKRAN GÖRÜNTÜLERİ - SOHBET ÖRNEĞİ
Örnek Sohbet (bilgi tabanı verisi):
Kullanıcı: “Selçuk Üniversitesi nerede?”
Asistan: “Selçuk Üniversitesi Konya ilinde, Selçuklu ilçesinde yer almaktadır. Ana kampüsü Alaeddin Keykubat Kampüsü’dür.”
Görsel Önerisi: Sohbet balonları + kaynaklar (citations) alanı.
Konuşmacı Notu (özet): Doğru şehir vurgusu (Konya, İzmir değil) öne çıkarılır.

## SLAYT 16: EKRAN GÖRÜNTÜLERİ - FARKLI SORU TİPLERİ
Desteklenen Soru Kategorileri (bilgi tabanı örnekleri):
- Konum ve kampüs bilgileri
- Fakülte/bölüm bilgileri
- Akademik takvim özetleri
- İletişim ve öğrenci işleri
- Rektörlük ve yönetim bilgileri
Görsel Önerisi: 3-4 farklı soru örneği grid görünümü.
Konuşmacı Notu (özet): Soru çeşitliliği bilgi tabanı ile örtüşür.

## SLAYT 17: TEST SENARYOLARI
Test Senaryoları (tanımlı betik/rapor):
| Soru | Beklenen | Sonuç |
| --- | --- | --- |
| “Selçuk Üniversitesi nerede?” | Konya | Doğrulama kuralı mevcut (validate_knowledge.py) |
| “Ne zaman kuruldu?” | 1975 | Doğrulama kuralı mevcut (validate_knowledge.py) |
| “Bilg. Müh. hangi fakültede?” | Teknoloji Fakültesi | Doğrulama kuralı mevcut (validate_knowledge.py) |
| “Bilg. Müh. akredite mi?” | MÜDEK var | Doğrulama kuralı mevcut (validate_knowledge.py) |
| “Kaç fakülte var?” | 23 | bilgi tabanı verisi (selcuk_knowledge_base.json) |
Görsel Önerisi: Test tablosu + kısa log alıntısı.
Konuşmacı Notu (özet): Test raporu ve doğrulama betikleri referans gösterilir.

## SLAYT 18: PERFORMANS METRİKLERİ
Kıyaslama Özeti (docs/reports/BENCHMARK_RAPORU.md):
- llama3.2:3b (12 örnek): Avg TTFT 5180 ms, 5.41 tok/s, Avg total 8.643 s
- turkcell-llm-7b (6 örnek): Avg TTFT 10126 ms, 4.10 tok/s
- selcuk_ai_assistant (6 örnek): Avg TTFT 10186 ms, 3.49 tok/s
- SSE akışı ile algılanan gecikme düşürülür
Görsel Önerisi: Bar chart (TTFT ve tok/s).
Konuşmacı Notu (özet): Performans verileri kıyaslama raporundan alınmıştır.

## SLAYT 19: KARŞILAŞILAN ZORLUKLAR
Zorluklar:
- Hallucination riski ve yanlış bilgi üretimi
- Türkçe dil yapısı ve resmi üslup ihtiyacı
- Yerel LLM performans/latency yönetimi
- Bilgi tabanının güncel tutulması
Görsel Önerisi: “Risk–Çözüm” eşleştirme görseli.
Konuşmacı Notu (özet): Her zorluğun repo’daki karşılığı belirtilir.

## SLAYT 20: ÇÖZÜMLER VE İYİLEŞTİRMELER
Uygulanan Çözümler:
- RAG + katı mod: kaynak yoksa “Bu bilgi kaynaklarda yok.”
- Doğrulama betiği: validate_knowledge.py
- SSE akışı ile kullanıcı deneyimi
- Sağlayıcı Deseni ile model esnekliği
- Türkçe hata mesajları ve input doğrulama
Görsel Önerisi: Çözüm ikonları ve kısa örnek yanıt.
Konuşmacı Notu (özet): Çözümler doğrudan kod ve dokümantasyona dayanır.

## SLAYT 21: SONUÇLAR
Başarılar:
- Çalışan yerel LLM + RAG prototipi
- Kaynaklı ve doğrulanabilir yanıtlar
- Çoklu platform Flutter arayüzü
- CI/test kalite kapıları (pytest, ruff, mypy, flutter)
Görsel Önerisi: Başarı checklist’i.
Konuşmacı Notu (özet): Test/CI vurgusu akademik güvenilirliği artırır.

## SLAYT 22: SWOT ANALİZİ
Güçlü Yönler:
- Gizlilik odaklı yerel LLM
- RAG ile kaynaklı yanıtlar
- Çoklu sağlayıcı/modele açık mimari

Zayıf Yönler:
- Yerel donanım gereksinimi
- Veri güncelleme süreçlerinin maliyeti

Fırsatlar:
- Resmi üniversite entegrasyonları
- LoRA ile alan özelleştirme

Tehditler:
- Model sürüm değişimleri
- Güncel veri ihtiyacı
Görsel Önerisi: 2x2 SWOT matrisi.
Konuşmacı Notu (özet): Güçlü/zayıf taraflar repo gerçeklerine dayanır.

## SLAYT 23: GELECEK ÇALIŞMALAR
Kısa Vadeli:
- RAG kaynaklarının genişletilmesi
- Bilgi tabanı doğrulama ve güncelleme otomasyonu

Orta Vadeli:
- LoRA/QLoRA ince ayar (docs/reports/FINE_TUNING_REPORT.md)
- Appwrite entegrasyonunun genişletilmesi

Uzun Vadeli:
- Resmi üniversite sistemleriyle entegrasyon
- Çoklu dil ve kişiselleştirme
Görsel Önerisi: Yol haritası (P1–P2–P3).
Konuşmacı Notu (özet): Yol haritası ve LoRA planı referans gösterilir.

## SLAYT 24: CANLI GÖSTERİM
Canlı Gösterim:
- Yerel ortam (arka uç: http://localhost:8000, Flutter uygulaması)

Test Edilecek Sorular:
1. “Selçuk Üniversitesi nerede?”
2. “Kampüsler hangileri?”
3. “Kaç fakülte var?”
4. “Rektör kim?”
5. “Bilgisayar Mühendisliği hangi fakültede?”
Görsel Önerisi: Gösterim akış adımları + ekran görüntüsü.
Konuşmacı Notu (özet): Gösterim betiği adımları DEMO_SCRIPT.md’de detaylıdır.

## SLAYT 25: TEŞEKKÜRLER
Teşekkürler!

Sorularınız?

İletişim:
- GitHub: github.com/esN2k/SelcukAiAssistant
- E-posta: Repo’da belirtilmemiş

Selçuk Üniversitesi
04.01.2026
Görsel Önerisi: Teşekkür/kurum logosu.
Konuşmacı Notu (özet): Soru-cevap için davet ve iletişim bilgisi.

## SLAYT 26+: KAYNAKLAR (Slayt sınırı dışında)
[1] Selçuk AI Asistanı README ve dokümantasyonları (README.md, docs/*.md)
[2] Selçuk Üniversitesi Resmi Web Sitesi - https://www.selcuk.edu.tr
[3] FastAPI Documentation - https://fastapi.tiangolo.com
[4] Flutter Documentation - https://docs.flutter.dev
[5] Ollama Documentation - https://ollama.com/docs
[6] FAISS Documentation - https://github.com/facebookresearch/faiss
[7] Sentence-Transformers - https://www.sbert.net
[8] RAG: Lewis et al., 2020, Retrieval-Augmented Generation
