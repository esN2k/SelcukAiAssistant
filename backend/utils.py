"""İstek işleme ve akışa yönelik yardımcı fonksiyonlar."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterable, Optional

from prompts import build_default_system_prompt
from schemas import ChatMessage


def pick_language(accept_language: Optional[str]) -> str:
    """Giriş: Accept-Language başlığı veya None.

    Çıkış: "tr" ya da "en".
    İşleyiş: Başlıktaki dil sırasına göre desteklenen ilk dili seçer.
    """
    if not accept_language:
        return "tr"
    for part in accept_language.split(","):
        lang = part.split(";", 1)[0].strip().lower()
        if lang.startswith("tr"):
            return "tr"
        if lang.startswith("en"):
            return "en"
    return "tr"


def build_default_system_message(language: str) -> ChatMessage:
    """Giriş: Dil kodu.

    Çıkış: Sistem rolünde ChatMessage.
    İşleyiş: Varsayılan sistem promptunu üretir.
    """
    return ChatMessage(
        role="system",
        content=build_default_system_prompt(language).strip(),
    )


def normalize_messages(
    messages: list[ChatMessage],
    language: str,
) -> list[ChatMessage]:
    """Giriş: Mesaj listesi ve dil kodu.

    Çıkış: Normalize edilmiş mesaj listesi.
    İşleyiş: Sistem mesajı yoksa ekler, içerikleri kopyalar.
    """
    normalized = [ChatMessage(role=m.role, content=m.content) for m in messages]
    if not any(m.role == "system" for m in normalized):
        normalized.insert(0, build_default_system_message(language))
    return normalized


def estimate_token_count(text: str) -> int:
    """Giriş: Metin.

    Çıkış: Yaklaşık token sayısı.
    İşleyiş: Basit uzunluk bölme yaklaşımı uygular.
    """
    if not text:
        return 0
    return max(1, len(text) // 4)


def estimate_messages_tokens(messages: Iterable[ChatMessage]) -> int:
    """Giriş: Mesaj listesi.

    Çıkış: Toplam token tahmini.
    İşleyiş: Her mesajın token tahminini toplar.
    """
    return sum(estimate_token_count(m.content) for m in messages)


def clamp_max_tokens(requested: int, max_allowed: int) -> int:
    """Giriş: İstenen ve izin verilen üst sınır.

    Çıkış: Sınırlandırılmış token sayısı.
    İşleyiş: Değeri 1 ile üst sınır arasında tutar.
    """
    return max(1, min(requested, max_allowed))


def trim_messages_for_context(
    messages: list[ChatMessage],
    max_tokens: int,
) -> list[ChatMessage]:
    """Giriş: Mesaj listesi ve bağlam limiti.

    Çıkış: Budanmış mesaj listesi.
    İşleyiş: Token limiti aşıldıkça en eski mesajları çıkarır.
    """
    trimmed = list(messages)
    while estimate_messages_tokens(trimmed) > max_tokens and len(trimmed) > 1:
        if trimmed[0].role == "system" and len(trimmed) > 1:
            trimmed.pop(1)
        else:
            trimmed.pop(0)
    return trimmed


def sse_event(payload: dict[str, object]) -> str:
    """Giriş: JSON'a dönüştürülebilir sözlük.

    Çıkış: SSE formatlı veri satırı.
    İşleyiş: JSON'u `data:` satırı olarak paketler.
    """
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


@dataclass
class ReasoningFilter:
    """Giriş: Akış metni parçaları.

    Çıkış: <think> blokları ayıklanmış metin.
    İşleyiş: <think> ... </think> aralıklarını filtreler.
    """

    inside_think: bool = False
    buffer: str = ""

    def feed(self, chunk: str) -> str:
        """Giriş: Yeni metin parçası.

        Çıkış: Ayıklanmış metin parçası.
        İşleyiş: Tamponu günceller, <think> bloklarını çıkarır.
        """
        self.buffer += chunk
        output_parts: list[str] = []

        while self.buffer:
            if self.inside_think:
                end_idx = self.buffer.find("</think>")
                if end_idx == -1:
                    # Keep a small tail for tag detection
                    self.buffer = self.buffer[-16:]
                    return "".join(output_parts)
                self.buffer = self.buffer[end_idx + len("</think>") :]
                self.inside_think = False
                continue

            start_idx = self.buffer.find("<think>")
            if start_idx == -1:
                output_parts.append(self.buffer)
                self.buffer = ""
                break

            if start_idx > 0:
                output_parts.append(self.buffer[:start_idx])
            self.buffer = self.buffer[start_idx + len("<think>") :]
            self.inside_think = True

        return "".join(output_parts)
