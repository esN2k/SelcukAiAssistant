"""Sunucu tarafında sohbet çıktılarının temizlenmesi için yardımcılar."""
from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import List, Tuple

from utils import ReasoningFilter


_META_LINE = re.compile(
    r"^\s*(?:"
    r"(?:reasoning|analysis|thoughts?|chain of thought|let me think)\s*:?\s*$|"
    r"(?:final answer|final|answer)\s*:?\s*$|"
    r"(?:ok(?:ay)?[, ]+i need to respond.*)$"
    r")",
    re.IGNORECASE,
)

_META_PREFIX = re.compile(
    r"^[\s\"']*(?:(?:so|well|then|next|since|maybe)[,\s]+)?(?:"
    r"okay|alright|sure|let me|let me think|i need to|i will|i should|i'?ll|"
    r"first|here'?s my|my plan|the user|they just|they said|they mentioned|"
    r"they'?re|they are|"
    r"they probably|they might|they want|user is|"
    r"i am going to|i'?m going to|i want to|tamam|peki|öncelikle|oncelikle|"
    r"ilk olarak|kullanıcı|kullanici|düşünüyorum|dusunuyorum"
    r")\b",
    re.IGNORECASE,
)

_META_SENTENCE = re.compile(
    r"^[\s\"']*(?:(?:so|well|then|next|since|maybe)[,\s]+)?(?:"
    r"okay|alright|sure|let me|let me think|i need to|i will|i should|i'?ll|"
    r"first|here'?s my|my plan|the user|they just|they said|they mentioned|"
    r"they'?re|they are|"
    r"they probably|they might|they want|user is|"
    r"i am going to|i'?m going to|i want to|tamam|peki|öncelikle|oncelikle|"
    r"ilk olarak|kullanıcı|kullanici|düşünüyorum|dusunuyorum"
    r")[^.!?\n]*[.!?]\s*",
    re.IGNORECASE,
)

_META_PREFIX_FRAGMENT = re.compile(
    r"^[\s\"']*(?:"
    r"so|well|then|next|since|maybe|okay|alright|sure|let|i|they|tamam|"
    r"peki|öncelikle|oncelikle|ilk"
    r")\b",
    re.IGNORECASE,
)

_META_SELF_ACTION = re.compile(
    r"\b(?:i need to|i should|i will|i'?ll|i am going to|let me)\b",
    re.IGNORECASE,
)

_META_META_ACTION = re.compile(
    r"\b(?:respond|answer|format|structure|plan|thinking|make sure|follow|"
    r"offer|introduce|mention|say|greet|start|begin)\b",
    re.IGNORECASE,
)

_META_CONTEXT = re.compile(
    r"\b(?:the user|they|their|they said|they mentioned|since they|looking at|based on|"
    r"system message|guidelines)\b",
    re.IGNORECASE,
)


def _split_by_fences(text: str) -> List[Tuple[str, bool]]:
    """Giriş: Metin.

    Çıkış: (parça, kod_mu) listesi.
    İşleyiş: ``` ayraçlarıyla metni parçalar.
    """
    out: List[Tuple[str, bool]] = []
    fence = "```"
    idx = 0
    in_code = False

    while idx < len(text):
        next_idx = text.find(fence, idx)
        if next_idx == -1:
            out.append((text[idx:], in_code))
            break
        out.append((text[idx:next_idx], in_code))
        in_code = not in_code
        out.append((fence, in_code))
        idx = next_idx + len(fence)
    return out


def _strip_leading_meta_lines(text: str) -> str:
    """Giriş: Metin.

    Çıkış: Meta satırları temizlenmiş metin.
    İşleyiş: Baştaki meta satırlarını siler.
    """
    lines = text.replace("\r\n", "\n").split("\n")
    idx = 0
    removed = 0
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1

    while idx < len(lines) and removed < 6:
        line = lines[idx].strip()
        if line == "":
            idx += 1
            continue
        if not _META_LINE.match(line):
            break
        lines[idx] = ""
        idx += 1
        removed += 1
    return "\n".join(lines)


def _strip_leading_meta_sentences(text: str) -> str:
    """Giriş: Metin.

    Çıkış: Meta cümleleri temizlenmiş metin.
    İşleyiş: İlk meta cümlelerini ayıklar.
    """
    cleaned = text
    for _ in range(6):
        match = _META_SENTENCE.match(cleaned)
        if not match:
            break
        cleaned = cleaned[match.end() :].lstrip()
    return cleaned


def _fallback_message(language: str) -> str:
    """Giriş: Dil kodu.

    Çıkış: Varsayılan mesaj.
    İşleyiş: Dil seçimine göre metin döndürür.
    """
    if language.lower().startswith("en"):
        return "Hello! How can I help you with Selçuk University?"
    return "Merhaba! Selçuk Üniversitesi ile ilgili nasıl yardımcı olabilirim?"


