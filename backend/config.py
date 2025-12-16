"""Configuration management for SelcukAiAssistant Backend."""
import logging
import os
import sys
from typing import List, Optional


def _configure_utf8_environment() -> None:
    """Ensure UTF-8 output without breaking pytest capture."""
    running_pytest = os.environ.get("PYTEST_CURRENT_TEST") is not None

    if sys.platform == 'win32':
        if running_pytest:
            return  # Let pytest manage stdout/stderr during capture

        for stream_name in ("stdout", "stderr"):
            stream = getattr(sys, stream_name, None)
            if stream is None:
                continue

            reconfigured = False
            if hasattr(stream, "reconfigure"):
                try:
                    stream.reconfigure(encoding='utf-8')
                    reconfigured = True
                except (AttributeError, ValueError):
                    pass

            if not reconfigured:
                buffer = getattr(stream, "buffer", None)
                if buffer is None:
                    continue
                import io
                setattr(sys, stream_name, io.TextIOWrapper(buffer, encoding='utf-8'))
    else:
        import locale
        try:
            locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
        except locale.Error:
            try:
                locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            except locale.Error:
                logging.warning(
                    "Failed to set UTF-8 locale. Turkish characters may not display correctly. "
                    "Available locales can be checked with 'locale -a' command."
                )


_configure_utf8_environment()


# Load environment variables from .env file if present
try:
    from dotenv import load_dotenv

    # Get the directory where this config.py file is located (backend/)
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(backend_dir, '.env')

    # Load .env file with explicit path
    load_dotenv(env_path)

    # Log if .env file exists
    if os.path.exists(env_path):
        logging.info(f"Loaded .env file from: {env_path}")
    else:
        logging.warning(f".env file not found at: {env_path}")
except ImportError:
    logging.warning("python-dotenv not installed, environment variables must be set manually")


    def load_dotenv(dotenv_path: Optional[str] = None) -> None:  # type: ignore[misc]
        return



class Config:
    """Application configuration with validation and type safety."""
    
    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS configuration
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    # Ollama configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1")
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "120"))
    OLLAMA_MAX_RETRIES: int = int(os.getenv("OLLAMA_MAX_RETRIES", "3"))
    OLLAMA_RETRY_DELAY: float = float(os.getenv("OLLAMA_RETRY_DELAY", "1.0"))
    
    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # RAG configuration (for future implementation)
    RAG_ENABLED: bool = os.getenv("RAG_ENABLED", "false").lower() == "true"
    RAG_VECTOR_DB_PATH: Optional[str] = os.getenv("RAG_VECTOR_DB_PATH", None)
    RAG_COLLECTION_NAME: str = os.getenv("RAG_COLLECTION_NAME", "selcuk_documents")
    RAG_CHUNK_SIZE: int = int(os.getenv("RAG_CHUNK_SIZE", "500"))
    RAG_CHUNK_OVERLAP: int = int(os.getenv("RAG_CHUNK_OVERLAP", "50"))

    # Appwrite configuration (optional)
    APPWRITE_ENDPOINT: Optional[str] = os.getenv("APPWRITE_ENDPOINT")
    APPWRITE_PROJECT_ID: Optional[str] = os.getenv("APPWRITE_PROJECT_ID")
    APPWRITE_API_KEY: Optional[str] = os.getenv("APPWRITE_API_KEY")
    APPWRITE_DATABASE_ID: Optional[str] = os.getenv("APPWRITE_DATABASE_ID")
    APPWRITE_COLLECTION_ID: Optional[str] = os.getenv("APPWRITE_COLLECTION_ID")

    @classmethod
    def validate(cls) -> None:
        """
        Validate configuration values on application startup.
        
        Raises:
            ValueError: If any configuration value is invalid
        """
        # Validate timeout settings
        if cls.OLLAMA_TIMEOUT < 1:
            raise ValueError("OLLAMA_TIMEOUT must be at least 1 second")
        
        if cls.OLLAMA_MAX_RETRIES < 1:
            raise ValueError("OLLAMA_MAX_RETRIES must be at least 1")
        
        if cls.OLLAMA_RETRY_DELAY < 0:
            raise ValueError("OLLAMA_RETRY_DELAY cannot be negative")
        
        # Validate server settings
        if cls.PORT < 1 or cls.PORT > 65535:
            raise ValueError("PORT must be between 1 and 65535")
        
        # Validate Ollama settings
        if not cls.OLLAMA_MODEL:
            raise ValueError("OLLAMA_MODEL cannot be empty")
        
        if not cls.OLLAMA_BASE_URL:
            raise ValueError("OLLAMA_BASE_URL cannot be empty")
        
        # Validate RAG settings if enabled
        if cls.RAG_ENABLED:
            if not cls.RAG_VECTOR_DB_PATH:
                raise ValueError("RAG_VECTOR_DB_PATH must be set when RAG_ENABLED is true")
            
            if cls.RAG_CHUNK_SIZE < 1:
                raise ValueError("RAG_CHUNK_SIZE must be at least 1")
            
            if cls.RAG_CHUNK_OVERLAP < 0:
                raise ValueError("RAG_CHUNK_OVERLAP cannot be negative")
            
            if cls.RAG_CHUNK_OVERLAP >= cls.RAG_CHUNK_SIZE:
                raise ValueError("RAG_CHUNK_OVERLAP must be less than RAG_CHUNK_SIZE")
    
    @classmethod
    def setup_logging(cls) -> None:
        """
        Configure application logging with UTF-8 encoding support.
        
        Sets up structured logging with timestamps, module names, and proper
        UTF-8 encoding for Turkish characters.
        """
        # Create a handler with UTF-8 encoding
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO))
        
        # Use UTF-8 encoding for the handler
        if hasattr(handler.stream, 'reconfigure'):
            handler.stream.reconfigure(encoding='utf-8')
        
        # Configure logging format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        # Set up root logger
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO),
            handlers=[handler],
            force=True  # Override any existing configuration
        )


# Validate configuration on import
Config.validate()
Config.setup_logging()
