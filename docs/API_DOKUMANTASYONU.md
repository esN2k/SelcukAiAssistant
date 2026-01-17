# API Dokümantasyonu

Bu doküman, Selçuk AI Asistanı backend uç noktalarını Türkçe olarak açıklar.

## Temel Bilgiler
- **Base URL:** `http://localhost:8000`
- **İçerik Tipi:** `application/json; charset=utf-8`

## Hata Formatı
Tüm hata yanıtları şu biçimdedir:
```json
{
  "hata": "Kullanıcıya gösterilecek Türkçe mesaj",
  "detay": "Opsiyonel açıklama",
  "kod": "opsiyonel_hata_kodu"
}
```

## GET /
**Amaç:** Basit sağlık mesajı

**Örnek Yanıt**
```json
{
  "status": "ok",
  "message": "Selçuk AI Asistanı arka uç çalışıyor"
}
```

## GET /health
**Amaç:** Genel sağlık kontrolü

## GET /health/ollama
**Amaç:** Ollama servis durumunu kontrol eder.

## GET /health/hf
**Amaç:** HuggingFace bağımlılık durumunu kontrol eder.

## GET /models
**Amaç:** Kullanılabilir modelleri listeler.

**Örnek Yanıt**
```json
{
  "models": [
    {
      "id": "selcuk_assistant_v1",
      "provider": "ollama",
      "model_id": "selcuk-assistant-v1",
      "display_name": "Selçuk Asistan v1 (Fine-tune)",
      "local_or_remote": "local",
      "requires_api_key": false,
      "context_length": 4096,
      "tags": ["turkish", "selcuk"],
      "notes": "Selçuk Üniversitesi verileriyle eğitilmiş model"
    }
  ]
}
```

## POST /chat
**Amaç:** Tek seferlik sohbet cevabı üretir.

**İstek Örneği**
```json
{
  "model": "selcuk_assistant_v1",
  "messages": [
    {"role": "user", "content": "Selçuk Üniversitesi nerede?"}
  ],
  "temperature": 0.2,
  "top_p": 0.9,
  "max_tokens": 256,
  "stream": false,
  "rag_enabled": true,
  "rag_strict": false,
  "rag_top_k": 4
}
```

**Yanıt Örneği**
```json
{
  "answer": "Selçuk Üniversitesi Konya'dadır.",
  "request_id": "abc123",
  "provider": "ollama",
  "model": "selcuk-assistant-v1",
  "usage": {
    "prompt_tokens": 120,
    "completion_tokens": 64,
    "total_tokens": 184
  },
  "citations": ["https://www.selcuk.edu.tr"]
}
```

## POST /chat/stream
**Amaç:** SSE ile akışlı yanıt üretir.

**Not:** Yanıt `text/event-stream` olarak gelir.

## POST /api/translate
**Amaç:** Metin çevirisi.

**İstek Örneği**
```json
{
  "text": "Merhaba",
  "source_lang": "tr",
  "target_lang": "en",
  "max_tokens": 128
}
```

**Yanıt Örneği**
```json
{
  "original_text": "Merhaba",
  "translated_text": "Hello",
  "source_lang": "tr",
  "target_lang": "en"
}
```

## POST /api/translate/image
**Amaç:** Görsel üzerinden çeviri yapar.

**Not:** `multipart/form-data` kullanılır.

## GET /api/translate/languages
**Amaç:** Desteklenen dilleri listeler.

## /admin Uç Noktaları
- `GET /admin/cache/stats`: Önbellek istatistikleri
- `GET /admin/analytics/popular`: Popüler sorular
- `GET /admin/analytics/hourly`: Saatlik istatistikler
- `GET /admin/analytics/models`: Model kullanım istatistikleri
