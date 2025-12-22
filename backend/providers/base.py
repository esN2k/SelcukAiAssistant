"""Provider interface and shared dataclasses."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import AsyncIterator, Optional, Protocol


@dataclass
class Usage:
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


@dataclass
class ChatResult:
    text: str
    usage: Optional[Usage] = None


@dataclass
class StreamChunk:
    token: str
    done: bool = False
    usage: Optional[Usage] = None


@dataclass
class ModelInfo:
    id: str
    provider: str
    model_id: str
    display_name: str
    local_or_remote: str
    requires_api_key: bool
    available: bool
    reason_unavailable: str = ""
    context_length: Optional[int] = None
    tags: list[str] = field(default_factory=list)
    notes: str = ""
    is_default: bool = False


class CancellationToken:
    """Thread-safe cancellation token."""

    def __init__(self) -> None:
        import threading

        self._event = threading.Event()

    def cancel(self) -> None:
        self._event.set()

    def is_cancelled(self) -> bool:
        return self._event.is_set()


class ModelProvider(Protocol):
    name: str

    async def generate(
        self,
        messages: list[dict[str, str]],
        model_id: str,
        temperature: float,
        top_p: float,
        max_tokens: int,
        request_id: str,
    ) -> ChatResult:
        ...

    def stream(
        self,
        messages: list[dict[str, str]],
        model_id: str,
        temperature: float,
        top_p: float,
        max_tokens: int,
        request_id: str,
        cancel_token: CancellationToken,
    ) -> AsyncIterator[StreamChunk]:
        ...

    def list_models(self) -> list[ModelInfo]:
        ...
