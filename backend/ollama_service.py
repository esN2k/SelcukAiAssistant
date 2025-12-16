"""Ollama service client for SelcukAiAssistant Backend (Async)."""
import asyncio
import json
import logging
from typing import Optional, Dict, Any, List, AsyncIterator

import httpx
from fastapi import HTTPException

from config import Config

logger = logging.getLogger(__name__)


class OllamaService:
    """Service class for interacting with Ollama API asynchronously."""
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """
        Initialize Ollama service.
        
        Args:
            base_url: Ollama base URL (defaults to Config.OLLAMA_BASE_URL)
            model: Model name (defaults to Config.OLLAMA_MODEL)
            timeout: Request timeout in seconds (defaults to Config.OLLAMA_TIMEOUT)
            max_retries: Maximum number of retry attempts for failed requests
            retry_delay: Initial delay between retries in seconds
        """
        self.base_url = base_url or Config.OLLAMA_BASE_URL
        self.model = model or Config.OLLAMA_MODEL
        self.timeout = timeout or Config.OLLAMA_TIMEOUT
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.api_url = f"{self.base_url}/api/generate"
        
        logger.info(
            f"Initialized Ollama service: url={self.api_url}, "
            f"model={self.model}, timeout={self.timeout}s, max_retries={self.max_retries}"
        )

    @staticmethod
    def _validate_prompt(prompt: str) -> None:
        """
        Validate prompt input.
        
        Args:
            prompt: The prompt to validate
            
        Raises:
            HTTPException: If prompt is empty or invalid
        """
        if not prompt or not prompt.strip():
            logger.warning("Empty prompt provided")
            raise HTTPException(
                status_code=400,
                detail="Lütfen bir soru girin."
            )

    @staticmethod
    def _clean_reasoning_artifacts(text: str) -> str:
        """
        Robustly clean DeepSeek-R1 reasoning artifacts from response.
        
        This method removes internal reasoning, think tags, and other artifacts
        that should not be shown to users, leaving only the final answer.
        
        Args:
            text: Raw response from the LLM
            
        Returns:
            Cleaned response with reasoning artifacts removed
        """
        import re
        
        if not text or not text.strip():
            return "Merhaba! Ben Selcuk AI Asistani. Size nasil yardimci olabilirim?"
        
        original_text = text
        
        # Step 1: Remove XML-style tags (think tags, instruction markers)
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = text.replace('<|im_end|>', '').replace('<|im_start|>', '')
        text = text.replace('<|end|>', '').replace('<|start|>', '')
        
        # Step 2: Remove reasoning block patterns
        # Pattern like: "Okay, let me..." or "Tamam, düşünelim..."
        reasoning_patterns = [
            r'^[^.!?\n]*\b(okay|alright|let me think|hmm|wait)\b[^.!?\n]*[\n.]',
            r'^[^.!?\n]*\b(tamam|peki|düşünelim|bakalım|bir dakika)\b[^.!?\n]*[\n.]',
        ]
        for pattern in reasoning_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
        
        # Step 3: Find the start of the actual answer
        # Priority 1: Look for "Merhaba" as answer start (common Turkish greeting)
        merhaba_matches = list(re.finditer(r'\bMerhaba[!.,]?', text, re.IGNORECASE))
        if merhaba_matches:
            # Take from the last "Merhaba" occurrence
            text = text[merhaba_matches[-1].start():]
        
        # Priority 2: Look for markdown headers as answer structure
        elif re.search(r'^##\s', text, re.MULTILINE):
            # Find the first markdown header
            header_match = re.search(r'^##\s', text, re.MULTILINE)
            if header_match:
                text = text[header_match.start():]
        
        # Step 4: Remove remaining reasoning sentences
        # English reasoning keywords
        english_reasoning = [
            r'[^.!?\n]*\b(the user (is asking|wants|needs))\b[^.!?\n]*[.!?\n]',
            r'[^.!?\n]*\b(i (should|need to|will|must))\b[^.!?\n]*[.!?\n]',
            r'[^.!?\n]*\b(let me|i\'ll|i\'m going to)\b[^.!?\n]*[.!?\n]',
        ]
        
        # Turkish reasoning keywords
        turkish_reasoning = [
            r'[^.!?\n]*\b(kullanıcı (soruyor|istiyor|diyor))\b[^.!?\n]*[.!?\n]',
            r'[^.!?\n]*\b(yapmalıyım|etmeliyim|aramalıyım)\b[^.!?\n]*[.!?\n]',
            r'[^.!?\n]*\b(bir bakalım|şöyle|hadi)\b[^.!?\n]*[.!?\n]',
        ]
        
        all_patterns = english_reasoning + turkish_reasoning
        for pattern in all_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
        
        # Step 5: Clean up whitespace
        # Remove multiple consecutive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        
        # Step 6: Validation and fallback
        # If the cleaned text is too short or empty, return a default message
        if len(text) < 15:
            # Try to salvage the original if it's not too contaminated
            if len(original_text.strip()) > 20 and '<think>' not in original_text.lower():
                return original_text.strip()
            return "Merhaba! Ben Selcuk AI Asistani. Size nasil yardimci olabilirim?"
        
        # If the text starts with lowercase (likely mid-sentence), try to find better start
        if text and text[0].islower():
            # Look for a sentence that starts with capital letter
            sentences = re.split(r'[.!?]\s+', text)
            for sentence in sentences:
                if sentence and sentence[0].isupper() and len(sentence) > 15:
                    text = sentence
                    break
        
        return text

    async def generate(self, prompt: str, stream: bool = False) -> str:
        """
        Generate a response from Ollama with retry logic (Async).
        
        Args:
            prompt: The prompt to send to Ollama
            stream: Whether to stream the response (default: False)
            
        Returns:
            Generated response text
            
        Raises:
            HTTPException: If there's an error communicating with Ollama
        """
        self._validate_prompt(prompt)
        
        logger.debug(f"Generating response for prompt (length: {len(prompt)} chars)")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for attempt in range(self.max_retries):
                try:
                    ollama_request = {
                        "model": self.model,
                        "prompt": prompt,
                        "stream": stream,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9,
                            "top_k": 40,
                            "repeat_penalty": 1.1,
                            "num_predict": 2048,
                            "stop": ["\n\n\n"]
                        }
                    }

                    response = await client.post(
                        self.api_url,
                        json=ollama_request,
                        headers={"Content-Type": "application/json; charset=utf-8"}
                    )

                    # Ensure response is decoded as UTF-8
                    response.encoding = 'utf-8'

                    # Log response status
                    logger.debug(
                        f"Ollama response status: {response.status_code} (attempt {attempt + 1}/{self.max_retries})")

                    # Handle HTTP errors
                    if response.status_code != 200:
                        error_detail = self._parse_error_response(response)
                        logger.error(f"Ollama API error: {error_detail}")
                        raise HTTPException(
                            status_code=response.status_code,
                            detail=f"Ollama API hatası: {error_detail}"
                        )

                    # Parse successful response with UTF-8 encoding
                    ollama_response = response.json()
                    answer = ollama_response.get("response", "")

                    if not answer:
                        logger.warning("Ollama returned empty response")
                        return "Üzgünüm, bir yanıt oluşturulamadı."

                    # Clean DeepSeek-R1 reasoning artifacts
                    answer = self._clean_reasoning_artifacts(answer)

                    logger.info(f"Successfully generated response (length: {len(answer)} chars)")
                    return answer

                except httpx.ReadTimeout:
                    logger.warning(
                        f"Ollama request timed out (attempt {attempt + 1}/{self.max_retries})")
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(self.retry_delay * (attempt + 1))
                        continue
                    logger.error(f"Ollama request timed out after {self.max_retries} attempts")
                    raise HTTPException(
                        status_code=504,
                        detail="Ollama isteği zaman aşımına uğradı. Lütfen tekrar deneyin."
                    )
                except httpx.RequestError as e:
                    logger.warning(
                        f"Failed to connect to Ollama (attempt {attempt + 1}/{self.max_retries}): {str(e)}")
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(self.retry_delay * (attempt + 1))
                        continue
                    logger.error(f"Failed to connect to Ollama after {self.max_retries} attempts")
                    raise HTTPException(
                        status_code=503,
                        detail=f"Ollama servisine bağlanılamadı. Hata: {str(e)}"
                    )
                except HTTPException:
                    # Re-raise HTTPExceptions as-is
                    raise
                except Exception as e:
                    logger.exception(f"Unexpected error in Ollama service: {str(e)}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Beklenmeyen hata: {str(e)}"
                    )

        return "Hata"

    async def generate_stream(self, prompt: str) -> AsyncIterator[str]:
        """
        Generate a streaming response from Ollama with token-by-token delivery (Async).
        
        This method:
        - Sends a streaming request to Ollama
        - Yields tokens as they arrive
        - Handles UTF-8 encoding properly
        - Provides real-time response experience
        
        Args:
            prompt: The prompt to send to Ollama
            
        Yields:
            Response tokens as strings (token-by-token or chunk-by-chunk)
            
        Raises:
            HTTPException: If there's an error communicating with Ollama
        """
        self._validate_prompt(prompt)
        
        logger.debug(f"Starting streaming generation for prompt (length: {len(prompt)} chars)")
        
        try:
            ollama_request = {
                "model": self.model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                    "repeat_penalty": 1.1,
                    "num_predict": 2048,
                    "stop": ["\n\n\n"]
                }
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                        "POST",
                        self.api_url,
                        json=ollama_request,
                        headers={"Content-Type": "application/json; charset=utf-8"}
                ) as response:

                    # Check HTTP status
                    if response.status_code != 200:
                        # We can't easily read the body in stream mode if error, but we try
                        error_detail = f"HTTP {response.status_code}"
                        logger.error(f"Ollama streaming API error: {error_detail}")
                        raise HTTPException(
                            status_code=response.status_code,
                            detail=f"Ollama API hatası: {error_detail}"
                        )

                    # Stream the response line by line
                    token_count = 0
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                # Parse JSON response
                                chunk_data = json.loads(line)

                                # Extract the response token
                                response_token = chunk_data.get("response", "")
                                if response_token:
                                    token_count += 1
                                    yield response_token

                                # Check if done
                                if chunk_data.get("done", False):
                                    logger.info(
                                        f"Streaming completed: {token_count} tokens generated")
                                    break

                            except json.JSONDecodeError:
                                logger.warning(
                                    f"Failed to parse streaming response line: {line[:100]}")
                                continue
                            except Exception as e:
                                logger.error(f"Error processing streaming chunk: {str(e)}")
                                continue

        except httpx.ReadTimeout:
            logger.error(f"Ollama streaming request timed out after {self.timeout}s")
            raise HTTPException(
                status_code=504,
                detail="Ollama isteği zaman aşımına uğradı. Lütfen tekrar deneyin."
            )
        except httpx.RequestError as e:
            logger.error(f"Failed to connect to Ollama for streaming: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail="Ollama servisine bağlanılamadı. Lütfen Ollama'nın çalıştığından emin olun."
            )
        except HTTPException:
            # Re-raise HTTPExceptions as-is
            raise
        except Exception as e:
            logger.exception(f"Unexpected error in Ollama streaming: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Beklenmeyen hata: {str(e)}"
            )

    async def health_check(self) -> Dict[str, Any]:
        """
        Check if Ollama service is healthy and if the configured model is available (Async).
        
        Returns:
            Dictionary with health status information
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Try to get the list of available models
                response = await client.get(f"{self.base_url}/api/tags")

                if response.status_code == 200:
                    models = response.json().get("models", [])
                    model_names = [m.get("name") for m in models]

                    # Check if our configured model is available
                    model_available = self._is_model_available(self.model, model_names)

                    return {
                        "status": "healthy" if model_available else "degraded",
                        "ollama_url": self.base_url,
                        "model": self.model,
                        "model_available": model_available,
                        "available_models": model_names
                    }
                else:
                    logger.warning(f"Ollama health check returned status {response.status_code}")
                    return {
                        "status": "unhealthy",
                        "ollama_url": self.base_url,
                        "model": self.model,
                        "error": f"HTTP {response.status_code}"
                    }

        except httpx.RequestError as e:
            logger.error(f"Cannot connect to Ollama for health check: {str(e)}")
            return {
                "status": "unhealthy",
                "ollama_url": self.base_url,
                "model": self.model,
                "error": "Connection failed"
            }
        except Exception as e:
            logger.exception(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "ollama_url": self.base_url,
                "model": self.model,
                "error": str(e)
            }
    
    @staticmethod
    def _is_model_available(target_model: str, available_models: List[str]) -> bool:
        """
        Check if a model is available, handling tag variations.
        
        Args:
            target_model: The model name to search for
            available_models: List of available model names
            
        Returns:
            True if the model is available (considering tag variations)
        """
        if not target_model or not available_models:
            return False
        
        # Direct match
        if target_model in available_models:
            return True
        
        # Extract base name (without tag)
        target_base = target_model.split(':')[0]
        
        # Check if any available model matches the base name
        for model in available_models:
            model_base = model.split(':')[0]
            if target_base == model_base:
                return True
        
        return False
    
    @staticmethod
    def _parse_error_response(response: httpx.Response) -> str:
        """
        Parse error response from Ollama.
        
        Args:
            response: The error response from Ollama
            
        Returns:
            Human-readable error message
        """
        try:
            error_data = response.json()
            return error_data.get("error", response.text)
        except (ValueError, KeyError, AttributeError):
            # JSON parsing or dict access failed, return raw text
            return response.text or f"HTTP {response.status_code}"
