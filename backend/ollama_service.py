"""Ollama service client for SelcukAiAssistant Backend."""
import json
import logging
import time
from typing import Optional, Dict, Any, List, Iterator

import requests
from fastapi import HTTPException

from config import Config

logger = logging.getLogger(__name__)


class OllamaService:
    """Service class for interacting with Ollama API."""
    
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
    
    def _validate_prompt(self, prompt: str) -> None:
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
    
    def generate(self, prompt: str, stream: bool = False) -> str:
        """
        Generate a response from Ollama with retry logic.
        
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
        
        for attempt in range(self.max_retries):
            try:
                ollama_request = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": stream
                }
                
                response = requests.post(
                    self.api_url,
                    json=ollama_request,
                    timeout=self.timeout,
                    headers={"Content-Type": "application/json; charset=utf-8"}
                )
                
                # Ensure response is decoded as UTF-8
                response.encoding = 'utf-8'
                
                # Log response status
                logger.debug(f"Ollama response status: {response.status_code} (attempt {attempt + 1}/{self.max_retries})")
                
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
                
                logger.info(f"Successfully generated response (length: {len(answer)} chars)")
                return answer

            except requests.exceptions.Timeout:
                logger.warning(f"Ollama request timed out (attempt {attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                logger.error(f"Ollama request timed out after {self.max_retries} attempts")
                raise HTTPException(
                    status_code=504,
                    detail="Ollama isteği zaman aşımına uğradı. Lütfen tekrar deneyin."
                )
            except requests.exceptions.ConnectionError:
                logger.warning(f"Failed to connect to Ollama (attempt {attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                logger.error(f"Failed to connect to Ollama after {self.max_retries} attempts")
                raise HTTPException(
                    status_code=503,
                    detail="Ollama servisine bağlanılamadı. Lütfen Ollama'nın çalıştığından emin olun."
                )
            except requests.exceptions.RequestException as e:
                logger.error(f"Ollama request failed: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Ollama isteği başarısız oldu: {str(e)}"
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

        # This part should be unreachable due to the exception raises in loop
        return "Hata"
    
    def generate_stream(self, prompt: str) -> Iterator[str]:
        """
        Generate a streaming response from Ollama with token-by-token delivery.
        
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
            
        Example:
            >>> for token in ollama_service.generate_stream("Hello"):
            ...     print(token, end='', flush=True)
            Hello! How can I help you?
        """
        self._validate_prompt(prompt)
        
        logger.debug(f"Starting streaming generation for prompt (length: {len(prompt)} chars)")
        
        try:
            ollama_request = {
                "model": self.model,
                "prompt": prompt,
                "stream": True  # Enable streaming
            }
            
            response = requests.post(
                self.api_url,
                json=ollama_request,
                timeout=self.timeout,
                headers={"Content-Type": "application/json; charset=utf-8"},
                stream=True  # Enable streaming response
            )
            
            # Check HTTP status
            if response.status_code != 200:
                error_detail = self._parse_error_response(response)
                logger.error(f"Ollama streaming API error: {error_detail}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Ollama API hatası: {error_detail}"
                )
            
            # Stream the response line by line
            token_count = 0
            for line in response.iter_lines():
                if line:
                    try:
                        # Decode line as UTF-8
                        line_str = line.decode('utf-8')
                        
                        # Parse JSON response
                        chunk_data = json.loads(line_str)
                        
                        # Extract the response token
                        token = chunk_data.get("response", "")
                        if token:
                            token_count += 1
                            yield token
                        
                        # Check if done
                        if chunk_data.get("done", False):
                            logger.info(f"Streaming completed: {token_count} tokens generated")
                            break

                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse streaming response line: {line_str[:100]}")
                        continue
                    except Exception as e:
                        logger.error(f"Error processing streaming chunk: {str(e)}")
                        continue
        
        except requests.exceptions.Timeout:
            logger.error(f"Ollama streaming request timed out after {self.timeout}s")
            raise HTTPException(
                status_code=504,
                detail="Ollama isteği zaman aşımına uğradı. Lütfen tekrar deneyin."
            )
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Failed to connect to Ollama for streaming: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail="Ollama servisine bağlanılamadı. Lütfen Ollama'nın çalıştığından emin olun."
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama streaming request failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Ollama isteği başarısız oldu: {str(e)}"
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
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if Ollama service is healthy and if the configured model is available.
        
        Handles model name variations like 'model:latest' matching 'model' or vice versa.
        
        Returns:
            Dictionary with health status information including:
            - status: 'healthy', 'degraded', or 'unhealthy'
            - ollama_url: Base URL of Ollama service
            - model: Configured model name
            - model_available: Whether the model is available
            - available_models: List of all available models (if service is up)
        """
        try:
            # Try to get the list of available models
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m.get("name") for m in models]
                
                # Check if our configured model is available
                # Handle model tag variations (e.g., 'model' vs 'model:latest')
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
                
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama for health check")
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
        
        Examples:
            - 'llama3.1' matches ['llama3.1:latest']
            - 'llama3.1:latest' matches ['llama3.1']
            - 'selcuk_ai_assistant:latest' matches ['selcuk_ai_assistant:latest']
        
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
    def _parse_error_response(response: requests.Response) -> str:
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
        except Exception:
            return response.text or f"HTTP {response.status_code}"
