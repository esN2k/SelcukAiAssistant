# Architecture Comparison

## Before Migration

```
┌─────────────────┐
│                 │
│  Flutter App    │
│  (Mobile/Web)   │
│                 │
└────────┬────────┘
         │ HTTP
         │ google_generative_ai
         │
         v
┌─────────────────┐
│                 │
│  Google Gemini  │
│  API (Cloud)    │
│                 │
└─────────────────┘
```

**Limitations:**

- ❌ Data sent to external services (privacy concerns)
- ❌ Requires API key and costs money
- ❌ Requires internet connection
- ❌ Subject to API rate limits
- ❌ No control over model behavior

---

## After Migration

```
┌─────────────────┐
│                 │
│  Flutter App    │
│  (Mobile/Web)   │
│                 │
└────────┬────────┘
         │ HTTP
         │ POST /chat
         │
         v
┌─────────────────┐
│                 │
│  FastAPI        │
│  Backend        │
│  (Python)       │
│                 │
└────────┬────────┘
         │ HTTP
         │ POST /api/generate
         │
         v
┌─────────────────┐
│                 │
│  Ollama         │
│  (Local)        │
│  llama3.1       │
│                 │
└─────────────────┘
```

**Benefits:**

- ✅ All processing happens locally (privacy)
- ✅ No API costs
- ✅ Works offline (after model download)
- ✅ Full control over model and behavior
- ✅ No rate limits
- ✅ Configurable and extensible

---

## Component Details

### 1. Flutter App

**Location:** Mobile device, web browser, or desktop  
**Language:** Dart  
**Changes:**

- Removed: `google_generative_ai` package
- Modified: `lib/apis/apis.dart` to make HTTP POST requests
- Added: `BACKEND_URL` configuration in `.env`

**API Contract:**

```dart
// Request
{
  "question": "Selçuk Üniversitesi'nin kuruluş tarihi nedir?"
}

// Response
{
  "answer": "Selçuk Üniversitesi, 1975 yılında kurulmuştur..."
}
```

### 2. FastAPI Backend (NEW)

**Location:** Developer's machine or server  
**Language:** Python  
**Port:** 8000 (configurable)  

**Responsibilities:**

1. Receives chat requests from Flutter app
2. Formats prompts with Turkish context
3. Forwards requests to Ollama
4. Handles errors and timeouts
5. Returns formatted responses

**Configuration (via .env):**

- `OLLAMA_URL` - Where Ollama is running
- `OLLAMA_MODEL` - Which model to use
- `OLLAMA_TIMEOUT` - Request timeout
- `ALLOWED_ORIGINS` - CORS configuration
- `PORT` - Server port

**Endpoints:**

- `GET /` - Health check
- `POST /chat` - Main chat endpoint
- `GET /docs` - Interactive API documentation

### 3. Ollama (NEW)

**Location:** Developer's machine or server  
**Language:** Go (Ollama runtime)  
**Port:** 11434 (default)  
**Model:** llama3.1 (~4GB)

**Responsibilities:**

1. Runs large language models locally
2. Processes prompts and generates responses
3. Manages model loading and inference

**Installation:**

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Download model
ollama pull llama3.1

# Verify
ollama list
```

---

## Data Flow

### Chat Request Flow

```
1. User types question in Flutter app
   ↓
2. Flutter sends POST /chat to FastAPI backend
   {
     "question": "user's question"
   }
   ↓
3. Backend formats prompt with Turkish context
   ↓
4. Backend sends POST /api/generate to Ollama
   {
     "model": "llama3.1",
     "prompt": "formatted prompt with context",
     "stream": false
   }
   ↓
5. Ollama processes request with llama3.1 model
   ↓
6. Ollama returns response
   {
     "response": "AI generated answer"
   }
   ↓
7. Backend extracts answer and returns to Flutter
   {
     "answer": "AI generated answer"
   }
   ↓
