"""Shared utilities for request processing and streaming."""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from prompts import build_default_system_prompt
from schemas import ChatMessage

logger = logging.getLogger(__name__)


def pick_language(accept_language: Optional[str]) -> str:
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
    return ChatMessage(
        role="system",
        content=build_default_system_prompt(language).strip(),
    )


def normalize_messages(messages: List[ChatMessage], language: str) -> List[ChatMessage]:
    """Ensure a system message exists and strip empty content."""
    normalized = [ChatMessage(role=m.role, content=m.content) for m in messages]
    if not any(m.role == "system" for m in normalized):
        normalized.insert(0, build_default_system_message(language))
    return normalized


def messages_to_dict(messages: Iterable[ChatMessage]) -> List[Dict[str, str]]:
    return [{"role": m.role, "content": m.content} for m in messages]


def estimate_token_count(text: str) -> int:
    """Rough token estimate without tokenizer (chars/4 heuristic)."""
    if not text:
        return 0
    return max(1, len(text) // 4)


def estimate_messages_tokens(messages: Iterable[ChatMessage]) -> int:
    return sum(estimate_token_count(m.content) for m in messages)


def clamp_max_tokens(requested: int, max_allowed: int) -> int:
    return max(1, min(requested, max_allowed))


def trim_messages_for_context(
    messages: List[ChatMessage], max_tokens: int
) -> List[ChatMessage]:
    trimmed = list(messages)
    while estimate_messages_tokens(trimmed) > max_tokens and len(trimmed) > 1:
        if trimmed[0].role == "system" and len(trimmed) > 1:
            trimmed.pop(1)
        else:
            trimmed.pop(0)
    return trimmed


def sse_event(payload: Dict[str, object]) -> str:
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


@dataclass
class ReasoningFilter:
    """Filters out <think> blocks from streaming text."""

    inside_think: bool = False
    buffer: str = ""

    def feed(self, chunk: str) -> str:
        self.buffer += chunk
        output_parts: List[str] = []

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
