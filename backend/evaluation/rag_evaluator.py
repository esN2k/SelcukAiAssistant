"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA: rag_evaluator.py                                                       ║
║  AMAÇ: RAG sistemi değerlendirme ve kalite güvence                            ║
║  ÖZELLİKLER:                                                                   ║
║    - RAGAS metrikleri (Faithfulness, Answer Relevancy, Context Precision)     ║
║    - Hallucination Detection                                                   ║
║    - Citation Accuracy                                                         ║
║    - Response Quality Scoring                                                  ║
║    - Automated Test Suite                                                      ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np

logger = logging.getLogger(__name__)

# Optional imports
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer, util
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


class MetricType(Enum):
    """Değerlendirme metrik türleri"""
    FAITHFULNESS = "faithfulness"
    ANSWER_RELEVANCY = "answer_relevancy"
    CONTEXT_PRECISION = "context_precision"
    CONTEXT_RECALL = "context_recall"
    HALLUCINATION = "hallucination"
    CITATION_ACCURACY = "citation_accuracy"


@dataclass
class EvaluationMetrics:
    """Değerlendirme metrikleri"""
    faithfulness: float = 0.0
    answer_relevancy: float = 0.0
    context_precision: float = 0.0
    context_recall: float = 0.0
    hallucination_score: float = 0.0
    citation_accuracy: float = 0.0
    overall_score: float = 0.0
    
    def calculate_overall(self, weights: Optional[Dict[str, float]] = None) -> float:
        """Ağırlıklı genel skor hesapla"""
        if weights is None:
            weights = {
                "faithfulness": 0.25,
                "answer_relevancy": 0.25,
                "context_precision": 0.20,
                "context_recall": 0.15,
                "hallucination_score": 0.15,
            }
        
        score = 0.0
        for metric, weight in weights.items():
            value = getattr(self, metric, 0.0)
            if metric == "hallucination_score":
                value = 1.0 - value
            score += value * weight
        
        self.overall_score = score
        return score
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "faithfulness": self.faithfulness,
            "answer_relevancy": self.answer_relevancy,
            "context_precision": self.context_precision,
            "context_recall": self.context_recall,
            "hallucination_score": self.hallucination_score,
            "citation_accuracy": self.citation_accuracy,
            "overall_score": self.overall_score,
        }


@dataclass
class EvaluationResult:
    """Tek bir değerlendirme sonucu"""
    query: str
    answer: str
    context: str
    ground_truth: Optional[str] = None
    metrics: EvaluationMetrics = field(default_factory=EvaluationMetrics)
    details: Dict[str, Any] = field(default_factory=dict)
    evaluated_at: str = ""
    
    def __post_init__(self):
        if not self.evaluated_at:
            self.evaluated_at = datetime.utcnow().isoformat()


class SemanticSimilarity:
    """Semantik benzerlik hesaplama"""
    
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError("sentence-transformers paketi gerekli")
        
        self.model = SentenceTransformer(model_name)
    
    def similarity(self, text1: str, text2: str) -> float:
        """İki metin arasındaki benzerlik"""
        emb1 = self.model.encode(text1, convert_to_tensor=True)
        emb2 = self.model.encode(text2, convert_to_tensor=True)
        return float(util.cos_sim(emb1, emb2)[0][0])
    
    def batch_similarity(self, queries: List[str], documents: List[str]) -> np.ndarray:
        """Batch benzerlik matrisi"""
        query_emb = self.model.encode(queries, convert_to_tensor=True)
        doc_emb = self.model.encode(documents, convert_to_tensor=True)
        return util.cos_sim(query_emb, doc_emb).numpy()


