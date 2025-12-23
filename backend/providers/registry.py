"""Model registry and routing."""
from __future__ import annotations

from dataclasses import dataclass, field
import importlib.util
import os
from pathlib import Path
from typing import Dict, Optional

from config import Config
from ollama_service import OllamaService
from providers.base import ModelInfo, ModelProvider


@dataclass
class ResolvedModel:
    alias: str
    provider: str
    model_id: str
    display_name: str


@dataclass
class CatalogEntry:
    id: str
    provider: str
    model_id: str
    display_name: str
    local_or_remote: str
    requires_api_key: bool
    context_length: Optional[int] = None
    tags: list[str] = field(default_factory=list)
    notes: str = ""


_REMOTE_API_KEYS = {
    "openai": ["OPENAI_API_KEY"],
    "anthropic": ["ANTHROPIC_API_KEY"],
    "google": ["GOOGLE_API_KEY", "GEMINI_API_KEY"],
    "xai": ["XAI_API_KEY"],
}


def _default_model_id(provider: str) -> str:
    if provider == "huggingface":
        return Config.HF_MODEL_NAME
    return Config.OLLAMA_MODEL


def _display_name(alias: str, model_id: str) -> str:
    if alias:
        return alias.replace("_", " ").title()
    return model_id


def parse_aliases(raw: str) -> Dict[str, ResolvedModel]:
    aliases: Dict[str, ResolvedModel] = {}
    if not raw:
        return aliases
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        if "=" not in item or ":" not in item:
            continue
        alias, target = item.split("=", 1)
        provider, model_id = target.split(":", 1)
        provider = provider.strip().lower()
        model_id = model_id.strip()
        alias = alias.strip()
        if not alias or not provider or not model_id:
            continue
        aliases[alias] = ResolvedModel(
            alias=alias,
            provider=provider,
            model_id=model_id,
            display_name=_display_name(alias, model_id),
        )
    return aliases


