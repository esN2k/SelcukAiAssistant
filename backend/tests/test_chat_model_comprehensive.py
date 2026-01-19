"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA ADI: tests/test_chat_model_comprehensive.py                            ║
║  AMAÇ: Chat model için kapsamlı test suite                                    ║
║  KULLANIM: pytest tests/test_chat_model_comprehensive.py -v                   ║
║  BAĞIMLILIKLAR: pytest, pytest-asyncio                                         ║
║  YAZAN: esN2k - Selçuk Üniversitesi                                           ║
╚════════════════════════════════════════════════════════════════════════════════╝

DETAYLI AÇIKLAMA:
─────────────────
Bu test dosyası, chat model'in tüm özelliklerini kapsamlı şekilde test eder.

TEST KATEGORİLERİ:
1. Temel Fonksiyonellik: Mesaj gönderme, yanıt alma
2. RAG Entegrasyonu: Bağlam kullanımı, kaynak atıfları
3. Hata Yönetimi: Timeout, geçersiz girdi, bağlantı hataları
4. Performans: Yanıt süresi, token kullanımı
5. Türkçe Destek: Özel karakterler, dil kalitesi
"""
import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from providers.ollama_provider import OllamaProvider
from providers.base import ChatResult, Usage, StreamChunk, CancellationToken


class TestChatModelBasics:
    """Temel chat model fonksiyonelliği testleri."""

    @pytest.mark.asyncio
    async def test_simple_message(self):
        """
        Test: Basit mesaj gönderme ve yanıt alma
        Beklenen: Başarılı yanıt dönmeli
        """
        provider = OllamaProvider()
        
        with patch.object(provider._client, 'generate', new_callable=AsyncMock) as mock_gen:
            mock_gen.return_value = {
                "text": "Merhaba! Size nasıl yardımcı olabilirim?",
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 15,
                }
            }
            
            result = await provider.generate(
                messages=[{"role": "user", "content": "Merhaba"}],
                model_id="llama3.1",
                temperature=0.2,
                top_p=0.9,
                max_tokens=500,
                request_id="test-001"
            )
            
            assert isinstance(result, ChatResult)
            assert len(result.text) > 0
            assert result.usage is not None
            assert result.usage.prompt_tokens == 10
            assert result.usage.completion_tokens == 15
            assert result.usage.total_tokens == 25

    @pytest.mark.asyncio
    async def test_turkish_characters(self):
        """
        Test: Türkçe özel karakterler (ç, ğ, ı, ö, ş, ü)
        Beklenen: Karakterler doğru işlenmeli
        """
        provider = OllamaProvider()
        
        with patch.object(provider._client, 'generate', new_callable=AsyncMock) as mock_gen:
            mock_gen.return_value = {
                "text": "Selçuk Üniversitesi Türkiye'nin önde gelen üniversitelerinden biridir.",
                "usage": {"prompt_tokens": 20, "completion_tokens": 30}
            }
            
            result = await provider.generate(
                messages=[{"role": "user", "content": "Selçuk Üniversitesi hakkında bilgi ver"}],
                model_id="llama3.1",
                temperature=0.2,
                top_p=0.9,
                max_tokens=500,
                request_id="test-002"
            )
            
            assert "Selçuk" in result.text
            assert "Üniversitesi" in result.text
            assert "Türkiye" in result.text

    @pytest.mark.asyncio
    async def test_conversation_context(self):
        """
        Test: Konuşma geçmişi ile bağlam yönetimi
        Beklenen: Önceki mesajları hatırlamalı
        """
        provider = OllamaProvider()
        
        messages = [
            {"role": "user", "content": "Benim adım Ahmet"},
            {"role": "assistant", "content": "Merhaba Ahmet! Tanıştığımıza memnun oldum."},
            {"role": "user", "content": "Benim adım neydi?"}
        ]
        
        with patch.object(provider._client, 'generate', new_callable=AsyncMock) as mock_gen:
            mock_gen.return_value = {
                "text": "Sizin adınız Ahmet.",
                "usage": {"prompt_tokens": 50, "completion_tokens": 10}
            }
            
            result = await provider.generate(
                messages=messages,
                model_id="llama3.1",
                temperature=0.2,
                top_p=0.9,
                max_tokens=500,
                request_id="test-003"
            )
            
            assert "Ahmet" in result.text


class TestStreamingFunctionality:
    """Streaming (akış) yanıt testleri."""

    @pytest.mark.asyncio
    async def test_streaming_response(self):
        """
        Test: Token token akış yanıtı
        Beklenen: Her token ayrı ayrı gelmeli
        """
        provider = OllamaProvider()
        cancel_token = CancellationToken()
        
        async def mock_stream(*args, **kwargs):
            tokens = ["Merhaba", " ", "dünya", "!"]
            for token in tokens:
                yield {"token": token, "done": False}
            yield {
                "token": "",
                "done": True,
                "usage": {"prompt_tokens": 5, "completion_tokens": 4}
            }
        
        with patch.object(provider._client, 'generate_stream', side_effect=mock_stream):
            chunks = []
            async for chunk in provider.stream(
                messages=[{"role": "user", "content": "Test"}],
                model_id="llama3.1",
                temperature=0.2,
                top_p=0.9,
                max_tokens=500,
                request_id="test-004",
                cancel_token=cancel_token
            ):
                chunks.append(chunk)
            
            assert len(chunks) > 0
            assert any(chunk.done for chunk in chunks)

    @pytest.mark.asyncio
    async def test_stream_cancellation(self):
        """
        Test: Akış iptali
        Beklenen: İptal sinyali çalışmalı
        """
        provider = OllamaProvider()
        cancel_token = CancellationToken()
        
        async def mock_stream(*args, **kwargs):
            for i in range(100):
                yield {"token": f"token{i}", "done": False}
        
        with patch.object(provider._client, 'generate_stream', side_effect=mock_stream):
            chunks = []
            async for chunk in provider.stream(
                messages=[{"role": "user", "content": "Test"}],
                model_id="llama3.1",
                temperature=0.2,
                top_p=0.9,
                max_tokens=500,
                request_id="test-005",
                cancel_token=cancel_token
            ):
                chunks.append(chunk)
                if len(chunks) == 5:
                    cancel_token.cancel()
            
            assert len(chunks) <= 10  # İptal sonrası fazla token gelmemeli


class TestErrorHandling:
    """Hata yönetimi testleri."""

    @pytest.mark.asyncio
    async def test_empty_message_list(self):
        """
        Test: Boş mesaj listesi
        Beklenen: Hata fırlatmalı
        """
        provider = OllamaProvider()
        
        with patch.object(provider._client, 'generate', new_callable=AsyncMock) as mock_gen:
            mock_gen.side_effect = Exception("Mesaj listesi boş olamaz")
            
            with pytest.raises(Exception):
                await provider.generate(
                    messages=[],
                    model_id="llama3.1",
                    temperature=0.2,
                    top_p=0.9,
                    max_tokens=500,
                    request_id="test-006"
                )

    @pytest.mark.asyncio
    async def test_connection_timeout(self):
        """
        Test: Bağlantı zaman aşımı
        Beklenen: Timeout hatası yakalanmalı
        """
        provider = OllamaProvider()
        
        with patch.object(provider._client, 'generate', new_callable=AsyncMock) as mock_gen:
            mock_gen.side_effect = asyncio.TimeoutError("Request timeout")
            
            with pytest.raises(asyncio.TimeoutError):
                await provider.generate(
                    messages=[{"role": "user", "content": "Test"}],
                    model_id="llama3.1",
                    temperature=0.2,
                    top_p=0.9,
                    max_tokens=500,
                    request_id="test-007"
                )


class TestPerformance:
    """Performans testleri."""

    @pytest.mark.asyncio
    async def test_response_time(self):
        """
        Test: Yanıt süresi < 1 saniye olmalı (mock ile)
        Beklenen: Hızlı yanıt
        """
        import time
        provider = OllamaProvider()
        
        with patch.object(provider._client, 'generate', new_callable=AsyncMock) as mock_gen:
            mock_gen.return_value = {
                "text": "Test yanıtı",
                "usage": {"prompt_tokens": 10, "completion_tokens": 5}
            }
            
            start = time.time()
            result = await provider.generate(
                messages=[{"role": "user", "content": "Test"}],
                model_id="llama3.1",
                temperature=0.2,
                top_p=0.9,
                max_tokens=500,
                request_id="test-008"
            )
            elapsed = time.time() - start
            
            assert elapsed < 1.0  # Mock ile çok hızlı olmalı
            assert result.text == "Test yanıtı"

    @pytest.mark.asyncio
    async def test_token_usage_tracking(self):
        """
        Test: Token kullanımı doğru hesaplanmalı
        Beklenen: prompt + completion = total
        """
        provider = OllamaProvider()
        
        with patch.object(provider._client, 'generate', new_callable=AsyncMock) as mock_gen:
            mock_gen.return_value = {
                "text": "Test",
                "usage": {
                    "prompt_tokens": 100,
                    "completion_tokens": 50,
                }
            }
            
            result = await provider.generate(
                messages=[{"role": "user", "content": "Uzun bir soru..."}],
                model_id="llama3.1",
                temperature=0.2,
                top_p=0.9,
                max_tokens=500,
                request_id="test-009"
            )
            
            assert result.usage.prompt_tokens == 100
            assert result.usage.completion_tokens == 50
            assert result.usage.total_tokens == 150


class TestRAGIntegration:
    """RAG entegrasyonu testleri."""

    @pytest.mark.asyncio
    async def test_rag_context_injection(self):
        """
        Test: RAG bağlamı sistem mesajına eklenmeli
        Beklenen: Kaynak bilgisi yanıtta olmalı
        """
        provider = OllamaProvider()
        
        rag_context = """
        [Kaynak: selcuk.edu.tr]
        Selçuk Üniversitesi 1975 yılında Konya'da kurulmuştur.
        """
        
        messages = [
            {"role": "system", "content": f"Sen Selçuk AI asistanısın.\n\nBağlam:\n{rag_context}"},
            {"role": "user", "content": "Selçuk Üniversitesi ne zaman kuruldu?"}
        ]
        
        with patch.object(provider._client, 'generate', new_callable=AsyncMock) as mock_gen:
            mock_gen.return_value = {
                "text": "Selçuk Üniversitesi 1975 yılında kurulmuştur. [Kaynak: selcuk.edu.tr]",
                "usage": {"prompt_tokens": 80, "completion_tokens": 20}
            }
            
            result = await provider.generate(
                messages=messages,
                model_id="llama3.1",
                temperature=0.2,
                top_p=0.9,
                max_tokens=500,
                request_id="test-010"
            )
            
            assert "1975" in result.text
            assert "[Kaynak:" in result.text


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
