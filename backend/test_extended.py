"""FastAPI backend için genişletilmiş birim testleri.

Giriş: TestClient ve mock nesneler.
Çıkış: HTTP yanıtları ve fonksiyon sonuçları doğrulanır.
İşleyiş: Doğrulama, retry ve RAG akışları test edilir.
"""
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import numpy as np
import pytest
from fastapi.testclient import TestClient

from config import Config
from main import app
from ollama_service import OllamaService
from providers.base import ChatResult
from providers.ollama_provider import OllamaProvider
from rag_service import Document, RAGService, RagIndex, chunk_text

client = TestClient(app)


def _chat_payload(content: str) -> dict[str, list[dict[str, str]]]:
    """Giriş: Kullanıcı mesajı.

    Çıkış: Chat payload sözlüğü.
    İşleyiş: /chat şemasına uygun JSON üretir.
    """
    return {"messages": [{"role": "user", "content": content}]}


# ============================================================================
# Input Validation Tests
# ============================================================================


def test_chat_empty_question():
    """Giriş: Boş mesaj.

    Çıkış: 422.
    İşleyiş: İçerik doğrulamasını kontrol eder.
    """
    response = client.post("/chat", json=_chat_payload(""))
    assert response.status_code == 422


def test_chat_whitespace_only_question():
    """Giriş: Sadece boşluk.

    Çıkış: 422.
    İşleyiş: İçerik doğrulamasını kontrol eder.
    """
    response = client.post("/chat", json=_chat_payload("   "))
    assert response.status_code == 422


def test_chat_too_long_question():
    """Giriş: Aşırı uzun içerik.

    Çıkış: 422.
    İşleyiş: Uzunluk kontrolünü doğrular.
    """
    long_question = "a" * 11000
    response = client.post("/chat", json=_chat_payload(long_question))
    assert response.status_code == 422


def test_chat_xss_prevention():
    """Giriş: Zararlı içerik.

    Çıkış: 422.
    İşleyiş: XSS filtre kontrolünü doğrular.
    """
    dangerous_inputs = [
        "<script>alert('xss')</script>",
        "test javascript:alert(1)",
        "test onerror=alert(1)",
        "test onload=alert(1)",
    ]
    for dangerous_input in dangerous_inputs:
        response = client.post("/chat", json=_chat_payload(dangerous_input))
        assert response.status_code == 422


@patch.object(OllamaProvider, "generate", new_callable=AsyncMock)
def test_chat_valid_input_with_sanitization(mock_generate):
    """Giriş: Geçerli içerik.

    Çıkış: 200.
    İşleyiş: Sanitize sonrası başarılı yanıt bekler.
    """
    mock_generate.return_value = ChatResult(text="Test response")
    response = client.post("/chat", json=_chat_payload("  Test question  "))
    assert response.status_code == 200


# ============================================================================
# Health Check Model Matching Tests
# ============================================================================


@pytest.mark.asyncio
@patch("ollama_service.httpx.AsyncClient.get")
async def test_health_check_exact_match(mock_get):
    """Giriş: Tam model adı.

    Çıkış: healthy.
    İşleyiş: /api/tags eşleşmesini doğrular.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "models": [{"name": Config.OLLAMA_MODEL}, {"name": "mistral"}]
    }
    mock_get.return_value = mock_response

    service = OllamaService()
    health = await service.health_check()
    assert health["status"] == "healthy"
    assert health["model_available"] is True


@pytest.mark.asyncio
@patch("ollama_service.httpx.AsyncClient.get")
async def test_health_check_with_latest_tag(mock_get):
    """Giriş: latest tag.

    Çıkış: healthy.
    İşleyiş: Tag eşleşmesini doğrular.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "models": [{"name": f"{Config.OLLAMA_MODEL}:latest"}, {"name": "mistral:latest"}]
    }
    mock_get.return_value = mock_response

    service = OllamaService()
    health = await service.health_check()
    assert health["status"] == "healthy"
    assert health["model_available"] is True


