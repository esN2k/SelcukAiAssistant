# Sunum Notları (Jüri Odaklı)

## Proje Özeti
Bu çalışmada, Selçuk Üniversitesi akademik ihtiyaçları için gizliliğe odaklı bir yapay zeka akademik asistan geliştirilmiştir. Sistem, bulut servis bağımlılığını kaldıracak biçimde yerel LLM (yerel çıkarım / local inference) temelli kurgulanmış; RAG (Retrieval-Augmented Generation / Kaynak Destekli Üretim) yaklaşımıyla kaynaklı yanıt üretimi sağlanarak akademik doğrulanabilirlik güçlendirilmiştir.

## Problem ve Çözüm
Eğitim ortamında verinin gizliliğinin korunmasının zorunlu olduğu; bulut tabanlı API kullanımının hassas verileri dış ortamlara taşıma riski oluşturduğu değerlendirilmiştir. Bu risk, yerel LLM'e geçiş ve RAG mimarisi ile azaltılmıştır. Böylece akademik içeriklerin kurum içinde işlenmesi sağlanmış ve kaynaklı yanıtlar ile güvenilirlik artırılmıştır.

## Mimari ve Sağlayıcı Deseni (Provider Pattern)
Backend katmanında `backend/providers/` altında Sağlayıcı Deseni (Provider Pattern) uygulanmıştır. Bu yaklaşım ile Ollama ve HuggingFace (HF) aynı arayüz üzerinden yönlendirilmekte, sağlayıcı değişimi yapılandırma ile gerçekleştirilmektedir.

ASCII akış çizimi:
Flutter -> FastAPI Router -> Provider Factory -> (Ollama | HF) -> VektörDB
                                   |-> RAG (FAISS/ChromaDB)

## Teknik Detaylar
- `rag_service.py` içinde belgeler parçalara ayrılmakta, embedding (gömme) üretimi yapılmakta ve FAISS üzerinden en yakın parçalar sorgulanmaktadır.
- Bulunan parçalar sistem promptuna eklenmekte, yanıt üretildikten sonra `citations` alanı ile kaynak listesi istemciye dönülmektedir.
- Bellek ve hız dengesi için embedding batch boyutu ve `top_k` parametresi yapılandırılabilir tutulmuştur.
- Akışlı yanıt (SSE) ile gecikme algısı azaltılmakta, istemci deneyimi stabil tutulmaktadır.

## Güvenlik ve Gizlilik
- Yerel LLM kullanımı ile veri kurum dışına çıkmadan işlenmektedir.
- Ortam değişkenleri (.env) ile anahtarlar ve kritik ayarlar ayrıştırılmıştır.
- Hata mesajları Türkçe ve açıklayıcı olacak biçimde tasarlanmıştır.

## Sunum Akışı (7-10 Dakika)
- 0:00-1:00 Proje özeti ve motivasyon.
- 1:00-2:00 Problem tanımı ve gizlilik ihtiyacı.
- 2:00-3:30 Mimari akış ve sağlayıcı deseni.
- 3:30-5:00 RAG işleyişi ve kaynaklı yanıtlar.
- 5:00-6:30 Teknoloji yığını ve yerel LLM gerekçesi.
- 6:30-8:00 Test/CI sonuçları ve kalite kapıları.
- 8:00-9:30 Sınırlılıklar ve gelecek çalışmalar.
- 9:30-10:00 Kısa özet ve kapanış.

## Olası Jüri Soruları ve Akademik Yanıtlar
- Soru: Neden ChromaDB yerine FAISS kullanılmıştır? Yanıt: Hızlı benzerlik araması ihtiyacı nedeniyle FAISS tercih edilmiş, ChromaDB kalıcı saklama (persistence) senaryoları için opsiyonel katman olarak değerlendirilmiştir.
- Soru: Gecikmeler (latency) nasıl yönetilmektedir? Yanıt: Akışlı yanıt (SSE) ve zaman aşımı sınırlarıyla deneyim stabil tutulmakta; embedding batch boyutları performans için ayarlanabilir kılınmaktadır.
- Soru: Ollama servisi çökerse ne olur? Yanıt: Sağlık kontrolleri ve Türkçe hata mesajlarıyla durum raporlanmakta; sağlayıcı değişimi yapılandırma ile yapılabilmektedir.
- Soru: HF modelleri neden opsiyonel olarak sunulmaktadır? Yanıt: HF modelleri ek bağımlılık ve disk alanı gerektirdiğinden opsiyonel tutulmuş, uygunluk durumu `/models` üzerinden raporlanmıştır.
- Soru: Kaynak gösterimi güvenilir midir? Yanıt: RAG hattında getirilen parçalar kaynak etiketiyle dönülmekte, yanıtların doğrulanabilirliği artırılmaktadır.