def _catalog_entries() -> list[CatalogEntry]:
    max_context = Config.MAX_CONTEXT_TOKENS
    return [
        CatalogEntry(
            id="selcuk_ai_assistant",
            provider="ollama",
            model_id="selcuk_ai_assistant",
            display_name="Selcuk AI Assistant (Local)",
            local_or_remote="local",
            requires_api_key=False,
            context_length=max_context,
            tags=["turkish", "high_quality"],
            notes="Local Ollama model tuned for Selcuk University.",
        ),
        CatalogEntry(
            id="llama3.1",
            provider="ollama",
            model_id="llama3.1",
            display_name="Llama 3.1",
            local_or_remote="local",
            requires_api_key=False,
            context_length=max_context,
            tags=["high_quality", "reasoning"],
            notes="Open weights via Ollama.",
        ),
        CatalogEntry(
            id="selcuk-assistant",
            provider="ollama",
            model_id="selcuk-assistant",
            display_name="Selcuk Assistant",
            local_or_remote="local",
            requires_api_key=False,
            context_length=max_context,
            tags=["turkish"],
            notes="Local Ollama variant.",
        ),
        CatalogEntry(
            id="mistral",
            provider="ollama",
            model_id="mistral",
            display_name="Mistral",
            local_or_remote="local",
            requires_api_key=False,
            context_length=max_context,
            tags=["fast"],
            notes="Lightweight local model.",
        ),
        CatalogEntry(
            id="gemma2:2b",
            provider="ollama",
            model_id="gemma2:2b",
            display_name="Gemma 2 2B",
            local_or_remote="local",
            requires_api_key=False,
            context_length=max_context,
            tags=["fast"],
            notes="Small open-weights model.",
        ),
        CatalogEntry(
            id="qwen2.5:7b",
            provider="ollama",
            model_id="qwen2.5:7b",
            display_name="Qwen 2.5 7B",
            local_or_remote="local",
            requires_api_key=False,
            context_length=max_context,
            tags=["reasoning"],
            notes="Verify exact Ollama tag before installing.",
        ),
        CatalogEntry(
            id="llama3.2:3b",
            provider="ollama",
            model_id="llama3.2:3b",
            display_name="Llama 3.2 3B",
            local_or_remote="local",
            requires_api_key=False,
            context_length=max_context,
            tags=["fast", "small"],
            notes="Small Ollama model suited for 6GB GPUs.",
        ),
        CatalogEntry(
            id="phi3:mini",
            provider="ollama",
            model_id="phi3:mini",
            display_name="Phi-3 Mini",
            local_or_remote="local",
            requires_api_key=False,
            context_length=max_context,
            tags=["fast", "microsoft"],
            notes="Compact model with strong instruction tuning.",
        ),
        CatalogEntry(
            id="deepseek-r1:8b",
            provider="ollama",
            model_id="deepseek-r1:8b",
            display_name="DeepSeek R1 8B",
            local_or_remote="local",
            requires_api_key=False,
            context_length=max_context,
            tags=["reasoning"],
            notes="Heavier local model; consider 4-bit quantization.",
        ),
        CatalogEntry(
            id="aya:8b",
            provider="ollama",
            model_id="aya:8b",
            display_name="Aya 8B",
            local_or_remote="local",
            requires_api_key=False,
            context_length=max_context,
            tags=["multilingual", "turkish"],
            notes="Multilingual model with strong Turkish coverage.",
        ),
        CatalogEntry(
            id="hf_qwen2_5_1_5b",
            provider="huggingface",
            model_id="Qwen/Qwen2.5-1.5B-Instruct",
            display_name="Qwen 2.5 1.5B Instruct (HF)",
            local_or_remote="local",
            requires_api_key=False,
            context_length=max_context,
            tags=["fast"],
            notes="Requires backend/requirements-hf.txt and cached weights.",
        ),
        CatalogEntry(
            id="hf_phi3_mini",
            provider="huggingface",
            model_id="microsoft/Phi-3-mini-4k-instruct",
            display_name="Phi-3 Mini 4k (HF)",
            local_or_remote="local",
            requires_api_key=False,
            context_length=max_context,
            tags=["fast"],
            notes="Requires backend/requirements-hf.txt and cached weights.",
        ),
        CatalogEntry(
            id="hf_qwen2_5_3b",
            provider="huggingface",
            model_id="Qwen/Qwen2.5-3B-Instruct",
            display_name="Qwen 2.5 3B Instruct (HF)",
            local_or_remote="local",
            requires_api_key=False,
            context_length=max_context,
            tags=["balanced", "multilingual"],
            notes="4-bit recommended for 6GB GPUs.",
        ),
        CatalogEntry(
            id="hf_tinyllama_1_1b",
            provider="huggingface",
            model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            display_name="TinyLlama 1.1B Chat (HF)",
            local_or_remote="local",
            requires_api_key=False,
            context_length=max_context,
            tags=["tiny", "fast"],
            notes="Very small model for quick iterations.",
        ),
        CatalogEntry(
            id="gpt-4o",
            provider="openai",
            model_id="gpt-4o",
            display_name="GPT-4o",
            local_or_remote="remote",
            requires_api_key=True,
            context_length=max_context,
            tags=["high_quality"],
            notes="Remote API model. Verify model name for your OpenAI account.",
        ),
        CatalogEntry(
            id="gpt-4o-mini",
            provider="openai",
            model_id="gpt-4o-mini",
            display_name="GPT-4o Mini",
            local_or_remote="remote",
            requires_api_key=True,
            context_length=max_context,
            tags=["fast"],
            notes="Remote API model. Verify model name for your OpenAI account.",
        ),
        CatalogEntry(
            id="claude-3-5-sonnet",
            provider="anthropic",
            model_id="claude-3-5-sonnet",
            display_name="Claude 3.5 Sonnet",
            local_or_remote="remote",
            requires_api_key=True,
            context_length=max_context,
            tags=["high_quality"],
            notes="Remote API model. Verify model name for your Anthropic account.",
        ),
        CatalogEntry(
            id="gemini-1.5-pro",
            provider="google",
            model_id="gemini-1.5-pro",
            display_name="Gemini 1.5 Pro",
            local_or_remote="remote",
            requires_api_key=True,
            context_length=max_context,
            tags=["high_quality"],
            notes="Remote API model. Verify model name for your Google AI account.",
        ),
        CatalogEntry(
            id="grok-2",
            provider="xai",
            model_id="grok-2",
            display_name="Grok 2",
            local_or_remote="remote",
            requires_api_key=True,
            context_length=max_context,
            tags=["high_quality"],
            notes="Remote API model. Verify model name for your xAI account.",
        ),
    ]


def _has_hf_dependencies() -> bool:
    return (
        importlib.util.find_spec("transformers") is not None
        and importlib.util.find_spec("torch") is not None
    )


