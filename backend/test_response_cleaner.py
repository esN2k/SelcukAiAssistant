"""Sunucu tarafı yanıt temizleme için birim testleri.

Giriş: Örnek metinler.
Çıkış: Temizlenmiş metinler.
İşleyiş: Meta içerik ve think blokları ayıklanır.
"""
from response_cleaner import StreamingResponseCleaner, clean_text


def test_clean_text_strips_meta_prefix():
    """Giriş: Meta prefix.

    Çıkış: Temiz metin.
    İşleyiş: Prefix içeriği silinir.
    """
    text = (
        "Okay, I need to help the user by thinking.\n"
        "Merhaba! Selçuk Üniversitesi 1975 yılında kuruldu."
    )
    cleaned = clean_text(text, language="tr")
    assert "Okay, I need to help the user" not in cleaned
    assert "Merhaba" in cleaned


def test_clean_text_removes_think_tags():
    """Giriş: <think> tag'leri.

    Çıkış: Tagsiz metin.
    İşleyiş: Tag temizleme yapılır.
    """
    text = "<think>internal plan</think>Final answer."
    cleaned = clean_text(text, language="en")
    assert "<think>" not in cleaned
    assert "Final answer" in cleaned


def test_clean_text_preserves_code_blocks():
    """Giriş: Kod bloğu.

    Çıkış: Blok korunur.
    İşleyiş: Fence ayrımı ile kod blokları korunur.
    """
    text = (
        "Okay, I need to help the user.\n\n"
        "```python\nprint('hi')\n```\n"
        "Answer: done."
    )
    cleaned = clean_text(text, language="en")
    assert "Okay, I need to help the user" not in cleaned
    assert "```python" in cleaned
    assert "print('hi')" in cleaned
    assert "Answer: done." in cleaned


def test_streaming_cleaner_strips_meta_sentences():
    """Giriş: Meta cümleleri.

    Çıkış: Gerçek cevap.
    İşleyiş: Akış filtresi meta cümlelerini ayıklar.
    """
    cleaner = StreamingResponseCleaner(language="en")
    output = ""
    output += cleaner.feed("Okay, I need to help the user by thinking. ")
    output += cleaner.feed("Here is the answer.\n")
    output += cleaner.finalize()
    assert "Okay, I need to help the user" not in output
    assert "Here is the answer" in output
