#!/usr/bin/env python3
"""
DOSYA ADI: benchmark_model.py
AMAÇ: Fine-tuned modeli base model ile karşılaştırmak
NE YAPAR:
  - Her iki modeli de aynı sorularla test eder
  - Doğruluk, hız, Türkçe kalite skorları hesaplar
  - Karşılaştırma raporu oluşturur
BAĞIMLILIKLAR:
  - ollama CLI
  - backend/data/test_questions.json
SON DEĞİŞİKLİK: 17.01.2026
"""

import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_test_questions() -> List[Dict]:
    """Test sorularını yükle"""
    test_file = Path("backend/data/test_questions.json")
    
    if not test_file.exists():
        logger.error(f"❌ Test soruları bulunamadı: {test_file}")
        return []
    
    with open(test_file, "r", encoding="utf-8") as f:
        return json.load(f)


def test_model(model_name: str, question: str) -> Dict:
    """
    Bir modeli tek bir soru ile test et
    
    Returns:
        {
            "answer": str,
            "response_time": float,
            "error": str or None
        }
    """
    start_time = time.time()
    
    try:
        result = subprocess.run(
            ["ollama", "run", model_name, question],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            answer = result.stdout.strip()
            return {
                "answer": answer,
                "response_time": elapsed,
                "error": None
            }
        else:
            return {
                "answer": "",
                "response_time": elapsed,
                "error": result.stderr
            }
    
    except subprocess.TimeoutExpired:
        return {
            "answer": "",
            "response_time": 30.0,
            "error": "Timeout (30s)"
        }
    except Exception as e:
        return {
            "answer": "",
            "response_time": 0,
            "error": str(e)
        }


def evaluate_answer(answer: str, expected_keywords: List[str]) -> float:
    """Cevabın kalitesini değerlendir (0-1 arası)"""
    if not answer:
        return 0.0
    
    # Keyword matching
    found_keywords = sum(1 for kw in expected_keywords if kw.lower() in answer.lower())
    keyword_score = found_keywords / max(len(expected_keywords), 1)
    
    # Cevap uzunluğu (çok kısa veya çok uzun kötü)
    length_score = 1.0
    if len(answer) < 20:
        length_score = 0.5
    elif len(answer) > 500:
        length_score = 0.8
    
    # Türkçe karakter varlığı
    turkish_chars = ['ı', 'ğ', 'ü', 'ş', 'ö', 'ç']
    has_turkish = any(char in answer.lower() for char in turkish_chars)
    turkish_score = 1.0 if has_turkish else 0.5
    
    # Toplam skor
    total_score = (keyword_score * 0.5 + length_score * 0.3 + turkish_score * 0.2)
    
    return total_score


def benchmark_models():
    """Ana benchmark fonksiyonu"""
    logger.info("\n" + "="*70)
    logger.info("🏁 MODEL BENCHMARK TESTİ")
    logger.info("="*70 + "\n")
    
    # Test sorularını yükle
    test_questions = load_test_questions()
    
    if not test_questions:
        logger.error("❌ Test soruları yüklenemedi")
        return
    
    logger.info(f"📝 {len(test_questions)} test sorusu yüklendi\n")
    
    # Test edilecek modeller
    models = {
        "Base Model (Turkcell)": "turkcell-llm-selcuk",  # Eski model
        "Fine-tuned (Selçuk)": "selcuk-assistant"        # Yeni model
    }
    
    results = {}
    
    # Her model için test
    for model_label, model_name in models.items():
        logger.info(f"\n{'='*70}")
        logger.info(f"🧪 Test ediliyor: {model_label}")
        logger.info(f"{'='*70}\n")
        
        # Model mevcut mu kontrol et
        check_result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True
        )
        
        if model_name not in check_result.stdout:
            logger.warning(f"⚠️  Model bulunamadı: {model_name}, atlanıyor")
            continue
        
        model_results = {
            "total_questions": len(test_questions),
            "response_times": [],
            "accuracy_scores": [],
            "errors": 0
        }
        
        for i, test_case in enumerate(test_questions, 1):
            question = test_case["question"]
            expected_keywords = test_case["expected_keywords"]
            
            logger.info(f"Soru {i}/{len(test_questions)}: {question}")
            
            # Test et
            result = test_model(model_name, question)
            
            if result["error"]:
                logger.error(f"  ❌ Hata: {result['error']}")
                model_results["errors"] += 1
            else:
                # Değerlendir
                accuracy = evaluate_answer(result["answer"], expected_keywords)
                
                model_results["response_times"].append(result["response_time"])
                model_results["accuracy_scores"].append(accuracy)
                
                logger.info(f"  ✅ Yanıt Süresi: {result['response_time']:.2f}s")
                logger.info(f"  📊 Doğruluk: {accuracy:.1%}")
                logger.info(f"  💬 Cevap: {result['answer'][:100]}...")
            
            logger.info("")
        
        # Ortalama metrikleri hesapla
        if model_results["response_times"]:
            model_results["avg_response_time"] = sum(model_results["response_times"]) / len(model_results["response_times"])
            model_results["avg_accuracy"] = sum(model_results["accuracy_scores"]) / len(model_results["accuracy_scores"])
        else:
            model_results["avg_response_time"] = 0
            model_results["avg_accuracy"] = 0
        
        results[model_label] = model_results
    
    # Karşılaştırma raporu
    logger.info("\n" + "="*70)
    logger.info("📊 KARŞILAŞTIRMA RAPORU")
    logger.info("="*70 + "\n")
    
    # Tablo başlıkları
    print(f"{'Model':<30} {'Ortalama Süre':<15} {'Doğruluk':<12} {'Hata':<8}")
    print("-" * 70)
    
    for model_label, metrics in results.items():
        print(
            f"{model_label:<30} "
            f"{metrics['avg_response_time']:>10.2f}s     "
            f"{metrics['avg_accuracy']:>8.1%}     "
            f"{metrics['errors']:>4}/{metrics['total_questions']}"
        )
    
    # İyileştirme yüzdesi
    if len(results) == 2:
        base_label, fine_label = list(results.keys())
        base_metrics = results[base_label]
        fine_metrics = results[fine_label]
        
        if base_metrics["avg_accuracy"] > 0:
            accuracy_improvement = ((fine_metrics["avg_accuracy"] - base_metrics["avg_accuracy"]) / base_metrics["avg_accuracy"]) * 100
        else:
            accuracy_improvement = 0
            
        if base_metrics["avg_response_time"] > 0:
            speed_improvement = ((base_metrics["avg_response_time"] - fine_metrics["avg_response_time"]) / base_metrics["avg_response_time"]) * 100
        else:
            speed_improvement = 0
        
        logger.info(f"\n{'='*70}")
        logger.info("📈 İYİLEŞTİRME")
        logger.info(f"{'='*70}")
        logger.info(f"Doğruluk: {accuracy_improvement:+.1f}%")
        logger.info(f"Hız: {speed_improvement:+.1f}%")
    
    # JSON raporu kaydet
    output_file = Path("backend/models/benchmark_report.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n💾 Rapor kaydedildi: {output_file}")


if __name__ == "__main__":
    benchmark_models()
