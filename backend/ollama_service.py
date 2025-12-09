"""Ollama service client for SelcukAiAssistant Backend."""
import logging
from typing import Optional, Dict, Any

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
        timeout: Optional[int] = None
    ):
        """
        Initialize Ollama service.
        
        Args:
            base_url: Ollama base URL (defaults to Config.OLLAMA_BASE_URL)
            model: Model name (defaults to Config.OLLAMA_MODEL)
            timeout: Request timeout in seconds (defaults to Config.OLLAMA_TIMEOUT)
        """
        self.base_url = base_url or Config.OLLAMA_BASE_URL
        self.model = model or Config.OLLAMA_MODEL
        self.timeout = timeout or Config.OLLAMA_TIMEOUT
        self.api_url = f"{self.base_url}/api/generate"
        
        logger.info(
            f"Initialized Ollama service: url={self.api_url}, "
            f"model={self.model}, timeout={self.timeout}s"
        )
    
    def generate(self, prompt: str, stream: bool = False) -> str:
        """
        Generate a response from Ollama.
        
        Args:
            prompt: The prompt to send to Ollama
            stream: Whether to stream the response (default: False)
            
        Returns:
            Generated response text
            
        Raises:
            HTTPException: If there's an error communicating with Ollama
        """
        logger.debug(f"Generating response for prompt (length: {len(prompt)} chars)")
        
        try:
            ollama_request = {
                "model": self.model,
                "prompt": prompt,
                "stream": stream
            }
            
            response = requests.post(
                self.api_url,
                json=ollama_request,
                timeout=self.timeout
            )
            
            # Log response status
            logger.debug(f"Ollama response status: {response.status_code}")
            
            # Handle HTTP errors
            if response.status_code != 200:
                error_detail = self._parse_error_response(response)
                logger.error(f"Ollama API error: {error_detail}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Ollama API hatası: {error_detail}"
                )
            
            # Parse successful response
            ollama_response = response.json()
            answer = ollama_response.get("response", "")
            
            if not answer:
                logger.warning("Ollama returned empty response")
                return "Üzgünüm, bir yanıt oluşturulamadı."
            
            logger.info(f"Successfully generated response (length: {len(answer)} chars)")
            return answer
            
        except requests.exceptions.Timeout:
            logger.error(f"Ollama request timed out after {self.timeout}s")
            raise HTTPException(
                status_code=504,
                detail="Ollama isteği zaman aşımına uğradı. Lütfen tekrar deneyin."
            )
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Failed to connect to Ollama: {str(e)}")
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
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if Ollama service is healthy.
        
        Returns:
            Dictionary with health status information
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
                model_available = self.model in model_names
                
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
