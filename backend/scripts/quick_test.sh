#!/bin/bash

# ============================================================
# DOSYA ADI: quick_test.sh
# AMAÇ: Pipeline öncesi hızlı sistem kontrolü yapmak
# NE YAPAR:
#   - Backend/frontend bağımlılıklarını kontrol eder
#   - Servis durumlarını test eder
#   - Temel fonksiyonaliteleri doğrular
# KULLANIM: bash backend/scripts/quick_test.sh
# SON DEĞİŞİKLİK: 17.01.2026
# ============================================================

set -euo pipefail

# Renkler
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

FAILED_TESTS=0
TOTAL_TESTS=0

# Test fonksiyonu
run_test() {
  local test_name="$1"
  local test_command="$2"
  
  TOTAL_TESTS=$((TOTAL_TESTS + 1))
  
  echo -ne "${BLUE}[${TOTAL_TESTS}] ${test_name}${NC} ... "
  
  if eval "$test_command" &> /dev/null; then
    echo -e "${GREEN}✅ BAŞARILI${NC}"
    return 0
  else
    echo -e "${RED}❌ BAŞARISIZ${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
    return 1
  fi
}

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     SELÇUK ÜNİVERSİTESİ AI ASİSTAN HIZLI TEST            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

# ============================================================
# PYTHON ENVIRONMENT
# ============================================================
echo -e "${YELLOW}🐍 Python Environment${NC}\n"

run_test "Python yüklü mü?" "command -v python3"
run_test "pip yüklü mü?" "command -v pip"
run_test "venv modülü mevcut mu?" "python3 -c 'import venv'"

echo ""

# ============================================================
# BACKEND DEPENDENCIES
# ============================================================
echo -e "${YELLOW}📦 Backend Dependencies${NC}\n"

run_test "FastAPI yüklü mü?" "python3 -c 'import fastapi'"
run_test "Uvicorn yüklü mü?" "python3 -c 'import uvicorn'"
run_test "Pydantic yüklü mü?" "python3 -c 'import pydantic'"
run_test "LangChain yüklü mü?" "python3 -c 'import langchain'"

echo ""

# ============================================================
# AI/ML DEPENDENCIES
# ============================================================
echo -e "${YELLOW}🤖 AI/ML Dependencies${NC}\n"

run_test "Ollama yüklü mü?" "command -v ollama"
run_test "PyTorch yüklü mü?" "python3 -c 'import torch'"
run_test "Transformers yüklü mü?" "python3 -c 'import transformers'"
run_test "Sentence Transformers yüklü mü?" "python3 -c 'import sentence_transformers'"

echo ""

# ============================================================
# BACKEND FILES
# ============================================================
echo -e "${YELLOW}📄 Backend Files${NC}\n"

run_test "main.py exists?" "test -f backend/main.py"
run_test "config.py exists?" "test -f backend/config.py"
run_test "prompts.py exists?" "test -f backend/prompts.py"
run_test "rag_service.py exists?" "test -f backend/rag_service.py"

echo ""

# ============================================================
# SCRIPTS
# ============================================================
echo -e "${YELLOW}📜 Scripts${NC}\n"

run_test "master_model_pipeline.sh exists?" "test -f backend/scripts/master_model_pipeline.sh"
run_test "benchmark_model.py exists?" "test -f backend/scripts/benchmark_model.py"
run_test "master_model_pipeline.sh executable?" "test -x backend/scripts/master_model_pipeline.sh"

echo ""

# ============================================================
# DATA FILES
# ============================================================
echo -e "${YELLOW}📊 Data Files${NC}\n"

run_test "test_questions.json exists?" "test -f backend/data/test_questions.json"
run_test "selcuk_knowledge_base.json exists?" "test -f backend/data/selcuk_knowledge_base.json"
run_test "test_questions.json valid JSON?" "python3 -c 'import json; json.load(open(\"backend/data/test_questions.json\"))'"

echo ""

# ============================================================
# FLUTTER ENVIRONMENT (Optional)
# ============================================================
echo -e "${YELLOW}📱 Flutter Environment (Optional)${NC}\n"

if command -v flutter &> /dev/null; then
  run_test "Flutter yüklü mü?" "command -v flutter"
  run_test "Flutter doctor check" "flutter doctor --android-licenses || true"
else
  echo -e "${YELLOW}⚠️  Flutter not installed (optional)${NC}"
fi

echo ""

# ============================================================
# SERVICES STATUS
# ============================================================
echo -e "${YELLOW}🔧 Services Status${NC}\n"

if pgrep -x "ollama" > /dev/null; then
  echo -e "${GREEN}✅ Ollama service is running${NC}"
else
  echo -e "${YELLOW}⚠️  Ollama service is not running${NC}"
  echo -e "   Start with: ${BLUE}ollama serve${NC}"
fi

# Check if backend is running
if curl -s http://localhost:8000/health &> /dev/null; then
  echo -e "${GREEN}✅ Backend API is running${NC}"
else
  echo -e "${YELLOW}⚠️  Backend API is not running${NC}"
  echo -e "   Start with: ${BLUE}cd backend && uvicorn main:app --reload${NC}"
fi

echo ""

# ============================================================
# FINAL SUMMARY
# ============================================================
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    TEST SONUÇLARI                          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}\n"

PASSED_TESTS=$((TOTAL_TESTS - FAILED_TESTS))
SUCCESS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))

echo -e "Toplam Test: ${BLUE}${TOTAL_TESTS}${NC}"
echo -e "Başarılı: ${GREEN}${PASSED_TESTS}${NC}"
echo -e "Başarısız: ${RED}${FAILED_TESTS}${NC}"
echo -e "Başarı Oranı: ${YELLOW}${SUCCESS_RATE}%${NC}\n"

if [ $FAILED_TESTS -eq 0 ]; then
  echo -e "${GREEN}✨ Tüm testler başarılı! Sistem hazır.${NC}\n"
  exit 0
else
  echo -e "${RED}⚠️  Bazı testler başarısız. Lütfen eksiklikleri giderin.${NC}\n"
  exit 1
fi
