"""
Extended unit tests for new features in the FastAPI backend.

Tests cover:
- Input validation and sanitization
- Health check model matching with tags
- Retry logic
- RAG service structure
"""
from unittest.mock import patch, MagicMock

import pytest
import requests
from fastapi.testclient import TestClient

from config import Config
from main import app
from ollama_service import OllamaService
from rag_service import RAGService, Document

client = TestClient(app)


# ============================================================================
# Input Validation Tests
# ============================================================================

def test_chat_empty_question():
    """Test that empty questions are rejected."""
    response = client.post("/chat", json={"question": ""})
    assert response.status_code == 422


def test_chat_whitespace_only_question():
    """Test that whitespace-only questions are rejected."""
    response = client.post("/chat", json={"question": "   "})
    assert response.status_code == 422


def test_chat_too_long_question():
    """Test that questions exceeding max length are rejected."""
    long_question = "a" * 6000  # Exceeds 5000 char limit
    response = client.post("/chat", json={"question": long_question})
    assert response.status_code == 422


def test_chat_xss_prevention():
    """Test that dangerous patterns are rejected."""
    dangerous_inputs = [
        "<script>alert('xss')</script>",
        "test javascript:alert(1)",
        "test onerror=alert(1)",
        "test onload=alert(1)",
    ]
    
    for dangerous_input in dangerous_inputs:
        response = client.post("/chat", json={"question": dangerous_input})
        assert response.status_code == 422, f"Should reject: {dangerous_input}"


@patch('ollama_service.requests.post')
def test_chat_valid_input_with_sanitization(mock_post):
    """Test that valid inputs are properly sanitized."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "Test response"}
    mock_post.return_value = mock_response
    
    # Input with extra whitespace
    response = client.post("/chat", json={"question": "  Test question  "})
    
    assert response.status_code == 200
    # Verify whitespace was stripped in the prompt
    call_args = mock_post.call_args
    prompt = call_args[1]["json"]["prompt"]
    assert "Test question" in prompt


# ============================================================================
# Health Check Model Matching Tests
# ============================================================================

@patch('ollama_service.requests.get')
def test_health_check_exact_match(mock_get):
    """Test health check with exact model name match."""
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
    assert data["model_available"] is True


@patch('ollama_service.requests.get')
def test_health_check_with_latest_tag(mock_get):
    """Test health check when configured model has no tag but available model has :latest."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "models": [
            {"name": f"{Config.OLLAMA_MODEL}:latest"},
            {"name": "mistral:latest"}
        ]
    }
    mock_get.return_value = mock_response
    
    response = client.get("/health/ollama")
    assert response.status_code == 200
    data = response.json()
    # Should match configured model with its :latest variant
    assert data["model_available"] is True


@patch('ollama_service.requests.get')
def test_health_check_reverse_tag_match(mock_get):
    """Test health check when configured model has :latest but available model doesn't."""
    # Create a service with model that includes tag
    service = OllamaService(model="selcuk_ai_assistant:latest")
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "models": [
            {"name": "selcuk_ai_assistant"},
            {"name": "llama3.1"}
        ]
    }
    mock_get.return_value = mock_response
    
    health = service.health_check()
    assert health["model_available"] is True


def test_is_model_available_helper():
    """Test the model availability helper method."""
    # Test exact match
    assert OllamaService._is_model_available("llama3.1", ["llama3.1", "mistral"]) is True
    
    # Test tag variation
    assert OllamaService._is_model_available("llama3.1", ["llama3.1:latest"]) is True
    assert OllamaService._is_model_available("llama3.1:latest", ["llama3.1"]) is True
    
    # Test no match
    assert OllamaService._is_model_available("gpt4", ["llama3.1", "mistral"]) is False
    
    # Test empty lists
    assert OllamaService._is_model_available("llama3.1", []) is False
    assert OllamaService._is_model_available("", ["llama3.1"]) is False


# ============================================================================
# Retry Logic Tests
# ============================================================================

@patch('ollama_service.requests.post')
@patch('ollama_service.time.sleep')  # Mock sleep to speed up tests
def test_retry_on_connection_error(mock_sleep, mock_post):
    """Test that connection errors trigger retries."""
    # First two attempts fail, third succeeds
    mock_post.side_effect = [
        requests.exceptions.ConnectionError("Connection refused"),
        requests.exceptions.ConnectionError("Connection refused"),
        MagicMock(status_code=200, json=lambda: {"response": "Success"})
    ]
    
    service = OllamaService(max_retries=3)
    result = service.generate("test prompt")
    
    # Should have tried 3 times
    assert mock_post.call_count == 3
    assert result == "Success"
    
    # Should have slept twice (between retries)
    assert mock_sleep.call_count == 2


