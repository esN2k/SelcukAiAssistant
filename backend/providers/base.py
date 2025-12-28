"""Model sağlayıcı arayüzü ve ortak veri sınıfları."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import AsyncIterator, Optional, Protocol


@dataclass
class Usage:
    """Giriş: Token kullanım alanları.

    Çıkış: Kullanım bilgisi nesnesi.
    İşleyiş: Prompt/cevap token metriklerini taşır.
    """

    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


@dataclass
class ChatResult:
    """Giriş: Yanıt metni ve kullanım bilgisi.

    Çıkış: ChatResult nesnesi.
    İşleyiş: Tek seferlik yanıt sonucunu taşır.
    """

    text: str
    usage: Optional[Usage] = None


@dataclass
class StreamChunk:
    """Giriş: Akış tokenı ve tamamlanma durumu.

    Çıkış: StreamChunk nesnesi.
    İşleyiş: Akışlı yanıt parçasını taşır.
    """

    token: str
    done: bool = False
    usage: Optional[Usage] = None


@dataclass
class ModelInfo:
    """Giriş: Model meta alanları.

    Çıkış: ModelInfo nesnesi.
    İşleyiş: UI tarafına gidecek metadata'yı taşır.
    """

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
    """Giriş: yok.

    Çıkış: İptal kontrolü sağlayan nesne.
    İşleyiş: Thread-safe iptal sinyali taşır.
    """

    def __init__(self) -> None:
        """Giriş: yok.

        Çıkış: Nesne.
        İşleyiş: Event tabanlı iptal işaretini hazırlar.
        """
        import threading

        self._event = threading.Event()

    def cancel(self) -> None:
        """Giriş: yok.

        Çıkış: yok.
        İşleyiş: İptal sinyalini aktif eder.
        """
        self._event.set()

    def is_cancelled(self) -> bool:
        """Giriş: yok.

        Çıkış: bool.
        İşleyiş: İptal sinyalinin aktif olup olmadığını döndürür.
        """
        return self._event.is_set()


class ModelProvider(Protocol):
    """Giriş: Model sağlayıcı kuralları.

    Çıkış: Uygulayan sınıflar için sözleşme.
    İşleyiş: generate/stream ve list_models yöntemlerini zorunlu kılar.
    """

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
