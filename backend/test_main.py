"""
Unit tests for the FastAPI backend.

These tests verify the API contract without requiring Ollama to be running.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import main
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "SelcukAiAssistant Backend is running"
    }


@patch('main.requests.post')
def test_chat_endpoint_success(mock_post):
    """Test successful chat request."""
    # Mock successful Ollama response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "response": "Merhaba! Ben Selçuk Üniversitesi AI asistanıyım."
    }
    mock_post.return_value = mock_response
    
    # Make request
    response = client.post(
        "/chat",
        json={"question": "Merhaba"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["answer"] == "Merhaba! Ben Selçuk Üniversitesi AI asistanıyım."


@patch('main.requests.post')
def test_chat_endpoint_connection_error(mock_post):
    """Test chat request when Ollama is not available."""
    # Mock connection error
    mock_post.side_effect = Exception("Connection refused")
    
    # Make request
    response = client.post(
        "/chat",
        json={"question": "Test"}
    )
    
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data


def test_chat_endpoint_invalid_request():
    """Test chat request with missing required field."""
    response = client.post(
        "/chat",
        json={}
    )
    
    assert response.status_code == 422  # Validation error


@patch('main.requests.post')
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


@patch('main.requests.post')
def test_prompt_contains_question(mock_post):
    """Test that the prompt sent to Ollama contains the user's question."""
    # Mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "Test response"}
    mock_post.return_value = mock_response
    
    # Make request
    question = "Selçuk Üniversitesi nerede?"
    response = client.post(
        "/chat",
        json={"question": question}
    )
    
    # Verify the mock was called
    assert mock_post.called
    call_args = mock_post.call_args
    
    # Check that the JSON payload contains our question
    json_payload = call_args[1]["json"]
    assert "prompt" in json_payload
    assert question in json_payload["prompt"]
    assert json_payload["model"] == "llama3.1"
    assert json_payload["stream"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
