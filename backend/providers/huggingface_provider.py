"""Hugging Face Transformers provider with optional 4-bit loading."""
from __future__ import annotations

import logging
from typing import Any, AsyncIterator, Dict, List, Optional, Tuple, cast

from config import Config
from providers.base import CancellationToken, ChatResult, ModelProvider, StreamChunk, Usage
from utils import ReasoningFilter

logger = logging.getLogger(__name__)


class HuggingFaceProvider(ModelProvider):
    name = "huggingface"

    def __init__(self) -> None:
        self._cache: Dict[str, Tuple[Any, Any, str]] = {}

    def _ensure_dependencies(self) -> None:
        try:
            import torch  # noqa: F401
            import transformers  # noqa: F401
        except ImportError as exc:
            raise RuntimeError(
                "HuggingFace dependencies missing. Install backend/requirements-hf.txt"
            ) from exc

    @staticmethod
    def _pick_device(preferred: str) -> str:
        import torch

        if preferred == "auto":
            if torch.cuda.is_available():
                return "cuda"
            if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
                return "mps"
            return "cpu"
        return preferred

    @staticmethod
    def _pick_dtype(name: str, device: str):
        import torch

        if name == "float16":
            return torch.float16
        if name == "bfloat16":
            return torch.bfloat16
        if name == "float32":
            return torch.float32
        if device == "cuda":
            return torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        return torch.float32

    def _load_model(self, model_id: str):
        self._ensure_dependencies()
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

        device = self._pick_device(Config.HF_DEVICE)
        dtype = self._pick_dtype(Config.HF_DTYPE, device)

        quant_config = None
        if Config.HF_LOAD_IN_4BIT and device == "cuda":
            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=dtype,
            )
        elif Config.HF_LOAD_IN_4BIT:
            logger.warning("HF_LOAD_IN_4BIT ignored on non-CUDA device")

        tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
        if tokenizer.pad_token is None and tokenizer.eos_token is not None:
            tokenizer.pad_token = tokenizer.eos_token

        kwargs = {
            "torch_dtype": dtype,
        }
        if quant_config is not None:
            kwargs["quantization_config"] = quant_config
        if device == "cuda":
            kwargs["device_map"] = "auto"

        if Config.HF_ATTENTION_IMPL:
            kwargs["attn_implementation"] = Config.HF_ATTENTION_IMPL

        try:
            model = AutoModelForCausalLM.from_pretrained(model_id, **kwargs)
        except TypeError:
            kwargs.pop("attn_implementation", None)
            model = AutoModelForCausalLM.from_pretrained(model_id, **kwargs)

        model = cast(Any, model)
        if device != "cuda":
            model.to(torch.device(device))

        model.eval()
        self._cache[model_id] = (model, tokenizer, device)
        return model, tokenizer, device

    def _get_model(self, model_id: str) -> Tuple[Any, Any, str]:
        if model_id in self._cache:
            return self._cache[model_id]
        return self._load_model(model_id)

    @staticmethod
    def _fallback_prompt(messages: List[Dict[str, str]]) -> str:
        lines = [f"{m['role']}: {m['content']}" for m in messages]
        lines.append("assistant:")
        return "\n".join(lines)

    def _tokenize(
        self, tokenizer: Any, messages: List[Dict[str, str]]
    ) -> Tuple[Any, Optional[Any]]:
        if hasattr(tokenizer, "apply_chat_template"):
            try:
                output = tokenizer.apply_chat_template(
                    messages,
                    tokenize=True,
                    add_generation_prompt=True,
                    return_tensors="pt",
                )
                if isinstance(output, dict):
                    return output["input_ids"], output.get("attention_mask")
                return output, None
            except TypeError:
                pass
        prompt = self._fallback_prompt(messages)
        encoded = tokenizer(prompt, return_tensors="pt")
        return encoded["input_ids"], encoded.get("attention_mask")

    def _truncate_messages(
        self, tokenizer: Any, messages: List[Dict[str, str]]
    ) -> Tuple[List[Dict[str, str]], Any, Optional[Any]]:
        while True:
            input_ids, attention_mask = self._tokenize(tokenizer, messages)
            prompt_tokens = int(input_ids.shape[-1])
            if prompt_tokens <= Config.MAX_CONTEXT_TOKENS or len(messages) <= 1:
                return messages, input_ids, attention_mask
            if messages[0]["role"] == "system" and len(messages) > 1:
                messages = messages[:1] + messages[2:]
            else:
                messages = messages[1:]

    async def generate(
        self,
        messages: List[Dict[str, str]],
        model_id: str,
        temperature: float,
        top_p: float,
        max_tokens: int,
        request_id: str,
    ) -> ChatResult:
        model, tokenizer, device = self._get_model(model_id)
        _trimmed_messages, input_ids, attention_mask = self._truncate_messages(
            tokenizer, list(messages)
        )
        prompt_tokens = int(input_ids.shape[-1])

        input_ids = input_ids.to(device)
        if attention_mask is not None:
            attention_mask = attention_mask.to(device)

        do_sample = temperature > 0
        output_ids = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=do_sample,
            repetition_penalty=1.1,
        )

        generated_ids = output_ids[0][prompt_tokens:]
        text = tokenizer.decode(generated_ids, skip_special_tokens=True)
        completion_tokens = int(generated_ids.shape[-1])

        usage = Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
        logger.info("request_id=%s provider=hf generate model=%s", request_id, model_id)
        return ChatResult(text=text, usage=usage)

    async def stream(
        self,
        messages: List[Dict[str, str]],
        model_id: str,
        temperature: float,
        top_p: float,
        max_tokens: int,
        request_id: str,
        cancel_token: CancellationToken,
    ) -> AsyncIterator[StreamChunk]:
        import asyncio
        from transformers import TextIteratorStreamer, StoppingCriteria, StoppingCriteriaList

        model, tokenizer, device = self._get_model(model_id)
        _trimmed_messages, input_ids, attention_mask = self._truncate_messages(
            tokenizer, list(messages)
        )
        prompt_tokens = int(input_ids.shape[-1])
        completion_tokens = 0

        input_ids = input_ids.to(device)
        if attention_mask is not None:
            attention_mask = attention_mask.to(device)

        class StopOnCancel(StoppingCriteria):
            def __init__(self, token: CancellationToken) -> None:
                self._token = token

            def __call__(self, *args, **kwargs) -> bool:
                return self._token.is_cancelled()

        streamer = TextIteratorStreamer(
            tokenizer, skip_prompt=True, skip_special_tokens=True
        )
        do_sample = temperature > 0
        stop_criteria = StoppingCriteriaList([StopOnCancel(cancel_token)])

        def _generate() -> None:
            model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=do_sample,
                repetition_penalty=1.1,
                streamer=streamer,
                stopping_criteria=stop_criteria,
            )

        loop = asyncio.get_running_loop()
        loop.run_in_executor(None, _generate)

        reasoning_filter = ReasoningFilter()

        def _next_token() -> Optional[str]:
            try:
                return next(streamer)
            except StopIteration:
                return None

        while True:
            if cancel_token.is_cancelled():
                break
            token = await asyncio.to_thread(_next_token)
            if token is None:
                break
            filtered = reasoning_filter.feed(token)
            if filtered:
                completion_tokens += len(
                    tokenizer.encode(filtered, add_special_tokens=False)
                )
                yield StreamChunk(token=filtered)

        usage = Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
        logger.info("request_id=%s provider=hf stream done model=%s", request_id, model_id)
        yield StreamChunk(token="", done=True, usage=usage)

    def list_models(self) -> list:
        return []
