#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://localhost:8000}"
TIMEOUT_SEC="${TIMEOUT_SEC:-60}"
REPORT_PATH="${REPORT_PATH:-tools/.tmp/smoke_report_web.md}"

mkdir -p "$(dirname "$REPORT_PATH")"

results=()

write_result() {
  local name="$1"
  local ok="$2"
  local detail="$3"
  local status="PASS"
  if [[ "$ok" != "true" ]]; then
    status="FAIL"
  fi
  results+=("$name|$status|$detail")
  echo "$status: $name - $detail"
}

health="$(curl -sS --max-time "$TIMEOUT_SEC" "$BASE_URL/health" || true)"
if echo "$health" | grep -q '"status"[[:space:]]*:[[:space:]]*"ok"'; then
  write_result "GET /health" true "$health"
else
  write_result "GET /health" false "$health"
fi

ollama="$(curl -sS --max-time "$TIMEOUT_SEC" "$BASE_URL/health/ollama" || true)"
if echo "$ollama" | grep -q '"status"'; then
  write_result "GET /health/ollama" true "$ollama"
else
  write_result "GET /health/ollama" false "$ollama"
fi

hf="$(curl -sS --max-time "$TIMEOUT_SEC" "$BASE_URL/health/hf" || true)"
if echo "$hf" | grep -q '"status"'; then
  write_result "GET /health/hf" true "$hf"
else
  write_result "GET /health/hf" false "$hf"
fi

models="$(curl -sS --max-time "$TIMEOUT_SEC" "$BASE_URL/models" || true)"
if echo "$models" | grep -q '"models"'; then
  write_result "GET /models" true "$models"
else
  write_result "GET /models" false "$models"
fi

invalid_body='{"foo":"bar"}'
invalid_code="$(curl -sS --max-time "$TIMEOUT_SEC" -H "Content-Type: application/json" -o /tmp/invalid.json -w "%{http_code}" -X POST "$BASE_URL/chat" --data-binary "$invalid_body" || true)"
if [[ "$invalid_code" =~ ^[0-9]{3}$ ]] && [[ "$invalid_code" -ge 400 ]]; then
  write_result "POST /chat (invalid payload)" true "HTTP $invalid_code"
else
  write_result "POST /chat (invalid payload)" false "HTTP $invalid_code"
fi

payload='{"model":"","messages":[{"role":"user","content":"Merhaba"}],"stream":false,"max_tokens":64}'
chat="$(curl -sS --max-time "$TIMEOUT_SEC" -H "Content-Type: application/json" -X POST "$BASE_URL/chat" --data-binary "$payload" || true)"
if echo "$chat" | grep -q '"answer"'; then
  write_result "POST /chat" true "$chat"
else
  write_result "POST /chat" false "$chat"
fi

stream="$(curl -sS -N --max-time "$TIMEOUT_SEC" -H "Content-Type: application/json" -X POST "$BASE_URL/chat/stream" --data-binary "$payload" || true)"
if echo "$stream" | grep -Eq '"type"[[:space:]]*:[[:space:]]*"(token|end)"'; then
  write_result "POST /chat/stream" true "SSE received"
else
  write_result "POST /chat/stream" false "$stream"
fi

{
  echo "# Selcuk AI Assistant Smoke Report (Web)"
  echo ""
  echo "Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo "Base URL: $BASE_URL"
  echo ""
  echo "| Check | Status | Detail |"
  echo "| --- | --- | --- |"
  for item in "${results[@]}"; do
    IFS="|" read -r name status detail <<< "$item"
    detail="${detail//|//}"
    echo "| $name | $status | $detail |"
  done
} > "$REPORT_PATH"

echo "Report saved: $REPORT_PATH"
