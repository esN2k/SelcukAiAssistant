#!/bin/bash

# ============================================================
# DOSYA ADI: master_model_pipeline.sh
# AMAÇ: Model geliştirme pipeline'ını tek komutla çalıştırmak
# NE YAPAR:
#   1. Model değerlendirme yapar
#   2. Dataset hazırlar
#   3. Fine-tuning yapar
#   4. Ollama'ya deploy eder
#   5. Test eder ve rapor oluşturur
# KULLANIM:
#   bash backend/scripts/master_model_pipeline.sh [--skip-eval] [--skip-training]
# SON DEĞİŞİKLİK: 17.01.2026
# ============================================================

set -e  # Hata durumunda dur

# Renkli output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     SELÇUK ÜNİVERSİTESİ AI ASİSTAN MODEL PİPELINE            ║"
echo "║     Model Seçimi → Fine-Tuning → Deployment                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

# Parametreler
SKIP_EVAL=false
SKIP_TRAINING=false
EPOCHS=3
BATCH_SIZE=4

# Argüman parse
while [[ $# -gt 0 ]]; do
  case $1 in
    --skip-eval)
      SKIP_EVAL=true
      shift
      ;;
    --skip-training)
      SKIP_TRAINING=true
      shift
      ;;
    --epochs)
      EPOCHS="$2"
      shift 2
      ;;
    --batch-size)
      BATCH_SIZE="$2"
      shift 2
      ;;
    *)
      echo -e "${RED}❌ Bilinmeyen parametre: $1${NC}"
      exit 1
      ;;
  esac
done

# Çalışma dizini
cd "$(dirname "$0")/../.."
BACKEND_DIR="$(pwd)/backend"

echo -e "${BLUE}📁 Çalışma Dizini: ${BACKEND_DIR}${NC}\n"

# Gereksinimler kontrolü
echo -e "${YELLOW}🔍 Gereksinimler kontrol ediliyor...${NC}"

check_requirement() {
  if ! command -v $1 &> /dev/null; then
    echo -e "${RED}❌ $1 bulunamadı. Lütfen kurun.${NC}"
    exit 1
  fi
  echo -e "${GREEN}✅ $1 mevcut${NC}"
}

check_requirement python
check_requirement ollama

# Python paketleri
echo -e "${YELLOW}📦 Python paketleri kontrol ediliyor...${NC}"
python -c "import torch, transformers, peft" 2>/dev/null || {
  echo -e "${RED}❌ Gerekli Python paketleri eksik${NC}"
  echo -e "${YELLOW}Kurulum için: pip install torch transformers peft bitsandbytes${NC}"
  exit 1
}
echo -e "${GREEN}✅ Python paketleri tamam${NC}\n"

# CUDA kontrolü
if command -v nvidia-smi &> /dev/null; then
  echo -e "${YELLOW}🎮 GPU Durumu:${NC}"
  nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader
  echo ""
else
  echo -e "${YELLOW}⚠️  CUDA bulunamadı, CPU modunda çalışılacak (çok yavaş!)${NC}\n"
fi

# ============================================================
# ADIM 1: MODEL DEĞERLENDİRME
# ============================================================

if [ "$SKIP_EVAL" = false ]; then
  echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
  echo -e "${BLUE}║  ADIM 1/5: Model Değerlendirme        ║${NC}"
  echo -e "${BLUE}╚════════════════════════════════════════╝${NC}\n"
  
  if [ -f "$BACKEND_DIR/models/evaluation_report.json" ]; then
    echo -e "${YELLOW}⚠️  Mevcut evaluation_report.json bulundu${NC}"
    read -p "Yeni değerlendirme yapmak istiyor musunuz? (e/h): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ee]$ ]]; then
      echo -e "${GREEN}✅ Mevcut rapor kullanılacak${NC}\n"
    else
      python "$BACKEND_DIR/scripts/model_evaluation.py" || {
        echo -e "${RED}❌ Model değerlendirme başarısız${NC}"
        exit 1
      }
    fi
  else
    python "$BACKEND_DIR/scripts/model_evaluation.py" || {
      echo -e "${RED}❌ Model değerlendirme başarısız${NC}"
      exit 1
    }
  fi
  
  # En iyi modeli göster
  BEST_MODEL=$(python -c "import json; data=json.load(open('$BACKEND_DIR/models/evaluation_report.json')); print(max(data, key=lambda x: x['overall_score'])['model_name'])")
  echo -e "${GREEN}🏆 Seçilen Model: ${BEST_MODEL}${NC}\n"
