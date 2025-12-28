"""Sohbet endpoint'leri için Pydantic şemaları."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class ChatMessage(BaseModel):
    """Giriş: rol ve içerik alanları.

    Çıkış: Doğrulanmış ChatMessage.
    İşleyiş: Rol ve içerik alanlarını normalize eder.
    """

    role: str = Field(..., description="system, user veya assistant")
    content: str = Field(..., min_length=1, max_length=10000)

    @field_validator("role")
    @classmethod
    def normalize_role(cls, value: str) -> str:
        """Giriş: Rol değeri.

        Çıkış: Normalize edilmiş rol.
        İşleyiş: Rolü küçük harfe çevirir ve doğrular.
        """
        role = value.strip().lower()
        if role not in {"system", "user", "assistant"}:
            raise ValueError("role yalnızca system, user veya assistant olabilir")
        return role

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        """Giriş: İçerik değeri.

        Çıkış: Temizlenmiş içerik.
        İşleyiş: Boşlukları temizler ve temel XSS kontrolü yapar.
        """
        text = value.strip()
        if not text:
            raise ValueError("content boş olamaz")

        lowered = text.lower()
        for pattern in ("<script", "</script", "javascript:", "onerror=", "onload="):
            if pattern in lowered:
                raise ValueError("content yasaklı bir ifade içeriyor")
        return text


class ChatRequest(BaseModel):
    """Giriş: /chat ve /chat/stream istek alanları.

    Çıkış: Doğrulanmış istek.
    İşleyiş: Mesaj listesi ve RAG ayarlarını içerir.
    """

    model: Optional[str] = Field(
        default=None,
        description="Model aliası veya provider:model_id",
        examples=["ollama_default", "huggingface:Qwen/Qwen2.5-1.5B-Instruct"],
    )
    messages: list[ChatMessage] = Field(
        ...,
        min_length=1,
        description="Sohbet mesajları listesi",
    )
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    max_tokens: int = Field(default=256, ge=1, le=8192)
    stream: bool = Field(default=False)
    rag_enabled: bool = Field(default=False, description="RAG bağlamını etkinleştir")
    rag_strict: Optional[bool] = Field(
        default=None, description="Sıkı RAG modu (sunucu varsayılanını ezer)"
    )
    rag_top_k: Optional[int] = Field(
        default=None,
        ge=1,
        le=20,
        description="Getirilecek RAG parça sayısı",
    )

    @model_validator(mode="after")
    def ensure_user_message(self) -> "ChatRequest":
        """Giriş: ChatRequest örneği.

        Çıkış: Doğrulanmış ChatRequest.
        İşleyiş: En az bir user mesajı olduğunu doğrular.
        """
        has_user = any(message.role == "user" for message in self.messages)
        if not has_user:
            raise ValueError("messages içinde en az bir user mesajı olmalı")
        return self


class UsageInfo(BaseModel):
    """Giriş: Token kullanım bilgisi alanları.

    Çıkış: Doğrulanmış UsageInfo.
    İşleyiş: Kullanım metriklerini taşır.
    """

    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class ChatResponse(BaseModel):
    """Giriş: Yanıt alanları.

    Çıkış: Doğrulanmış ChatResponse.
    İşleyiş: Yanıt metni ve metadata'yı taşır.
    """

    answer: str
    request_id: str
    provider: str
    model: str
    usage: Optional[UsageInfo] = None
    citations: Optional[list[str]] = None
