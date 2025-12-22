"""Unit tests for server-side response cleaning."""
from response_cleaner import StreamingResponseCleaner, clean_text


def test_clean_text_strips_meta_prefix():
    text = (
        "Okay, I need to help the user by thinking.\n"
        "Merhaba! Selcuk University 1975 yilinda kuruldu."
    )
    cleaned = clean_text(text, language="tr")
    assert "Okay, I need to help the user" not in cleaned
    assert "Merhaba" in cleaned


def test_clean_text_removes_think_tags():
    text = "<think>internal plan</think>Final answer."
    cleaned = clean_text(text, language="en")
    assert "<think>" not in cleaned
    assert "Final answer" in cleaned


def test_clean_text_preserves_code_blocks():
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
    cleaner = StreamingResponseCleaner(language="en")
    output = ""
    output += cleaner.feed("Okay, I need to help the user by thinking. ")
    output += cleaner.feed("Here is the answer.\n")
    output += cleaner.finalize()
    assert "Okay, I need to help the user" not in output
    assert "Here is the answer" in output
