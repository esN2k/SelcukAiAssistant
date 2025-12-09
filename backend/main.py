"""FastAPI backend for SelcukAiAssistant using Ollama."""
import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import Config
from ollama_service import OllamaService
from prompts import build_chat_prompt

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="SelcukAiAssistant Backend")

# Configure CORS to allow Flutter app to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Ollama service
ollama_service = OllamaService()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    question: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str


@app.get("/")
async def root():
    """Health check endpoint."""
    logger.info("Health check requested")
    return {"status": "ok", "message": "SelcukAiAssistant Backend is running"}


@app.get("/health/ollama")
async def ollama_health():
    """
    Check Ollama service health.
    
    Returns:
        Dictionary with Ollama health status and available models
    """
    logger.info("Ollama health check requested")
    health_status = ollama_service.health_check()
    
    # Return appropriate HTTP status based on health
    if health_status["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=health_status)
    
    return health_status



@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint that processes user questions using Ollama.
    
    Args:
        request: ChatRequest containing the user's question
        
    Returns:
        ChatResponse containing the AI-generated answer
        
    Raises:
        HTTPException: If there's an error communicating with Ollama
    """
    logger.info(f"Chat request received: {request.question[:50]}...")
    
    try:
        # Build prompt with context
        prompt = build_chat_prompt(request.question)
        
        # Generate response using Ollama service
        answer = ollama_service.generate(prompt)
        
        logger.info("Chat request completed successfully")
        return ChatResponse(answer=answer)
        
    except HTTPException:
        # Re-raise HTTP exceptions from the service
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Beklenmeyen hata: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {Config.HOST}:{Config.PORT}")
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
