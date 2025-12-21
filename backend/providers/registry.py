"""Model registry and routing."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from config import Config
from providers.base import ModelInfo, ModelProvider


@dataclass
class ResolvedModel:
    alias: str
    provider: str
    model_id: str
    display_name: str


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


class ModelRegistry:
    def __init__(self, providers: Dict[str, ModelProvider]) -> None:
        self.providers = providers
        self.aliases = parse_aliases(Config.MODEL_ALIASES)
        self.default_provider = Config.MODEL_BACKEND
        self.default_model_id = _default_model_id(self.default_provider)

    def resolve(self, model_name: Optional[str]) -> ResolvedModel:
        if model_name:
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

        return ResolvedModel(
            alias="default",
            provider=self.default_provider,
            model_id=self.default_model_id,
            display_name=_display_name("default", self.default_model_id),
        )

    def list_models(self) -> list[ModelInfo]:
        models: list[ModelInfo] = []
        default_alias = "default"
        default_model = self.resolve(None)

        # Alias entries
        for alias, resolved in self.aliases.items():
            if resolved.provider not in self.providers:
                continue
            models.append(
                ModelInfo(
                    id=alias,
                    provider=resolved.provider,
                    model_id=resolved.model_id,
                    display_name=resolved.display_name,
                    is_default=alias == default_alias,
                )
            )

        # Always include default model
        if default_model.provider in self.providers:
            models.append(
                ModelInfo(
                    id=default_alias,
                    provider=default_model.provider,
                    model_id=default_model.model_id,
                    display_name=default_model.display_name,
                    is_default=True,
                )
            )

        return models
