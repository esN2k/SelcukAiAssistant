# Migration Guide: Google Gemini to Ollama

This guide helps you migrate from using Google Gemini API to a local Ollama instance with llama3.1
model.

## Overview

**Before:** The Flutter app directly called Google Gemini API using the `google_generative_ai`
package.

**After:** The Flutter app calls a local FastAPI backend, which then forwards requests to a local
Ollama instance.

## Architecture Changes

```
Before:
Flutter App → Google Gemini API (Cloud)

After:
Flutter App → FastAPI Backend → Ollama (Local)
```

## Benefits

1. **Privacy**: All AI processing happens locally - no data sent to external services
2. **Cost**: No API usage fees
3. **Control**: Full control over the AI model and its behavior
4. **Offline**: Works without internet connection (after initial setup)

## Prerequisites

Before starting the migration, ensure you have:

- Python 3.8 or higher installed
- Ollama installed on your system
- At least 8GB of RAM (for running llama3.1)
- Sufficient disk space (~4GB for llama3.1 model)

## Step-by-Step Migration

### Step 1: Install Ollama

1. Download and install Ollama from [https://ollama.ai](https://ollama.ai)
2. Verify installation:

   ```bash
   ollama --version
   ```

### Step 2: Download llama3.1 Model

```bash
ollama pull llama3.1
```

This will download the ~4GB model file. Wait for it to complete.

### Step 3: Verify Ollama is Running

```bash
ollama list
```

You should see `llama3.1` in the list.

### Step 4: Set Up the Backend

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create a Python virtual environment (recommended):

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Linux/Mac:

     ```bash
     source venv/bin/activate
     ```

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. (Optional) Configure environment variables:

   ```bash
   cp .env.example .env
   # Edit .env if you need custom configuration
   ```

### Step 5: Start the Backend

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### Step 6: Test the Backend

Open a new terminal and test the API:

```bash
# Health check
curl http://localhost:8000/

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Merhaba, nasılsın?"}'
```

You should receive a JSON response with an `answer` field.

### Step 7: Configure the Flutter App

1. Create or update the `.env` file in the Flutter project root:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set:

   ```
   BACKEND_URL=http://localhost:8000
   ```

   **Note**: For Android emulator, use `http://10.0.2.2:8000` instead of `localhost`.

   **Note**: For iOS simulator, `localhost` should work.

   **Note**: For physical devices, use your computer's IP address (e.g.,
   `http://192.168.1.100:8000`).

### Step 8: Update Flutter Dependencies

The `google_generative_ai` package has been removed from `pubspec.yaml`. Update your dependencies:

```bash
flutter pub get
```

### Step 9: Run the Flutter App

```bash
flutter run
```

## Configuration

### Backend Configuration (backend/.env)

- `OLLAMA_URL`: Ollama API endpoint (default: `http://localhost:11434/api/generate`)
- `OLLAMA_MODEL`: Model to use (default: `llama3.1`)
- `OLLAMA_TIMEOUT`: Request timeout in seconds (default: `30`)
- `ALLOWED_ORIGINS`: CORS allowed origins (default: `*` for development)
- `PORT`: Backend server port (default: `8000`)

### Flutter Configuration (.env)

- `BACKEND_URL`: Backend API URL (default: `http://localhost:8000`)

## Troubleshooting

### Backend Issues

**Problem**: "Ollama servisine bağlanılamadı"

**Solution**:

1. Verify Ollama is running: `ollama list`
2. Check if the Ollama URL is correct in backend/.env
3. Try accessing Ollama directly:

   ```bash
   curl http://localhost:11434/api/generate -d '{
     "model": "llama3.1",
     "prompt": "Hello",
     "stream": false
   }'
   ```

**Problem**: Backend not starting

**Solution**:

1. Verify Python dependencies are installed: `pip list | grep fastapi`
2. Check if port 8000 is already in use: `lsof -i :8000` (Linux/Mac) or
   `netstat -ano | findstr :8000` (Windows)
3. Try a different port: `PORT=8001 python main.py`

### Flutter App Issues