8. Flutter displays answer to user
```

### Error Handling Flow

```
Error at Ollama level
   ↓
Backend catches error (timeout, connection, etc.)
   ↓
Backend returns appropriate HTTP error
   - 503: Service unavailable
   - 504: Timeout
   - 500: Internal error
   ↓
Flutter displays user-friendly error message
```

---

## Deployment Scenarios

### Development (Current Setup)

```
[Flutter Dev] ←→ [FastAPI localhost:8000] ←→ [Ollama localhost:11434]
```

### Production - All on One Server

```
[Flutter Web] ←→ [FastAPI server:8000] ←→ [Ollama server:11434]
```

### Production - Distributed

```
[Flutter Mobile App] 
         ↓
[FastAPI on Server A:8000]
         ↓
[Ollama on Server B:11434]
```

### Development - Multiple Devices

```
[Flutter on Phone]
         ↓ (WiFi)
[FastAPI on Computer:8000]
         ↓ (localhost)
[Ollama on Computer:11434]
```

---

## Network Configuration

### For Android Emulator

```
BACKEND_URL=http://10.0.2.2:8000
```

(10.0.2.2 is the special alias to host machine)

### For iOS Simulator

```
BACKEND_URL=http://localhost:8000
```

(localhost works on iOS simulator)

### For Physical Device

```
BACKEND_URL=http://192.168.1.100:8000
```

(Use your computer's actual IP address)

### For Production

```
BACKEND_URL=https://your-backend.com
```

(Use HTTPS in production!)

---

## Security Considerations

### Development

- ✅ CORS allows all origins (`*`)
- ✅ No authentication needed
- ✅ HTTP is acceptable

### Production

- ⚠️ Set specific CORS origins
- ⚠️ Add authentication (JWT, OAuth, etc.)
- ⚠️ Use HTTPS for all connections
- ⚠️ Add rate limiting
- ⚠️ Monitor resource usage

---

## Performance Metrics

### Before (Google Gemini)

- Network latency: 200-1000ms
- Response time: 1-3 seconds
- Depends on internet speed
- Subject to API rate limits

### After (Ollama)

- Network latency: 1-10ms (local)
- Response time: 2-5 seconds (first run, model loading)
- Response time: 0.5-2 seconds (subsequent requests)
- No rate limits
- Depends on local hardware

---

## Resource Requirements

### Backend (FastAPI)

- **CPU:** Minimal (< 5%)
- **RAM:** ~50-100 MB
- **Disk:** ~10 MB

### Ollama + llama3.1

- **CPU:** 20-50% during inference
- **RAM:** 8-16 GB recommended
- **Disk:** ~4 GB for model
- **GPU:** Optional (significantly faster with GPU)

---

## Maintenance

### Backend Updates

```bash
cd backend
pip install -r requirements.txt --upgrade
pytest test_main.py  # Verify tests pass
```

### Ollama Updates

```bash
# Update Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Update model
ollama pull llama3.1
```

### Flutter App Updates

```bash
flutter pub get
flutter pub upgrade
```

---

## Monitoring

### Backend Health

```bash
curl http://localhost:8000/
```

### Ollama Health

```bash
curl http://localhost:11434/api/tags
```

### Full System Test

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Test question"}'
```

---

## Troubleshooting Quick Reference

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| Backend won't start | Port in use | Change PORT in .env |
| Can't connect to Ollama | Ollama not running | `ollama list` to start |
| Flutter can't reach backend | Wrong URL | Check BACKEND_URL in .env |
| Slow responses | Model loading | Normal on first request |
| Out of memory | Insufficient RAM | Use smaller model or add RAM |
| CORS errors | Origins not allowed | Update ALLOWED_ORIGINS |

---

For detailed instructions, see:

- **MIGRATION.md** - Step-by-step migration guide
- **SUMMARY.md** - Quick start reference
- **backend/README.md** - Backend setup details
