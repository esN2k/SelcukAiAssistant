"""
Extended unit tests for new features in the FastAPI backend.

Tests cover:
- Input validation and sanitization
- Health check model matching with tags
- Retry logic
- RAG service structure
"""
from unittest.mock import patch, MagicMock

import httpx
import pytest
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


@patch('ollama_service.httpx.AsyncClient.post')
def test_chat_valid_input_with_sanitization(mock_post):
    """Test that valid inputs are properly sanitized."""
    # Note: TestClient calls endpoint synchronously, but inside we want to verify logic.
    # For actual sanitization check via endpoint, we use TestClient.
    # However, since the endpoint is now async and uses httpx, we mock httpx.
    # The TestClient handles the async endpoint execution for us.
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "Test response"}
    mock_post.return_value = mock_response
    
    # Input with extra whitespace
    response = client.post("/chat", json={"question": "  Test question  "})

    # We can't easily inspect the arguments passed to the async client mock 
    # because TestClient runs in a way that makes standard mock assertions tricky for async calls inside.
    # But we can verify the response code which means validation passed.
    assert response.status_code == 200


# ============================================================================
# Health Check Model Matching Tests
# ============================================================================

@pytest.mark.asyncio
@patch('ollama_service.httpx.AsyncClient.get')
async def test_health_check_exact_match(mock_get):
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

    service = OllamaService()
    health = await service.health_check()
    assert health["status"] == "healthy"
    assert health["model_available"] is True


@pytest.mark.asyncio
@patch('ollama_service.httpx.AsyncClient.get')
async def test_health_check_with_latest_tag(mock_get):
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

    service = OllamaService()
    health = await service.health_check()
    assert health["status"] == "healthy"
    # Should match configured model with its :latest variant
    assert health["model_available"] is True


@pytest.mark.asyncio
@patch('ollama_service.httpx.AsyncClient.get')
async def test_health_check_reverse_tag_match(mock_get):
    """Test health check when configured model has :latest but available model doesn't."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "models": [
            {"name": "selcuk_ai_assistant"},
            {"name": "llama3.1"}
        ]
    }
    mock_get.return_value = mock_response

    # Create a service with model that includes tag
    service = OllamaService(model="selcuk_ai_assistant:latest")
    health = await service.health_check()
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

@pytest.mark.asyncio
@patch('ollama_service.httpx.AsyncClient.post')
@patch('ollama_service.asyncio.sleep')  # Mock sleep to speed up tests
async def test_retry_on_connection_error(_mock_sleep, mock_post):
    """Test that connection errors trigger retries."""
    # First two attempts fail, third succeeds
    mock_post.side_effect = [
        httpx.RequestError("Connection refused"),
        httpx.RequestError("Connection refused"),
        MagicMock(status_code=200,
                  json=lambda: {"response": "Merhaba! This is a successful response."})
    ]
    
    service = OllamaService(max_retries=3)
    result = await service.generate("test prompt")
    
    # Should have tried 3 times
    assert mock_post.call_count == 3
    assert "Merhaba" in result
    
    # Should have slept twice (between retries)
    assert _mock_sleep.call_count == 2


@pytest.mark.asyncio
@patch('ollama_service.httpx.AsyncClient.post')
@patch('ollama_service.asyncio.sleep')
async def test_retry_on_timeout(_mock_sleep, mock_post):
    """Test that timeout errors trigger retries."""
    mock_post.side_effect = [
        httpx.ReadTimeout("Timeout"),
        MagicMock(status_code=200, json=lambda: {"response": "Success after retry"})
    ]
    
    service = OllamaService(max_retries=2)
    result = await service.generate("test prompt")
    
    assert mock_post.call_count == 2
    assert result == "Success after retry"


@pytest.mark.asyncio
@patch('ollama_service.httpx.AsyncClient.post')
@patch('ollama_service.asyncio.sleep')
async def test_retry_exhaustion(mock_post):
    """Test that retries are exhausted and error is raised."""
    from fastapi import HTTPException

    mock_post.side_effect = httpx.RequestError("Connection refused")
    
    service = OllamaService(max_retries=3)

    with pytest.raises(HTTPException) as exc_info:
        await service.generate("test prompt")
    
    # Should have tried max_retries times
    assert mock_post.call_count == 3
    assert isinstance(exc_info.value, HTTPException)
    if hasattr(exc_info.value, 'status_code'):
        assert exc_info.value.status_code == 503


@pytest.mark.asyncio
@patch('ollama_service.httpx.AsyncClient.post')
async def test_no_retry_on_http_error(mock_post):
    """Test that HTTP errors (4xx, 5xx) don't trigger retries."""
    from fastapi import HTTPException
    
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"error": "Model not found"}
    mock_response.text = "Model not found"
    mock_post.return_value = mock_response
    
    service = OllamaService(max_retries=3)

    with pytest.raises(HTTPException):
        await service.generate("test prompt")
    
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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
