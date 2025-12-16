"""
Unit tests for the FastAPI backend.

These tests verify the API contract without requiring Ollama to be running.
"""
from unittest.mock import patch, MagicMock

import httpx
import pytest
from fastapi.testclient import TestClient

# Import from the same directory
from config import Config
from main import app

# We need to wrap the app with TestClient for synchronous testing of endpoints,
# but the underlying service calls will be mocked as async.
client = TestClient(app)


@patch('main.appwrite_client', None)
def test_root_endpoint():
    """Test the health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "SelcukAiAssistant Backend is running"
    }


@pytest.mark.asyncio
@patch('main.appwrite_client', None)
@patch('httpx.AsyncClient.post')
async def test_chat_endpoint_success(mock_post):
    """Test successful chat request."""
    # Mock successful Ollama response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "response": "Merhaba! Ben Selçuk Üniversitesi AI asistanıyım."
    }
    mock_post.return_value = mock_response

    # Make request using TestClient (which handles the async endpoint via standard requests)
    # Since we are mocking httpx.AsyncClient.post inside the endpoint,
    # the fact that TestClient is synchronous doesn't matter for the unit test of logic.
    response = client.post(
        "/chat",
        json={"question": "Merhaba"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["answer"] == "Merhaba! Ben Selçuk Üniversitesi AI asistanıyım."


@patch('main.appwrite_client', None)
@patch('httpx.AsyncClient.post')
def test_chat_endpoint_connection_error(mock_post):
    """Test chat request when Ollama is not available."""
    # Mock connection error
    mock_post.side_effect = httpx.RequestError("Connection refused")
    
    # Make request
    response = client.post(
        "/chat",
        json={"question": "Test"}
    )
    
    assert response.status_code == 503
    data = response.json()
    assert "detail" in data


@patch('main.appwrite_client', None)
def test_chat_endpoint_invalid_request():
    """Test chat request with missing required field."""
    response = client.post(
        "/chat",
        json={}
    )
    
    assert response.status_code == 422  # Validation error


@patch('main.appwrite_client', None)
@patch('httpx.AsyncClient.post')
def test_chat_endpoint_empty_response(mock_post):
    """Test chat request when Ollama returns empty response."""
    # Mock empty response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": ""}
    mock_post.return_value = mock_response
    
    # Make request
    response = client.post(
        "/chat",
        json={"question": "Test"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Üzgünüm, bir yanıt oluşturulamadı."


@patch('main.appwrite_client', None)
@patch('httpx.AsyncClient.post')
def test_prompt_contains_question(mock_post):
    """Test that the prompt sent to Ollama contains the user's question."""
    # Mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "Test response"}
    mock_post.return_value = mock_response
    
    # Make request
    question = "Selçuk Üniversitesi nerede?"
    client.post(
        "/chat",
        json={"question": question}
    )
    
    # Verify the mock was called
    assert mock_post.called
    call_args = mock_post.call_args
    
    # Check that the JSON payload contains our question
    # call_args for async call is (args, kwargs)
    # kwargs should have 'json'
    kwargs = call_args.kwargs
    json_payload = kwargs.get("json", {})
    
    assert "prompt" in json_payload
    assert question in json_payload["prompt"]
    assert json_payload["model"] == Config.OLLAMA_MODEL
    assert json_payload["stream"] is False


@patch('main.appwrite_client', None)
@patch('httpx.AsyncClient.get')
def test_ollama_health_check_healthy(mock_get):
    """Test Ollama health check when service is healthy."""
    # Mock successful response with available models
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "models": [
            {"name": Config.OLLAMA_MODEL},
            {"name": "mistral"}
        ]
    }
    mock_get.return_value = mock_response
    
    response = client.get("/health/ollama")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_available"] is True
    assert Config.OLLAMA_MODEL in data["available_models"]


@patch('main.appwrite_client', None)
@patch('httpx.AsyncClient.get')
def test_ollama_health_check_unhealthy(mock_get):
    """Test Ollama health check when service is unavailable."""
    # Mock connection error
    mock_get.side_effect = httpx.RequestError("Connection refused")
    
    response = client.get("/health/ollama")
    
    assert response.status_code == 503
    data = response.json()
    assert "detail" in data


@patch('main.appwrite_client', None)
@patch('httpx.AsyncClient.post')
def test_chat_endpoint_timeout(mock_post):
    """Test chat request timeout handling."""
    # Mock timeout error
    mock_post.side_effect = httpx.ReadTimeout("Request timed out")
    
    response = client.post(
        "/chat",
        json={"question": "Test"}
    )
    
    assert response.status_code == 504
    data = response.json()
    assert "detail" in data
    assert "zaman aşımı" in data["detail"].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
