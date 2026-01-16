"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA ADI: providers/translate_gemma.py                                       ║
║  AMAÇ: Google TranslateGemma-4B-IT ile çok dilli çeviri                       ║
║  KULLANIM: from providers.translate_gemma import TranslateGemmaProvider        ║
║  BAĞIMLILIKLAR: torch, transformers, bitsandbytes                             ║
║  YAZAN: esN2k - Selçuk Üniversitesi                                           ║
╚════════════════════════════════════════════════════════════════════════════════╝

DETAYLI AÇIKLAMA:
─────────────────
Google TranslateGemma-4B-IT modeli ile çok dilli çeviri yapan sağlayıcı.

Model: https://huggingface.co/google/translategemma-4b-it

Özellikler:
- 4-bit quantization (VRAM: ~2GB)
- Flash Attention 2 desteği (varsa)
- Batch inference (çoklu istek)

Desteklenen Diller:
- İngilizce ↔ Türkçe
- Arapça ↔ Türkçe
- Farsça ↔ Türkçe
- Almanca ↔ Türkçe
- Rusça ↔ Türkçe
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class TranslateGemmaProvider:
    """Google TranslateGemma-4B-IT ile çeviri sağlayıcısı.

    Args:
        model_name: HuggingFace model ID.
        use_4bit: 4-bit quantization kullanılsın mı.
        device: Çalışma cihazı (cuda/cpu).

    Attributes:
        LANG_CODES: Desteklenen dil kodları mapping'i.
    """

    # TranslateGemma dil kodları
    LANG_CODES: Dict[str, str] = {
        "tr": "tur_Latn",  # Turkish (Latin script)
        "en": "eng_Latn",  # English
        "ar": "ara_Arab",  # Arabic
        "fa": "pes_Arab",  # Persian (Farsi)
        "de": "deu_Latn",  # German
        "ru": "rus_Cyrl",  # Russian
    }

    def __init__(
        self,
        model_name: str = "google/translategemma-4b-it",
        use_4bit: bool = True,
        device: Optional[str] = None,
    ) -> None:
        """Model yükleme ve yapılandırma.

        Args:
            model_name: HuggingFace model ID.
            use_4bit: 4-bit quantization kullanılsın mı.
            device: Çalışma cihazı (cuda/cpu/auto).
        """
        self.model_name = model_name
        self._use_4bit = use_4bit
        self._model: Any = None
        self._tokenizer: Any = None
        self._device: str = ""

        # Lazy loading için device tercihini kaydet
        self._preferred_device = device

        logger.info("🌐 TranslateGemmaProvider başlatıldı (lazy loading)")
        logger.info("📦 Model: %s", model_name)

    def _ensure_loaded(self) -> None:
        """Model yüklü değilse yükler (lazy loading).

        Raises:
            RuntimeError: Gerekli bağımlılıklar yüklü değilse.
        """
        if self._model is not None:
            return

        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
        except ImportError as exc:
            raise RuntimeError(
                "TranslateGemma bağımlılıkları eksik. "
                "pip install torch transformers bitsandbytes accelerate"
            ) from exc

        # Device seçimi
        if self._preferred_device:
            self._device = self._preferred_device
        else:
            self._device = "cuda" if torch.cuda.is_available() else "cpu"

        logger.info("🌐 TranslateGemma yükleniyor: %s", self.model_name)
        logger.info("📍 Device: %s", self._device)

        # 4-bit quantization config
        bnb_config: Optional[BitsAndBytesConfig] = None
        if self._use_4bit and self._device == "cuda":
            try:
                bnb_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.bfloat16,
                    bnb_4bit_use_double_quant=True,
                )
                logger.info("⚙️  4-bit quantization etkin")
            except Exception as e:
                logger.warning("⚠️ 4-bit quantization başarısız: %s", e)
                bnb_config = None
        else:
            logger.warning(
                "⚠️ 4-bit quantization kapalı (VRAM kullanımı yüksek olacak)"
            )

        # Tokenizer
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        # Model yükleme
        model_kwargs: Dict[str, Any] = {
            "device_map": "auto" if self._device == "cuda" else None,
            "torch_dtype": torch.bfloat16 if self._device == "cuda" else torch.float32,
        }

        if bnb_config is not None:
            model_kwargs["quantization_config"] = bnb_config

        # Flash Attention 2 desteği (varsa)
        try:
            model_kwargs["attn_implementation"] = "flash_attention_2"
            logger.info("⚡ Flash Attention 2 deneniyor...")
        except Exception:
            logger.info("ℹ️ Flash Attention 2 mevcut değil, standart attention kullanılacak")

        try:
            self._model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                **model_kwargs,
            )
        except Exception:
            # Flash Attention olmadan dene
            model_kwargs.pop("attn_implementation", None)
            self._model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                **model_kwargs,
            )

        if self._device != "cuda":
            self._model = self._model.to(self._device)

        self._model.eval()

        logger.info("✅ Model yüklendi")
        if self._device == "cuda":
            vram_gb = torch.cuda.memory_allocated() / 1e9
            logger.info("📊 VRAM: %.2f GB", vram_gb)

    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        max_length: int = 512,
        num_beams: int = 4,
    ) -> str:
        """Metni çevirir (TranslateGemma formatı).

        Args:
            text: Çevrilecek metin.
            source_lang: Kaynak dil kodu (tr, en, ar, fa, de, ru).
            target_lang: Hedef dil kodu.
            max_length: Max output uzunluğu.
            num_beams: Beam search (1=greedy, 4=kaliteli).

        Returns:
            Çevrilmiş metin.

        Raises:
            ValueError: Desteklenmeyen dil kodu.

        Example:
            >>> translator.translate("Merhaba dünya", "tr", "en")
            "Hello world"
        """
        import torch

        self._ensure_loaded()

        # Dil kodlarını kontrol et
        if source_lang not in self.LANG_CODES:
            raise ValueError(f"Desteklenmeyen kaynak dil: {source_lang}")
        if target_lang not in self.LANG_CODES:
            raise ValueError(f"Desteklenmeyen hedef dil: {target_lang}")

        # TranslateGemma prompt formatı
        tgt_code = self.LANG_CODES[target_lang]
        prompt = f"<2{tgt_code}> {text}"

        # Tokenize
        inputs = self._tokenizer(
            prompt,
            return_tensors="pt",
            max_length=1024,
            truncation=True,
            padding=True,
        )

        # Device'a taşı
        inputs = {k: v.to(self._device) for k, v in inputs.items()}

        # Generate
        with torch.inference_mode():
            outputs = self._model.generate(
                **inputs,
                max_new_tokens=max_length,
                num_beams=num_beams,
                early_stopping=True,
                do_sample=False,
            )

        # Decode
        translated = self._tokenizer.decode(
            outputs[0],
            skip_special_tokens=True,
        ).strip()

        # Prompt kısmını kaldır (varsa)
        if translated.startswith(prompt):
            translated = translated[len(prompt):].strip()

        return translated

    def batch_translate(
        self,
        texts: List[str],
        source_lang: str,
        target_lang: str,
        max_length: int = 512,
        num_beams: int = 4,
    ) -> List[str]:
        """Toplu çeviri (daha hızlı).

        Args:
            texts: Çevrilecek metinler listesi.
            source_lang: Kaynak dil kodu.
            target_lang: Hedef dil kodu.
            max_length: Max output uzunluğu.
            num_beams: Beam search sayısı.

        Returns:
            Çevrilmiş metinler listesi.

        Raises:
            ValueError: Desteklenmeyen dil kodu.
        """
        import torch

        self._ensure_loaded()

        # Dil kodlarını kontrol et
        if source_lang not in self.LANG_CODES:
            raise ValueError(f"Desteklenmeyen kaynak dil: {source_lang}")
        if target_lang not in self.LANG_CODES:
            raise ValueError(f"Desteklenmeyen hedef dil: {target_lang}")

        # Batch processing
        tgt_code = self.LANG_CODES[target_lang]
        prompts = [f"<2{tgt_code}> {text}" for text in texts]

        inputs = self._tokenizer(
            prompts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=1024,
        )

        # Device'a taşı
        inputs = {k: v.to(self._device) for k, v in inputs.items()}

        with torch.inference_mode():
            outputs = self._model.generate(
                **inputs,
                max_new_tokens=max_length,
                num_beams=num_beams,
                early_stopping=True,
                do_sample=False,
            )

        translations = []
        for i, out in enumerate(outputs):
            translated = self._tokenizer.decode(out, skip_special_tokens=True).strip()
            # Prompt kısmını kaldır
            if translated.startswith(prompts[i]):
                translated = translated[len(prompts[i]):].strip()
            translations.append(translated)

        return translations

    def get_model_info(self) -> Dict[str, Any]:
        """Model istatistikleri döndürür.

        Returns:
            Model bilgileri sözlüğü.
        """
        import torch

        info: Dict[str, Any] = {
            "model_name": self.model_name,
            "device": self._device if self._device else "not_loaded",
            "vram_usage_gb": 0.0,
            "max_vram_gb": 0.0,
            "quantization": "4-bit NF4" if self._use_4bit else "none",
            "supported_languages": list(self.LANG_CODES.keys()),
            "loaded": self._model is not None,
        }

        if self._device == "cuda" and self._model is not None:
            try:
                info["vram_usage_gb"] = round(torch.cuda.memory_allocated() / 1e9, 2)
                info["max_vram_gb"] = round(torch.cuda.max_memory_allocated() / 1e9, 2)
            except Exception:
                pass

        return info

    def is_loaded(self) -> bool:
        """Model yüklü mü kontrol eder.

        Returns:
            Model yüklü ise True.
        """
        return self._model is not None

    def unload(self) -> None:
        """Modeli bellekten kaldırır."""
        import gc

        if self._model is not None:
            del self._model
            self._model = None

        if self._tokenizer is not None:
            del self._tokenizer
            self._tokenizer = None

        gc.collect()

        try:
            import torch

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except Exception:
            pass

        logger.info("🗑️ Model bellekten kaldırıldı")