def clean_text(text: str, language: str = "tr") -> str:
    """Giriş: Ham metin ve dil.

    Çıkış: Temizlenmiş metin.
    İşleyiş: Think/meta içeriklerini ayıklar.
    """
    if not text or not text.strip():
        return _fallback_message(language)

    parts = _split_by_fences(text)
    for idx, (segment, is_code) in enumerate(parts):
        if is_code:
            continue

        cleaned = re.sub(
            r"<think>[\s\S]*?</think>", "", segment, flags=re.IGNORECASE
        )
        cleaned = re.sub(r"<think>[\s\S]*$", "", cleaned, flags=re.IGNORECASE)
        cleaned = _strip_leading_meta_lines(cleaned)
        cleaned = _strip_leading_meta_sentences(cleaned)
        parts[idx] = (cleaned, is_code)

    rebuilt = "".join(part for part, _ in parts)
    rebuilt = re.sub(r"^\s+", "", rebuilt)
    if not rebuilt.strip():
        return _fallback_message(language)
    if _looks_meta(rebuilt):
        return _fallback_message(language)
    return rebuilt


def _strip_meta_sentence_from_buffer(buffer: str) -> tuple[str, bool]:
    """Giriş: Buffer metni.

    Çıkış: (yeni buffer, silindi_mi).
    İşleyiş: Meta cümlelerini çıkarır.
    """
    match = _META_SENTENCE.match(buffer)
    if match:
        return buffer[match.end() :].lstrip(), True

    sentence_end = re.search(r"[.!?](?:\s|$)", buffer)
    if not sentence_end:
        return buffer, False

    sentence = buffer[: sentence_end.end()]
    if _META_CONTEXT.search(sentence):
        return buffer[sentence_end.end() :].lstrip(), True
    if _META_SELF_ACTION.search(sentence) and _META_META_ACTION.search(sentence):
        return buffer[sentence_end.end() :].lstrip(), True

    return buffer, False


def _should_delay_emit(buffer: str) -> bool:
    """Giriş: Buffer metni.

    Çıkış: bool.
    İşleyiş: Kısa meta prefix'leri bekletir.
    """
    if len(buffer) < 32 and _META_PREFIX_FRAGMENT.match(buffer):
        if not re.search(r"[.!?]", buffer):
            return True
    return False


def _looks_meta(text: str) -> bool:
    """Giriş: Metin.

    Çıkış: bool.
    İşleyiş: Meta kalıpları tarar.
    """
    sample = text[:200]
    if _META_CONTEXT.search(sample):
        return True
    if _META_SELF_ACTION.search(sample) and _META_META_ACTION.search(sample):
        return True
    if _META_PREFIX.search(sample):
        return True
    return False


@dataclass
class StreamingResponseCleaner:
    """Giriş: Dil kodu.

    Çıkış: Temizlenmiş akış metni.
    İşleyiş: Meta ve <think> içeriklerini ayıklar.
    """

    language: str = "tr"
    _think_filter: ReasoningFilter = field(default_factory=ReasoningFilter)
    _pending: str = ""
    _emitting: bool = False

    def feed(self, chunk: str) -> str:
        """Giriş: Token parçası.

        Çıkış: Temiz metin.
        İşleyiş: Tamponlayıp filtre uygular.
        """
        filtered = self._think_filter.feed(chunk)
        if not filtered:
            return ""
        self._pending += filtered
        return self._flush_pending()

    def finalize(self) -> str:
        """Giriş: yok.

        Çıkış: Kalan metin.
        İşleyiş: Son temizleme adımını uygular.
        """
        if not self._pending:
            return ""
        if self._emitting:
            output = self._pending
        else:
            output = clean_text(self._pending, self.language)
        self._pending = ""
        return output

    def _flush_pending(self) -> str:
        """Giriş: yok.

        Çıkış: Yayımlanacak metin.
        İşleyiş: Meta koşullarına göre tamponu boşaltır.
        """
        if self._emitting:
            output = self._pending
            self._pending = ""
            return output

        if self._pending.lstrip().startswith("```"):
            self._emitting = True
            output = self._pending
            self._pending = ""
            return output

        while True:
            stripped, removed = _strip_meta_sentence_from_buffer(self._pending)
            if removed:
                self._pending = stripped
                if not self._pending:
                    return ""
                continue

            newline_idx = self._pending.find("\n")
            if newline_idx != -1:
                line = self._pending[: newline_idx + 1]
                if _META_LINE.match(line.strip()):
                    self._pending = self._pending[newline_idx + 1 :]
                    continue
                if _should_delay_emit(self._pending):
                    return ""
                if _META_PREFIX.match(self._pending):
                    return ""
                self._emitting = True
                output = self._pending
                self._pending = ""
                return output

            if _should_delay_emit(self._pending):
                return ""

            if _looks_meta(self._pending):
                return ""

            if (
                (_META_CONTEXT.search(self._pending) or (
                    _META_SELF_ACTION.search(self._pending)
                    and _META_META_ACTION.search(self._pending)
                ))
                and not re.search(r"[.!?]", self._pending)
            ):
                return ""

            if (
                len(self._pending) < 80
                and not re.search(r"[.!?\n]", self._pending)
            ):
                return ""

            if self._pending and not _META_PREFIX.match(self._pending):
                self._emitting = True
                output = self._pending
                self._pending = ""
                return output

            return ""