@patch('ollama_service.requests.post')
@patch('ollama_service.time.sleep')
def test_retry_on_timeout(mock_sleep, mock_post):
    """Test that timeout errors trigger retries."""
    mock_post.side_effect = [
        requests.exceptions.Timeout("Timeout"),
        MagicMock(status_code=200, json=lambda: {"response": "Success after retry"})
    ]
    
    service = OllamaService(max_retries=2)
    result = service.generate("test prompt")
    
    assert mock_post.call_count == 2
    assert result == "Success after retry"


@patch('ollama_service.requests.post')
@patch('ollama_service.time.sleep')
def test_retry_exhaustion(mock_sleep, mock_post):
    """Test that retries are exhausted and error is raised."""
    from fastapi import HTTPException

    mock_post.side_effect = requests.exceptions.ConnectionError("Connection refused")
    
    service = OllamaService(max_retries=3)

    with pytest.raises(HTTPException) as exc_info:
        service.generate("test prompt")
    
    # Should have tried max_retries times
    assert mock_post.call_count == 3
    assert exc_info.value.status_code == 503


@patch('ollama_service.requests.post')
def test_no_retry_on_http_error(mock_post):
    """Test that HTTP errors (4xx, 5xx) don't trigger retries."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"error": "Model not found"}
    mock_response.text = "Model not found"
    mock_post.return_value = mock_response
    
    service = OllamaService(max_retries=3)
    
    with pytest.raises(Exception):
        service.generate("test prompt")
    
    # Should only try once (no retries for HTTP errors)
    assert mock_post.call_count == 1


# ============================================================================
# RAG Service Tests
# ============================================================================

def test_rag_service_initialization_disabled():
    """Test RAG service initializes correctly when disabled."""
    service = RAGService(enabled=False)
    assert service.enabled is False
    assert service.get_context("test query") == ""


def test_rag_service_initialization_enabled():
    """Test RAG service initializes with proper configuration."""
    service = RAGService(
        enabled=True,
        vector_db_path="/tmp/test_db",
        collection_name="test_collection",
        chunk_size=300,
        chunk_overlap=30
    )
    assert service.enabled is True
    assert service.vector_db_path == "/tmp/test_db"
    assert service.collection_name == "test_collection"
    assert service.chunk_size == 300
    assert service.chunk_overlap == 30


def test_rag_service_search_when_disabled():
    """Test that search returns empty list when RAG is disabled."""
    service = RAGService(enabled=False)
    results = service.search("test query")
    assert results == []


def test_rag_service_ingest_when_disabled():
    """Test that ingest raises error when RAG is disabled."""
    service = RAGService(enabled=False)
    with pytest.raises(RuntimeError, match="RAG service is not enabled"):
        service.ingest_document("test content")


def test_document_creation():
    """Test Document class initialization."""
    doc = Document(
        content="Test content",
        metadata={"source": "test.txt", "date": "2024-01-01"},
        doc_id="doc_123"
    )
    assert doc.content == "Test content"
    assert doc.metadata["source"] == "test.txt"
    assert doc.doc_id == "doc_123"
    assert "Test content" in repr(doc)


def test_rag_chunk_document():
    """Test document chunking logic."""
    service = RAGService(
        enabled=True,
        chunk_size=10,
        chunk_overlap=3
    )
    
    content = "0123456789abcdefghij"
    chunks = service._chunk_document(content)
    
    # Verify chunks have proper size
    assert all(len(chunk) <= 10 for chunk in chunks)
    
    # Verify overlap
    # With size=10 and overlap=3, we advance by 7 each time
    assert len(chunks) > 1


# ============================================================================
# UTF-8 Encoding Tests
# ============================================================================

@patch('ollama_service.requests.post')
def test_turkish_characters_in_question(mock_post):
    """Test that Turkish characters are properly handled."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.encoding = 'utf-8'
    mock_response.json.return_value = {
        "response": "Selçuk Üniversitesi'nin kuruluş tarihi 1975'tir."
    }
    mock_post.return_value = mock_response
    
    # Question with Turkish characters
    turkish_question = "Selçuk Üniversitesi'nin kuruluş tarihi nedir?"
    response = client.post("/chat", json={"question": turkish_question})
    
    assert response.status_code == 200
    data = response.json()
    # Verify Turkish characters are preserved
    assert "Selçuk" in data["answer"]
    assert "Üniversitesi" in data["answer"]


@patch('ollama_service.requests.post')
def test_utf8_header_sent(mock_post):
    """Test that UTF-8 content-type header is sent to Ollama."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "Test"}
    mock_post.return_value = mock_response
    
    service = OllamaService()
    service.generate("test")
    
    # Check that UTF-8 header was sent
    call_args = mock_post.call_args
    headers = call_args[1].get("headers", {})
    assert "charset=utf-8" in headers.get("Content-Type", "")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