**Problem**: "Backend servisine bağlanılamadı"

**Solution**:

1. Verify backend is running: `curl http://localhost:8000/`
2. Check BACKEND_URL in .env:
   - For emulator: Use `http://10.0.2.2:8000` (Android) or `http://localhost:8000` (iOS)
   - For physical device: Use your computer's IP address
3. Ensure firewall allows connections to port 8000

**Problem**: CORS errors in web/browser

**Solution**:

1. Update backend/.env and set ALLOWED_ORIGINS to your Flutter web app URL
2. Restart the backend

### Performance Issues

**Problem**: Slow response times

**Solution**:

1. Reduce OLLAMA_TIMEOUT if responses are taking too long
2. Consider using a smaller model if your hardware is limited
3. Ensure Ollama is running on a machine with sufficient resources

## Production Deployment

For production deployment:

1. **Security**:
   - Set specific CORS origins instead of `*`
   - Use HTTPS for the backend API
   - Consider adding authentication

2. **Performance**:
   - Use multiple uvicorn workers: `uvicorn main:app --workers 4`
   - Consider using a reverse proxy (nginx, Apache)
   - Monitor resource usage

3. **Reliability**:
   - Set up systemd service (Linux) or equivalent for auto-restart
   - Implement logging and monitoring
   - Configure appropriate timeouts

4. **Flutter App**:
   - Update BACKEND_URL to point to your production backend
   - Handle network errors gracefully
   - Consider adding retry logic

## Rollback Plan

If you need to roll back to Google Gemini:

1. Revert the changes in `lib/apis/apis.dart`
2. Add back `google_generative_ai: ^0.4.7` to `pubspec.yaml`
3. Run `flutter pub get`
4. Restore your Gemini API key in `.env`

## Uninstalling Old Dependencies

You can remove the Google Gemini SDK if no longer needed:

```bash
# The package is already removed from pubspec.yaml
# Just clean up:
flutter pub get
flutter clean
```

## Getting Help

If you encounter issues:

1. Check the logs:
   - Backend: Check terminal output where backend is running
   - Flutter: Check debug console in your IDE

2. Verify versions:
   - Python: `python --version` (should be 3.8+)
   - Ollama: `ollama --version`
   - Flutter: `flutter --version`

3. Review documentation:
   - Backend: See `backend/README.md`
   - Ollama: [https://ollama.ai/docs](https://ollama.ai/docs)

## Next Steps

After successful migration:

1. Test all app features thoroughly
2. Monitor response quality and adjust prompts if needed
3. Consider fine-tuning the model for your specific use case
4. Set up proper error handling and user feedback
5. Plan for production deployment if applicable

## Summary of Changes

### Removed Files/Dependencies

- ❌ `google_generative_ai` package dependency

### Added Files

- ✅ `backend/main.py` - FastAPI backend
- ✅ `backend/requirements.txt` - Python dependencies
- ✅ `backend/.env.example` - Backend configuration template
- ✅ `backend/README.md` - Backend documentation
- ✅ `.env.example` - Flutter configuration template
- ✅ `MIGRATION.md` - This migration guide

### Modified Files

- ✏️ `lib/apis/apis.dart` - Changed from Gemini to HTTP calls
- ✏️ `lib/helper/global.dart` - Added BACKEND_URL configuration
- ✏️ `pubspec.yaml` - Removed google_generative_ai dependency
- ✏️ `.gitignore` - Added Python-related exclusions

## Command Reference

### Backend Commands

```bash
# Start backend (development)
cd backend
python main.py

# Start backend with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start backend (production)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Test backend
curl http://localhost:8000/
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"question":"test"}'
```

### Ollama Commands

```bash
# List models
ollama list

# Pull a model
ollama pull llama3.1

# Test Ollama directly
ollama run llama3.1 "Hello"

# Check Ollama service status
curl http://localhost:11434/api/tags
```

### Flutter Commands

```bash
# Get dependencies
flutter pub get

# Run app
flutter run

# Build for release
flutter build apk
flutter build ios
flutter build web
```
