"""HuggingFace Transformers sağlayıcısı (opsiyonel 4-bit yükleme)."""
from __future__ import annotations

import logging
from typing import Any, AsyncIterator, Optional, cast

from config import Config
from providers.base import CancellationToken, ChatResult, ModelProvider, StreamChunk, Usage
from utils import ReasoningFilter

logger = logging.getLogger(__name__)


class HuggingFaceProvider(ModelProvider):
    """Giriş: HuggingFace yapılandırması.

    Çıkış: Sağlayıcı nesnesi.
    İşleyiş: Modeli yükler ve üretim işlemlerini yürütür.
    """

    name = "huggingface"

    def __init__(self) -> None:
        """Giriş: yok.

        Çıkış: Nesne.
        İşleyiş: Model önbelleğini başlatır.
        """
        self._cache: dict[str, tuple[Any, Any, str]] = {}

    def _ensure_dependencies(self) -> None:
        """Giriş: yok.

        Çıkış: yok.
        İşleyiş: Gerekli HuggingFace bağımlılıklarını kontrol eder.
        """
        try:
            import torch  # noqa: F401
            import transformers  # noqa: F401
        except ImportError as exc:
            raise RuntimeError(
                "HuggingFace bağımlılıkları eksik. "
                "backend/requirements-hf.txt kurun."
            ) from exc

    @staticmethod
    def _pick_device(preferred: str) -> str:
        """Giriş: Tercih edilen cihaz.

        Çıkış: Cihaz adı.
        İşleyiş: CUDA/MPS/CPU seçimini yapar.
        """
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
        """Giriş: dtype adı ve cihaz.

        Çıkış: Torch dtype.
        İşleyiş: Dtype tercihini belirler.
        """
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
        """Giriş: Model kimliği.

        Çıkış: (model, tokenizer, device) üçlüsü.
        İşleyiş: Modeli indirir/yükler ve önbelleğe alır.
        """
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
            logger.warning("HF_LOAD_IN_4BIT CUDA dışında yok sayıldı.")

        tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
        if tokenizer.pad_token is None and tokenizer.eos_token is not None:
            tokenizer.pad_token = tokenizer.eos_token

        kwargs: dict[str, Any] = {}
        if quant_config is not None:
            kwargs["quantization_config"] = quant_config
        if device == "cuda":
            kwargs["device_map"] = "auto"
            kwargs["max_memory"] = {0: "5GiB"}  # 6GB GPU için güvenli limit
        if Config.HF_ATTENTION_IMPL:
            kwargs["attn_implementation"] = Config.HF_ATTENTION_IMPL

        try:
            model = AutoModelForCausalLM.from_pretrained(model_id, dtype=dtype, **kwargs)
        except TypeError:
            try:
                model = AutoModelForCausalLM.from_pretrained(
                    model_id, torch_dtype=dtype, **kwargs
                )
            except TypeError:
                kwargs.pop("attn_implementation", None)
                try:
                    model = AutoModelForCausalLM.from_pretrained(
                        model_id, dtype=dtype, **kwargs
                    )
                except TypeError:
                    model = AutoModelForCausalLM.from_pretrained(
                        model_id, torch_dtype=dtype, **kwargs
                    )

        model = cast(Any, model)
        if device != "cuda":
            model.to(torch.device(device))

        model.eval()
        self._cache[model_id] = (model, tokenizer, device)
        return model, tokenizer, device

    def _get_model(self, model_id: str) -> tuple[Any, Any, str]:
        """Giriş: Model kimliği.

        Çıkış: (model, tokenizer, device) üçlüsü.
        İşleyiş: Önbellekten alır veya yükler.
        """
        if model_id in self._cache:
            return self._cache[model_id]
        return self._load_model(model_id)

    @staticmethod
    def _fallback_prompt(messages: list[dict[str, str]]) -> str:
        """Giriş: Mesaj listesi.

        Çıkış: Tek string prompt.
        İşleyiş: role:content formatında prompt üretir.
        """
        lines = [f"{m['role']}: {m['content']}" for m in messages]
        lines.append("assistant:")
        return "\n".join(lines)

    def _tokenize(
        self,
        tokenizer: Any,
        messages: list[dict[str, str]],
    ) -> tuple[Any, Optional[Any]]:
        """Giriş: Tokenizer ve mesajlar.

        Çıkış: input_ids ve attention_mask.
        İşleyiş: Chat template varsa onu, yoksa fallback promptu kullanır.
        """
        if hasattr(tokenizer, "apply_chat_template"):
            try:
                prompt = tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True,
                )
                if isinstance(prompt, str) and prompt.strip():
                    encoded = tokenizer(prompt, return_tensors="pt")
                    return encoded["input_ids"], encoded.get("attention_mask")
            except TypeError:
                pass

        prompt = self._fallback_prompt(messages)
        encoded = tokenizer(prompt, return_tensors="pt")
        return encoded["input_ids"], encoded.get("attention_mask")

    def _truncate_messages(
        self,
        tokenizer: Any,
        messages: list[dict[str, str]],
    ) -> tuple[list[dict[str, str]], Any, Optional[Any]]:
        """Giriş: Tokenizer ve mesajlar.

        Çıkış: Budanmış mesajlar, input_ids, attention_mask.
        İşleyiş: Token sınırına sığana kadar eski mesajları çıkarır.
        """
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
        messages: list[dict[str, str]],
        model_id: str,
        temperature: float,
        top_p: float,
        max_tokens: int,
        request_id: str,
    ) -> ChatResult:
        """Giriş: Mesajlar ve üretim parametreleri.

        Çıkış: ChatResult.
        İşleyiş: Transformers generate ile tek seferlik yanıt üretir.
        """
        model, tokenizer, device = self._get_model(model_id)
        _trimmed_messages, input_ids, attention_mask = self._truncate_messages(
            tokenizer, list(messages)
        )
        prompt_tokens = int(input_ids.shape[-1])

        input_ids = input_ids.to(device)
        if attention_mask is not None:
            attention_mask = attention_mask.to(device)
        else:
            import torch
            attention_mask = torch.ones_like(input_ids)

        do_sample = temperature > 0
        output_ids = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=do_sample,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.pad_token_id,
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
        messages: list[dict[str, str]],
        model_id: str,
        temperature: float,
        top_p: float,
        max_tokens: int,
        request_id: str,
        cancel_token: CancellationToken,
    ) -> AsyncIterator[StreamChunk]:
        """Giriş: Mesajlar ve üretim parametreleri.

        Çıkış: StreamChunk akışı.
        İşleyiş: TextIteratorStreamer ile token akışı sağlar.
        """
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
        else:
            import torch
            attention_mask = torch.ones_like(input_ids)

        class StopOnCancel(StoppingCriteria):
            """Giriş: CancellationToken.

            Çıkış: StoppingCriteria.
            İşleyiş: İptal sinyali geldiğinde üretimi durdurur.
            """

            def __init__(self, token: CancellationToken) -> None:
                """Giriş: CancellationToken.

                Çıkış: Nesne.
                İşleyiş: İptal sinyalini saklar.
                """
                self._token = token

            def __call__(self, *args, **kwargs) -> bool:
                """Giriş: Model üretim argümanları.

                Çıkış: bool.
                İşleyiş: İptal sinyalini kontrol eder.
                """
                return self._token.is_cancelled()

        streamer = TextIteratorStreamer(
            tokenizer, skip_prompt=True, skip_special_tokens=True
        )
        do_sample = temperature > 0
        stop_criteria = StoppingCriteriaList([StopOnCancel(cancel_token)])

        def _generate() -> None:
            """Giriş: yok.

            Çıkış: yok.
            İşleyiş: Model.generate çağrısını çalıştırır.
            """
            model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=do_sample,
                repetition_penalty=1.1,
                pad_token_id=tokenizer.pad_token_id,
                streamer=streamer,
                stopping_criteria=stop_criteria,
            )

        loop = asyncio.get_running_loop()
        loop.run_in_executor(None, _generate)

        reasoning_filter = ReasoningFilter()

        def _next_token() -> Optional[str]:
            """Giriş: yok.

            Çıkış: Yeni token veya None.
            İşleyiş: Streamer'dan sıradaki tokenı alır.
            """
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
        """Giriş: yok.

        Çıkış: Boş liste.
        İşleyiş: Katalog verisi başka katmanda tutulur.
        """
        return []