@pytest.mark.asyncio
@patch("ollama_service.httpx.AsyncClient.get")
async def test_health_check_reverse_tag_match(mock_get):
    """Giriş: Base model.

    Çıkış: available.
    İşleyiş: Ters tag eşleşmesini doğrular.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "models": [{"name": "selcuk_ai_assistant"}, {"name": "llama3.1"}]
    }
    mock_get.return_value = mock_response

    service = OllamaService()
    health = await service.health_check(model="selcuk_ai_assistant:latest")
    assert health["model_available"] is True


def test_is_model_available_helper():
    """Giriş: Model listeleri.

    Çıkış: bool.
    İşleyiş: Yardımcı fonksiyonun eşleşmesini doğrular.
    """
    assert OllamaService._is_model_available("llama3.1", ["llama3.1", "mistral"])
    assert OllamaService._is_model_available("llama3.1", ["llama3.1:latest"])
    assert OllamaService._is_model_available("llama3.1:latest", ["llama3.1"])
    assert not OllamaService._is_model_available("gpt4", ["llama3.1", "mistral"])
    assert not OllamaService._is_model_available("llama3.1", [])
    assert not OllamaService._is_model_available("", ["llama3.1"])


# ============================================================================
# Retry Logic Tests
# ============================================================================


@pytest.mark.asyncio
@patch("ollama_service.httpx.AsyncClient.post")
@patch("ollama_service.asyncio.sleep")
async def test_retry_on_connection_error(_mock_sleep, mock_post):
    """Giriş: Bağlantı hatası.

    Çıkış: Retry sonrası yanıt.
    İşleyiş: Tekrar deneme akışını doğrular.
    """
    mock_post.side_effect = [
        httpx.RequestError("Connection refused"),
        httpx.RequestError("Connection refused"),
        MagicMock(
            status_code=200,
            json=lambda: {"message": {"content": "Merhaba! This is a response."}},
        ),
    ]

    service = OllamaService(max_retries=3)
    result = await service.generate(
        messages=[{"role": "user", "content": "test"}],
        model=Config.OLLAMA_MODEL,
        temperature=0.2,
        top_p=0.9,
        max_tokens=32,
    )

    assert mock_post.call_count == 3
    assert "Merhaba" in result["text"]
    assert _mock_sleep.call_count == 2


@pytest.mark.asyncio
@patch("ollama_service.httpx.AsyncClient.post")
@patch("ollama_service.asyncio.sleep")
async def test_retry_on_timeout(_mock_sleep, mock_post):
    """Giriş: Timeout.

    Çıkış: Retry sonrası yanıt.
    İşleyiş: Zaman aşımı tekrarlarını doğrular.
    """
    mock_post.side_effect = [
        httpx.ReadTimeout("Timeout"),
        MagicMock(
            status_code=200,
            json=lambda: {"message": {"content": "Success after retry"}},
        ),
    ]

    service = OllamaService(max_retries=2)
    result = await service.generate(
        messages=[{"role": "user", "content": "test"}],
        model=Config.OLLAMA_MODEL,
        temperature=0.2,
        top_p=0.9,
        max_tokens=32,
    )

    assert mock_post.call_count == 2
    assert result["text"] == "Success after retry"


@pytest.mark.asyncio
@patch("ollama_service.httpx.AsyncClient.post")
@patch("ollama_service.asyncio.sleep")
async def test_retry_exhaustion(_mock_sleep, mock_post):
    """Giriş: Sürekli hata.

    Çıkış: HTTPException 503.
    İşleyiş: Retry tükenmesi senaryosunu doğrular.
    """
    from fastapi import HTTPException

    mock_post.side_effect = httpx.RequestError("Connection refused")

    service = OllamaService(max_retries=3)
    with pytest.raises(HTTPException) as exc_info:
        await service.generate(
            messages=[{"role": "user", "content": "test"}],
            model=Config.OLLAMA_MODEL,
            temperature=0.2,
            top_p=0.9,
            max_tokens=32,
        )

    assert mock_post.call_count == 3
    assert exc_info.value.status_code == 503


@pytest.mark.asyncio
@patch("ollama_service.httpx.AsyncClient.post")
async def test_no_retry_on_http_error(mock_post):
    """Giriş: HTTP 404.

    Çıkış: Tek deneme.
    İşleyiş: HTTP hatasında retry yapılmadığını doğrular.
    """
    from fastapi import HTTPException

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"error": "Model not found"}
    mock_response.text = "Model not found"
    mock_post.return_value = mock_response

    service = OllamaService(max_retries=3)
    with pytest.raises(HTTPException):
        await service.generate(
            messages=[{"role": "user", "content": "test"}],
            model=Config.OLLAMA_MODEL,
            temperature=0.2,
            top_p=0.9,
            max_tokens=32,
        )

    assert mock_post.call_count == 1


# ============================================================================
# RAG Service Tests
# ============================================================================


def test_rag_service_initialization_disabled():
    """Giriş: RAG disabled.

    Çıkış: Boş bağlam.
    İşleyiş: Devre dışı kontrolünü doğrular.
    """
    service = RAGService(enabled=False)
    assert service.enabled is False
    context, citations = service.get_context("test query")
    assert context == ""
    assert citations == []


class DummyEmbeddingBackend:
    """Giriş: Test amaçlı gömme üretici.

    Çıkış: Sabit boyutlu vektörler.
    İşleyiş: Metin uzunluğu tabanlı vektör üretir.
    """

    def __init__(self) -> None:
        """Giriş: yok.

        Çıkış: Nesne.
        İşleyiş: Boyutu sabitler.
        """
        self._dimension = 3

    @property
    def dimension(self) -> int:
        """Giriş: yok.

        Çıkış: Boyut.
        İşleyiş: Sabit değer döndürür.
        """
        return self._dimension

    def embed(self, texts: list[str]) -> np.ndarray:
        """Giriş: Metin listesi.

        Çıkış: Normalize vektörler.
        İşleyiş: Uzunluk tabanlı vektör üretir.
        """
        vectors = []
        for text in texts:
            vectors.append(
                [float(len(text)), float(text.count("a")), float(text.count("b"))]
            )
        array = np.array(vectors, dtype="float32")
        if array.size == 0:
            return array
        norms = np.linalg.norm(array, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return array / norms


def test_rag_service_initialization_enabled(tmp_path):
    """Giriş: Geçerli ayarlar.

    Çıkış: Aktif RAG.
    İşleyiş: İndeks kurulumunu doğrular.
    """
    service = RAGService(
        enabled=True,
        vector_db_path=str(tmp_path),
        collection_name="test_collection",
        chunk_size=300,
        chunk_overlap=30,
        embedder=DummyEmbeddingBackend(),
    )
    assert service.enabled is True
    assert service.vector_db_path == str(tmp_path)
    assert service.collection_name == "test_collection"
    assert service.chunk_size == 300
    assert service.chunk_overlap == 30


def test_rag_service_search_when_disabled():
    """Giriş: RAG disabled.

    Çıkış: Boş sonuç.
    İşleyiş: Arama bypass kontrolü.
    """
    service = RAGService(enabled=False)
    results = service.search("test query")
    assert results == []


def test_rag_service_ingest_when_disabled():
    """Giriş: RAG disabled.

    Çıkış: RuntimeError.
    İşleyiş: Korumalı ekleme doğrulanır.
    """
    service = RAGService(enabled=False)
    with pytest.raises(RuntimeError, match="RAG servisi etkin değil"):
        service.add_documents([Document(content="test content")])


def test_document_creation():
    """Giriş: Document.

    Çıkış: Alan doğrulama.
    İşleyiş: Dataclass davranışını kontrol eder.
    """
    doc = Document(
        content="Test content",
        metadata={"source": "test.txt", "date": "2024-01-01"},
        doc_id="doc_123",
    )
    assert doc.content == "Test content"
    assert doc.metadata["source"] == "test.txt"
    assert doc.doc_id == "doc_123"
    assert "Test content" in repr(doc)


def test_rag_chunk_document():
    """Giriş: Uzun metin.

    Çıkış: Parçalara bölme.
    İşleyiş: chunk_text fonksiyonunu doğrular.
    """
    content = "0123456789abcdefghij"
    chunks = chunk_text(content, chunk_size=10, chunk_overlap=3)
    assert all(len(chunk) <= 10 for chunk in chunks)
    assert len(chunks) > 1


def test_rag_index_add_and_search(tmp_path):
    """Giriş: İki doc.

    Çıkış: Arama sonucu.
    İşleyiş: İndeks ekleme/arama akışını doğrular.
    """
    embedder = DummyEmbeddingBackend()
    index = RagIndex(tmp_path, embedder)
    docs = [
        Document(content="aaa bbb", metadata={"source": "a.txt"}),
        Document(content="cccc dddd", metadata={"source": "b.txt"}),
    ]
    added = index.add_documents(docs)
    assert added == 2

    results = index.search("aaa", top_k=1)
    assert len(results) == 1
    assert results[0].metadata.get("source") == "a.txt"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
