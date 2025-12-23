"""Pydantic request/response schemas for chat endpoints."""
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class ChatMessage(BaseModel):
    """Single chat message with role and content."""

    role: str = Field(..., description="system, user, or assistant")
    content: str = Field(..., min_length=1, max_length=10000)

    @field_validator("role")
    @classmethod
    def normalize_role(cls, value: str) -> str:
        role = value.strip().lower()
        if role not in {"system", "user", "assistant"}:
            raise ValueError("role must be one of: system, user, assistant")
        return role

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        text = value.strip()
        if not text:
            raise ValueError("content must not be empty")

        # Basic XSS prevention
        lowered = text.lower()
        for pattern in ("<script", "</script", "javascript:", "onerror=", "onload="):
            if pattern in lowered:
                raise ValueError("content contains a forbidden pattern")
        return text


class ChatRequest(BaseModel):
    """Chat request schema used by /chat and /chat/stream."""

    model: Optional[str] = Field(
        default=None,
        description="Model alias or provider:model_id",
        examples=["ollama_default", "huggingface:Qwen/Qwen2.5-1.5B-Instruct"],
    )
    messages: List[ChatMessage] = Field(
        ...,
        min_length=1,
        description="Ordered list of chat messages",
    )
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    max_tokens: int = Field(default=256, ge=1, le=8192)
    stream: bool = Field(default=False)
    rag_enabled: bool = Field(default=False, description="Enable RAG context")
    rag_strict: Optional[bool] = Field(
        default=None, description="Strict RAG mode (override server default)"
    )
    rag_top_k: Optional[int] = Field(
        default=None,
        ge=1,
        le=20,
        description="Number of RAG chunks to retrieve",
    )

    @model_validator(mode="after")
    def ensure_user_message(self) -> "ChatRequest":
        has_user = any(message.role == "user" for message in self.messages)
        if not has_user:
            raise ValueError("messages must include at least one user message")
        return self


class UsageInfo(BaseModel):
    """Token usage info (best-effort)."""

    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class ChatResponse(BaseModel):
    """Non-streaming chat response."""

    answer: str
    request_id: str
    provider: str
    model: str
    usage: Optional[UsageInfo] = None
    citations: Optional[List[str]] = None
