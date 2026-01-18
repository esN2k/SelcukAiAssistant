from prompts import rag_no_source_message
from rag_guard import apply_rag_guard, is_context_relevant


def test_context_relevance_positive():
    context = "Selçuk Üniversitesi Konya'dadır."
    assert is_context_relevant("Selçuk Üniversitesi nerede?", context, "tr") is True


def test_context_relevance_negative():
    context = "Selçuk Üniversitesi Konya'dadır."
    assert is_context_relevant("Mars'ta yaşam var mı?", context, "tr") is False


def test_apply_rag_guard_filters_hallucination():
    context = "Selçuk Üniversitesi Konya'dadır."
    answer = (
        "Selçuk Üniversitesi Konya'dadır. "
        "Türkiye'nin en eski üniversitelerindendir."
    )
    filtered, applied = apply_rag_guard(
        "Selçuk Üniversitesi nerede?",
        answer,
        context,
        "tr",
    )
    assert applied is True
    assert "Konya" in filtered
    assert "en eski" not in filtered


def test_apply_rag_guard_no_source():
    context = "Selçuk Üniversitesi Konya'dadır."
    answer = "Evet, Mars'ta yaşam vardır."
    filtered, applied = apply_rag_guard(
        "Mars'ta yaşam var mı?",
        answer,
        context,
        "tr",
    )
    assert applied is True
    assert filtered == rag_no_source_message("tr")
