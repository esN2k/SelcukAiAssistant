# API Contract

This document defines the canonical request/response schema for `/chat` and `/chat/stream`.

## Request Schema

```json
{
  "model": "alias_or_provider:model_id",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Merhaba! Selcuk University yemekhane saatleri nedir?"}
  ],
  "temperature": 0.2,
  "top_p": 0.9,
  "max_tokens": 256,
  "stream": true
}
```

Rules:
- `messages[]` is required and must contain at least one user message.
- `role` must be one of: `system`, `user`, `assistant`.
- `model` is optional. If omitted, the backend uses its default provider/model.

## Non-Streaming Response (`POST /chat`)

```json
{
  "answer": "Merhaba! ...",
  "request_id": "abcd1234",
  "provider": "ollama",
  "model": "selcuk_ai_assistant",
  "usage": {
    "prompt_tokens": 120,
    "completion_tokens": 48,
    "total_tokens": 168
  }
}
```

## Streaming Response (`POST /chat/stream`)

The endpoint returns Server-Sent Events (SSE). Each event is a `data:` line with JSON.

Token event:
```
data: {"type":"token","token":"Merhaba","request_id":"abcd1234"}
```

End event:
```
data: {"type":"end","usage":{"prompt_tokens":120,"completion_tokens":48,"total_tokens":168},"request_id":"abcd1234"}
```

Error event:
```
data: {"type":"error","message":"Request timeout","request_id":"abcd1234"}
```

## Models

`GET /models` returns the available model aliases for this deployment:

```json
{
  "models": [
    {
      "id": "default",
      "provider": "ollama",
      "model_id": "selcuk_ai_assistant",
      "display_name": "Default",
      "is_default": true
    }
  ]
}
```