class HallucinationDetector:
    """Hallucination (uydurma bilgi) tespit sistemi"""
    
    HALLUCINATION_PATTERNS = [
        r"(?:şu an|şuan|şu anda)\s+(?:bilinmiyor|mevcut değil)",
        r"kesin olarak söyleyemem",
        r"tahmin ediyorum",
        r"sanırım|galiba|herhalde",
        r"(?:belki|muhtemelen)\s+\d+",
        r"(?:yaklaşık|civarında)\s+\d+(?:\s+(?:yıl|kişi|öğrenci))?",
    ]
    
    GROUNDING_KEYWORDS = [
        "kaynağa göre",
        "belgede belirtildiği",
        "metinde geçtiği",
        "bilgiye göre",
        "verilen bilgide",
    ]
    
    def __init__(self, use_llm: bool = True, gemini_api_key: Optional[str] = None):
        self.use_llm = use_llm and GEMINI_AVAILABLE
        
        if self.use_llm:
            api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            else:
                self.use_llm = False
                self.model = None
        else:
            self.model = None
        
        self._similarity: Optional[SemanticSimilarity] = None
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self._similarity = SemanticSimilarity()
            except Exception:
                pass
    
    def detect_pattern_hallucinations(self, answer: str) -> List[str]:
        """Pattern tabanlı hallucination tespit"""
        found = []
        for pattern in self.HALLUCINATION_PATTERNS:
            matches = re.findall(pattern, answer.lower())
            found.extend(matches)
        return found
    
    def check_grounding(self, answer: str) -> float:
        """Cevabın kaynaklara atıf yapıp yapmadığını kontrol et"""
        answer_lower = answer.lower()
        grounding_count = sum(1 for kw in self.GROUNDING_KEYWORDS if kw in answer_lower)
        return min(1.0, grounding_count / 2)
    
    def detect_with_context(self, answer: str, context: str) -> Tuple[float, List[str]]:
        """Bağlam ile hallucination tespit"""
        issues = []
        
        pattern_issues = self.detect_pattern_hallucinations(answer)
        if pattern_issues:
            issues.extend([f"Pattern: {p}" for p in pattern_issues])
        
        if self._similarity:
            sentences = re.split(r'[.!?]\s+', answer)
            for sent in sentences:
                if len(sent.strip()) > 20:
                    sim = self._similarity.similarity(sent, context)
                    if sim < 0.3:
                        issues.append(f"Low grounding: '{sent[:50]}...' (sim={sim:.2f})")
        
        hallucination_score = min(1.0, len(issues) / 5)
        
        return hallucination_score, issues
    
    def detect_with_llm(self, answer: str, context: str, query: str) -> Tuple[float, str]:
        """LLM ile hallucination tespit"""
        if not self.use_llm or not self.model:
            return 0.0, "LLM not available"
        
        prompt = f"""Aşağıdaki cevabın bağlamda verilen bilgilere sadık olup olmadığını değerlendir.

SORU: {query}

BAĞLAM:
{context[:2000]}

CEVAP:
{answer}

Değerlendirme kriterleri:
1. Cevaptaki TÜM bilgiler bağlamda mevcut mu?
2. Cevap bağlamda olmayan bilgi ekliyor mu?
3. Cevap doğru şekilde kaynak gösteriyor mu?

JSON formatında yanıt ver:
{{
    "faithfulness_score": 0.0-1.0 (1.0 = tamamen sadık),
    "hallucinated_claims": ["uydurulmuş iddialar listesi"],
    "explanation": "kısa açıklama"
}}"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
            
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                result = json.loads(json_match.group())
                score = 1.0 - result.get("faithfulness_score", 0.5)
                explanation = result.get("explanation", "")
                return score, explanation
            
            return 0.5, "Could not parse LLM response"
            
        except Exception as e:
            logger.warning(f"LLM hallucination detection error: {e}")
            return 0.5, str(e)
    
    def detect(
        self, 
        answer: str, 
        context: str, 
        query: str = ""
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Kapsamlı hallucination tespiti.
        
        Returns:
            (hallucination_score, details)
        """
        details = {}
        
        pattern_score = len(self.detect_pattern_hallucinations(answer)) / 5
        details["pattern_score"] = pattern_score
        
        grounding = self.check_grounding(answer)
        details["grounding_score"] = grounding
        
        context_score, context_issues = self.detect_with_context(answer, context)
        details["context_score"] = context_score
        details["context_issues"] = context_issues
        
        if self.use_llm and self.model:
            llm_score, llm_explanation = self.detect_with_llm(answer, context, query)
            details["llm_score"] = llm_score
            details["llm_explanation"] = llm_explanation
            
            final_score = (pattern_score * 0.2 + context_score * 0.3 + llm_score * 0.5)
        else:
            final_score = (pattern_score * 0.3 + context_score * 0.4 + (1 - grounding) * 0.3)
        
        return min(1.0, final_score), details


