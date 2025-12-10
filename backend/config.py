"""Configuration management for SelcukAiAssistant Backend."""
import logging
import os
import sys
from typing import List

# Configure Windows encoding if needed
if sys.platform == 'win32':
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class Config:
    """Application configuration with validation."""

    # Server configuration
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))

    # CORS configuration
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")

    # Ollama configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "selcuk-assistant")
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "30"))

    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls) -> None:
        """Validate configuration values."""
        if cls.OLLAMA_TIMEOUT < 1:
            raise ValueError("OLLAMA_TIMEOUT must be at least 1 second")

        if cls.PORT < 1 or cls.PORT > 65535:
            raise ValueError("PORT must be between 1 and 65535")

        if not cls.OLLAMA_MODEL:
            raise ValueError("OLLAMA_MODEL cannot be empty")

    @classmethod
    def setup_logging(cls) -> None:
        """Configure application logging."""
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )


# Validate configuration on import
Config.validate()
Config.setup_logging()
