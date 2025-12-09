# Quick Start Commands

This file contains all the commands you need to get started with the migrated codebase.

## Prerequisites Installation

### 1. Install Ollama
```bash
# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# macOS
brew install ollama

# Windows
# Download from https://ollama.ai/download/windows
```

### 2. Pull llama3.1 Model
```bash
ollama pull llama3.1
```

### 3. Verify Ollama Installation
```bash
ollama list
```
Expected output: You should see `llama3.1` in the list.

---

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment (Recommended)
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment (Optional)
```bash
cp .env.example .env
# Edit .env if you need custom configuration
```

### 5. Run Backend
```bash
python main.py
```

Expected output:
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Keep this terminal open - the backend needs to stay running!

---

## Test Backend (New Terminal)

### 1. Health Check
```bash
curl http://localhost:8000/
```

Expected output:
```json
{"status":"ok","message":"SelcukAiAssistant Backend is running"}
```

### 2. Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Merhaba, nasılsın?"}'
```

Expected output:
```json
{"answer":"Merhaba! ... (response from AI)"}
```

### 3. View API Documentation
Open in browser: http://localhost:8000/docs

---

## Flutter App Setup

### 1. Return to Project Root
```bash
# If you're in backend/ directory
cd ..
```

### 2. Create Configuration File
```bash
cp .env.example .env
```

### 3. Edit .env File

Open `.env` and set the correct BACKEND_URL:

**For Android Emulator:**
```
BACKEND_URL=http://10.0.2.2:8000
```

**For iOS Simulator:**
```
BACKEND_URL=http://localhost:8000
```

**For Physical Device:**
```
BACKEND_URL=http://YOUR_COMPUTER_IP:8000
```
Replace `YOUR_COMPUTER_IP` with your actual IP address.

To find your IP:
```bash
# Linux/macOS
ifconfig | grep "inet " | grep -v 127.0.0.1

# Windows
ipconfig | findstr "IPv4"
```

### 4. Update Flutter Dependencies
```bash
flutter pub get
```

### 5. Clean Previous Build (Optional)
```bash
flutter clean
```

### 6. Run Flutter App
```bash
flutter run
```

---

## Running Backend Unit Tests

```bash
cd backend
pip install -r requirements-dev.txt
pytest test_main.py -v
```

Expected output: 6 tests should pass.

---

## Stopping Services

### Stop Backend
In the terminal where backend is running:
- Press `Ctrl+C`

### Stop Ollama (if needed)
```bash
# Linux/macOS
pkill ollama

# Windows
# Stop from Task Manager or close terminal
```

---

## Production Deployment Commands

### Backend (Production)
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run with multiple workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Configure Production Settings
Create `backend/.env`:
```bash
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3.1
OLLAMA_TIMEOUT=30
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
PORT=8000
```

---

## Useful Commands Reference

### Check if ports are in use
```bash
# Linux/macOS
lsof -i :8000  # Backend
lsof -i :11434 # Ollama

# Windows
netstat -ano | findstr :8000  # Backend
netstat -ano | findstr :11434 # Ollama
```

### View Backend Logs
Backend logs are printed to the terminal where you ran `python main.py`.

### Restart Backend
```bash
# Stop with Ctrl+C, then:
python main.py
```

### Update Ollama Model
```bash
ollama pull llama3.1
```

### List Running Ollama Models
```bash
ollama list
```

---

## Troubleshooting Commands

### Test Ollama Directly
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1",
  "prompt": "Hello",
  "stream": false
}'
```

### Test with Different Model
```bash
# Edit backend/.env or set environment variable
export OLLAMA_MODEL=llama3.1
python main.py
```

### Check Python Version
```bash
python --version  # Should be 3.8+
```

### Check Flutter Version
```bash
flutter --version
```

### View Backend Dependencies
```bash
cd backend
pip list
```

---

## Complete Fresh Start (If Something Goes Wrong)

### 1. Stop Everything
```bash
# Stop backend: Ctrl+C in backend terminal
# Stop Flutter: Ctrl+C in Flutter terminal
```

### 2. Clean Backend
```bash
cd backend
rm -rf venv __pycache__ .pytest_cache
```

### 3. Reinstall Backend
```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 4. Clean Flutter
```bash
cd ..
flutter clean
flutter pub get
```

### 5. Verify Ollama
```bash
ollama list
ollama pull llama3.1  # if not present
```

### 6. Restart Everything
```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate  # if using venv
python main.py

# Terminal 2: Test backend
curl http://localhost:8000/

# Terminal 3: Run Flutter
flutter run
```

---

## Quick Reference

| Component | Command | Port |
|-----------|---------|------|
| Ollama | `ollama pull llama3.1` | 11434 |
| Backend | `python main.py` | 8000 |
| Backend Tests | `pytest test_main.py -v` | - |
| Flutter | `flutter run` | - |
| API Docs | Open browser | http://localhost:8000/docs |

---

## Next Steps After Setup

1. ✅ Verify backend is running: `curl http://localhost:8000/`
2. ✅ Test chat endpoint with curl
3. ✅ Configure Flutter `.env` with correct BACKEND_URL
4. ✅ Run Flutter app
5. ✅ Test chat functionality in the app
6. 📖 Read MIGRATION.md for detailed information
7. 📖 Read ARCHITECTURE.md to understand the system

---

## Getting Help

If you encounter issues:
1. Check the logs in the terminal where backend is running
2. Verify all services are running (Ollama, Backend)
3. Check your BACKEND_URL configuration
4. See MIGRATION.md "Troubleshooting" section
5. Run unit tests: `cd backend && pytest test_main.py -v`

---

## Uninstalling (If Needed)

### Remove Backend
```bash
cd backend
rm -rf venv __pycache__
```

### Revert Flutter Changes
```bash
# This migration is already committed
# To revert, you would need to restore from git history
git log --oneline  # Find commit before migration
git checkout <commit-hash> -- lib/apis/apis.dart lib/helper/global.dart pubspec.yaml
```

### Remove Ollama
```bash
# Linux
sudo rm -rf /usr/local/bin/ollama /usr/share/ollama ~/.ollama

# macOS
brew uninstall ollama
rm -rf ~/.ollama

# Windows
# Uninstall from Control Panel
```

---

**You're all set!** 🎉

Follow the commands above in order, and you'll have the system up and running in minutes.
