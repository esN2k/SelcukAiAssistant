"""RAG doğruluk kontrolü ve kaynak tabanlı cevap filtreleme."""
from __future__ import annotations

import re
import unicodedata

from prompts import rag_no_source_message


_TURKISH_MAP = str.maketrans(
    {
        "ç": "c",
        "ğ": "g",
        "ı": "i",
        "İ": "i",
        "ö": "o",
        "ş": "s",
        "ü": "u",
    }
)

_STOPWORDS_TR = {
    "ve",
    "veya",
    "ile",
    "icin",
    "kadar",
    "gibi",
    "bu",
    "su",
    "o",
    "bir",
    "mi",
    "mı",
    "mu",
    "mü",
    "nedir",
    "neler",
    "nerede",
    "hangi",
    "kac",
    "kim",
    "var",
    "yok",
    "degil",
    "de",
    "da",
    "den",
    "dan",
}

_STOPWORDS_EN = {
    "the",
    "and",
    "or",
    "for",
    "with",
    "what",
    "where",
    "which",
    "how",
    "who",
    "is",
    "are",
    "was",
    "were",
    "in",
    "on",
    "at",
    "of",
    "a",
    "an",
    "to",
    "from",
    "about",
    "info",
    "information",
    "please",
}


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().translate(_TURKISH_MAP)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _content_tokens(text: str, language: str) -> list[str]:
    normalized = _normalize(text)
    if not normalized:
        return []
    tokens = normalized.split()
    stopwords = _STOPWORDS_EN if language.lower().startswith("en") else _STOPWORDS_TR
    return [
        token
        for token in tokens
        if (len(token) >= 3 or token.isdigit()) and token not in stopwords
    ]


def _overlap_count(tokens: list[str], context_tokens: set[str]) -> int:
    overlap = 0
    for token in set(tokens):
        if token in context_tokens:
            overlap += 1
            continue
        if len(token) < 4:
            continue
        for ctx in context_tokens:
            if ctx.startswith(token) or token.startswith(ctx):
                overlap += 1
                break
    return overlap


def is_context_relevant(question: str, context: str, language: str) -> bool:
    question_tokens = _content_tokens(question, language)
    context_tokens = set(_content_tokens(context, language))
    if not question_tokens or not context_tokens:
        return False
    return _overlap_count(question_tokens, context_tokens) >= 1


def _unsupported_numbers(tokens: list[str], context_tokens: set[str]) -> bool:
    numbers = [token for token in tokens if token.isdigit()]
    return any(number not in context_tokens for number in numbers)


def _is_sentence_grounded(sentence: str, context_tokens: set[str], language: str) -> bool:
    tokens = _content_tokens(sentence, language)
    if not tokens:
        return False
    if _unsupported_numbers(tokens, context_tokens):
        return False
    overlap = _overlap_count(tokens, context_tokens)
    required = 1 if len(tokens) <= 4 else 2
    return overlap >= required


def filter_ungrounded_sentences(answer: str, context: str, language: str) -> str:
    context_tokens = set(_content_tokens(context, language))
    if not context_tokens:
        return ""
    lines = answer.splitlines()
    filtered_lines: list[str] = []
    for line in lines:
        if not line.strip():
            filtered_lines.append(line)
            continue

        bullet_match = re.match(r"^(\s*[-*]\s+)(.*)$", line)
        prefix = ""
        body = line
        if bullet_match:
            prefix = bullet_match.group(1)
            body = bullet_match.group(2)

        sentences = re.split(r"(?<=[.!?])\s+", body.strip())
        kept = [
            sentence
            for sentence in sentences
            if sentence and _is_sentence_grounded(sentence, context_tokens, language)
        ]
        if kept:
            filtered_lines.append(prefix + " ".join(kept))

    return "\n".join(filtered_lines).strip()


def apply_rag_guard(
    question: str,
    answer: str,
    context: str,
    language: str,
) -> tuple[str, bool]:
    if not context.strip():
        return answer, False
    if not is_context_relevant(question, context, language):
        return rag_no_source_message(language), True
    filtered = filter_ungrounded_sentences(answer, context, language)
    if not filtered:
        return rag_no_source_message(language), True
    if filtered != answer:
        return filtered, True
    return answer, False