def _hf_cache_roots() -> list[Path]:
    roots: list[Path] = []
    for env_var in ("HUGGINGFACE_HUB_CACHE", "TRANSFORMERS_CACHE"):
        value = os.getenv(env_var)
        if value:
            roots.append(Path(value))
    hf_home = os.getenv("HF_HOME")
    if hf_home:
        roots.append(Path(hf_home) / "hub")
    roots.append(Path.home() / ".cache" / "huggingface" / "hub")
    return roots


def _hf_model_cached(model_id: str) -> bool:
    model_dir = model_id.replace("/", "--")
    for root in _hf_cache_roots():
        if (root / f"models--{model_dir}").exists():
            return True
    return False


def _api_key_status(provider: str) -> tuple[bool, list[str]]:
    keys = _REMOTE_API_KEYS.get(provider, [])
    if not keys:
        return False, []
    present = any(os.getenv(key) for key in keys)
    return present, keys


class ModelRegistry:
    def __init__(self, providers: Dict[str, ModelProvider]) -> None:
        self.providers = providers
        self.aliases = parse_aliases(Config.MODEL_ALIASES)
        self.default_provider = Config.MODEL_BACKEND
        self.default_model_id = _default_model_id(self.default_provider)
        self.catalog = _catalog_entries()
        self.catalog_by_id = {entry.id: entry for entry in self.catalog}

    def resolve(self, model_name: Optional[str]) -> ResolvedModel:
        if model_name:
            entry = self.catalog_by_id.get(model_name)
            if entry:
                return ResolvedModel(
                    alias=entry.id,
                    provider=entry.provider,
                    model_id=entry.model_id,
                    display_name=entry.display_name,
                )

            if model_name in self.aliases:
                return self.aliases[model_name]

            if ":" in model_name:
                provider, model_id = model_name.split(":", 1)
                provider = provider.strip().lower()
                if provider in self.providers:
                    return ResolvedModel(
                        alias=model_name,
                        provider=provider,
                        model_id=model_id.strip(),
                        display_name=_display_name(model_name, model_id),
                    )

            provider = self.default_provider
            return ResolvedModel(
                alias=model_name,
                provider=provider,
                model_id=model_name,
                display_name=_display_name(model_name, model_name),
            )

        default_entry = next(
            (
                entry
                for entry in self.catalog
                if entry.provider == self.default_provider
                and entry.model_id == self.default_model_id
            ),
            None,
        )
        if default_entry:
            return ResolvedModel(
                alias=default_entry.id,
                provider=default_entry.provider,
                model_id=default_entry.model_id,
                display_name=default_entry.display_name,
            )

        return ResolvedModel(
            alias="default",
            provider=self.default_provider,
            model_id=self.default_model_id,
            display_name=_display_name("default", self.default_model_id),
        )

    async def list_models(self) -> list[ModelInfo]:
        ollama_models: list[str] = []
        if any(entry.provider == "ollama" for entry in self.catalog):
            ollama_models = await OllamaService().list_model_names()

        hf_deps = _has_hf_dependencies()
        models: list[ModelInfo] = []

        for entry in self.catalog:
            available = False
            reason = ""

            if entry.local_or_remote == "local":
                if entry.provider == "ollama":
                    if ollama_models and OllamaService._is_model_available(
                        entry.model_id, ollama_models
                    ):
                        available = True
                    elif not ollama_models:
                        reason = "Ollama not reachable or no models installed."
                    else:
                        reason = f"Not installed. Run: ollama pull {entry.model_id}"
                elif entry.provider == "huggingface":
                    if not hf_deps:
                        reason = "HuggingFace deps missing. Install backend/requirements-hf.txt."
                    elif not _hf_model_cached(entry.model_id):
                        reason = "Model not cached. Download from HuggingFace Hub."
                    else:
                        available = True
                else:
                    reason = "Provider not configured on server."
            else:
                key_present, keys = _api_key_status(entry.provider)
                if not key_present:
                    key_list = ", ".join(keys) if keys else "API key"
                    reason = f"Missing API key: {key_list}"
                elif entry.provider not in self.providers:
                    reason = "Provider not configured on server."
                else:
                    available = True

            is_default = (
                entry.provider == self.default_provider
                and entry.model_id == self.default_model_id
            )

            models.append(
                ModelInfo(
                    id=entry.id,
                    provider=entry.provider,
                    model_id=entry.model_id,
                    display_name=entry.display_name,
                    local_or_remote=entry.local_or_remote,
                    requires_api_key=entry.requires_api_key,
                    available=available,
                    reason_unavailable=reason,
                    context_length=entry.context_length,
                    tags=list(entry.tags),
                    notes=entry.notes,
                    is_default=is_default,
                )
            )

        return models
