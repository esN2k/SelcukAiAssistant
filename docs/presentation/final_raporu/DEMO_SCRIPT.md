# Gösterim Betiği (Selçuk AI Asistanı)

Süre hedefi: 5–7 dakika.

## Ön Koşullar
- Ollama çalışıyor ve model mevcut (ör. `llama3.2:3b`).
- Arka Uç: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`.
- Flutter istemci veya web derleme çalışır durumda.
- RAG gösterimi için `RAG_ENABLED=true` ve `data/rag` indeksi hazır.

## Adım 1: Sağlık Kontrolü (30 sn)
Komut:
```bash
curl http://localhost:8000/health
```
Beklenen:
```json
{ "status": "ok", "message": "Selçuk AI Asistanı arka uç çalışıyor" }
```
Not: Gerekirse `/health/ollama` ve `/health/hf` de gösterilir.

## Adım 2: Model Listesi (30 sn)
Komut:
```bash
curl http://localhost:8000/models
```
Beklenen: Modeller listelenir, uygunluk ve nedenleri görünür.

## Adım 3: Basit Sohbet (1 dk)
Komut:
```bash
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"messages\":[{\"role\":\"user\",\"content\":\"Selçuk Üniversitesi nerede?\"}]}"
```
Beklenen (örnek): Konya vurgusu ve kampüs bilgisi.

## Adım 4: RAG Gösterimi (2 dk)
Amaç: Kaynaklı yanıt ve atıfları (`citations`) göstermek.

Komut:
```bash
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"messages\":[{\"role\":\"user\",\"content\":\"RAG belgelerine göre proje mimarisi nasıl?\"}],\"rag_enabled\":true}"
```
Beklenen: Yanıtta mimari özeti + `citations` alanı.

Arayüz Alternatifi:
- Ayarlar → RAG Etkin = Açık
- Aynı soruyu sohbet ekranında sorun
- Kaynaklar kutusu görünsün

## Adım 5: Akışlı Yanıt (SSE) (1 dk)
Arayüz üzerinden bir soru daha sorun ve belirteç akışını gösterin.
Not: `NewChatScreen` içinde akışlı yanıt animasyonla görünür.

## İsteğe Bağlı: Hata Senaryosu (1 dk)
- Ollama kapatılırsa `/chat` 503 döner.
- Türkçe hata mesajı gösterilir (ön uç veya API).

## Yedek Plan
- Gösterim sırasında sorun yaşanırsa, aşağıdaki ekran görüntülerini gösterin:
  - /health yanıtı
  - /models yanıtı
  - Sohbet örneği (Konya vurgusu)
  - RAG atıflar ekranı (`citations`)
  - Tanılama ekranı
