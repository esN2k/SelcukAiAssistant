"""Ollama service client for SelcukAiAssistant Backend (Async)."""
import asyncio
import json
import logging
from typing import Any, AsyncIterator, Dict, List, Optional

import httpx
from fastapi import HTTPException

from config import Config

logger = logging.getLogger(__name__)


class OllamaService:
    """Service class for interacting with Ollama API asynchronously."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> None:
        self.base_url = base_url or Config.OLLAMA_BASE_URL
        self.timeout = timeout or Config.OLLAMA_TIMEOUT
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.api_url = f"{self.base_url}/api/chat"

        logger.info(
            "Initialized Ollama service: url=%s timeout=%ss max_retries=%s",
            self.api_url,
            self.timeout,
            self.max_retries,
        )

    @staticmethod
    def _validate_messages(messages: List[Dict[str, str]]) -> None:
        if not messages:
            raise HTTPException(status_code=400, detail="messages cannot be empty")

    @staticmethod
    def _clean_reasoning_artifacts(text: str) -> str:
        import re

        if not text or not text.strip():
            return "Merhaba! Ben Selcuk AI Asistani. Size nasil yardimci olabilirim?"

        original_text = text

        text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = text.replace("<|im_end|>", "").replace("<|im_start|>", "")
        text = text.replace("<|end|>", "").replace("<|start|>", "")

        reasoning_patterns = [
            r"^[^.!?\n]*\b(okay|alright|let me|let me think|hmm|wait)\b[^.!?\n]*[\n.]",
            r"^[^.!?\n]*\b(tamam|peki|dusunelim|bakalim|bir dakika)\b[^.!?\n]*[\n.]",
        ]
        for pattern in reasoning_patterns:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.MULTILINE)

        merhaba_matches = list(re.finditer(r"\bMerhaba[!.,]?", text, re.IGNORECASE))
        if merhaba_matches:
            text = text[merhaba_matches[-1].start() :]
        elif re.search(r"^##\s", text, re.MULTILINE):
            header_match = re.search(r"^##\s", text, re.MULTILINE)
            if header_match:
                text = text[header_match.start() :]

        text = re.sub(r"\n{3,}", "\n\n", text).strip()

        if len(text) < 15:
            if len(original_text.strip()) > 20 and "<think>" not in original_text.lower():
                return original_text.strip()
            return "Merhaba! Ben Selcuk AI Asistani. Size nasil yardimci olabilirim?"

        return text

    async def generate(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float,
        top_p: float,
        max_tokens: int,
    ) -> Dict[str, Any]:
        self._validate_messages(messages)

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for attempt in range(self.max_retries):
                try:
                    payload = {
                        "model": model,
                        "messages": messages,
                        "stream": False,
                        "options": {
                            "temperature": temperature,
                            "top_p": top_p,
                            "top_k": 40,
                            "repeat_penalty": 1.1,
                            "num_predict": max_tokens,
                        },
                    }

                    response = await client.post(
                        self.api_url,
                        json=payload,
                        headers={"Content-Type": "application/json; charset=utf-8"},
                    )
                    response.encoding = "utf-8"

                    if response.status_code != 200:
                        error_detail = self._parse_error_response(response)
                        raise HTTPException(
                            status_code=response.status_code,
                            detail=f"Ollama API error: {error_detail}",
                        )

                    data = response.json()
                    message = data.get("message") or {}
                    answer = message.get("content", "")
                    if not answer:
                        return {
                            "text": "Uzgunnm, bir yanit olusturulamadi.",
                            "usage": None,
                        }

                    cleaned = self._clean_reasoning_artifacts(answer)
                    usage = {
                        "prompt_tokens": data.get("prompt_eval_count"),
                        "completion_tokens": data.get("eval_count"),
                    }
                    return {"text": cleaned, "usage": usage}

                except httpx.ReadTimeout:
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(self.retry_delay * (attempt + 1))
                        continue
                    raise HTTPException(
                        status_code=504,
                        detail="Ollama request timed out.",
                    )
                except httpx.RequestError as exc:
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(self.retry_delay * (attempt + 1))
                        continue
                    raise HTTPException(
                        status_code=503,
                        detail=f"Cannot connect to Ollama: {exc}",
                    )

        raise HTTPException(status_code=500, detail="Ollama error")

    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float,
        top_p: float,
        max_tokens: int,
    ) -> AsyncIterator[Dict[str, Any]]:
        self._validate_messages(messages)

        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": 40,
                "repeat_penalty": 1.1,
                "num_predict": max_tokens,
            },
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            async with client.stream(
                "POST",
                self.api_url,
                json=payload,
                headers={"Content-Type": "application/json; charset=utf-8"},
            ) as response:
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Ollama API error: HTTP {response.status_code}",
                    )

                async for line in response.aiter_lines():
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    message = data.get("message") or {}
                    token = message.get("content", "")
                    done = bool(data.get("done", False))
                    usage = None
                    if done:
                        usage = {
                            "prompt_tokens": data.get("prompt_eval_count"),
                            "completion_tokens": data.get("eval_count"),
                        }
                    yield {"token": token, "done": done, "usage": usage}

    async def health_check(self, model: Optional[str] = None) -> Dict[str, Any]:
        model = model or Config.OLLAMA_MODEL
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")

                if response.status_code == 200:
                    models = response.json().get("models", [])
                    model_names = [m.get("name") for m in models]
                    model_available = self._is_model_available(model, model_names)
                    return {
                        "status": "healthy" if model_available else "degraded",
                        "ollama_url": self.base_url,
                        "model": model,
                        "model_available": model_available,
                        "available_models": model_names,
                    }
                return {
                    "status": "unhealthy",
                    "ollama_url": self.base_url,
                    "model": model,
                    "error": f"HTTP {response.status_code}",
                }
        except httpx.RequestError:
            return {
                "status": "unhealthy",
                "ollama_url": self.base_url,
                "model": model,
                "error": "Connection failed",
            }

    @staticmethod
    def _is_model_available(target_model: str, available_models: List[str]) -> bool:
        if not target_model or not available_models:
            return False
        if target_model in available_models:
            return True
        target_base = target_model.split(":")[0]
        for model in available_models:
            if target_base == model.split(":")[0]:
                return True
        return False

    @staticmethod
    def _parse_error_response(response: httpx.Response) -> str:
        try:
            error_data = response.json()
            return error_data.get("error", response.text)
        except (ValueError, KeyError, AttributeError):
            return response.text or f"HTTP {response.status_code}"
