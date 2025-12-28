"""Düşünce izi temizleme için kapsamlı testler.

Giriş: Örnek cevap metinleri.
Çıkış: Temizlenmiş metin.
İşleyiş: Think tag, meta cümle ve işaret temizliği doğrulanır.
"""
from ollama_service import OllamaService


class TestReasoningCleanup:
    """Giriş: Test senaryoları.

    Çıkış: Beklenen temiz metinler.
    İşleyiş: Temizleme kurallarını farklı örneklerle doğrular.
    """

    def test_simple_clean_response(self):
        """Giriş: Temiz metin.

        Çıkış: Metin korunur.
        İşleyiş: Değişiklik yapılmadığını doğrular.
        """
        clean_text = "Merhaba! Selçuk Üniversitesi 1975 yılında kurulmuştur."
        result = OllamaService._clean_reasoning_artifacts(clean_text)
        assert "Merhaba" in result
        assert "1975" in result
        assert len(result) > 15

    def test_remove_think_tags(self):
        """Giriş: Think tag'leri.

        Çıkış: Tagsiz metin.
        İşleyiş: Think içerikleri temizlenir.
        """
        text = (
            "<think>Hmm, the user wants to know about enrollment.</think>"
            "Merhaba! Kayıt tarihleri Eylül ayındadır."
        )
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "<think>" not in result
        assert "</think>" not in result
        assert "Merhaba" in result
        assert "Kayıt" in result

    def test_remove_im_tags(self):
        """Giriş: Instruction tag'leri.

        Çıkış: Temiz metin.
        İşleyiş: Özel tokenlar ayıklanır.
        """
        text = "<|im_start|>assistant\nMerhaba! Size yardımcı olabilirim.<|im_end|>"
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "<|im_start|>" not in result
        assert "<|im_end|>" not in result
        assert "Merhaba" in result

    def test_remove_english_reasoning(self):
        """Giriş: İngilizce meta cümle.

        Çıkış: Temiz metin.
        İşleyiş: Meta cümleler silinir.
        """
        text = (
            "Okay, let me think about this. The user wants information. "
            "Merhaba! İşte cevabınız."
        )
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "okay" not in result.lower()
        assert "let me" not in result.lower()
        assert "Merhaba" in result

    def test_remove_turkish_reasoning(self):
        """Giriş: Türkçe meta cümle.

        Çıkış: Cevap korunur.
        İşleyiş: Meta cümleler silinir.
        """
        text = (
            "Tamam, kullanıcı kayıt tarihleri soruyor. Düşünüyorum ki cevap verebilirim.\n\n"
            "Merhaba! Kayıt Eylül'de."
        )
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "Merhaba" in result
        assert "Kayıt" in result

    def test_markdown_header_extraction(self):
        """Giriş: Markdown başlığı.

        Çıkış: Başlık korunur.
        İşleyiş: Header seçimi yapılır.
        """
        text = (
            "Let me format this nicely.\n\n## Kayıt Tarihleri\n\n"
            "Kayıt işlemleri Eylül ayında yapılır.\n\n## İletişim\n\n"
            "Bize ulaşabilirsiniz."
        )
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "##" in result
        assert "Kayıt" in result
        assert "let me" not in result.lower()

    def test_multiple_merhaba_takes_last(self):
        """Giriş: Birden çok selamlama.

        Çıkış: Son selamlama.
        İşleyiş: Son indeks korunur.
        """
        text = "Merhaba test. Okay, let me rephrase. Merhaba! İşte gerçek cevap."
        result = OllamaService._clean_reasoning_artifacts(text)
        assert result.startswith("Merhaba!")
        assert "gerçek cevap" in result
        assert "test" not in result

    def test_paragraph_filtering(self):
        """Giriş: Meta paragraf.

        Çıkış: Meta silinir.
        İşleyiş: Paragraf filtresi uygulanır.
        """
        text = "İlk paragraf normal.\n\nOkay, kullanıcı soruyor.\n\nİkinci normal paragraf."
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "İlk paragraf" in result
        assert "İkinci normal paragraf" in result

    def test_whitespace_normalization(self):
        """Giriş: Fazla boşluk.

        Çıkış: Normalize metin.
        İşleyiş: Boşluk temizleme uygulanır.
        """
        text = "Merhaba!\n\n\n\nBu bir test.\n\n\n\nSon satır."
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "\n\n\n" not in result
        assert "Merhaba" in result
        assert "test" in result

    def test_fallback_for_too_short_text(self):
        """Giriş: Çok kısa metin.

        Çıkış: Fallback mesajı.
        İşleyiş: Minimum uzunluk kontrolü yapılır.
        """
        text = "<think>Just thinking</think>"
        result = OllamaService._clean_reasoning_artifacts(text)
        assert len(result) >= 15
        assert "Selçuk AI" in result or "yardımcı" in result

    def test_complex_mixed_reasoning(self):
        """Giriş: Karışık düşünce izi.

        Çıkış: Temiz yanıt.
        İşleyiş: Kapsamlı temizleme uygulanır.
        """
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

        assert "<think>" not in result
        assert "okay" not in result.lower()
        assert "tamam" not in result.lower()
        assert "i should" not in result.lower()
        assert "düşünüyorum" not in result.lower()

        assert "Merhaba" in result
        assert "Kayıt" in result
        assert "Eylül" in result
        assert "Kimlik" in result

    def test_preserve_legitimate_words(self):
        """Giriş: Geçerli kelimeler.

        Çıkış: Korunmuş yanıt.
        İşleyiş: Yanlış pozitifleri engeller.
        """
        text = (
            "Merhaba! Kullanıcı kayıt sistemine giriş yapabilir. "
            "Tamam butonu ile onaylayın."
        )
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "Merhaba" in result

    def test_empty_input(self):
        """Giriş: Boş metin.

        Çıkış: Fallback mesajı.
        İşleyiş: Boşluk kontrolü yapılır.
        """
        result = OllamaService._clean_reasoning_artifacts("")
        assert len(result) >= 15

    def test_only_whitespace(self):
        """Giriş: Sadece boşluk.

        Çıkış: Fallback mesajı.
        İşleyiş: Boşluk kontrolü yapılır.
        """
        result = OllamaService._clean_reasoning_artifacts("   \n\n  \t  ")
        assert len(result) >= 15

    def test_special_characters_preserved(self):
        """Giriş: Özel karakterler.

        Çıkış: Korunmuş metin.
        İşleyiş: Özel karakterlerin silinmediğini doğrular.
        """
        text = "Merhaba! E-posta: info@selcuk.edu.tr, Tel: +90 332 123 45 67"
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "@" in result
        assert "+" in result
        assert "Merhaba" in result

    def test_numbered_lists_preserved(self):
        """Giriş: Numaralı liste.

        Çıkış: Liste korunur.
        İşleyiş: Markdown liste düzenini korur.
        """
        text = """Merhaba! İşte adımlar:

1. Kayıt formunu doldurun
2. Belgelerinizi hazırlayın
3. Fakülteye başvurun"""
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "1." in result
        assert "2." in result
        assert "3." in result

    def test_code_blocks_preserved(self):
        """Giriş: Kod bloğu.

        Çıkış: Blok korunur.
        İşleyiş: Kod blokları silinmez.
        """
        text = "Merhaba! İşte örnek:\n\n```\nÖrnek kod\n```\n\nBu bir örnektir."
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "```" in result
        assert "Örnek kod" in result

    def test_urls_preserved(self):
        """Giriş: URL.

        Çıkış: URL korunur.
        İşleyiş: URL metninin bozulmadığını doğrular.
        """
        text = "Merhaba! Web sitesi: https://www.selcuk.edu.tr adresindedir."
        result = OllamaService._clean_reasoning_artifacts(text)
        assert "https://" in result
        assert "selcuk.edu.tr" in result
