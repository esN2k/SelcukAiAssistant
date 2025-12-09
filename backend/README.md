# SelcukAiAssistant Backend

This is the FastAPI backend for SelcukAiAssistant that uses a local Ollama instance with llama3.1 model.

## Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running locally
3. **llama3.1 model** downloaded in Ollama

## Setup

### 1. Install Ollama

Download and install Ollama from [https://ollama.ai](https://ollama.ai)

### 2. Pull the llama3.1 model

```bash
ollama pull llama3.1
```

### 3. Start Ollama (if not already running)

Ollama typically runs automatically after installation. To verify:

```bash
ollama list
```

### 4. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or using a virtual environment (recommended):

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Configure Environment Variables (Optional)

Copy `.env.example` to `.env` and modify if needed:

```bash
cp .env.example .env
```

Default configuration:
- `OLLAMA_URL`: http://localhost:11434/api/generate - Ollama API endpoint
- `OLLAMA_MODEL`: llama3.1 - Model to use
- `OLLAMA_TIMEOUT`: 30 - Request timeout in seconds
- `ALLOWED_ORIGINS`: * - CORS allowed origins (use specific URLs in production)
- `HOST`: 127.0.0.1 - Server host (use 0.0.0.0 to allow external connections)
- `PORT`: 8000 - Server port

## Running the Backend

### Development Mode (Local Only)

```bash
cd backend
python main.py
```

This runs on `127.0.0.1:8000` (localhost only) for security.

### Development Mode (Allow External Connections)

To allow connections from other devices (e.g., mobile devices on same network):

```bash
cd backend
HOST=0.0.0.0 python main.py
```

Or using uvicorn directly:

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Endpoints

### GET /

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "SelcukAiAssistant Backend is running"
}
```

### POST /chat

Main chat endpoint that processes questions using Ollama.

**Request:**
```json
{
  "question": "Selçuk Üniversitesi'nin kuruluş tarihi nedir?"
}
```

**Response:**
```json
{
  "answer": "Selçuk Üniversitesi, 1975 yılında kurulmuştur..."
}
```

**Error Responses:**
- `503`: Ollama service unavailable
- `504`: Request timeout
- `500`: Internal server error

## Testing the API

### Running Unit Tests

The backend includes unit tests that verify the API contract without requiring Ollama:

```bash
cd backend
pip install -r requirements-dev.txt
pytest test_main.py -v
```

All tests should pass:
- ✅ Health check endpoint
- ✅ Successful chat response
- ✅ Connection error handling
- ✅ Invalid request handling
- ✅ Empty response handling
- ✅ Prompt formatting

### Using curl

```bash
# Health check
curl http://localhost:8000/

# Chat request
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Merhaba, nasılsın?"}'
```

### Using the Interactive Documentation

Navigate to http://localhost:8000/docs and test the endpoints interactively.

## Troubleshooting

### Ollama Connection Issues

If you get "Ollama servisine bağlanılamadı" error:

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

3. Check if the port is correct (default is 11434)

### Model Not Found

If Ollama returns a model not found error:

```bash
ollama pull llama3.1
```

### CORS Issues

If the Flutter app cannot connect, ensure CORS is properly configured in `main.py`. For production, update the `allow_origins` list with your Flutter app's URL.

## Deployment

For production deployment, consider:

1. Using a production ASGI server (uvicorn with workers)
2. Setting up proper CORS origins
3. Adding authentication if needed
4. Using environment variables for configuration
5. Setting up monitoring and logging

Example production command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Migration Notes

### Removed Dependencies

The following package is no longer needed and can be uninstalled:

```bash
# In your Flutter project
flutter pub remove google_generative_ai
```

### Flutter App Changes

The Flutter app now calls this backend instead of directly calling Google Gemini. The API contract remains the same - it accepts a question and returns an answer.
