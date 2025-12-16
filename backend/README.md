# SelcukAiAssistant Backend

FastAPI backend for SelcukAiAssistant - A graduation project AI chatbot for Selçuk University students using local AI models via Ollama.

## 🎯 Project Overview

This backend provides:
- **AI Chat Interface**: Question-answering for Selçuk University topics
- **Streaming Support**: Real-time token-by-token responses
- **Turkish Language**: Full UTF-8 support for Turkish characters
- **RAG Ready**: Prepared structure for document retrieval augmentation
- **Production Ready**: Comprehensive error handling, retry logic, and validation

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running locally
3. **Model**: `selcuk_ai_assistant:latest` or `llama3.1` (fallback)

## 🚀 Quick Start

### 1. Install Ollama

Download and install from [https://ollama.ai](https://ollama.ai)

### 2. Pull the Model

For this project (recommended):
```bash
# After creating your custom model
ollama pull selcuk_ai_assistant:latest
```

Or use the fallback model:
```bash
ollama pull llama3.1
```

### 3. Verify Ollama is Running

```bash
ollama list
```

### 4. Install Python Dependencies

Using virtual environment (recommended):
```bash
cd backend
python -m venv venv
venv\Scripts\activate # On Linux: source venv/bin/activate  
pip install -r requirements.txt
```

Or directly:
```bash
cd backend
pip install -r requirements.txt
```

### 5. Configure Environment (Optional)

Copy `.env.example` to `.env` and adjust values:

```bash
cp .env.example .env
# Edit .env with your preferred settings
```

**Key Configuration Options:**
- `OLLAMA_MODEL`: Model name (default: `llama3.1`, recommended: `selcuk_ai_assistant`)
- `OLLAMA_TIMEOUT`: Request timeout in seconds (default: 120)
- `OLLAMA_MAX_RETRIES`: Retry attempts for failed requests (default: 3)
- `LOG_LEVEL`: Logging verbosity (DEBUG, INFO, WARNING, ERROR)
- `RAG_ENABLED`: Enable RAG for document-based responses (default: false)

See `.env.example` for all configuration options.

### 6. Run the Server

Development mode (localhost only):
```bash
cd backend
python main.py
```

Allow external connections (e.g., for mobile testing):
```bash
cd backend
HOST=0.0.0.0 python main.py
```

Using uvicorn with hot reload:
```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The server will start at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
**GET** `/`

Simple health check to verify the backend is running.

**Response:**
```json
{
  "status": "ok",
  "message": "SelcukAiAssistant Backend is running"
}
```

#### 2. Ollama Health Check
**GET** `/health/ollama`

Check Ollama service status and model availability. Handles model tag variations (e.g., `llama3.1` matches `llama3.1:latest`).

**Response (Healthy):**
```json
{
  "status": "healthy",
  "ollama_url": "http://localhost:11434",
  "model": "selcuk_ai_assistant",
  "model_available": true,
  "available_models": ["selcuk_ai_assistant:latest", "llama3.1"]
}
```

**Response (Degraded - Model Not Found):**
```json
{
  "status": "degraded",
  "ollama_url": "http://localhost:11434",
  "model": "selcuk_ai_assistant",
  "model_available": false,
  "available_models": ["llama3.1", "mistral"]
}
```

**Response (Unhealthy - Service Down):**
```
Status: 503 Service Unavailable
```
```json
{
  "detail": {
    "status": "unhealthy",
    "ollama_url": "http://localhost:11434",
    "model": "selcuk_ai_assistant",
    "error": "Connection failed"
  }
}
```

#### 3. Chat (Non-Streaming)
**POST** `/chat`

Send a question and receive a complete answer.

**Request:**
```json
{
  "question": "Selçuk Üniversitesi'nin kuruluş tarihi nedir?"
}
```

**Validation:**
- Question length: 1-5000 characters
- Automatic whitespace trimming
- XSS prevention (blocks dangerous patterns)

**Response:**
```json
{
  "answer": "Selçuk Üniversitesi, 17 Temmuz 1975 tarihinde Konya'da kurulmuştur..."
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input (empty, too long, dangerous content)
- `503 Service Unavailable`: Ollama not accessible
- `504 Gateway Timeout`: Request timed out (increases with retries)
- `500 Internal Server Error`: Unexpected error

#### 4. Chat (Streaming) 🆕
**POST** `/chat/stream`

Send a question and receive a streaming response token-by-token using Server-Sent Events (SSE).

**Request:**
```json
{
  "question": "Selçuk Üniversitesi hakkında bilgi ver"
}
```

**Response (SSE Stream):**
```
data: {"token": "Selçuk"}

data: {"token": " Üniversitesi"}

data: {"token": " 1975"}

data: {"token": " yılında"}

data: {"done": true}
```

**Error Event:**
```
data: {"error": "Error message", "status_code": 503}
```

**Client Example (JavaScript):**
```javascript
const eventSource = new EventSource('http://localhost:8000/chat/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: 'Test question' })
});

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.done) {
    eventSource.close();
  } else if (data.error) {
    console.error(data.error);
    eventSource.close();
  } else {
    process.stdout.write(data.token);
  }
};
```

## 🧪 Testing

### Run All Tests

```bash
cd backend
pytest -v
```

### Run Specific Test Files

```bash
# Original tests
pytest test_main.py -v

# Extended tests (new features)
pytest test_extended.py -v
```

### Test Coverage

**30 tests covering:**
- ✅ Health check endpoints (2 tests)
- ✅ Chat endpoint functionality (7 tests)
- ✅ Input validation and sanitization (5 tests)
- ✅ Health check model matching with tags (4 tests)
- ✅ Retry logic and error handling (4 tests)
- ✅ RAG service structure (6 tests)
- ✅ UTF-8 encoding for Turkish characters (2 tests)

### Test with Coverage Report

```bash
cd backend
pip install pytest-cov
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

## 🔧 Development

### Project Structure

```
backend/
├── main.py              # FastAPI app and endpoints
├── config.py            # Configuration management
├── ollama_service.py    # Ollama API client with retry logic
├── prompts.py           # Prompt templates
├── rag_service.py       # RAG service (placeholder for future)
├── test_main.py         # Original unit tests
├── test_extended.py     # Extended tests for new features
├── requirements.txt     # Production dependencies
├── requirements-dev.txt # Development dependencies
├── .env.example         # Example environment configuration
└── README.md           # This file
```

### Key Features

#### 1. UTF-8 Encoding Support
- Proper handling of Turkish characters (ı, ş, ğ, ü, ö, ç)
- UTF-8 headers in all HTTP requests
- Platform-specific encoding configuration (Windows/Linux)
- UTF-8 logging support

#### 2. Retry Logic
- Automatic retry on connection errors and timeouts
- Exponential backoff (1s, 2s, 3s delays)
- Configurable retry attempts (default: 3)
- No retry on HTTP errors (4xx, 5xx)

#### 3. Health Check Improvements
- Handles model tag variations (`:latest`, `:v1`, etc.)
- Smart model name matching
- Three states: healthy, degraded, unhealthy

#### 4. Input Validation & Security
- Pydantic V2 field validators
- Length constraints (1-5000 chars)
- XSS prevention (blocks `<script>`, `javascript:`, etc.)
- Automatic whitespace trimming

#### 5. Comprehensive Error Handling
- Specific error messages in Turkish
- Proper HTTP status codes
- Detailed logging for debugging
- Graceful degradation

## 📖 API Examples

### Using curl

**Health Check:**
```bash
curl http://localhost:8000/
```

**Ollama Status:**
```bash
curl http://localhost:8000/health/ollama
```

**Chat Request:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Selçuk Üniversitesi nerede?"}'
```

**Streaming Chat:**
```bash
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"question": "Selçuk Üniversitesi hakkında bilgi ver"}' \
  --no-buffer
```

### Using Python requests

```python
import requests

# Non-streaming chat
response = requests.post(
    "http://localhost:8000/chat",
    json={"question": "Merhaba!"}
)
print(response.json()["answer"])

# Streaming chat
import json
response = requests.post(
    "http://localhost:8000/chat/stream",
    json={"question": "Selçuk Üniversitesi nerede?"},
    stream=True
)

for line in response.iter_lines():
    if line:
        data = json.loads(line.decode('utf-8').replace('data: ', ''))
        if 'token' in data:
            print(data['token'], end='', flush=True)
        elif data.get('done'):
            print()  # New line at end
```

## 🚀 Deployment

### Production Considerations

1. **Use production ASGI server:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

2. **Set specific CORS origins:**
```bash
export ALLOWED_ORIGINS="https://yourdomain.com,https://app.yourdomain.com"
```

3. **Configure proper timeouts:**
```bash
export OLLAMA_TIMEOUT=180
export OLLAMA_MAX_RETRIES=5
```

4. **Enable production logging:**
```bash
export LOG_LEVEL=WARNING
```

5. **Set up monitoring and health checks**

6. **Use a reverse proxy (nginx/Caddy)** for SSL/TLS

### Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔮 Future Features (RAG Integration)

The backend is prepared for RAG (Retrieval-Augmented Generation):

### Planned Capabilities
- Document ingestion from PDFs, text files, Markdown
- Vector storage using ChromaDB
- Semantic similarity search
- Context injection into prompts
- University document knowledge base

### Configuration
```bash
# In .env
RAG_ENABLED=true
RAG_VECTOR_DB_PATH=./data/chromadb
RAG_COLLECTION_NAME=selcuk_documents
RAG_CHUNK_SIZE=500
RAG_CHUNK_OVERLAP=50
```

### Required Dependencies (not yet installed)
```bash
pip install chromadb sentence-transformers pypdf
```

See `rag_service.py` for the prepared structure.

## 🐛 Troubleshooting
## 🐛 Troubleshooting

### Ollama Connection Issues

**Error:** `Ollama servisine bağlanılamadı`

**Solutions:**
1. Verify Ollama is running:
   ```bash
   ollama list
   ```

2. Test Ollama directly:
   ```bash
   curl http://localhost:11434/api/generate -d '{
     "model": "llama3.1",
     "prompt": "Hello",
     "stream": false
   }'
   ```

3. Check if Ollama is on a different port:
   ```bash
   export OLLAMA_BASE_URL=http://localhost:11434
   ```

### Model Not Available

**Error:** Health check shows `model_available: false`

**Solutions:**
1. Pull the model:
   ```bash
   ollama pull selcuk_ai_assistant
   # or
   ollama pull llama3.1
   ```

2. Update the model name in `.env`:
   ```bash
   OLLAMA_MODEL=llama3.1
   ```

3. Check available models:
   ```bash
   curl http://localhost:11434/api/tags
   ```

### Turkish Character Issues

**Problem:** Garbled Turkish characters (Ä±, Å, etc.)

**Solutions:**
- Ensure terminal supports UTF-8:
  ```bash
  export LANG=tr_TR.UTF-8
  # or
  export LANG=en_US.UTF-8
  ```

- On Windows, use UTF-8 code page:
  ```cmd
  chcp 65001
  ```

- The backend automatically configures UTF-8 encoding

### Timeout Errors

**Error:** `Ollama isteği zaman aşımına uğradı`

**Solutions:**
1. Increase timeout:
   ```bash
   export OLLAMA_TIMEOUT=180
   ```

2. Check GPU/CPU performance
3. Verify model is fully loaded in Ollama

### CORS Issues

**Problem:** Flutter app cannot connect

**Solutions:**
1. For development, allow all origins:
   ```bash
   export ALLOWED_ORIGINS="*"
   ```

2. For production, specify exact origins:
   ```bash
   export ALLOWED_ORIGINS="https://app.example.com,https://mobile.example.com"
   ```

3. Verify CORS headers in browser console

### Rate Limiting (Future)

Currently no rate limiting is implemented. For production:
- Consider adding rate limiting middleware
- Use Redis for distributed rate limiting
- Implement API keys for access control

## 📊 Performance

### Benchmarks (Approximate)

- **Ollama Response Time:** 5-30 seconds (depends on model, prompt length, hardware)
- **API Overhead:** < 50ms
- **Streaming Latency:** Near real-time (tokens arrive as generated)

### Optimization Tips

1. **Use GPU acceleration** for Ollama (NVIDIA CUDA, Apple Metal)
2. **Adjust model size** based on hardware:
   - 7B models: 8GB+ RAM/VRAM
   - 13B models: 16GB+ RAM/VRAM
3. **Enable streaming** for better perceived performance
4. **Implement caching** for common questions (future)
5. **Use RAG** to reduce prompt size and improve accuracy

## 🔐 Security

### Current Measures
- ✅ Input validation and sanitization
- ✅ XSS prevention in user input
- ✅ CORS configuration
- ✅ No SQL injection risk (no database)
- ✅ Comprehensive error handling
- ✅ Logging for audit trails

### Recommendations for Production
- 🔲 Add API key authentication
- 🔲 Implement rate limiting
- 🔲 Use HTTPS only (reverse proxy)
- 🔲 Set up monitoring and alerts
- 🔲 Regular security updates
- 🔲 Input content filtering
- 🔲 DDoS protection

## 📝 Contributing

This is a graduation project. For contributions:

1. **Code Style:** Follow PEP 8
2. **Type Hints:** Required for all functions
3. **Docstrings:** Use Google style
4. **Testing:** Add tests for new features
5. **Logging:** Use structured logging
6. **Error Handling:** Comprehensive with proper status codes

## 📄 License

This is a university graduation project for Selçuk University.

## 🙏 Acknowledgments

- **Ollama** for local LLM inference
- **FastAPI** for the web framework
- **Selçuk University** for project support

## 📞 Support

For issues related to:
- **Ollama:** https://github.com/ollama/ollama/issues
- **FastAPI:** https://fastapi.tiangolo.com/
- **This Project:** Create an issue in the GitHub repository

---

**Built with ❤️ for Selçuk University students**