else
  echo -e "${YELLOW}⏭️  Model değerlendirme atlandı${NC}\n"
fi

# ============================================================
# ADIM 2: DATASET HAZIRLAMA
# ============================================================

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  ADIM 2/5: Dataset Hazırlama          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}\n"

if [ -f "$BACKEND_DIR/data/fine_tuning/train.json" ]; then
  TRAIN_SIZE=$(python -c "import json; print(len(json.load(open('$BACKEND_DIR/data/fine_tuning/train.json'))))")
  echo -e "${YELLOW}⚠️  Mevcut dataset bulundu (${TRAIN_SIZE} örnek)${NC}"
  read -p "Yeni dataset oluşturmak istiyor musunuz? (e/h): " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Ee]$ ]]; then
    echo -e "${GREEN}✅ Mevcut dataset kullanılacak${NC}\n"
  else
    python "$BACKEND_DIR/scripts/prepare_selcuk_dataset.py" || {
      echo -e "${RED}❌ Dataset hazırlama başarısız${NC}"
      exit 1
    }
  fi
else
  python "$BACKEND_DIR/scripts/prepare_selcuk_dataset.py" || {
    echo -e "${RED}❌ Dataset hazırlama başarısız${NC}"
    exit 1
  }
fi

# Dataset istatistikleri
TRAIN_SIZE=$(python -c "import json; print(len(json.load(open('$BACKEND_DIR/data/fine_tuning/train.json'))))")
VAL_SIZE=$(python -c "import json; print(len(json.load(open('$BACKEND_DIR/data/fine_tuning/validation.json'))))")
echo -e "${GREEN}✅ Dataset hazır: ${TRAIN_SIZE} train, ${VAL_SIZE} validation${NC}\n"

# ============================================================
# ADIM 3: FINE-TUNING
# ============================================================

if [ "$SKIP_TRAINING" = false ]; then
  echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
  echo -e "${BLUE}║  ADIM 3/5: Fine-Tuning (${EPOCHS} epochs)    ║${NC}"
  echo -e "${BLUE}╚════════════════════════════════════════╝${NC}\n"
  
  if [ -d "$BACKEND_DIR/models/selcuk-assistant-v1/merged" ]; then
    echo -e "${YELLOW}⚠️  Mevcut fine-tuned model bulundu${NC}"
    read -p "Yeni eğitim yapmak istiyor musunuz? (e/h): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ee]$ ]]; then
      echo -e "${GREEN}✅ Mevcut model kullanılacak${NC}\n"
    else
      echo -e "${YELLOW}🏋️  Eğitim başlıyor (${EPOCHS} epoch, batch size: ${BATCH_SIZE})...${NC}"
      echo -e "${YELLOW}⏱️  Tahmini süre: ~$((EPOCHS * 2)) saat${NC}\n"
      
      python "$BACKEND_DIR/scripts/finetune_model.py" \
        --epochs "$EPOCHS" \
        --batch-size "$BATCH_SIZE" || {
        echo -e "${RED}❌ Fine-tuning başarısız${NC}"
        exit 1
      }
    fi
  else
    echo -e "${YELLOW}🏋️  Eğitim başlıyor (${EPOCHS} epoch, batch size: ${BATCH_SIZE})...${NC}"
    echo -e "${YELLOW}⏱️  Tahmini süre: ~$((EPOCHS * 2)) saat${NC}\n"
    
    python "$BACKEND_DIR/scripts/finetune_model.py" \
      --epochs "$EPOCHS" \
      --batch-size "$BATCH_SIZE" || {
      echo -e "${RED}❌ Fine-tuning başarısız${NC}"
      exit 1
    }
  fi
  
  # Eğitim metriklerini göster
  if [ -f "$BACKEND_DIR/models/selcuk-assistant-v1/training_metrics.json" ]; then
    echo -e "\n${GREEN}📊 Eğitim Metrikleri:${NC}"
    python -c "import json; metrics=json.load(open('$BACKEND_DIR/models/selcuk-assistant-v1/training_metrics.json')); print(f\"  Final Loss: {metrics['final_loss']:.4f}\n  Süre: {metrics['train_runtime']:.2f}s\n  Epochs: {metrics['epochs']}\")"
    echo ""
  fi
