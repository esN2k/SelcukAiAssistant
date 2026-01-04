# Demo Script (Selçuk AI Asistanı)

Süre hedefi: 5–7 dakika.

## Ön Koşullar
- Ollama çalışıyor ve model mevcut (ör. `llama3.2:3b`).
- Backend: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`.
- Flutter istemci veya web build çalışır durumda.
- RAG demo için `RAG_ENABLED=true` ve `data/rag` indexi hazır.

## Adım 1: Sağlık Kontrolü (30 sn)
Komut:
```bash
curl http://localhost:8000/health
```
Beklenen:
```json
{ "status": "ok", "message": "Selçuk AI Asistanı backend çalışıyor" }
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

## Adım 4: RAG Demo (2 dk)
Amaç: Kaynaklı yanıt ve citations göstermek.

Komut:
```bash
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"messages\":[{\"role\":\"user\",\"content\":\"RAG belgelerine göre proje mimarisi nasıl?\"}],\"rag_enabled\":true}"
```
Beklenen: Yanıtta mimari özeti + `citations` alanı.

UI Alternatifi:
- Settings → RAG Enabled = ON
- Aynı soruyu chat ekranında sorun
- Kaynaklar (Sources) kutusu görünsün

## Adım 5: Akışlı Yanıt (SSE) (1 dk)
UI üzerinden bir soru daha sorun ve token akışını gösterin.
Not: `NewChatScreen` içinde akışlı yanıt animasyonla görünür.

## Opsiyonel: Hata Senaryosu (1 dk)
- Ollama kapatılırsa `/chat` 503 döner.
- Türkçe hata mesajı gösterilir (frontend veya API).

## Yedek Plan
- Demo sırasında sorun yaşanırsa, aşağıdaki ekran görüntülerini gösterin:
  - /health yanıtı
  - /models yanıtı
  - Chat örneği (Konya vurgusu)
  - RAG citations ekranı
  - Diagnostics ekranı
