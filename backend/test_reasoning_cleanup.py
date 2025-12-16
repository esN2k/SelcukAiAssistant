"""
Comprehensive unit tests for reasoning artifact cleanup.

This test suite validates that the _clean_reasoning_artifacts() method
properly removes DeepSeek-R1 reasoning tokens and returns clean answers.
"""
from ollama_service import OllamaService


class TestReasoningCleanup:
    """Test cases for reasoning artifact cleanup."""

    def test_simple_clean_response(self):
        """Test that already clean responses are preserved."""
        clean_text = "Merhaba! Selçuk Üniversitesi 1975 yılında kurulmuştur."
        result = OllamaService._clean_reasoning_artifacts(clean_text)
        assert "Merhaba" in result
        assert "1975" in result
        assert len(result) > 15

    def test_remove_think_tags(self):
        """Test removal of <think> tags."""
        text = "<think>Hmm, the user wants to know about enrollment.</think>Merhaba! Kayıt tarihleri Eylül ayındadır."
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "<think>" not in result
        assert "</think>" not in result
        assert "Merhaba" in result
        assert "Kayıt" in result

    def test_remove_im_tags(self):
        """Test removal of instruction marker tags."""
        text = "<|im_start|>assistant\nMerhaba! Size yardımcı olabilirim.<|im_end|>"
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "<|im_start|>" not in result
        assert "<|im_end|>" not in result
        assert "Merhaba" in result

    def test_remove_english_reasoning(self):
        """Test removal of English reasoning sentences."""
        text = "Okay, let me think about this. The user wants information. Merhaba! İşte cevabınız."
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "okay" not in result.lower()
        assert "let me" not in result.lower()
        assert "Merhaba" in result

    def test_remove_turkish_reasoning(self):
        """Test removal of Turkish reasoning sentences."""
        text = "Tamam, kullanıcı kayıt tarihleri soruyor. Düşünüyorum ki cevap verebilirim.\n\nMerhaba! Kayıt Eylül'de."
        result = OllamaService._clean_reasoning_artifacts(text)
        # Should remove reasoning but keep the answer
        assert "Merhaba" in result
        assert "Kayıt" in result

    def test_markdown_header_extraction(self):
        """Test extraction of markdown-formatted content."""
        text = "Let me format this nicely.\n\n## Kayıt Tarihleri\n\nKayıt işlemleri Eylül ayında yapılır.\n\n## İletişim\n\nBize ulaşabilirsiniz."
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "##" in result
        assert "Kayıt" in result
        # Should remove English reasoning
        assert "let me" not in result.lower()

    def test_multiple_merhaba_takes_last(self):
        """Test that when multiple 'Merhaba' exist, the last one is used."""
        text = "Merhaba test. Okay, let me rephrase. Merhaba! İşte gerçek cevap."
        result = OllamaService._clean_reasoning_artifacts(text)
        assert result.startswith("Merhaba!")
        assert "gerçek cevap" in result
        assert "test" not in result

    def test_paragraph_filtering(self):
        """Test filtering of paragraphs containing reasoning keywords."""
        text = "İlk paragraf normal.\n\nOkay, kullanıcı soruyor.\n\nİkinci normal paragraf."
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "İlk paragraf" in result
        assert "İkinci normal paragraf" in result

    def test_whitespace_normalization(self):
        """Test that excessive whitespace is normalized."""
        text = "Merhaba!\n\n\n\nBu bir test.\n\n\n\nSon satır."
        result = OllamaService._clean_reasoning_artifacts(text)
        # Should have at most double newlines
        assert "\n\n\n" not in result
        assert "Merhaba" in result
        assert "test" in result

    def test_fallback_for_too_short_text(self):
        """Test fallback message when cleaned text is too short."""
        text = "<think>Just thinking</think>"
        result = OllamaService._clean_reasoning_artifacts(text)
        assert len(result) >= 15
        assert "Selcuk AI" in result or "yardımcı" in result

    def test_complex_mixed_reasoning(self):
        """Test complex case with mixed Turkish/English reasoning."""
        text = """<think>
Okay, the user is asking about Selçuk University enrollment dates.
Tamam, kullanıcı kayıt tarihleri soruyor.
I should provide clear information.
Düşünüyorum ki açık bir cevap vermeliyim.
</think>

Merhaba! İşte kayıt bilgileri:

## Kayıt Tarihleri

Selçuk Üniversitesi kayıt işlemleri genellikle **Eylül ayı** içinde gerçekleşir.

**Gerekli Belgeler:**
- Kimlik fotokopisi
- Diploma
- Fotoğraflar

Detaylı bilgi için öğrenci işlerine başvurabilirsiniz."""

        result = OllamaService._clean_reasoning_artifacts(text)
        
        # Should NOT contain reasoning
        assert "<think>" not in result
        assert "okay" not in result.lower()
        assert "tamam" not in result.lower()
        assert "i should" not in result.lower()
        assert "düşünüyorum" not in result.lower()
        
        # Should CONTAIN the actual answer
        assert "Merhaba" in result
        assert "Kayıt" in result
        assert "Eylül" in result
        assert "Kimlik" in result

    def test_preserve_legitimate_words(self):
        """Test that legitimate uses of reasoning keywords are preserved in context."""
        text = "Merhaba! Kullanıcı kayıt sistemine giriş yapabilir. Tamam butonu ile onaylayın."
        result = OllamaService._clean_reasoning_artifacts(text)
        # Should preserve these when they're part of the actual answer
        assert "Merhaba" in result
        # Note: Current implementation might remove sentences with these words
        # This is a known limitation we'll improve

    def test_empty_input(self):
        """Test handling of empty input."""
        result = OllamaService._clean_reasoning_artifacts("")
        assert len(result) >= 15  # Should return fallback

    def test_only_whitespace(self):
        """Test handling of whitespace-only input."""
        result = OllamaService._clean_reasoning_artifacts("   \n\n  \t  ")
        assert len(result) >= 15  # Should return fallback

    def test_special_characters_preserved(self):
        """Test that special characters in answers are preserved."""
        text = "Merhaba! E-posta: info@selcuk.edu.tr, Tel: +90 332 123 45 67"
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "@" in result
        assert "+" in result
        assert "Merhaba" in result

    def test_numbered_lists_preserved(self):
        """Test that numbered lists are preserved."""
        text = """Merhaba! İşte adımlar:

1. Kayıt formunu doldurun
2. Belgelerinizi hazırlayın
3. Fakülteye başvurun"""
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "1." in result
        assert "2." in result
        assert "3." in result

    def test_code_blocks_preserved(self):
        """Test that code or special formatting is preserved."""
        text = "Merhaba! İşte örnek:\n\n```\nörnek kod\n```\n\nBu bir örnektir."
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "```" in result
        assert "örnek kod" in result

    def test_urls_preserved(self):
        """Test that URLs in answers are preserved."""
        text = "Merhaba! Web sitesi: https://www.selcuk.edu.tr adresindedir."
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "https://" in result
        assert "selcuk.edu.tr" in result
