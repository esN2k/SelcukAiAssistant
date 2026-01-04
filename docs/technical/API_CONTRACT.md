# API Kontratı

Bu doküman backend API sözleşmesini özetler.

## GET /health
- Cevap: `{ "status": "ok", "message": "..." }`

## GET /models
- Cevap: `{ "models": [ ... ] }`
- Model nesnesi alanları: `id`, `provider`, `model_id`, `display_name`,
  `local_or_remote`, `requires_api_key`, `available`, `reason_unavailable`,
  `tags`, `notes`.

## POST /chat
### İstek
```json
{
  "model": "ollama:llama3.1",
  "messages": [{ "role": "user", "content": "Merhaba" }],
  "temperature": 0.2,
  "top_p": 0.9,
  "max_tokens": 256,
  "rag_enabled": false,
  "rag_strict": true,
  "rag_top_k": 4
}
```

### Cevap
```json
{
  "answer": "...",
  "request_id": "...",
  "provider": "ollama",
  "model": "llama3.1",
  "usage": { "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0 },
  "citations": ["kaynak.pdf (sayfa 2)"]
}
```

## POST /chat/stream
- SSE ile parçalı yanıt döner.
- Etkinlik tipleri:
  - `token`: `{ "type": "token", "token": "...", "request_id": "..." }`
  - `end`: `{ "type": "end", "usage": { ... }, "citations": [ ... ], "request_id": "..." }`
  - `error`: `{ "type": "error", "message": "...", "request_id": "..." }`
