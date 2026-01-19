#!/bin/bash

# ============================================
# Selçuk AI Asistan - Tez Demo Başlatma
# ============================================

echo "============================================================"
echo "🎓 Selçuk AI Asistan - Tez Demo Başlatılıyor"
echo "============================================================"
echo ""

PROJECT_ROOT="/e/SelcukAiAssistant/repo"
BACKEND_DIR="$PROJECT_ROOT/backend"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Sistem Kontrolleri
echo -e "${YELLOW}🔍 Sistem kontrolleri...${NC}"

# Python
echo -n "   Checking Python... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python bulunamadı!${NC}"
    exit 1
fi

# Ollama
echo -n "   Checking Ollama... "
if pgrep -x "ollama" > /dev/null; then
    echo -e "${GREEN}✅ Çalışıyor${NC}"
else
    echo -e "${YELLOW}⚠️  Başlatılıyor...${NC}"
    ollama serve &
    sleep 3
fi

# Models
echo -n "   Checking Models... "
if ollama list | grep -q "llama" && ollama list | grep -q "translategemma"; then
    echo -e "${GREEN}✅ Llama + TranslateGemma yüklü${NC}"
elif ollama list | grep -q "llama"; then
    echo -e "${YELLOW}⚠️  TranslateGemma eksik${NC}"
    echo "   Kurulum için: python backend/install_translation.py"
else
    echo -e "${YELLOW}⚠️  Modeller bulunamadı${NC}"
fi

echo ""

# 2. Backend Başlatma
echo -e "${YELLOW}🔧 Backend başlatılıyor...${NC}"
cd "$BACKEND_DIR"

# Virtual environment
if [ -f "venv/bin/activate" ]; then
    echo "   Activating venv..."
    source venv/bin/activate
fi

# Backend'i arka planda başlat
echo "   Starting FastAPI server..."
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

sleep 5

# Health check
echo -n "   Health check... "
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ Backend hazır${NC}"
else
    echo -e "${RED}❌ Backend başlatılamadı!${NC}"
    kill $BACKEND_PID
    exit 1
fi

echo ""

# 3. API Docs
echo -e "${YELLOW}📖 API Dokümantasyonu açılıyor...${NC}"
if command -v xdg-open &> /dev/null; then
    xdg-open "http://localhost:8000/docs" 2>/dev/null
elif command -v open &> /dev/null; then
    open "http://localhost:8000/docs"
fi
echo -e "   ${GREEN}✅ http://localhost:8000/docs${NC}"

echo ""

# 4. Demo Bilgileri
echo "============================================================"
echo -e "${GREEN}✅ TÜM SERVİSLER HAZIR!${NC}"
echo "============================================================"
echo ""
echo -e "${YELLOW}📍 Erişim Noktaları:${NC}"
echo "   Backend API:  http://localhost:8000"
echo "   API Docs:     http://localhost:8000/docs"
echo "   Health Check: http://localhost:8000/health"
echo ""
echo -e "${YELLOW}🎯 Demo Test Komutları:${NC}"
echo "   1. Chat Test:"
echo '   curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '"'"'{"message":"Teknoloji Fakültesinde kaç bölüm var?"}'"'"
echo ""
echo "   2. Translation Test (TranslateGemma 4B):"
echo '   curl -X POST http://localhost:8000/translate -H "Content-Type: application/json" -d '"'"'{"text":"Yapay Zeka","source_lang":"tr","target_lang":"en"}'"'"
echo ""
echo -e "${RED}⏹️  Durdurmak için: Ctrl+C${NC}"
echo "============================================================"

# Trap SIGINT
trap "echo ''; echo 'Servisler durduruluyor...'; kill $BACKEND_PID; exit" INT

# Wait
wait $BACKEND_PID