class RAGEvaluator:
    """
    RAG sistemi değerlendirici.
    
    RAGAS benzeri metrikler:
        - Faithfulness: Cevabın bağlama sadakati
        - Answer Relevancy: Cevabın soruya uygunluğu
        - Context Precision: Getirilen bağlamın hassasiyeti
        - Context Recall: Getirilen bağlamın kapsayıcılığı
    """
    
    def __init__(
        self,
        use_llm: bool = True,
        gemini_api_key: Optional[str] = None,
    ):
        self.use_llm = use_llm and GEMINI_AVAILABLE
        
        if self.use_llm:
            api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            else:
                self.use_llm = False
                self.model = None
        else:
            self.model = None
        
        self._similarity: Optional[SemanticSimilarity] = None
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self._similarity = SemanticSimilarity()
            except Exception:
                pass
        
        self.hallucination_detector = HallucinationDetector(
            use_llm=use_llm,
            gemini_api_key=gemini_api_key
        )
    
    def evaluate_faithfulness(self, answer: str, context: str) -> float:
        """Cevabın bağlama sadakatini değerlendir"""
        if not self._similarity:
            return 0.5
        
        answer_sentences = [s.strip() for s in re.split(r'[.!?]\s+', answer) if len(s.strip()) > 10]
        
        if not answer_sentences:
            return 0.5
        
        scores = []
        for sent in answer_sentences:
            sim = self._similarity.similarity(sent, context)
            scores.append(sim)
        
        return float(np.mean(scores)) if scores else 0.5
    
    def evaluate_answer_relevancy(self, query: str, answer: str) -> float:
        """Cevabın soruya uygunluğunu değerlendir"""
        if not self._similarity:
            return 0.5
        
        return self._similarity.similarity(query, answer)
    
    def evaluate_context_precision(
        self, 
        query: str, 
        contexts: List[str],
        ground_truth: Optional[str] = None
    ) -> float:
        """Getirilen bağlamların hassasiyetini değerlendir"""
        if not self._similarity or not contexts:
            return 0.5
        
        relevant_count = 0
        for ctx in contexts:
            sim = self._similarity.similarity(query, ctx)
            if sim > 0.5:
                relevant_count += 1
        
        return relevant_count / len(contexts)
    
    def evaluate_context_recall(
        self,
        context: str,
        ground_truth: str,
    ) -> float:
        """Bağlamın ground truth'u kapsama oranını değerlendir"""
        if not self._similarity or not ground_truth:
            return 0.5
        
        gt_sentences = [s.strip() for s in re.split(r'[.!?]\s+', ground_truth) if len(s.strip()) > 10]
        
        if not gt_sentences:
            return 0.5
        
        recalled = 0
        for sent in gt_sentences:
            sim = self._similarity.similarity(sent, context)
            if sim > 0.6:
                recalled += 1
        
        return recalled / len(gt_sentences)
    
    def evaluate_citation_accuracy(self, answer: str, context: str) -> float:
        """Atıf doğruluğunu değerlendir"""
        citation_pattern = r'\[(\d+)\]'
        citations = re.findall(citation_pattern, answer)
        
        if not citations:
            if "[" in context and "]" in context:
                return 0.3
            return 0.5
        
        context_citations = set(re.findall(citation_pattern, context))
        
        valid = sum(1 for c in citations if c in context_citations or int(c) <= 10)
        
        return valid / len(citations) if citations else 0.5
    
    def evaluate_with_llm(
        self,
        query: str,
        answer: str,
        context: str,
        ground_truth: Optional[str] = None,
    ) -> Dict[str, float]:
        """LLM ile kapsamlı değerlendirme"""
        if not self.use_llm or not self.model:
            return {}
        
        gt_section = f"\nDOĞRU CEVAP: {ground_truth}" if ground_truth else ""
        
        prompt = f"""Aşağıdaki RAG sisteminin cevabını değerlendir.

SORU: {query}

BAĞLAM:
{context[:2000]}

SİSTEM CEVABI:
{answer}
{gt_section}

Her bir kriteri 0.0-1.0 arasında puanla:

1. faithfulness: Cevap sadece bağlamdaki bilgileri mi kullanıyor?
2. answer_relevancy: Cevap soruyu tam olarak yanıtlıyor mu?
3. completeness: Cevap yeterince detaylı mı?
4. coherence: Cevap tutarlı ve anlaşılır mı?

JSON formatında yanıt ver:
{{
    "faithfulness": 0.0-1.0,
    "answer_relevancy": 0.0-1.0,
    "completeness": 0.0-1.0,
    "coherence": 0.0-1.0,
    "overall_quality": 0.0-1.0,
    "feedback": "kısa geri bildirim"
}}"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
            
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                return json.loads(json_match.group())
            
            return {}
            
        except Exception as e:
            logger.warning(f"LLM evaluation error: {e}")
            return {}
    
    def evaluate(
        self,
        query: str,
        answer: str,
        context: str,
        ground_truth: Optional[str] = None,
        contexts: Optional[List[str]] = None,
    ) -> EvaluationResult:
        """
        Kapsamlı RAG değerlendirmesi.
        
        Args:
            query: Kullanıcı sorusu
            answer: Sistem cevabı
            context: Kullanılan bağlam
            ground_truth: Doğru cevap (opsiyonel)
            contexts: Ayrı bağlam parçaları (opsiyonel)
        
        Returns:
            EvaluationResult
        """
        metrics = EvaluationMetrics()
        details = {}
        
        metrics.faithfulness = self.evaluate_faithfulness(answer, context)
        
        metrics.answer_relevancy = self.evaluate_answer_relevancy(query, answer)
        
        if contexts:
            metrics.context_precision = self.evaluate_context_precision(
                query, contexts, ground_truth
            )
        
        if ground_truth:
            metrics.context_recall = self.evaluate_context_recall(context, ground_truth)
        
        hall_score, hall_details = self.hallucination_detector.detect(
            answer, context, query
        )
        metrics.hallucination_score = hall_score
        details["hallucination"] = hall_details
        
        metrics.citation_accuracy = self.evaluate_citation_accuracy(answer, context)
        
        if self.use_llm:
            llm_eval = self.evaluate_with_llm(query, answer, context, ground_truth)
            details["llm_evaluation"] = llm_eval
            
            if llm_eval:
                metrics.faithfulness = (metrics.faithfulness + llm_eval.get("faithfulness", metrics.faithfulness)) / 2
                metrics.answer_relevancy = (metrics.answer_relevancy + llm_eval.get("answer_relevancy", metrics.answer_relevancy)) / 2
        
        metrics.calculate_overall()
        
        return EvaluationResult(
            query=query,
            answer=answer,
            context=context,
            ground_truth=ground_truth,
            metrics=metrics,
            details=details,
        )
    
    def evaluate_batch(
        self,
        test_cases: List[Dict[str, str]],
    ) -> List[EvaluationResult]:
        """
        Batch değerlendirme.
        
        Args:
            test_cases: [{"query": ..., "answer": ..., "context": ..., "ground_truth": ...}, ...]
        
        Returns:
            EvaluationResult listesi
        """
        results = []
        for case in test_cases:
            result = self.evaluate(
                query=case["query"],
                answer=case["answer"],
                context=case["context"],
                ground_truth=case.get("ground_truth"),
                contexts=case.get("contexts"),
            )
            results.append(result)
        
        return results
    
    def generate_report(
        self,
        results: List[EvaluationResult],
        output_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Değerlendirme raporu oluştur"""
        if not results:
            return {"error": "No results to report"}
        
        all_metrics = [r.metrics.to_dict() for r in results]
        
        avg_metrics = {}
        for key in all_metrics[0].keys():
            values = [m[key] for m in all_metrics]
            avg_metrics[key] = {
                "mean": float(np.mean(values)),
                "std": float(np.std(values)),
                "min": float(np.min(values)),
                "max": float(np.max(values)),
            }
        
        report = {
            "summary": {
                "total_evaluations": len(results),
                "average_overall_score": avg_metrics["overall_score"]["mean"],
                "average_faithfulness": avg_metrics["faithfulness"]["mean"],
                "average_relevancy": avg_metrics["answer_relevancy"]["mean"],
                "average_hallucination": avg_metrics["hallucination_score"]["mean"],
            },
            "detailed_metrics": avg_metrics,
            "individual_results": [
                {
                    "query": r.query[:100],
                    "metrics": r.metrics.to_dict(),
                }
                for r in results
            ],
            "generated_at": datetime.utcnow().isoformat(),
        }
        
        if output_path:
            Path(output_path).write_text(
                json.dumps(report, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.info(f"Report saved to {output_path}")
        
        return report


class TestSuite:
    """RAG sistemi test suite"""
    
    SELCUK_TEST_CASES = [
        {
            "query": "Selçuk Üniversitesi ne zaman kuruldu?",
            "expected_keywords": ["1975", "konya"],
            "category": "general",
        },
        {
            "query": "Akademik takvimde final sınavları ne zaman?",
            "expected_keywords": ["ocak", "final", "sınav"],
            "category": "academic_calendar",
        },
        {
            "query": "Bilgisayar Mühendisliği bölümü hangi fakültede?",
            "expected_keywords": ["teknoloji", "fakülte"],
            "category": "faculty",
        },
        {
            "query": "Kayıt yenileme tarihleri nedir?",
            "expected_keywords": ["kayıt", "tarih"],
            "category": "registration",
        },
        {
            "query": "Öğrenci yemekhanesi nerede?",
            "expected_keywords": ["yemekhane", "kampüs"],
            "category": "campus",
        },
    ]
    
    def __init__(self, rag_service, evaluator: Optional[RAGEvaluator] = None):
        self.rag_service = rag_service
        self.evaluator = evaluator or RAGEvaluator(use_llm=False)
    
    def run_test_case(self, test_case: Dict) -> Dict[str, Any]:
        """Tek test case çalıştır"""
        query = test_case["query"]
        expected_keywords = test_case.get("expected_keywords", [])
        
        try:
            context, citations = self.rag_service.get_context(query)
            
            keyword_matches = sum(
                1 for kw in expected_keywords 
                if kw.lower() in context.lower()
            )
            keyword_score = keyword_matches / len(expected_keywords) if expected_keywords else 0.5
            
            return {
                "query": query,
                "category": test_case.get("category", "unknown"),
                "passed": keyword_score >= 0.5,
                "keyword_score": keyword_score,
                "context_length": len(context),
                "citations_count": len(citations),
                "error": None,
            }
            
        except Exception as e:
            return {
                "query": query,
                "category": test_case.get("category", "unknown"),
                "passed": False,
                "keyword_score": 0.0,
                "error": str(e),
            }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Tüm testleri çalıştır"""
        results = []
        for case in self.SELCUK_TEST_CASES:
            result = self.run_test_case(case)
            results.append(result)
        
        passed = sum(1 for r in results if r["passed"])
        total = len(results)
        
        return {
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total if total > 0 else 0,
            "results": results,
            "timestamp": datetime.utcnow().isoformat(),
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("RAG Evaluator module loaded")
    print(f"Gemini available: {GEMINI_AVAILABLE}")
    print(f"Sentence Transformers available: {SENTENCE_TRANSFORMERS_AVAILABLE}")
