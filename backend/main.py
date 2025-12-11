"""FastAPI backend for SelcukAiAssistant using Ollama."""
import logging
import json
from typing import Dict, Any, AsyncIterator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, field_validator

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
    """Request model for chat endpoint with validation."""
    
    question: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User's question (1-5000 characters)",
        examples=["Selçuk Üniversitesi'nin kuruluş tarihi nedir?"]
    )
    
    @field_validator('question')
    @classmethod
    def validate_question(cls, v: str) -> str:
        """Validate and sanitize question input."""
        if not v or not v.strip():
            raise ValueError("Soru boş olamaz")
        
        # Strip whitespace
        v = v.strip()
        
        # Basic XSS prevention - remove potential script tags
        dangerous_patterns = ['<script', '</script', 'javascript:', 'onerror=', 'onload=']
        v_lower = v.lower()
        for pattern in dangerous_patterns:
            if pattern in v_lower:
                raise ValueError("Geçersiz karakter dizisi tespit edildi")
        
        return v


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    
    answer: str = Field(
        ...,
        description="AI-generated answer to the user's question"
    )


@app.get("/")
async def root() -> Dict[str, str]:
    """
    Root health check endpoint.
    
    Returns:
        Dictionary with status and message
    """
    logger.info("Health check requested")
    return {"status": "ok", "message": "SelcukAiAssistant Backend is running"}


@app.get("/health/ollama")
async def ollama_health() -> Dict[str, Any]:
    """
    Check Ollama service health and model availability.
    
    This endpoint verifies:
    - Ollama service is running and accessible
    - Configured model is available (handles tag variations like :latest)
    - Lists all available models
    
    Returns:
        Dictionary with Ollama health status and available models
        
    Raises:
        HTTPException: 503 if Ollama service is unhealthy
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
    
    This endpoint:
    - Validates and sanitizes user input
    - Builds a contextualized prompt for Selçuk University
    - Generates AI response using the Ollama service
    - Includes retry logic for transient failures
    - Returns properly UTF-8 encoded Turkish text
    
    Args:
        request: ChatRequest containing the user's question (validated, 1-5000 chars)
        
    Returns:
        ChatResponse containing the AI-generated answer in Turkish
        
    Raises:
        HTTPException: 400 for invalid input, 503 for Ollama unavailable,
                      504 for timeout, 500 for other errors
    """
    # Log the request (truncate for privacy/security)
    question_preview = request.question[:50] + "..." if len(request.question) > 50 else request.question
    logger.info(f"Chat request received: {question_preview}")
    
    try:
        # Build prompt with Selçuk University context
        prompt = build_chat_prompt(request.question)
        
        # Generate response using Ollama service (with retry logic)
        answer = ollama_service.generate(prompt)
        
        logger.info(f"Chat request completed successfully (response length: {len(answer)} chars)")
        return ChatResponse(answer=answer)
        
    except HTTPException:
        # Re-raise HTTP exceptions from the service (already logged)
        raise
    except ValueError as e:
        # Validation errors from Pydantic
        logger.warning(f"Validation error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        # Catch-all for unexpected errors
        logger.exception(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Beklenmeyen hata: {str(e)}"
        )


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    """
    Streaming chat endpoint for real-time token-by-token responses.
    
    This endpoint:
    - Validates and sanitizes user input (same as /chat)
    - Builds a contextualized prompt for Selçuk University
    - Streams AI response token-by-token using Server-Sent Events (SSE)
    - Provides better user experience for long responses
    
    Args:
        request: ChatRequest containing the user's question (validated, 1-5000 chars)
        
    Returns:
        StreamingResponse with text/event-stream content type
        Each event contains a JSON object with partial response
        
    Raises:
        HTTPException: 400 for invalid input, 503 for Ollama unavailable,
                      504 for timeout, 500 for other errors
                      
    Example response stream:
        data: {"token": "Selçuk"}
        data: {"token": " Üniversitesi"}
        data: {"token": " 1975"}
        data: {"done": true}
    """
    # Log the request (truncate for privacy/security)
    question_preview = request.question[:50] + "..." if len(request.question) > 50 else request.question
    logger.info(f"Streaming chat request received: {question_preview}")
    
    async def generate_stream() -> AsyncIterator[str]:
        """Generate Server-Sent Events stream."""
        try:
            # Build prompt with Selçuk University context
            prompt = build_chat_prompt(request.question)
            
            # Stream response from Ollama
            for chunk in ollama_service.generate_stream(prompt):
                # Send each token as a Server-Sent Event
                yield f"data: {json.dumps({'token': chunk})}\n\n"
            
            # Send completion event
            yield f"data: {json.dumps({'done': True})}\n\n"
            
            logger.info("Streaming chat request completed successfully")
            
        except HTTPException as e:
            # Send error event
            error_data = {"error": e.detail, "status_code": e.status_code}
            yield f"data: {json.dumps(error_data)}\n\n"
            logger.error(f"HTTPException in streaming: {e.detail}")
        except Exception as e:
            # Send error event for unexpected errors
            error_data = {"error": f"Beklenmeyen hata: {str(e)}", "status_code": 500}
            yield f"data: {json.dumps(error_data)}\n\n"
            logger.exception(f"Unexpected error in streaming endpoint: {str(e)}")
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {Config.HOST}:{Config.PORT}")
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
