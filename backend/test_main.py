"""FastAPI backend için birim testleri.

Giriş: TestClient üzerinden istekler.
Çıkış: HTTP durum kodu ve gövde doğrulaması.
İşleyiş: Ollama çalışmadan API kontratını test eder.
"""
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from fastapi.testclient import TestClient

from config import Config
from main import app
from providers.base import ChatResult, Usage
from providers.ollama_provider import OllamaProvider

client = TestClient(app)


@patch("main.appwrite_client", None)
def test_root_endpoint():
    """Giriş: yok.

    Çıkış: Kök endpoint 200 ve doğru mesaj.
    İşleyiş: GET / çağrısını doğrular.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "Selçuk AI Asistanı arka uç çalışıyor",
    }


@pytest.mark.asyncio
@patch("main.appwrite_client", None)
@patch.object(OllamaProvider, "generate", new_callable=AsyncMock)
async def test_chat_endpoint_success(mock_generate):
    """Giriş: Geçerli chat isteği.

    Çıkış: 200 ve cevap metni.
    İşleyiş: Provider mock ile başarılı senaryo doğrulanır.
    """
    mock_generate.return_value = ChatResult(
        text="Merhaba! Ben Selçuk AI Asistanı.",
        usage=Usage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
    )

    response = client.post(
        "/chat",
        json={"messages": [{"role": "user", "content": "Merhaba"}]},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Merhaba! Ben Selçuk AI Asistanı."
    assert data["request_id"]


@patch("main.appwrite_client", None)
@patch.object(OllamaProvider, "generate", new_callable=AsyncMock)
def test_chat_endpoint_connection_error(mock_generate):
    """Giriş: Servis hatası.

    Çıkış: 503 ve detay.
    İşleyiş: HTTPException simülasyonu yapar.
    """
    from fastapi import HTTPException

    mock_generate.side_effect = HTTPException(status_code=503, detail="Unavailable")

    response = client.post(
        "/chat",
        json={"messages": [{"role": "user", "content": "Test"}]},
    )

    assert response.status_code == 503
    assert "detail" in response.json()


@patch("main.appwrite_client", None)
def test_chat_endpoint_invalid_request():
    """Giriş: Eksik payload.

    Çıkış: 422.
    İşleyiş: Doğrulama hatasını doğrular.
    """
    response = client.post("/chat", json={})
    assert response.status_code == 422


@patch("main.appwrite_client", None)
@patch.object(OllamaProvider, "generate", new_callable=AsyncMock)
def test_prompt_contains_question(mock_generate):
    """Giriş: Soru metni.

    Çıkış: Prompt içinde soru.
    İşleyiş: Çağrı argümanında soru metni aranır.
    """
    mock_generate.return_value = ChatResult(text="Test response")

    question = "Selçuk Üniversitesi nerede?"
    response = client.post(
        "/chat",
        json={"messages": [{"role": "user", "content": question}]},
    )

    assert response.status_code == 200
    messages = mock_generate.call_args.kwargs.get("messages", [])
    assert any(question in msg.get("content", "") for msg in messages)


@patch("main.appwrite_client", None)
@patch("httpx.AsyncClient.get")
def test_ollama_health_check_healthy(mock_get):
    """Giriş: Sağlıklı mock yanıt.

    Çıkış: healthy ve model var.
    İşleyiş: GET /health/ollama sonucunu doğrular.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "models": [{"name": Config.OLLAMA_MODEL}, {"name": "mistral"}]
    }
    mock_get.return_value = mock_response

    response = client.get("/health/ollama")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_available"] is True
    assert Config.OLLAMA_MODEL in data["available_models"]


@patch("main.appwrite_client", None)
@patch("httpx.AsyncClient.get")
def test_ollama_health_check_unhealthy(mock_get):
    """Giriş: Bağlantı hatası.

    Çıkış: 503.
    İşleyiş: RequestError simülasyonu yapar.
    """
    mock_get.side_effect = httpx.RequestError("Connection refused")

    response = client.get("/health/ollama")

    assert response.status_code == 503
    assert "detail" in response.json()


@patch("main.appwrite_client", None)
@patch.object(OllamaProvider, "generate", new_callable=AsyncMock)
def test_chat_endpoint_timeout(mock_generate):
    """Giriş: TimeoutError.

    Çıkış: 504.
    İşleyiş: Zaman aşımı senaryosunu doğrular.
    """
    mock_generate.side_effect = TimeoutError()

    response = client.post(
        "/chat",
        json={"messages": [{"role": "user", "content": "Test"}]},
    )

    assert response.status_code == 504
    data = response.json()
    assert "detail" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