else
  echo -e "${YELLOW}⏭️  Fine-tuning atlandı${NC}\n"
fi

# ============================================================
# ADIM 4: OLLAMA DEPLOYMENT
# ============================================================

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  ADIM 4/5: Ollama Deployment          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}\n"

# Ollama çalışıyor mu kontrol et
if ! pgrep -x "ollama" > /dev/null; then
  echo -e "${YELLOW}⚠️  Ollama çalışmıyor, başlatılıyor...${NC}"
  ollama serve &
  sleep 5
fi

# Deploy et
python "$BACKEND_DIR/scripts/deploy_to_ollama.py" || {
  echo -e "${RED}❌ Ollama deployment başarısız${NC}"
  exit 1
}

echo -e "${GREEN}✅ Model Ollama'ya yüklendi: selcuk-assistant${NC}\n"

# ============================================================
# ADIM 5: TEST VE DOĞRULAMA
# ============================================================

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  ADIM 5/5: Test ve Doğrulama          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}\n"

echo -e "${YELLOW}🧪 Model test ediliyor...${NC}\n"

# Test soruları
TEST_QUESTIONS=(
  "Merhaba, sen kimsin?"
  "Selçuk Üniversitesi hangi yıl kuruldu?"
  "Bilgisayar Mühendisliği bölümü nerede?"
  "Final sınavları ne zaman başlıyor?"
  "Öğrenci işleri ofisi nasıl ulaşabilirim?"
)

PASSED=0
TOTAL=${#TEST_QUESTIONS[@]}

for i in "${!TEST_QUESTIONS[@]}"; do
  QUESTION="${TEST_QUESTIONS[$i]}"
  echo -e "${BLUE}Soru $((i+1))/${TOTAL}: ${QUESTION}${NC}"
  
  RESPONSE=$(ollama run selcuk-assistant "$QUESTION" 2>/dev/null | head -n 3)
  
  if [ -n "$RESPONSE" ]; then
    echo -e "${GREEN}✅ Cevap alındı:${NC}"
    echo "$RESPONSE" | sed 's/^/  /'
    PASSED=$((PASSED+1))
  else
    echo -e "${RED}❌ Cevap alınamadı${NC}"
  fi
  echo ""
done

# Test sonuçları
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  TEST SONUÇLARI                        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}\n"
echo -e "${GREEN}✅ Başarılı: ${PASSED}/${TOTAL}${NC}"
echo -e "${YELLOW}📊 Başarı Oranı: $((PASSED * 100 / TOTAL))%${NC}\n"

# ============================================================
# FİNAL RAPOR
# ============================================================

echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                 PİPELINE TAMAMLANDI! 🎉                   ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}\n"

echo -e "${BLUE}📌 SONRAKI ADIMLAR:${NC}\n"
echo -e "1. Backend'i yeniden başlat:"
echo -e "   ${YELLOW}cd backend && python main.py${NC}\n"

echo -e "2. Frontend'i test et:"
echo -e "   ${YELLOW}flutter run${NC}\n"

echo -e "3. TensorBoard ile eğitim loglarını incele:"
echo -e "   ${YELLOW}tensorboard --logdir backend/models/selcuk-assistant-v1/logs${NC}\n"

echo -e "4. Model performansını benchmark et:"
echo -e "   ${YELLOW}python backend/scripts/benchmark_model.py${NC}\n"

echo -e "${BLUE}📁 OLUŞTURULAN DOSYALAR:${NC}"
echo -e "  • backend/models/evaluation_report.json"
echo -e "  • backend/data/fine_tuning/train.json"
echo -e "  • backend/data/fine_tuning/validation.json"
echo -e "  • backend/models/selcuk-assistant-v1/"
echo -e "  • backend/models/selcuk-assistant-v1/merged/"
echo -e "  • backend/models/selcuk-assistant-v1/training_metrics.json"
echo -e "  • backend/Modelfile.selcuk-assistant\n"

echo -e "${BLUE}🚀 KULLANIM:${NC}"
echo -e "  • Ollama: ${YELLOW}ollama run selcuk-assistant${NC}"
echo -e "  • API: ${YELLOW}curl http://localhost:8000/api/chat -d '{\"message\":\"test\"}'${NC}\n"

echo -e "${GREEN}✨ Başarıyla tamamlandı!${NC}\n"
