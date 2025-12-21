"""
Unit tests for the FastAPI backend.

These tests verify the API contract without requiring Ollama to be running.
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
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "SelcukAiAssistant Backend is running",
    }


@pytest.mark.asyncio
@patch("main.appwrite_client", None)
@patch.object(OllamaProvider, "generate", new_callable=AsyncMock)
async def test_chat_endpoint_success(mock_generate):
    mock_generate.return_value = ChatResult(
        text="Merhaba! Ben Selcuk University AI assistant.",
        usage=Usage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
    )

    response = client.post(
        "/chat",
        json={"messages": [{"role": "user", "content": "Merhaba"}]},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Merhaba! Ben Selcuk University AI assistant."
    assert data["request_id"]


@patch("main.appwrite_client", None)
@patch.object(OllamaProvider, "generate", new_callable=AsyncMock)
def test_chat_endpoint_connection_error(mock_generate):
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
    response = client.post("/chat", json={})
    assert response.status_code == 422


@patch("main.appwrite_client", None)
@patch.object(OllamaProvider, "generate", new_callable=AsyncMock)
def test_prompt_contains_question(mock_generate):
    mock_generate.return_value = ChatResult(text="Test response")

    question = "Selcuk University nerede?"
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
    mock_get.side_effect = httpx.RequestError("Connection refused")

    response = client.get("/health/ollama")

    assert response.status_code == 503
    assert "detail" in response.json()


@patch("main.appwrite_client", None)
@patch.object(OllamaProvider, "generate", new_callable=AsyncMock)
def test_chat_endpoint_timeout(mock_generate):
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
