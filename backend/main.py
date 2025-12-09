"""FastAPI backend for SelcukAiAssistant using Ollama."""
import os
import sys
import io
from typing import Optional

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="SelcukAiAssistant Backend")

# Configure CORS to allow Flutter app to connect
# In production, set ALLOWED_ORIGINS environment variable
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ollama configuration - configurable via environment variables
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "30"))  # Default 30 seconds


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    question: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "SelcukAiAssistant Backend is running"}


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
    try:
        # Build the prompt with the same context as before
        prompt = f'''
Siz dost canlısı ve profesyonel bir yapay zeka asistanısınız. Lütfen kullanıcı sorularını Türkçe yanıtlayın

Sen, Selçuk Üniversitesi (SÜ) öğrencileri ve akademik/idari personeli için çalışan, resmi bilgilere dayalı cevaplar veren bir AI asistansın.
Tüm soruları, Selçuk Üniversitesi'nin güncel yönetmeliklerine, akademik takvimine, duyurularına ve iç prosedürlerine göre yanıtlamalısın.
Yanıtlarında profesyonel, resmi ve kurallara uygun bir dil kullan.
Bilmediğin veya emin olmadığın SÜ ile ilgili konularda, tahminde bulunmak yerine dürüstçe 'Bu konuda güncel Selçuk Üniversitesi bilgisine sahip değilim' veya 'Lütfen ilgili birime danışınız' şeklinde yanıt ver.
Kesinlikle Selçuk Üniversitesi ile ilgisi olmayan veya genel kültür bilgisi gerektiren sorulara da SÜ bağlamını gözeterek cevap vermekten kaçın.

Yanıt verirken, içeriğinizi daha anlaşılır ve okunması kolay hale getirmek için Markdown biçimlendirmesini kullanabilirsiniz. Örneğin:
- Önemli noktaları vurgulamak için **kalın** kullanın
- Teknik terimleri belirtmek için **kod** kullanın
- Kodu görüntülemek için **kod blokları** kullanın
- İçeriği düzenlemek için liste ve başlıklar kullanın
- Önemli bilgilere atıfta bulunmak için > kullanın

Kullanıcı sorusu: {request.question}
'''

        # Prepare the request to Ollama
        ollama_request = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }

        # Send request to Ollama
        response = requests.post(
            OLLAMA_URL,
            json=ollama_request,
            timeout=OLLAMA_TIMEOUT
        )
        response.raise_for_status()

        # Parse Ollama response
        ollama_response = response.json()
        answer = ollama_response.get("response", "")

        if not answer:
            answer = "Üzgünüm, bir yanıt oluşturulamadı."

        return ChatResponse(answer=answer)

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Ollama isteği zaman aşımına uğradı. Lütfen tekrar deneyin."
        )
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Ollama servisine bağlanılamadı. Lütfen Ollama'nın çalıştığından emin olun."
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ollama isteği başarısız oldu: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Beklenmeyen hata: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "127.0.0.1")  # Default to localhost for security
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
